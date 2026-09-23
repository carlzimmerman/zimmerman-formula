"""Audit Qwen's radial claim with independent 3D null-collision transport."""
import json
import runpy
from pathlib import Path
import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
D0 = 4.0
EPS = 1 / 8
A = 2 * D0 / np.log((1 + EPS**2) / EPS**2)


def transport(n, seed, radial):
    rng = np.random.default_rng(seed)
    x = np.zeros((n, 3))
    u = np.zeros((n, 3)); u[:, 2] = 1.0
    t = np.zeros(n)
    collisions = np.zeros(n, dtype=int)
    active = np.arange(n)
    rate = A / EPS**2 if radial else 8.0
    mu2_sum = 0.0
    min_boundary_arg = 1.0
    max_radius2 = 0.0
    for iteration in range(100000):
        if not len(active):
            break
        pos, direction = x[active], u[active]
        projection = np.einsum('ij,ij->i', pos, direction)
        s = np.einsum('ij,ij->i', pos, pos)
        argument = projection**2 + 1 - s
        min_boundary_arg = min(min_boundary_arg, float(argument.min()))
        if argument.min() < -1e-10:
            raise ValueError('Invalid boundary geometry')
        boundary = -projection + np.sqrt(np.maximum(argument, 0))
        flight = rng.exponential(1 / rate, len(active))
        escape = flight >= boundary
        length = np.minimum(flight, boundary)
        if length.min() < -1e-10:
            raise ValueError('Negative physical flight')
        x[active] += direction * length[:, None]
        t[active] += length
        active = active[~escape]
        if not len(active):
            continue
        s = np.einsum('ij,ij->i', x[active], x[active])
        max_radius2 = max(max_radius2, float(s.max()))
        if s.max() > 1 + 1e-10:
            raise ValueError('Collision outside sphere')
        probability = EPS**2 / (EPS**2 + s) if radial else np.ones(len(active))
        ids = active[rng.random(len(active)) < probability]
        if not len(ids):
            continue
        # Rejection resamples angles only, never the already advanced flight.
        mu = np.empty(len(ids)); pending = np.arange(len(ids))
        while len(pending):
            trial = rng.uniform(-1, 1, len(pending))
            accepted = rng.random(len(pending)) < (1 + trial**2) / 2
            mu[pending[accepted]] = trial[accepted]
            pending = pending[~accepted]
        old = u[ids]
        perpendicular = rng.normal(size=(len(ids), 3))
        perpendicular -= np.einsum('ij,ij->i', perpendicular, old)[:, None] * old
        norm = np.linalg.norm(perpendicular, axis=1)
        if norm.min() <= 1e-12:
            raise ValueError('Degenerate perpendicular basis')
        perpendicular /= norm[:, None]
        u[ids] = mu[:, None] * old + np.sqrt(1 - mu**2)[:, None] * perpendicular
        collisions[ids] += 1
        mu2_sum += float(np.sum(mu**2))
        if collisions.max() >= 10000:
            raise RuntimeError('Physical collision cap exceeded')
    else:
        raise RuntimeError('Null-collision iteration cap exceeded')
    if len(active):
        raise RuntimeError('Unfinished paths')
    Z = np.einsum('ij,ij->i', x, u)
    D = t - Z
    geometry = bool(np.all(np.isfinite(D)) and np.all(D >= -1e-10)
                    and np.all(t >= 1 - 1e-10) and np.all(Z >= -1e-10)
                    and np.all(Z <= 1 + 1e-10)
                    and np.allclose(np.linalg.norm(x, axis=1), 1, atol=1e-10, rtol=0)
                    and np.allclose(np.linalg.norm(u, axis=1), 1, atol=1e-10, rtol=0))
    return D, Z, t, {'geometry': geometry, 'photons': n, 'seed': seed,
        'radial': radial, 'null_iterations': iteration, 'max_collisions': int(collisions.max()),
        'mean_collisions': float(collisions.mean()), 'actual_zero_collisions': int(np.sum(collisions == 0)),
        'expected_zero_fraction': float(np.exp(-A/EPS*np.arctan(1/EPS) if radial else -8)),
        'sample_mu2': mu2_sum / int(collisions.sum()),
        'min_boundary_argument': min_boundary_arg, 'max_collision_radius_squared': max_radius2}


