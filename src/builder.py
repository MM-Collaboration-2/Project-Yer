from storage import Storage
from construction import Construction
from expression_block import ExpressionBlock
from block import Block
from function_block import FunctionBlock
from construction_types import CONSTRUCTIONS_HEADS
from callable import Function
from variable import Variable


class Builder():
    @classmethod
    def __get_constructor(cls, header: str) -> object:
        for head in CONSTRUCTIONS_HEADS.keys():
            if header.startswith(head):
                return CONSTRUCTIONS_HEADS[head]
        return None

    @classmethod
    def create_construction(cls, header: str, constructions: list[Construction], storage: Storage) -> Construction:

        obj = cls.__get_constructor(header)

        if obj.name == 'Expr':
            return ExpressionBlock(header, storage)

        if obj.name == 'Func':
            func_block: FunctionBlock = FunctionBlock(header)

            # блок для функции
            block = Block(constructions)
            function: Function = Function(block)

            func_name = func_block.head

            # создаем переменную с объектом функции
            var: Variable = Variable(func_block.head, function)

            # добавляем в хранилище
            storage.add(var)
            return Block([])

        elif obj.name == 'Main' or obj.name == 'Block':
            return obj(constructions)

        else:
            block = Block(constructions)
            return obj(header, block, storage)
