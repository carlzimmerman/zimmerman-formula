#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
P34c -- GP4's COSMIC-SHEAR WINDOW AT TWICE THE RESOLUTION IN THE SAME 200 Mpc VOLUME, AND THE CLUSTER CENSUS OF EVERY BOX.

WHY.  P34b re-scored GP4's two window cells in GP3's 100 Mpc box at twice the resolution: (0.95, 1200) held, (0.90, 1400)
reached 1.208 on the alternative footing.  That box is the one MS3 (2a5def6d9, its M1) found cluster-poor: 4 cells with the
bound baryons of a >= 1e14 Msun halo against 7.4 expected, none >= 1e14.5 against 0.8.  For the region kernel clusters carry
>= 73% of the phantom's power at k = 1 (MS3 D1), so P34b's comparison mixed resolution with cluster content.  GP4's own score
used the 200 Mpc box, whose cluster content nobody had counted.  This lane (i) counts clusters in every box with MS3's
method, and (ii) re-scores GP4's window in a 200 Mpc box at 512^3 -- the same volume and seed as GP4's, twice the
resolution -- so that resolution is tested at fixed volume.

MACHINERY (loaded unedited, as GP4 and P34b load it): GP3's source up to its M1 banner (the 200 Mpc / 256^3 mock MK,
build_mock, measure, ratios, PNL_of, GP0); GP4's shear formula R(k) = T^2 + 2 r_x T s + s^2 with T from L364's committed
values; the gate R <= 1.2 on k = 0.1-1, both footings; MS3's census (cells holding at least the bound baryons of a 1e{lM}
halo, against the Sheth-Tormen expectation integrated over the box).

PRE-DECLARED (before the run):
  C1  CONTROL: the 200 Mpc / 256^3 box reproduces GP4's committed cosmic-shear scores for its two window cells (1e-9).
  C2  CONTROL: the census of the 100 Mpc box reproduces MS3's committed M1 counts exactly.
  H   GP4's two window cells pass cosmic shear (worst R <= 1.2, k = 0.1-1, both footings) in the 200 Mpc / 512^3 box.
      Recorded whichever way it falls.
  D1  (reported) the census of all three boxes against expectation.
MUTATE=1: no free streaming (T = 1), GP4's own control -- H must then fail (rc = 1).

