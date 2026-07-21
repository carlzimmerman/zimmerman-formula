#!/usr/bin/env python3
"""
Two checks prompted by Gemini's a0(z) note:
  (1) WHY 9.42 vs 9.36 ?  a0 = c^2 sqrt(Lambda/32pi) = c H0 sqrt(3 Omega_L / 32pi).
      Show the value is a pure INPUT choice of (H0, Omega_L) -- both are "Planck".
  (2) Is Gemini's "mic-drop" (framework demands a RISING a0 that matches MUSE) correct?
      The a0(z) formula and Taylor step are algebraically right, but the CONCLUSION
      inverts the physics: it truncates a Taylor series at O(z) and drops wa, which is
      ~4x LARGER than (1+w0) and DOMINATES by z~0.4. On the framework's OWN canonical
      dark-energy-only footing (a0 ~ sqrt(rho_DE)), full DESI-CPL gives a small BUMP
      then a DECLINE -- NOT the near-doubling MUSE reports.  Verify both ways.
"""
import numpy as np
c   = 2.99792458e8
Mpc = 3.0856775814913673e22

def a0_of(H0_kms, OmL):
    H0 = H0_kms*1e3/Mpc                       # s^-1
    return c*H0*np.sqrt(3.0*OmL/(32.0*np.pi)) # m/s^2  (== c^2 sqrt(Lambda/32pi))

print("="*84)
print("(1) a0 value is an INPUT: a0 = c H0 sqrt(3 Omega_L / 32pi)")
print("="*84)
cases = [
 ("Carl canonical            ", 67.4 , 0.6847),
 ("Planck18 base TT+lowE+lens", 67.36, 0.6847),
 ("Planck18 +BAO (67.66)     ", 67.66, 0.6889),  # <- Gemini's neighborhood
 ("Planck18 Omega_L=0.69     ", 67.4 , 0.69  ),
 ("SH0ES-ish H0=73           ", 73.0 , 0.6847),
]
for name,H0,OmL in cases:
    print(f"  {name}: H0={H0:6.2f}, Om_L={OmL:.4f}  ->  a0 = {a0_of(H0,OmL)*1e11:.3f}e-11 m/s^2")
print("  => 9.36 vs 9.42 is a ~0.6% shift from which Planck (H0,Om_L) pair you plug in.")
print("     Same formula, different cosmological INPUT. NOT a derivation discrepancy.")
print("     (Memory: the VALUE is quarantined/not-derived; cH0-vs-cH_Lambda + param spread.)")

# ---- (2) exact CPL a0(z) vs Gemini's dropped-wa linear approx ----
def rhoDE_ratio(z, w0, wa):
    return (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*z/(1+z))
def a0_ratio_exact(z, w0, wa):          # a0(z)/a0(0) = sqrt(rho_DE ratio)  (canonical footing)
    return np.sqrt(rhoDE_ratio(z, w0, wa))
def a0_ratio_gemini(z, w0):             # Gemini's low-z Taylor, wa DROPPED
    return 1 + 1.5*(1+w0)*z

print("\n"+"="*84)
print("(2) a0(z)/a0(0) on the CANONICAL sqrt(rho_DE) footing -- EXACT vs Gemini's linear")
print("="*84)
param = [
 ("LambdaCDM (w0=-1, wa=0)      ", -1.00,  0.00),
 ("DESI-DR2-ish (-0.83,-0.75)   ", -0.83, -0.75),
 ("DESI-DR1-ish (-0.45,-1.79)   ", -0.45, -1.79),
 ("Gemini toy w0=-0.8 (+ real wa)", -0.80, -0.75),
]
zs = [0.4, 0.5, 1.0, 1.5, 2.0, 3.0]
print(f"  {'model':32s} " + "".join(f"z={z:<5.1f}" for z in zs))
for name,w0,wa in param:
    row = "".join(f"{a0_ratio_exact(z,w0,wa):<7.3f}" for z in zs)
    print(f"  EXACT {name}: {row}")
print("  " + "-"*78)
for w0 in (-0.8, -0.83, -0.45):
    row = "".join(f"{a0_ratio_gemini(z,w0):<7.3f}" for z in zs)
    print(f"  GEMINI-linear (drop wa) w0={w0:+.2f}      : {row}")

print("\n"+"="*84)
print("WHERE GEMINI GOES WRONG")
print("="*84)
w0,wa = -0.80,-0.75
for z in (0.5,1.0,1.5):
    ex = a0_ratio_exact(z,w0,wa); ge = a0_ratio_gemini(z,w0)
    print(f"  z={z}:  EXACT a0(z)/a0(0) = {ex:.3f}   |   Gemini linear = {ge:.3f}   "
          f"(off by {100*(ge-ex)/ex:+.0f}%)")
print("""
  * Gemini's a0(z) FORMULA and the wa-cancellation-at-first-order are algebraically fine.
  * BUT the linear a1-slope is valid only for z << 1, and wa (~-0.75) is ~4x bigger than
    (1+w0)(~+0.2). The O(z^2) term Gemini dropped is wa-driven and already dominates by
    z~0.4 -- exactly the MUSE/MSA-3D redshifts. Extrapolating the linear slope to z~1
    gives +30% when the EXACT canonical curve gives ~ -1% (a small bump then DECLINE).
  * So the framework's OWN dark-energy-only branch does NOT 'geometrically demand' the
    MUSE near-doubling. It predicts BUMP(~+4-6% near z~0.4)-THEN-DECLINE. MUSE's rise
    LEANS AGAINST it (as MSA-3D independently did) -- it is NOT a confirmation.
  * A strong RISE only appears under the RIVAL footing a0 ~ sqrt(rho_TOTAL) ~ H(z), which
    the canonical footing REJECTS. Gemini used the right footing then broke it to force a win.
""")
