_type_list = type([])
_type_string = type("")
_type_int = type(1)

def car(l):
    """The Law of Car
    The primitive ``car`` is defined only for non-empty lists.
    """
    if type(l) == _type_list:
        if len(l) > 0:
            return l[0]
        else: raise TypeError("You cannot ask for the car of the empty list.")
    else: raise TypeError("You cannot ask for the car of the Non-List type.")

def cdr(l):
    """The Law of Cdr
    The primitive ``cdr`` is defined only for non-empty lists.
    The ``cdr`` of any non-empty list is always another list.
    """
    if type(l) == _type_list:
        if len(l) > 0:
            return l[1:]
        else: raise TypeError("You cannot ask for the cdr of the empty list.")
    else: raise TypeError("You cannot ask for the cdr of the Non-List type.")

def cons(atom, list):
    """The Law of Cons
    The primitive ``cons`` takes two arguments.
    The second argument to ``cons`` must be a list.
    The result is a list.
    """
    if type(list) != _type_list:
        raise TypeError("The second argument of cons must be list.")
    list.insert(0, atom)
    return list

def null(l):
    """The Law of Null
    The primitve ``null`` is defined only for lists.
    """
    if type(l) == _type_list:
        if len(l) > 0:
            return False
        return True
    else: raise TypeError("You cannot ask for the car of the empty list.")

def atom(l):
    if type(l) == _type_string or type(l) == _type_int:
        return True
    return False

def eq(a, b):
    """The Law of Eq
    The primitve ``eq`` takes two arguments.
    Each must be a non-numeric atom.
    """
    if not atom(a) or not atom(b):
        raise TypeError("Both arguments must be non-numeric atoms.")
    return a == b

"""The First Commandment
(preliminary)
Always ask ``null`` as first question in expressing any function.
"""

def lat(l):
    if null(l):
        return True
    elif atom(car(l)):
        return lat(cdr(l))
    else:
        return False

def member(a, lat):
    if null(lat):
        return False
    else:
        return eq(a, car(lat)) or member(a, cdr(lat))

"""The Second Commandment
Use ``cons`` to build lists.
"""

def rember(a, lat):
    if null(lat):
        return []
    elif eq(a, car(lat)):
        return cdr(lat)
    else:
        return cons(car(lat), rember(a, cdr(lat)))

def firsts(l):
    if null(l):
        return []
    else:
        return cons(car(car(l)), firsts(cdr(l)))

"""The Third Commandment
When building a list, describe the first typical element,
and the ``cons`` it onto the natural recursion.
"""

def multiinsertL(new, old, lat):
    if null(lat):
        return []
    elif eq(old, car(lat)):
        return cons(new, cons(car(lat), multiinsertL(new, old, cdr(lat))))
    else:
        return cons(car(lat), multiinsertL(new, old, cdr(lat)))

"""The Fourth Commandment
(preliminary)
Always change at least one argument at recurring.
It must be changed to be closer to termination.
The changing argument must be tested in termination condition:
when using ``cdr``, test termination with ``null``.
"""

def add1(n):
    return n + 1

def sub1(n):
    return n - 1

def zero(n):
    return n == 0

def add(n, m):
    if zero(m):
        return n
    else:
        return add1(add(n, sub1(m)))

def sub(n, m):
    if zero(m):
        return n
    else:
        return sub1(sub(n, sub1(m)))

"""The First Commandment
(first revision)
When recuring on a list of atoms, lat, ask two questions about it:
``null(lat)`` and else.
When recuring on a number, n, ask two questions about it:
``zero(n)`` and else.
"""

def addtup(t):
    if null(t):
        return 0
    else:
        return add(car(t), addtup(cdr(t)))

"""The Fourth Commandment
(first revision)
Always change at least one argument at recurring.
It must be changed to be closer to termination.
The changing argument must be tested in termination condition:
when using ``cdr``, test termination with ``null``.
when using ``sub1``, test termination with ``zero``.
"""

def mul(n, m):
    if zero(m):
        return 0
    else:
        return add(n, mul(n, sub1(m)))

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

def tupAdd(tup1, tup2):
    if null(tup1) and null(tup2):
        return []
    else:
        return cons(add(car(tup1), car(tup2)), tupAdd(cdr(tup1), cdr(tup2)))

def length(lat):
    if null(lat):
        return 0
    else:
        return add1(length(cdr(lat)))

def pick(n, lat):
    if null(lat) or zero(n):
        return None
    elif n == 1:
        return car(lat)
    else:
        return pick(sub1(n), cdr(lat))

def rempick(n, lat):
    if null(lat) or zero(n):
        return lat
    elif n == 1:
        return cdr(lat)
    else:
        return cons(car(lat), rempick(sub1(n), cdr(lat)))

def number(n):
    return type(n) == _type_int

def non_nums(lat):
    if null(lat):
        return lat
    elif number(car(lat)):
        return non_nums(cdr(lat))
    else:
        return cons(car(lat), non_nums(cdr(lat)))

def eqan(n, m):
    if number(n) and number(m):
        return n == m
    elif number(n) or number(m):
        return False
    else:
        return eq(n, m)

def occur(a, lat):
    if null(lat):
        return 0
    elif eqan(a, car(lat)):
        return add1(occur(a, cdr(lat)))
    else:
        return occur(a, cdr(lat))

def rember_star(a, l):
    if null(l):
        return l
    elif atom(car(l)):
        if eqan(a, car(l)):
            return rember_star(a, cdr(l))
        else:
            return cons(car(l), rember_star(a, cdr(l)))
    else:
        return cons(rember_star(a, car(l)), rember_star(a, cdr(l)))

def insertR_star(new, old, l):
    if null(l):
        return l
    elif atom(car(l)):
        if eqan(old, car(l)):
            return cons(car(l), cons(new, insertR_star(new, old, cdr(l))))
        else:
            return cons(car(l), insertR_star(new, old, cdr(l)))
    else:
        return cons(insertR_star(new, old, car(l)), insertR_star(new, old, cdr(l)))

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
    if null(l):
        return 0
    elif atom(car(l)):
        if eqan(a, car(l)):
            return add1(occur_star(a, cdr(l)))
        else:
            return occur_star(a, cdr(l))
    else:
        return add(occur_star(a, car(l)), occur_star(a, cdr(l)))

def eqlist(l1, l2):
    if null(l1) and null(l2):
        return True
    elif null(l1) or null(l2):
        return False
    elif atom(car(l1)) and atom(car(l2)):
        if eqan(car(l1), car(l2)):
            return eqlist(cdr(l1), cdr(l2))
        else:
            return False
    elif atom(car(l1)) or atom(car(l2)):
        return False
    else:
        return eqlist(car(l1), car(l2)) and eqlist(cdr(l1), cdr(l2))
