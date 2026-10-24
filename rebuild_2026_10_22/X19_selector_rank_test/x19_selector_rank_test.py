#!/usr/bin/env python3
"""X19_selector_rank_test: is there one physical variable V whose ordering of the record's system classes reproduces the
required "extra cold mass" pattern?  Criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (8960ea2285), AMENDMENT_A1 (0fc9bade54).

Run:   OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 15 python3 x19_selector_rank_test.py              -> .out, _results.json, _classes.csv
       X19_MUTATE=1 ... python3 x19_selector_rank_test.py                                             -> *_MUTATE.* (K0, K2 must FAIL; exit 1)
kappa = 1/2 FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled. No dark-matter particle. Not "theory closed".
"""
import csv, itertools, json, math, os, re, resource, sys, time

import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
RB = os.path.dirname(HERE)
REPO = os.path.dirname(RB)
EXT = os.path.join(os.path.dirname(REPO), "_external_data")
DATA = os.path.join(REPO, "real_research", "data")
CFGD = os.path.join(REPO, "campaign_fresh_gravity")
MUT = os.environ.get("X19_MUTATE", "") == "1"
TAG = "_MUTATE" if MUT else ""
FOOTS = ("canonical", "alt")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}

G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19; PC = KPC / 1e3; MPC = KPC * 1e3; CL = 2.99792458e8
KB = 1.380649e-23; MP = 1.67262192e-27; KEV = 1.602176634e-16; GYR = 3.15576e16; TH = 13.8; MU = 0.6
H0 = 0.672; OMB = 0.049; OMM = 0.31; OCB = 5.364
RHOC = 3 * (H0 * 100e3 / MPC) ** 2 / (8 * math.pi * G) * PC ** 3 / MSUN           # Msun / pc^3
RHOM = OMM * RHOC

OUTL = []


def P(s=""):
    OUTL.append(s); print(s, flush=True)


CHECKS = {}


def check(name, ok, value, line, detail=""):
    CHECKS[name] = dict(ok=bool(ok), value=value, line=line, detail=detail)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value} (line {line}) {detail}")


def law(gN, a0):                                   # isolated AQUAL, mu = x/(1+x): g = gN nu(gN/a0)
    return 0.5 * (gN + np.sqrt(gN * gN + 4 * gN * a0))


def law_inv(g, a0):
    return g * g / (g + a0)


def jl(p):
    return json.load(open(os.path.join(RB, p)))


P("X19_selector_rank_test  " + ("MUTATE (UFD<->LG field, T1<->T3 swapped in the class table)" if MUT else "normal run"))
P(f"kappa = 1/2 FITTED; footings canonical {A0['canonical']:.4e} / alt {A0['alt']:.4e} never pooled; rho_crit(h {H0}) {RHOC:.4e} Msun/pc^3")

# =====================================================================================================  step 0: the class table
P("\n=== STEP 0: required extra E per class (dex in g), from committed JSON; printed-value and independent checks")
X1 = jl("X1_hosted_recount/x1_hosted_recount_results.json")["class_stats"]
S1 = jl("S1_v3_hosted_small/s1_v3_hosted_small_results.json")["coma"]
U1 = jl("U1_v3_dust_content/u1_a2_field_frame_results.json")["numbers"]["F5"]
P4 = jl("P4_v3_galaxy_tiles/p4_v3_galaxy_tiles_results.json")["tiles"]
X7 = jl("X7_cluster_core_significance/x7_analysis_results.json")["bins"]
LN10 = math.log(10)

CLASSES = ["SPARC small", "SPARC large", "Groups", "Clusters T1", "Clusters T2", "Clusters T3", "MW disc", "LG field",
           "MW classical", "MW ultra-faint", "bright M31", "M31 others", "Crater II", "Antlia II", "Coma UDGs", "UMa members",
           "TDGs", "DF2/DF4", "Cosmic background"]
X1KEY = {"LG field": "LG field", "MW classical": "MW classical", "MW ultra-faint": "MW ultra-faint", "bright M31": "bright M31",
         "M31 others": "M31 others", "Crater II": "indiv:Crater II", "Antlia II": "indiv:Antlia II"}


def build_E(f, base, hkey="h0672"):
    """E, s, Z per class for footing f, baseline 'iso' or 'efe'.  Cluster rows from X7 (CAL)."""
    T = {}
    cg = P4["T1"]["footings"][f]["classes_global_U"]
    for nm, k in (("SPARC small", "small"), ("SPARC large", "large")):
        T[nm] = dict(E=cg[k]["mean"], s=cg[k]["se"], Z=cg[k]["mean"] / cg[k]["se"], src=f"P4 tiles.T1.footings.{f}.classes_global_U.{k}")
    g = P4["T3"]["footings"][f]["v3_isolated"]
    T["Groups"] = dict(E=2 * g["mean"], s=2 * g["tot"], Z=g["Z"], src=f"P4 tiles.T3.footings.{f}.v3_isolated (x2: log sigma -> log g)")
    for i, nm in enumerate(("Clusters T1", "Clusters T2", "Clusters T3")):
        b = X7[f"terciles|{f}|{hkey}"][i]["MID"]
        T[nm] = dict(E=math.log10(b["A_CAL"]), s=b["s_CAL"] / (b["A_CAL"] * LN10), Z=b["Z_CAL"], A=b["A_CAL"],
                     src=f"X7 bins[terciles|{f}|{hkey}][{i}].MID A_CAL/s_CAL/Z_CAL")
    K = P4["T4"]["models"]["B1_McMillan17"][f]["F0|L24"]["K_R0"]
    E = math.log10(66.4 / K); s = 2.2 / (66.4 * LN10)
    T["MW disc"] = dict(E=E, s=s, Z=E / s, src=f"P4 tiles.T4.models.B1_McMillan17.{f}.F0|L24.K_R0 vs 66.4+-2.2")
    lab = "iso AQUAL L*0" if base == "iso" else "AQUAL + EFE L*0 (exact MOND + EFE)"
    for nm, k in X1KEY.items():
        c = X1[f"{f}|{k}|primary|{lab}"]
        T[nm] = dict(E=c["median"], s=c["sd"], Z=c["median"] / c["sd"], src=f"X1 class_stats[{f}|{k}|primary|{lab}]")
    ck = f"{f}|S2 AQUAL isolated L*0 E-W" if base == "iso" else f"{f}|S3 AQUAL + EFE dmean L*0 E-W"
    T["Coma UDGs"] = dict(E=S1[ck]["meanE_dex"], s=S1[ck]["meanE_dex"] / S1[ck]["z_sys"], Z=S1[ck]["z_sys"], src=f"S1 coma[{ck}] (z_sys)")
    u = U1["footings"][f]["A4"]["any_radius"]["per_galaxy"]
    T["UMa members"] = dict(E=u["mean"], s=u["se"], Z=u["mean"] / u["se"], src=f"U1 F5.footings.{f}.A4.any_radius.per_galaxy")
    t5 = P4["T5"]["footings"][f]
    tt = t5["T_law_isolated"] if base == "iso" else dict(rbar=t5["L24"]["T"]["rbar"], se=t5["L24"]["T"]["se"])
    T["TDGs"] = dict(E=tt["rbar"], s=tt["se"], Z=tt["rbar"] / tt["se"], src=f"P4 tiles.T5.footings.{f}." + ("T_law_isolated" if base == "iso" else "L24.T"))
    uu = t5["U_law_isolated"] if base == "iso" else dict(rbar=t5["L24"]["U"]["rbar"], se=t5["L24"]["U"]["se"])
    T["DF2/DF4"] = dict(E=uu["rbar"] / LN10, s=uu["se"] / LN10, Z=uu["rbar"] / uu["se"], src=f"P4 tiles.T5.footings.{f}." + ("U_law_isolated" if base == "iso" else "L24.U") + " (ln -> dex)")
    T["Cosmic background"] = dict(E=math.log10(1 + OCB), s=0.0, Z=float("inf"), src="requirement: Omega_c/Omega_b = 5.364 grows from z~1100 (Z1 R16/R18)")
    if MUT:
        for a, b in (("MW ultra-faint", "LG field"), ("Clusters T1", "Clusters T3")):
            for q in ("E", "s", "Z"):
                T[a][q], T[b][q] = T[b][q], T[a][q]
    return T


