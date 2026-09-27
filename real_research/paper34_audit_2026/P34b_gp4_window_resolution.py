#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
P34b -- IS GP4's COSMIC-SHEAR WINDOW RESOLVED?  GP4's two window cells re-scored in GP3's finer box.

WHY.  PAPER34's alternative-set window (GP4) passes cosmic shear with GP1's source-switched kernel screened at
lambda = 1 Mpc.  GP4 measures the phantom's power on GP3's mock: 200 Mpc, 256^3, cells of 0.78 Mpc -- about 1.3 cells per
screening length.  GP3's own convergence check (a 100 Mpc box at twice the resolution, its L2) covers lambda = 2 and 3 Mpc
only.  MS3 (2a5def6d9) found that a DIFFERENT mock builder, L363's region builder for the flux-switched kernel, cannot grow a
region around an isolated galaxy, so the region kernel's mock-based cosmic-shear pass does not survive a resolution-free
estimate.  GP3's builder has no region step (the kernel acts on the whole grid; only its source is switched), so that defect
cannot occur here; what remains untested is plain resolution at lambda = 1 Mpc.  This lane runs GP3's L2 protocol at the
window's lambda and re-scores GP4's cells with GP4's own formula.

MACHINERY (loaded unedited, as GP4 loads it): GP3's source up to its M1 banner (the 200 Mpc mock MK, measure(), ratios(),
PNL_of); GP3's L2 box, build_mock(100, 256, 20260926); GP4's shear formula R(k) = T^2 + 2 r_x T s + s^2 on the mock's k bins
with T interpolated in log k from L364's committed six values; GP4's gate R <= 1.2 on k = 0.1-1, both footings.

PRE-DECLARED (before the run):
  C1  CONTROL: the 200 Mpc box reproduces GP4's committed cosmic-shear scores for its two window cells (1e-9).
  C2  CONTROL: the 100 Mpc box reproduces GP3's committed L2 ratios at lambda = 2 (1e-9).
  H   GP4's two window cells still pass cosmic shear (worst R <= 1.2 on k = 0.1-1, both footings) in the box at twice the
      resolution.  Recorded whichever way it falls.
  D1  (reported) the change of the kernel-alone ratio between the boxes at lambda = 1 against the change at lambda = 2 (where
      GP3 found the boxes agree), and the number of cluster-mass cells in each box: a large change at lambda = 1 with a
      small one at lambda = 2 points to resolution rather than the realisation.
MUTATE=1: no free streaming (T = 1), as GP4's own control -- H must then fail in both boxes (rc = 1).

