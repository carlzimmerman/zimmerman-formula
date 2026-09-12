#!/usr/bin/env python3
"""Exact static aligned principal metric response from the fixed covariant action.

Default: JSON to stdout. --output writes only the named JSON file.
No floating-point arithmetic, coefficient fitting, integration or source import.
"""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sympy as S


def derive():
    checks = {}

    def zero(name, expr):
        checks[name] = S.simplify(expr) == 0
        if not checks[name]:
            raise AssertionError((name, S.simplify(expr)))

    def truth(name, value):
        checks[name] = bool(value)
        if not checks[name]:
            raise AssertionError(name)

    e = S.symbols('epsilon', real=True)
    x = S.symbols('x', real=True)
    q, s, M2 = S.symbols('q s M2', positive=True)
    PX, PXX, W0, WY, gamma = S.symbols('PX PXX W0 WY gamma', real=True)
    phi, psi, pi, sigma = [S.Function(n)(x) for n in ('Phi', 'Psi', 'pi', 'sigma')]
    dphi, dpsi, dpi, dsigma = [S.diff(f, x) for f in (phi, psi, pi, sigma)]
    N, h = S.exp(e*phi), S.exp(-2*e*psi)
    volume = N*h**S.Rational(3, 2)
    X = q*q/N**2-e*e*dpi*dpi/h
    clock_norm = S.sqrt(s*s/N**2-e*e*dsigma*dsigma/h)
    inner = -s*q/N**2+e*e*dsigma*dpi/h
    Y = -X+inner*inner/clock_norm**2

    def quadratic(expr):
        return S.simplify(S.diff(expr, e, 2).subs(e, 0)/2)

    # Taylor jets suffice for a quadratic derivative action; coefficients
    # multiplying undifferentiated perturbations are outside this contract.
    Y2 = quadratic(Y)
    zero('Y_projector_derived', Y2-(dpi-q*dsigma/s)**2)
    PW = volume*(PX*(X-q*q)+PXX*(X-q*q)**2/2+clock_norm*(W0+WY*Y))
    PW2 = quadratic(PW)
    PWgrad = S.expand(PW2-PW2.subs({dpi: 0, dsigma: 0}))
    PWexpected = -PX*dpi**2+s*WY*(dpi-q*dsigma/s)**2-W0*dsigma**2/(2*s)
    zero('PW_spatial_action_derived', PWgrad-PWexpected)
    # gamma X Box chi = divergence - gamma grad X . grad chi.
    raw_braid = gamma*X*S.diff(volume*e*dpi/h, x)
    braid_boundary = S.diff(gamma*X*volume*e*dpi/h, x)
    braid_ibp = -gamma*volume*S.diff(X, x)*e*dpi/h
    zero('cubic_exact_integration_by_parts', raw_braid-braid_boundary-braid_ibp)
    braid2 = quadratic(braid_ibp)
    b = gamma*q*q
    zero('cubic_static_mixing_derived', braid2-2*b*dphi*dpi)
    zero('cubic_no_spatial_metric_principal_stress', S.diff(braid2, psi))
    zero('cubic_no_spatial_metric_derivative_stress', S.diff(braid2, dpsi))

    # Independent Einstein-Hilbert derivation: exact static diagonal metric,
    # with one spatial coordinate active. Isotropy supplies the dot products.
    coordinates = [S.symbols('t'), x, S.symbols('y'), S.symbols('z')]
    metric = S.diag(-N*N, h, h, h)
    inverse = metric.inv()
    Christoffel = [[[S.simplify(sum(inverse[a, d]*(
        S.diff(metric[d, c], coordinates[b0])+S.diff(metric[d, b0], coordinates[c])
        -S.diff(metric[b0, c], coordinates[d]))/2 for d in range(4)))
        for c in range(4)] for b0 in range(4)] for a in range(4)]
    Ricci = S.zeros(4)
    for a in range(4):
        for c in range(4):
            Ricci[a, c] = S.simplify(sum(
                S.diff(Christoffel[d][a][c], coordinates[d])
                -S.diff(Christoffel[d][a][d], coordinates[c])
                +sum(Christoffel[d][a][c]*Christoffel[f][d][f]
                     -Christoffel[f][a][d]*Christoffel[d][c][f] for f in range(4))
                for d in range(4)))
    scalar_curvature = S.simplify(S.trace(inverse*Ricci))
    EH2 = quadratic(M2*volume*scalar_curvature/2)
    EHibp = EH2
    for field in (phi, psi):
        second = S.diff(field, x, 2)
        coefficient = S.diff(EHibp, second)
        truth('EH_linear_second_derivative_'+str(field.func), not coefficient.has(second))
        EHibp = S.expand(EHibp-coefficient*second-S.diff(coefficient, x)*S.diff(field, x))
    zero('EH_static_quadratic_action_derived', EHibp-M2*(dpsi*dpsi-2*dphi*dpsi))

    # Clock constraint before division. For a Fourier mode the row is k²
    # times this gradient matrix, so k=0 cannot use its Schur complement.
    A = 2*PX-2*s*WY
    B = 2*q*WY
    C = W0-2*q*q*WY
    D = C/s
    raw_scalar = S.Matrix([[A, B], [B, D]])
    zero('raw_gradient_matrix_action', PWgrad+(A*dpi*dpi+2*B*dpi*dsigma+D*dsigma*dsigma)/2)
    sigma_ratio = S.factor(-B/D)
    G0 = S.factor(A-B*B/D)
    zero('G0_clock_reduction', G0-(2*PX-2*s*WY*W0/C))
    G = S.factor(G0-2*b*b/M2)
    K0 = 2*PX+4*q*q*PXX
    K = K0+6*b*b/M2
    pit, sigmat = S.symbols('pi_t sigma_t', real=True)
    Xt = (q+e*pit)**2
    temporal_PW2 = quadratic(PX*(Xt-q*q)+PXX*(Xt-q*q)**2/2+(s+e*sigmat)*W0)
    zero('K0_from_temporal_action', temporal_PW2-K0*pit*pit/2)
    zero('clock_no_temporal_principal_kinetic', S.diff(temporal_PW2,sigmat,2))
    L2 = S.factor(EHibp+PWgrad+braid2)
    Lreduced = S.simplify(L2.subs(dsigma, sigma_ratio*dpi))
    zero('reduced_static_action', Lreduced-(M2*(dpsi*dpsi-2*dphi*dpsi)-G0*dpi*dpi/2+2*b*dphi*dpi))

    # Full 3D Fourier Einstein operator, derived from the metric perturbation.
    # This is an independent tensor check that never assigns Psi=Phi.
    kx, ky, kz, omega = S.symbols('kx ky kz omega', real=True)
    k2 = kx*kx+ky*ky+kz*kz
    covector = S.Matrix([0, kx, ky, kz])
    eta = S.diag(-1, 1, 1, 1)
    Phi, Psi, Pi, Sig, rho = S.symbols('Phi_hat Psi_hat pi_hat sigma_hat rho_hat', real=True)
    perturbation = S.diag(-2*Phi, -2*Psi, -2*Psi, -2*Psi)
    trace_h = S.trace(eta*perturbation)
    linear_Ricci = S.zeros(4)
    for mu in range(4):
        for nu in range(4):
            linear_Ricci[mu, nu] = S.expand((
                -covector[mu]*(perturbation*eta*covector)[nu]
                -covector[nu]*(perturbation*eta*covector)[mu]
                +k2*perturbation[mu, nu]+covector[mu]*covector[nu]*trace_h)/2)
    linear_Einstein = linear_Ricci-eta*S.trace(eta*linear_Ricci)/2
    zero('Einstein_00_direct', linear_Einstein[0, 0]+2*k2*Psi)
    zero('Ricci_00_direct', linear_Ricci[0, 0]+k2*Phi)
    for i in range(1, 4):
        for j in range(1, 4):
            zero('Einstein_spatial_'+str(i)+str(j), linear_Einstein[i, j]
                 -(-covector[i]*covector[j]+int(i == j)*k2)*(Psi-Phi))
    zero('spatial_trace_forces_slip', sum(linear_Einstein[i, i] for i in range(1, 4))-2*k2*(Psi-Phi))

    # Arbitrary Hessian verifies the action-derived cubic metric stress and
    # Einstein debraiding before specializing to static modes.
    a00, a01, a02, a03, a11, a12, a13, a22, a23, a33 = S.symbols(
        'a00 a01 a02 a03 a11 a12 a13 a22 a23 a33', real=True)
    Hessian = S.Matrix([[a00,a01,a02,a03], [a01,a11,a12,a13],
                       [a02,a12,a22,a23], [a03,a13,a23,a33]])
    v = S.Matrix([q, 0, 0, 0])
    vu = eta*v
    cubic_T = 2*gamma*(S.trace(eta*Hessian)*v*v.T-v*(Hessian*vu).T
                      -(Hessian*vu)*v.T+eta*(vu.T*Hessian*vu)[0])
    cubic_R = (cubic_T-eta*S.trace(eta*cubic_T)/2)/M2
    zero('debraiding_kinetic_gradient_relation', -2*gamma*(vu.T*cubic_R*vu)[0]
         -(-6*b*b*a00/M2-2*b*b*(a11+a22+a33)/M2))
    static_subs = dict(zip((a00,a01,a02,a03,a11,a12,a13,a22,a23,a33),
        (0,0,0,0,-kx*kx*Pi,-kx*ky*Pi,-kx*kz*Pi,-ky*ky*Pi,-ky*kz*Pi,-kz*kz*Pi)))
    static_T = cubic_T.subs(static_subs)
    zero('cubic_T00_from_tensor', static_T[0, 0]+2*b*k2*Pi)
    for i in range(1, 4):
        for j in range(1, 4):
            zero('cubic_T_spatial_'+str(i)+str(j), static_T[i, j])
    zero('cubic_R00_from_tensor', cubic_R[0, 0].subs(static_subs)+b*k2*Pi/M2)

    # Static minimally coupled dust adds -rho*Phi to the quadratic action.
    # The raw four-field matrix remains available at C=0 or G=0.
    laplace = S.symbols('k_squared', positive=True)
    bb, aa, dd, cc = S.symbols('b A B D', real=True)
    matrix = S.Matrix([
        [0, -2*M2, 2*bb, 0],
        [-2*M2, 2*M2, 0, 0],
        [2*bb, 0, -aa, -dd],
        [0, 0, -dd, -cc],
    ])
    rhs = S.Matrix([rho/laplace, 0, 0, 0])
    solution = matrix.inv()*rhs
    raw_det = S.factor(matrix.det())
    zero('raw_static_matrix_determinant', raw_det+4*M2*(M2*(aa*cc-dd*dd)-2*bb*bb*cc))
    abstract_subs = {aa:A, dd:B, cc:D, bb:b}
    physical = S.simplify(solution.subs(abstract_subs))
    Phi_answer = -rho*G0/(2*M2*G*laplace)
    Pi_answer = -b*rho/(M2*G*laplace)
    zero('Phi_source_normalized', physical[0]-Phi_answer)
    zero('Psi_independently_solved', physical[1]-Phi_answer)
    zero('pi_source_normalized', physical[2]-Pi_answer)
    zero('sigma_source_normalized', physical[3]-sigma_ratio*Pi_answer)
    zero('source_equations_reinserted', (matrix.subs(abstract_subs)*physical-rhs).norm())
    enhancement = S.factor(G0/G)
    zero('enhancement_identity', enhancement-1-2*b*b/(M2*G))
    zero('static_gamma_on_nonzero_Phi', S.factor(physical[1]/physical[0])-1)
    zero('minimal_dust_R00_GR_normalization', (rho-S.trace(eta*S.diag(rho,0,0,0))*eta[0,0]/2)/M2-rho/(2*M2))

    # Vary an explicit g0x perturbation before choosing a zero-shift gauge.
    # dL/d(g0x)=T^0x=−T0x at the background, fixing the sign independently.
    shift = S.Function('metric_0x')(x)
    shifted_metric = S.Matrix([[-N*N,e*shift],[e*shift,h]])
    shifted_inverse = shifted_metric.inv()
    shifted_volume = S.sqrt(-shifted_metric.det()*h*h)
    chi_gradient = S.Matrix([q,e*dpi])
    tau_gradient = S.Matrix([s,e*dsigma])
    shifted_X = -(chi_gradient.T*shifted_inverse*chi_gradient)[0]
    shifted_s = S.sqrt(-(tau_gradient.T*shifted_inverse*tau_gradient)[0])
    shifted_inner = (tau_gradient.T*shifted_inverse*chi_gradient)[0]
    shifted_Y = -shifted_X+shifted_inner*shifted_inner/(shifted_s*shifted_s)
    shifted_PW2 = quadratic(shifted_volume*(PX*(shifted_X-q*q)
        +PXX*(shifted_X-q*q)**2/2+shifted_s*(W0+WY*shifted_Y)))
    shifted_braid2 = quadratic(-gamma*shifted_volume*S.diff(shifted_X,x)
        *(shifted_inverse*chi_gradient)[1])
    momentum_from_action = -S.diff(shifted_PW2+shifted_braid2,shift).subs(shift,0)
    T0x = 2*q*PX*dpi+W0*dsigma-2*gamma*q**3*dphi
    zero('momentum_stress_derived_from_shift_action', momentum_from_action-T0x)
    zero('momentum_constraint_consistency', T0x.subs(dsigma, sigma_ratio*dpi)-q*(G0*dpi-2*b*dphi))

    # Controls deliberately distinguish all zero denominators.
    zero('GR_decoupling_metric', S.factor(physical[0].subs(gamma,0))+rho/(2*M2*laplace))
    zero('GR_decoupling_scalar', physical[2].subs(gamma,0))
    zero('WY_zero_clock_reduction', G0.subs(WY,0)-2*PX)
    zero('W0_zero_clock_cancellation', G0.subs(W0,0)-2*PX)
    truth('k_zero_raw_rows_vanish', (laplace*matrix).subs(laplace,0) == S.zeros(4))
    # At D=0 with B!=0 the clock row fixes pi=0, but the complete matrix is
    # invertible. This is not the regular Schur formula, nor a physical proof
    # that this kinetic degeneracy is healthy.
    critical_clock_matrix = matrix.subs(cc,0)
    critical_clock_solution = S.simplify(critical_clock_matrix.inv()*rhs)
    zero('critical_clock_determinant_nonzero_when_B_nonzero', critical_clock_matrix.det()-4*M2*M2*dd*dd)
    zero('critical_clock_pi_zero', critical_clock_solution[2])
    zero('critical_clock_metric_GR', critical_clock_solution[0]+rho/(2*M2*laplace))
    zero('critical_clock_sigma', critical_clock_solution[3]+bb*rho/(M2*dd*laplace))
    # Regular clock, G=0 and b!=0: sourced rows are inconsistent. An exact
    # rational fixture tests ranks, not an approximate small-denominator fit.
    singular = matrix.subs({M2:1,bb:1,aa:2,dd:0,cc:1})
    forced = rhs.subs({rho:1,laplace:1})
    truth('G_zero_nonzero_b_inconsistent_rank', singular.rank() == 3 and singular.row_join(forced).rank() == 4)
    null_vector = S.Matrix([bb/M2,bb/M2,1,-dd/cc])
    singular_symbolic = matrix.subs(aa,dd*dd/cc+2*bb*bb/M2)
    zero('G_zero_exact_null_vector', (singular_symbolic*null_vector).norm())
    zero('G_zero_exact_source_compatibility', (null_vector.T*rhs)[0]-bb*rho/(M2*laplace))
    # If b=G0=0, the scalar row vanishes while the metric remains GR.
    decoupled_zero = matrix.subs({M2:1,bb:0,aa:0,dd:0,cc:1})
    truth('decoupled_G_zero_consistent_rank', decoupled_zero.rank() == decoupled_zero.row_join(forced).rank() == 3)
    # G0=0,b!=0 has zero potentials and nonzero scalar response: gamma_static
    # is 0/0 although the field equations still imply Phi=Psi.
    screened_fixture = S.simplify(solution.subs({aa:0,dd:0,cc:1,bb:1,M2:1}))
    zero('G0_zero_Phi', screened_fixture[0])
    zero('G0_zero_Psi', screened_fixture[1])
    zero('G0_zero_pi', screened_fixture[2]-rho/(2*laplace))
    positive_fixture = S.simplify(enhancement.subs({PX:2,PXX:0,WY:0,W0:1,q:1,s:1,M2:1,gamma:1}))
    zero('healthy_rational_fixture_enhancement_two', positive_fixture-2)
    zero('healthy_rational_fixture_G_two', G.subs({PX:2,WY:0,W0:1,q:1,s:1,M2:1,gamma:1})-2)
    zero('healthy_rational_fixture_K_ten', K.subs({PX:2,PXX:0,q:1,M2:1,gamma:1})-10)
    return {
        'claim': 'At an aligned frozen affine jet, exact leading static dust response has equal metric potentials and gain G0/G on the regular k!=0 clock branch.',
        'scope': 'Quadratic perturbations; highest spatial derivative static operator at one local affine timelike jet; constant positive Einstein coefficient; minimal stationary pressureless source; not PPN or a finite-wavelength/global solution.',
        'conventions': {'metric':'ds²=−(1+2Phi)dt²+(1−2Psi)delta_ij dx^i dx^j at linear order',
            'action':'sqrt(−g)[M2 R/2+P(X,tau)−V(tau)+s W(Y,tau)+gamma X Box chi]+S_m[g,m]',
            'X':'−g^mu nu d_mu chi d_nu chi', 's':'sqrt(−grad tau²)',
            'Y':'(g^mu nu+n^mu n^nu)d_mu chi d_nu chi', 'n':'−grad tau/s',
            'background':'chi=q t, tau=s t, q>0,s>0, vanishing covariant scalar Hessian at the affine jet',
            'Einstein':'M2 G_mu nu=T_mu nu, M2>0', 'Fourier':'exp(i k.x), Delta=−k²',
            'coefficient_domain':'exact SymPy rational function field, all named parameters real'},
        'derived_action': {'EH_after_boundary_removal':str(S.factor(EHibp)),
            'PW_spatial':str(S.factor(PWgrad)), 'cubic_static':str(braid2),
            'clock_gradient_matrix':str(raw_scalar), 'clock_sigma_over_pi':str(sigma_ratio),
            'G0':str(G0), 'G':str(G), 'K':str(K), 'b':str(b)},
        'metric_equations': ['2 M2 Delta Psi = rho + 2 b Delta pi',
            '(partial_i partial_j−delta_ij Delta)(Psi−Phi)=0',
            'G0 Delta pi−2 b Delta Phi=0',
            '(B pi+D sigma) k²=0, B=2q WY, D=(W0−2q²WY)/s'],
        'response': {'Phi_hat':str(Phi_answer), 'Psi_hat':str(Phi_answer),
            'pi_hat':str(Pi_answer),'sigma_hat':str(S.factor(sigma_ratio*Pi_answer)),
            'gain_over_GR':str(enhancement), 'gain_identity':'1+2 b²/(M2 G)',
            'gamma_static':'Psi_hat/Phi_hat=1 where Phi_hat!=0; equality of fields holds even where ratio is undefined',
            'scalar_speed_squared':'G/K, when kinetic/gradient reduction is valid',
            'propagator_denominator':'G k²−K omega²; scalar dust forcing at omega=0 is b rho/M2',
            'positive_scalar_principal_branch':'If K>0,G>0,M2>0, gain>=1; strict gain>1 for b!=0. These inequalities alone do not certify full health.',
            'lensing_potential':'(Phi+Psi)/2=Phi at this principal static order'},
        'degeneracies': {'raw_matrix_order':['Phi','Psi','pi','sigma'], 'raw_matrix':str(matrix),
            'raw_matrix_equation':'k² matrix field_vector=(rho,0,0,0)^T',
            'raw_determinant':str(raw_det),
            'k_zero':'Every displayed principal row vanishes. A nonzero homogeneous rho cannot be solved by this operator; lower derivative/background equations decide.',
            'C_zero_B_nonzero':'Do not divide by C. Raw matrix invertible: pi=0, Phi=Psi=−rho/(2M2 k²), sigma=−b rho/(M2 B k²). Health not established.',
            'C_zero_B_zero':'The clock principal row is zero; omit its undetermined direction and solve the remaining scalar/metric block. This occurs at W0=WY=0 for q>0.',
            'G_zero_b_nonzero':'With regular clock and rho_hat!=0, static principal equations inconsistent; no finite static inverse at this order.',
            'G_zero_b_zero':'Regular clock leaves an undetermined scalar mode; minimally sourced metric is still GR.',
            'G0_zero_b_nonzero':'Phi=Psi=0 and pi=rho/(2b k²), while G=−2b²/M2<0; the potential ratio is undefined and the K>0 branch has a gradient instability.'},
        'limitations': ['No background Einstein/clock evolution or tadpole cancellation has been solved.',
            'Frozen P/W/V coefficients and an affine background omit lower derivative mass, pressure, density and cosmological terms.',
            'Neglected terms need not be small near G=0, C=0, k=0, a finite-wavelength pole, or a non-affine background.',
            'The displayed 0i first-gradient constraint is consistent, but this does not solve all subprincipal equations.',
            'No global Green function, finite source matching, nonlinear radial branch, retarded prescription, empirical fit or PPN expansion is supplied.'],
        'checks':checks,
        'provenance': {'python':platform.python_version(), 'sympy':S.__version__,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'parent_base_revision':'f59fad6c7', 'arithmetic':'exact', 'randomness':False}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = json.dumps(derive(), indent=2)+'\n'
    if args.output:
        args.output.write_text(result)
    else:
        print(result, end='')
