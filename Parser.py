import lex

# List of token names.   This is always required
tokens = (
   '32_BIT_USIGN_INT',
   'ID',
   'PLUS',            # + (also positive)
   'MINUS',           # - (also negate) 
   'MULTIPLY',        # *
   'DIVIDE',          # /
   'LPAREN',          # (
   'RPAREN',          # )
   'INCREMENT',       # ++
   'DECREMENT',       # --
   'ADDRESS',         # & (also bit wise AND)
   'MODULO',          # %
   'COMMA',           # ,
   'ASSIGN',          # :=
   'EQUALITY',        # ==
   'INEQUALITY',      # !=
   #'LOGICAL_AND',     # &&
   'GREATER_THAN',    # >
   'LESS_THAN',       # <
   'GREATER_THAN_EQ', # >=
   'LESS_THAN_EQ',    # <=
   'XOR',             # ^
   'INCLUSIVE_OR',    # |
   #'LOGICAL_OR'       # ||
)

reserved = {
  'var' : 'VAR',
  'store' : 'STORE',
  'load' : 'LOAD',
  'goto' : 'GOTO',
  'assert' : 'ASSERT',
  'if' : 'IF',
  'then' : 'THEN',
  'else' : 'ELSE',
  'get_input' : 'GET_INPUT',
  'print_output' : 'PRINT_OUTPUT'#,
  #'true' : 'TRUE',
  #'false' : 'FALSE'
}

# Regular expression rules for simple tokens
t_PLUS              = r'\+'
t_MINUS             = r'-'
t_MULTIPLY          = r'\*'
t_DIVIDE            = r'/'
t_LPAREN            = r'\('
t_RPAREN            = r'\)'
t_INCREMENT         = r'\+\+'
t_DECREMENT         = r'--'
t_ADDRESS           = r'&'
t_MODULO            = r'%'
t_COMMA             = r','
t_ASSIGN            = r':='
t_EQUALITY          = r'=='
t_INEQUALITY        = r'!='
#t_LOGICAL_AND       = r'&&'
t_GREATER_THAN      = r'\>'
t_LESS_THAN         = r'\<'
t_GREATER_THAN_EQ   = r'\>='
t_LESS_THAN_EQ      = r'\<='
t_XOR               = r'\^'
t_INCLUSIVE_OR      = r'\|'
#t_LOGICAL_OR        = r'\|\|'

tokens = list(tokens) + list(reserved.values())

# A regular expression rule with some action code
def t_32_BIT_USIGN_INT(t):
    r'\d+'
    # We are going to cheat for now and just mod max 32 bit value
    if int(t.value) > 4294967295:
      t.value = int(t.value) % 4294967295
    else:
      t.value = int(t.value)
    return t

# Define a regular expression for variables
def t_ID(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = reserved.get(t.value,'ID')    # Check for reserved words
  return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

############################################################################

import yacc as yacc


# Production rule for program
def p_start(p):
	'''start	: statement_list'''

# Production rules for statement lists
def p_statement_list(p):
	'''statement_list	: statement_list statement
						| statement
						|'''

# Production rules for statements
def p_statement(p):
	'''statement	: VAR ID
					| VAR ID ASSIGN expression
					| ID ASSIGN expression
             		| STORE LPAREN expression COMMA expression RPAREN
             		| GOTO expression 
             		| ASSERT bool_expression
             		| IF LPAREN bool_expression RPAREN THEN GOTO expression ELSE GOTO expression
             		| PRINT_OUTPUT LPAREN expression RPAREN'''
	print ("MESSAGE =====> Length of p = %d") % len(p)
	print "MESSAGE =====> Parsed a statement ", 

		

# Production rules for expressions
def p_expression(p):
	'''expression 	: expression add_op term
					| term'''

# Production rules for addition operations
def p_add_op(p):
	'''add_op 		: PLUS
					| MINUS'''

# Prodution rules for factor operations. We are giving the
# logical operations the same precedence as factors
def p_term(p):
	'''term 		: term mulop factor
					| factor'''

# Production rules for the factor operators
def p_mulop(p):
	'''mulop 		: MULTIPLY
					| DIVIDE
					| MODULO
					| XOR
					| INCLUSIVE_OR
					| ADDRESS'''

# Production rules for factos
def p_factor(p):
	'''factor 		: unary_op factor
					| LPAREN expression RPAREN
					| 32_BIT_USIGN_INT
					| ID
					| GET_INPUT LPAREN RPAREN
					| LOAD LPAREN expression RPAREN'''

# Production rules for boolean expressions
def p_bool_expression(p):
	'''bool_expression 	: expression rel_op expression'''

# Production rules for relational operators
def p_rel_op(p): 
	'''rel_op 		: EQUALITY
					| INEQUALITY
					| LESS_THAN
					| GREATER_THAN
					| LESS_THAN_EQ
					| GREATER_THAN_EQ'''

# Production rules for unary operators
def p_unary_op(p):
	'''unary_op 	: PLUS 
					| MINUS 
					| INCREMENT 
					| DECREMENT 
					| ADDRESS'''
	




def parse(source_code):
	# Build the lexer
  	lexer = lex.lex()

  	# Give the lexer the source code
  	lexer.input(source_code)
	while True:
		tok = lexer.token()
		if not tok: break      # No more input
		print tok

	# Build the parser
	parser = yacc.yacc()

	# Parse the source code
	p = parser.parse(source_code, debug=True, tracking=True)

	print(p)