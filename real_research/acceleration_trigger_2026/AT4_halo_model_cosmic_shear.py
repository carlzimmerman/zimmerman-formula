#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
AT4 -- COSMIC SHEAR FOR THE ACCELERATION-TRIGGERED CARRIER, RESOLUTION-FREE: the carrier's own retention by halo mass on
MS3's halo model, at the common kernel cell and at the window's top corner, with MS3's region caps.  Does the mock-based
"corner rescue" survive?

WHY.  AT3 (dd1d6a0d6) found the acceleration-triggered carrier passing every gate but cosmic shear at the common kernel
cell (p = 1, x_c0 = 2.5), with cosmic shear scored on GP3's 100 Mpc mock (L364's convention).  DE5's mock-based table then
suggested the gate loosens at the window's top corner (x_c,eff(0.5) = 6.785), enough for a 700-750 km/s kick.  But MS3
(2a5def6d9) shows the mock cannot score phantom-supported regions: L363's builder cannot grow an isolated galaxy's region
(U1), and the box is cluster-poor (M1).  On L363's resolution-free halo model the region kernel fails cosmic shear for
every carrier history unless every MOND region is capped near 1.75 Mpc at z = 0.5.  That cap is the largest one that
keeps KiDS's lenses untouched (K1), and it passes only with the particle-mesh track's group and cluster clearing (L388's
retention); clearing galaxies alone fails even capped.  DE5b (e56c00165) reproduces U1 on the upper-branch builder.  This
lane scores the acceleration-triggered carrier on MS3's halo model, with ITS OWN retention by halo mass.

THE CARRIER'S RETENTION BY HALO MASS at the lens epoch z = 0.5 (AT1/AT3's construction, f_U(0) = 0.25):
  mode A: a halo keeps 1 - f_lc(M) f_esc(M; v_A).  f_lc is the steady-state loss cone of its trigger radius at
    y_v,eff(0.5) = y_v0 E(0.5)^(2q) (AT1's trig_acc).  f_esc is the escape fraction of daughters kicked at v_A (AT1's
    table).  Bound daughters stay in the halo: they are redistributed, not removed.
  mode U: the halo keeps 1 - f_U(0.5) f_esc,U(M), with L319's law and daughters at 3000 km/s (AT1's table, whole halo).
  Two readings.  STEADY STATE is the current halo alone.  OPTIMISTIC also takes AT1's cumulative escaped fraction from
  progenitors (bias-weighted, at z = 0.5) out of every halo; that is more removal than any halo suffers, so it is the most
  favourable case for the gate.
METHOD: MS3's R_of (L363's per-halo compensated phantom transform with a region cap and an edge convention, GP3's
  Sheth-Tormen + NFW P_NL, GP0's observed bound baryons), loaded unedited, with the carrier's retention function.
  Caps {inf, 2, 1.75, 1.5, 1.2, 1} Mpc (physical, z = 0.5).  Switch cells: MS3's linear cell x = 2.5 E(0.5)^2 and DE5's
  window-top corner x = 6.785.  Both edge conventions ('door' as MS3 K1, 'upper' as L363).  Both footings.
GATE: GP3's, worst R <= 1.2 on k = 0.1-1 h/Mpc, both footings.  KiDS-safe caps: MS3 K1's r_cap >= 1.75 Mpc (at 325 km/s the
  cap sits above every KiDS lens's region; smaller caps truncate the largest lenses).
PRE-DECLARED (before the run; from MS3's committed K1, whose galaxy-only clearing fails every KiDS-safe cap at 1.64/1.74
  and above):
  H1: at every KiDS-safe cap, at both switch cells and on both edge conventions, the acceleration-triggered carrier fails
      cosmic shear on at least one footing for every kick Harvey allows (v_A <= 800 km/s, AT3), in BOTH readings.  So the
      mock-based corner rescue does not survive the resolution-free estimate.
CHECKS
  C1 CONTROL: MS3's committed K1 rows (L388's retention; galaxies only cleared) at caps 2.0 and 1.75, door convention, are
     reproduced to 1e-9.
  C2 CONTROL: a retention of 1 reproduces MS3's committed intact row at the 1.75 Mpc cap.
  H1 as pre-declared.
  R1 (reported) the kick, if any, at which the optimistic reading passes a KiDS-safe cap, and AT3's Harvey verdict there.
