#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L360 -- THE ASSEMBLED VACUUM-GATED CONSTRUCTION ON KiDS-1000: the gated switch's phantom (L359) plus the gated carrier's
post-decay halo (L357) around the same isolated lenses.

WHY.  L357 built a carrier that decays where the vacuum-gated density variable u = x~ [Omega_L(z)/Omega_L,0]^p exceeds a
high threshold (galaxy interiors, cluster cores) and passes the forest, S_8, X-COP and the galaxy gate; its open gate was
KiDS.  L359 gated the MOND switch by the same factor and reopened it (growth, KiDS, forest).  Assembled, every isolated
lens carries both: the switched phantom inside its edge (cancelled beyond it by Gauss, L352) and the carrier's halo,
hollowed where it decayed.  This lane scores the pair on KiDS-1000 exactly as L352/L359 score the switch.

MACHINERY (L352's, loaded unedited): the four Brouwer+21 stellar-mass bins with full covariance, M_b profiled per bin,
the compensated switched phantom at x_c,eff(z_l = 0.25), the bias-like linear 2-halo term (free amplitude), exact annulus
averages.  One template added: the carrier's post-decay halo per bin -- (1 - f_b) x NFW(M200, c) of the bin's Moster+13
host, cleared inside the trigger radius (or capped at the trigger density) at x_v,eff(0.25) = x_v0 E(0.25)^(2 p_c) --
projected with L352's own projector.  Static profile (L357's phase mixing moves a little carrier inward; not included).
PRE-DECLARED CRITERION (L352's acceptance): Delta chi^2 <= +4 against the unswitched model, both footings, with the
construction's own carrier (amplitude fixed at 1).
CHECKS
  M0 CONTROL: with no carrier the fit reproduces L359's switch-alone scores (same code path).
  M1 CONTROL: an undecayed carrier (a full CDM-like halo) on top of the switched phantom is rejected (Delta chi^2 > +100):
     KiDS has the power to exclude a cold halo here.
  M2 THE ASSEMBLED CONSTRUCTION PASSES KiDS for pairs drawn from the two windows (L359's switch cells x L357's carrier
     cells), both footings.
  M3 (reported) the carrier amplitude KiDS prefers.
MUTATE=1 leaves the carrier undecayed in every pair: M2 must FAIL (rc = 1).
SCOPE.  KiDS is scored with L352's isolated phantom inside the switch edge (the bound-region kernel, L355's door).

Run from the repository root after L357 and L359:  python3 real_research/g03_audit_2026/L360_assembled_construction_kids.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L360_assembled_construction_kids"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L360", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the carrier never decays; M2 must FAIL ***")

# ---------------------------------------------------------------------------------- L352's KiDS machinery, unedited
P52 = os.path.join(HERE, "L352_switch_gauss_compensation.py")
L52 = {"__name__": "l352", "__file__": P52}
_src = open(P52).read().split("real_mode = ")[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src, L52)
fit_model, esd_bin, twoh_cache, LM, Ed, Sd, Ci, A0 = [L52[k] for k in ("fit_model", "esd_bin", "twoh_cache", "LM", "Ed", "Sd", "Ci", "A0")]
project_M2, annulus_esd, rr, Rp, MS, Om, OL, rho_crit0, Rd = [L52[k] for k in ("project_M2", "annulus_esd", "rr", "Rp", "MS", "Om", "OL", "rho_crit0", "Rd")]
h = 0.6736; FB = 0.02237 / (0.02237 + 0.1200)
ZL = 0.25
M200_BINS = [4.17e11, 8.97e11, 1.91e12, 5.55e12]                     # Moster+13 hosts of the bins (L355, K1 header)
rhoc_zl = rho_crit0 * (Om * (1 + ZL) ** 3 + OL)
c200 = lambda M: 10 ** (0.905 - 0.101 * math.log10(M / (1e12 / h)))   # Dutton-Maccio 2014 (as L321/L355)
mfn = lambda x: np.log(1 + x) - x / (1 + x)
E2 = lambda z: Om * (1 + z) ** 3 + OL
P(f"  L352 KiDS machinery loaded   [{time.time() - T0:.0f}s]")

