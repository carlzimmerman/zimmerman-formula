"""Unforced healthy canonical Cauchy-support failure for every finite K>=1.

The pinned pre-constraint action is varied with external sources set to zero.
Its b-to-K map and the general metric/Weyl response are then derived. The
annular harmonic-primitive fixture is not restricted to K=9. All statements
are linear, on expanding stiff-plus-positive-Lambda backgrounds with q!=0.
No b=0, b<0, infinite-K limit, nonlinear initial-data lift, or zero-past
actuator realization is claimed. Small amplitudes may depend on finite K.
"""

import argparse
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess

import sympy as s


BASE = "c759c46ac02e6c09cd0c7c3cb206b8c31bbc1b97"
ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]


@lru_cache(None)
def _module(relative, name):
    spec = importlib.util.spec_from_file_location(name, ROOT/relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _dt(expression, d, acceleration=None):
    rates = {d["a"]: d["a"]*d["H"], d["q"]: -3*d["H"]*d["q"],
             d["H"]: -d["q"]**2/(2*d["m"]), d["u"]: d["ud"],
             d["ud"]: d["acceleration"] if acceleration is None else acceleration}
    return s.factor(sum(s.diff(expression, variable)*rate for variable, rate in rates.items()))


@lru_cache(None)
def derive_action():
    source_module = _module("constraint_response_gate_2026/causal_response.py", "general_family_pinned_action")
    inherited = source_module.derive_adaptive_action()
    m, b, K, a, k, q, u, ud, n, z, v = (inherited[key] for key in
        ("m", "b", "K", "a", "k", "q", "u", "ud", "n", "z", "v"))
    H, udd, tau = s.symbols("H udd tau", real=True)
    # Use only the actual action here, not inherited solved constraints,
    # reduced action, stiff equation, or K9 endpoint expressions.
    L_b = inherited["L"].subs({inherited[key]: 0 for key in ("rho", "p", "J")})
    equations = [s.diff(L_b, variable) for variable in (n, z, v)]
    solution_b = s.solve(equations, (n, z, v), dict=True)[0]
    reduced_b = s.factor(L_b.subs(solution_b))
    kinetic_b = s.factor(s.diff(reduced_b, ud, 2))
    b_of_K = s.solve(kinetic_b-K, b)[0]
    solution = {variable: s.factor(value.subs(b, b_of_K)) for variable, value in solution_b.items()}
    reduced = s.factor(reduced_b.subs(b, b_of_K))
    kinetic = s.factor(s.diff(reduced, ud, 2))
    Bmass = s.factor(-s.diff(reduced, u, 2))
    equation = kinetic*(udd+3*H*ud)+Bmass*u
    acceleration = s.factor(-3*H*ud-Bmass*u/kinetic)
    speed_squared = s.factor(a*a*s.diff(Bmass, k, 2)/(2*kinetic))
    epsilon = s.symbols("epsilon", real=True)
    raw_p_sigma = a**3*s.exp(3*epsilon*z)*(q+epsilon*ud)/(1+epsilon*n)
    matter_momentum = s.factor(s.diff(raw_p_sigma, epsilon).subs(epsilon, 0).subs(solution))
    unit_speed_boundary = s.solve(kinetic_b-1, b)[0]
    zero_kinetic_boundary = s.solve(kinetic_b, b)[0]
    positive_b = s.Interval.open(0, s.oo)
    solve_interval = lambda relation: s.solve_univariate_inequality(
        relation, b, relational=False, domain=positive_b)
    classification = {
        "K_ge_one": solve_interval(kinetic_b >= 1),
        "zero_lt_K_lt_one": s.Intersection(solve_interval(kinetic_b > 0),
                                             solve_interval(kinetic_b < 1)),
        "K_zero": s.solveset(kinetic_b, b, domain=positive_b),
        "K_negative": solve_interval(kinetic_b < 0),
    }
    checks = {"free_auxiliary_"+str(i): s.simplify(eq.subs(solution_b)) for i, eq in enumerate(equations)}
    checks.update(kinetic_parameterization=s.simplify(kinetic-K),
        unit_speed_boundary=s.simplify(kinetic_b.subs(b, unit_speed_boundary)-1),
        zero_kinetic_boundary=s.simplify(kinetic_b.subs(b, zero_kinetic_boundary)),
        canonical_matter_momentum=s.factor(matter_momentum-K*a**3*ud))
    paths = [ROOT/"constraint_response_gate_2026/causal_response.py", Path(inherited["seed_path"]),
             ROOT/"constraint_response_gate_2026/adaptive_endpoint.py"]
    hashes = {}
    for path in paths:
        relative = str(path.relative_to(REPO))
        pinned = subprocess.run(["git", "show", BASE+":"+relative], cwd=REPO,
                                capture_output=True, check=True).stdout
        hashes[relative] = dict(current=hashlib.sha256(path.read_bytes()).hexdigest(),
                                pinned=hashlib.sha256(pinned).hexdigest())
    return dict(m=m, b=b, K=K, a=a, k=k, q=q, H=H, u=u, ud=ud, udd=udd,
        n=n, z=z, v=v, tau=tau, L_b=L_b, solution_b=solution_b, solution=solution,
        reduced_b=reduced_b, reduced_L=reduced, kinetic_b=kinetic_b, b_of_K=b_of_K,
        kinetic=kinetic, gradient_mass=Bmass, evolution_equation=equation,
        acceleration=acceleration, speed_squared=speed_squared,
        matter_momentum=matter_momentum, physical_density=s.factor(q*(ud-q*solution[n])),
        positive_b_classification=classification, kinetic_b_derivative=s.factor(s.diff(kinetic_b, b)),
        classification_scope="For b>0 only: K>=1 is the proved Cauchy-support family; 0<K<1 has superluminal principal matter speed; K=0 has degenerate reduced kinetic; K<0 has negative reduced kinetic. No constraint count is assigned at K=0.",
        pinned_inputs_match=all(item["current"] == item["pinned"] for item in hashes.values()),
        input_hashes=hashes, residuals=checks)


@lru_cache(None)
def derive_geometry():
    d = derive_action()
    a, m, k, q, H, K, u, ud, n, z, v = (d[key] for key in
        ("a", "m", "k", "q", "H", "K", "u", "ud", "n", "z", "v"))
    solution = d["solution"]
    B = s.factor(-solution[v]/k)
    Bdot = _dt(B, d)
    zd = _dt(solution[z], d)
    # Evaluate the actual 4D connection-derived Weyl at general K. No
    # candidate-curvature or special-K expression is imported.
    raw = _module("constraint_response_gate_2026/adaptive_endpoint.py", "general_family_raw_connection").derive_connection()
    t = raw["t"]
    jets = {raw["a"]: a, s.diff(raw["a"], t): a*H,
            s.diff(raw["a"], t, 2): a*(H*H-q*q/(2*m))}
    for key, variable in (("n", n), ("z", z), ("v", v)):
        expr = solution[variable]
        jets[raw[key]] = expr
        jets[s.diff(raw[key], t)] = _dt(expr, d)
        jets[s.diff(raw[key], t, 2)] = _dt(_dt(expr, d), d)
    Eparallel = s.factor(raw["Weyl_parallel"].subs(jets, simultaneous=True))
    Etransverse = s.factor(raw["Weyl_transverse"].subs(jets, simultaneous=True))
    scalar_Weyl_potential = s.factor(solution[n]-solution[z]+a*a*(Bdot+H*B))
    local_slip = s.factor(s.diff(solution[n]-solution[z], ud)/(2*a*a))
    inverse_shift_coefficient = s.factor(-k*k*s.diff(B, u))
    inverse_Weyl_coefficient = s.factor(-inverse_shift_coefficient/2)

    epsilon, theta = s.symbols("epsilon theta", real=True)
    zz_dot, nn_dot, vv_dot = s.symbols("z_dot n_dot v_dot", real=True)
    co, si = s.cos(theta), s.sin(theta)
    scale, lapse, shift = a*a*s.exp(2*epsilon*z*co), 1+epsilon*n*co, epsilon*v*si
    scale_dot = 2*(H+epsilon*zz_dot*co)*scale
    Kraw = s.diag(*[(scale_dot-shift*k*s.diff(scale, theta)
        -(2*scale*k*s.diff(shift, theta) if i == 0 else 0))/(2*lapse*scale) for i in range(3)])
    delta_K = Kraw.applyfunc(lambda expr: s.simplify(s.diff(expr, epsilon).subs(epsilon, 0)/co))
    delta_K = delta_K.subs(solution).subs(zz_dot, zd).applyfunc(s.factor)
    delta_Ktrace = s.factor(s.trace(delta_K))
    KTF = delta_K-s.eye(3)*delta_Ktrace/3
    delta_pi = (m*a**3*KTF/2+a**3*d["tau"]*solution[z]*s.eye(3)).applyfunc(s.factor)

    # Direct canonical scalar current, independently checking its physical
    # equation on the general auxiliary solution.
    volume = lapse*a**3*s.exp(3*epsilon*z*co)
    sigmadot, sigmax = q+epsilon*ud*co, -epsilon*k*u*si
    J0 = volume*(-sigmadot/lapse**2+shift*sigmax/lapse**2)
    Jx = volume*(shift*sigmadot/lapse**2+(1/scale-shift**2/lapse**2)*sigmax)
    J0linear = s.simplify(s.diff(J0, epsilon).subs(epsilon, 0))
    Jxlinear = s.simplify(s.diff(Jx, epsilon).subs(epsilon, 0))
    rates = {a: a*H, q: -3*H*q, u: ud, ud: d["udd"], n: nn_dot, z: zz_dot, v: vv_dot}
    current_dt = sum(s.diff(J0linear, variable)*rate for variable, rate in rates.items())
    physical_KG = s.simplify(-(current_dt+k*s.diff(Jxlinear, theta))/(a**3*co))
    physical_KG = physical_KG.subs(solution).subs({
        nn_dot: _dt(solution[n], d, d["udd"]), zz_dot: _dt(solution[z], d, d["udd"]),
        vv_dot: _dt(solution[v], d, d["udd"])})
    residuals = dict(raw["residuals"])
    residuals.update(
        general_Weyl_scalar_potential=s.factor(Eparallel+k*k*scalar_Weyl_potential/(3*a*a)),
        general_Weyl_trace=s.factor(Eparallel+2*Etransverse),
        general_Weyl_local_nonlocal_split=s.factor(Eparallel
            +(s.Rational(2, 3)*k*k)*local_slip*ud
            -(s.Rational(2, 3)*inverse_Weyl_coefficient)*(2*H*u-ud)),
        physical_Klein_Gordon=s.factor(physical_KG-d["evolution_equation"]),
        trace_primary=s.factor(s.trace(delta_pi)-3*a**3*d["tau"]*solution[z]))
    return dict(K=K, m=m, a=a, q=q, H=H, u=u, ud=ud,
        shift_potential=B, shift_potential_dot=Bdot, z_dot=zd,
        n_dot=_dt(solution[n], d), Weyl_parallel=Eparallel,
        Weyl_transverse=Etransverse, scalar_Weyl_potential=scalar_Weyl_potential,
        local_slip_coefficient=local_slip, inverse_shift_coefficient=inverse_shift_coefficient,
        inverse_Weyl_coefficient=inverse_Weyl_coefficient,
        delta_K_mixed=delta_K, delta_K_trace=delta_Ktrace, delta_K_TF=KTF,
        delta_pi_mixed=delta_pi, trace_multiplier_variation=s.factor(2*delta_Ktrace/3),
        Weyl_real_space="Ehat_ij=(9-K)D_ij ud/(6a^2 q)+3q D_ij Delta^-1(2Hu-ud)/(4m)",
        residuals=residuals)


@lru_cache(None)
def derive_annular():
    d, geometry = derive_action(), derive_geometry()
    x, y, z = s.symbols("annular_x annular_y annular_z", real=True)
    rvar, epsilon = s.symbols("radius epsilon", positive=True)
    r = s.sqrt(x*x+y*y+z*z)
    chi = s.Function("chi")
    harmonic, g = x*y, x*y*chi(r)
    lap = lambda expr: sum(s.diff(expr, coordinate, 2) for coordinate in (x, y, z))
    first = s.diff(chi(rvar), rvar).subs(rvar, r)
    second = s.diff(chi(rvar), rvar, 2).subs(rvar, r)
    lapg = harmonic*(second+6*first/r)
    w = s.symbols("initial_velocity", real=True)
    initial = {d["u"]: 0, d["ud"]: w}
    fields = {"lapse": d["solution"][d["n"]], "spatial_conformal_metric": d["solution"][d["z"]],
        "shift_potential": geometry["shift_potential"], "extrinsic_mixed": geometry["delta_K_mixed"],
        "pi_mixed": geometry["delta_pi_mixed"], "trace_multiplier": geometry["trace_multiplier_variation"],
        "n_dot": geometry["n_dot"], "z_dot": geometry["z_dot"],
        "scalar_field": d["u"], "scalar_velocity": d["ud"],
        "scalar_momentum": d["matter_momentum"], "physical_density": d["physical_density"]}
    initial_fields = {name: expr.subs(initial) for name, expr in fields.items()}
    inner_fields = {name: expr.subs(w, 0) for name, expr in initial_fields.items()}
    KK = d["K"]
    # The first kernel inverse is proportional to Delta g, while the second
    # is proportional to g; the latter is not an additional free datum.
    k, gh = d["k"], s.symbols("g_hat", real=True)
    slip_hat = (d["solution"][d["n"]]+d["solution"][d["z"]]).subs(
        {d["u"]: 0, d["ud"]: -epsilon*k*k*gh})
    I_hat = s.factor(4*k*k*slip_hat/d["a"]**2)
    potentials = [s.factor(I_hat*d["a"]**(2*order)/k**(2*order)) for order in (1, 2)]
    residuals = {"cutoff_laplacian": s.simplify(lap(g)-lapg),
        "inner_harmonic": lap(harmonic), "odd_x": s.simplify(g.subs(x, -x)+g),
        "odd_y": s.simplify(g.subs(y, -y)+g),
        "inner_cross_derivative": s.diff(harmonic, x, y)-1,
        "mean_zero_inverse": s.simplify((-1/k**2)*(-k**2*gh)-gh)}
    for name, field in inner_fields.items():
        for index, value in enumerate(list(field) if isinstance(field, s.MatrixBase) else [field]):
            residuals["inner_initial_"+name+"_"+str(index)] = s.simplify(value)
    eamp, point_w = s.symbols("small_amplitude point_w", real=True)
    initial_X = (d["q"]+eamp*point_w)**2/(2*(1+4*eamp*point_w/d["q"])**2)
    return dict(profile=g, physical_velocity=epsilon*lapg, initial_fields=initial_fields,
        inner_initial_fields=inner_fields, kernel_potentials=potentials,
        total_initial_canonical_X=initial_X,
        torus_mean_zero_by_parity=residuals["odd_x"] == 0 and residuals["odd_y"] == 0,
        epsilon_may_depend_on_K=True, localized_auxiliary_values_claimed_equal=False,
        healthy_matter_scope="For each finite K, choose epsilon small enough for positive lapse, timelike canonical scalar gradient, and small metric perturbations. K>0 and gradient/mass>0 give positive reduced matter quadratic energy. Since z=(K+3)ud/(3q), the permitted amplitude can depend on K; no uniform fixed-amplitude K->infinity limit is asserted.",
        data_scope="chi=1 for r<=1 and zero for r>=2, smooth and radial. Original canonical data differ only in the annulus. On R^3 use decay; on a centered flat torus of side L>4 use xy parity and mean-zero inverse. No incoming vector/TT data. Constrained localized potentials need not agree in the inner ball and are not adjoined as independent initial data.",
        residuals=residuals)


@lru_cache(None)
def derive_green():
    d, geometry = derive_action(), derive_geometry()
    t = s.symbols("time", positive=True)
    q, H, amplitude, Y = [s.Function(name)(t) for name in ("q", "H", "s_local", "Y")]
    Hd, H0, a_initial, q0, epsilon = s.symbols("H_d H0 a_initial q0 epsilon", positive=True)
    K, m = d["K"], d["m"]
    ode = (d["evolution_equation"]/d["kinetic"]).subs({d["k"]: 0,
        d["u"]: amplitude, d["ud"]: s.diff(amplitude, t), d["udd"]: s.diff(amplitude, t, 2),
        d["q"]: q, d["H"]: H})
    transformed = (q*ode.subs(amplitude, Y/q).doit()).subs({
        s.diff(q, t, 2): (9*H*H-3*s.diff(H, t))*q, s.diff(q, t): -3*H*q})
    transformed = s.simplify(transformed).subs(q*q, -2*m*s.diff(H, t))
    damping = s.simplify(s.diff(transformed, s.diff(Y, t)))
    mass = s.simplify(s.diff(transformed, Y))
    mass_Lambda = s.factor(mass.subs(s.diff(H, t), -3*(H*H-Hd*Hd)))
    mass_bound = s.simplify(mass_Lambda.subs(K, 1)/(H*H))
    damping_bound = s.simplify(damping/H)
    excess, H_excess = s.symbols("K_excess H_squared_excess", nonnegative=True)
    mass_slack = s.factor((mass_bound*H*H-mass_Lambda).subs(K, 1+excess)
                         .subs(H*H, Hd*Hd+H_excess))
    mass_positive = s.factor(mass_Lambda.subs(K, 1+excess).subs(H*H, Hd*Hd+H_excess))
    speed_gap = s.factor((1-d["speed_squared"]).subs(K, 1+excess))
    step = s.Rational(1, 20)
    green_lower = s.simplify(1-damping_bound*step-mass_bound*step**2/2)
    duration = s.Min(step/H0, a_initial/4)
    # In the hole F=s(t)xy, u=Delta F=0. The local n-z contribution
    # vanishes in an open region. Reconstruct B from its general action
    # coefficient, then differentiate the actual Weyl potential.
    x, y = s.symbols("hole_x hole_y", real=True)
    B_hole = geometry["inverse_shift_coefficient"].subs(d["q"], q)*epsilon*amplitude*x*y
    E_hole = s.diff(s.diff(s.diff(B_hole, t)+H*B_hole, x), y)/2
    E_Y = s.factor(E_hole.subs(amplitude, Y/q).doit())
    coefficient = s.factor(s.diff(E_Y, s.diff(Y, t)))
    Weyl_lower = s.factor(-coefficient*q0*green_lower)
    initial_E = E_Y.subs({Y: 0, s.diff(Y, t): q0}, simultaneous=True)
    residuals = {
        "moment_operator": s.simplify(transformed-s.diff(Y, t, 2)-damping*s.diff(Y, t)-mass*Y),
        "general_positive_Lambda_mass": s.factor(mass_Lambda
            -9*((1+1/K)*H*H+(1-1/K)*Hd*Hd)),
        "hole_Weyl_amplitude": s.factor(E_Y-coefficient*(s.diff(Y, t)+H*Y)),
        "initial_Weyl": s.factor(initial_E+3*epsilon*q0/(4*m)),
        "Green_arithmetic": s.simplify(green_lower-(1-damping_bound*step-mass_bound*step**2/2)),
        "initial_Ydot": s.simplify((-3*H0*q0)*0+q0*1-q0),
    }
    return dict(moment_variable="Y=q*s, s(t0)=0, sdot(t0)=1", local_ode=ode,
        transformed_ode=transformed, damping=damping, mass=mass_Lambda,
        damping_upper_bound=damping_bound, mass_upper_bound=mass_bound,
        mass_upper_slack=mass_slack, mass_positive_certificate=mass_positive,
        metric_speed_gap_certificate=speed_gap, response_interval=duration,
        green_lower=green_lower, hole_shift=B_hole, hole_Weyl_xy=E_Y,
        initial_Weyl_xy=initial_E, Weyl_abs_lower=Weyl_lower,
        matter_cone_margin=s.Rational(3, 4), metric_cone_margin=s.Rational(3, 4),
        proof=[
            "For F(t0)=0,Fdot(t0)=chi(r)xy, u=epsilon Delta F solves the physical unforced equation. The F equation has speed1/sqrt(K). Its local positive energy has flux bound e/(a sqrt(K)); for K>=1 the origin remains in the harmonic-data region through delta<=a_initial/4.",
            "There F=s(t)xy and the action-derived local n-z term is zero. The general shift gives the displayed E_xy proportional to Ydot+HY. Y=q*s obeys the displayed positive-Lambda homogeneous ODE, with Y(t0)=0,Ydot(t0)=q0.",
            "H decreases from H0 and Hd<=H. The exact certificates imply normalized damping0<=p<=9 and mass0<c<=18. With x=H0(t-t0), g=H0G, before a first zero of g' one has 0<=g'<=1 and0<=g<=x. Hence g'>=1-9x-9x^2>=211/400 for x<=1/20, excluding a first zero and giving G_t+HG>=211/400.",
            "Thus |E_xy(origin,t)|>=633epsilon q0/(1600m)>0 for every0<t-t0<=min[1/(20H0),a_initial/4]. Both matter and metric coordinate propagation distances are <=1/4; the differing original canonical data start at radius1.",
            "This compares two unforced linear solutions whose original metric/matter canonical data agree in the inner ball, but whose physical Weyl differs there before light can arrive. Curvature accelerations and constrained localized inverse-kernel potentials are not extra independently specified canonical data in that comparison.",
        ], residuals=residuals)


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
    action, geometry, annular, green = derive_action(), derive_geometry(), derive_annular(), derive_green()
    residuals = {}
    for name, result in (("action", action), ("geometry", geometry), ("annular", annular), ("green", green)):
        residuals.update({name+":"+key: value for key, value in result["residuals"].items()})
    checks = {name: s.simplify(value) == 0 for name, value in residuals.items()}
    passed = action["pinned_inputs_match"] and all(checks.values())
    if not passed:
        raise AssertionError({"pinned_inputs_match": action["pinned_inputs_match"],
            "failed_residuals": {name: str(residuals[name]) for name, ok in checks.items() if not ok}})
    detected = (green["mass_upper_slack"].is_nonnegative is True
        and green["mass_positive_certificate"].is_positive is True
        and green["metric_speed_gap_certificate"].is_nonnegative is True
        and green["Weyl_abs_lower"].is_positive is True)
    return encode(dict(checks_passed=passed, checks=checks,
        healthy_linear_cauchy_gate="FAIL" if detected else "INCONCLUSIVE",
        domain="Every finite K>=1, equivalently0<b<=9/32, on every expanding stiff-plus-positive-Lambda background with m,Hd,a_initial,q0>0 at finite t0. R^3 decay or a flat torus containing the cutoff chart.",
        action=action, geometry=geometry, annular=annular, green=green,
        zero_past_actuator_realization_claimed=False, nonlinear_initial_data_lift_claimed=False,
        infinite_K_or_b_zero_claimed=False, b_negative_claimed=False,
        localized_auxiliary_values_claimed_equal=False,
        amplitude_scope="For each finite K one may choose sufficiently small epsilon; there is no uniform fixed-amplitude K->infinity statement.",
        software=dict(python=platform.python_version(), sympy=s.__version__),
        base_commit=BASE, input_hashes=action["input_hashes"],
        assertion_scope="Action/geometry identities and a uniform analytic short-time support proof. No nonlinear closure, no arbitrary healthy actuator realization, and no equality of all constrained localized auxiliary fields."))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-cauchy-locality", action="store_true")
    args = parser.parse_args(argv)
    result = run()
    print("GENERAL_CANONICAL_CAUCHY_SUPPORT")
    print("Exact checks:", len(result["checks"]), "passed:", result["checks_passed"])
    print("Derived K(b):", result["action"]["kinetic_b"])
    print("Derived b(K):", result["action"]["b_of_K"])
    print("Healthy finite-K Cauchy locality:", result["healthy_linear_cauchy_gate"])
    print("Uniform pre-cone |Weyl_xy| lower bound:", result["green"]["Weyl_abs_lower"])
    return 2 if args.require_cauchy_locality and result["healthy_linear_cauchy_gate"] != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
