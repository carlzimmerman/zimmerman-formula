"""Construct and vary an exponential lapse/clock action; compute reduced constraints.

c=1; all acceleration variables are inverse lengths. No PPN or global
constraint certificate is inferred from this frozen scalar principal block.
Run from the repository root. Prints exact identities and a deterministic scan.
"""
import json
import platform
import shutil

import numpy as np
import sympy as s


def canonical_constraints(L, qs, vs):
    """Dirac preservation for a quadratic finite canonical system.

    Pseudoinverse constructs one canonical Hamiltonian; all null velocities
    enter via primary multipliers. Left nulls of the ACTUAL bracket matrix
    supply consistency conditions; iteration ends only at row-space closure.
    """
    n = len(qs)
    q = s.Matrix(qs)
    v = s.Matrix(vs)
    W = s.hessian(L, vs)
    B = s.Matrix(n, n, lambda i, j: s.diff(L, vs[i], qs[j]))
    C = s.hessian(L, qs)
    assert s.expand(L - (v.T*W*v/2 + v.T*B*q + q.T*C*q/2)[0]) == 0
    P = W.pinv()
    H = (B.T*P*B-C).row_join(-B.T*P).col_join((-P*B).row_join(P))
    J = s.zeros(n).row_join(s.eye(n)).col_join((-s.eye(n)).row_join(s.zeros(n)))
    rows = [(-z.T*B).row_join(z.T) for z in W.nullspace()]
    A = s.Matrix.vstack(*rows) if rows else s.zeros(0, 2*n)
    generations = [A.rows]
    raw = [A]
    for _ in range(2*n+1):
        bracket = A*J*A.T
        candidates = [z.T*A*J*H for z in bracket.T.nullspace()]
        old = A.rows
        for row in candidates:
            trial = A.col_join(row)
            if trial.rank() > A.rank():
                A = trial
        if A.rows == old:
            break
        generations.append(A.rows-old)
        raw.append(A[old:, :])
    else:
        raise RuntimeError('Dirac preservation did not reach closure')
    A = A.applyfunc(s.factor)
    bracket = (A*J*A.T).applyfunc(s.factor)
    nsc = bracket.rank()
    nfc = A.rows-nsc
    return dict(velocity_rank=W.rank(), generations=generations,
                constraint_rows=[str(x) for x in raw],
                poisson_matrix=str(bracket), poisson_rank=nsc,
                first_class=nfc, second_class=nsc,
                dof=s.Rational(2*n-2*nfc-nsc, 2))