MUTATE=1 replaces the carrier's retention with L388's (the particle-mesh track's group and cluster clearing): the 1.75 Mpc
cap then passes (MS3 K1), so H1 must FAIL (rc = 1).

Run from the repository root:  python3 real_research/acceleration_trigger_2026/AT4_halo_model_cosmic_shear.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "AT4_halo_model_cosmic_shear"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "AT4", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 116); P(t); P("=" * 116)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the carrier's retention is L388's -- H1 must FAIL ***")
_env = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"

# ------------------------------------------------------------------------------------------------ MS3's halo model, unedited
PMS3 = os.path.join(REPO, "real_research", "mond_sector_gate_2026", "MS3_cosmic_shear_bound_mond_sector.py")
MS = {"__name__": "ms3", "__file__": PMS3}
with contextlib.redirect_stdout(io.StringIO()):
    _ms = open(PMS3).read()
    exec(_ms[:_ms.rindex("# ============================================================================================ C1 control")]   # MS3's own C1 banner
         .replace('P(__doc__.split("CHECKS")[0].strip())', "pass"), MS)
R_of, SCEN, ret_L388, XLIN, A0, E2m = MS["R_of"], MS["SCEN"], MS["ret_L388"], MS["XLIN"], MS["A0"], MS["E2"]
MS3J = json.load(open(os.path.join(REPO, "real_research", "mond_sector_gate_2026", "MS3_cosmic_shear_bound_mond_sector_results.json")))["numbers"]
P(f"  MS3's halo model loaded (L363, GP0, L388's retention): E(0.5)^2 = {E2m:.6f}, linear cell x = {XLIN:.5f}   [{time.time()-T0:.0f}s]")

# ------------------------------------------------------------------------------------------------ AT1's head (trigger, loss cone, escape)
PA1 = os.path.join(HERE, "AT1_acceleration_trigger_highz.py")
_h1 = open(PA1).read().split("# ================================================================================================ C1-C3")[0]
_h1 = _h1.replace('P(__doc__.split("CHECKS")[0].strip())', "pass")
os.environ["FAST"] = "0"
A1 = {"__name__": "at1", "__file__": PA1}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_h1, A1)
if _env is None: os.environ.pop("MUTATE", None)
else: os.environ["MUTATE"] = _env
trig_acc, I_ES, CG, XVG, UGR, MH_h, hh, Ez2, A0K = A1["trig_acc"], A1["I_ES"], A1["CG"], A1["XVG"], A1["UGR"], A1["MH"], A1["h"], A1["Ez2"], A1["A0K"]
history_acc, ZG, G19 = A1["history_acc"], A1["ZG"], A1["L57"]["G19"]
a_grid = A1["a_grid"]
P(f"  AT1's head loaded (loss-cone and escape tables, the halo model's trigger)   [{time.time()-T0:.0f}s]")
ZS = 0.5
S_U, _ = G19["surv_triggered"](0.25, 2)
FU05 = float(1 - np.interp(1 / (1 + ZS), a_grid, S_U))


def q_of(yv0): return 0.0 if yv0 >= 0.1 else math.log(0.1 / yv0) / math.log(Ez2(2.5))       # AT3's gate law


def yv_eff(yv0, z): return yv0 * Ez2(z) ** q_of(yv0)


