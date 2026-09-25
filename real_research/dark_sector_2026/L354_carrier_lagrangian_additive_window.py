#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L354 -- THE LAMBDA-TRIGGERED CARRIER UNDER THE LAGRANGIAN KERNEL-INVISIBLE COUPLING (L353): is there a window when the
carrier feels NEWTONIAN gravity only, as action = reaction requires?

WHY.  L345: under C-H/K's own (universal) coupling the carrier has no window.  L322's alternative window (f_d = 0.9,
v_k = 1300-1400 km/s) exists only under L321's "additive" coupling, in which the carrier's orbits feel the baryons' full
MOND field while its own field is unboosted.  L353 (N2) shows that law has no action (the response matrix is asymmetric;
momentum balance fails by ~r/r_M), and builds the Lagrangian kernel-invisible coupling: the kernel reads baryons only,
the carrier's field is Newtonian and unboosted, and the carrier FEELS only the Newtonian field of all matter.  This lane
re-runs the carrier's z = 0 gates with that force law.

THE ONE CHANGE (L321's machinery loaded unedited, as L345 does):
  * the carrier's orbits -- its pre-decay Jeans dispersion and its daughters' post-decay binding and phase mixing -- use
    g_carrier = g_N,b + g_N,c  (Newtonian, no MOND boost, no external-field rule);
  * the observables are what baryons feel: galaxies' g_obs and X-COP's hydrostatic M_dyn from g = nu(|g_N,b|_eff/a0) g_N,b
    + g_N,c (L321's additive observable, which IS the Lagrangian construction's metric field).
  Everything else is L321/L345's: X-COP's 12 clusters, the three galaxy hosts and their 0.06-dex RAR gate, L319's S_8
  solver, L340's kernel nu_mono, both footings, L322's pre-declared thresholds (strict: |M_dyn/M_HSE - 1| <= 0.2 and
  S_8 >= 0.767; alternative: after X-COP's measured 6% non-thermal support and S_8 >= 0.748).

CHECKS
  C1 CONTROL: with L321's (non-Lagrangian) additive orbits, the machinery reproduces L322's alternative window cells at
     f_d = 0.9 (v_k = 1300, 1400 km/s) -- the scan is L322's.
  C2 (documentary) what the Newtonian force law does to retention: the retained carrier fraction in the reference cluster
     and in the Milky Way under Newtonian vs additive orbits.
  W1 THE WINDOW under the Lagrangian coupling, both threshold sets, both footings: the cells passing X-COP, S_8 and the
     galaxy gate together.
  MUTATE=1 replaces the carrier's orbits by C-H/K's universal coupling (L345's case, carrier boosted and feeling the MOND
  field): W1's finding must flip (rc = 1).

SCOPE.  The carrier model is L319's (Lambda-triggered decay Gamma ~ Omega_Lambda(a)^2, kicked daughters) and its halo
input is L321's (the LCDM-like cold halo, (1 - f_b) x the host's NFW).  S_8 is L319's GR-growth value (a necessary
condition; the web's growth with the construction is not computed).  The construction's own cost -- a dark-sector
equivalence-principle violation in clusters (L353 N4) -- is not tested here.

Run from the repository root:  python3 real_research/dark_sector_2026/L354_carrier_lagrangian_additive_window.py
"""
import os, sys, json, math, time, warnings, io, contextlib
import numpy as np
from scipy.optimize import brentq
warnings.filterwarnings("ignore", category=RuntimeWarning)

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L354_carrier_lagrangian_additive_window"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L354", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
ORBIT = "universal" if MUTATE else "newtonian"
OBS = "universal" if MUTATE else "additive"
if MUTATE: P("\n  *** MUTATE=1: carrier orbits and observables under C-H/K's universal coupling (L345's case); W1 must flip ***")

# ---------------------------------------------------------------------------------- L321's machinery, unedited (as L345)
_src = open(os.path.join(HERE, "L321_carrier_z0_retention_gate.py")).read()
_top = _src.split("# ============================================================================================ controls")[0]
_top = _top.split("P(__doc__)", 1)[1]
Lm = {"__name__": "l321", "__file__": os.path.join(HERE, "L321_carrier_z0_retention_gate.py"), "HERE": HERE,
      "MUTATE": False, "P": (lambda *a: None), "banner": (lambda t: None), "json": json, "os": os, "math": math, "np": np,
      "time": time, "T0": T0, "CH": [], "OUT": {"numbers": {}}, "check": (lambda *a, **k: True), "SLUG": "l321"}
exec("import os, sys, json, math, time\nimport numpy as np\n" + _top, Lm)
KPC_M = Lm["KPC_M"]


def h_rar(y):
    y = np.asarray(y, float)
    return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)


def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)


Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P))
LYG = np.linspace(-12, 12, 240001); YG = 10 ** LYG
DH = np.maximum(dh_rar(YG), 0.05 * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])


def nu_mono(y):                                                       # L340's monotone kernel (as L345)
    y = np.maximum(np.asarray(y, float), 1e-12)
    return 1.0 + np.interp(np.log10(y), LYG, H_MONO) / y


Lm["nu"] = nu_mono
_gravity_l321 = Lm["gravity"]


def gravity_ext(gb, gc, ge, coupling):
    """L321's gravity plus the Lagrangian carrier force law 'newtonian' (L353 N1/N2: g = g_N,b + g_N,c, no EFE rule)."""
    if coupling == "newtonian":
        return gb + gc
    return _gravity_l321(gb, gc, ge, coupling)


Lm["gravity"] = gravity_ext                                          # retained()/potential() look it up at call time
FOOT = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
retained, gal_shift, cl_ratio, CL, GAL = Lm["retained"], Lm["gal_shift"], Lm["cl_ratio"], Lm["CL"], Lm["GAL"]
hernquist, c200_dm14, GE_GAL, GE_CL = Lm["hernquist"], Lm["c200_dm14"], Lm["GE_GAL"], Lm["GE_CL"]
cl_ref = CL[int(np.argmin([abs(math.log10(cl["M200"] / 1e15)) for cl in CL]))]
cl_mass_fn = (lambda x, cl=cl_ref: cl["Mb"] * np.clip(np.asarray(x, dtype=float) / cl["R500"], 0, 1))
P(f"\n  L321 machinery loaded ({len(CL)} X-COP clusters, reference {cl_ref['name']}); kernel nu_mono; carrier orbits '{ORBIT}', "
  f"observables '{OBS}'")
NT = 0.06
S8_STRICT, S8_ALT = 0.767, 0.748
FDS = [0.8, 0.9, 0.95]
VKS = [800.0, 1000.0, 1200.0, 1400.0, 1600.0, 2000.0, 2500.0]

# ---------------------------------------------------------------------------------- L319's S_8 solver (unchanged)
_s19 = open(os.path.join(HERE, "L319_lambda_triggered_kicked_decay.py")).read().split(
    "# ============================================================================================ controls")[0]
G19 = {"__name__": "l319", "__file__": os.path.join(HERE, "L319_lambda_triggered_kicked_decay.py")}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_s19, G19)
    LC19 = G19["run"](np.ones(G19["N_A"]), 0.0)
