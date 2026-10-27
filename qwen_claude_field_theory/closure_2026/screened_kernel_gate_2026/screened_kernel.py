"""Bounded screen of one new scalar kernel, not a completed nonlinear theory.

The raw canonical scalar action is changed BEFORE eliminating auxiliaries.
Q=-b q^2 m kappa^2/(m kappa^2+b q^2), K0=9/(2b)-15>0.
The screened inverse cancels the ud/k^2 electric-Weyl coefficient; the
remaining H*u/k^2 contribution is H*KTF and is local in canonical data.
Only K0=3 (b=1/4) cancels the frozen dispersion pole. On expanding FLRW
that choice still has a Yukawa-dependent kinetic drift.

The witness uses u(t0)=epsilon Delta g, ud(t0)=0, with a smooth positive
radial g supported in 1<r<2. All original linear metric/matter canonical
initial data are local derivatives of g, and agree with background in r<1.
The initial second derivative of the gauge-invariant relational kinetic
density delta X-Xbar_dot*u/q is strictly negative at the origin. This is
incompatible with metric-cone support of a regular linear Cauchy flow.
It is not a zero-past actuator, a nonlinear initial-data lift, an exact k=0
calculation, or a gravitational constraint count. R^3 decay is essential.
"""
import argparse
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[1]
INPUTS = [ROOT/"vcdm_flrw_gate_2026/vcdm_flrw.py",
          ROOT/"constraint_response_gate_2026/adaptive_endpoint.py",
          ROOT/"positive_lambda_response_2026/physical_initial_data.py"]


@lru_cache(None)
def _module(index):
    spec = importlib.util.spec_from_file_location("screened_input_"+str(index), INPUTS[index])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _zero(expression):
    return s.factor(s.simplify(expression))


@lru_cache(None)
def derive_action():
    seed = _module(0).derive_nonzero_mode()
    a, k, q, u, ud = (seed[key] for key in ("a", "k", "q", "u", "ud"))
    n, z, v = seed["auxiliaries"]
    m, b, K0, H = s.symbols("m b K0 H", positive=True)
    udd = s.Symbol("udd", real=True)
    p = k*k/(a*a)
    mass2 = 3*q*q/(2*m)
    b_of_K0 = s.solve(s.Rational(9, 2)/b-15-K0, b)[0]
    Q = -b*q*q*m*p/(m*p+b*q*q)
    original = seed["L"].subs({seed["M"]**2: m, seed["alpha"]: 1, seed["Z"]: 1, seed["D"]: 1})
    modified = original-m*p*(z+n)**2+Q*(z+n)**2
    L = s.factor(modified.subs(b, b_of_K0))
    equations = [s.diff(L, field) for field in (n, z, v)]
    solution = s.solve(equations, (n, z, v), dict=True)[0]
    solution = {key: s.factor(value) for key, value in solution.items()}
    reduced = s.factor(L.subs(solution))
    kinetic = s.factor(s.diff(reduced, ud, 2))
    gradient = s.factor(-s.diff(reduced, u, 2))
    kinetic_drift = s.factor(a*H*s.diff(kinetic, a)-3*H*q*s.diff(kinetic, q))
    friction = s.factor(3*H+kinetic_drift/kinetic)
    frequency2 = s.factor(gradient/kinetic)
    acceleration = -friction*ud-frequency2*u
    t = s.Symbol("time", positive=True)
    at, qt, ut = [s.Function(name)(t) for name in ("a_time", "q_time", "u_time")]
    full_time_L = at**3*reduced.subs({a: at, q: qt, u: ut, ud: s.diff(ut, t)})
    actual_EL = (s.diff(s.diff(full_time_L, s.diff(ut, t)), t)-s.diff(full_time_L, ut))/at**3
    actual_EL = actual_EL.subs({s.diff(at, t): H*at, s.diff(qt, t): -3*H*qt})
    actual_EL = s.factor(actual_EL.subs({at: a, qt: q, ut: u,
        s.diff(ut, t): ud, s.diff(ut, t, 2): udd}, simultaneous=True))
    evolution = kinetic*udd+(3*H*kinetic+kinetic_drift)*ud+gradient*u
    ps, mu2 = s.symbols("kappa_squared mu_squared", positive=True)
    frozen = s.factor(frequency2.subs({k*k: a*a*ps, q*q: 2*m*mu2/3}, simultaneous=True))
    pole = -3*mu2/K0
    residue = s.factor(s.limit((ps-pole)*frozen, ps, pole))
    cancellations = s.solve(residue, K0)
    cancellation_b = [s.simplify(b_of_K0.subs(K0, value)) for value in cancellations]
    selected_drag = s.factor(friction.subs(K0, 3))
    drag_symbol = s.factor(selected_drag.subs({k*k: a*a*ps, q*q: 2*m*mu2/3}, simultaneous=True))
    return dict(a=a, k=k, q=q, m=m, b=b, K0=K0, H=H, u=u, ud=ud, udd=udd,
        n=n, z=z, v=v, Qscreen=Q, b_of_K0=b_of_K0, mass2=mass2,
        L=L, reduced_L=reduced, solution=solution, kinetic=kinetic, gradient=gradient,
        kinetic_drift=kinetic_drift, friction=friction, frequency_squared=frequency2,
        acceleration=acceleration, actual_time_EL=actual_EL, evolution_equation=evolution,
        constraint_residuals=[_zero(eq.subs(solution)) for eq in equations],
        time_EL_residual=_zero(actual_EL-evolution), seed_residuals=[seed["boundary_residual"], seed["background_tadpole_residual"]],
        kappa_squared_symbol=ps, mu2_symbol=mu2, frozen_dispersion=frozen,
        frozen_pole=pole, frozen_pole_residue=residue, frozen_cancellation_K0=cancellations,
        frozen_cancellation_b=cancellation_b,
        selected_speed_squared=s.factor(frozen.subs(K0, 3)/ps),
        selected_drag=selected_drag, selected_drag_symbol=drag_symbol,
        selected_drag_residual=_zero(drag_symbol-H*(3*ps-mu2)/(ps+mu2)),
        selected_drag_pole_residue=s.factor(s.limit((ps+mu2)*drag_symbol, ps, -mu2)))


