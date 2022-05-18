from rply import LexerGenerator
import re
class LexerGen():
    def __init__(self):
        self.lexer = LexerGenerator()
        self.lexer.add('NUM', '\d+')
        self.lexer.add('STR', '"[a-zA-Z0-9]*"')
        self.lexer.add('PLUS', '➕', flags = re.UNICODE)
        self.lexer.add('MINUS', '➖', flags = re.UNICODE)
        self.lexer.add('MULT', '❌', flags = re.UNICODE)
        self.lexer.add('DIV', '➗', flags = re.UNICODE)
        self.lexer.add('LESS', '👇', flags = re.UNICODE)
        self.lexer.add('MORE', '👆', flags = re.UNICODE)
        self.lexer.add('OP', '👉', flags = re.UNICODE)
        self.lexer.add('CP', '👈', flags = re.UNICODE)
        self.lexer.add('TSTR', '🔠', flags = re.UNICODE)
        self.lexer.add('TINT', '🔢', flags = re.UNICODE)
        self.lexer.add('BOOLEQUAL', '⬅️➡️', flags = re.UNICODE)
        self.lexer.add('AND', '🤝', flags = re.UNICODE)
        self.lexer.add('OR', '🚻', flags = re.UNICODE)
        self.lexer.add('OB', '📥', flags = re.UNICODE)
        self.lexer.add('CB', '📤', flags = re.UNICODE)
        self.lexer.add('CONCAT', '🖇️', flags = re.UNICODE)
        self.lexer.add('COMMA', '👭', flags = re.UNICODE)
        self.lexer.add('ID', '[a-zA-Z|_][a-zA-Z0-9|_]*')
        self.lexer.add('EQUAL', '⬅️', flags = re.UNICODE)
        self.lexer.add('SC', '✋', flags = re.UNICODE)
        self.lexer.add('PRINTF', '▶️', flags = re.UNICODE)
        self.lexer.add('SCANF', '⏺️', flags = re.UNICODE)
        self.lexer.add('WHILE', '♾️', flags = re.UNICODE)
        self.lexer.add('IF', '🤔', flags = re.UNICODE)
        self.lexer.add('NOT', '🙅', flags = re.UNICODE)
        self.lexer.add('ELSE', '🤷', flags = re.UNICODE)
        self.lexer.ignore('\s+')
        self.lexer.ignore('\n')
    
    def getBuild(self):
        return self.lexer.build()