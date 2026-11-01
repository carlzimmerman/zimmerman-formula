"""Bounded, conservative spherical entropy transport experiment.

This extends the archived shell operator without modifying it. K remains the
energy coordinate. With W=W(rho), Tbar=(K/Kstar)^(2/3) W/rho_q and the Kirchhoff
potential psi=Tbar^(3/2), each face carries

    L = P0 D (4 pi r_face^2 / delta_r_centroid) h_left h_right (psi_left-psi_right).

D has fixed physical dimensions length^2/time, independent of shell count.
This is Fourier conduction with conductivity proportional to sqrt(T), rather
than diffusion of K or entropy. Closed boundaries and shared face luminosities
give exact semidiscrete energy exchange. Memory bulk pressure is -zeta*theta;
the identical pressure supplies positive heat zeta*theta^2/(rho*W).

At negative intermediate solver K, pressure, temperature and memory activation
use max(K,0), matching the original stage extension. The Kirchhoff potential
uses its smooth linear continuation in K; this keeps a finite, differentiable
transport operator through first warming. Such stages are counted. No accepted
state is projected: a negative accepted K or invalid shell stage rejects the
whole step and restarts from the unchanged accepted state with a quarter step.
Retry/resource caps are inconclusive outcomes. Time conservation, positivity
and settling are measured, not asserted by a completed integrator status.
"""

import argparse
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import sys
import tempfile
import time

import numpy as np
from scipy.integrate import Radau
from scipy.sparse import lil_matrix

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import collapse
import material


@dataclass(frozen=True)
class TransportParameters:
    diffusivity: float = 0.1
    damping_strength: float = 1.0
    memory_activation: float = 0.01

    def __post_init__(self):
        for name in ("diffusivity", "damping_strength", "memory_activation"):
            value = np.asarray(getattr(self, name), dtype=float)
            if value.ndim != 0 or not np.isfinite(value) or value < 0:
                raise ValueError(f"{name} must be a finite nonnegative scalar")
            if name == "memory_activation" and value == 0:
                raise ValueError("memory_activation must be positive")
            object.__setattr__(self, name, float(value))


