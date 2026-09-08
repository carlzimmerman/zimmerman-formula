"""Canonical-matter realizability and compact initial-data support at b=3/16.

Same S0+DeltaS_b, physical minimal P(X)=X, no external source. Arithmetic is
exact over real symbols, on an expanding flat FLRW background with a,m,q>0.
Spatial inverses are the decaying inverses on R^3; the analysis is linear.
The compact-Laplacian outer-support result includes every smooth compact f,g.
Its proof uses a displayed local energy identity, not a finite mode scan.
That outer envelope is the support of primitive data f,g, not necessarily the
support of physical canonical data Delta f,Delta g, and does not imply local
Cauchy domain dependence in holes of the physical support.

Compact metric/extrinsic initial data and compact initial tidal curvature are
different requirements here. A dipole velocity fixture satisfies the former
linear constraints but already has an exterior electric-Weyl tail at t0.
It is not a zero-past or initially tidal-tail-free counterexample.
The annular fixture below has all initial canonical data equal to background
in an inner ball but a nonzero physical Weyl response there before light can
arrive. Curvature accelerations are not independent Cauchy data. This proves a
linear physical Cauchy-support failure, not a zero-past actuator realization.
"""

import argparse
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path
import platform

import sympy as s


ROOT = Path(__file__).resolve().parents[1]


@lru_cache(None)
def _module(relative, name):
    path = ROOT/relative
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _simplify(expression):
    return s.factor(s.trigsimp(s.simplify(expression)))


@lru_cache(None)
def derive_stress_ward():
    """Vary the physical metric and scalar, then both terms of the Ward law.

    A real scalar Fourier mode along x suffices by background isotropy. The
    4x4 metric, inverse variation, scalar gradient and 64 Christoffels are
    explicit. In particular delta T is not a separately conserved Sigma.
    """
    t, x, y, zcoord = s.symbols("t x y z_coordinate", real=True)
    k = s.symbols("k", positive=True)
    coordinates = (t, x, y, zcoord)
    a, q, u, n, z, B = [s.Function(name)(t) for name in ("a", "q", "u", "n", "z", "B")]
    co, si = s.cos(k*x), s.sin(k*x)
    metric = s.diag(-1, a*a, a*a, a*a)
    inverse = metric.inv()
    h = s.diag(-2*n*co, 2*a*a*z*co, 2*a*a*z*co, 2*a*a*z*co)
    h[0, 1] = h[1, 0] = -a*a*k*B*si
    inverse_variation = -inverse*h*inverse
    scalar_gradient = s.Matrix([q, 0, 0, 0])
    gradient_variation = s.Matrix([s.diff(u*co, coordinate) for coordinate in coordinates])
    raised_gradient = inverse*scalar_gradient
    raised_variation = inverse_variation*scalar_gradient+inverse*gradient_variation
    X = -(scalar_gradient.T*inverse*scalar_gradient)[0]/2
    delta_X = -(scalar_gradient.T*inverse_variation*scalar_gradient)[0]/2
    delta_X -= (scalar_gradient.T*inverse*gradient_variation)[0]
    stress = raised_gradient*raised_gradient.T+inverse*X
    delta_stress = (raised_variation*raised_gradient.T+raised_gradient*raised_variation.T
                    +inverse_variation*X+inverse*delta_X).applyfunc(_simplify)
    covariant_stress = metric*stress*metric
    delta_covariant = (h*stress*metric+metric*delta_stress*metric+metric*stress*h).applyfunc(_simplify)
    delta_mixed = (inverse_variation*covariant_stress+inverse*delta_covariant).applyfunc(_simplify)

    connection = [[[s.simplify(sum(inverse[i, ell]*(
        s.diff(metric[ell, j], coordinates[b])+s.diff(metric[ell, b], coordinates[j])
        -s.diff(metric[j, b], coordinates[ell])) for ell in range(4))/2)
        for b in range(4)] for j in range(4)] for i in range(4)]
    delta_connection = [[[s.simplify(sum(
        inverse_variation[i, ell]*(s.diff(metric[ell, j], coordinates[b])
            +s.diff(metric[ell, b], coordinates[j])-s.diff(metric[j, b], coordinates[ell]))
        +inverse[i, ell]*(s.diff(h[ell, j], coordinates[b])+s.diff(h[ell, b], coordinates[j])
                          -s.diff(h[j, b], coordinates[ell]))
        for ell in range(4))/2) for b in range(4)] for j in range(4)] for i in range(4)]
    H = s.diff(a, t)/a
    background_rule = {s.diff(q, t): -3*H*q}
    separate_divergence, correction = [], []
    for nu in range(4):
        separate_divergence.append(_simplify(sum(
            s.diff(delta_stress[mu, nu], coordinates[mu])
            +sum(connection[mu][mu][ell]*delta_stress[ell, nu]
                 +connection[nu][mu][ell]*delta_stress[mu, ell] for ell in range(4))
            for mu in range(4)).subs(background_rule)))
        correction.append(_simplify(sum(
            delta_connection[mu][mu][ell]*stress[ell, nu]
            +delta_connection[nu][mu][ell]*stress[mu, ell]
            for mu in range(4) for ell in range(4))))
    full_ward = [_simplify(left+right) for left, right in zip(separate_divergence, correction)]
    # Independently differentiate sqrt(-g)*g^{mu nu} partial_nu sigma.
    volume_variation = s.trace(inverse*h)/2
    current_variation = a**3*(raised_variation+volume_variation*raised_gradient)
    background_box = s.diff(-a**3*q, t)/a**3
    delta_box = sum(s.diff(current_variation[mu], coordinates[mu]) for mu in range(4))/a**3
    delta_box -= volume_variation*background_box
    kg_equation = _simplify(-delta_box.subs(background_rule)/co)
    rho = _simplify((delta_covariant[0, 0]-2*n*co*X)/co)
    pressure = _simplify((sum(delta_covariant[i, i] for i in range(1, 4))/(3*a*a)
                          -2*z*co*X)/co)
    residuals = {"physical_density": s.simplify(rho-q*s.diff(u, t)+q*q*n),
                 "canonical_pressure_density": s.simplify(pressure-rho),
                 "physical_mixed_momentum": s.simplify(delta_mixed[0, 1]+q*s.diff(u*co, x)),
                 "canonical_anisotropic_stress": s.simplify(delta_mixed[1, 1]-delta_mixed[2, 2]),
                 "Ward_time_including_delta_connection": _simplify(full_ward[0]-q*kg_equation*co)}
    residuals.update({"Ward_spatial_"+str(i): full_ward[i] for i in range(1, 4)})
    return dict(t=t, k=k, a=a, q=q, u=u, n=n, z=z, B=B, H=H,
        metric=metric, metric_variation=h, background_stress_upper=stress,
        delta_stress_upper=delta_stress, delta_stress_covariant=delta_covariant,
        delta_stress_mixed=delta_mixed, density=rho, pressure=pressure,
        background_divergence_delta_T=separate_divergence,
        connection_correction=correction, full_linear_ward=full_ward,
        physical_Klein_Gordon_equation=kg_equation, residuals=residuals,
        convention="T^{mu nu}=partial^mu sigma partial^nu sigma+g^{mu nu}X; delta(div T)=bar_div(delta T)+delta_Gamma*Tbar; B is N^i=partial_i B")


