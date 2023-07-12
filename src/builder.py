from constructions import Construction, ExpressionBlock, Block, Function, CONSTRUCTIONS_HEADS
from storage import Storage


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
            func: Function = Function(header)
            block = Block([], storage)
            return block

        elif obj.name == 'Main' or obj.name == 'Block':
            return obj(constructions, storage)

        else:
            block = Block(constructions, storage)
            return obj(header, block, storage)
