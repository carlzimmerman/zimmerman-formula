"""Exact parameter-family gate for the repaired clock construction.

This is a symbolic follow-up to source_response_v2.py and
general_sources_v3.py.  It does not assume the V3 coefficients.  Starting
from the scalar quadratic action with free (d,t), it derives:

* the order-r^2 matching condition against the measured-G Newton reference;
* the compact isotropic-stress inverse-Laplacian residue;
* the two algebraic branches that remove that residue;
* the tensor and transverse-vector normalizations required by the same
  measured-G response.

The finite assertion is deliberately narrower than a full theory theorem:
it says whether this constant-coefficient linear response family has any
other parameter branch satisfying all three response gates.  It does not
vary the nonlinear York-TT projector or certify PPN/cosmology.
"""
import json
import sympy as s


def scalar_family():
    C, ell, d, t, k, r, F, src = s.symbols(
        "C ell d t k r F src", nonzero=True, real=True
    )
    alpha = 2 - C
    z, n, B, zd = s.symbols("z n B zd", real=True)
    # This is the independently varied scalar sector before the V2/V3
    # coefficient choice.  The source is the conserved isotropic seed
    # T00=Delta F, T0i=-dt di F, Tij=deltaij dtt F.
    L = (-6*t*zd**2 + 4*d*k**2*zd*B
         - ell*(3*zd-k**2*B)**2
         + k**2*(2*z**2-4*n*z+alpha*n**2))

    def solve_source(mult):
        source = -src*n + r*src*B + mult*r**2*src*z/k**2
        eq = [s.diff(L+source, n).subs(zd, r*z),
              s.diff(L+source, B).subs(zd, r*z),
              r*s.diff(L, zd).subs(zd, r*z) - s.diff(L+source, z)]
        sol = s.solve(eq, [z, n, B], dict=True)[0]
        X = s.factor(r**2*sol[z])
        Z = s.factor(-k**2*(sol[n]+r*sol[B]) + X)
        return X, Z

    X1, Z1 = solve_source(1)
    # The GR comparison used in the construction is independently solved
    # before taking the GR degeneracy limit.
    Lgr = L.subs({d: 1, t: 1, ell: 0, C: 2})
    srcgr = -2*src*n/C + 2*r**2*src*z/(C*k**2)
    eqgr = [s.diff(Lgr+srcgr, n).subs({zd: r*z, B: 0}),
            (r*s.diff(Lgr, zd).subs(zd, r*z)
             - s.diff(Lgr+srcgr, z)).subs(B, 0)]
    solgr = s.solve(eqgr, [n, z], dict=True)[0]
    Zgr = s.factor((-k**2*n+r**2*z).subs(solgr))

    # First gate: match the order-r^2 longitudinal curvature response.
    mismatch = s.factor(s.limit((Z1.subs(alpha, 2-C)-Zgr)/r**2, r, 0))
    tmatch = s.factor(s.solve(s.together(mismatch), t)[0])

    # Second gate: use the independent isotropic stress (mult=3), and
    # measure the inverse-Laplacian residue lim_{k->0}(Z-X).  The source
    # substitution is made after the limit so no desired cancellation is
    # inserted by hand.
    X3, Z3 = solve_source(3)
    X3 = s.factor(X3.subs({t: tmatch, src: -k**2*F}))
    Z3 = s.factor(Z3.subs({t: tmatch, src: -k**2*F}))
    residue = s.factor(s.limit(Z3-X3, k, 0))
    residue_num = s.factor(s.together(residue).as_numer_denom()[0])
    branches = s.solve(s.Eq(residue_num, 0), d)
    branch_data = []
    for root in branches:
        branch_data.append({
            "d": s.factor(root),
            "t": s.factor(tmatch.subs(d, root)),
            "residue": s.factor(residue.subs(d, root)),
        })

    # For each branch, derive the scalar kinetic Hessian and wave symbol.
    branch_health = []
    for row in branch_data:
        tb = row["t"]
        db = row["d"]
        Lb = s.factor(L.subs({t: tb, d: db}))
        aux = s.solve([s.diff(Lb, n), s.diff(Lb, B)], [n, B], dict=True)
        # Generic symbolic elimination can have a removable singularity;
        # retain the branch result rather than treating that as a failure.
        reduced = s.factor(Lb.subs(aux[0])) if aux else None
        hess = s.factor(s.diff(reduced, zd, 2)) if reduced is not None else None
        c2 = (s.factor(-s.diff(reduced, z, 2)/(k**2*hess))
              if reduced is not None else None)
        branch_health.append({"d": str(db), "t": str(tb),
                              "reduced": str(reduced),
                              "kinetic_hessian": str(hess),
                              "clock_speed_squared": str(c2)})

    # The two remaining polarizations are independent response gates.  Vary
    # their quadratic Fourier actions and solve their normalization directly
    # against the measured-G Einstein response (G_N=2G_b/C).
    tau, q, hdot, h, S, j = s.symbols("tau q hdot h S j", nonzero=True)
    K = s.symbols("K", positive=True)
    tensor = tau*(hdot**2-K*h**2)/2 + s.symbols("stress")*h
    tensor_sol = s.solve(
        s.diff(tensor, h).subs(hdot, r*h)
        - r*s.diff(tensor, hdot).subs(hdot, r*h), h
    )
    # The equation above is written as E-L=0; solve returns h=stress/(tau(...)).
    tensor_required = s.solve(s.Eq(
        s.simplify(tensor_sol[0] / s.symbols("stress")),
        1/(s.symbols("tau")*(r**2+K))
    ), tau) if tensor_sol else []
    # Recompute the normalization equation without relying on a symbolic
    # placeholder collision.
    stress = s.symbols("stress")
    hsol = stress/(tau*(r**2+K))
    E_tau = -r**2*hsol/2
    E_GR = -r**2*stress/(C*(r**2+K))
    tau_roots = s.solve(s.Eq(E_tau, E_GR), tau)

    vector = q*K*S**2/2 + j*S
    Ssol = s.solve(s.diff(vector, S), S)[0]
    # The Einstein transverse response has the same measured-G factor as the
    # tensor response.  Its source normalization is fixed by q*K*S+jS.
    vector_response = s.factor(Ssol/j)
    vector_target = s.factor(-2/(C*K))
    q_roots = s.solve(s.Eq(vector_response, vector_target), q)

    # Independent six-polarization check.  This is the same conserved seed
    # basis used by general_sources_v3.py, but the scalar d,t branch is not
    # inserted until after solving the equations.  Thus the second residue
    # branch gets a genuine chance to survive the full electric-curvature
    # response gate.
    x, zz = s.symbols("kx kz", real=True)
    KK = x*x + zz*zz
    kv = s.Matrix([x, 0, zz])
    I = s.eye(3)
    P = I - kv*kv.T/KK
    modes = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]
    full_branch_gate = []
    witness_sub = {C: s.Rational(5, 3), ell: s.Rational(1, 100)}
    for row in branch_data:
        db, tb = row["d"], row["t"]
        Lb = L.subs({d: db, t: tb})
        psi, nn, BB = s.symbols("psi nn BB")
        # Re-use the same variable names structurally, but solve each source
        # with a fresh set to avoid accidental substitutions from the prior
        # scalar isotropic calculation.
        scalar_rows = []
        spatial_poles = []
        factor_failures = []
        clock = (2*ell + (C-2)*(C+3*ell if s.simplify(db-C/2)==0
                               else C-3*ell)*r*r)
        # The expression above is written as 2ell + ... temporarily; replace
        # K below so the divisibility test remains polynomial in x,z,r.
        clock = 2*ell*KK + (2-C)*(C+3*ell if s.simplify(db-C/2)==0
                                  else C-3*ell)*r*r
        light = r*r + KK
        for ii, jj in modes:
            A = s.zeros(3)
            A[ii, jj] = 1
            A[jj, ii] = 1
            srcA = -(kv.T*A*kv)[0]
            trA = s.trace(A)
            z0, n0, b0 = s.symbols("z0 n0 b0")
            Lmode = Lb.subs({z: z0, n: n0, B: b0, zd: r*z0,
                             k**2: KK})
            source_original = -srcA*n + r*srcA*B - r*r*trA*z
            Smode = source_original.subs({z: z0, n: n0, B: b0})
            # Fourier Euler-Lagrange equation: take both derivatives before
            # substituting zd=r*z, exactly as in general_sources_v3.
            mode_subs = {z: z0, n: n0, B: b0, zd: r*z0, k**2: KK}
            momentum_mode = (r*s.diff(Lb, zd)
                             - s.diff(Lb+source_original, z)).subs(mode_subs)
            eqmode = [s.diff(Lmode+Smode, n0),
                      s.diff(Lmode+Smode, b0),
                      momentum_mode]
            solmode = s.solve(eqmode, [z0, n0, b0], dict=True)[0]
            ps = s.cancel(solmode[z0])
            nnv = s.cancel(solmode[n0])
            bsv = s.cancel(solmode[b0])
            ATT = P*A*P - P*s.trace(P*A)/2
            jT = P*A*kv
            E = (-kv*kv.T*(nnv+r*bsv) + r*r*ps*I
                 - r*r/(C*KK)*(kv*jT.T+jT*kv.T)
                 - r**4*ATT/(C*(r*r+KK)))
            for hh, mm in modes:
                entry = s.cancel(E[hh, mm])
                den = s.factor(s.denom(entry))
                # A surviving KK divisor is the instantaneous inverse-Δ
                # residue.  The stronger test checks the whole denominator
                # against the two candidate wave symbols.
                if s.rem(den, KK, x) == 0:
                    spatial_poles.append([ii, jj, hh, mm])
                # Coefficients C,ell are allowed in a symbolic divisor.  The
                # witness check below removes them and tests only the actual
                # Fourier variables, avoiding a false failure from a harmless
                # rational parameter prefactor.
                ratio_w = s.cancel((light*clock/den).subs(witness_sub))
                if s.denom(ratio_w).free_symbols & {x, zz, r}:
                    factor_failures.append([ii, jj, hh, mm, str(den)])
        full_branch_gate.append({
            "d": str(db), "t": str(tb),
            "spatial_pole_count": len(spatial_poles),
            "factor_failure_count": len(factor_failures),
            "spatial_poles": spatial_poles,
            "factor_failures": factor_failures,
        })

    # The two branches may share the same response, but the scalar kinetic
    # sign is a separate gate.  Report it symbolically, never hard-code rank
    # or a determinant.
    return {
        "status": "PARAMETER_FAMILY_GATE_COMPLETED; FULL_THEORY_OPEN",
        "order_r2_matching_condition_t": str(tmatch),
        "inverse_laplacian_residue": str(residue),
        "residue_numerator": str(residue_num),
        "residue_free_branches": branch_data,
        "branch_health": branch_health,
        "tensor_normalization_roots": [str(x) for x in tau_roots],
        "vector_response": str(vector_response),
        "vector_target": str(vector_target),
        "vector_normalization_roots": [str(x) for x in q_roots],
        "all_six_source_branches": full_branch_gate,
        "interpretation": [
            "The result is an exact symbolic gate for this constant-coefficient linear family.",
            "It does not prove that the nonlocal action has a healthy nonlinear Dirac closure.",
            "It does not derive full boosted PPN, FLRW perturbations, or an empirical fit.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(scalar_family(), indent=2, default=str))
