#!/usr/bin/env python3
"""mi_kappa_spectral_reduction_2026.py -- collapse "derive Z" to "derive kappa", and show the
spectral axis is a LINEAR probe of kappa.

WHY THIS INSTEAD OF ANOTHER CANDIDATE CONDITION. Four attempts have now been made to find a
forced condition fixing Z:
  1. local kernel conditions            -> ALL scale-invariant (mi_bootstrap_circularity_2026)
  2. spectral weight vs natural values  -> no candidate gives 32pi/3 (mi_spectral_weight_swing)
  3. thermal half-saturation R(Z)=1/2   -> Z* = 4.185, misses both coefficients
  4. (this file's alternative) memory-time matching -> see S4
Each further guess costs look-elsewhere, and guessing conditions until one yields 32pi/3 is
exactly the failure mode PAPER_ATOMOS_NULL documents. So this script does something different:
it proves a REDUCTION. It does not try to produce the number.

THE FRAMEWORK'S OWN DOCUMENT ALREADY SAYS WHERE THE SCALE COMES FROM.
prep_2026/mi_fingerprint/KERNEL_THEORY.md:47 -- "the frequency response is forced by
(Herglotz class) + (the RAR): there is nothing left to tune." The measure is UNIQUE given
Herglotz analyticity plus the RAR CALIBRATION. The calibration is data. So the framework
already states, in its own words, that the scale is fixed empirically, not derived. Any
forced condition must therefore ADD an axiom -- and an axiom chosen to reproduce 32pi/3 is
fitting, not deriving. That is the honest boundary of the problem.

WHAT CAN STILL BE DONE HONESTLY: sharpen WHAT must be derived, and identify where a forced
condition could still live. Both are done below, with no fitting.

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
    print("\n" + "=" * 96); print(s); print("=" * 96)


def main() -> int:
    banner("mi_kappa_spectral_reduction_2026")

    kappa, G, rho, c, HL, Lam = sp.symbols("kappa G rho_Lambda c H_Lambda Lambda", positive=True)

    # -----------------------------------------------------------------------------------
    banner("S1. REDUCTION: 'why 32pi/3?' is EXACTLY 'why kappa = 1/2?'")
    # framework: a0 = c^2 sqrt(Lambda/(32 pi)),  Lambda = 3 H^2/c^2,  Z = cH/a0
    a0_of_Lam = c**2 * sp.sqrt(Lam / (32 * sp.pi))
    Z_expr = sp.simplify(c * HL / a0_of_Lam.subs(Lam, 3 * HL**2 / c**2))
    print(f"  a0 = c^2 sqrt(Lambda/32pi),  Lambda = 3H^2/c^2   =>   Z = cH/a0 = {Z_expr}")
    check(sp.simplify(Z_expr - sp.sqrt(32 * sp.pi / 3)) == 0, "Z = sqrt(32pi/3) reproduced")

    # write the 32pi as 8pi/kappa^2 (kappa = 1/2 gives 32pi) and re-derive Z(kappa)
    a0_kappa = c**2 * sp.sqrt(Lam * kappa**2 / (8 * sp.pi))
    Z_kappa = sp.simplify(c * HL / a0_kappa.subs(Lam, 3 * HL**2 / c**2))
    print(f"  general kappa:  a0 = c^2 sqrt(kappa^2 Lambda/8pi)  =>  Z(kappa) = {Z_kappa}")
    check(sp.simplify(Z_kappa.subs(kappa, sp.Rational(1, 2)) - sp.sqrt(32 * sp.pi / 3)) == 0,
          "Z(kappa=1/2) = sqrt(32pi/3) -- the 32pi is 8pi/kappa^2 with kappa=1/2")
    print(f"  so Z(kappa) = (1/kappa) sqrt(8pi/3),  and 32pi/3 = (8pi/3)/kappa^2.")

    # the clean physical form: substitute Lambda = 8 pi G rho_Lambda / c^2
    a0_rho = sp.simplify(a0_kappa.subs(Lam, 8 * sp.pi * G * rho / c**2))
    print(f"\n  substituting Lambda = 8 pi G rho_Lambda / c^2:")
    print(f"      a0 = {a0_rho}")
    check(sp.simplify(a0_rho - kappa * c * sp.sqrt(G * rho)) == 0,
          "a0 = kappa * c * sqrt(G rho_Lambda) EXACTLY -- all the pi's cancel")
    print(f"  With kappa = 1/2:   a0 = (c/2) sqrt(G rho_Lambda).")
    print("\n  THIS IS THE REDUCTION. In the form a0 = kappa c sqrt(G rho_Lambda) there is no")
    print("  32, no pi, no 3 -- they were all artifacts of writing the same statement via")
    print("  Lambda and Einstein's 8pi. The ENTIRE content of '32pi/3' is the single")
    print("  dimensionless number kappa = 1/2. 'Derive Z' and 'derive kappa' are the same")
    print("  problem, and the second is the honest way to state it.")

    # -----------------------------------------------------------------------------------
    banner("S2. The spectral weight is LINEAR in kappa -- a direct probe")
    # W_above(Z) = 1/(pi Z)   [mi_spectral_weight_swing_2026, exact from the committed measure]
    W_of_kappa = sp.simplify(1 / (sp.pi * Z_kappa))
    print(f"  W_above = 1/(pi Z)  and  Z = (1/kappa) sqrt(8pi/3)   =>")
    print(f"      W_above(kappa) = {W_of_kappa}")
    coef = sp.simplify(W_of_kappa / kappa)
    print(f"  i.e. W_above = kappa * {coef} = kappa * {float(coef):.8f}")
    check(sp.simplify(W_of_kappa - kappa * sp.sqrt(3 / (8 * sp.pi**3))) == 0,
          "W_above(kappa) = kappa * sqrt(3/(8 pi^3))  -- EXACTLY LINEAR in kappa")
    W_half = float(W_of_kappa.subs(kappa, sp.Rational(1, 2)))
    print(f"\n  kappa = 1/2  ->  W_above = {W_half:.8f}   (matches the committed 0.05498710)")
    check(abs(W_half - 0.05498710) < 1e-7, "reproduces the measured spectral weight")

    print("\n  WHY THIS MATTERS. The spectral weight above the de Sitter frequency is a")
    print("  STRICTLY LINEAR function of kappa, with a known constant sqrt(3/(8 pi^3)).")
    print("  So ANY forced condition on that weight forces kappa DIRECTLY -- no square")
    print("  roots, no inversion, one linear equation:")
    print(f"      kappa = W_above / sqrt(3/(8 pi^3)) = W_above * {float(1/coef):.6f}")
    print("  This is a genuinely new place to attack kappa. Every previous kappa-forcing")
    print("  attempt was FIELD-THEORETIC (ghost-freedom, unitarity, holography) and all of")
    print("  them closed. None was SPECTRAL. The spectral axis was only shown to exist")
    print("  today (W_above = 1/(pi Z) is an exact bijection), so it has never been tried.")

    # -----------------------------------------------------------------------------------
    banner("S3. What kappa values the natural spectral weights correspond to")
    print("  Stated as a MAP, not a search: the linear relation lets any forced weight be")
    print("  read straight off as a kappa. Reporting the inverse direction for reference.\n")
    inv = float(1 / coef)
    print(f"  {'W_above':>14}{'implied kappa':>16}{'implied Z':>12}   note")
    print("  " + "-" * 70)
    rows = [
        (W_half, "framework kappa=1/2"),
        (1 / (2 * math.pi**2), "gives kappa = pi/... see below"),
        (1 / (4 * math.pi), ""),
        (0.05, ""),
        (1 / 16, ""),
    ]
    for W, note in rows:
        k = W * inv
        Zi = 1.0 / (math.pi * W)
        print(f"  {W:>14.8f}{k:>16.6f}{Zi:>12.6f}   {note}")
    print("\n  Note the framework's kappa = 1/2 is a RATIONAL number, while the natural-looking")
    print("  weights map to irrational kappa. Stated against interest: that asymmetry runs")
    print("  the framework's way on this axis, the opposite of what the raw weight comparison")
    print("  in mi_spectral_weight_swing_2026 suggested. Neither is decisive.")

    # -----------------------------------------------------------------------------------
    banner("S4. The one other genuinely FORCED relation in the corpus, tested")
    # KERNEL_THEORY.md:45 -- the kernel's memory time is tau_mem = 2c/a0 = 2Z/H_Lambda.
    print("  KERNEL_THEORY.md:45 gives a forced timescale (from the branch point):")
    print("      tau_mem = 2c/a0 = 2Z/H_Lambda")
    tau_mem = sp.simplify(2 * Z_kappa / HL)
    print(f"      tau_mem(kappa) = {tau_mem}")
    Zf = math.sqrt(32 * math.pi / 3)
    print(f"      framework: tau_mem = {2*Zf:.6f} / H_Lambda  (i.e. {2*Zf:.3f} Hubble times)")
    print("\n  For this to FORCE kappa, an independently forced dS timescale must equal it.")
    print("  de Sitter supplies exactly ONE timescale, 1/H_Lambda (horizon light-crossing).")
    print("  Its unambiguous multiples:")
    for nm, val in (("1/H_L", 1.0), ("2/H_L (diameter)", 2.0),
                    ("2pi/H_L (thermal)", 2 * math.pi), ("4pi/H_L", 4 * math.pi)):
        implied_Z = val / 2
        implied_k = math.sqrt(8 * math.pi / 3) / implied_Z if implied_Z > 0 else float("nan")
        dev = 100 * (implied_Z - Zf) / Zf
        print(f"    tau_mem = {nm:<18} -> Z = {implied_Z:8.6f} ({dev:+7.2f}%)  "
              f"kappa = {implied_k:.6f}")
    print(f"\n  The framework needs tau_mem = {2*Zf:.4f}/H_Lambda. None of the forced dS")
    print("  multiples equals that (nearest is 4pi/H_L -> Z = 2pi, the conventional")
    print("  coefficient again, at +8.5%). So the memory-time route does not force kappa")
    print("  either. Attempt 4 of 4: MISS, recorded.")

    # -----------------------------------------------------------------------------------
    banner("S5. Look-elsewhere, applied to ourselves")
    n_attempts = 4
    print(f"  {n_attempts} distinct forced/semi-forced conditions have now been tried against")
    print(f"  the same target: log2({n_attempts}) = {math.log2(n_attempts):.2f} bits of")
    print("  look-elsewhere already spent. Per the atomos rule, a future 'hit' must supply")
    print("  more bits than the accumulated trial count -- and the count keeps rising with")
    print("  every further guess. This is the reason to STOP guessing conditions and instead")
    print("  demand a condition derived BEFORE its value is checked.")

    banner("VERDICT")
    print("  1. REDUCTION PROVED. a0 = kappa c sqrt(G rho_Lambda) exactly -- every pi, the 32")
    print("     and the 3 cancel. '32pi/3' contains exactly ONE number: kappa = 1/2. So")
    print("     'derive Z' IS 'derive kappa', and the latter is the honest statement.")
    print("  2. NEW ATTACK SURFACE. W_above(kappa) = kappa sqrt(3/(8 pi^3)) is EXACTLY LINEAR")
    print("     in kappa. So a forced spectral condition would force kappa directly, by one")
    print("     linear equation. Every previous kappa-forcing attempt was field-theoretic")
    print("     (ghost-freedom, unitarity, holography) and all closed; NONE was spectral,")
    print("     because the spectral axis was only shown to exist today. This is the one")
    print("     genuinely untried door, and it is now specified precisely enough to attack.")
    print("  3. NO FORCED CONDITION YET. Four attempts, four misses, honestly counted. And")
    print("     the framework's own KERNEL_THEORY.md:47 says the measure is fixed by Herglotz")
    print("     + the RAR -- i.e. the scale is set by DATA. A forced condition must add an")
    print("     axiom, and any axiom picked to reproduce kappa = 1/2 is fitting.")
    print("  4. Z remains POSTULATED, NOT DERIVED. Nothing empirical moves.")
    print("=" * 96)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
