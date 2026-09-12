#!/usr/bin/env python3
"""Bounded fixed-action exterior principal audit; no background refitting.

The numerical assertion concerns selected archived homogeneous jets. The
localization implication separately requires convergence of the complete
principal jet, including the covariant chi Hessian, on a regular on-shell
constraint-compatible background. Positive speed is NOT a stability pass.
"""
import argparse
from decimal import Decimal, localcontext
from functools import lru_cache
import json
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
REPAIR = HERE.parents[1]
sys.path.insert(0, str(REPAIR / 'finite_gradient_metric_2026/cubic'))
from cubic_debraiding import corrected
from radiation_probe import ProbeBackground
from transfer_evolve import mode_system

SOURCE = REPAIR / 'cosmological_bridge_2026/radiation_002/result.json'
INDICES = (0, 1, 46, 92, 138, 184)


def homogeneous(j, Q, H, qdot, clock_rate, gamma, M2=1.):
    """Independent Y=0 contraction including full cubic Hessian/metric terms."""
    p, r, W, w = (j[key] for key in ('PX', 'PXX', 'W', 'WY'))
    if not np.all(np.isfinite([p, r, W, w, Q, H, qdot, clock_rate, gamma, M2])):
        raise ValueError('nonfinite principal input')
    if clock_rate <= 0 or M2 <= 0:
        raise ValueError('positive clock norm and Planck coefficient required')
    F = W - 2*Q*Q*w
    if F == 0:
        raise ValueError('singular elliptic clock block')
    K = 2*p + 4*Q*Q*r - 12*gamma*H*Q + 6*gamma*gamma*Q**4/M2
    G = 2*p - 2*clock_rate*w*W/F - 4*gamma*(qdot+2*H*Q) - 2*gamma*gamma*Q**4/M2
    if K == 0:
        raise ValueError('degenerate scalar kinetic coefficient')
    speed2 = G/K
    return dict(F=F, K=K, G=G, B=0., quarter_discriminant=K*G,
                speed_squared=speed2,
                imaginary_speed=np.sqrt(-speed2) if speed2 < 0 else 0.,
                real_speed=np.sqrt(speed2) if speed2 >= 0 else 0.,
                negative_discriminant=bool(K*G < 0),
                healthy_positive_kinetic=bool(K > 0),
                interpretation='negative discriminant is an obstruction; nonnegative is not a full hyperbolicity/stability certificate')


def decimal_control(j, Q, H, qdot, clock_rate, gamma, M2=1.):
    """80-digit arithmetic of the SAME decimalized input jets, not new accuracy."""
    with localcontext() as ctx:
        ctx.prec = 80
        p, r, W, w, q, h, qd, s, g, m = map(
            lambda value: Decimal(str(value)),
            [j['PX'], j['PXX'], j['W'], j['WY'], Q, H, qdot, clock_rate, gamma, M2])
        F = W-2*q*q*w
        K = 2*p+4*q*q*r-12*g*h*q+6*g*g*q**4/m
        G = 2*p-2*s*w*W/F-4*g*(qd+2*h*q)-2*g*g*q**4/m
        return dict(F=str(F), K=str(K), G=str(G), speed_squared=str(G/K),
                    scope='80-digit evaluation of rounded input jets; not an interval or ODE-error certificate')


@lru_cache(maxsize=1)
def background():
    return ProbeBackground(5.)


