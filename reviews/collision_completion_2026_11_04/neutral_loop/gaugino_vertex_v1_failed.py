"""Zero-external-momentum scalar insertion into finite gaugino threshold.

Fixed OLD unbroken external gaugino columns; generic Takagi realification for
the CP-odd adjoint displacement, where historical component_data refuses z.
This is explicitly soft matching, not an exact on-shell three-point function.
"""
import os,sys,math,json,time,resource
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/neutral_loop'))
from loop import build,fundamental_basis,T
sys.path.insert(0,str(ROOT/'reviews/radial_ir_cold_2026_11_01/gapless_charge'))
from gaugino_threshold import threshold

def displaced(base,dz):
 d=dict(base);z=base['z']+dz;Y=base['Y'];R=base['R'];g=base['g'];E=base['E']
 F=np.r_[1.+0j,np.zeros(48)]+.5*np.einsum('ijk,j,k->i',Y,z,z)
 M=np.einsum('ijk,k->ij',Y,z);A=M.conj().T@M;B=np.einsum('k,kij->ij',F.conj(),Y)
 H=np.block([[A.real+B.real,-A.imag-B.imag],[A.imag-B.imag,A.real-B.real]])
 rz=np.einsum('aij,j->ai',R,z);L=2*g*(E.conj().T@rz.T).real.T
 S=2*g*np.einsum('ia,pij,jb->pab',E.conj(),R,E,optimize=True).real
 D=g*np.einsum('i,ai->a',z.conj(),rz).real;H+=L.T@L+np.einsum('p,pab->ab',D,S)
 J=math.sqrt(2)*g*np.einsum('i,aij->aj',z.conj(),R)
 MF=np.block([[M,J.T],[J,np.zeros((24,24),complex)]])
 # K (u,v)=m(u,v) iff MF (u+i v)=m(u-i v); nonzero columns
 # are a Takagi basis. The threshold multiplies each zero column by m=0.
 K=np.block([[MF.real,-MF.imag],[-MF.imag,-MF.real]])
 vals,vec=eigh(K);nf=len(MF);m=np.maximum(vals[-nf:],0);U=vec[:nf,-nf:]+1j*vec[nf:,-nf:]
 m[m<1e-12*max(m)]=0
 MV=2*g*g*(rz.conj()@rz.T).real;mv,Ov=eigh(MV);mv[abs(mv)<1e-12*max(mv)]=0
 ms,O=eigh(H)
 d.update(z=z,F=F,MF=MF,H=H,mF=m,mF2=m*m,U=U,MV=MV,mV2=mv,Ov=Ov,mS2=ms,O=O)
 nz=np.where(m>0)[0]
 d['generic_controls']=dict(Takagi=float(np.max(abs((U.T@MF@U-np.diag(m))[np.ix_(nz,nz)]))),
  massive_unitarity=float(np.max(abs((U.conj().T@U-np.eye(nf))[np.ix_(nz,nz)]))),
  D_flat=float(np.max(abs(D))))
 return d

