#!/usr/bin/env python3
"""
A10 -- Can ONE first-principles statement give BOTH framework postulates?

  P1 : a0 = (1/2) c sqrt(G rho_DE)
  P2 : g_N = g^2 / (g + a0)                    (simple / Langmuir kernel)

Candidate principles evaluated (BRIEF, lane A10):
  (i)   FINITE INFORMATION CAPACITY       -- de Sitter horizon stores S = pi/(G H^2) nats;
                                             one nat per cell per e-fold fixes a0.
  (ii)  MAXIMUM ENTROPY AT A FIXED MOMENT -- does a fixed moment give Langmuir vs quadrature?
  (iii) SATURATION OF A CONSERVED CURRENT -- j saturates at a0; derive the relation and solve it.

Chosen: (iii) for the response law, (i) only for the scale.  Both are tested exactly.

The kernel family is the repo's own (AG6B FROZEN_CRITERIA Sec.1):
      R_b(u) = u^2 / (a0 - b u),   u = g - g_N,   s = g_N/a0,   uhat = u/a0
      <=>  uhat^2 + b * s * uhat = s
b = 1 is P2 (Langmuir / pumped two-level cells, AG6B C-1);
b = 2 is the quadrature a0-line (Deser-Levin, AG6B E-1).

Run:  python3 a10_checks.py            -> prints one line per check, writes a10_results.json
      python3 a10_checks.py --mutate   -> must FAIL (proves the checks have teeth)
Exit 0 iff every declared check passes.  Deterministic, no network, < 10 s.
"""
import os
import re
import sys
import glob
import json
import math
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
MUTATE = ('--mutate' in sys.argv) or (os.environ.get('A10_MUTATE') == '1')

# ---------------------------------------------------------------- constants (BRIEF Sec.4)
c      = 2.99792458e8
G      = 6.67430e-11
H0     = 2.1843e-18
LAM    = 1.0890e-52
RHO_DE = 5.831e-27
A0_CAN = 9.36e-11
A0_ALT = 1.13e-10
KPC    = 3.0856775814913673e19
KAPPA_CAN = 0.5
H_LAM  = c * math.sqrt(LAM / 3.0)          # de Sitter / Lambda Hubble rate, s^-1
CONSTANTS_USED = [
    "c=2.99792458e8 m/s (BRIEF S4)",
    "G=6.67430e-11 (BRIEF S4)",
    "H0=2.1843e-18 s^-1 (BRIEF S4)",
    "Lambda=1.0890e-52 m^-2 (BRIEF S4)",
    "rho_DE=5.831e-27 kg/m^3 (BRIEF S4)",
    "a0_can=9.36e-11 m/s^2 (BRIEF S4, INPUT)",
    "a0_alt=1.13e-10 m/s^2 (BRIEF S4, INPUT)",
    "kappa_can=0.5 (BRIEF S4, FITTED)",
    "kpc=3.0856775814913673e19 m (BRIEF S4)",
    "EARTH_LIMIT read at runtime from real_research/reviews/mi_disformal_tail_freedom_2026.py",
    "AG6B in_family/n_cap/n1 read at runtime from argon_push/AG6B_.../ag6b_media_results.json",
    "SPARC rotmod curves read from real_research/data/sparc_data/*_rotmod.dat (175 files)",
]

checks = []
def chk(cid, ok, measured, threshold, note, value=None):
    checks.append(dict(id=cid, **{'pass': bool(ok)},
                       value=(float(value) if value is not None else None),
                       measured=str(measured), threshold=str(threshold), note=note))
    print("  [%s] %-4s %s  |  THRESHOLD: %s  |  %s"
          % ('PASS' if ok else 'FAIL', cid, measured, threshold, note))
    return ok

def head(t):
    print("\n" + t)

print("A10 -- one principle for two postulates: exact test of candidates (i)/(ii)/(iii)")
print("a0_can = %.4e m/s^2 (INPUT, BRIEF Sec.4);  kappa = %.2f FITTED;  footings never pooled"
      % (A0_CAN, KAPPA_CAN))
print("mutate = %s" % MUTATE)

