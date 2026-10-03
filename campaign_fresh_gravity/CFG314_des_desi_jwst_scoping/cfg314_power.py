#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG314 -- pre-flight power arithmetic for the DES / DESI / JWST scoping lane.

Scoping only. No data file is read except the DESI DR2 chain margestats already on disk (text, 4 files) and the
record's committed nu_mono kernel (imported read-only from CFG3_common). Every literature number is typed in below
with its source; every assumption is labelled ASSUMPTION. kappa = 1/2 is FITTED.

Rows:
  P1  DESI DR1 BGS spec-z isolated lenses x (DES Y3, KiDS-1000, HSC Y3): replicate the KiDS early/late split.
  P2  Lensing a0(z): DESI BGS (z~0.25) vs DESI LRG (z~0.8) x HSC/DES, flat vs a0 ~ H(z), with the M*-drift wall.
  P3  DESI DR1 PV Tully-Fisher zero point across 0.03 < z < 0.10.
  P4  JWST z~4-6 grism discs (Danhaive+25 class): baryon calibration needed to separate flat from H(z).
  P5  DESI DR2 w0wa fits: shift of the predicted local a0 (the kappa footing) and of a0(z) under the sqrt(rho_DE) branch.
  P6  COSMOS-Web galaxy-galaxy lensing at z~1 (order of magnitude).
  P7  DESI MWS radial velocities for ultra-faint dispersions.
