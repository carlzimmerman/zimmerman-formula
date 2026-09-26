#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
AT3 -- THE ACCELERATION-TRIGGERED CARRIER THROUGH EVERY GATE: one vacuum-gated threshold on the kernel's argument, a slow
kick, and L372's uniform mode.  Galaxies, X-COP, KiDS, Harvey, S_8, the forest on its observable, and the flagship at
every redshift from 0.5 to 2.5; cosmic shear reported.

WHY.  AT1 built the acceleration trigger: the carrier converts where the kernel's argument y_b exceeds y_v.  With
y_v <= 0.1 and v_A >= 600 km/s it keeps the flagship flat at every redshift.  AT2 showed that on the forest's own
observable this high-z clearing is cheap.  What neither scored is z <= 1, where the record's windows live.  L372 (a
uniform mode U plus a slow vacuum-gated density mode G) passes forest, S_8, X-COP, galaxies, KiDS and Harvey on the
alternative set.  But it keeps the carrier in galaxies at z ~ 2.5, which is GP5's failure.  This lane puts the
acceleration trigger in G's place.

THE CONSTRUCTION (a construction: the rules are put in by hand, like every decay channel on the record; the carrier is a
state of the framework's own field, not a new particle, and the mass is still required).
  Mode A converts the carrier where y_b >= y_v,eff(z) = y_v0 [Omega_L0 / Omega_L(z)]^q = y_v0 E(z)^(2q).  This is L359's
  vacuum gate, now on the kernel's argument: the threshold is low today and rises into the matter era.  The conversion is
  one-shot on entry (the steady-state loss cone, AT1), with kick v_A.  q is FIXED by y_v,eff(2.5) = 0.1, AT1's flagship
  edge, so the flagship at z = 2.5 is kept by construction; y_v0 sets how far out galaxies are cleared today.  The
  ungated trigger (q = 0, y_v0 = 0.1) is one of the cells.
  Mode U is L372's uniform mode: L319's rate law, fraction f_U(0), v_U = 3000 km/s.  The two modes' retained fractions
  multiply (L372's stated approximation).
METHOD (machinery loaded unedited; AT1's retention with decay on entry):
  * galaxies: L321's three hosts at z = 0: retention inside each gate radius, L321's gal_shift on both footings, <= 0.06 dex.
  * X-COP: the reference cluster's retention with its trigger radius from its own baryon profile, then L321's cl_ratio over
    the 12 clusters.  Strict, or with X-COP's 6% non-thermal support (L354/L372).
  * KiDS-1000, at the common switch cell: L360's switched fit (L352's Gauss-compensated profile plus 2-halo) at
    p = 1, x_c0 = 2.5 (L359's own x_c,eff(0.25)), with the carrier's post-conversion halo from AT1's retention in each lens
    bin.  Gate: Delta chi^2 <= +4 against L352's unswitched base (L360/L364's), both footings.  L355's switch-free
    web-blind fit (<= +9 against isolated MOND, L357/L372's gate) is reported beside it.
  * Harvey+2015: L370's machinery through L372's harvey(), unedited except two inputs.  The carrier profile is processed
    by mode A (retention on entry) and U's uniform factor.  The switch cell is the program's common kernel cell,
    p = 1, x_c0 = 2.5: DE2's linear gate, inside its window, the cell the parallel particle-mesh track re-runs.  L370's
    SWITCH table gains that entry, and SW_DEF is set to it.  Population-mean excess beta <= -0.04 + 2 x 0.07 on all
    three estimators.
  * S_8: L319's solver (one daughter speed per run) on each mode separately, A's escaped bias-weighted history at v_A
    and U's survival at v_U, combined additively in the power deficit: S_8^2 = S_8,A^2 + S_8,U^2 - S_8,LCDM^2.  The
    cross term of the exact square is positive, so the additive estimate over-counts the suppression (conservative for
    the floors); C3 measures its error at a common speed.  The single-run bounds (every decay at v_U; every decay at v_A)
    are reported.  Floors are 0.752 strict (PAPER34's correction of the record's 0.767, which used the upper error) and
    0.748 alternative.
  * the forest: on its observable (AT2's run() in L365's box, L365's rule) for the cell W1 names; L319's matter proxy is
    reported (AT2: the wrong yardstick for halo-internal clearing).
  * the flagship at z = 0.5, 1, 1.5, 2, 2.5 (GP5's definition, AT1's flagship_rows).  U is left out at high z, where
    f_U(z >= 0.5) is small; it only removes carrier, so the A-only flagship is conservative.
  * cosmic shear: L364's R = T^2 + 2 r_x T s + s^2 <= 1.2 on k = 0.1-1 h/Mpc, both footings, at the common kernel cell
    p = 1, x_c0 = 2.5.  Its phantom power s^2 and r_x are computed with L363's machinery exactly as L364 does (GP3's
    mock at z = 0.5, L364's seed), and C4 reproduces L364's committed numbers first.  T(k) at z = 0.5 comes from the
    solver with every decay at v_A (U's daughters would smooth more, so this is conservative for the gate).  L364's two
    committed cells are reported beside it.
GRID: y_v0 in {0.003, 0.01, 0.03, 0.1 (q = 0)}, v_A in {600, 800} km/s, f_U(0) in {0, 0.15, 0.25}.  The trigger radii for
  galaxies, X-COP, KiDS and Harvey use the canonical a0 (the alternative footing's are ~9% smaller); the flagship uses each
  footing's own (AT1).
PRE-DECLARED (before the main run).  Directions fixed after an exploratory run of two cells (y_v0 = 0.01 and 0.1 at
  600 km/s, not committed).  There, mode A's free-streaming transfer at z = 0.5 was T(k = 1) ~ 0.85.  A parallel lane's
  uncommitted table (DE3) puts the bound at the common cell near 0.76 / 0.72 (canonical / alt).
  H1: some cell passes every gate except cosmic shear together: the flagship at every redshift, galaxies, X-COP, KiDS,
      Harvey and S_8 on the alternative threshold set, and the forest on its observable.
  H2: cosmic shear at the common kernel cell blocks every H1 cell (R > 1.2 somewhere on k <= 1, on some footing).  This
      trigger removes too little small-scale carrier by z = 0.5 to hand its power to the phantom.
CHECKS
  C1 CONTROL: AT1's committed flagship result is reproduced.  With y_v0 = 0.1, q = 0 and v_A = 600 the z = 2.5 flagship
     row matches AT1's A2 value to 1e-9 dex.
  C2 CONTROL: mode U's retention in X-COP's reference cluster at f_U(0) = 0.25 reproduces L372's committed value (the
     same call, 1e-9).
  C3 CONTROL: the additive S_8 combination at a common speed (600 km/s) matches the solver's joint run within 0.003 and
     errs low (conservative).
  C4 CONTROL: L363's machinery reproduces L364's committed phantom power at its p = 2, x_c0 = 2 cell (canonical), 1e-9.
  C5 CONTROL: with no conversion, this lane's switched-KiDS carrier template reproduces L360's full-carrier template
     (carrier_esd at x_v -> infinity) within 2% in every bin (the density is rebuilt from the enclosed mass).
  W1 = H1.   W2 = H2.   W3 (reported) the full gate table, with cosmic shear at L364's two cells as well.
MUTATE=1: mode A is switched off (y_v -> infinity) in every cell.  The flagship must fail at z = 2.5 (GP5), so W1 must flip
(rc = 1).

Run from the repository root:  python3 real_research/acceleration_trigger_2026/AT3_acceleration_trigger_full_gates.py
"""
import os, sys, json, math, time, io, contextlib, warnings
from concurrent.futures import ThreadPoolExecutor
import numpy as np
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
FAST = os.environ.get("FAST", "0") == "1"                             # smoke test only; never committed
SLUG = "AT3_acceleration_trigger_full_gates"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "AT3", "mutate": MUTATE, "checks": {}, "numbers": {}}
NTH = int(os.environ.get("AT3_THREADS", "8"))
EXPECT = dict(H1=True, H2=True)                                       # set before the main run (docstring)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 116); P(t); P("=" * 116)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: mode A switched off in every cell -- the flagship must fail and W1 must flip ***")

# ------------------------------------------------------------------------------------------------ AT1's head (L357, L320, BK1, AT1's pieces)
PA1 = os.path.join(HERE, "AT1_acceleration_trigger_highz.py")
_sa1 = open(PA1).read()
_head1 = _sa1.split("# ================================================================================================ C1-C3")[0]
_head1 = _head1.replace('P(__doc__.split("CHECKS")[0].strip())', "pass")
_mut, os.environ["MUTATE"] = os.environ.get("MUTATE", "0"), "0"
_fst, os.environ["FAST"] = os.environ.get("FAST", "0"), ("1" if FAST else "0")
A1 = {"__name__": "at1", "__file__": PA1}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_head1, A1)
os.environ["MUTATE"], os.environ["FAST"] = _mut, _fst
L57, Lm = A1["L57"], A1["Lm"]
retained_acc, r_trigger, flagship_rows, F_acc = A1["retained_acc"], A1["r_trigger"], A1["flagship_rows"], A1["F_acc"]
FOOT, A0K, GK, hernquist, nfw21, FB = A1["FOOT"], A1["A0K"], A1["GK"], A1["hernquist"], A1["nfw21"], A1["FB"]
Ez2, RHOC0_KPC, ZG, a_grid, solve_hist, T2_53 = A1["Ez2"], A1["RHOC0_KPC"], A1["ZG"], A1["a_grid"], A1["solve_hist"], A1["T2_53"]
G19 = L57["G19"]
CL, CLREF, cl_ratio, cl_mass_fn, GAL = L57["CL"], L57["CLREF"], L57["cl_ratio"], L57["cl_mass_fn"], L57["GAL"]
M200_KIDS, c200_55, RHOC_ZL, ZL, LOGMS = L57["M200_KIDS"], L57["c200_55"], L57["RHOC_ZL"], L57["ZL"], L57["LOGMS"]
rr55, esd_of_M, MS, Rd55, Rp55, MPCm, KPC_M = L57["rr55"], L57["esd_of_M"], L57["MS"], L57["Rd55"], L57["Rp55"], L57["MPCm"], L57["KPC_M"]
kids_score, c200_z0, RHO_C0 = L57["kids_score"], Lm["c200_dm14"], Lm["RHO_C0"]
_s57 = open(L57["__file__"]).read()
exec(_s57[_s57.index("def gal_eps(pic, xv, vk):"):_s57.index("# the galaxy gate AT the strict forest floor")], L57)
gal_shifts = L57["gal_shifts"]                                        # L357's (L321's gal_shift on both footings)
P(f"  AT1's head loaded (L357 head, L320, BK1, AT1's retention and flagship)   [{time.time()-T0:.0f}s]")
NT, S8_STRICT, S8_ALT = 0.06, 0.752, 0.748
P60 = os.path.join(REPO, "real_research", "g03_audit_2026", "L360_assembled_construction_kids.py")
N60 = {"__name__": "l360", "__file__": P60}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(P60).read().split("BASE = {")[0], N60)
fit_comb60, fit_model60, A052 = N60["fit_comb"], N60["fit_model"], N60["A0"]
BASE60 = {f_: fit_model60(A052[f_], 0.0, "none", True)[0] for f_ in FOOT}
XE_COMMON = round(N60["XE59"][(1.0, 2.5)], 4)                          # L359's own x_c,eff(0.25) at the common cell
assert np.allclose(N60["M200_BINS"], M200_KIDS, rtol=0.01), "L360's and L355's lens hosts differ"   # L360 quotes L355's to 3 digits
P(f"  L360's switched KiDS machinery loaded: common cell x_c,eff(0.25) = {XE_COMMON}; unswitched base chi^2 "
  f"{BASE60['canonical']:.1f}/{BASE60['alt']:.1f}   [{time.time()-T0:.0f}s]")


def tc_switched(profs, scale=1.0):
    """L360's carrier template (projected, annulus ESD at L352's radii) for each lens bin, from a retained-mass profile."""
    out = []
    r_kpc = N60["rr"] / KPC_M
    for b, (pro, ratio_p) in enumerate(profs):
        M200 = N60["M200_BINS"][b]; c = float(c200_55(M200))
        Mn, r200, rs = nfw21(M200, c, RHOC_ZL)
        q = np.interp(np.log(np.clip(r_kpc, pro[0], pro[-1])), np.log(pro), ratio_p)
        Mc = scale * (1 - FB) * Mn(np.minimum(r_kpc, r200)) * q
        rho = np.maximum(np.gradient(Mc, r_kpc), 0.0) / (4 * math.pi * r_kpc ** 2)          # Msun / kpc^3
        M2 = N60["project_M2"](rho * N60["MS"] / KPC_M ** 3)
        out.append(N60["annulus_esd"](lambda R, M2=M2: np.interp(np.log(R), np.log(N60["Rp"]), M2), N60["Rd"][b]))
    return out


def kids_switched(profs, scale=1.0):
    TC = tc_switched(profs, scale)
    return {f_: float(fit_comb60(A052[f_], XE_COMMON, TC, [1.0])[0] - BASE60[f_]) for f_ in FOOT}
A0C = A0K["canonical"]


def q_of(yv0):                                                        # y_v,eff(2.5) = 0.1
    return 0.0 if yv0 >= 0.1 else math.log(0.1 / yv0) / math.log(Ez2(2.5))


def yv_eff(yv0, z):
    if MUTATE: return np.inf
    return yv0 * Ez2(z) ** q_of(yv0)


def fU_of_z(fu0, z):                                                  # L372's
    if fu0 <= 0: return 0.0
    S, _ = G19["surv_triggered"](fu0, 2)
    return float(1 - np.interp(1 / (1 + z), a_grid, S))


def r_v_profile(Mb_fn, yv, a0k=A0C, rmax=1e4):
    """outermost radius [kpc] where the baryons' y_b = G M_b(<r) / (r^2 a0) >= y_v (0 if never; inf if y_v is infinite)."""
    if not np.isfinite(yv): return 0.0
    rr = np.geomspace(0.01, rmax, 20000); yb = GK * Mb_fn(rr) / rr ** 2 / a0k
    ok = np.where(yb >= yv)[0]
    return float(rr[ok[-1]]) if len(ok) else 0.0


def xcop_from_eps(eps):
    """L372's xcop_from_eps: L321's X-COP median at this retention, both footings (sets the shared A0: serial only)."""
    out = {"eps": eps}
    for f_ in FOOT:
        Lm["A0"] = FOOT[f_] * KPC_M / 1e6
        med = float(np.median([cl_ratio(c_, eps, "additive") for c_ in CL]))
        out[f_] = dict(ratio=med, strict=abs(med - 1) <= 0.2, alt=abs(med * (1 - NT) - 1) <= 0.2)
    return out


def a_retention(yv0, vA):
    """mode A's retention for X-COP's reference cluster, L321's three hosts and the four KiDS lens bins."""
    out = {}
    zc = CLREF["z"]; rv = r_v_profile(cl_mass_fn, yv_eff(yv0, zc), rmax=5 * CLREF["R500"])
    out["xcop"] = float(retained_acc(cl_mass_fn, CLREF["M200"], CLREF["c"], [CLREF["R500"]], rv, vA, CLREF["rhoc"], N=12000)[0][0])
    out["rv_xcop"] = rv
    out["gal"], out["rv_gal"] = {}, {}
    for kh, hst in GAL.items():
        Mb_fn = hernquist(hst["Mb"], hst["a"]); rv = r_v_profile(Mb_fn, yv_eff(yv0, 0.0))
        out["gal"][kh] = float(retained_acc(Mb_fn, hst["M200"], float(c200_z0(hst["M200"])), [hst["rg"]], rv, vA, RHO_C0)[0][0])
        out["rv_gal"][kh] = rv
    T, rvs = [], []
    for b in range(4):
        M200 = M200_KIDS[b]; c = float(c200_55(M200))
        Mn, r200, rs = nfw21(M200, c, RHOC_ZL)
        pro = np.geomspace(0.02 * rs, 0.999 * r200, 40)
        Mb_fn = hernquist(1.3 * 10 ** LOGMS[b], 3.0); rv = r_v_profile(Mb_fn, yv_eff(yv0, ZL))
        ratio_p, _ = retained_acc(Mb_fn, M200, c, list(pro), rv, vA, RHOC_ZL, N=8000)
        out.setdefault("kids_prof", []).append((pro, np.asarray(ratio_p)))
        r_kpc = rr55 / KPC_M
        Mc = (1 - FB) * Mn(np.minimum(r_kpc, r200)) * np.interp(np.log(r_kpc), np.log(pro), ratio_p)
        dS = esd_of_M(Mc * MS + 1.0, 1.0)
        T.append(np.interp(Rd55[b], Rp55 / MPCm, dS)); rvs.append(rv)
    out["kidsT"], out["rv_kids"] = T, rvs
    return out


def a_history(yv0, vA, weight="bias", escaped=True):
    """mode A's history with the gated threshold (L357's irreversibility): survival on L319's grid, and F on ZG."""
    Fz = np.array([F_acc(z, yv_eff(yv0, z), vA, A0C, 1.0, weight, escaped) if np.isfinite(yv_eff(yv0, z)) else 0.0 for z in ZG])
    Fz = np.where(Fz < 1e-10, 0.0, Fz)
    Fc = np.maximum.accumulate(Fz[::-1])[::-1]
    return 1 - np.interp(1 / a_grid - 1, ZG, Fc, right=0.0), Fc


# ================================================================================================ C1 control
banner("C1-C2  CONTROLS")
a1j = json.load(open(os.path.join(HERE, "AT1_acceleration_trigger_highz_results.json")))
a1row = [r_ for r_ in a1j["numbers"]["A2"]["0.1|600.0|2.5"]["rows"]]
mine = flagship_rows(2.5, 0.1, 600.0)
dev1 = max(abs(a_["shift"] - b_["shift"]) for a_, b_ in zip(mine, a1row))
check("C1 CONTROL: the ungated cell (y_v0 = 0.1, q = 0, v_A = 600) reproduces AT1's committed z = 2.5 flagship rows (1e-9 dex)",
      f"max |dev| {dev1:.1e} over {len(mine)} rows", dev1 < 1e-9, load_bearing=False)
fu_ref = 0.25
EPS_U = {}
for fu in (0.15, 0.25):
    fz = fU_of_z(fu, CLREF["z"])
    EPS_U[fu] = float(Lm["retained"](cl_mass_fn, CLREF["M200"], CLREF["c"], CLREF["R500"], L57["GE_CL"], "newtonian", 3000.0, fz,
                                     rhoc=CLREF["rhoc"])[0])
l372 = json.load(open(os.path.join(REPO, "real_research", "merger_infall_2026", "L372_gated_slow_kick_carrier_results.json")))
epsU372 = float(l372["numbers"]["eps_U_ref"]["0.25"])
check("C2 CONTROL: mode U's retention in X-COP's reference cluster reproduces L372's committed value at f_U(0) = 0.25 (1e-9)",
      f"AT3 {EPS_U[0.25]:.6f}, L372 {epsU372:.6f}", abs(EPS_U[0.25] - epsU372) < 1e-9, load_bearing=False)
_pro0 = [(np.geomspace(1.0, 5000.0, 40), np.ones(40)) for _ in range(4)]
_mine0 = tc_switched(_pro0); _ref0 = N60["carrier_esd"](float("inf"), "cleared")
dev5 = max(float(np.max(np.abs(np.asarray(a_) / np.asarray(b_) - 1))) for a_, b_ in zip(_mine0, _ref0))
check("C5 CONTROL: with no conversion, this lane's switched-KiDS carrier template reproduces L360's full-carrier template "
      "within 2% in every bin", f"max relative deviation {dev5:.4f}", dev5 < 0.02, load_bearing=False)
OUT["numbers"]["controls"] = dict(flagship_dev=dev1, epsU=EPS_U, epsU_L372=epsU372, kids_template_dev=dev5)

# ================================================================================================ the cheap gates
banner("G1  THE CHEAP GATES OVER THE GRID: galaxies, X-COP, KiDS, S_8, the forest proxy")
YV0S = [0.003, 0.01, 0.03, 0.1] if not FAST else [0.01, 0.1]
VAS = [600.0, 800.0] if not FAST else [600.0]
FUS = [0.0, 0.15, 0.25]
with ThreadPoolExecutor(NTH) as ex:
    RET = dict(ex.map(lambda j: (j, a_retention(*j)), [(yv0, va) for yv0 in YV0S for va in VAS]))
P(f"    mode A retention done for {len(RET)} (y_v0, v_A) pairs   [{time.time()-T0:.0f}s]")


def hist_job(j):
    yv0, va = j
    S_A, Fb = a_history(yv0, va)
    _, Ft = a_history(yv0, va, weight="plain", escaped=False)
    return j, dict(S_A=S_A, Fb=Fb, Ft=Ft)


with ThreadPoolExecutor(NTH) as ex:
    HIST = dict(ex.map(hist_job, [(yv0, va) for yv0 in YV0S for va in VAS]))
SURV_U = {fu: (G19["surv_triggered"](fu, 2)[0] if fu > 0 else np.ones_like(a_grid)) for fu in FUS}


def solve_job(j):
    kind, yv0, va, fu, v = j
    if kind == "A": S = HIST[(yv0, va)]["S_A"]
    elif kind == "U": S = SURV_U[fu]
    else: S = SURV_U[fu] * HIST[(yv0, va)]["S_A"]
    return j, solve_hist(S, v)


_sj = [("A", yv0, va, 0.0, va) for yv0 in YV0S for va in VAS]
_sj += [("U", 0.0, 0.0, fu, 3000.0) for fu in FUS if fu > 0]
_sj += [("AU", yv0, va, fu, v) for yv0 in YV0S for va in VAS for fu in FUS if fu > 0 for v in (3000.0, va)]
with ThreadPoolExecutor(NTH) as ex:
    SOL = dict(ex.map(solve_job, _sj))
P(f"    {len(SOL)} solver runs done   [{time.time()-T0:.0f}s]")
S8L = float(L57["S8_LCDM"])


def s8_comb(yv0, va, fu):
    sA = SOL[("A", yv0, va, 0.0, va)]["S8"]
    if fu <= 0: return sA
    sU = SOL[("U", 0.0, 0.0, fu, 3000.0)]["S8"]
    return math.sqrt(max(sA ** 2 + sU ** 2 - S8L ** 2, 0.0))


# C3: additivity at a common speed (600 km/s), on the first cell with U
_y0, _va = YV0S[0], 600.0
_sA6 = SOL[("A", _y0, _va, 0.0, _va)]["S8"]
_sU6 = solve_hist(SURV_U[0.25], 600.0)["S8"]
_add6 = math.sqrt(max(_sA6 ** 2 + _sU6 ** 2 - S8L ** 2, 0.0)); _joint6 = SOL[("AU", _y0, _va, 0.25, _va)]["S8"]
check("C3 CONTROL: the additive S_8 combination at a common speed (600 km/s; y_v0 = %g, f_U(0) = 0.25) matches the solver's "
      "joint run within 0.003 and errs low (conservative)" % _y0, f"additive {_add6:.4f}, joint {_joint6:.4f}",
      abs(_add6 - _joint6) <= 0.003 and _add6 <= _joint6 + 1e-9, load_bearing=False)
ROWS = {}
for yv0 in YV0S:
    for va in VAS:
        R_ = RET[(yv0, va)]
        for fu in FUS:
            fz0, fzl = fU_of_z(fu, 0.0), fU_of_z(fu, ZL)
            epsU = EPS_U.get(fu, 1.0) if fu > 0 else 1.0
            xc = xcop_from_eps(R_["xcop"] * epsU)
            gs = gal_shifts({k: v * (1 - fz0) for k, v in R_["gal"].items()})
            ks = kids_score([t * (1 - fzl) for t in R_["kidsT"]])
            ksw = kids_switched(R_["kids_prof"], 1 - fzl)
            sa = SOL[("A", yv0, va, 0.0, va)]
            b_hi = SOL[("AU", yv0, va, fu, va)]["S8"] if fu > 0 else sa["S8"]           # every decay at v_A
            b_lo = SOL[("AU", yv0, va, fu, 3000.0)]["S8"] if fu > 0 else sa["S8"]       # every decay at v_U
            r = dict(yv0=yv0, q=q_of(yv0), vA=va, fU0=fu, xcop=xc, gal=gs, kids={f"{k[0]}|{k[1]}": v["dchi2"] for k, v in ks.items()},
                     S8=s8_comb(yv0, va, fu), S8_all_vA=b_hi, S8_all_vU=b_lo, t2=sa["t2"], t3=sa["t3"], eps_xcop=R_["xcop"] * epsU)
            r["gal_max"] = max(abs(v) for f_ in gs for v in gs[f_].values())
            r["gal_ok"] = r["gal_max"] <= 0.06
            r["kids_sw"] = ksw
            r["kids_ok"] = all(ksw[f_] <= 4.0 for f_ in FOOT)                            # switched, common cell (L360/L364's gate)
            r["kids_free_ok"] = all(r["kids"][f"web-blind kernel|{f_}"] <= 9.0 for f_ in FOOT)   # switch-free (reported)
            r["xcop_strict"] = all(xc[f_]["strict"] for f_ in FOOT); r["xcop_alt"] = all(xc[f_]["alt"] for f_ in FOOT)
            r["S8_strict"], r["S8_alt"] = r["S8"] >= S8_STRICT, r["S8"] >= S8_ALT
            ROWS[(yv0, va, fu)] = r
            P(f"    y_v0 {yv0:5.3f} (q {r['q']:.2f}) v_A {va:4.0f} f_U {fu:.2f}: galaxies {r['gal_max']:+.3f}; X-COP eps {r['eps_xcop']:.2f} -> "
              f"{xc['canonical']['ratio']:.2f}/{xc['alt']['ratio']:.2f}; KiDS (p1_x2.5) {r['kids_sw']['canonical']:+.1f}/{r['kids_sw']['alt']:+.1f} "
              f"(switch-free {r['kids']['web-blind kernel|canonical']:+.1f}/{r['kids']['web-blind kernel|alt']:+.1f}); S8 {r['S8']:.3f} (bounds {r['S8_all_vU']:.3f}-{r['S8_all_vA']:.3f}); proxy T2 {min(r['t2'], r['t3']):.3f}")
OUT["numbers"]["G1"] = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in ROWS.items()}
OUT["numbers"]["retention"] = {f"{k[0]}|{k[1]}": {kk: vv for kk, vv in v.items() if kk not in ("kidsT", "kids_prof")} for k, v in RET.items()}


def cheap_ok(r):
    return r["gal_ok"] and r["kids_ok"] and r["xcop_alt"] and r["S8_alt"]


# ================================================================================================ the flagship at every z
banner("G2  THE FLAGSHIP AT z = 0.5-2.5 (GP5's definition; mode A only, which is conservative)")
FLAG = {}


def flag_job(j):
    yv0, va, z = j
    mf = (1 / 1.5, 1.0, 1.5) if z == 2.5 else (1.0,)
    rows = flagship_rows(z, yv_eff(yv0, z), va, mufacs=mf)
    return j, max(abs(r_["shift"]) for r_ in rows)


ZF = (0.5, 1.0, 1.5, 2.0, 2.5)
with ThreadPoolExecutor(NTH) as ex:
    FLAG = dict(ex.map(flag_job, [(yv0, va, z) for yv0 in YV0S for va in VAS for z in ZF]))
for yv0 in YV0S:
    for va in VAS:
        P(f"    y_v0 {yv0:5.3f} v_A {va:4.0f}: " + "; ".join(f"z {z}: {FLAG[(yv0, va, z)]:.3f}" for z in ZF) + f"   [{time.time()-T0:.0f}s]")
OUT["numbers"]["G2"] = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in FLAG.items()}
flag_ok = {(yv0, va): max(FLAG[(yv0, va, z)] for z in ZF) <= 0.10 for yv0 in YV0S for va in VAS}

# ================================================================================================ Harvey on the candidates
banner("G3  HARVEY+2015 (L370's machinery via L372's harvey(), the carrier processed by modes A and U)")
P72 = os.path.join(REPO, "real_research", "merger_infall_2026", "L372_gated_slow_kick_carrier.py")
_s72 = open(P72).read()
_harv = _s72[_s72.index('P70 = os.path.join(HERE, "L370_boosted_infall_mergers.py")'):_s72.index("def non_harvey_ok(r):")]
from scipy.optimize import brentq
from scipy.interpolate import PchipInterpolator
HNS = dict(os=os, math=math, np=np, time=time, P=P, T0=T0, brentq=brentq, PchipInterpolator=PchipInterpolator, FAST=FAST,
           HERE=os.path.join(REPO, "real_research", "merger_infall_2026"), RHOC0_KPC_57=RHOC0_KPC, Ez2_57=Ez2,
           rho_thr_57=L57["rho_thr"], x_eff=None, retained_core_57=L57["retained_core"])
_mut, os.environ["MUTATE"] = os.environ.get("MUTATE", "0"), "0"
with contextlib.redirect_stdout(io.StringIO()):
    exec(_harv, HNS)
os.environ["MUTATE"] = _mut
cum_mass_70, RG70, RHOC_H, ZH = HNS["cum_mass"], HNS["RG"], HNS["RHOC_H"], HNS["ZH"]


def ratio_profile_acc(H, pic, xv, vk):
    """mode A's retention profile of L370's real halo: pic is unused, xv carries y_v,eff(z_H), vk is v_A."""
    Mb_tab = cum_mass_70(H.rho_b)
    Mb_fn = lambda r: np.interp(np.asarray(r, float), RG70, Mb_tab)
    rv = r_v_profile(Mb_fn, xv, rmax=3 * H.R200)
    pro = np.geomspace(10.0, 2.0 * H.R200, 24)
    q, _ = retained_acc(Mb_fn, H.M200, H.c, list(pro), rv, vk, RHOC_H)
    return pro, np.asarray(q)


HNS["ratio_profile"] = ratio_profile_acc                              # L372's solve_processed() calls it by name
SW_COMMON = "p1_x2.5"
HNS["L70"]["SWITCH"][SW_COMMON] = (1.0, 2.5)                            # DE2's linear gate: L370's table gains the entry
HNS["SW_DEF"] = SW_COMMON                                              # L372's harvey()/solve_processed() read it by name
harvey = HNS["harvey"]
P(f"    L372's Harvey section loaded (L370's machinery, its LCDM references computed); switch cell {SW_COMMON}   [{time.time()-T0:.0f}s]")
cands = sorted([k for k, r in ROWS.items() if cheap_ok(r) and flag_ok[(k[0], k[1])]],
               key=lambda k: (-ROWS[k]["S8"], k))[: (2 if FAST else 4)]
if not cands:                                                        # nothing passes the cheap gates: score the nearest for the record
    cands = sorted(ROWS, key=lambda k: -(ROWS[k]["gal_ok"] + ROWS[k]["kids_ok"] + ROWS[k]["xcop_alt"] + ROWS[k]["S8_alt"]))[:2]
HV = {}
for k in cands:
    yv0, va, fu = k
    us = 1 - fU_of_z(fu, ZH)
    HV[k] = harvey("acc", yv_eff(yv0, ZH), va, us)
    h_ = HV[k]
    P(f"    y_v0 {yv0} v_A {va:.0f} f_U {fu}: excess beta " + "/".join(f"{h_['beta'][e]:+.3f}" for e in ("100", "150", "fit"))
      + f"; core carrier/baryons(<150 kpc) {h_['core'][1e14]:.2f} / {h_['core'][3e14]:.2f} -> {'PASS' if h_['ok'] else 'FAIL'}   [{time.time()-T0:.0f}s]")
OUT["numbers"]["G3"] = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in HV.items()}

# ================================================================================================ the forest on its observable
banner("G4  THE FOREST ON ITS OBSERVABLE (AT2's run() in L365's box, L365's rule) for the Harvey-passing cells")
sys.path.insert(0, HERE)
import AT2_forest_flux_calibrated as AT2                              # noqa: E402  (main-guarded: only its functions load)
fcells = [k for k in HV if HV[k]["ok"]] or list(HV)[:1]
FOR = {}
if fcells:
    cfg = [("lcdm", AT2.BOX65, "lcdm", 0.0, None, None, 0.0, "densest")]
    for yv0, va in sorted({(k[0], k[1]) for k in fcells}):                # U's decays at z >= 2 are negligible: not in the PM
        cfg.append((f"acc{(yv0, va)}", AT2.BOX65, "acc", 0.0, np.array(ZG), np.array(HIST[(yv0, va)]["Ft"]), va, "densest"))
    with ThreadPoolExecutor(min(len(cfg), 4)) as ex:                  # threads: this script has no main guard for spawn
        RPM = dict(ex.map(AT2.run, cfg))
    for k in fcells:
        r_ = RPM[f"acc{(k[0], k[1])}"]
        FOR[k] = dict(rule=AT2.l365_rule(r_, RPM["lcdm"]), flux_max=max(abs(x) for zz in ("3.0", "2.0") for x in AT2.band_dev(r_, RPM["lcdm"])[zz]),
                      decayed=(r_["3.0"]["decayed"], r_["2.0"]["decayed"]))
        P(f"    y_v0 {k[0]} v_A {k[1]:.0f}: decayed z = 3/2 {FOR[k]['decayed'][0]:.3f}/{FOR[k]['decayed'][1]:.3f}; L365's rule "
          f"{FOR[k]['rule']:.4f}; largest band deviation (k_par <= 6.5) {FOR[k]['flux_max']:.4f}   [{time.time()-T0:.0f}s]")
OUT["numbers"]["G4"] = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in FOR.items()}

