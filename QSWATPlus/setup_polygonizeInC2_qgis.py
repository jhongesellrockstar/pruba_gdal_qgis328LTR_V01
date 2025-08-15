# setup_polygonizeInC2_qgis.py
from distutils.core import setup
from Cython.Build import cythonize
import numpy
import os

os.environ["INCLUDE"] = r"C:\PROGRA~1\QGIS32~1.8\apps\Python39\include"
setup(
    name="polygonizeInC2",
    ext_modules=cythonize("polygonizeInC2.pyx"),
    include_dirs=[numpy.get_include(), os.environ["INCLUDE"]],
)
