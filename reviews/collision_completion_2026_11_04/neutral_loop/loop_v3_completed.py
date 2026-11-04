"""Full leading neutral-adjoint -> two unbroken-gauge-boson amplitudes.

The vector A1 is the complete massive-gauge multiplet (V,G,ghost), never
a Proca matter-vector loop. All dimensional quantities below are in mu units.
"""
import os,sys,math,json,time,resource
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
 os.environ[key]='1'
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/cascades'))
from network import state,adapt,build_model,DCOEF,T

def fundamental_basis():
 out=[]
 # t=T/sqrt(2), with tr(t t)=1/2, matching model gauge coupling.
 for size,offset in ((3,0),(2,3)):
  for i in range(size):
   for j in range(i+1,size):
    a=np.zeros((5,5),complex);a[offset+i,offset+j]=a[offset+j,offset+i]=.5;out.append(a)
    a=np.zeros((5,5),complex);a[offset+i,offset+j]=-.5j;a[offset+j,offset+i]=.5j;out.append(a)
  for j in range(1,size):
   a=np.zeros((5,5),complex)
   for i in range(j):a[offset+i,offset+i]=1/math.sqrt(2*j*(j+1))
   a[offset+j,offset+j]=-j/math.sqrt(2*j*(j+1));out.append(a)
 out.append(np.diag([2,2,2,-3,-3])/math.sqrt(60))
 return np.array(out)

def forms(t):
 """tau=M_external^2/(4m_internal^2), exact below threshold.

 Small-t series avoid subtractive loss in A0/A1 at weak e and heavy x.
 """
 t=np.asarray(t,float);f=np.arcsin(np.sqrt(np.minimum(t,1)))**2+0j
 cut=t>1
 root=np.sqrt(1-1/t[cut]);f[cut]=-.25*(np.log((1+root)/(1-root))-1j*math.pi)**2
 small=t<1e-4
 a0=np.empty_like(f);af=np.empty_like(f);av=np.empty_like(f);ap=np.empty_like(f)
 z=t[~small];fz=f[~small]
 a0[~small]=(fz-z)/z**2
 af[~small]=2*(z+(z-1)*fz)/z**2
 av[~small]=-(2*z*z+3*z+3*(2*z-1)*fz)/z**2
 ap[~small]=2*fz/z
 z=t[small]
 a0[small]=1/3+8*z/45+4*z*z/35+128*z**3/1575
 af[small]=4/3+14*z/45+8*z*z/63+104*z**3/1575
 av[small]=-7-22*z/15-76*z*z/105-232*z**3/525
 ap[small]=2+2*z/3+16*z*z/45+8*z**3/35
 return a0,af,av,ap

def product(q):
 p=np.einsum('bij,cjk->bcik',q,q,optimize=True)
 return (p+p.transpose(1,0,2,3))/2

def orthogonal_mass_rotation(masses,physical=None):
 """Deterministic nontrivial real rotations in every degenerate mass block."""
 n=len(masses);v=np.eye(n);used=set()
 for i,m in enumerate(masses):
  if i in used:continue
  ids=[j for j,t in enumerate(masses) if abs(t-m)<1e-10 and (physical is None or physical[j]==physical[i])]
  used.update(ids)
  for j,k in zip(ids[::2],ids[1::2]):
   angle=.371+(j+1)*.013;co,si=math.cos(angle),math.sin(angle)
   v[j,j]=v[k,k]=co;v[j,k]=si;v[k,j]=-si
 return v

def active_tau(ext,M,vertices,products,masses):
 """Largest tau in a nonzero equal-mass block amplitude, not a spectator cut."""
 done=set();rows=[]
 for i,m in enumerate(masses):
  if i in done or m<1e-10:continue
  ids=np.where(abs(masses-m)<1e-10)[0];done.update(ids.tolist())
  t=np.einsum('aij,bcji->abc',vertices[:,ids][:,:,ids],products[:,:,ids][:,:,:,ids],optimize=True)
  norm=float(np.linalg.norm(t))
  rows.append((float(M*M/(4*m*m)),norm,float(m),len(ids)))
 scale=max([r[1] for r in rows]+[1e-300])
 active=[r for r in rows if r[1]>1e-10*scale]
 return dict(max_tau=max([r[0] for r in active]+[0]),blocks=[dict(tau=t,vertex_charge_trace_norm=n,mass=m,multiplicity=g) for t,n,m,g in active],discarded_max_relative=max([r[1]/scale for r in rows if r not in active]+[0]))

def transform_real(q):
 return np.array([np.block([[1j*r.imag,1j*r.real],[-1j*r.real,1j*r.imag]]) for r in q])