S8 = {}
for fd in FDS:
    with contextlib.redirect_stdout(io.StringIO()):
        sv, _ = G19["surv_triggered"](fd, 2)
    for vk in VKS:
        with contextlib.redirect_stdout(io.StringIO()):
            S8[(fd, vk)] = float(G19["S8_of"](G19["T2"](G19["run"](sv, vk), LC19, 0.0)))
P("  S_8 (L319 solver): " + "; ".join(f"f_d {fd}: " + ", ".join(f"{vk:.0f}:{S8[(fd, vk)]:.3f}" for vk in VKS) for fd in FDS)
  + f"   [{time.time() - T0:.0f}s]")
OUT["numbers"]["S8"] = {f"{fd}_{vk:.0f}": v for (fd, vk), v in S8.items()}


def cluster_cells(orbit, obs, foot, fd):
    Lm["A0"] = FOOT[foot] * KPC_M / 1e6
    cells = []
    for vk in VKS:
        ecl, _ = retained(cl_mass_fn, cl_ref["M200"], cl_ref["c"], cl_ref["R500"], GE_CL, orbit, vk, fd, rhoc=cl_ref["rhoc"])
        med = float(np.median([cl_ratio(cl, ecl, obs) for cl in CL]))
        cells.append(dict(vk=vk, eps=float(ecl), ratio=med, ratio_nt=med * (1 - NT)))
    return cells


def galaxy_shift(orbit, obs, foot, fd, vk):
    Lm["A0"] = FOOT[foot] * KPC_M / 1e6
    out = {}
    for kh, hst in GAL.items():
        e, _ = retained(hernquist(hst["Mb"], hst["a"]), hst["M200"], c200_dm14(hst["M200"]), hst["rg"], GE_GAL, orbit, vk, fd)
        out[kh] = gal_shift(hst, e, obs)
    return out


def window(orbit, obs, foots=("canonical", "alt"), fds=FDS, verbose=True):
    win = {"strict": [], "alt": []}; table = {}
    for foot in foots:
        for fd in fds:
            cells = cluster_cells(orbit, obs, foot, fd)
            table[(foot, fd)] = cells
            if verbose:
                P(f"    {foot:9s} f_d {fd:4.2f}: " + "  ".join(f"{c['vk']:.0f}:{c['ratio_nt']:.2f}" for c in cells)
                  + f"   [X-COP NT-corrected median; {time.time() - T0:.0f}s]")
            for c in cells:
                s8 = S8[(fd, c["vk"])]
                ok_cl = {"strict": abs(c["ratio"] - 1) <= 0.2, "alt": abs(c["ratio_nt"] - 1) <= 0.2}
                ok_s8 = {"strict": s8 >= S8_STRICT, "alt": s8 >= S8_ALT}
                if any(ok_cl[t] and ok_s8[t] for t in ("strict", "alt")):
                    gal = galaxy_shift(orbit, obs, foot, fd, c["vk"])
                    ok_g = max(gal.values()) <= 0.06
                    for t in ("strict", "alt"):
                        if ok_cl[t] and ok_s8[t] and ok_g:
                            win[t].append((foot, fd, c["vk"]))
                    if verbose:
                        P(f"      candidate {foot} f_d {fd} v_k {c['vk']:.0f}: X-COP {c['ratio']:.2f} (NT {c['ratio_nt']:.2f}), "
                          f"S_8 {s8:.3f}, galaxies max {max(gal.values()):+.3f} dex -> {'WINDOW' if ok_g else 'galaxies fail'}")
    return win, table


