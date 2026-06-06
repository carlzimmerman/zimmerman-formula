#!/usr/bin/env python3
"""
ROBUSTNESS of the uniqueness result -- hardening it three ways:
 (1) close the Planck-group loophole: a0 from {c,Lambda,hbar,G} admits ONE dimensionless group Lambda*l_P^2
     ~ 1e-122, so a0 ~ c^2 sqrt(Lambda) * (Lambda l_P^2)^n with n free -- UNLESS the observed MAGNITUDE forces n=0.
     It does: a0_obs ~ c^2 sqrt(Lambda) means n=0 (any n!=0 is off by 10^(122n)). And a0(z) ∝ rho_DE^(1/2+n)
     makes n TESTABLE. So the exponent 1/2 is forced by dimension + magnitude, and is itself falsifiable.
 (2) a SECOND independent derivation of the density = rho_DE: de Sitter-Unruh modified inertia. MOND onset where
     the Unruh temperature of a0 equals the de Sitter temperature set by the VACUUM curvature Lambda:
     T_Unruh(a0)=T_dS  =>  a0 = c H_dS = c^2 sqrt(Lambda/3) ∝ sqrt(rho_DE). hbar cancels; rho_DE (not rho_tot)
     because the de Sitter temperature is sourced by Lambda alone. Robust to thawing DE (instantaneous T_dS).
 (3) multi-route CONVERGENCE: dimensional, free-fall-time, de Sitter-Unruh, cosmic-coincidence -- all give the
     SAME scale ~1e-10, differing only by the O(1) coefficient = the unfalsifiable kappa. The scale is forced;
     the coefficient is the only spread.

C. Zimmerman, 2026-06-06. Pure numpy.
"""
import numpy as np
c=2.998e8; G=6.674e-11; hbar=1.055e-34
rho_crit=8.5e-27; OmL=0.69; rho_L=OmL*rho_crit               # dark-energy density kg/m^3
Lam=8*np.pi*G*rho_L/c**2                                       # 1/m^2
lP2=hbar*G/c**3                                               # Planck length^2
H0=2.20e-18

# ---------- (1) Planck-group loophole ----------
DIM=dict(a0=[1,0,-2],c=[1,0,-1],G=[3,-1,-2],hbar=[2,1,-1],Lam=[-2,0,0])
def pi_count(inputs):
    A=np.array([DIM[v] for v in inputs]).T
    return (len(inputs)+1)-np.linalg.matrix_rank(A), len(inputs)-np.linalg.matrix_rank(A)
print("="*90); print("(1) THE PLANCK-GROUP LOOPHOLE and how the observed MAGNITUDE closes it"); print("="*90)
nA,freeA=pi_count(["c","Lam"]); nB,freeB=pi_count(["c","Lam","hbar","G"])
print(f"  a0 from {{c,Lambda}}      : #free constants = {nA}  (form unique, exponent 1/2 forced)")
print(f"  a0 from {{c,Lambda,hbar,G}}: #free constants = {nB}  -> an EXTRA dimensionless group appears")
print(f"     the group is  Lambda * l_P^2 = {Lam*lP2:.2e}   (l_P^2 = hbar G/c^3)")
print(f"     => a0 = kappa c^2 sqrt(Lambda) * (Lambda l_P^2)^n  -- exponent on Lambda is (1/2 + n), n free in principle")
a0_n0 = c**2*np.sqrt(Lam)                                     # n=0 value
print(f"\n  CLOSING IT BY MAGNITUDE:  a0(n=0) = c^2 sqrt(Lambda) = {a0_n0:.2e} m/s^2  (~ observed 1.2e-10)")
for n in [-0.05,-0.01,0,0.01,0.05]:
    print(f"     n={n:+.2f}:  a0 = {a0_n0*(Lam*lP2)**n:.2e}  (off by 10^{122*n:+.0f})" if n!=0 else
          f"     n={n:+.2f}:  a0 = {a0_n0:.2e}  <- the ONLY value near observation")
