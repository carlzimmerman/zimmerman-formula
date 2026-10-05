#!/usr/bin/env python3
"""AUDIT_GLOBULARS_2026-10-05 -- independent recompute of the outer-halo globular tests (h93, CFG332, CFG334).

Reads the on-disk Baumgardt tables directly.  Imports nothing from h93/CFG332/CFG334; the only shared code is the
frozen kernel nu_mono (read-only, CFG3_common).  kappa = 1/2 fixed, both footings.  No downloads, no fitting.
Run from the repository root:  python3 campaign_fresh_gravity/AUDIT_GLOBULARS_2026-10-05/audit_globulars.py
"""
import os, sys, math, json
import numpy as np
from scipy.stats import norm, chi2

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "campaign_fresh_gravity"))
from CFG3_common import nu_mono, Y_PEAK  # noqa: E402  (frozen kernel, read-only)

G, MSUN, PC, KPC = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
UPS, DUPS_DEX = 1.6, 0.15            # SPS M/L_V (Kroupa, 12 Gyr, [Fe/H]~-1.5) and its prior width -- the record's values
MW_MB = 6.0e10                       # MW baryons only (point mass at 70-105 kpc) -- the record's value
EBV = {"NGC 2419": 0.08, "Pal 3": 0.04, "Pal 4": 0.01, "Pal 14": 0.04}   # Harris 2010 (hard-coded in h93; NOT on disk)
TGT = ["NGC 2419", "Pal 3", "Pal 4", "Pal 14"]
PUBLISHED = {"Pal 14": (0.38, 0.12, 16), "Pal 4": (0.87, 0.18, 23)}  # Jordi+09, Frank+12 (as quoted in h93)
OUT, LOG = {}, []


def P(s=""):
    print(s); LOG.append(s)


def nu_exp(y):
    y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


def num(s):
    """'7.83 +- 1.17 · 105' -> 7.83e5 (the web table writes 10^5 as '105')."""
    mult = 1.0
    if "·" in s:
        s, ex = s.split("·"); mult = 10 ** float(ex.strip()[2:])
    return float(s.split("+-")[0]) * mult


# ------------------------------------------------------------------ 1. provenance: three on-disk copies + BH2018
P("=" * 100); P("1. PROVENANCE -- the same four rows in every on-disk copy"); P("=" * 100)
D = os.path.join(ROOT, "real_research/data/globular_clusters")
tsv = {}
with open(os.path.join(D, "baumgardt_gc_parameters.tsv"), encoding="utf-8") as fh:
    hdr = None
    for line in fh:
        if line.startswith("#"): continue
        f = line.rstrip("\n").split("\t")
        if hdr is None: hdr = f; continue
        if f[0].strip() in TGT: tsv[f[0].strip()] = dict(zip(hdr, f))
comb = {}
for line in open(os.path.join(ROOT, "deepseek_push/data2/baumgardt_combined_table.txt"), encoding="utf-8"):
    if line.startswith("#"): continue
    f = line.split(); n = f[0].replace("_", " ")
    if n in TGT: comb[n] = f
csv = {}
for line in open(os.path.join(ROOT, "deepseek_push/data2/bhv4_parameters_2023.csv"), encoding="utf-8"):
    f = line.strip().split(",")
    if f[0] in TGT: csv[f[0]] = [float(x) for x in f[1:]]
bh18 = {}
for line in open(os.path.join(ROOT, "deepseek_push/data2/bh2018_cds_table2.dat"), encoding="utf-8"):
    n = line[2:14].strip()
    if n in TGT:
        bh18[n] = dict(NRV=int(line[15:19]), D=float(line[37:43]), M=float(line[45:52]), ML=float(line[61:66]),
                       eML=float(line[67:71]), rhl=float(line[84:89]), mf=line[108:114].strip(), sig0=float(line[115:119]))
prof = {n: [] for n in TGT}
for line in open(os.path.join(D, "baumgardt_gc_veldisp_profiles.tsv"), encoding="utf-8"):
    if line.startswith("#") or line.startswith("ClusterName"): continue
    f = line.rstrip("\n").split("\t")
    if f[0].strip() in TGT and f[6].strip() == "RV":
        prof[f[0].strip()].append([float(x) for x in f[1:6]])

