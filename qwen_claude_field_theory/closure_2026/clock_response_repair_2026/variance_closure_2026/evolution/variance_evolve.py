#!/usr/bin/env python3
"""Bounded quadratic-variance test of the existing constrained action.

State entries are RMS real Fourier/quadrature amplitudes, with ensemble
C=<u u^T>. Thus Y2=(k/a)^2 C[0,0]. The action source's cosine amplitude
would be sqrt(2) times this amplitude. All reported physical covariance
quantities use epsilon=1e-6/k, while ODEs evolve dimensionless unit-scaled
covariances so absolute tolerances do not erase the small signal.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
BRIDGE = BASE / "cosmological_bridge_2026"
sys.path.insert(0, str(BRIDGE))
from transfer_evolve import Background, mode_system, diagnose  # noqa: E402

SOURCE_FILES = (
    BRIDGE / "transfer_evolve.py",
    BRIDGE / "background_evolve.py",
    BRIDGE / "derive.py",
    BRIDGE / "transfer_jets.py",
    BASE / "nonlinear_evolution_2026" / "constitutive.py",
)


def covariance_rhs(operator, covariances):
    return operator @ covariances + covariances @ operator.T


def variance_jets(p, H, Hd, operator, operator_rate, covariance):
    """Y, Ydot, Yddot, with all physical-time rates retained."""
    cd = covariance_rhs(operator, covariance)
    cdd = (operator_rate @ covariance + covariance @ operator_rate.T
           + operator @ cd + cd @ operator.T)
    return np.array([
        p * covariance[0, 0],
        p * (cd[0, 0] - 2 * H * covariance[0, 0]),
        p * (cdd[0, 0] - 4 * H * cd[0, 0]
             + (4 * H * H - 2 * Hd) * covariance[0, 0]),
    ])


def forward_rate(function, h):
    """Fourth-order one-sided derivative; never leaves the solved history."""
    weights = np.array([-25., 48., -36., 16., -3.]) / (12 * h)
    return sum(w * function(float(i * h)) for i, w in enumerate(weights))


def forward_curvature(function, h):
    """Third-order one-sided second derivative, independently from solution."""
    weights = np.array([35., -104., 114., -56., 11.]) / (12 * h * h)
    return sum(w * function(float(i * h)) for i, w in enumerate(weights))


def initial_states(operator, H):
    """Same RMS sigma; free initial deltaQ gives sigma_dot=(H+d)*sigma."""
    if abs(operator[0, 1]) < 1e-10:
        raise ValueError("initial-state construction requires nonzero A[0,1]")
    states = []
    for rate in (-1., 0., 1.):
        state = np.zeros(6)
        state[0] = 1.
        state[1] = (H + rate - operator[0, 0]) / operator[0, 1]
        states.append(state)
    return np.array(states)


def integrate_fundamental(bg, k, tend, rtol):
    def rhs(t, flat):
        return (mode_system(bg.at(float(t))[0], k)[0]
                @ flat.reshape(6, 6)).ravel()
    solution = solve_ivp(rhs, [0., tend], np.eye(6).ravel(), method="DOP853",
                         rtol=rtol, atol=rtol * .01, dense_output=True)
    if not solution.success:
        raise RuntimeError(solution.message)
    return solution


def compact_diagnostic(bg, solution, k, tend, step):
    raw = diagnose(bg, solution, k, tend, step)
    return {key: value for key, value in raw.items() if key != "potentials"}


class MixedModeSolution:
    """Adapt original uneliminated-Euler check to the chosen initial modes."""
    def __init__(self, solution, states):
        self.solution = solution
        self.initial = np.zeros((6, 6))
        self.initial[:, :3] = states.T

    def sol(self, t):
        return (self.solution.sol(t).reshape(6, 6) @ self.initial).ravel()


def run(ks=(.3, 3., 30.), tend=.02):
    if not ks or any(not np.isfinite(k) or k <= 0 for k in ks):
        raise ValueError("strictly positive finite k required; k=0 is separate")
    if not 0 < tend <= .02:
        raise ValueError("contract restricts evolution to 0<tend<=0.02")
    source_before = {str(path.relative_to(BASE)): hashlib.sha256(path.read_bytes()).hexdigest()
                     for path in SOURCE_FILES}
    bg = Background(tend)
    v0 = bg.at(0.)[0]
    samples = np.linspace(0., tend, 9)
    background_checks = []
    for t in samples:
        v, matrix, constraint, margin = bg.at(float(t))
        background_checks.append(dict(t=float(t), a=v["a"], H=v["H"],
            Hdot=v["Hd"], clock_rate=v["sbar"],
            constraint_max=float(np.max(np.abs(constraint[:2]))),
            matrix_condition=float(np.linalg.cond(matrix)), domain_margin=margin))
    assert max(row["constraint_max"] for row in background_checks) < 1e-9
    mode_results = []
    for k in ks:
        def op(t):
            return mode_system(bg.at(float(t))[0], k)[0]
        A = op(0.)
        states = initial_states(A, v0["H"])
        cov0 = np.einsum("mi,mj->mij", states, states)
        epsilon = 1e-6 / k
        physical_y0 = epsilon ** 2 * k ** 2
        coarse = integrate_fundamental(bg, k, tend, 2e-10)
        fine = integrate_fundamental(bg, k, tend, 2e-12)

        # This independent solver uses the covariance differential equation,
        # not any propagated fundamental matrix or its internal solver stages.
        def crhs(t, flat):
            return covariance_rhs(op(t), flat.reshape(3, 6, 6)).ravel()
        covariance_solution = solve_ivp(crhs, [0., tend], cov0.ravel(), method="RK45",
            rtol=2e-11, atol=2e-13, dense_output=True)
        if not covariance_solution.success:
            raise RuntimeError(covariance_solution.message)
        diagnostics = [compact_diagnostic(bg, fine, k, tend, tend / divisor)
                       for divisor in (20, 40)]
        mixed_diagnostic = compact_diagnostic(bg, MixedModeSolution(fine, states),
                                              k, tend, tend / 40)
        all_diags = diagnostics + [mixed_diagnostic]
        assert max(d["max_scaled_euler"] for d in all_diags) < 3e-6
        assert max(d["max_scaled_momentum"] for d in all_diags) < 1e-6
        assert max(d["max_scaled_slip"] for d in all_diags) < 1e-6

        max_cov_error = max_transfer_error = max_variance_error = 0.
        min_eigenvalue = symmetry_error = 0.
        evolution = []
        matrix_conditions = []
        lapse_identity_error = 0.
        for t in samples:
            v = bg.at(float(t))[0]
            transfer = fine.sol(t).reshape(6, 6)
            low = coarse.sol(t).reshape(6, 6)
            direct = covariance_solution.sol(t).reshape(3, 6, 6)
            transported = transfer @ cov0 @ transfer.T
            propagated_modes = states @ transfer.T
            rank_one = np.einsum("mi,mj->mij", propagated_modes, propagated_modes)
            assert np.max(np.abs(transported - rank_one)) < 1e-9 * (1 + np.max(np.abs(transported)))
            scale = 1 + np.max(np.abs(transported))
            max_cov_error = max(max_cov_error, float(np.max(np.abs(direct - transported)) / scale))
            max_transfer_error = max(max_transfer_error, float(np.max(np.abs(transfer - low))
                / (1 + np.max(np.abs(transfer)))))
            max_variance_error = max(max_variance_error,
                float(np.max(np.abs(direct[:, 0, 0] - transported[:, 0, 0]))))
            symmetry_error = max(symmetry_error, float(np.max(np.abs(direct - direct.transpose(0, 2, 1)))))
            min_eigenvalue = min(min_eigenvalue, float(np.min(np.linalg.eigvalsh(direct))) / scale)
            p = k ** 2 / v["a"] ** 2
            operator, matrix, lapse, *_ = mode_system(v, k)
            delta = matrix[0, 0] * matrix[3, 3] - matrix[3, 0] * matrix[0, 3]
            predicted = -v["q"] * matrix[0, 0] / (2 * v["M2"] * delta)
            lapse_identity_error = max(lapse_identity_error, abs(operator[0, 5] - predicted))
            matrix_conditions.append(float(np.linalg.cond(matrix)))
            cd = covariance_rhs(operator, direct)
            evolution.append(dict(t=float(t),
                Y_over_initial=(p / k ** 2 * direct[:, 0, 0]).tolist(),
                Ydot_over_initial=(p / k ** 2 * (cd[:, 0, 0] - 2 * v["H"] * direct[:, 0, 0])).tolist()))
        assert max_cov_error < 1e-8
        assert max_transfer_error < 1e-8
        assert max_variance_error < 1e-8
        assert symmetry_error < 1e-10
        assert min_eigenvalue > -1e-8
        assert lapse_identity_error < 1e-10

        rate_steps = [min(1e-4, tend / 100), min(5e-5, tend / 200), min(2.5e-5, tend / 400)]
        curvatures = []
        A_rates = [forward_rate(op, h) for h in rate_steps]
        jets = np.array([variance_jets(k * k, v0["H"], v0["Hd"], A,
                                      A_rates[-1], c) * epsilon ** 2 for c in cov0])
        assert np.max(np.abs(jets[:, 0] / physical_y0 - 1)) < 1e-13
        assert np.max(np.abs(jets[:, 1] / physical_y0 - np.array([-2., 0., 2.]))) < 1e-12
        for h, Ad in zip(rate_steps, A_rates):
            acc = ((Ad + A @ A) @ states[1])[0]
            specialized = 2 * (acc - v0["Hd"] - v0["H"] ** 2)
            general = variance_jets(k * k, v0["H"], v0["Hd"], A, Ad, cov0[1])[2] / (k * k)
            assert abs(specialized - general) < 1e-10 * (1 + abs(general))
            curvatures.append(dict(h=h, Yddot_over_initial=general,
                                   sigma_acceleration_over_sigma=acc))
        rate_refinement = abs(curvatures[-1]["Yddot_over_initial"] - curvatures[-2]["Yddot_over_initial"])
        expected_curvature = curvatures[-1]["Yddot_over_initial"]
        assert rate_refinement < 1e-5 * (1 + abs(expected_curvature))
        assert abs(expected_curvature) > 1e-4

        def normalized_stationary_y(t):
            v = bg.at(t)[0]
            state = fine.sol(t).reshape(6, 6) @ states[1]
            return state[0] ** 2 / v["a"] ** 2
        direct_curvatures = [dict(h=tend / divisor,
            Yddot_over_initial=forward_curvature(normalized_stationary_y, tend / divisor))
            for divisor in (20, 40, 80)]
        curvature_error = abs(direct_curvatures[-1]["Yddot_over_initial"] - expected_curvature)
        assert curvature_error < 2e-3 * (1 + abs(expected_curvature))

        _, _, lapse, zrow, brow, jrow = mode_system(v0, k)
        reconstructed = []
        for label, state, jet in zip(("decreasing", "instantaneously_stationary", "increasing"), states, jets):
            physical_state = epsilon * state
            reconstructed.append(dict(label=label, state_rms=physical_state.tolist(),
                lapse_rms=float(lapse @ physical_state), z_rms=float(zrow @ physical_state),
                shift_rms=float(brow @ physical_state), J_rms=float(jrow @ physical_state),
                Y=float(jet[0]), Ydot=float(jet[1]), Yddot=float(jet[2])))
        # The same sigma and sigma_dot covariance column can hide extra
        # velocity variance. This PSD addition leaves Y,Ydot unchanged.
        enriched = cov0[1].copy()
        enriched[1, 1] += .01
        enriched_jets = variance_jets(k * k, v0["H"], v0["Hd"], A, A_rates[-1], enriched)
        expected_extra_curvature = .02 * A[0, 1] ** 2
        measured_extra_curvature = enriched_jets[2] / (k * k) - expected_curvature
        assert abs(measured_extra_curvature - expected_extra_curvature) < 1e-9
        mode_results.append(dict(k=k, epsilon_rms=epsilon, initial=reconstructed,
            stationary_curvature_from_operator=curvatures,
            stationary_curvature_from_solution=direct_curvatures,
            covariance_hidden_velocity_variance=dict(additional_deltaQ_variance=.01,
                unchanged_Y_over_initial=float(enriched_jets[0] / (k * k)),
                unchanged_Ydot_over_initial=float(enriched_jets[1] / (k * k)),
                extra_Yddot_over_initial=measured_extra_curvature),
            evolution=evolution, checks=dict(max_covariance_transport_error=max_cov_error,
                max_transfer_refinement_error=max_transfer_error,
                max_variance_transport_error=max_variance_error,
                min_scaled_covariance_eigenvalue=min_eigenvalue,
                covariance_symmetry_error=symmetry_error,
                operator_rate_curvature_refinement=rate_refinement,
                direct_solution_curvature_error=curvature_error,
                dust_lapse_minor_identity_error=lapse_identity_error,
                max_reduction_matrix_condition=max(matrix_conditions)),
            original_euler_basis_checks=diagnostics,
            original_euler_selected_ensemble_check=mixed_diagnostic,
            integration_evaluations=dict(fundamental_coarse=coarse.nfev,
                fundamental_fine=fine.nfev, independent_covariance=covariance_solution.nfev)))
        print(json.dumps(dict(k=k, initial_Y=physical_y0,
            Ydot_over_initial=(jets[:, 1] / physical_y0).tolist(),
            stationary_Yddot_over_initial=expected_curvature,
            stationary_Y_end_over_initial=evolution[-1]["Y_over_initial"][1],
            max_covariance_transport_error=max_cov_error,
            max_scaled_original_euler=max(d["max_scaled_euler"] for d in all_diags))), flush=True)
    source_after = {str(path.relative_to(BASE)): hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in SOURCE_FILES}
    assert source_before == source_after, "imported scientific source changed during run"
    return dict(status="bounded_numerical_assertions_passed", full_theory_status="OPEN",
        convention="u is an RMS mode/quadrature state; C=<u u^T>; Y2=(k/a)^2*C00; cosine amplitude instead gives factor 1/2",
        state_order=["sigma", "deltaQ", "radiation_field", "deltaQr", "dust_velocity", "delta_rho_b"],
        formulas=dict(Cdot="A C + C A^T", Y="p C00",
            Ydot="p [(A C+C A^T)00-2H C00]",
            Yddot="p [Cddot00-4H Cdot00+(4H^2-2Hdot) C00]",
            Cddot="Adot C+C Adot^T+A Cdot+Cdot A^T"),
        bounds=dict(k=list(ks), time=[0., tend], background_rtol=2e-12,
            fundamental_rtols=[2e-10, 2e-12], covariance_rtol=2e-11,
            covariance_method="RK45", fundamental_method="DOP853", sample_count=9,
            exact_dynamics="time-dependent constrained six-state linear action; float64 integration"),
        background=background_checks, source_sha256=source_after, modes=mode_results,
        conclusions=["Equal initial gradient variance allows opposite initial time derivatives on this constrained action.",
            "An initial state with Ydot=0 has nonzero action-derived Yddot in every tested mode.",
            "Adding independent deltaQ variance keeps Y and Ydot fixed while changing Yddot.",
            "The covariance law retains inertia, expansion, matter correlations and coefficient rates."],
        non_claims=["No all-k, late-time, nonlinear or global-attractor exclusion.",
            "No supplied primordial spectrum, CMB spectrum or observed cosmological variance.",
            "No claim that an arbitrary prescribed finite nonlinear variance is within the linear regime.",
            "k=0 has identically zero projected gradient and is not evaluated by the singular finite-k reduction.",
            "Numeric refinement and residuals are conditional evidence, not interval-certified error bounds."])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--result-file", type=Path, required=True)
    parser.add_argument("--ks", nargs="+", type=float, default=[.3, 3., 30.])
    parser.add_argument("--tend", type=float, default=.02)
    args = parser.parse_args()
    result = run(tuple(args.ks), args.tend)
    args.result_file.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
