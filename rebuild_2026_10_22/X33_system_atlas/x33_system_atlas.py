#!/usr/bin/env python3
"""X33_system_atlas: one per-object atlas of every system the record measured against the galaxy law, and a descriptive
correlation analysis of where the law is right and what the misfits share.  Criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md
(committed alone first).

Run:   PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x33_system_atlas.py            -> x33_atlas.csv, x33_findings.json, .out
       X33_MUTATE=1 ... python3 x33_system_atlas.py                                          -> *_MUTATE.json / .out (K_ident, K_plant must FAIL)
kappa = 1/2 FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled. No dark-matter particle. Not "theory closed".
Inputs are read only; nothing is downloaded.
"""
import os, sys
if os.environ.get("MallocMediumZone") != "0":
    os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "MallocMediumZone": "0"})
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import csv, glob, json, math, re, resource, time
import numpy as np
from scipy.stats import spearmanr, mannwhitneyu, rankdata
from astropy.io import fits

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
RB = os.path.dirname(HERE)
REPO = os.path.dirname(RB)
EXT = os.path.join(os.path.dirname(REPO), "_external_data")
DATA = os.path.join(REPO, "real_research", "data")
CFGD = os.path.join(REPO, "campaign_fresh_gravity")
MUT = os.environ.get("X33_MUTATE", "") == "1"
TAG = "_MUTATE" if MUT else ""
FOOTS = ("canonical", "alt")
FK = {"canonical": "can", "alt": "alt"}
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19; PC = KPC / 1e3; MPC = KPC * 1e3
KEV = 1.602176634e-16; MP = 1.67262192e-27; MU = 0.6
LN10 = math.log(10.0)
NBOOT = 1000; SEED = 33033
OUTL = []
CHECKS = {}


def P(s=""):
    s = str(s).replace(REPO, "<repo>"); OUTL.append(s); print(s, flush=True)


def check(name, ok, value, line):
    CHECKS[name] = dict(ok=bool(ok), value=str(value), line=line)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value} (line: {line})")


def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9


def nu1(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def law(gN, a0):
    return 0.5 * (gN + np.sqrt(gN * gN + 4 * gN * a0))


def law_inv(g, a0):
    return g * g / (g + a0)


def jl(p):
    return json.load(open(os.path.join(RB, p)))


NAN = float("nan")
P("X33_system_atlas  " + ("MUTATE (residuals permuted within class)" if MUT else "normal run"))
P(f"kappa = 1/2 FITTED; footings canonical {A0['canonical']:.4e} / alt {A0['alt']:.4e}, never pooled; descriptive lane")

P4 = jl("P4_v3_galaxy_tiles/p4_v3_galaxy_tiles_results.json")["tiles"]
CFG695 = json.load(open(os.path.join(CFGD, "CFG695_saturating_vacuum", "cfg695_results.json")))["numbers"]["S2"]
U0 = {f: float(CFG695[f]["U"]) for f in FOOTS}
ROWS = []          # the atlas
S0 = {}            # step-0 numbers


def newrow(**kw):
    r = dict(id="", cls="", subclass="", morphology_T=NAN, M_b=NAN, M_star=NAN, M_gas=NAN, f_gas=NAN, R_char_kpc=NAN, R_last_kpc=NAN,
             Sigma0=NAN, V_char_kms=NAN, sigma_kms=NAN, x_char=NAN, e_ext=NAN, hosted=NAN, z=NAN,
             resid_dex_can=NAN, resid_err_can=NAN, resid_dex_alt=NAN, resid_err_alt=NAN, quality="", source="",
             morph_label="", Sigma_half=NAN, D_Mpc=NAN, inc_deg=NAN, L36=NAN, M_HI=NAN, R_eff_kpc=NAN, R_disk_kpc=NAN, V_flat_kms=NAN, Q=NAN,
             Ups_fit_can=NAN, Ups_fit_alt=NAN, resid_perU_med_can=NAN, resid_perU_med_alt=NAN, rms_curve_can=NAN, rms_curve_alt=NAN,
             resid_wmean_can=NAN, resid_wmean_alt=NAN, resid_efe_can=NAN, resid_efe_alt=NAN, KT_keV=NAN, MGAS500=NAN, L500=NAN, R500_kpc=NAN,
             uma_member=NAN, in_pool="", A_can=NAN, A_alt=NAN)
    r.update(kw)
    if np.isfinite(r["M_b"]) and np.isfinite(r["R_char_kpc"]) and r["R_char_kpc"] > 0 and not np.isfinite(r["Sigma_half"]):
        r["Sigma_half"] = r["M_b"] / (2 * math.pi * (r["R_char_kpc"] * 1e3) ** 2)
    return r


# =====================================================================================================  SPARC
P("\n=== BUILD: SPARC (record loader; global Upsilon from CFG695; per-galaxy Upsilon from P4 L* 24 pc)")
KEYS = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q")
TAB = {}
for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
    tok = line.split()
    if len(tok) != 19:
        continue
    try:
        vals = [float(t) for t in tok[1:18]]
    except ValueError:
        continue
    TAB[tok[0]] = dict(zip(KEYS, vals))
GALS = []
for fn in sorted(os.listdir(os.path.join(DATA, "sparc_data"))):
    if not fn.endswith("_rotmod.dat"):
        continue
    try:
        d = np.genfromtxt(os.path.join(DATA, "sparc_data", fn), comments="#")
    except Exception:
        continue
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    GALS.append(dict(name=fn.replace("_rotmod.dat", ""), R=d[:, 0], Vobs=d[:, 1], eV=d[:, 2], Vgas=d[:, 3], Vdisk=d[:, 4], Vbul=d[:, 5],
                     meta=TAB.get(fn.replace("_rotmod.dat", ""))))
MASTER = {r["name"]: r for r in csv.DictReader(open(os.path.join(DATA, "sparc_master_clean.csv")))}
ENV = {r["galaxy"].strip(): r for r in csv.DictReader(open(os.path.join(REPO, "real_research", "reviews", "directional_efe_2026", "laneB_data", "chae21_env.csv")))}
KPC_S = 3.0857e19
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)


def gal_pts(q, ups, a0):
    """per-point log residual vs isolated algebraic law at Upsilon ups (scalar); weights; sig (dex); mask."""
    R = q["R"] * KPC_S
    vb2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + ups * q["Vdisk"] ** 2 + 1.4 * ups * q["Vbul"] ** 2
    gb = vb2 * 1e6 / R; go = (q["Vobs"] * 1e3) ** 2 / R
    ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (q["Vobs"] > 0)
    gbs = np.where(ok, gb, 1.0)
    r = np.where(ok, np.log10(np.where(ok, go, 1.0)) - np.log10(nu1(gbs / a0) * gbs), NAN)
    W = 1.0 / (np.clip(q["eV"], 1, None) / np.clip(q["Vobs"], 1, None)) ** 2
    sig = 2 * np.clip(q["eV"], 1, None) / (np.clip(q["Vobs"], 1, None) * LN10)
    return r, W, sig, ok, gb


PERU = {f: {x["name"]: x for x in P4["T1"]["footings"][f]["L24"]["per_galaxy"]} for f in FOOTS}
iso_rep = {}
for f in FOOTS:
    a0 = A0[f]; num = den = 0.0
    for q in GALS:
        mse = []; parts = []
        for u in UPS:
            r, W, sig, ok, gb = gal_pts(q, u, a0)
            Wm = np.where(ok, W, 0.0); rr = np.where(ok, r, 0.0)
            mse.append((Wm * rr * rr).sum() / max(Wm.sum(), 1e-300)); parts.append(((Wm * rr * rr).sum(), Wm.sum()))
        i = int(np.argmin(mse)); num += parts[i][0]; den += parts[i][1]
    iso_rep[f] = math.sqrt(num / den)
S0["S0a"] = {f: dict(mine=iso_rep[f], P4_iso=P4["T1"]["footings"][f]["iso_perUps"]["rms"], P4_L24=P4["T1"]["footings"][f]["L24"]["rms"]) for f in FOOTS}

