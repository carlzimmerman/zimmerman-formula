#!/usr/bin/env python3
r"""B04 -- THE 3-Z^2 SEQUENCE TEST: the mechanistic hook's next member, pre-registered.

A01 (project_atomos/A01_me100.py) registered the m_e/100 pair
    m_e/100 = 5.1099895 keV  vs  m = 5.089 +- 0.097 keV (G212 joint 5.0886 +- 0.0969)
    and found the one framework-native mechanism that reproduces it:
        m = m_e/(3 Z^2) = 5.0830 keV   with   3 Z^2 = 100.531 = 100 - 0.53%
    (the null's own generation-count germ 3 times the kernel germ Z = sqrt(32 pi/3)
     squared, Z11's Z = 5.7888).  A01's verdict: REGISTERED CURIOSITY WITH A
    MECHANISTIC HOOK, NOT A CLAIM; the hook is a POST-HOC reading of a pre-existing
    denominator.

B04 CLOSES THE MECHANISM QUESTION THE ONLY WAY IT CAN BE CLOSED: does the SAME
3 Z^2-class structure appear at ANY OTHER SM mass scale?  The family is
pre-registered BEFORE the run (the expected count is stated first, the survival
scan runs after):

(1) THE FAMILY (pre-registered):  m_i = SM_mass / (3 Z^2)^n,  n in {0, 1, 2},
    for the five SM masses i in {e, mu, tau, p, n}  ->  15 members in total,
    compared at the 1% tolerance to the framework's keV-scale ENERGY LADDER:
        L0  the committed m band:  m = 5.09 keV (G212 peak 5.0886, 1-sigma band
            [4.9917, 5.1855]); canonical cosmic-noon ladder value 5.051 keV at
            z* = 2.4 (G163/G168) cited alongside
        L1  the cluster 334-K-class energy: T_dark(2-5 R500) = 334 +- 22 K =
            2.878e-5 keV = 0.0288 eV (Z07, the framework's measured dark-sector
            temperature in the cluster class)
        L2  the 9.17-K phase energy: k_B x 9.1744 K = 7.906e-4 eV = 7.907e-7 keV
            (G151's T_phase = m sigma^2/k_B at the triad sigma, 9.1744 K)
    THE EXPECTED FDR, STATED BEFORE THE FIT: the null's window math
    (gate/fdr.py _poisson_e_chance): for each ladder rung t,
        E_chance(t) = n_wide(t) x (2 tol)/0.2 = n_wide(t) x 0.1
    with n_wide(t) = # family members within +-10% of t.  L1 and L2 have ZERO
    family members within +-10% (the family's smallest member, m_e/100.531^2 =
    0.0506 keV, sits 1756x above L1).  L0 (5.09 keV) has exactly ONE member
    within +-10%: m_e/100.531 = 5.0830 keV -- the A01 hook itself.  Hence
        E_chance(L0) = 0.10, E_chance(L1) = 0, E_chance(L2) = 0
        EXPECTED COINCIDENCE COUNT IN THE PRE-REGISTERED FAMILY AT 1% TOLERANCE:
        <N> = 0.10.
    A single hit is therefore ~1-in-10 expectation (P(>=1) = 0.095); a SECOND
    member landing on ANY rung would be ~10x the null expectation.

(2) THE RUN: the full 15 x 3 comparison table at the 1% tolerance
    |m_i/(3 Z^2)^n - L_j|/L_j <= 0.01, plus z-scores vs the committed m band
    (G212: z = (value - 5.0886)/0.0969) for every family member.

(3) THE GATE: any survivor must clear the null's family-wise threshold
        E* = 0.05/(19 swept targets x 8 depths) = 3.29e-4 ~ 3.3e-4
    (THRESHOLD.py) with the step-1 FDR, AND carry a mechanism.  Pre-registered
    consequence: ANY survivor has itself in the +-10% band of its rung, so its
    E_chance >= 0.1 = 300x ABOVE E* -- the gate is IMPASSABLE for this family
    by construction; and the only mechanism on record (100 = 3 Z^2 - 0.53%) is
    the m_e reading itself, which generalizes ONLY if another member lands.
    Either way the test CLOSES: a surviving hook + no gate-clearing new member
    means the m_e/100 agreement is a SINGLE coincidence.

(4) VERDICTS: V1 the pre-registered family table; V2 the survivors (or none);
    V3 the honest statement: the 3-Z^2 sequence -- found or closed, the number
    that tells (expected 0.1, additional survivors found: the count).

REGISTERS (all committed, nothing tuned here):
    m_e  = 510.99895000 keV, m_mu = 105.6583755 MeV, m_p = 938.27208816 MeV,
    m_n  = 939.56542052 MeV (CODATA, targets/pdg_constants.py),
    m_tau = 1776.86 MeV (PDG)
    Z    = sqrt(32 pi/3) = 5.78865... (Z11 register 5.7888), Z^2 = 32 pi/3
    3 Z^2 = 100.531 (A01's denominator reading, 100 - 0.53%)
    G212: m = 5.0886 +- 0.0969 keV, band [4.9917, 5.1855]
    G163/G168: canonical cosmic-noon m(z*=2.4) = 5.051 keV, band [4.60, 5.05]
    Z07: T_dark(2-5 R500) = 334 +- 22 K = 2.88e-5 keV
    G151 (A02): T_phase = 9.1744 K -> k_B T = 7.906e-4 eV
    THRESHOLD.py: E* = 0.05/(19 x 8) = 3.29e-4 (family-wise)

Reused machinery (the null's, READ-ONLY): gate/fdr.py _poisson_e_chance window
math; targets/pdg_constants.py SM masses.  Nothing long runs here.
"""

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)          # project_atomos root -- committed modules only

