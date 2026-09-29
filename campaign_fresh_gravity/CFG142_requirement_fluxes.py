#!/usr/bin/env python3
"""CFG142 pre-data table (written with the frozen criteria, before any GOODS-ALMA cross-match result is seen).

For each of the ten rotation-supported KURVS-CDFS discs: the 1.1-mm flux S_req that the dust continuum would show if the
disc held the gas CFG141's P2 model requires, mu_total = M_gas/M* = 4, read through Scoville et al. 2016 (ApJ 820, 83;
eqs. A4 and A8 with alpha_850 = 6.7e19 erg/s/Hz/Msun):
    M_ISM = 1.78 S[mJy] (1+z)^-4.8 (nu_850/nu_obs)^3.8 (Gamma_0/Gamma_RJ) (d_L/Gpc)^2 x 1e10 Msun,
    Gamma_RJ = x/(e^x - 1), x = h nu_obs (1+z)/(k T_d),  Gamma_0 = Gamma_RJ(T_d, nu_850, z = 0),  T_d = 25 K.
The generous end (gas-to-dust x 2 for sub-solar metallicity, so mu_dust = 2; and M* 0.2 dex below MAGPHYS) gives
S_req,gen = S(mu_dust = 2) x 10^-0.2, the hardest to exclude; the nominal end is S(mu_dust = 4).
Pre-data orientation only: nu_obs = c/1.1 mm here; the scoring uses the survey's stated frequency with the same code.
MUTATE=1 doubles the dust temperature (50 K): the fluxes change and the Gamma_0 check (C-b) must fail, exit 1.
"""
import csv
import math
import os

h, k, c = 6.62607015e-34, 1.380649e-23, 2.99792458e8
TD = 50.0 if os.environ.get("MUTATE", "0") == "1" else 25.0
NU850, NUOBS = c / 850e-6, c / 1.1e-3
H0, OM = 67.66, 0.30966            # Planck18 (astropy's Planck18 values)


def d_l_gpc(z, n=20000):
    s = sum(1.0 / math.sqrt(OM * (1 + z * (i + 0.5) / n) ** 3 + 1 - OM) for i in range(n)) * z / n
    return (1 + z) * c / 1e3 / H0 * s / 1e3


def gam(nu, z):
    x = h * nu * (1 + z) / (k * TD)
    return x / math.expm1(x)


def s_mjy(m_ism, z):
    per_mjy = 1.78 * (1 + z) ** -4.8 * (NU850 / NUOBS) ** 3.8 * (gam(NU850, 0) / gam(NUOBS, z)) * d_l_gpc(z) ** 2 * 1e10
    return m_ism / per_mjy


here = os.path.dirname(os.path.abspath(__file__))
pos = os.path.join(here, "..", "data_assembly", "arxiv_tables", "kurvs_positions", "kurvs_positions.csv")
rows = {r["kurvs_id"]: r for r in csv.DictReader(open(pos))}
print(f"CFG142 requirement fluxes (T_d = {TD:.0f} K, nu_obs = {NUOBS / 1e9:.1f} GHz; Gamma_0 = {gam(NU850, 0):.4f}, Scoville quotes 0.71)"
      + ("   [MUTATE: T_d x 2]" if TD != 25.0 else ""))
coef = 1.19e27 * 1e-3 * 1e6 / 6.7e19
ca = abs(coef / 1.78e10 - 1) < 0.01
cb = abs(gam(NU850, 0) / 0.71 - 1) < 0.02
print(f"  C-a: coefficient 1.19e27 x 1e-3 Jy x (1e3 Mpc)^2 / 6.7e19 = {coef:.4e} Msun per mJy at 1 Gpc, against 1.78e10 (1%): {'PASS' if ca else 'FAIL'}")
print(f"  C-b: Gamma_0 = {gam(NU850, 0):.4f} against the paper's 0.71 (2%): {'PASS' if cb else 'FAIL'}")
print(f"  {'KURVS':>5s} {'z':>6s} {'logM*':>6s} {'d_L/Gpc':>8s}  {'S(mu_dust=2) mJy':>17s} {'S(mu_dust=4) mJy':>17s} {'S_req,gen mJy':>14s}  GOODS-ALMA placement")
out = {}
for kid in ("3", "7", "8", "9", "11", "13", "15", "16", "17", "21"):
    r = rows[kid]
    z, lm = float(r["z_halpha"]), float(r["logMstar"])
    s2, s4 = s_mjy(2 * 10 ** lm, z), s_mjy(4 * 10 ** lm, z)
    out[kid] = (s2, s4)
    print(f"  {kid:>5s} {z:6.3f} {lm:6.2f} {d_l_gpc(z):8.3f}  {s2:17.3f} {s4:17.3f} {s2 * 10 ** -0.2:14.3f}  {r['GOODSALMA_status']}")
raise SystemExit(0 if (ca and cb) else 1)
