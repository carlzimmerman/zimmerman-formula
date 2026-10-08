#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG465 -- input audit of the globular verdicts (CFG332 three routes, CFG333 one ownership rule).  See FROZEN_CRITERIA.md.

Every CFG332/CFG333 globular input is traced to a source on disk or cited in the record and graded (A paper-verified, B
catalogue-only, C mismatched, U unsourced).  The verdicts are re-run on BASE (control), (a) sourced-only, (a') paper-verified
(reported) and (b) the full factorial over the record's alternative values, both footings separately.
kappa = 1/2 FITTED and fixed.  Kernels as committed (CFG332 exp-RAR nu_s form; CFG333 nu_mono).  On-disk data only.
Run:     python3 campaign_fresh_gravity/CFG465_globular_inputs_audit/cfg465_globular_inputs.py          (~2-3 min)
MUTATE:  CFG465_MUTATE=1 python3 ...   (Pal 4 sigma x2 in BASE; writes *_MUTATE.* outputs)
"""
import os, sys, math, json, itertools, functools
import numpy as np
from scipy.stats import chi2 as chi2dist, norm

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
sys.path.insert(0, LANES); sys.path.insert(0, os.path.join(REPO, "hunt_2026"))
import CFG7_common as C7                                  # noqa: E402  nu_mono, as CFG333 imports it (read-only)
from hunt_lib import G, kpc, Msun, A0                     # noqa: E402  constants and footings, as CFG332 imports them

MUT = os.environ.get("CFG465_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok))); P(f"  [{'PASS' if ok else 'FAIL'}] {name}  ({detail})")


FOOTS = list(A0)                                          # canonical 9.36e-11, alt 1.13e-10
PC = 3.0857e16; MSUN_V = 4.83; UPS_V = 1.6; WID = 0.15; R0_KPC = 8.178
TGT = ["NGC 2419", "Pal 3", "Pal 4", "Pal 14"]
EBV = {"NGC 2419": 0.08, "Pal 3": 0.04, "Pal 4": 0.01, "Pal 14": 0.04}      # 'Harris (2010)' as hard-coded in h93 (cited)
FRANK = (0.87, 0.18, 0.18, 23)        # Frank+12, MNRAS 423, 2917 -- quoted in hunt_2026/h93_outer_halo_globulars.py L170
JORDI = (0.38, 0.12, 0.12, 16)        # Jordi+09, AJ 137, 4586   -- quoted in hunt_2026/h93_outer_halo_globulars.py L169
MW_BASE, MW_ALTS = 6.0e10, (5.0e10, 7.3e10)   # 6e10 h93/FG001/CFG333; 5e10 hunt_2026/h37 bracket; 7.3e10 CFG286 census-high

# ======================================================================================== data
GCDIR = os.path.join(REPO, "real_research", "data", "globular_clusters")
COMB = os.path.join(REPO, "deepseek_push", "data2", "baumgardt_combined_table.txt")
BHV4 = os.path.join(REPO, "deepseek_push", "data2", "bhv4_parameters_2023.csv")
BH18 = os.path.join(REPO, "deepseek_push", "data2", "bh2018_cds_table2.dat")


def rows(fn):
    out = {}
    for line in open(fn, encoding="utf-8"):
        if line.startswith("#") or line.startswith("ClusterName"): continue
        f = line.rstrip("\n").split("\t"); out.setdefault(f[0].strip(), []).append(f)
    return out


def num(s):
    """'7.83 +- 1.17 · 105' -> 7.83e5 (the web table writes 10^5 as '105')."""
    mult = 1.0
    if "·" in s:
        s, ex = s.split("·"); mult = 10 ** float(ex.strip()[2:])
    return float(s.split("+-")[0]) * mult


par, prof = rows(os.path.join(GCDIR, "baumgardt_gc_parameters.tsv")), rows(os.path.join(GCDIR, "baumgardt_gc_veldisp_profiles.tsv"))
C23 = {}
for n in TGT:
    f = par[n][0]
    C23[n] = dict(RA=float(f[1]), DEC=float(f[2]), D=float(f[3].split("+-")[0]), RGC=float(f[4].split("+-")[0]), NRV=int(f[5]),
                  M=num(f[7]), V=float(f[8].split("+-")[0]), ML=float(f[9].split("+-")[0]), rhl=float(f[11]), sig0=float(f[21]),
                  bins=[(float(p[1]), int(p[2]), float(p[3]), float(p[4]), float(p[5])) for p in prof[n] if p[6].strip() == "RV"])
MF = {}
COMBROW = {}
for line in open(COMB, encoding="utf-8"):
    if line.startswith("#"): continue
    f = line.split(); nm = f[0].replace("_", " ")
    if nm in TGT:
        MF[nm] = dict(mlow=float(f[26]), mhigh=float(f[27]), alpha=float(f[28]), dalpha=float(f[29])); COMBROW[nm] = f
BHV = {}
for line in open(BHV4, encoding="utf-8"):
    f = line.strip().split(",")
    if f[0] in TGT: BHV[f[0]] = [float(x) for x in f[1:]]
B18 = {}
for line in open(BH18, encoding="utf-8"):
    nm = line[2:14].strip()
    if nm in TGT:
        B18[nm] = dict(NRV=int(line[15:19]), D=float(line[37:43]), Dnote=line[43], M=float(line[45:52]), ML=float(line[61:66]),
                       rmlp=float(line[84:89]), alpha=float(line[108:113]), MFnote=line[113], sig0=float(line[115:119]))

# ======================================================================================== provenance (fixed in FROZEN_CRITERIA.md)
PROV = [
    # (input, cluster, value used in CFG332/333, grade, source, alternatives in the record)
    ("sigma_obs", "NGC 2419", "4.771 (bins interp. at r_h; N 62)", "B catalogue-only",
     "Baumgardt web veldisp table (retrieved 2026-09-03), 3 RV bins N 62/62/59 = 183; BH2018 table2 lists N_RV 195; Ibata+11 / "
     "Baumgardt+09 named in the record, values and star lists NOT on disk", "light-weighted global over the 3 bins (AUDIT 1b), N 183"),
    ("sigma_obs", "Pal 3", "1.70 +0.38/-0.30 (N 22)", "U UNSOURCED",
     "Baumgardt web veldisp table only; BH2018 lists N_RV 14 (8 stars added from an unnamed source); no paper in the record names "
     "the stars; catalogue's own Newtonian model sigma0 0.80 sits 3.0 sigma below the bin", "none measured (sigma0 0.80 is a Newtonian model output: excluded)"),
    ("sigma_obs", "Pal 4", "0.88 +0.20/-0.17 (N 23)", "A paper-verified",
     "Baumgardt web veldisp table; N 23 = BH2018 N_RV 23 = Frank+12 (MNRAS 423, 2917) 23 members, 0.87 +- 0.18 quoted in h93", "Frank+12 0.87 +- 0.18"),
    ("sigma_obs", "Pal 14", "0.71 +0.18/-0.14 (N 16)", "C MISMATCHED",
     "Baumgardt web veldisp table; N 16 = Jordi+09 (AJ 137, 4586) 16 members, but Jordi+09 report 0.38 +- 0.12 (quoted in h93); "
     "BH2018 lists N_RV 17", "Jordi+09 0.38 +- 0.12 (A)"),
    ("D_sun", "all", "2023 catalogue 88.47/94.84/101.39/73.58 kpc", "A",
     "Baumgardt & Vasiliev 2021 via the 2023 parameter table (header names the paper)", "BH2018 table2 'literature' distances 83.20/92.50/103.00/71.00 (A)"),
    ("R_GC", "all", "2023 catalogue 95.93/98.17/104.05/68.55 kpc", "A (derived)",
     "2023 parameter table; reproduced from D and position with R0 = 8.178 kpc (C5)", "recomputed at the BH2018 distances"),
    ("V (apparent)", "all", "10.56/14.56/14.23/14.13", "B catalogue-only",
     "2023 parameter table; primary photometry not named", "via BH2018 Mass/(M/L_V)"),
    ("E(B-V)", "all", "0.08/0.04/0.01/0.04", "cited, not on disk",
     "'Harris (2010)' hard-coded in h93/CFG332/CFG333; Harris 2010 catalogue NOT on disk (needs owner go)", "none in the record"),
    ("L_V", "all", "from V, E(B-V), D (1.29e4 Pal 3, 1.16e4 Pal 14 ...)", "B derived",
     "rebuilt; matches the 2023 catalogue's own Mass/(M/L_V) to 1-3%", "BH2018 table2 Mass/(M/L_V) (A, derived): NGC 2419 4.40e5, Pal 3 2.16e4, Pal 4 1.82e4, Pal 14 6.68e3 at BH2018 D"),
    ("r_h,l", "all", "19.76/20.16/15.88/27.63 pc", "B (N-body fit to surface density)",
     "2023 parameter table", "BH2018 table2 rmlp 18.29/19.69/17.87/23.60 pc (A)"),
    ("Upsilon_V prior", "all", "lognormal(1.6, 0.15 dex)", "assumption",
     "h93's stated SPS fiducial (12 Gyr, [Fe/H] ~ -1.5, Kroupa); no SPS table on disk", "band edges 1.3 / 2.2 (reported, not scored); route 2 MF-slope Upsilon"),
    ("MF slope (route 2)", "all", "-1.57/-1.14/-0.34/-1.26 (2023)", "B (Newtonian N-body)",
     "2023 combined table cols 28-29", "BH2018 -1.50 d / -1.50 d / -1.52 c / -1.52 c (A; d = estimated from relaxation time)"),
    ("M_MW,b (g_ext)", "all", "6e10 point mass", "parameter",
     "h93 / FG001 / CFG333 (the framework's MW baryons)", "5e10 (hunt_2026/h37 bracket), 7.3e10 (CFG286 census-high)"),
    ("binary correction", "all", "none", "not applied",
     "no measured correction on disk; CFG334 is a model (OVERSTATED per AUDIT)", "none measured (needs multi-epoch RVs: owner go)"),
    ("Newtonian model outputs", "all", "sigma0, M_dyn, M/L_dyn", "never an input",
     "used only as checks in h93/AUDIT", "-"),
]

# ======================================================================================== geometry
_T = np.array([[-0.0548755604162154, -0.8734370902348850, -0.4838350155487132],
               [+0.4941094278755837, -0.4448296299600112, +0.7469822444972189],
               [-0.8676661490190047, -0.1980763734312015, +0.4559837761750669]])   # ICRS(J2000) -> Galactic


def rgc_geom(n, D):
    ra, de = math.radians(C23[n]["RA"]), math.radians(C23[n]["DEC"])
    x, y, z = _T @ np.array([math.cos(de) * math.cos(ra), math.cos(de) * math.sin(ra), math.sin(de)])
    return math.sqrt((D * x - R0_KPC) ** 2 + (D * y) ** 2 + (D * z) ** 2)


# ======================================================================================== variant -> clusters
BASE = dict(n2419="rh", p3="cat", p4="cat", p14="cat", D="23", L="23", R="23", MW=MW_BASE, MF="23")
SOURCED = dict(BASE, p3="drop", p4="frank", p14="jordi")
PAPER = dict(SOURCED, n2419="drop")
FACTORS = [("n2419", ["rh", "global"]), ("p3", ["cat", "drop"]), ("p4", ["cat", "frank"]), ("p14", ["cat", "jordi"]),
           ("D", ["23", "18"]), ("L", ["23", "18"]), ("R", ["23", "18"]), ("MW", [MW_BASE, *MW_ALTS]), ("MF", ["23", "18"])]


def vkey(ch):
    return "|".join(f"{k}={ch[k]:.1e}" if k == "MW" else f"{k}={ch[k]}" for k, _ in FACTORS)


def build(ch, mutate_pal4=False):
    gcs = []
    for n in TGT:
        c = C23[n]; b = B18[n]
        Du = c["D"] if ch["D"] == "23" else b["D"]
        if ch["L"] == "23":
            MV = c["V"] - 3.1 * EBV[n] - 5 * math.log10(Du * 1e3 / 10.0); LV = 10 ** (0.4 * (MSUN_V - MV))
        else:
            LV = b["M"] / b["ML"] * (Du / b["D"]) ** 2
        rhl = c["rhl"] * (Du / c["D"]) if ch["R"] == "23" else b["rmlp"] * (Du / b["D"])
        RGC = c["RGC"] if ch["D"] == "23" else rgc_geom(n, Du)
        sel = {"NGC 2419": ch["n2419"], "Pal 3": ch["p3"], "Pal 4": ch["p4"], "Pal 14": ch["p14"]}[n]
        if sel == "drop":
            continue
        bins = c["bins"]
        if sel == "frank":
            so, up, lo, N = FRANK
        elif sel == "jordi":
            so, up, lo, N = JORDI
        elif len(bins) == 1:
            _, N, so, up, lo = bins[0]
        else:
            Rpc = np.array([x[0] for x in bins]) / 206265.0 * Du * 1e3; s = np.array([x[2] for x in bins])
            e = 0.5 * (np.array([x[3] for x in bins]) + np.array([x[4] for x in bins])); Ns = np.array([x[1] for x in bins])
            if sel == "rh":
                ls = np.interp(math.log10(rhl), np.log10(Rpc), np.log10(s)); le = np.interp(math.log10(rhl), np.log10(Rpc), e / s)
                so = 10 ** ls; up = lo = so * le; N = int(Ns[int(np.argmin(np.abs(np.log10(Rpc) - math.log10(rhl))))])
            else:                                   # light-weighted global (AUDIT 1b): Plummer annuli split at geometric means
                edges = np.concatenate([[0.0], np.sqrt(Rpc[1:] * Rpc[:-1]), [np.inf]])
                frac = lambda R: 1.0 if np.isinf(R) else R ** 2 / (R ** 2 + rhl ** 2)
                w = np.array([frac(edges[i + 1]) - frac(edges[i]) for i in range(len(Rpc))])
                so = math.sqrt(float((w * s ** 2).sum())); d2 = math.sqrt(float(((w * 2 * s * e) ** 2).sum()))
                up = lo = d2 / (2 * so); N = int(Ns.sum())
        so, up, lo = float(so), float(up), float(lo)
        if mutate_pal4 and n == "Pal 4":
            so, up, lo = 2 * so, 2 * up, 2 * lo
        alpha = MF[n]["alpha"] if ch["MF"] == "23" else b["alpha"]
        gcs.append(dict(name=n, LV=LV, rhl=rhl, RGC=RGC, D=Du, so=so, eso=0.5 * (up + lo), up=up, lo=lo, N=int(N),
                        alpha=alpha, dalpha=MF[n]["dalpha"], gext=G * ch["MW"] * Msun / (RGC * kpc) ** 2, MW=ch["MW"]))
    return gcs


# ======================================================================================== CFG332 estimators (as committed)
Z = np.random.default_rng(931).standard_normal(4000)


def wolf_sigma(M_msun, rhl, boost=1.0):
    return np.sqrt(G * boost * np.asarray(M_msun) * Msun / (6.0 * (4.0 / 3.0) * rhl * PC)) / 1e3


def y_int(g, a0, ups): return G * (np.asarray(ups) * g["LV"] * Msun / 2) / ((4.0 / 3.0) * g["rhl"] * PC) ** 2 / a0


def nu_arr(y):
    y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 / (-np.expm1(-np.sqrt(y)))


def pred_newton(g, a0, ups): return wolf_sigma(np.asarray(ups) * g["LV"], g["rhl"])
def pred_efe_alg(g, a0, ups): return wolf_sigma(np.asarray(ups) * g["LV"], g["rhl"], nu_arr(y_int(g, a0, ups) + g["gext"] / a0))
def pred_iso(g, a0, ups): return wolf_sigma(np.asarray(ups) * g["LV"], g["rhl"], nu_arr(y_int(g, a0, ups)))


MU, WMU = np.polynomial.legendre.leggauss(200)


def flux_avg(gi, ge, a0):
    gi = np.asarray(gi, float)[..., None]
    gN = np.sqrt(np.maximum(gi ** 2 + ge ** 2 + 2 * gi * ge * MU, 1e-300))
    return 0.5 * np.sum(WMU * nu_arr(gN / a0) * (gi + ge * MU), axis=-1)


def pred_num(g, a0, ups):
    a = g["rhl"] * PC; r12 = (4.0 / 3.0) * a
    gi = G * np.asarray(ups) * g["LV"] * Msun * r12 / (r12 ** 2 + a ** 2) ** 1.5
    return wolf_sigma(np.asarray(ups) * g["LV"], g["rhl"], flux_avg(gi, g["gext"], a0) / gi)


def zobj(mc, ms):
    return float(norm.ppf(max(mc, 1e-300))) if mc <= 0.5 else float(norm.isf(max(ms, 1e-300)))


def fisher(ps): return float(chi2dist.sf(-2 * np.sum(np.log(np.clip(ps, 1e-300, 1))), 2 * len(ps)))


def score(fn, a0, gcs, centers, widths):
    pL, pT, zs = [], [], []
    for g in gcs:
        ups = centers[g["name"]] * 10 ** (widths[g["name"]] * Z)
        x = (g["N"] - 1) * (g["so"] / fn(g, a0, ups)) ** 2
        c, s = chi2dist.cdf(x, g["N"] - 1), chi2dist.sf(x, g["N"] - 1)
        pL.append(float(np.mean(c))); pT.append(float(np.mean(2 * np.minimum(c, 1 - c)))); zs.append(zobj(float(np.mean(c)), float(np.mean(s))))
    return dict(L=float(norm.isf(max(fisher(pL), 1e-300))), T=float(norm.isf(max(fisher(pT), 1e-300))), pT=pT, z=zs)


MLO, MTO, MBRK = 0.1, 0.80, 0.5


def dndm(m, alpha, branch):
    m = np.asarray(m, float)
    if branch == "kroupa": return np.where(m >= MBRK, m ** -2.3, 2.0 * m ** -1.3)
    A = MTO ** (-2.3 - alpha)
    if branch == "S": return A * m ** alpha
    return np.where(m >= MBRK, A * m ** alpha, 2.0 * A * m ** (alpha + 1))


_mg = np.linspace(MLO, MTO, 20001); _mi = np.linspace(MTO, 8.0, 20001)


def total_mass(alpha, branch):
    ms = np.trapz(_mg * dndm(_mg, alpha, branch), _mg)
    mfin = 0.109 * _mi + 0.394; mref = np.minimum(mfin, MTO)
    dep = dndm(mref, alpha, branch) / dndm(mref, 0, "kroupa")
    return ms + np.trapz(mfin * _mi ** -2.3 * dep, _mi)


MK = total_mass(0, "kroupa")


@functools.lru_cache(maxsize=None)
def ups_mf(alpha, branch): return UPS_V * total_mass(alpha, branch) / MK


def verdict332(Tc, Ta, bc, ba):
    if Tc < 2 and Ta < 2: return "MATCH"
    if Tc < 2 or Ta < 2 or (Tc <= bc / 2 and Ta <= ba / 2): return "PARTIAL"
    return "NOT"


# ======================================================================================== CFG333 GC cell (as committed)
def nu_m(y): return C7.nu_mono(np.maximum(np.asarray(y, float), 1e-14))


def gc_sigma333(g, a0, mode, ups):
    r12 = (4.0 / 3.0) * g["rhl"] * PC; M = np.asarray(ups) * g["LV"]
    sN = np.sqrt(G * M * Msun / (6.0 * r12)) / 1e3
    if mode == "own": return sN
    return sN * np.sqrt(nu_m(G * (M / 2) * Msun / r12 ** 2 / a0))


UPS_DRAWS = 1.6 * 10 ** (0.15 * Z)


def gc_stat333(gcs, a0, modes, ups_draws=UPS_DRAWS):
    ys = np.array([math.log(g["so"] / float(gc_sigma333(g, a0, md, 1.6))) for g, md in zip(gcs, modes)])
    es = np.array([math.hypot(g["eso"] / g["so"], 1 / math.sqrt(2 * (g["N"] - 1))) for g in gcs])
    w = 1 / es ** 2; m = float(np.sum(w * ys) / np.sum(w)); em = 1 / math.sqrt(float(np.sum(w)))
    U = 1.6 * math.exp(2 * m); eU = U * 2 * em
    tj = (U - 2.2) / eU if U > 2.2 else ((U - 1.3) / eU if U < 1.3 else 0.0)
    pl, pt, zs = [], [], []
    for g, md in zip(gcs, modes):
        x = (g["N"] - 1) * (g["so"] / gc_sigma333(g, a0, md, ups_draws)) ** 2
        F, S = chi2dist.cdf(x, g["N"] - 1), chi2dist.sf(x, g["N"] - 1)
        pl.append(float(np.mean(F))); pt.append(float(np.mean(2 * np.minimum(F, 1 - F)))); zs.append(zobj(float(np.mean(F)), float(np.mean(S))))
    return dict(ups=U, eups=eU, t_joint=tj, L=float(norm.isf(max(fisher(pl), 1e-300))), T_reported=float(norm.isf(max(fisher(pt), 1e-300))),
                z=zs, passes=bool(abs(tj) < 2 and float(norm.isf(max(fisher(pl), 1e-300))) < 2))


def labels333(gcs, a0, rule):
    out = []
    for g in gcs:
        r12 = (4.0 / 3.0) * g["rhl"] * PC
        gN = G * 0.5 * 1.6 * g["LV"] * Msun / r12 ** 2; gi = float(nu_m(gN / a0)) * gN
        gNh = G * g["MW"] * Msun / (g["RGC"] * kpc) ** 2; gh = float(nu_m(gNh / a0)) * gNh; gt = 2 * gh * r12 / (g["RGC"] * kpc)
        out.append({"R0": "top", "R1": "top" if gi > gt else "own", "R2": "own", "R3": "own" if gi < gh else "top"}[rule])
    return out


J333 = json.load(open(os.path.join(LANES, "CFG333_one_ownership_rule", "cfg333_one_rule_results.json")))
J332 = json.load(open(os.path.join(LANES, "CFG332_globulars_three_routes", "cfg332_globulars_results.json")))
JAUD = json.load(open(os.path.join(LANES, "AUDIT_GLOBULARS_2026-10-05", "audit_globulars_results.json")))
RULES = ["R0", "R1", "R2", "R3"]


def nonGC_pass(rule, pop, foot=None):
    if foot is None: return bool(J333["rules"][rule]["passes"][pop])
    return bool(abs(J333["rules"][rule]["res"][f"{pop}|{foot}"]["z"]) < 2)


def decide333(gc_pass):
    """gc_pass: rule -> bool.  Uses the committed WB/CL/UFD passes (combined)."""
    cnt = {r: sum(nonGC_pass(r, p) for p in ("WB", "CL", "UFD")) + int(gc_pass[r]) for r in RULES}
    best = max(cnt[r] for r in RULES[1:])
    lab = "ONE RULE WORKS" if best == 4 else ("PARTIAL" if best == 3 else "NONE")
    return lab, cnt


def decide333_foot(gc_pass, foot):
    cnt = {r: sum(nonGC_pass(r, p, foot) for p in ("WB", "CL", "UFD")) + int(gc_pass[r]) for r in RULES}
    best = max(cnt[r] for r in RULES[1:])
    return ("ONE RULE WORKS" if best == 4 else ("PARTIAL" if best == 3 else "NONE")), cnt


# ======================================================================================== AUDIT published-error statistic (tile number)
SIG_UPS = 0.5 * WID * math.log(10)


def pub_stat(gcs, a0, which, ups=UPS_V):
    zs = []
    for g in gcs:
        sp = float(pred_newton(g, a0, ups)) if which == "newton" else float(pred_efe_alg(g, a0, ups))
        e = 0.5 * (math.log(1 + g["up"] / g["so"]) - math.log(1 - g["lo"] / g["so"]))
        zs.append((math.log(g["so"]) - math.log(sp)) / math.hypot(e, SIG_UPS))
    p = [max(2 * norm.sf(abs(z)), 1e-300) for z in zs]
    pc = chi2dist.sf(-2 * sum(math.log(x) for x in p), 2 * len(p))
    return dict(T=float(norm.isf(max(pc, 1e-300))), z=zs)


# ======================================================================================== evaluate one variant
def evaluate(gcs, full=True):
    names = [g["name"] for g in gcs]
    SPS_C = {n: UPS_V for n in names}; SPS_W = {n: WID for n in names}
    out = {"clusters": names}
    for foot in FOOTS:
        a0 = A0[foot]; r = {}
        r["r1a"] = score(pred_newton, a0, gcs, SPS_C, SPS_W)
        r["r1bEFE"] = score(pred_efe_alg, a0, gcs, SPS_C, SPS_W)
        r["r1bB"] = score(pred_iso, a0, gcs, SPS_C, SPS_W)
        for br in ("S", "K"):
            Cc, Ww = {}, {}
            for g in gcs:
                u0 = ups_mf(round(g["alpha"], 6), br)
                up_, um_ = ups_mf(round(g["alpha"] + g["dalpha"], 6), br), ups_mf(round(g["alpha"] - g["dalpha"], 6), br)
                Cc[g["name"]] = u0; Ww[g["name"]] = math.hypot(WID, abs(math.log10(up_) - math.log10(um_)) / 2)
            r[f"r2{br}"] = score(pred_efe_alg, a0, gcs, Cc, Ww); r[f"r2{br}"]["ups_mf"] = Cc
            if full: r[f"r2{br}"]["newton_T"] = score(pred_newton, a0, gcs, Cc, Ww)["T"]
        r["r3"] = score(pred_num, a0, gcs, SPS_C, SPS_W)
        r["gc333"] = {}
        for rule in RULES:
            lab = labels333(gcs, a0, rule); st = gc_stat333(gcs, a0, lab); st["labels"] = lab; r["gc333"][rule] = st
        if full:
            r["gc333_modes"] = {md: gc_stat333(gcs, a0, [md] * len(gcs)) for md in ("own", "top")}
        r["pub_newton"] = pub_stat(gcs, a0, "newton"); r["pub_law"] = pub_stat(gcs, a0, "law")
        r["decision"] = decide333_foot({ru: r["gc333"][ru]["passes"] for ru in RULES}, foot)
        out[foot] = r
    bc, ba = out["canonical"]["r1bEFE"]["T"], out["alt"]["r1bEFE"]["T"]
    out["labels332"] = {k: verdict332(out["canonical"][k]["T"], out["alt"][k]["T"], bc, ba) for k in ("r1a", "r1bEFE", "r1bB", "r2S", "r2K", "r3")}
    gcp = {ru: out["canonical"]["gc333"][ru]["passes"] and out["alt"]["gc333"][ru]["passes"] for ru in RULES}
    out["gc333_combined"] = gcp
    out["decision333"] = decide333(gcp)
    return out


ROUTES = [("r1a", "1(a) class E Newton"), ("r1bEFE", "1(b-EFE) law + alg EFE"), ("r1bB", "1(b-B) isolated law"),
          ("r2S", "2 MF-slope Ups, branch S"), ("r2K", "2 MF-slope Ups, branch K"), ("r3", "3 full QUMOND monopole")]


def outcomes(ev):
    """element -> {foot: pass bool, 'label': combined label}."""
    o = {}
    for k, _ in ROUTES:
        o["E_" + k] = {f: ev[f][k]["T"] < 2 for f in FOOTS}; o["E_" + k]["label"] = ev["labels332"][k]
    for ru in RULES:
        o["E_gc333_" + ru] = {f: ev[f]["gc333"][ru]["passes"] for f in FOOTS}
        o["E_gc333_" + ru]["label"] = "PASS" if ev["gc333_combined"][ru] else "FAIL"
    o["E_decision333"] = {f: ev[f]["decision"][0] for f in FOOTS}; o["E_decision333"]["label"] = ev["decision333"][0]
    o["E_pub_newton"] = {f: ev[f]["pub_newton"]["T"] < 2 for f in FOOTS}
    o["E_pub_newton"]["label"] = "pass" if all(o["E_pub_newton"][f] for f in FOOTS) else "fail"
    o["E_pub_law"] = {f: ev[f]["pub_law"]["T"] < 2 for f in FOOTS}
    o["E_pub_law"]["label"] = "pass" if all(o["E_pub_law"][f] for f in FOOTS) else "fail"
    return o


ELEMENTS = [("E_r1a", "E1  CFG332 1(a) class E Newton"), ("E_r1bEFE", "E2  CFG332 1(b-EFE) law + alg EFE"),
            ("E_r1bB", "E3  CFG332 1(b-B) isolated law"), ("E_r2S", "E4  CFG332 route 2 S"), ("E_r2K", "E5  CFG332 route 2 K"),
            ("E_r3", "E6  CFG332 route 3 QUMOND"), ("E_gc333_R2", "E7  CFG333 GC cell, R2 (class E)"),
            ("E_gc333_R0", "E8a CFG333 GC cell, R0"), ("E_gc333_R1", "E8b CFG333 GC cell, R1"), ("E_gc333_R3", "E8c CFG333 GC cell, R3"),
            ("E_decision333", "E9  CFG333 decision"), ("E_pub_newton", "E10a tile: published-error T, class E"),
            ("E_pub_law", "E10b published-error T, law + EFE")]


def fmt_pass(b): return "pass" if b is True else ("fail" if b is False else str(b))


def compact(ev):
    d = {}
    for f in FOOTS:
        r = ev[f]
        d[f] = {k: round(r[k]["T"], 4) for k, _ in ROUTES}
        d[f].update({f"gc333_{ru}": [round(r["gc333"][ru]["t_joint"], 4), round(r["gc333"][ru]["L"], 4), r["gc333"][ru]["labels"]] for ru in RULES})
        d[f].update(pub_newton=round(r["pub_newton"]["T"], 4), pub_law=round(r["pub_law"]["T"], 4), decision=r["decision"][0])
    d["labels332"] = ev["labels332"]; d["decision333"] = ev["decision333"][0]
    return d


def ztable(ev, title):
    P(f"  per-object signed z ({title}); clusters: {', '.join(ev['clusters'])}")
    for f in FOOTS:
        r = ev[f]
        for k, lab in ROUTES:
            P(f"   {f:9} {lab:28}: T {r[k]['T']:6.2f}  z " + "  ".join(f"{n} {z:+6.2f}" for n, z in zip(ev["clusters"], r[k]["z"])))
        for ru in RULES:
            s = r["gc333"][ru]
            P(f"   {f:9} CFG333 GC {ru} labels {'/'.join(s['labels']):19}: joint Ups {s['ups']:.3f} +- {s['eups']:.3f}  t {s['t_joint']:+6.2f}  "
              f"L {s['L']:+6.2f}  -> {'PASS' if s['passes'] else 'FAIL'}")
        P(f"   {f:9} tile (published errors): class E T {r['pub_newton']['T']:+6.2f} z " + "  ".join(f"{n} {z:+5.2f}" for n, z in zip(ev["clusters"], r["pub_newton"]["z"]))
          + f" | law+EFE T {r['pub_law']['T']:+6.2f}")
        P(f"   {f:9} CFG333 decision (this footing): {r['decision'][0]}  counts {r['decision'][1]}")
    P(f"   CFG332 frozen labels: " + ", ".join(f"{k} {v}" for k, v in ev["labels332"].items()) + f" | CFG333 decision {ev['decision333'][0]} {ev['decision333'][1]}")


R = {"mutate": MUT, "provenance": [dict(zip(("input", "cluster", "value_used", "grade", "source", "alternatives"), p)) for p in PROV]}
P("=" * 118)
P(f"CFG465 input audit of the globular verdicts (CFG332, CFG333){'   *** MUTATE: Pal 4 sigma x2 ***' if MUT else ''}")
P("=" * 118)

if not MUT:
    # ------------------------------------------------------------------------------ 1. provenance
    P("\n--- 1. INPUT PROVENANCE (grades fixed in FROZEN_CRITERIA.md) ---")
    for p in PROV:
        P(f"  {p[0]:18} {p[1]:9} | used {p[2]}\n      grade {p[3]} | source: {p[4]}\n      alternatives: {p[5]}")
    P("\n  BH2018 table2 (deepseek_push/data2/bh2018_cds_table2.dat) vs the 2023 catalogue:")
    for n in TGT:
        b, c = B18[n], C23[n]
        P(f"   {n:9} N_RV {b['NRV']:3d} -> {c['NRV']:3d} | D {b['D']:6.2f}{b['Dnote']} -> {c['D']:6.2f} | L_V(BH18) = M/(M/L) {b['M']/b['ML']:.3e} at D18 "
          f"| rmlp {b['rmlp']:5.2f} -> r_h,l {c['rhl']:5.2f} | MF {b['alpha']:+.2f}{b['MFnote']} -> {MF[n]['alpha']:+.2f} | model sigma0 {b['sig0']:.1f} -> {c['sig0']:.1f}")
    P("\n  the two catalogue luminosities at a common distance (BH2018's D): L_V(BH18) / L_V(2023 V)")
    LRAT = {}
    for n in TGT:
        b, c = B18[n], C23[n]
        MV = c["V"] - 3.1 * EBV[n] - 5 * math.log10(b["D"] * 1e3 / 10.0); L23 = 10 ** (0.4 * (MSUN_V - MV)); L18 = b["M"] / b["ML"]
        LRAT[n] = L18 / L23
        P(f"   {n:9} {L18:.3e} / {L23:.3e} = {L18 / L23:.3f}  ({math.log10(L18 / L23):+.3f} dex, {-2.5 * math.log10(L18 / L23):+.2f} mag)")
    gG = {g["name"]: g for g in build(dict(BASE, n2419="global"))}
    P(f"  NGC 2419 light-weighted global sigma {gG['NGC 2419']['so']:.3f} +- {gG['NGC 2419']['eso']:.3f} (N {gG['NGC 2419']['N']}) vs at r_h 4.771 (N 62)")
    R["luminosity_ratio_BH18_over_2023"] = LRAT; R["ngc2419_global"] = dict(so=gG["NGC 2419"]["so"], eso=gG["NGC 2419"]["eso"], N=gG["NGC 2419"]["N"])
    # ------------------------------------------------------------------------------ controls C4-C6
    P("\n--- 2. DATA CONTROLS ---")
    nrv_ok = [B18[n]["NRV"] for n in TGT] == [195, 14, 23, 17] and [B18[n]["D"] for n in TGT] == [83.20, 92.50, 103.00, 71.00]
    worst = 0.0
    for n in TGT:
        c, f = C23[n], COMBROW[n]
        for a, bb in ((float(f[3]), c["D"]), (float(f[5]), c["RGC"]), (int(f[7]), c["NRV"]), (float(f[9]), c["M"]), (float(f[11]), c["V"]),
                      (float(f[13]), c["ML"]), (float(f[16]), c["rhl"]), (BHV[n][0], c["M"]), (BHV[n][1], c["rhl"]), (BHV[n][2], c["sig0"])):
            worst = max(worst, abs(a - bb) / abs(bb))
    check("C4 BH2018 table2 parses to N_RV 195/14/23/17 and D 83.20/92.50/103.00/71.00; the three 2023 copies agree (< 1e-6)",
          nrv_ok and worst < 1e-6, f"N_RV {[B18[n]['NRV'] for n in TGT]}, D {[B18[n]['D'] for n in TGT]}, worst copy diff {worst:.1e}")
    dev = max(abs(rgc_geom(n, C23[n]["D"]) / C23[n]["RGC"] - 1) for n in TGT)
    check("C5 R0 = 8.178 kpc reproduces the 2023 R_GC at the 2023 D (< 1e-3)", dev < 1e-3, f"max rel dev {dev:.1e}; "
          + ", ".join(f"{n} R_GC(D18) {rgc_geom(n, B18[n]['D']):.2f}" for n in TGT))
    c6 = ups_mf(-2.3, "K")
    check("C6 route-2 Kroupa input (alpha -2.3, branch K) returns Ups_MF = 1.6 (1e-6)", abs(c6 - 1.6) < 1e-6, f"{c6:.9f}")
    R["data_controls"] = dict(bh18={n: B18[n] for n in TGT}, worst_copy_diff=worst, rgc_dev=dev,
                              rgc_at_D18={n: rgc_geom(n, B18[n]["D"]) for n in TGT})

    # ------------------------------------------------------------------------------ 3. BASE reproduction
    P("\n--- 3. BASE (committed inputs) -- reproduction of CFG332 / CFG333 / AUDIT ---")
    gB = build(BASE)
    for g in gB:
        P(f"  {g['name']:9} sigma {g['so']:.3f} (+{g['up']:.3f}/-{g['lo']:.3f}) N {g['N']:3d}  L_V {g['LV']:.3e}  r_h {g['rhl']:.2f}  R_GC {g['RGC']:.2f}  "
          f"g_ext {g['gext']:.3e}  MF {g['alpha']:+.2f}")
    evB = evaluate(gB); ztable(evB, "BASE")
    mapJ = {"r1a": "route1_a_owned", "r1bEFE": "route1_b_EFE_h93", "r1bB": "route1_b_B_isolated", "r2S": "route2_S", "r2K": "route2_K", "r3": "route3_qumond"}
    d1 = max(abs(evB[f][k]["T"] - J332["verdicts"][mapJ[k]][f"T_{f}"]) for f in FOOTS for k in mapJ)
    lab_ok = all(evB["labels332"][k] == J332["verdicts"][mapJ[k]]["verdict"] for k in mapJ)
    evNP3 = evaluate(build(dict(BASE, p3="drop")), full=False); evPUB = evaluate(build(dict(BASE, p4="frank", p14="jordi")), full=False)
    jk = {"r1a": "a_newton", "r1bEFE": "b_EFE_h93"}
    d1b = max(max(abs(evNP3[f][k]["T"] - J332["route1"][f][jk[k]]["noPal3_T"]), abs(evPUB[f][k]["T"] - J332["route1"][f][jk[k]]["published_T"]))
              for f in FOOTS for k in jk)
    check("C1 BASE reproduces CFG332's six route T (both footings, +-0.01) and frozen labels; no-Pal-3 and published-alt cells for 1(a), 1(b-EFE)",
          d1 <= 0.01 and lab_ok and d1b <= 0.01, f"max |dT| {d1:.4f}; labels {'same' if lab_ok else 'DIFFER'}; no-Pal-3 / published cells max |dT| {d1b:.4f}")
    d2 = max(max(abs(evB[f]["gc333"][ru]["t_joint"] - J333["rules"][ru]["res"][f"GC|{f}"]["t_joint"]),
                 abs(evB[f]["gc333"][ru]["L"] - J333["rules"][ru]["res"][f"GC|{f}"]["L"])) for f in FOOTS for ru in RULES)
    dec_ok = evB["decision333"][0] == "PARTIAL" and evB["decision333"][1]["R2"] == J333["rules"]["R2"]["n_pass"]
    check("C2 BASE reproduces CFG333's GC cells R0-R3 (t_joint, L; +-0.01) and its PARTIAL decision", d2 <= 0.01 and dec_ok,
          f"max diff {d2:.4f}; decision {evB['decision333'][0]} {evB['decision333'][1]}")
    d3 = max(max(abs(evB[f]["pub_newton"]["T"] - JAUD["tension"][f]["Newton (class E)"]["T4"]),
                 abs(evB[f]["pub_law"]["T"] - JAUD["tension"][f]["law + alg EFE (h93)"]["T4"])) for f in FOOTS)
    check("C3 BASE reproduces AUDIT's published-error T: 1.58 (class E), 3.22 / 3.54 (law + EFE) (+-0.01)", d3 <= 0.01,
          f"class E {evB['canonical']['pub_newton']['T']:.2f}/{evB['alt']['pub_newton']['T']:.2f}, law {evB['canonical']['pub_law']['T']:.2f}/"
          f"{evB['alt']['pub_law']['T']:.2f}; max diff {d3:.4f}")
    R["base"] = compact(evB); R["base_perobject"] = {f: {k: evB[f][k]["z"] for k, _ in ROUTES} for f in FOOTS}

    # ------------------------------------------------------------------------------ 4. (a) SOURCED-ONLY and (a') PAPER-VERIFIED
    P("\n--- 4. (a) SOURCED-ONLY (grades A+B): Pal 3 dropped; Pal 4 Frank+12; Pal 14 Jordi+09; NGC 2419 catalogue at r_h ---")
    gS = build(SOURCED); nS = len(gS)
    P(f"  clusters retained: {nS} of 4 -> {'SUPPORTED (>= 3)' if nS >= 3 else 'UNSUPPORTED (< 3)'}")
    evS = evaluate(gS); ztable(evS, "(a) SOURCED-ONLY")
    R["sourced"] = compact(evS); R["sourced_perobject"] = {f: {k: evS[f][k]["z"] for k, _ in ROUTES} for f in FOOTS}; R["sourced_n"] = nS
    P("\n--- 4'. (a') PAPER-VERIFIED (grade A only: Pal 4 Frank+12, Pal 14 Jordi+09) -- REPORTED, 2 clusters < 3 => UNSUPPORTED at this level ---")
    gPV = build(PAPER); evPV = evaluate(gPV, full=False); ztable(evPV, "(a') PAPER-VERIFIED")
    R["paper_verified"] = compact(evPV); R["paper_verified_n"] = len(gPV)

    # ------------------------------------------------------------------------------ 5. one-at-a-time swaps
    P("\n--- 5. ONE-AT-A-TIME SWAPS from BASE (attribution; T canonical/alt; CFG333 R2 GC cell t, L) ---")
    SW = {}
    swaps = [("n2419", "global"), ("p3", "drop"), ("p4", "frank"), ("p14", "jordi"), ("D", "18"), ("L", "18"), ("R", "18"),
             ("MW", MW_ALTS[0]), ("MW", MW_ALTS[1]), ("MF", "18")]
    P(f"  {'swap':16} " + " ".join(f"{k:>13}" for k, _ in ROUTES) + f" {'R2 GC t;L':>16} {'tile E':>9} {'333':>8}")
    for k, v in [("BASE", None)] + swaps:
        ch = BASE if v is None else dict(BASE, **{k: v})
        ev = evB if v is None else evaluate(build(ch), full=False)
        lab = "BASE" if v is None else f"{k}={v:.1e}" if k == "MW" else f"{k}={v}"
        SW[lab] = compact(ev)
        P(f"  {lab:16} " + " ".join(f"{ev['canonical'][r]['T']:6.2f}/{ev['alt'][r]['T']:5.2f}" for r, _ in ROUTES)
          + f" {ev['canonical']['gc333']['R2']['t_joint']:+5.2f};{ev['canonical']['gc333']['R2']['L']:+5.2f}"
          + f" {ev['canonical']['pub_newton']['T']:+8.2f} {ev['decision333'][0]:>8}")
    R["swaps"] = SW

    # ------------------------------------------------------------------------------ 6. factorial
    P("\n--- 6. (b) FULL FACTORIAL over the record's alternatives ---")
    combos = list(itertools.product(*[vals for _, vals in FACTORS]))
    P(f"  {len(combos)} variants ({' x '.join(str(len(v)) for _, v in FACTORS)})")
    FACT = {}; OUTC = {}
    for i, combo in enumerate(combos):
        ch = dict(zip([k for k, _ in FACTORS], combo)); key = vkey(ch)
        ev = evaluate(build(ch), full=False); FACT[key] = compact(ev); OUTC[key] = (ch, outcomes(ev))
        if (i + 1) % 128 == 0: print(f"    ... {i + 1}/{len(combos)}", flush=True)
    R["factorial"] = FACT
    oB, oS = outcomes(evB), outcomes(evS)
    CLASS = {}
    P(f"\n  {'element':40} {'BASE (canon / alt / label)':34} {'(a) sourced':30} flips/N (canon, alt, label)  class")
    for ek, elab in ELEMENTS:
        cls = {}; detail = {}
        for slot in FOOTS + ["label"]:
            base_v = oB[ek][slot]
            flips = [key for key, (ch, o) in OUTC.items() if o[ek][slot] != base_v]
            sflip = oS[ek][slot] != base_v
            cond = {}
            for fk, vals in FACTORS:
                for v in vals:
                    sub = [key for key, (ch, o) in OUTC.items() if ch[fk] == v]
                    cond[f"{fk}={v:.1e}" if fk == "MW" else f"{fk}={v}"] = round(sum(1 for key in sub if OUTC[key][1][ek][slot] != base_v) / len(sub), 3)
            cls[slot] = "FRAGILE" if (flips or sflip) else "ROBUST"
            detail[slot] = dict(base=base_v, sourced=oS[ek][slot], n_flip=len(flips), n=len(OUTC), cond_flip_rate=cond)
        CLASS[ek] = dict(classes=cls, detail=detail)
        P(f"  {elab:40} {fmt_pass(oB[ek]['canonical']):>6} / {fmt_pass(oB[ek]['alt']):>6} / {str(oB[ek]['label']):14} "
          f"{fmt_pass(oS[ek]['canonical']):>6} / {fmt_pass(oS[ek]['alt']):>6} / {str(oS[ek]['label']):14} "
          f"{detail['canonical']['n_flip']:3d}, {detail['alt']['n_flip']:3d}, {detail['label']['n_flip']:3d} /{len(OUTC)}  "
          f"{cls['canonical']}/{cls['alt']}/{cls['label']}")
    R["classes"] = CLASS

    # attribution: which factor levels drive flips (conditional flip rates; label slot)
    P("\n  conditional flip rate of the combined label, by factor level (fraction of the variants at that level whose label differs from BASE):")
    lvl = [f"{fk}={v:.1e}" if fk == "MW" else f"{fk}={v}" for fk, vals in FACTORS for v in vals]
    P("  " + f"{'element':40}" + " ".join(f"{x:>11}" for x in lvl))
    for ek, elab in ELEMENTS:
        cr = CLASS[ek]["detail"]["label"]["cond_flip_rate"]
        P("  " + f"{elab:40}" + " ".join(f"{cr[x]:11.2f}" for x in lvl))

    # margins: extreme statistic over the factorial (how close to the 2-sigma line each element gets)
    P("\n  margins: range of each statistic over all variants (BASE value; min .. max), per footing")
    MARG = {}
    for f in FOOTS:
        for k, lab in [(r, l) for r, l in ROUTES] + [("pub_newton", "tile: published-error class E"), ("pub_law", "published-error law + EFE")]:
            v = [FACT[x][f][k] for x in FACT]
            MARG[f"{f}|{k}"] = (min(v), max(v)); P(f"   {f:9} {lab:32} T: BASE {FACT[vkey(BASE)][f][k]:+6.3f}; range {min(v):+6.3f} .. {max(v):+6.3f}")
        for ru in RULES:
            t = [FACT[x][f][f"gc333_{ru}"][0] for x in FACT]; L_ = [FACT[x][f][f"gc333_{ru}"][1] for x in FACT]
            MARG[f"{f}|gc333_{ru}"] = dict(t=(min(t), max(t)), L=(min(L_), max(L_)))
            P(f"   {f:9} CFG333 GC {ru:28} t range {min(t):+6.2f} .. {max(t):+6.2f}; L range {min(L_):+6.2f} .. {max(L_):+6.2f}")
    R["margins"] = MARG
    P("\n  fragile elements with Pal 3 KEPT (p3=cat): label flips and conditional flip rates by level")
    for ek, elab in ELEMENTS:
        if CLASS[ek]["classes"]["label"] != "FRAGILE": continue
        base_v = oB[ek]["label"]; kept = [x for x, (ch, o) in OUTC.items() if ch["p3"] == "cat"]
        fl = [x for x in kept if OUTC[x][1][ek]["label"] != base_v]
        rates = {}
        for fk, vals in FACTORS:
            if fk == "p3": continue
            for v in vals:
                sub = [x for x in kept if OUTC[x][0][fk] == v]
                rates[f"{fk}={v:.1e}" if fk == "MW" else f"{fk}={v}"] = round(sum(1 for x in sub if x in fl) / len(sub), 3)
        CLASS[ek]["pal3_kept"] = dict(n_flip=len(fl), n=len(kept), cond_flip_rate=rates)
        P(f"   {elab:40} {len(fl)}/{len(kept)}: " + ", ".join(f"{a} {b:.2f}" for a, b in rates.items()))

    # ------------------------------------------------------------------------------ 7. Upsilon-centre sensitivity (reported)
    P("\n--- 7. Upsilon_V prior centre (assumption) -- REPORTED, not scored: class E only ---")
    UPS_SENS = {}
    for lab, ch in (("BASE", BASE), ("SOURCED", SOURCED)):
        g = build(ch)
        for uc in (1.3, 1.6, 2.2):
            cc = {x["name"]: uc for x in g}; ww = {x["name"]: WID for x in g}
            t = score(pred_newton, A0["canonical"], g, cc, ww)["T"]
            pn = pub_stat(g, A0["canonical"], "newton", ups=uc)["T"]
            L333 = gc_stat333(g, A0["canonical"], ["own"] * len(g), ups_draws=uc * 10 ** (WID * Z))["L"]
            UPS_SENS[f"{lab}|{uc}"] = dict(T_cfg332=t, T_pub=pn, L_cfg333=L333)
            P(f"  {lab:8} Ups centre {uc:.1f}: CFG332 1(a) T {t:+6.2f} | published-error T {pn:+6.2f} | CFG333 Newton L {L333:+6.2f}")
    R["ups_sensitivity"] = UPS_SENS

    # ------------------------------------------------------------------------------ 8. verdict
    tile_keys = ["E_r1a", "E_gc333_R2", "E_decision333"]
    unsupported = nS < 3
    tile_class = "UNSUPPORTED" if unsupported else ("ROBUST" if all(all(v == "ROBUST" for v in CLASS[k]["classes"].values()) for k in tile_keys) else "FRAGILE")
    law_keys = ["E_r1bEFE", "E_r1bB", "E_r3"]
    law_class = "ROBUST" if all(all(v == "ROBUST" for v in CLASS[k]["classes"].values()) for k in law_keys) else "FRAGILE"
    R["verdict"] = dict(tile=tile_class, tile_elements={k: CLASS[k]["classes"] for k in tile_keys},
                        law_side=law_class, law_elements={k: CLASS[k]["classes"] for k in law_keys},
                        sourced_n=nS, paper_verified_n=len(gPV))
    P("\n--- 8. VERDICT ---")
    for ek, elab in ELEMENTS:
        c = CLASS[ek]["classes"]; d = CLASS[ek]["detail"]
        P(f"  {elab:40} canonical {c['canonical']:8} alt {c['alt']:8} label {c['label']:8}  (BASE {d['label']['base']} -> sourced {d['label']['sourced']}; "
          f"label flips in {d['label']['n_flip']}/{d['label']['n']} variants)")
    P(f"\n  TILE 'Globulars + ownership rule' (E1, E7, E9): {tile_class}   | sourced-only retains {nS}/4 clusters; paper-verified level {len(gPV)}/4 => UNSUPPORTED there")
    P(f"  LAW SIDE (globulars under the law: E2, E3, E6): {law_class}")
else:
    # ------------------------------------------------------------------------------ MUTATE: Pal 4 sigma x2 in BASE
    gB = build(BASE); gM = build(BASE, mutate_pal4=True)
    evB = evaluate(gB); evM = evaluate(gM)
    ztable(evM, "MUTATE: BASE with Pal 4 sigma x2")
    i4 = [g["name"] for g in gB].index("Pal 4")
    rows_ = []
    for f in FOOTS:
        for k, lab in ROUTES:
            rows_.append((f, lab, evB[f][k]["z"], evM[f][k]["z"]))
        for md in ("own", "top"):
            rows_.append((f, f"CFG333 mode {md}", evB[f]["gc333_modes"][md]["z"], evM[f]["gc333_modes"][md]["z"]))
    cls = lambda z: "consistent" if abs(z) < 2 else ("high" if z > 0 else "low")
    P("\n  Pal 4 per-object z, BASE -> MUTATE:")
    moved, flipped, others = [], [], []
    for f, lab, zb, zm in rows_:
        moved.append(abs(zm[i4] - zb[i4])); flipped.append(cls(zm[i4]) != cls(zb[i4]))
        others.append(max(abs(zm[j] - zb[j]) for j in range(len(zb)) if j != i4))
        P(f"   {f:9} {lab:28}: {zb[i4]:+6.2f} ({cls(zb[i4])}) -> {zm[i4]:+6.2f} ({cls(zm[i4])});  other clusters max |dz| {others[-1]:.1e}")
    check("MUTATE Pal 4's per-object z moves by >= 1 in every route (CFG332 six + CFG333 own/top, both footings)", min(moved) >= 1, f"min |dz| {min(moved):.2f}")
    check("MUTATE Pal 4's per-object class flips in >= 1 route", any(flipped), f"{sum(flipped)}/{len(flipped)} route-footings flip")
    check("MUTATE the other three clusters' per-object z are unchanged (< 1e-9)", max(others) < 1e-9, f"max {max(others):.1e}")
    oB, oM = outcomes(evB), outcomes(evM)
    P("\n  element outcomes BASE -> MUTATE (informational):")
    for ek, elab in ELEMENTS:
        P(f"   {elab:40} {fmt_pass(oB[ek]['canonical'])}/{fmt_pass(oB[ek]['alt'])}/{oB[ek]['label']} -> "
          f"{fmt_pass(oM[ek]['canonical'])}/{fmt_pass(oM[ek]['alt'])}/{oM[ek]['label']}")
    R["mutate_rows"] = [dict(foot=f, route=lab, z_base=zb, z_mut=zm) for f, lab, zb, zm in rows_]
    R["mutate_base"] = compact(evB); R["mutate"] = compact(evM)

R["checks"] = CHECKS
npass = sum(ok for _, ok in CHECKS)
P(f"\n{npass}/{len(CHECKS)} checks pass")
open(os.path.join(HERE, f"cfg465_globular_inputs{TAG}.out"), "w").write("\n".join(LOG) + "\n")
json.dump(R, open(os.path.join(HERE, f"cfg465_globular_inputs{TAG}_results.json"), "w"), separators=(",", ":"), default=lambda o: o.item() if hasattr(o, "item") else str(o))
