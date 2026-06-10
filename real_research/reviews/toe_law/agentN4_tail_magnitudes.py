#!/usr/bin/env python3
"""
agentN4: magnitude audit for the tail-literature map (agentN4_tail_literature.md).
Quantifies, with both Hubble footings where relevant (#1 working rule):
  [1] Haas-Poisson dS secular mass loss dm/dtau = -q^2 H^2 (Gaussian q^2; gr-qc/0411108
      Table II alpha=-1 with zeta = q^2 H / (2 m c^3) restored to SI) for a
      gravitational-strength scalar charge q^2 = G m^2 -> fractional inertia drift/Hubble.
  [2] The tail/Ricci velocity-force scale vs the MOND force scale (the cosmic-friction
      magnitude question: realize or exclude the N2/N5 structure?).
  [3] Orbital frequency of deep-MOND galactic orbits in units of H0 (the frequency-window
      mismatch with dS-IR enhancements that live at omega <~ H).
  [4] McCulloch QI (astro-ph/0612599) high-a tail vs Saturn ephemeris (Folkner 1e-14),
      same channel that killed F1/Milgrom-99 in MI_BATH_TAIL_CONSTRAINT.md.
  [5] Verlinde cH0/6 vs framework cH_Lambda/Z vs canonical a0 (adjacency, no claim).
  [6] Massive-kernel crossover: the Rindler/Deser-Levin suppression exponent 2*pi*m/kappa
      crosses O(1) at a ~ H for m ~ H (the decisive-calculation motivation).
No fetched data; pure unit arithmetic. C1/C2 only.
"""
import math

# --- constants (SI) ---
c   = 2.99792458e8
G   = 6.67430e-11
hbar= 1.054571817e-34
kB  = 1.380649e-23
Msun= 1.98892e30
mp  = 1.67262192e-27
AU  = 1.495978707e11
kpc = 3.0856775814913673e19
yr  = 3.155815e7

# --- both footings (repo convention; MEMORY #1 rule) ---
H0      = 70.0e3/ (kpc*1e3)        # 70 km/s/Mpc -> s^-1  (rho_total footing ~ cH0)
LambdaC = 1.1056e-52               # m^-2 (Planck-ish Lambda)
H_L     = c*math.sqrt(LambdaC/3.0) # "Lambda-only" H (rho_DE footing)
a0_fw   = 9.36e-11                 # framework a0 = c^2 sqrt(Lambda/32 pi)
a0_can  = 1.2e-10                  # canonical MOND a0
Z       = 5.789

print("=== footings ===")
print(f"H0      = {H0:.3e} s^-1   cH0      = {c*H0:.3e} m/s^2")
print(f"H_L     = {H_L:.3e} s^-1   cH_L     = {c*H_L:.3e} m/s^2")
print(f"a0_fw   = {a0_fw:.3e}      a0_can  = {a0_can:.3e}  (cH_L/Z = {c*H_L/Z:.3e})")

# [1] Haas-Poisson dS mass loss for gravitational-strength scalar charge
# dm/dtau = -q^2 H^2 (geometric, Gaussian force convention F = q^2/r^2)
# SI restore: q^2[N m^2] = G m^2  ->  dm/dtau = G m^2 H^2 / c^3  (kg/s)
print("\n=== [1] dS tail-induced secular inertia drift (Haas-Poisson, q^2 -> G m^2) ===")
for name, m in [("Sun", Msun), ("proton", mp), ("1 Msun star", Msun)]:
    for hn, H in [("H0", H0), ("H_L", H_L)]:
        rate = G*m*H/c**3          # fractional loss per Hubble time (= (1/m)(dm/dtau)*(1/H))
        print(f"  {name:12s} {hn:3s}: frac. inertia change per Hubble time = {rate:.2e}"
              f"   (need O(1) for MOND -> deficit {abs(math.log10(rate)):.0f} orders)")

# [2] velocity-force (cosmic friction / push) scale vs MOND force scale
# HP Eq.(5.4) scale: |F_self|/m ~ zeta * H * v (order, at t~O(1)); zeta = G m H / c^3.
print("\n=== [2] tail velocity-force scale vs MOND scale (Sun, v=220 km/s) ===")
v = 2.2e5
for hn, H in [("H0", H0), ("H_L", H_L)]:
    zeta = G*Msun*H/c**3
    a_anom = zeta*H*v
    print(f"  {hn}: zeta = {zeta:.2e};  |a_self| ~ zeta*H*v = {a_anom:.2e} m/s^2 "
          f" vs a0 = {a0_fw:.2e}  -> short by {abs(math.log10(a_anom/a0_fw)):.0f} orders")
print("  (kinematic 'cosmic dragging' -Hv is universal but is momentum redshift, not a force;")
print("   it is acceleration-blind and already in every GR/Newtonian cosmological calculation.)")

# [3] deep-MOND orbital frequency in units of H0
print("\n=== [3] frequency window of deep-MOND orbits ===")
for vrot in [80e3, 150e3, 220e3]:
    om = a0_fw/vrot                # omega = a/v at the a ~ a0 boundary
    print(f"  v = {vrot/1e3:3.0f} km/s: omega(a=a0) = {om:.2e} s^-1 = {om/H0:6.0f} H0"
          f"   (period {2*math.pi/om/yr/1e9:.2f} Gyr)")
print("  -> the kernel must deliver O(1) effects at omega ~ (1e2-1e3) H, where dS-IR")
print("     secular enhancements (which live at omega <~ H) do not operate.")

# [4] McCulloch QI tail vs Saturn (same channel as F1 kill)
# mu_QI = 1 - 2c^2/(|a| Theta), Theta = Hubble diameter = 2c/H -> 1-mu = cH/|a| (linear tail)
print("\n=== [4] McCulloch QI high-a tail vs Saturn ===")
gSat = G*Msun/(9.5826*AU)**2
for hn, H in [("H0", H0), ("H_L", H_L)]:
    dA = c*H            # constant anomalous acceleration implied by the linear 1/a tail
    print(f"  {hn}: delta_a(Saturn) = cH = {dA:.2e} m/s^2 vs Folkner 1e-14 -> x{dA/1e-14:,.0f}")
print(f"  (g_N(Saturn) = {gSat:.3e} m/s^2; same arithmetic class as F1's x54,000 kill.)")

# [5] Verlinde adjacency (number only, no claim)
print("\n=== [5] a0-from-horizon adjacencies ===")
print(f"  Verlinde cH0/6   = {c*H0/6:.3e} m/s^2")
print(f"  framework cH_L/Z = {c*H_L/Z:.3e} m/s^2 ; canonical 1.2e-10; Milgrom-99 2cH = {2*c*H_L:.2e}")

# [6] massive-kernel crossover: suppression exponent 2 pi m c^2 / (hbar * 2 pi kappa) ~ m c^2/(hbar kappa)
# For a field mass m_phi ~ hbar H / c^2 (the 'light in dS' scale), exponent ~ H/kappa -> O(1) at a ~ H.
print("\n=== [6] massive-kernel crossover scale ===")
for x in [0.1, 1.0, 5.789, 100.0]:
    kappa_over_H = math.sqrt(1+x**2)
    print(f"  a/cH = {x:7.3f}: kappa/H = {kappa_over_H:7.3f};  m_phi=hbar H/c^2 exponent m/kappa = "
          f"{1.0/kappa_over_H:.3f}")
print("  -> for m_phi ~ H the Boltzmann/Takagi suppression turns on exactly around a ~ cH:")
print("     the only known kernel class whose natural crossover sits at the MOND scale.")