Run from anywhere:  python3 real_research/paper34_audit_2026/P34b_gp4_window_resolution.py
"""
import os, sys, io, json, time, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
GPD = os.path.join(REPO, "real_research", "generated_phantom_2026")
MUTATE = os.environ.get("MUTATE", "0") == "1"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "P34b", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, ok, measured, load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")


def banner(t):
    P("\n" + "=" * 118 + f"\n{t}\n" + "=" * 118)


def load(path, split, name):
    """exec a committed lane's machinery (everything before `split`), unedited, with its MUTATE forced off (GP4's loader)."""
    src = open(path).read().split(split)[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
    ns = {"__name__": name, "__file__": path}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(src, ns)
    return ns


P(__doc__.strip().split("\n\n")[0])
if MUTATE:
    P("  *** MUTATE=1: no free streaming (T = 1); H must FAIL in both boxes ***")

G3 = load(os.path.join(GPD, "GP3_lensing_power_and_growth.py"),
          "# ============================================================================================ M1 control", "gp3")
MK = G3["MK"]
MK2 = G3["build_mock"](100.0, 256, 20260926)                      # GP3's L2 box (its seed), unedited
P(f"  boxes: 200 Mpc cell {MK['dx']:.3f} Mpc; 100 Mpc cell {MK2['dx']:.3f} Mpc   [{time.time() - T0:.0f}s]")

GP4J = json.load(open(os.path.join(GPD, "GP4_generated_phantom_plus_kicked_carrier_results.json")))["numbers"]
GP3J = json.load(open(os.path.join(GPD, "GP3_lensing_power_and_growth_results.json")))["numbers"]
L364 = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L364_replacement_carrier_cosmic_shear_results.json")))["numbers"]
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
KG = (0.1, 0.2, 0.3, 0.5, 0.7, 1.0)
WINDOW = [(0.95, 1200.0), (0.9, 1400.0)]
LAMS = (1.0, 2.0)


def shear_input(mk, lam, a0):
    ms = G3["measure"](mk, lam, a0)
    kh = ms["kh"]; Pnl = G3["PNL_of"](kh)
    s2 = ms["Ppp"] / Pnl; rx = ms["Pxx"] / np.sqrt(np.maximum(ms["Pmm"] * ms["Ppp"], 1e-300))
    _, _, Rc, _ = G3["ratios"](ms)
    return {"kh": kh, "s2_bin": s2, "rx_bin": rx, "Rc": {q: float(np.interp(q, kh, Rc)) for q in KG}}


def shear_R(sh, T05, T_on=True):
    """GP4's formula, verbatim in effect: R(k) = T^2 + 2 r_x T s + s^2 on the mock's bins, T interpolated in log k."""
    kh = sh["kh"]
    if T_on:
        lk = np.log([float(q) for q in KG]); Tv = np.array([T05[str(q)] for q in KG])
        T = np.interp(np.log(kh), lk, Tv)
    else:
        T = np.ones_like(kh)
    sb = np.sqrt(np.maximum(sh["s2_bin"], 0.0))
    Rb = T * T + 2 * sh["rx_bin"] * T * sb + sb * sb
    return {q: float(np.interp(q, kh, Rb)) for q in KG}


SH = {}
for box, mk in (("200", MK), ("100", MK2)):
    for foot in A0:
        for lam in LAMS:
            SH[(box, foot, lam)] = shear_input(mk, lam, A0[foot])
P(f"  spectra measured (2 boxes x 2 footings x lambda {LAMS})   [{time.time() - T0:.0f}s]")

T05 = {(r["fd"], r["vk"]): r["T05"] for r in L364["scan"]}

banner("CONTROLS")
dev1 = 0.0
for fd, vk in WINDOW:
    cell = [r for r in GP4J["scan"] if r["lam"] == 1.0 and r["fd"] == fd and r["vk"] == vk][0]
    for foot in A0:
        worst = max(shear_R(SH[("200", foot, 1.0)], T05[(fd, vk)]).values())
        dev1 = max(dev1, abs(worst - cell["shear"][foot]))
check("C1 CONTROL: the 200 Mpc box reproduces GP4's committed cosmic-shear scores for its two window cells (1e-9)", dev1 < 1e-9, f"max |diff| = {dev1:.1e}")
dev2 = max(abs(SH[("100", "canonical", 2.0)]["Rc"][float(k)] - v) for k, v in GP3J["L2"]["2.0"].items())
check("C2 CONTROL: the 100 Mpc box reproduces GP3's committed L2 ratios at lambda = 2 (1e-9)", dev2 < 1e-9, f"max |diff| = {dev2:.1e}")

banner("H  GP4's WINDOW CELLS IN THE BOX AT TWICE THE RESOLUTION (lambda = 1 Mpc)")
res = {}
for fd, vk in WINDOW:
    for box in ("200", "100"):
        w = {foot: max(shear_R(SH[(box, foot, 1.0)], T05[(fd, vk)], T_on=not MUTATE).values()) for foot in A0}
        res[(fd, vk, box)] = w
        P(f"    cell f_d(0) {fd}, v_k {vk:.0f}, {box} Mpc box: worst R canonical {w['canonical']:.3f}, alt {w['alt']:.3f}")
OUT["numbers"]["window"] = {f"{fd}|{vk:.0f}|{box}": v for (fd, vk, box), v in res.items()}
fine_pass = all(res[(fd, vk, "100")][f] <= 1.2 for fd, vk in WINDOW for f in A0)
check("H GP4's two window cells still pass cosmic shear (worst R <= 1.2, k = 0.1-1, both footings) in the box at twice the "
      "resolution", fine_pass, {f"{fd}|{vk:.0f}": {f: round(res[(fd, vk, '100')][f], 3) for f in A0} for fd, vk in WINDOW})

banner("D1  (reported) RESOLUTION OR REALISATION?  The kernel-alone ratio in both boxes, and the cluster cells")
drift = {}
for lam in LAMS:
    for foot in A0:
        a, b = SH[("200", foot, lam)]["Rc"], SH[("100", foot, lam)]["Rc"]
        drift[(foot, lam)] = {q: b[q] / a[q] - 1 for q in (0.3, 0.5, 0.7, 1.0)}
        P(f"    lambda {lam} {foot:9s}: fine/coarse - 1 at k 0.3/0.5/0.7/1: " + " / ".join(f"{drift[(foot, lam)][q]:+.3f}" for q in (0.3, 0.5, 0.7, 1.0)))
OUT["numbers"]["drift"] = {f"{f}|{l}": v for (f, l), v in drift.items()}
Mcl = 1e14
ncl = {box: int(np.sum(mk["rhoB"] * mk["dx"] ** 3 >= Mcl * 0.02)) for box, mk in (("200", MK), ("100", MK2))}
vol = {"200": 200.0 ** 3, "100": 100.0 ** 3}
P(f"    cells holding >= 2e12 Msun of bound baryons (~cluster cores): 200 Mpc {ncl['200']} ({ncl['200'] / vol['200'] * 1e6:.2f} per 1e6 Mpc^3), "
  f"100 Mpc {ncl['100']} ({ncl['100'] / vol['100'] * 1e6:.2f} per 1e6 Mpc^3)")
OUT["numbers"]["cluster_cells"] = ncl
m1 = max(abs(v) for (f, l), d in drift.items() if l == 1.0 for v in d.values())
m2 = max(abs(v) for (f, l), d in drift.items() if l == 2.0 for v in d.values())
check("D1 (reported) the kernel-alone ratio changes between the boxes by at most X at lambda = 1 against Y at lambda = 2",
      True, f"lambda 1: {m1:.3f}; lambda 2: {m2:.3f}", load_bearing=False)

banner("VERDICT")
nlb = sum(1 for _, ok, lb in CH if lb and not ok)
wc = {f"{fd}|{vk:.0f}": (round(res[(fd, vk, '200')]['alt'], 3), round(res[(fd, vk, '100')]['alt'], 3)) for fd, vk in WINDOW}
P(f"  GP4's window cells, worst cosmic-shear R on the alternative footing (200 Mpc -> 100 Mpc at twice the resolution): {wc}.")
P(f"  The kernel-alone ratio moves by up to {m1:.3f} at lambda = 1 and {m2:.3f} at lambda = 2 between the boxes.")
P(f"  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nlb}   [{time.time() - T0:.0f}s]")
fn = os.path.join(HERE, "P34b_gp4_window_resolution_results" + ("_MUTATE" if MUTATE else "") + ".json")
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"  wrote {os.path.basename(fn)}")
sys.exit(1 if nlb else 0)
