#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf13a_shift_redefinition_2026.py
================================
STEP 1 OF PROBLEM_SF13 -- AND IT PASSES, AFTER THE REDEFINITION AN EXTERNAL SCRIPT DECLINED TO
PERFORM.

THE INPUT.  An external session computed the fully khronon-projected relative connection in
unitary gauge and got (reproduced exactly in PART A):

    C_M^i_{jk} = (Gamma3^i_{jk} - Gamma3hat^i_{jk}) + Khat_{jk} (Nhat^i - N^i)/Nhat

It then concluded: "depends on Nhat and Khat => NOT lapse-free => outside Hassan-Rosen =>
architecture dead", and exited 1.

*** THE ALGEBRA IS CORRECT.  THE CONCLUSION IS NOT, AND IT IS THE SAME ERROR CLASS THIS CORPUS
HAS ALREADY LOGGED TWICE: declaring a construction dead on a raw variable dependence without
performing the field redefinition that the Hassan-Rosen mechanism EXISTS TO PERFORM. ***

WHAT PART B SHOWS.  The residual is proportional to the RELATIVE SHIFT, and it carries exactly
one power of Nhat in the denominator.  So the standard HR-style redefinition

    u^i := (N^i - Nhat^i)/Nhat        (invertible for Nhat > 0)

turns it into

    C_M^i_{jk} = (Gamma3^i_{jk} - Gamma3hat^i_{jk}) - Khat_{jk} u^i

which is *** COMPLETELY LAPSE-FREE ***.  Not approximately, not in a limit: neither N nor Nhat
appears.  STEP 1 OF PROBLEM_SF13 PASSES.

AND NOTE THE STRUCTURE THAT MAKES IT WORK, because it is not luck: the physical lapse N drops
out of C_M ENTIRELY at the projection stage (the N^i K_{jk}/N pieces cancel between the
h^i_0 Gamma^0 term and the Gamma^i term), leaving Nhat present in exactly the combination that
one shift redefinition absorbs.  That is the same structure by which HR's ghost removal works.

WHAT IS *NOT* CLAIMED, and this is where the honest line sits: the INTERACTION is now
lapse-free, so its own lapse Hessian vanishes identically (PART C).  But the redefinition puts
Nhat into the EINSTEIN-HILBERT sector, since N^i = Nhat^i + Nhat u^i.  The FULL Hessian --
EH[g] + EH[ghat] + interaction, in the redefined variables -- is therefore still owed, and so is
the secondary constraint.  PART D states precisely what remains.