def _time_derivative(expression, d):
    rates = {d["a"]: d["a"]*d["H"], d["q"]: -3*d["H"]*d["q"],
             d["H"]: -d["q"]**2/(2*d["m"]), d["u"]: d["ud"],
             d["ud"]: d["acceleration"]}
    return s.factor(sum(s.diff(expression, variable)*rate for variable, rate in rates.items()))


@lru_cache(None)
def derive_geometry():
    d = derive_action()
    a, k, q, m, H, u, ud, udd, K0 = (d[key] for key in ("a", "k", "q", "m", "H", "u", "ud", "udd", "K0"))
    n, z, v = (d[key] for key in ("n", "z", "v"))
    solution = d["solution"]
    dt = lambda expression: _time_derivative(expression, d)
    B, zd = s.factor(-solution[v]/k), dt(solution[z])
    nd, Bd = dt(solution[n]), dt(B)
    epsilon, theta = s.symbols("epsilon theta", real=True)
    scale = a*a*s.exp(2*epsilon*z*s.cos(theta))
    lapse, shift = 1+epsilon*n*s.cos(theta), epsilon*v*s.sin(theta)
    zd_raw = s.Symbol("zd_raw", real=True)
    metric_dot = 2*(H+epsilon*zd_raw*s.cos(theta))*scale
    Kraw = s.diag(*[(metric_dot-shift*k*s.diff(scale, theta)
        -(2*scale*k*s.diff(shift, theta) if i == 0 else 0))/(2*lapse*scale) for i in range(3)])
    Kvariation = Kraw.applyfunc(lambda value: s.simplify(s.diff(value, epsilon).subs(epsilon, 0)/s.cos(theta)))
    Kvariation = Kvariation.subs(solution).subs(zd_raw, zd).applyfunc(s.factor)
    Ktrace = s.factor(s.trace(Kvariation))
    KTF = (Kvariation-s.eye(3)*Ktrace/3).applyfunc(s.factor)
    raw_p = a**3*s.exp(3*epsilon*z)*(q+epsilon*ud)/(1+epsilon*n)
    matter_p = s.factor(s.diff(raw_p, epsilon).subs(epsilon, 0).subs(solution))
    tau = s.Symbol("tau", real=True)
    # Exact trace-constrained Legendre relation: pi^i_j=m sqrt(h) KTF^i_j/2
    # +sqrt(h) tau delta^i_j/3. The spatial-potential replacement has no velocities.
    gravity_p = (m*a**3*KTF/2+a**3*tau*solution[z]*s.eye(3)).applyfunc(s.factor)

    geometry = _module(1).derive_connection()
    gt = geometry["t"]
    jet = {geometry["a"]: a, s.diff(geometry["a"], gt): a*H,
           geometry["k"]: k, geometry["n"]: solution[n], geometry["z"]: solution[z],
           geometry["v"]: solution[v], s.diff(geometry["v"], gt): dt(solution[v]),
           s.diff(geometry["n"], gt): nd, s.diff(geometry["z"], gt): zd}
    Eparallel = s.factor(geometry["Weyl_parallel"].subs(jet, simultaneous=True))
    canonical_E = H*KTF[0, 0]-(9-K0)*k*k*ud/(9*a*a*q)
    # A general inverse-Q ansatz exposes the cancellation condition itself.
    A0, A1 = s.symbols("inverse_Q_local inverse_Q_inverse_laplacian", real=True)
    general_Q_inverse = A0/(q*q)+A1*a*a/(m*k*k)
    unscreened_z = -4*ud/q-3*q*ud*general_Q_inverse/2
    general_jet = dict(jet, **{})
    general_jet[geometry["z"]] = unscreened_z
    E_general = s.factor(geometry["Weyl_parallel"].subs(general_jet, simultaneous=True))
    # Divide by D_xx=-2k^2/3: the k-independent part of E/ud is the inverse pole.
    velocity_part = s.diff(E_general, ud)
    inverse_coefficient = s.simplify(velocity_part.subs(k, 0))
    required_A1 = s.solve(inverse_coefficient, A1)

    ward = _module(2).derive_stress_ward()
    wt = ward["t"]
    to_functions = {a: ward["a"], q: ward["q"], u: ward["u"], ud: s.diff(ward["u"], wt)}
    kg = ward["physical_Klein_Gordon_equation"].subs({ward["n"]: solution[n].subs(to_functions),
        ward["z"]: solution[z].subs(to_functions), ward["B"]: B.subs(to_functions)}).doit()
    kg = kg.subs(s.diff(ward["q"], wt), -3*ward["H"]*ward["q"])
    kg = kg.subs({s.diff(ward["a"], wt): a*H, ward["a"]: a, ward["q"]: q,
        ward["u"]: u, s.diff(ward["u"], wt): ud, s.diff(ward["u"], wt, 2): udd}, simultaneous=True)
    density = s.factor(q*(ud-q*solution[n]))
    relational = density+3*H*q*u
    T, Td = s.symbols("time_shift time_shift_dot", real=True)
    gauge_delta_X = q*((3*H*q*T-q*Td)-q*(-Td))
    relational_gauge = s.simplify(gauge_delta_X+3*H*q*(-q*T))

    # Construct the position-space initial data first; check their mode symbols
    # against the actual auxiliary and ADM/momentum equations above.
    x, y, zc = s.symbols("initial_x initial_y initial_z", real=True)
    coordinates = (x, y, zc)
    g = s.Function("annular_g")(*coordinates)
    eps = s.Symbol("amplitude", positive=True)
    lap = lambda value: sum(s.diff(value, coordinate, 2) for coordinate in coordinates)
    Dg = s.Matrix(3, 3, lambda i, j: s.diff(g, coordinates[i], coordinates[j])
                   -(lap(g)/3 if i == j else 0))
    u_initial = eps*lap(g)
    B_initial = -3*q*eps*g/(2*m)
    z_dot_initial = eps*(2*lap(lap(g))/(3*a*a*q)-d["mass2"]*lap(g)/(3*q))
    KTF_initial = 3*q*eps*Dg/(2*m)
    Ktrace_initial = 2*eps*lap(lap(g))/(a*a*q)
    local_fields = dict(scalar_field=u_initial, scalar_velocity=s.S.Zero,
        lapse=s.S.Zero, lapse_velocity=4*eps*lap(lap(g))/(3*a*a*q),
        spatial_conformal_metric=s.S.Zero, spatial_metric=s.zeros(3),
        spatial_conformal_velocity=z_dot_initial, spatial_metric_velocity=2*a*a*z_dot_initial*s.eye(3),
        shift_potential=B_initial, shift=s.Matrix([s.diff(B_initial, coord) for coord in coordinates]),
        shift_potential_velocity=-3*H*B_initial,
        extrinsic_curvature=KTF_initial+s.eye(3)*Ktrace_initial/3,
        extrinsic_trace=Ktrace_initial, gravity_tracefree_momentum=m*a**3*KTF_initial/2,
        gravity_trace_momentum=s.S.Zero, matter_momentum=s.S.Zero)
    ghat = s.Symbol("g_hat", real=True)
    mode = s.exp(s.I*k*x)
    mode_of = lambda value: s.simplify(value.subs(g, ghat*mode).doit()/mode)
    initial_mode = {K0: 3, u: -eps*k*k*ghat, ud: 0}
    pairs = [(local_fields["lapse"], solution[n]), (local_fields["lapse_velocity"], nd),
        (local_fields["spatial_conformal_metric"], solution[z]), (z_dot_initial, zd),
        (B_initial, B), (local_fields["shift_potential_velocity"], Bd),
        (Ktrace_initial, Ktrace), (local_fields["matter_momentum"], matter_p)]
    residuals = [_zero(mode_of(left)-right.subs(initial_mode)) for left, right in pairs]
    residuals += [_zero(mode_of(local_fields["extrinsic_curvature"][i, j])-Kvariation[i, j].subs(initial_mode))
                  for i in range(3) for j in range(3)]
    residuals += [_zero(mode_of(local_fields["gravity_tracefree_momentum"][i, j])-gravity_p[i, j].subs(initial_mode))
                  for i in range(3) for j in range(3)]
    inner = {}
    for name, value in local_fields.items():
        if isinstance(value, s.MatrixBase):
            inner.update({name+"_"+str(i)+str(j): s.simplify(value[i, j].subs(g, 0).doit())
                          for i in range(value.rows) for j in range(value.cols)})
        else:
            inner[name] = s.simplify(value.subs(g, 0).doit())
    return dict(matter_momentum=matter_p, gravity_momentum=gravity_p,
        extrinsic_curvature=Kvariation, extrinsic_trace=Ktrace, KTF=KTF,
        lapse_velocity=nd, z_velocity=zd, shift_potential=B, shift_velocity=Bd,
        Weyl_parallel=Eparallel, Weyl_canonical_tracefree_term=H*KTF[0, 0],
        Weyl_canonical_residual=_zero(Eparallel-canonical_E),
        required_inverse_Q_laplacian_coefficient=required_A1,
        geometry_residuals=list(geometry["residuals"].values()),
        physical_KG_action_residual=_zero(kg-d["evolution_equation"]),
        physical_ward_residuals=list(ward["residuals"].values()), external_stress_used=False,
        physical_density=density, relational_kinetic_density=relational,
        relational_gauge_variation=relational_gauge,
        trace_momentum_constraint_residual=_zero(s.trace(gravity_p)-3*a**3*tau*solution[z]),
        initial_local_fields=local_fields, initial_inner_ball_fields=inner,
        initial_reconstruction_residuals=residuals,
        initial_I_linear=_zero((4*k*k*(solution[n]+solution[z])/a**2).subs(initial_mode)))


