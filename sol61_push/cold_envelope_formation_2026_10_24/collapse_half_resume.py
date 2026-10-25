"""Coherent isolated collapse with nonaxisymmetric high-l transfer; CCT-009."""
import argparse,hashlib,json,math,pathlib,resource,time,subprocess
import numpy as np
from scipy.linalg.lapack import zgttrf,zgttrs
from angular_half import Angular
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1]
p=argparse.ArgumentParser();p.add_argument('--resume',default=None);p.add_argument('--galaxy',choices=['Draco','Sextans','Fornax','Leo I'],required=True);p.add_argument('--tag',required=True)
p.add_argument('--nr',type=int,default=384);p.add_argument('--lmax',type=int,default=12);p.add_argument('--mmax',type=int,default=4);p.add_argument('--dt',type=float,default=.02);p.add_argument('--T',type=float,default=40);p.add_argument('--rmax',type=float,default=28);p.add_argument('--absorb',type=float,default=16);p.add_argument('--gamma',type=float,default=1);p.add_argument('--eta',type=float,default=1500);p.add_argument('--gas',choices=['cycle','none'],default='cycle');p.add_argument('--seed',type=float,default=.01);a=p.parse_args()
source=ROOT/'sol61_push/cold_survey_capture_2026_10_24/capture_results.json';obsfile=ROOT/'sol61_push/cold_data_constraints_2026_10_24/results.json';targetfile=ROOT/'sol61_push/cold_envelope_spectrum_2026_10_24/eta1500_refine.json'
gal=next(g for g in json.loads(source.read_text())['models'] if g['name']==a.galaxy);obs=json.loads(obsfile.read_text())['galaxies'][a.galaxy]['observations'];tar=next(g for g in json.loads(targetfile.read_text())['results'] if g['name']==a.galaxy)
targetnpz=targetfile.parent/f'eta1500_refine_{a.galaxy.replace(" ","")}.npz'
pins=[pathlib.Path(__file__),P/'angular_half.py',P/'CONTRACT.md',source,obsfile,targetfile,targetnpz]
def hashes():return {str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in pins}

if a.resume:
 parent=P/'runs'/(a.resume+'.json');parentfields=P/'runs'/(a.resume+'_fields.npz');pins.extend([parent,parentfields,P/'collapse.py'])
before=hashes();G=.00430091;M=5.364*200*gal['formed_mass'];R=float(obs['rhalf_sph_physical']);V=math.sqrt(G*M/R);eta=a.eta/(R*V);tunit=.977792*R/V
inner=a.nr//3;r=np.r_[np.geomspace(1e-4,1,inner,endpoint=False),np.linspace(1,a.rmax,a.nr-inner+1)[:-1]]
hl=np.diff(np.r_[0,r]);hr=np.diff(np.r_[r,a.rmax]);w=(hl+hr)/2
base_diag=.5*eta*eta*(1/hl+1/hr)/w;off=-.5*eta*eta/(hr[:-1]*np.sqrt(w[:-1]*w[1:]))
ang=Angular(a.lmax,a.mmax,r,w);lm=ang.field.lm;ms=ang.m;nm=len(lm);groups=[]
for l in range(a.lmax+1):
 ix=np.array([j for j,(ll,m) in enumerate(lm) if ll==l]);td=base_diag+.5*eta*eta*l*(l+1)/r**2;c=1j*a.dt/(4*eta);fact=zgttrf(c*off,1+c*td,c*off);assert fact[-1]==0;groups.append((ix,td,fact[:-1]))
def K(v):
 total=0
 for ix,td,fact in groups:
  z=v[:,ix];total+=np.sum(td[:,None]*abs(z)**2)+2*np.real(np.sum(off[:,None]*z[:-1].conj()*z[1:]))
 return float(total)
