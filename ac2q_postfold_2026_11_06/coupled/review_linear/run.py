import sys,json,warnings
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from evolve_adm_v2 import System,rk4
warnings.filterwarnings('ignore',category=RuntimeWarning)
g=.1;ss=.01;V=.01;K=.5;k=128;m=4;eps=1e-12
H0=np.sqrt((ss/2+V)/3)
def rhs(t,y):
    B,H,b,n=y;v2=np.exp(6*B);X=ss/(2*v2);Q2=(k*m)**2*np.exp(-2*B)
    c=1-2*g*X;S=K+g*Q2;E=2*X*S+c*c*Q2;A=S/E
    Sd=-2*g*H*Q2;cd=12*g*H*X
    Ed=-12*H*X*S+2*X*Sd+2*c*cd*Q2-2*H*c*c*Q2
    Hd=V*v2
    return [H,Hd,H*n,(Sd/S-Ed/E+Hd/H-6*H)*n-A*ss*Q2*b/H]
ref=solve_ivp(rhs,[0,.01],[0,H0,eps,0],method='DOP853',rtol=1e-12,atol=[1e-14,1e-14,1e-24,1e-24],dense_output=True)
rows=[]
for dt in [.000625,.0003125]:
    s=System(31,k);y=s.initial(True);th=2*np.pi*np.arange(31)/31;wave=np.cos(m*th)
    y[1:32]+=eps*wave
    y[32:63]+=-4*H0*eps*wave
    y[63:]+=- (8*H0-2*(k*m)**2/H0)*eps*wave
    try:
        for _ in range(round(.01/dt)):y=rk4(s,y,dt)
        f=s.constrain(y);B,H,b,n=ref.y[:,-1];v2=np.exp(6*B);Q2=(k*m)**2*np.exp(-2*B);X=ss/(2*v2)
        A=(K+g*Q2)/(2*X*(K+g*Q2)+(1-2*g*X)**2*Q2)
        pb=v2*n/(A*H)-(8*H-2*v2*Q2/H)*b
        projection=lambda z:float(2*np.mean(z*wave))
        rows.append(dict(dt=dt,beta_native=projection(f['b']-B),beta_reference=b,
          beta_field_relative=float(np.max(np.abs(f['b']-B-b*wave))/eps),
          lapse_native=projection(f['N']/np.exp(3*B)-1),lapse_reference=n,
          pb_native=projection(f['pb']+4*H),pb_reference=pb,
          momentum_abs=s.diagnostic(y,.01)['momentum_abs']))
    except Exception as e:rows.append(dict(dt=dt,error=str(e)))
out=dict(contract='CONTRACT.md',reference_success=ref.success,reference_final=ref.y[:,-1].tolist(),rows=rows)
print(json.dumps(out,indent=2))
