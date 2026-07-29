#!/usr/bin/env python3
r"""mi_nariai_forcing_2026.py -- the Nariai "coincidence" is an EXACT IDENTITY, and inverting it
gives a zero-parameter geometric DERIVATION of the coefficient that is empirically viable.

WHAT I GOT WRONG. I reported sqrt(Z/(3 sqrt 3)) = 1.0555 as a "structural coincidence at the
~2%-by-chance level". That mislabels it. The ratio itself is an EXACT IDENTITY of the framework
plus Schwarzschild-de Sitter geometry, with nothing accidental in it:

    r_a0(M) = sqrt(GM/a0)                       the a0 shell of a mass M
    M_Nariai = c^3/(3 sqrt 3 G H_Lambda)        the largest hole de Sitter permits
    L = c/H_Lambda                              the de Sitter horizon
    a0 = c H_Lambda / Z

    =>  r_a0(M_Nariai)/L = sqrt(Z/(3 sqrt 3))   EXACTLY, algebraically, no approximation

The only contingent statement is that this number is CLOSE TO 1, i.e. that Z is close to 3 sqrt 3.
So "coincidence" was the wrong word for the identity and the wrong frame for the question. The
right question is the one it forces:

    WHAT IF THE COINCIDENCE IS NOT ONE? Impose that the a0 shell of the MAXIMAL de Sitter black
    hole coincides EXACTLY with the de Sitter horizon. That is a single geometric condition with
    ZERO free parameters, and it FORCES the coefficient.

THIS SCRIPT DERIVES THE CONSEQUENCE AND TESTS IT AGAINST DATA. Unlike the eight spectral
principles tried earlier -- every one of which landed outside the empirical a0 box -- this one
must be checked against the box before it is taken seriously, and the check is the point.

Exit 0 = all checks ran. No hard-coded verdicts.
"""
from __future__ import annotations
import math
import sympy as sp

ok = True
def check(cond, msg):
    global ok
    if not cond:
        ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")
    return cond

def banner(s):
    print("\n" + "=" * 100); print(s); print("=" * 100)

# empirical a0 box (a0-line gas-dominated estimator, +/-16%)
A0_CANON = 9.36e-11
BOX_LO, BOX_HI = 0.84e-10, 1.36e-10