GC = {}
worst = 0.0
for n in TGT:
    t = tsv[n]
    g = dict(D=num(t["R_sun[kpc]"]), RGC=num(t["R_GC[kpc]"]), NRV=int(t["N_RV"]), M=num(t["Mass[Msun]"]),
             V=num(t["V[mag]"]), ML=num(t["M/L_V"]), rhl=float(t["rh_l[pc]"]), rt=float(t["rt[pc]"]),
             sig0=float(t["sigma0[km/s]"]), mf=t["MFSlope"].strip())
    c = comb[n]
    cc = dict(D=float(c[3]), RGC=float(c[5]), NRV=int(c[7]), M=float(c[9]), V=float(c[11]), ML=float(c[13]),
              rhl=float(c[16]), sig0=float(c[30]))
    for k in cc: worst = max(worst, abs(cc[k] - g[k]) / abs(g[k]))
    for k, v in zip(["M", "rhl", "sig0"], csv[n]): worst = max(worst, abs(v - g[k]) / abs(g[k]))
    GC[n] = g
P(f"  TSV vs combined_table vs bhv4 csv (8 + 3 columns x 4 clusters): worst relative difference {worst:.1e}")
P("  NOTE: all three are the SAME 2023 web table (same retrieval generation) -- agreement is transcription, not independent confirmation.")
P("")
P("  version drift: Baumgardt & Hilker 2018 (CDS table2) vs the 2023 web table -- model outputs move, inputs barely do")
P(f"  {'cluster':9} {'N_RV 18->23':>12} {'D 18->23':>15} {'M_dyn 18->23':>22} {'M/L_dyn 18->23':>22} {'rh_l 18->23':>14} {'MF note 18':>10}")
drift = {}
for n in TGT:
    b, g = bh18[n], GC[n]
    P(f"  {n:9} {b['NRV']:5d}->{g['NRV']:<5d} {b['D']:7.2f}->{g['D']:<7.2f} {b['M']:9.2e}->{g['M']:<9.2e}   "
      f"{b['ML']:.2f}+-{b['eML']:.2f}->{g['ML']:.2f}   {b['rhl']:5.2f}->{g['rhl']:<6.2f} {b['mf'][-1]:>6}")
    drift[n] = dict(ML18=b["ML"], ML23=g["ML"], NRV18=b["NRV"], NRV23=g["NRV"], mfnote18=b["mf"][-1])
P("  MF note: c = slope from observed mass functions; d = slope ESTIMATED from relaxation time (a Newtonian-dynamics prior).")
OUT["provenance"] = dict(worst_copy_diff=worst, drift=drift)

# ------------------------------------------------------------------ Baumgardt's model vs his own measured bins
P(""); P("  Baumgardt's N-body central sigma_0 (MODEL) vs his own innermost measured RV bin (DATA):")
modfit = {}
for n in TGT:
    R, Ns, s, up, lo = prof[n][0]
    r_pc = R / 206265 * GC[n]["D"] * 1e3
    z = (s - GC[n]["sig0"]) / lo
    modfit[n] = dict(sig0=GC[n]["sig0"], bin=s, r_pc=r_pc, z=z)
    P(f"   {n:9} sigma_0(model) {GC[n]['sig0']:4.2f}  bin {s:4.2f} +{up:.2f}/-{lo:.2f} at {r_pc:5.1f} pc (N={int(Ns)})   "
      f"bin/model {s/GC[n]['sig0']:4.2f}  ({z:+.1f} sigma)")
P("  -> Pal 3 is the only cluster where Baumgardt's own Newtonian model sits ~3 sigma BELOW his own data: his Pal 3 mass/M/L is")
P("     NOT a dynamical measurement from those 22 stars (set by the light profile / priors), so M/L_dyn = 1.45 must not be read as one.")
OUT["model_vs_bin"] = modfit

