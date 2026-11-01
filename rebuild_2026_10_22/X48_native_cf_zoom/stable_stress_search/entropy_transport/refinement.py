"""Observation-only fixed-mass floor sampling for the pinned convective law.

The observer changes no fields, forces, heating, transport or physical parameters.
For exactly cold initial states before shock activation, it integrates the exact
2N-dimensional (r,u) invariant subspace with K identically zero, then hands off
to the pinned full Radau algorithm at the physical activation event. This avoids
floating leakage into zero K in the coupled sparse LU solve, without a K seed,
floor or accepted-state projection. Wall/RHS caps cover both phases together.
It records every cell's K, density and outer radius at diagnostic sample times.
A prefix ending inside a constant-K cell includes that cell's K;
its outside guard is the NEXT cell, index ceil(f*N), in zero-based indexing.
Exact decimal mass fractions determine this mapping without a floating ceil.

Optional restart preparation is performed once before integration:
    r_prepared = radius_factor * r_restart,
    u_prepared = u_restart + velocity_gradient * r_prepared,
    K_prepared = K_restart.
The original cell/node masses remain fixed. The full internal, kinetic and
gravitational energy change is reported as preparation work. No state changes
are applied during the run. Sampled floor inequalities remain finite numerical
observations, not a continuous-time barrier certificate.
"""

import argparse
from dataclasses import asdict
from fractions import Fraction
import json
from pathlib import Path
import time

import numpy as np
from scipy.integrate import Radau
from scipy.optimize import brentq
from scipy.sparse import bmat, diags

import convective_transport as convective


PREFIXES = ((0.01, "1pct"), (0.05, "5pct"), (0.10, "10pct"), (0.25, "25pct"))


def prefix_mapping(n_shells, fraction):
    """Cell/guard convention for the requested exact decimal mass fraction."""
    if not isinstance(n_shells, int) or n_shells < 2:
        raise ValueError("n_shells must be an integer >=2")
    fraction = float(fraction)
    if not np.isfinite(fraction) or not 0 < fraction < 1:
        raise ValueError("fraction must lie strictly between zero and one")
    exact = Fraction(str(fraction))
    coordinate = exact * n_shells
    quotient, remainder = divmod(coordinate.numerator, coordinate.denominator)
    count = quotient + (remainder != 0)
    guard = count if count < n_shells else None
    return dict(
        requested_mass_fraction=fraction,
        mass_fraction_numerator=exact.numerator, mass_fraction_denominator=exact.denominator,
        boundary_cell_coordinate=float(coordinate), exact_cell_boundary=remainder == 0,
        included_cell_count=count, last_included_cell_index=count - 1,
        last_included_cell_fraction=float(Fraction(remainder, coordinate.denominator)) if remainder else 1.0,
        boundary_inside_cell_index=count - 1 if remainder else None,
        guard_cell_index=guard,
        guard_inner_mass_fraction=guard / n_shells if guard is not None else None,
        guard_outer_mass_fraction=(guard + 1) / n_shells if guard is not None else None,
        convention="Guard is after every cell intersecting the prefix, including a partial last cell",
    )


class FloorAuditedCollapse(convective.ConvectiveCollapse):
    def diagnostics(self, t, y):
        result = super().diagnostics(t, y)
        r, _, K, _, rho, _ = self.geometry(y)
        result.update(K_by_cell=K.tolist(), rho_by_cell=rho.tolist(), r_by_cell=r.tolist(),
                      min_all_K=float(K.min()), floor_prefixes={})
        for fraction, label in PREFIXES:
            mapping = prefix_mapping(self.n, fraction)
            minimum = float(K[:mapping["included_cell_count"]].min())
            index = mapping["guard_cell_index"]
            guard = float(K[index]) if index is not None else None
            result[f"prefix_{label}_min_K"] = minimum
            result[f"K_guard_{label}"] = guard
            result["floor_prefixes"][label] = dict(mapping, prefix_min_K=minimum, K_guard=guard)
        return result


