#!/usr/bin/env python3
"""X31_feedback_energy_selector: does F = (cumulative feedback / heating energy per baryon) / (binding energy per baryon)
separate X19's EXTRA classes from its NONE classes, and does it order the amounts?
Criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (1aa11f9bcb), AMENDMENT_A1.md (358e3859ed, pre-result).

Run:   OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 15 python3 x31_feedback_energy_selector.py            -> .out, _results.json, x31_classes.csv
       X31_MUTATE=1 ... (F lists deranged across classes; E/s/Z swapped UFD<->LG field, T1<->T3)          -> *_MUTATE.* (K0, K3 must FAIL; exit 1)
X19's class-table machinery and rank test are exec'd read-only from its committed source (X19_MUTATE unset).
kappa = 1/2 FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled. No dark-matter particle. Not "theory closed".
"""
import contextlib, csv, io, json, math, os, resource, sys, time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
os.environ.pop("X19_MUTATE", None)
sys.dont_write_bytecode = True
import numpy as np
from scipy.integrate import quad
from scipy.stats import spearmanr, mannwhitneyu

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
MUT = os.environ.get("X31_MUTATE", "") == "1"; TAG = "_MUTATE" if MUT else ""
OUTL = []


def P(s=""):
    OUTL.append(str(s)); print(s, flush=True)


CHECKS = {}


def check(name, ok, value, line):
    CHECKS[name] = dict(ok=bool(ok), value=str(value), line=line)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value} (line {line})")


def rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)


P("X31_feedback_energy_selector  " + ("MUTATE (F lists deranged across classes; E/s/Z swapped UFD<->LG field, T1<->T3)" if MUT else "normal run"))
P("kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed.")

# =====================================================================================================  X19 machinery (exec'd)
X19PATH = os.path.join(RB, "X19_selector_rank_test", "x19_selector_rank_test.py")
SRC = open(X19PATH).read(); CUT = SRC[:SRC.index("RESULTS = {")]
NS = {"__file__": X19PATH, "__name__": "x19_exec"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(CUT, X19PATH, "exec"), NS)
assert NS["MUT"] is False
X19J = json.load(open(os.path.join(RB, "X19_selector_rank_test", "x19_selector_rank_test_results.json")))
CLASSES = NS["CLASSES"]; FOOTS = NS["FOOTS"]; ETAB = NS["ETAB"]; SYS = NS["SYS"]; INTX = NS["INT"]
rank_test = NS["rank_test"]; two_var = NS["two_var"]; labels = NS["labels"]; interval = NS["interval"]
G = NS["G"]; MSUN = NS["MSUN"]; KPC = NS["KPC"]; MPC = NS["MPC"]; KB = NS["KB"]; MP = NS["MP"]; KEV = NS["KEV"]; MU = NS["MU"]
LN10 = math.log(10)

# =====================================================================================================  STEP 0
P("\n=== STEP 0: X19 class table, labels (both baselines) and M_b / sigma intervals vs X19's committed JSON (exact)")
k0 = []
for f in FOOTS:
    for b in ("iso", "efe"):
        for nm in CLASSES:
            mine = ETAB[(f, b)][nm]; js = X19J["E_table"][f"{f}|{b}"][nm]
            for q in ("E", "s"):
                if mine[q] != js[q]:
                    k0.append(f"{f}|{b}|{nm}|{q}")
            if js["Z"] is None:
                if not math.isinf(mine["Z"]):
                    k0.append(f"{f}|{b}|{nm}|Z")
            elif mine["Z"] != js["Z"]:
                k0.append(f"{f}|{b}|{nm}|Z")
    Lm = labels(ETAB[(f, "iso")], "LS")
    for nm in CLASSES:
        if Lm[nm] != X19J["results"]["labels"][f][nm]:
            k0.append(f"{f}|label|{nm}")
k0b = []
for f in FOOTS:
    for nm in CLASSES:
        for v in ("M_b", "sigma"):
            a = INTX[(f, False)][nm][v]; js = X19J["intervals"][f"{f}|p16_84"][nm][v]
            if (a is None) != (js is None) or (a is not None and any(x != y for x, y in zip(a, js))):
                k0b.append(f"{f}|{nm}|{v}")
P(f"  {'class':18s} " + " | ".join(f"{f} {b}: E (s) Z label" for f in FOOTS for b in ("iso", "efe")))
for nm in CLASSES:
    cells = []
    for f in FOOTS:
        for b in ("iso", "efe"):
            e = ETAB[(f, b)][nm]; Lb = labels(ETAB[(f, b)], "LS")[nm]
            cells.append(f"{e['E']:+.3f} ({e['s']:.3f}) {e['Z']:+.2f} {Lb}")
    P(f"  {nm:18s} " + " | ".join(cells))

