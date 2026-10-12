"""Finite numerical cross-check of the source's n=2 Lame instability."""
import json, math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import ellipj, ellipk
rows=[]; checks=[]
for eps in [0.001,0.003,0.01,0.1,0.3]:
    A=1+eps; am1=eps*(2+eps); k2=2*am1/(1+am1)
    gap=3*k2*k2/(2*math.sqrt(1-k2+k2*k2)+2-k2)
    pmax2=A*A*gap/4
    T=4*ellipk(k2)/A
    for offset in [.1,.5,.9,1.1,2.,10.]:
        p2=offset*pmax2; w=math.sqrt(1+p2)
        def rhs(t,z):
            sn=ellipj(A*t/2,k2)[0]
            delta=1.5*am1*(1-2*sn*sn)
            si,co=math.sin(w*t),math.cos(w*t)
            L=delta*np.array([[si*co/w,si*si/(w*w)],[-co*co,-co*si/w]])
            return (L@z.reshape(2,2)).ravel()
        sol=solve_ivp(rhs,(0,T),np.eye(2).ravel(),method='DOP853',rtol=1e-12,atol=1e-14,max_step=T/160)
        si,co=math.sin(w*T),math.cos(w*T)
        F=np.array([[co,si/w],[-w*si,co]])@sol.y[:,-1].reshape(2,2)
        det=float(np.linalg.det(F)); disc=float(((F[0,0]-F[1,1])/2)**2+F[0,1]*F[1,0])
        growth=math.asinh(math.sqrt(max(0,disc)/det))/T
        checks.append(dict(epsilon=eps,offset=offset,passed=bool(sol.success and abs(det-1)<1e-10 and (disc>0 if offset<1 else disc<0))))
        rows.append(dict(epsilon=eps,p2_over_M2=p2,gap_upper_p2_over_M2=pmax2,offset=offset,growth_per_Mt=growth,growth_over_epsilon_squared=growth/eps**2))
eps=1e-7; A=1+eps;k2=2*eps*(2+eps)/(1+eps*(2+eps))
gap=3*k2*k2/(2*math.sqrt(1-k2+k2*k2)+2-k2)
out=dict(rows=rows,checks=checks,all_pass=all(c['passed'] for c in checks),benchmark_upper_p_over_M=A*math.sqrt(gap)/2,non_claims=['No floating monodromy at epsilon=1e-7','No nonlinear fragmentation bound','No expansion or depleted-source radial evolution'])
(Path(__file__).parent/'radial_band_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print('Checks:',len(checks),out['all_pass'])
for row in rows:
    if row['offset']==.5: print(json.dumps(row))
print('benchmark upper p/M:',out['benchmark_upper_p_over_M'])
assert out['all_pass']
