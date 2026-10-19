"""CFG824 -- H-FOSSIL: does the dwarf excess over the galaxy law grow with quenching age?  Criteria: FROZEN_CRITERIA.md (fba1e9482).
tau50 / tau90 = lookback times at which the published cumulative SFH (Weisz+14 VizieR J/ApJ/789/147: table6 combined fields where
given, else table5) reaches 50% / 90% (linear in log t between grid points).  sigma_law = CFG821's isolated law, unchanged.
Run: python3 cfg824.py   (CFG824_MUTATE=1: injection + shuffle controls).  kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, numpy as np
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
DS = os.path.join(REPO, "real_research", "data", "dsph"); WZ = os.path.join(DS, "weisz2014_dl")
MUT = os.environ.get("CFG824_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, PC = 6.674e-11, 1.989e30, 3.0857e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; WID = 0.15
TRAIN = {"Antlia II", "Canes Venatici I", "Carina", "Crater II", "Draco", "Fornax", "Leo I", "Leo II", "Sculptor", "Sextans", "Ursa Minor"}
NAMEMAP = {"Canes Venetici I": "Canes Venatici I", "Canes Venetici II": "Canes Venatici II", "DDO 210": "Aquarius",
           "Pegasus": "Pegasus dIrr", "Sag DIG": "Sagittarius dIrr", "M32": "M 32"}
def fnum(x):
    try: return float(x)
    except: return None
# ---- Weisz+14 cumulative SFHs -> tau50, tau90 (Gyr lookback)
def read_tsv(fn):
    L = [l.rstrip("\n") for l in open(fn) if not l.startswith("#") and l.strip()]
    hdr = L[0].split("\t"); rows = []
    for l in L[3:]:
        v = l.split("\t")
        if len(v) == len(hdr): rows.append(dict(zip(hdr, [x.strip() for x in v])))
    return rows
def taus(r):
    fk = {float(k[1:]): fnum(v) for k, v in r.items() if k.startswith("f") and k[1:].replace(".", "").isdigit() and fnum(v) is not None}
    grid = sorted(fk, reverse=True); f = np.array([fk[g] for g in grid])
    out = {}
    for X in (0.5, 0.9):
        if f[0] >= X: out[X] = 10 ** grid[0] / 1e9; continue
        i = int(np.argmax(f >= X)); lt = grid[i - 1] + (X - f[i - 1]) * (grid[i] - grid[i - 1]) / (f[i] - f[i - 1])
        out[X] = 10 ** lt / 1e9
    return out[0.5], out[0.9]
T6 = {r["ID"]: r for r in read_tsv(os.path.join(WZ, "table6.tsv"))}
AGE = {}
for r in read_tsv(os.path.join(WZ, "table5.tsv")):
    nm = r["ID"]
    if nm in AGE: continue
    src = T6.get(nm, r); t50, t90 = taus(src)
    AGE[NAMEMAP.get(nm, nm)] = dict(tau50=t50, tau90=t90, combined=nm in T6, weisz_id=nm)
# ---- LVD kinematics
LVD = {}
for fn in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(DS, fn))):
        MV, s_, es, rh = fnum(r.get("M_V")), fnum(r.get("vlos_sigma")), fnum(r.get("vlos_sigma_em")), fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical"))
        LVD[r["name"]] = dict(MV=MV, so=s_, eso=es or (0.1 * s_ if s_ else None), rhl=rh, file=fn)
# ---- CFG821 isolated law (unchanged statements, Upsilon as an argument)
def wolf(M, rhl): return math.sqrt(G * M * Msun / (6.0 * (4.0 / 3.0) * rhl * PC)) / 1e3
def nu(y): y = max(y, 1e-12); return 1.0 / (-math.expm1(-math.sqrt(y)))
def law(g, a0, ups):
    M = ups * 10 ** (0.4 * (4.83 - g["MV"])); y = G * (M / 2) * Msun / ((4 / 3) * g["rhl"] * PC) ** 2 / a0
    return wolf(M, g["rhl"]) * math.sqrt(nu(y))
ups_ml = lambda t50: min(4.0, max(0.5, 2.0 * (t50 / 10.0) ** 0.7))
rows, skipped = [], []
for nm, a in sorted(AGE.items()):
    g = LVD.get(nm)
    if g is None or not g["so"] or not g["rhl"] or g["MV"] is None: skipped.append(f"{nm} ({'no LVD row' if g is None else 'no sigma/r_h/M_V'})"); continue
    rows.append(dict(name=nm, train=nm in TRAIN, **a, **g))
def score(sel, foot, ml, Eover=None, tauover=None):
    E = np.array([math.log(r["so"] / law(r, A0[foot], ups_ml(r["tau50"]) if ml else 2.0)) for r in sel]) if Eover is None else Eover
    t = np.array([r["tau90"] for r in sel]) if tauover is None else tauover
    w = np.array([1 / ((r["eso"] / r["so"]) ** 2 + (math.log(10) * WID / 2) ** 2) for r in sel])
    rho, p = spearmanr(E, t, alternative="greater"); _, pneg = spearmanr(E, t, alternative="less")
    A = np.vstack([np.ones_like(t), t]).T; W = np.diag(w); cov = np.linalg.inv(A.T @ W @ A); b = cov @ A.T @ W @ E
    return dict(N=len(sel), rho=float(rho), p_greater=float(p), p_less=float(pneg), slope=float(b[1]), slope_err=float(math.sqrt(cov[1, 1])),
                tau_range=float(t.max() - t.min()), E=E.tolist())
def classify(pr, ml):
    if pr["N"] < 8 or pr["tau_range"] < 4: return "NOT DIAGNOSTIC"
    if pr["rho"] > 0 and pr["p_greater"] < 0.05 and ml["rho"] > 0 and ml["p_greater"] < 0.10: return "SUPPORTS"
    if pr["rho"] < 0 and pr["p_less"] < 0.05: return "OPPOSITE"
    return "NO SIGNAL"
OOS = [r for r in rows if not r["train"]]; TR = [r for r in rows if r["train"]]
P(f"CFG824  H-FOSSIL age test" + ("  [MUTATE]" if MUT else "") + f"   Weisz+14 galaxies {len(AGE)}, with LVD sigma {len(rows)} (out-of-sample {len(OOS)}, training {len(TR)})")
P(f"  skipped (no kinematics): {', '.join(skipped)}")
RES = dict(lane="CFG824", mutate=MUT, skipped=skipped, rows={})
if not MUT:
    P(f"\n  {'dwarf':18s} {'set':5s} {'tau50':>6s} {'tau90':>6s} {'sig_obs':>7s} {'law(2)':>7s} {'E':>6s} {'law(ML)':>7s} {'E_ML':>6s}")
    for r in sorted(rows, key=lambda r: (r["train"], -r["tau90"])):
        l2, lm = law(r, A0["canonical"], 2.0), law(r, A0["canonical"], ups_ml(r["tau50"]))
        RES["rows"][r["name"]] = dict(train=r["train"], tau50=r["tau50"], tau90=r["tau90"], combined=r["combined"], so=r["so"], eso=r["eso"], law2=l2, lawML=lm, E=math.log(r["so"] / l2), E_ML=math.log(r["so"] / lm))
        P(f"  {r['name']:18s} {'TRAIN' if r['train'] else 'OOS':5s} {r['tau50']:6.2f} {r['tau90']:6.2f} {r['so']:7.2f} {l2:7.2f} {math.log(r['so'] / l2):+6.2f} {lm:7.2f} {math.log(r['so'] / lm):+6.2f}")
    for foot in ("canonical", "alt"):
        pr, ml = score(OOS, foot, False), score(OOS, foot, True)
        cls = classify(pr, ml); RES[foot] = dict(primary=pr, C_ML=ml, cls=cls)
        tr = score(TR, foot, False)
        P(f"\n  [{foot}] OUT-OF-SAMPLE N {pr['N']}  tau90 range {pr['tau_range']:.1f} Gyr")
        P(f"     primary (Ups 2): rho {pr['rho']:+.2f}  p(>0) {pr['p_greater']:.3f}  p(<0) {pr['p_less']:.3f}  slope {pr['slope']:+.3f} +- {pr['slope_err']:.3f} per Gyr")
        P(f"     C-ML (Ups(tau50)): rho {ml['rho']:+.2f}  p(>0) {ml['p_greater']:.3f}  slope {ml['slope']:+.3f} +- {ml['slope_err']:.3f}")
        P(f"     TRAINING (MW, {tr['N']}; not a verdict): rho {tr['rho']:+.2f}  p(>0) {tr['p_greater']:.3f}  slope {tr['slope']:+.3f}")
        P(f"     CLASS: {cls}")
    d = [r for r in rows if r["name"] == "Draco"][0]; k1 = law(d, A0["canonical"], 2.0)
    P(f"\n  K1 Draco law {k1:.2f} vs CFG821 4.61 -> {'PASS' if abs(k1 - 4.61) < 0.01 else 'FAIL'}")
    RES["cls"] = RES["canonical"]["cls"]; P(f"\n  CLASS (canonical, out-of-sample): {RES['cls']}")
else:
    rng = np.random.default_rng(824); t = np.array([r["tau90"] for r in OOS])
    Einj = 0.06 * t + rng.normal(0, 0.1, len(t))
    a, b = score(OOS, "canonical", False, Eover=Einj), score(OOS, "canonical", True, Eover=Einj)
    c1 = classify(a, b); P(f"  injection E = 0.06 tau90 + N(0,0.1): rho {a['rho']:+.2f} p {a['p_greater']:.4f} -> {c1} (must be SUPPORTS)")
    ts = rng.permutation(t); a2, b2 = score(OOS, "canonical", False, tauover=ts), score(OOS, "canonical", True, tauover=ts)
    c2 = classify(a2, b2); P(f"  shuffled tau90 on real E: rho {a2['rho']:+.2f} p {a2['p_greater']:.3f} -> {c2} (must NOT be SUPPORTS)")
    RES.update(injection=dict(a, cls=c1), shuffle=dict(a2, cls=c2), bites=(c1 == "SUPPORTS" and c2 != "SUPPORTS"))
    P(f"  MUTATE bites: {RES['bites']}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg824_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg824{sfx}.out"), "w").write("\n".join(OUT) + "\n")
