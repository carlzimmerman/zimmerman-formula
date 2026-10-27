"""Frozen-snapshot finite-h central-elastic-C22 hazards and reciprocal receipts.

No dynamics, profile fitting, or random sampling is performed. All unordered
cold pairs within the largest support are enumerated once, then each requested
strict 0<r<h kernel is evaluated. The original carrier constants and central
reflection are copied explicitly; no old driver or compiled library is imported.
Energy receipts are kinetic energy in the fixed supplied bulk frame, including
streaming/rotation, not temperature after subtracting local mean velocity.
Angular momentum is about the supplied fixed centre in that same bulk frame.
Positions do not move during a collision, so there is no instantaneous mass
flux or gravitational-potential-energy change. Across-aperture flux here means
collision-mediated exchange between particles on opposite sides of a sphere.
"""
import os
for _name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[_name] = '1'
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time

import numpy as np
from scipy.spatial import cKDTree


CM2_G_TO_PC2_MSUN = .0002088420524663771
C = 306601.39378555055
RESONANCE_U = .02


def _stats(values):
    values = np.asarray(values)
    if not len(values):
        return dict(mean=None, median=None, minimum=None, maximum=None, zero_fraction=None)
    return dict(mean=float(np.mean(values)), median=float(np.median(values)),
                minimum=float(np.min(values)), maximum=float(np.max(values)),
                zero_fraction=float(np.mean(values == 0.)))


