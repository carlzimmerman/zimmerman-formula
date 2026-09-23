#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L322 -- THE ADDITIVE NEAR-WINDOW, PINNED DOWN; RC100 UNDER ADDITIVE COUPLING; AND A LOOK-ELSEWHERE-CONTROLLED COINCIDENCE TEST.

L321: under ADDITIVE coupling (a metric-coupled carrier that does not source the MOND field) the Lambda-triggered carrier
passes every galaxy host; X-COP clusters overshoot at the kicks S_8 allows (1.34 at 1000 km/s) and match only at 2000 km/s,
where S_8 = 0.72.  A near-window at v_k ~ 1500-1800 km/s depends on thresholds.  This lane pins it down with thresholds
DECLARED BEFORE THE SCAN, then asks RC100 under the same coupling, then -- only if a window exists -- tests whether its
parameters coincide with a framework scale, with the look-elsewhere count stated.

PRE-DECLARED THRESHOLDS
  S_8   strict: KiDS-Legacy 0.815 +/- 0.016, floor 0.767 (3 sigma, as L168/L319 used)
        alternative: DES-Y3 x KiDS-1000 joint 0.790 (+0.018/-0.014), floor 0.748 (3 sigma, lower error)
  X-COP strict: median M_dyn/M_HSE within 20%
        alternative: M_HSE corrected for X-COP's measured non-thermal pressure at R500 (Eckert+2019, ~6%), then within 20%
  galaxies: shift of predicted g_obs at the gate <= 0.06 dex (RAR scatter), as L321
  RC100: the additive-coupling d log a0/dz and median f_DM(<R_e), against -0.112 +/- 0.062 and 0.29 (L320 machinery)
COINCIDENCE TEST (run only if a window exists; the candidate list is fixed here, before the numbers):
  the window's decay rate today Gamma_0 against {H_0, H_Lambda, a0/c, sqrt(G rho_Lambda)} x {1/4, 1/3, 1/2, 1, 2, 3, 4} and
  the window's kick v_k against {(a0 G M_b)^(1/4) of an X-COP cluster, sigma(R500), c H_Lambda/Z-type velocities ...}: a
  match counts only if it falls inside the window AND the chance rate of a random candidate doing so (fraction of the 28
  rate candidates or of the velocity candidates landing in the window by construction width) is reported with it.
MUTATE=1 swaps additive for universal coupling in the galaxy gate: G1 must then FAIL (rc = 1).

