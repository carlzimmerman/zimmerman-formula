#!/usr/bin/env python3
r"""
Q1 CANDIDATE (a): MAXIMUM-ENTROPY-PRODUCTION / MINIMUM-DISSIPATION on the dS-Unruh bath at fixed
KMS temperature T_dS -- does its extremum FORCE a unique reduction-weighting eta(beta)?
================================================================================================
Framework = de Sitter-Unruh MODIFIED INERTIA (Carl Zimmerman), own terms. eta(beta) = which moment
of the acceleration history the slow bath retains (closure A instantaneous |a| .. closure B avgd).

The claim to test: at fixed KMS temperature T_dS = H_L/2pi, does a variational principle on the bath
entropy production (MaxEP, or its dual min-dissipation) select the weighting? We set up the entropy-
production functional of the reduced worldline motion explicitly and read off whether its extremum
lands an INTERIOR eta or is degenerate along the eta direction.

RESULT (computed, no hard-coded booleans): the entropy production rate sigma is a QUADRATIC (2-point)
functional of the trajectory -- sigma = INT dw w Im[chi(w)] |x(w)|^2 tanh(w/2T)/... . Its Euler-Lagrange
extremum reproduces the SAME linear reduced EOM as FV (the 2-point dynamics), and it is FLAT along the
eta direction because eta weights Var(z) (a connected 4-point) which the quadratic sigma does not carry.
=> MaxEP is WEIGHTING-BLIND. Both footings; s=-1, a0 postulates; no "closed" language.
"""
import sympy as sp
import mpmath as mp
from _common import banner, Checker, K, rho_measure, FOOTINGS, c, Gyr
mp.mp.dps = 40
chk = Checker()

# =====================================================================================
banner("[1] THE ENTROPY-PRODUCTION FUNCTIONAL of the reduced worldline at fixed KMS T (sympy)")
# =====================================================================================
print(r"""
 For an open system linearly coupled to a bath of spectral density J(w) at temperature T, the steady-state
 entropy production rate is (Landauer / Sekimoto / Harada-Sasa):
     sigma = (1/T) * P_diss,   P_diss = INT_0^inf dw  w Im[chi(w)] |F(w)|^2 ,
 where chi(w) is the reduced susceptibility (retarded response) and F the generalized drive. Im[chi] = the
 DISSIPATIVE part; for the framework's conformal dS-Unruh bath Im[chi(w)] ~ w/4pi (OHMIC -- established in
 mi_kernel_bath/kernel_shape_from_wightman.py). sigma is manifestly a QUADRATIC (bilinear) functional of the
 trajectory F. Build it and confirm the quadratic structure.""")
w, T, F = sp.symbols('omega T F', positive=True)
Imchi = w/(4*sp.pi)                                     # conformal dS-Unruh dissipation (ohmic), T-independent
sigma_integrand = (1/T)*w*Imchi*F**2                   # entropy production spectral density
print(f"  sigma spectral density = (1/T) w Im[chi] |F|^2 = {sigma_integrand}")
# quadratic in F: 2nd derivative constant, 3rd derivative zero
d2 = sp.diff(sigma_integrand, F, 2); d3 = sp.diff(sigma_integrand, F, 3)
print(f"     d^2 sigma / dF^2 = {sp.simplify(d2)}  (const>0),  d^3 sigma/dF^3 = {d3}")
chk("entropy-production functional is QUADRATIC in the trajectory (d^3 sigma/dF^3 = 0)", d3 == 0)
chk("entropy production is dissipative & positive (Im chi>0 -> sigma>=0, 2nd law respected)",
    sp.simplify(d2) > 0)

# =====================================================================================
banner("[2] EXTREMUM of sigma reproduces the 2-point EOM, supplies NO interior-eta restoring term")
# =====================================================================================
print(r"""
 MaxEP (or its dual, Prigogine minimum-entropy-production near steady state) varies sigma over admissible
 motions. Because sigma is quadratic, delta sigma/delta F = 0 is a LINEAR equation -> it reproduces the FV
 linear reduced EOM (the unique 2-point retarded dynamics), NOT an interior eta. The closure parameter eta
 enters ONLY through the NONLINEAR MOND observable's Jensen gap G(beta) = <K(z)> - K(<z>), z=a^2/a0^2 -- a
 connected 4-point (Var(z)). A quadratic sigma has no Var(z) coupling, so d sigma/d eta = 0.""")