# ================================================================================================ cosmic shear (reported)
banner("G5  COSMIC SHEAR: L364's formula; the common kernel cell's phantom power from L363's machinery, as L364 computes it")
l364 = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L364_replacement_carrier_cosmic_shear_results.json")))
PH = dict(l364["numbers"]["phantom"]); KG = ("0.1", "0.2", "0.3", "0.5", "0.7", "1.0")
P63 = os.path.join(REPO, "real_research", "g03_audit_2026", "L363_region_kernel_lensing_power.py")
N63 = {"__name__": "l363", "__file__": P63}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(P63).read().split("# ============================================================================================ C1 control")[0]
         .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), N63)
MK = N63["build_mock"](100.0, 256, 20260926)                          # L364's mock and seed


def phantom_power(xc, a0):
    src = MK["rhoB"]
    mask, _ = N63["build_regions"](MK, src, xc, a0)
    rp, _, _, _ = N63["region_phantom"](MK, mask, src * mask, a0)
    pk = N63["spectra"](MK, {"m": MK["rho_m"] / N63["RHO"] - 1, "ph": rp / N63["RHO"]})
    kh, Pmm = pk("m", "m"); _, Pxx = pk("m", "ph"); _, Ppp = pk("ph", "ph")
    rx = Pxx / np.sqrt(np.maximum(Pmm * Ppp, 1e-300)); s2 = Ppp / N63["PNL_of"](kh)
    return dict(s2={q: float(np.interp(float(q), kh, s2)) for q in KG}, rx={q: float(np.interp(float(q), kh, rx)) for q in KG})


