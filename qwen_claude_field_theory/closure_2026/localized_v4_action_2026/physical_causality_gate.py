"""Physical-response causality test for the localized V4 MOND branch.

The previous causal gate checked algebraic source poles.  This gate asks the
different question required by the target: does the elliptic MOND potential
enter a local observable?  Linearising the *action-derived* exponential AQUAL
equation around a uniform external field gives the anisotropic elliptic
symbol.  A nonzero equal-time transfer from a distant density perturbation to
the local external field, combined with the nonzero exponential EFE response,
is an instantaneous physical channel.  GR's constant-mu control has zero EFE
derivative, so the argument does not condemn an ordinary elliptic lapse.

This is a bounded linear-response obstruction, not a nonlinear Cauchy theorem.
"""
import json

import sympy as sp


def physical_causality_gate():
    y, a0, G, rho_k = sp.symbols("y a0 G rho_k", positive=True)
    kx, ky, kz = sp.symbols("k_x k_y k_z", real=True)
    k = sp.Matrix([kx, ky, kz])
    mu = 1 - sp.exp(-y)
    lam_perp = sp.simplify(mu)
    lam_parallel = sp.simplify(mu + y * sp.exp(-y))
    M = sp.diag(lam_parallel, lam_perp, lam_perp)
    denom = sp.factor((k.T * M * k)[0])
    delta_phi = sp.factor(-4 * sp.pi * G * rho_k / denom)
    delta_g = sp.Matrix([sp.I * component * delta_phi
                         for component in (kx, ky, kz)])

    # A local EFE observable can be taken as the internal response factor
    # O=1/mu(g_ext/a0).  It is local and gauge-invariant in the MOND branch.
    observable = sp.factor(1 / mu)
    d_observable_dgext = sp.factor(sp.diff(observable, y) / a0)
    transfer_component = sp.factor(sp.diff(delta_g[0], rho_k))
    chain_response = sp.factor(d_observable_dgext * transfer_component)

    y_witness = sp.Integer(1)
    k_witness = {kx: 1, ky: 2, kz: 3}
    witness = {
        "mu": sp.simplify(mu.subs(y, y_witness)),
        "lambda_perp": sp.simplify(lam_perp.subs(y, y_witness)),
        "lambda_parallel": sp.simplify(lam_parallel.subs(y, y_witness)),
        "denominator": sp.simplify(denom.subs({**k_witness, y: y_witness})),
        "transfer_dg_parallel_drho": sp.simplify(
            transfer_component.subs({**k_witness, y: y_witness})
        ),
        "d_observable_dgext": sp.simplify(
            d_observable_dgext.subs(y, y_witness)
        ),
        "chain_response": sp.simplify(
            chain_response.subs({**k_witness, y: y_witness})
        ),
    }

    # The exact zero-field point is separate: transverse ellipticity tends to
    # zero, while the witness y=1 is regular.  Do not silently continue the
    # finite-y result through y=0.
    zero_limits = {
        "lambda_perp": sp.limit(lam_perp, y, 0, dir="+"),
        "lambda_parallel": sp.limit(lam_parallel, y, 0, dir="+"),
        "d_observable_dgext": sp.limit(d_observable_dgext, y, 0, dir="+"),
        "newtonian_d_observable_dgext": sp.limit(d_observable_dgext, y, sp.oo),
    }

    # GR control: mu=1 has no external-field dependence, even if a chosen
    # foliation uses an elliptic lapse constraint.
    gr_observable = sp.Integer(1)
    gr_efe_derivative = sp.diff(gr_observable, y)

    checks = {
        "exponential_constitutive_symbol_derived": sp.simplify(
            lam_perp - (1 - sp.exp(-y))
        ) == 0 and sp.simplify(
            lam_parallel - (1 + (y - 1) * sp.exp(-y))
        ) == 0,
        "witness_symbol_positive": witness["lambda_perp"] > 0
        and witness["lambda_parallel"] > 0,
        "equal_time_transfer_nonzero": witness["transfer_dg_parallel_drho"] != 0,
        "efe_response_nonzero": witness["d_observable_dgext"] != 0,
        "composed_physical_response_nonzero": witness["chain_response"] != 0,
        "no_frequency_in_elliptic_transfer": sp.Symbol("omega") not in
        sp.sympify(delta_phi).free_symbols,
        "zero_field_transverse_rank_loss_explicit": zero_limits["lambda_perp"] == 0,
        "newtonian_efe_suppression_explicit": zero_limits["newtonian_d_observable_dgext"] == 0,
        "gr_control_no_efe": gr_efe_derivative == 0,
    }
    return {
        "status": "PHYSICAL_INSTANTANEOUS_CHANNEL_DETECTED; ELLIPTIC_ROUTE_FAILS_STRICT_CAUSAL_GATE",
        "constitutive_law": "mu(y)=1-exp(-y)",
        "linearised_symbol": {
            "lambda_perp": str(lam_perp),
            "lambda_parallel": str(lam_parallel),
            "denominator": str(denom),
            "delta_phi_k": str(delta_phi),
            "delta_g_k": [str(value) for value in delta_g],
        },
        "efe_observable": {
            "observable": str(observable),
            "d_observable_dgext": str(d_observable_dgext),
            "chain_response": str(chain_response),
        },
        "witness": {key: str(value) for key, value in witness.items()},
        "zero_and_newtonian_limits": {key: str(value) for key, value in zero_limits.items()},
        "gr_control": {"observable": str(gr_observable), "efe_derivative": str(gr_efe_derivative)},
        "checks": {key: bool(value) for key, value in checks.items()},
        "scope": [
            "linearized nonzero external-field branch y=1 and k=(1,2,3)",
            "single-metric physical potential identified with the action-derived Phi",
            "not a nonlinear global Cauchy proof; a preferred-foliation convention could reject the strict target instead",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(physical_causality_gate(), indent=2))
