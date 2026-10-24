"""X20_hosted_dwarf_requirement -- per-system rank test of the required extra in X1's 89 LG systems.

Criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (8a6247efea, committed alone first).
kappa = 1/2 FITTED. Footings canonical / alt, never pooled. No dark-matter particle. Not "theory closed".

X1's code path (load_lvd, build, pred_draws for iso0/emb0, boot_ix, boot_median, klass, seed and RNG-call order of
stage_final) is COPIED with provenance from rebuild_2026_10_22/X1_hosted_recount/x1_hosted_recount.py (commit c74c622229).
Z2's member-count rule is copied from rebuild_2026_10_22/Z2_satellite_systematics (14be14f282), without its N_eff fallback.
Inputs are read only. No downloads. No fit, no scan.

Run:  OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 15 python3 x20_hosted_dwarf_requirement.py      (X20_MUTATE=1 for the twin)
"""
import csv, json, math, os, resource, sys, time
import numpy as np
from scipy import stats as SS
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
X1D = os.path.join(REPO, "rebuild_2026_10_22", "X1_hosted_recount")
Z2D = os.path.join(REPO, "rebuild_2026_10_22", "Z2_satellite_systematics")
DATA = os.path.join(REPO, "real_research", "data")
CFG = os.path.join(REPO, "campaign_fresh_gravity")
MUT = os.environ.get("X20_MUTATE", "") == "1"
SFX = "_MUTATE" if MUT else ""
T0 = time.time()
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
CHK = {}
def check(k, ok, val, thr, what):
    CHK[k] = dict(ok=bool(ok), value=val, threshold=thr, what=what)
    P(f"{k} {'PASS' if ok else 'FAIL'} {val} {thr}  ({what})")
def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)

# ------------------------------------------------------------------ X1 constants (copied)
G, MSUN, PC = 6.67430e-11, 1.989e30, 3.0856775814913673e16
KPC = 1e3 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
A_H = 3.0 * KPC
MHOST = {"MW": 6.0e10, "M31": 1.0e11, "field": 6.0e10}
NMC, NBOOT = 2000, 4000
DY = 0.6
R12 = 4.0 / 3.0
UPS_PRIOR = 0.15
KISO, KEFE = "iso AQUAL L*0", "AQUAL + EFE L*0 (exact MOND + EFE)"
BASES = {"B_iso": ("iso0", KISO), "B_EFE": ("emb0", KEFE)}

def lin3(x, xs, v):
    x = np.asarray(x, float)
    s0 = (v[1] - v[0]) / (xs[1] - xs[0]); s1 = (v[2] - v[1]) / (xs[2] - xs[1])
    return np.where(x < xs[1], v[1] + s0 * (x - xs[1]), v[1] + s1 * (x - xs[1]))
def g_host(R_m, Mb, a0):
    gN = G * Mb * MSUN / (R_m + A_H) ** 2
    return 0.5 * gN * (1 + math.sqrt(1 + 4 * a0 / gN))
def fl(x):
    try:
        v = float(x); return v if math.isfinite(v) else None
    except Exception:
        return None
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
                             dhost=fl(r.get("distance_host")), dist=fl(r.get("distance")),
                             mv=mv, dm31=fl(r.get("distance_m31")),
                             # X20 extras (not used by X1's build)
                             ref=r.get("ref_vlos", ""), ell=fl(r.get("ellipticity")),
                             sem_raw=fl(r.get("vlos_sigma_em")), sep_raw=fl(r.get("vlos_sigma_ep"))))
    return rows
ALL = load_lvd()
ARR = list(csv.DictReader(open(os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}
arr_f07 = {r["lvd_name"]: float(r["sig_f07"]) / float(r["sig_f0"]) for r in ARR}
med_free = float(np.median(list(arr_free.values()))); med_f07 = float(np.median(list(arr_f07.values())))
GEH = {}; GEHN = {}
for r in csv.DictReader(open(os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "geha_vs_lvd_match.csv"))):
    if r.get("geha_N_stars"):
        GEHN[r["lvd_name"]] = int(float(r["geha_N_stars"]))
    if r.get("geha_sigma_resolved") == "1" and fl(r.get("geha_sigma")):
        GEH[r["lvd_name"]] = (float(r["geha_sigma"]), fl(r.get("geha_e_sigma_ll")) or 0.1, fl(r.get("geha_e_sigma_ul")) or 0.1)
GEH2 = {r["full_name"]: r for r in csv.DictReader(open(os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "geha2026_paperII_tableA1.csv")))}

def split_normal(rng, c, em, ep, n):
    z = rng.standard_normal(n); return c + np.where(z < 0, z * em, z * ep)
def binfactor(r, binmode="free", mvrule=True):
    ufd = (r["mv"] is not None and r["mv"] > -7.7)
    if binmode == "free": return arr_free.get(r["name"], med_free if (ufd or not mvrule) else 1.0)
    if binmode == "f07": return arr_f07.get(r["name"], med_f07 if (ufd or not mvrule) else 1.0)
    return 1.0
