#!/usr/bin/env python3
"""Action-derived ADM falsifier for the intrinsic-elliptic DW rescue.

The committed localized Deffayet--Woodard representative has an unrestricted
``(X, xi)`` wave pair with opposite kinetic signs.  The strongest small repair
is to make that localizer genuinely spatial while retaining the curvature
coupling needed to affect the metric:

    S_eDW = int sqrt(-g) [
        (R-a0^2 M)/kappa
        + xi (Delta_u X - R_mn nhat^m nhat^n)
        + lambda (v^2+1)
        - Q nhat^m nabla_m nu + L_m
    ],

    Q = M + f(Z_s),  Z_s = 4 D_i X D^i X/a0^2.

The off-shell prescription is fixed as
``v_mu=nabla_mu phi``, ``nhat_mu=-v_mu/sqrt(-v^2)``, and
``h_mn=g_mn+nhat_m nhat_n``; ``D`` is the intrinsic derivative of these
hypersurface-orthogonal slices and ``Delta_u=D_i D^i``.  The lambda equation
then fixes the clock normalization on shell.  A spatial integration by parts
with the ``N sqrt(h)`` measure also produces a lapse-acceleration term; the
code therefore keeps the xi equation in its unintegrated intrinsic form.
Ordinary matter is minimally coupled to the same metric.

The frozen-coefficient principal finite-k density is derived from the ADM
Einstein-Hilbert scalar block, the linearized Ricci tensor, and the varied
elliptic terms on a xi_bar=0 background.  Within that unitary-gauge principal
block its Legendre map, Hamiltonian, primary/secondary preservation chain,
actual Poisson matrix, constraint classes, reduced characteristic, k=0
metric-clock subchain, and mutation controls are computed.  No desired rank,
determinant, mode count, or speed is fed into the calculation.

Scope: one scalar Fourier mode transverse to a constant static background
gradient, on the regular conserved Q=0 branch.  This direction removes f''
anisotropy, but it does not remove the metric contribution
``delta Z_s=-8 y^2 zeta``; that term is retained in the transport constraint.
The finite-k clock calculation is explicitly unitary-gauge, while the exact
homogeneous xi equation is covariant within the frozen off-shell definition.
The result falsifies this candidate, not every formal nonlocal action.
"""

from __future__ import annotations

import functools
import itertools
import sys
from typing import Any

import sympy as sp


def _pb(
    left: sp.Expr,
    right: sp.Expr,
    coordinates: list[sp.Symbol],
    momenta: list[sp.Symbol],
) -> sp.Expr:
    """Canonical Poisson bracket, calculated rather than table-looked-up."""

    return sp.factor(
        sum(
            sp.diff(left, q) * sp.diff(right, p)
            - sp.diff(left, p) * sp.diff(right, q)
            for q, p in zip(coordinates, momenta)
        )
    )


def _first_nonzero_principal_minor(
    matrix: sp.Matrix, rank: int
) -> tuple[tuple[int, ...], sp.Expr]:
    """Find a rank-size principal minor without assuming where it lives."""

    for indices in itertools.combinations(range(matrix.rows), rank):
        determinant = sp.factor(matrix.extract(indices, indices).det())
        if determinant != 0:
            return indices, determinant
    return tuple(), sp.Integer(0)


def derive_exact_kernel() -> dict[str, Any]:
    """Differentiate the DW kernel that gives the exact exponential law."""

    Z = sp.Symbol("Z_s", positive=True)
    y = sp.Symbol("y", positive=True)
    # The integration constant fixes f(0)=0 and is dynamically irrelevant.
    f = 4 - 2 * (sp.sqrt(Z) + 2) * sp.exp(-sp.sqrt(Z) / 2)
    f_Z_general = sp.simplify(sp.diff(f, Z))
    f_ZZ_general = sp.simplify(sp.diff(f, Z, 2))
    f_Z = sp.simplify(f_Z_general.subs(Z, 4 * y**2))
    mu_eff = sp.simplify(1 - 2 * f_Z)
    mu_target = 1 - sp.exp(-y)
    lambda_perp = mu_eff
    lambda_parallel = sp.factor(mu_eff + y * sp.diff(mu_eff, y))

    return {
        "symbols": {"Z": Z, "y": y},
        "f": f,
        "f_Z_general": f_Z_general,
        "f_ZZ_general": f_ZZ_general,
        "f_ZZ_zero_limit": sp.limit(f_ZZ_general, Z, 0, dir="+"),
        "f_Z": f_Z,
        "mu_eff": mu_eff,
        "mu_target": mu_target,
        "mu_residual": sp.simplify(mu_eff - mu_target),
        "lambda_perp": lambda_perp,
        "lambda_parallel": lambda_parallel,
        "ellipticity_origin": (
            sp.limit(lambda_perp, y, 0, dir="+"),
            sp.limit(lambda_parallel, y, 0, dir="+"),
        ),
        "deep_limit": sp.limit(mu_eff, y, 0, dir="+"),
        "deep_slope": sp.limit(mu_eff / y, y, 0, dir="+"),
        "newtonian_limit": sp.limit(mu_eff, y, sp.oo),
    }


def derive_static_mond_law() -> dict[str, Any]:
    """Vary the Q=0 static action and derive MOND and the BTFR."""

    A = sp.Symbol("A", positive=True)
    a0 = sp.Symbol("a0", positive=True)
    G = sp.Symbol("G", positive=True)
    M = sp.Symbol("M_b", positive=True)
    r = sp.Symbol("r", positive=True)
    p = sp.Symbol("p", positive=True)  # |grad Phi| on a monotonic branch
    y = sp.simplify(p / a0)
    Z = 4 * p**2 / a0**2
    f = 4 - 2 * (sp.sqrt(Z) + 2) * sp.exp(-sp.sqrt(Z) / 2)

    # EH plus M=-f on Q=0.  With A=1/(16 pi G), variation of
    # L_grad-rho Phi gives div(mu grad Phi)=4 pi G rho.
    gradient_density = sp.simplify(-2 * A * p**2 + A * a0**2 * f)
    flux = sp.simplify(sp.diff(gradient_density, p))
    mu_from_flux = sp.simplify(-flux / (4 * A * p))
    poisson_source_coefficient = sp.simplify(1 / (4 * A))

    gN = G * M / r**2
    deep_mond_g_squared = sp.simplify(a0 * gN)
    circular_speed_fourth = sp.simplify(r**2 * deep_mond_g_squared)

    return {
        "symbols": {
            "A": A,
            "a0": a0,
            "G": G,
            "M": M,
            "r": r,
            "p": p,
            "y": y,
        },
        "gradient_density": gradient_density,
        "flux": flux,
        "mu_from_flux": mu_from_flux,
        "poisson_source_coefficient": poisson_source_coefficient,
        "field_equation": "div[(1-exp(-|grad Phi|/a0)) grad Phi]=rho/(4A)",
        "spherical_equation": "mu(g/a0) g = G M_b/r^2",
        "deep_mond_g_squared": deep_mond_g_squared,
        "btfr": circular_speed_fourth,
    }


