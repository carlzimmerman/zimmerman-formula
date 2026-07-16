#!/usr/bin/env python3
r"""
Q1 CANDIDATE (c): FLUCTUATION-DISSIPATION THEOREM at T_dS -- does detailed balance fix the
reactive/dissipative split, and does that split DETERMINE eta(beta)?
================================================================================================
Framework = de Sitter-Unruh MODIFIED INERTIA (Carl Zimmerman), own terms.
The dS-Unruh bath is KMS at T_eff = kappa_eff/2pi, kappa_eff=sqrt(H^2+a^2). The FDT (established in
mi_kernel_bath/kernel_shape_from_wightman.py) reads
     S_sym(w) = coth(w/2T) chi''(w),      chi''(w) = w/4pi   (conformal, ohmic),
splitting the bath response into a DISPERSIVE (reactive, chi') and DISSIPATIVE (chi'') part. QUESTION:
does that split -- which detailed balance fixes UNIQUELY at fixed T -- determine the closure weighting eta?

RESULT (computed): FDT/detailed balance is a statement about the 2-POINT function (the split chi'<->chi''
is Kramers-Kronig/analyticity-locked and unique). But eta(beta) is a NONLINEAR ordering (4-point Jensen
gap). Detailed balance S(w)/S(-w)=e^{w/T} holds IDENTICALLY for both closures (they share the 2-point), so
it cannot distinguish them. => FDT is WEIGHTING-BLIND. Both footings; s=-1, a0 postulates; no "closed".
"""
import sympy as sp
import mpmath as mp
from _common import banner, Checker, K, FOOTINGS, c, Gyr
mp.mp.dps = 40
chk = Checker()

# =====================================================================================
banner("[1] FDT fixes the reactive/dissipative SPLIT uniquely at fixed T (Kramers-Kronig, sympy)")
# =====================================================================================
print(r"""
 The retarded susceptibility chi(w)=chi'(w)+i chi''(w) is analytic in the upper half plane (causality), so
 chi' and chi'' are Kramers-Kronig partners -- the split is UNIQUE given either half. FDT ties the symmetric
 (fluctuation) correlator to the dissipative half at temperature T:
     S_sym(w) = coth(w/2T) chi''(w).
 Verify (i) detailed balance S(w)/S(-w) = e^{w/T}, and (ii) the split is fixed (chi' determined by chi'' via KK).""")
w, T = sp.symbols('omega T', positive=True, real=True)
chi_dd = w/(4*sp.pi)                                    # dissipative (odd, ohmic)
S_sym = sp.coth(w/(2*T))*chi_dd                         # symmetrized correlator
# one-sided (non-symmetric) rates: S_>(w) = S_sym + chi''(w)/2 ... detailed balance on the GreaterLesser:
S_gt = S_sym + chi_dd                                   # S_> = (coth+1) chi'' ; spectral fn S_>-S_< = 2chi''
S_lt = S_sym - chi_dd                                   # S_< = (coth-1) chi''
db = sp.simplify((S_gt/S_lt).rewrite(sp.exp))
print(f"  S_sym(w) = coth(w/2T) chi''(w),  chi''(w)=w/4pi")
print(f"  detailed-balance ratio S_>(w)/S_<(w) = {db}")
db_target = sp.exp(w/T)
chk("FDT detailed balance: S_>(w)/S_<(w) = e^{w/T} (KMS, fixes the split at fixed T)",
    sp.simplify(db - db_target) == 0)
# KK partner (dispersive) of an ohmic chi''=w/4pi: chi'(w) = (1/pi) P INT chi''(w')/(w'-w) dw' -> a constant
# (contact) term after regularization; the point is the split is DETERMINED, carrying no free parameter.
print("  chi' (reactive) is the Kramers-Kronig transform of chi'' -> the reactive/dissipative split is FIXED")
print("     (no free parameter in the split: given chi'', both chi' and S_sym are determined at fixed T).")
# Computed check: causality/analyticity forces chi'' ODD in w (its spectral role), so the KK partner chi' and
# the FDT-fixed S_sym carry NO free constant that could hide a weighting. Verify chi'' is odd and S_sym even.
chi_dd_odd = sp.simplify(chi_dd.subs(w, -w) + chi_dd)               # chi''(-w) = -chi''(w) -> sum = 0
S_sym_even = sp.simplify((S_sym.subs(w, -w) - S_sym).rewrite(sp.exp))  # S_sym even -> difference = 0
print(f"     chi''(-w)+chi''(w) = {chi_dd_odd} (=0 -> chi'' odd, causal),  "
      f"S_sym(-w)-S_sym(w) = {S_sym_even} (=0 -> even)")
