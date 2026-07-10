#!/usr/bin/env python3
"""
LANE 1 -- THE BATH'S OWN ENERGY (source-lensing candidate audit)

Candidate mechanism: the de Sitter-Unruh radiation bath at the Deser-Levin
temperature T(a(r)) carries real energy density that clusters where a(r) is
large, and that energy density gravitates as the effective lensing source.

Framework premises (Carl's, reasoned from ON THEIR OWN TERMS):
  - modified INERTIA, a0 = cH_Lambda/Z, canonical a0 = 9.36e-11 m/s^2 (Z=5.79)
    alt footing a0 = 1.13e-10 m/s^2 (rho_total / cH0 footing)
  - Deser-Levin temperature: T(a) = (hbar / (2 pi kB c)) * sqrt(a^2 + (c H_L)^2)
    with c H_L = Z * a0
  - RAR: g_obs = sqrt(g_bar^2 + g_bar a0); nu(y) = sqrt(1 + 1/y), y = g_bar/a0

REQUIRED TARGET (what any source mechanism must supply):
  rho_eff(r) = (1/4piG) div[(nu-1) g_bar]  ==>  M_eff(r) = M_bar (nu(y) - 1)
  deep-MOND: M_eff -> sqrt(a0 M_bar / G) * r  (isothermal-like)

Tests:
 (1) Stefan-Boltzmann rho_bath(r) = a_rad T(a(r))^4 / c^2 vs rho_eff(r)
 (2) The EXCESS above the horizon floor: a_rad (T(a)^4 - T(0)^4)/c^2 vs rho_eff
 (3) Most generous variant: if the bath carried the FULL local dark-energy
     density rho_Lambda redistributed, what concentration factor
     rho_eff/rho_Lambda is needed at 10-50 kpc?

Both footings. Honest orders-of-magnitude, no softening.
"""
import numpy as np

# ---------- constants (SI) ----------
G      = 6.674e-11        # m^3 kg^-1 s^-2
c      = 2.998e8          # m/s
hbar   = 1.0546e-34       # J s
kB     = 1.3807e-23       # J/K
a_rad  = 7.5657e-16       # J m^-3 K^-4  (radiation constant, 4*sigma/c)
Msun   = 1.989e30         # kg
kpc    = 3.0857e19        # m

Z      = 5.79
rho_Lambda = 6.0e-27      # kg/m^3  (Lambda c^2 / 8 pi G, framework value)

FOOTINGS = {
    "canonical (rho_DE, cH_Lambda)": 9.36e-11,
    "alt (rho_total, cH0)":          1.13e-10,
}

M_bar = 1.0e11 * Msun

def nu(y):
    return np.sqrt(1.0 + 1.0/y)