# MUTATE (ii): E/s/Z swapped in the table used for testing (as X19's MUTATE)
TT = {k: {nm: dict(v) for nm, v in ETAB[k].items()} for k in ETAB}
if MUT:
    for k in TT:
        for a, b in (("MW ultra-faint", "LG field"), ("Clusters T1", "Clusters T3")):
            for q in ("E", "s", "Z"):
                TT[k][a][q], TT[k][b][q] = TT[k][b][q], TT[k][a][q]
    for f in FOOTS:
        for b in ("iso", "efe"):
            for nm in CLASSES:
                for q in ("E", "s", "Z"):
                    if TT[(f, b)][nm][q] != ETAB[(f, b)][nm][q] and f"{f}|{b}|{nm}|{q}|testing" not in k0:
                        k0.append(f"{f}|{b}|{nm}|{q}|testing")
check("K0", not k0, f"{len(k0)} mismatches" + (f": {k0[:8]}{' ...' if len(k0) > 8 else ''}" if k0 else " (E, s, Z both baselines, both footings; L-S labels)"), "0 (exact; any -> stop)")
check("K0b", not k0b, f"{len(k0b)} interval mismatches (M_b, sigma)", "0 (exact)")
STOP = bool(k0) and not MUT

# =====================================================================================================  constants
P("\n=== CONSTANTS (frozen section 2; PROVISIONAL from memory unless noted)")
E_SN = 1e44                         # J (1e51 erg)
M1, MB, M2, ML, MU_ = 0.1, 0.5, 100.0, 8.0, 100.0
KCONT = MB ** (2.3 - 1.3)           # xi = m^-1.3 (0.1-0.5), KCONT m^-2.3 (0.5-100): continuous at 0.5


def xi(m):
    return m ** -1.3 if m < MB else KCONT * m ** -2.3


NSN_cf = KCONT * (ML ** -1.3 - MU_ ** -1.3) / 1.3
MASS_cf = (MB ** 0.7 - M1 ** 0.7) / 0.7 + KCONT * (MB ** -0.3 - M2 ** -0.3) / 0.3
ETA = NSN_cf / MASS_cf
ETA_q = quad(xi, ML, MU_)[0] / (quad(lambda m: m * xi(m), M1, MB)[0] + quad(lambda m: m * xi(m), MB, M2)[0])
R_RET = 0.4; EPS = 1.0; T_RE = 2e4; FSTAR_COS = 0.07
E_RE = 1.5 * KB * T_RE / (MU * MP) / 1e6                                      # (km/s)^2
ESN_PER_MSTAR = EPS * E_SN * ETA / (1 - R_RET) / MSUN / 1e6                  # (km/s)^2 per (M*/M_den)
P(f"  Kroupa IMF eta_SN (8-100 / 0.1-100) = {ETA:.6f} per Msun formed (quadrature {ETA_q:.6f}); R {R_RET}; E_SN 1e51 erg; eps_SN {EPS}")
P(f"  e_SN per unit (M*/M_den) = {ESN_PER_MSTAR:.4g} (km/s)^2 = ({math.sqrt(ESN_PER_MSTAR):.1f} km/s)^2; e_re (T 2e4 K, mu 0.6) = {E_RE:.4g} (km/s)^2")
s1kev = math.sqrt(KEV / (MU * MP)) / 1e3
kt_rt = []

# =====================================================================================================  per-system F
DATA = NS["DATA"]
TDGM = {}
for r in csv.DictReader(open(os.path.join(DATA, "tidal_dwarfs", "lelli2015_tdg.csv"))):
    TDGM[r["object"].replace(" ", "")] = (float(r["M_star_1e8"]) * 1e8, float(r["M_bar_1e8"]) * 1e8)