uma_set = {nm for nm, r in MASTER.items() if r["fD"] == "4"}
cls_means = {f: {"small": [], "large": []} for f in FOOTS}
for q in GALS:
    m = q["meta"]; nm = q["name"]
    U = U0["canonical"]
    Mst = U * m["L36"] * 1e9; Mg = 1.33 * m["MHI"] * 1e9; Mb = Mst + Mg
    row = newrow(id=nm, cls="SPARC", morphology_T=m["T"], M_b=Mb, M_star=Mst, M_gas=Mg, f_gas=Mg / Mb if Mb > 0 else NAN,
                 R_char_kpc=m["Reff"] if m["Reff"] > 0 else NAN, R_last_kpc=float(q["R"][-1]), Sigma0=U * m["SBdisk"] if m["SBdisk"] > 0 else NAN,
                 V_char_kms=m["Vflat"] if m["Vflat"] > 0 else NAN, D_Mpc=m["D"], inc_deg=m["Inc"], L36=m["L36"] * 1e9, M_HI=m["MHI"] * 1e9,
                 R_eff_kpc=m["Reff"], R_disk_kpc=m["Rdisk"], V_flat_kms=m["Vflat"] if m["Vflat"] > 0 else NAN, Q=m["Q"],
                 uma_member=1.0 if nm in uma_set else 0.0, hosted=1.0 if nm in uma_set else 0.0, morph_label=f"disc T={int(m['T'])}",
                 quality=f"Q={int(m['Q'])}", in_pool="P_gal",
                 source="SPARC rotmod + Lelli2016c.mrt; Upsilon CFG695 S2 (global) / P4 T1 L24 per_galaxy")
    if nm in ENV:
        lne = 0.5 * (float(ENV[nm]["log_eN_maxclu"]) + float(ENV[nm]["log_eN_noclu"]))
        row["e_ext"] = float(law(10 ** lne * 1.2e-10, A0["canonical"])) / A0["canonical"]
    inc = math.radians(m["Inc"]); einc = math.radians(m["eInc"])
    s2 = (m["eD"] / (m["D"] * LN10)) ** 2 + (2 * einc / math.tan(inc) / LN10) ** 2
    for f in FOOTS:
        a0 = A0[f]; k = FK[f]
        r, W, sig, ok, gb = gal_pts(q, U0[f], a0)
        if ok.any():
            row[f"resid_dex_{k}"] = float(np.median(r[ok]))
            row[f"resid_err_{k}"] = float(math.sqrt(1.0 / np.sum(1.0 / sig[ok] ** 2) + s2))
            row[f"resid_wmean_{k}"] = float(np.sum(W[ok] * r[ok]) / np.sum(W[ok]))
            Mb_f = 1.33 * m["MHI"] * 1e9 + U0[f] * m["L36"] * 1e9
            cls_means[f]["small" if Mb_f <= 3e9 else "large"].append(row[f"resid_wmean_{k}"])
            if f == "canonical":
                i = np.nonzero(ok)[0][-1]
                row["x_char"] = float(gb[i] / A0["canonical"])
                row["subclass"] = "small" if Mb_f <= 3e9 else "large"
        pu = PERU[f].get(nm)
        if pu is not None:
            row[f"Ups_fit_{k}"] = pu["U_rms"]
            r2, W2, _, ok2, _ = gal_pts(q, pu["U_rms"], a0)
            if ok2.any():
                row[f"resid_perU_med_{k}"] = float(np.median(r2[ok2]))
                row[f"rms_curve_{k}"] = float(math.sqrt(np.sum(W2[ok2] * r2[ok2] ** 2) / np.sum(W2[ok2])))
    ROWS.append(row)
S0["S0b"] = {f: {c: dict(N=len(v), mine=float(np.mean(v)), P4=P4["T1"]["footings"][f]["classes_global_U"][c]["mean"],
                         P4_N=P4["T1"]["footings"][f]["classes_global_U"][c]["N"]) for c, v in cls_means[f].items()} for f in FOOTS}
P(f"  SPARC rows {sum(1 for r in ROWS if r['cls'] == 'SPARC')}; UMa members {int(sum(r['uma_member'] for r in ROWS if r['cls'] == 'SPARC'))}; global U0 {U0}")

# =====================================================================================================  MW disc
for f in FOOTS:
    pass
K = {f: P4["T4"]["models"]["B1_McMillan17"][f]["F0|L24"]["K_R0"] for f in FOOTS}
vc = P4["T4"]["models"]["B1_McMillan17"]["canonical"]["F0|L24"]["vc_R0"] * 1e3
R0 = 8.122 * KPC
gN_mw = float(law_inv(vc ** 2 / R0, A0["canonical"]))
geN = G * 1e11 * MSUN / (785 * KPC) ** 2
ROWS.append(newrow(id="Milky Way", cls="MW disc", subclass="MW disc", morphology_T=4.0, M_b=6.6461135288785715e10, R_char_kpc=8.122, R_last_kpc=8.122,
                   V_char_kms=229.1, x_char=gN_mw / A0["canonical"], e_ext=float(law(geN, A0["canonical"])) / A0["canonical"], hosted=0.0,
                   resid_dex_can=math.log10(66.4 / K["canonical"]), resid_err_can=2.2 / (66.4 * LN10),
                   resid_dex_alt=math.log10(66.4 / K["alt"]), resid_err_alt=2.2 / (66.4 * LN10), morph_label="MW disc (K_z at R0)",
                   quality="APPROX axis: vertical force K_z,1.1", in_pool="", source="P4 T4 B1_McMillan17 F0|L24 K_R0 vs 66.4+-2.2"))

# =====================================================================================================  Groups (Tian+26; P4's estimator)
P("=== BUILD: groups (Tian+26 BFJR; P4's group_logsig with nu1)")
P4SRC = open(os.path.join(RB, "P4_v3_galaxy_tiles", "p4_v3_galaxy_tiles.py")).read()
i0 = P4SRC.index("G540, MSUN540, KPC540 = "); i1 = P4SRC.index("def class_stats(d, s):")
NSG = {"np": np, "math": math}
exec(P4SRC[i0:i1], NSG)
groups = []
for l in open(os.path.join(EXT, "vizier2026", "J_A_A_710_L39.tsv")):
    if l.startswith("#"):
        continue
    r = l.rstrip("\n").split("\t")
    if len(r) < 13 or not r[0].strip().isdigit() or r[1].strip() != "Galaxy group":
        continue
    groups.append(dict(id=r[2].strip(), ls=float(r[5]), els=float(r[6]), lM=float(r[7]), elM=float(r[8]), lgb=float(r[9]), Re=float(r[10])))
gd = {f: [] for f in FOOTS}
for o in groups:
    row = newrow(id=o["id"], cls="Groups", subclass="group", M_b=10 ** o["lM"], R_char_kpc=o["Re"], R_last_kpc=o["Re"], sigma_kms=10 ** o["ls"],
                 V_char_kms=math.sqrt(3) * 10 ** o["ls"], x_char=10 ** o["lgb"] / A0["canonical"], hosted=0.0, morph_label="galaxy group",
                 quality="APPROX axis: 2 x dlog sigma", in_pool="P_gal", source="Tian+26 J/A+A/710/L39; P4 group_logsig (nu1, Hernquist, whole system)")
    for f in FOOTS:
        dl = o["ls"] - NSG["group_logsig"](o, A0[f], nu1)
        gd[f].append(dl)
        row[f"resid_dex_{FK[f]}"] = 2 * dl; row[f"resid_err_{FK[f]}"] = 2 * o["els"]
    ROWS.append(row)
S0["S0e"] = {f: dict(N=len(gd[f]), mine=float(np.mean(gd[f])), P4=P4["T3"]["footings"][f]["v3_isolated"]["mean"]) for f in FOOTS}

# =====================================================================================================  Clusters (X21 machinery, read-only)
P("=== BUILD: clusters (X7 per-cluster arrays; X2's model exec'd read-only exactly as X21; C* MID band, CAL, h0672)")
LANES = CFGD
X2DIR = os.path.join(RB, "X2_cluster_outskirts"); TX = open(os.path.join(X2DIR, "x2_cluster_outskirts.py")).read()


def cutx(a, b):
    i = TX.index(a); j = TX.index(b, i); return TX[i:j]


NS2 = {"np": np, "os": os, "sys": sys, "math": math, "json": json, "time": time, "REB": RB, "REPO": REPO, "HERE": X2DIR,
       "LANES": LANES, "MUT": False, "RES": {}, "say": (lambda *a: None), "check": (lambda *a: None),
       "sha": (lambda p: ""), "rss": rss_gb, "guard": (lambda tag: None)}
