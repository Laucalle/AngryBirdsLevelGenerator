# distutils: libraries = ./Box2D_v2.1.2/Box2D/Build/Box2D/libBox2D.a
# distutils: include_dirs = ./Box2D_v2.1.2/Box2D/

cimport cy_example # Import the pxd "header"
cimport cython
from libc.stdlib cimport malloc, free

# Import some functionality from Python and the C stdlib
from cpython.pycapsule cimport *

from AngryBirdsGA import *
# Python wrapper functions.

def psilly(list_of_blocks):

    array_of_block_data = <float *>malloc(6 * len(list_of_blocks) * cython.sizeof(float))

    if array_of_block_data is NULL:
        raise MemoryError()

    for i in xrange(len(list_of_blocks)):
        array_of_block_data[i*6    ] = list_of_blocks[i].x
        array_of_block_data[i*6 + 1] = list_of_blocks[i].y
        array_of_block_data[i*6 + 2] = BLOCKS[str(list_of_blocks[i].type)][0]/2 
        array_of_block_data[i*6 + 3] = BLOCKS[str(list_of_blocks[i].type)][1]/2
        array_of_block_data[i*6 + 4] = float(ROTATION[list_of_blocks[i].rot])
        array_of_block_data[i*6 + 5] = 0.3


    cy_example.world_simulation(array_of_block_data, 6, len(list_of_blocks))
    free(array_of_block_data)
