#!/usr/bin/env python3
"""LR10X v2 -- zero-recognition exact confirmation of the E2F1 closed forms (Z17 door; owns LR10X_*).

Pre-registration: Z17-WAVE_BRIEF.md (09297b484) + AMENDMENTS 1-3, all committed BEFORE
the adjudicating run. Run history: run-1 KeyError g3 fire; run-2 regex fire; run-3 dead
line fire; run-4 KILL at channel b (all preserved verbatim in LR10X_stdout_0.txt);
LR10X_diag localized the kill: tot_b = 701/1050 EXACT, E2F1's zeta(3)-form_b a lattice
misfire (+3.566e-13 inside nsimplify tol 1e-11); parity structure => a, b, c all rational.

THIS run (run-5) adjudicates per AMENDMENT 3 gates G-T1..G-T5, per channel:
  G-T1 every term integral vs independent mpmath quad (dps 40, subdivided): rel <= 1e-25
  G-T2 sum of term quads vs exact tot: rel <= 1e-30
  G-T3 free_symbols == {r}; <= 1 log factor per term; log(1+r) only at ODD r-powers
  G-T4 fresh S1 pipeline (rule-doubling <= 1e-11) vs tot: rel <= 1e-13; parsed-log G3 vs tot <= 2e-12
  G-T5 tot == form syntactic zero -> E2F1 form CONFIRMED-EXACT;
       mismatch -> E2F1 form KILLED, replaced by exact tot (must be pure rational)
Verdicts: CONFIRMED-EXACT / KILLED-REFORMED only; register corrected by APPENDED rows.
"""
import json, os, sys, time, math, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "LR10X_exact_check.out")
RESF = os.path.join(HERE, "LR10X_results.json")
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time()-_T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="LR10X: zero-recognition exact confirmation of the E2F1 closed forms (Z17 door)",
               pre_registration="Z17-WAVE_BRIEF.md 09297b484 + AMENDMENTS 1-3 (before any run)",
               verdict=verdict, exit=rc, elapsed_s=round(time.time()-_T0,1), log=LOG)
    if extra: RES.update(extra)
    json.dump(RES, open(RESF, "w"), indent=1, default=str)
    with open(OUT, "a") as f: f.write("\n".join(LOG) + "\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

log("loading E2F1_results.json (loaded-not-transcribed)")
E = json.load(open(os.path.join(HERE, "E2F1_results.json")))
assert E.get("exit") == 0 and E["symbolic"]["status"] == "CLOSED", "E2F1 source state invalid"
FORMS = {k: E["symbolic"][k] for k in "abc"}
NUMP = {}
for line in E["log"]:
    m = re.search(r"G3: ([abc]): symbolic ([0-9.]+) vs numeric ([0-9.]+) rel", line)
    if m: NUMP[m.group(1)] = float(m.group(3))
assert set(NUMP) == set("abc"), "G3 numeric values not found in E2F1 log"
log("forms: a=%s | b=%s | c=%s" % (FORMS["a"], FORMS["b"], FORMS["c"]))

import sympy as sp
rr = sp.symbols("r", positive=True); cu = sp.symbols("cu", positive=True)
vv = sp.symbols("v", real=True); uuS = sp.symbols("u", real=True)
qs = sp.Symbol("q", positive=True); wwS = sp.symbols("w", real=True)

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
    return sp.simplify(sp.cancel(res.subs(cu, sp.sqrt(1-rr**2))))
MO = {}
for (j, n) in [(0,1),(0,2),(0,3),(0,4),(1,2),(1,3)]:
    for p2w, tg in ((False,'I'), (True,'Q')):
        MO[(j,n,tg)] = inner_moment_sym(j, n, p2w)
        log("S4: moment (j=%d,n=%d,%s) closed" % (j, n, tg))
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
        JT[(k,tg)] = sp.simplify(sp.cancel(res.subs(cu, sp.sqrt(1-rr**2))))
        log("S4: J(k=%d,Q=%d) closed" % (k, tg))
m1, m1q = MO[(0,1,'I')], MO[(0,1,'Q')]
m2, m2q = MO[(0,2,'I')], MO[(0,2,'Q')]
m3  = rr**2*MO[(0,1,'I')] + rr*MO[(1,2,'I')] + MO[(0,3,'I')]/3
m3q = rr**2*MO[(0,1,'Q')] + rr*MO[(1,2,'Q')] + MO[(0,3,'Q')]/3
m4  = rr**2*MO[(0,2,'I')]/2 + sp.Rational(2,3)*rr*MO[(1,3,'I')] + MO[(0,4,'I')]/4
m4q = rr**2*MO[(0,2,'Q')]/2 + sp.Rational(2,3)*rr*MO[(1,3,'Q')] + MO[(0,4,'Q')]/4
J10, J11, J20, J21 = JT[(1,0)], JT[(1,1)], JT[(2,0)], JT[(2,1)]
Fa = (m1*J20 + m1q*J21/2)/2 + (m2*J10 + m2q*J11/2)/2
Fb = (m3*J20 + m3q*J21/2)/2 + m4*J10 + m4q*J11/2

# ============ S1 verbatim (E2F1): fresh numeric pipeline for G-T4 ============
from numpy.polynomial.legendre import leggauss
UMAX = 30.0
def num_coeffs(Nu=90, Nv=70, Nw=70):
    xg, wg = leggauss(Nu); us = 0.5*(xg+1)*UMAX; wu = 0.5*wg*UMAX
    vg, wvg = leggauss(Nv); wg_, wwg = leggauss(Nw)
    pairs = [(0,1),(0,2),(0,3),(0,4),(1,2),(1,3)]
    Fa_all = np.zeros(Nu); Fb_all = np.zeros(Nu)
    for i, uu in enumerate(us):
        r = math.tanh(uu); c = 1.0/math.cosh(uu)
        V = uu*vg; WV = uu*wvg
        sh = np.sinh(V); en = np.exp(-V)
        mI = {}; mQ = {}
        for (j, n) in pairs:
            base = (c*sh)**j * (c*en)**n * (c*np.cosh(V))
            mI[(j,n)] = np.sum(WV*base)/(2.0*r**(j+1))
            mQ[(j,n)] = np.sum(WV*base*(1.5*(c*sh/r)**2 - 0.5))/(2.0*r**(j+1))
        W = uu*wg_; wW = uu*wwg
        ew = np.exp(W); shw = np.sinh(W); chw = np.cosh(W)
        J = {}
        for k in (1, 2):
            baseJ = (c*ew)**k * (c/r)*chw
            J[(k,0)] = np.sum(wW*baseJ)
            J[(k,1)] = np.sum(wW*baseJ*(1.5*(c*shw/r)**2 - 0.5))
        mm1, mm1q = mI[(0,1)], mQ[(0,1)]
        mm2, mm2q = mI[(0,2)], mQ[(0,2)]
        mm3  = r*r*mI[(0,1)] + r*mI[(1,2)] + mI[(0,3)]/3.0
        mm3q = r*r*mQ[(0,1)] + r*mQ[(1,2)] + mQ[(0,3)]/3.0
        mm4  = r*r*mI[(0,2)]/2.0 + (2.0/3.0)*r*mI[(1,3)] + mI[(0,4)]/4.0
        mm4q = r*r*mQ[(0,2)]/2.0 + (2.0/3.0)*r*mQ[(1,3)] + mQ[(0,4)]/4.0
        Fa_all[i] = 0.5*(mm1*J[(2,0)] + 0.5*mm1q*J[(2,1)]) + 0.5*(mm2*J[(1,0)] + 0.5*mm2q*J[(1,1)])
        Fb_all[i] = 0.5*(mm3*J[(2,0)] + 0.5*mm3q*J[(2,1)]) + mm4*J[(1,0)] + 0.5*mm4q*J[(1,1)]
    r2 = np.tanh(us)**2; sech2 = 1.0/np.cosh(us)**2
    return np.array([1.5*np.sum(wu*r2*sech2*Fa_all),
                     1.5*np.sum(wu*r2*sech2*(r2*Fa_all + Fb_all)),
                     1.5*np.sum(wu*r2*sech2*r2*Fb_all)])
abc1 = num_coeffs(90, 70, 70); abc2 = num_coeffs(140, 110, 110)
rule_dev = float(np.max(np.abs(abc1-abc2)/np.abs(abc2)))
log("S1-fresh: GL(90,70,70) = %s | GL(140,110,110) = %s | rule-doubling %.2e" % (tuple(abc1), tuple(abc2), rule_dev))
if rule_dev > 1e-11:
    finish(1, "S1-fresh FIRED: rule-doubling %.2e > 1e-11" % rule_dev)

# ============ per-channel exact adjudication (G-T1..G-T5) ============
import mpmath as mp
mp.mp.dps = 40
QUAD_PTS = [0, mp.mpf('0.5'), mp.mpf('0.9'), mp.mpf('0.99'), mp.mpf('0.9999'), 1]
def term_num(term):
    f = sp.lambdify(rr, term, modules='mpmath')
    return mp.quad(lambda x: mp.mpf(f(x)), QUAD_PTS)

INTEG = {"a": sp.expand(rr**2*Fa)*sp.Rational(3,2),
         "b": sp.expand(rr**2*(rr**2*Fa + Fb))*sp.Rational(3,2),
         "c": sp.expand(rr**4*Fb)*sp.Rational(3,2)}
results = {}
for k_ in "abc":
    log("== channel %s ==" % k_)
    e = sp.expand(sp.expand_log(INTEG[k_].rewrite(sp.log), force=True))
    e = e.subs(sp.log(1-rr**2), sp.log(1-rr)+sp.log(1+rr))
    terms = sp.Add.make_args(sp.expand(e))
    log("channel %s: %d integrand terms" % (k_, len(terms)))
    r = {"n_terms": len(terms), "terms": []}
    tot = sp.Integer(0); quad_sum = mp.mpf(0)
    for i, term in enumerate(terms):
        # G-T3 audits (syntactic)
        assert term.free_symbols <= {rr}, "G-T3: stray symbol in term %d: %s" % (i, term.free_symbols)
        logs = [f for f in sp.Mul.make_args(term) if f.func == sp.log]
        assert len(logs) <= 1, "G-T3: multiple log factors in term %d: %s" % (i, term)
        if logs:
            arg = logs[0].args[0]
            assert arg in (1-rr, 1+rr), "G-T3: unexpected log arg %s in term %d" % (arg, i)
            if arg == 1+rr:
                pf = [f for f in sp.Mul.make_args(term) if f.is_Pow and f.base == rr]
                pexp = int(pf[0].exp) if pf else 0
                assert pexp % 2 == 1, "G-T3 PARITY: log(1+r) at even r-power %d in term %d: %s" % (pexp, i, term)
        # G-T1: term integral vs independent quad
        iv = sp.simplify(sp.integrate(term, (rr, 0, 1)))
        nv = term_num(term)
        sv = mp.mpf(str(sp.N(iv, 35)))
        rel = abs(sv - nv)/abs(nv) if nv != 0 else abs(sv - nv)
        if rel > mp.mpf("1e-25"):
            finish(1, "G-T1 FIRED: channel %s term %d (rel %.3e): %s" % (k_, i, float(rel), sp.sstr(term)[:200]), dict(results=results))
        quad_sum += nv
        tot += iv
        r["terms"].append(dict(i=i, integrand=sp.sstr(term)[:200], integral=sp.sstr(iv)[:120],
                               quad_rel=float(rel)))
    log("channel %s: G-T1 PASS (all terms)" % k_)
    # G-T2
    tot_val = mp.mpf(str(sp.N(tot, 45)))
    rel_t2 = abs(quad_sum - tot_val)/abs(tot_val)
    if rel_t2 > mp.mpf("1e-30"):
        finish(1, "G-T2 FIRED: channel %s (rel %.3e)" % (k_, float(rel_t2)), dict(results=results))
    r["gt2_rel"] = float(rel_t2)
    # G-T4
    i_ = "abc".index(k_)
    num_fresh = mp.mpf(repr(float(abc2[i_])))
    rel_t4a = abs(tot_val - num_fresh)/abs(num_fresh)
    num_ref = mp.mpf(repr(NUMP[k_]))
    rel_t4b = abs(tot_val - num_ref)/abs(num_ref)
    r["gt4"] = dict(rel_fresh=float(rel_t4a), rel_parsed=float(rel_t4b))
    if rel_t4a > mp.mpf("1e-13"):
        finish(1, "G-T4a FIRED: channel %s (fresh pipeline rel %.3e > 1e-13)" % (k_, float(rel_t4a)), dict(results=results))
    if rel_t4b > mp.mpf("2e-12"):
        finish(1, "G-T4b FIRED: channel %s (parsed G3 rel %.3e > 2e-12)" % (k_, float(rel_t4b)), dict(results=results))
    log("channel %s: G-T2 rel %.2e | G-T4a rel %.2e | G-T4b rel %.2e" % (k_, rel_t2, rel_t4a, rel_t4b))
    # G-T5: exact test vs E2F1's form
    form = sp.sympify(FORMS[k_])
    d = sp.cancel(sp.expand(sp.simplify(sp.expand(tot - form))))
    if d == 0:
        r["gt5"] = "CONFIRMED-EXACT (syntactic zero: tot == E2F1 form)"
        r["form_status"] = "CONFIRMED-EXACT"
    else:
        assert tot.is_Rational, "channel %s exact tot NOT pure rational: %s" % (k_, sp.sstr(tot)[:300])
        r["gt5"] = "KILLED-REFORMED: E2F1 form off by %s; exact tot = %s" % (sp.sstr(sp.N(tot - form, 10)), sp.sstr(tot))
        r["form_status"] = "KILLED-REFORMED"
        r["exact_value"] = sp.sstr(tot)
        r["form_minus_tot"] = sp.sstr(sp.N(form - tot, 30))
        log("channel %s: G-T5 MISMATCH: N(form - tot, 30) = %s ; exact tot = %s (pure rational)" % (k_, sp.N(form - tot, 30), tot))
    results[k_] = r
    log("channel %s: %s" % (k_, r["gt5"]))

n_conf = sum(1 for k_ in "abc" if results[k_]["form_status"] == "CONFIRMED-EXACT")
n_kill = 3 - n_conf
reformed = {k_: results[k_].get("exact_value") for k_ in "abc" if results[k_]["form_status"] == "KILLED-REFORMED"}
verdict = ("BANKED: E2F1 closed forms adjudicated exactly (zero recognition): %d CONFIRMED-EXACT, %d KILLED-REFORMED. %s" %
           (n_conf, n_kill, "; ".join("%s: %s%s" % (k_, results[k_]["form_status"],
                    (" -> " + results[k_]["exact_value"]) if k_ in reformed else "") for k_ in "abc")))
finish(0, verdict, dict(results=results, forms=FORMS, rule_doubling=rule_dev, num_fresh=[float(x) for x in abc2]))