def retention(yv0, va):
    """the carrier's retained fraction in a halo of mass M [Msun] at z = 0.5, as a function (for MS3's R_of)."""
    lc, xv, cs, V200 = trig_acc(ZS, yv_eff(yv0, ZS), A0K["canonical"])
    u = np.clip(va / V200, 0, UGR[-1]); cl = np.log(np.clip(cs, CG[0], CG[-1]))
    fe = np.where(xv > 0, I_ES(np.stack([cl, np.log(np.maximum(xv, XVG[0])), u], 1)), 0.0)
    feU = I_ES(np.stack([cl, np.zeros_like(cl), np.clip(3000.0 / V200, 0, UGR[-1])], 1))      # whole halo (x_v = 1)
    keep = (1 - np.clip(lc * fe, 0, 1)) * (1 - FU05 * np.clip(feU, 0, 1))
    lgM = np.log10(MH_h / hh)                                                                # L357's grid in Msun
    return lambda M, lgM=lgM, keep=keep: float(np.interp(math.log10(M), lgM, keep))


def cumulative_escaped(yv0, va):
    """AT1/AT3's cumulative bias-weighted escaped fraction by z = 0.5 with the gated threshold (irreversible)."""
    Fz = np.array([A1["F_acc"](z, yv_eff(yv0, z), va, A0K["canonical"], 1.0, "bias", True) for z in ZG])
    Fz = np.where(Fz < 1e-10, 0.0, Fz); Fc = np.maximum.accumulate(Fz[::-1])[::-1]
    return float(np.interp(ZS, ZG, Fc))


def retention_fn(yv0, va, reading):
    base = retention(yv0, va)
    if reading == "steady": return base
    extra = cumulative_escaped(yv0, va)                             # progenitors' mode-A losses, taken from every halo
    return lambda M, base=base, extra=extra: max(base(M) - extra, 0.0)


# ================================================================================================ C1-C2 controls
banner("C1-C2  CONTROLS")
dev = 0.0
for rc_ in (2.0, 1.75):
    for f_ in A0:
        R, _, _ = R_of(XLIN, A0[f_], rc_, "door", ret_L388)
        dev = max(dev, abs(max(R.values()) - MS3J["K1"][str(rc_)][f_]["worst"]))
        Rg, _, _ = R_of(XLIN, A0[f_], rc_, "door", SCEN["cleared<1e13"])
        dev = max(dev, abs(max(Rg.values()) - MS3J["K1"][str(rc_)]["cleared<1e13"][f_]))
check("C1 CONTROL: MS3's committed K1 rows (L388's retention and galaxies-only clearing, caps 2.0 and 1.75 Mpc, door "
      "convention, both footings) reproduced", f"max |dev| {dev:.1e}", dev < 1e-9, load_bearing=False)
one = lambda M: 1.0
d2 = max(abs(max(R_of(XLIN, A0[f_], 1.75, "door", one)[0].values()) - MS3J["K1"]["1.75"]["intact"][f_]) for f_ in A0)
check("C2 CONTROL: a retention of 1 reproduces MS3's committed intact row at the 1.75 Mpc cap (1e-9)",
      f"intact |dev| {d2:.1e}; mode U's decayed share by z = 0.5, f_U(0.5) = {FU05:.4f}", d2 < 1e-9, load_bearing=False)

# ================================================================================================ the scan
banner("S1  THE SCAN: the carrier's own retention on MS3's halo model (worst R over k = 0.1-1, canonical / alt)")
YV0S = [0.03, 0.1]; VAS = [600.0, 700.0, 800.0, 1200.0, 2000.0]
CAPS = [math.inf, 2.0, 1.75, 1.5, 1.2, 1.0]
XCELLS = {"linear (1, 2.5)": XLIN, "corner (1.904, 2.350)": float(json.load(open(os.path.join(
    REPO, "real_research", "dark_energy_2026", "DE5_tmax_window_both_branches_results.json")))["numbers"]["window_top"]["xmax"])}