GASRICH = {"Antlia B", "Aquarius", "IC 1613", "Leo A", "Leo T", "NGC 6822", "Pegasus dIrr", "Phoenix", "Sagittarius dIrr", "UGC 4879", "WLM", "LGS 3"}
X1CL = set(NS["X1KEY"])
# MW gas (A1): McMillan17 HI + H2 as P4 encodes, R 0-100 kpc
R_FID = 8.33
S0HI = 10.0e6 / math.exp(-4.0 / R_FID - R_FID / 7.0); S0H2 = 2.0e6 / math.exp(-12.0 / R_FID - R_FID / 1.5)
MGAS_MW = quad(lambda R: 2 * math.pi * R * (S0HI * math.exp(-4.0 / R - R / 7.0) + S0H2 * math.exp(-12.0 / R - R / 1.5)), 1e-6, 100.0, limit=400)[0]
P(f"  MW gas (McMillan17 HI+H2, P4 shapes, 0-100 kpc) = {MGAS_MW:.4e} Msun; MW M* = {6.6461135288785715e10 - MGAS_MW:.4e} Msun")
GREF = {}
for f in FOOTS:
    U = NS["U0"][f]
    gr = [1.33 * q["meta"]["MHI"] / (U * q["meta"]["L36"]) for q in NS["GALS"].values() if q["meta"]["L36"] > 0 and U * q["meta"]["L36"] * 1e9 <= 1e9]
    GREF[f] = (float(np.median(gr)), len(gr))
    P(f"  [{f}] g_ref = median 1.33 M_HI / (U0 L36) over SPARC with U0 L36 <= 1e9 Msun = {GREF[f][0]:.4f} (N {GREF[f][1]}; U0 {U})")


def sysF(f, cls, r, conv="C1", eps=1.0, cl_mode="ICM"):
    """returns dict(F, Mstar, Mden, sig2, e_fb, Gflag) for one X19 member row."""
    sig2 = r["sigma"] ** 2; Gf = 0; e_icm = 0.0
    if cls in ("SPARC small", "SPARC large", "UMa members"):
        q = NS["GALS"][r["name"]]["meta"]; Ms = NS["U0"][f] * q["L36"] * 1e9; Md = r["M_b"]
    elif cls == "TDGs":
        Ms, Md = TDGM[r["name"]]
    elif cls == "MW disc":
        Md = r["M_b"]; Ms = Md - MGAS_MW
    elif cls == "Groups":
        raise ValueError
    elif cls.startswith("Clusters"):
        row = NS["EF"][NS["EIDX"][r["name"]]]; kT = float(row["KT"])
        if not kT > 0:
            return None
        M500 = float(row["M500"]) * 1e13 * MSUN; R500 = float(row["R500"]) / 1e3 * MPC
        sig2 = G * M500 / (2 * R500) / 1e6
        kT500 = MU * MP * G * M500 / (2 * R500); kt_rt.append(abs(kT500 / (MU * MP) / 1e6 / sig2 - 1))
        kTJ = kT * KEV if cl_mode == "ICM" else max(kT * KEV - kT500, 0.0)
        e_icm = (1 / 1.2) * 1.5 * kTJ / (MU * MP) / 1e6
        Md = r["M_b"]; Ms = 0.2 / 1.2 * Md
    else:                                            # star-only inventories: X1 dwarfs, Coma UDGs, DF2/DF4
        Ms = r["M_b"]
        Gf = 0 if (cls == "LG field" or cls == "bright M31") and r["name"] in GASRICH else 1
        if cls in X1CL and r["name"] in GASRICH:
            Gf = 0
        if conv == "C0":
            Md = Ms
        elif conv == "C2" and Gf == 1:
            Md = Ms / FSTAR_COS
        else:
            Md = Ms * (1 + GREF[f][0])
    e_sn = eps * ESN_PER_MSTAR * Ms / Md
    e = e_sn + e_icm + E_RE
    return dict(F=e / sig2, Mstar=Ms, Mden=Md, sig2=sig2, e_fb=e, e_sn=e_sn, e_icm=e_icm, G=Gf, name=r.get("name", ""))


def group_band(f, eps=1.0):
    lo, hi = [], []
    for r in SYS[f]["Groups"]:
        s2 = r["sigma"] ** 2
        lo.append((eps * ESN_PER_MSTAR * 0.1 + E_RE) / s2); hi.append((eps * ESN_PER_MSTAR * 1.0 + E_RE) / s2)
    return lo, hi


def build(f, conv="C1", eps=1.0, cl_mode="ICM"):
    """per-class member lists of F (and G); groups as band lists."""
    FL, GL, ROWS = {}, {}, {}
    for nm in CLASSES:
        if nm == "Cosmic background":
            continue
        if nm == "Groups":
            lo, hi = group_band(f, eps); FL[nm] = (lo, hi); GL[nm] = [0.0] * len(lo); continue
        rows = [sysF(f, nm, r, conv, eps, cl_mode) for r in SYS[f][nm]]
        rows = [x for x in rows if x is not None]
        ROWS[nm] = rows; FL[nm] = [x["F"] for x in rows]; GL[nm] = [float(x["G"]) for x in rows]
    return FL, GL, ROWS


