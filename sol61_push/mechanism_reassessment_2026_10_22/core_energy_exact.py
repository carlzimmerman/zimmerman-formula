"""Exact rational evaluation of a proved continuum-energy remainder bound."""
import json,sys
from fractions import Fraction as F
from pathlib import Path
terms=[F(3,(2*n+1)*(n+5)*6**(2*n+1)) for n in range(1,11)]
low=-F(97,240)+F(1,14400)+sum(terms,F(0))
next_term=F(3,23*16*6**23)
high=low+next_term*F(36,35)
def floor(m,R=None):
    return -(F(3,5)+F(3,2)*m)**2/F(6,5)-(1-m)/R if R else -(F(3,5)+F(3,2)*m)**2/F(6,5)
checks=dict(negative_gap=high<-F(3,10),
    retained=floor(F(6378,100000))>high,
    inside20=floor(F(3516,100000),20)>high,
    inside100=floor(F(5834,100000),100)>high,
    remainder_width=high-low<F(1,10**19))
out=dict(checks=checks,all_pass=all(checks.values()),
    exact_energy_interval=[str(low),str(high)],approximate_energy_interval=[float(low),float(high)],
    exact_interval_width=str(high-low),strict_mass_lower_bounds=dict(asymptotic='0.06378',inside20='0.03516',inside100='0.05834'),
    scope='Exact arithmetic checks conditional on the analytic Hamiltonian inequality and geometric series remainder proof. No global-existence or settled-core claim.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
