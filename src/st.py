class SymbolTable:
    def __init__(self):
        self.table = {}
    
    def getValue(self, identifier):
        try:
            return tuple(self.table[identifier])
        except:
            raise Exception("variable is not declared")
    
    def setValue(self, identifier, value):
        if(identifier in self.table.keys()):
            if(self.table[identifier][1] == "int"):
                if(value[1] == "int"):
                    self.table[identifier][0] = value[0]
                else:
                    raise Exception(f"cannot attribute {value[1]} to int variable")
            elif(self.table[identifier][1] == "str"):
                if(value[1] == "str"):
                    self.table[identifier][0] = value[0]
                else:
                    raise Exception(f"cannot attribute {value[1]} to str variable")
            elif(self.table[identifier][1] == "void"):
                raise Exception("void type variable????")
        else:
            raise Exception("variable is not declared")

    def create(self, identifier, value):
        # print(identifier)
        if(identifier in self.table.keys()):
            raise Exception("variable cannot be redeclared")
        if(value == "TINT"):
            self.table[identifier] = [None, "int"]
        elif(value == "TSTR"):
            self.table[identifier] = [None, "str"]
        elif(value == "TVOID"):
            raise Exception("variable cannot be of type void")