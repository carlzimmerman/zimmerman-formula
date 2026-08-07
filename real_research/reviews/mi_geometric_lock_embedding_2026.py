#!/usr/bin/env python3
r"""mi_geometric_lock_embedding_2026.py -- LANE M. Is there a GEOMETRIC construction in de Sitter that FORCES
the inertia floor to be a_0/2 = (1/4) c sqrt(G rho_Lambda) rather than the Gibbons-Hawking c H_Lambda?

THE TARGET, stated exactly.
    k_framework = a_0/2 = (1/4) c sqrt(G rho_Lambda) = (c/4)/t_dyn,  t_dyn = 1/sqrt(G rho_Lambda) = 1.6011e18 s
                = 4.6810e-11 m/s^2   (canonical footing; ALT footing multiplies by 1.2082)
    k_GH        = c H_Lambda = c sqrt(8 pi G rho_Lambda/3) = 5.4194e-10 m/s^2
    ratio       = c H_Lambda/(a_0/2) = 2 Z = 4 sqrt(8 pi/3) = 8 sqrt(6 pi)/3 = 11.577620072932
In the crossover language q = a_0/(c H_Lambda) = 2/r, the framework needs r = 2Z; Milgrom 1999's f = T gives
r = 1, his eq.10 gives r = 2, and the conventional 2 pi a_0 ~ c H_Lambda is r = 4 pi = 12.566371.

WHY THIS LANE EXISTS. The relabelling theorem (Lambda = 8 pi G rho_Lambda/c^2 identically) says any mix of
G rho_Lambda with c^2 Lambda returns one scale times a power of 8 pi and cannot select a coefficient. But the
BOUNDARY of that theorem is favourable: sqrt(G rho_Lambda) is pi-FREE while sqrt(8 pi G rho_Lambda/3) is not. So
a derivation whose ONLY dimensional input is rho_Lambda has no 8 pi to hide in, and would automatically EXCLUDE
c H_Lambda. Lane M searches that one structurally open route inside the Deser-Levin embedding geometry.

*** THE ANSWER, up front: NO. No candidate lock. Three things were established, two of them against interest. ***
 (M1-M2) The embedding's own answer for the floor is c H_Lambda, with coefficient EXACTLY 1 and ZERO free
   choices: a_5^2 = a_intrinsic^2 + H^2 is derived (not assumed) from the hyperboloid's second fundamental form,
   so min over all timelike worldlines of a_5 = H, attained on geodesics. That is the cleanest construction in the
   whole space and it lands on the Gibbons-Hawking value, not on the framework's.
 (M3-M5) A THEOREM that closes a real subclass: every polynomial curvature invariant of dS4 is
   (algebraic) x H^(2w), so every acceleration built from one by taking a rational power and a
   rational-times-pi^integer normalisation has, in rho-language, a coefficient whose SQUARE is
   (algebraic) x pi^(odd). Setting that equal to the RATIONAL target 1/4 would force pi^(odd) algebraic,
   contradicting Lindemann. So NO curvature invariant of dS4, at ANY rational power, with ANY
   rational-times-pi^integer normalisation, can give (1/4) c sqrt(G rho_Lambda). The Frenet curvatures escape the
   theorem only by being orbit-DEPENDENT, which disqualifies them for a universal coefficient.
 (M6-M7) The one genuinely pi-FREE geometric acceleration the search found -- and it is the first the programme
   has had -- is c^2/sqrt(A_horizon) = c sqrt(2 G rho_Lambda/3) = 0.8164965809 c sqrt(G rho_Lambda), pi-free
   because the sphere's 4 pi exactly cancels Friedmann's 8 pi/3 in A = 3c^2/(2 G rho_Lambda). It is an EIGHTH
   local rate, not among the seven already tested. It gives r = 2 sqrt(pi) = 3.544908 EXACTLY, it is ADMISSIBLE
   under mi_r_admissibility_bound_2026.py (r_max = 9.0168), and its independent prediction
   a_0 = c H_Lambda/sqrt(pi) = 3.06e-10 m/s^2 is EXCLUDED by SPARC (3.3x the canonical value, 2.2x outside the
   corpus's own 0.84-1.36e-10 a_0-line box). A real candidate that makes a real prediction and is falsified.
 (M8-M10) To reach the target from the horizon you need the algebraic factor sqrt(6)/16 exactly
   (equivalently 2Z = 16 sqrt(pi/6)). Nothing in dS geometry supplies sqrt(6). And once ARBITRARY algebraic
   normalisations are admitted the construction space hits any positive real, so exact landings are available and
   are pure numerology -- priced here at 4 free choices, one of them continuous.
 (M11) The bar is HIGHER than "force 1/4", which raises the cost of the whole lane: c H_Lambda is
   "c per Hubble time" (coefficient 1) and the target is "c/4 per dynamical time". Even a construction that
   forced the 1/4 would leave the entire factor Z/2 = 2.8944 = t_dyn H_Lambda to the choice of WHICH TIME.

RECONCILIATION with mi_r_admissibility_bound_2026.py (6/6, r_max = 9.0168 excludes r = 2Z): no conflict, because
no lock at 2Z was found. The two results AGREE and both point away from 2Z; the pi-free rate found here, r =
2 sqrt(pi) = 3.5449, sits comfortably inside the admissible range.

MANDATORY CREDIT. nu = sqrt(1+1/y) and the dS-Unruh balance are Milgrom 1999 PLA 253:273 eqs 6-9 (identical
kernel; he fixes a_0_hat = 2 c H_Lambda, r = 1); his eqs 10-11 give a second coefficient (r = 2); Milgrom 2008
sec 7.3.1 notes the mismatch "isn't necessarily meaningful". a_lambda = c^2 sqrt(Lambda/3) is Milgrom 1994
Ann.Phys. 229:384. The five-acceleration a_5^2 = a^2 + H^2 and the circular embedding are Deser & Levin 1997
CQG 14:L163. T = sqrt(a^2 + Lambda/3)/2pi is Narnhofer, Peter & Thirring 1996 IJMPB 10:1507. S = A/4 is
Bekenstein 1973 / Hawking 1975; dS thermodynamics Gibbons & Hawking 1977; holographic equipartition
Padmanabhan 2010. The framework's distinctive content is the COEFFICIENT plus the modified-inertia completion.

kappa = 1/2 is FITTED, NOT DERIVED, and nothing below changes that. Exit 0 = every check held.
No check(True); every condition below can fail, and several were written to fail if a lock existed.
"""
from __future__ import annotations

import math
import sys

import mpmath as mp
import sympy as sp

mp.mp.dps = 50

