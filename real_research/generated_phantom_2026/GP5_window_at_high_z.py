#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
GP5 -- THE GP4 WINDOW AT HIGH REDSHIFT: does the generated phantom with L319's kicked carrier (lambda = 1 Mpc;
f_d(0) = 0.95, v_k = 1200 or f_d(0) = 0.9, v_k = 1400) keep the framework's flagship prediction -- a FLAT deep-MOND
Tully-Fisher zero point at z ~ 2.5 (0.00 dex, against LCDM's +0.33) -- and RC100's low dark fractions at z ~ 1-2.5?

WHY.  GP4 found the first window across every z <~ 1 gate on the record (alternative thresholds): KiDS, cosmic shear,
X-COP, the galaxies, S_8 and the forest.  L356 showed, for L319's carrier at f_d(0) = 0.8, that the price comes at high
redshift: a Lambda-triggered decay acts at z < 1, so galaxies at z ~ 2.5 still sit in the carrier's halo, and the
flagship zero point moves +0.82..+1.05 dex.  GP4's cells decay more (0.9-0.95 by today), but on the same Omega_Lambda^2
clock.  This lane scores them at high z with L320's and L356's machinery, unedited.

THE MODEL (L356's, one change).  Baryons feel their own phantom plus the carrier's Newtonian field (the construction's
additive observable, L353/GP1): g_obs = nu(g_bar/a0) g_bar + r(z) g_NFW, the carrier's halo from Moster+13 and the
Dutton-Maccio concentration (L320), r(z) the carrier still in the galaxy at z.  THE CHANGE: r(z) is L319's survival for
GP4's cells (p = 2, f_d(0) = 0.9 and 0.95; kicked daughters at 1200-1400 km/s escape galaxy halos, L320's full-escape
reading) instead of f_d(0) = 0.8.  GP1's kernel differs from L320's nu only by the external field (~1e-4 a0) and the
screening at lambda = 1 Mpc, both negligible at R_e and at the flagship's outer radius (g_bar = 0.1 a0, 11-39 kpc);
L340's nu_mono is reported alongside L320's nu.

CHECKS
  C1 CONTROL: with f_d(0) = 0.8 the machinery reproduces L356's committed flagship shifts (to 0.005 dex).
  C2 CONTROL: GP4's cells' survival at z = 0.5 matches L364's committed F(z = 0.5) (to 0.005).
  F1 THE FLAGSHIP GATE (fixed before the run): for both GP4 window cells, both footings, M_b = 1e10-1e11 and L356's
     gas-fraction range, the deep-MOND Tully-Fisher zero point at z = 2.5 stays within 0.10 dex of the framework's 0.00 --
     the construction keeps the prediction that separates the framework from LCDM (+0.33).
  F2 (documentary) the carrier still in galaxies, r(z), at z = 0.5, 1, 1.5, 2, 2.5, and the zero-point shift at each z
     (where a lower-z deep-MOND test would sit).
  R1 (documentary; RC100 is calibration-conditional, L331/L332) the median dark fraction inside R_e and the inverted a0(z)
     slope for the window cells, against the data (0.29; -0.112 +/- 0.063).
MUTATE=1: the carrier has left galaxies at every z (r = 0).  F1 must then PASS -- an inverted control (rc = 0) showing any
shift is the carrier's.
SCOPE.  L356's: the carrier's intact NFW halo (no adiabatic contraction, no depletion by the kicks before it decays),
point-like baryons at the flagship's outer radius, Moster+13 halo masses (LCDM-calibrated).

Run from the repository root:  python3 real_research/generated_phantom_2026/GP5_window_at_high_z.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "GP5_window_at_high_z"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "GP5", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the carrier has left galaxies at every z (r = 0); F1 must PASS (inverted control, rc = 0) ***")

# ---------------------------------------------------------------------------------- L320's machinery and data, unedited
DS = os.path.join(REPO, "real_research", "dark_sector_2026")
_src = open(os.path.join(DS, "L320_carrier_highz_price_rc100.py")).read()
_top = _src.split("# ------------------------------------------------------------------------------------------------ models")[0]
L20 = {"__name__": "l320", "__file__": os.path.join(DS, "L320_carrier_highz_price_rc100.py")}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_top.replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), L20)
nu, halo_mass, g_nfw, invert, slope_boot = L20["nu"], L20["halo_mass"], L20["g_nfw"], L20["invert"], L20["slope_boot"]
gal, A0, G, MSUN, KPC = L20["gal"], L20["A0"], L20["G"], L20["MSUN"], L20["KPC"]
Om, OL = L20["Om"], L20["OL"]
zs = [g["z"] for g in gal]; s_data, e_data = L20["s_data"], L20["e_data"]
fd_data = float(np.median([g["fdm"] for g in gal]))
P(f"  L320 loaded: {len(gal)} RC100 galaxies; data slope {s_data:+.3f} +/- {e_data:.3f}; median f_DM(<R_e) {fd_data:.2f}")

