"""Bounded conserved-source response of the flat kinetic-conformal control.

S_g = m/2 int N sqrt(h) [Kij K^ij - K^2/3 + R + 2 f(a_i a^i)].
Here f(0)=0 and alpha=f_s(0) is the constant quadratic coefficient.
This is neither a finite-acceleration-background calculation nor a nonlinear
constraint count.  All inverse Laplacians decay at infinity; wave inverses are
retarded, with no incoming field.  The explicit source is a signed stress
perturbation, not a constructed healthy positive-energy matter realization.
"""
import argparse
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path

import sympy as s


def _zeros(expressions):
    return [s.simplify(value) for value in expressions]


@lru_cache(None)
def derive_action():
    """Derive the quadratic action from actual symmetric metric contractions.

    A real spatial mode with k along z retains both TT polarizations and both
    transverse shifts.  Twice the spatial average fixes the mode normalization.
    The Ricci term is computed from Christoffels, not supplied as a scalar ansatz.
    """
    m, k = s.symbols("m k", positive=True)
    alpha, omega, e, theta = s.symbols("alpha omega e theta", real=True)
    n, zeta, B, Vx, Vy = s.symbols("n zeta B Vx Vy", real=True)
    p, c, pd, cd, zd = s.symbols("p c pd cd zd", real=True)
    rho, rhodot, tau, jx, jy, jz, Txx, Tyy, Txy = s.symbols(
        "rho rhodot tau jx jy jz Txx Tyy Txy", real=True)
    C, S, I = s.cos(theta), s.sin(theta), s.eye(3)
    gamma = s.Matrix([[p, c, 0], [c, -p, 0], [0, 0, 0]])
    gamma_dot = gamma.subs({p: pd, c: cd})

    def trunc(expression):
        expanded = s.expand(expression)
        return sum(expanded.coeff(e, power)*e**power for power in range(3))

    def partial(expression, index):
        return k*s.diff(expression, theta) if index == 2 else s.S.Zero

    def average(expression):
        # At quadratic order this expression is a sum of sin^2 and cos^2.
        return s.simplify(s.integrate(s.expand(expression), (theta, 0, 2*s.pi))/s.pi)

    H1 = (2*zeta*I+gamma)*C
    H2 = (2*zeta**2*I+2*zeta*gamma)*C**2
    h = I+e*H1+e**2*H2
    inverse = I-e*H1+e**2*(H1*H1-H2)
    volume = 1+e*s.trace(H1)/2+e**2*(s.trace(H2)/2
        +s.trace(H1)**2/8-s.trace(H1*H1)/4)
    connection = [[[trunc(sum(inverse[a, d]*(partial(h[d, b], cindex)
        +partial(h[d, cindex], b)-partial(h[b, cindex], d))/2
        for d in range(3))) for cindex in range(3)] for b in range(3)]
        for a in range(3)]
    ricci = s.zeros(3)
    for i in range(3):
        for j in range(3):
            ricci[i, j] = trunc(sum(partial(connection[a][i][j], a)
                -partial(connection[a][i][a], j)
                +sum(connection[a][a][b]*connection[b][i][j]
                     -connection[a][j][b]*connection[b][i][a]
                     for b in range(3)) for a in range(3)))
    curvature_density = trunc((1+e*n*C)*volume*sum(
        inverse[i, j]*ricci[i, j] for i in range(3) for j in range(3)))
    L_R = m*average(curvature_density.coeff(e, 2))/2

    shift = s.Matrix([Vx*S, Vy*S, -k*B*S])
    hdot = (2*zd*I+gamma_dot)*C
    K = s.Matrix(3, 3, lambda i, j:
        (hdot[i, j]-partial(shift[j], i)-partial(shift[i], j))/2)
    L_K = m*average(s.trace(K*K)-s.trace(K)**2/3)/2
    L_a = m*alpha*average(sum(partial(n*C, i)**2 for i in range(3)))

    # Compute delta g_mu_nu T^mu_nu/2, including both off-diagonal entries.
    metric_perturbation = s.zeros(4)
    metric_perturbation[0, 0] = -2*n*C
    for i in range(3):
        metric_perturbation[0, i+1] = shift[i]
        metric_perturbation[i+1, 0] = shift[i]
    metric_perturbation[1:4, 1:4] = H1
    source = s.zeros(4)
    source[0, 0] = rho*C
    for i, current in enumerate([jx, jy, jz]):
        source[0, i+1] = source[i+1, 0] = current*S
    source[1:4, 1:4] = s.Matrix([
        [Txx, Txy, 0], [Txy, Tyy, 0], [0, 0, tau-Txx-Tyy]])*C
    L_source = average(sum(metric_perturbation[i, j]*source[i, j]/2
        for i in range(4) for j in range(4))).subs(jz, -rhodot/k)
    source_control = (-n*rho+zeta*tau+B*rhodot+Vx*jx+Vy*jy
                      +p*(Txx-Tyy)/2+c*Txy)
    L = s.expand(L_K+L_R+L_a+L_source)
    auxiliaries = [n, zeta, B, Vx, Vy]
    variations = [s.diff(L, variable) for variable in auxiliaries]

    # Reclassify the singular branch using the original equations first.
    scalar_hessian = s.hessian(L, [n, zeta])
    alpha_one = {
        "scalar_hessian_determinant": s.factor(scalar_hessian.subs(alpha, 1).det()),
        "compatibility": s.simplify((variations[1]-variations[0]).subs(alpha, 1)),
        "rho": rho, "tau": tau, "regular_solution_inherited": None,
    }
    solution = s.solve(variations, auxiliaries, dict=True)[0]
    # Euler-Lagrange equations for both independent symmetric TT components.
    tensor_frequency_equations = [
        -omega**2*field*s.diff(L, velocity, 2)-s.diff(L, field)
        for field, velocity in [(p, pd), (c, cd)]]
    tensor_solution = s.solve(tensor_frequency_equations, [p, c], dict=True)[0]
    tensor_wave_operator = s.simplify(s.diff(tensor_frequency_equations[0], p)
                                       /s.diff(L, pd, 2))
    return dict(m=m, k=k, alpha=alpha, omega=omega, n=n, zeta=zeta, B=B,
        Vx=Vx, Vy=Vy, p=p, c=c, pd=pd, cd=cd, zd=zd, rho=rho,
        rhodot=rhodot, tau=tau, jx=jx, jy=jy, Txx=Txx, Tyy=Tyy, Txy=Txy,
        L=L, L_R=L_R, L_K=L_K, L_a=L_a, L_source=L_source,
        solution=solution, tensor_solution=tensor_solution,
        scalar_hessian_determinant=s.factor(scalar_hessian.det()),
        curvature_action_residual=s.simplify(L_R-m*k**2*(zeta**2+2*n*zeta
                                                       -(p**2+c**2)/4)),
        source_coupling_residual=s.simplify(L_source-source_control),
        auxiliary_residuals=_zeros(v.subs(solution) for v in variations),
        tensor_frequency_residuals=_zeros(v.subs(tensor_solution)
                                          for v in tensor_frequency_equations),
        tensor_wave_operator=tensor_wave_operator, alpha_one=alpha_one)


