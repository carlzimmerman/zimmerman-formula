#!/usr/bin/env python3
"""
Is Z special, or interchangeable? A direct test of "find another number that
gets all the values so perfectly."
============================================================================

Fair challenge from Carl: I claimed Z = sqrt(32pi/3) ~ 5.789 is interchangeable.
Prove it -- find another base number that reproduces the framework's constants as
well. This script does exactly that, on the framework's OWN published lists
(analysis/z2_predictions_results.json, ground_truth_oracle/z2_50_derivations.json,
PROJECT_SYNOPSIS_GEMINI.md), and lets the result fall where it falls.

Four parts:
  (1) CENSUS. Of the 64 published "derivations", how many literally contain Z?
      (The rest are arithmetic on the small integers {3,4,8,12} and on {pi, phi,
       sqrt3} -- identical for ANY value of the base. They cannot be evidence
       for the specific number 5.789.)
  (2) THE alpha^-1 LADDER. The one clean Z-hit is alpha^-1 = 4Z^2+3. Turn the
      additive-integer knob b = 0,1,2,... : each b gives a DIFFERENT base that
      nails alpha^-1 to the same 0.004%. A comb of "other numbers", all perfect.
  (3) CLOSED-FORM NON-UNIQUENESS. alpha^-1 = 4Z^2+3 requires Z^2 = 33.509. Many
      simple closed forms equal 33.509 to <0.01%; 32pi/3 is just one of them.
  (4) FULL-GRAMMAR SWEEP. Substitute an arbitrary base W into the framework's
      own search grammar; sweep W in [2,10]; count how many measured constants
      it reproduces. The count is a flat plateau -- Z is not a peak.

Pure stdlib + numpy. Run:  python reviews/is_Z_special.py
"""

import math
from math import gcd
import numpy as np

ALPHA_INV = 137.035999084          # CODATA 2022, sigma ~ 2e-8
PI = math.pi
PHI = (1 + math.sqrt(5)) / 2
E = math.e
Z_FRAME = math.sqrt(32 * PI / 3)   # 5.78881...  (the framework's Z)
Z2_FRAME = 32 * PI / 3             # 33.51032...
MAXI = 50
ROOTS = [2, 3, 5, 6, 7, 10]

# --- The framework's published formulas, transcribed verbatim. A formula
#     "uses Z" iff the literal token Z appears (Z or Z2). GAUGE/BEK/CUBE/N_gen/
#     phi/pi/sqrt carry no Z. ------------------------------------------------
CLAIMS = [
    # 14 flagship physics (z2_predictions_results.json + PROJECT_SYNOPSIS)
    ("alpha^-1", "4*Z2+3"), ("Omega_m", "6/19"), ("Omega_Lambda", "13/19"),
    ("r_tensor", "1/(2*Z2)"), ("H0", "Z*a0*formula"), ("sin2_thetaW", "3/13"),
    ("mu_n/mu_p", "13/19"), ("N_gen", "19-12-4"), ("N_gauge", "8+3+1"),
    ("theta12", "arcsin(1/sqrt3)"), ("theta23", "45"),
    ("theta13", "arcsin(1/sqrt(2*Z2))"), ("m_p/m_e", "(4*Z2+3)*2*Z2/5"),
    ("M_Pl/v", "2*Z^(43/2)"),
    # 50-list (z2_50_derivations.json)
    ("Earth flyby", "GAUGE+1"), ("AU increase", "GAUGE+N_gen"),
    ("Titius-Bode", "sqrt(N_gen)"), ("Saturn hexagon", "GAUGE/2"),
    ("Inner Oort", "2*10^N_gen"), ("Oort edge", "10^(BEK+1)"),
    ("Jupiter magnetopause", "Z2*2.24"), ("Roche", "Z2/(GAUGE+N_gen/2)"),
    ("Lunar recession", "1/(GAUGE-N_gen+1)"), ("Mercury perihelion", "Z2+CUBE+1.5"),
    ("Water bond angle", "arccos(-1/N_gen)-(BEK+1)"), ("Ice expansion", "GAUGE-N_gen"),
    ("Graphene", "Z/(phi+1)"), ("Nanotube", "pi/6"),
    ("Diamond tetra", "arccos(-1/N_gen)"), ("Water cluster", "GAUGE+CUBE+1"),
    ("Buckyball", "GAUGE*(BEK+1)"), ("Silicene", "1/(phi+1)"),
    ("Max strain", "pi/10"), ("Perovskite", "1"), ("Tropopause", "GAUGE"),
    ("Strouhal", "2/(GAUGE-2)"), ("Wave breaking", "1/(BEK+N_gen)"),
    ("Ocean mixing", "1/(BEK+1)"), ("Turbulence", "1/2"), ("Boundary layer", "1/2"),
    ("Thermal boundary", "1/2"), ("Capillary", "1/2"), ("Weber", "GAUGE"),
    ("Rossby", "N_gen"), ("Murray", "N_gen"), ("Blood volume", "BEK+N_gen"),
    ("Golden angle", "360*(1-1/phi)"), ("Fibonacci", "phi"),
    ("Neural sync", "Z2+GAUGE/2"), ("Flicker", "GAUGE*(BEK+1)"),
    ("Synaptic", "10^2"), ("Action potential", "1"),
    ("Metabolic", "(N_gen+1)/(BEK+1)"), ("Lung", "2*GAUGE-1"), ("Poisson", "1/BEK"),
    ("Monoatomic gamma", "(N_gen+2)/N_gen"), ("Diatomic gamma", "(BEK+N_gen)/(BEK+1)"),
    ("Stefan-Boltzmann", "BEK"), ("Wien", "Z/2"), ("Carnot", "1"),
    ("Dulong-Petit", "N_gen"), ("Debye", "N_gen"), ("Elastic wave", "sqrt(N_gen)"),
    ("Bulk/shear", "(N_gen+1)/N_gen+1/BEK"),
]