def build(rows, a0, rng, ups=2.0, binmode="free", sig_src="lvd", drop_ul=False, mvrule=False):
    """X1's (S1's) build, copied."""
    keep = [r for r in rows if not (drop_ul and r["ul"])]
    N = len(keep)
    lb = np.empty((N, NMC)); ly = np.empty((N, NMC)); la = np.empty((N, NMC))
    for i, r in enumerate(keep):
        s, sem, sep = r["sigma"], r["sem"], r["sep"]
        if sig_src == "lower" and r["name"] in GEH:
            gs, gl, gu = GEH[r["name"]]
            if gs < s: s, sem, sep = gs, gl, gu
        b = binfactor(r, binmode, mvrule)
        fD = 10 ** (split_normal(rng, 0.0, r["dmem"], r["dmep"], NMC) / 5.0)
        sig = np.abs(split_normal(rng, s, sem, sep, NMC)) * b
        rh = np.abs(split_normal(rng, r["rh"], r["rhem"], r["rhep"], NMC)) * fD
        ms = ups / 2.0 * 10 ** r["logms"] * fD ** 2
        r12 = R12 * rh * PC
        gobs = 3.0 * (sig * 1e3) ** 2 / r12; gbar = G * (ms / 2) * MSUN / r12 ** 2
        lb[i] = np.log10(gobs / gbar)
        ly[i] = np.log10(G * ms * MSUN / ((rh * PC) ** 2 * a0)); la[i] = np.log10(rh)
    return dict(lb=lb, ly=ly, la=la, rows=keep)
def boot_ix(rng, N):
    return rng.integers(0, N, (NBOOT, N)), rng.integers(0, NMC, (NBOOT, N))
def boot_median(X, ix):
    idx, col = ix
    meds = np.median(X[idx, col], axis=1)
    return float(np.median(meds)), float(np.std(meds))
def pred_draws(TABf, X, key, est=0):
    out = np.empty_like(X["lb"])
    for i, r in enumerate(X["rows"]):
        t = TABf[r["name"]]
        out[i] = lin3(X["ly"][i], t["ys"], np.asarray(t[key])[:, est])
    return out
CLASSICAL = {"Carina", "Draco", "Fornax", "Leo I", "Leo II", "Sculptor", "Sextans", "Ursa Minor"}
INDIV = ["Crater II", "Antlia II", "Canes Venatici I", "Sagittarius"]
EXCL = {"LMC", "SMC", "M 32"}
DES = {"NGC 147", "NGC 185", "NGC 205"}
def klass(r):
    n = r["name"]
    if n in EXCL: return None
    if r["host"] == "MW":
        if n in CLASSICAL: return "MW classical"
        if n in INDIV: return "indiv:" + n
        if r["mv"] is not None and r["mv"] > -7.7: return "MW ultra-faint"
        return "MW other"
    if r["host"] == "M31":
        if n in DES: return "M31 dE"
        return "bright M31" if r["logms"] >= 5.0 else "M31 others"
    return "LG field"

# ------------------------------------------------------------------ Z2's member-count rule (copied, no N_eff fallback)
COLL = {}
for line in open(os.path.join(DATA, "dsph", "collins2013_m31_dsph.tsv")):
    if line.startswith("#") or not line.strip(): continue
    p_ = line.rstrip("\n").split("\t")
    if len(p_) > 4 and p_[1].strip().startswith("And"):
        try: COLL["Andromeda " + p_[1].strip()[4:].strip()] = int(p_[4])
        except ValueError: pass
COLL["Cassiopeia II"] = COLL.get("Andromeda XXX")
def ref_key(s):
    s = s.replace("+", "").replace(" ", "")
    i = 0
    while i < len(s) and s[i].isalpha(): i += 1
    return (s[:i].lower(), s[i:i + 4])
def nstar(r):
    ref = r["ref"]
    if ref.startswith("Geha2026"):
        if r["name"] in GEHN: return GEHN[r["name"]], "Geha II"
        if r["name"] in GEH2: return int(GEH2[r["name"]]["N_stars"]), "Geha II"
        return None, "Geha-cited, absent from Geha II"
    if ref.startswith("Collins2013") and COLL.get(r["name"]):
        return COLL[r["name"]], "Collins 2013"
    for a in ARR:
        if a["lvd_name"] == r["name"] and ref_key(a["ref"]) == (ref_key(ref)[0], ref_key(ref)[1]):
            return int(a["N_stars"]), "Arroyo-Polonio (same dataset)"
    return None, "none on disk"

# ================================================================== step 0: rebuild X1's draws (same RNG order)
P("=" * 110)
P("X20_hosted_dwarf_requirement -- per-system rank test of the required extra (X1's 89 LG systems)" + ("   [MUTATE]" if MUT else ""))
P("criteria 8a6247efea + AMENDMENT_A1 (check code); kappa = 1/2 FITTED; footings never pooled; not theory closed")
P("=" * 110)
SMP = [r for r in ALL if klass(r) is not None]
TB = {f: json.load(open(os.path.join(X1D, f"x1_stage_tables_{f}.json")))["tables"] for f in FOOTS}
RNG = np.random.default_rng(20261031)
DS = {}
for f in FOOTS:
    DS[(f, "primary")] = build(SMP, A0[f], RNG, mvrule=True)
    DS[(f, "W")] = build(SMP, A0[f], RNG, ups=4.0, binmode="f07", sig_src="lower", drop_ul=True, mvrule=True)
groups = {}
for r in SMP:
    groups.setdefault(klass(r), []).append(r["name"])
IXS = {}
for f in FOOTS:
    for ds in ("primary", "W"):
        X = DS[(f, ds)]
        for g, mem in sorted(groups.items()):
            IXS[(f, ds, tuple(sorted(mem)))] = boot_ix(RNG, len([r for r in X["rows"] if r["name"] in mem]))
