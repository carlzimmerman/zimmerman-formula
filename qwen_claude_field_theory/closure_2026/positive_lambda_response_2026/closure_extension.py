"""Collect same-action evidence; arithmetic success is not physical closure."""
import argparse
from functools import lru_cache
import json
from pathlib import Path

import constraint_hessian
import general_family
import infrared_domain
import localized_auxiliary
import physical_initial_data
import positive_lambda


@lru_cache(None)
def run():
    evidence = {
        'positive_lambda_external': positive_lambda.run(),
        'physical_cauchy': physical_initial_data.run(),
        'homogeneous_dirac': constraint_hessian.run(),
        'auxiliary_localization': localized_auxiliary.run(),
        'infrared_domain': infrared_domain.run(),
        'general_family': general_family.run(),
    }
    numerical = evidence['positive_lambda_external']['numerical_corroboration']
    numerical_ok = all(row['F'] > row['rigorous_F_lower_bound']
        and row['relative_refinement_change'] < 1e-8 for row in numerical)
    checked = all(part['checks_passed'] for part in evidence.values()) and numerical_ok
    # None denotes an absent derivation, never a failed numerical calculation.
    # Partial (homogeneous or auxiliary) ranks are deliberately not substituted.
    gates = {
        'positive_lambda_external_response': evidence['positive_lambda_external']['causal_response_gate'],
        'healthy_linear_cauchy_locality': evidence['general_family']['healthy_linear_cauchy_gate'],
        'unprojected_R3_nonlinear_action_domain': evidence['infrared_domain']['unprojected_R3_domain_gate'],
        'full_nonlinear_gravitational_count': None,
        'complete_PPN_and_measured_Newton_constant': None,
        'full_nonlinear_matter_and_clock_stability': None,
        'controlled_zero_field_and_exact_vacuum_limit': None,
        'nonlinear_causal_constraint_completion': None,
    }
    closed = checked and all(value == 'PASS' for value in gates.values())
    return dict(base_commit=positive_lambda.BASE, checks_passed=checked,
        numerical_corroboration_consistent=numerical_ok,
        evidence=evidence, full_theory_gates=gates, full_closure_proved=closed,
        goal_status='CLOSED' if closed else 'OPEN',
        interpretation='Every finite positive-kinetic subluminal canonical member of this positive-Lambda family, including b=3/16, has a linear Cauchy-locality obstruction. The unprojected R3 action also has a quartic infrared domain obstruction. Neither result is a universal MOND no-go or a nonlinear existence theorem.',
        same_action_scope='S0+DeltaS_b from c759c46; canonical P(X)=X, tau=-3m Hd coth(3Hd T). Physical Cauchy witness fixes b=3/16 (derived kinetic coefficient 9). The external-response family permits finite K>=1 with b=9/[2(K+15)], so it includes that same member; it does not donate PPN or DOF counts from a different model.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--require-closure', action='store_true')
    args = parser.parse_args(argv)
    result = run()
    serialized = json.dumps(result, indent=2, sort_keys=True, allow_nan=False)
    if args.output:
        with args.output.open('x') as stream:
            stream.write(serialized+'\n')
    print(serialized)
    if not result['checks_passed']:
        return 1
    return 2 if args.require_closure and not result['full_closure_proved'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
