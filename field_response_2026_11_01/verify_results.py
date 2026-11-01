#!/usr/bin/env python3
"""Final finite-result consistency and exact admissibility-bound checks."""
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE=Path(__file__).resolve().parent


def read(path):return json.loads((HERE/path).read_text())


def main():
    result={'assertion_tested':'Stored finite-result consistency and exact rational Legendre bounds for all six canonical spatial maps.','checks':{},'map_bounds':[]}
    checks=result['checks']
    radial=read('radial_run_003/result.json');kinetic=read('kinetic_run_002/result.json')
    canonical=read('canonical_energy_run_001/result.json')
    dilute=read('dilute_stability_run_001/result.json');end=read('endpoint_stability_run_001/result.json')
    checks['radial_six_adverse']=len(radial['cases'])==6 and radial['all_controls_pass'] and all(c['refined_scaled_margin'] < -1e-5 for c in radial['cases'])
    checks['kinetic_six_adverse']=len(kinetic['cases'])==6 and kinetic['all_controls_pass'] and all(c['evaluations'][-1]['nested'][-1]['scaled_margin'] < -1e-5 for c in kinetic['cases'])
    checks['finite_energy_six_verified']=len(canonical['cases'])==6 and canonical['all_controls_pass']
    for c in canonical['cases']:
        coeff=[Fraction.from_float(abs(v)) for v in c['vector']]
        B=sum(coeff);A=sum(v*(1+2*j*(j+1)) for j,v in enumerate(coeff))
        R=Fraction.from_float(c['radius']);L=Fraction.from_float(c['outer'])
        for s in c['evaluations'][-1]['steps']:
            h=Fraction.from_float(abs(s['h']))
            row={'psi_c':c['psi_c'],'epsilon':c['epsilon'],'h':s['h'],
                 'radial_stretch_global_lower_bound':float(1-h*A),
                 'tangential_stretch_global_lower_bound':float(1-h*B),
                 'deformed_edge_global_upper_bound':float(R*(1+h*B)),
                 'outer_radius':float(L),
                 'exact_rational_inequalities_pass':bool(h*A<1 and h*B<1 and R*(1+h*B)<L),
                 'both_energy_differences_negative':s['delta_energy_plus']<0 and s['delta_energy_minus']<0}
            result['map_bounds'].append(row)
    checks['global_map_admissibility']=all(r['exact_rational_inequalities_pass'] for r in result['map_bounds'])
    checks['both_sign_finite_energy_decrease']=all(r['both_energy_differences_negative'] for r in result['map_bounds'])
    checks['dilute_three_positive_screens']=len(dilute['cases'])==3 and dilute['all_controls_pass'] and all(c['fluid']['refined_lowest_omega2_ritz']>0 and c['kinetic']['evaluations'][-1]['nested'][-1]['minimum_rayleigh']>0 for c in dilute['cases'])
    checks['endpoint_three_positive_screens']=len(end['cases'])==3 and end['all_controls_pass'] and all(min(c['evaluations'][-1]['fluid_minimum_rayleigh'],c['evaluations'][-1]['kinetic_minimum_rayleigh'])>0 for c in end['cases'])
    for name,expected in [('static_run_002',(60,24,9,27)),('static_refinement_run_001',(492,163,9,320)),('static_dilute_run_001',(246,173,3,70))]:
        data=read(name+'/result.json');rows=data['cases']
        passes=sum(bool(x.get('passed')) for x in rows)
        skipped=sum(bool(x.get('not_attempted')) for x in rows)
        failed=len(rows)-passes-skipped
        actual=(len(rows),passes,failed,skipped)
        checks[name+'_coverage']=actual==expected
        result[name+'_counts']={'actual':actual,'expected':expected}
    result['all_checks_pass']=all(checks.values())
    target=Path(sys.argv[1]);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'all_checks_pass':result['all_checks_pass'],'checks':checks},indent=2))
    return 0 if result['all_checks_pass'] else 1


if __name__=='__main__':sys.exit(main())