c4 = phantom_power(2.0 * N63["E2"] ** 2.0, FOOT["canonical"])
ref4 = l364["numbers"]["phantom"]["p=2, x_c0=2.0/canonical"]
dev4 = max(max(abs(c4["s2"][q] - ref4["s2"][q]), abs(c4["rx"][q] - ref4["rx"][q])) for q in KG)
check("C4 CONTROL: L363's machinery reproduces L364's committed phantom power at its p = 2, x_c0 = 2 cell (canonical; s^2 and r_x "
      "at k = 0.1-1, 1e-9)", f"max |dev| {dev4:.1e}", dev4 < 1e-9, load_bearing=False)
XC_COMMON = 2.5 * N63["E2"] ** 1.0
for f_ in FOOT:
    PH[f"p=1, x_c0=2.5/{f_}"] = phantom_power(XC_COMMON, FOOT[f_])
P(f"    common cell p = 1, x_c0 = 2.5: x_c,eff(0.5) = {XC_COMMON:.5f}; s^2 at k = 0.5/1: " + "; ".join(
    f"{f_} {PH[f'p=1, x_c0=2.5/{f_}']['s2']['0.5']:.4f}/{PH[f'p=1, x_c0=2.5/{f_}']['s2']['1.0']:.4f}" for f_ in FOOT) + f"   [{time.time()-T0:.0f}s]")
