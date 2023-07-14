from object import Object
from integer import Integer
from variable import Variable
from basic_types import BASIC_TYPES
from storage import Storage


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
    def __same_types(cls, lop: Object, rop: Object) -> bool:
        # осторожно, один из них может быть переменной
        return lop.type == rop.type

    @classmethod
    def __valid_operation(cls, lop: Object, rop: Object, op: str, storage: Storage) -> bool:
        lop = cls.__get_object(lop, storage)
        rop = cls.__get_object(rop, storage)
        if cls.__same_types(lop, rop):
            if lop.type in ['list', 'string'] and op in ['-', '*', '/']:
                return False
            if rop.type in ['integer', 'float']:
                if rop.data == 0:
                    return False
            return True
        return False


    # В приравнивании левый операнд всегда переменная
    @classmethod
    def equate(cls, lop: Variable, rop: Object, storage: Storage) -> Object:
        rop = cls.__get_object(rop, storage)
        storage.set(lop.name, rop)
        return rop

    @classmethod
    def operate(cls, lop: Object, rop: Object, op: str, storage: Storage) -> Object:
        lop = cls.__get_object(lop, storage)
        rop = cls.__get_object(rop, storage)
        if cls.__valid_operation(lop, rop, op, storage):
            basic_type = BASIC_TYPES[lop.type]
            func = cls.operations[op]
            return basic_type(func(lop.data, rop.data))
        return Integer(0)

    @classmethod
    def run(cls, lop: Object, rop: Object, op: str, storage: Storage):
        if op == '=':
            return cls.equate(lop, rop, storage)
        else:
            return cls.operate(lop, rop, op, storage)

