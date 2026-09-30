#!/usr/bin/env python3
"""CFG224 -- how well is the gas-mass calibration known?  Tracer-to-tracer offsets and scatter against redshift from galaxies with gas masses from two or more tracers,
against the +-0.15 dex (CFG221) and +-0.05 to 0.10 dex (CFG223) requirements.  Frozen criteria: FROZEN_CRITERIA.md here (99f62160b), committed before any tracer offset was computed.
Conversions are as each source states them; the data chat's reconstructions (NOEMA3D CO, [CI], dust) are unverified against the papers; a tracer agreement does not prove an absolute mass scale.
kappa = 1/2 FITTED.  No sentence says the data favour a law.
Run:  python3 campaign_fresh_gravity/CFG224_gas_calibration/cfg224_gas_calibration.py        (MUTATE=1: +0.30 dex injected into every CO mass of Stripe82 and NOEMA3D)"""
import os, sys, io, csv, json, math, re, tarfile, time
sys.dont_write_bytecode = True
import numpy as np

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
MG = os.path.join(REPO, "data_assembly", "multitracer_gas")
MUT = os.environ.pop("MUTATE", "").strip() == "1"
SFX = "_MUTATE" if MUT else ""
OUT, CHK = [], []
T0 = time.time()
SEED = 224
NBOOT = 10000


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


def rd(name):
    return list(csv.DictReader(open(os.path.join(MG, name), newline="")))


def f(x):
    try:
        v = float(str(x).strip())
        return v if math.isfinite(v) else float("nan")
    except (TypeError, ValueError):
        return float("nan")


P(__doc__.split("Run:")[0].strip())
ORDER = ["CO", "CI", "CII", "DUST"]
PAIRS = ["CO-CI", "CO-CII", "CO-DUST", "CI-CII", "CI-DUST", "CII-DUST"]
BINS = [("B1 z<0.6", 0.0, 0.6), ("B2 0.6<=z<1.6", 0.6, 1.6), ("B3 1.6<=z<3.0", 1.6, 3.0), ("B4 z>=3.0", 3.0, 99.0)]


def binof(z):
    for b in BINS:
        if b[1] <= z < b[2]:
            return b[0]
    return None


CO_SHIFT = 0.30 if MUT else 0.0
ROWS = []      # dict(src, id, z, pair, d, sig (dex, nan if not stated), indep)


def add(src, gid, z, tA, tB, lmA, lmB, eA=float("nan"), eB=float("nan"), indep=True):
    """d = log10(M_A/M_B) with A before B in ORDER; masses passed as log10."""
    assert ORDER.index(tA) < ORDER.index(tB)
    ROWS.append(dict(src=src, id=gid, z=z, pair=f"{tA}-{tB}", d=lmA - lmB, sig=math.sqrt(eA ** 2 + eB ** 2) if math.isfinite(eA) and math.isfinite(eB) else float("nan"), indep=indep))


# ---- Stripe82: CO-DUST
s82 = rd("stripe82_z_lt0.3_CO_dust.csv")
for r in s82:
    add("Stripe82", r["id"], f(r["z"]), "CO", "DUST", f(r["logMgas_CO"]) + CO_SHIFT, f(r["logMgas_dust"]), f(r["logMgas_CO_errlo"]), f(r["logMgas_dust_errlo"]))
# ---- Bourne+19: CI-DUST (continuum)
bo = [r for r in rd("bourne2019_z1_CI_CO_dust.csv") if math.isfinite(f(r["Mmol_CI_1e9"])) and math.isfinite(f(r["Mmol_cont_1e9"]))]
for r in bo:
    mc, mk = f(r["Mmol_CI_1e9"]), f(r["Mmol_cont_1e9"])
    ec, ek = 0.5 * (f(r["Mmol_CI_1e9_errlo"]) + f(r["Mmol_CI_1e9_errhi"])) / mc / math.log(10), 0.5 * (f(r["Mmol_cont_1e9_errlo"]) + f(r["Mmol_cont_1e9_errhi"])) / mk / math.log(10)
    add("Bourne+19", r["id"], f(r["z"]), "CI", "DUST", math.log10(mc), math.log10(mk), ec, ek)
