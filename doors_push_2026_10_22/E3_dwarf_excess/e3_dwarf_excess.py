"""E3_dwarf_excess -- audit of the sub-threshold satellite excess (+2.15 dex above Newton) and the framework's native
bound-cold capacity.  Criteria: FROZEN_CRITERIA.md (committed alone first, 5686635887).

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 e3_dwarf_excess.py            -> e3_dwarf_excess.out, e3_dwarf_excess_results.json,
                                                                           e3_per_system.csv, e3_inputs_ledger.csv
      OMP_NUM_THREADS=1 nice -n 10 python3 e3_dwarf_excess.py --mutate   -> *_MUTATE.*  (sigma := screened prediction)
Deterministic (seeded), no network, seconds.  kappa = 1/2 FITTED; not theory closed."""
import csv, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(REPO, "real_research", "data")
CFG = os.path.join(REPO, "campaign_fresh_gravity")
MUT = "--mutate" in sys.argv
SFX = "_MUTATE" if MUT else ""

# ------------------------------------------------------------------ constants (sources in the README ledger)
G, MSUN, PC = 6.67430e-11, 1.989e30, 3.0856775814913673e16
KPC = 1e3 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}        # BRIEF footings; kappa = 1/2 FITTED
LSTAR_PC = 24.0                                          # CFG820 lower bound (least screening allowed)
LSTAR_HI_PC = 90.0                                       # D8 window upper edge (reported)
SUP = 5.364                                              # cold per baryon (Planck Omega_c/Omega_b; CFG886) -- LCDM-fit, flagged
FRET_CENSUS = 0.10                                       # CFG416/556 census floor (CFG809 fret_of) -- LCDM-PROCESSED
MHOST = {"MW": 6.0e10, "M31": 1.0e11}                    # MW: CFG332; M31: labelled external (as D2)
ST_s = np.array([0.01, 0.1, 0.3, 1, 3, 10, 100, 1000])   # CFG691 screening table (as used by CFG820)
ST_S = np.array([0.0050, 0.048, 0.134, 0.358, 0.663, 0.894, 0.990, 0.998999])
NMC, NBOOT = 2000, 4000
RNG = np.random.default_rng(20261022)

OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

def fl(x):
    try:
        v = float(x); return v if math.isfinite(v) else None
    except Exception:
        return None

def nu(y):
    y = np.maximum(np.asarray(y, float), 1e-30)
    return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y))

def Sfun(s):
    s = np.asarray(s, float)
    out = np.interp(np.log(np.clip(s, 0.01, 1000)), np.log(ST_s), ST_S)
    out = np.where(s <= 0.01, s / 2, out)
    return np.where(s >= 1000, 1 - 1 / np.maximum(s, 1e-300), out)

def B_scr(Ms, r12, a0, Lstar_pc):
    """CFG820 recipe: 1 + S(s)(nu(y)-1); Ms in Msun, r12 in m. Lstar_pc None -> unscreened law; inf -> Newton."""
    gb = G * (Ms / 2) * MSUN / r12 ** 2
    nv = nu(gb / a0)
    if Lstar_pc is None:
        return nv
    if np.isinf(Lstar_pc):
        return np.ones_like(nv)
    rM = np.sqrt(G * Ms * MSUN / a0)
    lg = (Lstar_pc * PC) ** 2 / (2 * rM)
    return 1 + Sfun(r12 / lg) * (nv - 1)

