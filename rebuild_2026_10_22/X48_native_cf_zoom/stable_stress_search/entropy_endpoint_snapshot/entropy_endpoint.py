"""Construct, without evolving mixing, an entropy-sorted hydrostatic endpoint.

Contract: retain the measured equal-mass parcel K values and source-byte hash,
sort those values by enclosed mass, and interpolate linearly between parcel
centers (clipping at both ends). This preserves the discrete parcel values and
the integral of K in mass; it defines a continuous proxy between those values.
Shoot regular spherical P(r),m(r) hydrostatics to P=0 at fixed cold mass. Compare
its energy with the measured cold initial energy. Only if the sorted state is
energetically allowed, increase all parcel K by one common alpha>=1 to match
that energy. This constructs an admissible endpoint; no convective mixing law,
flow reachability, cosmological halo envelope, or 3D stability is demonstrated.
"""

import argparse
import hashlib
import json
from pathlib import Path
import time

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq

import material


_d_table = np.linspace(1.0, 2.0, 4097)
_t_table = _d_table - 1
_w_table = _d_table * _t_table * np.sqrt(3 - 2 * _t_table)
_inverse_pressure_root = PchipInterpolator(_w_table, _d_table, extrapolate=False)


class EntropyProfile:
    """Positive measured parcel coefficients; no entropy floor is introduced."""

    def __init__(self, K_samples, total_mass, *, input_sha256=None, input_path=None,
                 source_time=None, initial_energy=None):
        values = np.asarray(K_samples, dtype=float)
        if values.ndim != 1 or len(values) < 2 or not np.all(np.isfinite(values)) or np.any(values <= 0):
            raise ValueError("endpoint hydrostatics requires finite K>0 for every parcel")
        if not np.isfinite(total_mass) or total_mass <= 0:
            raise ValueError("total cold mass must be positive and finite")
        self.original_K = values.copy()
        self.sorted_K = np.sort(values)
        self.total_mass = float(total_mass)
        self.centers = (np.arange(len(values)) + 0.5) * self.total_mass / len(values)
        self.input_sha256, self.input_path = input_sha256, input_path
        self.source_time, self.initial_energy = source_time, initial_energy

    def coefficient(self, m, alpha=1.0):
        if not np.isfinite(alpha) or alpha < 1:
            raise ValueError("alpha must be finite and >=1")
        return alpha * np.interp(m, self.centers, self.sorted_K)

    def coefficient_derivative(self, m, alpha=1.0):
        values = np.asarray(m)
        indices = np.clip(np.searchsorted(self.centers, values) - 1, 0, len(self.sorted_K) - 2)
        slopes = np.diff(self.sorted_K) / np.diff(self.centers)
        return np.where((values > self.centers[0]) & (values < self.centers[-1]), alpha * slopes[indices], 0)


def load_collapse(path):
    """Read the exact final K profile and initial energy of one measured run."""
    path = Path(path)
    raw = path.read_bytes()
    data = json.loads(raw)
    values = data["final_profile"]["K"]
    if len(values) != data["n_shells"]:
        raise ValueError("collapse shell count and final K count disagree")
    return EntropyProfile(values, data["total_mass"], input_sha256=hashlib.sha256(raw).hexdigest(),
                          input_path=str(path.resolve()), source_time=data["t_reached"],
                          initial_energy=data["initial"]["total"])


def density_from_pressure(P, K, params):
    """Inverse occupied EOS branch, rho>=rho_q, including its P=0 limit.

    The inverse table uses sqrt(P/(K*rho_q**2)), which is smooth at the gate.
    Its accuracy is checked against the independent material evaluator.
    """
    P, K = np.broadcast_arrays(np.asarray(P, dtype=float), np.asarray(K, dtype=float))
    if np.any(~np.isfinite(P)) or np.any(P < 0) or np.any(~np.isfinite(K)) or np.any(K <= 0):
        raise ValueError("require finite P>=0 and K>0")
    w = np.sqrt(P / K) / params.rho_q
    d = np.where(w >= 2, w, _inverse_pressure_root(np.minimum(w, 2)))
    return params.rho_q * d


