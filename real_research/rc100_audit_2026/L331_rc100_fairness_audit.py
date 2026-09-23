#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L331 -- THE RC100 FAIRNESS AUDIT: "the framework alone beats LCDM on RC100" does not survive a fair LCDM.
What survives is a ~3 sigma lean in the REDSHIFT TREND against non-evolving LCDM halos, from one survey.

THE CLAIM AUDITED
  real_research/dark_sector_2026/L320 (README, and the CLOSURE_MAP 09-22 rung-10 line): on RC100 (Nestor Shachar
  et al. 2023, ApJ 944, 78; 100 rotation curves, z = 0.6-2.5) the framework alone gives f_DM(<R_e) = 0.23-0.31
  and a flat a0(z), matching the data's 0.29, while LCDM gives 0.38-0.49 and a rising trend -- "the framework
  alone beats LCDM on both the level and the trend".  L320's LCDM is dark-matter-only NFW (Moster+13 halo masses,
  Dutton-Maccio concentrations, no contraction, no cores) -- the baseline RC100's own authors say over-predicts
  the inner dark matter and explain with cores.  The standing rule is never to say the data favour the framework
  over LCDM without testing the claim as hard as a failure.

WHAT THIS LANE CHECKS (same table, same estimator as L320; everything recomputed here)
  R1 the data: medians 0.38 (z < 1.3) and 0.27 (z >= 1.3) reproduce the paper's 0.38 +/- 0.23 and 0.27 +/- 0.18.
  R2 THE LEVEL IS NOT FRAMEWORK-SPECIFIC: nu_RAR at the canonical footing, the simple nu, and constant-a0 MOND at
     1.2e-10 all land at 0.28-0.32.  RC100 sits on the z = 0 radial acceleration relation; any MOND does this.
  R3 A CORED LCDM TIES THE LEVEL: coreNFW (Read+2016 form, r_c = 2 R_e -- one fitted choice) gives 0.28, with a
     per-galaxy rms (0.168) and rank correlation (0.59) equal to the framework's (0.162, 0.62).  Milder variants
     (halo mass -0.3 dex, c x 0.7, r_c = R_e) give 0.38-0.40.
  R4 WHAT SURVIVES IS THE TREND: the residual f_model - f_data rises with z by +0.077 +/- 0.026 for LCDM, cored or
     not (3.0 sigma, galaxy bootstrap), against +0.023 +/- 0.026 for the framework (0.9 sigma).  Cores that grow
     with z (one more free function) could absorb it; this lane does not test that.
  R5 THE FRAMEWORK'S OWN TENSION: flat against the data's inverted slope -0.112 +/- 0.062 is 1.8 sigma.
  VERDICT WORDING: "RC100 is consistent with the z = 0 RAR and disfavours non-evolving LCDM halos at ~3 sigma in the
  trend" -- a tie on the level, one survey, model-dependent f_DM.  Not "the framework beats LCDM".

  MUTATE=1 removes the core in R3 (plain NFW): the cored-level check must FAIL (rc = 1).

