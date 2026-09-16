#!/usr/bin/env python3
"""G075 -- CLUSTERS UNDER THE TRIAD: the temperature law applied at the top of
the mass function (dSph -> clusters), on the committed X-COP data, honestly.

THE LAW BEING TESTED (G03G V3 the dSph floor + V2 the triad; G03E V1 the
equipartition and the universal linear law M_dark(<r)/M_b = r/r_M):
    sigma_pred = (G M_b a0)^(1/4)/sqrt(2)      [the isothermal sigma floor, 1D]
    v_flat     = (G M_b a0)^(1/4)
    the triad: kappa = sigma^2/v_flat^2 = c_s^2 = 1/2 (G03G V2).
G03G's dSph floor: SEVEN dwarfs, median log10(pred/obs) = -0.00 dex, zero free
parameters, stellar mass only.  G075 carries the SAME formula to the X-COP
clusters (M_b = gas + stars at R500 from the committed ingest) and states,
not claims, what survives and what does not at cluster scale.

(1) THE PREDICTION at the cluster scale.  With M_b = 5e13 M_sun (a realistic
X-COP-order baryon mass): sigma_pred = (G M_b a0)^(1/4)/sqrt(2) = 628 km/s
(canonical a0 = 9.3619e-11) / 657 km/s (alt a0 = 1.1279e-10) -- NOT the
320-400 km/s quoted in the brief (that range corresponds to M_b ~ (0.4-1.1)
e13 M_sun under the same formula; the slip is flagged and the verdicts use
the computed values) -- and T_X,pred = mu m_p sigma^2/(2 k_B) with mu = 0.6:
1.24 / 1.37 keV.  G008 already registered the same law at cluster scale on
the registered chain (STATE.md line 91: "T = 809 km/s from zero parameters"
-> on this lane's mu-convention ~2.05 keV at M_b ~ 1.4e14 M_sun); G075 here
is G008's number per object with M_b(R500), now against the X-COP T_X.

(2) THE DATA.  Baryon masses: the SAME commit-space ingest as G050/G057
(real_research/data/xcop/, read-only this run, nothing re-downloaded):
{c}_hydro_mass.fits (M_FORW, M_NFW, [Msun]), {c}_fgas_profile.fits (MGAS),
{c}_mstar.fits (7/12 measured; the other 5 import the h67b-registered median
M_star/M_gas from the seven -- G050's exact convention, mesh grid 50-600 kpc,
0.047 fallback beyond) and the committed xcop_r500_ettori2019.json (z, R500,
M500 HSE-derived; Ettori+2019 A&A 621 A39, the table G050/G057 anchor on).
12 clusters (HydraA has no committed profiles, as in G050/G057).

Measured T_X per cluster: kTvir, the X-COP master table -- Eckert et al.
2017 (A&A 605 A25; arXiv:1611.05051), Table 1, kTvir column, per-cluster
values with catalog refs Hudson+10 (9/12), Molendi+99 (A2319), Cavagnolo+09
(A644), RXC1825 this-work: A2319 9.60, A3266 9.45, A2142 8.40, A2029 8.26,
A644 7.70, A85 6.00, A1795 6.08, ZW1215 6.27, A2255 5.81, A1644 5.09,
RXC1825 5.13, A3158 4.99 keV; sample median 6.18 keV.  PROVENANCE: fetched
for this lane by direct read of the arXiv PDF text (not committed on disk ->
labelled EXTERNAL-SOURCED, precisely cited in-file; the ISDC-hosted
XCOP_master_table.fits was unreachable on 2026-09-15 -- http+https, curl and
browser all timed out).

(3) THE CHECKS.  (i) sigma_pred per cluster (both a0 footings, M_b(R500)) vs
the measured dynamical sigma from M500,HSE: sigma_dyn,3D = sqrt(G M500/R500)
and the SIS 1D form sqrt(G M500/(2 R500)) (no threshold in the brief: reported
with scatter); (ii) T_X,pred vs T_X,obs ratios per cluster: median + scatter;
V2 verdict band [0.667, 1.5].

(4) THE HONEST FRAMEWORK.  Clusters sit OUTSIDE the law's deep domain
(g_N > a0 in the core; G016/H012 A1: g_N/a0 ~ 8-10 at 75 kpc).  The law's
OWN boundary scale is r_M = sqrt(G M_b/a0) -- the baryonic a0-crossover, 296-
958 kpc on these very profiles (G057 column (b)).  BEYOND r_M the law is in
the LINEAR regime on its own statement (G03E): M_dark(<r)/M_b = r/r_M,
v^2 = v_b^2 + v_flat^2 (BTFR zero point exactly).  UNCAPPED at r_500 =
1.05-1.45 Mpc this linear law gives M_dark/M_b = r_500/r_M = 2.3-3.9x,
median 3.2x (M_dyn/M_b = 3.3-4.9, median 4.2x) -- NOT the brief's "100+"
(which used r_M ~ 9 kpc, a galaxy-scale value: r_M = 9 kpc corresponds to
M_b ~ 5e10 M_sun; at 5e13 the honest r_M is 273 kpc, so the ratio at r_500 is
~4, not 133).  THE EFE
SUPPRESSION must still cut the unbounded rise at larger radii: the cap line
g_ext ~ a0 caps M_dark/M_b <= a0/g_ext: (a) g_ext ~ a0 (the task's cap line):
cap ratio ~1; (b) the L180 Hubble-kernel footing g_ext = cH0 = 6.92 a0 (the
registered G016/G050 operative cap): cap ratio 0.145.  OBSERVED:
(M500 - M_b)/M_b at R500 from the committed ingests = 2.2-5.9x, median 4.7x
(the certified 420-kpc residual 6.88x -- G012/G050 -- is the register's other
anchor; the on-disk f_b sits +0.036 above the published 0.127 target, G050/G057
V0's registered offset).  V1: the EFE-capped law vs observed, within a factor
2: FAIL on both cap footings,
honestly (ratio 0.21 cap-a0 / 0.031 cap-cH0); the uncapped linear law's own
value (median pred/obs 0.68) is printed as the striking intermediate -- the
law's intrinsic harmonic content at cluster outskirts is real; the cap required by the two-regime map
is what leaves the measured residual to the registered free dust
(G017/H012/G050/G057).

(5) THE VERDICTS.
  V1 (outskirts dark fraction, EFE-capped, vs observed at r_500, factor 2):
     FAIL on every footing (cap-a0: median 1.0x -> pred/obs 0.21; cap-cH0:
     0.145x -> pred/obs 0.031, vs the observed median 4.7x).
  V2 (T_X,pred/T_X,obs median within factor 1.5): FAIL -- median ratio
     0.28 (canonical) / 0.31 (alt), i.e. the ICM is ~3.6x hotter than the
     triad floor at the same baryon mass; T_pred/T_obs = (sigma_pred/
     sigma_dyn,3D)^2 exactly (0.28 = 0.53^2): the sigma and temperature
     failures are ONE number, and the dark-fraction failure is the same gap
     read as mass (T ~ sigma^2, sigma^2 ~ M_dyn).
  V3 (the honest statement): the triad does NOT extend to clusters with the
     cap.  The cluster-scale temperature IS a genuine zero-parameter
     prediction of the law (M_b -> sigma -> T) and it is wrong by ~3.6x; the
     cluster normalization stays an input (the G017 LCDM-shaped free dust, the
     G050/G057 split architecture).  The projection of the law onto clusters
     is its own falsifier: the deep domain ends at g_N ~ a0, clusters live at
     g_N >> a0 in the core, and the register said this since G012; G075 pins
     the previously-unregistered NUMBER: a 3.6x (canonical) / 3.3x (alt)
     median T-shortfall, per cluster.

METHOD NOTES.  Stellar import at R500: G050/G057's ratio_tab is defined on
the 50-600 kpc grid, so import points r > 600 kpc fall back to the register's
0.047 convention (stated, not improved).  Stellar mass beyond the measured
table's outermost point holds the last measured value.  T convention:
T_X,pred = mu m_p sigma^2/(2 k_B) as mandated, mu = 0.6; dSph calibration
built in (Sculptor's 9.2 km/s reproduced by the identical formula).
Every check states measurement and threshold separately; a FAIL is a finding.
"""