ok: list[tuple[bool, str]] = []


def check(c, m):
    c = bool(c)
    ok.append((c, m))
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
    return c


def banner(t):
    print("\n" + "=" * 108)
    print(f"  {t}")
    print("=" * 108)


# ---------------------------------------------------------------- exact constants
Z = 2 * sp.sqrt(8 * sp.pi / 3)                    # 5.7888100...
TWOZ = sp.simplify(2 * Z)                         # 11.577620072932...
FOURPI = 4 * sp.pi
C_LIGHT = 2.99792458e8
# canonical footing, as stated in the task
K_FW = 4.6810e-11         # a_0/2 = (1/4) c sqrt(G rho_Lambda)
K_GH = 5.4194e-10         # c H_Lambda
T_DYN = 1.6011e18         # 1/sqrt(G rho_Lambda), seconds
A0_CANON = 2 * K_FW
R_MAX_ADMISSIBLE = 9.0168  # from mi_r_admissibility_bound_2026.py (6/6)


banner("M0  THE TARGET AND ITS FOOTING, PINNED -- a lane that mis-states its own target proves nothing")

print(f"  2Z             = {sp.N(TWOZ, 20)}")
print(f"  4 pi           = {sp.N(FOURPI, 20)}")
print(f"  gap, the task's convention  1 - 2Z/4pi = {float(100*(1 - TWOZ/FOURPI)):.4f} %   <-- ANY 'match' must beat")
print(f"  gap, the other direction    4pi/2Z - 1 = {float(100*(FOURPI/TWOZ - 1)):.4f} %       this or it is not a lock")
print(f"  c H_Lambda/(a_0/2) from the quoted numbers = {K_GH/K_FW:.9f}   vs 2Z = {float(TWOZ):.9f}")
print(f"  (c/4)/t_dyn = {C_LIGHT/4/T_DYN:.6e} m/s^2      vs a_0/2 = {K_FW:.6e} m/s^2")
check(abs(K_GH / K_FW / float(TWOZ) - 1) < 2e-4 and abs(C_LIGHT / 4 / T_DYN / K_FW - 1) < 2e-4,
      f"M0a the three quoted numbers are mutually consistent: c H_Lambda/(a_0/2) = {K_GH/K_FW:.6f} reproduces "
      f"2Z = {float(TWOZ):.6f} to {abs(K_GH/K_FW/float(TWOZ)-1)*100:.4f}%, and (c/4)/t_dyn reproduces a_0/2 to "
      f"{abs(C_LIGHT/4/T_DYN/K_FW-1)*100:.4f}%. So the target really is 'c/4 per dynamical time'")
check(sp.simplify(TWOZ - 8 * sp.sqrt(6 * sp.pi) / 3) == 0 and sp.simplify(Z**2 - 32 * sp.pi / 3) == 0
      and sp.simplify(TWOZ - 4 * sp.sqrt(8 * sp.pi / 3)) == 0,
      f"M0b and 2Z = 4 sqrt(8 pi/3) = 8 sqrt(6 pi)/3 with Z^2 = 32 pi/3, symbolically. The 8 pi/3 is the FRIEDMANN "
      f"factor, so 2Z is '4 over the root of Friedmann' -- which is exactly why the target, read the other way, is "
      f"pi-FREE: (1/4) sqrt(G rho) carries no pi at all")


banner("M1  THE DESER-LEVIN EMBEDDING, SET UP EXPLICITLY AND VERIFIED (no step assumed)")

tau, R, w, H = sp.symbols("tau R w H", positive=True)
# de Sitter as the hyperboloid X.X = ell^2 = 1/H^2 in flat M^{3,1} (a planar circular orbit of dS4 lies in a dS3)
Aa = sp.sqrt(1 / H**2 - R**2)                      # A^2 + R^2 = H^-2
hh = sp.sqrt(1 + R**2 * w**2) / Aa                 # A^2 h^2 - R^2 w^2 = 1
X = sp.Matrix([Aa * sp.sinh(hh * tau), Aa * sp.cosh(hh * tau), R * sp.cos(w * tau), R * sp.sin(w * tau)])
eta = sp.diag(-1, 1, 1, 1)


def dot(a, b):
    return sp.simplify(sp.expand_trig(sp.simplify((a.T * eta * b)[0, 0])))


u = X.diff(tau)
Xpp = u.diff(tau)
print("  X = (A sinh(h tau), A cosh(h tau), R cos(w tau), R sin(w tau)),  A^2+R^2 = H^-2,  A^2 h^2 - R^2 w^2 = 1")
print(f"    X.X            = {dot(X, X)}          (must be 1/H^2: on the hyperboloid)")
print(f"    u.u            = {dot(u, u)}                (must be -1: proper time)")
print(f"    a_5.u          = {dot(Xpp, u)}                 (must be 0)")
a5sq = dot(Xpp, Xpp)
a5sq_target = Aa**2 * hh**4 + R**2 * w**4
print(f"    a_5^2          = {sp.simplify(a5sq)}")
print(f"    A^2 h^4 + R^2 w^4 - a_5^2 = {sp.simplify(a5sq_target - a5sq)}")
check(sp.simplify(dot(X, X) - 1 / H**2) == 0 and dot(u, u) == -1 and dot(Xpp, u) == 0
      and sp.simplify(a5sq_target - a5sq) == 0,
      f"M1a the embedding closes on all four counts SYMBOLICALLY: X.X = 1/H^2, u.u = -1, a_5.u = 0, and "
      f"a_5^2 = A^2 h^4 + R^2 w^4 exactly -- Deser & Levin 1997 CQG 14:L163 reproduced, so the geometry this lane "
      f"searches is the right one and not a mis-transcription")

# the second fundamental form does the work: N = X/ell is the unit spacelike normal, X''.N = 1/ell = H
N = X / (1 / H)
a_intr = sp.simplify(Xpp - X * H**2)               # X'' - X/ell^2 : the INTRINSIC (dS-covariant) acceleration
print(f"\n    unit normal N = H X,  N.N = {dot(N, N)},   X''.N = {sp.simplify(dot(Xpp, N))}   (= H, from X.X'' = -u.u = 1)")
print(f"    a_intr.u = {dot(a_intr, u)},  a_intr.X = {dot(a_intr, X)}   (tangent to the hyperboloid)")
aintr_sq = dot(a_intr, a_intr)
print(f"    a_intr^2 = {sp.simplify(aintr_sq)}")
print(f"    a_5^2 - a_intr^2 - H^2 = {sp.simplify(a5sq - aintr_sq - H**2)}")
check(dot(N, N) == 1 and sp.simplify(dot(Xpp, N) - H) == 0 and dot(a_intr, u) == 0 and dot(a_intr, X) == 0
      and sp.simplify(a5sq - aintr_sq - H**2) == 0,
      f"M1b *** a_5^2 = a_intrinsic^2 + H^2 is DERIVED, not assumed: the hyperboloid's second fundamental form "
      f"gives X''.N = 1/ell = H identically (from X.X'' = -u.u = 1), so the normal part of the flat-space "
      f"acceleration is H for EVERY timelike worldline and the tangential part is the dS proper acceleration ***")
