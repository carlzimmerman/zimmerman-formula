"""Deterministic posthoc centring and instantaneous self-boundness diagnostics.

This changes no forces, particles, random draws, or saved simulation state.
The centre is the deepest *local self-potential minimum found* from cold kNN
density seeds and stellar density/potential seeds. The host potential is
deliberately excluded: its minimum is the host, not the dwarf remnant.
This finite seed search is not a certified global optimization.

The separate endpoint unbinding test starts within a stated finite radius,
uses the same softened pair potential with each particle's self term removed,
and monotonically removes positive-energy particles in a fitted bulk frame.
It is instantaneous isolated self-boundness, not a Jacobi criterion or proof
of survival in the host tidal field. Its radius and centre dependence are
reported. A density aperture is not automatically a bound core.
"""
import numpy as np
from scipy.optimize import minimize
from scipy.spatial import cKDTree


G = 0.004498638185693768


def _validate(x, m, cold, eps):
    x, m, cold = np.asarray(x, float), np.asarray(m, float), np.asarray(cold, bool)
    if (x.shape != (len(m), 3) or cold.shape != m.shape or len(m) == 0
            or np.any(m <= 0.) or eps <= 0. or not np.all(np.isfinite(x))):
        raise ValueError("finite positions (N,3), positive masses and eps, matching cold mask required")
    return x, m, cold


def _potential(points, x, m, eps):
    """Exact softened test-point potential, in bounded-memory chunks."""
    points = np.asarray(points, float).reshape(-1, 3)
    result = np.empty(len(points))
    for first in range(0, len(points), 64):
        delta = points[first:first + 64, None, :] - x[None, :, :]
        inverse_r = 1. / np.sqrt(np.einsum("ijk,ijk->ij", delta, delta) + eps * eps)
        result[first:first + 64] = -G * (inverse_r @ m)
    return result


def _seeds(x, m, cold, eps):
    seeds = []
    separation = max(2. * eps, 50.)

    def add(point, label):
        if not any(np.linalg.norm(point - prior[0]) < separation for prior in seeds):
            seeds.append((point.copy(), label))

    for mask, label, neighbors in ((cold, "cold_knn", (16, 32, 64)),
                                    (~cold, "star_knn", (8,))):
        ids = np.flatnonzero(mask)
        if len(ids) == 0:
            continue
        tree = cKDTree(x[ids])
        for requested in neighbors:
            k = min(requested + 1, len(ids))
            distances, _ = tree.query(x[ids], k=k)
            radii = distances[:, -1] if k > 1 else np.zeros(len(ids))
            before = len(seeds)
            for rank in np.argsort(radii, kind="stable"):
                add(x[ids[rank]], label + str(k - 1))
                if len(seeds) >= before + 2:
                    break
    stars = np.flatnonzero(~cold)
    if len(stars):
        potentials = _potential(x[stars], x, m, eps)
        # Equal stellar masses make the individual soft self term irrelevant
        # to ranking; explicitly remove it for general unequal-mass inputs.
        potentials += G * m[stars] / eps
        for rank in np.argsort(potentials, kind="stable")[:8]:
            add(x[stars[rank]], "stellar_self_potential")
            if len(seeds) >= 12:
                break
    if not seeds:
        add(x[np.argmax(m)], "mass_seed")
    return seeds[:12]


def _candidate_centres(x, m, cold, eps):
    seeds = _seeds(x, m, cold, eps)
    found = []
    for seed, label in seeds:
        relative_x = x - seed

        def objective(offset):
            displacement = offset - relative_x
            inverse_r = 1. / np.sqrt(np.einsum("ij,ij->i", displacement, displacement) + eps * eps)
            value = -G * np.sum(m * inverse_r)
            gradient = G * np.sum((m * inverse_r ** 3)[:, None] * displacement, axis=0)
            return value, gradient

        fit = minimize(objective, np.zeros(3), jac=True, method="L-BFGS-B",
                       bounds=[(-600., 600.)] * 3,
                       options=dict(ftol=1.e-13, gtol=1.e-10, maxiter=150, maxls=40))
        centre = seed + fit.x
        if any(np.linalg.norm(centre - prior["centre"]) < 1. for prior in found):
            continue
        found.append(dict(centre=centre, potential=float(fit.fun), seed_label=label,
                          optimizer_success=bool(fit.success),
                          refinement_hit_boundary=bool(np.any(np.abs(fit.x) > 599.99))))
    found.sort(key=lambda row: row["potential"])
    return found, seeds


def remnant_centre(x, m, cold, eps=40.):
    """Cheap deterministic geometry-only centre; does not consume any RNG."""
    x, m, cold = _validate(x, m, cold, eps)
    candidates, _ = _candidate_centres(x, m, cold, eps)
    return candidates[0]["centre"].copy()


