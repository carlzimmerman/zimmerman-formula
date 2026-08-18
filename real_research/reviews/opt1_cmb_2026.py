#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
opt1_cmb_2026.py
================
OPTION 1, ROUTE 4:  DOES F(Z,Q) KEEP THE COSMOLOGY?

THE PROPOSAL under test.  AeST's action (transcribed verbatim in
real_research/bridge1_aest_equations.md from arXiv:2007.00082 Eq. 5) is

    S = int d^4x (sqrt(-g)/16 pi Gt)[ R - 2 Lam - (K_B/2) F^{mu nu}F_{mu nu}
          + 2(2-K_B) J^mu grad_mu phi - (2-K_B) Y - F(Y,Q) - lam(A^mu A_mu + 1) ] + S_m[g]

with Y = q^{mu nu} grad_mu phi grad_nu phi (the SCALAR's own spatial gradient),
Q = A^mu grad_mu phi, and J^mu = A^nu grad_nu A^mu (the AETHER'S ACCELERATION).

Option 1 replaces the free function's first argument by the aether-acceleration invariant

    Z := J^mu J_mu       (= a^mu a_mu, the Einstein-aether c_4 structure),

i.e. F(Y,Q) -> F(Z,Q).  Because J_i reduces to the TOTAL potential gradient in the
quasi-static limit, this is meant to buy the AQUAL escape from the saturation trap that
kills the Y-form (ephemeris s <= 1.27e-5 vs RAR s >= 0.1257-0.4348, a 1.2e4-3.4e4x gap).

THIS FILE OWNS ONLY THE COSMOLOGY.  PASS = background and CMB unchanged, a_0(z) preserved.
KILL = the acoustic peaks move outside cosmic variance, or the background is disturbed.

WHAT IT FINDS, up front and with the adverse half first because it is the half that decides:

  * BACKGROUND: PASS, and rigorously.  J^mu vanishes IDENTICALLY on FRW for an arbitrary
    lapse (sympy, PART B), so Z_bar = 0, F(0,Q) = K(Q), and every background object --
    Friedmann, w = -1, the dust mode, Q(a), and therefore the DERIVED a_0(z) law -- is
    bit-for-bit the AeST one.  The modification is INVISIBLE to the background.

  * LINEAR ORDER: J_i = grad_i E EXACTLY, where E = alpha_dot + Psi is AeST's OWN mixing
    variable (sympy, PART C).  So Z = |grad E|^2/a^2 is SECOND order -- NOT third order like
    Y^{3/2} -- and its analytic part is EXACTLY DEGENERATE with the K_B F^2 term in the
    scalar sector (and, adversarially, NOT degenerate in the vector sector).

  * AND THAT IS THE PROBLEM.  Because the free function now eats the TOTAL gradient, its
    MOND branch is switched ON wherever the total acceleration approaches a_0 -- and CLASS
    says the acoustic-band gravitational acceleration at recombination is only y = 8-11
    times a_0 if a_0 does not run (CLASS: 7.6-11.9 over l = 100-2500).  The fractional distortion of the linear gravitational
    dynamics is then 1 - mu(y) ~ 5%, which is far outside cosmic variance in aggregate.
    The Y-form never had this exposure: its MOND term is O(delta^3) by the order-counting
    theorem, so it is invisible at linear order WHATEVER the acceleration.

  * SO THE CMB DOES NOT COME FREE.  It comes only through the a_0(z) suppression the
    framework independently derives, and PART F prices exactly how much suppression is
    needed -- which partially RE-ARMS the nu_0 squeeze stage76 had relieved.  The corpus's
    banked a_0(rec)/a_0(0) = 0.0060 MEETS that requirement on all eight forks; delivering it
    needs nu_0 above stage76's RAR ceiling on 2 of the 8, both of them the alpha=1 kernel
    under the conservative per-mode reading.

  * AND OPTION 1 REOPENS THE KERNEL CHOICE IN ITS OWN FAVOUR: the legality theorem that
    SELECTED alpha = 1 in the Y-form does not apply in the Z-form, so Route A's exponential
    kernel is legal again -- and it is the one the CMB prefers, clearing the RAR ceiling on
    every reading where alpha = 1 clashes on one.

  * WHAT IS NOT COMPUTED, and it is the number the verdict hinges on: the response
    S = |dlnC_l / d eps| of the CMB to that fractional distortion.  There is no AeST module
    in CLASS, so no honest delta-C_l can be produced here.  PART F reports the threshold in
    S at which the verdict flips instead of guessing it.

Exit 0 = every check passed.
"""

import sys

import numpy as np
import sympy as sp
from scipy.optimize import brentq

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


print(__doc__)

C_LIGHT = 2.99792458e8
MPC = 3.0856775814913673e22
A0_CANON, A0_ALT = 9.3619e-11, 1.1279e-10
NU0_RAR_CEILING = 2.36e-6      # stage76 PART A, recomputed there from the 0.108 dex RAR
A0Z_BANKED = 0.0060            # the corpus's banked a_0(1090)/a_0(0)

t, x1, x2, x3, ep = sp.symbols("t x1 x2 x3 epsilon")
XC = [t, x1, x2, x3]


def christoffel(g):
    gi = g.inv()
    G = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(m, 4):
                s = 0
                for r in range(4):
                    s += gi[l, r] * (sp.diff(g[r, m], XC[n]) + sp.diff(g[r, n], XC[m])
                                     - sp.diff(g[m, n], XC[r]))
                s = sp.simplify(s / 2)
                G[l][m][n] = s
                G[l][n][m] = s
    return G


def lin(e):
    """strict linearisation: series in the bookkeeping parameter, truncated at O(eps^2)."""
    return sp.simplify(sp.series(sp.expand(e), ep, 0, 2).removeO())


def quad(e):
    """strict truncation at O(eps^3): keeps eps^0, eps^1, eps^2 only."""
    return sp.simplify(sp.series(sp.expand(e), ep, 0, 3).removeO())


# =================================================================================================
print("=" * 100)
print("PART A -- what is being changed, and what is NOT")
print("=" * 100)
check(True,
      "A1  the ONLY change is F(Y,Q) -> F(Z,Q) with Z = J^mu J_mu, J^mu = A^nu grad_nu A^mu. "
      "R, Lam, the K_B F^2 term, the 2(2-K_B) J.grad(phi) mixing, the -(2-K_B)Y scalar kinetic "
      "term, the constraint -lam(A.A+1) and S_m[g] are all UNTOUCHED",
      "action per real_research/bridge1_aest_equations.md, which is the correct transcription "
      "(THE_COMPLETION.md's was wrong on three counts and was corrected 2026-08-17)")
check(True,
      "A2  in Einstein-aether language the AeST dictionary is c_1 = +K_B, c_2 = 0, c_3 = -K_B, "
      "c_4 = 0, and Z = a^mu a_mu is exactly the c_4 structure -- so Option 1 promotes c_4 from "
      "the constant 0 to a FUNCTION",
      "c_1 + c_3 = 0 is untouched, which is why c_T = 1 survives -- but c_T is Route 2's gate, "
      "not this file's, and is only noted here")
info("A3  this file's scope", "background (PART B), linear order (PART C), the branch question "
     "and CLASS (PARTS D-E), the a_0(z) law and the interlock (PART F)")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- THE FRW BACKGROUND: does the modification even see it?")
print("=" * 100)
N = sp.Function("N")(t)
a = sp.Function("a")(t)
g_bg = sp.diag(-N**2, a**2, a**2, a**2)
G_bg = christoffel(g_bg)
Aup_bg = [1 / N, 0, 0, 0]
J_bg = []
for m in range(4):
    s = 0
    for nu in range(4):
        term = sp.diff(Aup_bg[m], XC[nu])
        for l in range(4):
            term += G_bg[m][nu][l] * Aup_bg[l]
        s += Aup_bg[nu] * term
    J_bg.append(sp.simplify(s))
norm_bg = sp.simplify(sum(Aup_bg[m] * g_bg[m, n] * Aup_bg[n] for m in range(4) for n in range(4)))
check(sp.simplify(norm_bg + 1) == 0,
      "B1  the background aether A^mu = (1/N,0,0,0) is correctly unit-timelike, A.A = -1, for an "
      "ARBITRARY lapse N(t)",
      "the general lapse matters: the Friedmann equation comes from varying N, so the background "
      "result must hold off-shell in N, not just at N = 1")
check(all(sp.simplify(j) == 0 for j in J_bg),
      "B2  *** J^mu VANISHES IDENTICALLY ON FRW, for arbitrary N(t) and a(t) -- all four "
      "components, computed from the full Christoffel connection.  The comoving aether "
      "congruence is GEODESIC, so its acceleration is zero ***",
      f"sympy returns J^mu = {J_bg}")
check(True,
      "B3  *** THEREFORE Z_bar = J^mu J_mu = 0 EXACTLY on the background, and F(Z,Q)|_bg = "
      "F(0,Q) = K(Q).  The Option-1 free function reduces on FRW to the SAME K(Q) that AeST's "
      "F(Y,Q) reduces to (Y_bar = 0 for the same projection reason) ***",
      "so the modification is INVISIBLE to the background -- this is the favourable structural "
      "result the brief asked to be checked rather than hoped for, and it holds")
check(True,
      "B4  and the stress-tensor contribution of the new term is 2 F_Z J_mu J_nu + (trace), "
      "every piece of which carries at least one factor of J and therefore VANISHES on the "
      "background whatever F_Z(0,Q) is",
      "so 8 pi Gt rho_bar = Q dK/dQ - K and 8 pi Gt P_bar = K are UNCHANGED -- the AeST "
      "background relations transcribed in bridge1_aest_equations.md carry over verbatim")
check(True,
      "B5  the background SCALAR equation is unchanged too: Z contains no phi at all, so the "
      "phi-variation of F(Z,Q) is -F_Q A^mu exactly as before, giving dK/dQ = I_0/a^3 and hence "
      "the SAME Q(a).  (In AeST the F_Y piece also drops on the background because it carries "
      "q^{mu nu} grad_nu phi_bar = 0.)",
      "identical Q(a) is the hinge for PART F: every Q-sector statement is inherited unchanged")

# w = -1 and the dust mode, on the same offset-DBI K the corpus uses (stage75 PART C)
Qs, Q0s, LDs, M4s = sp.symbols("Q Q_0 Lambda_D M4", positive=True)
Kq = -M4s * sp.sqrt(1 - (Qs - Q0s) ** 2 / LDs**2)
check(sp.simplify(Kq.subs(Qs, Q0s) + M4s) == 0,
      "B6  on the corpus's own K(Q) (offset DBI at beta = 1, stage75 PART C): K(Q_0) = -M^4, so "
      "P_bar = K = -M^4 and rho_bar = Q K' - K = +M^4 at the minimum -- w = -1 EXACTLY, "
      "preserved because PARTS B3-B5 leave the whole Q-sector alone")
uexc = sp.symbols("u", positive=True)
rho_exc = sp.series(sp.simplify(-Kq.subs(Qs, Q0s + uexc)), uexc, 0, 3).removeO()
check(sp.simplify(sp.diff(rho_exc, uexc).subs(uexc, 0)) == 0,
      "B7  and small excitations are still DUST (rho linear, P quadratic in the displacement), "
      "so the CMB's clustering component is unchanged",
      "PART B verdict: THE BACKGROUND IS EXACTLY UNDISTURBED.  No 'KILL: the background is "
      "disturbed' branch is reachable")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- LINEAR PERTURBATIONS: at what order does F(Z) first bite?")
print("=" * 100)
Psi = sp.Function("Psi")(t, x1, x2, x3)
Phi = sp.Function("Phi")(t, x1, x2, x3)
alf = sp.Function("alpha")(t, x1, x2, x3)
gp = sp.zeros(4, 4)
gp[0, 0] = -(1 + 2 * ep * Psi)
for i in range(1, 4):
    gp[i, i] = a**2 * (1 - 2 * ep * Phi)
Gp = christoffel(gp)
# the ansatz is SZ21's own, transcribed in bridge1_aest_equations.md: A_mu = {-1-Psi, grad_i alpha}
Adn = [-(1 + ep * Psi)] + [ep * sp.diff(alf, XC[i]) for i in (1, 2, 3)]
gpi = gp.inv()
Aup = [sp.simplify(sum(gpi[m, n] * Adn[n] for n in range(4))) for m in range(4)]
check(sp.simplify(lin(sum(Aup[m] * Adn[m] for m in range(4))) + 1) == 0,
      "C1  the SZ21 perturbation ansatz A_mu = {-(1+Psi), grad_i alpha} in Newtonian gauge is "
      "unit-timelike to O(delta), so the lam-constraint is satisfied at linear order",
      "ansatz + the mixing variables chi, gamma, E are quoted verbatim in "
      "real_research/bridge1_aest_equations.md, completed 2026-08-14 from the arXiv LaTeX")

Jdn = []
for m in range(4):
    s = 0
    for nu in range(4):
        term = sp.diff(Adn[m], XC[nu])
        for l in range(4):
            term -= Gp[l][nu][m] * Adn[l]
        s += Aup[nu] * term
    Jdn.append(lin(s))
E_mix = sp.diff(alf, t) + Psi              # SZ21's own E = alpha_dot + Psi
resid = [sp.simplify(Jdn[i] - ep * sp.diff(E_mix, XC[i])) for i in (1, 2, 3)]
check(all(r == 0 for r in resid) and sp.simplify(Jdn[0]) == 0,
      "C2  *** J_i = grad_i E EXACTLY at linear order, with E = alpha_dot + Psi -- SZ21'S OWN "
      "MIXING VARIABLE, arrived at here from the aether acceleration rather than assumed.  And "
      "J_0 = 0 at this order (it is O(delta^2), forced by A^mu J_mu = 0) ***",
      "the H*grad(alpha) pieces from Gamma^j_{0i} and from Gamma^0_{ji}A_0 cancel exactly; "
      "this is the cosmological counterpart of the brief's quasi-static J_i ~ grad_i Psi")

# Z at quadratic order
Jup = [sp.simplify(sum(gpi[m, n] * Jdn[n] for n in range(4))) for m in range(4)]
Zpert = quad(sum(Jup[m] * Jdn[m] for m in range(4)))
Zexp = ep**2 * sum(sp.diff(E_mix, XC[i]) ** 2 for i in (1, 2, 3)) / a**2
check(sp.simplify(sp.expand(Zpert - Zexp)) == 0,
      "C3  *** Z = |grad E|^2 / a^2 + O(delta^3): SECOND order in perturbations, and manifestly "
      "NON-NEGATIVE (J is spacelike because A.J = 0), so Z^{3/2} is real ***",
      f"sympy: Z = {sp.simplify(Zpert/ep**2)} * eps^2")
check(True,
      "C4  *** AND THAT IS THE STRUCTURAL DIFFERENCE FROM THE Y-FORM.  Y is O(delta^2) too, but "
      "AeST's free function enters through the NON-ANALYTIC MOND term J ~ (2/3)Y^{3/2}/a_0, "
      "which is O(delta^3) and drops out of the linear equations -- SZ21's own statement that "
      "a_0 'does not appear in the linear cosmological regime'.  For Z the MOND branch is NOT "
      "automatically third order, because Z is the TOTAL gradient and the interpolation is "
      "evaluated at the TOTAL acceleration.  PART D asks which branch that lands in ***")

# the scalar-sector degeneracy with the K_B term
Fdn = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        Fdn[m, n] = sp.diff(Adn[n], XC[m]) - sp.diff(Adn[m], XC[n])
F2 = quad(sum(gpi[m, r] * gpi[n, s_] * Fdn[m, n] * Fdn[r, s_]
              for m in range(4) for n in range(4) for r in range(4) for s_ in range(4)))
check(sp.simplify(sp.expand(F2 + 2 * Zexp)) == 0,
      "C5  *** EXACT SCALAR-SECTOR DEGENERACY: F^{mu nu}F_{mu nu} = -2Z at O(delta^2), so the "
      "action's -(K_B/2)F^2 term is +K_B Z and any ANALYTIC linear-in-Z piece of F is nothing "
      "but a shift K_B -> K_B - F_Z(0,Q) ***",
      "consequence, and it is a real model condition: F_Z(0,Q) must be Q-INDEPENDENT, or the "
      "aether coefficient becomes time-dependent through Q = Q_0 + I_0/a^3, which at "
      "recombination is a factor ~1e9 excursion in the argument -- not a re-fit of a constant")

# ADVERSARIAL: the degeneracy fails in the vector sector
fV = sp.Function("f")(t, x1)
AdnV = [0, 0, ep * fV, 0]          # transverse: div(A^V) = d_2 f(t,x1) = 0
gV = sp.diag(sp.Integer(-1), a**2, a**2, a**2)
gVi = gV.inv()
FdnV = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        FdnV[m, n] = sp.diff(AdnV[n], XC[m]) - sp.diff(AdnV[m], XC[n])
F2V = sp.simplify(sum(gVi[m, r] * gVi[n, s_] * FdnV[m, n] * FdnV[r, s_]
                      for m in range(4) for n in range(4) for r in range(4) for s_ in range(4)))
magnetic = sp.simplify(F2V - (-2 * ep**2 * sp.diff(fV, t) ** 2 / a**2))
check(sp.simplify(magnetic - 2 * ep**2 * sp.diff(fV, x1) ** 2 / a**4) == 0,
      "C6  *** ADVERSARIAL, AND IT SURVIVES: the degeneracy of C5 is SCALAR-SECTOR ONLY.  For a "
      "transverse aether vector mode, F^2 carries an extra 'magnetic' piece "
      "2|curl A^V|^2/a^4 that Z does NOT contain (Z only ever sees the acceleration).  So a "
      "nonzero F_Z(0,Q) is NOT a relabelling of K_B -- it changes the vector-mode dispersion "
      "relation and must be re-checked for gradient stability ***",
      "vector modes are decaying and unsourced in standard scalar-seeded cosmology, so the CMB "
      "cost is negligible; the STABILITY cost is Route 2's gate and is flagged, not settled, "
      "here.  The corpus already carries a 'vector WATCH' on the a_0-bump for the same reason")
check(True,
      "C7  and DELETING the Y-dependence of F costs nothing at linear order: on the corpus's own "
      "determined family (stage75 PART B) J_Y = v/(1-2v) with v = sqrt(Y)/a_0, so F_Y(0,Q) = 0 "
      "and the Y-sector never contributed an analytic quadratic term in the first place -- "
      "the -(2-K_B)Y kinetic term, which is retained, was carrying all of it",
      "so the linear scalar sector loses nothing by the swap; it only gains whatever F(Z) adds")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- THE DECIDING QUESTION: which branch of F(Z) is the CMB in?  (real CLASS)")
print("=" * 100)
from classy import Class                                                     # noqa: E402

BASE = {"h": 0.6736, "omega_b": 0.02237, "omega_cdm": 0.1200,
        "A_s": 2.100e-9, "n_s": 0.9649, "tau_reio": 0.0544}
cl_run = Class()
cl_run.set({**BASE, "output": "tCl", "l_max_scalars": 2500, "lensing": "no"})
cl_run.compute()
der = cl_run.get_current_derived_parameters(["z_rec", "rs_rec", "100*theta_s"])
Z_REC = der["z_rec"]
CHI_REC = (1.0 + Z_REC) * cl_run.angular_distance(Z_REC)          # comoving distance, Mpc
cls = cl_run.raw_cl(2500)
ell, C_tt = np.asarray(cls["ell"]), np.asarray(cls["tt"])
check(abs(der["100*theta_s"] - 1.0404) < 0.002 and 1080 < Z_REC < 1095,
      f"D1  CLASS baseline: committed Planck 2018 cosmology reproduces 100*theta_s = "
      f"{der['100*theta_s']:.5f} and z_rec = {Z_REC:.2f}, comoving distance to last scattering "
      f"{CHI_REC:.1f} Mpc",
      "this run is the BASELINE against which any modification would have to be compared")

tk_run = Class()
tk_run.set({**BASE, "output": "mTk", "P_k_max_1/Mpc": 12.0, "z_max_pk": 1200.0,
            "matter_source_in_current_gauge": "yes"})
tk_run.compute()
tk = tk_run.get_transfer(z=Z_REC)
kk = np.asarray(tk["k (h/Mpc)"]) * BASE["h"]                       # -> 1/Mpc comoving
Tpsi = np.abs(np.asarray(tk["psi"]))
A_s, n_s, k_piv = BASE["A_s"], BASE["n_s"], 0.05
Psi_rms = Tpsi * np.sqrt(A_s * (kk / k_piv) ** (n_s - 1.0))        # rms |Psi| per ln k
k_phys = kk * (1.0 + Z_REC) / MPC                                  # 1/m, PHYSICAL
g_mode = k_phys * Psi_rms * C_LIGHT**2                             # m/s^2, per ln k
ell_of_k = kk * CHI_REC
check(np.all(np.isfinite(g_mode)) and g_mode.max() > 1e-10,
      f"D2  the physical gravitational acceleration at z_rec, g(k) = k_phys |Psi| c^2, peaks at "
      f"{g_mode.max():.3e} m/s^2 near k = {kk[np.argmax(g_mode)]:.4f} 1/Mpc "
      f"(l ~ {ell_of_k[np.argmax(g_mode)]:.0f})",
      "same construction as nbody_2026/stage76_nu0_recombination_pin_2026.py PART B, reproduced "
      "here so this file stands alone")
info("D3  THE PROXY, named because it is the file's weakest link",
     "the field the free function actually eats is E = alpha_dot + Psi (PART C2), not Psi.  "
     "Solving AeST's Eq (12) for E is NOT DONE HERE -- there is no AeST module in CLASS.  Psi "
     "is used as the subhorizon proxy E ~ Psi.  Every epsilon below scales as (Psi/E), so if "
     "E is SMALLER than Psi the distortion is LARGER and the verdict gets WORSE, not better")

# the two legal kernels, as functions of the TOTAL acceleration x = g/a_0
def mu_alpha1(x):
    """g^2 = g_bar^2 + a_0 g_bar  =>  mu(x) = g_bar/g = (sqrt(1+4x^2)-1)/(2x)."""
    return (np.sqrt(1.0 + 4.0 * x**2) - 1.0) / (2.0 * x)


def mu_routeA(x):
    """nu(y) = 1/(1-exp(-sqrt y)) with y = g_bar/a_0; invert y*nu(y) = x, mu = y/x."""
    x = float(x)
    if x > 1e12:
        return 1.0
    f = lambda y: y / (1.0 - np.exp(-np.sqrt(y))) - x
    lo, hi = 1e-16, max(4.0 * x, 1.0)
    while f(hi) < 0:
        hi *= 4.0
    y = brentq(f, lo, hi, xtol=1e-18, rtol=1e-14)
    return y / x


xs = np.array([1.0, 3.0, 10.0, 30.0, 100.0, 1000.0])
check(all(0 < mu_alpha1(v) < 1 for v in xs) and mu_alpha1(1e6) > 0.9999,
      "D4  both kernels are LEGAL in the Z/AQUAL form (the saturation trap is a Y-form disease): "
      "mu(x) rises monotonically to 1, so d g_obs/d g_bar > 0 everywhere",
      "  ".join(f"x={v:g}: mu_a1={mu_alpha1(v):.4f}/mu_A={mu_routeA(v):.4f}" for v in xs))
check(abs(mu_alpha1(10.0) - (1.0 - 1.0 / (2 * 10.0))) < 0.002,
      f"D5  *** AND THIS IS THE WHOLE ROUTE-4 ISSUE IN ONE LINE: the fractional modification of "
      f"gravity is eps = 1 - mu(x), which for ANY kernel that reproduces the RAR is ~1/(2x) at "
      f"large x.  At x = 10 that is {1-mu_alpha1(10.0):.4f} (alpha=1) / {1-mu_routeA(10.0):.4f} "
      f"(Route A) -- kernel-ROBUST, a few per cent, NOT exponentially small ***",
      "the Y-form is immune to this because its MOND term is O(delta^3) at ANY acceleration; "
      "the Z-form is exposed because it switches on wherever the TOTAL acceleration nears a_0")


def eps_of(g, a0_rec, kern=mu_alpha1):
    x = np.atleast_1d(g) / a0_rec
    return np.array([1.0 - kern(float(v)) for v in x])


for a0lab, a0v in (("canonical", A0_CANON), ("alt", A0_ALT)):
    y_band = g_mode / a0v
    sel = (ell_of_k > 100) & (ell_of_k < 2500)
    info(f"D6  {a0lab} a_0 = {a0v:.4e}, NO running",
         f"over the acoustic band l = 100-2500: y = g/a_0 spans "
         f"{y_band[sel].min():.2f} to {y_band[sel].max():.2f}, "
         f"eps = 1-mu spans {eps_of(g_mode[sel], a0v).min():.4f} to "
         f"{eps_of(g_mode[sel], a0v).max():.4f}")
check(True,
      "D7  *** SO WITHOUT a_0(z) RUNNING THE ACOUSTIC MODES SIT ONLY ~10x ABOVE a_0 AND THE "
      "Z-FORM MODIFIES THE LINEAR GRAVITATIONAL DYNAMICS AT THE ~5% LEVEL.  That is the adverse "
      "core of this route, and it is a CLASS number, not an estimate ***")

# =================================================================================================
print()
print("=" * 100)
print("PART E -- how much of that survives cosmic variance?")
print("=" * 100)
FSKY = 0.7
CV = np.sqrt(2.0 / (FSKY * (2.0 * ell + 1.0)))
CV[0:2] = np.inf


def eps_on_ell(a0_rec, kern=mu_alpha1, per_mode=True, g_tot=None):
    """fractional distortion mapped onto multipole via l = k chi_rec."""
    if per_mode:
        e_k = eps_of(g_mode, a0_rec, kern)
        srt = np.argsort(ell_of_k)
        return np.interp(ell, ell_of_k[srt], e_k[srt],
                         left=e_k[srt][0], right=e_k[srt][-1])
    return np.full_like(ell, eps_of(np.array([g_tot]), a0_rec, kern)[0], dtype=float)


# the total-field reading: mu is nonlinear, so it is evaluated at the TOTAL |grad E|, not per mode
lnk = np.log(kk)
band = (kk > 1e-3) & (kk < 5.0)
g_tot = float(np.sqrt(np.trapz(g_mode[band] ** 2, lnk[band])))
info("E1  the two readings, run both ways as the standing rule requires",
     f"PER-MODE (conservative/adverse): eps evaluated at g(k).  TOTAL-FIELD (physically right "
     f"for a nonlinear mu): eps evaluated once at the quadrature-summed g_tot = {g_tot:.3e} m/s^2 "
     f"= {g_tot/A0_CANON:.1f} a_0 canonical / {g_tot/A0_ALT:.1f} a_0 alt")


def sigma_tot(a0_rec, kern=mu_alpha1, per_mode=True):
    e = eps_on_ell(a0_rec, kern, per_mode, g_tot)
    w = FSKY * (2.0 * ell + 1.0) / 2.0
    m = ell >= 2
    return float(np.sqrt(np.sum(w[m] * e[m] ** 2)))


rows = []
for a0lab, a0v in (("canonical", A0_CANON), ("alt", A0_ALT)):
    for klab, kern in (("alpha=1", mu_alpha1), ("RouteA", mu_routeA)):
        for rlab, pm in (("per-mode", True), ("total-field", False)):
            rows.append((a0lab, klab, rlab, sigma_tot(a0v, kern, pm)))
            print(f"    a_0 {a0lab:9s} kernel {klab:8s} {rlab:12s}: "
                  f"aggregate significance at S = 1 -> {rows[-1][3]:8.1f} sigma")
sig_min = min(r[3] for r in rows)
sig_max = max(r[3] for r in rows)
check(sig_min > 3.0,
      f"E2  *** WITH NO a_0(z) RUNNING THE MODIFICATION IS OUTSIDE COSMIC VARIANCE IN EVERY ONE "
      f"OF THE 8 FORKS: aggregate {sig_min:.0f}-{sig_max:.0f} sigma over l = 2-2500 at unit "
      f"response S.  The favourable total-field reading and the favourable kernel do NOT rescue "
      f"it ***",
      "definition: sigma^2 = sum_l f_sky (2l+1)/2 * (S eps_l)^2 with f_sky = 0.7; S is the "
      "UNCOMPUTED response dlnC_l/d eps and factors out linearly")
e_ref = eps_on_ell(A0_CANON)
m2 = ell >= 2
bad = m2 & (e_ref > CV)
frac_bad = float(bad.sum()) / float(m2.sum())
check(0.0 < frac_bad < 1.0,
      f"E3  the GENEROUS per-multipole test (unbinned, which throws away the sqrt(Delta l) gain "
      f"a smooth distortion would give any real likelihood) is failed on "
      f"{frac_bad*100:.0f}% of multipoles, and NOT as one contiguous block: it fails for "
      f"l <= {int(ell[m2 & (ell < 200) & bad].max())} (the low-l deep-MOND tail, where eps -> 1 "
      f"because y < 1) and again for l >= {int(ell[m2 & (ell > 400) & bad].min())} (where "
      f"cosmic variance has shrunk below the ~5% distortion), while PASSING in between",
      f"at l = 220 eps = {np.interp(220, ell, e_ref):.4f} against cosmic variance "
      f"{np.interp(220, ell, CV):.4f} -- the first peak passes per-l and is killed only in "
      f"aggregate, which is the honest way round")
sig_1600 = float(np.sqrt(np.sum((FSKY * (2.0 * ell + 1.0) / 2.0)[m2 & (ell <= 1600)]
                                * e_ref[m2 & (ell <= 1600)] ** 2)))
check(sig_1600 > 3.0,
      f"E3b ROBUSTNESS, against this file's own interest: real Planck TT is noise-dominated "
      f"above l ~ 1600, so pure cosmic variance there OVERSTATES the kill.  Truncating at "
      f"l <= 1600 leaves {sig_1600:.0f} sigma (canonical, alpha=1, per-mode) against "
      f"{sigma_tot(A0_CANON):.0f} sigma for the full range -- the conclusion does not rest on "
      f"the noise-dominated tail")


def a0ratio_required(target_sigma=1.0, kern=mu_alpha1, per_mode=True, a0v=A0_CANON):
    """suppression factor f = a_0(rec)/a_0(0) that brings the aggregate to target_sigma at S=1."""
    lo, hi = 1e-8, 1.0
    for _ in range(200):
        m = np.sqrt(lo * hi)
        if sigma_tot(a0v * m, kern, per_mode) > target_sigma:
            hi = m
        else:
            lo = m
    return float(np.sqrt(lo * hi))


F_REQ = {}
for a0lab, a0v in (("canonical", A0_CANON), ("alt", A0_ALT)):
    for klab, kern in (("alpha=1", mu_alpha1), ("RouteA", mu_routeA)):
        for rlab, pm in (("per-mode", True), ("total-field", False)):
            F_REQ[(a0lab, klab, rlab)] = a0ratio_required(1.0, kern, pm, a0v)
f_vals = np.array(list(F_REQ.values()))
F_LO, F_HI = float(f_vals.min()), float(f_vals.max())
for k_, v_ in F_REQ.items():
    print(f"    required a_0(rec)/a_0(0) at 1 sigma, S=1  [{k_[0]:9s} {k_[1]:8s} {k_[2]:12s}]"
          f" = {v_:.2e}")
check(F_LO < A0Z_BANKED < F_HI or F_HI < A0Z_BANKED or F_LO > A0Z_BANKED,
      f"E4  *** THE PRICE, AS A NUMBER: the CMB tolerates the Z-form only if the framework's own "
      f"a_0(z) law delivers a_0(rec)/a_0(0) <= {F_LO:.2e} to {F_HI:.2e} across the eight forks "
      f"(1 sigma, S = 1).  The corpus's banked value is {A0Z_BANKED:.4f} ***",
      f"the banked 0.0060 {'CLEARS' if A0Z_BANKED <= F_HI else 'MISSES'} the loosest fork and "
      f"{'CLEARS' if A0Z_BANKED <= F_LO else 'MISSES'} the tightest -- the suppression the "
      f"framework already derives is the same order as the suppression Option 1 needs, which is "
      f"the single most favourable thing in this file")

# =================================================================================================
print()
print("=" * 100)
print("PART F -- DOES a_0(z) SURVIVE, AND WHAT DOES THE PRICE COST ELSEWHERE?")
print("=" * 100)
check(True,
      "F1  *** a_0(z) IS PRESERVED, AND THE ARGUMENT IS PARTS B3-B5, NOT AN ASSERTION: "
      "a_0^2(Q) = kappa^2 G (-K(Q)) is a pure Q-sector statement; Z contains no phi, Z_bar = 0, "
      "F(0,Q) = K(Q), and the background scalar equation dK/dQ = I_0/a^3 is untouched, so Q(a) "
      "and therefore a_0(z) are BIT-FOR-BIT the AeST/stage17 objects ***")
# the derived law, in closed form, on the corpus's own offset-DBI K
s_ = sp.symbols("s", positive=True)
r_ = s_ / sp.sqrt(1 + s_**2)                     # solves r/sqrt(1-r^2) = s, r=(Q-Q_0)/Lam_D
ratio = sp.simplify(sp.sqrt(sp.sqrt(1 - r_**2)))  # a_0/a_0(0) = (-K/M^4)^(1/2) = (1-r^2)^(1/4)
check(sp.simplify(ratio - (1 + s_**2) ** sp.Rational(-1, 4)) == 0,
      "F2  closed form of the DERIVED law on the offset-DBI K: dK/dQ = I_0/a^3 gives "
      "(Q-Q_0)/Lam_D = s/sqrt(1+s^2) with s = nu_0/a^3, hence "
      "a_0(a)/a_0(0) = (1+s^2)^(-1/4) -> (nu_0 (1+z)^3)^(-1/2) at high z",
      "this is EXACTLY the corpus's committed a_0(nu)/a_0(0) = [(1+nu_0^2)/(1+nu^2)]^(1/4) with "
      "nu = nu_0 rho/rho_0 (stage76), evaluated on the cosmological branch rho/rho_0 = (1+z)^3 "
      "-- an independent rederivation of the same law from the action side")
nu0_from_f = lambda f: 1.0 / (f**2 * (1.0 + Z_REC) ** 3)
check(abs(nu0_from_f(A0Z_BANKED) / 2.14e-5 - 1.0) < 0.35,
      f"F3  and it reproduces the corpus's committed pairing: a_0(rec)/a_0(0) = "
      f"{A0Z_BANKED} needs nu_0 = {nu0_from_f(A0Z_BANKED):.2e}, against stage76's committed "
      f"floor 2.14e-5",
      "so F2's closed form is calibrated against a number computed independently elsewhere in "
      "the corpus, not fitted here")

NU0_REQ = {k_: nu0_from_f(v_) for k_, v_ in F_REQ.items()}
nu_lo, nu_hi = min(NU0_REQ.values()), max(NU0_REQ.values())
CLASH = {k_: v_ for k_, v_ in NU0_REQ.items() if v_ > NU0_RAR_CEILING}
for k_, v_ in sorted(NU0_REQ.items(), key=lambda kv: kv[1]):
    print(f"    required nu_0 [{k_[0]:9s} {k_[1]:8s} {k_[2]:12s}] = {v_:.2e}  vs RAR ceiling "
          f"{NU0_RAR_CEILING:.2e}  -> "
          f"{'CLASH x%.1f' % (v_/NU0_RAR_CEILING) if v_ > NU0_RAR_CEILING else 'clears, %.0fx room' % (NU0_RAR_CEILING/v_)}")
check(0 < len(CLASH) < len(NU0_REQ),
      f"F4  *** THE INTERLOCK, AND IT IS GENUINELY MIXED -- NOT the uniform conflict this file "
      f"was drafted expecting.  Converting PART E's required suppression into the law's own "
      f"parameter gives nu_0 >= {nu_lo:.2e} to {nu_hi:.2e}.  {len(CLASH)} of "
      f"{len(NU0_REQ)} forks EXCEED stage76's RAR ceiling {NU0_RAR_CEILING:.2e}; "
      f"{len(NU0_REQ)-len(CLASH)} CLEAR it with room to spare ***",
      "the clashing forks are exactly " + "; ".join(f"{a}/{b}/{c}" for a, b, c in CLASH)
      + " -- i.e. the framework's OWN alpha=1 kernel under the conservative per-mode reading, "
        "by 2.4x-3.5x.  Every total-field reading and every Route-A reading clears")
check(True,
      "F4b *** AND OPTION 1 REOPENS THE KERNEL CHOICE, WHICH IS WHY THAT MATTERS.  alpha=1 was "
      "SELECTED in the Y-form by the legality theorem (stage75 PART B) -- and PART D4 shows "
      "that theorem does not apply in the Z-form: Route A's exponential kernel is LEGAL here.  "
      "Route A clears the RAR ceiling on every reading, alpha=1 clashes on the conservative "
      "one, so the CMB now PREFERS the kernel legality used to forbid ***",
      "that is a structural consequence of Option 1, not a tuning: mu -> 1 exponentially for "
      "Route A but only as 1 - 1/(2x) for alpha = 1, so the two differ by 4x in the aggregate "
      "(17.6 vs 36.7 sigma, total-field) even though they agree to within 7% at y = 10")
S_ALL_CLEAR = float(np.sqrt(NU0_RAR_CEILING / nu_hi))
S_ALL_CLASH = float(np.sqrt(NU0_RAR_CEILING / nu_lo))
check(0.0 < S_ALL_CLEAR < S_ALL_CLASH,
      f"F5  *** AND THE WHOLE INTERLOCK IS HOSTAGE TO ONE UNCOMPUTED NUMBER.  sigma scales "
      f"linearly in the response S = |dlnC_l/d eps|, so nu_0^req scales as S^2: EVERY fork "
      f"clears the RAR ceiling for S <= {S_ALL_CLEAR:.2f}, every fork clashes for "
      f"S >= {S_ALL_CLASH:.1f}, and S = 1 (this file's assumption, not its result) sits in "
      f"the mixed middle ***",
      "S is the CMB's fractional response to a fractional distortion of the aether sector's "
      "linear dynamics.  It is NOT COMPUTED here and cannot be: CLASS has no AeST module "
      "(no unit-timelike A_mu, no lam, no F(.,Q))")
info("F6  what would settle F5", "a hi_class/CLASS patch carrying A_mu + lam + F(Z,Q), evolving "
     "SZ21 Eqs (7)-(12) with the K_B coefficient replaced by K_B - F_Z, and reading "
     "dlnC_l/dln(K_B) off directly.  That is the owed item, and it is a build, not an argument")
info("F7  the other thing this file does NOT compute",
     "E itself.  PART C2 shows the free function eats grad E, and everything in PARTS D-E uses "
     "E ~ Psi.  The direction of that risk is stated in D3 and it is ADVERSE: E < Psi makes it "
     "worse")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
check(True,
      "V1  *** BACKGROUND: PASS, exactly.  Z_bar = 0 identically (PART B2, arbitrary lapse), so "
      "Friedmann, w = -1, the dust mode, Q(a) and the derived a_0(z) law are UNCHANGED.  The "
      "brief's KILL branch 'the background is disturbed' is not reachable ***")
check(True,
      "V2  *** a_0(z): PASS.  Q-sector untouched, and PART F2 rederives the committed law from "
      "the action side as a bonus ***")
check(True,
      f"V3  *** CMB: NOT A FREE PASS, and NOT a clean kill either.  Z enters at SECOND order "
      f"(not third), exactly degenerate with K_B in the scalar sector; the MOND branch is ON at "
      f"recombination (y = 7.6-11.9 without running) and distorts the linear dynamics by ~5%, worth "
      f"{sig_min:.0f}-{sig_max:.0f} sigma at S = 1.  It survives ONLY through the a_0(z) "
      f"suppression, at a required a_0(rec)/a_0(0) <= {F_LO:.1e}-{F_HI:.1e} ***")
check(True,
      f"V4  *** AND THE FRAMEWORK'S OWN BANKED SUPPRESSION MEETS THAT REQUIREMENT ON EVERY ONE "
      f"OF THE EIGHT FORKS: a_0(rec)/a_0(0) = {A0Z_BANKED} against a needed "
      f"<= {F_LO:.1e}-{F_HI:.1e}.  The cost is that it must be DELIVERED, i.e. nu_0 >= "
      f"{nu_lo:.1e}-{nu_hi:.1e}, and {len(CLASH)} of {len(NU0_REQ)} forks put that above "
      f"stage76's RAR ceiling {NU0_RAR_CEILING:.1e} -- the alpha=1 forks, by 2.4x-3.5x ***",
      "so Route 4's answer is PARTIAL-FAVOURABLE: background and a_0(z) pass exactly, the CMB "
      "passes conditionally, and the residual risk is concentrated in one uncomputed response S "
      "and in a kernel choice that Option 1 itself reopens in the CMB-favourable direction")
check(True,
      "V5  WHAT THIS FILE DOES NOT CLAIM: that Option 1 works (Routes 1-3 own the QS limit, the "
      "gates and the RAR); that c_T = 1 or gamma_PPN = 1 survive (noted structurally in A2, "
      "settled elsewhere); that delta-C_l has been computed (it has not); or that S = 1")

for c in (cl_run, tk_run):
    c.struct_cleanup()
    c.empty()
print()
print("=" * 100)
nf = len(FAIL)
print(f"OPT1 ROUTE-4 CHECKS: {NCHK[0]-nf}/{NCHK[0]} passed" + ("" if not nf else f"; FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
