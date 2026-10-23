import json,sys
from pathlib import Path
import numpy as np
from scipy.special import roots_legendre
from scipy.interpolate import PchipInterpolator
from scipy.linalg import eigh
p=Path(__file__).parent;omega=.8228;F=15*10000/(2**4.5*np.pi)
# Fixed approximate mode direction from finest finite-broadening response, S normalized.
d=np.load(p/'action_128.npz');S=d['S'];freq=d['omega'][:,None]*np.arange(1,17);a=(2*d['derivative_weights'][:,None]*freq**2).ravel();b=(freq**2).ravel();V=d['coeff'].reshape(-1,8)*np.sqrt(a[:,None]);Pi=V.T@(V/(((omega+.003j)**2-b)[:,None]));ev,U=eigh((S-Pi).real,S);mode=U[:,np.argmin(abs(ev))]
source=(p/'multishape_orbits.py').read_text().split('cdf=cumulative')[0]
ns={'__file__':str(p/'multishape_orbits.py'),'__name__':'endpoint_background'};exec(source,ns)
rg=ns['r'];phis=ns['phi'];sol=ns['sol'];R=ns['R'];r0=ns['r0'];fun=ns['ns']['fun']
from scipy.optimize import brentq
def dp(r):return fun(r,sol.sol(r))[1]
def lc(r):return -r**3*dp(r)
def endpoint_orbit(e,u,rc,count=2048):
 def v2(r):return 2*(e+sol.sol(r)[1])-u/r**2
 rp=brentq(v2,r0,rc,xtol=1e-13);ra=brentq(v2,rc,R,xtol=1e-13)
 theta=(np.arange(count)+.5)*np.pi/(2*count);x=rp+(ra-rp)*np.sin(theta)**2;w=(ra-rp)*np.sin(2*theta)/np.sqrt(v2(x));phase=np.pi*(np.cumsum(w)-w/2)/w.sum()
 potentials=np.array([np.interp(x,rg,f) for f in phis]);C=(np.cos(np.arange(1,17)[:,None]*phase)*w)@potentials.T/w.sum()
 return 2*count/w.sum(),C
rows=[]
for order in [64,128]:
 data=np.load(p/f'action_{order}.npz');meta=json.load(open(p/f'action_{order}.json'));gx,gw=roots_legendre(order);u=(gx+1)*meta['max_L2']/2;uw=gw*meta['max_L2']/2
 Os=data['omega'].reshape(order,order);Qs=data['Q'].reshape(order,order);Cs=data['coeff'].reshape(order,order,16,8)
 matrices=np.zeros((16,8,8));counts=np.zeros(16,dtype=int);derivatives=[];near_ends=0;nonmonotonic=0;spots=[]
 for j in range(order):
  E=-Qs[j]-u[j]/2;O=Os[j]
  rc=brentq(lambda x:lc(x)-u[j],r0,R);emin=-sol.sol(rc)[1]+u[j]/(2*rc*rc);emax=-u[j]/2;h=rc*1e-5
  omega_circ=np.sqrt(-(dp(rc+h)-dp(rc-h))/(2*h)-3*dp(rc)/rc);omega_end,Cend=endpoint_orbit(emax,u[j],rc)
  E=np.r_[emin,E,emax];O=np.r_[omega_circ,O,omega_end];Cfull=np.concatenate([np.zeros((1,16,8)),Cs[j],Cend[None,:,:]],axis=0)
  interp=PchipInterpolator(E,O,extrapolate=False);deriv=interp.derivative()
  nonmonotonic+=int(np.any(np.diff(O)>0) and np.any(np.diff(O)<0))
  for n in range(1,17):
   roots=interp.solve(omega/n,extrapolate=False);roots=roots[np.isfinite(roots)&(roots>E[0])&(roots<E[-1])]
   cinterp=PchipInterpolator(E,Cfull[:,n-1,:],axis=0,extrapolate=False)
   for root in roots:
    index=min(max(np.searchsorted(E,root)-1,0),len(E)-2)
    def exact_res(energy):
     if energy==emin:return omega_circ-omega/n
     return endpoint_orbit(energy,u[j],rc)[0]-omega/n
    root=brentq(exact_res,E[index],E[index+1],xtol=1e-12)
    actual,Cactual=endpoint_orbit(root,u[j],rc);step=min((emax-emin)*1e-4,(root-emin)/4,(emax-root)/4)
    plus,_=endpoint_orbit(root+step,u[j],rc);minus,_=endpoint_orbit(root-step,u[j],rc);slope=abs((plus-minus)/(2*step))
    if slope<1e-9:raise RuntimeError('near tangent resonance needs special treatment')
    C=Cactual[n-1]
    if n==3 and j%16==0:
     actual,ca=endpoint_orbit(root,u[j],rc,count=1024);step=min((emax-emin)*1e-4,(root-emin)/4,(emax-root)/4)
     plus,_=endpoint_orbit(root+step/2,u[j],rc);minus,_=endpoint_orbit(root-step/2,u[j],rc);actual_slope=abs((plus-minus)/step)
     spots.append(dict(relative_resonance_error=abs(n*actual/omega-1),relative_slope_error=abs(actual_slope/slope-1),max_coefficient_error=float(max(abs(ca[n-1]-C)))))
    matrices[n-1]+=2*np.pi**3*F*uw[j]*np.outer(C,C)/slope;counts[n-1]+=1;derivatives.append(slope)
    near_ends+=int((root-E[0])/(E[-1]-E[0])<.01 or (E[-1]-root)/(E[-1]-E[0])<.01)
 B=matrices.sum(axis=0)
 rows.append(dict(order=order,spot_checks=spots,matrix=B.tolist(),mode_projected_absorption=float(mode@B@mode),dilation_absorption=float(B[0,0]),harmonic_mode_absorption=[float(mode@B@mode) for B in matrices],roots_per_harmonic=counts.tolist(),minimum_abs_energy_derivative=min(derivatives),near_end_roots=near_ends,nonmonotonic_rows=nonmonotonic,min_matrix_eigenvalue=float(min(np.linalg.eigvalsh(B)))))
B0=np.array(rows[0]['matrix']);B1=np.array(rows[1]['matrix']);checks=dict(direct_spots=all(all(x['relative_resonance_error']<1e-4 and x['relative_slope_error']<.01 and x['max_coefficient_error']<1e-4 for x in row['spot_checks']) for row in rows),positive_matrices=all(x['min_matrix_eigenvalue']>-1e-10 for x in rows),finite=all(np.isfinite(x['mode_projected_absorption']) for x in rows))
out=dict(checks=checks,all_pass=all(checks.values()),frequency=omega,mode=mode.tolist(),mode_reference_generalized_eigenvalue=float(ev[np.argmin(abs(ev))]),rows=rows,matrix_relative_change=float(np.linalg.norm(B1-B0)/np.linalg.norm(B1)),mode_relative_change=abs(rows[1]['mode_projected_absorption']/rows[0]['mode_projected_absorption']-1),scope='PCHIP-bracketed, direct-orbit-refined resonant curves; principal-value response and basis refinement still required')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps({**out,'rows':[{k:v for k,v in x.items() if k!='matrix'} for x in rows]},indent=2));sys.exit(0 if out['all_pass'] else 1)
