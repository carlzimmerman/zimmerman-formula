#!/usr/bin/env python3
"""Gauge-restored finite quadratic IC-2 Dirac closure on its fixed FLRW witness.

Base 0a9f9fa33be9d4ace0e1496cef9ff19f48215017. One real k>0 scalar
mode; complex modes are two copies. T=t fixes the genuine clock slicing.
E is dimensionless: delta bar h_xx/(2 B^2)=(z+E)cos(k x), with transverse
diagonal entries z cos(k x). The spatial gauge acts by delta E=lambda,
delta shift=lambda_dot/k. The restoration is justified by an explicit ADM
pullback, not by assuming a constraint count. No nonlinear count is inferred.
"""
import argparse
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path
import platform

import sympy as s

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "scalar_completion.py"
SOURCE_SHA256 = "801e50f8a3485842eec9bafd58d4f652c42200050917da6d9f0360aea5ff7745"
IC4_SOURCE = HERE / "local_clock_wave.py"
# Rechecked after the source added packet readouts; its L and coefficients
# were unchanged, and all finite Hamiltonian/readout identities are rerun.
IC4_SHA256 = "a88d84135ea99263c62ecc339feffc76830623fb70b394222a1843174be7511d"
BASE = "0a9f9fa33be9d4ace0e1496cef9ff19f48215017"


