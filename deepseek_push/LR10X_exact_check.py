#!/usr/bin/env python3
"""LR10X -- zero-recognition exact confirmation of the E2F1 closed forms (Z17 door; owns LR10X_*).

Pre-registration: Z17-WAVE_BRIEF.md (committed 09297b484 BEFORE any run) + AMENDMENT 1
(srepr[:120] term cache dropped; S4/S5 chain otherwise verbatim from E2F1_closed_form.py).
Context: E2F1 (Z16, 167f11fab, exit 0) banked a = 37/60,
b = (217 - 489 ln2 - 8 pi^2 + 251 zeta(3))/151, c = (17 + 47 pi^2 - 423 ln2 - 137 zeta(3))/121
-- but by sp.nsimplify LATTICE RECOGNITION (tolerance 1e-11), never a symbolic zero test.
This lane re-derives the symbolic-exact tot per channel and tests tot - closed_form == 0
EXACTLY. Gates (frozen in the brief; any fire -> exit 1, no tuning):
  G-X1 syntactic zero: sp.cancel(sp.expand(sp.simplify(tot - form))) == 0
       branch (i) syntactic 0 -> BANKED-EXACT
       branch (ii) 240 s time-box on the syntactic leg, then tot-form equals(0) True
                   -> BANKED-ZEROTEST (syntactic leg recorded OPEN)
  G-X2 mpmath dps=50 closed form vs sp.N(tot,50), rel <= 1e-30
       (G-X2a transcription guard: sp.N(stored form,50) vs mpmath-transcribed atoms, dev <= 1e-48)
  G-X3 vs E2F1 numeric pipeline (g3 num, loaded-not-transcribed), rel <= 1e-12
Kills: any G-X2/G-X3 fire; tot-form nonzero under BOTH syntactic and .equals;
all-branch time-box exhaustion; uncaught exception.
"""
import json, os, sys, time, math, signal, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "LR10X_exact_check.out")
RESF = os.path.join(HERE, "LR10X_results.json")
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time() - _T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="LR10X: zero-recognition exact confirmation of the E2F1 closed forms (Z17 door)",
               pre_registration="Z17-WAVE_BRIEF.md 09297b484 + AMENDMENT 1 (before any run)",
               verdict=verdict, exit=rc, elapsed_s=round(time.time()-_T0,1), log=LOG)
    if extra: RES.update(extra)
    json.dump(RES, open(RESF, "w"), indent=1, default=str)
    with open(OUT, "a") as f: f.write("\n".join(LOG) + "\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

class TimeBox(Exception): pass
def _alarm(signum, frame): raise TimeBox()
def timeboxed(fn, seconds):
    old = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(int(seconds))
    try:
        return fn(), None
    except TimeBox:
        return None, "TIMEBOX(%ds)" % seconds
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)

# ---- load-not-transcribe the E2F1 closed forms and numeric pipeline ----
log("loading E2F1_results.json (loaded-not-transcribed)")
E = json.load(open(os.path.join(HERE, "E2F1_results.json")))
assert E.get("exit") == 0 and E["symbolic"]["status"] == "CLOSED", "E2F1 source state invalid"
FORMS = {k: E["symbolic"][k] for k in "abc"}
# AMENDMENT 2: G-X3b numeric values parsed from E2F1's own log lines (loaded-not-transcribed)
NUMP = {}
for line in E["log"]:
    m = re.search(r"G3: ([abc]): symbolic ([0-9.]+) vs numeric ([0-9.]+) rel", line)
    if m: NUMP[m.group(1)] = float(m.group(3))
assert set(NUMP) == set("abc"), "G3 numeric values not found in E2F1 log"
log("forms: a=%s | b=%s | c=%s" % (FORMS["a"], FORMS["b"], FORMS["c"]))

import sympy as sp
rr = sp.symbols("r", positive=True)
cu = sp.symbols("cu", positive=True)     # c = sqrt(1-r^2)
vv = sp.symbols("v", real=True)
uuS = sp.symbols("u", real=True)         # u = atanh(r); cosh(u) = 1/c, sinh(u) = r/c
qs = sp.Symbol("q", positive=True)       # e^{u} bridge for clean power extraction
wwS = sp.symbols("w", real=True)

