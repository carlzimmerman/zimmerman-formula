"""Fixed positive-Lambda adaptive-family retarded signed-probe response.

The input is the actual general-a,q reduced action at the pinned base, never
the older stiff response.  K denotes its canonical scalar kinetic coefficient.
For finite K>=1, m>0, Hd>0, and t0>0, a short smooth external pulse produces
electric Weyl outside the metric light cone from zero past perturbations.
This is an external-response certificate, not a positive-energy matter model.

Uniform Green comparison used below: normalize x=H0(t-s), g=H0 G(t,s).
Then g(0)=0, g'(0)=1 and g''+p g'+c g=0, with 0<=p<=9, 0<c<=18.
Before a first zero of g', one has 0<=g'<=1 and 0<=g<=x.  Integration gives
g'>=1-9x-9x^2>=211/400 on x<=1/20, contradicting such a zero.  Thus
G>=0 and (partial_t+H(t))G>=211/400 there.  The proof uses continuity and
the displayed coefficient bounds, not samples of a numerical solution.
"""
import argparse
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess

import sympy as s

BASE = "c759c46ac02e6c09cd0c7c3cb206b8c31bbc1b97"


def zeros(values):
    return [s.simplify(value) for value in values]


@lru_cache(None)
def derive():
    root = Path(__file__).resolve().parents[3]
    relative = "qwen_claude_field_theory/closure_2026/constraint_response_gate_2026/causal_response.py"
    path = root/relative
    spec = importlib.util.spec_from_file_location("pinned_adaptive_action", path)
    previous = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(previous)
    d = previous.derive_adaptive_action()
    kinematic = previous.derive_adaptive_weyl()
    input_hashes = {}
    for input_path in [path, Path(d["seed_path"])]:
        rel = str(input_path.relative_to(root))
        pinned = subprocess.run(["git", "show", BASE+":"+rel], cwd=root,
                                check=True, capture_output=True).stdout
        current_hash = hashlib.sha256(input_path.read_bytes()).hexdigest()
        input_hashes[rel] = {"current_sha256": current_hash,
                            "base_sha256": hashlib.sha256(pinned).hexdigest()}
    base_matches = all(item["current_sha256"] == item["base_sha256"]
                       for item in input_hashes.values())
    m, K, k, t = (d[key] for key in ["m", "K", "k", "t"])
    Hd = s.Symbol("Hd", positive=True)
    a, q, H = [s.Function(name)(t) for name in ["a_Lambda", "q_Lambda", "H_Lambda"]]
    u, rho, p, j = [s.Function(name)(t) for name in ["u", "R", "P", "j"]]
    Hp = s.diff(H, t)
    # Retain the actual volume factor before varying this general-a,q action.
    full_L = a**3*d["reduced_L"].subs({d["a"]: a, d["q"]: q,
        d["u"]: u, d["ud"]: s.diff(u, t), d["rho"]: rho, d["p"]: p, d["J"]: j})
    background_rules = {s.diff(a, t): H*a, s.diff(q, t): -3*H*q}
    equation = s.simplify((s.diff(s.diff(full_L, s.diff(u, t)), t)
                           -s.diff(full_L, u))/(K*a**3)).subs(background_rules)
    A = ((K+3)*p-4*rho)/q
    expected = (s.diff(u, t, 2)+3*H*s.diff(u, t)
        +(k*k/a**2+3*q*q/(2*m))*u/K-3*q*j/(2*m*K)
        +(s.diff(A, t)+3*H*A)/K).subs(background_rules)
    speed2 = s.simplify(a*a*s.diff(equation, k, 2)/(2*u))
    X = 3*Hd*t
    a_fixed = s.sinh(X)**s.Rational(1, 3)
    q_fixed = s.sqrt(6*m)*Hd/s.sinh(X)
    H_fixed = Hd*s.cosh(X)/s.sinh(X)
    tau_fixed = -3*m*H_fixed
    bg_residuals = zeros([s.diff(a_fixed, t)/a_fixed-H_fixed,
        s.diff(q_fixed, t)+3*H_fixed*q_fixed,
        s.diff(H_fixed, t)+q_fixed*q_fixed/(2*m),
        H_fixed*H_fixed-Hd*Hd-q_fixed*q_fixed/(6*m),
        s.diff(tau_fixed, t)-3*q_fixed*q_fixed/2])

    # Actual physical source uses g=partial_x eta and hence has zero mean.
    # The radial primitive u0 only organizes its dipole moment: u=partial_x u0.
    P = -s.diff(j, t)-3*H*j
    Y, Z = s.Function("Y_radial_moment")(t), s.Function("Z")(t)
    moment = (q*equation.subs({u: Y/q, p: P, k: 0}).doit()).subs({
        s.diff(q, t, 2): (9*H*H-3*Hp)*q, s.diff(q, t): -3*H*q,
        s.diff(rho, t): -3*H*(rho+P)})
    moment = s.simplify(moment).subs(q*q, -2*m*Hp)
    damping = s.simplify(s.diff(moment, s.diff(Y, t)))
    mass = s.simplify(s.diff(moment, Y))
    operator = lambda field: s.diff(field, t, 2)+damping*s.diff(field, t)+mass*field
    source = s.simplify(-moment.subs(Y, 0).doit())
    c = s.simplify(s.diff(source, s.diff(j, t, 2)))
    remainder = s.simplify(source-operator(c*j))
    remainder_control = 12*H*s.diff(j, t)/K+(36*H*H/K+9*Hp/(K*K))*j+12*H*rho/K
    F = s.diff(Y-j, t)+H*(Y-j)
    split_F = s.expand(F.subs(Y, c*j+Z).doit())
    contact = s.simplify(s.diff(split_F, s.diff(j, t)))
    mass_Lambda = s.factor(mass.subs(Hp, -3*(H*H-Hd*Hd)))
    expected_mass = 9*((1+1/K)*H*H+(1-1/K)*Hd*Hd)

    # Build all four covariant Ward components from the FLRW metric itself.
    x, y, z = s.symbols("x y z", real=True)
    coords, spatial = [t, x, y, z], [x, y, z]
    eta = s.Function("eta")(x, y, z)
    g = s.diff(eta, x)
    C = s.Function("C_spatial")(t)
    Sigma = s.zeros(4)
    Sigma[0, 0] = rho*g+C*sum(s.diff(g, v, 2) for v in spatial)
    for i in range(3):
        Sigma[0, i+1] = Sigma[i+1, 0] = j*s.diff(g, spatial[i])/a**2
        Sigma[i+1, i+1] = P*g/a**2
    metric, inverse = s.diag(-1, a*a, a*a, a*a), s.diag(-1, a**-2, a**-2, a**-2)
    Gamma = [[[s.simplify(sum(inverse[i, ell]*(
        s.diff(metric[ell, b], coords[cindex])+s.diff(metric[ell, cindex], coords[b])
        -s.diff(metric[b, cindex], coords[ell]))/2 for ell in range(4)))
        for cindex in range(4)] for b in range(4)] for i in range(4)]
    ward = [sum(s.diff(Sigma[mu, nu], coords[mu])+sum(
        Gamma[mu][mu][ell]*Sigma[ell, nu]+Gamma[nu][mu][ell]*Sigma[mu, ell]
        for ell in range(4)) for mu in range(4)) for nu in range(4)]
    ward_rules = {s.diff(a, t): H*a, s.diff(rho, t): -3*H*(rho+P),
                  s.diff(C, t): -3*H*C-j/a**2}
    kx, ky, kz, phat, jhat, eta_hat = s.symbols("kx ky kz phat jhat eta_hat", real=True)
    kv = s.Matrix([kx, ky, kz])
    transverse = s.eye(3)-kv*kv.T/kv.dot(kv)
    stress = phat*s.eye(3)
    tt = transverse*stress*transverse-transverse*s.trace(transverse*stress)/2
    projections = zeros(transverse*(jhat*kv))+zeros(tt)

    # Certificates use H^2=Hd^2+positive excess and K=1+nonnegative excess.
    hs, H0, a_initial = s.symbols("H H0 a_initial", positive=True)
    w, h_excess = s.symbols("w_nonnegative H2_excess", nonnegative=True)
    source_weights = [s.diff(remainder, s.diff(j, t)), s.diff(remainder, j),
                      s.diff(remainder, rho)]
    weights_Lambda = [s.factor(weight.subs(Hp, -3*(H*H-Hd*Hd)).subs(H, hs))
                      for weight in source_weights]
    positive_certificates = [s.factor(value.subs(K, 1+w)) for value in
                             weights_Lambda+[contact, mass_Lambda.subs(H, hs)]]
    mass_bound = s.simplify(mass.subs(K, 1)/(H*H))
    damping_bound = s.simplify(damping/H)
    slack = s.factor((mass_bound*H*H-mass_Lambda).subs(H, hs)
                     .subs(K, 1+w).subs(hs*hs, Hd*Hd+h_excess))
    normalized_step = s.Rational(1, 20)
    delta = normalized_step/H0
    green_lower = s.simplify(1-damping_bound*normalized_step
                              -mass_bound*normalized_step**2/2)
    xi = s.Symbol("xi", positive=True)
    pulse = s.exp(-delta**2/xi**2)
    F_lower = s.simplify(contact*s.diff(pulse, xi).subs(xi, delta))
    r_event = 1+2*delta/a_initial
    radius, amplitude = s.symbols("radius F_amplitude", positive=True)
    inverse_dipole = s.diff(-amplitude/(4*s.pi*s.sqrt(x*x+y*y+z*z)), x)
    Dxx = s.diff(inverse_dipole, x, 2)-sum(s.diff(inverse_dipole, v, 2) for v in spatial)/3
    Eaxis = s.simplify((d["exterior_weyl_inverse_coefficient"]*Dxx).subs(
        {x: radius, y: 0, z: 0}))
    E_lower = s.simplify(abs(s.diff(Eaxis, amplitude)).subs(radius, r_event)*F_lower)
    initial = {d["u"]: 0, d["ud"]: 0, d["rho"]: 0, d["p"]: 0, d["J"]: 0}
    return dict(K=K, m=m, Hd=Hd, t=t, H=H, H0=H0, a_initial=a_initial, r_event=r_event,
        base_inputs_match=base_matches, input_hashes=input_hashes,
        background=dict(a=a_fixed, q=q_fixed, H=H_fixed, tau=tau_fixed),
        background_residuals=bg_residuals, action_equation=equation,
        action_equation_residual=s.simplify(equation-expected), matter_speed_squared=speed2,
        moment_operator_residual=s.simplify(moment-operator(Y)+source),
        positive_lambda_mass_residual=s.simplify(mass_Lambda-expected_mass),
        mass=mass_Lambda, damping=damping, moment_source=source,
        remainder_source=remainder, remainder_source_residual=s.simplify(remainder-remainder_control),
        contact_coefficient=contact, exterior_amplitude_decomposition=split_F,
        ward_residuals=zeros(value.subs(ward_rules) for value in ward),
        scalar_projection_residuals=projections, zero_mean_profile=(s.I*kx*eta_hat).subs(kx, 0),
        source_onset_jets=[s.limit(s.diff(pulse, xi, order), xi, 0, dir="+") for order in range(4)],
        initial_auxiliary_fields=zeros(value.subs(initial) for value in d["solution"].values()),
        weyl_identity_residuals=kinematic["fourier_weyl_residuals"],
        slicing_variation=kinematic["slicing_variation"], positive_certificates=positive_certificates,
        mass_upper_slack_certificate=slack,
        metric_speed_gap_certificate=s.factor((1-speed2).subs(K, 1+w)),
        normalized_damping_bound=damping_bound, normalized_mass_bound=mass_bound,
        normalized_step=normalized_step, pulse_duration=delta,
        green_derivative_lower_bound=green_lower,
        green_comparison_identity=s.simplify(green_lower-(1-damping_bound*normalized_step
                                                         -mass_bound*normalized_step**2/2)),
        weyl_amplitude_lower_bound=F_lower, electric_weyl_abs_lower_bound=E_lower,
        outside_cone_margin_lower_bound=s.simplify(r_event-1-delta/a_initial),
        dipole_geometry_residual=s.simplify(Eaxis+9*amplitude/(8*s.pi*m*radius**4)),
        exterior_dipole_weyl=Eaxis, source_weights_Lambda=weights_Lambda)


