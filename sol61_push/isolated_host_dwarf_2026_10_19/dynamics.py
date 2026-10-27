"""Newtonian carrier/stars kernel in pc, Msun, and Myr.

Gravity is the full, central, softened pair Hamiltonian, with no target density.
The optional host is a static Plummer potential; it has no live heat reservoir.

The collision kernel is a finite spatial approximation to isotropic elastic
Boltzmann scattering. For each unordered carrier pair within h, n points from
j to i and w=v_i-v_j. An approaching pair receives the central reflection
w' = w - 2(w.n)n, with event probability

    m (sigma/m) W_h 4 max(-w.n, 0) dt,  W_h=3/(4 pi h^3).

For locally uniform pair directions, q=-w.n/|w| has incoming event density
2q on [0,1]. Hence cos(theta)=1-2q^2 is uniform on [-1,1], giving isotropic
outgoing scattering. The sphere average of 4 max(-w.n,0) is |w|, so the
orientation-averaged rate is the usual m(sigma/m) W_h |w|. Each realized
central impulse conserves energy, momentum, and all three components of
orbital angular momentum, even at finite separation. Spatial locality and
sequential multiple-collision errors still require h and dt controls; exact
conservation alone does not validate this finite kernel as a Boltzmann solver.

All neighbor candidates are visited once in random order. Rates use current
velocities and are rejected above p=.05 rather than clipped. There is no
disjoint-pair multiplier and no random rotation at separated positions.
"""
from functools import lru_cache
import ctypes
from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree


G = 0.004498638185693768
KM_S_TO_PC_MYR = 1.022712165045695
CM2_G_TO_PC2_MSUN = 0.0002088420524663771
C = 306601.39378555055
HOST_MASS = 6.e11
HOST_SCALE = 10000.
RESONANCE_U = .02


def _load_c_backend():
    """Load an explicitly built local kernel; never invoke a compiler."""
    library_path = Path(__file__).with_name("direct_gravity.dylib")
    if not library_path.exists():
        return None
    library = ctypes.CDLL(str(library_path))
    array_type = np.ctypeslib.ndpointer(dtype=np.float64, flags="C_CONTIGUOUS")
    library.gravity_kernel.argtypes = [array_type, array_type, ctypes.c_size_t,
                                      ctypes.c_double, ctypes.c_double,
                                      array_type, ctypes.POINTER(ctypes.c_double)]
    library.gravity_kernel.restype = ctypes.c_int
    integer_array = np.ctypeslib.ndpointer(dtype=np.int64, flags="C_CONTIGUOUS")
    library.scatter_kernel.argtypes = [array_type, array_type, array_type,
                                      integer_array, array_type, ctypes.c_size_t,
                                      ctypes.c_double, ctypes.c_double,
                                      ctypes.c_double, ctypes.c_double, array_type,
                                      ctypes.POINTER(ctypes.c_int64)]
    library.scatter_kernel.restype = ctypes.c_int
    return library


_C_BACKEND = _load_c_backend()
GRAVITY_BACKEND = "c" if _C_BACKEND is not None else "numpy"


@lru_cache(maxsize=8)
def _pairs(count):
    return np.triu_indices(count, 1)


def _gravity_numpy(x, m, eps):
    """Independent NumPy pair reduction used as a small-N reference."""
    x = np.asarray(x, dtype=float)
    m = np.asarray(m, dtype=float)
    if x.shape != (len(m), 3) or eps < 0. or np.any(m <= 0.):
        raise ValueError("gravity needs positions (N,3), positive masses, eps>=0")
    count = len(m)
    acceleration = np.zeros_like(x)
    if count < 2:
        return acceleration, 0.
    i, j = _pairs(count)
    separation = x[j] - x[i]
    softened_r2 = np.einsum("ij,ij->i", separation, separation) + eps * eps
    if np.any(softened_r2 == 0.):
        raise ValueError("unsoftened coincident particles have singular gravity")
    inverse_r = 1. / np.sqrt(softened_r2)
    force_factor = G * inverse_r ** 3
    for axis in range(3):
        component = force_factor * separation[:, axis]
        acceleration[:, axis] = (np.bincount(i, weights=m[j] * component, minlength=count)
                                 - np.bincount(j, weights=m[i] * component, minlength=count))
    potential = -G * np.sum(m[i] * m[j] * inverse_r)
    return acceleration, float(potential)


def gravity(x, m, eps):
    """Return acceleration and pair potential, using an optional C backend."""
    if _C_BACKEND is None:
        return _gravity_numpy(x, m, eps)
    x = np.ascontiguousarray(x, dtype=np.float64)
    m = np.ascontiguousarray(m, dtype=np.float64)
    if x.shape != (len(m), 3) or eps < 0. or np.any(m <= 0.):
        raise ValueError("gravity needs positions (N,3), positive masses, eps>=0")
    acceleration = np.zeros_like(x)
    potential = ctypes.c_double()
    status = _C_BACKEND.gravity_kernel(x, m, len(m), eps, G,
                                       acceleration, ctypes.byref(potential))
    if status:
        raise ValueError("unsoftened coincident particles have singular gravity")
    return acceleration, potential.value