def run_footing(label, a0):
    cH = Z * a0                      # the horizon acceleration scale c*H_Lambda
    T_coeff = hbar / (2*np.pi*kB*c)  # K per (m/s^2)
    T_floor = T_coeff * cH           # T(a=0): the pure-horizon floor

    print("="*100)
    print(f"FOOTING: {label}   a0 = {a0:.3e} m/s^2,  cH = Z*a0 = {cH:.3e} m/s^2")
    print(f"  Deser-Levin coefficient hbar/(2 pi kB c) = {T_coeff:.4e} K/(m s^-2)")
    print(f"  Horizon-floor temperature T(0) = {T_floor:.4e} K")
    print("="*100)

    # radial grid for derivative (dense), report grid
    r_all = np.logspace(np.log10(1*kpc), np.log10(500*kpc), 200000)
    r_report = np.array([5, 10, 20, 50, 100, 300]) * kpc

    g_bar = G * M_bar / r_all**2
    y = g_bar / a0

    # REQUIRED effective source: M_eff(r) = M_bar (nu - 1);
    # rho_eff = (1/4 pi r^2) dM_eff/dr
    M_eff = M_bar * (nu(y) - 1.0)
    dMdr = np.gradient(M_eff, r_all)
    rho_eff_all = dMdr / (4*np.pi*r_all**2)

    # Bath: the acceleration entering Deser-Levin. On the framework's own
    # terms the test particle's actual acceleration is g_obs; use g_obs
    # (this is the GENEROUS choice -- g_obs >= g_bar). Also note using g_bar
    # changes nothing at the orders involved.
    g_obs = np.sqrt(g_bar**2 + g_bar*a0)
    T_bath = T_coeff * np.sqrt(g_obs**2 + cH**2)
    rho_bath_all   = a_rad * T_bath**4 / c**2
    rho_excess_all = a_rad * (T_bath**4 - T_floor**4) / c**2

    print(f"{'r[kpc]':>7} {'g_bar':>10} {'y':>9} {'T_bath[K]':>11} "
          f"{'rho_eff':>11} {'rho_bath':>11} {'bath/eff':>10} "
          f"{'rho_excess':>11} {'exc/eff':>10} {'eff/rhoL':>9}")
    results = []
    for rr in r_report:
        i = np.argmin(np.abs(r_all - rr))
        re_, rb, rx = rho_eff_all[i], rho_bath_all[i], rho_excess_all[i]
        ratio_b = rb / re_
        ratio_x = rx / re_
        conc = re_ / rho_Lambda
        results.append((rr/kpc, re_, rb, rx, ratio_b, ratio_x, conc))
        print(f"{rr/kpc:>7.0f} {g_bar[i]:>10.2e} {y[i]:>9.3f} {T_bath[i]:>11.3e} "
              f"{re_:>11.3e} {rb:>11.3e} {ratio_b:>10.1e} "
              f"{rx:>11.3e} {ratio_x:>10.1e} {conc:>9.1e}")

    # sanity: deep-MOND analytic check M_eff -> sqrt(a0 M G)/G * r ... i.e.
    # rho_eff -> sqrt(a0 M_bar/G) / (4 pi r^2)
    i = np.argmin(np.abs(r_all - 100*kpc))
    rho_deepmond = np.sqrt(a0*M_bar/G) / (4*np.pi*r_all[i]**2)
    assert abs(rho_deepmond/rho_eff_all[i] - 1) < 0.15, "deep-MOND sanity failed"
    print(f"  [sanity] deep-MOND analytic rho_eff at 100 kpc: {rho_deepmond:.3e} "
          f"vs numeric {rho_eff_all[i]:.3e}  (ratio {rho_deepmond/rho_eff_all[i]:.3f})  OK")

    # (1)/(2) shortfall in orders at 10 kpc and 100 kpc
    for rr in (10*kpc, 100*kpc):
        i = np.argmin(np.abs(r_all - rr))
        sh_b = np.log10(rho_eff_all[i]/rho_bath_all[i])
        sh_x = np.log10(rho_eff_all[i]/rho_excess_all[i])
        print(f"  SHORTFALL at {rr/kpc:.0f} kpc: full bath {sh_b:.1f} orders; "
              f"excess-above-floor {sh_x:.1f} orders")

    # (3) concentration factor needed if the bath carried FULL rho_Lambda
    print("  (3) If the bath carried the FULL rho_Lambda locally redistributed:")
    for rr in (10*kpc, 20*kpc, 50*kpc):
        i = np.argmin(np.abs(r_all - rr))
        print(f"      r={rr/kpc:>3.0f} kpc: needed concentration rho_eff/rho_Lambda "
              f"= {rho_eff_all[i]/rho_Lambda:.2e}")
    return results

for label, a0 in FOOTINGS.items():
    run_footing(label, a0)

print()
print("VERDICT NOTES (computed above):")
print(" - The Deser-Levin bath temperature is ~4e-30 K in a galaxy; Stefan-Boltzmann")
print("   energy density ~ T^4 is ~1e-149..1e-150 kg/m^3 -- versus a required")
print("   rho_eff of ~1e-21..1e-24 kg/m^3. The shortfall is >120 orders of magnitude.")
print(" - The excess above the horizon floor is even smaller (the a^2 correction is")
print("   fractional at these radii), so variant (2) is strictly worse or comparable.")
print(" - Variant (3): even granting the bath the ENTIRE dark-energy density locally,")
print("   the mechanism needs a ~1e3-1e5x concentration of vacuum energy at 10-50 kpc,")
print("   with the specific radial profile 1/r^2 * sqrt(M_bar) -- no framework")
print("   ingredient (passive frame, 0 dof; K(Box_u) response; Herglotz measure)")
print("   supplies ANY vacuum-energy clustering, let alone 1e4-1e5x with that profile.")
