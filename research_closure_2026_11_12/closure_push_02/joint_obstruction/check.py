"""Arithmetic certificate combining two separately audited necessary bounds."""
import json
import math
from pathlib import Path
import sys

def main(output):
    base=Path(__file__).resolve().parents[1]
    background=json.loads((base/'growth_gate_audit/run_001/results.json').read_text())['BBN']['canonical']
    static=json.loads((base/'static_gate/polarized_pressure/run01/results.json').read_text())['raw_lapse_necessary_mu_upper_bound']
    factor=background['Omega_d']*background['I0']/(4*background['Omega_r']*background['a_BBN']**2)
    frozen=math.sqrt(factor/background['radiation_budget'])
    assert abs(frozen/background['mu_B1b']-1)<1e-13
    selected=[r for r in static if r['Lambda_Mpc_inverse2']<=1.1e-7]
    exact_upper=max(r['mu_necessary_upper_Mpc_inverse'] for r in selected)
    rounded_upper=450.0
    assert exact_upper<rounded_upper
    weak_budget=1.0
    weak_lower=math.sqrt(factor/weak_budget)
    assert frozen>rounded_upper and weak_lower>rounded_upper
    result={
        'claim':'No overlap of the stated repaired-action galaxy target and unchanged homogeneous early-history requirements',
        'scope':'Perspective B plus Q Gamma, Pi concavity on the rectangular Q band, specified static target/energy ceiling, positive energy, no additional stress sector, unchanged source-free quadratic FRW branch',
        'units':'mu in Mpc^-1, Lambda in Mpc^-2',
        'Lambda_benchmarks_max':1.1e-7,
        'raw_static_upper':exact_upper,'conservative_rounded_static_upper':rounded_upper,
        'frozen_BBN_budget':background['radiation_budget'],'frozen_BBN_lower':frozen,
        'frozen_interval_gap_factor':frozen/rounded_upper,
        'weakened_radiation_budget':weak_budget,'weakened_BBN_lower':weak_lower,
        'weakened_interval_gap_factor':weak_lower/rounded_upper,
        'stiff_over_radiation_at_rounded_static_upper':factor/rounded_upper**2,
        'max_early_inventory_fraction_for_frozen_budget_at_static_upper':rounded_upper/frozen,
        'non_claims':['Not a new observational likelihood or a universal modified-gravity no-go',
                      'A different early branch, correlated invariant domain or additional stress sector changes the hypotheses',
                      'The inherited polarization-off growth bound is not used'],
        'all_arithmetic_checks_pass':True}
    p=Path(output);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main(sys.argv[1])
