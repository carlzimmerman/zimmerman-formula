#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A26 -- SETTLE THE FORK: law-first or medium-first, on the dwarfs already on disk.

THE FORK (FINAL_THEORY.md sec 5b, from A22):
  A22 eq. (9): inside lambda = L*/sqrt2 = 17.0 pc the P sector is a hedgehog of constant
  magnitude u = K|P| = GM/(2 lambda^2) = 2.42e-16 m/s^2 = 2.59e-6 a0, so the Solar System
  is not in the P sector's MOND regime at all.  The crossover r_MOND = sqrt(GM/a0) > L*
  defines M_crit = a0 L*^2/G = 3.87e5 Msun, below which the medium never reaches the MOND
  branch.
    law-first    : g_N = g^2/(g + a0) at every scale  -> sub-threshold systems ARE MOND.
    medium-first : the crossover is physical           -> sub-threshold systems are NEWTONIAN.

THE TEST.  For every dwarf on disk with (sigma_los, r_half, M_star):
    r12   = (4/3) r_half                       [3D half-light radius]
    g_bar = G (M_star/2) / r12^2               [half the stars enclosed]
    g_obs = 3 sigma^2 / r12                    [Wolf estimator = dynamical mass]
    Delta = log10 g_obs - log10[ g_bar * nu(g_bar/a0) ],   nu(y) = (1+sqrt(1+4/y))/2
  law-first predicts Delta = 0 at every mass.  medium-first predicts, for M_star < M_crit,
  g_obs = g_bar exactly, i.e. Delta = Delta_N = -log10 nu(g_bar/a0) ~ -1.5 dex (a DEFICIT).
  The sign of Delta below M_crit is the decider; the magnitude of the step at M_crit is the
  number.

