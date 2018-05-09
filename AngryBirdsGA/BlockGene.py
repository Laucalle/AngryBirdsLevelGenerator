import math
from AngryBirdsGA import *
import numpy as np


class BlockGene:
    def __init__(self, type, pos, r):
        self.type = type
        self.x = pos[0]
        self.y = pos[1]
        self.rot = r
        self.mat = 0
        self._corners = None

    def __eq__(self, other):

        return self.type == other.type and self.x == other.x and self.y == other.y and \
               self.rot == other.rot and self.mat == other.mat

    def corners(self):
        """ computes and returns corners of the figure """

        if self._corners:
            return self._corners
        else:
            dims = [BLOCKS[str(self.type)][0]/2, BLOCKS[str(self.type)][1]/2]
            sinA = math.sin(math.radians(int(ROTATION[self.rot])))
            cosA = math.cos(math.radians(int(ROTATION[self.rot])))
            
            p_1 = np.array([cosA*(+dims[0]) - sinA*(+dims[1]) + self.x, cosA*(+dims[1]) + sinA*(+dims[0]) + self.y])
            p_2 = np.array([cosA*(+dims[0]) - sinA*(-dims[1]) + self.x, cosA*(-dims[1]) + sinA*(+dims[0]) + self.y])
            p_3 = np.array([cosA*(-dims[0]) - sinA*(-dims[1]) + self.x, cosA*(-dims[1]) + sinA*(-dims[0]) + self.y])
            p_4 = np.array([cosA*(-dims[0]) - sinA*(+dims[1]) + self.x, cosA*(+dims[1]) + sinA*(-dims[0]) + self.y])
            self._corners = [p_1,p_2,p_3,p_4]

            return self._corners

    def toString(self):
        return 'Type: {0} pos: ({1},{2}) rot:{3}'.format(str(self.type), str(self.x), str(self.y), str(self.rot))

    
