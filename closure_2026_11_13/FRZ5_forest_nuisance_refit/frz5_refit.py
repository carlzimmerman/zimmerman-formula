#!/usr/bin/env python3
"""FRZ5 (FROZEN_CRITERIA.md 84ab155bc1): the forest row with the forest nuisance parameters refit.
Executes FRZ4's frz4_grade.py read-only up to its "halo model per case" marker (which executes FRZ3R's grading set-up:
the record's ss1_cosmo.forest_setup / forest_eval, F1A B2 cold reference, DESI DR1 P1D, full covariance), with FRZ4's
import of frz4_tables replaced by its two constants (that import creates a folder; nothing is written outside this folder).
Primary refit: P1D3's nuisance set per DESI bin (amplitude A_j > 0, tilt alpha_j in [-1, 1], R_J,j in [0.02, 0.30] Mpc/h),
profiled Asimov Delta chi^2 on the full covariance. Twins go to frz5_<footing>_MUTATE.json/.out from the same run.
Usage: nice -n 19 python3 frz5_refit.py <canonical|alt>
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, io, json, math, contextlib, warnings, time, resource
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import least_squares
from scipy.linalg import solve_triangular, cho_solve
from scipy.interpolate import CubicSpline
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FRZ4 = os.path.join(REPO, "closure_2026_11_13", "FRZ4_forest_flux_graded")
FRZ1 = os.path.join(REPO, "closure_2026_11_10", "FRZ1_forest_redistribution_at_z")
CO1 = os.path.join(REPO, "closure_2026_11_09", "CO1_form_b_cosmology_computed")
FOOT = sys.argv[1]; assert FOOT in ("canonical", "alt")
OUT, OUTM = [], []
def P(*a, m=False):
    s = " ".join(str(x) for x in a); print(s, flush=True); (OUTM if m else OUT).append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9   # macOS: bytes

# ------------------------------------------------------------------ FRZ4's grading prefix, read-only
src = open(os.path.join(FRZ4, "frz4_grade.py")).read()
cut = src.index("# ------------------------------------------------------------------ halo model per case")
old = "sys.path.insert(0, HERE); import frz4_tables as TB\nKT = TB.KT; fk_ = TB.fkey\nCASES = [fk_(f) for f in TB.CASES]"
assert old in src[:cut]
new = "KT = None\nCASES = ['f1.00', 'f2.00', 'f3.00', 'finf']"
g4 = {"__file__": os.path.join(FRZ4, "frz4_grade.py"), "__name__": "frz4_grade_prefix_frz5"}; _a = sys.argv; sys.argv = ["frz4_grade.py", FOOT]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:cut].replace(old, new), "frz4_grade_prefix", "exec"), g4)
sys.argv = _a
FD, r_points, flux_set, dchi2_sel, ALL, PR, BR, BGB, forest_eval = (g4[k] for k in ("FD", "r_points", "flux_set", "dchi2_sel", "ALL", "PR", "BR", "BGB", "forest_eval"))
G3 = g4["g"]; NS = G3["ns"]; COV = G3["COV"]; HB = G3["HB"]
KG, ZG, KF, p1d_at, M, REFBG = (NS[k] for k in ("KG", "ZG", "KF", "p1d_at", "M", "REFBG"))
assert M is G3["MB"] and REFBG is BGB
NB = FD["NB"]; ZS = FD["zs"]; KS = FD["ks"]; PD = FD["Pd"]
BINS = [float(z) for z in FD["ZB"]]; BID = np.array([BINS.index(float(z)) for z in ZS]); NZ = len(BINS)
KP = 0.01                                                            # s/km, P1D3's pivot
R0_BASE = 0.079 * HB                                                 # lambda_P = 79 comoving kpc -> Mpc/h
RES = dict(lane="FRZ5", footing=FOOT, criteria="84ab155bc1", note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
P(f"[{FOOT}] FRZ5: {NB} points, {NZ} bins; F1A h {HB:.5f}; R0 = lambda_P = 79 ckpc = {R0_BASE:.5f} Mpc/h; computed flux bins {g4['ZCOMP']}")

# ------------------------------------------------------------------ chi^2 machinery
LC = np.linalg.cholesky(COV)
def white(e): return solve_triangular(LC, e, lower=True)
def chi2_w(r): w = white((r - 1.0) * PD); return float(w @ w)
def chi2_rec(r): d = (r - 1.0) * PD; return float(d @ cho_solve(FD["CF"], d))     # ss1_cosmo line 237

# ------------------------------------------------------------------ smoothing response S_j(k; R) with the gate's own P1D
RG = np.linspace(0.0, 0.46, 231)                                     # Mpc/h
ksamp = np.exp(np.linspace(math.log(1e-4), math.log(0.999 * 200.0), 700))
LNS = []
for j, z in enumerate(BINS):
    s_ = BID == j
    lp = np.log([M.pk_lin(float(k_), float(z)) for k_ in ksamp]); PL = np.exp(CubicSpline(np.log(ksamp), lp, extrapolate=True)(np.log(KF)))
    Href = float(np.interp(z, REFBG["z"], REFBG["H"])); kp = KS[s_] * Href / (1 + z)
    tab = np.array([np.log(p1d_at(kp, PL * np.exp(-(KF * (R / HB)) ** 2))) for R in RG])
    LNS.append(CubicSpline(RG, tab, axis=0))
def lnS(j, R): return LNS[j](R)
LK = np.log(KS / KP)

def r_case_C():
    """FRZ1's primary through FRZ1's Rkz_z (frz1_forest.py line 72) and forest_eval's r (ss1_cosmo lines 230 to 236)."""
    HM = json.load(open(os.path.join(CO1, "co1_hm.json"))); KH = np.array(HM["k"])
    rows = {z: v["R_cold"] for z, v in json.load(open(os.path.join(FRZ1, "frz1_hm.json")))["cases"][f"primary|{FOOT}"].items()}
    zb = np.array(sorted(float(z) for z in rows)); RZ = np.empty((len(KG), len(ZG))); kh = KG / HB
    for jj, zz in enumerate(ZG):
        zn = zb[int(np.argmin(abs(zb - zz)))]; R = np.interp(np.log(kh), np.log(KH), np.asarray(rows[f"{zn:.1f}" if f"{zn:.1f}" in rows else str(zn)], float))
        RZ[:, jj] = np.sqrt(np.maximum(R, 0.0))
    r = np.empty(NB); lk = np.log(KG)
    for z in FD["ZB"]:
        s_ = ZS == z; lp = np.log([M.pk_lin(float(k_), float(z)) for k_ in ksamp]); PL = np.exp(CubicSpline(np.log(ksamp), lp, extrapolate=True)(np.log(KF)))
        Href = float(np.interp(z, REFBG["z"], REFBG["H"])); jz = int(np.argmin(abs(ZG - z))); Rk = np.interp(np.log(KF), lk, RZ[:, jz])
        kp = KS[s_] * Href / (1 + z); r[s_] = (p1d_at(kp, PL * Rk ** 2) * Href) / (p1d_at(kp, PL) * Href)
    return r, float(forest_eval(FD, BGB, RZ)["dchi2"])