def _tidal(metric, derivative):
    """Linear R_0i0j, from the metric, with a fixed Riemann sign convention."""
    return s.Matrix(3, 3, lambda i, j: s.simplify((
        derivative[0]*derivative[i+1]*metric[0, j+1]
        +derivative[0]*derivative[j+1]*metric[0, i+1]
        -derivative[i+1]*derivative[j+1]*metric[0, 0]
        -derivative[0]**2*metric[i+1, j+1])/2))


@lru_cache(None)
def derive_curvature():
    """Check every tidal component for a general conserved Fourier source."""
    a = derive_action()
    m, k, alpha, omega = (a[key] for key in ["m", "k", "alpha", "omega"])
    rho, jx, jy, Txx, Tyy, Txy = (a[key] for key in
                                  ["rho", "jx", "jy", "Txx", "Tyy", "Txy"])
    stress = s.Matrix([[Txx, Txy, omega*jx/k],
        [Txy, Tyy, omega*jy/k], [omega*jx/k, omega*jy/k, omega**2*rho/k**2]])
    upper = s.zeros(4)
    upper[0, 0] = rho
    current = s.Matrix([jx, jy, omega*rho/k])
    upper[0, 1:4] = current.T
    upper[1:4, 0] = current
    upper[1:4, 1:4] = stress
    derivative = s.Matrix([-s.I*omega, 0, 0, s.I*k])
    substitutions = {a["tau"]: s.trace(stress), a["rhodot"]: -s.I*omega*rho}
    auxiliary = {variable: s.simplify(value.subs(substitutions))
                 for variable, value in a["solution"].items()}
    gamma = s.Matrix([[a["p"], a["c"], 0], [a["c"], -a["p"], 0],
                      [0, 0, 0]]).subs(a["tensor_solution"])
    metric = s.zeros(4)
    metric[0, 0] = -2*auxiliary[a["n"]]
    shift = s.Matrix([auxiliary[a["Vx"]], auxiliary[a["Vy"]],
                      s.I*k*auxiliary[a["B"]]])
    metric[0, 1:4] = shift.T
    metric[1:4, 0] = shift
    metric[1:4, 1:4] = 2*auxiliary[a["zeta"]]*s.eye(3)+gamma
    tidal = _tidal(metric, derivative)
    eta = s.diag(-1, 1, 1, 1)
    D = a["tensor_wave_operator"]
    gr_metric = 2/(m*D)*(eta*upper*eta-eta*s.trace(eta*upper)/2)
    gr_tidal = _tidal(gr_metric, derivative)
    extra = (tidal-tidal.subs(alpha, 0)).applyfunc(s.factor)
    extra_n = s.factor(a["solution"][a["n"]]
                       -a["solution"][a["n"]].subs(alpha, 0))
    coefficient = s.simplify(-k**2*extra_n/(rho+a["tau"]))
    wavevector = s.Matrix([0, 0, k])
    expected_extra = coefficient*(rho+s.trace(stress))*(
        wavevector*wavevector.T+omega**2*s.eye(3))/k**2
    extra_zeta = a["solution"][a["zeta"]]-a["solution"][a["zeta"]].subs(alpha, 0)
    return dict(tidal=tidal, gr_tidal=gr_tidal, extra_curvature=extra,
        extra_coefficient=coefficient,
        gr_identity_residuals=_zeros(tidal.subs(alpha, 0)-gr_tidal),
        extra_identity_residuals=_zeros(extra-expected_extra),
        fourier_conservation_residuals=_zeros(upper*derivative),
        extra_zeta_plus_n=s.simplify(extra_n+extra_zeta),
        alpha0_trace_K=s.simplify((-3*s.I*omega*auxiliary[a["zeta"]]
                                  +k**2*auxiliary[a["B"]]).subs(alpha, 0)))