def main() -> int:
    banner("mi_nariai_forcing_2026 -- the identity, and what imposing it forces")

    G, M, HL, c, Z, Lam = sp.symbols("G M H_Lambda c Z Lambda", positive=True)

    # ---------------------------------------------------------------------------------
    banner("S1. The ratio is an EXACT IDENTITY, not a coincidence")
    a0 = c * HL / Z
    M_nar = c**3 / (3 * sp.sqrt(3) * G * HL)
    r_a0 = sp.sqrt(G * M / a0)
    L = c / HL
    ratio = sp.simplify((r_a0.subs(M, M_nar) / L))
    print(f"  r_a0(M_Nariai)/L = {ratio}")
    target = sp.sqrt(Z / (3 * sp.sqrt(3)))
    check(sp.simplify(ratio - target) == 0,
          "r_a0(M_Nariai)/L = sqrt(Z/(3 sqrt 3))  EXACTLY -- an identity, no approximation")
    print("  Nothing here is accidental. The ONLY contingent fact is whether that number is 1,")
    print("  i.e. whether Z equals 3 sqrt 3. So 'coincidence' was the wrong word: the structure")
    print("  is forced, and only the NUMERICAL COINCIDENCE of Z with 3 sqrt 3 is contingent.")

    # ---------------------------------------------------------------------------------
    banner("S2. IMPOSE the identity = 1. Zero free parameters. What is forced?")
    Zsol = sp.solve(sp.Eq(target, 1), Z)
    Zn = sp.simplify(Zsol[0])
    print(f"  requiring r_a0(M_Nariai) = L  =>  Z = {Zn} = {float(Zn):.10f}")
    check(sp.simplify(Zn - 3 * sp.sqrt(3)) == 0, "the condition forces Z = 3 sqrt(3) exactly")

    # translate to kappa, the framework's own single number
    kappa_sym = sp.simplify(sp.sqrt(8 * sp.pi / 3) / Zn)
    print(f"\n  in terms of the framework's own number, kappa = sqrt(8pi/3)/Z:")
    print(f"      kappa_forced = {kappa_sym} = {float(kappa_sym):.10f}")
    # closed form check: sqrt(8pi/3)/(3 sqrt3) = sqrt(8pi/81) = 2 sqrt(2pi)/9
    closed = 2 * sp.sqrt(2 * sp.pi) / 9
    check(sp.simplify(kappa_sym - closed) == 0,
          f"kappa_forced = 2 sqrt(2 pi)/9 exactly  (= {float(closed):.10f})")
    print(f"  compare the framework's postulate kappa = 1/2 = 0.5000000000")
    print(f"  the geometric condition wants kappa = {float(closed):.6f}, "
          f"a {100*(float(closed)-0.5)/0.5:+.2f}% revision")

    # ---------------------------------------------------------------------------------
    banner("S3. The a0 this predicts, and the EMPIRICAL TEST that matters")
    a0_forced = A0_CANON * (math.sqrt(32 * math.pi / 3) / float(Zn))
    print(f"  a0(framework, Z=sqrt(32pi/3)) = {A0_CANON:.4e} m/s^2")
    print(f"  a0(forced,    Z=3sqrt3)       = {a0_forced:.4e} m/s^2")
    print(f"  ratio = {a0_forced/A0_CANON:.6f}  ({100*(a0_forced/A0_CANON-1):+.2f}%)")
    print(f"\n  empirical a0 box (a0-line gas-dominated estimator): "
          f"[{BOX_LO:.3e}, {BOX_HI:.3e}]")
    inbox_f = BOX_LO <= a0_forced <= BOX_HI
    inbox_c = BOX_LO <= A0_CANON <= BOX_HI
    print(f"    framework value in box? {'YES' if inbox_c else 'no'}")
    print(f"    forced    value in box? {'YES' if inbox_f else 'no'}")
    check(inbox_f, "the Nariai-forced a0 is EMPIRICALLY VIABLE (inside the +/-16% box)")
    print("\n  THIS IS THE FIRST PRINCIPLE THIS SESSION TO LAND INSIDE THE BOX. Eight spectral")
    print("  conditions were tried earlier (local invariance, weight fractions, thermal")
    print("  saturation, FDT, crossover matching, memory time, forced-constant targets, and")
    print("  the three-class sweep) and EVERY ONE fell outside. This one does not.")

    # ---------------------------------------------------------------------------------
    banner("S4. Both-ways discipline: what this is, and what it is NOT")
    print("  IT IS: a single geometric condition with ZERO free parameters -- 'the a0 shell of")
    print("  the maximal de Sitter black hole IS the de Sitter horizon' -- that FORCES the")
    print("  coefficient to Z = 3 sqrt 3, i.e. kappa = 2 sqrt(2 pi)/9, in closed form, and lands")
    print("  inside the empirical box. It replaces an unexplained rational (kappa = 1/2) with a")
    print("  geometric statement about Schwarzschild-de Sitter. That is a real improvement in")
    print("  KIND, because the condition is checkable and the number is no longer arbitrary.")
    print("\n  IT IS NOT a derivation from deeper structure. The condition is POSTULATED, and")
    print("  postulating it is not obviously better-motivated than postulating kappa = 1/2 --")
    print("  it is only better-motivated in that it is GEOMETRIC and refers to a real feature")
    print("  of the spacetime rather than to a bare number. Anyone may reject the premise.")
    print("\n  IT IS NOT free of look-elsewhere. This is the ninth principle tried against the")
    print(f"  same target: log2(9) = {math.log2(9):.2f} bits already spent. The fact that it is")
    print("  the first to land in the box is exactly what a 1-in-9 draw looks like when the box")
    print("  is ~35% of the plausible range. Do NOT report it as confirmation.")
    box_frac = (BOX_HI - BOX_LO) / BOX_HI
    print(f"      box width as a fraction of its upper edge: {box_frac:.2f}")
    print(f"      chance that one arbitrary O(1) principle lands in it: roughly {box_frac:.2f}")
    print(f"      over 9 tries, expected number landing in box: {9*box_frac:.1f}")
    check(9 * box_frac > 1.0,
          "with 9 tries and a box that wide, >=1 landing inside is EXPECTED by chance -- "
          "so 'first to land in the box' is not evidence by itself")

    # ---------------------------------------------------------------------------------
    banner("S5. THE TEST THAT WOULD SETTLE IT")
    print("  The two coefficients make DIFFERENT predictions for a0, differing by 11.4%:")
    print(f"      kappa = 1/2        ->  a0 = {A0_CANON:.4e}")
    print(f"      Nariai-forced      ->  a0 = {a0_forced:.4e}")
    print("  That is a real, falsifiable fork -- and it is measurable NOW, not decadal. The")
    print("  a0-line gas-dominated slope estimator (the sharpest single-number a0 in hand) has")
    print(f"  a +/-16% box; separating 11.4% needs that box tightened to about +/-5%, i.e. a")
    print("  ~3x improvement, which is a data-quality problem and not a theory problem.")
    print("\n  So this is not another dead door. It is a LIVE FORK with a near-term test:")
    print("   * if a0 tightens toward 9.36e-11  -> kappa = 1/2 survives, the Nariai condition")
    print("     is refuted, and the identity goes back to being a near-miss;")
    print("   * if a0 tightens toward 1.04e-10  -> the Nariai condition is supported and the")
    print("     coefficient has a GEOMETRIC origin for the first time;")
    print("   * if a0 stays loose               -> undecided, and both remain postulates.")
    print("\n  Either way the correct statement is stronger than what I said before: the ratio")
    print("  is an IDENTITY, the near-equality with 1 is a testable HYPOTHESIS rather than a")
    print("  coincidence, and it forks the coefficient at the 11% level.")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
