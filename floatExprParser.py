# expression     ::= [IDENTIFIER ASSIGNMENT] arithmetic
# arithmetic     ::= term { PLUS term | MINUS term }
# term           ::= factor { TIMES factor | DIVIDE factor }
# factor         ::= LPAREN arithmetic RPAREN | FLOAT_NUM | IDENTIFIER

from tokenizer import tokenize
from nodes import *

class SyntaxError(Exception):
    pass

class Parser:
    def __init__(self, input_string):
        self.__tokens = tokenize(input_string)
        self.__current_token = None
        self.__index = -1
        self.__advance()

    def __advance(self):
        self.__index += 1
        if self.__index < len(self.__tokens):
            self.__current_token = self.__tokens[self.__index]
        else:
            self.__current_token = None

    def __backtrack(self, steps):
        self.__index -= steps
        if self.__index < 0:
            self.__index = 0

        self.__current_token = self.__tokens[self.__index]

    def __error(self):
        raise SyntaxError(f"Syntax error at token {self.__current_token}")

    def __match(self, expected_token_type):
        current_token_type = self.__current_token[0]        

        if current_token_type == expected_token_type:
            self.__advance()

        else:
            self.__error()

    def parse(self):
        return self.__expression()

    def __expression(self):
        step_back = 0
        current_token_type = self.__current_token[0]
        if current_token_type == "IDENTIFIER":
            identifier = self.__identifier()
            step_back += 1

            current_token_type = self.__current_token[0]
            if current_token_type == "ASSIGNMENT":
                self.__advance()
                arith_expr = self.__arithmetic()
                return AssignNode(identifier, arith_expr)
            
            else:
                self.__backtrack(steps=step_back)

        return self.__arithmetic()

    def __identifier(self):
        name = self.__current_token[1]
        self.__match("IDENTIFIER")
        return IdentifierNode(name)

    def __arithmetic(self):
        left = self.__term()
        current_token_type = self.__current_token[0]

        while current_token_type in ("PLUS", "MINUS"):
            op = self.__current_token
            self.__advance()
            right = self.__term()
            left = BinaryOpNode(left, op, right)
            current_token_type = self.__current_token[0]

        return left

    def __term(self):
        left = self.__factor()
        current_token_type = self.__current_token[0]

        while current_token_type in ("TIMES", "DIVIDE"):
            op = self.__current_token
            self.__advance()
            right = self.__factor()
            left = BinaryOpNode(left, op, right)
            current_token_type = self.__current_token[0]

        return left

    def __factor(self):
        current_token_type = self.__current_token[0]

        if current_token_type == "LPAREN":
            self.__match("LPAREN")
            expr = self.__arithmetic()
            self.__match("RPAREN")
            return expr
        
        elif current_token_type == "FLOAT_NUM":
            value = self.__current_token[1]
            self.__match("FLOAT_NUM")
            return NumberNode(value)
        
        elif current_token_type == "IDENTIFIER":
            return self.__identifier()
        
        else:
            self.__error()

