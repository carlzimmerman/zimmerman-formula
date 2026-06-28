#!/usr/bin/env python3
"""
B4 SETTLED — the REAL Jeans / equilibrium calculation (replaces the hand-waved posit_empirical_sharpen.py B4).

CLAIM UNDER TEST (B4): in an external field (EFE regime), modified INERTIA gives a velocity-ellipsoid TANGENTIALLY
biased w.r.t. the field axis (beta_field<0), while modified GRAVITY gives the OPPOSITE (beta_field>0) for ANY a0 ->
a clean 'MG-impossible' sign discriminator.

The hand-waved script ASSUMED both signs (beta_MG hardcoded >0; beta_MI from a sigma^2~1/mu proxy). Here we do it
properly: take an IDENTICAL, well-defined distribution function (an ENERGY DF f(E), i.e. a relaxed system with NO
imposed orbital anisotropy) in the SAME anisotropic external-field potential, and compute the actual velocity-
dispersion tensor in each theory. Footing a0=9.36e-11, dS-Unruh mu_fw. Both-ways, no thumb on the scale.
"""
import numpy as np
rng = np.random.default_rng(20260627)
A0 = 9.36e-11

def mu_fw(x):                      # dS-Unruh interpolation, x=a/a0
    x = np.asarray(x, float)
    return np.where(x>0, (np.sqrt(1+4*x*x)-1)/(2*x+1e-300), 0.0)
def Lext(x, h=1e-4):               # L = dln mu / dln a  at a_ext/a0 = x  (the EFE anisotropy parameter, same in both)
    return (np.log(mu_fw(x*(1+h)))-np.log(mu_fw(x*(1-h))))/(2*h)

print("="*100)
print("  B4 SETTLED: does MI vs MG give OPPOSITE-sign velocity anisotropy in the EFE?  (real energy-DF calc)")
print("="*100)
print(f"\n  The controlling EFE parameter L_ext = dln mu/dln a at a_ext (SAME object in both theories):")
for xe in (0.3,0.5,1.0,2.0,4.0):
    print(f"     a_ext/a0={xe:4.1f}:  mu={mu_fw(xe):.4f}   L_ext={Lext(xe):.4f}   (1+L_ext={1+Lext(xe):.4f})")
xe=1.0; Le=Lext(xe)
print(f"\n  Use a_ext/a0={xe} (cluster outskirt): 1+L_ext = {1+Le:.4f}. In the EFE both theories make the dynamics")
print(f"  STIFFER along the field axis z, by the SAME factor (1+L_ext): MG via stronger effective G_par=G_perp*(1+L),")
print(f"  MI via larger effective inertia mu_par=mu_perp*(1+L). The QUESTION is what that does to the VELOCITIES.")

# ---------- MODIFIED GRAVITY: energy DF in an anisotropic harmonic core ----------
# Effective potential Phi = 1/2 (wx^2 x^2 + wy^2 y^2 + wz^2 z^2), with wz^2/wx^2 = G_par/G_perp = 1+L_ext.
# Energy DF: f(E) ~ exp(-E/sig0^2), E = 1/2 v^2 + Phi(x).  STANDARD inertia (kinetic = 1/2 v^2, isotropic).
N=400000
wx=wy=1.0; wz=np.sqrt(1+Le)                     # stiffer along z
sig0=1.0
# velocities: E factorizes -> f(v) ~ exp(-v^2/2sig0^2) ISOTROPIC by construction of an energy DF (this is the point)
vMG = rng.normal(0, sig0, size=(N,3))
# positions: f(x) ~ exp(-Phi/sig0^2) -> Gaussian with sigma_i = sig0/w_i (FLATTENED along z since wz>1)
xMG = np.stack([rng.normal(0, sig0/wx, N), rng.normal(0, sig0/wy, N), rng.normal(0, sig0/wz, N)], axis=1)
sMG = vMG.std(axis=0)
beta_MG = 1 - (0.5*(sMG[0]**2+sMG[1]**2))/sMG[2]**2     # field axis = z = 'radial'; beta=1 - sig_perp^2/sig_par^2
print("\n"+"-"*100)
print("  MODIFIED GRAVITY (standard inertia, anisotropic effective G; energy DF f(E)):")
print(f"     velocity dispersions  sig_x,sig_y,sig_z = {sMG[0]:.4f}, {sMG[1]:.4f}, {sMG[2]:.4f}  -> ISOTROPIC")
print(f"     spatial extents       L_x,L_y,L_z       = {xMG[:,0].std():.4f}, {xMG[:,1].std():.4f}, {xMG[:,2].std():.4f}  -> FLATTENED along z")
print(f"     => beta_field(MG) = {beta_MG:+.4f}   (~0: the anisotropy is in the DENSITY/shape, NOT the velocities)")
print(f"     KEY: an energy DF gives ISOTROPIC sigma_v for ANY potential -> MG does NOT give beta>0. The B4 'MG radial")
print(f"     beta>0' premise is FALSE for a relaxed system; MG hides the EFE in the shape, not the velocity ellipsoid.")