@lru_cache(None)
def derive_tail():
    d = derive_action()
    a, q, m, H, K0, u, ud, k = (d[key] for key in ("a", "q", "m", "H", "K0", "u", "ud", "k"))
    p, mu2 = d["kappa_squared_symbol"], d["mu2_symbol"]
    selected = dict(d, acceleration=d["acceleration"].subs(K0, 3))
    jerk = _time_derivative(selected["acceleration"], selected).subs(ud, 0)
    jerk_transfer = s.factor((jerk/u).subs({k*k: a*a*p, q*q: 2*m*mu2/3}, simultaneous=True))
    jerk_pole_coefficient = s.factor(s.limit((p+mu2)*jerk_transfer, p, -mu2))
    jerk_local = s.factor(jerk_transfer-jerk_pole_coefficient/(p+mu2))
    primitive = s.factor(-a*a*p*jerk_transfer)
    hole_coefficient = s.factor(s.limit((p+mu2)*primitive, p, -mu2))
    primitive_local = s.factor(primitive-hole_coefficient/(p+mu2))
    radius = s.Symbol("radius", positive=True)
    eps = s.Symbol("amplitude", positive=True)
    green = a*a*s.exp(-a*s.sqrt(mu2)*radius)/(4*s.pi*radius)
    green_residual = _zero(-(s.diff(green, radius, 2)+2*s.diff(green, radius)/radius)/a**2+mu2*green)
    unit_flux = s.simplify(s.limit(-4*s.pi*radius**2*s.diff(green, radius)/a**2, radius, 0)-1)
    # g(r)=exp[-1/(r-1)^2-1/(2-r)^2] in (1,2), zero otherwise.
    # On [4/3,5/3], g>=exp(-18); r>=4/3 and interval width=1/3.
    green_integral_lower = 4*a*a*s.exp(-18-5*a*s.sqrt(mu2)/3)/9
    jerk_lower = s.factor(eps*hole_coefficient*green_integral_lower)
    third = s.Symbol("u_third", real=True)
    udd = d["udd"]
    jet_rates = {a: a*H, q: -3*H*q, H: -q*q/(2*m), u: ud, ud: udd, udd: third}
    jet_dt = lambda value: s.expand(sum(s.diff(value, field)*rate for field, rate in jet_rates.items()))
    relational = derive_geometry()["relational_kinetic_density"]
    inner_second = s.factor(jet_dt(jet_dt(relational)).subs({u: 0, ud: 0, udd: 0}))
    observable_lower = s.factor(abs(s.diff(inner_second, third))*jerk_lower)
    mean_k = s.Symbol("mean_mode_k", nonnegative=True)
    primitive_hat = s.Symbol("primitive_hat")

    t, Hd = s.symbols("background_time Hd", positive=True)
    at = s.sinh(3*Hd*t)**s.Rational(1, 3)
    qt = s.sqrt(6*m)*Hd/s.sinh(3*Hd*t)
    Ht = Hd/s.tanh(3*Hd*t)
    background_residuals = [_zero(s.diff(at, t)/at-Ht), _zero(s.diff(qt, t)+3*Ht*qt),
        _zero(s.diff(Ht, t)+qt*qt/(2*m)), _zero(Ht*Ht-Hd*Hd-qt*qt/(6*m))]
    return dict(jerk_transfer=jerk_transfer, jerk_local_part=jerk_local,
        jerk_pole_coefficient=jerk_pole_coefficient,
        jerk_decomposition_residual=_zero(jerk_transfer-(5*H*p/3-4*H*mu2/3+4*H*mu2**2/(3*(p+mu2)))),
        primitive_transfer=primitive, primitive_local_part=primitive_local,
        hole_jerk_coefficient=hole_coefficient,
        primitive_division_residual=_zero(primitive-primitive_local-4*H*a*a*mu2**3/(3*(p+mu2))),
        green_kernel=green, green_ODE_residual=green_residual, green_unit_flux_residual=unit_flux,
        strict_green_convolution_origin_lower_bound=green_integral_lower,
        strict_jerk_origin_lower_bound=jerk_lower,
        inner_relational_second_derivative=inner_second,
        relational_second_derivative_residual=_zero(inner_second+3*q*third),
        strict_abs_relational_second_derivative_lower_bound=observable_lower,
        physical_mean_zero_symbol=(-mean_k**2*primitive_hat).subs(mean_k, 0),
        positive_lambda_background=dict(a=at, q=qt, H=Ht, Lambda=3*Hd*Hd, tau=-3*m*Ht),
        background_residuals=background_residuals)


