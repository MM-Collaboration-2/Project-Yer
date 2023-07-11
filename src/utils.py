from re import fullmatch, compile, findall, match
from stack import Stack


# Определение регулярных выражений для паттернов типов и имен типов
global token_types
token_types: dict[str, str] = {
                             '[+\-*/=<>][=]?': 'operation', # первым делом операция, чтобы отличить от отрицательныъ чисел
                             '-?\d+\.\d+': 'float',
                             '[-]?\d+': 'integer',
                             '[a-zA-Z][a-zA-Z0-9_]*': 'variable',
                             '\".*?\"': 'string',
                             '\[.*\]': 'list',
                             '\(': 'open_bracket',
                             '\)': 'close_bracket',
                             }


# Получаем список токенов из строки выражения в инфиксном виде
def tokens(infixexpr: str):
    d = {}    
    pattern = '|'.join(t for t in token_types.keys())
    
    return findall(pattern, infixexpr)


# Определяем тип токена
def token_type(token: str) -> str:
    for pattern, token_type in token_types.items():
        if match(pattern, token):
            return token_type
    return 'other'



# Получает строку, возвращает массив с токенами в постыиксно форме:
# 'a = b + 2' -> ['a', 'b', '2', '+', '=']
def infix_to_postfix(infixexpr) -> list[str]:
    prec = {}
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    prec["="] = 1

    op_stack = Stack()
    postfix_list = []

    token_list = tokens(infixexpr)

    for token in token_list:
        tok_type = token_type(token)
        if tok_type == 'integer':                   # если число
            postfix_list.append(token)
        elif tok_type == 'float':                   # если дробное
            postfix_list.append(token)
        elif tok_type == 'string':                  # если строка
            postfix_list.append(token)
        elif tok_type == 'variable':                # если переменная
            postfix_list.append(token)
        elif tok_type == 'list':                    # если список
            postfix_list.append(token)
        elif tok_type == 'open_bracket':
            op_stack.push( token)
        elif tok_type == 'close_bracket':
            top_token = op_stack.pop()
            while top_token != '(':
                postfix_list.append(top_token)
                top_token = op_stack.pop()

        else:
            while (not op_stack.is_empty()) and \
                (prec.get(op_stack.peek(), 1) >= prec.get(token, 1)):
                postfix_list.append(op_stack.pop())
            op_stack.push(token)

    while not op_stack.is_empty():
        postfix_list.append(op_stack.pop())

    return postfix_list


if __name__ == '__main__':
    t = tokens('var+=11')
    print(t)

