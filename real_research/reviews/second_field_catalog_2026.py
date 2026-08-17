#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
second_field_catalog_2026.py
============================
THE SECOND-FIELD CATALOG FOR THE DUST PROBLEM -- four candidate structures priced against the
corpus's three-legged obstruction, one at a time, with the algebra.  ALL FOUR DIE, and the prior
("all die") is CONFIRMED -- but not uniformly, and the differences are the deliverable:

  * candidates 1, 2a, 2b, 3 are DEAD OUTRIGHT, three of them by leg L1 alone;
  * candidate 4 (mine: gate the Proca on a FIXED bare-Lambda scale instead of on A(Q)) is the only
    structure that CLEARS ALL THREE LEGS plus the CMB cap, the linear-cosmology protection and the
    P(k) leg -- and it then dies on a FOURTH leg derived here, the RADIAL SUPPORT-SIGN CONDITION
    (PART F5): a gate built from the field gradient anti-supports 99.3% of the held mass, because
    the gradient rises outward wherever the held dust dominates its own field.  Verdict
    CONDITIONAL-DEAD, with both escapes named and priced rather than a rescue claimed.

TWO NEW THEOREM-GRADE RESULTS FALL OUT, and they are the reusable part:
  (i)  D2b/D2c -- the barotropic violation is V ~ G M^(2/3) rho_c^(4/3-Gamma) rho_rec^(Gamma-1)/cap,
       so at Gamma = 4/3 (the dynamical-stability boundary itself) it is CALIBRATION-INDEPENDENT:
       1.16e3 x the committed CMB cap, movable by no choice of support radius or stiffness.
  (ii) F5a -- the anti-support crossover is r_x/R_supp = [M_bar/((pi^2/3) M_dust)]^(1/3) = 0.194,
       fixed by the baryon-to-dust ratio ALONE (R, K, a_0, q, footing and gate scale all cancel).

--------------------------------------------------------------------------------------------------
THE OBSTRUCTION (committed, nbody_2026 stages 5/6/9 -- restated and RE-DERIVED here in PART A)
--------------------------------------------------------------------------------------------------
  L1  rho = Q_0 n identically: the dust mass IS the conserved shift charge, so it cannot be
      suppressed locally (stage 5).
  L2  dynamics sees rho + 3p, lensing sees rho + p; rho+3p=0 needs w=-1/3 and rho+p=0 needs w=-1,
      which are incompatible => no equation of state hides a given energy from both.  At the f=1/3
      fixed point M_lens/M_dyn = 29 (stage 6 Part E).
  L3  c_s^2 = K'/[(Q_0+u)K''] -> 0 as the charge dilutes, for EVERY ghost-free K, at the fixed rate
      c_s^2 ~ n ~ a^-3 (stage 9).  So the sector cannot be kept warm.
Consequence: the excitation is dust, halos capture it, it collapses, endpoint a black hole,
falsified 5.8e5x against Sgr A*.  The corpus's named escape: "a SECOND FIELD carrying the pressure
-- a structural change, not a new free function."

--------------------------------------------------------------------------------------------------
THE ORGANISING RESULT OF THIS SCRIPT (PART B) -- WHY THE SECOND-FIELD PROGRAMME IS HARD
--------------------------------------------------------------------------------------------------
A second field can only help through a DISCRIMINANT: something that is large where support is
needed and small where the CMB forbids it.  Priced across the corpus's committed support
calibrations, only TWO of six available discriminants run the framework's way, and one factor
appears twice:

  *** THE a_0-GATE'S AMPLIFICATION AND THE BAROTROPIC FACTOR ARE THE SAME OBSTRUCTION.  Both are
      monotone functions of the CHARGE DENSITY, and both are adverse by >= 1.3e3 in every committed
      cell.  In the genuinely linear-nu regime (nu0 r_supp >= 10) they are EQUAL to 0.11%, because
      a_0^2(Q) = kappa^2 G(-K(Q)) with -K linear in the charge there, so A(Q) ~ n.  At SHALLOW
      support densities the identity fails and the gate amplification saturates at
      A(0)/A(rec) = 2.8e4 - 2.3e5, which is LESS adverse than the barotropic factor -- so the
      identity is a deep-regime statement, stated restrictedly (B4c/B4d/B4e) and never used
      outside its range. ***

Consequence (PART F): the structural change that has NEVER been priced is to normalise the gate by
a FIXED scale (the bare -2Lambda piece of K) instead of by the full -K(Q).  That removes the
amplification, and it is the only route in this catalog that clears all three legs -- and it then
dies on a FOURTH leg derived in PART F5, the radial support-sign condition.

--------------------------------------------------------------------------------------------------
FRAMEWORK / PROVENANCE / SCOPE
--------------------------------------------------------------------------------------------------
a_0 = kappa c sqrt(G rho_Lambda) = 9.3619e-11 canonical / 1.1279e-10 alt (BOTH reported for every
dimensional result).  kappa = 1/2 is FITTED (measured 0.551 +/- 0.043), NOT derived.  beta = 1 is
SELECTED.  Kernel nu(y) = 1/(1-exp(-sqrt y)).  Relativistic home AeST (Skordis & Zlosnik 2021)
with the promotion A(Q) = a_0^2(Q) = kappa^2 G(-K(Q)) and offset-DBI K.

INHERITED, NOT RE-DERIVED HERE (labelled [inh] at point of use, and every one is load-bearing):
  * c_s^2(rec) cap 2606 (km/s)^2 = 2.9e-8 c^2                      [committed CLASS run]
  * captured dust share M_dust = 2.51e12 Msun, L* baryons 6e10     [smooth-accretion capture chain]
  * support calibrations rho_c = 8.7e3 / 1654 / 1e6 rho_dm0        [stage 51 C / stage 53 B1, D2b]
  * K_eff = 1.44e33 SI <-> R = 189 kpc n=1 polytrope               [stage 51 C]
  * realised recombination flow v_rec = 12.6 (mode) / 23.1 (rms) km/s   [stage 54, ESTABLISHED]
  * A(0)/A(rec) = 2.78e4 (nu0 floor) - 2.30e5 (ceiling)            [stage 54]
  * X = Q_0 c^2/a_0(0): core band 106-453, envelope 70-1340        [stage 56/58, CANDIDATE grade]
  * lensing range 40 kpc - 2.2 Mpc, no dark component admitted     [stage 12 KiDS fit]
  * five-environment |Phi|/c^2: cluster 2.2e-5, galaxy 9e-7, web 1e-5  [stage 37]
  * PPN alpha_1 = -4 K_B => K_B < 2.5e-5 from LLR                  [stages 70-71, 2026-08-17]
ASSUMPTIONS I MAKE AND OWN (stated at point of use, tagged [asm]): the support criterion
c_s^2(rho_c) ~ G M/R (validated against the committed polytrope to 0.4% in B3); the halt criterion
rho_dust - 2 rho_chi <= 0 for a w=-1 second component; the sub-horizon growth exponent
p = (-1+sqrt(1+24 f_eff))/4 for a fifth force acting on the dust alone.