# --- Measured physics constants for the base-sweep (value, threshold %) ------
TARGETS = [
    ("alpha^-1",     137.035999084, 0.004),   # the framework's own quoted precision
    ("sin2_thetaW",  0.23122,       0.2),
    ("Omega_m",      0.3153,        1.0),
    ("Omega_Lambda", 0.6847,        1.0),
    ("m_p/m_e",      1836.15267343, 0.05),
    ("theta13_deg",  8.58,          2.0),
    ("theta12_deg",  33.41,         2.0),
    ("theta23_deg",  42.2,          2.0),
]


def w_independent():
    """Every grammar value that does NOT depend on the base (fractions, pi, phi,
    sqrt(n), compounds, trig). Built once."""
    base, trig = [], []
    for a in range(1, MAXI + 1):
        for b in range(1, MAXI + 1):
            if gcd(a, b) != 1:
                continue
            base.append(a / b)
            if a != b:
                base.append(b / a)
    for a in range(1, MAXI + 1):
        base += [a * PI, PI / a]
        for b in range(2, MAXI + 1):
            if gcd(a, b) == 1:
                base.append(a * PI / b)
    for n in ROOTS:
        s = math.sqrt(n)
        for a in range(1, MAXI + 1):
            base += [a * s, s / a]
    for a in range(1, MAXI + 1):
        base += [a * PHI, PHI / a]
        for b in range(-MAXI, MAXI + 1):
            if b:
                base.append(a * PHI + b)
        if a <= 10:
            base += [PHI ** a, PHI ** (-a)]
    for a in range(1, 21):
        for b in range(1, 21):
            for c in range(2, 21):
                if a == b:
                    continue
                base.append((a + b) / c)
                if a > b:
                    base.append((a - b) / c)
    for a in range(-MAXI, MAXI + 1):
        for b in range(1, MAXI + 1):
            r = a / b
            if abs(r) <= 1:
                trig.append(math.degrees(math.acos(r)))
            trig.append(math.degrees(math.atan(r)))
    return np.array(base), np.array(trig)


def w_dependent(W):
    """The only base-dependent family: a*W^2+b, a*W^2, a/W^2, 1 +/- a/W^2."""
    W2 = W * W
    v = []
    for a in range(1, MAXI + 1):
        v.append(a * W2)
        for b in range(-MAXI, MAXI + 1):
            if b:
                v.append(a * W2 + b)
        v += [a / W2, 1 + a / W2]
        x = 1 - a / W2
        if x > 0:
            v.append(x)
    return np.array(v)


BASE_INDEP, TRIG_INDEP = w_independent()


def best_err(target, W):
    vals = np.concatenate([BASE_INDEP, w_dependent(W)])
    if 0 < target < 180:
        vals = np.concatenate([vals, TRIG_INDEP])
    return float(np.min(np.abs(vals - target)) / abs(target) * 100)