# ---- NOEMA3D: the five validated; the five failing as a sensitivity (CO from the recipe reconstruction and from Table 1)
nr = rd("noema3d_three_tracer_reconstruction.csv")
for r in nr:
    ok = r["CO_control_pass"].strip() in ("1", "True", "PASS")
    co1, cor, ci, du, z = f(r["logMmol_CO_table1"]), f(r["logMmol_CO_reconstructed"]), f(r["logMmol_CI_reconstructed"]), f(r["logMmol_dust_reconstructed"]), f(r["z"])
    src = "NOEMA3D" if ok else "NOEMA3D-failing(Table1 CO)"
    for nm, co in ((src, co1),) + (() if ok else (("NOEMA3D-failing(recipe CO)", cor),)):
        add(nm, r["id"], z, "CO", "DUST", co + CO_SHIFT, du, indep=ok)
        if math.isfinite(ci):
            add(nm, r["id"], z, "CO", "CI", co + CO_SHIFT, ci, indep=ok)
            add(nm, r["id"], z, "CI", "DUST", ci, du, indep=ok)
VALID = sorted(r["id"] for r in nr if r["CO_control_pass"].strip() in ("1", "True", "PASS"))
# ---- singles (stated values at the stated default conversions; TRANSCRIBED from singles_multitracer_galaxies.csv, which is the authority: checked below)
SING = {"PKS 0529-549": dict(z=2.5725, CI=(3.1e11, 0.6e11), CO=(0.73e11, 0.09e11), DUST=(2.2e11, 0.2e11)),
        "Q1700-MD94": dict(z=2.333, CO=(1.7e11, float("nan")), DUST=(7e10, float("nan"))),
        "J081740": dict(z=4.2603, CO=(8.8e10, 2.6e10), DUST=(5.7e10, 0.7e10), CII=(9.8e10, 0.6e10))}
sg = {r["galaxy"].split(" (")[0]: r["stated_gas_masses_and_conversions"] for r in rd("singles_multitracer_galaxies.csv")}
txt_ok = ("3.1+-0.6e11" in sg["PKS 0529-549"] and "0.73+-0.09e11" in sg["PKS 0529-549"] and "2.2+-0.2e11" in sg["PKS 0529-549"] and "1.7e11" in sg["Q1700-MD94"] and "7e10" in sg["Q1700-MD94"]
          and "8.8+-2.6e10" in sg["J081740"] and "5.7+-0.7e10" in sg["J081740"] and "9.8+-0.6e10" in sg["J081740"])
for name, g in SING.items():
    tr = [t for t in ORDER if t in g]
    for i in range(len(tr)):
        for j in range(i + 1, len(tr)):
            (mA, eA), (mB, eB) = g[tr[i]], g[tr[j]]
            lA, lB = math.log10(mA) + (CO_SHIFT * 0.0), math.log10(mB)
            add("singles", name, g["z"], tr[i], tr[j], lA, lB, eA / mA / math.log(10) if math.isfinite(eA) else float("nan"), eB / mB / math.log(10) if math.isfinite(eB) else float("nan"))
D49_BOUND = 11.22 - 11.19          # CI-DUST < +0.03 (upper limit; never in a mean)


# ---- statistics
def stats(d, sig=None, seed=SEED):
    d = np.asarray(d, float); n = len(d)
    o = dict(N=n)
    if n < 3:
        return o
    mu, s = float(d.mean()), float(d.std(ddof=1)); se = s / math.sqrt(n)
    o.update(mean=mu, sd=s, se=se, median=float(np.median(d)), mad=float(1.4826 * np.median(np.abs(d - np.median(d)))))
    if n >= 6:
        I = np.random.default_rng(seed).integers(0, n, size=(NBOOT, n)); bm = d[I].mean(axis=1)
        o["boot68"] = [float(np.percentile(bm, 16)), float(np.percentile(bm, 84))]
    if sig is not None and np.all(np.isfinite(sig)):
        o["sd_int"] = float(math.sqrt(max(0.0, s ** 2 - float(np.mean(np.asarray(sig) ** 2)))))
    o["K"] = float(math.sqrt(se ** 2 + (abs(mu) / 2) ** 2))
    K = o["K"]
    o["class"] = "below the CFG223 range (K < 0.05)" if K < 0.05 else ("inside the CFG223 range (0.05 <= K < 0.10)" if K < 0.10 else ("between the CFG223 and CFG221 requirements (0.10 <= K < 0.15)" if K < 0.15 else "at or above the CFG221 requirement (K >= 0.15)"))
    return o


