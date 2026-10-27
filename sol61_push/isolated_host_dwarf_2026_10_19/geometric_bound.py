"""Finite saved-coordinate aperture bound; this performs no time evolution.

For each particle p, any radius-R sphere containing p lies inside its radius-2R
neighbourhood. A disjoint pair separated by more than 2R cannot both be in the
sphere. Thus |neighbours(p)| minus the size of any disjoint far-pair matching is
an upper bound. Taking the maximum over every p covers every nonempty sphere.

Coordinates and the inflated comparison length are converted from their stored
binary64 values to exact dyadic integers before distance comparisons. Inflating
2R by a positive tolerance only weakens the upper bound. No floating distance
query, optimizer, random sampling, or simulation module is used.
"""
import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import time

import numpy as np


def exact_grid(points, limit):
    """Represent finite binary64 inputs on one exact power-of-two grid."""
    points = np.asarray(points, dtype=np.float64)
    if points.ndim != 2 or points.shape[1] != 3 or not np.all(np.isfinite(points)):
        raise ValueError('finite (N,3) binary64 points required')
    values = [float(value).as_integer_ratio() for value in points.flat]
    limit_ratio = float(limit).as_integer_ratio()
    denominator = max([value[1] for value in values] + [limit_ratio[1]])
    # IEEE binary64 denominators are powers of two, so their maximum is an LCM.
    if denominator & (denominator - 1):
        raise AssertionError('dyadic denominator invariant failed')
    integers = [numerator * (denominator // divisor) for numerator, divisor in values]
    rows = [tuple(integers[first:first + 3]) for first in range(0, len(integers), 3)]
    limit_integer = limit_ratio[0] * (denominator // limit_ratio[1])
    return rows, denominator, limit_integer * limit_integer


def distance_squared(a, b):
    dx, dy, dz = a[0] - b[0], a[1] - b[1], a[2] - b[2]
    return dx * dx + dy * dy + dz * dz


def exact_neighbours(points, limit):
    integers, denominator, limit_squared = exact_grid(points, limit)
    count = len(integers)
    neighbours = [{index} for index in range(count)]
    visited = 0
    for first in range(count):
        for second in range(first + 1, count):
            if distance_squared(integers[first], integers[second]) <= limit_squared:
                neighbours[first].add(second)
                neighbours[second].add(first)
            visited += 1
    if visited != count * (count - 1) // 2:
        raise AssertionError('unordered pair coverage failed')
    return neighbours, integers, denominator, limit_squared, visited


def disjoint_far_matching(ids, neighbours):
    """Deterministic greedy matching; maximality/optimality is not required."""
    count = len(ids)
    far = np.array([[second not in neighbours[first] for second in ids]
                    for first in ids], dtype=bool)
    active = np.ones(count, dtype=bool)
    matching = []
    while True:
        degree = np.sum(far & active[None, :], axis=1)
        degree[~active] = 0
        first = int(np.argmax(degree))
        if degree[first] == 0:
            break
        choices = np.flatnonzero(far[first] & active)
        second = int(choices[np.argmax(degree[choices])])
        active[[first, second]] = False
        matching.append([ids[first], ids[second]])
    return matching


def aperture_bound(points, radius=300., tolerance=1.e-8):
    """Return a certificate covering every centre for the saved points."""
    if radius <= 0. or tolerance < 0.:
        raise ValueError('positive radius and nonnegative tolerance required')
    # The exact represented inflated value must be at least the exact 2R.
    limit = float(2. * radius + tolerance)
    if Fraction.from_float(limit) < 2 * Fraction.from_float(float(radius)):
        raise AssertionError('inflation failed to cover exact twice-radius')
    neighbours, integers, denominator, limit_squared, visited = exact_neighbours(points, limit)
    counts = [len(ids) for ids in neighbours]
    upper = 0
    certificates = []
    # Stable ordering only improves speed: every omitted matching is covered by
    # the recorded cardinality bound, and no particle centre is omitted.
    order = sorted(range(len(points)), key=lambda index: (-counts[index], index))
    for index in order:
        ids = sorted(neighbours[index])
        if len(ids) <= upper:
            matching = []
            skipped = True
        else:
            matching = disjoint_far_matching(ids, neighbours)
            skipped = False
        distinct = [endpoint for pair in matching for endpoint in pair]
        if len(distinct) != len(set(distinct)) or not set(distinct).issubset(neighbours[index]):
            raise AssertionError('matching disjointness/membership failed')
        for first, second in matching:
            if distance_squared(integers[first], integers[second]) <= limit_squared:
                raise AssertionError('non-far pair in certificate')
        local_upper = len(ids) - len(matching)
        if skipped:
            if local_upper > upper:
                raise AssertionError('invalid coverage skip')
        else:
            upper = max(upper, local_upper)
        certificates.append(dict(particle_index=index, neighbourhood_count=len(ids),
                                 matching=matching, local_upper=local_upper,
                                 cardinality_skip=skipped))
    if len(certificates) != len(points) or {row['particle_index'] for row in certificates} != set(range(len(points))):
        raise AssertionError('all-centre certificate coverage failed')
    return dict(radius_pc=radius, inflation_tolerance_pc=tolerance,
                represented_comparison_limit_pc=limit,
                comparison_limit_exact_ratio=list(limit.as_integer_ratio()),
                exact_grid_denominator=str(denominator),
                point_count=len(points), unordered_pairs_checked=visited,
                max_inflated_2R_neighbourhood_count=max(counts, default=0),
                upper_count=upper, matched_neighbourhoods=sum(not row['cardinality_skip'] for row in certificates),
                certificates=certificates)


def fractional_distance_squared(a, b):
    """Orthogonal rational route used to check arithmetic and match witnesses."""
    return sum((Fraction.from_float(float(a[axis])) - Fraction.from_float(float(b[axis]))) ** 2
               for axis in range(3))


def verify_fraction_witnesses(points, certificate):
    limit = Fraction(*certificate['comparison_limit_exact_ratio'])
    pairs = {tuple(pair) for row in certificate['certificates'] for pair in row['matching']}
    for first, second in pairs:
        if fractional_distance_squared(points[first], points[second]) <= limit ** 2:
            raise AssertionError('independent Fraction matching check failed')
    integers, denominator, limit_squared = exact_grid(points, float(limit))
    # Deterministic samples cover self, near and widely separated indices.
    samples = {(0, 0), (0, len(points) - 1)}
    for first in range(0, len(points), max(1, len(points) // 31)):
        samples.add((first, (37 * first + 11) % len(points)))
    for first, second in samples:
        exact = Fraction(distance_squared(integers[first], integers[second]), denominator ** 2)
        if exact != fractional_distance_squared(points[first], points[second]):
            raise AssertionError('dyadic and Fraction distance routes disagree')
    return dict(unique_far_pairs_fraction_checked=len(pairs), sampled_distances_checked=len(samples))


def brute_force_pairwise_diameter_limit(points, limit):
    """Exhaustive tiny-case orthogonal upper bound; not used on the snapshot."""
    limit_squared = Fraction.from_float(float(limit)) ** 2
    for size in range(len(points), 0, -1):
        for subset in itertools.combinations(range(len(points)), size):
            if all(fractional_distance_squared(points[a], points[b]) <= limit_squared
                   for a, b in itertools.combinations(subset, 2)):
                return size
    return 0


def handcrafted_checks():
    checks = []
    close = np.array([[0., 0., 0.], [100., 0., 0.], [200., 0., 0.]])
    first = aperture_bound(close)
    assert first['upper_count'] == 3
    assert not any(row['matching'] for row in first['certificates'])
    checks.append(dict(name='no-far-pair case admits all three particles', passed=True))
    # Two mutually distant triples, with one bridge at the origin. Any sphere
    # can contain one triple plus the bridge, but not both distant triples.
    separated = np.column_stack(([-500., -490., -480., 0., 480., 490., 500.], np.zeros(7), np.zeros(7)))
    second = aperture_bound(separated)
    exhaustive = brute_force_pairwise_diameter_limit(separated, second['represented_comparison_limit_pc'])
    assert second['upper_count'] == exhaustive == 4
    assert any(len(row['matching']) == 3 for row in second['certificates'])
    checks.append(dict(name='two distant triples plus bridge: bound four, exhaustive diameter check four', passed=True))
    boundary = np.array([[0., 0., 0.], [600.000000005, 0., 0.]])
    third = aperture_bound(boundary)
    assert third['upper_count'] == 2  # Intentionally weakened by positive tolerance.
    checks.append(dict(name='inflation conservatively retains a pair just beyond exactly 600pc', passed=True))
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    start = time.monotonic()
    checks = handcrafted_checks()
    snapshot_path = Path(args.snapshot)
    with np.load(snapshot_path, allow_pickle=False) as snapshot:
        x = np.array(snapshot['x'], dtype=np.float64, copy=True)
        mass = np.array(snapshot['m'], dtype=np.float64, copy=True)
        cold = np.array(snapshot['cold'], dtype=bool, copy=True)
    if x.shape != (len(mass), 3) or cold.shape != mass.shape or len(x) > 4096:
        raise ValueError('matching arrays and bounded N<=4096 required')
    points, cold_mass = x[cold], mass[cold]
    if len(points) == 0 or not np.all(cold_mass == cold_mass[0]) or cold_mass[0] <= 0.:
        raise ValueError('nonempty exactly equal positive cold particle masses required')
    result = aperture_bound(points)
    result['orthogonal_fraction_checks'] = verify_fraction_witnesses(points, result)
    threshold = (len(points) + 9) // 10
    # This is a reported finite comparison, not an assertion encoded into the
    # neighbour iterator. The runner succeeds even if the gate is not excluded.
    result.update(snapshot=str(snapshot_path), snapshot_sha256=hashlib.sha256(snapshot_path.read_bytes()).hexdigest(),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  assertion_tested='Every radius-300pc sphere contains at most the reported upper_count of cold particles in this saved coordinate set.',
                  ten_percent_inventory_threshold_count=threshold,
                  endpoint_ten_percent_aperture_excluded=result['upper_count'] < threshold,
                  equal_cold_particle_mass_Msun=float(cold_mass[0]),
                  upper_mass_Msun=float(result['upper_count'] * cold_mass[0]),
                  upper_fraction_of_original_cold_count=result['upper_count'] / len(points),
                  handcrafted_checks=checks,
                  interpretation='Exact dyadic arithmetic for saved coordinates, with conservative inflated distance cutoff; no continuum, trajectory, tidal-survival, or universal physical conclusion.',
                  software=dict(python=platform.python_version(), numpy=np.__version__),
                  wall_seconds=time.monotonic() - start,
                  observed_peak_RSS_native_units=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
                  RSS_units='bytes on Darwin, KiB on Linux')
    output = Path(args.output)
    output.write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    print(json.dumps({key: result[key] for key in ['point_count', 'unordered_pairs_checked', 'upper_count',
        'ten_percent_inventory_threshold_count', 'endpoint_ten_percent_aperture_excluded',
        'upper_mass_Msun', 'upper_fraction_of_original_cold_count', 'matched_neighbourhoods', 'wall_seconds']}))


if __name__ == '__main__':
    main()
