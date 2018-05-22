import random
import time

Random = random.Random(time.time())

def random_set_seed(x):
    return random.Random(x)

STRING_XML =""

BLOCKS = {'0':[0.84,0.84], '1':[0.85,0.43], '2':[0.43,0.43],
          '3':[0.22,0.22], '4':[0.43,0.22], '5':[0.85,0.22],
          '6':[1.68,0.22], '7':[2.06,0.22]}
# additional objects number and size
ADDITIONAL_OBJECT_SIZES = {'1':[0.82, 0.82], '2':[0.82, 0.82], '3':[0.8, 0.8], '4':[0.45, 0.45]}
# additional objects number and name
ADDITIONAL_OBJECTS = {'1': "TriangleHole", '2': "Triangle", '3': "Circle", '4': "CircleSmall"}
# blocks number and name
# (blocks 3, 7, 9, 11 and 13) are their respective block names rotated 90 derees clockwise
BLOCK_NAMES = {'0':"SquareHole", '1':"RectFat", '2':"SquareSmall",
               '3':"SquareTiny", '4':"RectTiny", '5':"RectSmall",
               '6':"RectMedium", '7':"RectBig"}

MATERIALS = ["wood", "stone", "ice"]

ABSOLUTE_GROUND = -3.3 #Real -3.5
# desirable number of blocks
B = 10
MAX_B = 20
MIN_B = 5

MAX_X = 5
MIN_X = 0
MAX_Y = 0
MIN_Y = ABSOLUTE_GROUND
SMALLEST_STEP = 0.21
ROTATION = ["0", "45", "90", "135"]
#Rotation = ["0", "90"]



PIGS = [
    "BasicSmall",
    "BasicMedium",
    "BasicLarge"
]
BIRDS = [
    "BirdRed",
    "BirdBlue",
    "BirdWhite"
]
IDX_TO_BLOCK = [
    ("Circle", "wood"),
    ("Circle", "stone"),
    ("Circle", "ice"),
    ("CircleSmall", "wood"),
    ("CircleSmall", "stone"),
    ("CircleSmall", "ice"),
    ("RectBig", "wood"),
    ("RectBig", "stone"),
    ("RectBig", "ice"),
    ("RectFat", "wood"),
    ("RectFat", "stone"),
    ("RectFat", "ice"),
    ("RectMedium", "wood"),
    ("RectMedium", "stone"),
    ("RectMedium", "ice"),
    ("RectSmall", "wood"),
    ("RectSmall", "stone"),
    ("RectSmall", "ice"),
    ("RectTiny", "wood"),
    ("RectTiny", "stone"),
    ("RectTiny", "ice"),
    ("SquareHole", "wood"),
    ("SquareHole", "stone"),
    ("SquareHole", "ice"),
    ("SquareSmall", "wood"),
    ("SquareSmall", "stone"),
    ("SquareSmall", "ice"),
    ("SquareTiny", "wood"),
    ("SquareTiny", "stone"),
    ("SquareTiny", "ice"),
    ("Triangle", "wood"),
    ("Triangle", "stone"),
    ("Triangle", "ice"),
    ("TriangleHole", "wood"),
    ("TriangleHole", "stone"),
    ("TriangleHole", "ice"),
    ("BasicSmall", ""),  # Pig
    ("BasicMedium", ""),  # Pig
    ("BasicLarge", ""),  # Pig
    ("", "")  # TNT does not have type or material
]


def getTag(number):
    if number < 36:
        return "Block"
    if number < 39:
        return "Pig"
    return "TNT"
