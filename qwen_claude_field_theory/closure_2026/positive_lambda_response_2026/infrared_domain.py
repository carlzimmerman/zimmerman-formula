"""Nonlinear R^3 domain screen for -b*tau_T/24 <K^-1 I,K^-1 I>_h.

Input: N=1, h=e^(2 zeta) delta, I=R_h, K=-Delta_h with the unprojected
decaying Poisson inverse, and smooth compactly supported nonconstant zeta.
The field is an off-shell domain probe, not a solution or physical initial datum.

A useful exact path is zeta=2 log(1+epsilon psi), epsilon>0, psi>=0 smooth
radial compact and nonconstant.  Write A=int_0^1 r^2 psi'(r)^2 dr>0.
For example take psi proportional to exp[-1/(1-r^2)] inside r<1 and zero
outside.  Dividing that bump by sqrt(A_raw) makes A=1 exactly.  This is a
fixed smooth profile; h=(1+epsilon psi)^4 delta tends to delta in every
fixed C^k norm as epsilon tends to zero, with fixed compact support.

The squared Poisson potential has an O(epsilon^4) linear radial divergence.
Consequently this unprojected decaying functional has no open neighborhood
containing all such compact-conformal off-shell perturbations.  This is not
an exclusion of all theories, projected compact spaces, or on-shell solutions.
"""
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path

import sympy as s

BASE = "c759c46ac02e6c09cd0c7c3cb206b8c31bbc1b97"