# ------------------------------------------------------------------ data
def load_lvd():
    rows = []
    for fn, host in (("lvd_dwarf_mw.csv", "MW"), ("lvd_dwarf_m31.csv", "M31"), ("lvd_dwarf_local_field.csv", "field")):
        for r in csv.DictReader(open(os.path.join(DATA, "dsph", fn))):
            s = fl(r.get("vlos_sigma"))
            rh = fl(r.get("rhalf_sph_physical")) or fl(r.get("rhalf_physical"))
            ms = fl(r.get("mass_stellar")); mv = fl(r.get("M_V"))
            if not s or s <= 0 or not rh or rh <= 0:
                continue
            if ms is None and mv is not None:
                ms = 0.4 * (4.83 - mv) + 0.301
            if ms is None:
                continue
            rhe = fl(r.get("rhalf_sph_physical_em")) if fl(r.get("rhalf_sph_physical")) else fl(r.get("rhalf_physical_em"))
            rhp = fl(r.get("rhalf_sph_physical_ep")) if fl(r.get("rhalf_sph_physical")) else fl(r.get("rhalf_physical_ep"))
            rows.append(dict(name=r["name"], host=host, sigma=s, sem=fl(r.get("vlos_sigma_em")) or 0.1 * s,
                             sep=fl(r.get("vlos_sigma_ep")) or 0.1 * s, ul=bool(r.get("vlos_sigma_ul")),
                             rh=rh, rhem=rhe or 0.1 * rh, rhep=rhp or 0.1 * rh, logms=ms,
                             dmem=fl(r.get("distance_modulus_em")) or 0.1, dmep=fl(r.get("distance_modulus_ep")) or 0.1,
                             dhost=fl(r.get("distance_host")), mhi=fl(r.get("mass_HI")),
                             mwolf=fl(r.get("mass_dynamical_wolf")), ref=r.get("ref_vlos", "")))
    return rows

