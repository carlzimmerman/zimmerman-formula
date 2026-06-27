#!/usr/bin/env python3
"""
FRONT 1 -- THE DARK-SECTOR SCALE. Does the framework (the swampland tower + the de Sitter horizon +
the ghost-condensate dark sector) hand the dark sector a SPECIFIC, FORCED mass, or only a FREE one?

Footing (memory-locked): a0 = cH_Lambda/Z, Z=sqrt(32pi/3) => a0 = 9.36e-11 m/s^2 (pure-Lambda).
We DO NOT use rho_total/cH0 (=1.13e-10, the wrong footing). de Sitter horizon scale H_Lambda from
a0 and Z. Everything below is COMPUTED, no scale put in by hand except the published comparison windows.

Both-ways mandate: a forced scale that lands in a viable DM window = a real dark-sector prediction
(NOT a TOE). A scale that is free (tower absolute = total field distance unobservable; ghost-condensate
amount I0 = the conserved shift-charge MEAN, robustly free) => SAY SO, do NOT manufacture a DM mass.

The candidate framework scales:
  (a) swampland tower absolute  m ~ M_Pl exp(-alpha phi_total)  [phi_total UNobservable => FREE]
  (b) the IR floor  m = hbar H_Lambda / c^2  [the lightest the horizon allows: COMPUTED]
  (c) rho_DE^(1/4) ~ 2.3 meV  [the dark-energy scale: COMPUTED]
  (d) the ghost-condensate dust mass M ~ 0.04-1 eV  [banked, but TUNED to Omega_dm, not derived]
Published DM windows to land in:
  fuzzy-DM Lyman-alpha lower bound ~ 2e-20 eV (Rogers-Peiris 2021 PRL 126 071302; strong-lens/streams 2.1e-21;
     UFD 3e-19) -- the naive 1e-22 eV fuzzy window is now DISFAVORED.
  warm-DM thermal ~ few keV; standard cold-DM/WIMP ~ GeV.
"""
import math

# ----- fundamental constants (SI), CODATA-ish -----
hbar = 1.054571817e-34      # J s
c    = 2.99792458e8         # m/s
G    = 6.67430e-11          # m^3 kg^-1 s^-2
eV   = 1.602176634e-19      # J
kpc  = 3.0856775814913673e19 # m
Mpc  = 1e3*kpc

# ----- framework footing (memory-locked) -----
a0   = 9.36e-11             # m/s^2  (= cH_Lambda/Z, pure-Lambda)
Z    = math.sqrt(32*math.pi/3)   # = 5.7928... the framework normalization
# a0 = c H_Lambda / Z  =>  H_Lambda = a0 Z / c
H_Lambda = a0 * Z / c       # s^-1, the de Sitter (Lambda-only) Hubble rate
# cross-check: cH_Lambda
cH_Lambda = c * H_Lambda

# reduced Planck mass
M_Pl_kg = math.sqrt(hbar*c/(8*math.pi*G))   # reduced, kg
M_Pl_J  = M_Pl_kg * c**2
M_Pl_eV = M_Pl_J / eV
M_Pl_GeV = M_Pl_eV/1e9

def J_to_eV(E): return E/eV
def kg_to_eV(m): return m*c**2/eV

print("="*96)
print("FRONT 1 -- THE DARK-SECTOR SCALE: forced or free? (all magnitudes COMPUTED, footing a0=9.36e-11)")
print("="*96)
print(f"  a0            = {a0:.3e} m/s^2   (memory-locked, = cH_Lambda/Z)")
print(f"  Z             = sqrt(32pi/3) = {Z:.4f}")
print(f"  H_Lambda      = a0*Z/c       = {H_Lambda:.4e} s^-1   (de Sitter / Lambda-only)")
print(f"  cH_Lambda     = {cH_Lambda:.4e} m/s^2   (sanity: = Z*a0 = {Z*a0:.4e})")
print(f"  M_Pl(reduced) = {M_Pl_GeV:.4e} GeV = {M_Pl_eV:.4e} eV")

print("\n--- (b) THE IR FLOOR  m = hbar H_Lambda / c^2  (lightest mass the horizon supports) ---")
m_IR_J  = hbar * H_Lambda                # rest energy hbar*H_Lambda (since E = hbar * (c/L) with L=c/H)
m_IR_eV = J_to_eV(m_IR_J)
# Compton wavelength of the IR-floor quantum
lam_IR  = hbar/(m_IR_eV*eV/c**2 * c)      # = hbar/(m c) ; m = m_IR_eV*eV/c^2
print(f"  m_IR = hbar*H_Lambda          = {m_IR_eV:.3e} eV")
print(f"  (Compton wavelength           = {lam_IR/Mpc:.3e} Mpc ~ the Hubble horizon, as expected)")

print("\n--- (c) THE DARK-ENERGY SCALE  rho_DE^(1/4) ---")
# rho_DE = Lambda c^2/(8 pi G), Lambda = 3 H_Lambda^2 / c^2  (Lambda-only de Sitter)
Lambda  = 3*H_Lambda**2/c**2             # m^-2
rho_DE  = Lambda * c**2 /(8*math.pi*G)   # kg/m^3  (energy density / c^2)
rho_DE_energy = rho_DE * c**2            # J/m^3
# rho_DE^(1/4) as an energy: (rho_DE_energy * (hbar c)^3)^(1/4) in J, then eV
E_DE = (rho_DE_energy * (hbar*c)**3)**0.25   # J
E_DE_eV = J_to_eV(E_DE)
print(f"  Lambda                        = {Lambda:.3e} m^-2")
print(f"  rho_DE (energy)               = {rho_DE_energy:.3e} J/m^3")
print(f"  rho_DE^(1/4)                  = {E_DE_eV*1e3:.3f} meV   = {E_DE_eV:.3e} eV")

