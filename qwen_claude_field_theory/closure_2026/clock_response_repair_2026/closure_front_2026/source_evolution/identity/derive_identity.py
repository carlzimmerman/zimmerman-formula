#!/usr/bin/env python3
"""Exact ADM source/slip identities; no background or perturbation integration.

M denotes the constant Einstein coefficient M2, and L=2<L_density>/a^3.
The covariant action-to-quadratic reduction is an explicitly external input;
this script independently differentiates that quadratic action. All checks
are rational-function identities, not finite numerical samples.
"""
import json
import platform

import sympy as s


def derive():
    M, r = s.symbols("M2 r", nonzero=True, real=True)
    H = s.symbols("H", real=True)
    Th, Sig, W, D, E, C = s.symbols("Theta Sigma W D E C", real=True)
    z, v, n, ell, sig, rho = s.symbols("zeta zetadot n LapB sigma rho", real=True)
    vd, nd, eld, sigd, Thd, Wd = s.symbols(
        "zetaddot ndot LapBdot sigmadot Thetadot Wdot", real=True)
    variables = (z, v, n, ell, sig, Th, W, r)
    velocities = (v, vd, nd, eld, sigd, Thd, Wd, -2*H*r)

    def dt(expr):
        return sum(s.diff(expr, x)*dx for x, dx in zip(variables, velocities))

    checks = {}

    def zero(name, expression):
        residual = s.factor(s.cancel(s.expand(expression)))
        checks[name] = residual == 0
        if residual != 0:
            raise AssertionError((name, str(residual)))

    # Exactly the on-background-shell quadratic action in finite_wavelength/.
    L = (-3*M*v*v+6*Th*n*v+Sig*n*n+2*(M*v-Th*n)*ell
         +M*r*z*z+2*M*r*n*z+D*n*sig-3*W*sig*v+W*sig*ell
         +(E-C*r)*sig*sig/2-rho*n)
    shift_row = s.diff(L, ell)
    lapse_row = s.diff(L, n)
    clock_row = s.diff(L, sig)
    mom = s.diff(L, v)
    zeta_row = dt(mom)+3*H*mom-s.diff(L, z)
    u = -ell/r
    phi = n+dt(u)
    psi = -z-H*u
    slip = s.factor(phi-psi)
    zero("momentum_shift_row_identity", mom-2*M*ell+3*shift_row)
    zero("curvature_gradient_row", s.diff(L, z)-2*M*r*(z+n))
    zero("shift_time_derivative", dt(u)+eld/r+2*H*ell/r)
    zero("off_shell_slip_identity", 2*M*r*slip+zeta_row
         +3*(dt(shift_row)+3*H*shift_row))

    # On the shift row and its derivative, the curvature row sets this elldot.
    eld_on = r*(z+n)-3*H*ell
    zero("no_slip_on_variational_rows", slip.subs(eld, eld_on))
    T, Td, u0, ud = s.symbols("T Tdot u udot", real=True)
    zero("Phi_time_gauge_invariance", (n-Td)+(ud+Td)-(n+ud))
    zero("Psi_time_gauge_invariance", -(z-H*T)-H*(u0+T)-(-z-H*u0))
    zero("dust_source_has_no_shift_row", s.diff(-rho*n, ell))
    zero("dust_source_has_no_curvature_row", s.diff(-rho*n, z))

    # Derive elimination directly, without importing probe.py or its formulas.
    nsol = s.solve(shift_row, n)[0]
    after_shift = s.expand(L.subs(n, nsol))
    sigsol = s.solve(s.diff(after_shift, sig), sig)[0]
    Leff = s.factor(after_shift.subs(sig, sigsol))
    ellsol = s.solve(lapse_row, ell)[0].subs(n, nsol)
    fully_on = {n:nsol.subs(sig, sigsol), sig:sigsol,
                ell:ellsol.subs(sig, sigsol)}
    zero("all_three_auxiliary_rows_shift", shift_row.subs(fully_on, simultaneous=True))
    zero("all_three_auxiliary_rows_lapse", lapse_row.subs(fully_on, simultaneous=True))
    zero("all_three_auxiliary_rows_clock", clock_row.subs(fully_on, simultaneous=True))
    P = s.factor(s.diff(Leff, v))  # P=p/a^3.
    zero("Schur_envelope_momentum", P-2*M*fully_on[ell])
    zero("Schur_envelope_curvature_row", s.diff(Leff, z)-2*M*r*(z+fully_on[n]))

    den = C*r-E-D*W/Th-Sig*W*W/(2*Th*Th)
    J = M*(Sig*W+D*Th)/(Th*Th)
    f = rho*W/(2*Th)
    F = -rho*M/Th-J*f/den
    initial = {z:0, v:0}
    sigma0 = -f/den
    n0 = -rho*W*W/(4*Th*Th*den)
    ell0 = F/(2*M)
    zero("initial_clock", sigsol.subs(initial)-sigma0)
    zero("initial_lapse", fully_on[n].subs(initial)-n0)
    zero("initial_momentum_is_F", P.subs(initial)-F)
    zero("initial_shift", fully_on[ell].subs(initial)-ell0)
    zero("initial_Psi", psi.subs({z:0, ell:ell0})-H*F/(2*M*r))
    zero("initial_Phi_independent_reconstruction", phi.subs(eld, eld_on)
         .subs({z:0, n:n0, ell:ell0}, simultaneous=True)-H*F/(2*M*r))

    # The only source evolution hypothesis, checked without perturbation EOM.
    t = s.symbols("t", real=True)
    a = s.Function("a")(t)
    charge = s.symbols("rho_star", real=True)
    source = charge/a**3
    zero("signed_dust_background_conservation", s.diff(source,t)+3*s.diff(a,t)*source/a)

    # Keep discarded background residuals visible to delimit the theorem.
    E0, Et, Ea = s.symbols("E0 Et Ea", real=True)
    tadpoles = 3*E0*n*z+3*Et*z*sig+s.Rational(9,2)*Ea*z*z
    full_zeta_row = zeta_row-s.diff(tadpoles,z)
    zero("off_background_shell_remainder", 2*M*r*slip+full_zeta_row
         +3*(dt(shift_row)+3*H*shift_row)+s.diff(tadpoles,z))
    return {
        "base_revision":"486edc78eaed87647c0b605cdbebccb996a464cf",
        "scope":"Exact finite-mode action identity and constrained source initial data",
        "software":{"python":platform.python_version(),"sympy":s.__version__},
        "domain":"Real rational functions; a>0, constant M2 nonzero, k nonzero; elimination additionally Theta, Dcal nonzero",
        "raw_L":str(L), "shift_row":str(shift_row), "lapse_row":str(lapse_row),
        "clock_row":str(clock_row), "momentum_density":str(mom),
        "zeta_row":str(zeta_row), "Phi":str(phi), "Psi":str(psi),
        "slip":str(slip),
        "off_shell_identity":"2*M2*r*(Phi-Psi)+E_zeta+3*(dot(E_shift)+3*H*E_shift)=0",
        "canonical_on_shell":["p=2*M2*a^3*LapB", "pdot=2*M2*a^3*r*(zeta+n)",
                              "u=-p/(2*M2*a*k^2)",
                              "Phi=n-pdot/(2*M2*a*k^2)+H*p/(2*M2*a*k^2)",
                              "Psi=-zeta+H*p/(2*M2*a*k^2)"],
        "initial_data":{"sigma":str(sigma0),"n":str(n0),"p_over_a3":str(F),
                        "LapB":str(ell0),"Phi_equals_Psi":str(H*F/(2*M*r))},
        "background_remainder":str(s.diff(tadpoles,z)),
        "checks":checks,"checks_passed":len(checks),
        "non_claims":["No derivation of the input quadratic action from the full covariant action in this script",
                      "No homogeneous k=0 claim, nonlinear anisotropic-stress theorem, or PPN inference",
                      "No positive-density galaxy from the signed zero-background-density probe",
                      "No claim that nonconserved forcing is physically admissible, although its lapse-only algebra has the same identity",
                      "No numerical integration, accuracy estimate, force fit, or singular-constraint continuation"]
    }


if __name__ == "__main__":
    print(json.dumps(derive(), indent=2))