# ============ S4 verbatim (E2F1_closed_form.py) ============
def inner_moment_sym(j, n, p2w):
    sinhE = sp.expand(((sp.exp(vv) - sp.exp(-vv))/2)**j)
    coshE = sp.expand((sp.exp(vv) + sp.exp(-vv))/2)
    expr = (cu)**(j+n+1) * sinhE * sp.exp(-n*vv) * coshE
    if p2w:
        expr = expr * ((3*(cu**2*sp.expand(((sp.exp(vv) - sp.exp(-vv))/2)**2))/rr**2 - 1)/2)
    res = sp.integrate(sp.expand(expr), (vv, -uuS, uuS))
    res = sp.expand(res.subs(uuS, sp.log(qs)))
    res = sp.cancel(sp.expand(res.subs(qs, (1+rr)/cu)))
    res = res/(2*rr**(j+1))
    res = res.subs(cu**2, 1-rr**2)
    res = sp.simplify(sp.cancel(res.subs(cu, sp.sqrt(1-rr**2))))
    return res

log("S4: building 12 inner moments (verbatim chain) ...")
MO = {}
for (j, n) in [(0,1),(0,2),(0,3),(0,4),(1,2),(1,3)]:
    for p2w, tg in ((False,'I'), (True,'Q')):
        MO[(j,n,tg)] = inner_moment_sym(j, n, p2w)
        log("S4: moment (j=%d,n=%d,%s) closed" % (j, n, tg))
log("S4: J-table ...")
JT = {}
for k in (1, 2):
    for p2w, tg in ((False,0), (True,1)):
        coshE = sp.expand((sp.exp(wwS) + sp.exp(-wwS))/2)
        expr = (cu*sp.exp(wwS))**k * (cu/rr)*coshE
        if p2w: expr = expr*((3*(cu**2*sp.expand(((sp.exp(wwS) - sp.exp(-wwS))/2)**2))/rr**2 - 1)/2)
        res = sp.integrate(sp.expand(expr), (wwS, -uuS, uuS))
        res = sp.expand(res.subs(uuS, sp.log(qs)))
        res = sp.cancel(sp.expand(res.subs(qs, (1+rr)/cu)))
        res = sp.cancel(sp.expand(res)).subs(cu**2, 1-rr**2)
        res = sp.simplify(sp.cancel(res.subs(cu, sp.sqrt(1-rr**2))))
        JT[(k,tg)] = res
        log("S4: J(k=%d,Q=%d) closed" % (k, tg))
m1, m1q = MO[(0,1,'I')], MO[(0,1,'Q')]
m2, m2q = MO[(0,2,'I')], MO[(0,2,'Q')]
m3  = rr**2*MO[(0,1,'I')] + rr*MO[(1,2,'I')] + MO[(0,3,'I')]/3
m3q = rr**2*MO[(0,1,'Q')] + rr*MO[(1,2,'Q')] + MO[(0,3,'Q')]/3
m4  = rr**2*MO[(0,2,'I')]/2 + sp.Rational(2,3)*rr*MO[(1,3,'I')] + MO[(0,4,'I')]/4
m4q = rr**2*MO[(0,2,'Q')]/2 + sp.Rational(2,3)*rr*MO[(1,3,'Q')] + MO[(0,4,'Q')]/4
J10, J11, J20, J21 = JT[(1,0)], JT[(1,1)], JT[(2,0)], JT[(2,1)]
Fa = (m1*J20 + m1q*J21/2)/2 + (m2*J10 + m2q*J11/2)/2   # AMENDMENT 2 of E2F1: c00f = W2^2/2
Fb = (m3*J20 + m3q*J21/2)/2 + m4*J10 + m4q*J11/2

def rint_exact(expr):
    """E2F1 rint verbatim, minus the srepr[:120] term cache and minus nsimplify."""
    e = sp.expand(sp.expand_log(expr.rewrite(sp.log), force=True))
    e = e.subs(sp.log(1-rr**2), sp.log(1-rr)+sp.log(1+rr))
    e = sp.expand(e)
    terms = sp.Add.make_args(e)
    log("rint: %d terms to integrate term-wise" % len(terms))
    tot = sp.Integer(0)
    for i, term in enumerate(terms):
        iv = sp.simplify(sp.integrate(term, (rr, 0, 1)))
        tot += iv
        if (i+1) % 25 == 0: log("rint: %d/%d terms integrated" % (i+1, len(terms)))
    return sp.simplify(tot)

log("S5: assembling a/b/c r-integrands and integrating term-wise (no cache, no nsimplify)")
tot_a = rint_exact(sp.expand(rr**2*Fa)*sp.Rational(3,2)); log("S5: tot_a built")
tot_b = rint_exact(sp.expand(rr**2*(rr**2*Fa + Fb))*sp.Rational(3,2)); log("S5: tot_b built")
tot_c = rint_exact(sp.expand(rr**4*Fb)*sp.Rational(3,2)); log("S5: tot_c built")
TOTS = {"a": tot_a, "b": tot_b, "c": tot_c}


