from re import findall, match
from stack import Stack


# Определение регулярных выражений для паттернов типов и имен типов
global TOKEN_TYPES
TOKEN_TYPES: dict[str, str] = {

        # перед переменными
        '[a-zA-Z_][a-zA-Z0-9_]*\ *\(.*?\)': 'function',

        # отрицательные числа перед операциями
        '-\d+': 'integer',
        '-\d+\.\d+': 'float',

        # return перед переменными
        '[+\-*/=<>][=]?|return': 'operation',

        # положительные числа после операциями
        '\d+': 'integer',
        '\d+\.\d+': 'float',

        # все буквенно-циферные комбинации
        '[a-zA-Z_][a-zA-Z0-9_]*': 'variable',

        # уникальные сами по себе
        '\".*?\"': 'string',
        '\[.*?\]': 'list',
        '\$argv\d+': 'argument',

        # скобки
        '\(': 'open_bracket',
        '\)': 'close_bracket',
                             }


# Получаем список токенов из строки выражения в инфиксном виде
def tokens(infixexpr: str):
    d = {}    
    pattern = '|'.join(t for t in TOKEN_TYPES.keys())
    
    return findall(pattern, infixexpr)


def recover_tokens(token_list: list[str]):
    pass

# Определяем тип токена
def token_type(token: str) -> str:
    for pattern, token_type in TOKEN_TYPES.items():
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
        elif tok_type == 'function':                # если функция
            postfix_list.append(token)
        elif tok_type == 'argument':                # если аргумент
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

def syntax_analysis(text: str, logging:bool = False) -> str:
    analysed_text = ''
    brackets_open = ('(', '{', '[')
    brackets_closed = (')', '}', ']')
    stack = Stack()
    comment_flag = False
    string_flag = False
    for ch in text:
        if ch == '\n': # убираем перенос строки
            continue
        if ch == '\'':
            comment_flag = not(comment_flag)
            continue
        if comment_flag:
            continue
        if ch == '"':
            string_flag = not(string_flag)
            analysed_text += ch
            continue
        if string_flag:
            analysed_text += ch
            continue
        else:
            if ch != ' ': #табы тоже чекаются
                analysed_text += ch
            if ch in brackets_open:
                stack.push(ch)
            elif ch in brackets_closed:    
                if stack.is_empty(): 
                    if logging: print("Ошибка в расстановке скобочек (нет ни одной открывающей)")
                    return ''
                else:
                    index = brackets_closed.index(ch)
                    open_bracket = brackets_open[index]
                    if stack.peek() == open_bracket:
                        stack.pop()  
                    else: 
                        if logging: print("Ошибка в расстановке скобочек (последняя скобочка не совпадает с предыдущей, типо '{)')")
                        return ''

    if not(stack.is_empty()):
        if logging: print("Ошибка в расстановке скобочек (не хватает закрывающей(их))")
        return ''

    return analysed_text
    


if __name__ == '__main__':
    text = 'l = ["a"] + ["b"]'
    for t in tokens(text):
        print(token_type(t), t)
