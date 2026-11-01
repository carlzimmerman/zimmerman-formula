"""Independent SciPy BDF continuation of a strictly warm, fixed-law state.

The physical RHS, constitutive parameters, sparse dependency envelope, energies,
entropy and diagnostics come unchanged from the pinned convective/refinement
model. This driver uses scipy.integrate.BDF directly; it does not patch a module
or label a Radau run as BDF. It is restricted to strictly positive initial K and
does not implement the exact cold subspace.

Accepted negative K and invalid shell stages reject/restart from the unchanged
accepted state with a quarter step, under explicit retry and resource bounds.
No accepted state is clipped, projected or seeded. Completion alone certifies
neither settling nor continuum convergence. Energy and entropy errors remain
numerical diagnostics with the continuation's initial state as their reference.
"""

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import time

import numpy as np
from scipy.integrate import BDF

import refinement


def model_from_restart(previous):
    material_params = refinement.convective.baseline.material.MaterialParameters(
        rho_q=1, G=1, a0=np.sqrt(8 * np.pi), tau=0.5)
    transport_params = refinement.convective.ConvectiveParameters()
    if (previous.get("closure") != refinement.convective.CLOSURE
            or previous["material_parameters"] != asdict(material_params)
            or previous["transport_parameters"] != asdict(transport_params)):
        raise ValueError("restart must match the fixed closure and every material/transport parameter")
    return refinement.FloorAuditedCollapse(
        previous["n_shells"], material_params, transport=transport_params,
        initial_density=previous["initial_density"], radius=previous["initial_radius"],
        initial_velocity_gradient=previous["initial_velocity_gradient"],
    )


