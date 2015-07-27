import sys
sys.setrecursionlimit(5000)

_type_list = type([])
_type_string = type("")
_type_int = type(1)

def _car(l):
    """The Law of Car
    The primitive ``car`` is defined only for non-empty lists.
    """
    if type(l) == _type_list:
        if len(l) > 0:
            return l[0]
        else: raise TypeError("You cannot ask for the car of the empty list.")
    else: raise TypeError("You cannot ask for the car of the Non-List type.")

def car():
    return lambda l: l[0] if type(l) == _type_list and len(l) > 0 else (TypeError("You cannot ask for the car of the empty list.") if len(l) <= 0 else TypeError("You cannot ask for the car of the Non-List type."))

def _cdr(l):
    """The Law of Cdr
    The primitive ``cdr`` is defined only for non-empty lists.
    The ``cdr`` of any non-empty list is always another list.
    """
    if type(l) == _type_list:
        if len(l) > 0:
            return l[1:]
        else: raise TypeError("You cannot ask for the cdr of the empty list.")
    else: raise TypeError("You cannot ask for the cdr of the Non-List type.")

def cdr():
    return lambda l: l[1:] if type(l) == _type_list and len(l) > 0 else (TypeError("You cannot ask for the cdr of the empty list.") if len(l) <= 0 else TypeError("You cannot ask for the cdr of the Non-List type."))

def _cons(s, list):
    """The Law of Cons
    The primitive ``cons`` takes two arguments.
    The second argument to ``cons`` must be a list.
    The result is a list.
    """
    if type(list) != _type_list:
        raise TypeError("The second argument of cons must be list.")
    list.insert(0, s)
    return list

def cons():
    return lambda s, list: list if list.insert(0, s) == None else (TypeError("The second argument of cons must be list.") if type(list) != _type_list else list)

def _null(l):
    """The Law of Null
    The primitve ``null`` is defined only for lists.
    """
    if type(l) == _type_list:
        if len(l) > 0:
            return False
        return True
    else: raise TypeError("You cannot ask for the car of the empty list.")

def null():
    return lambda l: False if type(l) == _type_list and len(l) > 0 else (True if type(l) == _type_list and len(l) <= 0 else TypeError("You cannot ask for the car of the empty list."))

def _atom(l):
    if type(l) == _type_string or type(l) == _type_int:
        return True
    return False

def atom():
    return lambda l: True if type(l) == _type_string or type(l) == _type_int else False

def _eq(a, b):
    """The Law of Eq
    The primitve ``eq`` takes two arguments.
    Each must be a non-numeric atom.
    """
    if not _atom(a) or not _atom(b):
        raise TypeError("Both arguments must be atoms.")
    return a == b

def eq():
    return lambda a, b: TypeError("Both arguments must be atoms.") if not atom()(a) or not atom()(b) else a == b

"""The First Commandment
(preliminary)
Always ask ``null`` as first question in expressing any function.
"""

def _lat(l):
    if _null(l):
        return True
    elif _atom(_car(l)):
        return _lat(_cdr(l))
    else:
        return False

def lat():
    return lambda l:True if null()(l) else (lat()(cdr()(l)) if atom()(car()(l)) else False)

def _member(a, lat):
    if _null(lat):
        return False
    else:
        return _eq(a, _car(lat)) or _member(a, _cdr(lat))

def member():
    return lambda a, lat: False if null()(lat) else eq()(a, car()(lat)) or member()(a, cdr()(lat))


"""The Second Commandment
Use ``cons`` to build lists.
"""

def _rember(a, lat):
    if _null(lat):
        return lat
    elif _eq(a, _car(lat)):
        return _cdr(lat)
    else:
        return _cons(car(lat), _rember(a, _cdr(lat)))

def rember():
    return lambda a, lat: lat if null()(lat) else (cdr()(lat) if eq()(a, car()(lat)) else cons()(car()(lat), rember()(a, cdr()(lat))))

