#!/usr/bin/env python3
"""Data note (no lane number): can X-ray data test B's hot-gas escape from the KiDS early/late split?

CFG61's escape: early-type lenses carry extra baryons Delta_f x M* (0.25 acceptable, ~1 best fit) at the M* node, i.e. enclosed within
the smallest 1-halo lensing radius (~50 kpc for early types).  This script prints the numbers quoted in KIDS_HOT_GAS_ESCAPE_NOTE_2026-09-29.md:
  (1) the eROSITA eRASS:4 hot-CGM luminosities (Zhang et al. 2025, A&A 693, A197, arXiv:2411.19945, Table 3; read from the arXiv HTML v1
      on 2026-09-29, no file downloaded) and their internal consistency (L_mask - L_AGN+XRB+SAT = L_CGM);
  (2) an ESTIMATE, not a result: the 0.5-2 keV bremsstrahlung luminosity of the escape's extra gas in its X-ray-faintest geometry
      (uniform density inside radius R), metal lines omitted (Gaunt factor 1; lines only add emission), with its bremsstrahlung cooling time;
  (3) measured context: the hot-gas fraction M_gas(<20 kpc) / M* of CFG57's seven X-ray-covered SLUGGS early types (CFG57's committed
      output, Lakhchaura+2018 / Fukazawa+2006 profiles, SLUGGS distances and stellar masses).
Run: python3 campaign_fresh_gravity/closure_map/kids_hot_gas_escape_note.py
"""
import os, re, math

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

# (1) eROSITA eRASS:4, Table 3 (0.5-2 keV, within R500c, erg/s): (L_mask, err, L_CGM, err, L_AGN+XRB+SAT, err)
T3 = {("10.5-11.0", "SF"): (1.7e40, 0.4e40, 8.0e39, 5.0e39, 9.2e39, 2.9e39),
      ("10.5-11.0", "QU"): (1.6e40, 0.4e40, 1.1e40, 0.4e40, 4.4e39, 1.0e39),
      ("11.0-11.25", "SF"): (5.0e40, 1.0e40, 2.3e40, 1.5e40, 2.6e40, 1.1e40),
      ("11.0-11.25", "QU"): (7.3e40, 0.8e40, 6.2e40, 0.8e40, 1.1e40, 0.3e40)}
print(__doc__.split("Run:")[0].strip())
print("\n(1) eROSITA eRASS:4 hot CGM, 0.5-2 keV within R500c (Zhang+2025 Table 3)")
for (b, s), (lm, _, lc, ec, la, _) in T3.items():
    print(f"    log M* {b:10s} {s}: L_CGM = {lc:.2e} +- {ec:.1e}   consistency L_mask - L_AGN+XRB+SAT = {lm - la:.2e} ({(lm - la) / lc - 1:+.0%})")
for b in ("10.5-11.0", "11.0-11.25"):
    q, s = T3[(b, "QU")], T3[(b, "SF")]
    d, e = q[2] - s[2], math.hypot(q[3], s[3])
    print(f"    log M* {b}: QU - SF = {d:+.2e} +- {e:.2e} erg/s ({d / e:+.1f} sigma)")
QU2 = T3[("10.5-11.0", "QU")][2] + 2 * T3[("10.5-11.0", "QU")][3]
print(f"    QU 2-sigma upper bound, log M* 10.5-11.0: {QU2:.2e} erg/s")

# (2) the ESTIMATE: bremsstrahlung only, uniform sphere (the X-ray-faintest geometry for a fixed mass inside R)
MP, KPC, MSUN, KEV = 1.6726e-24, 3.0857e21, 1.989e33, 1.1605e7          # g, cm, g, K per keV
X_HE = 0.25 / 4 / 0.75                                                  # n_He / n_H for Y = 0.25
NE, SZ2, RHO = 1 + 2 * X_HE, 1 + 4 * X_HE, 1 + 4 * X_HE                 # n_e / n_H, sum Z^2 n_i / n_H, rho / (m_p n_H)
LMS = 10.81                                                             # median log M_gal of the KiDS early class (CFG110 C2)