# printed values (README / .out digits), canonical / alt, B_iso unless noted
PRINTED = {
    "SPARC small": ({"canonical": -0.046}, 3), "SPARC large": ({"canonical": -0.047}, 3),
    "Clusters T1": ({"canonical": math.log10(1.096), "alt": math.log10(1.002)}, 3),
    "Clusters T2": ({"canonical": math.log10(1.852), "alt": math.log10(1.698)}, 3),
    "Clusters T3": ({"canonical": math.log10(1.837), "alt": math.log10(1.690)}, 3),
    "MW disc": ({"canonical": math.log10(66.4 / 92.3), "alt": math.log10(66.4 / 96.9)}, 3),
    "LG field": ({"canonical": 0.05, "alt": 0.02}, 2), "MW classical": ({"canonical": 0.28, "alt": 0.24}, 2),
    "MW ultra-faint": ({"canonical": 0.63, "alt": 0.59}, 2), "bright M31": ({"canonical": 0.25, "alt": 0.21}, 2),
    "M31 others": ({"canonical": 0.64, "alt": 0.59}, 2),
    "Coma UDGs": ({"canonical": 0.325, "alt": 0.285}, 3), "UMa members": ({"canonical": -0.063, "alt": -0.060}, 3),
    "TDGs": ({"canonical": -0.691, "alt": -0.728}, 3), "DF2/DF4": ({"canonical": -1.940 / LN10, "alt": -2.028 / LN10}, 3),
}
PRINTED_Z = {"Clusters T1": {"canonical": 0.29, "alt": 0.01}, "Clusters T2": {"canonical": 2.29, "alt": 2.05}, "Clusters T3": {"canonical": 4.83, "alt": 4.32},
             "Coma UDGs": {"canonical": 1.64, "alt": 1.45}}

ETAB = {(f, b): build_E(f, b) for f in FOOTS for b in ("iso", "efe")}
ETAB_686 = {f: build_E(f, "iso", "h0686") for f in FOOTS}

# raw per-system tables (X1 CSV): Crater II / Antlia II printed checks + independent medians
X1ROWS = list(csv.DictReader(open(os.path.join(RB, "X1_hosted_recount", "x1_per_system.csv"))))
ISO = "Delta[iso AQUAL L*0]"; EFE = "Delta[AQUAL + EFE L*0 (exact MOND + EFE)]"
# AMENDMENT A2 (post-result, implementation): X1 rows are compared with X1's printed .out class lines ("iso +0.xx"), as frozen
# section 6 says (the first run used the per-system CSV for Crater II / Antlia II, which is not a printed value); groups are
# compared in the record's own unit (log sigma) at its printed digits (the first run doubled the value but not the tolerance).
X1OUT = open(os.path.join(RB, "X1_hosted_recount", "x1_hosted_recount.out")).read().split("--- step 2: class statistics")[1].split("--- step 2: class status")[0]
for f in FOOTS:
    blk = X1OUT.split(f"[{f}]")[1].split("[alt]")[0] if f == "canonical" else X1OUT.split("[alt]")[1]
    for nm, k in X1KEY.items():
        m = re.search(re.escape(k) + r"\s+N\s+\d+ \|.*? iso ([+-][0-9.]+)", blk)
        PRINTED.setdefault(nm, ({}, 2))[0][f] = float(m.group(1))
GROUPS_PRINTED = {"canonical": 0.010, "alt": -0.010}

P(f"\n  {'class':18s} " + " | ".join(f"{f:>9s} E (s) Z" for f in FOOTS) + " | source")
k0_fail = []
for nm in CLASSES:
    row = []
    for f in FOOTS:
        e = ETAB[(f, "iso")][nm]
        row.append(f"{e['E']:+.3f} ({e['s']:.3f}) {e['Z']:+.2f}")
    P(f"  {nm:18s} " + " | ".join(row) + " | " + ETAB[("canonical", "iso")][nm]["src"])
    if nm == "Groups":
        for f, v in GROUPS_PRINTED.items():
            if abs(ETAB[(f, "iso")][nm]["E"] / 2 - v) > 0.0005 + 1e-12:
                k0_fail.append(f"{nm}|{f}|E/2 {ETAB[(f, 'iso')][nm]['E'] / 2:+.4f} vs printed {v:+.3f}")
    elif nm in PRINTED:
        vals, nd = PRINTED[nm]
        for f, v in vals.items():
            if abs(ETAB[(f, "iso")][nm]["E"] - v) > 0.5 * 10 ** (-nd) + 1e-12:
                k0_fail.append(f"{nm}|{f}|E {ETAB[(f, 'iso')][nm]['E']:+.4f} vs printed {v:+.4f}")
    if nm in PRINTED_Z:
        for f, v in PRINTED_Z[nm].items():
            if abs(ETAB[(f, "iso")][nm]["Z"] - v) > 0.005 + 1e-12:
                k0_fail.append(f"{nm}|{f}|Z {ETAB[(f, 'iso')][nm]['Z']:+.3f} vs printed {v:+.2f}")
P("\n  B_EFE (secondary) where it differs from B_iso:")
for nm in CLASSES:
    if any(abs(ETAB[(f, 'efe')][nm]["E"] - ETAB[(f, 'iso')][nm]["E"]) > 1e-9 for f in FOOTS):
        P(f"  {nm:18s} " + " | ".join(f"{ETAB[(f, 'efe')][nm]['E']:+.3f} ({ETAB[(f, 'efe')][nm]['s']:.3f}) {ETAB[(f, 'efe')][nm]['Z']:+.2f}" for f in FOOTS))

decisive_fail = len(k0_fail)
check("K0", decisive_fail == 0, f"{decisive_fail} mismatches" + (": " + "; ".join(k0_fail) if k0_fail else ""), "0 (stop if > 2 decisive rows)",
      "JSON vs printed README/.out digits, B_iso, both footings")
STOP = len({x.split("|")[0] for x in k0_fail}) > 2

# ---------- independent recomputations (K1)
k1 = {}
# TDG and DF2/DF4 isolated-law means (P4 tdg_law / CFG933 estimator with nu1)
TDG = []
for r in csv.DictReader(open(os.path.join(DATA, "tidal_dwarfs", "lelli2015_tdg.csv"))):
    TDG.append(dict(name=r["object"].replace(" ", ""), V=float(r["V_circ_kms"]), M=float(r["M_bar_1e8"]) * 1e8, R=float(r["R_out_kpc"]),
                    Dp=float(r["D_p_kpc"]), tmo=float(r["tmerg_over_torb"]), torb=float(r["t_orb_Gyr"])))
src657 = open(os.path.join(CFGD, "CFG657_trail_capture_rule", "cfg657_capture.py")).read()
DFG = {}
for nm in ("DF2", "DF4"):
    m = re.search(r'"%s":\s*dict\(Ms=([0-9.e+]+), eMs=[0-9.]+, Re=([0-9.]+), Dref=[0-9.]+, D=([0-9.]+), obs=\(([0-9.]+), ([0-9.]+), ([0-9.]+)\), pos=\(([0-9.-]+), ([0-9.-]+)\), age=\(([0-9.]+)' % nm, src657)
    DFG[nm] = dict(Ms=float(m.group(1)), Re=float(m.group(2)), D=float(m.group(3)), sig=float(m.group(4)), ra=float(m.group(7)), dec=float(m.group(8)), age=float(m.group(9)))