# ============================================================================================ C1 control
banner("C1  CONTROL: L321's (non-Lagrangian) additive orbits give L322/L345's alternative window (f_d 0.8-0.9, v_k ~1300-1500)")
if not MUTATE:
    win_add, tab_add = window("additive", "additive", foots=("canonical",), fds=[0.8, 0.9], verbose=True)
    c1 = any(1200.0 <= vk <= 1600.0 for (_, _, vk) in win_add["alt"])
    OUT["numbers"]["C1"] = {"alt_window": win_add["alt"], "strict_window": win_add["strict"]}
    check("C1 the machinery with L321's additive orbits reproduces an alternative window at v_k ~ 1200-1600 km/s "
          "(L322: f_d 0.9, 1300-1400 with nu_RAR; L345 MUTATE: f_d 0.8, 1500 with nu_mono)", f"alt window {win_add['alt']}", c1,
          "the scan below differs from this control only in the carrier's force law", load_bearing=False)
else:
    P("    (skipped under MUTATE)")

# ============================================================================================ C2 what the force law does
banner("C2  RETENTION UNDER THE NEWTONIAN FORCE LAW vs L321's ADDITIVE ORBITS (canonical, f_d = 0.9)")
Lm["A0"] = FOOT["canonical"] * KPC_M / 1e6
c2rows = []
for vk in (1000.0, 1500.0, 2000.0):
    en, _ = retained(cl_mass_fn, cl_ref["M200"], cl_ref["c"], cl_ref["R500"], GE_CL, "newtonian", vk, 0.9, rhoc=cl_ref["rhoc"])
    ea, _ = retained(cl_mass_fn, cl_ref["M200"], cl_ref["c"], cl_ref["R500"], GE_CL, "additive", vk, 0.9, rhoc=cl_ref["rhoc"])
    mw = GAL["Milky Way"]
    gn, _ = retained(hernquist(mw["Mb"], mw["a"]), mw["M200"], c200_dm14(mw["M200"]), mw["rg"], GE_GAL, "newtonian", vk, 0.9)
    ga, _ = retained(hernquist(mw["Mb"], mw["a"]), mw["M200"], c200_dm14(mw["M200"]), mw["rg"], GE_GAL, "additive", vk, 0.9)
    c2rows.append((vk, en, ea, gn, ga))
    P(f"    v_k {vk:.0f}: cluster retained fraction newtonian {en:.3f} vs additive {ea:.3f};  Milky Way (30 kpc) {gn:.3f} vs {ga:.3f}")
OUT["numbers"]["C2"] = [dict(zip(("vk", "cluster_newtonian", "cluster_additive", "MW_newtonian", "MW_additive"), r_)) for r_ in c2rows]
check("C2 (documentary) the Newtonian force law retains less carrier than L321's additive orbits, in clusters and galaxies",
      "; ".join(f"{r_[0]:.0f}: cl {r_[1]:.2f}/{r_[2]:.2f}, MW {r_[3]:.2f}/{r_[4]:.2f}" for r_ in c2rows),
      all(r_[1] <= r_[2] + 1e-3 and r_[3] <= r_[4] + 1e-3 for r_ in c2rows), load_bearing=False)

# ============================================================================================ W1 the window
banner(f"W1  THE WINDOW with carrier orbits '{ORBIT}' and observables '{OBS}' (both footings, f_d 0.8-0.95, v_k 800-2500)")
win, tab = window(ORBIT, OBS)
OUT["numbers"]["W1"] = {"window": win, "table": {f"{f_}_{fd}": v for (f_, fd), v in tab.items()}}
has = bool(win["alt"] or win["strict"])
P(f"    strict window: {win['strict'] or 'none'};  alternative window: {win['alt'] or 'none'}")
check("W1 under the Lagrangian kernel-invisible coupling the Lambda-triggered carrier HAS a window (X-COP, S_8 and galaxies "
      "together, under at least one pre-declared threshold set)", f"strict {win['strict'] or 'none'}; alt {win['alt'] or 'none'}",
      has, "the two live fronts are compatible through L353's construction if this passes")

banner("VERDICT")
P(f"""  With the carrier's orbits under the force law that action = reaction requires (Newtonian, L353) and the observables
  from the construction's metric field, the Lambda-triggered carrier's z = 0 window is: strict {win['strict'] or 'none'};
  alternative {win['alt'] or 'none'}.  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
sys.exit(0 if n_fail == 0 else 1)