# =====================================================================
head("S1  THE FAMILY: eliminate u between the saturation law and g = g_N + u")
# =====================================================================
a0, u, s, g, bsym = sp.symbols('a_0 u s g b', positive=True)

def kernel(bval):
    """g_N(g) from eliminating u between  s = u^2/(a0-b u)  and  g = s+u."""
    expr = sp.expand((g - u) * (a0 - bval * u) - u ** 2)
    roots = sp.solve(sp.Eq(expr, 0), u)
    good = [r for r in roots if sp.simplify(r.subs(g, 0)) == 0]
    assert len(good) == 1, roots
    return sp.simplify(g - good[0])

def uhat_of(bv, sv=s):
    """positive root of uhat^2 + bv*sv*uhat - sv = 0, in closed form
    (sp.solve will not return roots of a symbol declared positive)."""
    return (sp.sqrt(bv ** 2 * sv ** 2 + 4 * sv) - bv * sv) / 2

def uhat_np(bv, sv):
    """the same root, numpy-vectorised."""
    sv = np.asarray(sv, dtype=float)
    return (np.sqrt(bv ** 2 * sv ** 2 + 4 * sv) - bv * sv) / 2

gN2 = kernel(2)
P2_target = g ** 2 / (g + a0)
quad_target = (sp.sqrt(a0 ** 2 + 4 * g ** 2) - a0) / 2

b_used = 2 if MUTATE else 1        # MUTATION: claim the b=2 member IS P2
res1 = sp.simplify(kernel(b_used) - P2_target)
chk("K1", res1 == 0, "|b=%d kernel - g^2/(g+a0)| = %s" % (b_used, res1),
    "identically 0 (sympy simplify)", "b=1 is exactly P2; b=2 is not", value=0.0 if res1 == 0 else 1.0)

res2 = sp.simplify(gN2 - quad_target)
chk("K2", res2 == 0, "|b=2 kernel - (sqrt(a0^2+4g^2)-a0)/2| = %s" % res2,
    "identically 0 (sympy simplify)", "b=2 is exactly the quadrature a0-line",
    value=0.0 if res2 == 0 else 1.0)

gg = sp.symbols('gN', positive=True)
x1 = sp.simplify(sp.solve(sp.Eq(gg, g ** 2 / (g + a0)), g)[-1])
x2 = sp.simplify(sp.solve(sp.Eq(gg ** 2 + a0 * gg - g ** 2, 0), g)[0])
ok3 = (sp.simplify(x1 - (gg / 2) * (1 + sp.sqrt(1 + 4 * a0 / gg))) == 0 and
       sp.simplify(x2 - sp.sqrt(gg ** 2 + a0 * gg)) == 0)
chk("K3", ok3, "g(b=1)=(gN/2)(1+sqrt(1+4a0/gN)); g(b=2)=sqrt(gN^2+a0 gN)",
    "both identities exact", "the kernels differ only by the cross term u^2+b*u*s=s",
    value=0.0 if ok3 else 1.0)
print("      family:  uhat^2 + b*s*uhat - s = 0 ,  uhat=(g-gN)/a0 ,  s=gN/a0")

# =====================================================================
head("S2  DEEP LIMIT and CAPACITY are b-INDEPENDENT: what saturation alone cannot fix")
# =====================================================================
t = sp.symbols('t', positive=True)
Acoef = {}
for bv in (1, 2, 3):
    xhat = sp.simplify(s + uhat_of(bv))
    ser = sp.series(xhat.subs(s, t ** 2), t, 0, 3).removeO()
    Acoef[bv] = sp.nsimplify(sp.expand(ser).coeff(t, 2))
ok4 = (Acoef[1] == sp.Rational(1, 2)) and (Acoef[2] == 0) and (Acoef[3] == sp.Rational(-1, 2))
chk("K4", ok4, "deep coeff A(b)=(1-b/2): %s" % {k: str(v) for k, v in Acoef.items()},
    "A(1)=1/2, A(2)=0, A(3)=-1/2",
    "g/sqrt(a0 gN) = 1 + (1-b/2)sqrt(gN/a0) + O(gN/a0)", value=float(Acoef[1]))

deep = {}
for bv in (1, 2, 3):
    deep[bv] = sp.limit(uhat_of(bv) ** 2 / s, s, 0)