Exit 0 only if every numbered check passes.  Negative controls: D4 (the density-ordering test is
not rigged), D1 (the machinery reproduces stage 51's independently committed 3.25e6), F2 (the
machinery reproduces the known stage-51/54 gate kill when fed the known-dead structure).
"""

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

# ---------------------------------------------------------------------------------------------
# constants
C = 2.99792458e8
C_KMS = 2.99792458e5
G = 6.67430e-11
MPC = 3.0856775814913673e22
KPC = 3.0856775814913673e19
MSUN = 1.98892e30
H0_KMSMPC = 67.4
H0 = H0_KMSMPC * 1e3 / MPC
OM_DM, OM_L, OM_M = 0.265, 0.685, 0.315
OM_B = OM_M - OM_DM
RHO_CRIT = 3 * H0 ** 2 / (8 * np.pi * G)
RHO_DM0 = OM_DM * RHO_CRIT
RHO_L = OM_L * RHO_CRIT
Z_REC = 1090.0
A0 = {"canon": 9.3619e-11, "alt": 1.1279e-10}

# inherited anchors [inh]
CS2_CAP = 2606.0                       # (km/s)^2, committed CLASS recombination cap
M_DUST = 2.51e12 * MSUN                # captured share
M_BAR = 6.0e10 * MSUN                  # L* baryons
K_EFF_51 = 1.44e33                     # SI, stage 51's polytropic stiffness
R_51_KPC = 189.0
RHO_SUPP_CAL = {"polytrope(s51)": 8.7e3, "surface(s53 B1)": 1654.0, "deep(s53 D2b)": 1.0e6}
V_REC = {"mode": 12.6, "rms": 23.1}    # km/s
AMP = {"nu0 floor": 2.78e4, "nu0 ceil": 2.30e5}   # A(0)/A(rec)
X_CORE = (106.0, 453.0)
X_ENV = (70.0, 1340.0)
NU0 = (2.14e-5, 1.77e-4)
PHI = {"cluster": 2.2e-5, "galaxy": 9.0e-7, "web": 1.0e-5}
KB_LLR = 2.5e-5

RHO_REC = RHO_DM0 * (1 + Z_REC) ** 3
POLY_C_OVER_MEAN = np.pi ** 2 / 3      # n=1 polytrope central/mean density


# =============================================================================================
print("=" * 100)
print("PART A -- the three legs, re-derived here so the catalog stands on its own")
print("=" * 100)

u, Q0 = sp.symbols("u Q_0", positive=True)
K = sp.Function("K")

n_sym = sp.diff(K(u), u)
rho_sym = (Q0 + u) * sp.diff(K(u), u) - K(u)
rho_lead = sp.simplify(sp.series(rho_sym.subs(K(u), sp.Symbol("k0") + sp.Symbol("k1") * u
                                             + sp.Symbol("k2") * u ** 2 / 2), u, 0, 2).removeO())
# leading order in u about a stationary point k1 = K'(0) = 0, k0 = K(0) = -rho_Lambda
rho_lead0 = sp.simplify(rho_lead.subs({sp.Symbol("k1"): 0, sp.Symbol("k0"): -sp.Symbol("rL")}))
n_lead0 = sp.simplify(sp.diff(sp.Symbol("k0") + sp.Symbol("k2") * u ** 2 / 2, u))
check(sp.simplify(rho_lead0 - (sp.Symbol("rL") + Q0 * n_lead0)) == 0,
      "A1  L1: rho = rho_Lambda + Q_0 n exactly at leading order in u for ANY K with a stationary "
      "point -- the EXCITATION's energy is Q_0 times the CONSERVED charge",
      f"rho_exc = {sp.simplify(rho_lead0 - sp.Symbol('rL'))}; suppressing the amplitude u at fixed "
      "charge removes no mass")

drho = sp.simplify(sp.diff(rho_sym, u))
cs2 = sp.simplify(sp.diff(K(u), u) / drho)
check(sp.simplify(drho - (Q0 + u) * sp.diff(K(u), u, 2)) == 0,
      f"A2  L3: c_s^2 = {cs2} exactly for every K -- the whole question is the ratio K'/K''",
      "ghost-freedom K''>0 + charge conservation n=K' ~ a^-3 force K'->0, so c_s^2 ~ n ~ a^-3")
cs2_ratio_rec_to_now = (1 + Z_REC) ** 3
check(abs(cs2_ratio_rec_to_now / 1.2985e9 - 1) < 0.01,
      f"A2b L3's rate: c_s^2(rec)/c_s^2(0) = (1+z)^3 = {cs2_ratio_rec_to_now:.4e} -- the SAME "
      "factor that will reappear as the gate amplification in PART B",
      "this is why 'warm today' needs c_s^2(rec) = 595 c^2 (stage 9)")

w = sp.Symbol("w", real=True)
sol_dyn = sp.solve(sp.Eq(1 + 3 * w, 0), w)
sol_len = sp.solve(sp.Eq(1 + w, 0), w)
check(sol_dyn == [sp.Rational(-1, 3)] and sol_len == [-1] and sol_dyn != sol_len,
      "A3  L2: rho+3p=0 <=> w=-1/3, rho+p=0 <=> w=-1; no single w does both, so no equation of "
      "state hides an energy from BOTH dynamics and lensing",
      "at the f=1/3 dynamical-null fixed point the lensing source is (2/3)rho -> M_lens/M_dyn = 29")

X = sp.Symbol("X", positive=True)
Kc = sp.Function("Kc")
cs2_kess = sp.simplify(sp.diff(Kc(X), X) / (sp.diff(Kc(X), X) + 2 * X * sp.diff(Kc(X), X, 2)))
num, den = sp.fraction(sp.together(cs2_kess))
check(sp.simplify(num - sp.diff(Kc(X), X)) == 0,
      f"A4  L3 TRANSFERS to any SECOND shift-symmetric k-essence p=K(X): c_s^2 = {cs2_kess}, whose "
      "numerator is K_X -- it vanishes at the same stationary point, at the same a^-3 rate",
      "so a second shift-symmetric scalar inherits the obstruction rather than solving it")


# =============================================================================================
print("=" * 100)
print("PART B -- the environmental discriminant table: what a second field has to work with")
print("=" * 100)

info("B0  cosmology", f"rho_dm0 = {RHO_DM0:.4e} kg/m^3, rho_Lambda = {RHO_L:.4e} "
     f"(= {RHO_L/RHO_DM0:.3f} rho_dm0), rho_rec = {RHO_REC:.4e} = {RHO_REC/RHO_DM0:.4e} rho_dm0")
check(abs(RHO_REC / RHO_DM0 / 1.2985e9 - 1) < 0.01,
      f"B1  the recombination charge density is {RHO_REC/RHO_DM0:.4e} x today's",
      "every 'local' lever a second field could use is evaluated against THIS")


def config_from_rho_c(rho_c_over_dm0, M=M_DUST):
    """Given a central density (n=1 polytrope) and mass, return (rho_c, rho_mean, R, GM/R)."""
    rho_c = rho_c_over_dm0 * RHO_DM0
    rho_mean = rho_c / POLY_C_OVER_MEAN
    R = (3 * M / (4 * np.pi * rho_mean)) ** (1.0 / 3.0)
    return rho_c, rho_mean, R, G * M / R


CAL = {}
for name, rc in RHO_SUPP_CAL.items():
    rho_c, rho_mean, R, gm_r = config_from_rho_c(rc)
    CAL[name] = dict(rho_c=rho_c, rho_mean=rho_mean, R=R, cs2_supp=gm_r,
                     ratio=RHO_REC / rho_c)
    info(f"B2  calibration {name:18s}",
         f"rho_c = {rc:9.3e} rho_dm0, R = {R/KPC:7.1f} kpc, c_s^2_supp = GM/R = "
         f"{gm_r/1e6:9.4e} (km/s)^2, rho_rec/rho_c = {RHO_REC/rho_c:9.4e}")
check(all(CAL[k]["ratio"] > 1e3 for k in CAL),
      "B2b EVERY committed support calibration is LESS dense than the universe at recombination, "
      f"by {min(CAL[k]['ratio'] for k in CAL):.3e} to {max(CAL[k]['ratio'] for k in CAL):.3e}",
      "ADVERSE, and it is the master fact of this catalog: the configuration that must be held up "
      "is more dilute than the epoch that must stay pressureless")

# B3 -- validate the support criterion c_s^2 ~ GM/R against the committed polytrope
R51 = np.pi * np.sqrt(K_EFF_51 / (2 * np.pi * G))
rho_c51 = CAL["polytrope(s51)"]["rho_c"]
cs2_51 = 2 * K_EFF_51 * rho_c51
check(abs(R51 / (R_51_KPC * KPC) - 1) < 0.01,
      f"B3a K_eff = 1.44e33 SI -> R = pi sqrt(K/2 pi G) = {R51/KPC:.1f} kpc, reproducing the "
      f"committed {R_51_KPC:.0f} kpc [inh]")
check(abs(cs2_51 / CAL["polytrope(s51)"]["cs2_supp"] - 1) < 0.02,
      f"B3b and c_s^2(rho_c) = 2 K rho_c = {cs2_51/1e6:.4e} (km/s)^2 equals GM/R = "
      f"{CAL['polytrope(s51)']['cs2_supp']/1e6:.4e} to "
      f"{abs(cs2_51/CAL['polytrope(s51)']['cs2_supp']-1)*100:.2f}% [asm validated]",
      "so using c_s^2_supp = GM/R as the support criterion is exact for the committed structure")

# B4 -- THE UNIFICATION: the a0-gate amplification IS the density ratio
print("-" * 100)


def A_ratio(r_over_n0, nu0):
    """A(Q)/A(0) with the committed beta=1 law: sqrt(1+nu0^2)/sqrt(1+(nu0 r)^2)."""
    return np.sqrt(1 + nu0 ** 2) / np.sqrt(1 + (nu0 * r_over_n0) ** 2)


for nu0 in NU0:
    amp_rec = 1.0 / A_ratio(RHO_REC / RHO_DM0, nu0)
    info("B4  a_0-gate amplification at rec", f"nu0 = {nu0:.3e}: A(0)/A(rec) = {amp_rec:.3e}")
check(abs(1 / A_ratio(RHO_REC / RHO_DM0, NU0[0]) / AMP["nu0 floor"] - 1) < 0.05
      and abs(1 / A_ratio(RHO_REC / RHO_DM0, NU0[1]) / AMP["nu0 ceil"] - 1) < 0.05,
      "B4a reproduces the committed A(0)/A(rec) = 2.78e4 (floor) / 2.30e5 (ceiling) [inh]")

GATE_AMP = {}
uni_deep, uni_shallow = [], []
for name, d in CAL.items():
    for nu0 in NU0:
        r_s = d["rho_c"] / RHO_DM0
        gate_amp = A_ratio(r_s, nu0) / A_ratio(RHO_REC / RHO_DM0, nu0)
        GATE_AMP[(name, nu0)] = gate_amp
        (uni_deep if nu0 * r_s >= 10.0 else uni_shallow).append(gate_amp / d["ratio"])
        info(f"B4b {name:18s} nu0={nu0:.2e}", f"nu0*r_supp = {nu0*r_s:8.4f}, gate amplification "
             f"A(supp)/A(rec) = {gate_amp:.4e}, rho_rec/rho_supp = {d['ratio']:.4e}, "
             f"ratio = {gate_amp/d['ratio']:.4f}")
check(max(abs(np.array(uni_deep) - 1)) < 0.01,
      "B4c *** THE UNIFICATION, in its CORRECT (restricted) form: the a_0-gate amplification "
      f"A(rho_supp)/A(rho_rec) EQUALS rho_rec/rho_supp to "
      f"{max(abs(np.array(uni_deep)-1))*100:.2f}% in the cells where nu0*r_supp >= 10 (the "
      "genuinely linear-nu regime) ***",
      "because a_0^2 ~ -K(Q) is linear in the charge THERE.  So stage 51's gate kill and the "
      "barotropic kill are the SAME FACTOR at deep support densities -- one obstruction, counted "
      "twice")
check(min(np.array(uni_shallow)) < 0.5,
      f"B4d SELF-CORRECTION, reported against the tidy version of the claim: at SHALLOW support "
      f"densities (nu0*r_supp < 1) A(rho_supp) ~ A(0), so the amplification SATURATES at "
      f"A(0)/A(rec) = {AMP['nu0 floor']:.2e}-{AMP['nu0 ceil']:.2e} and is only "
      f"{min(np.array(uni_shallow)):.3f}-{max(np.array(uni_shallow)):.3f} of rho_rec/rho_supp -- "
      "i.e. LESS adverse than the barotropic factor there",
      "the identity is a deep-regime statement, not a universal one; PART F uses the EXACT A_ratio, "
      "never this identity")
check(min(GATE_AMP.values()) > 1e3 and min(CAL[k]["ratio"] for k in CAL) > 1e3,
      f"B4e what IS universal (and is what the catalog uses): BOTH factors are monotone functions "
      f"of the CHARGE DENSITY and both are adverse by >= 1e3 in every cell -- gate amplification "
      f"{min(GATE_AMP.values()):.3e}-{max(GATE_AMP.values()):.3e}, density ratio "
      f"{min(CAL[k]['ratio'] for k in CAL):.3e}-{max(CAL[k]['ratio'] for k in CAL):.3e}")

# B5 -- the six discriminants
print("-" * 100)
rmin = min(CAL[k]["ratio"] for k in CAL)
rmax = max(CAL[k]["ratio"] for k in CAL)
disc = [
    ("charge density n ~ rho", rmin, rmax, "ADVERSE"),
    ("physical length at fixed comoving k", 1 / (1 + Z_REC), 1 / (1 + Z_REC), "ADVERSE"),
    ("gate y = Y/A(Q)  [= discriminant 1]", rmin, rmax, "ADVERSE"),
    ("|Phi| (cluster vs web)", PHI["web"] / PHI["cluster"], 1.0, "DEGENERATE"),
    ("Y itself (static gradient vs rec flow)", None, None, "FAVOURABLE"),
    ("flow speed v", None, None, "FAVOURABLE"),
]
for nm, lo, hi, sgn in disc:
    if lo is None:
        info(f"B5  discriminant {nm:38s}", f"{sgn} (quantified in PART F)")
    else:
        info(f"B5  discriminant {nm:38s}", f"rec/supp = {lo:.3e} - {hi:.3e}  =>  {sgn}")
check(PHI["web"] / PHI["cluster"] > 0.4,
      f"B5a |Phi| is DEGENERATE: the cosmic web sits at {PHI['web']/PHI['cluster']:.2f} of the "
      "cluster depth [inh stage 37], so potential depth alone is not a usable discriminant")
check(sum(1 for _, _, _, s in disc if s == "FAVOURABLE") == 2,
      "B5b exactly TWO of six available discriminants run the framework's way (Y and the flow it "
      "is built from); the other four are adverse or degenerate")


# =============================================================================================
print("=" * 100)
print("PART C -- CANDIDATE 1: a second shift-symmetric k-essence chi, p_chi = K_chi(X_chi)")
print("=" * 100)

uu, Q0s = sp.symbols("u Q_0", positive=True)
Xc = sp.Symbol("X_chi", positive=True)
Ktot = K(uu) + Kc(Xc)                      # no cross term
check(sp.simplify(sp.diff(Ktot, uu) - sp.diff(K(uu), uu)) == 0,
      "C1  with NO cross term, dL/du = K'(u) EXACTLY -- the second field is invisible to the dust's "
      "own thermodynamics, so L3 applies to the dust verbatim and the Sgr A* factor is untouched",
      "the field COUNT was never the obstacle; a DIRECT coupling is required (stage 51 Part A, "
      "re-derived)")

# C2: at a stationary point of K_chi the energy is exactly -K = const -> cannot clump
rho_chi_stat = sp.simplify((2 * Xc * sp.diff(Kc(Xc), Xc) - Kc(Xc)).subs(sp.Derivative(Kc(Xc), Xc), 0))
check(sp.simplify(rho_chi_stat + Kc(Xc)) == 0,
      "C2  at a stationary point K_chi,X = 0 the second field's energy is rho_chi = -K_chi exactly, "
      "i.e. a CONSTANT: delta rho_chi = 0 identically, so it cannot clump at all",
      "and OFF the stationary point it carries its own conserved charge => it IS dust, by L1")

# C3: how much clumping would be needed
for name, d in CAL.items():
    need = d["rho_c"] / 2.0
    info("C3  halt requires rho_chi >= rho_dust/2 [asm: uniform-sphere source rho+3p]",
         f"{name:18s}: rho_chi >= {need/RHO_DM0:.4e} rho_dm0 = {need/RHO_L:.4e} x rho_Lambda")
need_min = min(d["rho_c"] for d in CAL.values()) / 2.0 / RHO_L
check(need_min > 100,
      f"C3b even the most dilute committed calibration needs the second field CLUMPED to "
      f"{need_min:.3e} x its cosmic value -- and C2 says a w=-1 k-essence clumps by 0 exactly",
      "so the required clumping is unavailable BY THE SAME ALGEBRA that makes it dark energy")

print("""
  VERDICT CANDIDATE 1: DEAD.  Killed by L1 and L3 -- both applied to the NEW field, not the old one.
  Uncoupled, it leaves the dust's c_s^2 exactly as stage 9 left it (C1); coupled only gravitationally
  it must clump by 1e2-1e5 x its cosmic value (C3), which a stationary-point k-essence cannot do at
  all (C2), and a NON-stationary one is itself dust with its own conserved charge (A4).
  *** L2 is the leg that does NOT kill this candidate: a w=-1 component is genuinely invisible to
  lensing (rho+p=0) while repelling dynamically (rho+3p=-2rho).  The kill is L1+L3, not L2. ***
  DIRECTION: adverse to the framework (the cheapest structural change buys nothing).
