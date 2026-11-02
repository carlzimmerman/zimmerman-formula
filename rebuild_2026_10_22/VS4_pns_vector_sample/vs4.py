# VS4: law offsets from PN dispersions read off Pulsoni+18's vector figures. MUTATE=1 shuffles slow labels within mass terciles. One thread, seconds.
import json, math, os, re, sys
import numpy as np
import fitz
from scipy.optimize import brentq

MUT = os.environ.get("MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
sys.path.insert(0, f"{REPO}/campaign_fresh_gravity")
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4
SRC = f"{REPO}/_external_data/vs3_pulsoni2018/src"
rng = np.random.default_rng(20261102)
G, KPC, MSUN = 6.674e-11, 3.0857e19, 1.989e30
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
nu = lambda y: np.asarray(C4.nu_mono(np.maximum(np.asarray(y, float), 1e-14)), float)

# Panels top to bottom, with y ticks read from each rendering.
PANELS = {
    "SR1": [(1399, 100, 350), (3608, 0, 250), (3923, 100, 350), (4365, 100, 350), (4374, 100, 350), (4472, 100, 350), (4552, 100, 350), (4636, 100, 350), (5846, 100, 350)],
    "FR1": [(584, 0, 250), (821, 0, 250), (1023, 0, 250), (1316, 0, 250), (1344, 0, 250), (2768, 0, 250), (2974, 0, 250), (3115, 0, 250)],
    "FR2": [(3377, 0, 250), (3379, 0, 250), (3384, 0, 250), (3489, 0, 250), (4278, 0, 250), (4339, 0, 250), (4473, 0, 250), (4494, 0, 250)],
    "FR3": [(4564, 0, 250), (4594, 50, 300), (4649, 100, 350), (4697, 50, 300), (4742, 0, 250), (5128, 0, 250), (5866, 0, 250), (7457, 0, 250)],
}

def navy(c):
    return c is not None and c[0] == 0 and abs(c[2] - 0.502) < 0.01

def extract(fig, panels):
    dr = fitz.open(f"{SRC}/{fig}_sigma.pdf")[0].get_drawings()
    lines = [d["items"][0] for d in dr if navy(d.get("color")) and d["items"][0][0] == "l"]
    marks = [d["rect"] for d in dr if navy(d.get("fill"))]
    hl = [d["rect"] for d in dr if d.get("color") == (0.0, 0.0, 0.0) and len(d["items"]) == 1 and d["rect"].width > 300 and d["rect"].height == 0]
    ys = sorted({round(r.y0, 1) for r in hl}); x0, x1 = min(r.x0 for r in hl), max(r.x1 for r in hl)
    frames = [(ys[i], ys[i + 1]) for i in range(0, len(ys), 2)]
    assert len(frames) == len(panels), (fig, len(frames), len(panels))
    out = {}
    for (top, bot), (n, lo, hi) in zip(frames, panels):
        pts = []
        for r in marks:
            cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
            if not top < cy < bot: continue
            v = [abs(l[1].y - l[2].y) for l in lines if abs(l[1].x - l[2].x) < 1e-3 and abs(l[1].x - cx) < 1.0 and min(l[1].y, l[2].y) - 0.5 <= cy <= max(l[1].y, l[2].y) + 0.5]
            sc = (hi - lo) / (bot - top)
            pts.append(((cx - x0) / (x1 - x0) * 14, lo + (bot - cy) * sc, (max(v) / 2 * sc) if v else float("nan")))
        out[n] = sorted(pts)
    return out

PTS = {}
for fig, pan in PANELS.items():
    PTS.update(extract(fig, pan))

# Paper tables: D, R_e, eps, Vsys.
tex = open(f"{SRC}/PNSpaperETGhalokinematics_2018-07-16.tex").read().split("\n")
T1, VS = {}, {}
for l in tex:
    m = re.match(r"\s*(\d{4})\s*&\s*\$-[\d.]+\$\s*&\s*([\d.]+)\s*&\s*([FS])\s*&\s*([\d.]+)\s*\(\d+\)\s*&\s*[\d.]+\s*&\s*[\d.]+\s*&\s*\$\s*([\d.]+)", l)
    if m: T1[int(m[1])] = dict(D=float(m[2]), cls=m[3], Re=float(m[4]), eps=float(m[5]))
    m = re.match(r"\s*(\d{4})\s*&.*?&\s*([\d.]+)\.?\$\\pm\$", l)
    if m: VS[int(m[1])] = float(m[2])

A3 = {}
for l in open(f"{REPO}/real_research/data/atlas3d_fj_table.tsv"):
    if l.startswith("#") or not l.strip(): continue
    p = l.rstrip("\n").split("\t")
    if p[0] == "name": H = p; continue
    A3[p[0]] = dict(zip(H, p))
EM = {}
for ln in open(f"{REPO}/_external_data/atlas3d_emsellem11/tableb1.tsv"):
    p = ln.rstrip("\n").split("\t")
    if len(p) > 16 and p[1].strip().startswith("NGC"):
        EM[p[1].strip()] = dict(cls=p[10].strip(), ra=float(p[15]), de=float(p[16]))
TM = []
for x in (l.rstrip("\n").split("\t") for l in open(f"{REPO}/real_research/data/2mrs_huchra2012.tsv") if not l.startswith("#")):
    try: TM.append([float(x[0]), float(x[1]), float(x[2]), float(x[3])])
    except (ValueError, IndexError): pass
TM = np.array(TM)

def central(n, Rk, dv):
    e = EM[f"NGC{n:04d}"]; D = T1[n]["D"]; v = VS[n]
    dr = np.hypot((TM[:, 0] - e["ra"]) * np.cos(np.radians(e["de"])), TM[:, 1] - e["de"]); i = np.argmin(dr)
    return not (TM[(dr < np.degrees(Rk / 1e3 / D)) & (np.abs(TM[:, 2] - v) < dv) & (dr > 0.02), 3] < TM[i, 3]).any()

# CFG492's law path.
RG = np.geomspace(1e-3, 1e8, 6000); LR = np.log(RG); U = np.linspace(0, 14, 4000); CH = np.cosh(U); AS = math.pi / 180 / 3600
def offset(n, a0):
    t = T1[n]; a = A3[f"NGC{n:04d}"]; f = float
    Mj = 10 ** (f(a["logML_JAM"]) + f(a["logL"])) * t["D"] / f(a["Dist_Mpc"]); r12 = 10 ** f(a["logr12"]) * AS * t["D"] * 1e3
    Re = t["Re"] * AS * t["D"] * 1e3; ah = Re / 1.8153
    M = 10 ** brentq(lambda lm: math.log10(0.5 * 10 ** lm * float(nu(G * 0.5 * 10 ** lm * MSUN / (r12 * KPC) ** 2 / a0))) - math.log10(0.5 * Mj), math.log10(Mj) - 4, math.log10(Mj) + 1, xtol=1e-12)
    gN = G * M * MSUN * RG ** 2 / (RG + ah) ** 2 / (RG * KPC) ** 2; g = gN * nu(gN / a0)
    rho = lambda r: 1.0 / (r * (r + ah) ** 3)
    w = rho(RG) * g * RG * KPC
    s2 = np.concatenate([np.cumsum((0.5 * (w[1:] + w[:-1]) * np.diff(LR))[::-1])[::-1], [0.0]]) / rho(RG)
    p = np.array(PTS[n]); R = p[:, 0] * Re * math.sqrt(1 - t["eps"]); keep = R > max(Re, 2.0)
    if not keep.any(): return None
    pr = []
    for Rb in R[keep]:
        r = Rb * CH; s = np.exp(np.interp(np.log(r), LR, np.log(np.maximum(s2, 1e-30)))); q = rho(r)
        pr.append(math.sqrt(np.trapz(q * s * r, U) / np.trapz(q * r, U)) / 1e3)
    d = np.log10(p[keep, 1] / np.array(pr)); e = p[keep, 2] / p[keep, 1] / math.log(10)
    return dict(O=float(d.mean()), e=float(math.sqrt(np.nansum(e ** 2)) / keep.sum()), lM=math.log10(M), nb=int(keep.sum()), q=int(float(a["qual"])), slow=EM[f"NGC{n:04d}"]["cls"] == "S")

def fit(O, M, S, C):
    X = np.c_[np.ones_like(M), M - M.mean(), S.astype(float), C.astype(float)]
    b = np.linalg.lstsq(X, O, rcond=None)[0]; r = O - X @ b
    se = np.sqrt(np.diag(r @ r / (len(O) - 4) * np.linalg.inv(X.T @ X)))
    return dict(n=len(O), mass=b[1], mass_se=se[1], s=b[2], s_se=se[2], k=b[3], k_se=se[3], rms=float(np.sqrt(r @ r / (len(O) - 4))), corr_sc=float(np.corrcoef(S, C)[0, 1]))

def label(f, f_noq0, f_500, nsn):
    s, ss, k, ks = f["s"], f["s_se"], f["k"], f["k_se"]
    if nsn >= 4 and s >= 0.10 and s / ss > 3 and abs(k) < ks and f_noq0["s"] / f_noq0["s_se"] > 2 and f_500["s"] / f_500["s_se"] > 2: return "SETTLED ROTATION"
    if k >= 0.10 and k / ks > 3 and abs(s) < ss and f_noq0["k"] / f_noq0["k_se"] > 2 and f_500["k"] / f_500["k_se"] > 2: return "SETTLED ENVIRONMENT"
    if s + 2 * ss < 0.10 and k + 2 * ks < 0.10: return "SPLIT NOT REAL"
    if s >= 0.10 and s / ss > 2 and abs(k) < ks: return "LEANS ROTATION"
    if k >= 0.10 and k / ks > 2 and abs(s) < ss: return "LEANS ENVIRONMENT"
    return "UNDECIDED"

names = sorted(n for n in PTS if f"NGC{n:04d}" in A3 and f"NGC{n:04d}" in EM and n in T1 and n in VS)
print("panels", {k: len(v) for k, v in PTS.items()})
print("missing bar", [n for n in PTS if any(not math.isfinite(p[2]) for p in PTS[n])]); print("not usable", sorted(set(PTS) - set(names)))
print("class disagreements paper vs Emsellem", [n for n in names if T1[n]["cls"] != EM[f"NGC{n:04d}"]["cls"]])
ref = json.load(open(f"{REPO}/campaign_fresh_gravity/CFG492_multisource_synthesis/cfg492_gc_vs_pn_results.json"))["per_galaxy"]
out = {"mode": "MUTATE" if MUT else "normal", "points": {str(k): v for k, v in PTS.items()}}; labs = {}
for foot, a0 in A0.items():
    rows = {n: r for n in names if (r := offset(n, a0))}
    ns = list(rows); O = np.array([rows[n]["O"] for n in ns]); M = np.array([rows[n]["lM"] for n in ns]); S = np.array([rows[n]["slow"] for n in ns]); Q = np.array([rows[n]["q"] for n in ns])
    if MUT:
        for c in np.array_split(np.argsort(M), 3): S[c] = rng.permutation(S[c])
    res = {}
    for w in ((1000, 1000), (500, 500), (300, 500)):
        C = np.array([central(n, *w) for n in ns]); key = f"{w[0]}/{w[1]}"
        res[key] = dict(fit(O, M, S, C), quadrants={lab: dict(n=int(q.sum()), mean=float(O[q].mean()) if q.any() else None, names=[n for n, k in zip(ns, q) if k]) for lab, q in (("slow_central", S & C), ("slow_non", S & ~C), ("fast_central", ~S & C), ("fast_non", ~S & ~C))})
        for n, c in zip(ns, C): rows[n][f"central_{key}"] = bool(c)
        if key == "1000/1000": res["no_q0"] = fit(O[Q > 0], M[Q > 0], S[Q > 0], C[Q > 0]); nsn = int((S & ~C).sum())
    labs[foot] = label(res["1000/1000"], res["no_q0"], res["500/500"], nsn)
    ov = [n for n in ns if str(n) in ref[foot] and ref[foot][str(n)].get("O_PN") is not None]
    dif = np.array([rows[n]["O"] - ref[foot][str(n)]["O_PN"] for n in ov]); rms = float(np.sqrt((dif ** 2).mean()))
    res["C1"] = dict(rms=rms, mean=float(dif.mean()), per={n: float(d) for n, d in zip(ov, dif)})
    out[foot] = dict(rows=rows, **res)
    print(f"\n{foot}: {labs[foot]}, slow non-centrals {nsn}, C1 rms {rms:.3f}, mean diff {dif.mean():+.3f}, per {res['C1']['per']}")
    for k in ("1000/1000", "no_q0", "500/500", "300/500"):
        f = res[k]; print(f"  {k}: n {f['n']} slow {f['s']:+.3f} +- {f['s_se']:.3f}, central {f['k']:+.3f} +- {f['k_se']:.3f}, mass {f['mass']:+.3f} +- {f['mass_se']:.3f}, rms {f['rms']:.3f}, corr {f['corr_sc']:+.2f}" + (f"\n     {f['quadrants']}" if "quadrants" in f else ""))
    if foot == "canonical":
        for n in ns: print(f"   NGC{n:<5d}{'slow' if rows[n]['slow'] else 'fast'} q{rows[n]['q']} logM {rows[n]['lM']:.2f} bins {rows[n]['nb']} O {rows[n]['O']:+.3f} +- {rows[n]['e']:.3f} cen1000 {rows[n]['central_1000/1000']} cen500 {rows[n]['central_500/500']}")
c1ok = all(out[f]["C1"]["rms"] <= 0.05 for f in A0)
out["labels"] = labs; out["C1_pass"] = c1ok
L = labs["canonical"] if labs["canonical"] == labs["alt"] else "FOOTING-DEPENDENT"
out["label"] = L if c1ok else "NO VERDICT (C1)"
json.dump(out, open(f"{HERE}/vs4{'_MUTATE' if MUT else ''}.json", "w"), indent=1, default=float)
print("\nC1 pass", c1ok, "LABEL", out["label"])
