import math

from src.dataclass import QueryFunction

min_f = QueryFunction("min_f", min, -1)
max_f = QueryFunction("max_f", max, -1)

add_f = QueryFunction("add_f", lambda x, y: x + y, 0)
sub_f = QueryFunction("sub_f", lambda x, y: x - y, 0)
mul_f = QueryFunction("mul_f", lambda x, y: x * y, -1)
exp_f = QueryFunction("exp_f", lambda x, y: x ** y, -1)
mod_f = QueryFunction("mod_f", lambda x, y: x % y, -1)

and_f = QueryFunction("and_f", lambda x, y: x & y, -1)
or_f = QueryFunction("or_f", lambda x, y: x | y, -1)
xor_f = QueryFunction("xor_f", lambda x, y: x ^ y, -1)

lcm_f = QueryFunction("lcm_f", math.lcm, -1)
gcd_f = QueryFunction("gcd_f", math.gcd, 1)

avg_f = QueryFunction("avg_f", lambda x, y: int((x+y)/2), 0)

exported_core_query_functions: list[QueryFunction] = [
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