ROWS = {}
for f in FOOTS:
    X = DS[(f, "primary")]
    ROWS[(f, KISO)] = X["lb"] - pred_draws(TB[f], X, "iso0")
    ROWS[(f, KEFE)] = X["lb"] - pred_draws(TB[f], X, "emb0")
names = [r["name"] for r in DS[("canonical", "primary")]["rows"]]
NS = len(names)
P(f"sample: {NS} systems; classes " + ", ".join(f"{k} {len(v)}" for k, v in sorted(groups.items())))
if MUT:
    rm = np.random.default_rng(777)
    for f in FOOTS:
        perm = rm.permutation(NS)
        for key in (KISO, KEFE):
            ROWS[(f, key)] = ROWS[(f, key)][perm]
    P("MUTATE: per-system rows of the B_iso and B_EFE draw arrays shuffled across systems (seed 777, per footing)")

X1CSV = {(r["footing"], r["name"]): r for r in csv.DictReader(open(os.path.join(X1D, "x1_per_system.csv")))}
X1J = json.load(open(os.path.join(X1D, "x1_hosted_recount_results.json")))
P("\n--- step 0: X1 reproduced ---")
mx0 = 0.0; nmis = 0
for f in FOOTS:
    for i, n in enumerate(names):
        c = X1CSV[(f, n)]
        for key in (KISO, KEFE):
            v = ROWS[(f, key)][i]
            d = max(abs(float(np.median(v)) - float(c[f"Delta[{key}]"])), abs(float(np.std(v)) - float(c[f"sdMC[{key}]"])))
            mx0 = max(mx0, d); nmis += d > 1e-9
check("K0", nmis == 0 and len(X1CSV) == 2 * NS, f"max |diff| {mx0:.2e}, {nmis} mismatches over {2 * NS} system-footings x 2 baselines",
      "<= 1e-9 dex", "per-system B_iso/B_EFE median and sd reproduce x1_per_system.csv")
mx1 = 0.0; nmis1 = 0; K1ROWS = {}
for f in FOOTS:
    X = DS[(f, "primary")]
    for g, mem in sorted(groups.items()):
        idx = [i for i, r in enumerate(X["rows"]) if r["name"] in mem]
        for key in (KISO, KEFE):
            m, s = boot_median(ROWS[(f, key)][idx], IXS[(f, "primary", tuple(sorted(mem)))])
            ref = X1J["class_stats"][f"{f}|{g}|primary|{key}"]
            d = max(abs(m - ref["median"]), abs(s - ref["sd"]))
            mx1 = max(mx1, d); nmis1 += d > 1e-9
            K1ROWS[f"{f}|{g}|{key}"] = dict(median=m, sd=s, x1_median=ref["median"], x1_sd=ref["sd"])
check("K1", nmis1 == 0, f"max |diff| {mx1:.2e}, {nmis1} mismatches over {len(K1ROWS)} class-baseline-footing cells", "<= 1e-9",
      "X1 bootstrap class medians and sd reproduced")
for f in FOOTS:
    P(f"   [{f}] " + "; ".join(f"{g} iso {K1ROWS[f'{f}|{g}|{KISO}']['median']:+.3f} EFE {K1ROWS[f'{f}|{g}|{KEFE}']['median']:+.3f}"
                        for g in ["MW classical", "MW ultra-faint", "bright M31", "M31 others", "M31 dE", "LG field",
                                  "indiv:Crater II", "indiv:Antlia II", "indiv:Canes Venatici I", "indiv:Sagittarius"]))
STOP = not (CHK["K0"]["ok"] and CHK["K1"]["ok"])

# ================================================================== step 1: per-system E, s, Z, variables
Z2 = {}
for r in csv.DictReader(open(os.path.join(Z2D, "z2_per_system.csv"))):
    Z2[(r["footing"], r["name"])] = r
BYN = {r["name"]: r for r in SMP}
def fam(ref):
    k = ref_key(ref)[0]
    return k if k else "none"
FAMCOUNT = {}
for n in names: FAMCOUNT[fam(BYN[n]["ref"])] = FAMCOUNT.get(fam(BYN[n]["ref"]), 0) + 1
def vesc_b(M, rh_pc):
    a = rh_pc * PC; r = R12 * a
    return math.sqrt(2 * G * M * MSUN / math.sqrt(r * r + a * a)) / 1e3
