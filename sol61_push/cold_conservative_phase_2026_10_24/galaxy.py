"""Bounded actual saved-field pilots; all times in parent code units."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import argparse,datetime,hashlib,json,pathlib,platform,resource,subprocess,sys,time
import numpy as np,scipy
from scipy.interpolate import CubicSpline,RegularGridInterpolator
from scipy.special import sph_harm
from solver import Grid,Evolve
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1]
p=argparse.ArgumentParser();p.add_argument('--galaxy',required=True,choices=['draco','sextans','fornax','leoi']);p.add_argument('--late',action='store_true');p.add_argument('--n',type=int,default=48);p.add_argument('--box',type=float,default=28);p.add_argument('--dt',type=float,default=.02);p.add_argument('--T',type=float,default=10);p.add_argument('--wall',type=float,default=120);p.add_argument('--tag',required=True);a=p.parse_args()
assert not a.late or a.galaxy in ['draco','sextans']
start=time.time();utc=datetime.datetime.now(datetime.timezone.utc).isoformat();revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
if a.galaxy in ['draco','sextans']:parent=ROOT/f'sol61_push/cold_envelope_formation_2026_10_24/runs/{a.galaxy}_escape_long'
else:parent=ROOT/f'sol61_push/cold_material_transport_2026_10_24/runs/{a.galaxy}_matched_L8'
f=pathlib.Path(str(parent)+'_fields.npz');jf=pathlib.Path(str(parent)+'.json');meta=json.loads(jf.read_text());data=np.load(f);units=meta['physical'];eta=units['eta_code']
pins=[P/'solver.py',pathlib.Path(__file__),P/'CONTRACT.md',f,jf];track=None
if a.late:
 tf=ROOT/f'sol61_push/cold_moving_cores_2026_10_24/runs/{a.galaxy}_track_tracking.json';pins.append(tf);track=json.loads(tf.read_text())['history'][0]
def hashes():return {str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in pins}
before=hashes();g=Grid(a.n,a.box);r,w,lm=data['r'],data['w'],data['lm'];v=data['final' if a.late else 'initial'];mass_parent=float(np.sum(abs(v)**2));phase=np.zeros_like(r)
if not a.late:
 i0=next(i for i,x in enumerate(lm) if tuple(x)==(0,0));valid=(r<21.8)&(abs(v[:,i0])>1e-20);rv=r[valid];pv=np.unwrap(np.angle(v[valid,i0]));cs=CubicSpline(rv,pv,extrapolate=True);phase=cs(r)
 # Continue the carrier linearly outside the incoming support to avoid polynomial growth.
 phase[r>rv[-1]]=pv[-1]+cs(rv[-1],1)*(r[r>rv[-1]]-rv[-1])
 S=CubicSpline(r,eta*phase);speed=S(g.r,1);speed[g.r>rv[-1]]=eta*cs(rv[-1],1)
else:speed=np.zeros_like(g.r)
pfield=[speed*x/np.maximum(g.r,1e-20) for x in g.xyz]
amp=v/(np.sqrt(w)*r)[:,None]*np.exp(-1j*phase)[:,None];active=np.flatnonzero(np.max(abs(amp),axis=0)>1e-14)
spl=CubicSpline(r,amp[:,active],axis=0,extrapolate=True)
xyz=np.stack([x.ravel() for x in g.xyz],axis=1);rr=g.r.ravel();psi=np.zeros_like(rr,dtype=complex)
# Analytic continuous phase-fitted kinetic action from radial splines.
exact=np.zeros_like(psi)
for st in range(0,len(rr),4096):
 sl=slice(st,st+4096);rad=rr[sl];th=np.arccos(np.clip(xyz[sl,2]/rad,-1,1));ph=np.arctan2(xyz[sl,1],xyz[sl,0]);ls=lm[active,0];ms=lm[active,1];Y=sph_harm(ms[None,:],ls[None,:],ph[:,None],th[:,None]);av=spl(rad);ap=spl(rad,1);app=spl(rad,2);outside=rad>=r[-1];av[outside]=0;ap[outside]=0;app[outside]=0
 psi[sl]=np.sum(av*Y,axis=1)
 if not a.late:
  sp=S(rad,1);spp=S(rad,2);outer=rad>rv[-1];sp[outer]=eta*cs(rv[-1],1);spp[outer]=0
 else:sp=np.zeros_like(rad);spp=sp
 ev=-eta**2/2*(app+2*ap/rad[:,None]-ls[None,:]*(ls[None,:]+1)*av/rad[:,None]**2)-1j*eta*sp[:,None]*ap-.5j*eta*(spp+2*sp/rad)[:,None]*av+.5*sp[:,None]**2*av
 exact[sl]=np.sum(ev*Y,axis=1)
u=psi.reshape(g.r.shape)*g.sv;ev=Evolve(g,eta,pfield,a.dt);phi=g.poisson(abs(u)**2)
# Independent continuum-generator comparison, not an evolution calibration.
ha=ev.p2*u
for op in ev.ops:
 z=np.moveaxis(u,op.axis,0);h=op.diag*z;h[:-1]+=op.h*z[1:];h[1:]+=op.h.conj()*z[:-1];ha=ha+np.moveaxis(h,0,op.axis)
ex=exact.reshape(g.r.shape)*g.sv;generr=float(np.linalg.norm(ha-ex)/max(np.linalg.norm(ex),1e-30))
parentcdf=np.cumsum(np.sum(abs(v)**2,axis=1));ix=np.argsort(g.r.ravel());newcdf=np.cumsum(abs(u.ravel()[ix])**2);cdferr=float(np.max(abs(newcdf-np.interp(g.r.ravel()[ix],r,parentcdf))))
c=np.array(track['aperture_COM_code'] if track else [0,0,0]);velocity=np.array(track['aperture_velocity_code'] if track else [0,0,0]);dist=np.sqrt(sum((g.xyz[k]-c[k])**2 for k in range(3)));q=abs(u)**2*(dist<1);q0=float(q.sum());M0=float(np.sum(abs(u)**2));E0=ev.energy(u,phi);escale=max(abs(E0),sum(abs(o.expectation(u)) for o in ev.ops),1e-12)
# Paired passive stellar probes, only on late remnants. Not a live DF likelihood.
rng=np.random.default_rng(1012);stars=control=vs=vc=None;initialphi=phi.copy();probe=[]
cat=ROOT/'sol61_push/cold_survey_capture_2026_10_24/capture_results.json';pins.append(cat);before=hashes();name={'draco':'Draco','sextans':'Sextans','fornax':'Fornax','leoi':'Leo I'}[a.galaxy];model=next(x for x in json.loads(cat.read_text())['models'] if x['name']==name)
def accel(pos,field,center):
 gradients=np.gradient(field,g.x,g.x,g.x,edge_order=2);force=-np.stack([RegularGridInterpolator((g.x,g.x,g.x),h,bounds_error=False,fill_value=0)(pos) for h in gradients],axis=1)
 d=pos-center;rad=np.maximum(np.linalg.norm(d,axis=1),1e-10);G=.00430091;R=units['Runit_pc'];V=units['Vunit_kms'];aa=[434.24183348/R,794.188604/R] if a.galaxy=='sextans' else [1.];gn=sum(model['stellar_mass']/len(aa)/units['Munit_Msun']*rad/(rad*rad+b*b)**1.5 for b in aa);ac=9.3603e-11*3.085677581491367e10*R/V**2;gb=.5*(gn+np.sqrt(gn*gn+4*ac*gn));return force-gb[:,None]*d/rad[:,None]
if a.late:
 d=rng.normal(size=(64,3));d/=np.linalg.norm(d,axis=1)[:,None];z=(np.arange(64)+.5)/64*.85;rad=(z**(-2/3)-1)**(-.5);off=d*rad[:,None];off=np.concatenate([off,-off]);stars=c+off;control=stars.copy();force=accel(stars,phi,c);tang=np.cross(np.tile([0.,0.,1.],(128,1)),np.concatenate([d,-d]));tang/=np.linalg.norm(tang,axis=1)[:,None];speed0=np.sqrt(np.maximum(0,-np.sum(force*off,axis=1)));vs=velocity+tang*speed0[:,None];vc=vs.copy()
def phasebad(u):
 mass=abs(u)**2;bad=0.;den=0.
 for axis in range(3):
  z=np.moveaxis(u,axis,0);m=np.moveaxis(mass,axis,0);weight=(m[:-1]+m[1:])/2;bad+=np.sum(weight*(abs(np.angle(z[:-1].conj()*z[1:]))>np.pi/3));den+=weight.sum()
 return float(bad/den)
def row(t):
 mass=abs(u)**2;center=stars.mean(axis=0) if stars is not None else c;dd=np.sqrt(sum((g.xyz[k]-center[k])**2 for k in range(3)));sel=dd<1;tagcenter=[float(np.sum(q*g.xyz[k])/max(q.sum(),1e-30)) for k in range(3)]
 h=dict(t=t,M=float(mass.sum()),tag_mass=float(q.sum()),tag_min=float(q.min()),tag_excess=float(np.max(q-mass)),field_aperture_Msun=float(mass[sel].sum()*units['Munit_Msun']),tag_aperture_Msun=float(q[sel].sum()*units['Munit_Msun']),tag_COM=tagcenter,E=ev.energy(u,phi),phase_bad_fraction=phasebad(u),star_COM=center.tolist())
 if stars is not None:
  def obs(pos,vel):return dict(r50=float(np.median(np.linalg.norm(pos-pos.mean(axis=0),axis=1))),sigma=float(np.sqrt(np.mean((vel-vel.mean(axis=0))**2))))
  h['stars']=obs(stars,vs);h['control']=obs(control,vc)
 return h
history=[row(0)];status='finished requested finite interval';bond=0.
# These gates are numerical: never use a stopped endpoint as dwarf evidence.
if abs(M0/mass_parent-1)>.01:status='stopped initial mass transfer error >1%'
elif history[0]['phase_bad_fraction']>.05:status='stopped initial residual amplitude phase occupancy >5%'
elif generr>.1:status='stopped initial continuum generator mismatch >10%'
else:
 for it in range(round(a.T/a.dt)):
  t=it*a.dt
  if stars is not None:
   vs+=.5*a.dt*accel(stars,phi,stars.mean(axis=0));vc+=.5*a.dt*accel(control,initialphi,control.mean(axis=0));stars+=a.dt*vs;control+=a.dt*vc
  u,q,phi,e=ev.step(u,q,phi);bond=max(bond,e)
  if stars is not None:
   vs+=.5*a.dt*accel(stars,phi,stars.mean(axis=0));vc+=.5*a.dt*accel(control,initialphi,control.mean(axis=0))
  if (it+1)%5==0 or it+1==round(a.T/a.dt):
   h=row(t+a.dt);history.append(h)
   assert h['tag_min']>-1e-10 and h['tag_excess']<1e-10 and abs(h['tag_mass']-q0)<1e-10 and abs(h['M']-M0)<1e-10
   if h['phase_bad_fraction']>.05:status='stopped residual amplitude phase occupancy >5%';break
   if abs(h['E']-E0)/escale>.05:status='stopped energy ledger >5%';break
   if time.time()-start>a.wall:status='stopped wall budget';break
out=dict(parameters=vars(a),scope='finite CCT phase-fitted candidate; passive paired probes; no live stars, host or infinity escape claim',started_utc=utc,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=sys.argv,software=dict(Python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),revision_before=revision,revision_after=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),physical=units,parent_mass=mass_parent,initial_mass_relative_error=M0/mass_parent-1,initial_CDF_absolute_error=cdferr,initial_generator_relative_error=generr,history=history,status=status,bond_residual=bond,energy_scale=escale,energy_relative_error=(history[-1]['E']-E0)/escale,inputs_before=before,inputs_after=hashes(),seconds=time.time()-start)
assert before==out['inputs_after'];dest=P/'runs';dest.mkdir(exist_ok=True);np.savez_compressed(dest/(a.tag+'.npz'),u=u,q=q,x=g.x,phi=phi,stars=stars if stars is not None else np.empty(0));out['peak_RSS_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;(dest/(a.tag+'.json')).write_text(json.dumps(out,indent=2)+'\n');print(a.tag,status,'T',history[-1]['t'],'masserr',out['initial_mass_relative_error'],'generr',generr,'phase',history[-1]['phase_bad_fraction'],'RSS',out['peak_RSS_bytes'],flush=True)