@functools.lru_cache(maxsize=1)
def _derive_spatial_curvature_fourier_density() -> sp.Expr:
    """Expand N sqrt(h) R^(3) directly for a real scalar Fourier mode.

    A cosine mode has average cos^2=1/2.  Multiplication by two converts the
    real-mode average to the usual q(-k)q(k) Fourier normalization used by the
    rest of the one-mode action.
    """

    x = sp.Symbol("x", real=True)
    eps = sp.Symbol("epsilon", real=True)
    k = sp.Symbol("k_spatial", positive=True)
    z, E, n = sp.symbols("z_spatial E_spatial n_spatial", real=True)
    cosine = sp.cos(k * x)
    metric = sp.diag(
        1 + 2 * eps * (z - k**2 * E) * cosine,
        1 + 2 * eps * z * cosine,
        1 + 2 * eps * z * cosine,
    )
    inverse = sp.simplify(metric.inv())
    coordinates = (x, sp.Symbol("y_spatial"), sp.Symbol("z_coord"))

    christoffel = [
        [
            [
                sp.simplify(
                    sp.Rational(1, 2)
                    * sum(
                        inverse[rho, sigma]
                        * (
                            sp.diff(metric[sigma, nu], coordinates[mu])
                            + sp.diff(metric[sigma, mu], coordinates[nu])
                            - sp.diff(metric[mu, nu], coordinates[sigma])
                        )
                        for sigma in range(3)
                    )
                )
                for nu in range(3)
            ]
            for mu in range(3)
        ]
        for rho in range(3)
    ]
    ricci = sp.zeros(3)
    for mu in range(3):
        for nu in range(3):
            ricci[mu, nu] = sp.simplify(
                sum(
                    sp.diff(christoffel[rho][mu][nu], coordinates[rho])
                    - sp.diff(christoffel[rho][mu][rho], coordinates[nu])
                    + sum(
                        christoffel[rho][rho][sigma]
                        * christoffel[sigma][mu][nu]
                        - christoffel[rho][nu][sigma]
                        * christoffel[sigma][mu][rho]
                        for sigma in range(3)
                    )
                    for rho in range(3)
                )
            )
    scalar_curvature = sp.simplify(
        sum(inverse[mu, nu] * ricci[mu, nu] for mu in range(3) for nu in range(3))
    )
    lapse = 1 + eps * n * cosine
    density = sp.simplify(lapse * sp.sqrt(metric.det()) * scalar_curvature)
    quadratic = sp.simplify(sp.diff(density, eps, 2).subs(eps, 0) / 2)
    averaged = sp.simplify(
        k / (2 * sp.pi) * sp.integrate(quadratic, (x, 0, 2 * sp.pi / k))
    )
    return sp.factor(2 * averaged)


@functools.lru_cache(maxsize=1)
def derive_quadratic_action() -> dict[str, Any]:
    """Build the xi_bar=0 frozen-coefficient principal scalar density."""

    A = sp.Symbol("A", positive=True)
    k = sp.Symbol("k", positive=True)
    beta = sp.Symbol("beta", positive=True)
    lambda_bar = sp.Symbol("lambda_bar", real=True)
    y_background = sp.Symbol("y_background", positive=True)
    z, E, xi, X, n, B, ell = sp.symbols(
        "zeta E sigma x n B delta_lambda", real=True
    )
    zd, Ed, xid = sp.symbols("zeta_dot E_dot sigma_dot", real=True)
    zdd, Edd, Bd = sp.symbols("zeta_ddot E_ddot B_dot", real=True)

    # K_ij for h_ij=delta_ij+2 zeta delta_ij+2 d_i d_j E and
    # N_i=d_i B, with the Fourier vector along the first coordinate.
    K11 = zd - k**2 * (Ed - B)
    K22 = zd
    K33 = zd
    trace_K = sp.simplify(K11 + K22 + K33)
    Kij_squared = sp.simplify(K11**2 + K22**2 + K33**2)
    eh_kinetic = sp.factor(A * (Kij_squared - trace_K**2))

    spatial_raw = _derive_spatial_curvature_fourier_density()
    spatial_symbols = {symbol.name: symbol for symbol in spatial_raw.free_symbols}
    eh_spatial = sp.factor(
        A
        * spatial_raw.subs(
            {
                spatial_symbols["k_spatial"]: k,
                spatial_symbols["z_spatial"]: z,
                spatial_symbols["n_spatial"]: n,
            }
        )
    )

    # Linearized R_00 from
    # R_00^(1)=1/2(2 d_alpha d_0 h^alpha_0-Box h_00-d_0^2 h).
    # The coordinate expression is B_xxt+n_xx-3 z_tt-E_xxtt.
    R_uu_linear = sp.factor(-k**2 * Bd - k**2 * n - 3 * zdd + k**2 * Edd)

    # Varying -xi R_uu first, then integrating the zdd, Edd and Bdot terms
    # by parts in time gives this density.  No equation-level source is pasted.
    curvature_coupling_after_parts = sp.factor(
        -3 * xid * zd + k**2 * xid * (Ed - B) + k**2 * n * xi
    )

    # The x-dependent gradient contribution to delta Z_s begins quadratically
    # for a transverse mode and gives beta k^2 x^2.  The metric contribution
    # is linear and is recorded below for Q transport.  Frozen-background
    # zeta^2/tadpole pieces from sqrt(h)f(Z_s) are lower principal order and
    # are outside this characteristic block.
    # beta=4(a0^2 A) f_Z/a0^2=4 A f_Z; its exact value is substituted later.
    elliptic_sector = -k**2 * xi * X + beta * k**2 * X**2
    # u_mu=partial_mu phi and lambda(u^2+1).  In unitary gauge phi=t,
    # expanding N sqrt(h) lambda(1-N^-2) to second order gives this term.
    # It cannot be omitted: delta_lambda varies to the lapse constraint n=0.
    unit_clock_sector = sp.expand(
        n
        * (
            2 * ell
            + 2 * lambda_bar * (3 * z - k**2 * E)
            - lambda_bar * n
        )
    )
    # Even for k perpendicular to grad(Xbar), the inverse spatial metric gives
    # a linear delta Z_s.  It enters the Q=0 transport constraint below.  It
    # has no derivatives and therefore does not alter this principal Hessian.
    delta_Z_metric = -8 * y_background**2 * z
    lagrangian = sp.expand(
        eh_kinetic
        + eh_spatial
        + curvature_coupling_after_parts
        + elliptic_sector
        + unit_clock_sector
    )

    return {
        "symbols": {
            "A": A,
            "k": k,
            "beta": beta,
            "lambda_bar": lambda_bar,
            "y_background": y_background,
            "z": z,
            "E": E,
            "xi": xi,
            "X": X,
            "n": n,
            "B": B,
            "ell": ell,
            "zd": zd,
            "Ed": Ed,
            "xid": xid,
            "zdd": zdd,
            "Edd": Edd,
            "Bd": Bd,
        },
        "K_components": (K11, K22, K33),
        "K_trace": trace_K,
        "Kij_squared": Kij_squared,
        "eh_kinetic": eh_kinetic,
        "spatial_curvature_density_from_metric": spatial_raw,
        "eh_spatial": eh_spatial,
        "R_uu_linear": R_uu_linear,
        "curvature_coupling_after_parts": curvature_coupling_after_parts,
        "elliptic_sector": elliptic_sector,
        "unit_clock_sector": unit_clock_sector,
        "delta_Z_metric": delta_Z_metric,
        "lagrangian": lagrangian,
    }


