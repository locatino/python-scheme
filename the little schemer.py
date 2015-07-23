_type_list = type([])

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
    if type(list) == _type_list:
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