@lru_cache(None)
def derive_constraints():
    """Vary the inherited raw-action seed with only the specified kernel change."""
    seed = _module("vcdm_flrw_gate_2026/vcdm_flrw.py", "physical_initial_seed")
    original = seed.derive_nonzero_mode()
    m = s.symbols("m", positive=True)
    a, k, q, u, ud = (original[key] for key in ("a", "k", "q", "u", "ud"))
    n, z, v = original["auxiliaries"]
    H, udd, tau = s.symbols("H udd tau", real=True)
    replacements = {original["M"]**2: m, original["alpha"]: 1,
                    original["Z"]: 1, original["D"]: 1}
    L = original["L"].subs(replacements)
    # b=3/16 is this task's fixed action, not a fitted output of this file.
    L = s.factor(L-m*k*k*(z+n)**2/a**2-s.Rational(3, 16)*q*q*(z+n)**2)
    equations = [s.diff(L, variable) for variable in (n, z, v)]
    solution = s.solve(equations, (n, z, v), dict=True)[0]
    reduced = s.factor(L.subs(solution))
    kinetic = s.factor(s.diff(reduced, ud, 2))
    frequency_numerator = s.factor(-s.diff(reduced, u, 2))
    acceleration = -3*H*ud-frequency_numerator*u/kinetic
    evolution = kinetic*(udd+3*H*ud)+frequency_numerator*u

    def dt(expression):
        return s.factor(sum(s.diff(expression, variable)*value for variable, value in
            {a: a*H, q: -3*H*q, u: ud, ud: acceleration, H: -q*q/(2*m)}.items()))

    zd = dt(solution[z])
    B = s.factor(-solution[v]/k)
    Bdot = dt(B)
    # Actual ADM definition with longitudinal shift v sin(kx).
    epsilon, theta = s.symbols("epsilon theta", real=True)
    scale = a*a*s.exp(2*epsilon*z*s.cos(theta))
    lapse = 1+epsilon*n*s.cos(theta)
    shift = epsilon*v*s.sin(theta)
    metric_dot = 2*(H+epsilon*s.Symbol("zd")*s.cos(theta))*scale
    Kraw = s.diag(*[(metric_dot-shift*k*s.diff(scale, theta)
        -(2*scale*k*s.diff(shift, theta) if i == 0 else 0))/(2*lapse*scale) for i in range(3)])
    delta_K = Kraw.applyfunc(lambda expression: s.simplify(s.diff(expression, epsilon).subs(epsilon, 0)/s.cos(theta)))
    delta_K = delta_K.subs(solution).subs(s.Symbol("zd"), zd).applyfunc(s.factor)
    delta_Ktrace = s.factor(s.trace(delta_K))
    delta_KTF = delta_K-s.eye(3)*delta_Ktrace/3
    raw_matter_momentum = a**3*s.exp(3*epsilon*z)*(q+epsilon*ud)/(1+epsilon*n)
    matter_momentum = s.factor(s.diff(raw_matter_momentum, epsilon).subs(epsilon, 0).subs(solution))
    # Mixed momentum density from the six-component Legendre map in
    # trace_hamiltonian.py: pi^i_j=m sqrt(h) KTF^i_j/2+sqrt(h) tau delta^i_j/3.
    delta_pi = (m*a**3*delta_KTF/2+a**3*tau*solution[z]*s.eye(3)).applyfunc(s.factor)

    ward = derive_stress_ward()
    time = ward["t"]
    to_time_functions = {a: ward["a"], q: ward["q"], u: ward["u"],
                         ud: s.diff(ward["u"], time)}
    kg = ward["physical_Klein_Gordon_equation"].subs({
        ward["n"]: solution[n].subs(to_time_functions),
        ward["z"]: solution[z].subs(to_time_functions),
        ward["B"]: B.subs(to_time_functions)}).doit()
    kg = kg.subs(s.diff(ward["q"], time), -3*ward["H"]*ward["q"])
    kg = kg.subs({s.diff(ward["a"], time): a*H, ward["a"]: a,
        ward["q"]: q, ward["u"]: u, s.diff(ward["u"], time): ud,
        s.diff(ward["u"], time, 2): udd}, simultaneous=True)
    endpoint = _module("constraint_response_gate_2026/adaptive_endpoint.py", "physical_initial_curvature")
    curvature = endpoint.derive()
    Eparallel = curvature["candidate_curvature"]["Weyl_parallel"]
    Eparallel = Eparallel.subs({curvature["a"]: a, curvature["m"]: m,
        curvature["q"]: q, curvature["H"]: H, curvature["u"]: u, curvature["ud"]: ud})
    kx, ky, kz = s.symbols("kx ky kz", real=True)
    wavevector = s.Matrix([kx, ky, kz])
    projector = wavevector*wavevector.T/(wavevector.dot(wavevector))-s.eye(3)/3
    Weyl = s.Rational(3, 2)*Eparallel*projector
    residuals = {"action_constraint_"+str(i): s.simplify(eq.subs(solution)) for i, eq in enumerate(equations)}
    residuals.update(seed_boundary_identity=original["boundary_residual"],
        physical_KG_matches_reduced_action=s.factor(kg-evolution),
        trace_momentum_constraint=s.factor(s.trace(delta_pi)-3*a**3*tau*solution[z]),
        Weyl_trace=s.factor(s.trace(Weyl)),
        Weyl_parallel_reconstruction=s.factor(Weyl[0, 0].subs({kx: k, ky: 0, kz: 0})-Eparallel))
    return dict(m=m, a=a, k=k, q=q, H=H, u=u, ud=ud, udd=udd, tau=tau,
        n=n, z=z, v=v, L=L, reduced_L=reduced, solution=solution,
        kinetic=kinetic, speed_squared=s.factor(s.diff(frequency_numerator, k, 2)*a*a/(2*kinetic)),
        frequency_numerator=frequency_numerator, evolution_equation=evolution,
        acceleration=acceleration, shift_potential=B, shift_potential_dot=Bdot,
        z_dot=zd, n_dot=dt(solution[n]), delta_K_mixed=delta_K,
        delta_K_trace=delta_Ktrace, delta_K_TF=delta_KTF, delta_pi_mixed=delta_pi,
        trace_multiplier_variation=s.factor(2*delta_Ktrace/3),
        matter_momentum=matter_momentum, physical_density=s.factor(q*(ud-q*solution[n])),
        Weyl_parallel=Eparallel, Weyl_tensor_fourier=Weyl, residuals=residuals,
        spatial_reconstruction="B=−3q Delta^-1 u/(2m); Ehat_ij=3q D_ij Delta^-1(2Hu−ud)/(4m), D_ij=partial_i partial_j−delta_ij Delta/3",
        constraint_scope="All nonzero-mode linear scalar auxiliary constraints, their evolution-consistent first jets, trace primary and canonical momenta; homogeneous mean is absent; vectors and TT initial data zero. Not a nonlinear constraint completion.")