def intervals_from(FL, GL, strict=False):
    I = {}
    for nm in CLASSES:
        I[nm] = {v: INTX[("canonical", strict)][nm][v] for v in NS["VN"]}       # placeholder, overwritten per footing below
        if nm == "Cosmic background":
            I[nm]["F"] = None; I[nm]["G"] = (0.0, 0.0, 0.0, 0); continue
        if nm == "Groups":
            lo, hi = FL[nm]; a = interval(lo, strict); b = interval(hi, strict)
            I[nm]["F"] = (a[0], b[1], math.sqrt(a[2] * b[2]), len(lo))
        else:
            I[nm]["F"] = interval(FL[nm], strict)
        I[nm]["G"] = interval(GL[nm], strict)
    return I


def full_I(f, FL, GL, strict=False):
    I = intervals_from(FL, GL, strict)
    for nm in CLASSES:
        for v in NS["VN"]:
            I[nm][v] = INTX[(f, strict)][nm][v]
    return I


def spearman_classes(I, T, seed=3131, nperm=20000):
    use = [nm for nm in CLASSES if nm != "Cosmic background" and I[nm]["F"] is not None]
    x = np.array([math.log10(I[nm]["F"][2]) for nm in use]); y = np.array([T[nm]["E"] for nm in use])
    rho = float(spearmanr(x, y)[0]); rng = np.random.default_rng(seed)
    ry = np.argsort(np.argsort(y)).astype(float); rx = np.argsort(np.argsort(x)).astype(float)
    perms = np.array([rng.permutation(len(use)) for _ in range(nperm)])
    a = (rx - rx.mean()) / rx.std(); B = ry[perms]; B = (B - B.mean(1, keepdims=True)) / B.std(1, keepdims=True)
    rp = (B * a[None, :]).mean(1)
    return rho, float(np.mean(rp >= rho - 1e-12)), len(use)


def verdict_cell(I, T, L):
    r = rank_test("F", I, T, L); rho, p, n = spearman_classes(I, T)
    r.update(spearman_rho=rho, spearman_p=p, spearman_n=n)
    if r["status"] == "SEPARATES":
        c = "SEPARATES"
    elif r["status"].startswith("SEPARATES, NOT GRADED") or (rho >= 0.5 and p <= 0.05):
        c = "ORDERS"
    elif r.get("n_extra", 0) < 2 or r.get("n_none", 0) < 2 or r["status"] == "NO CONTRAST":
        c = "UNDECIDED"
    else:
        c = "FAILS"
    r["cls"] = c
    return r


# =====================================================================================================  STEP 1: F per class
RES = dict(lane="X31_feedback_energy_selector", criteria="1aa11f9bcb", amendment_A1="358e3859ed", mutate=MUT, constants=dict(
    eta_SN=ETA, eta_SN_quad=ETA_q, R=R_RET, eps_SN=EPS, E_SN_erg=1e51, T_re=T_RE, e_re_kms2=E_RE, e_SN_per_unit_kms2=ESN_PER_MSTAR,
    f_star_cos=FSTAR_COS, MW_gas=MGAS_MW, g_ref={f: GREF[f][0] for f in FOOTS}, g_ref_N={f: GREF[f][1] for f in FOOTS}))
BUILD = {f: build(f) for f in FOOTS}
k3 = []
FTAB = {}
for f in FOOTS:
    FL, GL, ROWS = BUILD[f]
    FT = {nm: list(v) if nm != "Groups" else v for nm, v in FL.items()}
    if MUT:                                                           # (i) derangement of the F lists across the bound classes
        keys = [nm for nm in CLASSES if nm not in ("Cosmic background", "Groups")]
        rng = np.random.default_rng(3131)
        while True:
            pm = rng.permutation(len(keys))
            if all(pm[i] != i for i in range(len(keys))):
                break
        FT = dict(FT); orig = {k: FL[k] for k in keys}
        for i, k in enumerate(keys):
            FT[k] = list(orig[keys[pm[i]]])
    FTAB[f] = (FT, GL, ROWS)
    for nm in CLASSES:
        if nm in ("Cosmic background", "Groups"):
            continue
        rec = [sysF(f, nm, r)["F"] for r in SYS[f][nm] if sysF(f, nm, r) is not None]
        if abs(np.median(FT[nm]) - np.median(rec)) > 1e-12 * abs(np.median(rec)):
            k3.append(f"{f}|{nm}")