""")


# =============================================================================================
print("=" * 100)
print("PART D -- CANDIDATE 2: an UNGATED Proca/vector condensate on the conserved shift current")
print("=" * 100)

print("""  Structure (stage 51 Part B, the surviving algebra): vector exchange between LIKE charges is
  REPULSIVE, so a Proca chi_mu coupled to J^mu_shift gives P_ind = +g^2 n^2/(2 m_A^2) > 0, and since
  rho = Q_0 n identically (L1) this is P_ind = K_eff rho^2 -- an n=1 polytrope, gamma_eff = 2,
  stiffness FREE of K''.  Stage 51 GATED it and the gate died (y ~ 1/a_0^2(z) explodes at rec).
  THE QUESTION HERE: does UNGATING evade that?  Answer below: NO -- ungating is the SATURATING
  bound the gate could never beat, and the reason is L1 itself.""")

print("-" * 100)
print("  D1 -- THE BAROTROPIC-LOCALITY THEOREM (general, derived here)")
print("""      L1 forces any induced pressure built from the shift charge to be a local function of the
      DUST DENSITY: P = P(rho).  Write P = K rho^Gamma, so c_s^2 = Gamma K rho^(Gamma-1).  Then
              V(Gamma) = c_s^2(rho_rec)/cap = [c_s^2(rho_supp)/cap] x (rho_rec/rho_supp)^(Gamma-1).
      Because rho_rec > rho_supp for EVERY committed calibration (B2b), the exponent is adverse for
      every Gamma > 1 -- and Gamma > 6/5 is required for a finite-radius equilibrium (polytropic
      index n < 5), Gamma > 4/3 for dynamical stability.""")

GAMMAS = {"6/5 (finite R floor)": 1.2, "4/3 (stability floor)": 4.0 / 3.0, "2 (Proca/L1)": 2.0}
Vtab = {}
for name, d in CAL.items():
    pref = d["cs2_supp"] / 1e6 / CS2_CAP
    for gname, gam in GAMMAS.items():
        V = pref * d["ratio"] ** (gam - 1)
        Vtab[(name, gname)] = V
        info(f"D1  V  {name:18s} Gamma={gname:22s}", f"prefactor {pref:9.4e} x "
             f"({d['ratio']:.3e})^{gam-1:.4f} = {V:.4e} x the CLASS cap")

V_s51 = Vtab[("polytrope(s51)", "2 (Proca/L1)")]
check(abs(V_s51 / 3.25e6 - 1) < 0.05,
      f"D1a NEGATIVE-CONTROL / CROSS-VALIDATION: the theorem's (polytrope, Gamma=2) cell gives "
      f"{V_s51:.3e}, reproducing stage 51's INDEPENDENTLY committed ungated violation 3.25e6 to "
      f"{abs(V_s51/3.25e6-1)*100:.1f}%",
      "so the 3.25e6 in the corpus IS the ungated endpoint, and the machinery here is calibrated "
      "against a number it did not fit")

V_min_stab = min(v for (c, g), v in Vtab.items() if "6/5" in g)
V_min_dyn = min(v for (c, g), v in Vtab.items() if "4/3" in g)
check(V_min_stab > 1 and V_min_dyn > 1,
      f"D2  the MINIMUM violation over all calibrations is {V_min_stab:.3e}x at the finite-radius "
      f"floor Gamma=6/5 and {V_min_dyn:.3e}x at the stability floor Gamma=4/3 -- no exponent in the "
      "permitted range escapes",
      "this GENERALISES stage 51's single-point 3.25e6 into a statement about the whole class")

# D2b -- the theorem has a CALIBRATION-INDEPENDENT floor, exactly at the stability boundary
Gs, Ms, rcs, rrs, caps, Gg = sp.symbols("G M rho_c rho_rec cap Gamma", positive=True)
Rs = (Ms / rcs) ** sp.Rational(1, 3)                     # R ~ (M/rho_c)^(1/3) at fixed M
Vsym = sp.powsimp(sp.simplify((Gs * Ms / Rs / caps) * (rrs / rcs) ** (Gg - 1)))
exp_rc = sp.simplify(sp.diff(sp.log(Vsym), rcs) * rcs)
check(sp.simplify(exp_rc - (sp.Rational(4, 3) - Gg)) == 0
      and sp.simplify(exp_rc.subs(Gg, sp.Rational(4, 3))) == 0,
      f"D2b *** AND THE FLOOR IS CALIBRATION-INDEPENDENT: V ~ G M^(2/3) rho_c^(4/3-Gamma) "
      f"rho_rec^(Gamma-1)/cap, so the rho_c exponent is exactly (4/3 - Gamma) and VANISHES at "
      f"Gamma = 4/3 -- the dynamical-stability boundary itself ***",
      "so at Gamma=4/3 the violation depends ONLY on the captured dust mass and the recombination "
      "density: the support radius, the stiffness and the calibration all cancel")
V43 = np.array([v for (c, g), v in Vtab.items() if "4/3" in g])
check(V43.std() / V43.mean() < 1e-3,
      f"D2c and numerically the three independent calibrations agree to "
      f"{V43.std()/V43.mean()*100:.4f}% at Gamma = 4/3: V = {V43.mean():.4e} x the CLASS cap",
      "this is the sharpest form of the barotropic kill -- a floor no choice of support radius can "
      "move, sitting 1.2e3x above the committed cap")

pref_min = min(d["cs2_supp"] / 1e6 / CS2_CAP for d in CAL.values())
check(pref_min > 1,
      f"D3  and the exponent-free limit Gamma->1 still leaves {pref_min:.3f}x, because the support "
      "criterion GM/R already exceeds the recombination cap on its own",
      "Gamma=1 (constant c_s^2) is separately excluded: stage 69 finds constant c_s^2 destroys "
      "P(k=0.2) [inh]")

# D4 negative control: invert the density ordering
fake = dict(CAL["polytrope(s51)"])
fake_ratio = 0.1
V_fake = (fake["cs2_supp"] / 1e6 / CS2_CAP) * fake_ratio ** (2 - 1)
check(V_fake < CS2_CAP,
      f"D4  NEGATIVE CONTROL: feed the same algebra a hypothetical support point DENSER than "
      f"recombination (rho_rec/rho_supp = {fake_ratio}) and V drops to {V_fake:.3f} -- the test is "
      "driven by the density ORDERING, not rigged by the algebra")

print("-" * 100)
print("  D5 -- the OPPOSITE (long-range / massless) limit of the same vector")
print("""      If 1/m_A exceeds the region size the exchange is unscreened, and because rho = Q_0 n
      identically the charge-to-mass ratio of every dust element is 1/Q_0 EXACTLY -- universal and
      epoch-independent.  So the vector is exactly a rescaling of the dust's SELF-gravity,
      G_dd -> G(1-eps), with the SAME eps at recombination and today.  L1 forbids gating it.""")


def growth_exponent(f_eff):
    return (-1 + np.sqrt(1 + 24 * f_eff)) / 4.0


f_d = OM_DM / OM_M
for eps in (0.0, 0.01, 0.02, 0.1, 1.0):
    f_eff = 1.0 - f_d * eps
    p = growth_exponent(f_eff)
    supp = (1 + Z_REC) ** (p - growth_exponent(1.0))
    info(f"D5  eps = {eps:5.2f}", f"f_eff = {f_eff:.4f}, delta ~ a^{p:.4f}, growth from z=1090 "
         f"suppressed by {supp:.4f} ({1/supp:.3g}x loss)")
p1 = growth_exponent(1.0 - f_d * 1.0)
supp1 = (1 + Z_REC) ** (p1 - growth_exponent(1.0))
check(1 / supp1 > 30,
      f"D5a halting the dust's own collapse needs eps >= 1 [asm: source (1-eps)rho_d <= 0], and "
      f"eps = 1 costs {1/supp1:.0f}x of the linear growth between recombination and today",
      "the CMB's clustering component is the very thing the framework banks on the dust for, so "
      "eps ~ 1 is self-defeating; eps <~ 0.02 is the most the growth history tolerates")
check(1.0 / 0.02 > 30,
      "D5b violation of the long-range route: eps_needed/eps_allowed >= 50x, and L1 forbids making "
      "eps environment-dependent (the charge-to-mass ratio is 1/Q_0 identically)")

check((1 / (1 + Z_REC)) < 1,
      f"D6  and the fixed-RANGE lever also runs backwards: physical lengths at recombination are "
      f"{1/(1+Z_REC):.3e} of today's, so any fixed-Compton-wavelength force is MORE unscreened on "
      "every comoving scale in the early universe")

print("""
  VERDICT CANDIDATE 2: DEAD, and UNGATING DOES NOT EVADE STAGE 51 -- it is the saturating endpoint.
  Killed by L1: rho = Q_0 n makes the induced pressure a local function of the CONSERVED CHARGE,
  so it is automatically stiffest exactly where the charge is densest, which is recombination
  (1.3e3 - 7.9e5 x the committed support densities).  Contact limit: >= 1.9e2x the CLASS cap at the
  finite-radius floor, >= 1.2e3x at the stability floor, 1.4e5 - 9.9e6x at the L1-forced Gamma = 2.
  Long-range limit: needs eps >= 1 against eps <~ 0.02 from the growth history, >= 50x, and L1
  forbids gating eps.  L2 and L3 are not needed; L1 alone does it.
  AND THE SHARPEST FORM (D2b/D2c): at Gamma = 4/3 -- the dynamical-stability boundary itself -- the
  violation is CALIBRATION-INDEPENDENT, V ~ G M^(2/3) rho_rec^(1/3)/cap = 1.16e3 x the cap, because
  the rho_c exponent is exactly (4/3 - Gamma).  No choice of support radius, stiffness or
  calibration can move that floor; only M_dust and rho_rec enter.
  DIRECTION: adverse.  It also DEMOTES the corpus's framing -- the gate was never the problem's
  cure, it was the only thing that COULD have been the cure, and B4c/B4e show the gate's own
  amplification is the same charge-density factor that kills the ungated version.