exec(cutx("# ============================================================== F1's own functions", "# ============================================================== data: the replay"), NS2)
exec(cutx("# ============================================================== data: the replay", "# ============================================================== statistics"), NS2)
exec(cutx("# ============================================================== statistics", "# ============================================================== EFE"), NS2)
exec(cutx('sys.path.insert(0, os.path.join(REB, "F2_outer_lensing"))', 'for f in FEET:\n    for k in ("noclu", "maxclu", "p2cat"):'), NS2)
exec(cutx("# ============================================================== the model", "# ============================================================== K2, K3, K7"), NS2)
for f in FOOTS:
    NS2["CTAB"][(f, "noclu")] = NS2["ctable"](NS2["AQ"].solve_efe(NS2["YE"][f]["noclu"], maxit=3000))
MY = np.load(os.path.join(RB, "X7_cluster_core_significance", "x7_measure_percluster.npz"))
NCL = len(MY["name"])
HI_ = {"h0672": 1, "h0686": 2}; HXI = {"h0672": 0, "h0686": 1}
DAT = {}
for hk in ("h0672", "h0686"):
    i = HI_[hk]; W = np.where(MY["E"][:, i] < 1e8, 1 / MY["E"][:, i] ** 2, 0); B = MY["den"][:, i].sum(0) / MY["den_r"][:, i].sum(0)
    DAT[hk] = dict(D=MY["D"][:, i], W=W, B=B, Dx=MY["Dx"][:, i], Wx=W, DRR=MY["DRR"][:, i], m2=MY["den"][:, i], m=MY["m3to8"][:, i])
NS2["DAT"] = DAT; NS2["PRED"].clear(); JM = NS2["BANDS"]["MID"]
assert [c["name"] for c in NS2["CL"]] == [str(x) for x in MY["name"]]
CSTAR = dict(gasshape="P", efe="noclu", red=True)
CELLD = {}
for f in FOOTS:
    hk = "h0672"; d_ = DAT[hk]; WB = d_["W"] * d_["B"][None, :]; Pm = NS2["stack_model"](f, hk, **CSTAR)[0].copy(); NS2["PRED"].clear()
    CELLD[f] = dict(n=(WB[:, JM] * (d_["D"][:, JM] - MY["leakP"][:, HXI[hk], 0][:, JM])).sum(1), d=(d_["W"][:, JM] * Pm[:, JM]).sum(1),
                    sn=np.sqrt((d_["W"][:, JM] * d_["B"][None, JM] ** 2).sum(1)))
EFITS = fits.open(os.path.join(DATA, "erass1cl_primary_v3.2.fits"))[1].data
EIDX = {str(nm).strip(): i for i, nm in enumerate(EFITS["NAME"])}
JI = np.array([EIDX[str(x).strip()] for x in MY["name"]])


def ecol(c):
    return np.asarray(EFITS[c], float)[JI]


KT = ecol("KT"); Mg5 = np.asarray(MY["Mgas500"], float); R500 = ecol("R500"); L500 = ecol("L500"); ZB = ecol("BEST_Z")
# S0d: X21 KT terciles
X21 = jl("X21_cluster_switch_anatomy/x21_switch_anatomy_results.json")
okv = np.isfinite(KT) & (KT > 0); I = np.where(okv)[0]; vv = KT[I]; xk = np.log10(vv / np.median(vv))
ids = np.digitize(xk, np.quantile(xk, [1 / 3, 2 / 3]))
S0["S0d"] = dict(nKT=int(len(I)), n=[int((ids == k).sum()) for k in range(3)], edges=np.quantile(vv, [1 / 3, 2 / 3]).tolist(), cells={})
for f in FOOTS:
    c = CELLD[f]
    S0["S0d"]["cells"][f] = dict(mine=[float(c["n"][I][ids == k].sum() / c["d"][I][ids == k].sum()) for k in range(3)],
                                 X21=X21["binned"]["V1"]["terciles"]["cells"][f"{f}|h0672"]["A"])
q3 = jl("X7_cluster_core_significance/x7_analysis_results.json")["mass"]["q3"]
RMID = 0.548 * MPC


def beta_M(r, rc):
    xx = r / rc; return rc ** 3 * (xx - np.arctan(xx))


for j in range(NCL):
    nm = str(MY["name"][j]).strip()
    Mg = Mg5[j]; rc = 0.15 * R500[j] / 1e3 * MPC; norm = 1.2 * Mg / beta_M(R500[j] / 1e3 * MPC, rc); Mr = norm * beta_M(RMID, rc)
    sig = math.sqrt(KT[j] * KEV / (MU * MP)) / 1e3 if KT[j] > 0 else NAN
    tier = "T1" if Mg <= q3[0] else ("T2" if Mg <= q3[1] else "T3")
    row = newrow(id=nm, cls="Clusters", subclass=tier, M_b=1.2 * Mg, M_star=0.2 * Mg, M_gas=Mg, f_gas=1 / 1.2, R_char_kpc=R500[j], R_last_kpc=548.0,
                 sigma_kms=sig, V_char_kms=math.sqrt(3) * sig if np.isfinite(sig) else NAN, x_char=G * Mr * MSUN / RMID ** 2 / A0["canonical"],
                 hosted=0.0, z=ZB[j], KT_keV=KT[j] if KT[j] > 0 else NAN, MGAS500=Mg, L500=L500[j], R500_kpc=R500[j], morph_label="eRASS1 cluster",
                 in_pool="P_all", source="X7 x7_measure_percluster.npz + X2 C* model (X21 read-only), MID band, CAL, h0672; eRASS1 v3.2")
    qual = []
    for f in FOOTS:
        c = CELLD[f]; A = c["n"][j] / c["d"][j]; k = FK[f]
        row[f"A_{k}"] = float(A)
        if A > 0:
            row[f"resid_dex_{k}"] = math.log10(A); row[f"resid_err_{k}"] = float(c["sn"][j] / c["d"][j] / (A * LN10))
        else:
            qual.append(f"A_{k}={A:.3g}<=0")
    row["quality"] = "APPROX axis: lensing ratio; shape-noise error only" + ("; " + "; ".join(qual) if qual else "")
    ROWS.append(row)
P(f"  clusters {NCL}; KT>0 {int(okv.sum())}; [{time.time() - T0:.0f} s, RSS {rss_gb():.2f} GB]")

# =====================================================================================================  LG dwarfs (X1 + X20)
X1ROWS = list(csv.DictReader(open(os.path.join(RB, "X1_hosted_recount", "x1_per_system.csv"))))
X20 = {(r["footing"], r["name"]): r for r in csv.DictReader(open(os.path.join(RB, "X20_hosted_dwarf_requirement", "x20_per_system.csv")))}
ISO = "Delta[iso AQUAL L*0]"; EFE = "Delta[AQUAL + EFE L*0 (exact MOND + EFE)]"
byname = {}
for x in X1ROWS:
    byname.setdefault(x["name"], {})[x["footing"]] = x
for nm, dd in byname.items():
    x = dd["canonical"]
    M = 10 ** float(x["logMstar"]); rh = float(x["rh_pc"]) / 1e3; r12 = 4 / 3 * rh
    h = X20.get(("canonical", nm), {}).get("hosted", "")
    row = newrow(id=nm, cls="LG dwarfs", subclass=x["cls"], M_b=M, M_star=M, R_char_kpc=rh, R_last_kpc=r12, sigma_kms=float(x["sigma"]),
                 V_char_kms=math.sqrt(3) * float(x["sigma"]), x_char=G * (M / 2) * MSUN / (r12 * KPC) ** 2 / A0["canonical"], e_ext=float(x["x_e_mid"]),
                 hosted=float(h) if h != "" else NAN, morph_label="dSph/dIrr", quality=f"host={x['host']}; d_host={x['d_host_kpc']} kpc", in_pool="P_gal",
                 source="X1 x1_per_system.csv (Delta iso AQUAL L*0 / sdMC; EFE column) + X20 hosted")
    for f in FOOTS:
        xf = dd[f]; k = FK[f]
        row[f"resid_dex_{k}"] = float(xf[ISO]); row[f"resid_err_{k}"] = float(xf["sdMC[iso AQUAL L*0]"]); row[f"resid_efe_{k}"] = float(xf[EFE])
    ROWS.append(row)
