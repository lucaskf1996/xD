from symtable import SymbolTable
from lexerGen import LexerGen
from parser import Parser
import re
import sys

def code_cleanup(text): # FROM https://stackoverflow.com/questions/241327/remove-c-and-c-comments-using-python
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " " # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)

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
            if(self.table[identifier][1] == "int" and value[1] == "int"):
                self.table[identifier][0] = value[0]
            else:
                if(value[1] == "str"):
                    self.table[identifier][0] = value[0]
                else:
                    raise Exception("cannot add an int to a str variable")
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

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        contents = f.read()

    contents = code_cleanup(contents)
    
    st = SymbolTable()

    lg = LexerGen()
    lexer = lg.getBuild()
    tokens = lexer.lex(contents)

    pg = Parser()
    pg.parse()
    parser = pg.getParser()

    parser.parse(tokens).eval(st)