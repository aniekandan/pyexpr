symbol_table = {}

class Node:
    pass    

class NumberNode(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return str(self.value)
    
    def eval(self):
        return float(self.value)

class BinaryOpNode(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f"{self.op[1]}({self.left}, {self.right})"
    
    def eval(self):
        if self.op[1]=="+":
            return self.left.eval() + self.right.eval()
        
        if self.op[1]=="-":
            return self.left.eval() - self.right.eval()
        
        if self.op[1]=="*":
            return self.left.eval() * self.right.eval()
        
        if self.op[1]=="/":
            try:
                return self.left.eval() / self.right.eval()
            except ZeroDivisionError as e:
                raise Exception(f"Division by zero")
        
        raise TypeError("Invalid Operator")
        

class AssignNode(Node):
    def __init__(self, identifier, expr):
        self.identifier = identifier
        self.expr = expr

    def __repr__(self) -> str:
        return f"=({self.identifier}, {self.expr})"
    
    def eval(self):
        rhs_value = self.expr.eval()
        self.identifier.store(rhs_value)
        return rhs_value

class IdentifierNode(Node):
    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        return str(self.name)
    
    def eval(self):
        try:
            return symbol_table[self.name]
        
        except Exception as e:
            raise Exception(f"name '{self.name}' not defined")
        
    def store(self, value):
        symbol_table[self.name] = value