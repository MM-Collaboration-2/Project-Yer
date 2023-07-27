from re import findall, match
from stack import Stack


# Определение регулярных выражений для паттернов типов и имен типов
global TOKEN_TYPES
TOKEN_TYPES: dict[str, str] = {

        # перед переменными
        '[a-zA-Z_][a-zA-Z0-9_]*\ *\(': 'function',
        #'[a-zA-Z_][a-zA-Z0-9_]*\ *\(': 'function',

        # отрицательные числа перед операциями
        '-\d+\.\d+': 'float',
        '-\d+': 'integer',

        # return перед переменными
        '[+\-*/=<>!][=]?|return': 'operation',

        # положительные числа после операциями
        '\d+\.\d+': 'float',
        '\d+': 'integer',

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


# Определяем тип токена
def token_type(token: str) -> str:
    for pattern, token_type in TOKEN_TYPES.items():
        if match(pattern, token):
            return token_type
    return 'other'


# возвращает число, равное нессответсвию заданных скобок
# 0 если количесво скобок равно
# отрицательное - больше закрывающих
# положительное - больше открывающих
def brackets_not_in_string(text: str, open_bracket='(', close_bracket=')') -> bool:
    quotes: int = 0
    brackets: int = 0
    for ch in text:
        if ch == '"':
            quotes += 1
            quotes %= 2
        
        if quotes == 0 and ch == open_bracket:
            brackets += 1
        if quotes == 0 and ch == close_bracket:
            brackets -= 1

    return brackets


# разделяет строку выражений по запятым
# вложенные запятые игнорируются
def smart_split_comma(expression: str):
    parts = expression.split(',')
    valid_parts = []
    index: int = 0
    while index < len(parts):
        part = parts[index]

        # проверка строки
        if part.strip().startswith('"') and not part.strip().endswith('"'):
            while True:
                index += 1
                new_part = parts[index]
                part +=  ',' + new_part
                if new_part.strip().endswith('"'):
                    break

        # проверка функции
        if brackets_not_in_string(part) > 0:
            brackets: int = brackets_not_in_string(part)
            while brackets != 0:
                index += 1
                new_part = parts[index]
                part += ',' + new_part
                brackets += brackets_not_in_string(new_part)


        # проверка списка
        if brackets_not_in_string(part, '[', ']') > 0:
            brackets: int = brackets_not_in_string(part, '[', ']')
            while brackets != 0:
                index += 1
                new_part = parts[index]
                part += ',' + new_part
                brackets += brackets_not_in_string(new_part, '[', ']')



        index += 1
        valid_parts.append(part)
    valid_parts = [p for p in valid_parts if p]

    return valid_parts


def smart_split_semi(expressions: str):
    parts: list[str] = expressions.split(';')
    parts = [_ for _ in parts if _]
    new_expressions: list[str] = []
    index: int = 0
    string: int = 0
    while index < len(parts):
        part = parts[index]
        for char in part:
            if char == '"':
                string += 1
                string %= 2

        while string != 0:
            index += 1
            new_part = parts[index]

            for char in new_part:
                if char == '"':
                    string += 1
                    string %= 2

            part += ';' + new_part

        index += 1
        new_expressions.append(part)

    return new_expressions



# получить выражения заголовка конструкции
def get_header_expressions(text: str):
    text = text[text.find('(')+1:]
    new_text: str = ''
    brackets: int = 1
    index: int = 0
    string: int = 0
    while brackets != 0:
        char = text[index]
        if char == '"':
            string += 1
            string %= 2

        if string == 0:
            if char == '(':
                brackets += 1
            elif char == ')':
                brackets -= 1

        new_text += char
        index += 1

    return new_text[:-1]

    


# Получаем список токенов из строки выражения в инфиксном виде
def get_tokens(expression: str):
    pattern = '|'.join(t for t in TOKEN_TYPES.keys())
    args = findall(pattern, expression)
    new_args = []
    index: int = 0
    while index < len(args):
        token = args[index]

        if token.startswith('-') and len(token) > 1:
            if len(new_args) > 0 and new_args[-1] not in ['-', '+']:
                new_args.append('-')
                token = token[1:]


        # списки
        if token == '[':
            brackets: int = 1
            while brackets != 0:
                index += 1
                new_token = args[index]
                token += new_token
                brackets += brackets_not_in_string(new_token, '[', ']')


        # функции
        if len(token) > 1 and brackets_not_in_string(token) > 0:
            brackets: int = brackets_not_in_string(token)
            while brackets != 0:
                index += 1
                new_token = args[index]
                token += new_token
                brackets += brackets_not_in_string(new_token)


        index += 1
        new_args.append(token)

    return new_args


# Получает строку, возвращает массив с токенами в постынфиксной форме:
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

    token_list = get_tokens(infixexpr)

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
    text = 'Func (a) {'
    print(get_header_expressions(text))
    #print(smart_split_comma(text))

