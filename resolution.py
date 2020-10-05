# -----------------------------------------------------------------------------
# resolution.py
#
# resolution method implementation
# -----------------------------------------------------------------------------


import re, string

# 1. Tokens

tokens = [ 'VAR', 'IMP', 'CONJ', 'DISJ' ]
literals = ['(', ')', '~']

t_VAR = r'[a-zA-Z]'
t_IMP = r'->'
t_CONJ = r'/\\'
t_DISJ = r'\\/'

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# 2. Main algorithm and helping functions

def negate(lit):
    if lit[0] == "~":
        return lit[1]
    else:
        return "~" + lit

def is_tautology(clause):
    for var in clause:
        if negate(var) in clause:
            return True
    return False

def resolution_step(clauses):
    new_clauses = set()
    for c1 in clauses:
        for var in c1:
            for c2 in clauses:
                if negate(var) in c2 and c1 != c2:
                    new_clause = frozenset((c1 | c2) - {var, negate(var)})
                    if not is_tautology(new_clause):
                        new_clauses.add(new_clause)
    return new_clauses

def resolution(p):
    parsed = list(p)[1].split(r" /\ ")
    regex = re.compile('[%s]' % re.escape("()"))
    clauses = set(frozenset([regex.sub('', var)
                            for var in c.split(r" \/ ")]) for c in parsed)
    while True:
        new_clauses = resolution_step(clauses)
        if frozenset() in  new_clauses:
            return (False, str_repr(clauses))
        elif new_clauses <= clauses:
            return (True, str_repr(clauses))
        else:
            clauses.update(new_clauses)

def str_repr(clauses):
    disjunctions = []
    for clause in clauses:
        if len(clause) > 1:
            s = "(%s)" % (" \/ ".join(list(clause)))
        else:
            s = str(list(clause)[0])
        disjunctions.append(s)
    sorted_disjunctions = sorted(disjunctions, key = lambda x: len(x))
    return  " /\ ".join(sorted_disjunctions)

import ply.yacc as yacc

# 3. Parsing rules

def p_final(p):
    'quest : cnf'
    result, saturated_cnf = resolution(p)
    print("Saturated cnf:", saturated_cnf)
    if result:
        print("Formula is satisfiable")
    else:
        print("Formula is NOT satisfiable")

def p_cnf_disjunction(p):
    "cnf : cnf CONJ '(' disjunction ')'"
    p[0] = p[1] + " " + p[2] + " " + p[3] + p[4] + p[5]

def p_cnf_disjunction_brackets(p):
    "cnf : '(' disjunction ')'"
    p[0] = p[1] + p[2] + p[3]

def p_cnf_conj_litearl(p):
    "cnf : cnf CONJ literal"
    p[0] = p[1] + " " + p[2] + " " + p[3]

def p_cnf_litearl(p):
    "cnf : literal"
    p[0] = p[1]

def p_implication(p):
    'disjunction : VAR IMP literal'
    p[0] = '~' + p[1] + r' \/ ' + p[3]

def p_implication_neg(p):
    'disjunction : "~" VAR IMP literal'
    p[0] = p[2] + r' \/ ' + p[4]

def p_disjunction(p):
    """disjunction : literal DISJ literal"""
    p[0] = p[1] + " " + p[2] + " " + p[3]

def p_literal(p):
    """literal : VAR
               | "~" VAR """
    if p[1] == '~':
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

#Input format: (a -> b) /\ (a \/ b) /\ (b \/ ~c) /\ a /\ ~b
#Please use parentheses for single \/ or -> (e.g. (a -> b))

while True:
    try:
        s = input('Input formula > ')
    except EOFError:
        break
    if not s: continue
    parser.parse(s)