# ---------------------------------------------------------------------------------- the two windows (committed results)
R59 = json.load(open(os.path.join(HERE, "L359_vacuum_gated_switch_results.json")))
R57 = json.load(open(os.path.join(REPO, "real_research", "dark_sector_2026", "L357_virialization_triggered_carrier_results.json")))
SW = [(float(c["p"]), float(c["x_c0"])) for c in R59["numbers"]["W1"]]
_strict = sorted({(float(c["p"]), c["picture"], float(c["x_v0"])) for c in R57["numbers"]["D2"]["window"]["strict"]})
_alt = sorted({(float(c["p"]), c["picture"], float(c["x_v0"])) for c in R57["numbers"]["D2"]["window"]["alt"]} - set(_strict))
CW = _strict + _alt[:max(0, 12 - len(_strict))]                        # every strict carrier cell, then alternative ones (12 in all)
XE59 = {(float(k_.split("/")[0]), float(k_.split("/")[1])): v_["x_eff"] for k_, v_ in R59["numbers"]["K1"].items()}
P(f"  switch window (L359): {SW}")
P(f"  carrier window (L357, distinct (p, picture, x_v0)): {CW}")


def carrier_esd(xv_eff, pic):
    out = []
    for b, M in enumerate(M200_BINS):
        c = c200(M); r200 = (3 * M * MS / (4 * math.pi * 200 * rhoc_zl)) ** (1 / 3); rs = r200 / c
        rho_s = M * MS / (4 * math.pi * rs ** 3 * mfn(c))
        rho = np.where(rr < r200, rho_s / ((rr / rs) * (1 + rr / rs) ** 2), 0.0)
        rv = (Om * (1 + ZL) ** 3 / E2(ZL) + 2 / 3 * xv_eff) * rhoc_zl
        rc = (1 - FB) * rho
        if not np.isfinite(xv_eff): keep = rc
        elif pic == "cleared": keep = np.where(rho >= rv, 0.0, rc)
        else: keep = np.minimum(rc, rv)
        M2 = project_M2(keep)
        out.append(annulus_esd(lambda R, M2=M2: np.interp(np.log(R), np.log(Rp), M2), Rd[b]))
    return out


def fit_comb(a0, xc, TC, fs_grid):
    best_all = None
    for fsv in fs_grid:
        mods, As = [], []
        for b in range(4):
            best = None
            for lm in LM:
                mk0, _ = esd_bin(b, lm, a0, xc, "compensated", False)
                mk0 = mk0 + fsv * TC[b]
                t2 = twoh_cache[b]; w = 1 / Sd[b] ** 2
                A = float(np.clip(np.sum(w * t2 * (Ed[b] - mk0)) / np.sum(w * t2 * t2), 0.0, 20.0)); mk = mk0 + A * t2
                c_ = float(np.sum(((Ed[b] - mk) / Sd[b]) ** 2))
                if best is None or c_ < best[0]: best = (c_, mk, lm, A)
            mods.append(best[1]); As.append(round(best[3], 2))
        dv = np.concatenate(Ed) - np.concatenate(mods); c2 = float(dv @ Ci @ dv)
        if best_all is None or c2 < best_all[0]: best_all = (c2, fsv, As)
    return best_all


BASE = {f_: fit_model(A0[f_], 0.0, "none", True)[0] for f_ in ("canonical", "alt")}

# ============================================================================================ M0 / M1 controls
banner("M0-M1  CONTROLS")
m0 = {}
for (ps, xc0) in SW:
    xe = round(XE59[(ps, xc0)], 4)                                     # L359's own x_c,eff(0.25) (same background, same edge)
    for f_ in ("canonical", "alt"):
        m0[(ps, xc0, f_)] = fit_comb(A0[f_], xe, [np.zeros_like(Rd[b]) for b in range(4)], [0.0])[0] - BASE[f_]
ref59 = {(float(k_.split("/")[0]), float(k_.split("/")[1])): v_ for k_, v_ in R59["numbers"]["K1"].items()}
dev0 = max(abs(m0[(ps, xc0, f_)] - ref59[(ps, xc0)]["dchi2"][f_]) for (ps, xc0) in SW for f_ in ("canonical", "alt")) if SW else float("nan")
check("M0 CONTROL: with no carrier the assembled fit reproduces L359's switch-alone KiDS scores (same code path)",
      f"max |difference| = {dev0:.2e}", SW and dev0 < 1e-6, load_bearing=False)
TC_INT = carrier_esd(float("inf"), "cleared")
m1 = {(ps, xc0, f_): fit_comb(A0[f_], round(XE59[(ps, xc0)], 4), TC_INT, [1.0])[0] - BASE[f_] for (ps, xc0) in SW
      for f_ in ("canonical", "alt")}