@lru_cache(None)
def derive_support():
    t, x, y, z = s.symbols("support_t support_x support_y support_z", real=True)
    spatial = (x, y, z)
    F = s.Function("F")(t, x, y, z)
    P = s.Function("harmonic_test")(x, y, z)
    a, q = s.Function("scale")(t), s.Function("matter_q")(t)
    m, H = s.symbols("m H", positive=True)
    lap = lambda expression: sum(s.diff(expression, coordinate, 2) for coordinate in spatial)
    operator = lambda expression: (s.diff(expression, t, 2)+3*H*s.diff(expression, t)
        -lap(expression)/(9*a*a)+q*q*expression/(6*m))
    commutator = s.simplify(operator(lap(F))-lap(operator(F)))
    Ft = s.diff(F, t)
    grad2 = sum(s.diff(F, coordinate)**2 for coordinate in spatial)
    energy = (Ft*Ft+grad2/(9*a*a)+q*q*F*F/(6*m))/2
    flux = [-Ft*s.diff(F, coordinate)/(9*a*a) for coordinate in spatial]
    balance = s.diff(energy, t)+sum(s.diff(flux[i], spatial[i]) for i in range(3))
    balance = balance.subs(s.diff(F, t, 2), -3*H*Ft+lap(F)/(9*a*a)-q*q*F/(6*m))
    balance = s.simplify(balance.subs({s.diff(a, t): a*H, s.diff(q, t): -3*H*q}))
    dissipation = -3*H*Ft*Ft-H*grad2/(9*a*a)-H*q*q*F*F/(2*m)
    aa, qq = s.symbols("a q", positive=True)
    vel, normal, tan1, tan2, amp = s.symbols("Ft Fn Ftangent1 Ftangent2 F", real=True)
    speed = 1/(3*aa)
    ee = (vel**2+speed**2*(normal**2+tan1**2+tan2**2)+qq**2*amp**2/(6*m))/2
    normal_flux = -speed**2*vel*normal
    positive_remainder = speed**2*(tan1**2+tan2**2)/2+qq**2*amp**2/(12*m)
    outgoing_square = (vel-speed*normal)**2/2+positive_remainder
    incoming_square = (vel+speed*normal)**2/2+positive_remainder
    divergence = sum(s.diff(P*s.diff(F, coordinate)-F*s.diff(P, coordinate), coordinate)
                     for coordinate in spatial)
    khat, Fhat = s.symbols("nonzero_k Fhat", nonzero=True)
    return dict(laplacian_commutator=commutator, energy=energy, energy_flux=flux,
        energy_balance=balance, energy_dissipation=dissipation,
        energy_balance_residual=s.simplify(balance-dissipation),
        outgoing_flux_square=outgoing_square, incoming_flux_square=incoming_square,
        outgoing_flux_square_residual=s.simplify(ee+normal_flux/speed-outgoing_square),
        incoming_flux_square_residual=s.simplify(ee-normal_flux/speed-incoming_square),
        harmonic_moment_integrand_residual=s.simplify(P*lap(F)-F*lap(P)-divergence),
        kernel_inverse_cancellation=s.simplify((-1/khat**2)*(-khat**2*Fhat)-Fhat),
        proof_steps=[
            "For f,g in C_c^infinity(R^3), let F solve L F=0 with F(t0)=f, Fdot(t0)=g. The computed commutator gives u=Delta F with the required physical initial data.",
            "The displayed positive local energy obeys d_t e+div j<=0 for H>0. Its normal flux satisfies |j.normal|<=e/(3a), by the displayed sums of squares. Integrating over the exterior moving boundary gives zero exterior energy if it is initially zero.",
            "Thus supp F(t) lies within radius R+integral_t0^t ds/(3a(s)). Decaying-inverse uniqueness gives Delta^-1u=F. B, n, z, metric first jets, canonical momenta and Ehat_ij=3q D_ij(2HF−Fdot)/(4m) all have the same finite support bound.",
            "Integration by parts gives integral P Delta f=integral f Delta P=0 for every harmonic P; this excludes all harmonic moments, not merely the homogeneous mean.",
            "For compact u,ud, compact initial K_TF forces Hessian(Delta^-1u)=0 outside a large ball. Harmonicity and decay then force Delta^-1u=0 there. If initial Weyl is compact as well, the same argument applied to 2Hu−ud forces Delta^-1ud compact. This reduces that scalar class to the preceding f,g construction.",
            "Zero unforced full initial data are the f=g=0 case. The same energy argument gives the unique zero solution; they cannot realize a nonzero retarded external signed source."],
        outer_envelope_qualification="The support bound is based on primitive f,g. Harmonic nonzero f or g in a hole have Delta f=Delta g=0 there but can source local curvature through the inverse Laplacian. This is not a physical Cauchy-locality theorem.",
        boundary_scope="R^3, smooth compact data, decaying inverse Laplacian; finite t intervals with a,q nonzero. No torus, q=0, nonlinear, or independently forced claim.")