mh = re.search(r'HOSTS = \{"NGC1052": \(([0-9.-]+), ([0-9.-]+)\)', src657)
NGC1052 = (float(mh.group(1)), float(mh.group(2)))
for f in FOOTS:
    a0 = A0[f]
    tl = np.mean([math.log10(((o["V"] * 1e3) ** 2 / (o["R"] * KPC)) / float(law(G * o["M"] * MSUN / (o["R"] * KPC) ** 2, a0))) for o in TDG])
    dl = []
    for nm, o in DFG.items():
        r12 = 4 / 3 * o["Re"] * KPC; gb = G * (o["Ms"] / 2) * MSUN / r12 ** 2
        dl.append(2 * math.log(o["sig"] / (math.sqrt(r12 * float(law(gb, a0)) / 3) / 1e3)))
    k1[f"TDG|{f}"] = (float(tl), P4["T5"]["footings"][f]["T_law_isolated"]["rbar"], 1e-3)
    k1[f"DF|{f}"] = (float(np.mean(dl)), P4["T5"]["footings"][f]["U_law_isolated"]["rbar"], 1e-3)
    for nm, k in X1KEY.items():
        v = [float(x[ISO]) for x in X1ROWS if x["footing"] == f and x["cls"] == k]
        k1[f"X1 {nm}|{f}"] = (float(np.median(v)), X1[f"{f}|{k}|primary|iso AQUAL L*0"]["median"], 0.03)
# clusters: membership and medians from X2's per-cluster npz
NPZ = np.load(os.path.join(RB, "X2_cluster_outskirts", "x2_replay_percluster.npz"), allow_pickle=True)
cnames = [str(x) for x in NPZ["name"]]; cMg = np.asarray(NPZ["Mgas500"], float); cR5 = np.asarray(NPZ["R500"], float); cz = np.asarray(NPZ["z"], float)
order = np.argsort(cMg, kind="stable"); n = len(order); qa, qb = n // 3, n - n // 3
TERC = [order[:qa], order[qa:qb], order[qb:]]
q3 = jl("X7_cluster_core_significance/x7_analysis_results.json")["mass"]["q3"]
TERC = [np.nonzero(cMg <= q3[0])[0], np.nonzero((cMg > q3[0]) & (cMg <= q3[1]))[0], np.nonzero(cMg > q3[1])[0]]
tn = [len(t) for t in TERC]; tmed = [float(np.median(cMg[t])) for t in TERC]
k1["cluster terciles n"] = (tn, [109, 108, 109], 0)
k1["cluster terciles median Mgas500"] = (tmed, [3.30e12, 1.17e13, 2.92e13], 0.005)
# SPARC
CFG695 = json.load(open(os.path.join(CFGD, "CFG695_saturating_vacuum", "cfg695_results.json")))["numbers"]["S2"]
U0 = {f: float(CFG695[f]["U"]) for f in FOOTS}
TAB = {}
for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
    tok = line.split()
    if len(tok) != 19:
        continue
    try:
        vals = [float(t) for t in tok[1:18]]
    except ValueError:
        continue
    TAB[tok[0]] = dict(zip(("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q"), vals))
GALS = {}
for fn in sorted(os.listdir(os.path.join(DATA, "sparc_data"))):
    if not fn.endswith("_rotmod.dat"):
        continue
    try:
        d = np.genfromtxt(os.path.join(DATA, "sparc_data", fn), comments="#")
    except Exception:
        continue
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    nm = fn.replace("_rotmod.dat", "")
    if nm in TAB:
        GALS[nm] = dict(R=d[:, 0], Vo=d[:, 1], Vg=d[:, 3], Vd=d[:, 4], Vb=d[:, 5], meta=TAB[nm])
MASTER = {r["name"]: r for r in csv.DictReader(open(os.path.join(DATA, "sparc_master_clean.csv")))}
UMA = sorted(nm for nm, r in MASTER.items() if r["fD"] == "4" and nm in GALS)
ENV = {r["galaxy"].strip(): r for r in csv.DictReader(open(os.path.join(REPO, "real_research", "reviews", "directional_efe_2026", "laneB_data", "chae21_env.csv")))}
for f in FOOTS:
    ns = sum(1 for q in GALS.values() if 1.33 * q["meta"]["MHI"] * 1e9 + U0[f] * q["meta"]["L36"] * 1e9 <= 3e9)
    k1[f"SPARC split|{f}"] = ([ns, len(GALS) - ns], [P4["T1"]["footings"][f]["classes_global_U"]["small"]["N"], P4["T1"]["footings"][f]["classes_global_U"]["large"]["N"]], 0)
k1["UMa N"] = (len(UMA), U1["N_members"], 0)
k1fail = []; k1rep = {}
for k in [k for k in k1 if k.startswith("X1 ")]:
    k1rep[k] = k1.pop(k)
for k, (mine, rec, tol) in k1rep.items():
    P(f"    K1-reported {k:30s} plain median {mine:+.3f} vs X1 bootstrap median {rec:+.3f} (|d| {abs(mine - rec):.3f}; frozen section 6: reported)")
for f in FOOTS:
    lab_plain = {}
    for nm, k in X1KEY.items():
        e_pl = k1rep[f"X1 {nm}|{f}"][0]; s_ = ETAB[(f, "iso")][nm]["s"]; Z = e_pl / s_
        lab_plain[nm] = "EXTRA" if Z >= 2 else ("NONE" if Z < 1 else "AMBIG")
    lab_js = {nm: ("EXTRA" if ETAB[(f, "iso")][nm]["Z"] >= 2 else ("NONE" if ETAB[(f, "iso")][nm]["Z"] < 1 else "AMBIG")) for nm in X1KEY}
    ch = {nm: (lab_js[nm], lab_plain[nm]) for nm in X1KEY if lab_js[nm] != lab_plain[nm]}
    P(f"    [{f}] L-S labels of the X1 classes with plain medians instead of bootstrap medians: changes {ch if ch else 'none'}")
for k, (mine, rec, tol) in k1.items():
    if isinstance(mine, list):
        ok = all(abs(a - b) <= tol * (abs(b) if tol < 1 and abs(b) > 1e3 else 1) for a, b in zip(mine, rec))
    else:
        ok = abs(mine - rec) <= tol
    P(f"    K1 {k:36s} mine {mine} record {rec} tol {tol} {'ok' if ok else 'MISMATCH'}")
    if not ok:
        k1fail.append(k)
check("K1", not k1fail, f"{len(k1) - len(k1fail)}/{len(k1)} agree" + (f"; mismatches {k1fail}" if k1fail else ""), "all within tolerance")

# =====================================================================================================  step 1: V per system
P("\n=== STEP 1: candidate variables per system, at the radius where E is measured")
VN = ["M_b", "sigma", "rho_b", "x", "e", "Phi", "f_hot", "kT", "N_orb", "rho_env", "H"]
VREP = ["f_b", "O"]
VDESC = {"M_b": "baryonic mass [Msun]", "sigma": "velocity scale [km/s] (T_vir same order)", "rho_b": "mean enclosed baryonic density [Msun/pc^3]",
         "x": "internal g_N,bar/a0", "e": "host field g_e/a0", "Phi": "|Phi|/c^2 (Newtonian baryonic + host)", "f_hot": "hot-gas fraction of baryons",
         "kT": "X-ray/virial temperature of the gas [keV] (0 = no X-ray gas)", "N_orb": "t_age/t_orb", "rho_env": "environment density [Msun/pc^3]",
         "H": "hosted flag", "f_b": "M_b/M_dyn (REPORTED ONLY: by-construction risk)", "O": "tidal/collisional origin flag (REPORTED ONLY)"}
