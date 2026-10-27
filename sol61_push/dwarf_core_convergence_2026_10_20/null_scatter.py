"""Exact frozen-position CTMC for the existing finite-h central elastic C22.

Each unordered cold pair with 0<r<h has jump rate
  m (sigma0/m) [3/(4*pi*h**3)] 4 ratio(|w|) max(-w.n, 0).
The jump is the same equal-mass central reflection as the historical driver.
Poisson thinning avoids visiting/drawing randomness for every spatial pair.
This integrates the continuous-time jump operator with x held fixed, rather
than the historical once-per-pair Bernoulli approximation. Their difference
is a collision-step time-discretization difference, not a new interaction.

Constants are copied explicitly from the original read-only
../isolated_host_dwarf_2026_10_19/dynamics.py (no import or compiled side effect).
No target profile, thermostat, inelastic cooling, particle deletion, or gravity
is implemented here. Finite spatial support and kinetic splitting still need
their own convergence checks. A failed call invalidates the attempted step;
velocities and RNG are not rolled back after a guard/cap exception.
"""
import numpy as np
from scipy.spatial import cKDTree


CM2_G_TO_PC2_MSUN = .0002088420524663771
C = 306601.39378555055
RESONANCE_U = .02


class NeighborProposal:
    """Uniform oriented edge of an inclusive radius-h graph, excluding self.

Counts require no explicit all-pairs table. The first index is weighted by
its degree, and its neighbor is chosen uniformly. Each unordered pair then
has probability 2/Q. Boundary/coincident candidates receive zero acceptance
in scatter(), retaining the strict 0<r<h physical support without a costly
full-neighbor enumeration just to remove exact boundary ties.
    """
    def __init__(self, positions, h):
        self.positions = np.ascontiguousarray(positions, dtype=float)
        if (self.positions.ndim != 2 or self.positions.shape[1] != 3
                or not np.all(np.isfinite(self.positions)) or not np.isfinite(h) or h <= 0.):
            raise ValueError('finite positions(N,3) and finite h>0 required')
        self.h = float(h)
        self.tree = cKDTree(self.positions)
        self.counts = np.asarray(self.tree.query_ball_point(
            self.positions, self.h, return_length=True), dtype=np.int64) - 1
        self.cumulative = np.cumsum(self.counts, dtype=np.int64)
        self.oriented_count = int(self.cumulative[-1]) if len(self.cumulative) else 0
        if np.any(self.counts < 0) or self.oriented_count < 0 or self.oriented_count % 2:
            raise RuntimeError('inconsistent symmetric neighbor graph')

    def draw(self, rng):
        if self.oriented_count == 0:
            raise ValueError('cannot sample an empty neighbor graph')
        ticket = int(rng.integers(self.oriented_count))
        i = int(np.searchsorted(self.cumulative, ticket, side='right'))
        previous = int(self.cumulative[i - 1]) if i else 0
        neighbors = self.tree.query_ball_point(self.positions[i], self.h, return_sorted=True)
        neighbors.remove(i)
        if len(neighbors) != self.counts[i]:
            raise RuntimeError('neighbor count/list mismatch')
        return i, int(neighbors[ticket - previous])


