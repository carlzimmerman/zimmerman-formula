"""CFG827 (= CFG824b) -- dwarf age test with each dwarf's own SFH-based stellar M/L.  Criteria: FROZEN_CRITERIA.md (055269e4d).
E-MILES Kroupa SSPs x Weisz+14 SFHs; sigma_law = CFG821 isolated law unchanged.  Run: python3 cfg827.py  (CFG827_MUTATE=1).
kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, numpy as np
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
DS = os.path.join(REPO, "real_research", "data", "dsph"); WZ = os.path.join(DS, "weisz2014_dl")
MUT = os.environ.get("CFG827_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, PC = 6.674e-11, 1.989e30, 3.0857e16; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; WID = 0.15
def fnum(x):
    try: return float(x)
    except: return None
# ---- E-MILES SSP table
SSP = {}
for l in open(os.path.join(DS, "emiles_ml_dl", "UBBVRIJHK_ku_iPp0.00.MAG")).readlines()[1:]:
    v = l.split(); Z, age, Mn, mlV = float(v[2]), float(v[3]), float(v[4]), float(v[17])
    SSP.setdefault(Z, []).append((age, Mn, mlV))
for Z in SSP: SSP[Z] = np.array(sorted(SSP[Z]))
def ssp(Z, t):
    a = SSP[Z]; t = min(max(t, a[0, 0]), a[-1, 0]); lt = math.log10(t); la = np.log10(a[:, 0])
    Mn = float(np.interp(lt, la, a[:, 1])); ml = float(np.interp(lt, la, a[:, 2])); return Mn, Mn / ml
# ---- Weisz+14 SFHs (CFG824's reader)
def read_tsv(fn):
    L = [l.rstrip("\n") for l in open(fn) if not l.startswith("#") and l.strip()]
    hdr = L[0].split("\t"); return [dict(zip(hdr, [x.strip() for x in l.split("\t")])) for l in L[3:] if len(l.split("\t")) == len(hdr)]
def fgrid(r):
    fk = {float(k[1:]): fnum(v) for k, v in r.items() if k.startswith("f") and k[1:].replace(".", "").isdigit() and fnum(v) is not None}
    g = sorted(fk, reverse=True); return np.array(g), np.array([fk[x] for x in g])
def bins(r):
    g, f = fgrid(r); out = [(13.3, f[0])]
    for i in range(1, len(g)):
        dm = f[i] - f[i - 1]
        if dm > 0: out.append((10 ** (0.5 * (g[i - 1] + g[i])) / 1e9, dm))
    return out
def ups_sfh(B, Z):
    m = sum(dm * ssp(Z, t)[0] for t, dm in B); l = sum(dm * ssp(Z, t)[1] for t, dm in B); return m / l
NAMEMAP = {"Canes Venetici I": "Canes Venatici I", "Canes Venetici II": "Canes Venatici II", "DDO 210": "Aquarius",
           "Pegasus": "Pegasus dIrr", "Sag DIG": "Sagittarius dIrr", "M32": "M 32"}
T6 = {r["ID"]: r for r in read_tsv(os.path.join(WZ, "table6.tsv"))}
SFH = {}
for r in read_tsv(os.path.join(WZ, "table5.tsv")):
    if NAMEMAP.get(r["ID"], r["ID"]) in SFH: continue
    SFH[NAMEMAP.get(r["ID"], r["ID"])] = bins(T6.get(r["ID"], r))
R24 = json.load(open(os.path.join(LANES, "CFG824_dwarf_age_fossil", "cfg824_results.json")))["rows"]
LVD = {}
for fn in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(DS, fn))):
        LVD[r["name"]] = dict(MV=fnum(r.get("M_V")), rhl=fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical")))
def wolf(M, rhl): return math.sqrt(G * M * Msun / (6.0 * (4.0 / 3.0) * rhl * PC)) / 1e3
def nu(y): y = max(y, 1e-12); return 1.0 / (-math.expm1(-math.sqrt(y)))
def law(MV, rhl, a0, ups):
    M = ups * 10 ** (0.4 * (4.83 - MV)); y = G * (M / 2) * Msun / ((4 / 3) * rhl * PC) ** 2 / a0
    return wolf(M, rhl) * math.sqrt(nu(y))
rows = [dict(name=k, **v, **LVD[k]) for k, v in R24.items()]
OOS = [r for r in rows if not r["train"]]; TR = [r for r in rows if r["train"]]
wt = lambda S: np.array([1 / ((r["eso"] / r["so"]) ** 2 + (math.log(10) * WID / 2) ** 2) for r in S])
def fit(E, t, w):
    A = np.vstack([np.ones_like(t), t]).T; W = np.diag(w); cov = np.linalg.inv(A.T @ W @ A); return cov @ A.T @ W @ E, cov
P("CFG827 (= CFG824b)  age test with SFH-based M/L" + ("  [MUTATE]" if MUT else ""))
RES = dict(lane="CFG827", mutate=MUT, rows={})
if not MUT:
    # K1: an SFH entirely in the bin containing 12.59 Gyr
    Mn, L = ssp(-1.31, 12.5893); node = [x for x in SSP[-1.31] if abs(x[0] - 12.5893) < 1e-3][0]
    k1 = abs(Mn / L / node[2] - 1); P(f"  K1 SSP node 12.59 Gyr [M/H] -1.31: Ups {Mn / L:.4f} vs table {node[2]:.4f} -> {'PASS' if k1 < 0.05 else 'FAIL'}")
    P(f"\n  {'dwarf':18s} {'set':5s} {'tau90':>6s} {'Ups_SFH':>8s} (-1.71/-0.71)  {'law':>6s} {'E_SFH':>7s}  (E at Ups 2)")
    for Zc in (-1.31, -1.71, -0.71):
        for r in rows: r[f"U{Zc}"] = ups_sfh(SFH[r["name"]], Zc); r[f"E{Zc}"] = math.log(r["so"] / law(r["MV"], r["rhl"], A0["canonical"], r[f"U{Zc}"]))
    for r in sorted(rows, key=lambda r: (r["train"], -r["tau90"])):
        RES["rows"][r["name"]] = dict(train=r["train"], tau90=r["tau90"], ups=r["U-1.31"], ups_lo=r["U-1.71"], ups_hi=r["U-0.71"], E_SFH=r["E-1.31"], E_ups2=r["E"])
        P(f"  {r['name']:18s} {'TRAIN' if r['train'] else 'OOS':5s} {r['tau90']:6.2f} {r['U-1.31']:8.2f} ({r['U-1.71']:.2f}/{r['U-0.71']:.2f})  {law(r['MV'], r['rhl'], A0['canonical'], r['U-1.31']):6.2f} {r['E-1.31']:+7.2f}  ({r['E']:+.2f})")
    t = np.array([r["tau90"] for r in OOS]); w = wt(OOS); sc = {}
    for Zc in (-1.31, -1.71, -0.71):
        E = np.array([r[f"E{Zc}"] for r in OOS]); rho, p = spearmanr(E, t, alternative="greater"); _, pn = spearmanr(E, t, alternative="less"); ab, cov = fit(E, t, w)
        sc[Zc] = dict(rho=float(rho), p=float(p), p_less=float(pn), slope=float(ab[1]), slope_err=float(math.sqrt(cov[1, 1])), a=float(ab[0]))
        P(f"  [M/H] {Zc:+.2f}: OOS N {len(OOS)} rho {rho:+.2f} p(>0) {p:.3f} p(<0) {pn:.3f} slope {ab[1]:+.3f} +- {math.sqrt(cov[1, 1]):.3f}")
    # alt footing at the primary metallicity
    Ealt = np.array([math.log(r["so"] / law(r["MV"], r["rhl"], A0["alt"], r["U-1.31"])) for r in OOS]); ra, pa = spearmanr(Ealt, t, alternative="greater")
    P(f"  alt footing [M/H] -1.31: rho {ra:+.2f} p(>0) {pa:.3f}")
    Etr = np.array([r["E-1.31"] for r in TR]); rt, pt = spearmanr(Etr, [r["tau90"] for r in TR], alternative="greater")
    P(f"  TRAINING MW {len(TR)} (not a verdict): rho {rt:+.2f} p(>0) {pt:.3f}")
    s0 = sc[-1.31]
    cls = "NOT DIAGNOSTIC" if len(OOS) < 8 else ("SUPPORTS" if (s0["rho"] > 0 and s0["p"] < 0.05 and sc[-1.71]["p"] < 0.10 and sc[-0.71]["p"] < 0.10) else ("OPPOSITE" if (s0["rho"] < 0 and s0["p_less"] < 0.05) else "NO SIGNAL"))
    RES.update(scores={str(k): v for k, v in sc.items()}, alt=dict(rho=float(ra), p=float(pa)), training=dict(rho=float(rt), p=float(pt)), cls=cls)
    # CFG826 UFD re-check with Ups_SFH (13.3 Gyr burst)
    U26 = json.load(open(os.path.join(LANES, "CFG826_ufd_age_crosscheck", "cfg826_results.json")))["canonical|E|primary"]["rows"]
    Uu = ups_sfh([(13.3, 1.0)], -1.31); Eu = np.array([e + math.log(law(LVD[n]["MV"], LVD[n]["rhl"], A0["canonical"], 2.0) / law(LVD[n]["MV"], LVD[n]["rhl"], A0["canonical"], Uu)) for n, e in U26.items()])
    E0 = np.array([r["E-1.31"] for r in OOS]); ab, cov = fit(E0, t, w); sres = float(np.sqrt(np.mean((E0 - (ab[0] + ab[1] * t)) ** 2)))
    mp = float(ab[0] + ab[1] * 12.5); x = np.array([1, 12.5]); sp = math.sqrt(x @ cov @ x + sres ** 2 / len(Eu)); mo, so = float(Eu.mean()), float(Eu.std(ddof=1) / math.sqrt(len(Eu)))
    flat = float(np.sum(w * E0) / np.sum(w)); fse = float(np.std(E0, ddof=1) / math.sqrt(len(E0)))
    z = (mo - mp) / math.sqrt(so ** 2 + sp ** 2); zf = (mo - flat) / math.sqrt(so ** 2 + fse ** 2 + sres ** 2 / len(Eu))
    RES["ufd"] = dict(ups=Uu, E_obs=mo, se=so, E_pred=mp, se_pred=sp, z=z, flat=flat, z_flat=zf)
    P(f"\n  UFD re-check (Ups_SFH 13.3-Gyr burst = {Uu:.2f}; 7 binary-corrected): E_UFD {mo:+.3f} +- {so:.3f}  trend@12.5 {mp:+.3f} +- {sp:.3f}  z {z:+.2f}  | flat {flat:+.3f} z_flat {zf:+.2f}")
    P(f"\n  CLASS (canonical, out-of-sample, SFH M/L): {cls}")
else:
    U1 = ups_sfh([(1.0, 1.0)], -1.31); ups_all = [ups_sfh([(1.0, 1.0)], -1.31) for r in rows]
    P(f"  1-Gyr burst for every dwarf: Ups all = {U1:.3f} (table 1-Gyr {ssp(-1.31, 1.0)[0] / ssp(-1.31, 1.0)[1]:.3f}) -> bites: {max(ups_all) - min(ups_all) < 1e-9}")
    rng = np.random.default_rng(827); t = rng.permutation([r["tau90"] for r in OOS])
    E = np.array([math.log(r["so"] / law(r["MV"], r["rhl"], A0["canonical"], ups_sfh(SFH[r["name"]], -1.31))) for r in OOS]); rho, p = spearmanr(E, t, alternative="greater")
    c = "SUPPORTS" if (rho > 0 and p < 0.05) else "not SUPPORTS"; P(f"  shuffled tau90: rho {rho:+.2f} p {p:.3f} -> {c} (must be not SUPPORTS)")
    RES.update(burst_ups=U1, shuffle=dict(rho=float(rho), p=float(p), cls=c))
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg827_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg827{sfx}.out"), "w").write("\n".join(OUT) + "\n")
