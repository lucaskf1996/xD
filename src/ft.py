class FunctionTable:
    def __init__(self):
        self.table = {}
    
    def getValue(self, identifier):
        try:
            return tuple(self.table[identifier])
        except:
            raise Exception("function is not declared")
    
    def setValue(self, identifier, value):
        # print(value)
        if(identifier in self.table.keys()):
            self.table[identifier][0] = value
        else:
            raise Exception("function is not declared")

    def create(self, identifier, value):
        if(identifier in self.table.keys()):
            raise Exception("function cannot be redeclared")
        if(value == "TINT"):
            self.table[identifier] = [None, "int"]
        elif(value == "TSTR"):
            self.table[identifier] = [None, "str"]
        elif(value == "TVOID"):
            self.table[identifier] = [None, "void"]