def main(out):
 start=time.monotonic();x=25.4000254000381;e=.003
 base,state,*_=build(x,e)
 coeff=np.einsum('bij,aji->ba',fundamental_basis(),T)*math.sqrt(2)
 ext=np.zeros((73,12),complex);ext[49:]=coeff.T
 b=threshold(base,ext,xi=1.);d0=displaced(base,np.zeros(49));bg=threshold(d0,ext,xi=1.)
 baseerr=float(np.linalg.norm(bg['matrix']-b['matrix'])/np.linalg.norm(b['matrix']))
 rows=[];controls=[]
 for name in ('S8_0','S3_0'):
  group=next(t for t in state['groups'] if t['id']==name);ids=group['indices'];M=group['mass']
  # raw O and adapted O are related by mass-block rotations; use original
  # raw mass eigenspace and project the full normalized group to it.
  rawids=np.where(abs(np.sqrt(np.maximum(base['mS2'],0))-M)<1e-8)[0]
  if len(rawids)!=len(ids):raise ValueError('irrep mass degeneracy mixed with another representation')
  vertices=[];steperrors=[];gaugeerrors=[];qerrors=[]
  h=2e-4
  for a in rawids:
   direction=base['E']@base['O'][:,a]
   deriv=[]
   for step in (h,h/2,h/4):
    plus=displaced(base,step*direction);minus=displaced(base,-step*direction)
    controls.extend([plus['generic_controls'],minus['generic_controls']])
    yp=threshold(plus,ext,xi=1.)['matrix'];ym=threshold(minus,ext,xi=1.)['matrix']
    deriv.append((yp-ym)/(2*step))
   vertex=(4*deriv[-1]-deriv[-2])/3
   vertices.append(vertex)
   steperrors.append(float(np.linalg.norm(deriv[-1]-deriv[-2])/max(np.linalg.norm(vertex),1e-300)))
   # Only mixed U1 amplitudes are claimed controlled by the heavy charged
   # threshold. Pure nonabelian light-particle cuts need separate matching.
   plus=displaced(base,h/2*direction);minus=displaced(base,-h/2*direction)
   gauge=(threshold(plus,ext,xi=2.)['matrix']-threshold(minus,ext,xi=2.)['matrix'])/h
   qalt=(threshold(plus,ext,Q2=7.,xi=1.)['matrix']-threshold(minus,ext,Q2=7.,xi=1.)['matrix'])/h
   gaugeerrors.append(float(np.linalg.norm((gauge-vertex)[:11,11])/max(np.linalg.norm(vertex[:11,11]),1e-300)))
   qerrors.append(float(np.linalg.norm((qalt-vertex)[:11,11])/max(np.linalg.norm(vertex[:11,11]),1e-300)))
   print(name,int(a),'step',steperrors[-1],'xi',gaugeerrors[-1],flush=True)
  V=np.array(vertices)
  # For L=-S y_ij lambda_i lambda_j/2+h.c. and effectively massless
  # daughters, Gamma=M/(16pi) sum ordered_ij |y_ij|^2.
  width_matrix=M/(16*math.pi)*np.einsum('aij,bij->ab',V,V.conj()).real
  mixed=M/(8*math.pi)*np.einsum('ai,bi->ab',V[:,:11,11],V[:,:11,11].conj()).real
  w=float(np.trace(width_matrix)/len(rawids));wm=float(np.trace(mixed)/len(rawids))
  # Lightest U1-charged internal scalar/fermion sets the derivative expansion.
  charged=state['charged'];m=state['mass'];mch=min(m[charged&m.astype(bool)])
  rows.append(dict(id=name,mass=M,degeneracy=len(rawids),soft_all_gaugino_width=w,soft_mixed_photino_width=wm,
   soft_mixed_photino_width_GeV=2e6*wm,soft_mixed_photino_lifetime_seconds=6.582119569e-25/(2e6*wm),
   mixed_su3_width=float(M/(8*math.pi)*np.sum(abs(V[:,:8,11])**2)/len(rawids)),
   mixed_su2_width=float(M/(8*math.pi)*np.sum(abs(V[:,8:11,11])**2)/len(rawids)),
   mixed_width_eigenvalues=np.linalg.eigvalsh(mixed).tolist(),
   mixed_irrep_covariance_error=float(np.max(abs(mixed-wm*np.eye(len(rawids))))/max(wm,1e-300)),
   vertex_norm=float(np.linalg.norm(V)/math.sqrt(len(rawids))),mixed_vertex_norm=float(np.linalg.norm(V[:,:11,11])/math.sqrt(len(rawids))),
   max_step_halving_relative_error=max(steperrors),max_xi1_xi2_mixed_relative_difference=max(gaugeerrors),
   max_Q1_Q7_mixed_relative_difference=max(qerrors),lightest_U1_charged_mass=float(mch),
   tau_charged=M*M/(4*mch*mch),momentum_expansion_M2_over_mcharged2=M*M/(mch*mch),
   vertex_real=V.real.tolist(),vertex_imag=V.imag.tolist()))
 checks=dict(generic_Takagi=all(c['Takagi']<1e-12 for c in controls),generic_massive_unitarity=all(c['massive_unitarity']<1e-8 for c in controls),
  baseline_threshold=baseerr<1e-9,step_convergence=all(r['max_step_halving_relative_error']<1e-3 for r in rows),
  mixed_gauge_covariance=all(r['mixed_irrep_covariance_error']<1e-3 for r in rows))
 result=dict(claim_id='CC10_SOFT_NEUTRAL_GAUGINO_VERTEX',x=x,e=e,mu_GeV=2e6,baseline_threshold_real=b['matrix'].real.tolist(),baseline_threshold_reconstruction_error=baseerr,
  states=rows,checks=checks,controls_max={k:max(c[k] for c in controls) for k in controls[0]},
  runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
  scope='Fixed-old-basis zero-external-momentum threshold derivative, Richardson extrapolated. Mixed photino channels have heavy U1-charged internal sector. Exact finite-momentum three-point matching remains distinct.',
  non_claims=['No exact on-shell vertex assertion from zero-momentum derivative','No cold photino abundance/history claim','Pure nonabelian channels may have light internal cuts and are diagnostic only'])
 Path(out).write_text(json.dumps(result,indent=2)+'\n');assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