PER = {}
for f in FOOTS:
    a0 = A0[f]; rows = []
    for i, n in enumerate(names):
        r = BYN[n]; t = TB[f][n]
        d = dict(footing=f, name=n, host=r["host"], cls=klass(r), hosted=int(r["host"] in ("MW", "M31")))
        for bl, (tk, key) in BASES.items():
            v = ROWS[(f, key)][i]
            T = np.asarray(t[tk])
            k = abs(1.0 + (T[2, 0] - T[0, 0]) / (2 * DY))
            E = float(np.median(v)); sd = float(np.std(v)); s = math.hypot(sd, UPS_PRIOR * k)
            Z = E / s
            d.update({f"E_{bl}": E, f"sdMC_{bl}": sd, f"k_{bl}": k, f"s_{bl}": s, f"Z_{bl}": Z,
                      f"lab_{bl}": "EXTRA" if Z >= 2 else ("NONE" if Z < 1 else "AMBIG")})
        M = 10 ** r["logms"]; rh = r["rh"]; r12 = R12 * rh * PC
        x = G * (M / 2) * MSUN / r12 ** 2 / a0
        Rm = t["Rh_kpc"] * KPC
        vrel = math.sqrt(g_host(Rm, MHOST[r["host"]], a0) * Rm) / 1e3
        ve = vesc_b(M, rh)
        z2 = Z2.get((f, n))
        qi = qe = None
        if z2 is not None and z2["pm"] == "True":
            qi = fl(z2["q_ISO"]); qe = fl(z2["q_MOND"])
        ns, nsrc = nstar(r)
        b = binfactor(r, "free", True)
        ds_ = None
        if r["sem_raw"] is not None and r["sep_raw"] is not None:
            ds_ = 0.5 * (r["sem_raw"] + r["sep_raw"]) / r["sigma"]
        d.update(P0_logMstar=r["logms"], P1_logrh=math.log10(rh), P2_logSigma=math.log10(M / (2 * math.pi * rh * rh)),
                 P3_logx=math.log10(x), P4_loge=math.log10(t["xe"]["E_mid"]), P5_logx_over_e=math.log10(x / t["xe"]["E_mid"]),
                 P6_logVrel_Vesc=math.log10(vrel / ve), Vrel_kms=vrel, Vesc_b_kms=ve,
                 P7_logq_iso=math.log10(qi) if qi and qi > 0 else None, P7_logq_efe=math.log10(qe) if qe and qe > 0 else None,
                 P8_ell=r["ell"], P9_logdhost=math.log10(t["Rh_kpc"]),
                 M1_logdsig=math.log10(ds_) if ds_ else None, M2_logNstar=math.log10(ns) if ns else None, Nstar=ns, Nstar_src=nsrc,
                 M3_logb=math.log10(b), M3f_binflag=int(b != 1.0), M4_family=fam(r["ref"]) if FAMCOUNT[fam(r["ref"])] >= 3 else "other",
                 ref_vlos=r["ref"], x1_E_iso=float(X1CSV[(f, n)][f"Delta[{KISO}]"]))
        rows.append(d)
    PER[f] = rows

PVARS = ["P0_logMstar", "P1_logrh", "P2_logSigma", "P3_logx", "P4_loge", "P5_logx_over_e", "P6_logVrel_Vesc", "P7_logq", "P8_ell", "P9_logdhost"]
MVARS = ["M1_logdsig", "M2_logNstar", "M3_logb", "M3f_binflag"]
CATV = "M4_family"

# ================================================================== statistics
def rank2d(A):
    return SS.rankdata(A, axis=1)
def spearman_rows(Vb, Eb):
    rv = rank2d(Vb); re = rank2d(Eb)
    rv = rv - rv.mean(1, keepdims=True); re = re - re.mean(1, keepdims=True)
    den = np.sqrt((rv * rv).sum(1) * (re * re).sum(1))
    with np.errstate(invalid="ignore", divide="ignore"):
        return (rv * re).sum(1) / den
NB = 2000
def corr_cell(V, E, s, seed):
    V = np.asarray(V, float); E = np.asarray(E, float); s = np.asarray(s, float)
    N = len(V)
    rho = float(SS.spearmanr(V, E)[0]); tau = float(SS.kendalltau(V, E)[0])
    rg = np.random.default_rng(seed)
    idx = rg.integers(0, N, (NB, N))
    Eb = E[idx] + s[idx] * rg.standard_normal((NB, N))
    rb = spearman_rows(V[idx], Eb)
    rb = rb[np.isfinite(rb)]
    sd = float(np.std(rb))
    tb = np.array([SS.kendalltau(V[idx[j]], Eb[j])[0] for j in range(0, NB, 4)])
    tb = tb[np.isfinite(tb)]
    rp = np.random.default_rng(seed + 1)
    perm = np.array([rp.permutation(E) for _ in range(NB)])
    rperm = spearman_rows(np.broadcast_to(V, (NB, N)), perm)
    p = float((np.sum(np.abs(rperm) >= abs(rho)) + 1) / (NB + 1))
    return dict(N=N, rho=rho, sd=sd, z=abs(rho) / sd if sd > 0 else float("inf"), tau=tau, tau_sd=float(np.std(tb)), p_perm=p)
def kw_cell(cats, E, seed):
    cats = np.asarray(cats); E = np.asarray(E, float)
    levels = sorted(set(cats))
    def H(Ev):
        return SS.kruskal(*[Ev[cats == c] for c in levels])[0]
    h = float(H(E)); rp = np.random.default_rng(seed)
    hp = np.array([H(rp.permutation(E)) for _ in range(NB)])
    p = float((np.sum(hp >= h) + 1) / (NB + 1))
    z = float(SS.norm.isf(p / 2))
    meds = {c: float(np.median(E[cats == c])) for c in levels}
    ns = {c: int(np.sum(cats == c)) for c in levels}
    return dict(N=len(E), H=h, p_perm=p, z=z, levels=levels, medians=meds, counts=ns)