def audit_snapshot(x, v, m, cold, centre, bulk, supports=(100., 50., 25., 12.5, 6.25),
                   apertures=(50., 100., 300.),
                   radial_edges=(0., 25., 50., 100., 200., 300., 600., 1000., 2000.),
                   sigma_cm2_g=.3, batch_size=32768, max_pairs=5000000):
    """Return JSON-safe summary and full cold-particle hazard/receipt arrays.

Each particle hazard counts its participation; its sum is twice the total
unordered-pair rate. Spatial pair counts include outgoing pairs, whereas active
counts require incoming relative motion. Inverse rate participation is a weight
concentration diagnostic, not an independently sampled statistical sample size.
    """
    x, v, m = (np.asarray(a, dtype=float) for a in (x, v, m))
    cold = np.asarray(cold, dtype=bool)
    centre, bulk, supports, apertures, edges = (np.asarray(a, dtype=float) for a in
        (centre, bulk, supports, apertures, radial_edges))
    if (m.ndim != 1 or x.shape != (m.size, 3) or v.shape != x.shape or cold.shape != m.shape
            or centre.shape != (3,) or bulk.shape != (3,) or np.any(m <= 0.)
            or supports.ndim != 1 or len(supports) == 0 or np.any(supports <= 0.)
            or apertures.ndim != 1 or np.any(apertures <= 0.)
            or edges.ndim != 1 or len(edges) < 2 or edges[0] != 0. or np.any(np.diff(edges) <= 0.)
            or not all(np.all(np.isfinite(a)) for a in (x, v, m, centre, bulk, supports, apertures, edges))
            or not np.isfinite(sigma_cm2_g) or sigma_cm2_g < 0.
            or not isinstance(batch_size, int) or batch_size < 1
            or not isinstance(max_pairs, int) or max_pairs < 1):
        raise ValueError('invalid finite snapshot, frame, supports, apertures, radial edges, cross section, or resource bounds')
    ids = np.flatnonzero(cold)
    xc, wc, mc = x[ids] - centre, v[ids] - bulk, m[ids]
    if len(ids) and not np.all(mc == mc[0]):
        raise ValueError('the audited central-reflection kernel requires exactly equal carrier masses')
    n, ns = len(ids), len(supports)
    particle_rate = np.zeros((ns, n))
    neighbors = np.zeros((ns, n), dtype=np.int64)
    energy_receipt = np.zeros((ns, n))
    J_receipt = np.zeros((ns, n, 3))
    radius = np.linalg.norm(xc, axis=1)
    tree = cKDTree(xc)
    count_inclusive = int(tree.count_neighbors(tree, float(max(supports))))
    pair_bound = (count_inclusive - n) // 2
    if pair_bound > max_pairs:
        raise RuntimeError('candidate pair resource cap exceeded; no partial support audit returned')
    pairs = tree.query_pairs(float(max(supports)), output_type='ndarray')
    if len(pairs) != pair_bound:
        raise RuntimeError('independent tree count and pair enumeration disagree')
    rows = []
    for h in supports:
        rows.append(dict(h_pc=float(h), strict_neighbor_pairs=0, active_incoming_pairs=0,
            total_pair_rate_per_Myr=0., sum_pair_rate_squared=0., maximum_pair_rate_per_Myr=0.,
            pair_energy_closure_rate=0., pair_abs_energy_receipt_rate=0.,
            pair_vector_J_closure_rate=np.zeros(3), pair_abs_vector_J_receipt_rate=0.,
            aperture_exchange=[dict(radius_pc=float(r), crossing_neighbor_pairs=0, active_crossing_pairs=0,
                crossing_pair_rate_per_Myr=0., energy_into_inside_Msun_pc2_Myr3=0.,
                energy_into_outside_Msun_pc2_Myr3=0., energy_abs_receipt_scale_Msun_pc2_Myr3=0.,
                J_into_inside_Msun_pc2_Myr2=np.zeros(3), J_into_outside_Msun_pc2_Myr2=np.zeros(3)) for r in apertures]))
    max_z = 0.
    coefficient = 0. if n == 0 else mc[0] * sigma_cm2_g * CM2_G_TO_PC2_MSUN * 3. / np.pi
    for start in range(0, len(pairs), batch_size):
        block = pairs[start:start + batch_size]
        i, j = block[:, 0], block[:, 1]
        separation = xc[i] - xc[j]
        distance = np.linalg.norm(separation, axis=1)
        strict = (distance > 0.) & (distance < max(supports))
        i, j, separation, distance = i[strict], j[strict], separation[strict], distance[strict]
        if not len(i):
            continue
        normal = separation / distance[:, None]
        relative = wc[i] - wc[j]
        z = np.einsum('ij,ij->i', relative, relative) / (2 * RESONANCE_U * C) ** 2
        max_z = max(max_z, float(max(z)))
        if np.any(z >= .1) or not np.all(np.isfinite(z)):
            raise RuntimeError('candidate pair leaves declared below-resonance domain z<.1')
        incoming = np.maximum(-np.einsum('ij,ij->i', relative, normal), 0.)
        ratio = ((2. - z / (1. - z)) / 2.) ** 2 / (1. + RESONANCE_U ** 2 * z)
        impulse = incoming[:, None] * normal
        kinetic_i = mc[0] * (np.einsum('ij,ij->i', wc[i], impulse) + .5 * incoming ** 2)
        kinetic_j = mc[0] * (-np.einsum('ij,ij->i', wc[j], impulse) + .5 * incoming ** 2)
        spin_i = np.cross(xc[i], mc[0] * impulse)
        spin_j = np.cross(xc[j], -mc[0] * impulse)
        for k, h in enumerate(supports):
            keep = distance < h
            a, b = i[keep], j[keep]
            rate = coefficient / h ** 3 * ratio[keep] * incoming[keep]
            ei, ej, Ji, Jj = kinetic_i[keep], kinetic_j[keep], spin_i[keep], spin_j[keep]
            row = rows[k]
            row['strict_neighbor_pairs'] += int(np.count_nonzero(keep))
            row['active_incoming_pairs'] += int(np.count_nonzero(rate > 0.))
            row['total_pair_rate_per_Myr'] += float(rate.sum())
            row['sum_pair_rate_squared'] += float(rate @ rate)
            row['maximum_pair_rate_per_Myr'] = max(row['maximum_pair_rate_per_Myr'], float(max(rate)) if len(rate) else 0.)
            row['pair_energy_closure_rate'] += float(rate @ (ei + ej))
            row['pair_abs_energy_receipt_rate'] += float(rate @ (abs(ei) + abs(ej)))
            row['pair_vector_J_closure_rate'] += np.sum(rate[:, None] * (Ji + Jj), axis=0)
            row['pair_abs_vector_J_receipt_rate'] += float(rate @ (np.linalg.norm(Ji, axis=1) + np.linalg.norm(Jj, axis=1)))
            neighbors[k] += np.bincount(a, minlength=n) + np.bincount(b, minlength=n)
            particle_rate[k] += np.bincount(a, weights=rate, minlength=n) + np.bincount(b, weights=rate, minlength=n)
            energy_receipt[k] += np.bincount(a, weights=rate * ei, minlength=n) + np.bincount(b, weights=rate * ej, minlength=n)
            for axis in range(3):
                J_receipt[k, :, axis] += (np.bincount(a, weights=rate * Ji[:, axis], minlength=n)
                                          + np.bincount(b, weights=rate * Jj[:, axis], minlength=n))
            for flux in row['aperture_exchange']:
                inside_i, inside_j = radius[a] <= flux['radius_pc'], radius[b] <= flux['radius_pc']
                crossing = inside_i != inside_j
                cr = rate[crossing]
                first_inside = inside_i[crossing]
                first_J = first_inside[:, None]
                fi, fj, si, sj = ei[crossing], ej[crossing], Ji[crossing], Jj[crossing]
                flux['crossing_neighbor_pairs'] += int(np.count_nonzero(crossing))
                flux['active_crossing_pairs'] += int(np.count_nonzero(cr > 0.))
                flux['crossing_pair_rate_per_Myr'] += float(cr.sum())
                flux['energy_into_inside_Msun_pc2_Myr3'] += float(cr @ np.where(first_inside, fi, fj))
                flux['energy_into_outside_Msun_pc2_Myr3'] += float(cr @ np.where(first_inside, fj, fi))
                flux['energy_abs_receipt_scale_Msun_pc2_Myr3'] += float(cr @ (abs(fi) + abs(fj)))
                flux['J_into_inside_Msun_pc2_Myr2'] += np.sum(cr[:, None] * np.where(first_J, si, sj), axis=0)
                flux['J_into_outside_Msun_pc2_Myr2'] += np.sum(cr[:, None] * np.where(first_J, sj, si), axis=0)
    bin_indices = np.searchsorted(edges, radius, side='right') - 1
    for k, row in enumerate(rows):
        total = row['total_pair_rate_per_Myr']
        row['particle_hazard_sum_per_Myr'] = float(particle_rate[k].sum())
        row['pair_to_particle_rate_relative_defect'] = abs(row['particle_hazard_sum_per_Myr'] - 2 * total) / (2 * total) if total else 0.
        row['inverse_rate_participation'] = total ** 2 / row['sum_pair_rate_squared'] if row['sum_pair_rate_squared'] else 0.
        row['relative_pair_energy_closure'] = abs(row['pair_energy_closure_rate']) / row['pair_abs_energy_receipt_rate'] if row['pair_abs_energy_receipt_rate'] else 0.
        row['relative_pair_vector_J_closure'] = float(np.linalg.norm(row['pair_vector_J_closure_rate'])) / row['pair_abs_vector_J_receipt_rate'] if row['pair_abs_vector_J_receipt_rate'] else 0.
        row['pair_vector_J_closure_rate'] = row['pair_vector_J_closure_rate'].tolist()
        row['neighbor_count'] = _stats(neighbors[k])
        row['particle_hazard_per_Myr'] = _stats(particle_rate[k])
        row['radial'] = []
        for shell in range(len(edges)):
            selected = bin_indices == shell
            row['radial'].append(dict(lower_pc=float(edges[shell]),
                upper_pc=float(edges[shell + 1]) if shell + 1 < len(edges) else None,
                count=int(selected.sum()), neighbor_count=_stats(neighbors[k, selected]),
                particle_hazard_per_Myr=_stats(particle_rate[k, selected]),
                summed_particle_hazard_per_Myr=float(particle_rate[k, selected].sum())))
        for flux in row['aperture_exchange']:
            flux['J_into_inside_Msun_pc2_Myr2'] = flux['J_into_inside_Msun_pc2_Myr2'].tolist()
            flux['J_into_outside_Msun_pc2_Myr2'] = flux['J_into_outside_Msun_pc2_Myr2'].tolist()
        if max(row['relative_pair_energy_closure'], row['relative_pair_vector_J_closure'], row['pair_to_particle_rate_relative_defect']) > 1.e-12:
            raise RuntimeError('reciprocal pair/rate closure check failed')
    summary = dict(kind='all-pairs deterministic frozen-snapshot C22 hazard audit',
        units='pc, Msun, Myr; pair and particle rates per Myr', cold_count=n,
        carrier_particle_mass_Msun=float(mc[0]) if n else None, sigma0_cm2_g=float(sigma_cm2_g),
        centre_pc=centre.tolist(), fixed_bulk_pc_Myr=bulk.tolist(),
        inclusive_largest_support_candidate_pairs=int(len(pairs)), max_sampled_z=max_z,
        supports=rows, nonclaims=[
            'No time evolution, repeated scattering, gravity step, profile convergence or h->0 extrapolation',
            'Kinetic exchange includes streaming/rotation; not locally thermal heat flux or radiative cooling',
            'No particle or mass crosses an aperture during the instantaneous collision operation',
            'Pair participation and neighboring particles are correlated; inverse rate participation is not an error bar',
            'One finite prepared snapshot; spatial noise and physical history remain unseparated'])
    arrays = dict(cold_particle_indices=ids, radius_pc=radius, supports_pc=supports,
        particle_hazard_per_Myr=particle_rate, neighbor_count=neighbors,
        expected_energy_receipt_Msun_pc2_Myr3=energy_receipt,
        expected_J_receipt_Msun_pc2_Myr2=J_receipt)
    return summary, arrays


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', required=True)
    parser.add_argument('--metadata', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    start = time.monotonic()
    source, metadata = Path(args.snapshot), Path(args.metadata)
    data = np.load(source)
    record = json.loads(metadata.read_text())
    final = record['snapshots'][-1]
    summary, arrays = audit_snapshot(*(data[k] for k in ('x', 'v', 'm', 'cold')),
                                     np.asarray(final['centre']), np.asarray(final['bulk']))
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    array_path = target.with_suffix('.npz')
    np.savez_compressed(array_path, **arrays)
    summary.update(snapshot_path=str(source), snapshot_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        metadata_path=str(metadata), metadata_sha256=hashlib.sha256(metadata.read_bytes()).hexdigest(),
        snapshot_time_Myr=float(final['time_Myr']), per_particle_arrays_path=str(array_path),
        wall_seconds=time.monotonic() - start,
        observed_peak_RSS_bytes=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
    target.write_text(json.dumps(summary, indent=2, allow_nan=False) + '\n')
    print(json.dumps(dict(output=str(target), cold_count=summary['cold_count'],
        candidates=summary['inclusive_largest_support_candidate_pairs'], seconds=summary['wall_seconds'],
        supports=[dict(h_pc=r['h_pc'], pairs=r['strict_neighbor_pairs'],
            rate=r['total_pair_rate_per_Myr'], mean_neighbors=r['neighbor_count']['mean']) for r in summary['supports']]), indent=2))


if __name__ == '__main__':
    main()