OUT["numbers"]["phantom_common"] = {f_: PH[f"p=1, x_c0=2.5/{f_}"] for f_ in FOOT}
_de3 = os.path.join(REPO, "real_research", "dark_energy_2026", "DE3_tmax_at_linear_gate_results.json")
if os.path.exists(_de3):                                              # a parallel lane's export (reported only)
    try:
        _t = json.load(open(_de3))["numbers"]["table"]
        _k = [k_ for k_ in _t if k_.startswith("4.36302") and k_.endswith("/canonical")]
        if _k:
            P(f"    (reported) DE3's table at the same cell, canonical s^2 at k = 1: {_t[_k[0]]['s2']['1.0']:.4f} (this lane: "
              f"{PH['p=1, x_c0=2.5/canonical']['s2']['1.0']:.4f})")
    except Exception as _e:
        P(f"    (DE3's table not read: {_e})")
LC = L57["LC"]; T2f = L57["T2f"]; K_H = L57["K_H"]
SHEAR = {}
for k in sorted(set(cands) | {k_ for k_, r_ in ROWS.items() if cheap_ok(r_) and flag_ok[(k_[0], k_[1])]}):
    yv0, va, fu = k
    R = G19["run"](SURV_U[fu] * HIST[(yv0, va)]["S_A"], va)
    T05 = np.sqrt(np.maximum(T2f(R, LC, 0.5), 0.0)); Tq = {q: float(np.interp(math.log(float(q)), np.log(K_H), T05)) for q in KG}
    SHEAR[k] = {cell: max(Tq[q] ** 2 + 2 * v["rx"][q] * Tq[q] * math.sqrt(v["s2"][q]) + v["s2"][q] for q in KG) for cell, v in PH.items()}
    P(f"    y_v0 {yv0} v_A {va:.0f} f_U {fu}: T(k = 0.5/1) {Tq['0.5']:.3f}/{Tq['1.0']:.3f}; worst R " + "; ".join(f"{c_}: {v:.2f}" for c_, v in SHEAR[k].items()))
