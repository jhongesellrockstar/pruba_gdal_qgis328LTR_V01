from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name="jenks",
    ext_modules=cythonize("jenks.pyx"),
    include_dirs=[numpy.get_include()],
)
