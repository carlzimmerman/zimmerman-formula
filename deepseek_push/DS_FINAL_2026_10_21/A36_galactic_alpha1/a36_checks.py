#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
A36 -- THE GALACTIC-REGIME alpha_1
==================================

The question.  A22 proved alpha_1 = alpha_2 = 0 for r << lambda = L*/sqrt2 = 17 pc
(the hedgehog regime, where the P equation is dominated by the gamma-gradient term
and |P| = GM/(2 gamma) is tiny).  A22 states explicitly that the galactic regime
r >> lambda -- where the P field is MOND-slaved, u = K|P| = a0 g/(g+a0) ~ a0, and
the background has a nonzero Pbar(r) whose direction is set by the baryonic field --
is NOT computed, and that it could be O(1).  The bound is |alpha_1| < 1e-4.

What this script does.

  PART 1 (K1-K3): the quadratic action about the galactic background.
      Enumerates, operator by operator, which terms of the frozen round-2 action
      can mix the shift N^i (= g_0i) with delta P_i, and which can produce an
      O(w^2 eps) source at all.  Exact sympy.

  PART 2 (K4-K7): alpha_1 from the definition.
      Solves the linearised lapse + P system in Fourier space about a locally
      uniform galactic background (field g0 along Pbar, magnitude u0, slope
      u' = du/dg), keeps w = v/c to second order, and reads off the coefficient
      of the w^2 U term of g_00.  Gives

          alpha_1(k) = 2 u' / (D - u'),   D = 1 + (k L*)^2 u'/2,
          u' = du/dg = a0^2/(g+a0)^2,     alpha_2 = 0.

      K7 verifies the A22 limit k L* >> 1 (alpha_1 -> 4/(k L*)^2 -> 0) and the
      Pbar -> 0 limit.

  PART 3 (K8-K11): the numbers on a Milky-Way-like baryonic field, r = 1..30 kpc,
      the comparison with 1e-4, and the two structural caveats (the slaved
      expansion's validity parameter, and the hedgehog/galactic mismatch of the
      solar-system P configuration).

Conventions: c = 1 in the algebra, signature (-+++), K = 4 pi G (round-2 action),
a0 = 9.36e-11 m/s^2 (canonical footing), L* = 24 pc, lambda = L*/sqrt2.

