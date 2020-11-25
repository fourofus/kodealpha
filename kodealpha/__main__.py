import asyncio
from kodealpha import __version__, server

import logging


def main():
    print(f"Hello, I'm Kode Alpha ({__version__})")

    asyncio.run(server())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