# ------------------------------------------------------------------ 2. measured inputs only
P(""); P("=" * 100); P("2. MEASURED INPUTS (V, E(B-V), distance, r_h,l, RV bins) -> L_V, Newton and law predictions"); P("=" * 100)
for n in TGT:
    g = GC[n]
    MV = g["V"] - 3.1 * EBV[n] - 5 * math.log10(g["D"] * 1e3 / 10)
    g["LV"] = 10 ** (-0.4 * (MV - 4.83))
    g["ML_check"] = g["M"] / g["LV"] / g["ML"]
    pr = np.array(prof[n]); Rpc = pr[:, 0] / 206265 * g["D"] * 1e3
    if len(pr) == 1:
        g["sobs"], g["up"], g["lo"], g["robs"] = pr[0, 2], pr[0, 3], pr[0, 4], Rpc[0]
    else:
        ls = np.interp(math.log10(g["rhl"]), np.log10(Rpc), np.log10(pr[:, 2]))
        fe = np.interp(math.log10(g["rhl"]), np.log10(Rpc), 0.5 * (pr[:, 3] + pr[:, 4]) / pr[:, 2])
        g["sobs"] = 10 ** ls; g["up"] = g["lo"] = g["sobs"] * fe; g["robs"] = g["rhl"]
        # light-weighted global alternative: Plummer annuli split at the geometric means between bin radii
        edges = np.concatenate([[0], np.sqrt(Rpc[1:] * Rpc[:-1]), [np.inf]])
        a = g["rhl"]; frac = lambda R: 1.0 if np.isinf(R) else R ** 2 / (R ** 2 + a ** 2)
        w = np.array([frac(edges[i + 1]) - frac(edges[i]) for i in range(len(Rpc))])
        g["s_global_lw"] = math.sqrt(float((w * pr[:, 2] ** 2).sum()))
        g["bins"] = list(zip(Rpc.round(1), pr[:, 2]))
    P(f"  {n:9} M_V {MV:7.3f}  L_V {g['LV']:.3e}  (M_dyn/L_V)/(M/L_V quoted) = {g['ML_check']:.3f}   r_h,l {g['rhl']:5.2f} pc  "
      f"r_t {g['rt']:6.1f} pc (r_t/r_h {g['rt']/g['rhl']:.1f})  sigma_obs {g['sobs']:.3f} at {g['robs']:.1f} pc")
g = GC["NGC 2419"]
P(f"  NGC 2419 global sigma: interpolated-at-r_h 4.77 (used by h93/CFG332) vs light-weighted over its 3 bins {g['s_global_lw']:.2f} km/s")
P("  Pal 14: r_t/r_h = 1.7 -- the model's tidal radius (computed in a MW potential WITH a dark halo; not used by any test) is")
P("          barely outside r_h: Pal 14 is tidally extended, so equilibrium is in doubt in either gravity.")


def sig_newton_wolf(M, rhl):
    return math.sqrt(G * M * MSUN / (6 * (4 / 3) * rhl * PC)) / 1e3


def sig_newton_plummer(M, rhl):          # isotropic Plummer: global LOS sigma^2 = (3 pi / 64) G M / a, a = R_e
    return math.sqrt(3 * math.pi / 64 * G * M * MSUN / (rhl * PC)) / 1e3


def law(g, a0, ups=UPS, kern=nu_exp, MWb=MW_MB):
    M = ups * g["LV"]; r12 = (4 / 3) * g["rhl"] * PC
    yi = G * (M / 2) * MSUN / r12 ** 2 / a0
    ye = G * MWb * MSUN / (g["RGC"] * KPC) ** 2 / a0
    sN = sig_newton_wolf(M, g["rhl"])
    nu_alg = float(kern(yi + ye)); nu_iso = float(kern(yi))
    dl = 1e-4; L = (math.log(float(kern(ye * (1 + dl)))) - math.log(float(kern(ye * (1 - dl))))) / (2 * dl)
    s_efedom = sN * math.sqrt(float(kern(ye)) * (1 + L / 3))
    s_dmond = (4 / 81 * G * M * MSUN * a0) ** 0.25 / 1e3
    return dict(yi=yi, ye=ye, sN=sN, sF=sN * math.sqrt(nu_alg), s_iso=sN * math.sqrt(nu_iso), s_efedom=s_efedom,
                s_dmond=s_dmond)