def kinetic(v):
 out=np.empty_like(v);c=1j*a.dt/(4*eta)
 for ix,td,fact in groups:
  z=v[:,ix];rhs=(1-c*td[:,None])*z;rhs[:-1]-=c*off[:,None]*z[1:];rhs[1:]-=c*off[:,None]*z[:-1];out[:,ix],info=zgttrs(*fact,np.asfortranarray(rhs));assert info==0
 return out
def gas(t):
 if a.gas=='none':return np.zeros_like(r)
 ag=5 if t<=4 else 3+2*math.cos(math.pi*(t-4)/6) if t<10 else 1
 f=1 if t<=16 else .5*(1+math.cos(math.pi*(t-16)/8)) if t<24 else 0
 return -f/5.364/np.sqrt(r*r+ag*ag)
def E(v,pg):
 W=ang.self_energy(v);return K(v)+W+float(np.sum(abs(v)**2*pg[:,None]))
def J(v):return float(eta*np.sum(abs(v)**2*ms[None,:]))
v=np.zeros((len(r),nm),complex);rad=r*np.exp(-r*r/32)*np.exp(-1j*(10/V)/eta*np.sqrt(r*r+.04));rad*=np.where(r<=18,1,np.where(r<22,np.cos(np.pi*(r-18)/8)**4,0))
v[:,lm.index((0,0))]=rad
for m,c in [(2,.5),(-2,.15*np.exp(1j*np.pi/3)),(0,.2)]:v[:,lm.index((2,m))]=c*(r/4)**2*rad
v[:,lm.index((3,0))]=a.seed*(r/4)**3*rad
v*=np.sqrt(w)[:,None];v/=np.linalg.norm(v);v0=v.copy();rem={'M':0.,'E':0.,'Jz':0.};work=epos=eneg=0.;hist=[];start=time.time();pg=gas(0);status='finished'
damp=np.exp(-a.dt*a.gamma*(np.maximum(r-a.absorb,0)/(a.rmax-a.absorb))**4)
def diagnostics(t,v,pg):
 shell=np.sum(abs(v)**2,axis=1);cdf=np.cumsum(shell);modes=np.sum(abs(v)**2,axis=0);high=float(sum(z for z,(l,m) in zip(modes,lm) if l>4));edge=float(sum(z for z,(l,m) in zip(modes,lm) if l>=a.lmax-1));medge=float(sum(z for z,(l,m) in zip(modes,lm) if abs(m)==a.mmax));u=v/np.sqrt(w)[:,None];flux=eta*np.imag(np.sum(u.conj()*np.gradient(u,r,axis=0),axis=1));ix=int(np.argmin(abs(r-.85*a.absorb)))
 return dict(t=t,M=float(sum(shell)),E=E(v,pg),K=K(v),Jz=J(v),Jx=0.,Jy=0.,M_inner=float(sum(shell[r<1])),rhalf=float(np.interp(sum(shell)/2,cdf,r)),l_gt4_mass=high,l_edge_mass=edge,m_edge_mass=medge,cdf=cdf.tolist(),mode_mass=modes.tolist(),source_work=work,removed=dict(rem),positive_sink_E=epos,negative_sink_E=eneg,outward_mass_flux=float(flux[ix]),flux_radius=float(r[ix]))
h0=diagnostics(0,v,pg);hist.append(h0);tstart=0.;energy_scale=max(abs(h0['E']),1e-12)
if a.resume:
 prior=json.loads(parent.read_text());pf=np.load(parentfields)
 for key in ['galaxy','nr','lmax','mmax','rmax','absorb','gamma','eta','gas','seed']:
  assert vars(a)[key]==prior['parameters'][key],key
 v=pf['final'].copy();v0=pf['initial'].copy();hist=prior['history'];h0=prior['initial'];last=hist[-1];tstart=last['t'];rem=last['removed'].copy();work=last['source_work'];epos=last['positive_sink_E'];eneg=last['negative_sink_E'];pg=gas(tstart)
 energy_scale=prior.get('energy_ledger_scale_code',max(abs(h0['E']),1e-12))
 assert tstart<a.T