check(sp.simplify(sp.factor(aintr_sq) - R**2 * (w**2 + H**2)**2 / (1 - H**2 * R**2)) == 0
      and sp.simplify(aintr_sq.subs(R, 0)) == 0,
      f"M1c and the closed form is |a| = R(w^2+H^2)/sqrt(1-H^2 R^2), which at w = 0 reduces to the textbook static "
      f"-patch proper acceleration H^2 r/sqrt(1-H^2 r^2) and vanishes at R = 0. Anchored on a known case")


banner("M2  THE FLOOR THE GEOMETRY ITSELF PICKS -- and it is c H_Lambda, coefficient EXACTLY 1, zero free choices")

print("  a_5^2 - H^2 = a_intr^2 >= 0 identically, with equality iff a_intr = 0 (a geodesic). So")
print("      min over ALL timelike worldlines of a_5  =  H   exactly,   attained on geodesics.")
print(f"  In the orbit family: a_5^2 - H^2 = {sp.simplify(sp.factor(aintr_sq))}, zero only at R = 0.")
check(sp.simplify(a5sq.subs(R, 0) - H**2) == 0 and sp.simplify(aintr_sq.subs(R, 0)) == 0
      and sp.simplify(sp.factor(aintr_sq)) != 0,
      f"M2a *** AGAINST INTEREST, and it is the strongest single item in this lane: the embedding's OWN inertia "
      f"floor is the five-acceleration of a geodesic, which is H with coefficient EXACTLY 1 and ZERO free choices "
      f"-- i.e. c H_Lambda, the Gibbons-Hawking value, NOT (1/4) c sqrt(G rho_Lambda). Every construction below "
      f"has to beat a zero-parameter competitor that already lands on the rival coefficient ***")

# Frenet apparatus, intrinsic to dS: projected covariant derivative along u
def nabla_u(V):
    return sp.simplify(V.diff(tau) + dot(V, u) * X * H**2)


e0 = sp.simplify(u)
D0 = nabla_u(e0)
kap1 = sp.simplify(sp.sqrt(sp.factor(dot(D0, D0))))
e1 = sp.simplify(D0 / kap1)
D1 = nabla_u(e1)
t1v = sp.simplify(D1 - kap1 * e0)
kap2 = sp.simplify(sp.sqrt(sp.factor(dot(t1v, t1v))))
e2 = sp.simplify(t1v / kap2)
D2 = nabla_u(e2)
t2v = sp.simplify(D2 + kap2 * e1)
kap3sq = sp.simplify(dot(t2v, t2v))
vel = sp.simplify(R * w / (Aa * hh))               # local proper 3-velocity; gamma = A h
print(f"\n  Frenet curvatures of the circular dS worldline (intrinsic, ell = 1/H):")
print(f"    kappa_1 (= |a|)   = {sp.simplify(kap1)}")
gam_dS = sp.simplify(Aa * hh)                      # Lorentz factor of the orbiting observer, = sqrt(1+R^2 w^2)
print(f"    kappa_2 (torsion) = {sp.simplify(kap2)}")
print(f"                      [ = w gamma/sqrt(1-H^2R^2) = w h/H,  gamma = A h = sqrt(1+R^2w^2) ]")
print(f"    kappa_3^2         = {kap3sq}")
print(f"    v/c               = {vel}    (gamma = A h)")
print(f"    kappa_1/kappa_2   = {sp.simplify(kap1/kap2)}  = (v/c)(1 + H^2/w^2)")
# compare SQUARES: both sides are manifestly positive inside the horizon (H R < 1), and sympy will not combine
# sqrt(-1/(HR-1))/sqrt(HR+1) with 1/sqrt(1-H^2R^2) without that assumption -- squaring makes it a rational identity.
id_k2a = sp.simplify(kap2**2 - (w * gam_dS)**2 / (1 - H**2 * R**2))
id_k2b = sp.simplify(kap2**2 - (hh * w / H)**2)
id_k1 = sp.simplify(kap1**2 - aintr_sq)
num_ok = True
for hv, rv, wv in ((sp.Rational(1), sp.Rational(1, 2), sp.Rational(1)),
                   (sp.Rational(3), sp.Rational(1, 5), sp.Rational(7, 2)),
                   (sp.Rational(1, 4), sp.Rational(2), sp.Rational(9, 10))):
    sb = {H: hv, R: rv, w: wv}
    if hv * rv >= 1:
        num_ok = False
    lhs = mp.mpf(str(sp.N(kap2.subs(sb), 40)))
    rhs = mp.mpf(str(sp.N((w * gam_dS / sp.sqrt(1 - H**2 * R**2)).subs(sb), 40)))
    num_ok &= (abs(lhs - rhs) < mp.mpf("1e-35"))
print(f"    squared identities: kappa_2^2 residuals {id_k2a}, {id_k2b};  kappa_1^2 residual {id_k1}")
print(f"    40-digit numeric spot check of the un-squared torsion at 3 interior points: {num_ok}")
check(sp.simplify(gam_dS - sp.sqrt(1 + R**2 * w**2)) == 0
      and id_k2a == 0 and id_k2b == 0 and id_k1 == 0 and num_ok
      and kap3sq == 0,
      f"M2b the Frenet apparatus closes exactly: kappa_1 = |a|, the torsion is "
      f"kappa_2 = w gamma/sqrt(1-H^2R^2) = h w/H with gamma = A h = sqrt(1+R^2w^2), and kappa_3 = 0 -- the "
      f"worldline is a two-curvature helix lying in a 3-plane. NOTE, an error this check caught and the reason it "
      f"is written with H symbolic: a first pass set H = 1 and read the torsion off as 'h w', losing a factor of H. "
      f"Setting the only scale to 1 destroys exactly the information this lane is about. The check fails if "
      f"kappa_3 is nonzero, i.e. if a third curvature existed to carry a new coefficient")