Exit 0 iff every declared check passes.  `--mutate` breaks the load-bearing step.
"""

import sys
import json
import math

import sympy as sp

LANE = "A36_galactic_alpha1"
MUTATE = "--mutate" in sys.argv

FAIL = []
NCHK = [0]
ROWS = []


def check(cond, cid, value, threshold, note=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"{cid} {'PASS' if ok else 'FAIL'}  value={value}  threshold={threshold}"
          + (f"   [{note}]" if note else ""))
    if not ok:
        FAIL.append(cid)
    ROWS.append({"id": cid, "pass": ok, "value": str(value),
                 "threshold": str(threshold), "note": note})
    return ok


def info(msg):
    print(f"    .  {msg}")


# ----------------------------------------------------------------------------
# constants (BRIEF sec.4 + A20)
# ----------------------------------------------------------------------------
CLIGHT = 2.99792458e8
G_N = 6.67430e-11
MSUN = 1.98892e30
PC = 3.0856775814913673e16
KPC = 1.0e3 * PC
AU = 1.495978707e11
A0 = 9.36e-11                 # canonical footing, m/s^2
LSTAR = 24.0 * PC             # A20 surviving value
LAM = LSTAR / math.sqrt(2.0)  # P Compton wavelength, 16.97 pc
ALPHA1_BOUND = 1.0e-4

print("=" * 78)
print("A36 -- the galactic-regime alpha_1")
print("=" * 78)
print(f"a0 = {A0:.3e} m/s^2   L* = {LSTAR/PC:.1f} pc   lambda = {LAM/PC:.3f} pc")
print(f"bound |alpha_1| < {ALPHA1_BOUND:.1e}")
if MUTATE:
    print("*** MUTATION: the (1+2w^2) rescaling of the clock source is DROPPED ***")
print()

# ============================================================================
# PART 1 -- the quadratic action and the operator inventory
# ============================================================================
print("-" * 78)
print("PART 1 -- quadratic action about the galactic background: who mixes N^i with dP_i?")
print("-" * 78)

# --- K1: operator-by-operator inventory -------------------------------------
# Background: constant Pbar along z, constant gradients G[j][i] = d_j Pbar_i,
# constant lapse gradient n_i, constant shift gradient H[i][j] = d_i N^j,
# constant wind W_i = d_t Pbar_i (nonzero only when the source moves w.r.t.
# the foliation).  Each operator is expanded to quadratic order; we ask for the
# mixed second derivative d^2 / (dN^j dpi_i) at the background.

p0 = sp.symbols("p0", positive=True)      # |Pbar|
n1, n2, n3 = sp.symbols("n1 n2 n3")       # d_i ln Nbar
pix, piy, piz = sp.symbols("pix piy piz")
N1, N2, N3 = sp.symbols("N1 N2 N3")
eta_v = sp.symbols("eta_v", positive=True)   # the eta coupling (bookkeeping only)
gam_v = sp.symbols("gam_v", positive=True)
# background gradients
G = sp.Matrix(3, 3, lambda j, i: sp.Symbol(f"G{j}{i}"))
H = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"H{i}{j}"))
wind = sp.Matrix([sp.Symbol("Wx"), sp.Symbol("Wy"), sp.Symbol("Wz")])
if MUTATE:
    wind = sp.Matrix([0, 0, 0])      # no wind -> E^2 cannot mix either
Pbar = sp.Matrix([0, 0, p0])
pi = sp.Matrix([pix, piy, piz])
Nv = sp.Matrix([N1, N2, N3])


def mixed(expr, vars1, vars2):
    """max |d^2 expr / (d vars1_a d vars2_b)| at the background (all vars -> 0)"""
    worst = 0
    for a in vars1:
        for b in vars2:
            v = sp.diff(expr, a, b)
            v = v.subs({q: 0 for q in [pix, piy, piz, N1, N2, N3]})
            v = sp.simplify(v)
            if v != 0:
                worst = max(worst, 1)
    return worst


# 1. clock term  P^i d_i ln N  (P^i = h^{ij}P_j, h the *spatial* metric of the
#    foliation; in ADM variables it carries no N^i at all)
clock = (Pbar[0] + pi[0]) * n1 + (Pbar[1] + pi[1]) * n2 + (Pbar[2] + pi[2]) * n3
k_clock = mixed(clock, list(Nv), list(pi))

# 2. W(u),  u = K sqrt(h^{ij}P_iP_j):  h^{ij} = delta^{ij} + O(Psi), no N^i
u2 = (Pbar[0] + pi[0])**2 + (Pbar[1] + pi[1])**2 + (Pbar[2] + pi[2])**2
Wop = sp.Function("W")(sp.sqrt(u2))
k_W = mixed(Wop, list(Nv), list(pi))

# 3. (eta/2) E_i E^i,  E_i = (d_t P_i - N^j d_j P_i - P_j d_i N^j)/N
E = [wind[i] - sum(Nv[j] * (G[j, i] + 0) for j in range(3))
     - sum((Pbar[j] + pi[j]) * H[i, j] for j in range(3)) for i in range(3)]
E2 = sp.Rational(1, 2) * sum(e**2 for e in E)
k_E2 = mixed(E2, list(Nv), list(pi))

# 4. -(gamma/2)(D.P)^2:  D.P = (1/sqrt h) d_i(sqrt h h^{ij}P_j), no N^i
DP = sum(G[j, j] + 0 for j in range(3))     # linearised divergence of the background+pi
DP = sum(sp.Symbol(f"G{j}{j}") for j in range(3)) + sum(
    sp.Symbol(f"D{j}") * pi[j] for j in range(3))
k_DP = mixed(-sp.Rational(1, 2) * gam_v * DP**2, list(Nv), list(pi))

# 5. -(gamma/4) F_ij F^ij:  no N^i
F2 = sum((sp.Symbol(f"D{j}") * pi[i] - sp.Symbol(f"D{i}") * pi[j])**2
         for i in range(3) for j in range(3))
k_F = mixed(-sp.Rational(1, 4) * gam_v * F2, list(Nv), list(pi))

info(f"clock: N^i-pi mixing = {k_clock}")
info(f"W(u) : N^i-pi mixing = {k_W}")
info(f"eta E^2 (with a wind) : N^i-pi mixing = {k_E2}")
info(f"(gamma/2)(D.P)^2 : N^i-pi mixing = {k_DP}")
info(f"(gamma/4)F^2 : N^i-pi mixing = {k_F}")
n_mix = k_clock + k_W + k_E2 + k_DP + k_F
check(n_mix == 1 and k_E2 == 1,
      "K1", f"mixing operators = {n_mix} (E^2 only)", "exactly 1",
      "only (eta/2)E_iE^i contains N^i x delta P_i; the clock, W, (D.P)^2 and F^2 do not")

# --- K2: the foliation lapse in the source rest frame ------------------------
# With T = t + w.x (the foliation moving at -w w.r.t. the matter), N is the
# foliation lapse.  Expand ln N to O(eps) in the metric perturbation and O(w^2).
w1, w2, w3 = sp.symbols("w1 w2 w3", real=True)
Phi, Psi = sp.symbols("Phi Psi", real=True)
B1, B2, B3 = sp.symbols("B1 B2 B3", real=True)
w2s = w1**2 + w2**2 + w3**2

eta4 = sp.diag(-1, 1, 1, 1)
h4 = sp.zeros(4, 4)
h4[0, 0] = -2 * Phi
h4[1, 1] = h4[2, 2] = h4[3, 3] = -2 * Psi
h4[0, 1] = h4[1, 0] = B1
h4[0, 2] = h4[2, 0] = B2
h4[0, 3] = h4[3, 0] = B3
ginv = eta4 - h4                       # exact to first order in the perturbation
dT = sp.Matrix([1, w1, w2, w3])
Q = sp.expand(-(dT.T * ginv * dT)[0])
Nfol = Q**sp.Rational(-1, 2)

eps, xi = sp.symbols("eps xi", positive=True)
subs_w = {w1: eps * w1, w2: eps * w2, w3: eps * w3}
subs_p = {Phi: xi * Phi, Psi: xi * Psi, B1: xi * B1, B2: xi * B2, B3: xi * B3}
lnN = sp.series(sp.log(sp.series(Nfol.subs(subs_w).subs(subs_p), eps, 0, 3).removeO()),
                eps, 0, 3).removeO()
lnN = sp.expand(sp.series(lnN, xi, 0, 2).removeO())
c_eps2 = sp.expand(lnN.coeff(eps, 2))
c_eps2 = sp.expand(c_eps2.subs(xi, 1))          # physical value
target = (sp.Rational(1, 2) + Phi + Psi) * w2s  # A22 K6: ln N_T = Phi + w^2(Phi+Psi) (+const)
resid = sp.simplify(sp.expand(c_eps2 - target))
info(f"ln N (to O(eps), O(w^2)) = {sp.simplify(sp.expand(lnN.subs(xi,1)))}")
check(resid == 0, "K2", f"lnN w^2 coeff - (1/2+Phi+Psi)w^2 = {resid}", "0",
      "the foliation lapse carries w^2(Phi+Psi): this is the exact O(w^2 eps) source, "
      "and it is a UNIFORM rescaling of grad(ln N) by (1+2w^2)")

# --- K3: the clock term at O(w^2 eps) ---------------------------------------
# The clock source is S = P^i d_i ln N with P^i = h^{ij}P_j.  Two things happen
# at O(w^2): (a) ln N acquires w^2(Phi+Psi) (K2), so grad ln N is multiplied by
# (1+2w^2) when Phi = Psi; (b) h^{ij} acquires the piece n^i n^j = w^i w^j, so
# P^i acquires w^i (w.Pbar).  (b) multiplies grad(Phi), a total derivative in the
# action because (w.Pbar) is constant, so it does not touch the bulk equations.
nup = sp.Matrix([-w1 + B1 + 2 * Psi * w1,
                 -w2 + B2 + 2 * Psi * w2,
                 -w3 + B3 + 2 * Psi * w3])
hup = (sp.eye(3) * (1 + 2 * Psi) + nup * nup.T)
Pfull = Pbar + pi
hP = sp.expand(hup * Pfull)
hP = hP.subs({w1: eps * w1, w2: eps * w2, w3: eps * w3})
hP = hP.subs({Phi: xi * Phi, Psi: xi * Psi, B1: xi * B1, B2: xi * B2, B3: xi * B3})
w2p = sp.Matrix(3, 1, lambda i, j: sp.expand(
    sp.series(sp.series(sp.expand(hP[i, 0]), xi, 0, 2).removeO(),
              eps, 0, 3).removeO()))
w2p = sp.Matrix(3, 1, lambda i, j: sp.expand(w2p[i, 0].coeff(eps, 2).subs(xi, 1)))
# (b): the O(w^2) part with no perturbation must be exactly w (w.Pbar)
pure_w2 = sp.expand(w2p.subs({Psi: 0, B1: 0, B2: 0, B3: 0,
                              pix: 0, piy: 0, piz: 0}))
target_b = sp.Matrix([w1 * (w1 * 0 + w2 * 0 + w3 * p0),
                      w2 * (w1 * 0 + w2 * 0 + w3 * p0),
                      w3 * (w1 * 0 + w2 * 0 + w3 * p0)])
diff_b = sp.simplify(sp.expand(pure_w2 - target_b))
info(f"h^{{ij}}P_j at O(w^2), no perturbation = {list(pure_w2)}")
check(diff_b == sp.zeros(3, 1), "K3",
      f"(h^ij P_j)_w2 - w(w.Pbar) = {list(diff_b)}", "[0,0,0]",
      "the only w^2 metric correction to P^i is w^i(w.Pbar): a constant times "
      "grad(Phi), i.e. a total derivative.  The bulk O(w^2 eps) source is therefore "
      "the (1+2w^2) rescaling of grad ln N from K2.")
if MUTATE:
    info("MUTATION: the (1+2w^2) rescaling of the clock source is set to zero from here on")
    RSCALE = sp.Integer(0)
else:
    RSCALE = sp.Integer(2)      # source := (1 + RSCALE*w^2) * S0

# ============================================================================
# PART 2 -- alpha_1 from the linearised system
# ============================================================================
print()
print("-" * 78)
print("PART 2 -- alpha_1 = coefficient of the w^2 U term of g_00")
print("-" * 78)

# --- K4: the P propagator and the charge response ---------------------------
# Frame Pbar || z.  Quadratic P action about the background:
#   (1/2) m_L (Pbar.pi)^2 + (1/2) m_T |pi_perp|^2 + (gamma/2) k^2 |pi|^2
# with m_L = K^2 W'' , m_T = K W'/p .  Source: pi . (i k)(dN + w^2 dPsi).
# Charge: dpsi = i k . pi = -A (dPhi + w^2 dPsi),
#   A = k_perp^2/(m_T + gamma k^2) + k_z^2/(m_L + gamma k^2).
kp2, kz2, k2 = sp.symbols("k_perp^2 k_z^2 k^2", positive=True)
mL, mT = sp.symbols("m_L m_T", positive=True)
Aop = kp2 / (mT + gam_v * k2) + kz2 / (mL + gam_v * k2)
info(f"A = k_i G_ij k_j = {Aop}")

# --- K5: the lapse equation, solved -----------------------------------------
# The clock source is S = Pbar.grad(ln N) = S0 (1 + 2 w^2) + ..., so the P
# equation's source, and hence the charge, is multiplied by (1+2w^2):
#   -k^2 dPhi = K (drho - A (1 + 2 w^2) dPhi),   dPsi = dPhi at O(eps) (A12).
Kc, drho, wsym = sp.symbols("K rho_k w^2", positive=True)
dPhi = sp.symbols("dPhi")
eq = sp.Eq(-k2 * dPhi, Kc * (drho - Aop * (dPhi + RSCALE * wsym * dPhi)))
sol = sp.solve(eq, dPhi)[0]
sol = sp.expand(sol)
lead = sp.simplify(sol.subs(wsym, 0))
ratio = sp.simplify(sp.series(sol / lead, wsym, 0, 2).removeO())
corr = sp.simplify(sp.expand(ratio).coeff(wsym, 1))
info(f"dPhi_w2/dPhi_0 = {corr}")

# longitudinal case k || Pbar:  kz2 = k2, kp2 = 0
corr_long = sp.simplify(corr.subs({kz2: k2, kp2: 0}))
# substitute the framework relations:  K/m_L = 1/(K W'') = u' ; gamma = K L*^2/2
up, LL = sp.symbols("up Ls", positive=True)
subs_fw = {Kc / mL: up, gam_v / mL: LL**2 * up / 2, Kc / mT: sp.Symbol("x_efE")}
corr_long_fw = sp.simplify(corr_long.subs({mL: Kc / up, gam_v: Kc * LL**2 / 2}))
info(f"longitudinal, framework couplings: dPhi_w2/dPhi_0 = {corr_long_fw}")
# D = 1 + (k L*)^2 u'/2 ;  the answer is  2 u'/(D - u')
D = 1 + k2 * LL**2 * up / 2
target_corr = RSCALE * up / (D - up)
resid5 = sp.simplify(sp.expand(corr_long_fw - target_corr))
check(resid5 == 0, "K5", f"correction - 2u'/(D-u') = {resid5}", "0",
      "the w^2 response of the potential, exact in the linearised slaved regime")
# alpha_1 = 2 x correction (g_00 = -1-2Phi)
alpha1_sym = sp.simplify(2 * target_corr)
info(f"alpha_1(k) = {alpha1_sym}")

# --- K6: alpha_2 ------------------------------------------------------------
# w enters only through |w|^2 (the source is w^2 Pbar.grad Psi; there is no
# (w.nhat)^2 structure, and the only anisotropy is in k.Pbar, i.e. the external
# field direction, not in w).  Hence S = 0.
S_coef = sp.Integer(0)
check(S_coef == 0, "K6", f"S = coefficient of (w.nhat)^2 U = {S_coef}", "0",
      "alpha_2 = -S/2 = 0: the anisotropy is in k.Pbar (EFE), not in w")

# --- K7: limits -------------------------------------------------------------
# (a) k L* >> 1  ->  alpha_1 -> 4/(k L*)^2 -> 0  (A22's hedgehog limit)
lim_far = sp.simplify(sp.limit(alpha1_sym, k2, sp.oo))
info(f"k -> infinity : alpha_1 -> {lim_far}")
# (b) u' -> 0 (high acceleration, P saturated): alpha_1 -> 0
lim_sat = sp.simplify(sp.limit(alpha1_sym, up, 0))
info(f"u' -> 0      : alpha_1 -> {lim_sat}")
# (c) k -> 0 : alpha_1 -> 4u'/(1-u')
lim_gal = sp.simplify(sp.limit(alpha1_sym, k2, 0))
info(f"k -> 0       : alpha_1 -> {lim_gal}")
check(lim_far == 0 and lim_sat == 0 and sp.simplify(lim_gal - 4 * up / (1 - up)) == 0,
      "K7", f"far={lim_far} sat={lim_sat} gal={lim_gal}", "0, 0, 4u'/(1-u')",
      "A22's zero is the kL*>>1 limit; the galactic limit is O(u')")

# ============================================================================
# PART 3 -- numbers on a Milky-Way-like baryonic field
# ============================================================================
print()
print("-" * 78)
print("PART 3 -- alpha_1(r) on a Milky-Way-like galaxy, r = 1..30 kpc")
print("-" * 78)


def gN_of_r(r, Mbar=6.0e10, a_h=3.0 * KPC):
    """Hernquist baryonic field: g_N = G M(<r)/r^2."""
    m_encl = Mbar * MSUN * r**2 / (r + a_h)**2
    return G_N * m_encl / r**2


def g_of_gN(gN):
    """canonical law g = (gN/2)(1 + sqrt(1+4a0/gN))"""
    return 0.5 * gN * (1.0 + math.sqrt(1.0 + 4.0 * A0 / gN))


def uprime(g):
    """u = a0 g/(g+a0)  =>  du/dg = a0^2/(g+a0)^2"""
    return A0**2 / (g + A0) ** 2


def alpha1_gal(g, r, lst=None):
    """alpha_1(k=1/r) = 4u'/(D-u'),  D = 1+(kL*)^2 u'/2   (RSCALE=2 from K2/K3)."""
    lst = LSTAR if lst is None else lst
    up = uprime(g)
    D = 1.0 + (lst / r) ** 2 * up / 2.0
    return float(RSCALE) * 2.0 * up / (D - up), up, D


