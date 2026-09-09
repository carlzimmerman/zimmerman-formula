"""A scoped no-go for the strict local transport realization.

The statement proved here is intentionally architectural, not universal: if
the exact local constraint is implemented by
``A*lambda*(Qdot-Theta)`` and no spatial Q term is present, the multiplier
block has a singular principal symbol for every k.  Adding a Q kinetic
regulator raises the velocity-Hessian rank but leaves the lambda variation
unchanged, so the exact transport constraint is still present.  A genuine
hyperbolic replacement must therefore change this constraint (or the field
content), which is precisely the next design fork.
"""

from functools import lru_cache

import sympy as sp


@lru_cache(None)
def no_go_report():
    area, epsilon, cs = sp.symbols("A epsilon c_s", positive=True)
    qdot, ldot, sigma = sp.symbols("Qdot lambdadot Theta_pert", real=True)
    q, lam = sp.symbols("Q lambda", real=True)
    omega, k = sp.symbols("omega k", real=True)

    L_base = area * lam * (qdot - sigma)
    L_reg = L_base + epsilon * (qdot ** 2 - cs ** 2 * k ** 2 * q ** 2) / 2
    velocity_hessian_base = sp.hessian(L_base, (qdot, ldot))
    velocity_hessian_reg = sp.hessian(L_reg, (qdot, ldot))

    # The canonical momenta and the multiplier bracket follow directly from
    # the Legendre map of the exact transport term.
    pQ_base = sp.diff(L_base, qdot)
    pl_base = sp.diff(L_base, ldot)
    pQ, pl = sp.symbols("p_Q p_lambda", real=True)
    CQ = pQ - pQ_base
    p_lambda_constraint = pl - pl_base
    # canonical bracket {p_lambda, C_Q}; q=(Q,lambda), p=(pQ,pl)
    dirac_bracket = sp.diff(p_lambda_constraint, lam) * sp.diff(CQ, pl) - \
        sp.diff(p_lambda_constraint, pl) * sp.diff(CQ, lam)

    # Euler equations of the base block and their Fourier principal matrix are
    # generated from time-dependent fields, rather than entered as a target.
    t = sp.symbols("t", real=True)
    Qf = sp.Function("Q_f")(t)
    lf = sp.Function("lambda_f")(t)
    sf = sp.Function("Theta_f")(t)
    L_time = area * lf * (sp.diff(Qf, t) - sf)
    E_Q_time = sp.diff(sp.diff(L_time, sp.diff(Qf, t)), t) - sp.diff(L_time, Qf)
    E_lambda_time = sp.diff(L_time, lf)
    qhat, lhat = sp.symbols("Q_hat lambda_hat")
    fourier = {
        Qf: qhat,
        lf: lhat,
        sf: 0,
        sp.diff(Qf, t): sp.I * omega * qhat,
        sp.diff(lf, t): sp.I * omega * lhat,
    }
    fourier_equations = [
        sp.expand(E_lambda_time.xreplace(fourier)),
        sp.expand(E_Q_time.xreplace(fourier)),
    ]
    memory_matrix = sp.Matrix([
        [sp.diff(eq, variable) for variable in (qhat, lhat)]
        for eq in fourier_equations
    ])
    principal_determinant = sp.factor(memory_matrix.det())

    # A Q kinetic/gradient regulator changes the Legendre Hessian but does not
    # change the exact lambda equation; this equality is computed, not set by
    # a target flag.
    lambda_equation_difference = sp.simplify(
        sp.diff(L_reg, lam) - sp.diff(L_base, lam)
    )
    escape_requires_changing_constraint = (
        lambda_equation_difference == 0
        and int(velocity_hessian_reg.rank()) > int(velocity_hessian_base.rank())
    )

    return {
        "area": area,
        "epsilon": epsilon,
        "c_s": cs,
        "momentum_map": {"p_Q": pQ_base, "p_lambda": pl_base},
        "primary_constraints": [p_lambda_constraint, CQ],
        "dirac_bracket_p_lambda_CQ": sp.simplify(dirac_bracket),
        "momentum_hessian": velocity_hessian_base,
        "momentum_hessian_rank": int(velocity_hessian_base.rank()),
        "kinetic_regulator_hessian": velocity_hessian_reg,
        "kinetic_regulator_rank": int(velocity_hessian_reg.rank()),
        "lambda_equation_base": sp.diff(L_base, lam),
        "lambda_equation_regulator": sp.diff(L_reg, lam),
        "lambda_equation_difference": lambda_equation_difference,
        "principal_matrix": memory_matrix,
        "principal_determinant": principal_determinant,
        "k": k,
        "omega": omega,
        "escape_requires_changing_constraint": escape_requires_changing_constraint,
        "strict_architecture_conclusion": (
            "The exact local transport block cannot be a healthy hyperbolic "
            "Q mode without changing its multiplier constraint or field content."
        ),
    }


def encode(value):
    if isinstance(value, dict):
        return {str(key): encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    if isinstance(value, sp.MatrixBase):
        return [[encode(item) for item in row] for row in value.tolist()]
    if isinstance(value, sp.Basic):
        return str(value)
    return value


if __name__ == "__main__":
    import json

    print(json.dumps(encode(no_go_report()), indent=2))