@lru_cache(None)
def source():
    spec = importlib.util.spec_from_file_location("ic2_quadratic_dirac_source", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.derive(), module.repair()


def pb(f, g, coordinates, momenta):
    return s.factor(sum(s.diff(f, q)*s.diff(g, p)-s.diff(f, p)*s.diff(g, q)
                        for q, p in zip(coordinates, momenta)))


def _ricci(metric, coordinates):
    inverse = metric.inv()
    connection = [[[s.simplify(sum(inverse[i, ell]*(
        s.diff(metric[ell, j], coordinates[k])+s.diff(metric[ell, k], coordinates[j])
        -s.diff(metric[j, k], coordinates[ell])) for ell in range(3))/2)
        for k in range(3)] for j in range(3)] for i in range(3)]
    ricci = s.Matrix(3, 3, lambda i, j: s.simplify(sum(
        s.diff(connection[ell][i][j], coordinates[ell])
        -s.diff(connection[ell][i][ell], coordinates[j])
        +sum(connection[ell][ell][b]*connection[b][i][j]
             -connection[ell][j][b]*connection[b][i][ell] for b in range(3))
        for ell in range(3))))
    return s.simplify(s.trace(inverse*ricci))


@lru_cache(None)
def derive_gauge():
    raw, _ = source()
    B, h, k, z, zd, shift = [raw[key] for key in ("B", "h", "k", "z", "zd", "shift")]
    E, Ed, ep, theta = s.symbols("E Ed epsilon theta", real=True)
    co, si = s.cos(theta), s.sin(theta)
    metric = s.diag(B**2*s.exp(2*ep*(z+E)*co),
                    B**2*s.exp(2*ep*z*co), B**2*s.exp(2*ep*z*co))
    metric_dot = s.diag(*[2*(h+ep*(zd+(Ed if i == 0 else 0))*co)*metric[i, i]
                         for i in range(3)])
    velocity = ep*shift*si
    lie = s.diag(*[velocity*k*s.diff(metric[i, i], theta)
                   +(2*metric[i, i]*k*s.diff(velocity, theta) if i == 0 else 0)
                   for i in range(3)])
    Knum = metric.inv()*(metric_dot-lie)/2
    linear_K = Knum.applyfunc(lambda val: s.simplify(s.diff(val, ep).subs(ep, 0)/co))

    # Exact y=y(t,x) ADM pullback: new shift=(y_t+V)/J, J=y_x.
    J, Jx, Jt, yt, V, Vy, rt, ry = s.symbols("J Jx Jt yt V Vy rt ry", real=True)
    new_shift = (yt+V)/J
    new_shift_x = (Jt+Vy*J)/J-(yt+V)*Jx/J**2
    Kpull_xx = rt+ry*yt+Jt/J-new_shift*(ry*J+Jx/J)-new_shift_x
    Kpull_yy = rt+ry*yt-new_shift*ry*J

    # Actual curved spatial Ricci check, including the Jacobian derivative.
    xc, yc, zc = s.symbols("pullback_x pullback_y pullback_z", real=True)
    Afunc, Jfunc = s.Function("A")(xc), s.Function("Jac")(xc)
    pull_metric = s.diag(Afunc**2*Jfunc**2, Afunc**2, Afunc**2)
    Rpull = _ricci(pull_metric, (xc, yc, zc))
    A = s.Symbol("A", positive=True)
    Ay, Ayy = s.symbols("Ay Ayy", real=True)
    Rjets = Rpull.subs({s.diff(Afunc, xc, 2): Ayy*J**2+Ay*Jx,
        s.diff(Afunc, xc): Ay*J, s.diff(Jfunc, xc): Jx,
        Afunc: A, Jfunc: J}, simultaneous=True)
    # A(y)=B exp(epsilon z cos(k y)) gives the actual linear curvature.
    Rseed = -4*Ayy/A**3+2*Ay**2/A**4
    linear_R = s.simplify(s.diff(Rseed.subs({A:B*s.exp(ep*z*co),
        Ay:-ep*k*z*si*B*s.exp(ep*z*co),
        Ayy:(-ep*k*k*z*co+ep**2*k*k*z*z*si*si)*B*s.exp(ep*z*co)}), ep).subs(ep, 0)/co)

    # Every scalar-density term transforms as J f(y). Its averaged quadratic
    # coefficient is unchanged, including a nonzero first-order density.
    f0, fc, fs, fcc, fss, fcs = s.symbols("f0 fc fs fcc fss fcs", real=True)
    phase = theta+ep*E*si
    density = f0+ep*(fc*s.cos(phase)+fs*s.sin(phase))
    density += ep**2*(fcc*s.cos(phase)**2+fss*s.sin(phase)**2+fcs*s.cos(phase)*s.sin(phase))
    pulled_quadratic = s.diff((1+ep*E*co)*density, ep, 2).subs(ep, 0)/2
    pull_average = s.integrate(s.expand_trig(pulled_quadratic), (theta, 0, 2*s.pi))/(2*s.pi)

    # Check the expanding witness's three homogeneous first variations.
    rate, xi, uu, ell = s.symbols("rate xi u_witness ell", real=True)
    U = lambda c: (1-c)*(s.log(1-c)**2-2*s.log(1-c)+2)-2
    f = s.exp(-s.Rational(1, 2))
    acceleration2 = 27*h*h*f/(8*ell*ell)
    potential = 6*h*h*f+acceleration2*(U(uu*uu)-U(s.Rational(4, 9)))
    hom = (-3*rate**2+3*h*h)*s.exp((3*uu-4)*xi)-s.exp((3*uu-2)*xi)*potential
    witness = {rate:h, xi:s.Rational(1, 4), uu:s.Rational(2, 3)}
    clean = lambda val: s.simplify(val.subs(witness).subs(s.log(s.Rational(5, 9)), -ell))
    lamdot = s.Symbol("lambda_dot", real=True)
    residuals = dict(
        ADM_longitudinal=linear_K-s.diag(zd+Ed-k*shift, zd, zd),
        exact_pullback_Kxx=s.factor(Kpull_xx-(rt-V*ry-Vy)),
        exact_pullback_Kyy=s.factor(Kpull_yy-(rt-V*ry)),
        exact_pullback_R=s.simplify(Rjets-Rseed),
        gradient_pullback=s.cancel((J*Ay)**2/(A*A*J*J)-Ay*Ay/(A*A)),
        density_quadratic_average=s.simplify(pull_average-(fcc+fss)/2),
        linear_R=s.simplify(linear_R-4*k*k*z/(B*B)),
        gauge_combination=s.expand(shift+lamdot/k-(Ed+lamdot)/k-(shift-Ed/k)),
        background_lapse=clean(s.diff(hom, xi)),
        background_auxiliary=clean(s.diff(hom, uu)),
        background_scale=clean(3*(hom-rate*s.diff(hom, rate))))
    return dict(B=B, h=h, k=k, z=z, zd=zd, shift=shift, E=E, Ed=Ed,
        linear_Knum=linear_K, linear_R=linear_R, residuals=residuals,
        restoration="L2=L2_E0(shift-Ed/k); E dimensionless and longitudinal, not trace-free",
        pullback="y=x+epsilon E(t)sin(kx)/k; J=y_x; new shift=(seed shift+y_t)/J; N,u pulled as scalars",
        proof="The exact ADM numerator, Ricci scalar, gradient contraction and density Jacobian checks cover every imported action term. The quadratic density average is invariant. The checked background first variations ensure that a different second-order completion of the same linear metric changes only boundary terms.",
        boundary_domain="One periodic Fourier cell, or wave packets with vanishing spatial surface terms; fixed temporal endpoints. Small orientation-preserving pullback. No new full ADM field-theory count.")


def _dirac(L, raw, F, active, active_momenta, extra_coordinates=(), extra_momenta=()):
    z, n, v, h, x = [raw[key] for key in ("z", "n", "v", "h", "x")]
    pz, pn, pv = s.symbols("p_z p_n p_v", real=True)
    coordinates = [z]+list(extra_coordinates)+[n, v]
    momenta = [pz]+list(extra_momenta)+[pn, pv]
    # The final extra variable, if supplied, is the nondynamical shift.
    if extra_coordinates:
        E, shift = extra_coordinates
        pE, ps = extra_momenta
        coordinates, momenta = [z, E, n, v, shift], [pz, pE, pn, pv, ps]
        primary = [pn, pv, ps]
    else:
        primary = [pn, pv]
    derived_momenta = [s.diff(L, vel) for vel in active]
    velocity_solution = s.solve([p-val for p, val in zip(active_momenta, derived_momenta)], active, dict=True)[0]
    H = s.factor((sum(p*vel for p, vel in zip(active_momenta, active))-L).subs(velocity_solution))
    primary_velocity_residuals = [s.diff(L, vel) for vel in s.symbols("nd vd shiftd")[:len(primary)]]
    secondary = [pb(p, H, coordinates, momenta) for p in primary]
    constraints = primary+secondary
    omega = s.Matrix([[pb(c, d, coordinates, momenta) for d in constraints] for c in constraints])
    solve_variables = [n, v]+([pE] if extra_coordinates else [])
    surface = s.solve(secondary, solve_variables, dict=True)[0]
    weak = {**surface, **{p:0 for p in primary}}
    on_surface = lambda expr: s.factor(expr.subs(weak, simultaneous=True))
    explicit_time = lambda expr: s.factor(3*h*F*s.diff(expr, F)-2*h*x*s.diff(expr, x))
    drift = s.Matrix([pb(c, H, coordinates, momenta)+explicit_time(c) for c in secondary])
    multiplier_block = s.Matrix([[pb(c, p, coordinates, momenta) for p in primary] for c in secondary])
    block = multiplier_block.applyfunc(on_surface)
    independent_columns = block.rref()[1]
    independent_rows = block.T.rref()[1]
    subblock = block.extract(independent_rows, independent_columns)
    multipliers = s.zeros(len(primary), 1)
    solved = -subblock.inv()*drift.applyfunc(on_surface).extract(independent_rows, [0])
    for i, value in zip(independent_columns, solved):
        multipliers[i] = s.factor(value)
    preservation = (block*multipliers+drift.applyfunc(on_surface)).applyfunc(s.factor)
    frozen_drift = s.Matrix([pb(c, H, coordinates, momenta) for c in secondary])
    frozen_residuals = (block*multipliers+frozen_drift.applyfunc(on_surface)).applyfunc(s.factor)
    Hred = on_surface(H)
    multiplier_evolution = {str(field):s.factor(multipliers[i]-explicit_time(surface[field])
        -pb(surface[field], Hred, [z], [pz])) for i, field in enumerate((n, v))}
    weak_omega = omega.applyfunc(on_surface)
    rank = weak_omega.rank()
    gradient_rank = s.Matrix(constraints).jacobian(coordinates+momenta).rank()
    independent_variables = primary+[n, v]+([pE] if extra_coordinates else [])
    independence_minor = s.factor(s.Matrix(constraints).jacobian(independent_variables).det())
    sc_indices = weak_omega.rref()[1]
    second_class_minor = s.factor(weak_omega.extract(sc_indices, sc_indices).det())
    first, second = len(constraints)-rank, rank
    return dict(coordinates=coordinates, momenta=momenta, pz=pz, pn=pn, pv=pv,
        L=L, H=H, H_reduced=Hred, velocity_hessian=s.hessian(L, active),
        momenta_from_L={str(p):val for p, val in zip(active_momenta, derived_momenta)},
        velocity_solution=velocity_solution, primary_constraints=primary,
        secondary_constraints=secondary, constraint_surface=surface,
        poisson_matrix=omega, weak_poisson_matrix=weak_omega,
        poisson_rank=rank, constraint_gradient_rank=gradient_rank,
        constraint_independence_variables=independent_variables,
        constraint_independence_minor=independence_minor,
        second_class_poisson_minor=second_class_minor,
        first_class=first, second_class=second,
        physical_pairs=s.Rational(2*len(coordinates)-2*first-second, 2),
        first_class_combinations=[s.factor(sum(c*v for c, v in zip(constraints, vector)))
                                  for vector in weak_omega.nullspace()],
        multiplier_block=multiplier_block, multipliers=multipliers,
        undetermined_primary_indices=[i for i in range(len(primary)) if i not in independent_columns],
        explicit_secondary_time_derivatives=[explicit_time(c) for c in secondary],
        preservation_residuals={str(i):val for i, val in enumerate(preservation)},
        frozen_coefficient_preservation_residuals=list(frozen_residuals),
        multiplier_evolution_residuals=multiplier_evolution,
        auxiliary_hessian=s.hessian(H, (n, v)),
        residuals={**{"Legendre_"+str(i):s.factor((p-val).subs(velocity_solution))
                     for i, (p, val) in enumerate(zip(active_momenta, derived_momenta))},
                   **{"nondynamical_velocity_"+str(i):val for i, val in enumerate(primary_velocity_residuals)},
                   **{"primary_preservation_"+str(i):on_surface(c) for i, c in enumerate(secondary)}})


@lru_cache(None)
def derive_nonzero():
    raw, repair = source()
    F = s.Symbol("F", positive=True)
    z, zd, n, v, shift, h, k, x, T = [raw[key] for key in ("z", "zd", "n", "v", "shift", "h", "k", "x", "Tcal")]
    E, Ed, pz, pE, ps, P = s.symbols("E Ed p_z p_E p_shift P", real=True)
    selected = {raw["alpha"]:0, raw["beta"]:-s.Rational(1, 3), raw["gamma"]:s.Rational(1, 16)}
    L = s.expand(F*raw["L"].subs(selected).subs(shift, shift-Ed/k))
    result = _dirac(L, raw, F, [zd, Ed], [pz, pE], [E, shift], [pE, ps])
    a, b, c, g = [repair[key] for key in ("a", "bcoef", "c", "g")]
    reduced_L = F*(a*zd**2+h*b*z*zd+h*h*c*z*z)
    pred = s.diff(reduced_L, zd)
    zd_from_pred = s.solve(pz-pred, zd)[0]
    reduced_H_control = s.factor((pz*zd-reduced_L).subs(zd, zd_from_pred))
    generator = F*h*b*z*z/2
    tpart = lambda expr: s.factor(3*h*F*s.diff(expr, F)-2*h*x*s.diff(expr, x))
    boundary_removed_H = s.factor(result["H_reduced"].subs(pz, P+s.diff(generator, z))+tpart(generator))
    zdd = s.factor(tpart(zd_from_pred)+pb(zd_from_pred, result["H_reduced"], [z], [pz]))
    zdd = s.factor(zdd.subs(pz, pred))
    expected_acceleration = -(3*h-2*h*x*s.diff(a, x)/a)*zd+h*h*g*z/a
    gap, xpos = s.symbols("T_gap x_positive", positive=True)
    positive_minor = s.factor(result["auxiliary_hessian"].det().subs({T:s.Rational(27, 4)+gap, x:xpos}))
    gauge_speed = s.diff(result["H"], pE).subs(pE, 0)
    gauge_shift = s.solve(gauge_speed, shift)[0]
    residuals = dict(result["residuals"])
    residuals.update(
        F_definition_rate=s.simplify(s.diff(raw["m"]*s.exp(-s.Rational(1, 2))*raw["B"]**3, raw["B"])*h*raw["B"]
            -3*h*raw["m"]*s.exp(-s.Rational(1, 2))*raw["B"]**3),
        x_definition_rate=s.simplify(s.diff(s.exp(s.Rational(2, 3))*k*k/(h*h*raw["B"]**2), raw["B"])*h*raw["B"]
            +2*h*s.exp(s.Rational(2, 3))*k*k/(h*h*raw["B"]**2)),
        restored_gauge_Ward=s.factor(s.diff(L, shift)+k*s.diff(L, Ed)),
        gauge_fixed_shift=s.factor(gauge_shift-pz/(2*F*k)))
    result.update(F=F, F_definition=raw["m"]*s.exp(-s.Rational(1, 2))*raw["B"]**3,
        z=z, zd=zd, n=n, v=v, shift=shift, h=h, k=k, x=x, Tcal=T,
        E=E, Ed=Ed, pE=pE, P=P, a=a, b=b, c=c, g=g,
        gauge_fixed_shift=gauge_shift,
        regular_minor_positive=bool(positive_minor.is_positive),
        regular_minor_positive_expression=positive_minor,
        source_boundary_generator=-9*F*h*z*z,
        original_raw_pz=pz-18*F*h*z,
        second_boundary_generator=generator, boundary_removed_H=boundary_removed_H,
        reduced_residuals=dict(Hamiltonian=s.factor(result["H_reduced"]-reduced_H_control),
            boundary_map=s.factor(boundary_removed_H-P*P/(4*F*a)+F*h*h*g*z*z),
            actual_evolution=s.factor(zdd-expected_acceleration)),
        residuals=residuals,
        domain="F,h,k>0; x>0 with xdot=-2hx; Tcal=−27/16+54/[5 ln(9/5)]>27/4. Same fixed expanding IC-2 witness; no extra matter perturbations.",
        canonical_scope="One scalar canonical pair on the regular quadratic nonzero-mode surface. The two first-class constraints form one time-dependent spatial-gauge chain. The lapse/u momenta and their preservation constraints are second class. This is not a nonlinear functional Dirac calculation.")
    return result


@lru_cache(None)
def derive_homogeneous():
    raw, _ = source()
    F = s.Symbol("F", positive=True)
    ep = s.Symbol("homogeneous_epsilon", real=True)
    z, zd, n, v, h, T, ell = [raw[key] for key in ("z", "zd", "n", "v", "h", "Tcal", "ell")]
    xi, uu = s.Rational(1, 4)+ep*n, s.Rational(2, 3)+ep*v
    U = lambda c: (1-c)*(s.log(1-c)**2-2*s.log(1-c)+2)-2
    f = s.exp(-s.Rational(1, 2))
    potential = 6*h*h*f+27*h*h*f*(U(uu*uu)-U(s.Rational(4, 9)))/(8*ell*ell)
    raw_hom = s.exp(3*ep*z)*((-3*(h+ep*zd)**2+3*h*h)*s.exp((3*uu-4)*xi)
              -potential*s.exp((3*uu-2)*xi))/f
    coefficient = s.diff(raw_hom, ep, 2).subs(ep, 0)/2
    coefficient = s.expand(coefficient.subs(s.log(s.Rational(5, 9)), -ell), log=False)
    coefficient = s.factor(coefficient.subs(1/ell, s.Rational(5, 54)*(T+s.Rational(27, 16))))
    coefficient += 9*h*(3*h*z*z+2*z*zd)
    L = s.factor(F*coefficient)
    pz = s.Symbol("p_z", real=True)
    result = _dirac(L, raw, F, [zd], [pz])
    aux = s.solve([s.diff(L, q) for q in (n, v)], (n, v), dict=True)[0]
    reduced_L = s.factor(L.subs(aux))
    kinetic = s.factor(s.diff(reduced_L, zd, 2)/(2*F))
    residuals = dict(result["residuals"])
    residuals.update(
        independent_homogeneous_L=s.factor(L-F*raw["L0"].subs(raw["shift"], 0)),
        frozen_homogeneous_kinetic=s.factor(kinetic-raw["zero_mode_kinetic"]),
        reduced_H=s.factor(result["H_reduced"]-pz*pz/(4*F*kinetic)))
    for q in (n, v):
        residuals["frozen_homogeneous_"+str(q)] = s.factor(aux[q]-raw["zero_mode_solutions"][q])
    result.update(F=F, z=z, zd=zd, n=n, v=v, h=h, Tcal=T, kinetic=kinetic,
        residuals=residuals, domain="Exactly homogeneous mode in the fixed-volume spatial normalization (for example a flat torus): no E harmonic and no scalar shift harmonic. Global nondecaying spatial dilations are not added as gauge transformations. Independently differentiated before elimination; not k->0 of the nonzero-mode system.")
    return result


@lru_cache(None)
def derive_ic4():
    """Recompute the entire finite Dirac system from IC-4's new actual L."""
    spec = importlib.util.spec_from_file_location("ic4_for_quadratic_dirac", IC4_SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    candidate = module.derive()
    raw = candidate["raw"]
    F = s.Symbol("F", positive=True)
    z, zd, n, v, shift, h, k, x, T = [raw[key] for key in
        ("z", "zd", "n", "v", "shift", "h", "k", "x", "Tcal")]
    E, Ed, pz, pE, ps, P = s.symbols("E Ed p_z p_E p_shift P", real=True)
    shift_scaled = next(field for field in candidate["solutions"] if field not in (n, v))
    L = s.expand(F*h*h*candidate["L"].subs(
        {candidate["y"]:zd/h, shift_scaled:(k*shift-Ed)/h}, simultaneous=True))
    result = _dirac(L, raw, F, [zd, Ed], [pz, pE], [E, shift], [pE, ps])
    a, b, c, g = [candidate[key] for key in ("a", "b", "c", "g")]
    reduced_L = F*(a*zd**2+h*b*z*zd+h*h*c*z*z)
    pred = s.diff(reduced_L, zd)
    zd_from_pred = s.solve(pz-pred, zd)[0]
    Hcontrol = s.factor((pz*zd-reduced_L).subs(zd, zd_from_pred))
    tpart = lambda expr: s.factor(3*h*F*s.diff(expr, F)-2*h*x*s.diff(expr, x))
    generator = F*h*b*z*z/2
    boundary_H = s.factor(result["H_reduced"].subs(pz, P+s.diff(generator, z))+tpart(generator))
    acceleration = s.factor((tpart(zd_from_pred)
        +pb(zd_from_pred, result["H_reduced"], [z], [pz])).subs(pz, pred))
    expected = -(3*h-2*h*x*s.diff(a, x)/a)*zd+h*h*g*z/a
    gap, xpos = s.symbols("ic4_T_gap ic4_x_positive", positive=True)
    minor = s.factor(result["auxiliary_hessian"].det().subs({T:s.Rational(27, 4)+gap, x:xpos}))
    uniform = derive_homogeneous()
    readouts = {}
    for field in (n, v):
        independently_reduced = candidate["canonical_readouts"][str(field)].subs(candidate["P"], pz/(F*h))
        readouts[str(field)+"_canonical"] = s.factor(result["constraint_surface"][field]-independently_reduced)
        readouts[str(field)+"_genuine_zero_limit"] = s.factor(
            result["constraint_surface"][field].subs(x, 0)-uniform["constraint_surface"][field])
    gauge_shift = s.solve(s.diff(result["H"], pE).subs(pE, 0), shift)[0]
    source_shift = h*candidate["solutions"][shift_scaled].subs(candidate["y"], zd_from_pred/h)/k
    readouts["shift_canonical"] = s.factor(gauge_shift-source_shift)
    residuals = dict(result["residuals"])
    residuals.update({"action_bridge_"+str(name):value for name, value in candidate["bridge_residuals"].items()})
    residuals["restored_gauge_Ward"] = s.factor(s.diff(L, shift)+k*s.diff(L, Ed))
    result.update(F=F, z=z, zd=zd, n=n, v=v, shift=shift, h=h, k=k, x=x, Tcal=T,
        E=E, Ed=Ed, pE=pE, P=P, a=a, b=b, c=c, g=g,
        sigma=candidate["target_speed_squared"], actual_acceleration=acceleration,
        gauge_fixed_shift=gauge_shift,
        regular_minor_positive=bool(minor.is_positive), regular_minor_positive_expression=minor,
        source_boundary_generator=-9*F*h*z*z, original_raw_pz=pz-18*F*h*z,
        second_boundary_generator=generator, boundary_removed_H=boundary_H,
        reduced_residuals=dict(Hamiltonian=s.factor(result["H_reduced"]-Hcontrol),
            boundary_map=s.factor(boundary_H-P*P/(4*F*a)+F*h*h*g*z*z),
            actual_evolution=s.factor(acceleration-expected)),
        readout_residuals=readouts, residuals=residuals,
        source_normalization="The supplied L is dimensionless. The physical mode action is F h^2 L with y=zd/h and shift_scaled=(k shift-Ed)/h.",
        domain="IC-4 fixed action family, F,h,k>0, x>0, Tcal>27/4, 0<sigma<=1; exact same constant-lapse/auxiliary expanding witness. No extra ordinary matter perturbations.",
        gauge_bridge="The added Q^2 Rhat times a scalar coupling is also a spatial scalar density. The explicit ADM/curvature pullback in derive_gauge applies; its checked vanishing first variations preserve the background. No IC-2 constraint rank or multiplier is transferred.",
        canonical_scope="One physical scalar pair is obtained from this IC-4 quadratic Poisson matrix itself. Canonical n/v readouts match the independently reduced IC-4 action and their exactly homogeneous limits; this is not a nonlinear initial-data lift or all-background count.")
    return result


def encode(value):
    if isinstance(value, dict):
        return {str(k):encode(v) for k, v in value.items()}
    if isinstance(value, s.MatrixBase):
        return encode(value.tolist())
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    if isinstance(value, s.Integer):
        return int(value)
    if isinstance(value, s.Basic):
        return str(value)
    return value


@lru_cache(None)
def run():
    gauge, local, uniform = derive_gauge(), derive_nonzero(), derive_homogeneous()
    ic4 = derive_ic4()
    checks = {}
    for section, data in (("gauge", gauge), ("nonzero", local), ("homogeneous", uniform), ("IC4", ic4)):
        for key in ("residuals", "preservation_residuals", "multiplier_evolution_residuals", "reduced_residuals", "readout_residuals"):
            for name, value in data.get(key, {}).items():
                values = list(value) if isinstance(value, s.MatrixBase) else [value]
                checks[section+":"+key+":"+name] = all(s.simplify(v)==0 for v in values)
    checks["nonzero_regular_minor_positive"] = local["regular_minor_positive"]
    checks["IC4_regular_minor_positive"] = ic4["regular_minor_positive"]
    if not all(checks.values()):
        raise AssertionError({name:ok for name, ok in checks.items() if not ok})
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    ic4_hash = hashlib.sha256(IC4_SOURCE.read_bytes()).hexdigest()
    return encode(dict(base=BASE, checks_passed=all(checks.values()), checks=checks,
        input_hash_matches=source_hash==SOURCE_SHA256 and ic4_hash==IC4_SHA256,
        source_sha256=source_hash, ic4_source_sha256=ic4_hash,
        self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        software=dict(python=platform.python_version(), sympy=s.__version__),
        gauge_restoration=gauge, nonzero_mode=local, homogeneous_mode=uniform, IC4=ic4,
        mode_normalization="F times the pinned twice-spatial-average L2; equivalently a unit-norm real harmonic. Keeping an unnormalized cosine average 1/2 rescales every mode momentum and Hamiltonian by 1/2, without changing the equations or counts. The homogeneous harmonic is treated independently.",
        full_nonlinear_count_proved=False,
        open_hypotheses="No full inhomogeneous nonlinear preservation, constraint-domain/rank-stratum theorem, added ordinary-matter sector, or physical locality certificate. The finite pair is the coupled scalar/clock sector in unitary gauge; its gravitational/matter interpretation beyond this witness requires the nonlinear constraints."))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-full-nonlinear-count", action="store_true")
    args = parser.parse_args(argv)
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["input_hash_matches"]:
        return 1
    return 2 if args.require_full_nonlinear_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