@lru_cache(None)
def derive_fixture():
    """Conserved compact signed source and an off-diagonal exterior witness.

    chi=b(t) g(r), g smooth radial with support r<R and integral Q>0.
    b=exp[-1/(t(2-t))] for 0<t<2 and zero elsewhere.  Q fixes normalization;
    g can be a normalized exp[-1/(1-r^2/R^2)] bump.  No energy condition is
    assumed.  The exterior Newton kernel follows exactly from spherical
    symmetry and Delta[-1/(4 pi r)]=delta^3, not a far-field approximation.
    """
    a, response = derive_action(), derive_curvature()
    t, x, y, z = s.symbols("t x y z", real=True)
    r, Q = s.symbols("r Q", positive=True)
    coordinates = [x, y, z]
    chi = s.Function("chi")(t, x, y, z)
    laplacian = sum(s.diff(chi, coordinate, 2) for coordinate in coordinates)
    rho = laplacian
    current = s.Matrix([-s.diff(chi, t, coordinate) for coordinate in coordinates])
    stress = s.Matrix(3, 3, lambda i, j: s.diff(chi, coordinates[i], coordinates[j])
        +(s.diff(chi, t, 2)-laplacian)*(1 if i == j else 0))
    conservation = [s.diff(rho, t)+sum(s.diff(current[i], coordinates[i])
                                      for i in range(3))]
    conservation += [s.diff(current[i], t)+sum(s.diff(stress[i, j], coordinates[j])
                                             for j in range(3)) for i in range(3)]
    # Independently insert this scalar source into the already derived response.
    chi_hat = s.Symbol("chi_hat")
    k, omega = a["k"], a["omega"]
    fourier_fixture = {a["rho"]: -k**2*chi_hat, a["jx"]: 0, a["jy"]: 0,
        a["Txx"]: (k**2-omega**2)*chi_hat,
        a["Tyy"]: (k**2-omega**2)*chi_hat, a["Txy"]: 0}
    wavevector = s.Matrix([0, 0, k])
    local_gr_curvature = (wavevector*wavevector.T-omega**2*s.eye(3))*chi_hat/(2*a["m"])
    gr_local_residuals = _zeros(response["gr_tidal"].subs(fourier_fixture)-local_gr_curvature)
    vector_tt_residuals = _zeros(expression.subs(fourier_fixture) for expression in
        [a["jx"], a["jy"], a["Txx"]-a["Tyy"], a["Txy"]])
    b = s.exp(-1/(t*(2-t)))
    b_second = s.simplify(s.diff(b, t, 2).subs(t, 1))
    # rho+tau = 3 chi_tt - Delta chi.  The local chi term vanishes outside.
    exterior_delta_n = (response["extra_coefficient"]*3*s.diff(b, t, 2)
                       *(-Q/(4*s.pi*s.sqrt(x*x+y*y+z*z))))
    exterior_tidal_12 = s.factor(s.diff(exterior_delta_n, x, y).subs(
        {t: 1, x: r/s.sqrt(2), y: r/s.sqrt(2), z: 0}))
    half_witness = s.simplify(exterior_tidal_12.subs(
        {a["alpha"]: s.Rational(1, 2), a["m"]: 1, Q: 1, r: 3}))
    return dict(conservation_residuals=_zeros(conservation),
        gr_local_curvature_residuals=gr_local_residuals,
        vector_tt_source_residuals=vector_tt_residuals,
        # Integral Delta chi vanishes for the compact smooth spatial bump.
        alpha_one_integrated_compatibility_at_t1_Q1=s.simplify(3*b_second),
        trace_combination_residual=s.simplify(rho+s.trace(stress)
                                               -3*s.diff(chi, t, 2)+laplacian),
        b_second_at_1=b_second, exterior_tidal_12=exterior_tidal_12,
        half_alpha_witness=half_witness,
        outside_cone_margin=s.Integer(3)-s.Integer(1)-s.Integer(1),
        alpha0_exterior_witness=s.simplify(exterior_tidal_12.subs(a["alpha"], 0)),
        signed_stress_perturbation=True)


