#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L320 -- THE PRICE OF THE LAMBDA-TRIGGERED CARRIER AT HIGH REDSHIFT: RC100 (z = 0.6-2.5) under three models.

WHY.  L319's carrier passes the forest and S_8 BECAUSE it has not decayed at z >~ 1: the cold component keeps its small-scale
power, so galaxies at z >~ 1 still sit in (nearly) full cold halos.  In this framework those galaxies ALSO feel the MOND
kernel.  So the carrier converts the framework's high-z galaxy prediction from "MOND only, flat a0(z)" into "MOND + a
retained LCDM halo".  RC100 (Nestor Shachar+2023, 100 rotation curves at z = 0.6-2.5, in the repo) is the existing data set
that speaks to it.  This lane computes, per RC100 galaxy, the dark-matter fraction inside R_e predicted by
  (a) the framework alone                      g_obs = nu(g_bar/a0) g_bar                         (the control: flat by design)
  (b) the framework + the L319 carrier          g_obs = nu(g_tot/a0) g_tot, g_tot = g_bar + r(z) g_CDM
  (c) LCDM alone                                g_obs = g_bar + g_CDM
and pushes each prediction through the SAME closed-form inversion the data went through (hunt_2026/h16: a0 = (1 - f_DM) g_obs
/ [ln(1/f_DM)]^2), so model and data are compared as like with like: the d log a0/dz slope and the level.

INPUTS (stated, with their systematic ranges carried):
  g_bar(R_e) = G (M_bar/2) xi_geo / R_e^2, half the baryons inside the half-light radius, disc geometry xi_geo in {1.0, 1.3}.
  M_* = M_bar/(1 + mu_gas(z)), mu_gas = 0.5 ((1+z)/2)^2 (massive star-forming discs; +/- a factor 1.5 swept).
  M_halo from the Moster, Naab & White 2013 stellar-to-halo relation at z (their Table 1 fit); NFW with the Dutton & Maccio
  2014 c_200(M, z) (Planck); no adiabatic contraction (conservative for (b)/(c): contraction adds inner mass).
  r(z) = the L319 cell (p = 2, f_d(0) = 0.8) survival fraction, with full escape of daughters (the carrier's most favourable
  case: any retention adds cold mass and moves (b) toward (c)).
DATA CONTROL: the data slope reproduces h16's d log a0/dz = -0.112 +/- 0.063.
MUTATE=1 sets r(z) = 0 in model (b): (b) must then coincide with (a) and the "(b) rises" finding must FAIL (rc = 1).

Run from the repository root:  python3 real_research/dark_sector_2026/L320_carrier_highz_price_rc100.py
"""
import os, sys, csv, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L320_carrier_highz_price_rc100"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L320", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__)
G, MSUN, KPC, MPC = 6.6743e-11, 1.98892e30, 3.0856775814913673e19, 3.0856775814913673e22
h = 0.6736; H0 = 100 * h * 1e3 / MPC; Om, OL = 0.3153, 0.6847
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}


def nu(x):
    return 1.0 / (1.0 - np.exp(-np.sqrt(np.clip(x, 1e-12, None))))


def Ez(z): return math.sqrt(Om * (1 + z) ** 3 + OL)
def rho_crit(z): return 3 * (H0 * Ez(z)) ** 2 / (8 * math.pi * G)


def mstar_over_mh(Mh, z):
    """Moster, Naab & White 2013, Table 1 (M in Msun)."""
    zz = z / (1 + z)
    M1 = 10 ** (11.590 + 1.195 * zz); N = 0.0351 - 0.0247 * zz
    beta = 1.376 - 0.826 * zz; gamma = 0.608 + 0.329 * zz
    return 2 * N / ((Mh / M1) ** -beta + (Mh / M1) ** gamma)


def halo_mass(Ms, z):
    lg = np.linspace(9.5, 15.5, 6001); Mh = 10 ** lg
    ms = Mh * mstar_over_mh(Mh, z)
    return float(10 ** np.interp(math.log10(Ms), np.log10(ms), lg))


def c200(Mh, z):
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z
    return 10 ** (a + b * math.log10(Mh / (1e12 / h)))


def g_nfw(Mh, z, r):
    c = c200(Mh, z); r200 = (3 * Mh * MSUN / (4 * math.pi * 200 * rho_crit(z))) ** (1 / 3); rs = r200 / c
    m = lambda x: math.log(1 + x) - x / (1 + x)
    return G * Mh * MSUN * m(r / rs) / m(c) / r ** 2


# the L319 carrier's survival at z (p = 2, f_d(0) = 0.8), full-escape reading
_a = np.geomspace(1e-4, 1.0, 40000)
_Hs = np.sqrt(Om * _a ** -3 + OL)
_OmL = OL / (Om * _a ** -3 + OL)
_shape = (_OmL / _OmL[-1]) ** 2 / (_a * _Hs)
_cum = np.concatenate([[0], np.cumsum(0.5 * (_shape[1:] + _shape[:-1]) * np.diff(_a))])
_g0 = -math.log(1 - 0.8) / _cum[-1]
def retained(z):
    if MUTATE:
        return 0.0
    return float(math.exp(-_g0 * np.interp(1 / (1 + z), _a, _cum)))


def invert(fdm, gobs):
    """h16's closed form: a0 = (1 - f) g_obs / [ln(1/f)]^2."""
    if not (0.02 < fdm < 0.98):
        return float("nan")
    return math.log10((1 - fdm) * gobs / math.log(1 / fdm) ** 2)


