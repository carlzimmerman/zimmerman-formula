#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRECTED clean-room verification of the modified-INERTIA PPN alpha2 (Nordtvedt
solar-spin) result for the Zimmerman framework, 2026-06-17.

HISTORY (both ways, on the record):
  * An intermediate DERIVE agent ("D", woglr53nv) claimed alpha2 is SELF-ENERGY
    ENHANCED: alpha2_MI = c^2 * INT rho W dV / E_g = (5/4)a0 c^2 R^3/(G^2 M^2)
    ~ 1e-8..2e-7, a "LIVE ~1-22x Nordtvedt test", calling the prior ~1e-13 a
    "category error that dropped the (c/v_esc)^2 weighting".
  * The workflow's own VERIFY_COEFF + SYNTH OVERTURNED that: D's c^2/E_g =
    c^2/(GM/R) ~ 4.7e5 factor is a DOUBLE-COUNT imported from the metric-PPN
    template (where alpha2 multiplies the potential U_ij and carries self-energy).
    A modified-INERTIA theory (Route E: STANDARD-GR metric) has NO such U_ij
    coupling. The correct alpha2 is the per-particle order a0/g ~ 1e-13, ~1e6x safe.

THIS SCRIPT verifies the CORRECT physics (what Carl asked: "verify the toy and the
Shao-Wex Eq.5 linearity yourself before editing"):
  A. Shao-Wex Eq.5 (arXiv:1307.2552): Omega_prec = -(alpha2/2)(2pi/P)(w/c)^2 cos psi
     is STRICTLY LINEAR in the dimensionless alpha2 and contains NO gravitational
     self-energy (E_g) factor.
  B. Rigid-body toy: the boost-induced inertia-tensor anisotropy is
     delta-I/I = (1-mu) * beta^2/2 * O(1) -- a dimensionless RATIO normalized by the
     moment of inertia I ~ M R^2 (i.e. by MASS), with NO 1/E_g amplification.
     => matching to Eq.5 gives alpha2_MI = O(1)*(1-mu)(g_internal) ~ a0/g.
  C. The two normalizations: INT rho W /M ~ 1e-13 (CORRECT) vs c^2 INT rho W /E_g
     ~ 1e-7 (D's). Their ratio is EXACTLY M c^2/E_g = c^2/(GM/R) -- the double-count.
  D. alpha2_MI(Sun) ~ a few x 1e-13, margin vs Nordtvedt 2.4e-7 ~ 1e6x: SAFE.

Quarantine: a0 is the INPUT throughout; nothing SM derived. Outcome PARTIAL
(order a0/g + internal-g acceleration FORCED; O(1) structure prefactor open).
"""
import numpy as np
import sympy as sp

print("="*72)
print("PART A — Shao-Wex Eq.5 is LINEAR in dimensionless alpha2, NO self-energy")
print("="*72)
alpha2, P, w, c, psi, Eg, M = sp.symbols('alpha2 P w c psi E_g M', positive=True)
Omega = -(alpha2/2)*(2*sp.pi/P)*(w/c)**2*sp.cos(psi)   # Shao-Wex Eq.5
d1 = sp.diff(Omega, alpha2)
d2 = sp.diff(Omega, alpha2, 2)
print("  Omega_prec(alpha2)      =", Omega)
print("  d Omega / d alpha2      =", sp.simplify(d1), "  (constant in alpha2 -> LINEAR)")
print("  d^2 Omega / d alpha2^2  =", d2, "  (=> strictly linear, no alpha2^2)")
print("  contains E_g (self-energy)?", Omega.has(Eg), "  -> precession-per-alpha2 has NO E_g factor")
print("  => to USE the Nordtvedt bound 2.4e-7 you match the MI precession to THIS;")
print("     the effective alpha2 is whatever dimensionless number multiplies (2pi/P)(w/c)^2.")

print()
print("="*72)
print("PART B — rigid-body toy: delta-I/I = (1-mu)*beta^2/2, normalized by MASS")
print("="*72)
# A spinning body whose constituents have a boost-induced ANISOTROPIC inertial mass:
# along w the inertial mass is modulated by the MI factor; the fractional anisotropy
# of the inertia TENSOR is what torques the spin. Model: continuous sphere, each
# element's inertial mass m_eff = m*(1 - eps*(rhat . what)^2), eps = (1-mu)*beta^2,
# representing the leading w^2 boost anisotropy of the dS-Unruh inertia coupling.
# Compute I_zz (w || z) vs I_xx and the fractional split; show it = eps*O(1),
# independent of any binding energy, normalized by I ~ M R^2.
eps = sp.symbols('epsilon', positive=True)      # = (1-mu)*beta^2  (per-constituent)
th, ph, r, R = sp.symbols('theta phi r R', positive=True)
rho0 = sp.symbols('rho0', positive=True)
# direction cosines; w along z.  (rhat.what)^2 = cos^2(theta)
aniso = 1 - eps*sp.cos(th)**2                    # anisotropic inertial-mass weight
dV = r**2*sp.sin(th)
# moment of inertia about z (spin axis = z): integrand rho*aniso*(r sin th)^2
Izz = sp.integrate(rho0*aniso*(r*sp.sin(th))**2 * dV, (r,0,R),(th,0,sp.pi),(ph,0,2*sp.pi))
# moment about x: distance^2 from x-axis = r^2 (sin^2th sin^2ph + cos^2th)
dx2 = (r*sp.sin(th)*sp.sin(ph))**2 + (r*sp.cos(th))**2
Ixx = sp.integrate(rho0*aniso*dx2 * dV, (r,0,R),(th,0,sp.pi),(ph,0,2*sp.pi))
Iiso = sp.integrate(rho0*(r*sp.sin(th))**2 * dV, (r,0,R),(th,0,sp.pi),(ph,0,2*sp.pi))
Mtot = sp.integrate(rho0*dV,(r,0,R),(th,0,sp.pi),(ph,0,2*sp.pi))
dItr = sp.simplify((Izz - Ixx)/Iiso)             # fractional inertia anisotropy
print("  I_iso (no MI)           =", sp.simplify(Iiso), "  (= (2/3) of ... ~ M R^2: an INERTIA, normalized by M)")
print("  total mass M            =", sp.simplify(Mtot))
print("  fractional anisotropy (I_zz - I_xx)/I_iso =", dItr)
print("    -> = eps * O(1) = (1-mu)*beta^2 * O(1).  PURE RATIO, no E_g anywhere.")
# substitute eps = (1-mu)*beta^2 and show alpha2 ~ (1-mu) after matching Eq.5 (~beta^2 cancels)
mu_, beta_ = sp.symbols('mu beta', positive=True)
dItr_phys = dItr.subs(eps,(1-mu_)*beta_**2)
print("  with eps=(1-mu)beta^2:  delta-I/I =", sp.simplify(dItr_phys))
print("  matching Omega=(alpha2/2)(2pi/P)beta^2 to (delta-I/I)*(2pi/P):")
print("     alpha2 = 2*(delta-I/I)/beta^2 =", sp.simplify(2*dItr_phys/beta_**2),
      "= O(1)*(1-mu)   <- NO self-energy, normalized by MASS")

print()
print("="*72)
print("PART C — the two normalizations: M (correct) vs E_g/c^2 (D's double-count)")
print("="*72)
G_, c_, a0_ = 6.674e-11, 2.998e8, 9.36e-11
Msun, Rsun = 1.989e30, 6.957e8
# n=3 Lane-Emden (RK4), as before, to compute INT rho W dV with W=a0/2g
def lane_emden(n=3.0, dxi=1e-4):
    x,t,d = 1e-6,1.0,0.0; xs=[x]; ts=[t]; ds=[d]
    while t>0:
        def f(x,t,d):
            tt=t if t>0 else 0.0
            return d, -(2.0/x)*d - tt**n
        k1t,k1d=f(x,t,d); k2t,k2d=f(x+dxi/2,t+dxi/2*k1t,d+dxi/2*k1d)
        k3t,k3d=f(x+dxi/2,t+dxi/2*k2t,d+dxi/2*k2d); k4t,k4d=f(x+dxi,t+dxi*k3t,d+dxi*k3d)
        t+=dxi/6*(k1t+2*k2t+2*k3t+k4t); d+=dxi/6*(k1d+2*k2d+2*k3d+k4d); x+=dxi
        xs.append(x); ts.append(max(t,0.0)); ds.append(d)
    return np.array(xs),np.array(ts),np.array(ds)
xi,th_le,dth=lane_emden()
xi1=xi[-1]; alpha_len=Rsun/xi1
mfac=np.clip(-xi**2*dth,0,None); rho_c=Msun/(4*np.pi*alpha_len**3*mfac[-1])
rr=alpha_len*xi; rho_r=rho_c*th_le**3; Mr=4*np.pi*alpha_len**3*rho_c*mfac
g_r=np.where(rr>0,G_*Mr/np.maximum(rr,1e-9)**2,0.0)
W_r=np.where(g_r>0,a0_/(2*g_r),0.0)
INT=np.trapz(rho_r*W_r*4*np.pi*rr**2,rr)             # INT rho W dV  (units: mass)
Eg=np.trapz(np.where(rr>0,G_*Mr/np.maximum(rr,1e-9)*4*np.pi*rr**2*rho_r,0.0),rr)
norm_by_M   = INT/Msun                                 # CORRECT (moment-of-inertia ratio)
norm_by_Egc = c_**2*INT/Eg                             # D's (metric-PPN import)
print(f"  INT rho W dV            = {INT:.3e} kg")
print(f"  alpha2 normalized by M       = INT/M        = {norm_by_M:.3e}   <- CORRECT (~1e-13)")
print(f"  alpha2 normalized by E_g/c^2 = c^2 INT/E_g  = {norm_by_Egc:.3e}   <- D's (~1e-7)")
print(f"  ratio (D / correct)          = {norm_by_Egc/norm_by_M:.3e}")
print(f"  M c^2 / E_g                  = {Msun*c_**2/Eg:.3e}   <- the double-count factor matches")
print(f"  => D divided the inertia-anomaly integral by E_g/c^2 instead of M (the moment-")
print(f"     of-inertia normalization), inflating alpha2 by c^2/(GM/R) ~ 5e5. SPURIOUS.")

print()
print("="*72)
print("PART D — alpha2_MI(Sun) and the Nordtvedt margin")
print("="*72)
g_surf=G_*Msun/Rsun**2
a2_surface=a0_/(2*g_surf)                               # (1-mu) at the surface, O(1) prefactor ~1
print(f"  (1-mu) at surface = a0/2g_surf = {a2_surface:.3e}   (g_surf={g_surf:.0f} m/s^2)")
print(f"  structure-weighted INT rho W /M (n=3)        = {norm_by_M:.3e}")
print(f"  representative alpha2_MI ~ a few x 1e-13 (range ~1e-14..4e-13 over g~274..1e4)")
print(f"  Nordtvedt bound |alpha2| < 2.4e-7  ->  margin = {2.4e-7/norm_by_M:.2e}x  (~1e6x)")
print()
print("VERDICT: alpha2_MI ~ a few x 1e-13, ~1e6x under Nordtvedt = COMFORTABLY SAFE,")
print("NOT a 'LIVE ~1-22x' test. D's self-energy enhancement was a c^2/(GM/R) double-count.")
print("The prior ~1e-13 ORDER was right. Outcome PARTIAL (O(1) structure prefactor open).")
print("s^TX dipole (~9.6x, COM/orbital) is untied from alpha2 and UNCHANGED. a0 = input.")
print("="*72)