@functools.lru_cache(maxsize=1)
def derive_euler_lagrange_equations() -> dict[str, Any]:
    """Vary every scalar variable in the same finite-mode action."""

    action = derive_quadratic_action()
    s = action["symbols"]
    coordinates = [s[name] for name in ("z", "E", "xi", "X", "n", "B", "ell")]
    Xd, nd, elld = sp.symbols("x_dot n_dot delta_lambda_dot", real=True)
    xidd, Xdd, ndd, Bdd, elldd = sp.symbols(
        "sigma_ddot x_ddot n_ddot B_ddot delta_lambda_ddot", real=True
    )
    velocities = [s["zd"], s["Ed"], s["xid"], Xd, nd, s["Bd"], elld]
    accelerations = [s["zdd"], s["Edd"], xidd, Xdd, ndd, Bdd, elldd]
    velocity_of = dict(zip(coordinates, velocities))
    acceleration_of = dict(zip(velocities, accelerations))
    L = action["lagrangian"]

    def total_time_derivative(expression: sp.Expr) -> sp.Expr:
        return sp.factor(
            sum(sp.diff(expression, q) * velocity_of[q] for q in coordinates)
            + sum(sp.diff(expression, velocity) * acceleration_of[velocity] for velocity in velocities)
        )

    equations: dict[sp.Symbol, sp.Expr] = {}
    for coordinate, velocity in zip(coordinates, velocities):
        equations[coordinate] = sp.factor(
            total_time_derivative(sp.diff(L, velocity)) - sp.diff(L, coordinate)
        )

    static_xi_equation = sp.factor(
        equations[s["xi"]].subs(
            {
                s["zd"]: 0,
                s["Ed"]: 0,
                s["xid"]: 0,
                s["zdd"]: 0,
                s["Edd"]: 0,
                xidd: 0,
                s["B"]: 0,
                s["Bd"]: 0,
            }
        )
    )

    return {
        "symbols": {
            **s,
            "Xd": Xd,
            "nd": nd,
            "elld": elld,
            "xidd": xidd,
            "Xdd": Xdd,
            "ndd": ndd,
            "Bdd": Bdd,
            "elldd": elldd,
        },
        "equations": equations,
        "static_xi_equation": static_xi_equation,
        "covariant_xi_equation": "D_i D^i X - R_mn nhat^m nhat^n = 0",
        "integration_by_parts_warning": (
            "With the N sqrt(h) measure, the formal adjoint of D_i D^i "
            "contains the lapse acceleration; it must not be identified with "
            "the lapse-weighted Laplacian in the xi Euler equation."
        ),
    }


@functools.lru_cache(maxsize=1)
def derive_finite_k_dirac() -> dict[str, Any]:
    """Run the finite-k Dirac chain after fixing the clock to unitary gauge.

    The clock norm multiplier is retained.  Its perturbation is a canonical
    coordinate with a primary momentum constraint; varying it enforces n=0.
    This is the term missing from the tempting six-variable truncation.
    """

    action = derive_quadratic_action()
    s = action["symbols"]
    z, E, xi, X, n, B, ell = (
        s[name] for name in ("z", "E", "xi", "X", "n", "B", "ell")
    )
    zd, Ed, xid = (s[name] for name in ("zd", "Ed", "xid"))
    L = action["lagrangian"]

    pz, pE, pxi, pX, pn, pB, pell = sp.symbols(
        "p_zeta p_E p_sigma p_x p_n p_B p_delta_lambda", real=True
    )
    coordinates = [z, E, xi, X, n, B, ell]
    canonical_momenta = [pz, pE, pxi, pX, pn, pB, pell]
    momenta = [pz, pE, pxi]
    velocities = [zd, Ed, xid]
    differentiated_momenta = [sp.factor(sp.diff(L, velocity)) for velocity in velocities]
    velocity_hessian = sp.simplify(sp.hessian(L, velocities))
    inverse_solution = sp.solve(
        [sp.Eq(momentum, expression) for momentum, expression in zip(momenta, differentiated_momenta)],
        velocities,
        dict=True,
        simplify=True,
    )[0]
    inverse_legendre_check = {
        velocity: sp.factor(solution.subs(dict(zip(momenta, differentiated_momenta))))
        for velocity, solution in inverse_solution.items()
    }
    canonical_hamiltonian = sp.factor(
        (sum(momentum * velocity for momentum, velocity in zip(momenta, velocities)) - L).subs(
            inverse_solution
        )
    )

    u_n, u_B, u_X, u_ell = sp.symbols(
        "u_n u_B u_x u_delta_lambda", real=True
    )
    primary_constraints = [pn, pB, pX, pell]
    total_hamiltonian = sp.expand(
        canonical_hamiltonian
        + u_n * pn
        + u_B * pB
        + u_X * pX
        + u_ell * pell
    )
    primary_preservation = [
        sp.factor(_pb(constraint, total_hamiltonian, coordinates, canonical_momenta))
        for constraint in primary_constraints
    ]

    # These normalizations are taken from the calculated primary preservation
    # equations; no constraint is supplied independently of the Hamiltonian.
    secondary_constraints = [
        primary_preservation[0],
        -primary_preservation[1],
        -primary_preservation[2],
        primary_preservation[3] / 2,
    ]
    secondary_constraints = [sp.factor(item) for item in secondary_constraints]
    all_constraints = primary_constraints + secondary_constraints
    constraint_jacobian = sp.Matrix(all_constraints).jacobian(
        coordinates + canonical_momenta
    )
    poisson_matrix = sp.Matrix(
        [
            [
                _pb(left, right, coordinates, canonical_momenta)
                for right in all_constraints
            ]
            for left in all_constraints
        ]
    )
    poisson_rank = poisson_matrix.rank()
    minor_indices, maximal_minor = _first_nonzero_principal_minor(
        poisson_matrix, poisson_rank
    )

    secondary_preservation = [
        sp.factor(_pb(constraint, total_hamiltonian, coordinates, canonical_momenta))
        for constraint in secondary_constraints
    ]
    constraint_surface = sp.solve(
        secondary_constraints, [n, pE, xi, ell], dict=True, simplify=True
    )[0]
    preservation_on_surface = [
        sp.factor(item.subs(constraint_surface)) for item in secondary_preservation
    ]
    fixed_multiplier = sp.solve(
        [sp.Eq(item, 0) for item in preservation_on_surface],
        [u_n, u_X, u_ell],
        dict=True,
        simplify=True,
    )[0]
    preservation_after_multipliers = [
        sp.factor(item.subs(fixed_multiplier)) for item in preservation_on_surface
    ]
    tertiary_constraints = [
        item for item in preservation_after_multipliers if item != 0
    ]

    second_class_count = poisson_rank
    first_class_count = len(all_constraints) - poisson_rank
    phase_dimension = 2 * len(coordinates)
    physical_scalar_dof = sp.simplify(
        sp.Rational(1, 2)
        * (phase_dimension - 2 * first_class_count - second_class_count)
    )

    return {
        "symbols": {
            **s,
            "p_z": pz,
            "p_E": pE,
            "p_xi": pxi,
            "p_X": pX,
            "p_n": pn,
            "p_B": pB,
            "p_ell": pell,
            "u_n": u_n,
            "u_B": u_B,
            "u_X": u_X,
            "u_ell": u_ell,
        },
        "coordinates": coordinates,
        "canonical_momenta": canonical_momenta,
        "lagrangian": L,
        "velocities": velocities,
        "momenta": momenta,
        "dL_dvelocities": differentiated_momenta,
        "velocity_hessian": velocity_hessian,
        "velocity_hessian_rank": velocity_hessian.rank(),
        "velocity_hessian_determinant": sp.factor(velocity_hessian.det()),
        "inverse_legendre": inverse_solution,
        "inverse_legendre_check": inverse_legendre_check,
        "canonical_hamiltonian": canonical_hamiltonian,
        "primary_constraints": primary_constraints,
        "primary_preservation": primary_preservation,
        "secondary_constraints": secondary_constraints,
        "secondary_preservation": secondary_preservation,
        "constraint_surface": constraint_surface,
        "fixed_multiplier": fixed_multiplier,
        "preservation_after_constraints": preservation_after_multipliers,
        "tertiary_constraints": tertiary_constraints,
        "constraint_order": (
            "p_n", "p_B", "p_X", "p_delta_lambda",
            "S_n", "C_B", "C_X", "C_delta_lambda",
        ),
        "constraint_jacobian": constraint_jacobian,
        "constraint_jacobian_rank": constraint_jacobian.rank(),
        "poisson_matrix": poisson_matrix,
        "poisson_rank": poisson_rank,
        "maximal_minor_indices": minor_indices,
        "maximal_nonzero_minor": maximal_minor,
        "first_class_count": first_class_count,
        "second_class_count": second_class_count,
        "phase_dimension": phase_dimension,
        "physical_scalar_dof": physical_scalar_dof,
        "unitary_gauge_scope": True,
    }