def entropy_integrals(profile, params, *, alpha=1.0):
    """Analytic mass integrals of sigma=(K/Kstar)**(1/3), before/after proxying.

    Concavity implies the linear-K continuous proxy has at least the discrete
    parcel entropy integral. Sorting alone preserves the latter exactly.
    """
    K = profile.sorted_K
    sigma = np.cbrt(K / params.k_star)
    relative_step = np.diff(K) / K[:-1]
    average = sigma[:-1].copy()
    nonzero = relative_step != 0
    average[nonzero] *= (0.75 * np.expm1(4 / 3 * np.log1p(relative_step[nonzero]))
                         / relative_step[nonzero])
    dm = profile.total_mass / len(K)
    discrete = float(dm * sigma.sum())
    continuous = float(dm * (sigma[0] / 2 + sigma[-1] / 2 + average.sum()))
    return dict(source_discrete_sigma_mass_integral=discrete,
                sorted_continuous_sigma_mass_integral=continuous,
                endpoint_continuous_sigma_mass_integral=alpha**(1 / 3) * continuous,
                interpolation_relative_entropy_increase=continuous / discrete - 1,
                alpha_sigma_factor=alpha**(1 / 3),
                discrete_K_mass_integral=float(dm * K.sum()))


def solve_equilibrium(profile, params, *, alpha=1.0, rtol=2e-7,
                      output_points=1025, deadline=None, baryon_mass=0.0,
                      baryon_scale=1.0):
    """Shoot central pressure to preserve cold mass, with optional Plummer load."""
    if rtol <= 0 or output_points < 3 or baryon_mass < 0 or baryon_scale <= 0:
        raise ValueError("invalid equilibrium bounds or baryonic load")
    M, G, rho_q = profile.total_mass, params.G, params.rho_q
    radius_bound = (3 * 2.01 * M / (4 * np.pi * rho_q))**(1 / 3)
    pressure_unit = G * M**(2 / 3) * rho_q**(4 / 3)
    shots = 0

    def integrate(Pc, dense=False):
        nonlocal shots
        shots += 1
        Kc = float(profile.coefficient(0, alpha))
        dc = float(density_from_pressure(Pc, Kc, params))
        start = min(radius_bound * 1e-7, np.sqrt(Pc / (G * dc**2)) * 1e-4)
        rho_b_center = 3 * baryon_mass / (4 * np.pi * baryon_scale**3)
        m0 = 4 * np.pi / 3 * dc * start**3
        initial = [m0, Pc - 2 * np.pi * G / 3 * dc * (dc + rho_b_center) * start**2,
                   m0 * Kc * float(material.density_weight(dc, params)),
                   -16 * np.pi**2 * G * dc**2 * start**5 / 15,
                   -G * baryon_mass / baryon_scale * m0]

        def rhs(r, y):
            if deadline is not None and time.monotonic() > deadline:
                raise TimeoutError("endpoint wall budget exhausted")
            m, pressure = y[:2]
            K = float(profile.coefficient(m, alpha))
            rho = float(density_from_pressure(max(pressure, 0), K, params))
            dm = 4 * np.pi * r**2 * rho
            mb = baryon_mass * (r / np.hypot(r, baryon_scale))**3
            e = K * float(material.density_weight(rho, params))
            return [dm, -G * (m + mb) * rho / r**2,
                    e * dm, -G * m / r * dm,
                    -G * baryon_mass / np.hypot(r, baryon_scale) * dm]

        def surface(r, y):
            return y[1]

        def mass_cap(r, y):
            return y[0] - 2 * M

        surface.terminal, surface.direction = True, -1
        mass_cap.terminal, mass_cap.direction = True, 1
        sol = solve_ivp(rhs, (start, radius_bound), initial, events=(surface, mass_cap),
                        rtol=rtol, atol=rtol * 1e-3, dense_output=dense, max_step=radius_bound / 40)
        if not sol.success:
            raise RuntimeError(sol.message)
        reached_surface = len(sol.t_events[0]) == 1
        if not reached_surface and len(sol.t_events[1]) != 1:
            raise RuntimeError("neither surface nor mass cap reached")
        return sol, dc, reached_surface, start

    def residual(log_pressure):
        sol = integrate(float(np.exp(log_pressure)))[0]
        return float(sol.y[0, -1] / M - 1)

    low, high = np.log(pressure_unit * 1e-9), np.log(pressure_unit)
    if residual(low) >= 0:
        raise RuntimeError("low-pressure mass bracket is not below the target")
    for _ in range(24):
        if residual(high) >= 0:
            break
        high += np.log(4)
    else:
        raise RuntimeError("central-pressure mass bracket exhausted")
    root = brentq(residual, low, high, xtol=2e-9, rtol=2e-9)
    Pc = float(np.exp(root))
    sol, dc, reached_surface, start = integrate(Pc, dense=True)
    if not reached_surface:
        raise RuntimeError("fixed-mass root did not reach a free surface")
    radius, mass = float(sol.t[-1]), float(sol.y[0, -1])
    radii = np.linspace(start, radius, output_points - 1)
    m, pressure, internal, gravitational, external = sol.sol(radii)
    K = profile.coefficient(m, alpha)
    rho = density_from_pressure(np.maximum(pressure, 0), K, params)
    # Add the regular central limit explicitly; exclude the vacuum exterior.
    radii = np.r_[0.0, radii]
    m, pressure = np.r_[0.0, m], np.r_[Pc, np.maximum(pressure, 0)]
    K, rho = np.r_[profile.coefficient(0, alpha), K], np.r_[dc, rho]
    h = material.activation(rho / rho_q)
    c2 = material.sound_speed_squared(rho, K, params)
    gamma = np.divide(rho * c2, pressure, out=np.full_like(rho, np.inf), where=pressure > Pc * 1e-12)
    dK_dr = profile.coefficient_derivative(m, alpha) * 4 * np.pi * radii**2 * rho
    enclosed_baryons = baryon_mass * (radii / np.hypot(radii, baryon_scale))**3
    gravity = np.divide(G * (m + enclosed_baryons), radii**2, out=np.zeros_like(m), where=radii > 0)
    N2 = np.divide(gravity * rho * h * dK_dr, c2, out=np.zeros_like(m), where=c2 > 0)
    active = (pressure > Pc * 1e-12) & np.isfinite(gamma)
    half_mass = brentq(lambda r: float(sol.sol(r)[0]) - M / 2, start, radius)
    five_pct = brentq(lambda r: float(sol.sol(r)[0]) - M * 0.05, start, radius)
    core_indices = np.flatnonzero(rho <= dc / 2)
    core = float(radii[core_indices[0]]) if len(core_indices) else radius
    U, V, B = (float(sol.y[j, -1]) for j in (2, 3, 4))
    return dict(alpha=alpha, central_pressure=Pc, central_density=dc, radius=radius,
                cold_mass=mass, target_cold_mass=M, relative_mass_error=abs(mass / M - 1),
                five_pct_radius=five_pct, half_mass_radius=half_mass, core_radius=core,
                half_density_crossing_found=bool(len(core_indices)),
                internal_energy=U, gravitational_energy=V, external_energy=B, total_energy=U + V + B,
                minimum_active_gamma1=float(gamma[active].min()),
                minimum_buoyancy_squared=float(N2.min()), maximum_buoyancy_squared=float(N2.max()),
                parcel_K=(alpha * profile.sorted_K).tolist(), shooting_integrations=shots,
                baryon_mass=baryon_mass, baryon_scale=baryon_scale, rtol=rtol,
                profile=dict(r=radii.tolist(), m=m.tolist(), P=pressure.tolist(),
                             rho=rho.tolist(), K=K.tolist(), N2=N2.tolist()))


