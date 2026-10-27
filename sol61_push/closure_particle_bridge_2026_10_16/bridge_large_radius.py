"""Discriminate a boundary-sensitive large-box limit in the joint bridge."""
import json
import sys
from pathlib import Path
from scipy.optimize import brentq

out=Path(sys.argv[1]);assert out.is_dir()
base=Path(__file__).parent;parent=base/'joint_cold_bridge.py'
text=parent.read_text();marker='\nrows=[]';assert text.count(marker)==1
ns={'__file__':str(parent),'__name__':'large_radius_bridge_definitions'}
exec(compile(text.split(marker)[0],str(parent),'exec'),ns)
integrals=ns['integrals'];check=ns['check'];rows=[]
for z in (1.,3.):
    B=2*z;target=2*B;prior=None
    for R in (1000.,10000.):
        def balance(mu):
            p,n,_=integrals(R,mu,z);return p-n
        mu=brentq(balance,0.,(target+2)/R,xtol=1e-14,rtol=1e-13)
        pos,neg,neutral=integrals(R,mu,z)
        error=abs(mu*R/target-1)
        check('large box conserved charge '+str((z,R)),abs(pos-neg)/(pos+neg)<1e-7)
        if prior is not None:
            check('approach analytic muR limit '+str(z),error<prior)
            check('finite comparison to asymptotic muR '+str(z),error<.01)
        predicted=[.5-1/(2*B),.5+1/(2*B)]
        measured=[v/R for v in neutral[0]]
        if R==10000.:
            check('inner occupation edge asymptotic '+str(z),abs(measured[0]-predicted[0])<.01)
            check('outer occupation edge asymptotic '+str(z),abs(measured[1]-predicted[1])<.01)
        row=dict(coupling=z,R=R,mu=mu,mu_times_R=mu*R,analytic_mu_times_R_limit=target,
            relative_limit_difference=mu*R/target-1,neutral_interval_over_R=measured,
            analytic_neutral_interval_over_R=predicted,positive_charge=pos,negative_charge_magnitude=neg)
        rows.append(row);print(json.dumps(row),flush=True);prior=error
checks=check.__globals__['checks']
result=dict(rows=rows,checks=checks,scope='Finite comparison to a proved large-R asymptotic of the specified local external-trap candidate; not a physical halo boundary or global novelty claim')
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print('Completed %d controls.'%len(checks))
