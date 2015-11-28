import sympy as s
import sympy.mpmath as m
from sympy.parsing.sympy_parser import parse_expr

def eval_expr(expr, x_):
    """ Evaluate the expression with a given x value. If the expression
    isn't numerical at this point, return false. Else, return the value.
    """
    try:
        x = s.symbols("x")
        return float(expr.subs(x, x_))
    except TypeError:
        return False
    except SyntaxError:
        return False

# Accept input from the user as a sympy expression; handle all possible errors
print "Please input an expression."
expr = raw_input()
test = s.simplify(parse_expr(expr))

if not test == False:
    print test