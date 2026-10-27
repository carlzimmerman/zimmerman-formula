"""Bounded kinetic ledger and stopping-sign checks; no halo simulation."""
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp


def energy(v):
    return sum(F(x)**2 for x in v)/2


channels = [
    [(2, 0, 0), (0, 0, 0), (1, 1, 0), (1, -1, 0)],
    [(0, 2, 0), (0, 0, 0), (0, 1, 1), (0, 1, -1)],
]
collision_records = []
for velocities in channels:
    moment = [sum((-1 if i < 2 else 1)*F(velocities[i][j])
                  for i in range(4)) for j in range(3)]
    en = sum((-1 if i < 2 else 1)*energy(velocities[i]) for i in range(4))
    vals = [F(4), F(1), F(2), F(1)]
    flux = vals[0]*vals[1]-vals[2]*vals[3]
    hdot = -float(flux)*math.log(float(vals[0]*vals[1]/(vals[2]*vals[3])))
    collision_records.append({"momentum_residual": list(map(str, moment)),
                              "energy_residual": str(en), "mass_residual": "0",
                              "entropy_H_derivative": hdot})

# Positive eight-beam distribution, rho=1/10, mean zero, full-rank stress.
beams = []
for vx, wx in [(-1, F(2, 3)), (2, F(1, 3))]:
    for vy in [-1, 1]:
        for vz in [-1, 1]:
            beams.append(((vx, vy, vz), F(1, 10)*wx/F(4)))
rho = sum(w for v, w in beams)
u = [sum(w*v[j] for v, w in beams)/rho for j in range(3)]
pi = [[sum(w*(F(v[j])-u[j])*(F(v[k])-u[k]) for v, w in beams)
       for k in range(3)] for j in range(3)]
q = [sum(w*(F(v[j])-u[j])*sum((F(v[k])-u[k])**2 for k in range(3))/2
         for v, w in beams) for j in range(3)]
detpi = pi[0][0]*pi[1][1]*pi[2][2]


def activation(s):
    z = s**4
    return max(z-1, 0)/(1+z)


def run_case(s0, h0, b, duration=200):
    def rhs(t, y):
        exchange = activation(y[0])*(y[1]-y[0])
        return [-exchange, -exchange/b]
    def collapse(t, y):
        return y[0]-10
    collapse.terminal = True
    collapse.direction = 1
    sol = solve_ivp(rhs, [0, duration], [s0, h0], rtol=1e-10, atol=1e-12,
                    max_step=.2, events=collapse)
    s, h = sol.y
    E = -s+b*h
    production = np.array([activation(si)*(hi-si)**2/(si*hi)
                           for si, hi in zip(s, h)])
    return {"s0": s0, "h0": h0, "b": b,
            "s_final": float(s[-1]), "h_final": float(h[-1]),
            "Sigma_over_target_final": float(s[-1]**2),
            "time_final": float(sol.t[-1]),
            "energy_max_error": float(np.max(np.abs(E-E[0]))),
            "minimum_entropy_production": float(production.min()),
            "solver_success": bool(sol.success),
            "hit_collapse_stop": bool(len(sol.t_events[0]))}


cases = {
    "expanding_core": run_case(1.3, 2., 4.),
    "contracting_core": run_case(1.3, .8, 4.),
    "below_floor": run_case(.9, 2., 4.),
    "small_envelope_thermal_stable": run_case(1.3, 1.4, .5),
}
baseline = cases["expanding_core"]
impulse = .05  # Added core energy / (C0 T_star), after the baseline run.
cases["heat_impulse_after_stopping"] = run_case(
    baseline["s_final"]-impulse, baseline["h_final"], 4.)
pre = -baseline["s_final"]+4*baseline["h_final"]
post = -cases["heat_impulse_after_stopping"]["s_final"]+4*cases["heat_impulse_after_stopping"]["h_final"]

checks = {
    "exact_elastic_momentum_energy": all(
        r["momentum_residual"] == ["0", "0", "0"] and r["energy_residual"] == "0"
        for r in collision_records),
    "elastic_H_decreases": all(r["entropy_H_derivative"] < 0 for r in collision_records),
    "beam_mean_zero": u == [0, 0, 0],
    "gate_off_full_rank_nonzero_heat_flux": detpi > 0 and detpi < 1 and q[0] == F(1, 10),
    "expansion_reaches_inserted_threshold": abs(cases["expanding_core"]["s_final"]-1) < 1e-7,
    "outward_heat_runs_away": cases["contracting_core"]["hit_collapse_stop"],
    "below_floor_not_restored": cases["below_floor"]["s_final"] == .9,
    "finite_small_envelope_equilibrates_above_floor": abs(cases["small_envelope_thermal_stable"]["s_final"]-1.2) < 1e-7,
    "external_heat_breaks_floor": cases["heat_impulse_after_stopping"]["s_final"] < 1,
    "impulse_energy_accounted": abs(post-pre-impulse) < 1e-12,
    "all_energy_ledgers": all(r["energy_max_error"] < 1e-10 for r in cases.values()),
    "all_entropy_production_nonnegative": all(r["minimum_entropy_production"] >= 0 for r in cases.values()),
    "all_ODE_solvers_succeeded": all(r["solver_success"] for r in cases.values()),
}
result = {"collision_channels": collision_records,
          "beam_counterexample": {"rho": str(rho), "u": list(map(str, u)),
              "Pi": [[str(x) for x in row] for row in pi],
              "det_Pi": str(detpi), "heat_flux": list(map(str, q)),
              "P_star": 1, "geometric_pressure_ratio": float(detpi)**(1/3)},
          "two_zone_cases": cases, "external_heat_impulse": impulse,
          "checks": checks,
          "interpretation": "Conserving elastic mixing and an imposed one-sided conductive stop are possible; collision deactivation alone does not stop heat flux, derive its pressure scale, or restore below-floor cores."}
Path(sys.argv[1]).write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
assert all(checks.values()), checks
