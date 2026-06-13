"""
agentRR Part 2 -- D2/D3: the OPERATING-POINT dispersion from the saturated, peaked self-energy.
Does the clamped saturated-gain response produce sigma6 >= sigma6* on the STABLE branch with k* at
the b->c_chi sonic edge?

Setup (QQ units): roton dispersion omega^2(k) = c^2 k^2 + sigma4 k^4 + sigma6 k^6, c=c_chi.
QQ banked: sigma4 < 0 (dS-bath bend, FORCED); no-ghost / bounded-fold threshold
    sigma6* = sigma4^2/(4 c^2),  = 1/16 in QQ's normalized units (c=1, sigma4=-1/2 there).
At sigma6 = sigma6* the inflection cubic factorizes to a triple root (soft sonic edge: omega(k*)=0,
v_g=0 at the edge). sigma6 > sigma6* => real inflection k*, omega^2(k*)>0, no ghost, retarded poles
in LHP (the stable bounded-fold window). sigma6 < sigma6* => ghost (continuum side, the wrong sign).

The PHYSICS: the saturated, PEAKED gain medium contributes a self-energy Sigma_sat(k) centered at a
gain-center k0 with width Gamma and clamped strength. Its REAL part (Kramers-Kronig partner of the
peaked Im) is dispersive and, expanded in k around the operating region, supplies the k^4 (sigma4) and
k^6 (sigma6) coefficients. We ask: does the saturated peak supply sigma6 >= sigma6*?

We model Re Sigma_sat(k) as the dispersive (real) response of a single clamped Lorentzian gain line.
A negative-residue (active) Lorentzian centered at k0 with width Gamma:
    chi(k) = -A * Gamma / ( (k^2 - k0^2) + i Gamma )     [intensity-form, k^2 variable]
Re chi(k) = -A*Gamma*(k^2-k0^2) / ((k^2-k0^2)^2 + Gamma^2).
The self-energy correction to omega^2 is delta(omega^2) = Re Sigma = +Re chi (sign set so the active
band lifts/bends per QQ). Expand omega^2(k) = c^2 k^2 + Re chi(k) about small k (the IR roton tower)
and READ OFF sigma4, sigma6. Then test sigma6 vs sigma6* = sigma4^2/(4 c^2).
"""
import sympy as sp

k, k0, Gam, A, c = sp.symbols('k k0 Gamma A c', positive=True, real=True)
u = sp.symbols('u', real=True)  # u = k^2

# negative-residue (active) Lorentzian dispersive part in the k^2 variable
# Re chi(u) = -A*Gam*(u-k0^2)/((u-k0^2)^2 + Gam^2)
Rechi = -A*Gam*(u - k0**2)/((u - k0**2)**2 + Gam**2)

# full omega^2 as function of u=k^2:  c^2 u + Rechi(u)
om2 = c**2*u + Rechi

# Taylor expand about u=0 (IR roton tower): omega^2 = a0 + a1 u + a2 u^2 + a3 u^3 + ...
# in k: u=k^2 so a1 u = a1 k^2 (=> c_eff^2), a2 u^2 = a2 k^4 (=> sigma4), a3 u^3 = a3 k^6 (=> sigma6)
ser = sp.series(om2, u, 0, 4).removeO()
ser = sp.expand(ser)
a0 = ser.coeff(u, 0)
a1 = ser.coeff(u, 1)   # -> c_eff^2 (coefficient of k^2)
a2 = ser.coeff(u, 2)   # -> sigma4  (coefficient of k^4)
a3 = ser.coeff(u, 3)   # -> sigma6  (coefficient of k^6)
print("omega^2(k) IR expansion (u=k^2):")
print("  a0 (const, gap)      =", sp.simplify(a0))
print("  a1 (-> c_eff^2, k^2) =", sp.simplify(a1))
print("  a2 (-> sigma4, k^4)  =", sp.simplify(a2))
print("  a3 (-> sigma6, k^6)  =", sp.simplify(a3))

c_eff2 = sp.simplify(a1)
sigma4 = sp.simplify(a2)
sigma6 = sp.simplify(a3)

# sign checks: QQ needs sigma4<0 (bend) and sigma6>0 (bounded fold). Which sign does the active
# Lorentzian give? Active = negative residue. Let's see.
print("\nsign of sigma4 (need <0 for bend):", sp.simplify(sigma4))
print("sign of sigma6 (need >0 for bound):", sp.simplify(sigma6))

# threshold: sigma6* = sigma4^2/(4 c_eff^2).  Compute sigma6 - sigma6* and factor.
sigma6_star = sigma4**2/(4*c_eff2)
margin = sp.simplify(sigma6 - sigma6_star)
print("\nsigma6* = sigma4^2/(4 c_eff^2) =", sp.simplify(sigma6_star))
print("MARGIN sigma6 - sigma6*  =", margin)
print("factored:", sp.factor(sp.simplify(margin)))

# also report sigma6*/c_eff structural and the ratio sigma6/sigma6*
ratio = sp.simplify(sigma6/sigma6_star)
print("\nratio sigma6/sigma6* =", ratio)
print("simplified:", sp.simplify(ratio))