OUT["numbers"]["G5"] = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in SHEAR.items()}

# ================================================================================================ W1 the window
banner("W1-W3  THE WINDOW")
WIN = []
for k in HV:
    r = ROWS[k]
    ok = (flag_ok[(k[0], k[1])] and r["gal_ok"] and r["kids_ok"] and r["xcop_alt"] and r["S8_alt"] and HV[k]["ok"]
          and (k in FOR and FOR[k]["rule"] <= 0.10))
    if ok: WIN.append(k)
SH_COMMON = {k: max(SHEAR[k][f"p=1, x_c0=2.5/{f_}"] for f_ in FOOT) for k in SHEAR}
FULL = [k for k in WIN if k in SH_COMMON and SH_COMMON[k] <= 1.2]
table = {}
for k, r in ROWS.items():
    fl = []
    if not flag_ok[(k[0], k[1])]: fl.append(f"flagship {max(FLAG[(k[0], k[1], z)] for z in ZF):.2f}")
    if not r["gal_ok"]: fl.append(f"galaxies {r['gal_max']:+.3f}")
    if not r["kids_ok"]: fl.append(f"KiDS (p1_x2.5) {r['kids_sw']['canonical']:+.1f}/{r['kids_sw']['alt']:+.1f}")
    if not r["xcop_alt"]: fl.append(f"X-COP {r['xcop']['canonical']['ratio']:.2f}/{r['xcop']['alt']['ratio']:.2f}")
    if not r["S8_alt"]: fl.append(f"S8 {r['S8']:.3f}")
    if k in HV and not HV[k]["ok"]: fl.append(f"Harvey {HV[k]['beta']['fit']:+.3f}")
    if k in FOR and FOR[k]["rule"] > 0.10: fl.append(f"forest {FOR[k]['rule']:.3f}")
    if k in SH_COMMON and SH_COMMON[k] > 1.2: fl.append(f"cosmic shear (p1_x2.5) {SH_COMMON[k]:.2f}")
    table[f"{k[0]}|{k[1]}|{k[2]}"] = fl or (["PASSES EVERY GATE SCORED"] if k in HV else ["passes the cheap gates (Harvey/forest not scored)"])
    P(f"    y_v0 {k[0]:5.3f} v_A {k[1]:4.0f} f_U {k[2]:.2f}: " + ", ".join(table[f'{k[0]}|{k[1]}|{k[2]}']))
