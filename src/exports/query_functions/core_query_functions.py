import math

from src.dataclass import QueryFunction

min_f = QueryFunction(name="min_f", description="min(x, y)", fn=min, invalid_query_val=-1)
max_f = QueryFunction(name="max_f", description="max(x, y)", fn=max, invalid_query_val=-1)

add_f = QueryFunction(name="add_f", description="x + y", fn=lambda x, y: x + y, invalid_query_val=0)
sub_f = QueryFunction(name="sub_f", description="x - y", fn=lambda x, y: x - y, invalid_query_val=0)
mul_f = QueryFunction(name="mul_f", description="x * y", fn=lambda x, y: x * y, invalid_query_val=-1)
exp_f = QueryFunction(name="exp_f", description="x ** y", fn=lambda x, y: x ** y,invalid_query_val=-1)
mod_f = QueryFunction(name="mod_f", description="x % y", fn=lambda x, y: x % y, invalid_query_val=-1)

and_f = QueryFunction(name="and_f", description="x & y", fn=lambda x, y: x & y, invalid_query_val=-1)
or_f  = QueryFunction(name="or_f",  description="x | y", fn=lambda x, y: x | y, invalid_query_val=-1)
xor_f = QueryFunction(name="xor_f", description="x ^ y", fn=lambda x, y: x ^ y, invalid_query_val=-1)

lcm_f = QueryFunction(name="lcm_f", description="Least Common Multiple of x and y", fn=math.lcm, invalid_query_val=-1)
gcd_f = QueryFunction(name="gcd_f", description="Greatest Common Divisor of x and y", fn=math.gcd, invalid_query_val=1)

avg_f = QueryFunction(name="avg_f", description="The arithmetic mean of x and y", fn=lambda x, y: int((x+y)/2), invalid_query_val=0)

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