P("")
P(f"  kernel check: nu_mono (frozen, peak y = {Y_PEAK:.2f}) vs exp-RAR nu_s at every cluster's y:")
kd = max(abs(float(nu_mono(np.array([law(GC[n], a0)['yi'] + law(GC[n], a0)['ye']]))[0]) / float(nu_exp(law(GC[n], a0)['yi'] + law(GC[n], a0)['ye'])) - 1)
         for n in TGT for a0 in A0.values())
P(f"    max |nu_mono/nu_s - 1| = {kd:.1e}  -> the h93/CFG332 use of nu_s is the record's kernel here")
OUT["kernel_max_reldiff"] = kd

P("")
res = {}
for fk, a0 in A0.items():
    P(f"  footing {fk} (a0 = {a0:.3e})   [Upsilon_V = 1.6 SPS; MW baryons 6e10 point mass]")
    P(f"   {'cluster':9} {'y_int':>7} {'y_ext':>7} {'sigObs':>7} {'N_Wolf':>7} {'N_Plum':>7} {'law_alg':>8} {'law_iso':>8} "
      f"{'deepMOND':>8} {'EFEdom':>7} {'obs/N':>6} {'obs/law':>7} {'Ups_req N':>9} {'Ups_req F':>9}")
    res[fk] = {}
    for n in TGT:
        g = GC[n]; r = law(g, a0)
        sP = sig_newton_plummer(UPS * g["LV"], g["rhl"])
        # required Upsilon: Newton exact (sigma ~ sqrt(Ups)); law by bisection
        uN = UPS * (g["sobs"] / r["sN"]) ** 2
        lo_, hi_ = 1e-3, 100.0
        for _ in range(80):
            mid = math.sqrt(lo_ * hi_)
            (lo_, hi_) = (mid, hi_) if law(g, a0, ups=mid)["sF"] < g["sobs"] else (lo_, mid)
        uF = math.sqrt(lo_ * hi_)
        res[fk][n] = dict(r, sP=sP, uN=uN, uF=uF, sobs=g["sobs"])
        P(f"   {n:9} {r['yi']:7.4f} {r['ye']:7.4f} {g['sobs']:7.3f} {r['sN']:7.3f} {sP:7.3f} {r['sF']:8.3f} {r['s_iso']:8.3f} "
          f"{r['s_dmond']:8.3f} {r['s_efedom']:7.3f} {g['sobs']/r['sN']:6.3f} {g['sobs']/r['sF']:7.3f} {uN:9.2f} {uF:9.2f}")
OUT["predictions"] = res

# r_h sensitivity: the h93 caveat says a 10% r_h error moves BOTH laws by 5%
P("")
P("  r_h,l sensitivity (+10%):  d ln sigma / Newton vs law (canonical)")
rs = {}
for n in TGT:
    g = dict(GC[n]); b = law(g, A0["canonical"]); g["rhl"] *= 1.1; a = law(g, A0["canonical"])
    rs[n] = (a["sN"] / b["sN"] - 1, a["sF"] / b["sF"] - 1)
    P(f"   {n:9} Newton {100*rs[n][0]:+5.1f}%   law {100*rs[n][1]:+5.1f}%")
P("  -> h93's caveat ('moves BOTH gravity laws equally') is wrong for the three deep-MOND clusters: the law is nearly r-independent")
P("     there.  Size of the slip: a 10% r_h error shifts the Newton-vs-law differential by ~4%.  Immaterial to every verdict.")
OUT["rh_sensitivity"] = rs

# ------------------------------------------------------------------ 3. tension statistic, with the PUBLISHED errors
P(""); P("=" * 100); P("3. TENSION, using each bin's PUBLISHED asymmetric error (log-normal) + 0.075 dex in sigma for Upsilon"); P("=" * 100)
SIG_UPS = 0.5 * DUPS_DEX * math.log(10)


def zval(sobs, up, lo, spred):
    e = 0.5 * (math.log(1 + up / sobs) - math.log(1 - lo / sobs))
    return (math.log(sobs) - math.log(spred)) / math.hypot(e, SIG_UPS), e


def fisher_two_sided(zs):
    p = [max(2 * norm.sf(abs(z)), 1e-300) for z in zs]
    X = -2 * sum(math.log(x) for x in p); pc = chi2.sf(X, 2 * len(p))
    return pc, float(norm.isf(max(pc, 1e-300)))