@lru_cache(None)
def derive_fixture():
    d = derive_constraints()
    m, a, q, H, u, ud = (d[key] for key in ("m", "a", "q", "H", "u", "ud"))
    w = s.symbols("compact_velocity_w", real=True)
    initial = {u: 0, ud: w}
    first_jet = {
        "lapse": d["solution"][d["n"]].subs(initial),
        "spatial_conformal_metric": d["solution"][d["z"]].subs(initial),
        "shift_potential": d["shift_potential"].subs(initial),
        "lapse_dot": d["n_dot"].subs(initial),
        "z_dot": d["z_dot"].subs(initial),
        "extrinsic_mixed": d["delta_K_mixed"].subs(initial),
        "pi_mixed": d["delta_pi_mixed"].subs(initial),
        "matter_momentum": d["matter_momentum"].subs(initial),
        "physical_density": d["physical_density"].subs(initial),
        "trace_multiplier": d["trace_multiplier_variation"].subs(initial),
    }
    x, y, z = s.symbols("fixture_x fixture_y fixture_z", real=True)
    radius, mass, epsilon = s.symbols("radius bump_integral epsilon", positive=True)
    r = s.sqrt(x*x+y*y+z*z)
    # eta is smooth radial, supported r<R, integral mass. The physical w is
    # epsilon*partial_x eta, hence mean zero, but it has a dipole moment.
    potential = s.diff(-epsilon*mass/(4*s.pi*r), x)
    Dij_potential_xx = s.diff(potential, x, 2)-sum(s.diff(potential, coord, 2) for coord in (x, y, z))/3
    exterior_E = s.simplify((-3*q*Dij_potential_xx/(4*m)).subs({x: radius, y: 0, z: 0}))
    expected = -9*epsilon*q*mass/(8*s.pi*m*radius**4)
    amplitude, point_w = s.symbols("amplitude point_w", real=True)
    exact_initial_X = (q+amplitude*point_w)**2/(2*(1+4*amplitude*point_w/q)**2)
    kx, etahat = s.symbols("kx eta_hat", real=True)
    residuals = {"initial_shift_zero": s.simplify(first_jet["shift_potential"]),
        "initial_zdot_zero": s.simplify(first_jet["z_dot"]),
        "initial_lapsedot_zero": s.simplify(first_jet["lapse_dot"]),
        "initial_extrinsic_isotropic": s.simplify(first_jet["extrinsic_mixed"][0, 0]-first_jet["extrinsic_mixed"][1, 1]),
        "dipole_exterior_Weyl": s.simplify(exterior_E-expected),
        "physical_profile_mean_zero": (s.I*kx*etahat).subs(kx, 0),
        "exact_positive_X_linear_density": s.simplify(s.diff(exact_initial_X, amplitude).subs(amplitude, 0)+3*q*point_w)}
    return dict(initial_scalar_field=s.S.Zero, initial_scalar_velocity=w,
        initial_first_jet=first_jet, initial_exterior_Weyl_xx=exterior_E,
        initial_shift_acceleration_potential=d["shift_potential_dot"].subs(initial),
        initial_tidal_data_compact=False, zero_past_realization=False,
        exact_initial_canonical_X=exact_initial_X,
        healthy_matter_scope="For sufficiently small amplitude the lapse and scalar normal derivative stay nonzero, X>0 and total canonical energy is positive. Signed delta rho is a perturbation of positive background rho, not exotic negative-energy matter. This does not furnish a nonlinear gravitational constraint completion.",
        admissibility="All listed scalar metric, extrinsic, momentum and multiplier first-jet perturbations are compact for compact w. Choosing w=epsilon partial_x eta gives a mean-zero physical mode. The nonlocal Bdot, hence electric Weyl, is already exterior at t0. Calling this initially tidal-tail-free would be false.",
        residuals=residuals)


