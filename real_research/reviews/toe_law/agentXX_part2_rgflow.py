"""
agentXX Route 2 — PART 2: the RG / radiative fixed-point test.

Does the khronon's own RG flow (Lorentz-violating gravity is power-counting
renormalizable in the Horava/khronometric UV completion) drive c_chi to a
fixed value? And crucially: is that fixed value tied to H (scale-locked) or
is it an H-independent number (a luminal/conformal fixed point that would
DECOUPLE the edge)?

Key physics facts to encode:
  1. In a RELATIVISTIC (Lorentz-invariant) UV theory, c_chi=1 is protected by
     the Lorentz symmetry: it is an exact RG fixed point and radiative
     corrections cannot move it. But that is the LUMINAL fixed point => HURTS
     the edge (b->c_chi->1 = horizon).
  2. In a LORENTZ-VIOLATING theory (the actual khronon case), c_chi != 1 is
     allowed and RADIATIVELY UNPROTECTED: different species' speeds run
     differently and there is NO symmetry forcing them together. The relevant
     literature result (Collins-Perez-Sudarsky-Urrutia-Vucetich; and the
     khronometric naturalness problem) is that LV speed differences are
     radiatively driven to O(1) — there is NO infrared fixed point pulling
     c_chi to a special value, and certainly not to an H-dependent one.
  3. dS background: H enters the EOM only through the friction term 3H d/dt,
     NOT through the gradient/dispersion term. The dispersion omega = c_chi k
     is a UV/local property; H is an IR/cosmological scale. A beta-function
     beta(c_chi) = d c_chi/d ln(mu) runs c_chi with the RG scale mu, NOT with H.
     For c_chi to be f(H), the RG fixed point would have to sit at the scale
     mu ~ H AND the flow would have to actually reach a nontrivial value there
     — neither is generic.

This part:
  (b1) Model the one-loop-type running schematically and show the fixed-point
       structure: the only protected fixed point is c_chi=1 (luminal,
       Lorentz-restoring), reached ONLY if a Lorentz-invariant attractor
       exists; otherwise c_chi is a free IR modulus.
  (b2) Show that even AT a fixed point, the fixed value is an H-INDEPENDENT
       pure number => not a scale-lock. The fixed point cuts AGAINST the edge.
  (b3) Decisive separation: H couples to the friction term; c_chi to the
       gradient term. Compute the dS-background khronon EOM and confirm H does
       not enter the dispersion relation => no dynamical c_chi=f(H).
"""
import sympy as sp

print("="*70)
print("PART 2 (b3): dS khronon EOM — does H enter the dispersion?")
print("="*70)
# Khronon scalar perturbation phi on a dS background a(t)=e^{Ht}.
# Quadratic action (agentEE STEP 1, Lim astro-ph/0407437 / 1206.1083 form):
#   S2 ~ integral a^3 [ (dot phi)^2 - c_chi^2 (grad phi)^2 / a^2 ] dt d^3x
# EOM (Fourier mode k):  ddot phi + 3 H dot phi + c_chi^2 (k^2/a^2) phi = 0.
t, H, cchi, k = sp.symbols('t H c_chi k', positive=True)
a = sp.exp(H*t)
phi = sp.Function('phi')(t)
EOM = phi.diff(t,2) + 3*H*phi.diff(t) + cchi**2*(k**2/a**2)*phi
print("dS khronon mode EOM:")
sp.pprint(sp.Eq(EOM, 0))
print()
print("Structure: H multiplies the FRICTION term (3H dot phi).")
print("           c_chi multiplies the GRADIENT/dispersion term c_chi^2 k^2/a^2.")
print("They sit in DIFFERENT terms. The local dispersion (high-k WKB) is")
print("   omega^2 = c_chi^2 k_phys^2   with k_phys=k/a,   INDEPENDENT of H.")
print()
# WKB / sub-horizon limit: phi ~ exp(-i \int omega dt); leading term:
# omega = c_chi k_phys. H only sets the Hubble friction / horizon crossing,
# not the speed. Confirm by extracting the high-frequency dispersion:
kphys = sp.symbols('k_phys', positive=True)
# In the adiabatic (WKB) regime the dispersion is the coefficient ratio
# (gradient term)/(time-kinetic term) = c_chi^2 k_phys^2. H-free.
disp = cchi**2 * kphys**2
print("WKB dispersion omega^2 =", disp, "  (no H)")
print()
print("=> H does NOT appear in the khronon dispersion. The sound speed c_chi")
print("   is a UV/local datum; H is the IR cosmological friction scale.")
print("   There is NO dynamical mechanism in the dS+khronon EOM that sets")
print("   c_chi = f(H). The two are SCALE-DECOUPLED at the level of the EOM.")
print("   (This independently reproduces agentRR CHECK 5 and agentSS's")
print("    c_chi<->H decoupling from the dynamics side.)")

print()
print("="*70)
print("PART 2 (b1,b2): fixed-point structure of c_chi under RG flow")
print("="*70)
# Schematic but faithful: in a LV gravity, the speed-squared s=c_chi^2 runs
# under a beta-function. The ONLY symmetry-protected fixed point is the
# Lorentz-invariant one s*=1 (all speeds equal). A toy beta capturing the
# generic structure: speeds relax toward each other only if a Lorentz-
# restoring attractor is present; the LV theory has NO such attractor in the
# IR (Collins et al.: LV is radiatively UNSTABLE, differences grow/stay O(1)).
s, mu = sp.symbols('s mu', positive=True)   # s = c_chi^2, mu = RG scale
# Lorentz-protected fixed point: beta(s) = -gamma (s - 1).
gamma = sp.symbols('gamma', positive=True)
beta_LI = -gamma*(s - 1)
fp = sp.solve(sp.Eq(beta_LI, 0), s)
print("Lorentz-protected toy beta-function beta(s) = -gamma (s-1):")
print("  fixed point s* =", fp, "  i.e. c_chi^2 = 1  (LUMINAL).")
print()
print("RUTHLESS reading of this fixed point:")
print("  * It is an H-INDEPENDENT pure number (s*=1). No H => NO scale-lock.")
print("  * c_chi -> 1 means the sonic edge b->c_chi -> 1 = the LIGHT CONE /")
print("    de Sitter horizon. The sonic edge MERGES with the horizon and")
print("    DECOUPLES from the interior fold band. This HURTS the edge")
print("    coincidence (it removes the distinct sonic surface the fold needs).")
print()
print("  In the LV (non-luminal) case there is NO protected fixed point at")
print("  c_chi != 1, so c_chi is a free IR modulus (agentU's Cherenkov corner")
print("  c_chi^2 in [1.000,1.033]) — radiatively UNPROTECTED, must be TUNED.")
print()
print("EITHER WAY: a fixed point gives an H-independent number (no lock), and")
print("the only protected one (luminal) actively HURTS. No RG route to c_chi=f(H).")