# ------------------------------------------------------------------ nuisance model (P1D3 per bin) and refit
PRI = dict(a=(-1.0, 1.0), R=(0.02, 0.30), Amax=0.15, sha=1.0, shR=0.14)
DBL = dict(a=(-2.0, 2.0), R=(0.001, 0.44), Amax=0.30, sha=2.0, shR=0.28)
def N_of(lnA, al, R, R0):
    """per-point nuisance factor from per-bin arrays."""
    out = np.empty(NB)
    for j in range(NZ):
        s_ = BID == j; out[s_] = math.exp(lnA[j]) * np.exp(al[j] * LK[s_]) * np.exp(lnS(j, R[j]) - lnS(j, R0))
    return out

def refit(r, free=("A", "a", "R"), pri=PRI, R0=R0_BASE, smoothz=False):
    """profiled Asimov Delta chi^2. Returns dict with chi2, per-bin parameters, shifts, honesty."""
    names, lo, hi, x0s = [], [], [], []
    if smoothz:
        lay = [("lnA", j) for j in range(NZ)] + [("r0", 0), ("r1", 0), ("a0", 0), ("a1", 0)]
        bnd = {"lnA": (-3, 3), "r0": pri["R"], "r1": (-0.2, 0.2), "a0": pri["a"], "a1": (-1, 1)}
        base = {"lnA": 0.0, "r0": R0, "r1": 0.0, "a0": 0.0, "a1": 0.0}
    else:
        lay = []
        for j in range(NZ):
            if "A" in free: lay.append(("lnA", j))
            if "a" in free: lay.append(("a", j))
            if "R" in free: lay.append(("R", j))
        bnd = {"lnA": (-3, 3), "a": pri["a"], "R": pri["R"]}; base = {"lnA": 0.0, "a": 0.0, "R": R0}
    lo = np.array([bnd[n][0] for n, _ in lay]); hi = np.array([bnd[n][1] for n, _ in lay])
    def unpack(x):
        lnA = np.zeros(NZ); al = np.zeros(NZ); R = np.full(NZ, R0)
        if smoothz:
            d = {}
            for (n, j), v in zip(lay, x):
                if n == "lnA": lnA[j] = v
                else: d[n] = v
            zc = np.array(BINS) - 3.3
            R = np.clip(d["r0"] + d["r1"] * zc, pri["R"][0], pri["R"][1]); al = np.clip(d["a0"] + d["a1"] * zc, pri["a"][0], pri["a"][1])
        else:
            for (n, j), v in zip(lay, x):
                if n == "lnA": lnA[j] = v
                elif n == "a": al[j] = v
                else: R[j] = v
        return lnA, al, R
    def res(x):
        lnA, al, R = unpack(x); return white((r * N_of(lnA, al, R, R0) - 1.0) * PD)
    starts = []
    for rs in (None, 0.03, 0.20):
        x = np.array([base[n] for n, _ in lay], float)
        if rs is not None:
            for i, (n, _) in enumerate(lay):
                if n in ("R", "r0"): x[i] = rs
        starts.append(np.clip(x, lo + 1e-9, hi - 1e-9))
    best = None
    for x in starts:
        s = least_squares(res, x, bounds=(lo, hi), method="trf", xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=4000, x_scale="jac")
        c = float(s.fun @ s.fun)
        if best is None or c < best[0]: best = (c, s)
    c, s = best; lnA, al, R = unpack(s.x)
    try: err = np.sqrt(np.diag(np.linalg.pinv(s.jac.T @ s.jac)))
    except Exception: err = np.full(len(s.x), np.nan)
    sig = {f"{n}_{j}": float(abs(v - base[n]) / e) if e > 0 else None for (n, j), v, e in zip(lay, s.x, err)}
    A = np.exp(lnA)
    # honesty (section 6): bounds proximity and shifts; only parameters that were free
    viol = []
    fa = smoothz or "a" in free; fR = smoothz or "R" in free; fA = smoothz or "A" in free
    wa = pri["a"][1] - pri["a"][0]; wR = pri["R"][1] - pri["R"][0]
    for j, z in enumerate(BINS):
        if fA and abs(A[j] - 1) > pri["Amax"]: viol.append(f"A z{z:.1f} {A[j]:.4f} (|A-1| > {pri['Amax']})")
        if fa:
            if min(al[j] - pri["a"][0], pri["a"][1] - al[j]) < 0.01 * wa: viol.append(f"alpha z{z:.1f} {al[j]:+.4f} at bound")
            if abs(al[j]) > pri["sha"]: viol.append(f"alpha z{z:.1f} shift {al[j]:+.4f} > {pri['sha']}")
        if fR:
            if min(R[j] - pri["R"][0], pri["R"][1] - R[j]) < 0.01 * wR: viol.append(f"R z{z:.1f} {R[j]:.4f} at bound")
            if abs(R[j] - R0) > pri["shR"]: viol.append(f"R z{z:.1f} shift {R[j]-R0:+.4f} > {pri['shR']}")
    return dict(dchi2=c, A=A.tolist(), alpha=al.tolist(), R=R.tolist(), R0=R0, max_absA_minus1=float(np.max(np.abs(A - 1))),
                max_abs_alpha=float(np.max(np.abs(al))), max_abs_dR=float(np.max(np.abs(R - R0))),
                max_shift_alpha_prior_widths=float(np.max(np.abs(al)) / wa), max_shift_R_prior_widths=float(np.max(np.abs(R - R0)) / wR),
                max_shift_fisher_sigma=float(np.nanmax([v for v in sig.values() if v is not None])) if any(v is not None for v in sig.values()) else None,
                honesty_violations=viol, honest=not viol, nfev=int(s.nfev), status=int(s.status))