@lru_cache(None)
def derive_adaptive_action():
    """Read the actual FLRW seed and change only its stated scalar kernel.

    Canonical matter, alpha=1, Q=-b q^2.  K below labels the derived matter
    kinetic coefficient, not the inverse spatial operator or a DOF count.
    An independently conserved, zero-background external stress couples as
    delta g_mu_nu Sigma^mu_nu/2, with Sigma^0i=a^-2 partial_i J.
    """
    path = Path(__file__).resolve().parents[1]/"vcdm_flrw_gate_2026"/"vcdm_flrw.py"
    spec = importlib.util.spec_from_file_location("adaptive_response_seed", path)
    seed = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(seed)
    d = seed.derive_nonzero_mode()
    m, b, K = s.symbols("m b K_scalar", positive=True)
    rho, p, J = s.symbols("external_rho external_p external_J", real=True)
    n, z, v = d["auxiliaries"]
    a, k, q, u, ud = (d[key] for key in ["a", "k", "q", "u", "ud"])
    original = d["L"].subs({d["M"]**2: m, d["alpha"]: 1, d["Z"]: 1, d["D"]: 1})
    L = original-m*k**2*(z+n)**2/a**2-b*q**2*(z+n)**2
    delta_metric = s.diag(-2*n, 2*a*a*z, 2*a*a*z, 2*a*a*z)
    delta_metric[0, 1] = delta_metric[1, 0] = a*a*v
    external = s.diag(rho, p/a**2, p/a**2, p/a**2)
    external[0, 1] = external[1, 0] = -k*J/a**2
    # Matching real-mode amplitudes: diagonal cos^2 and shift sin^2 both
    # have twice their spatial average equal to one.
    coupling = s.simplify(sum(delta_metric[i, j]*external[i, j]/2
                              for i in range(4) for j in range(4)))
    L = s.expand(L+coupling)
    variations = [s.diff(L, variable) for variable in (n, z, v)]
    solution_b = s.solve(variations, (n, z, v), dict=True)[0]
    reduced_b = s.factor(L.subs(solution_b))
    kinetic = s.factor(s.diff(reduced_b, ud, 2))
    b_of_K = s.solve(kinetic-K, b)[0]
    solution = {key: s.factor(value.subs(b, b_of_K)) for key, value in solution_b.items()}
    reduced = s.factor(reduced_b.subs(b, b_of_K))
    t = s.Symbol("t", positive=True)
    ut, rt, pt, jt = [s.Function(name)(t) for name in ["u", "R", "P", "j"]]
    C0 = s.sqrt(2*m/3)
    full_time_L = t*reduced.subs({a: t**s.Rational(1, 3), q: C0/t,
        u: ut, ud: s.diff(ut, t), rho: rt, p: pt, J: jt})
    equation = s.simplify((s.diff(s.diff(full_time_L, s.diff(ut, t)), t)
                           -s.diff(full_time_L, ut))/(t*K))
    return dict(m=m, b=b, K=K, a=a, k=k, q=q, u=u, ud=ud, n=n, z=z, v=v,
        rho=rho, p=p, J=J, t=t, ut=ut, rt=rt, pt=pt, jt=jt, C0=C0,
        kinetic=kinetic, b_of_K=b_of_K, L=L, reduced_L=reduced,
        solution=solution, field_equation=equation,
        free_local_weyl_velocity_coefficient=s.factor(q*s.diff(solution[n]-solution[z], ud)),
        # beta=-v/k in the seed's real-mode shift convention; k^-2=-Delta^-1.
        exterior_weyl_inverse_coefficient=s.factor(-k**2*s.diff(-solution[v]/k, u)/(2*q)),
        source_coupling_residual=s.simplify(coupling-(-n*rho+3*z*p-k*v*J)),
        auxiliary_residuals=_zeros(value.subs(solution_b) for value in variations),
        seed_path=str(path), seed_sha256=hashlib.sha256(path.read_bytes()).hexdigest())


@lru_cache(None)
def derive_adaptive_weyl():
    """Derive all nine conformal electric-Weyl entries and slicing invariance."""
    omega, k, n, z, B = s.symbols("omega k n z B", real=True)
    eta = s.diag(-1, 1, 1, 1)
    derivative = s.Matrix([-s.I*omega, s.I*k, 0, 0])
    perturbation = s.diag(-2*n, 2*z, 2*z, 2*z)
    perturbation[0, 1] = perturbation[1, 0] = s.I*k*B
    trace = s.trace(eta*perturbation)
    box = (derivative.T*eta*derivative)[0]
    raised = eta*perturbation
    ricci = s.Matrix(4, 4, lambda i, j: s.simplify((sum(
        derivative[ell]*derivative[i]*raised[ell, j]
        +derivative[ell]*derivative[j]*raised[ell, i] for ell in range(4))
        -box*perturbation[i, j]-derivative[i]*derivative[j]*trace)/2))
    weyl = _tidal(perturbation, derivative)+ricci[1:4, 1:4]/2
    weyl -= s.eye(3)*(ricci[0, 0]/2+s.trace(eta*ricci)/6)
    wavevector = s.Matrix([k, 0, 0])
    expected = -(wavevector*wavevector.T-s.eye(3)*k*k/3)*(n-z-s.I*omega*B)/2
    t = s.Symbol("t", positive=True)
    scale, shift_time = s.Function("a")(t), s.Function("T_shift")(t)
    H = s.diff(scale, t)/scale
    # B=a beta, B'=a^2(beta_dot+H beta).  Four orthonormal legs and
    # conformal covariance of all-lowered Weyl supply the overall a^-2.
    slicing = -s.diff(shift_time, t)+H*shift_time+scale**2*(
        s.diff(shift_time/scale**2, t)+H*shift_time/scale**2)
    return dict(fourier_weyl_residuals=_zeros(weyl-expected),
        slicing_variation=s.simplify(slicing),
        formula="Ehat_ij=(2a^2)^-1 D_ij[n-z+a^2(beta_dot+H beta)]")


