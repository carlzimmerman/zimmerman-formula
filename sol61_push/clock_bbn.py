"""Conditional coupling bound; no nuclear network or abundance likelihood."""
import argparse
import json
import math
from scipy.optimize import brentq

dmin = brentq(lambda d: d*(1+d)**2-48*math.pi, 0, 10, xtol=1e-13)
rmax = dmin/(1+dmin)
alpha = (7/8)*(4/11)**(4/3)
# Ideal instantaneous-decoupling baseline, consistently three neutrinos.
delta_early = (43/7)*(1/rmax-1)
delta_late = (1/alpha+3)*(1/rmax-1)
checks = []
def check(name, passed):
    checks.append({'name': name, 'passed': bool(passed)})
check('root residual', abs(dmin*(1+dmin)**2-48*math.pi)<1e-10)
check('equivalent endpoint ratio', abs(rmax-48*math.pi/(1+dmin)**3)<1e-12)
check('endpoint below published BBN-only interval', rmax<0.92)
rows=[]
for d in (dmin+0.01, 5, 10, 100):
    lam=(1+d*(1+d)**2/(24*math.pi))/3
    ratio=2*d/((1+d)*(3*lam-1))
    check('target elimination '+str(d), abs(ratio-48*math.pi/(1+d)**3)<1e-12)
    check('strict endpoint bound '+str(d), lam>1 and ratio<rmax)
    rows.append({'D':d, 'lambda':lam, 'G_cosm_over_G_N':ratio})
early_tuned_late=rmax*(1+alpha*(3+delta_early))/(1+3*alpha)
late_tuned_early=rmax*(1+7*delta_late/43)
check('one constant species count cannot match both ideal epochs', delta_early<delta_late and early_tuned_late<1 and late_tuned_early>1)
result={'passed':all(c['passed'] for c in checks), 'checks':checks,
        'D_min':dmin, 'R_supremum':rmax, 'H_ratio_supremum':math.sqrt(rmax),
        'published_BBN_only_95_4_interval':[0.92,1.04],
        'ideal_extra_neutrino_count_early_infimum':delta_early,
        'ideal_extra_neutrino_count_late_infimum':delta_late,
        'early_tuned_late_H_squared_ratio':early_tuned_late,
        'late_tuned_early_H_squared_ratio':late_tuned_early, 'samples':rows}
parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
with open(args.output,'w') as f: json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
raise SystemExit(0 if result['passed'] else 1)