# ------------------------------------------------------------------ reading G: FRZ4's own gas-bracket response (base box, seed 0)
GZ = (2.2, 3.0)
GL = {}
for z in GZ:
    b = BR[z][0]["base"]["flux"]; p = PR[z][0]["base"]["flux"]["primary"]["R"]["p"]; kv = np.array(BR[z][0]["kv"])
    def L_(tag): return np.log(np.array(b[tag]["R"]["p"])[1:] / np.array(p)[1:])
    GL[z] = dict(kv=kv[1:], gam=(L_("gam_1.2"), L_("gam_1.6")), tau=(L_("tau_x0.9"), L_("tau_x1.1")), lam=(L_("lam_x0.5"), L_("lam_x2")))
def L_points(par, sign):
    out = np.zeros(NB); i = 0 if sign < 0 else 1
    a = {z: GL[z][par][i] for z in GZ}
    for j, z in enumerate(BINS):
        s_ = BID == j
        la = np.interp(KS[s_], GL[2.2]["kv"], a[2.2]); lb = np.interp(KS[s_], GL[3.0]["kv"], a[3.0])
        w = min(max((z - 2.2) / 0.8, 0.0), 1.0); out[s_] = la + (lb - la) * w
    return out
LG = {p: (L_points(p, -1), L_points(p, +1)) for p in ("gam", "tau", "lam")}
def refit_G(r, cmax=1.0):
    def NG(c):
        e = np.zeros(NB)
        for ci, p in zip(c, ("gam", "tau", "lam")):
            e += abs(ci) * (LG[p][1] if ci >= 0 else LG[p][0])
        return np.exp(e)
    def res(c): return white((r * NG(c) - 1.0) * PD)
    best = None
    for x0 in ([0, 0, 0], [0.5, 0.5, 0.5], [-0.5, -0.5, -0.5], [0.5, -0.5, 0.5], [-0.5, 0.5, -0.5]):
        s = least_squares(res, np.array(x0, float) + 1e-6, bounds=(-cmax, cmax), method="trf", xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=3000)
        c = float(s.fun @ s.fun)
        if best is None or c < best[0]: best = (c, s)
    c, s = best; viol = [f"c_{p} {v:+.3f} at bound" for p, v in zip(("gam", "tau", "lam"), s.x) if abs(v) > 0.99 * cmax]
    return dict(dchi2=c, c=dict(zip(("gamma", "tau_eff", "lambda_P"), s.x.tolist())), honesty_violations=viol, honest=not viol)