# ---------- MODIFIED INERTIA: generalized energy DF with anisotropic effective inertia ----------
# Heuristic 'energy' E = 1/2 (mu_perp v_perp^2 + mu_par v_par^2) + Phi, mu_par/mu_perp = 1+L_ext.
# f(E) -> generalized equipartition <mu_i v_i^2> equal -> <v_i^2> ~ 1/mu_i -> sig_par^2/sig_perp^2 = mu_perp/mu_par.
mu_perp=mu_fw(xe); mu_par=mu_perp*(1+Le)
sig_par = sig0/np.sqrt(mu_par/mu_perp)          # along field: larger inertia -> SMALLER dispersion
vMI = np.stack([rng.normal(0,sig0,N), rng.normal(0,sig0,N), rng.normal(0,sig_par,N)], axis=1)
sMI = vMI.std(axis=0)
beta_MI = 1 - (0.5*(sMI[0]**2+sMI[1]**2))/sMI[2]**2
print("\n  MODIFIED INERTIA (anisotropic effective inertia, generalized equipartition):")
print(f"     velocity dispersions  sig_x,sig_y,sig_z = {sMI[0]:.4f}, {sMI[1]:.4f}, {sMI[2]:.4f}  -> sig_z SMALLER")
print(f"     => beta_field(MI) = {beta_MI:+.4f}   (TANGENTIAL bias, beta<0) -- a REAL effect from anisotropic inertia")
print(f"     *** BUT: modified inertia has NO standard equilibrium statistical mechanics -- the inertia is")
print(f"     ACCELERATION-history dependent, not a fixed mass, so 'E=1/2 mu_i v_i^2' and equipartition are a")
print(f"     HEURISTIC, not a theorem. The MI beta is an order-of-magnitude estimate, not a forced prediction. ***")

# ---------- the swamp: real cluster infall anisotropy ----------
beta_infall = 0.3   # typical cluster-centric radial-orbit anisotropy from infall (sims/observations ~0.2-0.5)
print("\n"+"-"*100)
print("  THE SWAMP (why neither is measurable as a clean lock):")
print(f"   - real clusters have INFALL orbital anisotropy beta_cc ~ +{beta_infall:.1f} (RADIAL, cluster-centric) from")
print(f"     formation -- magnitude COMPARABLE to or LARGER than the theory effect (|beta_theory| ~ {abs(beta_MI):.2f}).")
print(f"   - that infall anisotropy is aligned with the CLUSTER RADIUS, not the EXTERNAL-FIELD axis -- a different,")
print(f"     dominant, DF-driven signal sitting on top of (and not aligned with) the tiny field-axis term.")
print(f"   - the field-axis term's MAGNITUDE rides L_ext, i.e. the interpolation-function form (a knob).")

print("\n"+"="*100)
print(" VERDICT — B4 is BURIED as a clean 'MG-impossible' discriminator")
print("="*100)
print(f"""  1. The B4 premise is WRONG: MG does NOT give beta>0. For a relaxed (energy) DF, MG gives beta_field = {beta_MG:+.3f}
     (~0) -- the EFE shows up as a FLATTENED DENSITY, with ISOTROPIC velocities. So the 'opposite sign' is fictional.
  2. MI does give a real-ish tangential tilt (beta_field ~ {beta_MI:+.2f}) via anisotropic inertia, BUT modified
     inertia has no rigorous equilibrium stat-mech (acceleration-dependent inertia) -> this is a HEURISTIC estimate,
     not a forced prediction; a full non-equilibrium kinetic treatment is required to even define it.
  3. EITHER WAY it is not a clean discriminator: the signal (|beta|~{abs(beta_MI):.2f}) is comparable to / swamped by
     formation infall anisotropy (beta_cc~+{beta_infall:.1f}, and on the WRONG axis), and its magnitude is knob-dependent.
  => B4 does NOT promote to the live ledger. The hand-waved 'MI beta<0 vs MG beta>0, MG-impossible' is FALSE (MG~0,
     not >0) and the MI side is ill-defined + infall-swamped. Honest residue: a relaxed system MIGHT carry a small
     MI-specific field-axis velocity tilt that MG (relaxed) lacks, but it is below the systematic floor and not a
     near-term test. The 4 banked DE-separable locks (Cassini, relational sigma-spread, dwarf clock, s^TX) stand;
     B4 is NOT added. This is the win-flavored claim killed by the real calculation -- exactly as it should be.""")
print("="*100)