@lru_cache(None)
def derive():
    x, y, z = s.symbols("x y z", real=True)
    coords = [x, y, z]
    zeta = s.Function("zeta", real=True)(x, y, z)
    metric, inverse = s.exp(2*zeta)*s.eye(3), s.exp(-2*zeta)*s.eye(3)
    volume = s.exp(3*zeta)
    connection = [[[s.simplify(sum(inverse[i, ell]*(
        s.diff(metric[ell, b], coords[c])+s.diff(metric[ell, c], coords[b])
        -s.diff(metric[b, c], coords[ell]))/2 for ell in range(3)))
        for c in range(3)] for b in range(3)] for i in range(3)]
    ricci_tensor = s.Matrix(3, 3, lambda i, j: sum(
        s.diff(connection[ell][i][j], coords[ell])-s.diff(connection[ell][i][ell], coords[j])
        +sum(connection[ell][i][j]*connection[n][ell][n]
             -connection[ell][i][n]*connection[n][ell][j] for n in range(3))
        for ell in range(3)))
    ricci = s.simplify(sum(inverse[i, j]*ricci_tensor[i, j]
                           for i in range(3) for j in range(3)))
    lap = lambda f: sum(s.diff(f, coordinate, 2) for coordinate in coords)
    grad2 = lambda f: sum(s.diff(f, coordinate)**2 for coordinate in coords)
    div_weighted_grad = sum(s.diff(s.exp(zeta)*s.diff(zeta, coordinate), coordinate)
                            for coordinate in coords)
    bulk = s.simplify(volume*ricci+4*div_weighted_grad)
    epsilon, A = s.symbols("epsilon A_radial_energy", positive=True)
    psi = s.Function("psi", real=True)(x, y, z)
    phi = 1+epsilon*psi
    profile_zeta = 2*s.log(phi)
    profile_ricci = s.simplify(ricci.subs(zeta, profile_zeta).doit())
    profile_density = s.simplify((volume*ricci).subs(zeta, profile_zeta).doit())
    profile_divergence = sum(s.diff(phi*s.diff(psi, coordinate), coordinate)
                             for coordinate in coords)
    profile_bulk = s.simplify(bulk.subs(zeta, profile_zeta).doit())
    energy_coefficient = s.simplify(profile_bulk/grad2(psi))
    # Compact support removes the explicit divergence.  Spherical integration
    # gives int_R3 |grad psi|^2 = 4*pi*A for a radial profile.
    profile_charge = s.factor(energy_coefficient*4*s.pi*A)

    r, R, L1, L2, Q = s.symbols("r R L1 L2 Q", positive=True)
    theta, azimuth = s.symbols("theta azimuth", real=True)
    wr = s.Function("zeta_radial")(r)
    V = s.Function("V")(r)
    spherical_metric = s.exp(2*wr)*s.diag(1, r*r, r*r*s.sin(theta)**2)
    spherical_inverse = spherical_metric.inv()
    # This volume element is positive for 0<theta<pi; coordinate poles have
    # zero measure and are not singularities of the smooth Cartesian metric.
    spherical_volume = s.exp(3*wr)*r*r*s.sin(theta)
    spherical_coords = [r, theta, azimuth]
    curved_laplace = s.simplify(sum(s.diff(spherical_volume*spherical_inverse[i, i]
        *s.diff(V, spherical_coords[i]), spherical_coords[i]) for i in range(3))/spherical_volume)
    curved_flux_residual = s.simplify(-r*r*s.exp(3*wr)*curved_laplace
                                     +s.diff(r*r*s.exp(wr)*s.diff(V, r), r))
    radial_R = s.exp(-2*wr)*(-4*(s.diff(wr, r, 2)+2*s.diff(wr, r)/r)-2*s.diff(wr, r)**2)
    integration_r = s.Dummy("s", positive=True)
    ws = s.Function("zeta_radial")(integration_r)
    enclosed = -16*s.pi*r*r*s.exp(wr)*s.diff(wr, r)+8*s.pi*s.Integral(
        integration_r**2*s.exp(ws)*s.diff(ws, integration_r)**2, (integration_r, 0, r))
    enclosed_residual = s.simplify(s.diff(enclosed, r)-4*s.pi*r*r*s.exp(3*wr)*radial_R)
    # -4*pi*r^2*exp(zeta)*V'=M(r).  Outside support M=Q and zeta=0.
    # Integrating the resulting derivative with V(infinity)=0 fixes its sign.
    exterior = s.integrate(Q/(4*s.pi*integration_r**2), (integration_r, r, s.oo))
    exterior_flux = s.simplify(-4*s.pi*r*r*s.diff(exterior, r)-Q)
    shell_norm = s.simplify(4*s.pi*s.integrate(r*r*exterior**2, (r, L1, L2)))
    b, tau_T = s.symbols("b tau_T", positive=True)
    shell_action = s.factor(-b*tau_T*shell_norm/24)
    profile_action_slope = s.factor(s.diff(shell_action, L2).subs(Q, profile_charge))
    profile_norm_slope = s.factor(s.diff(shell_norm, L2).subs(Q, profile_charge))
    amplitude_jets = [s.simplify(s.diff(profile_action_slope, epsilon, order).subs(epsilon, 0))
                      for order in range(7)]
    nonzero_order = next(order for order, value in enumerate(amplitude_jets) if value != 0)
    gradient_tail = s.simplify(4*s.pi*s.integrate(r*r*s.diff(exterior, r)**2, (r, R, s.oo)))

    # A smooth zero-monopole control: I=partial_z rho0 with rho0 radial compact
    # and integral d.  Its exterior potential is the derivative of d/(4*pi*r),
    # not a point-dipole prescription for the interior.  Elliptic regularity
    # for that smooth source supplies a regular, finite-norm interior.
    dipole_strength = s.Symbol("dipole_strength", positive=True)
    cartesian_radius = s.sqrt(x*x+y*y+z*z)
    dipole_cartesian = s.diff(dipole_strength/(4*s.pi*cartesian_radius), z)
    dipole = -dipole_strength*s.cos(theta)/(4*s.pi*r*r)
    angular_norm = s.simplify(2*s.pi*s.integrate(dipole**2*s.sin(theta), (theta, 0, s.pi)))
    dipole_flux = s.simplify(-2*s.pi*r*r*s.integrate(s.diff(dipole, r)*s.sin(theta),
                                                    (theta, 0, s.pi)))
    dipole_tail = s.simplify(s.integrate(r*r*angular_norm, (r, R, s.oo)))
    return dict(epsilon=epsilon, A=A, b=b, tau_T=tau_T, Q=Q, r=r, R=R, L1=L1, L2=L2,
        dipole_strength=dipole_strength, ricci=ricci, volume_density=volume*ricci,
        ricci_residual=s.simplify(ricci-s.exp(-2*zeta)*(-4*lap(zeta)-2*grad2(zeta))),
        density_ibp_residual=s.simplify(volume*ricci+4*div_weighted_grad-2*s.exp(zeta)*grad2(zeta)),
        phi_curvature_residual=s.simplify(profile_ricci+8*epsilon*lap(psi)/phi**5),
        phi_density_ibp_residual=s.simplify(profile_density+8*epsilon*profile_divergence
                                          -8*epsilon**2*grad2(psi)),
        profile_charge=profile_charge, profile_ricci=profile_ricci,
        background_metric_residual=(phi**4*s.eye(3)).subs(epsilon, 0)-s.eye(3),
        curved_laplacian=curved_laplace, curved_flux_residual=curved_flux_residual,
        enclosed_charge=enclosed, enclosed_charge_derivative_residual=enclosed_residual,
        exterior_potential=exterior, exterior_flux_residual=exterior_flux,
        shell_norm=shell_norm, shell_action=shell_action,
        norm_limit=s.limit(shell_norm.subs(L1, R), L2, s.oo),
        action_limit=s.limit(shell_action.subs(L1, R), L2, s.oo),
        profile_norm_slope=profile_norm_slope, profile_action_slope=profile_action_slope,
        first_nonzero_amplitude_order=nonzero_order, zero_amplitude_jets=amplitude_jets[:4],
        fourth_amplitude_derivative=amplitude_jets[4],
        monopole_gradient_tail=gradient_tail,
        dipole_laplace_residual=s.simplify(lap(dipole_cartesian)),
        dipole_flux=dipole_flux, dipole_tail_norm=dipole_tail,
        dipole_shell_norm=s.simplify(s.integrate(r*r*angular_norm, (r, L1, L2))))