tau_yard = {f"{z}": float(max(abs(math.exp(np.interp(0.01, GL[z]["kv"], GL[z]["tau"][i])) - 1) for i in (0, 1))) for z in GZ}

# ------------------------------------------------------------------ cases
F4 = json.load(open(os.path.join(FRZ4, f"frz4_grade_{FOOT}.json")))["rows"]
F1 = json.load(open(os.path.join(FRZ1, f"frz1_forest_{FOOT}.json")))["cases"]["primary"]["dchi2"]
R_ = {k: r_points(flux_set(k)) for k in ("f1.00", "f2.00", "f3.00", "finf")}
rC, fC = r_case_C()
CASE = {"A_finf": R_["finf"], "B_f1.00": R_["f1.00"], "B_f2.00": R_["f2.00"], "B_f3.00": R_["f3.00"], "C_FRZ1_matter": rC}
REFN = {"A_finf": F4["finf"]["flux"], "B_f1.00": F4["f1.00"]["flux"], "B_f2.00": F4["f2.00"]["flux"], "B_f3.00": F4["f3.00"]["flux"], "C_FRZ1_matter": F1}
P(f"[{FOOT}] set-up {time.time()-T0:.0f} s, {rss():.2f} GB")

# known answers
KA = {}
KA["K1"] = {c: dict(mine=chi2_w(r), record=REFN[c], rel=abs(chi2_w(r) / REFN[c] - 1), pass_=bool(abs(chi2_w(r) / REFN[c] - 1) <= 1e-6)) for c, r in CASE.items()}
KA["K1"]["C_forest_eval_direct"] = dict(mine=fC, record=F1, pass_=bool(abs(fC / F1 - 1) <= 1e-6))
ra = CASE["A_finf"]
k2 = [chi2_rec(ra), dchi2_sel(ra, ALL), chi2_w(ra)]
KA["K2"] = dict(record_cho_solve=k2[0], frz4_dchi2_sel=k2[1], whitened=k2[2], pass_=bool(max(k2) / min(k2) - 1 <= 1e-8))
k3 = refit(np.ones(NB))
KA["K3"] = dict(dchi2=k3["dchi2"], max_absA_minus1=k3["max_absA_minus1"], max_abs_alpha=k3["max_abs_alpha"], max_abs_dR=k3["max_abs_dR"],
                pass_=bool(k3["dchi2"] <= 1e-8 and max(k3["max_absA_minus1"], k3["max_abs_alpha"], k3["max_abs_dR"]) <= 1e-4))
