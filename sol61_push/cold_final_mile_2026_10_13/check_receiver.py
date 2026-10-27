"""CE-FM-007 comparison receiver accounting, full and cubic, variable packets and empty state."""
import json,sys
from pathlib import Path
import numpy as np
from conservative_receiver import capture,energy

checks=[];rows=[]
def check(name,cond,detail):
    checks.append(dict(name=name,passed=bool(cond),detail=detail))
    if not cond:raise AssertionError(name)

r=np.array([.1,.5,.8]);v=np.array([-4.,-1.,-.5]);dm=np.array([.004,.04,.2])
for full in (False,True):
    for c2 in (1e6,1e10):
        for radiation in (0.,.001):
            ans=capture(r,v,dm,[True,False,False],1.,.0001,c2,radiation,full)
            key=f'full={full},c2={c2},radiation={radiation}'
            check('whole modeled energy balance '+key,abs(ans['energy_balance_residual'])<1e-8,ans['energy_balance_residual'])
            check('variable packet stays subpercent '+key,0<ans['delta_bh']<.01,ans['delta_bh'])
            # Remove every remaining packet in a second event; tests an actually empty receiver update.
            final=capture(ans['r'],ans['v'],ans['dm'],[True,True],1.,ans['bh_mass'],c2,0.,full)
            check('empty halo update '+key,len(final['r'])==0 and final['energy_after']==0 and abs(final['energy_balance_residual'])<1e-6,final['energy_balance_residual'])
            rows.append({k:value for k,value in ans.items() if k not in ('r','v','dm')})
check('empty halo has zero dynamical energy',energy([],[],[],1.,True)==0,'Avoids CFG750 empty-array crash')
try:
    energy([.1],[0.],[.05],1.,True)
    rejected=False
except ValueError:
    rejected=True
check('inadmissible saturated packet rejected',rejected,'dm/r^2=5 is outside full model')
result=dict(checks=checks,updates=rows,
            scope='Instantaneous energy-conserving declared comparison receiver only; no physical capture law, radiation prediction or relativistic closure.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
