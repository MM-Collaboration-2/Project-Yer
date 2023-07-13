from expression_block import ExpressionBlock
from block import Block
from control_structures import *
from main import Main
from function_block import FunctionBlock


global CONSTRUCTIONS_OBJECTS
CONSTRUCTIONS_OBJECTS = [ExpressionBlock, Block, If, While, For, Main,
                         FunctionBlock]
global CONSTRUCTIONS_HEADS
CONSTRUCTIONS_HEADS = {c.name: c for c in CONSTRUCTIONS_OBJECTS}
global CONSTRUCTIONS_TYPES
CONSTRUCTIONS_TYPES = {c.regex: c for c in CONSTRUCTIONS_OBJECTS}
