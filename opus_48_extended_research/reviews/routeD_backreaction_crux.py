#!/usr/bin/env python3
r"""
ROUTE D -- the BACK-REACTION crux, isolated and stress-tested both ways.

The one thing Route D adds over the generic-bath run: the bath temperature is T_eff(a), set by
the worldline's OWN acceleration (self-consistent / parametric). Does that self-consistency
genuinely open the active (MOND-inverting) door the linear bath could not, or does it ALSO land
anti-MOND? And is the Deser-Levin floor b=1/2 a genuine match or a fit?

Both ways. sympy/mpmath. Tag DERIVED vs ASSUMED vs ANSATZ.
"""
import sympy as sp, numpy as np, mpmath as mp
mp.mp.dps=30
def hr(s): print("\n"+"="*80+"\n "+s+"\n"+"="*80)

# ----------------------------------------------------------------------------
hr("A.  Is the Deser-Levin floor b=1/2 a genuine match? (check the physical numbers)")
# ----------------------------------------------------------------------------
# Deser-Levin (gr-qc/9706018): an accelerated detector in dS sees
#   T_eff = (hbar/2 pi c k) sqrt(a^2 + (c H_L)^2).
# The dS (Gibbons-Hawking) floor for a COMOVING detector (a=0) is T_dS=(hbar/2pi c k)(c H_L).
# So in T_eff the floor acceleration is a_floor = c H_L.  The framework: a0 = c H_L / Z, Z=sqrt(32pi/3).
# Question: does mu_fw's internal floor b=1/2 (in a0-units, Part 0 of routeD) equal c H_L / a0 = Z?
# NO -- and that is the honest subtlety. Resolve it explicitly.
Z = mp.sqrt(mp.mpf(32)*mp.pi/3)
print("[A1] Z = sqrt(32 pi/3) =", mp.nstr(Z,8))
print("     c H_L / a0 = Z =", mp.nstr(Z,8), " (the dS floor in a0-units, from a0=cH_L/Z)")
print("     BUT mu_fw's internal floor (Part 0) is b=1/2 in a0-units. These DIFFER (Z vs 1/2).")
print(r"""
[A2] RESOLUTION (both ways, the honest reading):
   mu_fw = (sqrt(1+4x^2)-1)/2x is the inverse of g_obs=sqrt(gN^2+gN a0). Writing it as a
   Deser-Levin ratio (sqrt(x^2+b^2)-b)/x forces b=1/2 -- this b is the floor IN THE INERTIA-RATIO,
   NOT the temperature floor. The relation between them is the response->inertia MAP:
     - T_eff floor (temperature) sits at a = c H_L = Z a0   (Z=5.789 in a0 units),
     - mu_fw inertia floor sits at b = 1/2 a0.
   The factor between them (Z vs 1/2) is absorbed by the SAME response->inertia map that is the
   unproven ansatz. So even the FLOOR MATCH is map-contingent: the sqrt FORM is Deser-Levin's,
   but the numerical floor (1/2 vs Z) only lines up after the ansatz map. This SHARPENS routeD's
   verdict: the FORM (sqrt of sum of squares) is genuinely dS-Unruh; the COEFFICIENTS (both the
   1/2 floor and the inertia reading) ride on the un-derived map. [DERIVED, corrects an over-claim]
""")
# Show the two-parameter family and that matching BOTH the form and v^4=GMa0 needs the map:
x,b = sp.symbols('x b', positive=True)
R = (sp.sqrt(x**2+b**2)-b)/x
print("[A3] deep-MOND slope of R(x)= (x->0):", sp.limit(R/x,x,0), " => to get mu~x need b=1/2 EXACTLY.")
print("     So b=1/2 is FORCED *given* the (T_eff-floor)/a reading -- but that reading is the ansatz.")

# ----------------------------------------------------------------------------
hr("B.  Does self-consistent T_eff(a) open the active door? (the parametric back-reaction)")
# ----------------------------------------------------------------------------
print(r"""
The linear bath (fixed T) is passive -> anti-MOND (routeD Part 4). Route D's hope: T_eff=T_eff(a)
is a PARAMETRIC coupling (bath set by the system's own state), the one regime agentZZ Part 4 said
*could* host an active kernel. We test the self-consistent inertia directly.

Self-consistent ansatz-FREE statement: integrating out a bath at temperature T gives a reactive
inertia dressing Delta m(T) = (2/pi) int [A(W;T)/W] dW (the DC reactive shift). For the dS bath
A(W;T)=(W/2pi)coth(W/2T), this DC shift is a MONOTONE function of T. Whether the SELF-CONSISTENT
m_eff(a)=m+Delta m(T_eff(a)) rises or falls with a is then fixed by sign(d Delta m/dT) -- DERIVED,
no ansatz. If d Delta m/dT>0, higher a (higher T_eff) => MORE inertia => anti-MOND. Compute it.
""")
def DC_reactive_shift(Tval, Wc=400.0, n=2_000_000):
    # Delta m(T) = (2/pi) int_0^Wc [A(W)/W] dW, A(W)/W=(1/2pi)coth(W/2T); UV-cutoff Wc.
    W=np.linspace(1e-4,Wc,n)
    integrand=(1.0/(2*np.pi))*(1.0/np.tanh(W/(2*Tval)))
    return (2/np.pi)*np.trapz(integrand,W)