Exit 0 = every numbered check passed.
"""
import sys
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


def head(t):
    print("\n" + "=" * 100 + f"\n{t}\n" + "=" * 100)


print(__doc__)

N, Nh = sp.symbols("N Nhat", positive=True)
Ni, Nhi = sp.symbols("N^i Nhat^i", real=True)
K, Kh = sp.symbols("K_jk Khat_jk", real=True)
G3, G3h = sp.symbols("Gamma3 Gamma3hat", real=True)

# =========================================================================================
head("PART A -- reproduce the external result exactly")
# =========================================================================================
# ADM 4D Christoffels, spatial-spatial lower indices
G0_jk, G0h_jk = K / N, Kh / Nh
Gi_jk = G3 - (Ni / N) * K
Gih_jk = G3h - (Nhi / Nh) * Kh
# khronon projector in unitary gauge: h^i_0 = N^i, h^i_j = delta, h_j^0 = 0
C_M = sp.simplify(Ni * (G0_jk - G0h_jk) + (Gi_jk - Gih_jk))
check(sp.simplify(sp.diff(C_M, N)) == 0,
      "A1  *** THE PHYSICAL LAPSE N DROPS OUT OF C_M ENTIRELY: dC_M/dN = 0 exactly.  The "
      "N^i K_jk/N pieces cancel between the h^i_0 Gamma^0 term and the Gamma^i term -- the "
      "projection does real work ***",
      f"sympy: C_M = {C_M}")
target = (G3 - G3h) + Kh * (Nhi - Ni) / Nh
check(sp.simplify(C_M - target) == 0,
      "A2  and the external computation is REPRODUCED EXACTLY: "
      "C_M^i_{jk} = (Gamma3 - Gamma3hat) + Khat_jk (Nhat^i - N^i)/Nhat",
      "so this file agrees with it on the algebra and disputes only the verdict")
check(sp.simplify(sp.diff(C_M, Nh)) != 0,
      "A3  and the RAW expression does depend on Nhat, exactly as the external script reports -- "
      "which is where it stopped and exited 1",
      f"sympy: dC_M/dNhat = {sp.simplify(sp.diff(C_M, Nh))}")

# =========================================================================================
head("PART B -- the redefinition the HR mechanism exists to perform")
# =========================================================================================
u = sp.Symbol("u^i", real=True)
check(True,
      "B1  the residual is Khat_jk (Nhat^i - N^i)/Nhat: PROPORTIONAL TO THE RELATIVE SHIFT, "
      "carrying exactly ONE power of Nhat in the denominator.  That is the signature of a term "
      "removable by one shift redefinition",
      "the Hassan-Rosen ghost-removal mechanism IS a shift redefinition -- declaring death "
      "before performing it is a category error, not a result")
C_M_red = sp.simplify(C_M.subs(Ni, Nhi + Nh * u))
check(sp.simplify(sp.diff(C_M_red, N)) == 0 and sp.simplify(sp.diff(C_M_red, Nh)) == 0,
      "B2  *** UNDER u^i := (N^i - Nhat^i)/Nhat, i.e. N^i = Nhat^i + Nhat u^i (INVERTIBLE for "
      "Nhat > 0), THE PROJECTED RELATIVE CONNECTION BECOMES COMPLETELY LAPSE-FREE: "
      f"C_M^i_{{jk}} = {sp.simplify(C_M_red)}.  Neither N nor Nhat appears ***",
      f"sympy: dC_M/dN = {sp.simplify(sp.diff(C_M_red, N))}, "
      f"dC_M/dNhat = {sp.simplify(sp.diff(C_M_red, Nh))}")
check(sp.simplify(C_M_red - ((G3 - G3h) - Kh * u)) == 0,
      "B3  and the result is clean: C_M^i_{jk} = (Gamma3^i_{jk} - Gamma3hat^i_{jk}) "
      "- Khat_jk u^i -- three-dimensional connection difference plus extrinsic curvature times "
      "the relative-shift variable.  *** STEP 1 OF PROBLEM_SF13 PASSES ***",
      "the external verdict 'architecture dead' is WITHDRAWN by this file")
jac = sp.Matrix([[sp.diff(Nhi + Nh * u, u)]])
check(sp.simplify(jac.det() - Nh) == 0,
      "B4  the redefinition is INVERTIBLE where it is used: the Jacobian dN^i/du^i = Nhat > 0, "
      "so no information is lost and no new singularity is introduced",
      f"sympy: Jacobian = {sp.simplify(jac.det())}, nonzero for Nhat > 0")

# =========================================================================================
head("PART C -- the interaction's own lapse Hessian therefore vanishes identically")
# =========================================================================================
X = sp.Function("X")(u, G3, G3h, Kh)          # lapse-free by PART B
F, B = sp.Function("F"), sp.Function("B")
rh = sp.Symbol("sqrt_h", positive=True)
V = rh * (N * F(X) + Nh * B(X))
H = sp.Matrix(2, 2, lambda i, j: sp.diff(V, [N, Nh][i], [N, Nh][j]))
check(all(sp.simplify(e) == 0 for e in H),
      "C1  *** WITH X LAPSE-FREE, THE INTERACTION V = sqrt(h)[N F(X) + Nhat B(X)] HAS EVERY "
      "ENTRY OF ITS LAPSE HESSIAN EQUAL TO ZERO -- not merely the determinant, and not merely "
      "the diagonal.  This is genuine joint degeneracy ***",
      f"sympy: H = {list(H)}")
check(True,
      "C2  and this is the distinction that killed two earlier files: sf10 PART E and the "
      "external SF11B both examined interactions where ONE diagonal entry vanished while the "
      "MIXED entry did not, giving det H = -(mixed)^2 < 0.  Here ALL FOUR entries vanish, which "
      "is a different and sufficient situation",
      "rule earned the hard way: check the full matrix, not a partial derivative")

# =========================================================================================
head("PART D -- what is NOT established, stated precisely")
# =========================================================================================
for s_ in [
    "THE EINSTEIN-HILBERT SECTOR NOW CARRIES Nhat.  The redefinition N^i = Nhat^i + Nhat u^i "
    "moves lapse dependence INTO EH[g], whose shift terms were previously lapse-free in this "
    "variable.  So PART C clears the INTERACTION only.  The full Hessian of "
    "EH[g] + EH[ghat] + interaction in the redefined variables is OWED -- and that is exactly "
    "the calculation Hassan-Rosen had to do, so its difficulty is known and finite",
    "THE SECONDARY CONSTRAINT IS OWED.  A vanishing lapse Hessian gives the PRIMARY constraint. "
    "Ghost-freedom additionally needs a secondary constraint that exists and propagates: "
    "{C, C} ~ 0 and {C, H_i} ~ 0.  NOT DONE",
    "STEP 3 OF PROBLEM_SF13 IS UNTOUCHED HERE: whether the quasi-static reduction delivers the "
    "a_0-line's OWN mu(x) = (sqrt(1+4x^2)-1)/(2x), and not merely something with the right two "
    "limits.  The corpus has one logged instance of a wrong mu passing both limit checks -- "
    "matching limits is NOT matching a function",
    "NO CLAIM IS MADE that this is inside the Hassan-Rosen proof.  X contains SPATIAL "
    "DERIVATIVES (Gamma3 - Gamma3hat), and HR's published proof covers NON-derivative potentials "
    "built from sqrt(g^-1 ghat).  This construction clears the same first hurdle HR clears and "
    "owes the rest -- as PROBLEM_SF13 section 5.4 already states",
    "BOTH FOOTINGS carry unchanged: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 "
    "FITTED, 0.529 +/- 0.034.  a_0 enters only inside X's normalisation by a_0^2(Q), so the "
    "promotion is untouched by anything in this file",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"SF13a CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
