from rply.token import BaseBox
from st import SymbolTable

class Node(BaseBox):
    def eval():
        return

class BinOp(BaseBox):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def eval(self, symbolTable, funcTable):
        child1 = self.children[0].eval(symbolTable, funcTable)
        child2 = self.children[1].eval(symbolTable, funcTable)
        # print(child1, child2)
        if self.value == "PLUS":
            if(child1[1] == child2[1] == "int"):
                return (child1[0] + child2[0], "int")
            else:
                raise Exception("cannot make operation with str")
        elif self.value == "MINUS":
            if(child1[1] == child2[1] == "int"):
                return (child1[0] - child2[0], "int")
            else:
                raise Exception("cannot make operation with str")
        elif self.value == "MULT":
            if(child1[1] == child2[1] == "int"):
                return (child1[0] * child2[0], "int")
            else:
                raise Exception("cannot make operation with str")
        elif self.value == "DIV":
            if(child1[1] == child2[1] == "int"):
                return (child1[0] // child2[0], "int")
            else:
                raise Exception("cannot make operation with str")
        elif self.value == "BOOLEQUAL":
            if(child1[1] == child2[1]):
                if(child1[0] == child2[0]):
                    return (1, "int")
                else:
                    return (0, "int")
            else:
                raise Exception("cannot compare int with str")
        elif self.value == "LESS":
            if(child1[1] == child2[1]):
                if(child1[0] < child2[0]):
                    return (1, "int")
                else:
                    return (0, "int")
            else:
                raise Exception("cannot compare int with str")
        elif self.value == "MORE":
            if(child1[1] == child2[1]):
                if(child1[0] > child2[0]):
                    return (1, "int")
                else:
                    return (0, "int")
            else:
                raise Exception("cannot compare int with str")
        elif self.value == "OR":
            if(child1[1] == child2[1]):
                if(child1[0] or child2[0]):
                    return (1, "int")
                else:
                    return (0, "int")
            else:
                raise Exception("cannot compare int with str")
        elif self.value == "AND":
            if(child1[1] == child2[1]):
                if(child1[0] and child2[0]):
                    return (1, "int")
                else:
                    return (0, "int")
            else:
                raise Exception("cannot compare int with str")
        elif self.value == "CONCAT":
            return (str(child1[0]) + str(child2[0]), "str")
        else:
            raise Exception("eval Error")

class UnOp(BaseBox):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def eval(self, symbolTable, funcTable):
        child = self.children.eval(symbolTable, funcTable)
        if child[1] != "int":
            raise Exception("cannot make operation with str")
        if self.value == "PLUS":
            return (child[0], "int")
        elif self.value == "MINUS":
            return (-child[0], "int")
        elif self.value == "NOT":
            return (not child[0], "int")
        else:
            raise Exception("eval Error")

class IntVal(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self, symbolTable, funcTable):
        if self.value.isnumeric():
            return (int(self.value), "int")
        else:
            raise Exception("eval Error")

class StrVal(BaseBox):
    def __init__(self, value):
        if(len(value) > 2):
            self.value = value[2:-2]
        else:
            self.value = ""

    def eval(self, symbolTable, funcTable):
        return (self.value, "str")

class NoOp(BaseBox):
    def __init__(self):
        self.value = None
        self.children = None

    def eval(self, symbolTable, funcTable):
        return

class IdOp(BaseBox):
    def __init__(self, value):
        self.value = value
    
    def eval(self, symbolTable, funcTable):
        return symbolTable.getValue(self.value) #ja retorna como tupla

class Block(BaseBox):
    def __init__(self):
        self.value = "block"
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def eval(self, symbolTable, funcTable):
        for child in self.children:
            ret = child.Evaluate(symbolTable, funcTable)
            return ret

class PrintOp(BaseBox):
    def __init__(self, child):
        self.value = "print"
        self.child = child

    def eval(self, symbolTable, funcTable):
        child = self.child.eval(symbolTable, funcTable)[0]
        print(child)

class AssignOp(BaseBox):
    def __init__(self, children):
        self.children = children
        self.value = "assign"

    def eval(self, symbolTable, funcTable):
        symbolTable.setValue(self.children[0].value, self.children[1].eval(symbolTable, funcTable))
        return

class WhileOp(BaseBox):
    def __init__(self, children):
        self.value = "while"
        self.children = children
    
    def eval(self, symbolTable, funcTable):
        while(self.children[0].eval(symbolTable, funcTable)[0]):
            # self.children[1].__repr__()
            self.children[1].eval(symbolTable, funcTable)
        return

class IfOp(BaseBox):
    def __init__(self, children):
        self.children = children
        self.value = "if"
    
    def eval(self, symbolTable, funcTable):
        if(self.children[0].eval(symbolTable, funcTable)[0]):
            self.children[1].eval(symbolTable, funcTable)
        else:
            self.children[2].eval(symbolTable, funcTable)
        return

class VarDec(BaseBox):

    def __init__(self, value, child):
        self.children = child
        self.value = value

    def addChild(self, child):
        self.children.append(child)

    def eval(self, symbolTable, funcTable):
        # for i in self.children:
        #     symbolTable.create(i.value, self.value)
        symbolTable.create(self.children, self.value)

class ScanOp(BaseBox):
    def __init__(self):
        self.value = "scan"
    
    def eval(self, symbolTable, funcTable):
        try:
            inp = int(input())
        except:
            raise Exception("not a int")
        return (inp, "int")

class Statements(BaseBox):
    def __init__(self, child):
        self.children = [child]

    def add_child(self, child):
        self.children.append(child)

    def eval(self, symbolTable, funcTable):
        # for child in self.children:
        #     child.eval(symbolTable, funcTable)
        for child in self.children:
            if(child.value == "return"):
                ret = child.eval(symbolTable, funcTable)
                return ret
            child.eval(symbolTable, funcTable)

class FuncDec(Node):

    def __init__(self, value, args, block):
        self.value = value
        self.args = args
        self.block = block
    
    def eval(self, symbolTable, funcTable):
        # print(self.value)
        funcTable.create(self.value[1], self.value[0])
        funcTable.setValue(self.value[1], self)
        # print(funcTable.table)

class FuncCall(BaseBox):

    def __init__(self, value, args):
        self.value = value
        self.args = args
        # print(len(args))
        self.LocalST = SymbolTable()
    
    def eval(self, symbolTable, funcTable):
        func = funcTable.getValue(self.value)
        ids = []
        if len(self.args.children) == len(func[0].args.children):
            if(len(self.args.children) == 0):
                returned = func[0].block.eval(self.LocalST, funcTable)
                if(returned[1] == func[1]):
                    return returned
                else:
                    raise Exception(f"tried to return {returned[1]} but function has type {func[1]}")
            else:
                for arg in func[0].args.children:
                    arg.eval(self.LocalST, funcTable)
                    ids.append(arg.children)
                for arg, id in zip(self.args.children, ids):
                    self.LocalST.setValue(id, arg.eval(symbolTable, funcTable))
                returned = func[0].block.eval(self.LocalST, funcTable)
                if(returned[1] == func[1]):
                    return returned
                else:
                    raise Exception(f"tried to return {returned[1]} but function has type {func[1]}")
                return func[0].block.eval(self.LocalST, funcTable)
        else:
            raise Exception("num of args missmatch")

class ReturnOp(BaseBox):
    def __init__(self, child):
        self.value = "return"
        self.child = child

    def eval(self, symbolTable, funcTable):
        # print(type(self.child))
        if(self.child == None):
            return(None, "void")
        ret = self.child.eval(symbolTable, funcTable)
        return ret

class Arguments(BaseBox):
    def __init__(self):
        self.children = []

    def addChild(self, child):
        self.children.append(child)

    def eval(self, symbolTable, funcTable):
        return self.children 