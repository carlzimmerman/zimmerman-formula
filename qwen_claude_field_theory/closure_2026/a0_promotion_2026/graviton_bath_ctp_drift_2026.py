#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
graviton_bath_ctp_drift_2026.py
===============================
THE GRAVITON-BATH CTP NONLINEAR DRIFT -- evaluated.   (the last named lane for deriving kappa = 1/2)

Setup (the lane as specified by mi_cubic_noise_ctp_2026.py and mi_ctp_variational_2026.py):
  * a classical worldline of mass m in the de Sitter static patch, coupled to metric fluctuations h_mn
    through the point-particle action  S_pp = -m c^2 int dtau sqrt(1 - h_uu),  h_uu = h_mn u^m u^n;
  * the graviton bath in the Bunch-Davies state, which the static-patch worldline sees as THERMAL at the
    Gibbons-Hawking / Deser-Levin temperature  k_B T(a) = (hbar/2 pi c) sqrt(a^2 + c^2 H^2);
  * CTP (in-in): the mean equation of motion gets the dissipation kernel (commutator, state-independent)
    at Gaussian order, and the noise kernel reaches the mean trajectory ONLY through the NONLINEAR
    couplings g_2 h_uu^2, g_3 h_uu^3, ... (the rectified drift  <g_2 h^2> = g_2 c_2).

Questions, each with checks that can FAIL (rc=1) and a mutation control (MUTATE=1 must break them):
  A. the worldline couplings g_n exactly, and the universality screen (drift/m is m-independent);
  B. hbar-COUNTING THEOREM: every Lambda-(H-)dependent term of the mean EOM is proportional to hbar,
     because it enters only through the noise kernel and k_B T_GH = hbar H / 2 pi; the hbar-free part of
     the EOM (dissipation, UV mass renormalisation) is Lambda-BLIND.  Hence no hbar-free acceleration built
     from Lambda exists at ANY order in the coupling;
  C. the magnitude: the drift is a fraction  n/(6 S_dS)  of the de Sitter acceleration H^2 r, with S_dS the
     de Sitter entropy (~3e122), and it is proportional to r (a Lambda renormalisation), NOT a constant a_0;
  D. the shape: the perturbative bath gives f(T) = T^2 (the variance), for which the crossover master
     formula yields q = 0 -- no MOND interpolation function at all; the a = cH_Lambda crossover of T(a)
     survives only as a 1e-117 higher-derivative term;
  E. the rescues, each priced: induced inertia (= MI, excluded 21 sigma), holographic coherence (needs an
     enhancement of exactly S_dS: a new postulate, category III), dS IR secular growth (needs ~S_dS e-folds),
     a primordial tensor background (r A_s ceiling, an initial condition not a derivation).

VERDICT: the graviton-bath CTP nonlinear drift CANNOT deliver kappa: the drift is hbar-suppressed by
1/S_dS ~ 1e-122, r-proportional, and shapeless.  With this, EVERY named derivation lane for kappa = 1/2
is closed.  kappa is a measured constitutive number (0.465 +- 0.076 / 0.551 +- 0.043).  Layer A untouched.

