from rply import ParserGenerator
from ast import (IntVal, BinOp, IfOp, UnOp, StrVal,
                 NoOp, IdOp, PrintOp, AssignOp,
                 WhileOp, IfOp, VarDec, Statements, ScanOp)#, Function)


class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # TOKENS
            ['NUM', 'STR', 'OP', 'CP',  #3
             'PLUS', 'MINUS', 'MULT', 'DIV', 'IF', #5
             'MORE', 'LESS', 'EQUAL', 'NOT', #4
             'OB', 'CB', 'SC', 'BOOLEQUAL', #4
             'ID', 'SCANF', 'ELSE', 'PRINTF', 'WHILE',  #5
             'OR', 'AND', 'TSTR',# 'COMMA',# 'QUOTE', #5
             'CONCAT', 'TINT'
             ]
        )

    def parse(self):
        @self.pg.production('expression : NUM')
        def expression_number(p):
            # p is a list of the pieces matched by the right hand side of the
            # rule
            return IntVal(p[0].getstr())

    def parse(self):
        @self.pg.production('program : statement_list')
        def program(p):
            # print("teste")
            return p[0]

        @self.pg.production('statement_list : statement')
        def statement_list_rest(p):
            return Statements(p[0])

        @self.pg.production('statement_list : statement_list statement')
        def statement_list_rest(p):
            p[0].add_child(p[1])
            return p[0]

        @self.pg.production('statement : TINT ID SC')
        @self.pg.production('statement : TSTR ID SC')
        def var_dec(p):
            return VarDec(p[0].gettokentype(), p[1].getstr())

        # @self.pg.production('statement : TINT ID id_list SC')
        # @self.pg.production('statement : TSTR ID id_list SC')
        # def var_dec(p):
        #     return VarDec(p[0].gettokentype(), p[1].getstr())

        # @self.pg.production("id_list : COMMA ID")
        # def id_list_rest(p):
        #     return VarDec

        @self.pg.production('statement : IF OP rel_expr CP block')
        def statement_if(p):
            children = [p[2], p[5], NoOp()]
            return IfOp(children)

        @self.pg.production('statement : WHILE OP rel_expr CP block')
        def statement_while(p):
            children = [p[2], p[4]]
            return WhileOp(children)

        # @self.pg.production('statement : function')
        # def statement_if(p):
        #     return p[0]
        
        # @self.pg.production('fucntion : TYPE ID OP args_list CP block')
        # def statement_if(p):
        #     return p[0]

        @self.pg.production('statement : IF OP rel_expr CP block ELSE block')
        def statement_if(p):
            children = [p[2], p[4], p[6]]
            return IfOp(children)

        @self.pg.production('statement : ID EQUAL rel_expr SC')
        def attribution(p):
            children = [p[0], p[2]]
            return AssignOp(children)

        @self.pg.production('statement : PRINTF OP rel_expr CP SC')
        def print_func(p):
            return PrintOp(p[2])

        @self.pg.production('rel_expr : expr MORE expr')
        @self.pg.production('rel_expr : expr LESS expr')
        @self.pg.production('rel_expr : expr BOOLEQUAL expr')
        def rel_binop(p):
            children = [p[0], p[2]]
            if p[1].gettokentype() == 'MORE':
                return BinOp(p[1].gettokentype(), children)
            elif p[1].gettokentype() == 'LESS':
                return BinOp(p[1].gettokentype(), children)
            elif p[1].gettokentype() == 'BOOLEQUAL':
                return BinOp(p[1].gettokentype(), children)
            else:
                raise AssertionError('invalid sequence rel_expr')
        
        @self.pg.production('rel_expr : expr')
        def rel_expr(p):
            return p[0]

        @self.pg.production('expr : term PLUS term')
        @self.pg.production('expr : term MINUS term')
        @self.pg.production('expr : term OR term')
        @self.pg.production('expr : term CONCAT term')
        def expr_binop(p):
            children = [p[0], p[2]]
            if p[1].gettokentype() == 'PLUS':
                return BinOp(p[1].gettokentype(), children)
            elif p[1].gettokentype() == 'MINUS':
                return BinOp(p[1].gettokentype(), children)
            elif p[1].gettokentype() == 'OR':
                return BinOp(p[1].gettokentype(), children)
            elif p[1].gettokentype() == 'CONCAT':
                return BinOp(p[1].gettokentype(), children)
            else:
                raise AssertionError('invalid sequence expr')

        @self.pg.production('expr : term')
        def expr_term(p):
            return p[0]

        @self.pg.production('term : factor MULT factor')
        @self.pg.production('term : factor DIV factor')
        @self.pg.production('term : factor AND factor')
        def term(p):
            children = [p[0], p[2]]
            if p[1].gettokentype() == 'MULT':
                return BinOp(p[1].gettokentype(), children)
            elif p[1].gettokentype() == 'DIV':
                return BinOp(p[1].gettokentype(), children)
            elif p[1].gettokentype() == 'AND':
                return BinOp(p[1].gettokentype(), children)
            else:
                raise AssertionError('invalid sequence term')

        @self.pg.production('term : factor')
        def term_factor(p):
            return p[0]

        @self.pg.production('factor : NUM')
        def factor_number(p):
            return IntVal(p[0].getstr())

        @self.pg.production('factor : ID')
        def identifier(p):
            return IdOp(p[0].getstr())

        @self.pg.production('factor : OP rel_expr CP')
        def factor_parenthesis(p):
            return p[1]

        @self.pg.production('factor : STR')
        def factor_number(p):
            return StrVal(p[0].getstr())

        @self.pg.production('factor : NOT factor')
        def factor_not(p):
            return UnOp(p[0].gettokentype(), p[1])

        @self.pg.production('factor : PLUS factor')
        def factor_plus(p):
            return UnOp(p[0].gettokentype(), p[1])

        @self.pg.production('factor : MINUS factor')
        def factor_minus(p):
            return UnOp(p[0].gettokentype(), p[1])

        @self.pg.production('factor : SCANF OP CP')
        def not_op(p):
            return ScanOp()
        
        @self.pg.production('block : OB statement_list CB')
        def block(p):
            return p[1]

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def getParser(self):
        return self.pg.build()