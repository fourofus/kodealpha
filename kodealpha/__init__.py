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
            normalize_path_middleware(append_slash=False, remove_slash=True, merge_slashes=True)
        ])

        app.add_routes([
            web.get('/', self.default_handler),
            web.get('/{misc}', self.default_handler),
            web.get('/api/greeting', self.greeting_handler, name='greeting_default'),
            web.get('/api/greeting/{message}', self.greeting_handler, name='greeting_message'),
        ])
        return app

    @staticmethod
    async def greeting_handler(request):
        message = request.match_info.get('message', '')
        if message:
            return web.Response(text=f'Received "{message}"')
        return web.Response(text=f'Hello there, hope you are having a fine day!')

    @staticmethod
    async def default_handler(request):
        try:
            location = request.app.router['greeting_default'].url_for()
            raise web.HTTPFound(location=location)
        except KeyError as e:
            return web.Response(text=f'Cannot redirect. Sorry I failed. "{e.__class__}:{e}"')


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