def construct_endpoint(profile, params, *, target_energy=None, rtol=2e-7, wall_seconds=22):
    """Check sorted energy, then match energy by increasing all K together."""
    started = time.monotonic()
    deadline = started + wall_seconds
    target = profile.initial_energy if target_energy is None else target_energy
    if target is None or not np.isfinite(target):
        raise ValueError("a finite target energy is required")
    cache = {}

    def solve(alpha):
        if alpha not in cache:
            cache[alpha] = solve_equilibrium(profile, params, alpha=alpha, rtol=rtol, deadline=deadline)
        return cache[alpha]

    base = solve(1.0)
    scale = max(abs(target), 1e-12)
    if base["total_energy"] > target + 1e-7 * scale:
        return dict(status="energetic_obstruction", alpha=None, endpoint=None,
                    sorted_equilibrium=base, target_energy=target,
                    elapsed_seconds=time.monotonic() - started)
    if abs(base["total_energy"] - target) <= 1e-7 * scale:
        alpha = 1.0
    else:
        high = 2.0
        for _ in range(10):
            if solve(high)["total_energy"] >= target:
                break
            high *= 2
        else:
            raise RuntimeError("alpha energy bracket exhausted")
        alpha = float(brentq(lambda a: solve(a)["total_energy"] - target,
                             1.0, high, xtol=2e-8, rtol=2e-8))
    result = solve(alpha)
    return dict(status="constructed_endpoint", alpha=alpha, endpoint=result,
                sorted_equilibrium=base, target_energy=target,
                relative_energy_error=abs(result["total_energy"] - target) / scale,
                source_time=profile.source_time, input_sha256=profile.input_sha256,
                input_path=profile.input_path, measured_K_min=float(profile.sorted_K.min()),
                measured_K_max=float(profile.sorted_K.max()),
                energy_alpha_trace=[dict(alpha=a, energy=v["total_energy"]) for a, v in sorted(cache.items())],
                entropy_integrals=entropy_integrals(profile, params, alpha=alpha),
                elapsed_seconds=time.monotonic() - started,
                non_claims=["Constructed endpoint, not an implemented mixing evolution",
                            "No proof that collapse reaches this state", "No 3D stability calculation",
                            "Linear interpolation is a continuous proxy for measured parcel entropies"])