def _firsts(l):
    if _null(l):
        return l
    else:
        return _cons(_car(_car(l)), _firsts(_cdr(l)))

def firsts():
    return lambda l: l if null()(l) else cons()(car()(car()(l)), firsts()(cdr()(l)))

def _seconds(l):
    if _null(l):
        return l
    else:
        return _cons(_car(_cdr(_car(l))), _seconds(_cdr(l)))

def seconds():
    return lambda l: l if null()(l) else cons()(car()(cdr()(car()(l))), seconds()(cdr()(l)))

"""The Third Commandment
When building a list, describe the first typical element,
and the ``cons`` it onto the natural recursion.
"""

def _multiinsertL(new, old, lat):
    if null(lat):
        return lat
    elif _eq(old, car(lat)):
        return _cons(new, _cons(car(lat), _multiinsertL(new, old, _cdr(lat))))
    else:
        return _cons(_car(lat), _multiinsertL(new, old, _cdr(lat)))

def multiinsertL():
    return lambda new, old, lat: lat if null()(lat) else (cons()(new, cons()(car()(lat), multiinsertL()(new, old, cdr()(lat)))) if eq()(old, car()(lat)) else cons()(car()(lat), multiinsertL()(new, old, cdr()(lat))))

"""The Fourth Commandment
(preliminary)
Always change at least one argument at recurring.
It must be changed to be closer to termination.
The changing argument must be tested in termination condition:
when using ``cdr``, test termination with ``null``.
"""

def _add1(n):
    return n + 1

def add1():
    return lambda n: n + 1

def _sub1(n):
    return n - 1

def sub1():
    return lambda n: n - 1

def _zero(n):
    return n == 0

def zero():
    return lambda n: n == 0

def _add(n, m):
    if _zero(m):
        return n
    else:
        return _add1(_add(n, _sub1(m)))

def add():
    return lambda n, m: n if zero()(m) else add1()(add()(n, sub1()(m)))

def _sub(n, m):
    if _zero(m):
        return n
    else:
        return _sub1(_sub(n, _sub1(m)))

def sub():
    return lambda n, m: n if zero()(m) else sub1()(sub()(n, sub1()(m)))

"""The First Commandment
(first revision)
When recuring on a list of atoms, lat, ask two questions about it:
``null(lat)`` and else.
When recuring on a number, n, ask two questions about it:
``zero(n)`` and else.
"""

def _addtup(t):
    if _null(t):
        return 0
    else:
        return _add(car(t), _addtup(_cdr(t)))

def addtup():
    return lambda t: 0 if null()(t) else add()(car()(t), addtup()(cdr()(t)))

"""The Fourth Commandment
(first revision)
Always change at least one argument at recurring.
It must be changed to be closer to termination.
The changing argument must be tested in termination condition:
when using ``cdr``, test termination with ``null``.
when using ``sub1``, test termination with ``zero``.
"""

def _mul(n, m):
    if _zero(m):
        return 0
    else:
        return _add(n, _mul(n, _sub1(m)))

def mul():
    return lambda n, m: 0 if zero()(m) else add()(n, mul()(n, sub1()(m)))

def _expt(n, m):
    if _zero(m):
        return 1
    else:
        return _mul(n, _expt(n, _sub1(m)))

def expt():
    return lambda n, m: 1 if zero()(m) else (mul()(n, expt()(n, sub1()(m))))

"""The Fifth Commandment
When building a value with ``add``,
always use 0 for the value of the termination line,
for adding 0 does not change the value of an addition.

When building a value with ``mul``,
always use 1 for the value of the termination line,
for multiplying 1 does not change the value of a multiplication.

When building a value with ``cons``,
always consider [] for the value of the termination line.
"""

def _tupAdd(tup1, tup2):
    if _null(tup1) and _null(tup2):
        return []
    else:
        return _cons(_add(_car(tup1), _car(tup2)), _tupAdd(_cdr(tup1), _cdr(tup2)))

