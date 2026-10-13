"""Conditional running-width vacuum scattering and production scan."""
import json,math
from pathlib import Path
from scipy.integrate import quad
P=Path(__file__).resolve().parent
b=json.loads((P.parent/'dilute_decay_v2_run/results.json').read_text())['rows'][-1]
m=b['m_eV'];rho=9.7151061903e6;c=299792.458;hb=6.582119569e-16
rows=[];checks=[]
for S in [.1,.3]:
 for u in [.01,.015,.02,.03]:
  lm=b['lambda_min']*math.sqrt(S/4);g=2*m*u*math.sqrt(lm);M=2*m*math.sqrt(1+u*u)
  G=g*g*u/(8*math.pi*M*math.sqrt(1+u*u));A=math.sqrt(rho)/(math.sqrt(2)*M);O=2*g*A/M
  eta=lm*u/(8*math.pi*math.sqrt(1+u*u));vp=2*c*u
  def cross(x):
   # lambda_eff/lambda_min = 3 + 1/(x-1+i*eta(x)).
   width=lm*u*math.sqrt(x)/(8*math.pi*math.sqrt(1+u*u*x))
   amp=3+1/complex(x-1,width)
   return S*abs(amp/2)**2/(1+u*u*x)
  results={}
  for mean in [1150.,1900.]:
   sd=mean*math.sqrt(math.pi)/4
   def weight(x):
    v=vp*math.sqrt(x)
    pdf=v*v*math.exp(-v*v/(4*sd*sd))/(2*math.sqrt(math.pi)*sd**3)
    return (vp*vp/2)*pdf/mean
   xmax=(25000/vp)**2
   vals=[]
   for nwidth in [100.,1000.]:
    lo=1-nwidth*eta;hi=1+nwidth*eta
    def segmented(a,b):
     pts=[a,b]+[1+sign*eta*nwidth*10**j for sign in [-1,1] for j in range(10) if a<1+sign*eta*nwidth*10**j<b]
     pts=sorted(set(pts))
     return sum(quad(lambda x:cross(x)*weight(x),aa,bb,epsabs=1e-10,limit=100)[0] for aa,bb in zip(pts[:-1],pts[1:]))
    left=segmented(0,lo)
    right=segmented(hi,xmax)
    local=quad(lambda t:cross(1+eta*math.tan(t))*weight(1+eta*math.tan(t))*eta/(math.cos(t)**2),-math.atan(nwidth),math.atan(nwidth),epsabs=1e-8,limit=500)[0]
    vals.append(left+local+right)
   checks.append(dict(name=f'partition agreement S={S} u={u} mean={mean}',passed=abs(vals[0]-vals[1])<max(1e-6,1e-5*vals[1])))
   results[str(mean)]=vals[1]
  rows.append(dict(S_cm2_g=S,u=u,resonance_speed_proxy_kms=vp,g_eV=g,lambda_total=3*lm,lifetime_s=hb/G,occupation_bound=math.sinh(2*O/G)**2,free_pressure_over_energy=u*u/(3*(1+u*u)),effective_scattering_cm2_g=results))
R=dict(rows=rows,checks=checks,all_pass=all(q['passed'] for q in checks),assumptions=['Vacuum running-width ansatz, no renormalized real self energy','Maxwell relative speeds to 25000km/s, not escape-truncated halos','Velocity proxy v=2p/m, NR accurate only to order u²','No separately added real-source collision term','Passing this screen is not empirical evidence for the carrier'])
(P/'resonance_run_v2'/'results.json').write_text(json.dumps(R,indent=2)+'\n');print(json.dumps(R,indent=2));assert R['all_pass']