strict_note = {f"{k[0]}|{k[1]}|{k[2]}": dict(S8_strict=ROWS[k]["S8_strict"], xcop_strict=ROWS[k]["xcop_strict"]) for k in WIN}
check("W1 = H1: a cell passes every gate except cosmic shear together -- the flagship at every redshift (0.5-2.5), galaxies, "
      "X-COP, KiDS and Harvey (both at the common switch cell p = 1, x_c0 = 2.5) and S_8 on the alternative set, and the forest on "
      "its observable (L365's rule)",
      (WIN, strict_note) if WIN else "no cell", (len(WIN) > 0) == EXPECT["H1"],
      "mode A clears galaxies at every z by the kernel's own argument; mode U depletes clusters without hollowing group cores")
check("W2 = H2: cosmic shear at the common kernel cell (p = 1, x_c0 = 2.5) blocks every W1 cell (worst R > 1.2 on k <= 1, some "
      "footing)", {f"{k[0]}|{k[1]}|{k[2]}": round(SH_COMMON.get(k, float('nan')), 3) for k in WIN} if WIN else "no W1 cell",
      (len(FULL) == 0) == EXPECT["H2"] and len(WIN) > 0,
      "the acceleration trigger clears galaxies' inner regions; cosmic shear needs the carrier's group-scale power handed over "
      "by z = 0.5, which this trigger does not remove")
