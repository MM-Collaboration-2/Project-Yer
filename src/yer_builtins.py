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
    string = ''.join(str(p) for p in params)
    print(string)
    return Integer(len(params))


def len_func(params: list[Object]):

    print('in len', params)
    if len(params) < 1:
        return Integer(0)

    param = get_object(params[0])
    print(param)

    if param.type in ['list', 'string']:
        return Integer(param.len())
    return Integer(0)


def get_func(params: list[Object]):
    print('in get', params)
    if len(params) < 2:
        return Integer(0)

    param1: Object = get_object(params[0])

    param2: Object = get_object(params[1])

    if param1.type not in ['list', 'string'] or param2.type != 'integer':
        return Integer(0)
    if 0 <= param2.data < len(param1.data):
        return param1.get([param2.data])
    return Integer(0)


BUILTINS: dict[str, Variable] = {

    'yell': Variable('yell', BuiltIn(yell_func)),
    'len': Variable('len', BuiltIn(len_func)),
    'get': Variable('get', BuiltIn(get_func)),
}

if __name__ == '__main__':
    from list import List
    lst: list[Object] = [Integer(1), Integer(2), Integer(3)] 
    print(len_func([List(lst)]))
