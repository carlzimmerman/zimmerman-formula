"""Independent exact Weyl integration and tree-gauge photon arithmetic.

No author code is imported. The supplied author result is used only at the end
as a comparison table. Bounds and interpretation are in CONTRACT.json.
"""
import json
import sys
from collections import defaultdict, deque
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, factorial
from pathlib import Path

BASE = Path(__file__).parent
INPUTS = json.loads((BASE / 'INPUTS.json').read_text())
CHECKS = 0


def check(value):
    global CHECKS
    if not value:
        raise AssertionError('independent check failed')
    CHECKS += 1


def laurent_mul(a, b):
    out = defaultdict(int)
    for (x, y), c in a.items():
        for (u, v), d in b.items():
            out[x + u, y + v] += c * d
    return {m: c for m, c in out.items() if c}


def invert(matrix):
    size = len(matrix)
    aug = [[Q(x) for x in row] + [Q(i == j) for j in range(size)]
           for i, row in enumerate(matrix)]
    for j in range(size):
        pivot = next(i for i in range(j, size) if aug[i][j])
        aug[j], aug[pivot] = aug[pivot], aug[j]
        scale = aug[j][j]
        aug[j] = [x / scale for x in aug[j]]
        for i in range(size):
            if i != j and aug[i][j]:
                scale = aug[i][j]
                aug[i] = [a - scale * b for a, b in zip(aug[i], aug[j])]
    return [row[size:] for row in aug]


def poly_mul(a, b, degree=9):
    return [sum(a[j] * b[i-j] for j in range(i+1))
            for i in range(degree+1)]


def poly_power(a, power):
    out = [Q(1)] + [Q(0)] * 9
    for _ in range(power):
        out = poly_mul(out, a)
    return out


