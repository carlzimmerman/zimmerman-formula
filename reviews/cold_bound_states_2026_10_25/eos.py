import argparse,json,math
from pathlib import Path
from scipy.optimize import brentq
from scipy.integrate import quad
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
req=json.load(open('reviews/cold_local_production_2026_10_25/run/result.json'))['rows'];wave=json.load(open('reviews/cold_wave_relaxation_2026_10_25/run/result.json'))['rows'];speed={(r['name'],r['model'],r['footing'],r['shell']):r['sigma_kms'] for r in wave if r['sigma_factor']==1}
rows=[]
for r in req:
 d=r['gas_d'];E=r['required_source_over_D']
 def potential(q):
  s=math.sin(q/2)**2;z=s/(math.sqrt(1-s)*(1+math.sqrt(1-s)))
  return (d-8)*z+36*z*z+40*z**3+10*z**4
 def deriv(q):
  x=1/math.cos(q/2);return (40*x**3-48*x+d)*.5*x*math.tan(q/2)
 amp=brentq(lambda q:potential(q)-E,0,math.pi-1e-5,xtol=1e-14)
 def integ(theta,which):
  q=amp*math.sin(theta);diff=E-potential(q)
  assert diff>0
  weight=amp*math.cos(theta)/math.sqrt(2*diff)
  if which==0:return weight
  if which==1:return diff*weight
  if which==2:return .5*q*deriv(q)*weight
  return d*(1/math.cos(q/2)-1)*weight
 vals=[quad(lambda t:integ(t,j),0,math.pi/2,epsabs=1e-10,epsrel=2e-10)[0] for j in range(4)]
 K=vals[1]/vals[0];vir=vals[2]/vals[0];assert abs(K-vir)<1e-7*max(K,vir)
 w=(2*K-E)/E;v2=(speed[(r['name'],r['model'],r['footing'],r['shell'])]/299792.458)**2
 assert w>0
 rows.append(dict(name=r['name'],model=r['model'],footing=r['footing'],shell=r['shell'],d=d,E=E,amplitude=amp,w_eff=w,matter_energy_fraction=vals[3]/vals[0]/E,w_over_v2=w/v2,virial_relative_error=abs(K-vir)/K))
summary=dict(cases=len(rows),w_eff_range=[min(r['w_eff'] for r in rows),max(r['w_eff'] for r in rows)],w_over_v2_range=[min(r['w_over_v2'] for r in rows),max(r['w_over_v2'] for r in rows)],max_virial_error=max(r['virial_relative_error'] for r in rows))
(out/'result.json').write_text(json.dumps(dict(summary=summary,rows=rows),indent=2)+'\n');print(json.dumps(summary,indent=2))