@functools.lru_cache(maxsize=1)
def derive_reduced_scalar() -> dict[str, Any]:
    """Reduce the clock-retaining unitary-gauge block without dropping B."""

    action = derive_quadratic_action()
    finite = derive_finite_k_dirac()
    s0 = action["symbols"]
    A, k, beta = s0["A"], s0["k"], s0["beta"]
    z, E, xi, X, n, B, ell = (
        s0[name] for name in ("z", "E", "xi", "X", "n", "B", "ell")
    )
    zd, Ed, xid = s0["zd"], s0["Ed"], s0["xid"]
    y = sp.Symbol("y", positive=True)
    omega = sp.Symbol("omega", real=True)
    speed = sp.Symbol("c_squared", real=True)

    # C_delta_lambda fixes n=0 and C_X fixes X=xi/(2 beta).  E=0 is a spatial
    # gauge choice, but B must remain until its Euler equation is imposed.
    # Deleting B prematurely creates a spurious second wave and a fake ghost.
    constraint_and_spatial_gauge_solution = {
        n: 0,
        X: xi / (2 * beta),
        E: 0,
        Ed: 0,
    }
    reduced_lagrangian = sp.factor(
        action["lagrangian"].subs(constraint_and_spatial_gauge_solution)
    )
    Bd = s0["Bd"]
    zdd = s0["zdd"]
    xidd = sp.Symbol("sigma_ddot", real=True)
    reduced_coordinates = [z, xi, B]
    reduced_velocities = [zd, xid, Bd]
    reduced_accelerations = [zdd, xidd, sp.Symbol("B_ddot", real=True)]

    def total_time_derivative(expression: sp.Expr) -> sp.Expr:
        return sp.factor(
            sum(
                sp.diff(expression, q) * velocity
                for q, velocity in zip(reduced_coordinates, reduced_velocities)
            )
            + sum(
                sp.diff(expression, velocity) * acceleration
                for velocity, acceleration in zip(reduced_velocities, reduced_accelerations)
            )
        )

    equations = [
        sp.factor(
            total_time_derivative(sp.diff(reduced_lagrangian, velocity))
            - sp.diff(reduced_lagrangian, coordinate)
        )
        for coordinate, velocity in zip(reduced_coordinates, reduced_velocities)
    ]
    harmonic_substitution = {
        zd: -sp.I * omega * z,
        xid: -sp.I * omega * xi,
        Bd: -sp.I * omega * B,
        zdd: -omega**2 * z,
        xidd: -omega**2 * xi,
    }
    harmonic_equations = [
        sp.factor(equation.subs(harmonic_substitution)) for equation in equations
    ]
    harmonic_operator = sp.Matrix(
        [
            [sp.diff(equation, coordinate) for coordinate in reduced_coordinates]
            for equation in harmonic_equations
        ]
    )
    dispersion_determinant = sp.factor(harmonic_operator.det())
    zero_frequency_multiplicity = sp.Poly(
        dispersion_determinant, omega
    ).terms()[-1][0][0]
    nonzero_frequency_expression = sp.factor(
        dispersion_determinant / omega**zero_frequency_multiplicity
    )
    raw_speed_expression = sp.factor(
        nonzero_frequency_expression.subs(omega**2, speed * k**2)
    )
    speed_numerator = sp.together(raw_speed_expression).as_numer_denom()[0]
    speed_polynomial = sp.factor(sp.Poly(speed_numerator, speed).monic().as_expr())
    speed_roots = tuple(sp.solve(sp.Eq(speed_polynomial, 0), speed))

    beta_exact = 2 * A * sp.exp(-y)
    exact_speed_polynomial = sp.factor(speed_polynomial.subs(beta, beta_exact))
    exact_speed_roots = tuple(
        sp.simplify(root.subs(beta, beta_exact)) for root in speed_roots
    )

    # For omega != 0 the shift equation imposes xi=-4 A z.  Substitution
    # after deriving that equation gives the genuine one-mode Lagrangian.
    finite_frequency_solution = {xi: -4 * A * z, xid: -4 * A * zd}
    finite_frequency_lagrangian = sp.factor(
        reduced_lagrangian.subs(finite_frequency_solution)
    )
    finite_kinetic_coefficient = sp.factor(
        sp.diff(finite_frequency_lagrangian, zd, 2)
    )
    exact_speed = exact_speed_roots[0]
    speed_origin = sp.limit(exact_speed, y, 0, dir="+")
    speed_derivative = sp.factor(sp.diff(exact_speed, y))
    luminal_crossing = sp.solve(sp.Eq(exact_speed, 1), y)[0]

    fs = finite["symbols"]
    reduced_hamiltonian_substitution = {
        fs["n"]: 0,
        fs["E"]: 0,
        fs["X"]: fs["xi"] / (2 * fs["beta"]),
        fs["p_E"]: 0,
        fs["p_X"]: 0,
        fs["p_n"]: 0,
        fs["p_B"]: 0,
        fs["p_ell"]: 0,
    }
    reduced_hamiltonian = sp.factor(
        finite["canonical_hamiltonian"].subs(reduced_hamiltonian_substitution)
    )
    r, q, pr, pq = sp.symbols("r q p_r p_q", real=True)
    canonical_transformation = {
        fs["z"]: r,
        fs["xi"]: q - 4 * A * r,
        fs["p_z"]: pr + 4 * A * pq,
        fs["p_xi"]: pq,
    }
    charge_form_hamiltonian = sp.factor(
        reduced_hamiltonian.subs(canonical_transformation)
    )
    conserved_charge_velocity = sp.factor(sp.diff(charge_form_hamiltonian, pq))
    charge_sector_potential = sp.factor(charge_form_hamiltonian.subs(pr, 0))
    charge_sector_potential_hessian = sp.hessian(charge_sector_potential, [r, q])
    charge_sector_potential_determinant = sp.factor(
        charge_sector_potential_hessian.det()
    )

    return {
        "symbols": {**s0, "y": y, "omega": omega, "speed": speed},
        "constraint_and_spatial_gauge_solution": constraint_and_spatial_gauge_solution,
        "reduced_lagrangian": reduced_lagrangian,
        "reduced_coordinates": reduced_coordinates,
        "reduced_velocities": reduced_velocities,
        "euler_equations": equations,
        "shift_constraint": equations[2],
        "harmonic_equations": harmonic_equations,
        "harmonic_operator": harmonic_operator,
        "dispersion_determinant": dispersion_determinant,
        "zero_frequency_multiplicity": zero_frequency_multiplicity,
        "nonzero_frequency_expression": nonzero_frequency_expression,
        "speed_polynomial": speed_polynomial,
        "speed_roots": speed_roots,
        "beta_exact": beta_exact,
        "exact_speed_polynomial": exact_speed_polynomial,
        "exact_speed_roots": exact_speed_roots,
        "finite_frequency_solution": finite_frequency_solution,
        "finite_frequency_lagrangian": finite_frequency_lagrangian,
        "finite_kinetic_coefficient": finite_kinetic_coefficient,
        "finite_mode_no_ghost": sp.ask(sp.Q.positive(finite_kinetic_coefficient)) is True,
        "reduced_hamiltonian": reduced_hamiltonian,
        "canonical_charge_variables": {"r": r, "q": q, "p_r": pr, "p_q": pq},
        "canonical_transformation": canonical_transformation,
        "charge_form_hamiltonian": charge_form_hamiltonian,
        "conserved_charge_velocity": conserved_charge_velocity,
        "charge_sector_potential": charge_sector_potential,
        "charge_sector_potential_hessian": charge_sector_potential_hessian,
        "charge_sector_potential_determinant": charge_sector_potential_determinant,
        "energy_unbounded_across_charge_sectors": (
            sp.ask(sp.Q.negative(charge_sector_potential_determinant)) is True
        ),
        "exact_speed": exact_speed,
        "deep_mond_speed_limit": speed_origin,
        "speed_derivative": speed_derivative,
        "gradient_stable_for_positive_y": (
            speed_origin == 0 and sp.ask(sp.Q.positive(speed_derivative)) is True
        ),
        "luminal_crossing": luminal_crossing,
        "newtonian_speed_limit": sp.limit(exact_speed, y, sp.oo),
        "pb_minor_newtonian_limit": sp.limit(
            16 * beta_exact**2 * k**4, y, sp.oo
        ),
        "zero_frequency_sector_requires_full_clock_transport_analysis": True,
    }


