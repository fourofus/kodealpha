__version__ = '0.0.0a'

from kodealpha.server import KodeAppFactory, KodeService


async def server():
    try:
        print(f'Kode server ({__version__}) started')
        app = KodeAppFactory().create_app()
        await KodeService(app).start()
    finally:
        print(f'Kode server ({__version__}) finished.')