ok5 = all(sp.simplify(deep[bv] - 1) == 0 for bv in (1, 2, 3))
chk("K5", ok5, "lim (g-gN)^2/(a0 gN) = %s for b=1,2,3" % {k: str(v) for k, v in deep.items()},
    "all equal 1", "deep limit common to the whole family -> cannot select b", value=1.0)

cap = {}
for bv in (1, 2, 3):
    cap[bv] = sp.limit(uhat_of(bv), s, sp.oo)
ok6 = all(sp.simplify(cap[bv] - sp.Rational(1, bv)) == 0 for bv in (1, 2, 3))
chk("K6", ok6, "sup_u (g-gN)/a0 = %s" % {k: str(v) for k, v in cap.items()},
    "= 1/b exactly", "capacity a0/b: b=1 -> a0 (P2), b=2 -> a0/2 (quadrature)",
    value=float(cap[1]))

sv = np.logspace(-6, 6, 4001)
for bv in (1, 2):
    uh = (-bv * sv + np.sqrt(bv ** 2 * sv ** 2 + 4 * sv)) / 2
    assert np.all(np.diff(uh) > 0) and np.all(uh < 1.0 / bv + 1e-12)
print("      monotone rise to the capacity verified on 4001 points, b=1,2")

# =====================================================================
head("S3  STRONG-FIELD TAIL: constant anomalous acceleration = a0/b  (a NEW number)")
# =====================================================================
tail = {}
for bv in (1, 2):
    xh = s + uhat_of(bv)
    tail[bv] = sp.limit(s * (sp.simplify(xh / s) - 1), s, sp.oo)
ok7 = (tail[1] == 1) and (tail[2] == sp.Rational(1, 2))
chk("K7", ok7, "lim_{y->inf} y(nu-1) = %s (b=1), %s (b=2)" % (tail[1], tail[2]),
    "= 1/b exactly", "constant anomaly a0/b, not a decaying one", value=float(tail[1]))

lim_src = os.path.join(REPO, 'real_research', 'reviews', 'mi_disformal_tail_freedom_2026.py')
earth = float('nan')
if os.path.exists(lim_src):
    mm = re.search(r'EARTH_LIMIT\s*=\s*([0-9.eE+-]+)', open(lim_src).read())
    if mm:
        earth = float(mm.group(1))
ratio_q = (A0_CAN / 2) / earth
ratio_s = A0_CAN / earth
chk("K8", (abs(ratio_q - 1279.0) / 1279.0 < 1e-2) and (abs(ratio_s / ratio_q - 2) < 1e-12),
    "a0/2 / EARTH_LIMIT = %.2f (registered 1279); a0 / EARTH_LIMIT = %.2f" % (ratio_q, ratio_s),
    "|ratio_q-1279|/1279<1e-2 and ratio_s/ratio_q=2",
    "reproduces the registered quadrature number; CANONICAL law is 2x worse (2557)",
    value=ratio_s)

# =====================================================================
head("S4  (i) FINITE CAPACITY: what a cell count can and cannot give for kappa")
# =====================================================================
kap = lambda N: sp.sqrt(8 * sp.pi / 3) / N
counts = [('4 pi (full horizon sphere)', 4 * sp.pi),
          ('2 pi (modular / one-sided)', 2 * sp.pi),
          ('pi (hemisphere)', sp.pi),
          ('1 (surface gravity / Unruh)', sp.Integer(1))]
kvals = {}
for name, N in counts:
    kvals[name] = float(kap(N).evalf())
N_can = sp.simplify(sp.sqrt(8 * sp.pi / 3) / sp.Rational(1, 2))
print("      kappa(N)=sqrt(8 pi/3)/N ;  kappa=1/2 needs N = 2 sqrt(8 pi/3) = %.6f"
      % float(N_can.evalf()))
for name, N in counts:
    print("        N = %-32s kappa = %.6f" % (name, kvals[name]))
