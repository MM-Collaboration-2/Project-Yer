from object import Object
from integer import Integer
from string import String
from variable import Variable
from callable import BuiltIn
from storage import Storage
from execute import execute
from list import List





def get_object(param: Object) -> Object:

    if param.type == 'variable':
        param: Object = param.obj
    return param


# functions to send to BuiltIn object
def yell_func(params: list[Object], storage: Storage):
    string = ''.join(str(p) for p in params)
    print(string)
    return Integer(len(params))


def len_func(params: list[Object], storage: Storage):

    if len(params) < 1:
        return Integer(0)

    param = get_object(params[0])

    if param.type in ['list', 'string']:
        return Integer(param.len())
    return Integer(0)


def get_func(params: list[Object], storage: Storage):
    if len(params) < 2:
        return Integer(0)

    param1: Object = get_object(params[0])

    param2: Object = get_object(params[1])

    if param1.type not in ['list', 'string'] or param2.type != 'integer':
        return Integer(0)
    if 0 <= param2.data < len(param1.data):
        return param1.get(param2.data)
    return Integer(0)


def type_func(params: list[Object], storage: Storage):
    if len(params) > 0:
        param = get_object(params[0])
        return String(param.type)
    return Integer(0)
    

def screw_on_func(params: list[Object], storage: Storage):
    counter: int = 0
    for param in params:
        if param.type == 'string':
            if execute(param.data, storage):
                counter += 1
    return Integer(counter)
    

def defined_func(params: list[Object], storage: Storage):
    lst = []
    for name, data in storage.variables.items():
        sublst = []
        sublst.append(String(name))
        sublst.append(data)
        lst.append(List(sublst))
    return List(lst)



BUILTINS: dict[str, Variable] = {

    'yell': Variable('yell', BuiltIn(yell_func)),
    'len': Variable('len', BuiltIn(len_func)),
    'get': Variable('get', BuiltIn(get_func)),
    'type': Variable('type', BuiltIn(type_func)),
    'screw_on': Variable('screw_on', BuiltIn(screw_on_func)),
    'defined': Variable('defined', BuiltIn(defined_func)),
}

if __name__ == '__main__':
    from stack import Stack
    string = String("test")
    s = Storage(BUILTINS, Stack())
    screw_on_func([string], s)
    print(defined_func([], s))