@lru_cache(None)
def derive_kernel_realizer():
    d = derive_action()
    a, k, m, q, b, n, z = (d[key] for key in ("a", "k", "m", "q", "b", "n", "z"))
    eps, x, y, zc = s.symbols("epsilon x y z_coordinate", real=True)
    coordinates = (x, y, zc)
    mode = s.cos(k*x)
    h = a*a*s.exp(2*eps*z*mode)*s.eye(3)
    inverse = h.inv()
    connection = [[[s.simplify(sum(inverse[i, ell]*(s.diff(h[ell, j], coordinates[l])
        +s.diff(h[ell, l], coordinates[j])-s.diff(h[j, l], coordinates[ell]))/2 for ell in range(3)))
        for l in range(3)] for j in range(3)] for i in range(3)]
    ricci = s.Matrix(3, 3, lambda i, j: sum(s.diff(connection[l][i][j], coordinates[l])
        -s.diff(connection[l][i][l], coordinates[j])
        +sum(connection[l][i][j]*connection[r][l][r]-connection[l][i][r]*connection[r][l][j]
             for r in range(3)) for l in range(3)))
    R = s.simplify(s.trace(inverse*ricci))
    N = 1+eps*n*mode
    volume = a**3*s.exp(3*eps*z*mode)
    acceleration = s.diff(s.log(N), x)
    div = s.diff(volume*inverse[0, 0]*acceleration, x)/volume
    I = R-4*div-2*inverse[0, 0]*acceleration**2
    I1 = s.simplify(s.diff(I, eps).subs(eps, 0)/mode)
    p = k*k/(a*a)
    screening_mass2 = b*q*q/m
    F = -1/(4*p)+1/(8*(p+screening_mass2))
    extra_density = s.factor(m*I1**2*F/2)
    recovered_Q = s.factor(m*p+s.diff(extra_density, z, 2)/2)
    tau_dot, Nbar = s.symbols("tau_T Nbar", positive=True)
    clock_mass2 = 2*b*tau_dot/(3*m*Nbar)
    return dict(I_linear=I1, spectral_F=F, extra_quadratic_density=extra_density,
        recovered_Q=recovered_Q, quadratic_matching_residual=_zero(recovered_Q-d["Qscreen"]),
        clock_screening_mass_squared=clock_mass2,
        clock_mass_matching_residual=_zero(clock_mass2.subs(tau_dot, 3*Nbar*q*q/2)-screening_mass2),
        possible_full_ADM_term="-m/8 <sqrt(N) I,L^-1 sqrt(N) I>_h + m/16 <sqrt(N) I,(L+2b*tau_T/(3mN))^-1 sqrt(N) I>_h, integrated over dT; L=-Delta_h",
        operator_scope="L+2b*tau_T/(3mN) means an elliptic operator plus multiplication by the displayed function, with a self-adjoint boundary realization. Its inverse does not commute with general N or h.",
        full_nonlinear_field_variation_completed=False)