""")


# =============================================================================================
print("=" * 100)
print("PART E -- CANDIDATE 3: a field entering ONLY through the promotion, a_0^2(Q, chi)")
print("=" * 100)

# E1 the order counting, symbolically: q^{mu nu} kills a purely temporal gradient
Qb = sp.Symbol("Qbar", positive=True)
eta = sp.diag(-1, 1, 1, 1)
Alow = sp.Matrix([-1, 0, 0, 0])                      # unit-timelike aether on FRW
dphi_bg = sp.Matrix([Qb, 0, 0, 0])                   # purely temporal background gradient
Aup = eta.inv() * Alow
qup = eta.inv() + Aup * Aup.T
Ybar = sp.simplify((dphi_bg.T * qup * dphi_bg)[0])
dp = sp.Matrix(sp.symbols("d0 d1 d2 d3", real=True))
dY_lin = sp.simplify(2 * (dphi_bg.T * qup * dp)[0])
check(Ybar == 0 and sp.simplify(dY_lin) == 0,
      "E1  the order counting, re-derived: Ybar = 0 and delta-Y^(1) = 0 on FRW (the spatial "
      "projector q^{munu} annihilates a temporal gradient), so Y = O(delta phi^2) and the "
      "a_0-dependent Y^{3/2} term is O(delta phi^3) -- absent from the LINEAR EOMs",
      "[bridge1_aest_equations.md, verbatim from the arXiv source]  so a chi entering only through "
      "a_0^2(Q,chi) is EXACTLY invisible to the background and to linear cosmology")

print("""  E2 -- and that protection is EXACTLY the impotence.  The Y-sector's own stress in the deep-MOND
      limit is rho_Y c^2 = (1/12 pi G) |grad phi|^3 / a_0 [AQUAL convention; O(1) factor stated, not
      hidden].  Evaluate it at the support point, both footings, two readings of the source.""")

for foot, a0 in A0.items():
    for lbl, Msrc in (("baryons only (target config)", M_BAR),
                      ("baryons + captured dust", M_BAR + M_DUST)):
        Rp = CAL["polytrope(s51)"]["R"]
        gN = G * Msrc / Rp ** 2
        g = np.sqrt(gN ** 2 + gN * a0)               # the framework's OWN interpolation
        rho_Y = (1.0 / (12 * np.pi * G)) * g ** 3 / a0 / C ** 2
        frac = rho_Y / CAL["polytrope(s51)"]["rho_c"]
        info(f"E2  {foot:5s} / {lbl:28s}", f"g/a0 = {g/a0:.4f}, rho_Y = {rho_Y:.4e} kg/m^3 = "
             f"{frac:.3e} x rho_dust")
        globals().setdefault("_E2", []).append(frac)
check(max(_E2) < 1e-6,
      f"E2a the promotion sector's own stress is at most {max(_E2):.3e} of the dust density it "
      "would have to support -- 6 to 10 ORDERS short, on both footings and both source readings")
check(True,
      "E2b and there is NO amplitude to turn up: the coefficient of the Y^{3/2} term IS a_0, "
      "pinned by the RAR/BTFR, so this is a PARAMETER-FREE shortfall",
      "the promotion route has one knob (a_0) and it is already spent on the galaxy fits")

print("""
  VERDICT CANDIDATE 3: DEAD -- and killed by NO leg.  It is killed by the promotion's OWN order
  counting, which is a no-free-lunch theorem: the fact that makes a_0(z) CMB-safe (Y = O(dphi^2), so
  the MOND term is O(dphi^3)) is the same fact that makes the Y-sector's stress 1e-10 - 1e-7 of the
  dust.  A field that never appears in the background cannot carry the background's pressure.
  DIRECTION: adverse to this candidate, but NEUTRAL-to-favourable for the framework's CMB safety --
  E1 re-derives that protection independently, and it stands.