@lru_cache(None)
def numerical_check():
    """Bounded corroboration only: Hd=m=t0=1; three K values; two tolerances."""
    import math
    import numpy as np
    from scipy.integrate import solve_ivp
    d = derive()
    Hfun = lambda time: 1/math.tanh(3*time)
    H0 = Hfun(1.0)
    delta = float(d["normalized_step"])/H0
    # Lambdify the action-derived coefficients, not a fitted or frozen ODE.
    hs = s.Symbol("H_numeric", positive=True)
    mass = s.lambdify((d["K"], hs), d["mass"].subs({d["H"]: hs, d["Hd"]: 1}), "math")
    weights = s.lambdify((d["K"], hs), [value.subs({s.Symbol("H", positive=True): hs,
        d["Hd"]: 1}) for value in d["source_weights_Lambda"]], "math")
    damping_coefficient = float(d["normalized_damping_bound"])
    contact = s.lambdify(d["K"], d["contact_coefficient"], "math")
    result = []
    for kinetic in [1, 9, 100]:
        def integrate(tolerance):
            def rhs(x, state):
                time = 1+delta*x
                H = Hfun(time)
                pulse = math.exp(-1/(x*x)) if x > 0 else 0.0
                pulse_dot = 2*pulse/(delta*x**3) if x > 0 else 0.0
                R, Z, Zd = state
                P = -pulse_dot-3*H*pulse
                w1, w0, wR = weights(kinetic, H)
                source = w1*pulse_dot+w0*pulse+wR*R
                return [delta*(-3*H*(R+P)), delta*Zd,
                        delta*(source-damping_coefficient*H*Zd-mass(kinetic, H)*Z)]
            answer = solve_ivp(rhs, (0, 1), [0, 0, 0], method="DOP853",
                               rtol=tolerance, atol=tolerance*1e-3)
            if not answer.success or not np.all(np.isfinite(answer.y)):
                raise RuntimeError("Positive-Lambda corroboration integration failed")
            R, Z, Zd = answer.y[:, -1]
            H = Hfun(1+delta)
            F = contact(kinetic)*(2/(math.e*delta)+H/math.e)+Zd+H*Z
            return float(F), answer.nfev
        coarse, _ = integrate(1e-9)
        fine, nfev = integrate(1e-11)
        lower = float(d["weyl_amplitude_lower_bound"].subs({d["H0"]: H0, d["K"]: kinetic}))
        result.append(dict(K=kinetic, F=fine, rigorous_F_lower_bound=lower,
            relative_refinement_change=abs(fine-coarse)/abs(fine), nfev=nfev,
            Hd=1, m=1, t0=1, duration=delta))
    return result


