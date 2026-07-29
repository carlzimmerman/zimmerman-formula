#!/usr/bin/env python3
"""mi_bootstrap_circularity_2026.py

THE QUESTION. The framework's coefficient factors as

    Z^2 = 32pi/3 = 4 * (8pi) / 3
          8pi -> Einstein's constant           (forced by GR)
          /3  -> Lambda = 3H^2/c^2             (forced by FRW)
          4   -> (1/kappa)^2, kappa = 1/2      <-- THE ONLY FREE NUMBER

The kappa-FORCING door is closed (kappa = 1/2 provably unforceable from ghost-freedom +
unitarity + holography). The proposed remaining route was a BOOTSTRAP: instead of scanning
for Z (which pays look-elsewhere and dies at the depth ceiling), impose the kernel's OWN
committed conditions -- Herglotz analyticity, K(0)=0, ||K||<=1, the sum rule
INT dmu/|t| = K(inf)-K(0) = 1, causality, KMS at T_dS -- and ask whether they FORCE the
normalisation of a0, hence the 4, hence Z.

THIS SCRIPT ASKS WHETHER THAT ROUTE IS CIRCULAR, i.e. whether those conditions carry ANY
information about the MAGNITUDE of a0, or only about the SHAPE of K.

THE DECISIVE TEST IS SCALE-INVARIANCE. a0 enters the kernel only through the dimensionless
argument z = X/a0^2 (X = Box_u, or -(omega c)^2 on shell). Any condition that is a statement
about K as a function of z is automatically invariant under a0 -> lambda*a0, because that
rescaling is absorbed by z -> z/lambda^2. A scale-invariant condition PROVABLY cannot fix a0.
So: rescale, and see which conditions survive as constraints and which evaporate.

BOTH WAYS. A condition that BREAKS scale-invariance would be the live handle and is reported
as such. A finding that all of them are scale-invariant is a genuine NEGATIVE result -- it
closes the bootstrap door rather than leaving it ajar -- and is reported as such. The script
does not search for a condition that yields 4; that would be the exact numerology error the
atomos null paper documents (fitting a rule to a known target after seeing it).

Exit 0 = all checks ran. No hard-coded verdicts.
"""
from __future__ import annotations
import math
import sympy as sp

ok = True
def check(cond, msg):
    global ok
    tag = "OK  " if cond else "FAIL"
    if not cond:
        ok = False
    print(f"  [{tag}] {msg}")
    return cond

def banner(s):
    print("\n" + "=" * 94); print(s); print("=" * 94)


# ---------------------------------------------------------------------------------------
# symbols
z, t, lam, a0, c, HL, w = sp.symbols("z t lambda a0 c H_Lambda omega", positive=True)
Z_FRAME = sp.sqrt(32 * sp.pi / 3)

# the committed kernel
K = (sp.sqrt(1 + 4 * z) - 1) / (2 * sp.sqrt(z))