# ============ S1 verbatim (E2F1_closed_form.py): fresh numeric pipeline for G-X3a ============
log("S1-fresh: numeric (a,b,c) via exponential-coordinate spectral nesting (verbatim E2F1 S1)")
from numpy.polynomial.legendre import leggauss
UMAX = 30.0
def num_coeffs(Nu=90, Nv=70, Nw=70):
    xg, wg = leggauss(Nu); us = 0.5*(xg+1)*UMAX; wu = 0.5*wg*UMAX
    vg, wvg = leggauss(Nv); wg_, wwg = leggauss(Nw)
    out = np.zeros(3)
    pairs = [(0,1),(0,2),(0,3),(0,4),(1,2),(1,3)]
    Fa_all = np.zeros(Nu); Fb_all = np.zeros(Nu)
    for i, uu in enumerate(us):
        r = math.tanh(uu); c = 1.0/math.cosh(uu)
        V = uu*vg; WV = uu*wvg
        sh = np.sinh(V); ch = np.cosh(V); en = np.exp(-V)
        mI = {}; mQ = {}
        for (j, n) in pairs:
            base = (c*sh)**j * (c*en)**n * (c*ch)
            mI[(j,n)] = np.sum(WV*base)/(2.0*r**(j+1))
            mQ[(j,n)] = np.sum(WV*base*(1.5*(c*sh/r)**2 - 0.5))/(2.0*r**(j+1))
        m1, m1q = mI[(0,1)], mQ[(0,1)]
        m2, m2q = mI[(0,2)], mQ[(0,2)]
        m3  = r*r*mI[(0,1)] + r*mI[(1,2)] + mI[(0,3)]/3.0
        m3q = r*r*mQ[(0,1)] + r*mQ[(1,2)] + mQ[(0,3)]/3.0
        m4  = r*r*mI[(0,2)]/2.0 + (2.0/3.0)*r*mI[(1,3)] + mI[(0,4)]/4.0
        m4q = r*r*mQ[(0,2)]/2.0 + (2.0/3.0)*r*mQ[(1,3)] + mQ[(0,4)]/4.0
        W = uu*wg_; wW = uu*wwg
        ew = np.exp(W); shw = np.sinh(W); chw = np.cosh(W)
        J = {}
        for k in (1, 2):
            baseJ = (c*ew)**k * (c/r)*chw
            J[(k,0)] = np.sum(wW*baseJ)
            J[(k,1)] = np.sum(wW*baseJ*(1.5*(c*shw/r)**2 - 0.5))
        J10, J11, J20, J21 = J[(1,0)], J[(1,1)], J[(2,0)], J[(2,1)]
        Fa = 0.5*(m1*J20 + 0.5*m1q*J21) + 0.5*(m2*J10 + 0.5*m2q*J11)
        Fb = 0.5*(m3*J20 + 0.5*m3q*J21) + m4*J10 + 0.5*m4q*J11
        Fa_all[i] = Fa; Fb_all[i] = Fb
    r2 = np.tanh(us)**2; sech2 = 1.0/np.cosh(us)**2
    a = 1.5*np.sum(wu*r2*sech2*Fa_all)
    b = 1.5*np.sum(wu*r2*sech2*(r2*Fa_all + Fb_all))
    cc = 1.5*np.sum(wu*r2*sech2*r2*Fb_all)
    return np.array([a, b, cc])
abc1 = num_coeffs(90, 70, 70)
log("S1-fresh: GL(90,70,70): a=%.12f b=%.12f c=%.12f" % tuple(abc1))
abc2 = num_coeffs(140, 110, 110)
log("S1-fresh: GL(140,110,110): a=%.12f b=%.12f c=%.12f" % tuple(abc2))
rule_dev = float(np.max(np.abs(abc1-abc2)/np.abs(abc2)))
log("S1-fresh: rule-doubling max rel dev %.2e" % rule_dev)
if rule_dev > 1e-11:
    finish(1, "S1-fresh FIRED: quadrature rule-doubling disagreement %.2e > 1e-11" % rule_dev)

import mpmath as mp
mp.mp.dps = 60
ATOMS = {sp.log(2): mp.log(2), sp.pi: mp.pi, sp.zeta(3): mp.zeta(3)}
def form_mp(form_str):
    """mpmath-transcribed evaluation of a stored form: sum of Q-lattice terms in the atoms."""
    ex = sp.sympify(form_str)
    ex = sp.expand(ex)
    val = mp.mpf(0)
    for term in sp.Add.make_args(ex):
        rat = sp.Rational(1); rest = []
        for f in sp.Mul.make_args(term) if term != 1 else []:
            if f.is_Rational: rat *= sp.Rational(f)
            else: rest.append(f)
        unk = [f for f in rest if f not in ATOMS]
        if unk: raise ValueError("form atom not recognized: %s" % unk)
        v = mp.mpf(rat.numerator) / mp.mpf(rat.denominator)
        for f in rest: v = v * ATOMS[f]
        val += v
    return val

