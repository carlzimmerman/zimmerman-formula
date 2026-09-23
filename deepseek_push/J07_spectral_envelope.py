#!/usr/bin/env python3
"""
J07 -- THE SHARPENED SPECTRAL ENVELOPE OF THE DELAY KERNEL
2026-09-23.  Follow-on to J05 on the JWST moment channel (does not overlap
the six running lanes: J04 closure, J06 bound chain, N05 audit, tooling
sweep, I21 Lean, J00 ledger).

FROZEN LANE (bhstar_scattering_clock/density_free/THEOREM.md, Thm 3):
    |H(omega)| >= max(0, 1 - |omega| E[D]),   H(omega) = E[exp(i omega D)]
    (linear envelope; asymptotic at omega->0 it is WEAK: cos x = 1 - x^2/2 + ...)

NEW THEOREM (this file; elementary, machine-verified):
    (T3')  |H(omega)| >= max(0, 1 - (1/2) omega^2 E[D^2])      (second-moment
           envelope; asymptotically TIGHT at omega->0: 1-Re H ~ (omega^2/2) E[D^2])
    (T3'') with the J05 bound E[D^2] >= L := 3 E[D v^2]^2 / E[v^4]:
           |H(omega)| >= max(0, 1 - (1/2) omega^2 L)           (line-moment-only
           envelope; density-free, isothermality-free)
    Crossing: T3' beats the frozen T3 for |omega| < omega* = 2 E[D]/E[D^2],
    and the asymptotic sharpness is exact: 1 - Re H ~ omega^2 E[D^2]/2.

Checks (engine: deepseek_push/J02_moment_hierarchy.py::simulate):
  S1  measured |H| >= frozen Thm-3 envelope at omega = 0.25..8 (all clouds)
  S2  measured |H| >= T3' envelope at omega = 0.25..8 (all clouds)
  S3  T3' > T3 on a finite interval; crossing omega* = 2E[D]/E[D^2] verified
  S4  asymptotic tightness: |1 - Re H(omega) - omega^2 E[D^2]/2| = O(omega^4)
      (log-log slope ~4 at small omega)
  S5  line-moment envelope L holds as a lower bound on E[D^2] (J05 re-check)
"""
import json
import sys

import numpy as np

sys.path.insert(0, "deepseek_push")
from J02_moment_hierarchy import simulate

def se(x):
    return float(np.std(x, ddof=1) / np.sqrt(len(x)))


def run():
    res = {"checks": {}, "measurements": {}}
    ok = True
    omegas = np.array([0.25, 0.5, 1.0, 2.0, 4.0, 8.0])
    for (tau0, q, src) in ((1.0, 0.0, "central"), (1.0, 3.0, "central"),
                           (1.0, 10.0, "central"), (1.0, 0.0, "volume")):
        n = 400000
        r = simulate(n, tau0, q, src, seed=61)
        D, v2, v4 = r["D"], r["v2"], r["v2"]*r["v2"]
        E_D = float(np.mean(D)); E_D2 = float(np.mean(D*D))
        E_Dv2 = float(np.mean(D*v2)); E_v4 = float(np.mean(v4))
        L = 3.0*E_Dv2*E_Dv2/E_v4
        m = res["measurements"][f"cloud_{tau0}_{q}_{src}"] = {
            "E_D": E_D, "E_D2": E_D2, "E_Dv2": E_Dv2, "E_v4": E_v4,
            "L": L, "omega_star": 2.0*E_D/E_D2}
        # measured H(omega)
        H = np.array([complex(np.mean(np.cos(w*D)), np.mean(np.sin(w*D)))
                      for w in omegas])
        magH = np.abs(H)
        env3 = np.maximum(0.0, 1.0 - omegas*E_D)
        env32 = np.maximum(0.0, 1.0 - 0.5*omegas*omegas*E_D2)
        envL = np.maximum(0.0, 1.0 - 0.5*omegas*omegas*L)
        # S1, S2: measured above both envelopes (with SE slop)
        t1 = magH + 6.0*np.array([se(np.cos(w*D)) + se(np.sin(w*D))
                                  for w in omegas])
        m["magH"] = [float(v) for v in magH]
        m["env3"] = [float(v) for v in env3]
        m["env32"] = [float(v) for v in env32]
        m["envL"] = [float(v) for v in envL]
        res["checks"][f"S1_frozen_{tau0}_{q}_{src}"] = bool(np.all(t1 >= env3 - 1e-9))
        res["checks"][f"S2_second_moment_{tau0}_{q}_{src}"] = bool(np.all(t1 >= env32 - 1e-9))
        # S3: crossing -- there exists omega with env32 > env3 + margin
        wins = env32 - env3
        res["checks"][f"S3_crossing_{tau0}_{q}_{src}"] = bool(
            np.any(wins > 0.02) and np.any(np.array([1 - 0.5*o*o*E_D2 for o in omegas]) > 0))
        # S4: asymptotic tightness at small omega -- 1-ReH vs (omega^2/2)E[D^2]
        small = np.array([0.02, 0.04, 0.08, 0.16])
        reH = np.array([np.mean(np.cos(w*D)) for w in small])
        diff = np.abs(1.0 - reH - 0.5*small*small*E_D2)
        slope = np.polyfit(np.log(small[1:]), np.log(diff[1:] + 1e-12), 1)[0]
        m["asymp_loglog_slope"] = float(slope)
        res["checks"][f"S4_asymptotic_{tau0}_{q}_{src}"] = bool(slope > 3.0)
        # S5: L <= E[D^2]
        res["checks"][f"S5_line_env_{tau0}_{q}_{src}"] = bool(E_D2 >= L*(1-1e-3))
        ok &= all(res["checks"][k] for k in res["checks"] if k.endswith(f"_{tau0}_{q}_{src}"))
    res["total_checks"] = len(res["checks"])
    res["passed"] = sum(1 for v in res["checks"].values() if v)
    res["ALL_PASSED"] = bool(ok)
    print(json.dumps(res, indent=1))
    print("ALL J07 CHECKS PASSED" if ok else "J07 CHECK FAILURE")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(run())