"""Trace-constrained EH+f: finite Legendre and homogeneous Poisson checks.

Base: 92ff5f9703bfa9fccc1097fcbbc081e004b548ec. All arithmetic is exact.
The six independent h_ij velocities have genuinely independent canonical
momenta: an off-diagonal canonical momentum equals twice pi^ij. Spatial
shift Lie derivatives are absorbed into the six metric velocities.

The global-equivalence argument is analytic, conditional on compact slices
or vanishing surface terms and tau_dot!=0. It is not an executed field-theory
Poisson-matrix calculation. No full inhomogeneous degree-of-freedom count is
assigned, and no seed matter coupling or count is silently inherited.
"""

import json
from functools import lru_cache

import sympy as s


def pb(first, second, coordinates, momenta):
    return s.expand(sum(s.diff(first, q)*s.diff(second, p)
                        - s.diff(first, p)*s.diff(second, q)
                        for q, p in zip(coordinates, momenta)))


@lru_cache(None)
def derive_legendre():
    m, N, h1, h2, h3 = s.symbols("m N h1 h2 h3", positive=True)
    lam, tau, R, f, Lam = s.symbols("lambda tau R f Lambda", real=True)
    metric = s.diag(h1, h2, h3)
    inverse = metric.inv()
    volume = s.sqrt(metric.det())
    velocities = list(s.symbols("u11 u22 u33 u12 u13 u23", real=True))
    momenta = list(s.symbols("p11 p22 p33 p12 p13 p23", real=True))
    p11, p22, p33, p12, p13, p23 = momenta
    u11, u22, u33, u12, u13, u23 = velocities
    pi = s.Matrix([[p11, p12/2, p13/2], [p12/2, p22, p23/2], [p13/2, p23/2, p33]])
    velocity_matrix = s.Matrix([[u11, u12, u13], [u12, u22, u23], [u13, u23, u33]])
    trace_pi = s.trace(pi*metric)
    norm_pi = s.trace(pi*metric*pi*metric)
    H_EH = 2*(norm_pi-trace_pi**2/2)/(m*volume)-m*volume*R/2+m*volume*Lam
    H = N*(H_EH-m*volume*f)+lam*(trace_pi-volume*tau)
    equations = [velocity-s.diff(H, momentum)
                 for velocity, momentum in zip(velocities, momenta)]
    solution = {key: s.factor(value) for key, value in
                s.solve(equations, momenta, dict=True, simplify=False)[0].items()}
    L = s.factor((sum(p*u for p, u in zip(momenta, velocities))-H).subs(solution))
    kcov = velocity_matrix/(2*N)
    kmixed = inverse*kcov
    ktrace = s.trace(kmixed)
    knorm = s.trace(kmixed*kmixed)
    kt_squared = knorm-ktrace**2/3
    lam_solution = s.factor(s.solve(s.diff(L, lam), lam)[0])
    Lred = s.factor(L.subs(lam, lam_solution))

    phi, lambda_v = s.symbols("phi lambda_VCDM", real=True)
    L_vcdm_raw = m*N*volume*((R+knorm-ktrace**2)/2-Lam
                            -3*lambda_v**2/4-lambda_v*(ktrace+phi)+f)
    L_vcdm_reduced = m*N*volume*(R/2+kt_squared/2
                                +s.Rational(2, 3)*phi*ktrace+phi**2/3-Lam+f)
    # VCDM trace primary is derived by differentiating the reduced action.
    vcdm_momenta = [s.diff(L_vcdm_reduced, u) for u in velocities]
    vcdm_trace = h1*vcdm_momenta[0]+h2*vcdm_momenta[1]+h3*vcdm_momenta[2]
    trace_constraint = trace_pi-m*volume*phi
    piT2 = norm_pi-trace_pi**2/3
    H_vcdm = 2*piT2/(m*volume)-m*volume*(R/2+phi**2/3-Lam+f)
    difference = s.factor(H_vcdm-(H_EH-m*volume*f))
    multiplier_shift = (trace_pi+m*volume*phi)/(3*m*volume)
    momentum_hessian = s.hessian(H, momenta)
    hessian_determinant = s.factor(momentum_hessian.det())
    residuals = {
        **{"momentum_variation_"+str(i): s.simplify(equation.subs(solution))
           for i, equation in enumerate(equations)},
        "vcdm_raw_multiplier_map": s.simplify(L-L_vcdm_raw.subs(
            {phi: tau/m, lambda_v: -lam/N}, simultaneous=True)),
        "vcdm_reduced_action": s.simplify(Lred-L_vcdm_reduced.subs(phi, tau/m)),
        "vcdm_trace_primary": s.simplify(vcdm_trace-m*volume*phi),
        "hamiltonian_constraint_multiple": s.simplify(difference-trace_constraint*multiplier_shift),
        "momentum_hessian_inverse": s.simplify(
            sum(entry**2 for entry in momentum_hessian*momentum_hessian.inv()-s.eye(6))),
    }
    return dict(m=m, N=N, metric=metric, volume=volume, tau=tau, lam=lam,
                phi=phi, lambda_VCDM=lambda_v, trace_pi=trace_pi,
                velocities=velocities, momenta=momenta,
                momentum_solution=solution, H=H, L=L,
                lambda_solution=lam_solution, L_reduced=Lred,
                K=ktrace, KT_squared=kt_squared,
                vcdm_raw_L=L_vcdm_raw, vcdm_reduced_L=L_vcdm_reduced,
                trace_constraint=trace_constraint,
                vcdm_hamiltonian_difference=difference,
                hamiltonian_multiplier_shift=multiplier_shift,
                momentum_hessian=momentum_hessian,
                momentum_hessian_determinant=hessian_determinant,
                momentum_hessian_rank=momentum_hessian.rank(),
                residuals=residuals,
                matrix_scope="The six-component momentum Hessian checks the Legendre map only; it is not a constraint count",
                matter_scope="Identical physical minimal matter phase variables and Hamiltonian are appended on both sides; this gravitational map does not recouple matter",
                cosmological_constant_scope="Lambda is an optional constant seed potential; Lambda=0 is the stated zero-potential EH seed")


