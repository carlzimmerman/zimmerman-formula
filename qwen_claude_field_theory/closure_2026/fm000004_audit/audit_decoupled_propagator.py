#!/usr/bin/env python3
"""AUDIT of autoresearch survivor FM-000004 'Spatially Nonlocal F+ Screened Preferred-Frame with
Decoupled Propagator'. Central claim: a Maxwell vector A_mu carries a FIXED kinetic term, so 'the
finite propagating mode has a kinetic normalization NOT inherited from the screened preferred-frame
response' -> dodges P7. We test that claim on the mode that actually carries the preferred-frame
physics: the u-longitudinal polarization of A_mu. Signature mostly-minus (+,-,-,-)."""
import sympy as sp

t, x, y = sp.symbols('t x y', real=True)          # y = g/a0 (MOND variable); M^2 = screened coupling
k, M, s = sp.symbols('k M sigma', positive=True)   # k=|momentum|, M^2(y)=e^{-y} preferred-frame mass
sig, A0 = sp.symbols('sigma_amp A0', real=True)     # longitudinal amplitude, temporal component
sigd = sp.symbols('sigmadot', real=True)            # sigma-dot (time deriv of longitudinal potential)

print("=== FACT 1: Maxwell F_{mu nu} is IDENTICALLY BLIND to the longitudinal mode A_i = d_i sigma ===")
# In Fourier, longitudinal A_i = i k_i sigma. Spatial field strength F_ij = d_i A_j - d_j A_i:
ki, kj = sp.symbols('k_i k_j', real=True)
F_ij = (sp.I*ki)*(sp.I*kj*sig) - (sp.I*kj)*(sp.I*ki*sig)   # d_i A_j - d_j A_i on longitudinal
print(f"   F_ij[A=grad sigma] = {sp.simplify(F_ij)}   -> Maxwell gives the longitudinal mode NO -1/4 F_ij^2 kinetic term")

print("\n=== FACT 2: integrate out A_0 in ( -1/4 F^2 + 1/2 M^2 A_mu A^mu ), longitudinal sector ===")
# L_long = 1/2 k^2 (sigmadot - A0)^2  - 1/2 M^2 k^2 sigma^2 + 1/2 M^2 A0^2   (F_ij=0; mostly-minus Proca)
L = sp.Rational(1,2)*k**2*(sigd - A0)**2 - sp.Rational(1,2)*M**2*k**2*sig**2 + sp.Rational(1,2)*M**2*A0**2
A0_sol = sp.solve(sp.diff(L, A0), A0)[0]
print(f"   A_0 (non-dynamical, eliminated) = {sp.simplify(A0_sol)}")
L_eff = sp.simplify(L.subs(A0, A0_sol))
print(f"   L_eff(longitudinal) = {sp.simplify(L_eff)}")
K_long = sp.simplify(sp.expand(L_eff).coeff(sigd, 2))   # coefficient of sigmadot^2 (expand first!)
print(f"   ==> longitudinal KINETIC coefficient K_long = {K_long}")

print("\n=== FACT 3: behaviour of K_long as the screening turns off (solar system, y->inf, M^2=e^-y->0) ===")
K_short = sp.limit(K_long, k, sp.oo)                # short-wavelength (k>>M): probes the normalization
print(f"   short-wavelength limit (k>>M): K_long -> {K_short}   (== M^2, i.e. the SCREENED coupling)")
# substitute M^2 = e^{-y} and show -> 0
K_of_y = K_short.subs(M, sp.sqrt(sp.exp(-y)))
print(f"   with M^2 = e^-y : K_long -> {sp.simplify(K_of_y)} ; limit y->inf = {sp.limit(K_of_y, y, sp.oo)}")

print("\n=== FACT 4: canonical normalization + strong coupling scale ===")
# canonical field sigma_hat = sqrt(K_long)*sigma ~ M*sigma. An interaction g*O(sigma) becomes (g/M)*O(sigma_hat).
g = sp.symbols('g', positive=True)
Lambda_sc = sp.sqrt(K_short)                        # schematic: Lambda_sc ∝ sqrt(K_long) ∝ M ∝ e^{-y/2}
print(f"   canonical sigma_hat = sqrt(K_long)*sigma ~ M*sigma ; any vertex g -> g/M ~ g*e^{{y/2}}")
print(f"   strong-coupling scale Lambda_sc ∝ M(y) = e^(-y/2) -> 0 as y->inf")
for yv in [0, 5, 30, 60]:
    print(f"      y={yv:3d}:  e^(-y/2) = {float(sp.exp(-sp.Rational(yv,2))):.3e}")

print("\n=== VERDICT ===")
print("The Maxwell term normalizes ONLY the 2 transverse polarizations (frame-blind spectators;")
print("they carry no alpha_1,alpha_2 or u-dependent lensing). The u-LONGITUDINAL mode -- the one that")
print("carries the preferred-frame MOND physics -- gets K_long ∝ M^2 = e^-y from the SCREENED coupling,")
print("NOT from Maxwell (F_{mu nu} vanishes on it). So 'independent finite propagator' is FALSE for the")
print("physical mode: its normalization -> 0 exactly where alpha_1,alpha_2 are screened. P7 collision")
print("intact. Same wall as AeST (alpha_2) and the GW170817-collapsed khronometric endpoint.")
print('CERTIFICATE_JSON: {"gate":"G8","status":"KILL","certificate":"Decoupled-propagator claim holds '
      'only for transverse spectator modes. u-longitudinal polarization (carrier of preferred-frame '
      'MOND physics) has K_long=M^2 k^2/(k^2+M^2)->M^2=e^-y from the screened coupling; Maxwell F^2 '
      'vanishes on it identically, so provides no normalization. Lambda_sc ∝ e^{-y/2}->0 in solar '
      'system => strong coupling. P7 unbroken.","numeric_values":{"K_long_short":"M^2",'
      '"Lambda_sc_scaling":"e^{-y/2}"},"assumptions":["screened preferred-frame coupling acts as a '
      'field-dependent vector mass M^2(y)=e^-y on the u-projection (natural reading of a preferred-'
      'frame chi-A_mu order-phi^2 term)","transverse modes are frame-blind"]}')