k2pi = kvals['2 pi (modular / one-sided)']
nearest = min(abs(v - KAPPA_CAN) / KAPPA_CAN for v in kvals.values())
chk("K9", nearest > 0.01,
    "min_N |kappa(N)-1/2|/(1/2) = %.4f at kappa(2pi)=%.6f ; N(1/2)=%.4f"
    % (nearest, k2pi, float(N_can.evalf())),
    "> 0.01 (no admissible count gives 1/2)",
    "nearest count is %.1f%% away; the required count 2sqrt(8pi/3) is not a count"
    % (100 * nearest),
    value=nearest)

r_req = sp.simplify(sp.Rational(1, 2) / sp.sqrt(8 * sp.pi / 3))
irr = (sp.sqrt(8 * sp.pi / 3).is_rational is False) and (r_req.is_rational is False)
best = (9e9, 0, 0)
for q in range(1, 2001):
    p = int(round(q * float(r_req)))
    best = min(best, (abs(float(r_req.evalf()) - p / q), q, p))
chk("K10", irr,
    "sqrt(8pi/3).is_rational=%s ; r=kappa/sqrt(8pi/3)=%.6f is_rational=%s"
    % (sp.sqrt(8 * sp.pi / 3).is_rational, float(r_req.evalf()), r_req.is_rational),
    "both irrational (sympy assumption; proof via Lindemann)",
    "no RATIONAL cell count turns cH into (1/2)c sqrt(G rho): kappa=1/2 is a convention",
    value=float(r_req.evalf()))
print("        control (not a proof): best p/q with q<=2000 is %d/%d, residual %.1e" % (best[2], best[1], best[0]))

Z = 2 * sp.sqrt(8 * sp.pi / 3)
ok11 = (abs(float(Z.evalf()) - 5.788810) < 1e-6) and (Z.is_rational is False)
chk("K11", ok11,
    "Z=2sqrt(8pi/3)=%.6f ; 2Z=%.6f ; Z.is_rational=%s"
    % (float(Z.evalf()), float(2 * Z.evalf()), Z.is_rational),
    "|Z-5.788810|<1e-6 and Z irrational",
    "'1/12 of the horizon' is 2Z=11.5776, not 12 -> the twelfth is not a count",
    value=float(Z.evalf()))

# =====================================================================
head("S5  (ii) MAXIMUM ENTROPY AT A FIXED MOMENT: does it land on either kernel?")
# =====================================================================
ag6b = os.path.join(REPO, 'argon_push', 'AG6B_saturating_vacuum_microphysics',
                    'ag6b_media_results.json')
cand = json.load(open(ag6b))['candidates'] if os.path.exists(ag6b) else {}
rows = {}
for k in ('C-1', 'E-1', 'F-1', 'F-2'):
    if k in cand:
        rows[k] = (cand[k].get('in_family'), str(cand[k].get('n_cap')), str(cand[k].get('n1')))
ok12 = (rows.get('F-1', (None,))[0] is False) and (rows.get('F-2', (None,))[0] is False)
chk("K12", ok12,
    "AG6B in_family: C-1=%s E-1=%s F-1(MaxEnt <c>)=%s n_cap=%s n1=%s F-2(MaxEnt <c^2>)=%s n_cap=%s"
    % (rows.get('C-1', ('?',))[0], rows.get('E-1', ('?',))[0],
       rows.get('F-1', ('?',))[0], rows.get('F-1', ('?', '?', '?'))[1], rows.get('F-1', ('?', '?', '?'))[2],
       rows.get('F-2', ('?',))[0], rows.get('F-2', ('?', '?', '?'))[1]),
    "both MaxEnt rows out of family (False)",
    "neither fixed-mean nor fixed-variance MaxEnt gives Langmuir or the quadrature -> (ii) dead",
    value=1.0 if ok12 else 0.0)

n_ = sp.symbols('n', integer=True, nonnegative=True)
lam = sp.symbols('lam', positive=True)
pmf = sp.exp(-lam) * lam ** n_ / sp.factorial(n_)
m2v = sp.summation(n_ ** 2 * pmf, (n_, 0, sp.oo))
ok13 = sp.simplify(m2v - (lam ** 2 + lam)) == 0
chk("K13", ok13, "<n^2>_Poisson = %s  vs  quadrature x^2 = s(s+1)" % sp.simplify(m2v),
    "<n^2> = lam^2+lam exactly",
    "quadrature = SECOND moment of a Poisson cell (moment identity, not MaxEnt)",
    value=0.0 if ok13 else 1.0)

