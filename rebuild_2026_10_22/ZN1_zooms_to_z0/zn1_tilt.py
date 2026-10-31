#!/usr/bin/env python3
"""ZN1 POST-RESULT, reported only: Argon's audit item G. SM1's +0.111 dex gas offset comes from five massive clusters; it may tilt with mass. The same grade with the offset at +0.111 + t (13.38 - lg Mgas500), t = +/-0.0625 per dex: Mgas500 is the variable the terciles use, and this is about +/-0.04 dex between M3 and M1. kappa = 1/2 FITTED; footings never pooled; not theory closed.
    ZN1_TILT=0.0625 python3 zn1_tilt.py"""
import os, sys
HERE0 = os.path.dirname(os.path.abspath(__file__)); T3 = open(os.path.join(HERE0, "zn1_grade.py")).read(); TILT = os.environ["ZN1_TILT"]
def _s(a, b, n=1):
    global T3
    assert T3.count(a) == n, a
    T3 = T3.replace(a, b)
_s("""\\\\'Mg500 = cl["Mgas500"]*qd**2.5*%r;\\\\' % (10 ** 0.111))""", """\\\\'Mg500 = cl["Mgas500"]*qd**2.5*10**(0.111+(%s)*(13.38-math.log10(cl["Mgas500"])));\\\\' % (""" + TILT + """))""")
_s('TAG = "zn1_MUTATE" if MUT else "zn1"', f'TAG = "zn1_tilt{TILT}"')
_s('os.path.join(HERE, "zn1_results.json")', f'os.path.join(HERE, "zn1_tilt{TILT}_unused.json")', 2)
_s('JOBS = [(f"f* {fs}, X-COP\'s gas", dict(fs=fs, mode="fs", gas=True, shapes=SH)) for fs in ("0.034", "0.0615")] + [(f"f* {fs}, eRASS1\'s own gas", dict(fs=fs, mode="fs", gas=False, shapes=SH)) for fs in ("0.034", "0.0615")] + [(f"f* {fs}, X-COP\'s gas, MA1\'s budget M200", dict(fs=fs, mode="budget", gas=True, shapes=SH)) for fs in ("0.034", "0.0615")] + [(f"f* {fs}, X-COP\'s gas, z = 0 shape for all", dict(fs=fs, mode="fs", gas=True, shapes=SH, snap="0.00")) for fs in ("0.034", "0.0615")]', 'JOBS = [(f"f* {fs}, X-COP\'s gas", dict(fs=fs, mode="fs", gas=True, shapes=SH)) for fs in ("0.034", "0.0615")]')
_s('''    def cls(a, b):''', '''    open(os.path.join(HERE, f"{TAG}.out"), "w").write("\\n".join(OUT) + "\\n"); sys.exit(0)
    def cls(a, b):''')
exec(compile(T3, os.path.abspath(__file__), "exec"))
