#!/usr/bin/env python3
"""LF1_lensing_gas_fraction (FROZEN_CRITERIA.md): baryon share of the compensated cylinder from measured gas and KiDS shear, no halo-model mass.
    python3 lf1.py [--mutate-gas | --mutate-shuffle]
kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
MUTG, MUTS = "--mutate-gas" in sys.argv, "--mutate-shuffle" in sys.argv; TAG = "lf1_MUTATE_gas" if MUTG else "lf1_MUTATE_shuffle" if MUTS else "lf1"
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
TXT = open(os.path.join(REB, "F1_cluster_cores", "f1_cluster_cores.py")).read()
def cut(a, b): i = TXT.index(a); return TXT[i:TXT.index(b, i)]
NS = {"np": np, "os": os, "sys": sys, "REPO": REPO, "_trap": np.trapezoid if hasattr(np, "trapezoid") else np.trapz}
from scipy.interpolate import PchipInterpolator; NS["PchipInterpolator"] = PchipInterpolator
exec(cut("G = 6.674e-11", "# ---------------------------------------------------------------- sources"), NS); exec(cut("EDGES = np.logspace", "def gather("), NS); exec(cut("RG = np.logspace(-3", "# SIS self-test (K4)"), NS)
G, MSUN, MPC, KG = NS["G"], NS["MSUN"], NS["MPC"], NS["KG_PC2"]; RG, RF, EDGES, RC = NS["RG"], NS["RF"], NS["EDGES"], NS["RC"]; DM, DA = NS["DM"], NS["DA_lcdm"]; offset, dsig, at_bins = NS["offset"], NS["dsig_from_sig"], NS["at_bins"]
X2T = open(os.path.join(REB, "X2_cluster_outskirts", "x2_cluster_outskirts.py")).read(); _i = X2T.index("def project_floor("); NS2 = dict(NS, RG=RG); exec(X2T[_i:X2T.index("def offset_floor(")], NS2); project = NS2["project_floor"]
MY = np.load(os.path.join(REB, "X7_cluster_core_significance", "x7_measure_percluster.npz")); XR = np.load(os.path.join(REB, "X2_cluster_outskirts", "x2_replay_percluster.npz")); N = len(MY["name"]); assert [str(a) for a in XR["name"]] == [str(a) for a in MY["name"]]
Z, MG, R5, OFF = XR["z"], XR["Mgas500"], XR["R500"], XR["off_deg"]; MGL, MGH = XR["MgL"], XR["MgH"]
order = np.argsort(XR["ra"]); PATCH = np.empty(N, int); PATCH[order] = np.arange(N) * 30 // N
T3 = np.digitize(np.asarray(MY["Mgas500"], float), np.quantile(np.asarray(MY["Mgas500"], float), [1 / 3, 2 / 3])); SETS = {"M3": T3 == 2, "M2": T3 == 1, "M1": T3 == 0, "all": np.ones(N, bool)}
HH = {"h0672": (0.672, 1, 0), "h0686": (0.686, 2, 1)}; FS = (0.034, 0.0615); FAIR = 0.15945; FC = 1 - FAIR; SLOPE = 2.7774425603108597; OM = 0.2976016; LN = math.log(20) / 8
def gas3d(Mg500, R500, s, rcut):
    r = RG; rc = 0.15 * R500; sh = (1 + (r / rc) ** 2) ** -1.0; sm = (1 + (R500 / rc) ** 2) ** -1.0; sh = np.where(r > R500, sm * (r / R500) ** -s, sh); sh = np.where(r > rcut, 0.0, sh)
    dm = 4 * np.pi * (r * MPC) ** 2 * sh; M = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(r * MPC))]; nrm = Mg500 * MSUN / np.interp(R500, r, M); return M * nrm, sh * nrm
def r200_fair(M, z, h, fs):
    rc = 3 * (100 * h * 1e3 / MPC) ** 2 * (OM * (1 + z) ** 3 + 1 - OM) / (8 * math.pi * G); d = (1 + fs) * M / FAIR / (4 / 3 * math.pi * (RG * MPC) ** 3) / (200 * rc); k = np.where(d[300:] >= 1)[0]; return float(RG[300 + k[-1]]) if len(k) else float("nan")
def ds_bins(rho, d=0.0):
    S = project(rho)
    return at_bins(dsig(offset(S, d) if d > 1e-4 else S)) / KG
def zeta(S, k1, k2=8): return 2 / (1 - (EDGES[k1] / EDGES[k2]) ** 2) * (S[..., k1:k2].sum(-1)) * LN
def nfw_rho(r, R200, M200, c):
    x = r / R200; mu = math.log1p(c) - c / (1 + c); rs = R200 / c; out = M200 * MSUN / (4 * np.pi * mu * (rs * MPC) ** 3) / ((r / rs) * (1 + r / rs) ** 2); return np.where(x > 3, 0.0, out)
GB = {}; RAD = {}
def build(hk, s=SLOPE, cen=False):
    k = (hk, s, cen)
    if k in GB: return GB[k]
    h = HH[hk][0]; A = np.zeros((N, 8)); R2 = np.zeros(N)
    for i in range(N):
        q = float(DM(Z[i], h)) / (1 + Z[i]) / DA(Z[i]); M, _ = gas3d(MG[i] * q ** 2.5, R5[i] * q, s, 1e9); R2[i] = r200_fair(M, Z[i], h, 0.034); rc = 3 * R2[i] if np.isfinite(R2[i]) else 3 * R5[i] * q * 2
        _, rho = gas3d(MG[i] * q ** 2.5, R5[i] * q, s, rc); A[i] = ds_bins(rho, np.radians(OFF[i]) * float(DM(Z[i], h)) / (1 + Z[i]) if cen else 0.0)
    GB[k] = (A, R2); return GB[k]
def ref_cold(hk, c, fs, share=FAIR):
    h = HH[hk][0]; A = np.zeros((N, 8))
    for i in range(N):
        q = float(DM(Z[i], h)) / (1 + Z[i]) / DA(Z[i]); M, _ = gas3d(MG[i] * q ** 2.5, R5[i] * q, SLOPE, 1e9); R2 = r200_fair(M, Z[i], h, fs)
        if not np.isfinite(R2): continue
        Mb2 = (1 + fs) * float(np.interp(R2, RG, M)) / MSUN; Mc = Mb2 * (1 - share) / share; A[i] = ds_bins(nfw_rho(RG, R2, Mc, c))
    return A
def data(hk, key="D", shuffle=MUTS):
    _, i, hx = HH[hk]; E = MY["E"][:, i]; W = np.where(E < 1e8, 1 / E ** 2, 0); B = MY["den"][:, i].sum(0) / MY["den_r"][:, i].sum(0)
    if key == "D": D = MY["D"][:, i] - MY["leakP"][:, hx, 0]
    else: D = MY[key][:, i]
    if shuffle: D = D[np.random.default_rng(1).permutation(N)]
    return W, W * B[None, :] * D
def stack(W, v, wts=None):
    if wts is None: return v.sum(0) / W.sum(0)
    return (wts[:, None] * v).sum(0) / (wts[:, None] * W).sum(0)
def edge(x): c = [3, 4, 5, 6, 7]; return c[int(np.argmin([abs(math.log(x / EDGES[k])) for k in c]))]
RESULT = {}
# checks
ok = True
A, R2 = build("h0672"); h = .672; K1 = 0
for i in (0, 60, 120, 200, 300):
    q = float(DM(Z[i], h)) / (1 + Z[i]) / DA(Z[i]); rc = 3 * R2[i] if np.isfinite(R2[i]) else 3 * R5[i] * q * 2; _, rho = gas3d(MG[i] * q ** 2.5, R5[i] * q, SLOPE, rc); rl = np.log(RG); ls = np.log(np.maximum(rho, 1e-300)); Rg = np.geomspace(2e-3, 3.5, 400); Si = []
    for R_ in Rg:
        u = np.linspace(0, np.arccosh(30 / R_), 40000); rr = R_ * np.cosh(u); Si.append(2 * NS["_trap"](np.exp(np.interp(np.log(rr), rl, ls)) * rr * MPC, u))
    Si = np.array(Si); cum = np.r_[0.5 * Si[0] * Rg[0] ** 2, 0.5 * Si[0] * Rg[0] ** 2 + np.cumsum(0.5 * (Si[1:] * Rg[1:] + Si[:-1] * Rg[:-1]) * np.diff(Rg))]; Dd = (2 * cum / Rg ** 2 - Si) / KG; v = np.exp(np.interp(np.log(RC), np.log(Rg), np.log(np.maximum(Dd, 1e-30)))); K1 = max(K1, float(np.max(np.abs(v[2:] / A[i][2:] - 1))))
g = K1 <= 0.01; ok &= g; P(f"K1 own LOS integral against the grader's projector, 5 clusters, bins from 0.42 Mpc: {K1:.2e}: {'PASS' if g else 'FAIL'}")
sis = 1 / RC; ex = lambda k: 2 / (1 - (EDGES[k] / 3) ** 2) * (1 / EDGES[k] - 1 / 3); K2 = max(abs(zeta(sis, k) / ex(k) - 1) for k in range(3, 8)); g = K2 <= 0.02; ok &= g; P(f"K2 SIS zeta on the 8-bin grid against the closed form: max bias {K2:.2e}: {'PASS' if g else 'FAIL'}")
W, V = data("h0672", shuffle=False); se = SETS["M3"]; K3 = 0.0; OB = [6, 7]; BX = XR["den"][:, 1].sum(0) / XR["den_r"][:, 1].sum(0); nx = (np.where(XR["E"][:, 1] < 1e8, 1 / XR["E"][:, 1] ** 2, 0) * BX[None, :] * (XR["D"][:, 1] - MY["leakP"][:, 0, 0]))[se][:, OB].sum(); K3 = abs(V[se][:, OB].sum() / nx - 1); g = K3 <= 1e-9; ok &= g; P(f"K3 M3 OUTER numerator, X7 npz against X2's replay npz with the grader's formula: {K3:.1e}: {'PASS' if g else 'FAIL'} (a data replay, not a read of the grader's stored n; X30 doesn't store n)")
FS0 = 0.034; AR = ref_cold("h0672", 5.0, FS0, share=0.10); AF = ref_cold("h0672", 5.0, FS0); Ws = W[se]; Sb = ((1 + FS0) * stack(Ws, Ws * A[se])); Ss = stack(Ws, Ws * (AR[se] + (1 + FS0) * A[se])); Sr = stack(Ws, Ws * (AF[se] + (1 + FS0) * A[se])); kk = edge(float(np.nanmedian(R2[se]))); got = zeta(Sb, kk) / zeta(Ss, kk) / (zeta(Sb, kk) / zeta(Sr, kk)) * FAIR; K4 = abs(got / 0.10 - 1); g = K4 <= 0.03; ok &= g; P(f"K4 injection, share 0.10, c 5, M3 at edge {EDGES[kk]:.2f} Mpc: returns {got:.4f}: {'PASS' if g else 'FAIL'}")
if not ok: P("K FAILED: no verdict"); open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1)
REFC = {(hk, c, fs): ref_cold(hk, c, fs) for hk in HH for c in (4.43, 5.94) for fs in FS}
def stat(hk, fs, Ag, sel, k, Rmax=8, wts=None, shuffle=MUTS):
    W, V = data(hk, shuffle=shuffle); W, V = W[sel], V[sel]; Agg = Ag[sel] * (2 if MUTG else 1); Sb = (1 + fs) * stack(W, W * Agg, wts); Ss = stack(W, V, wts); return zeta(Sb, k, Rmax), zeta(Ss, k, Rmax)
def full(hk, fs, set_, k, seedk, Rmax=8, Ag=None, shuffle=MUTS):
    if Ag is None: Ag = build(hk)[0]
    sel = SETS[set_]; zb, zs = stat(hk, fs, Ag, sel, k, Rmax, shuffle=shuffle); G_ = zb / zs; ly = math.log10(G_ / FAIR)
    n = int(sel.sum()); rng = np.random.default_rng([20261031, seedk]); vals = []
    for _ in range(2000):
        w = np.bincount(rng.integers(0, n, n), minlength=n).astype(float); a, b = stat(hk, fs, Ag, sel, k, Rmax, w, shuffle); vals.append(a / b if b > 0 else np.nan)
    vals = np.array(vals); sb = float(np.nanstd(np.log10(np.maximum(vals, 1e-6)), ddof=1)) if np.all(np.nan_to_num(vals, nan=1) > 0) else float("inf")
    pp = PATCH[sel]; J = []
    for p in np.unique(pp):
        w = (pp != p).astype(float); a, b = stat(hk, fs, Ag, sel, k, Rmax, w, shuffle); J.append(a / b)
    J = np.array(J); lj = np.log10(np.where(J > 0, J, np.nan)); sj = float(np.sqrt((len(J) - 1) / len(J) * np.nansum((lj - np.nanmean(lj)) ** 2)))
    W, _ = data(hk); Wm = W[sel]; sx = []
    for key in ("Dx", "DRR"):
        _, Vx = data(hk, key); zx = zeta(stack(Wm, Vx[sel]), k, Rmax); sx.append(abs(zx) / zs / math.log(10))
    s = math.sqrt(max(sb, sj) ** 2 + sum(x ** 2 for x in sx)); return dict(G=G_, ly=ly, se=s, sb=sb, sj=sj, sx=sx, zb=zb, zs=zs, boot=vals)
def edges_for(set_, hk):
    h = HH[hk][0]; A_, R2_ = build(hk); sel = SETS[set_]; q = np.array([float(DM(Z[i], h)) / (1 + Z[i]) / DA(Z[i]) for i in range(N)]); return edge(float(np.nanmedian(R2_[sel]))), edge(float(np.median((R5 * q)[sel])))
def cls(rows):
    if any(r["se"] > 0.06 for r in rows): return "NOT POWERED"
    if all(abs(r["ly"]) <= 2 * r["se"] for r in rows): return "FAIR SHARE HOLDS"
    if all(r["ly"] < -2 * r["se"] for r in rows):
        t = all((r["ly"] - 2 * r["se"] <= -0.093 <= r["ly"] + 2 * r["se"]) or (r["ly"] + 2 * r["se"] < -0.093) for r in rows); return "DEPLETED" + (" [ENOUGH FOR ZN3]" if t else "")
    if all(r["ly"] > 2 * r["se"] for r in rows): return "EXCESS"
    return "MIXED"
P(f"LF1 {TAG}: kappa = 1/2 FITTED; not theory closed; not independent of the keys")
rows = []; seed = 0; CELLS = [(hk, fs) for hk in HH for fs in FS]; P("M3 at fair-share R200, R500 edges:")
for hk, fs in CELLS:
    k2, k5 = edges_for("M3", hk); seed += 1; r = full(hk, fs, "M3", k2, seed); seed += 1; r5 = full(hk, fs, "M3", k5, seed); nb = min(len(r["boot"]), len(r5["boot"])); rows.append(r | dict(hk=hk, fs=fs, k2=k2, k5=k5, r5=r5))
    P(f"  {hk} f* {fs}: R200 edge {EDGES[k2]:.2f} Mpc, R500 edge {EDGES[k5]:.2f}: Gamma {r['G']:.4f}, log Y {r['ly']:+.3f} +- {r['se']:.3f} (boot {r['sb']:.3f}, jack {r['sj']:.3f}, x/RR {r['sx'][0]:.3f}, {r['sx'][1]:.3f}); at R500 Gamma {r5['G']:.4f}, log Y {r5['ly']:+.3f} +- {r5['se']:.3f}")
C = cls(rows); P(f"class: {C}")
# radial: paired by construction of a shared seed
tags = []
for r in rows:
    if r["k2"] == r["k5"]: tags.append("NOT MEASURED"); continue
    hk, fs = r["hk"], r["fs"]; sel = SETS["M3"]; n = int(sel.sum()); rng = np.random.default_rng([20261031, 99]); Ag = build(hk)[0]; d = []
    for _ in range(2000):
        w = np.bincount(rng.integers(0, n, n), minlength=n).astype(float); a2, b2 = stat(hk, fs, Ag, sel, r["k2"], 8, w); a5, b5 = stat(hk, fs, Ag, sel, r["k5"], 8, w)
        if a2 / b2 > 0 and a5 / b5 > 0: d.append(math.log10((a5 / b5) / (a2 / b2)))
    dv = r["r5"]["ly"] - r["ly"]; sd = float(np.std(d, ddof=1)); r["D"] = dv; r["sD"] = sd; tags.append("FLAT" if abs(dv) <= 2 * sd else "OUTSKIRTS-LED" if dv > 0 else "CORE-LED"); P(f"  {hk} f* {fs}: Delta {dv:+.3f} +- {sd:.3f}: {tags[-1]}")
P("radial tags: " + ", ".join(tags))
# shape reference
SHP = {}
for c in (4.43, 5.94):
    r2 = []
    for r in rows:
        hk, fs = r["hk"], r["fs"]; sel = SETS["M3"]; W, _ = data(hk); Wm = W[sel]; Ag = build(hk)[0]; Sb = (1 + fs) * stack(Wm, Wm * Ag[sel]); Sr = stack(Wm, Wm * REFC[(hk, c, fs)][sel]) + Sb; Gref = zeta(Sb, r["k2"]) / zeta(Sr, r["k2"]); ly = math.log10(r["G"] / Gref); r2.append(dict(ly=ly, se=r["se"], Gref=Gref, zb=zeta(Sb, r["k2"]), zr=zeta(Sr, r["k2"])))
    SHP[c] = (cls(r2), r2); P(f"reference c {c}: Gamma_ref " + ", ".join(f"{q['Gref']:.4f}" for q in r2) + "; log Y " + ", ".join(f"{q['ly']:+.3f}" for q in r2) + f"; class {SHP[c][0]}")
sd_tag = " [SHAPE-DEPENDENT]" if any(SHP[c][0] != C for c in SHP) else ""
P(f"VERDICT: {C}{sd_tag}; radial {sorted(set(tags))}")
if MUTG or MUTS:
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n"); json.dump(dict(rows=[{k: v for k, v in r.items() if k in ("hk", "fs", "G", "ly", "se")} for r in rows], cls=C), open(os.path.join(HERE, TAG + ".json"), "w"), indent=1); sys.exit(0)
# reported
P("reported: other sets at their own edges, h 0.672, f* 0.034")
OTH = {}
for s_ in ("M2", "M1", "all"):
    k2, k5 = edges_for(s_, "h0672"); seed += 1; a = full("h0672", 0.034, s_, k2, seed); seed += 1; b = full("h0672", 0.034, s_, k5, seed); OTH[s_] = dict(k2=k2, k5=k5, ly2=a["ly"], se2=a["se"], ly5=b["ly"], se5=b["se"], G2=a["G"]); P(f"  {s_}: R200 edge {EDGES[k2]:.2f} log Y {a['ly']:+.3f} +- {a['se']:.3f}; R500 edge {EDGES[k5]:.2f} log Y {b['ly']:+.3f} +- {b['se']:.3f}")
P("reported: Gamma by edge, M3, h 0.672, f* 0.034 (zeta_b, zeta_shear M_sun/pc^2)")
BYE = []
W, V = data("h0672"); Wm, Vm = W[se], V[se]; Sb = (1 + .034) * stack(Wm, Wm * build("h0672")[0][se]); Ss = stack(Wm, Vm)
for k in range(2, 8): BYE.append((float(EDGES[k]), float(zeta(Sb, k)), float(zeta(Ss, k)))); P(f"  R {EDGES[k]:.2f}: {zeta(Sb, k):.2f}, {zeta(Ss, k):.2f}, Gamma {zeta(Sb, k) / zeta(Ss, k):.4f}")
P("reported: sensitivities, M3 at R200 edge, h 0.672, f* 0.034 (log Y; bootstrap kept off, central only)")
r0 = rows[0]; k = r0["k2"]; ly0 = r0["ly"]; SEN = {}
def cen(Ag, Rmax=8): a, b = stat("h0672", .034, Ag, se, k, Rmax); return math.log10(a / b / FAIR)
SEN["Rmax 2.06 (nearest edge; criteria wrote 2.18)"] = cen(build("h0672")[0], 7) if k < 7 else None
SEN["s 2.676"] = cen(build("h0672", s=2.676)[0]); SEN["s 3.071"] = cen(build("h0672", s=3.071)[0]); SEN["miscentred gas"] = cen(build("h0672", cen=True)[0])
Sig = float(zeta(Ss, k)) ; kap = None
m2 = MY["den"][:, 1]; m3 = MY["m3to8"][:, 1, 0]; ratio = (m3[se] / np.where(m2[se] > 0, m2[se], np.inf)); SEN["f_r - 1 (k-based, top bin of the aperture, order of magnitude)"] = float(np.median(ratio[:, k])) * Sig * KG
SEN["Mgas500 catalogue error, median dex"] = float(np.median(0.5 * np.log10(MGH[se] / MGL[se])))
for a, b in SEN.items(): P(f"  {a}: {b if b is None else round(b, 4)}")
json.dump(dict(verdict=C + sd_tag, radial=tags, rows=[{k_: v for k_, v in r.items() if k_ not in ("boot", "r5")} | dict(r5={a: b for a, b in r["r5"].items() if a != "boot"}) for r in rows], reference={str(c): SHP[c][1] for c in SHP}, others=OTH, by_edge=BYE, sens=SEN, R200_med_M3=float(np.nanmedian(build("h0672")[1][se]))), open(os.path.join(HERE, "lf1_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