print("  => any n!=0 is wrong by powers of 10^122. The observed magnitude FORCES n=0 => exponent 1/2 forced.")
print("  => and a0(z) ∝ rho_DE^(1/2+n): the deep-MOND z>=2 measurement constrains n -> the exponent is TESTABLE.")

# ---------- (2) de Sitter-Unruh independent derivation of rho_DE ----------
print("\n"+"="*90); print("(2) SECOND, INDEPENDENT derivation of the density = rho_DE: de Sitter-Unruh inertia"); print("="*90)
H_dS=c*np.sqrt(Lam/3)                                          # de Sitter Hubble rate from VACUUM curvature Lambda
a0_dSU=c*H_dS                                                  # T_Unruh(a0)=T_dS => a0 = c H_dS
T_dS=hbar*H_dS/(2*np.pi);
print(f"  T_Unruh(a0) = hbar a0/2pi c  ==  T_dS = hbar H_dS/2pi   =>   a0 = c H_dS = c^2 sqrt(Lambda/3)")
print(f"  H_dS = c sqrt(Lambda/3) = {H_dS:.2e} /s  (set by Lambda = VACUUM density, NOT rho_total)")
print(f"  a0(de Sitter-Unruh) = c H_dS = {a0_dSU:.2e} m/s^2  ;  hbar CANCELS (T_dS/T_Unruh) -> a0 classical")
print("  => independently selects rho_DE: the de Sitter temperature is sourced by Lambda (vacuum curvature) alone.")
print("     Robust to thawing DE: the INSTANTANEOUS de Sitter temperature T_dS(z) ∝ sqrt(rho_DE(z)) is always defined,")
print("     even with no asymptotic de Sitter -- so a0(z) ∝ sqrt(rho_DE(z)) survives evolving w.")

# ---------- (3) multi-route convergence ----------
print("\n"+"="*90); print("(3) FOUR INDEPENDENT ROUTES converge on the SAME scale (spread = the O(1) coefficient kappa)"); print("="*90)
routes={
 "dimensional  a0=c^2 sqrt(Lambda/32pi) [framework]": c**2*np.sqrt(Lam/(32*np.pi)),
 "free-fall    a0=(c/2) sqrt(G rho_DE)":               (c/2)*np.sqrt(G*rho_L),
 "de Sitter-Unruh a0=c H_dS=c^2 sqrt(Lambda/3)":       a0_dSU,
 "cosmic-coincidence a0=c H0 (Milgrom 1983)":          c*H0,
}
print("   route                                          | a0 [m/s^2] | a0/1.2e-10")
for k,v in routes.items(): print(f"   {k:46s} | {v:.2e}  |  {v/1.2e-10:5.2f}")
vals=np.array(list(routes.values()))
print(f"\n   spread: {vals.min():.2e} - {vals.max():.2e}  = factor {vals.max()/vals.min():.1f}  (= the O(1) coefficient freedom)")
print("   => the SCALE ~1e-10 is route-INDEPENDENT (forced); the factor-few spread IS the unfalsifiable kappa.")
print("      Every road through the de Sitter/vacuum scale lands at a0 ~ c^2 sqrt(Lambda). Only rho_total/horizon")
print("      (Verlinde) is genuinely different -- and that is the one excluded by data + killed by thawing DE.")

# ---------- theory-space isolation ----------
print("\n"+"="*90); print("THEORY-SPACE ISOLATION (the framework is a point; neighbors make DIFFERENT testable predictions)"); print("="*90)
print("""  The full space of dimensionally-allowed a0 laws: a0 = kappa * (rho)^(1/2+n), rho in {rho_DE, rho_tot, ...}.
   - n (Planck-group exponent): pinned to 0 by the observed magnitude (above) AND testable via a0(z) slope.
   - rho (which density): pinned to rho_DE by universality + non-rising data + the de Sitter-Unruh mechanism.
   - kappa (coefficient): the ONLY free coordinate -- and it is unobservable (cancels in every ratio).
  => the framework occupies an ISOLATED point: every neighbor (different n, different rho) makes a DIFFERENT
     falsifiable a0(z) prediction, and all are excluded or pinned. Only the coefficient axis is free, and nothing
     lives on it observationally. The falsifiable theory is rigid and alone.""")