def prepare_restart_state(model, state, *, radius_factor=1.0, velocity_gradient=0.0):
    """Return a new prepared state and the complete mechanical/thermal work audit."""
    if not np.all(np.isfinite([radius_factor, velocity_gradient])) or radius_factor <= 0:
        raise ValueError("radius_factor must be positive and the added velocity gradient finite")
    original = np.asarray(state, dtype=float)
    model.fields(original)
    before = model.energy(original)
    prepared = original.copy()
    prepared[:model.n] *= radius_factor
    prepared[model.n:2 * model.n] += velocity_gradient * prepared[:model.n]
    model.fields(prepared)
    after = model.energy(prepared)
    changes = {key: after[key] - before[key] for key in before}
    audit = dict(
        radius_factor=float(radius_factor), velocity_gradient_added=float(velocity_gradient),
        velocity_kick_radius="prepared radius", before_energy=before, prepared_energy=after,
        delta_energy=changes, delta_total_energy=changes["total"],
        K_preserved_exactly=bool(np.array_equal(original[2 * model.n:], prepared[2 * model.n:])),
        conserved_cell_mass=float(model.dm), conserved_total_mass=float(model.total_mass),
        applied_once_before_integration=True,
    )
    return prepared, audit


def _activation_indicator(model, state):
    _, _, _, _, rho, theta = model.geometry(state)
    return float(np.max(np.minimum(rho / model.params.rho_q - 1,
                                    model.params.tau * np.maximum(-theta, 0) - 1)))