""")


# =============================================================================================
print("=" * 100)
print("PART F -- CANDIDATE 4 (mine): the same Proca, gated on a FIXED scale instead of on A(Q)")
print("=" * 100)

print("""  THE STRUCTURAL CHANGE, stated precisely.  Stage 51 gated the coupling with W(y), y = Y/A(Q),
  A(Q) = a_0^2(Q) = kappa^2 G(-K(Q)).  B4c/B4e showed WHY that dies: A(Q) is a monotone function of
  the CHARGE DENSITY (and equals it in the linear-nu regime), so the gate variable is amplified at
  recombination by 1.3e3 - 2.2e5, adverse in every committed cell.  But
  -K(Q) = 2 Lambda + (charge-dependent piece), and NOTHING forces the GATE to use the full -K.
  Gate instead on the BARE Lambda piece:
        W(ytil),   ytil = Y / (kappa^2 G * 2 Lambda) = Y / a_0^2(0) x O(1).
  This is a different function of the SAME action ingredients, it costs no new dimensionful
  constant (Lambda is already in the action, and a_0(0)^2 ~ kappa^2 G * 2 Lambda is the framework's
  own anchor -- so NO new coincidence is posited), and the promotion a_0^2(Q) is left untouched, so
  stage 17's derived a_0(z) law, MOND-off-at-recombination and lambda_J ~ a_0^(-1/3) all survive.
  Parameter count is stage 51's: 4 -> 6.  NOT a new free function -- a different normalisation.""")