P("\nPRIMARY: independent pairs, pooled per (pair type, bin) as frozen (Kirkpatrick+19 and H-ATLAS are not in ROWS); source rows are supplementary")
P(f"  independent rows: {sum(1 for r in ROWS if r['indep'])}; transcription of the singles matches the data chat's CSV text: {txt_ok}")
RES = {}
HEAD = {}
for b in BINS:
    P(f"\n  {b[0]}")
    cand = []
    for pr in PAIRS:
        sel = [r for r in ROWS if r["indep"] and r["pair"] == pr and binof(r["z"]) == b[0] and not r["src"].startswith("NOEMA3D-failing")]
        if not sel:
            continue
        st = stats([r["d"] for r in sel], [r["sig"] for r in sel])
        RES[(b[0], pr)] = st
        srcs = sorted({r["src"] for r in sel})
        if st["N"] < 3:
            P(f"    {pr:8s} N = {st['N']} (no statistics): " + "; ".join(f"{r['src']} {r['id']} z {r['z']:.3f} d {r['d']:+.3f}" for r in sel))
        else:
            ex = (f", 68% boot [{st['boot68'][0]:+.3f}, {st['boot68'][1]:+.3f}]" if "boot68" in st else "") + (f", intrinsic SD {st['sd_int']:.3f}" if "sd_int" in st else "")
            P(f"    {pr:8s} N = {st['N']:3d} ({', '.join(srcs)}): mean {st['mean']:+.3f}, SD {st['sd']:.3f}, SE {st['se']:.3f}, median {st['median']:+.3f}, 1.4826 MAD {st['mad']:.3f}{ex};  K = {st['K']:.3f}: {st['class']}")
            cand.append((st["N"], -PAIRS.index(pr), pr))
    if cand:
        HEAD[b[0]] = sorted(cand, reverse=True)[0][2]
        P(f"    headline pair type: {HEAD[b[0]]} (N = {RES[(b[0], HEAD[b[0]])]['N']}); K = {RES[(b[0], HEAD[b[0]])]['K']:.3f}")
    else:
        P("    no pair type with N >= 3: K not estimated")

P("\nSUPPLEMENTARY per-source rows (sources are not pooled here; conversions differ between sources)")
SRCROWS = {}
for src in ("Stripe82", "Bourne+19", "NOEMA3D", "NOEMA3D-failing(Table1 CO)", "NOEMA3D-failing(recipe CO)"):
    for pr in PAIRS:
        sel = [r for r in ROWS if r["src"] == src and r["pair"] == pr]
        if len(sel) >= 3:
            st = stats([r["d"] for r in sel], [r["sig"] for r in sel])
            SRCROWS[(src, pr)] = st
            P(f"    {src:28s} {pr:8s} N = {st['N']:3d} z {min(r['z'] for r in sel):.2f}-{max(r['z'] for r in sel):.2f}: mean {st['mean']:+.3f}, SD {st['sd']:.3f}, SE {st['se']:.3f}; K = {st['K']:.3f}")
P(f"    D49 (z ~ 3): CI-DUST < {D49_BOUND:+.2f} dex (upper limit on the [CI] mass; not in any mean)")
P("    Kirkpatrick+19 (not independent: RJ dust is calibrated to CO with alpha_CO = 6.5): paper's own CO-RJ ratio check")
kp = rd("kirkpatrick2019_z2_CO_dust.csv")
kd = [math.log10(f(r["Mmol_CO_1e11"]) / f(r["Mmol_RJ_1e11"])) for r in kp if math.isfinite(f(r["Mmol_CO_1e11"])) and math.isfinite(f(r["Mmol_RJ_1e11"]))]
P(f"      N = {len(kd)}, log10(M_CO / M_RJ): mean {np.mean(kd):+.3f}, SD {np.std(kd, ddof=1):.3f} (beside the primary, never in it)")

