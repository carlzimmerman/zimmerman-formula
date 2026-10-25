import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import datetime,hashlib,json,pathlib,resource,subprocess,sys,time,numpy as np,scipy
from scipy.interpolate import CubicSpline
Q=pathlib.Path(__file__).resolve().parent;ROOT=Q.parents[1];P=Q.parent/'cold_resolved_pulse_2026_10_25';sys.path.insert(0,str(P))
from memory_gauss_v2 import Sphere
from lean import OLD
from budget import initial
start=time.time();rev=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();utc=datetime.datetime.now(datetime.timezone.utc).isoformat();paths={g:ROOT/(f'sol61_push/cold_envelope_formation_2026_10_24/runs/{g}_escape_long' if g in ['draco','sextans'] else f'sol61_push/cold_material_transport_2026_10_24/runs/{g}_matched_L8') for g in ['draco','sextans','fornax','leoi']};pins=[Q/'assembly_screen.py',Q/'ASSEMBLY_SCREEN_CONTRACT.md']+[P/x for x in ['memory_gauss_v2.py','memory_gauss.py','gauss.py','lean.py']]+[OLD/x for x in ['sphere_v3.py','budget.py']]+[pathlib.Path(str(b)+s) for b in paths.values() for s in ['.json','_fields.npz']]
def hashes():return {str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in pins}
before=hashes();rows=[]
for ne in [128,256]:
 for g,base in paths.items():
  meta=json.loads(pathlib.Path(str(base)+'.json').read_text());units=meta['physical'];eta=units['eta_code'];raw=np.load(str(base)+'_fields.npz');r,v,lm=[raw[k] for k in ['r','initial','lm']];k=next(j for j,z in enumerate(lm) if tuple(z)==(0,0));good=(r<21.8)&(abs(v[:,k])>1e-20);rv=r[good];sp=CubicSpline(rv,eta*np.unwrap(np.angle(v[good,k])))
  def phase(x,der=0):
   if der:return np.where(x<=rv[-1],sp(x,1),sp(rv[-1],1))
   return np.where(x<=rv[-1],sp(x),sp(rv[-1])+sp(rv[-1],1)*(x-rv[-1]))
  s0=Sphere(ne,24,32,eta=eta);s1=Sphere(ne,24,32,eta=eta,phase=phase);u=initial(s1,raw);M=float(np.vdot(u,u).real);sourceM=float(np.sum(abs(v)**2));assert abs(M/sourceM-1)<.01;phi=s0.poisson(u);W=.5*float(np.sum(abs(u)**2*phi));C=float(np.vdot(u,s0.radial_apply(u)).real+np.vdot(u,s0.angular(u,0,True)).real);A=.5*float(np.sum(abs(u)**2*s1.p[:,None,None]**2));Hcross=s1.H-s0.H-np.diag(.5*s1.p*s1.p);cross=Hcross.diagonal()[:,None,None]*u
  for off in [1,2,3]:
   h=np.diag(Hcross,off);cross[:-off]+=h[:,None,None]*u[off:];cross[off:]+=h.conj()[:,None,None]*u[:-off]
  B=float(np.vdot(u,cross).real);b=np.fft.fft(u,axis=2,norm='ortho');Jz=float(eta*np.sum(abs(b)**2*s0.m[None,None,:]));roots=np.roots([A,B,C+W]);realroots=sorted(float(z.real) for z in roots if abs(z.imag)<1e-10 and 0<=z.real<=1.5);row=dict(galaxy=g,ne=ne,M=M,source_M=sourceM,mass_transfer_relative=M/sourceM-1,Jz=Jz,A=A,B=B,C=C,W=W,energy_at_original_infall=A+B+C+W,energy_at_zero_carrier=C+W,roots_in_domain=realroots,physical=units);rows.append(row);print(g,ne,'root',realroots,'E0/E1',C+W,A+B+C+W,flush=True);del raw,u,v,phi,b,s0,s1,Hcross,cross
intervals=[]
for ne in [128,256]:
 rr=[x for x in rows if x['ne']==ne];edges=sorted(set([0.,1.5]+[z for x in rr for z in x['roots_in_domain']]));parts=[]
 for a,b in zip(edges[:-1],edges[1:]):
  t=(a+b)/2;signs={x['galaxy']:x['A']*t*t+x['B']*t+x['C']+x['W'] for x in rr};desired=all(signs[g]<0 for g in ['draco','sextans']) and all(signs[g]>=0 for g in ['fornax','leoi']);parts.append(dict(lower=a,upper=b,test_lambda=t,energies=signs,desired_initial_energy_selector=desired))
 assert all(x['A']>0 and x['C']+x['W']<0 and len(x['roots_in_domain'])==1 for x in rr)
 rmap={x['galaxy']:x['roots_in_domain'][0] for x in rr};gap=min(rmap[g] for g in ['draco','sextans'])-max(rmap[g] for g in ['fornax','leoi']);intervals.append(dict(ne=ne,root_gap=gap,open_intervals=parts,desired_intervals=[x for x in parts if x['desired_initial_energy_selector']],endpoint_scope='A>0,E(0)<0,one positive root: desired common interval iff root_gap>0; equality cannot satisfy strict D/S negativity'))
out=dict(scope='initial whole-wave energy-sign screen only; not dynamical capture or a derived history',parameters=dict(lambda_domain=[0,1.5],ne=[128,256],nt=24,nf=32),rows=rows,intervals=intervals,inputs_before=before,inputs_after=hashes(),started_utc=utc,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),revision_before=rev,revision_after=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),argv=sys.argv,interpreter=sys.executable,software=dict(Python=sys.version,numpy=np.__version__,scipy=scipy.__version__),seconds=time.time()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,status='completed declared finite screen');assert before==out['inputs_after'] and out['peak_RSS_bytes']<750_000_000;f=Q/'assembly_screen.json';assert not f.exists();f.write_text(json.dumps(out,indent=2)+'\n')