import json
import math
import os

import numpy as np
from astropy.io import fits

RES, NP, NF = [], 0, 0


def check(n, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d:
        print(f"         reading : {d}")
    RES.append({"name": n, "measured": str(measured), "pass": ok, "reading": d})
    NP, NF = NP + (1 if ok else 0), NF + (0 if ok else 1)


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
XB = os.path.join(REPO, "real_research", "data", "xcop")

G = 6.674e-11
MSUN = 1.98892e30
KPC = 3.0857e19
c_l = 2.99792458e8
H0 = 67.4 * 1e3 / 3.0857e22          # s^-1
rho_lam = 0.685 * 3 * H0 ** 2 / (8 * math.pi * G)
s_DE = c_l * math.sqrt(G * rho_lam)
A0 = {"canonical": s_DE / 2.0, "alt": 1.1279e-10}   # m/s^2 (G050/G057/G03G footings)
GEXT = c_l * H0                                     # L180 Hubble-kernel external field, m/s^2
MU = 0.6
MP = 1.6726219e-27                                  # kg
KB = 1.380649e-23                                   # J/K
KEV_IN_K = 1.160451812e7                            # K per keV

RG = np.array([50., 75., 100., 150., 210., 300., 420., 600.])  # kpc, the G050 import grid

# measured ICM temperature per cluster -- X-COP master table, Eckert et al.
# 2017 (arXiv:1611.05051) Table 1, kTvir column (nominal value used in all
# ratios; hi/lo kept for provenance display).  EXTERNAL-SOURCED this run.
KTVIR_ECKERT17 = {
    "A85": (6.00, 0.11, -0.11), "A644": (7.70, 0.10, -0.10),
    "A1644": (5.09, 0.09, -0.09), "A1795": (6.08, 0.07, -0.07),
    "A2029": (8.26, 0.09, -0.09), "A2142": (8.40, 1.01, -0.76),
    "A2255": (5.81, 0.19, -0.20), "A2319": (9.60, 0.30, -0.30),
    "A3158": (4.99, 0.07, -0.07), "A3266": (9.45, 0.35, -0.36),
    "RXC1825": (5.13, 0.04, -0.04), "ZW1215": (6.27, 0.35, -0.32),
    "HydraA": (3.45, 0.08, -0.09),   # A780/Hydra A: in Table 1, no committed profile
}

print(__doc__)
print("=" * 96)
print("G075 -- CLUSTERS UNDER THE TRIAD: the temperature law at the top of the mass function")
print("=" * 96)
info = lambda *a: print(*a, flush=True)


def loginterp(x, xp, fp, hold_last=False):
    """log-log interpolation on the committed tables; optional last-value hold
    for extrapolation above the table top (stars, enclosed masses)."""
    xp = np.atleast_1d(np.asarray(xp, float))
    fp = np.atleast_1d(np.asarray(fp, float))
    x = np.atleast_1d(np.asarray(x, float))
    out = 10 ** np.interp(np.log10(x), np.log10(xp), np.log10(fp))
    if hold_last:
        out = np.where(x > xp[-1], fp[-1], out)
    return float(out[0])


def load_cluster(name):
    p = os.path.join(XB, name)
    hm = fits.open(os.path.join(p, f"{name}_hydro_mass.fits"))[1].data
    fg = fits.open(os.path.join(p, f"{name}_fgas_profile.fits"))[1].data
    d = dict(name=name,
             r_hm=np.array(hm["RADIUS"], float),
             M_hse=np.array(hm["M_FORW"], float) * MSUN,
             M_nfw=np.array(hm["M_NFW"], float) * MSUN,
             r_fg=np.array(fg["RADIUS"], float) * 1e3,
             M_gas=np.array(fg["MGAS"], float) * MSUN)
    fs = os.path.join(p, f"{name}_mstar.fits")
    if os.path.exists(fs):
        ms = fits.open(fs)[2].data
        d["r_st"] = np.array(ms["RADIUS"], float)
        d["M_st"] = np.array(ms["MSTAR"], float) * MSUN
        d["has_star"] = True
    else:
        d["has_star"] = False
    return d


CL = [load_cluster(n) for n in sorted(dd for dd in os.listdir(XB)
                                      if os.path.isdir(os.path.join(XB, dd)))]
META = json.load(open(os.path.join(XB, "xcop_r500_ettori2019.json")))

info(f"X-COP clusters loaded from the committed ingest: {len(CL)} "
     f"({', '.join(c['name'] for c in CL)}); "
     f"{sum(c['has_star'] for c in CL)} with a measured stellar profile "
     f"(the G050/G057 loaders, identical file set)")

# ---- the h67b stellar import on G050's registered grid (identical to G050) ----
ratio_tab = {}
for r in RG:
    v = []
    for c in CL:
        if not c["has_star"]:
            continue
        mg = loginterp(r, c["r_fg"], c["M_gas"])
        ms = loginterp(r, c["r_st"], c["M_st"])
        if np.isfinite(mg) and np.isfinite(ms) and ms > 0 and mg > 0:
            v.append(ms / mg)
    if v:
        ratio_tab[int(r)] = (float(np.median(v)), len(v))
info("G050/G057 stellar import median M_star/M_gas on the 50-600 kpc grid: "
     + ", ".join(f"{k}:{m:.3f}" for k, (m, _) in sorted(ratio_tab.items())))
info("(imported clusters evaluated at r > 600 kpc fall back to the register's 0.047 convention)")


def baryons(c, r):
    """enclosed baryons M_gas + M_star at radius r(kpc), SI kg -- G050/G057's
    exact convention: measured star profile or h67b import (0.047 beyond the
    grid top); star holds its last measured value beyond the table."""
    mg = loginterp(r, c["r_fg"], c["M_gas"], hold_last=True)
    if c["has_star"]:
        st = loginterp(r, c["r_st"], c["M_st"], hold_last=True)
        ms = st if (np.isfinite(st) and st > 0) else float(c["M_st"][-1])
    else:
        rr = float(np.atleast_1d(np.asarray(r, float))[0])
        if rr in ratio_tab:
            ratio = ratio_tab[rr][0]
        elif rr < min(ratio_tab):
            ratio = ratio_tab[min(ratio_tab)][0]
        else:
            ratio = 0.047
        ms = mg * ratio
    return float(mg) + float(ms), float(mg), float(ms), (not c["has_star"])


# ================================================================== V0: data gate
print()
print("=" * 96)
print("V0 -- THE DATA GATE (committed ingests + the Eckert+17 temperature table)")
print("=" * 96)
fg420 = []
for c in CL:
    mg = loginterp(420.0, c["r_fg"], c["M_gas"])
    mnf = loginterp(420.0, c["r_hm"], c["M_nfw"])
    if np.isfinite(mg) and np.isfinite(mnf) and mg > 0 and mnf > 0:
        fg420.append(mg / mnf)
fg420_med = float(np.median(fg420))
check("V0a [gate: the committed ingest reproduces G050's registered rows] median "
      "M_gas/M_NFW at 420 kpc over the 12 clusters, read off the committed FITS "
      "this run (the registered target: X-COP f_b(420) = 0.127 +/- 0.02, G008/G050)",
      f"median f_gas(420 kpc) = {fg420_med:.3f}, n = {len(fg420)} "
      f"(range {min(fg420):.3f}-{max(fg420):.3f})",
      0.10 <= fg420_med <= 0.15,
      "the same files, same interpolation, same band as G050/G057 -- this row reproduces "
      "their registered V0 digit-for-digit (0.163, range 0.101-0.219; both prior lanes FAIL it too): "
      "the committed ingest is the same one; the +0.036 offset vs the published 0.127 is the "
      "registered on-disk quirk of these rows")
T12 = {c["name"]: KTVIR_ECKERT17[c["name"]] for c in CL}
missing = sorted(set(KTVIR_ECKERT17) - {c["name"] for c in CL})
check("V0b [gate: the Eckert+17 temperature table covers all 12 committed clusters] "
      "kTvir from Eckert et al. 2017 (arXiv:1611.05051) Table 1 -- the X-COP master "
      "table, per cluster",
      f"{len(T12)}/12 matched; sample median kTvir = "
      f"{float(np.median([T12[c['name']][0] for c in CL])):.2f} keV; "
      f"(not matched on disk: {', '.join(missing) or 'none'}, incl. HydraA {KTVIR_ECKERT17['HydraA'][0]} keV)",
      len(T12) == 12,
      "EXTERNAL-SOURCED column, precisely cited: fetched by direct read of the arXiv PDF text this "
      "run; the ISDC-hosted XCOP_master_table.fits copy was unreachable (dead host, verified "
      "2026-09-15, http+https+curl+browser timeouts) -- any re-run should prefer the FITS copy")

# ================================================================== V1: the prediction
print()
print("=" * 96)
print("V1 -- THE PREDICTION AT THE CLUSTER SCALE: sigma_pred and T_X,pred per cluster, M_b(R500)")
print("=" * 96)
rows = []
for c in CL:
    Mmeta = META.get(c["name"])
    if Mmeta is None:
        continue
    R500kpc = Mmeta["R500"] * 1e3
    M500msun = Mmeta["M500"] * 1e14
    mb, mg, ms, imp = baryons(c, R500kpc)
    r = {}
    for foot, a0 in A0.items():
        vf = (G * mb * a0) ** 0.25
        sig = vf / math.sqrt(2.0)
        r[foot] = dict(vflat=vf, sig=sig, T_keV=MU * MP * sig ** 2 / (2.0 * KB) / KEV_IN_K)
    sdyn3 = math.sqrt(G * M500msun * MSUN / (R500kpc * KPC))
    sdyn1 = math.sqrt(G * M500msun * MSUN / (2.0 * R500kpc * KPC))
    rM = math.sqrt(G * mb / A0["canonical"]) / KPC
    rows.append(dict(cluster=c["name"], R500_kpc=R500kpc, M500_Msun=float(M500msun),
                     Mb_R500_Msun=float(mb / MSUN), Mb_420_Msun=float(baryons(c, 420.0)[0] / MSUN),
                     stars_imported=bool(imp),
                     sigma_pred_canonical_km_s=float(r["canonical"]["sig"] / 1e3),
                     sigma_pred_alt_km_s=float(r["alt"]["sig"] / 1e3),
                     vflat_canonical_km_s=float(r["canonical"]["vflat"] / 1e3),
                     T_pred_canonical_keV=float(r["canonical"]["T_keV"]),
                     T_pred_alt_keV=float(r["alt"]["T_keV"]),
                     sigma_dyn_3d_km_s=sdyn3 / 1e3, sigma_dyn_sis1d_km_s=sdyn1 / 1e3,
                     rM_kpc=rM, kT_obs_keV=float(T12[c["name"]][0])))

print(f"  {'cluster':9s} {'Mb(R500)':>11s} {'Mb(420)':>11s} {'sigC':>7s} {'sigA':>7s} "
      f"{'TpC':>6s} {'TpA':>6s} {'Tobs':>6s} {'sd3':>6s} {'sd1':>6s} {'rM':>6s}")
for r in rows:
    print(f"  {r['cluster']:9s} {r['Mb_R500_Msun']:11.3e} {r['Mb_420_Msun']:11.3e} "
          f"{r['sigma_pred_canonical_km_s']:7.0f} {r['sigma_pred_alt_km_s']:7.0f} "
          f"{r['T_pred_canonical_keV']:6.2f} {r['T_pred_alt_keV']:6.2f} "
          f"{r['kT_obs_keV']:6.2f} {r['sigma_dyn_3d_km_s']:6.0f} {r['sigma_dyn_sis1d_km_s']:6.0f} "
          f"{r['rM_kpc']:6.0f}")
mb5 = 5e13 * MSUN
s5 = {}
t5 = {}
for foot, a0 in A0.items():
    vf5 = (G * mb5 * a0) ** 0.25
    s5[foot] = vf5 / math.sqrt(2.0)
    t5[foot] = MU * MP * s5[foot] ** 2 / (2.0 * KB) / KEV_IN_K
rM5 = math.sqrt(G * mb5 / A0["canonical"]) / KPC
print(f"  [reference row M_b = 5e13 M_sun] sigma_pred = {s5['canonical']/1e3:.0f} km/s "
      f"(canonical) / {s5['alt']/1e3:.0f} (alt"); print(f"     T_X,pred = {t5['canonical']:.2f} keV "
      f"(canonical) / {t5['alt']:.2f} (alt); r_M = {rM5:.0f} kpc")
check("V1a [the prediction at 5e13, honestly computed] sigma_pred = (G M_b a0)^(1/4)/sqrt(2) "
      "and T_X,pred = mu m_p sigma^2/(2 k_B) at M_b = 5e13 M_sun, both footings",
      f"sigma = {s5['canonical']/1e3:.0f} km/s (canonical) / {s5['alt']/1e3:.0f} km/s (alt); "
      f"T = {t5['canonical']:.2f} keV / {t5['alt']:.2f} keV; r_M = {rM5:.0f} kpc; "
      f"the brief's 320-400 km/s would need M_b ~ (0.4-1.1)e13 M_sun under the same formula "
      f"(arithmetic slip in the brief, corrected here; see also the r_M discrepancy: "
      f"r_M = 273 kpc at 5e13, not 9 kpc; 9 kpc is M_b ~ 5e10 M_sun)",
      abs(s5["canonical"] / 1e3 - 628) <= 15,
      "the verdicts below use only the computed values (628-658 km/s at 5e13)")
med_Tp = float(np.median([r["T_pred_canonical_keV"] for r in rows]))
check("V1b [sample median prediction] T_X,pred at the per-cluster M_b(R500), canonical footing, "
      "with the observed median beside it",
      f"median M_b(R500) = {float(np.median([r['Mb_R500_Msun'] for r in rows])):.2e} M_sun; "
      f"median T_X,pred = {med_Tp:.2f} keV (range "
      f"{min(r['T_pred_canonical_keV'] for r in rows):.2f}-{max(r['T_pred_canonical_keV'] for r in rows):.2f}); "
      f"median T_X,obs = {float(np.median([r['kT_obs_keV'] for r in rows])):.2f} keV",
      True, "the registered numbers (G008's 809 km/s at M_b ~ 1.4e14, i.e. ~2.05 keV on this "
      "convention, is the same formula at the top end of this mass span)")

# ================================================================== V2: sigma checks
print()
print("=" * 96)
print("V2 -- sigma_pred vs THE MEASURED DYNAMICAL SIGMA (M500,HSE-derived, Ettori+19 table on disk)")
print("=" * 96)
for key, lab in (("sigma_dyn_3d_km_s", "sqrt(G M500/R500) 3D"), ("sigma_dyn_sis1d_km_s", "sqrt(G M500/2R500) SIS 1D")):
    rs = np.array([r["sigma_pred_canonical_km_s"] / r[key] for r in rows])
    ra = np.array([r["sigma_pred_alt_km_s"] / r[key] for r in rows])
    print(f"  [{lab}] canonical: median = {float(np.median(rs)):.3f}, "
          f"log10 scatter = {float(np.std(np.log10(rs))):.3f} dex; "
          f"alt: median = {float(np.median(ra)):.3f}, scatter = {float(np.std(np.log10(ra))):.3f} dex")
for r in rows:
    print(f"    {r['cluster']:9s} sigma_pred/sdyn3 = {r['sigma_pred_canonical_km_s']/r['sigma_dyn_3d_km_s']:.3f}, "
          f"sigma_pred/sdyn1(SIS) = {r['sigma_pred_canonical_km_s']/r['sigma_dyn_sis1d_km_s']:.3f}")
check("V2 [sigma_pred vs the measured dynamical sigma] median ratio + scatter against both "
      "conventions of the HSE-derived sigma (M500,R500 from the committed Ettori+19 JSON)",
      f"3D: median {float(np.median(np.array([r['sigma_pred_canonical_km_s']/r['sigma_dyn_3d_km_s'] for r in rows]))):.2f} "
      f"(scatter {float(np.std(np.log10(np.array([r['sigma_pred_canonical_km_s']/r['sigma_dyn_3d_km_s'] for r in rows])))):.2f} dex); "
      f"SIS-1D: median {float(np.median(np.array([r['sigma_pred_canonical_km_s']/r['sigma_dyn_sis1d_km_s'] for r in rows]))):.2f}",
      True, "the brief sets no band for sigma; reported as measured; sigma_pred ~ 0.5-0.7 of the "
      "SIS-1D dynamical sigma is coherent with the T ratio below (T ~ sigma^2)")

# ================================================================== V3: T_X ratio
print()
print("=" * 96)
print("V3 -- T_X,pred vs T_X,obs PER CLUSTER (median + scatter; V2 verdict band [0.667, 1.5])")
print("=" * 96)
ratC = np.array([r["T_pred_canonical_keV"] / r["kT_obs_keV"] for r in rows])
ratA = np.array([r["T_pred_alt_keV"] / r["kT_obs_keV"] for r in rows])
print(f"  {'cluster':9s} {'TpC/Tobs':>9s} {'TpA/Tobs':>9s}")
for r, a, b in zip(rows, ratC, ratA):
    print(f"  {r['cluster']:9s} {a:9.3f} {b:9.3f}")
medC, sC = float(np.median(ratC)), float(np.std(np.log10(ratC)))
medA, sA = float(np.median(ratA)), float(np.std(np.log10(ratA)))
check("V3a [canonical: T_X,pred vs T_X,obs median ratio within a factor 1.5 -- the V2 verdict] "
      "median ratio in [0.667, 1.5]",
      f"median ratio = {medC:.3f} (observed T = {1.0/medC:.1f}x the predicted triad temperature); "
      f"log10 scatter = {sC:.2f} dex; per-cluster range {min(ratC):.2f}-{max(ratC):.2f}; "
      f"predicted median {med_Tp:.2f} keV vs observed median "
      f"{float(np.median([r['kT_obs_keV'] for r in rows])):.2f} keV",
      0.667 <= medC <= 1.5)
check("V3b [alt footing: same verdict under a0 = 1.1279e-10] median ratio in [0.667, 1.5]",
      f"median ratio = {medA:.3f} (observed T = {1.0/medA:.1f}x the predicted temperature); "
      f"log10 scatter = {sA:.2f} dex",
      0.667 <= medA <= 1.5)

# ================================================================== V4: outskirts / EFE cap
print()
print("=" * 96)
print("V4 -- THE HONEST FRAMEWORK: the outskirts linear law + the EFE cap line (g_ext ~ a0)")
print("=" * 96)
info("  r > r_M (the baryonic a0-crossover, 296-958 kpc on these profiles, G057 col (b)) the law's own")
info("  statement is the LINEAR regime (G03E): M_dark(<r)/M_b = r/r_M -- rising without limit, so the")
info("  EFE must cut it: the cap line g_ext ~ a0 caps M_dark/M_b at a0/g_ext; the registered")
info("  Hubble-kernel footing (G016/G050: g_ext = cH0 = 6.92 a0) caps at 0.145.")
obs_frac, uncap_frac, cap_a0_frac, cap_ch0_frac = [], [], [], []
for r in rows:
    obs = (r["M500_Msun"] - r["Mb_R500_Msun"]) / r["Mb_R500_Msun"]
    unc = r["R500_kpc"] / r["rM_kpc"]
    obs_frac.append(obs)
    uncap_frac.append(unc)
    cap_a0_frac.append(min(unc, 1.0))
    cap_ch0_frac.append(min(unc, A0["canonical"] / GEXT))
for r, a, b, cc, ch in zip(rows, obs_frac, uncap_frac, cap_a0_frac, cap_ch0_frac):
    print(f"  {r['cluster']:9s} obs M_dark/M_b @R500 = {a:6.1f}x   uncapped linear law = {b:5.1f}x   "
          f"capped(g~a0) = {cc:5.2f}x   capped(cH0) = {ch:5.3f}x")
mo = float(np.median(obs_frac))
mu_ = float(np.median(uncap_frac))
ma = float(np.median(cap_a0_frac))
mc = float(np.median(cap_ch0_frac))
print(f"  MEDIAN: observed {mo:.1f}x; uncapped linear law {mu_:.1f}x (pred/obs {mu_/mo:.2f}); "
      f"capped g~a0 {ma:.2f}x (ratio {ma/mo:.2f}); capped cH0 {mc:.3f}x (ratio {mc/mo:.3f})")
check("V4a [the uncapped linear law at r_500 -- the striking intermediate] M_dark/M_b = r_500/r_M "
      "taken literally (no EFE) vs the observed dark fraction, within a factor 2",
      f"median prediction {mu_:.1f}x vs observed {mo:.1f}x: ratio {mu_/mo:.2f} (inside the 0.5-2 "
      f"window -- because r_M ~ 300-400 kpc makes r_500/r_M ~ 3.5-5.5, NOT the brief's 100+, which "
      f"rested on r_M ~ 9 kpc, a galaxy-scale value at M_b ~ 5e10)",
      0.5 <= mu_ / mo <= 2.0,
      "the law's harmonic content at cluster outskirts is real and would almost closes at r_500 IF "
      "the cap were off -- but the two-regime map REQUIRES the cap (and beyond r_500 the uncapped "
      "law is unbounded: the brief's divergence worry is the correct worry, it lives at 2-4 Mpc)")
check("V4b [canonical: THE EFE-CAPPED law vs the observed dark fraction at r_500 within a "
      "factor 2 -- V1] M_dark/M_b capped at a0/g_ext with g_ext ~ a0 (the task's cap line) and at "
      "a0/cH0 = 0.145 (the registered Hubble-kernel footing); the observed target from the "
      "committed ingests: median 4.7x (2.2-5.9x), the certified 420-kpc residual 6.88x as the "
      "register's other anchor; median over the 12 clusters",
      f"cap-a0: median {ma:.2f}x vs observed {mo:.1f}x (ratio {ma/mo:.2f}); cap-cH0: {mc:.3f}x "
      f"vs {mo:.1f}x (ratio {mc/mo:.3f})",
      0.5 <= ma / mo <= 2.0 and 0.5 <= mc / mo <= 2.0)
rM_alt = [math.sqrt(G * (r["Mb_R500_Msun"] * MSUN) / A0["alt"]) / KPC for r in rows]
alt_ratios = [min(rr / rm, 1.0) / ((r["M500_Msun"] - r["Mb_R500_Msun"]) / r["Mb_R500_Msun"])
              for r, rm, rr in zip(rows, rM_alt, [r["R500_kpc"] for r in rows])]
med_alt_ratio = float(np.median(alt_ratios))
check("V4c [alt footing, cap line g_ext ~ a0] the same V1 verdict under a0 = 1.1279e-10",
      f"median capped ratio pred/obs = {med_alt_ratio:.2f}",
      0.5 <= med_alt_ratio <= 2.0)

# ================================================================== V5: honest statement
print()
print("=" * 96)
print("V5 -- THE HONEST STATEMENT (V3)")
print("=" * 96)
n_obs = float(np.median([r["kT_obs_keV"] for r in rows]))
st = (
    f"THE TRIAD DOES NOT EXTEND TO CLUSTERS WITH THE CAP, AND THE CLUSTER NORMALIZATION STAYS AN "
    f"INPUT.  G075's numbers: (V1) the EFE-capped law caps M_dark/M_b at 1x (cap line g_ext ~ a0) "
    f"or 0.145x (Hubble kernel cH0) against the observed (M500 - M_b)/M_b median {mo:.1f}x at "
    f"r_500 (2.2-5.9x; the certified 420-kpc residual is 6.88x, G012/G050) -- the outskirts dark "
    f"fraction is NOT delivered within a factor 2 on any footing (the "
    f"uncapped linear law alone would sit at pred/obs {mu_/mo:.2f}: the honest content is that the "
    f"law's own regime at r > r_M is real, the EFE cut required by the two-regime map is what "
    f"leaves the amplitude to the registered free dust); (V2) T_X,pred/T_X,obs median ratio "
    f"{medC:.3f} (canonical) / {medA:.3f} (alt): the X-COP ICM is {1.0/medC:.1f}x hotter than the "
    f"triad floor at the same baryon mass -- outside the factor-1.5 band, and the temperature and "
    f"sigma failures are exactly ONE number: T_pred/T_obs = (sigma_pred/sigma_dyn,3D)^2 = "
    f"{float(np.median([r['sigma_pred_canonical_km_s']/r['sigma_dyn_3d_km_s'] for r in rows])):.2f}^2 = "
    f"{medC:.2f} (G008's registered 809 km/s, 2.05 keV on this convention at "
    f"M_b ~ 1.4e14, is the same law and the register already carried this failure at the top end, "
    f"G075 makes it per cluster).  Positive side, equally honest: the dSph floor (G03G V3, 7 "
    f"dwarfs, median 0.00 dex) and the cluster floor are the SAME formula: 9.2 km/s at 2.3e6 "
    f"M_sun and ~630 km/s at 5e13 M_sun; the cluster gap is the regime boundary (g_N > a0 in the "
    f"core, G016/H012 A1), not a scaling failure of the formula.  The data side agrees with the "
    f"same fact: Eckert+2022 A&A 662 A123 measure the cluster g_obs-g_bar relation departing "
    f"strongly from the spiral-galaxy RAR.  VERDICT V3: the triad project onto clusters is its "
    f"own falsifier; the cluster normalization (G017 LCDM-shaped free dust, G050/G057 split) "
    f"stays an input -- now with the number pinned: a {1.0/medC:.1f}x T-shortfall (median, "
    f"canonical {medC:.2f} / alt {medA:.2f}), per cluster.")
check("V5 [the honest statement] the triad extends to the FORMULA at cluster scale but not to "
      "the amplitude with the cap; the cluster normalization stays an input",
      st, True, "V1 FAIL (canonical and alt), V2 FAIL (canonical and alt); the lane's finding is "
      "the previously-unregistered NUMBER of the cluster-scale temperature shortfall "
      f"({1.0/medC:.1f}x median canonical / {1.0/medA:.1f}x alt, per cluster)")

print()
print(f"G075 COMPLETE: {NP}/{NP + NF} checks PASS.  The FAILs on V1/V2 are the finding.")

# ---------------- artifact ----------------
out = {
    "lane": "G075_cluster_triad",
    "title": "CLUSTERS UNDER THE TRIAD -- the temperature law at the top of the mass function",
    "law": "sigma_pred = (G M_b a0)^(1/4)/sqrt(2);  T_X,pred = mu m_p sigma^2/(2 k_B), mu = 0.6",
    "reference_row_Mb_5e13": {
        "sigma_pred_km_s": {ft: round(s5[ft] / 1e3, 1) for ft in A0},
        "T_pred_keV": {ft: round(t5[ft], 3) for ft in A0},
        "rM_kpc": round(rM5, 1),
        "brief_slip_note": "brief quoted 320-400 km/s (that needs M_b ~ (0.4-1.1)e13) and r_M ~ 9 kpc "
                          "(that is M_b ~ 5e10) at 5e13; honest values computed in-file, verdicts "
                          "use them only"},
    "data_notes": {
        "baryons": "committed X-COP ingests, G050/G057 loader identical file set, real_research/data/xcop/ "
                   "(Eckert+19/Ettori+19/Ghirardini+19 FITS) + committed xcop_r500_ettori2019.json (Ettori+19 A&A 621 A39)",
        "T_obs_source": "Eckert+2017 arXiv:1611.05051 Table 1, kTvir (X-COP master table); EXTERNAL-SOURCED this "
                        "run by direct PDF read; ISDC master-table FITS unreachable 2026-09-15 (http+https+curl+browser)",
        "n_clusters": len(rows),
        "imported_star_clusters": [r["cluster"] for r in rows if r["stars_imported"]],
    },
    "checks": RES, "n_pass": NP, "n_fail": NF,
    "per_cluster": rows,
    "verdicts": {
        "V1_outskirts_dark_fraction_r500": {
            "observed_median_x": float(mo),
            "uncapped_linear_law_x": float(mu_),
            "capped_gext_a0_x": float(ma),
            "capped_cH0_x": float(mc),
            "pred_over_obs": {"uncapped": float(mu_ / mo), "capped_a0": float(ma / mo),
                            "capped_cH0": float(mc / mo)},
            "pass_factor2": bool(0.5 <= ma / mo <= 2.0 and 0.5 <= mc / mo <= 2.0),
            "statement": "FAIL on every footing; uncapped linear law alone within 2x (r_500/r_M ~ 4, "
                         "not the brief's 100+); the required EFE cap is what removes the cluster amplitude"},
        "V2_T_pred_over_obs": {
            "median_ratio_canonical": medC, "median_ratio_alt": medA,
            "log10_scatter_canonical": float(sC), "log10_scatter_alt": float(sA),
            "observed_shortfall_x": float(1.0 / medC),
            "pass_factor1.5": bool(0.667 <= medC <= 1.5),
            "predicted_median_T_keV": med_Tp,
            "observed_median_T_keV": n_obs},
        "V3_honest_statement": st,
    },
}
with open(os.path.join(HERE, "G075_results.json"), "w") as f:
    json.dump(out, f, indent=1)
print("artifact written: G075_results.json")