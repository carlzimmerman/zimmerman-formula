#!/usr/bin/env python3
"""General target-point inputs for the SAME global-a0 inverse action.

This imports the independent arbitrary-precision inverse from the preceding
checkpoint. eps labels exterior targets, not a calibrated baryonic mass.
No coefficient or acceptance flag is inserted as an expected physics result.
"""
from dataclasses import dataclass
from pathlib import Path
import sys
import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kgb_universal_clock_2026'))
import high_precision_gate as h


@dataclass(frozen=True)
class Spec:
    eps1: str = '1e-6'
    eps2: str = '2e-6'
    y1: str = '.1'
    X: str = '.5'
    F: str = '.525'
    sign_w: int = -1
    pressure_root: int = 1


def pair(theta, u1, spec=Spec()):
    if spec.sign_w not in (-1, 1) or spec.pressure_root not in (-1, 1):
        raise ValueError('branch signs must be +1 or -1')
    dw1, y2, u2 = [mp.exp(v) for v in theta]
    eps1, eps2, y1, X, F = map(mp.mpf, (spec.eps1, spec.eps2, spec.y1, spec.X, spec.F))
    if min(eps1, eps2, y1, X, F, u1) <= 0:
        raise ValueError('positive regular target parameters required')
    base = h.normalized(eps1, y1, X, eps1*u1, -1, F)
    w1 = spec.sign_w * mp.mpf('.05') * dw1 * base['g']
    a = h.normalized(eps1, y1, X, eps1*u1, w1, F)
    bb = h.normalized(eps2, y2, X, eps2*u2, -1, F)
    aa = bb['g'] + 2/bb['r']
    disc = aa*aa + mp.mpf('1.5')*bb['B']*a['P']/F
    if not mp.isfinite(disc) or disc <= 0:
        raise ValueError('pressure quadratic outside real regular branch')
    if spec.pressure_root == 1:
        w2 = bb['B']*a['P']/(aa+mp.sqrt(disc))
    else:
        w2 = -2*F*(aa+mp.sqrt(disc))/3
    b = h.normalized(eps2, y2, X, eps2*u2, w2, F)
    for row in (a, b):
        if min(row['Dcoord'], row['B'], row['U']) <= 0 or not row['w']:
            raise ValueError('singular or reversed target chart')
        if not all(mp.isfinite(v) for v in row.values()):
            raise ValueError('nonfinite inverse coefficients')
    return a, b


def relative_difference(a, b):
    return (a-b)/(1+abs(a)+abs(b))


def residual(theta, u1, spec=Spec()):
    """Three initial-match conditions in the nonzero-braiding chart."""
    a, b = pair(theta, u1, spec)
    A1, B1 = h.parts(a); A2, B2 = h.parts(b)
    A, B = A1-A2, B1-B2
    den = mp.norm(A)*mp.norm(B)
    if not den:
        raise ValueError('zero first-preservation vector requires separate chart')
    return (relative_difference(a['H'], b['H']),
            relative_difference(a['gamma'], b['gamma']),
            (A[0]*B[1]-A[1]*B[0])/den)


def gate(theta, u1, spec=Spec(), tolerance='1e-20'):
    a, b = pair(theta, u1, spec)
    A1, B1 = h.parts(a); A2, B2 = h.parts(b)
    A, B = A1-A2, B1-B2
    den = mp.fdot(B, B)
    if not den:
        raise ValueError('zero B requires separate first-control chart')
    f = -mp.fdot(A, B)/den
    h.check_map(f, a['F'], a['X'])
    N1, N2 = h.next_drift(a, f), h.next_drift(b, f)
    N = N1-N2
    j, err = h.next_control(N, B)
    product = mp.norm(N)*mp.norm(B)
    obstruction = (N[0]*B[1]-N[1]*B[0])/product if product else mp.mpf(0)
    def jets(row, AA, BB):
        return [row['P'], f*row['kappa'], f*row['gamma'],
                j*row['kappa']+f*(AA[0]+f*BB[0]),
                j*row['gamma']+f*(AA[1]+f*BB[1])]
    raw_relative = [relative_difference(v, w) for v, w in zip(jets(a, A1, B1), jets(b, A2, B2))]
    first_relative = [(A[i]+f*B[i])/(1+abs(A[i])+abs(f*B[i])) for i in range(2)]
    next_relative = [err[i]/(1+abs(N[i])+abs(j*B[i])) for i in range(2)]
    maximum = max(map(abs, raw_relative+first_relative+next_relative))
    return dict(states=(a,b), f=f, j=j, A=A, B=B, N=N,
                raw_five_relative=raw_relative, first_relative=first_relative,
                next_relative=next_relative, next_obstruction=obstruction,
                joint_accepted=maximum < mp.mpf(tolerance), maximum=maximum,
                scope='Necessary pointwise action compatibility only; not full theory closure')


if __name__ == '__main__':
    with mp.workdps(40):
        theta = [mp.log(mp.mpf(x)) for x in
                 ('4164.895400320220432828310157', '.153793693461797102646484544',
                  '.026005824599944823806882655')]
        row = gate(theta, mp.mpf('.03'))
        print('next_obstruction=' + mp.nstr(row['next_obstruction'], 30))
        print('joint_accepted=' + str(row['joint_accepted']))
