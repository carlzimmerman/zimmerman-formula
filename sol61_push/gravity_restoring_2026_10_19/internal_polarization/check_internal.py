#!/usr/bin/env python3
"""Exact finite coefficient checks. The universal argument is in the note."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json


def cadd(z, w):
    return (z[0] + w[0], z[1] + w[1])


def cscale(a, z):
    return (a * z[0], a * z[1])


def cmul(z, w):
    return (z[0]*w[0] - z[1]*w[1], z[0]*w[1] + z[1]*w[0])


def norm(z):
    return z[0]**2 + z[1]**2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    masses = [F(1, 3), F(1), F(3, 2), F(2), F(5, 2), F(7)]
    charges = [F(1), F(2), F(3), F(5)]
    slopes = [F(-2), F(0), F(1, 3)]
    forces = [F(-3, 4), F(1, 2)]
    count = 0
    unequal_examples = []
    for m1, m2, q1, q2, slope, force in product(
            masses, masses, charges, charges, slopes, forces):
        total = m1 + m2
        qsum = q1 + q2
        delta = (m1*q2 - m2*q1) / qsum
        aq = (m1*q2*q2 + m2*q1*q1) / (qsum*qsum)
        reduced = m1*m2 / total
        det = total*aq - delta*delta
        assert det == m1*m2
        assert aq - delta*delta/total == reduced
        rhs_center = -total*slope
        rhs_relative = -force - delta*slope
        # Solve the two coupled equations in the reference-center variables.
        rdd = (total*rhs_relative - delta*rhs_center) / det
        centerdd = (aq*rhs_center - delta*rhs_relative) / det
        assert rdd == -force/reduced
        physical_centerdd = centerdd + delta*rdd/total
        assert physical_centerdd == -slope
        # A separate direct relative-acceleration calculation is the benchmark.
        assert rdd == (-slope-force/m1) - (-slope+force/m2)
        count += 1
        if delta and slope and len(unequal_examples) < 2:
            unequal_examples.append({
                "m1": str(m1), "m2": str(m2),
                "q1": str(q1), "q2": str(q2),
                "apparent_dipole_coefficient": str(delta),
                "uniform_field_relative_acceleration": "0",
                "reference_center_is_free": True,
            })

    # Exact original potential check with rational complex fields. This is
    # arithmetic over Q(i); no binary floating point or symbolic solver.
    fields = [(F(0), F(0)), (F(1), F(0)), (F(1, 2), F(2, 3)),
              (F(-3, 4), F(1, 5))]
    couplings = [F(-2), F(0), F(3, 5)]
    square_checks = 0
    for mass, ratio, gs, lam, phi, source in product(
            [F(1), F(3, 2)], [F(5, 2), F(3)], couplings,
            [F(1, 7), F(2)], fields, fields):
        source_mass = ratio*mass
        delta = source_mass**2 - 4*mass**2
        lambda_total = lam + gs*gs/delta
        phi2 = cmul(phi, phi)
        # Re(conj(X)*Phi^2) is X_real*Re(Phi^2)+X_imag*Im(Phi^2).
        conv = 2*gs*(source[0]*phi2[0] + source[1]*phi2[1])
        original = (mass*mass*norm(phi) + source_mass**2*norm(source)
                    + conv + lambda_total*norm(phi)**2)
        positive = (mass*mass*(norm(phi)+4*norm(source))
                    + delta*norm(cadd(source, cscale(gs/delta, phi2)))
                    + lam*norm(phi)**2)
        assert original == positive
        assert positive >= mass*mass*(norm(phi)+4*norm(source))
        square_checks += 1

    # Distinguish the nonminimal-ratio loophole from unequal bare masses.
    loophole_checks = 0
    for m1, m2, eta1, eta2 in product(
            masses, masses, [F(1), F(2)], [F(1), F(3)]):
        mu = m1*m2/(m1+m2)
        gamma1, gamma2 = m1*eta1, m2*eta2
        dg = (gamma1*m2-gamma2*m1)/(m1+m2)
        assert dg == mu*(eta1-eta2)
        assert (dg == 0) == (eta1 == eta2)
        loophole_checks += 1

    residual_checks = 0
    for a0, kval, fraction in product(
            [F(1), F(3, 2)], [F(1, 3), F(2)],
            [F(1, 10), F(1, 2), F(9, 10)]):
        u = a0*fraction
        derivative_full = a0*u/(a0-u)
        residual = derivative_full-u
        assert residual == u*u/(a0-u)
        # The exact second derivative with respect to |P| is positive.
        second = kval*a0*a0/(a0-u)**2
        assert second > 0
        residual_checks += 1

    result = {
        "status": "passed",
        "arithmetic": "exact rational numbers; rational complex pair arithmetic",
        "reference_center_cases": count,
        "reference_center_assertions_per_case": 5,
        "potential_square_cases": square_checks,
        "nonuniversal_ratio_cases": loophole_checks,
        "target_residual_cases": residual_checks,
        "unequal_center_examples": unequal_examples,
        "coverage": {
            "masses": [str(x) for x in masses],
            "reference_weights": [str(x) for x in charges],
            "uniform_slopes": [str(x) for x in slopes],
            "internal_forces": [str(x) for x in forces],
            "randomness": False,
        },
        "non_claims": [
            "Finite checks do not establish universal COM separation; the note proves it.",
            "No bound object, droplet, continuum phase or target W is numerically constructed.",
            "No relativistic strong-self-gravity or quantum-field theorem is tested.",
        ],
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items()
                      if k.endswith("cases") or k == "status"}))


if __name__ == "__main__":
    main()