def lx_ff(mgas, r_kpc, t_kev, e1=0.5, e2=2.0, gaunt=1.0):
    v = 4 / 3 * math.pi * (r_kpc * KPC) ** 3
    nh = mgas * MSUN / (RHO * MP * v)
    t = t_kev * KEV
    band = math.exp(-e1 / t_kev) - math.exp(-e2 / t_kev)
    lum = 1.4175e-27 * math.sqrt(t) * gaunt * SZ2 * NE * nh ** 2 * band * v
    bol = 1.4175e-27 * math.sqrt(t) * gaunt * SZ2 * NE * nh ** 2
    tcool = 1.5 * (NE + 1 + X_HE) * nh * 1.380649e-16 * t / bol / 3.156e16  # Gyr
    return lum, nh * NE, tcool


print(f"\n(2) ESTIMATE (not a result): bremsstrahlung-only 0.5-2 keV luminosity of Delta_f x M* (log M* {LMS}) spread uniformly inside R")
print("    (metal lines omitted: a lower bound at fixed T; uniform density is the X-ray-faintest way to put the mass inside R)")
for f in (0.25, 1.0):
    for r in (50.0, 100.0, 180.0):
        row = []
        for t in (0.1, 0.15, 0.2, 0.3):
            lum, ne, tc = lx_ff(f * 10 ** LMS, r, t)
            row.append(f"T {t:.2f}: {lum:.1e} ({lum / QU2:.2g}x)")
        _, ne, tc = lx_ff(f * 10 ** LMS, r, 0.1)
        print(f"    Delta_f {f:.2f}, R {r:3.0f} kpc (n_e {ne:.1e} cm^-3, t_cool,ff at 0.1 keV {tc:.1f} Gyr): " + "; ".join(row))
print("    (x = the ratio to the QU 2-sigma upper bound; above 1 would be excluded if the emission were pure bremsstrahlung)")

# (3) measured context: CFG57's M_gas(<20 kpc) and SLUGGS stellar masses
out = open(os.path.join(REPO, "campaign_fresh_gravity", "CFG57_sluggs_hot_gas.out")).read()
line = [l for l in out.splitlines() if "gas per covered galaxy" in l][0]
mg = {m.group(1): float(m.group(2)) for m in re.finditer(r"(NGC\d+) src\d M_gas\(<r12\) [0-9.e+]+, \(<20 kpc\) ([0-9.e+]+)", line)}
lm = {}
for l in open(os.path.join(REPO, "real_research", "data", "sluggs_forbes2017_galaxies.tsv")):
    p = l.rstrip("\n").split("\t")
    if len(p) > 4 and p[1].strip().isdigit():
        lm["NGC" + p[1].strip()] = float(p[4])
print("\n(3) measured context: hot-gas fraction within 20 kpc of CFG57's X-ray-covered SLUGGS early types (M_gas from CFG57's committed output)")
fr = []
for n, m in sorted(mg.items()):
    fr.append(m / 10 ** lm[n])
    print(f"    {n}: log M* {lm[n]:.2f}, M_gas(<20 kpc) {m:.2e} Msun, M_gas / M* = {m / 10 ** lm[n]:.4f}")
print(f"    range {min(fr):.4f} - {max(fr):.4f} (N = {len(fr)})")

# (2b) ESTIMATE: the temperature of hydrostatic gas in B's deep-regime potential (flat v_c = (G M a0)^(1/4), a0 = 1.2e-10 m/s^2 for the
#      estimate), isothermal with density slope s: kT = mu m_p v_c^2 / s, mu = 0.6, s = 1.5 - 2
vc = (6.674e-11 * 10 ** LMS * 1.989e30 * 1.2e-10) ** 0.25
kts = [0.6 * 1.6726e-27 * vc ** 2 / s / 1.602e-16 for s in (2.0, 1.5)]
print(f"\n(2b) ESTIMATE: B's flat v_c for log M* {LMS}: {vc / 1e3:.0f} km/s; hydrostatic isothermal kT = {kts[0]:.3f} (slope 2) to {kts[1]:.3f} keV (slope 1.5)")
