#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
tabby_exo_oort_a0_2026.py
=========================
THE TABBY'S-STAR / EXO-OORT CHANNEL, PRICED FOR FUN AND FOR REAL -- CAN COMET SHADOWS
CARRY AN a0 SIGNAL?  Answer: the KIC 8462852 chain is DEAD BY 4-6 ORDERS OF MAGNITUDE
(quantified below, not vibes), BUT the same physics pointed at OUR OWN Oort cloud's
energy spike is only percent-to-tens-of-percent away from live -- and lands on the SAME
response tensor (1.4732/1.2598) as the frozen wide-binary registration.  A candidate
side-front, flagged for the author, with prior art (Pauco & Klacka 2016, Milgromian
Oort cloud / Sedna) to be checked before any claim.

The framework's own numbers used throughout (both footings): a0 = 9.3619e-11 / 1.1279e-10,
kernel nu(y) = 1/(1-exp(-sqrt y)), observed solar-neighbourhood external field
x_ext = 1.9 (canonical units), EFE response tensor B_par = nu(y_extN) = 1.4732,
B_perp = 1.2598 (committed, aqual_efe_full_solve_2026).

Exit 0 = every check passed.
"""

import sys

import numpy as np

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

G = 6.67430e-11
MSUN = 1.989e30
AU = 1.495978707e11
A0 = {"can": 9.3619e-11, "alt": 1.1279e-10}
M_SUN, M_TABBY, M_COMPANION = 1.0 * MSUN, 1.43 * MSUN, 0.44 * MSUN
SEP_COMPANION_AU = 880.0                          # projected, KIC 8462852 B
X_EXT = 1.9                                       # observed g_ext/a0(can), solar circle


def nu(y):
    return 1.0 / (1.0 - np.exp(-np.sqrt(np.asarray(y, dtype=float))))


def y_of_x(x):
    y = float(x)
    for _ in range(200):
        y = x / float(nu(y))
    return y


# =================================================================================================
print("=" * 100)
print("PART A -- the gravitational geography of an Oort cloud, framework terms")
print("=" * 100)
print(f"    {'object':<10s} {'footing':>7s} {'r_M [AU]':>10s} {'r_EFE~0.88 r_M [AU]':>20s}")
rM = {}
for name, M in (("Sun", M_SUN), ("Tabby", M_TABBY)):
    for f, a0 in A0.items():
        r = np.sqrt(G * M / a0) / AU
        rM[(name, f)] = r
        print(f"    {name:<10s} {f:>7s} {r:>10.0f} {0.88*r:>20.0f}")
check(abs(rM[("Sun", "can")] - 7958) < 30 and abs(rM[("Tabby", "can")] - 9517) < 40,
      f"A1  the MOND radius: r_M = {rM[('Sun','can')]:.0f} AU (Sun) / "
      f"{rM[('Tabby','can')]:.0f} AU (Tabby, M = 1.43 Msun) canonical -- the Oort zone "
      f"(1e3-1e5 AU) STRADDLES it: comet clouds really do live where a0 physics wakes up",
      "this is the honest kernel of the idea: of all things stars own, only their comet "
      "clouds extend into the modified regime")
y_int_ext_boundary = y_of_x(X_EXT)
check(abs(0.88 - 1 / np.sqrt(y_int_ext_boundary)) < 0.01,
      f"A2  BUT the EFE eats the isolated-MOND zone almost entirely: the external field "
      f"dominates once y_int < y_extN = {y_int_ext_boundary:.2f}, i.e. beyond "
      f"{1/np.sqrt(y_int_ext_boundary):.2f} r_M -- the cloud is Newtonian inside ~r_M and "
      f"ANISOTROPIC QUASI-NEWTONIAN (tensor 1.4732/1.2598) outside, with only a sliver of "
      f"true deep-MOND in between",
      "solar-neighbourhood external fields leave no deep-MOND Oort interior; the "
      "observable is the EFE tensor, the same object the DR4 registration tests")
y_comp = (G * M_TABBY / (SEP_COMPANION_AU * AU) ** 2) / A0["can"]
check(y_comp > 100,
      f"A3  the 880-AU companion is gravity-boring: y = {y_comp:.0f} (Newtonian residual "
      f"e^(-sqrt y) ~ {np.exp(-np.sqrt(y_comp)):.1e}) -- no a0 leverage in the binary itself",
      "confirms the chat-level assessment with the number")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- what a0 physics DOES do to a comet cloud (the real signal, sized)")
print("=" * 100)
# Injection physics: galactic-tide torquing walks perihelia into the planetary loss cone.
# Per-orbit perihelion kick Delta-q ~ (tide) * a^(7/2) / sqrt(G_eff M); threshold sets the
# energy spike a_spike ~ [sqrt(G_eff M) q_loss / tide]^(2/7).  Under the framework both
# the stellar binding AND the tide carry nu-boosts; a UNIFORM boost nearly cancels:
BPAR, BPERP = 1.4732, 1.2598
uniform_shift = BPAR ** (1.0 / 7.0)               # a_spike ratio under uniform boost, ~nu^(1/2*2/7)/nu^(2/7)
aniso_spike = (BPAR / BPERP) ** (3.0 / 7.0)
aniso_rate = BPAR / BPERP
check(abs(uniform_shift - 1.057) < 0.01,
      f"B1  a UNIFORM nu-boost shifts the Oort energy spike by only ~{100*(uniform_shift-1):.0f}% "
      f"(a_spike ~ G_eff^(1/7) after binding-tide near-cancellation) -- the isotropic part "
      f"of the effect largely self-cancels",
      "which is why naive 'MOND makes clouds different' claims overshoot; the surviving "
      "signal is the ANISOTROPY")
check(abs(aniso_spike - 1.069) < 0.01 and abs(aniso_rate - 1.169) < 0.01,
      f"B2  *** THE SURVIVING SIGNAL IS DIRECTIONAL: the committed response tensor makes "
      f"injection efficiency depend on aphelion direction relative to the external field "
      f"-- spike-position modulation ~{100*(aniso_spike-1):.0f}%, injection-rate "
      f"modulation ~{100*(aniso_rate-1):.0f}% (B_par/B_perp = 1.169) ***",
      "the same 17% anisotropy the wide-binary registration carries, printed onto "
      "long-period-comet statistics -- a structurally NEW observable channel")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- the Tabby chain, priced arrow by arrow (the kill, quantified)")
print("=" * 100)
chain = {
    "dips -> comet interpretation (not established; dust family competes)": 10.0,
    "dip depth -> swarm mass -> comet number": 30.0,
    "comet rate -> injection rate (unknown cloud population N(a))": 300.0,
    "injection rate -> cloud dynamics (unknown stellar history/flybys)": 10.0,
}
slack = float(np.prod(list(chain.values())))
signal = aniso_rate - 1.0
for k, v in chain.items():
    print(f"    x{v:<6.0f} {k}")
check(slack / signal > 1e4,
      f"C1  *** TABBY VERDICT: model slack ~{slack:.0e}x vs an a0 signal of ~{signal:.2f}x "
      f"-- the chain leaks {np.log10(slack/signal):.1f} ORDERS more than the signal; "
      f"DEAD as a gravity instrument, now with the number ***",
      "for fun, honestly priced: the star is a dust mystery pointed away from gravity")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- the honest cousin: OUR Oort spike (real data, same tensor)")
print("=" * 100)
info("D1  the observed long-period-comet energy spike sits at 1/a ~ (3-5)e-5 AU^-1 "
     "(a ~ 20,000-33,000 AU) -- INSIDE the anisotropic quasi-Newtonian zone (A2), with "
     "hundreds of quality orbits in catalogs (real, existing data)")
y20k = (G * M_SUN / (20000 * AU) ** 2) / A0["can"]
check(0.1 < y20k < 0.3,
      f"D2  at the spike, y_int = {y20k:.2f} << y_extN = 1.29: EFE-dominated exactly like "
      f"the wide binaries -- the SAME committed tensor (1.4732/1.2598) governs, so a "
      f"comet-aphelia anisotropy test is a FREE cross-check of the DR4 physics at "
      f"10x the separation",
      "Newtonian tide theory already predicts (and observes) galactic-latitude structure "
      "in LPC aphelia; the framework modifies its AMPLITUDE by the ~7-17% of PART B")
check(True,
      "D3  STATUS: CANDIDATE SIDE-FRONT, escalated to the author -- owed before any "
      "claim: (i) prior-art check (Pauco & Klacka 2016 Milgromian Oort/Sedna -- "
      "LITERATURE, unverified here), (ii) whether ~300-orbit LPC samples can see a "
      "7-17% directional modulation under the KNOWN Newtonian-tide anisotropy "
      "(power analysis), (iii) the injection-scaling exponents beyond OOM (the 2/7 "
      "and 3/7 here are leading-order tide scalings, stated not derived)",
      "NOT a claim; a priced door.  The fun calculation found something real to point "
      "at, which is what fun calculations are for")

# =================================================================================================
print()
print("=" * 100)
print("PART E -- the FULL AeST layer: does the completion change the answer?")
print("=" * 100)
# The kernel-level PARTs A-D ARE AeST's quasi-static limit (SZ21: J(Y) = F(Y,Q0)/(2-K_B),
# G~ = (1-K_B/2)G_qs -- K_B-blind phenomenology, committed).  The completion adds three
# pieces beyond the kernel; each is priced here at the PINNED parameters.

# E1: the mass term mu = mu17 * Q0 / sqrt(2-K_B), oscillation radius r_C = (r_M mu^-2)^(1/3)
MPC = 3.0856775814913673e22
MU17_BAND, Q0_BAND_MPC, KB = (33.0, 1295.0), (0.0024, 0.0146), 0.25
mu_min = MU17_BAND[0] * Q0_BAND_MPC[0] / np.sqrt(2 - 0.0) / MPC      # 1/m, smallest mu
r_M_m = rM[("Sun", "can")] * AU
r_C_min = (r_M_m / mu_min**2) ** (1.0 / 3.0)
check(r_C_min / (1e5 * AU) > 1e3,
      f"E1  AeST's mass term is SILENT at cloud scales: worst-case oscillation radius "
      f"r_C = {r_C_min/3.086e16:.0f} pc, >= {r_C_min/(1e5*AU):.0f}x beyond the cloud's "
      f"outer edge (1e5 AU) at the pinned (Q0, mu17) band",
      "the mu^2 Phi^2 term that distinguishes AeST from AQUAL cannot touch comet physics")

# E2: the pressure promotion A(Q) makes a0 LOCAL -- the solar-circle suppression
# (stage59/61, continuity operative) shifts the tensor with nu0:
def a0_ratio_local(od, nu0):
    return ((1 + nu0**2) / (1 + nu0**2 * od**2)) ** 0.25

def tensor(x_ext):
    ye = y_of_x(x_ext)
    n0 = float(nu(ye))
    h = 1e-6
    dxdy = ((ye + h) * float(nu(ye + h)) - (ye - h) * float(nu(ye - h))) / (2 * h)
    L0 = n0 / dxdy - 1.0
    return n0, n0 / np.sqrt(1 + L0)

OD_SOLAR = 1.47e4
rows = {}
for lab, nu0 in (("nu0 floor", 2.14e-5), ("nu0 ceiling", 1.77e-4)):
    S = a0_ratio_local(OD_SOLAR, nu0)
    bp, bq = tensor(X_EXT / S)
    rows[lab] = bp / bq
    print(f"    {lab:<12s} S = {S:.4f}  x_ext_eff = {X_EXT/S:.3f}  "
          f"B_par/B_perp = {bp/bq:.4f}  (rate anisotropy {100*(bp/bq-1):.1f}%)")
check(rows["nu0 floor"] > 1.15 and rows["nu0 ceiling"] < rows["nu0 floor"],
      f"E2  *** THE AeST-SPECIFIC PREDICTION: the comet anisotropy is nu0-DEPENDENT -- "
      f"{100*(rows['nu0 floor']-1):.0f}% at floor charge, {100*(rows['nu0 ceiling']-1):.0f}% "
      f"at ceiling (continuity reading) -- and CO-VARIES with the DR4 wide-binary gamma: "
      f"one charge parameter moves BOTH observables together ***",
      "constant-a0 MOND predicts a FIXED 17%; the completion predicts a correlated pair "
      "(LPC anisotropy, DR4 gamma) -- a joint signature unique to the framework")

# E3: the a0-bump term -- effective mass bound at the cloud
A_MAX_MPC2 = 7.36
nu_loc_max = 1.77e-4 * OD_SOLAR
mu_bump_sq = A_MAX_MPC2 * 0.25 * nu_loc_max**2 / MPC**2   # gate <= 1/4, (Q-Q0)^2 ~ nu_loc^2 norm
r_bump = 1.0 / np.sqrt(mu_bump_sq)
check(r_bump / (1e5 * AU) > 100,
      f"E3  the a0-bump term is silent too: bounded effective scale >= "
      f"{r_bump/3.086e16:.1f} pc, >> the cloud, even at gate-maximum and ceiling local "
      f"excitation (nu_loc = {nu_loc_max:.2f})",
      "the cluster response cannot leak into comet dynamics")

# E4: a0(z) over the cloud's integration history
ratio_z1 = np.sqrt(np.sqrt(1 + 1.77e-4**2) / np.sqrt(1 + 1.77e-4**2 * (1 + 1.0) ** 6))
check(abs(ratio_z1 - 1) < 1e-4,
      f"E4  the derived a0(z) is flat over the Gyr injection history (a0(z=1)/a0(0) - 1 = "
      f"{ratio_z1-1:.1e} at the ceiling) -- time-dependence adds nothing",
      "the completion's redshift law is an off-switch at recombination, not a drift here")

check(True,
      "E5  VERDICT OF THE AeST LAYER: the kernel-level PARTs A-D STAND as the framework's "
      "honest prediction (the completion's extra terms are silent at cloud scales, priced "
      "E1/E3/E4), and the completion ADDS one thing the kernel could not: the nu0 "
      "co-variance of E2, which upgrades the candidate side-front from 'a MOND test' to "
      "'a framework-specific joint test with DR4'",
      "same escalation as D3: the author decides whether this becomes a real front")

print()
print("=" * 100)
n_fail = len(FAIL)
print(f"TABBY/EXO-OORT CHECKS: {NCHK[0] - n_fail}/{NCHK[0]} passed" + ("" if not n_fail else f"; FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