Run:      python3 a26_checks.py
Mutate:   python3 a26_checks.py --mutate        (M1: inject medium-first below M_crit)
          python3 a26_checks.py --mutate2       (M2: sigma/1.45 everywhere, CFG828's control)
Output:   a26.out (captured), a26_results.json, a26_rar.csv
Deterministic, no network, numpy + scipy only.  kappa = 1/2, a0 = 9.36e-11 (canonical).
"""
import csv, json, math, os, sys
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DATA = os.path.join(REPO, "real_research", "data")
CFG = os.path.join(REPO, "campaign_fresh_gravity")

MUT1 = "--mutate" in sys.argv            # medium-first injection
MUT2 = "--mutate2" in sys.argv           # sigma/1.45
MUT = MUT1 or MUT2

# ---------------------------------------------------------------- constants (BRIEF sec 4)
G = 6.67430e-11
MSUN = 1.989e30
PC = 3.0856775814913673e16
A0_CAN = 9.36e-11
A0_ALT = 1.13e-10
LSTAR = 24.0 * PC                        # A20 window lower edge, FINAL_THEORY sec 4
M_CRIT = A0_CAN * LSTAR ** 2 / G / MSUN  # = 3.87e5 Msun  (A22)
LAM = LSTAR / math.sqrt(2.0)             # = 17.0 pc
U_SUN = G * MSUN / (2 * LAM ** 2)        # A22 eq. (9) for M = 1 Msun
A0 = A0_CAN

def nu(y):
    y = np.maximum(np.asarray(y, float), 1e-30)
    return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y))

OUT = []
def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))

def fl(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except Exception:
        return None

# ---------------------------------------------------------------- sample loaders
def load_lvd():
    """Local Volume Database (Pace 2024, ApJS 273, 15) -- the primary compilation."""
    rows = []
    for fn, host in (("lvd_dwarf_mw.csv", "MW"), ("lvd_dwarf_m31.csv", "M31"),
                     ("lvd_dwarf_local_field.csv", "field"),
                     ("lvd_dwarf_local_field_distant.csv", "distant")):
        for r in csv.DictReader(open(os.path.join(DATA, "dsph", fn))):
            s = fl(r.get("vlos_sigma"))
            rh = fl(r.get("rhalf_sph_physical")) or fl(r.get("rhalf_physical"))
            ms = fl(r.get("mass_stellar"))
            mv = fl(r.get("M_V"))
            if not s or s <= 0 or not rh or rh <= 0:
                continue
            if ms is None and mv is not None:
                ms = 0.4 * (4.83 - mv) + 0.301     # Upsilon_V = 2, same convention as LVD
            if ms is None:
                continue
            rows.append(dict(name=r["name"], host=host, sigma=s, rh=rh, logms=ms,
                             mdyn=fl(r.get("mass_dynamical_wolf")),
                             ul=bool(r.get("vlos_sigma_ul")), src=fn))
    return rows

def load_mcconnachie():
    """McConnachie 2012 AJ 144,4 (VizieR J/AJ/144/4) -- independent LG compilation."""
    rows = []
    for r in csv.DictReader(open(os.path.join(DATA, "dsph", "mcconnachie2012_dsph.csv"))):
        s, rh, mv = fl(r.get("sigma*")), fl(r.get("R2")), fl(r.get("VMag"))
        if not s or s <= 0 or not rh or mv is None:
            continue
        rows.append(dict(name=r["Name"], host=r.get("SubG", "?"), sigma=s, rh=rh,
                         logms=0.4 * (4.83 - mv) + 0.301, src="mcconnachie2012_dsph.csv"))
    return rows

def load_collins():
    """Collins 2013 ApJ 768,172 (VizieR J/ApJ/768/172) -- independent M31 dSph sample."""
    rows = []
    for line in open(os.path.join(DATA, "dsph", "collins2013_m31_dsph.tsv")):
        if line.startswith("#") or not line.strip():
            continue
        v = line.rstrip("\n").split("\t")
        if len(v) < 20:
            continue
        try:
            name, mv, rh, s = v[1].strip(), float(v[7]), float(v[8]), float(v[18])
        except (ValueError, IndexError):
            continue
        if s <= 0 or rh <= 0:
            continue                     # sigV = 0.0 rows are upper limits, not measurements
        rows.append(dict(name=name, host="M31", sigma=s, rh=rh,
                         logms=0.4 * (4.83 - mv) + 0.301, src="collins2013_m31_dsph.tsv"))
    return rows

def load_geha():
    """Geha 2026 ApJS (arXiv:2602.10202) Table A1 -- independent DEIMOS dispersions."""
    rows = []
    p = os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "geha2026_paperII_tableA1.csv")
    for r in csv.DictReader(open(p)):
        s = fl(r.get("sigma")) if fl(r.get("sigma_resolved")) == 1 else None
        if not s or s <= 0:
            continue
        rows.append(dict(name=r["full_name"], sigma=s, rh=None,
                         logms=(0.4 * (4.83 - fl(r["M_V"])) + 0.301) if fl(r.get("M_V")) else None,
                         src="geha2026_paperII_tableA1.csv"))
    return rows

def load_arroyo():
    """Arroyo-Polonio+ 2026 A&A 708,A287 Table A.1 -- UFD dispersions vs binary fraction f."""
    p = os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv")
    return list(csv.DictReader(open(p)))

def load_mcquinn():
    """McQuinn+ 2022 ApJ -- faint ROTATORS (V_rot, not sigma): listed, not used in the test."""
    p = os.path.join(DATA, "faint_rotators_mcquinn2022", "apjac9285t1_mrt.txt")
    n, ms = 0, []
    for line in open(p):
        if len(line) > 50 and line[0] != " " and not line.startswith(("#", "Title", "Authors",
                                                                      "Table", "Byte", "---", "Note")):
            try:
                ms.append(float(line[46:51]))
                n += 1
            except ValueError:
                pass
    return n, (min(ms), max(ms)) if ms else (None, None)

# ---------------------------------------------------------------- primary sample
PS_EXCL = {"WLM", "NGC 6822", "IC 1613", "Leo A", "Sagittarius dIrr", "Pegasus dIrr", "M 32",
           "LMC", "SMC"}

def build_primary(mut1=False, mut2=False, a0=A0_CAN, thr=1.0, sig_factor=1.0, go_factor=3.0, ul_drop=False,
                  exclude=frozenset(), hosts=("MW", "M31", "field")):
    rows = [r for r in load_lvd() if r["host"] in hosts]
    if exclude:
        rows = [r for r in rows if r["name"] not in exclude]
    if ul_drop:
        rows = [r for r in rows if not r["ul"]]
    r12 = np.array([(4.0 / 3.0) * r["rh"] for r in rows]) * PC
    ms = 10.0 ** np.array([r["logms"] for r in rows])
    if mut2:
        sig_factor = 1.0 / 1.45
    sig = np.array([r["sigma"] for r in rows]) * 1e3 * sig_factor
    gbar = G * (ms / 2.0) * MSUN / r12 ** 2
    gobs = go_factor * sig ** 2 / r12
    below = np.log10(ms) < math.log10(M_CRIT * thr)
    if mut1:                               # inject medium-first: sub-threshold => Newtonian
        gobs = np.where(below, gbar, gobs)
    return rows, ms, gbar, gobs, below, a0

def deltas(gbar, gobs, a0):
    y = gbar / a0
    return np.log10(gobs / (gbar * nu(y))), -np.log10(nu(y)), np.log10(gobs / gbar)

def boot_median(x, n=4000, seed=26):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, float)
    b = np.array([np.median(rng.choice(x, len(x))) for _ in range(n)])
    return float(np.median(x)), float(np.std(b, ddof=1))

def step_fit(lg, d, below):
    """Delta = a + b (log g_bar + 12) + c 1[M<M_crit].  c is the threshold step at fixed
    acceleration -- the quantity medium-first needs to be -1.62 dex."""
    X = np.column_stack([np.ones(len(d)), lg + 12.0, below.astype(float)])
    beta = np.linalg.lstsq(X, d, rcond=None)[0]
    res = d - X @ beta
    s2 = float(res @ res) / (len(d) - 3)
    cov = s2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    rng = np.random.default_rng(2602)
    bs = []
    for _ in range(2000):
        i = rng.integers(0, len(d), len(d))
        try:
            bs.append(np.linalg.lstsq(X[i], d[i], rcond=None)[0][2])
        except np.linalg.LinAlgError:
            pass
    return beta, se, float(np.std(bs, ddof=1)), s2

def model_compare(d, dN, below):
    """H_law: Delta = a + eps.   H_med: Delta = a + 1*Delta_N 1[below] + eps.
    The amplitude of the medium-first term is FIXED at 1 (that is the prediction); only the
    global offset a is free in each model, so neither is a superset of the other."""
    d = np.asarray(d, float); dN = np.asarray(dN, float); bl = below.astype(float)
    a_law = float(np.mean(d)); r_law = d - a_law
    a_med = float(np.mean(d - dN * bl)); r_med = d - a_med - dN * bl
    s_law = math.sqrt(float(r_law @ r_law) / len(d))
    s_med = math.sqrt(float(r_med @ r_med) / len(d))
    dchi2 = 2.0 * len(d) * math.log(s_med / s_law)   # >0 favours H_law
    return s_law, s_med, dchi2, (a_law, a_med)

# ================================================================ K1 / sample inventory
P("A26  SETTLE THE FORK (law-first vs medium-first) on dwarfs already on disk")
P("=" * 100)
if MUT1:
    P("*** MUTATION M1: medium-first INJECTED (g_obs := g_bar for every M_star < M_crit) ***")
if MUT2:
    P("*** MUTATION M2: every sigma divided by 1.45 (CFG828's control) ***")
P(f"a0 = {A0:.4e} m/s^2 (canonical)   L* = 24 pc   lambda = L*/sqrt2 = {LAM/PC:.2f} pc")
P(f"M_crit = a0 L*^2/G = {M_CRIT:.4e} Msun        u(M=1 Msun) = {U_SUN:.4e} m/s^2 = {U_SUN/A0:.3e} a0")
P("")
P("SAMPLE INVENTORY (every dwarf compilation on disk with the three required columns)")
P(f"{'sample':34s} {'file':38s} {'Nrows':>5s} {'Nuse':>5s} {'log M* range':>16s}  role")
P("-" * 118)
inv = []
lvd_all = []
for fn, host in (("lvd_dwarf_mw.csv", "MW"), ("lvd_dwarf_m31.csv", "M31"),
                 ("lvd_dwarf_local_field.csv", "LG field"),
                 ("lvd_dwarf_local_field_distant.csv", "beyond LG")):
    raw = list(csv.DictReader(open(os.path.join(DATA, "dsph", fn))))
    use = [r for r in lvd_all if False]
    lvd_all.append((fn, host, raw))
for fn, host, raw in lvd_all:
    u = [r for r in load_lvd() if r["src"] == fn]
    ms = [r["logms"] for r in u]
    inv.append(dict(sample=f"LVD {host}", file=fn, nrows=len(raw), nuse=len(u),
                    logm=(min(ms), max(ms)) if ms else None, role=("PRIMARY" if fn !=
                    "lvd_dwarf_local_field_distant.csv" else "cross-check (all are satellites)")))
mc = load_mcconnachie(); co = load_collins(); ge = load_geha(); ar = load_arroyo()
nq, nq_rng = load_mcquinn()
inv.append(dict(sample="McConnachie 2012", file="mcconnachie2012_dsph.csv",
                nrows=sum(1 for _ in open(os.path.join(DATA, "dsph", "mcconnachie2012_dsph.csv"))) - 1,
                nuse=len(mc), logm=(min(r["logms"] for r in mc), max(r["logms"] for r in mc)),
                role="independent sigma/r_h cross-check"))
inv.append(dict(sample="Collins 2013 (M31)", file="collins2013_m31_dsph.tsv",
                nrows=18, nuse=len(co), logm=(min(r["logms"] for r in co), max(r["logms"] for r in co)),
                role="independent M31 cross-check"))
inv.append(dict(sample="Geha 2026 Paper II", file="geha2026_paperII_tableA1.csv",
                nrows=67, nuse=len(ge),
                logm=(min(r["logms"] for r in ge if r["logms"]), max(r["logms"] for r in ge if r["logms"])),
                role="independent sigma (DEIMOS), no r_h"))
inv.append(dict(sample="Arroyo-Polonio 2026", file="arroyo_polonio2026_tableA1.csv",
                nrows=len(ar), nuse=len(ar), logm=None,
                role="binary-corrected sigma, 12 UFDs (confound budget)"))
inv.append(dict(sample="Walker 2023 (M2FS/Hect)", file="walker2023/ (per-star; CFG51 reduction)",
                nrows=38, nuse=2, logm=None, role="multi-epoch binary-cleaned sigma, 2 UFDs"))
inv.append(dict(sample="McQuinn 2022 faint rotators", file="apjac9285t1_mrt.txt",
                nrows=nq, nuse=0, logm=nq_rng, role="rotation-supported: no sigma, not used"))
for it in inv:
    rng = "%.2f..%.2f" % it["logm"] if it["logm"] else "   n/a"
    P(f"{it['sample']:34s} {it['file']:38s} {it['nrows']:5d} {it['nuse']:5d} {rng:>16s}  {it['role']}")
P("")

rows, ms, gbar, gobs, below, _ = build_primary(mut1=MUT1, mut2=MUT2)
d, dN, R = deltas(gbar, gobs, A0)
lg = np.log10(gbar)
n, nb = len(d), int(below.sum())
P(f"K1 sample: N_primary = {n} (LVD MW+M31+field with sigma>0, r_half>0, M_star)   "
  f"N_below_Mcrit = {nb}   N_above = {n-nb}")
P(f"           log M* {np.log10(ms).min():.2f}..{np.log10(ms).max():.2f}   "
  f"log g_bar {np.log10(gbar).min():.2f}..{np.log10(gbar).max():.2f}   "
  f"upper-limit sigma rows: {sum(1 for r in rows if r['ul'])}")
K1 = (n >= 80) and (nb >= 40)
P(f"K1 {'PASS' if K1 else 'FAIL'} N={n} N_below={nb}  threshold: N>=80 and N_below>=40")
P("")

# ================================================================ K2 theory identities
mc_err = abs(M_CRIT - 3.87e5) / 3.87e5
lam_pc = LAM / PC
u_ratio = U_SUN / A0
K2 = (mc_err < 0.01) and (abs(lam_pc - 17.0) < 0.05) and (abs(u_ratio / 2.59e-6 - 1) < 0.01)
P(f"K2 {'PASS' if K2 else 'FAIL'} M_crit={M_CRIT:.4e} Msun (3.87e5 to {mc_err*100:.2f}%), "
  f"lambda={lam_pc:.2f} pc, u/a0={u_ratio:.3e}  threshold: 1%, 0.05 pc, 1%")
P("")

# ================================================================ K3 record control (CFG828)
def cfg828_control():
    R27 = json.load(open(os.path.join(CFG, "CFG827_dwarf_age_sfh_ml", "cfg827_results.json")))["rows"]
    R24 = json.load(open(os.path.join(CFG, "CFG824_dwarf_age_fossil", "cfg824_results.json")))["rows"]
    LVD = {}
    for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
        for r in csv.DictReader(open(os.path.join(DATA, "dsph", f))):
            LVD[r["name"]] = (fl(r.get("M_V")),
                              fl(r.get("rhalf_sph_physical")) or fl(r.get("rhalf_physical")))
    EXCL = {"WLM", "NGC 6822", "IC 1613", "Leo A", "Sagittarius dIrr", "Pegasus dIrr", "M 32"}
    gb, go_, lm = [], [], []
    for nm, r in R27.items():
        if nm in EXCL:
            continue
        MV, rh = LVD[nm]
        s = R24[nm]["so"] / (1.45 if MUT2 else 1.0)
        r12 = (4.0 / 3.0) * rh * PC
        Ms = r["ups"] * 10 ** (0.4 * (4.83 - MV))
        gb.append(6.674e-11 * (Ms / 2) * 1.989e30 / r12 ** 2)
        go_.append(3 * (s * 1e3) ** 2 / r12)
        lm.append(math.log10(Ms))
    gb, go_, lm = map(np.array, (gb, go_, lm))
    dd = np.log10(go_ / (gb * nu(gb / 9.3603e-11)))
    out = np.log10(gb) < -11.9
    return len(dd), out.sum(), float(dd[out].mean()), gb, dd, lm

n828, n828o, mean828, gb828, d828, lm828 = cfg828_control()
K3 = abs(mean828 - 0.44) <= 0.06
P(f"K3 {'PASS' if K3 else 'FAIL'} CFG828 reproduction: N={n828}, out-of-SPARC-range N={n828o}, "
  f"mean Delta={mean828:+.3f} dex  threshold |mean-0.44|<=0.06  (record: +0.44)")
P("")

# ================================================================ main split statistics
med_b, se_b = boot_median(d[below]); med_a, se_a = boot_median(d[~below])
Rb, se_Rb = boot_median(R[below]); Ra, se_Ra = boot_median(R[~below])
gap = float(np.median(d[below] - dN[below]))
_rg = np.random.default_rng(2626)
_gb = []
for _ in range(2000):
    i = _rg.integers(0, nb, nb)
    _gb.append(np.median(d[below][i] - dN[below][i]))
se_gap = float(np.std(_gb, ddof=1))
mw_d = stats.mannwhitneyu(d[below], d[~below], alternative="two-sided")
ks_d = stats.ks_2samp(d[below], d[~below])
mw_R = stats.mannwhitneyu(R[below], R[~below], alternative="two-sided")
n_law = int((np.abs(d[below]) < 0.5).sum())
n_newt = int((np.abs(d[below] - dN[below]) < 0.5).sum())

P("RAR SPLIT AT M_crit (law g_N = g^2/(g+a0); Delta = dex from the law)")
P(f"  below M_crit  N={nb:3d}  median log g_bar {np.median(np.log10(gbar[below])):6.2f}  "
  f"median Delta {med_b:+.3f} +- {se_b:.3f}  median log(g_obs/g_bar) {Rb:+.3f} +- {se_Rb:.3f}")
P(f"  above M_crit  N={n-nb:3d}  median log g_bar {np.median(np.log10(gbar[~below])):6.2f}  "
  f"median Delta {med_a:+.3f} +- {se_a:.3f}  median log(g_obs/g_bar) {Ra:+.3f} +- {se_Ra:.3f}")
P(f"  Mann-Whitney p(Delta) = {mw_d.pvalue:.3e}   KS p(Delta) = {ks_d.pvalue:.3e}   "
  f"MW p(log g_obs/g_bar) = {mw_R.pvalue:.3e}")
P("  (identity: Delta - Delta_N = log10(g_obs/g_bar) exactly, so the 'distance from Newtonian' and "
  "the 'boost' are one number)")
P(f"  medium-first requires Delta = Delta_N below M_crit: median {np.median(dN[below]):+.3f} dex "
  f"(deficit); measured {med_b:+.3f} dex -> gap {gap:+.3f} +- {se_gap:.3f} dex")
P(f"  within +-0.5 dex of the LAW: {n_law}/{nb}    within +-0.5 dex of NEWTONIAN: {n_newt}/{nb}")
_s1, _ = boot_median(d[below] - math.log10(3.0))
P(f"  estimator normalisation: with g_obs = sigma^2/r (no Wolf factor 3) the below-M_crit median "
  f"Delta is {_s1:+.3f} dex (law-first: 0); with the Wolf dynamical mass 3 sigma^2/r it is {med_b:+.3f}")
P("")
P("THE RAR ITSELF (median of log g_obs per g_bar bin; law = g_bar nu(g_bar/a0), Newton = g_bar)")
P(f"  {'log g_bar bin':16s} {'N':>4s} {'N<Mcrit':>8s} {'med log g_obs':>14s} {'law':>8s} {'Newton':>8s} "
  f"{'med Delta':>10s} {'deficit?':>9s}")
edges = np.arange(-14.5, -8.4, 0.5)
for e in edges:
    m = (lg >= e) & (lg < e + 0.5)
    if m.sum() < 3:
        continue
    law_g = np.median(np.log10(gbar[m] * nu(gbar[m] / A0)))
    P(f"  [{e:6.2f},{e+0.5:6.2f}) {int(m.sum()):4d} {int((m & below).sum()):8d} "
      f"{np.median(np.log10(gobs[m])):14.3f} {law_g:8.3f} {np.median(np.log10(gbar[m])):8.3f} "
      f"{np.median(d[m]):+10.3f} {'NO' if np.median(d[m]) > 0 else 'YES':>9s}")
P("")
# the theory's own criterion, per system: r_MOND = sqrt(G M_star / a0) vs L* = 24 pc
r_mond = np.sqrt(G * ms * MSUN / A0) / PC
P(f"  the theory's criterion per system: median r_MOND = sqrt(GM/a0) is "
  f"{np.median(r_mond[below]):.1f} pc below M_crit and {np.median(r_mond[~below]):.1f} pc above "
  f"(L* = 24 pc); {int((r_mond < 24.0).sum())}/{n} systems have r_MOND < L*")
P("")
rho_mg = stats.spearmanr(np.log10(ms), lg)
frac_low = float((lg[below] < -12.0).mean())
P(f"  CONFOUND GEOMETRY: Spearman rho(log M*, log g_bar) = {rho_mg.statistic:+.3f} (p {rho_mg.pvalue:.1e}); "
  f"{frac_low*100:.0f}% of sub-threshold systems lie below g_bar = 1e-12")
P("")

# ================================================================ K4..K6
K4 = Rb >= 0.7
P(f"K4 {'PASS' if K4 else 'FAIL'} kernel-free boost below M_crit: median log10(g_obs/g_bar)="
  f"{Rb:+.3f} ({10**Rb:.1f}x)  threshold >=0.70 (5x); medium-first = 0.000")
K5 = (med_b > 0) and (med_b - 1.96 * se_b > 0)
P(f"K5 {'PASS' if K5 else 'FAIL'} sign below M_crit: median Delta={med_b:+.3f}+-{se_b:.3f} "
  f"(95% lo {med_b-1.96*se_b:+.3f})  threshold >0 at 95%")
K6 = gap >= 1.0
P(f"K6 {'PASS' if K6 else 'FAIL'} distance from Newtonian below M_crit: {gap:+.3f}+-{se_gap:.3f} dex "
  f"threshold >=1.0 dex")
P("")

# ================================================================ K7 step at M_crit
beta, se, se_boot, s2 = step_fit(lg, d, below)
c, sc = beta[2], max(se[2], se_boot)
# medium-first requirement: above-group baseline med_a, below-group at Delta_N
c_med = float(np.median(dN[below]) - med_a)
nsig = (c - c_med) / sc
K7 = nsig >= 5.0
P(f"K7 {'PASS' if K7 else 'FAIL'} step at M_crit, g_bar-controlled: c={c:+.3f}+-{sc:.3f} dex "
  f"(a={beta[0]:+.3f}, b={beta[1]:+.3f})")
P(f"     medium-first requires c={c_med:+.3f} dex; separation {nsig:.1f} sigma  threshold >=5 sigma")
s_law, s_med, dchi2, offs = model_compare(d, dN, below)
fav = "LAW-FIRST" if dchi2 > 0 else "MEDIUM-FIRST"
P(f"     model comparison (Gaussian, scatter by ML, one offset each): s_law={s_law:.3f} dex  "
  f"s_med={s_med:.3f} dex  Delta(-2lnL)={dchi2:+.1f} -> favours {fav}")
P("")

# ================================================================ K8 matched-g_bar bin
lo, hi = -14.2, -12.5
mb = (lg >= lo) & (lg < hi)
inb, ina = mb & below, mb & (~below)
diffm = float(np.median(d[inb]) - np.median(d[ina])) if inb.sum() and ina.sum() else float("nan")
K8 = (inb.sum() >= 10) and (ina.sum() >= 5) and (diffm > -1.0)
P(f"K8 {'PASS' if K8 else 'FAIL'} matched g_bar in [{lo},{hi}]: N_below={int(inb.sum())} "
  f"median Delta={np.median(d[inb]):+.3f} | N_above={int(ina.sum())} median Delta={np.median(d[ina]):+.3f} "
  f"| difference={diffm:+.3f} dex  threshold >-1.0 (medium-first: -1.5)")
P("")

# ================================================================ K9 census
K9 = (n_law >= 10) and (n_newt <= 2)
P(f"K9 {'PASS' if K9 else 'FAIL'} census below M_crit: near-law {n_law} vs near-Newton {n_newt} "
  f"threshold >=10 and <=2")
P("")

# ================================================================ K10 robustness
def variant(label, **kw):
    rr, mm, gb_, go_, bl, a0_ = build_primary(**kw)
    dd, dN_, RR = deltas(gb_, go_, a0_)
    return label, len(dd), int(bl.sum()), float(np.median(dd[bl])), float(np.median(dd[~bl])), \
        step_fit(np.log10(gb_), dd, bl)[0][2]

base_kw = dict(mut1=MUT1, mut2=MUT2)
V = []
V.append(variant("sigma^2/r (no factor 3)", go_factor=1.0, **base_kw))
_rr, _mm, _gb, _go, _bl, _a0 = build_primary(**base_kw)
_md = np.array([r["mdyn"] if r["mdyn"] is not None else np.nan for r in _rr])
_go2 = G * 10 ** _md * MSUN / (((4.0 / 3.0) * np.array([r["rh"] for r in _rr])) * PC) ** 2
_dd2 = np.log10(_go2 / (_gb * nu(_gb / _a0)))
_ok = np.isfinite(_dd2)
V.append(("M_dyn(Wolf)", int(_ok.sum()), int(_bl.sum()), float(np.nanmedian(_dd2[_bl])),
          float(np.nanmedian(_dd2[~_bl])), step_fit(np.log10(_gb)[_ok], _dd2[_ok], _bl[_ok])[0][2]))
V.append(variant("a0 alt = 1.13e-10", a0=A0_ALT, **base_kw))
V.append(variant("MW only", hosts=("MW",), **base_kw))
V.append(variant("M31 only", hosts=("M31",), **base_kw))
V.append(variant("LG field only", hosts=("field",), **base_kw))
V.append(variant("threshold on M*/2", thr=0.5, **base_kw))
V.append(variant("pressure-supported only", exclude=PS_EXCL, **base_kw))
K10 = all(v[3] > 0 and v[5] > -0.5 for v in V)
P("K10 robustness (median Delta below M_crit and g_bar-controlled step, every variant)")
for v in V:
    P(f"     {v[0]:26s} N={v[1]:3d} N_below={v[2]:3d}  med Delta below {v[3]:+.3f}  "
      f"above {v[4]:+.3f}  step {v[5]:+.3f}")
P(f"K10 {'PASS' if K10 else 'FAIL'} all {len(V)} variants keep med Delta(below)>0 and step>-0.5  "
  f"threshold: all")
P("")

# ================================================================ K11 confound budget
bin_shift, bin_med = [], []
for r in ar:
    f0, f07 = fl(r.get("sig_f0")), fl(r.get("sig_f07"))
    if f0 and f07 and f0 > 0 and f07 > 0:
        bin_shift.append(2 * math.log10(f07 / f0))
        bin_med.append(r["galaxy"])
# Walker+ 2023 multi-epoch reduction (CFG51): the largest *measured* cleaning effect in the record
def walker_budget():
    try:
        d = json.load(open(os.path.join(CFG, "CFG51_walker_ufd_results.json")))
        nums = d["numbers"]["RES"]
        out = []
        for k, v in nums.items():
            if "|canonical|single" in k or "|canonical|clean" in k:
                nm, _, tag = k.split("|")
                out.append((nm, tag, v["off"]))
        best = (None, 0.0)
        for nm in {o[0] for o in out}:
            si = [o[2] for o in out if o[0] == nm and o[1] == "single"]
            cl = [o[2] for o in out if o[0] == nm and o[1] == "clean"]
            if si and cl and si[0] > 0 and cl[0] > 0:
                sh = 2.0 * (cl[0] - si[0])              # off is log10(sigma/sigma_law); Delta = 2*off
                if abs(sh) > abs(best[1]):
                    best = (nm, sh)
        return best
    except Exception:
        return (None, float("nan"))

w_name, w_shift = walker_budget()
max_bin = float(min(bin_shift)) if bin_shift else float("nan")
med_bin = float(np.median(bin_shift)) if bin_shift else float("nan")
need = float(np.median(d[below]) - np.median(dN[below]))
worst_corr = max(abs(max_bin), abs(w_shift) if w_shift == w_shift else 0.0)
after_max = need - worst_corr
ctl = (~below) & (lg < -12.0)
med_ctl = float(np.median(d[ctl]))
K11 = (after_max >= 1.0) and (ctl.sum() >= 5) and (abs(med_ctl) <= 0.5)
P(f"K11 {'PASS' if K11 else 'FAIL'} confound budget: binary correction (Arroyo-Polonio f=0.7 vs f=0) "
  f"median {med_bin:+.3f}, largest {max_bin:+.3f} dex in Delta over {len(bin_shift)} UFDs")
frac = ("%.0f%%" % (after_max / need * 100.0)) if need else "n/a"
P(f"     Walker 2023 multi-epoch cleaning ({w_name}): {w_shift:+.3f} dex in Delta")
P(f"     medium-first needs {need:.2f} dex; after the LARGEST measured correction ({worst_corr:.2f} dex) "
  f"{after_max:.2f} dex survive ({frac} of the gap)  threshold >=1.0 dex")
P(f"     low-g_bar control ABOVE M_crit (N={int(ctl.sum())}, log g_bar<-12): median Delta={med_ctl:+.3f} dex "
  f"(near the law at 1e-13 m/s^2 without the UFD population)")
P("")

# ================================================================ verdict
checks = [
    ("K1", K1, f"N={n}, N_below={nb}", "N>=80 and N_below>=40"),
    ("K2", K2, f"M_crit={M_CRIT:.4e}, lambda={lam_pc:.2f} pc, u/a0={u_ratio:.3e}",
     "1% of 3.87e5, |lambda-17|<0.05 pc, 1% of 2.59e-6"),
    ("K3", K3, f"mean Delta={mean828:+.3f} dex (N={n828})", "|mean-0.44|<=0.06"),
    ("K4", K4, f"median log10(g_obs/g_bar)={Rb:+.3f}", ">=0.70"),
    ("K5", K5, f"median Delta={med_b:+.3f}+-{se_b:.3f}", ">0 at 95%"),
    ("K6", K6, f"median distance to Newtonian={gap:+.3f}+-{se_gap:.3f} dex", ">=1.0 dex"),
    ("K7", K7, f"c={c:+.3f}+-{sc:.3f} dex, {nsig:.1f} sigma from {c_med:+.3f}", ">=5 sigma"),
    ("K8", K8, f"difference={diffm:+.3f} dex (N={int(inb.sum())}/{int(ina.sum())})", ">-1.0 dex"),
    ("K9", K9, f"near-law {n_law}, near-Newton {n_newt}", ">=10 and <=2"),
    ("K10", K10, f"{len(V)} variants, all med Delta(below)>0 and step>-0.5", "all"),
    ("K11", K11, f"{after_max:.2f} dex survives the largest correction ({worst_corr:.2f} dex)",
     ">=1.0 dex"),
]
npass = sum(1 for ck in checks if ck[1])
verdict = "LAW-FIRST" if (K4 and K5 and K7 and K6) else ("MEDIUM-FIRST" if (K4 is False and K5 is False)
                                                          else "UNDECIDABLE(confound)")
P("=" * 100)
P(f"VERDICT: {verdict}")
P(f"  deciding number 1 (kernel-free): median log10(g_obs/g_bar) below M_crit = {Rb:+.3f} "
  f"({10**Rb:.0f}x); medium-first = 0 ({1:.0f}x)")
P(f"  deciding number 2 (threshold step): c = {c:+.3f} +- {sc:.3f} dex at fixed g_bar; "
  f"medium-first requires {c_med:+.3f} dex -> {nsig:.1f} sigma")
P(f"  deciding number 3 (per system): the most negative Delta below M_crit is "
  f"{d[below].min():+.3f} dex; {int((d[below] < -0.5).sum())}/{nb} systems show a deficit >=0.5 dex, "
  f"and medium-first needs {np.median(dN[below]):+.2f}")
P(f"  residual honesty: below M_crit the data sit {med_b:+.3f} dex from the law (medium-first would be "
  f"{c_med:+.3f}); a non-zero residual here is the separate dwarf-excess problem, not the fork")
P(f"A26 COMPLETE: {npass}/{len(checks)} checks PASS.")

# ---------------------------------------------------------------- write artefacts
res = dict(lane="A26_fork_decider", status=("NUMERICAL" if npass == len(checks) else "NUMERICAL(FAILED CHECK)"),
           verdict=verdict, mutate=(1 if MUT1 else (2 if MUT2 else 0)),
           checks=[dict(id=i, **{"pass": bool(v)}, value=val, threshold=thr)
                   for i, v, val, thr in checks],
           numbers=dict(
               M_crit_Msun=float(M_CRIT), L_star_pc=24.0, lambda_pc=float(lam_pc),
               u_over_a0=float(u_ratio), a0=float(A0),
               N_primary=int(n), N_below=int(nb), N_above=int(n - nb),
               logMstar_min=float(np.log10(ms).min()), logMstar_max=float(np.log10(ms).max()),
               loggbar_min=float(np.log10(gbar).min()), loggbar_max=float(np.log10(gbar).max()),
               median_Delta_below=med_b, se_Delta_below=se_b,
               median_Delta_below_sigma2r=float(med_b - math.log10(3.0)),
               median_Delta_above=med_a, se_Delta_above=se_a,
               median_logboost_below=float(Rb), se_logboost_below=float(se_Rb),
               median_logboost_above=float(Ra),
               median_DeltaN_below=float(np.median(dN[below])),
               gap_to_newton=float(gap), se_gap_to_newton=se_gap,
               step_c=float(c), step_se=float(sc), step_c_medium_first=float(c_med),
               step_separation_sigma=float(nsig),
               mw_p_delta=float(mw_d.pvalue), ks_p_delta=float(ks_d.pvalue),
               mw_p_boost=float(mw_R.pvalue),
               n_within_0p5_of_law=int(n_law), n_within_0p5_of_newton=int(n_newt),
               min_Delta_below=float(d[below].min()),
               n_below_deficit_0p5=int((d[below] < -0.5).sum()),
               matched_bin=[lo, hi, int(inb.sum()), float(np.median(d[inb])),
                            int(ina.sum()), float(np.median(d[ina])), diffm],
               s_law=float(s_law), s_med=float(s_med), delta_chi2_law_first=float(dchi2),
               max_binary_correction_dex=float(max_bin),
               walker_multiepoch_shift_dex=float(w_shift),
               worst_measured_correction_dex=float(worst_corr),
               r_MOND_below_pc=float(np.median(r_mond[below])),
               r_MOND_above_pc=float(np.median(r_mond[~below])),
               n_rMOND_below_Lstar=int((r_mond < 24.0).sum()),
               n_subthreshold_at_low_gbar=int(((lg < -12.0) & below).sum()),
               spearman_rho_logM_loggbar=float(rho_mg.statistic),
               spearman_p=float(rho_mg.pvalue),
               lowgbar_control_N=int(ctl.sum()), lowgbar_control_median_Delta=float(med_ctl),
               cfg828_N=int(n828), cfg828_mean_Delta=float(mean828),
               variants=[[v[0], v[1], v[2], v[3], v[4], v[5]] for v in V],
               examples={r["name"]: dict(logMstar=float(np.log10(ms[i])),
                                         loggbar=float(lg[i]), loggobs=float(np.log10(gobs[i])),
                                         boost=float(R[i]), Delta=float(d[i]),
                                         Delta_newton=float(dN[i]), r_MOND_pc=float(r_mond[i]),
                                         below=int(below[i]))
                         for i, r in enumerate(rows)
                         if r["name"] in ("Segue 1", "Tucana V", "Bootes I", "Willman 1", "Draco",
                                          "Sculptor", "Crater II", "Antlia II", "Fornax", "Leo I")},
               sample_inventory=inv),
           constants_used=["c=2.99792458e8", "G=6.67430e-11", "Msun=1.989e30", "pc=3.0856775814913673e16",
                           "a0_can=9.36e-11", "a0_alt=1.13e-10", "L_star=24 pc (A20 window edge)",
                           "kappa=1/2", "M_star: LVD mass_stellar at Upsilon_V=2"])
sfx = "" if not MUT else ("_MUTATE" if MUT1 else "_MUTATE2")
json.dump(res, open(os.path.join(HERE, f"a26_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"a26{sfx}.out"), "w").write("\n".join(OUT) + "\n")
with open(os.path.join(HERE, f"a26_rar{sfx}.csv"), "w") as f:
    f.write("name,host,logMstar,loggbar,loggobs,Delta,Delta_newton,logboost,below_Mcrit,r_MOND_pc\n")
    for i in np.argsort(np.log10(ms)):
        f.write(f"{rows[i]['name']},{rows[i]['host']},{np.log10(ms[i]):.3f},{np.log10(gbar[i]):.6f},"
                f"{np.log10(gobs[i]):.6f},{d[i]:+.4f},{dN[i]:+.4f},{R[i]:+.4f},{int(below[i])},{r_mond[i]:.3f}\n")
sys.exit(0 if npass == len(checks) else 1)
