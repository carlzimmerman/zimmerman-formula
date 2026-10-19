"""CFG857 -- size dependence of the extra speed V_x and the SPARC re-test.  Criteria: FROZEN_CRITERIA.md.
Run: python3 cfg857.py (CFG857_MUTATE=1).  kappa = 1/2 FITTED; not theory closed."""
import os, glob, csv, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG857_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, KPC, PC = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; R0 = 0.3
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
def sparc_D(a0, V0, beta):
    gal = []
    for fn in sorted(glob.glob(os.path.join(REPO, "real_research", "data", "sparc_data", "*_rotmod.dat"))):
        nm = os.path.basename(fn).replace("_rotmod.dat", ""); g = Q.get(nm)
        if not g or g["q"] > 2 or g["inc"] < 30 or g["Mb"] > 3e9: continue
        d_ = []
        for l in open(fn):
            if l.startswith("#") or not l.strip(): continue
            R, V, eV, Vg, Vd, Vb = [float(t) for t in l.split()[:6]]
            if V <= 0 or R <= 0 or eV / V >= 0.10: continue
            gbar = (Vg * abs(Vg) + 0.5 * Vd * abs(Vd) + 0.7 * Vb * abs(Vb)) * 1e6 / (R * KPC)
            if gbar <= 0: continue
            gl = float(gbar * nu(gbar / a0)); go = V * V * 1e6 / (R * KPC); gx = (V0 * 1e3) ** 2 * (R / R0) ** (2 * beta) / (R * KPC)
            d_.append(math.log10(go / gl) - math.log10((gl + gx) / gl))
        if d_: gal.append(float(np.median(d_)))
    D = np.array(gal); rng = np.random.default_rng(857); bs = [rng.choice(D, len(D)).mean() for _ in range(2000)]
    return float(D.mean()), float(np.std(bs)), len(D)
P("CFG857  size dependence of the extra speed V_x" + ("  [MUTATE r1/2 shuffled]" if MUT else ""))
RES = dict(lane="CFG857", mutate=MUT); rng = np.random.default_rng(857)
for foot in ("canonical", "alt"):
    a0 = A0[foot]; dw = []
    for r in R28[f"{foot}|nu_e"]["rows"]:
        if r["delta"] <= 0.05: continue
        L = LVD[r["name"]]; rhk = (4 / 3) * (fnum(L.get("rhalf_sph_physical")) or fnum(L.get("rhalf_physical"))) / 1000; rh = rhk * KPC
        Ms = R27[r["name"]]["ups"] * 10 ** (0.4 * (4.83 - fnum(L["M_V"]))); gb = G * (Ms / 2) * Msun / rh ** 2; gl = float(gb * nu(gb / a0))
        dw.append(dict(name=r["name"], host=L.get("host") or "field", lr=math.log10(rhk / R0), lV=0.5 * math.log10(gl * (10 ** r["delta"] - 1) * rh) - 3))
    lr = np.array([d["lr"] for d in dw]); lV = np.array([d["lV"] for d in dw]); m31 = np.array([1.0 if d["host"] == "m_031" else 0.0 for d in dw])
    if MUT: lr = rng.permutation(lr)
    def fit(idx, host=True):
        A = np.c_[np.ones(len(idx)), lr[idx], m31[idx]] if host else np.c_[np.ones(len(idx)), lr[idx]]
        return np.linalg.lstsq(A, lV[idx], rcond=None)[0]
    allidx = np.arange(len(dw)); fh = fit(allidx); f0 = fit(allidx, False)
    bh = np.array([fit(rng.integers(0, len(dw), len(dw))) for _ in range(2000)]); b0 = np.array([fit(rng.integers(0, len(dw), len(dw)), False) for _ in range(2000)])
    beta, sbeta = float(f0[1]), float(b0[:, 1].std()); c, sc = float(fh[2]), float(bh[:, 2].std()); beta_h, sbeta_h = float(fh[1]), float(bh[:, 1].std())
    V0 = 10 ** f0[0]; D, sD, NG = sparc_D(a0, V0, beta)
    sp = abs(D) < 0.05 and abs(D) <= 2 * sD; bsig = abs(beta) >= 2 * sbeta; off0 = abs(c) < 2 * sc
    cls = ("SIZE LAW WORKS" if (bsig and off0 and sp) else ("SIZE LAW FAILS SPARC" if (bsig and off0) else ("NO SIZE DEPENDENCE" if not bsig else "OFFSET REMAINS")))
    RES[foot] = dict(N=len(dw), beta=beta, sbeta=sbeta, V0=V0, beta_with_host=beta_h, sbeta_with_host=sbeta_h, host_offset=c, s_host=sc, sparc_D=D, sparc_sD=sD, sparc_N=NG, cls=cls)
    P(f"\n  [{foot}] N {len(dw)} dwarfs: log V_x = {f0[0]:.3f} + {beta:+.3f}(+-{sbeta:.3f}) log(r1/2/0.3 kpc)  -> V0 = {V0:.2f} km/s at 0.3 kpc")
    P(f"     with host term: beta {beta_h:+.3f} +- {sbeta_h:.3f}, M31 offset at fixed size c = {c:+.3f} +- {sc:.3f} dex ({c / sc:+.1f} sigma)")
    P(f"     SPARC re-test with V_x(r) = V0 (r/0.3 kpc)^beta: D = {D:+.3f} +- {sD:.3f} (N {NG})  -> {'pass' if sp else 'FAIL'}")
    P(f"     CLASS: {cls}")
if not MUT:
    Dk, sk, _ = sparc_D(A0["canonical"], 9.42, 0.0); P(f"\n  K1 beta=0, V0=9.42: SPARC D {Dk:+.3f} (CFG856 +0.017)")
RES["cls"] = RES["canonical"]["cls"]; P(f"\n  CLASS (canonical): {RES['cls']}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg857_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg857{sfx}.out"), "w").write("\n".join(OUT) + "\n")
