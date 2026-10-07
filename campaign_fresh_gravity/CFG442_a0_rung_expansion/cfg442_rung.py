#!/usr/bin/env python3
"""CFG442: expanded ladder-anchored gas-dominated a0 rung (criteria FROZEN_CRITERIA.md, dd851292c).
Samples: S0 = CFG397 anchor (reproduced, control C0); SR = SPARC flow/UMa gas galaxies re-distanced with Cosmicflows-4 TRGB/Cepheid;
LT = LITTLE THINGS (Oh+2015) non-SPARC galaxies, baryons read from the vector paths of the arXiv-source disk-halo figures, axes calibrated on the
VizieR total-curve markers (C1 gates). Statistic = CFG397's (bounded min of weighted log-g residuals, nu_mono kernel; galaxy bootstrap 500, seed 7).
Inputs: data/ (VizieR Oh+2015, Hunter+2012, Sesame) and ../_external_data/cfg442/ (CF4 table2, figure PDFs) from cfg442_fetch.py.
Run: python3 cfg442_rung.py [--mutate]
"""
import os, sys, io, re, json, math, contextlib
import numpy as np
import fitz                                    # PyMuPDF: vector paths of the figure PDFs
from scipy.optimize import minimize_scalar
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
DAT = os.path.join(HERE, "data"); EXT = os.path.join(LANES, "_external_data", "cfg442"); FIG = os.path.join(EXT, "oh15_figs")
OUT = []
def P(s=""): print(s); OUT.append(str(s))
def finish(code, res=None):
    if res is not None: json.dump(res, open(os.path.join(HERE, f"cfg442_rung{TAG}_results.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg442_rung{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(code)
KPC = 3.0857e19
FOOT = (("canonical", 9.3603e-11), ("alt", 1.1312e-10), ("PAPER43 gas-point", 8.3e-11))
# ---------------------------------------------------------------- galaxy record: R [kpc], Vobs, eV, Vgas (signed), Vdisk, Vbul [km/s]
# LT stars are stored as Vdisk = V_star,auth / sqrt(0.5), so Upsilon 0.5 reproduces the authors' SPS stellar curve and 0.7 multiplies V_star^2 by 1.4.
def rec(name, sample, R, Vobs, eV, Vgas, Vdisk, Vbul, **kw):
    return dict(name=name, sample=sample, R=np.asarray(R, float), Vobs=np.asarray(Vobs, float), eV=np.asarray(eV, float),
                Vgas=np.asarray(Vgas, float) * (0 if MUT else 1), Vdisk=np.asarray(Vdisk, float), Vbul=np.asarray(Vbul, float), **kw)
def sel_points(g):
    vg2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2
    vb2 = vg2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2
    return (vg2 >= 0.7 * vb2) & (vb2 > 0) & (g["Vobs"] > 0)
def arrays(gs, U):                                            # CFG397's arrays(), unchanged
    out = []
    for g in gs:
        m = sel_points(g); R = g["R"][m] * KPC; vg = g["Vgas"][m]
        b = (np.sign(vg) * vg ** 2 + U * g["Vdisk"][m] ** 2 + 1.4 * U * g["Vbul"][m] ** 2) * 1e6 / R
        o = (g["Vobs"][m] * 1e3) ** 2 / R
        w = 1 / (np.clip(g["eV"][m], 1, None) / np.clip(g["Vobs"][m], 1, None)) ** 2
        ok = (b > 0) & (o > 0)
        out.append((b[ok], o[ok], w[ok]))
    return out
def fit(parts):                                               # CFG397's fit(), unchanged
    gb = np.concatenate([p[0] for p in parts]); go = np.concatenate([p[1] for p in parts]); w = np.concatenate([p[2] for p in parts])
    lgo, lgb = np.log10(go), np.log10(gb)
    f = lambda la: np.sum(w * (lgo - lgb - np.log10(C.nu_mono(gb / 10 ** la))) ** 2)
    return minimize_scalar(f, bounds=(-10.8, -9.3), method="bounded", options={"xatol": 1e-5}).x
def fit_boot(gs):
    parts = arrays(gs, 0.5); la = fit(parts)
    rng = np.random.default_rng(7)
    bs = [fit([parts[i] for i in rng.integers(0, len(parts), len(parts))]) for _ in range(500)]
    return dict(n=len(gs), log_a0=float(la), sd=float(np.std(bs)), npts=int(sum(len(p[0]) for p in parts)), names=[g["name"] for g in gs])
def rescale(g, f):                                            # R ∝ D; V_bar^2 terms ∝ D; V_obs unchanged
    h = dict(g); h["R"] = g["R"] * f; s = math.sqrt(f)
    for k in ("Vgas", "Vdisk", "Vbul"): h[k] = g[k] * s
    return h
# ---------------------------------------------------------------- SPARC (CFG397's galaxy list)
SP = []
for g in C.load_sparc():
    if g["meta"] and g["meta"]["Q"] <= 2:
        SP.append(rec(g["name"], "SPARC", g["R"], g["Vobs"], g["eV"], g["Vgas"], g["Vdisk"], g["Vbul"], meta=g["meta"]))
SPd = {g["name"]: g for g in SP}
use_sp = [g for g in SP if sel_points(g).sum() >= 3]
# ---------------------------------------------------------------- Cosmicflows-4 table2 (byte positions from its ReadMe)
CF4 = {}
for l in open(os.path.join(EXT, "cf4_table2.dat")):
    def fl(a, b):
        s = l[a - 1:b].strip(); return float(s) if s else None
    CF4[int(l[0:7])] = dict(pgc=int(l[0:7]), DM=fl(29, 34), DMtrgb=fl(103, 107), e_trgb=fl(109, 112), DMceph=fl(114, 119), e_ceph=fl(121, 125),
                            ra=fl(138, 145), dec=fl(147, 154))
cf_pgc = np.array(list(CF4)); cf_ra = np.array([CF4[k]["ra"] for k in cf_pgc]); cf_de = np.array([CF4[k]["dec"] for k in cf_pgc])
def ladder(e):
    if e is None: return None, None, None
    if e["DMtrgb"] is not None: return 10 ** ((e["DMtrgb"] - 25) / 5), "CF4 TRGB", e["DMtrgb"]
    if e["DMceph"] is not None: return 10 ** ((e["DMceph"] - 25) / 5), "CF4 Cepheid", e["DMceph"]
    return None, None, None
# ---------------------------------------------------------------- empty-selection check (MUTATE)
n_sel_sparc = len(use_sp)
P(f"CFG442 expanded gas-dominated rung{' [MUTATE: gas dropped]' if MUT else ''}: SPARC Q<=2 galaxies with >= 3 gas-dominated points: {n_sel_sparc}")
# ---------------------------------------------------------------- S0 and control C0
S0 = [g for g in use_sp if g["meta"]["fD"] in (2, 3, 5)]
# ---------------------------------------------------------------- SR: re-distanced SPARC flow / UMa galaxies
ses = json.load(open(os.path.join(DAT, "sesame_sr.json")))
SR, sr_log = [], []
for g in use_sp:
    if g["meta"]["fD"] not in (1, 4): continue
    s = ses.get(g["name"])
    if not s or s["ra"] is None or s["dec"] is None:
        sr_log.append((g["name"], "unresolved by Sesame", None)); continue
    sep = np.hypot((cf_ra - s["ra"]) * math.cos(math.radians(s["dec"])), cf_de - s["dec"]) * 60
    i = int(np.argmin(sep))
    if sep[i] > 1.0:
        sr_log.append((g["name"], f"no CF4 entry within 1' (nearest {sep[i]:.1f}')", None)); continue
    e = CF4[int(cf_pgc[i])]; D, meth, dm = ladder(e)
    if D is None:
        sr_log.append((g["name"], f"CF4 PGC {e['pgc']}: no TRGB/Cepheid modulus", None)); continue
    f = D / g["meta"]["D"]
    h = rescale(g, f); h.update(sample="SR", D_old=g["meta"]["D"], D_new=D, method=meth, pgc=e["pgc"], sep_arcmin=float(sep[i]))
    SR.append(h); sr_log.append((g["name"], f"CF4 PGC {e['pgc']} sep {sep[i]:.2f}' {meth} D {D:.2f} Mpc vs SPARC {g['meta']['D']:.2f} (ratio {f:.3f})", f))
# ---------------------------------------------------------------- LT: LITTLE THINGS (Oh+2015)
key = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
SPARC_ALIAS = {"ddo50": "UGC04305", "ddo87": "UGC05918", "ddo126": "UGC07559", "ddo154": "DDO154", "ddo168": "DDO168", "haro29": "UGCA281",
               "ngc2366": "NGC2366", "wlm": "UGCA444"}
NO_STARS = {"ddo43", "ddo46", "ddo47", "f564v3", "haro29"}
FALLBACK = {"ddo70": "6", "ngc1569": "16", "ugc8508": "1"}             # Hunter+2012 ref code: Sakai+2004, Grocholski+2008, Dalcanton+2009
def load_rc(fn):
    out = {}
    for l in open(os.path.join(DAT, fn)):
        p = l.split()
        if len(p) < 7 or p[1] != "Data": continue
        R0, V0, Rs, Vs, eVs = map(float, p[2:7]); out.setdefault(p[0], []).append((Rs * R0, Vs * V0, eVs * V0))
    return {k: np.array(v) for k, v in out.items()}
TOT, DMC = load_rc("oh15_rotdmbar.dat"), load_rc("oh15_rotdm.dat")
D_OH = {key(l[0:8]): float(l[32:36]) for l in open(os.path.join(DAT, "oh15_table1.dat"))}
HUN = {}
for l in open(os.path.join(DAT, "hunter12_table1.dat")):
    pg = l[20:25].strip()
    HUN[key(l[4:13])] = dict(pgc=int(pg) if pg else None, D=float(l[86:90]), ref=l[91:96].strip())
HUN["cvnidwa"]["pgc"] = 42275                                        # UGCA 292 (frozen)
def dsh(x): return [round(float(v), 1) for v in re.findall(r"[0-9.]+", str(x.get("dashes")).split("]")[0])]
def isgray(c, v): return c is not None and all(abs(c[i] - v) < 0.01 for i in range(3))
def vpts(x):
    Q = []
    for it in x["items"]:
        for q in it[1:]:
            if hasattr(q, "x"): Q.append((q.x, q.y))
    return np.array(Q)
def digitize(kk, t):
    """returns calibration diagnostics and the gas / star curves (R [kpc at D_Hunter], V [km/s]) from the disk-halo panel."""
    dr = fitz.open(os.path.join(FIG, [f for f in os.listdir(FIG) if key(f[len("rMD_DH_DM_profiles_"):-4]) == kk][0]))[0].get_drawings()
    frames = [x for x in dr if x["type"] == "s" and len(x["items"]) > 50 and x["rect"].x0 < 100 and x["rect"].width > 150 and x["rect"].y0 > 380]
    fr = min(frames, key=lambda x: x["rect"].y0)["rect"]
    mk = [x for x in dr if x["type"] == "f" and isgray(x.get("fill"), 0.5879) and len(x["items"]) == 10]
    cen = np.array([((x["rect"].x0 + x["rect"].x1) / 2, (x["rect"].y0 + x["rect"].y1) / 2) for x in mk])
    cen = cen[(cen[:, 0] > fr.x0) & (cen[:, 0] < fr.x1) & (cen[:, 1] > fr.y0) & (cen[:, 1] < fr.y1)]
    rng = np.random.default_rng(1); M, N = len(cen), len(t); best = (0, None)
    for _ in range(60000):
        i1, i2 = rng.choice(M, 2, replace=False); j1, j2 = rng.choice(N, 2, replace=False)
        if t[j1, 0] == t[j2, 0] or t[j1, 1] == t[j2, 1]: continue
        bx = (cen[i2, 0] - cen[i1, 0]) / (t[j2, 0] - t[j1, 0]); ax = cen[i1, 0] - bx * t[j1, 0]
        by = (cen[i2, 1] - cen[i1, 1]) / (t[j2, 1] - t[j1, 1]); ay = cen[i1, 1] - by * t[j1, 1]
        if bx <= 0 or by >= 0: continue
        px = ax + bx * t[:, 0]; py = ay + by * t[:, 1]
        if px.max() - px.min() < 0.4 * fr.width or py.max() - py.min() < 0.15 * fr.height: continue
        n = int((np.hypot(px[:, None] - cen[None, :, 0], py[:, None] - cen[None, :, 1]).min(1) < 0.5).sum())
        if n > best[0]: best = (n, (ax, bx, ay, by))
    ax, bx, ay, by = best[1]
    Dm = np.hypot((ax + bx * t[:, 0])[:, None] - cen[None, :, 0], (ay + by * t[:, 1])[:, None] - cen[None, :, 1])
    j = Dm.argmin(1); ok = Dm.min(1) < 0.5
    A = np.vstack([np.ones(ok.sum()), t[ok, 0]]).T; cx = np.linalg.lstsq(A, cen[j[ok], 0], rcond=None)[0]
    B = np.vstack([np.ones(ok.sum()), t[ok, 1]]).T; cy = np.linalg.lstsq(B, cen[j[ok], 1], rcond=None)[0]
    rx = float(np.sqrt(np.mean((A @ cx - cen[j[ok], 0]) ** 2))); ry = float(np.sqrt(np.mean((B @ cy - cen[j[ok], 1]) ** 2)))
    def curve(pat):
        Q = [vpts(x) for x in dr if x["type"] == "s" and dsh(x) == pat and len(x["items"]) > 1 and x["rect"].x0 >= fr.x0 - 1
             and x["rect"].x1 <= fr.x1 + 1 and x["rect"].y0 >= fr.y0 - 1 and x["rect"].y1 <= fr.y1 + 1]
        if not Q: return None
        Q = np.vstack(Q); R = (Q[:, 0] - cx[0]) / cx[1]; V = (Q[:, 1] - cy[0]) / cy[1]; o = np.argsort(R, kind="stable")
        R, V = R[o], V[o]; u = np.concatenate([[True], np.diff(R) > 1e-9]); return R[u], V[u]
    return dict(n_mk=M, n_inl=int(ok.sum()), rms_x=rx, rms_y=ry, gas=curve([1.4, 2.9]), star=curve([1.4, 2.9, 7.7, 2.9]))
LT, LT_overlap, lt_log = [], [], []
for nm in sorted(TOT):
    kk = key(nm); t = TOT[nm]; t = t[np.argsort(t[:, 0], kind="stable")]
    if kk in NO_STARS:
        lt_log.append((nm, "excluded: no authors' stellar curve" + (" (also SPARC)" if kk in SPARC_ALIAS else ""))); continue
    hu = HUN[kk]; Dh = D_OH[kk]
    if kk in SPARC_ALIAS:
        D, meth = None, "SPARC member: method control C2 only"
    else:
        D, meth, _ = ladder(CF4.get(hu["pgc"]))
        if D is None and kk in FALLBACK and hu["ref"] == FALLBACK[kk]:
            D, meth = hu["D"], f"fallback Hunter+2012 ref {hu['ref']} (TRGB paper)"
        if D is None:
            lt_log.append((nm, f"excluded: no ladder distance (CF4 PGC {hu['pgc']}: {'absent' if hu['pgc'] not in CF4 else 'no TRGB/Cepheid'}; Hunter ref '{hu['ref']}')")); continue
    dz = digitize(kk, t)
    gate_a = dz["n_inl"] >= 0.8 * min(len(t), dz["n_mk"] - 1) and dz["rms_x"] <= 0.15 and dz["rms_y"] <= 0.15
    if dz["gas"] is None or dz["star"] is None:
        lt_log.append((nm, "C1 FAIL: gas or star path not found")); continue
    (Rg, Vg), (Rs, Vs) = dz["gas"], dz["star"]
    lo, hi = max(Rg.min(), Rs.min()), min(Rg.max(), Rs.max())
    m = (t[:, 0] >= lo) & (t[:, 0] <= hi)
    R, Vt, eV = t[m, 0], t[m, 1], t[m, 2]
    vg = np.interp(R, Rg, Vg); vs = np.interp(R, Rs, Vs)
    dm = DMC.get(nm, np.zeros((0, 3))); rel = []
    for r, v, a, b in zip(R, Vt, vg, vs):
        jj = np.where(np.abs(dm[:, 0] - r) <= 1e-3 * r)[0]
        if len(jj): rel.append(abs(np.sign(a) * a * a + b * b - (v * v - dm[jj[0], 1] ** 2)) / (v * v))
    cons = float(np.median(rel)) if rel else float("nan")
    gate_b = bool(rel) and cons <= 0.02
    vg2 = np.sign(vg) * vg ** 2 * (1.33 / 1.4)
    g = rec(nm, "LT", R, Vt, eV, np.sign(vg2) * np.sqrt(np.abs(vg2)), np.abs(vs) / math.sqrt(0.5), 0 * R,
            D_old=Dh, D_new=D, method=meth, pgc=hu["pgc"], C1=dict(n_viz=len(t), n_markers=dz["n_mk"], n_inliers=dz["n_inl"], rms_x_pt=dz["rms_x"],
            rms_y_pt=dz["rms_y"], cons_median=cons, n_cons=len(rel), gate_a=bool(gate_a), gate_b=bool(gate_b), n_cover=int(m.sum())))
    tag = f"C1 {'pass' if gate_a and gate_b else 'FAIL'} (inliers {dz['n_inl']}/{len(t)} of {dz['n_mk']} markers, rms {dz['rms_x']:.3f}/{dz['rms_y']:.3f} pt, Vbar consistency {cons:.4f} on {len(rel)})"
    if not (gate_a and gate_b):
        lt_log.append((nm, tag + " -> excluded")); continue
    if kk in SPARC_ALIAS:
        g["sparc"] = SPARC_ALIAS[kk]; LT_overlap.append(g); lt_log.append((nm, tag + f"; SPARC member {SPARC_ALIAS[kk]} -> C2 only")); continue
    h = rescale(g, D / Dh); h["sample"] = "LT"; nsel = int(sel_points(h).sum())
    lt_log.append((nm, tag + f"; {meth} D {D:.2f} vs Hunter {Dh:.1f} Mpc; gas-dominated points {nsel}"))
    if nsel >= 3: LT.append(h)
SRu = [g for g in SR if sel_points(g).sum() >= 3]
n_all = len(S0) + len(SRu) + len(LT)
if n_all == 0:
    P("MUTATE: empty selection detected -> exit 1" if MUT else "empty selection -> exit 1"); finish(1)
# ---------------------------------------------------------------- C0: reproduce CFG397's anchor
c397 = json.load(open(os.path.join(LANES, "CFG397_gas_only_a0_rung", "cfg397_gas_rung_results.json")))["res"]["B ladder (TRGB/Cep/SNe)"]
r0 = fit_boot(S0)
c0 = abs(r0["log_a0"] - c397["log_a0"]) <= 0.002 and abs(r0["sd"] - c397["sd"]) <= 0.002
P(f"C0 reproduce CFG397 anchor: N {r0['n']}, log a0 {r0['log_a0']:+.4f} +- {r0['sd']:.4f} vs CFG397 {c397['log_a0']:+.4f} +- {c397['sd']:.4f} -> {'PASS' if c0 else 'FAIL'}")
P(""); P("SR (SPARC Hubble-flow / UMa gas-dominated galaxies, CF4 ladder distances):")
for n, s, f in sr_log: P(f"  {n:10s} {s}")
P(""); P("LT (LITTLE THINGS, Oh+2015):")
for n, s in lt_log: P(f"  {n:9s} {s}")
# ---------------------------------------------------------------- fits
samples = {"COMBINED (S0+SR+LT)": S0 + SRu + LT, "NEW-ONLY (SR+LT)": SRu + LT, "SR only": SRu, "LT only": LT, "S0 (CFG397 anchor)": S0,
           "COMBINED w/o fallback distances": S0 + SRu + [g for g in LT if not g["method"].startswith("fallback")]}
res = {}
P(""); P("Fits (CFG397 statistic; galaxy bootstrap 500, seed 7):")
for nm, gs in samples.items():
    if len(gs) < 2: P(f"  {nm:34s} N gal {len(gs)}: too few to fit"); continue
    res[nm] = fit_boot(gs)
    r = res[nm]; P(f"  {nm:34s} N gal {r['n']:3d} pts {r['npts']:4d}: a0 = {10 ** r['log_a0']:.3e} (log {r['log_a0']:+.3f} +- {r['sd']:.3f})")
# ---------------------------------------------------------------- C2: LT route vs SPARC route on the overlap galaxies
c2 = None
pairs = []
for g in LT_overlap:
    s = SPd.get(g["sparc"])
    if s is None: continue
    h = rescale(g, s["meta"]["D"] / g["D_old"])
    if sel_points(h).sum() >= 3 and sel_points(s).sum() >= 3: pairs.append((h, s))
if len(pairs) >= 1:
    la_lt = fit(arrays([p[0] for p in pairs], 0.5)); la_sp = fit(arrays([p[1] for p in pairs], 0.5)); d2 = la_lt - la_sp
    c2 = dict(galaxies=[p[1]["name"] for p in pairs], log_a0_LT=float(la_lt), log_a0_SPARC=float(la_sp), delta=float(d2), pass_=bool(abs(d2) <= 0.10),
              per_gal={p[1]["name"]: dict(LT=float(fit(arrays([p[0]], 0.5))), SPARC=float(fit(arrays([p[1]], 0.5)))) for p in pairs})
    P(""); P(f"C2 LT-route vs SPARC-route on {len(pairs)} overlap galaxies ({', '.join(c2['galaxies'])}): log a0 {la_lt:+.3f} vs {la_sp:+.3f}, "
             f"delta {d2:+.3f} dex -> {'PASS' if c2['pass_'] else 'FAIL'} (|delta| <= 0.10)")
    for k, v in c2["per_gal"].items(): P(f"    {k:10s} LT {v['LT']:+.3f}  SPARC {v['SPARC']:+.3f}  diff {v['LT'] - v['SPARC']:+.3f}")
else:
    P(""); P("C2: no overlap galaxy with >= 3 gas points in both routes -> C2 NOT EVALUABLE (treated as FAIL)")
c2ok = bool(c2 and c2["pass_"])
VNAME = "COMBINED (S0+SR+LT)" if c2ok else "S0+SR (C2 failed)"
if not c2ok:
    res[VNAME] = fit_boot(S0 + SRu); r = res[VNAME]
    P(f"  {VNAME:34s} N gal {r['n']:3d} pts {r['npts']:4d}: a0 = {10 ** r['log_a0']:.3e} (log {r['log_a0']:+.3f} +- {r['sd']:.3f})")
Vs = samples["COMBINED (S0+SR+LT)"] if c2ok else S0 + SRu
# ---------------------------------------------------------------- K1
k1 = {U: float(fit(arrays(Vs, U))) for U in (0.3, 0.5, 0.7)}
dk = k1[0.7] - k1[0.5]; k1ok = abs(dk) <= 0.05
P(""); P(f"K1 Upsilon check on {VNAME}: log a0 at 0.3/0.5/0.7 (LT stars x0.6/x1/x1.4) = {k1[0.3]:+.3f}/{k1[0.5]:+.3f}/{k1[0.7]:+.3f}; "
         f"0.5->0.7 shift {dk:+.3f} -> {'PASS' if k1ok else 'FAIL'}")
V = res[VNAME]; est = V["sd"] <= 0.05 and k1ok
P(""); P(f"RUNG {'ESTABLISHED' if est else 'NOT ESTABLISHED'} ({VNAME}: N {V['n']}, sd {V['sd']:.3f} {'<=' if V['sd'] <= 0.05 else '>'} 0.05; K1 {'pass' if k1ok else 'fail'})")
cmp = {}
for foot, a0 in FOOT:
    d = V["log_a0"] - math.log10(a0); cmp[foot] = dict(a0=a0, delta=float(d), nsig=float(d / V["sd"]))
    P(f"  {VNAME} vs {foot:18s} {a0:.4e}: {d:+.3f} dex ({d / V['sd']:+.2f} sigma) -> {'consistent' if abs(d) < 2 * V['sd'] else 'differs'}")
P(f"  shift from CFG397 anchor ({c397['log_a0']:+.3f}): {V['log_a0'] - c397['log_a0']:+.3f} dex")
if SRu:
    rat = np.array([g["D_new"] / g["D_old"] for g in SRu])
    P(f"  SR distance ratios CF4/SPARC: median {np.median(rat):.3f}, range {rat.min():.3f}-{rat.max():.3f} (N {len(rat)})")
perg = {g["name"]: dict(sample=g["sample"], log_a0_single=float(fit(arrays([g], 0.5))), n_gas=int(sel_points(g).sum()),
                        D_old=g.get("D_old", g.get("meta", {}).get("D") if g["sample"] == "SPARC" else None), D_new=g.get("D_new"), method=g.get("method"))
        for g in samples["COMBINED (S0+SR+LT)"]}
P(""); P("Per-galaxy single-fit log a0 (diagnostic only, not a verdict):")
for k, v in perg.items(): P(f"  {k:10s} {v['sample']:5s} n_gas {v['n_gas']:3d}  log a0 {v['log_a0_single']:+.3f}")
finish(0, dict(C0=dict(pass_=c0, log_a0=r0["log_a0"], sd=r0["sd"]), res=res, C2=c2, verdict_sample=VNAME, K1=k1, K1_pass=k1ok, established=est,
               compare=cmp, SR_log=sr_log, LT_log=lt_log, LT_C1={g["name"]: g["C1"] for g in LT + LT_overlap}, per_galaxy=perg))