# ------------------------------------------------------------------------------------------------ data
rows = list(csv.DictReader(open(os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3.csv"))))
gal = []
for r in rows:
    try:
        z, lMb, Re, fdm, g = (float(r[k]) for k in ("z", "logMbar_Msun", "Re_kpc", "fDM_within_Re", "g_Re_ms2"))
    except (ValueError, KeyError):
        continue
    if all(np.isfinite([z, lMb, Re, fdm, g])):
        gal.append(dict(z=z, Mb=10 ** lMb, Re=Re * KPC, fdm=fdm, gobs=g))
P(f"  RC100: {len(gal)} galaxies with z, M_bar, R_e, f_DM(<R_e), g_obs(R_e)")


def slope_boot(zs, las, n=2000, seed=3):
    m = np.isfinite(las); zs, las = np.asarray(zs)[m], np.asarray(las)[m]
    s = float(np.polyfit(zs, las, 1)[0]); rng = np.random.default_rng(seed)
    bs = [np.polyfit(zs[k], las[k], 1)[0] for k in (rng.integers(0, len(zs), len(zs)) for _ in range(n))]
    return s, float(np.std(bs)), int(m.sum())


zs = [g["z"] for g in gal]
la_data = [invert(g["fdm"], g["gobs"]) for g in gal]
s_data, e_data, n_data = slope_boot(zs, la_data)
banner("DATA CONTROL: the RC100 closed-form inversion reproduces h16")
check("D0 the data slope d log a0/dz reproduces h16's -0.112 +/- 0.063",
      f"{s_data:+.3f} +/- {e_data:.3f} (N = {n_data})", abs(s_data + 0.112) < 0.01)

# ------------------------------------------------------------------------------------------------ models
banner("THE THREE MODELS through the same inversion, over the systematic grid (geometry x gas fraction x footing)")
results = []
for foot, a0 in A0.items():
    for xi_geo in (1.0, 1.3):
        for mu_fac in (1 / 1.5, 1.0, 1.5):
            pred = {"framework": [], "carrier": [], "LCDM": []}
            fd_pred = {"framework": [], "carrier": [], "LCDM": []}
            for g in gal:
                z = g["z"]
                gb = G * 0.5 * g["Mb"] * MSUN * xi_geo / g["Re"] ** 2
                mu = mu_fac * 0.5 * ((1 + z) / 2) ** 2
                Mh = halo_mass(g["Mb"] / (1 + mu), z)
                gc = g_nfw(Mh, z, g["Re"])
                go = {"framework": nu(gb / a0) * gb,
                      "carrier": nu((gb + retained(z) * gc) / a0) * (gb + retained(z) * gc),
                      "LCDM": gb + gc}
                for k, v in go.items():
                    f = 1 - gb / v
                    fd_pred[k].append(f); pred[k].append(invert(f, v))
            row = dict(footing=foot, xi_geo=xi_geo, mu_fac=round(mu_fac, 3))
            for k in pred:
                s, e, n = slope_boot(zs, pred[k])
                row[k] = dict(slope=s, err=e, n=n, median_fdm=float(np.nanmedian(fd_pred[k])),
                              median_la=float(np.nanmedian(pred[k])))
            results.append(row)
            P(f"    {foot:9s} xi_geo {xi_geo} mu x{mu_fac:.2f}: slope fw {row['framework']['slope']:+.3f} | carrier "
              f"{row['carrier']['slope']:+.3f} | LCDM {row['LCDM']['slope']:+.3f};  median f_DM fw {row['framework']['median_fdm']:.2f} "
              f"carrier {row['carrier']['median_fdm']:.2f} LCDM {row['LCDM']['median_fdm']:.2f} (data {np.median([g['fdm'] for g in gal]):.2f})")
OUT["numbers"]["results"] = results
OUT["numbers"]["data"] = dict(slope=s_data, err=e_data, median_fdm=float(np.median([g["fdm"] for g in gal])),
                              median_la=float(np.nanmedian(la_data)))
fw_flat = all(abs(r["framework"]["slope"]) < 1e-6 for r in results)
check("C1 control: the framework-alone prediction returns a FLAT inverted a0(z) exactly (the inversion is the kernel's own)",
      f"max |slope| = {max(abs(r['framework']['slope']) for r in results):.1e}", fw_flat)
car = np.array([r["carrier"]["slope"] for r in results]); lcd = np.array([r["LCDM"]["slope"] for r in results])
z_car = (car - s_data) / e_data
check("C2 the carrier converts the flat prediction into a RISE: over the whole systematic grid its inverted slope is > 0 and sits "
      f"{z_car.min():.1f}-{z_car.max():.1f} sigma above RC100's measured slope",
      f"carrier slope {car.min():+.3f} to {car.max():+.3f}; LCDM {lcd.min():+.3f} to {lcd.max():+.3f}; data {s_data:+.3f} +/- {e_data:.3f}",
      car.min() > 0, "the price of passing the forest: galaxies at z >~ 1 carry the cold halo, and RC100 sees no rise")
fd_car = np.array([r["carrier"]["median_fdm"] for r in results]); fd_data = OUT["numbers"]["data"]["median_fdm"]
check("C3 the carrier's median dark fraction inside R_e exceeds RC100's measured median on every grid point (the level, not "
      "only the trend)", f"carrier {fd_car.min():.2f}-{fd_car.max():.2f} vs data {fd_data:.2f}", fd_car.min() > fd_data,
      "MOND plus a retained LCDM halo overshoots the dark fraction of z ~ 1-2.5 discs", load_bearing=False)

# ------------------------------------------------------------------------------------------------ verdict
banner("VERDICT")
P(f"""  L319's carrier passes the forest and S_8 only because its cold component is intact until z ~ 1.  RC100 then prices it:
  pushed through the data's own inversion, framework + carrier predicts d log a0/dz = {car.min():+.2f} to {car.max():+.2f} across the
  systematic grid (LCDM alone {lcd.min():+.2f} to {lcd.max():+.2f}), against the measured {s_data:+.3f} +/- {e_data:.3f}: {z_car.min():.1f}-{z_car.max():.1f} sigma,
  and a median dark fraction inside R_e of {fd_car.min():.2f}-{fd_car.max():.2f} against the data's {fd_data:.2f}.  RC100's own caveats apply
  (f_DM is model-dependent; selection is not controlled across redshift; h16 quotes it as a constraint on a rise, not a
  detection of a decline).  THE STRUCTURAL POINT does not depend on RC100: any carrier that keeps the forest's small-scale
  power at z = 2-3 puts cold halos around z >~ 1 galaxies, so the framework's flat-a0(z) prediction for galaxies cannot
  survive alongside it -- the dark-sector closure and the z ~ 2.5 flagship test pull against each other.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
