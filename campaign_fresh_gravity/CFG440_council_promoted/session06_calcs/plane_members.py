#!/usr/bin/env python3
"""Session 6, P: VPOS members vs non-members under the law. Run: python3 plane_members.py [--mutate]"""
import os, sys, csv, json, math, warnings
import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord, Galactocentric
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""): print(s); OUT.append(str(s))
G, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
def nu(y): y = max(y, 1e-12); return 1 / (1 - math.exp(-math.sqrt(y)))
def fnum(v):
    try: x = float(v); return x if np.isfinite(x) else None
    except (TypeError, ValueError): return None
lv, bv = math.radians(169.3), math.radians(-2.8)
NRM = np.array([math.cos(bv) * math.cos(lv), math.cos(bv) * math.sin(lv), math.sin(bv)])
objs = []
for r in csv.DictReader(open(os.path.join(REPO, "real_research/data/dsph/lvd_dwarf_mw.csv"))):
    MV, sig, ul = fnum(r["M_V"]), fnum(r["vlos_sigma"]), fnum(r["vlos_sigma_ul"])
    rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"]); Dh = fnum(r["distance_host"]) or fnum(r["distance_gc"])
    if None in (MV, sig, rh) or ul is not None or r["name"] in ("Large Magellanic Cloud", "Small Magellanic Cloud", "LMC", "SMC"): continue
    if MV > -7.7 and Dh is None: continue
    ph = [fnum(r[k]) for k in ("ra", "dec", "distance", "vlos_systemic", "pmra", "pmdec")]
    if None in ph: continue
    objs.append(dict(name=r["name"], pop="UFD" if MV > -7.7 else "classical", LV=10 ** (0.4 * (4.83 - MV)), rh=rh, sig=sig,
                     MHI=(10 ** fnum(r["mass_HI"]) if fnum(r["mass_HI"]) is not None else 0.0), ph=ph,
                     e=[fnum(r["distance_em"]) or 0.05 * ph[2], fnum(r["vlos_systemic_em"]) or 1.0, fnum(r["pmra_em"]) or 0.05, fnum(r["pmdec_em"]) or 0.05]))
gc = Galactocentric(); rng = np.random.default_rng(41)
for d in objs:
    n = 300; ra, dec, D, vl, pa, pd = d["ph"]
    c = SkyCoord(ra=np.full(n, ra) * u.deg, dec=np.full(n, dec) * u.deg, distance=np.clip(D + rng.normal(0, d["e"][0], n), 1, None) * u.kpc,
                 pm_ra_cosdec=(pa + rng.normal(0, d["e"][2], n)) * u.mas / u.yr, pm_dec=(pd + rng.normal(0, d["e"][3], n)) * u.mas / u.yr,
                 radial_velocity=(vl + rng.normal(0, d["e"][1], n)) * u.km / u.s).transform_to(gc)
    x = np.vstack([c.x.value, c.y.value, c.z.value]).T; v = np.vstack([c.v_x.value, c.v_y.value, c.v_z.value]).T
    L = np.cross(x, v); L /= np.linalg.norm(L, axis=1)[:, None]; cs = L @ NRM
    d["mem_any"] = float((np.abs(cs) > math.cos(math.radians(30))).mean()) >= 0.5
    d["mem_co"] = float((cs > math.cos(math.radians(30))).mean()) >= 0.5
res = {}
for foot, a0 in A0.items():
    for d in objs:
        Mb = 2 * d["LV"] + 1.33 * d["MHI"]; r = 4 / 3 * d["rh"] * PC; gN = G * 0.5 * Mb * MSUN / r ** 2
        d["off"] = math.log10(d["sig"] / (math.sqrt(nu(gN / a0) * gN * r / 3) / 1e3))
        d["nu"] = nu(gN / a0)
    for key in ("mem_any", "mem_co"):
        rows = []
        for pop in ("UFD", "classical"):
            g = [d for d in objs if d["pop"] == pop]; med = np.median([d["off"] for d in g])
            for d in g:
                o = d["off"] - (0.5 * math.log10(d["nu"]) if (MUT and d[key]) else 0.0)
                rows.append((o - med, d[key], pop))
        x = np.array([q[0] for q in rows]); m = np.array([q[1] for q in rows])
        dl = float(np.median(x[m]) - np.median(x[~m])) if m.any() and (~m).any() else float("nan")
        b = np.random.default_rng(43); bs = []
        for _ in range(2000):
            i = b.integers(0, len(x), len(x)); mm = m[i]
            if mm.any() and (~mm).any(): bs.append(np.median(x[i][mm]) - np.median(x[i][~mm]))
        sd = float(np.std(bs))
        v = "TDG-ORIGIN SUPPORTED" if (dl < -0.2 and dl / sd < -3) else "DISFAVOURED" if dl - 2 * sd > -0.2 else "NON-DISCRIMINATING"
        res[f"{foot}|{key}"] = dict(delta=dl, sd=sd, n_mem=int(m.sum()), n_non=int((~m).sum()), verdict=v)
        P(f"{foot:9s} {key}: members {m.sum()} / non {(~m).sum()}: Delta {dl:+.3f} +- {sd:.3f} -> {v}")
P("members (any sense): " + ", ".join(f"{d['name']}({d['pop'][0]})" for d in objs if d["mem_any"]))
json.dump(res, open(os.path.join(HERE, f"plane_members{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"plane_members{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit((1 if res["canonical|mem_any"]["verdict"] == "TDG-ORIGIN SUPPORTED" else 0) if MUT else 0)
