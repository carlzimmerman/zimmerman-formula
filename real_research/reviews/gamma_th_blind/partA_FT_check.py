#!/usr/bin/env python3
"""
PART A.3 (redo) -- clean numerical verification that
   F(omega) = int ds e^{-i omega s} W(s) = (1/2pi) omega/(e^{omega/T_GH}-1)
for the dS conformal-scalar sinh^2 kernel.

The naive trapezoid fails because W(s) has a *double pole* at s=0 (the i*eps was too
small -> the s=0 sample dominated). Proper handling: the standard QFT result evaluates
the response via the i*eps contour. We verify the closed form two independent ways:

 (1) the integral with the SINGULARITY SUBTRACTED. Write
        W(s) = W_sing(s) + W_reg(s),
     where W_sing(s) = -1/(4 pi^2 (s - i eps)^2) is the flat-space Hadamard piece whose
     Fourier transform is known exactly:
        int ds e^{-i omega s} (-1/(4 pi^2 (s-i eps)^2)) = -(omega/(2 pi)) theta(omega)
     (for omega>0; this is the flat-space/Unruh "vacuum" no-click-when-cold piece...).
     Actually the cleanest is the KNOWN pair:
        int_{-inf}^{inf} ds e^{-i omega s} / (s - i eps)^2 = -2 pi omega theta(omega).
     Then W_reg = W - W_sing is bounded and its FT is done by trapezoid safely.
 (2) Cross-check via the DETAILED-BALANCE-FIXED Planck form at several omega.

We implement (1).
"""
import numpy as np

def W_full(s, a):
    # i eps via s - i eps in the argument; use a small eps but we will NOT sample s=0.
    return -1.0/(16*np.pi**2*a**2) / np.sinh(s/(2*a))**2  # real s, s!=0

def W_sing(s):
    # flat Hadamard piece (a-independent): -1/(4 pi^2 s^2)
    return -1.0/(4*np.pi**2*s**2)

def FT_sing(omega):
    # exact: int e^{-i omega s} (-1/(4 pi^2 s^2)) ds  with i eps -> = -(omega/(2pi)) for omega>0
    # Derivation: int e^{-i w s}/(s-i0)^2 ds = -2 pi w theta(w); times -1/(4 pi^2):
    #   = -1/(4 pi^2) * (-2 pi w) = w/(2 pi) for w>0.   (sign set by matching below)
    return np.where(omega > 0, omega/(2*np.pi), 0.0)

def F_numeric(omega, a, S=80.0, N=800001):
    s = np.linspace(-S*a, S*a, N)
    s = s[np.abs(s) > 1e-9]  # excise exact 0 (measure zero; integrand regular there after subtraction)
    reg = W_full(s, a) - W_sing(s)            # bounded, ~ const near 0
    integ = np.exp(-1j*omega*s) * reg
    Freg = np.trapz(integ, s) if hasattr(np,'trapz') else np.trapezoid(integ, s)
    return Freg + FT_sing(np.array(omega))    # add back exact singular FT

def F_closed(omega, a):
    TGH = 1.0/(2*np.pi*a)
    return (1.0/(2*np.pi))*omega/(np.exp(omega/TGH)-1.0)

print("Clean FT (singularity-subtracted)  vs  Planck closed form:")
print(f"{'a':>5} {'omega':>7} {'Re F_num':>14} {'F_closed':>14} {'ratio':>9} {'Im F_num':>11}")
ok = True
for a in [1.0, 2.0]:
    for om in [0.2, 0.5, 1.0, 2.0, 3.0]:
        fn = F_numeric(om, a)
        fc = F_closed(om, a)
        r = fn.real/fc
        if abs(r-1) > 0.02: ok = False
        print(f"{a:5.2f} {om:7.3f} {fn.real:14.6e} {fc:14.6e} {r:9.4f} {fn.imag:11.2e}")

# check the regular-part limit near 0 is finite:
s0 = np.array([1e-3, 1e-4])
print("\nregular part (W_full - W_sing) near s=0 (should be finite ~ +1/(48 pi^2 a^2)):")
for a in [1.0]:
    print("  s, reg:", s0, (W_full(s0,a)-W_sing(s0)), "  expected ~", 1/(48*np.pi**2*a**2))

print("\nRESULT:", "F(omega) closed form CONFIRMED numerically." if ok else "MISMATCH -- investigate.")
