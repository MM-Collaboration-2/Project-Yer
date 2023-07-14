#!/usr/bin/env python3
import re
import sys
from utils import syntax_analysis
from stack import Stack
from yer_builtins import BUILTINS
from variable import Variable
from storage import Storage
from expression import Expression
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
    #variable_pattern = Variable.regex
    variables = Storage(BUILTINS, Stack())
    while True:
        input_string = '>>> '
        inp = input(input_string)
        if inp == 'q':
            break
        if len(inp) == 0:
            continue
        else:
            if re.fullmatch('.*{.*', inp):
                bracket_diff = inp.count('{') - inp.count('}')
                buf = inp
                input_string = '>>> ' + bracket_diff * '  '
                while(bracket_diff > 0):
                    inp = input(input_string)               # inp - всегда текущая строка
                    bracket_diff += inp.count('{') - inp.count('}')
                    input_string = '>>> ' + bracket_diff * '  '
                    if re.fullmatch('}.*', inp):
                        print(CURSOR_UP_ONE+ERASE_LINE+input_string+inp)
                    buf += inp
                t = ConstructionTree(syntax_analysis(buf, logging=True), variables)
                outp = t.run()
            #elif re.fullmatch(variable_pattern, inp):
                #outp = variables.get(inp)  
            else:
                exp = Expression(inp, variables)
                outp = exp.run()
        print(outp)


if sys.argv[1:]: # файл указан
    with open(sys.argv[1], "r") as f:
        variables = Storage(BUILTINS, Stack())
        text = f.read()
        text = syntax_analysis(text)
        t = ConstructionTree(syntax_analysis(text, logging=True), variables)
        t.run()
else:
    main()