@lru_cache(None)
def derive_adaptive_fixture():
    """Exact retarded, mean-zero dipole witness on the actual stiff background.

    The physical profile is g=partial_x eta, not eta: eta is radial, smooth,
    supported r<1, with integral one.  Thus every physical source has zero
    mean.  u=partial_x u0 by uniqueness of the local sourced matter equation.
    Integrating the auxiliary radial packet u0 is not assigning an equation
    to a homogeneous physical mode.  Spatial inverses decay on R^3.

    j=exp[-1/(t-1)^2] for 1<t<=3/2, zero before t=1; a smooth cutoff can be
    placed after t=2.  R and C are retarded integrals, not independent initial
    data.  Sigma may persist later in time but stays compact in space.
    """
    d = derive_adaptive_action()
    t, K, m, k = (d[key] for key in ["t", "K", "m", "k"])
    a = t**s.Rational(1, 3)
    x, y, z = s.symbols("x y z", real=True)
    coordinates = [t, x, y, z]
    spatial = coordinates[1:]
    eta = s.Function("eta")(x, y, z)
    g = s.diff(eta, x)
    lap_g = sum(s.diff(g, coordinate, 2) for coordinate in spatial)
    j, R = d["jt"], d["rt"]
    C = s.Function("C_spatial")(t)
    P = -s.diff(j, t)-j/t
    source = s.zeros(4)
    source[0, 0] = R*g+C*lap_g
    for i in range(3):
        source[0, i+1] = source[i+1, 0] = j*s.diff(g, spatial[i])/a**2
        source[i+1, i+1] = P*g/a**2
    background = s.diag(-1, a*a, a*a, a*a)
    inverse = background.inv()
    connection = [[[s.simplify(sum(inverse[i, ell]*(
        s.diff(background[ell, b], coordinates[c])+s.diff(background[ell, c], coordinates[b])
        -s.diff(background[b, c], coordinates[ell]))/2 for ell in range(4)))
        for c in range(4)] for b in range(4)] for i in range(4)]
    ward = [sum(s.diff(source[mu, nu], coordinates[mu])
        +sum(connection[mu][mu][ell]*source[ell, nu]
             +connection[nu][mu][ell]*source[mu, ell] for ell in range(4))
        for mu in range(4)) for nu in range(4)]
    source_odes = {s.diff(R, t): -(R+P)/t,
                   s.diff(C, t): -C/t-j/a**2}
    ward_residuals = _zeros(value.subs(source_odes) for value in ward)

    V, W = s.Function("V_radial_moment")(t), s.Function("W")(t)
    # Integral Delta u0=0 is the divergence theorem for the finite-propagation
    # radial packet; the physical field is its spatial derivative, mean zero.
    moment_equation = s.simplify(d["C0"]*d["field_equation"].subs(
        {d["ut"]: V/d["C0"], d["pt"]: P, k: 0}).doit().subs(source_odes))
    operator = lambda f: s.diff(f, t, 2)+s.diff(f, t)/t+f/(K*t*t)
    moment_source = s.simplify(operator(V)-moment_equation)
    control_source = ((K+3)*t*s.diff(j, t, 2)+(3*K+13)*s.diff(j, t)
                      +(K+8)*j/t+4*R)/K
    c = s.simplify(s.diff(moment_source, s.diff(j, t, 2))/t)
    remainder_source = s.simplify(moment_source-operator(c*t*j))
    control_remainder = 4*s.diff(j, t)/K+(4*K-3)*j/(K*K*t)+4*R/K
    # Exterior beta depends on q u-J.  Its Weyl combination is not beta alone.
    q = d["C0"]/t
    F = s.simplify(s.diff(q*V/d["C0"]-j, t)+(q*V/d["C0"]-j)/(3*t))
    split_F = s.expand(F.subs(V, c*t*j+W).doit())
    contact = s.simplify(s.diff(split_F, s.diff(j, t)))
    st = s.Symbol("source_time", positive=True)
    green = s.sqrt(K)*st*s.sin(s.log(t/st)/s.sqrt(K))
    weyl_kernel = s.simplify(s.diff(green, t)/t-2*green/(3*t*t))

    # On 1<=source_time<=t<=3/2, 0<=log(t/source_time)<1/2.
    # cos(theta)>=1-theta^2/2 and sin(theta)<=theta give this exact
    # lower bound on the Weyl kernel's bracket; its prefactor st/t^2>0.
    bracket_lower = 1-s.Rational(1, 2)**2/(2*K)-s.Rational(2, 3)*s.Rational(1, 2)
    remainder_weights = [s.simplify(s.diff(remainder_source, s.diff(j, t))),
        s.simplify(t*s.diff(remainder_source, j)), s.simplify(s.diff(remainder_source, R))]
    pulse = s.exp(-1/(t-1)**2)
    t_event, r_event = s.Rational(3, 2), s.Integer(3)
    F_lower = s.simplify(contact*s.diff(pulse, t).subs(t, t_event))
    amplitude, radius = s.symbols("F_amplitude radius", real=True, positive=True)
    dipole_inverse = s.diff(-amplitude/(4*s.pi*s.sqrt(x*x+y*y+z*z)), x)
    Dxx = s.diff(dipole_inverse, x, 2)-sum(s.diff(dipole_inverse, coordinate, 2)
                                          for coordinate in spatial)/3
    Eaxis = s.simplify((d["exterior_weyl_inverse_coefficient"]*Dxx).subs(
        {x: radius, y: 0, z: 0}))
    E_control = -9*amplitude/(8*s.pi*m*radius**4)
    lower_E = s.simplify(abs(s.diff(Eaxis, amplitude)).subs(
        {radius: r_event, m: 1})*F_lower.subs(K, 9))
    general_lower_E = s.simplify(abs(s.diff(Eaxis, amplitude)).subs(radius, r_event)*F_lower)
    excess = s.Symbol("w_nonnegative", nonnegative=True)
    family_certificates = [s.factor(value.subs(K, 1+excess))
                           for value in [bracket_lower, contact]+remainder_weights]
    speed2 = s.simplify(t**s.Rational(2, 3)*s.diff(d["field_equation"], k, 2)/(2*d["ut"]))
    speed_gap = s.factor((1-speed2).subs(K, 1+excess))
    # Scalar sources cannot hide a transverse-current or TT-stress channel.
    kx, ky, kz, phat, jhat = s.symbols("kx ky kz phat jhat", real=True)
    wavevector = s.Matrix([kx, ky, kz])
    transverse = s.eye(3)-wavevector*wavevector.T/(wavevector.dot(wavevector))
    isotropic_stress = phat*s.eye(3)
    tt_stress = transverse*isotropic_stress*transverse
    tt_stress -= transverse*s.trace(transverse*isotropic_stress)/2
    projections = _zeros(transverse*(jhat*wavevector))+_zeros(tt_stress)
    light_radius = s.integrate(t**(-s.Rational(1, 3)), (t, 1, t_event))
    zero_source = {d["u"]: 0, d["ud"]: 0, d["rho"]: 0, d["p"]: 0, d["J"]: 0}
    kx, eta_hat = s.symbols("kx eta_hat")
    return dict(K=K, m=m, t=t, moment_source=moment_source, remainder_source=remainder_source,
        green=green, weyl_kernel=weyl_kernel, exterior_time_amplitude=F,
        exterior_time_contact_decomposition=split_F,
        weyl_contact_coefficient=contact,
        free_local_weyl_velocity_coefficient=d["free_local_weyl_velocity_coefficient"],
        ward_residuals=ward_residuals,
        zero_mean_profile_symbol=(s.I*kx*eta_hat).subs(kx, 0),
        source_onset_jets=[s.limit(s.diff(pulse, t, order), t, 1, dir="+")
                          for order in range(4)],
        initial_constraint_fields=_zeros(value.subs(zero_source) for value in d["solution"].values()),
        green_ode_residual=s.simplify(operator(green)),
        green_initial_value=s.simplify(green.subs(t, st)),
        green_initial_slope=s.simplify(s.diff(green, t).subs(t, st)),
        moment_equation_residual=s.simplify(moment_source-control_source),
        contact_subtraction_residual=s.simplify(remainder_source-control_remainder),
        k9_kernel_bracket_lower_bound=s.simplify(bracket_lower.subs(K, 9)),
        k9_remainder_weights=[value.subs(K, 9) for value in remainder_weights],
        k9_time_amplitude_lower_bound=s.simplify(F_lower.subs(K, 9)),
        k9_exterior_abs_lower_bound=lower_E,
        general_exterior_abs_lower_bound=general_lower_E,
        general_time_amplitude_lower_bound=F_lower,
        family_positive_certificates=family_certificates,
        family_metric_speed_gap=speed_gap, matter_speed_squared=speed2,
        scalar_vector_tt_projection_residuals=projections,
        dipole_weyl_on_axis=Eaxis,
        dipole_weyl_geometry_residual=s.simplify(Eaxis-E_control),
        outside_cone_margin=s.simplify(r_event-1-light_radius),
        outside_metric_light_cone=bool(r_event-1-light_radius > 0))


