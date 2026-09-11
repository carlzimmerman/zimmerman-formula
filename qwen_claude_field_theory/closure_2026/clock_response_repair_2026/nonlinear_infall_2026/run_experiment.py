#!/usr/bin/env python3
"""Bounded source-amplitude/width study; exits nonzero on failed controls.

No observational fit. a0 is one global diagnostic constant, absent from the
fixed action; neither the force nor the initial data is chosen to obey MOND.
"""
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import simpson

from initial import solve_slice, force_bound


def run():
    rows = []
    for gamma in (0.,1e-6):
        for width in (.05,.3,1.):
            for amplitude in (1e-7,1e-5,1e-3,.05,.5):
                out = solve_slice(amplitude,width,gamma=gamma)
                c = out["coefficients"]
                r = out["r"]
                bound = force_bound(out,amplitude,width)
                assert bound["hypotheses"], "maximum-principle hypotheses not satisfied"
                assert out["equation_relative_residual"] < 1e-7
                assert out["offgrid_equation_relative_residual"] < 1e-6
                assert max(out["time_equation_absolute_residuals"].values()) < 1e-10
                assert np.min(out["g_areal"]) >= -1e-14
                assert np.max(out["g_areal"]-amplitude*bound["C"]) < 1e-12
                assert np.max(-out["delta"])-amplitude*bound["d"] < 1e-12
                a0 = math.sqrt(c["Lambda"]/(32*math.pi))
                index = np.argmin(abs(r-3*width))
                force,newton = out["g_areal"][index],out["gN"][index]
                mond_ratio = -math.expm1(-force/a0)*force/newton
                rows.append(dict(gamma=gamma,width=width,amplitude=amplitude,
                    a0_global_diagnostic=a0,radius=float(r[index]),
                    force=float(force),newton_bare=float(newton),
                    force_ratio=float(force/newton),mond_balance_ratio=mond_ratio,
                    lapse_min=float(np.min(out["N"])),f_min=float(np.min(out["f"])),
                    f_uniform_lower_bound=out["f_lower_bound"],
                    max_eta_over_amplitude=float(np.max(-out["delta"])/amplitude),
                    C_at_radius=float(bound["C"][index]),
                    lean_threshold_at_radius=float(a0*bound["n"][index]/bound["C"][index]**2),
                    coordinate_mass=float(4*math.pi*out["enclosed"][-1]),
                    proper_dust_mass=float(4*math.pi*simpson(out["rho"]*r*r/np.sqrt(out["f"]),x=r)),
                    equation_relative_residual=out["equation_relative_residual"],
                    offgrid_equation_relative_residual=out["offgrid_equation_relative_residual"],
                    time_equation_absolute_residuals=out["time_equation_absolute_residuals"],
                    collocation_nodes=out["collocation_nodes"]))
    scaling = []
    for gamma in (0.,1e-6):
        for width in (.05,.3,1.):
            part = [row for row in rows if row["gamma"]==gamma and row["width"]==width]
            small,larger = part[0],part[2]
            slope = math.log(larger["force"]/small["force"])/math.log(larger["amplitude"]/small["amplitude"])
            scaling.append(dict(gamma=gamma,width=width,measured_log_slope=slope))
            assert abs(slope-1.) < .001, "source scaling changed in the tested range"
    return dict(status="bounded_initial_slice_computations_passed",cases=rows,
                scaling=scaling,interpretation="initial expanding normal-rest slice, not a stationary galaxy",
                non_claims=["no finite-time nonlinear evolution", "no new empirical fit",
                  "no cosmological/PPN/stability/DOF certificate", "no derived a0 or coefficient selection",
                  "no full-theory no-go; no exclusion of late-time nonperturbative branch"])


if __name__ == "__main__":
    result = run()
    destination = Path(__file__).resolve().parent/"run_001"
    destination.mkdir(exist_ok=True)
    (destination/"experiment.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"case_count":len(result["cases"]),
                      "scaling":result["scaling"],
                      "max_lapse_residual":max(row["equation_relative_residual"] for row in result["cases"])},indent=2))