check("W3 (reported) the gate table, with cosmic shear at the common cell and L364's two cells",
      dict(table=table, shear={f"{k[0]}|{k[1]}|{k[2]}": v for k, v in SHEAR.items()}), True, load_bearing=False)
OUT["numbers"]["W"] = dict(window_except_shear=[list(k) for k in WIN], full_window=[list(k) for k in FULL], table=table,
                           shear_common={f"{k[0]}|{k[1]}|{k[2]}": v for k, v in SH_COMMON.items()})

banner("VERDICT")
if WIN:
    k = WIN[0]; r = ROWS[k]
    P(f"""  THE ACCELERATION-TRIGGERED CARRIER PASSES EVERY GATE BUT COSMIC SHEAR (alternative threshold set){' -- AND COSMIC SHEAR TOO' if FULL else ''}.
  Cell y_v0 = {k[0]} (q = {r['q']:.2f}, y_v,eff(2.5) = 0.1), v_A = {k[1]:.0f} km/s, f_U(0) = {k[2]}: flagship <= {max(FLAG[(k[0], k[1], z)] for z in ZF):.3f} dex at
  z = 0.5-2.5; galaxies {r['gal_max']:+.3f} dex; X-COP {r['xcop']['canonical']['ratio']:.2f}/{r['xcop']['alt']['ratio']:.2f}; KiDS (p1_x2.5) {r['kids_sw']['canonical']:+.1f}/{r['kids_sw']['alt']:+.1f};
  Harvey fit {HV[k]['beta']['fit']:+.3f} (switch p1_x2.5); S_8 {r['S8']:.3f}; forest (L365's rule) {FOR[k]['rule']:.4f}.
  Cosmic shear at the common kernel cell: worst R {SH_COMMON.get(k, float('nan')):.2f} (gate 1.2).""")
else:
    P("  No cell passes every gate scored; the table above lists what blocks each.")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
OUT["runtime_s"] = time.time() - T0
outname = f"{SLUG}_results{'_FAST' if FAST else ''}{'_MUTATE' if MUTATE else ''}.json"   # smoke runs never overwrite the main output
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=lambda o: float(o) if np.isscalar(o) else str(o))
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time()-T0:.0f}s]")
sys.exit(0 if n_fail == 0 else 1)