def run():
    d = derive()
    residuals = [d[key] for key in ["ricci_residual", "density_ibp_residual",
        "phi_curvature_residual", "phi_density_ibp_residual", "curved_flux_residual",
        "enclosed_charge_derivative_residual", "exterior_flux_residual",
        "dipole_laplace_residual", "dipole_flux"]]
    checked = all(value == 0 for value in residuals)
    checked = checked and d["background_metric_residual"] == s.zeros(3)
    detected = (checked and d["profile_charge"].is_positive is True
                and d["norm_limit"] == s.oo and d["action_limit"] == -s.oo)
    return dict(base_commit=BASE,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        sympy_version=s.__version__, checks_passed=checked,
        unprojected_R3_domain_gate="FAIL" if detected else "INCONCLUSIVE",
        domain="N=1; smooth compact nonconstant conformal metric; unprojected decaying R^3 inverse; b*tau_T>0.",
        actual_curvature=str(d["ricci"]),
        compact_support_IBP="Integral sqrt(h) R_h = 2 integral exp(zeta)|grad zeta|^2 > 0.",
        explicit_path="zeta=2 log(1+epsilon psi), h=(1+epsilon psi)^4 delta, epsilon>0, psi smooth nonnegative radial compact nonconstant.",
        computable_profile="psi=c exp[-1/(1-r^2)] for r<1, zero outside. c=1/sqrt(A_raw) gives A=integral r^2 psi'^2 dr=1 exactly.",
        normalization_integral="A_raw=integral_0^1 4r^4 exp[-2/(1-r^2)]/(1-r^2)^4 dr, positive and finite.",
        exact_profile_charge=str(d["profile_charge"]),
        curved_radial_laplacian=str(d["curved_laplacian"]),
        enclosed_charge=str(d["enclosed_charge"]),
        regular_solution="M(r)=integral_Br sqrt(h)I; V'=-M/(4pi r^2 exp(zeta)); V(r)=integral_r^infinity M(s)/(4pi s^2 exp(zeta(s))) ds. Smooth radial data give M=O(r^3), so the center is regular.",
        exterior_monopole=str(d["exterior_potential"]),
        shell_conditions="L2>L1>support radius; the exterior metric is exactly Euclidean.",
        exact_shell_squared_norm=str(d["shell_norm"]),
        exact_second_action_difference=str(d["shell_action"]),
        clock_time_scope="The displayed action differences are densities per dT. A smooth epsilon(T)>0 on an interval where b*tau_T>0 gives a negative, nonzero integrated cutoff slope; the full time-integrated term then also diverges.",
        norm_limit=str(d["norm_limit"]), second_action_limit=str(d["action_limit"]),
        profile_norm_cutoff_slope=str(d["profile_norm_slope"]),
        profile_second_action_cutoff_slope=str(d["profile_action_slope"]),
        first_nonzero_amplitude_order=d["first_nonzero_amplitude_order"],
        amplitude_derivatives_orders_0_through_3=[str(value) for value in d["zero_amplitude_jets"]],
        fourth_amplitude_derivative=str(d["fourth_amplitude_derivative"]),
        first_kernel_term_control="I has compact support and V is regular there, so <I,V> is finite. Its cutoff stops changing beyond the support; it cannot cancel the second term's linear tail.",
        monopole_gradient_tail=str(d["monopole_gradient_tail"]),
        sufficient_finite_control="With smooth regular interior and flat exterior, zero total monopole removes r^-1. Exterior dipole O(r^-2) and higher multipoles have finite squared norm.",
        smooth_dipole_source="Flat control I=partial_z rho0, rho0 smooth radial compact with integral dipole_strength; integral I=0.",
        exact_dipole_tail_squared_norm=str(d["dipole_tail_norm"]),
        exact_dipole_shell_squared_norm=str(d["dipole_shell_norm"]),
        neighborhood_conclusion="No open compact-conformal off-shell neighborhood of the flat FLRW slice lies in this unprojected squared-inverse domain: the fixed-support smooth path approaches the background as epsilon tends to zero.",
        inverse_domain_alternative="If K^-1 is defined only on zero-monopole/L2-compatible sources, these data are excluded from its domain rather than assigned a finite action.",
        all_onshell_perturbations_excluded=False, compact_projected_theories_excluded=False,
        all_nonlocal_theories_excluded=False, no_solution_theorem_claimed=False,
        scope_caveat="No field equations are imposed. A compact torus, projected inverse, or explicit infrared prescription is a different domain and is not tested here.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-finite-domain", action="store_true")
    args = parser.parse_args(argv)
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["checks_passed"]:
        return 1
    return 2 if args.require_finite_domain and result["unprojected_R3_domain_gate"] != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
