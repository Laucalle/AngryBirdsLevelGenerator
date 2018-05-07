
STRING_XML =""

BLOCKS = {'1':[0.84, 0.84], '2':[0.85, 0.43], '3':[0.43, 0.85], '4':[0.43, 0.43],
          '5':[0.22,0.22], '6':[0.43,0.22], '7':[0.22,0.43], '8':[0.85,0.22],
          '9':[0.22,0.85], '10':[1.68,0.22], '11':[0.22,1.68],
          '12':[2.06,0.22], '13':[0.22,2.06]}
# additional objects number and size
ADDITIONAL_OBJECT_SIZES = {'1':[0.82, 0.82], '2':[0.82, 0.82], '3':[0.8, 0.8], '4':[0.45, 0.45]}
# additional objects number and name
ADDITIONAL_OBJECTS = {'1': "TriangleHole", '2': "Triangle", '3': "Circle", '4': "CircleSmall"}
# blocks number and name
# (blocks 3, 7, 9, 11 and 13) are their respective block names rotated 90 derees clockwise
BLOCK_NAMES = {'1': "SquareHole", '2': "RectFat", '3': "RectFat", '4': "SquareSmall",
               '5':"SquareTiny", '6':"RectTiny", '7':"RectTiny", '8':"RectSmall",
               '9':"RectSmall",'10':"RectMedium",'11':"RectMedium",
               '12':"RectBig",'13':"RectBig"}

MATERIALS = ["wood", "stone", "ice"]

ABSOLUTE_GROUND = -3.5
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
