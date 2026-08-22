#!/usr/bin/env python3
r"""A_eff = A_gg - A_gn A_nn^-1 A_ng : BOTH matrix elements, and the eps -> 0 check.

MY PREVIOUS COMMIT (8d7d9cab) CLAIMED: 'A_nn ~ eps A (c^4/a0^2) k^4, so the reduced
correction A_ngamma^2/A_nn carries 1/eps -- the indirect channel GROWS as eps shrinks.'
THAT IS WRONG.  It scaled A_nn only and implicitly held A_ngamma eps-independent.  Carl's
demand that the eps -> 0 limit be traced rather than accepted is exactly what exposes it.
"""
import sympy as sp
def head(t): print("\n"+"="*96+f"\n{t}\n"+"="*96)
eps,k,a,X0,al,A,LL=sp.symbols('epsilon k a X_0 alpha A L',positive=True)

head("A -- the two matrix elements, by origin")
print("  A_nn : n-n block.  Two sources:")
print("     (MOND/eta_K sector)  alpha k^2 ,  alpha = eta_K + F_X          [eps-INDEPENDENT]")
print("     (Y_a sector)         eps A (c^4/a0^2) k^4                       [O(eps)]")
print("  A_ng : n-gamma block.  Two sources:")
print("     (MOND sector) from (1/2)F_XX (dX)^2 with dX|_gamma = -X0 gamma_aa (NO derivs)")
print("                   and dX|_n = 2(c^4/a0^2) a.dn  ->  A^0_ng ~ F_XX X0 (c^4/a0^2) a k")
print("                                                                     [eps-INDEPENDENT]")
print("     (Y_a sector)  eps A (c^4/a0^2) (didj n)(d gamma . a)")
print("                                       ->  A^1_ng ~ eps A (c^4/a0^2) k^3 a   [O(eps)]")
Ann = al*k**2 + eps*A*LL**2*k**4          # LL^2 stands for c^4/a0^2
Ang0, Ang1 = sp.symbols('A0_ng A1_ng', positive=True)
Ang = Ang0 + eps*A*LL**2*k**3*a
head("B -- the correction, and its eps -> 0 and eps -> large limits")
corr = Ang**2/Ann
print(f"  correction = A_ng^2/A_nn")
lim0 = sp.limit(corr, eps, 0)
print(f"\n  eps -> 0 :  {sp.simplify(lim0)}")
print("     = the eps=0 KHRONOMETRIC value A^0_ng^2/(alpha k^2).  FINITE and smooth.")
print("     This is the known-safe baseline (its tensor effect is the mass |m| ~ a0/c^2,")
print("     observationally nil).  So there is NO 1/eps divergence -- my earlier claim fails")
print("     its own smoothness check, exactly as Carl predicted it would.")
print("\n  eps -> large (the LIGO regime, eps A (kL)^2 = 1.3e17 >> 1):")
big = sp.simplify(sp.limit(corr/eps, eps, sp.oo))
print(f"     correction/eps -> {big}")
print("     i.e. correction ~ eps * [A (c^4/a0^2) k^3 a]^2 / [A (c^4/a0^2) k^4]")
print("                     = eps A (c^4/a0^2) k^2 a^2")
print("     and a^2 = X0 a0^2/c^4, so   correction ~ eps A X0 k^2 .")
head("C -- compare with the GR gradient term k^2")
print("  ratio = eps A(X0) X0        -- IDENTICAL in form to the DIRECT term 2 eps A X0,")
print("  and with NO (k c^2/a0)^2 enhancement.")
print("\n  So in the k^4-dominated regime the indirect channel is the SAME ORDER as the")
print("  direct one, and scales as eps (not 1/eps).  The large A_nn that the k^4 term")
print("  produces SUPPRESSES the response n, and that suppression exactly compensates the")
print("  fact that the Y-sector also enlarges the mixing A_ng.")
head("D -- what is now established, and what is not")
for s in [
 "CORRECTED: the indirect channel does NOT carry 1/eps.  My commit 8d7d9cab said it did;",
 "  that came from scaling A_nn while holding A_ng fixed.  In the k^4-dominated regime the",
 "  dominant mixing is itself O(eps), and the two eps factors leave correction ~ eps A X0 k^2.",
 "PASSES Carl's smoothness test: eps -> 0 returns the finite khronometric value",
 "  A^0_ng^2/(alpha k^2), no divergence, no non-uniform limit to explain away.",
 "INDICATED (scaling only): H_T = 0 at this order -- the indirect channel produces a k^2",
 "  (gradient) contribution, not k^4, so it shifts c_T rather than creating dispersion.",
 "NOT ESTABLISHED: the O(1) coefficients, and whether A^0_ng and A^1_ng partially cancel.",
 "  A scaling argument already misled me once in this exact calculation.  H_T = 0 must come",
 "  from the explicit constraint elimination, which is running.  Until then the status Carl",
 "  set stands unchanged: Gen-2 GW UNDETERMINED.",
]: print("  [S]",s)
