import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import argparse,datetime,hashlib,json,pathlib,platform,resource,subprocess,sys,time
import numpy as np,scipy
from scipy.interpolate import CubicSpline
from scipy.special import sph_harm
from sphere_v3 import Sphere
from flux import flux
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1]
p=argparse.ArgumentParser();p.add_argument('--galaxy',required=True,choices=['draco','sextans','fornax','leoi']);p.add_argument('--ne',type=int,default=128);p.add_argument('--nt',type=int,default=24);p.add_argument('--nf',type=int,default=32);p.add_argument('--dt',type=float,default=.02);p.add_argument('--T',type=float,default=8);p.add_argument('--wall',type=float,default=240);p.add_argument('--tag',required=True);a=p.parse_args()
start=time.time();utc=datetime.datetime.now(datetime.timezone.utc).isoformat();rev=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
base=ROOT/(f'sol61_push/cold_envelope_formation_2026_10_24/runs/{a.galaxy}_escape_long' if a.galaxy in ('draco','sextans') else f'sol61_push/cold_material_transport_2026_10_24/runs/{a.galaxy}_matched_L8');f=pathlib.Path(str(base)+'_fields.npz');jf=pathlib.Path(str(base)+'.json')
pins=[P/'late.py',P/'sphere_v3.py',P/'flux.py',P/'CONTRACT.md',P/'V2_CONTRACT.md',P/'V3_CONTRACT.md',P/'LATE_CHECK_CONTRACT.md',f,jf]
def hashes():return {str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in pins}
before=hashes();meta=json.loads(jf.read_text());ff=np.load(f);r,w,lm,v=[ff[k] for k in ['r','w','lm','initial']];units=meta['physical'];eta=units['eta_code'];parentM=float(np.sum(abs(v)**2));j=next(j for j,x in enumerate(lm) if tuple(x)==(0,0));valid=(r<21.8)&(abs(v[:,j])>1e-20);rv=r[valid];phase=CubicSpline(rv,eta*np.unwrap(np.angle(v[valid,j])))
def Sin(x,der=0):
 if der==1:return np.where(x<=rv[-1],phase(x,1),phase(rv[-1],1))
 return np.where(x<=rv[-1],phase(x),phase(rv[-1])+phase(rv[-1],1)*(x-rv[-1]))
s=Sphere(a.ne,a.nt,a.nf,eta=eta,phase=Sin);amp=v/(np.sqrt(w)*r)[:,None]*np.exp(-1j*Sin(r)/eta)[:,None];active=np.flatnonzero(np.max(abs(amp),axis=0)>1e-14);av=CubicSpline(r,amp[:,active],axis=0)(s.r);av[s.r>=r[-1]]=0
Y=np.array([sph_harm(lm[k,1],lm[k,0],s.phi[None,:],np.arccos(s.mu)[:,None]) for k in active]);u=np.einsum('rk,kij->rij',av,Y)*s.sr[:,None,None]*s.sa[None,:,:];pot=s.poisson(u);initial=s.moments(u,pot);m0=initial['M'];escale=max(initial['K']+abs(initial['W']),1e-12);history=[];cdfs=[];rg=np.linspace(0,24,481);status='finished requested finite interval';done=0
parentcdf=np.cumsum(np.sum(abs(v)**2,axis=1));transfer=float(np.max(abs(np.cumsum(np.sum(abs(u)**2,axis=(1,2)))-np.interp(s.r,r,parentcdf))))
def diag(t):
 h=s.moments(u,pot);m=abs(u)**2;h.update(t=t,elapsed_Myr=t*units['tunit_Myr'],E_relative_error=(h['E']-initial['E'])/escale,Jz_relative_error=(h['Jz']-initial['Jz'])/max(abs(initial['Jz']),eta*m0),field_aperture_Msun=h['M_inner']*units['Munit_Msun'],flux=flux(s,u,pot));history.append(h);cdfs.append(np.interp(rg,s.r,np.cumsum(m.sum(axis=(1,2)))));print(a.tag,t,h['E_relative_error'],h['angular_edge_fraction'],h['field_aperture_Msun'],flush=True);return h
h=diag(0)
if abs(m0/parentM-1)>.01:status='stopped initial mass transfer >1%'
else:
 for it in range(round(a.T/a.dt)):
  u,pot=s.step(u,pot,a.dt);done=(it+1)*a.dt
  if (it+1)%max(5,round(.1/a.dt))==0 or it+1==round(a.T/a.dt):
   h=diag(done)
   if abs(h['M']/m0-1)>1e-10:status='stopped mass conservation';break
   if abs(h['E_relative_error'])>.05:status='stopped energy drift >5%';break
   if abs(h['Jz_relative_error'])>.05:status='stopped Jz drift >5%';break
   if max(h['angular_edge_fraction'],h['azimuth_edge_fraction'])>.05:status='stopped angular edge >5%';break
   if h['boundary_fraction']>1e-4:status='stopped boundary mass >1e-4';break
   if time.time()-start>a.wall:status='stopped soft wall budget';break
if history[-1]['t']<done:diag(done)
out=dict(parameters=vars(a),started_utc=utc,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),interpreter=sys.executable,argv=sys.argv,software=dict(Python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),revision_before=rev,revision_after=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),inputs_before=before,inputs_after=hashes(),physical=units,finite_mass_transport=s.transport_mass.tolist(),finite_radial_matter_Jz_transport=s.transport_Jz.tolist(),transport_r=((s.r[1:]+s.r[:-1])/2).tolist(),scope='conditional CCT field; no action bridge, bound-remnant or stellar claim',initial_mass_relative_error=m0/parentM-1,initial_CDF_absolute_error=transfer,history=history,status=status,seconds=time.time()-start)
assert before==out['inputs_after'];dest=P/'runs';dest.mkdir(exist_ok=True);np.savez_compressed(dest/(a.tag+'.npz'),u=u,phi=pot,r=s.r,w=s.w,mu=s.mu,aw=s.aw,S=s.phase,physical_CDF_r=rg,physical_CDF=cdfs,times=[h['t'] for h in history]);out['peak_RSS_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;(dest/(a.tag+'.json')).write_text(json.dumps(out,indent=2)+'\n');print(status,out['peak_RSS_bytes'],flush=True)
