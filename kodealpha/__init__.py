import asyncio
from aiohttp import web
from aiohttp.abc import AbstractAccessLogger

__version__ = '0.0.0a'


class KodeAccessLogger(AbstractAccessLogger):
    def log(self, request, response, time):
        self.logger.info(f'{request.remote} {request.method} {request.path}')


class KodeAppFactory:
    def create_app(self):
        app = web.Application()
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
        runner = web.AppRunner(self.app)
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