# =====================================================================
head("S6  NEW CONSEQUENCE: cross-regime relation A = 1 - 1/(2T) and its SPARC reach")
# =====================================================================
bb = sp.symbols('b', positive=True)
rel = sp.simplify((1 - bb / 2) - (1 - 1 / (2 * (1 / bb))))
chk("K14", rel == 0, "A(b) - (1 - 1/(2T(b))) = %s  with A=1-b/2, T=1/b" % rel,
    "identically 0", "the family ties deep shape to the Solar-System anomaly: one number b",
    value=0.0 if rel == 0 else 1.0)

paths = sorted(glob.glob(os.path.join(REPO, 'real_research', 'data', 'sparc_data', '*_rotmod.dat')))
sparc = {}
for f in paths:
    d = np.genfromtxt(f, comments='#')
    if d.ndim == 2 and len(d):
        sparc[os.path.basename(f)] = d
names = sorted(sparc)

def rar(ups):
    S_, X_, D_ = [], [], []
    for nm in names:
        d = sparc[nm]
        r = d[:, 0] * KPC
        vo, vg, vd, vb = d[:, 1] * 1e3, d[:, 3] * 1e3, d[:, 4] * 1e3, d[:, 5] * 1e3
        gb = (vg ** 2 + ups * vd ** 2 + 1.4 * ups * vb ** 2) / r
        go = vo ** 2 / r
        mk = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go)
        S_.append(gb[mk]); X_.append(go[mk]); D_.append(ups * vd[mk] ** 2 / (gb[mk] * r[mk]))
    S_, X_, D_ = (np.concatenate(z) for z in (S_, X_, D_))
    return S_, X_, D_

Ameas, Aerr = {}, {}
for ups in (0.5, 0.7):
    s_, x_, _ = rar(ups)
    sa = s_ / A0_CAN
    Bo = x_ / np.sqrt(A0_CAN * s_)
    mk = (sa < 0.2) & np.isfinite(Bo)
    xx = np.sqrt(sa[mk]); yy = Bo[mk] - 1
    with np.errstate(all='ignore'):          # numpy reports sticky FPU flags from earlier divides
        Ameas[ups] = float((xx @ yy) / (xx @ xx))
        rng = np.random.default_rng(20261021)
        boots = [float((xx[i] @ yy[i]) / (xx[i] @ xx[i]))
                 for i in (rng.integers(0, len(xx), len(xx)) for _ in range(200))]
    Aerr[ups] = float(np.std(boots))
swing = abs(Ameas[0.7] - Ameas[0.5])
chk("K15", swing > 0.5,
    "A_hat(Ups=0.5)=%.3f+-%.3f  A_hat(Ups=0.7)=%.3f+-%.3f  swing=%.3f (b=1->0.5, b=2->0.0)"
    % (Ameas[0.5], Aerr[0.5], Ameas[0.7], Aerr[0.7], swing),
    "swing > 0.5 (the whole b1-b2 separation)",
    "the Upsilon systematic alone exceeds the b=1 vs b=2 separation", value=swing)

dAdU = (Ameas[0.7] - Ameas[0.5]) / 0.2
dU_req = 0.5 / (3 * abs(dAdU))
chk("K16", dU_req < 0.10,
    "dA/dUps=%.2f ; dUps needed for 3sigma on the b-split = %.3f ; SPARC band 0.50-0.80"
    % (dAdU, dU_req),
    "dUps_req < 0.10 (existing band insufficient)",
    "short by a factor %.1f: the deep-limit shape cannot decide b on SPARC" % (0.10 / dU_req),
    value=dU_req)

# the capacity bound as a data test: where b=1 and b=2 differ, how big is the Upsilon lever arm?
med_d, sep_bin = {}, None
for ups in (0.5, 0.7):
    s_, x_, _ = rar(ups)
    dd = (x_ - s_) / A0_CAN
    bnd = (s_ / A0_CAN > 3) & (s_ / A0_CAN < 10)
    med_d[ups] = float(np.median(dd[bnd]))
    if sep_bin is None:
        sv_ = s_[bnd] / A0_CAN
        sep_bin = float(np.mean(uhat_np(1, sv_) - uhat_np(2, sv_)))
