import json,sys
from pathlib import Path
import numpy as np
p=Path(__file__).parent
out={};checks={}
for N in [1024,4096]:
 d=json.load(open(p/f'kinetic_weight_{N}.json'));r=d['rows'][0];o=np.array(r['omega_samples']);Q=np.array(r['Q_samples']);C=np.array(r['couplings']);freq=o[:,None]*np.arange(1,17);S=2*freq**2*C*C/Q[:,None]
 checks[f'direct_checks_{N}']=d['all_pass'];checks[f'positive_Q_{N}']=bool(min(Q)>0)
 widths=[]
 for eps in [.1,.03,.01,.003,.001]:
  terms=-r['mass']*np.mean(S/(freq**2-(d['cold_collective_omega']+1j*eps)**2),axis=0);v=sum(terms)
  widths.append(dict(epsilon=eps,real=float(v.real),absorptive=float(-v.imag),third=float(-terms[2].imag),fourth=float(-terms[3].imag)))
 out[N]=dict(sum_rule_error=r['sum_rule_relative_error'],sum_rule_sample=r['sum_rule_sample'],sum_rule_integral=r['sum_rule_integral'],widths=widths)
checks['sum_rule_improves']=out[4096]['sum_rule_error']<out[1024]['sum_rule_error'];checks['passive']=all(x['absorptive']>=0 for r in out.values() for x in r['widths'])
result=dict(checks=checks,all_pass=all(checks.values()),results=out,scope='audit of direct prescribed-potential calculations; broadening is numerical, no damping-rate claim')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));sys.exit(0 if result['all_pass'] else 1)