SYS = {f: {nm: [] for nm in CLASSES} for f in FOOTS}       # list of dicts per class


def sysrow(**kw):
    d = {k: float("nan") for k in VN + VREP}
    d.update(kw); return d


def tdyn_norb(r_m, v_ms, tage=TH):
    return tage * GYR / (2 * math.pi * r_m / v_ms)


for f in FOOTS:
    a0 = A0[f]
    # ---- SPARC + UMa
    for nm, q in GALS.items():
        m = q["meta"]; U = U0[f]
        Mb = 1.33 * m["MHI"] * 1e9 + U * m["L36"] * 1e9
        vb2 = np.sign(q["Vg"]) * q["Vg"] ** 2 + U * q["Vd"] ** 2 + 1.4 * U * q["Vb"] ** 2
        ok = (vb2 > 0) & (q["Vo"] > 0)
        if not ok.any():
            continue
        i = np.nonzero(ok)[0][-1]; R = q["R"][i] * KPC; vb2l = vb2[i] * 1e6; vo = q["Vo"][i] * 1e3
        gN = vb2l / R; Mr = vb2l * R / G / MSUN
        e = float("nan")
        if nm in ENV:
            lne = 0.5 * (float(ENV[nm]["log_eN_maxclu"]) + float(ENV[nm]["log_eN_noclu"]))
            e = float(law(10 ** lne * 1.2e-10, a0)) / a0
        row = sysrow(M_b=Mb, sigma=vo / math.sqrt(2) / 1e3, rho_b=Mr / (4 / 3 * math.pi * (R / PC) ** 3), x=gN / a0, e=e,
                     Phi=G * Mb * MSUN / R / CL ** 2, f_hot=0.0, kT=0.0, N_orb=tdyn_norb(R, vo), rho_env=RHOM if nm not in UMA else float("nan"),
                     H=1.0 if nm in UMA else 0.0, f_b=vb2l / vo ** 2, O=0.0, name=nm)
        SYS[f]["SPARC small" if Mb <= 3e9 else "SPARC large"].append(row)
        if nm in UMA:
            SYS[f]["UMa members"].append(dict(row))
    # ---- groups (Tian+26 BFJR)
    for l in open(os.path.join(EXT, "vizier2026", "J_A_A_710_L39.tsv")):
        if l.startswith("#"):
            continue
        r = l.rstrip("\n").split("\t")
        if len(r) < 13 or not r[0].strip().isdigit() or r[1].strip() != "Galaxy group":
            continue
        M = 10 ** float(r[7]); s = 10 ** float(r[5]); Re = float(r[10]) * KPC; gb = 10 ** float(r[9])
        SYS[f]["Groups"].append(sysrow(M_b=M, sigma=s, rho_b=(M / 2) / (4 / 3 * math.pi * (Re / PC) ** 3), x=gb / a0, e=float("nan"),
                                       Phi=G * M * MSUN / Re / CL ** 2, f_hot=float("nan"), kT=float("nan"), N_orb=tdyn_norb(Re, math.sqrt(3) * s * 1e3),
                                       rho_env=RHOM, H=0.0, f_b=(G * (M / 2) * MSUN / Re) / (3 * (s * 1e3) ** 2), O=0.0, name=r[2].strip()))
# ---- clusters (eRASS1 FITS; membership by X7's MGAS500 tercile bounds on X2's 326)
from astropy.io import fits  # noqa: E402
EF = fits.open(os.path.join(DATA, "erass1cl_primary_v3.2.fits"))[1].data
EIDX = {str(nm).strip(): i for i, nm in enumerate(EF["NAME"])}
RMID = 0.548 * MPC


def beta_M(r, rc):                    # beta = 2/3 shape, M(<r) up to a constant
    xx = r / rc; return rc ** 3 * (xx - np.arctan(xx))


def beta_phi_out(r1, r2, rc):         # int_r1^r2 4 pi r rho dr up to the same constant / (4 pi): = rc^2/2 ln((1+(r2/rc)^2)/(1+(r1/rc)^2))
    return 0.5 * rc ** 2 * math.log((1 + (r2 / rc) ** 2) / (1 + (r1 / rc) ** 2))