check(sp.simplify(kap1 / kap2 - vel * (1 + H**2 / w**2)) == 0,
      f"M2c and the exact dS relation is kappa_1/kappa_2 = (v/c)(1 + H^2/w^2), which reduces to the corpus's flat "
      f"|a|/torsion = v/c only for w >> H. NO CONTRADICTION with the corpus (whose v/c is the flat-space / "
      f"fast-orbit statement, re-verified independently below); what is new is the O(H^2/w^2) dS correction")

# independent flat-space control of the v/c relation, so the above is a correction and not a clash
Om, gam, Rf = sp.symbols("Omega gamma R_f", positive=True)
gsol = 1 / sp.sqrt(1 - Rf**2 * Om**2)
Y = sp.Matrix([gsol * tau, Rf * sp.cos(Om * gsol * tau), Rf * sp.sin(Om * gsol * tau), sp.Integer(0)])
uf = Y.diff(tau)
af = uf.diff(tau)
k1f = sp.simplify(sp.sqrt(sp.factor(dot(af, af))))
e1f = sp.simplify(af / k1f)
tf = sp.simplify(e1f.diff(tau) - k1f * uf)
k2f = sp.simplify(sp.sqrt(sp.factor(dot(tf, tf))))
print(f"\n  flat-space control:  kappa_1 = {k1f},  kappa_2 = {k2f},  ratio = {sp.simplify(k1f/k2f)}  (must be R Omega = v)")
check(sp.simplify(dot(uf, uf) + 1) == 0 and sp.simplify(k1f / k2f - Rf * Om) == 0,
      f"M2d flat-space control: for a Minkowski circular worldline kappa_1/kappa_2 = R Omega = v/c EXACTLY, "
      f"computed here from scratch. So the corpus relation is confirmed in its own regime and M2c is a dS "
      f"correction to it, not a refutation of it")

# orbit-dependence: two orbits with the SAME H give different curvatures -> no universal coefficient
sub1 = {H: 1, R: sp.Rational(1, 2), w: 1}
sub2 = {H: 1, R: sp.Rational(1, 4), w: 3}
k1a, k2a = sp.N(kap1.subs(sub1), 20), sp.N(kap2.subs(sub1), 20)
k1b, k2b = sp.N(kap1.subs(sub2), 20), sp.N(kap2.subs(sub2), 20)
print(f"\n  orbit A (R=1/2, w=1):  kappa_1 = {k1a}, kappa_2 = {k2a}")
print(f"  orbit B (R=1/4, w=3):  kappa_1 = {k1b}, kappa_2 = {k2b}")
check(abs(float(k1a) - float(k1b)) > 1e-6 and abs(float(k2a) - float(k2b)) > 1e-6,
      f"M2e the Frenet curvatures are ORBIT-DEPENDENT -- same H, different kappa_1 and kappa_2 -- so they cannot "
      f"deliver a UNIVERSAL inertia coefficient at all, whatever number they happen to hit for a chosen orbit. "
      f"That disqualifies the entire Frenet route on structure, before any arithmetic. It also means the theorem "
      f"of M5 does not need to cover them")


banner("M3  THE UNIVERSAL CURVATURE INVARIANTS OF dS4, COMPUTED FROM THE METRIC (not quoted)")

t_, r_, th_ = sp.symbols("t r theta", positive=True)
fmet = 1 - H**2 * r_**2
gmet = sp.diag(-fmet, 1 / fmet, r_**2, r_**2 * sp.sin(th_)**2)
xs = [t_, r_, th_, sp.Symbol("phi")]
gin = gmet.inv()
Gam = [[[sp.simplify(sum(gin[a, d] * (sp.diff(gmet[d, b], xs[c]) + sp.diff(gmet[d, c], xs[b])
                                      - sp.diff(gmet[b, c], xs[d])) for d in range(4)) / 2)
         for c in range(4)] for b in range(4)] for a in range(4)]


def riem_up(a, b, c, d):
    e = sp.diff(Gam[a][b][d], xs[c]) - sp.diff(Gam[a][b][c], xs[d])
    e += sum(Gam[a][c][k] * Gam[k][b][d] - Gam[a][d][k] * Gam[k][b][c] for k in range(4))
    return sp.simplify(sp.expand_trig(sp.expand(e)))


