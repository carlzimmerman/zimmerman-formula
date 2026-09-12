#!/usr/bin/env python3
"""Independent unitary-chi quadratic ADM action and archived gauge cross-check.

No history or coefficient function is reconstructed. The exact spatial plane
mode is used only to represent the scalar quadratic sector.
"""
import json
import platform
from pathlib import Path
import sympy as S


def derive():
    checks = {}

    def zero(name, expression):
        rem = S.factor(S.cancel(S.expand(expression)))
        checks[name] = rem == 0
        if rem != 0:
            raise AssertionError((name, rem))

    a, q = S.symbols("a q", positive=True)
    M, gamma, H, Hd, qd = S.symbols("M2 gamma H Hdot qdot", real=True)
    e = S.symbols("epsilon", real=True)
    z, zd, zx, zxx, n, nx = S.symbols("z zd zx zxx n nx", real=True)
    sig, sd, sx, beta, ell = S.symbols("sigma sd sx beta Bxx", real=True)
    F, PX, PXX, Ft, PXt, Ftt = S.symbols("F PX PXX Ft PXt Ftt", real=True)
    W, WY, Wt, Wtt = S.symbols("W WY Wt Wtt", real=True)
    N = 1+e*n
    conf = S.exp(e*z)
    vol = a**3*conf**3
    flow = H+e*zd-e**2*beta*zx
    Kx, Ky = (flow-e*ell)/N, flow/N
    K = Kx+2*Ky
    R3 = (-4*e*zxx-2*e**2*zx**2)/(a*a*conf**2)
    X = q*q/N**2
    dX = X-q*q
    clock_T = 1+e*sd-e**2*beta*sx
    clock_s2 = clock_T**2/N**2-e**2*sx**2/(a*a*conf**2)
    clock_s = S.sqrt(clock_s2)
    Y = (q*q/N**2)*(e**2*sx**2/(a*a*conf**2))/clock_s2
    PminusV = F+PX*dX+PXX*dX*dX/2+Ft*e*sig+PXt*dX*e*sig+Ftt*e**2*sig**2/2
    Wfun = W+Wt*e*sig+Wtt*e**2*sig**2/2+WY*Y
    cubic = -S.Rational(2, 3)*gamma*(q/N)**3*K
    sectors = {
        "EH": N*vol*M*(Kx*Kx+2*Ky*Ky-K*K+R3)/2,
        "P_V": N*vol*PminusV,
        "clock": N*vol*clock_s*Wfun,
        "cubic": N*vol*cubic,
    }
    jets = {name: S.expand(S.diff(lag, e, 2).subs(e, 0)/2/a**3)
            for name, lag in sectors.items()}
    raw = S.expand(sum(jets.values()))
    # Spatial integration by parts, coefficients depend only on time.
    spatial = S.expand(raw.subs({beta*zx: -ell*z, beta*sx: -ell*sig,
                                n*zxx: -nx*zx, z*zxx: -zx*zx}))
    # Individual cross monomials are replaced separately to avoid accidental
    # matching through a coefficient containing the same formal variables.
    cz = S.expand(spatial).coeff(zd, 1).coeff(z, 1)
    cs = S.expand(spatial).coeff(sd, 1).coeff(sig, 1)
    czs = S.expand(spatial).coeff(sd, 1).coeff(z, 1)
    zero("z_zdot_coefficient", cz+18*M*H+6*gamma*q**3)
    zero("sigma_sigmadot_coefficient", cs-Wt)
    zero("z_sigmadot_coefficient", czs-3*W)
    czdot = S.diff(cz, H)*Hd+S.diff(cz, q)*qd
    after_ibp = S.expand(spatial-cz*z*zd-cs*sig*sd-czs*z*sd
                         -(3*H*cz+czdot)*z*z/2
                         -(3*H*Wt+Wtt)*sig*sig/2
                         -3*W*sig*zd-(9*H*W+3*Wt)*z*sig)

    c = gamma*q**3
    Theta = M*H+c
    Sigma = q*q*PX+2*q**4*PXX-3*M*H*H-12*H*c
    C = Ft-2*q*q*PXt
    D = Ftt-3*H*Wt
    Sclock = W-2*q*q*WY
    E0 = 3*M*H*H+6*H*c+F-2*q*q*PX
    Ea = M*(2*Hd+3*H*H)+F+W+2*gamma*q*q*qd
    Et = Ft-3*H*W
    compact = (-3*M*zd*zd+6*Theta*n*zd+Sigma*n*n
               +2*(M*zd-Theta*n)*ell+M*(zx*zx+2*nx*zx)/a**2
               +C*n*sig-3*W*sig*zd+W*sig*ell+D*sig*sig/2
               -Sclock*sx*sx/(2*a*a))
    tadpoles = 3*E0*n*z+3*Et*z*sig+S.Rational(9, 2)*Ea*z*z
    zero("full_quadratic_action_including_tadpoles", after_ibp-compact-tadpoles)
    zero("no_clock_time_kinetic", S.diff(after_ibp, sd, 2))
    zero("no_clock_time_derivative_after_IBP", S.diff(after_ibp, sd))
    zero("clock_spatial_block", S.diff(compact, sx, 2)+Sclock/a**2)

    # Exact cubic ADM integration by parts in unitary chi.
    Q, normal_Q, Ksym = S.symbols("Q normal_Q K", real=True)
    raw_covariant = -gamma*Q*Q*normal_Q-gamma*Q**3*Ksym
    reduced_covariant = -S.Rational(2, 3)*gamma*Q**3*Ksym
    boundary_divergence = -gamma*(3*Q*Q*normal_Q+Q**3*Ksym)/3
    zero("cubic_ADM_covariant_boundary_identity",
         raw_covariant-reduced_covariant-boundary_divergence)
    Lhom = a**3*(-3*M*H**2+F+W-2*gamma*H*q**3)
    zero("homogeneous_action_control", sum(lag.subs(e, 0) for lag in sectors.values())-Lhom)

    # Real cosine amplitude convention. All products average to one half.
    k = S.symbols("k", real=True)
    averaged = a**3*S.expand(compact.subs({zx*zx: k*k*z*z,
                       nx*zx: k*k*n*z, sx*sx: k*k*sig*sig}))/2
    nsol = (M*zd+W*sig/2)/Theta
    zero("shift_constraint_lapse", S.diff(averaged, ell).subs(n, nsol))
    aux = S.hessian(averaged, (n, ell))
    zero("lapse_shift_hessian_determinant_Bxx", aux.det()+a**6*Theta**2)
    after_shift = S.factor(averaged.subs(n, nsol))
    zero("shift_multiplier_drops", S.diff(after_shift, ell))
    Bhat = 2*PX+4*q*q*PXX-12*gamma*H*q+6*gamma**2*q**4/M
    Kchi = a**3*M*M*q*q*Bhat/(2*Theta*Theta)
    zero("unitary_chi_velocity_Hessian", S.diff(after_shift, zd, 2)-Kchi)
    Dchi = a**3*(Sigma*W*W/(4*Theta**2)+C*W/(2*Theta)+D/2)-a*k*k*Sclock/2
    Jchi = a**3*M*(Sigma*W/Theta**2+C/Theta)/2
    zero("remaining_clock_constraint_Hessian", S.diff(after_shift, sig, 2)-Dchi)
    zero("remaining_clock_velocity_mixing", S.diff(after_shift, sig, zd)-Jchi)
    zero("clock_constraint_k_squared_coefficient", S.diff(Dchi, k, 2)/2+a*Sclock/2)

    # Read prior evidence as mathematical data only. Its declared coefficient
    # strings are compared, never executed as commands or imported as code.
    archive = Path(__file__).resolve().parents[3]/"cubic_finite_wavelength/run_001/derivation.json"
    prior = json.loads(archive.read_text())
    Acur, U, B0 = S.symbols("A U B0", real=True)
    canonical_PX = Acur/(2*q)+3*gamma*q*H
    canonical_PXX = (B0-Acur/q)/(4*q*q)
    canonical_Hd = -(Acur*q+U)/(2*M)
    canonical_PXt = (-3*H*Acur/(2*q)+3*gamma*(qd*H+q*canonical_Hd)
                     -B0*qd/(2*q))
    canonical_W = U-2*gamma*q*q*qd
    bg = {PX: canonical_PX, PXX: canonical_PXX, W: canonical_W,
          WY: Acur*U/(2*q*(Acur*q+U)),
          Ft: 3*H*canonical_W, PXt: canonical_PXt,
          Ftt: 3*canonical_Hd*canonical_W+3*H*Wt-2*q*qd*canonical_PXt}
    local_symbols = {str(x):x for x in (a,H,q,M,gamma,k,Acur,U,B0,qd,PX,PXX)}
    old_D = S.sympify(prior["zeta_constraint_coefficient"], locals=local_symbols)
    old_J = S.sympify(prior["mixing_velocity"], locals=local_symbols)
    old_K = S.sympify(prior["reduced_velocity_matrix"], locals={**local_symbols,"Matrix":S.Matrix})
    zero("archived_full_finite_k_clock_constraint_gauge_match", Dchi.subs(bg)/H**2-old_D)
    zero("archived_clock_velocity_mixing_gauge_match", Jchi.subs(bg)/q-old_J)
    zero("archived_unitary_tau_kinetic_matrix_gauge_match", Kchi-old_K[0,0])
    old_D2 = S.sympify(prior["constraint_k_squared_coefficient"], locals=local_symbols)
    zero("archived_spatial_clock_constraint_gauge_match", -a*Sclock.subs(bg)/(2*H**2)-old_D2)

    # Tiny exact controls of normalization, not selected physical backgrounds.
    canonical_control = {gamma:0, PX:S.Rational(1,2), PXX:0, M:1, H:1, q:1, a:1}
    zero("canonical_scalar_unitary_kinetic_fixture", Kchi.subs(canonical_control)-S.Rational(1,2))
    zero("clock_gradient_sign_fixture", (-Sclock/2).subs({W:3,WY:1,q:1})+S.Rational(1,2))
    return {
        "base_revision": "196f84653fec06a359314ec705d69647c5bd05a4",
        "scope": "Full quadratic unitary-chi scalar ADM action and exact gauge checks against existing source-free finite-k evidence; no sourced transfer or nonlinear PDE",
        "software": {"python":platform.python_version(),"sympy":S.__version__},
        "conventions": {"metric":"N=1+n; h_ij=a^2 exp(2zeta)delta_ij; N^x=partial_x B", "fields":"chi=chibar(t); tau=t+sigma; q=chidotbar", "F":"P(q^2,t)-V(t)-M2*Lambda when Lambda is present", "averaging":"real cosine products have period average 1/2", "Bxx":"shift divergence, not the sine shift amplitude"},
        "raw_sector_quadratic_divided_by_a3": {key:str(value) for key,value in jets.items()},
        "quadratic_after_IBP_divided_by_a3":str(compact),
        "tadpole_remainders_divided_by_a3":str(tadpoles),
        "coefficients":{"Theta":str(Theta),"Sigma":str(Sigma),"C":str(C),"D":str(D),"Sclock":str(Sclock),"Bhat":str(Bhat)},
        "lapse_from_shift":str(nsol),"zeta_velocity_Hessian_averaged":str(Kchi),
        "remaining_clock_Hessian_averaged":str(Dchi),
        "remaining_clock_velocity_mixing_averaged":str(Jchi),
        "gauge_map":"zeta_tau=zeta_chi-H*sigma_chi; delta_chi_tau=-q*sigma_chi; u=delta_chi_tau-(q/H)zeta_tau=-(q/H)zeta_chi",
        "checks":checks,"checks_passed":len(checks),
        "non_claims":["No new fixed functions or reconstructed histories","No ordinary-matter source or transfer calculation","No new nonlinear constraint or stability theorem","No division allowed at q=0, Theta=0, or H=0 in the corresponding gauge comparison","No removal of tadpoles unless the actual background equations hold"]
    }


if __name__ == "__main__":
    print(json.dumps(derive(), indent=2))