ALL = load_lvd()
ARR = list(csv.DictReader(open(os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}
arr_f07 = {r["lvd_name"]: float(r["sig_f07"]) / float(r["sig_f0"]) for r in ARR}
med_free = float(np.median(list(arr_free.values()))); med_f07 = float(np.median(list(arr_f07.values())))
GEH = {}
for r in csv.DictReader(open(os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "geha_vs_lvd_match.csv"))):
    if r.get("geha_sigma_resolved") == "1" and fl(r.get("geha_sigma")):
        GEH[r["lvd_name"]] = (float(r["geha_sigma"]), fl(r.get("geha_e_sigma_ll")) or 0.1, fl(r.get("geha_e_sigma_ul")) or 0.1)
# largest dataset-to-dataset sigma change on disk (LVD vs DEIMOS; non-equilibrium / dataset yardstick)
pair_ratios = {n: max(v[0] / s["sigma"], s["sigma"] / v[0]) for n, v in GEH.items() for s in ALL if s["name"] == n}

D2R = json.load(open(os.path.join(REPO, "doors_push_2026_10_22", "D2_wide_binary_fork", "d2_wide_binary_fork_results.json")))["R7"]

R = dict(lane="E3_dwarf_excess", mutate=MUT, constants=dict(G=G, MSUN=MSUN, PC=PC, a0=A0, Lstar_pc=LSTAR_PC, sup=SUP,
         fret_census=FRET_CENSUS, mhost=MHOST, nmc=NMC, nboot=NBOOT, seed=20261022))
CHK = []
def ck(k, ok, val, thr, what):
    CHK.append((k, bool(ok))); P(f"{k} {'PASS' if ok else 'FAIL'} {val} {thr}  ({what})")

def sample(a0):
    mcrit = a0 * (LSTAR_PC * PC) ** 2 / G / MSUN
    return [r for r in ALL if r["logms"] < math.log10(mcrit)], mcrit

# ------------------------------------------------------------------ per-system Monte Carlo
def split_normal(c, em, ep, n):
    z = RNG.standard_normal(n)
    return c + np.where(z < 0, z * em, z * ep)

def build(rows, a0, ups=2.0, binmode="none", sig_src="lvd", drop_ul=False, wolf=3.0, mut=False):
    """Return dict of arrays [N, NMC]: log boost, M_dyn, M*, r12; plus names."""
    keep = [r for r in rows if not (drop_ul and r["ul"])]
    N = len(keep)
    lb = np.empty((N, NMC)); Md = np.empty((N, NMC)); Ms_ = np.empty((N, NMC)); R12 = np.empty((N, NMC))
    for i, r in enumerate(keep):
        s, sem, sep = r["sigma"], r["sem"], r["sep"]
        if sig_src in ("geha", "lower") and r["name"] in GEH:
            gs, gl, gu = GEH[r["name"]]
            if sig_src == "geha" or gs < s:
                s, sem, sep = gs, gl, gu
        b = 1.0
        if binmode == "free":
            b = arr_free.get(r["name"], med_free)
        elif binmode == "f07":
            b = arr_f07.get(r["name"], med_f07)
        ddm = split_normal(0.0, r["dmem"], r["dmep"], NMC)          # distance-modulus offset
        fD = 10 ** (ddm / 5.0)
        sig = np.abs(split_normal(s, sem, sep, NMC)) * b
        rh = np.abs(split_normal(r["rh"], r["rhem"], r["rhep"], NMC)) * fD
        ms = ups / 2.0 * 10 ** r["logms"] * fD ** 2
        r12 = (4.0 / 3.0) * rh * PC
        if mut:   # inject the screened theory's own prediction (no extra cold)
            sig = np.sqrt(B_scr(ms, r12, a0, LSTAR_PC) * G * (ms / 2) * MSUN / r12 / 3.0) / 1e3
        gobs = wolf * (sig * 1e3) ** 2 / r12
        gbar = G * (ms / 2) * MSUN / r12 ** 2
        lb[i] = np.log10(gobs / gbar); Md[i] = gobs * r12 ** 2 / G / MSUN; Ms_[i] = ms; R12[i] = r12
    return dict(lb=lb, Md=Md, Ms=Ms_, r12=R12, rows=keep)

def central(rows, a0, ups=2.0, binmode="none", wolf=3.0):
    out = []
    for r in rows:
        b = 1.0 if binmode == "none" else (arr_free if binmode == "free" else arr_f07).get(r["name"], med_free if binmode == "free" else med_f07)
        r12 = (4.0 / 3.0) * r["rh"] * PC; ms = ups / 2.0 * 10 ** r["logms"]; sig = r["sigma"] * b * 1e3
        out.append(math.log10(wolf * sig ** 2 / r12 / (G * (ms / 2) * MSUN / r12 ** 2)))
    return np.array(out)

def boot_median(X, n=NBOOT):
    N = X.shape[0]; meds = np.empty(n)
    for k in range(n):
        idx = RNG.integers(0, N, N); col = RNG.integers(0, X.shape[1], N)
        meds[k] = np.median(X[idx, col])
    return float(np.median(meds)), float(np.std(meds)), float(np.percentile(meds, 16)), float(np.percentile(meds, 84))

# ================================================================== K checks on the pipeline
P("E3_dwarf_excess  sub-threshold satellite excess audit + native bound-cold capacity" + ("  [MUTATE: sigma := screened prediction]" if MUT else ""))
P("kappa = 1/2 FITTED; footings canonical 9.3603e-11 / alt 1.1312e-10, never pooled\n")
S_can, MC_can = sample(A0["canonical"])
S_alt, MC_alt = sample(A0["alt"])
raw_c = central(S_can, A0["canonical"])
if MUT:
    Xm = build(S_can, A0["canonical"], mut=True); raw_c = np.median(Xm["lb"], axis=1)
E_raw = float(np.median(raw_c))
ck("K1", len(S_can) == 45 and abs(E_raw - 2.147) <= 0.01, f"N={len(S_can)} E_raw={E_raw:+.3f}", "45 & 2.147+-0.01", "A26 reproduced")
md = [(math.log10(3 * (r["sigma"] * 1e3) ** 2 * (4 / 3) * r["rh"] * PC / G / MSUN) - r["mwolf"]) for r in S_can if r["mwolf"]]
k2 = float(np.median(np.abs(md)))
ck("K2", k2 <= 0.05, f"median|dlog Mdyn|={k2:.4f} (N={len(md)})", "<=0.05", "Wolf mass identity vs LVD mass_dynamical_wolf")
ms0 = np.array([10 ** r["logms"] for r in S_can]); r0 = np.array([(4 / 3) * r["rh"] * PC for r in S_can])
dN = float(np.max(np.abs(np.log10(B_scr(ms0, r0, A0["canonical"], 1e9)))))
dL = float(np.max(np.abs(np.log10(B_scr(ms0, r0, A0["canonical"], 1e-6) / nu(G * ms0 / 2 * MSUN / r0 ** 2 / A0["canonical"])))))
ck("K3", dN <= 1e-3 and dL <= 1e-3, f"Newton-limit {dN:.2e} law-limit {dL:.2e}", "<=1e-3 dex", "screening limits")
la_free = float(np.median(np.log10(list(arr_free.values())))); la_f07 = float(np.median(np.log10(list(arr_f07.values()))))
ck("K4", abs(la_free + 0.068) <= 0.02 and abs(la_f07 + 0.104) <= 0.02, f"free {la_free:+.3f} f0.7 {la_f07:+.3f}",
   "-0.068/-0.104 +-0.02", "Arroyo-Polonio ratios vs CFG257 scoping")
# K5: ceiling code on Draco with CFG823's inputs (M_V, Upsilon 2, Newtonian)
dr = [r for r in csv.DictReader(open(os.path.join(DATA, "dsph", "lvd_dwarf_mw.csv"))) if r["name"] == "Draco"][0]
Mb_d = 2.0 * 10 ** (0.4 * (4.83 - float(dr["M_V"]))); r12_d = (4 / 3) * float(dr["rhalf_sph_physical"]) * PC
Mdyn_d = 3 * (float(dr["vlos_sigma"]) * 1e3) ** 2 * r12_d / G / MSUN
q_d = (Mdyn_d - Mb_d / 2) / (SUP * Mb_d / FRET_CENSUS)
q823 = json.load(open(os.path.join(CFG, "CFG823_dsph_cold_budget", "cfg823_results.json")))["rows"]["2.0|Draco"]["q"]
ck("K5", abs(q_d / q823 - 1) <= 0.02, f"Draco q={q_d:.4f} vs CFG823 {q823:.4f}", "<=2%", "ceiling code")
ck("K6", E_raw >= 1.0, f"E_raw={E_raw:+.3f}", ">=1.0 dex", "pipeline sees the excess")

# ================================================================== PART A
P("\n[A] the +2.15 dex: ingredients and clean recompute (median log10 g_obs/g_bar, sub-threshold sample)")
A = {}
def runA(lab, rows, a0, **kw):
    X = build(rows, a0, mut=MUT, **kw)
    m, s, lo, hi = boot_median(X["lb"])
    A[lab] = dict(N=len(X["rows"]), median=m, sd=s, p16=lo, p84=hi)
    P(f"   {lab:44s} N={len(X['rows']):2d}  E_N = {m:+.3f} +- {s:.3f}   (16-84%: {lo:+.3f} {hi:+.3f})")
    return X
for foot, rows in (("canonical", S_can), ("alt", S_alt)):
    a0 = A0[foot]
    P(f"  footing {foot}: M_crit = {a0 * (LSTAR_PC * PC) ** 2 / G / MSUN:.4e} Msun, N = {len(rows)}")
    runA(f"{foot}|raw A26 (Ups2, LVD sigma, UL as values)", rows, a0)
    Xc = runA(f"{foot}|clean primary (Arroyo free-f)", rows, a0, binmode="free")
    runA(f"{foot}|clean, UL dropped", rows, a0, binmode="free", drop_ul=True)
    runA(f"{foot}|clean Ups 1", rows, a0, ups=1.0, binmode="free")
    runA(f"{foot}|clean Ups 4", rows, a0, ups=4.0, binmode="free")
    runA(f"{foot}|binaries f=0.7", rows, a0, binmode="f07")
    runA(f"{foot}|Geha DEIMOS sigma where resolved", rows, a0, binmode="free", sig_src="geha")
    runA(f"{foot}|Wolf factor 1 (sigma^2/r, not clean)", rows, a0, binmode="free", wolf=1.0)
    runA(f"{foot}|no MC errors check (raw)", rows, a0) if False else None
    Xw = runA(f"{foot}|WORST-CLEAN W (Ups4,f0.7,lower sigma,UL drop)", rows, a0, ups=4.0, binmode="f07", sig_src="lower", drop_ul=True)
    W = A[f"{foot}|WORST-CLEAN W (Ups4,f0.7,lower sigma,UL drop)"]
    Wlo = W["median"] - 2 * W["sd"]
    clsA = "A-SURVIVES" if Wlo >= 1.0 else ("A-REDUCED-BUT-LARGE" if Wlo >= 0.5 else "A-COLLAPSES")
    rawm = A[f"{foot}|raw A26 (Ups2, LVD sigma, UL as values)"]["median"]
    A[f"{foot}|class"] = dict(W_minus_2sd=Wlo, cls=clsA, surviving_fraction=W["median"] / rawm if rawm else None)
    P(f"  -> {foot}: W - 2 sd = {Wlo:+.3f} dex ; surviving fraction W/raw = {W['median'] / rawm:.2f} ; CLASS {clsA}")
nUL = sum(r["ul"] for r in S_can)
P(f"  sigma upper-limit systems in the canonical 45: {nUL}; Arroyo-Polonio systems among them: "
  f"{sum(r['name'] in arr_free for r in S_can)}; Geha resolved among them: {sum(r['name'] in GEH for r in S_can)}")
P(f"  Arroyo medians (sigma ratio): free-f {med_free:.3f} ({2 * math.log10(med_free):+.3f} dex in g_obs), f=0.7 {med_f07:.3f} "
  f"({2 * math.log10(med_f07):+.3f} dex)")
R["A"] = A
R["A_meta"] = dict(n_ul=nUL, arroyo_med_free=med_free, arroyo_med_f07=med_f07, n_arroyo=sum(r['name'] in arr_free for r in S_can),
                   n_geha=sum(r['name'] in GEH for r in S_can), D2_EFE=dict(median_Delta_EFE_below=D2R["median_Delta_EFE_below"],
                   median_Delta_isolated_below=D2R["median_Delta_isolated_below"], variants=D2R["variants"],
                   label="STANDARD-MOND-MACHINERY (1-D QUMOND EFE) + external host masses; not used in the Newton excess"))

# non-equilibrium yardsticks
Xc = build(S_can, A0["canonical"], binmode="free", mut=MUT)
Bs = B_scr(Xc["Ms"], Xc["r12"], A0["canonical"], LSTAR_PC)
infl = np.sqrt(10 ** Xc["lb"] / Bs)                      # sigma inflation needed to reach the screened prediction
infl_med = np.median(infl, axis=1)
maxpair = max(pair_ratios.values()) if pair_ratios else float("nan")
maxpair_name = max(pair_ratios, key=pair_ratios.get) if pair_ratios else ""
nbeat = int(np.sum(infl_med <= maxpair))
# baryon-only Newtonian Jacobi radius (informational)
jac = []
for r in S_can:
    if r["host"] in MHOST and r["dhost"]:
        rJ = r["dhost"] * KPC * (10 ** r["logms"] / (3 * MHOST[r["host"]])) ** (1 / 3)
        jac.append((4 / 3) * r["rh"] * PC / rJ)
fr_J = float(np.mean(np.array(jac) > 1.0)) if jac else float("nan")
P(f"\n  non-equilibrium yardstick: sigma inflation needed to reach the screened prediction (L*=24 pc): median "
  f"{np.median(infl_med):.2f}x (range {infl_med.min():.2f}-{infl_med.max():.2f}); largest dataset-to-dataset sigma change on disk "
  f"(LVD vs DEIMOS) {maxpair:.2f}x ({maxpair_name}); systems within that: {nbeat}/{len(infl_med)}")
P(f"  informational: satellites with r12 beyond the baryon-only Newtonian Jacobi radius: {fr_J * 100:.0f}% of {len(jac)} "
  f"(median r12/r_J {np.median(jac):.2f})")
# reported diagnostic (added during the run, not a frozen line): distance of the data above the SCREENED prediction itself
DSCR = {}
for foot, rows in (("canonical", S_can), ("alt", S_alt)):
    Xd = build(rows, A0[foot], binmode="free", mut=MUT)
    for lab, Lst in (("L*24", LSTAR_PC), ("L*90", LSTAR_HI_PC), ("unscreened law", None)):
        d = Xd["lb"] - np.log10(B_scr(Xd["Ms"], Xd["r12"], A0[foot], Lst))
        m, s, lo, hi = boot_median(d)
        mb, _, _, _ = boot_median(np.log10(B_scr(Xd["Ms"], Xd["r12"], A0[foot], Lst)))
        DSCR[f"{foot}|{lab}"] = dict(median_Delta=m, sd=s, median_log_B=mb)
        P(f"  [diag] {foot:9s} clean data above the {lab:15s} prediction: {m:+.3f} +- {s:.3f} dex (median log B = {mb:+.3f})")
R["A_above_screened_diag"] = DSCR
R["A_noneq"] = dict(sigma_inflation_median=float(np.median(infl_med)), sigma_inflation_min=float(infl_med.min()),
                    sigma_inflation_max=float(infl_med.max()), max_dataset_sigma_ratio=maxpair, max_dataset_name=maxpair_name,
                    n_within=nbeat, frac_beyond_baryon_jacobi=fr_J, median_r12_over_rJ=float(np.median(jac)), n_jacobi=len(jac))

# ================================================================== PART B
P("\n[B] framework-native capacity: extra bound cold needed inside r12 vs the catchment's whole cold supply")
B = {}; PER = []
def qstats(rows, a0, Lst, fret, ups=2.0, binmode="free", sig_src="lvd", drop_ul=False, selfboost=False, tag=""):
    X = build(rows, a0, ups=ups, binmode=binmode, sig_src=sig_src, drop_ul=drop_ul, mut=MUT)
    Bv = B_scr(X["Ms"], X["r12"], a0, Lst)
    Mreq = (X["Md"] / Bv - X["Ms"] / 2) if selfboost else (X["Md"] - X["Ms"] / 2 * Bv)
    mhi = np.array([10 ** r["mhi"] if r["mhi"] else 0.0 for r in X["rows"]])[:, None]
    Mb = X["Ms"] + mhi
    q = np.maximum(Mreq, 1e-30) / (SUP * Mb / fret)
    Lreq = np.maximum(Mreq, 1e-30) / (SUP * Mb)
    lq = np.log10(q)
    m, s, lo, hi = boot_median(lq)
    n2 = int(np.sum(np.percentile(q, 2.5, axis=1) > 1))
    return dict(N=len(X["rows"]), log_median_q=m, sd=s, log_q_p16=lo, log_q_p84=hi, median_q=10 ** m, q_p16=10 ** lo,
                n_q_gt1_2sig=n2, median_Lreq=float(np.median(np.median(Lreq, axis=1))),
                median_Mreq=float(np.median(np.median(Mreq, axis=1))), median_C=float(np.median(np.median(SUP * Mb / fret, axis=1))),
                median_Bscr=float(np.median(np.median(Bv, axis=1)))), X, q, Lreq, Bv
for foot, rows in (("canonical", S_can), ("alt", S_alt)):
    a0 = A0[foot]
    for lab, kw in (("primary L*24 f_ret0.10", dict(Lst=LSTAR_PC, fret=FRET_CENSUS)),
                    ("L*24 f_ret1 (census-free)", dict(Lst=LSTAR_PC, fret=1.0)),
                    ("L*90 f_ret0.10", dict(Lst=LSTAR_HI_PC, fret=FRET_CENSUS)),
                    ("Newton f_ret0.10", dict(Lst=float("inf"), fret=FRET_CENSUS)),
                    ("self-boost variant f_ret0.10 (not record)", dict(Lst=LSTAR_PC, fret=FRET_CENSUS, selfboost=True)),
                    ("Ups4 L*24 f_ret0.10", dict(Lst=LSTAR_PC, fret=FRET_CENSUS, ups=4.0)),
                    ("WORST-CLEAN L*24 f_ret0.10", dict(Lst=LSTAR_PC, fret=FRET_CENSUS, ups=4.0, binmode="f07", sig_src="lower", drop_ul=True)),
                    ("WORST-CLEAN L*24 f_ret1", dict(Lst=LSTAR_PC, fret=1.0, ups=4.0, binmode="f07", sig_src="lower", drop_ul=True))):
        st, X, q, Lreq, Bv = qstats(rows, a0, **kw)
        B[f"{foot}|{lab}"] = st
        P(f"   {foot:9s} {lab:42s} N={st['N']:2d} median q = {st['median_q']:7.3f} (16%: {st['q_p16']:6.3f})  q>1 at 2sig: "
          f"{st['n_q_gt1_2sig']:2d}  L_req {st['median_Lreq']:6.1f}  M_req {st['median_Mreq']:.2e}  B_scr {st['median_Bscr']:.2f}")
        if lab.startswith("primary"):
            for i, r in enumerate(X["rows"]):
                PER.append(dict(footing=foot, name=r["name"], host=r["host"], logMstar=r["logms"], sigma=r["sigma"], rh_pc=r["rh"],
                                sigma_ul=int(r["ul"]), binary_ratio=arr_free.get(r["name"], med_free),
                                arroyo=int(r["name"] in arr_free), geha_sigma=GEH.get(r["name"], (None,))[0],
                                log_boost_newton=float(np.median(X["lb"][i])), B_scr_L24=float(np.median(Bv[i])),
                                M_dyn=float(np.median(X["Md"][i])), M_c_req=float(np.median(Lreq[i]) * SUP * 10 ** r["logms"]),
                                q_fret010=float(np.median(q[i])), q_fret010_p2p5=float(np.percentile(q[i], 2.5)),
                                L_req=float(np.median(Lreq[i])), sigma_inflation_to_screened=float(np.median(np.sqrt(10 ** X["lb"][i] / Bv[i])))))
cls = {}
for foot in ("canonical", "alt"):
    p = B[f"{foot}|primary L*24 f_ret0.10"]; f1 = B[f"{foot}|L*24 f_ret1 (census-free)"]
    if p["q_p16"] > 1:
        c = f"CANNOT (shortfall {math.log10(p['median_q']):+.2f} dex)"
    elif f1["median_q"] > 1:
        c = "UNDECIDABLE (catchment baryon mass / f_ret not native)"
    else:
        c = "CEILING ALLOWS"
    cls[foot] = c
    P(f"  -> {foot}: CLASS {c}  [+ NO MECHANISM IN THE RECORD binds extra cold inside r12: CFG822/842/888/889/959]")
R["B"] = B; R["B_class"] = cls
R["B_mechanism_inventory"] = ["CFG822 free cold from expelled gas lands too far out", "CFG842 host capture 1e-8..1e-5 of need (Liouville)",
                              "CFG888 extra cold gets no law self-boost (Class A Newtonian) / no self-gravity in S3",
                              "CFG889 gate does not retain a clump with orbits", "CFG959 H-UNR native debris BELOW the law on dSphs"]

# ------------------------------------------------------------------ ledger
LED = [
    ("vlos_sigma (LOS dispersion)", "real_research/data/dsph/lvd_dwarf_*.csv (LVD compilation of published spectroscopy)", "RAW",
     "single-epoch for most UFDs; binaries inflate (see binary rows)"),
    ("rhalf_sph_physical (circularised R_e)", "LVD", "RAW (photometry) x distance", "propagated in MC"),
    ("distance modulus", "LVD", "SURVEY-CALIBRATION (RR Lyrae / HB / TRGB)", "g_obs/g_bar ∝ 1/D; propagated in MC"),
    ("mass_stellar (Upsilon_V = 2)", "LVD", "SURVEY-CALIBRATION (SPS M/L)", "bracket Upsilon 1-4: ±0.30 dex"),
    ("Wolf estimator 3 sigma^2 r12 / G", "Wolf et al. 2010 convention (A26 eq. 3)", "MODEL ASSUMPTION (spherical Jeans, equilibrium, anisotropy-insensitive at r12)",
     "factor-1 variant −0.477 dex (not clean)"),
    ("binary correction (statistical)", "CFG257/arroyo_polonio2026_tableA1.csv (12 UFDs, Moe & Di Stefano population)", "SURVEY-CALIBRATION (population model)",
     "free-f and f=0.7 applied"),
    ("binary cleaning (multi-epoch)", "CFG51 (Walker 2023: Boo I, Tuc II); Geha 2026 II (DEIMOS chi2 variables removed)", "RAW (multi-epoch)", "Geha variant"),
    ("tidal state / equilibrium", "CFG838 (no present-day tidal signal); none measured per UFD", "MODEL ASSUMPTION (not measured)", "bounded by sigma-inflation yardstick"),
    ("EFE (+1.25 dex reading)", "D2 d2_wide_binary_fork.py efe_delta (1-D QUMOND nu(y_i+y_e) with K term)", "STANDARD-MOND-MACHINERY + externally-calibrated host masses",
     "not used in the +2.15 (pure Newton) nor in Part B"),
    ("host masses MW 6e10 / M31 1e11", "CFG332 / labelled external (D2)", "EXTERNALLY CALIBRATED", "EFE and Jacobi (informational) only"),
    ("M_crit = a0 L*^2 / G (sample cut)", "A22/A26; L* = 24 pc from CFG820 globulars", "FRAMEWORK-NATIVE (L* fitted lower bound; a0 via kappa = 1/2 FITTED)", "alt footing sample reported"),
    ("screening S(s)", "CFG691 table via CFG820", "FRAMEWORK-NATIVE", "L* 24 vs 90 pc"),
    ("cold per baryon 5.364", "Planck Omega_c/Omega_b; CFG886 (BAO+BBN recovered, not pinned)", "ΛCDM-PROCESSED (cosmological fit)", "q ∝ 1/5.364 (linear)"),
    ("f_ret census floor 0.10", "CFG416/556 via CFG809 fret_of", "ΛCDM-PROCESSED (halo-mass census relative to Planck f_b)", "f_ret = 1 census-free: q ×10"),
    ("M_HI", "LVD mass_HI", "RAW (21 cm)", "adds to catchment baryons (only Leo T in the sample)"),
]
with open(os.path.join(HERE, f"e3_inputs_ledger{SFX}.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["input", "source", "class", "sensitivity / handling"]); w.writerows(LED)
with open(os.path.join(HERE, f"e3_per_system{SFX}.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(PER[0].keys())); w.writeheader()
    for row in PER: w.writerow(row)

npass = sum(ok for _, ok in CHK)
R["checks"] = {k: ok for k, ok in CHK}
P(f"\nE3_DWARF_EXCESS COMPLETE: {npass}/{len(CHK)} checks PASS.")
json.dump(R, open(os.path.join(HERE, f"e3_dwarf_excess_results{SFX}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"e3_dwarf_excess{SFX}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHK) else 1)