@functools.lru_cache(maxsize=1)
def derive_zero_mode() -> dict[str, Any]:
    """Restart k=0 on FLRW with the norm multiplier still present."""

    A = sp.Symbol("A", positive=True)
    a = sp.Symbol("a", positive=True)
    N = sp.Symbol("N", positive=True)
    sigma, ell = sp.symbols("sigma lambda", real=True)
    adot, sigmadot = sp.symbols("a_dot sigma_dot", real=True)
    addot, Ndot = sp.symbols("a_ddot N_dot", real=True)
    pa, psigma, pN, pell = sp.symbols(
        "p_a p_sigma p_N p_lambda", real=True
    )
    Hubble, Hdot = sp.symbols("H H_dot", real=True)

    # Insert flat FLRW into A R-sigma R_nn, integrate dot(H) once, and add
    # N a^3 lambda(1-N^-2) exactly rather than freezing the clock sector.
    gravity_lagrangian = sp.factor(
        -6 * a * (A + sigma) * adot**2 / N
        - 3 * a**2 * sigmadot * adot / N
    )
    norm_lagrangian = sp.factor(a**3 * ell * (N - 1 / N))
    lagrangian = sp.factor(gravity_lagrangian + norm_lagrangian)
    velocities = [adot, sigmadot]
    velocity_hessian = sp.simplify(sp.hessian(lagrangian, velocities))
    momenta_from_lagrangian = [
        sp.factor(sp.diff(lagrangian, velocity)) for velocity in velocities
    ]
    inverse = sp.solve(
        [
            sp.Eq(pa, momenta_from_lagrangian[0]),
            sp.Eq(psigma, momenta_from_lagrangian[1]),
        ],
        velocities,
        dict=True,
    )[0]
    hamiltonian = sp.factor(
        (pa * adot + psigma * sigmadot - lagrangian).subs(inverse)
    )

    coordinates = [a, sigma, N, ell]
    canonical_momenta = [pa, psigma, pN, pell]
    uN, uell = sp.symbols("u_N u_lambda", real=True)
    primary_constraints = [pN, pell]
    total_hamiltonian = hamiltonian + uN * pN + uell * pell
    primary_preservation = [
        sp.factor(_pb(item, total_hamiltonian, coordinates, canonical_momenta))
        for item in primary_constraints
    ]
    secondary_constraints = primary_preservation
    all_constraints = primary_constraints + secondary_constraints
    zero_mode_pb = sp.Matrix(
        [
            [
                _pb(left, right, coordinates, canonical_momenta)
                for right in all_constraints
            ]
            for left in all_constraints
        ]
    )
    poisson_rank = zero_mode_pb.rank()
    minor_indices, maximal_minor = _first_nonzero_principal_minor(
        zero_mode_pb, poisson_rank
    )
    secondary_preservation = [
        sp.factor(_pb(item, total_hamiltonian, coordinates, canonical_momenta))
        for item in secondary_constraints
    ]
    multiplier_solution = sp.solve(
        [sp.Eq(item, 0) for item in secondary_preservation],
        [uN, uell],
        dict=True,
        simplify=False,
    )[0]
    preservation_after_multipliers = [
        sp.factor(item.subs(multiplier_solution)) for item in secondary_preservation
    ]

    first_class_count = len(all_constraints) - poisson_rank
    second_class_count = poisson_rank
    phase_dimension = 2 * len(coordinates)
    # Derive the load-bearing homogeneous equation from L0 itself.  This is
    # not assigned from the desired FLRW conclusion.
    sigma_momentum = sp.factor(sp.diff(lagrangian, sigmadot))
    sigma_momentum_time_derivative = sp.factor(
        sp.diff(sigma_momentum, a) * adot
        + sp.diff(sigma_momentum, adot) * addot
        + sp.diff(sigma_momentum, N) * Ndot
        + sp.diff(sigma_momentum, sigma) * sigmadot
    )
    sigma_euler_lagrange = sp.factor(
        sigma_momentum_time_derivative - sp.diff(lagrangian, sigma)
    )
    R_nn_geometry = sp.factor(
        -3 * (addot / (a * N**2) - adot * Ndot / (a * N**3))
    )
    variation_geometry_residual = sp.factor(
        sigma_euler_lagrange - N * a**3 * R_nn_geometry
    )
    proper_time_acceleration = sp.factor(-a * R_nn_geometry / 3)
    intrinsic_laplacian = sp.Integer(0)
    R_nn_hubble = -3 * (Hdot / N + Hubble**2)
    H_definition = adot / (a * N)
    Hdot_definition = sp.factor(
        addot / (a * N)
        - adot**2 / (a**2 * N)
        - adot * Ndot / (a * N**2)
    )
    hubble_geometry_residual = sp.factor(
        R_nn_hubble.subs({Hubble: H_definition, Hdot: Hdot_definition})
        - R_nn_geometry
    )
    de_sitter_residual = sp.simplify(R_nn_hubble.subs(Hdot, 0))

    return {
        "symbols": {
            "A": A,
            "a": a,
            "N": N,
            "sigma": sigma,
            "ell": ell,
            "adot": adot,
            "sigmadot": sigmadot,
            "addot": addot,
            "Ndot": Ndot,
            "p_a": pa,
            "p_sigma": psigma,
            "p_N": pN,
            "p_ell": pell,
            "u_N": uN,
            "u_ell": uell,
            "H": Hubble,
            "Hdot": Hdot,
        },
        "gravity_lagrangian": gravity_lagrangian,
        "norm_lagrangian": norm_lagrangian,
        "lagrangian": lagrangian,
        "velocity_hessian": velocity_hessian,
        "velocity_hessian_rank": velocity_hessian.rank(),
        "velocity_hessian_determinant": sp.factor(velocity_hessian.det()),
        "momenta": momenta_from_lagrangian,
        "inverse_legendre": inverse,
        "hamiltonian": hamiltonian,
        "primary_constraints": primary_constraints,
        "primary_preservation": primary_preservation,
        "secondary_constraints": secondary_constraints,
        "secondary_preservation": secondary_preservation,
        "fixed_multipliers": multiplier_solution,
        "preservation_after_multipliers": preservation_after_multipliers,
        "tertiary_constraints": [
            item for item in preservation_after_multipliers if item != 0
        ],
        "constraint_order": ("p_N", "p_lambda", "S_N", "S_lambda"),
        "poisson_matrix": zero_mode_pb,
        "poisson_rank": poisson_rank,
        "maximal_minor_indices": minor_indices,
        "maximal_nonzero_minor": maximal_minor,
        "first_class_count": first_class_count,
        "second_class_count": second_class_count,
        "phase_dimension": phase_dimension,
        "homogeneous_configuration_dof": sp.simplify(
            sp.Rational(1, 2)
            * (phase_dimension - 2 * first_class_count - second_class_count)
        ),
        "intrinsic_laplacian_on_homogeneous_X": intrinsic_laplacian,
        "sigma_momentum": sigma_momentum,
        "sigma_momentum_time_derivative": sigma_momentum_time_derivative,
        "sigma_euler_lagrange": sigma_euler_lagrange,
        "R_nn": R_nn_geometry,
        "R_nn_hubble": R_nn_hubble,
        "H_definition": H_definition,
        "Hdot_definition": Hdot_definition,
        "hubble_geometry_residual": hubble_geometry_residual,
        "variation_geometry_residual": variation_geometry_residual,
        "proper_time_acceleration": proper_time_acceleration,
        "de_sitter_residual": de_sitter_residual,
        "de_sitter_allowed": bool(de_sitter_residual == 0),
        "allowed_background_equation": sp.Eq(Hdot / N + Hubble**2, 0),
        "proper_time_scale_factor_equation": sp.Eq(proper_time_acceleration, 0),
    }


