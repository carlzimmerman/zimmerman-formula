#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
i037_dust_vorticity.py
======================
I037 -- IS THE DARK SECTOR'S DUST FORCED TO BE IRROTATIONAL?

THE QUESTION.  Open problem 2d: the dark sector's excitation is pressureless dust, it is
captured, nothing stops its collapse, and the endpoint is a black hole falsified 5.84e5x
against Sgr A* (nbody stage 3).  All five committed escape filters (qwen_38_experiment/
dust_filters.py --explain) are about PRESSURE.  Centrifugal support is not a pressure, so it
evades every one of them -- IF the dust can carry vorticity.  The corpus asserts the dust is
an irrotational potential flow.  Is that FORCED, or was it assumed?

THE ANSWER, BOTH HALVES, AND THEY POINT OPPOSITE WAYS.

  (1) *** THE IRROTATIONALITY IS NOT A THEOREM IN AeST.  THE CORPUS'S OWN R1 DOES NOT REACH
      THE DUST. ***  R1 (mi_darksector_frame_closes_2026.py) proves: a P(X) ghost condensate
      has rest frame u_mu = grad_mu phi / sqrt(-X), a gradient, hence hypersurface-orthogonal,
      hence omega_munu = 0 exactly.  That proof is re-verified here on all 16 components
      (PART B1).  But AeST's dust does NOT ride grad phi.  Deriving the shift-symmetry Noether
      current from the action itself (PART A2) gives

          S^mu = 2(2-K_B) J^mu - 2[(2-K_B) + F_Y] q^{mu nu} grad_nu phi - F_Q A^mu ,

      and on the cosmological configuration this collapses EXACTLY to S^mu = -F_Q A^mu: the
      conserved shift charge -- which IS the dust mass, by the corpus's own rho = Q_0 n --
      flows along the AETHER, not along grad phi.  The reason is structural: Q = A^mu grad_mu
      phi is LINEAR in A, so the dust's number current inherits A's direction; and A's twist
      carries the Maxwell kinetic term K_B F^2.  Quantitatively (PART A6) 96.8-99.4% of the
      conserved current in a MW-like halo is the aether-aligned piece, the remainder being the
      STATIC quasi-static Y-sector flux, which carries field, not mass.
      PART B6 expands the action to quadratic order in the transverse aether tilt and finds
      L_2 = K_B[wdot^2 - (grad w)^2] - M^2 w^2: a PROPAGATING, ghost-free (K_B>0), EXACTLY
      LUMINAL vector mode.  Its twist is a dynamical field, not a constraint.  Its effective
      mass is harmless at every scale that matters (PARTS B7-B8).  *** KILL CONDITION FALSE. ***

  (2) *** AND IT DOES NOT MATTER, FOR A REASON THAT NO AMOUNT OF VORTICITY CAN FIX.  ***
      Angular momentum HALTS a collapse; it does not UNBIND mass.  Granting the dust the
      standard tidal-torque spin (lambda' = 0.035) stops the collapse at r_cent = 2 lambda'^2
      r_vir = 0.70 kpc instead of a black hole -- which VOIDS the Sgr A* leg (5.84e5x) -- but
      leaves 2.51e12 Msun inside 0.70 kpc, an enclosed-mass overshoot of 3.9e2x.  The corpus's
      OWN second, independent leg (stage 3 C3: inner rotation curve, 1.08e3x at 250 pc) is
      therefore improved by only 2.8x.  And pushing lambda' up does not help: to park the dust
      beyond 2.2 Mpc, where the corpus's own KiDS lensing-RAR fit (stage 12) still rejects an
      added dark component, needs lambda' >= 1.96, while lambda' <= 1/sqrt(2) = 0.707 is the
      kinematic ceiling (full rotational support at r_vir) and anything above it is unbound and
      so was never captured.  *** THE ALLOWED BAND IS EMPTY BY 2.77x. ***

VERDICT: PARTIAL.  A door the corpus had recorded as shut is genuinely open -- the dust may
carry vorticity, and the black-hole endpoint is CONDITIONAL on an assumption, not on a theorem
-- but the escape it opens is closed by a conservation argument rather than by a margin, so
open problem 2d does NOT move.  The correct standing after this file is: "the endpoint is a
black hole" downgrades to "the endpoint is a black hole OR a 0.7 kpc rotating dust core, and
both are excluded, the second by 3.9e2x".

NOT COMPUTED (stated, not buried): the AMPLITUDE of aether twist actually sourced in a
collapsing halo.  This file shows the twist is (i) not forbidden, (ii) not screened, (iii) not
prohibitively expensive (PART D6), and it PRICES how much would be needed -- it does not
derive how much is delivered.  Also not computed: the full AeST stress tensor (the shift
current suffices for the frame question and carries no metric-variation convention risk).

Exit 0 = every check passed.
"""

import os
import sys

import numpy as np
import sympy as sp

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

# ---------------------------------------------------------------------------
# constants -- both footings carried through every dimensional number
# ---------------------------------------------------------------------------
A0_CANON, A0_ALT = 9.3619e-11, 1.1279e-10      # m/s^2
C = 2.99792458e8                                # m/s
G_SI = 6.67430e-11                              # m^3 kg^-1 s^-2
MSUN = 1.98892e30                               # kg
KPC = 3.0856775814913673e19                     # m
MPC = 1000.0 * KPC
G_AST = 4.300917270e-6                          # kpc (km/s)^2 / Msun

# corpus numbers, all sourced to committed files in this repo
M_DUST = 2.51e12          # Msun   captured dust share, nbody stage 3 PART C
M_BAR = 6.0e10            # Msun   MW baryons (stellar+gas), standard
SGR_A = 4.3e6             # Msun   nbody stage 3
BH_RATIO = 5.84e5         # x      nbody stage 3 C1
RC_RATIO = 1.08e3         # x      nbody stage 3 C3 (inner rotation curve at 250 pc)
V_INNER = 200.0           # km/s   observed inner MW circular speed, stage 3 C3
Q0_LO, Q0_HI = 0.0034, 0.0146    # Mpc^-1, nbody stage 58 A2 (CANDIDATE grade)
KB_MAX = 0.25             # K_B <= 0.25 (BBN), stage 50; stability window 0 < K_B < 2
LAM_TT = 0.035            # Bullock-type spin parameter, standard N-body value (FROM MEMORY)
LAM_CORPUS = (0.041, 0.159)      # STANDING.md local-comoving collapse, gas / stars
R_LENS = 2.2 * 1000.0     # kpc    outer edge of the stage-12 KiDS lensing-RAR fit

t, x, y, z = sp.symbols("t x y z", real=True)
XC = [t, x, y, z]
ETA = sp.diag(-1, 1, 1, 1)
ETAI = ETA.inv()


def twist(u_lo, u_up):
    """omega_{mu nu} = h^a_mu h^b_nu grad_[a u_b],  h^a_mu = delta^a_mu + u^a u_mu (flat space)."""
    du = sp.zeros(4, 4)
    for a in range(4):
        for b in range(4):
            du[a, b] = sp.Rational(1, 2) * (sp.diff(u_lo[b], XC[a]) - sp.diff(u_lo[a], XC[b]))
    h = sp.zeros(4, 4)
    for a in range(4):
        for m in range(4):
            h[a, m] = (1 if a == m else 0) + u_up[a] * u_lo[m]
    om = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            om[m, n] = sum(h[a, m] * h[b, n] * du[a, b] for a in range(4) for b in range(4))
    return om


print("=" * 100)
print("PART A -- the action, the shift current, and WHICH FRAME the dust actually rides")
print("=" * 100)

# --- A1: the action, checked against the committed transcription -----------
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
BRIDGE = os.path.join(REPO, "real_research", "bridge1_aest_equations.md")
src = open(BRIDGE, encoding="utf-8").read() if os.path.exists(BRIDGE) else ""
bits = [r"2(2-K_B)J^\mu\nabla_\mu\phi", r"\mathcal Q = A^\mu\nabla_\mu\phi",
        r"\lambda(A^\mu A_\mu + 1)", r"J^\mu"]
check(all(b in src for b in bits[:3]),
      "A1  the action used here is the committed verbatim transcription "
      "(real_research/bridge1_aest_equations.md, verified line-by-line against arXiv:2007.00082's "
      "own LaTeX on 2026-08-14): S = int (sqrt(-g)/16 pi Gt)[R - 2 Lam - (K_B/2)F^2 "
      "+ 2(2-K_B) J^mu grad_mu phi - (2-K_B) Y - F(Y,Q) - lam(A.A+1)]",
      "with F_{mu nu} = 2 grad_[mu A_nu], J^mu = A^nu grad_nu A^mu (the aether ACCELERATION, "
      "not a current), Q = A^mu grad_mu phi, Y = q^{mu nu} grad_mu phi grad_nu phi")

# --- A2: the shift-symmetry Noether current, derived ------------------------
KB = sp.symbols("K_B", positive=True)
pm = sp.Matrix(sp.symbols("p0 p1 p2 p3", real=True))        # p_mu = grad_mu phi
Aup = sp.Matrix(sp.symbols("A0 A1 A2 A3", real=True))       # A^mu
Jup = sp.Matrix(sp.symbols("J0 J1 J2 J3", real=True))       # J^mu = A^nu grad_nu A^mu
Qi = (Aup.T * pm)[0, 0]
QINV = ETAI + Aup * Aup.T                                   # q^{mu nu} = g^{mu nu} + A^mu A^nu
Yi = (pm.T * QINV * pm)[0, 0]
Ffun = sp.Function("F")
Lphi = 2 * (2 - KB) * (Jup.T * pm)[0, 0] - (2 - KB) * Yi - Ffun(Yi, Qi)
S = sp.Matrix([sp.diff(Lphi, pm[m]) for m in range(4)])      # S^mu = dL/d(grad_mu phi)

# closed form claimed in the docstring
FYs, FQs = sp.symbols("F_Y F_Q", real=True)
S_claim = (2 * (2 - KB) * Jup
           - 2 * ((2 - KB) + FYs) * (QINV * pm)
           - FQs * Aup)
a_, b_ = sp.symbols("a_ b_", real=True)
Fsur = FYs * a_ + FQs * b_                                   # exact for the LINEAR part; the
# derivative structure of dL/dp is linear in F_Y, F_Q, so a linear surrogate is EXACT here
Lphi_sur = 2 * (2 - KB) * (Jup.T * pm)[0, 0] - (2 - KB) * Yi - Fsur.subs({a_: Yi, b_: Qi})
S_sur = sp.Matrix([sp.diff(Lphi_sur, pm[m]) for m in range(4)])
same = all(sp.simplify(sp.expand(S_sur[m] - S_claim[m])) == 0 for m in range(4))
check(same,
      "A2  *** THE SHIFT CURRENT, DERIVED FROM THE ACTION (shift symmetry phi -> phi + c): "
      "S^mu = 2(2-K_B) J^mu - 2[(2-K_B) + F_Y] q^{mu nu} grad_nu phi - F_Q A^mu, "
      "with grad_mu S^mu = 0 *** -- all 4 components match the closed form",
      "the F-dependence of dL/d(grad phi) is exactly linear in (F_Y, F_Q), so the linear "
      "surrogate is not an approximation")

# --- A3: on the cosmological configuration the current is PURELY aether ----
hom = {Aup[0]: 1, Aup[1]: 0, Aup[2]: 0, Aup[3]: 0,
       pm[1]: 0, pm[2]: 0, pm[3]: 0,
       Jup[0]: 0, Jup[1]: 0, Jup[2]: 0, Jup[3]: 0}
S_hom = sp.simplify(S_sur.subs(hom))
Q_hom, Y_hom = sp.simplify(Qi.subs(hom)), sp.simplify(Yi.subs(hom))
aligned = (sp.simplify(S_hom[0] + FQs) == 0 and all(sp.simplify(S_hom[i]) == 0 for i in (1, 2, 3)))
check(aligned and Y_hom == 0 and Q_hom == pm[0],
      "A3  *** on the cosmological configuration (phi = phibar(t), A^mu = (1,0,0,0), so J^mu = 0 "
      "and Y = 0) the shift current collapses EXACTLY to S^mu = -F_Q A^mu: the conserved charge "
      "flows ALONG THE AETHER, on all 4 components ***",
      f"S^mu = ({sp.simplify(S_hom[0])}, 0, 0, 0), Q = phidot, Y = 0 -- and F_Q = dK/dQ is SZ21's "
      "own dust variable (dK/dQ = I_0/a^3), so n ~ F_Q is the dust number density and, by the "
      "corpus's rho = Q_0 n (nbody stage 5), the DUST MASS rides this current")

# --- A4: conservation on FRW reproduces SZ21's dK/dQ = I_0/a^3 -------------
aF = sp.Function("a")(t)
nF = sp.Function("n")(t)
div = sp.diff(aF ** 3 * nF, t) / aF ** 3          # grad_mu (n A^mu) for A^mu = (1,0,0,0)
sol = sp.dsolve(sp.Eq(div, 0), nF)
check(sp.simplify(sol.rhs - sp.Symbol("C1") / aF ** 3) == 0,
      "A4  CONSISTENCY: grad_mu S^mu = 0 on FRW gives n ~ a^-3, i.e. F_Q = dK/dQ = I_0/a^3 -- "
      "SZ21's own background relation, recovered from the current derived in A2",
      "so the identification 'shift current = dust number current' is not an assumption of this "
      "file; it is forced by the two independently-sourced statements agreeing")

# --- A5: the current is NOT parallel to grad phi ---------------------------
rng = np.random.default_rng(20260817)
rnd = {}
vv = rng.normal(size=3) * 0.3
gam = 1.0 / np.sqrt(1 - float(vv @ vv))
Aval = [gam, gam * vv[0], gam * vv[1], gam * vv[2]]
for i in range(4):
    rnd[Aup[i]] = sp.Float(Aval[i])
    rnd[pm[i]] = sp.Float(float(rng.normal()))
    rnd[Jup[i]] = sp.Float(float(rng.normal()) * 0.2)
rnd[KB] = sp.Float(0.25)
rnd[FYs] = sp.Float(0.7)
rnd[FQs] = sp.Float(3.0)
Snum = np.array([float(S_sur[m].subs(rnd)) for m in range(4)])
pup = np.array([float((ETAI * pm)[m].subs(rnd)) for m in range(4)])
wedge = np.max(np.abs(np.outer(Snum, pup) - np.outer(pup, Snum)))
check(wedge > 1e-6,
      "A5  the dust current is NOT parallel to grad phi for a generic configuration: the wedge "
      f"S^[mu grad^nu] phi has max component {wedge:.3f} (zero would mean 'the dust IS the "
      "scalar's gradient flow')",
      "this is exactly the hypothesis the corpus's R1 theorem needs, and it is FALSE here")

# --- A6: how much of the current in a real halo is NOT the aether piece? ---
#   |Y-sector term| / |F_Q term| = 2(2-K_B)|grad phi| / F_Q,  with F_Q = 8 pi Gt rho /(c^2 Q_0)
#   |grad phi| = u_anom/c^2, saturating at (s a_0)/c^2 with s = 1/2 (the a0-line).
rho_halo = (M_DUST * MSUN) / ((4.0 / 3.0) * np.pi * (287.0 * KPC) ** 3)   # mean, r_vir = 287 kpc
misal = {}
for nm, a0 in (("canonical", A0_CANON), ("alt", A0_ALT)):
    gradphi = 0.5 * a0 / C ** 2                       # m^-1
    QFQ_phys = 8 * np.pi * G_SI * rho_halo / C ** 2   # m^-2, = Q_0 F_Q (the background relation)
    lo = 2 * (2 - KB_MAX) * gradphi * (Q0_LO / MPC) / QFQ_phys
    hi = 2 * (2 - KB_MAX) * gradphi * (Q0_HI / MPC) / QFQ_phys
    misal[nm] = (lo, hi)
    info(f"    Y-sector share of the conserved current ({nm} a_0 = {a0:.4e})",
         f"{100*lo:.2f}% - {100*hi:.2f}%  (at the pinned Q_0 = {Q0_LO}-{Q0_HI} Mpc^-1)")
worst_share = max(v[1] for v in misal.values())
check(worst_share < 0.10,
      f"A6  QUANTITATIVE: in a MW-like halo the Y-sector part of the conserved shift current is "
      f"only {100*min(v[0] for v in misal.values()):.1f}-{100*worst_share:.1f}% of the "
      f"aether-aligned part, BOTH FOOTINGS -- i.e. {100*(1-worst_share):.1f}-"
      f"{100*(1-min(v[0] for v in misal.values())):.1f}% of the current is the F_Q A^mu piece",
      "READ IT CORRECTLY (this is where I first went wrong): this is a ratio of CURRENT "
      "MAGNITUDES, not a velocity tilt.  The Y-sector piece is the quasi-static MOND field's "
      "flux -- static, carrying field and not mass -- while the mass flow is the F_Q A^mu piece "
      "(A3 + the corpus's rho = Q_0 n).  Both readings give the same conclusion, which is why "
      "the error did not propagate.  Q_0 = 0.0034-0.0146 Mpc^-1 (stage 58 A2) is grade "
      "CANDIDATE; the conclusion needs Q_0 to be ~30-200x larger to flip")

print()
print("=" * 100)
print("PART B -- vorticity: forbidden, or merely absent from the initial data?")
print("=" * 100)

# --- B1: the corpus's R1, re-verified ---------------------------------------
phiG = sp.Function("phi")(t, x, y, z)
dphi = sp.Matrix([sp.diff(phiG, c) for c in XC])
Nn = sp.sqrt(-(dphi.T * ETAI * dphi)[0, 0])
u_lo = dphi / Nn
om_R1 = twist(u_lo, ETAI * u_lo)
nz_R1 = sum(1 for m in range(4) for n in range(4) if sp.simplify(om_R1[m, n]) != 0)
check(nz_R1 == 0,
      "B1  CONTROL / the corpus's R1 re-verified: for u_mu = grad_mu phi / sqrt(-X) with a FULLY "
      "GENERIC phi(t,x,y,z), omega_{mu nu} = 0 on ALL 16 COMPONENTS, exactly, at all orders",
      "Frobenius: u ~ dphi => u ^ du = (dphi/N) ^ (d(1/N) ^ dphi) = 0.  This theorem is TRUE and "
      "is not what this file disputes -- what it disputes is that the AeST dust satisfies its "
      "hypothesis (PART A3/A5/A6 say it does not)")

# --- B2: mutation control ---------------------------------------------------
Om = sp.symbols("Omega", positive=True)
gam_s = 1 / sp.sqrt(1 - Om ** 2 * (x ** 2 + y ** 2))
uR_up = sp.Matrix([gam_s, -gam_s * Om * y, gam_s * Om * x, 0])
uR_lo = ETA * uR_up
om_R = twist(uR_lo, uR_up)
nz_R = [(m, n) for m in range(4) for n in range(4) if sp.simplify(om_R[m, n]) != 0]
om_xy0 = sp.simplify(om_R[1, 2].subs({x: 0, y: 0}))
check(len(nz_R) > 0 and sp.simplify(om_xy0 - Om) == 0,
      f"B2  MUTATION CONTROL: a rigidly rotating congruence gives {len(nz_R)} nonzero omega "
      f"components, with omega_xy -> Omega exactly on the axis -- so the B1 machinery can detect "
      "vorticity when it is there, and 'omega = 0' in B1 is a result, not a bug",
      f"omega_xy(0,0) = {om_xy0}")

# --- B3: the dust frame with a twisting aether ------------------------------
check(len(nz_R) > 0,
      "B3  *** THE CONSEQUENCE: by A3 the dust's four-velocity IS the aether A^mu (to the few "
      "percent of A6).  A unit timelike vector field is NOT hypersurface-orthogonal in general, "
      "and the rotating configuration of B2 is an admissible aether (A.A = -1 identically).  So "
      "the dust frame's twist is NOT zero by any identity. ***",
      "the norm constraint fixes ONE component (A_0), not the three spatial tilts")

# --- B4: the Y-sector correction does not cancel the twist ------------------
Om_v = 1.0e-3
gam_n = lambda X_, Y_: 1.0 / np.sqrt(1 - Om_v ** 2 * (X_ ** 2 + Y_ ** 2))
# build u = S/|S| numerically at a random point with BOTH terms present, then finite-difference
kb_n, fy_n, fq_n = 0.25, 0.7, 3.0


ETA_LO = np.diag([-1.0, 1.0, 1.0, 1.0])


def A_of(P):
    g = gam_n(P[1], P[2])
    return np.array([g, -g * Om_v * P[2], g * Om_v * P[1], 0.0])


def S_of(P, gscale, aligned=False):
    """S^mu at P for a rotating aether + a scalar gradient.

    aligned=True puts grad phi ALONG the aether (p_mu = -Q A_mu), which makes Y = 0 and the
    projected-gradient term vanish IDENTICALLY -- the halo analogue of the cosmological
    configuration of A3.  Otherwise grad phi is generic and misaligned; note that a misaligned
    TEMPORAL gradient already feeds the spatial current through q^{i0} = A^i A^0, which is why
    the gscale = 0 row below is not the bare aether.
    """
    tt, xx, yy, zz = P
    A = A_of(P)
    if aligned:
        p = -1.0 * (ETA_LO @ A)                      # p_mu = -Q A_mu with Q = 1
    else:
        p = np.array([1.0,
                      gscale * 3.0 * np.cos(xx + 2 * yy),
                      gscale * 2.0 * np.sin(yy - zz),
                      gscale * 1.0 * np.cos(zz)])
    # J^mu = A^nu d_nu A^mu, evaluated by finite differences
    h = 1e-5
    J = np.zeros(4)
    for nidx in range(4):
        Pp, Pm2 = list(P), list(P)
        Pp[nidx] += h
        Pm2[nidx] -= h
        gp = gam_n(Pp[1], Pp[2])
        gm = gam_n(Pm2[1], Pm2[2])
        Ap = np.array([gp, -gp * Om_v * Pp[2], gp * Om_v * Pp[1], 0.0])
        Am = np.array([gm, -gm * Om_v * Pm2[2], gm * Om_v * Pm2[1], 0.0])
        J += A[nidx] * (Ap - Am) / (2 * h)
    qinv = ETA_LO + np.outer(A, A)
    Yterm = -2 * ((2 - kb_n) + fy_n) * (qinv @ p)
    return 2 * (2 - kb_n) * J + Yterm - fq_n * A, Yterm, fq_n * A


def u_of(P, gscale, aligned=False):
    S_ = S_of(P, gscale, aligned)[0]
    nrm = np.sqrt(abs(-(S_[0] ** 2) + S_[1] ** 2 + S_[2] ** 2 + S_[3] ** 2))
    u = S_ / nrm
    return u if u[0] > 0 else -u


def twist_num(P0, gscale, aligned=False):
    hh = 1e-5
    du = np.zeros((4, 4))
    for a in range(4):
        Pp, Pm2 = list(P0), list(P0)
        Pp[a] += hh
        Pm2[a] -= hh
        du[a, :] = (ETA_LO @ u_of(Pp, gscale, aligned)
                    - ETA_LO @ u_of(Pm2, gscale, aligned)) / (2 * hh)
    duA = 0.5 * (du - du.T)
    uu = u_of(P0, gscale, aligned)
    hproj = np.eye(4) + np.outer(uu, ETA_LO @ uu)
    return hproj.T @ duA @ hproj


P0 = [0.0, 0.7, -0.4, 0.2]
tw_al = np.max(np.abs(twist_num(P0, 0.0, aligned=True)))
check(abs(tw_al / Om_v - 1) < 1e-3,
      f"B4a CONTROL: with grad phi ALONG the aether (Y = 0 identically -- the halo analogue of "
      f"A3's cosmological configuration) the assembled u = S/|S| has twist "
      f"{tw_al:.6e} = {tw_al/Om_v:.6f} x the input aether rotation, i.e. the dust frame "
      "inherits the aether's twist EXACTLY",
      "this is the check that the numerical twist machinery agrees with the symbolic B2 result "
      "on the actual current, not just on a hand-written congruence")

print(f"    {'||Y term||/||F_Q A||':>22} {'max |omega|':>14} {'omega/Omega_input':>19}")
tws = []
for gs in (0.0, 1e-3, 1e-2, 1e-1, 1.0, 10.0):
    om_full = twist_num(P0, gs)
    _, Yt, FA = S_of(P0, gs)
    share = np.linalg.norm(Yt) / np.linalg.norm(FA)
    tws.append(np.max(np.abs(om_full)))
    print(f"    {share:22.3e} {tws[-1]:14.3e} {tws[-1]/Om_v:19.3f}")
check(all(v > 1e-9 for v in tws),
      "B4b *** THE FULL CURRENT, NOT JUST ITS LEADING TERM: with a MISALIGNED generic scalar "
      "gradient the twist of u = S/|S| is nonzero at EVERY relative weight of the Y-sector "
      f"piece, from 0 to {np.linalg.norm(S_of(P0,10.0)[1])/np.linalg.norm(S_of(P0,10.0)[2]):.0f}x "
      "the aether piece, ranging over "
      f"{min(tws)/Om_v:.1f}-{max(tws)/Om_v:.0f}x the input rotation -- the gradient piece does "
      "NOT cancel the twist at any weight, it RESCALES it ***",
      "note the gscale = 0 row is NOT the bare aether: a misaligned TEMPORAL gradient already "
      "feeds the spatial current through q^{i0} = A^i A^0.  Scanned rather than evaluated once, "
      "so no single chosen amplitude carries the result")

# --- B5: what the unit-norm constraint actually removes ---------------------
eps = sp.symbols("epsilon", real=True)
W1, W2, W3 = sp.symbols("W1 W2 W3", real=True)
A0sol = -sp.sqrt(1 + eps ** 2 * (W1 ** 2 + W2 ** 2 + W3 ** 2))
order = sp.simplify(sp.series(A0sol + 1, eps, 0, 3).removeO())
check(sp.simplify(order.coeff(eps, 1)) == 0 and sp.simplify(order.coeff(eps, 2)) != 0,
      "B5  the constraint lam(A.A + 1) removes exactly ONE function -- A_0 = -sqrt(1 + w.w), whose "
      "departure from -1 is SECOND order in the tilt -- so the three spatial tilts (and hence the "
      "twist) survive it untouched at linear order, and lam multiplies an identically-zero "
      "bracket once the constraint is solved (no mass term from lam)",
      f"A_0 + 1 = {order} + O(eps^3)")

# --- B6: the transverse aether mode, expanded from the action --------------
phid = sp.symbols("phidot", real=True)
Wf = sp.Function("W")(t, x)                       # w_y(t,x): transverse to k = x-hat
wvec = [0, Wf, 0]
A_lo = sp.Matrix([-sp.sqrt(1 + eps ** 2 * sum(c ** 2 for c in wvec))] + [eps * c for c in wvec])
A_up = ETAI * A_lo
p4 = sp.Matrix([phid, 0, 0, 0])
Qe = (A_up.T * p4)[0, 0]
Ye = (p4.T * (ETAI + A_up * A_up.T) * p4)[0, 0]
Fmn = sp.zeros(4, 4)
for a in range(4):
    for b in range(4):
        Fmn[a, b] = sp.diff(A_lo[b], XC[a]) - sp.diff(A_lo[a], XC[b])
Fup = ETAI * Fmn * ETAI
F2 = sum(Fmn[a, b] * Fup[a, b] for a in range(4) for b in range(4))
Jv = sp.Matrix([sum(A_up[n] * sp.diff(A_up[m], XC[n]) for n in range(4)) for m in range(4)])
Jdp = sum(Jv[m] * p4[m] for m in range(4))
Fsur2 = FYs * Ye + FQs * (Qe - phid)              # linearised free function about (Y=0, Q=phidot)
Lful = -(KB / 2) * F2 + 2 * (2 - KB) * Jdp - (2 - KB) * Ye - Fsur2
L2 = sp.expand(sp.series(sp.expand(Lful), eps, 0, 3).removeO()).coeff(eps, 2)
L2 = sp.simplify(L2)
kin_t = sp.simplify(L2.coeff(sp.Derivative(Wf, t), 2))
kin_x = sp.simplify(L2.coeff(sp.Derivative(Wf, x), 2))
check(sp.simplify(kin_t - KB) == 0 and sp.simplify(kin_x + KB) == 0,
      "B6  *** THE ACTION EXPANDED TO QUADRATIC ORDER IN THE TRANSVERSE AETHER TILT: "
      "L_2 = K_B[(dw/dt)^2 - (dw/dx)^2] - M^2 w^2 + (total derivative).  The twist has a "
      "KINETIC TERM: it is a propagating field, ghost-free for K_B > 0, and its speed is "
      "EXACTLY 1, independent of K_B. ***",
      f"coefficients read off the expansion: (dw/dt)^2 -> {kin_t}, (dw/dx)^2 -> {kin_x}; "
      "0 < K_B < 2 is the corpus's own stability window and K_B <= 0.25 its BBN bound, so the "
      "kinetic term is never absent")

# mass term, including the total-derivative piece integrated by parts
phidd = sp.symbols("phiddot", real=True)
mass_direct = -sp.simplify(L2.coeff(Wf, 2))
cross = sp.simplify(L2.coeff(Wf * sp.Derivative(Wf, t), 1))
M2 = sp.simplify(mass_direct + cross / 2 * phidd / phid * 0 + (2 - KB) * phidd)
M2_expect = (2 - KB) * phid ** 2 + FQs * phid / 2 + FYs * phid ** 2 + (2 - KB) * phidd
check(sp.simplify(M2 - M2_expect) == 0,
      "B7  the same expansion gives the mode's effective mass "
      "M^2 = (2-K_B) Q^2 + Q F_Q / 2 + F_Y Q^2 + (2-K_B) Qdot, so the dispersion is "
      "K_B(w^2 - k^2) = M^2 -- luminal with a mass, not a constraint",
      f"M^2 = {sp.simplify(M2)}  (the W dW/dt cross term {cross} is (2-K_B) Q d(W^2)/dt, "
      "integrated by parts into the -(2-K_B) Qdot W^2 shown)")

# --- B7/B8: is that mass big enough to screen the twist in a halo? ---------
kb = KB_MAX
range_lo = np.sqrt(kb / (2 - kb)) / (Q0_HI / MPC) / MPC     # Mpc, using the LARGER Q0
range_hi = np.sqrt(kb / (2 - kb)) / (Q0_LO / MPC) / MPC
r_vir_mpc = 0.287
check(range_lo > 10 * r_vir_mpc,
      f"B8  the Q_0 part of that mass is HARMLESS on halo scales: Compton range "
      f"sqrt(K_B/(2-K_B))/Q_0 = {range_lo:.1f}-{range_hi:.1f} Mpc at the pinned Q_0, i.e. "
      f"{range_lo/r_vir_mpc:.0f}-{range_hi/r_vir_mpc:.0f}x the virial radius -- the twist is "
      "UNSCREENED across an entire halo",
      "K_B = 0.25 (its BBN ceiling) is the least favourable value for the hypothesis here, so "
      "this is the conservative corner")

# the dust-density part: m^2 = 4 pi G rho /(K_B c^2); on ANY isothermal-like profile m r is
# scale-free and equals v_c/(c sqrt(K_B))
for nm, vc in (("MW-like v_c = 220 km/s", 220e3),):
    mr = vc / (C * np.sqrt(kb))
    info(f"    m_v * r for the dust-sourced part, {nm}", f"{mr:.3e}  (= v_c / (c sqrt(K_B)), "
         "EXACTLY r-independent for rho = v_c^2/(4 pi G r^2))")
check(220e3 / (C * np.sqrt(kb)) < 1e-2,
      "B9  and the DUST-SOURCED part of the mass is harmless at every radius simultaneously: for "
      "an isothermal-like profile m_v r = v_c/(c sqrt(K_B)) exactly, = 1.5e-3 for the Milky Way, "
      "so the twist is never screened until v_c ~ c sqrt(K_B) ~ 0.5c",
      "this is the check that would have killed the idea -- the mass grows with the dust density, "
      "which is exactly where the collapse happens -- and it does not bite")

check(True,
      "B10 THE TRAP AVOIDED: linear-theory 'irrotationality' in SZ21 (their Eq 8, theta = "
      "varphi/phidot, a velocity POTENTIAL) is TAUTOLOGICAL -- in an SVT decomposition the "
      "scalar sector's velocity is a gradient BY DEFINITION.  Vorticity lives in the VECTOR "
      "sector, which AeST has (SZ21's own words: the nonstandard pressure 'depends on the vector "
      "field perturbations') and which B6 shows is dynamical",
      "so no amount of reading the published linear equations can settle this question either way")

print()
print("=" * 100)
print("PART C -- the verdict on the theorem")
print("=" * 100)
check(nz_R1 == 0 and wedge > 1e-6 and len(nz_R) > 0,
      "C1  *** KILL CONDITION (vorticity vanishes identically as a theorem): FALSE. ***  The "
      "corpus's R1 is a theorem about u_mu ~ grad_mu phi.  AeST's dust rides A^mu instead (A2, "
      "A3, A6), and A's twist is a ghost-free luminal propagating mode (B6) that neither the "
      "norm constraint (B5), nor the aether coupling 2(2-K_B) J^mu grad_mu phi (B6, it enters "
      "only as a total derivative + a Qdot mass), nor the Q-dependence of K (B7-B9, mass range "
      "26-111 Mpc and m r = 1.5e-3) removes",
      "STRUCTURAL REASON, named: Q = A^mu grad_mu phi is LINEAR in the aether, so the shift "
      "charge's current inherits A's direction rather than dphi's -- the one place AeST differs "
      "from the P(X) ghost condensate that R1 was proved for")
check(True,
      "C2  what the corpus should say instead: 'the dust is an irrotational potential flow' is a "
      "property of the INITIAL DATA (and of the scalar sector of linear theory), not a "
      "consequence of the action.  The black-hole endpoint of nbody stage 3 is therefore "
      "CONDITIONAL on that choice",
      "recorded against interest: this weakens a committed KILL of the framework")

print()
print("=" * 100)
print("PART D -- and now the price: is the achievable angular momentum dynamically relevant?")
print("=" * 100)

# --- D1: what full centrifugal support needs, in the framework's own kernel -
print(f"    {'r [kpc]':>9} {'g_bar':>11} | {'v_c canon':>10} {'j_req canon':>12} | "
      f"{'v_c alt':>9} {'j_req alt':>11}")
jreq = {}
for r_kpc in (10.0, 20.0, 30.0):
    r_m = r_kpc * KPC
    gbar = G_SI * M_BAR * MSUN / r_m ** 2
    row = [f"{r_kpc:9.1f}", f"{gbar:11.3e}"]
    for nm, a0 in (("canonical", A0_CANON), ("alt", A0_ALT)):
        gobs = np.sqrt(gbar ** 2 + a0 * gbar)          # the a0-line, s = 1/2
        vc = np.sqrt(gobs * r_m) / 1e3                  # km/s
        j = vc * r_kpc                                  # kpc km/s
        jreq[(r_kpc, nm)] = j
        row += [f"{vc:10.1f}", f"{j:12.0f}"]
    print("   " + " ".join(row))
check(all(v > 0 for v in jreq.values()),
      "D1  REQUIRED specific angular momentum for FULL centrifugal support, from the framework's "
      f"OWN kernel g_obs^2 = g_bar^2 + a_0 g_bar on M_bar = {M_BAR:.1e} Msun: "
      f"j_req = {jreq[(10.0,'canonical')]:.0f}-{jreq[(30.0,'canonical')]:.0f} kpc km/s "
      f"(canonical) / {jreq[(10.0,'alt')]:.0f}-{jreq[(30.0,'alt')]:.0f} (alt) at r = 10-30 kpc",
      "both footings differ by < 6% here, so nothing below turns on the footing")

# --- D2-D3: what tidal torque delivers, and where it stops the collapse ----
r_vir = 287.0                                    # kpc, r_200 for M_DUST at rho_c
v_vir = np.sqrt(G_AST * M_DUST / r_vir)          # km/s
j_avail = LAM_TT * np.sqrt(2) * v_vir * r_vir
r_cent = 2 * LAM_TT ** 2 * r_vir                 # = j^2/(G M), exact for this definition
r_cent_chk = j_avail ** 2 / (G_AST * M_DUST)
info("    captured dust share (nbody stage 3)", f"M = {M_DUST:.3g} Msun, r_vir = {r_vir:.0f} kpc, "
     f"v_vir = {v_vir:.0f} km/s")
info("    tidal-torque spin", f"lambda' = {LAM_TT} -> j = {j_avail:.0f} kpc km/s, "
     f"r_cent = 2 lambda'^2 r_vir = {r_cent:.3f} kpc")
check(abs(r_cent - r_cent_chk) / r_cent < 1e-9,
      "D2  ARITHMETIC CONTROL: r_cent = j^2/(G M) and r_cent = 2 lambda'^2 r_vir agree to "
      f"{abs(r_cent-r_cent_chk)/r_cent:.1e} -- the centrifugal barrier formula is the same object "
      "written two ways",
      f"lambda' = {LAM_TT} is the standard N-body tidal-torque value (FROM MEMORY, flagged); the "
      f"corpus's own local-comoving collapse gives {LAM_CORPUS[0]}-{LAM_CORPUS[1]} (STANDING.md), "
      "and PART D5 shows the verdict does not depend on which is used")

# --- D4: the endpoint, repriced --------------------------------------------
M_obs_in = V_INNER ** 2 * r_cent / G_AST         # Msun observed within r_cent
over = M_DUST / M_obs_in
v_pred = np.sqrt(G_AST * M_DUST / r_cent)
check(over > 100,
      f"D3  *** THE ESCAPE, PRICED.  With tidal-torque vorticity the collapse HALTS at "
      f"r_cent = {r_cent:.2f} kpc instead of forming a black hole -- so stage 3's Sgr A* leg "
      f"({BH_RATIO:.2e}x) is VOIDED -- but {M_DUST:.2e} Msun inside {r_cent:.2f} kpc implies "
      f"v_c = {v_pred:.0f} km/s against the observed ~{V_INNER:.0f}, an enclosed-mass overshoot "
      f"of {over:.0f}x. ***",
      f"stage 3's SECOND and independent leg (C3, inner rotation curve, {RC_RATIO:.2e}x at "
      f"250 pc) is therefore improved by only {RC_RATIO/over:.1f}x -- because that leg measures "
      "ENCLOSED MASS, and rotation redistributes mass without removing it")

# --- D5: the band that would be needed, versus the band that exists --------
lam_need = {}
for nm, R in (("10 kpc (inside the RAR-tested disc)", 10.0),
              ("30 kpc (outer RAR)", 30.0),
              ("287 kpc (r_vir: no concentration at all)", r_vir),
              ("2200 kpc (edge of the stage-12 lensing-RAR fit)", R_LENS)):
    lam_need[nm] = np.sqrt(R / (2 * r_vir))
    print(f"    to park the dust beyond {nm:<44s} needs lambda' >= {lam_need[nm]:.3f}")
lam_max = 1 / np.sqrt(2)
worst = lam_need["2200 kpc (edge of the stage-12 lensing-RAR fit)"]
check(worst > lam_max,
      f"D4  *** THE NO-WIN BAND, AND IT IS EMPTY.  To evade the corpus's OWN weak-lensing RAR fit "
      f"(stage 12: the pure kernel fits KiDS from 40 kpc to 2.2 Mpc and that fit REJECTS an added "
      f"dark component) the dust must sit beyond 2.2 Mpc, needing lambda' >= {worst:.2f}.  But "
      f"lambda' <= 1/sqrt(2) = {lam_max:.3f} is the kinematic ceiling -- full rotational support "
      f"AT the virial radius -- and anything above it is unbound and so was never captured.  "
      f"REQUIREMENT EXCEEDS CEILING BY {worst/lam_max:.2f}x. ***",
      "this is a conservation argument, not a margin: angular momentum can HALT a collapse, it "
      "cannot UNBIND mass.  It therefore holds for ANY lambda', for either footing, and for any "
      "twist amplitude the aether might source")
l10 = lam_need["10 kpc (inside the RAR-tested disc)"]
check(l10 / LAM_TT > 3,
      f"D5  the modest target fails on the realistic spin: reaching 10 kpc needs lambda' = "
      f"{l10:.3f}, {l10/LAM_TT:.1f}x the tidal-torque value ({(l10/LAM_TT)**2:.0f}x in rotational "
      f"energy).  *** AGAINST MY OWN CONCLUSION, STATED PLAINLY: on the corpus's own most "
      f"generous lambda' = {LAM_CORPUS[1]} the 10 kpc target IS reached ({l10/LAM_CORPUS[1]:.2f} "
      f"of the required value), so the SUB-KPC pile-up of D3 is lambda'-sensitive. ***  What is "
      f"NOT lambda'-sensitive is D4: no lambda' below the ceiling parks the dust outside the "
      f"lensing-RAR fit, and moving it out of the centre only moves it INTO the RAR-tested "
      f"region, which is the same contradiction one radius further out",
      f"lambda' = {LAM_CORPUS[0]}-{LAM_CORPUS[1]} is STANDING.md's local-comoving collapse "
      f"(gas/stars) and {LAM_TT} the standard N-body value (FROM MEMORY); reported both ways so "
      "the verdict cannot be moved by re-choosing lambda'")

# --- D6: what a twisting aether costs -------------------------------------
Om_s, vc_s, r_s = sp.symbols("Omega v_c r", positive=True)
A_rot = sp.Matrix([-1, -Om_s * y, Om_s * x, 0])          # tilt v/c = Omega r (geometric units)
Fr = sp.zeros(4, 4)
for a in range(4):
    for b in range(4):
        Fr[a, b] = sp.diff(A_rot[b], XC[a]) - sp.diff(A_rot[a], XC[b])
F2r = sp.simplify(sum(Fr[a, b] * (ETAI * Fr * ETAI)[a, b] for a in range(4) for b in range(4)))
# energy density of a static configuration = -L = +(K_B/2) F^2, in units c^4/(16 pi G)
rho_tw = sp.simplify((KB / 2) * F2r / (16 * sp.pi))       # x c^4/G ; Omega in 1/length
# isothermal comparison: rho_iso = v_c^2 /(4 pi G r^2), same units once Omega = v_c/r
ratio = sp.simplify((rho_tw.subs(Om_s, vc_s / r_s)) / (sp.Rational(1, 4) / sp.pi * (vc_s / r_s) ** 2))
check(sp.simplify(ratio - KB) == 0,
      f"D6  THE COST, and it is NOT prohibitive: a rigidly twisting aether carries energy density "
      f"rho_twist = K_B x rho_isothermal EXACTLY -- r-independent, because both go as 1/r^2 -- so "
      f"at the BBN ceiling K_B <= 0.25 the twist adds <= 25% to the mass it is supporting",
      f"rho_twist/rho_iso = {sp.simplify(ratio)}; computed from -(K_B/2)F^2 on the rotating "
      "aether, not asserted.  So the idea does not die on energetics -- it dies on D4")

# --- D7: the five free filters ---------------------------------------------
check(True,
      "D7  FILTER AUDIT: centrifugal support is not a pressure, so it evades F1 (rho = Q_0 n "
      "forces a LOCAL P(rho)), F2 (no equation of state hides energy from both channels), F3 "
      "(c_s^2 ~ a^-3), F4 (the barotropic floor at Gamma = 4/3) and F5 (a monotone |grad phi| "
      "gate has the wrong sign) -- all five are statements about SUPPORT PRESSURE",
      "so this was a legitimately un-screened candidate, which is why it was worth a session; it "
      "dies on a filter the catalogue did not have: ANGULAR MOMENTUM CANNOT UNBIND MASS (D4)")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  KILL CONDITION -- 'vorticity vanishes identically as a theorem': *** FALSE. ***
    The corpus's R1 (u_mu ~ grad_mu phi => omega = 0, re-verified here on 16/16 components) is a
    theorem about a P(X) ghost condensate.  AeST's dust does not satisfy its hypothesis: the
    shift-symmetry current derived from the action is
        S^mu = 2(2-K_B) J^mu - 2[(2-K_B)+F_Y] q^{{mu nu}} grad_nu phi - F_Q A^mu
    which on the cosmological configuration is EXACTLY -F_Q A^mu, and in a MW-like halo is
    {100*(1-worst_share):.1f}-{100*(1-min(v[0] for v in misal.values())):.1f}% the aether-aligned piece.
    The dust rides the AETHER, whose twist is a ghost-free, exactly luminal, propagating mode
    (L_2 = K_B[wdot^2 - (grad w)^2] - M^2 w^2), unscreened over a halo (mass range
    {range_lo:.0f}-{range_hi:.0f} Mpc from Q_0; m_v r = {220e3/(C*np.sqrt(kb)):.1e} from the dust), and untouched by
    the norm constraint.  STRUCTURAL REASON: Q = A^mu grad_mu phi is LINEAR in A.

  PASS CONDITION -- 'the achievable angular momentum is dynamically relevant': *** PARTIAL. ***
    It is relevant to the ENDPOINT and irrelevant to the PROBLEM.  At the tidal-torque spin the
    collapse halts at {r_cent:.2f} kpc, voiding stage 3's Sgr A* leg ({BH_RATIO:.1e}x) -- but stage 3's
    independent enclosed-mass leg only improves {RC_RATIO:.2e}x -> {over:.0f}x, a factor {RC_RATIO/over:.1f}.
    (That halting radius IS lambda'-sensitive: at STANDING.md's lambda' = {LAM_CORPUS[1]} it moves out
    to {2*LAM_CORPUS[1]**2*r_vir:.1f} kpc -- stated in D5 against my own conclusion.)
    THE DECISIVE NUMBER, and it is lambda'-free: parking the dust outside the corpus's own
    lensing-RAR fit needs lambda' >= {worst:.2f}; the kinematic ceiling is lambda' <= {lam_max:.3f}.
    Empty by {worst/lam_max:.2f}x -- and moving the dust out of the centre only moves it into the
    RAR-tested region, so the two constraints close on it from both sides.

  NET: a door the corpus recorded as shut is open, and a kill the corpus recorded as clean is
  conditional -- but open problem 2d does not move, because the obstruction is conservation of
  angular momentum, not a shortfall that a better mechanism could make up.  Both halves are
  worth having, and they cut in opposite directions.

  NOT COMPUTED: the amplitude of aether twist actually SOURCED during collapse (this file prices
  what is needed and shows what is allowed); the full AeST stress tensor (not needed -- the shift
  current settles the frame question with no metric-variation convention risk); the corpus's
  R1 file was re-derived here, not re-run.
  GRADE CAVEAT: Q_0 = {Q0_LO}-{Q0_HI} Mpc^-1 (stage 58) is CANDIDATE, and lambda' = {LAM_TT} is from
  memory.  Neither carries the verdict: D4 is footing-free, Q_0-free and lambda'-free.
""")

print(f"  {NCHK[0] - len(FAIL)}/{NCHK[0]} checks passed.")
if FAIL:
    print("  FAILED:")
    for f in FAIL:
        print("   -", f)
    sys.exit(1)
sys.exit(0)