@lru_cache(None)
def derive_background():
    t, Hd, m, A = s.symbols("proper_time H_d m scale_normalization", positive=True)
    a = A*s.sinh(3*Hd*t)**s.Rational(1, 3)
    H = Hd*s.coth(3*Hd*t)
    q = s.sqrt(6*m)*Hd/s.sinh(3*Hd*t)
    tau = -3*m*H
    cosmological_constant = 3*Hd*Hd
    residuals = {"Hubble": s.simplify(s.diff(a, t)/a-H),
        "Friedmann": s.simplify(3*m*H*H-m*cosmological_constant-q*q/2),
        "canonical_conservation": s.simplify(s.diff(a**3*q, t)),
        "Hubble_dot": s.simplify(s.diff(H, t)+q*q/(2*m)),
        "tau_dot": s.simplify(s.diff(tau, t)-3*q*q/2)}
    return dict(t=t, Hd=Hd, m=m, scale_normalization=A, a=a, H=H, q=q, tau=tau,
        Lambda=cosmological_constant, residuals=residuals,
        scope="Every H_d,m,A>0 on the expanding canonical stiff-plus-positive-Lambda branch, t>0. Negative q is related by sigma->−sigma. The exact q=0 de Sitter stratum is excluded.")


@lru_cache(None)
def derive_annular_fixture():
    """Canonical initial support is an annulus; the inverse primitive is not.

    chi=1 on r<=1 and chi=0 on r>=2, with smooth transitions. This function
    and every derivative vanish at the outer boundary. The cutoff is radial,
    so xy parity makes g=chi(r)xy mean zero on both R^3 and a centered flat
    torus whose chart contains the closed radius-two ball.
    """
    d, initial_fixture = derive_constraints(), derive_fixture()
    x, y, z = s.symbols("annulus_x annulus_y annulus_z", real=True)
    radial, epsilon = s.symbols("radial epsilon", positive=True)
    coordinates = (x, y, z)
    r = s.sqrt(x*x+y*y+z*z)
    cutoff = s.Function("chi")
    harmonic = x*y
    profile = cutoff(r)*harmonic
    lap = lambda expression: sum(s.diff(expression, coordinate, 2) for coordinate in coordinates)
    raw_laplacian = lap(profile)
    radial_first = s.diff(cutoff(radial), radial).subs(radial, r)
    radial_second = s.diff(cutoff(radial), radial, 2).subs(radial, r)
    laplacian_control = harmonic*(radial_second+6*radial_first/r)
    initial_velocity = epsilon*laplacian_control
    # The constant-cutoff inner region is not part of the physical support.
    inner_velocity = s.simplify(initial_velocity.subs({radial_first: 0, radial_second: 0}))
    w = initial_fixture["initial_scalar_velocity"]
    fields = {name: expression.subs(w, initial_velocity)
              for name, expression in initial_fixture["initial_first_jet"].items()}
    inner_fields = {name: expression.subs(w, inner_velocity)
                    for name, expression in initial_fixture["initial_first_jet"].items()}
    inner_fields["scalar_field"] = s.S.Zero
    inner_fields["scalar_velocity"] = inner_velocity
    inner_fields["spatial_metric"] = 2*d["a"]**2*inner_fields["spatial_conformal_metric"]*s.eye(3)
    Dij_xy = s.diff(harmonic, x, y)
    initial_Weyl = s.factor(-3*epsilon*d["q"]*Dij_xy/(4*d["m"]))
    kk, gg, a, q = s.symbols("nonzero_k ghat a q", positive=True)
    # I1=-4 a^-2 Delta(n+z). This fixture has n+z=8 epsilon Delta g/q.
    z_plus_n_hat = 8*epsilon*(-kk**2)*gg/q
    I_hat = -4*(-kk**2)*z_plus_n_hat/a**2
    inverse_I = s.factor(a**2*I_hat/kk**2)
    inverse_twice_I = s.factor(a**4*I_hat/kk**4)
    residuals = {
        "raw_cutoff_laplacian": s.simplify(raw_laplacian-laplacian_control),
        "inner_harmonic_laplacian": lap(harmonic),
        "inner_physical_velocity_zero": inner_velocity,
        "inner_Weyl_mixed_derivative": Dij_xy-1,
        "mean_zero_odd_x": s.simplify(profile.subs(x, -x)+profile),
        "mean_zero_odd_y": s.simplify(profile.subs(y, -y)+profile),
        "mean_zero_inverse_laplacian": s.simplify((-1/kk**2)*(-kk**2*gg)-gg),
        "first_kernel_potential": s.simplify(inverse_I-32*epsilon*(-kk**2)*gg/q),
        "second_kernel_potential": s.simplify(inverse_twice_I+32*epsilon*a**2*gg/q),
    }
    return dict(profile=profile, physical_initial_velocity=initial_velocity,
        initial_fields=fields, initial_inner_ball_fields=inner_fields,
        initial_inner_ball_Weyl_xy=initial_Weyl,
        physical_initial_support="1<r<2; u(t0)=0 and ud(t0)=epsilon Delta[chi(r)xy].",
        primitive_initial_support="g=chi(r)xy is nonzero throughout portions of r<1, even though Delta g=0 there.",
        kernel_potentials=dict(I1=I_hat, K_inverse_I1=inverse_I, K_inverse_squared_I1=inverse_twice_I),
        torus_mean_zero_by_parity=all(residuals[name] == 0 for name in ("mean_zero_odd_x", "mean_zero_odd_y")),
        torus_scope="Centered flat torus of side L>4 with the radius-two ball inside one chart. Extend g periodically by zero. Its xy parity gives integral g=0; thus the mean-zero inverse has Delta^-1 Delta g=g exactly. Only linear perturbations and the early local chart are used.",
        initial_data_scope="Compare background with these perturbed linear canonical data: lapse, spatial metric, shift, extrinsic curvature, trace/TF momenta, scalar field and momentum all coincide throughout r<1. Vector and TT data vanish in both. No independent nonlocal kernel potentials are adjoined as extra freely specifiable data. Constrained localized potentials such as W=L^-2(source), with L the localization's spatial elliptic operator, need not agree in the inner ball. The claim concerns the original metric/matter canonical data, not equality of every constrained auxiliary value in a localized reformulation.",
        residuals=residuals)


