import re
from constructions import Expression
from basic_structures import Variable
from service_structures import Storage
from construction_tree import ConstructionTree

def main():
    print(
''' \tМожно создавать переменные и присваивать им значения. 
    \tМожно использовать в выражениях. 
    \tВыражения могут быть составными. 
    \tМожно использовать скобки.
    \tМежду частями выражения должны быть пробелы
    \n\tНапример:
    \t>>> 1 + 2
    \t>>> x = 14 * 3
    \t>>> y = x - ( 218 / 4 )
    \t>>> z = x + y
    \t>>> z
    ''')

    inp = ''
    buf = ''
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K' 
    variable_pattern = Variable("test").regex
    variables = Storage({})
    while inp != 'q':
        input_string = '>>> '
        inp = input(input_string)
        if len(inp) == 0:
            continue
        else:
            if re.fullmatch('.*{', inp):
                bracket_diff = 1
                buf = inp
                input_string = '>>> ' + bracket_diff * '  '
                while(bracket_diff > 0):
                    inp = input(input_string)               # inp - всегда текущая строка
                    bracket_diff += inp.count('{') - inp.count('}')
                    input_string = '>>> ' + bracket_diff * '  '
                    if re.fullmatch('}.*', inp):
                        print(CURSOR_UP_ONE+ERASE_LINE+input_string+inp)
                    buf += inp
                outp = buf                  # buf перекидывать в магическую функию построения дерева
                t = ConstructionTree(buf)
                outp = t.run()

            elif re.fullmatch(variable_pattern, inp):
                outp = variables.get(inp)  
            else:
                exp = Expression(inp, variables)
                outp = exp.run()
        print(outp)

main()