Run from the repository root:  python3 real_research/dark_sector_2026/L322_additive_window_and_coincidence_test.py
"""
import os, sys, json, math, time, warnings, io, contextlib
import numpy as np
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*encountered in matmul")

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L322_additive_window_and_coincidence_test"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L322", "mutate": MUTATE, "checks": {}, "numbers": {}}


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
# L321's machinery (functions, X-COP loading), executed without its gates
_src = open(os.path.join(HERE, "L321_carrier_z0_retention_gate.py")).read()
_top = _src.split("# ============================================================================================ controls")[0]
_top = _top.split("P(__doc__)", 1)[1]
L = {"__name__": "l321", "__file__": os.path.join(HERE, "L321_carrier_z0_retention_gate.py"), "HERE": HERE,
     "MUTATE": False, "P": (lambda *a: None), "banner": (lambda t: None), "json": json, "os": os, "math": math, "np": np,
     "time": time, "T0": T0, "CH": [], "OUT": {"numbers": {}}, "check": (lambda *a, **k: True), "SLUG": "l321"}
exec("import os, sys, json, math, time\nimport numpy as np\n" + _top, L)
retained, gal_shift, cl_ratio, CL, GAL = L["retained"], L["gal_shift"], L["cl_ratio"], L["CL"], L["GAL"]
hernquist, c200_dm14, GE_GAL, GE_CL = L["hernquist"], L["c200_dm14"], L["GE_GAL"], L["GE_CL"]
P(f"  L321 machinery loaded: {len(CL)} X-COP clusters, hosts {list(GAL)}")

# L319's solver for S_8
_s19 = open(os.path.join(HERE, "L319_lambda_triggered_kicked_decay.py")).read().split(
    "# ============================================================================================ controls")[0]
G19 = {"__name__": "l319", "__file__": os.path.join(HERE, "L319_lambda_triggered_kicked_decay.py")}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_s19, G19)
    LC19 = G19["run"](np.ones(G19["N_A"]), 0.0)

S8_STRICT, S8_ALT = 0.767, 0.748
NT_R500 = 0.06
coupling_gal = "universal" if MUTATE else "additive"
VKS = [1100.0, 1200.0, 1300.0, 1400.0, 1500.0, 1600.0, 1700.0, 1800.0, 1900.0]
FDS = [0.8, 0.9]
cl_ref = CL[int(np.argmin([abs(math.log10(cl["M200"] / 1e15)) for cl in CL]))]
cl_mass_fn = (lambda x, cl=cl_ref: cl["Mb"] * np.clip(np.asarray(x, dtype=float) / cl["R500"], 0, 1))

# ============================================================================================ W1 the scan
banner("W1  THE ADDITIVE SCAN: galaxies, X-COP and S_8 per (f_d(0), v_k), p = 2")
rows = []
for fd in FDS:
    with contextlib.redirect_stdout(io.StringIO()):
        sv, g0 = G19["surv_triggered"](fd, 2)
    for vk in VKS:
        with contextlib.redirect_stdout(io.StringIO()):
            s8 = float(G19["S8_of"](G19["T2"](G19["run"](sv, vk), LC19, 0.0)))
        gal = {}
        for k, hst in GAL.items():
            e, _ = retained(hernquist(hst["Mb"], hst["a"]), hst["M200"], c200_dm14(hst["M200"]), hst["rg"], GE_GAL,
                            coupling_gal, vk, fd)
            gal[k] = gal_shift(hst, e, coupling_gal)
        ecl, _ = retained(cl_mass_fn, cl_ref["M200"], cl_ref["c"], cl_ref["R500"], GE_CL, "additive", vk, fd,
                          rhoc=cl_ref["rhoc"])
        rat = np.array([cl_ratio(cl, ecl, "additive") for cl in CL])
        med, med_nt = float(np.median(rat)), float(np.median(rat * (1 - NT_R500)))
        row = dict(fd=fd, vk=vk, S8=s8, gal=gal, eps_cl=float(ecl), cl_ratio=med, cl_ratio_nt=med_nt,
                   gal_ok=all(v <= 0.06 for v in gal.values()),
                   strict=bool(s8 >= S8_STRICT and abs(med - 1) <= 0.2 and all(v <= 0.06 for v in gal.values())),
                   alt=bool(s8 >= S8_ALT and abs(med_nt - 1) <= 0.2 and all(v <= 0.06 for v in gal.values())),
                   Gamma0_over_H0=float(g0 * (G19["omega_L"](1.0) / G19["omega_L"](1.0)) ** 2 / G19["H0"]))
        rows.append(row)
        P(f"    f_d {fd} v_k {vk:6.0f}: S_8 {s8:.3f}; X-COP M_dyn/M_HSE {med:.2f} (NT-corrected {med_nt:.2f}); "
          f"galaxies max +{max(gal.values()):.3f} dex  -> strict {'WINDOW' if row['strict'] else '-'}, alt {'WINDOW' if row['alt'] else '-'}")
OUT["numbers"]["scan"] = rows
strict_w = [(r["fd"], r["vk"]) for r in rows if r["strict"]]
alt_w = [(r["fd"], r["vk"]) for r in rows if r["alt"]]
check("G1 under the ADDITIVE coupling every galaxy host stays within the RAR scatter at every scanned kick",
      f"max shift {max(max(r['gal'].values()) for r in rows):.3f} dex", all(r["gal_ok"] for r in rows),
      "the metric-coupled carrier is invisible to galaxy dynamics once kicked out; a MOND-sourcing one is not (L321)")
check("W1 the window under the STRICT pre-declared thresholds (KiDS-Legacy 3 sigma, X-COP HSE within 20%)",
      f"strict window cells: {strict_w or 'none'}", True, "reported either way", load_bearing=False)
check("W2 the window under the ALTERNATIVE pre-declared thresholds (DES-Y3 x KiDS-1000 3 sigma; X-COP corrected for the "
      "measured 6% non-thermal support)", f"alternative window cells: {alt_w or 'none'}", True, "reported either way",
      load_bearing=False)

# ============================================================================================ W3 RC100 additive
banner("W3  RC100 UNDER ADDITIVE COUPLING (L320's machinery; the carrier is intact at z >~ 1)")
import csv
REPO = os.path.dirname(os.path.dirname(HERE))
G, MSUN, KPC, MPC = 6.6743e-11, 1.98892e30, 3.0856775814913673e19, 3.0856775814913673e22
hh = 0.6736; H0s = 100 * hh * 1e3 / MPC; Om, OL = 0.3153, 0.6847
a0s = 9.3619e-11
nu = lambda x: 1.0 / (1.0 - np.exp(-np.sqrt(np.clip(x, 1e-12, None))))
def rho_crit(z): return 3 * (H0s * math.sqrt(Om * (1 + z) ** 3 + OL)) ** 2 / (8 * math.pi * G)
def mstar_over_mh(Mh, z):
    zz = z / (1 + z); M1 = 10 ** (11.590 + 1.195 * zz); N = 0.0351 - 0.0247 * zz
    return 2 * N / ((Mh / M1) ** -(1.376 - 0.826 * zz) + (Mh / M1) ** (0.608 + 0.329 * zz))
def halo_mass(Ms, z):
    lg = np.linspace(9.5, 15.5, 6001); Mh = 10 ** lg
    return float(10 ** np.interp(math.log10(Ms), np.log10(Mh * mstar_over_mh(Mh, z)), lg))
def g_nfw(Mh, z, r):
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z
    c = 10 ** (a + b * math.log10(Mh / (1e12 / hh)))
    r200 = (3 * Mh * MSUN / (4 * math.pi * 200 * rho_crit(z))) ** (1 / 3); rs = r200 / c
    m = lambda x: math.log(1 + x) - x / (1 + x)
    return G * Mh * MSUN * m(r / rs) / m(c) / r ** 2
def invert(f, go):
    return math.log10((1 - f) * go / math.log(1 / f) ** 2) if 0.02 < f < 0.98 else float("nan")
rc = list(csv.DictReader(open(os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3.csv"))))
gal100 = []
for r in rc:
    try:
        z, lMb, Re, fdm, gg = (float(r[k]) for k in ("z", "logMbar_Msun", "Re_kpc", "fDM_within_Re", "g_Re_ms2"))
    except ValueError:
        continue
    if all(np.isfinite([z, lMb, Re, fdm, gg])):
        gal100.append(dict(z=z, Mb=10 ** lMb, Re=Re * KPC, fdm=fdm, go=gg))
zs = np.array([g["z"] for g in gal100])
def surv_z(z, fd):
    with contextlib.redirect_stdout(io.StringIO()):
        sv, _ = G19["surv_triggered"](fd, 2)
    return float(np.interp(1 / (1 + z), G19["a_grid"], sv))
def slope(las):
    m = np.isfinite(las); s = float(np.polyfit(zs[m], las[m], 1)[0]); rng = np.random.default_rng(3)
    e = float(np.std([np.polyfit(zs[m][k], las[m][k], 1)[0] for k in (rng.integers(0, m.sum(), m.sum()) for _ in range(1500))]))
    return s, e
la_d = np.array([invert(g["fdm"], g["go"]) for g in gal100]); s_d, e_d = slope(la_d)
rc_rows = []
for xi_geo in (1.0, 1.3):
    for fd in FDS:
        las, fds = [], []
        for g in gal100:
            gb = G * 0.5 * g["Mb"] * MSUN * xi_geo / g["Re"] ** 2
            Mh = halo_mass(g["Mb"] / (1 + 0.5 * ((1 + g["z"]) / 2) ** 2), g["z"])
            gc = surv_z(g["z"], fd) * g_nfw(Mh, g["z"], g["Re"])            # parents surviving at z (daughters escaped)
            go = nu(gb / a0s) * gb + gc                                      # ADDITIVE
            f = 1 - gb / go; fds.append(f); las.append(invert(f, go))
        s, e = slope(np.array(las))
        rc_rows.append(dict(xi_geo=xi_geo, fd=fd, slope=s, median_fdm=float(np.nanmedian(fds)),
                            sigma_vs_data=(s - s_d) / e_d))
        P(f"    xi_geo {xi_geo} f_d {fd}: additive carrier slope {s:+.3f}, median f_DM {np.nanmedian(fds):.2f}  "
          f"(data {s_d:+.3f} +/- {e_d:.3f}, f_DM {np.median([g['fdm'] for g in gal100]):.2f}) -> {(s - s_d)/e_d:.1f} sigma")
OUT["numbers"]["rc100_additive"] = rc_rows
zmin = min(r["sigma_vs_data"] for r in rc_rows); zmax = max(r["sigma_vs_data"] for r in rc_rows)
check("W3 RC100 under additive coupling: the carrier's inverted-a0 trend against the data (the price, recomputed)",
      f"{zmin:.1f}-{zmax:.1f} sigma; median f_DM {min(r['median_fdm'] for r in rc_rows):.2f}-{max(r['median_fdm'] for r in rc_rows):.2f} "
      f"vs 0.29", True, "reported either way", load_bearing=False)

# ============================================================================================ W4 coincidence
banner("W4  THE COINCIDENCE TEST (pre-declared candidates; runs only if a window exists)")
window = alt_w or strict_w
if not window:
    P("    no window under either threshold set: there is no window parameter for a coincidence to explain -- NOT RUN.")
    OUT["numbers"]["coincidence"] = "not run: no window"
else:
    C_KMS = 299792.458
    HL = H0s * math.sqrt(OL); rhoL = OL * rho_crit(0.0)
    # (1) the decay rate today, over the window's f_d(0) range, in units of H0
    g_win = sorted(set(round(r["Gamma0_over_H0"], 6) for r in rows if (r["fd"], r["vk"]) in window))
    glo, ghi = min(g_win) * 0.97, max(g_win) * 1.03
    rate_base = {"H0": 1.0, "H_Lambda": math.sqrt(OL), "a0/c": a0s / 2.99792458e8 / H0s,
                 "sqrt(G rho_Lambda)": math.sqrt(G * rhoL) / H0s}
    mults = [0.25, 1 / 3, 0.5, 1.0, 2.0, 3.0, 4.0]
    rc_ = {f"{m:.3g} x {k}": m * v for k, v in rate_base.items() for m in mults}
    rhits = {k: v for k, v in rc_.items() if glo <= v <= ghi}
    Wr = math.log(max(rc_.values()) / min(rc_.values())); wr = math.log(ghi / glo)
    p_rate = 1 - (1 - wr / Wr) ** len(rc_)
    # (2) the kick, over the window's v_k range
    vks = sorted(set(v for _, v in window)); vlo, vhi = min(vks) - 50, max(vks) + 50
    vc = {f"(a0 G M_b)^1/4 {cl['name']}": (a0s * G * cl["Mb"] * MSUN) ** 0.25 / 1e3 for cl in CL}
    vc.update({f"sigma_1D(R500) {cl['name']}": math.sqrt(G * cl["Mhse"] * MSUN / (cl["R500"] * KPC) / 2) / 1e3 for cl in CL})
    vc.update({"sqrt(a0 x 1 Mpc)": math.sqrt(a0s * MPC) / 1e3, "c/Z": C_KMS / (2 * math.sqrt(8 * math.pi / 3)),
               "sqrt(a0 c/H_Lambda)": math.sqrt(a0s * 2.99792458e8 / HL) / 1e3})
    vhits = {k: v for k, v in vc.items() if vlo <= v <= vhi}
    Wv = math.log(max(vc.values()) / min(vc.values())); wv = math.log(vhi / vlo)
    p_vel = 1 - (1 - wv / Wv) ** len(vc)
    OUT["numbers"]["coincidence"] = dict(rate_window_H0=[glo, ghi], rate_candidates=rc_, rate_hits=rhits, p_rate_chance=p_rate,
                                         kick_window_kms=[vlo, vhi], kick_candidates=vc, kick_hits=vhits, p_kick_chance=p_vel)
    P(f"    decay rate today in the window: Gamma_0/H0 in [{glo:.3f}, {ghi:.3f}]")
    for k, v in rc_.items():
        if k in rhits:
            P(f"      HIT  {k:28s} = {v:.3f} H0")
    P(f"      {len(rhits)}/{len(rc_)} rate candidates in the window; chance that >= 1 of {len(rc_)} log-uniform candidates lands there: {p_rate:.2f}")
    P(f"    kick in the window: [{vlo:.0f}, {vhi:.0f}] km/s")
    for k, v in vc.items():
        if k in vhits:
            P(f"      HIT  {k:34s} = {v:.0f} km/s")
    P(f"      {len(vhits)}/{len(vc)} velocity candidates in the window; chance rate for >= 1: {p_vel:.2f}")
    check("W4 a coincidence counts only if the chance probability is small (< 0.05); stated for the rate and the kick",
          f"p_rate = {p_rate:.2f} ({len(rhits)} hits); p_kick = {p_vel:.2f} ({len(vhits)} hits)", True,
          "reported either way: a hit with a large chance probability is not evidence", load_bearing=False)

# ============================================================================================ verdict
banner("VERDICT")
P(f"""  ADDITIVE coupling (a metric-coupled carrier) is the only reading that survives galaxies (L321, G1 here).
  Window cells -- strict: {strict_w or 'none'}; alternative: {alt_w or 'none'}.
  RC100 under additive coupling: {zmin:.1f}-{zmax:.1f} sigma against the data's trend.
  A coincidence is worth something only if the window is narrow and the chance rate is small; both are printed above.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time()-T0:.0f}s]")
sys.exit(0 if n_fail == 0 else 1)