# L340's nu_mono (GP1's kernel), for the side-by-side
_B = {"__name__": "bk1", "__file__": os.path.join(REPO, "real_research", "blind_kernel_2026", "BK1_screened_kernel.py")}
_bs = open(_B["__file__"]).read().split("# ------------------------------------------------------------------ linear LCDM")[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(_bs.replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), _B)
nu_mono = lambda x: float(_B["nu_mono_arr"](np.array([x]))[0])


# ---------------------------------------------------------------------------------- L319's survival, any f_d(0) (L320's law)
_a = np.geomspace(1e-4, 1.0, 40000)
_Hs = np.sqrt(Om * _a ** -3 + OL); _OmL = OL / (Om * _a ** -3 + OL)
_shape = (_OmL / _OmL[-1]) ** 2 / (_a * _Hs)
_cum = np.concatenate([[0], np.cumsum(0.5 * (_shape[1:] + _shape[:-1]) * np.diff(_a))])


def survival(z, fd0):
    g0 = -math.log(1 - fd0) / _cum[-1]
    return float(math.exp(-g0 * np.interp(1 / (1 + z), _a, _cum)))


def retained(z, fd0):
    return 0.0 if MUTATE else survival(z, fd0)


CELLS = [(0.95, 1200.0), (0.90, 1400.0)]                                 # GP4's alternative-set window (lambda = 1 Mpc)


def flagship(fd0, z, kernel="l320", r_override=None):
    """L356's H3 at redshift z: the Tully-Fisher zero-point shift 2 log10(g_co/g_fw) at the outer radius g_bar = 0.1 a0."""
    rows = []
    for foot, a0 in A0.items():
        for lMb in (10.0, 10.5, 11.0):
            Mb = 10 ** lMb
            r_out = math.sqrt(G * Mb * MSUN / (0.1 * a0)); gb = G * Mb * MSUN / r_out ** 2
            nuf = nu if kernel == "l320" else nu_mono
            g_fw = nuf(gb / a0) * gb
            for mu_fac in (1 / 1.5, 1.0, 1.5):
                mu = mu_fac * 0.5 * ((1 + z) / 2) ** 2
                r_ = retained(z, fd0) if r_override is None else r_override
                gc = g_nfw(halo_mass(Mb / (1 + mu), z), z, r_out) * r_
                rows.append((foot, lMb, round(mu_fac, 2), r_out / KPC, 2 * math.log10((g_fw + gc) / g_fw)))
    return rows


# ============================================================================================ C1, C2
banner("C1-C2  CONTROLS: L356's committed flagship shifts (f_d(0) = 0.8); L364's committed F(z = 0.5) for GP4's cells")
l356 = json.load(open(os.path.join(DS, "L356_construction_highz_price_results.json")))["numbers"]["H3"]
mine = flagship(0.8, 2.5, r_override=(survival(2.5, 0.8)))
dev1 = max(abs(m[4] - r_["dzp_dex"]) for m, r_ in zip(mine, l356))
P(f"    max |shift - L356| = {dev1:.1e} dex (f_d(0) = 0.8, z = 2.5)")
l364 = {(c["fd"], c["vk"]): c for c in json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026",
                                                                  "L364_replacement_carrier_cosmic_shear_results.json")))["numbers"]["scan"]}
dev2 = max(abs((1 - survival(0.5, fd)) - l364[(fd, vk)]["fd_z05"]) for fd, vk in CELLS)
P(f"    max |F(z = 0.5) - L364| = {dev2:.1e} for GP4's cells")
OUT["numbers"]["C"] = {"dev_l356": dev1, "dev_l364": dev2}
check("C1 CONTROL: L356's flagship shifts reproduced (0.005 dex)", f"{dev1:.1e}", dev1 < 5e-3)
check("C2 CONTROL: L364's decayed fraction at z = 0.5 reproduced for GP4's cells (0.005)", f"{dev2:.1e}", dev2 < 5e-3)

# ============================================================================================ F1, F2
banner("F1-F2  THE FLAGSHIP FOR GP4's WINDOW: the deep-MOND Tully-Fisher zero point with the carrier still in galaxies")
F = {}
for fd, vk in CELLS:
    for z in (0.5, 1.0, 1.5, 2.0, 2.5):
        for kern in ("l320", "mono"):
            rows = flagship(fd, z, kern)
            F[(fd, vk, z, kern)] = {"r": retained(z, fd), "shift_min": min(r_[4] for r_ in rows), "shift_max": max(r_[4] for r_ in rows),
                                    "rows": rows}
    P(f"    f_d(0) {fd}, v_k {vk:.0f}: " + "; ".join(
        f"z {z}: r = {F[(fd, vk, z, 'l320')]['r']:.3f}, shift {F[(fd, vk, z, 'l320')]['shift_min']:+.2f}..{F[(fd, vk, z, 'l320')]['shift_max']:+.2f}"
        for z in (0.5, 1.0, 1.5, 2.0, 2.5)))
    P(f"      (nu_mono at z = 2.5: {F[(fd, vk, 2.5, 'mono')]['shift_min']:+.2f}..{F[(fd, vk, 2.5, 'mono')]['shift_max']:+.2f})")