def tupAdd():
    return lambda tup1, tup2: [] if null()(tup1) and null()(tup2) else cons()(add()(car()(tup1), car()(tup2)), tupAdd()(cdr()(tup1), cdr()(tup2)))

def _length(lat):
    if _null(lat):
        return 0
    else:
        return _add1(_length(_cdr(lat)))

def length():
    return lambda lat: 0 if null(lat) else add1()(length()(cdr()(lat)))

def _pick(n, lat):
    if _null(lat) or _zero(n):
        return None
    elif n == 1:
        return _car(lat)
    else:
        return _pick(_sub1(n), _cdr(lat))

def pick():
    return lambda n, lat: None if null()(lat) or zero()(n) else (car()(lat) if n == 1 else pick()(sub1()(n), cdr()(lat)))

def _rempick(n, lat):
    if _null(lat) or _zero(n):
        return lat
    elif n == 1:
        return _cdr(lat)
    else:
        return _cons(car(lat), _rempick(sub1(n), _cdr(lat)))

def rempick():
    return lambda n, lat: lat if null()(lat) or zero()(n) else (cdr()(lat) if n == 1 else cons()(car()(lat), rempick()(sub1()(n), cdr()(lat))))

def _number(n):
    try:
        return type(n) == _type_int or type(int(n)) == _type_int
    except:
        return False

#positive only
def number():
    return lambda n: type(n) == _type_int or n.isdigit()

def _non_nums(lat):
    if _null(lat):
        return lat
    elif _number(car(lat)):
        return _non_nums(_cdr(lat))
    else:
        return _cons(_car(lat), _non_nums(_cdr(lat)))

def non_nums():
    return lambda lat: lat if null()(lat) else (non_nums()(cdr()(lat)) if number()(car()(lat)) else cons()(car()(lat), non_nums()(cdr()(lat))))

def _eqan(n, m):
    if _number(n) and _number(m):
        return n == m
    elif _number(n) or _number(m):
        return False
    else:
        return _eq(n, m)

def eqan():
    return lambda n, m: n == m if number()(n) and number()(m) else (False if number()(n) or number()(m) else eq()(n, m))

def _occur(a, lat):
    if _null(lat):
        return 0
    elif _eqan(a, _car(lat)):
        return _add1(_occur(a, _cdr(lat)))
    else:
        return _occur(a, _cdr(lat))

def occur():
    return lambda a, lat: 0 if null()(lat) else (add1()(occur()(a, cdr()(lat))) if eqan()(a, car()(lat)) else occur()(a, cdr()(lat)))

def _rember_star(a, l):
    if _null(l):
        return l
    elif _atom(_car(l)):
        if _eqan(a, _car(l)):
            return _rember_star(a, _cdr(l))
        else:
            return _cons(_car(l), _rember_star(a, _cdr(l)))
    else:
        return _cons(_rember_star(a, _car(l)), _rember_star(a, _cdr(l)))

def rember_star():
    return lambda a, l: l if null()(l) else (rember_star()(a, cdr()(l)) if atom()(car()(l)) and eqan()(a, car()(l)) else (cons()(car()(l), rember_star()(a, cdr()(l))) if atom()(car()(l)) and not eqan()(a, car()(l)) else cons()(rember_star()(a, car()(l)), rember_star()(a, cdr()(l)))))

def _insertR_star(new, old, l):
    if _null(l):
        return l
    elif _atom(_car(l)):
        if _eqan(old, _car(l)):
            return _cons(_car(l), _cons(new, _insertR_star(new, old, _cdr(l))))
        else:
            return _cons(_car(l), _insertR_star(new, old, _cdr(l)))
    else:
        return _cons(_insertR_star(new, old, _car(l)), _insertR_star(new, old, _cdr(l)))

