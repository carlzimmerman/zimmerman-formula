"""Spherical density-matrix SP response; no nonspherical stability claim."""
import argparse,json,pathlib,hashlib,time,resource
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.linalg.lapack import zgttrf,zgttrs
P=pathlib.Path(__file__).resolve().parent; ROOT=P.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=argparse.ArgumentParser();a.add_argument('--galaxy',default='Sextans');a.add_argument('--dt',type=float,default=.02);a.add_argument('--T',type=float,default=10);a.add_argument('--kick',type=float,default=0);a.add_argument('--tag',required=True);args=a.parse_args()
fp=P/f'eta1500_refine_{args.galaxy.replace(" ","")}.npz';jp=P/'eta1500_refine.json';files=[pathlib.Path(__file__),fp,jp];before={p.name:sha(p) for p in files};start=time.time()
raw=np.load(fp);record=json.loads(jp.read_text());res=next(z for z in record['results'] if z['name']==args.galaxy);eta=res['eta_code'];x=raw['x'];h=x[1]-x[0];n=len(x);pot=raw['target_potential'];pb=pot+1/np.sqrt(1+x*x);ids=raw['mode_ids'];occ=raw['occupation'];keep=occ>1e-10;ids=ids[keep];occ=occ[keep];K0=np.full(n,eta*eta/h**2);off=np.full(n-1,-eta*eta/(2*h*h));modes=[];blocks={}
for l in sorted(set(ids[:,0])):
    sel=np.where(ids[:,0]==l)[0];ind=ids[sel,1];dk=K0+eta*eta*l*(l+1)/(2*x*x)
    ev,U=eigh_tridiagonal(dk+pot,off,select='i',select_range=(0,int(max(ind))))
    modes.extend([(int(l),int(j)) for j in ind]);V=U[:,ind]*np.sqrt(occ[sel])[None,:]
    phase=np.exp(1j*args.kick*x*x/(2*eta))
    V=(V*phase[:,None]).astype(complex)
    c=1j*args.dt/(4*eta);fact=zgttrf(c*off,1+c*dk,c*off)
    assert fact[-1]==0
    blocks[int(l)]=[V,dk,fact[:-1]]
def density():return sum(np.sum(abs(B[0])**2,axis=1) for B in blocks.values())
def pc(s):return -np.cumsum(s)/x-(np.cumsum((s/x)[::-1])[::-1]-s/x)
def diag(t):
    s=density();p=pc(s);K=0
    for V,dk,f in blocks.values():K+=np.sum(dk[:,None]*abs(V)**2)+2*np.real(np.sum(off[:,None]*V[:-1].conj()*V[1:]))
    E=float(K+np.sum(s*pb)+.5*np.sum(s*p));cdf=np.cumsum(s)
    return {'t':t,'mass':float(sum(s)),'E':E,'core_mass_fraction':float(np.interp(1.,x+h/2,cdf)),'rhalf':float(np.interp(.5*sum(s),cdf,x+h/2)),'max_cdf_change':float(max(abs(cdf-cdf0))) if 'cdf0' in globals() else 0}
def kinetic():
    for l,B in blocks.items():
        V,dk,f=B;c=1j*args.dt/(4*eta);rhs=(1-c*dk[:,None])*V;rhs[:-1]-=c*off[:,None]*V[1:];rhs[1:]-=c*off[:,None]*V[:-1]
        V,info=zgttrs(*f,rhs);assert info==0;B[0]=V
cdf0=np.cumsum(density());hist=[diag(0)];steps=round(args.T/args.dt)
for j in range(steps):
    kinetic();v=pc(density())+pb;phase=np.exp(-1j*args.dt*v/eta)
    for B in blocks.values():B[0]*=phase[:,None]
    kinetic()
    if (j+1)%max(1,steps//50)==0:hist.append(diag((j+1)*args.dt))
after={p.name:sha(p) for p in files};assert before==after
out={'scope':'spherical density-matrix time evolution only; not pure-state or nonspherical stability','parameters':vars(args),'inputs_before':before,'inputs_after':after,'history':hist,'max_relative_energy_drift':max(abs(z['E']/hist[0]['E']-1) for z in hist),'max_relative_mass_drift':max(abs(z['mass']/hist[0]['mass']-1) for z in hist),'max_cdf_change':max(z['max_cdf_change'] for z in hist),'runtime_s':time.time()-start,'maxrss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/(args.tag+'.json')).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ['history','inputs_before','inputs_after']},flush=True)
