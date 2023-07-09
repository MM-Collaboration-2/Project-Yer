class Node:
    def __init__(self, value=None, left=None, right=None, next=None):
        self.value = value
        self.left = left
        self.right = right
        self.next = next
 
class Stack:
    def __init__(self):
        self.head = None
 
    def push(self, node):
        if not self.head:
            self.head = node
        else:
            node.next = self.head
            self.head = node
 
    def pop(self):
        if self.head:
            popped = self.head
            self.head = self.head.next
            return popped
        else:
            raise Exception("Stack is empty")
 
class ExpressionTree:
    def inorder(self, x):
        if not x:
            return
        self.inorder(x.left)
        print(x.value, end=" ")
        self.inorder(x.right)
 
def main():
    s = "ABC*+D/"
    stack = Stack()
    tree = ExpressionTree()
    for c in s:
        if c in "+-*/^":
            z = Node(c)
            x = stack.pop()
            y = stack.pop()
            z.left = y
            z.right = x
            stack.push(z)
        else:
            stack.push(Node(c))
    print("The Inorder Traversal of Expression Tree: ", end="")
    tree.inorder(stack.pop())
 
if __name__ == "__main__":
    main()
