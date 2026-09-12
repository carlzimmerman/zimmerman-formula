#!/usr/bin/env python3
"""Independent C003 on-shell recoil audit; deterministic, exact + 80-digit checks.

Units: c=1 in derivations. Numeric speeds are km/s, c=299792.458 km/s.
No galaxy fit, CLASS run, cosmological inference, or amplitude is implemented.
"""
import argparse
import json
import platform
from pathlib import Path

import mpmath as mp
import sympy as s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[5]
    source = root / "fable_independent_2026/L189_results.json"
    fit = json.loads(source.read_text())
    mp.mp.dps = 80
    checks = []

    def exact(label, expression):
        residue = s.factor(s.together(expression))
        checks.append({"name": label, "zero_residue": str(residue), "passed": residue == 0})
        if residue != 0:
            raise AssertionError((label, residue))

    M, m, mu = s.symbols("M m mu", positive=True)
    ed = (M**2 + m**2 - mu**2) / (2*M)
    ef = (M**2 - m**2 + mu**2) / (2*M)
    p2 = ((M-m-mu)*(M+m+mu)*(M-m+mu)*(M+m-mu))/(4*M**2)
    exact("two_body_energy", ed + ef - M)
    exact("daughter_mass_shell", ed**2 - p2 - m**2)
    exact("scalar_mass_shell", ef**2 - p2 - mu**2)
    exact("released_rest_energy_partition", M-m-mu - ((ed-m)+(ef-mu)))
    b = s.symbols("beta", nonnegative=True)
    q2 = (1-b)/(1+b)
    a = 1/(1+b)
    r = b/(1+b)
    exact("massless_momentum_energy", a+r-1)
    exact("massless_mass_shell", a*a-r*r-q2)
    exact("massless_speed", r/a-b)
    q = s.sqrt(q2)
    exact("massless_rest_loss_is_heat_plus_radiation", (1-q)-((a-q)+r))
    g, y, x = s.symbols("gamma y x", real=True)
    exact("massive_fixed_speed_conservation_polynomial",
          (1-g*x)**2 - (y*y+(g*g-1)*x*x) - (1-2*g*x+x*x-y*y))
    # A rational beta and alleged rest mass avoid any floating verdict decision.
    bfit = s.Rational(str(fit["vk"])) / s.Rational("299792.458")
    alleged_m = 1-bfit*bfit/2
    alleged_residue = s.factor(alleged_m**2 - (1-bfit)/(1+bfit))
    checks.append({"name": "claimed_mass_split_mass_shell_compatibility",
                   "residue": str(alleged_residue),
                   "compatible": alleged_residue == 0})

    beta = mp.mpf(str(fit["vk"])) / mp.mpf("299792.458")
    n = mp.mpf(str(fit["kicks_by_z0"]))
    qn = mp.sqrt((1-beta)/(1+beta))
    an = 1/(1+beta)
    rad = 1-an
    mass_loss = 1-qn
    heat = an-qn
    l189_split = (mp.mpf(str(fit["vk"]))/mp.mpf("299800"))**2/2
    mean_m = mp.exp(n*(qn-1))
    mean_E = mp.exp(n*(an-1))
    summed_m = mp.fsum(mp.exp(-n)*n**k/mp.factorial(k)*qn**k for k in range(60))
    summed_E = mp.fsum(mp.exp(-n)*n**k/mp.factorial(k)*an**k for k in range(60))
    tail = 1-mp.fsum(mp.exp(-n)*n**k/mp.factorial(k) for k in range(60))
    # Tail checks compare independently evaluated finite Poisson sums to PGFs.
    for label, delta in [("poisson_rest_mass_sum_error", abs(summed_m-mean_m)),
                         ("poisson_energy_sum_error", abs(summed_E-mean_E))]:
        checks.append({"name": label, "value": mp.nstr(delta, 55),
                       "tail_upper_bound": mp.nstr(tail, 55),
                       "passed": delta <= tail + mp.mpf("1e-75")})
        assert delta <= tail + mp.mpf("1e-75")

    # Cross-check the fixed-speed massive solution against general two-body
    # kinematics throughout a stated finite deterministic grid.
    grid_b = [mp.mpf(t) for t in ("0", "1e-8", "1e-5", "0.001", "0.01", "0.1", "0.5", "0.9", "0.99")]
    grid_y = [mp.mpf(t) for t in ("0", "1e-6", "0.001", "0.01", "0.1", "0.5", "0.9", "0.99")]
    max_residue = mp.mpf(0)
    massive_rows = []
    for bv in grid_b:
        gamma = 1/mp.sqrt(1-bv*bv)
        qzero = mp.sqrt((1-bv)/(1+bv))
        for yv in grid_y:
            # gamma^2*beta^2 avoids subtracting nearly equal gamma^2 and 1.
            xv = (1-yv*yv)/(gamma+mp.sqrt(gamma*gamma*bv*bv+yv*yv))
            ev = (1+xv*xv-yv*yv)/2
            fv = (1-xv*xv+yv*yv)/2
            pv = gamma*bv*xv
            residues = [ev-gamma*xv, ev*ev-pv*pv-xv*xv,
                        fv*fv-pv*pv-yv*yv, ev+fv-1, pv-bv*ev]
            max_residue = max(max_residue, *(abs(z) for z in residues))
            assert xv > 0 and xv+yv <= 1+mp.mpf("1e-75")
            assert xv <= qzero+mp.mpf("1e-75")
    assert max_residue < mp.mpf("1e-70")
    checks.append({"name": "massive_72_point_grid", "passed": True,
                   "max_absolute_residue": mp.nstr(max_residue, 55)})
    for yv in (mp.mpf("0"), mp.mpf("1e-6"), mp.mpf("0.001"), mp.mpf("0.01"), mp.mpf("0.1"), mp.mpf("0.5")):
        gamma = 1/mp.sqrt(1-beta*beta)
        xv = (1-yv*yv)/(gamma+mp.sqrt(gamma*gamma*beta*beta+yv*yv))
        massive_rows.append({"mu_over_M": mp.nstr(yv, 25), "daughter_rest_loss": mp.nstr(1-xv, 40),
                            "total_final_rest_mass_deficit": mp.nstr(1-xv-yv, 40)})

    one = {"beta": beta, "daughter_mass_ratio": qn,
           "lost_daughter_rest_mass_fraction": mass_loss,
           "daughter_kinetic_energy_over_Mc2": heat,
           "scalar_radiated_energy_over_Mc2": rad,
           "L189_quadratic_split_approx_c": l189_split,
           "true_rest_loss_over_L189_claim": mass_loss/l189_split}
    repeated = {"poisson_mean": n, "L189_linear_mass_loss_proxy": n*l189_split,
                "mean_surviving_rest_mass": mean_m, "mean_surviving_total_energy": mean_E,
                "mean_surviving_kinetic_energy": mean_E-mean_m,
                "mean_rest_mass_lost": 1-mean_m,
                "mean_radiated_energy_initial_frame": 1-mean_E,
                "probability_at_least_two_kicks": 1-mp.exp(-n)*(1+n),
                "max_mean_for_rest_loss_below_0.001": mp.log(mp.mpf("0.999"))/(qn-1),
                "poisson_N_ge_60": tail}
    capacity_rows = []
    for kmax in (1, 2, 5, 8, 10, 12, 20):
        overflow = 1-mp.fsum(mp.exp(-n)*n**k/mp.factorial(k) for k in range(kmax+1))
        capacity_rows.append({"max_transitions": kmax,
                              "P_requested_kicks_exceed_capacity": mp.nstr(overflow, 45),
                              "fractional_rest_mass_reservoir_for_capacity": mp.nstr(1-qn**kmax, 45)})
    result = {
        "scope": "isolated positive-energy on-shell two-body decay; no environment momentum supply",
        "software": {"python": platform.python_version(), "sympy": s.__version__, "mpmath": mp.__version__},
        "precision_decimal_digits": mp.mp.dps,
        "symbolic_checks": checks,
        "series_beta_zero": {"rest_loss": str(s.series(1-q,b,0,5)),
                              "kinetic_energy": str(s.series(a-q,b,0,5)),
                              "radiation": str(s.series(r,b,0,5))},
        "single_massless_event": {k: mp.nstr(v, 55) for k,v in one.items()},
        "fractional_mass_ladder_poisson": {k: mp.nstr(v, 55) for k,v in repeated.items()},
        "reported_gate_threshold": "0.001",
        "reported_gate_L189_proxy_passes": bool(n*l189_split < mp.mpf("0.001")),
        "reported_gate_corrected_rest_loss_passes": bool(1-mean_m < mp.mpf("0.001")),
        "massive_fixed_speed_examples": massive_rows,
        "finite_reservoir_examples": capacity_rows,
        "non_claims": ["No full classical or quantum action is constructed.",
                       "No halo or cosmology observable is recalculated.",
                       "Poisson energy mean assumes event count independent of recoil history and rest-frame isotropic emission.",
                       "Massive grid is finite numerical evidence; formulas are separately derived.",
                       "Lorentz-breaking dispersion, scattering, negative-energy modes, and external pumps are excluded from the isolated-decay obstruction."]}
    args.result.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