X1OUT = open(os.path.join(RB, "X1_hosted_recount", "x1_hosted_recount.out")).read().split("--- step 2: class statistics")[1].split("--- step 2: class status")[0]
X1KEY = {"LG field": "LG field", "MW classical": "MW classical", "MW ultra-faint": "MW ultra-faint", "bright M31": "bright M31",
         "M31 others": "M31 others", "Crater II": "indiv:Crater II", "Antlia II": "indiv:Antlia II"}
S0["S0c"] = {}
X1J = jl("X1_hosted_recount/x1_hosted_recount_results.json")["class_stats"]       # AMENDMENT A1: graded = record JSON vs printed
for f in FOOTS:
    blk = X1OUT.split(f"[{f}]")[1].split("[alt]")[0] if f == "canonical" else X1OUT.split("[alt]")[1]
    for nm, k in X1KEY.items():
        m = re.search(re.escape(k) + r"\s+N\s+\d+ \|.*? iso ([+-][0-9.]+)", blk)
        v = [float(x[ISO]) for x in X1ROWS if x["footing"] == f and x["cls"] == k]
        S0["S0c"][f"{f}|{nm}"] = dict(record_json=X1J[f"{f}|{k}|primary|iso AQUAL L*0"]["median"], printed=float(m.group(1)), N=len(v),
                                      plain_median_REPORTED=float(np.median(v)))

# =====================================================================================================  Coma UDGs (S1)
S1C = jl("S1_v3_hosted_small/s1_v3_hosted_small_results.json")["coma"]
COMA = {}
for x in csv.DictReader(open(os.path.join(RB, "S1_v3_hosted_small", "s1_coma_per_galaxy.csv"))):
    COMA.setdefault(x["name"], {})[x["footing"]] = x
S0["S0g"] = {}
for f in FOOTS:
    per = S1C[f"{f}|S2 AQUAL isolated L*0 E-W"]["per"]
    S0["S0g"][f] = dict(mine=float(np.mean([p[1] / LN10 for p in per])), S1=S1C[f"{f}|S2 AQUAL isolated L*0 E-W"]["meanE_dex"])
for nm, dd in COMA.items():
    x = dd["canonical"]; M = float(x["Mstar"]); Re = float(x["Re_kpc"]); r12 = 4 / 3 * Re
    row = newrow(id=nm, cls="Coma UDGs", subclass="Coma UDG", M_b=M, M_star=M, R_char_kpc=Re, R_last_kpc=r12, sigma_kms=float(x["sigma"]),
                 V_char_kms=math.sqrt(3) * float(x["sigma"]), x_char=G * (M / 2) * MSUN / (r12 * KPC) ** 2 / A0["canonical"], e_ext=float(x["x_e_dmean"]),
                 hosted=1.0, morph_label="UDG", quality=f"esig={x['esig']} km/s; d_mean={x['d_mean_kpc']} kpc", in_pool="P_gal",
                 source="S1 coma[S2 AQUAL isolated L*0 E-W].per (iso) / [S3 AQUAL + EFE dmean L*0 E-W].per (EFE); s1_coma_per_galaxy.csv")
    for f in FOOTS:
        k = FK[f]
        pi = {p[0]: p for p in S1C[f"{f}|S2 AQUAL isolated L*0 E-W"]["per"]}[nm]
        pe = {p[0]: p for p in S1C[f"{f}|S3 AQUAL + EFE dmean L*0 E-W"]["per"]}[nm]
        row[f"resid_dex_{k}"] = pi[1] / LN10; row[f"resid_err_{k}"] = pi[2] / LN10; row[f"resid_efe_{k}"] = pe[1] / LN10
    ROWS.append(row)

# =====================================================================================================  TDGs, DF2/DF4
TDG = []
for r in csv.DictReader(open(os.path.join(DATA, "tidal_dwarfs", "lelli2015_tdg.csv"))):
    TDG.append(dict(name=r["object"].replace(" ", ""), V=float(r["V_circ_kms"]), M=float(r["M_bar_1e8"]) * 1e8, R=float(r["R_out_kpc"]),
                    Ms=float(r["M_star_1e8"]) * 1e8, Mg=(float(r["M_atom_1e8"]) + float(r["M_mol_1e8"])) * 1e8, host=r["host"], D=float(r["dist_Mpc"]),
                    inc=float(r["i_deg"])))
T5 = {f: P4["T5"]["footings"][f] for f in FOOTS}
S0["S0f"] = {}
for f in FOOTS:
    tl = [math.log10(((o["V"] * 1e3) ** 2 / (o["R"] * KPC)) / float(law(G * o["M"] * MSUN / (o["R"] * KPC) ** 2, A0[f]))) for o in TDG]
    S0["S0f"][f"TDG|{f}"] = dict(mine=float(np.mean(tl)), P4=T5[f]["T_law_isolated"]["rbar"])
for o in TDG:
    row = newrow(id=o["name"], cls="TDGs", subclass=o["host"], M_b=o["M"], M_star=o["Ms"], M_gas=o["Mg"], f_gas=o["Mg"] / o["M"], R_char_kpc=o["R"],
                 R_last_kpc=o["R"], V_char_kms=o["V"], x_char=G * o["M"] * MSUN / (o["R"] * KPC) ** 2 / A0["canonical"], hosted=1.0, D_Mpc=o["D"],
                 inc_deg=o["inc"], morph_label="tidal dwarf", in_pool="P_gal", quality="R_char = R_out (no half radius)",
                 source="Lelli+15 TDG CSV (X19 K1 estimator); err P4 T5 L0 T_points s; EFE P4 T5 L24 T_points r")
    gep = {p["name"]: p for p in T5["canonical"]["L0"]["T_points"]}
    row["e_ext"] = gep[o["name"]]["ge"]
    for f in FOOTS:
        k = FK[f]; a0 = A0[f]
        row[f"resid_dex_{k}"] = math.log10(((o["V"] * 1e3) ** 2 / (o["R"] * KPC)) / float(law(G * o["M"] * MSUN / (o["R"] * KPC) ** 2, a0)))
        row[f"resid_err_{k}"] = {p["name"]: p for p in T5[f]["L0"]["T_points"]}[o["name"]]["s"]
        row[f"resid_efe_{k}"] = {p["name"]: p for p in T5[f]["L24"]["T_points"]}[o["name"]]["r"]
    ROWS.append(row)
src657 = open(os.path.join(CFGD, "CFG657_trail_capture_rule", "cfg657_capture.py")).read()
DFG = {}
for nm in ("DF2", "DF4"):
    m = re.search(r'"%s":\s*dict\(Ms=([0-9.e+]+), eMs=[0-9.]+, Re=([0-9.]+), Dref=[0-9.]+, D=([0-9.]+), obs=\(([0-9.]+), ([0-9.]+), ([0-9.]+)\), pos=\(([0-9.-]+), ([0-9.-]+)\), age=\(([0-9.]+)' % nm, src657)
    DFG[nm] = dict(Ms=float(m.group(1)), Re=float(m.group(2)), D=float(m.group(3)), sig=float(m.group(4)))
for f in FOOTS:
    dl = []
    for nm, o in DFG.items():
        r12 = 4 / 3 * o["Re"] * KPC; gb = G * (o["Ms"] / 2) * MSUN / r12 ** 2
        dl.append(2 * math.log(o["sig"] / (math.sqrt(r12 * float(law(gb, A0[f])) / 3) / 1e3)))
    S0["S0f"][f"DF|{f}"] = dict(mine=float(np.mean(dl)), P4=T5[f]["U_law_isolated"]["rbar"])
