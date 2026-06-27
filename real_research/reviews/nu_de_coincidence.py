#!/usr/bin/env python3
"""
FRONT 1 -- THE NEUTRINO-DE COINCIDENCE + SCALE-GAP CLOSURE.

Carl's premise: the neutrino is the ONE SM sector where the framework's scale gap may CLOSE. Every prior
particle door died on the ~30-order gap between the a0/horizon scale (~1e-10) and SM masses (>=MeV-TeV).
But rho_DE^(1/4) ~ 2.3 meV sits RIGHT IN the neutrino-mass window (sqrt(splittings) ~ 8.6-50 meV;
Sigma m_nu floor 0.059 eV NO / 0.10 eV IO). This script COMPUTES, both-ways:

  (a) E_dS = rho_DE^(1/4) in eV, with rho_DE = Lambda c^2 / (8 pi G) [framework's pure-Lambda footing].
  (b) the neutrino mass scales from oscillation splittings + the Sigma floors.
  (c) the framework IR floor m_IR = hbar H_Lambda / c^2 (a graviton/condensate-mode floor mass).
  (d) the SCALE-GAP RATIO rho_DE^(1/4)/m for: lightest nu, the two splittings, the electron, and
      a0/(g of an atomic electron) -- to show the gap CLOSES (O(1)..O(10)) for nu and is ~1e30 for e.

NO mechanism is asserted here -- this front only quantifies the COINCIDENCE and whether the gap closes.
Footing: a0 = 9.36e-11 m/s^2, rho_DE = Lambda c^2/8piG, H_Lambda = 1.808e-18 /s, Lambda ~ 1.1e-52 m^-2.
"""
import math

# ---- fundamental constants (SI) -------------------------------------------------
c      = 2.99792458e8          # m/s
G      = 6.67430e-11           # m^3 kg^-1 s^-2
hbar   = 1.054571817e-34       # J s
eV     = 1.602176634e-19       # J
meV    = 1e-3 * eV

# ---- framework footing ----------------------------------------------------------
# Use H_Lambda directly (the de Sitter / pure-Lambda Hubble rate), then derive Lambda from it,
# so the whole chain is internally consistent with a0 = c H_Lambda / Z.
H_Lambda = 1.808e-18           # 1/s  (framework footing)
a0_fw    = 9.36e-11            # m/s^2 (framework footing)
Z        = c * H_Lambda / a0_fw # the framework normalization a0 = cH_Lambda/Z
# Lambda from H_Lambda:  Lambda = 3 H_Lambda^2 / c^2   (de Sitter: H^2 = Lambda c^2/3)
Lambda   = 3.0 * H_Lambda**2 / c**2          # m^-2
# NOTE on units: Lambda c^2/(8 pi G) has units of MASS density (kg/m^3), NOT energy density.
#   [Lambda]=1/m^2, [c^2]=m^2/s^2, [G]=m^3/kg/s^2  ->  Lambda c^2/G = kg/m^3.
# The ENERGY density is rho_DE = (Lambda c^2/8piG) * c^2  [J/m^3]. (This was a real bug caught at runtime:
#   forgetting the final c^2 makes E_dS come out ~18000x too small, 1.3e-7 eV instead of ~2.3 meV.)
rho_DE_mass = Lambda * c**2 / (8.0 * math.pi * G)   # kg/m^3  (mass density of the DE)
rho_DE      = rho_DE_mass * c**2                     # J/m^3   (ENERGY density)

print("="*92)
print("FRONT 1: neutrino <-> dark-energy scale coincidence and scale-gap closure")
print("="*92)
print(f"  H_Lambda       = {H_Lambda:.4e} /s")
print(f"  Z = cH_Lambda/a0 = {Z:.4f}   (framework normalization)")
print(f"  Lambda = 3H^2/c^2 = {Lambda:.4e} m^-2   (target ~1.1e-52)")
print(f"  rho_DE(mass) = Lambda c^2/8piG = {rho_DE_mass:.4e} kg/m^3")
print(f"  rho_DE(energy) = (...)*c^2      = {rho_DE:.4e} J/m^3")

# ---- E_dS = rho_DE^(1/4) as an ENERGY ------------------------------------------
# rho_DE [J/m^3]; convert to natural units where an energy density E^4 has E in Joules via
# E = ( rho_DE * (hbar c)^3 )^(1/4).   ( [J/m^3]*[J^3 m^3] = J^4 )
hbarc = hbar * c                                  # J*m
E_dS_J  = (rho_DE * hbarc**3) ** 0.25             # Joules
E_dS_eV = E_dS_J / eV                             # eV
print(f"\n  E_dS = rho_DE^(1/4) = {E_dS_J:.4e} J = {E_dS_eV*1e3:.4f} meV = {E_dS_eV:.5e} eV")
print(f"    (literature quotes ~2.3-2.4 meV for (rho_Lambda)^(1/4); cross-check)")

# ---- neutrino mass scales (oscillation data, NuFIT-class central values) --------
dm21_2 = 7.5e-5     # eV^2  (solar splitting)
dm31_2 = 2.5e-3     # eV^2  (atmospheric splitting)
sqrt_dm21 = math.sqrt(dm21_2)   # eV ~ 8.66 meV
sqrt_dm31 = math.sqrt(dm31_2)   # eV ~ 50 meV
Sigma_NO  = 0.059   # eV  minimal sum, normal ordering (lightest -> 0)
Sigma_IO  = 0.10    # eV  minimal sum, inverted ordering
# heaviest single eigenstate in the minimal NO case ~ sqrt(dm31_2)
m_heavy = sqrt_dm31

