#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mi_orbital_unruh_gems_2026.py -- GEMS/embedding lane for the orbital dS-Unruh programme.

LANE (a): circular worldline in the M5 embedding of dS4, built from static-patch
          coordinates; unit normalization, stationarity, (DX)^2(s) derived from scratch
          and compared against the brief's stated closed form.
LANE (b): identities A^2 h^2 - R^2 w^2 = 1 ; a5^2 = A^2 h^4 + R^2 w^4 ;
          GEMS a^2 = a5^2 - H^2 proved via the normal-component argument (the normal
          part of the 5-acceleration is H for ANY worldline on the hyperboloid) AND
          independently via the intrinsic static-coordinate Christoffel computation;
          static limit = pure hyperbolic worldline with alpha = H/N0 (why Deser-Levin
          is exact there).
LANE (c): TORSION-BLINDNESS THEOREM -- the s^4 coefficient of (DX)^2 is a5^2/12 =
          (a^2+H^2)/12 EXACTLY for the orbit, so any second-moment (Luo-type)
          functional is blind to orbit-vs-line at leading order.  The s^6 coefficient
          (where the Frenet torsion first enters) is computed exactly and sized at
          galactic v -- that size is the honest measure of how protected the
          second-moment reading is.
LANE (d): the three limit forms (Omega=0 hyperbolic; H->0 Letaw flat circular with
          w -> gamma*Omega; small-s), plus the exact (R,Omega) <-> (a,v,H) dictionary
          the compute lane needs for its grids.