def evaluate(index, extended=False):
    archived = json.loads(SOURCE.read_text())['samples'][index]
    state = [archived[key] for key in ('a', 'H', 'q', 'tau', 'rho_baryon', 'rho_radiation')]
    bg = background()
    values, matrix, checks, margin = bg.evaluate(state, extended=extended)
    Q, H, qdot, s = (values[key] for key in ('q', 'H', 'qd', 'sbar'))
    raw = bg.model.jets(archived['tau'], Q*Q, 0.)
    j = {key: float(raw[name]) for key, name in
         dict(PX='P_X', PXX='P_XX', W='W', WY='W_Y', WYY='W_YY').items()}
    independent = homogeneous(j, Q, H, qdot, s, values['gamma'])
    hessian = np.diag([qdot, -H*Q, -H*Q, -H*Q])
    tensor = corrected(j, Q, s, 0., 0., gamma=values['gamma'], hessian_cov=hessian)
    differences = {key: abs(independent[key]-tensor[other]) for key, other in
                   dict(F='F', K='kinetic', G='gradient', quarter_discriminant='quarter_finite_gamma').items()}
    if max(differences.values()) > 1e-11*(1+abs(independent['quarter_discriminant'])):
        raise AssertionError('independent homogeneous contraction disagrees with covariant tensor implementation')
    row = dict(index=index, a=archived['a'], tau=archived['tau'], H=H, physical_Q=Q,
               reference_qbar=bg.model.background(archived['tau'])['q'], Qdot=qdot,
               clock_rate=s, gamma=values['gamma'], M2=1., Y=0., jets=j,
               hessian_cov=hessian.tolist(), principal=independent,
               decimal_control=decimal_control(j, Q, H, qdot, s, values['gamma']),
               independent_vs_tensor_absolute_errors=differences,
               background_constraint_residuals=checks[:2].tolist(),
               background_matrix_condition=float(np.linalg.cond(matrix)),
               scalar_charge=float(archived['a']**3*checks[2]), domain_margin=margin)
    return row, values


def constrained_modes(values, target_speed):
    """Independent existing six-state constrained transfer operator; no evolution."""
    rows = []
    for k in (1e2, 1e3, 1e4, 1e5):
        operator, matrix, *_ = mode_system(values, k)
        physical_k = k/values['a']
        scaling = np.array([1., physical_k, 1., physical_k, 1., physical_k])
        balanced = operator*(scaling[None, :]/scaling[:, None])/physical_k
        eig, vectors = np.linalg.eig(balanced)
        residual = max(np.linalg.norm(balanced@vectors[:, i]-eig[i]*vectors[:, i]) /
                       ((1+np.linalg.norm(balanced)+abs(eig[i]))*np.linalg.norm(vectors[:, i]))
                       for i in range(6))
        growth = float(max(eig.real))
        rows.append(dict(comoving_k=k, physical_k=physical_k,
                         eigenvalues_over_physical_k=[dict(real=float(x.real), imag=float(x.imag)) for x in eig],
                         largest_scaled_growth=growth,
                         distance_to_independent_imaginary_speed=abs(growth-target_speed),
                         normalized_eigen_residual=float(residual),
                         unscaled_constraint_solve_condition=float(np.linalg.cond(matrix))))
    return rows


def run():
    rows = [evaluate(index)[0] for index in INDICES]
    first, values = evaluate(0, extended=True)
    modes = constrained_modes(values, first['principal']['imaginary_speed'])
    if max(row['normalized_eigen_residual'] for row in modes) > 1e-10:
        raise AssertionError('transfer eigensolver residual exceeded numerical gate')
    # No expected sign is inserted here: a changed physical result is reported.
    return dict(rows=rows, first_epoch_constrained_modes=modes,
                first_epoch_exterior_obstruction=first['principal']['negative_discriminant'],
                result='negative exterior characteristic discriminant' if first['principal']['negative_discriminant']
                       else 'this exterior test found no negative discriminant',
                scope='Six selected archived homogeneous physical jets of unchanged gamma=1e-6 action; first stored epoch is a=1, not earliest cosmological time',
                non_claims=['No construction of a new constraint-compatible localized solution',
                            'No conclusion at epochs whose tested exterior discriminant is nonnegative',
                            'No full nonlinear or matter-sector hyperbolicity certificate',
                            'No interval certification of the archived physical background',
                            'The localization theorem needs convergence of all principal coefficients including the covariant chi Hessian'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--result-file', type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.result_file.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(result=result['result'], first=result['rows'][0],
                          constrained_modes=result['first_epoch_constrained_modes']), indent=2))
