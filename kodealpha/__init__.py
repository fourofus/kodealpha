import asyncio

from aiohttp import web
from aiohttp.abc import AbstractAccessLogger
from aiohttp.web import normalize_path_middleware

__version__ = '0.0.0a'


class ApiLogger(AbstractAccessLogger):
    """
    Only logs requests including /api/.
    """

    def log(self, request, response, time):
        if request.path.startswith('/api'):
            self.logger.info(f'{request.remote} {request.method} {request.path}')


class KodeAppFactory:
    def create_app(self):
        app = web.Application(middlewares=[
            normalize_path_middleware(append_slash=False, remove_slash=True, merge_slashes=True)]
        )

        app.add_routes([
            web.get('/', self.handler),
            web.get('/api/{general}', self.handler)
        ])
        return app

    @staticmethod
    async def handler(request):
        general = request.match_info.get('general', 'unknown')
        return web.Response(text=f'Received "{general}"')


class KodeService:
    def __init__(self, app: web.Application):
        self.app = app

    async def start(self):
        """ Starts KODE service.
        References:
            Application runners: https://docs.aiohttp.org/en/stable/web_advanced.html
        :return: None
        """
        runner = web.AppRunner(self.app, access_log_class=ApiLogger)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', 8080)
        await site.start()
        while True:
            try:
                await asyncio.sleep(100)
            except asyncio.CancelledError:
                print('Server cancelled')
                break


async def server():
    try:
        print(f'Kode server ({__version__}) started')
        app = KodeAppFactory().create_app()
        await KodeService(app).start()
    finally:
        print(f'Kode server ({__version__}) finished.')