PRIOR ART (credited per corpus rule; none of the geometry here is new):
 * GEMS mapping, static dS temperature: Deser & Levin, CQG 14 (1997) L163;
   Deser & Levin, PRD 59 (1999) 064004 (a5^2 = a^2 + H^2 for embedded worldlines).
 * Flat-space stationary/circular detector response: Letaw, PRD 23 (1981) 1709;
   Bell & Leinaas, NPB 212 (1983) 131.
 * Stationary worldlines in dS via the embedding, with effective temperatures:
   Good, Juarez-Aubry, Moustos, Temirkhan, JHEP 06 (2020) 059 [arXiv:2004.03974].
   The closed interval form verified below very likely appears in their stationary-dS
   classification; any write-up MUST check their equations before claiming novelty.
 * Hyperbolic balance sqrt(a^2+H^2)-H and q=2: Milgrom, PLA 253 (1999) 273 (Eq 9
   kernel credit per the corpus's standing wellhead-credit rule).
 * kappa = 1/2pi: Milgrom 2020.  The framework's kappa = 1/2 remains FITTED, NOT
   DERIVED; nothing in this lane changes that standing.

Conventions: c = 1, signature (-,+,+,+,+) (mostly-plus, timelike (DX)^2 < 0).
All symbolic checks are exact sympy; numerics are mpmath at 60 digits (no float64
anywhere a result is load-bearing).
"""

import sys
import sympy as sp
import mpmath as mp

mp.mp.dps = 60

n_pass = 0
n_fail = 0


def check(name, cond, detail=""):
    global n_pass, n_fail
    tag = "[OK]  " if cond else "[FAIL]"
    if cond:
        n_pass += 1
    else:
        n_fail += 1
    print(f"{tag} {name}" + (f"  -- {detail}" if detail else ""))


ETA5 = [-1, 1, 1, 1, 1]
ETA4 = [-1, 1, 1, 1]


def mdot(u, v, eta=ETA5):
    return sum(eta[i] * u[i] * v[i] for i in range(len(eta)))


def is_zero(expr, subs_list=None, tol="1e-40"):
    """Exact-zero test: try simplification; if inconclusive, evaluate at fixed
    rational sample points at 60 digits (polynomial-identity-testing style).
    Returns (bool, detail)."""
    e = sp.simplify(expr)
    if e == 0:
        return True, "simplified to 0 exactly"
    if subs_list is None:
        return False, f"did not simplify to 0: {e}"
    worst = 0
    for sub in subs_list:
        v = abs(complex(sp.N(expr.subs(sub), 60)))
        worst = max(worst, v)
    return worst < float(tol), f"max |expr| over {len(subs_list)} rational points = {worst:.3e}"


# ----------------------------------------------------------------------------------
# Symbols.  Two levels:
#   generic level: (Asym, hsym, wsym, Rsym) free -- fast trig/hyperbolic identities;
#   physical level: A = sqrt(1/H^2 - R^2), h = H/N, w = Omega/N,
#                   N = sqrt(1 - H^2 R^2 - R^2 Omega^2).
# ----------------------------------------------------------------------------------
t, tau, tau1, tau2, s, lam = sp.symbols('t tau tau1 tau2 s lambda', real=True)
H, R, Om = sp.symbols('H R Omega', positive=True)
Asym, hsym, wsym, Rsym = sp.symbols('A h w Rs', positive=True)

Nexpr = sp.sqrt(1 - H**2 * R**2 - R**2 * Om**2)
Aexpr = sp.sqrt(1 / H**2 - R**2)
hexpr = H / Nexpr
wexpr = Om / Nexpr

PHYS = {Asym: Aexpr, hsym: hexpr, wsym: wexpr, Rsym: R}
# constraint-only substitution at the generic level: A^2 h^2 - R^2 w^2 = 1
CONSTR = {Asym: sp.sqrt(1 + Rsym**2 * wsym**2) / hsym}

# rational sample points satisfying 1 - H^2 R^2 - R^2 Om^2 > 0
SAMPLES = [
    {H: sp.Rational(1), R: sp.Rational(1, 3), Om: sp.Rational(2, 5)},
    {H: sp.Rational(1, 2), R: sp.Rational(1, 2), Om: sp.Rational(1, 3)},
    {H: sp.Rational(3, 2), R: sp.Rational(1, 4), Om: sp.Rational(1, 2)},
    {H: sp.Rational(2), R: sp.Rational(1, 5), Om: sp.Rational(3, 4)},
]
SAMPLES_S = [{**d, s: sp.Rational(3, 7)} for d in SAMPLES] + \
            [{**SAMPLES[0], s: sp.Rational(-5, 11)}]

print("=" * 88)
print("SECTION A -- the worldline in the embedding, and the interval (DX)^2(s)")
print("=" * 88)

# (a) coordinate-time form of the worldline (static patch: rho=R, theta=pi/2, phi=Om t)
Xt = [Aexpr * sp.sinh(H * t),
      R * sp.cos(Om * t),
      R * sp.sin(Om * t),
      sp.Integer(0),
      Aexpr * sp.cosh(H * t)]

ok, d = is_zero(mdot(Xt, Xt) - 1 / H**2)
check("A1 worldline lies on the hyperboloid X.X = 1/H^2", ok, d)

dXt = [sp.diff(c, t) for c in Xt]
ok, d = is_zero(mdot(dXt, dXt) + Nexpr**2)
check("A2 pullback: (dX/dt).(dX/dt) = -N^2, N^2 = 1 - H^2R^2 - R^2Om^2 (dtau = N dt)", ok, d)

# proper-time parametrization at the generic level
Xg = [Asym * sp.sinh(hsym * tau),
      Rsym * sp.cos(wsym * tau),
      Rsym * sp.sin(wsym * tau),
      sp.Integer(0),
      Asym * sp.cosh(hsym * tau)]
dXg = [sp.diff(c, tau) for c in Xg]

norm_generic = sp.simplify(mdot(dXg, dXg))        # = R^2 w^2 - A^2 h^2
ok, d = is_zero(norm_generic.subs(CONSTR) + 1)
check("A3 unit normalization Xdot.Xdot = -1  (given A^2h^2 - R^2w^2 = 1)", ok, d)

ok, d = is_zero((Asym**2 * hsym**2 - Rsym**2 * wsym**2 - 1).subs(PHYS), SAMPLES)
check("A4 the constraint A^2h^2 - R^2w^2 = 1 HOLDS for the physical A,h,w,N", ok, d)

# the two-point interval, derived from scratch, vs the brief's closed form
DXv = [Xg[i].subs(tau, tau2) - Xg[i].subs(tau, tau1) for i in range(5)]
interval_2pt = mdot(DXv, DXv)
closed_form_g = 4 * Rsym**2 * sp.sin(wsym * (tau2 - tau1) / 2)**2 \
    - 4 * Asym**2 * sp.sinh(hsym * (tau2 - tau1) / 2)**2
diffAB = sp.expand((interval_2pt - closed_form_g).rewrite(sp.exp))
ok, d = is_zero(diffAB)
check("A5 (DX)^2 = 4R^2 sin^2(w s/2) - 4A^2 sinh^2(h s/2), s = tau2-tau1 "
      "(brief's form CONFIRMED; depends on s only => stationary)", ok, d)

# numeric spot check of the closed form against the raw embedding difference
def interval_direct_num(Hv, Rv, Omv, t1v, t2v):
    Nv = mp.sqrt(1 - (Hv * Rv)**2 - (Rv * Omv)**2)
    Av = mp.sqrt(1 / Hv**2 - Rv**2)
    hv, wv = Hv / Nv, Omv / Nv
    X = lambda u: [Av * mp.sinh(hv * u), Rv * mp.cos(wv * u),
                   Rv * mp.sin(wv * u), mp.mpf(0), Av * mp.cosh(hv * u)]
    d5 = [X(t2v)[i] - X(t1v)[i] for i in range(5)]
    return -d5[0]**2 + d5[1]**2 + d5[2]**2 + d5[3]**2 + d5[4]**2

Hv, Rv, Omv = mp.mpf(1), mp.mpf(1) / 3, mp.mpf(2) / 5
t1v, t2v = mp.mpf("0.31"), mp.mpf("1.27")
Nv = mp.sqrt(1 - (Hv * Rv)**2 - (Rv * Omv)**2)
Av = mp.sqrt(1 / Hv**2 - Rv**2)
hv, wv = Hv / Nv, Omv / Nv
sv = t2v - t1v
cf = 4 * Rv**2 * mp.sin(wv * sv / 2)**2 - 4 * Av**2 * mp.sinh(hv * sv / 2)**2
di = interval_direct_num(Hv, Rv, Omv, t1v, t2v)
ok = abs(cf - di) / abs(di) < mp.mpf("1e-45")
check("A6 numeric spot (60 dps): closed form == raw embedding difference",
      ok, f"rel diff = {mp.nstr(abs(cf-di)/abs(di), 3)}")

print()
print("=" * 88)
print("SECTION B -- the identities and the GEMS relation")
print("=" * 88)

ddXg = [sp.diff(c, tau, 2) for c in Xg]
a5sq_generic = sp.simplify(mdot(ddXg, ddXg))
ok, d = is_zero(a5sq_generic - (Asym**2 * hsym**4 + Rsym**2 * wsym**4))
check("B1 5-acceleration: a5^2 = Xdd.Xdd = A^2 h^4 + R^2 w^4", ok, d)

a5sq_phys = (Asym**2 * hsym**4 + Rsym**2 * wsym**4).subs(PHYS)
a5sq_closed = ((1 - H**2 * R**2) * H**2 + R**2 * Om**4) / Nexpr**4
ok, d = is_zero(a5sq_phys - a5sq_closed, SAMPLES)
check("B2 physical closed form: a5^2 = [(1-H^2R^2) H^2 + R^2 Om^4] / N^4", ok, d)

# --- GEMS normal-component argument -------------------------------------------------
# On X.X = 1/H^2:  d/dtau(X.X)=0 => X.Xdot = 0 ;  d/dtau(X.Xdot)=0 => X.Xdd = -Xdot.Xdot.
# Unit-speed (Xdot.Xdot = -1) gives X.Xdd = +1, i.e. Xdd.n = H with n = H X the unit
# spacelike normal (n.n = H^2 X.X = 1).  So the NORMAL part of the 5-acceleration is H
# for ANY worldline on the hyperboloid; the tangential part is the intrinsic dS
# 4-acceleration, and orthogonality gives a5^2 = a^2 + H^2.
rho_f = sp.Function('rho')(lam)
th_f = sp.Function('theta')(lam)
ph_f = sp.Function('phi')(lam)
t_f = sp.Function('tt')(lam)
Xgen = [sp.sqrt(1 / H**2 - rho_f**2) * sp.sinh(H * t_f),
        rho_f * sp.sin(th_f) * sp.cos(ph_f),
        rho_f * sp.sin(th_f) * sp.sin(ph_f),
        rho_f * sp.cos(th_f),
        sp.sqrt(1 / H**2 - rho_f**2) * sp.cosh(H * t_f)]
ok, d = is_zero(mdot(Xgen, Xgen) - 1 / H**2)
check("B3 GENERIC static-patch curve (any rho,theta,phi,t of lambda) lies on X.X = 1/H^2 "
      "(the two-derivative chain then forces Xdd.n = H for ANY unit-speed worldline)", ok, d)

# numeric confirmation of X.X'' = -X'.X' on a wiggly NON-stationary curve (any param)
def wiggly(lv):
    lv = mp.mpf(lv)
    rho = mp.mpf("0.31") + mp.mpf("0.07") * mp.sin(mp.mpf("1.3") * lv)
    th = mp.mpf("1.1") + mp.mpf("0.2") * mp.cos(mp.mpf("0.6") * lv)
    ph = mp.mpf("0.9") * lv + mp.mpf("0.15") * mp.sin(mp.mpf("2.1") * lv)
    tt = mp.mpf("1.2") * lv + mp.mpf("0.1") * mp.cos(mp.mpf("0.8") * lv)
    q = mp.sqrt(1 - rho**2)  # H = 1
    return [q * mp.sinh(tt), rho * mp.sin(th) * mp.cos(ph),
            rho * mp.sin(th) * mp.sin(ph), rho * mp.cos(th), q * mp.cosh(tt)]

worst = mp.mpf(0)
for lv in ("0.2", "0.7", "1.5"):
    val = mp.mpf(0)
    for i in range(5):
        f_i = lambda u, j=i: wiggly(u)[j]
        X0 = f_i(mp.mpf(lv))
        X1 = mp.diff(f_i, mp.mpf(lv))
        X2 = mp.diff(f_i, mp.mpf(lv), 2)
        val += ETA5[i] * (X0 * X2 + X1 * X1)
    worst = max(worst, abs(val))
check("B4 numeric (60 dps): X.X'' + X'.X' = 0 on a wiggly non-stationary hyperboloid "
      "curve at 3 points (normal 5-acceleration = H for ANY worldline)",
      worst < mp.mpf("1e-25"), f"max |X.X'' + X'.X'| = {mp.nstr(worst, 3)}")

# on the circular worldline itself, with the constraint: Xdd.X = +1  (=> Xdd.n = H)
XddX = mdot([c.subs(PHYS) for c in ddXg], [c.subs(PHYS) for c in Xg])
ok, d = is_zero(XddX - 1, [{**sub, tau: sp.Rational(2, 7)} for sub in SAMPLES])
check("B5 circular worldline: Xdd.X = 1 exactly, i.e. Xdd.n = H", ok, d)

# projection: |a_tan|^2 = a5^2 - H^2, with n = H X the unit normal
XddX_g = mdot(ddXg, Xg)                          # generic; equals (1/H) * (Xdd.n)
a_tan = [ddXg[i] - (H**2 * XddX_g) * Xg[i] for i in range(5)]  # Xdd - (Xdd.n) n
atan2 = mdot(a_tan, a_tan).subs(PHYS)
ok, d = is_zero(sp.simplify(atan2 - (a5sq_phys - H**2)),
                [{**sub, tau: sp.Rational(2, 7)} for sub in SAMPLES])
check("B6 tangential projection: |Xdd - (Xdd.n) n|^2 = a5^2 - H^2 (GEMS split)", ok, d)

# --- intrinsic check: static-coordinate Christoffels ---------------------------------
tt_c, rho_c, th_c, ph_c = sp.symbols('t_c rho_c theta_c phi_c', real=True)
coords = (tt_c, rho_c, th_c, ph_c)
f_c = 1 - H**2 * rho_c**2
g = sp.diag(-f_c, 1 / f_c, rho_c**2, rho_c**2 * sp.sin(th_c)**2)
ginv = g.inv()
Gam = [[[sp.simplify(sum(ginv[m, k] * (sp.diff(g[k, i], coords[j]) +
                                       sp.diff(g[k, j], coords[i]) -
                                       sp.diff(g[i, j], coords[k])) / 2
                         for k in range(4)))
         for j in range(4)] for i in range(4)] for m in range(4)]
u_up = [1 / Nexpr, 0, 0, Om / Nexpr]             # constant components along the orbit
acc_up = [sp.simplify(sum(Gam[m][i][j] * u_up[i] * u_up[j]
                          for i in range(4) for j in range(4)))
          for m in range(4)]
at_pt = {rho_c: R, th_c: sp.pi / 2}
a2_int = sp.simplify(sum(g[m, m].subs(at_pt) * acc_up[m].subs(at_pt)**2 for m in range(4)))
a2_closed = (1 - H**2 * R**2) * R**2 * (H**2 + Om**2)**2 / Nexpr**4
ok, d = is_zero(a2_int - a2_closed, SAMPLES)
check("B7 INTRINSIC 4-acceleration (Christoffels, from scratch): "
      "a^2 = (1-H^2R^2) R^2 (H^2+Om^2)^2 / N^4", ok, d)

ok, d = is_zero(a2_int - (a5sq_phys - H**2), SAMPLES)
check("B8 GEMS RELATION: intrinsic a^2 = a5^2 - H^2 (independent routes agree)", ok, d)

# --- static limit --------------------------------------------------------------------
Ah_static = (Aexpr * hexpr).subs(Om, 0)
ok, d = is_zero(sp.simplify(Ah_static - 1))
check("B9 static limit Om=0: A*h = 1 exactly => worldline is PURE HYPERBOLIC, "
      "X0 = (1/alpha) sinh(alpha tau), alpha = H/N0, N0 = sqrt(1-H^2R^2)", ok, d)

a2_static = a2_closed.subs(Om, 0)
ok, d = is_zero(sp.sqrt(a2_static + H**2) * sp.sqrt(1 - H**2 * R**2) - H, SAMPLES)
check("B10 static limit: sqrt(a^2 + H^2) = H/N0 -- alpha/2pi is exactly the "
      "Deser-Levin 1997 Tolman-shifted Gibbons-Hawking temperature (anchor A1 basis)",
      ok, d)

print()
print("=" * 88)
print("SECTION C -- torsion-blindness theorem and where torsion first enters")
print("=" * 88)

F_s = 4 * Rsym**2 * sp.sin(wsym * s / 2)**2 - 4 * Asym**2 * sp.sinh(hsym * s / 2)**2
ser = sp.expand(sp.series(F_s, s, 0, 10).removeO())
c = {k: ser.coeff(s, k) for k in range(2, 10)}

odd_ok = all(sp.simplify(c[k]) == 0 for k in (3, 5, 7))
check("C1 odd coefficients s^3, s^5, s^7 each vanish (stationarity/evenness)", odd_ok,
      "all three are identically 0" if odd_ok else f"{[sp.simplify(c[k]) for k in (3,5,7)]}")

ok, d = is_zero(c[2].subs(CONSTR) + 1)
check("C2 s^2 coefficient = -1 under the constraint (unit-speed)", ok, d)

ok, d = is_zero(c[4] + a5sq_generic / 12)
check("C3 THEOREM: s^4 coefficient = -a5^2/12 EXACTLY, a5^2 = A^2h^4 + R^2w^4 "
      "= a^2 + H^2.  Any second-moment (Luo-type) functional is therefore "
      "orbit-vs-line BLIND at this order and inherits the hyperbolic q = 2", ok, d)

ok, d = is_zero(c[6] - (Rsym**2 * wsym**6 - Asym**2 * hsym**6) / 360)
check("C4 s^6 coefficient of (DX)^2 = (R^2w^6 - A^2h^6)/360 (torsion enters here)", ok, d)

ok, d = is_zero(c[8] + (Rsym**2 * wsym**8 + Asym**2 * hsym**8) / 20160)
check("C5 s^8 coefficient of (DX)^2 = -(R^2w^8 + A^2h^8)/20160", ok, d)

# independent derivative-combinatorics route (no series command):
X3 = [sp.diff(cmp_, tau, 3) for cmp_ in Xg]
X4 = [sp.diff(cmp_, tau, 4) for cmp_ in Xg]
X5 = [sp.diff(cmp_, tau, 5) for cmp_ in Xg]
c4_alt = sp.simplify(mdot(ddXg, ddXg) / 4 + mdot(dXg, X3) / 3)
c6_alt = sp.simplify(mdot(X3, X3) / 36 + mdot(ddXg, X4) / 24 + mdot(dXg, X5) / 60)
ok1, d1 = is_zero(c4_alt - c[4])
ok2, d2 = is_zero(c6_alt - c[6])
check("C6 independent route (Taylor of DX, term-by-term dot products): "
      "s^4 coeff = Xdd.Xdd/4 + Xd.X3/3 and s^6 coeff = X3.X3/36 + Xdd.X4/24 + Xd.X5/60 "
      "both MATCH the series", ok1 and ok2, d1 if not ok1 else d2)

# Frenet torsion: |X3|^2 = kappa^2 tau1^2 - kappa^4  =>  tau1^2 = (|X3|^2 + kappa^4)/kappa^2
X3sq = sp.simplify(mdot(X3, X3))
tau1sq = sp.simplify((X3sq + a5sq_generic**2) / a5sq_generic)
tau1sq_closed = Asym**2 * Rsym**2 * hsym**2 * wsym**2 * (hsym**2 + wsym**2)**2 / a5sq_generic
ok, d = is_zero((tau1sq - tau1sq_closed).subs(CONSTR),
                [{Rsym: sp.Rational(1, 3), wsym: sp.Rational(2, 5), hsym: sp.Rational(5, 4),
                  tau: sp.Rational(2, 7)},
                 {Rsym: sp.Rational(1, 2), wsym: sp.Rational(1, 3), hsym: sp.Rational(7, 5),
                  tau: sp.Rational(2, 7)}])
check("C7 Frenet torsion closed form: tau1 = A R h w (h^2+w^2)/a5 "
      "(under the unit-speed constraint)", ok, d)

# flat limit of the torsion: tau1 -> gamma^2 Omega (Letaw's circular value)
tau1sq_phys = tau1sq_closed.subs(PHYS)
tau1sq_flat = sp.limit(tau1sq_phys, H, 0)
ok, d = is_zero(sp.simplify(tau1sq_flat - Om**2 / (1 - R**2 * Om**2)**2))
check("C8 flat limit: tau1 -> gamma^2 Omega, gamma = 1/sqrt(1-R^2Om^2) "
      "(Letaw 1981 circular Frenet torsion)", ok, d)

# physical (a, H, v) closed form for the s^6 bracket coefficient
# bracket convention: (DX)^2 = -s^2 [ 1 + (a5^2/12) s^2 + C6 s^4 + C8 s^6 + ... ]
C6_g = (Asym**2 * hsym**6 - Rsym**2 * wsym**6) / 360
v_expr = R * Om / sp.sqrt(1 - H**2 * R**2)
gam2 = 1 / (1 - v_expr**2)
C6_phys_target = gam2**3 * (H**4 / (1 - H**2 * R**2)**2 - v_expr**6 / R**4) / 360
ok, d = is_zero(C6_g.subs(PHYS) - C6_phys_target, SAMPLES)
check("C9 C6 in physical variables: C6 = gamma^6 [H^4/(1-H^2R^2)^2 - v^6/R^4]/360, "
      "v = R Om/sqrt(1-H^2R^2)  (leading order: C6 = (H^4 - a^4/v^2)/360)", ok, d)

# N^2 = (1-H^2R^2)(1-v^2) and a5^2 = gamma^4 (H^2/(1-H^2R^2) + v^4/R^2)
ok1, d1 = is_zero(Nexpr**2 - (1 - H**2 * R**2) * (1 - v_expr**2), SAMPLES)
ok2, d2 = is_zero(a5sq_phys - gam2**2 * (H**2 / (1 - H**2 * R**2) + v_expr**4 / R**2),
                  SAMPLES)
check("C10 local-speed dictionary: N^2 = (1-H^2R^2)(1-v^2) and "
      "a5^2 = gamma^4 [H^2/(1-H^2R^2) + v^4/R^2]", ok1 and ok2, d1 if not ok1 else d2)

# ---- numeric sizing of the torsion window at galactic parameters --------------------
def solve_R_Om(a_over_H, v, Hn=mp.mpf(1)):
    """Exact inversion: y = (H R)^2 is the stable small root of
    Aq y^2 + Bq y + Cq = 0, Aq=(1-v^2)^2(1+ahat^2), Bq=(1-v^2)(2v^2-ahat^2(1-v^2)),
    Cq=v^4;  then Omega = v sqrt(1-y)/R."""
    ahat, v = mp.mpf(a_over_H), mp.mpf(v)
    Aq = (1 - v**2)**2 * (1 + ahat**2)
    Bq = (1 - v**2) * (2 * v**2 - ahat**2 * (1 - v**2))
    Cq = v**4
    disc = Bq**2 - 4 * Aq * Cq
    y = 2 * Cq / (-Bq + mp.sqrt(disc))
    Rn = mp.sqrt(y) / Hn
    Omn = v * mp.sqrt(1 - y) / Rn
    return Rn, Omn

def phys_num(Hn, Rn, Omn):
    Nn = mp.sqrt(1 - (Hn * Rn)**2 - (Rn * Omn)**2)
    An = mp.sqrt(1 / Hn**2 - Rn**2)
    return Nn, An, Hn / Nn, Omn / Nn

# exact-inversion round trip at the compute lane's grid corners
worst = mp.mpf(0)
for ah in ("0.01", "1", "1000"):
    for vv in ("1e-4", "1e-3"):
        Rn, Omn = solve_R_Om(mp.mpf(ah), mp.mpf(vv))
        Nn, An, hn, wn = phys_num(mp.mpf(1), Rn, Omn)
        a_rec = mp.sqrt(1 - Rn**2) * Rn * (1 + Omn**2) / Nn**2   # H = 1
        worst = max(worst, abs(a_rec - mp.mpf(ah)) / mp.mpf(ah))
check("C11 exact (a,v,H)->(R,Omega) inversion round-trips at 6 grid corners "
      "(a/H in {0.01,1,1000} x v in {1e-4,1e-3})", worst < mp.mpf("1e-40"),
      f"max rel err = {mp.nstr(worst, 3)}")

Rn, Omn = solve_R_Om(mp.mpf(1000), mp.mpf("1e-3"))
ok = abs(Rn - mp.mpf("1e-6") / 1000) / (mp.mpf("1e-6") / 1000) < mp.mpf("1e-5")
check("C12 leading-order R = v^2/a confirmed at a/H=1000, v=1e-3 (rel err < 1e-5)",
      ok, f"R = {mp.nstr(Rn, 8)} vs v^2/a = 1e-9")

# torsion ~ a/v at galactic parameters
Rn, Omn = solve_R_Om(mp.mpf(100), mp.mpf("1e-3"))
Nn, An, hn, wn = phys_num(mp.mpf(1), Rn, Omn)
a5sq_n = An**2 * hn**4 + Rn**2 * wn**4
a_n = mp.sqrt(a5sq_n - 1)
tau1_n = An * Rn * hn * wn * (hn**2 + wn**2) / mp.sqrt(a5sq_n)
ok = abs(tau1_n * mp.mpf("1e-3") / a_n - 1) < mp.mpf("1e-3")
check("C13 Frenet torsion tau1 = a/v at galactic parameters (a/H=100, v=1e-3, tol 1e-3)",
      ok, f"tau1*v/a - 1 = {mp.nstr(tau1_n*mp.mpf('1e-3')/a_n - 1, 3)}")

# the honest window: ratio of s^6 to s^4 bracket terms
C6n = (An**2 * hn**6 - Rn**2 * wn**6) / 360
C8n = (An**2 * hn**8 + Rn**2 * wn**8) / 20160
ratio_at = lambda sn: 12 * abs(C6n) * sn**2 / a5sq_n
r_at_a = ratio_at(1 / a_n)          # sampling scale of the self-consistent E* = a
pred = 1 / (30 * mp.mpf("1e-3")**2)
ok = abs(r_at_a / pred - 1) < mp.mpf("1e-3")
check("C14 at s = 1/a (self-consistent E* = a): |s^6 term|/|s^4 term| = 1/(30 v^2) "
      "= 3.33e4 >> 1 -- the short-time expansion has ALREADY FAILED at that scale",
      ok, f"ratio = {mp.nstr(r_at_a, 6)}, prediction 1/(30 v^2) = {mp.nstr(pred, 6)}")

r_at_w = ratio_at(1 / wn)
ok = abs(r_at_w - mp.mpf(1) / 30) / (mp.mpf(1) / 30) < mp.mpf("1e-3")
check("C15 at s = 1/tau1 = v/a (one orbital radian): the ratio is 1/30 -- the "
      "second-moment reading is protected ONLY for s <~ v/a, i.e. E >> Omega = a/v",
      ok, f"ratio = {mp.nstr(r_at_w, 6)}")

# series truncation honesty, both sides of the window
bracket_exact = lambda sn: (4 * An**2 * mp.sinh(hn * sn / 2)**2
                            - 4 * Rn**2 * mp.sin(wn * sn / 2)**2) / sn**2
bracket_S8 = lambda sn: 1 + a5sq_n * sn**2 / 12 + C6n * sn**4 + C8n * sn**6
s0 = mp.mpf(1) / (20 * wn)
err_in = abs(bracket_exact(s0) - bracket_S8(s0))
bound = abs(C8n) * s0**6
ok = mp.mpf(0) < err_in < bound
check("C16 INSIDE the window (s = 1/(20 w)): truncation error < last kept term "
      "(series through s^8 of (DX)^2 is faithful)", ok,
      f"|err| = {mp.nstr(err_in, 3)}, |C8 s^6| = {mp.nstr(bound, 3)}")

s1 = 1 / a_n
err_out = abs(bracket_exact(s1) - bracket_S8(s1)) / abs(bracket_exact(s1))
ok = err_out > 100
check("C17 OUTSIDE the window (s = 1/a): truncated series is off by >100x -- "
      "torsion-blindness does NOT extend to the E* = a sampling scale", ok,
      f"rel truncation error = {mp.nstr(err_out, 3)}")

print()
print("  torsion window vs galactic v  (ratio of s^6 to s^4 term at s = 1/a):")
for vv in ("1e-4", "3e-4", "1e-3"):
    print(f"    v = {vv}:  1/(30 v^2) = {mp.nstr(1/(30*mp.mpf(vv)**2), 4)}")

print()
print("=" * 88)
print("SECTION D -- the three limit forms for the anchors")
print("=" * 88)

# D1: Omega = 0 (anchor A1) -- substitute the PHYSICAL A, h at Om=0 (the equality
# then hinges on the nontrivial fact A0 = 1/h0, so this check can fail):
h0 = H / sp.sqrt(1 - H**2 * R**2)
ok, d = is_zero(sp.simplify(
    closed_form_g.subs(wsym, 0).subs({Asym: Aexpr.subs(Om, 0), hsym: hexpr.subs(Om, 0)})
    + (4 / h0**2) * sp.sinh(h0 * (tau2 - tau1) / 2)**2))
check("D1 Omega=0: (DX)^2 = -(4/alpha^2) sinh^2(alpha s/2), alpha = H/N0 "
      "(pure hyperbolic; Deser-Levin thermality exact -- anchor A1 form)", ok, d)

# D2: H -> 0 (anchor A2): the sinh part -> gamma^2 s^2 / 4 (x4), w -> gamma Omega
sinh_part = (Aexpr**2 * sp.sinh(hexpr * s / 2)**2)
lim_sinh = sp.limit(sinh_part, H, 0)
gam2_flat = 1 / (1 - R**2 * Om**2)
ok1, d1 = is_zero(lim_sinh - gam2_flat * s**2 / 4, SAMPLES_S)
lim_w = sp.limit(wexpr, H, 0)
ok2, d2 = is_zero(lim_w - Om * sp.sqrt(gam2_flat), SAMPLES)
check("D2 H->0: 4A^2 sinh^2(hs/2) -> gamma^2 s^2 and w -> gamma*Omega "
      "=> (DX)^2 -> 4R^2 sin^2(gamma Om s/2) - gamma^2 s^2", ok1 and ok2,
      d1 if not ok1 else d2)

# independently constructed flat circular worldline in M4 (Letaw)
gam = sp.sqrt(gam2_flat)
Y = [gam * tau, R * sp.cos(gam * Om * tau), R * sp.sin(gam * Om * tau), sp.Integer(0)]
DY = [Y[i].subs(tau, tau2) - Y[i].subs(tau, tau1) for i in range(4)]
flat_interval = mdot(DY, DY, ETA4)
flat_target = 4 * R**2 * sp.sin(gam * Om * (tau2 - tau1) / 2)**2 - gam2_flat * (tau2 - tau1)**2
ok, d = is_zero(sp.expand((flat_interval - flat_target).rewrite(sp.exp)))
check("D3 INDEPENDENT M4 construction (t = gamma tau, phi = gamma Om tau): its interval "
      "equals the H->0 limit of the dS closed form (Letaw 1981 / Bell-Leinaas circular)",
      ok, d)

# unit normalization of the flat worldline (guards D3 against a mis-built comparator)
dY = [sp.diff(c, tau) for c in Y]
ok, d = is_zero(sp.simplify(mdot(dY, dY, ETA4) + 1))
check("D4 the M4 comparator worldline is unit-normalized (gamma^2(1 - R^2Om^2) = 1)",
      ok, d)

# D5: flat proper acceleration from our exact a^2: a -> gamma^2 v^2 / R
a2_flat = sp.limit(a2_closed, H, 0)
ok, d = is_zero(sp.simplify(a2_flat - gam2_flat**2 * R**2 * Om**4))
check("D5 H->0 of a^2: a -> gamma^2 R Om^2 = gamma^2 v^2/R (standard flat circular "
      "proper acceleration; anchor A3's a>>H regime connects here)", ok, d)

print()
print("=" * 88)
print(f"RESULT: {n_pass} passed, {n_fail} failed")
print("=" * 88)

print("""
CLOSED FORMS FOR THE COMPUTE LANE (all verified above; c = 1, signature -++++):

  N^2 = 1 - H^2 R^2 - R^2 Omega^2 ;  A^2 = 1/H^2 - R^2 ;  h = H/N ;  w = Omega/N
  (DX)^2(s) = 4 R^2 sin^2(w s/2) - 4 A^2 sinh^2(h s/2)          [CONFIRMED as stated]
  A^2 h^2 - R^2 w^2 = 1                                          [unit normalization]
  a5^2 = A^2 h^4 + R^2 w^4 = [(1-H^2R^2) H^2 + R^2 Omega^4]/N^4
  a^2  = a5^2 - H^2 = (1-H^2R^2) R^2 (H^2+Omega^2)^2 / N^4       [GEMS]
     i.e.  a = sqrt(1-H^2R^2) R (H^2+Omega^2) / N^2

  local speed (static-observer-measured; the definitional choice adopted):
     v = R Omega / sqrt(1-H^2R^2) ,  gamma = 1/sqrt(1-v^2),  N^2 = (1-H^2R^2)(1-v^2)
     a5^2 = gamma^4 [ H^2/(1-H^2R^2) + v^4/R^2 ]

  EXACT grid inversion (a,v,H) -> (R,Omega), ahat = a/H, y = (H R)^2:
     Aq y^2 + Bq y + Cq = 0,  Aq = (1-v^2)^2 (1+ahat^2),
     Bq = (1-v^2)(2v^2 - ahat^2(1-v^2)),  Cq = v^4
     stable physical root:  y = 2 Cq / ( -Bq + sqrt(Bq^2 - 4 Aq Cq) )
     Omega = v sqrt(1-y)/R ;  leading order R = v^2/a, Omega = a/v  [confirmed]

  LIMITS:
   Omega=0 : (DX)^2 = -(4/alpha^2) sinh^2(alpha s/2), alpha = H/sqrt(1-H^2R^2)
             = sqrt(a^2+H^2)  -> exactly thermal, T = alpha/2pi (Deser-Levin; anchor A1)
   H->0    : (DX)^2 = 4R^2 sin^2(gamma Omega s/2) - gamma^2 s^2, w -> gamma Omega
             (Letaw flat circular; anchor A2)
   small s : (DX)^2 = -s^2 [ 1 + (a5^2/12) s^2 + C6 s^4 + C8 s^6 + ... ]
             s^4 coefficient = a5^2/12 = (a^2+H^2)/12 EXACT   [torsion-blind]
             C6 = (A^2h^6 - R^2w^6)/360
                = gamma^6 [H^4/(1-H^2R^2)^2 - v^6/R^4]/360  ~  (H^4 - a^4/v^2)/360
             C8 = (A^2h^8 + R^2w^8)/20160
             Frenet torsion tau1 = A R h w (h^2+w^2)/a5  ~  a/v  (= Omega);
             flat limit gamma^2 Omega (Letaw).

  TORSION-BLINDNESS -- honest scope: the s^4 theorem is EXACT, but the expansion's
  validity window is |s| <~ 1/tau1 = v/a.  At the self-consistent sampling scale
  s ~ 1/a the s^6/s^4 ratio is 1/(30 v^2) (3.3e4 at v=1e-3; 3.3e6 at v=1e-4), so a
  second-moment functional inherits the hyperbolic a_eff^2 = a^2 + H^2 (q = 2) ONLY
  if it weights proper times s << v/a (energies E >> Omega = a/v).  Whether Luo-type
  functionals do so is a property of the FUNCTIONAL, not of the geometry -- the
  compute lane must not quote "torsion-blind" outside that window.
""")

sys.exit(0 if n_fail == 0 else 1)
