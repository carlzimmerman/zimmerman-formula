#!/usr/bin/env python3
"""M2 -- red-team of lane B: (i) the f >= 0 restriction of E4, (ii) the precision needed of the gravity coefficient f_g.
Run:    python3 m2_lane_b_sign_and_precision.py
MUTATE: python3 m2_lane_b_sign_and_precision.py MUTATE   (flips sign of b_Y; must exit 1)
Beta functions (Eichhorn-Versteegen form, as used by lane B):  beta_g = -f g + b g^3/(16 pi^2)   [b_Y = +41/6 (screening), b_2 = -19/6, b_3 = -7]
i.e. UNIVERSAL gravity coefficient f multiplies g in every group (gravity is blind to the gauge group at this order).
"""
import sys
import sympy as sp
MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
fails = []
def chk(n, ok, m=""):
    print(("[PASS] " if ok else "[FAIL] ") + n + " " + m)
    if not ok: fails.append(n)
g, f = sp.symbols('g f', real=True)
bY = sp.Rational(41, 6) * (-1 if MUT else 1)
groups = {"U(1)_Y": bY, "SU(2)": -sp.Rational(19, 6), "SU(3)": -sp.Integer(7)}
res = {}
for name, b in groups.items():
    beta = -f * g + b * g**3 / (16 * sp.pi**2)          # gravity term -f g, matter/gauge term +b g^3/(16 pi^2)
    sol = sp.solve(sp.Eq(beta / g, 0), g)               # non-Gaussian roots: g^2 = 16 pi^2 f / b
    for sign_name, fv in (("f>0", sp.Rational(1, 20)), ("f<0", -sp.Rational(1, 20))):
        real_pos = [s for s in [x.subs(f, fv) for x in sol] if s.is_real and s > 0]
        res[(name, sign_name)] = len(real_pos) > 0
        print("  %-7s %s : interacting real fixed point %s %s" % (name, sign_name, "EXISTS" if real_pos else "none", [sp.N(r, 5) for r in real_pos]))
chk("U(1)_Y has an interacting FP only for f>0", res[("U(1)_Y", "f>0")] and not res[("U(1)_Y", "f<0")])
chk("SU(2) has an interacting FP only for f<0", (not res[("SU(2)", "f>0")]) and res[("SU(2)", "f<0")])
chk("SU(3) has an interacting FP only for f<0", (not res[("SU(3)", "f>0")]) and res[("SU(3)", "f<0")])
both = [s for s in ("f>0", "f<0") if res[("U(1)_Y", s)] and res[("SU(2)", s)]]
chk("no sign of a UNIVERSAL f gives interacting FPs for U(1)_Y and SU(2) together", both == [], str(both))
print("  => lane B's restriction f>=0 in E4 excludes only the sign for which U(1)_Y has NO fixed point; it is harmless.")

# (ii) precision: with g_Y(IR) = run of g_Y* = 4 pi sqrt(6 f/41) down with b_Y (one loop), d ln alpha_Y(IR)/d ln f
import mpmath as mp
mp.mp.dps = 25
def gY_IR(fv, L=mp.log(mp.mpf('1.22089e19') / mp.mpf('173'))):
    gs = 4*mp.pi*mp.sqrt(6*fv/41)   # 1/g^2(mu) = 1/g^2(M) + b/(8 pi^2) ln(M/mu)
    return 1/mp.sqrt(1/gs**2 + (mp.mpf(41)/6)/(8*mp.pi**2)*L)
f_pub = mp.mpf('0.04796'); f_req = mp.mpf('0.009805')
for lab, fv in (("published truncation", f_pub), ("required", f_req)):
    h = fv*mp.mpf('1e-6')
    el = (mp.log(gY_IR(fv+h)**2) - mp.log(gY_IR(fv-h)**2)) / (mp.log(fv+h) - mp.log(fv-h))
    print("  %-22s f=%.5f  g_Y(173)=%.4f  d ln alpha_Y/d ln f = %.4f" % (lab, fv, gY_IR(fv), el))
el_req = (mp.log(gY_IR(f_req*(1+mp.mpf('1e-6')))**2) - mp.log(gY_IR(f_req*(1-mp.mpf('1e-6')))**2)) / (2*mp.mpf('1e-6'))
need = mp.mpf('1e-3')/abs(el_req)
print("  to hold alpha_Y(IR) to 1e-3 near the required point, f must be known to %.4f (relative) = %.2f %%" % (need, 100*need))
chk("required precision on f_g (~0.2-0.3 %) is far below the ~tens-of-percent (and sign/zero) truncation & regulator spread reported for f_g", need < 0.01)
chk("published f_g is > 4x the required one (lane B: 4.89)", 4.5 < f_pub/f_req < 5.3, "ratio %.2f" % (f_pub/f_req))
print("  SOURCE NOTE: regulator/gauge dependence of f_g incl. f_g = 0 is quoted by lane B from arXiv:2508.03563 (see source check S1 in the report).")
print("SUMMARY: fails =", fails)
sys.exit(1 if fails else 0)
