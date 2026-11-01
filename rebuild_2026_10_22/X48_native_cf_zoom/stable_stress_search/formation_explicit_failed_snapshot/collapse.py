"""Bounded 1D Lagrangian formation pilot, with an exact semidiscrete energy.

Contract: evolve one uniform cold sphere, not a cosmological or 3D halo. Equal
cell masses dm have moving outer interfaces r_i, node weights mu_i=dm except
mu_N=dm/2, m_i=i*dm, and a vacuum exterior. Egrav=-sum(G*mu_i*m_i/r_i).
Pressure work telescopes exactly against sum(dm*K*W); the same q heats and
pushes. Conservation in time remains a numerical diagnostic, not an assertion.
Any internal-stage shell crossing terminates the run at the last accepted state.
Negative intermediate RK K is evaluated using max(K,0) and counted; accepted
negative K fails without projection. No baryons, envelope model, heat conduction,
entropy mixing, equilibrium fitting, or production X48 force is included.
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np
from scipy.integrate import DOP853

import material


class ShellOrderingError(ValueError):
    """Raised before evaluating a nonpositive shell volume."""


class SphericalCollapse:
    """Conservative staggered shell model in the declared physical units."""

    def __init__(self, n_shells, params, initial_density=0.25, radius=1.0,
                 initial_velocity_gradient=-0.25):
        if not isinstance(n_shells, int) or n_shells < 2:
            raise ValueError("n_shells must be an integer >=2")
        if not np.all(np.isfinite([initial_density, radius, initial_velocity_gradient])):
            raise ValueError("initial sphere inputs must be finite")
        if initial_density <= 0 or radius <= 0:
            raise ValueError("initial density and radius must be positive")
        self.n = n_shells
        self.params = params
        self.initial_density = initial_density
        self.radius = radius
        self.velocity_gradient = initial_velocity_gradient
        self.total_mass = 4 * np.pi / 3 * radius**3 * initial_density
        self.dm = self.total_mass / self.n
        self.node_mass = self.dm * np.arange(1, self.n + 1)
        self.mu = np.full(self.n, self.dm)
        self.mu[-1] /= 2
        self.stage_memory_floor_count = 0
        self.minimum_stage_memory = 0.0

    def initial_state(self):
        r = self.radius * (np.arange(1, self.n + 1) / self.n)**(1 / 3)
        return np.concatenate([r, self.velocity_gradient * r, np.zeros(self.n)])

    def geometry(self, y):
        y = np.asarray(y, dtype=float)
        if y.shape != (3 * self.n,) or not np.all(np.isfinite(y)):
            raise ValueError("state must contain finite r,u,K arrays")
        r, u, K = np.split(y, 3)
        if np.any(np.diff(np.r_[0.0, r]) <= 0):
            raise ShellOrderingError("shell ordering violated at an ODE stage")
        volume = 4 * np.pi / 3 * np.diff(np.r_[0.0, r**3])
        volume_dot = 4 * np.pi * np.diff(np.r_[0.0, r**2 * u])
        return r, u, K, volume, self.dm / volume, volume_dot / volume

    def fields(self, y, *, stage_extension=False):
        r, u, K, volume, rho, theta = self.geometry(y)
        if np.any(K < 0):
            if not stage_extension:
                raise ValueError("accepted state has negative K")
            self.stage_memory_floor_count += 1
            self.minimum_stage_memory = min(self.minimum_stage_memory, float(K.min()))
        K_eval = np.maximum(K, 0) if stage_extension else K
        pressure = material.pressure(rho, K_eval, self.params)
        q, dk = material.bulk_viscosity_source(rho, theta, self.params)
        return dict(r=r, u=u, K=K, volume=volume, rho=rho, theta=theta,
                    pressure=pressure, q=q, dk=dk)

    def rhs(self, t, y):
        f = self.fields(y, stage_extension=True)
        stress = f["pressure"] + f["q"]
        force = 4 * np.pi * f["r"]**2 * np.diff(np.r_[-stress, 0.0])
        acceleration = force / self.mu - self.params.G * self.node_mass / f["r"]**2
        return np.concatenate([f["u"], acceleration, f["dk"]])

    def energy(self, y):
        r, u, K, _, rho, _ = self.geometry(y)
        internal = float(self.dm * np.sum(material.specific_energy(rho, K, self.params)))
        kinetic = float(np.sum(0.5 * self.mu * u**2))
        gravitational = float(-np.sum(self.params.G * self.mu * self.node_mass / r))
        return dict(internal=internal, kinetic=kinetic, gravitational=gravitational,
                    total=internal + kinetic + gravitational)

    def enclosed_estimator(self, y, fraction):
        """Radius and mean density enclosing an exact fraction of conserved mass.

        Within a cell, interpolate its volume at constant cell density. Thus the
        5% estimator need not correspond to an integer number of shells.
        """
        if not 0 < fraction <= 1:
            raise ValueError("enclosed fraction must lie in (0,1]")
        r = self.geometry(y)[0]
        count = fraction * self.n
        whole = min(int(np.floor(count)), self.n - 1)
        remainder = count - whole
        inner_cube = 0.0 if whole == 0 else r[whole - 1]**3
        enclosed_cube = inner_cube + remainder * (r[whole]**3 - inner_cube)
        radius = enclosed_cube**(1 / 3)
        density = fraction * self.total_mass / (4 * np.pi / 3 * enclosed_cube)
        return float(radius), float(density)

    def diagnostics(self, t, y):
        f = self.fields(y)
        r05, rho05 = self.enclosed_estimator(y, 0.05)
        r10, rho10 = self.enclosed_estimator(y, 0.10)
        r50, _ = self.enclosed_estimator(y, 0.50)
        crossings = np.flatnonzero(f["rho"] <= rho05 / 2)
        core_radius = float(f["r"][crossings[0]]) if len(crossings) else float(f["r"][-1])
        gradient = np.diff(f["K"]) / np.diff(f["r"])
        return dict(t=float(t), first_shell_density=float(f["rho"][0]),
                    enclosed_5pct_mean_density=rho05, enclosed_10pct_mean_density=rho10,
                    enclosed_5pct_radius=r05, enclosed_10pct_radius=r10,
                    half_mass_radius=r50, outer_radius=float(f["r"][-1]),
                    half_density_core_radius=core_radius,
                    half_density_crossing_found=bool(len(crossings)),
                    half_mass_potential_depth=self.params.G * self.total_mass / (2 * r50),
                    max_K=float(f["K"].max()), min_K=float(f["K"].min()),
                    min_radial_K_gradient=float(gradient.min()),
                    max_radial_K_gradient=float(gradient.max()),
                    negative_K_gradient_fraction=float(np.mean(gradient < -1e-10 * self.params.k_star / self.radius)),
                    min_shell_gap=float(np.diff(np.r_[0.0, f["r"]]).min()),
                    **self.energy(y))

    def profile(self, y):
        f = self.fields(y)
        return {key: f[key].tolist() for key in ("r", "u", "K", "rho", "theta", "pressure", "q")}


def simulate(model, *, t_end=8.0, samples=161, rtol=2e-7, atol=1e-9,
             wall_seconds=40.0, max_rhs_calls=300000, max_step=0.05):
    """Run a bounded DOP853 pilot; resource limits return inconclusive statuses."""
    if t_end <= 0 or samples < 2 or wall_seconds <= 0 or max_rhs_calls < 1:
        raise ValueError("invalid run bounds")
    started = time.monotonic()
    y = model.initial_state()
    initial_energy = model.energy(y)
    energy_scale = max(abs(initial_energy["total"]), np.finfo(float).tiny)
    initial = model.diagnostics(0, y)
    history = [initial]
    targets = np.linspace(0, t_end, samples)[1:]
    next_target = 0
    calls = 0

    class RunLimit(RuntimeError):
        pass

    def bounded_rhs(t, state):
        nonlocal calls
        calls += 1
        if calls > max_rhs_calls:
            raise RunLimit("rhs_limit")
        if time.monotonic() - started > wall_seconds:
            raise RunLimit("wall_limit")
        return model.rhs(t, state)

    current_t, accepted_steps, max_energy_error = 0.0, 0, 0.0
    minimum_accepted_K = 0.0
    status, message = "completed", "reached declared finite end time"
    solver = None
    try:
        solver = DOP853(bounded_rhs, 0, y, t_end, rtol=rtol, atol=atol, max_step=max_step)
        while solver.status == "running":
            solver.step()
            if solver.status == "failed":
                status, message = "integrator_failed", "DOP853 could not take a step"
                break
            trial = solver.y.copy()
            fields = model.fields(trial)
            min_gap = float(np.diff(np.r_[0.0, fields["r"]]).min())
            if min_gap < 1e-9 * model.radius / model.n:
                status, message = "minimum_gap", "stopped before the declared shell-gap floor"
                break
            y, current_t = trial, float(solver.t)
            accepted_steps += 1
            minimum_accepted_K = min(minimum_accepted_K, float(fields["K"].min()))
            error = abs(model.energy(y)["total"] - initial_energy["total"]) / energy_scale
            max_energy_error = max(max_energy_error, float(error))
            interpolant = solver.dense_output()
            while next_target < len(targets) and targets[next_target] <= current_t:
                target = float(targets[next_target])
                sample_state = interpolant(target)
                # Dense interpolation can undershoot a monotone source near its
                # onset. Do not project or silently use a nonphysical sample.
                try:
                    sample = model.diagnostics(target, sample_state)
                    history.append(sample)
                except (ValueError, ShellOrderingError):
                    history.append(dict(t=target, sample_status="invalid_dense_interpolation"))
                next_target += 1
    except RunLimit as exc:
        status, message = str(exc), "resource bound reached; finite-time result is inconclusive"
    except ShellOrderingError as exc:
        status, message = "shell_ordering_stage", str(exc)
    except ValueError as exc:
        status, message = "invalid_state", str(exc)
    final = model.diagnostics(current_t, y)
    if not history or history[-1].get("t") != current_t:
        history.append(final)
    good_samples = [row for row in history if "enclosed_5pct_mean_density" in row]
    return dict(status=status, message=message, n_shells=model.n,
                t_requested=t_end, t_reached=current_t, tau=model.params.tau,
                initial_density=model.initial_density, initial_radius=model.radius,
                initial_velocity_gradient=model.velocity_gradient,
                K_initial=0.0, total_mass=model.total_mass,
                rtol=rtol, atol=atol, max_step=max_step,
                wall_cap_seconds=wall_seconds, rhs_cap=max_rhs_calls,
                elapsed_seconds=time.monotonic() - started,
                rhs_calls=calls, accepted_steps=accepted_steps,
                max_relative_energy_error=max_energy_error,
                minimum_accepted_K=minimum_accepted_K,
                stage_memory_floor_count=model.stage_memory_floor_count,
                minimum_stage_memory=model.minimum_stage_memory,
                peak_sampled_5pct_density=max(row["enclosed_5pct_mean_density"] for row in good_samples),
                initial=initial, final=final, time_history=history,
                final_profile=model.profile(y),
                non_claims=["No 3D or convective stability test", "No resolved halo envelope",
                            "No forest comparison", "No baryons", "No certified continuum formation result"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shells", type=int, default=64)
    parser.add_argument("--tau", type=float, default=0.5)
    parser.add_argument("--t-end", type=float, default=8.0)
    parser.add_argument("--samples", type=int, default=161)
    parser.add_argument("--wall-seconds", type=float, default=40.0)
    parser.add_argument("--max-rhs-calls", type=int, default=300000)
    parser.add_argument("--rtol", type=float, default=2e-7)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    params = material.MaterialParameters(rho_q=1, G=1, a0=np.sqrt(8 * np.pi), tau=args.tau)
    result = simulate(SphericalCollapse(args.shells, params), t_end=args.t_end,
                      samples=args.samples, wall_seconds=args.wall_seconds,
                      max_rhs_calls=args.max_rhs_calls, rtol=args.rtol)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    summary = {key: result[key] for key in ("status", "n_shells", "tau", "t_reached",
               "elapsed_seconds", "rhs_calls", "max_relative_energy_error", "peak_sampled_5pct_density")}
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