def run():
    d = derive()
    residuals = (d["background_residuals"]+d["ward_residuals"]+d["scalar_projection_residuals"]
        +d["source_onset_jets"]+d["initial_auxiliary_fields"]+d["weyl_identity_residuals"]
        +[d[key] for key in ["action_equation_residual", "moment_operator_residual",
          "positive_lambda_mass_residual", "remainder_source_residual", "zero_mean_profile",
          "slicing_variation", "green_comparison_identity", "dipole_geometry_residual"]])
    checked = d["base_inputs_match"] and all(value == 0 for value in residuals)
    certificates = all(value.is_positive is True for value in d["positive_certificates"])
    certificates = certificates and d["mass_upper_slack_certificate"].is_nonnegative is True
    certificates = certificates and d["metric_speed_gap_certificate"].is_nonnegative is True
    detected = (checked and certificates and d["green_derivative_lower_bound"].is_positive is True
                and d["outside_cone_margin_lower_bound"].is_positive is True)
    numerical = numerical_check()
    return dict(base_commit=BASE, input_hashes=d["input_hashes"], sympy_version=s.__version__,
        checks_passed=checked, causal_response_gate="FAIL" if detected else "INCONCLUSIVE",
        domain="All finite K>=1, m>0, Hd>0, t0>0; canonical alpha=1, b=9/[2(K+15)].",
        background={key: str(value) for key, value in d["background"].items()},
        background_residuals=[str(value) for value in d["background_residuals"]],
        actual_action_equation=str(d["action_equation"]),
        stiff_background_response_reused=False,
        moment_variable="Y=q(t) integral u0(t,x) dx; physical mean-zero matter u=partial_x u0.",
        moment_damping=str(d["damping"]), moment_mass=str(d["mass"]),
        moment_source=str(d["moment_source"]), remainder_source=str(d["remainder_source"]),
        contact_coefficient=str(d["contact_coefficient"]),
        exterior_amplitude_decomposition=str(d["exterior_amplitude_decomposition"]),
        source="g=partial_x eta, eta radial smooth supported r<1 with integral1; J=jg, p=Pg, rho=Rg+C Delta g.",
        source_ward_odes="P=-j_dot-3Hj; R_dot+3H(R+P)=0; C_dot+3HC=-j/a^2; retarded zero data.",
        ward_residuals=[str(value) for value in d["ward_residuals"]],
        zero_mode_scope="The physical fields are mean zero. The radial primitive moment is not a homogeneous physical-mode equation.",
        source_pulse="j=0 for t<=t0; exp[-delta^2/(t-t0)^2] through t0+delta; smooth cutoff may follow.",
        pulse_duration=str(d["pulse_duration"]),
        green_definition="G_tt+9H G_t+M(t)G=0, G(s,s)=0, G_t(s,s)=1, and G=0 for t<s.",
        green_proof="Normalize x=H0(t-s), g=H0G. Before a first zero of g', 0<=g'<=1 and 0<=g<=x; hence g'>=1-9x-9x^2. At x<=1/20 this excludes a first zero and gives G_t+HG>=211/400.",
        green_derivative_lower_bound=str(d["green_derivative_lower_bound"]),
        positive_certificates=[str(value) for value in d["positive_certificates"]],
        mass_upper_slack_certificate=str(d["mass_upper_slack_certificate"]),
        event="t=t0+delta; x=1+2delta/a(t0), y=z=0; source starts at t0 in r<1.",
        event_radius=str(d["r_event"]),
        light_cone_radius_bound="Integral_t0^t1 dt/a(t) <=delta/a(t0), since a is increasing.",
        outside_cone_margin_lower_bound=str(d["outside_cone_margin_lower_bound"]),
        strict_Weyl_amplitude_lower_bound=str(d["weyl_amplitude_lower_bound"]),
        strict_abs_Ehat_xx_lower_bound=str(d["electric_weyl_abs_lower_bound"]),
        no_incoming_completion="Source jets and scalar metric auxiliaries vanish before t0. Longitudinal current and isotropic stress have zero transverse/TT projections; set the unsourced vector and TT sectors to zero.",
        numerical_corroboration=numerical, numerics_are_not_the_inequality_proof=True,
        healthy_positive_energy_matter_realization_claimed=False,
        nonlinear_constraint_count_or_global_causality_claimed=False,
        boundary_scope="R^3 spatial decay; linear conserved signed external probe. Compact-torus image kernels not evaluated.",
        amplitude_scope="An arbitrarily small common source amplitude scales the witness and all fields.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-causal-response", action="store_true")
    args = parser.parse_args(argv)
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["checks_passed"]:
        return 1
    return 2 if args.require_causal_response and result["causal_response_gate"] != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