Run from the repository root:  python3 campaign_fresh_gravity/CFG314_des_desi_jwst_scoping/cfg314_power.py
MUTATE=1 flips the rival's sign (a0 ~ 1/H(z)) so the H(z)-dependent rows must change; the rows that do not depend on
the rival must stay the same, and the script checks that it notices.
"""
import os, sys, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
EXT = os.path.join(os.path.dirname(REPO), "_external_data")
sys.path.insert(0, CFG)
import CFG3_common as C3  # read-only: nu_mono only

MUTATE = os.environ.get("MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
OM = 0.315  # ASSUMPTION: flat background used for the rival's H(z) (Planck-like; the record's convention)
CHECKS, NUM = [], {}


def check(name, ok, detail, load_bearing=True):
    CHECKS.append(dict(name=name, ok=bool(ok), detail=detail, load_bearing=load_bearing))
    print(("PASS " if ok else "FAIL ") + name + " :: " + detail)


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + 1 - OM)


def dlog_a0_rival(z1, z2):
    """log10 a0(z2)/a0(z1) for the rival a0 ~ H(z) (MUTATE: a0 ~ 1/H)."""
    s = -1.0 if MUTATE else 1.0
    return s * math.log10(E(z2) / E(z1))


def DA(z, n=4000):
    """angular-diameter distance in units of c/H0, flat background"""
    zz = np.linspace(0, z, n)
    chi = np.trapz(1 / np.sqrt(OM * (1 + zz) ** 3 + 1 - OM), zz)
    return chi / (1 + z)


# ------------------------------------------------------------------------------------------------ P1
print("\n== P1  DESI spec-z isolated lenses: the early/late split (B's one specific failure)")
# KiDS reference (record): split in baryons needed 0.35-0.4 dex (CFG95) -> deep-regime ESD offset = half of it.
S_split = 0.5 * 0.375          # dex in g_obs at fixed g_bar (deep regime, g_obs ~ sqrt(g_bar))
z_kids = 4.4                   # CFG88 jackknife significance in the 1-halo bins
sig_kids = S_split / z_kids    # implied per-split error on KiDS
B_pred = 0.5 * 0.07            # B with its own dynamical calibration (CFG95: +0.07 dex baryon differential)
N_kids, n_kids = 181477, 6.2   # CFG96 isolated lenses; KiDS-1000 n_eff (arcmin^-2)
S_K = N_kids * n_kids
areas = {"KiDS-1000": (446.3, 6.2), "DES-Y3": (587.5, 5.6), "HSC-Y3": (413.3, 19.9)}  # 2512.15960 Tab.3; n_eff CFG255 1a
rows = {}
for nb in (500.0, 730.0):          # ASSUMPTION bracket: DR1 BGS density (5.5e6 / 7500 deg^2 = 733 deg^-2 is the mean)
    for fi in (0.16, 0.26):        # ASSUMPTION bracket: isolated fraction (Mistele 16% strict; Brouwer ~26%)
        for which in ("all3", "no_HSC", "DES_only"):
            keys = [k for k in areas if (which == "all3") or (which == "no_HSC" and k != "HSC-Y3") or (which == "DES_only" and k == "DES-Y3")]
            S_D = sum(areas[k][0] * nb * fi * areas[k][1] for k in keys)
            sig = sig_kids * math.sqrt(S_K / S_D)
            rows[f"nb{int(nb)}_f{fi}_{which}"] = dict(sigma=sig, z_if_real=S_split / sig, z_B_vs_split=(S_split - B_pred) / sig,
                                                     z_B_vs_split_x158=(S_split - B_pred) / (1.58 * sig), N_lens=sum(areas[k][0] for k in keys) * nb * fi)
for k, v in rows.items():
    print(f"  {k:24s} N_lens {v['N_lens']:9.0f}  sigma_S {v['sigma']:.4f} dex  split-if-real {v['z_if_real']:.1f} sig  "
          f"B-vs-split {v['z_B_vs_split']:.1f} sig  (x1.58 cov: {v['z_B_vs_split_x158']:.1f})")
NUM["P1"] = dict(S_split=S_split, sig_kids=sig_kids, B_pred=B_pred, rows=rows)
lo = min(v["z_B_vs_split_x158"] for k, v in rows.items() if k.endswith("no_HSC"))
hi = max(v["z_B_vs_split"] for k, v in rows.items() if k.endswith("all3"))
check("P1a arithmetic: KiDS per-split sigma = S/4.4", abs(sig_kids - 0.0426) < 0.001, f"sigma_KiDS {sig_kids:.4f} dex")
check("P1b without HSC (public shear only) the worst cell with x1.58 covariance still separates B from the split at >= 2 sigma",
      lo >= 2.0, f"worst no-HSC cell {lo:.2f} sigma; best all-3 cell {hi:.2f} sigma")
check("P1c [reported] the replication is statistically CRISPY in the median cell (>= 3 sigma B vs split, no inflation, all 3 surveys)",
      rows["nb730_f0.16_all3"]["z_B_vs_split"] >= 3, f"{rows['nb730_f0.16_all3']['z_B_vs_split']:.2f} sigma", load_bearing=False)

# ------------------------------------------------------------------------------------------------ P2
print("\n== P2  Lensing a0(z): BGS z 0.25 vs LRG z 0.8")
zl, zh = 0.25, 0.80
d_rival = 0.5 * dlog_a0_rival(zl, zh)    # deep-regime amplitude shift
req_total = abs(d_rival) / 3.0           # 3 sigma
req_Mdrift = 2 * req_total               # an M* drift delta moves the amplitude by delta/2 (CFG255)
# statistical estimate for the high-z leg (order of magnitude; ASSUMPTIONS stated)
pen = (DA(zh) / DA(zl)) ** 2             # fewer sources per physical annulus
n_src_behind = {"HSC-Y3": 8.0, "DES-Y3": 2.0, "KiDS-1000": 1.5}   # ASSUMPTION: n_eff behind z~0.8 lenses
nLRG_iso = 600.0 * 0.5 * 0.15            # ASSUMPTION: 600 deg^-2 targets, DR1 completeness 0.5, isolated 15%
S_hi = sum(areas[k][0] * nLRG_iso * n_src_behind[k] for k in areas) / pen
sig_hi = sig_kids * math.sqrt(S_K / S_hi) / math.sqrt(2)   # sig_kids is a split (difference of 2 halves); one amplitude ~ /sqrt2
sig_lo = sig_kids / math.sqrt(2)
sig_stat = math.hypot(sig_hi, sig_lo)
print(f"  rival deep-amplitude shift {d_rival:+.4f} dex; needs total sigma <= {req_total:.4f}; M* drift <= {req_Mdrift:.4f} dex")
print(f"  D_A penalty {pen:.2f}; stat sigma high-z leg {sig_hi:.4f}, low-z {sig_lo:.4f}, combined {sig_stat:.4f} -> {abs(d_rival)/sig_stat:.1f} sigma (stat only)")
hot_gas_sys = (0.5 * 0.1, 0.5 * 0.3)    # ASSUMPTION: LRG-vs-BGS hot-gas baryon difference 0.1-0.3 dex -> half in amplitude
print(f"  hot-gas baryon difference 0.1-0.3 dex -> {hot_gas_sys[0]:.3f}-{hot_gas_sys[1]:.3f} dex in amplitude (vs signal {abs(d_rival):.3f})")
NUM["P2"] = dict(d_rival=d_rival, req_total=req_total, req_Mdrift=req_Mdrift, DA_penalty=pen, sig_stat=sig_stat, hot_gas_sys=hot_gas_sys)
check("P2a rival shift BGS->LRG in the deep amplitude lies in CFG255's 0.06-0.09 dex window", 0.06 <= d_rival <= 0.09, f"{d_rival:+.4f} dex")
check("P2b the M*-drift requirement is tighter than the published SPS method-to-method systematic (0.2 dex) -> systematic-limited",
      req_Mdrift < 0.2, f"needs <= {req_Mdrift:.3f} dex across z; 0.2 dex method-to-method (Brouwer+21)")
check("P2c [reported] the hot-gas difference can be as large as the whole signal", hot_gas_sys[1] >= abs(d_rival) * 0.9,
      f"{hot_gas_sys[1]:.3f} vs {abs(d_rival):.3f}", load_bearing=False)

# ------------------------------------------------------------------------------------------------ P3
print("\n== P3  DESI DR1 PV Tully-Fisher zero point, 0.03 < z < 0.10")
b_TF, s_int, N_TF = -7.22, 0.466, 10262   # 2512.03227 abstract
zg = np.linspace(0.03, 0.10, 20001); w = zg ** 2   # ASSUMPTION: volume-limited-like p(z) ~ z^2
cdf = np.cumsum(w) / w.sum(); zmed = zg[np.searchsorted(cdf, 0.5)]
zlo = np.sum(zg[zg < zmed] * w[zg < zmed]) / np.sum(w[zg < zmed]); zhi = np.sum(zg[zg >= zmed] * w[zg >= zmed]) / np.sum(w[zg >= zmed])
dla = dlog_a0_rival(zlo, zhi); dla_full = dlog_a0_rival(0.03, 0.10)
dM_slope = -b_TF * dla / 4.0      # fixed L: dlogV = dlog a0 / 4
dM_btfr = 2.5 * dla               # fixed V: L ~ 1/a0
sig_half = s_int / math.sqrt(N_TF / 2) * math.sqrt(2)
Qunc = 0.5                        # ASSUMPTION: luminosity-evolution uncertainty +-0.5 mag per unit z (r band)
evo = Qunc * (zhi - zlo)
print(f"  halves z {zlo:.4f} / {zhi:.4f}; rival dlog a0 {dla:+.4f} dex (full range {dla_full:+.4f})")
print(f"  intercept shift {dM_slope:.4f} (slope map) - {dM_btfr:.4f} (BTFR map) mag; stat sigma {sig_half:.4f} mag; evolution unc {evo:.4f} mag")
NUM["P3"] = dict(zlo=zlo, zhi=zhi, dla=dla, dM=(dM_slope, dM_btfr), sig_stat=sig_half, evo_unc=evo)
check("P3a rival lever across the whole PV range is < 0.02 dex in a0", abs(dla_full) < 0.02, f"{dla_full:+.4f} dex")
check("P3b NOT POSSIBLE: the luminosity-evolution uncertainty alone matches or exceeds the signal between halves",
      evo >= 0.5 * abs(dM_slope), f"evolution {evo:.4f} mag vs signal {abs(dM_slope):.4f}-{abs(dM_btfr):.4f} mag")

# ------------------------------------------------------------------------------------------------ P4
print("\n== P4  JWST z~4-6 grism discs: baryons needed by FLAT vs the rival at fixed dynamics")
nu = C3.nu_mono
from scipy.optimize import brentq
z4 = 4.17                         # CFG273 PALL median z
r_riv = 10 ** dlog_a0_rival(0.0, z4)
D_star = 4.35                     # CFG273 median g_obs / g_bar,* at r_e (stars only)
# FLAT at the canonical scale needs (1+mu) = 3.9 (CFG273 PALL gas-to-stars 2.9). Back out y_* (stars-only y, canonical a0)
f_flat = 3.9
y_star = brentq(lambda y: nu(y * f_flat) * f_flat - D_star, 1e-4, 1e3)
def need(r):  # total baryon / stars needed under a0 multiplied by r
    return brentq(lambda f: nu(y_star * f / r) * f - D_star, 1e-3, 1e4)
f_r = need(r_riv)
sep = math.log10(f_flat / f_r)
# conditioned-sample spread: y_* bracket from CFG273's y range for conditioned rows
seps = {}
for ys in (0.08, 0.3, 1.0, 3.0):
    try:
        ff = brentq(lambda f: nu(ys * f) * f - D_star, 1e-3, 1e4)
        fr = brentq(lambda f: nu(ys * f / r_riv) * f - D_star, 1e-3, 1e4)
        seps[ys] = (ff, fr, math.log10(ff / fr) if fr > 0 else float('nan'))
    except ValueError:
        seps[ys] = None
print(f"  rival a0 ratio at z {z4}: {r_riv:.2f} ({math.log10(r_riv):+.3f} dex); y_* {y_star:.3f}")
print(f"  M_b/M* needed: FLAT {f_flat:.2f}, rival {f_r:.2f}; separation {sep:+.3f} dex in baryon mass")
for ys, v in seps.items():
    print(f"   y_*={ys}: " + ("no solution" if v is None else f"FLAT {v[0]:.2f}  rival {v[1]:.2f}  sep {v[2]:+.3f} dex"))
req_cal = abs(sep) / 3
gas_scaling_unc = 0.3             # ASSUMPTION: scaling-relation gas extrapolated to z~4-6, shared zero point ~0.3 dex
print(f"  3 sigma needs a SHARED baryon calibration <= {req_cal:.3f} dex; scaling-relation gas ~{gas_scaling_unc} dex (f_gas ~0.77)")
NUM["P4"] = dict(z=z4, a0_ratio=r_riv, y_star=y_star, f_flat=f_flat, f_rival=f_r, sep_dex=sep, req_cal=req_cal, seps={str(k): v for k, v in seps.items()})
check("P4a rival a0 ratio at z~4.2 is > 6", r_riv > 6, f"{r_riv:.2f}")
check("P4b FLAT needs more baryons than the rival at the same dynamics (sep > 0)", sep > 0, f"sep {sep:+.3f} dex")
check("P4c NOT POSSIBLE with scaling-relation gas: required shared calibration is below the gas zero-point uncertainty",
      req_cal < gas_scaling_unc, f"needs <= {req_cal:.3f} dex vs ~{gas_scaling_unc} dex")

# P4d: the record's own stars-only upper bounds (CFG273, committed CSV, read-only) against the rival at each disc's z.
# Gas can only LOWER a stars-only s*, so a 95% upper bound below E(z) would exclude the rival robustly against gas.
import csv
p273 = os.path.join(CFG, "CFG273_danhaive_gold41", "cfg273_points_stageB_relabelled.csv")
below_c, below_95, sig0 = [], [], 0
for r in csv.DictReader(open(p273)):
    if r["no_root"] == "1":
        continue
    z, s, hi = float(r["z"]), float(r["s_star"]), float(r["stat95_hi"])
    riv = 10 ** dlog_a0_rival(0.0, z)
    if s < riv:
        below_c.append((r["object"], round(z, 2), round(s, 2), round(hi, 1), round(riv, 2)))
        sig0 += int(r["sigma0_limit"] == "1")
    if hi < riv:
        below_95.append(r["object"])
print(f"  CFG273 rooted discs with central s* below the rival: {len(below_c)} ({sig0} are sigma0-limit rows); with 95% upper bound below: {len(below_95)}")
for b in below_c:
    print("   ", b)
NUM["P4d"] = dict(central_below=below_c, upper95_below=below_95)
check("P4d [reported] no CFG273 disc's 95% stars-only upper bound excludes the rival (per-disc errors span ~2 dex)",
      len(below_95) == 0, f"central-below {len(below_c)}, 95%-below {len(below_95)}", load_bearing=False)

# ------------------------------------------------------------------------------------------------ P5
print("\n== P5  DESI DR2 w0wa fits: predicted local a0 and a0(z) under the sqrt(rho_DE) branch")
def margestat(path, name):
    for line in open(path):
        p = line.split()
        if p and p[0] == name:
            import re
            return float(re.match(r"[-+]?[0-9.]+", p[1]).group(0))  # central value of the 68% column
    raise KeyError(name)
planck = 67.4 ** 2 * (1 - 0.315)
P5 = {}
for fit in ("cmb", "desy5", "pantheonplus", "union3"):
    fp = os.path.join(EXT, "desi_dr2_chains", fit, "chain.margestats")
    H0, om, w0, wa = (margestat(fp, k) for k in ("H0", "omegam", "w", "wa"))
    shift0 = 0.5 * math.log10(H0 ** 2 * (1 - om) / planck)   # a0 ~ sqrt(rho_DE,0) ~ H0 sqrt(1-Om)
    def rho(z):  # CPL rho_DE(z)/rho_DE(0)
        a = 1 / (1 + z)
        return a ** (-3 * (1 + w0 + wa)) * math.exp(-3 * wa * (1 - a))
    P5[fit] = dict(H0=H0, om=om, w0=w0, wa=wa, dlog_a0_local=shift0, dlog_a0_z25=0.5 * math.log10(rho(2.5)))
    print(f"  {fit:13s} H0 {H0:6.2f} Om {om:.4f} w0 {w0:+.3f} wa {wa:+.2f}: local a0 shift {shift0:+.4f} dex; a0(2.5)/a0(0) {0.5*math.log10(rho(2.5)):+.3f} dex")
NUM["P5"] = P5
mx = max(abs(v["dlog_a0_local"]) for v in P5.values())
check("P5a every DESI DR2 w0wa fit moves the predicted local a0 by < 0.05 dex (local a0 is known only to ~0.16 dex: CFG309 0.9-1.31e-10)",
      mx < 0.05, f"max |shift| {mx:.4f} dex vs log10(1.31/0.9) = {math.log10(1.31/0.9):.3f}")
check("P5b [reported] a0(2.5) under the CPL branch spans about +-0.1 dex (CFG6: -0.10..+0.14)",
      max(abs(v["dlog_a0_z25"]) for v in P5.values()) < 0.2, ", ".join(f"{k} {v['dlog_a0_z25']:+.3f}" for k, v in P5.items()), load_bearing=False)

# ------------------------------------------------------------------------------------------------ P6
print("\n== P6  COSMOS-Web galaxy-galaxy lensing at z~1 (order of magnitude)")
area6 = 0.54                       # deg^2 NIRCam
nlens6 = 8000.0 * 0.25             # ASSUMPTION: 8000 deg^-2 with M*>1e10 at 0.5<z<1.5, 25% isolated
nsrc6 = 50.0                       # ASSUMPTION: of 129 arcmin^-2 shapes, ~50 behind z~1 lenses
pen6 = (DA(1.0) / DA(0.25)) ** 2
S6 = area6 * nlens6 * nsrc6 / pen6
sig6 = sig_kids / math.sqrt(2) * math.sqrt(S_K / S6)
d6 = 0.5 * dlog_a0_rival(0.0, 1.0)
print(f"  N_lens ~{area6*nlens6:.0f}; sigma_A ~{sig6:.3f} dex; rival deep shift at z=1 vs local {d6:+.3f} dex -> {abs(d6)/sig6:.2f} sigma (stat only)")
NUM["P6"] = dict(N_lens=area6 * nlens6, sigma=sig6, d_rival=d6)
check("P6 NOT POSSIBLE statistically: COSMOS-Web alone gives < 2 sigma on the rival at z~1", abs(d6) / sig6 < 2, f"{abs(d6)/sig6:.2f} sigma")

# ------------------------------------------------------------------------------------------------ P7
print("\n== P7  DESI MWS RVs for ultra-faint dispersions")
floor = (1.0, 2.0); sig_ufd = (2.0, 4.0)  # DESI systematic floor (bright/backup; data_assembly DESI_MWS_RV); UFD sigma range
# a dispersion needs per-star errors well below sigma; with floor ~ sigma, the binary-free sigma is lost in the deconvolution
ratio = floor[0] / sig_ufd[0], floor[1] / sig_ufd[0]
print(f"  floor/sigma for a 2 km/s UFD: {ratio[0]:.2f}-{ratio[1]:.2f}; Keck/DEIMOS floor 1.1 km/s already in the record's inputs (CFG257)")
check("P7 NOT POSSIBLE: DESI floor is >= half of the coldest UFD dispersions and no better than DEIMOS", ratio[0] >= 0.5, f"{ratio}")

# ------------------------------------------------------------------------------------------------ MUTATE sentinel
if MUTATE:
    check("MUTATE sentinel: the rival-dependent rows changed sign (P2a, P4a, P4b must fail)", d_rival < 0 and r_riv < 1 and sep < 0, f"d_rival {d_rival:+.4f}")
nf = sum(1 for c in CHECKS if not c["ok"] and c["load_bearing"])
print(f"\n{sum(c['ok'] for c in CHECKS)}/{len(CHECKS)} checks pass; load-bearing failures {nf}")
json.dump(dict(slug="CFG314_power" + SUF, mutate=MUTATE, checks=CHECKS, numbers=NUM), open(os.path.join(HERE, f"cfg314_power{SUF}_results.json"), "w"), indent=1, default=float)
sys.exit(1 if nf else 0)
