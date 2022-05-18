from rply.token import BaseBox

class Node(BaseBox):
    def eval():
        return

class BinOp(BaseBox):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def eval(self, symbolTable):
        child1 = self.children[0].eval(symbolTable)
        child2 = self.children[1].eval(symbolTable)
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

    def eval(self, symbolTable):
        child = self.children.eval(symbolTable)
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

    def eval(self, symbolTable):
        if self.value.isnumeric():
            return (int(self.value), "int")
        else:
            raise Exception("eval Error")

class StrVal(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self, symbolTable):
        return (self.value, "str")

class NoOp(BaseBox):
    def __init__(self):
        self.value = None
        self.children = None

    def eval(self, symbolTable):
        return

class IdOp(BaseBox):
    def __init__(self, value):
        self.value = value
    
    def eval(self, symbolTable):
        return symbolTable.getValue(self.value) #ja retorna como tupla

class Block(BaseBox):
    def __init__(self):
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def eval(self, symbolTable):
        for child in self.children:
            child.eval(symbolTable)

class PrintOp(BaseBox):
    def __init__(self, child):
        self.child = child

    def eval(self, symbolTable):
        child = self.child.eval(symbolTable)[0]
        print(child)

class AssignOp(BaseBox):
    def __init__(self, children):
        self.children = children

    def eval(self, symbolTable):
        symbolTable.setValue(self.children[0].value, self.children[1].eval(symbolTable))
        return

class WhileOp(BaseBox):
    def __init__(self, children):
        self.children = children
    
    def eval(self, symbolTable):
        while(self.children[0].eval(symbolTable)[0]):
            # self.children[1].__repr__()
            self.children[1].eval(symbolTable)
        return

class IfOp(BaseBox):
    def __init__(self, children):
        self.children = children
    
    def eval(self, symbolTable):
        if(self.children[0].eval(symbolTable)[0]):
            self.children[1].eval(symbolTable)
        else:
            self.children[2].eval(symbolTable)
        return

class VarDec(BaseBox):

    def __init__(self, value, child):
        self.children = child
        self.value = value

    def addChild(self, child):
        self.children.append(child)

    def eval(self, symbolTable):
        # for i in self.children:
        #     symbolTable.create(i.value, self.value)
        symbolTable.create(self.children, self.value)

class ScanOp(BaseBox):
    
    def eval(self, symbolTable):
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

    def eval(self, symbolTable):
        for child in self.children:
            child.eval(symbolTable)