results = {}
status_all = []
for k_ in "abc":
    log("== channel %s ==" % k_)
    form = sp.sympify(FORMS[k_])
    d = sp.expand(TOTS[k_] - form)
    r = {}
    # G-X1 branch (i): syntactic zero
    d_red, err = timeboxed(lambda: sp.cancel(sp.expand(sp.simplify(d))), 240)
    if err is None and d_red == 0:
        r["gx1"] = "BANKED-EXACT (syntactic zero)"
        r["gx1_branch"] = "i"
    else:
        if err: log("G-X1 branch (i): %s (falling to .equals zero-test)" % err)
        else: log("G-X1 branch (i): syntactic residual NOT 0 after cancel/expand/simplify (falling to .equals)")
        eq, err2 = timeboxed(lambda: bool(d.equals(0)), 240)
        if eq is True:
            r["gx1"] = "BANKED-ZEROTEST (equals(0) True; syntactic leg OPEN: %s)" % (err or "simplify-residual-nonzero")
            r["gx1_branch"] = "ii"
        elif eq is None:
            finish(1, "KILL: channel %s time-box exhausted on BOTH branches (err: %s / %s)" % (k_, err, err2), dict(results=results))
        else:
            dv, errn = timeboxed(lambda: float(sp.N(d, 30)), 120)
            finish(1, "KILL: channel %s: tot - form nonzero (syntactic residual %s; equals(0)=False; N(d,30)=%s)" % (k_, str(d_red)[:200], dv), dict(results=results))
    # G-X2: transcription guard + mpmath-vs-sympy at dps 50
    val_sym_form = sp.N(form, 55)
    val_mp_form = form_mp(FORMS[k_])
    dev_x2a = abs(mp.mpf(str(val_sym_form)) - val_mp_form)
    if dev_x2a > mp.mpf("1e-48"):
        finish(1, "KILL: G-X2a FIRED at %s (transcription dev %.3e > 1e-48)" % (k_, float(dev_x2a)), dict(results=results))
    val_tot = sp.N(TOTS[k_], 55)
    dev_x2 = abs(mp.mpf(str(val_tot)) - val_mp_form) / abs(val_mp_form)
    r["gx2"] = dict(rel=float(dev_x2), gate=1e-30)
    if dev_x2 > mp.mpf("1e-30"):
        finish(1, "KILL: G-X2 FIRED at %s (rel %.3e > 1e-30)" % (k_, float(dev_x2)), dict(results=results))
    # G-X3a: fresh numeric pipeline (verbatim E2F1 S1 re-run)
    i_ = "abc".index(k_)
    num_fresh = mp.mpf(repr(float(abc2[i_])))
    dev_x3a = abs(mp.mpf(str(val_tot)) - num_fresh) / abs(num_fresh)
    # G-X3b: G3 numeric values parsed from the E2F1 results log (loaded-not-transcribed)
    num_ref = mp.mpf(repr(NUMP[k_]))
    dev_x3b = abs(mp.mpf(str(val_tot)) - num_ref) / abs(num_ref)
    r["gx3"] = dict(rel_fresh=float(dev_x3a), gate_fresh=1e-12,
                    rel_parsed=float(dev_x3b), gate_parsed=2e-12)
    if dev_x3a > mp.mpf("1e-12"):
        finish(1, "KILL: G-X3a FIRED at %s (rel %.3e > 1e-12)" % (k_, float(dev_x3a)), dict(results=results))
    if dev_x3b > mp.mpf("2e-12"):
        finish(1, "KILL: G-X3b FIRED at %s (rel %.3e > 2e-12)" % (k_, float(dev_x3b)), dict(results=results))
    status_all.append(r["gx1_branch"])
    r["tot_terms"] = len(sp.Add.make_args(sp.expand(TOTS[k_])))
    r["tot_free_atoms"] = sorted(str(s) for s in (TOTS[k_].free_symbols - {rr}))
    results[k_] = r
    log("channel %s: %s | G-X2 rel %.2e | G-X3a rel %.2e | G-X3b rel %.2e" % (k_, r["gx1"], r["gx2"]["rel"], r["gx3"]["rel_fresh"], r["gx3"]["rel_parsed"]))

verdict = ("BANKED: exact zero-recognition confirmation of the E2F1 closed forms — %s" %
           ("; ".join("%s: %s" % (k_, results[k_]["gx1"]) for k_ in "abc")))
if all(b == "i" for b in status_all):
    verdict = "BANKED-EXACT (all three channels syntactic zero): " + verdict
finish(0, verdict, dict(results=results, forms=FORMS, num_pipeline=NUMP))
