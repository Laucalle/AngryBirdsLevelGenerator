from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
#import numpy as np

ext_modules = [
    Extension('cy_example',
              ['cy_example.pyx'],
              # Note here that the C++ language was specified
              # The default language is C
              language="c++",
              include_dirs= ['./Box2D_v2.1.2/Box2D'],
              #extra_objects = ['./DebugSimulation/obj/simulation.o'],
              extra_objects=["./Box2D_v2.1.2/Box2D/Build/Box2D/libBox2D.a"],
              library_dirs=['./Box2D_v2.1.2/Box2D']
              ),
    ]

setup(
    name = 'cy_example',
    package_dir = {'AngryBirdsGA': ''},
    cmdclass = {'build_ext': build_ext},
    ext_modules = cythonize(ext_modules), # cythonize("cy_example.pxd"),
    # include_dirs=[np.get_include()]  # This gets all the required Numpy core files
)