def build(x,e):
 d=build_model(x,e,e,math.sqrt(29/200)*e,vertices=True)
 # Repeat the exact charge/Casimir adaptation used by state(); retain rotations.
 R=d['R'];RY=np.einsum('a,aij->ij',DCOEF/math.sqrt(30),R);Q2=RY@RY
 un=[a for a,t in enumerate(T) if np.max(abs(t@np.diag([2,2,2,-3,-3])-np.diag([2,2,2,-3,-3])@t))<1e-12]
 C=np.einsum('aij,ajk->ik',R[un],R[un])
 def fextend(q):
  out=np.zeros((73,73),complex);out[:49,:49]=q;out[49:,49:]=q[1:25,1:25];return out
 def sextend(q):return np.block([[q.real,-q.imag],[q.imag,q.real]])
 QS,CS=sextend(Q2),sextend(C);QF,CF=fextend(Q2),fextend(C)
 O=adapt(d['O'],d['mS2'],QS);O=adapt(O,d['mS2']+np.einsum('ia,ia->a',O,QS@O).real,CS)
 U=adapt(d['U'],d['mF'],QF);U=adapt(U,d['mF']+np.einsum('ia,ia->a',U.conj(),QF@U).real,CF)
 GP=np.diag(np.r_[np.zeros(49),np.ones(24)])
 uv=d['mF']+np.einsum('ia,ia->a',U.conj(),QF@U).real+10*np.einsum('ia,ia->a',U.conj(),CF@U).real
 U=adapt(U,uv,GP)
 RS=d['O'].T@O;RF=d['U'].conj().T@U
 cube=np.einsum('ia,jb,kc,ijk->abc',RS,RS,RS,d['cubic'],optimize=True)
 yuk=np.einsum('iu,jv,ka,ijk->uva',RF,RF,RS,d['yukawa'],optimize=True)
 coeff=np.einsum('bij,aji->ba',fundamental_basis(),T)*math.sqrt(2)
 q=np.einsum('ba,aij->bij',coeff,R)
 qs=np.einsum('ia,bij,jc->bac',O,transform_real(q),O,optimize=True)
 qf=np.einsum('ia,bij,jc->bac',U.conj(),np.array([fextend(a) for a in q]),U,optimize=True)
 qv=np.einsum('ia,bij,jc->bac',d['Ov'],q[:,1:25,1:25],d['Ov'],optimize=True)
 Em=d['E']@O;rz=np.einsum('aij,j->ai',R,d['z']);re=np.einsum('aij,jk->aik',R,Em)
 # K[a,i,j]=d M_V,ij^2 / d S_a, expressed in vector mass basis.
 K=2*d['g']**2*(np.einsum('pia,qi->apq',re.conj(),rz)+np.einsum('pi,qia->apq',rz.conj(),re)).real
 K=np.einsum('pi,apq,qj->aij',d['Ov'],K,d['Ov'],optimize=True)
 s=state(x,e,vertices=False)
 ms=np.sqrt(np.maximum(d['mS2'],0));mf=d['mF'];mv=np.sqrt(np.maximum(d['mV2'],0));physical=s['physical'][:98]
 # Gauge Ward identity: Goldstone tangent and scalar-to-Goldstone coupling.
 massive=np.where(mv>1e-10)[0];massless=np.where(mv<1e-10)[0]
 gold=math.sqrt(2)*np.r_[-rz.imag.T,rz.real.T]@d['Ov'][:,massive]
 gold=gold/np.linalg.norm(gold,axis=0)[None,:]
 goldmass=O.T@gold
 controls=dict(gold_orthonormal=float(np.max(abs(gold.T@gold-np.eye(len(massive))))),
  gold_physical_overlap=float(np.max(abs(goldmass[physical]))),
  AVphysical=float(np.max(abs(K[np.ix_(np.where(physical)[0],massless,massive)]))),
  scalar_charge_mass_commutator=float(np.max(abs(qs*(d['mS2'][None,:,None]-d['mS2'][None,None,:])))),
  fermion_charge_mass_commutator=float(np.max(abs(qf*(mf[None,:,None]-mf[None,None,:])))),
  vector_charge_mass_commutator=float(np.max(abs(qv*(d['mV2'][None,:,None]-d['mV2'][None,None,:])))),
  Takagi=float(np.max(abs(U.T@d['MF']@U-np.diag(mf)))))
 # These traces count ALL physical U1-charged species, including all copies.
 beta=dict(scalar_trace=float(np.trace((qs[-1]@qs[-1])[np.ix_(physical,physical)]).real),
  Weyl_trace=float(np.trace(qf[-1]@qf[-1]).real),
  vector_trace=float(np.trace(qv[-1]@qv[-1]).real))
 beta['b_total']=beta['scalar_trace']/6+2*beta['Weyl_trace']/3-7*beta['vector_trace']/2
 return d,s,cube,yuk,K,qs,qf,qv,ms,mf,mv,physical,goldmass,controls,beta

