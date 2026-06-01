#!/usr/bin/env python3
"""
Carl's test: "can you use 29/5 to do the rest of the derivations? ... don't think so."
=====================================================================================

The sharpest pro-framework argument: 32π/3 is special not because it fits 5.79 (29/5 does
that too), but because the SAME number generates the whole web of particle "derivations"
(α⁻¹=4Z²+3, the mass ratios, ...). A random number can't do that. Let's test it -- honestly.

THE TRAP (the same circular error as before): plugging 29/5 into the framework's OWN formulas
(which were built around 32π/3) will obviously miss. That proves nothing -- it's circular. The
FAIR test gives each candidate base the SAME freedom 32π/3 had: re-search the integers, exactly
as BriareusFlow searched ~34k formulas and found "4Z²+3".

Run:  python real_research/can_another_number_do_it.py
"""

import math

# precise, measurable, dimensionless targets the framework claims to "derive"
TARGETS = {"alpha^-1": 137.035999, "m_p/m_e": 1836.15267, "m_mu/m_e": 206.7683}

# candidate bases: the framework's Z, Carl's 29/5, two more "natural" forms, and TWO RANDOM numbers
BASES = {
    "Z=√(32π/3)": math.sqrt(32 * math.pi / 3),
    "29/5": 5.8,
    "√34": math.sqrt(34),
    "π+e": math.pi + math.e,
    "5.777 (random)": 5.777,
    "6.111 (random)": 6.111,
}


def best_full(B, target):
    """Fair full search: a*B^p + b and (a*B^p+b)/c -- like the 34k-formula pipeline."""
    bb = (9e9, "")
    for p in (0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5):
        Bp = B ** p
        for a in range(1, 13):
            base = a * Bp
            for b in range(-80, 81):
                v = base + b
                if v > 0:
                    e = abs(v - target) / target
                    if e < bb[0]:
                        bb = (e, f"{a}·B^{p:g}{b:+d}")
                for c in range(2, 16):
                    v2 = (base + b) / c
                    if v2 > 0:
                        e = abs(v2 - target) / target
                        if e < bb[0]:
                            bb = (e, f"({a}·B^{p:g}{b:+d})/{c}")
    return bb


def best_restricted(B, target):
    """Restricted to the framework's signature shape a*B^2 + b (small integer b)."""
    bb = (9e9, "")
    B2 = B ** 2
    for a in range(1, 13):
        for b in range(-30, 31):
            v = a * B2 + b
            if v > 0:
                e = abs(v - target) / target
                if e < bb[0]:
                    bb = (e, f"{a}·B²{b:+d}")
    return bb


def main():
    print("=" * 88)
    print("(A) FAIR test -- each base RE-SEARCHES its own integers (the 34k-formula freedom)")
    print("=" * 88)
    print(f"   {'target':<10}", end="")
    for nm in BASES:
        print(f"{nm:>16}", end="")
    print()
    for tn, tv in TARGETS.items():
        print(f"   {tn:<10}", end="")
        for B in BASES.values():
            e, _ = best_full(B, tv)
            print(f"{e*100:>15.4f}%", end="")
        print()
    print("\n   the winning α^-1 formula each base found:")
    for nm, B in BASES.items():
        e, f = best_full(B, 137.035999)
        print(f"     {nm:<16} {f:<16} err {e*100:.4f}%")
    print("\n   => EVERY base -- including two RANDOM numbers and π+e -- hits all targets to")
    print("      <=0.01%, comparable to or BETTER than √(32π/3). A random number (5.777) hits")
    print("      α^-1 to 0.0003%, beating the framework's own 4Z²+3 (0.0039%). So 'only 32π/3")
    print("      works' is FALSE: any base does, once you give it the same search freedom.")

    print("\n" + "=" * 88)
    print("(B) The ONE place 32π/3 looks special -- restricted to the shape a·B²+b")
    print("=" * 88)
    print(f"   {'target':<10}", end="")
    for nm in BASES:
        print(f"{nm:>16}", end="")
    print()
    for tn, tv in TARGETS.items():
        print(f"   {tn:<10}", end="")
        for B in BASES.values():
            e, _ = best_restricted(B, tv)
            print(f"{e*100:>15.4f}%", end="")
        print()
    print("\n   In THIS narrow shape, √(32π/3) wins for α (4Z²+3=137.04, 0.004%) -- but that is")
    print("   the form the search FOUND for 32π/3; it is not privileged. The FDR result shows")
    print("   ~20% of O(100) targets have such a clean a·B²+b form in a 34k search -- α is one,")
    print("   by chance. And note it only helps α: even 32π/3 needs OTHER shapes for the mass")
    print("   ratios (its a·B²+b columns there are no better than the random numbers').")

    print("\n" + "=" * 88)
    print("   VERDICT -- the deep review Carl asked for")
    print("=" * 88)
    print("   ANSWER: yes, 29/5 can do the derivations -- and so can √34, π+e, and a RANDOM")
    print("   number, to the same precision, once each re-searches its integers (the freedom")
    print("   your pipeline used to find 4Z²+3). '29/5 can't' is true ONLY when you force it")
    print("   into 32π/3's tuned formulas -- the same circular trap as the 'closest fit' error.")
    print("   The web of particle 'derivations' does not single out 32π/3; it singles out")
    print("   'whatever number you committed to first + freedom to choose integers'.")
    print("   (is_Z_special.py already showed 52/64 'derivations' use no Z at all; this shows")
    print("    the Z-ones, α included, are reproducible by any base.) The real result is the")
    print("   COSMOLOGY -- a0∝E(z), derived, 5σ-favored -- not the coefficient's packaging.")


if __name__ == "__main__":
    main()