@functools.lru_cache(maxsize=1)
def derive_mutation_controls() -> dict[str, Any]:
    """Switch off the curvature vertex and watch the Legendre rank change."""

    action = derive_quadratic_action()
    s = action["symbols"]
    coupling = sp.Symbol("c_R", real=True)
    lagrangian = sp.expand(
        action["eh_kinetic"]
        + action["eh_spatial"]
        + coupling * action["curvature_coupling_after_parts"]
        + action["elliptic_sector"]
        + action["unit_clock_sector"]
    )
    velocities = [s["zd"], s["Ed"], s["xid"]]
    hessian = sp.simplify(sp.hessian(lagrangian, velocities))
    on = hessian.subs(coupling, 1)
    off = hessian.subs(coupling, 0)
    return {
        "coupling": coupling,
        "general_hessian": hessian,
        "general_determinant": sp.factor(hessian.det()),
        "coupling_on_hessian_rank": on.rank(),
        "coupling_off_hessian_rank": off.rank(),
        "coupling_on_determinant": sp.factor(on.det()),
        "coupling_off_determinant": sp.factor(off.det()),
    }


@functools.lru_cache(maxsize=1)
def derive_transport_dirac() -> dict[str, Any]:
    """Derive the first-order Q,M,nu transport primaries and shared PBs.

    This deliberately does not manufacture a block diagonal matrix.  The
    inverse spatial metric gives delta Z_s=-8 y^2 zeta, so Q mixes with the
    metric coordinate even for a Fourier vector transverse to grad Xbar.
    """

    finite = derive_finite_k_dirac()
    s0 = finite["symbols"]
    z = s0["z"]
    y = sp.Symbol("y", positive=True)
    M, nu = sp.symbols("delta_M delta_nu", real=True)
    pM, pnu = sp.symbols("p_M p_nu", real=True)
    Mdot, nudot = sp.symbols("M_dot nu_dot", real=True)
    uM, unu = sp.symbols("u_M u_nu", real=True)
    fZ = sp.exp(-y) / 2
    delta_Z = -8 * y**2 * z
    Q = sp.factor(M + fZ * delta_Z)

    coordinates = finite["coordinates"] + [M, nu]
    momenta = finite["canonical_momenta"] + [pM, pnu]
    # After expanding the full -C_M M-Q nu_dot action about its M equation,
    # nu_bar_dot=-C_M, the linear M pieces cancel.  C_M delta f supplies the
    # beta term in the frozen principal action and the remaining first-order
    # transport fluctuation is -delta Q delta nu_dot.
    transport_lagrangian = -Q * nudot
    transport_momenta_from_lagrangian = [
        sp.factor(sp.diff(transport_lagrangian, velocity))
        for velocity in (Mdot, nudot)
    ]
    transport_constraints = [
        sp.factor(momentum - derived)
        for momentum, derived in zip(
            (pM, pnu), transport_momenta_from_lagrangian
        )
    ]
    combined_constraints = (
        finite["primary_constraints"]
        + finite["secondary_constraints"]
        + transport_constraints
    )
    combined_poisson = sp.Matrix(
        [
            [_pb(left, right, coordinates, momenta) for right in combined_constraints]
            for left in combined_constraints
        ]
    )
    combined_rank = combined_poisson.rank()
    combined_constraint_jacobian = sp.Matrix(combined_constraints).jacobian(
        coordinates + momenta
    )
    minor_indices, combined_minor = _first_nonzero_principal_minor(
        combined_poisson, combined_rank
    )
    transport_poisson = sp.Matrix(
        [
            [_pb(left, right, coordinates, momenta) for right in transport_constraints]
            for left in transport_constraints
        ]
    )
    scalar_count = len(finite["primary_constraints"] + finite["secondary_constraints"])
    cross_block = combined_poisson.extract(
        range(scalar_count), range(scalar_count, len(combined_constraints))
    )
    transport_total_hamiltonian = (
        finite["canonical_hamiltonian"] + uM * pM + unu * (pnu + Q)
    )
    transport_primary_preservation = [
        sp.factor(_pb(item, transport_total_hamiltonian, coordinates, momenta))
        for item in transport_constraints
    ]
    transport_multiplier_solution = sp.solve(
        [sp.Eq(item, 0) for item in transport_primary_preservation],
        [uM, unu],
        dict=True,
        simplify=True,
    )[0]
    transport_preservation_after_multipliers = [
        sp.factor(item.subs(transport_multiplier_solution))
        for item in transport_primary_preservation
    ]
    Q_time_derivative = sp.factor(
        sp.diff(Q, M) * Mdot + sp.diff(Q, z) * s0["zd"]
    )
    nu_euler_lagrange = sp.factor(-Q_time_derivative)
    pnu_preservation = sp.factor(
        _pb(pnu, transport_total_hamiltonian, coordinates, momenta)
    )
    Q_is_independent_dirac_constraint = any(
        sp.simplify(item - Q) == 0 for item in transport_constraints
    )

    return {
        "symbols": {
            "k": s0["k"],
            "beta": s0["beta"],
            "y": y,
            "M": M,
            "nu": nu,
            "p_M": pM,
            "p_nu": pnu,
            "Mdot": Mdot,
            "nudot": nudot,
            "u_M": uM,
            "u_nu": unu,
        },
        "delta_Z_metric": delta_Z,
        "f_Z_exact": fZ,
        "Q_constraint": Q,
        "metric_mixing_present": sp.diff(Q, z) != 0,
        "transport_lagrangian": transport_lagrangian,
        "transport_momenta_from_lagrangian": transport_momenta_from_lagrangian,
        "transport_constraint_order": ("p_M", "p_nu+Q"),
        "transport_poisson_matrix": transport_poisson,
        "transport_rank": transport_poisson.rank(),
        "transport_total_hamiltonian": transport_total_hamiltonian,
        "transport_primary_preservation": transport_primary_preservation,
        "transport_fixed_multipliers": transport_multiplier_solution,
        "transport_preservation_after_multipliers": transport_preservation_after_multipliers,
        "transport_tertiary_constraints": [
            item for item in transport_preservation_after_multipliers if item != 0
        ],
        "Q_time_derivative": Q_time_derivative,
        "nu_euler_lagrange": nu_euler_lagrange,
        "p_nu_preservation": pnu_preservation,
        "Q_is_independent_dirac_constraint": Q_is_independent_dirac_constraint,
        "Q_zero_is_branch_not_dirac_constraint": not Q_is_independent_dirac_constraint,
        "Q_zero_branch_condition": sp.Eq(pnu, 0),
        "combined_constraint_order": finite["constraint_order"] + ("p_M", "p_nu+Q"),
        "combined_poisson_matrix": combined_poisson,
        "combined_rank": combined_rank,
        "combined_constraint_jacobian": combined_constraint_jacobian,
        "combined_constraint_jacobian_rank": combined_constraint_jacobian.rank(),
        "combined_first_class_count": len(combined_constraints) - combined_rank,
        "combined_second_class_count": combined_rank,
        "combined_phase_dimension": 2 * len(coordinates),
        "combined_scalar_configuration_dof": sp.simplify(
            sp.Rational(1, 2)
            * (
                2 * len(coordinates)
                - 2 * (len(combined_constraints) - combined_rank)
                - combined_rank
            )
        ),
        "combined_maximal_minor_indices": minor_indices,
        "combined_nonzero_minor": combined_minor,
        "calculated_cross_block": cross_block,
        "equal_time_cross_block_zero": cross_block == sp.zeros(*cross_block.shape),
        "scope_warning": (
            "This calculated principal transport chain includes Q's metric "
            "dependence.  It does not replace the missing covariant pre-gauge "
            "clock analysis.  The independent FLRW obstruction already kills "
            "the candidate."
        ),
    }


