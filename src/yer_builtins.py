from object import Object
from integer import Integer
from variable import Variable
from callable import BuiltIn




def get_object(param: Object) -> Object:

    if param.type == 'variable':
        param: Object = param.obj
    return param


# functions to send to BuiltIn object
def yell_func(params: list[Object]):
    string = ' '.join(str(p) for p in params)
    print(string)
    return Integer(len(params))


def len_func(params: list[Object]):

    if len(params) < 1:
        return Integer(0)

    param = get_object(params[0])

    if param.type != 'list':
        return Integer(0)
    return Integer(param.len())


def get_func(params: list[Object]):
    if len(params) < 2:
        return Integer(0)

    param1: Object = get_object(params[0])

    param2: Object = get_object(params[1])

    if param1.type != 'list' or param2.type != 'integer':
        return Integer(0)
    if 0 <= param2.data < param1.len():
        return param1.get(param2.data)
    return Integer(0)


BUILTINS: dict[str, Variable] = {

    'yell': Variable('yell', BuiltIn(yell_func)),
    'len': Variable('len', BuiltIn(len_func)),
    'get': Variable('get', BuiltIn(get_func)),
}
