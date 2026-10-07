#!/usr/bin/env python3
"""Session 3, test T (FROZEN_CRITERIA.md): are the UFD law offsets tidal at pericentre in the law's own MW?
Run: python3 tidal_ufd.py [--mutate] -> tidal_ufd[_MUTATE].out / _results.json"""
import os, sys, csv, math, json, warnings
import numpy as np
from scipy.optimize import brentq
from scipy.stats import spearmanr
import astropy.units as u
from astropy.coordinates import SkyCoord, Galactocentric, CartesianRepresentation
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""): print(s); OUT.append(str(s))
Gk = 4.30091e-6                       # kpc (km/s)^2 / Msun
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
A0K = {k: v * 3.0857e19 / 1e6 for k, v in A0.items()}   # (km/s)^2 / kpc
MMW, AH = 6e10, 3.0
G, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
def nu_exp(y): y = np.maximum(y, 1e-12); return 1 / (1 - np.exp(-np.sqrt(y)))
def fnum(v):
    try: x = float(v); return x if np.isfinite(x) else None
    except (TypeError, ValueError): return None
rows = list(csv.DictReader(open(os.path.join(REPO, "real_research/data/dsph/lvd_dwarf_mw.csv"))))
RES = []
for r in rows:
    MV = fnum(r["M_V"]); sig = fnum(r["vlos_sigma"]); ul = fnum(r["vlos_sigma_ul"])
    rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"]); Dh = fnum(r["distance_host"]) or fnum(r["distance_gc"])
    if MV is None or MV <= -7.7 or rh is None or Dh is None: continue
    if not (sig is not None and ul is None and sig > 0): continue
    RES.append(dict(name=r["name"], LV=10 ** (0.4 * (4.83 - MV)), rh=rh, sig=sig,
                    MHI=(10 ** fnum(r["mass_HI"]) if fnum(r["mass_HI"]) is not None else 0.0),
                    ra=fnum(r["ra"]), dec=fnum(r["dec"]), D=fnum(r["distance"]), eD=fnum(r["distance_em"]) or 0.05 * (fnum(r["distance"]) or 1),
                    vl=fnum(r["vlos_systemic"]), evl=fnum(r["vlos_systemic_em"]) or 1.0,
                    pa=fnum(r["pmra"]), epa=fnum(r["pmra_em"]) or 0.05, pd=fnum(r["pmdec"]), epd=fnum(r["pmdec_em"]) or 0.05, Dgc=fnum(r["distance_gc"])))
checks = {}
P("Session 3 T: UFD law offsets vs tidal susceptibility at pericentre (law's own MW)" + (" [MUTATE]" if MUT else ""))
# ---- host
RG = np.geomspace(0.01, 3000, 6000)
def g_host(r, foot):
    gN = Gk * MMW / (r + AH) ** 2
    return nu_exp(gN / A0K[foot]) * gN
PHI = {}
for f in A0:
    gg = g_host(RG, f)
    cum = np.concatenate([[0], np.cumsum(0.5 * (gg[1:] + gg[:-1]) * np.diff(RG))])
    PHI[f] = cum - cum[-1]                     # Phi(r) = -int_r^Rmax g
phi = lambda r, f: np.interp(r, RG, PHI[f])
gc = Galactocentric()
sun = SkyCoord(x=0 * u.kpc, y=0 * u.kpc, z=0 * u.kpc, frame="icrs", representation_type="cartesian") if False else None
k1 = abs(np.hypot(gc.galcen_distance.to_value(u.kpc), gc.z_sun.to_value(u.kpc)) - gc.galcen_distance.to_value(u.kpc)) < 1e-3
checks["K1_galcen_R0"] = bool(k1)
gd = math.sqrt(Gk * MMW * A0K["canonical"]) / (50 + AH)
checks["K2_deep_host"] = bool(abs(g_host(np.array([50.0]), "canonical")[0] / gd - 1) < 0.03)
# K2b (added AFTER the first run, disclosed): K2's premise was wrong (the MW at 50 kpc has y = 0.032, not deep), so check the formula
# independently by hand: g = gN / (1 - exp(-sqrt(gN/a0))) with gN = G M/(r+a)^2 -> 562.4019 (km/s)^2/kpc at 50 kpc, canonical
_gN = Gk * MMW / 53.0 ** 2
checks["K2b_hand_formula_POSTRUN"] = bool(abs(g_host(np.array([50.0]), "canonical")[0] / (_gN / (1 - math.exp(-math.sqrt(_gN / A0K["canonical"])))) - 1) < 1e-9)
def peri(rn, vr2, L, f):
    E = 0.5 * vr2 + phi(rn, f)
    F = lambda r: 2 * (E - phi(r, f)) - L ** 2 / r ** 2
    if F(rn) < 0: return rn
    lo = 0.011
    return rn if F(lo) > 0 else brentq(F, lo, rn, xtol=1e-5)
