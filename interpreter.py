import sys
from enum import Enum




_type_string = type("")

source_path = sys.argv[1]

source_file = open(source_path).read().strip()

def StoList(s):
    if s[0] != "(":
        if s.isdigit():
            return int(s)
        else:
            return s
    tmp = []
    l = []
    i = 1
    while i < len(s) - 1:
        if s[i] == "(":
            start = i
            count = 1
            new_end = 0
            for j in range(i + 1, len(s) - 1):
                if s[j] == "(":
                    count += 1
                elif s[j] == ")":
                    count -= 1
                if count == 0:
                    new_end = j + 1
                    break
            l.append(StoList(s[start:new_end]))
            i = new_end + 1
        elif s[i] == " ":
            if len(tmp) != 0:
                l.append("".join(tmp))
                tmp = []
            i += 1
        else:
            tmp.append(s[i])
            i += 1
    if len(tmp) != 0:
        l.append("".join(tmp))
    return l

def ListtoS(l):
    if type(l) == type([]):
        ret = str(l).replace("[","(")
        ret = ret.replace("]",")")
        ret = ret.replace(","," ")
        ret = ret.replace("'","")
        return ret
    else:
        return l

def preprocessor(f):
    def job(*argv):
        l = []
        for i in argv:
            l.append(StoList(i))
        return f(*l)
    return job

def proprocessor(f):
    def job(*argv):
        return ListtoS(f(*argv))
    return job

@proprocessor
@preprocessor
def cons(s, list):
    list.insert(0, s)
    return list

@proprocessor
@preprocessor
def car(t):
    return t[0]

@proprocessor
@preprocessor
def cdr(t):
    return t[1:]


def first(s):
    return car(s)

def second(s):
    return car(cdr(s))

def third(e):
    return car(cdr(cdr(e)))

@preprocessor
def null(s):
    if len(s) == 0:
        return True
    else:
        return False

@preprocessor
def eq(a, b):
    return a == b


def lookup_in_entry_help(name, names, values, entry_f):
    if null(names):
        return entry_f(name)
    elif eq(name, car(names)):
        return car(values)
    else:
        return lookup_in_entry_help(name, cdr(names), cdr(values), entry_f)

def lookup_in_entry(name, entry, entry_f):
    return lookup_in_entry_help(name, first(entry), second(entry), entry_f)

def lookup_in_table(name, table, table_f):
    if null(table):
        return table_f(name)
    else:
        return lookup_in_entry(name, car(table),
        lambda name: lookup_in_table(name, cdr(table), table_f))

def number(e):
    return e.isdigit()

def atom(e):
    return e[0] != "("

@preprocessor
def add1(n):
    return n + 1

@preprocessor
def zero(n):
    return n == 0

def build(a, b):
    return cons(a, cons(b, "()"))

def Const(e, table):
    if number(e):
        return e
    elif eq(e, "True") or eq(e, "False"):
        return e
    else:
        return build("primitve", e)

def Quote(e, table):
    return car(cdr(e))

def initial_table(name):
    return car("()")

def Identifier(e, table):
    return lookup_in_table(e, table, initial_table)

def Lambda(e, table):
    return build("non-primitive", cons(table, cdr(e)))


table_of = first
formals_of = second
body_of = third

def Else(x):
    if atom(x):
        return eq(x, "else")
    else:
        return False

question_of = first
answer_of = second

def atom_to_action(e):
    if number(e) or eq(e, "True") or eq(e, "False") or eq(e, "cons") or eq(e, "car") or eq(e, "cdr") or eq(e, "null") or eq(e, "eq") or eq(e, "atom") or eq(e, "sub1") or eq(e, "add1") or eq(e, "number") or eq(e, "zero"):
        return Const
    else:
        return Identifier

def list_to_action(e):
    if atom(e):
        if eq(car(e), "quote"):
            return Quote
        elif eq(car(e), "lambda"):
            return Lambda
        elif eq(car(e), "cond"):
            return Cond
        else:
            return Application
    else:
        return Application

def expression_to_action(e):
    if atom(e):
        return atom_to_action(e)
    else:
        return list_to_action(e)

def meaning(e, table):
    return (expression_to_action(e))(e, table)

def evcon(lines, table):
    if Else(question_of(car(lines))):
        return meaning(answer_of(car(lines)), table)
    elif meaning(question_of(car(lines)), table):
        return meaning(answer_of(car(lines)), table)
    else:
        return evcon(cdr(lines), table)

cond_lines_of = cdr

def Cond(e, table):
    return evcon(cond_lines_of(e), table)

print(Cond("(cond (coffee klatsch) (else party))","(((coffee) (True)) ((klatsch party) (5 (6))))"))