def summarize(D, Z, T):
    B = D**2 - 7/5 * D0**2
    n = len(D)
    seD = np.std(D, ddof=1) / np.sqrt(n)
    seB = np.std(B, ddof=1) / np.sqrt(n)
    return {'n': n, 'mean_D': float(np.mean(D)), 'se_D': float(seD),
        'mean_T': float(np.mean(T)), 'mean_Z': float(np.mean(Z)),
        'var_D': float(np.var(D, ddof=1)), 'cv2_using_exact_mean': float(np.var(D, ddof=1) / D0**2),
        'mean_B': float(np.mean(B)), 'se_B': float(seB), 'B_z': float(np.mean(B) / seB),
        'mean_D_z': float((np.mean(D) - D0) / seD),
        'counterexample': bool(np.mean(B) < -6 * seB and abs(np.mean(D) - D0) <= 6 * seD)}


def main():
    checks = {}
    l, z, s, eps, amp = sp.symbols('l z s eps amp', real=True)
    b = sp.sqrt(eps**2 + s - z**2)
    tau = amp/b * (sp.atan((z+l)/b) - sp.atan(z/b))
    checks['optical_depth_derivative'] = sp.simplify(sp.diff(tau, l) - amp/(eps**2+s+2*z*l+l**2)) == 0
    checks['mean_calibration_algebra'] = bool(abs(A/2 * np.log((1+EPS**2)/EPS**2) - D0) < 1e-14)
    # Replay original fixed cases unchanged; they remain below the required significance.
    qwen = runpy.run_path(str(HERE/'qwen_candidate.py'))
    original = json.loads((HERE/'origin.json').read_text())['original_results']
    rows = []
    for mode, start in [('main', 9500000), ('positive', 9600000)]:
        paths = np.array([qwen['simulate_photon_path_radial'](A, EPS, start+i) for i in range(8000)])
        row = summarize(*paths.T); row.update(kind='original_replay', mode=mode, seed_start=start)
        rows.append(row)
        checks['replay_'+mode] = bool(abs(row['mean_B'] - original[mode]['measurements']['mean_B']) < 1e-12)
        checks['original_inconclusive_'+mode] = not row['counterexample']
    # Fresh finite audit, frozen n/seeds before any independent result is obtained.
    for radial, seed in [(True, 9810001), (True, 9820001), (False, 9830001)]:
        D, Z, T, diagnostics = transport(32000, seed, radial)
        row = summarize(D, Z, T); row.update(kind='independent_3D_null_collision', diagnostics=diagnostics)
        rows.append(row)
        checks['geometry_'+str(seed)] = diagnostics['geometry']
        checks['mean_'+str(seed)] = abs(row['mean_D_z']) <= 6
        checks['predicate_'+str(seed)] = row['counterexample'] if radial else not row['counterexample']
        # A separate angle-kernel diagnostic using a deliberately generous fixed tolerance.
        checks['thomson_mu2_'+str(seed)] = abs(diagnostics['sample_mu2'] - .4) < .003
    result = {'claim':'Fixed centrally concentrated profile test, not a universal theorem or novelty certificate',
        'parameters': {'d':D0, 'epsilon':EPS, 'A':float(A)}, 'checks':checks, 'rows':rows,
        'all_checks_pass':all(checks.values()), 'limitations':['Approximate Monte Carlo SEs',
        'Original Qwen scalar source broadly clamps negative geometry arguments',
        'Independent 3D method enforces small geometry tolerances', 'No measured JWST response tested']}
    (HERE/'certified/result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
