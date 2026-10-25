"""Actual incoming fields in adaptive radial gauge; physical force unchanged."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import argparse,datetime,hashlib,json,pathlib,platform,resource,subprocess,sys,time
import numpy as np,scipy
from scipy.interpolate import CubicSpline
from scipy.special import sph_harm
from adaptive import Grid,Radial,Adaptive
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1]
p=argparse.ArgumentParser();p.add_argument('--galaxy',choices=['draco','sextans','fornax','leoi'],required=True);p.add_argument('--n',type=int,default=64);p.add_argument('--nr',type=int,default=1025);p.add_argument('--dt',type=float,default=.02);p.add_argument('--T',type=float,default=6);p.add_argument('--wall',type=float,default=240);p.add_argument('--tag',required=True);a=p.parse_args()
start=time.time();utc=datetime.datetime.now(datetime.timezone.utc).isoformat();rev=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
parent=ROOT/(f'sol61_push/cold_envelope_formation_2026_10_24/runs/{a.galaxy}_escape_long' if a.galaxy in ('draco','sextans') else f'sol61_push/cold_material_transport_2026_10_24/runs/{a.galaxy}_matched_L8')
f=pathlib.Path(str(parent)+'_fields.npz');jf=pathlib.Path(str(parent)+'.json');pins=[P/'galaxy.py',P/'adaptive.py',P/'CONTRACT.md',P.parent/'cold_lens_phase_2026_10_25/lens.py',P.parent/'cold_conservative_phase_2026_10_24/solver.py',f,jf]
def hashes():return {str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in pins}
before=hashes();meta=json.loads(jf.read_text());ff=np.load(f);r,w,lm,v=[ff[k] for k in ['r','w','lm','initial']];units=meta['physical'];eta=units['eta_code'];parentM=float(np.sum(abs(v)**2));g=Grid(a.n,28);rad=Radial(g,a.nr)
j=next(j for j,x in enumerate(lm) if tuple(x)==(0,0));valid=(r<21.8)&(abs(v[:,j])>1e-20);rv=r[valid];phase=CubicSpline(rv,eta*np.unwrap(np.angle(v[valid,j])))
def Sin(x):return np.where(x<=rv[-1],phase(x),phase(rv[-1])+phase(rv[-1],1)*(x-rv[-1]))
amp=v/(np.sqrt(w)*r)[:,None]*np.exp(-1j*Sin(r)/eta)[:,None];active=np.flatnonzero(np.max(abs(amp),axis=0)>1e-14);spl=CubicSpline(r,amp[:,active],axis=0);rr=g.r.ravel();coords=np.stack([x.ravel() for x in g.xyz],axis=1);avalue=np.zeros_like(rr,dtype=complex)
for st in range(0,len(rr),4096):
 sl=slice(st,st+4096);radius=rr[sl];th=np.arccos(np.clip(coords[sl,2]/radius,-1,1));ph=np.arctan2(coords[sl,1],coords[sl,0]);Y=sph_harm(lm[active,1][None,:],lm[active,0][None,:],ph[:,None],th[:,None]);av=spl(radius);av[radius>=r[-1]]=0;avalue[sl]=np.sum(av*Y,axis=1)
ev=Adaptive(g,eta,rad,Sin(rad.R));u=avalue.reshape(g.r.shape)*g.sv*np.exp(1j*(Sin(g.r)-ev.value)/eta);del avalue,coords
q=abs(u)**2*(g.r<1);phi=ev.potential(u);initial=ev.moments(u,phi);m0=initial['M'];q0=float(q.sum());escale=max(initial['K']+abs(initial['W']),1e-12);jscale=max(np.linalg.norm(initial['J']),1e-12);gsigned=gabs=bond=0.;maxsub=0;history=[];cdfs=[];idx=np.argsort(g.r.ravel());rg=np.linspace(0,24,241)
parentcdf=np.cumsum(np.sum(abs(v)**2,axis=1));transferCDF=float(np.max(abs(np.cumsum(abs(u.ravel()[idx])**2)-np.interp(g.r.ravel()[idx],r,parentcdf))))
def diag(t):
 h=ev.moments(u,phi);m=abs(u)**2;bad=den=0.
 for k in range(3):
  z=np.moveaxis(u,k,0);mm=np.moveaxis(m,k,0);weight=(mm[:-1]+mm[1:])/2;bad+=np.sum(weight*(abs(np.angle(z[:-1].conj()*z[1:]))>np.pi/3));den+=weight.sum()
 sel=g.r<1;h.update(t=t,elapsed_Myr=t*units['tunit_Myr'],phase_bad_fraction=float(bad/den),boundary_fraction=float(m[g.r>.8*28].sum()/m0),E_relative_error=(h['E']-initial['E'])/escale,J_relative_error=float(np.linalg.norm(np.array(h['J'])-initial['J'])/jscale),gauge_signed_relative=gsigned/escale,gauge_absolute_relative=gabs/escale,tag_mass=float(q.sum()),tag_min=float(q.min()),tag_excess=float(np.max(q-m)),field_aperture_Msun=float(m[sel].sum()*units['Munit_Msun']),tag_aperture_Msun=float(q[sel].sum()*units['Munit_Msun']))
 history.append(h);cdfs.append(np.interp(rg,g.r.ravel()[idx],np.cumsum(m.ravel()[idx])));return h
h=diag(0);completed_t=0.;status='finished requested finite interval'
if abs(m0/parentM-1)>.01:status='stopped initial mass transfer >1%'
elif h['phase_bad_fraction']>.05:status='stopped initial amplitude edge phase >5%'
else:
 for it in range(round(a.T/a.dt)):
  try:u,q,phi,d=ev.step(u,q,phi,it*a.dt,a.dt)
  except RuntimeError as exc:status='stopped '+str(exc);break
  completed_t=(it+1)*a.dt;gsigned+=d['gauge_signed'];gabs+=d['gauge_absolute'];bond=max(bond,d['bond']);maxsub=max(maxsub,d['HJ_substeps'])
  if (it+1)%5==0 or it+1==round(a.T/a.dt):
   h=diag((it+1)*a.dt)
   assert abs(h['M']-m0)<1e-10 and abs(h['tag_mass']-q0)<1e-10 and h['tag_min']>-1e-10 and h['tag_excess']<1e-10
   if h['phase_bad_fraction']>.05:status='stopped amplitude edge phase >5%';break
   if h['gauge_absolute_relative']>.05:status='stopped absolute gauge energy defect >5%';break
   if abs(h['E_relative_error'])>.05:status='stopped physical energy drift >5%';break
   if h['boundary_fraction']>1e-4:status='stopped boundary envelope mass >1e-4';break
   if time.time()-start>a.wall:status='stopped soft wall budget';break
if history[-1]['t']<completed_t:diag(completed_t)
out=dict(parameters=vars(a),started_utc=utc,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),interpreter=sys.executable,argv=sys.argv,software=dict(Python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),revision_before=rev,revision_after=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),inputs_before=before,inputs_after=hashes(),physical=units,scope='same incoming physical CCT fields, adaptive radial carrier only; no retained-bound mass or stars',initial_mass_relative_error=m0/parentM-1,initial_CDF_absolute_error=transferCDF,parent_Jz=meta['initial']['Jz'],history=history,status=status,bond_residual=bond,max_HJ_substeps=maxsub,seconds=time.time()-start)
assert before==out['inputs_after'];dest=P/'runs';dest.mkdir(exist_ok=True);np.savez_compressed(dest/(a.tag+'.npz'),u=u,q=q,phi=phi,x=g.x,reference_R=rad.R,S=ev.S,physical_CDF_r=rg,physical_CDF=np.array(cdfs),times=[h['t'] for h in history]);out['peak_RSS_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;(dest/(a.tag+'.json')).write_text(json.dumps(out,indent=2)+'\n');print(a.tag,status,'t',history[-1]['t'],'E',history[-1]['E_relative_error'],'gauge',history[-1]['gauge_absolute_relative'],'phase',history[-1]['phase_bad_fraction'],'RSS',out['peak_RSS_bytes'],flush=True)