# ---- three-cornered hat
P("\nTHREE-CORNERED HAT (the five validated NOEMA3D galaxies: CO, CI, DUST)")
nv = [r for r in nr if r["CO_control_pass"].strip() in ("1", "True", "PASS")]
co = np.array([f(r["logMmol_CO_table1"]) + CO_SHIFT for r in nv]); ci = np.array([f(r["logMmol_CI_reconstructed"]) for r in nv]); du = np.array([f(r["logMmol_dust_reconstructed"]) for r in nv])


def hat(co, ci, du):
    v_ci_co, v_co_du, v_ci_du = np.var(co - ci, ddof=1), np.var(co - du, ddof=1), np.var(ci - du, ddof=1)
    return np.array([(v_ci_co + v_co_du - v_ci_du) / 2, (v_ci_co + v_ci_du - v_co_du) / 2, (v_co_du + v_ci_du - v_ci_co) / 2])     # CO, CI, DUST variances


h = hat(co, ci, du)
jk = np.array([hat(np.delete(co, i), np.delete(ci, i), np.delete(du, i)) for i in range(len(co))])
n = len(co); se = np.sqrt((n - 1) / n * ((jk - jk.mean(axis=0)) ** 2).sum(axis=0))
HATRES = {}
for k, nm in enumerate(("CO", "CI", "DUST")):
    flag = "NOT CONSTRAINED (negative variance)" if h[k] < 0 else f"sigma = {math.sqrt(h[k]):.3f} dex"
    P(f"    {nm:5s} variance {h[k]:+.4f} (jackknife SE {se[k]:.4f}): {flag}")
    HATRES[nm] = dict(var=float(h[k]), se=float(se[k]))
P("    PKS 0529-549 and J081740 have three tracers each but N = 1: no statistics.")

# ---- secondary: luminosity ratios at z > 2
P("\nSECONDARY (z > 2, conversion-free luminosity ratios; luminosity-level, NOT a mass test)")
smg = rd("smg_CI_CO_3mm_arxiv2404.05596.csv")
SEC = {}
rr, za, jup, aimp = [], [], [], []
for r in smg:
    lci, lco, mci = f(r["LpCI_1e10"]), f(r["LpCO10_1e10"]), f(r["Mgas_CI_1e10"])
    if math.isfinite(lci) and math.isfinite(lco) and lci > 0 and lco > 0:
        rr.append(math.log10(lci / lco)); za.append(f(r["z"])); jup.append(f(r["Jup"]))
        aimp.append(math.log10(mci / lco) if math.isfinite(mci) and mci > 0 else float("nan"))
rr, za, jup, aimp = map(np.array, (rr, za, jup, aimp))
P(f"    SMGs: N = {len(rr)}, z {za.min():.2f}-{za.max():.2f}: log10(L'_CI / L'_CO(1-0)) mean {rr.mean():+.3f}, SD {rr.std(ddof=1):.3f}, SE {rr.std(ddof=1) / math.sqrt(len(rr)):.3f}")
SEC["smg_ratio"] = dict(N=len(rr), mean=float(rr.mean()), sd=float(rr.std(ddof=1)))
for jv in sorted(set(jup[np.isfinite(jup)])):
    m = jup == jv
    if m.sum() >= 3:
        P(f"      observed CO J_up = {jv:.0f}: N = {int(m.sum())}: mean {rr[m].mean():+.3f}, SD {rr[m].std(ddof=1):.3f}")
ok_a = np.isfinite(aimp)
P(f"    implied alpha_CO = M_gas,[CI] / L'_CO(1-0) (X_[CI] = 5.1e-5): N = {int(ok_a.sum())}, median {10 ** np.median(aimp[ok_a]):.2f}, SD of log {aimp[ok_a].std(ddof=1):.3f} dex")
SEC["alpha_implied"] = dict(N=int(ok_a.sum()), median=float(10 ** np.median(aimp[ok_a])), sd=float(aimp[ok_a].std(ddof=1)))
for aa in (0.8, 3.6, 4.36):
    off = np.log10(aa) - aimp[ok_a]
    P(f"      alpha_assumed {aa}: offset log10(alpha_assumed L'_CO / M_gas,[CI]) mean {off.mean():+.3f}, SD {off.std(ddof=1):.3f}")
    SEC[f"offset_{aa}"] = dict(mean=float(off.mean()), sd=float(off.std(ddof=1)))
