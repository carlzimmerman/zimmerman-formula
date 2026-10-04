#!/usr/bin/env python3
"""CFG327 -- MW ultra-faint offsets vs tidal susceptibility in the MW's own MOND field (frozen: FROZEN_CRITERIA.md, 219e0a0b9).
Run from the repository root:  python3 campaign_fresh_gravity/CFG327_ufd_tidal_susceptibility/cfg327_tidal.py   (CFG327_MUTATE=1 for MUTATE)"""
import os, csv, math, json
import numpy as np
from scipy.stats import spearmanr
import astropy.units as u
from astropy.coordinates import SkyCoord, Galactocentric

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("CFG327_MUTATE", "0") == "1"
SLUG = "cfg327_tidal" + ("_MUTATE" if MUTATE else "")
G, MSUN, PC, KPC, MYR = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19, 3.156e13
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
M_MW = 6e10
OUTL, OUT, CH = [], {"lane": "CFG327", "frozen": "219e0a0b9", "mutate": MUTATE, "checks": {}}, []


def P(s=""):
    print(s); OUTL.append(s)


def check(name, val, ok):
    CH.append(ok); OUT["checks"][name] = {"ok": bool(ok), "measured": str(val)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def nu(y):
    y = np.maximum(y, 1e-12); return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


def g_mw(r, a0):                      # r in m
    gN = G * M_MW * MSUN / r ** 2
    return gN * nu(gN / a0)


rows = list(csv.DictReader(open(os.path.join(REPO, "real_research/data/dsph/lvd_dwarf_mw.csv"))))
D = []
for r in rows:
    MV, sig, ul = fnum(r["M_V"]), fnum(r["vlos_sigma"]), fnum(r["vlos_sigma_ul"])
    rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
    Dh = fnum(r["distance_host"]) or fnum(r["distance_gc"])
    if MV is None or MV <= -7.7 or rh is None or Dh is None:
        continue
    d = dict(name=r["name"], host=r["host"], LV=10 ** (0.4 * (4.83 - MV)), rh=rh, Dgc=fnum(r["distance_gc"]),
             MHI=(10 ** fnum(r["mass_HI"]) if fnum(r["mass_HI"]) is not None else 0.0),
             ra=fnum(r["ra"]), dec=fnum(r["dec"]), dm=fnum(r["distance_modulus"]), vlos=fnum(r["vlos_systemic"]),
             pmra=fnum(r["pmra"]), pmdec=fnum(r["pmdec"]))
    if sig is not None and ul is None and sig > 0:
        d["sig"] = sig; d["esig"] = 0.5 * ((fnum(r["vlos_sigma_em"]) or 0.2 * sig) + (fnum(r["vlos_sigma_ep"]) or 0.2 * sig))
    elif ul is not None:
        d["sig_ul"] = ul
    else:
        continue
    D.append(d)
RES = [d for d in D if "sig" in d]
P(f"CFG327: {len(RES)} resolved + {len(D) - len(RES)} upper limits (cut as AUDIT_UFD)")


def pred(d, a0):
    Mb = 2.0 * d["LV"] + 1.33 * d["MHI"]
    rm = (4.0 / 3.0) * d["rh"] * PC
    gN = G * 0.5 * Mb * MSUN / rm ** 2
    g = gN * nu(gN / a0)
    return math.sqrt(g * rm / 3.0) / 1e3, g * rm ** 2 / G / MSUN          # sigma_pred km/s, M_eff (of half mass) Msun


# ---- orbits in the MW's MOND field
def accel(x, a0):
    r = np.linalg.norm(x); return -g_mw(r, a0) * x / r


def integrate(x, v, a0, T=6000.0, dt=0.5):
    n = int(T / dt); h = -dt * MYR                      # backwards
    rmin = np.linalg.norm(x); a = accel(x, a0)
    E0 = 0.5 * v @ v + phi(np.linalg.norm(x), a0); Emax = 0.0
    for i in range(n):
        v = v + 0.5 * h * a; x = x + h * v; a = accel(x, a0); v = v + 0.5 * h * a
        rr = np.linalg.norm(x); rmin = min(rmin, rr)
        if i % 400 == 0:
            Emax = max(Emax, abs((0.5 * v @ v + phi(rr, a0)) - E0) / abs(E0))
    return rmin, Emax


_rg = np.logspace(np.log10(0.1 * KPC), np.log10(3000 * KPC), 4000)


def phi(r, a0):                                         # potential from integrating g outward, zero at 3 Mpc
    return -np.interp(r, _rg, _cum[a0]) if False else _phi_interp(r, a0)


_cum = {}
for a0 in A0.values():
    gg = g_mw(_rg, a0)
    integ = np.concatenate([[0.0], np.cumsum(0.5 * (gg[1:] + gg[:-1]) * np.diff(_rg))])
    _cum[a0] = integ - integ[-1]                       # phi(r) = -int_r^Rmax g dr


def _phi_interp(r, a0):
    return np.interp(r, _rg, _cum[a0])


P("\nControls")
x = np.array([50 * KPC, 0, 0]); vc = math.sqrt(g_mw(50 * KPC, A0["canonical"]) * 50 * KPC)
rp_c, Ec = integrate(x, np.array([0, vc, 0]), A0["canonical"])
check("C3 circular orbit at 50 kpc keeps r_p within 1%", f"r_p/50kpc = {rp_c / (50 * KPC):.4f}", abs(rp_c / (50 * KPC) - 1) < 0.01)

gc = Galactocentric()
Erec = []
for d in RES:
    d["rp"] = {}
    if None in (d["pmra"], d["pmdec"], d["vlos"], d["dm"], d["ra"], d["dec"]):
        continue
    c = SkyCoord(ra=d["ra"] * u.deg, dec=d["dec"] * u.deg, distance=10 ** (d["dm"] / 5 + 1) * u.pc,
                 pm_ra_cosdec=d["pmra"] * u.mas / u.yr, pm_dec=d["pmdec"] * u.mas / u.yr, radial_velocity=d["vlos"] * u.km / u.s)
    g6 = c.transform_to(gc)
    xx = np.array([g6.x.to(u.m).value, g6.y.to(u.m).value, g6.z.to(u.m).value])
    vv = np.array([g6.v_x.to(u.m / u.s).value, g6.v_y.to(u.m / u.s).value, g6.v_z.to(u.m / u.s).value])
    d["rnow"] = np.linalg.norm(xx)
    for foot, a0 in A0.items():
        rp, Em = integrate(xx, vv, a0); d["rp"][foot] = rp; Erec.append(Em)
check("C2 orbit energy conserved < 1e-4 over 6 Gyr (all orbits, both footings)", f"max |dE/E| = {max(Erec):.2e}", max(Erec) < 1e-4)

rng = np.random.default_rng(327)
VERD = {}
for foot, a0 in A0.items():
    P(f"\n--- footing {foot} (a0 = {a0:.4e}) ---")
    for d in RES:
        sp, Meff = pred(d, a0); d["delta"] = math.log10(d["sig"] / sp); d["Meff"] = 2 * Meff
        for key, rr in (("A", d["rp"].get(foot)), ("B", (d["Dgc"] or 0) * KPC if d["Dgc"] else None)):
            if rr:
                Mmw = g_mw(rr, a0) * rr ** 2 / G / MSUN
                rt = rr * (d["Meff"] / (3 * Mmw)) ** (1 / 3)
                d["m" + key] = d["rh"] * PC / rt
            else:
                d["m" + key] = None
    med_all = float(np.median([d["delta"] for d in RES]))
    P(f"  measured-only median offset {med_all:+.4f} dex (AUDIT_UFD measured-only row is the C1 reference)")
    S = [d for d in RES if d["mA"] is not None]
    P(f"  metric A available for {len(S)} of {len(RES)} (missing PM/RV: {', '.join(d['name'] for d in RES if d['mA'] is None) or 'none'})")
    mA = np.array([d["mA"] for d in S]); dl = np.array([d["delta"] for d in S])
    if MUTATE:
        mA = rng.permutation(mA)
    rho, p2 = spearmanr(np.log10(mA), dl); p1 = p2 / 2 if rho > 0 else 1 - p2 / 2
    order = np.argsort(mA); low = dl[order[: len(S) // 3]]
    bs = [np.median(rng.choice(low, len(low))) for _ in range(4000)]
    err = math.hypot(float(np.std(bs)), 0.077); medlow = float(np.median(low)); zlow = medlow / err
    hi = dl[order[-(len(S) // 3):]]
    P(f"  T1 Spearman rho(delta, log A) = {rho:+.3f}, one-sided p = {p1:.3g}")
    P(f"  T2 least-susceptible third (N={len(low)}): median delta {medlow:+.3f} +- {err:.3f} ({zlow:.2f} sigma); most-susceptible third {np.median(hi):+.3f}")
    T1, T2 = (rho > 0 and p1 < 0.01), abs(zlow) < 2
    for d in S:
        P(f"    {d['name']:22s} delta {d['delta']:+.3f}  r_p {d['rp'][foot] / KPC:7.1f} kpc  A {d['mA']:.3e}  B {d['mB'] if d['mB'] is None else round(d['mB'], 5)}")
    sB = [d for d in RES if d["mB"]]
    rB, pB = spearmanr(np.log10([d["mB"] for d in sB]), [d["delta"] for d in sB])
    nl = [d for d in S if d["host"].strip().lower() not in ("lmc", "smc")]
    rN, pN = spearmanr(np.log10([d["mA"] for d in nl]), [d["delta"] for d in nl])
    far = [d for d in S if d["rp"][foot] >= 10 * KPC]
    rF, pF = spearmanr(np.log10([d["mA"] for d in far]), [d["delta"] for d in far])
    P(f"  reported: metric B rho {rB:+.3f} (p2 {pB:.3g}); no LMC/SMC-hosted rho {rN:+.3f} (N={len(nl)}, p2 {pN:.3g}); r_p >= 10 kpc rho {rF:+.3f} (N={len(far)}, p2 {pF:.3g})")
    VERD[foot] = dict(rho=rho, p1=p1, T1=T1, T2=T2, med_low=medlow, err_low=err, z_low=zlow, med_high=float(np.median(hi)),
                      N=len(S), med_all=med_all, rhoB=rB, rho_noLMC=rN, rho_far=rF)

if MUTATE:
    check("MUTATE shuffled metric: T1 must fail on both footings", {f: VERD[f]["T1"] for f in VERD}, not any(VERD[f]["T1"] for f in VERD))
else:
    T1all = all(VERD[f]["T1"] for f in VERD); T2all = all(VERD[f]["T2"] for f in VERD)
    verdict = "TIDES EXPLAIN" if T1all and T2all else ("PARTIAL" if T1all else "NOT SUPPORTED")
    P(f"\nVERDICT: {verdict}")
    OUT["verdict"] = verdict
OUT["footings"] = VERD
P(f"\n{sum(CH)}/{len(CH)} checks pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(OUTL) + "\n")
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=2, default=float)
raise SystemExit(0 if all(CH) else 1)
