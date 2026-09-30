#!/usr/bin/env python3
"""LR9 -- R0 algebra audit + core-assembly extraction for the W3 survival law
S(q) = 1/3 + (1/3) q + (46/525) q^2  (Z13 door; owns LR9_*).

Door: W3 (exit 0) banked S(q) = C00 + q C01 + q^2 C02 with exact rationals
1/3, 1/3, 46/525 on THREE independent evaluations + MC (z = 0.79/0.85/0.89).
Its rationals are NOT yet certificate-grade. This lane: (R0a) FRESH sympy
derivation by a DIFFERENT method than W3's sp.integrate -- monomial-basis
assembly (Poly arithmetic in v over atom symbols R,Z,W + explicit
int_0^W v^j dv = W^{j+1}/(j+1), then the atom substitutions
W -> s(1-w), Z -> s w, R -> 1-s^2+s^2 w^2 (x^2 = 1-s^2), odd-w monomials
zeroed explicitly, even-w moments 2/(2j+1)) -- must reproduce W3's banked
rationals (LOADED from W3_results.json, never transcribed) AND yield the
core assembly C_k = sum_j alpha_{k,j}/(2j+3) where core_j =
int_0^1 x (1-x^2)^j sqrt(1-x^2) dx = 1/(2j+3) (T_k class, LR7 precedent).
(R0b) two independent quadratures of the (x,w) integral (mp dps=40 via
GL(300) nodes; float64 GL(600)xGL(140) with v-quadrature). (R0c) MC of the
full geometric reduction, FRESH seed (W3 used 202609293).
KILLS pre-registered (Z13-WAVE_BRIEF.md LR9 door): exact mismatch /
quadrature dev > 1e-12 rel / MC |z| > 5 -> exit 1.
"""
import json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "LR9_sq_law.out")
RESF = os.path.join(HERE, "LR9_results.json")
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time()-_T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="LR9 R0 audit: W3 survival law S(q) rationals",
               pre_registration="Z13-WAVE_BRIEF.md LR9 door",
               verdict=verdict, exit=rc, elapsed_s=round(time.time()-_T0,1), log=LOG)
    if extra: RES.update(extra)
    json.dump(RES, open(RESF,"w"), indent=1, default=str)
    with open(OUT,"a") as f: f.write("\n".join(LOG)+"\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

import sympy as sp

_w3 = json.load(open(os.path.join(HERE, "W3_results.json")))
want = [sp.Rational(sp.sstr(sp.nsimplify(c))) for c in _w3["S_exact"]]
log("W3 banked rationals LOADED from W3_results.json: %s" % want)

# ---------- R0a: fresh monomial-basis exact derivation ----------
log("R0a: fresh monomial-basis derivation of C00, C01, C02")
# atom symbols: the integrand lives in (v; R=r^2, Z=p.u, W=wall distance, q)
_v, R, Z, W, qq = sp.symbols("v R Z W q", real=True)
A = R + 2*Z*_v + _v**2
B = R*_v + Z*_v**2 + _v**3/3
integ = sp.expand(_v*(1 + qq*A)*(_v + qq*B))
pv = sp.Poly(integ, _v)
Iant_RZW = sp.expand(sum(c * W**(j+1)/(j+1) for (j,), c in pv.terms()))  # int_0^W v^j dv = W^{j+1}/(j+1)
Iant_RZW = sp.expand(Iant_RZW - Iant_RZW.subs(W, 0))                     # exact int_0^W (kills constant term if any)

x, w, s = sp.symbols("x w s", real=True, positive=True)
# atom substitutions (rectangle integral over s = sqrt(1-x^2), z = s w, r2 = x^2 + s^2 w^2, x^2 = 1-s^2):
subsmap = {W: s*(1 - w), Z: s*w, R: 1 - s**2 + s**2*w**2}
Iant_sw = sp.expand(Iant_RZW.xreplace(subsmap))

C_fresh = []; alpha = {}
for k in (0, 1, 2):
    P = sp.Poly(sp.expand(Iant_sw.coeff(qq, k) * x * s), w)   # polynomial in w, coeffs in s (+ x-prefactor)
    # zero odd w-monomials explicitly, integrate even ones over [-1,1]: 2/(2j+1)
    inner = 0
    for (j,), c in P.terms():
        if j % 2 == 0:
            inner += c * sp.Rational(2, j+1)   # int_{-1}^{1} w^j dw = 2/(j+1) for even j
    inner = sp.expand(inner)          # = x * sum_m beta_m s^m (m odd), betas pure rational
    Pin = sp.Poly(sp.simplify(inner / x), s)   # strip the x-prefactor
    tot = 0; am = {}
    for (m,), c in Pin.terms():
        assert c.is_Rational, "non-rational coefficient %s" % c
        # int_0^1 x s^{m} dx = 1/(m+2) for EVERY m >= 0 (t = 1-x^2: (1/2) int_0^1 t^{m/2} dt).
        # odd m = 2j+1: T_k class (LR7), value 1/(2j+3); even m = 2j: U_k class, value 1/(2j+2).
        core = sp.Rational(1, m+2)
        c95 = sp.simplify(sp.Rational(3,2) * c)     # the (3/2) cylindrical density prefactor
        tot += c95 * core
        am[m] = c95                                  # alpha_{k,m} ; C_k = sum_m alpha/(m+2)
    C_fresh.append(sp.simplify(tot))
    alpha[k] = {int(mm): sp.nsimplify(aa) for mm, aa in am.items()}
    log("R0a: C%d fresh = %s" % (k, C_fresh[k]))

if C_fresh != want:
    finish(1, "R0a FIRED: fresh derivation %s != W3 banked %s" % (C_fresh, want),
           dict(alpha={k: {str(a): str(b) for a,b in alpha[k].items()} for k in alpha}))
log("R0a PASS: W3 banked rationals reproduced by the independent monomial path")
for k in (0,1,2):
    log("R0a: alpha[q^%d]: %s" % (k, {("m=%d (1/%d, %s)" % (m, m+2, "T" if m % 2 else "U")): str(alpha[k][m]) for m in sorted(alpha[k])}))

# ---------- R0b: two independent quadratures of the (x,w) integral ----------
import mpmath as mp
mp.mp.dps = 40
Iant_mp = sp.lambdify((W, R, Z, qq), Iant_RZW, modules="mpmath")
from scipy.special import roots_legendre
t300, w300 = roots_legendre(300)
tx = [mp.mpf(repr(a)) for a in t300]; wx = [mp.mpf(repr(a)) for a in w300]
def S_mp(qv):
    qm = mp.mpf(qv); tot = mp.mpf(0)
    for i in range(300):
        xi = (1 + tx[i])/2; sm = mp.sqrt(1 - xi*xi)
        row = mp.mpf(0)
        for j in range(300):
            Wm = sm*(1 - tx[j]); zm = sm*tx[j]
            row += wx[j]*sm*Iant_mp(Wm, xi*xi + zm*zm, zm, qm)
        tot += wx[i]/2*xi*row
    return mp.mpf(3)/2*tot
def S_gl(qv):
    qf = float(qv)
    ng1, ng2, ngv = 600, 140, 140
    t1, w1 = roots_legendre(ng1); t2, w2 = roots_legendre(ng2); tv, wv = roots_legendre(ngv)
    xg = 0.5*(1 - t1); wx1 = 0.5*w1
    sg = np.sqrt(1 - xg**2)[:, None]
    Wm = sg*(1 - t2[None, :]); zm = sg*t2[None, :]
    r2m = xg[:, None]**2 + zm**2
    vv = Wm[..., None]*(1 + tv[None, None, :])/2
    wvv = Wm[..., None]*wv[None, None, :]/2
    kv = 1 + qf*(r2m[..., None] + 2*zm[..., None]*vv + vv**2)
    Kv = vv + qf*(r2m[..., None]*vv + zm[..., None]*vv**2 + vv**3/3)
    return 1.5*np.sum(wx1[:, None, None]*w2[None, :, None]*xg[:, None, None]*sg[..., None]*wvv*vv*kv*Kv)
S_ex = {q: float(want[0] + want[1]*q + want[2]*q*q) for q in (0.0, 1.0, 3.0)}
devs = {}
for q in (0.0, 1.0, 3.0):
    a0 = float(S_mp(q)); a1 = float(S_gl(q))
    devs[q] = (abs(a0 - S_ex[q])/max(abs(S_ex[q]), 1e-300), abs(a1 - S_ex[q])/max(abs(S_ex[q]), 1e-300))
    log("R0b: S(%g): exact %.10f  mp dev %.2e  gl dev %.2e (gate 1e-12)" % (q, S_ex[q], devs[q][0], devs[q][1]))
    if max(devs[q]) > 1e-12:
        finish(1, "R0b FIRED: quadrature dev > 1e-12 at q=%g" % q, dict(devs={str(k): v for k, v in devs.items()}))
log("R0b PASS")

# ---------- R0c: MC of the full geometric reduction, fresh seed ----------
log("R0c: MC of S(q), n=2e7, FRESH seed 20260930")
Iant_np = sp.lambdify((W, R, Z, qq), Iant_RZW, modules="numpy")
rng = np.random.default_rng(20260930)
n = 20_000_000
d0 = rng.normal(size=(n, 3)); d0 /= np.linalg.norm(d0, axis=1)[:, None]
p = d0 * rng.random(n)[:, None]**(1/3)
du = rng.normal(size=(n, 3)); u = du/np.linalg.norm(du, axis=1)[:, None]
zz = np.sum(p*u, axis=1); r2n = np.sum(p*p, axis=1)
Wn = -zz + np.sqrt(np.maximum(zz*zz - r2n + 1.0, 0.0))
mcS = {}
for q in (0.0, 1.0, 3.0):
    X = Iant_np(Wn, r2n, zz, q)
    m_, se_ = float(np.mean(X)), float(np.std(X, ddof=1)/np.sqrt(n))
    zsc = abs(m_ - S_ex[q])/se_
    mcS[q] = dict(mean=m_, se=se_, z=zsc)
    log("R0c: q=%g: %.6f +- %.6f vs exact %.6f  z=%.2f (gate 5)" % (q, m_, se_, S_ex[q], zsc))
    if zsc > 5:
        finish(1, "R0c FIRED at q=%g (z=%.2f)" % (q, zsc), dict(mcS=mcS))
log("R0c PASS")
finish(0, "R0 AUDIT LANDED: fresh monomial path reproduces S(q) = 1/3 + (1/3)q + (46/525)q^2 exactly; "
          "quadrature-clean (mp dps=40 GL(300), float64 GL(600)xGL(140)v); MC-consistent at fresh seed; "
          "core-assembly coefficients extracted for the Lean leg",
       dict(alpha={k: {("core_%d" % m): str(alpha[k][m]) for m in sorted(alpha[k])} for k in alpha},
            devs={str(k): v for k, v in devs.items()}, mcS={str(k): v for k, v in mcS.items()}))