chi_vs_pub = {}
for n in TGT:
    g = GC[n]; N = g["NRV"] if n != "NGC 2419" else 62
    chi_vs_pub[n] = (0.5 * (g["up"] + g["lo"]) / g["sobs"], 1 / math.sqrt(2 * (N - 1)))
P("  error check: published fractional error vs the chi^2_(N-1) width used by h93/CFG332's p_low:")
for n in TGT:
    P(f"   {n:9} published {chi_vs_pub[n][0]:.3f}   chi^2_(N-1) {chi_vs_pub[n][1]:.3f}   ratio {chi_vs_pub[n][0]/chi_vs_pub[n][1]:.2f}")
P("  -> the chi^2_(N-1) statistic ignores per-star velocity errors and is 20-45% tighter than the published errors in the sparse clusters")
OUT["err_ratio"] = chi_vs_pub

tens = {}
for fk in A0:
    tens[fk] = {}
    for model, key in [("Newton (class E)", "sN"), ("law + alg EFE (h93)", "sF"), ("law isolated (B)", "s_iso")]:
        zs = {n: zval(GC[n]["sobs"], GC[n]["up"], GC[n]["lo"], res[fk][n][key])[0] for n in TGT}
        p4, s4 = fisher_two_sided(list(zs.values()))
        p3, s3 = fisher_two_sided([zs[n] for n in TGT if n != "Pal 3"])
        zpub = dict(zs)
        for n, (s, e, _) in PUBLISHED.items():
            zpub[n] = zval(s, e, e, res[fk][n][key])[0]
        pp, sp = fisher_two_sided(list(zpub.values()))
        zj = dict(zs); zj["Pal 14"] = zpub["Pal 14"]
        pj, sj = fisher_two_sided([zj[n] for n in TGT if n != "Pal 3"])
        tens[fk][model] = dict(z=zs, T4=s4, T_noPal3=s3, T_published=sp, T_noPal3_Jordi=sj)
        P(f"  {fk:9} {model:21} z: " + "  ".join(f"{n} {zs[n]:+5.2f}" for n in TGT) +
          f"  | T4 {s4:5.2f}  noPal3 {s3:5.2f}  pub-alt {sp:5.2f}  noPal3+Jordi {sj:5.2f}")
OUT["tension"] = tens

# leave-one-out for the law (does one cluster dominate?)
P("")
for fk in A0:
    zs = tens[fk]["law + alg EFE (h93)"]["z"]
    loo = {n: fisher_two_sided([zs[m] for m in TGT if m != n])[1] for n in TGT}
    P(f"  {fk:9} law leave-one-out T: " + "  ".join(f"drop {n} {loo[n]:.2f}" for n in TGT))
    OUT.setdefault("law_loo", {})[fk] = loo

# ------------------------------------------------------------------ 4. CFG334 binaries: clipping + joint consistency
P(""); P("=" * 100); P("4. BINARIES -- the CFG334 model (DM91 periods, flat q, thermal e, M1 0.8, periastron >= 30 Rsun), re-implemented"); P("=" * 100)
rng = np.random.default_rng(20261005)
NDRAW = 20000


def binary_dv(n):
    out = np.empty(n); k0 = 0
    while k0 < n:
        m = 4 * (n - k0) + 100
        Pd = 10 ** rng.normal(4.8, 2.3, m); q = rng.uniform(0.1, 1, m); e = np.sqrt(rng.uniform(0, 1, m))
        a = (G * 0.8 * (1 + q) * MSUN * (Pd * 86400) ** 2 / (4 * math.pi ** 2)) ** (1 / 3)
        ok = (a * (1 - e) >= 30 * 6.957e8) & (a < 0.1 * PC)
        Pd, q, e, a = Pd[ok], q[ok], e[ok], a[ok]; k = len(Pd)
        i = np.arccos(rng.uniform(-1, 1, k)); w = rng.uniform(0, 2 * math.pi, k); Mn = rng.uniform(0, 2 * math.pi, k)
        E = Mn.copy()
        for _ in range(40): E = E - (E - e * np.sin(E) - Mn) / (1 - e * np.cos(E))
        th = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
        K = 2 * math.pi * a / (Pd * 86400) * q / (1 + q) * np.sin(i) / np.sqrt(1 - e ** 2)
        v = K * (np.cos(th + w) + e * np.cos(w)) / 1e3
        t = min(k, n - k0); out[k0:k0 + t] = v[:t]; k0 += t
    return out


