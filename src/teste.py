from st import SymbolTable
from ft import FunctionTable
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

if __name__ == "__main__":
    if(sys.argv[1].rsplit('.', 1)[-1] != "xD"):
        raise Exception("not a .xD")
    with open(sys.argv[1], 'r') as f:
        contents = f.read()

    contents = code_cleanup(contents)
    
    ft = FunctionTable()
    st = SymbolTable()

    lg = LexerGen()
    lexer = lg.getBuild()
    tokens = lexer.lex(contents)

    pg = Parser()
    pg.parse()
    parser = pg.getParser()

    parser.parse(tokens).eval(st, ft)