def scatter(x, v, m, cold_mask, dt, h, rng, sigma_cm2_g=.3,
            *, max_proposals=1000000, max_events=1000000):
    """Mutate float64 velocities by CTMC central elastic jumps over dt Myr.

The upper speed is 2*max|v_i-Vcold|, valid for every pair. After every accepted
jump it is enlarged when needed. Bulk momentum is conserved by equal-mass
collisions; the initial cold bulk therefore remains a valid reference frame.
The upper envelope is constant between accepted jumps. Exponential proposal
waiting times and null acceptance thus give the exact specified frozen-x
Markov generator, up to floating arithmetic and pseudorandom sampling.

max_prob is the largest upper per-pair hazard times dt, NOT a Bernoulli
probability. It is a diagnostic and is not clipped or constrained to .05.
Caps/domain/progress failures raise rather than truncate the physical step.
    """
    x, m, cold_mask = np.asarray(x, dtype=float), np.asarray(m, dtype=float), np.asarray(cold_mask, dtype=bool)
    if (m.ndim != 1 or x.shape != (m.size, 3)
            or not isinstance(v, np.ndarray) or v.shape != x.shape or v.dtype != np.float64
            or not v.flags.writeable or cold_mask.shape != m.shape
            or not np.all(np.isfinite(x)) or not np.all(np.isfinite(v))
            or not np.all(np.isfinite(m)) or np.any(m <= 0.)
            or not np.isscalar(dt) or not np.isfinite(dt) or dt < 0.
            or not np.isscalar(h) or not np.isfinite(h) or h <= 0.
            or not np.isscalar(sigma_cm2_g) or not np.isfinite(sigma_cm2_g) or sigma_cm2_g < 0.
            or not isinstance(max_proposals, (int, np.integer)) or max_proposals < 1
            or not isinstance(max_events, (int, np.integer)) or max_events < 1):
        raise ValueError('invalid collision arrays, positive equal carrier masses, dt>=0, h>0, cross section, or caps')
    report = dict(n=0, max_prob=0., delta_energy=0., delta_J=[0., 0., 0.],
                  max_x_resonance=0., proposals=0, elapsed_Myr=float(dt),
                  method='frozen-position-CTMC-thinning',
                  max_prob_definition='upper per-pair hazard * full dt; not a Bernoulli probability',
                  proposal_graph='inclusive radius h, no self; exact boundary/coincident candidates are null',
                  resonance_speed_upper_bound_z=0.)
    cold = np.flatnonzero(cold_mask)
    if len(cold) < 2 or dt == 0. or sigma_cm2_g == 0.:
        return report
    if not np.allclose(m[cold], m[cold[0]], rtol=1.e-12, atol=0.):
        raise ValueError('collision carriers must have equal masses')
    graph = NeighborProposal(x[cold], h)
    if graph.oriented_count == 0:
        return report
    bulk = np.mean(v[cold], axis=0)
    maximum_speed = float(np.max(np.linalg.norm(v[cold] - bulk, axis=1)))
    if maximum_speed == 0.:
        return report
    coefficient = float(m[cold[0]] * sigma_cm2_g * CM2_G_TO_PC2_MSUN * 3. / (np.pi * h ** 3))
    if not np.isfinite(coefficient) or coefficient <= 0.:
        raise RuntimeError('nonfinite or underflowed collision coefficient')
    elapsed, delta_J = 0., np.zeros(3)
    resonance_speed2 = (2. * RESONANCE_U * C) ** 2
    while elapsed < dt:
        # A small outward roundoff margin protects acceptance <=1. The bound
        # can stay conservative when the fastest particle subsequently slows.
        upper_incoming = np.nextafter(2. * maximum_speed * (1. + 2.e-14), np.inf)
        z_upper = upper_incoming ** 2 / resonance_speed2
        report['resonance_speed_upper_bound_z'] = max(report['resonance_speed_upper_bound_z'], z_upper)
        if not np.isfinite(z_upper) or z_upper >= .1:
            raise RuntimeError('cannot certify declared below-resonance domain z<.1 from the global speed bound')
        pair_envelope = coefficient * upper_incoming
        rate = .5 * graph.oriented_count * pair_envelope
        if not np.isfinite(rate) or rate <= 0.:
            raise RuntimeError('nonfinite or underflowed CTMC proposal rate')
        report['max_prob'] = max(report['max_prob'], pair_envelope * dt)
        wait = float(rng.exponential(1. / rate))
        if not np.isfinite(wait) or wait <= 0.:
            raise RuntimeError('nonpositive or nonfinite CTMC waiting time')
        if wait >= dt - elapsed:
            break
        advanced = elapsed + wait
        if advanced <= elapsed:
            raise RuntimeError('CTMC proposal failed to advance positive elapsed time')
        elapsed = advanced
        report['proposals'] += 1
        if report['proposals'] > max_proposals:
            raise RuntimeError('CTMC proposal cap exceeded; attempted step rejected')
        local_i, local_j = graph.draw(rng)
        i, j = cold[local_i], cold[local_j]
        separation = x[i] - x[j]
        radius = float(np.linalg.norm(separation))
        if radius == 0. or radius >= h:
            continue
        normal = separation / radius
        relative = v[i] - v[j]
        speed2 = float(relative @ relative)
        z = speed2 / resonance_speed2
        report['max_x_resonance'] = max(report['max_x_resonance'], z)
        if not np.isfinite(z) or z >= .1:
            raise RuntimeError('sampled pair leaves declared below-resonance domain z<.1')
        incoming = -float(relative @ normal)
        if incoming <= 0.:
            continue
        ratio = ((2. - z / (1. - z)) / 2.) ** 2 / (1. + RESONANCE_U ** 2 * z)
        acceptance = ratio * incoming / upper_incoming
        if not np.isfinite(acceptance) or acceptance > 1. or acceptance < 0.:
            raise RuntimeError('CTMC thinning envelope violated')
        if rng.random() >= acceptance:
            continue
        if report['n'] >= max_events:
            raise RuntimeError('CTMC accepted-event cap exceeded; attempted step rejected')
        before_i, before_j = v[i].copy(), v[j].copy()
        impulse = incoming * normal
        v[i] += impulse
        v[j] -= impulse
        report['delta_energy'] += float(.5 * m[i] * (
            v[i] @ v[i] + v[j] @ v[j] - before_i @ before_i - before_j @ before_j))
        delta_J += (np.cross(x[i], m[i] * (v[i] - before_i))
                    + np.cross(x[j], m[j] * (v[j] - before_j)))
        report['n'] += 1
        maximum_speed = max(maximum_speed, float(np.linalg.norm(v[i] - bulk)), float(np.linalg.norm(v[j] - bulk)))
    report['delta_J'] = delta_J.tolist()
    return report
