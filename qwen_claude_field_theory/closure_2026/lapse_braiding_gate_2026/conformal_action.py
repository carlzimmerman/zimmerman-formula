"""Raw ADM derivations for lapse-dependent metric transformations.

Physical matter is minimal to g, not inherited from the seed metric. The
explicit family is g_tilde=N^(2 eta) g with Einstein-Hilbert seed action and
an additional physical-frame f((D ln N)^2). This file constructs actions;
it supplies no constraint ranks or inherited degree-of-freedom counts.

Static local background: N_bar=1, h_bar=delta, K_bar=0, acceleration A along
x^2, perturbation wavevector k along x^1. Coefficients are frozen at the
evaluation point. Amplitude expansion precedes the principal projection:
degree(k)=degree(zd)=degree(nd)=1, while frozen A has degree zero. Retain
total perturbation derivative degree two. This is a local symbol calculation,
not a solved global background or a nonlinear constraint certificate.
"""

from functools import lru_cache

import sympy as s


def _ricci_scalar(metric, coordinates):
    """Contract actual Christoffels/Ricci from a supplied spatial metric."""
    inverse = metric.inv()
    dimension = len(coordinates)
    gamma = [[[
        s.simplify(sum(inverse[i, ell]*(s.diff(metric[ell, q], coordinates[j])
                       + s.diff(metric[ell, j], coordinates[q])
                       - s.diff(metric[j, q], coordinates[ell]))
                        for ell in range(dimension))/2)
        for q in range(dimension)] for j in range(dimension)]
        for i in range(dimension)]
    ricci = s.Matrix(dimension, dimension, lambda i, j: sum(
        s.diff(gamma[ell][i][j], coordinates[ell])
        - s.diff(gamma[ell][i][ell], coordinates[j])
        + sum(gamma[ell][i][j]*gamma[q][ell][q]
              - gamma[q][i][ell]*gamma[ell][j][q]
              for q in range(dimension))
        for ell in range(dimension)))
    scalar = s.simplify(sum(inverse[i, j]*ricci[i, j]
                            for i in range(dimension) for j in range(dimension)))
    return scalar, gamma, ricci


@lru_cache(None)
def _conformal_geometry():
    x, y, w = s.symbols("x y w", real=True)
    omega = s.Function("omega")(x, y)
    scalar, gamma, ricci = _ricci_scalar(s.eye(3)*s.exp(2*omega), (x, y, w))
    return x, y, omega, scalar, gamma, ricci


def _quadratic_average(expression, epsilon, theta):
    """Twice the real cosine/sine average of the amplitude-quadratic term."""
    quadratic = s.diff(expression, epsilon, 2).subs(epsilon, 0)/2
    quadratic = s.expand_trig(s.expand(quadratic))
    return s.expand(2*quadratic.subs({s.cos(theta)**2: s.Rational(1, 2),
                                    s.sin(theta)**2: s.Rational(1, 2)}))


