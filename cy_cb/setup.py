from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

setup(
  name = 'cycallback',
  ext_modules=cythonize([
    Extension("ccycheese",
        sources = ["ccycheese.pyx", "ccycheesefinder.c"]),
    ]),
)
