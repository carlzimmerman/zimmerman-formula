"""Functional lapse-Hessian screen for a fixed physical MOND potential.

Sources: Iyonaga--Takahashi--Kobayashi, arXiv:1809.10935v2, Eq.84 (affine
A5=0 seed Hamiltonian); Lin--Gong--Lu--Zhang, arXiv:2011.05739v2, Eqs.72--77
(lapse-dependent spatial conformal map and correlated spatial terms).

This module differentiates the physical potential after h_tilde=exp(2w(N))*h
at fixed h_tilde. It assumes a separately established affine seed Hamiltonian;
it does not certify the seed's full constraint algebra or the modified matter
theory. The source's divergence-free-tensor-to-zero inference (86 => 87) is
not used. beta4 in Eq.72 and beta1 in Eq.77 are renamed betaK consistently.

Conventions: standard ADM lapse N>0, h positive definite, smooth finite real
w(N), s=h^{ij}(D_i ln N)(D_j ln N), F=Lie_n N. Positive-s calculations use the
exact exponential kernel. The homogeneous calculation instead uses a fresh
C1 expansion f(s)=f(0)+alpha*s+o(s) at fixed wavelength: exact f_ss is singular
at s=0, and must not be substituted there. Arithmetic is exact symbolic.

The computed rank at y=1 is ONLY the 3x3 potential gradient-Hessian rank.
It is neither a full Dirac rank nor a count of gravitational degrees of freedom.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import platform

import sympy as s


def _symmetric(values):
    x11, x22, x33, x12, x13, x23 = values
    return s.Matrix([[x11, x12, x13], [x12, x22, x23], [x13, x23, x33]])


@lru_cache(None)
def derive_point_transformation():
    """Solve equality of the full symmetric metric symplectic one-forms."""
    N = s.Symbol("N", positive=True)
    w = s.Function("w", real=True)(N)
    hs = s.symbols("h11 h22 h33 h12 h13 h23", real=True)
    ps = s.symbols("pi11 pi22 pi33 pi12 pi13 pi23", real=True)
    pts = s.symbols("pit11 pit22 pit33 pit12 pit13 pit23", real=True)
    dhs = s.symbols("dh11 dh22 dh33 dh12 dh13 dh23", real=True)
    pn, pnt, dN = s.symbols("pN pN_tilde dN", real=True)
    h, pi, pit, dh = map(_symmetric, (hs, ps, pts, dhs))
    mapped_dh = s.exp(2*w)*dh+s.diff(s.exp(2*w), N)*h*dN
    old_form = s.trace(pi*dh)+pn*dN
    new_form = s.trace(pit*mapped_dh)+pnt*dN
    equations = [s.diff(new_form-old_form, differential) for differential in (*dhs, dN)]
    solution = s.solve(equations, (*pts, pnt), dict=True)[0]
    trace = s.trace(pi*h)
    return dict(
        N=N, w=w, h_components=hs, pi_components=ps, pi_trace=trace,
        old_symplectic_form=old_form, transformed_symplectic_form=new_form,
        momentum_map=solution, transformed_lapse_momentum=s.factor(solution[pnt]),
        symplectic_residual=s.simplify((new_form-old_form).subs(solution)),
        primary_relation_residual=s.simplify(solution[pnt]-(pn-2*s.diff(w, N)*trace)),
    )


@lru_cache(None)
def derive_potential():
    """Pull back the actual physical volume/inverse metric, then differentiate."""
    N = s.Symbol("N", positive=True)
    w = s.Function("w", real=True)(N)
    scales = s.symbols("l1 l2 l3", positive=True)
    q = s.symbols("q1 q2 q3", real=True)  # q_i = D_i N, held independent of N in jets
    ht = s.diag(*[a**2 for a in scales])
    hit = ht.inv()
    h = s.exp(-2*w)*ht
    volume_t = s.prod(scales)
    volume = s.simplify(s.sqrt(h.det()))
    qvector = s.Matrix(q)
    physical_s = s.simplify((qvector.T*h.inv()*qvector)[0]/N**2)
    z = s.exp(2*w)*(qvector.T*hit*qvector)[0]/N**2
    f, zvar = s.Function("f"), s.Symbol("z")
    P = N*volume/volume_t*f(physical_s)
    expected_P = N*s.exp(-3*w)*f(z)
    Q = s.hessian(P, q)
    fp = s.Subs(s.diff(f(zvar), zvar), zvar, z)
    fpp = s.Subs(s.diff(f(zvar), zvar, 2), zvar, z)
    at = hit*qvector/N
    expected_Q = 2*s.exp(-w)/N*(fp*hit+2*s.exp(2*w)*fpp*at*at.T)
    Fs, Fss = s.symbols("f_s f_ss", real=True)
    # Q contains derivatives evaluated at the actual, algebraically factored
    # physical_s. Replace those complete Subs nodes without SymPy's nested
    # derivative-substitution semantics, using that exact argument.
    actual_fp = s.Subs(s.diff(f(zvar), zvar), zvar, physical_s)
    actual_fpp = s.Subs(s.diff(f(zvar), zvar, 2), zvar, physical_s)
    coefficient_Q = Q.xreplace({actual_fp: Fs, actual_fpp: Fss})
    return dict(
        N=N, w=w, scales=scales, q=q, ht=ht, hit=hit, h=h,
        volume=volume, volume_t=volume_t, f=f, z=z, P=P,
        physical_s=physical_s, gradient_hessian=Q,
        coefficient_hessian=coefficient_Q, Fs=Fs, Fss=Fss,
        pullback_residual=s.simplify(P-expected_P),
        acceleration_pullback_residual=s.simplify(physical_s-z),
        volume_pullback_residual=s.simplify(volume/volume_t-s.exp(-3*w)),
        gradient_hessian_residuals=[s.simplify(v) for v in Q-expected_Q],
    )


@lru_cache(None)
def derive_homogeneous():
    """Recompute the second variation from C1 data at homogeneous lapse."""
    d = derive_potential()
    N, alpha = d["N"], s.Symbol("alpha", real=True)
    M, a, k = s.symbols("M a k", positive=True)
    w0, e, n, theta, x = s.symbols("w0 epsilon n theta x", real=True)
    eta = s.Function("eta")(x)
    f0 = s.Symbol("f0", real=True)
    lapse = N+e*eta
    # Variations of w contribute only at cubic order to the gradient sector,
    # because grad(Nbar)=0. f(0) is affine in original N before the transform;
    # its transformed algebraic Hessian cannot change this principal symbol.
    field_w = d["w"].subs(N, lapse)
    physical_s = s.exp(2*field_w)*s.diff(lapse, x)**2/(a**2*lapse**2)
    added_H = -M**2*a**3*lapse*s.exp(-3*field_w)*alpha*physical_s
    H2 = s.simplify(s.diff(added_H, e, 2).subs(e, 0)/2).subs(d["w"], w0)
    variation = s.simplify(s.diff(H2, eta)-s.diff(s.diff(H2, s.diff(eta, x)), x))
    mode_H2 = H2.subs({s.diff(eta, x): -n*k*s.sin(theta), eta: n*s.cos(theta)})
    mode_H = s.simplify(s.integrate(mode_H2, (theta, 0, 2*s.pi))/s.pi)
    symbol = s.simplify(s.diff(mode_H, n, 2))
    functional_symbol = s.simplify(variation.subs(s.diff(eta, x, 2),
                                                  -n*k**2*s.cos(theta))/(n*s.cos(theta)))
    return dict(
        N=N, M=M, a=a, k=k, w0=w0, alpha=alpha,
        quadratic_gradient_density=H2, functional_variation=variation,
        mode_hamiltonian=mode_H, hamiltonian_symbol=symbol,
        mode_functional_residual=s.simplify(symbol-functional_symbol),
        homogeneous_zero_mode_symbol=symbol.subs(k, 0),
        regularity="C1 f at s=0; amplitude limit before wavelength limit; no evaluation of f_ss(0)",
    )


@lru_cache(None)
def derive_anisotropy():
    """Evaluate the actual tensor Hessian in an orthonormal frame at s>0."""
    d = derive_potential()
    y, a0 = s.symbols("y a0", positive=True)
    kernel = 2*a0**2*(1-(1+y)*s.exp(-y))
    fs = s.simplify(s.diff(kernel, y)/(2*a0**2*y))
    fss = s.simplify(s.diff(fs, y)/(2*a0**2*y))
    frame = {**dict.fromkeys(d["scales"], 1), d["q"][0]: d["N"]*s.exp(-d["w"])*a0*y,
             d["q"][1]: 0, d["q"][2]: 0}
    Qaxis = d["coefficient_hessian"].subs(frame).subs({d["Fs"]: fs, d["Fss"]: fss})
    Qaxis = Qaxis.applyfunc(s.simplify)
    factor = 2*s.exp(-d["w"])/d["N"]
    longitudinal = s.simplify(Qaxis[0, 0]/factor)
    tangential = s.simplify(Qaxis[1, 1]/factor)
    expected = factor*s.diag(fs+2*a0**2*y**2*fss, fs, fs)
    at_one = Qaxis.subs(y, 1)
    mu = 1-fs
    return dict(
        y=y, a0=a0, kernel=kernel, fs=fs, fss=fss,
        mond_alpha=s.limit(fs, y, 0, dir="+"),
        axis_hessian=Qaxis, positive_prefactor=factor,
        potential_hessian_eigenvalues=Qaxis.eigenvals(),
        longitudinal_normalized=longitudinal, tangential_normalized=tangential,
        longitudinal_positive_roots=s.solve(longitudinal, y),
        tangential_positive_roots=s.solve(tangential, y),
        potential_hessian_rank_at_y1=at_one.rank(),
        potential_hessian_determinant_at_y1=s.simplify(at_one.det()),
        anisotropic_hessian_residuals=[s.simplify(v) for v in Qaxis-expected],
        mond_transverse=mu, mond_radial=s.simplify(mu+y*s.diff(mu, y)),
    )


@lru_cache(None)
def derive_matter():
    """Legendre-transform a minimally coupled canonical scalar in physical h."""
    d = derive_potential()
    velocity, momentum, potential = s.symbols("sigma_dot p_sigma V_sigma", real=True)
    gradient = s.Matrix(s.symbols("sigma_1 sigma_2 sigma_3", real=True))
    shift = s.Matrix(s.symbols("shift1 shift2 shift3", real=True))
    drift = (shift.T*gradient)[0]
    spatial = (gradient.T*d["h"].inv()*gradient)[0]
    L = d["N"]*d["volume"]*((velocity-drift)**2/(2*d["N"]**2)-spatial/2-potential)
    raw_momentum = s.diff(L, velocity)
    solved_velocity = s.solve(momentum-raw_momentum, velocity)[0]
    H = s.simplify((momentum*velocity-L).subs(velocity, solved_velocity))
    return dict(
        lagrangian=L, hamiltonian=H,
        matter_momentum_residual=s.simplify(raw_momentum.subs(velocity, solved_velocity)-momentum),
        matter_velocity_residual=s.simplify(s.diff(H, momentum)-solved_velocity),
        gradient_lapse_hessian=s.hessian(H, d["q"]),
        algebraic_lapse_hessian=s.diff(H, d["N"], 2),
        scope="Canonical scalar exemplar: no DiN principal term; algebraic lapse dependence remains. No full matter constraint count.",
    )


def run():
    """Return JSON-ready results without writing files or assigning DOF counts."""
    point, potential = derive_point_transformation(), derive_potential()
    homogeneous, anisotropy, matter = derive_homogeneous(), derive_anisotropy(), derive_matter()
    checks = {
        "symplectic_form": point["symplectic_residual"] == 0,
        "primary_momentum_relation": point["primary_relation_residual"] == 0,
        "physical_potential_pullback": potential["pullback_residual"] == 0,
        "physical_acceleration_pullback": potential["acceleration_pullback_residual"] == 0,
        "physical_volume_pullback": potential["volume_pullback_residual"] == 0,
        "all_gradient_hessian_components": potential["gradient_hessian_residuals"] == [0]*9,
        "homogeneous_functional_mode_agreement": homogeneous["mode_functional_residual"] == 0,
        "exact_mond_slope": anisotropy["mond_alpha"] == 1,
        "exact_anisotropic_hessian": anisotropy["anisotropic_hessian_residuals"] == [0]*9,
        "longitudinal_zero_is_y1": anisotropy["longitudinal_positive_roots"] == [1],
        "no_finite_transverse_zero": anisotropy["tangential_positive_roots"] == [],
        "matter_legendre_inverse": matter["matter_momentum_residual"] == 0,
        "matter_hamilton_velocity": matter["matter_velocity_residual"] == 0,
        "matter_has_no_gradient_lapse_hessian": matter["gradient_lapse_hessian"] == s.zeros(3),
    }
    symbol = homogeneous["hamiltonian_symbol"].subs(homogeneous["alpha"], anisotropy["mond_alpha"])
    return {
        "name": "transformed_affine_seed_fixed_physical_lapse_potential",
        "software": {"python": platform.python_version(), "sympy": s.__version__},
        "arithmetic": "exact symbolic, no sampling",
        "source": {
            "urls": ["https://arxiv.org/html/1809.10935v2", "https://arxiv.org/html/2011.05739v2"],
            "versions": ["1809.10935v2 (2018-12-05), Eq.84", "2011.05739v2 (2021-03-11), Eqs.72-77"],
            "verification_scope": "restriction_equations_and_point_transformation_not_dof_certification",
            "caveats": ["Eq.86 divergence-free momentum tensor plus boundary decay does not imply Eq.87 tensor zero; this inference is not used.",
                        "Eq.72 beta4 versus Eq.77 beta1 is a trace-coefficient index mismatch; use betaK consistently.",
                        "Eq.2 omits the lapse square; standard ADM lapse convention is used."],
        },
        "checks": checks, "checks_passed": all(checks.values()),
        "two_tensor_gate": "FAIL" if symbol != 0 else "NOT_REFUTED",
        "assumption": "Separately audited A5=0 affine seed; no re-certification of its full constraint algebra",
        "momentum_relation": "pN_tilde = pN - 2*w_N*pi, pi=h_ij*pi^ij",
        "potential_pullback": str(potential["P"]),
        "homogeneous_mond_hamiltonian_symbol": str(symbol),
        "wavevector_convention": "comoving k, h_tilde=a^2 delta; physical seed k_tilde=k/a",
        "anisotropy": {
            "scope": "Eigenvalues of P_qiqj only, not MOND operator eigenvalues or Dirac rank",
            "common_positive_prefactor": str(anisotropy["positive_prefactor"]),
            "transverse_normalized": str(anisotropy["tangential_normalized"]),
            "longitudinal_normalized": str(anisotropy["longitudinal_normalized"]),
            "positive_longitudinal_zeros": [str(v) for v in anisotropy["longitudinal_positive_roots"]],
            "positive_transverse_zeros": [str(v) for v in anisotropy["tangential_positive_roots"]],
            "potential_hessian_rank_at_y1": anisotropy["potential_hessian_rank_at_y1"],
            "mond_radial_coefficient_at_y1": str(anisotropy["mond_radial"].subs(anisotropy["y"], 1)),
        },
        "matter_gradient_lapse_hessian_zero": matter["gradient_lapse_hessian"] == s.zeros(3),
        "matter_scope": matter["scope"],
        "full_constraint_count_claimed": False,
        "domain": "N,a,M>0; smooth finite real w; homogeneous symbol k!=0; anisotropy y>0",
        "limitations": ["No modified-action nonlinear DOF count or stability certificate",
                        "k=0 supplies zero principal symbol, not a homogeneous constraint count",
                        "The y=1 longitudinal zero is a potential-Hessian rank change, not restored two-tensor degeneracy",
                        "No restriction proved for nonconformal or gradient-dependent kinetic transformations"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-two-tensor", action="store_true")
    parser.add_argument("--output", type=Path, help="Create a new JSON result exclusively")
    args = parser.parse_args(argv)
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output is None:
        print(payload, end="")
    else:
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(payload)
    if not result["checks_passed"]:
        return 1
    return 2 if args.require_two_tensor and result["two_tensor_gate"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