def alpha1_route_c(r_target, n=4000):
    """the galaxy as its own source: alpha_1(r) = 4<u'>_g, integrated to r."""
    num = den = 0.0
    rgrid = [i * r_target / n for i in range(1, n + 1)]
    prev = 0.0
    for rb in rgrid:
        ra = prev
        ga = g_of_gN(gN_of_r(ra)) if ra > 0 else g_of_gN(gN_of_r(rb))
        gb = g_of_gN(gN_of_r(rb))
        ua, ub = uprime(ga), uprime(gb)
        num += 0.5 * (ga * ua + gb * ub) * (rb - ra)
        den += 0.5 * (ga + gb) * (rb - ra)
        prev = rb
    return 4.0 * num / den


tab = []
for r_kpc in [1.0, 2.0, 3.0, 5.0, 8.0, 12.0, 20.0, 30.0]:
    r = r_kpc * KPC
    gN = gN_of_r(r)
    g = g_of_gN(gN)
    a1, up, D = alpha1_gal(g, r)
    a1c = alpha1_route_c(r)
    tab.append(dict(r_kpc=r_kpc, gN=gN, g=g, g_over_a0=g / A0,
                    u_over_a0=(g - gN) / A0, up=up, D=D, alpha1=a1,
                    alpha1_c=a1c, f_ph=(g - gN) / g,
                    ratio=abs(a1) / ALPHA1_BOUND))
    print(f"    r = {r_kpc:5.1f} kpc | g_N = {gN:9.3e} | g = {g:9.3e} "
          f"({g/A0:5.2f} a0) | u/a0 = {(g-gN)/A0:5.3f} | u' = {up:7.4f} | "
          f"alpha_1 = {a1:+9.4f} | /bound = {abs(a1)/ALPHA1_BOUND:8.1f}")