def separation(V, lab):
    V = np.asarray(V, float); lab = np.asarray(lab)
    m = lab != "AMBIG"; V = V[m]; L = lab[m] == "EXTRA"
    nE, nN = int(L.sum()), int((~L).sum())
    if nE == 0 or nN == 0:
        return dict(nE=nE, nN=nN, offenders=None, separates=False, auc=None)
    u = np.unique(V); cuts = np.concatenate([[u[0] - 1], 0.5 * (u[1:] + u[:-1]), [u[-1] + 1]])
    best = (10 ** 9, None, None)
    for c in cuts:
        above = V > c
        o1 = int(np.sum(above & ~L) + np.sum(~above & L))     # EXTRA above
        o2 = int(np.sum(~above & ~L) + np.sum(above & L))     # EXTRA below
        if o1 < best[0]: best = (o1, float(c), "EXTRA above")
        if o2 < best[0]: best = (o2, float(c), "EXTRA below")
    auc = float(SS.mannwhitneyu(V[L], V[~L]).statistic / (nE * nN))
    rg = np.random.default_rng(99); aucs = []
    for _ in range(500):
        ii = rg.integers(0, len(V), len(V)); Lb = L[ii]
        if Lb.sum() and (~Lb).sum():
            aucs.append(SS.mannwhitneyu(V[ii][Lb], V[ii][~Lb]).statistic / (Lb.sum() * (~Lb).sum()))
    return dict(nE=nE, nN=nN, offenders=best[0], threshold=best[1], orient=best[2],
                separates=bool(best[0] == 0 and nE >= 3 and nN >= 3), auc=auc, auc_sd=float(np.std(aucs)))
def vcol(rows, v, bl):
    if v == "P7_logq":
        return [r["P7_logq_iso" if bl == "B_iso" else "P7_logq_efe"] for r in rows]
    return [r[v] for r in rows]
def partial(E, A, B, s, seed):
    """partial Spearman of E on A controlling B (rank-residual), bootstrap sd with E redrawn."""
    E = np.asarray(E, float); A = np.asarray(A, float); B = np.asarray(B, float); s = np.asarray(s, float)
    def pc(e, a, b):
        re, ra, rb = SS.rankdata(e), SS.rankdata(a), SS.rankdata(b)
        X = np.vstack([np.ones_like(rb), rb]).T
        r1 = re - X @ np.linalg.lstsq(X, re, rcond=None)[0]; r2 = ra - X @ np.linalg.lstsq(X, ra, rcond=None)[0]
        return float(np.corrcoef(r1, r2)[0, 1])
    v = pc(E, A, B); rg = np.random.default_rng(seed); N = len(E); bs = []
    for _ in range(500):
        ii = rg.integers(0, N, N); bs.append(pc(E[ii] + s[ii] * rg.standard_normal(N), A[ii], B[ii]))
    bs = np.array(bs); bs = bs[np.isfinite(bs)]; sd = float(np.std(bs))
    return dict(partial=v, sd=sd, z=abs(v) / sd if sd > 0 else 0.0)

RES = {}
SEED = 2026102401
cellno = 0
if not STOP:
    for f in FOOTS:
        for samp in ("HOSTED", "ALL"):
            rows = [r for r in PER[f] if (samp == "ALL" or r["hosted"])]
            for bl in BASES:
                cell = {}
                for v in PVARS + MVARS:
                    col = vcol(rows, v, bl)
                    sel = [i for i, c in enumerate(col) if c is not None]
                    V = [col[i] for i in sel]; E = [rows[i][f"E_{bl}"] for i in sel]; s = [rows[i][f"s_{bl}"] for i in sel]
                    lab = [rows[i][f"lab_{bl}"] for i in sel]
                    cellno += 1
                    c = corr_cell(V, E, s, SEED + cellno) if len(sel) >= 3 else dict(N=len(sel))
                    c["graded"] = len(sel) >= 10
                    if len(sel) >= 3: c["sep"] = separation(V, lab)
                    cell[v] = c
                cellno += 1
                cell[CATV] = kw_cell([r[CATV] for r in rows], [r[f"E_{bl}"] for r in rows], SEED + cellno)
                cell[CATV]["graded"] = True
                labs = [r[f"lab_{bl}"] for r in rows]
                cell["_labels"] = {k: labs.count(k) for k in ("EXTRA", "AMBIG", "NONE")}
                RES[f"{f}|{samp}|{bl}"] = cell

# ------------------------------------------------------------------ verdict per cell
def cell_class(f, samp, bl):
    c = RES[f"{f}|{samp}|{bl}"]
    zP = max(((c[v]["z"], v) for v in PVARS if c[v].get("graded") and "z" in c[v]), default=(0.0, None))
    zM = max([(c[v]["z"], v) for v in MVARS if c[v].get("graded") and "z" in c[v]] + [(c[CATV]["z"], CATV)], default=(0.0, None))
    sepP = [v for v in PVARS if c[v].get("graded") and c[v].get("sep", {}).get("separates")]
    sepM = [v for v in MVARS if c[v].get("graded") and c[v].get("sep", {}).get("separates")]
    nEi = RES[f"{f}|{samp}|B_iso"]["_labels"]["EXTRA"]; nEe = RES[f"{f}|{samp}|B_EFE"]["_labels"]["EXTRA"]
    if bl == "B_iso" and nEi < 3 and nEe >= 3:
        return dict(cls="BASELINE-DRIVEN", V=None, zP=zP, zM=zM, sepP=sepP, sepM=sepM)
    if zM[0] >= 3 and zM[0] >= zP[0]:
        return dict(cls="MEASUREMENT-DRIVEN", V=zM[1], zP=zP, zM=zM, sepP=sepP, sepM=sepM)
    if (zP[0] >= 3 or sepP) and zP[0] > zM[0]:
        return dict(cls="PHYSICAL SELECTOR", V=zP[1] if zP[0] >= 3 else sepP[0], zP=zP, zM=zM, sepP=sepP, sepM=sepM)
    if zP[0] < 3 and zM[0] < 3 and not sepP and not sepM:
        return dict(cls="NO ORDERING", V=None, zP=zP, zM=zM, sepP=sepP, sepM=sepM)
    return dict(cls="UNDECIDED", V=None, zP=zP, zM=zM, sepP=sepP, sepM=sepM)