def compare_plummer_loading(profile, params, reference, *, rtol=2e-9, deadline=None):
    """One fixed-K, fixed-mass quasistatic load and a circular-shell reference."""
    M, alpha = profile.total_mass, reference["alpha"]
    Mb, b = 0.3 * M, 0.1 * reference["radius"]
    loaded = solve_equilibrium(profile, params, alpha=alpha, rtol=rtol,
                               baryon_mass=Mb, baryon_scale=b, deadline=deadline)
    comparisons = []
    for fraction, key in [(0.05, "five_pct_radius"), (0.5, "half_mass_radius")]:
        initial_radius = reference[key]
        shell_mass = fraction * M

        def circular_residual(r):
            mb = Mb * (r / np.hypot(r, b))**3
            return r * (shell_mass + mb) - initial_radius * shell_mass

        circular_radius = brentq(circular_residual, 0, initial_radius, xtol=1e-12)
        comparisons.append(dict(mass_fraction=fraction, initial_radius=initial_radius,
                                loaded_radius=loaded[key], circular_reference_radius=circular_radius,
                                pressure_radius_ratio=loaded[key] / initial_radius,
                                circular_radius_ratio=circular_radius / initial_radius,
                                pressure_radius_exceeds_reference=loaded[key] > circular_radius))
    return dict(status="quasistatic_plummer_comparison", unchanged_alpha=alpha,
                baryon_mass=Mb, baryon_scale=b, comparisons=comparisons, loaded_equilibrium=loaded,
                non_claims=["Prescribed smooth spherical baryons, not a disc",
                            "Circular shell reference is a comparison model, not general dust dynamics",
                            "No additional entropy generation or alpha adjustment"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collapse-input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--rtol", type=float, default=2e-7)
    parser.add_argument("--wall-seconds", type=float, default=22)
    parser.add_argument("--plummer-check", action="store_true")
    args = parser.parse_args()
    profile = load_collapse(args.collapse_input)
    params = material.MaterialParameters(rho_q=1, G=1, a0=np.sqrt(8 * np.pi), tau=0.5)
    started = time.monotonic()
    try:
        result = construct_endpoint(profile, params, rtol=args.rtol, wall_seconds=args.wall_seconds)
        if args.plummer_check and result["status"] == "constructed_endpoint":
            try:
                result["plummer_check"] = compare_plummer_loading(
                    profile, params, result["endpoint"], rtol=args.rtol,
                    deadline=started + args.wall_seconds)
            except TimeoutError as exc:
                result["plummer_check"] = dict(status="wall_limit", message=str(exc))
    except TimeoutError as exc:
        result = dict(status="wall_limit", message=str(exc), input_sha256=profile.input_sha256)
    result["total_elapsed_seconds"] = time.monotonic() - started
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "alpha", "relative_energy_error", "elapsed_seconds") if key in result}))


if __name__ == "__main__":
    main()