nKT = [0, 0, 0]
for f in FOOTS:
    a0 = A0[f]
    for ti, idx in enumerate(TERC):
        for j in idx:
            nm = cnames[j]; row = EF[EIDX[nm]]
            Mg5 = float(row["MGAS500"]) * 1e11; R5 = float(row["R500"]) / 1e3 * MPC; M500 = float(row["M500"]) * 1e13; kT = float(row["KT"])
            rc = 0.15 * R5; norm = 1.2 * Mg5 / beta_M(R5, rc)                 # Msun per shape unit (stars f* = 0.20 on the gas shape)
            Mr = norm * beta_M(RMID, rc); r3 = 3.0 * MPC
            phi = G * MSUN * (Mr / RMID + norm * beta_phi_out(RMID, r3, rc))          # norm = 4 pi rho0 (beta_M is M/(4 pi rho0))
            sig = math.sqrt(kT * KEV / (MU * MP)) / 1e3 if kT > 0 else float("nan")
            if f == "canonical" and kT > 0:
                nKT[ti] += 1
            SYS[f][f"Clusters T{ti + 1}"].append(sysrow(M_b=1.2 * Mg5, sigma=sig, rho_b=Mr / (4 / 3 * math.pi * (RMID / PC) ** 3), x=G * Mr * MSUN / RMID ** 2 / a0,
                                                        e=float("nan"), Phi=phi / CL ** 2, f_hot=1 / 1.2, kT=kT if kT > 0 else float("nan"),
                                                        N_orb=tdyn_norb(RMID, math.sqrt(3) * sig * 1e3) if kT > 0 else float("nan"), rho_env=RHOM, H=0.0,
                                                        f_b=1.2 * Mg5 / M500, O=0.0, name=nm))
    # ---- MW disc (single system)
    Mb = 6.6461135288785715e10; R0 = 8.122 * KPC; vc = P4["T4"]["models"]["B1_McMillan17"][f]["F0|L24"]["vc_R0"] * 1e3
    gN = float(law_inv(vc ** 2 / R0, a0)); dM31 = 785 * KPC; geN = G * 1e11 * MSUN / dM31 ** 2; ge = float(law(geN, a0))
    vobs = 229.1e3
    SYS[f]["MW disc"].append(sysrow(M_b=Mb, sigma=vobs / math.sqrt(2) / 1e3, rho_b=(gN * R0 ** 2 / G / MSUN) / (4 / 3 * math.pi * (R0 / PC) ** 3), x=gN / a0, e=ge / a0,
                                    Phi=G * Mb * MSUN / R0 / CL ** 2, f_hot=0.0, kT=0.0, N_orb=tdyn_norb(R0, vobs), rho_env=3 * ge / (4 * math.pi * G * dM31) * PC ** 3 / MSUN,
                                    H=0.0, f_b=gN / (vobs ** 2 / R0), O=0.0, name="MW"))
    # ---- LG dwarfs (X1 CSV)
    for x in X1ROWS:
        if x["footing"] != f:
            continue
        cls = {v: k for k, v in X1KEY.items()}.get(x["cls"])
        if cls is None:
            continue
        M = 10 ** float(x["logMstar"]); rh = float(x["rh_pc"]) * PC; r12 = 4 / 3 * rh; s = float(x["sigma"]) * 1e3
        xe = float(x["x_e_mid"]); d = float(x["d_host_kpc"]) * KPC
        ge = xe * a0; gNh = float(law_inv(ge, a0))
        SYS[f][cls].append(sysrow(M_b=M, sigma=s / 1e3, rho_b=(M / 2) / (4 / 3 * math.pi * (r12 / PC) ** 3), x=G * (M / 2) * MSUN / r12 ** 2 / a0, e=xe,
                                  Phi=(G * M * MSUN / math.sqrt(r12 ** 2 + rh ** 2) + gNh * d) / CL ** 2, f_hot=0.0, kT=0.0, N_orb=tdyn_norb(r12, math.sqrt(3) * s),
                                  rho_env=3 * ge / (4 * math.pi * G * d) * PC ** 3 / MSUN, H=0.0 if cls == "LG field" else 1.0,
                                  f_b=(G * (M / 2) * MSUN / r12) / (3 * s ** 2), O=0.0, name=x["name"], y_rec=float(x["y_plummer"])))
    # ---- Coma UDGs (S1 CSV)
    for x in csv.DictReader(open(os.path.join(RB, "S1_v3_hosted_small", "s1_coma_per_galaxy.csv"))):
        if x["footing"] != f:
            continue
        M = float(x["Mstar"]); Re = float(x["Re_kpc"]) * KPC; r12 = 4 / 3 * Re; s = float(x["sigma"]) * 1e3
        xe = float(x["x_e_dmean"]); d = float(x["d_mean_kpc"]) * KPC; ge = xe * a0; gNh = float(law_inv(ge, a0))
        SYS[f]["Coma UDGs"].append(sysrow(M_b=M, sigma=s / 1e3, rho_b=(M / 2) / (4 / 3 * math.pi * (r12 / PC) ** 3), x=G * (M / 2) * MSUN / r12 ** 2 / a0, e=xe,
                                          Phi=(G * M * MSUN / math.sqrt(r12 ** 2 + Re ** 2) + gNh * d) / CL ** 2, f_hot=0.0, kT=0.0, N_orb=tdyn_norb(r12, math.sqrt(3) * s),
                                          rho_env=3 * ge / (4 * math.pi * G * d) * PC ** 3 / MSUN, H=1.0, f_b=(G * (M / 2) * MSUN / r12) / (3 * s ** 2), O=0.0, name=x["name"]))
    # ---- TDGs (Lelli+15), e from P4's solved host field
    gep = {p["name"]: p["ge"] for p in P4["T5"]["footings"][f]["L24"]["T_points"]} if "T_points" in P4["T5"]["footings"][f]["L24"] else \
          {p["name"]: p["ge"] for p in P4["T5"]["footings"][f]["L0"]["T_points"]}
    for o in TDG:
        R = o["R"] * KPC; V = o["V"] * 1e3; d = o["Dp"] * KPC; ge = gep[o["name"]] * a0; gNh = float(law_inv(ge, a0))
        SYS[f]["TDGs"].append(sysrow(M_b=o["M"], sigma=V / math.sqrt(2) / 1e3, rho_b=o["M"] / (4 / 3 * math.pi * (R / PC) ** 3), x=G * o["M"] * MSUN / R ** 2 / a0,
                                     e=ge / a0, Phi=(G * o["M"] * MSUN / R + gNh * d) / CL ** 2, f_hot=0.0, kT=0.0, N_orb=o["tmo"],
                                     rho_env=3 * ge / (4 * math.pi * G * d) * PC ** 3 / MSUN, H=1.0, f_b=(G * o["M"] * MSUN / R) / V ** 2, O=1.0, name=o["name"]))
    # ---- DF2/DF4 (CFG657 inputs), e from P4's solved host field
    gup = {p["name"]: p["ge"] for p in P4["T5"]["footings"][f]["L0"]["U_points"]}
    for nm, o in DFG.items():
        Re = o["Re"] * KPC; r12 = 4 / 3 * Re; s = o["sig"] * 1e3
        dra = math.radians(o["ra"] - NGC1052[0]) * math.cos(math.radians(o["dec"])); dde = math.radians(o["dec"] - NGC1052[1])
        d = math.hypot(dra, dde) * o["D"] * MPC; ge = gup[nm] * a0; gNh = float(law_inv(ge, a0)); M = o["Ms"]
        SYS[f]["DF2/DF4"].append(sysrow(M_b=M, sigma=o["sig"], rho_b=(M / 2) / (4 / 3 * math.pi * (r12 / PC) ** 3), x=G * (M / 2) * MSUN / r12 ** 2 / a0, e=gup[nm],
                                        Phi=(G * M * MSUN / math.sqrt(r12 ** 2 + Re ** 2) + gNh * d) / CL ** 2, f_hot=0.0, kT=0.0, N_orb=tdyn_norb(r12, math.sqrt(3) * s, o["age"]),
                                        rho_env=3 * ge / (4 * math.pi * G * d) * PC ** 3 / MSUN, H=1.0, f_b=(G * (M / 2) * MSUN / r12) / (3 * s ** 2), O=1.0, name=nm))

P(f"  eRASS1 KT available (KT > 0) per tercile: {nKT} of {tn}")
X7J = jl("X7_cluster_core_significance/x7_analysis_results.json")
for f in FOOTS:
    qA = [b["MID"]["A_CAL"] for b in X7J["bins"][f"quintiles|{f}|h0672"]]
    P(f"  record (X7, read-only) [{f}] quintile A_MID CAL h0672: {' / '.join(f'{a:.3f}' for a in qA)}; X7 V2 {X7J['V2']}, step dchi2 {X7J['V2_dchi2']}")
# cluster e band (X2 (c1) noclu / (c2) maxclu y_e), background bands
CL_E = {"canonical": (7.8e-4, 6.4e-3), "alt": (6.5e-4, 5.3e-3)}
TB = 2.725 * 1101 * KB / KEV
BG = {"rho_b": (OMB * RHOC, OMB * RHOC * 1101 ** 3), "x": (0.0, 15.6), "e": (0.0, 0.0), "kT": (TB, TB), "f_hot": (0.0, 0.0), "N_orb": (0.0, 0.0),
      "rho_env": (RHOM, RHOM * 1101 ** 3), "H": (0.0, 0.0), "O": (0.0, 0.0)}


def interval(vals, strict=False):
    v = np.array([u for u in vals if np.isfinite(u)], float)
    if v.size == 0:
        return None
    if strict or v.size < 3:
        return (float(v.min()), float(v.max()), float(np.median(v)), int(v.size))
    return (float(np.percentile(v, 16)), float(np.percentile(v, 84)), float(np.median(v)), int(v.size))


def class_intervals(f, strict=False):
    I = {}
    for nm in CLASSES:
        I[nm] = {}
        for v in VN + VREP:
            if nm == "Cosmic background":
                b = BG.get(v); I[nm][v] = None if b is None else (b[0], b[1], math.sqrt(max(b[0], 1e-300) * max(b[1], 1e-300)) if b[0] > 0 else b[1], 0)
                continue
            if v == "e" and nm.startswith("Clusters"):
                lo, hi = CL_E[f]; I[nm][v] = (lo, hi, math.sqrt(lo * hi), 0); continue
            I[nm][v] = interval([r[v] for r in SYS[f][nm]], strict)
    return I


INT = {(f, s): class_intervals(f, s) for f in FOOTS for s in (False, True)}

