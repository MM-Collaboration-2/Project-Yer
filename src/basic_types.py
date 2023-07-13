from object import Object
from integer import Integer
from string import String
from float import Float
from list import List
from variable import Variable

global BASIC_OBJECTS
BASIC_OBJECTS: list[Object] = [Integer, Float, String, List, Variable]

global BASIC_TYPES
BASIC_TYPES: dict[str: Object] = {obj.type: obj for obj in BASIC_OBJECTS}