OUT  = os.path.join(HERE, "B04_3z2_sequence.out")
JSON = os.path.join(HERE, "B04_results.json")

# ------------------------------------------------------------------ constants
# the five SM masses, keV (CODATA/PDG via targets/pdg_constants.py)
SM = {
    "m_e":   510.99895000,          # keV (0.51099895000 MeV)
    "m_mu":  105658.3755,           # keV (105.6583755 MeV)
    "m_tau": 1776860.0,             # keV (1776.86 MeV, PDG)
    "m_p":   938272.08816,          # keV (938.27208816 MeV)
    "m_n":   939565.42052,          # keV (939.56542052 MeV)
}

# the framework germ (the null's own, Z11 register Z = 5.7888)
Z2        = 32.0 * math.pi / 3.0    # 33.5103...
THREE_Z2  = 3.0 * Z2                # 100.5309649...  = 100.531 to 3 dp
Z_REG     = 5.7888                  # Z11 committed register

# the framework's keV-scale energy ladder (three committed rungs)
G212_PEAK = 5.0886                  # keV -- the m band peak (G212 joint posterior)
G212_SIG  = 0.0969                  # keV -- G212 1-sigma
G212_BAND = (G212_PEAK - G212_SIG, G212_PEAK + G212_SIG)   # [4.9917, 5.1855]
G163_CANON_24 = 5.051               # keV -- cosmic-noon ladder at z* = 2.4 (canonical)
K_PER_KEV = 8.617333262e-8          # keV per K (Boltzmann)
T_CLUSTER_K  = 334.0                # Z07: T_dark(2-5 R500) = 334 +- 22 K
T_PHASE_K    = 9.1744               # G151: T_phase = m sigma^2/k_B at triad sigma
LADDER = {                          # keV, with the registers
    "L0_m_band_5p09keV":      (G212_PEAK, 5.09,
                               "the committed m band (G212 peak 5.0886; band [4.9917, 5.1855]; canonical cosmic-noon 5.051 keV)"),
    "L1_cluster_334K":        (T_CLUSTER_K * K_PER_KEV, 334.0 * K_PER_KEV,
                               "the cluster 334-K-class energy = k_B x 334 K (Z07 measured T_dark(2-5 R500))"),
    "L2_phase_9p17K":         (T_PHASE_K * K_PER_KEV, 9.1744 * K_PER_KEV,
                               "the 9.17-K phase energy = k_B x 9.1744 K (G151 T_phase at the triad sigma)"),
}
TOL = 0.01                          # the pre-registered 1% tolerance
E_STAR = 0.05 / (19 * 8)            # null's family-wise threshold 3.29e-4 (THRESHOLD.py)

RES = []
def check(name, measured, ok, reading=""):
    RES.append({"name": name, "measured": measured, "pass": bool(ok),
                "reading": reading})
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if reading:
        print(f"         reading : {reading}")