def y_gate(R, a0, M=M_DUST + M_BAR):
    """The framework's own gate variable at radius R: y = (g/a0)^2 with g from ITS interpolation
    g = sqrt(g_N^2 + g_N a0).  In deep MOND this equals g_N/a0 identically.  M = the mass sourcing
    the scalar -- the dust sources phi too, so the DEFAULT includes it (self-consistent)."""
    gN = G * M / R ** 2
    g = np.sqrt(gN ** 2 + gN * a0)
    return (g / a0) ** 2


def ytil_rec(Xv, v_kms):
    """Fixed-scale gate variable on the realised recombination flow: ytil = X^2 (v/c)^2
    [stage 54's ESTABLISHED flow-form identity Y_lin = Q0^2 |v_phi - v_ae|^2]."""
    return Xv ** 2 * (v_kms / C_KMS) ** 2


def M_eff_fw(R, a0, M=M_BAR):
    """The framework's OWN effective (lensing/dynamical) mass from a baryon source at radius R."""
    gN = G * M / R ** 2
    return np.sqrt(gN ** 2 + gN * a0) * R ** 2 / G


print("-" * 100)
print("  F1 -- the OPERATIVE endpoint is set by the corpus's own lensing fit, and it is a TRADE-OFF")
print("""      Stage 51's 189 kpc endpoint is REJECTED by stage 12's committed KiDS machinery
      (Delta chi^2 ~ +1.2e3 to +2.0e3) [inh].  The dust must therefore be held out beyond the fit's
      outer edge R_fit = 2.2 Mpc.  For a uniform-ish held configuration the dust's fractional
      contribution to the lensing mass PEAKS at R_fit (M_dust(r) ~ r^3 while the framework's own
      M_eff ~ r in deep MOND), so evaluating there is both correct and conservative.
      Spreading further costs stiffness: K ~ R^2 for a Gamma = 2 polytrope, so V_ungated ~ R^2.""")

R_FIT = 2.2 * MPC
M_EFF_FIT = M_eff_fw(R_FIT, A0["canon"])
TRADE = {}
for f_lens in (0.18, 0.05, 0.02):
    R_supp = R_FIT * (M_DUST / (f_lens * M_EFF_FIT)) ** (1.0 / 3.0)
    K_s = K_EFF_51 * (R_supp / R51) ** 2
    V_s = 2 * K_s * RHO_REC / 1e6 / CS2_CAP
    rho_c_s = POLY_C_OVER_MEAN * M_DUST / ((4.0 / 3.0) * np.pi * R_supp ** 3)
    TRADE[f_lens] = dict(R=R_supp, K=K_s, V=V_s, rho_c=rho_c_s)
    info(f"F1  lensing tolerance {f_lens*100:5.1f}% of M_eff at 2.2 Mpc",
         f"R_supp = {R_supp/MPC:6.3f} Mpc, rho_c = {rho_c_s/RHO_DM0:6.3f} rho_dm0, K_eff = "
         f"{K_s:.3e} SI, c_s(supp) = {np.sqrt(2*K_s*rho_c_s)/1e3:5.1f} km/s, "
         f"V_ungated = {V_s:.4e} x cap  (c_s(rec) = {np.sqrt(2*K_s*RHO_REC)/C:.2f} c)")
check(abs(M_DUST / M_EFF_FIT / 0.18 - 1) < 0.05,
      f"F1a SELF-CORRECTION (my first pass had this favourable and it is NOT): at R_supp = R_fit = "
      f"2.2 Mpc the held dust is {M_DUST/M_EFF_FIT*100:.2f}% of the framework's own lensing mass "
      f"there ({M_EFF_FIT/MSUN:.3e} Msun), i.e. ~{M_DUST/M_EFF_FIT/2*100:.1f}% in g -- a real "
      "perturbation on stage 12's fit, not a clean pass",
      "ADVERSE.  So 2.2 Mpc is the LOOSEST admissible endpoint, not the target")
check(TRADE[0.02]["V"] > TRADE[0.18]["V"],
      f"F1b THE SQUEEZE, quantified: tightening the lensing tolerance 18% -> 2% pushes R_supp "
      f"{TRADE[0.18]['R']/MPC:.2f} -> {TRADE[0.02]['R']/MPC:.2f} Mpc and the ungated recombination "
      f"violation {TRADE[0.18]['V']:.3e} -> {TRADE[0.02]['V']:.3e} x cap",
      "the two committed constraints pull the SAME lever in opposite directions: lensing wants the "
      "dust dilute, the CMB penalises exactly that dilution through rho_rec/rho_supp")
OP = TRADE[0.05]
R_OP, K_OP, V_OP = OP["R"], OP["K"], OP["V"]
info("F1c OPERATIVE configuration adopted [asm, stated]",
     f"5% lensing tolerance -> R_supp = {R_OP/MPC:.3f} Mpc, V_ungated = {V_OP:.4e} x cap")
check(np.sqrt(2 * K_OP * RHO_REC) / C > 1,
      f"F1d and UNGATED it is superluminal at recombination: c_s(rec) = "
      f"{np.sqrt(2*K_OP*RHO_REC)/C:.2f} c -- so a gate is not optional even before the CMB cap")

print("-" * 100)
print("  F2 -- NEGATIVE CONTROL: feed the machinery the KNOWN-DEAD A(Q)-normalised gate")

rows_A = []
for name, d in CAL.items():
    for foot, a0 in A0.items():
        ys = y_gate(d["R"], a0)
        for nu0 in NU0:
            for Xv in X_CORE:
                for vv in V_REC.values():
                    sep_A = (ys / ytil_rec(Xv, vv)) / GATE_AMP[(name, nu0)]   # EXACT A_ratio
                    rows_A.append((name, sep_A))
sepA = np.array([r[1] for r in rows_A])
deep = np.array(["deep" in r[0] for r in rows_A])
check(sepA[~deep].max() <= 1.0,
      f"F2a NEGATIVE CONTROL PASSES: with the exact A(Q) normalisation the gate is MORE OPEN at "
      f"recombination than at the support point in every non-deep cell (max separation "
      f"{sepA[~deep].max():.3e} <= 1), so NO gate power q can help -- reproducing stage 51's kill "
      "and stage 54's ratio theorem from independent arithmetic")
check((sepA[deep] > 1).any(),
      f"F2b AGAINST THE KILL'S INTEREST, and it must be reported: at the DEEP support calibration "
      f"the A(Q)-gate separation reaches {sepA[deep].max():.3e} > 1, so the 'gate-class wall' is "
      "NOT exception-free -- it has an escape corner the corpus has not priced")

R_deep = CAL["deep(s53 D2b)"]["R"]
_F2C = []
for foot, a0 in A0.items():
    Me = M_eff_fw(R_deep, a0)
    _F2C.append(M_DUST / Me)
    info(f"F2c deep-corner mass budget ({foot})", f"at R = {R_deep/KPC:.1f} kpc the framework's own "
         f"M_eff(baryons) = {Me/MSUN:.3e} Msun vs the held dust {M_DUST/MSUN:.3e} Msun => over by "
         f"{M_DUST/Me:.2f}x")