def amplitudes(ext,M,cube,yuk,K,ps,pf,pv,ms,mf,mv,physical,soft=False):
 a0=np.zeros(len(ms),complex);af=np.zeros(len(mf),complex);ap=np.zeros(len(mf),complex);av=np.zeros(len(mv),complex)
 ss=(ms>1e-10)&physical;ff=mf>1e-10;vv=mv>1e-10
 ts=M*M/(4*ms[ss]**2);tf=M*M/(4*mf[ff]**2);tv=M*M/(4*mv[vv]**2)
 # All gauge-charged internal states must be below no pair cut. Neutral
 # singlets can be lighter but have zero gauge trace and are removed here.
 gs=np.max(abs(ps),axis=(0,1,3))>1e-10;gf=np.max(abs(pf),axis=(0,1,3))>1e-10;gv=np.max(abs(pv),axis=(0,1,3))>1e-10
 tau_max=max(np.max(M*M/(4*ms[ss&gs]**2)),np.max(M*M/(4*mf[ff&gf]**2)),np.max(M*M/(4*mv[vv&gv]**2)))
 if soft:
  a0[ss]=1/(12*ms[ss]**2);af[ff]=2/(3*mf[ff]);ap[ff]=1/mf[ff];av[vv]=-7/(4*mv[vv]**2)
 else:
  a0[ss]=forms(ts)[0]/(4*ms[ss]**2);af[ff]=forms(tf)[1]/(2*mf[ff]);ap[ff]=forms(tf)[3]/(2*mf[ff]);av[vv]=forms(tv)[2]/(4*mv[vv]**2)
 cs=np.einsum('aij,bcji,i->abc',cube[ext],ps,a0,optimize=True)
 cf=np.einsum('ija,bcji,i->abc',yuk[:,:,ext].real,pf,af,optimize=True)
 cp=np.einsum('ija,bcji,i->abc',yuk[:,:,ext].imag,pf,ap,optimize=True)
 cv=np.einsum('aij,bcji,i->abc',K[ext],pv,av,optimize=True)
 return cs,cf,cv,cp,float(tau_max)