def gauss_z(x, mu, sig):
    return (x - mu) / sig

def fmt(v):
    return f"{v:.6g}"

def sz(z, nd=2):
    """Signed fixed format -- plain f'{z:+.2f}' hits a C-printf overflow quirk
    (asterisks) for large magnitudes on this platform; do the sign manually."""
    s = f"{abs(z):.{nd}f}"
    return ("-" if z < 0 else "+") + s

# ====================================================================
# STEP 1 -- THE PRE-REGISTRATION (state the expected count BEFORE the fit)
# ====================================================================
print("=" * 96)
print("B04 -- THE 3-Z^2 SEQUENCE TEST (the mechanistic hook's next member, pre-registered)")
print("=" * 96)
print("""
STEP 1. THE PRE-REGISTRATION (declared BEFORE the survival scan):
  FAMILY : m_i / (3 Z^2)^n  with n in {0,1,2} for the 5 SM masses
           (3 Z^2 = 100.531 = 100 - 0.53%, the A01 denominator reading)
  -> 15 pre-registered members, compared at the 1% tolerance to the ladder.""")
print(f"  THREE_Z2 = 32 pi = {THREE_Z2:.6f}  (Z = {Z_REG}, Z11 register)")
print("  member generation table (keV):")
f = THREE_Z2
for name, m in SM.items():
    row = [m / f ** n for n in (0, 1, 2)]
    print(f"    {name:<6} n=0 {fmt(row[0]):>13} | n=1 {fmt(row[1]):>13} | "
          f"n=2 {fmt(row[2]):>13}")
print("\n  THE LADDER (keV):")
for k, (v, reg, note) in LADDER.items():
    print(f"    {k:<22} {fmt(v):>12}   ({note})")

# null's window math (gate/fdr.py _poisson_e_chance, read-only):
#   n_wide = # family members within +-10% of the rung;  E = n_wide x (2 tol)/0.2
family = [(name, n, SM[name] / f ** n) for name in SM for n in (0, 1, 2)]
print("\n  NULL'S WINDOW MATH (gate/fdr.py _poisson_e_chance), PRE-REGISTERED:")
exp_total = 0.0
wide_rows = []
for k, (v, reg, note) in LADDER.items():
    n_wide = sum(1 for _, _, x in family if 0.9 * v <= x <= 1.1 * v)
    e = n_wide * (2.0 * TOL) / 0.2          # the null's window fraction
    exp_total += e
    wide_rows.append((k, v, n_wide, e))
    memb = ", ".join(f"{nm}/100.531^{nn}" for nm, nn, x in family
                     if 0.9 * v <= x <= 1.1 * v) or "NONE"
    print(f"    {k:<22} n_wide(+-10%) = {n_wide}  ->  E_chance(1% window) = {e:.3f}"
          f"   [members in band: {memb}]")
print(f"  ** EXPECTED COINCIDENCE COUNT IN THE PRE-REGISTERED FAMILY AT 1% TOLERANCE:"
      f"  <N> = {exp_total:.2f} **")
print(f"  P(>=1 anywhere) = 1 - exp(-{exp_total:.2f}) = {1 - math.exp(-exp_total):.3f}."
      f"  A single hit is ~1-in-10 expectation; a SECOND survivor would be ~10x the null.")
print(f"  THE FAMILY-WISE GATE:  E* = 0.05/(19 targets x 8 depths) = {E_STAR:.4e}"
      f"  (THRESHOLD.py).  Pre-registered consequence: ANY survivor sits inside the "
      f"+-10% band of its own rung -> its E_chance >= 0.10 = {0.10 / E_STAR:.0f}x ABOVE "
      f"E* -- the gate is impassable for this family BY CONSTRUCTION.")

# the m-band z of every member (the committed band is G212)
def z_mband(x):
    return gauss_z(x, G212_PEAK, G212_SIG)

print("\n  The committed m band (G212) z-scores for every member:")
bands = [(nm, n, x, z_mband(x)) for nm, n, x in family]
for nm, n, x, z in bands:
    print(f"    {nm}/100.531^{n:<2} = {fmt(x):>12} keV   z(m band) = {sz(z)} sigma")