def host(x, enabled=True):
    """Return the fixed spherical Plummer host's acceleration and potential."""
    x = np.asarray(x, dtype=float)
    if x.ndim != 2 or x.shape[1] != 3:
        raise ValueError("host needs positions (N,3)")
    if not enabled:
        return np.zeros_like(x), np.zeros(len(x))
    inverse_r = 1. / np.sqrt(np.einsum("ij,ij->i", x, x) + HOST_SCALE ** 2)
    acceleration = -G * HOST_MASS * x * (inverse_r ** 3)[:, None]
    return acceleration, -G * HOST_MASS * inverse_r


def scatter(x, v, m, cold_mask, dt, h, rng, sigma_cm2_g=.3):
    """Apply equal-mass carrier collisions, returning signed numerical defects.

    ``delta_energy`` and ``delta_J`` sum the measured velocity-change defects
    of every accepted pair. No particle is moved or removed. A failed domain
    check raises, and the caller must reject that attempted simulation run.
    """
    return _scatter_impl(x, v, m, cold_mask, dt, h, rng, sigma_cm2_g, use_c=True)


def _scatter_python(x, v, m, cold_mask, dt, h, rng, sigma_cm2_g=.3):
    """Orthogonal sequential-loop reference for the same sampled candidates."""
    return _scatter_impl(x, v, m, cold_mask, dt, h, rng, sigma_cm2_g, use_c=False)


def _scatter_impl(x, v, m, cold_mask, dt, h, rng, sigma_cm2_g, use_c):
    x = np.asarray(x, dtype=float)
    m = np.asarray(m, dtype=float)
    cold_mask = np.asarray(cold_mask, dtype=bool)
    if (x.shape != (len(m), 3) or v.shape != x.shape or cold_mask.shape != m.shape
            or h <= 0. or dt < 0. or sigma_cm2_g < 0. or np.any(m <= 0.)):
        raise ValueError("invalid collision positions, velocities, masses, mask, dt, h, or cross section")
    report = dict(n=0, max_prob=0., delta_energy=0., delta_J=[0., 0., 0.],
                  max_x_resonance=0.)
    cold = np.flatnonzero(cold_mask)
    if len(cold) < 2 or dt == 0. or sigma_cm2_g == 0.:
        return report
    cold_mass = m[cold]
    if not np.allclose(cold_mass, cold_mass[0], rtol=1.e-12, atol=0.):
        raise ValueError("collision carriers must have equal masses")
    pairs = cKDTree(x[cold]).query_pairs(h, output_type="ndarray")
    if len(pairs) == 0:
        return report
    pairs = np.ascontiguousarray(cold[pairs[rng.permutation(len(pairs))]], dtype=np.int64)
    uniforms = rng.random(len(pairs))
    coefficient = (cold_mass[0] * sigma_cm2_g * CM2_G_TO_PC2_MSUN
                   * 3. / (4. * np.pi * h ** 3) * 4. * dt)
    if (use_c and _C_BACKEND is not None and v.dtype == np.float64
            and v.flags.c_contiguous):
        stats, hits = np.zeros(6), ctypes.c_int64()
        status = _C_BACKEND.scatter_kernel(np.ascontiguousarray(x), v,
                                           np.ascontiguousarray(m), pairs, uniforms,
                                           len(pairs), coefficient, h, RESONANCE_U,
                                           C, stats, ctypes.byref(hits))
        if status == 1:
            raise RuntimeError("sampled pair leaves declared below-resonance domain z<.1")
        if status == 2:
            raise RuntimeError("collision probability exceeds .05; reduce timestep")
        return dict(n=hits.value, max_prob=float(stats[0]), delta_energy=float(stats[1]),
                    delta_J=stats[2:5].tolist(), max_x_resonance=float(stats[5]))
    delta_J = np.zeros(3)
    for offset, (i, j) in enumerate(pairs):
        separation = x[i] - x[j]
        radius = float(np.linalg.norm(separation))
        # The direction of a coincident pair is undefined; this zero-measure
        # finite-particle configuration is excluded rather than given a torque.
        if radius == 0. or radius >= h:
            continue
        normal = separation / radius
        relative = v[i] - v[j]
        speed2 = float(np.dot(relative, relative))
        z = speed2 / (2. * RESONANCE_U * C) ** 2
        report["max_x_resonance"] = max(report["max_x_resonance"], z)
        if z >= .1:
            raise RuntimeError("sampled pair leaves declared below-resonance domain z<.1")
        incoming = -float(np.dot(relative, normal))
        if incoming <= 0.:
            continue
        cross_section_ratio = ((2. - z / (1. - z)) / 2.) ** 2 / (1. + RESONANCE_U ** 2 * z)
        probability = coefficient * cross_section_ratio * incoming
        report["max_prob"] = max(report["max_prob"], probability)
        if probability > .05:
            raise RuntimeError("collision probability exceeds .05; reduce timestep")
        if uniforms[offset] >= probability:
            continue
        before_i, before_j = v[i].copy(), v[j].copy()
        impulse_velocity = incoming * normal
        v[i] += impulse_velocity
        v[j] -= impulse_velocity
        report["delta_energy"] += float(.5 * m[i] * (
            np.dot(v[i], v[i]) + np.dot(v[j], v[j])
            - np.dot(before_i, before_i) - np.dot(before_j, before_j)))
        delta_J += (np.cross(x[i], m[i] * (v[i] - before_i))
                    + np.cross(x[j], m[j] * (v[j] - before_j)))
        report["n"] += 1
    report["delta_J"] = delta_J.tolist()
    return report
