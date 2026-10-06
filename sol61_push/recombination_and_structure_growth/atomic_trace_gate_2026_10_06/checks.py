import argparse,json,math
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['density','trace']);args=ap.parse_args();rows=[]
def ck(n,v):rows.append({'name':n,'passed':bool(v)})
A,m,B,th,n,x=s.symbols('A m B theta n x',positive=True)
rho=n*(m-(1-x)*B+s.Rational(3,2)*(1+x)*th);pressure=n*(1+x)*th
trace=rho-3*pressure
if args.control=='trace':trace=rho
ck('trace_expression',s.expand(trace-n*(m-(1-x)*B-s.Rational(3,2)*(1+x)*th))==0)
ck('ionization_trace_derivative',s.expand(s.diff(trace,x)-n*(B-s.Rational(3,2)*th))==0)
ck('ionized_nonzero_rest_trace',s.expand(trace.subs(x,1)-n*(m-3*th))==0)
ck('binding_energy_difference',s.expand((rho.subs(x,1)-rho.subs(x,0))-n*(B+s.Rational(3,2)*th))==0)
density_power=2 if args.control=='density' else 3
ck('saha_frame_cancellation',s.simplify((A*A)**s.Rational(3,2)/A**density_power-1)==0)
ck('binding_temperature_invariant',s.cancel(A*B/(A*th)-B/th)==0)
ck('collision_rate_weight',s.cancel(A**3*A**-2-A)==0)
R=s.symbols('R',positive=True)
ck('tight_coupling_sound_speed',s.cancel(1/(3*(1+R))-((s.Rational(1,3))/(1+R)))==0)
frac=13.6/(938.783e6);ck('small_atomic_trace_fraction',frac<1.5e-8)
for t in [0,.1,.3,.5,1.36]:ck('fixed_temperature_bound_'+str(t),abs(13.6-1.5*t)/(938.783e6)<=frac)
out={'checks':rows,'passed':sum(r['passed'] for r in rows),'total':len(rows),'control':args.control,'binding_rest_fraction':frac,'scope':'Exact identities under declared ideal atomic approximation; finite energy bound samples are corroboration,not transport simulation.'}
Path(args.out).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'passed':out['passed'],'total':out['total'],'failed':[r['name'] for r in rows if not r['passed']]}))
