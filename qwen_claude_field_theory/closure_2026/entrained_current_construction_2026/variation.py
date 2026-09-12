#!/usr/bin/env python3
"""Independent Hilbert variation and current Ward identity for the actual action."""
import json

import sympy as s

from current_action import CURRENT, master


def derive():
    n, m, cross = s.symbols("n m cross", positive=True)
    r = cross-n*m
    F = -n-m+r/16+(s.Rational(5, 2)-(n+m)**2/8-s.Rational(5, 3)*(n-m)**2)*r*r
    fn, fm, fs = [s.diff(F, x) for x in (n, m, cross)]
    pressure = s.expand(F-n*fn-m*fm-2*cross*fs)
    j1, j2 = s.Matrix(CURRENT[:4]), s.Matrix(CURRENT[4:])
    metric = s.diag(-1, 1, 1, 1)
    nval = s.sqrt(-(j1.T*metric*j1)[0])
    mval = s.sqrt(-(j2.T*metric*j2)[0])
    cval = -(j1.T*metric*j2)[0]
    subs = {n: nval, m: mval, cross: cval}
    actual = master()[0]
    assert s.simplify(F.subs(subs)-actual) == 0
    pi1 = -fn/n*(metric*j1)-fs*(metric*j2)
    pi2 = -fm/m*(metric*j2)-fs*(metric*j1)
    for a, pi in enumerate((pi1, pi2)):
        for mu in range(4):
            assert s.simplify(pi[mu].subs(subs)-s.diff(actual, CURRENT[4*a+mu])) == 0
    # Metric first variation about an inertial frame, independent of the
    # current derivative construction. Contravariant currents are held fixed.
    # Use invariant chain derivatives; this audits all ten symmetric variations.
    eps = s.Symbol("eps", real=True)
    residuals = []
    for a in range(4):
        for b in range(a, 4):
            perturb = s.zeros(4)
            perturb[a, b] = perturb[b, a] = 1
            # δg_cov = -g_cov δg_inv g_cov. No finite inverse is needed.
            dg = -metric*perturb*metric
            dn = -(j1.T*dg*j1)[0]/(2*n)
            dm = -(j2.T*dg*j2)[0]/(2*m)
            dc = -(j1.T*dg*j2)[0]
            # On shell J·∂theta + F = pressure, including volume variation.
            varied = -pressure*s.trace(metric*perturb)/2+fn*dn+fm*dm+fs*dc
            stress_from_variation = -2*varied/(1 if a == b else 2)
            stress_from_currents = (pressure*metric[a, b]
                                    +(metric*j1)[a]*pi1[b]+(metric*j2)[a]*pi2[b])
            residuals.append(s.simplify(stress_from_variation-stress_from_currents))
    assert residuals == [0]*10
    # Covariant product-rule identity, in a local inertial frame:
    # ∇μT^μν = Σ πν ∇μJμ + Σ Jμ(∇μπν-∇νπμ).
    # EL equations give current conservation and π=-dtheta, so both vanish.
    derivative = s.Matrix(4, 4, lambda i, j: s.Symbol(f"pi_deriv_{min(i,j)}_{max(i,j)}"))
    ward = [sum(j1[mu]*(derivative[mu, nu]-derivative[nu, mu]) for mu in range(4))
            for nu in range(4)]
    assert ward == [0]*4
    return {"master_invariants": str(F), "generalized_pressure": str(pressure),
            "momentum1": list(map(str, pi1)), "momentum2": list(map(str, pi2)),
            "ten_hilbert_variation_residuals": list(map(str, residuals)),
            "ward_on_conserved_irrotational_currents": list(map(str, ward)),
            "EL": ["nabla_mu J_A^mu=0", "partial_mu theta_A + partial F/partial J_A^mu=0"],
            "scope": "exact current-sector variational identities; ordinary matter conservation follows separately from minimally coupled S_m; no halo/CMB inference"}


if __name__ == "__main__":
    print(json.dumps(derive(), indent=2))