for nm, o in DFG.items():
    M = o["Ms"]; r12 = 4 / 3 * o["Re"]
    row = newrow(id=nm, cls="DF2/DF4", subclass="NGC1052 group", M_b=M, M_star=M, R_char_kpc=o["Re"], R_last_kpc=r12, sigma_kms=o["sig"],
                 V_char_kms=math.sqrt(3) * o["sig"], x_char=G * (M / 2) * MSUN / (r12 * KPC) ** 2 / A0["canonical"], hosted=1.0, D_Mpc=o["D"],
                 e_ext={p["name"]: p for p in T5["canonical"]["L0"]["U_points"]}[nm]["ge"], morph_label="dark-matter-deficient UDG", in_pool="P_gal",
                 source="CFG657 inputs (X19 K1 estimator); err P4 T5 L0 U_points s/ln10; EFE P4 T5 L24 U_points r/ln10")
    for f in FOOTS:
        k = FK[f]; r12m = r12 * KPC; gb = G * (M / 2) * MSUN / r12m ** 2
        row[f"resid_dex_{k}"] = 2 * math.log(o["sig"] / (math.sqrt(r12m * float(law(gb, A0[f])) / 3) / 1e3)) / LN10
        row[f"resid_err_{k}"] = {p["name"]: p for p in T5[f]["L0"]["U_points"]}[nm]["s"] / LN10
        row[f"resid_efe_{k}"] = {p["name"]: p for p in T5[f]["L24"]["U_points"]}[nm]["r"] / LN10
    ROWS.append(row)

# =====================================================================================================  SLUGGS centrals (S4 R4, nu1, no ownership)
SLJ = json.load(open(glob.glob(os.path.join(RB, "S4_v3_muK_clusters", "r4_out", "cfg528b_measured_tracers", "nu1_noown", "*_results.json"))[0]))
SLR = SLJ["rows"]["J joint best case"]


def vizier(fn):
    rows = [l.rstrip("\n") for l in open(os.path.join(DATA, fn), encoding="latin-1") if l.strip() and not l.startswith("#")]
    k = next(i for i, l in enumerate(rows) if set(l.replace("\t", "").strip()) <= set("-"))
    hdr = [h.strip() for h in rows[k - 2].split("\t")]
    return [dict(zip(hdr, [x.strip() for x in l.split("\t")])) for l in rows[k + 1:]]


SLG = {int(r["NGC"]): r for r in vizier("sluggs_forbes2017_galaxies.tsv") if r["NGC"].isdigit()}
for n in (4486, 4365, 4374, 5846):
    g = SLG[n]; D = float(g["Dist"]); M = 10 ** float(g["logM*"]); Re = float(g["Reff"]) / 206264.8 * D * 1e3
    row = newrow(id=f"NGC{n}", cls="SLUGGS centrals", subclass=g["MType"].strip(), M_b=M, M_star=M, R_char_kpc=Re, D_Mpc=D,
                 sigma_kms=float(g["sigma"]) if g["sigma"] else NAN, x_char=G * (M / 2) * MSUN / (Re * KPC) ** 2 / A0["canonical"], hosted=0.0,
                 morph_label="central elliptical", in_pool="P_gal", quality="APPROX axis: 2 x dlog sigma (GC kinematics, outer bins)",
                 source="S4 R4 r4_out/cfg528b_measured_tracers/nu1_noown rows['J joint best case']; Forbes+17 SLUGGS table")
    for f in FOOTS:
        k = FK[f]; o = SLR[f]["per"][f"NGC{n}"]; Z = SLR[f]["Z"][f"NGC{n}"]
        row[f"resid_dex_{k}"] = 2 * o; row[f"resid_err_{k}"] = abs(2 * o / Z)
    ROWS.append(row)

# =====================================================================================================  lens stacks (S2)
S2L = jl("S2_v3_lowg_lensing/s2_v3_lowg_lensing_results.json")["ladder"]
for pop in ("blue", "red"):
    row = newrow(id=f"KiDS {pop} lens stack", cls="Lens stacks", subclass=pop, morph_label=f"{pop} isolated lenses (stack)",
                 quality="STACK (population, not an object): never in per-object statistics; APPROX axis", in_pool="",
                 source="S2 ladder L4 (v3 at y_e = 0) / L5 (+EFE primary)")
    for f in FOOTS:
        k = FK[f]
        a = S2L[f][[x for x in S2L[f] if x.startswith("L4")][0]][pop]; b = S2L[f][[x for x in S2L[f] if x.startswith("L5")][0]][pop]
        row[f"resid_dex_{k}"] = math.log10(a["A"]); row[f"resid_err_{k}"] = a["sA"] / (a["A"] * LN10); row[f"resid_efe_{k}"] = math.log10(b["A"])
    ROWS.append(row)

# =====================================================================================================  STEP 0
P("\n=== STEP 0: reproduce the record's headline numbers from the atlas sources (stop rule)")
s0 = {}
s0["S0a"] = all(len(GALS) == 175 and abs(S0["S0a"][f]["mine"] - S0["S0a"][f]["P4_iso"]) <= 1e-4 and abs(S0["S0a"][f]["mine"] - S0["S0a"][f]["P4_L24"]) <= 1e-3 for f in FOOTS)
check("S0a", s0["S0a"], "; ".join(f"{f}: mine {S0['S0a'][f]['mine']:.5f} vs P4 iso {S0['S0a'][f]['P4_iso']:.5f} / L24 {S0['S0a'][f]['P4_L24']:.5f}" for f in FOOTS),
      "|d iso| <= 1e-4, |d L24| <= 1e-3, N 175")
s0["S0b"] = all(S0["S0b"][f][c]["N"] == S0["S0b"][f][c]["P4_N"] and abs(S0["S0b"][f][c]["mine"] - S0["S0b"][f][c]["P4"]) <= 0.010 for f in FOOTS for c in ("small", "large"))
check("S0b", s0["S0b"], "; ".join(f"{f} {c}: N {S0['S0b'][f][c]['N']}/{S0['S0b'][f][c]['P4_N']} mean {S0['S0b'][f][c]['mine']:+.4f} vs P4 {S0['S0b'][f][c]['P4']:+.4f}"
                                  for f in FOOTS for c in ("small", "large")), "N equal; |d| <= 0.010 dex")
s0["S0c"] = all(abs(v["record_json"] - v["printed"]) <= 0.005 + 1e-12 for v in S0["S0c"].values())
check("S0c", s0["S0c"], "; ".join(f"{k} {v['record_json']:+.3f}/{v['printed']:+.2f}" for k, v in S0["S0c"].items()), "AMENDMENT A1: X1 JSON vs printed, |d| <= 0.005")
P("  S0c-plain (REPORTED, A1): plain per-system medians vs X1 printed: " + "; ".join(f"{k} {v['plain_median_REPORTED']:+.3f} (d {v['plain_median_REPORTED'] - v['printed']:+.3f})" for k, v in S0["S0c"].items()))
s0["S0d"] = S0["S0d"]["nKT"] == 106 and S0["S0d"]["n"] == [35, 35, 36] and all(abs(a - b) <= 1e-9 for f in FOOTS for a, b in zip(S0["S0d"]["cells"][f]["mine"], S0["S0d"]["cells"][f]["X21"]))
check("S0d", s0["S0d"], f"N_KT {S0['S0d']['nKT']}, n {S0['S0d']['n']}, edges {[round(e, 3) for e in S0['S0d']['edges']]}; " +
      "; ".join(f"{f}: " + " / ".join(f"{a:.4f}" for a in S0["S0d"]["cells"][f]["mine"]) + " vs X21 " + " / ".join(f"{b:.4f}" for b in S0["S0d"]["cells"][f]["X21"]) for f in FOOTS),
      "106; 35/35/36; |d| <= 1e-9")
s0["S0e"] = all(S0["S0e"][f]["N"] == 63 and abs(S0["S0e"][f]["mine"] - S0["S0e"][f]["P4"]) <= 1e-6 for f in FOOTS)
check("S0e", s0["S0e"], "; ".join(f"{f}: {S0['S0e'][f]['mine']:+.6f} vs P4 {S0['S0e'][f]['P4']:+.6f}" for f in FOOTS), "N 63; |d| <= 1e-6")
s0["S0f"] = all(abs(v["mine"] - v["P4"]) <= 1e-3 for v in S0["S0f"].values())
check("S0f", s0["S0f"], "; ".join(f"{k} {v['mine']:+.4f}/{v['P4']:+.4f}" for k, v in S0["S0f"].items()), "|d| <= 1e-3")
s0["S0g"] = all(abs(S0["S0g"][f]["mine"] - S0["S0g"][f]["S1"]) <= 1e-9 for f in FOOTS)
check("S0g", s0["S0g"], "; ".join(f"{f} {S0['S0g'][f]['mine']:+.5f}/{S0['S0g'][f]['S1']:+.5f}" for f in FOOTS), "|d| <= 1e-9")
STOP = not all(s0.values())

