from basic_structures import *



class Storage():                            # Хранилище переменных
    def __init__(self, variables):         # и функций в будущем
        self.variables: dict = variables

    def add(self, variable: Variable) -> None:
        self.variables[variable.name] = variable

    def set(self, name: str, obj: Object) -> None:
        if self.declared(name):
            self.get(name).obj = obj

    def remove(self, name: str) -> None:
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



class Operation():                                                  # Класс для осуществления и менеджмента
    operations: dict[str, ()] = {
            # Операции с приравниванием
            #'+=': lambda lop, rop: lop + rop,
            #'-=': lambda lop, rop: lop - rop,
            #'*=': lambda lop, rop: lop * rop,
            #'/=': lambda lop, rop: lop / rop,

            # Арифметические операции
            '+': lambda lop, rop: lop + rop,
            '-': lambda lop, rop: lop - rop,
            '*': lambda lop, rop: lop * rop,
            '/': lambda lop, rop: lop / rop,

            # Логические операции
            '<': lambda lop, rop: lop < rop,
            '>': lambda lop, rop: lop > rop,
            '<=': lambda lop, rop: lop <= rop,
            '>=': lambda lop, rop: lop >= rop,
            '==': lambda lop, rop: lop == rop,
            }


    @classmethod
    def __get_object(cls, operand: Object, storage: Storage) -> Object:
        if operand.type == 'variable':                      # Если  операнд -- переменная
            return storage.get(operand.name).obj            # Извлечем ее значение
        return operand

    @classmethod
    def __same_types(cls, lop: Object, rop: Object, storage: Storage) -> bool:
        lop = cls.__get_object(lop, storage)
        rop = cls.__get_object(rop, storage)
        return lop.type == rop.type


    # В приравнивании левый операнд всегда переменная
    @classmethod
    def equate(cls, lop: Variable, rop: Object, storage: Storage) -> Object:
        ######
        if lop.type != 'variable':
            print('panic1')
        rop = cls.__get_object(rop, storage)
        storage.set(lop.name, rop)
        return rop

    @classmethod
    def operate(cls, lop: Object, rop: Object, op: str, storage: Storage) -> Object:
        lop = cls.__get_object(lop, storage)
        rop = cls.__get_object(rop, storage)
        if cls.__same_types(lop, rop, storage):
            basic_type = BASIC_TYPES[lop.type]
            func = cls.operations[op]
            return basic_type(func(lop.data, rop.data))
        return Integer(0)

    @classmethod
    def run(cls, lop: Object, rop: Object, op: str, storage: Storage):
        if op == '=':
            ######
            if lop.type != 'variable':
                print('panic2')
            return cls.equate(lop, rop, storage)
        else:
            return cls.operate(lop, rop, op, storage)









if __name__ == '__main__':
#'Expr{a=16*3;b=a-10}'
    s = Storage({})
    v1 = Variable('a', Integer(0))
    v2 = Variable('b', Integer(0))
    s.add(v1)
    s.add(v2)
    i1 = Integer(16)
    i2 = Integer(3)
    i3 = Integer(10)

    op1 = '>='
    r1 = Operation.run(i1, i2, op1, s)
    print(r1)

    print(s.get('a'))
    print(s.get('b'))