RES = {}
for yv0 in YV0S:
    for va in VAS:
        for reading in ("steady", "optimistic"):
            ret = ret_L388 if MUTATE else retention_fn(yv0, va, reading)
            keep_s = [ret(10 ** lm) for lm in (12.0, 13.0, 13.5, 14.0, 14.5)]
            for xl, xc in XCELLS.items():
                for conv in ("door", "upper"):
                    for rc_ in CAPS:
                        w = {f_: max(R_of(xc, A0[f_], rc_, conv, ret)[0].values()) for f_ in A0}
                        RES[(yv0, va, reading, xl, conv, rc_)] = w
            P(f"    y_v0 {yv0:4.2f} v_A {va:5.0f} {reading:10s}: retention at 1e12/1e13/1e13.5/1e14/1e14.5 = "
              + "/".join(f"{k:.2f}" for k in keep_s) + " | door, corner: " + ", ".join(
                  f"cap {rc_:g}: {RES[(yv0, va, reading, 'corner (1.904, 2.350)', 'door', rc_)]['canonical']:.2f}/"
                  f"{RES[(yv0, va, reading, 'corner (1.904, 2.350)', 'door', rc_)]['alt']:.2f}" for rc_ in CAPS)
              + f"   [{time.time()-T0:.0f}s]")
OUT["numbers"]["scan"] = {"|".join(map(str, k)): v for k, v in RES.items()}
OUT["numbers"]["fU05"] = FU05

# ================================================================================================ H1, R1
banner("H1-R1  THE VERDICT")
SAFE = [rc_ for rc_ in CAPS if rc_ >= 1.75]
fails = all(any(v > 1.2 for v in RES[(yv0, va, rd, xl, conv, rc_)].values())
            for yv0 in YV0S for va in VAS if va <= 800.0 for rd in ("steady", "optimistic")
            for xl in XCELLS for conv in ("door", "upper") for rc_ in SAFE)
best = min(((max(RES[(yv0, va, rd, xl, conv, rc_)].values()), (yv0, va, rd, xl, conv, rc_))
            for yv0 in YV0S for va in VAS if va <= 800.0 for rd in ("steady", "optimistic") for xl in XCELLS
            for conv in ("door", "upper") for rc_ in SAFE))
check("H1: at every KiDS-safe cap (>= 1.75 Mpc), both switch cells, both edge conventions and both readings, the acceleration-"
      "triggered carrier fails cosmic shear on at least one footing for every kick Harvey allows (v_A <= 800 km/s): the mock-based "
      "corner rescue does not survive the resolution-free estimate", f"best case: worst R {best[0]:.3f} at {best[1]}", fails,
      "cosmic shear on the halo model is a group-and-cluster phantom problem (MS3 D1); the acceleration trigger clears galaxies' "
      "inner regions, and its slow daughters stay bound in groups and clusters")
R1 = {}
for yv0 in YV0S:
    for va in VAS:
        ok = [(xl, conv, rc_) for xl in XCELLS for conv in ("door", "upper") for rc_ in SAFE
              if all(v <= 1.2 for v in RES[(yv0, va, "optimistic", xl, conv, rc_)].values())]
        R1[f"{yv0}|{va}"] = ok
P("    optimistic reading, KiDS-safe caps, passing (switch cell, convention, cap): " + "; ".join(f"{k}: {v if v else 'none'}" for k, v in R1.items()))
check("R1 (reported) where the optimistic reading passes a KiDS-safe cap, by kick; AT3's Harvey fails at 800 km/s (+0.110/+0.114) "
      "and the loss would grow with faster kicks", R1, True, load_bearing=False)
OUT["numbers"]["R1"] = R1

banner("VERDICT")
P(f"""  On the resolution-free halo model the acceleration-triggered carrier {'FAILS' if fails else 'does not fail'} cosmic shear at every KiDS-safe
  region cap for every kick Harvey allows, at the common cell and at the window-top corner alike (best case {best[0]:.3f}).  The
  corner rescue suggested by the mock (DE5) rests on regions the mock cannot grow (MS3 U1, DE5b).  What passes on the halo
  model is group-and-cluster clearing plus a region cap near 1.75 Mpc (MS3 K1, L388's retention) -- and clearing group cores
  is what Harvey forbids for this trigger's kicks (AT3).""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
OUT["runtime_s"] = time.time() - T0
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=lambda o: float(o) if np.isscalar(o) else str(o))
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time()-T0:.0f}s]")
sys.exit(0 if n_fail == 0 else 1)