check("K3", not k3, f"{len(k3)} classes whose tabled F median does not recompute from its own members" + (f": {k3}" if k3 else ""), "0 (<= 1e-12 rel)")
check("K1", abs(ETA / ETA_q - 1) <= 1e-6 and abs(s1kev / 399.6 - 1) <= 0.01 and (max(kt_rt) if kt_rt else 0) <= 1e-12,
      f"eta closed form / quadrature - 1 = {ETA / ETA_q - 1:.1e}; sigma(1 keV, mu 0.6) {s1kev:.1f} km/s; kT500 round trip max {max(kt_rt):.1e}", "<= 1e-6; 399.6 +- 1 %; <= 1e-12")

P("\n=== STEP 1: F per class (primary: C1, eps_SN 1; 16-84 % or min-max for N < 3; groups = band M*/M_bar 0.1-1)")
CSVROWS = []
PRIMARY = {}
for f in FOOTS:
    FT, GL, ROWS = FTAB[f]; I = full_I(f, FT, GL); T = TT[(f, "iso")]; Te = TT[(f, "efe")]
    L = labels(T, "LS"); Le = labels(Te, "LS")
    P(f"\n  [{f}]  {'class':18s} {'label iso/efe':14s} {'E_iso':>7s} {'F median':>10s} {'F 16-84 %':>22s} {'log F':>6s} {'N':>4s} {'G':>9s} {'e_fb^0.5':>9s} {'sig_b':>7s}")
    for nm in CLASSES:
        iv = I[nm]["F"]
        if iv is None:
            P(f"         {nm:18s} {L[nm] + '/' + Le[nm]:14s} {T[nm]['E']:+7.3f}  F not placeable (no binding energy)"); continue
        gi = I[nm]["G"]
        if nm == "Groups":
            ef = sg = float("nan")
        else:
            ef = math.sqrt(np.median([x["e_fb"] for x in ROWS[nm]])); sg = math.sqrt(np.median([x["sig2"] for x in ROWS[nm]]))
        P(f"         {nm:18s} {L[nm] + '/' + Le[nm]:14s} {T[nm]['E']:+7.3f} {iv[2]:10.3g} [{iv[0]:9.3g},{iv[1]:9.3g}] {math.log10(iv[2]):6.2f} {iv[3]:4d} "
          f"[{gi[0]:.0f},{gi[1]:.0f}]{gi[2]:.2f} {ef:9.1f} {sg:7.1f}")
        CSVROWS.append(dict(footing=f, cls=nm, label_iso=L[nm], label_efe=Le[nm], E_iso=T[nm]["E"], Z_iso=T[nm]["Z"], E_efe=Te[nm]["E"], Z_efe=Te[nm]["Z"],
                            F_med=iv[2], F_p16=iv[0], F_p84=iv[1], N=iv[3], G_med=gi[2], sqrt_e_fb_med=ef, sigma_b_med=sg))
    PRIMARY[f] = (I, T, L)

# =====================================================================================================  STEP 2: rank test
P("\n=== STEP 2: rank test on log F (X19's rank_test, verbatim); ordering statistic Spearman(log F_med, E), one-sided permutation p")
CELLS = {}


def show(tag, r):
    s = (f"  {tag:44s} {r['cls']:10s} status {r['status']:28s} best {r.get('best_direction')} at log F {r.get('best_threshold_log', float('nan')):+.2f}"
         f" offenders {r.get('offenders')} | rho {r['spearman_rho']:+.3f} p {r['spearman_p']:.4f} (n {r['spearman_n']})")
    if "vstar_log" in r:
        s += f" | F* 10^{r['vstar_log']:.2f}"
    if r.get("grading_violations"):
        s += f" | grading violations {r['grading_violations']}"
    P(s)


def run(tag, f, I, T, L):
    r = verdict_cell(I, T, L); CELLS[f"{tag}|{f}"] = r; show(f"{tag} [{f}]", r); return r


prim = {f: run("PRIMARY B_iso C1 eps1", f, *PRIMARY[f]) for f in FOOTS}
cls_f = {f: prim[f]["cls"] for f in FOOTS}
if STOP:
    VERDICT = "UNDECIDED (step-0 stop rule)"
elif len(set(cls_f.values())) > 1:
    VERDICT = f"UNDECIDED (footings disagree: {cls_f})"
elif cls_f["canonical"] == "SEPARATES":
    VERDICT = "FEEDBACK SEPARATES (threshold F* " + " / ".join(f"10^{prim[f]['vstar_log']:.2f}" for f in FOOTS) + ")"
