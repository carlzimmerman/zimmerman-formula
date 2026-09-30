#!/usr/bin/env python3
"""W3 -- c1(q), the O(tau0) coefficient of c0(tau0,q) = E[D]/tau0 (Z12 door; owns W3_*).

Door: MC7 (exit 0, 4754ea411) left the extrapolation model UNSETTLED; W2 banked
c00(q) = 2/5 + (8/35) q exactly, leaving c1(q) open - it existed NOWHERE on disk
as a measured quantity. Pre-registration: Z12-WAVE_BRIEF.md + AMENDMENTS 1-2
(BEFORE any run; the drafted 4-point intercept gate FIRED in the conductor
pre-audit at q=1, z=3.27, preserved verbatim in Amendment 2 - gate-design
artifact: intercept-slope covariance on the 8e-4 lever arm; estimator replaced
by the c00_exact-anchored fit, which uses the W2/LR8-certified intercept as a
fixed anchor, not a tuned constant).

Engine-exact structure (conductor derivation vs J02_moment_hierarchy.py source,
recorded in Amendment 1): E[D] = E[D1] + E[D2] + O(tau0^3),
  D = sum_j l_j (1 - u_{j-1}.u_f) (telescoping, D = elapsed - (pos-origin).u_f),
  E[D1] = tau0 int_0^W s k(s) e^{-tau0 K(s)} ds,  k(s) = 1 + q(r^2 + 2(p.u)s + s^2),
  K(s) = int_0^s k,  =>  c1(q) = -S(q) + E2(q),
  S(q) = E[int_0^W s k(s) K(s) ds] = C00 + q C01 + q^2 C02  (survival correction),
  E2(q) = E[ int_0^W ds1 k1(s1) int_0^{W2} ds2 k2(s2) (s1+s2) ]  (two-scatter leg;
  the mu-terms vanish: E[u.u2] = E[u1.u2] = 0 by the zero-mean dipole kernel
  thomson_mu, verified against the engine source).

Gates (pre-registered, Z12 brief + amendments):
  M2a: sympy exact C00, C01, C02 (W2 cylindrical mechanism); mpmath + GL(500)
       quadrature of S(q) at q in {0,1,3} dev <= 1e-11 rel -> else exit 1.
  R0c-equivalent: MC cross-check of S(q) (n=2e7, seed 20260929w3): |z| <= 5.
  M1 (amended): anchored quadratic fits on ALL 8 stored MC7 points per q;
       c1(q) measured with propagated SE; LOO ablation recorded (no gate).
  M2c: predicted c1(q) = -S(q) + E2(q) vs measured c1(q) at q in {0,1,3}:
       any |z| > 4 -> structural decomposition REFUTED, exit 1.
       (MC SE of E2 included in the combined SE.)
  q in {6,10}: recorded as scope (curvature/selection knowns).
Exit 0 iff M2a + MC-S pass and M2c completes with no fire (or E2 execution
failure -> honest UNRESOLVED scope note, exit 0).
"""
import json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "W3_c1_measurement.out")
RESF = os.path.join(HERE, "W3_results.json")
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time() - _T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="W3 c1(q): O(tau0) coefficient of c0(tau0,q)",
               pre_registration="Z12-WAVE_BRIEF.md + AMENDMENTS 1-2 (before any run)",
               verdict=verdict, exit=rc, elapsed_s=round(time.time()-_T0,1), log=LOG)
    if extra: RES.update(extra)
    json.dump(RES, open(RESF, "w"), indent=1, default=str)
    with open(OUT, "a") as f: f.write("\n".join(LOG) + "\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

QS = [0.0, 1.0, 3.0, 6.0, 10.0]

# ---------- M1 (amended): anchored quadratic fits on MC7's stored 8-point grids ----------
log("M1: anchored fits c0 - c00_exact = c1*tau0 + c2*tau0^2, all 8 stored points")
m7 = json.load(open(os.path.join(HERE, "MC7_results.json")))
ex = lambda q: 0.4 + (8/35)*q
m1 = {}
for k in sorted(m7["meas"], key=float):
    q = float(k)
    pts = sorted(m7["meas"][k]["points"], key=lambda p: p[0])
    t = np.array([p[0] for p in pts]); y = np.array([p[1] for p in pts]) - ex(q)
    se = np.array([p[2] for p in pts])
    Wd = np.diag(1/se**2); A = np.vstack([t, t*t]).T
    ata = A.T@Wd@A; cov = np.linalg.inv(ata); sol = np.linalg.solve(ata, A.T@Wd@y)
    c1, c2 = float(sol[0]), float(sol[1]); se1, se2 = float(np.sqrt(np.diag(cov))[0]), float(np.sqrt(np.diag(cov))[1])
    loo = []
    for j in range(len(t)):
        m = np.ones(len(t), bool); m[j] = False
        Wj = np.diag(1/se[m]**2); Aj = A[m]
        sol_j = np.linalg.solve(Aj.T@Wj@Aj, Aj.T@Wj@y[m])
        loo.append(float(sol_j[0]))
    m1[k] = dict(c1=c1, se1=se1, c2=c2, se2=se2, loo=loo, npts=len(t))
    log("M1: q=%-4g c1 = %+.4f +- %.4f  (c2 = %+.2f +- %.2f; LOO %s)"
        % (q, c1, se1, c2, se2, " ".join("%+.2f" % v for v in loo)))

# ---------- M2a: sympy exact survival correction ----------
log("M2a: sympy exact C00, C01, C02 via the W2 cylindrical (rho,w) mechanism")
import sympy as sp
x, w, v, qq = sp.symbols("x w v q", real=True)
s = sp.sqrt(1 - x**2)
Wg = s*(1 - w); z = s*w; r2 = x**2 + s**2*w**2
A = r2 + 2*z*v + v**2; B = r2*v + z*v**2 + v**3/3
integ = sp.expand(v*(1 + qq*A)*(v + qq*B))
Iint = sp.expand(sp.integrate(integ, (v, 0, Wg)))   # expand BEFORE coeff (dry-run trap, on record)
C = []
for kk in (0, 1, 2):
    e = sp.expand(x*s*Iint.coeff(qq, kk))
    C.append(sp.simplify(sp.Rational(3,2)*sp.integrate(e, (w, -1, 1), (x, 0, 1))))
log("M2a: C00 = %s, C01 = %s, C02 = %s" % tuple(sp.nsimplify(c) for c in C))
S_ex = {q: float(C[0] + C[1]*q + C[2]*q*q) for q in QS}
S_rat = {q: (C[0] + C[1]*sp.Rational(int(q)) + C[2]*sp.Rational(int(q))**2) for q in QS}
if not all(c == sp.nsimplify(c) and c.is_Rational for c in C):
    finish(1, "M2a FIRED: C's not exact rationals", dict(C=[str(c) for c in C]))

# quadrature gates: mpmath + GL(500) of S(q) at q in {0,1,3}
import mpmath as mp
mp.mp.dps = 40
# Amendment 10: antiderivative built MECHANICALLY by sympy (hand form fired honestly, on record)
import sympy as _sp
_v, _q, _R, _Z = _sp.symbols("v q r2 z", real=True)
_integ = _sp.expand(_v*(1 + _q*(_R + 2*_Z*_v + _v**2))*(_v + _q*(_R*_v + _Z*_v**2 + _v**3/3)))
_Ia = _sp.expand(_sp.integrate(_integ, _v))
_Iant0 = _Ia - _Ia.subs(_v, 0)                      # exact int_0^v s k K ds
_W = _sp.Symbol("W")
Iant = _sp.lambdify((_W, _R, _Z, _q), _Iant0.subs(_v, _W), modules="mpmath")
def S_quad(qq_val, method):
    qv = mp.mpf(qq_val)
    if method == "mp":
        # Amendment 6: GL(200) nodes from scipy -> mpf; dps=40 arithmetic is the independence payload
        from scipy.special import roots_legendre as _rl
        _t, _w = _rl(200)
        tx = [mp.mpf(repr(v)) for v in _t]; wxm = [mp.mpf(repr(v)) for v in _w]
        xg = [(1 + t)/2 for t in tx]; wxp = [v/2 for v in wxm]
        wwg, wwp = tx, wxm                   # w on [-1,1] directly
        tot = mp.mpf(0)
        for i in range(200):
            row = mp.mpf(0)
            xi = xg[i]
            sm_i = mp.sqrt(1 - xi*xi)
            for j in range(200):
                _Wm = sm_i*(1 - wwg[j]); _zm = sm_i*wwg[j]
                row += wwp[j]*sm_i*Iant(_Wm, xi*xi + _zm*_zm, _zm, qv)
            tot += wxp[i]*xi*row
        return mp.mpf(3)/2*tot
    qv = float(qq_val)   # Amendment 8: GL branch is float64 (mpf x ndarray = object-dtype hang, on record)
    from scipy.special import roots_legendre
    ng = 500; t, wg = roots_legendre(ng)
    xg = 0.5*(1 - t); wx = 0.5*wg          # x on [0,1]
    ww = wg                                 # w on [-1,1] (Amendment 9: full weights)
    sg = np.sqrt(1 - xg**2)[:, None]; Wm = sg*(1 - t[None, :]); zm = sg*t[None, :]
    r2m = xg[:, None]**2 + zm**2
    # Gauss-Legendre in v on [0, W] per (x,w): v = W*(1+t)/2
    tv, wv = roots_legendre(120)
    vv = Wm[..., None]*(1 + tv[None, None, :])/2
    wvv = Wm[..., None]*wv[None, None, :]/2
    kv = 1 + qv*(r2m[..., None] + 2*zm[..., None]*vv + vv**2)
    Kv = vv + qv*(r2m[..., None]*vv + zm[..., None]*vv**2 + vv**3/3)
    return 1.5*np.sum(ww[None, :, None]*wx[:, None, None]*xg[:, None, None]*sg[..., None]*wvv*vv*kv*Kv)
def Sint(x, ww, qv):
    sm = mp.sqrt(1 - x*x); Wm = sm*(1 - ww); zm = sm*ww; r2m = x*x + zm*zm
    f = lambda vv: vv*(1 + qv*(r2m + 2*zm*vv + vv**2))*(vv + qv*(r2m*vv + zm*vv**2 + vv**3/3))
    return mp.quad(f, [0, Wm])
sm_ = lambda x: mp.sqrt(1 - x*x)
devs = {}
for q in (0.0, 1.0, 3.0):
    a0 = float(S_quad(q, "mp")); a1 = float(S_quad(q, "gl"))
    devs[q] = (abs(a0 - S_ex[q])/max(abs(S_ex[q]), 1e-300), abs(a1 - S_ex[q])/max(abs(S_ex[q]), 1e-300))
    log("M2a: S(%g): exact %.8f  mp dev %.2e  gl dev %.2e (gate 1e-11)" % (q, S_ex[q], devs[q][0], devs[q][1]))
    if max(devs[q]) > 1e-11:
        finish(1, "M2a FIRED: quadrature dev > 1e-11 at q=%g" % q, dict(devs={str(k): v for k, v in devs.items()}))
log("M2a PASS: S(q) = %s + (%s) q + (%s) q^2 exact, quadrature-clean" % tuple(sp.nsimplify(c) for c in C))

# ---------- MC cross-check of S(q) ----------
log("MC-S: direct MC of S(q) = E[int_0^W s k K ds], n=2e7, seed 20260929w3")
rng = np.random.default_rng(202609293)
n = 20_000_000
d0 = rng.normal(size=(n, 3)); d0 /= np.linalg.norm(d0, axis=1)[:, None]
p = d0 * rng.random(n)[:, None]**(1/3)
du = rng.normal(size=(n, 3)); u = du/np.linalg.norm(du, axis=1)[:, None]
z = np.sum(p*u, axis=1); r2n = np.sum(p*p, axis=1)
Wn = -z + np.sqrt(np.maximum(z*z - r2n + 1.0, 0.0))
Iant_np = _sp.lambdify((_W, _R, _Z, _q), _Iant0.subs(_v, _W), modules="numpy")  # Amendment 12: mechanical antiderivative, vectorized
mcS = {}
for q in (0.0, 1.0, 3.0):
    X = Iant_np(Wn, r2n, z, q)   # exact int_0^W s k K ds per sample (mechanically derived, Amendment 10)
    m_, se_ = float(np.mean(X)), float(np.std(X, ddof=1)/np.sqrt(n))
    zz = abs(m_ - S_ex[q])/se_
    mcS[q] = dict(mean=m_, se=se_, z=zz)
    log("MC-S: q=%g: %.6f +- %.6f vs exact %.6f  z=%.2f (gate 5)" % (q, m_, se_, S_ex[q], zz))
    if zz > 5:
        finish(1, "MC-S FIRED at q=%g (z=%.2f): exact S(q) or reduction wrong" % (q, zz), dict(mcS=mcS))
log("MC-S PASS")

# ---------- M2b: MC of the two-scatter leg E2(q) ----------
log("M2b: MC of E2(q) (two-scatter leg), n=4e6 events x 8 dipole samples, seed 20260929e2")
def dipole_sample(rng, m):
    """Engine thomson_mu distribution: rejection on (1+mu^2)/2 in [-1,1], zero-mean."""
    out = np.empty(m); todo = np.arange(m)
    while len(todo):
        mm = rng.uniform(-1, 1, len(todo))
        take = rng.random(len(todo)) < (1 + mm*mm)/2
        out[todo[take]] = mm[take]; todo = todo[~take]
    return out
rng2 = np.random.default_rng(202609294)
ne, nu1 = 4_000_000, 8
d0 = rng2.normal(size=(ne, 3)); d0 /= np.linalg.norm(d0, axis=1)[:, None]
p = d0 * rng2.random(ne)[:, None]**(1/3)
du = rng2.normal(size=(ne, 3)); u = du/np.linalg.norm(du, axis=1)[:, None]
z = np.sum(p*u, axis=1); r2n = np.sum(p*p, axis=1)
Wn = -z + np.sqrt(np.maximum(z*z - r2n + 1.0, 0.0))
S = rng2.random(ne)*Wn                       # S ~ U[0,W]; weight k1(S)
k1 = 1.0                                     # per-q below
p1 = p + S[:, None]*u
r12 = np.sum(p1*p1, axis=1)
# dipole u1 samples: mu via thomson_mu dist, azimuth uniform, basis per event
mu = dipole_sample(rng2, ne*nu1).reshape(ne, nu1)
phi = rng2.uniform(0, 2*np.pi, (ne, nu1))
a = np.where(np.abs(u[:, 0:1]) < 0.9, np.array([1.0, 0, 0]), np.array([0, 1.0, 0]))*np.ones((ne, 3))
e1 = np.cross(u, a); e1 /= np.linalg.norm(e1, axis=1)[:, None]
e2 = np.cross(u, e1)
u1 = (mu[..., None]*u[:, None, :]
      + np.sqrt(1 - mu*mu)[..., None]*(np.cos(phi)[..., None]*e1[:, None, :] + np.sin(phi)[..., None]*e2[:, None, :]))
pd2 = np.sum(p1[:, None, :]*u1, axis=2)                       # (ne, nu1)
disc = pd2*pd2 - r12[:, None] + 1.0
W2 = -pd2 + np.sqrt(np.maximum(disc, 0.0))
e2mc = {}
for q in QS:
    k1q = 1 + q*(r2n + 2*z*S + S*S)
    K2tot = W2 + q*(r12[:, None]*W2 + pd2*W2**2 + W2**3/3)
    c0f = W2**2/2 + q*(r12[:, None]*W2**2/2 + 2*pd2*W2**3/3 + W2**4/4)
    G = S[:, None]*K2tot + c0f                                # E over u1 inside
    X = Wn*k1q*G.mean(axis=1)
    m_, se_ = float(X.mean()), float(X.std(ddof=1)/np.sqrt(ne))
    e2mc[q] = dict(mean=m_, se=se_)
    log("M2b: E2(%g) = %.6f +- %.6f" % (q, m_, se_))

# ---------- M2c: structural prediction vs measured slopes ----------
log("M2c: predicted c1(q) = -S(q) + E2(q) vs measured (anchored) c1(q), gate |z| <= 4 at q in {0,1,3}")
m2c = {}; fired = False
for q in (0.0, 1.0, 3.0):
    k = str(float(q))   # Amendment 13: m1 keys are MC7's "0.0"-style strings
    pred = -S_ex[q] + e2mc[q]["mean"]
    comb = np.sqrt(m1[k]["se1"]**2 + e2mc[q]["se"]**2)
    zz = abs(pred - m1[k]["c1"])/comb
    m2c[q] = dict(pred=pred, surv=-S_ex[q], e2=e2mc[q]["mean"], meas=m1[k]["c1"],
                  se_comb=float(comb), z=float(zz))
    log("M2c: q=%g: pred %+.4f (surv %+.4f + e2 %+.4f) vs meas %+.4f +- %.4f  z=%.2f %s"
        % (q, pred, -S_ex[q], e2mc[q]["mean"], m1[k]["c1"], comb, zz,
           "GATE" if zz > 4 else "pass"))
    if zz > 4: fired = True
scope = {q: dict(pred=-S_ex[q] + e2mc[q]["mean"], meas=m1[str(float(q))]["c1"],
                 se=m1[str(float(q))]["se1"]) for q in (6.0, 10.0)}
log("M2c scope: q=6: pred %+.4f vs meas %+.4f+-%.4f ; q=10: pred %+.4f vs meas %+.4f+-%.4f (records only)"
    % (scope[6.0]["pred"], scope[6.0]["meas"], scope[6.0]["se"],
       scope[10.0]["pred"], scope[10.0]["meas"], scope[10.0]["se"]))
if fired:
    finish(1, "M2c FIRED: structural decomposition c1 = -S + E2 REFUTED at measured power",
           dict(m1=m1, m2c=m2c, scope={str(k): v for k, v in scope.items()}, mcS=mcS, devs=devs))
Srat = {("%g" % q): str(sp.nsimplify(S_rat[q])) for q in QS}
finish(0, "LANDED: c1(q) = -S(q) + E2(q) structure CONFIRMED at measured power (z = %.2f/%.2f/%.2f at q=0/1/3, gate 4); "
          "survival correction EXACT: S(q) = %s + (%s) q + (%s) q^2; two-scatter leg MEASURED by MC "
          "E2 = %.4f/%.4f/%.4f (+- %.4f/%.4f/%.4f) at q=0/1/3; exact c1(q) closed form remains OPEN "
          "(E2 leg = a 6D two-ray integral, reduced exact form recorded); measured c1(q) now on disk "
          "for the first time" % (m2c[0.0]["z"], m2c[1.0]["z"], m2c[3.0]["z"],
          sp.nsimplify(C[0]), sp.nsimplify(C[1]), sp.nsimplify(C[2]),
          e2mc[0.0]["mean"], e2mc[1.0]["mean"], e2mc[3.0]["mean"],
          e2mc[0.0]["se"], e2mc[1.0]["se"], e2mc[3.0]["se"]),
       dict(m1=m1, m2c=m2c, scope={str(k): v for k, v in scope.items()},
            S_exact=[str(sp.nsimplify(c)) for c in C], S_rat=Srat, mcS=mcS, devs={str(k): v for k, v in devs.items()},
            e2mc={str(k): v for k, v in e2mc.items()}))
