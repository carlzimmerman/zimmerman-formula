import sys,json,runpy
from pathlib import Path
import numpy as np
from scipy.special import roots_legendre
out=Path(sys.argv[1]);sys.argv=['calculate.py','--output',str(out.parent/'replica.json')];g=runpy.run_path(str(Path(__file__).with_name('calculate.py')))
r=g['result'];cache={};rec=[]
def calc(m,R,omega,n):
 if n not in cache:cache[n]=roots_legendre(n)
 x,w=cache[n];L=np.log1p(100/R**2);y=(x+1)*L/2;u=R**2/2*np.expm1(y);w=w*L/2*(u+R**2/2)*np.exp(-u)
 s=R*R+2*u[:,None];v=R*R+2*u[None,:];S=s+v;q=np.sqrt(omega*omega-.04)
 base=(4*np.pi*m)**2/(2*np.pi)**1.5*S**(-1.5)*np.exp(-q*q*s*v/(2*S))
 src=np.sum(w[:,None]*w[None,:]*base*(-.1*R*R)*(3/S+.5*q*q*(s*s+v*v)/S**2))
 p=omega*q*src*src/(32*np.pi*np.pi*.125)
 widths=R*R+2*u;h=4*np.pi*m*np.sum(w/(2*np.pi*widths)**1.5)
 rr=np.linspace(0,5*R,1001);P=4*np.pi*m*np.sum(w[None,:]*rr[:,None]/widths[None,:]*np.exp(-rr[:,None]**2/(2*widths[None,:]))/(2*np.pi*widths[None,:])**1.5,axis=1)
 return float(p),float(max(P)),float(100*h*h)
for row in r['rows']:
 if not row['power']:continue
 R=row['R_kpc']/g['ell'];m=row['mass_Msun']/g['M0'];p,P,C=calc(m,R,row['omega'],256);p2,P2,C2=calc(m,R,row['omega'],512)
 rec.append(dict(z=row['z'],factor=row['factor'],M=row['mass_Msun'],weak=P2<.1 and C2<.1,power=p2,maxP=P2,chi_bound=C2,error=abs(p/p2-1),old_error=abs(row['power']/p2-1),cooling_Gyr=float(m*m/(2*np.sqrt(np.pi)*R)/p2*g['t0']),age_Gyr=row['age_Gyr']))
checks=[dict(name='transformed_quadrature_all_256_vs_512',passed=max(x['error'] for x in rec)<1e-5,value=max(x['error'] for x in rec))]
weak=[x for x in rec if x['weak']];best=min(weak,key=lambda x:x['cooling_Gyr']/x['age_Gyr'])
out.write_text(json.dumps(dict(checks=checks,records=rec,best_weak_age_ratio=best),indent=2)+'\n')