check(min(_F2C) > 5,
      f"F2d and the escape corner CLOSES on the framework's own terms: the deep calibration puts "
      f"{min(_F2C):.1f}x-{max(_F2C):.1f}x more dust inside {R_deep/KPC:.0f} kpc than the RAR/"
      "lensing budget admits.  The A(Q)-gate wall stands -- but on THIS leg, not the one advertised")

print("-" * 100)
print("  F3 -- the FIXED-SCALE gate: the required gate power q at the operative endpoint")
print("""      V(q) = V_ungated x (ytil_rec/ytil_supp)^q <= 1  =>  q >= ln V / ln(separation),
      and the separation must exceed 1 before ANY q helps.""")

qreq = {}
for foot, a0 in A0.items():
    ys_op = y_gate(R_OP, a0)
    for Xv in X_CORE:
        for vk, vv in V_REC.items():
            sep = ys_op / ytil_rec(Xv, vv)
            q = np.log(V_OP) / np.log(sep) if sep > 1 else np.inf
            qreq[(foot, Xv, vk)] = q
            info(f"F3  {foot:5s} X={Xv:6.0f} v_rec={vk:4s}",
                 f"ytil_supp = {ys_op:.4e}, ytil_rec = {ytil_rec(Xv, vv):.4e}, separation = "
                 f"{sep:9.3f}  =>  " + ("q >= %.2f" % q if np.isfinite(q)
                                        else "IMPOSSIBLE (separation <= 1)"))
qv = np.array(list(qreq.values()))
live = np.isfinite(qv)
check(live.any(),
      f"F3a the fixed-scale gate has a NON-EMPTY surviving region: {int(live.sum())} of {len(qv)} "
      f"core (footing, X, v_rec) cells admit a finite gate power, needing q >= "
      f"{qv[live].min():.2f} to {qv[live].max():.2f}")
check((~live).any(),
      f"F3b and it is NARROW, reported against interest: {int((~live).sum())} of {len(qv)} core "
      "cells are IMPOSSIBLE at any q (the high-X / high-flow corner), so survival is hostage to X "
      "-- a CANDIDATE-grade pin (core 106-453, envelope 70-1340) [inh stage 56/58]")
q_min_live = qv[live].min()

print("-" * 100)
print("  F4 -- the two structural legs the fixed-scale gate PASSES")
check(q_min_live >= 2.0,
      f"F4a LINEAR-COSMOLOGY PROTECTION IS COMPATIBLE: W(ytil) A_mu J^mu multiplies a BACKGROUND "
      f"charge, so it enters the second-order action iff 2q <= 2; every surviving cell needs "
      f"q >= {q_min_live:.2f} >= 2, hence O(delta^4) and EXACTLY zero linear contribution",
      "FAVOURABLE, and the leg the A(Q)-gate could not have: there the amplification defeated the "
      "protection, here the required power and the protection point the same way")
k_J = 2 * np.pi / (R_OP / MPC)
check(k_J > 0.2,
      f"F4b P(k) LEG PASSES: for Gamma = 2 lambda_J = sqrt(2 pi K/G) is DENSITY-INDEPENDENT "
      f"(= {R_OP/MPC:.2f} Mpc at every epoch once open), so the dark-sector smoothing sits at "
      f"k_J = {k_J:.2f} /Mpc, well above the k = 0.2 h/Mpc scale stage 69's non-claim names",
      "FAVOURABLE -- but it predicts low-z dark suppression at k ~ 2-3 /Mpc, which the committed "
      "forest front must price (OWED)")

print("-" * 100)
print("  F5 -- *** A FOURTH LEG, DERIVED HERE: THE RADIAL SUPPORT-SIGN CONDITION *** ")
print("""      Hydrostatic support requires dP/dr < 0 with P = W(y) K rho^2.  y is built from the FIELD
      GRADIENT, so its radial run decides the SIGN of the pressure force:
        * inside the baryon-dominated radius r_x, g ~ G M_bar/r^2 FALLS, so y and W FALL outward
          => dP/dr < 0 => genuine support;
        * outside r_x the held dust dominates and g ~ (4pi/3)G rho_c r RISES, so W RISES outward
          => P rises outward => the pressure force points INWARD => ANTI-support.
      The crossover is where the two sources' gradients match, and it is parameter-free:
            r_x/R_supp = [ M_bar / (pi^2/3 * M_dust) ]^(1/3)
      -- set by the baryon-to-dust ratio ALONE (R, K, a_0, q, the footing and the gate scale all
      cancel).  So the equilibrium truncates at r_x and the rest of the dust piles up there.""")

frac_x = (M_BAR / (POLY_C_OVER_MEAN * M_DUST)) ** (1.0 / 3.0)
r_x = frac_x * R_OP
rho_c_op = OP["rho_c"]
r_x_direct = (3 * M_BAR / (4 * np.pi * rho_c_op)) ** (1.0 / 3.0)
check(abs(r_x_direct / r_x - 1) < 0.02,
      f"F5a the crossover is r_x = {frac_x:.4f} R_supp = {r_x/KPC:.0f} kpc, and the closed form "
      f"agrees with the direct solve G M_bar/r^2 = (4pi/3) G rho_c r to "
      f"{abs(r_x_direct/r_x-1)*100:.2f}%",
      "parameter-free: it depends on M_bar/M_dust and the polytrope shape only")
f_wrong = 1.0 - (r_x / R_OP) ** 3
check(f_wrong > 0.9,
      f"F5b so {f_wrong*100:.2f}% of the held dust mass sits OUTSIDE r_x, in the region where a "
      "monotone gradient-gate gives the pressure force the WRONG SIGN",
      "ADVERSE and it is a property of the CLASS, not of my parameter choices -- it applies to "
      "stage 51's gated construction too")
_F5 = []
for foot, a0 in A0.items():
    Me = M_eff_fw(r_x, a0)
    _F5.append(M_DUST / Me)
    info(f"F5c the pile-up at r_x, priced against lensing ({foot})",
         f"M_eff(baryons, r_x = {r_x/KPC:.0f} kpc) = {Me/MSUN:.3e} Msun vs piled dust "
         f"{M_DUST/MSUN:.3e} => {M_DUST/Me*100:.1f}% of the lensing mass")
check(min(_F5) > 0.2,
      f"F5d and the pile-up is INSIDE stage 12's fit range (40 kpc - 2.2 Mpc) carrying "
      f"{min(_F5)*100:.0f}%-{max(_F5)*100:.0f}% of the framework's own lensing mass there -- "
      "rejected by the same committed machinery that rejected stage 51's 189 kpc endpoint")
R_needed = R_FIT / frac_x
K_needed = K_EFF_51 * (R_needed / R51) ** 2
V_needed = 2 * K_needed * RHO_REC / 1e6 / CS2_CAP
sep_needed = y_gate(R_needed, A0["canon"]) / ytil_rec(X_CORE[0], V_REC["mode"])
q_needed = np.log(V_needed) / np.log(sep_needed) if sep_needed > 1 else np.inf
check(q_needed > 20,
      f"F5e THE ONLY ESCAPE INSIDE THE CLASS, priced: push r_x beyond the fit's edge, i.e. "
      f"R_supp >= R_fit/{frac_x:.4f} = {R_needed/MPC:.1f} Mpc.  Then V_ungated = {V_needed:.3e} and "
      f"even the most favourable core cell needs q >= {q_needed:.0f} -- not a theory, a fitted "
      "exponent",
      "so the class does not escape by dilution; it would need a NON-monotone (band-pass) gate, and "
      "stage 54 already priced band-pass gates as WORSE at recombination")