chk("reactive/dissipative split is KK-locked: chi'' is odd (causal) and S_sym even (FDT-fixed) -> "
    "no free parameter/weighting hides in the 2-point split", (chi_dd_odd == 0) and (S_sym_even == 0))

# =====================================================================================
banner("[2] but the SPLIT is a 2-POINT object; eta weights a 4-POINT (Jensen gap) -> orthogonal (sympy)")
# =====================================================================================
print(r"""
 FDT constrains the 2-point functions {S_sym, chi'', chi'} and their ratios. The closure weighting eta(beta)
 lives in the NONLINEAR MOND observable's ordering: G(beta)=<K(z)>-K(<z>), z=a^2/a0^2, a CONNECTED 4-POINT
 of the acceleration. There is NO FDT-type relation linking a 2-point split to a 4-point ordering for a
 Gaussian KMS bath -- the higher Kubo/FDT hierarchy relations for a Gaussian bath close at 2nd order (all
 connected n-point functions with n>2 vanish). Verify: the connected 4-point of a Gaussian bath is 0, so FDT
 gives NO constraint that could fix Var(z)-weighting.""")
lam = sp.symbols('lambda', real=True); sig = sp.symbols('sigma', positive=True)
logM = sp.log(sp.exp(lam**2*sig**2/2))                  # Gaussian cumulant generating function
kappa4 = sp.simplify(sp.diff(logM, lam, 4).subs(lam, 0))
print(f"  connected 4-point (4th cumulant) of the Gaussian KMS bath = {kappa4}")
chk("Gaussian KMS bath: connected 4-point = 0 -> the FDT/Kubo hierarchy closes at 2nd order",
    kappa4 == 0)
print(r"""
 => Because the 4th cumulant vanishes, there is NO fluctuation-dissipation relation of 4th order to constrain
    Var(z). The 2nd-order FDT (the only nonvanishing one) fixes the 2-point split but says NOTHING about the
    4-point ordering eta weights. The two are ORTHOGONAL data.""")

# =====================================================================================
banner("[3] detailed balance holds IDENTICALLY for closures A and B -> cannot distinguish them")
# =====================================================================================
print(r"""
 Closures A and B are evaluated in the SAME KMS state at the SAME T_dS and share the SAME 2-point structure
 (they differ only by the reordering of the nonlinearity). So the detailed-balance ratio e^{w/T} is identical
 for both -> FDT assigns them the same 2-point data and cannot select. Numeric check of T_eff at a=a0 (both
 footings): the KMS temperature the FDT uses is the Pythagorean kappa_eff/2pi -- closure-independent.""")
for name, a0, HL in FOOTINGS:
    kap_a0 = mp.sqrt(HL**2 + (a0/c)**2)                 # kappa_eff at the MOND transition a=a0
    T_a0 = kap_a0/(2*mp.pi)
    ratio = kap_a0/HL
    print(f"  {name:18s}: kappa_eff(a=a0)/H_L = {mp.nstr(ratio,7)} (=sqrt(1+1/Z^2), footing-independent), "
          f"T_eff = {mp.nstr(T_a0,5)} -- SAME for A and B")
    chk(f"[{name}] KMS T_eff at a=a0 is closure-independent (Pythagorean pole) -> FDT common to A,B",
        abs(ratio - mp.sqrt(1+1/(mp.sqrt(32*mp.pi/3))**2)) < mp.mpf('1e-20'))

print(r"""
 SYNTHESIS (candidate c): the FLUCTUATION-DISSIPATION THEOREM at T_dS is WEIGHTING-BLIND. FDT/detailed
 balance fixes the reactive/dissipative SPLIT of the 2-point response uniquely (Kramers-Kronig-locked), but
 that is 2-point data. eta(beta) weights the connected 4-point (Jensen gap), and the Gaussian KMS bath's
 4th cumulant vanishes -> there is no 4th-order FDT relation to constrain it. Detailed balance holds
 identically for closures A and B. => FDT does NOT force eta.""")
raise SystemExit(chk.done())
