"""VCDM+f(a^2): action-derived FLRW scalar/zero-mode falsification gate.

c=1, M^2>0, Kij=(dot h_ij-Lie_shift h_ij)/(2N), X=-(d sigma)^2/2.
Spatial gauge h_ij=a^2 exp(2 zeta) delta_ij. D_i varphi=0 is imposed only
for k!=0; its independent homogeneous mode is treated by derive_homogeneous.
P(X) matter has q=dot sigma!=0, Z=P_X>0, D=P_X+q^2 P_XX>0.
alpha=f_s(0); exact exponential MOND requires alpha=1, unmodified control=0.
No ranks, determinants, dispersion relations, or mode counts are inputs.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path

import sympy as s


def pb(f, g, coords, momenta):
    return s.expand(sum(s.diff(f, x)*s.diff(g, p)-s.diff(f, p)*s.diff(g, x)
                        for x, p in zip(coords, momenta)))


@lru_cache(None)
def derive_nonzero_mode():
    e, theta = s.symbols("epsilon theta", real=True)
    a, M, k, q, Z, D = s.symbols("a M k q Z D", positive=True)
    alpha, H, varphi, varphidot, U, P0 = s.symbols("alpha H varphi varphidot U P0", real=True)
    z, zd, n, v, u, ud = s.symbols("z zd n v u ud", real=True)
    C, S = s.cos(theta), s.sin(theta)
    dx = lambda expr: k*s.diff(expr, theta)
    zeta, lapse, shift = e*z*C, 1+e*n*C, e*v*S
    scale = a**2*s.exp(2*zeta)
    volume = a**3*s.exp(3*zeta)
    # Compute the actual diagonal extrinsic-curvature tensor using the Lie
    # derivative of h. This retains trace velocities until after lambda's
    # algebraic variation has been accounted for.
    hdot = 2*(H+e*zd*C)*scale
    Kmixed = s.diag(*[(hdot-shift*dx(scale)-(2*scale*dx(shift) if i == 0 else 0))
                       /(2*lapse*scale) for i in range(3)])
    Ktrace = s.trace(Kmixed)
    KT2 = s.simplify(s.trace(Kmixed*Kmixed)-Ktrace**2/3)
    # Three-dimensional conformal curvature, calculated from Christoffels.
    h, hi = s.eye(3)*scale, s.eye(3)/scale
    deriv = lambda expr, i: dx(expr) if i == 0 else s.S.Zero
    Gamma = [[[s.simplify(sum(hi[i, l]*(deriv(h[l, b], j)+deriv(h[l, j], b)
                      -deriv(h[j, b], l)) for l in range(3))/2)
               for b in range(3)] for j in range(3)] for i in range(3)]
    Ric = s.Matrix(3, 3, lambda i, j: sum(
        deriv(Gamma[l][i][j], l)-deriv(Gamma[l][i][l], j)
        +sum(Gamma[l][i][j]*Gamma[m][l][m]-Gamma[m][i][l]*Gamma[l][j][m]
             for m in range(3)) for l in range(3)))
    R = s.simplify(sum(hi[i, j]*Ric[i, j] for i in range(3) for j in range(3)))
    acc2 = dx(lapse)**2/(lapse**2*scale)
    X = (q+e*ud*C-shift*dx(e*u*C))**2/(2*lapse**2)-dx(e*u*C)**2/(2*scale)
    deltaX = X-q**2/2
    pressure = P0+Z*deltaX+(D-Z)*deltaX**2/(2*q**2)
    matter = lapse*volume*pressure
    # After varying lambda: lambda=-2(K+varphi)/3 and U=varphi^2/3-V.
    raw = M**2*lapse*volume*(R/2+KT2/2+s.Rational(2, 3)*varphi*Ktrace+U+alpha*acc2)+matter
    integrated = M**2*volume*(lapse*(R/2+KT2/2+U+alpha*acc2)-s.Rational(2, 3)*varphidot)+matter

    def mode_coefficient(expr):
        quadratic = s.expand(s.series(expr, e, 0, 3).removeO()).coeff(e, 2)
        quadratic = s.expand_trig(s.expand(quadratic))
        # Twice the average over a period, so a free matter mode has D ud^2/2.
        return s.expand(2*quadratic.subs({C**2: s.Rational(1, 2), S**2: s.Rational(1, 2)}))

    raw2, int2 = mode_coefficient(raw), mode_coefficient(integrated)
    boundary_dt = 3*M**2*a**3*((varphidot+3*H*varphi)*z**2+2*varphi*z*zd)
    boundary_residual = s.simplify(raw2-int2-boundary_dt)
    # These are background equations derived independently from the
    # homogeneous action, not assumptions of staticity or vanishing H.
    background = {U: (q**2*Z-P0)/M**2, varphidot: 3*q**2*Z/(2*M**2)}
    L = s.factor(int2.subs(background)/a**3)
    potential_residual = s.simplify(s.diff(L, z, 2).subs(k, 0)+s.diff(L, z, n).subs(k, 0))
    auxiliaries = (n, z, v)
    constraints = [s.diff(L, b) for b in auxiliaries]
    Saux = s.hessian(L, auxiliaries)
    solution = s.solve(constraints, auxiliaries, dict=True)[0]
    reduced = s.factor(L.subs(solution))
    kinetic = s.factor(s.diff(reduced, ud, 2))
    gradient_mass = s.factor(-s.diff(reduced, u, 2))
    omega2 = s.factor(gradient_mass/kinetic)
    density = s.factor((q*D*(ud-q*n)).subs(solution))
    return dict(a=a, M=M, k=k, q=q, Z=Z, D=D, alpha=alpha,
                u=u, ud=ud, auxiliaries=auxiliaries, physical_k2=k**2/a**2,
                raw_quadratic=raw2, integrated_quadratic=int2, L=L,
                boundary_residual=boundary_residual,
                background_tadpole_residual=potential_residual,
                auxiliary_hessian=Saux.tolist(), auxiliary_determinant=s.factor(Saux.det()),
                auxiliary_solution=solution,
                constraint_residuals=[s.simplify(c.subs(solution)) for c in constraints],
                reduced_L=reduced, kinetic=kinetic, gradient_mass=gradient_mass, omega2=omega2,
                density=density,
                mond_kinetic=s.factor(kinetic.subs(alpha, 1)),
                mond_density=s.factor(density.subs(alpha, 1)),
                mond_UV_speed2=s.factor(s.limit(omega2.subs(alpha, 1)/(k**2/a**2), k, s.oo)),
                control_UV_speed2=s.factor(s.limit(omega2.subs(alpha, 0)/(k**2/a**2), k, s.oo)))


def scalar_dirac(d):
    """Actual canonical algorithm for the gauge-fixed quadratic scalar sector.

    D_i varphi=0 and spatial gauge have already been reduced; this is NOT
    a full nonlinear gravitational constraint count. Includes time-dependent
    secondary coefficients through arbitrary source terms in preservation.
    """
    n, z, v = d["auxiliaries"]
    u, ud = d["u"], d["ud"]
    L = d["L"].subs(d["alpha"], 1)
    coords = [u, n, z, v]
    pu, pn, pz, pv = momenta = list(s.symbols("pu pn pz pv", real=True))
    # Overall a^3 is retained in the canonical momentum and brackets.
    Lfull = d["a"]**3*L
    velocity = s.solve(pu-s.diff(Lfull, ud), ud)[0]
    Hamiltonian = s.factor((pu*ud-Lfull).subs(ud, velocity))
    primary = [pn, pz, pv]
    secondary = [s.factor(pb(p, Hamiltonian, coords, momenta)) for p in primary]
    cs = primary+secondary
    Omega = s.Matrix([[pb(c, b, coords, momenta) for b in cs] for c in cs])
    determinant = s.factor(Omega.det())
    # Nonzero exact determinant proves full rank; rank is also calculated.
    rank = Omega.rank()
    multipliers = s.Matrix(s.symbols("un uz uv"))
    ct = s.Matrix(s.symbols("Ct_n Ct_z Ct_v"))
    Dmul = s.Matrix([[pb(c, p, coords, momenta) for p in primary] for c in secondary])
    drift = s.Matrix([pb(c, Hamiltonian, coords, momenta) for c in secondary])+ct
    solved_multipliers = Dmul.inv()*(-drift)
    remainder = [s.simplify(x) for x in Dmul*solved_multipliers+drift]
    count_first = len(cs)-rank
    # Reclassify the canonical-matter vacuum BEFORE solving the nonvacuum
    # constraints: solutions proportional to 1/q cannot be continued to q=0.
    vac_sub = {d["q"]: 0, d["Z"]: 1, d["D"]: 1}
    vac_H = Hamiltonian.subs(vac_sub)
    vac_raw = [s.factor(pb(p, vac_H, coords, momenta)) for p in primary]
    vac_jac = s.Matrix(vac_raw).jacobian(coords+momenta)
    pivots = vac_jac.T.rref()[1]
    vac_sec = [vac_raw[i] for i in pivots]
    vac_cs = primary+vac_sec
    vac_omega = s.Matrix([[pb(c, b, coords, momenta) for b in vac_cs] for c in vac_cs])
    vac_rank = vac_omega.rank()
    vac = dict(primary_count=len(primary), independent_secondary_count=len(vac_sec),
               poisson_matrix=vac_omega.tolist(), poisson_rank=vac_rank,
               linear_first_class=len(vac_cs)-vac_rank,
               matter_velocity_hessian=s.diff(L, ud, 2).subs(vac_sub),
               limitation="Additional linear null direction is not a nonlinear gauge-symmetry proof")
    return dict(hamiltonian=Hamiltonian, primary=primary, secondary=secondary,
                poisson_matrix=Omega.tolist(), poisson_determinant=determinant,
                poisson_rank=rank, first_class=count_first, second_class=rank,
                scalar_sector_dof=s.Rational(2*len(coords)-2*count_first-rank, 2),
                preservation_residuals=remainder,
                vacuum_canonical_control=vac,
                preservation_scope="Ct_i includes actual explicit time derivatives; invertible multiplier matrix solves arbitrary Ct_i, so no tertiary constraint is hidden",
                vacuum_warning="q=0 not covered by nonzero determinant; constraint rank must be recalculated")


def derive_homogeneous():
    vol, M, N = s.symbols("vol M N", positive=True)
    phi, sigma = s.symbols("varphi sigma", real=True)
    vd, sd = s.symbols("vd sd", real=True)
    V = s.Function("V")(phi)
    W = V-phi**2/3
    gamma = 2*M**2/3
    L = gamma*phi*vd-N*M**2*vol*W+vol*sd**2/(2*N)
    pv, pp, ps, pn = momenta = list(s.symbols("pv pphi psigma pN", real=True))
    coords = [vol, phi, sigma, N]
    primary = [pv-s.diff(L, vd), pp, pn]
    Hc = s.simplify((pv*vd+ps*sd-L).subs(sd, N*ps/vol).subs(pv, gamma*phi))
    C = s.simplify(-pb(pn, Hc, coords, momenta))
    ua, ub, un = s.symbols("ua ub un")
    Ht = Hc+ua*primary[0]+ub*pp+un*pn
    preserving = [pb(c, Ht, coords, momenta) for c in primary[:2]]
    solution = s.solve(preserving, (ua, ub), dict=True)[0]
    Cdot = s.factor(pb(C, Ht, coords, momenta).subs(solution))
    cons = primary+[C]
    Omega = s.Matrix([[pb(c, b, coords, momenta) for b in cons] for c in cons])
    # Classify on C=0, on the regular v>0,M>0 stratum. Auxiliary primary
    # pair remains independent; retaining phi avoids dividing by V''-2/3.
    rank = Omega.rank()
    velocity_v = s.factor(solution[ua])
    velocity_phi = s.factor(solution[ub])
    # The exact massless stiff-fluid solution, V=0, unit lapse, v=t.
    t = s.symbols("t", positive=True)
    vsol, phisol, sigsol = t, -1/t, s.sqrt(s.Rational(2, 3))*M*s.log(t)
    rhosol, Hsol = M**2/(3*t**2), 1/(3*t)
    residuals = [s.simplify(phisol**2-3*rhosol/M**2),
                 s.simplify(s.diff(phisol, t)-3*rhosol/M**2),
                 s.simplify(3*Hsol+phisol),
                 s.simplify(s.diff(vsol*s.diff(sigsol, t), t))]
    Hd, rho0 = s.symbols("H_deSitter rho0", positive=True)
    phistar = s.symbols("varphi_star", real=True)
    rhod = rho0*s.exp(-6*Hd*t)
    phid = phistar-rhod/(2*M**2*Hd)
    Vd = phi**2/3+2*Hd*(phi-phistar)
    ds_residuals = [s.simplify(phid**2-3*Vd.subs(phi, phid)-3*rhod/M**2),
                    s.simplify(s.diff(phid, t)-3*rhod/M**2),
                    s.simplify(3*Hd+phid-s.Rational(3, 2)*s.diff(Vd, phi).subs(phi, phid)),
                    s.simplify(s.diff(rhod, t)+6*Hd*rhod)]
    return dict(L=L, canonical_H=Hc, primary=primary, secondary=[C],
                poisson_matrix=Omega.tolist(), poisson_rank=rank,
                bracket_antisymmetric=Omega == -Omega.T,
                first_class=len(cons)-rank, second_class=rank,
                homogeneous_dof=s.Rational(2*len(coords)-2*(len(cons)-rank)-rank, 2),
                volume_velocity=velocity_v, phi_velocity=velocity_phi,
                preservation_residuals=[s.simplify(e.subs(solution)) for e in preserving]+[Cdot],
                stiff_solution_residuals=residuals, stiff_H=Hsol,
                de_sitter_stiff_potential=Vd, de_sitter_stiff_residuals=ds_residuals,
                exceptional_stratum="rho=H=0: constraint differential may vanish; generic count not a vacuum certificate")


def radiation_evolution(d):
    """Evolve the same quadratic equations on an EXACT expanding solution.

    V=0, P=X^2, M=1, a=sqrt(t), q=1/sqrt(t), Z=1/t, D=3/t.
    This is a linear transfer experiment; solutions scale with the initial
    amplitude and are not claimed nonlinear after their growth becomes large.
    """
    import numpy as np
    from scipy.integrate import solve_ivp
    t = s.symbols("t", positive=True)
    bg = {d["a"]: s.sqrt(t), d["q"]: 1/s.sqrt(t), d["Z"]: 1/t,
          d["D"]: 3/t, d["M"]: 1}
    rho, phi, H = 3/(4*t**2), -3/(2*t), 1/(2*t)
    residuals = [s.simplify(phi**2-3*rho),
                 s.simplify(s.diff(phi, t)-s.Rational(3, 2)/t**2),
                 s.simplify(s.diff(rho, t)+4*H*rho)]
    kvalue = 30
    def evolution(alpha, rtol):
        K = s.factor(d["kinetic"].subs(bg).subs({d["alpha"]: alpha, d["k"]: kvalue}))
        B = s.factor(d["gradient_mass"].subs(bg).subs({d["alpha"]: alpha, d["k"]: kvalue}))
        damping = s.factor(s.diff(t**s.Rational(3, 2)*K, t)/(t**s.Rational(3, 2)*K))
        frequency = s.factor(B/K)
        dampfn, freqfn = s.lambdify(t, damping, "numpy"), s.lambdify(t, frequency, "numpy")
        def rhs(time, state):
            return [state[1], -float(dampfn(time))*state[1]-float(freqfn(time))*state[0]]
        sol = solve_ivp(rhs, (1.0, 4.0), [1.0, kvalue/3], method="DOP853",
                        rtol=rtol, atol=rtol*1e-3, t_eval=np.linspace(1, 4, 301))
        if not sol.success:
            raise RuntimeError(sol.message)
        return dict(final_u=float(sol.y[0, -1]), max_abs_u=float(np.max(np.abs(sol.y[0]))),
                    nfev=int(sol.nfev), damping=str(damping), omega2=str(frequency))
    mond, refined, control = evolution(1, 1e-9), evolution(1, 1e-11), evolution(0, 1e-11)
    return dict(background_residuals=residuals, k=kvalue, time_interval=[1, 4],
                samples=301, initial_state=[1, kvalue/3], mond=mond,
                mond_refined=refined, unmodified_control=control,
                mond_growth=refined["final_u"], control_max_abs_u=control["max_abs_u"],
                mond_relative_tolerance_change=abs(mond["final_u"]-refined["final_u"])/abs(refined["final_u"]),
                non_claim="Not observed galaxy data, not a nonlinear cosmology simulation, and no claim of evolution beyond linear validity")


def encode(obj):
    if isinstance(obj, dict):
        return {str(k): encode(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [encode(x) for x in obj]
    if isinstance(obj, s.Integer):
        return int(obj)
    if isinstance(obj, s.Basic):
        return str(obj)
    return obj


def run():
    d = derive_nonzero_mode()
    canonical = scalar_dirac(d)
    hom = derive_homogeneous()
    evolution = radiation_evolution(d)
    residuals = [d["boundary_residual"], d["background_tadpole_residual"],
                 *d["constraint_residuals"], *canonical["preservation_residuals"],
                 *hom["preservation_residuals"], *hom["stiff_solution_residuals"],
                 *hom["de_sitter_stiff_residuals"], *evolution["background_residuals"]]
    if any(s.simplify(x) != 0 for x in residuals):
        raise AssertionError("Variational or canonical consistency check failed")
    fixtures = []
    for name, zv, dv in (("canonical_scalar", 1, 1), ("radiation_P_equals_X_squared_at_q1", 1, 3)):
        # Same a,M,q,k for transparent dimensionless arithmetic, not a fit.
        subs = {d["a"]: 1, d["M"]: 1, d["q"]: 1, d["k"]: 100,
                d["Z"]: zv, d["D"]: dv, d["alpha"]: 1}
        fixtures.append(dict(name=name, kinetic=s.factor(d["kinetic"].subs(subs)),
                             frozen_omega2=s.factor(d["omega2"].subs(subs)),
                             UV_speed2=d["mond_UV_speed2"].subs(subs)))
    accepted = all(row["kinetic"] > 0 and row["frozen_omega2"] >= 0 for row in fixtures)
    return encode(dict(status="FLRW_MATTER_GATE_PASSED" if accepted else "VCDM_EXPONENTIAL_FLRW_MATTER_GATE_FAILED",
                       acceptance=bool(accepted), nonzero_mode=d, scalar_dirac=canonical,
                       homogeneous=hom, fixtures=fixtures, radiation_evolution=evolution,
                       scope="Exact quadratic action about expanding flat FLRW with healthy timelike P(X) matter; no universal all-gravity no-go or full nonlinear Dirac certificate"))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path)
    ap.add_argument("--require-healthy-flrw", action="store_true")
    args = ap.parse_args()
    result = run()
    if args.output:
        with args.output.open("x") as stream:
            json.dump(result, stream, indent=2, sort_keys=True)
            stream.write("\n")
    print(result["status"])
    print("MOND kinetic:", result["nonzero_mode"]["mond_kinetic"])
    print("MOND UV speed squared:", result["nonzero_mode"]["mond_UV_speed2"])
    print("Scalar-sector bracket rank:", result["scalar_dirac"]["poisson_rank"])
    print("Homogeneous bracket rank:", result["homogeneous"]["poisson_rank"])
    print("Fixtures:", json.dumps(result["fixtures"]))
    print("Expanding radiation linear growth:", result["radiation_evolution"]["mond_growth"])
    print("Unmodified control max |u|:", result["radiation_evolution"]["control_max_abs_u"])
    raise SystemExit(2 if args.require_healthy_flrw and not result["acceptance"] else 0)


if __name__ == "__main__":
    main()
