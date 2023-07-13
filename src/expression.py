from utils import tokens, token_type, infix_to_postfix
from stack import Stack
from object import Object
from integer import Integer
from list import List
from variable import Variable
from basic_types import BASIC_TYPES
from storage import Storage
from operation import Operation
from construction import Construction


class Expression(Construction):                                     # Выражение состоит из одного или нескольких базовых выражений
    name: str = 'Exprssion'
    def __init__(self, string: str, storage: Storage):
        self.storage: Storage = storage
        self.string: str = string
        self.postfix: list[str] = infix_to_postfix(self.clear())

    def clear(self):
        if self.string.startswith('Expr{'):
            return self.string[:-1].replace('Expr{', '')
        return self.string
        
    def run(self):                                                  # создаем конвейер из элементарных выражений
        result: Object
        stack: Stack = Stack()
        for token in self.postfix:
            tok_type = token_type(token)

            if tok_type == 'operation':                             # если переменная если оператор -- создаем базовую операцию
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
                                                                            # экспрешн состоит из одного операнда
                result = obj
                
                stack.push(obj)                                     # помещаем в стек

        return result                                               # для использования в условиях и циклах

    @classmethod
    def validate_list(cls, string: str, storage: Storage) -> List:
        lst = []

        # очистка от скобочек
        if string.startswith('['):
            string = string[1:]
        if string.endswith(']'):
            string = string[:-1]

        objects = tokens(string)
        for token in objects:
            tok_type = token_type(token)
            lst.append(cls.validate_operand(token, tok_type, storage))
        return List(lst)

    @classmethod
    def validate_variable(cls, token, storage: Storage):
        if storage.declared(token):
            variable: Variable = storage.get(token)

        else:
            variable: Variable = Variable(token, Integer(0)) # создаем новую
            storage.add(variable);
        
        return variable
    

    @classmethod
    def validate_operand(cls, token, tok_type, storage: Storage) -> Object:

        if tok_type == 'variable':
            var = cls.validate_variable(token, storage)
            return var

        elif tok_type == 'function':



            token: str = token[token.find('(')+1:-1]
            argument_list = cls.validate_list(token, storage).data
            storage.set_arguments(argument_list)


            ########
            if token.startswith('yell'):
                lst = token[:-1].replace('yell(', '')
                lst = cls.validate_list(lst, storage)
                for obj in lst.data:
                    print(obj)
                return Integer(len(lst.data))
            return Integer(0)
            #######

        elif tok_type == 'list':
            lst = cls.validate_list(token, storage)
            return lst

        elif tok_type == 'argument':
            num = int(token[-1])
            obj = storage.get_argument(num)
            return obj
        
        else:
            obj: Object = cls.basic_object(token, tok_type)
            return obj

    @classmethod
    def basic_object(cls, token: str, tok_type: str) -> Object:
        obj = BASIC_TYPES[tok_type](token)
        return obj


    def __repr__(self):
        return f'{self.string};'