print("\n  neutrino mass scales (oscillations):")
print(f"    sqrt(Dm^2_21)  = {sqrt_dm21*1e3:.2f} meV   (solar splitting)")
print(f"    sqrt(Dm^2_31)  = {sqrt_dm31*1e3:.2f} meV   (atmospheric splitting; ~heaviest eigenstate, NO)")
print(f"    Sigma m_nu floor: NO >= {Sigma_NO*1e3:.0f} meV,  IO >= {Sigma_IO*1e3:.0f} meV")

# ---- framework IR floor m_IR = hbar H_Lambda / c^2 ------------------------------
m_IR_kg = hbar * H_Lambda / c**2     # kg
m_IR_eV = m_IR_kg * c**2 / eV        # eV  (= hbar H_Lambda in energy)
print(f"\n  framework IR floor m_IR = hbar H_Lambda / c^2 = {m_IR_eV:.4e} eV  (= {m_IR_eV*1e3:.3e} meV)")
print(f"    -> this is ~{E_dS_eV/m_IR_eV:.3e}x SMALLER than E_dS; it is the GRAVITON/horizon floor, NOT the nu scale")

# ---- electron, for contrast -----------------------------------------------------
m_e_eV = 510998.95   # eV

# ---- a0 / g for an atomic electron (Bohr ground state), for contrast -----------
# g = a0_centripetal of the 1s electron ~ e^2/(4 pi eps0 m_e a_B^2) -> just use a_B and v=alpha c
a_B = 5.29177210903e-11   # m  Bohr radius
alpha_fs = 7.2973525693e-3
v_e = alpha_fs * c
g_atomic = v_e**2 / a_B    # centripetal accel of 1s electron, m/s^2

print("\n" + "-"*92)
print("  SCALE-GAP RATIO  rho_DE^(1/4) / m   (how far the DE energy scale is from each mass):")
print("-"*92)
def ratio_line(label, m_eV):
    r = E_dS_eV / m_eV
    # log10 of the gap
    print(f"    {label:34s}: E_dS/m = {r:.3e}   (log10 = {math.log10(r):+.2f})")
ratio_line("sqrt(Dm^2_21) solar split",       sqrt_dm21)
ratio_line("sqrt(Dm^2_31) atmos split/heavy", sqrt_dm31)
ratio_line("Sigma_NO floor (0.059 eV)",       Sigma_NO)
ratio_line("Sigma_IO floor (0.10 eV)",        Sigma_IO)
ratio_line("electron (0.511 MeV)",            m_e_eV)

print("\n  for contrast, the GRAVITY-side gap (a0 vs an atomic electron's g):")
print(f"    g(1s electron)  = {g_atomic:.3e} m/s^2")
print(f"    a0 / g_atomic   = {a0_fw/g_atomic:.3e}   (log10 = {math.log10(a0_fw/g_atomic):+.2f})  <- the ~22-order MOND gap")

# ---- VERDICT block (computed) ---------------------------------------------------
print("\n" + "="*92)
print("VERDICT (computed) -- does the scale gap CLOSE for the neutrino?")
print("="*92)
r_solar = E_dS_eV/sqrt_dm21
r_atmos = E_dS_eV/sqrt_dm31
r_e     = E_dS_eV/m_e_eV
print(f"""  E_dS = rho_DE^(1/4) = {E_dS_eV*1e3:.3f} meV.
  * vs sqrt(Dm^2_21) = {sqrt_dm21*1e3:.1f} meV  -> ratio {r_solar:.2f}   (E_dS is ~{1/r_solar:.1f}x BELOW the solar split; SAME order)
  * vs sqrt(Dm^2_31) = {sqrt_dm31*1e3:.1f} meV  -> ratio {r_atmos:.3f}  (E_dS is ~{1/r_atmos:.0f}x BELOW the atmos split)
  * vs the electron               -> ratio {r_e:.2e}  (gap ~1e{math.log10(1/r_e):.0f}  -- the usual SM disaster)
  * gravity-side MOND gap a0/g_atomic ~ 1e{math.log10(a0_fw/g_atomic):.0f}.

  NET: For the NEUTRINO the gap is O(1)-O(20): E_dS = {E_dS_eV*1e3:.2f} meV is a factor {1/r_solar:.1f} below the
  SOLAR splitting (8.66 meV), {1/r_atmos:.0f}x below the ATMOSPHERIC splitting/heaviest eigenstate (50 meV),
  and ~{Sigma_NO/(E_dS_eV):.0f}x below the Sigma_NO floor. For the electron the gap is ~1e8; for an atomic electron's
  acceleration the gravity-side MOND gap is ~1e33. => The scale gap GENUINELY CLOSES for the neutrino
  sector and ONLY the neutrino sector. E_dS is NOT an O(1) match to a SINGLE nu mass -- it is best read
  as sitting at the BOTTOM of the neutrino tower: ~1/4 of the solar splitting, ~1/22 of the heaviest
  eigenstate -- the same order, off by ~1 power of ten at most. Whether this is mechanism or coincidence
  is Fronts 2-3; Front 1 certifies only this: the ~8-to-33-order gap that killed every other particle
  door is, for the neutrino, CLOSED to within ~1 order of magnitude.""")
