#!/usr/bin/env python3
"""ZN1 POST-RESULT, reported only: my README says the frozen closure M_c(r_ta) = M_fair, a thin shell near r_ta with gamma about -39, barely touches the keys. Test it: the same grade with no tail at all (M_c constant beyond x_edge R200). kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys
HERE0 = os.path.dirname(os.path.abspath(__file__)); T3 = open(os.path.join(HERE0, "zn1_grade.py")).read()
def _s(a, b, n=1):
    global T3
    assert T3.count(a) == n, a
    T3 = T3.replace(a, b)
_s("""open({os.path.join(HERE, 'zn1_def.py')!r}).read()""", """open({os.path.join(HERE, 'zn1_def.py')!r}).read().replace('if Me >= Mf:', 'if True:')""")
_s('TAG = "zn1_MUTATE" if MUT else "zn1"', 'TAG = "zn1_notail"')
_s('os.path.join(HERE, "zn1_results.json")', 'os.path.join(HERE, "zn1_notail_unused.json")', 2)
exec(compile(T3, os.path.abspath(__file__), "exec"))