def derive_tensor_and_ward_gates() -> dict[str, Any]:
    """Record what remains standard in the favorable background."""

    A = sp.Symbol("A", positive=True)
    k, omega = sp.symbols("k_T omega_T", positive=True)
    hp, hx, hpd, hxd = sp.symbols("h_plus h_cross h_plus_dot h_cross_dot", real=True)
    tensor_lagrangian = sp.factor(
        A / 4 * (hpd**2 + hxd**2 - k**2 * (hp**2 + hx**2))
    )
    tensor_hessian = sp.hessian(tensor_lagrangian, [hpd, hxd])
    tensor_operator = sp.factor(omega**2 - k**2)
    matter_auxiliary_variation = sp.Integer(0)  # S_aux has no psi dependence.

    return {
        "tensor_lagrangian": tensor_lagrangian,
        "tensor_velocity_hessian": tensor_hessian,
        "tensor_hessian_positive": all(
            sp.ask(sp.Q.positive(value)) is True
            for value in tensor_hessian.diagonal()
        ),
        "tensor_polarizations": tensor_hessian.rank(),
        "tensor_operator": tensor_operator,
        "c_T_squared": sp.simplify(sp.solve(sp.Eq(tensor_operator, 0), omega**2)[0] / k**2),
        "auxiliary_direct_matter_euler_derivative": matter_auxiliary_variation,
        "ordinary_matter_ward_on_matter_shell": (
            "nabla_mu T_m^{mu nu}=E_psi^m nabla^nu psi=0"
        ),
    }


def derive_all() -> dict[str, Any]:
    kernel = derive_exact_kernel()
    static_mond = derive_static_mond_law()
    action = derive_quadratic_action()
    euler_lagrange = derive_euler_lagrange_equations()
    finite = derive_finite_k_dirac()
    reduced = derive_reduced_scalar()
    zero = derive_zero_mode()
    mutation = derive_mutation_controls()
    transport = derive_transport_dirac()
    tensor_ward = derive_tensor_and_ward_gates()

    analyzed_unitary_gauge_configuration_count = sp.simplify(
        tensor_ward["tensor_polarizations"]
        + transport["combined_scalar_configuration_dof"]
    )
    candidate_dead_reasons = []
    if transport["combined_scalar_configuration_dof"] != 0:
        candidate_dead_reasons.append(
            "unitary-gauge principal block contains a wave, conserved charge, and transport pair"
        )
    if zero["de_sitter_allowed"] is False:
        candidate_dead_reasons.append(
            "exact intrinsic homogeneous equation forces coasting and excludes viable FLRW"
        )
    if reduced["newtonian_speed_limit"] is sp.oo:
        candidate_dead_reasons.append("scalar cone becomes infinitely fast in the Newtonian limit")
    if kernel["f_ZZ_zero_limit"] is -sp.oo:
        candidate_dead_reasons.append(
            "zero-field operator loses ellipticity and the constitutive Hessian diverges"
        )
    if reduced["energy_unbounded_across_charge_sectors"]:
        candidate_dead_reasons.append(
            "principal Hamiltonian is unbounded across conserved-charge sectors"
        )
    candidate_status = "DEAD" if candidate_dead_reasons else "OPEN"

    return {
        "kernel": kernel,
        "static_mond": static_mond,
        "quadratic_action": action,
        "euler_lagrange": euler_lagrange,
        "finite_k": finite,
        "reduced_scalar": reduced,
        "k_zero": zero,
        "mutation": mutation,
        "transport": transport,
        "tensor_and_ward": tensor_ward,
        "analyzed_unitary_gauge_configuration_count": analyzed_unitary_gauge_configuration_count,
        "analyzed_unitary_gauge_scalar_configuration_count": transport["combined_scalar_configuration_dof"],
        "full_covariant_gravitational_dof": "UNRESOLVED_BEFORE_DECISIVE_FLRW_FAILURE",
        "candidate_status": candidate_status,
        "candidate_dead_reasons": candidate_dead_reasons,
        "parent_program_status": "OPEN",
        "Phi_minus_Psi": "UNCOMPUTED_FROM_FULL_METRIC_EQUATIONS",
        "gamma_PPN": "UNCOMPUTED_AFTER_DECISIVE_FLRW_FAILURE",
        "beta_PPN": "UNCOMPUTED_AFTER_DECISIVE_FLRW_FAILURE",
        "alpha_1": "UNCOMPUTED_AFTER_DECISIVE_FLRW_FAILURE",
        "alpha_2": "UNCOMPUTED_AFTER_DECISIVE_FLRW_FAILURE",
        "alpha_3": "UNCOMPUTED_AFTER_DECISIVE_FLRW_FAILURE",
    }


def _check(label: str, condition: Any) -> bool:
    passed = bool(condition)
    print(f"  [{'PASS' if passed else 'FAIL'}] {label}")
    return passed