k4u = [float(lnS(j, R0_BASE)[0] - lnS(j, R0_BASE)[0]) for j in range(NZ)]
k4d = [bool(lnS(j, R0_BASE + 0.05)[np.argmax(KS[BID == j])] < lnS(j, R0_BASE)[np.argmax(KS[BID == j])]) for j in range(NZ)]
KA["K4"] = dict(unity_at_R0=max(abs(x) for x in k4u), lowers_at_kmax=all(k4d), pass_=bool(max(abs(x) for x in k4u) == 0 and all(k4d)))
for k, v in KA.items():
    P(f"[{FOOT}] known answer {k}: " + ("PASS" if (v["pass_"] if "pass_" in v else all(x["pass_"] for x in v.values())) else "FAIL") + " " + json.dumps(v, default=float))
KA_ok = KA["K2"]["pass_"] and KA["K3"]["pass_"] and KA["K4"]["pass_"] and all(x["pass_"] for x in KA["K1"].values())
RES["known_answers"] = KA

# primary + brackets per case
BRK_DEF = [("A_only", dict(free=("A",))), ("alpha_only", dict(free=("a",))), ("R_only", dict(free=("R",))),
           ("priors_doubled", dict(pri=DBL)), ("R0_x0.5", dict(R0=0.5 * R0_BASE)), ("R0_x2", dict(R0=2 * R0_BASE)), ("smooth_in_z", dict(smoothz=True))]
ROWS = {}
for c, r in CASE.items():
    fx = chi2_w(r); pri = refit(r)
    row = dict(fixed=fx, refit=pri, brackets={})
    for nm, kw in BRK_DEF:
        row["brackets"][nm] = refit(r, **kw)
    row["brackets"]["reading_G_gas"] = refit_G(r)
    row["reading_G_doubled_reported"] = refit_G(r, 2.0)
    ROWS[c] = row
    P(f"[{FOOT}] {c}: fixed {fx:.4f} -> refit {pri['dchi2']:.4f}; max |A-1| {pri['max_absA_minus1']:.4f}, max |alpha| {pri['max_abs_alpha']:.4f}, max |R-R0| {pri['max_abs_dR']:.4f} Mpc/h "
      f"({pri['max_shift_R_prior_widths']:.3f} prior widths), max Fisher shift {pri['max_shift_fisher_sigma']:.1f} sigma; honesty {'OK' if pri['honest'] else pri['honesty_violations']}  [{time.time()-T0:.0f}s {rss():.2f}GB]")
    P(f"[{FOOT}]   per bin A: " + " ".join(f"{z:.1f}:{a:.4f}" for z, a in zip(BINS, pri["A"])))
    P(f"[{FOOT}]   per bin alpha: " + " ".join(f"{z:.1f}:{a:+.4f}" for z, a in zip(BINS, pri["alpha"])))
    P(f"[{FOOT}]   per bin R (Mpc/h): " + " ".join(f"{z:.1f}:{a:.4f}" for z, a in zip(BINS, pri["R"])))
    for nm, b in row["brackets"].items():
        P(f"[{FOOT}]   bracket {nm}: {b['dchi2']:.4f}" + ("" if b["honest"] else f"  honesty: {b['honesty_violations'][:4]}{' ...' if len(b['honesty_violations']) > 4 else ''}")
          + (f"  c {json.dumps(b['c'])}" if "c" in b else ""))
    gd = row["reading_G_doubled_reported"]; P(f"[{FOOT}]   reading G with c in [-2, 2] (reported): {gd['dchi2']:.4f} c {json.dumps(gd['c'])}")
RES["rows"] = ROWS; RES["tau_amplitude_yardstick_kv0.01"] = tau_yard
P(f"[{FOOT}] tau_eff x0.9/x1.1 amplitude yardstick at k_v 0.01 (base box): " + json.dumps(tau_yard))