def derive():
    y = s.symbols('y', positive=True)
    C, b, A = s.symbols('C b A', positive=True)
    mu = 1-s.exp(-y)
    primitive = s.integrate(2*y*mu, y)
    G = s.simplify(primitive-s.limit(primitive, y, 0, dir='+'))
    f = 2*y**2-C*G
    at = s.simplify(s.diff(f, y)/(2*y))
    al = s.simplify(s.diff(f, y, 2)/2)
    assert s.simplify(at-(2-C*mu)) == 0
    assert s.simplify(al-(2-C*s.diff(y*mu, y))) == 0

    # Algebraic projected-vector representation, not a gradient scalar.
    # L_extra=c14*g^2+2*b*g.V-b*J(V^2), A=2-c14.
    u = y*(A-C*mu)/b
    jp0 = s.integrate(2*y*s.diff(u, y), y)
    Jp = s.simplify(jp0-s.limit(jp0, y, 0, dir='+'))
    jY = s.simplify(s.diff(Jp, y)/s.diff(u*u, y))
    assert s.simplify(jY*u-y) == 0
    assert s.simplify((2-A)*y*y+2*b*y*u-b*Jp-f) == 0

    # Keep Phi and Psi independent, Cartesian gradient jets in c=1 units.
    gp, gs, a0, rho, Gb = s.symbols('gPhi gPsi a0 rho Gbare', positive=True)
    Lstat = 2*gs**2-4*gp*gs+a0**2*f.subs(y, gp/a0)
    psi_flux = s.diff(Lstat, gs)
    phi_flux = s.simplify(s.diff(Lstat, gp).subs(gs, gp))
    assert s.simplify(psi_flux-4*(gs-gp)) == 0
    assert s.simplify(phi_flux+2*C*mu.subs(y, gp/a0)*gp) == 0
    GN = s.solve(s.Eq(2*C*4*s.pi*s.Symbol('Gmeasured'), 16*s.pi*Gb),
                 s.Symbol('Gmeasured'))[0]

    # Frozen, nonzero acceleration background. Angle enters alpha through
    # Hessian of f(|a|); beta=0, lambda=ell in standard ADM notation.
    alpha, ell, k = s.symbols('alpha ell k', positive=True)
    trace_factor = s.symbols('trace_factor', real=True)
    z, n, shift = qs = s.symbols('zeta lapse shift', real=True)
    zd, nd, shd = vs = s.symbols('zetadot lapsedot shiftdot', real=True)
    L = (-6*trace_factor*zd**2+4*k*k*zd*shift-ell*(3*zd-k*k*shift)**2
         +k*k*(2*z*z-4*n*z+alpha*n*n))
    aux = s.solve([s.diff(L, n), s.diff(L, shift)], [n, shift])
    reduced = s.factor(L.subs(aux))
    kinetic = s.factor(s.diff(reduced, zd, 2))
    stiffness = s.factor(-s.diff(reduced, z, 2)/k**2)
    cs2 = s.factor(stiffness/kinetic)
    # Opposite order of elimination is an independent algebraic control.
    nfirst = L.subs(n, s.solve(s.diff(L, n), n)[0])
    other = nfirst.subs(shift, s.solve(s.diff(nfirst, shift), shift)[0])
    assert s.simplify(other-reduced) == 0
    count = canonical_constraints(L.subs(trace_factor, 1), qs, vs)
    # Deterministic numerical scan, checked against generalized eigenvalues
    # of the unreduced (lapse,shift,zeta) field equations below.
    cval = s.Rational(5, 3)
    lval = s.Rational(1, 100)
    ys = np.geomspace(1e-8, 80., 141)
    angles = np.linspace(0., 1., 25)  # cos(theta)^2
    muf = -np.expm1(-ys)
    ml = muf+ys*np.exp(-ys)
    avals = 2-float(cval)*(muf[:, None]*(1-angles)+ml[:, None]*angles)
    speeds = float(lval)*(2-avals)/((2+3*float(lval))*avals)
    assert np.all(avals > 0) and np.all(avals < 2)
    assert np.all(speeds > 0) and np.all(speeds < 1)

    W = s.hessian(L, vs)
    B = s.Matrix(3, 3, lambda i, j: s.diff(L, vs[i], qs[j]))
    H = s.hessian(L, qs)
    rate, w2 = s.symbols('rate omega2')
    char = s.factor((rate**2*W+rate*(B-B.T)-H).det())
    poly = s.Poly(char, rate)
    dynamical = s.simplify(poly.coeff_monomial(1)/poly.coeff_monomial(rate**2)/k**2)
    assert s.simplify(dynamical-cs2) == 0

    # Scalar conserved-source test, deriving equations by Euler-Lagrange.
    # src=16 pi Gb rho, Tzz=-rate^2 rho/k^2, div j=-rho_dot.
    # This tests a linear, conserved longitudinal source, not full nonlinear PPN.
    src = s.symbols('src', real=True)
    source_L = -src*n+rate*src*shift+rate**2*src*z/k**2
    time_EL = rate*s.diff(L, zd).subs(zd, rate*z)-s.diff(L, z)
    equations = [s.diff(L+source_L, n).subs(zd, rate*z),
                 s.diff(L+source_L, shift).subs(zd, rate*z),
                 time_EL-s.diff(source_L, z)]
    response = s.solve(equations, [n, shift, z])
    Rzz = s.factor((-k*k*(n+rate*shift)+rate**2*z).subs(response))
    Rxx = s.factor((rate**2*z).subs(response))
    # GR reference is re-solved from its lapse and scalar equations in shift=0
    # gauge. Gb is replaced by GN, hence src_GR=2src/C.
    Lgr = L.subs({alpha: 0, ell: 0, trace_factor: 1})
    source_gr = source_L.subs(src, 2*src/C)
    gr_eqs = [s.diff(Lgr+source_gr, n).subs({zd: rate*z, shift: 0}),
               (rate*s.diff(Lgr, zd).subs(zd, rate*z)-s.diff(Lgr+source_gr, z)).subs(shift, 0)]
    gr_response = s.solve(gr_eqs, [n, z])
    Rgr = s.factor((-k*k*n+rate**2*z).subs(gr_response))
    high_response = Rzz.subs(alpha, 2-C)
    mismatch = s.factor(s.limit((high_response-Rgr)/rate**2, rate, 0))
    trace_match = s.solve(mismatch, trace_factor)[0]
    # U=P_T^{ij}Kij=-2*zeta_dot at nonzero k; eta_U U^2 changes
    # -6 zeta_dot^2 to -6 trace_factor zeta_dot^2.
    etaU = s.simplify(s.Rational(3, 2)*(1-trace_match))
    repaired_L = s.factor(L.subs(trace_factor, trace_match))
    repaired_count = canonical_constraints(repaired_L.subs({C: cval, ell: lval}), qs, vs)
    repaired_kinetic = s.factor(kinetic.subs(trace_factor, trace_match))
    repaired_cs2 = s.factor(cs2.subs(trace_factor, trace_match))
    repaired_speeds = np.asarray(s.lambdify(alpha, repaired_cs2.subs({C:cval,ell:lval}), 'numpy')(avals))
    assert np.all(repaired_speeds > 0) and np.all(repaired_speeds < 1)
    assert s.simplify(mismatch.subs(trace_factor, trace_match)) == 0
    leftover = s.factor((high_response-Rgr).subs(trace_factor, trace_match))
    # Preserve residual at higher frequency rather than reporting full GR.
    assert s.limit(leftover/rate**2, rate, 0) == 0
    gr_Rxx = s.factor((rate**2*z).subs(gr_response))
    left_xx = s.factor((Rxx.subs(alpha, 2-C)-gr_Rxx).subs(trace_factor, trace_match))
    assert s.limit(left_xx/rate**2, rate, 0) == 0
    # Global coefficient bound is analytic; the grid only checks implementation.
    longitudinal = s.diff(y*mu, y)
    critical = s.solve(s.diff(longitudinal, y), y)
    C_ceiling = s.simplify(2/longitudinal.subs(y, critical[0]))
    alpha_min = s.simplify(2-cval*longitudinal.subs(y, critical[0]))
    global_speed_max = s.simplify(repaired_cs2.subs({C:cval, ell:lval, alpha:alpha_min}))

    # Exact background FLRW: lapse varied BEFORE cosmic-time gauge.
    scale, adot, lapse, Lam = s.symbols('scale adot N Lambda', positive=True)
    Lh = -3*(2+3*ell)*scale*adot**2/lapse-2*Lam*lapse*scale**3
    homogeneous_lapse = s.diff(Lh, lapse)
    Hubble, rh = s.symbols('H rho', real=True)
    h2 = s.solve((homogeneous_lapse-16*s.pi*Gb*scale**3*rh).subs(
        adot, lapse*scale*Hubble), Hubble**2)[0]
    Gcos = s.simplify(s.diff(h2, rh)/(8*s.pi/3))
    # Tensor TT kinetic and gradient follow from KijKij-K^2+R3;
    # trace-only ell term does not contribute on TT at principal order.
    ht, hx, hy = s.symbols('hplusdot hplusgrad hcrossdot')
    # Explicit symmetric trace-free shear contracts to twice each amplitude.
    Ktt = s.Matrix([[ht/2, hy/2, 0], [hy/2, -ht/2, 0], [0, 0, 0]])
    Lttkin = s.trace(Ktt*Ktt)-s.trace(Ktt)**2-ell*s.trace(Ktt)**2
    Ltt = Lttkin.subs(hy, 0)-hx**2/2
    tensor_speed = s.simplify(-s.diff(Ltt, hx, 2)/s.diff(Ltt, ht, 2))

    # NEW constructive operator: eta V_i(-Delta)^-1 V^i, with
    # V_i=P_T_i^j D^m K_jm and P_T=I-D Delta^-1 div.
    # k is along z. Compute its quadratic principal block from K itself.
    eta, sx, sy, px, py = s.symbols('eta shiftx shifty px py', real=True)
    Kvec = s.Matrix([[0, 0, -k*sx/2], [0, 0, -k*sy/2],
                     [-k*sx/2, -k*sy/2, 0]])
    KTscalar = s.diag(-zd, -zd, -zd+k*k*shift)
    PT = s.diag(1, 1, 0)
    Vvec = PT*(k*Kvec[:, 2])
    Vscalar = PT*(k*KTscalar[:, 2])
    Vtensor = PT*(k*Ktt[:, 2])
    Lv = s.expand(s.trace(Kvec*Kvec)+eta*(Vvec.T*Vvec)[0]/k**2)
    assert Vscalar == s.zeros(3, 1) and Vtensor == s.zeros(3, 1)
    mom, Vpot = s.symbols('momentum_density V_PPN', real=True)
    # Sm variation in stationary transverse sector is +j_i shift^i.
    sourced = Lv.subs(sy, 0)+16*s.pi*Gb*mom*sx
    shift_solution = s.solve(s.diff(sourced, sx), sx)[0]
    shift_ratio = s.simplify(shift_solution/(4*s.pi*GN*mom/k**2))
    # Standard PPN transverse projection, gamma=1:
    # g0i^T=-(4+alpha1/2) V_i^T. This is the parameter definition,
    # not an imported value of alpha1.
    alpha1 = s.factor(-2*shift_ratio-8)
    eta_solution = s.solve(alpha1, eta)
    eta_match = eta_solution[0]
    repaired_lv = s.factor(Lv.subs(eta, eta_match))
    vector_count = canonical_constraints(repaired_lv, [sx, sy], [px, py])
    assert s.simplify(alpha1.subs(eta, eta_match)) == 0
    assert s.simplify(s.diff(repaired_lv, sx, 2)-C*k*k/2) == 0
    # The pure GR normalization control follows directly from the same EOM.
    assert s.simplify(shift_ratio.subs({C: 2, eta: 0})+4) == 0

    return {
        'status': 'CONSTRUCTED_STATIC_AND_FROZEN_PRINCIPAL_BRANCH; FULL_THEORY_OPEN',
        'action': 'S=(16 pi Gb)^-1 integral sqrt(-g) [R-2Lambda-ell theta^2+a0^2 f(a/a0)+eta V_i(-Delta_h)^-1 V^i+eta_U U^2]+Sm',
        'primitive': str(G), 'f': str(f),
        'auxiliary_vector': {'u(y)': str(u), 'J(u(y)^2)': str(Jp), 'J_Y': str(jY)},
        'static': {'Psi_flux': str(psi_flux), 'Phi_flux_on_matched_branch': str(phi_flux),
                   'measured_G': str(GN), 'PDE': 'div[mu grad Phi]=4 pi Gmeasured rho',
                   'boundary_requirement': 'harmonic Psi-Phi fixed to zero'},
        'principal': {'alpha_transverse': str(at), 'alpha_parallel': str(al),
                      'reduced_L': str(reduced), 'kinetic_hessian': str(kinetic),
                      'gradient_hessian': str(stiffness), 'sound_speed_squared': str(cs2),
                      'unreduced_characteristic': str(char),
                      'count': count, 'tensor_speed_squared': str(tensor_speed)},
        'finite_scan': {'C': str(cval), 'ell': str(lval), 'y_range': [1e-8, 80],
                        'angle_cos2_range': [0, 1], 'points': int(speeds.size),
                        'min_alpha': float(avals.min()), 'max_alpha': float(avals.max()),
                        'min_cs2': float(speeds.min()), 'max_cs2': float(speeds.max())},
        'FLRW': {'lapse_equation': str(homogeneous_lapse), 'H_squared': str(h2),
                 'Gcos': str(Gcos), 'Gcos_over_Gmeasured': str(s.simplify(Gcos/GN))},
        'transverse_repair': {
            'definition': 'V_i=P_T_i^j D^m K_jm; P_T=I-D Delta_h^-1 div, on zero-mean flat Fourier modes',
            'computed_vector_L': str(Lv), 'scalar_V': str(Vscalar), 'tensor_V': str(Vtensor),
            'shift_solution': str(shift_solution), 'g0i_over_Vppn': str(shift_ratio),
            'alpha1_from_transverse_PPN_matching': str(alpha1),
            'eta_for_alpha1_zero': str(eta_match), 'repaired_vector_L': str(repaired_lv),
            'vector_constraint_count': vector_count,
            'scope': 'constant high-acceleration coefficients; full boosted scalar PPN alpha2 not inferred'},
        'scalar_response_repair': {
            'definition': 'U=K-mean(K)-Delta_h^-1 D_i D_j K^ij, zero homogeneous mode',
            'source': 'Tzz=-rate^2 rho/k^2; div(j)=-rate rho; src=16 pi Gb rho',
            'computed_Rzz': str(Rzz), 'computed_Rxx': str(Rxx), 'GR_Rzz': str(Rgr),
            'order_rate2_mismatch': str(mismatch), 'trace_factor_match': str(trace_match),
            'eta_U': str(etaU), 'remaining_Rzz_difference': str(leftover),
            'remaining_Rxx_difference': str(left_xx),
            'repaired_kinetic_hessian': str(repaired_kinetic),
            'repaired_clock_cs2': str(repaired_cs2), 'repaired_count': repaired_count,
            'min_cs2': float(repaired_speeds.min()), 'max_cs2': float(repaired_speeds.max()),
            'scope': 'two conserved-source curvature components matched through rate^2; full alpha2,beta uncomputed'},
        'analytic_bounds': {'stationary_y_of_mu_longitudinal': str(critical),
                            'C_ceiling': str(C_ceiling), 'witness_alpha_min': str(alpha_min),
                            'witness_cs2_supremum': str(global_speed_max),
                            'witness_cs2_supremum_float': float(global_speed_max)},
        'zero_field': {'alpha_limit': str(s.limit(at, y, 0, dir='+')),
                       'cs2_limit': str(s.limit(cs2.subs(alpha, at), y, 0, dir='+')),
                       'interpretation': 'zero stiffness; nonlinear well-posedness/strong coupling not certified'},
        'open': ['full covariant Dirac algebra and homogeneous constraints',
                 'PPN beta gamma alpha2 alpha3 and full-background alpha1 validation',
                 'curved-leaf projector, inverse domain and metric variation',
                 'causal response with clock and matter retained',
                 'zero-field strong coupling and regular centers',
                 'cluster, binary and cosmological data comparison',
                 'unscreened exact-AQUAL Solar-System external-field problem'],
        'environment': {'python': platform.python_version(), 'sympy': s.__version__,
                        'numpy': np.__version__, 'lean': shutil.which('lean'),
                        'lake': shutil.which('lake')},
    }


if __name__ == '__main__':
    print(json.dumps(derive(), indent=2, default=str))
