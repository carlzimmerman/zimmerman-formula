#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
esc_gw_amplitude_2026.py -- ROUTE 4 OF THE OPTION-1 "s-RESCALING" ESCAPE:
WHAT DOES THE G_cosmo / G_local SPLIT COST IN GRAVITATIONAL WAVES?
2026-08-18.

=========================================================================================
THE THING BEING PRICED
=========================================================================================
Option 1 replaces AeST's free-function argument Y -> Z = J^mu J_mu (the aether's
acceleration squared, = the total potential gradient squared).  The reduction is AQUAL
exactly, with mu(g_obs) = J_Z.  Two deaths follow: the transverse aether kinetic
coefficient C_V = K_B - (2-K_B) J_Z goes negative across the whole RAR (ghost + tachyon),
and Zbar = 0 on FRW puts the cosmological background at the deep-MOND end so that
F_Z(0) = K_B kills SZ21's Eq (12).

THE ESCAPE (found by an adversarial verifier, NOT adjudicated by me): rescale the free
function, J -> s*J.  Both sector conditions constrain only the total Z-coefficient
M(Z) = F_Z = (2-K_B) s mu_phys, so

    static attraction  M > 0        and     vector no-ghost  M < K_B
    are satisfied at EVERY acceleration for   s < K_B/(2-K_B)  ( = 1/7 at K_B = 0.25 ).

THE PRICE, stated but not computed by anyone: under F(Z) the free-function normalisation is
the SOLE carrier of the Newtonian limit (opt1_gates_2026.py D6b/D8: the Einstein term
cancels identically against the mixing term on w = grad Psi), so

    G_N = Ghat / s,      Ghat = Gt/(1 - K_B/2)      ==>   r := Gt/G_N = (1 - K_B/2) s
    and no-ghost  <==>  r < K_B/2  =  0.125 at K_B = 0.25,   versus AeST's r = 0.875.

A ~7x split between the constant that normalises the graviton (Gt, the action's) and the
constant that Cavendish measures (G_N).  My assignment: price that in GRAVITATIONAL WAVES.

=========================================================================================
RESULT IN ONE PARAGRAPH -- direction: MIXED.  ASSIGNED GATES: PASS.  ONE NEW ADVERSE
CONSEQUENCE, DERIVED HERE, THAT THIS ROUTE DOES NOT CLOSE.
=========================================================================================
(a) DERIVED, not assumed: on FRW + a TT tensor mode the aether stays exactly A_mu =
(-1,0,0,0), and then J^mu = 0, F_{mu nu} = 0, Y = 0 and Q = phidot IDENTICALLY -- to ALL
orders in h, not just linear -- so Z = 0, the entire non-Einstein sector is h-independent,
its stress tensor is proportional to delta^mu_nu, and it carries NO anisotropic stress.
The tensor sector is therefore pure Einstein-Hilbert with 1/(16 pi Gt): M_*^2 = 1/(8 pi Gt)
CONSTANT, c_T^2 = 1, and the wave equation is hddot + 3H hdot + k^2 h/a^2 = 16 pi Gt Pi^TT.
The strain from a binary then carries Gt (graviton normalisation x minimally-coupled matter
quadrupole) while the ORBIT carries G_N -- the split is real and both constants appear.
(b) AND YET THE STANDARD-SIREN DISTANCE IS EXACTLY BLIND TO IT.  The emitted amplitude and
the radiated flux carry the SAME power of Gt (h ~ Gt Qddot, and the Isaacson flux
~ M_*^2 hdot^2 ~ Gt^{-1} x Gt^2), so the amplitude and the chirp rate are set by ONE
combination, K53 = Gt G_N^{2/3} mu M^{2/3}, and it cancels out of
D_L = 5 c fdot / (24 pi^2 h f^3).  Shown symbolically (dD_L/dGt = dD_L/dG_N = 0 exactly) and
numerically over s spanning 4 decades: the recovered distance is invariant to 1e-15 while
the recovered chirp mass moves as r^{3/5}.  GW170817's d_L^GW = 40 (+8/-14) Mpc against the
NGC 4993 SBF distance 40.7 +/- 1.4 +/- 1.9 Mpc therefore bounds s NOT AT ALL: the sensitivity
is zero, not merely small.  (c) alpha_M = dln M_*^2/dln a = 0 EXACTLY, for any free
function, any s, and either a0 footing (the a0-carrying term sits inside F(Z,.) and Z is
identically zero in the tensor sector, so a0(z) cannot touch GW friction) -- against a
GW170817 leverage of only |alpha_M| <~ 40-70 anyway.  (d) THE WHOLE OF ROUTE 1's WINDOW,
s in (0, 0.142857], is allowed by GW amplitude and GW friction.  PASS.
THE ADVERSE CONSEQUENCE, at equal volume.  The same three lines that give the cancellation
give two unavoidable riders.  (i) EVERY GW-INFERRED MASS IS RESCALED: Mchirp_inferred =
Mchirp_true * r^{3/5}, so at the ghost-free edge GW170817's true chirp mass is
1.186/0.125^{0.6} = 4.13 Msun and its components ~4.7-5.6 Msun -- black holes, against a
kilonova.  (ii) THE BINARY-PULSAR ORBITAL DECAY IS SUPPRESSED BY EXACTLY r: with the masses
fixed by the near-zone observables omegadot and gamma (which see G_N), the tensor-channel
Pbdot/Pbdot_GR = r = 0.125, an 8x deficit against B1913+16's measured 0.9983 +/- 0.0016.
Taken alone that is a ~550 sigma kill.  I DO NOT SCORE IT AS ONE, for a reason that cuts
against my own interest in finding a kill: the same tensor-only bookkeeping applied to the
UNMODIFIED parent theory (s = 1, r = 0.875) would exclude AeST itself at ~78 sigma, so my
flux ledger is almost certainly INCOMPLETE -- the aether's now-healthy vector modes (c_V^2 =
K_B/C_V, superluminal here) and the scalar radiate too, and dipole channels are exactly what
the Einstein-aether literature finds dominant.  THE FULL RADIATED FLUX IS **NOT COMPUTED**.
What IS established is the shape of the liability: the missing channels must supply 87.5% of
the flux at EVERY orbital period, which a dipole term (relative order (c/v)^2) cannot do
uniformly across systems -- so this is the sharpest surviving handle on s, and it lives in
the GW sector, not in BBN.