lever = abs(med_d[0.7] - med_d[0.5]) / 0.2                 # a0 per unit Upsilon
dU_req_d = sep_bin / (3 * lever)
chk("K17", dU_req_d < 0.10,
    "s in (3,10)a0: median d(Ups=0.5)=%+.2f, (Ups=0.7)=%+.2f -> lever %.2f a0/Ups ; "
    "b-split %.2f a0 ; dUps_req(3sig)=%.3f"
    % (med_d[0.5], med_d[0.7], lever, sep_bin, dU_req_d),
    "dUps_req < 0.10 (existing Upsilon band insufficient)",
    "sup(g-gN)=a0/b is exact but needs Upsilon to +-%.2f to be seen" % dU_req_d,
    value=dU_req_d)
s6, x6, _ = rar(0.6)
d6 = (x6 - s6) / A0_CAN
print("      SPARC: %d galaxies, %d points (Ups=0.6); max observed (g_obs-g_bar)/a0 = %.1f"
      % (len(names), len(s6), float(np.max(d6))))

# =====================================================================
head("S7  P1 ROUND TRIP, both footings, and the horizon ratio")
# =====================================================================
a0_from_kappa = KAPPA_CAN * c * math.sqrt(G * RHO_DE)
a0_from_lam = c ** 2 * math.sqrt(LAM / (32 * math.pi))
chk("K18", abs(a0_from_kappa - A0_CAN) / A0_CAN < 3e-3 and abs(a0_from_lam - A0_CAN) / A0_CAN < 3e-3,
    "kappa*c*sqrt(G rho_DE)=%.4e ; c^2 sqrt(Lam/32pi)=%.4e ; target %.4e"
    % (a0_from_kappa, a0_from_lam, A0_CAN),
    "both within 0.3% of 9.36e-11",
    "P1 is one algebraic statement with two normalisations; the 1/2 IS the content",
    value=a0_from_lam)
cHL = c * H_LAM
print("      cH_Lambda = %.5e m/s^2 ; a0/(cH_Lambda) canonical = %.6f (BRIEF 0.172747; the 6e-4"
      " difference is a0_can=9.36e-11 vs the Lambda-derived 9.3542e-11), alt = %.6f"
      % (cHL, A0_CAN / cHL, A0_ALT / cHL))
for foot, a0f in (('canonical', A0_CAN), ('alt', A0_ALT)):
    print("      %-9s: a0=%.4e  a0/(cH_L)=%.4f  cH_L/a0=%.4f  a0/EARTH_LIMIT=%.1f"
          % (foot, a0f, a0f / cHL, cHL / a0f, a0f / earth))

# =====================================================================
head("S8  STATUS OF EACH CANDIDATE")
# =====================================================================
print("      (i)  PARTIAL: a0 ~ c sqrt(G rho) forced by dimensions; coefficient kappa NOT (K9-K11).")
print("      (ii) DEAD: neither fixed-moment MaxEnt family is in the kernel family (K12);")
print("                the quadrature is a Poisson second-moment identity, not MaxEnt (K13).")
print("      (iii) STRONGEST: gives the whole family + deep limit, but b is free (K4-K6);")
print("                b=1 (=P2) needs the extra single-quantum clause.")
print("      VERDICT: NO-GO(obstruction). P2 is DERIVED as the b=1 member; P1's coefficient")
print("      cannot come from any cell count, because kappa/sqrt(8pi/3) is irrational (K10).")