spt = rd("spt_dsfg_CI_CO_CII_fluxes_arxiv2306.03153.csv")
NU = dict(CI10=492.1607, CI21=809.3446, CO76=806.6518, CII=1900.5369)


def lratio(A, B):
    v = []
    for r in spt:
        a, b = f(r[A + "_Jykms"]), f(r[B + "_Jykms"])
        if math.isfinite(a) and math.isfinite(b) and a > 0 and b > 0:
            v.append(math.log10((a / b) * (NU[B] / NU[A]) ** 2))
    return np.array(v)


for A, B in (("CI21", "CI10"), ("CII", "CI10")):
    v = lratio(A, B)
    if len(v) >= 3:
        P(f"    SPT: log10(L'_{A} / L'_{B}): N = {len(v)}, mean {v.mean():+.3f}, SD {v.std(ddof=1):.3f}")
        SEC[f"spt_{A}_{B}"] = dict(N=len(v), mean=float(v.mean()), sd=float(v.std(ddof=1)))
    else:
        P(f"    SPT: log10(L'_{A} / L'_{B}): N = {len(v)} (< 3): not summarised")

# ---- Dunne+22 literature calibrations parsed from the TeX tables
P("\nLITERATURE (Dunne+22, parsed from the TeX tables on disk; no download)")
tex = None
with tarfile.open(os.path.join(os.path.dirname(REPO), "_external_data", "arxiv_src", "2208.01622.tar.gz")) as tf:
    for m in tf.getmembers():
        if m.name.endswith("MonsterCalibration.tex"):
            tex = tf.extractfile(m).read().decode("utf-8", "replace")
assert tex is not None
t1 = tex[tex.index("\\caption{Mean optimised conversion factors"):tex.index("\\label{caloptT}")]
TRI = re.compile(r"\$([\d.]+)\^\{\+([\d.]+)\}_\{-([\d.]+)\}\$")
DUN = []
for ln in t1.split("\\\\"):
    cells = [c.strip() for c in ln.split("&")]
    tok = re.search(r"\b(daX|Xd|ad|Xa)\b", cells[0]) if cells else None
    if len(cells) >= 9 and re.search(r"\d", cells[2]) and tok:
        nm = tok.group(1)
        sel = cells[1].replace("$", "").replace("\\", "").strip()
        rec = dict(sample=nm, sel=sel, N=int(re.sub(r"\D", "", cells[2])))
        for key, ci_, si_ in (("X_CI", 3, 4), ("alpha_CO", 5, 6), ("kappa_H", 7, 8)):
            m = TRI.search(cells[ci_])
            if m:
                mean, up, dn = map(float, m.groups())
                rec[key] = dict(mean=mean, scatter_dex=(math.log10(mean + up) - math.log10(mean - dn)) / 2, err_mean=f(cells[si_]), err_mean_dex=f(cells[si_]) / mean / math.log(10))
        DUN.append(rec)
P(f"    parsed {len(DUN)} sample rows of the mean-optimised table")
for r in DUN:
    bits = []
    for key in ("X_CI", "alpha_CO", "kappa_H"):
        if key in r:
            bits.append(f"{key} {r[key]['mean']:g}: per-galaxy scatter {r[key]['scatter_dex']:.3f} dex, error on the mean {r[key]['err_mean_dex']:.3f} dex")
    P(f"    {r['sample']:4s} {r['sel']:14s} N = {r['N']:3d}: " + "; ".join(bits))
