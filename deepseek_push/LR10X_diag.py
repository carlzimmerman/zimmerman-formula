#!/usr/bin/env python3
"""LR10X_diag -- localize the channel-b exactness failure (conductor diagnosis, Z17)."""
import json, os, sys, time, math
HERE = os.path.dirname(os.path.abspath(__file__))
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time()-_T0, m); LOG.append(line); print(line, flush=True)

E = json.load(open(os.path.join(HERE, "E2F1_results.json")))
FORMS = {k: E["symbolic"][k] for k in "abc"}

import sympy as sp
rr = sp.symbols("r", positive=True); cu = sp.symbols("cu", positive=True)
vv = sp.symbols("v", real=True); uuS = sp.symbols("u", real=True)
qs = sp.Symbol("q", positive=True); wwS = sp.symbols("w", real=True)

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
m1, m1q = MO[(0,1,'I')], MO[(0,1,'Q')]
m2, m2q = MO[(0,2,'I')], MO[(0,2,'Q')]
m3  = rr**2*MO[(0,1,'I')] + rr*MO[(1,2,'I')] + MO[(0,3,'I')]/3
m3q = rr**2*MO[(0,1,'Q')] + rr*MO[(1,2,'Q')] + MO[(0,3,'Q')]/3
m4  = rr**2*MO[(0,2,'I')]/2 + sp.Rational(2,3)*rr*MO[(1,3,'I')] + MO[(0,4,'I')]/4
m4q = rr**2*MO[(0,2,'Q')]/2 + sp.Rational(2,3)*rr*MO[(1,3,'Q')] + MO[(0,4,'Q')]/4
J10, J11, J20, J21 = JT[(1,0)], JT[(1,1)], JT[(2,0)], JT[(2,1)]
Fa = (m1*J20 + m1q*J21/2)/2 + (m2*J10 + m2q*J11/2)/2
Fb = (m3*J20 + m3q*J21/2)/2 + m4*J10 + m4q*J11/2

expr_b = sp.expand(sp.expand(sp.expand(rr**2*(rr**2*Fa + Fb))*sp.Rational(3,2)).rewrite(sp.log), force=True)
expr_b = expr_b.subs(sp.log(1-rr**2), sp.log(1-rr)+sp.log(1+rr))
terms = sp.Add.make_args(sp.expand(expr_b))
log("channel-b r-integrand: %d terms" % len(terms))

import mpmath as mp
mp.mp.dps = 40
def term_num(term):
    f = sp.lambdify(rr, term, modules='mpmath')
    def g(x):
        try: return mp.mpf(f(mp.mpf(x)))
        except Exception: return mp.mpf(0)
    pts = [0, mp.mpf('0.5'), mp.mpf('0.9'), mp.mpf('0.99'), mp.mpf('0.9999'), 1]
    return mp.quad(g, pts)

bad = []
tot = sp.Integer(0)
for i, term in enumerate(terms):
    iv = sp.simplify(sp.integrate(term, (rr, 0, 1)))
    tot += iv
    nv = term_num(term)
    sv = mp.mpf(str(sp.N(iv, 30)))
    dev = abs(sv - nv)/abs(nv) if nv != 0 else abs(sv - nv)
    flag = "CULPRIT" if dev > mp.mpf('1e-25') else "ok"
    if flag == "CULPRIT": bad.append(i)
    log("term %2d: sym %.30s | quad %.20s | rel %.2e  %s" % (i, sp.N(iv,8), mp.nstr(nv,8), float(dev), flag))
    log("         integrand: %s" % sp.sstr(term)[:180])
    log("         integral : %s" % sp.sstr(iv)[:180])
form = sp.sympify(FORMS["b"])
log("tot_b (no cache)      = %s" % sp.sstr(sp.expand(tot))[:400])
log("N(tot_b,30)           = %s" % sp.N(tot, 30))
log("N(form_b,30)          = %s" % sp.N(form, 30))
log("N(tot_b - form_b, 30) = %s" % sp.N(tot - form, 30))
# also: E2F1's cached tot -- replay WITH the srepr[:120] cache to compare
cache = {}; totc = sp.Integer(0)
for term in terms:
    key = sp.srepr(term)[:120]
    if key in cache: totc += cache[key]; log("CACHE COLLISION at term %d" % terms.index(term)); continue
    iv = sp.simplify(sp.integrate(term, (rr, 0, 1)))
    cache[key] = iv; totc += iv
log("N(E2F1-style cached tot_b, 30) = %s" % sp.N(totc, 30))
log("cached vs no-cache differ: %s" % (sp.simplify(totc - tot) != 0))
log("diag complete; culprits: %s" % bad)
json.dump(dict(log=LOG, culprits=bad), open(os.path.join(HERE, "LR10X_diag.json"), "w"), indent=1)