@lru_cache(None)
def derive_homogeneous():
    volume, N, m = s.symbols("volume N m", positive=True)
    tau, tau_dot, lam, Lam, sigma = s.symbols("tau tau_dot lambda Lambda sigma", real=True)
    vd, sd = s.symbols("volume_dot sigma_dot", real=True)
    pv, ps, pn, pl = s.symbols("p_volume p_sigma p_N p_lambda", real=True)
    q = [volume, sigma, N, lam]
    p = [pv, ps, pn, pl]
    # Derive the EH+canonical-physical-matter homogeneous Hamiltonian before
    # adding the trace multiplier. f=0 identically on homogeneous lapse.
    seed_L = -m*vd**2/(3*N*volume)-m*N*Lam*volume+volume*sd**2/(2*N)
    solution = s.solve([pv-s.diff(seed_L, vd), ps-s.diff(seed_L, sd)], (vd, sd), dict=True)[0]
    H0 = s.factor((pv*vd+ps*sd-seed_L).subs(solution))
    H = H0+lam*(s.Rational(3, 2)*volume*pv-volume*tau)
    C = s.factor(-pb(pn, H, q, p))
    F = s.factor(-2*pb(pl, H, q, p)/(3*volume))
    Cdot = s.factor(pb(C, H, q, p))
    Fdot = s.factor(pb(F, H, q, p)-s.Rational(2, 3)*tau_dot)
    pv_constraint = s.solve(F, pv)[0]
    lambda_constraint = s.solve(C.subs(pv, pv_constraint), Lam)[0]

    def weak(expression):
        return s.factor(expression.subs(pv, pv_constraint).subs(Lam, lambda_constraint))

    weak_Cdot, weak_Fdot = weak(Cdot), weak(Fdot)
    regular = s.solve([weak_Cdot, weak_Fdot], (lam, N), dict=True)[0]
    rho = ps**2/(2*volume**2)
    reduced_lapse = s.factor(regular[N])
    reduced_multiplier = s.factor(regular[lam])
    volume_velocity = s.factor(pb(volume, H, q, p).subs(pv, pv_constraint).subs(lam, reduced_multiplier))
    trace_pair = [F, C]
    pair_matrix = s.Matrix([[weak(pb(a, b, q, p)) for b in trace_pair] for a in trace_pair])
    vacuum = {pv: 0, ps: 0, tau: 0, tau_dot: 0, Lam: 0}
    vacuum_constraints = [s.simplify(expression.subs(vacuum)) for expression in (C, F)]
    vacuum_momentum_drift = s.simplify(pb(pv, H, q, p).subs(vacuum))
    vacuum_volume_velocity = s.simplify(pb(volume, H, q, p).subs(vacuum))
    # Independently specified regular expanding common solution, N=1.
    time = s.symbols("T", positive=True)
    background = {volume: time, N: 1, lam: 0, Lam: 0,
                  tau: -m/time, tau_dot: m/time**2,
                  pv: -2*m/(3*time), ps: s.sqrt(2*m/3)}
    residuals = {
        "homogeneous_lapse_constraint": s.simplify(C-H0/N),
        "homogeneous_trace_constraint": s.simplify(F-(pv-2*tau/3)),
        "secondary_preservation_C": s.simplify(weak_Cdot.subs(regular)),
        "secondary_preservation_F": s.simplify(weak_Fdot.subs(regular)),
        "matter_clock_lapse": s.simplify(reduced_lapse-tau_dot/(3*rho)),
        "extrinsic_trace": s.simplify(volume_velocity/(N*volume)+tau/m),
        "expanding_background_C": s.simplify(C.subs(background)),
        "expanding_background_F": s.simplify(F.subs(background)),
        "expanding_background_Cdot": s.simplify(Cdot.subs(background)),
        "expanding_background_Fdot": s.simplify(Fdot.subs(background)),
        "expanding_background_volume": s.simplify(pb(volume, H, q, p).subs(background)-1),
        "expanding_background_scalar": s.simplify(pb(sigma, H, q, p).subs(background)-s.sqrt(2*m/3)/time),
    }
    return dict(volume=volume, N=N, m=m, tau=tau, tau_dot=tau_dot, lam=lam,
                rho=rho, seed_L=seed_L, H0=H0, H=H, C=C, F=F,
                Cdot=Cdot, Fdot=Fdot, weak_Cdot=weak_Cdot, weak_Fdot=weak_Fdot,
                regular_lapse=reduced_lapse, regular_trace_multiplier=reduced_multiplier,
                regular_domain="volume,N,m>0; p_sigma!=0; tau_dot>0 for the displayed positive-lapse solution",
                trace_pair_poisson_matrix=pair_matrix,
                trace_pair_matrix_scope="Executed bracket of F,C only; not a complete lapse/multiplier or field-theory Dirac matrix",
                volume_velocity=volume_velocity,
                vacuum_constraints=vacuum_constraints,
                vacuum_momentum_drift=vacuum_momentum_drift,
                vacuum_volume_velocity=vacuum_volume_velocity,
                vacuum_scope="tau=0, Lambda=0, p_sigma=p_volume=0: arbitrary lambda changes volume; the VCDM global phi equation would additionally force lambda=0",
                residuals=residuals,
                matter_scope="Exact canonical massless scalar minimal to the physical metric; matter is not inherited from a transformed frame")