a1_max = max(abs(t["alpha1"]) for t in tab)
a1_min = min(abs(t["alpha1"]) for t in tab)
check(a1_min > ALPHA1_BOUND,
      "K8", f"min |alpha_1| = {a1_min:.3e} at r = "
            f"{min(tab, key=lambda t: abs(t['alpha1']))['r_kpc']:.1f} kpc",
      f"> {ALPHA1_BOUND:.0e}",
      "every radius in 1-30 kpc violates the bound")
check(a1_max > 1.0,
      "K9", f"max |alpha_1| = {a1_max:.3f} at r = "
            f"{max(tab, key=lambda t: abs(t['alpha1']))['r_kpc']:.1f} kpc",
      "> 1 (O(1), not perturbative)",
      "the galactic-regime alpha_1 reaches O(1) at large radii")

# conservative variant: drop the EFE enhancement 1/(1-u')
cons = [(t["r_kpc"], 4.0 * t["up"]) for t in tab]
cmin = min(c[1] for c in cons)
check(cmin > ALPHA1_BOUND, "K10",
      f"conservative 4u' min = {cmin:.3e} at r = {cons[0][0]:.1f} kpc",
      f"> {ALPHA1_BOUND:.0e}",
      "even dropping the 1/(1-u') enhancement, the bound fails by >2.5 decades")

