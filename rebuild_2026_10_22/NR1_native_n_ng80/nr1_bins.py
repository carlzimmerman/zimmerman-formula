#!/usr/bin/env python3
"""NR1, reported not graded: PRIMARY by V_flat against ET1, NF1 read's own tail with eta(1e12) 21.53 and PRIMARY's ratios. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
FHERE = os.path.dirname(os.path.abspath(__file__)); FRB = os.path.dirname(FHERE); OUTL = []; CER = os.path.join(FRB, "CE1_converged_eta_grade", "ce1_a4_results.json"); r10, r11 = 29.26 / 21.53, 24.34 / 21.53; TABV = [math.log10(r10), math.log10(r11), 0.0]; CHECK = HYP = False; RES = dict(r10=r10, r11=r11)
def Pn(s): print(s, flush=True); OUTL.append(s)
T = open(os.path.join(FRB, "NF1_no_floor_rule", "nf1_native_read.py")).read(); T = T[T.index("ETAJ = json.load"):]
for a, b in (('ETAV = [ETAJ[str(e)]["med"] for e in (12, 13, 14)]', 'ETAV = [21.53, ETAJ["13"]["med"], ETAJ["14"]["med"]]'), ('tg = "nf1_native_check" if CHECK else (f"nf1_native_hyp_{r10:g}_{r11:g}" if HYP else "nf1_native_read")', 'tg = "nr1_bins"')): assert T.count(a) == 1, a; T = T.replace(a, b)
exec(compile(T, "nf1_tail", "exec"))
