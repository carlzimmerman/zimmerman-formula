"""Reproducible aggregate; computation success is not theory closure.

Each module retains its own action/domain. The three adaptive perturbation
calculations are matched explicitly before their results are combined.
No output gravitational count or PPN value is filled with an expected value.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path

import sympy as s
import adaptive_endpoint
import causal_response
import legacy_constraint_audit
import spatial_kernel_gate
import trace_hamiltonian


@lru_cache(None)
def same_action_checks():
    d=spatial_kernel_gate.derive()
    e=adaptive_endpoint.derive()
    c=causal_response.derive_adaptive_action()
    dictionary={e[key]:d[key] for key in ('a','k','q','u','ud','n','z')}
    raw=spatial_kernel_gate.vcdm_flrw.derive_nonzero_mode()
    dictionary.update({e['m']:d['M']**2,e['v']:raw['auxiliaries'][2],e['Q']:d['Q']})
    canonical=d['L'].subs({d['Z']:1,d['D']:1})
    endpoint=s.factor(e['L'].subs(dictionary,simultaneous=True)-canonical)
    b=d['adaptive_family']['b']
    cdictionary={c[key]:d[key] for key in ('a','k','q','u','ud','n','z')}
    cdictionary.update({c['m']:d['M']**2,c['v']:raw['auxiliaries'][2],c['b']:b,
                       c['rho']:0,c['p']:0,c['J']:0})
    causal=s.factor(c['L'].subs(cdictionary,simultaneous=True)
                    -canonical.subs(d['Q'],-b*d['q']**2))
    chosen=e['candidate_beta']
    kinetic=s.factor(c['kinetic'].subs(c['b'],chosen)
                      -e['kinetic'].subs(e['beta'],chosen))
    return dict(endpoint_residual=endpoint,causal_zero_source_residual=causal,
                selected_causal_kinetic_residual=kinetic)


@lru_cache(None)
def run():
    residuals=same_action_checks()
    endpoint=adaptive_endpoint.run()
    response=causal_response.run()
    spatial=spatial_kernel_gate.run()
    trace=trace_hamiltonian.run()
    legacy=legacy_constraint_audit.run()
    checked=all(s.simplify(x)==0 for x in residuals.values()) and all([
        endpoint['algebra_checks_passed'],response['checks_passed'],
        response['adaptive_response']['checks_passed'],spatial['algebra_checks_passed'],
        trace['algebra_checks_passed'],legacy['algebra_checks_passed']])
    if not checked:
        raise AssertionError('Action matching or independently derived checks failed')
    chosen=adaptive_endpoint.derive()['candidate_beta']
    kin=adaptive_endpoint.derive()['kinetic'].subs(adaptive_endpoint.derive()['beta'],chosen)
    missing=['Full nonlinear functional Dirac closure on generic backgrounds',
        'Exact causal-response extension from Lambda=0 stiff member to fixed positive Lambda and its prescribed tau_Lambda(T)',
        'Physical healthy-matter realization or exclusion of the conserved-probe witness',
        'Controlled full k=0 and q=0/y=0 limits',
        'Same-action nonlinear galactic solutions and measured Newton constant',
        'Full PPN beta, gamma, alpha_1, alpha_2, alpha_3',
        'Vector/tensor/scalar nonlinear stability and strong coupling',
        'Observationally viable cosmology; no new empirical fit is performed']
    closure=(response['adaptive_response']['causal_response_gate']=='PASS' and not missing)
    return spatial_kernel_gate.encode(dict(checks_passed=checked,
        full_theory_status='CLOSED' if closure else 'OPEN',closure_passed=closure,
        selected_b=chosen,selected_kinetic=kin,same_action_residuals=residuals,
        action_matching_scope='Identical quadratic kinetic/kernel architecture. Endpoint uses positive Lambda with tau=-3m Hd coth(3Hd T); exact causal witness uses Lambda=0,tau=-m/T. No fixed-positive-Lambda causal exclusion is inferred.',
        spatial_kernel=spatial,endpoint=endpoint,causal_response=response,
        trace_hamiltonian=trace,legacy_audit=legacy,missing_certificates=missing,
        novelty='No literature-wide novelty certificate is claimed',
        interpretation='Selected adaptive kernel passes the displayed matter and positive-Lambda curvature screens; its Lambda=0 stiff member fails the conserved-external-probe causal-response gate.'))


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path)
    ap.add_argument('--require-closure',action='store_true')
    args=ap.parse_args(argv)
    result=run()
    if args.output:
        with args.output.open('x') as stream:
            json.dump(result,stream,indent=2,sort_keys=True,allow_nan=False)
            stream.write('\n')
    print('Same-action checks:',result['same_action_residuals'])
    print('Derived curvature selection b:',result['selected_b'])
    print('Derived canonical kinetic:',result['selected_kinetic'])
    print('Conserved-probe causal response:',result['causal_response']['adaptive_response']['causal_response_gate'])
    print('Full theory:',result['full_theory_status'])
    return 2 if args.require_closure and not result['closure_passed'] else 0


if __name__=='__main__':
    raise SystemExit(main())
