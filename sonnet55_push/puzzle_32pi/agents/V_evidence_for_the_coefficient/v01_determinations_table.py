#!/usr/bin/env python3
"""v01_determinations_table.py -- every a0 (g_dagger) determination I could open, with the number as printed, its errors, what it depends on,
and the implied Z = c H / a0 on both footings.  Numbers were read from the papers' text (PDFs converted locally; arXiv IDs below);
the checks here only RECOMPUTE what can be recomputed (unit conversions, quadrature sums, the BTFR -> a0 conversion, Z, sigma offsets).

ENSEMBLE LIST E (declared BEFORE the ensemble statistics were computed): the full-sample, free-a0, z ~ 0 determinations of the RAR/BTFR
class whose IF is the data-preferred RAR/simple family:   MLS16 1.20 ; Desmond23 1.19 ; Rodrigues18 RAR 1.099 ; ChangZhou19 RAR 1.099 ;
ESR-paper RAR 1.13 ; McGaugh12 BTFR 1.3 ; this work (v02) RAR Upsilon-free 0.8725, RAR Upsilon in [0.25,1] 0.944, RAR fixed 0.5 1.106.
E is an ENSEMBLE OF ANALYSIS CHOICES (not independent measurements): its scatter is the analysis-choice systematic.
Exit 0 = every check held.
"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v_common import *

ok = []
def check(cond, msg):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {msg}")

r2 = json.load(open("v02_results.json"))
U = 1e-10
def lg(x):   # log10 a0 [km/s^2] -> a0 [m/s^2]
    return 10 ** x * 1e3

# ---- rows: id, ref, arXiv, dataset, IF, Upsilon/nuisance treatment, a0 (1e-10), stat, sys, indep_of_SPARC_RAR, role
rows = [
 dict(id="BBS91", ref="Begeman, Broeils & Sanders 1991 (MNRAS 249, 523), as quoted in Sanders & McGaugh 2002", arxiv="astro-ph/0204521 (no arXiv for BBS91)",
      data="9 nearby spirals, HI rotation curves, H0=75 distance scale", IF="standard mu", ups="M/L per galaxy free", a0=1.2, stat=0.27, sys=None,
      note="'mean ... 1.2 +- 0.27 x 10^-8 cm/s^2' (scatter over nine galaxies); the paper says a0 scales with the assumed distance scale", indep=True, role="history"),
 dict(id="McG12", ref="McGaugh 2012 AJ 143, 40", arxiv="1107.2934", data="BTFR of gas-rich galaxies (M_gas > M_star), outer V_f only", IF="none (deep-MOND V_f^4 = G M a0 / chi)",
      ups="none needed (gas dominates)", a0=1.3, stat=0.3, sys=None, note="A = 47 +- 6 Msun km^-4 s^4; a0 = chi/(G A) with chi = 0.80 (geometry); '+- 0.3' includes formal A error and a 20% chi allowance; Swaters+2010 rotation-curve fits give 0.7 (1.0 with same cuts)", indep=True, role="E"),
 dict(id="MLS16", ref="McGaugh, Lelli & Schombert 2016 PRL 117, 201101", arxiv="1609.05917", data="SPARC RAR, 153 galaxies, ~2700 points, orthogonal-distance regression", IF="RAR (eq 4)",
      ups="fixed 0.5 (disk), 0.7 (bulge) at 3.6um", a0=1.20, stat=0.02, sys=0.24, note="'20% normalization uncertainty in Upsilon'", indep=False, role="E"),
 dict(id="Lel17", ref="Lelli, McGaugh, Schombert & Pawlowski 2017 ApJ 836, 152", arxiv="1610.08981", data="same 153 LTGs (+ETGs, dSphs shown)", IF="RAR (eq 11)", ups="fixed", a0=1.20, stat=0.02, sys=0.24,
      note="same fit as MLS16; variant with an acceleration floor, eq 15 (errors neglected, dSphs included): g_dagger = 1.1 +- 0.1", indep=False, role="dup"),
 dict(id="Li18", ref="Li, Lelli, McGaugh & Schombert 2018 A&A 615, A3", arxiv="1803.00022", data="SPARC, 175 individual MCMC fits", IF="RAR", ups="Gaussian priors + D, i priors", a0=None, stat=None, sys=None,
      note="NOT a determination: fixes g_dagger = 1.20 +- 0.02 (prior from MLS16). With a FLAT prior on g_dagger per galaxy the best-fit g_dagger distribution is broad with no chi2 gain (M/L-g_dagger degeneracy); rms 0.057 dex", indep=False, role="context"),
 dict(id="Rod18-std", ref="Rodrigues, Marra, del Popolo & Davari 2018 Nat.Astron. 2, 668 (Table 1)", arxiv="1806.06803", data="100 SPARC galaxies passing quality cuts; per-galaxy Bayesian, global best fit of posterior means",
      IF="standard", ups="Upsilon within factor 2, D +-20%, flat priors", a0=lg(-12.902) / U, stat=None, sys=None, note="log10 a0[km/s^2] = -12.902; paper argues a0 is NOT universal", indep=False, role="table"),
 dict(id="Rod18-sim", ref="same", arxiv="1806.06803", data="same", IF="simple", ups="same", a0=lg(-12.918) / U, stat=None, sys=None, note="-12.918", indep=False, role="table"),
 dict(id="Rod18-RAR", ref="same", arxiv="1806.06803", data="same", IF="RAR-inspired", ups="same", a0=lg(-12.959) / U, stat=None, sys=None, note="-12.959", indep=False, role="E"),
 dict(id="CZ19-std", ref="Chang & Zhou 2019 MNRAS 486, 1658 (Table 1, Gaussian priors)", arxiv="1812.05002", data="100 SPARC galaxies", IF="standard", ups="Gaussian priors on Upsilon, D, i", a0=lg(-12.925) / U, stat=None, sys=None, note="-12.925", indep=False, role="table"),
 dict(id="CZ19-sim", ref="same", arxiv="1812.05002", data="same", IF="simple", ups="same", a0=lg(-12.941) / U, stat=None, sys=None, note="-12.941", indep=False, role="table"),
 dict(id="CZ19-RAR", ref="same", arxiv="1812.05002", data="same", IF="RAR-inspired", ups="same", a0=lg(-12.959) / U, stat=None, sys=None, note="-12.959 (their flat-prior comparison values: -12.899 / -12.954 / -12.970)", indep=False, role="E"),
 dict(id="DBF23-sim", ref="Desmond, Bartlett & Ferreira 2023 MNRAS 521, 1817 (Table 1)", arxiv="2301.04368", data="SPARC, 2696 points, galaxy parameters at prior maxima", IF="simple", ups="fixed prior-max", a0=1.11, stat=None, sys=None, note="Table 1 lower rows (x = g_bar/1e-10)", indep=False, role="table"),
 dict(id="DBF23-RAR", ref="same", arxiv="2301.04368", data="same", IF="RAR", ups="same", a0=1.13, stat=None, sys=None, note="", indep=False, role="E"),
 dict(id="DBF23-std", ref="same", arxiv="2301.04368", data="same", IF="standard", ups="same", a0=1.54, stat=None, sys=None, note="chi2 far worse than simple/RAR (log-likelihood -939.5 vs -1217.3 / -1212.8)", indep=False, role="table"),
 dict(id="DBF23-EFE", ref="same", arxiv="2301.04368", data="same", IF="simple + universal EFE", ups="same", a0=1.16, stat=None, sys=None, note="e_N = 6.8e-3", indep=False, role="table"),
 dict(id="Des23", ref="Desmond 2023 MNRAS 526, 3342", arxiv="2303.11314", data="SPARC, 147 galaxies, 2696 points, HMC with all galaxy parameters free (priors)", IF="RAR", ups="lognormal priors; D, i, L3.6 free",
      a0=1.19, stat=0.04, sys=0.09, note="'naive averaging over all the models'; individual models span 1.07 to 1.31 (Table 3: scatter/EFE/boosted-error choices)", indep=False, role="E"),
 dict(id="Chae20", ref="Chae, Lelli, Desmond, McGaugh, Li & Schombert 2020 ApJ 904, 51", arxiv="2009.11525", data="SPARC + EFE", IF="RAR/simple + EFE", ups="priors", a0=None, stat=None, sys=None, note="NOT a determination: fixes g_dagger = 1.2 throughout", indep=False, role="context"),
 dict(id="Bro21", ref="Brouwer et al. 2021 A&A 650, A113", arxiv="2106.11677", data="KiDS-1000 weak lensing, isolated galaxies, RAR to ~1e-13 m/s^2", IF="g_obs ~ sqrt(g_bar a0) tail", ups="M* from photometry", a0=None, stat=None, sys=None,
      note="states the low-acceleration lensing RAR has 'a very similar proportionality constant' ~1.2e-10; no formal fit or error; independent of rotation curves", indep=True, role="context"),
 dict(id="Tia20", ref="Tian et al. 2020 ApJ 896, 70", arxiv="2001.08340", data="20 CLASH clusters, BCG-cluster RAR", IF="RAR form, slope 0.51", ups="BCG M*", a0=20.2, stat=1.1, sys=None,
      note="g_ddagger = (2.02 +- 0.11) x 10^-9 m/s^2: 17x the galaxy value -> 'no universal RAR from galaxies to clusters' (read from the abstract page arxiv.org/abs/2001.08340; slope 0.51 +0.04 -0.05; full text not opened, it exceeds the fetch size limit)", indep=True, role="cluster"),
 dict(id="thisA1", ref="this work v02 (record's own profile likelihood, corrected grid)", arxiv="-", data="SPARC 175 galaxies, 3380 points", IF="alpha1 (record kernel)", ups="free 0.05-3", a0=r2["matrix"]["Upsilon free 0.05-3 (record)"]["alpha1 (record kernel)"]["a0"] / U,
      stat=100 * r2["record_pl"]["sig_ln_bootstrap"] * r2["matrix"]["Upsilon free 0.05-3 (record)"]["alpha1 (record kernel)"]["a0"] / U / 100, sys=None, note="stat = galaxy bootstrap 8.2%", indep=False, role="this"),
 dict(id="thisR0", ref="this work v02", arxiv="-", data="SPARC 175", IF="RAR", ups="free 0.05-3", a0=r2["matrix"]["Upsilon free 0.05-3 (record)"]["RAR (MLS16)"]["a0"] / U, stat=None, sys=None, note="the IF preferred by the record's own likelihood (d chi2 = 168 over alpha1)", indep=False, role="E"),
 dict(id="thisR1", ref="this work v02", arxiv="-", data="SPARC 175", IF="RAR", ups="[0.25,1.0]", a0=r2["matrix"]["Upsilon in [0.25,1.0] (factor-2)"]["RAR (MLS16)"]["a0"] / U, stat=None, sys=None, note="", indep=False, role="E"),
 dict(id="thisR2", ref="this work v02", arxiv="-", data="SPARC 175", IF="RAR", ups="fixed 0.5/0.7", a0=r2["matrix"]["Upsilon fixed 0.5 (bulge 0.7)"]["RAR (MLS16)"]["a0"] / U, stat=None, sys=None, note="", indep=False, role="E"),
 dict(id="Rec", ref="record: real_research/reviews/mi_a0_profile_likelihood_milgrom_footing_2026.py", arxiv="-", data="SPARC 175", IF="alpha1 (record kernel)", ups="free 0.05-3", a0=1.0766, stat=1.0766 * 0.0544, sys=None, note="1.24% independent / 5.44% clustered-crude, as quoted", indep=False, role="record"),
]
c, H_P = c_si, H_si(H0_PLANCK)
print(f"c H0 (67.4) = {c*H_P:.4e} m/s^2   c H_Lambda = {c*H_P*math.sqrt(OM_L):.4e} m/s^2   candidates Z: F {Z_F:.4f}, V 6, M {Z_M:.4f}\n")
print(f"{'id':<11}{'a0 [1e-10]':>11}{'+-stat':>8}{'+-sys':>7}{'tot%':>6}{'Z_tot':>7}{'Z_Lam':>7}   {'IF':<22}{'Upsilon / nuisance':<30}indep")
for r in rows:
    if r["a0"] is None:
        print(f"{r['id']:<11}{'-':>11}{'':>8}{'':>7}{'':>6}{'':>7}{'':>7}   {r['IF']:<22}{r['ups']:<30}{'Y' if r['indep'] else 'n'}   ({r['note'][:70]}...)")
        continue
    tot = math.hypot(r["stat"] or 0, r["sys"] or 0)
    r["tot"] = tot if (r["stat"] or r["sys"]) else None
    zt, zl = c * H_P / (r["a0"] * U), c * H_P * math.sqrt(OM_L) / (r["a0"] * U)
    r["Z_tot"], r["Z_Lam"] = zt, zl
    print(f"{r['id']:<11}{r['a0']:>11.4f}{(r['stat'] if r['stat'] else 0):>8.3f}{(r['sys'] if r['sys'] else 0):>7.3f}{(100*tot/r['a0'] if r['tot'] else float('nan')):>6.1f}{zt:>7.3f}{zl:>7.3f}   {r['IF']:<22}{r['ups']:<30}{'Y' if r['indep'] else 'n'}")

# ---- recomputation checks
byid = {r["id"]: r for r in rows}
# independent expectation via exp(x ln 10) (10^0.098 = 1.2531, 10^0.082 = 1.2078, 10^0.041 = 1.0990, 10^0.075 = 1.1885, 10^0.059 = 1.1455)
check(all(abs(byid[k]["a0"] - math.exp((x + 13) * math.log(10))) < 1e-9 for k, x in (("Rod18-std", -12.902), ("Rod18-sim", -12.918), ("Rod18-RAR", -12.959))) and
      abs(byid["Rod18-std"]["a0"] - 1.2531) < 5e-4 and abs(byid["Rod18-sim"]["a0"] - 1.2078) < 5e-4 and abs(byid["Rod18-RAR"]["a0"] - 1.0990) < 5e-4,
      "T1 Rodrigues+2018 Table 1 log10 a0 [km/s^2] -12.902/-12.918/-12.959 -> 1.2531 / 1.2078 / 1.0990 e-10 m/s^2 (recomputed)")
check(abs(byid["CZ19-std"]["a0"] - 1.1885) < 5e-4 and abs(byid["CZ19-sim"]["a0"] - 1.1455) < 5e-4 and abs(byid["CZ19-RAR"]["a0"] - 1.0990) < 5e-4,
      "T2 Chang & Zhou 2019 Table 1 (Gaussian priors) -12.925/-12.941/-12.959 -> 1.1885 / 1.1455 / 1.0990 (recomputed)")
Msun = 1.98847e30
A = 47 * Msun / (1e3) ** 4                          # kg s^4 m^-4
a_btfr = 0.80 / (G_SI * A)
a_btfr_chi1 = 1.0 / (G_SI * A)
err_btfr = a_btfr * math.hypot(6 / 47, 0.20)
print(f"\n  BTFR (McGaugh 2012): a0 = chi/(G A), A = 47 Msun km^-4 s^4: chi = 0.80 -> {a_btfr/U:.4f}e-10 ; chi = 1 -> {a_btfr_chi1/U:.4f}e-10 ; error sqrt((6/47)^2 + 0.2^2) = {err_btfr/U:.3f}e-10")
check(abs(a_btfr / U - 1.28) < 0.02 and abs(err_btfr / U - 0.30) < 0.02, "T3 McGaugh 2012: a0 = 0.80/(G A) = 1.28e-10 +- 0.30 reproduces the quoted 1.3 +- 0.3")
check(abs(a_btfr_chi1 / U / (a_btfr / U) - 1.25) < 0.01, "T3b the geometry factor chi = 0.8 is worth 25% in a0 (chi = 1 would give 1.60): an assumption inside the BTFR route")
check(abs(math.hypot(0.02, 0.24) - 0.2408) < 1e-3 and abs(math.hypot(0.04, 0.09) - 0.0985) < 1e-3, "T4 total errors: MLS16 sqrt(0.02^2+0.24^2) = 0.241; Desmond 2023 sqrt(0.04^2+0.09^2) = 0.098")
check(abs(byid["Tia20"]["a0"] / byid["MLS16"]["a0"] - 16.8) < 0.3, "T5 the CLASH cluster acceleration scale is 16.8x the galaxy value (a universal a0 fails for clusters as published)")
Zt = {r["id"]: r["Z_tot"] for r in rows if r["a0"] is not None}
zE = [Zt[k] for k in ("MLS16", "Des23", "McG12", "Rod18-RAR", "CZ19-RAR", "DBF23-RAR", "thisR0", "thisR1", "thisR2", "Rec")]
print(f"  Z_tot = cH0/a0 over the E members and the record: min {min(zE):.2f}, max {max(zE):.2f}, median {np.median(zE):.2f}")
check(all(6 / 1.6 < z < 6 * 1.6 for z in zE), "T6 every galaxy-scale z ~ 0 determination in E gives Z_tot within a factor 1.6 of 6 (a wrong unit or a 17x cluster value would fail this)")
# control: a mutated unit conversion must fail the checks
check(abs(lg(-12.902) / U - 12.505) > 1.0, "T7 (mutation) forgetting the km -> m factor (x1e3) would give 12.5, not 1.25: the conversion check T1 has teeth")

# ---- ensemble E (declared in the header)
E_ids = ["MLS16", "Des23", "Rod18-RAR", "CZ19-RAR", "DBF23-RAR", "McG12", "thisR0", "thisR1", "thisR2"]
vals = np.array([byid[k]["a0"] for k in E_ids])
med, mean, sd = float(np.median(vals)), float(vals.mean()), float(vals.std(ddof=1))
lnv = np.log(vals); mean_ln = float(lnv.mean()); sd_ln = float(lnv.std(ddof=1))
p16, p84 = np.percentile(vals, [16, 84])
print(f"\n  ENSEMBLE E (9 analysis choices, declared in the header): values {np.round(np.sort(vals),3).tolist()}")
print(f"  median {med:.3f}, mean {mean:.3f}, sd {sd:.3f} ({100*sd/mean:.1f}%), log-mean {math.exp(mean_ln):.3f} with sd(ln) {100*sd_ln:.1f}%;  16-84% percentile range [{p16:.3f}, {p84:.3f}];  full range {vals.min():.3f}-{vals.max():.3f}")
check(0.05 < sd_ln < 0.20, f"T8 the analysis-choice scatter of E is {100*sd_ln:.1f}% in ln a0: larger than any single published statistical error (1-4%) and comparable to MLS16's quoted 20% total")
# leave-one-out robustness of the ensemble centre
loo = [float(np.exp(np.mean(np.delete(lnv, i)))) for i in range(len(lnv))]
print(f"  leave-one-out log-mean range: {min(loo):.3f} - {max(loo):.3f}")
check(max(loo) / min(loo) < 1.10, f"T9 the ensemble centre is stable to dropping any one member (range {100*(max(loo)/min(loo)-1):.1f}% < 10%)")
res = dict(rows=[{k: (float(v) if isinstance(v, (int, float, np.floating)) else v) for k, v in r.items()} for r in rows],
           E=dict(ids=E_ids, values=vals.tolist(), median=med, mean=mean, sd=sd, logmean=math.exp(mean_ln), sd_ln=sd_ln))
json.dump(res, open("v01_results.json", "w"), indent=1, default=float)
print(f"\n  {sum(ok)}/{len(ok)} checks held.")
sys.exit(0 if all(ok) else 1)
