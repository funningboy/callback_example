
from distutils.core import setup
from distutils.extension import Extension

setup(
  name = 'pycallback',
  ext_modules = [Extension("cpypthread",
        libraries=['pthread'],
        sources = ["cpypthread.c"],
      )],
)