elif cls_f["canonical"] == "ORDERS":
    VERDICT = "FEEDBACK ORDERS BUT DOES NOT SEPARATE"
elif cls_f["canonical"] == "UNDECIDED":
    VERDICT = "UNDECIDED (too few placeable EXTRA or NONE classes)"
else:
    off = sorted(set(prim["canonical"]["offenders"]) | set(prim["alt"]["offenders"]))
    VERDICT = "FEEDBACK FAILS (offending classes: " + ", ".join(off) + ")"
if MUT:
    VERDICT = "UNDECIDED (MUTATE run)"
P(f"\n  VERDICT: {VERDICT}")

P("\n  Qualifiers (reported, no verdict weight):")
QUAL = {}
for f in FOOTS:
    I, T, L = PRIMARY[f]
    QUAL[f"B_EFE|{f}"] = run("B_EFE", f, I, TT[(f, "efe")], labels(TT[(f, "efe")], "LS"))
    QUAL[f"L-B|{f}"] = run("L-B labels", f, I, T, labels(T, "LB"))
    FT, GL, _ = FTAB[f]
    QUAL[f"strict|{f}"] = run("strict min-max", f, full_I(f, FT, GL, True), T, L)
    for conv in ("C0", "C2"):
        FL, GLc, _ = build(f, conv=conv); QUAL[f"{conv}|{f}"] = run(f"denominator {conv}", f, full_I(f, FL, GLc), T, L)
        QUAL[f"{conv}+B_EFE|{f}"] = run(f"denominator {conv} + B_EFE", f, full_I(f, FL, GLc), TT[(f, "efe")], labels(TT[(f, "efe")], "LS"))
    FL, GLc, _ = build(f, eps=0.1); QUAL[f"eps0.1|{f}"] = run("eps_SN 0.1", f, full_I(f, FL, GLc), T, L)
    FL, GLc, _ = build(f, cl_mode="EXC"); QUAL[f"F_exc|{f}"] = run("clusters F_exc (thermal excess)", f, full_I(f, FL, GLc), T, L)
    FL, GLc, _ = build(f, eps=0.1, cl_mode="EXC"); QUAL[f"eps0.1+F_exc|{f}"] = run("eps_SN 0.1 + F_exc", f, full_I(f, FL, GLc), T, L)

P("\n  Rank test on the gas-expelled flag G alone, and two-variable search (X19's two_var), primary cell:")
TWO = {}
for f in FOOTS:
    I, T, L = PRIMARY[f]
    rG = rank_test("G", I, T, L); TWO[f"G|{f}"] = rG
    P(f"  G alone [{f}]: {rG['status']}; offenders {rG.get('offenders')}")
    for v2 in ["G"] + NS["VN"]:
        b = two_var("F", v2, I, L); TWO[f"F,{v2}|{f}"] = b
        P(f"  (F, {v2:7s}) [{f}]: {'SEPARATES' if b['separates'] else 'no'}; {b['comb']} s ({b['s1']:+d},{b['s2']:+d}) thresholds {b['a']:+.2f}, {b['b']:+.2f}; "
          f"offenders {b['offenders']}" + (f"; incomplete {b['incomplete']}" if b["incomplete"] else ""))
    for v2 in ["G"]:
        b = two_var("F", v2, I, labels(TT[(f, "efe")], "LS")); TWO[f"F,{v2}|B_EFE|{f}"] = b
        P(f"  (F, {v2:7s}) B_EFE [{f}]: {'SEPARATES' if b['separates'] else 'no'}; offenders {b['offenders']}")

def best_up(I, L, var="F"):
    """A2 (post-result, reported only): X19's best-threshold loop restricted to direction UP (the hypothesis: more feedback, more extra)."""
    use = [n for n in CLASSES if L[n] in ("EXTRA", "NONE") and I[n][var] is not None]
    X = {n: (math.log10(I[n][var][0]), math.log10(I[n][var][1])) for n in use}
    EX = [n for n in use if L[n] == "EXTRA"]; NO = [n for n in use if L[n] == "NONE"]
    edges = sorted({X[n][0] for n in use} | {X[n][1] for n in use})
    cands = [edges[0] - 1] + [0.5 * (a + b) for a, b in zip(edges[:-1], edges[1:])] + [edges[-1] + 1]
    best = None
    for t in cands:
        off = [n for n in NO if X[n][1] >= t] + [n for n in EX if X[n][0] <= t]
        if best is None or len(off) < len(best[1]):
            best = (t, off)
    return dict(best_direction="UP", best_threshold_log=best[0], offenders=best[1])