# ====================================================================
# STEP 2 -- THE RUN: the 15 x 3 comparison at the 1% tolerance
# ====================================================================
print("\n" + "=" * 96)
print("STEP 2. THE RUN -- the family table at the 1% tolerance (|v-L|/L <= 1%)")
print("=" * 96)
survivors = []
for k, (v, reg, note) in LADDER.items():
    for nm, n, x in family:
        ok = abs(x - v) / v <= TOL
        if ok:
            survivors.append((k, v, nm, n, x, abs(x - v) / v))
for k, v, nm, n, x, rel in survivors:
    print(f"  SURVIVOR @1%: {nm}/100.531^{n} = {fmt(x)} keV vs {k} = {fmt(v)} keV"
          f"  (delta = {rel * 100:.3f}%)")
if not survivors:
    print("  NO SURVIVORS at the 1% tolerance.")

print("\n  THE FULL 15 x 3 TABLE (closest ladder rung and its distance per member):")
table = []
for nm, n, x in family:
    best = min(LADDER.items(),
               key=lambda kv: abs(x - kv[1][0]) / kv[1][0])
    bk, (bv, _, _) = best
    rel = abs(x - bv) / bv
    table.append({"member": f"{nm}/100.531^{n}", "keV": x,
                  "closest_rung": bk, "rung_keV": bv,
                  "rel_distance": rel, "inside_1pct": rel <= TOL,
                  "z_vs_m_band": z_mband(x)})
    tag = "  <-- SURVIVOR (the A01 hook)" if (rel <= TOL and nm == "m_e" and n == 1) else \
          ("  <-- SURVIVOR" if rel <= TOL else "")
    print(f"    {nm}/100.531^{n:<2} = {fmt(x):>13} keV  closest rung {bk:<22} "
          f"({fmt(bv):>11})  rel {rel * 100:9.3f}%{tag}")
print(f"  -> {len(survivors)} survivor(s) at the 1% tolerance in the 15 x 3 = 45 "
      f"comparisons (expected <N> = {exp_total:.2f}).")

n_new = sum(1 for s in survivors if not (s[2] == "m_e" and s[3] == 1))
n_hook = len(survivors) - n_new

# ====================================================================
# STEP 3 -- THE GATE
# ====================================================================
print("\n" + "=" * 96)
print("STEP 3. THE GATE -- E* family-wise threshold + mechanism")
print("=" * 96)
gate_rows = []
for k, v, nm, n, x, rel in survivors:
    e = next(e for kk, _, _, e in wide_rows if kk == k)
    cleared = e < E_STAR
    gate_rows.append({"rung": k, "member": f"{nm}/100.531^{n}", "keV": x,
                      "E_chance": e, "E_star": E_STAR, "cleared_familywise": cleared})
    print(f"  survivor {nm}/100.531^{n} @ {k}:  E_chance = {e:.3f}  vs  E* = {E_STAR:.4e}"
          f"  ->  {'CLEARS' if cleared else 'FAILS (300x above)'}")
    if cleared:
        print("      mechanism requirement: the only mechanism on record is 100 = 3 Z^2 - 0.53%")
        print("      (the m_e reading itself); a new member would need its own framework germ.")

if not gate_rows:
    print("  no survivors -> gate vacuous, sequence closed.")
else:
    hook_clears = [g for g in gate_rows if g["member"] == "m_e/100.531^1"]
    other_clears = [g for g in gate_rows if g["member"] != "m_e/100.531^1"]
    print(f"  gate summary: {len(gate_rows)} survivor(s); hook(s) "
          f"{len(hook_clears)}/{len([s for s in survivors if s[2]=='m_e' and s[3]==1])}"
          f" present as the family DEFINITION, new-member survivor(s) {len(other_clears)}.")
    if hook_clears:
        print("  the hook's E_chance = 0.10 = 300 x E* = 3.29e-4  ->  FAILS the family-wise gate")
        print("  (consistent with A01: 3.3-3.75 surplus bits << the 10-bit gate).")
    if other_clears:
        print("  !! a NEW member clears the gate -- the sequence would be OPEN. (not the outcome)")