def _cold_phase(model, initial_state, *, t_end, samples, rtol, atol, wall_seconds,
                max_rhs_calls, max_step, initial_time, max_domain_retries,
                minimum_retry_step, started):
    """Integrate the exact dust subspace until the upward shock-activation event."""
    n = model.n
    y = initial_state.copy()
    current_t = float(initial_time)
    initial = model.diagnostics(current_t, y)
    initial_energy = model.energy(y)
    energy_scale = max(abs(initial_energy["total"]), np.finfo(float).tiny)
    history = [initial]
    targets = np.linspace(initial_time, t_end, samples)[1:]
    next_target, calls, accepted_steps, max_energy_error = 0, 0, 0, 0.0
    rejections = []
    failed_trial = None
    solver = None
    status, message = "completed", "reached declared finite end time in the exact cold subspace"
    triggered = False
    root_xtol = 1e-13

    class RunLimit(RuntimeError):
        pass

    def expand(reduced):
        return np.r_[reduced, np.zeros(n)]

    def rhs(t, reduced):
        nonlocal calls
        calls += 1
        if calls > max_rhs_calls:
            raise RunLimit("rhs_limit")
        if time.monotonic() - started > wall_seconds:
            raise RunLimit("wall_limit")
        state = expand(reduced)
        try:
            r, u, _, _, _, _ = model.geometry(state)
        except convective.baseline.collapse.ShellOrderingError as exc:
            exc.trial_time = float(t)
            raise
        # This smooth dust extension is used only to locate the first activation.
        # Before the terminal event it is exactly the full constitutive law.
        return np.r_[u, -model.params.G * model.node_mass / r**2]

    def jacobian(t, reduced):
        return bmat([[None, diags(np.ones(n))],
                     [diags(2 * model.params.G * model.node_mass / reduced[:n]**3), None]],
                    format="csc")

    def make_solver(first_step=None):
        return Radau(rhs, current_t, y[:2 * n].copy(), t_end, rtol=rtol, atol=atol,
                     max_step=max_step, first_step=first_step, jac=jacobian)

    try:
        solver = make_solver()
        while solver.status == "running":
            attempted_step = min(float(solver.h_abs), max_step, t_end - current_t)
            try:
                solver.step()
            except convective.baseline.collapse.ShellOrderingError as exc:
                record = dict(reason="cold_shell_ordering_stage", t=exc.trial_time,
                              attempted_step=attempted_step, last_accepted_time=current_t,
                              min_trial_gap=float(np.diff(np.r_[0.0, exc.state[:n]]).min()),
                              min_trial_K=0.0)
                rejections.append(record)
                if failed_trial is None:
                    failed_trial = dict(**record, state=exc.state.tolist(), last_accepted_state=y.tolist())
                retry = attempted_step / 4
                if len(rejections) >= max_domain_retries or retry < minimum_retry_step:
                    status, message = "domain_retry_limit", "cold shell stage persisted at the declared retry bound"
                    break
                solver = make_solver(retry)
                continue
            if solver.status == "failed":
                status, message = "integrator_failed", "cold-subspace Radau could not take a step"
                break
            trial = expand(solver.y)
            trial_time = float(solver.t)
            interpolate = solver.dense_output()
            if _activation_indicator(model, trial) >= 0:
                trial_time = brentq(lambda t: _activation_indicator(model, expand(interpolate(t))),
                                    current_t, trial_time, xtol=root_xtol, rtol=4 * np.finfo(float).eps)
                trial = expand(interpolate(trial_time))
                triggered = True
            gap = float(np.diff(np.r_[0.0, trial[:n]]).min())
            if gap < 1e-9 * model.radius / n:
                status, message = "minimum_gap", "cold subspace stopped before the declared shell-gap floor"
                triggered = False
                break
            y, current_t = trial, trial_time
            accepted_steps += 1
            max_energy_error = max(max_energy_error,
                                   abs(model.energy(y)["total"] - initial_energy["total"]) / energy_scale)
            while next_target < len(targets) and targets[next_target] <= current_t:
                target = float(targets[next_target])
                try:
                    history.append(model.diagnostics(target, expand(interpolate(target))))
                except ValueError:
                    history.append(dict(t=target, sample_status="invalid_dense_interpolation"))
                next_target += 1
            if triggered:
                break
    except RunLimit as exc:
        status, message = str(exc), "shared resource bound reached during exact cold-subspace integration"
    except (ValueError, FloatingPointError) as exc:
        status, message = "invalid_state", str(exc)
    final = model.diagnostics(current_t, y)
    if history[-1].get("t") != current_t:
        history.append(final)
    phase_status = ("activation_handoff" if triggered else "completed_without_activation") if status == "completed" else status
    good = [row for row in history if "enclosed_5pct_mean_density" in row]
    result = dict(
        schema_version=1, status=status, message=message, method="Radau", closure=convective.CLOSURE,
        n_shells=n, t_initial=initial_time, t_requested=t_end, t_reached=current_t,
        initial_density=model.initial_density, initial_radius=model.radius,
        initial_velocity_gradient=model.velocity_gradient, total_mass=model.total_mass,
        material_parameters=asdict(model.params), transport_parameters=asdict(model.transport),
        transport_units=dict(diffusivity="physical length^2/time", damping_strength="dimensionless",
                             memory_activation="K/Kstar", temperature_bar="T/(3*Kstar*rho_q)",
                             stratification_length="fixed physical length", stratification_scale="K/Kstar"),
        rtol=rtol, atol=atol, max_step=max_step, wall_cap_seconds=wall_seconds, rhs_cap=max_rhs_calls,
        max_domain_retries=max_domain_retries, minimum_retry_step=minimum_retry_step,
        minimum_shell_gap=1e-9 * model.radius / n, elapsed_seconds=time.monotonic() - started,
        rhs_calls=calls, accepted_steps=accepted_steps, max_relative_energy_error=float(max_energy_error),
        minimum_accepted_K=0.0, minimum_accepted_total_entropy=0.0, max_single_step_entropy_decrease=0.0,
        stage_memory_floor_count=0, minimum_stage_memory=0.0, minimum_stage_memory_before_run=model.minimum_stage_memory,
        domain_rejections=rejections, accepted_negative_memory_rejections=0, failed_trial=failed_trial,
        invalid_dense_sample_count=sum("sample_status" in row for row in history),
        peak_sampled_5pct_density=max(row["enclosed_5pct_mean_density"] for row in good),
        initial=initial, final=final, time_history=history,
        settling=convective.baseline.settling_metrics(history), final_profile=model.profile(y), final_state=y.tolist(),
        non_claims=["No 3D, convective or nonradial stability test", "No cosmological forest realization",
                    "No baryons", "No fitted halo envelope", "No certified continuum formation or settling result",
                    "Instability-gated heat transport is not resolved material convection"],
        cold_phase=dict(status=phase_status, initial_time=initial_time, final_time=current_t,
                        rhs_calls=calls, accepted_steps=accepted_steps,
                        activation_indicator="max_i min(rho_i/rho_q-1, tau*max(-theta_i,0)-1), upward crossing",
                        activation_indicator_at_handoff=_activation_indicator(model, y) if triggered else None,
                        activation_root_xtol=root_xtol,
                        handoff_K_exactly_zero=bool(np.all(y[2 * n:] == 0)) if triggered else None,
                        dimension=2 * n, K_coordinate_integrated=False),
    )
    return result, triggered