VERD = {}
if not STOP:
    for f in FOOTS:
        for samp in ("HOSTED", "ALL"):
            for bl in BASES:
                VERD[f"{f}|{samp}|{bl}"] = cell_class(f, samp, bl)
    # collinearity on the verdict cell
    COLL_Q = {}
    for f in FOOTS:
        vc = VERD[f"{f}|HOSTED|B_iso"]
        bp = vc["zP"][1]; bm = vc["zM"][1]
        rows = [r for r in PER[f] if r["hosted"]]
        if bp and bm and bm != CATV:
            ca = vcol(rows, bp, "B_iso"); cb = vcol(rows, bm, "B_iso")
            sel = [i for i in range(len(rows)) if ca[i] is not None and cb[i] is not None]
            A = [ca[i] for i in sel]; B = [cb[i] for i in sel]
            E = [rows[i]["E_B_iso"] for i in sel]; s = [rows[i]["s_B_iso"] for i in sel]
            mut = float(SS.spearmanr(A, B)[0])
            pA = partial(E, A, B, s, SEED + 9001); pB = partial(E, B, A, s, SEED + 9002)
            COLL_Q[f] = dict(best_P=bp, best_M=bm, N=len(sel), mutual_rho=mut, partial_P_given_M=pA, partial_M_given_P=pB,
                             confounded=bool(abs(mut) >= 0.5 and pA["z"] < 2 and pB["z"] < 2))
        else:
            COLL_Q[f] = dict(best_P=bp, best_M=bm, note="categorical or missing best variable: partial not defined", confounded=False)
    # also: every P vs every M partial for the top P and top complete M (M1), reported
    PART_M1 = {}
    for f in FOOTS:
        rows = [r for r in PER[f] if r["hosted"]]
        for v in PVARS:
            ca = vcol(rows, v, "B_iso"); cb = vcol(rows, "M1_logdsig", "B_iso")
            sel = [i for i in range(len(rows)) if ca[i] is not None and cb[i] is not None]
            if len(sel) < 10: continue
            A = [ca[i] for i in sel]; B = [cb[i] for i in sel]; E = [rows[i]["E_B_iso"] for i in sel]; s = [rows[i]["s_B_iso"] for i in sel]
            PART_M1[f"{f}|{v}"] = dict(P_given_M1=partial(E, A, B, s, SEED + 9100), M1_given_P=partial(E, B, A, s, SEED + 9200),
                                       mutual_rho=float(SS.spearmanr(A, B)[0]), N=len(sel))

# ================================================================== checks K2-K6
P("\n--- checks ---")
if True:   # K2 is computed even under the stop rule, so that the MUTATE twin tests its content
    k2 = []
    for f in FOOTS:
        rows = [r for r in PER[f] if r["hosted"]]
        V = [r["x1_E_iso"] for r in rows]
        c = corr_cell(V, [r["E_B_iso"] for r in rows], [r["s_B_iso"] for r in rows], SEED + 7)
        # A1 (post-result, check code only): labels are defined on Z = E/s, so the separation oracle is Z from the CSV's E
        sp = separation([r["x1_E_iso"] / r["s_B_iso"] for r in rows], [r["lab_B_iso"] for r in rows])
        k2.append((f, c["z"], c["rho"], sp["separates"], sp["offenders"]))
    check("K2", all(z >= 3 and sep for _, z, _, sep, _ in k2), "; ".join(f"{f}: rho {r:+.3f} z {z:.1f} separates {sep} (offenders {o})" for f, z, r, sep, o in k2),
          "z >= 3 and SEPARATES", "oracle V = x1_per_system.csv E column (z) and E/s_i (separation, A1) (positive control)")
rows = [r for r in PER["canonical"] if r["hosted"]]
rgn = np.random.default_rng(31337); fa = 0
for j in range(200):
    c = corr_cell(rgn.standard_normal(len(rows)), [r["E_B_iso"] for r in rows], [r["s_B_iso"] for r in rows], 50000 + j)
    fa += c["z"] >= 3
check("K3", fa / 200 <= 0.05, f"false-alarm rate {fa / 200:.3f} ({fa}/200)", "<= 0.05", "null random V")
rgk = np.random.default_rng(5); a_ = rgk.standard_normal(40); b_ = a_ + rgk.standard_normal(40)
mine = float(spearman_rows(a_[None, :], b_[None, :])[0]); ref = float(SS.spearmanr(a_, b_)[0])
tied = np.round(a_, 0); mine2 = float(spearman_rows(tied[None, :], b_[None, :])[0]); ref2 = float(SS.spearmanr(tied, b_)[0])
check("K4", abs(mine - ref) < 1e-12 and abs(mine2 - ref2) < 1e-12, f"{abs(mine - ref):.1e}, ties {abs(mine2 - ref2):.1e}", "< 1e-12",
      "vectorised Spearman equals scipy.stats.spearmanr (with ties)")
k5 = 0.0
for n in ("Draco", "Crater II", "Segue 1"):
    if n not in BYN: continue
    r = BYN[n]; M = 10 ** r["logms"]; a = r["rh"] * PC; rr = R12 * a
    gN = lambda x: G * M * MSUN * x / (x * x + a * a) ** 1.5
    phi = quad(gN, rr, 1e4 * rr, limit=200)[0] + G * M * MSUN / math.sqrt((1e4 * rr) ** 2 + a * a)
    k5 = max(k5, abs(math.sqrt(2 * phi) / 1e3 / vesc_b(M, r["rh"]) - 1))
