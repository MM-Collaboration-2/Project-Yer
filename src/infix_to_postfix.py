
class Stack():
    def __init__(self):
        self.list = list()

    def isEmpty(self):
        return len(self.list) == 0

    def pop(self):
        return self.list.pop()

    def peek(self):
        return self.list[-1]

    def push(self, data):
        self.list.append(data)

    def __str__(self):
        print(self.list)


def infixToPostfix(infixexpr):

    prec = {}
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    prec["="] = 1

    opStack = Stack()
    postfixList = []

    tokenList = infixexpr.split()


    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789":
            postfixList.append(token)
        elif token == '(':
            opStack.push( token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()

        else:
            while (not opStack.isEmpty()) and \
                (prec[opStack.peek()] >= prec[token]):
                postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return postfixList

if __name__ == '__main__':
    print(infixToPostfix("A = B + C = D"))
    print(infixToPostfix("( A + B ) * C - ( D - E ) * ( F + 6 )"))
