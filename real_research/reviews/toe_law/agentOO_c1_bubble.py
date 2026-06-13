"""
agentOO Route 1 — DIRECT ONE-LOOP SELF-ENERGY of the khronon chi in the dS horizon bath.

Goal: compute the real part of the one-loop self-energy Sigma(omega,k), put it ON-SHELL
(omega = c_chi k), Taylor-expand in k, and extract the induced k^4 coefficient sigma4 and its SIGN,
plus k^6. sigma4 < 0 = roton/bending (-> Airy fold, NN requirement). sigma4 >= 0 = convex (MM kill stands).

MODEL (concrete, tractable):
  - khronon perturbation chi: free dispersion omega = c_chi k  (linear, gapless Goldstone of the foliation).
  - bath = de Sitter horizon Gibbons-Hawking reservoir at T_dS = H/2pi, occupation
        n(w) = 1/(exp(2 pi w / H) - 1) = 1/(exp(w/T) - 1),  T = H/2pi.
    The bath quanta phi are the thermal modes of a relativistic bath with dispersion W(q) = c_b q
    (we vary c_b; the natural value is the bath sound/light speed). The thermal phase space is the
    Gibbons-Hawking Planck spectrum.
  - coupling: leading EFT operator. We START with the relevant scalar-trilinear  g chi phi phi /2
    (chi couples to a bath bilinear) -> one-loop "sunset/bubble" self-energy of chi from a thermal
    phi-phi loop. This is the cleanest in-medium self-energy and its thermal (finite-T) part is the
    PHYSICS that bends the dispersion.

The finite-T one-loop self-energy real part (standard thermal field theory, e.g. Kapusta-Gale,
Le Bellac) for chi(omega,k) from a phi-phi bubble has the structure

  Re Sigma_T(omega,k) = g^2 \int d^3q/(2pi)^3  * [ n(W_q) terms ] * (energy denominators).

We compute the STATIC and dynamic structure and Taylor-expand in k at fixed on-shell omega = c_chi k.

This file: build the thermal bubble integrand symbolically, then do the angular + radial integral
numerically with mpmath for a grid of k, and fit Re Sigma(k_onshell) = s0 + s2 k^2 + s4 k^4 + s6 k^6.
The SIGN of s4 (after the c_chi^2 renormalization is absorbed) is the deliverable.
"""
import numpy as np
import mpmath as mp
mp.mp.dps = 40

# ---- parameters (units H=1, so T_dS = 1/(2 pi)) ----
H = 1.0
T = H/(2*mp.pi)           # Gibbons-Hawking temperature
c_chi = mp.mpf('1.0')     # khronon sound speed (vary later)
c_b   = mp.mpf('1.0')     # bath mode speed
g     = mp.mpf('1.0')     # coupling (overall scale; sign of s4 is g^2>0 independent)

def nB(w):
    # Bose occupation at T_dS
    x = w/T
    if x > 60:
        return mp.e**(-x)
    return 1/(mp.e**x - 1)

# Bath dispersion
def Wq(q):
    return c_b*q

# ---------------------------------------------------------------------------
# One-loop bubble self-energy of chi from a thermal phi-phi loop.
# External: (omega, k). Loop momentum q. The two bath lines carry q and q+k (3-momenta),
# energies W_q = c_b q and W_{q+k} = c_b |q+k|.
# The retarded thermal self-energy real part (the part that shifts the dispersion) from the
# Landau/decay + scattering cuts, keeping the n(W) thermal weights, has the standard form
# (see Le Bellac "Thermal Field Theory" eq. for the scalar bubble):
#
#  Re Sigma_T(omega,k) = -g^2 \int d^3q/(2pi)^3 (1/(4 W_q W_{q+k})) *
#       [ (n(W_q)+n(W_{q+k}))*( 1/(omega - W_q - W_{q+k}) - 1/(omega + W_q + W_{q+k}) )
#        +(n(W_q)-n(W_{q+k}))*( 1/(omega - W_q + W_{q+k}) - 1/(omega + W_q - W_{q+k}) ) ] (PV)
#
# We take the principal value (real part) on-shell omega = c_chi k.
# ---------------------------------------------------------------------------

def ReSigma(omega, k):
    # integrate over q (radial) and angle (cos theta = x)
    omega = mp.mpf(omega); k = mp.mpf(k)
    def radial(q):
        Wq_ = Wq(q)
        def ang(x):
            qpk = mp.sqrt(q*q + k*k + 2*q*k*x)
            Wpk = Wq(qpk)
            denom_pref = 1/(4*Wq_*Wpk)
            n1 = nB(Wq_); n2 = nB(Wpk)
            # principal-value pieces; guard near-poles with a tiny imaginary part then take .real
            eps = mp.mpf('1e-12')
            def PV(z):
                return (z/(z*z+eps*eps))  # PV approx of 1/z
            t1 = (n1+n2)*( PV(omega-Wq_-Wpk) - PV(omega+Wq_+Wpk) )
            t2 = (n1-n2)*( PV(omega-Wq_+Wpk) - PV(omega+Wq_-Wpk) )
            return denom_pref*(t1+t2)*q*q   # q^2 from d^3q
        val = mp.quad(ang, [-1, 1])
        return val
    I = mp.quad(radial, [mp.mpf('1e-6'), 8, 30])
    # d^3q/(2pi)^3 = (1/(2pi)^3) * 2pi * q^2 dq dx = q^2 dq dx /(4 pi^2)
    pref = -g*g/(4*mp.pi**2)
    return pref*I

# ---- evaluate on-shell across a grid of small k and fit polynomial in k ----
print("# Re Sigma on-shell (omega = c_chi k), c_chi=%s c_b=%s T=%.5f" % (c_chi, c_b, float(T)))
ks = [mp.mpf(s) for s in ['0.05','0.10','0.15','0.20','0.25','0.30','0.40','0.50']]
vals = []
for k in ks:
    om = c_chi*k
    s = ReSigma(om, k)
    vals.append(s)
    print("k=%5.3f  ReSigma=% .8e" % (float(k), float(s)))

# Fit s0 + s2 k^2 + s4 k^4 + s6 k^6 (even powers; on-shell self-energy of a gapless mode)
A = np.array([[1, float(k)**2, float(k)**4, float(k)**6] for k in ks], dtype=float)
b = np.array([float(v) for v in vals], dtype=float)
coef, res, rk, sv = np.linalg.lstsq(A, b, rcond=None)
s0,s2,s4,s6 = coef
print("\n# polynomial fit Re Sigma(k) = s0 + s2 k^2 + s4 k^4 + s6 k^6")
print("s0 = % .6e" % s0)
print("s2 = % .6e   (renormalizes c_chi^2)" % s2)
print("s4 = % .6e   <--- sigma4 (SIGN is the deliverable)" % s4)
print("s6 = % .6e" % s6)
print("\nSIGN of sigma4:", "NEGATIVE (bending/roton)" if s4<0 else "POSITIVE/ZERO (convex/stiffening)")