def case(x,e):
 d,s,cube,yuk,K,qs,qf,qv,ms,mf,mv,physical,G,controls,beta=build(x,e)
 ps,pf,pv=map(product,(qs,qf,qv));rows=[]
 Vs=orthogonal_mass_rotation(ms,physical);Vf=orthogonal_mass_rotation(mf);Vv=orthogonal_mass_rotation(mv)
 def rotate(q,v):return np.einsum('ji,ajk,kl->ail',v,q,v,optimize=True)
 pr=[product(rotate(q,v)) for q,v in ((qs,Vs),(qf,Vf),(qv,Vv))]
 cubeR=rotate(cube,Vs);yukR=rotate(yuk.transpose(2,0,1),Vf).transpose(1,2,0);KR=rotate(K,Vv)
 for name in ('S8_0','S3_0'):
  group=next(g for g in s['groups'] if g['id']==name);ids=group['indices'];M=group['mass']
  a,b,c,p,tau=amplitudes(ids,M,cube,yuk,K,ps,pf,pv,ms,mf,mv,physical)
  aL,bL,cL,pL,_=amplitudes(ids,M,cube,yuk,K,ps,pf,pv,ms,mf,mv,physical,soft=True)
  ar,br,cr,prr,_=amplitudes(ids,M,cubeR,yukR,KR,*pr,ms,mf,mv,physical)
  basis_error=max(np.linalg.norm(ar-a),np.linalg.norm(br-b),np.linalg.norm(cr-c),np.linalg.norm(prr-p))/max(np.linalg.norm(a),np.linalg.norm(b),np.linalg.norm(c),np.linalg.norm(p),1e-300)
  even=a+b+c;odd=p;let=aL+bL+cL
  pref=d['g']**4*M**3/(4096*math.pi**5)
  gamma=pref*(np.einsum('abc,dbc->ad',even,even.conj())+np.einsum('abc,dbc->ad',odd,odd.conj())).real
  width=float(np.trace(gamma)/len(ids));letwidth=float(pref*(np.sum(abs(let)**2)+np.sum(abs(pL)**2))/len(ids))
  sectors={}
  for n,is_,js in (('gg',range(8),range(8)),('gY',range(8),[11]),('WW',range(8,11),range(8,11)),('WY',range(8,11),[11]),('gW',range(8),range(8,11)),('YY',[11],[11])):
   f=1 if list(is_)==list(js) else 2
   sectors[n]=float(pref*f*(np.sum(abs(even[:,is_][:,:,js])**2)+np.sum(abs(odd[:,is_][:,:,js])**2))/len(ids))
  cg=np.einsum('aij,ip,jq->apq',cube[ids],G,G,optimize=True)
  kv=K[np.ix_(ids,np.where(mv>1e-10)[0],np.where(mv>1e-10)[0])]
  ward=float(np.max(abs(cg-M*M*kv/(2*max(mv)**2))))
  rows.append(dict(id=name,degeneracy=len(ids),mass=M,width=width,width_GeV=2e6*width,lifetime_seconds=6.582119569e-25/(2e6*width) if width else None,
   soft_width=letwidth,finite_over_soft=width/letwidth if letwidth else None,tau_max_spectators_included=tau,sectors=sectors,
   active_scalar=active_tau(ids,M,cube[ids],ps,ms),active_fermion=active_tau(ids,M,yuk[:,:,ids].transpose(2,0,1),pf,mf),active_vector=active_tau(ids,M,K[ids],pv,mv),
   internal_basis_rotation_relative_error=float(basis_error),
   even_norm=float(np.linalg.norm(even)/math.sqrt(len(ids))),odd_norm=float(np.linalg.norm(odd)/math.sqrt(len(ids))),
   scalar_norm=float(np.linalg.norm(a)/math.sqrt(len(ids))),fermion_norm=float(np.linalg.norm(b)/math.sqrt(len(ids))),vector_norm=float(np.linalg.norm(c)/math.sqrt(len(ids))),
   no_vector_width=float(pref*(np.sum(abs(a+b)**2)+np.sum(abs(p)**2))/len(ids)),
   coherence_width_eigenvalues=np.linalg.eigvalsh(gamma).tolist(),irrep_width_spread=float(np.max(abs(gamma-width*np.eye(len(ids))))/max(width,1e-300)),
   Goldstone_cubic_Ward_error=ward,coeff_even_real=even.real.tolist(),coeff_even_imag=even.imag.tolist(),coeff_odd_real=odd.real.tolist(),coeff_odd_imag=odd.imag.tolist(),
   max_coefficient_imaginary=float(max(np.max(abs(even.imag)),np.max(abs(odd.imag))))))
  print(x,e,name,M,width,flush=True)
 return dict(x=x,e=e,controls=controls,U1_beta=beta,states=rows)

def main(out):
 start=time.monotonic();cases=[]
 for x,e in ((3.,.003),(10.,.003),(25.4000254000381,.003),(30.,.003),(100.,.003),(25.4000254000381*math.sqrt(3),.001),(25.4000254000381*math.sqrt(.3),.01)):
  cases.append(case(x,e))
 checks=dict(beta=all(abs(c['U1_beta']['b_total']+5)<1e-9 for c in cases),gauge_covariant=all(s['irrep_width_spread']<1e-7 for c in cases for s in c['states']),
  Goldstone_Ward=all(s['Goldstone_cubic_Ward_error']<1e-10 for c in cases for s in c['states']),mixed_physical_zero=all(c['controls']['AVphysical']<1e-10 for c in cases),
  basis_invariant=all(s['internal_basis_rotation_relative_error']<1e-10 for c in cases for s in c['states']),
  positive=all(s['width']>0 for c in cases for s in c['states']))
 scaling=[]
 for index,name in enumerate(('S8_0','S3_0')):
  v=[dict(e=c['e'],width_over_e13over2=c['states'][index]['width']/c['e']**6.5) for c in (cases[2],cases[-2],cases[-1])]
  rel=max(t['width_over_e13over2'] for t in v)/min(t['width_over_e13over2'] for t in v)-1
  scaling.append(dict(id=name,cases=v,relative_spread=rel));checks['scaling_'+name]=rel<1e-9
 result=dict(claim_id='CC10_COMPLETE_LEADING_NEUTRAL_GAUGE_EXITS',cases=cases,checks=checks,scaling=scaling,runtime_seconds=time.monotonic()-start,
  peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
  coefficient_convention='L=g^2/(32pi^2) sum_bc S (CE_bc F_b.F_c + CO_bc F_b.Fdual_c), canonical generators tr(t t)=1/2',
  coverage='All physical massive scalar and Weyl internal states, full broken massive-gauge multiplet; all 12 unbroken gauge-boson pairs; S8_0 and S3_0 every degenerate component',
  non_claims=['Leading vacuum widths on fixed tree background; no medium, higher-loop or expansion evolution','Gauge radiation is in residual unbroken SU3/SU2/U1, with no asserted visible portal'])
 Path(out).write_text(json.dumps(result,indent=2)+'\n');assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
