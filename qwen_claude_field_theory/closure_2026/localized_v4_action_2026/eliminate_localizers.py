"""Eliminate the flat Fourier localizers by their own equations."""
import sympy as sp


def eliminate_localizers():
    k2 = sp.symbols("k2", positive=True)
    S, A1, A2, R1, R2 = sp.symbols("S A1 A2 R1 R2", real=True)
    chi, Abar1, Abar2, Q1, Q2 = sp.symbols(
        "chi Abar1 Abar2 Q1 Q2", real=True
    )

    # Delta=-k^2 on the flat leaf.  The scalar localizer is written with
    # signs fixed by varying its local action, not by inserting Delta^-1 S.
    L_scalar = -2*chi*S + k2*chi**2
    chi_eq = sp.diff(L_scalar, chi)
    chi_sol = sp.solve(chi_eq, chi)[0]
    scalar_on_shell = sp.factor(L_scalar.subs(chi, chi_sol))
    scalar_target = sp.factor(-S**2/k2)

    # Hodge one-form block, restricted to two transverse components.
    L_vector = (2*Abar1*A1 - k2*Abar1**2
                + 2*Abar2*A2 - k2*Abar2**2)
    vector_eq = [sp.diff(L_vector, Abar1), sp.diff(L_vector, Abar2)]
    vector_sol = sp.solve(vector_eq, [Abar1, Abar2], dict=True)[0]
    vector_on_shell = sp.factor(L_vector.subs(vector_sol))
    vector_target = sp.factor((A1**2 + A2**2)/k2)

    # York-TT block has the opposite sign because V3 contains
    # -R_TT H_TT^dagger R_TT.
    L_tt = (-2*Q1*R1 + k2*Q1**2
            -2*Q2*R2 + k2*Q2**2)
    tt_eq = [sp.diff(L_tt, Q1), sp.diff(L_tt, Q2)]
    tt_sol = sp.solve(tt_eq, [Q1, Q2], dict=True)[0]
    tt_on_shell = sp.factor(L_tt.subs(tt_sol))
    tt_target = sp.factor(-(R1**2 + R2**2)/k2)

    return {
        "scalar_equation": str(chi_eq),
        "scalar_solution": str(chi_sol),
        "scalar_on_shell": str(scalar_on_shell),
        "scalar_target": str(scalar_target),
        "scalar_identity": sp.simplify(scalar_on_shell-scalar_target) == 0,
        "vector_equations": [str(x) for x in vector_eq],
        "vector_solution": {str(k): str(v) for k, v in vector_sol.items()},
        "vector_on_shell": str(vector_on_shell),
        "vector_target": str(vector_target),
        "vector_identity": sp.simplify(vector_on_shell-vector_target) == 0,
        "tt_equations": [str(x) for x in tt_eq],
        "tt_solution": {str(k): str(v) for k, v in tt_sol.items()},
        "tt_on_shell": str(tt_on_shell),
        "tt_target": str(tt_target),
        "tt_identity": sp.simplify(tt_on_shell-tt_target) == 0,
        "scope": "flat nonzero Fourier mode; kernel modes excluded explicitly",
    }
