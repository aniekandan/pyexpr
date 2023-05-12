from floatExprParser import Parser, SyntaxError
from nodes import *

symbol_table = {}

print("PyExpr -- Enter expressions to evaluate. Press CTRL + C to quit.")

while True:
    try:
        text = input('calc> ')
        tree = Parser(text).parse()
        result = tree.eval()
        print(result)

    except SyntaxError as e:
        print(e)

    except KeyboardInterrupt:
        print('Exiting...')
        break

    except Exception as e:
        print(e)
