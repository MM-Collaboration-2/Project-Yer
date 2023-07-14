from re import findall, match
from stack import Stack


# Определение регулярных выражений для паттернов типов и имен типов
global TOKEN_TYPES
TOKEN_TYPES: dict[str, str] = {

        # перед переменными
        '[a-zA-Z_][a-zA-Z0-9_]*\ *\(.*?\)': 'function',
        #'[a-zA-Z_][a-zA-Z0-9_]*\ *\(': 'function',


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

        # скобки
        '\(': 'open_bracket',
        '\)': 'close_bracket',
        '\[': 'list',
        '\]': 'square_close_bracket',

        # уникальные сами по себе
        '\".*?\"': 'string',

        # список после скобок
        '\[.*?\]': 'list',
        '\$argv\d+': 'argument',
        ',': 'comma',

        }


'''a = b() * [[1+3], "str"]'''
def get_arguments(expression: str):
    pattern = '|'.join(t for t in TOKEN_TYPES.keys())
    args = findall(pattern, expression)
    new_args = []
    index: int = 0
    while index < len(args):
        token = args[index]
        if token == '[':
            brackets: int = 1
            while brackets != 0:
                index += 1
                new_token = args[index]
                token += new_token
                if new_token == '[':
                    brackets += 1
                elif new_token == ']':
                    brackets -= 1

        index += 1
        new_args.append(token)

    print(new_args)
    return new_args

                


# Получаем список токенов из строки выражения в инфиксном виде
def tokens(infixexpr: str):
    pattern = '|'.join(t for t in TOKEN_TYPES.keys())
    return findall(pattern, infixexpr)


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
    text = 'a = b() * [[1+3], "str"]'
    for t in get_arguments(text):
        print(token_type(t), t)