OUT["numbers"]["F"] = {f"{k[0]}|{k[1]}|{k[2]}|{k[3]}": {kk: v for kk, v in d.items() if kk != "rows"} for k, d in F.items()}
worst = max(max(abs(F[(fd, vk, 2.5, k)]["shift_min"]), abs(F[(fd, vk, 2.5, k)]["shift_max"])) for fd, vk in CELLS for k in ("l320", "mono"))
check("F1 THE FLAGSHIP: for GP4's window cells the deep-MOND Tully-Fisher zero point at z = 2.5 stays within 0.10 dex of the "
      "framework's 0.00 (both footings, M_b 1e10-1e11, L356's gas range, both kernels)", f"worst |shift| {worst:.2f} dex (LCDM +0.33)",
      worst <= 0.10, "the carrier must have left galaxies by z ~ 2.5 for the flagship to keep separating the framework from LCDM")
check("F2 (documentary) the carrier still in galaxies and the zero-point shift by redshift",
      {f"fd {fd}": {str(z): f"r {F[(fd, vk, z, 'l320')]['r']:.3f}, {F[(fd, vk, z, 'l320')]['shift_max']:+.2f}" for z in (0.5, 1.0, 1.5, 2.0, 2.5)}
       for fd, vk in CELLS}, True, "", load_bearing=False)

# ============================================================================================ R1 RC100
banner("R1  RC100 (documentary; calibration-conditional): dark fraction inside R_e and the inverted a0(z) slope")
R = {}
for fd, vk in CELLS:
    rows = []
    for foot, a0 in A0.items():
        for xi_geo in (1.0, 1.3):
            for mu_fac in (1 / 1.5, 1.0, 1.5):
                pred, fdm = [], []
                for g in gal:
                    z = g["z"]; gb = G * 0.5 * g["Mb"] * MSUN * xi_geo / g["Re"] ** 2
                    mu = mu_fac * 0.5 * ((1 + z) / 2) ** 2
                    gc = g_nfw(halo_mass(g["Mb"] / (1 + mu), z), z, g["Re"]) * retained(z, fd)
                    go = nu(gb / a0) * gb + gc
                    f = 1 - gb / go; fdm.append(f); pred.append(invert(f, go))
                s, e, n = slope_boot(zs, pred)
                rows.append({"footing": foot, "xi_geo": xi_geo, "mu_fac": round(mu_fac, 3), "slope": s, "median_fdm": float(np.nanmedian(fdm))})
    R[(fd, vk)] = rows
    sl = np.array([r_["slope"] for r_ in rows]); fm = np.array([r_["median_fdm"] for r_ in rows])
    P(f"    f_d(0) {fd}, v_k {vk:.0f}: inverted a0(z) slope {sl.min():+.3f}..{sl.max():+.3f} (data {s_data:+.3f} +/- {e_data:.3f}); "
      f"median f_DM {fm.min():.2f}..{fm.max():.2f} (data {fd_data:.2f})")
OUT["numbers"]["R1"] = {f"{k[0]}|{k[1]}": v for k, v in R.items()}
check("R1 (documentary) RC100 for GP4's window cells", {f"fd {k[0]}": f"f_DM {min(r_['median_fdm'] for r_ in v):.2f}-{max(r_['median_fdm'] for r_ in v):.2f}"
                                                        for k, v in R.items()}, True,
      "RC100's level and trend are calibration-conditional (L331/L332); reported, not gated", load_bearing=False)

# ============================================================================================ verdict
banner("VERDICT")
r25 = {fd: retained(2.5, fd) for fd, _ in CELLS}
P(f"""  At z = 2.5 the carrier is still in galaxies (r = {r25[0.95]:.3f} for f_d(0) = 0.95, {r25[0.9]:.3f} for 0.9): the Omega_Lambda^2 clock
  that lets it pass the forest also keeps it in galaxies until z < 1.  GP4's window cells shift the flagship zero point by
  {min(F[(fd, vk, 2.5, 'l320')]['shift_min'] for fd, vk in CELLS):+.2f}..{max(F[(fd, vk, 2.5, 'l320')]['shift_max'] for fd, vk in CELLS):+.2f} dex at z = 2.5 (framework 0.00, LCDM +0.33).  Gate F1 (<= 0.10 dex): {'PASS' if worst <= 0.10 else 'FAIL'}.
  What the window needs at high z: a carrier that leaves galaxy halos by z ~ 2.5 while staying cold in the web (the
  forest) and free-streaming by z ~ 0.5 (cosmic shear) -- a density (virialization) trigger in bound regions on top of the
  late Lambda trigger (L357/L365/L379's direction), not the Lambda clock alone.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname} ({time.time() - T0:.0f} s)")
sys.exit(0 if n_fail == 0 else 1)
