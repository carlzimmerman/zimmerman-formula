#!/usr/bin/env python3
r"""mi_structural_theorems_v3_kernel_mixing_2026.py -- TWO DEFECTS IN A PUBLISHED PAPER, found by the
orphan-closure hunt and verified here from the kernels themselves rather than on subagent authority.

PROVENANCE, stated honestly. The orphan-closure triage fan-out reported "zero conflicts survived
refutation". That headline was WRONG, for two reasons in MY OWN harness, both recorded here because the
same mistake would hide the same class of finding again:
  (i)  the vote aggregation read `refuters >= votes.length / 2`, so with two lenses a 1-1 SPLIT was
       filed as "killed". One refuter had returned refuted=FALSE ("I could not kill it") at MEDIUM.
  (ii) more fundamentally, the refute schema had no way to say "the ATTRIBUTION is wrong but the
       DEFECT is real". Several refuters killed the pairing while explicitly CONFIRMING the underlying
       defect ("The residue is factually correct and I verified every number"). Those got filed as dead.
Everything below is re-derived from scratch here; nothing rests on an unrefuted subagent claim.

THE TARGET. opus_48_extended_research/papers/MI_STRUCTURAL_THEOREMS.md, Version 2026-07-30 (v3),
published (Zenodo DOIs in-file: 21264727 / 21284144 / 21702746). Its Theorem 2 / Corollary 2.1-2.2
compare the framework's two closures. Two defects, both in the alpha=2 migration being only half done.

  S1  THE KERNELS ON THE FREQUENCY AXIS, exactly. With z = -w^2, w = omega*c/a0:
        alpha=1:  K_1 = sqrt(1 - 1/(4w^2)) + i/(2w)  for w > 1/2   -> COMPLEX, Im K_1 = 1/(2w)
        alpha=2:  K_2 = w/sqrt(w^2 - 1)               for w > 1     -> REAL, Im K_2 = 0 EXACTLY
      Both derived symbolically, then checked numerically.
  S2  DEFECT 1 -- A MIXED-KERNEL ROW at :207-210. The published parenthesis reads
      "$K=0.99999997+2.5\times10^{-4}i$ against the required $K(1)=1/\sqrt2=0.7071$ at $a=a_0$".
      The COMPUTED value is alpha=1's K_1 (recovered here to 9 digits, at w=2000 i.e. v=149.9 km/s);
      the REQUIRED value is alpha=2's K_2(1)=1/sqrt2. One parenthesis, two different kernels.
  S3  DEFECT 2 -- AN INTERNAL CONTRADICTION, :194 vs :207. The paper's own Theorem 2 proof states that
      for alpha=2 the cut is the COMPACT interval -1 < z < 0. Twelve lines later :207 asserts the
      argument -(omega c/a0)^2 "lies on the cut". Every real system has -(omega c/a0)^2 << -1, i.e.
      OUTSIDE that interval. Quantified for real systems, both footings.
  S4  WHAT DEFECT 2 COSTS: the published 8.5-sigma pulsar exclusion at :220-224 targets the "universal
      drift a0/2c", which S1 shows is an alpha=1-EXCLUSIVE quantity (omega*Im K_1 = a0/2c exactly,
      w-independent). Under the paper's own current alpha=2 kernel the drift is EXACTLY ZERO, so there
      is nothing for a pulsar to exclude. The exclusion is sound about alpha=1 and vacuous about alpha=2.
  S5  Scope: what still stands, and the defect CLASS this belongs to.

BOTH a0 FOOTINGS throughout. Exit 0 = ran and every internal check held. No hard-coded verdicts.
"""
from __future__ import annotations
import math
import sys

import numpy as np
import sympy as sp

ok: list[tuple[bool, str]] = []


def check(cond: bool, msg: str) -> bool:
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t: str) -> None:
    print("\n" + "=" * 100)
    print(f"  {t}")
    print("=" * 100)


