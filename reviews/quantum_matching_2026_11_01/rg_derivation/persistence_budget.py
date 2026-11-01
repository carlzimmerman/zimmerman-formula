"""Conditional derivative budgets; does not estimate the missing correction."""
import argparse
import json
from pathlib import Path
import resource
import mpmath as mp

mp.mp.dps=50
root=Path(__file__).resolve().parents[3]
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
source=root/'reviews/three_priorities_2026_11_01/spectrum_pressure/run_exact_gap/result.json'
d=json.loads(source.read_text(),parse_float=str)
selected=[r for r in d['gap_and_pressure'] if mp.mpf(r['X_over_min']) in map(mp.mpf,('1.2','1.3','1.5'))]
assert len(selected)==3
L=16*mp.pi**2;rows=[]
for e in map(mp.mpf,('.01','.03','.05','.1')):
    for r in selected:
        fac=(e/mp.mpf('.6'))**2
        u=mp.mpf(r['U_s'])*fac;dd=mp.mpf(r['U_ss'])*fac
        W=2*u+dd;N=dd-3*u
        assert u>0 and W>0 and N<0
        budget=min(u,W/3,-N/4)
        Cmax=budget*L**2/e**4
        # A correction below half this hypothetical budget preserves all signs.
        b=budget/2
        assert u-b>0 and W-3*b>0 and N+4*b<0
        rows.append({'e':str(e),'X_over_min':r['X_over_min'],
                     'baseline_Us':str(u),'baseline_Wss':str(W),'baseline_N':str(N),
                     'strict_equal_absolute_derivative_budget':str(budget),
                     'hypothetical_C_must_be_strictly_less_than':str(Cmax),
                     'normalization_of_hypothetical_bound':'|deltaUs|,|deltaUss| <= C e^4/(16pi^2)^2',
                     'scaled_tree_transverse_gap':str(mp.mpf(r['tree_transverse_min_positive_m2'])*e/mp.mpf('.6'))})
out={'claim_id':'TP02-CONDITIONAL-PERSISTENCE-BUDGET','cases':rows,'checks':{'12cases':len(rows)==12,'baseline_admissible_negative_pressure_numerator':True,'half_budget_sign_test':True},
     'scope':'Derived conditional budget only; no actualmatchingcoefficient or derivative correction bounded',
     'non_claims':['Saved numerical baseline is not an intervalcertificate','No conclusionat e=.03 without provingthe unknownfinitecorrectionderivativebound','Gapless/IRandfinitekineticmatchingobligationsremain'],
     'peak_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
assert out['peak_RSS_bytes']<1073741824
Path(a.out).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'cases':len(rows),'peak_RSS_bytes':out['peak_RSS_bytes'],'scope':out['scope']}))