def _encode(value):
    if isinstance(value, dict):
        return {str(key): _encode(item) for key, item in value.items()}
    if isinstance(value, s.MatrixBase):
        return _encode(value.tolist())
    if isinstance(value, (list, tuple)):
        return [_encode(item) for item in value]
    if isinstance(value, s.Integer):
        return int(value)
    if isinstance(value, s.Basic):
        return str(value)
    return value


@lru_cache(None)
def run():
    d, geometry, tail, realizer = derive_action(), derive_geometry(), derive_tail(), derive_kernel_realizer()
    residuals = d["constraint_residuals"]+d["seed_residuals"]+[d["time_EL_residual"], d["selected_drag_residual"]]
    residuals += geometry["geometry_residuals"]+geometry["physical_ward_residuals"]+geometry["initial_reconstruction_residuals"]
    residuals += [geometry[key] for key in ("Weyl_canonical_residual", "physical_KG_action_residual",
        "relational_gauge_variation", "trace_momentum_constraint_residual", "initial_I_linear")]
    residuals += list(geometry["initial_inner_ball_fields"].values())+tail["background_residuals"]
    residuals += [tail[key] for key in ("jerk_decomposition_residual", "primitive_division_residual",
        "green_ODE_residual", "green_unit_flux_residual", "relational_second_derivative_residual", "physical_mean_zero_symbol")]
    residuals += [realizer["quadratic_matching_residual"], realizer["clock_mass_matching_residual"]]
    checked = all(_zero(value) == 0 for value in residuals)
    detected = checked and tail["strict_abs_relational_second_derivative_lower_bound"].is_positive is True
    return _encode(dict(checks_passed=checked, expanding_linear_Cauchy_gate="FAIL" if detected else "INCONCLUSIVE",
        sympy_version=s.__version__, input_sha256={str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in [*INPUTS, Path(__file__).resolve()]},
        action=d, geometric_and_canonical_checks=geometry, expanding_tail=tail, possible_kernel_realizer=realizer,
        full_gravitational_count=None, zero_past_actuator_realization_claimed=False,
        nonlinear_initial_data_lift_claimed=False, exact_zero_mode_inverse_assigned=False,
        scope="NEW screened quadratic kernel, canonical P(X)=X, alpha=1. K0>0 in the frozen screen; the expanding witness is only K0=3,b=1/4. On the exact positive-Lambda branch m,Hd,t0>0, hence H,q,a>0. All conclusions are linear and on R3.",
        Weyl_identity="Ehat_ij=H KTF_ij+(9-K0) D_ij(ud)/(6a^2 q). The H KTF term is local in original canonical data and is not set to zero.",
        frozen_scope="Frozen real-frequency dispersion is a symbol diagnostic, not an exact charged Minkowski background. Pole cancellation occurs only at K0=3 for q!=0; the evolving background is separately varied.",
        witness="u(t0)=epsilon Delta g, ud(t0)=0; g(r)=exp[-1/(r-1)^2-1/(2-r)^2] for 1<r<2 and zero elsewhere. The initial original canonical fields and their displayed first metric jets are local derivatives of g, so they vanish in r<1. Vector and TT perturbations are zero. I1=0 globally initially.",
        positivity_proof="For L0=-Delta/a(t0)^2+mu^2, mu^2=3q(t0)^2/(2m), G(r)=a(t0)^2 exp[-a(t0)mu r]/(4pi r)>0. In the inner hole u'''=epsilon*(4H a^2 mu^6/3)*L0^-1 g>0. On 4/3<=r<=5/3, g>=exp(-18), giving the displayed strict convolution lower bound at the origin.",
        physical_observable="X=-g^{mu nu}partial_mu(sigma)partial_nu(sigma)/2. The scalar delta X-Xbar_dot*u/q=-3q ud+3Hq u is time-slicing invariant. In the hole its initial second derivative is -3q u'''<0. This is not inferred from a divergent lapse or from the uncancelled H*u inverse alone.",
        small_time_conclusion="A regular linear Cauchy flow has a nonzero quadratic-time relational-density perturbation at the origin, despite identical original initial canonical data throughout r<1. Metric-cone support would force that scalar and all of its initial time derivatives to vanish there. Thus such support is incompatible with the derived equations. No explicit finite-time remainder bound or nonlinear lift is supplied.",
        linear_flow_conditions="Smooth rapidly decaying Fourier data on any finite interval where a,q>0 and H is smooth. The selected equation is a wave equation with a smooth bounded order-zero Yukawa damping multiplier; the time-jet obstruction is conditional on a regular linear evolution, not a full nonlinear well-posedness theorem.",
        mean_zero_scope="Physical initial u=Delta g has zero integral by compact-support integration by parts; no homogeneous physical-mode equation is assigned. The primitive g has positive mean. The R3 decaying inverse gives Delta^-1 Delta g=g; compact torus/projector effects are NOT inherited.",
        operator_obligations="The proposed nonlinear ADM kernel only matches this quadratic density. Full metric/lapse variation, spatial inverse domains, covariant clock restoration, functional constraints, other sectors, PPN and nonlinear stability remain open."))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-causal-screen", action="store_true")
    args = parser.parse_args(argv)
    result = run()
    text = json.dumps(result, indent=2, sort_keys=True, allow_nan=False)
    if args.output:
        with args.output.open("x") as stream:
            stream.write(text+"\n")
    print(text)
    if not result["checks_passed"]:
        return 1
    return 2 if args.require_causal_screen and result["expanding_linear_Cauchy_gate"] != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