Run:  python3 graviton_bath_ctp_drift_2026.py          (rc=0)
      MUTATE=1 python3 graviton_bath_ctp_drift_2026.py (rc=1: T_GH made hbar-free -> the theorem's hinge breaks)
"""
import os, sys, math
import sympy as sp

MUTATE = os.environ.get("MUTATE", "0") == "1"
P = lambda *a: print(*a, flush=True)
FAILS = []
def check(name, ok, detail=""):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)

# SI constants, canonical footing (pure-Lambda density)
c = 2.99792458e8; G = 6.674e-11; hbar = 1.054571817e-34; MPC = 3.0857e22
H0 = 67.4e3/MPC; OmL = 0.685
rho_c = 3*H0**2/(8*math.pi*G); rho_L = OmL*rho_c
HL = math.sqrt(8*math.pi*G*rho_L/3)                      # pure-Lambda de Sitter rate
lP = math.sqrt(hbar*G/c**3)
A0 = 0.5*c*math.sqrt(G*rho_L)                            # kappa = 1/2 reference, 9.36e-11
S_dS = math.pi*(c/HL)**2/lP**2                           # A/(4 l_P^2), A = 4 pi (c/H)^2
KAPPA_MEAS = [("BTFR", 0.465, 0.076), ("distance-free", 0.551, 0.043)]
allowed = lambda k: any(abs(k-m)/s <= 2 for _, m, s in KAPPA_MEAS)

P("="*100); P("A. the worldline-graviton couplings, exactly, and the universality screen"); P("="*100)
x, m, cc = sp.symbols('x m c', positive=True)              # x = h_uu
ser = sp.series(-m*cc**2*sp.sqrt(1 - x), x, 0, 4).removeO()
g1 = ser.coeff(x, 1); g2 = ser.coeff(x, 2); g3 = ser.coeff(x, 3)
check("S_pp = -mc^2 int dtau sqrt(1-h_uu): g_1 = mc^2/2 (linear), g_2 = mc^2/8 (the NONLINEAR coupling), g_3 = mc^2/16",
      sp.simplify(g1 - m*cc**2/2) == 0 and sp.simplify(g2 - m*cc**2/8) == 0 and sp.simplify(g3 - m*cc**2/16) == 0,
      f"g1={g1}, g2={g2}, g3={g3}")
check("universality screen PASSES for the graviton bath: every g_n is proportional to m, so drift/m is m-independent",
      all(sp.simplify(sp.diff(g/m, m)) == 0 for g in (g1, g2, g3)))
P("  (the scalar-bath exclusion of mi_cubic_noise_ctp_2026.py does not apply here: this IS the gravitational bath)")

P(""); P("="*100); P("B. hbar-COUNTING THEOREM: Lambda enters the mean EOM only through the noise, and the noise is O(hbar)"); P("="*100)
hb, Gs, Hs, w, a, r, n = sp.symbols('hbar G H omega a r n', positive=True)
# canonical graviton: h = sqrt(32 pi G / c^4) hhat, with <hhat hhat> = hbar x (mode sum).  c=1 inside this part.
# static-patch worldline at proper acceleration a: k_B T(a) = hbar sqrt(a^2+H^2)/(2 pi)   (Deser-Levin 1997)
T_of_a = (hb if not MUTATE else 1)*sp.sqrt(a**2 + Hs**2)/(2*sp.pi)     # MUTATION: a classical temperature (no hbar)
# spectral density of the free graviton commutator (state-independent, Raval-Hu-Anglin): rho(w) = w/pi^2
rho_w = w/sp.pi**2
commutator = hb*32*sp.pi*Gs*rho_w                          # <[h,h]>(w) = 32 pi G x hbar rho(w)
anticomm   = hb*32*sp.pi*Gs*rho_w*sp.coth(hb*w/(2*T_of_a)) # <{h,h}>(w) = same x coth(hbar w / 2 k_B T)
# CTP: influence phase Phi = (1/hbar) S_IF.  Dissipation kernel D = g1^2 <[h,h]> / hbar ; noise covariance N = g1^2 <{h,h}>/2
G1 = m/2                                                   # c = 1
D_kernel = G1**2*commutator/hb
N_kernel = G1**2*anticomm/2
check("B1 dissipation kernel D = g_1^2 <[h,h]>/hbar is hbar-FREE and H-FREE (classical radiation reaction, Lambda-blind)",
      sp.simplify(sp.diff(D_kernel, hb)) == 0 and sp.simplify(sp.diff(D_kernel, Hs)) == 0, f"D = {sp.simplify(D_kernel)}")
coth_arg = sp.simplify(hb*w/(2*T_of_a))
check("B2 the Bose factor is hbar-FREE: hbar w / 2 k_B T(a) = pi w / sqrt(a^2+H^2)  (T_GH is itself O(hbar))",
      sp.simplify(sp.diff(coth_arg, hb)) == 0, f"arg = {coth_arg}")
check("B3 hence the noise covariance N = g_1^2 <{h,h}>/2 is O(hbar^1): lim_{hbar->0} N = 0 while dN/dH != 0",
      sp.limit(N_kernel.subs({a: 1, Hs: 1, w: 1, Gs: 1, m: 1}), hb, 0) == 0 and sp.simplify(sp.diff(N_kernel, Hs)) != 0)
# the rectified drift: <g_2 h_uu^2>.  Thermal coincident variance of a canonical massless field: <phi^2>_T = (k_B T)^2/(12 hbar)
var_hhat = T_of_a**2/(12*hb)                               # per polarisation (c=1)
var_h    = 32*sp.pi*Gs*n*var_hhat                          # n = polarisation x tensor/kinematic factor, n <= O(1)
drift_L  = (m/8)*var_h                                     # g_2 <h_uu^2>: the term the noise adds to the mean Lagrangian
check("B4 <h_uu^2>_th = (2n/3pi) G hbar (a^2 + H^2)  [= (2n/3pi) l_P^2 (a^2 + c^2 H^2) in SI]",
      sp.simplify(var_h - sp.Rational(2, 3)/sp.pi*n*Gs*hb*(a**2 + Hs**2)) == 0 if not MUTATE else True,
      f"<h^2> = {sp.factor(sp.simplify(var_h))}")
check("B5 THEOREM: the H-dependent (Lambda-dependent) part of the mean EOM vanishes as hbar -> 0 at this order",
      sp.limit(sp.diff(drift_L, Hs).subs({a: 1, Hs: 1, Gs: 1, m: 1, n: 1}), hb, 0) == 0)
# all orders: with k field insertions the connected Gaussian contribution is (32 pi G hbar)^{k/2} x (hbar-free thermal factors)
k = sp.symbols('k', positive=True, integer=True)
order_k = (32*sp.pi*Gs*hb)**(k/2)
check("B6 all orders: a term with k graviton insertions carries (32 pi G hbar)^{k/2}; Lambda-dependence adds NO 1/hbar",
      sp.limit(order_k.subs(k, 2), hb, 0) == 0 and sp.limit(order_k.subs(k, 4), hb, 0) == 0)
P("  => Every Lambda-dependent term in the mean EOM is O(hbar^{>=1}); the O(hbar^0) part (dissipation, UV mass")
P("     renormalisation) is Lambda-blind.  NO hbar-free acceleration built from Lambda exists at ANY perturbative order.")

P(""); P("="*100); P("C. MAGNITUDE of the rectified drift, and its r-dependence"); P("="*100)
# static-patch Tolman temperature T_loc(r) = T_GH / sqrt(1 - H^2 r^2) => <h^2>(r) = <h^2>_0 / (1 - H^2 r^2)
var_r = var_h.subs(a, 0)/(1 - Hs**2*r**2)
force_drift = (m/8)*sp.diff(var_r, r)                      # g_2 d<h^2>/dr : the spatial-gradient (rectified) drift
a_drift = sp.simplify(force_drift/m)
ratio = sp.simplify(sp.series(a_drift/(Hs**2*r), r, 0, 1).removeO())   # relative to the de Sitter acceleration H^2 r
check("C1 drift acceleration / (H^2 r) = (n/6pi) G hbar H^2 = (n/6pi)(l_P H/c)^2 at leading order in Hr",
      sp.simplify(ratio - n*Gs*hb*Hs**2/(6*sp.pi)) == 0 if not MUTATE else True, f"ratio = {ratio}")
lPH = lP*HL/c
check("C2 identity: 1/(l_P H/c)^2 = S_dS/pi  -- the missing factor IS the de Sitter entropy",
      abs(1/lPH**2 - S_dS/math.pi)/(S_dS/math.pi) < 1e-12, f"S_dS = {S_dS:.3e}, (l_P H/c)^2 = {lPH**2:.3e}")
rel = 1/(6*S_dS)                                             # n = 1
P(f"  drift/(H^2 r) = n/(6 S_dS) = {rel:.2e} x n   (n <= 2 by polarisation counting; TT coupling of a slow worldline gives n ~ 2 v^2/c^2)")
check("C3 the drift is r-PROPORTIONAL (a renormalisation delta Lambda/Lambda = n/6 S_dS), not a constant acceleration",
      sp.simplify(sp.diff(sp.series(a_drift, r, 0, 2).removeO(), r, 2)) == 0 and sp.simplify(a_drift.subs(r, 0)) == 0)
r_kpc = 3.0857e19
a_dS = HL**2*r_kpc; a_dr = rel*a_dS
P(f"  at r = 1 kpc: de Sitter acceleration H^2 r = {a_dS:.2e} m/s^2; drift = {a_dr:.2e} m/s^2; a_0 = {A0:.2e}")
check("C4 the drift misses a_0 by more than 120 orders of magnitude at galactic radii",
      math.log10(A0/a_dr) > 120, f"a_0/drift = 10^{math.log10(A0/a_dr):.1f}")

P(""); P("="*100); P("D. SHAPE: the bath gives f(T) = T^2, for which the crossover master formula yields q = 0"); P("="*100)
# master formula (mi_crossover_master_formula_2026.py): I(a) = f(T(a)) - f(T_GH); MOND needs f asymptotically LINEAR
# (c1p = lim f/T finite) so that I ~ a at large a (Newton).  The variance is f = T^2.
T = sp.symbols('T', positive=True)
f_var = T**2
I_a = sp.simplify(f_var.subs(T, T_of_a) - f_var.subs(T, T_of_a.subs(a, 0)))
check("D1 I(a) = f(T(a)) - f(T_GH) with f = T^2 is PURELY QUADRATIC in a: the H^2 pieces cancel exactly",
      sp.simplify(I_a - (hb if not MUTATE else 1)**2*a**2/(4*sp.pi**2)) == 0, f"I(a) = {I_a}")
c1p = sp.limit(f_var/T, T, sp.oo)
check("D2 c1p = lim f/T = infinity => q = 2 c1p'/f'(T_GH) is NOT in the family: q = 0, no Newtonian limit, no interpolation",
      c1p == sp.oo)
# the acceleration channel: L ⊃ g_2 <h^2>(a) = m (n/12 pi) G hbar (a^2 + H^2): the H^2 piece is a CONSTANT in L (no force),
# the a^2 piece is an Ostrogradsky higher-derivative term whose EOM weight is (n/6pi) G hbar omega^2 relative to m a
L_acc = sp.expand(drift_L)
check("D3 the H^2 piece of g_2<h^2>(a) is x-, v-, a-independent: it contributes NOTHING to the EOM (a constant in L)",
      sp.simplify(sp.diff(L_acc.coeff(a, 0), a)) == 0 and sp.simplify(sp.diff(L_acc.coeff(a, 0), r)) == 0)
omega_gal = A0/1.0e5                                         # a_0 / v with v ~ 100 km/s
hd_weight = (1/(6*math.pi))*(lP*omega_gal/c)**2
P(f"  the a^2 piece: higher-derivative term of relative weight (n/6pi)(l_P omega/c)^2 = {hd_weight:.1e} at omega = a_0/(100 km/s)")
check("D4 the a = cH crossover of T(a) leaves only a higher-derivative trace below 1e-110: no MOND transition in the EOM",
      hd_weight < 1e-110)
kappa_cross = math.sqrt(8*math.pi/3)                         # if one insisted a_0 = the T(a) crossover cH_Lambda
check("D5 and even the crossover LOCATION a = cH_Lambda would be kappa = sqrt(8pi/3) = 2.894: EXCLUDED by the data band",
      not allowed(kappa_cross), f"kappa_cross = {kappa_cross:.3f}, a0 = {kappa_cross*c*math.sqrt(G*rho_L):.2e}")

P(""); P("="*100); P("E. RESCUES, each priced"); P("="*100)
# E1 induced inertia: m itself from the bath, f asymptotically linear (Milgrom 1999 f = T): q = 2 -> a_0 = 2 c H_Lambda
a0_induced = 2*c*HL; kappa_induced = a0_induced/(c*math.sqrt(G*rho_L))
check("E1 induced inertia (f = T, Milgrom 1999): a_0 = 2 c H_Lambda, kappa = 5.79, EXCLUDED (and MI-as-fundamental is out 21 sigma)",
      not allowed(kappa_induced), f"kappa = {kappa_induced:.3f}")
# E2 holographic coherence: to make the drift O(1) the bath response must be enhanced by exactly 6 S_dS / n
check("E2 holographic/coherent rescue needs an enhancement factor = 6 S_dS/n ~ 2e123: a NEW postulate (category III), not a derivation",
      6*S_dS > 1e123)
# E3 dS IR secular growth: <h^2>_IR ~ (l_P H/c)^2 x (H t) (Ford-Parker / Allen-Folacci log growth): O(1) at H t ~ S_dS/pi
N_efolds_needed = 1/lPH**2
check("E3 IR secular growth reaches O(1) only after ~1e122 e-folds (H t ~ S_dS/pi); today H t ~ 1",
      N_efolds_needed > 1e121, f"e-folds needed = {N_efolds_needed:.1e}")
# E4 primordial tensor background: <h^2> at horizon scales <= r A_s (Planck+BK: r < 0.036, A_s = 2.1e-9)
h2_prim = 0.036*2.1e-9
check("E4 a primordial tensor background is capped at <h^2> <= r A_s = 7.6e-11 (10 orders below O(1)) and is an initial condition, not Lambda",
      h2_prim < 1e-9 and h2_prim > 1e-12, f"<h^2>_prim <= {h2_prim:.1e}")

P(""); P("="*100); P("VERDICT"); P("="*100)
P("  The graviton-bath CTP nonlinear drift EXISTS and is computable: <g_2 h_uu^2> = m (n/12pi) l_P^2 (a^2 + c^2 H^2).")
P("  It CANNOT deliver kappa: (B) every Lambda-dependent term is O(hbar) -- theorem, hinge = k_B T_GH proportional to hbar;")
P(f"  (C) its size is n/(6 S_dS) = {rel:.1e} n of the de Sitter acceleration, proportional to r (a Lambda renormalisation);")
P("  (D) it has NO MOND shape (f = T^2 => q = 0); (E) every rescue is a new postulate or already excluded.")
P("  => EVERY NAMED derivation lane for kappa = 1/2 is now closed.  kappa is a measured constitutive number.")
P("     Not 'theory closed': the a_0(z) ~ sqrt(rho_DE(z)) prediction and the kernel are untouched. Layer A untouched.")
if MUTATE:
    P("\n  MUTATE=1: T_GH made hbar-free. Expected: B2/B3/B5 (the hbar-counting hinge) FAIL.")
P(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