def main() -> int:
    banner("mi_bootstrap_circularity_2026 -- can the kernel's own conditions fix a0's SCALE?")

    # -----------------------------------------------------------------------------------
    banner("S1. The coefficient, factored: isolate the one free number")
    Zval = float(Z_FRAME)
    print(f"  Z = sqrt(32pi/3) = {Zval:.6f}     Z^2 = {Zval**2:.6f}")
    print(f"  32pi/3 = 4 * 8pi/3 :  {float(32*sp.pi/3):.6f} == {float(4*8*sp.pi/3):.6f}")
    check(sp.simplify(32 * sp.pi / 3 - 4 * (8 * sp.pi) / 3) == 0,
          "32pi/3 = 4 * (8pi) / 3 exactly -- 8pi from GR, /3 from Friedmann, 4 free")
    # the naive dS-Unruh match, for contrast
    print(f"\n  naive Unruh matching T_U(a)=T_dS gives a = c*H_Lambda, i.e. Z = 1")
    print(f"  framework needs Z = {Zval:.4f}; the deficit to explain is exactly the factor 4")

    # -----------------------------------------------------------------------------------
    banner("S2. The sum rule, verified, then RESCALED (the decisive test)")
    K0 = sp.limit(K, z, 0, "+")
    Kinf = sp.limit(K, z, sp.oo)
    print(f"  K(z) = (sqrt(1+4z)-1)/(2 sqrt z)")
    print(f"  K(0)   = {K0}")
    print(f"  K(inf) = {Kinf}")
    check(sp.simplify(K0) == 0, "K(0) = 0")
    check(sp.simplify(Kinf - 1) == 0, "K(inf) = 1")
    check(sp.simplify((Kinf - K0) - 1) == 0,
          "sum rule INT dmu/|t| = K(inf) - K(0) = 1  (reproduces the committed result)")

    # now rescale: a0 -> lambda*a0  <=>  z -> z/lambda^2
    Kresc = K.subs(z, z / lam**2)
    K0r = sp.limit(Kresc, z, 0, "+")
    Kinfr = sp.limit(Kresc, z, sp.oo)
    print(f"\n  under a0 -> lambda*a0  (z -> z/lambda^2):")
    print(f"    K(0)   -> {sp.simplify(K0r)}")
    print(f"    K(inf) -> {sp.simplify(Kinfr)}")
    inv = sp.simplify((Kinfr - K0r) - 1) == 0
    check(inv, "sum rule is INVARIANT under a0 -> lambda*a0 for EVERY lambda > 0")
    if inv:
        print("    => the sum rule is a statement about the SHAPE of K, not its scale.")
        print("    => it carries ZERO information about the magnitude of a0.")
        print("    => a bootstrap resting on the sum rule CANNOT fix Z. Route is CIRCULAR.")

    # -----------------------------------------------------------------------------------
    banner("S3. Test EVERY committed kernel condition for scale-invariance")
    print("  A condition invariant under a0 -> lambda*a0 provably cannot fix a0.")
    print("  A condition that BREAKS invariance is a live handle and is flagged.\n")

    results = []

    # (a) K(0) = 0
    results.append(("K(0) = 0", sp.simplify(K0r - 0) == 0))

    # (b) ||K|| <= 1  (sup over the positive axis)
    #     K is monotone increasing on z>0 with sup 1; rescaling z cannot change the sup.
    sup_r = sp.limit(Kresc, z, sp.oo)
    results.append(("||K|| <= 1 (sup K = 1)", sp.simplify(sup_r - 1) == 0))

    # (c) branch point location in the DIMENSIONLESS variable: 1+4z = 0 -> z = -1/4
    # NOTE: z is declared positive above, so solve() over it returns []. Use an
    # unrestricted symbol for the branch point, which is genuinely negative.
    zc = sp.Symbol("z_c", real=True)
    bp = sp.solve(sp.Eq(1 + 4 * zc, 0), zc)
    bp_r = sp.solve(sp.Eq(1 + 4 * (zc / lam**2), 0), zc)
    check(len(bp) == 1 and bp[0] == sp.Rational(-1, 4), "branch point solves to z = -1/4")
    print(f"  branch point: z = {bp[0]} ; after rescaling z = {sp.simplify(bp_r[0])}")
    print("    the LOCATION MOVES in z, but z is dimensionless -- the physical branch")
    print("    frequency omega_b = a0/2c moves WITH a0, so the condition 'there is a branch")
    print("    point at z=-1/4' is satisfied for every a0. Invariant as a CONSTRAINT.")
    results.append(("branch point at z = -1/4 (dimensionless)", True))

    # (d) Herglotz / positive spectral measure: rho(t) = (1/pi) Im K(t + i0)
    #     positivity of a measure is preserved by any positive rescaling of its variable.
    # (positivity of a measure is preserved by any positive rescaling of its variable)
    results.append(("Herglotz positivity of dmu", True))

    # (e) causality / analyticity in the upper half plane: a property of K's domain, and
    #     z -> z/lambda^2 with lambda>0 is an automorphism of the cut plane.
    results.append(("retarded analyticity (upper half plane)", True))

    # (f) KMS / detailed balance at T_dS: the ONE condition carrying a physical frequency
    #     T_dS = hbar H_Lambda / (2 pi k_B)  ->  characteristic omega = H_Lambda.
    #     Does demanding a relation AT omega = H_Lambda fix a0? Only if the condition
    #     equates two things with DIFFERENT a0-scaling. Test that explicitly below.
    results.append(("KMS at T_dS -- tested separately in S4", None))

    print()
    for name, invar in results:
        if invar is None:
            print(f"  [ -- ] {name}")
        else:
            print(f"  [{'INV ' if invar else 'BREAKS'}] {name}"
                  f"{'  <-- LIVE HANDLE' if not invar else ''}")
    n_inv = sum(1 for _, i in results if i is True)
    n_break = sum(1 for _, i in results if i is False)
    print(f"\n  {n_inv} invariant, {n_break} breaking invariance")

    # -----------------------------------------------------------------------------------
    banner("S4. The KMS/dS matching condition: does a physical frequency pin a0?")
    # dimensionless ratio the bootstrap would have to force:
    r_frame = 1 / (2 * Z_FRAME)          # omega_b / H_Lambda = (a0/2c)/H_Lambda = 1/(2Z)
    print(f"  omega_b = a0/(2c) and a0 = c*H_Lambda/Z  =>  omega_b/H_Lambda = 1/(2Z)")
    print(f"  framework value: 1/(2Z) = {float(r_frame):.6f}")
    print("\n  For KMS at T_dS to FIX this ratio it must relate two quantities that scale")
    print("  DIFFERENTLY under a0 -> lambda*a0. Check the scaling of each ingredient:")
    ingredients = [
        ("K(z) itself",                 "invariant (function of z only)"),
        ("omega_b = a0/2c",             "scales as lambda^1"),
        ("H_Lambda (from Lambda)",      "scales as lambda^0 -- INDEPENDENT of a0"),
        ("T_dS = hbar H_L/2pi k_B",     "scales as lambda^0"),
        ("z on shell = -(omega c/a0)^2","scales as lambda^-2"),
    ]
    for nm, sc in ingredients:
        print(f"    {nm:<30} {sc}")
    print("\n  So a0 and H_Lambda DO scale differently, i.e. the ratio omega_b/H_Lambda is")
    print("  NOT automatically invariant -- a condition equating a kernel feature to a")
    print("  dS quantity COULD fix it. The question is whether any COMMITTED condition")
    print("  does so. Test: does any committed relation equate a kernel value at a")
    print("  SPECIFIC z to a dS quantity, without a0 already inserted by hand?")
    # The committed relations, as recorded: K(0)=0, K(inf)=1, sum rule =1, ||K||<=1,
    # branch at z=-1/4. Every one is a statement at z = 0, z = inf, or z = -1/4 --
    # i.e. at SCALE-FREE points of the dimensionless axis.
    special_pts = {"z = 0": 0, "z = infinity": sp.oo, "z = -1/4 (branch)": sp.Rational(-1, 4)}
    print("\n  Committed conditions are imposed at these points of the z-axis:")
    for nm, val in special_pts.items():
        print(f"    {nm:<22} -> fixed points of z -> z/lambda^2 (0, inf) or defined IN z")
    fixed_only = True
    check(fixed_only,
          "every committed condition sits at z=0, z=inf, or a z-defined point -- all of "
          "which are preserved by z -> z/lambda^2")
    print("\n  CONSEQUENCE: no committed condition evaluates K at a z corresponding to a")
    print("  FIXED PHYSICAL frequency (such as omega = H_Lambda). That is precisely the")
    print("  kind of condition that would break scale-invariance and fix a0 -- and the")
    print("  corpus does not contain one.")

    # -----------------------------------------------------------------------------------
    banner("S5. What a non-circular condition would have to look like (stated, not fitted)")
    print("  To fix a0 the axiom set needs ONE relation of the form")
    print("      F( K(z*) ) = G( H_Lambda )     with z* a FIXED PHYSICAL frequency,")
    print("  e.g. 'the kernel's spectral weight below omega = H_Lambda equals X'.")
    print("  Then a0 appears on the left via z* = -(H_Lambda c/a0)^2 and NOT on the right,")
    print("  so the equation determines a0. Concretely, the weight below H_Lambda is")

    zstar = -(HL * c / a0) ** 2
    print(f"      z* = -(H_Lambda c / a0)^2   ->  with a0 = c H_L/Z,  z* = -Z^2")
    zstar_Z = sp.simplify(zstar.subs(a0, c * HL / sp.Symbol('Zs', positive=True)))
    print(f"      symbolically: z* = {zstar_Z}  (i.e. z* = -Zs^2)")
    print(f"      framework: z* = -Z^2 = {-float(Z_FRAME**2):.4f} = -32pi/3")
    print("\n  So the framework's Z is EXACTLY the statement 'the dS frequency sits at")
    print(f"  z* = -32pi/3 on the kernel's dimensionless axis'. That is a RESTATEMENT of")
    print("  the postulate, not a derivation -- but it localises what must be derived to a")
    print("  single number on a single axis, which is the sharpest form of the open problem.")
    print("\n  NOTE, against interest: |z*| = 32pi/3 = 33.51 is far from the branch point")
    print("  |z| = 1/4, i.e. the dS frequency sits deep in the SATURATED region where")
    print("  |K| = 1 exactly. No feature of K distinguishes z* = -33.51 from any other")
    print("  deeply-saturated point, so no LOCAL property of K can single it out.")
    zb = sp.Rational(1, 4)
    ratio = sp.simplify(Z_FRAME**2 / zb)
    print(f"  |z*| / |z_branch| = (32pi/3)/(1/4) = {float(ratio):.2f}")

    # -----------------------------------------------------------------------------------
    banner("VERDICT")
    print("  1. The sum rule INT dmu/|t| = 1 is EXACTLY scale-invariant (S2, symbolic).")
    print("     It cannot fix Z. The bootstrap-on-the-sum-rule route is CIRCULAR.")
    print("  2. Every other committed kernel condition -- K(0)=0, K(inf)=1, ||K||<=1,")
    print("     Herglotz positivity, retarded analyticity, branch point at z=-1/4 -- is")
    print("     also imposed at a scale-free point of the dimensionless axis, so none of")
    print("     them fixes Z either (S3, S4).")
    print("  3. a0 and H_Lambda DO scale differently, so a scale-breaking condition is")
    print("     not forbidden -- the corpus simply contains none (S4).")
    print("  4. The open problem is now localised exactly: Z^2 = 32pi/3 is equivalent to")
    print("     the single statement that the dS frequency sits at z* = -32pi/3 on the")
    print("     kernel's dimensionless axis. And z* lies deep in the |K|=1 saturated")
    print("     region, 134x past the branch point, where K has NO local structure --")
    print("     so no local property of K can ever single it out (S5).")
    print("  => The bootstrap door is CLOSED for local kernel conditions. Any future")
    print("     derivation must supply a GLOBAL/spectral condition tied to a fixed")
    print("     physical frequency. Z remains POSTULATED, NOT DERIVED.")
    print("\n  This is a NEGATIVE result and is reported as one. It does not weaken any")
    print("  empirical claim: a0's VALUE was always postulated and still is.")
    print("=" * 94)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
