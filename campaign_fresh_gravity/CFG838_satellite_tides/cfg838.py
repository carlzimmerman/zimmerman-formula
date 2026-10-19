"""CFG838 -- is the satellite-dwarf excess driven by host tides?  Criteria: FROZEN_CRITERIA.md (19d9754bb).
Run: python3 cfg838.py  (CFG838_MUTATE=1: injection + shuffle).  kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, numpy as np
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG838_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, PC, KPC, a0 = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19, 9.3603e-11
nu = lambda y: 1.0 / (-math.expm1(-math.sqrt(max(y, 1e-15))))
law = lambda gN: gN * nu(gN / a0)
def fnum(x):
    try: return float(x)
    except: return None
LVD = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f))):
        LVD[r["name"]] = dict(host=r.get("host", ""), D=fnum(r.get("distance_host")), MV=fnum(r.get("M_V")),
                              rh=fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical")))
rows28 = json.load(open(os.path.join(LANES, "CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")))["canonical|nu_e"]["rows"]
U27 = json.load(open(os.path.join(LANES, "CFG827_dwarf_age_sfh_ml", "cfg827_results.json")))["rows"]
def tide(nm, MM31):
    g = LVD[nm]; Mh = {"mw": 6.0e10, "m_031": MM31}.get(g["host"])
    if Mh is None or g["D"] is None or g["D"] != g["D"]: return None
    D = g["D"] * KPC; r12 = (4 / 3) * g["rh"] * PC; Ms = U27[nm]["ups"] * 10 ** (0.4 * (4.83 - g["MV"]))
    gh = lambda d: law(G * Mh * Msun / d ** 2); dgdD = abs(gh(D * 1.001) - gh(D * 0.999)) / (0.002 * D)
    gint_N = G * (Ms / 2) * Msun / r12 ** 2; gint = law(gint_N)
    return dict(T=dgdD * r12 / gint, efe=gh(D) / gint_N, D_kpc=g["D"], host=g["host"])
P("CFG838  satellite tides vs the dwarf excess" + ("  [MUTATE]" if MUT else ""))
RES = dict(lane="CFG838", mutate=MUT, rows={})
for MM31, lab in ((1.0e11, "primary (M31 1.0e11)"), (1.5e11, "bracket (M31 1.5e11)")):
    sat, field = [], []
    for r in rows28:
        t = tide(r["name"], MM31)
        (sat if t else field).append(dict(name=r["name"], delta=r["delta"], **(t or {})))
    lT = np.array([math.log10(s["T"]) for s in sat]); d = np.array([s["delta"] for s in sat])
    if MUT:
        rng = np.random.default_rng(838); dinj = 0.3 * lT + rng.normal(0, 0.1, len(lT))
        ri, pi = spearmanr(dinj, lT, alternative="greater"); rs, ps = spearmanr(d, rng.permutation(lT), alternative="greater")
        P(f"  [{lab}] injection rho {ri:+.2f} p {pi:.4f} -> {'TIDES IMPLICATED' if pi < 0.05 else 'not'} (must be IMPLICATED); shuffle rho {rs:+.2f} p {ps:.3f} -> {'IMPLICATED' if ps < 0.05 else 'not'} (must be not)")
        RES[lab] = dict(inj=(float(ri), float(pi)), shuf=(float(rs), float(ps))); continue
    rho, p = spearmanr(d, lT, alternative="greater"); _, pn = spearmanr(d, lT, alternative="less")
    re_, pe = spearmanr(d, [math.log10(s["efe"]) for s in sat], alternative="greater")
    rD, pD = spearmanr(d, [s["D_kpc"] for s in sat])
    RES[lab] = dict(N=len(sat), rho=float(rho), p=float(p), p_less=float(pn), rho_efe=float(re_), p_efe=float(pe), rho_D=float(rD), p_D=float(pD))
    P(f"\n  [{lab}] satellites N {len(sat)}: rho(Delta, log T) {rho:+.2f}  p(>0) {p:.3f}  p(<0) {pn:.3f} | rho(Delta, log g_host/g_int,N) {re_:+.2f} p {pe:.3f} | rho(Delta, D) {rD:+.2f} (two-sided p {pD:.3f})")
    if MM31 == 1.0e11:
        P(f"    {'dwarf':18s} host   D_kpc   log T   log efe   Delta")
        for s in sorted(sat, key=lambda s: s["T"]):
            RES["rows"][s["name"]] = dict(host=s["host"], D=s["D_kpc"], logT=math.log10(s["T"]), logefe=math.log10(s["efe"]), delta=s["delta"])
            P(f"    {s['name']:18s} {s['host']:5s} {s['D_kpc']:7.1f} {math.log10(s['T']):7.2f} {math.log10(s['efe']):8.2f} {s['delta']:+7.2f}")
        P(f"    field ({len(field)}): " + ", ".join(f"{f['name']} {f['delta']:+.2f}" for f in field) + "   (gas-free field dSphs: Cetus, Tucana)")
        RES["field"] = {f["name"]: f["delta"] for f in field}
        dr = [s for s in sat if s["name"] == "Draco"][0]; P(f"    K1 Draco: D {dr['D_kpc']:.1f} kpc, log T {math.log10(dr['T']):.2f}, log g_host/g_int,N {math.log10(dr['efe']):.2f}")
if not MUT:
    pr, br = RES["primary (M31 1.0e11)"], RES["bracket (M31 1.5e11)"]
    cls = "TIDES IMPLICATED" if (pr["N"] >= 15 and pr["rho"] > 0 and pr["p"] < 0.05 and br["p"] < 0.10) else ("OPPOSITE" if (pr["rho"] < 0 and pr["p_less"] < 0.05) else "NO TIDAL SIGNAL")
    RES["cls"] = cls; P(f"\n  CLASS: {cls}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg838_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg838{sfx}.out"), "w").write("\n".join(OUT) + "\n")
