"""CFG839 -- does the satellite excess track past tidal stress (pericentre in the framework's own MW field)?
Criteria: FROZEN_CRITERIA.md (288ab33eb).  Run: python3 cfg839.py (CFG839_MUTATE=1).  kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, numpy as np
from scipy.stats import spearmanr
from scipy.optimize import brentq
from scipy.integrate import quad
import astropy.units as u
import astropy.coordinates as coord
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG839_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, PC, KPC, a0, GYR = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19, 9.3603e-11, 3.156e16
nu = lambda y: 1.0 / (-math.expm1(-math.sqrt(max(y, 1e-15))))
law = lambda gN: gN * nu(gN / a0)
def fnum(x):
    try: return float(x)
    except: return None
LVD = {r["name"]: r for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", "lvd_dwarf_mw.csv")))}
rows28 = json.load(open(os.path.join(LANES, "CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")))["canonical|nu_e"]["rows"]
U27 = json.load(open(os.path.join(LANES, "CFG827_dwarf_age_sfh_ml", "cfg827_results.json")))["rows"]
def orbit(r, Mmw):
    c = coord.SkyCoord(ra=float(r["ra"]) * u.deg, dec=float(r["dec"]) * u.deg, distance=float(r["distance"]) * u.kpc,
                       pm_ra_cosdec=float(r["pmra"]) * u.mas / u.yr, pm_dec=float(r["pmdec"]) * u.mas / u.yr,
                       radial_velocity=float(r["vlos_systemic"]) * u.km / u.s).transform_to(coord.Galactocentric())
    x = np.array([c.x.to(u.m).value, c.y.to(u.m).value, c.z.to(u.m).value]); v = np.array([c.v_x.to(u.m / u.s).value, c.v_y.to(u.m / u.s).value, c.v_z.to(u.m / u.s).value])
    gf = lambda rr: law(G * Mmw * Msun / rr ** 2)
    rn = float(np.linalg.norm(x)); Lz = float(np.linalg.norm(np.cross(x, v))); E0 = 0.5 * float(v @ v)
    Phi = lambda rr: quad(gf, rn, rr, limit=200)[0]                       # Phi(rn) = 0
    f = lambda rr: 2 * (E0 - Phi(rr)) - Lz ** 2 / rr ** 2
    rp = brentq(f, 1e-3 * rn, rn * (1 - 1e-9)) if f(rn * (1 - 1e-9)) > 0 else rn
    hi = rn * 1.0001
    while f(hi) > 0: hi *= 1.5
    ra_ = brentq(f, rn * (1 + 1e-9), hi) if f(rn * (1 + 1e-9)) > 0 else rn
    Tr = 2 * quad(lambda rr: 1 / math.sqrt(max(f(rr), 1e-30)), rp * (1 + 1e-6), ra_ * (1 - 1e-6), limit=200)[0] if ra_ > rp * 1.001 else float("nan")
    return dict(x=x, v=v, rnow=rn / KPC, rp=rp / KPC, ra=ra_ / KPC, Tr_Gyr=Tr / GYR, gf=gf)
def leapfrog_check(o, Gyr=5.0, n=200000):
    x, v = o["x"].copy(), o["v"].copy(); dt = -Gyr * GYR / n; rmin = rmax = np.linalg.norm(x)
    acc = lambda x: -o["gf"](np.linalg.norm(x)) * x / np.linalg.norm(x)
    a = acc(x)
    for _ in range(n):
        v += 0.5 * dt * a; x += dt * v; a = acc(x); v += 0.5 * dt * a; rr = np.linalg.norm(x); rmin, rmax = min(rmin, rr), max(rmax, rr)
    return rmin / KPC, rmax / KPC
P("CFG839  pericentre tides in the framework's MW field" + ("  [MUTATE]" if MUT else ""))
RES = dict(lane="CFG839", mutate=MUT, rows={})
for Mmw, lab in ((6.0e10, "primary (M_MW 6e10)"), (8.0e10, "bracket (M_MW 8e10)")):
    S = []
    for r in rows28:
        L = LVD.get(r["name"])
        if L is None or L.get("host") != "mw" or not all(fnum(L.get(k)) is not None for k in ("pmra", "pmdec", "vlos_systemic", "distance")): continue
        o = orbit(L, Mmw); rh = fnum(L.get("rhalf_sph_physical")) or fnum(L.get("rhalf_physical")); r12 = (4 / 3) * rh * PC
        Ms = U27[r["name"]]["ups"] * 10 ** (0.4 * (4.83 - fnum(L["M_V"]))); gint = law(G * (Ms / 2) * Msun / r12 ** 2)
        rp = o["rp"] * KPC; dg = abs(o["gf"](rp * 1.001) - o["gf"](rp * 0.999)) / (0.002 * rp); Tp = dg * r12 / gint
        npass = 10.0 / o["Tr_Gyr"] if o["Tr_Gyr"] == o["Tr_Gyr"] else 0.0
        S.append(dict(name=r["name"], delta=r["delta"], rnow=o["rnow"], rp=o["rp"], ra=o["ra"], Tr=o["Tr_Gyr"], logTp=math.log10(Tp), npass=npass, logS=math.log10(max(npass * Tp, 1e-30)), _o=o))
    lT = np.array([s["logTp"] for s in S]); d = np.array([s["delta"] for s in S])
    if MUT:
        rng = np.random.default_rng(839); di = 0.3 * lT + rng.normal(0, 0.1, len(lT))
        ri, pi = spearmanr(di, lT, alternative="greater"); rs, ps = spearmanr(d, rng.permutation(lT), alternative="greater")
        P(f"  [{lab}] injection rho {ri:+.2f} p {pi:.4f} -> {'IMPLICATED' if pi < 0.05 else 'not'} (must be IMPLICATED); shuffle rho {rs:+.2f} p {ps:.3f} -> {'IMPLICATED' if ps < 0.05 else 'not'} (must be not)")
        RES[lab] = dict(inj=[float(ri), float(pi)], shuf=[float(rs), float(ps)]); continue
    rho, p = spearmanr(d, lT, alternative="greater"); _, pn = spearmanr(d, lT, alternative="less")
    rS, pS = spearmanr(d, [s["logS"] for s in S], alternative="greater"); rP, pP = spearmanr(d, [s["rp"] for s in S])
    RES[lab] = dict(N=len(S), rho=float(rho), p=float(p), p_less=float(pn), rho_S=float(rS), p_S=float(pS), rho_rp=float(rP), p_rp=float(pP))
    P(f"\n  [{lab}] N {len(S)}: rho(Delta, log T_peri) {rho:+.2f} p(>0) {p:.3f} p(<0) {pn:.3f} | rho(Delta, log S) {rS:+.2f} p {pS:.3f} | rho(Delta, r_peri) {rP:+.2f} (two-sided p {pP:.3f})")
    if Mmw == 6.0e10:
        P(f"    {'dwarf':18s} r_now  r_peri  r_apo  T_r(Gyr)  log T_peri  n_peri(10Gyr)  Delta")
        for s in sorted(S, key=lambda s: s["logTp"]):
            RES["rows"][s["name"]] = {k: v for k, v in s.items() if k != "_o"}
            P(f"    {s['name']:18s} {s['rnow']:6.1f} {s['rp']:6.1f} {s['ra']:7.1f} {s['Tr']:7.2f} {s['logTp']:10.2f} {s['npass']:10.1f}   {s['delta']:+.2f}")
        dr = [s for s in S if s["name"] == "Draco"][0]; lm = leapfrog_check(dr["_o"])
        ok = abs(lm[0] / dr["rp"] - 1) < 0.02 and abs(lm[1] / dr["ra"] - 1) < 0.02
        P(f"    K1 Draco turning points r_peri {dr['rp']:.1f} r_apo {dr['ra']:.1f} vs 5-Gyr leapfrog {lm[0]:.1f} / {lm[1]:.1f} -> {'PASS' if ok else 'FAIL'}")
        RES["k1"] = dict(rp=dr["rp"], ra=dr["ra"], leap=lm, ok=ok)
if not MUT:
    pr, br = RES["primary (M_MW 6e10)"], RES["bracket (M_MW 8e10)"]
    cls = "PAST TIDES IMPLICATED" if (pr["N"] >= 10 and pr["rho"] > 0 and pr["p"] < 0.05 and br["p"] < 0.10) else ("OPPOSITE" if (pr["rho"] < 0 and pr["p_less"] < 0.05) else "NO SIGNAL")
    RES["cls"] = cls; P(f"\n  CLASS: {cls}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg839_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg839{sfx}.out"), "w").write("\n".join(OUT) + "\n")