# ---------- printed class table (medians and 16-84 % ranges)
for f in FOOTS:
    P(f"\n  [{f}] class medians (16-84 % or min-max for N < 3; bands for clusters' e and the background)")
    P("  " + f"{'class':18s}" + "".join(f"{v:>22s}" for v in VN + VREP))
    for nm in CLASSES:
        cells = []
        for v in VN + VREP:
            iv = INT[(f, False)][nm][v]
            cells.append(f"{'N/A':>22s}" if iv is None else f"{iv[2]:9.3g} [{iv[0]:.2g},{iv[1]:.2g}]".rjust(22))
        P("  " + f"{nm:18s}" + "".join(cells))

# =====================================================================================================  rank rule


def L10(v):
    return math.log10(v) if v > 0 else -30.0


def tr(iv, var):
    if iv is None:
        return None
    if var in ("H", "O"):
        return (iv[0], iv[1], iv[2])
    return (L10(iv[0]), L10(iv[1]), L10(iv[2]) if iv[2] > 0 else -30.0)


def labels(T, scheme):
    L = {}
    for nm in CLASSES:
        Z = T[nm]["Z"]
        if scheme == "LS":
            L[nm] = "EXTRA" if Z >= 2 else ("NONE" if Z < 1 else "AMBIG")
        else:
            L[nm] = "EXTRA" if nm in ("Clusters T2", "Clusters T3", "Cosmic background", "MW classical", "MW ultra-faint", "bright M31", "M31 others",
                                      "Crater II", "Antlia II", "Coma UDGs") else "NONE"
    return L


def rank_test(var, I, T, L):
    """returns dict: status, direction, V*, offenders, graded."""
    dec = [nm for nm in CLASSES if L[nm] in ("EXTRA", "NONE")]
    na = [nm for nm in dec if tr(I[nm][var], var) is None]
    na_bound = [nm for nm in na if nm != "Cosmic background"]
    use = [nm for nm in dec if nm not in na]
    X = {nm: tr(I[nm][var], var) for nm in use}
    EX = [nm for nm in use if L[nm] == "EXTRA"]; NO = [nm for nm in use if L[nm] == "NONE"]
    res = dict(var=var, n_extra=len(EX), n_none=len(NO), not_placeable=na)
    if not EX or not NO:
        res.update(status="NO CONTRAST"); return res
    best = None
    edges = sorted({X[n][0] for n in use} | {X[n][1] for n in use})
    cands = [edges[0] - 1] + [0.5 * (a + b) for a, b in zip(edges[:-1], edges[1:])] + [edges[-1] + 1]
    for dirn in ("UP", "DOWN"):
        for t in cands:
            if dirn == "UP":
                off = [n for n in NO if X[n][1] >= t] + [n for n in EX if X[n][0] <= t]
            else:
                off = [n for n in EX if X[n][1] >= t] + [n for n in NO if X[n][0] <= t]
            if best is None or len(off) < len(best[2]):
                best = (dirn, t, off)
    gapU = max(X[n][1] for n in NO) < min(X[n][0] for n in EX)
    gapD = max(X[n][1] for n in EX) < min(X[n][0] for n in NO)
    res.update(best_direction=best[0], best_threshold_log=best[1], offenders=best[2], n_offenders=len(best[2]))
    if gapU or gapD:
        dirn = "UP" if gapU else "DOWN"
        lo_edge = max(X[n][1] for n in NO) if gapU else max(X[n][1] for n in EX)
        hi_edge = min(X[n][0] for n in EX) if gapU else min(X[n][0] for n in NO)
        vstar = 0.5 * (lo_edge + hi_edge)
        viol = []
        for a, b in itertools.permutations(EX, 2):
            va, vb = X[a][2], X[b][2]
            closer = (va < vb) if dirn == "UP" else (va > vb)     # a closer to V* than b
            if closer and T[a]["E"] - T[b]["E"] > math.hypot(T[a]["s"], T[b]["s"]):
                viol.append(f"{a} (E {T[a]['E']:+.2f}) > {b} (E {T[b]['E']:+.2f})")
        graded = not viol
        st = "SEPARATES" if graded else "SEPARATES, NOT GRADED"
        if na_bound:
            st += " (INCOMPLETE)"
        res.update(status=st, direction=dirn, vstar_log=vstar, gap_log=(lo_edge, hi_edge), grading_violations=viol)
    else:
        res.update(status="FAILS" + (" (INCOMPLETE)" if na_bound else ""))
    return res


def two_var(v1, v2, I, L):
    dec = [nm for nm in CLASSES if L[nm] in ("EXTRA", "NONE")]
    use = [nm for nm in dec if tr(I[nm][v1], v1) is not None and tr(I[nm][v2], v2) is not None]
    na_bound = [nm for nm in dec if nm not in use and nm != "Cosmic background"]
    EX = [nm for nm in use if L[nm] == "EXTRA"]; NO = [nm for nm in use if L[nm] == "NONE"]
    best = None
    for s1, s2 in itertools.product((1, -1), repeat=2):
        B = {}
        for nm in use:
            a = tr(I[nm][v1], v1); b = tr(I[nm][v2], v2)
            B[nm] = ((a[0], a[1]) if s1 > 0 else (-a[1], -a[0]), (b[0], b[1]) if s2 > 0 else (-b[1], -b[0]))
        e1 = sorted({B[n][0][0] for n in use} | {B[n][0][1] for n in use}); e2 = sorted({B[n][1][0] for n in use} | {B[n][1][1] for n in use})
        c1 = [e1[0] - 1] + [0.5 * (a + b) for a, b in zip(e1[:-1], e1[1:])] + [e1[-1] + 1]
        c2 = [e2[0] - 1] + [0.5 * (a + b) for a, b in zip(e2[:-1], e2[1:])] + [e2[-1] + 1]
        for comb in ("AND", "OR"):
            for a in c1:
                for b in c2:
                    off = []
                    for n in EX:
                        s_ok = (B[n][0][0] > a and B[n][1][0] > b) if comb == "AND" else (B[n][0][0] > a or B[n][1][0] > b)
                        if not s_ok:
                            off.append(n)
                    for n in NO:
                        v_ok = (B[n][0][1] <= a or B[n][1][1] <= b) if comb == "AND" else (B[n][0][1] <= a and B[n][1][1] <= b)
                        if not v_ok:
                            off.append(n)
                    if best is None or len(off) < len(best["offenders"]):
                        best = dict(s1=s1, s2=s2, comb=comb, a=a, b=b, offenders=off)
                        if not off:
                            break
                if best and not best["offenders"]:
                    break
            if best and not best["offenders"]:
                break
        if best and not best["offenders"]:
            break
    best.update(pair=(v1, v2), separates=not best["offenders"], incomplete=na_bound)
    return best


def run_cell(f, base, scheme, strict, T=None):
    T = T or ETAB[(f, base)]
    L = labels(T, scheme); I = INT[(f, strict)]
    single = {v: rank_test(v, I, T, L) for v in VN}
    rep = {v: rank_test(v, I, T, L) for v in VREP}
    return T, L, single, rep, I


def is_sel(r):
    return r["status"] == "SEPARATES"


RESULTS = {"single": {}, "two": {}, "labels": {}, "reported_only": {}}
P("\n=== STEP 1: rank test (primary: B_iso, L-S labels, 16-84 % intervals, h 0.672)")
for f in FOOTS:
    T, L, single, rep, I = run_cell(f, "iso", "LS", False)
    RESULTS["labels"][f] = L
    P(f"\n  [{f}] labels: EXTRA {[n for n in CLASSES if L[n] == 'EXTRA']}")
    P(f"  [{f}]         NONE  {[n for n in CLASSES if L[n] == 'NONE']}")
    P(f"  [{f}]         AMBIG {[n for n in CLASSES if L[n] == 'AMBIG']}")
    for v in VN + VREP:
        r = single.get(v) or rep.get(v)
        extra = ""
        if r["status"].startswith("SEPARATES"):
            extra = f" dir {r['direction']} V* = 10^{r['vstar_log']:.3f} = {10 ** r['vstar_log']:.4g}" if v not in ("H", "O") else f" dir {r['direction']} at {r['vstar_log']:.2f}"
            if r.get("grading_violations"):
                extra += f"; grading violations {r['grading_violations']}"
        P(f"    {v:8s} {r['status']:32s} best dir {r.get('best_direction')} offenders ({r.get('n_offenders')}): {r.get('offenders')}{extra}"
          + (f"; not placeable {r['not_placeable']}" if r["not_placeable"] else "") + ("   [REPORTED ONLY]" if v in VREP else ""))
    RESULTS["single"][f] = single; RESULTS["reported_only"][f] = rep

