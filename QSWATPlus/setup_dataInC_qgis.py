# setup_dataInC_qgis.py
from distutils.core import setup
from Cython.Build import cythonize
import numpy
import os

include_path = numpy.get_include()
print("Include path:", include_path)

setup(
    name="dataInC",
    ext_modules=cythonize("dataInC.pyx"),
    include_dirs=[include_path]
)