def _weighted_median(values, mass):
    answer = []
    for axis in range(3):
        order = np.argsort(values[:, axis], kind="stable")
        index = np.searchsorted(np.cumsum(mass[order]), .5 * np.sum(mass))
        answer.append(values[order[min(index, len(order) - 1)], axis])
    return np.asarray(answer)


def _unbind(x, v, m, centre, eps, radius):
    distance = np.linalg.norm(x - centre, axis=1)
    ids = np.flatnonzero(distance <= radius)
    if len(ids) == 0:
        return ids, np.zeros(3), 0
    inner = np.flatnonzero(distance <= min(300., radius))
    if len(inner) == 0:
        inner = ids
    bulk = _weighted_median(v[inner], m[inner])
    iterations = 0
    for iterations in range(1, 51):
        potential = _potential(x[ids], x[ids], m[ids], eps) + G * m[ids] / eps
        energy = .5 * np.sum((v[ids] - bulk) ** 2, axis=1) + potential
        keep = energy < 0.
        if not np.any(keep):
            return np.empty(0, dtype=int), bulk, iterations
        retained = ids[keep]
        new_bulk = np.average(v[retained], axis=0, weights=m[retained])
        stable = len(retained) == len(ids) and np.linalg.norm(new_bulk - bulk) < 1.e-9
        ids, bulk = retained, new_bulk
        if stable:
            break
    return ids, bulk, iterations


def _aperture(x, m, cold, centre, radius, bound=None):
    inside = np.linalg.norm(x - centre, axis=1) <= radius
    if bound is not None:
        inside &= bound
    return dict(cold_mass_Msun=float(m[inside & cold].sum()),
                cold_count=int(np.count_nonzero(inside & cold)),
                stellar_mass_Msun=float(m[inside & ~cold].sum()),
                star_count=int(np.count_nonzero(inside & ~cold)))


def diagnose_remnant(x, v, m, cold, eps=40., binding_radius=1000.):
    """Endpoint centre sensitivity, apertures, and local self-unbinding."""
    x, m, cold = _validate(x, m, cold, eps)
    v = np.asarray(v, float)
    if v.shape != x.shape or not np.all(np.isfinite(v)) or binding_radius <= 0.:
        raise ValueError("finite velocities matching positions and positive binding radius required")
    candidates, seeds = _candidate_centres(x, m, cold, eps)
    centre = candidates[0]["centre"]
    bound_ids, bulk, iterations = _unbind(x, v, m, centre, eps, binding_radius)
    bound = np.zeros(len(m), bool); bound[bound_ids] = True
    aperture = {str(radius): _aperture(x, m, cold, centre, radius) for radius in (100, 300)}
    bound_aperture = {str(radius): _aperture(x, m, cold, centre, radius, bound) for radius in (100, 300)}
    for row in candidates:
        row["M300"] = _aperture(x, m, cold, row["centre"], 300.)["cold_mass_Msun"]
        row["centre"] = row["centre"].tolist()
    density_seed_accounts = [dict(label=label, centre=seed.tolist(),
                                  **_aperture(x, m, cold, seed, 300.)) for seed, label in seeds]
    # For any nonempty radius-R aperture choose a member p: every other member
    # is within 2R of p. Thus max particle-centred M(2R) is a rigorous, loose
    # upper bound on the mass in any radius-R aperture, independent of seeds.
    cold_ids = np.flatnonzero(cold)
    upper_bound = 0.
    if len(cold_ids):
        tree = cKDTree(x[cold_ids])
        neighborhoods = tree.query_ball_point(x[cold_ids], 600.00000001)
        upper_bound = max(float(m[cold_ids[neighbors]].sum()) for neighbors in neighborhoods)
    return dict(centre=centre.tolist(), centre_definition="deepest found local minimum of all-member softened self-potential",
                M100=aperture["100"]["cold_mass_Msun"], M300=aperture["300"]["cold_mass_Msun"],
                cold_count300=aperture["300"]["cold_count"], star_count300=aperture["300"]["star_count"],
                bound_M100=bound_aperture["100"]["cold_mass_Msun"],
                bound_M300=bound_aperture["300"]["cold_mass_Msun"],
                bound_star_count300=bound_aperture["300"]["star_count"],
                aperture=aperture, bound_aperture=bound_aperture,
                binding_radius_pc=float(binding_radius), bound_indices=bound_ids.tolist(),
                bound_bulk_velocity_pc_Myr=bulk.tolist(), unbinding_iterations=iterations,
                self_bound_mass_Msun=float(m[bound].sum()),
                instantaneously_self_bound_remnant=bool(np.any(bound & cold)),
                any_centre_M300_upper_bound_Msun=upper_bound,
                candidates=candidates, seed_apertures=density_seed_accounts,
                interpretation="Posthoc diagnostic only; finite-seed centre search and finite-radius isolated instantaneous self-unbinding; no new physics or tidal-survival proof.")