nstep=round((a.T-tstart)/a.dt)
for it in range(nstep):
 t=tstart+it*a.dt;pm=gas(t+a.dt/2);pn=gas(t+a.dt);work+=float(np.sum(abs(v)**2*(pm-pg)[:,None]));v=kinetic(v)
 pang,_,_=ang.potential(v);pang+=pm[:,None,None];mid=ang.exp(v,pang,a.dt/2,eta);pang,_,_=ang.potential(mid);pang+=pm[:,None,None];v=ang.exp(v,pang,a.dt,eta);v=kinetic(v)
 work+=float(np.sum(abs(v)**2*(pn-pm)[:,None]));pg=pn
 m0=float(np.linalg.norm(v)**2);j0=J(v);e0=E(v,pg);v*=damp[:,None];m1=float(np.linalg.norm(v)**2);j1=J(v);e1=E(v,pg)
 rem['M']+=m0-m1;rem['Jz']+=j0-j1;rem['E']+=e0-e1;epos+=max(0,e0-e1);eneg+=min(0,e0-e1)
 if (it+1)%25==0 or it+1==nstep:
  h=diagnostics(t+a.dt,v,pg);h['M_residual']=h['M']+rem['M']-h0['M'];h['E_residual']=(h['E']+rem['E']-work-h0['E'])/energy_scale;h['J_residual']=(h['Jz']+rem['Jz']-h0['Jz'])/max(abs(h0['Jz']),1e-12);hist.append(h)
  if abs(h['E_residual'])>.05 or abs(h['J_residual'])>.05:status='stopped numerical ledger >5%';break
  if (it+1)%250==0:print(a.tag,'t',round(h['t'],2),'M',round(h['M'],5),'high-l',round(h['l_gt4_mass'],5),'edge-l',round(h['l_edge_mass'],5),'Eres',round(h['E_residual'],6),flush=True)
# Constructed endpoint Hamiltonian: subtract target mean potential once from summed eigenenergies.
z=np.load(targetnpz);s=z['shell_mass_fraction'];bm=gal['cold_scale_pc'];q=gal['stellar_mass']/gal['cold_mass'];aa=R/bm;bpot=-q/np.sqrt(z['x']**2+aa**2)
if a.galaxy=='Sextans':bpot=-q/2*(1/np.sqrt(z['x']**2+(434.2418/bm)**2)+1/np.sqrt(z['x']**2+(794.1886/bm)**2))
pctarget=-1/np.sqrt(1+z['x']**2);kin=float(z['occupation']@z['energy']-np.sum(s*(pctarget+bpot)));efinal=(kin+np.sum(s*bpot)+.5*np.sum(s*z['fitted_cold_potential']))*G*gal['cold_mass']**2/bm
out=dict(parameters=vars(a),physical=dict(Munit_Msun=M,Runit_pc=R,Vunit_kms=V,tunit_Myr=tunit,eta_code=eta),angular_modes=lm,radial_grid=r.tolist(),radial_weights=w.tolist(),initial=h0,history=hist,status=status,seconds=time.time()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,source_hashes_before=before,source_hashes_after=hashes(),revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),energy_ledger_scale_code=energy_scale,target_energy_Msun_kms2=efinal,initial_energy_Msun_kms2=h0['E']*M*V*V,initial_minus_target_energy_Msun_kms2=h0['E']*M*V*V-efinal)
assert before==out['source_hashes_after'];(P/'runs').mkdir(exist_ok=True);(P/'runs'/f'{a.tag}.json').write_text(json.dumps(out,indent=2)+'\n');np.savez_compressed(P/'runs'/f'{a.tag}_fields.npz',initial=v0,final=v,r=r,w=w,lm=lm);print(a.tag,status,'seconds',out['seconds'],'RSS',out['peak_RSS_bytes'],flush=True)