C = 2.99792458e8
MPC = 3.0856775814913673e22
H0 = 67.66e3 / MPC
OMEGA_L = 0.6889
Z_FACTOR = math.sqrt(32.0 * math.pi / 3.0)
YR = 3.155693e7  # Julian-ish year in seconds
KPC = 3.0856775814913673e19

FOOTINGS = {"canon": C * H0 * math.sqrt(OMEGA_L) / Z_FACTOR, "alt": C * H0 / Z_FACTOR}
# the paper's own quoted numbers imply the canonical 9.36e-11 footing; verified in S4
A0_PAPER = 9.36e-11


def K1(z: complex) -> complex:
    z = complex(z)
    return 0j if z == 0 else (np.sqrt(1.0 + 4.0 * z) - 1.0) / (2.0 * np.sqrt(z))


def K2(z: complex) -> complex:
    z = complex(z)
    return np.sqrt(z) / np.sqrt(1.0 + z)   # factored, to avoid branch-picking on sqrt(z/(1+z))


banner("S1  THE TWO KERNELS ON THE FREQUENCY AXIS z = -w^2, EXACTLY")

w = sp.Symbol("w", positive=True)
# alpha=1, w > 1/2: sqrt(1+4z) = sqrt(1-4w^2) = i*u with u = sqrt(4w^2-1) POSITIVE. Introducing u as a
# positive SYMBOL -- rather than sqrt(4w^2-1), whose sign sympy cannot settle for symbolic w, which made
# re/im return atan2 branches and the first version of these two checks FAIL -- lets re/im be exact.
u = sp.Symbol("u", positive=True)          # u^2 = 4w^2 - 1, real and > 0 exactly when w > 1/2
K1_sym = sp.simplify((sp.I * u - 1) / (2 * sp.I * w))
K1_re, K1_im = sp.re(K1_sym), sp.im(K1_sym)
print(f"  alpha=1 (w > 1/2):  K_1 = {K1_sym}  ->  Re = {K1_re}  Im = {K1_im}   [u = sqrt(4w^2-1)]")
check(sp.simplify(K1_im - 1 / (2 * w)) == 0,
      "Im K_1 = 1/(2w) EXACTLY (u taken as the positive root) -- alpha=1 IS complex on this axis")
check(sp.simplify(K1_re - u / (2 * w)) == 0 and
      sp.simplify((u / (2 * w)).subs(u, sp.sqrt(4 * w**2 - 1)) - sp.sqrt(1 - 1 / (4 * w**2))) == 0,
      "Re K_1 = u/(2w), which on substituting u back is exactly sqrt(1 - 1/(4w^2))")

# alpha=2, w > 1 : sqrt(z)=i w, sqrt(1+z)=i sqrt(w^2-1)  ->  K_2 = w/sqrt(w^2-1), REAL
# same treatment: for w > 1, sqrt(1+z) = sqrt(1-w^2) = i*vv with vv = sqrt(w^2-1) POSITIVE, so both
# square roots are imaginary and the i's CANCEL. Using vv as a positive symbol makes that exact.
vv = sp.Symbol("v", positive=True)         # vv^2 = w^2 - 1, real and > 0 exactly when w > 1
K2_sym = sp.simplify((sp.I * w) / (sp.I * vv))
print(f"  alpha=2 (w > 1  ):  K_2 = {K2_sym}   [v = sqrt(w^2-1)] -- the i's cancel, so no imaginary part")
check(sp.simplify(sp.im(K2_sym)) == 0 and sp.simplify(K2_sym - w / vv) == 0,
      "Im K_2 = 0 EXACTLY for w > 1 -- alpha=2 is REAL on the frequency axis beyond w=1, because its "
      "cut is the COMPACT interval -1 < z < 0 and z = -w^2 is past it")
check(sp.simplify((w / vv).subs(vv, sp.sqrt(w**2 - 1)) - w / sp.sqrt(w**2 - 1)) == 0,
      "and substituting v back gives K_2 = w/sqrt(w^2-1), the real modulus that tends to 1 as w -> oo")
