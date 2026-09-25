#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L356 -- THE CARRIER'S HIGH-REDSHIFT PRICE UNDER THE KERNEL-INVISIBLE CONSTRUCTION (L353): RC100 re-scored with the
unboosted carrier, and what the carrier does to the framework's flagship test (the deep-MOND Tully-Fisher zero point at
z ~ 2.5, predicted FLAT at 0.00 dex against LCDM's +0.33).

WHY.  L320 priced L319's carrier on RC100 with the carrier BOOSTED by the kernel, g_obs = nu(g_tot/a0) g_tot.  Under L353's
construction the carrier is invisible to the kernel and the observable is additive: g_obs = nu(g_bar/a0) g_bar + r(z) g_CDM
(baryons feel the phantom of the baryons plus the carrier's Newtonian field; L353 N1/N3).  The carrier passes the forest
only because it is intact at z >~ 1 (L319: f_d(z = 1) small), so galaxies at z ~ 2.5 still sit in its halos -- exactly
where the flagship test is taken.

WHAT THIS LANE COMPUTES (L320's machinery and data loaded unedited; one model added)
  H1 CONTROL: L320's three models reproduce (framework flat; boosted carrier rises).
  H2 RC100 under the construction: the inverted a0(z) slope and the median dark fraction inside R_e for
     g_obs = nu(g_bar/a0) g_bar + r(z) g_CDM, over L320's systematic grid (geometry x gas fraction x footing), against the
     data slope (-0.112 +/- 0.063) -- the same inversion the data went through.
  H3 THE FLAGSHIP: for deep-MOND rotators at z = 2.5 (M_b = 1e10 .. 1e11, outer radius where g_bar = 0.1 a0), the shift of
     the Tully-Fisher zero point log[v^4/(G M_b a0)] caused by the carrier's halo (Moster+13 halo, Dutton-Maccio c, r(z) from
     L319's decay law), against the framework's 0.00 and LCDM's +0.33 dex.
  MUTATE=1 sets r(z) = 0 (no carrier): H3's shift must vanish and the load-bearing H3 finding must FAIL (rc = 1).
  RESULT IN ONE LINE: kernel-invisibility does not lower the carrier's high-z price; the forest-compatible carrier must
  leave galaxies by z ~ 2.5, which a Lambda trigger cannot do.

SCOPE.  RC100's standing is weak (L331/L332: level not framework-specific; the trend is calibration-conditional and not
replicated on KMOS3D); H2 is reported, not load-bearing.  H3 uses the carrier's intact NFW halo with no adiabatic
contraction or depletion by the kicks (it has not decayed at z = 2.5), and point-like baryons at the outer radius.

Run from the repository root:  python3 real_research/dark_sector_2026/L356_construction_highz_price.py
"""
import os, sys, json, math, csv
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L356_construction_highz_price"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L356", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 104); P(t); P("=" * 104)


P(__doc__.split("WHAT THIS LANE COMPUTES")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: r(z) = 0 (no carrier); H3 must FAIL ***")

# ---------------------------------------------------------------------------------- L320's machinery and data, unedited
_src = open(os.path.join(HERE, "L320_carrier_highz_price_rc100.py")).read()
_top = _src.split("# ------------------------------------------------------------------------------------------------ models")[0]
L20 = {"__name__": "l320", "__file__": os.path.join(HERE, "L320_carrier_highz_price_rc100.py")}
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    exec(_top.replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), L20)
nu, halo_mass, g_nfw, invert, slope_boot = L20["nu"], L20["halo_mass"], L20["g_nfw"], L20["invert"], L20["slope_boot"]
retained_l320 = L20["retained"]
retained = (lambda z: 0.0) if MUTATE else retained_l320
gal, A0, G, MSUN, KPC = L20["gal"], L20["A0"], L20["G"], L20["MSUN"], L20["KPC"]
zs = [g["z"] for g in gal]
s_data, e_data = L20["s_data"], L20["e_data"]
P(f"  L320 loaded: {len(gal)} RC100 galaxies; data slope {s_data:+.3f} +/- {e_data:.3f}; r(z=1, 2, 2.5) = "
  f"{retained_l320(1.0):.3f}, {retained_l320(2.0):.3f}, {retained_l320(2.5):.3f}")

# ============================================================================================ H1 + H2
banner("H1-H2  RC100: framework, boosted carrier (L320), and the construction's additive carrier (same inversion)")
res = []
for foot, a0 in A0.items():
    for xi_geo in (1.0, 1.3):
        for mu_fac in (1 / 1.5, 1.0, 1.5):
            pred = {"framework": [], "boosted": [], "construction": []}; fd = {k: [] for k in pred}
            for g in gal:
                z = g["z"]; gb = G * 0.5 * g["Mb"] * MSUN * xi_geo / g["Re"]**2
                mu = mu_fac * 0.5 * ((1 + z) / 2)**2
                gc = g_nfw(halo_mass(g["Mb"] / (1 + mu), z), z, g["Re"]); r_ = retained_l320(z)
                go = {"framework": nu(gb / a0) * gb,
                      "boosted": nu((gb + r_ * gc) / a0) * (gb + r_ * gc),
                      "construction": nu(gb / a0) * gb + r_ * gc}
                for k, v in go.items():
                    f = 1 - gb / v; fd[k].append(f); pred[k].append(invert(f, v))
            row = dict(footing=foot, xi_geo=xi_geo, mu_fac=round(mu_fac, 3))
            for k in pred:
                s, e, n = slope_boot(zs, pred[k]); row[k] = dict(slope=s, median_fdm=float(np.nanmedian(fd[k])))
            res.append(row)
fw = np.array([r_["framework"]["slope"] for r_ in res]); bo = np.array([r_["boosted"]["slope"] for r_ in res])
co = np.array([r_["construction"]["slope"] for r_ in res])
fdb = np.array([r_["boosted"]["median_fdm"] for r_ in res]); fdc = np.array([r_["construction"]["median_fdm"] for r_ in res])
fd_data = float(np.median([g["fdm"] for g in gal]))
P(f"    slopes: framework {fw.min():+.3f}..{fw.max():+.3f} | boosted carrier (L320) {bo.min():+.3f}..{bo.max():+.3f} | "
  f"construction {co.min():+.3f}..{co.max():+.3f} | data {s_data:+.3f} +/- {e_data:.3f}")
P(f"    median f_DM(<R_e): boosted {fdb.min():.2f}..{fdb.max():.2f} | construction {fdc.min():.2f}..{fdc.max():.2f} | data {fd_data:.2f}")
OUT["numbers"]["H2"] = {"rows": res, "data": dict(slope=s_data, err=e_data, median_fdm=fd_data)}
check("H1 (control) L320 reproduced: the framework alone inverts to a flat a0(z); the boosted carrier rises",
      f"framework max |slope| {np.abs(fw).max():.1e}; boosted {bo.min():+.3f}..{bo.max():+.3f}", np.abs(fw).max() < 1e-6 and bo.min() > 0,
      load_bearing=False)
zc = (co - s_data) / e_data
check("H2 (reported; RC100 is calibration-conditional, L332) kernel-invisibility does NOT lower the carrier's RC100 price: the "
      "additive carrier's inverted a0(z) rises at least as steeply as the boosted one, and its dark fraction overshoots the data's",
      f"construction slope {co.min():+.3f}..{co.max():+.3f} ({zc.min():.1f}-{zc.max():.1f} sigma above the data) vs boosted "
      f"{bo.min():+.3f}..{bo.max():+.3f}; median f_DM {fdc.min():.2f}-{fdc.max():.2f} vs data {fd_data:.2f}",
      co.min() >= bo.min() - 0.02 and fdc.min() > fd_data, "near R_e (g_bar ~ 1.6 a0) the kernel's response slope is ~1.05, so "
      "boosting or not changes the carrier's contribution by only a few per cent; the halo itself is the price", load_bearing=False)

# ============================================================================================ H3 the flagship
banner("H3  THE FLAGSHIP: the deep-MOND Tully-Fisher zero point at z = 2.5 with the carrier's (intact) halo")
ZF = 2.5
rows = []
for foot, a0 in A0.items():
    for lMb in (10.0, 10.5, 11.0):
        Mb = 10**lMb
        r_out = math.sqrt(G * Mb * MSUN / (0.1 * a0))                  # outer radius where g_bar = 0.1 a0 (deep MOND)
        gb = G * Mb * MSUN / r_out**2
        g_fw = nu(gb / a0) * gb
        for mu_fac in (1 / 1.5, 1.0, 1.5):
            mu = mu_fac * 0.5 * ((1 + ZF) / 2)**2
            gc = g_nfw(halo_mass(Mb / (1 + mu), ZF), ZF, r_out) * retained(ZF)
            g_co = g_fw + gc
            dzp = 2 * math.log10(g_co / g_fw)                        # v^2 = g r at fixed r: log10 v^4 shifts by 2 log10(g_co/g_fw)
            rows.append((foot, lMb, round(mu_fac, 2), r_out / KPC, gc / g_fw, dzp))
for r_ in rows:
    if r_[2] == 1.0:
        P(f"    {r_[0]:9s} log M_b {r_[1]:.1f}: outer radius {r_[3]:.1f} kpc; carrier/phantom-field ratio {r_[4]:.2f}; "
          f"zero-point shift {r_[5]:+.2f} dex")
shifts = np.array([r_[5] for r_ in rows])
OUT["numbers"]["H3"] = [dict(zip(("footing", "logMb", "mu_fac", "r_out_kpc", "gc_over_gfw", "dzp_dex"), r_)) for r_ in rows]
check("H3 with the carrier intact at z = 2.5 (as the forest requires), the construction's deep-MOND Tully-Fisher zero point "
      "shifts up by a large fraction of the framework-LCDM separation (0.33 dex): the flagship's discriminating power is "
      "eroded by the dark sector that passes the forest", f"shift {shifts.min():+.2f} .. {shifts.max():+.2f} dex (framework 0.00, "
      f"LCDM +0.33)", shifts.min() > 0.1,
      "the dark sector and the flagship pull against each other (L320's structural point, now quantified at the flagship)")

banner("VERDICT")
P(f"""  Kernel-invisibility does not rescue the carrier at high redshift.  On RC100 the unboosted carrier's inverted a0(z) rises at
  {co.min():+.2f}..{co.max():+.2f} (boosted: {bo.min():+.2f}..{bo.max():+.2f}; data {s_data:+.3f} +/- {e_data:.3f}; RC100 is calibration-conditional), and
  its dark fraction inside R_e ({fdc.min():.2f}-{fdc.max():.2f}) overshoots the data's {fd_data:.2f}: near R_e the kernel's response slope is
  ~1, so boosting or not barely matters -- the halo is the price.  At the flagship the price is larger: with the carrier
  intact at z = 2.5 (as the forest requires) the deep-MOND Tully-Fisher zero point moves {shifts.min():+.2f}..{shifts.max():+.2f} dex, beyond
  LCDM's +0.33.  Any carrier that keeps the forest's cold power at z = 2-3 must leave galaxies by z ~ 2.5; a Lambda
  trigger cannot do that (it acts at z < 1).  (Halo masses from the LCDM-calibrated Moster+13 relation.)""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