# =====================================================================================================  atlas checks, plant, MUTATE
CLASSES = ["SPARC", "MW disc", "Groups", "Clusters", "LG dwarfs", "Coma UDGs", "TDGs", "DF2/DF4", "SLUGGS centrals", "Lens stacks"]
cnt = {c: sum(1 for r in ROWS if r["cls"] == c) for c in CLASSES}
nlg = len(byname)
exp = {"SPARC": 175, "MW disc": 1, "Groups": 63, "Clusters": 326, "LG dwarfs": nlg, "Coma UDGs": 9, "TDGs": 6, "DF2/DF4": 2, "SLUGGS centrals": 4, "Lens stacks": 2}
check("K_rows", cnt == exp, json.dumps(cnt), json.dumps(exp))

# the planted positive control (SPARC only; before any shuffle)
def L(v):
    v = np.asarray(v, float); return np.where(v > 0, np.log10(np.where(v > 0, v, 1.0)), NAN)


spr = [r for r in ROWS if r["cls"] == "SPARC"]
ls0 = L([r["Sigma0"] for r in spr]); zs = (ls0 - np.nanmean(ls0)) / np.nanstd(ls0)
for r, z in zip(spr, zs):
    for k in ("can", "alt"):
        r[f"plant_{k}"] = r[f"resid_dex_{k}"] + 0.10 * z if np.isfinite(z) else NAN

RESCOLS = [f"{a}_{k}" for k in ("can", "alt") for a in ("resid_dex", "resid_err", "resid_efe", "resid_perU_med", "rms_curve", "resid_wmean", "Ups_fit", "A", "plant")]
if MUT:
    rng = np.random.default_rng(3333)
    for c in CLASSES:
        idx = [i for i, r in enumerate(ROWS) if r["cls"] == c]
        perm = rng.permutation(len(idx))
        blk = [{k: ROWS[i].get(k, NAN) for k in RESCOLS} for i in idx]
        for j, i in enumerate(idx):
            ROWS[i].update(blk[perm[j]])

# K_ident
def find(c, nm):
    return next(r for r in ROWS if r["cls"] == c and r["id"] == nm)


idv = []
for f in FOOTS:
    k = FK[f]
    idv.append(("CamB Ups_fit", find("SPARC", "CamB")[f"Ups_fit_{k}"], PERU[f]["CamB"]["U_rms"]))
    for nm in ("Crater II", "Antlia II", "Bootes I"):
        idv.append((nm, find("LG dwarfs", nm)[f"resid_dex_{k}"], float(next(x for x in X1ROWS if x["footing"] == f and x["name"] == nm)[ISO])))
    idv.append(("DF2", find("DF2/DF4", "DF2")[f"resid_dex_{k}"], {p["name"]: p for p in T5[f]["L0"]["U_points"]}["DF2"]["E_obs"] / LN10 if "E_obs" in T5[f]["L0"]["U_points"][0] else NAN))
    idv.append(("NGC5291N", find("TDGs", "NGC5291N")[f"resid_efe_{k}"], {p["name"]: p for p in T5[f]["L24"]["T_points"]}["NGC5291N"]["r"]))
    idv.append(("DFX1", find("Coma UDGs", "DFX1")[f"resid_dex_{k}"], {p[0]: p for p in S1C[f"{f}|S2 AQUAL isolated L*0 E-W"]["per"]}["DFX1"][1] / LN10))
    idv.append(("NGC4486", find("SLUGGS centrals", "NGC4486")[f"resid_dex_{k}"], 2 * SLR[f]["per"]["NGC4486"]))
# DF2 reference: the record's own L0 E_obs is vs the isolated law at L*0 (solver) -> compare to X19's estimator within 1e-3 instead of 1e-9
bad = []
for nm, a, b in idv:
    tol = 1e-3 if nm == "DF2" else 1e-9
    if not (np.isfinite(a) and np.isfinite(b) and abs(a - b) <= tol):
        bad.append(f"{nm} {a} vs {b}")
check("K_ident", not bad, f"{len(idv) - len(bad)}/{len(idv)} named rows equal their sources" + (f"; mismatches {bad[:4]}" if bad else ""),
      "all within 1e-9 (DF2 1e-3: record solver vs algebraic)")

# =====================================================================================================  CSV
COLS = ["id", "class", "subclass", "morphology_T", "M_b", "M_star", "M_gas", "f_gas", "R_char_kpc", "R_last_kpc", "Sigma0", "V_char_kms", "sigma_kms",
        "x_char", "e_ext", "hosted", "z", "resid_dex_can", "resid_err_can", "resid_dex_alt", "resid_err_alt", "quality", "source",
        "morph_label", "Sigma_half", "D_Mpc", "inc_deg", "L36", "M_HI", "R_eff_kpc", "R_disk_kpc", "V_flat_kms", "Q", "Ups_fit_can", "Ups_fit_alt",
        "resid_perU_med_can", "resid_perU_med_alt", "rms_curve_can", "rms_curve_alt", "resid_wmean_can", "resid_wmean_alt", "resid_efe_can",
        "resid_efe_alt", "KT_keV", "MGAS500", "L500", "R500_kpc", "A_can", "A_alt", "uma_member", "in_pool"]


def fmt(v):
    if isinstance(v, str):
        return v
    if v is None or not np.isfinite(v):
        return "NaN"
    return f"{v:.6g}"


