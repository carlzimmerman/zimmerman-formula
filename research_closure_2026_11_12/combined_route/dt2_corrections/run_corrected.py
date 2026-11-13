"""Bounded corrected benchmarks; writes only the explicitly supplied fresh result.

Non-claims: no post-caustic continuation, no full cosmological perturbation solve,
no universal kinetic-function exclusion, no observational parameter inference.
"""
import argparse
import json
import sys
from pathlib import Path
import math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "hy4_preview_push/CLOSE-1_DT2"))
import dt2_function as D
import dt2_linear as L
import dt2_form as F
import dt2_reach as R


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", required=True)
    parser.add_argument("--formation", action="store_true")
    args = parser.parse_args()
    out = {"time": {}, "growth": [], "band_candidates": [], "formation": []}
    h0 = 70e3/D.MPC
    h = lambda a: h0*math.sqrt(.31*a**-3+.69)
    expected = quad(lambda a: 1/(a*h(a)), 1/11, 1)[0]
    for module in (F, R):
        elapsed = float(module.T_OF_A(1)-module.T_OF_A(1/11))
        out["time"][module.__name__] = {"Gyr_z10_to_0": elapsed/(1e9*F.YR),
                                       "relative_error_vs_quadrature": elapsed/expected-1}
    for k in (20/3, 2, .2, .02):
        dt2 = L.growth_factor(k, 1/7)
        ref = L.growth_factor(k, 1/7, dt2=False)
        out["growth"].append({"k_com_Mpc": k, "D_DT2": dt2, "D_ref": ref,
                              "ratio": dt2/ref, "frozen_K1_pass": bool(dt2/ref >= .5)})

    # Existing family, changed support only. All choices stated in the contract.
    # No outcome selects a new preferred model or changes the old gates.
    original = D.Q1, D.Q2
    try:
        for name, q1, q2 in (("original", 2, 26), ("intermediate", 30, 216),
                              ("early_collapse", 1500, 5000),
                              ("higher_density", 2000, 10000)):
            D.Q1, D.Q2 = q1, q2
            qwell = brentq(lambda q: float(D.x_of_q(q))-D.PHI_DEEPEST,
                           1, 1e7, xtol=1e-9)
            growth = L.growth_factor(20/3, 1/7)/L.growth_factor(20/3, 1/7, dt2=False)
            out["band_candidates"].append({"name": name, "q1": q1, "q2": q2,
                "q_at_phi_4e_minus6": qwell,
                "local_static_density_cap_pass": bool(qwell <= D.CAP_GALAXY),
                "growth_ratio": growth, "frozen_K1_pass": bool(growth >= .5),
                "compression_from_q1331_can_enter_support": bool(q2 > 1331),
                "x_at_static_cap": float(D.x_of_q(D.CAP_GALAXY))})
    finally:
        D.Q1, D.Q2 = original

    # Homogeneous benchmark of the implemented force: at uniform cold density
    # pressure and polarization vanish. Missing baryons/Lambda are thus explicit.
    out["background_force_scope"] = {
        "implemented_acceleration_over_H0sq_r": "-Omega_c/(2*a^3)",
        "required_flat_LCDM_acceleration_over_H0sq_r": "-Omega_m/(2*a^3)+Omega_L",
        "Omega_c": D.OMEGA_C, "Omega_m": F.OM_M, "Omega_L": 1-F.OM_M,
        "cosmological_background_limit_pass": False,
        "interpretation": "Formation numbers below are reduced-code diagnostics only."}
    if args.formation:
        for footing, a0 in (("canonical", D.A0_CANON), ("alt", D.A0_ALT)):
            for n in (130, 260, 520):
                res = F.run(10.45, a0, N=n, max_steps=60000, absorb=False)
                event = res["first_fold"]
                row = {"footing": footing, "N": n, "log_Mb": 10.45,
                    "first_event_kind": res["first_event_kind"],
                    "first_event_Gyr": None if event is None else
                        (event-float(F.T_OF_A(1/11)))/(1e9*F.YR),
                    "termination": res["termination_reason"],
                    "reached_z0": res["reached_z0"],
                    "end_z": 1/float(F.A_OF_T(res["t_end"]))-1,
                    "steps": res["iters"],
                    "q_max": float(np.max(D.n_of_x(res["h"]/D.C_SI**2))/D.N0),
                    "R_set_z0": None, "settled_mass_residual": None}
                out["formation"].append(row)
                print(json.dumps(row), flush=True)
    out["conclusion"] = "K1 fails at 20/3 Mpc^-1; no physical present-day formation verdict."
    Path(args.result).write_text(json.dumps(out, indent=2, allow_nan=False)+"\n")
    print(json.dumps(out, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
