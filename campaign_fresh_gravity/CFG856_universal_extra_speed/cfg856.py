"""CFG856 -- universal extra circular speed V_x on top of the law.  Criteria: FROZEN_CRITERIA.md (e7b1ea0e3).
Run: python3 cfg856.py (CFG856_MUTATE=1: V_x x 3).  kappa = 1/2 FITTED; not theory closed."""
import os, glob, csv, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG856_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, KPC, PC = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
nu = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
def fnum(x):
    try: return float(x)
    except: return None
LVD = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f))): LVD[r["name"]] = r
R27 = json.load(open(os.path.join(LANES, "CFG827_dwarf_age_sfh_ml", "cfg827_results.json")))["rows"]
R28 = json.load(open(os.path.join(LANES, "CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")))
Q = {}
for l in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    v = l.split()
    if len(v) >= 18 and v[1].isdigit():
        try: Q[v[0]] = dict(inc=float(v[5]), q=int(v[17]), Mb=(0.5 * float(v[7]) + 1.33 * float(v[13])) * 1e9)
        except ValueError: pass
P("CFG856  universal extra circular speed V_x on top of the law" + ("  [MUTATE V_x x3]" if MUT else ""))
RES = dict(lane="CFG856", mutate=MUT)
for foot in ("canonical", "alt"):
    a0 = A0[foot]; rows = R28[f"{foot}|nu_e"]["rows"]; dw = []
    for r in rows:
        if r["delta"] <= 0.05: continue
        L = LVD[r["name"]]; rh = (4 / 3) * (fnum(L.get("rhalf_sph_physical")) or fnum(L.get("rhalf_physical"))) * PC
        Ms = R27[r["name"]]["ups"] * 10 ** (0.4 * (4.83 - fnum(L["M_V"]))); gb = G * (Ms / 2) * Msun / rh ** 2; gl = float(gb * nu(gb / a0))
        dw.append(dict(name=r["name"], host=L.get("host") or "field", lMs=math.log10(Ms), lVx=0.5 * math.log10(gl * (10 ** r["delta"] - 1) * rh) - 3))
    mw = np.array([d["lVx"] for d in dw if d["host"] == "mw"]); m31 = np.array([d["lVx"] for d in dw if d["host"] == "m_031"]); fld = np.array([d["lVx"] for d in dw if d["host"] == "field"])
    lV0 = float(mw.mean()); sV0 = float(mw.std(ddof=1) / math.sqrt(len(mw))); Vx = 10 ** lV0 * (3 if MUT else 1)
    # P3 SPARC
    gal = []
    for fn in sorted(glob.glob(os.path.join(REPO, "real_research", "data", "sparc_data", "*_rotmod.dat"))):
        nm = os.path.basename(fn).replace("_rotmod.dat", ""); g = Q.get(nm)
        if not g or g["q"] > 2 or g["inc"] < 30 or g["Mb"] > 3e9: continue
        d_, o_ = [], []
        for l in open(fn):
            if l.startswith("#") or not l.strip(): continue
            R, V, eV, Vg, Vd, Vb = [float(t) for t in l.split()[:6]]
            if V <= 0 or R <= 0 or eV / V >= 0.10: continue
            gbar = (Vg * abs(Vg) + 0.5 * Vd * abs(Vd) + 0.7 * Vb * abs(Vb)) * 1e6 / (R * KPC)
            if gbar <= 0: continue
            gl = float(gbar * nu(gbar / a0)); go = V * V * 1e6 / (R * KPC); gx = (Vx * 1e3) ** 2 / (R * KPC)
            o = math.log10(go / gl); p = math.log10((gl + gx) / gl); d_.append(o - p); o_.append(o)
        if d_: gal.append(dict(name=nm, d=float(np.median(d_)), obs=float(np.median(o_))))
    D = np.array([x["d"] for x in gal]); rng = np.random.default_rng(856); bs = [rng.choice(D, len(D)).mean() for _ in range(2000)]
    mD, sD = float(D.mean()), float(np.std(bs)); D0 = float(np.mean([x["obs"] for x in gal]))
    p3 = abs(mD) < 0.05 and abs(mD) <= 2 * sD; excl = (mD <= -0.05 and mD / sD <= -3)
    z1 = (m31.mean() - lV0) / math.hypot(sV0, m31.std(ddof=1) / math.sqrt(len(m31))); p1 = abs(z1) < 2
    lM = np.array([d["lMs"] for d in dw]); lv = np.array([d["lVx"] for d in dw]); cf, cov = np.polyfit(lM, lv, 1, cov=True); sl, ssl = float(cf[0]), float(math.sqrt(cov[0, 0]))
    p2 = abs(sl) < 0.15 or abs(sl) <= 2 * ssl
    cls = ("UNIVERSAL V_x SUPPORTED" if (p3 and p1 and p2) else ("SPARC-COMPATIBLE ONLY" if p3 else ("EXCLUDED BY SPARC" if excl else "OTHER")))
    RES[foot] = dict(Vx0_kms=10 ** lV0, lV0=lV0, sV0=sV0, N_mw=len(mw), m31_mean=float(m31.mean()), z_m31=float(z1), field_mean=float(fld.mean()) if len(fld) else None,
                     slope_M=sl, slope_err=ssl, sparc_N=len(gal), D=mD, sD=sD, D_law_only=D0, P1=p1, P2=p2, P3=p3, cls=cls)
    P(f"\n  [{foot}] V_x0 (MW, N {len(mw)}) = {10 ** lV0:.2f} km/s (log {lV0:.3f} +- {sV0:.3f}); M31 mean {10 ** m31.mean():.2f} km/s (z {z1:+.1f}); field mean {10 ** fld.mean():.2f} km/s")
    P(f"     universality: slope of log V_x on log M* = {sl:+.3f} +- {ssl:.3f}   -> P2 {'pass' if p2 else 'FAIL'};  P1 {'pass' if p1 else 'FAIL'}")
    P(f"     P3 SPARC dwarfs (N {len(gal)}): law alone residual {D0:+.3f};  with V_x: D = obs - pred = {mD:+.3f} +- {sD:.3f}  -> {'pass' if p3 else 'FAIL'}")
    P(f"     CLASS: {cls}")
RES["cls"] = RES["canonical"]["cls"]
if not MUT: P(f"\n  K1 (V_x = 0) law-only SPARC residual {RES['canonical']['D_law_only']:+.3f} vs CFG845 +0.032")
P(f"\n  CLASS (canonical): {RES['cls']}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg856_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg856{sfx}.out"), "w").write("\n".join(OUT) + "\n")