# ====================================================================
# STEP 4 -- VERDICTS
# ====================================================================
print("\n" + "=" * 96)
print("STEP 4. VERDICTS")
print("=" * 96)
hook_survived = any(s[2] == "m_e" and s[3] == 1 for s in survivors)
V1 = (f"THE PRE-REGISTERED FAMILY TABLE: the 5 SM masses x n = {{0,1,2}} = 15 members "
      f"(m_i/100.531^n) vs the 3-rung ladder at the 1% tolerance.  15 x 3 = 45 "
      f"comparisons, expected count <N> = 0.10 (the null's window math: only "
      f"m_e/100.531 = 5.0830 keV sits within +-10% of the 5.09-keV rung; L1 (334 K = "
      f"2.878e-5 keV) and L2 (9.17 K = 7.906e-7 keV) have ZERO members within "
      f"+-10%, the family's smallest member m_e/100.531^2 = 0.0506 keV being 1756x "
      f"above L1).  One survivor: m_e/100.531 vs L0 at 0.11% -- the A01 hook itself.  "
      f"No other member comes within 1% of ANY rung (next closest: m_mu/100.531^2 = "
      f"10.45 keV at 2.05x L0; everything else >= 18x).")
V2 = (f"THE SURVIVORS: exactly ONE member survives at the 1% tolerance -- "
      f"m_e/100.531 = {fmt(SM['m_e'] / f)} keV vs the committed m band rung "
      f"5.0886 keV, delta -0.11%, z = {sz(z_mband(SM['m_e'] / f), 3)} sigma vs G212 "
      f"(inside the 1-sigma band [4.992, 5.186]).  This is the PRE-EXISTING A01 hook "
      f"that DEFINED the family -- its survival is by construction, not evidence.  "
      f"ADDITIONAL survivors at other SM scales: {n_new}.  The same 3-Z^2-class "
      f"structure appears at NO other SM mass scale.")
V3 = (f"THE HONEST STATEMENT -- THE NUMBER THAT TELLS: the 3-Z^2 sequence is CLOSED.  "
      f"Pre-registered expectation <N> = 0.10 coincidences in the 15-member family at "
      f"the 1% tolerance; the run finds the expected single member (m_e/100.531 = "
      f"5.083 keV vs the 5.09-keV ladder, the A01 hook) and ZERO additional members: "
      f"m_mu/100.531-class (1050.8, 10.45 keV), m_p/100.531-class (9333, 92.84 keV), "
      f"m_n/100.531-class (9346, 92.97 keV), m_tau/100.531-class (17675, 175.8 keV), "
      f"m_e/100.531^2 (50.6 eV) all miss every ladder rung by >= 100% (most by >= 10x).  "
      f"The gate is closed twice over: (i) FDR - the hook's own chance rate is "
      f"E_chance = 0.10 = 300x ABOVE the family-wise E* = 3.3e-4 (THRESHOLD.py), and "
      f"pre-registered as impassable for the family (any survivor carries its own "
      f"+-10% presence); (ii) MECHANISM - the only framework reading on record "
      f"(100 = 3 Z^2 - 0.53%) is the m_e hook itself and generalizes to NO other "
      f"scale, so no next member exists to carry it.  FINAL REGISTER: m_e/100 is a "
      f"SINGLE COINCIDENCE (the A01 hook at z = +0.22 sigma against G212, with the "
      f"3-Z^2 hook at 0.53% post-hoc); the sequence test CLOSES the question - the "
      f"mechanistic hook has no next member.")
print(f"  V1 {V1}\n")
print(f"  V2 {V2}\n")
print(f"  V3 {V3}\n")

def hook_clears_any_gate():
    """True if the A01 hook itself clears the family-wise E* (it does not: 0.10 vs 3.3e-4)."""
    return any(g["cleared_familywise"] and g["member"] == "m_e/100.531^1"
               for g in gate_rows)


check("V1 THE PRE-REGISTERED FAMILY TABLE",
      f"V1: family 15 members x 3 rungs = 45 comparisons at 1%; expected <N> = "
      f"{exp_total:.2f}; survivors {len(survivors)} (the hook alone).  The 334-K and "
      f"9.17-K rungs see ZERO members within +-10%.",
      (len(survivors) == 1 and hook_survived),
      "the pre-registered expected count 0.10 is stated BEFORE the scan and the scan "
      "confirms it: the family is built around the m_e hook and produces nothing else")