def simulate(model, *, initial_state, initial_time, t_end=64.0, samples=129,
             rtol=2e-7, atol=1e-9, wall_seconds=45.0, max_rhs_calls=300000,
             max_step=0.05, max_domain_retries=80, minimum_retry_step=1e-12):
    values = [initial_time, t_end, rtol, atol, wall_seconds, max_step, minimum_retry_step]
    if (not np.all(np.isfinite(values)) or initial_time < 0 or t_end <= initial_time
            or samples < 2 or min(rtol, atol, wall_seconds, max_step, minimum_retry_step) <= 0
            or max_rhs_calls < 1 or max_domain_retries < 1):
        raise ValueError("invalid run bounds")
    started = time.monotonic()
    y = np.asarray(initial_state, dtype=float).copy()
    model.fields(y)
    if np.any(y[2 * model.n:] <= 0):
        raise ValueError("BDF warm continuation requires strictly positive initial K")
    current_t = float(initial_time)
    initial = model.diagnostics(current_t, y)
    scale = max(abs(initial["total"]), np.finfo(float).tiny)
    history = [initial]
    targets = np.linspace(initial_time, t_end, samples)[1:]
    next_target, calls, accepted_steps = 0, 0, 0
    max_energy_error = 0.0
    minimum_accepted_K = float(y[2 * model.n:].min())
    minimum_entropy = initial["total_entropy"]
    last_entropy = initial["total_entropy"]
    max_entropy_decrease = 0.0
    status, message = "completed", "reached declared finite end time with SciPy BDF"
    solver, failed_trial = None, None
    rejections, step_sizes, order_counts = [], [], {}
    prior_njev, prior_nlu = 0, 0
    stage_count_before = model.stage_memory_floor_count
    minimum_stage_before = model.minimum_stage_memory

    class RunLimit(RuntimeError):
        pass

    def rhs(t, state):
        nonlocal calls
        calls += 1
        if calls > max_rhs_calls:
            raise RunLimit("rhs_limit")
        if time.monotonic() - started > wall_seconds:
            raise RunLimit("wall_limit")
        try:
            return model.rhs(t, state)
        except refinement.convective.baseline.collapse.ShellOrderingError as exc:
            exc.trial_time = float(t)
            raise

    def make_solver(first_step=None):
        nonlocal prior_njev, prior_nlu
        new = BDF(rhs, current_t, y.copy(), t_end, rtol=rtol, atol=atol,
                  max_step=max_step, first_step=first_step, jac_sparsity=model.jacobian_sparsity())
        if solver is not None:
            prior_njev += solver.njev
            prior_nlu += solver.nlu
        return new

    def reject(reason, state, trial_time, attempted_step):
        nonlocal failed_trial
        record = dict(reason=reason, t=trial_time, attempted_step=attempted_step,
                      last_accepted_time=current_t,
                      min_trial_gap=float(np.diff(np.r_[0.0, state[:model.n]]).min()),
                      min_trial_K=float(state[2 * model.n:].min()))
        rejections.append(record)
        if failed_trial is None:
            failed_trial = dict(**record, state=state.tolist(), last_accepted_state=y.tolist())
        return attempted_step / 4

    try:
        solver = make_solver()
        while solver.status == "running":
            attempted_step = min(float(solver.h_abs), max_step, t_end - current_t)
            try:
                solver.step()
            except refinement.convective.baseline.collapse.ShellOrderingError as exc:
                retry = reject("shell_ordering_stage", exc.state, exc.trial_time, attempted_step)
                if len(rejections) >= max_domain_retries or retry < minimum_retry_step:
                    status, message = "domain_retry_limit", "invalid BDF stage persisted at the declared retry bound"
                    break
                solver = make_solver(retry)
                continue
            if solver.status == "failed":
                status, message = "integrator_failed", "BDF could not take a step"
                break
            trial = solver.y.copy()
            if np.any(trial[2 * model.n:] < 0):
                retry = reject("negative_accepted_memory", trial, float(solver.t), float(solver.t - current_t))
                if len(rejections) >= max_domain_retries or retry < minimum_retry_step:
                    status, message = "domain_retry_limit", "negative BDF memory persisted at the declared retry bound"
                    break
                solver = make_solver(retry)
                continue
            fields = model.fields(trial)
            if np.diff(np.r_[0.0, fields["r"]]).min() < 1e-9 * model.radius / model.n:
                status, message = "minimum_gap", "stopped before the declared shell-gap floor"
                break
            step_sizes.append(float(solver.t - current_t))
            order = str(int(solver.order))
            order_counts[order] = order_counts.get(order, 0) + 1
            y, current_t = trial, float(solver.t)
            accepted_steps += 1
            minimum_accepted_K = min(minimum_accepted_K, float(fields["K"].min()))
            max_energy_error = max(max_energy_error, abs(model.energy(y)["total"] - initial["total"]) / scale)
            entropy = float(model.dm * np.sum(fields["sigma"]))
            minimum_entropy = min(minimum_entropy, entropy)
            max_entropy_decrease = max(max_entropy_decrease, last_entropy - entropy)
            last_entropy = entropy
            interpolate = solver.dense_output()
            while next_target < len(targets) and targets[next_target] <= current_t:
                target = float(targets[next_target])
                try:
                    history.append(model.diagnostics(target, interpolate(target)))
                except ValueError:
                    history.append(dict(t=target, sample_status="invalid_dense_interpolation"))
                next_target += 1
    except RunLimit as exc:
        status, message = str(exc), "resource bound reached; requested BDF continuation is inconclusive"
    except (ValueError, FloatingPointError) as exc:
        status, message = "invalid_state", str(exc)
    final = model.diagnostics(current_t, y)
    if history[-1].get("t") != current_t:
        history.append(final)
    good = [row for row in history if "enclosed_5pct_mean_density" in row]
    return dict(
        schema_version=1, status=status, message=message, method="BDF",
        closure=refinement.convective.CLOSURE, integrator_variant="independent_warm_BDF_continuation",
        n_shells=model.n, t_initial=initial_time, t_requested=t_end, t_reached=current_t,
        initial_density=model.initial_density, initial_radius=model.radius,
        initial_velocity_gradient=model.velocity_gradient, total_mass=model.total_mass,
        material_parameters=asdict(model.params), transport_parameters=asdict(model.transport),
        transport_units=dict(diffusivity="physical length^2/time", damping_strength="dimensionless",
                             memory_activation="K/Kstar", temperature_bar="T/(3*Kstar*rho_q)",
                             stratification_length="fixed physical length", stratification_scale="K/Kstar"),
        rtol=rtol, atol=atol, max_step=max_step, wall_cap_seconds=wall_seconds, rhs_cap=max_rhs_calls,
        max_domain_retries=max_domain_retries, minimum_retry_step=minimum_retry_step,
        minimum_shell_gap=1e-9 * model.radius / model.n,
        elapsed_seconds=time.monotonic() - started, rhs_calls=calls, accepted_steps=accepted_steps,
        max_relative_energy_error=float(max_energy_error), minimum_accepted_K=minimum_accepted_K,
        minimum_accepted_total_entropy=minimum_entropy, max_single_step_entropy_decrease=max_entropy_decrease,
        stage_memory_floor_count=model.stage_memory_floor_count - stage_count_before,
        minimum_stage_memory=model.minimum_stage_memory, minimum_stage_memory_before_run=minimum_stage_before,
        domain_rejections=rejections, failed_trial=failed_trial,
        accepted_negative_memory_rejections=sum(row["reason"] == "negative_accepted_memory" for row in rejections),
        invalid_dense_sample_count=sum("sample_status" in row for row in history),
        peak_sampled_5pct_density=max(row["enclosed_5pct_mean_density"] for row in good),
        accepted_step_statistics=dict(minimum=min(step_sizes) if step_sizes else None,
                                      maximum=max(step_sizes) if step_sizes else None,
                                      mean=float(np.mean(step_sizes)) if step_sizes else None,
                                      last=step_sizes[-1] if step_sizes else None,
                                      order_counts=order_counts,
                                      maximum_order=max(map(int, order_counts)) if order_counts else None),
        jacobian_evaluations=prior_njev + (solver.njev if solver is not None else 0),
        lu_factorizations=prior_nlu + (solver.nlu if solver is not None else 0),
        initial=initial, final=final, time_history=history,
        settling=refinement.convective.baseline.settling_metrics(history),
        final_profile=model.profile(y), final_state=y.tolist(),
        observer=dict(name="fixed_mass_prefix_floor", sample_origin="BDF dense-output samples and final accepted state"),
        cold_phase=dict(status="not_applicable_warm_continuation", K_coordinate_integrated=True),
        energy_error_reference="Continuation initial total energy",
        non_claims=["No 3D, convective or nonradial stability test", "No cosmological forest realization",
                    "No baryons", "No certified continuum formation or settling result",
                    "Instability-gated heat transport is not resolved material convection"],
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--restart", type=Path, required=True)
    parser.add_argument("--t-end", type=float, default=64.0)
    parser.add_argument("--samples", type=int, default=129)
    parser.add_argument("--wall-seconds", type=float, default=45.0)
    parser.add_argument("--max-rhs-calls", type=int, default=300000)
    parser.add_argument("--rtol", type=float, default=2e-7)
    parser.add_argument("--atol", type=float, default=1e-9)
    parser.add_argument("--max-step", type=float, default=0.05)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    restart_bytes = args.restart.read_bytes()
    previous = json.loads(restart_bytes)
    try:
        model = model_from_restart(previous)
        result = simulate(model, initial_state=previous["final_state"], initial_time=previous["t_reached"],
                          t_end=args.t_end, samples=args.samples, rtol=args.rtol, atol=args.atol,
                          wall_seconds=args.wall_seconds, max_rhs_calls=args.max_rhs_calls,
                          max_step=args.max_step)
    except ValueError as exc:
        parser.error(str(exc))
    result["continuation"] = dict(restart_source=str(args.restart.resolve()),
                                  restart_sha256=hashlib.sha256(restart_bytes).hexdigest(),
                                  restart_time=previous["t_reached"], previous_status=previous["status"])
    refinement.convective.baseline.atomic_json(args.output, result)
    print(json.dumps({key: result[key] for key in ("method", "status", "n_shells", "t_reached",
                                                  "elapsed_seconds", "rhs_calls", "max_relative_energy_error")},
                     sort_keys=True))
    return 0 if result["status"] == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