check("K5", k5 <= 1e-6, f"max rel diff {k5:.1e}", "<= 1e-6", "Plummer V_esc,b closed form vs numerical integral")
check("K6", rss_gb() < 1.0, f"{rss_gb():.3f} GB", "< 1 GB", "peak RSS")

# ================================================================== print
SHORT = {"P0_logMstar": "log M*", "P1_logrh": "log r_half", "P2_logSigma": "log Sigma", "P3_logx": "log x", "P4_loge": "log e",
         "P5_logx_over_e": "log x/e", "P6_logVrel_Vesc": "log Vrel/Vesc", "P7_logq": "log q (peri)", "P8_ell": "ellipticity",
         "P9_logdhost": "log d_host", "M1_logdsig": "log dsig/sig", "M2_logNstar": "log N*", "M3_logb": "log b (binary)",
         "M3f_binflag": "binary flag", "M4_family": "source family"}
if not STOP:
    for f in FOOTS:
        P(f"\n--- [{f}] per-system labels (HOSTED): " + "; ".join(f"{bl} " + ", ".join(f"{k} {v}" for k, v in RES[f'{f}|HOSTED|{bl}']['_labels'].items()) for bl in BASES))
        for samp in ("HOSTED", "ALL"):
            for bl in BASES:
                c = RES[f"{f}|{samp}|{bl}"]
                P(f"\n   [{f} | {samp} | {bl}]  {'var':16s} {'N':>3s} {'rho_S':>7s} {'sd':>6s} {'z':>5s} {'tau_b':>7s} {'sd':>6s} {'p_perm':>7s}  sep: off/nE/nN  AUC+-sd")
                for v in PVARS + MVARS:
                    d = c[v]
                    if "rho" not in d:
                        P(f"   {'':30s}{SHORT[v]:16s} {d['N']:3d}  (too few)"); continue
                    sp = d.get("sep", {})
                    sps = (f"{sp.get('offenders')}/{sp.get('nE')}/{sp.get('nN')}" + (" SEP" if sp.get("separates") else "")
                           + (f"  {sp['auc']:.2f}+-{sp['auc_sd']:.2f}" if sp.get("auc") is not None else ""))
                    P(f"   {'':30s}{SHORT[v]:16s} {d['N']:3d} {d['rho']:+7.3f} {d['sd']:6.3f} {d['z']:5.1f} {d['tau']:+7.3f} {d['tau_sd']:6.3f} {d['p_perm']:7.4f}  {sps}"
                      + ("" if d["graded"] else "  [not graded, N<10]"))
                k = c[CATV]
                P(f"   {'':30s}{SHORT[CATV]:16s} {k['N']:3d}  KW H {k['H']:.2f}  p_perm {k['p_perm']:.4f}  z {k['z']:.2f}  medians " +
                  ", ".join(f"{l} {k['medians'][l]:+.2f} (n{k['counts'][l]})" for l in k["levels"]))
                vc = VERD[f"{f}|{samp}|{bl}"]
                P(f"   => {vc['cls']}{': ' + SHORT[vc['V']] if vc['V'] else ''}   best P {SHORT.get(vc['zP'][1], '-')} z {vc['zP'][0]:.2f}; best M {SHORT.get(vc['zM'][1], '-')} z {vc['zM'][0]:.2f}; "
                  f"separating P {[SHORT[v] for v in vc['sepP']]}, M {[SHORT[v] for v in vc['sepM']]}")
    P("\n--- collinearity on the verdict cell (HOSTED x B_iso) ---")
    for f in FOOTS:
        q = COLL_Q[f]
        if "mutual_rho" in q:
            P(f"   [{f}] best P {SHORT[q['best_P']]} vs best M {SHORT[q['best_M']]} (N {q['N']}): mutual rho {q['mutual_rho']:+.3f}; partial P|M {q['partial_P_given_M']['partial']:+.3f} +- {q['partial_P_given_M']['sd']:.3f} (z {q['partial_P_given_M']['z']:.1f}); "
              f"partial M|P {q['partial_M_given_P']['partial']:+.3f} +- {q['partial_M_given_P']['sd']:.3f} (z {q['partial_M_given_P']['z']:.1f}); CONFOUNDED {q['confounded']}")
        else:
            P(f"   [{f}] {q}")
    P("   reported: every P against M1 (log dsig/sig), HOSTED x B_iso:")
    for f in FOOTS:
        for v in PVARS:
            k = f"{f}|{v}"
            if k not in PART_M1: continue
            q = PART_M1[k]
            P(f"   [{f}] {SHORT[v]:14s} N {q['N']:2d} mutual {q['mutual_rho']:+.2f}  P|M1 {q['P_given_M1']['partial']:+.3f}+-{q['P_given_M1']['sd']:.3f} (z {q['P_given_M1']['z']:.1f})  "
              f"M1|P {q['M1_given_P']['partial']:+.3f}+-{q['M1_given_P']['sd']:.3f} (z {q['M1_given_P']['z']:.1f})")
    P("\n--- baseline dependence (HOSTED) ---")
    BD = {}
    for f in FOOTS:
        rows = [r for r in PER[f] if r["hosted"]]
        flips = [(r["name"], r["lab_B_iso"], r["lab_B_EFE"], r["E_B_iso"], r["E_B_EFE"]) for r in rows if r["lab_B_iso"] != r["lab_B_EFE"]]
        dE = [r["E_B_EFE"] - r["E_B_iso"] for r in rows]
        rr = float(SS.spearmanr([r["P4_loge"] for r in rows], dE)[0])
        med_iso = float(np.median([r["E_B_iso"] for r in rows])); med_efe = float(np.median([r["E_B_EFE"] for r in rows]))
        BD[f] = dict(flips=flips, rho_dE_loge=rr, median_E_iso=med_iso, median_E_efe=med_efe, n_flips=len(flips))
        P(f"   [{f}] median E: B_iso {med_iso:+.3f}, B_EFE {med_efe:+.3f}; rho(E_EFE - E_iso, log e) {rr:+.3f}; {len(flips)} label changes:")
        for n, a, b, e1, e2 in flips:
            P(f"      {n:24s} {a:6s} -> {b:6s}  (E_iso {e1:+.2f}, E_EFE {e2:+.2f})")
    P("\n--- named systems (canonical / alt; E dex, Z) ---")
    for n in ["Crater II", "Antlia II", "Canes Venatici I", "Sagittarius", "Fornax", "Leo I", "Draco", "Ursa Minor", "Sextans", "Segue 1", "Willman 1", "Bootes I"]:
        if n not in BYN: continue
        s_ = []
        for f in FOOTS:
            r = next(x for x in PER[f] if x["name"] == n)
            s_.append(f"iso {r['E_B_iso']:+.2f} (Z {r['Z_B_iso']:+.1f}) EFE {r['E_B_EFE']:+.2f} (Z {r['Z_B_EFE']:+.1f})")
        r = next(x for x in PER["canonical"] if x["name"] == n)
        P(f"   {n:18s} {' / '.join(s_)}  | log M* {r['P0_logMstar']:.2f} log x {r['P3_logx']:+.2f} log e {r['P4_loge']:+.2f} dsig/sig {10 ** r['M1_logdsig']:.2f} N* {r['Nstar']}")

