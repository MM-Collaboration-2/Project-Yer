from re import search
from construction import Construction
from utils import get_header_expressions


class FunctionBlock(Construction): # не обязана наследоваться от конструкции. можно в парсинге дерева добавлять в хранилище
    regex: str = 'Func\ *\(.*?\)\ *{'
    name: str = 'Func'

    def __init__(self, text: str):
        self.head = get_header_expressions(text)

    def __repr__(self):
        return 'fn#' + self.head