vc = math.sqrt(g_host(np.array([60.0]), "canonical")[0] * 60.0)
checks["K3_circular"] = bool(abs(peri(60.0, vc ** 2, 60.0 * vc, "canonical") / 60.0 - 1) < 1e-4)
P(f"K2b (post-run) hand formula {checks['K2b_hand_formula_POSTRUN']}")
P(f"K1 {checks['K1_galcen_R0']}  K2 g(50)/deep {g_host(np.array([50.0]),'canonical')[0]/gd:.4f} -> {checks['K2_deep_host']}  K3 {checks['K3_circular']}")
# ---- pericentres
rng = np.random.default_rng(9)
have = [d for d in RES if None not in (d["pa"], d["pd"], d["vl"], d["D"])]
P(f"objects with full phase space: {len(have)}/{len(RES)}; missing: {', '.join(d['name'] for d in RES if d not in have) or 'none'}")
for d in have:
    n = 300
    D = np.clip(d["D"] + rng.normal(0, d["eD"], n), 1, None)
    c = SkyCoord(ra=np.full(n, d["ra"]) * u.deg, dec=np.full(n, d["dec"]) * u.deg, distance=D * u.kpc,
                 pm_ra_cosdec=(d["pa"] + rng.normal(0, d["epa"], n)) * u.mas / u.yr, pm_dec=(d["pd"] + rng.normal(0, d["epd"], n)) * u.mas / u.yr,
                 radial_velocity=(d["vl"] + rng.normal(0, d["evl"], n)) * u.km / u.s).transform_to(gc)
    x = np.vstack([c.x.to_value(u.kpc), c.y.to_value(u.kpc), c.z.to_value(u.kpc)]).T
    v = np.vstack([c.v_x.to_value(u.km / u.s), c.v_y.to_value(u.km / u.s), c.v_z.to_value(u.km / u.s)]).T
    rn = np.linalg.norm(x, axis=1); L = np.linalg.norm(np.cross(x, v), axis=1); v2 = (v ** 2).sum(1)
    d["rnow"] = float(np.median(rn))
    for f in A0:
        d["rp_" + f] = float(np.median([peri(rn[i], v2[i], L[i], f) for i in range(n)]))
# ---- offsets and tau
def g_int(d, f):
    Mb = 2 * d["LV"] + 1.33 * d["MHI"]; r = 4 / 3 * d["rh"] * PC
    gN = G * 0.5 * Mb * MSUN / r ** 2; return float(nu_exp(gN / A0[f]) * gN), r
def tidal(d, f, rr):
    gh = g_host(np.array([rr]), f)[0]; eps = 1e-3
    dl = (math.log(g_host(np.array([rr * (1 + eps)]), f)[0]) - math.log(g_host(np.array([rr * (1 - eps)]), f)[0])) / (2 * eps)
    t = (gh / rr) * (1 - dl) * (4 / 3 * d["rh"] / 1e3)            # (km/s)^2/kpc
    return t * 1e6 / 3.0857e19                                      # -> m/s^2
res = {}
for f in A0:
    for where in ("peri", "now"):
        off, lt = [], []
        for d in have:
            gi, r = g_int(d, f)
            sp = math.sqrt(gi * r / 3) / 1e3
            off.append(math.log10(d["sig"] / sp))
            rr = d["rp_" + f] if where == "peri" else d["rnow"]
            lt.append(math.log10(tidal(d, f, rr) / gi))
        off, lt = np.array(off), np.array(lt)
        if MUT: off = np.random.default_rng(13).permutation(off)
        rho, p = spearmanr(off, lt)
        lo = lt <= np.median(lt)
        mlo, mhi = float(np.median(off[lo])), float(np.median(off[~lo]))
        if mlo > 3 * 0.086: v = "NOT TIDAL"
        elif rho > 0 and p < 0.01 and abs(mlo) < 2 * 0.086: v = "TIDES-DRIVEN"
        else: v = "INCONCLUSIVE"
        res[f"{f}|{where}"] = dict(rho=float(rho), p=float(p), med_low_tau=mlo, med_high_tau=mhi, verdict=v, logtau_range=[float(lt.min()), float(lt.max())])
        P(f"{f:9s} {where:4s}: rho {rho:+.2f} (p {p:.3f}); low-tau half offset {mlo:+.3f}, high-tau half {mhi:+.3f}; log tau {lt.min():+.1f}..{lt.max():+.1f} -> {v}")
P("\nper object (canonical): name | r_now | r_peri | log tau_peri | offset")
for d in sorted(have, key=lambda d: d["rp_canonical"]):
    gi, r = g_int(d, "canonical"); sp = math.sqrt(gi * r / 3) / 1e3
    P(f"  {d['name']:20s} {d['rnow']:6.1f} {d['rp_canonical']:6.1f}  {math.log10(tidal(d,'canonical',d['rp_canonical'])/gi):+6.2f}  {math.log10(d['sig']/sp):+.3f}")
rc = 0 if all(checks.values()) else 1   # K2 fails as frozen (mis-specified control, see K2b) -> main run exits 1; disclosed
if MUT:
    m = abs(res["canonical|peri"]["rho"])
    main = json.load(open(os.path.join(HERE, "tidal_ufd_results.json")))
    P(f"MUTATE: shuffled |rho| {m:.2f}; main rho {main['res']['canonical|peri']['rho']:+.2f}" + ("  (main |rho| < 0.3: MUTATE uninformative)" if abs(main['res']['canonical|peri']['rho']) < 0.3 else ""))
    rc = 1 if m < 0.3 else 0
json.dump(dict(checks=checks, res=res, objects=[{k: d[k] for k in ("name", "rnow", "rp_canonical", "rp_alt")} for d in have]),
          open(os.path.join(HERE, f"tidal_ufd{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"tidal_ufd{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(rc)