def adaptive_run():
    d, w, f = derive_adaptive_action(), derive_adaptive_weyl(), derive_adaptive_fixture()
    residuals = d["auxiliary_residuals"]+w["fourier_weyl_residuals"]+f["ward_residuals"]
    residuals += f["source_onset_jets"]+f["initial_constraint_fields"]
    residuals += f["scalar_vector_tt_projection_residuals"]
    residuals += [d["source_coupling_residual"], w["slicing_variation"],
        f["zero_mean_profile_symbol"], f["green_ode_residual"], f["green_initial_value"],
        f["green_initial_slope"]-1, f["moment_equation_residual"],
        f["contact_subtraction_residual"], f["dipole_weyl_geometry_residual"]]
    checked = all(value == 0 for value in residuals)
    positive = all(bool(value > 0) for value in f["k9_remainder_weights"]
                   +[f["k9_kernel_bracket_lower_bound"], f["k9_exterior_abs_lower_bound"]])
    detected = checked and positive and f["outside_metric_light_cone"]
    family_detected = (checked and f["outside_metric_light_cone"]
        and all(value.is_positive is True for value in f["family_positive_certificates"])
        and f["family_metric_speed_gap"].is_nonnegative is True)
    return {
        "checks_passed": checked, "causal_response_gate": "FAIL" if detected else "INCONCLUSIVE",
        "scope": "Actual stiff FLRW, canonical matter, alpha=1, Q=-b q^2; linear external response.",
        "derived_kinetic": str(d["kinetic"]), "b_of_K": str(d["b_of_K"]),
        "gate_fixture_K": 9, "gate_fixture_b": str(d["b_of_K"].subs(d["K"], 9)),
        "seed_path": d["seed_path"], "seed_sha256": d["seed_sha256"],
        "auxiliary_solution": {str(key): str(value) for key, value in d["solution"].items()},
        "reduced_action": str(d["reduced_L"]), "stiff_field_equation": str(d["field_equation"]),
        "electric_weyl": w["formula"],
        "weyl_identity_residuals": [str(value) for value in w["fourier_weyl_residuals"]],
        "source": "g=partial_x eta; J=j g; p=-(j_dot+j/t)g; rho=R g+C Delta g",
        "source_odes": "R_dot+(R+p_coefficient)/t=0; C_dot+C/t=-j/t^(2/3)",
        "source_retarded_integrals": "R=j/t+t^-1 int_1^t j(s)/s ds; C=-t^-1 int_1^t s^(1/3)j(s) ds",
        "source_pulse": "j=0 before t=1; exp[-1/(t-1)^2] through t=3/2; optional smooth cutoff after t=2",
        "spatial_profile": "eta smooth radial supported r<1, integral 1; g=partial_x eta has mean zero",
        "ward_residuals": [str(value) for value in f["ward_residuals"]],
        "retarded_green": str(f["green"]), "retarded_green_jump": ["0", "1"],
        "radial_moment_scope": "u=partial_x u0; V=sqrt(2m/3) int u0. This is not a homogeneous physical mode.",
        "moment_source": str(f["moment_source"]), "remainder_source": str(f["remainder_source"]),
        "weyl_contact_decomposition": str(f["exterior_time_contact_decomposition"]),
        "derived_contact_coefficient": str(f["weyl_contact_coefficient"]),
        "k9_contact_coefficient": str(f["weyl_contact_coefficient"].subs(f["K"], 9)),
        "kernel_positivity_proof": "log(t/s)<1/2; cos(theta)>=1-theta^2/2; sin(theta)<=theta; R,j,j_dot positive",
        "k9_kernel_bracket_lower_bound": str(f["k9_kernel_bracket_lower_bound"]),
        "event": "t=3/2, x=3, y=z=0, m=1; source begins t=1 in r<1",
        "outside_cone_margin": str(f["outside_cone_margin"]),
        "k9_strict_abs_Ehat_xx_lower_bound": str(f["k9_exterior_abs_lower_bound"]),
        "finite_subluminal_family": {
            "conditions": "Every finite K>=1 and m>0 on the same canonical stiff background; same signed external probe.",
            "causal_response_gate": "FAIL" if family_detected else "INCONCLUSIVE",
            "strict_time_amplitude_lower_bound": str(f["general_time_amplitude_lower_bound"]),
            "strict_abs_Ehat_xx_lower_bound_at_r3": str(f["general_exterior_abs_lower_bound"]),
            "positive_certificates_K_equals_1_plus_w": [str(value) for value in f["family_positive_certificates"]],
            "matter_speed_squared": str(f["matter_speed_squared"]),
            "metric_speed_gap_K_equals_1_plus_w": str(f["family_metric_speed_gap"]),
            "infinite_K_limit_claimed": False,
        },
        "scalar_vector_tt_projection_residuals": [str(value) for value in f["scalar_vector_tt_projection_residuals"]],
        "no_incoming_completion": "On isotropic FLRW the linear scalar, vector, and TT sectors separate. Longitudinal current and isotropic stress have zero transverse and TT projections. Choose the source-free vector/TT solutions zero; retarded scalar matter and reconstructed auxiliaries vanish before t=1. No initial constrained tails are used.",
        "dipole_exterior_Ehat_xx": str(f["dipole_weyl_on_axis"]),
        "preexisting_constraint_tail_used": False,
        "initial_data": "All source and matter/metric perturbations zero for t<=1; retarded solution only.",
        "healthy_positive_energy_matter_realization_claimed": False,
        "nonlinear_causality_or_matter_realizability_theorem_claimed": False,
        "boundary_scope": "R^3 spatial decay, physical mean-zero dipole; compact-torus image kernels not evaluated.",
        "interpretation": "Failure of metric-light-cone support for this conserved signed external source, not a universal realizable-matter theorem.",
    }