def ml(v, e, mask):
    w0 = mask.astype(float); n = w0.sum(1)
    mu = (w0 * v).sum(1) / n
    s2 = np.maximum((w0 * (v - mu[:, None]) ** 2).sum(1) / np.maximum(n - 1, 1) - e ** 2, 1e-4)
    for _ in range(100):
        wt = w0 / (s2[:, None] + e ** 2)
        mu = (wt * v).sum(1) / wt.sum(1)
        s2 = np.maximum((w0 * (wt ** 2) * ((v - mu[:, None]) ** 2 - e ** 2)).sum(1) / (w0 * wt ** 2).sum(1), 1e-4)
    return np.sqrt(s2), mu


def sim(sint, N, f, e, clip):
    v = rng.normal(0, sint, (NDRAW, N)); isb = rng.uniform(0, 1, (NDRAW, N)) < f
    if isb.sum(): v[isb] += binary_dv(int(isb.sum()))
    v = v + rng.normal(0, e, (NDRAW, N))
    mask = np.ones_like(v, bool)
    s, mu = ml(v, e, mask)
    if clip:
        for _ in range(5):
            mask = np.abs(v - mu[:, None]) <= 3 * np.sqrt(s[:, None] ** 2 + e ** 2)
            s, mu = ml(v, e, mask)
    return s


bin_res = {}
fk = "canonical"
for clip in (False, True):
    for e in (1.0, 0.5):
        for f in (0.0, 0.1, 0.3, 0.5):
            row = {}
            for n in ["Pal 3", "Pal 4", "Pal 14"]:
                sN = res[fk][n]["sN"]; N = GC[n]["NRV"]
                s = sim(sN, N, f, e, clip)
                row[n] = float((s >= GC[n]["sobs"]).mean()) if n == "Pal 3" else float((s <= GC[n]["sobs"]).mean())
                row[n + "_med"] = float(np.median(s))
            row["joint"] = row["Pal 3"] * row["Pal 4"] * row["Pal 14"]
            row["fisher_p"] = float(chi2.sf(-2 * math.log(max(row["joint"], 1e-300)), 6))
            bin_res[f"clip{int(clip)}_e{e}_f{f}"] = row
            P(f"  {'3-sig clip' if clip else 'no clip  '} e {e:.1f} f {f:.1f}:  P(Pal3 >= 1.70) {row['Pal 3']:.3f} (med {row['Pal 3_med']:.2f})"
              f" | P(Pal4 <= 0.88) {row['Pal 4']:.3f} (med {row['Pal 4_med']:.2f}) | P(Pal14 <= 0.71) {row['Pal 14']:.3f}"
              f" (med {row['Pal 14_med']:.2f}) | Fisher p {row['fisher_p']:.3f}")
P("  intrinsic sigma = Newton (Wolf, Upsilon 1.6): Pal 3 %.2f, Pal 4 %.2f, Pal 14 %.2f km/s" %
  tuple(res[fk][n]["sN"] for n in ["Pal 3", "Pal 4", "Pal 14"]))
P("  CFG334 frozen rule: EXPLAIN if P(Pal 3) >= 0.05 at (0.75, e 1.0, f 0.3); PLAUSIBLE if only at f 0.5 / e 1.5.")
P("  -> unclipped (as CFG334 ran it) the primary P reproduces (~0.26). With a standard 3-sigma clip the primary falls to ~0.045:")
P("     the verdict would read PLAUSIBLE, not EXPLAIN.  Whether Baumgardt's 1.70 was clipped/membership-filtered is NOT on disk.")
P("  -> joint test (same binary population in all three sparse clusters, Newton intrinsic): Fisher p >= ~0.1 at f 0.3 --")
P("     a binary population big enough for Pal 3 leaves Pal 4 / Pal 14 low-ish but not inconsistent.  Not a refutation.")
OUT["binaries"] = bin_res

json.dump(OUT, open(os.path.join(HERE, "audit_globulars_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "audit_globulars.out"), "w").write("\n".join(LOG) + "\n")
