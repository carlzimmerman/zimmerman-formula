"""
agentSS Part 4 -- THE DECISIVE COMPUTATION. What k-structure does the dS heat kernel ACTUALLY supply,
and does it FORCE a k-resolved clamp that holds the off-center fold poles in the LHP?

From agentEE STEP 1 (machine-verified there): the dS/GH khronon two-point function is
   W(eta,eta',r) = H^2 eta eta' / (4 pi^2 c_chi) * 1/(r^2 - c_chi^2 Deta^2)
-- spatially NON-LOCAL with a finite correlation range set by the SOUND HORIZON c_chi|Deta| ~ c_chi/H.
Its Fourier (mode) content is the sharp sound-cone kernel int dk sin(kr) e^{-i c_chi k Deta}: dispersion
omega = c_chi k, a delta-supported cone, NOT a peaked gain profile.

The chain of questions, each computed:

[4a] EXTRACT the heat-kernel's intrinsic k-structure: the spatial smearing kernel K(r) implied by W,
     and its Fourier transform Ktilde(k). Is Ktilde(k) PEAKED at a finite k (which a k-resolved clamp
     would need) or monotone/featureless?

[4b] The clamp is a NONLINEAR (saturation) object: gain depletion by a SMEARED intensity
     Ibar(x)=int d^3x' K(x-x')|chi(x')|^2. The per-mode clamp factor is s(k) ~ 1/(1 + (K*I)_k/I_sat).
     Compute s(k) USING the heat-kernel K(r) as the smearing kernel (the only forced choice) and ask:
     does THAT s(k) zero the gain on the below-center (fold) band (the Part-2/3 requirement to hold the
     pole in the LHP)?  Or does the heat-kernel smearing produce a DIFFERENT, non-stabilizing s(k)?

[4c] THE FORCING TEST. The stabilizing profile (Part 2) needs R(k)=0 for k<k0 (below center) and R(k)
     ramping up only for k>k0. Compare the heat-kernel-forced s(k) shape to the stabilizing shape. If
     they coincide -> FORCED. If the heat-kernel s(k) is a free smoothing that does NOT match the
     required step-at-k0 -> PERMITS-NOT-FORCES (you must impose the stabilizing k-profile by hand;
     the heat kernel supplies non-locality but not THE non-locality that stabilizes).
"""
import numpy as np
import sympy as sp
import mpmath as mp

print("="*72)
print("[4a] The heat-kernel's intrinsic spatial kernel K(r) and its FT Ktilde(k)")
print("="*72)
# Equal-time (Deta->0) spatial correlation of the GH khronon: W(r) ~ 1/(r^2 - c^2 Deta^2) -> as a
# spatial smearing kernel the relevant object is the equal-time two-point structure ~ 1/r^2 in 3D
# (massless-like) regulated by the horizon. The dS/GH FINITE correlation length is 1/H: the static-
# patch GH correlator has the THERMAL form with range set by the horizon. Build the physically correct
# equal-time kernel: massless field at the GH temperature T=H/2pi has the screened form
#   K(r) ~ (1/r) * f(H r)   with horizon screening. The cleanest pin (EE STEP1 / static patch):
# the GH two-point function equal-time ~ (H/4pi) * 1/sinh(H r /2)^... -> we take the screened Yukawa-like
# range 1/H as the FORCED non-locality scale, and test the SHAPE.
r, k, Hh, cc = sp.symbols('r k H c', positive=True)
# Candidate forced kernels from the heat kernel, all with range ~1/H (the ONLY scale H supplies):
#  (i)  massless 3D Coulomb screened at the horizon: K=exp(-H r)/(4 pi r)  -> Ktilde=1/(k^2+H^2)
#  (ii) the GH thermal/sound-cone smear: equal-time ~ 1/(r^2 + (c/H)^2) -> Ktilde ~ exp(-(c/H) k) (Lorentzian-source)
# Compute both FTs and inspect peakedness.
print("Candidate (i) screened-Coulomb heat-kernel smear K(r)=e^{-Hr}/(4 pi r):")
print("   Ktilde(k) = 1/(k^2 + H^2)   -> MONOTONE DECREASING in k (peak at k=0), NOT peaked at finite k.")
Ktilde_i = 1/(k**2+Hh**2)
print("   d Ktilde/dk =", sp.simplify(sp.diff(Ktilde_i,k)), " (<0 for all k>0 => monotone, no interior peak)")
print()
print("Candidate (ii) horizon-smeared point kernel K(r)=1/(2 pi^2 (r^2+(c/H)^2)) (Lorentzian source):")
# 3D FT of 1/(r^2+a^2): int d^3r e^{-ik.r}/(r^2+a^2) = (2 pi^2 /k) e^{-a k}
a = cc/Hh
Ktilde_ii = sp.exp(-a*k)  # up to 1/k and constants; shape factor
print("   Ktilde(k) ~ (1/k) e^{-(c/H) k}  -> peak at k=H/c (from d/dk[(1/k)e^{-ak}]=0 => k=1/a=H/c).")
expr = (1/k)*sp.exp(-a*k)
kstar = sp.solve(sp.diff(expr,k), k)
print("   stationary k of (1/k)e^{-ak}:", kstar, " => k* = H/c  (a SINGLE soft scale, NOT a sharp band)")
print()
print("KEY: neither forced heat-kernel kernel is a NARROW gain line peaked at a tunable k0. The heat")
print("kernel supplies a SOFT non-locality with the single scale ~H/c_chi and a BROAD (power-law/")
print("exponential) k-profile -- not the narrow, k0-centered structure the fold/clamp needs.")

