"""CFG826 -- does CFG824's age trend, extrapolated to tau90 = 12.5 Gyr, predict the UFD excess?  Criteria: FROZEN_CRITERIA.md (13399acac).
Run: python3 cfg826.py  (CFG826_MUTATE=1: slope b = 0).  kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG826_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, PC = 6.674e-11, 1.989e30, 3.0857e16; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; WID = 0.15
T90, T50 = 12.5, 12.6; UPS_ML = min(4.0, max(0.5, 2.0 * (T50 / 10.0) ** 0.7))
def fnum(x):
    try: return float(x)
    except: return None
def wolf(M, rhl): return math.sqrt(G * M * Msun / (6.0 * (4.0 / 3.0) * rhl * PC)) / 1e3
def nu(y): y = max(y, 1e-12); return 1.0 / (-math.expm1(-math.sqrt(y)))
def law(MV, rhl, a0, ups):
    M = ups * 10 ** (0.4 * (4.83 - MV)); y = G * (M / 2) * Msun / ((4 / 3) * rhl * PC) ** 2 / a0
    return wolf(M, rhl) * math.sqrt(nu(y))
R24 = json.load(open(os.path.join(LANES, "CFG824_dwarf_age_fossil", "cfg824_results.json")))
OOS = [dict(name=k, **v) for k, v in R24["rows"].items() if not v["train"]]
USED = {"Antlia II", "Canes Venatici I", "Carina", "Crater II", "Draco", "Fornax", "Leo I", "Leo II", "Sculptor", "Sextans", "Ursa Minor"} | set(R24["rows"])
def trend(key):
    t = np.array([r["tau90"] for r in OOS]); E = np.array([r[key] for r in OOS])
    w = np.array([1 / ((r["eso"] / r["so"]) ** 2 + (math.log(10) * WID / 2) ** 2) for r in OOS])
    A = np.vstack([np.ones_like(t), t]).T; W = np.diag(w); cov = np.linalg.inv(A.T @ W @ A); ab = cov @ A.T @ W @ E
    if MUT: ab = np.array([float(np.sum(w * E) / np.sum(w)), 0.0]); cov = np.diag([1 / np.sum(w), 0.0])
    res = E - A @ ab; s_res = float(np.sqrt(np.mean(res ** 2)))
    flat = float(np.sum(w * E) / np.sum(w)); flat_se = float(np.std(E, ddof=1) / math.sqrt(len(E)))
    return ab, cov, s_res, flat, flat_se
LVD = {r["name"]: r for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", "lvd_dwarf_mw.csv")))}
AMAP = {"Boo I": "Bootes I", "Car II": "Carina II", "Cra II": "Crater II", "Eri III": "Eridanus III", "Hyd I": "Hydrus I", "Leo IV": "Leo IV",
        "Leo V": "Leo V", "Ret II": "Reticulum II", "Sag II": "Sagittarius II", "Seg 1": "Segue 1", "Uni 1": "Unions 1", "Wil 1": "Willman 1"}
prim, drop = [], []
for l in open(os.path.join(REPO, "real_research", "data", "arroyopolonio2026_ufd_binary_corrected.tsv")):
    if l.startswith("#") or l.startswith("name"): continue
    v = l.rstrip("\n").split("\t"); nm = AMAP.get(v[0], v[0]); r = LVD.get(nm)
    if nm in USED: drop.append(f"{nm} (used in CFG821/824)"); continue
    if r is None or fnum(r.get("M_V")) is None or not (fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical"))): drop.append(f"{nm} (no LVD M_V/r_h)"); continue
    s, ep, em = float(v[11]), float(v[12]), float(v[14])
    prim.append(dict(name=nm, so=s, eso=0.5 * (ep + em), MV=fnum(r["M_V"]), rhl=fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical"))))
sec = []
for nm, r in LVD.items():
    MV, s_, es, rh = fnum(r.get("M_V")), fnum(r.get("vlos_sigma")), fnum(r.get("vlos_sigma_em")), fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical"))
    if MV is None or s_ is None or rh is None or MV <= -7.7 or nm in USED or nm in ("LMC", "SMC"): continue
    sec.append(dict(name=nm, so=s_, eso=es or 0.1 * s_, MV=MV, rhl=rh))
P(f"CFG826  UFD cross-check of the CFG824 age trend" + ("  [MUTATE b = 0]" if MUT else ""))
P(f"  primary (binary-corrected, Arroyo-Polonio+26) N {len(prim)}: {', '.join(r['name'] for r in prim)}")
P(f"  dropped: {', '.join(drop)}")
P(f"  secondary (LVD literature sigma, M_V > -7.7) N {len(sec)}")
RES = dict(lane="CFG826", mutate=MUT, dropped=drop)
for foot in ("canonical", "alt"):
    for key, ups, lab in (("E", 2.0, "primary Ups 2"), ("E_ML", UPS_ML, f"C-ML Ups {UPS_ML:.2f}")):
        if foot == "alt" and key == "E_ML": continue
        ab, cov, s_res, flat, flat_se = trend(key)
        for sname, S in (("primary", prim), ("secondary", sec)):
            E = np.array([math.log(r["so"] / law(r["MV"], r["rhl"], A0[foot], ups)) for r in S]); N = len(E)
            mo, so = float(E.mean()), float(E.std(ddof=1) / math.sqrt(N))
            xp = np.array([1.0, T90]); mp = float(xp @ ab); sp = float(math.sqrt(xp @ cov @ xp + s_res ** 2 / N))
            z = (mo - mp) / math.sqrt(so ** 2 + sp ** 2); zf = (mo - flat) / math.sqrt(so ** 2 + flat_se ** 2 + s_res ** 2 / N)
            cls = "NOT DIAGNOSTIC" if N < 4 else ("CONSISTENT" if abs(z) < 2 else ("UFDs ABOVE TREND" if z >= 2 else "UFDs BELOW TREND"))
            RES[f"{foot}|{key}|{sname}"] = dict(N=N, E_obs=mo, se_obs=so, E_pred=mp, se_pred=sp, z=z, flat=flat, z_flat=zf, slope=float(ab[1]), a=float(ab[0]), s_res=s_res, cls=cls,
                                                 rows={r["name"]: float(e) for r, e in zip(S, E)})
            P(f"  [{foot} | {lab} | {sname} N {N}] E_UFD {mo:+.3f} +- {so:.3f} (dex {mo / math.log(10):+.3f})  trend@12.5 {mp:+.3f} +- {sp:.3f}  z {z:+.2f}  | flat {flat:+.3f}  z_flat {zf:+.2f}  -> {cls}")
if not MUT:
    P("\n  primary UFD rows (E, canonical, Ups 2): " + ", ".join(f"{k} {v:+.2f}" for k, v in RES["canonical|E|primary"]["rows"].items()))
    k1 = abs(RES["canonical|E|primary"]["slope"] - R24["canonical"]["primary"]["slope"])
    P(f"  K1 refit slope {RES['canonical|E|primary']['slope']:.6f} vs CFG824 {R24['canonical']['primary']['slope']:.6f} -> {'PASS' if k1 < 1e-6 else 'FAIL'}")
RES["cls"] = RES["canonical|E|primary"]["cls"]; P(f"\n  CLASS (canonical, primary trend, binary-corrected UFDs): {RES['cls']}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg826_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg826{sfx}.out"), "w").write("\n".join(OUT) + "\n")