# =====================================================================================================  hard cases
P("\n=== HARD CASES (primary C1, eps 1): F, interval, label, side of the best threshold (B_iso; B_EFE in brackets)")
HARD = {}
for f in FOOTS:
    I, T, L = PRIMARY[f]; r = prim[f]; re_ = QUAL[f"B_EFE|{f}"]; Le = labels(TT[(f, "efe")], "LS")
    rup = best_up(I, L); rupe = best_up(I, Le)
    for nm in ("Crater II", "Antlia II", "DF2/DF4", "TDGs", "Clusters T1", "Clusters T2", "Clusters T3", "MW ultra-faint", "LG field"):
        iv = I[nm]["F"]; lo, hi = math.log10(iv[0]), math.log10(iv[1])

        def side(rr, lab):
            t = rr["best_threshold_log"]; up = rr["best_direction"] == "UP"
            if lab == "AMBIG":
                return "AMBIG (does not constrain)"
            want_high = (lab == "EXTRA") == up
            if (want_high and lo > t) or ((not want_high) and hi < t):
                return "right side"
            if (want_high and hi <= t) or ((not want_high) and lo >= t):
                return "WRONG side"
            return "straddles"
        HARD[f"{f}|{nm}"] = dict(F_med=iv[2], F_lo=iv[0], F_hi=iv[1], label=L[nm], label_efe=Le[nm], side=side(r, L[nm]), side_efe=side(re_, Le[nm]),
                                 side_UP=side(rup, L[nm]), side_UP_efe=side(rupe, Le[nm]))
        P(f"  [{f}] {nm:15s} F {iv[2]:9.3g} [{iv[0]:9.3g}, {iv[1]:9.3g}] (log {math.log10(iv[2]):+.2f}) label {L[nm]:5s} -> {HARD[f'{f}|{nm}']['side']:10s}"
          f" [B_EFE {Le[nm]:5s} -> {HARD[f'{f}|{nm}']['side_efe']}] | hypothesis direction UP: {HARD[f'{f}|{nm}']['side_UP']} [B_EFE {HARD[f'{f}|{nm}']['side_UP_efe']}]")
    P(f"  [{f}] best threshold (B_iso) {r['best_direction']} at F = 10^{r['best_threshold_log']:.2f}; (B_EFE) {re_['best_direction']} at 10^{re_['best_threshold_log']:.2f}")
    P(f"  [{f}] best UP-only threshold (reported, A2): B_iso 10^{rup['best_threshold_log']:.2f} offenders {rup['offenders']}; B_EFE 10^{rupe['best_threshold_log']:.2f} offenders {rupe['offenders']}")
    HARD[f"{f}|UP"] = dict(iso=rup, efe=rupe)