def insertR_star():
    return lambda new, old, l: l if null()(l) else (cons()(car()(l), cons()(new, insertR_star()(new, old, cdr()(l)))) if atom()(car()(l)) and eqan()(old, car()(l)) else (cons()(car()(l), insertR_star()(new, old, cdr()(l))) if atom()(car()(l)) and not eqan()(old, car()(l)) else cons()(insertR_star()(new, old, car()(l)), insertR_star()(new, old, cdr()(l)))))

"""The First Commandment
(final version)
When recuring on a list of atoms, lat, ask two questions about it:
``null(lat)`` and else.
When recuring on a number, n, ask two questions about it:
``zero(n)`` and else.
When recuring on a list of S-expressions, l, ask three questions about it:
``null(l)``, ``atom(car(l))``, and else.
"""

"""The Fourth Commandment
(final version)
Always change at least one argument at recurring.
When recurring on a list of atoms, lat, using ``cdr(lat)``.
When recurring on a number, n, using ``sub1(n)``.
And when recurring on a list of S-expressions, l, use ``car(l)``
and ``cdr(l)`` if neither ``null(l)`` nor ``atom(car(l))`` are true.

It must be changed to be closer to termination.
The changing argument must be tested in termination condition:
when using ``cdr``, test termination with ``null``.
when using ``sub1``, test termination with ``zero``.
"""

def occur_star(a, l):
    if _null(l):
        return 0
    elif _atom(_car(l)):
        if _eqan(a, _car(l)):
            return _add1(_occur_star(a, _cdr(l)))
        else:
            return _occur_star(a, _cdr(l))
    else:
        return _add(_occur_star(a, _car(l)), _occur_star(a, _cdr(l)))

def occur_star():
    return lambda a, l: 0 if null()(l) else (add1()(occur_star()(a, cdr()(l))) if atom()(car()(l)) and eqan()(a, car()(l)) else (occur_star()(a, cdr()(l)) if atom()(car()(l)) and not eqan()(a, car()(l)) else add()(occur_star()(a, car()(l)), occur_star()(a, cdr()(l)))))

def _eqlist(l1, l2):
    if _null(l1) and _null(l2):
        return True
    elif _null(l1) or _null(l2):
        return False
    elif _atom(_car(l1)) and _atom(_car(l2)):
        if _eqan(_car(l1), _car(l2)):
            return _eqlist(_cdr(l1), _cdr(l2))
        else:
            return False
    elif _atom(_car(l1)) or _atom(_car(l2)):
        return False
    else:
        return _eqlist(_car(l1), _car(l2)) and _eqlist(_cdr(l1), _cdr(l2))

def eqlist():
    return lambda l1, l2: True if null()(l1) and null()(l2) else (False if null()(l1) or null()(l2) else (eqlist()(cdr()(l1), cdr()(l2)) if atom()(car()(l1)) and atom()(car()(l2)) and eqan()(car()(l1), car()(l2)) else (False if atom()(car()(l1)) and atom()(car()(l2)) and not eqan()(car()(l1), car()(l2)) else eqlist()(car()(l1), car()(l2)) and eqlist()(cdr()(l1), cdr()(l2)))))

def _equal(s1, s2):
    if _atom(s1) and _atom(s2):
        return eq(s1, s2)
    if _atom(s1) or _atom(s2):
        return False
    else:
        return _eqlist(s1, s2)

def equal():
    return lambda s1, s2: eq()(s1, s2) if atom()(s1) and atom()(s2) else (False if atom()(s1) or atom()(s2) else eqlist()(s1, s2))

"""The Sixth Commandment
Simplify only after the function is correct.
"""

def _numbered(aexp):
    if _atom(aexp):
        return _number(aexp)
    else:
        return _number(_car(aexp)) and _number(_car(_cdr(_cdr(aexp))))

def numbered():
    return lambda aexp: number()(aexp) if atom()(aexp) else number()(car()(aexp)) and number()(car()(cdr()(cdr()(aexp))))

