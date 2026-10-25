"""Fresh incoming galaxy lens pilots. No stars or retained-bound-mass claim."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import argparse,datetime,hashlib,json,pathlib,platform,resource,subprocess,sys,time
import numpy as np,scipy
from scipy.interpolate import CubicSpline
from scipy.special import sph_harm
from lens import Grid,Lens
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1]
p=argparse.ArgumentParser();p.add_argument('--galaxy',choices=['draco','sextans','fornax','leoi'],required=True);p.add_argument('--n',type=int,default=64);p.add_argument('--box',type=float,default=40);p.add_argument('--beta',type=float,default=.1);p.add_argument('--dt',type=float,default=.02);p.add_argument('--T',type=float,default=6);p.add_argument('--wall',type=float,default=150);p.add_argument('--tag',required=True);args=p.parse_args()
started=time.time();utc=datetime.datetime.now(datetime.timezone.utc).isoformat();revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
if args.galaxy in ('draco','sextans'):parent=ROOT/f'sol61_push/cold_envelope_formation_2026_10_24/runs/{args.galaxy}_escape_long'
else:parent=ROOT/f'sol61_push/cold_material_transport_2026_10_24/runs/{args.galaxy}_matched_L8'
f=pathlib.Path(str(parent)+'_fields.npz');jf=pathlib.Path(str(parent)+'.json');oldsolver=P.parent/'cold_conservative_phase_2026_10_24/solver.py';pins=[P/'galaxy.py',P/'lens.py',oldsolver,P/'CONTRACT.md',P/'PLAN.md',f,jf]
def hashes():return {str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in pins}
before=hashes();meta=json.loads(jf.read_text());fields=np.load(f);units=meta['physical'];eta=units['eta_code'];r,w,lm,v=[fields[k] for k in ['r','w','lm','initial']];parentM=float(np.sum(abs(v)**2));g=Grid(args.n,args.box)
j=next(i for i,x in enumerate(lm) if tuple(x)==(0,0));valid=(r<21.8)&(abs(v[:,j])>1e-20);rv=r[valid];pv=np.unwrap(np.angle(v[valid,j]));Sin=CubicSpline(rv,eta*pv)
def phase(rad):return np.where(rad<=rv[-1],Sin(rad),Sin(rv[-1])+Sin(rv[-1],1)*(rad-rv[-1]))
def speed(rad):return np.where(rad<=rv[-1],Sin(rad,1),Sin(rv[-1],1))
phase_r=phase(r);amp=v/(np.sqrt(w)*r)[:,None]*np.exp(-1j*phase_r/eta)[:,None];active=np.flatnonzero(np.max(abs(amp),axis=0)>1e-14);spl=CubicSpline(r,amp[:,active],axis=0)
xyz=np.stack([q.ravel() for q in g.xyz],axis=1);rr=g.r.ravel();A=np.zeros_like(rr,dtype=complex)
for st in range(0,len(rr),4096):
 sl=slice(st,st+4096);rad=rr[sl];th=np.arccos(np.clip(xyz[sl,2]/rad,-1,1));ph=np.arctan2(xyz[sl,1],xyz[sl,0]);Y=sph_harm(lm[active,1][None,:],lm[active,0][None,:],ph[:,None],th[:,None]);av=spl(rad);av[rad>=r[-1]]=0;A[sl]=np.sum(av*Y,axis=1)
u=A.reshape(g.r.shape)*g.sv;del A,xyz
pbase=[speed(g.r)*q/g.r for q in g.xyz];p0=[pbase[k]+args.beta*g.xyz[k] for k in range(3)];ev=Lens(g,eta,p0,args.beta);phi=ev.potential(u);q=abs(u)**2*(g.r<1);m0=float(np.sum(abs(u)**2));q0=float(q.sum());h0=ev.moments(u,phi,0);energy_scale=max(abs(h0['K'])+abs(h0['W']),1e-12);Jscale=max(np.linalg.norm(h0['J']),1e-12)
# Frozen-field initial-rate invariance is an algebraic check independent of evolution.
# T(p+beta y)=T(p)+beta D_A+beta int m y.p+beta² I/2.
m=abs(u)**2;D0=h0['D_chi']-args.beta*h0['I_chi'];T0=sum(op.expectation(u) for op in ev.ops)+float(np.sum(m*ev.p2));T_unshift=T0-args.beta*D0-.5*args.beta**2*h0['I_chi'];T_static=float(.5*np.sum(m*sum(vv*vv for vv in pbase)))
for k,op in enumerate(ev.ops):
 z=np.moveaxis(u,k,0);yy=np.moveaxis(g.xyz[k],k,0);den=(2*np.sqrt(g.w[:-1]*g.w[1:])).reshape((-1,1,1));hstatic=op.h+1j*eta*args.beta*(yy[:-1]+yy[1:])/2/den
 T_static+=float(np.sum(op.diag*abs(z)**2)+2*np.real(np.sum(z[:-1].conj()*hstatic*z[1:])))
gauge_E_residual=h0['E']-(T_static+h0['W'])
assert abs(gauge_E_residual)<1e-10
parentcdf=np.cumsum(np.sum(abs(v)**2,axis=1));idx=np.argsort(g.r.ravel());cdf0=np.cumsum(m.ravel()[idx]);transfer_cdf=float(np.max(abs(cdf0-np.interp(g.r.ravel()[idx],r,parentcdf))));physical_grid=np.linspace(0,24,241);history=[];cdfs=[]
def diagnose(t):
 h=ev.moments(u,phi,t);a=h['a'];m=abs(u)**2;bad=den=0.
 for k in range(3):
  z=np.moveaxis(u,k,0);mass=np.moveaxis(m,k,0);weight=(mass[:-1]+mass[1:])/2;bad+=np.sum(weight*(abs(np.angle(z[:-1].conj()*z[1:]))>np.pi/3));den+=weight.sum()
 sel=a*g.r<1;h.update(t=t,elapsed_Myr=t*units['tunit_Myr'],phase_bad_fraction=float(bad/den),boundary_fraction=float(m[g.r>.8*args.box].sum()/m0),E_relative_error=(h['E']-h0['E'])/energy_scale,J_relative_error=float(np.linalg.norm(np.array(h['J'])-h0['J'])/Jscale),tag_mass=float(q.sum()),tag_min=float(q.min()),tag_excess=float(np.max(q-m)),field_aperture_Msun=float(m[sel].sum()*units['Munit_Msun']),tag_aperture_Msun=float(q[sel].sum()*units['Munit_Msun']))
 cdf=np.cumsum(m.ravel()[idx]);cdfs.append(np.interp(physical_grid,a*g.r.ravel()[idx],cdf));history.append(h);return h
h=diagnose(0);status='finished requested finite interval';bond=0.
if abs(m0/parentM-1)>.01:status='stopped initial mass transfer >1%'
elif h['phase_bad_fraction']>.05:status='stopped initial amplitude edge phase >5%'
else:
 for it in range(round(args.T/args.dt)):
  t=it*args.dt
  if ev.scale(t+args.dt)[0]<.35:status='stopped scale safety gate';break
  u,q,phi,e=ev.step(u,q,phi,t,args.dt);bond=max(bond,e)
  if (it+1)%5==0 or it+1==round(args.T/args.dt):
   h=diagnose(t+args.dt)
   assert abs(h['M']-m0)<1e-10 and abs(h['tag_mass']-q0)<1e-10 and h['tag_min']>-1e-10 and h['tag_excess']<1e-10
   if h['phase_bad_fraction']>.05:status='stopped amplitude edge phase >5%';break
   if h['boundary_fraction']>1e-4:status='stopped moving boundary envelope mass >1e-4';break
   if abs(h['E_relative_error'])>.05:status='stopped physical energy drift >5%';break
   if time.time()-started>args.wall:status='stopped soft wall budget';break
out=dict(parameters=vars(args),started_utc=utc,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),interpreter=sys.executable,argv=sys.argv,software=dict(Python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),revision_before=revision,revision_after=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),inputs_before=before,inputs_after=hashes(),physical=units,scope='incoming prestellar lens-coordinate closed-box CCT candidate; no bound remnant or stars',initial_mass_relative_error=m0/parentM-1,initial_CDF_absolute_error=transfer_cdf,initial_gauge_energy_identity_residual=gauge_E_residual,parent_Jz=meta['initial']['Jz'],history=history,bond_residual=bond,status=status,seconds=time.time()-started)
assert out['inputs_before']==out['inputs_after'];dest=P/'runs';dest.mkdir(exist_ok=True);np.savez_compressed(dest/(args.tag+'.npz'),u=u,q=q,phi_y=phi,x=g.x,a=history[-1]['a'],physical_CDF_r=physical_grid,physical_CDF=np.array(cdfs),times=[h['t'] for h in history]);out['peak_RSS_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;(dest/(args.tag+'.json')).write_text(json.dumps(out,indent=2)+'\n');print(args.tag,status,'t',history[-1]['t'],'E',history[-1]['E_relative_error'],'phase',history[-1]['phase_bad_fraction'],'edge',history[-1]['boundary_fraction'],'RSS',out['peak_RSS_bytes'],flush=True)
