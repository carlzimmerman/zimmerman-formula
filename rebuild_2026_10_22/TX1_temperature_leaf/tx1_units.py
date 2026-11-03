#!/usr/bin/env python3
"""TX1 units and sources. Prints conversions per cluster; writes SOURCES_USED.txt. python3 -I tx1_units.py. kappa = 1/2 FITTED; not theory closed."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tx1_lib import *
T = tload(); out = []; P = out.append; XD = os.path.join(REPO, "real_research", "data", "xcop")
P("cluster z R500_kpc R500_hydro T500 T500_formula Tew med(KT/(T_X T500)) min max kpc_per_arcmin_implied Hubble_ratio max_T min_T")
for n in NAMES12:
    q = T[n]
    with fits.open(os.path.join(XD, n, f"{n}_hydro_mass.fits")) as h: r5h = float(h[1].header["R500"])
    E_ = math.sqrt(.3 * (1 + q["z"]) ** 3 + .7); Tf = 8.85 * (q["M500"] / 10) ** (2 / 3) * E_ ** (2 / 3)
    o = np.argsort(q["arcmin"]); ka = np.median(q["x"] * q["R500"] / q["arcmin"][o]); kh = (299792.458 * q["z"] / 70 / (1 + q["z"]) ** 2) * 1e3 * math.pi / 180 / 60
    P(f"{n} {q['z']:.4f} {q['R500']:.0f} {r5h:.0f} {q['T500']:.3f} {Tf:.3f} {q['Tew']:.3f} {np.median(q['fac']):.4f} {q['fac'].min():.3f} {q['fac'].max():.3f} {ka:.1f} {ka/kh:.3f} {q['kT'].max():.2f} {q['kT'].min():.2f}")
g, tau = tau_nodes(); P("tau nodes x " + " ".join(f"{a:.3f}" for a in g[::6])); P("tau " + " ".join(f"{a:.3f}" for a in tau[::6])); P(f"s_c = {s_c():.4f} dex; 5 keV sqrt(s2) = {math.sqrt(5*KT2S)/1e3:.1f} km/s; c/b: M* files on {[n for n in NAMES12 if os.path.exists(os.path.join(XD, n, f'{n}_mstar.fits'))]}")
print("\n".join(out)); open(os.path.join(LANE, "tx1_units.out"), "w").write("\n".join(out) + "\n")
with open(os.path.join(LANE, "SOURCES_USED.txt"), "w") as f:
    f.write("X-COP release allfiles.tar.gz sha256 0edf5038b419b70d070b73b22f4801e27f318b0854db61eec52142c27c140d94, per the data directory's SOURCES.txt. Directory untracked. wb/ not used. Files used:\n")
    for n in NAMES12:
        for b in (f"{n}_temperature.fits", f"spectral_results_{n}.fits"): f.write(f"{sha(os.path.join(DATA, n, b))}  {n}/{b}\n")