# ------------------------------------------------------------------ twins (MUTATE outputs)
TW = {}
for c in ("A_finf", "C_FRZ1_matter"):
    r = CASE[c]; d2 = refit(1.0 + 2.0 * (r - 1.0)); p = ROWS[c]["refit"]["dchi2"]
    bites = (d2["dchi2"] >= 1.25 * p) if p >= 0.1 else (d2["dchi2"] >= p)
    TW[f"T1_doubled_{c}"] = dict(primary=p, doubled=d2["dchi2"], fixed_doubled=chi2_w(1.0 + 2.0 * (r - 1.0)), bites=bool(bites))
for nm, r in (("T2_const_1.05", np.full(NB, 1.05)), ("T2_linear_z", 1.0 + 0.05 * (ZS - 3.3))):
    fx = chi2_w(r); rf = refit(r)["dchi2"]; TW[nm] = dict(fixed=fx, refit=rf, bites=bool(fx > 100 and rf <= 1e-4))
rT3 = np.exp(0.1 * LK) * N_of(np.zeros(NZ), np.zeros(NZ), np.full(NZ, R0_BASE + 0.02), R0_BASE)
fx = chi2_w(rT3); rf = refit(rT3)["dchi2"]; TW["T3_nuisance_shaped"] = dict(fixed=fx, refit=rf, bites=bool(rf <= 1e-4))
p = ROWS["A_finf"]["refit"]; t4 = refit(CASE["A_finf"], free=("a", "R"))
TW["T4_amplitude_frozen_A"] = dict(primary=p["dchi2"], amp_frozen=t4["dchi2"], primary_max_absA_minus1=p["max_absA_minus1"],
                                   bites=bool(t4["dchi2"] >= p["dchi2"] - 1e-9 and (t4["dchi2"] >= 1.25 * p["dchi2"] or p["max_absA_minus1"] < 1e-3)))
for k, v in TW.items():
    P(f"[{FOOT}] MUTATE {k}: " + json.dumps(v, default=float) + (" -> bites" if v["bites"] else " -> DOES NOT BITE"), m=True)
RES["twins"] = TW

# ------------------------------------------------------------------ labels
def word(b): return "FAILS" if (b["dchi2"] > 4 or not b["honest"]) else "HOLDS"
LAB = {}
for c in CASE:
    row = ROWS[c]; pri = row["refit"]
    if c.startswith("B_"):
        LAB[c] = f"NO VERDICT (inherited from FRZ4); ungraded refit {pri['dchi2']:.4f} (fixed {row['fixed']:.4f})"; P(f"[{FOOT}] LABEL {c}: {LAB[c]}"); continue
    tw_ok = TW["T2_const_1.05"]["bites"] and TW["T2_linear_z"]["bites"] and TW["T3_nuisance_shaped"]["bites"] and TW[f"T1_doubled_{c}"]["bites"] and (TW["T4_amplitude_frozen_A"]["bites"] if c == "A_finf" else True)
    if not KA_ok or not tw_ok:
        lab = "NO VERDICT (" + ("known answer fails" if not KA_ok else "a twin does not bite") + ")"
    else:
        if pri["dchi2"] > 4: lab = "FOREST ROW FAILS AFTER REFIT"
        elif pri["honest"]: lab = "FOREST ROW HOLDS AFTER REFIT (a hit awaiting an independent blind re-grade, not a pass of the theory)"
        else: lab = "HOLDS ONLY WITH A PARAMETER AT ITS BOUND OR BEYOND THE FROZEN SHIFT (counts as FAILS: " + "; ".join(pri["honesty_violations"][:6]) + ")"
        w0 = "FAILS" if (pri["dchi2"] > 4 or not pri["honest"]) else "HOLDS"
        flips = [nm for nm, b in row["brackets"].items() if word(b) != w0]
        if flips: lab += ", FRAGILE (" + "; ".join(flips) + ")"
    LAB[c] = lab; P(f"[{FOOT}] LABEL {c}: {lab}")
RES["labels"] = LAB; RES["reading_S"] = "the gate has no forest nuisance parameter: the strict refit set is empty and the refit equals the fixed number"
RES["seconds"] = time.time() - T0; RES["peak_rss_GB"] = rss()
P(f"[{FOOT}] done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")
json.dump(RES, open(os.path.join(HERE, f"frz5_{FOOT}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"frz5_{FOOT}.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
json.dump(dict(lane="FRZ5", footing=FOOT, twins=TW, note=RES["note"]), open(os.path.join(HERE, f"frz5_{FOOT}_MUTATE.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"frz5_{FOOT}_MUTATE.out"), "w").write("\n".join(OUTM) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
