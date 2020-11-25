from kodealpha import __version__
from setuptools import setup

setup(name='kodealpha-alpha',
      version=__version__,
      packages=['kodealpha'],
      entry_points={
          'console_scripts': [
              'kodealpha-alpha=kodealpha.__main__:main']
      })