def main() -> int:
    result = derive_all()
    kernel = result["kernel"]
    static_mond = result["static_mond"]
    action = result["quadratic_action"]
    euler = result["euler_lagrange"]
    finite = result["finite_k"]
    reduced = result["reduced_scalar"]
    zero = result["k_zero"]
    mutation = result["mutation"]
    transport = result["transport"]
    tensor = result["tensor_and_ward"]

    print("=" * 104)
    print("INTRINSIC-ELLIPTIC DW ACTION: CLOCK-RETAINING FALSIFICATION GATE")
    print("=" * 104)
    print("\n[1] Exact exponential constitutive branch")
    print("  f(Z_s) =", kernel["f"])
    print("  f_Z(4 y^2) =", kernel["f_Z"])
    print("  mu_eff =", kernel["mu_eff"])
    print("  elliptic eigenvalues =", kernel["lambda_perp"], "/", kernel["lambda_parallel"])
    print("  y=0 eigenvalues =", kernel["ellipticity_origin"])
    print("  f_ZZ at Z->0+ =", kernel["f_ZZ_zero_limit"])
    print("  reduced branch density/flux =", static_mond["gradient_density"], "/", static_mond["flux"])
    print("  spherical/deep law =", static_mond["spherical_equation"], "/ v^4 =", static_mond["btfr"])
    print("  WARNING: this static reduction assumes Q=0 and X=Phi; it is not an independent Phi/Psi derivation.")

    print("\n[2] Varied seven-field frozen-coefficient principal density (xi_bar=0)")
    print("  L_k =", action["lagrangian"])
    print("  unit-clock term =", action["unit_clock_sector"])
    print("  delta Z_s from the metric =", action["delta_Z_metric"])
    for coordinate, equation in euler["equations"].items():
        print("   EL[", coordinate, "] =", equation)
    print("  covariant xi equation =", euler["covariant_xi_equation"])

    print("\n[3] Unitary-gauge principal finite-k Dirac chain")
    print("  det/rank W =", finite["velocity_hessian_determinant"], "/", finite["velocity_hessian_rank"])
    print("  H_c =", finite["canonical_hamiltonian"])
    print("  primaries =", finite["primary_constraints"])
    print("  primary preservation =", finite["primary_preservation"])
    print("  secondaries =", finite["secondary_constraints"])
    print("  fixed multipliers =", finite["fixed_multiplier"])
    print("  tertiary constraints =", finite["tertiary_constraints"])
    print("  independent constraint Jacobian rank =", finite["constraint_jacobian_rank"])
    print("  PB matrix =", finite["poisson_matrix"])
    print("  PB rank/minor =", finite["poisson_rank"], "/", finite["maximal_nonzero_minor"])
    print("  first/second class =", finite["first_class_count"], "/", finite["second_class_count"])
    print("  scalar configuration count =", finite["physical_scalar_dof"])

    print("\n[4] Shift-preserving pole reduction")
    print("  L after n,X,E constraints (B retained) =", reduced["reduced_lagrangian"])
    print("  shift equation =", reduced["shift_constraint"])
    print("  harmonic determinant =", reduced["dispersion_determinant"])
    print("  zero-frequency multiplicity =", reduced["zero_frequency_multiplicity"])
    print("  nonzero-mode c_s^2(y) =", reduced["exact_speed"])
    print("  nonzero-mode L =", reduced["finite_frequency_lagrangian"])
    print("  canonical H(r,q) =", reduced["charge_form_hamiltonian"])
    print("  q_dot =", reduced["conserved_charge_velocity"])
    print("  charge-sector potential Hessian determinant =", reduced["charge_sector_potential_determinant"])
    print("  luminal at y / Newtonian limit =", reduced["luminal_crossing"], "/", reduced["newtonian_speed_limit"])

    print("\n[5] M,nu transport derived from -Q nu_dot")
    print("  Q =", transport["Q_constraint"])
    print("  metric mixing present =", transport["metric_mixing_present"])
    print("  primaries =", transport["transport_constraint_order"])
    print("  primary PB/rank =", transport["transport_poisson_matrix"], "/", transport["transport_rank"])
    print("  preservation =", transport["transport_primary_preservation"])
    print("  fixed multipliers =", transport["transport_fixed_multipliers"])
    print("  Q=0 is a conserved branch, not a generated Dirac constraint =", transport["Q_zero_is_branch_not_dirac_constraint"])
    print("  combined constraint Jacobian/PB ranks =", transport["combined_constraint_jacobian_rank"], "/", transport["combined_rank"])
    print("  combined first/second class =", transport["combined_first_class_count"], "/", transport["combined_second_class_count"])
    print("  extended unitary-gauge scalar configurations =", transport["combined_scalar_configuration_dof"])

    print("\n[6] k=0 metric-xi-clock subchain and exact xi FLRW equation")
    print("  L_0 =", zero["lagrangian"])
    print("  det/rank W_0 =", zero["velocity_hessian_determinant"], "/", zero["velocity_hessian_rank"])
    print("  primaries/secondaries =", zero["primary_constraints"], "/", zero["secondary_constraints"])
    print("  PB rank/minor =", zero["poisson_rank"], "/", zero["maximal_nonzero_minor"])
    print("  homogeneous configuration count =", zero["homogeneous_configuration_dof"])
    print("  Delta_u X_hom =", zero["intrinsic_laplacian_on_homogeneous_X"])
    print("  EL_sigma - N a^3 R_nn =", zero["variation_geometry_residual"])
    print("  xi equation = R_nn =", zero["R_nn"], "= 0")
    print("  proper-time consequence =", zero["proper_time_scale_factor_equation"])
    print("  de Sitter residual =", zero["de_sitter_residual"])

    print("\n[7] Mutation and favorable gates")
    print("  det W(c_R) =", mutation["general_determinant"])
    print("  rank curvature on/off =", mutation["coupling_on_hessian_rank"], "/", mutation["coupling_off_hessian_rank"])
    print("  favorable-background tensor polarizations/c_T^2 =", tensor["tensor_polarizations"], "/", tensor["c_T_squared"])
    print("  ordinary-matter Ward identity =", tensor["ordinary_matter_ward_on_matter_shell"])

    checks = [
        _check("f differentiates to exactly mu=1-exp(-y)", kernel["mu_residual"] == 0),
        _check("the reduced static branch varies to exact MOND", sp.simplify(static_mond["mu_from_flux"] - kernel["mu_target"].subs(kernel["symbols"]["y"], static_mond["symbols"]["y"])) == 0),
        _check("the exact y=0 point loses ellipticity", kernel["ellipticity_origin"] == (0, 0)),
        _check("the constitutive second derivative diverges at Z=0", kernel["f_ZZ_zero_limit"] == -sp.oo),
        _check("all seven finite-k Euler equations were varied", len(euler["equations"]) == 7),
        _check("delta_lambda really enforces n=0", sp.simplify(euler["equations"][action["symbols"]["ell"]] + 2 * action["symbols"]["n"]) == 0),
        _check("the finite-k constraint set is functionally independent", finite["constraint_jacobian_rank"] == len(finite["primary_constraints"] + finite["secondary_constraints"])),
        _check("the calculated finite-k chain closes", not finite["tertiary_constraints"]),
        _check("the calculated PB matrix leaves two scalar configurations", finite["physical_scalar_dof"] == 2),
        _check("retaining B yields one nonzero pole plus a zero-frequency charge", reduced["zero_frequency_multiplicity"] == 2 and reduced["conserved_charge_velocity"] == 0),
        _check("the nonzero scalar has positive kinetic and gradient terms for y>0", reduced["finite_mode_no_ghost"] and reduced["gradient_stable_for_positive_y"]),
        _check("the principal energy is unbounded across charge sectors", reduced["energy_unbounded_across_charge_sectors"]),
        _check("the M,nu primaries are derived and close without Q=0 insertion", transport["transport_rank"] == 2 and not transport["transport_tertiary_constraints"] and transport["Q_zero_is_branch_not_dirac_constraint"]),
        _check("the extended principal PB calculation exposes three scalar configurations", transport["combined_constraint_jacobian_rank"] == 10 and transport["combined_scalar_configuration_dof"] == 3),
        _check("the k=0 metric-xi-clock subchain closes", zero["poisson_rank"] == 4 and not zero["tertiary_constraints"]),
        _check("the varied homogeneous xi equation equals N a^3 R_nn", zero["variation_geometry_residual"] == 0 and zero["hubble_geometry_residual"] == 0),
        _check("the exact homogeneous xi equation excludes de Sitter", not zero["de_sitter_allowed"]),
        _check("curvature coupling is load-bearing in the velocity rank", mutation["coupling_off_hessian_rank"] < mutation["coupling_on_hessian_rank"]),
        _check("the favorable TT and ordinary-matter Ward gates remain standard", tensor["c_T_squared"] == 1 and tensor["auxiliary_direct_matter_euler_derivative"] == 0),
    ]

    print("\n[VERDICT]")
    print("  candidate status =", result["candidate_status"])
    for reason in result["candidate_dead_reasons"]:
        print("   -", reason)
    print("  extended principal unitary-gauge scalar count =", result["analyzed_unitary_gauge_scalar_configuration_count"])
    print("  analyzed tensor+scalar configuration count =", result["analyzed_unitary_gauge_configuration_count"])
    print("  full covariant N_grav =", result["full_covariant_gravitational_dof"])
    print("  Phi-Psi / gamma_PPN =", result["Phi_minus_Psi"], "/", result["gamma_PPN"])
    print("  alpha_1,alpha_2,alpha_3 =", result["alpha_1"], result["alpha_2"], result["alpha_3"])
    print("  parent fried-chicken program =", result["parent_program_status"])
    print("  The decisive result is action-level: homogeneous intrinsic Delta_u X vanishes,")
    print("  so the xi equation forces R_nn=0 and d^2a/dtau^2=0.  This excludes radiation,")
    print("  matter, de Sitter, and LambdaCDM acceleration.  The candidate is DEAD even though")
    print("  the wider metric-spectral/nonlocal architecture remains OPEN.")
    print(f"  Reproducibility checks: {sum(checks)}/{len(checks)}")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
