import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp
from scipy.linalg import eigh_tridiagonal
from scipy.signal import find_peaks
p=Path(__file__).parent
x=np.linspace(1e-6,1,600);m=2.5*x**3-1.5*x**5;rho=7.5*(1-x*x)/8

def fun(t,y,a):
 R=a[0];r=R*t;q=y[0]/r**2
 return np.array([R*r*r*y[1],R/.01*(q*q/(1-q)-r/(1+r*r)**1.5)])
def bc(a,b,z):return np.array([a[0]-a[1]*(z[0]*1e-6)**3/3,b[0]-1,b[1]])
sol=solve_bvp(fun,bc,x,np.array([m,rho]),p=[2.],tol=2e-10,max_nodes=20000);R=sol.p[0]
results=[]
for n in [256,512,1024,2048]:
 h=R/(n+1);r=h*np.arange(1,n+1);m,d=sol.sol(r/R);q=m/r**2
 b=1/(r*r*d);faces=.01/(h*(np.arange(n+1)+.5))**2
 diag=(faces[:-1]+faces[1:])/h**2+q*(2-q)/(1-q)**2/r**2
 off=-faces[1:-1]/h**2
 vals,vec=eigh_tridiagonal(diag/b,off/np.sqrt(b[:-1]*b[1:]),select='i',select_range=(0,31),tol=1e-11)
 # Transform eigenvector back to s; independent Rayleigh quotient.
 s=vec[:,0]/np.sqrt(b);jumps=np.diff(np.r_[0,s,0]);potential=q*(2-q)/(1-q)**2/r**2
 rq=(np.sum(faces*jumps*jumps)/h+np.sum(potential*s*s)*h)/(np.sum(b*s*s)*h)
 s0=r**3*d
 overlaps=vec.T@(np.sqrt(b)*s0)
 strengths=overlaps**2/np.sum(b*s0*s0)
 results.append(dict(n=n,omega2=vals[:6].tolist(),omega=np.sqrt(vals[:6]).tolist(),periods=(2*np.pi/np.sqrt(vals[:6])).tolist(),dilation_mode_strengths=strengths[:6].tolist(),captured_dilation_strength=float(strengths.sum()),rayleigh_error=abs(rq/vals[0]-1)))
live={}
for ng in [256,512]:
 c=json.load(open(p/f'cold_control_{ng}.json'))['rows'];k=json.load(open(p/f'cold_kick_{ng}.json'))['rows'];t=np.array([r['t'] for r in c]);delta=np.array([a['rms_radius']-b['rms_radius'] for a,b in zip(k,c)])
 peaks,_=find_peaks(delta,prominence=.02,distance=int(3/(t[1]-t[0])))
 live[str(ng)]=dict(peak_times=t[peaks].tolist(),peak_spacings=np.diff(t[peaks]).tolist())
checks=dict(background=bool(sol.status==0),positive=all(min(r['omega2'])>0 for r in results),rayleigh=all(r['rayleigh_error']<1e-7 for r in results),refinement=bool(max(abs(np.array(results[-1]['omega'])/results[-2]['omega']-1))<.005))
out=dict(checks=checks,all_pass=all(checks.values()),edge=float(R),spectra=results,live=live,scope='zero-dispersion spherical fluid spectrum; comparison with finite-A simulations is diagnostic')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
