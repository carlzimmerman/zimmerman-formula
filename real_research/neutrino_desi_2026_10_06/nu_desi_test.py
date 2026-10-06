"""Test the labelled-speculation neutrino hypothesis m_lightest = rho_Lambda^(1/4)
against DESI DR2 (Elbers et al. 2025, arXiv:2503.14744; DESI DR2 Results II, arXiv:2503.14738).

Hypothesis (unforced, coefficient = 1 fitted by inversion): m_1 = rho_Lambda^(1/4), normal ordering.
Also adds a scale check: can isotropic background radiation (CMB photons, relic neutrinos)
push a star with anything near a0?

DESI numbers used (quoted from the papers' text, 2026-10-06):
  LCDM, DESI DR2 BAO + CMB:   sum m_nu < 0.0642 eV (95%), sigma = 0.020 eV
  Feldman-Cousins 95%:        sum m_nu < 0.053 eV
  lightest mass (NO):         m_l < 0.023 eV (95%)
  effective mass (may be <0): sum m_nu,eff = -0.101 +0.047 -0.056 eV (68%), 3.0 sigma below 0.059 eV
  w0wa CDM, DESI + CMB:       sum m_nu < 0.163 eV (95%)

MUTATE=1 plants the inverted-ordering floor (0.10 eV) as the hypothesis sum: the 95% LCDM
limit and the effective-mass tension must then FAIL, or the test cannot fail.
"""
import json, math, os

MUTATE = os.environ.get("MUTATE") == "1"
here = os.path.dirname(os.path.abspath(__file__))
tag = "_MUTATE" if MUTATE else ""

# physical constants (SI)
G, c, hbar, eV = 6.67430e-11, 2.99792458e8, 1.054571817e-34, 1.602176634e-19
Mpc = 3.0856775814913673e22

# Planck 2018 footing for rho_Lambda
H0, Om_L = 67.4e3 / Mpc, 0.6847
rho_crit = 3 * H0**2 / (8 * math.pi * G)                  # kg/m^3
u_L = Om_L * rho_crit * c**2                              # J/m^3
m1 = (u_L * (hbar * c) ** 3) ** 0.25 / eV                 # eV

# NuFIT 5.2 normal ordering (no SK atm)
dm21, dm31 = 7.41e-5, 2.511e-3
m2, m3 = math.sqrt(m1**2 + dm21), math.sqrt(m1**2 + dm31)
S_hyp = m1 + m2 + m3
S_NOmin = math.sqrt(dm21) + math.sqrt(dm31)
S_IOmin = math.sqrt(dm31) + math.sqrt(dm31 + dm21)        # approx IO floor (~0.10)

if MUTATE:
    S_hyp = S_IOmin

# DESI DR2
LIM95_LCDM, SIG_LCDM, FC95, ML95, LIM95_W0WA = 0.0642, 0.020, 0.053, 0.023, 0.163
EFF_MU, EFF_UP = -0.101, 0.047
EFF_TENSION_AT_059 = 3.0

# Gaussian (upper-side) distance of a sum from the effective-mass posterior.
def z_gauss(S):
    return (S - EFF_MU) / EFF_UP

# calibrate to DESI's stated 3.0 sigma at 0.059 (their posterior has heavier tails than
# the split-normal), then report the hypothesis relative to that anchor
z_hyp_raw, z_059_raw = z_gauss(S_hyp), z_gauss(0.059)
z_hyp_cal = EFF_TENSION_AT_059 * z_hyp_raw / z_059_raw
dz_vs_NOmin = (S_hyp - S_NOmin) / EFF_UP