# =====================================================================================================  P1: per-system dwarfs
P("\n=== P1: per-system dwarfs (X20 E and labels joined to X1 M*, sigma; F under C1; reported only)")
X1R = {(r["footing"], r["name"]): r for r in csv.DictReader(open(os.path.join(RB, "X1_hosted_recount", "x1_per_system.csv")))}
X20R = list(csv.DictReader(open(os.path.join(RB, "X20_hosted_dwarf_requirement", "x20_per_system.csv"))))
P1 = {}
for f in FOOTS:
    rows = []
    for r in X20R:
        if r["footing"] != f or (f, r["name"]) not in X1R:
            continue
        x = X1R[(f, r["name"])]; Ms = 10 ** float(x["logMstar"]); s = float(x["sigma"])
        Gf = 0 if r["name"] in GASRICH else 1
        Fv = (ESN_PER_MSTAR / (1 + GREF[f][0]) + E_RE) / s ** 2
        rows.append(dict(name=r["name"], cls=r["cls"], G=Gf, F=Fv, logM=math.log10(Ms), sigma=s, E_iso=float(r["E_B_iso"]), s_iso=float(r["s_B_iso"]),
                         Z_iso=float(r["Z_B_iso"]), lab_iso=r["lab_B_iso"], E_efe=float(r["E_B_EFE"]), s_efe=float(r["s_B_EFE"]), Z_efe=float(r["Z_B_EFE"]), lab_efe=r["lab_B_EFE"]))
    if MUT:
        Fs = [q["F"] for q in rows]; pm = np.random.default_rng(3131).permutation(len(Fs))
        for i, q in enumerate(rows):
            q["F"] = Fs[pm[i]]
    P1[f] = dict(N=len(rows))
    for b in ("iso", "efe"):
        lf = np.array([math.log10(q["F"]) for q in rows]); E = np.array([q[f"E_{b}"] for q in rows]); lm = np.array([q["logM"] for q in rows])
        rF = spearmanr(lf, E); rM = spearmanr(lm, E)
        # X19 rank test on per-system points (CLASSES swapped temporarily in X19's namespace)
        names = [q["name"] for q in rows]; Ipt = {q["name"]: {"F": (q["F"], q["F"], q["F"], 1)} for q in rows}
        Tpt = {q["name"]: dict(E=q[f"E_{b}"], s=q[f"s_{b}"], Z=q[f"Z_{b}"]) for q in rows}
        Lpt = {q["name"]: q[f"lab_{b}"] for q in rows}
        old = NS["CLASSES"]; NS["CLASSES"] = names
        try:
            rp = rank_test("F", Ipt, Tpt, Lpt)
        finally:
            NS["CLASSES"] = old
        gx = [q[f"E_{b}"] for q in rows if q["G"] == 1]; gr = [q[f"E_{b}"] for q in rows if q["G"] == 0]
        mw = mannwhitneyu(gx, gr, alternative="two-sided") if gr and gx else None
        nE = sum(1 for q in rows if q[f"lab_{b}"] == "EXTRA"); nN = sum(1 for q in rows if q[f"lab_{b}"] == "NONE")
        P1[f][b] = dict(spearman_F=float(rF[0]), p_F=float(rF[1]), spearman_M=float(rM[0]), p_M=float(rM[1]), status=rp["status"],
                        n_offenders=rp.get("n_offenders"), best_dir=rp.get("best_direction"), best_thr=rp.get("best_threshold_log"),
                        n_extra=nE, n_none=nN, med_E_G1=float(np.median(gx)), med_E_G0=float(np.median(gr)) if gr else None, n_G1=len(gx), n_G0=len(gr),
                        mw_p=float(mw.pvalue) if mw else None, offenders=rp.get("offenders"))
        q_ = P1[f][b]
        P(f"  [{f}] B_{b}: N {len(rows)} (EXTRA {nE}, NONE {nN}); Spearman(log F, E) {q_['spearman_F']:+.3f} (p {q_['p_F']:.2g}); "
          f"Spearman(log M*, E) {q_['spearman_M']:+.3f} (p {q_['p_M']:.2g}); rank test {q_['status']}, best {q_['best_dir']} at log F {q_['best_thr']:+.2f} "
          f"with {q_['n_offenders']} offenders; median E gas-expelled {q_['med_E_G1']:+.3f} (N {q_['n_G1']}) vs gas-rich {q_['med_E_G0']:+.3f} (N {q_['n_G0']}), MW p {q_['mw_p']:.3f}")
    P1[f]["rows"] = rows

# =====================================================================================================  checks, outputs
P("\n=== CHECKS")
# K2: oracle F_or = 10^E per class, same layout
k2 = []
for f in FOOTS:
    T = ETAB[(f, "iso")]; L = labels(T, "LS")
    Ior = {nm: {"F": (10 ** T[nm]["E"],) * 3 + (1,)} for nm in CLASSES}
    k2.append(rank_test("F", Ior, T, L)["status"])
check("K2", all(s == "SEPARATES" for s in k2), f"oracle 10^E: {k2}", "SEPARATES on both footings")
pk = rss(); check("K4", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB")
npass = sum(c["ok"] for c in CHECKS.values())
P(f"\nX31 class script: {npass}/{len(CHECKS)} checks PASS; verdict {VERDICT}  [{time.time() - T0:.1f} s]")


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        o = o.item()
    if isinstance(o, float) and not math.isfinite(o):
        return str(o)
    return o


RES.update(verdict=VERDICT, primary_class=cls_f, primary=CELLS, qualifiers=QUAL, two_var=TWO, hard_cases=HARD,
           P1={f: {k: v for k, v in P1[f].items()} for f in FOOTS}, class_table=CSVROWS,
           checks=CHECKS, runtime_s=time.time() - T0, peak_rss_GB=pk)
json.dump(clean(RES), open(os.path.join(HERE, f"x31_feedback_energy_selector_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"x31_feedback_energy_selector{TAG}.out"), "w").write(
    "\n".join(OUTL).replace(REPO, "<repo>").replace(os.path.dirname(REPO), "<parent>") + "\n")
with open(os.path.join(HERE, f"x31_classes{TAG}.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(CSVROWS[0].keys())); w.writeheader(); w.writerows(CSVROWS)
sys.exit(0 if npass == len(CHECKS) and not MUT else 1)
