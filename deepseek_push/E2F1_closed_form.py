#!/usr/bin/env python3
"""E2F1 -- exact closed form of E2(q) = a + b q + c q^2 (Z16 door; owns E2F1_*).

Pre-registration: Z16-WAVE_BRIEF.md (committed f049ca089 BEFORE any run) + AMENDMENT 1
(exponential-coordinate implementation; lattice may need zeta(3); gates unchanged).
Reduction (brief, hand-derived BEFORE any run):
  E2(q) = (3/2) int_0^1 r^2 dr int_{-1}^{1} dmu int_0^{Wb} dS (1+q r^2)[ S(M1+qM3) + (M2+qM4) ]
  p1 uniform in ball x u isotropic independent; Wb = r mu + A, A = sqrt(1-r^2+r^2 mu^2);
  a1 = r^2; u1-dependence only via x = pd2/r: W2(x) = -r x + sqrt(r^2 x^2+1-r^2),
  A2 = r^2 W2 + r x W2^2 + W2^3/3, c0qf = r^2 W2^2/2 + (2/3) r x W2^3 + W2^4/4;
  E_dip[h] = Ibar[h] + hbar2[h] P2(mu)/2;  Mj = mj + P2(mu) mjq/2; S-integrated:
    a = (3/2) int r^2 Fa,  Fa = (1/2)(m1 J20 + (m1q/2) J21) + m2 J10 + (m2q/2) J11
    b = (3/2) int r^2 (r^2 Fa + Fb),  Fb = (1/2)(m3 J20 + (m3q/2) J21) + m4 J10 + (m4q/2) J11
    c = (3/2) int r^4 Fb
AMENDMENT 1 (registered before any run): exponential coordinates
  r = tanh(uu), c = sech(uu), t = r x = c sinh(v), mu = (c/r) sinh(w), with
  v, w in [-uu, uu] (since asinh(r/c) = uu identically); then
  W2 = c e^{-v}, Wb = c e^{w}, A = c cosh w -- every integrand is an
  exponential polynomial => entire => spectral quadrature and mechanical symbolic closure.
  Inner moments: I_{jn}[+Q] = (1/(2 r^{j+1})) int_{-uu}^{uu} c^{j+n+1} sinh^j(v) e^{-nv} cosh(v) [P2(c sinh(v)/r)] dv
  J-table:      J_k[+Q]   = int_{-uu}^{uu} (c e^w)^k (c/r) cosh(w) [P2(c sinh(w)/r)] dw
Hand pre-checks (derived pre-run, gated below): J20 = 2 - (2/3) r^2, J21 = (8/15) r^2,
J10 = 1 + (c^2/r) atanh(r), Ibar[W2] = 1/2 + (c^2/(2r)) atanh(r),
E[Wb] = 3/4, E[int dS S] = 2/5, and u-branches (atanh terms) occur ONLY on
m1/m3/m1q/m3q/J10/J11 => no atanh^2 => closed form in span{1, ln2, pi^2} x Q
(zeta(3) basis kept defensively).
Gates (frozen in the brief; any fire -> exit 1, no tuning):
  G0  numeric (a,b,c) vs E2Q1 stored fit |z|<=3
  G0b internal: E[Wb]=3/4, int dS S -> 2/5, Ibar[W2](0.5) hand formula, rel<=1e-10
  G1  symbolic inner moments vs numeric rel<=1e-10 at r in {0.2,0.5,0.8,0.95}
  G2  dipole decomposition: direct (mu,phi) 2D quad vs Ibar+hbar2*P2/2, rel<=1e-10
  G2b symbolic J-table vs numeric rel<=1e-10
  G3  symbolic closed (a,b,c) vs independent numeric pipeline rel<=1e-9 (+rule doubling <=1e-11)
  G4  closed (a,b,c) vs E2Q1 stored fit |z|<=3 (SEs loaded-not-transcribed)
  G5  fresh MC seed 20261001, n=2e6 x 4 dipole, q in {0,3,10}: |z|<=3
"""
import json, os, sys, time, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "E2F1_closed_form.out")
RESF = os.path.join(HERE, "E2F1_results.json")
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time() - _T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="E2F1: exact closed form of E2(q) = a + b q + c q^2 (Z16 door)",
               pre_registration="Z16-WAVE_BRIEF.md f049ca089 + AMENDMENT 1 (before any run)",
               verdict=verdict, exit=rc, elapsed_s=round(time.time()-_T0,1), log=LOG)
    if extra: RES.update(extra)
    json.dump(RES, open(RESF, "w"), indent=1, default=str)
    with open(OUT, "a") as f: f.write("\n".join(LOG) + "\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

def P2(x): return 1.5*x*x - 0.5
from numpy.polynomial.legendre import leggauss

# ============ S1: numeric pipeline in exponential coordinates ============
log("S1: numeric (a,b,c) via exponential-coordinate spectral nesting")
UMAX = 12.0
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
            base = (c*sh)**j * (c*en)**n * (c*ch)          # c^{j+n+1} sinh^j e^{-n v} cosh v
            mI[(j,n)] = np.sum(WV*base)/(2.0*r**(j+1))
            mQ[(j,n)] = np.sum(WV*base*P2(c*sh/r))/(2.0*r**(j+1))
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
            J[(k,1)] = np.sum(wW*baseJ*P2(c*shw/r))
        J10, J11, J20, J21 = J[(1,0)], J[(1,1)], J[(2,0)], J[(2,1)]
        Fa = 0.5*(m1*J20 + 0.5*m1q*J21) + 0.5*(m2*J10 + 0.5*m2q*J11)   # AMENDMENT 2: c00f = W2^2/2
        Fb = 0.5*(m3*J20 + 0.5*m3q*J21) + m4*J10 + 0.5*m4q*J11
        Fa_all[i] = Fa; Fb_all[i] = Fb
    r2 = np.tanh(us)**2; sech2 = 1.0/np.cosh(us)**2
    a = 1.5*np.sum(wu*r2*sech2*Fa_all)
    b = 1.5*np.sum(wu*r2*sech2*(r2*Fa_all + Fb_all))
    cc = 1.5*np.sum(wu*r2*sech2*r2*Fb_all)
    return np.array([a, b, cc]), us, wu

abc1, us1, wu1 = num_coeffs(90, 70, 70)
log("S1: GL(90,70,70): a=%.12f b=%.12f c=%.12f" % tuple(abc1))
abc2, _, _ = num_coeffs(140, 110, 110)
log("S1: GL(140,110,110): a=%.12f b=%.12f c=%.12f" % tuple(abc2))
rule_dev = float(np.max(np.abs(abc1-abc2)/np.abs(abc2)))
log("S1: rule-doubling max rel dev %.2e" % rule_dev)
if rule_dev > 1e-11:
    finish(1, "S1 FIRED: quadrature rule-doubling disagreement %.2e > 1e-11" % rule_dev)

# ---- G0b internal consistency ----
log("G0b: internal consistency checks")
xg, wg = leggauss(90); us_ = 0.5*(xg+1)*UMAX; wus = 0.5*wg*UMAX
wg_, wwg = leggauss(70)
J10s = []; J20s = []
for uu in us_:
    r = math.tanh(uu); c = 1/math.cosh(uu); W = uu*wg_
    ew = np.exp(W); chw = np.cosh(W)
    J10s.append(np.sum(wwg_*(c*ew)*(c/r)*chw))
    J20s.append(np.sum(wwg_*(c*ew)**2*(c/r)*chw))
J10s = np.array(J10s); J20s = np.array(J20s)
sech2_ = 1.0/np.cosh(us_)**2
E_Wb   = 1.5*np.sum(wus*np.tanh(us_)**2*sech2_*J10s)
E_intS = 1.5*np.sum(wus*np.tanh(us_)**2*sech2_*0.5*J20s)
# Ibar[W2](0.5): direct v-quad
uu = math.atanh(0.5); c05 = math.sqrt(1-0.25)
vg2, wvg2 = leggauss(200); V = uu*vg2
base = (c05*np.exp(-V))*(c05*np.cosh(V))
ib05 = np.sum(uu*wvg2*base)/(2*0.5)
hand = 0.5*(1.0 + (1.0-0.25)/0.5*math.atanh(0.5))
g0b = dict(E_Wb=dict(val=float(E_Wb), expect=0.75, reldev=float(abs(E_Wb-0.75)/0.75)),
           E_intS=dict(val=float(E_intS), expect=0.4, reldev=float(abs(E_intS-0.4)/0.4)),
           Ibar_W2_r05=dict(val=float(ib05), expect=float(hand), reldev=float(abs(ib05-hand)/abs(hand))))
for k, v in g0b.items():
    log("G0b: %s = %.14f expect %.14f reldev %.2e" % (k, v['val'], v['expect'], v['reldev']))
    if v['reldev'] > 1e-10:
        finish(1, "G0b FIRED at %s (reldev %.2e)" % (k, v['reldev']), dict(g0b=g0b))
log("G0b PASS")

# ---- G0: vs E2Q1 stored fit ----
log("G0: numeric (a,b,c) vs E2Q1 stored fit (loaded-not-transcribed)")
stored = json.load(open(os.path.join(HERE, "E2Q1_results.json")))["fit"]
g0 = {}
for i, k in enumerate("abc"):
    z = (abc2[i] - stored[k]) / stored["s"+k]
    g0[k] = dict(num=float(abc2[i]), stored=stored[k], se=stored["s"+k], z=float(z))
    log("G0: %s: %.9f vs stored %.9f +- %.9f  z=%.2f" % (k, abc2[i], stored[k], stored["s"+k], z))
    if abs(z) > 3:
        finish(1, "G0 FIRED at %s (z=%.2f): reduction chain disagrees with the on-disk estimator" % (k, z), dict(g0=g0))
log("G0 PASS")

# ---- G2: dipole decomposition (direct 2D quad vs reduced) ----
log("G2: dipole decomposition E_dip[h] = Ibar + hbar2*P2(mu)/2 vs direct (mu_dipole,phi) quad")
from scipy.integrate import quad as squad
def hval(h, x, r):
    W2 = -r*x + math.sqrt(r*r*x*x + 1.0 - r*r)
    if h == 1: return W2
    if h == 2: return W2*W2
    if h == 3: return r*r*W2 + r*x*W2*W2 + W2**3/3.0
    if h == 4: return r*r*W2*W2/2.0 + (2.0/3.0)*r*x*W2**3 + W2**4/4.0
def Edip_direct(h, r, mugam):
    sing = math.sqrt(max(0.0, 1.0-mugam*mugam))
    f = lambda mud: (3.0/8.0)*(1.0+mud*mud)*(
        (1.0/(2*math.pi))*squad(lambda ph: hval(h, mud*mugam + math.sqrt(max(0.0,1-mud*mud))*sing*math.cos(ph), r),
                               0, 2*math.pi, epsabs=1e-13, epsrel=1e-11, limit=200)[0])
    return squad(f, -1, 1, epsabs=1e-12, epsrel=1e-10, limit=400, points=[-0.5,0.5])[0]
g2 = {}
ri = 0.5
uu = math.atanh(ri); c05 = math.sqrt(1-ri*ri)
def mom_direct(j, n, p2w, r):
    # smooth even-part form: (1/2) int_{-1}^{1} x^j W2(x)^n [P2(x)] dx
    uu = math.atanh(r); c = math.sqrt(1-r*r)
    f = lambda v: (c*math.sinh(v))**j * (c*math.exp(-v))**n * (c*math.cosh(v)) * (((3*(c*math.sinh(v)/r)**2-1)/2) if p2w else 1.0)
    return squad(f, -uu, uu, epsabs=1e-14, epsrel=1e-12, limit=400)[0]/(2.0*r**(j+1))
for (h, tag) in [(1,'W2'), (4,'c0qf')]:
    if h == 1:
        ib, hb = mom_direct(0,1,False,ri), mom_direct(0,1,True,ri)
    else:
        ib = ri*ri*mom_direct(0,2,False,ri)/2.0 + (2.0/3.0)*ri*mom_direct(1,3,False,ri) + mom_direct(0,4,False,ri)/4.0
        hb = ri*ri*mom_direct(0,2,True,ri)/2.0  + (2.0/3.0)*ri*mom_direct(1,3,True,ri)  + mom_direct(0,4,True,ri)/4.0
    for mugam in (-0.6, 0.3, 0.9):
        direct = Edip_direct(h, ri, mugam)
        pred = ib + 0.5*hb*P2(mugam)
        rel = abs(direct-pred)/max(abs(direct), 1e-30)
        g2["%s_mu%.1f" % (tag, mugam)] = dict(direct=direct, pred=pred, rel=rel)
        log("G2: h=%s r=%.1f mugam=%.1f: direct %.12f vs pred %.12f rel %.2e" % (tag, ri, mugam, direct, pred, rel))
        if rel > 1e-10:
            finish(1, "G2 FIRED (h=%s, mugam=%.1f, rel %.2e): dipole decomposition wrong" % (tag, mugam, rel), dict(g2=g2))
log("G2 PASS")

# ============ S4/S5: symbolic leg in exponential coordinates ============
log("S4: symbolic inner moments + J-table (exponential coordinates)")
import sympy as sp
sym = {"status": None, "a": None, "b": None, "c": None, "notes": []}
try:
    rr = sp.symbols("r", positive=True)
    cu = sp.symbols("cu", positive=True)     # c = sqrt(1-r^2)
    vv = sp.symbols("v", real=True)
    uuS = sp.symbols("u", real=True)         # u = atanh(r); cosh(u) = 1/c, sinh(u) = r/c
    EXP = sp.exp(vv)
    def inner_moment_sym(j, n, p2w):
        expr = (cu)**(j+n+1) * sp.sinh(vv)**j * sp.exp(-n*vv) * sp.cosh(vv)
        if p2w:
            expr = expr * ((3*(cu*sp.sinh(vv)/rr)**2 - 1)/2)
        # expand sinh/cosh into exponentials
        e1 = sp.expand(sp.sinh(vv).rewrite(sp.exp)); e1c = sp.expand(sp.cosh(vv).rewrite(sp.exp))
        repl = {sp.sinh(vv): e1, sp.cosh(vv): e1c}
        ex = sp.expand(expr.subs(repl))
        acc = {}
        for term in sp.Add.make_args(ex):
            d = term.as_powers_dict()
            lam = int(d.get(sp.exp(vv), 0))
            rest = term/(sp.exp(vv)**lam if lam else 1)
            key = lam
            acc[key] = acc.get(key, sp.Integer(0)) + sp.cancel(rest)
        tot = 0
        for lam, cf in acc.items():
            if cf == 0: continue
            if lam == 0:
                tot += cf*2*uuS
            else:
                tot += cf*((sp.exp(lam*uuS) - sp.exp(-lam*uuS))/lam)
        res = tot/(2*rr**(j+1))
        res = res.subs(sp.exp(uuS), (1+rr)/cu).subs(sp.exp(-uuS), cu/(1+rr))
        for k in range(1, 25):
            res = res.subs(sp.exp(k*uuS), ((1+rr)/cu)**k).subs(sp.exp(-k*uuS), (cu/(1+rr))**k)
        res = sp.cancel(sp.expand(res))
        res = res.subs(cu**2, 1-rr**2)
        res = sp.simplify(sp.cancel(res.subs(cu, sp.sqrt(1-rr**2))))
        return res
    log("S4: building 12 inner moments ...")
    MO = {}
    for (j, n) in [(0,1),(0,2),(0,3),(0,4),(1,2),(1,3)]:
        for p2w, tg in ((False,'I'), (True,'Q')):
            v = inner_moment_sym(j, n, p2w)
            MO[(j,n,tg)] = v
            log("S4: moment (j=%d,n=%d,%s) closed" % (j, n, tg))
    log("S4: J-table ...")
    wwS = sp.symbols("w", real=True)
    JT = {}
    for k in (1, 2):
        for p2w, tg in ((False,0), (True,1)):
            expr = (cu*sp.exp(wwS))**k * (cu/rr)*sp.cosh(wwS)
            if p2w: expr = expr*((3*(cu*sp.sinh(wwS)/rr)**2 - 1)/2)
            e1 = sp.expand(sp.sinh(wwS).rewrite(sp.exp)); e1c = sp.expand(sp.cosh(wwS).rewrite(sp.exp))
            ex = sp.expand(expr.subs({sp.sinh(wwS): e1, sp.cosh(wwS): e1c}))
            acc = {}
            for term in sp.Add.make_args(ex):
                d = term.as_powers_dict()
                lam = int(d.get(sp.exp(wwS), 0))
                rest = term/(sp.exp(wwS)**lam if lam else 1)
                acc[lam] = acc.get(lam, sp.Integer(0)) + sp.cancel(rest)
            tot = 0
            for lam, cf in acc.items():
                if cf == 0: continue
                if lam == 0: tot += cf*2*uuS
                else: tot += cf*((sp.exp(lam*uuS) - sp.exp(-lam*uuS))/lam)
            res = tot.subs(sp.exp(uuS), (1+rr)/cu).subs(sp.exp(-uuS), cu/(1+rr))
            for kk in range(1, 25):
                res = res.subs(sp.exp(kk*uuS), ((1+rr)/cu)**kk).subs(sp.exp(-kk*uuS), (cu/(1+rr))**kk)
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
    # ---- G1/G2b: symbolic vs numeric at sample r ----
    log("G1/G2b: symbolic moments/J vs numeric quadrature")
    import mpmath as mp
    mp.mp.dps = 30
    g1 = {}; g2b = {}
    for rsamp in (0.2, 0.5, 0.8, 0.95):
        subs = {rr: rsamp, cu: sp.sqrt(1-rsamp**2)}
        for (j, n) in [(0,1),(0,2),(0,3),(0,4),(1,2),(1,3)]:
            for p2w, tg in ((False,'I'), (True,'Q')):
                sval = float(sp.N(MO[(j,n,tg)].subs(subs), 30))
                uu_ = math.atanh(rsamp); c_ = math.sqrt(1-rsamp*rsamp)
                f = lambda v_: (c_*mp.sinh(v_))**j * (c_*mp.exp(-v_))**n * (c_*mp.cosh(v_)) * (((3*(c_*mp.sinh(v_)/rsamp)**2-1)/2) if p2w else 1)
                nval = mp.quad(f, [-uu_, uu_])/(2*rsamp**(j+1))
                rel = abs(mp.mpf(sval) - nval)/abs(nval)
                key = "r%.2f_j%d_n%d_%s" % (rsamp, j, n, tg)
                g1[key] = float(rel)
                if rel > 1e-10:
                    finish(1, "G1 FIRED (%s rel %.2e): symbolic moment disagrees with quadrature" % (key, rel), dict(g1=g1))
        for k in (1, 2):
            for tg in (0, 1):
                sval = float(sp.N(JT[(k,tg)].subs(subs), 30))
                uu_ = math.atanh(rsamp); c_ = math.sqrt(1-rsamp*rsamp)
                f = lambda w_: (c_*mp.exp(w_))**k * (c_/rsamp)*mp.cosh(w_) * (((3*(c_*mp.sinh(w_)/rsamp)**2-1)/2) if tg else 1)
                nval = mp.quad(f, [-uu_, uu_])
                rel = abs(mp.mpf(sval) - nval)/abs(nval)
                key = "r%.2f_J%d_Q%d" % (rsamp, k, tg)
                g2b[key] = float(rel)
                if rel > 1e-10:
                    finish(1, "G2b FIRED (%s rel %.2e)" % (key, rel), dict(g2b=g2b))
    log("G1/G2b PASS (all sampled rel <= 1e-10)")
    # ---- S5: assemble and close the r-integrals ----
    log("S5: assembling a/b/c r-integrands and integrating term-wise")
    Fa = (m1*J20 + m1q*J21/2)/2 + (m2*J10 + m2q*J11/2)/2   # AMENDMENT 2: c00f = W2^2/2
    Fb = (m3*J20 + m3q*J21/2)/2 + m4*J10 + m4q*J11/2
    def rint(expr):
        e = sp.expand(sp.expand_log(expr.rewrite(sp.log), force=True))
        e = e.subs(sp.log(1-rr**2), sp.log(1-rr)+sp.log(1+rr))
        e = sp.expand(e)
        tot = sp.Integer(0)
        cache = {}
        for term in sp.Add.make_args(e):
            key = sp.srepr(term)[:120]
            if key in cache: tot += cache[key]; continue
            iv = sp.simplify(sp.integrate(term, (rr, 0, 1)))
            cache[key] = iv; tot += iv
        return sp.simplify(sp.nsimplify(tot, [sp.log(2), sp.pi**2, sp.zeta(3)], rational=False, tolerance=sp.Float('1e-11')))
    a_sym = sp.simplify(rint(sp.expand(rr**2*Fa)*sp.Rational(3,2)))
    log("S5: a_sym = %s" % a_sym)
    b_sym = sp.simplify(rint(sp.expand(rr**2*(rr**2*Fa + Fb))*sp.Rational(3,2)))
    log("S5: b_sym = %s" % b_sym)
    c_sym = sp.simplify(rint(sp.expand(rr**4*Fb)*sp.Rational(3,2)))
    log("S5: c_sym = %s" % c_sym)
    sym["a"], sym["b"], sym["c"] = sp.sstr(a_sym), sp.sstr(b_sym), sp.sstr(c_sym)
    # ---- G3: symbolic vs numeric pipeline ----
    g3 = {}
    for k_, vs_ in (("a", a_sym), ("b", b_sym), ("c", c_sym)):
        ref = float(abc2["abc".index(k_)])
        val = float(sp.N(vs_, 30))
        rel = abs(val - ref)/abs(ref)
        g3[k_] = dict(sym=val, num=ref, rel=float(rel))
        log("G3: %s: symbolic %.12f vs numeric %.12f rel %.2e" % (k_, val, ref, rel))
        if rel > 1e-9:
            sym["status"] = "CLOSED-MISMATCH"
            finish(1, "G3 FIRED at %s (rel %.2e): symbolic closure disagrees with the independent numeric pipeline" % (k_, rel), dict(g3=g3, sym=sym))
    sym["status"] = "CLOSED"
    log("G3 PASS: symbolic closure agrees with numeric pipeline at <= 1e-9")
except Exception as e:
    sym["status"] = "OPEN (%s: %s)" % (e.__class__.__name__, e)
    sym["notes"].append(repr(e)[:400])
    log("S4/S5: symbolic leg did NOT close: %r" % (e,))

# ---- G4: closed vs E2Q1 stored fit ----
log("G4: closed (a,b,c) vs E2Q1 stored fit")
g4 = {}
if sym["status"] == "CLOSED":
    import sympy as sp
    for k_ in "abc":
        val = float(sp.N(sym[k_], 30))
        z = (val - stored[k_])/stored["s"+k_]
        g4[k_] = dict(closed=val, stored=stored[k_], z=float(z))
        log("G4: %s: closed %.9f vs stored %.9f +- %.9f  z=%.2f" % (k_, val, stored[k_], stored["s"+k_], z))
        if abs(z) > 3:
            finish(1, "G4 FIRED at %s (z=%.2f)" % (k_, z), dict(g4=g4, sym=sym))
    log("G4 PASS")
else:
    log("G4 SKIPPED (no symbolic closure)")

# ---- G5: fresh MC of the ORIGINAL estimator vs a + b q + c q^2 ----
log("G5: fresh MC seed 20261001, n=2e6 x 4 dipole, q in {0,3,10}")
def dipole_sample(rng, m):
    out = np.empty(m); todo = np.arange(m)
    while len(todo):
        mm = rng.uniform(-1, 1, len(todo))
        take = rng.random(len(todo)) < (1 + mm*mm)/2
        out[todo[take]] = mm[take]; todo = todo[~take]
    return out
rng = np.random.default_rng(20261001)
NE, NU1, CH = 2_000_000, 4, 500_000
QS5 = [0.0, 3.0, 10.0]
acc = {qq: [0.0, 0.0, 0] for qq in QS5}
done = 0
if sym["status"] == "CLOSED":
    import sympy as sp
    A_B, B_B, C_B = (float(sp.N(sym[k], 30)) for k in "abc")
else:
    A_B, B_B, C_B = (float(v) for v in abc2)
while done < NE:
    n = min(CH, NE - done); done += n
    d0 = rng.normal(size=(n,3)); d0 /= np.linalg.norm(d0, axis=1)[:,None]
    p = d0 * rng.random(n)[:,None]**(1/3)
    du = rng.normal(size=(n,3)); u = du/np.linalg.norm(du, axis=1)[:,None]
    z_ = np.sum(p*u, axis=1); r2n = np.sum(p*p, axis=1)
    Wn = -z_ + np.sqrt(np.maximum(z_*z_ - r2n + 1.0, 0.0))
    S = rng.random(n)*Wn
    p1 = p + S[:,None]*u
    r12n = np.sum(p1*p1, axis=1)
    mu = dipole_sample(rng, n*NU1).reshape(n, NU1)
    phi = rng.uniform(0, 2*np.pi, (n, NU1))
    ax_ = np.where(np.abs(u[:,0:1]) < 0.9, np.array([1.0,0,0]), np.array([0,1.0,0]))*np.ones((n,3))
    e1 = np.cross(u, ax_); e1 /= np.linalg.norm(e1, axis=1)[:,None]
    e2 = np.cross(u, e1)
    u1 = (mu[...,None]*u[:,None,:] + np.sqrt(1-mu*mu)[...,None]*(np.cos(phi)[...,None]*e1[:,None,:] + np.sin(phi)[...,None]*e2[:,None,:]))
    pd2n = np.sum(p1[:,None,:]*u1, axis=2)
    disc = pd2n*pd2n - r12n[:,None] + 1.0
    W2 = -pd2n + np.sqrt(np.maximum(disc, 0.0))
    a1n = r2n + 2*z_*S + S*S
    A2n = r12n[:,None]*W2 + pd2n*W2**2 + W2**3/3
    c0qf = r12n[:,None]*W2**2/2 + 2*pd2n*W2**3/3 + W2**4/4
    c00f = W2**2/2
    K2q0 = W2
    for qq in QS5:
        k1q = 1 + qq*a1n
        K2tot = K2q0 + qq*A2n
        c0f_  = c00f + qq*c0qf
        G = S[:,None]*K2tot + c0f_
        X = Wn*k1q*G.mean(axis=1)
        s1_ = float(X.sum()); s2_ = float((X*X).sum())
        acc[qq][0] += s1_; acc[qq][1] += s2_; acc[qq][2] += n
    log("G5: chunk done (%d/%d)" % (done, NE))
g5 = {}
for qq in QS5:
    s1_, s2_, n_ = acc[qq]
    m_ = s1_/n_; var = (s2_ - n_*m_*m_)/(n_-1); se_ = float(np.sqrt(var/n_))
    pred = A_B + B_B*qq + C_B*qq*qq
    z = (m_ - pred)/se_
    g5[str(qq)] = dict(mc=m_, se=se_, pred=pred, z=float(z))
    log("G5: q=%g: MC %.6f +- %.6f vs closed %.6f  z=%.2f" % (qq, m_, se_, pred, z))
    if abs(z) > 3:
        finish(1, "G5 FIRED at q=%g (z=%.2f): closed (a,b,c) fails fresh MC" % (qq, z), dict(g5=g5, sym=sym))
log("G5 PASS")

# ---- verdict ----
if sym["status"] == "CLOSED":
    finish(0, "BANKED: exact closed forms of (a,b,c) for E2(q); G0/G0b/G1/G2/G2b/G3/G4/G5 all PASS",
           dict(symbolic=sym, g0=g0, g0b=g0b, g1_size=len(g1), g2=g2, g2b_size=len(g2b), g4=g4, g5=g5, rule_dev=rule_dev))
else:
    finish(1, "PARTIAL: numeric (a,b,c) certified by G0/G0b/G2/G5 but the exact-symbolic leg stayed OPEN (%s)" % sym["status"],
           dict(symbolic=sym, g0=g0, g0b=g0b, g2=g2, g5=g5, rule_dev=rule_dev, numeric=abc2.tolist()))