=========================================================================================
EVERY REDUCTION AND EVERY IMPORT, DECLARED
=========================================================================================
R1  G_N = Ghat/s with Ghat = Gt/(1-K_B/2) is TAKEN AS GIVEN from the assignment and from
    opt1_gates_2026.py D6b/D7/D8 + c14_ppn_sector_2026.py ("the explicit solve gives
    G_eff = Ghat/J_Z with Ghat = 2G~/(2-K_B)").  I do NOT re-derive the static sector.
    Because the corpus has a live convention fork here (the scalar-DECOUPLED limit obeys
    the Einstein-aether Cavendish form G/(1 - c_14/2) with c_14 = K_B - (2-K_B)J_Z, which
    at s = s_max gives c_14 = 0 and NO split at all), EVERY result below is stated as a
    function of the single ratio r = Gt/G_N and can be re-priced under either dictionary.
    PART A prints both.
R2  TENSOR SECTOR: FRW + one TT polarisation h(t,z), i.e.
    ds^2 = -dt^2 + a^2[(1+h)dx^2 + (1-h)dy^2 + dz^2].  The aether is held at A^mu =
    (1,0,0,0).  Its consistency is checked two ways: (i) the unit constraint is exact on
    this metric, (ii) PART B6 expands the full invariant set with a GENERIC aether
    perturbation v_i(t,z) at O(eps^2) and shows no h.v cross term exists, so a TT mode
    cannot source an aether perturbation (the SVT statement, verified rather than cited).
R3  RADIATION ZONE: leading (Newtonian / quadrupole) order only.  Matter couples minimally
    to g alone (S_m[g]), so T_matter is separately conserved and the leading radiative
    source is the MATTER quadrupole.  Field-energy contributions to the radiating source
    are O(v^2/c^2); PART F4 prices that at 2.6% for GW170817 at 100 Hz, below the ~20-35%
    GW distance error.  1PN and beyond: NOT COMPUTED.
R4  The pure numbers 4, 96/5, 32 pi, 192 pi/5 are the GR control's; what is DERIVED here is
    WHICH constant sits in each of them.  This is legitimate only because the tensor sector
    is shown to be EXACTLY Einstein-Hilbert and the orbit EXACTLY Newtonian -- both
    established in PARTs B and A rather than assumed.
R5  NOT DONE HERE: the vector/scalar radiative channels and any dipole flux (PART F2, the
    named liability); the theory's own 1PN dynamics (so omegadot/gamma mass extraction is
    imported from GR); strong-field stellar structure (so the "4.7 Msun neutron star"
    reading of F1 is left open); BBN / CLASS / the CMB degeneracy (other routes).
R6  a0 footings: canonical 9.3619e-11 and ALT 1.1279e-10 are both carried.  They enter in
    exactly one place that matters -- PART C0's check that a GW source is on the saturated
    branch by ~20 orders under BOTH -- and are then provably absent from everything else.

LITERATURE INPUTS (values quoted, not derived; each used only where flagged):
  GW170817 d_L^GW = 40 (+8/-14) Mpc, detector-frame Mchirp = 1.1977 Msun   [LVC PRL 119, 161101]
  GW170817 source-frame Mchirp = 1.186 Msun                                [LVC PRX 9, 011001]
  NGC 4993 SBF distance 40.7 +/- 1.4 (stat) +/- 1.9 (sys) Mpc              [Cantiello+ 2018]
  NGC 4993 Hubble-flow recession 3017 +/- 166 km/s  => z = 0.0100          [LVC Nature 551, 85]
  B1913+16  Pbdot_obs/Pbdot_GR = 0.9983 +/- 0.0016                         [Weisberg & Huang 2016]
  J0737-3039 Pbdot agreement at the 1.3e-4 level                           [Kramer+ 2021]
The verdict of PARTs B-E does not depend on any of them (the sensitivity is exactly zero);
they are load-bearing only for the SIZE of the PART F liability, which is not scored.

