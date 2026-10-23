import sys,json
from pathlib import Path
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.special import roots_legendre
from scipy.linalg import eigh
p=Path(__file__).parent
# Endpoint functions and identical background from the verified resonance calculation.
source=(p/'resonant16.py').read_text().split('rows=[]')[0];ns={'__file__':str(p/'resonant16.py'),'__name__':'pv_background'};exec(source,ns)
sol=ns['sol'];R=ns['R'];r0=ns['r0'];dp=ns['dp'];lc=ns['lc'];endpoint_orbit=ns['endpoint_orbit'];F=ns['F'];brentq=ns['brentq'];rows=[]
for order in [64,128]:
 d=np.load(p/f'action16_{order}.npz');meta=json.load(open(p/f'action16_{order}.json'));gx,gw=roots_legendre(order);us=(gx+1)*meta['max_L2']/2;uw=gw*meta['max_L2']/2;Os=d['omega'].reshape(order,order);Qs=d['Q'].reshape(order,order);Cs=d['coeff'].reshape(order,order,16,16);S=d['S']
 cached=[]
 for j,u in enumerate(us):
  rc=brentq(lambda x:lc(x)-u,r0,R);emin=-sol.sol(rc)[1]+u/(2*rc*rc);emax=-u/2;h=rc*1e-5;oc=np.sqrt(-(dp(rc+h)-dp(rc-h))/(2*h)-3*dp(rc)/rc);oe,ce=endpoint_orbit(emax,u,rc)
  E=np.r_[emin,-Qs[j]-u/2,emax];O=np.r_[oc,Os[j],oe];C=np.concatenate([np.zeros((1,16,16)),Cs[j],ce[None,:,:]])
  cached.append((E,PchipInterpolator(E,O),PchipInterpolator(E,C,axis=0)))
 for quadorder in [16,32]:
  gx2,gw2=roots_legendre(quadorder)
  for omega in [.822,.8228,.8236]:
   Pi=np.zeros((16,16));rootcount=0
   for (E,oi,ci),wu in zip(cached,uw):
    nodes=((E[:-1,None]+E[1:,None])/2+(E[1:]-E[:-1])[:,None]/2*gx2).ravel();weights=((E[1:]-E[:-1])[:,None]/2*gw2).ravel();O=oi(nodes);C=ci(nodes)
    for n in range(1,17):
     roots=oi.solve(omega/n,extrapolate=False);roots=roots[np.isfinite(roots)&(roots>E[0])&(roots<E[-1])];rootcount+=len(roots)
     v=C[:,n-1,:];mult=4*np.pi*n*n*O/(omega*omega-n*n*O*O);piece=v.T@((weights*mult)[:,None]*v)
     for er in roots:
      slope=float(oi.derivative()(er));cr=ci(er)[n-1];res=-2*np.pi*np.outer(cr,cr)/slope
      piece+=res*(np.log((E[-1]-er)/(er-E[0]))-np.sum(weights/(nodes-er)))
     Pi+=F*np.pi*wu*piece
   Pi=(Pi+Pi.T)/2;vals,vec=eigh(S-Pi,S);ix=np.argmin(abs(vals));rows.append(dict(order=order,quadrature=quadorder,omega=omega,near_zero_eigenvalue=float(vals[ix]),mode=vec[:,ix].tolist(),matrix=Pi.tolist(),root_count=rootcount))
comparisons=[]
for order in [64,128]:
 for omega in [.822,.8228,.8236]:
  a=next(r for r in rows if r['order']==order and r['omega']==omega and r['quadrature']==16);b=next(r for r in rows if r['order']==order and r['omega']==omega and r['quadrature']==32)
  comparisons.append(dict(order=order,omega=omega,relative_matrix_error=float(np.linalg.norm(np.array(a['matrix'])-b['matrix'])/np.linalg.norm(b['matrix'])),eigenvalue_difference=abs(a['near_zero_eigenvalue']-b['near_zero_eigenvalue'])))
checks=dict(finite=all(np.isfinite(r['near_zero_eigenvalue']) for r in rows),quadrature=all(x['relative_matrix_error']<1e-4 for x in comparisons))
out=dict(checks=checks,all_pass=all(checks.values()),rows=rows,comparisons=comparisons,scope='pole-subtracted PCHIP principal-value matrix; interpolation and action-grid convergence still required')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps({**out,'rows':[{k:v for k,v in r.items() if k not in ['mode','matrix']} for r in rows]},indent=2));sys.exit(0 if out['all_pass'] else 1)