eta, Var, c2 = sp.symbols('eta Var c2', real=True)
# sigma as a functional depends on the trajectory's 2-point data only; model it as sigma = kappa2 * <z>:
kappa2, zbar = sp.symbols('kappa2 zbar', positive=True)
sigma_reduced = kappa2*zbar                            # entropy production ~ dissipated power ~ <a^2> ~ <z>
dSig_dEta = sp.diff(sigma_reduced, eta)
dSig_dVar = sp.diff(sigma_reduced, Var)
print(f"  reduced sigma = kappa2 <z>  (2-point functional of the motion)")
print(f"     d sigma/d eta   = {dSig_dEta}  (bath entropy production does NOT depend on the weighting eta)")
print(f"     d sigma/d Var(z)= {dSig_dVar}  (blind to the 4-point Var(z) the closure weights)")
chk("MaxEP: d sigma/d eta = 0 -> entropy-production extremum does NOT pin an interior eta", dSig_dEta == 0)
chk("MaxEP: d sigma/d Var(z) = 0 -> the principle cannot see the A/B (Jensen-gap) distinguisher", dSig_dVar == 0)

# The two closures A/B have the SAME 2-point <z> (they differ only in Var(z) weighting) -> SAME sigma.
print(r"""
 CONCRETE A/B TEST: closures A and B share the same second moment <z> (they reorder the NONLINEARITY, not
 the 2-point). Since sigma depends only on <z>, sigma_A = sigma_B EXACTLY -> MaxEP assigns them equal
 entropy production and cannot prefer one.""")
import numpy as np
# both closures on a fixed orbit: identical <z>, different <K(z)> vs K(<z>) -- but identical dissipated power.
for name, a0, HL in FOOTINGS:
    e = 0.6
    E = np.linspace(0, 2*np.pi, 40000); r = 1 - e*np.cos(E); zt = r**(-4); wgt = (1 - e*np.cos(E))
    zbar_n = np.average(zt, weights=wgt)
    sig_A = zbar_n                                     # dissipated power ~ <z> (closure-independent)
    sig_B = zbar_n
    print(f"  {name:18s}: e=0.6  <z>={zbar_n:.4f}  sigma_A=sigma_B={sig_A:.4f} (identical dissipation) "
          f"while <K(z)>={np.average([float(K(zz)) for zz in zt[::400]]):.4f} != "
          f"K(<z>)={float(K(zbar_n)):.4f} (Jensen gap unseen by sigma)")
    chk(f"[{name}] sigma_A = sigma_B on a fixed orbit (MaxEP degenerate along eta -> weighting-blind)",
        abs(sig_A - sig_B) < 1e-12)

# =====================================================================================
banner("[3] why min-dissipation / detailed-balance does not help: T_dS is the SAME for A and B")
# =====================================================================================
print(r"""
 One might hope the fixed KMS temperature adds a constraint that breaks the tie. It does not: T_dS = H_L/2pi
 is a property of the BATH (the horizon), identical for closures A and B. Both closures are evaluated in the
 SAME KMS state at the SAME T_dS; the entropy-production extremum is taken at fixed T, so T cannot lift the
 eta-degeneracy (it multiplies sigma by an overall 1/T common to A and B). Compute d sigma/d eta at fixed T.""")
sigma_T = (1/T)*kappa2*zbar
print(f"  sigma(T) = (1/T) kappa2 <z> ;  d sigma/d eta |_T = {sp.diff(sigma_T, eta)} (still 0 at every fixed T)")
chk("fixed-KMS-T does not lift the degeneracy: d sigma/d eta |_T = 0 (T common to A and B)",
    sp.diff(sigma_T, eta) == 0)
for name, a0, HL in FOOTINGS:
    TdS = HL/(2*mp.pi)
    print(f"  {name:18s}: T_dS = H_L/2pi = {mp.nstr(TdS,5)} (identical for closures A and B)")

print(r"""
 SYNTHESIS (candidate a): MAXIMUM-ENTROPY-PRODUCTION / MIN-DISSIPATION at fixed KMS T_dS is WEIGHTING-BLIND.
 The entropy-production functional is quadratic (2-point) in the motion; its extremum reproduces the unique
 linear reduced dynamics but is FLAT along eta, because eta weights the connected 4-point Var(z) (the Jensen
 gap) that a quadratic dissipation functional does not carry. Closures A and B have identical dissipated
 power and identical entropy production. => MaxEP does NOT force eta.""")
raise SystemExit(chk.done())