Run from the repository root:  python3 real_research/rc100_audit_2026/L331_rc100_fairness_audit.py
"""
import os, sys, csv, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG = "L331", "L331_rc100_fairness_audit"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}


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
    P("\n" + "=" * 104); P(t); P("=" * 104)


P(__doc__.split("WHAT THIS LANE CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: R3 uses plain NFW (no core); the cored-level check must FAIL ***")

G, MSUN, KPC, MPC = 6.6743e-11, 1.98892e30, 3.0856775814913673e19, 3.0856775814913673e22
h = 0.6736; H0 = 100 * h * 1e3 / MPC; Om, OL = 0.3153, 0.6847
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
nu_rar = lambda x: 1 / (1 - np.exp(-np.sqrt(np.clip(x, 1e-12, None))))
nu_simple = lambda x: 0.5 + np.sqrt(0.25 + 1 / x)
Ez = lambda z: math.sqrt(Om * (1 + z)**3 + OL)
rho_crit = lambda z: 3 * (H0 * Ez(z))**2 / (8 * math.pi * G)


def smhm_moster(Mh, z):                                   # Moster, Naab & White 2013, eq. 2 + table 1
    zz = z / (1 + z); M1 = 10**(11.590 + 1.195 * zz); N = 0.0351 - 0.0247 * zz
    b = 1.376 - 0.826 * zz; g = 0.608 + 0.329 * zz
    return 2 * N / ((Mh / M1)**-b + (Mh / M1)**g)


def halo_mass(Ms, z, shift=0.0):
    lg = np.linspace(9.5, 15.5, 6001); Mh = 10**lg; ms = Mh * smhm_moster(Mh, z)
    return float(10**(np.interp(math.log10(Ms), np.log10(ms), lg) + shift))


def c200(Mh, z):                                          # Dutton & Maccio 2014
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z**1.21); b = -0.101 + 0.026 * z
    return 10**(a + b * math.log10(Mh / (1e12 / h)))


def g_halo(Mh, z, r, core=None, cfac=1.0):
    c = c200(Mh, z) * cfac; r200 = (3 * Mh * MSUN / (4 * math.pi * 200 * rho_crit(z)))**(1 / 3); rs = r200 / c
    m = lambda x: math.log(1 + x) - x / (1 + x)
    M = Mh * MSUN * m(r / rs) / m(c)
    if core is not None:                                  # coreNFW (Read et al. 2016), n = 1
        M *= math.tanh(r / core)
    return G * M / r**2


rows = list(csv.DictReader(open(os.path.join(REPO, "real_research/data/rc100_nestorshachar2023_table3.csv"))))
gal = []
for r in rows:
    try:
        z, lMb, Re, fdm, gobs = (float(r[k]) for k in ("z", "logMbar_Msun", "Re_kpc", "fDM_within_Re", "g_Re_ms2"))
    except (ValueError, KeyError):
        continue
    gal.append(dict(z=z, Mb=10**lMb, Re=Re * KPC, fdm=fdm, gobs=gobs))
z = np.array([g["z"] for g in gal]); fd = np.array([g["fdm"] for g in gal])
lo, hi = z < 1.3, z >= 1.3
gbar = np.array([G * 0.5 * g["Mb"] * MSUN / g["Re"]**2 for g in gal])   # L320's xi_geo = 1 disc geometry


def f_mond(nufun, a0):
    return 1 - 1 / nufun(gbar / a0)


def f_lcdm(shift=0.0, core=None, cfac=1.0):
    out = []
    for g, gb in zip(gal, gbar):
        zz = g["z"]; mu = 0.5 * ((1 + zz) / 2)**2                        # L320's gas fraction
        Mh = halo_mass(g["Mb"] / (1 + mu), zz, shift)
        gc = g_halo(Mh, zz, g["Re"], None if core is None else core * g["Re"], cfac)
        out.append(1 - gb / (gb + gc))
    return np.array(out)


def rank_corr(a, b):
    return float(np.corrcoef(np.argsort(np.argsort(a)), np.argsort(np.argsort(b)))[0, 1])


def resid_trend(f, nboot=3000, seed=7):
    r = f - fd; s0 = np.polyfit(z, r, 1)[0]; rng = np.random.default_rng(seed)
    bs = [np.polyfit(z[i], r[i], 1)[0] for i in (rng.integers(0, len(z), len(z)) for _ in range(nboot))]
    return float(s0), float(np.std(bs))


# ============================================================================================ R1
banner("R1  THE DATA (Nestor Shachar+2023 table 3, as committed in real_research/data)")
m_lo, m_hi = float(np.median(fd[lo])), float(np.median(fd[hi]))
P(f"    N = {len(gal)};  median f_DM(<R_e): all {np.median(fd):.2f};  z < 1.3: {m_lo:.2f} (N={lo.sum()});  z >= 1.3: {m_hi:.2f} (N={hi.sum()})")
OUT["numbers"]["R1"] = {"N": len(gal), "median_all": float(np.median(fd)), "median_lo": m_lo, "median_hi": m_hi}
check("R1 the table reproduces the paper's medians (0.38 at z~1, 0.27 at z~2)", f"{m_lo:.2f} / {m_hi:.2f}",
      abs(m_lo - 0.38) <= 0.01 and abs(m_hi - 0.27) <= 0.01)

# ============================================================================================ R2
banner("R2  THE LEVEL IS NOT FRAMEWORK-SPECIFIC")
lev = {"nu_RAR canonical": f_mond(nu_rar, A0["canonical"]), "nu_RAR alt": f_mond(nu_rar, A0["alt"]),
       "simple nu canonical": f_mond(nu_simple, A0["canonical"]), "nu_RAR a0 = 1.2e-10": f_mond(nu_rar, 1.2e-10)}
for k, f in lev.items():
    P(f"    {k:22s} median f_DM {np.median(f):.2f}")
meds = [float(np.median(f)) for f in lev.values()]
OUT["numbers"]["R2"] = dict(zip(lev, meds))
check("R2 every MOND variant (both footings, two kernels, constant a0 = 1.2e-10) lands within 0.05 of the data's 0.29",
      ", ".join(f"{m:.2f}" for m in meds), all(abs(m - 0.29) <= 0.05 for m in meds),
      "the level match says RC100 sits on the z = 0 RAR; it does not single out a0 = kappa c sqrt(G rho_Lambda)")

# ============================================================================================ R3
banner("R3  LCDM VARIANTS: the L320 baseline and fairer halos")
variants = [("L320 baseline: Moster+13, DM14 NFW, no cores", {}),
            ("halo mass -0.3 dex", {"shift": -0.3}),
            ("concentration x 0.7", {"cfac": 0.7}),
            ("coreNFW r_c = 1 R_e", {"core": 1.0}),
            ("coreNFW r_c = 2 R_e", {"core": 2.0})]
vt = {}
for lab, kw in variants:
    f = f_lcdm(**kw); vt[lab] = f
    P(f"    {lab:45s} median {np.median(f):.2f}  (z<1.3 {np.median(f[lo]):.2f}, z>=1.3 {np.median(f[hi]):.2f});  "
      f"rms {np.sqrt(np.mean((f - fd)**2)):.3f};  rank corr {rank_corr(f, fd):+.2f}")
fw = lev["nu_RAR canonical"]
P(f"    {'framework (nu_RAR, canonical)':45s} median {np.median(fw):.2f};  rms {np.sqrt(np.mean((fw - fd)**2)):.3f};  "
  f"rank corr {rank_corr(fw, fd):+.2f}")
f_fair = f_lcdm() if MUTATE else vt["coreNFW r_c = 2 R_e"]
m_fair = float(np.median(f_fair)); rms_fair = float(np.sqrt(np.mean((f_fair - fd)**2)))
rms_fw = float(np.sqrt(np.mean((fw - fd)**2)))
OUT["numbers"]["R3"] = {lab: {"median": float(np.median(f)), "rms": float(np.sqrt(np.mean((f - fd)**2))),
                              "rank_corr": rank_corr(f, fd)} for lab, f in vt.items()}
check("R3 a cored LCDM halo (r_c = 2 R_e, one fitted choice) matches the level within 0.03 and the per-galaxy rms "
      "within 0.01 of the framework's", f"median {m_fair:.2f} vs 0.29; rms {rms_fair:.3f} vs framework {rms_fw:.3f}",
      abs(m_fair - 0.29) <= 0.03 and abs(rms_fair - rms_fw) <= 0.01,
      "on the level, RC100 is a tie once LCDM is given the cores its authors invoke")

# ============================================================================================ R4
banner("R4  WHAT SURVIVES: THE REDSHIFT TREND OF THE RESIDUAL (galaxy bootstrap)")
tr = {}
for lab, f in (("framework (nu_RAR, canonical)", fw), ("LCDM NFW baseline", vt["L320 baseline: Moster+13, DM14 NFW, no cores"]),
               ("LCDM coreNFW 2 R_e", vt["coreNFW r_c = 2 R_e"])):
    s, e = resid_trend(f); tr[lab] = (s, e)
    P(f"    {lab:32s} d(f_model - f_data)/dz = {s:+.3f} +/- {e:.3f}  ({s / e:+.1f} sigma)")
OUT["numbers"]["R4"] = {k: {"slope": v[0], "err": v[1]} for k, v in tr.items()}
s_l, e_l = tr["LCDM coreNFW 2 R_e"]; s_f, e_f = tr["framework (nu_RAR, canonical)"]
check("R4 the LCDM residual trend is >= 2.5 sigma for NFW and cored halos alike, the framework's is < 1.5 sigma",
      f"LCDM cored {s_l / e_l:+.1f} sigma, NFW {tr['LCDM NFW baseline'][0] / tr['LCDM NFW baseline'][1]:+.1f} sigma; "
      f"framework {s_f / e_f:+.1f} sigma", s_l / e_l >= 2.5 and tr['LCDM NFW baseline'][0] / tr['LCDM NFW baseline'][1] >= 2.5
      and abs(s_f / e_f) < 1.5,
      "a ~3 sigma lean against NON-EVOLVING halos; cores whose size grows with z are one more free function, untested here")

# ============================================================================================ R5
banner("R5  THE FRAMEWORK'S OWN TENSION WITH THE DATA SLOPE")
data_slope, data_err = -0.112, 0.062                        # L320's inversion (reproduces h16)
P(f"    flat a0(z) vs the data's inverted slope {data_slope} +/- {data_err}: {abs(data_slope) / data_err:.1f} sigma")
OUT["numbers"]["R5"] = {"sigma": abs(data_slope) / data_err}
check("R5 the framework's flat law sits 1.5-2 sigma from RC100's own inverted slope (reported, not hidden)",
      f"{abs(data_slope) / data_err:.1f} sigma", 1.5 <= abs(data_slope) / data_err <= 2.0, load_bearing=False)

banner("VERDICT")
P("""  RC100's level of inner dark matter (0.29) is what any MOND on the z = 0 RAR predicts (R2), and a cored LCDM halo
  matches it as well as the framework does (R3).  The claim "the framework alone beats LCDM on RC100" rests on a
  dark-matter-only NFW baseline and does not survive.  What survives is the redshift trend: LCDM halos that do not
  evolve leave a residual rising at ~3 sigma, cored or not, while the framework's residual is flat to 0.9 sigma
  (R4) and the framework itself is 1.8 sigma from the data slope (R5).  Fair wording: RC100 is consistent with the
  z = 0 RAR and disfavours non-evolving LCDM halos at ~3 sigma in the trend -- one survey, model-dependent f_DM.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