any_single = {f: [v for v, r in RESULTS["single"][f].items() if is_sel(r)] for f in FOOTS}

# ---------- two-variable search (only if every single V fails on that footing)
VV = VN
for f in FOOTS:
    if any_single[f]:
        P(f"\n  [{f}] a single V separates: {any_single[f]}; two-variable search not run (frozen)")
        continue
    T, L, _, _, I = run_cell(f, "iso", "LS", False)
    P(f"\n  [{f}] TWO-VARIABLE SEARCH (verdict-bearing pairs, axis-aligned AND/OR, 16-84 % boxes)")
    res = [two_var(a, b, I, L) for a, b in itertools.combinations(VV, 2)]
    sep = [r for r in res if r["separates"] and not r["incomplete"]]
    sep_inc = [r for r in res if r["separates"] and r["incomplete"]]
    res.sort(key=lambda r: (len(r["offenders"]), r["pair"]))
    for r in res[:12]:
        P(f"    {r['pair'][0]:>8s} x {r['pair'][1]:<8s} {'SEPARATES' if r['separates'] else 'fails':9s} rule ({'+' if r['s1'] > 0 else '-'}{r['pair'][0]} > {r['a']:.2f}) {r['comb']} "
          f"({'+' if r['s2'] > 0 else '-'}{r['pair'][1]} > {r['b']:.2f}) offenders {r['offenders']}" + (f" INCOMPLETE (N/A: {r['incomplete']})" if r["incomplete"] else ""))
    rep2 = [two_var(a, b, I, L) for a in VREP for b in VN + VREP if a != b]
    rep2.sort(key=lambda r: (len(r["offenders"]), r["pair"]))
    P(f"  [{f}] reported-only pairs (with O or f_b), best 6:")
    for r in rep2[:6]:
        P(f"    {r['pair'][0]:>8s} x {r['pair'][1]:<8s} {'SEPARATES' if r['separates'] else 'fails':9s} rule ({'+' if r['s1'] > 0 else '-'}{r['pair'][0]} > {r['a']:.2f}) {r['comb']} "
          f"({'+' if r['s2'] > 0 else '-'}{r['pair'][1]} > {r['b']:.2f}) offenders {r['offenders']}" + (f" INCOMPLETE (N/A: {r['incomplete']})" if r["incomplete"] else ""))
    RESULTS["two"][f] = dict(separating=[r["pair"] for r in sep], separating_incomplete=[r["pair"] for r in sep_inc],
                             best=[dict(pair=r["pair"], offenders=r["offenders"], rule=f"{r['s1']}{r['pair'][0]}>{r['a']:.3f} {r['comb']} {r['s2']}{r['pair'][1]}>{r['b']:.3f}",
                                        incomplete=r["incomplete"]) for r in res[:12]],
                             reported_best=[dict(pair=r["pair"], offenders=r["offenders"], incomplete=r["incomplete"]) for r in rep2[:6]])

# ---------- verdict
def verdict_for(fsel, ftwo):
    cls = {}
    for f in FOOTS:
        if fsel[f]:
            cls[f] = "SINGLE"
        elif ftwo.get(f, {}).get("separating"):
            cls[f] = "TWO"
        else:
            cls[f] = "NONE"
    return cls


nE = {f: sum(1 for n in CLASSES if RESULTS["labels"][f][n] == "EXTRA") for f in FOOTS}
nN = {f: sum(1 for n in CLASSES if RESULTS["labels"][f][n] == "NONE") for f in FOOTS}
cls = verdict_for(any_single, RESULTS["two"])
if STOP:
    VERDICT = "UNDECIDED (step-0 stop rule)"
elif any(nE[f] < 2 or nN[f] < 2 for f in FOOTS):
    VERDICT = "UNDECIDED (too few decisive classes)"
elif cls["canonical"] != cls["alt"]:
    VERDICT = f"UNDECIDED (footings disagree: canonical {cls['canonical']}, alt {cls['alt']})"
elif cls["canonical"] == "SINGLE":
    common = [v for v in any_single["canonical"] if v in any_single["alt"]]
    VERDICT = "SINGLE SELECTOR FOUND: " + ", ".join(f"{v} (V* {10 ** RESULTS['single']['canonical'][v]['vstar_log']:.3g} / {10 ** RESULTS['single']['alt'][v]['vstar_log']:.3g})" for v in common) if common \
        else f"UNDECIDED (different single V per footing: {any_single})"
elif cls["canonical"] == "TWO":
    common = [p for p in RESULTS["two"]["canonical"]["separating"] if p in RESULTS["two"]["alt"]["separating"]]
    VERDICT = "ONLY TWO-VARIABLE SEPARATION: " + ", ".join(f"({a}, {b})" for a, b in common) if common else "UNDECIDED (different pairs per footing)"
else:
    VERDICT = "NO LOW-DIMENSIONAL SELECTOR"
P(f"\n=== VERDICT (primary): {VERDICT}")

# ---------- qualifiers (reported)
P("\n=== QUALIFIERS (reported, no verdict weight)")
QUAL = {}
for tag, (base, scheme, strict, use686) in {"B_EFE": ("efe", "LS", False, False), "L-B": ("iso", "LB", False, False), "strict": ("iso", "LS", True, False),
                                             "h0686": ("iso", "LS", False, True), "B_EFE+L-B": ("efe", "LB", False, False)}.items():
    QUAL[tag] = {}
    for f in FOOTS:
        T = ETAB_686[f] if use686 else None
        T, L, single, rep, I = run_cell(f, base, scheme, strict, T)
        sel = [v for v, r in single.items() if is_sel(r)]
        nearly = {v: (r["status"], r.get("n_offenders"), r.get("offenders")) for v, r in single.items()}
        QUAL[tag][f] = dict(selectors=sel, labels=L, per_V={v: dict(status=s, n_off=n, offenders=o) for v, (s, n, o) in nearly.items()})
        P(f"  {tag:10s} [{f}] EXTRA {[n for n in CLASSES if L[n] == 'EXTRA']}")
        P(f"  {tag:10s} [{f}] separating single V: {sel if sel else 'none'}; fewest offenders: "
          + ", ".join(f"{v}:{n}" for v, (s, n, o) in sorted(nearly.items(), key=lambda kv: kv[1][1] if kv[1][1] is not None else 99)[:4]))

P("\n  B_EFE two-variable search (reported only), best 4 per footing:")
QUAL["B_EFE"]["two_var_best"] = {}
for f in FOOTS:
    T, L, _, _, I = run_cell(f, "efe", "LS", False)
    rr = sorted([two_var(a, b, I, L) for a, b in itertools.combinations(VN, 2)], key=lambda r: (len(r["offenders"]), r["pair"]))
    QUAL["B_EFE"]["two_var_best"][f] = [dict(pair=r["pair"], offenders=r["offenders"], incomplete=r["incomplete"], separates=r["separates"]) for r in rr[:4]]
    for r in rr[:4]:
        P(f"    [{f}] {r['pair'][0]:>8s} x {r['pair'][1]:<8s} {'SEPARATES' if r['separates'] else 'fails':9s} rule ({'+' if r['s1'] > 0 else '-'}{r['pair'][0]} > {r['a']:.2f}) {r['comb']} "
          f"({'+' if r['s2'] > 0 else '-'}{r['pair'][1]} > {r['b']:.2f}) offenders {r['offenders']}" + (f" INCOMPLETE (N/A: {r['incomplete']})" if r["incomplete"] else ""))