print("\n--- (a) THE SWAMPLAND TOWER ABSOLUTE SCALE  m = M_Pl exp(-alpha phi_total/M_Pl) ---")
print("  phi_total (TOTAL field distance, pre-observable) is UNBOUNDED & UNOBSERVABLE from a0(z).")
print("  alpha (tower<->potential coefficient) is a model-dependent conjecture, not forced.")
# illustrate the sensitivity: a modest field distance scans the ENTIRE spectrum
for phi_tot, alpha in [(5,1),(20,1),(35,1),(60,1),(80,0.82)]:
    m = M_Pl_eV*math.exp(-alpha*phi_tot)
    print(f"    phi_total/M_Pl={phi_tot:>4}, alpha={alpha:<4}: m_tower(0) = {m:.2e} eV")
print("  => the absolute tower scale spans ~60 orders for O(1)-O(80) field distance: ABSOLUTE SCALE IS FREE.")

print("\n--- (d) THE GHOST-CONDENSATE DUST MASS  M ~ 0.04-1 eV (banked, TUNED not derived) ---")
print("  amount I0 = the conserved shift-charge = the MEAN of a shift-symmetric flat direction;")
print("  dS-Unruh/GH thermal physics sets only the VARIANCE => Omega_dust from thermal occupation")
print("  ~1e-72 (72 orders below 0.266). Fixable ONLY by an early-universe IC => I0 robustly FREE.")
M_gc_lo, M_gc_hi = 0.04, 1.0   # eV, banked window
print(f"  banked dust mass window: {M_gc_lo}-{M_gc_hi} eV  (set by matching Omega_dm, NOT forced)")

print("\n--- THE AeST/ghost-condensate FIELD MASS  mu  (1/mu ~ 1 Mpc, the Compton scale) ---")
# 1/mu ~ 1 Mpc is a Compton wavelength -> a mass m = hbar/(L c)
for L_Mpc in (1.0, 10.0):
    m_mu_eV = J_to_eV(hbar*c/(L_Mpc*Mpc))
    print(f"  1/mu = {L_Mpc:>4} Mpc  ->  m_mu = hbar/(L c) = {m_mu_eV:.3e} eV")
print("  (galaxy-forced 1/mu >~ tens of Mpc => even lighter; this is the Jeans/coherence scale, not a DM quantum)")

print("\n"+"="*96)
print("LANDING TABLE -- which COMPUTED framework scale lands in a viable DM window?")
print("="*96)
windows = [
    ("fuzzy-DM Lyman-alpha floor", 2e-20, "Rogers-Peiris 2021; lens/streams 2.1e-21; UFD 3e-19"),
    ("warm-DM thermal (few keV)",  3e3,   "thermal WDM transfer-fn cutoff"),
    ("cold-DM/WIMP (~GeV-TeV)",     1e9,   "standard CDM"),
]
scales = [
    ("(b) IR floor hbar H_Lambda/c^2", m_IR_eV),
    ("(c) rho_DE^(1/4)",               E_DE_eV),
    ("(d) ghost-condensate dust (lo)", M_gc_lo),
    ("(d) ghost-condensate dust (hi)", M_gc_hi),
]
fuzzy_floor = 2e-20
for label, m in scales:
    if m < fuzzy_floor:
        n = math.log10(fuzzy_floor/m)
        verdict = f"BELOW fuzzy floor by {n:.1f} dex -> free-streams, NOT viable DM"
    elif m < 3e3:
        verdict = "in [fuzzy floor, warm] -> COULD be viable ULDM IF amount were fixed"
    else:
        verdict = "above warm scale -> cold-like"
    print(f"  {label:34s} m={m:.3e} eV   {verdict}")

print("\n  NOTE: the (d) dust window 0.04-1 eV formally sits ABOVE the fuzzy floor (viable mass band),")
print("  BUT the mass M is itself TUNED to give Omega_dm; it is not forced, and the AMOUNT I0 is free.")
print("  So even (d) is NOT a forced prediction -- it is a fitted closure of a free 2-parameter sector.")

print("\n"+"="*96)
print("VERDICT (both-ways)")
print("="*96)
print("""  FORCED scales the framework actually computes:
     - IR floor hbar H_Lambda/c^2 ~ 1e-33 eV  -- but this is ~13 orders BELOW the fuzzy-DM floor (2e-20 eV):
       its Compton wavelength is the Hubble horizon, it free-streams on all sub-horizon scales => NOT viable DM.
     - rho_DE^(1/4) ~ 2.3 meV -- the dark-ENERGY scale, not a dark-MATTER quantum (it sets Lambda, w(z), a0(z)).
  FREE scales (the would-be DM masses):
     - swampland tower ABSOLUTE m_tower(0): set by phi_total (unobservable) and alpha => spans ~60 orders => FREE.
     - ghost-condensate dust M ~ 0.04-1 eV and its amount I0: both TUNED to Omega_dm, never derived => FREE.
  => NO forced framework mass lands inside [fuzzy floor 2e-20 eV, few keV warm]. The two scales the framework
     DOES force (IR floor, rho_DE^(1/4)) are dark-ENERGY-side and too light to be DM. The dark-MATTER mass is FREE.
  WHAT IS GENUINELY FORCED & TESTABLE is NOT a mass but a VARYING-MASS SIGNATURE: m_tower(z)/m_tower(0) =
     exp(-alpha Delta_phi(z)) DECLINES ~30-40% over z=0-3, locked to a0(z)=sqrt(rho_DE(z)) (the swampland-tower
     result). That is a real dark-sector prediction (conditional on alpha~lambda) -- the absolute scale is FREE,
     the variation is forced. Honest: forced VARIATION, free ABSOLUTE. Do NOT manufacture a DM mass.""")