# background-radiation push: dipole radiation pressure on a Sun moving at v through the CMB
T_cmb, a_rad = 2.7255, 7.565767e-16                       # K, J m^-3 K^-4
u_cmb = a_rad * T_cmb**4
v, Rsun, Msun = 220e3, 6.957e8, 1.989e30
F_cmb = (4.0 / 3.0) * u_cmb * (v / c) * math.pi * Rsun**2  # drag, opposite to motion
acc_cmb = F_cmb / Msun
# relic neutrinos: energy density (7/8)(4/11)^(4/3) * 3 species of photon value if massless;
# weak cross-section at meV ~1e-63 cm^2 per nucleon -> coupling vs photons on a star's surface is
# irrelevant; bound it generously by giving them photon-like full absorption.
u_nu = 3 * (7 / 8) * (4 / 11) ** (4 / 3) * u_cmb
acc_nu_bound = (4.0 / 3.0) * u_nu * (v / c) * math.pi * Rsun**2 / Msun
a0_low, a0_high = 9.36e-11, 1.13e-10

checks = []
def check(name, ok, val):
    checks.append({"name": name, "pass": bool(ok), "value": val})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {val}")

print(f"rho_Lambda^(1/4) = {m1*1e3:.3f} meV   masses (meV): {m1*1e3:.2f} {m2*1e3:.2f} {m3*1e3:.2f}")
print(f"sum (hypothesis{' = IO floor, MUTATE' if MUTATE else ''}) = {S_hyp:.4f} eV; min NO = {S_NOmin:.4f}; min IO = {S_IOmin:.4f}")
check("D1 lightest mass under DESI m_l < 0.023 eV (95%, NO)", m1 < ML95, round(m1, 5))
check("D2 sum under DESI LCDM 95% limit 0.0642 eV", S_hyp < LIM95_LCDM,
      f"{S_hyp:.4f} vs 0.0642 (margin {LIM95_LCDM - S_hyp:+.4f} eV = {(LIM95_LCDM - S_hyp)/SIG_LCDM:+.2f} sigma_LCDM)")
check("D3 sum under Feldman-Cousins 95% limit 0.053 eV", S_hyp < FC95, f"{S_hyp:.4f} vs 0.053")
check("D4 sum under w0wa 95% limit 0.163 eV", S_hyp < LIM95_W0WA, f"{S_hyp:.4f} vs 0.163")
check("D5 effective-mass tension < 3 sigma (calibrated to DESI's 3.0 at 0.059)", z_hyp_cal < 3.0,
      f"{z_hyp_cal:.2f} sigma (raw split-normal {z_hyp_raw:.2f}; 0.059 raw {z_059_raw:.2f})")
print(f"     hypothesis vs minimal NO: {S_hyp - S_NOmin:+.4f} eV = {dz_vs_NOmin:+.3f} sigma{' -> DESI cannot tell them apart' if abs(dz_vs_NOmin) < 0.5 else ''}")
check("R1 CMB radiation drag on a Sun at 220 km/s is < 1e-6 a0", acc_cmb < 1e-6 * a0_low,
      f"{acc_cmb:.2e} m/s^2 = {acc_cmb/a0_low:.1e} a0 (and it points against the motion, not to the centre)")
check("R2 relic-neutrino push (full-absorption bound) < 1e-6 a0", acc_nu_bound < 1e-6 * a0_low,
      f"{acc_nu_bound:.2e} m/s^2 = {acc_nu_bound/a0_low:.1e} a0")

out = {"hypothesis": "m_lightest = rho_Lambda^(1/4), normal ordering (labelled speculation)",
       "mutate": MUTATE, "m1_eV": m1, "masses_eV": [m1, m2, m3], "sum_eV": S_hyp,
       "sum_NOmin_eV": S_NOmin, "sum_IOmin_eV": S_IOmin, "z_eff_calibrated": z_hyp_cal,
       "z_eff_raw": z_hyp_raw, "dz_vs_NOmin": dz_vs_NOmin, "acc_cmb": acc_cmb,
       "acc_nu_bound": acc_nu_bound, "checks": checks,
       "sources": ["arXiv:2503.14744", "arXiv:2503.14738"]}
json.dump(out, open(os.path.join(here, f"nu_desi_results{tag}.json"), "w"), indent=1)
n = sum(ch["pass"] for ch in checks)
print(f"{n}/{len(checks)} pass")