if not MUT:
    with open(os.path.join(HERE, "x33_atlas.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(COLS)
        for r in ROWS:
            w.writerow([fmt(r["cls"] if c == "class" else r[c]) for c in COLS])
    sz = os.path.getsize(os.path.join(HERE, "x33_atlas.csv"))
    check("K_size", sz < 2e6, f"{sz / 1e6:.3f} MB, {len(ROWS)} rows", "< 2 MB")

if STOP:
    P("\nSTEP 0 FAILED: stop rule. No findings written.")
    open(os.path.join(HERE, f"x33_system_atlas{TAG}.out"), "w").write("\n".join(OUTL) + "\n")
    sys.exit(1)

# =====================================================================================================  ANALYSIS
P(f"\n=== ANALYSIS (both footings, never pooled; bootstrap {NBOOT}; BH-FDR q 0.05 + Bonferroni) [{time.time() - T0:.0f} s]")
PROPS = [  # name, column, transform, flag
    ("log M_b", "M_b", "log", ""), ("log M_star", "M_star", "log", ""), ("f_gas", "f_gas", "lin", ""), ("log R_char", "R_char_kpc", "log", ""),
    ("log R_last", "R_last_kpc", "log", ""), ("log Sigma_half", "Sigma_half", "log", ""), ("log Sigma0", "Sigma0", "log", ""),
    ("log V_char", "V_char_kms", "log", "shares observable"), ("log sigma", "sigma_kms", "log", "shares observable"),
    ("log x_char", "x_char", "log", ""), ("log e_ext", "e_ext", "log", ""), ("hosted", "hosted", "lin", ""), ("z", "z", "lin", ""),
    ("morphology T", "morphology_T", "lin", ""), ("D_Mpc", "D_Mpc", "lin", "systematic"), ("inc_deg", "inc_deg", "lin", "systematic"),
    ("Q", "Q", "lin", "systematic"), ("log KT", "KT_keV", "log", ""), ("log L500", "L500", "log", ""), ("log MGAS500", "MGAS500", "log", ""),
]
PERCLASS = ["SPARC", "Groups", "Clusters", "LG dwarfs", "Coma UDGs", "TDGs"]           # N >= 8
SUBS = [("SPARC", "small"), ("SPARC", "large"), ("LG dwarfs", "MW ultra-faint"), ("LG dwarfs", "bright M31")]


def pv(rows, col, tr):
    v = np.array([r[col] if not isinstance(r[col], str) else NAN for r in rows], float)
    return L(v) if tr == "log" else v


def resv(rows, k, use_A=False, plant=False):
    if plant:
        return np.array([r.get(f"plant_{k}", NAN) for r in rows], float)
    if use_A:
        return np.array([r[f"A_{k}"] for r in rows], float)
    return np.array([r[f"resid_dex_{k}"] for r in rows], float)


RNG = np.random.default_rng(SEED)


def spear_boot(x, y, key):
    ok = np.isfinite(x) & np.isfinite(y); x, y = x[ok], y[ok]; n = len(x)
    if n < 8 or len(np.unique(x)) < 3 or len(np.unique(y)) < 3:
        return None
    rho, p = spearmanr(x, y)
    rng = np.random.default_rng([SEED, key])
    ix = rng.integers(0, n, size=(NBOOT, n))
    rx = rankdata(x[ix], axis=1); ry = rankdata(y[ix], axis=1)
    rx -= rx.mean(1, keepdims=True); ry -= ry.mean(1, keepdims=True)
    den = np.sqrt((rx ** 2).sum(1) * (ry ** 2).sum(1)); rb = np.where(den > 0, (rx * ry).sum(1) / np.where(den > 0, den, 1), NAN)
    lo, hi = np.nanpercentile(rb, [16, 84])
    return dict(n=int(n), rho=float(rho), err=float(0.5 * (hi - lo)), p=float(p))


def bh(ps, q=0.05):
    ps = np.asarray(ps, float); m = len(ps)
    if m == 0:
        return np.zeros(0, bool), NAN
    o = np.argsort(ps); thr = q * np.arange(1, m + 1) / m; ok = ps[o] <= thr
    kmax = np.max(np.nonzero(ok)[0]) if ok.any() else -1
    sig = np.zeros(m, bool)
    if kmax >= 0:
        sig[o[:kmax + 1]] = True
    return sig, (float(thr[kmax]) if kmax >= 0 else 0.0)


def pool_rows(name):
    if name == "P_gal":
        return [r for r in ROWS if r["in_pool"] == "P_gal"]
    return [r for r in ROWS if r["in_pool"] in ("P_gal", "P_all")]


FIND = {"footings": {}, "counts": cnt, "step0": S0, "plan": "FROZEN_CRITERIA.md section 4"}
key = 0
for f in FOOTS:
    k = FK[f]; FR = {}
    tests = []      # (label, dict)
    # (a) within class, subclass, pooled, pooled-centred
    corr = {}
    for c in PERCLASS:
        rows = [r for r in ROWS if r["cls"] == c]
        y = resv(rows, k, use_A=(c == "Clusters"))
        for pn, col, tr, fl in PROPS:
            key += 1; o = spear_boot(pv(rows, col, tr), y, key)
            if o:
                o.update(scope=c, prop=pn, flag=fl, resid="A_i (rank-invariant)" if c == "Clusters" else "resid_dex"); corr[f"{c}|{pn}"] = o
    for c, sc in SUBS:
        rows = [r for r in ROWS if r["cls"] == c and r["subclass"] == sc]
        y = resv(rows, k)
        for pn, col, tr, fl in PROPS:
            key += 1; o = spear_boot(pv(rows, col, tr), y, key)
            if o:
                o.update(scope=f"{c}:{sc}", prop=pn, flag=fl, resid="resid_dex"); corr[f"{c}:{sc}|{pn}"] = o
    for pool in ("P_gal", "P_all"):
        rows = pool_rows(pool)
        y = resv(rows, k)
        med = {c: np.nanmedian([r[f"resid_dex_{k}"] for r in rows if r["cls"] == c]) for c in {r["cls"] for r in rows}}
        yc = np.array([r[f"resid_dex_{k}"] - med[r["cls"]] for r in rows], float)
        for pn, col, tr, fl in PROPS:
            key += 1; o = spear_boot(pv(rows, col, tr), y, key)
            if o:
                o.update(scope=pool, prop=pn, flag=fl, resid="resid_dex"); corr[f"{pool}|{pn}"] = o
            key += 1; o = spear_boot(pv(rows, col, tr), yc, key)
            if o:
                o.update(scope=pool + " (class-centred)", prop=pn, flag=fl, resid="resid_dex - class median"); corr[f"{pool} centred|{pn}"] = o
    # plant (SPARC)
    rows = [r for r in ROWS if r["cls"] == "SPARC"]
    plant = spear_boot(pv(rows, "Sigma0", "log"), resv(rows, k, plant=True), 999999)
    # (d) misfits vs law-right (Mann-Whitney)
    mw = {}
    for scope in ("P_gal", "P_all", "SPARC", "LG dwarfs"):
        rows = pool_rows(scope) if scope.startswith("P_") else [r for r in ROWS if r["cls"] == scope]
        y = resv(rows, k)
        right = np.abs(y) <= 0.05; above = y > 0.2; below = y < -0.2
        for pn, col, tr, fl in PROPS:
            x = pv(rows, col, tr)
            for side, msk in (("above", above), ("below", below)):
                a = x[msk & np.isfinite(x)]; b = x[right & np.isfinite(x)]
                if len(a) < 5 or len(b) < 5 or len(np.unique(np.r_[a, b])) < 2:
                    continue
                U, p = mannwhitneyu(a, b, alternative="two-sided")
                mw[f"{scope}|{side}|{pn}"] = dict(scope=scope, side=side, prop=pn, flag=fl, n_mis=int(len(a)), n_right=int(len(b)),
                                                  med_mis=float(np.median(a)), med_right=float(np.median(b)), U=float(U), p=float(p),
                                                  effect=float(U / (len(a) * len(b)) - 0.5))
    allp = [v["p"] for v in corr.values()] + [v["p"] for v in mw.values()]
    sig, thr = bh(allp)
    m = len(allp)
    for (kk, v), s in zip(list(corr.items()) + list(mw.items()), sig):
        v["fdr"] = bool(s); v["bonf"] = bool(v["p"] <= 0.05 / m)
    sigP, thrP = bh(allp + [plant["p"]])
    FR["n_tests"] = m; FR["bh_threshold_p"] = thr; FR["bonferroni_p"] = 0.05 / m
    FR["correlations"] = corr; FR["misfit_vs_lawright"] = mw
    FR["plant"] = dict(plant, survives_fdr=bool(sigP[-1]))
    # (b) binned residual
    binned = {}
    for scope in ["SPARC", "Groups", "Clusters", "LG dwarfs", "P_gal", "P_all"]:
        rows = pool_rows(scope) if scope.startswith("P_") else [r for r in ROWS if r["cls"] == scope]
        y = resv(rows, k)
        for pn, col, tr in (("morphology T", "morphology_T", "lin"), ("log Sigma0", "Sigma0", "log"), ("f_gas", "f_gas", "lin"),
                            ("log R_char", "R_char_kpc", "log"), ("log V_char", "V_char_kms", "log"), ("log x_char", "x_char", "log"),
                            ("log Sigma_half", "Sigma_half", "log"), ("log M_b", "M_b", "log")):
            x = pv(rows, col, tr); ok = np.isfinite(x) & np.isfinite(y)
            if ok.sum() < 20 or len(np.unique(x[ok])) < 4:
                continue
            edges = [-np.inf, 3.5, 6.5, 8.5, np.inf] if pn == "morphology T" else [-np.inf] + np.quantile(x[ok], [0.25, 0.5, 0.75]).tolist() + [np.inf]
            bins = []
            for b in range(4):
                sel = ok & (x > edges[b]) & (x <= edges[b + 1]) if b > 0 else ok & (x <= edges[1])
                yy = y[sel]
                if len(yy) == 0:
                    bins.append(dict(n=0)); continue
                key += 1; rg = np.random.default_rng([SEED, key]); bm = np.median(yy[rg.integers(0, len(yy), size=(NBOOT, len(yy)))], axis=1)
                bins.append(dict(n=int(len(yy)), lo=float(np.min(x[sel])), hi=float(np.max(x[sel])), median=float(np.median(yy)),
                                 q16=float(np.percentile(bm, 16)), q84=float(np.percentile(bm, 84)), frac_lawright=float(np.mean(np.abs(yy) <= 0.05))))
            binned[f"{scope}|{pn}"] = dict(edges=[float(e) for e in edges[1:-1]], bins=bins)
    FR["binned"] = binned
    # (c) outliers
    outl = {}
    for c in CLASSES:
        rows = [r for r in ROWS if r["cls"] == c and np.isfinite(r[f"resid_dex_{k}"])]
        if len(rows) < 2:
            continue
        nout = max(1, int(math.ceil(0.05 * len(rows))))
        srt = sorted(rows, key=lambda r: -abs(r[f"resid_dex_{k}"]))[:nout]
        outl[c] = [dict(id=r["id"], subclass=r["subclass"], resid=r[f"resid_dex_{k}"], err=r[f"resid_err_{k}"],
                        Z=r[f"resid_dex_{k}"] / r[f"resid_err_{k}"] if r[f"resid_err_{k}"] > 0 else NAN,
                        **{p: r[p] for p in ("morphology_T", "M_b", "f_gas", "R_char_kpc", "Sigma0", "Sigma_half", "V_char_kms", "sigma_kms", "x_char",
                                             "e_ext", "hosted", "z", "D_Mpc", "inc_deg", "Q", "KT_keV", "quality")}) for r in srt]
    FR["outliers"] = outl
    # (d) law-right region
    lr = {"per_class": {}, "ranges": {}}
    for c in CLASSES:
        y = np.array([r[f"resid_dex_{k}"] for r in ROWS if r["cls"] == c], float); y = y[np.isfinite(y)]
        e = np.array([r[f"resid_err_{k}"] for r in ROWS if r["cls"] == c and np.isfinite(r[f"resid_dex_{k}"])], float)
        if len(y) == 0:
            continue
        key += 1; rg = np.random.default_rng([SEED, key]); fb = np.mean(np.abs(y[rg.integers(0, len(y), size=(NBOOT, len(y)))]) <= 0.05, axis=1)
        lr["per_class"][c] = dict(N=int(len(y)), frac_lawright=float(np.mean(np.abs(y) <= 0.05)), frac_err=float(np.std(fb)),
                                  median=float(np.median(y)), frac_above_0p2=float(np.mean(y > 0.2)), frac_below_m0p2=float(np.mean(y < -0.2)),
                                  frac_absZ_lt2=float(np.mean(np.abs(y / e) < 2)) if np.all(e > 0) else NAN)
    for scope in ("P_gal", "P_all", "SPARC"):
        rows = pool_rows(scope) if scope.startswith("P_") else [r for r in ROWS if r["cls"] == scope]
        y = resv(rows, k); right = np.abs(y) <= 0.05
        lr["ranges"][scope] = {}
        for pn, col, tr, fl in PROPS:
            x = pv(rows, col, tr); a = x[right & np.isfinite(x)]; allx = x[np.isfinite(x) & np.isfinite(y)]
            if len(a) < 5:
                continue
            lr["ranges"][scope][pn] = dict(n_right=int(len(a)), p10=float(np.percentile(a, 10)), p90=float(np.percentile(a, 90)),
                                           all_p10=float(np.percentile(allx, 10)), all_p90=float(np.percentile(allx, 90)), flag=fl)
    lr["classes_in_lawright_set"] = {scope: dict(sorted(((c, int(sum(1 for r in (pool_rows(scope) if scope.startswith("P_") else [x for x in ROWS if x["cls"] == scope])
                                                                  if r["cls"] == c and abs(r[f"resid_dex_{k}"]) <= 0.05))) for c in CLASSES)))
                                     for scope in ("P_gal", "P_all")}
    FR["law_right"] = lr
    FIND["footings"][f] = FR
    nfdr = sum(1 for v in corr.values() if v["fdr"]); nfdr_w = sum(1 for v in corr.values() if v["fdr"] and v["scope"] in PERCLASS)
    P(f"\n  [{f}] tests {m}; BH threshold p {thr:.3g}; Bonferroni {0.05 / m:.2g}; FDR-surviving correlations {nfdr} (within-class {nfdr_w}); "
      f"misfit tests surviving {sum(1 for v in mw.values() if v['fdr'])}; plant rho {plant['rho']:+.3f} p {plant['p']:.2g} FDR {FR['plant']['survives_fdr']}")
    FR["n_fdr_corr"] = nfdr; FR["n_fdr_withinclass"] = nfdr_w

# K_plant, K_null
check("K_plant", all(FIND["footings"][f]["plant"]["survives_fdr"] for f in FOOTS),
      "; ".join(f"{f}: rho {FIND['footings'][f]['plant']['rho']:+.3f} p {FIND['footings'][f]['plant']['p']:.2g}" for f in FOOTS), "planted SPARC rho(log Sigma0) survives BH-FDR, both footings")
P(f"  K_null (reported): FDR-surviving within-class correlations {[FIND['footings'][f]['n_fdr_withinclass'] for f in FOOTS]}")

# =====================================================================================================  report
for f in FOOTS:
    FR = FIND["footings"][f]
    P(f"\n=== [{f}] (a) correlations surviving BH-FDR (|rho| order); flag in brackets")
    srt = sorted([v for v in FR["correlations"].values() if v["fdr"]], key=lambda v: -abs(v["rho"]))
    for v in srt[:60]:
        P(f"  {v['scope']:32s} {v['prop']:16s} N {v['n']:4d} rho {v['rho']:+.3f} +- {v['err']:.3f} p {v['p']:.2g}{' BONF' if v['bonf'] else ''}" + (f" [{v['flag']}]" if v["flag"] else ""))
    P(f"  [{f}] misfit vs law-right (Mann-Whitney) surviving BH-FDR:")
    for v in sorted([v for v in FR["misfit_vs_lawright"].values() if v["fdr"]], key=lambda v: v["p"]):
        P(f"  {v['scope']:10s} {v['side']:5s} {v['prop']:16s} n {v['n_mis']}/{v['n_right']} median misfit {v['med_mis']:+.3g} vs law-right {v['med_right']:+.3g} "
          f"(effect {v['effect']:+.2f}) p {v['p']:.2g}{' BONF' if v['bonf'] else ''}" + (f" [{v['flag']}]" if v["flag"] else ""))
    P(f"  [{f}] (d) law-right fraction per class (|resid| <= 0.05 dex):")
    for c, v in FR["law_right"]["per_class"].items():
        P(f"  {c:16s} N {v['N']:4d} median {v['median']:+.3f} law-right {v['frac_lawright']:.3f} +- {v['frac_err']:.3f}  >+0.2 {v['frac_above_0p2']:.3f}  <-0.2 {v['frac_below_m0p2']:.3f}  |Z|<2 {v['frac_absZ_lt2']:.3f}")
    P(f"  [{f}] (d) law-right property ranges (10-90 %) vs all (P_gal):")
    for pn, v in FR["law_right"]["ranges"]["P_gal"].items():
        P(f"  {pn:16s} n_right {v['n_right']:3d}  law-right [{v['p10']:.3g}, {v['p90']:.3g}]  all [{v['all_p10']:.3g}, {v['all_p90']:.3g}]" + (f" [{v['flag']}]" if v["flag"] else ""))
    P(f"  [{f}] (b) binned medians (selected):")
    for kb in ("SPARC|morphology T", "SPARC|log Sigma0", "SPARC|f_gas", "SPARC|log x_char", "P_gal|log Sigma_half", "P_gal|log x_char", "P_gal|log M_b", "Clusters|log x_char"):
        if kb in FR["binned"]:
            b = FR["binned"][kb]
            P(f"  {kb:24s} edges {[round(e, 3) for e in b['edges']]}: " + " | ".join(f"n{x['n']} {x.get('median', NAN):+.3f} [{x.get('q16', NAN):+.3f},{x.get('q84', NAN):+.3f}] lr {x.get('frac_lawright', NAN):.2f}" for x in b["bins"]))
    P(f"  [{f}] (c) worst 5 % per class:")
    for c, lst in FR["outliers"].items():
        P(f"  {c:16s} " + "; ".join(f"{o['id']} {o['resid']:+.3f} (Z {o['Z']:+.1f})" for o in lst[:8]) + (f" ... ({len(lst)} total)" if len(lst) > 8 else ""))

FIND["checks"] = CHECKS; FIND["mutate"] = MUT; FIND["runtime_s"] = time.time() - T0; FIND["rss_gb"] = rss_gb()
npass = sum(v["ok"] for v in CHECKS.values())
P(f"\nX33_SYSTEM_ATLAS COMPLETE: {npass}/{len(CHECKS)} checks PASS  [{time.time() - T0:.0f} s, RSS {rss_gb():.2f} GB]")
json.dump(FIND, open(os.path.join(HERE, f"x33_findings{TAG}.json"), "w"), indent=1, default=lambda o: None if (isinstance(o, float) and not np.isfinite(o)) else float(o))
open(os.path.join(HERE, f"x33_system_atlas{TAG}.out"), "w").write("\n".join(OUTL) + "\n")
sys.exit(0 if npass == len(CHECKS) else 1)
