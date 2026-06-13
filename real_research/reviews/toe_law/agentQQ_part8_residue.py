import sympy as sp
import numpy as np
import mpmath as mp
mp.mp.dps = 30

print("="*78)
print("PART 8 — RUTHLESS: is the X2 DC active gain (mu_hat(0)<mu_hat(inf)) achievable by a")
print("         STABLE (LHP) response, or does it FORCE an anti-damped UHP pole (runaway)?")
print("="*78)
print("""
This is the sharpest form of the tension. X2 needs Im mu_hat<0 in a band (active /
negative spectral weight). PP needs the same. The question that could KILL the story:
is negative spectral weight only realizable with anti-damping (negative gamma => UHP
pole => exponential runaway), which X's OWN dynamics run (6c: damped Picard, no
runaway) FORBIDS? If so, X2's stability premise (P3) and the active requirement
collide and the fold is incompatible with X.
""")

# Model: chi(omega) = sum residues. A NEGATIVE-residue Lorentzian with gamma>0 gives
# Im chi<0 (active) while keeping the pole in the LHP. Verify: does it have a CAUSAL,
# DECAYING (non-runaway) impulse response? Compute the time-domain Green's function.
print("Test: negative-residue Lorentzian chi(omega)= -A/(w0^2-omega^2-i*gamma*omega), gamma>0.")
print("  Impulse response g(t) = inverse FT. Poles at omega=+-sqrt(w0^2-gamma^2/4)-i gamma/2.")
A=1.0; w0=1.0; gamma=0.2
# poles in omega-plane:
disc = w0**2 - (gamma/2)**2
wr = np.sqrt(disc)
print(f"  poles: omega = +-{wr:.4f} - i*{gamma/2:.4f}  => Im(omega)<0 => LHP => DECAYING in time.")
print(f"  g(t) ~ e^{{-(gamma/2) t}} sin(wr t)  for t>0, ZERO for t<0 => CAUSAL and DECAYING.")
# numerically invert via residues
t = np.linspace(0,40,400)
g = -A/wr*np.exp(-(gamma/2)*t)*np.sin(wr*t)  # standard retarded Green fn x (-A)
print(f"  g(t) envelope at t=40: {abs(-A/wr*np.exp(-(gamma/2)*40)):.2e}  => decays to ~0 (no runaway).")
print(f"  max|g| over t: {np.max(np.abs(g)):.3f} finite => bounded. STABLE.\n")

# Im chi on real axis (active band):
om = np.linspace(0.01,3,600)
chi = -A/(w0**2 - om**2 - 1j*gamma*om)
print(f"  Im chi: min={chi.imag.min():+.3f} (negative => ACTIVE band present).")
# DC ordering
chi0 = (-A/(w0**2)).real
chiinf = 0.0
print(f"  chi(0)={chi0:+.3f} < chi(inf)={chiinf:.3f}  => INVERTED MOND ordering delivered.")
print()
print("KEY RESULT: a NEGATIVE-RESIDUE, POSITIVE-gamma Lorentzian gives:")
print("  (i) Im chi<0 in a band  [active / negative spectral weight: PP + X2 satisfied]")
print("  (ii) poles in LHP, g(t) causal & DECAYING  [P1 + P3: causal, no runaway]")
print("  (iii) chi(0)<chi(inf)   [the X2 inverted ordering]")
print("ALL THREE AT ONCE. Active gain does NOT require anti-damping (negative gamma).")
print("Negative RESIDUE (gain) is distinct from negative DAMPING (instability).\n")

# The crucial distinction, made rigorous:
print("THE DISTINCTION THAT RESOLVES THE TENSION:")
print("  'non-passive / Im chi<0' (what PP+X2 need)  =/=  'anti-damped / pole in UHP' (runaway).")
print("  Passivity is violated by the SIGN of the spectral weight (residue), which can be")
print("  negative while every pole stays in the LHP. Stability (P3) is about pole LOCATION,")
print("  not residue sign. So a medium can be active (non-passive) AND stable AND causal.")
print("  => There is NO contradiction; X2's stability premise survives the active fold.\n")

# Honesty check: but does the doubled-action SK pump actually realize negative-residue
# (gain) without anti-damping? That is the COUPLING question (Link 5), not settled here.
print("HONEST CAVEAT (the residual gap): that a STABLE active (negative-residue) response")
print("EXISTS mathematically is proven. Whether the dS-bath PUMP realizes it as negative-")
print("RESIDUE (stable gain) rather than negative-DAMPING (runaway) is the COUPLING question")
print("= Link 5's unbanked mechanism. The structure permits stability; it does not FORCE it.")