# Im K_2 = 0 holds for EVERY w > 1, but |K_2| -> 1 is a LARGE-w asymptote ONLY: at w = 2, |K_2| = 2/sqrt3
# = 1.1547. The first version of this loop asserted both at once and so FAILED at w = 2 -- the assertion
# was wrong there, not the physics. The two claims are now checked separately, at their true scopes.
for wv in (2.0, 1e3, 1e6):
    k2 = K2(-(wv**2))
    check(abs(k2.imag) < 1e-25,
          f"numeric: at w={wv:.0e}, K_2 = {k2.real:.9f}{k2.imag:+.1e}i -- purely REAL, no imaginary part")
check(abs(abs(K2(-4.0)) - 2.0 / math.sqrt(3.0)) < 1e-12,
      f"|K_2| is NOT ~1 at small w: at w=2 it is {abs(K2(-4.0)):.6f} = 2/sqrt3 exactly")
for wv in (1e3, 1e6):
    check(abs(abs(K2(-(wv**2))) - 1.0) < 1e-5,
          f"but |K_2| -> 1 asymptotically: at w={wv:.0e}, |K_2| = {abs(K2(-(wv**2))):.9f}")


banner("S2  DEFECT 1 -- THE MIXED-KERNEL ROW AT :207-210")

PUB_COMPLEX = complex(0.99999997, 2.5e-4)
PUB_REQUIRED = 1.0 / math.sqrt(2.0)
print(f'  published: "K = {PUB_COMPLEX.real:.8f}+{PUB_COMPLEX.imag:.1e}i against the required '
      f'K(1) = 1/sqrt2 = {PUB_REQUIRED:.4f} at a = a0"\n')

# invert Im K_1 = 1/(2w) on the published imaginary part
w_pub = 1.0 / (2.0 * PUB_COMPLEX.imag)
k1_at = K1(-(w_pub**2))
v_implied = C / w_pub  # at a = a0 (x = 1), Theorem 8 gives w/x = c/v so w = c/v
print(f"  inverting Im K_1 = 1/(2w) on the published 2.5e-4  ->  w = {w_pub:.1f}")
print(f"  K_1(-w^2) at that w = {k1_at.real:.9f} + {k1_at.imag:.9f}i")
print(f"  implied speed (w = c/v at a = a0)  v = {v_implied/1e3:.1f} km/s")
check(abs(k1_at.real - PUB_COMPLEX.real) < 5e-9 and abs(k1_at.imag - PUB_COMPLEX.imag) < 1e-12,
      f"the published COMPLEX value is alpha=1's K_1 at w={w_pub:.0f}, recovered to 9 digits -- it is "
      f"NOT the alpha=2 kernel")
k2_same = K2(-(w_pub**2))
check(abs(k2_same.imag) < 1e-25,
      f"at the SAME point alpha=2 gives K_2 = {k2_same.real:.9f} with Im K_2 = {abs(k2_same.imag):.1e}, "
      f"i.e. purely real -- alpha=2 cannot produce the published complex value at any w > 1")
check(abs(abs(K2(1.0)) - PUB_REQUIRED) < 1e-12,
      f"but the REQUIRED value in the same parenthesis, 1/sqrt2 = {PUB_REQUIRED:.10f}, IS alpha=2's "
      f"K_2(1) = {abs(K2(1.0)):.10f}")
check(abs(abs(K1(1.0)) - (math.sqrt(5) - 1) / 2) < 1e-12,
      f"and alpha=1's own K_1(1) = {abs(K1(1.0)):.6f} = (sqrt5-1)/2, which the paper correctly records "
      f"as 0.618 in the NEXT clause -- so the row knowingly holds both kernels, but assigns the "
      f"COMPUTED value to the wrong one")


banner("S3  DEFECT 2 -- THE INTERNAL CONTRADICTION, :194 vs :207")