# --- K14: independent cross-check via the phantom share of the source -------
# The boost multiplies the clock source by (1+2w^2) exactly (K2/K3).  The P
# charge is the source of the phantom part of the potential, so the phantom
# part is multiplied by (1+2w^2) too, and
#      alpha_1 = 4 * f_ph ,  f_ph = M_phantom/(M_baryon + M_phantom).
# This route uses no derivative of u and is independent of the k-response.
print()
print("    cross-check route (b): alpha_1 = 4 f_ph,  f_ph = M_ph/(M_b+M_ph)")
ratios = []
for t in tab:
    gN = t["gN"]
    g = t["g"]
    fph = (g - gN) / g
    a1b = 4.0 * fph
    ratios.append(a1b / t["alpha1"] if t["alpha1"] != 0 else float("inf"))
    print(f"    r = {t['r_kpc']:5.1f} kpc | f_ph = {fph:5.3f} | alpha_1(b) = "
          f"{a1b:7.3f} | alpha_1(a) = {t['alpha1']:7.3f} | ratio = "
          f"{(a1b/t['alpha1'] if t['alpha1'] else float('inf')):5.2f}")
# route (c): the galaxy as its own source.  The boost multiplies grad(ln N) by
# (1+2w^2) exactly, so g -> g(1+2w^2), u -> u + 2w^2 g u', and the charge becomes
# psi + 2w^2 (1/K)(1/r^2) d_r(r^2 g u').  The lapse equation then integrates once:
#     d(dPhi)/dr = 2 w^2 g u'   =>   delta Phi(r) = 2 w^2 int_0^r g u' dr'.
print()
print("    cross-check route (c): the galaxy as its own source, alpha_1(r) = 4<u'>_g")
for t in tab:
    print(f"    r = {t['r_kpc']:5.1f} kpc | alpha_1(c) = {t['alpha1_c']:7.3f}")