class TransportCollapse(collapse.SphericalCollapse):
    def __init__(self, n_shells, params, transport=None, **sphere_parameters):
        super().__init__(n_shells, params, **sphere_parameters)
        self.transport = TransportParameters() if transport is None else transport
        if not isinstance(self.transport, TransportParameters):
            raise ValueError("transport must be TransportParameters")

    def fields(self, y, *, stage_extension=False):
        f = super().fields(y, stage_extension=stage_extension)
        rho, theta, K, r = (f[key] for key in ("rho", "theta", "K", "r"))
        W = material.density_weight(rho, self.params)
        h = material.activation(rho / self.params.rho_q)
        chi = np.maximum(K, 0) / self.params.k_star
        memory_gate = chi / (chi + self.transport.memory_activation)
        zeta = (self.transport.damping_strength * self.params.tau * self.params.p0
                * (rho / self.params.rho_q) * (W / self.params.rho_q) * h * memory_gate)
        q_damping = -zeta * theta
        dk_damping = zeta * theta**2 / (rho * W)
        inner = np.r_[0.0, r[:-1]]
        # Volume centroids: mean radial position with spherical volume weight.
        centers = (0.75 * (r + inner) * (r**2 + inner**2)
                   / (r**2 + r * inner + inner**2))
        psi = (K / self.params.k_star) * (W / self.params.rho_q)**1.5
        luminosity = np.zeros(self.n + 1)
        luminosity[1:-1] = (self.params.p0 * self.transport.diffusivity
                            * (4 * np.pi * r[:-1]**2 / np.diff(centers))
                            * h[:-1] * h[1:] * (psi[:-1] - psi[1:]))
        dk_conduction = -np.diff(luminosity) / (self.dm * W)
        f.update(W=W, activation=h, center_radius=centers,
                 temperature_bar=chi**(2 / 3) * W / self.params.rho_q,
                 sigma=np.cbrt(chi), psi=psi, luminosity=luminosity,
                 q_original=f["q"], q_damping=q_damping,
                 dk_original=f["dk"], dk_damping=dk_damping,
                 dk_conduction=dk_conduction,
                 q=f["q"] + q_damping,
                 dk=f["dk"] + dk_damping + dk_conduction)
        return f

    def jacobian_sparsity(self):
        """Conservative envelope including neighbor geometry in face exchange."""
        n = self.n
        pattern = lil_matrix((3 * n, 3 * n), dtype=int)
        for i in range(n):
            pattern[i, n + i] = 1
            for block in (1, 2):
                row = block * n + i
                for source_block in (0, 1, 2):
                    indices = [source_block * n + j
                               for j in range(max(0, i - 2), min(n, i + 3))]
                    pattern[row, indices] = 1
        return pattern.tocsc()

    def _inner_weights(self, fraction):
        return np.clip(fraction * self.n - np.arange(self.n), 0, 1)

    def diagnostics(self, t, y):
        result = super().diagnostics(t, y)
        f = self.fields(y)
        energy = self.energy(y)
        gravity = self.params.G * self.node_mass / f["r"]**2
        area = 4 * np.pi * f["r"]**2
        acceleration = area * np.diff(np.r_[-f["pressure"] - f["q"], 0]) / self.mu - gravity
        hydrostatic = area * np.diff(np.r_[-f["pressure"], 0]) / self.mu - gravity
        gravity_norm = float(np.sum(self.mu * gravity**2))
        result.update(
            kinetic_over_abs_gravitational=energy["kinetic"] / abs(energy["gravitational"]),
            force_residual_rms_over_gravity=float(np.sqrt(np.sum(self.mu * acceleration**2) / gravity_norm)),
            hydrostatic_residual_rms_over_gravity=float(np.sqrt(np.sum(self.mu * hydrostatic**2) / gravity_norm)),
            total_entropy=float(self.dm * np.sum(f["sigma"])),
            min_positive_K=float(f["K"][f["K"] > 0].min()) if np.any(f["K"] > 0) else None,
            max_abs_luminosity=float(np.max(np.abs(f["luminosity"]))),
            total_damping_heating_power=float(np.sum(f["volume"] * (-f["q_damping"] * f["theta"]))),
            total_original_heating_power=float(np.sum(f["volume"] * (-f["q_original"] * f["theta"]))),
            net_conduction_heating_power=float(np.sum(self.dm * f["W"] * f["dk_conduction"])),
        )
        for fraction, label in ((0.01, "1pct"), (0.05, "5pct"), (0.10, "10pct")):
            weights = self._inner_weights(fraction)
            included = weights > 0
            result[f"inner_{label}_min_K"] = float(f["K"][included].min())
            result[f"inner_{label}_mean_K"] = float(np.dot(weights, f["K"]) / weights.sum())
            result[f"inner_{label}_mean_sigma"] = float(np.dot(weights, f["sigma"]) / weights.sum())
        core_weights = self._inner_weights(0.1)
        core = core_weights > 0
        core_temperature = float(np.dot(core_weights, f["temperature_bar"]) / core_weights.sum())
        variance = float(np.dot(core_weights, (f["temperature_bar"] - core_temperature)**2) / core_weights.sum())
        result["inner_10pct_temperature_bar_mean"] = core_temperature
        result["inner_10pct_temperature_relative_std"] = float(np.sqrt(variance) / core_temperature) if core_temperature > 0 else 0.0
        entropy_gradient = np.diff(f["sigma"][core]) / np.diff(f["center_radius"][core])
        result["inner_10pct_min_entropy_gradient"] = float(entropy_gradient.min()) if len(entropy_gradient) else None
        result["inner_10pct_max_entropy_gradient"] = float(entropy_gradient.max()) if len(entropy_gradient) else None
        return result

    def profile(self, y):
        f = self.fields(y)
        keys = ("r", "u", "K", "rho", "theta", "pressure", "q", "q_original",
                "q_damping", "dk_original", "dk_damping", "dk_conduction", "W",
                "center_radius", "temperature_bar", "sigma", "psi", "luminosity")
        return {key: f[key].tolist() for key in keys}


def settling_metrics(history, window_fraction=0.25):
    """Descriptive late-window quantities; no equilibrium pass is inferred."""
    good = [row for row in history if "enclosed_5pct_mean_density" in row]
    start, finish = good[0]["t"], good[-1]["t"]
    cutoff = finish - window_fraction * (finish - start)
    window = [row for row in good if row["t"] >= cutoff]
    output = dict(window_fraction=window_fraction, window_start=cutoff,
                  window_end=finish, sample_count=len(window))
    for key in ("enclosed_5pct_mean_density", "enclosed_10pct_mean_density",
                "half_mass_radius", "kinetic_over_abs_gravitational",
                "force_residual_rms_over_gravity", "inner_5pct_min_K",
                "inner_10pct_temperature_relative_std"):
        values = np.array([row[key] for row in window])
        times = np.array([row["t"] for row in window])
        mean = float(values.mean())
        span = float(times[-1] - times[0])
        slope = float(np.polyfit(times - times[0], values, 1)[0]) if len(window) >= 2 and span > 0 else None
        output[key] = dict(mean=mean, minimum=float(values.min()), maximum=float(values.max()),
                           relative_peak_to_peak=float(np.ptp(values) / abs(mean)) if mean != 0 else None,
                           slope_per_time=slope,
                           relative_slope_over_window=slope * span / abs(mean) if slope is not None and mean != 0 else None)
    return output


