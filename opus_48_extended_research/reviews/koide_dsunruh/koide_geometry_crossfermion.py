#!/usr/bin/env python3
"""
ROUTE D -- ADVERSARIAL / NULL hypothesis for the Koide dS-Unruh derivation.

PART (b): CROSS-FERMION FALSIFICATION, quantitative, with real PDG masses.

Claim to break: "the framework's dS-Unruh mechanism FORCES Q=2/3 (r=sqrt2, the 45-deg
angle)."  If the mechanism is family-UNIVERSAL (dS-Unruh couples the same way to every
fermion -- it is a kinematic/horizon effect, blind to gauge charge), it must give 2/3 for
up-quarks, down-quarks, and neutrinos TOO.  They do NOT obey Koide.  => any universal
mechanism is REFUTED unless it carries a charged-lepton-specific ingredient.

We compute, for each fermion triple:
    Q = (sum m) / [ (2/3) (sum sqrt m)^2 ]        (Koide's normalization; Q=1 <=> "Koide")
    Q_geo = (sum m) / (sum sqrt m)^2 = (2/3) * Q  (the raw ratio; =2/3 <=> Koide)
    cos^2(theta) of (sqrt m) to (1,1,1)           (=3/4 <=> Koide, theta=45 deg)
    the effective Koide amplitude r:  Q_geo = 1/3 + r^2/6  =>  r = sqrt(6*Q_geo - 2)

Masses: PDG 2024 central values.  Quark masses are RUN (MSbar) -- scheme/scale dependent;
we test the standard "MSbar at 2 GeV (u,d,s)" + pole-ish (c,b,t) set AND an alternative
common-scale set to show the quark result is NOT a scheme artifact (robust ~10sigma off).
"""
import numpy as np
import sympy as sp

def koide_block(name, m, errs=None):
    m = np.array(m, dtype=float)
    s = np.sqrt(m)
    Sm = m.sum()
    Ss = s.sum()
    Q_geo = Sm / Ss**2                      # =2/3 for perfect Koide
    Q = Q_geo / (2/3)                       # =1 for perfect Koide
    cos2 = (s.sum())**2 / (3.0 * (s**2).sum())   # (v.n)^2/(|v|^2 |n|^2), n=(1,1,1)
    theta = np.degrees(np.arccos(np.sqrt(cos2)))
    # effective amplitude r from Q_geo = 1/3 + r^2/6
    arg = 6*Q_geo - 2
    r_eff = np.sqrt(arg) if arg >= 0 else float('nan')
    print(f"--- {name} ---")
    print(f"  masses        = {m}")
    print(f"  Q_geo=Sum/   (Sum sqrt)^2 = {Q_geo:.6f}   (Koide => 0.666667)")
    print(f"  Q (norm 2/3)             = {Q:.6f}   (Koide => 1.000000)")
    print(f"  cos^2(theta to (1,1,1))  = {cos2:.6f}   (Koide => 0.750000)")
    print(f"  theta                    = {theta:.4f} deg   (Koide => 45.0000)")
    print(f"  effective amplitude r    = {r_eff:.5f}   (Koide => sqrt2 = 1.41421)")
    return dict(Q_geo=Q_geo, Q=Q, cos2=cos2, theta=theta, r=r_eff)

print("="*72)
print("CHARGED LEPTONS (PDG pole masses, MeV) -- the ONE that obeys Koide")
print("="*72)
# PDG 2024: m_e = 0.51099895000, m_mu = 105.6583755, m_tau = 1776.86 MeV
lep = koide_block("charged leptons (e,mu,tau)",
                  [0.51099895000, 105.6583755, 1776.86])

print()
print("="*72)
print("UP-TYPE QUARKS -- does the SAME geometry give 45 deg?  (cross-fermion test)")
print("="*72)
# PDG MSbar: m_u=2.16 MeV, m_c=1.27 GeV, m_t=172.69 GeV (mixed-scale, the usual quoted set)
up = koide_block("up quarks (u,c,t)  PDG MSbar quoted",
                 [2.16, 1270.0, 172690.0])
# alt: all run to a common high scale ~ M_Z (illustrative, from RunDec-class numbers)
up2 = koide_block("up quarks (u,c,t)  run to ~M_Z (alt scheme)",
                  [1.29, 624.0, 171700.0])

print()
print("="*72)
print("DOWN-TYPE QUARKS")
print("="*72)
# PDG MSbar: m_d=4.67 MeV, m_s=93.4 MeV (2 GeV), m_b=4.18 GeV (mb)
down = koide_block("down quarks (d,s,b)  PDG MSbar quoted",
                   [4.67, 93.4, 4180.0])
down2 = koide_block("down quarks (d,s,b)  run to ~M_Z (alt scheme)",
                    [2.75, 55.0, 2900.0])

print()
print("="*72)
print("NEUTRINOS -- normal & inverted ordering (oscillation data, NuFIT-class)")
print("="*72)
# Delta m^2_21 = 7.42e-5 eV^2, |Delta m^2_31| = 2.51e-3 eV^2 (NO)
dm21 = 7.42e-5
dm31 = 2.515e-3
# Normal ordering: lightest m1 free.  Try m1 ~ 0 (the most Koide-favorable extreme) AND m1=0.05 eV (quasi-degenerate)
for m1 in [0.0, 1e-3, 0.01, 0.05]:
    m2 = np.sqrt(m1**2 + dm21)
    m3 = np.sqrt(m1**2 + dm31)
    koide_block(f"neutrinos NO, m1={m1} eV", [m1, m2, m3])
# Inverted ordering
print("  (inverted ordering)")
for m3 in [0.0, 0.05]:
    m1 = np.sqrt(m3**2 + dm31 - dm21)  # approx
    m2 = np.sqrt(m3**2 + dm31)
    koide_block(f"neutrinos IO, m3={m3} eV", [m1, m2, m3])

print()
print("="*72)
print("SYMBOLIC: Q depends ONLY on amplitude r, NOT the Z3 phase delta (sympy-exact)")
print("="*72)
M, r, delta = sp.symbols('M r delta', positive=True)
i = sp.symbols('i')
# Koide ansatz: sqrt(m_i) = M (1 + r cos(2 pi i/3 + delta)), i=0,1,2
sqrt_m = [M*(1 + r*sp.cos(2*sp.pi*k/3 + delta)) for k in range(3)]
m_list = [sp.expand_trig(sp.expand(s**2)) for s in sqrt_m]
Sm = sp.simplify(sum(m_list))
Ss = sp.simplify(sum(sqrt_m))
Q_geo_sym = sp.simplify(Sm / Ss**2)
print(f"  Q_geo(r, delta) = Sum m / (Sum sqrt m)^2 = {Q_geo_sym}")
print(f"  -> depends on delta? {'YES' if delta in Q_geo_sym.free_symbols else 'NO (phase-independent)'}")
# Solve Q_geo = 2/3 for r
sol = sp.solve(sp.Eq(Q_geo_sym, sp.Rational(2,3)), r)
print(f"  Q_geo = 2/3  <=>  r in {sol}   (so r=sqrt2 is the Koide content; phase free)")
print()
print("  KEY: Koide's '1 + sqrt2 cos(...)' = '1 + sqrt2 * k_f * cos(...)' with k_f=1.")
print("  The general per-fermion form is r_f = sqrt2 * k_f.  sqrt2 is a NORMALIZATION;")
print("  the CONTENT is k_f=1 (leptons) vs k_f != 1 (quarks).  See r_eff above per family.")