print("""  :194 (Theorem 2's own proof): for the alpha=2 kernel the cut is the COMPACT interval -1 < z < 0.
  :207 (twelve lines later):      the argument -(omega c/a0)^2 "lies on the cut".
  Those cannot both hold unless -(omega c/a0)^2 falls inside (-1, 0). Check real systems:\n""")
SYS = {"galaxy disc (v=200 km/s, R=8 kpc)": 200e3 / (8.0 * KPC),
       "wide binary (10 kAU, 1.5 Msun)": 2.4394e-13,
       "Hubble rate H_0 itself": H0}
print(f"  {'system':<36}{'omega [rad/s]':>16}{'footing':>9}{'z = -(omega c/a0)^2':>22}{'in (-1,0)?':>12}")
print("  " + "-" * 96)
inside = []
for sname, om in SYS.items():
    for fname, a0 in FOOTINGS.items():
        z = -((om * C / a0) ** 2)
        isin = -1.0 < z < 0.0
        inside.append(isin)
        print(f"  {sname:<36}{om:>16.4e}{fname:>9}{z:>22.4e}{str(isin):>12}")
check(not any(inside),
      "NO system on EITHER footing has -(omega c/a0)^2 inside the alpha=2 cut (-1, 0) -- every one is "
      "far past it, so :207's 'lies on the cut' is false under the paper's OWN :194")
# how far past, and what period WOULD be needed
for fname, a0 in FOOTINGS.items():
    om_need = a0 / C                      # |z| < 1  <=>  omega < a0/c
    per_need = 2 * math.pi / om_need / YR / 1e9
    print(f"    to reach the alpha=2 cut on the {fname} footing needs omega < {om_need:.3e} rad/s, "
          f"i.e. a period > {per_need:.3e} Gyr")
    check(per_need > 1e2,
          f"{fname}: reaching the alpha=2 cut needs a period > {per_need:.2e} Gyr, far beyond any "
          f"bound system -- the compact cut is physically unreachable, which is exactly Theorem 2's point")


banner("S4  WHAT DEFECT 2 COSTS -- the published 8.5-sigma pulsar exclusion at :220-224")

# omega * Im K_1 = omega/(2w) = omega/(2 omega c/a0) = a0/(2c) : exact and w-independent
om_s = sp.Symbol("omega", positive=True)
a0_s = sp.Symbol("a_0", positive=True)
drift_sym = sp.simplify(om_s * (1 / (2 * (om_s * sp.Symbol("c", positive=True) / a0_s))))
print(f"  alpha=1:  omega * Im K_1 = omega/(2w) with w = omega*c/a0  ->  {drift_sym}")
check(sp.simplify(drift_sym - a0_s / (2 * sp.Symbol("c", positive=True))) == 0,
      "omega * Im K_1 = a0/(2c) EXACTLY and w-INDEPENDENTLY -- the 'universal drift' is a genuine, "
      "well-defined alpha=1 prediction, so the 8.5-sigma exclusion is SOUND about alpha=1")

print(f"\n  {'footing':>9}{'a0 [m/s^2]':>14}{'a0/2c [1/s]':>15}{'a0/2c [1/yr]':>15}{'tau [Gyr]':>12}")
print("  " + "-" * 66)
for fname, a0 in list(FOOTINGS.items()) + [("paper", A0_PAPER)]:
    d = a0 / (2 * C)
    print(f"  {fname:>9}{a0:>14.4e}{d:>15.4e}{d*YR:>15.4e}{1.0/(d*YR)/1e9:>12.1f}")
d_paper = A0_PAPER / (2 * C) * YR
check(abs(d_paper - 4.93e-12) / 4.93e-12 < 0.005,
      f"the paper's quoted 4.93e-12 /yr and tau=203 Gyr reproduce on a0 = {A0_PAPER:.2e} to <0.5% "
      f"({d_paper:.3e} /yr, tau = {1.0/d_paper/1e9:.0f} Gyr) -- confirming the canonical footing")
