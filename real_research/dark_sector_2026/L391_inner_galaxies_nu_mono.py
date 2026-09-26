#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L391 -- L376's RAR and RC100 gates re-scored with the construction's OWN kernel, nu_mono (L340's monotone kernel), in place
of the nu_RAR L376 used.

WHY.  The cross-thread consistency registry (XR1) flagged that L376 computes g_MOND with nu_RAR, while every construction
lane (L340, L352, L377, L388) uses nu_mono -- identical to nu_RAR below the phantom peak y_p = 2.54 and a monotone
continuation above it.  L376's verdict rests on the carrier's contribution g_c (~0 inside galaxies), which does not depend
on the kernel, but the RC100 dark fractions and the gate denominators do.  This lane closes that ledger item.

METHOD: L376's halo2() imported unchanged (same hosts, seeds, redshifts, trigger); L377's nu_vec (the nu_mono table,
equal to L352's by L377's C2) as the kernel; L376's gate arithmetic, with the kernel as the only change.
PRE-DECLARED (before the run): H: with nu_mono the RAR gate (carrier shift <= 0.057 dex at 2, 4, 8 R_d, three hosts, both
footings) and the RC100 inner-clearing gate (carrier inside R_e at z = 1, 2 <= 0.30 of LCDM's) still pass.
CHECKS
  C1 CONTROL: with nu_RAR the same halos reproduce L376's committed RAR shifts and RC100 f_DM values exactly.
  R1 = H.  W (informational): the nu_mono f_DM(<R_e) at z = 1, 2 beside L376's nu_RAR values.
MUTATE=1: v_k = 0 in every decaying run: R1 must FAIL (rc = 1).
SCOPE: the trigger is L376's matter-only (least-trigger) one, as L375/L376/L390; the cosmological lanes use the
phantom-inclusive trigger (XR1 item 6).

Run from the repository root:  python3 real_research/dark_sector_2026/L391_inner_galaxies_nu_mono.py
"""
import os, sys, json, math, time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import L376_triggered_carrier_inner_galaxies as L76             # noqa: E402  (L376's shell model and gate arithmetic)
from L377_full_construction_pm import nu_vec as nu_mono          # noqa: E402  (the construction's kernel)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L391_inner_galaxies_nu_mono"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L391", "mutate": MUTATE, "checks": {}, "numbers": {}, "kernel": "nu_mono (L340/L352/L377)",
               "trigger": "matter-only (least-trigger), as L376"}
EXPECT_PASS = True                                               # H, set before the run
G, KMS2_KPC, A0, interp_log = L76.G, L76.KMS2_KPC, L76.A0, L76.interp_log
HOSTS = {"dwarf": (1e11, 3e9), "milky_way": (1e12, 6e10), "massive": (5e12, 2e11)}


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


if __name__ == "__main__":
    P(__doc__)
    N = int(os.environ.get("L391_N", "60000"))
    VK = 0.0 if MUTATE else 650.0
    cfgs = []                                                    # L376's configurations, seeds unchanged
    for i, (hn, (M0, Mb)) in enumerate(HOSTS.items()):
        c0 = L76.c200_dm(M0, 0.0)
        cfgs.append((f"rar_{hn}", M0, c0, Mb, VK, 10.0, 0.75, True, N, 1000 + i, 0.0, 2.75))
        cfgs.append((f"rar_{hn}_nodecay", M0, c0, Mb, 650.0, 0.0, 0.75, True, N, 1100 + i, 0.0, 2.75))
    for zo in (1.0, 2.0):
        c0 = L76.c200_dm(1e12, zo)
        cfgs.append((f"rc_z{zo:.0f}", 1e12, c0, 1e11, VK, 10.0, 0.75, True, N, 2000 + int(zo), zo, zo + 2.75))
        cfgs.append((f"rc_z{zo:.0f}_nodecay", 1e12, c0, 1e11, 650.0, 0.0, 0.75, True, N, 2100 + int(zo), zo, zo + 2.75))
    if MUTATE:
        P("  MUTATE: v_k = 0 in every decaying run")
    with Pool(int(os.environ.get("L391_POOL", "4"))) as pool:
        res = dict(pool.map(L76.halo2, cfgs, chunksize=1))
    P(f"  {len(cfgs)} halos done   [{time.time() - T0:.0f}s]")

    def rar_table(tag, nu):                                      # L376's rar_table(), the kernel as the argument
        d = res[tag]; Rd = 1.08 * d["ab"]; rows = {}
        for f_, a0 in A0.items():
            for k in (2, 4, 8):
                rk = k * Rd
                gN = G * interp_log(rk, d["r"], d["Mbar"]) / rk ** 2 * KMS2_KPC
                gM = nu(gN / a0) * gN
                gc = G * interp_log(rk, d["r"], np.maximum(d["Mc"], 1e-30)) / rk ** 2 * KMS2_KPC if np.any(d["Mc"] > 0) else 0.0
                rows[f"{f_}/{k}Rd"] = dict(r_kpc=rk, Delta_dex=float(math.log10(1 + gc / gM)))
        return rows

    def rc_table(nu):                                            # L376's RC100 block, the kernel as the argument
        out = {}
        for zo in (1, 2):
            d, d0 = res[f"rc_z{zo}"], res[f"rc_z{zo}_nodecay"]; Re = 1.815 * d["ab"]
            mc, mc0 = interp_log(Re, d["r"], np.maximum(d["Mc"], 1e-30)), interp_log(Re, d0["r"], d0["Mc"])
            mb = interp_log(Re, d["r"], d["Mbar"]); fr = {}
            for f_, a0 in A0.items():
                gN = G * mb / Re ** 2 * KMS2_KPC; gM = float(nu(gN / a0)) * gN; gc = G * mc / Re ** 2 * KMS2_KPC
                gL = gN + G * mc0 / Re ** 2 * KMS2_KPC
                fr[f_] = dict(fDM_construction=float(1 - gN / (gM + gc)), fDM_lcdm=float(1 - gN / gL))
            out[f"z{zo}"] = dict(Re_kpc=Re, carrier_ratio=mc / mc0, fDM=fr)
        return out

    banner("C1  CONTROL: with nu_RAR the same halos reproduce L376")
    R76 = json.load(open(os.path.join(HERE, "L376_triggered_carrier_inner_galaxies_results.json")))["numbers"]
    dev = 0.0
    if not MUTATE:
        for hn in HOSTS:
            rr_ = rar_table(f"rar_{hn}", L76.nu_rar)
            dev = max(dev, max(abs(rr_[k_]["Delta_dex"] - R76["rar"][hn][k_]["Delta_dex"]) for k_ in rr_))
        rc_ = rc_table(L76.nu_rar)
        dev = max(dev, max(abs(rc_[z]["fDM"][f_]["fDM_construction"] - R76["rc100"][z]["fDM"][f_]["fDM_construction"]) for z in rc_ for f_ in A0))
        check("C1 with nu_RAR the same halos reproduce L376's committed RAR shifts and RC100 f_DM exactly (the kernel is the only change)",
              f"max |difference| {dev:.1e}", dev < 1e-12)

    banner("THE GATES WITH nu_mono")
    RAR = {hn: rar_table(f"rar_{hn}", nu_mono) for hn in HOSTS}
    worst = {hn: max(v["Delta_dex"] for v in RAR[hn].values()) for hn in HOSTS}
    RC = rc_table(nu_mono)
    for hn in HOSTS:
        P(f"    RAR {hn:10s}: worst carrier shift {worst[hn]:.2e} dex (gate 0.057)")
    for z, d in RC.items():
        P(f"    RC100 {z}: carrier inside R_e / LCDM's {d['carrier_ratio']:.3f} (gate 0.30);  f_DM(<R_e) nu_mono: "
          + ", ".join(f"{f_} {v['fDM_construction']:.3f}" for f_, v in d["fDM"].items())
          + f"  (L376 nu_RAR: " + ", ".join(f"{f_} {v['fDM_construction']:.3f}" for f_, v in R76["rc100"][z]["fDM"].items()) + ")")
    OUT["numbers"].update(rar=RAR, rar_worst=worst, rc100=RC)
    check("W (informational) nu_mono f_DM(<R_e) beside L376's nu_RAR values", "see table", True, "reported either way", load_bearing=False)

    banner("R1  THE HYPOTHESIS (set before the run)")
    ok = all(v <= 0.057 for v in worst.values()) and all(d["carrier_ratio"] <= 0.30 for d in RC.values())
    check("R1 = H: with nu_mono the RAR gate (<= 0.057 dex) and the RC100 inner-clearing gate (<= 0.30) still pass",
          f"RAR worst {worst}; RC100 carrier ratio { {z: round(d['carrier_ratio'], 3) for z, d in RC.items()} }", ok == EXPECT_PASS)

    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