Ts=[0.2,0.5,1.0,2.0,5.0,10.0]
shifts=[DC_reactive_shift(T) for T in Ts]
print("   T_eff:    ", "  ".join(f"{t:6.2f}" for t in Ts))
print("   Delta m:  ", "  ".join(f"{s:6.3f}" for s in shifts))
mono = all(shifts[i+1]>shifts[i] for i in range(len(shifts)-1))
print(f"   d(Delta m)/dT > 0 monotone: {mono}")
print(r"""   => higher T_eff (higher a) gives MORE reactive inertia. Self-consistently,
      m_eff(a) = m + Delta m(T_eff(a)) INCREASES with a. But MOND needs m_eff to DECREASE with a
      (inertia drops at LOW a). So the self-consistent dS back-reaction is ANTI-MOND TOO. The
      parametric T_eff(a) coupling does NOT flip the sign -- it makes inertia rise with a, the
      WRONG way. [DERIVED] The 'parametric door' is open in CLASS (agentZZ) but the dS bath walks
      through it in the anti-MOND direction. Route D's specific environment does not invert.
""")

# ----------------------------------------------------------------------------
hr("C.  The non-adiabatic / high-persistence opening (the one genuine live lead, honestly)")
# ----------------------------------------------------------------------------
print(r"""
agentZZ's WALL 3 + the verifier extension found the ONLY physically-realized active baths
(2505.18665, 1707.09020) need HIGH PERSISTENCE / NON-ADIABATIC drive. For the dS bath:
the correlation/persistence time is tau_c ~ 1/T_eff ~ 1/sqrt(a^2+(cH)^2). Adiabaticity ratio for
a galactic orbit is omega_orbit * tau_c.
""")
# numbers
hbar=1.0545718e-34; kB=1.380649e-23; cc=2.998e8; H0=2.20e-18; OmL=0.685
HL=H0*np.sqrt(OmL)                      # de Sitter Hubble rate (pure-Lambda)
a0=cc**2*np.sqrt((3*OmL*H0**2/cc**2)/(32*np.pi))   # = c^2 sqrt(Lambda/32pi)
# at the MOND scale a~a0: T_eff floor temperature, persistence time
T_floor=(hbar/(2*np.pi*cc*kB))*(cc*HL)             # GH temperature
tau_c=hbar/(kB*T_floor) if T_floor>0 else np.inf   # thermal correlation time ~ hbar/kT
kpc=3.086e19
for v,r in [(150e3,10*kpc),(200e3,30*kpc)]:
    wo=v/r
    print(f"   galaxy v={v/1e3:.0f}km/s r={r/kpc:.0f}kpc: omega_orb={wo:.2e}/s, tau_c={tau_c:.2e}s, "
          f"omega_orb*tau_c={wo*tau_c:.2e}")
print(f"   (T_dS floor temperature = {T_floor:.2e} K; a0={a0:.3e} m/s^2; cH_L={cc*HL:.3e} m/s^2)")
print(r"""   => omega_orb * tau_c >> 1: galactic orbits are DEEPLY NON-ADIABATIC w.r.t. the dS thermal
      correlation time (tau_c ~ 1/H_L ~ Hubble time >> orbital period). This is the OPPOSITE of
      agentZZ's 'H/omega_orb<<1 adiabatic' framing -- and it MATTERS: in the high-persistence /
      non-adiabatic regime is exactly where the active baths (2505.18665) realize negative friction.
      So the dS bath IS in the non-adiabatic regime that *permits* the active sign. BUT (both ways):
      permission != realization -- those baths ALSO need detailed-balance-breaking INTERNAL FUEL
      (self-propulsion), which the equilibrium (KMS) dS vacuum lacks (Part B: dS is KMS-passive,
      d Delta m/dT>0). Non-adiabaticity removes ONE barrier; the dS vacuum still lacks the fuel.
      Status: the non-adiabatic door is OPEN for the dS bath (corrects agentZZ's adiabatic framing
      for the persistence-time comparison), but the dS vacuum is still equilibrium/passive, so it
      does not supply the active sign. The gap is now SHARP: a SUSTAINED, NON-EQUILIBRIUM dS state
      (decaying-dS / non-KMS) would be needed -- not the static dS vacuum. [DERIVED, both ways]
""")

# ----------------------------------------------------------------------------
hr("D.  Route D verdict, sharpened")
# ----------------------------------------------------------------------------
print(r"""
- The sqrt FORM of mu_fw IS genuinely induced (Deser-Levin T_eff of the accelerated detector in
  the dS vacuum) -- real, verified, not an ansatz. [credit]
- The numerical floor (b=1/2 vs the temperature floor Z=5.789) and the inertia-reading both ride
  on the unproven response->inertia MAP; even the floor match is map-contingent (Part A). [concede]
- The dS bath, integrated out, is KMS-passive: both the fixed-T self-energy (routeD Part4) and the
  self-consistent T_eff(a) back-reaction (Part B) give inertia RISING with a = ANTI-MOND. The
  parametric door is open in class but the dS vacuum walks the wrong way. [concede]
- The non-adiabatic regime IS where the dS bath sits (tau_c~1/H_L >> orbit), correcting the prior
  adiabatic framing -- this removes one barrier, but the static dS vacuum is still equilibrium and
  lacks the detailed-balance-breaking fuel, so it does not realize the active sign. The sharpened
  gap: a NON-EQUILIBRIUM / decaying dS (not the static vacuum) would be required. [both ways]
NET: induced FORM yes; induced INVERSION no; the map and the active sign remain un-sourced.
""")