check("V2 THE SURVIVORS",
      f"V2: survivors at 1% = {[(f'{s[2]}/100.531^{s[3]}', round(100 * s[5], 3)) for s in survivors]}; "
      f"new-member survivors = {n_new}; hook z vs m band = {z_mband(SM['m_e'] / f):+.3f}",
      n_new == 0,
      "the only 1% survivor is the A01 hook; no other SM mass lands on any ladder rung")
check("V3 THE HONEST STATEMENT (sequence closed or found?)",
      f"V3: expected {exp_total:.2f}, hook survivors {n_hook}, additional {n_new}; "
      f"hook E_chance {0.10:.2f} vs E* {E_STAR:.3e} -> fails 300x; no mechanism on any "
      f"other scale -> THE 3-Z^2 SEQUENCE IS CLOSED, m_e/100 is a SINGLE COINCIDENCE",
      n_new == 0 and (n_hook == 0 or not hook_clears_any_gate()),
      "the number that tells: 0 additional members found at 1% tolerance against "
      "expected 0.10; the gate is impassable by construction (0.10 >> 3.3e-4)")
check("C-GATE [family-wise E*]",
      f"gate: survivor E_chance = 0.10 vs E* = {E_STAR:.4e}; ratio {0.10 / E_STAR:.0f}x above",
      all(not g["cleared_familywise"] for g in gate_rows) if gate_rows else True,
      "family-wise E* = 3.29e-4 is 300x below the minimum possible family E_chance -> "
      "the pre-registered gate is impassable for the family as defined")
check("C-MECH [the next member's mechanism]",
      f"mechanism: 100 = 3 Z^2 - 0.53% is the m_e reading; new-member survivors = {n_new}",
      n_new == 0,
      "a mechanism can only exist where a member lands; no member lands -> no mechanism "
      "to invoke -> the hook is a single coincidence")

n_pass = sum(1 for r in RES if r["pass"])
print(f"\nB04 COMPLETE: {n_pass}/{len(RES)} checks PASS.")
print("THE 3-Z^2 SEQUENCE TEST: expected 0.10 coincidences at 1% tolerance in the "
      "15-member pre-registered family; the run finds the A01 hook alone (m_e/100.531 "
      "= 5.083 keV, -0.11% from the m band) and ZERO additional members.  "
      "E_chance(hook) = 0.10 = 300x the family-wise E* = 3.3e-4; no mechanism exists at "
      "any other scale.  THE SEQUENCE IS CLOSED: m_e/100 is a SINGLE COINCIDENCE.")

# ------------------------------------------------------------------ JSON
verdicts = {"V1": V1, "V2": V2, "V3": V3}
summary = {
 "lane": "B04_3z2_sequence",
 "question": "THE 3-Z^2 SEQUENCE TEST -- the mechanistic hook's next member, "
             "pre-registered: does the SAME 3 Z^2-class structure (100.531 = 100 - "
             "0.53%, A01) appear at ANY OTHER SM mass scale?  The family m_i/"
             "100.531^n (n = 0,1,2) vs the framework's keV-scale ladder (the 5.09-keV "
             "m band, the cluster 334-K energy 2.88e-5 keV, the 9.17-K phase energy "
             "7.91e-7 keV), the expected FDR stated BEFORE the fit, the survivors, "
             "and the honest verdict -- sequence member found or sequence closed.",
 "family": {
   "formula": "m_i / (3 Z^2)^n, n in {0,1,2}, i in {e,mu,tau,p,n} (15 members)",
   "3_Z2": THREE_Z2,
   "3_Z2_rounded": 100.531,
   "Z_register": Z_REG,
   "Z2": Z2,
   "members_keV": {f"{nm}/100.531^{n}": SM[nm] / f ** n
                   for nm in SM for n in (0, 1, 2)},
 },
 "ladder_keV": {k: v for k, (v, _, _) in LADDER.items()},
 "ladder_registers": {k: note for k, (_, _, note) in LADDER.items()},
 "pre_registration": {
   "tolerance": TOL,
   "window_math": "gate/fdr.py _poisson_e_chance: E_chance(t) = n_wide(t) x (2 tol)/0.2",
   "n_wide": {k: n for k, _, n, _ in wide_rows},
   "E_chance_per_rung": {k: e for k, _, _, e in wide_rows},
   "expected_coincidence_count_before_fit": round(exp_total, 4),
   "P_at_least_one": round(1 - math.exp(-exp_total), 4),
   "state": "EXPECTED <N> = 0.10 coincidences in the pre-registered family at the "
            "1% tolerance, stated BEFORE the run",
 },
 "gate": {
   "E_star_familywise": E_STAR,
   "E_star_rounded": 3.3e-4,
   "origin": "0.05/(19 swept targets x 8 depths), THRESHOLD.py",
   "impassable_by_construction": True,
   "explanation": "any survivor sits inside the +-10% band of its own rung -> its "
                  "E_chance >= 0.10 = 300x above E* = 3.29e-4",
 },
 "run": {
   "n_comparisons": len(family) * len(LADDER),
   "n_survivors_1pct": len(survivors),
   "survivors": [{"member": f"{s[2]}/100.531^{s[3]}", "keV": s[4],
                  "rung": s[0], "rung_keV": s[1],
                  "delta_pct": round(100 * s[5], 3)} for s in survivors],
   "hook_survived": hook_survived,
   "new_member_survivors": n_new,
   "full_table": table,
   "z_vs_m_band_G212": {f"{r['member']}": round(r['z_vs_m_band'], 3)
                        for r in table},
 },
 "verdicts": verdicts,
 "final_register": {
   "sequence_status": "CLOSED",
   "hook_status": "m_e/100 is a SINGLE COINCIDENCE (A01: pre-existing pair at "
                  "z = +0.22 sigma vs G212; 3 Z^2 hook at 0.53%, post-hoc, "
                  "3.3-3.75 bits < 10-bit gate)",
   "the_number_that_tells": "expected 0.10 coincidences at 1% tolerance; "
                            "additional members found: 0",
 },
}
summary["checks"] = RES
summary["n_pass"] = n_pass
summary["n_total"] = len(RES)