@lru_cache(None)
def derive():
    m, k = s.symbols("m k", positive=True)
    alpha, eta, z, zd, n, nd, v = s.symbols("alpha eta z zd n nd v", real=True)
    A, a0 = s.symbols("A a0", positive=True)
    epsilon, theta = s.symbols("epsilon theta", real=True)
    cosine, sine = s.cos(theta), s.sin(theta)
    dx = lambda expr: k*s.diff(expr, theta)
    zeta = epsilon*z*cosine
    lapse = 1+epsilon*n*cosine
    shift = epsilon*v*sine
    lapse_dot = epsilon*nd*cosine
    physical_hfactor = s.exp(2*zeta)
    physical_volume = s.exp(3*zeta)
    transformed_hfactor = lapse**(2*eta)*physical_hfactor
    transformed_lapse = lapse**(1+eta)
    transformed_volume = lapse**(3*eta)*physical_volume
    transformed_hdot = 2*(epsilon*zd*cosine+eta*lapse_dot/lapse)*transformed_hfactor
    kmixed = s.diag(*[
        (transformed_hdot-shift*dx(transformed_hfactor)
         -(2*transformed_hfactor*dx(shift) if i == 0 else 0))
        /(2*transformed_lapse*transformed_hfactor)
        for i in range(3)])
    # K_bar=0: the quadratic kinetic action is exactly its background
    # measure times contractions of the action-derived first variation K1.
    klinear = kmixed.diff(epsilon).subs(epsilon, 0)
    kinetic_quadratic = (s.trace(klinear*klinear)-s.trace(klinear)**2)/2
    kinetic_average = s.expand(2*kinetic_quadratic).subs(
        {cosine**2: s.Rational(1, 2), sine**2: s.Rational(1, 2)})

    x, y, omega, generic_R, _, _ = _conformal_geometry()
    local_omega = zeta+eta*s.log(lapse)
    # N_bar=exp(A y) locally. Its first y derivative contributes eta*A to
    # the transformed conformal factor. Perturbations are transverse to A.
    curvature = generic_R.subs({
        s.diff(omega, x, 2): dx(dx(local_omega)),
        s.diff(omega, y, 2): 0,
        s.diff(omega, x): dx(local_omega),
        s.diff(omega, y): eta*A,
        omega: local_omega,
    }, simultaneous=True)
    curvature_density = transformed_lapse*transformed_volume*curvature/2
    curvature_average = _quadratic_average(curvature_density, epsilon, theta)

    # The added f(s) belongs to the physical frame. Differentiate the
    # exponential f explicitly; its principal contribution is then named
    # alpha, so the canonical calculation can also examine other fs values.
    acceleration_squared = (A**2+(dx(lapse)/lapse)**2)/physical_hfactor
    argument = s.symbols("s_argument", positive=True)
    f = 2*a0**2*(1-(1+s.sqrt(argument)/a0)*s.exp(-s.sqrt(argument)/a0))
    f_derivatives = tuple(s.simplify(s.diff(f, argument, order).subs(argument, A**2))
                          for order in range(3))
    f0, fs, fss = s.symbols("f0 fs fss", real=True)
    delta_s = acceleration_squared-A**2
    f_taylor = f0+fs*delta_s+fss*delta_s**2/2
    f_average = _quadratic_average(lapse*physical_volume*f_taylor, epsilon, theta)
    full_average = s.expand(kinetic_average+curvature_average+f_average)
    polynomial = s.Poly(full_average, k, zd, nd)
    principal = s.expand(sum(coefficient*k**i*zd**j*nd**ell
                             for (i, j, ell), coefficient in polynomial.terms()
                             if i+j+ell == 2))
    L = s.expand(m*principal.subs(fs, alpha))
    target = m*(-3*(zd+eta*nd)**2+2*k*v*(zd+eta*nd)
                +k**2*(z**2+2*(1+2*eta)*n*z+(2*eta+3*eta**2+alpha)*n**2))
    conformal_identity = s.exp(-2*omega)*(
        -4*(s.diff(omega, x, 2)+s.diff(omega, y, 2))
        -2*(s.diff(omega, x)**2+s.diff(omega, y)**2))
    residuals = {
        "raw_ricci_identity": s.simplify(generic_R-conformal_identity),
        "raw_trace_first_variation": s.simplify(
            s.trace(klinear)-(3*(zd+eta*nd)-k*v)*cosine),
        "raw_kinetic_contraction": s.simplify(
            kinetic_average-(-3*(zd+eta*nd)**2+2*k*v*(zd+eta*nd))),
        "f_s_derivative": s.simplify(f_derivatives[1]-s.exp(-A/a0)),
        "action_structure": s.expand(L-target),
    }
    mass_b = s.Symbol("mass_b", positive=True)
    speed2 = s.Symbol("speed2", nonnegative=True)
    # The SAME model may contain both a canonical scalar and physical minimal
    # particles. The static diagnostic sets sigma constant and uses the
    # leading nonrelativistic particle source; homogeneous() sets particles
    # absent and counts canonical scalar matter separately.
    particle_L = -mass_b*s.sqrt((1+epsilon*n)**2-s.exp(2*epsilon*z)*epsilon*speed2)
    particle_linear = s.diff(particle_L, epsilon).subs({epsilon: 0, speed2: 0})
    particle_source = dict(mass=mass_b, L=particle_L,
                           linear_lapse_source=particle_linear,
                           linear_spatial_source=s.diff(particle_linear, z))
    residuals["minimal_particle_source"] = s.simplify(particle_linear+mass_b*n)
    return dict(m=m, k=k, alpha=alpha, eta=eta, z=z, zd=zd, n=n, nd=nd, v=v,
                L=L, residuals=residuals, A=A, a0=a0, kmixed=kmixed,
                klinear=klinear, curvature=curvature,
                acceleration_squared=acceleration_squared,
                raw_quadratic_average=full_average, f=f,
                f_derivatives=f_derivatives, alpha_exponential=f_derivatives[1],
                principal_degree="degree(k)=degree(zd)=degree(nd)=1; frozen A degree 0; keep total degree 2",
                particle_source=particle_source,
                matter_scope="S_m is minimal to physical g; no matter coupling or constraint count is inherited from the seed")


