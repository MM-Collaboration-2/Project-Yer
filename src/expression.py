from utils import token_type, infix_to_postfix, smart_split_comma
from stack import Stack
from object import Object
from void import Void
from integer import Integer
from list import List
from variable import Variable
from basic_types import BASIC_TYPES
from storage import Storage
from operation import Operation
from construction import Construction
from callable import Function, BuiltIn


class Expression(Construction):                                     # Выражение состоит из одного или нескольких базовых выражений
    name: str = 'Exprssion'
    def __init__(self, string: str, storage: Storage, return_flag: bool=False):
        self.storage: Storage = storage
        self.string: str = string
        self.postfix: list[str] = infix_to_postfix(self.clear())
        self.return_flag: bool = return_flag
        self.delete_flag: bool = False


    def clear(self):
        if self.string.startswith('Expr{'):
            return self.string[:-1].replace('Expr{', '')
        return self.string
        
    def run(self):                                                  # создаем конвейер из элементарных выражений
        #result: Object = Integer(0)
        #######
        result: Object = Void()
        #######
        stack: Stack = Stack()
        for token in self.postfix:
            tok_type = token_type(token)

            if tok_type == 'operation':                             # если переменная если оператор -- создаем базовую операцию

                if token == 'return':
                    self.return_flag = True
                    self.delete_flag = True
                    continue

                rop = stack.pop()
                lop = stack.pop()
                op = token
                
                result = Operation.run(lop, rop, op, self.storage)
                # Здесь валидировать операнды
                # так как результат операции возвращается обратно в стек
                # т.е. тип возвращаемого операцией объекта
                # должен быть таким же как и тип объектов в стеке
                # -- строка или Object.
                # Конвертить строку в объект потом обратно в строку 
                # чтобы засунутть в стек неоч логично
                # лучше уж на ходу здесь токены в объекты валидировать
                #result = basic_expression.run()
                stack.push(result)                                  # помещаем результат выражения в обратно в стек
            else:


                obj = self.validate_operand(token, tok_type, self.storage)  # чтобы возвращать последний добавленный операндб в случае если
                result = obj
                stack.push(obj)                                     # помещаем в стек

        if self.return_flag:
            # чисим аргументы после выполнения функции
            # удаление списка аргументов из стека аргументов хранилища

            # если не было оператора return, не удаляем аргументы
            if self.delete_flag:
                self.storage.del_arguments()
            # возвращаем результат
            return result                                               # для использования в условиях и циклах

        # возвращаем пустоту
        return Void()


    @classmethod
    def validate_operation(cls, token: str):
        # обработка return и += -= ...
        pass


    @classmethod
    def validate_basic_object(cls, token: str, tok_type: str) -> Object:
        obj = BASIC_TYPES[tok_type](token)
        return obj


    @classmethod
    def validate_list(cls, token: str, storage: Storage) -> List:
        # очистка от скобочек
        token = token[1:-1]

        lst: list[Object] = []

        exprs: list[Expression] = smart_split_comma(token)


        ### здесь $argv в экспрешне не валидируется
        for expr in exprs:
            expr = Expression(expr, storage, True)
            obj = expr.run()
            if obj.type == 'void':
                continue
            lst.append(obj)
        return List(lst)

    @classmethod
    def validate_variable(cls, token: str, storage: Storage):
        if storage.declared(token):
            variable: Variable = storage.get(token)

        else:
            variable: Variable = Variable(token, Integer(0)) # создаем новую
            storage.add(variable);
        
        return variable

    @classmethod
    def validate_argument(cls, token: str, storage: Storage):

        # получаем номер аргумента в списке аргументов
        num = int(token.replace('$argv', ''))
        arguments = storage.get_arguments()
        if 0 <= num < len(arguments):
            return arguments[num]
        return Integer(0)

    @classmethod
    def validate_function(cls, token: str, storage: Storage):

        # получаем строку с аргументами
        arguments_str: str = token[token.find('(')+1:-1]
        arguments_str = '[' + arguments_str + ']'


        # получаем список с аргументами
        argument_list = cls.validate_list(arguments_str, storage).data 

        # имя функции
        function_name: str = token[:token.find('(')]  

        # функция хранится как объект, помещенный в переменную
        var: Variable = cls.validate_variable(function_name, storage)

        # извлекаем функцию function:
        function: Object = var.obj

        if function.type == 'function':
            if function.specification == 'userdefined':

                # одобавляем список параметров в хранилице аргументов
                storage.add_arguments(argument_list) 
                obj: Object = function.run()

            elif function.specification == 'builtin':

                # builtin функции не изменяют стек списков парамеров
                # так как из выполнение не предусмтаривает 
                # использование оператора return
                obj: Object = function.run(argument_list, storage)

        else:
            obj: Object = Integer(0)

        return obj

    

    @classmethod
    def validate_operand(cls, token: str, tok_type: str, storage: Storage) -> Object:

        if tok_type == 'variable':
            var: Variable = cls.validate_variable(token, storage)
            return var

        elif tok_type == 'function':
            obj: Object = cls.validate_function(token, storage)
            return obj


        elif tok_type == 'list':
            lst: List = cls.validate_list(token, storage)
            return lst

        elif tok_type == 'argument':
            obj: Object = cls.validate_argument(token, storage)
            return obj
        
        else:
            obj: Object = cls.validate_basic_object(token, tok_type) 
            return obj


    def __repr__(self):
        return f'{self.string};'

if __name__ == '__main__':
    text = '[1+2] + ["aboba", []]'
    s = Storage({}, Stack())
    e = Expression(text, s, True)
    print(e.run())
