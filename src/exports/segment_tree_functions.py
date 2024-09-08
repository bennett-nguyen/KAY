import math

from src.core.dataclasses import Function

min_f = Function("min_f", min, -1)
max_f = Function("max_f", max, -1)

add_f = Function("add_f", lambda x, y: x + y, -1)
sub_f = Function("sub_f", lambda x, y: x - y, -1)
mul_f = Function("mul_f", lambda x, y: x * y, -1)
exp_f = Function("exp_f", lambda x, y: x ** y, -1)
mod_f = Function("mod_f", lambda x, y: x % y, -1)

and_f = Function("and_f", lambda x, y: x & y, -1)
or_f = Function("or_f", lambda x, y: x | y, -1)
xor_f = Function("xor_f", lambda x, y: x ^ y, -1)

lcm_f = Function("lcm_f", math.lcm, -1)
gcd_f = Function("gcd_f", math.gcd, 1)

avg_f = Function("avg_f", lambda x, y: int((x+y)/2), 0)

st_exported_functions: list[Function] = [
    min_f,
    max_f,

    add_f,
    sub_f,
    mul_f,
    exp_f,
    mod_f,

    and_f,
    or_f,
    xor_f,

    lcm_f,
    gcd_f,
    avg_f,
]