@lru_cache(None)
def derive_cauchy_response():
    """Exact unforced pre-cone Weyl bound for the annular canonical fixture.

    Locally F=s(t)xy has Delta F=0 and matches F(t0)=0,Fdot(t0)=xy.
    The local matter equation for F proves this equality inside the shrinking
    inner ball. Y=q*s is a derived homogeneous moment/amplitude variable, not
    an independently assigned physical zero mode.
    """
    d = derive_constraints()
    t = s.symbols("cauchy_time", positive=True)
    q, H, amp, Y = [s.Function(name)(t) for name in ("q_cauchy", "H_cauchy", "s_local", "Y_local")]
    Hd, H0, a_initial, q0, epsilon = s.symbols("H_d H0 a_initial q0 epsilon", positive=True)
    m = d["m"]
    original_equation = (d["evolution_equation"]/d["kinetic"]).subs({
        d["k"]: 0, d["u"]: amp, d["ud"]: s.diff(amp, t),
        d["udd"]: s.diff(amp, t, 2), d["q"]: q, d["H"]: H})
    transformed = (q*original_equation.subs(amp, Y/q).doit()).subs({
        s.diff(q, t, 2): (9*H**2-3*s.diff(H, t))*q, s.diff(q, t): -3*H*q})
    transformed = s.simplify(transformed).subs(q*q, -2*m*s.diff(H, t))
    damping = s.simplify(s.diff(transformed, s.diff(Y, t)))
    mass = s.simplify(s.diff(transformed, Y))
    mass_Lambda = s.factor(mass.subs(s.diff(H, t), -3*(H*H-Hd*Hd)))
    normalized_damping_bound = s.simplify(damping/H)
    normalized_mass_bound = s.simplify(mass_Lambda.subs(Hd, H)/(H*H))
    h_excess = s.symbols("H_squared_excess", nonnegative=True)
    mass_slack = s.factor((normalized_mass_bound*H*H-mass_Lambda)
                         .subs(H*H, Hd*Hd+h_excess))
    step = s.Rational(1, 20)
    delta = s.Min(step/H0, a_initial/4)
    green_lower = s.simplify(1-normalized_damping_bound*step-normalized_mass_bound*step**2/2)
    G, Gdot = s.symbols("G Gdot", real=True)
    Y_initial, Ydot_initial = s.S.Zero, q0
    Weyl_amplitude = -3*epsilon*(Gdot+H*G)*q0/(4*m)
    Weyl_lower = s.factor(3*epsilon*q0*green_lower/(4*m))
    # a increases: both matter and metric coordinate distances are bounded by
    # their initial-speed values. delta<=a_initial/4 keeps the origin's metric past
    # cone strictly inside the initial background-data ball r<1.
    light_margin = s.Rational(3, 4)
    matter_margin = s.Rational(11, 12)
    qdot0 = -3*H0*q0
    amp0, ampdot0 = s.S.Zero, s.S.One
    derived_Ydot0 = qdot0*amp0+q0*ampdot0
    residuals = {
        "derived_moment_operator": s.simplify(transformed-s.diff(Y, t, 2)-damping*s.diff(Y, t)-mass*Y),
        "positive_Lambda_mass": s.simplify(mass_Lambda-10*H*H-8*Hd*Hd),
        "derived_initial_Y": s.simplify(q0*amp0-Y_initial),
        "derived_initial_Ydot": s.simplify(derived_Ydot0-Ydot_initial),
        "Green_bound_arithmetic": s.simplify(green_lower-(1-normalized_damping_bound*step-normalized_mass_bound*step**2/2)),
        "initial_Weyl_matches_annular_fixture": s.simplify(Weyl_amplitude.subs({G: 0, Gdot: 1})+3*epsilon*q0/(4*m)),
        "light_cone_margin_arithmetic": s.simplify(1-s.Rational(1, 4)-light_margin),
        "matter_cone_margin_arithmetic": s.simplify(1-s.Rational(1, 12)-matter_margin),
    }
    return dict(local_amplitude_equation=original_equation, moment_variable="Y=q*s",
        transformed_equation=transformed, damping=damping, mass=mass_Lambda,
        Y_initial=Y_initial, Ydot_initial=Ydot_initial,
        normalized_damping_bound=normalized_damping_bound,
        normalized_mass_bound=normalized_mass_bound, mass_upper_slack=mass_slack,
        normalized_step=step, a_initial=a_initial, response_interval=delta,
        green_derivative_lower_bound=green_lower,
        inner_ball_Weyl_xy=Weyl_amplitude,
        inner_ball_abs_Weyl_lower_bound=Weyl_lower,
        outside_light_cone_margin_bound=light_margin,
        inside_primitive_harmonic_region_margin=matter_margin,
        initial_Weyl_is_independent_Cauchy_datum=False,
        external_source_used=False, incoming_vector_or_tensor_data_used=False,
        proof_steps=[
            "The actual reduced equation is local for u and commutes with Delta. Set u=epsilon Delta F and F(t0)=0,Fdot(t0)=g=chi(r)xy. In the inner local domain, F=s(t)xy because xy is harmonic and local finite propagation gives uniqueness there.",
            "The displayed transformation Y=q*s gives Y''+9H Y'+(10H^2+8Hd^2)Y=0, Y(t0)=0,Y'(t0)=q0. Thus Y=q0 G(t,t0), for the monic retarded homogeneous Green solution with initial slope one.",
            "Let H0=H(t0), a_initial=a(t0), x=H0(t-t0), g_G=H0 G. The symbol a_initial is the initial scale factor, not the MOND acceleration scale. Since H decreases and Hd<=H<=H0, normalized damping lies in [0,9] and normalized mass in (0,18]. Before any first zero of g_G', one has 0<=g_G'<=1 and 0<=g_G<=x. Integration yields g_G'>=1-9x-9x^2, which stays >=211/400 for x<=1/20 and contradicts a first zero. Consequently G_t+HG>=211/400.",
            "At the origin D_xy(xy)=1 and the action-derived orthonormal electric Weyl is −3epsilon(Y'+HY)/(4m). Its magnitude is at least 633epsilon q0/(1600m) for every 0<t-t0<=min[1/(20H0),a_initial/4].",
            "The source annulus starts at coordinate distance one. The metric light distance is <=(t-t0)/a_initial<=1/4; the F propagation distance is <=1/12. Hence the event lies strictly outside the metric future of the differing initial canonical data, while F=s(t)xy is valid around the event.",
            "Two solutions have identical full original canonical data in r<1, no external Sigma, and no incoming vector or tensor perturbations, but different gauge-invariant Weyl there at positive time. This is a linear physical Cauchy-domain-dependence failure. Initial curvature accelerations are derived observables, not independent data to add to that premise.",
        ],
        scope="b=3/16,K=9; all m,Hd,t0>0 and scale normalizations on the expanding stiff-plus-positive-Lambda branch; sufficiently small canonical matter perturbations. R^3 and a flat torus admitting the cutoff chart. Linear Cauchy support only, not a nonlinear lift or a zero-past actuator realization.",
        residuals=residuals)