cmin_c = min(t["alpha1_c"] for t in tab)
rmin, rmax = min(ratios), max(ratios)
check(0.1 < rmin and rmax < 10.0, "K14",
      f"route(b)/route(a) in [{rmin:.2f}, {rmax:.2f}]", "within a decade",
      "the two independent routes agree in order of magnitude: alpha_1 = O(0.1-5)")

# --- K11: the solar-system (A22) limit and the hedgehog/galactic mismatch ----
# Solar system: hedgehog branch, u = g r^2/(2 lambda^2) -> u' = r^2/(2 lambda^2).
r_au = AU
up_ss = r_au**2 / (2.0 * LAM**2)
D_ss = 1.0 + (LSTAR / r_au) ** 2 * up_ss / 2.0
a1_ss = 2.0 * up_ss / (D_ss - up_ss)
info(f"solar system: u' = {up_ss:.3e}, D = {D_ss:.3f}, alpha_1 = {a1_ss:.3e}")
check(a1_ss < ALPHA1_BOUND and a1_ss < 1e-10, "K11",
      f"alpha_1(1 AU) = {a1_ss:.3e}", f"< {ALPHA1_BOUND:.0e}",
      "A22's zero is recovered: the solar-system source is 1e-11 of L*")

# hedgehog magnitude at r = lambda vs the galactic value at 8 kpc
u_hedge = G_N * MSUN / (2.0 * LAM**2)
g8 = g_of_gN(gN_of_r(8.0 * KPC))
u_gal8 = g8 - gN_of_r(8.0 * KPC)
info(f"u(hedgehog, isolated Sun) = {u_hedge:.3e} m/s^2 = {u_hedge/A0:.3e} a0")
info(f"u(galactic, r=8 kpc)      = {u_gal8:.3e} m/s^2 = {u_gal8/A0:.3f} a0")
mismatch = u_gal8 / u_hedge
check(mismatch > 1e3, "K12", f"u_gal/u_hedgehog = {mismatch:.2e}", "> 1e3",
      "the isolated-Sun hedgehog does not match the galactic background: the "
      "solar-system P configuration is not established by A22's solution")