if MUTATE:
    # M1: flip the tail coefficient of b=1  (K7's claim must break)
    tail[1] = sp.Rational(1, 2)
    chk("M1", tail[1] == 1, "mutated tail coeff b=1 -> %s" % tail[1], "must equal 1",
        "MUTATION: flipping the tail coefficient", value=0.5)
    # M2: claim the 2pi cell count gives kappa = 1/2 exactly  (K9's claim must break)
    chk("M2", abs(k2pi - 0.5) < 1e-6, "mutated claim kappa(2pi)=%.6f == 1/2" % k2pi,
        "must equal 0.5 to 1e-6", "MUTATION: asserting the count lands on 1/2", value=k2pi)
    # M3: claim the b=2 capacity is a0 (not a0/2)  (K6's claim must break)
    chk("M3", abs(float(cap[2]) - 1.0) < 1e-12, "mutated claim capacity(b=2)=%s a0" % cap[2],
        "must equal 1 a0", "MUTATION: asserting the quadrature capacity is a0", value=float(cap[2]))

npass = sum(1 for cc in checks if cc['pass'])
print("\nA10 COMPLETE: %d/%d checks PASS." % (npass, len(checks)))

out = dict(
    lane="A10_first_principles",
    status="NO-GO(obstruction)",
    claim=("No single first-principles statement yields both P1 and P2. The saturating-current "
           "principle gives P2 exactly as the b=1 member of gN=u^2/(a0-b u); P1's coefficient "
           "cannot come from any rational cell count on the de Sitter horizon because "
           "kappa/sqrt(8pi/3) is irrational."),
    checks=[dict(id=cc['id'], **{'pass': cc['pass']}, value=cc['value'],
                 measured=cc['measured'], threshold=cc['threshold'], note=cc['note'])
            for cc in checks],
    numbers=dict(kappa_counts=kvals, kappa_required_count=float(N_can.evalf()),
                 kappa_nearest_rel=nearest, kappa_2pi_dev_rel=abs(k2pi - KAPPA_CAN) / KAPPA_CAN,
                 kappa_at_integer_counts={str(N): float(kap(sp.Integer(N)).evalf()) for N in range(1, 7)},
                 kappa_spread_factor=max(kvals.values()) / min(kvals.values()),
                 Z=float(Z.evalf()), two_Z=float(2 * Z.evalf()),
                 kappa_ratio_irrational=float(r_req.evalf()),
                 deep_coeff={str(k): str(v) for k, v in Acoef.items()},
                 capacity={str(k): str(v) for k, v in cap.items()},
                 tail={str(k): str(v) for k, v in tail.items()},
                 earth_limit=earth, a0_half=float(A0_CAN / 2), ratio_a0_2_over_limit=ratio_q,
                 ratio_a0_over_limit=ratio_s, anomaly_canonical_over_quad=ratio_s / ratio_q,
                 A=Ameas, A_err=Aerr, A_swing=swing, dA_dUps=dAdU, dUps_required=dU_req,
                 sparc_galaxies=len(names), sparc_points=int(len(s6)),
                 max_d_obs=float(np.max(d6)), sep_bin=sep_bin, ups_lever=lever,
                 dUps_required_capacity=dU_req_d, med_d=med_d,
                 cH_Lambda=float(cHL), a0_over_cHL_can=float(A0_CAN / cHL),
                 a0_over_cHL_alt=float(A0_ALT / cHL),
                 a0_from_kappa=float(a0_from_kappa), a0_from_lambda=float(a0_from_lam)),
    mutate=MUTATE,
    constants_used=CONSTANTS_USED,
    # transcribed, not computed here: provenance is named for each entry
    external_inputs=dict(
        ag6b_rms_n1_can=0.100908, ag6b_rms_n2_can=0.108272,
        ag6b_source="argon_push/AG6B_saturating_vacuum_microphysics/ag6b_sparc.out (global Upsilon 0.60)",
        brief_paired_rms_n1=0.220, brief_paired_rms_n2=0.178,
        brief_source="FRAMEWORK_EQUATIONS_2026-10-15.md Sec.1 'Open law-form split (AG3)'",
        brief_y_t_range=[94, 129],
        ups_gas=1.33, ups_bul_factor=1.4,
        sparc_convention="SPARC rotmod: g_bar=(Vgas^2+Ups*Vdisk^2+1.4*Ups*Vbul^2)/r, g_obs=Vobs^2/r",
    ),
)
with open(os.path.join(HERE, 'a10_results_MUTATE.json' if MUTATE else 'a10_results.json'), 'w') as fh:
    json.dump(out, fh, indent=1)

sys.exit(0 if npass == len(checks) else 1)