check("M1 CONTROL: an undecayed carrier (a full cold halo) on top of the switched phantom is rejected by KiDS (Delta chi^2 > +100, "
      "every switch cell, both footings)", f"min {min(m1.values()):+.1f}" if m1 else "no switch cell",
      bool(m1) and min(m1.values()) > 100, "KiDS can tell a CDM halo from a hollowed one here", load_bearing=False)

# ============================================================================================ M2 the assembled construction
banner("M2  THE ASSEMBLED CONSTRUCTION: switched phantom + the carrier's post-decay halo (amplitude 1) + 2-halo")
M2 = {}
for (pc, pic, xv0) in CW:
    xve = float("inf") if MUTATE else xv0 * E2(ZL) ** pc
    TC = carrier_esd(xve, pic)
    for (ps, xc0) in SW:
        xe = round(XE59[(ps, xc0)], 4)
        d_, fsb, Ab = {}, {}, {}
        for f_ in ("canonical", "alt"):
            c1, _, A1 = fit_comb(A0[f_], xe, TC, [1.0])
            cf, fsv, _ = fit_comb(A0[f_], xe, TC, np.linspace(0, 1.2, 25))
            d_[f_] = c1 - BASE[f_]; fsb[f_] = (fsv, cf - BASE[f_]); Ab[f_] = A1
        M2[(ps, xc0, pc, pic, xv0)] = dict(dchi2=d_, best_fs=fsb, A_2h=Ab, ok=all(v <= 4.0 for v in d_.values()))
        P(f"    switch (p = {ps:g}, x_c0 = {xc0:g}) + carrier (p = {pc:g}, {pic}, x_v0 = {xv0:g}): Delta chi^2 canonical "
          f"{d_['canonical']:+.1f}, alt {d_['alt']:+.1f} -> {'PASS' if all(v <= 4 for v in d_.values()) else 'FAIL'};  "
          f"KiDS-preferred amplitude {fsb['canonical'][0]:.2f}/{fsb['alt'][0]:.2f} ({fsb['canonical'][1]:+.1f}/{fsb['alt'][1]:+.1f}); "
          f"2-halo A {Ab['canonical']}   [{time.time() - T0:.0f}s]")
OUT["numbers"]["M0"] = {f"{k_[0]}/{k_[1]}/{k_[2]}": v_ for k_, v_ in m0.items()}
OUT["numbers"]["M1"] = {f"{k_[0]}/{k_[1]}/{k_[2]}": v_ for k_, v_ in m1.items()}
OUT["numbers"]["M2"] = {"/".join(str(x_) for x_ in k_): v_ for k_, v_ in M2.items()}
passing = [k_ for k_, v_ in M2.items() if v_["ok"]]
check("M2 THE ASSEMBLED CONSTRUCTION PASSES KiDS-1000: pairs from the two windows score Delta chi^2 <= +4 against the "
      "unswitched model on both footings with the construction's own (decayed) carrier",
      f"{len(passing)} of {len(M2)} pairs pass: " + "; ".join(f"switch (p={k_[0]:g}, x_c0={k_[1]:g}) + carrier (p={k_[2]:g}, {k_[3]}, "
                                                              f"x_v0={k_[4]:g})" for k_ in passing[:8]),
      len(passing) > 0, "the switch removes the phantom beyond its edge (Gauss); the hollowed carrier halo fills that "
      "deficit instead of doubling the phantom inside it")
fsall = [v_["best_fs"][f_][0] for v_ in M2.values() for f_ in ("canonical", "alt")]
check("M3 (reported) the carrier amplitude KiDS prefers on top of the switched phantom", f"{min(fsall):.2f}-{max(fsall):.2f}"
      if fsall else "none", True, "a preferred amplitude below 1 is a target for the decay (more outer depletion), not a failure",
      load_bearing=False)

banner("VERDICT")
P(f"""  {len(passing)} of {len(M2)} (switch cell, carrier cell) pairs pass KiDS-1000 with the construction's own carrier.  Without decay the
  carrier would be rejected (M1, Delta chi^2 >= {min(m1.values()) if m1 else float('nan'):+.0f}); hollowed where the gated trigger fired it fits the deficit the
  compensated phantom leaves beyond the switch edge.  Conditional on the bound-region kernel (L352's isolated phantom
  inside the edge).""")
n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
sys.exit(0 if n_fail == 0 else 1)