ratio = (FOOTINGS["alt"] / FOOTINGS["canon"])
check(abs(ratio - 1.21) < 0.01,
      f"and the paper's '1.21x footing spread' reproduces exactly as a0_alt/a0_canon = {ratio:.4f}")

print("\n  Now the same quantity under the paper's OWN CURRENT kernel:")
for sname, om in SYS.items():
    for fname, a0 in FOOTINGS.items():
        z = -((om * C / a0) ** 2)
        print(f"    {sname:<36}{fname:>7}  Im K_2 = {abs(K2(z).imag):.3e}")
check(all(abs(K2(-((om * C / a0) ** 2)).imag) < 1e-25
          for om in SYS.values() for a0 in FOOTINGS.values()),
      "Im K_2 = 0 to machine zero for EVERY system on BOTH footings -> under alpha=2 the dissipative "
      "drift is EXACTLY ZERO, so a0/2c is not predicted and there is nothing for a pulsar to exclude")

print("""
  => THE 8.5-SIGMA EXCLUSION IS AN alpha=1-EXCLUSIVE RESULT PRESENTED IN AN alpha=2 PAPER. It is
     correct and non-trivial ABOUT alpha=1 (the drift really is a0/2c, universally). It is VACUOUS
     about alpha=2, whose drift is identically zero. Note this does not weaken the paper's CONCLUSION:
     Corollary 2.1/2.2 argue the dissipative channel is unobservable, and Im K_2 == 0 makes that case
     MORE strongly, not less. What is wrong is the framing -- an empirical 8.5-sigma kill is offered as
     "independent confirmation from data" for a proposition the current kernel does not assert.""")


banner("S5  SCOPE -- what stands, and the defect CLASS")

print("""  WHAT STANDS, unqualified:
   * Theorem 2 and Corollary 2.1/2.2. The disjointness of z >= 0 from the cut, and the conclusion that
     no first-moment closure delivers both the relation and dissipation, are UNAFFECTED -- indeed S1
     strengthens them, since Im K_2 == 0 is a stronger statement than "small".
   * :194 is CORRECT and is what the paper should be read by.
   * The pulsar analysis itself, as a statement about alpha=1, including the Peters back-reaction
     validation against J0737-3039 and B1913+16.

  WHAT IS OWED (reporting, not editing -- the paper is published and republication is Carl's call):
   1. :207-210 -- assign the computed complex K to alpha=1 explicitly, or recompute it for alpha=2
      (where it is real and no such "failure" arises in that form).
   2. :207 -- "lies on the cut" must be scoped to alpha=1, since :194 already says alpha=2's cut is
      compact and unreachable.
   3. :220-224 -- label the 8.5-sigma exclusion as bearing on the RETIRED alpha=1 closure.

  THE DEFECT CLASS, and this is the point worth carrying forward. This is the SECOND independently
  confirmed case of an alpha=1-EXCLUSIVE quantity underpinning a published or frozen claim after the
  alpha=2 switch -- the first being the frozen pre-registration's s^TX amplitude built on the alpha=1
  tail a0/(2g) (margin 1.50x -> 1.03e6x, Amendment 5 still owed). The alpha=2 migration was done
  paper-by-paper and at least one paper got only half of it: the source script
  mi_dcac_split_settled_2026.py still carries the alpha=1 values ("required K(1) = 0.618", "the cut
  needs z <= -1/4") that v3 promoted inconsistently. RECOMMENDATION: audit every published artefact for
  alpha=1-exclusive quantities as a class, rather than one at a time as they surface.""")

banner("RESULT")
npass = sum(1 for c, _ in ok if c)
print(f"  {npass}/{len(ok)} checks held.")
if npass != len(ok):
    print("\n  FAILED CHECKS:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: both defects verified from the kernels, independent of the subagents that flagged them.")
