#!/usr/bin/env python3
"""Forced finite-mode constraint reduction; not a galaxy or CMB simulation.

Uses the independently derived on-shell unitary-chi ADM quadratic action.
All coefficients remain arbitrary background functions at this algebra step.
L is twice the period average, divided by a^3; this common normalization also
applies to the source. Derivatives below do not freeze coefficients in time.
"""
import json
import sympy as s


def derive():
    M, A, r = s.symbols('M2 Theta physical_k_squared', positive=True)
    W, Sigma, D, E, C = s.symbols('W Sigma D E C', real=True)
    z, v, n, shift, sigma, rho = s.symbols('zeta zetadot n LapB sigma rho', real=True)
    # S_source=-int m ds. For a comoving test worldline, ds=N dt to
    # the required source*metric order. Hence -a^3 rho n; no scalar source.
    source = -rho*n
    L = (-3*M*v*v+6*A*n*v+Sigma*n*n+2*(M*v-A*n)*shift
         +M*r*z*z+2*M*r*n*z+D*n*sigma-3*W*sigma*v
         +W*sigma*shift+(E-C*r)*sigma*sigma/2+source)
    checks = {}
    def zero(name, expression):
        residual = s.factor(expression)
        checks[name] = residual == 0
        if residual != 0:
            raise AssertionError((name, residual))
    nsol = s.solve(s.diff(L, shift), n)[0]
    reduced = s.expand(L.subs(n, nsol))
    sigsol = s.solve(s.diff(reduced, sigma), sigma)[0]
    Leff = s.factor(reduced.subs(sigma, sigsol))
    # Differentiate the true reduced density instead of assigning dynamics.
    Ak = s.factor(s.diff(Leff, v, 2))
    Bk = s.factor(s.diff(Leff, v, z))
    Ck = s.factor(s.diff(Leff, z, 2))
    Fk = s.factor(s.diff(Leff, v).subs({v:0,z:0}))
    Sk = s.factor(s.diff(Leff, z).subs({v:0,z:0}))
    clock_den = s.factor(-s.diff(reduced, sigma, 2))
    shift_sol = s.solve(s.diff(L,n),shift)[0].subs(n,nsol)
    zero('shift_Euler', s.diff(L,shift).subs(n,nsol))
    zero('clock_Euler', s.diff(reduced,sigma).subs(sigma,sigsol))
    zero('lapse_Euler', s.diff(L,n).subs({n:nsol,shift:shift_sol},simultaneous=True))
    zero('source_metric_variation', s.diff(source,n)+rho)
    zero('no_direct_clock_source', s.diff(source,sigma))
    zero('zero_source_F', Fk.subs(rho,0))
    zero('zero_source_S', Sk.subs(rho,0))
    K = 6*M+2*Sigma*M*M/(A*A)
    mix = M*(Sigma*W+D*A)/(A*A)
    R = M*W/A
    forcing = rho*W/(2*A)
    den = C*r-E-D*W/A-Sigma*W*W/(2*A*A)
    zero('independent_clock_denominator', clock_den-den)
    zero('independent_shift_lapse', nsol-(M*v+W*sigma/2)/A)
    zero('independent_clock_response', sigsol-(mix*v+R*r*z-forcing)/den)
    zero('independent_kinetic_Schur', Ak-K-mix*mix/den)
    zero('independent_cross_Schur', Bk-2*M*M*r/A-mix*R*r/den)
    zero('independent_potential_Schur', Ck-2*M*r-R*R*r*r/den)
    zero('independent_momentum_source', Fk+rho*M/A+mix*forcing/den)
    zero('independent_force_source', Sk+R*r*forcing/den)
    # Exact source Ward control: on the background, a comoving dust probe has
    # rho_dot+3H rho=0 and zero spatial momentum. It has no homogeneous density.
    t = s.symbols('t',real=True)
    aa = s.Function('a')(t)
    charge = s.symbols('rho_star',real=True)
    rr = charge/aa**3
    zero('conserved_dust_density', s.diff(rr,t)+3*s.diff(aa,t)*rr/aa)
    # Gauge transformations independently establish the observable definitions.
    nd, H, u, ud, T, Td = s.symbols('n0 H shift_cov shift_cov_dot T Tdot',real=True)
    Phi, Psi = nd+ud, -z-H*u
    zero('Phi_gauge_invariance', (nd-Td)+(ud+Td)-Phi)
    zero('Psi_gauge_invariance', -(z-H*T)-H*(u+T)-Psi)
    return dict(
        scope='Exact forced quadratic finite-k reduction; no time integration or physical-force fit',
        assumptions=['homogeneous on-shell clock/scalar-only FLRW', 'unitary chi with q nonzero',
                     'k nonzero, Theta nonzero, clock denominator nonzero, effective kinetic coefficient nonzero',
                     'rho=rho_star/a^3 is a conserved zero-background-density signed test perturbation',
                     'ordinary matter backreaction on homogeneous expansion is not modeled'],
        normalization='L is twice the spatial period average divided by a^3',
        raw_L=str(L), lapse=str(nsol), clock=str(sigsol), shift_laplacian=str(shift_sol),
        clock_denominator=str(clock_den),
        coefficients={key:str(val) for key,val in dict(A=Ak,B=Bk,C=Ck,F=Fk,S=Sk).items()},
        canonical_equations=['p=a^3*(A*zetadot+B*zeta+F)',
                             'zetadot=(p/a^3-B*zeta-F)/A',
                             'pdot=a^3*(B*zetadot+C*zeta+S)'],
        physical_potentials=['u=a^2 Bshift=-LapB/physical_k_squared',
                             'Phi=n+dot(u)', 'Psi=-zeta-H*u'],
        checks=checks,
        non_claims=['No assigned Phi=Psi or PPN value', 'No numerical response or CMB/galaxy prediction',
                    'No positive-density isolated galaxy from the signed probe',
                    'No nonlinear degree count or singular-denominator continuation']), dict(
        rho=rho, F=Fk, S=Sk, source_lapse_derivative=s.diff(source,n))


if __name__ == '__main__':
    print(json.dumps(derive()[0],indent=2))
