from constructions import Expression

def main():
    variables = {}
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
    while inp != 'q':
        inp = input('>>> ')
        if len(inp) == 0:
            continue
        elif len(inp) == 1:
            outp = variables.get(inp, inp)
        else:
            exp = Expression(inp, variables)
            outp = exp.run()
        print(outp)

main()
