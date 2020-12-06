import asyncio

from aiohttp import web
from aiohttp.abc import AbstractAccessLogger
from aiohttp.web_middlewares import normalize_path_middleware

from kodealpha.parser import RequestParser
from kodealpha.strings import GENERAL_RESPONSES


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
            web.get('/api/general', self.general_handler, name='general'),
            web.get('/api/general/{message}', self.general_handler, name='general_message'),
        ])
        return app

    @staticmethod
    async def general_handler(request):
        parser = RequestParser()
        message = request.match_info.get('message', '')
        if message:
            msg_type = parser.parse(message)['type']
            if msg_type == RequestParser.MessageType.Greeting:
                return web.Response(text=f'[{msg_type}] {GENERAL_RESPONSES["REPLY_TO_GREETING"]} ')
            if msg_type == RequestParser.MessageType.Insulting:
                return web.Response(text=f'[{msg_type}] {GENERAL_RESPONSES["REPLY_TO_INSULTING"]}')
        return web.Response(text=f'[{RequestParser.MessageType.Unknown}] {GENERAL_RESPONSES["GENERAL_REPLY"]}')

    @staticmethod
    async def default_handler(request):
        try:
            location = request.app.router['general'].url_for()
            raise web.HTTPFound(location=location)
        except KeyError as e:
            return web.Response(text=f'Cannot redirect due to "{e.__class__}:{e}"')


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