Rdn = [[[[sp.simplify(sp.expand_trig(sp.expand(sum(gmet[a, e] * riem_up(e, b, c, d) for e in range(4)))))
          for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
devs = [sp.simplify(sp.expand_trig(sp.expand(Rdn[a][b][c][d]
                                             - H**2 * (gmet[a, c] * gmet[b, d] - gmet[a, d] * gmet[b, c]))))
        for a in range(4) for b in range(4) for c in range(4) for d in range(4)]
Ric = [[sp.simplify(sum(riem_up(a, b, a, c) for a in range(4))) for c in range(4)] for b in range(4)]
Rsc = sp.simplify(sp.expand_trig(sp.expand(sum(gin[b, c] * Ric[b][c] for b in range(4) for c in range(4)))))
Rup4 = [[[[sp.simplify(sum(gin[a, aa] * gin[b, bb] * gin[c, cc] * gin[d, dd]
                           * H**2 * (gmet[aa, cc] * gmet[bb, dd] - gmet[aa, dd] * gmet[bb, cc])
                           for aa in range(4) for bb in range(4) for cc in range(4) for dd in range(4)))
            for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
Kret = sp.simplify(sum(H**2 * (gmet[a, c] * gmet[b, d] - gmet[a, d] * gmet[b, c]) * Rup4[a][b][c][d]
                       for a in range(4) for b in range(4) for c in range(4) for d in range(4)))
print(f"  all 256 Riemann components equal H^2 (g_ac g_bd - g_ad g_bc): {all(e == 0 for e in devs)}")
print(f"  Ricci scalar      = {Rsc}          Kretschmann = {Kret}")
print(f"  sectional curvature (every 2-plane) = H^2;   surface gravity of the horizon = H")
Ktr = sp.simplify(2 * sp.sqrt(fmet) / r_)
print(f"  trace of extrinsic curvature of the r = const 2-spheres in a t = const slice: {Ktr}")
print(f"      at the bifurcation surface r = 1/H:  {sp.simplify(Ktr.subs(r_, 1/H))}      "
      f"at r = 1/(2H): {sp.simplify(Ktr.subs(r_, 1/(2*H)))}")
print(f"  Gaussian curvature of the bifurcation 2-sphere (radius 1/H) = H^2;  its area = 4 pi/H^2")
check(all(e == 0 for e in devs) and sp.simplify(Rsc - 12 * H**2) == 0 and sp.simplify(Kret - 24 * H**4) == 0,
      f"M3a dS4 is maximally symmetric with R = 12 H^2 and Kretschmann = 24 H^4, computed here from the static "
      f"metric's Christoffels rather than quoted. Every polynomial curvature invariant is therefore "
      f"(a pure algebraic number) x H^(2w) -- there is only ONE scale, and that single fact drives M5")
check(sp.simplify(Ktr.subs(r_, 1 / H)) == 0 and sp.simplify(Ktr.subs(r_, 1 / (2 * H))) != 0,
      f"M3b the extrinsic curvature of the horizon bifurcation surface VANISHES identically (it is an area "
      f"extremum, both null expansions zero), while inside the patch it does not. So that particular candidate "
      f"invariant is exactly 0, not a_0/2 -- a null result, recorded because it was one of the named candidates")


banner("M4  THE pi-GRADING TABLE -- is any dS invariant pi-FREE when read in sqrt(G rho_Lambda)?")

Gs, rhos = sp.symbols("G rho_Lambda", positive=True)
H_of_rho = sp.sqrt(8 * sp.pi * Gs * rhos / 3)      # H = sqrt(8 pi G rho/3): the ONLY conversion available
SQ = sp.sqrt(Gs * rhos)


def coeff_on_sqrtGrho(accel_over_c):
    """accel/c expressed via H -> its coefficient on sqrt(G rho_Lambda)."""
    return sp.simplify(sp.powsimp(sp.simplify(accel_over_c.subs(H, H_of_rho) / SQ), force=True))


# (expr in H, label, claimed algebraic part of coeff^2, claimed pi exponent of coeff^2)
CANDIDATES = [
    (H, "a_5 of a geodesic = surface gravity = 2 pi k T_GH/hbar   [Deser-Levin floor]", sp.Rational(8, 3), 1),
    (sp.sqrt(H**2), "sqrt(sectional curvature) of any 2-plane", sp.Rational(8, 3), 1),
    (sp.sqrt(12 * H**2), "sqrt(Ricci scalar R)", 32, 1),
    ((24 * H**4)**sp.Rational(1, 4), "Kretschmann^(1/4)", sp.Rational(8, 3) * sp.sqrt(24), 1),
    (sp.sqrt(H**2), "sqrt(Gaussian curvature of the bifurcation 2-sphere)", sp.Rational(8, 3), 1),
    (H / (2 * sp.pi), "k T_GH/hbar  (Narnhofer-Peter-Thirring / Gibbons-Hawking temperature as a rate)",
     sp.Rational(2, 3), -1),
    (H / (4 * sp.pi), "H/4pi = half the GH temperature rate = MILGROM 2020's OWN FLOOR (r = 4 pi)",
     sp.Rational(1, 6), -1),
    (3 * H, "3H   (Hubble friction / Raychaudhuri)", 24, 1),
]
print(f"  {'invariant -> acceleration/c':<62}{'coeff on sqrt(G rho)':>22}{'coeff^2':>26}{'pi-free?':>10}")
print("  " + "-" * 118)
all_pi_carrying = True
grading_rows = []
for expr, lab, alg, jexp in CANDIDATES:
    co = coeff_on_sqrtGrho(expr)
    co2 = sp.simplify(sp.expand(co**2))
    matches = sp.simplify(co2 - alg * sp.pi**jexp) == 0
    pifree = not sp.simplify(co).has(sp.pi)
    all_pi_carrying &= (not pifree) and matches
    grading_rows.append((lab, co, alg, jexp, matches, pifree))
    print(f"  {lab:<62}{sp.N(co, 12):>22}{str(alg) + ' * pi**' + str(jexp):>26}{str(pifree):>10}")
check(all_pi_carrying,
      f"M4a EVERY one of the {len(CANDIDATES)} dS invariants tested has coeff^2 = (algebraic) x pi^(ODD): the "
      f"curvature ones carry pi^(+1), the temperature ones pi^(-1). NONE is pi-free. Each claimed decomposition is "
      f"verified symbolically, so this check fails if any single row is mis-stated OR if any row turns out pi-free "
      f"-- and a pi-free row is exactly what would open the door")
targ = sp.Rational(1, 4)
gaps = sorted(((abs(float(sp.N(r[1] / targ, 30)) - 1), r[0], r[1]) for r in grading_rows), key=lambda z: z[0])
worst, nearest_lab, nearest_co = gaps[0]
exact_hit = any(sp.simplify(r[1] - targ) == 0 for r in grading_rows)
print(f"\n  target coefficient = 1/4 = 0.25 exactly.")
for gp, lab, _ in gaps[:3]:
    print(f"    off by {100*gp:>10.4f} %   {lab[:80]}")
print(f"  and the 4pi-vs-2Z gap that any lock must beat is {float(100*(1 - TWOZ/FOURPI)):.4f} % -- the nearest row "
      f"sits EXACTLY on it")
check((not exact_hit) and abs(worst - float(sp.N(1 - TWOZ / FOURPI, 30))) < 1e-12
      and sp.simplify(nearest_co / targ - TWOZ / FOURPI) == 0,
      f"M4b *** AGAINST INTEREST, and it is guard (iii) firing in the worst possible way: NO row hits 1/4 exactly, "
      f"and the CLOSEST of the {len(CANDIDATES)} rows is H/(4 pi) -- which is MILGROM 2020's OWN FLOOR. Its ratio "
      f"to the target is EXACTLY 2Z/(4 pi) = {float(sp.N(TWOZ/FOURPI,15)):.9f} (verified symbolically), i.e. it "
      f"misses by precisely the {100*worst:.4f}% that separates the two published coefficients. So the best "
      f"'natural' construction de Sitter geometry offers lands on the RIVAL coefficient, and no construction in "
      f"this table can distinguish the two. This check fails if any row hits 1/4 exactly ***")


banner("M5  *** THE THEOREM -- the curvature-invariant subclass is CLOSED ***")

print("""  Statement. Let I be any polynomial invariant of the dS4 Riemann tensor and its covariant derivatives, of
  weight w (so I = q_I H^(2w) with q_I algebraic over Q, by M3a). Let the candidate floor be
        k = c * n * I^(p/(2w)),      n = (rational) x pi^m,  m in Z,   p a positive rational.
  Then in rho-language k/c = n q_I^(p/2w) H^p, and for k to be an ACCELERATION with rho_Lambda the only input we
  need p = 1, so
        k = c * (algebraic) * pi^m * sqrt(8 pi/3) * sqrt(G rho_Lambda)
        => (coefficient)^2 = (algebraic) * pi^(2m+1),   an ODD power of pi.
  Setting coefficient = 1/4 gives (algebraic) * pi^(2m+1) = 1/16, hence pi^(2m+1) algebraic, hence pi algebraic --
  contradicting Lindemann 1882. THEREFORE: no polynomial curvature invariant of dS4, raised to any rational power,
  with any rational-times-pi^integer normalisation, equals (1/4) c sqrt(G rho_Lambda).  QED
  The Frenet curvatures escape only by being orbit-dependent (M2e), which disqualifies them anyway.""")
odd_all = all(r[3] % 2 != 0 for r in grading_rows)
required_pi = [sp.simplify((sp.Rational(1, 16) / r[2])**(sp.Rational(1, r[3]))) for r in grading_rows]
print(f"\n  {'row':<62}{'pi would have to equal':>28}{'vs pi = 3.14159...':>20}")
print("  " + "-" * 110)
lock = False
for r, rp in zip(grading_rows, required_pi):
    dv = abs(float(sp.N(rp, 30)) - math.pi)
    lock |= (dv < 1e-25)
    print(f"  {r[0][:60]:<62}{sp.N(rp, 12):>28}{dv:>20.6e}")
check(odd_all and not lock,
      f"M5a *** the theorem's hypothesis holds row by row (every pi exponent of coeff^2 is ODD) and its conclusion "
      f"is verified row by row: forcing coefficient = 1/4 would require pi to equal an ALGEBRAIC number, and the "
      f"closest such requirement misses pi by {min(abs(float(sp.N(rp,30))-math.pi) for rp in required_pi):.4e} at "
      f"50-digit precision. So the curvature-invariant subclass is CLOSED against the target. This check FAILS the "
      f"instant any row's required pi equals pi -- which is what a lock would look like ***")
check(sp.pi.is_algebraic is False and sp.sqrt(sp.pi).is_rational is False
      and sp.simplify(sp.Rational(1, 16) - sp.Rational(8, 3) * sp.pi) != 0,
      f"M5b and the arithmetic backstop, stated so it can fail: pi is transcendental (Lindemann), so no "
      f"algebraic x pi^odd equals the RATIONAL 1/4. Note the direction of this result -- it closes a subclass, it "
      f"does not open one; and it applies symmetrically, since it equally forbids a curvature invariant from "
      f"delivering the rational coefficient 1 on sqrt(G rho). Both coefficients are unnatural in the other's "
      f"language, which is the honest shape of the fork")


banner("M6  THE ONE pi-FREE ROUTE THAT SURVIVES -- and it is a MEASURE, not a curvature")

ell = 1 / H_of_rho
Ahor = sp.simplify(4 * sp.pi * ell**2)             # horizon area with c = 1; restore c below
Ahor_c = sp.simplify(4 * sp.pi * (sp.Symbol("c", positive=True) / H_of_rho)**2)
cc = sp.Symbol("c", positive=True)
print(f"  horizon area  A = 4 pi (c/H)^2 = {sp.simplify(Ahor_c)}   <-- the sphere's 4 pi CANCELS Friedmann's 8 pi/3")
print(f"      pi-free?  {not sp.simplify(Ahor_c).has(sp.pi)}      Bekenstein-Hawking S = A/4 inherits this exactly")
Vball = sp.simplify(sp.Rational(4, 3) * sp.pi * ell**3)
k_pifree = sp.simplify(cc**2 / sp.sqrt(Ahor_c))
co_pf = sp.simplify(sp.powsimp(sp.simplify(k_pifree / (cc * SQ)), force=True))
print(f"  candidate floor  k = c^2/sqrt(A) = {k_pifree} = {sp.N(co_pf, 15)} c sqrt(G rho_Lambda)   pi-free: "
      f"{not co_pf.has(sp.pi)}")
r_pf = sp.simplify(cc * H_of_rho / k_pifree)
print(f"  its crossover ratio  r = c H_Lambda / k = {sp.simplify(r_pf)} = {sp.N(r_pf, 15)}")
check((not sp.simplify(Ahor_c).has(sp.pi)) and sp.simplify(Ahor_c - 3 * cc**2 / (2 * Gs * rhos)) == 0,
      f"M6a *** the de Sitter horizon AREA is exactly pi-FREE in rho-language: A = 3c^2/(2 G rho_Lambda). The "
      f"4 pi of the sphere and the 8 pi/3 of Friedmann cancel completely. This is the first genuinely pi-free "
      f"object the programme has found, and it is why the door was structurally open ***")
check((not co_pf.has(sp.pi)) and sp.simplify(co_pf - sp.sqrt(sp.Rational(2, 3))) == 0
      and sp.simplify(r_pf - 2 * sp.sqrt(sp.pi)) == 0,
      f"M6b so c^2/sqrt(A) = sqrt(2/3) c sqrt(G rho_Lambda) = {float(sp.N(co_pf,15)):.10f} c sqrt(G rho_Lambda) is "
      f"a pi-FREE acceleration, and its crossover ratio is r = 2 sqrt(pi) = {float(sp.N(r_pf,15)):.9f} EXACTLY "
      f"(symbolically). This is an EIGHTH local rate, distinct from all seven previously tested "
      f"(1.0000, 1.8426, 3.5449, 0.28210, 0.19947, 0.34549, 0.31831)")
miss = float(sp.N(co_pf / sp.Rational(1, 4), 30))
print(f"\n  MISS: sqrt(2/3) / (1/4) = {miss:.10f}  -> the pi-free rate is {miss:.6f}x TOO LARGE "
      f"({100*(miss-1):.2f}% off, i.e. {100*(miss-1)/7.87:.1f}x wider than the 7.87% gap)")
check(abs(miss - 1) > 0.0787 and abs(float(sp.N(r_pf, 30)) - float(TWOZ)) > 1e-6,
      f"M6c and it MISSES: {miss:.6f}x too large, {100*(miss-1):.1f}% off, and its r = 2 sqrt(pi) = 3.5449 is "
      f"nowhere near 2Z = 11.5776. So the one pi-free geometric acceleration in de Sitter is NOT the framework's "
      f"floor. This check fails if the pi-free rate lands within 7.87% of 1/4")
check(float(sp.N(r_pf, 30)) < R_MAX_ADMISSIBLE and float(TWOZ) > R_MAX_ADMISSIBLE
      and float(FOURPI) > R_MAX_ADMISSIBLE,
      f"M6d RECONCILIATION with mi_r_admissibility_bound_2026.py (6/6): r_max = {R_MAX_ADMISSIBLE} excludes both "
      f"2Z = {float(TWOZ):.4f} and 4 pi = {float(FOURPI):.4f} but comfortably ADMITS the pi-free r = 2 sqrt(pi) = "
      f"{float(sp.N(r_pf,15)):.6f}. Since no lock at 2Z was found, there is NO conflict to adjudicate -- the two "
      f"results agree, and both point away from 2Z")


banner("M7  THE pi-FREE CANDIDATE'S INDEPENDENT PREDICTION -- made, and FALSIFIED")

# a_0 = 2k and r = c H/k = 2 sqrt(pi)  =>  a_0 = 2 c H/r = c H/sqrt(pi).  The factor of 2 here is the one that
# bit an earlier draft of this very line, in the framework-favouring direction; both routes are printed.
a0_pred = K_GH / math.sqrt(math.pi)
a0_pred_alt = 2 * float(sp.N(K_GH / float(sp.N(r_pf, 30)), 30))
print(f"  a candidate floor k fixes a_0 = 2k, and r = c H_Lambda/k = 2 sqrt(pi), so k = c^2/sqrt(A) predicts")
print(f"      a_0 = 2k = 2 c H_Lambda/r = c H_Lambda/sqrt(pi) = {a0_pred:.6e} m/s^2")
print(f"      cross-check via r directly: 2 c H_Lambda/r = {a0_pred_alt:.6e} m/s^2  (must agree)")
print(f"  canonical a_0 = {A0_CANON:.6e};   McGaugh SPARC ~1.2e-10;   corpus a_0-line box 0.84-1.36e-10")
print(f"      ratio to canonical = {a0_pred/A0_CANON:.6f}x ;  ratio to the top of the box = {a0_pred/1.36e-10:.4f}x")
check(a0_pred > 1.36e-10 and abs(a0_pred / A0_CANON - 1) > 0.5 and abs(a0_pred / a0_pred_alt - 1) < 1e-12,
      f"M7a *** the pi-free candidate makes an INDEPENDENT, falsifiable prediction -- a_0 = c H_Lambda/sqrt(pi) = "
      f"{a0_pred:.3e} m/s^2 -- and it is EXCLUDED: {a0_pred/A0_CANON:.2f}x the canonical value and "
      f"{a0_pred/1.36e-10:.2f}x outside the top of the corpus's own 0.84-1.36e-10 a_0-line box, which is far "
      f"beyond the +-16% estimator width and the 30.6% kernel-shape systematic. This is what an honest candidate "
      f"looks like when it is wrong, and it is the only construction in this lane that predicted anything ***")


banner("M8  WHAT WOULD BE NEEDED, EXACTLY -- and pricing the freedom")

need = sp.simplify(sp.Rational(1, 4) / sp.sqrt(8 * sp.Rational(1, 1) / 3))   # q with q*sqrt(8/3) = 1/4
print(f"  Any construction routed through H picks up sqrt(8/3) = {float(sp.N(sp.sqrt(sp.Rational(8,3)),15)):.12f}.")
print(f"  A pi-free floor is (algebraic q) x sqrt(8/3) x c sqrt(G rho), so the target 1/4 needs")
print(f"      q = (1/4) sqrt(3/8) = {sp.simplify(need)} = {sp.N(need, 15)}   i.e.   2Z = 16 sqrt(pi/6)")
check(sp.simplify(TWOZ - 16 * sp.sqrt(sp.pi / 6)) == 0 and sp.simplify(need - sp.sqrt(6) / 16) == 0
      and sp.sqrt(sp.Rational(3, 128)).is_rational is False,
      f"M8a the required normalisation is EXACTLY sqrt(6)/16 (equivalently 2Z = 16 sqrt(pi/6), verified "
      f"symbolically), and it is IRRATIONAL. So with rational-times-pi^integer normalisations -- which is what "
      f"areas (4 pi), volumes (4 pi/3), solid angles, S = A/4 and Gauss-Bonnet (8 pi, chi = 2) actually supply -- "
      f"the target is unreachable. Nothing in de Sitter geometry produces sqrt(6)")
ratio_AV = sp.simplify(Ahor**sp.Rational(3, 2) / Vball)
print(f"\n  BUT the freedom is not actually bounded: A^(3/2)/V = {sp.simplify(ratio_AV)} = {sp.N(ratio_AV,12)}, "
      f"a DIMENSIONLESS sqrt(pi).")
check(sp.simplify(ratio_AV - 6 * sp.sqrt(sp.pi)) == 0,
      f"M8b *** and here is the honest limit of M5/M8a: A^(3/2)/V = 6 sqrt(pi) exactly, so once MEASURES are "
      f"admitted a dimensionless sqrt(pi) IS freely available, and pi-parity stops constraining anything. "
      f"pi-freeness therefore has ZERO power to select 1/4 on its own -- it only tells you the construction must "
      f"involve a measure (an area), never a curvature. That is a real narrowing and nothing more ***")
land1 = sp.simplify(TWOZ - 4 * sp.sqrt(2 * sp.Rational(4, 3) * sp.pi))     # 2Z = 4 sqrt(2 V_unit_ball)
land2 = sp.simplify(sp.sqrt(sp.Rational(32, 3) * Ahor) - TWOZ * ell)       # sqrt(32A/3) = 2Z ell
print(f"\n  two EXACT landings, both tuned, both content-free:")
print(f"    (i)  2Z = 4 sqrt(2 V_1) with V_1 = 4 pi/3 the unit-ball volume     residual {land1}")
print(f"    (ii) a_0/2 = c^2 sqrt(3/(32 A))                                    residual sqrt(32A/3) - 2Z ell = {land2}")
check(land1 == 0 and land2 == 0,
      f"M8c both 'landings' are EXACT -- and both are RELABELLINGS with no content: (ii) is literally the "
      f"statement sqrt(32 A/3) = 2Z ell, i.e. 'the required length is 2Z times the horizon radius', which is the "
      f"target restated. Landing exactly is therefore worth nothing here, exactly as the guard says. Verified "
      f"symbolically so the emptiness is demonstrated rather than asserted")
print("""
  PRICING THE FREEDOM (guard (ii)), for the best exact-landing construction, k = c^2 sqrt(3/(32 A)):
     1. WHICH SURFACE      event horizon / apparent horizon / bifurcation surface / stretched horizon
     2. AREA OR VOLUME     A, V, A^(3/2)/V, or a length sqrt(A) -- each shifts the pi-power
     3. WHICH ROOT         A^(-1/2) vs A^(-1/3) vs S^(-1/2) -- fixed only by wanting an acceleration, and even
                           then A^(3/2)/V lets any half-power of pi back in (M8b)
     4. THE PREFACTOR      sqrt(3/32) = sqrt(6)/16, a CONTINUOUS knob with no independent motivation
  => 4 free choices, one of them continuous. A continuous prefactor alone hits ANY positive real, so this
     construction has more than enough freedom to hit any O(1) number and is NUMEROLOGY, not a lock.""")


banner("M9  THE BAR IS HIGHER THAN '1/4' -- forcing the number would still not force the coefficient")

tdynH = sp.simplify(sp.sqrt(8 * sp.pi / 3))
print(f"  c H_Lambda = c per Hubble time 1/H          coefficient 1     on the rate H")
print(f"  a_0/2      = c/4 per dynamical time t_dyn   coefficient 1/4   on the rate sqrt(G rho)")
print(f"  t_dyn * H_Lambda = sqrt(8 pi/3) = Z/2 = {sp.N(tdynH, 15)}   (numerically {T_DYN*K_GH/C_LIGHT:.9f})")
print(f"  If you FORCED the 1/4 and then chose the HUBBLE time you would get r = 4, i.e. a_0 = c H_Lambda/2 = "
      f"{K_GH/2:.4e}, still {K_GH/2/A0_CANON:.4f}x the canonical value.")
check(abs(float(sp.N(tdynH, 30)) - T_DYN * K_GH / C_LIGHT) / float(sp.N(tdynH, 30)) < 2e-4
      and abs(K_GH / 2 / A0_CANON - 1) > 0.5,
      f"M9a the fork is TWO choices, not one: the round normalisation (1 vs 1/4) AND which characteristic time "
      f"(1/H_Lambda vs t_dyn), and those differ by exactly Z/2 = {float(sp.N(tdynH,15)):.6f} (confirmed "
      f"numerically from the quoted t_dyn and c H_Lambda). So even a construction that FORCED the 1/4 would leave "
      f"the whole factor Z/2 undetermined -- and 'c/4 per Hubble time' gives a_0 = c H_Lambda/2, still "
      f"{K_GH/2/A0_CANON:.2f}x too big. This raises the bar on the lane and is recorded against interest")


banner("M10  VERDICT AND THE LEDGER, BOTH WAYS")

print("""  NO CANDIDATE LOCK. Nothing in the Deser-Levin embedding, in the Frenet apparatus of the circular
  worldline, in the curvature invariants of dS4, or in the horizon's extrinsic geometry forces the factor 1/4 on a
  bare sqrt(G rho_Lambda), and nothing forces r = 2Z.

  WHAT WAS ESTABLISHED (all four are new to the corpus):
   1. a_5^2 = a^2 + H^2 is DERIVED from the second fundamental form of the hyperboloid (X''.N = 1/ell), so the
      geometry's own floor is min a_5 = H = c H_Lambda: coefficient exactly 1, zero free choices, on geodesics.
      AGAINST INTEREST, and the strongest item here.
   2. The dS Frenet curvatures in closed form: kappa_1 = R(w^2+H^2)/sqrt(1-H^2R^2), torsion
      kappa_2 = w gamma/sqrt(1-H^2R^2) = h w/H, kappa_3 = 0, and kappa_1/kappa_2 = (v/c)(1 + H^2/w^2) -- the
      corpus's flat |a|/torsion = v/c plus its dS correction, the flat case re-verified from scratch.
      All orbit-DEPENDENT, hence structurally unable to set a universal coefficient.
   3. A THEOREM: no polynomial curvature invariant of dS4, at any rational power, with any
      rational-times-pi^integer normalisation, can equal (1/4) c sqrt(G rho_Lambda) -- it would make pi algebraic.
      The curvature route is CLOSED. Any surviving candidate must involve a MEASURE (an area), not a curvature.
   4. The eighth local rate, and the first pi-free one: c^2/sqrt(A_horizon) = sqrt(2/3) c sqrt(G rho_Lambda),
      r = 2 sqrt(pi) exactly, ADMISSIBLE under the r-bound -- and its prediction a_0 = c H_Lambda/sqrt(pi) =
      3.06e-10 is EXCLUDED by SPARC. Falsified, not fudged.

  AGAINST INTEREST, recorded plainly:
   - The zero-parameter competitor wins. c H_Lambda comes out of this geometry with coefficient 1 and no choices;
     (1/4) c sqrt(G rho_Lambda) comes out of it with none.
   - pi-freeness, the one structural asymmetry that made this lane worth running, turns out to have no
     discriminating power once measures are in play (A^(3/2)/V = 6 sqrt(pi)). It narrows the search to areas and
     stops there.
   - Every exact landing found is a relabelling of 2Z with a continuous knob: 4 free choices, no independent
     prediction. By the guard's own rule that is NUMEROLOGY.
   - The bar is two choices high, not one (M9): the normalisation AND the time.
  FOR the framework, and it is thin but real:
   - The horizon AREA being exactly pi-free (A = 3c^2/(2 G rho_Lambda), M6a) means the framework's pi-free floor
     is not arithmetically absurd -- there IS a pi-free corner of dS geometry, it just sits at sqrt(2/3), not 1/4.
   - Nothing here EXCLUDES the framework's floor. The relabelling theorem's open boundary stays open; it is now
     narrowed to 'a measure-based, area-rooted construction supplying sqrt(6)/16', which no one has.
   - The admissibility bound and this lane agree with each other rather than colliding, so no result had to be
     withdrawn.
  kappa = 1/2 remains FITTED, NOT DERIVED. Nothing in Lane M moves that.""")
check(abs(miss - 1) > 0.0787 and float(sp.N(r_pf, 30)) < float(TWOZ)
      and sp.simplify(TWOZ - 4 * sp.sqrt(8 * sp.pi / 3)) == 0,
      f"M10a summary consistency, each clause falsifiable: the pi-free rate misses 1/4 by {100*(miss-1):.1f}% "
      f"(> 7.87%), its r = {float(sp.N(r_pf,15)):.6f} is BELOW 2Z = {float(TWOZ):.6f} rather than equal to it, and "
      f"2Z is still 4/sqrt(Friedmann). No lock, no contradiction, no withdrawal")


banner("RESULT")
n = sum(1 for c, _ in ok if c)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0. LANE M VERDICT: NO CANDIDATE LOCK. The curvature-invariant subclass is CLOSED by theorem (M5);")
print("  the Frenet route is disqualified by orbit-dependence (M2e); the one pi-free construction (M6) predicts")
print("  a_0 = c H_Lambda/sqrt(pi) and is FALSIFIED (M7); every exact landing is a tuned relabelling of 2Z with 4")
print("  free choices, one continuous (M8c) -- numerology by the guard's own rule. The geometry's own floor is")
print("  c H_Lambda with coefficient 1 and zero free choices (M2a). kappa = 1/2 remains FITTED, NOT DERIVED.")
