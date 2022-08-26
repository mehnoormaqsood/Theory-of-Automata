import ply.lex as lex

tokens = [
    'INT',
    'STRING',
    'FLOAT',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'PRINT',
    'SEMICOL',
    'CHAR',
    'BOOL',
    'NOT',
    'ANDAND',
    'OROR',
    'NAME',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LT',
    'GT',
    'LTE',
    'GTE',
    'EQEQ',
    'EQ',
    'MOD',
    'PLUSPLUS',
    'MINUSMINUS',
    'AND',
    'OR',
    'POWER',
    'FOR',
    'STRUCT',
    'boolValue',
    'charValue',
    'stringValue',
    'floatValue',
    'intValue',
    'IF',
    'ELIF',
    'ELSE',
    'NOTEQ',
    'COMMA',
    'DOT'
]

t_PLUS = r'\+'
t_DOT = r'\.'
t_PLUSPLUS = r'\+\+'
t_MINUS = r'\-'
t_COMMA = r','
t_MINUSMINUS = r'\-\-'
t_MULTIPLY = r'\*'
t_EQ = r'\='
t_NOTEQ = r'\!\='
t_NOT = r'\!'
t_EQEQ = r'\=\='
t_LT = r'\<'
t_GT = r'\>'
t_LTE = r'\<\='
t_GTE = r'\>\='
t_DIVIDE = r'\/'
t_SEMICOL = r'\;'
t_ANDAND = r'&&'
t_AND = r'\&'
t_OR = r'\|'
t_OROR = r'\|\|'
t_POWER = r'\^'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ignore = ' \t\r\n\f\v'


def t_NAME(t):
    r'-?[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value == 'print':
        t.type = 'PRINT'
    elif t.value == 'string':
        t.type = 'STRING'
    elif t.value == 'float':
        t.type = 'FLOAT'
    elif t.value == 'int':
        t.type = 'INT'
    elif t.value == 'char':
        t.type = 'CHAR'
    elif t.value == 'bool':
        t.type = 'BOOL'
    elif t.value == 'for':
        t.type = 'FOR'
    elif t.value == 'struct':
        t.type = 'STRUCT'
    elif t.value == 'true' or t.value == 'false' or t.value == 'True' or t.value == 'False':
        t.type = 'boolValue'
    elif t.value == 'if':
        t.type = 'IF'
    elif t.value == 'else':
        t.type = 'ELSE'
    elif t.value == 'elif':
        t.type = 'ELIF'
    else:
        t.type = 'NAME'
    return t

def t_stringValue(t):
    r'\"[^\"]*"'
    t.value = t.value[1:-1]
    return t

def t_charValue(t):
    r"\'[^\'\"]\'"
    if len(t.value) == 3:
        t.value = t.value[1:-1]
    return t

def t_floatValue(t):
    r'\-?\d*\.\d+'
    t.value = float(t.value)
    return t

def t_intValue(t):
    r'\-?\d+' 
    t.value = int(t.value)
    return t

def t_lineno(t):
    r'\n'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("[LEXER ERROR] LINE", t.lineno)
    print(f"ILLEGAL CHARACTER: {t.value}")
    t.lexer.skip(1)

#text = "nn"
lexer = lex.lex()
#lexer.input(text)
#while True:
        #tok = lexer.token()
        #if not tok: break
        #print (tok)