def simulate(model, *, t_end=4.0, samples=161, rtol=2e-7, atol=1e-9,
             wall_seconds=45.0, max_rhs_calls=300000, max_step=0.05,
             initial_state=None, initial_time=0.0, max_domain_retries=80,
             minimum_retry_step=1e-12):
    numbers = [t_end, initial_time, rtol, atol, wall_seconds, max_step, minimum_retry_step]
    if (not np.all(np.isfinite(numbers)) or t_end <= initial_time or initial_time < 0
            or samples < 2 or min(rtol, atol, wall_seconds, max_step, minimum_retry_step) <= 0
            or max_rhs_calls < 1 or max_domain_retries < 1):
        raise ValueError("invalid run bounds")
    started = time.monotonic()
    state = model.initial_state() if initial_state is None else np.asarray(initial_state, dtype=float).copy()
    model.fields(state)
    kwargs = dict(t_end=t_end, samples=samples, rtol=rtol, atol=atol, wall_seconds=wall_seconds,
                  max_rhs_calls=max_rhs_calls, max_step=max_step, initial_state=state,
                  initial_time=initial_time, max_domain_retries=max_domain_retries,
                  minimum_retry_step=minimum_retry_step)
    if np.all(state[2 * model.n:] == 0) and _activation_indicator(model, state) < 0:
        result, triggered = _cold_phase(model, started=started, **kwargs)
        if triggered and result["t_reached"] < t_end:
            remaining_wall = wall_seconds - (time.monotonic() - started)
            remaining_calls = max_rhs_calls - result["rhs_calls"]
            if remaining_wall <= 0 or remaining_calls < 1:
                result["status"] = "wall_limit" if remaining_wall <= 0 else "rhs_limit"
                result["message"] = "shared resource bound reached at cold-to-warm handoff"
            else:
                warm = convective.simulate(
                    model, **dict(kwargs, initial_state=result["final_state"], initial_time=result["t_reached"],
                                  samples=max(2, int(np.ceil((samples - 1) * (t_end - result["t_reached"])
                                                             / (t_end - initial_time))) + 1),
                                  wall_seconds=remaining_wall, max_rhs_calls=remaining_calls,
                                  max_domain_retries=max_domain_retries - len(result["domain_rejections"])))
                history = result["time_history"] + warm["time_history"][1:]
                # The warm solver references handoff energy. This triangle bound
                # references the ORIGINAL initial energy and covers every accepted
                # state in both phases, rather than resetting the energy audit.
                energy_scale = max(abs(result["initial"]["total"]), np.finfo(float).tiny)
                bound = (result["max_relative_energy_error"] + warm["max_relative_energy_error"]
                         * abs(result["final"]["total"]) / energy_scale)
                warm.update(t_initial=initial_time, initial=result["initial"], time_history=history,
                            rhs_calls=result["rhs_calls"] + warm["rhs_calls"],
                            accepted_steps=result["accepted_steps"] + warm["accepted_steps"],
                            wall_cap_seconds=wall_seconds, rhs_cap=max_rhs_calls,
                            max_domain_retries=max_domain_retries,
                            max_relative_energy_error=float(bound),
                            max_relative_energy_error_is_upper_bound=True,
                            energy_error_reference="Original initial total energy; triangle bound over cold and warm phases",
                            domain_rejections=result["domain_rejections"] + warm["domain_rejections"],
                            failed_trial=result["failed_trial"] or warm["failed_trial"],
                            invalid_dense_sample_count=result["invalid_dense_sample_count"] + warm["invalid_dense_sample_count"],
                            peak_sampled_5pct_density=max(row["enclosed_5pct_mean_density"] for row in history
                                                         if "enclosed_5pct_mean_density" in row),
                            settling=convective.baseline.settling_metrics(history), cold_phase=result["cold_phase"])
                result = warm
    else:
        result = convective.simulate(model, **kwargs)
        result["cold_phase"] = dict(status="not_applicable", K_coordinate_integrated=True)
    result["elapsed_seconds"] = time.monotonic() - started
    result["observer"] = dict(
        name="fixed_mass_prefix_floor", prefix_fractions=[fraction for fraction, _ in PREFIXES],
        guard_rule="zero-based cell index ceil(f*N), after the whole last included cell",
        sample_origin="Radau dense-output samples; after cold activation the remaining sample grid is uniform from handoff",
        non_claim="Finite sampled floor observations do not certify a continuous-time barrier",
    )
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shells", type=int, default=32)
    parser.add_argument("--t-end", type=float, default=32.0)
    parser.add_argument("--restart", type=Path)
    parser.add_argument("--samples", type=int, default=321)
    parser.add_argument("--wall-seconds", type=float, default=45.0)
    parser.add_argument("--rtol", type=float, default=2e-7)
    parser.add_argument("--atol", type=float, default=1e-9)
    parser.add_argument("--perturb-radius-factor", type=float, default=1.0)
    parser.add_argument("--perturb-velocity-gradient", type=float, default=0.0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.restart is None and (args.perturb_radius_factor != 1 or args.perturb_velocity_gradient != 0):
        parser.error("state perturbations require --restart and are applied only before integration")
    material_params = convective.baseline.material.MaterialParameters(
        rho_q=1, G=1, a0=np.sqrt(8 * np.pi), tau=0.5)
    transport_params = convective.ConvectiveParameters()
    sphere_parameters = {}
    previous = None
    if args.restart is not None:
        previous = json.loads(args.restart.read_text())
        if (previous.get("closure") != convective.CLOSURE or previous["n_shells"] != args.shells
                or previous["material_parameters"] != asdict(material_params)
                or previous["transport_parameters"] != asdict(transport_params)):
            parser.error("restart must match the fixed closure, shell count and every material/transport parameter")
        sphere_parameters = dict(initial_density=previous["initial_density"],
                                 radius=previous["initial_radius"],
                                 initial_velocity_gradient=previous["initial_velocity_gradient"])
    model = FloorAuditedCollapse(args.shells, material_params, transport=transport_params,
                                 **sphere_parameters)
    initial_state, initial_time, preparation = None, 0.0, None
    if previous is not None:
        try:
            initial_state, preparation = prepare_restart_state(
                model, previous["final_state"], radius_factor=args.perturb_radius_factor,
                velocity_gradient=args.perturb_velocity_gradient)
        except ValueError as exc:
            parser.error(str(exc))
        initial_time = previous["t_reached"]
        preparation["restart_source"] = str(args.restart.resolve())
        preparation["restart_time"] = initial_time
    result = simulate(model, t_end=args.t_end, samples=args.samples, rtol=args.rtol, atol=args.atol,
                      wall_seconds=args.wall_seconds, max_rhs_calls=300000, max_step=0.05,
                      initial_state=initial_state, initial_time=initial_time)
    result["preparation"] = preparation
    convective.baseline.atomic_json(args.output, result)
    print(json.dumps({key: result[key] for key in ("closure", "status", "n_shells", "t_reached",
                                                  "elapsed_seconds", "rhs_calls", "max_relative_energy_error")},
                     sort_keys=True))
    return 0 if result["status"] == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