gates = {
 "a_pre_registered": "PASS -- the family (5 SM masses x n = 0,1,2 = 15 members), the "
    "tolerance (1%), the ladder (5.09 keV / 334 K / 9.17 K) and the expected count "
    "(<N> = 0.10 from the null's window math) are all stated BEFORE the survival "
    "scan runs, and the scan is a deterministic lookup over the declared family.",
 "b_fdr": "PASS -- the null's own window math (gate/fdr.py _poisson_e_chance) prices "
    "the family: E_chance = 0.10 for the 5.09-keV rung (the hook alone in the +-10% "
    "band), 0 for the 334-K and 9.17-K rungs, <N> = 0.10 total.  The ONE found "
    "coincidence (the hook) is the expected member, not a surplus; a second would "
    "have been ~10x the null.  Family-wise E* = 3.29e-4 is impassable by "
    "construction (any survivor's E_chance >= 0.10).",
 "c_accuracy": "PASS (bridge level as registered) -- the hook sits at 0.11% from the "
    "m band (inside its 1-sigma width +-1.9%); the sequence claim is structural "
    "(member present/absent at 1%), not kepler-grade.",
 "d_mechanism": "FAIL for any next member -- the only mechanism on record "
    "(100 = 3 Z^2 - 0.53%) is the m_e hook itself; m_mu, m_p, m_n, m_tau at "
    "100.531^n land 100%-2000% from every ladder rung, so no member exists to "
    "carry it.  The m_e/100 hook stands alone: SINGLE COINCIDENCE, sequence "
    "closed.",
 "e_framework_origin": "PASS -- every input is committed framework/SM: 3 and Z (null "
    "germs), the 5 SM masses (CODATA/PDG pdg_constants), the ladder rungs (G212, "
    "Z07, G151), the E* (THRESHOLD.py); nothing refit.",
 "f_falsifier": "REGISTERED -- (i) any measured SM-scale mass m_i and keV-ladder "
    "energy E with |m_i/100.531^n - E|/E <= 1% for n in {1,2}, i != e re-OPENS the "
    "sequence (a gate-clearing member needs E_chance < 3.3e-4 AND a mechanism); "
    "(ii) |m_meas - m_e/100| > 1% kills the pair (A01's standing falsifier); "
    "(iii) a measured m_e/100.531-class relic mass at any OTHER scale is the "
    "sequence's discovery channel.",
}
summary["gates"] = gates

json.dump(summary, open(JSON, "w"), indent=1, sort_keys=False)
print(f"\nJSON written: {JSON}")