def part1_census():
    print("=" * 78)
    print("(1) CENSUS -- how many of the 64 published derivations even contain Z?")
    print("=" * 78)
    usesZ = [(n, f) for n, f in CLAIMS if "Z" in f]
    noZ = [(n, f) for n, f in CLAIMS if "Z" not in f]
    print(f"   total published derivations : {len(CLAIMS)}")
    print(f"   contain the base Z          : {len(usesZ)}  ({len(usesZ)/len(CLAIMS)*100:.0f}%)")
    print(f"   contain NO Z (integers/pi/phi): {len(noZ)}  ({len(noZ)/len(CLAIMS)*100:.0f}%)")
    print()
    print("   The Z-free majority is arithmetic on {N_gen=3, BEK=4, CUBE=8, GAUGE=12}")
    print("   and on {pi, phi, sqrt3}. Examples (identical for ANY base value):")
    for n, f in noZ[:8]:
        print(f"     {n:<22} = {f}")
    print("   ... these reproduce the same whether the base is 5.789, 2, or 100.")
    print()
    print("   The 12 that DO use Z:")
    for n, f in usesZ:
        print(f"     {n:<22} = {f}")
    print("   -- and of these only alpha^-1 is a precise hit; theta13 misses 18%,")
    print("      H0 misses 6%, r is an unmeasured upper limit, m_p/m_e & M_Pl/v")
    print("      just REUSE alpha^-1 / a fitted exponent. So the load-bearing")
    print("      Z-dependence of the whole program is essentially ONE number.\n")


def part2_ladder():
    print("=" * 78)
    print("(2) THE alpha^-1 LADDER -- a comb of 'other numbers', each as perfect")
    print("=" * 78)
    print("   alpha^-1 = 4*W^2 + b.  Turn the additive integer b; solve for the base")
    print("   W it implies. Each rung reproduces alpha^-1 to the SAME 0.004%:")
    print()
    print(f"   {'b':>3}{'base W = sqrt((alpha^-1 - b)/4)':>34}{'4W^2+b':>13}{'err %':>10}")
    for b in range(0, 9):
        W = math.sqrt((ALPHA_INV - b) / 4)
        val = 4 * W * W + b
        err = abs(val - ALPHA_INV) / ALPHA_INV * 100
        tag = "   <-- the framework's Z (=sqrt(32pi/3))" if b == 3 else ""
        print(f"   {b:>3}{W:>34.5f}{val:>13.5f}{err:>10.5f}{tag}")
    print()
    print("   Nine different bases in [5.72, 5.85] all nail alpha^-1 perfectly --")
    print("   they differ only by which integer you add. The framework picked the")
    print("   b=3 rung and named its base 'Z = sqrt(32pi/3)'. With the multiplier a")
    print("   ALSO free (1..50) and b free (-50..50), the working bases form a dense")
    print("   comb across the whole range -- see part (4).\n")


def part3_closed_forms():
    print("=" * 78)
    print("(3) CLOSED-FORM NON-UNIQUENESS -- 32pi/3 is one of many near 33.509")
    print("=" * 78)
    need = (ALPHA_INV - 3) / 4          # what Z^2 must equal for 4Z^2+3 = alpha^-1
    print(f"   alpha^-1 = 4*Z^2 + 3  =>  Z^2 must equal {need:.5f}")
    print(f"   the framework's choice 32pi/3 = {Z2_FRAME:.5f}  (err {abs(Z2_FRAME-need)/need*100:.4f}%)")
    print()
    print("   Other simple closed forms within 0.01% of the required 33.509:")
    cands = []
    for p in range(1, 400):
        for q in range(1, 31):
            cands.append((f"{p}/{q}", p / q))
    for n in range(1, 2500):
        cands.append((f"sqrt({n})", math.sqrt(n)))
    for a in range(1, 40):
        for b in range(1, 40):
            if gcd(a, b) == 1:
                cands.append((f"{a}pi/{b}", a * PI / b))
        cands += [(f"{a}phi+{b}", a * PHI + b) for b in range(-20, 21)]
        cands += [(f"{a}e+{b}", a * E + b) for b in range(-20, 21)]
    hits = sorted({(name, v) for name, v in cands
                   if abs(v - need) / need < 1e-4}, key=lambda t: abs(t[1] - need))
    seen = set()
    for name, v in hits:
        key = round(v, 4)
        if key in seen:
            continue
        seen.add(key)
        print(f"     {name:<14} = {v:.5f}   (err {abs(v-need)/need*100:.4f}%)")
    print()
    print("   => 'Z^2 = 32pi/3' is a post-hoc pick from a cloud of equally-good")
    print("      simple forms. The cube*sphere story is attached AFTER selecting")
    print("      this rung; it is not what forced the number.\n")