Run from anywhere:  python3 real_research/paper34_audit_2026/P34c_gp4_window_fixed_volume.py   (needs ~20 GB of memory)
"""
import os, sys, io, gc, json, math, time, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
GPD = os.path.join(REPO, "real_research", "generated_phantom_2026")
MUTATE = os.environ.get("MUTATE", "0") == "1"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "P34c", "mutate": MUTATE, "checks": {}, "numbers": {}}


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
    P("  *** MUTATE=1: no free streaming (T = 1); H must FAIL ***")

G3 = load(os.path.join(GPD, "GP3_lensing_power_and_growth.py"),
          "# ============================================================================================ M1 control", "gp3")
GP0, ZS = G3["GP0"], G3["ZS"]
GP4J = json.load(open(os.path.join(GPD, "GP4_generated_phantom_plus_kicked_carrier_results.json")))["numbers"]
L364 = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L364_replacement_carrier_cosmic_shear_results.json")))["numbers"]
MS3J = json.load(open(os.path.join(REPO, "real_research", "mond_sector_gate_2026", "MS3_cosmic_shear_bound_mond_sector_results.json")))["numbers"]
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
KG = (0.1, 0.2, 0.3, 0.5, 0.7, 1.0)
WINDOW = [(0.95, 1200.0), (0.9, 1400.0)]
T05 = {(r["fd"], r["vk"]): r["T05"] for r in L364["scan"]}
dn, bh, _ = GP0.mass_function(ZS)                                  # MS3's census inputs, same calls
LMH = np.arange(10.0, 15.51, 0.05)


def census(mk, L):
    Vc = mk["dx"] ** 3; Vbox = L ** 3; out = {}
    for lM in (13.5, 14.0, 14.5):
        thr = float(GP0.M_bound(10 ** lM, ZS, "observed"))
        sel = LMH >= lM
        out[str(lM)] = {"cells_with_bound_baryons_above": int((mk["rhoB"] * Vc >= thr).sum()),
                        "expected_halos_above": float(np.trapz(np.interp(LMH[sel], GP0.LM, dn), LMH[sel] * math.log(10))) * Vbox}
    return out


def shear_input(mk, lam, a0):
    ms = G3["measure"](mk, lam, a0)
    kh = ms["kh"]; Pnl = G3["PNL_of"](kh)
    s2 = ms["Ppp"] / Pnl; rx = ms["Pxx"] / np.sqrt(np.maximum(ms["Pmm"] * ms["Ppp"], 1e-300))
    _, _, Rc, _ = G3["ratios"](ms)
    del ms; gc.collect()
    return {"kh": kh, "s2_bin": s2, "rx_bin": rx, "Rc": {q: float(np.interp(q, kh, Rc)) for q in KG}}


def shear_R(sh, T05c, T_on=True):
    kh = sh["kh"]
    if T_on:
        lk = np.log([float(q) for q in KG]); Tv = np.array([T05c[str(q)] for q in KG])
        T = np.interp(np.log(kh), lk, Tv)
    else:
        T = np.ones_like(kh)
    sb = np.sqrt(np.maximum(sh["s2_bin"], 0.0))
    Rb = T * T + 2 * sh["rx_bin"] * T * sb + sb * sb
    return {q: float(np.interp(q, kh, Rb)) for q in KG}


banner("D1  THE CLUSTER CENSUS OF EVERY BOX (MS3's method)")
CEN = {"200/256": census(G3["MK"], 200.0)}
SH = {("200/256", f): shear_input(G3["MK"], 1.0, A0[f]) for f in A0}
mk100 = G3["build_mock"](100.0, 256, 20260926)
CEN["100/256"] = census(mk100, 100.0); del mk100; gc.collect()
P(f"  256^3 boxes counted and the 200 Mpc box measured   [{time.time() - T0:.0f}s]")
mk512 = G3["build_mock"](200.0, 512, 20260925)
CEN["200/512"] = census(mk512, 200.0)
P(f"  200 Mpc / 512^3 box built (cell {mk512['dx']:.3f} Mpc)   [{time.time() - T0:.0f}s]")
for f in A0:
    SH[("200/512", f)] = shear_input(mk512, 1.0, A0[f])
    P(f"    measured {f}   [{time.time() - T0:.0f}s]")
del mk512; gc.collect()
for box, c in CEN.items():
    P(f"    {box:8s}: " + "; ".join(f">= 1e{lM}: {v['cells_with_bound_baryons_above']} cells vs {v['expected_halos_above']:.1f} expected" for lM, v in c.items()))
OUT["numbers"]["census"] = CEN

banner("CONTROLS")
dev1 = 0.0
for fd, vk in WINDOW:
    cell = [r for r in GP4J["scan"] if r["lam"] == 1.0 and r["fd"] == fd and r["vk"] == vk][0]
    for f in A0:
        dev1 = max(dev1, abs(max(shear_R(SH[("200/256", f)], T05[(fd, vk)]).values()) - cell["shear"][f]))
check("C1 CONTROL: the 200 Mpc / 256^3 box reproduces GP4's committed cosmic-shear scores for its two window cells (1e-9)", dev1 < 1e-9, f"max |diff| = {dev1:.1e}")
m1ok = all(CEN["100/256"][k]["cells_with_bound_baryons_above"] == MS3J["M1"][k]["cells_with_bound_baryons_above"]
           and abs(CEN["100/256"][k]["expected_halos_above"] - MS3J["M1"][k]["expected_halos_above"]) < 1e-6 for k in MS3J["M1"])
check("C2 CONTROL: the census of the 100 Mpc box reproduces MS3's committed M1 counts exactly", m1ok,
      {k: (CEN["100/256"][k]["cells_with_bound_baryons_above"], MS3J["M1"][k]["cells_with_bound_baryons_above"]) for k in MS3J["M1"]})

banner("H  GP4's WINDOW CELLS IN THE 200 Mpc BOX AT TWICE THE RESOLUTION (512^3, lambda = 1 Mpc)")
res = {}
for fd, vk in WINDOW:
    for box in ("200/256", "200/512"):
        w = {f: max(shear_R(SH[(box, f)], T05[(fd, vk)], T_on=not MUTATE).values()) for f in A0}
        res[(fd, vk, box)] = w
        P(f"    cell f_d(0) {fd}, v_k {vk:.0f}, {box}: worst R canonical {w['canonical']:.3f}, alt {w['alt']:.3f}")
OUT["numbers"]["window"] = {f"{fd}|{vk:.0f}|{box}": v for (fd, vk, box), v in res.items()}
drift = {f: {q: SH[("200/512", f)]["Rc"][q] / SH[("200/256", f)]["Rc"][q] - 1 for q in (0.3, 0.5, 0.7, 1.0)} for f in A0}
OUT["numbers"]["kernel_alone_drift"] = drift
P("    kernel-alone ratio, 512^3 / 256^3 - 1 at k 0.3/0.5/0.7/1: " + "; ".join(f"{f} " + " / ".join(f"{drift[f][q]:+.3f}" for q in (0.3, 0.5, 0.7, 1.0)) for f in A0))
fine_pass = {f"{fd}|{vk:.0f}": all(res[(fd, vk, "200/512")][f] <= 1.2 for f in A0) for fd, vk in WINDOW}
check("H GP4's two window cells pass cosmic shear (worst R <= 1.2, k = 0.1-1, both footings) in the 200 Mpc box at twice the "
      "resolution", all(fine_pass.values()), {f"{fd}|{vk:.0f}": {f: round(res[(fd, vk, '200/512')][f], 3) for f in A0} for fd, vk in WINDOW})

banner("VERDICT")
nlb = sum(1 for _, ok, lb in CH if lb and not ok)
P(f"  window cells passing at 512^3 in 200 Mpc: {[k for k, v in fine_pass.items() if v]}")
P(f"  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nlb}   [{time.time() - T0:.0f}s]")
fn = os.path.join(HERE, "P34c_gp4_window_fixed_volume_results" + ("_MUTATE" if MUTATE else "") + ".json")
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"  wrote {os.path.basename(fn)}")
sys.exit(1 if nlb else 0)