@lru_cache(None)
def derive_general_map():
    """General point map: tilde h=C(N)h, tilde N=D(N)N, same shift."""
    m, C, D, k = s.symbols("m C D k", positive=True)
    c, d, c1, d1, Phi, Psi = s.symbols("c d c1 d1 Phi Psi", real=True)
    epsilon, theta = s.symbols("epsilon theta", real=True)
    dx = lambda expr: k*s.diff(expr, theta)
    logN = epsilon*Phi*s.cos(theta)
    # These are general second-order jets of ln C(N), ln D(N). Keeping c1
    # and d1 verifies that second logarithmic derivatives cancel from L2.
    local_omega = -epsilon*Psi*s.cos(theta)+c*logN/2+c1*logN**2/4
    log_tildeN = (1+d)*logN+d1*logN**2/2
    x, y, omega, generic_R, _, _ = _conformal_geometry()
    R = generic_R.subs({s.diff(omega, x, 2): dx(dx(local_omega)),
                       s.diff(omega, y, 2): 0,
                       s.diff(omega, x): dx(local_omega),
                       s.diff(omega, y): 0,
                       omega: local_omega}, simultaneous=True)/C
    raw_density = m*D*C**s.Rational(3, 2)*s.exp(log_tildeN+3*local_omega)*R/2
    L_static = _quadratic_average(raw_density, epsilon, theta)
    W = D*s.sqrt(C)
    cross_coefficient = s.factor(-s.diff(L_static, Phi, Psi)/(2*m*W*k**2))
    lapse_coefficient = s.factor(s.diff(L_static, Phi, 2)/(2*m*W*k**2))
    potential_solution = s.solve(s.diff(L_static, Psi), Psi)[0]
    slip_coefficient = s.factor(potential_solution/Phi)
    newton_factor = s.factor(cross_coefficient**2-lapse_coefficient)

    # Tensor coefficients from actual tracefree extrinsic curvature and the
    # Ricci scalar of diag(C,C exp(gamma),C exp(-gamma)). The time is the
    # physical proper time, so the transformed background lapse is D.
    gd = s.symbols("gamma_dot", real=True)
    gamma_wave = s.Function("gamma")(x)
    ktensor = s.diag(0, gd/(2*D), -gd/(2*D))
    tensor_kinetic_raw = m*D*C**s.Rational(3, 2)*(s.trace(ktensor**2)-s.trace(ktensor)**2)/2
    tensor_R, _, _ = _ricci_scalar(
        s.diag(C, C*s.exp(gamma_wave), C*s.exp(-gamma_wave)),
        (x, y, s.symbols("w", real=True)))
    tensor_gradient_raw = m*D*C**s.Rational(3, 2)*tensor_R/2
    tensor_kinetic = s.simplify(2*s.diff(tensor_kinetic_raw, gd, 2))
    tensor_gradient = s.simplify(-2*s.diff(tensor_gradient_raw, s.diff(gamma_wave, x), 2))
    tensor_speed2 = s.factor(tensor_gradient/tensor_kinetic)
    # General integrated conformal-Ricci coefficient. Grad ln F=(1+d+c/2)a
    # for F=N D sqrt(C); Grad ln C=c a.
    Q_integrated = s.expand((1+d+c/2)*c-c**2/4)
    residuals = {
        "raw_static_cross": s.simplify(cross_coefficient-(1+d+c/2)),
        "raw_static_lapse": s.simplify(lapse_coefficient-Q_integrated),
        "physical_potential_relation": s.simplify(slip_coefficient-cross_coefficient),
        "newton_normalization": s.simplify(newton_factor-(1+d)**2),
        "tensor_light_cone": s.simplify(tensor_speed2-D**2/C),
    }
    return dict(m=m, C=C, D=D, c=c, d=d, W=W, Phi=Phi, Psi=Psi, k=k,
                L_static=L_static, Q=lapse_coefficient, t=cross_coefficient,
                slip_coefficient=slip_coefficient, potential_solution=potential_solution,
                newton_factor=newton_factor,
                G_effective=1/(8*s.pi*m*W*newton_factor),
                tensor_kinetic=tensor_kinetic, tensor_gradient=tensor_gradient,
                tensor_speed2=tensor_speed2,
                tensor_kinetic_raw=tensor_kinetic_raw, tensor_gradient_raw=tensor_gradient_raw,
                residuals=residuals, invertibility_factor=1+d,
                coefficient_scope="c=d ln C/d ln N and d=d ln D/d ln N; all values evaluated at the physical background lapse",
                source_scope="The physical static source is -rho Phi; G_effective is derived after eliminating Psi, not inherited from the seed",
                constitutive_scope="The exact static point-map density is M^2 N sqrt(h) W(N)[R/2+Q(N)s]; Q depends on lapse, not acceleration magnitude")