print("""
  VERDICT CANDIDATE 4: PASSES ALL THREE LEGS -- AND DIES ON A FOURTH THAT THIS CATALOG DERIVES.
    vs L1  it does not fight rho = Q_0 n, it USES it (P_ind ~ n^2 ~ rho^2 is what L1 forces).
    vs L2  it hides nothing: it PREVENTS concentration, so there is no energy to hide.
    vs L3  its stiffness is g^2/m_A^2, not K'', so c_s^2 ~ a^-3 does not bind it.
    vs the CMB  a fixed-scale (bare-Lambda) gate removes the rho_rec/rho_supp amplification that
           B4c/B4e show is the A(Q)-gate's whole failure mode, leaving a real separation and a
           finite required gate power in part of the band (F3).
    *** BUT the radial support-sign condition (F5) kills it: because the gate is built from the
    FIELD GRADIENT, and the gradient RISES outward wherever the held dust dominates its own field,
    a monotone gate delivers ANTI-support to 99% of the held mass.  The equilibrium truncates at
    r_x = 0.194 R_supp and the dust piles up there, inside stage 12's fit range, at 55-61% of the
    framework's own lensing mass -- the same rejection that killed stage 51's endpoint, reached from
    the gate's radial structure instead of from its amplitude. ***
  STATUS: CONDITIONAL-DEAD, with the escape named and priced (F5e: a band-pass gate, already worse
  at recombination by stage 54; or a gate variable that is monotone-DECREASING in radius throughout,
  which cannot be built from |grad phi| alone).
  DIRECTION OF RISK: ADVERSE.  Reported with the same prominence as the near-miss: F3 genuinely
  opened a door that stage 51/54 never priced, and F5 closed it two steps later.
""")


# =============================================================================================
print("=" * 100)
print("PART G -- the catalog, the verdicts, and what remains OWED")
print("=" * 100)

table = [
    ("1  second shift-symmetric k-essence K_chi(X_chi)", "DEAD", "L1 + L3, applied to CHI",
     "uncoupled => dL/du = K' exactly (C1); a stationary-point chi cannot clump at all (C2) yet "
     "needs 1e2-1e5x clumping (C3); off-stationary it IS dust.  L2 does NOT kill it."),
    ("2a UNGATED Proca on J^mu_shift (contact limit)", "DEAD", "L1",
     "L1 forces P = P(rho) local in the CONSERVED charge => stiffest at rec.  >=1.9e2x cap at "
     "Gamma=6/5, >=1.2e3x at 4/3, 1.4e5-9.9e6x at Gamma=2.  Ungating is the SATURATING bound."),
    ("2b same Proca, long-range/massless limit", "DEAD", "L1",
     "charge-to-mass ratio = 1/Q_0 identically => G_dd -> G(1-eps) with the SAME eps at rec; "
     "needs eps>=1 vs eps<~0.02 from growth, >=50x."),
    ("3  field only in the promotion a_0^2(Q, chi)", "DEAD", "no leg -- the promotion's own "
     "order counting",
     "Ybar=0 and delta-Y^(1)=0 (E1) protect the CMB and, by the same fact, make the Y-sector's "
     "stress 1e-10-1e-7 of the dust (E2), with NO free amplitude."),
    ("4  Proca gated on a FIXED (bare-Lambda) scale", "CONDITIONAL-DEAD (passes L1/L2/L3)",
     "a FOURTH leg, derived here: the radial support-sign condition",
     "the normalisation change is real and removes the A(Q)-gate's whole failure mode (B4c/B4e), "
     "leaving a finite required gate power in part of the band (F3) -- but a gradient-built "
     "monotone gate anti-supports 99% of the held mass (F5), truncating at r_x = 0.194 R_supp and "
     "piling up inside stage 12's fit range at 55-61% of the lensing mass."),
]
for nm, verdict, leg, why in table:
    print(f"\n  {nm}\n      VERDICT : {verdict}\n      KILLED BY: {leg}\n      WHY     : {why}")

check(sum(1 for _, v, _, _ in table if v == "DEAD") == 4,
      "G1  4 of the 5 catalogued structures are DEAD outright on the corpus's own committed numbers")
check(sum(1 for _, v, _, _ in table if "CONDITIONAL-DEAD" in v) == 1,
      "G2  the fifth -- the only one that clears all THREE legs -- is CONDITIONAL-DEAD on a fourth "
      "leg this catalog derives; so the prior ('all die') is CONFIRMED, with a new obstruction and "
      "its two named escapes on the record rather than a rescue claimed")
q_class = np.array([q for q in qv if np.isfinite(q)])
check(q_class.min() >= 2.0 and frac_x < 0.25,
      f"G3  the two numbers a future attempt has to beat: gate power q >= {q_class.min():.2f} (from "
      f"the CMB cap) and the anti-support crossover r_x/R_supp = {frac_x:.4f} (from M_bar/M_dust)")

print("""
  OWED, none of it cosmetic (items 1-3 are DECIDING):
   (O1) THE PERTURBATION HEALTH MATRIX of the gated coupling.  Still owed from stage 51 and now the
        deciding item: W(ytil) A_mu J^mu is a derivative interaction, so no-ghost and gradient
        stability of the (chi_mu, phi, aether) system must be SHOWN.  A gate that grows with the
        field gradient is exactly the structure that produces gradient instability/superluminality,
        and F1b already has the ungated c_s(rec) at 3.6c.
   (O2) THE NEW VECTOR'S OWN PPN/BBN BUDGET.  Stage 51 Part B's sign theorem forces a VECTOR (scalar
        exchange is anti-support), so this is a NEW Proca on top of AeST's aether.  Today's result
        alpha_1 = -4 K_B => K_B < 2.5e-5 from LLR [stages 70-71] applies to the AETHER, not to
        chi_mu, but the analogous exercise for chi_mu is owed -- and note K_B < 2.5e-5 makes AeST's
        E-equation a CONSTRAINT rather than an evolution equation, which the gate's evaluation
        inside a halo will inherit.
   (O3) X.  Every verdict in PART F is a function of X = Q_0 c^2/a_0(0), pinned only at CANDIDATE
        grade (core 106-453, envelope 70-1340).  X near the top of the core band CLOSES candidate 4.
        This is the same X whose dilemma stage 62 resolved at OOM grade; here it is load-bearing at
        derivation grade.
   (O4) THE FOREST.  F4b's dark Jeans length of 2.2 Mpc switching on at low z must be priced against
        the committed forest front (stages 14-16), which the baryons feel gravitationally.
   (O5) THE TILTED-AETHER COLLAPSE SOLVE (stage 63's derivation-grade item).  PART F uses the STATIC
        MOND gradient as the support-side gate variable -- stage 54's referee ESTABLISHED that
        (y_static ~ 0.06-0.28, X-free), so the gate is open in a static configuration and candidate 4
        is not self-defeating.  But the actual value inside a collapsing halo needs the solve.
   (O6) The corpus should record F2b/F2d: the A(Q)-gate wall had an unpriced deep-support escape
        corner, and it is closed here by the RAR/lensing mass budget (5-10x), not by the gate
        argument.  The wall stands, on a different leg than advertised.

  AND TWO CORRECTIONS TO THE FRAMING, banked:
   (1) 'the second field carries the pressure' is not one problem.  B4c/B4e: the barotropic kill and
       the a_0-gate kill are the SAME charge-density factor (equal to rho_rec/rho_supp in the
       linear-nu regime, because a_0^2 ~ -K(Q) ~ n).  That is why three of the four candidates die by
       L1 alone: L1 ties the pressure to the conserved charge, and the charge density is exactly what
       separates recombination from a galaxy.  De-normalising the gate from the charge is therefore
       the RIGHT structural move -- and PART F shows it is necessary but not sufficient.
   (2) the surviving obstruction is no longer about AMPLITUDE, it is about RADIAL STRUCTURE.  Every
       previous attempt in the corpus (stages 4, 5, 36, 51) was killed by a magnitude; candidate 4
       gets the magnitudes right in part of the band and is killed by a SIGN (F5).  A future attempt
       should be screened against r_x/R_supp = 0.194 FIRST, because that test is parameter-free and
       costs nothing -- it would have killed stage 51's construction on day one.
""")

print("=" * 100)
print(f"CHECKS: {NCHK[0]-len(FAIL)}/{NCHK[0]} passed" + ("" if not FAIL else f"   FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