# ================================================================== verdict
P("\n" + "=" * 110)
if STOP:
    FINAL = dict(cls="UNDECIDED (stop rule)", reason="K0 or K1 failed")
else:
    vcan, valt = VERD["canonical|HOSTED|B_iso"], VERD["alt|HOSTED|B_iso"]
    if vcan["cls"] == valt["cls"] and vcan["V"] == valt["V"]:
        FINAL = dict(cls=vcan["cls"], V=vcan["V"])
    else:
        FINAL = dict(cls="UNDECIDED", reason=f"footings differ: canonical {vcan['cls']} {vcan['V']}, alt {valt['cls']} {valt['V']}")
    qual = []
    for tag, key in (("EFE-DIFFERS", "B_EFE"), ):
        for f in FOOTS:
            a, b = VERD[f"{f}|HOSTED|B_iso"], VERD[f"{f}|HOSTED|{key}"]
            if (a["cls"], a["V"]) != (b["cls"], b["V"]): qual.append(f"{tag} ({f}: B_EFE gives {b['cls']}{' ' + b['V'] if b['V'] else ''})")
    for f in FOOTS:
        if COLL_Q[f].get("confounded"): qual.append(f"CONFOUNDED ({f})")
        a, b = VERD[f"{f}|HOSTED|B_iso"], VERD[f"{f}|ALL|B_iso"]
        if (a["cls"], a["V"]) != (b["cls"], b["V"]): qual.append(f"ALL-DIFFERS ({f}: ALL gives {b['cls']}{' ' + b['V'] if b['V'] else ''})")
    FINAL["qualifiers"] = qual
    FINAL["cells"] = {k: dict(cls=v["cls"], V=v["V"], zP=v["zP"], zM=v["zM"], sepP=v["sepP"], sepM=v["sepM"]) for k, v in VERD.items()}
allok = all(v["ok"] for v in CHK.values())
P(f"VERDICT: {FINAL['cls']}" + (f": {SHORT.get(FINAL.get('V'), FINAL.get('V'))}" if FINAL.get("V") else "") + (f"  [{'; '.join(FINAL.get('qualifiers', []))}]" if FINAL.get("qualifiers") else ""))
if "reason" in FINAL: P(f"   reason: {FINAL['reason']}")
P(f"checks: {sum(v['ok'] for v in CHK.values())}/{len(CHK)} PASS" + ("" if allok else " -- FAIL: " + ", ".join(k for k, v in CHK.items() if not v["ok"])))
P(f"runtime {time.time() - T0:.0f} s; peak RSS {rss_gb():.3f} GB; one thread")
P("kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed.")

R = dict(lane="X20_hosted_dwarf_requirement", criteria="8a6247efea", x1_commit="c74c622229", mutate=MUT, checks=CHK,
         step0=K1ROWS, verdict=FINAL, cells=RES, per_system=PER)
if not STOP:
    R.update(collinearity=COLL_Q, partial_vs_M1=PART_M1, baseline_dependence=BD)
json.dump(R, open(os.path.join(HERE, f"x20_hosted_dwarf_requirement_results{SFX}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"x20_hosted_dwarf_requirement{SFX}.out"), "w").write("\n".join(OUT) + "\n")
if not MUT:
    keys = list(PER["canonical"][0].keys())
    with open(os.path.join(HERE, "x20_per_system.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys); w.writeheader()
        for f in FOOTS:
            for r in PER[f]: w.writerow(r)
sys.exit(0 if allok else 1)