# =====================================================================================================  checks K2-K5
P("\n=== CHECKS")
# K2: oracle from raw tables (re-read, not from the class table)
k2 = {}
for f in FOOTS:
    T = ETAB[(f, "iso")]; L = labels(T, "LS")
    raw = {}
    for nm, k in X1KEY.items():
        raw[nm] = float(np.median([float(x[ISO]) for x in X1ROWS if x["footing"] == f and x["cls"] == k]))
    X7r = json.load(open(os.path.join(RB, "X7_cluster_core_significance", "x7_analysis_results.json")))["bins"][f"terciles|{f}|h0672"]
    for i in range(3):
        raw[f"Clusters T{i + 1}"] = math.log10(X7r[i]["MID"]["A_CAL"])
    P4r = json.load(open(os.path.join(RB, "P4_v3_galaxy_tiles", "p4_v3_galaxy_tiles_results.json")))["tiles"]
    raw["SPARC small"] = P4r["T1"]["footings"][f]["classes_global_U"]["small"]["mean"]; raw["SPARC large"] = P4r["T1"]["footings"][f]["classes_global_U"]["large"]["mean"]
    raw["Groups"] = 2 * P4r["T3"]["footings"][f]["v3_isolated"]["mean"]
    raw["MW disc"] = math.log10(66.4 / P4r["T4"]["models"]["B1_McMillan17"][f]["F0|L24"]["K_R0"])
    raw["TDGs"] = P4r["T5"]["footings"][f]["T_law_isolated"]["rbar"]; raw["DF2/DF4"] = P4r["T5"]["footings"][f]["U_law_isolated"]["rbar"] / LN10
    raw["Coma UDGs"] = S1[f"{f}|S2 AQUAL isolated L*0 E-W"]["meanE_dex"]; raw["UMa members"] = U1["footings"][f]["A4"]["any_radius"]["per_galaxy"]["mean"]
    raw["Cosmic background"] = math.log10(1 + OCB)
    I = {nm: {"oracle": (10 ** -raw[nm], 10 ** -raw[nm], 10 ** -raw[nm], 1)} for nm in CLASSES}
    r = rank_test("oracle", I, T, L)
    k2[f] = r
    P(f"    K2 [{f}] oracle 10^-E_raw: {r['status']} (offenders {r.get('offenders')})")
check("K2", all(k2[f]["status"] == "SEPARATES" for f in FOOTS), {f: k2[f]["status"] for f in FOOTS}, "SEPARATES on both footings", "positive control of the rank machinery")
# K3: synthetic unit tests
CLS0 = CLASSES


def synth(vals, Es, Zs):
    T = {nm: dict(E=Es[i], s=0.05, Z=Zs[i]) for i, nm in enumerate(CLS0)}
    I = {nm: {"v": (vals[i], vals[i] * 1.1, vals[i] * 1.05, 3)} for i, nm in enumerate(CLS0)}
    return T, I


nC = len(CLS0)
Zs = [3.0 if i % 2 else 0.0 for i in range(nC)]
Es_g = [0.1 * i if i % 2 else 0.0 for i in range(nC)]
vals_sep = [10.0 ** (5 + i) if i % 2 else 10.0 ** (i * 0.1) for i in range(nC)]
T, I = synth(vals_sep, Es_g, Zs); r1 = rank_test("v", I, T, labels(T, "LS"))
vals_mix = [10.0 ** (i % 5) for i in range(nC)]
T, I = synth(vals_mix, Es_g, Zs); r2 = rank_test("v", I, T, labels(T, "LS"))
Es_bad = [(1.0 - 0.1 * i) if i % 2 else 0.0 for i in range(nC)]
T, I = synth(vals_sep, Es_bad, Zs); r3 = rank_test("v", I, T, labels(T, "LS"))
check("K3", r1["status"] == "SEPARATES" and r2["status"].startswith("FAILS") and r3["status"] == "SEPARATES, NOT GRADED",
      f"{r1['status']} / {r2['status']} / {r3['status']}", "SEPARATES / FAILS / SEPARATES, NOT GRADED")
# K4: identities
gg = np.logspace(-14, -8, 50); rt = max(float(np.max(np.abs(law(law_inv(gg, a0), a0) / gg - 1))) for a0 in A0.values())
sk = math.sqrt(KEV / (MU * MP)) / 1e3
k4b = abs(beta_M(2.0, 1.0) - (2.0 - math.atan(2.0))) < 1e-12
check("K4", rt <= 1e-12 and abs(sk / 399.6 - 1) <= 0.01 and k4b, f"law round trip {rt:.1e}; sigma(1 keV) {sk:.1f} km/s; beta-model M ok {k4b}",
      "<=1e-12; 399.6 +- 1 % (A1); exact")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
check("K5", rss < 1.0, f"{rss:.3f} GB", "< 1 GB")

# =====================================================================================================  outputs
ok_all = all(c["ok"] for c in CHECKS.values())
P(f"\nchecks {sum(c['ok'] for c in CHECKS.values())}/{len(CHECKS)}; runtime {time.time() - T0:.1f} s; peak RSS {rss:.3f} GB")


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not math.isfinite(float(o)) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    return o


OUT = dict(lane="X19_selector_rank_test", criteria="8960ea2285", amendment_A1="0fc9bade54", amendment_A2="post-result implementation fixes (K0 references, X1 median comparison reported)", mutate=MUT, verdict=VERDICT, per_footing_class=cls,
           E_table={f"{f}|{b}": ETAB[(f, b)] for f in FOOTS for b in ("iso", "efe")}, E_table_h0686=ETAB_686,
           intervals={f"{f}|{'strict' if s else 'p16_84'}": INT[(f, s)] for f in FOOTS for s in (False, True)},
           results=RESULTS, qualifiers=QUAL, checks=CHECKS, nKT=nKT, tercile_n=tn, tercile_median_Mgas500=tmed, U0=U0, n_UMa=len(UMA),
           k1=k1, k1_reported=k1rep, runtime_s=time.time() - T0, peak_rss_GB=rss)
json.dump(clean(OUT), open(os.path.join(HERE, f"x19_selector_rank_test_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"x19_selector_rank_test{TAG}.out"), "w").write("\n".join(OUTL).replace(REPO, "<repo>").replace(os.path.dirname(REPO), "<parent>") + "\n")
with open(os.path.join(HERE, f"x19_classes{TAG}.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["footing", "class", "E_iso", "s_iso", "Z_iso", "label_LS", "E_efe", "Z_efe"] + [f"{v}_{q}" for v in VN + VREP for q in ("med", "p16", "p84", "N")])
    for f in FOOTS:
        for nm in CLASSES:
            Ti = ETAB[(f, "iso")][nm]; Te = ETAB[(f, "efe")][nm]
            row = [f, nm, Ti["E"], Ti["s"], Ti["Z"], RESULTS["labels"][f][nm], Te["E"], Te["Z"]]
            for v in VN + VREP:
                iv = INT[(f, False)][nm][v]
                row += ["NA"] * 4 if iv is None else [iv[2], iv[0], iv[1], iv[3]]
            w.writerow(row)
sys.exit(0 if ok_all else 1)
