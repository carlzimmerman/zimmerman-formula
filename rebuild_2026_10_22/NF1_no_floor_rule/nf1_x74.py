#!/usr/bin/env python3
"""NF1_no_floor_rule: X74's grader with FC1's conversions (through cn1_x74's text, contraction off) and, with NF1_ON=1, no floor: S = f_c eta Sigma_coll at every mass; NF1_S the slope of eta below 1e12; NF1_MUT a factor on S.
    kappa = 1/2 FITTED; not theory closed."""
import os
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
T = open(os.path.join(REB, "CN1_contraction_on_cold_share", "cn1_x74.py")).read(); a = "INJ = r'''\n"; assert T.count(a) == 1
ADD = """sub('    return max(s, sc), sc > s', '    return (sc * float(os.environ.get("NF1_MUT", "1")) * 10 ** (float(os.environ.get("NF1_S", "0")) * max(0.0, 12.0 - math.log10(M))), True) if os.environ.get("NF1_ON") == "1" and ETA_USE["v"] == ETA else (max(s, sc), sc > s)')\n"""
T = T.replace(a, a + ADD); T = T.replace('HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)', f'HERE = {HERE!r}; REB = {REB!r}')
exec(compile(T, os.path.join(HERE, "cn1_x74_nf1"), "exec"))