def simulate(model, *, t_end=4.0, samples=161, rtol=2e-7, atol=1e-9,
             wall_seconds=45.0, max_rhs_calls=300000, max_step=0.05,
             initial_state=None, initial_time=0.0, max_domain_retries=80,
             minimum_retry_step=1e-12):
    """Bounded sparse Radau with explicit state-domain rejection and restart."""
    numbers = [t_end, initial_time, rtol, atol, wall_seconds, max_step, minimum_retry_step]
    if (not np.all(np.isfinite(numbers)) or t_end <= initial_time or initial_time < 0
            or samples < 2 or min(rtol, atol, wall_seconds, max_step, minimum_retry_step) <= 0
            or max_rhs_calls < 1 or max_domain_retries < 1):
        raise ValueError("invalid run bounds")
    started = time.monotonic()
    y = model.initial_state() if initial_state is None else np.asarray(initial_state, dtype=float).copy()
    model.fields(y)
    initial_energy = model.energy(y)
    energy_scale = max(abs(initial_energy["total"]), np.finfo(float).tiny)
    initial = model.diagnostics(initial_time, y)
    history = [initial]
    targets = np.linspace(initial_time, t_end, samples)[1:]
    next_target, calls, accepted_steps = 0, 0, 0
    current_t = float(initial_time)
    max_energy_error = 0.0
    minimum_accepted_K = float(y[2 * model.n:].min())
    minimum_entropy = initial["total_entropy"]
    max_entropy_decrease = 0.0
    last_entropy = initial["total_entropy"]
    status, message = "completed", "reached declared finite end time"
    solver, failed_trial = None, None
    rejections = []
    stage_count_before = model.stage_memory_floor_count
    initial_minimum_stage_memory = model.minimum_stage_memory

    class RunLimit(RuntimeError):
        pass

    def bounded_rhs(t, state):
        nonlocal calls
        calls += 1
        if calls > max_rhs_calls:
            raise RunLimit("rhs_limit")
        if time.monotonic() - started > wall_seconds:
            raise RunLimit("wall_limit")
        try:
            return model.rhs(t, state)
        except collapse.ShellOrderingError as exc:
            exc.trial_time = float(t)
            raise

    def make_solver(first_step=None):
        return Radau(bounded_rhs, current_t, y.copy(), t_end, rtol=rtol, atol=atol,
                     max_step=max_step, first_step=first_step,
                     jac_sparsity=model.jacobian_sparsity())

    def record_rejection(reason, state, time_at_trial, attempted_step):
        nonlocal failed_trial
        record = dict(reason=reason, t=time_at_trial, attempted_step=attempted_step,
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
            except collapse.ShellOrderingError as exc:
                retry = record_rejection("shell_ordering_stage", exc.state, exc.trial_time, attempted_step)
                if len(rejections) >= max_domain_retries or retry < minimum_retry_step:
                    status, message = "domain_retry_limit", "invalid stage persisted at the declared retry bound"
                    break
                solver = make_solver(retry)
                continue
            if solver.status == "failed":
                status, message = "integrator_failed", "Radau could not take a step"
                break
            trial = solver.y.copy()
            if np.any(trial[2 * model.n:] < 0):
                retry = record_rejection("negative_accepted_memory", trial, float(solver.t), float(solver.t - current_t))
                if len(rejections) >= max_domain_retries or retry < minimum_retry_step:
                    status, message = "domain_retry_limit", "negative accepted memory persisted at the declared retry bound"
                    break
                solver = make_solver(retry)
                continue
            fields = model.fields(trial)
            gap = float(np.diff(np.r_[0.0, fields["r"]]).min())
            if gap < 1e-9 * model.radius / model.n:
                status, message = "minimum_gap", "stopped before the declared shell-gap floor"
                break
            y, current_t = trial, float(solver.t)
            accepted_steps += 1
            minimum_accepted_K = min(minimum_accepted_K, float(fields["K"].min()))
            energy_error = abs(model.energy(y)["total"] - initial_energy["total"]) / energy_scale
            max_energy_error = max(max_energy_error, float(energy_error))
            entropy = float(model.dm * np.sum(fields["sigma"]))
            minimum_entropy = min(minimum_entropy, entropy)
            max_entropy_decrease = max(max_entropy_decrease, last_entropy - entropy)
            last_entropy = entropy
            interpolate = solver.dense_output()
            while next_target < len(targets) and targets[next_target] <= current_t:
                target = float(targets[next_target])
                try:
                    history.append(model.diagnostics(target, interpolate(target)))
                except (ValueError, collapse.ShellOrderingError):
                    history.append(dict(t=target, sample_status="invalid_dense_interpolation"))
                next_target += 1
    except RunLimit as exc:
        status, message = str(exc), "resource bound reached; the requested finite-time result is inconclusive"
    except (ValueError, FloatingPointError) as exc:
        status, message = "invalid_state", str(exc)
    final = model.diagnostics(current_t, y)
    if history[-1].get("t") != current_t:
        history.append(final)
    good_samples = [row for row in history if "enclosed_5pct_mean_density" in row]
    return dict(
        schema_version=1, status=status, message=message, method="Radau",
        n_shells=model.n, t_initial=initial_time, t_requested=t_end, t_reached=current_t,
        initial_density=model.initial_density, initial_radius=model.radius,
        initial_velocity_gradient=model.velocity_gradient, total_mass=model.total_mass,
        material_parameters=asdict(model.params), transport_parameters=asdict(model.transport),
        transport_units=dict(diffusivity="physical length^2/time", damping_strength="dimensionless",
                             memory_activation="K/Kstar", temperature_bar="T/(3*Kstar*rho_q)"),
        rtol=rtol, atol=atol, max_step=max_step, wall_cap_seconds=wall_seconds,
        rhs_cap=max_rhs_calls, max_domain_retries=max_domain_retries,
        minimum_retry_step=minimum_retry_step, minimum_shell_gap=1e-9 * model.radius / model.n,
        elapsed_seconds=time.monotonic() - started, rhs_calls=calls, accepted_steps=accepted_steps,
        max_relative_energy_error=max_energy_error, minimum_accepted_K=minimum_accepted_K,
        minimum_accepted_total_entropy=minimum_entropy,
        max_single_step_entropy_decrease=max_entropy_decrease,
        stage_memory_floor_count=model.stage_memory_floor_count - stage_count_before,
        minimum_stage_memory=model.minimum_stage_memory,
        minimum_stage_memory_before_run=initial_minimum_stage_memory,
        domain_rejections=rejections,
        accepted_negative_memory_rejections=sum(row["reason"] == "negative_accepted_memory" for row in rejections),
        failed_trial=failed_trial,
        invalid_dense_sample_count=sum("sample_status" in row for row in history),
        peak_sampled_5pct_density=max(row["enclosed_5pct_mean_density"] for row in good_samples),
        initial=initial, final=final, time_history=history, settling=settling_metrics(history),
        final_profile=model.profile(y), final_state=y.tolist(),
        non_claims=["No 3D, convective or nonradial stability test", "No cosmological forest realization",
                    "No baryons", "No fitted halo envelope", "No certified continuum formation or settling result"],
    )


def atomic_json(path, result):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, prefix=f".{path.name}.",
                                         suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(result, handle, indent=2, allow_nan=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shells", type=int, default=32)
    parser.add_argument("--tau", type=float, default=0.5)
    parser.add_argument("--diffusivity", type=float, default=0.1)
    parser.add_argument("--damping-strength", type=float, default=1.0)
    parser.add_argument("--memory-activation", type=float, default=0.01)
    parser.add_argument("--t-end", type=float, default=4.0)
    parser.add_argument("--samples", type=int, default=161)
    parser.add_argument("--wall-seconds", type=float, default=45.0)
    parser.add_argument("--max-rhs-calls", type=int, default=300000)
    parser.add_argument("--rtol", type=float, default=2e-7)
    parser.add_argument("--atol", type=float, default=1e-9)
    parser.add_argument("--max-step", type=float, default=0.05)
    parser.add_argument("--restart", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    material_params = material.MaterialParameters(rho_q=1, G=1, a0=np.sqrt(8 * np.pi), tau=args.tau)
    transport_params = TransportParameters(args.diffusivity, args.damping_strength, args.memory_activation)
    model = TransportCollapse(args.shells, material_params, transport=transport_params)
    initial_state, initial_time = None, 0.0
    if args.restart is not None:
        previous = json.loads(args.restart.read_text())
        if (previous["n_shells"] != args.shells or previous["material_parameters"] != asdict(material_params)
                or previous["transport_parameters"] != asdict(transport_params)):
            parser.error("restart must have identical shell count and material/transport parameters")
        initial_state, initial_time = previous["final_state"], previous["t_reached"]
        model = TransportCollapse(args.shells, material_params, transport=transport_params,
                                  initial_density=previous["initial_density"],
                                  radius=previous["initial_radius"],
                                  initial_velocity_gradient=previous["initial_velocity_gradient"])
    result = simulate(model, t_end=args.t_end, samples=args.samples, rtol=args.rtol, atol=args.atol,
                      wall_seconds=args.wall_seconds, max_rhs_calls=args.max_rhs_calls,
                      max_step=args.max_step, initial_state=initial_state, initial_time=initial_time)
    atomic_json(args.output, result)
    print(json.dumps({key: result[key] for key in ("status", "n_shells", "t_reached", "elapsed_seconds",
                                                  "rhs_calls", "max_relative_energy_error")}, sort_keys=True))
    return 0 if result["status"] == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
