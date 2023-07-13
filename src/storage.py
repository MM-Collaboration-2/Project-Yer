from stack import Stack
from object import Object
from integer import Integer
from variable import Variable
from construction import Construction


class Storage():                            # Хранилище переменных
    def __init__(self, variables: dict, arguments_stack: Stack):         # и функций в будущем
        self.variables: dict[str, Variable] = variables
        ####
        self.arguments_stack: Stack = arguments_stack

    ####
    def add_arguments(self, arguments: list[Object]):
        self.arguments_stack.push(arguments)

    ####
    def get_arguments(self) -> Object:
        if self.arguments_stack.is_empty:
            return []
        return self.arguments_stack.peek()

    ####
    def del_arguments(self):
        if not self.arguments_stack.is_empty():
            self.arguments_stack.pop()

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