@lru_cache(None)
def derive_gradient_map():
    """Track operators generated if C and D instead depend on s=a_i a^i."""
    cs, ds = s.symbols("c_s d_s", real=True)
    acc_dot_grad_s, grad_s_squared = s.symbols("a_dot_grad_s grad_s_squared", real=True)
    # Exact spatial integration by parts of -F Delta ln C, F=N D sqrt(C):
    # Grad ln F=a+(ds+cs/2)Grad s, Grad ln C=cs Grad s.
    integrated = s.expand(cs*acc_dot_grad_s
                          +(ds+cs/2)*cs*grad_s_squared-cs**2*grad_s_squared/4)
    squared_coefficient = s.diff(integrated, grad_s_squared)
    luminal = s.factor(squared_coefficient.subs(ds, cs/2))
    a_dot_k, k_squared, n = s.symbols("a_dot_k k_squared n", real=True)
    # For a lapse perturbation on finite background acceleration,
    # delta s=2 a^i partial_i n. Hence |Grad delta s|^2 has this k^4 symbol.
    fourth_order = s.expand(luminal*4*a_dot_k**2*k_squared*n**2)
    residuals = {"integration_by_parts": s.simplify(
        integrated-(cs*acc_dot_grad_s+(cs*ds+cs**2/4)*grad_s_squared))}
    return dict(cs=cs, ds=ds, integrated_operator=integrated,
                gradient_squared_coefficient=squared_coefficient,
                luminal_gradient_squared_coefficient=luminal,
                a_dot_k=a_dot_k, k_squared=k_squared, n=n,
                fourier_fourth_order_term=fourth_order, residuals=residuals,
                scope="Grad_i s=2a^j D_iD_j ln N; these higher spatial derivatives are retained. Their presence alone does not count time-propagating modes.")


if __name__ == "__main__":
    print("SymPy:", s.__version__)
    for name, function in (("explicit conformal action", derive),
                           ("general point map", derive_general_map),
                           ("gradient-dependent map", derive_gradient_map)):
        result = function()
        print(name)
        for key in ("L", "Q", "slip_coefficient", "G_effective", "tensor_speed2",
                    "luminal_gradient_squared_coefficient", "fourier_fourth_order_term"):
            if key in result:
                print(key+":", s.factor(result[key]))
        for key, residual in result["residuals"].items():
            print(key+":", residual)
            assert residual == 0, (name, key, residual)
