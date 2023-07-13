from object import Object
from integer import Integer
from variable import Variable
from construction import Construction

#from function import Function

class Storage():                            # Хранилище переменных
    def __init__(self, variables: dict, arguments: list=[]):         # и функций в будущем
        self.variables: dict[str, Variable] = variables
        ####
        self.arguments: list[Object] = arguments

    ####
    def set_arguments(self, arguments: list[Object]):
        self.arguments = arguments

    ####
    def get_argument(self, index: int) -> Object:
        if 0 <= index < len(self.arguments) - 1:
            return self.arguments[index]
        return Integer(0)

    def add(self, variable: Variable) -> None:
        self.variables[variable.name] = variable

    def set(self, name: str, obj: Object) -> None:
        if self.declared(name):
            self.get(name).obj = obj

    def remove_variable(self, name: str) -> None:
        if self.declared:
            del self.variables[name]

    def get(self, name: str) -> Variable:
        var = self.variables.get(name, None)
        return var

    def declared(self, name: str) -> bool:
        if self.get(name):
            return True
        return False

    def type(self, name: str) -> str:
        if self.declared(name):
            return self.get(name).type
        return ''

