from construction import Construction


class Function(Construction): # не обязана наследоваться от конструкции. можно в парсинге дерева добавлять в хранилище
    regex: str = 'Func\(.*?\)'
    name: str = 'Func'

    def __init__(self, text: str):
        self.validate(text)

    def validate(self, text: str):
        m = search(self.regex, text)

        self.head: str = text[m.start():m.end()-1].replace('Func(', '')
        self.text: str = syntax_analysis(text[m.end()+1:-1])

    def __repr__(self):
        return 'fn#' + self.head