def encode(value):
    if isinstance(value, dict):
        return {str(key): encode(item) for key, item in value.items()}
    if isinstance(value, s.MatrixBase):
        return encode(value.tolist())
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    if isinstance(value, s.Integer):
        return int(value)
    if isinstance(value, s.Basic):
        return str(value)
    return value


@lru_cache(None)
def run():
    stress, constraints = derive_stress_ward(), derive_constraints()
    support, fixture, background = derive_support(), derive_fixture(), derive_background()
    annular, cauchy = derive_annular_fixture(), derive_cauchy_response()
    residuals = {}
    for prefix, result in (("physical_ward", stress), ("constraints", constraints),
                           ("fixture", fixture), ("background", background),
                           ("annular_fixture", annular), ("physical_cauchy", cauchy)):
        residuals.update({prefix+":"+name: value for name, value in result["residuals"].items()})
    for name in ("laplacian_commutator", "energy_balance_residual", "outgoing_flux_square_residual",
                 "incoming_flux_square_residual", "harmonic_moment_integrand_residual", "kernel_inverse_cancellation"):
        residuals["support:"+name] = support[name]
    checks = {name: s.simplify(value) == 0 for name, value in residuals.items()}
    if not all(checks.values()):
        raise AssertionError({name: str(residuals[name]) for name, ok in checks.items() if not ok})
    cauchy_failure = (cauchy["green_derivative_lower_bound"].is_positive is True
        and cauchy["mass_upper_slack"].is_nonnegative is True
        and cauchy["inner_ball_abs_Weyl_lower_bound"].is_positive is True
        and cauchy["outside_light_cone_margin_bound"].is_positive is True
        and annular["torus_mean_zero_by_parity"])
    inputs = [ROOT/"vcdm_flrw_gate_2026/vcdm_flrw.py",
              ROOT/"constraint_response_gate_2026/adaptive_endpoint.py", Path(__file__).resolve()]
    return encode(dict(checks_passed=all(checks.values()), checks=checks,
        compact_laplacian_data_result="NO_EXTERIOR_TAIL",
        compact_first_jet_fixture_result="INITIAL_TIDAL_TAIL_ALREADY_PRESENT",
        healthy_linear_cauchy_gate="FAIL" if cauchy_failure else "INCONCLUSIVE",
        external_signed_probe_identified_with_canonical_delta_T=False,
        zero_past_unforced_nontrivial_matter_claimed=False,
        nonlinear_constraint_completion_claimed=False,
        physical_stress_and_ward=stress, constraints_and_cauchy_fields=constraints,
        support_proof=support, initial_tail_fixture=fixture, positive_lambda_background=background,
        annular_physical_initial_data=annular, physical_cauchy_response=cauchy,
        software=dict(python=platform.python_version(), sympy=s.__version__),
        input_sha256={str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in inputs},
        interpretation="The external signed zero-past witness has not been realized by unforced healthy canonical matter. A distinct unforced annular canonical-data fixture violates linear physical Cauchy domain dependence: Weyl is nonzero inside a ball whose original metric/matter canonical data equal background, before metric-light propagation can arrive. No independent nonlocal potentials are adjoined as initial data. A constrained localized potential W=L^-2(source) need not agree inside the ball, so this is nonlocal evolution of the original canonical data, not equality of all constrained localized auxiliary values. Compact-Laplacian data obey only an outer primitive-support envelope, not locality in holes of the physical support.",
        execution_scope="Exact symbolic identities and an analytic energy/support argument. No finite PDE simulation, full nonlinear count, nonlinear initial-data existence theorem, or general causality certificate."))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-cauchy-locality", action="store_true")
    args = parser.parse_args(argv)
    result = run()
    print("PHYSICAL_INITIAL_DATA_SCOPE_RESOLVED")
    print("Exact checks:", len(result["checks"]), "passed:", result["checks_passed"])
    print("Compact Laplacian class:", result["compact_laplacian_data_result"])
    print("Compact first-jet dipole:", result["compact_first_jet_fixture_result"])
    print("Initial exterior Weyl:", result["initial_tail_fixture"]["initial_exterior_Weyl_xx"])
    print("External signed probe identified with physical delta T:",
          result["external_signed_probe_identified_with_canonical_delta_T"])
    print("Healthy linear canonical Cauchy locality:", result["healthy_linear_cauchy_gate"])
    print("Annular pre-cone |Weyl_xy| lower bound:",
          result["physical_cauchy_response"]["inner_ball_abs_Weyl_lower_bound"])
    return 2 if args.require_cauchy_locality and result["healthy_linear_cauchy_gate"] != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