"""The Seventh Commandment
Recur on the subparts that are of the same nature:
    ·On the sublists of a list.
    ·On the subexpressions of an arithmetic expression.
"""

def _operator(aexp):
    return _car(aexp)

def operator():
    return lambda aexp: car()(aexp)

def _first_sub_exp(aexp):
    return _car(_cdr(aexp))

def first_sub_exp():
    return lambda aexp: car()(cdr()(aexp))

def _second_sub_exp(aexp):
    return _car(_cdr(_cdr(aexp)))

def second_sub_exp():
    return lambda aexp: car()(cdr()(cdr()(aexp)))

def _value(nexp):
    if _atom(nexp):
        return nexp
    elif _eq(_operator(nexp), "add"):
        return _add(_value(_first_sub_exp(nexp)), _value(_second_sub_exp(nexp)))
    elif _eq(_operator(nexp), "mul"):
        return _mul(_value(_first_sub_exp(nexp)), _value(_second_sub_exp(nexp)))
    else:
        return _expt(_value(_first_sub_exp(nexp)), _value(_second_sub_exp(nexp)))

def value():
    return lambda nexp: nexp if atom()(nexp) else (add()(value()(first_sub_exp()(nexp)), value()(second_sub_exp()(nexp))) if eq()(operator()(nexp), "add") else (mul()(value()(first_sub_exp()(nexp)), value()(second_sub_exp()(nexp))) if eq()(operator()(nexp), "mul") else expt()(value()(first_sub_exp()(nexp)), value()(second_sub_exp()(nexp)))))

"""The Eighth Commandment
Use help functions to abstract from representations.
"""

def _set(lat):
    if _null(lat):
        return True
    elif _member(_car(lat), _cdr(lat)):
        return False
    else:
        return _set(_cdr(lat))

def set():
    return lambda lat: True if null()(lat) else (False if member()(car()(lat), cdr()(lat)) else set()(cdr()(lat)))

def _makeset(lat):
    if _null(lat):
        return lat
    elif _member(_car(lat), _cdr(lat)):
        return _makeset(cdr(lat))
    else:
        return _cons(_car(lat), _makeset(_cdr(lat)))

def makeset():
    return lambda lat: lat if null()(lat) else (makeset()(cdr()(lat)) if member()(car()(lat), cdr()(lat)) else cons()(car()(lat), makeset()(cdr()(lat))))

def _first(l):
    return _car(l)

def first():
    return lambda l: car()(l)

def _second(l):
    return _car(_cdr(l))

def second():
    return lambda l: car()(cdr()(l))

def _build(s1, s2):
    return _cons(s1, _cons(s2, []))

def build():
    return lambda s1, s2: cons()(s1, cons()(s2, []))

def _fun(lat):
    return _set(_firsts(lat))

def fun():
    return lambda: set()(firsts()(lat))

def _revrel(lat):
    if _null(lat):
        return lat
    else:
        return _cons(_build(_second(car(lat)), _first(_car(lat))), _revrel(_cdr(lat)))

def revrel():
    return lambda lat: lat if null()(lat) else cons()(build()(second()(car()(lat)), first(car()(lat))), revrel()(cdr()(lat)))

def _fullfun(lat):
    return _set(_seconds(lat))

def fullfun():
    return lambda: set()(seconds()(lat))

def _one_to_one(lat):
    return _fun(_revrel(lat))

def one_to_one():
    return lambda lat: fun()(revrel()(lat))

def _rember_f(test, a, l):
    if _null(l):
        return l
    elif test(a, _car(l)):
        return _rember_f(test, a, _cdr(l))
    else:
        return _cons(_car(l), _rember_f(test, a, _cdr(l)))

def rember_f():
    return lambda test: lambda a, l: l if null()(l) else (cdr()(l) if test(car()(l), a) else cons()(car()(l), rember_f()(test)(a, cdr()(l))))
