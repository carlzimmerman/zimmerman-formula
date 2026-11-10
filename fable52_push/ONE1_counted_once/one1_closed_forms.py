#!/usr/bin/env python3
"""ONE1 closed-form checks at 50 digits (mpmath), each with a twin false statement that must fail. Written at the lead's request
as checks of record beside ONE1.lean. Statements: the end radius x_t^2 = X (X + 1) from nu = 1 + X; continuity of the enclosed
mass at x_t; the far-field ratio 4 (1 + X) / (pi u) of the point mass to the isothermal form (and against the numerically
projected untruncated halo); a thin shell outside R lowers DeltaSigma at R; monotonicity of the enclosed mass in X; and the
shape ratio's monotonicity in X, which holds only up to about X = 300 for the stack (read from one1_kids.json).
    python3 one1_closed_forms.py -> one1_closed_forms.out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, json
import mpmath as mp
mp.mp.dps = 50
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = []; RES = []
def P(s): print(s, flush=True); OUT.append(s)
def m(x): return mp.mpf(1) / 2 + mp.sqrt(mp.mpf(1) / 4 + x * x)
def mt(X, x): return min(m(x), 1 + X)
def check(name, true_fn, twin_fn):
    t = true_fn(); w = twin_fn(); ok = bool(t[0]) and not bool(w[0]); RES.append(ok)
    P(f"{name}: true statement {'holds' if t[0] else 'FAILS'} (worst {mp.nstr(t[1], 5)}); twin {'fails, as it must' if not w[0] else 'HOLDS (the twin does not bite)'} (worst {mp.nstr(w[1], 5)}) -> {'PASS' if ok else 'FAIL'}")
XS = [mp.mpf(v) for v in ("0.5", "5.562", "10.82", "53.64", "59.4861236", "80", "595", "1e4")]
# 1. end radius
def end_true():
    w = max(abs(m(mp.sqrt(X * (X + 1))) - (1 + X)) for X in XS); return w < mp.mpf("1e-45"), w
def end_twin():
    w = min(abs(m(X) - (1 + X)) for X in XS); return w < mp.mpf("1e-45"), w            # x_t = X (that is, x^2 = X^2)
check("end radius: nu = 1 + X at x^2 = X (X + 1)", end_true, end_twin)
# 2. continuity at x_t: the inner mass at x_t - eps and the outer mass 1 + X agree as eps -> 0
def cont_true():
    w = max(abs(mt(X, mp.sqrt(X * (X + 1)) - mp.mpf("1e-40")) - (1 + X)) for X in XS); return w < mp.mpf("1e-35"), w
def cont_twin():
    w = max(abs(mt(X, mp.sqrt(X * (X + 1)) - mp.mpf("1e-40")) - X) for X in XS); return w < mp.mpf("1e-35"), w   # outer mass X
check("continuity of the enclosed mass at x_t", cont_true, cont_twin)
# 3. far-field ratio: [(1 + X) / (pi u^2)] / [1 / (4 u)] = 4 (1 + X) / (pi u); and the untruncated projection tends to 1 / (4 u)
def far_true():
    w = max(abs(((1 + X) / (mp.pi * u * u)) / (1 / (4 * u)) - 4 * (1 + X) / (mp.pi * u)) for X in XS for u in (mp.mpf(100), mp.mpf(2000)))
    return w < mp.mpf("1e-40"), w
def far_twin():
    w = min(abs(((1 + X) / (mp.pi * u * u)) / (1 / (4 * u)) - 2 * (1 + X) / (mp.pi * u)) for X in XS for u in (mp.mpf(100), mp.mpf(2000)))
    return w < mp.mpf("1e-40"), w
check("far-field ratio 4 (1 + X) / (pi u)", far_true, far_twin)
def dsig_inf(u):
    """untruncated halo, DeltaSigma in M_b / r_M^2 (cosh substitution, 50 digits)."""
    f_dm = lambda t: (u * mp.cosh(t)) / mp.sqrt(mp.mpf(1) / 4 + (u * mp.cosh(t)) ** 2)
    Sig = mp.quad(lambda t: f_dm(t) / mp.cosh(t), [0, 5, 20, 60]) / (2 * mp.pi * u)
    Mc = m(u) + u * mp.quad(lambda t: f_dm(t) * mp.tanh(t) * mp.exp(-t), [0, 5, 20, 60])
    return Mc / (mp.pi * u * u) - Sig
def iso_true():
    w = max(abs(dsig_inf(u) * 4 * u - 1) for u in (mp.mpf(300), mp.mpf(2000))); return w < mp.mpf("3e-3"), w
def iso_twin():
    w = min(abs(dsig_inf(u) * 2 * u - 1) for u in (mp.mpf(300), mp.mpf(2000))); return w < mp.mpf("3e-3"), w   # the 1 / (2u) form
check("the untruncated halo's DeltaSigma tends to the isothermal 1 / (4 u)", iso_true, iso_twin)
# 4. a thin shell at s > R lowers DeltaSigma at R: (1 - c) / (1 - c^2) - 1 / (2 c) < 0 for 0 < c < 1
CS = [mp.mpf(k) / 1000 for k in range(1, 1000)]
def shell_true():
    w = max((1 - c) / (1 - c * c) - 1 / (2 * c) for c in CS); return w < 0, w
def shell_twin():
    w = min((1 - c) / (1 - c * c) - 1 / (2 * c) for c in CS); return w > 0, w
check("a thin shell outside R lowers DeltaSigma at R", shell_true, shell_twin)
# 5. the enclosed mass is monotone in X and the inner part (x <= x_t) does not depend on X
def mono_true():
    xs = [mp.mpf(v) for v in ("0.1", "1", "10", "50", "60", "100", "1000")]; worst = mp.mpf(0)
    for a, b in zip(XS[:-1], XS[1:]):
        for x in xs:
            worst = min(worst, mt(b, x) - mt(a, x))
            if x <= mp.sqrt(a * (a + 1)): worst = min(worst, -abs(mt(a, x) - m(x)))
    return worst >= 0, worst
def mono_twin():
    xs = [mp.mpf(v) for v in ("0.1", "1", "10", "50", "60", "100", "1000")]; worst = mp.mpf(0)
    for a, b in zip(XS[:-1], XS[1:]):
        for x in xs: worst = min(worst, mt(a, x) - mt(b, x))                         # claims the mass falls as X grows
    return worst >= 0, worst
check("the enclosed mass rises with X; inside x_t it is the law's", mono_true, mono_twin)
# 6. the shape ratio of the stack against X (from one1_kids.json, canonical, all, 1.6 R_h, k = 1, no neighbours)
mono = json.load(open(os.path.join(HERE, "one1_kids.json")))["monotonicity_k1"]
Xv = [r[0] for r in mono]; Rs = [r[3] for r in mono]
upto = [i for i in range(len(Xv) - 1) if Xv[i + 1] <= 300]
ok_low = all(Rs[i + 1] >= Rs[i] for i in upto); ok_all = all(Rs[i + 1] >= Rs[i] for i in range(len(Xv) - 1))
RES.append(ok_low and not ok_all)
P(f"shape ratio of the stack against X (k = 1, canonical, all, 1.6 R_h): " + ", ".join(f"{x:g}: {r:.3f}" for x, r in zip(Xv, Rs)))
P(f"   non-decreasing for X up to 300: {ok_low}; non-decreasing over the whole range (the twin statement): {ok_all} -> "
  f"{'PASS: monotone on X <= 300, not globally (it peaks near X = 300 and falls back to the law)' if (ok_low and not ok_all) else 'FAIL'}")
P(f"\nall checks: {sum(RES)} of {len(RES)} PASS")
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
open(os.path.join(HERE, "one1_closed_forms.out"), "w").write("\n".join(OUT) + "\n")