def main():
    # Weyl integration for SU(3), z=(x,y,1/(xy)). The factor is |Delta|^2/3!.
    eigen = [(1, 0), (0, 1), (-1, -1)]
    tr = {m: 1 for m in eigen}
    anti = {(-x, -y): 1 for x, y in eigen}
    density = {(0, 0): 1}
    for a in eigen:
        for b in eigen:
            if a != b:
                density = laurent_mul(density, {(0, 0): 1, (a[0]-b[0], a[1]-b[1]): -1})
    check(density[(0, 0)] == 6)
    powers = [[{(0, 0): 1}], [{(0, 0): 1}]]
    for side, factor in enumerate((tr, anti)):
        for _ in range(10):
            powers[side].append(laurent_mul(powers[side][-1], factor))
    moments = {}
    for k in range(11):
        for l in range(11-k):
            integrand = laurent_mul(powers[0][k], powers[1][l])
            value = Q(sum(c * integrand.get((-x, -y), 0)
                          for (x, y), c in density.items()), 6)
            check(value.denominator == 1)
            moments[k, l] = value
    check(moments[3, 0] == 1)
    check(moments[1, 1] == 1)
    c0, numerator = [Q(0)] * 10, [Q(0)] * 10
    for (k, l), value in moments.items():
        if k+l <= 9:
            c0[k+l] += value / (factorial(k)*factorial(l)*6**(k+l))
        # Numerator integral Tr Udagger exp(action)/3. Swap k,l symmetry
        # supplies the same moments without differentiating author series.
        if l >= 1 and k+l-1 <= 9:
            numerator[k+l-1] += value / (3*factorial(k)*factorial(l-1)*6**(k+l-1))
    v = [Q(0)] * 10
    for i in range(10):
        v[i] = numerator[i] - sum(c0[j]*v[i-j] for j in range(1, i+1))
    collective = [720*x for x in poly_power(v, 6)]
    z = poly_mul(poly_power(c0, 80), [1+collective[0]]+collective[1:])
    logz = [Q(0)] * 10
    # z'=z*(log z)' is independent of the author's log(1+x) routine.
    for i in range(1, 10):
        logz[i] = z[i] - sum(Q(j, i)*logz[j]*z[i-j] for j in range(1, i))
    beta = Q(INPUTS['beta'])
    endpoint = sum(c*beta**i for i, c in enumerate(z))
    error = (80*beta)**10 / factorial(10) / (1-80*beta)
    check(endpoint >= 1)
    check(error < Q(40, 1889568)*beta**6/1000)

    # K1 vertices and links are bitstrings. Square rows come from explicit
    # vertex cycles, independently of the author's recursive face generator.
    vertices = list(product((0, 1), repeat=5))
    edges = [(x, x[:j]+(1,)+x[j+1:]) for x in vertices for j in range(5) if x[j] == 0]
    edge_id = {frozenset(e): i for i, e in enumerate(edges)}
    adjacency = {x: [] for x in vertices}
    for i, (x, y) in enumerate(edges):
        adjacency[x].append((y, i))
        adjacency[y].append((x, i))
    seen, tree, queue = {vertices[0]}, set(), deque([vertices[0]])
    while queue:
        x = queue.popleft()
        for y, edge in adjacency[x]:
            if y not in seen:
                seen.add(y)
                tree.add(edge)
                queue.append(y)
    check(len(tree) == 31)
    remaining = [i for i in range(80) if i not in tree]
    rem_id = {edge: i for i, edge in enumerate(remaining)}
    rows = []
    phase_checks = 0
    for j, k in combinations(range(5), 2):
        for x in vertices:
            if x[j] or x[k]:
                continue
            y = x[:j]+(1,)+x[j+1:]
            zeta = y[:k]+(1,)+y[k+1:]
            t = x[:k]+(1,)+x[k+1:]
            cycle, row, sign = (x, y, zeta, t, x), {}, 1
            for a, b in zip(cycle, cycle[1:]):
                axis = next(i for i in range(5) if a[i] != b[i])
                forward = a[axis] < b[axis]
                low = a if forward else b
                sign *= (1 if forward else -1)*(-1)**sum(low[:axis])
                edge = edge_id[frozenset((a, b))]
                if edge in rem_id:
                    row[rem_id[edge]] = 1 if forward else -1
            check(sign == -1)
            phase_checks += 1
            rows.append(row)
    check(len(rows) == 80)
    gaussian = []
    for special_weight in (1, 2):
        weights = [special_weight] + [1]*79
        gram = [[Q(0) for _ in remaining] for _ in remaining]
        for w, row in zip(weights, rows):
            for i, a in row.items():
                for j, b in row.items():
                    gram[i][j] += w*a*b
        cov = invert(gram)
        variances = [sum(a*b*cov[i][j] for i, a in row.items() for j, b in row.items())
                     for row in rows]
        check(sum(w*v for w, v in zip(weights, variances)) == 49)
        check(all(v > 0 for v in variances))
        if special_weight == 1:
            check(set(variances) == {Q(49, 80)})
        gaussian.append({'first_plaquette_weight': special_weight,
                         'weighted_trace': '49', 'min_variance': str(min(variances)),
                         'max_variance': str(max(variances))})
    geometry = []
    for n in (1, 2, 3):
        counts = [comb(5, k)*n**k*((n+1)**(5-k)-(n-1)**(5-k)) for k in range(5)]
        check(sum((-1)**k*c for k, c in enumerate(counts)) == 2)
        geometry.append({'n': n, 'counts_from_formula': counts,
                         'd1_rank_from_topology': counts[1]-counts[0]+1,
                         'charge_coefficient': str(Q(counts[1]-counts[0]+1, 9))})
    # Comparison is deliberately after all independent arithmetic.
    author = json.loads(Path(INPUTS['author_result']).read_text())
    for item in author['su3_singlet_moments']:
        check(moments[item['k'], item['l']] == item['multiplicity'])
    for name, independent in [('c0_beta_coefficients', c0),
                              ('fundamental_character_coefficient', v),
                              ('K1_Z_beta_coefficients_through9', z),
                              ('K1_logZ_beta_coefficients_through9', logz)]:
        check([Q(x) for x in author['series'][name]] == independent)
    check(Q(author['finite_endpoint']['P9_minus1']) == endpoint-1)
    check(Q(author['finite_endpoint']['absolute_Z_remainder_upper']) == error)
    result = {'status': 'completed', 'checks': CHECKS,
              'method': 'Exact Laurent Weyl constant terms and exact rational tree-gauge inversion; no author imports',
              'moment_count': len(moments), 'moments': {str(k): str(v) for k, v in moments.items()},
              'K1_logZ_through9': list(map(str, logz)),
              'P9_minus1': str(endpoint-1), 'absolute_error_bound': str(error),
              'gaussian': gaussian, 'square_phase_checks': phase_checks,
              'geometry_formula_values': geometry,
              'limitations': INPUTS['non_claims']}
    Path(sys.argv[1]).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': 'completed', 'checks': CHECKS, 'moments': len(moments),
                      'exact_gaussian_weight_cases': len(gaussian)}))


if __name__ == '__main__':
    main()