def run():
    """JSON-safe evidence; an execution success is not a causal-gate success."""
    a, c, f = derive_action(), derive_curvature(), derive_fixture()
    residuals = (a["auxiliary_residuals"]+a["tensor_frequency_residuals"]
        +c["gr_identity_residuals"]+c["extra_identity_residuals"]
        +c["fourier_conservation_residuals"]+f["conservation_residuals"]
        +f["gr_local_curvature_residuals"]+f["vector_tt_source_residuals"]
        +[a["curvature_action_residual"], a["source_coupling_residual"],
          c["alpha0_trace_K"], c["extra_zeta_plus_n"], f["trace_combination_residual"]])
    checks_passed = all(value == 0 for value in residuals)
    witness = f["half_alpha_witness"]
    detected = checks_passed and witness.is_zero is False and bool(f["outside_cone_margin"] > 0)
    return {
        "adaptive_response": adaptive_run(),
        "name": "flat_kinetic_conformal_conserved_source_response",
        "sympy_version": s.__version__, "checks_passed": checks_passed,
        "causal_response_gate": "FAIL" if detected else "INCONCLUSIVE",
        "causal_gate_evaluated_at_alpha": "1/2",
        "scope": "Flat f(0)=0; constant alpha=f_s(0); m>0; k!=0; linear response.",
        "boundary_conditions": "Spatial decay; retarded tensor inverse; no incoming fields.",
        "finite_acceleration_background_claimed": False,
        "full_nonlinear_constraint_count_claimed": False,
        "healthy_positive_energy_matter_realization_claimed": False,
        "quadratic_action": str(a["L"]),
        "auxiliary_response": {str(key): str(value) for key, value in a["solution"].items()},
        "tensor_response": {str(key): str(value) for key, value in a["tensor_solution"].items()},
        "retarded_tensor_denominator": "k^2-(omega+i0)^2",
        "all_nine_gr_alpha0_residuals": [str(value) for value in c["gr_identity_residuals"]],
        "all_nine_extra_curvature_residuals": [str(value) for value in c["extra_identity_residuals"]],
        "extra_curvature_position_space":
            "alpha/[2m(1-alpha)] (partial_i partial_j + delta_ij partial_t^2) Delta^-1(rho+tau)",
        "derived_extra_coefficient": str(c["extra_coefficient"]),
        "alpha_zero_control": "All nine R_0i0j equal causal GR; trace K=0 in this slicing.",
        "alpha_one": {
            "scalar_hessian_determinant": str(a["alpha_one"]["scalar_hessian_determinant"]),
            "compatibility": str(a["alpha_one"]["compatibility"])+" = 0",
            "regular_solution_inherited": None,
            "interpretation": "Separate singular source-compatibility branch, not a regular response."},
        "fixture": {
            "definition": "T^munu=(partial^mu partial^nu-eta^munu Box) chi; chi=b(t)g(r)",
            "support": "0<t<2, r<1; smooth normalized radial g with integral Q=1",
            "signed_stress_perturbation": f["signed_stress_perturbation"],
            "conservation_residuals": [str(value) for value in f["conservation_residuals"]],
            "gr_local_curvature": "(delta_ij chi_tt - partial_i partial_j chi)/(2m)",
            "gr_local_curvature_residuals": [str(value) for value in f["gr_local_curvature_residuals"]],
            "vector_tt_source_residuals": [str(value) for value in f["vector_tt_source_residuals"]],
            "alpha_one_integrated_compatibility_at_t1_Q1":
                str(f["alpha_one_integrated_compatibility_at_t1_Q1"]),
            "event": "t=1, x=y=3/sqrt(2), z=0; m=1, alpha=1/2",
            "outside_cone_margin": str(f["outside_cone_margin"]),
            "R_0102": str(witness), "alpha0_R_0102": str(f["alpha0_exterior_witness"]),
            "general_exterior_R_0102_at_t1": str(f["exterior_tidal_12"]),
            "amplitude": "An arbitrary small overall source amplitude multiplies this response."},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-causal-response", action="store_true")
    parser.add_argument("--require-adaptive-causal-response", action="store_true")
    args = parser.parse_args(argv)
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["checks_passed"] or not result["adaptive_response"]["checks_passed"]:
        return 1
    if args.require_adaptive_causal_response and result["adaptive_response"]["causal_response_gate"] != "PASS":
        return 2
    return 2 if args.require_causal_response and result["causal_response_gate"] != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
