import ply.yacc as yacc
from yapl_lexer import *

#sys.tracebacklimit = 0 # to prevent traceback debug output since it is not needed

# to resolve ambiguity, individual tokens assigned a precedence level and associativity. 
# tokens ordered from lowest to highest precedence, rightmost terminal judged
precedence = ( # +, - same precedence, left associative
    ('left', 'ANDAND', 'OROR'), # +, - same precedence, left associative
    ('left', 'LT', 'LTE','GT','GTE'), # +, - same precedence, left associative
    ('left', 'PLUS', 'MINUS'), # +, - same precedence, left associative
    ('left', 'MULTIPLY', 'DIVIDE', 'MOD'), # +, - same precedence, left associative
    ('left', 'POWER'),
    ('left', 'MINUSMINUS','PLUSPLUS'),
    ('left', 'LPAREN','RPAREN'),
    ('right','NOT')
)

start = 'S'
# multiple variables, assigning data from one variable to another

# after the lexing, start parsing

def p_start(p): # non-terminal, starting
    """
    S : stmt S
    """
    p[0] = [p[1]] + p[2] # list comprehension used to solve recursive grammar, added/appending as well
    

def p_start_empty(p):
    """
    S :
    """
    p[0] = []

def p_struct_dec(p):
    """
    stmt : STRUCT NAME LBRACE S RBRACE SEMICOL
    """
    p[0] = ('struct', p[2], p[4])

def p_struct_attributes(p):
    """
    stmt : STRING NAME 
            | INT NAME
            | FLOAT NAME
            | CHAR NAME
            | BOOL NAME           
    """
    p[0] = ('struct-attribute', p[1], p[2])

def p_struct_instance(p):
    """
    stmt : NAME NAME
    """
    p[0] = ('struct-instance', p[1], p[2])

def p_struct_attribute_assignment(p):
    """
    stmt : stmt EQ exp
    """
    p[0] = ('attribute-update', p[1], p[3])

def p_struct_attribute_ref(p):
    """
    stmt : NAME DOT NAME
    """
    p[0] = ('attribute-ref', p[1], p[3])

def p_for_loop(p):
    """
    stmt : FOR LPAREN stmt SEMICOL exp SEMICOL stmt RPAREN LBRACE S RBRACE
    """
    p[0] = ('for', p[3], p[5], p[7], p[10]) 


def p_stmt_conditional_if(p):
    """
    stmt : IF LPAREN exp RPAREN LBRACE S RBRACE el_stmts
    """ 
    p[0] = ('if', p[3], p[6], p[8])

def p_stmt_conditional_empty(p):
    """
    el_stmts : 
    """ 
    p[0] = []


def p_stmt_conditional_elif(p):
    """
    el_stmts : ELIF LPAREN exp RPAREN LBRACE S RBRACE el_stmts
    """ 
    p[0] = [('elif', p[3], p[6])] + p[8]

def p_stmt_conditional_else(p):
    """
    el_stmts : ELSE LBRACE S RBRACE
    """ 
    p[0] = [('else', p[3])]




def p_assignment_var(p):
    """
    stmt : STRING NAME EQ exp
        | CHAR NAME EQ exp
        | INT NAME EQ exp
        | FLOAT NAME EQ exp
        | BOOL NAME EQ exp
    """
    p[0] = ('assignment', p[1], p[2], p[4]) # ('EQ', 'dtype', 'identifier', 'exp')

def p_update_var(p):
    """
    stmt : NAME EQ exp
    """
    p[0] = ('update_var', p[1], p[3])

def p_exp_unary(p):
    """
    stmt : exp PLUSPLUS
        | exp MINUSMINUS
    """
    p[0] = ('unary', p[1], p[2]) #('unary', ('NAME',x), PLUSPLUS)

def p_print_stmt(p):
    """
    stmt : PRINT LPAREN exp RPAREN
    """
    p[0] = ('PRINT', p[3])


def p_logical_not_exp(p):
    """
    exp : NOT exp
    """
    p[0] = ('logical',p[1], p[2])

def p_stmt_exp(p):
    """
    exp : exp COMMA exp
    """
    p[0] = ('comma-sep',p[1], p[3])



def p_exp_bin(p):
    """ 
    exp : exp PLUS exp
        | exp MINUS exp
        | exp MULTIPLY exp
        | exp DIVIDE exp
        | exp GT exp
        | exp GTE exp
        | exp LT exp
        | exp LTE exp
        | exp EQEQ exp
        | exp NOTEQ exp
        | exp POWER exp
        | exp ANDAND exp
        | exp OROR exp
    """
    p[0] = ('binop',p[2], p[1], p[3]) # '1+2' -> ('+', '1', '2')



def p_exp_braces(p):
    """
    exp : LPAREN exp RPAREN
    """
    p[0] = p[2]


def p_exp_intval(p):
    """
    exp : intValue
    """
    p[0] = ('INT', p[1])

def p_exp_floatval(p):
    """
    exp : floatValue
    """
    p[0] = ('FLOAT', p[1])

def p_exp_charval(p):
    """
    exp : charValue
    """
    p[0] = ('CHAR', p[1])

def p_exp_stringval(p):
    """
    exp : stringValue
    """
    p[0] = ('STRING', p[1])

def p_exp_struct_attribute(p):
    """
    exp : NAME DOT NAME
    """
    p[0] = ('attribute-ref', p[1], p[3])


def p_exp_boolval(p):
    """
    exp : boolValue
    """
    p[0] = ('BOOL', p[1])

def p_exp_name(p):
    """
    exp : NAME
    """
    p[0] = ('NAME', p[1])


def p_error(p):
    print("Syntax error at token", p.value, p.type, p.lexpos)
    exit(1)

parser = yacc.yacc() # start parsing, yacc object created