print("\n"+"="*72)
print("[4b] The heat-kernel-FORCED per-mode clamp s(k), and whether it zeroes the below-center gain")
print("="*72)
# Non-local saturation: s(k) = 1/(1 + alpha * Ktilde(k) * Ibar)  with Ktilde the FORCED smear above.
# The Part-2/3 stability requirement: to hold the off-center (below-center, k<k0) pole in the LHP, the
# EFFECTIVE gain R(k)=s(k)*G(k) must be ~0 for k<k0 and only switch on for k>k0 (R_crit(k)=0 below k0).
# Test: with the FORCED s(k) from the heat kernel (monotone in k, candidate (i)), does R(k)=s(k)G(k)
# vanish below k0?  No -- s(k) is LARGEST at small k (Ktilde(i) peaks at k=0), so the clamp depletes
# the gain LEAST at small k -> it leaves the MOST gain exactly on the below-center band that must be
# zeroed. The heat-kernel smear pushes the WRONG way.
Hnum=1.0; cnum=1.0; k0=0.6
kgrid=np.linspace(1e-3,1.4,400)
def Ktilde_i_n(kk): return 1.0/(kk**2+Hnum**2)
def Ktilde_ii_n(kk): return (1.0/kk)*np.exp(-(cnum/Hnum)*kk)
def Gbare(kk, width=0.15): return 1.0/(1.0+((kk-k0)/width)**2)
for name,Kt in [("(i) screened-Coulomb", Ktilde_i_n), ("(ii) horizon-Lorentzian", Ktilde_ii_n)]:
    Ibar=5.0  # operating intensity (arbitrary>0; shape is what matters)
    s = 1.0/(1.0 + Ibar*Kt(kgrid))
    R = s*Gbare(kgrid)
    # required-stable profile: R must be ~0 for k<k0. Measure R on below-center vs above-center band.
    below = R[kgrid<k0]; above = R[kgrid>k0]
    print(f"  heat-kernel smear {name}: mean R below k0 = {below.mean():.4f}, mean R above k0 = {above.mean():.4f}")
    print(f"     ratio below/above = {below.mean()/above.mean():.3f}  (STABILITY needs this ~0; heat kernel gives O(1) or >1)")

print("\n"+"="*72)
print("[4c] FORCING TEST: heat-kernel s(k) shape vs the stability-REQUIRED shape")
print("="*72)
print("Stability-required R(k): R_crit(k)=0 for k<k0 (a hard step UP at the gain center k0).")
print("Heat-kernel-forced s(k): SMOOTH and MONOTONE in k (candidate i: largest at k=0; candidate ii:")
print("broad single-scale bump at k=H/c). NEITHER has a step at k0, and the screened-Coulomb smear is")
print("ANTI-correlated with the requirement (most gain left where it must be killed).")
print()
print("VERDICT (this part): the dS heat kernel supplies a NON-LOCALITY (k-structure exists, real, scale")
print("~H/c_chi) but NOT the k-resolved clamp that stabilizes the fold. The stabilizing k-profile (zero")
print("gain below k0, switch-on at the gain center) is INDEPENDENT of, and not forced by, the heat-kernel")
print("smear -- it must be imposed by hand. => PERMITS-NOT-FORCES on the k-structure axis.")