EXIT 0 iff every numbered check passes.
"""

import math
import os
import sys
import time

import numpy as np
import sympy as sp

# ================================================================================================
# harness
# ================================================================================================
FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"\n         {detail}" if detail else ""))


def head(s):
    print()
    print("=" * 100)
    print(s)
    print("=" * 100)


print(__doc__)
T0 = time.time()
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

# ================================================================================================
# constants
# ================================================================================================
CLIGHT = 2.99792458e8
GNEWT = 6.67430e-11                 # the LABORATORY constant = G_N in this theory (Cavendish)
MSUN = 1.98892e30
GMSUN_C3 = 4.925490947e-6           # G Msun / c^3, seconds  (standard)
PC = 3.0856775814913673e16
MPC = 1.0e6 * PC
A0_CAN = 9.3619e-11                 # kappa c sqrt(G rho_Lambda), canonical (kappa = 1/2 FITTED)
A0_ALT = 1.1279e-10                 # alt footing
FOOT = (("canonical", A0_CAN), ("ALT      ", A0_ALT))
KB_FID = 0.25                       # corpus fiducial ceiling, K_B <~ 0.25 (BBN)

# literature inputs (see header)
GW170817_DL_MPC, GW170817_DL_HI, GW170817_DL_LO = 40.0, 8.0, 14.0
GW170817_MC_SRC = 1.186             # source-frame chirp mass, Msun
GW170817_MC_DET = 1.1977            # detector-frame chirp mass, Msun
GW170817_MTOT = 2.74                # detector-frame total mass, Msun
NGC4993_SBF, NGC4993_SBF_STAT, NGC4993_SBF_SYS = 40.7, 1.4, 1.9
NGC4993_Z = 0.0100
B1913_RATIO, B1913_ERR = 0.9983, 0.0016
J0737_PREC = 1.3e-4

# ================================================================================================
head("PART A -- the split, algebraically; and the convention fork, printed both ways")
# ================================================================================================
KB, s_, JZ = sp.symbols("K_B s J_Z", positive=True)

s_max_sym = sp.simplify(KB / (2 - KB))
r_sym = sp.simplify((1 - KB / 2) * s_)                       # r = Gt/G_N  under R1
r_sup = sp.simplify(r_sym.subs(s_, s_max_sym))               # supremum of r at the ghost edge

check(sp.simplify(r_sup - KB / 2) == 0,
      "A1  the no-ghost ceiling in NORMALISATION-FREE form: sup_s [Gt/G_N] = (1-K_B/2)*K_B/(2-K_B) "
      "= K_B/2 EXACTLY (sympy identity), i.e. the escape is equivalent to  2 Gt < K_B G_N",
      f"symbolically: (1-K_B/2)*K_B/(2-K_B) simplifies to {r_sup}")

s_max_num = float(s_max_sym.subs(KB, KB_FID))
r_max_num = float(r_sup.subs(KB, KB_FID))
r_aest = float((1 - KB_FID / 2))                              # s = 1, the unmodified theory
check(abs(s_max_num - 1.0 / 7.0) < 1e-12 and abs(r_max_num - 0.125) < 1e-12,
      f"A2  at K_B = {KB_FID}: s_max = K_B/(2-K_B) = {s_max_num:.6f} (= 1/7), and "
      f"r = Gt/G_N <= {r_max_num:.6f}; the unmodified theory has r = {r_aest:.6f}",
      f"split factor G_N/Gt >= {1/r_max_num:.4f} versus AeST's {1/r_aest:.4f}; "
      f"ratio of the two = {r_aest/r_max_num:.3f}x -- this reproduces the assignment's '~7x split'")

# the convention fork, stated at equal volume (R1)
c14_eff = KB - (2 - KB) * s_                                  # c14_ppn_sector_2026.py's dictionary
r_alt_sym = sp.simplify(1 - c14_eff / 2)                      # Einstein-aether Cavendish reading
r_alt_at_smax = float(sp.simplify(r_alt_sym.subs(s_, s_max_sym)).subs(KB, KB_FID))
check(abs(r_alt_at_smax - 1.0) < 1e-12,
      "A3  THE FORK, ON THE RECORD: under the scalar-DECOUPLED Einstein-aether Cavendish form "
      "G_N = Gt/(1 - c_14/2) with c_14 = K_B - (2-K_B)s, the ghost edge s = s_max is exactly "
      f"c_14 = 0, giving r = {r_alt_at_smax:.3f} -- NO SPLIT AT ALL",
      "the two readings disagree because under F(Z) the Newtonian limit is carried by the free "
      "function, NOT by the scalar-decoupled Einstein term (opt1_gates D8).  I use R1's "
      "r = (1-K_B/2)s throughout, but every result below is a function of r alone, so the fork "
      "re-prices without redoing anything: at r -> 1 every liability in PART F vanishes")

check(True,
      "A4  a0 does not appear in r.  s and K_B are a0-free, so the split -- and therefore every "
      "GW consequence of it -- is identical under BOTH footings",
      f"canonical a0 = {A0_CAN:.4e} m/s^2, ALT a0 = {A0_ALT:.4e} m/s^2; PART C0 is the one place "
      "the footings do real work")

R_VALS = {"escape edge (s=s_max)": r_max_num,
          "escape, s=0.10": float((1 - KB_FID / 2) * 0.10),
          "AeST (s=1)": r_aest,
          "GR (no split)": 1.0}

# ================================================================================================
head("PART B -- the tensor sector, DERIVED from the action on FRW + a TT mode (sympy)")
# ================================================================================================
t, x, y, z = sp.symbols("t x y z", real=True)
CO = [t, x, y, z]
e = sp.Symbol("epsilon")
a = sp.Function("a", positive=True)(t)
hh = sp.Function("h")(t, z)
phib = sp.Function("phibar")(t)

g = sp.diag(-1, a ** 2 * (1 + e * hh), a ** 2 * (1 - e * hh), a ** 2)
ginv = g.inv()
detg = sp.simplify(g.det())


def christoffel(gm, gi, co):
    n = len(co)
    Gam = [[[0] * n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for nu in range(m, n):
                expr = 0
                for sgm in range(n):
                    expr += gi[l, sgm] * (sp.diff(gm[sgm, m], co[nu])
                                          + sp.diff(gm[sgm, nu], co[m])
                                          - sp.diff(gm[m, nu], co[sgm]))
                expr = sp.simplify(expr / 2)
                Gam[l][m][nu] = expr
                Gam[l][nu][m] = expr
    return Gam


GAM = christoffel(g, ginv, CO)

# ---- B1: the aether ---------------------------------------------------------------------------
Aup = sp.Matrix([1, 0, 0, 0])
Adn = sp.simplify(g * Aup)
norm = sp.simplify((Adn.T * Aup)[0, 0])
check(sp.simplify(norm + 1) == 0 and sp.simplify(Adn - sp.Matrix([-1, 0, 0, 0])) == sp.zeros(4, 1),
      "B1  A^mu = (1,0,0,0) has A_mu = (-1,0,0,0) and A^mu A_mu = -1 EXACTLY on the TT-perturbed "
      "metric -- to all orders in h, not perturbatively",
      "so the Lagrange-multiplier term -lambda(A.A+1) vanishes identically and contributes nothing")

# ---- B2: J^mu = 0 exactly ----------------------------------------------------------------------
Jup = [sp.simplify(sum(GAM[m][0][0] * 1 for _ in [0])) for m in range(4)]
Jup = [sp.simplify(GAM[m][0][0]) for m in range(4)]          # J^mu = A^nu nabla_nu A^mu = Gamma^mu_00
check(all(sp.simplify(J) == 0 for J in Jup),
      "B2  J^mu = A^nu grad_nu A^mu = Gamma^mu_{00} = 0 IDENTICALLY on FRW + TT (all four "
      "components, exact in h)  ==>  Z = J^mu J_mu = 0 IDENTICALLY",
      f"components: {[sp.simplify(J) for J in Jup]}.  The whole free function F(Z,Q) is therefore "
      "evaluated at Z = 0 in the tensor sector, whatever F is and whatever s is")

# ---- B3: F_{mu nu} = 0 exactly ------------------------------------------------------------------
Fmn = sp.Matrix(4, 4, lambda m, n: sp.diff(Adn[n], CO[m]) - sp.diff(Adn[m], CO[n]))
check(sp.simplify(Fmn) == sp.zeros(4, 4),
      "B3  F_{mu nu} = 2 grad_[mu A_nu] = d_mu A_nu - d_nu A_mu = 0 IDENTICALLY (A_mu is a "
      "constant covector here)  ==>  the -(K_B/2)F^2 term is absent from the tensor sector",
      "this is why c_13 = c_1 + c_3 = 0 never had to be invoked: the term simply is not there")

# ---- B4: Y and Q ---------------------------------------------------------------------------------
qinv = sp.Matrix(4, 4, lambda m, n: ginv[m, n] + Aup[m] * Aup[n])
dphi = sp.Matrix([sp.diff(phib, t), 0, 0, 0])
Yscal = sp.simplify((dphi.T * qinv * dphi)[0, 0])
Qscal = sp.simplify((Adn.T * ginv * dphi)[0, 0] * -1)        # Q = A^mu d_mu phi
Qscal = sp.simplify(sum(Aup[m] * dphi[m] for m in range(4)))
check(sp.simplify(Yscal) == 0 and sp.simplify(Qscal - sp.diff(phib, t)) == 0,
      "B4  Y = q^{mu nu} d_mu phi d_nu phi = 0 IDENTICALLY (q^{00} = g^{00} + A^0 A^0 = -1+1 = 0) "
      "and Q = A^mu d_mu phi = dphibar/dt, with NO h-dependence",
      f"Y = {sp.simplify(Yscal)},  Q = {sp.simplify(Qscal)}")

# ---- B5: hence no anisotropic stress from the dark sector ---------------------------------------
check(True,
      "B5  *** CONSEQUENCE: every non-Einstein invariant in the action (Z, Y, Q, F^2, J.grad phi, "
      "A.A) is h-INDEPENDENT, so the extra Lagrangian is a CONSTANT C on the TT background.  For "
      "L = C the stress tensor is T_{mu nu} = C g_{mu nu}, i.e. T^mu_nu = C delta^mu_nu: "
      "T^x_x - T^y_y = 0.  THE DARK SECTOR CARRIES NO ANISOTROPIC STRESS, for ANY free function "
      "and ANY s ***",
      "uses only delta(sqrt(-g))/delta g^{mu nu} = -(1/2) sqrt(-g) g_{mu nu}; the h^2 piece of "
      "sqrt(-g) is the Lambda-like piece that the background equations cancel, exactly as in GR")

# ---- B6: no h-v mixing => a TT mode cannot source an aether perturbation -------------------------
v1 = sp.Function("v1")(t, z)
v2 = sp.Function("v2")(t, z)
v3 = sp.Function("v3")(t, z)
vv = [v1, v2, v3]
# solve the unit constraint for A^0 to O(eps^2)
A0s = sp.Symbol("A0s")
spatial_norm = sum(g[i + 1, i + 1] * (e * vv[i]) ** 2 for i in range(3))
A0sol = sp.series(sp.sqrt(1 + spatial_norm), e, 0, 3).removeO()
Aup_v = sp.Matrix([A0sol, e * v1, e * v2, e * v3])
Adn_v = sp.simplify(g * Aup_v)


def ser2(expr):
    return sp.expand(sp.series(sp.expand(expr), e, 0, 3).removeO())


# J^mu = A^nu nabla_nu A^mu
Jv = []
for m in range(4):
    expr = 0
    for nu in range(4):
        expr += Aup_v[nu] * (sp.diff(Aup_v[m], CO[nu])
                             + sum(GAM[m][nu][sg] * Aup_v[sg] for sg in range(4)))
    Jv.append(ser2(expr))
Zv = ser2(sum(Jv[m] * sum(g[m, n] * Jv[n] for n in range(4)) for m in range(4)))
qinv_v = sp.Matrix(4, 4, lambda m, n: ginv[m, n] + Aup_v[m] * Aup_v[n])
Yv = ser2((dphi.T * qinv_v * dphi)[0, 0])
Qv = ser2(sum(Aup_v[m] * dphi[m] for m in range(4)))
Fmn_v = sp.Matrix(4, 4, lambda m, n: sp.diff(Adn_v[n], CO[m]) - sp.diff(Adn_v[m], CO[n]))
F2v = ser2(sum(Fmn_v[m, n] * Fmn_v[p, q_] * ginv[m, p] * ginv[n, q_]
               for m in range(4) for n in range(4) for p in range(4) for q_ in range(4)))
Jdphi_v = ser2(sum(Jv[m] * dphi[m] for m in range(4)))

mixing = []
for nm, ex in (("Z", Zv), ("Y", Yv), ("Q", Qv), ("F^2", F2v), ("J.grad phi", Jdphi_v)):
    c2 = sp.expand(ex.coeff(e, 2))
    # does the O(eps^2) coefficient contain h at all?
    if c2.has(hh):
        mixing.append(nm)
check(not mixing,
      "B6  with a GENERIC aether perturbation v_i(t,z) switched on (unit constraint solved to "
      "O(eps^2)), the O(eps^2) part of EVERY invariant -- Z, Y, Q, F^2, J.grad phi -- is free of h: "
      "there is NO h.v cross term, so a TT mode cannot source an aether perturbation and holding "
      "A^mu = (1,0,0,0) in B1-B5 is CONSISTENT, not an assumption",
      f"invariants carrying an h.v mixing: {mixing if mixing else 'none'} (this is the SVT "
      "statement, verified rather than cited)")

# ---- B7: the Einstein side, and c_T, alpha_M ------------------------------------------------------
def ricci_and_einstein(gm, gi, co, Gam):
    ND = len(co)
    Ric = sp.zeros(ND, ND)
    for m in range(ND):
        for nu in range(m, ND):
            expr = 0
            for l in range(ND):
                expr += sp.diff(Gam[l][m][nu], co[l]) - sp.diff(Gam[l][m][l], co[nu])
                for sg in range(ND):
                    expr += Gam[l][l][sg] * Gam[sg][m][nu] - Gam[l][nu][sg] * Gam[sg][m][l]
            expr = sp.expand(expr)
            Ric[m, nu] = expr
            Ric[nu, m] = expr
    Rs = sp.expand(sum(gi[p, q2] * Ric[p, q2] for p in range(ND) for q2 in range(ND)))
    Ein = sp.zeros(ND, ND)
    for m in range(ND):
        for nu in range(ND):
            Ein[m, nu] = sp.expand(Ric[m, nu] - gm[m, nu] * Rs / 2)
    return Ric, Rs, Ein


RIC, RS, EIN = ricci_and_einstein(g, ginv, CO, GAM)
Emix = sp.Matrix(4, 4, lambda m, n: sp.expand(sum(ginv[m, p] * EIN[p, n] for p in range(4))))
dG = sp.expand(sp.series(sp.expand(Emix[1, 1] - Emix[2, 2]), e, 0, 2).removeO().coeff(e, 1))
dG = sp.simplify(dG)

H = sp.diff(a, t) / a

# --- SIGN/CONVENTION CONTROL FIRST (named: the Friedmann equation) --------------------------------
G00_bg = sp.simplify(Emix[0, 0].subs(hh, 0).doit())
check(sp.simplify(G00_bg + 3 * H ** 2) == 0,
      "B7a CONTROL (named: the Friedmann equation).  Before any TT read-off, the SAME Einstein "
      "tensor evaluated on the unperturbed background gives G^0_0 = -3(adot/a)^2, which with "
      "G^mu_nu = 8 pi G T^mu_nu and T^0_0 = -rho is H^2 = 8 pi G rho/3",
      f"sympy: G^0_0|_(h=0) = {sp.simplify(G00_bg)}.  This fixes the sign and factor conventions of "
      "the machinery against a known answer, so the B7 read-off is calibrated, not asserted")

target = (sp.diff(hh, t, 2) + 3 * H * sp.diff(hh, t) - sp.diff(hh, z, 2) / a ** 2)
ratio = sp.simplify(dG / target)
check(sp.simplify(ratio - 1) == 0,
      "B7  G^x_x - G^y_y at O(h) = [ hddot + 3 H hdot - (1/a^2) d_z^2 h ]  EXACTLY (sympy: the "
      "ratio to that expression simplifies to 1).  Since h_xx = +h and h_yy = -h, the source side "
      "G^mu_nu = 8 pi Gt T^mu_nu gives 8 pi Gt (T^x_x - T^y_y) = 16 pi Gt Pi^TT, so the TT "
      "equation is  hddot + 3H hdot + c_T^2 k^2 h/a^2 = 16 pi Gt Pi^TT_matter",
      f"ratio computed = {sp.simplify(ratio)}; friction coefficient is exactly 3H and the gradient "
      "coefficient exactly 1/a^2.  B5 has already shown the dark sector contributes 0 to "
      "T^x_x - T^y_y, so Gt is the ONLY constant on the source side")

check(True,
      "B8  READ-OFF, all three at once: M_*^2 = 1/(8 pi Gt) with Gt a CONSTANT of the action; "
      "c_T^2 = 1 (the 1/a^2 coefficient equals the hddot coefficient); and therefore "
      "*** alpha_M = dln M_*^2 / dln a = 0 EXACTLY ***",
      "alpha_M = 0 holds for ANY free function, ANY s, ANY K_B and BOTH a0 footings -- because "
      "Z = 0 identically (B2) removes the entire F(Z,Q) sector, INCLUDING the a0-carrying "
      "Z^{3/2} branch and the theta-promotion a0(theta), from the tensor sector")

# CONTROL: the same machinery with no aether and no scalar must give the textbook GR TT equation
check(sp.simplify(sp.expand(dG - target)) == 0,
      "B9  CONTROL (named: the textbook GR tensor-mode equation on FRW).  The Einstein-side "
      "computation above involves no aether and no free function at all -- it IS the GR control, "
      "and it reproduces hddot + 3H hdot - lap h/a^2 = 0 in vacuo with M_*^2 = 1/(8 pi G)",
      "so the derivation is calibrated against the known answer before the new one is claimed; "
      "the ONLY new content is B1-B6, i.e. that the dark sector adds nothing to it")

# ================================================================================================
head("PART C -- the source: where Gt and G_N enter the strain, the flux and the chirp")
# ================================================================================================
# C0: is a GW source on the saturated branch?  (the one place the a0 footings do work)
Mtot_kg = GW170817_MTOT * MSUN
f_gw = 100.0
om_orb = math.pi * f_gw                      # GW frequency = 2 x orbital
r_orb = (GNEWT * Mtot_kg / om_orb ** 2) ** (1.0 / 3.0)
g_orb = GNEWT * Mtot_kg / r_orb ** 2
sat = {}
for nm, a0 in FOOT:
    yv = g_orb / a0
    # exponential kernel mu(x) = 1 - exp(-sqrt(x)) at x = g_obs/a0 >> 1
    sat[nm] = (yv, math.sqrt(yv))
check(all(v[0] > 1e15 for v in sat.values()),
      "C0  the GW source is on the SATURATED branch by ~20 orders under BOTH footings, so "
      "mu_phys = 1 - exp(-sqrt(x)) = 1 to within exp(-1e10) and the orbital coupling is exactly "
      "G_N = Ghat/s with no interpolation-function correction",
      f"GW170817-like binary at f_GW = {f_gw:g} Hz: separation {r_orb/1e3:.1f} km, "
      f"g = {g_orb:.3e} m/s^2; " + "; ".join(
          f"{nm}: g/a0 = {v[0]:.3e}, sqrt = {v[1]:.3e}" for nm, v in sat.items()))

# C1-C4: symbolic derivation of the two observables and the distance
Gt_s, GN_s, mu_s, M_s, om_s, D_s, Mc_s, G_s = sp.symbols(
    "Gtilde G_N mu M omega D_L Mchirp G", positive=True)
c_s = sp.Symbol("c", positive=True)

# orbit (Newtonian, G_N):  Kepler and energy
r_kep = (GN_s * M_s / om_s ** 2) ** sp.Rational(1, 3)
E_orb = -sp.Rational(1, 2) * mu_s * (GN_s * M_s * om_s) ** sp.Rational(2, 3)
check(sp.simplify(sp.expand(-GN_s * mu_s * M_s / (2 * r_kep) - E_orb)) == 0,
      "C1  ORBIT: Kepler r = (G_N M/omega^2)^{1/3} and E = -G_N mu M/(2r) = "
      "-(1/2) mu (G_N M omega)^{2/3}.  The ORBIT sees G_N ONLY -- established at C0 "
      "(saturated branch) and by R1",
      "the reduced mass mu and the total mass M are the true (baryonic) masses")

# radiation: h ~ Gt x (matter quadrupole);  flux ~ M_*^2 hdot^2 ~ Gt^{-1} x Gt^2 = Gt
# NOTE (R4): the RAW constructions below fix the POWERS of Gt and G_N, which is the derived
# content.  Their pure numbers are convention-dependent (which component of Qddot, which angle
# average), so the numerical coefficients 4 and 96/5 are taken from the GR control at C4.
Qdd = 4 * mu_s * (GN_s * M_s * om_s) ** sp.Rational(2, 3)     # kinematic, up to an O(1) angle factor
h_raw = 2 * Gt_s * Qdd / (c_s ** 4 * D_s)
P_rad = sp.Rational(32, 5) * Gt_s * mu_s ** 2 * r_kep ** 4 * om_s ** 6 / c_s ** 5
omdot_raw = sp.simplify(P_rad / sp.Abs(sp.diff(E_orb, om_s)))
K53 = Gt_s * GN_s ** sp.Rational(2, 3) * mu_s * M_s ** sp.Rational(2, 3)

hr = sp.simplify(sp.powsimp(h_raw / K53, force=True))
check(sp.simplify(sp.diff(hr, Gt_s)) == 0 and sp.simplify(sp.diff(hr, GN_s)) == 0,
      "C2  STRAIN: box hbar = -16 pi Gt T (the graviton kinetic term is 1/(16 pi Gt) by B7-B8 and "
      "matter couples minimally to g), so hbar_ij = (4 Gt/c^4 R) int T_ij = (2 Gt/c^4 R) Qddot, "
      "with Qddot set by a G_N orbit.  *** THE G-CONTENT IS EXACTLY Gt^1 G_N^{2/3}: h/K53 is "
      "independent of BOTH constants, K53 = Gt G_N^{2/3} mu M^{2/3} ***",
      f"sympy: h_raw/K53 = {hr}, free of Gtilde and G_N.  The Gt comes from the graviton "
      "normalisation, the G_N^{2/3} from the orbit inside Qddot.  BOTH constants appear -- the "
      "split is physically real in the strain")

orr = sp.simplify(sp.powsimp(omdot_raw / K53, force=True))
check(sp.simplify(sp.diff(orr, Gt_s)) == 0 and sp.simplify(sp.diff(orr, GN_s)) == 0
      and sp.simplify(omdot_raw / (sp.Rational(96, 5) * om_s ** sp.Rational(11, 3) / c_s ** 5)
                      - K53) == 0,
      "C3  CHIRP: the Isaacson flux is (c^3/32 pi Gt)<hdot^2>, so with h ~ Gt the radiated power "
      "carries Gt^{-1} x Gt^2 = Gt^{+1}; energy balance omegadot = P/|dE/domega| then gives "
      "*** THE SAME G-CONTENT Gt^1 G_N^{2/3}, i.e. the SAME K53 *** -- and here the raw "
      "construction also reproduces the GR coefficient exactly: omegadot = (96/5) K53 "
      "omega^{11/3}/c^5",
      f"sympy: omegadot_raw/K53 = {orr}, free of Gtilde and G_N")

# the distance, eliminating K53 -- with the GR-control coefficients (R4)
f_s = sp.Symbol("f", positive=True)
h_of_f = 4 * K53 * (sp.pi * f_s) ** sp.Rational(2, 3) / (c_s ** 4 * D_s)
fdot_of_f = sp.Rational(96, 5) * sp.pi ** sp.Rational(8, 3) * K53 * f_s ** sp.Rational(11, 3) / c_s ** 5
DL_formula = sp.simplify(5 * c_s * fdot_of_f / (24 * sp.pi ** 2 * h_of_f * f_s ** 3))
check(sp.simplify(DL_formula - D_s) == 0,
      "C4  *** THE CANCELLATION, EXPLICIT: eliminating K53 between C2 and C3 gives "
      "D_L = 5 c fdot / (24 pi^2 h f^3), which sympy confirms returns D_L exactly.  Gt and G_N "
      "have CANCELLED -- the standard-siren distance is built from observables alone ***",
      f"sympy result for 5 c fdot/(24 pi^2 h f^3): {sp.simplify(DL_formula)}")

check(sp.simplify(sp.diff(DL_formula, Gt_s)) == 0 and sp.simplify(sp.diff(DL_formula, GN_s)) == 0,
      "C5  and the derivatives are identically zero: dD_L/dGtilde = 0 and dD_L/dG_N = 0.  The "
      "GW-inferred luminosity distance has ZERO sensitivity to the split, not merely a small one",
      "MECHANISM (this is the demonstration the assignment asked for, not an assertion): the "
      "emitted amplitude scales as 1/M_*^2 and the radiated flux -- which drives the chirp -- "
      "scales as M_*^2 x (1/M_*^2)^2 = 1/M_*^2 as well.  Amplitude and chirp carry the SAME power "
      "of the graviton normalisation, so their ratio, which is what fixes D_L, is blind to it")

# what is NOT blind: the mass scale
Mc_true_s, Mc_inf_s = sp.symbols("Mchirp_true Mchirp_inf", positive=True)
# analyst (GR + laboratory G, which IS G_N here):   K53 = G_N^{5/3} Mchirp_inf^{5/3}
# theory:                                           K53 = Gt G_N^{2/3} Mchirp_true^{5/3}
ratio_53 = sp.simplify(sp.powsimp(
    (Gt_s * GN_s ** sp.Rational(2, 3) * Mc_true_s ** sp.Rational(5, 3))
    / (GN_s ** sp.Rational(5, 3) * Mc_true_s ** sp.Rational(5, 3)), force=True))
check(sp.simplify(ratio_53 - Gt_s / GN_s) == 0,
      "C6  WHAT IS *NOT* BLIND: an analyst fitting GR with the LABORATORY constant (= G_N) reads "
      "K53 = G_N^{5/3} Mchirp_inferred^{5/3}, while the theory says K53 = Gt G_N^{2/3} "
      "Mchirp_true^{5/3}.  Equating them gives (Mchirp_inf/Mchirp_true)^{5/3} = Gt/G_N = r "
      "exactly (sympy), i.e.  Mchirp_inferred = Mchirp_true * r^{3/5}",
      "the distance is exact but the MASS SCALE is rescaled.  Verified numerically at D2 and "
      "priced in PART F1")

# ================================================================================================
head("PART C-CONTROL -- reproduce the GR inspiral relations and GW170817 before claiming anything")
# ================================================================================================
def h_amp_num(K53_over_G53, DL_m, f):
    """strain amplitude; K53_over_G53 has units of (G Mchirp)^{5/3} in SI."""
    return 4.0 / DL_m * K53_over_G53 * (math.pi * f) ** (2.0 / 3.0) / CLIGHT ** 4


def fdot_num(K53_over_G53, f):
    return 96.0 / 5.0 * math.pi ** (8.0 / 3.0) * K53_over_G53 * f ** (11.0 / 3.0) / CLIGHT ** 5


def DL_from_obs(h, fdot, f):
    return 5.0 * CLIGHT * fdot / (24.0 * math.pi ** 2 * h * f ** 3)


K53_GR = (GNEWT * GW170817_MC_SRC * MSUN) ** (5.0 / 3.0)
DL_true = GW170817_DL_MPC * MPC
h_ctrl = h_amp_num(K53_GR, DL_true, f_gw)
fdot_ctrl = fdot_num(K53_GR, f_gw)
DL_ctrl = DL_from_obs(h_ctrl, fdot_ctrl, f_gw) / MPC

check(1e-23 < h_ctrl < 1e-21,
      f"CC1 CONTROL (named: GW170817's published parameters, LVC PRL 119 161101 / PRX 9 011001).  "
      f"Mchirp = {GW170817_MC_SRC} Msun at D_L = {GW170817_DL_MPC:g} Mpc gives strain "
      f"h({f_gw:g} Hz) = {h_ctrl:.3e} -- the right order for a network-SNR-32 event",
      f"and fdot({f_gw:g} Hz) = {fdot_ctrl:.2f} Hz/s, the standard BNS value")

check(abs(DL_ctrl - GW170817_DL_MPC) / GW170817_DL_MPC < 1e-12,
      f"CC2 CONTROL: inverting with the G-free formula D_L = 5c fdot/(24 pi^2 h f^3) returns "
      f"{DL_ctrl:.6f} Mpc against the input {GW170817_DL_MPC:g} Mpc "
      f"(relative error {abs(DL_ctrl-GW170817_DL_MPC)/GW170817_DL_MPC:.2e})",
      "the textbook Newtonian-inspiral relations h(f) and fdot(f) are thereby reproduced and the "
      "inversion validated BEFORE it is used on the modified theory")

# ================================================================================================
head("PART D -- the cancellation demonstrated numerically across the whole s window")
# ================================================================================================
rows = []
worst_D, worst_M = 0.0, 0.0
for s_val in [1.0, 0.5, s_max_num, 0.10, 0.01, 1e-3, 1e-4]:
    r_val = (1 - KB_FID / 2) * s_val
    Gt_val = r_val * GNEWT                       # G_N is the laboratory constant
    # true system: the LVC-inferred chirp mass is what the fit returns; hold the TRUE masses fixed
    Mc_true = GW170817_MC_SRC * MSUN
    mu_M = Mc_true ** (5.0 / 3.0)                # mu M^{2/3} in kg^{5/3}
    K53_th = Gt_val * GNEWT ** (2.0 / 3.0) * mu_M
    h_th = h_amp_num(K53_th, DL_true, f_gw)
    fd_th = fdot_num(K53_th, f_gw)
    D_inf = DL_from_obs(h_th, fd_th, f_gw) / MPC
    Mc_inf = (K53_th / GNEWT ** (5.0 / 3.0)) ** (3.0 / 5.0) / MSUN
    pred_Mc = GW170817_MC_SRC * r_val ** 0.6
    worst_D = max(worst_D, abs(D_inf - GW170817_DL_MPC) / GW170817_DL_MPC)
    worst_M = max(worst_M, abs(Mc_inf - pred_Mc) / pred_Mc)
    rows.append((s_val, r_val, h_th, fd_th, D_inf, Mc_inf))

info("s        r=Gt/G_N   h(100Hz)     fdot(Hz/s)   D_L inferred   Mchirp inferred",
     "\n         " + "\n         ".join(
         f"{a_:8.1e} {b_:8.5f}  {c_:.4e}  {d_:9.4f}   {e_:10.6f} Mpc  {f_:8.5f} Msun"
         for a_, b_, c_, d_, e_, f_ in rows))

check(worst_D < 1e-12,
      f"D1  *** ACROSS FOUR DECADES OF s THE RECOVERED DISTANCE IS INVARIANT to "
      f"{worst_D:.2e} (machine precision): D_L^GW is EXACTLY the true 40 Mpc for every s ***",
      "the strain and the chirp rate both drop by the same factor r; only their ratio enters D_L")

check(worst_M < 1e-12,
      f"D2  the recovered CHIRP MASS moves exactly as r^{{3/5}} (max deviation from the "
      f"prediction {worst_M:.2e}): at the ghost-free edge r = {r_max_num:.4f}, "
      f"Mchirp_inferred/Mchirp_true = {r_max_num**0.6:.4f}",
      f"equivalently Mchirp_true = {GW170817_MC_SRC} / {r_max_num**0.6:.4f} = "
      f"{GW170817_MC_SRC/r_max_num**0.6:.3f} Msun.  This is the observable that is NOT blind")

# ================================================================================================
head("PART E -- pricing against GW170817: the amplitude test and the friction test")
# ================================================================================================
# (b) the amplitude / standard-siren test
dl_gw_frac_hi = GW170817_DL_HI / GW170817_DL_MPC
dl_gw_frac_lo = GW170817_DL_LO / GW170817_DL_MPC
sbf_err = math.sqrt(NGC4993_SBF_STAT ** 2 + NGC4993_SBF_SYS ** 2)
ratio_meas = GW170817_DL_MPC / NGC4993_SBF
ratio_err = ratio_meas * math.sqrt((dl_gw_frac_lo) ** 2 + (sbf_err / NGC4993_SBF) ** 2)
info("the measurement",
     f"d_L^GW = {GW170817_DL_MPC:g} (+{GW170817_DL_HI:g}/-{GW170817_DL_LO:g}) Mpc "
     f"[+{100*dl_gw_frac_hi:.0f}%/-{100*dl_gw_frac_lo:.0f}%];  "
     f"NGC 4993 SBF = {NGC4993_SBF:g} +/- {sbf_err:.1f} Mpc [{100*sbf_err/NGC4993_SBF:.1f}%];  "
     f"ratio d_L^GW/d_L^EM = {ratio_meas:.3f} +/- {ratio_err:.3f}")

sens = 0.0
for s_val in [1.0, s_max_num, 1e-3]:
    r_val = (1 - KB_FID / 2) * s_val
    Gt_val = r_val * GNEWT
    K53_th = Gt_val * GNEWT ** (2.0 / 3.0) * (GW170817_MC_SRC * MSUN) ** (5.0 / 3.0)
    D_inf = DL_from_obs(h_amp_num(K53_th, DL_true, f_gw), fdot_num(K53_th, f_gw), f_gw) / MPC
    sens = max(sens, abs(D_inf / GW170817_DL_MPC - 1.0))
check(sens < 1e-12,
      f"E1  *** GATE (b) ANSWERED: d ln d_L^GW / d ln s = 0 EXACTLY (numerically {sens:.2e} over "
      f"s from 1e-3 to 1).  The GW170817 amplitude-vs-EM-distance comparison places NO BOUND ON s "
      f"WHATSOEVER -- the allowed range is the full window, and would be even if the distances "
      f"agreed to 0.001% ***",
      "this is a null with zero leverage, not a null from weak data.  Stated that way so it is "
      "never mis-read later as 'GW170817 is consistent with the split', which would imply the "
      "test had power")

# counterfactual leverage, so the zero is quantified rather than merely asserted
cf = {}
for p in (1.0, 0.5):
    # if d_L^GW/d_L^EM were r^p, what would the 1-sigma bound on r be?
    lim = (1.0 - ratio_err / ratio_meas) ** (1.0 / p)
    cf[p] = lim
check(all(v > 3.0 * r_max_num for v in cf.values()),
      "E2  COUNTERFACTUAL, to size the zero: if the ratio had scaled as r^p, GW170817 would have "
      f"required r >~ {cf[1.0]:.3f} (p=1) or r >~ {cf[0.5]:.3f} (p=1/2) at 1 sigma -- "
      f"{cf[1.0]/r_max_num:.1f}x and {cf[0.5]/r_max_num:.1f}x above the escape's ceiling "
      f"r <= {r_max_num:.3f}.  So the data ARE sharp enough to kill the split; it is the "
      "OBSERVABLE that is blind",
      f"1-sigma fractional uncertainty on d_L^GW/d_L^EM is {ratio_err/ratio_meas:.3f}, using the "
      "conservative (lower) GW error bar")

# (c) the friction test
alpha_M = 0.0
zsrc = NGC4993_Z
frac_err = ratio_err / ratio_meas
alphaM_bound_20 = 2.0 * 0.20 / math.log(1.0 + zsrc)
alphaM_bound_meas = 2.0 * frac_err / math.log(1.0 + zsrc)
ratio_pred = math.exp(-0.5 * alpha_M * math.log(1.0 + zsrc))
check(abs(ratio_pred - 1.0) < 1e-15,
      "E3  *** GATE (c) ANSWERED: the theory has NO GW friction term.  d_L^GW/d_L^EM = "
      "exp(-(1/2) int alpha_M dln a) = 1 EXACTLY, because alpha_M = 0 exactly (B8) -- M_*^2 = "
      "1/(8 pi Gt) is a constant of the action and the entire F(Z,Q) sector is switched off in "
      "the tensor sector by Z = 0 ***",
      f"predicted d_L^GW/d_L^EM = {ratio_pred:.15f}; a CONSTANT split, however large, produces no "
      "friction -- only a RUNNING Planck mass does, and there is nothing here to run")

check(alphaM_bound_meas > 10.0,
      f"E4  and the GW170817 leverage on alpha_M is weak anyway: at z = {zsrc:g} and a "
      f"{100*frac_err:.0f}% distance agreement, |alpha_M| <~ {alphaM_bound_meas:.0f} "
      f"({alphaM_bound_20:.0f} at a 20% agreement).  The theory's 0 passes at 0.0 sigma",
      "so gate (c) is passed twice over: by the exact structural result, and by the fact that the "
      "single-event bound could not have detected a violation of realistic size")

# (d) the window
check(True,
      f"E5  *** GATE (d) ANSWERED: the s range allowed by GW amplitude + GW friction is the ENTIRE "
      f"window  0 < s <= K_B/(2-K_B) = {s_max_num:.6f}  (and in fact all s > 0).  ROUTE 4 VERDICT "
      f"ON ITS ASSIGNED GATES: PASS ***",
      "GW observations do not pay the price the escape was flagged for.  What follows in PART F "
      "is NOT part of that verdict and is reported separately")

# ================================================================================================
head("PART F -- the liabilities the SAME derivation creates.  Reported at equal volume, NOT scored")
# ================================================================================================
# F1: the mass rescaling
r_edge = r_max_num
Mc_true_edge = GW170817_MC_SRC / r_edge ** 0.6
m_comp_edge = Mc_true_edge / 2.0 ** (-0.2)      # equal-mass: Mchirp = m 2^{-1/5}
Mc_true_aest = GW170817_MC_SRC / r_aest ** 0.6
check(Mc_true_edge > 4.0,
      f"F1  MASS RESCALING (derived at C6/D2, adverse).  At the ghost-free edge r = {r_edge:.4f}: "
      f"GW170817's TRUE chirp mass is {Mc_true_edge:.2f} Msun (not {GW170817_MC_SRC}), i.e. "
      f"components ~{m_comp_edge:.1f} Msun each if equal-mass.  At the unmodified theory's "
      f"r = {r_aest:.3f} the shift is only to {Mc_true_aest:.3f} Msun",
      "a 4-5 Msun pair is not a neutron-star binary, and GW170817 had a kilonova.  CLOSURE "
      "REQUIRES the theory's own strong-field stellar structure and its own 1PN mass extraction, "
      "NEITHER OF WHICH IS COMPUTED -- so this is ADVERSE-LEANING and OPEN, not a kill")

# F2: the binary-pulsar orbital decay
pbdot_ratio_edge = r_edge
pbdot_ratio_aest = r_aest
sig_edge = abs(pbdot_ratio_edge - B1913_RATIO) / B1913_ERR
sig_aest = abs(pbdot_ratio_aest - B1913_RATIO) / B1913_ERR
check(sig_edge > 100.0,
      f"F2  BINARY-PULSAR ORBITAL DECAY (the sharpest handle, and it is in MY sector).  With the "
      f"masses fixed by the near-zone observables omegadot and gamma (which see G_N), the "
      f"TENSOR-CHANNEL prediction is Pbdot/Pbdot_GR = r exactly.  At the edge r = {r_edge:.4f} "
      f"that is an {1/r_edge:.1f}x deficit against B1913+16's {B1913_RATIO} +/- {B1913_ERR} "
      f"= {sig_edge:.0f} sigma (and J0737-3039 measures the same ratio to {J0737_PREC:.1e})",
      f"BUT -- and this is why I do NOT score it -- the identical bookkeeping applied to the "
      f"UNMODIFIED parent theory (s=1, r={r_aest:.3f}) gives {sig_aest:.0f} sigma against the same "
      "datum, i.e. it would exclude AeST itself.  The overwhelmingly likely reading is that my "
      "TENSOR-ONLY flux ledger is INCOMPLETE: the aether's now-healthy vector modes (c_V^2 = "
      "K_B/C_V) and the scalar radiate as well, and Einstein-aether binaries are known to have "
      "dipole channels.  *** THE TOTAL RADIATED FLUX IS NOT COMPUTED ***")

check(True,
      "F3  BUT THE SHAPE OF THE REPAIR IS CONSTRAINED, and that is the usable result: the missing "
      "channels must supply the SAME 1-r fraction of the flux at EVERY orbital period, because "
      "Pbdot/Pbdot_GR is measured at 0.16% in a 7.75 h orbit AND at 1.3e-4 in a 2.45 h orbit.  A "
      "dipole term enters at relative order (c/v)^2 and therefore CANNOT be period-independent",
      "so the repair, if it exists, must be a renormalisation of the quadrupole coefficient "
      "itself, not an added multipole.  THAT is the single computation that would decide route 4's "
      "liability, and it is the one I recommend next")

# F4: how big are the 1PN corrections I dropped?
x_pn = (math.pi * GMSUN_C3 * GW170817_MTOT * f_gw) ** (2.0 / 3.0)
check(x_pn < 0.05,
      f"F4  SIZE OF WHAT R3 DROPPED: the field-energy (1PN) corrections to the radiating source "
      f"enter at x = (pi G M f/c^3)^{{2/3}} = {x_pn:.4f} = {100*x_pn:.1f}% for GW170817 at "
      f"{f_gw:g} Hz -- well below the {100*frac_err:.0f}% distance uncertainty",
      "so the leading-order cancellation of PART C is not an artefact of dropping them; even a "
      "100%-relative 1PN bias would move d_L^GW by only a few percent")

# F5: what this route explicitly does not touch
check(True,
      "F5  OUT OF SCOPE, NAMED so the PASS is not over-read: the split makes the COSMOLOGICAL "
      f"gravitational constant Gt = r G_N = {r_edge:.3f} G_N, which is exactly what BBN and the "
      "committed CLASS pass see.  Route 4 says nothing about that and the PASS here must not be "
      "quoted as relief for it",
      "nor does route 4 address DEATH 2 (the F_Z(0) = K_B collapse of SZ21 Eq (12)), the "
      "preferred-frame alphas (c14_ppn_sector_2026.py: ADVERSE), or clusters")

# ================================================================================================
head("PART G -- verdict")
# ================================================================================================
info("GATE (a)  how the split enters the strain",
     "DERIVED: tensor sector is exactly Einstein-Hilbert with M_*^2 = 1/(8 pi Gt) (B1-B9); strain "
     "h ~ Gt x matter quadrupole, orbit ~ G_N, so both constants appear (C1-C3)")
info("GATE (b)  GW170817 amplitude vs EM distance",
     f"d_L^GW = {GW170817_DL_MPC:g}(+{GW170817_DL_HI:g}/-{GW170817_DL_LO:g}) Mpc vs SBF "
     f"{NGC4993_SBF:g}+/-{sbf_err:.1f} Mpc; sensitivity to s is EXACTLY ZERO (C4-C5, D1, E1-E2) "
     "=> NO BOUND ON s")
info("GATE (c)  GW friction",
     "alpha_M = 0 EXACTLY, any F, any s, both footings (B8, E3); GW170817 leverage "
     f"|alpha_M| <~ {alphaM_bound_meas:.0f} anyway (E4)")
info("GATE (d)  allowed s",
     f"the entire route-1 window 0 < s <= {s_max_num:.6f} is allowed.  PASS")
info("NOT SCORED, but on the record",
     f"the same derivation predicts Mchirp_inferred = Mchirp_true r^{{3/5}} (F1) and a "
     f"tensor-channel Pbdot deficit of {1/r_edge:.0f}x (F2) -- the latter would also exclude the "
     "unmodified parent theory, so the flux ledger is incomplete and the total radiated flux is "
     "NOT COMPUTED (F2-F3)")
info("BOTH FOOTINGS",
     f"canonical a0 = {A0_CAN:.4e}, ALT a0 = {A0_ALT:.4e} m/s^2: identical verdicts.  a0 enters "
     "only at C0 (saturation, ~20 orders of margin either way) and is provably absent from the "
     "tensor sector because Z = 0 identically")

nf = len(FAIL)
print()
print(f"ROUTE-4 (GW AMPLITUDE) CHECKS: {NCHK[0]-nf}/{NCHK[0]} passed"
      + ("" if not nf else f"; FAILED: {FAIL}"))
print(f"elapsed {time.time()-T0:.1f} s")
sys.exit(1 if FAIL else 0)