c6 = {(r["sample"], r["sel"][:3], r["N"]): r for r in DUN}
a_daX = next((r for r in DUN if r["sample"] == "daX" and r["N"] == 90), None)
a_adh = next((r for r in DUN if r["sample"] == "ad" and r["N"] == 240), None)
a_adl = next((r for r in DUN if r["sample"] == "ad" and r["N"] == 88), None)
okc6 = bool(a_daX and a_adh and a_adl and abs(a_daX["alpha_CO"]["mean"] - 2.66) < 1e-9 and abs(a_adh["alpha_CO"]["mean"] - 3.08) < 1e-9 and abs(a_adl["alpha_CO"]["mean"] - 3.52) < 1e-9)
alpha_hi = [r["alpha_CO"]["mean"] for r in DUN if "alpha_CO" in r and r["N"] in (90, 240, 97)]
alpha_lo = [r["alpha_CO"]["mean"] for r in DUN if "alpha_CO" in r and r["N"] in (12, 88) and r["sample"] in ("daX", "ad", "Xa")]
sp_hi = math.log10(max(alpha_hi) / min(alpha_hi)); sp_lo = math.log10(max(alpha_lo) / min(alpha_lo))
P(f"    spread of the mean alpha_CO between samples: high-L class {sp_hi:.3f} dex (samples N = 90, 240, 97); low-L class {sp_lo:.3f} dex (N = 12, 88, 12; the CIcor row is not used)")
t2 = tex[tex.index("\\caption{Empirical calibration factors derived from"):tex.index("\\label{empT}")]
PM = re.compile(r"\$([\d.]+)\s*\\pm\s*([\d.]+)\s*\$")
EMP = []
for ln in t2.split("\\\\"):
    cells = [c.strip() for c in ln.split("&")]
    tk = re.search(r"\b(daX|Xd|ad|Xa)\b", cells[0]) if cells else None
    if len(cells) >= 8 and re.search(r"\d", cells[1]) and tk:
        vals = [PM.search(c) for c in cells[2:8]]
        EMP.append(dict(sample=tk.group(1) + (" (Lhi)" if "Lhi" in cells[0] else ""), N=int(re.sub(r"\D", "", cells[1])), a850_H=float(vals[0].group(1)) if vals[0] else None, aCO_H=float(vals[1].group(1)) if vals[1] else None, aCI_H=float(vals[2].group(1)) if vals[2] else None))
P(f"    empirical calibration table: {len(EMP)} rows: " + "; ".join(f"{e['sample'][:10]} N={e['N']}: a850 {e['a850_H']}, aCO {e['aCO_H']}, aCI {e['aCI_H']}" for e in EMP))
sp = {}
for key in ("a850_H", "aCO_H", "aCI_H"):
    v = [e[key] for e in EMP if e[key]]
    sp[key] = math.log10(max(v) / min(v)) if v else float("nan")
P(f"    spread between samples in the empirical table (max over min, dex): alpha_850 {sp['a850_H']:.3f}, alpha_CO {sp['aCO_H']:.3f}, alpha_CI {sp['aCI_H']:.3f}")
LIT = dict(rows=DUN, empirical=EMP, spread_alphaCO_hiL=sp_hi, spread_alphaCO_loL=sp_lo, spread_emp=sp)

# ---- implication arithmetic (section 6)
P("\nIMPLICATION (arithmetic with declared inputs, not a forecast): K_needed = (Delta/2) / (|L| f_gas)")
lev = {}
for ln in open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_lever.out")):
    m = re.match(r"\s+(RC100 corr Q\d|CR R_e fit|CR R_out fit|CR R_e ind|CR R_out ind)\s+\d+\s+[\d.]+\s+[\d.]+\s+([+-][\d.]+)\s+x", ln)
    if m:
        lev[m.group(1)] = float(m.group(2))