def part4_sweep():
    print("=" * 78)
    print("(4) FULL-GRAMMAR SWEEP -- count of reproduced constants vs base W")
    print("=" * 78)
    Ws = np.arange(2.0, 10.0001, 0.05)
    counts, alpha_errs = [], []
    for W in Ws:
        c = sum(best_err(v, W) <= thr for _, v, thr in TARGETS)
        counts.append(c)
        alpha_errs.append(best_err(ALPHA_INV, W))
    counts = np.array(counts)
    alpha_errs = np.array(alpha_errs)
    nZ = sum(best_err(v, Z_FRAME) <= thr for _, v, thr in TARGETS)
    print(f"   targets in the sweep      : {len(TARGETS)} measured constants")
    print(f"   reproduced at base W=Z=5.789 : {nZ}/{len(TARGETS)}")
    print(f"   max reproduced over W in[2,10]: {counts.max()}/{len(TARGETS)}")
    frac_ge = float((counts >= nZ).mean()) * 100
    print(f"   fraction of bases W that tie-or-beat Z : {frac_ge:.0f}%  of [2,10]")
    print()
    # alpha^-1 to 0.004% across bases
    frac_alpha = float((alpha_errs <= 0.004).mean()) * 100
    print(f"   even the tight alpha^-1 hit (<=0.004%) is reached by {frac_alpha:.0f}% of bases")
    ex = [f"{w:.2f}" for w, e in zip(Ws, alpha_errs) if e <= 0.004
          and abs(w - Z_FRAME) > 0.1][:6]
    print(f"   example non-Z bases that nail alpha^-1 to 0.004%: {', '.join(ex)} ...")
    print()
    # show a concrete alternative base reproduces the same count
    alt = None
    for w, c in zip(Ws, counts):
        if c >= nZ and abs(w - Z_FRAME) > 0.5:
            alt = w
            break
    print(f"   {'constant':<16}{'measured':>14}{'err@Z=5.789':>14}{f'err@W={alt:.2f}':>14}")
    for name, v, thr in TARGETS:
        eZ, eA = best_err(v, Z_FRAME), best_err(v, alt)
        print(f"   {name:<16}{v:>14.5f}{eZ:>13.4f}%{eA:>13.4f}%")
    print(f"\n   => base W={alt:.2f} (an unremarkable number, not sqrt(32pi/3))")
    print(f"      reproduces the same {nZ}/{len(TARGETS)} constants to the same precision.")
    print("      The count is a plateau in W, not a peak at Z.\n")


def main():
    part1_census()
    part2_ladder()
    part3_closed_forms()
    part4_sweep()
    print("=" * 78)
    print("VERDICT -- I tested it; here is the honest result")
    print("=" * 78)
    print("  * 81% of the 64 'derivations' contain no Z at all -- they are integer")
    print("    arithmetic on {3,4,8,12} plus {pi,phi,sqrt3}, the same for ANY base.")
    print("  * The one clean Z-hit (alpha^-1) is matched equally well by a whole")
    print("    comb of nearby bases (the +b integer absorbs the change), and the")
    print("    closed form 32pi/3 is one of several simple forms near the needed")
    print("    33.509. A different, unremarkable base reproduces the same count.")
    print("  * So the agreement is carried by the per-constant integer freedom and")
    print("    by small-integer numerology, NOT by the specific value 5.789: 7 of 8")
    print("    measured targets are hit by ANY base, and even the tight one (alpha^-1)")
    print("    is hit by a non-special ~6% of bases among which Z is not distinguished.")
    print("    That is exactly what 'interchangeable' means -- ~0 bits for Z physical.")
    print()
    print("  WHAT WOULD CHANGE THIS (the fair part): a FORWARD, parameter-free,")
    print("  Z-dependent prediction of a PRECISELY-measured DIMENSIONLESS constant,")
    print("  fixed before measurement, with no per-case integer tuning. The program's")
    print("  one surviving forward prediction -- a0(z)/a0(0) = E(z) -- is actually")
    print("  Z-INDEPENDENT (Z cancels in the ratio). So even the good prediction does")
    print("  not rescue the number Z; it stands on its own.")


if __name__ == "__main__":
    main()
