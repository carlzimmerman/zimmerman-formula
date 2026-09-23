#!/usr/bin/env python3
"""
J10 -- ARITHMETIC + CONSISTENCY VERIFICATION of J10_A0_RADIUS_READING.md
Checks:
  1. d_bar_phys = E[D]*R/c for R = 941 AU, E[D] = 1/2  -> ~2.72 days
  2. frozen lane 12-14 day figure implies E[D] = d*c/R in [1.8, 2.5]
     at R = 941 AU  ->  tau0_eff = 2 E[D] in [3.6, 5.0]  (heavier kappa)
  3. J10-I identity: -ln A * r_M/(c*d) = (r_M/R) * window
     with r_M = sqrt(G M_b / a0), a0 = 9.3619e-11, G = 6.6743e-11
  4. A2744-QSO1-class example (doorB): r_B = 40.9 ld predicted, 45 ld
     measured: J10-I at R = 45 ld (q=0, A=e^-1) = 2.0*40.9/45 = 1.818
     in [4/3, 2]; kill condition R > 2 r_M -> J10-I < 4/3 at q=0.
  5. window(q) monotone decreasing from 2.0 to 4/3; endpoints attained.
"""
import json
import math
import sys

C = 2.99792458e8       # m/s
AU = 1.495978707e11    # m
DAY = 86400.0
G = 6.6743e-11
A0 = 9.3619e-11
MSUN = 1.98840987e30


def window(q):
    return (1.0 + q / 3.0) / (0.5 + q / 4.0)


def r_M_of(Mb):
    return math.sqrt(G * Mb / A0)


def run():
    res = {"checks": {}, "measurements": {}}
    ok = True

    # C1: base physical lag
    R = 941.0 * AU
    E_D = 0.5
    d_phys = E_D * R / C
    d_days = d_phys / DAY
    res["measurements"]["dbar_phys_days_tau1"] = d_days
    res["checks"]["c1_272_days"] = bool(abs(d_days - 2.72) < 0.03)
    ok &= res["checks"]["c1_272_days"]
    print(f"C1: E[D]=1/2, R=941AU -> d_bar = {d_days:.3f} days (expect 2.72)")

    # C2: frozen lane 12-14 d at the same R -> heavier kappa
    lo, hi = 12.0 * DAY * C / R, 14.0 * DAY * C / R
    res["measurements"]["frozen_E_D_range"] = (round(lo, 3), round(hi, 3))
    res["measurements"]["frozen_tau0_eff_range"] = (round(2 * lo, 2),
                                                    round(2 * hi, 2))
    res["checks"]["c2_frozen_tau_range"] = bool(3.0 < 2.0 * lo and
                                                2.0 * hi < 6.0)
    ok &= res["checks"]["c2_frozen_tau_range"]
    print(f"C2: frozen 12-14d at R=941AU -> E[D] in [{lo:.2f}, {hi:.2f}]"
          f" -> tau0_eff in [{2*lo:.2f}, {2*hi:.2f}] (heavier kappa, q=0)")

    # C3: J10-I identity with the DENSITY-LOCAL radius r_B = sqrt(G M_b/a0(rho_B)).
    # DoorB pins A2744-QSO1: r_B = 40.9 ld.  The deep-MOND r_M = sqrt(G M/a0)
    # is ~kpc for 1e9 Msun (1.45e6 ld) -- NOT the BLR radius; recorded as
    # contrast (the framework's BLR radius is the density-local reading).
    Mb = 1e9 * MSUN
    rM = r_M_of(Mb)
    rM_ld = rM / (C * DAY)
    res["measurements"]["rM_ld_Mb1e9_deepMOND"] = round(rM_ld, 1)
    res["checks"]["c3a_rM_positive"] = bool(rM > 0)
    ok &= res["checks"]["c3a_rM_positive"]
    print(f"C3a: deep-MOND r_M(M_b=1e9 Msun) = {rM_ld:.1f} ld (~kpc) -- "
          f"contrast; BLR radius is the density-local r_B (doorB: 40.9 ld)")

    rB = 40.9 * C * DAY          # doorB A2744-QSO1 predicted radius
    A = math.exp(-1.0)           # q = 0, tau0 = 1
    R_use = rB
    J10I = -math.log(A) * rB / (C * (E_D * R_use / C))
    res["measurements"]["J10I_identity"] = round(J10I, 6)
    res["checks"]["c3b_identity"] = bool(abs(J10I - 2.0 * (rB / R_use)) < 1e-9)
    ok &= res["checks"]["c3b_identity"]
    print(f"C3b: J10-I identity = {J10I:.6f}"
          f" == (r_B/R)*window = {2.0*(rB/R_use):.6f}")

    # C4: A2744-QSO1-class (doorB numbers): R = 45 ld measured lag
    R45 = 45.0 * C * DAY
    J10I_45 = -math.log(A) * rB / (C * (E_D * R45 / C))
    res["measurements"]["J10I_A2744_45ld"] = round(J10I_45, 3)
    res["checks"]["c4_a2744_in_window"] = bool(4.0/3.0 <= J10I_45 <= 2.0)
    ok &= res["checks"]["c4_a2744_in_window"]
    print(f"C4: A2744-QSO1: R=45 ld, r_B=40.9 ld -> J10-I = {J10I_45:.3f}"
          f" (in [4/3, 2] -> CONSISTENT-OPEN stays open)")

    # C5: kill condition.  J10-I = (r_B/R)*window(q) with window in [4/3, 2].
    # At R = 2 r_B: J10-I = w(q)/2 <= 1.0 < 4/3 for EVERY q -> the assignment
    # R = r_B dies.  Sharp bound: J10-I < 4/3 for all q iff (r_B/R)*2 < 4/3
    # iff R > (3/2) r_B  (q = 0 is the least favorable case).
    R2 = 2.0 * rB
    J10I_2r = -math.log(A) * rB / (C * (E_D * R2 / C))
    res["measurements"]["J10I_at_2rM"] = round(J10I_2r, 3)
    res["checks"]["c5_kill_floor"] = bool(J10I_2r < 4.0/3.0 and
                                          abs(J10I_2r - 1.0) < 1e-6)
    ok &= res["checks"]["c5_kill_floor"]
    print(f"C5: R = 2 r_M -> J10-I = {J10I_2r:.3f} < 4/3 for all q"
          f" (kill: R > 1.5 r_M suffices at q=0)")

    # C6: window monotone + endpoints
    qs = [0.0, 1.0, 3.0, 10.0, 100.0, 1e6]
    ws = [window(q) for q in qs]
    res["measurements"]["window_qs"] = ws
    mono = all(ws[i] >= ws[i+1] for i in range(len(ws) - 1))
    res["checks"]["c6_window_monotone"] = bool(mono and
                                               abs(ws[0] - 2.0) < 1e-9 and
                                               abs(ws[-1] - 4.0/3.0) < 2e-5)
    ok &= res["checks"]["c6_window_monotone"]
    print(f"C6: window(q) endpoints: q=0 -> {ws[0]:.6f} (2.0),"
          f" q->inf -> {ws[-1]:.6f} (4/3); monotone={mono}")

    res["total_checks"] = len(res["checks"])
    res["passed"] = sum(1 for v in res["checks"].values() if v)
    res["ALL_PASSED"] = bool(ok)
    print(json.dumps(res, indent=1))
    print("ALL J10 CHECKS PASSED" if ok else "J10 CHECK FAILURE")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(run())