J23 = json.load(open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_results.json")))["points"]
IMPL = []
for p in J23[:8]:
    L = lev.get(p["short"])
    if L is None:
        continue
    z = p["z_med"]; dl = math.log10(math.sqrt(0.315 * (1 + z) ** 3 + 0.685)); b = binof(z)
    kneed = {fg: (dl / 2) / (abs(L) * fg) for fg in (0.3, 0.5, 0.7)}
    hk = RES.get((b, HEAD.get(b, "")), {}).get("K")
    IMPL.append(dict(point=p["short"], z=z, bin=b, lever=L, delta_dex=dl, K_needed=kneed, K_measured_headline=hk))
    P(f"    {p['short']:14s} z {z:.2f} ({b}): lever {L:+.2f}, separation {dl:.3f} dex; K_needed at f_gas 0.3 / 0.5 / 0.7: {kneed[0.3]:.3f} / {kneed[0.5]:.3f} / {kneed[0.7]:.3f}; measured headline K in the bin: " + (f"{hk:.3f}" if hk is not None else "not estimated"))

# ---- controls
P("\nCONTROLS")
chk = open(os.path.join(MG, "checks_multitracer.txt")).read()
cnt = dict(kp=len(kp), bo=len(bo), smg=len(smg), spt=len(spt), s82=len(s82))
okc1 = (cnt["kp"] == 12 and cnt["bo"] == 9 and cnt["smg"] == 20 and cnt["spt"] == 29 and cnt["s82"] == 78 and len(VALID) == 5 and VALID == sorted(["G4_38065", "G4_38232", "G4_20371", "GN4_24517", "GN4_18574"])
        and all(math.isfinite(r["d"]) for r in ROWS) and "12 galaxies" in chk and "78 galaxies" in chk and "20 sources" in chk and "29 lensed" in chk and "9 in Table 4" in chk)
check("C1 data counts equal the data chat's checks file (Stripe82 78, Bourne 9 with both masses, Kirkpatrick 12, SMG 20, SPT 29), the NOEMA3D validated set is exactly the five with CO control pass, no non-finite offset", f"{cnt}; validated {VALID}", okc1 or MUT)
rng = np.random.default_rng(SEED)
x = rng.normal(0.10, 0.15, 500); stx = stats(x)
Ib = np.random.default_rng(1).integers(0, 500, size=(4000, 500)); bm = x[Ib].mean(axis=1)
okc2 = abs(stx["mean"] - 0.10) < 3 * stx["se"] and abs(stx["sd"] - 0.15) < 3 * stx["sd"] / math.sqrt(2 * 499) and abs((np.percentile(bm, 84) - np.percentile(bm, 16)) / 2 / stx["se"] - 1) < 0.10
check("C2 estimator identity on synthetic pairs (N = 500, mu = 0.10, s = 0.15): mean, SD and SE recovered to 3 SE and the bootstrap half-interval within 10% of SE", f"mean {stx['mean']:.3f}, SD {stx['sd']:.3f}, SE {stx['se']:.4f}, boot/SE {(np.percentile(bm, 84) - np.percentile(bm, 16)) / 2 / stx['se']:.3f}", okc2)
cov = {}
for n_ in (9, 78):
    hit = 0
    for k in range(2000):
        xx = rng.normal(0.0, 0.17, n_)
        I = rng.integers(0, n_, size=(1000, n_)); b_ = xx[I].mean(axis=1)
        hit += int(np.percentile(b_, 16) <= 0 <= np.percentile(b_, 84))
    cov[n_] = hit / 2000
check("C3 bootstrap coverage of the 68% interval of the mean on Gaussian mocks (K = 2,000): in [0.60, 0.76] at N = 9 and 78", f"{cov}", all(0.60 <= v <= 0.76 for v in cov.values()))
sA, sB, sC = 0.10, 0.15, 0.20
ok4 = []
for n_ in (300,):
    t = rng.normal(0, 0.3, n_); a = t + rng.normal(0, sA, n_); b_ = t + rng.normal(0, sB, n_); c = t + rng.normal(0, sC, n_)
    hv = hat(a, b_, c); ok4 += [abs(math.sqrt(max(hv[0], 0)) - sA) / sA < 0.15, abs(math.sqrt(max(hv[1], 0)) - sB) / sB < 0.15, abs(math.sqrt(max(hv[2], 0)) - sC) / sC < 0.15]
neg = 0
for k in range(2000):
    t = rng.normal(0, 0.3, 5); a = t + rng.normal(0, sA, 5); b_ = t + rng.normal(0, sB, 5); c = t + rng.normal(0, sC, 5)
    neg += int(np.any(hat(a, b_, c) < 0))
check("C4 three-cornered hat: synthetic (0.10, 0.15, 0.20) dex recovered to 15% at N = 300; at N = 5 the fraction of draws with at least one negative variance is REPORTED", f"N = 300 {ok4}; N = 5 fraction with a negative variance {neg / 2000:.3f}", all(ok4))
check("C5 independence guard: no Kirkpatrick or H-ATLAS row in any primary statistic (ROWS holds only Stripe82, Bourne, NOEMA3D and the singles)", f"sources in ROWS: {sorted({r['src'] for r in ROWS})}", not any(r["src"].startswith(("Kirkpatrick", "H-ATLAS")) for r in ROWS))
check("C6 the TeX parse reproduces the quoted Dunne+22 values (alpha_CO 2.66 +0.96/-0.70 N = 90; 3.08 +1.32/-0.81 N = 240; 3.52 +0.95/-0.84 N = 88) and the transcribed singles match the data chat's CSV text", f"{okc6}; singles text {txt_ok}", okc6 and txt_ok)

if MUT:
    base = {}
    SFX0 = None
    ok = True
    P("\nMUTATE: +0.30 dex injected into every CO mass of Stripe82 and the validated NOEMA3D galaxies")
    # compare with the unmutated offsets recomputed here
    for r in s82:
        pass
    d_m = np.array([r["d"] for r in ROWS if r["src"] == "Stripe82"])
    d_0 = np.array([f(r["logMgas_CO"]) - f(r["logMgas_dust"]) for r in s82])
    ok &= np.max(np.abs((d_m - d_0) - 0.30)) < 1e-9
    nm = [r for r in ROWS if r["src"] == "NOEMA3D"]
    base_n = {(r["id"], r["pair"]): (f(next(q for q in nr if q["id"] == r["id"])["logMmol_CO_table1"]) if r["pair"].startswith("CO") else 0) for r in nm}
    for r in nm:
        q = next(q for q in nr if q["id"] == r["id"])
        co1, ci_, du_ = f(q["logMmol_CO_table1"]), f(q["logMmol_CI_reconstructed"]), f(q["logMmol_dust_reconstructed"])
        d0 = {"CO-DUST": co1 - du_, "CO-CI": co1 - ci_, "CI-DUST": ci_ - du_}[r["pair"]]
        shift = r["d"] - d0
        ok &= abs(shift - (0.30 if r["pair"].startswith("CO") else 0.0)) < 1e-9
    kk = RES.get(("B1 z<0.6", "CO-DUST"), {}).get("K")
    k0 = math.sqrt((d_0.std(ddof=1) / math.sqrt(len(d_0))) ** 2 + (abs(d_0.mean()) / 2) ** 2)
    P(f"    Stripe82 CO-DUST: mean offset {d_0.mean():+.3f} -> {d_m.mean():+.3f}; K {k0:.3f} -> {kk:.3f}")
    ok &= kk > k0
    check("MUTATE every CO-containing pair offset shifts by +0.300 to 1e-9, every other pair by 0, and the B1 CO-DUST K rises", f"{ok}", ok)
    open(os.path.join(LANE, "cfg224_gas_calibration_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if all(CHK) else 1)

P(f"\n{sum(CHK)}/{len(CHK)} controls pass; {time.time() - T0:.0f} s")
P("Reading rule: these are tracer-to-tracer offsets at the conversions each source states; they measure how well the tracers agree, not an absolute mass scale; no sentence says the data favour a law.")
ser = lambda d: {f"{k[0]}|{k[1]}": v for k, v in d.items()}
J = dict(primary=ser(RES), headline=HEAD, sources=ser(SRCROWS), hat=HATRES, secondary=SEC, literature=LIT, implication=IMPL, controls=dict(passed=sum(CHK), n=len(CHK)),
         rows=[dict(src=r["src"], id=r["id"], z=r["z"], pair=r["pair"], d=r["d"], indep=r["indep"]) for r in ROWS], d49_bound=D49_BOUND)
json.dump(J, open(os.path.join(LANE, "cfg224_gas_calibration_results.json"), "w"), indent=1, default=float)
open(os.path.join(LANE, "cfg224_gas_calibration.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(CHK) else 1)
