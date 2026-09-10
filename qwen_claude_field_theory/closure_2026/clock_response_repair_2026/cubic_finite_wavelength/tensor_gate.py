#!/usr/bin/env python3
"""Direct homogeneous-branch tensor variation of the SAME cubic clock action.

Both polarizations are varied; the spatial Ricci scalar is built from the
metric, connection and Ricci tensor, not replaced by its expected TT answer.
No nonlinear degree-of-freedom or inhomogeneous-background claim is made.
"""
import argparse
import json
from pathlib import Path

import sympy as s


def derive():
    ep = s.Symbol('epsilon', real=True)
    a, lapse, M2, k = s.symbols('a N M2 k', positive=True)
    H, gamma, Lambda = s.symbols('H gamma Lambda', real=True)
    p, c, pd, cd, pz, cz, pzz, czz = s.symbols(
        'p c pd cd pz cz pzz czz', real=True)
    chid, chidd, Nd, taud, rd = s.symbols(
        'chid chidd Ndot taud rd', real=True)
    P, W, V, Cr = s.symbols('P W V Cr', real=True)

    def trunc(expr):
        return s.expand(expr).series(ep, 0, 3).removeO().expand()

    def mat_trunc(mat):
        return mat.applyfunc(trunc)

    def dt(expr):
        rates = {a: lapse*a*H, p: pd, c: cd, chid: chidd,
                 lapse: Nd}
        return s.expand(sum(s.diff(expr, v)*rate for v, rate in rates.items()))

    def dz(expr):
        rates = {p: pz, c: cz, pz: pzz, cz: czz}
        return s.expand(sum(s.diff(expr, v)*rate for v, rate in rates.items()))

    def spatial(expr, index):
        return dz(expr) if index == 2 else s.S.Zero

    # The two components are transverse to z and traceless. Exponential
    # parametrization keeps the spatial volume independent of the tensors.
    tensor = s.Matrix([[p, c, 0], [c, -p, 0], [0, 0, 0]])
    h = a*a*(s.eye(3) + ep*tensor + ep**2*tensor*tensor/2)
    hi = (s.eye(3) - ep*tensor + ep**2*tensor*tensor/2)/(a*a)
    checks = {}

    def check(name, residual):
        if isinstance(residual, s.MatrixBase):
            ok = all(s.simplify(x) == 0 for x in residual)
        else:
            ok = s.simplify(residual) == 0
        checks[name] = bool(ok)
        assert ok, name

    check('TT_trace', s.trace(tensor))
    check('TT_transverse', tensor[:, 2])
    check('metric_inverse_through_order_two', mat_trunc(h*hi)-s.eye(3))
    determinant = trunc(h.det())
    volume = trunc(s.sqrt(determinant))
    check('unimodular_spatial_volume', volume-a**3)

    # Direct ADM velocity variation. No field equations or background
    # cancellation are needed for the tensor kinetic term.
    Kmixed = mat_trunc(hi*h.applyfunc(dt)/(2*lapse))
    traceK = trunc(s.trace(Kmixed))
    normK = trunc(s.trace(mat_trunc(Kmixed*Kmixed)))
    check('traceK_unchanged', traceK-3*H)

    # Direct three-dimensional Levi-Civita connection and Ricci contraction.
    connection = [[[s.S.Zero for _ in range(3)] for _ in range(3)]
                  for _ in range(3)]
    for upper in range(3):
        for i in range(3):
            for j in range(3):
                connection[upper][i][j] = trunc(sum(
                    hi[upper, ell]*(spatial(h[ell, j], i)
                                    + spatial(h[ell, i], j)
                                    - spatial(h[i, j], ell))/2
                    for ell in range(3)))
    ricci = s.zeros(3)
    for i in range(3):
        for j in range(3):
            ricci[i, j] = trunc(sum(
                spatial(connection[ell][i][j], ell)
                - spatial(connection[ell][i][ell], j)
                + sum(connection[ell][i][j]*connection[m][ell][m]
                      - connection[m][i][ell]*connection[ell][j][m]
                      for m in range(3))
                for ell in range(3)))
    R3 = trunc(sum(hi[i, j]*ricci[i, j]
                   for i in range(3) for j in range(3)))
    EH = trunc(lapse*volume*M2*(normK-traceK**2+R3-2*Lambda)/2)
    kinetic_local = s.factor(EH.coeff(ep, 2).subs({pz: 0, cz: 0,
                                                  pzz: 0, czz: 0}))
    gradient_local = s.factor(EH.coeff(ep, 2)-kinetic_local)
    check('EH_local_velocity_from_metric',
          kinetic_local-M2*a**3*(pd**2+cd**2)/(4*lapse))
    check('EH_local_gradient_from_Ricci',
          gradient_local+M2*lapse*a*(pz**2+cz**2)/4)

    # Homogeneous covariant scalar contractions from the actual inverse
    # four-metric. P and W mean arbitrary values P(X,tau), W(0,tau);
    # their arguments have no tensor variation, not merely vanishing jets.
    inverse4 = s.diag(-1/lapse**2, 1, 1, 1)
    inverse4[1:4, 1:4] = hi
    chi_gradient = s.Matrix([chid, 0, 0, 0])
    tau_gradient = s.Matrix([taud, 0, 0, 0])
    rad_gradient = s.Matrix([rd, 0, 0, 0])
    X = trunc(-(chi_gradient.T*inverse4*chi_gradient)[0])
    Xtau = trunc(-(tau_gradient.T*inverse4*tau_gradient)[0])
    Xrad = trunc(-(rad_gradient.T*inverse4*rad_gradient)[0])
    Q = chid/lapse
    Y = trunc(Q**2-X)
    check('chi_invariant_no_tensor_variation', X-Q**2)
    check('tau_invariant_no_tensor_variation', Xtau-taud**2/lapse**2)
    check('Y_zero', Y)
    boxchi = trunc(-dt(volume*chid/lapse)/(lapse*volume))
    nonEH = {
        'P': trunc(lapse*volume*P),
        # Positive future-oriented clock branch, taud/N > 0.
        'sqrt_Xtau_W': trunc(volume*taud*W),
        'minus_V': trunc(-lapse*volume*V),
        'cubic_covariant': trunc(lapse*volume*gamma*X*boxchi),
        'radiation_proxy': trunc(lapse*volume*Cr*Xrad**2),
    }
    for name, density in nonEH.items():
        check(name+'_linear_tensor_variation', density.coeff(ep, 1))
        check(name+'_quadratic_tensor_variation', density.coeff(ep, 2))
    cubicADM = trunc(-s.Rational(2, 3)*lapse*volume*gamma*Q**3*traceK)
    boundary = trunc(dt(-gamma*volume*Q**3/3))
    check('cubic_covariant_ADM_boundary_identity',
          nonEH['cubic_covariant']-cubicADM-boundary)
    check('cubic_ADM_quadratic_tensor_variation', cubicADM.coeff(ep, 2))

    # Independent real cos(kz) amplitudes, averaged exactly over one period.
    plus, cross, plusd, crossd, cosine, sine = s.symbols(
        'plus cross plusd crossd cosine sine', real=True)
    wave = {p: plus*cosine, c: cross*cosine,
            pd: plusd*cosine, cd: crossd*cosine,
            pz: -k*plus*sine, cz: -k*cross*sine,
            pzz: -k*k*plus*cosine, czz: -k*k*cross*cosine}
    local2 = s.expand(EH.coeff(ep, 2).subs(wave))
    moments = {(0, 0): 1, (1, 0): 0, (0, 1): 0,
               (2, 0): s.Rational(1, 2),
               (0, 2): s.Rational(1, 2), (1, 1): 0}
    L2 = s.expand(sum(coef*moments[powers]
                      for powers, coef in s.Poly(local2, cosine, sine).terms()))
    velocity_hessian = s.hessian(L2, [plusd, crossd])
    gradient_hessian = -s.hessian(L2, [plus, cross])
    rank = velocity_hessian.rank()
    # Coordinate-frequency eigenvalues are N^2 k^2/a^2 times c_T^2.
    speed_matrix = (a*a/(lapse*lapse*k*k)
                    * velocity_hessian.inv()*gradient_hessian).applyfunc(s.factor)
    speeds = speed_matrix.eigenvals()
    check('computed_two_polarizations', rank-2)
    check('computed_luminal_speed_matrix', speed_matrix-s.eye(2))

    # Sensitivity control: deform only the directly computed Ricci term.
    # The speed must respond; this detects a tautological c_T^2 assignment.
    eta = s.Symbol('eta', real=True)
    deformed_L2 = L2.subs({plus: 0, cross: 0}) + eta*L2.subs(
        {plusd: 0, crossd: 0})
    deformed_speed = (a*a/(lapse*lapse*k*k)*velocity_hessian.inv()
                      *(-s.hessian(deformed_L2, [plus, cross]))).applyfunc(s.factor)
    check('curvature_mutation_changes_computed_speed',
          deformed_speed-eta*s.eye(2))
    check('zero_EH_coefficient_removes_tensor_Hessian',
          velocity_hessian.subs(M2, 0))

    facts = dict(
        scope='Linear TT modes on the homogeneous chi,tau branch; no nonlinear or all-sector degree count.',
        conventions='signature -+++; Kij=hdot_ij/(2N); H=adot/(Na); real cosine modes period-averaged',
        checks=checks, check_count=len(checks),
        spatial_Ricci_scalar_through_order_two=str(s.factor(R3)),
        KijKij_through_order_two=str(s.factor(normK)),
        traceK=str(traceK), EH_quadratic_local=str(s.factor(EH.coeff(ep, 2))),
        quadratic_mode_action=str(s.factor(L2)),
        tensor_velocity_hessian=str(velocity_hessian),
        tensor_gradient_hessian=str(gradient_hessian),
        tensor_hessian_rank=rank, speed_matrix=str(speed_matrix),
        cT_squared_eigenvalues={str(value): multiplicity for value, multiplicity in speeds.items()},
        curvature_mutation_speed_matrix=str(deformed_speed),
        non_EH_quadratic_variations={name: str(density.coeff(ep, 2))
                                     for name, density in nonEH.items()},
        radiation_scope='C_r X_r^2 is a homogeneous perfect-fluid proxy, not a photon/neutrino free-streaming CMB model.',
    )
    ctx = dict(a=a, N=lapse, M2=M2, k=k, gamma=gamma,
               quadratic_action=L2, velocity_hessian=velocity_hessian,
               gradient_hessian=gradient_hessian, speed_matrix=speed_matrix)
    return facts, ctx


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--result-file', type=Path)
    args = parser.parse_args()
    facts, _ = derive()
    rendered = json.dumps(facts, indent=2, sort_keys=True)
    if args.result_file:
        args.result_file.write_text(rendered+'\n')
    print(rendered)