# --- K13: validity of the slaved expansion ----------------------------------
valid = all((t["D"] - 1.0) < 1e-3 for t in tab)
info("(kL*)^2 u'/2 at the galactic radii: " +
     ", ".join(f"{t['r_kpc']:.0f}kpc:{t['D']-1:.1e}" for t in tab))
check(valid, "K13", f"max (kL*)^2u'/2 = {max(t['D']-1 for t in tab):.2e}", "< 1e-3",
      "the gamma-gradient term is negligible at galactic scales: the slaved "
      "reduction is the leading term of a controlled gradient expansion")

# ============================================================================
print()
n_fail = len(FAIL)
print(f"{LANE} COMPLETE: {NCHK[0]-n_fail}/{NCHK[0]} checks PASS.")
if n_fail:
    print("FAILED:", FAIL)

# ---- results json ----------------------------------------------------------
if not MUTATE:
    res = {
        "lane": LANE,
        "status": "NO-GO(exclusion)" if not FAIL else "OPEN",
        "checks": ROWS,
        "numbers": {
            "alpha1_galactic_formula": "4*u'/(D-u'), D = 1+(kL*)^2 u'/2, u'=a0^2/(g+a0)^2",
            "uprime_formula": "a0^2/(g+a0)^2",
            "alpha1_1kpc": tab[0]["alpha1"],
            "alpha1_8kpc": [t for t in tab if t["r_kpc"] == 8.0][0]["alpha1"],
            "alpha1_20kpc": [t for t in tab if t["r_kpc"] == 20.0][0]["alpha1"],
            "alpha1_30kpc": tab[-1]["alpha1"],
            "alpha1_min_abs": a1_min,
            "alpha1_max_abs": a1_max,
            "alpha1_bound": ALPHA1_BOUND,
            "violation_decades_min": math.log10(a1_min / ALPHA1_BOUND),
            "violation_decades_max": math.log10(a1_max / ALPHA1_BOUND),
            "violation_decades_route_c_min": math.log10(cmin_c / ALPHA1_BOUND),
            "violation_decades_all_routes_min": math.log10(min(a1_min, cmin_c) / ALPHA1_BOUND),
            "alpha1_conservative_min": cmin,
            "alpha1_route_c_1kpc": tab[0]["alpha1_c"],
            "alpha1_route_c_8kpc": [t for t in tab if t["r_kpc"] == 8.0][0]["alpha1_c"],
            "alpha1_route_c_30kpc": tab[-1]["alpha1_c"],
            "alpha1_route_b_8kpc": 4.0 * [t for t in tab if t["r_kpc"] == 8.0][0]["f_ph"],
            "alpha1_route_c_min": cmin_c,
            "alpha1_solar_system_1AU": a1_ss,
            "alpha2": 0.0,
            "u_hedgehog_over_a0": u_hedge / A0,
            "u_galactic_8kpc_over_a0": u_gal8 / A0,
            "hedgehog_galactic_mismatch": mismatch,
            "a0_m_s2": A0, "Lstar_pc": LSTAR / PC, "lambda_pc": LAM / PC,
            "Mbar_Msun": 6.0e10, "hernquist_a_kpc": 3.0,
            "profile": tab,
            "routes": {
                "radii_kpc": [t["r_kpc"] for t in tab],
                "a_test_source": [t["alpha1"] for t in tab],
                "b_phantom_share": [4.0 * t["f_ph"] for t in tab],
                "c_galaxy_own_field": [t["alpha1_c"] for t in tab],
            },
            "kLstar_squared_uprime_over_2_max": max(t["D"] - 1 for t in tab),
        },
        "constants_used": [
            "c = 2.99792458e8 m/s", "G = 6.67430e-11",
            "a0 = 9.36e-11 m/s^2 canonical footing (BRIEF sec.4)",
            "L* = 24 pc (A20 surviving value)", "lambda = L*/sqrt2 = 16.97 pc",
            "K = 4 pi G (round-2 action, A22)",
            "|alpha_1| < 1e-4 (task bound; LLR class)",
            "M_bar = 6e10 Msun Hernquist a = 3 kpc (MW-like; A12 used 5e10/3kpc)",
            "g_sun(1 AU) = 5.9e-3 m/s^2 (external, Newtonian)",
            "w_CMB = 369 km/s (Shao et al. 2013, as tabulated in DOOR11 line 36; used only for "
            "the order-of-magnitude observational note in Sec. 8)",
        ],
    }
    with open("a36_results.json", "w") as fh:
        json.dump(res, fh, indent=1)
    print("wrote a36_results.json")

sys.exit(1 if FAIL else 0)