@lru_cache(None)
def derive_global_scaling():
    N, q_squared, m, volume, a0, scale = s.symbols("N q_squared m volume a0 scale", positive=True)
    affine_coefficient = s.symbols("affine_coefficient", real=True)
    argument = q_squared/N**2
    f = 2*a0**2*(1-(1+s.sqrt(argument)/a0)*s.exp(-s.sqrt(argument)/a0))
    density = N*affine_coefficient-m*volume*N*f
    scaled_density = density.subs({N: scale*N, q_squared: scale**2*q_squared}, simultaneous=True)
    residuals = {
        "exact_lapse_density_scaling": s.simplify(scaled_density-scale*density),
        "pointwise_euler_identity": s.simplify(
            N*s.diff(density, N)+2*q_squared*s.diff(density, q_squared)-density),
    }
    return dict(lapse_density=density, residuals=residuals,
                executed_evidence="Exact pointwise scaling identities for the actual exponential f; finite six-component Legendre and homogeneous bracket checks are recorded separately",
                boundary_assumption="compact connected spatial slices, or boundary conditions making every displayed integration-by-parts and Hamiltonian surface term vanish; asymptotically flat boundary Hamiltonians are not covered",
                monotone_branch="tau_dot!=0 and an admissible orientation-preserving clock choice",
                global_equivalence_evidence="Conditional analytic argument, not an executed full functional Poisson-matrix calculation",
                analytic_argument=[
                    "Spatially constant rescaling of N leaves a_i=D_i ln N unchanged. The exact density scaling identity makes H0[N] homogeneous of degree one.",
                    "With the stated boundary assumption, Euler integration gives H0=integral N delta(H0)/delta(N), so the lapse equation implies H0=0.",
                    "F=pi-sqrt(h)tau has zero self-bracket. Its preservation gives {F,H0}=sqrt(h)tau_dot, modulo the spatial momentum constraints.",
                    "Preserving H0=0 gives tau_dot integral sqrt(h)lambda=0. On the monotone branch this is the VCDM global phi equation for constant V.",
                    "The zero-mean condition permits restoring a divergence multiplier satisfying D_i lambda_gf^i=-lambda on the stated spatial domain.",
                    "At tau_dot=0 this implication does not follow; the homogeneous vacuum counterexample is separately executed.",
                ])


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


def run():
    results = dict(legendre=derive_legendre(), homogeneous=derive_homogeneous(),
                   global_scaling=derive_global_scaling())
    checks = {section+"."+name: s.simplify(residual) == 0
              for section, result in results.items()
              for name, residual in result["residuals"].items()}
    if not all(checks.values()):
        raise AssertionError({name: passed for name, passed in checks.items() if not passed})
    return encode(dict(algebra_checks_passed=all(checks.values()), checks=checks,
                       results=results,
                       conclusion="Same local VCDM+f action; global equivalence is conditional on the stated boundary and monotone-clock assumptions",
                       scope="Exact finite Legendre and homogeneous preservation evidence, not a full inhomogeneous constraint or stability count"))


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
