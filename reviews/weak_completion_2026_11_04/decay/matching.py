"""Ordinary fixed-vacuum Rxi scalar -> two massless Majorana fermions.

All six triangle classes are integrated, retaining Goldstones in Rxi scalar
propagators. Numerators are reduced between on-shell external spinors before
Feynman-parameter integration. No displaced-background gauge fixing is used.
This implementation is an experiment until its Ward/benchmark checks pass.
"""
import os,sys,math,json,time,resource,functools
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from numpy.polynomial.legendre import leggauss
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/neutral_loop'))
from loop import fundamental_basis,transform_real,T
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/cascades'))
from network import build_model,adapt,DCOEF

@functools.lru_cache(None)
def quadrature(n):
 z,w=leggauss(n);z=(z+1)/2;w=w/2
 x=z[:,None]+np.zeros((n,n));y=(1-x)*z[None,:];ww=w[:,None]*w[None,:]*(1-x)
 return x,y,1-x-y,ww

def moments(s,mt,mb,mr,powers=(1,1,1),n=24,uv=0.,Q2=1.):
 x,y,z,weights=quadrature(n);den=x*mt+y*mb+z*mr-x*y*s
 if min(den.flat)<=0:raise ValueError('Internal cut requires complex integration, not silently clipped')
 wt=x**(powers[0]-1)*y**(powers[1]-1)*z**(powers[2]-1)
 degree=sum(powers)
 if degree==3:
  j0=-1/den;j2=.5*(uv-np.log(den/Q2)-.5);j4=np.zeros_like(den)
 elif degree==4:
  j0=wt/den**2;j2=-.5*wt/den;j4=.25*wt*(uv-np.log(den/Q2)-5/6)
 elif degree==5 and max(powers)==2:
  j0=-2*wt/den**3;j2=.5*wt/den**2;j4=-.25*wt/den
 else:raise ValueError('Unsupported denominator multiplicity')
 u=-x*y*s;v=y*s;w=-x*s
 values=dict(one=j0,u=u*j0+4*j2,v=v*j0,w=w*j0,
  uu=u*u*j0+12*u*j2+24*j4,uv=u*v*j0+6*v*j2,uw=u*w*j0+6*w*j2,vw=v*w*j0+2*s*j2)
 return {k:float(np.sum(weights*t)) for k,t in values.items()}

def grouped(ids,masses):
 out=[]
 for i in ids:
  match=next((a for a in out if abs(a[0]-masses[i])<1e-10),None)
  if match is None:out.append([float(masses[i]),[int(i)]])
  else:match[1].append(int(i))
 return [(m,np.array(ii,int)) for m,ii in out]

def model(x=25.4000254000381,e=.003,rotate=False):
 d=build_model(x,e,e,math.sqrt(29/200)*e,vertices=True);R=d['R'];g=d['g'];U=d['U']
 RY=np.einsum('a,aij->ij',DCOEF/math.sqrt(30),R);Q2=RY@RY
 q2s=np.block([[Q2.real,-Q2.imag],[Q2.imag,Q2.real]])
 O=adapt(d['O'],d['mS2'],q2s)
 if rotate:
  from loop import orthogonal_mass_rotation
  sc=np.einsum('ia,ia->a',O,q2s@O).real>.1
  O=O@orthogonal_mass_rotation(d['mS2'],sc)
  U=U@orthogonal_mass_rotation(d['mF'])
  d=dict(d);d['Ov']=d['Ov']@orthogonal_mass_rotation(d['mV2'])
 rot=d['O'].T@O
 cubic=np.einsum('ia,jb,kc,ijk->abc',rot,rot,rot,d['cubic'],optimize=True)
 Em=d['E']@O;qsval=np.einsum('ia,ia->a',O,q2s@O).real
 q2f=np.zeros((73,73),complex);q2f[:49,:49]=Q2;q2f[49:,49:]=Q2[1:25,1:25]
 qfval=np.einsum('ia,ia->a',U.conj(),q2f@U).real
 coeff=np.einsum('bij,aji->ba',fundamental_basis(),T)*math.sqrt(2)
 ext=np.zeros((73,12),complex);ext[49:]=coeff.T
 dy=np.zeros((73,73,98),complex);dy[:49,:49]=np.einsum('ijk,ka->ija',d['Y'],Em)
 dj=math.sqrt(2)*g*np.einsum('ka,pki->pia',Em.conj(),R,optimize=True)
 dy[49:,:49]=dj;dy[:49,49:]=dj.transpose(1,0,2)
 Y=np.einsum('Ia,JK,IJs->aKs',ext,U,dy,optimize=True)
 RF=np.zeros((24,73,73),complex);RF[:,:49,:49]=R;RF[:,49:,49:]=R[:,1:25,1:25]
 G=g*np.einsum('rv,Ia,rIJ,JK->vaK',d['Ov'],ext.conj(),RF,U,optimize=True)
 qsm=np.einsum('ia,rij,jb->rab',O,transform_real(R),O,optimize=True)
 rz=np.einsum('aij,j->ai',R,d['z'])
 chargedS=np.where(qsval>.1)[0];chargedF=np.where(qfval>.1)[0];chargedV=np.where(d['mV2']>1e-12)[0]
 gold=(qsval>.1)&(d['mS2']<1e-15)
 return dict(d=d,O=O,U=U,Em=Em,cubic=cubic,dy=dy,Y=Y,G=G,RF=RF,qsm=qsm,rz=rz,coeff=coeff,ext=ext,
  qsval=qsval,qfval=qfval,chargedS=chargedS,chargedF=chargedF,chargedV=chargedV,gold=gold)

def parent(data,name):
 d=data['d'];cas={'S8_0':(3,7),'S3_0':(2,10)}[name];C=np.einsum('aij,ajk->ik',d['R'],d['R'])
 # Select masses by the same residual-group Casimir used by CC10.
 q=np.einsum('ba,aij->bij',data['coeff'],d['R']);cg=np.einsum('aij,ajk->ik',q[:11],q[:11])
 Cg=np.block([[cg.real,-cg.imag],[cg.imag,cg.real]])
 cv=np.einsum('ia,ia->a',data['O'],Cg@data['O']).real
 possible=np.where((abs(cv-cas[0])<1e-7)&(data['qsval']<.1)&(d['mS2']>1e-15))[0]
 m2=min(d['mS2'][possible]);ids=np.where((abs(d['mS2']-m2)<1e-10)&(abs(cv-cas[0])<1e-7))[0]
 target=np.zeros(98);b=cas[1]
 # Canonical external state aligned to t8 of SU3 or t3 of SU2.
 target[(25 if name=='S8_0' else 74): (49 if name=='S8_0' else 98)]=data['coeff'][b].real
 weights=data['O'][:,ids].T@target;weights=weights/np.linalg.norm(weights);a=np.zeros(98);a[ids]=weights
 ep=data['Em']@a;yp=data['U'].T@np.einsum('IJa,a->IJ',data['dy'],a)@data['U']
 cp=np.einsum('a,aij->ij',a,data['cubic']);D=d['g']*np.einsum('rv,a,ras->vs',d['Ov'],a,data['qsm'],optimize=True)
 re=np.einsum('aij,j->ai',d['R'],ep);K=2*d['g']**2*(re.conj()@data['rz'].T+data['rz'].conj()@re.T).real
 K=d['Ov'].T@K@d['Ov']
 return dict(name=name,mass=math.sqrt(m2),ids=ids,weights=a,ep=ep,yp=yp,cp=cp,D=D,K=K,b=b)

def coefficients(data,p,a=None,b=11,charged_only=True):
 d=data['d'];Y=data['Y'];G=data['G'];a=p['b'] if a is None else a
 fs=grouped(data['chargedF'] if charged_only else range(73),d['mF'])
 sid=data['chargedS'] if charged_only else np.arange(98)
 # Tree-zero physical singlets and charged Goldstones share m²=0, but only
 # the Goldstones acquire xi*mV². They must remain distinct propagator blocks.
 ss=[]
 for isgold in (False,True):ss+=grouped([i for i in sid if data['gold'][i]==isgold],np.sqrt(np.maximum(d['mS2'],0)))
 vv=grouped(data['chargedV'] if charged_only else range(24),np.sqrt(np.maximum(d['mV2'],0)))
 terms=[]
 for mi,I in fs:
  for mj,J in fs:
   for ms,S in ss:
    A=np.einsum('is,js,ij->',Y[a][np.ix_(I,S)].conj(),Y[b][np.ix_(J,S)].conj(),p['yp'][np.ix_(I,J)])
    B=np.einsum('is,js,ij->',Y[a][np.ix_(I,S)].conj(),Y[b][np.ix_(J,S)].conj(),p['yp'][np.ix_(I,J)].conj())*mi*mj
    if max(abs(A),abs(B))>1e-25:terms.append(dict(kind='FFS',mt=mi**2,mb=mj**2,mr=ms**2,goldr=bool(data['gold'][S[0]]),A=A,B=B))
   for mv,V in vv:
    A=np.einsum('vi,vj,ij->',G[V,a][:,I],G[V,b][:,J],p['yp'][np.ix_(I,J)].conj())
    B=np.einsum('vi,vj,ij->',G[V,a][:,I],G[V,b][:,J],p['yp'][np.ix_(I,J)])*mi*mj
    if max(abs(A),abs(B))>1e-25:terms.append(dict(kind='FFV',mt=mi**2,mb=mj**2,mr=mv**2,A=A,B=B))
  for ms,S in ss:
   for mt,Tt in ss:
    A=np.einsum('st,is,it->',p['cp'][np.ix_(S,Tt)],Y[a][np.ix_(I,S)].conj(),Y[b][np.ix_(I,Tt)].conj())*mi
    if abs(A)>1e-25:terms.append(dict(kind='FSS',mt=ms**2,mb=mt**2,mr=mi**2,goldt=bool(data['gold'][S[0]]),goldb=bool(data['gold'][Tt[0]]),A=A))
   for mv,V in vv:
    A=np.einsum('vs,is,vi->',p['D'][np.ix_(V,S)],Y[a][np.ix_(I,S)].conj(),G[V,b][:,I])
    B=np.einsum('vs,vi,is->',p['D'][np.ix_(V,S)],G[V,a][:,I],Y[b][np.ix_(I,S)].conj())
    # The bridge fermion flows opposite to k in both mixed graphs; its
    # numerator is -slash(k)+m. This reverses the surviving kinetic term.
    if abs(A)>1e-25:terms.append(dict(kind='FSV',mt=ms**2,mb=mv**2,mr=mi**2,goldt=bool(data['gold'][S[0]]),A=A))
    if abs(B)>1e-25:terms.append(dict(kind='FVS',mt=mv**2,mb=ms**2,mr=mi**2,goldb=bool(data['gold'][S[0]]),A=-B))
  for mv,V in vv:
   A=np.einsum('vw,vi,wi->',p['K'][np.ix_(V,V)],G[V,a][:,I],G[V,b][:,I])*mi
   if abs(A)>1e-25:terms.append(dict(kind='FVV',mt=mv**2,mb=mv**2,mr=mi**2,A=A))
 scale=max([max(abs(t['A']),abs(t.get('B',0))) for t in terms]+[1e-300])
 return [t for t in terms if max(abs(t['A']),abs(t.get('B',0)))>1e-12*scale]

def amplitude(data,p,terms,xi=1.,s=None,n=24,ntheta=10,uv=0.,Q2=1.):
 if s is None:s=p['mass']**2
 zg,wg=leggauss(ntheta);theta=(zg+1)/2;wt=wg/2;delta=xi-1;mv2=max(data['d']['mV2']);out={k:0j for k in ('FFS','FSS','FFV','FVV','FSV','FVS')}
 def mom(mt,mb,mr,pow=(1,1,1)):return moments(s,mt,mb,mr,pow,n,uv,Q2)
 for t in terms:
  kind=t['kind'];mt=t['mt'];mb=t['mb'];mr=t['mr']
  if t.get('goldt'):mt=xi*mv2
  if t.get('goldb'):mb=xi*mv2
  if t.get('goldr'):mr=xi*mv2
  m=mom(mt,mb,mr)
  if kind=='FFS':v=t['A']*m['u']+t['B']*m['one']
  elif kind=='FSS':v=t['A']*m['one']
  elif kind=='FFV':
   v=4*t['A']*(m['u']+(m['v']-m['w']-s*m['one'])/2)+4*t['B']*m['one']
   if delta:
    for th,w in zip(theta,wt):
     z=mom(mt,mb,mr*(1+delta*th),(1,1,2));v+=delta*w*(t['A']*(z['uu']+z['uv']-z['uw']-z['vw'])+t['B']*z['u'])
  elif kind=='FVV':
   v=4*t['A']*m['one']
   if delta:
    for th,w in zip(theta,wt):
     z=mom(mt*(1+delta*th),mb,mr,(2,1,1));v+=delta*w*t['A']*(z['u']+z['v'])
     z=mom(mt,mb*(1+delta*th),mr,(1,2,1));v+=delta*w*t['A']*(z['u']-z['w'])
     for th2,w2 in zip(theta,wt):
      z=mom(mt*(1+delta*th),mb*(1+delta*th2),mr,(2,2,1));v+=delta*delta*w*w2*t['A']*(z['uu']+(z['uv']-z['uw']-s*z['u'])/2)
  elif kind=='FSV':
   v=t['A']*(m['u']+2*m['v'])
   if delta:
    for th,w in zip(theta,wt):
     z=mom(mt,mb*(1+delta*th),mr,(1,2,1));v+=delta*w*t['A']*(z['uu']+z['uv']-s*z['u'])
  elif kind=='FVS':
   v=t['A']*(-m['u']+2*m['w'])
   if delta:
    for th,w in zip(theta,wt):
     z=mom(mt*(1+delta*th),mb,mr,(2,1,1));v+=delta*w*t['A']*(-z['uu']+z['uw']+s*z['u'])
  out[kind]+=v
 return {k:-v.conjugate()/(16*math.pi**2) for k,v in out.items()}

def messenger_benchmark(n=32):
 from model import component_data
 import itertools
 X=1.;lam=.7;g=.2;mx=.3;Y=np.zeros((3,3,3),complex)
 for p in itertools.permutations([0,1,2]):Y[p]=lam
 mu=np.diag([mx,0,0]);linear=np.array([-mx*X,0,0],complex)
 d=component_data(Y,np.array([X,0,0],complex),linear,np.array([np.diag([0,1,-1])]),g,mu=mu,vertices=True)
 Em=d['E']@d['O'];dy=np.zeros((4,4,6),complex);dy[:3,:3]=np.einsum('ijk,ka->ija',Y,Em)
 dj=math.sqrt(2)*g*np.einsum('ka,pki->pia',Em.conj(),d['R']);dy[3:,:3]=dj;dy[:3,3:]=dj.transpose(1,0,2)
 ep=np.array([0,0,0,1],complex);ye=np.einsum('I,JK,IJs->Ks',ep,d['U'],dy)
 a=d['O'][0];yp=d['U'].T@np.einsum('IJs,s->IJ',dy,a)@d['U'];cp=np.einsum('a,aij->ij',a,d['cubic'])
 fids=np.where(abs(d['mF']-lam*X)<1e-10)[0];sids=np.where(abs(d['mS2']-(lam*X)**2)<1e-10)[0]
 A=np.einsum('is,js,ij->',ye[np.ix_(fids,sids)].conj(),ye[np.ix_(fids,sids)].conj(),yp[np.ix_(fids,fids)])
 B=np.einsum('is,js,ij->',ye[np.ix_(fids,sids)].conj(),ye[np.ix_(fids,sids)].conj(),yp[np.ix_(fids,fids)].conj())*(lam*X)**2
 C=np.einsum('st,is,it->',cp[np.ix_(sids,sids)],ye[np.ix_(fids,sids)].conj(),ye[np.ix_(fids,sids)].conj())*(lam*X)
 ans=[]
 for s in (0.,mx*mx):
  mm=moments(s,(lam*X)**2,(lam*X)**2,(lam*X)**2,n=n)
  total=-(A*mm['u']+(B+C)*mm['one']).conjugate()/(16*math.pi**2)
  tau=s/(4*(lam*X)**2);ff=math.asin(math.sqrt(tau))**2/tau if tau else 1.
  expected=-math.sqrt(2)*g*g*mx/(16*math.pi**2*X)*ff
  ans.append(dict(s=s,amplitude=[total.real,total.imag],expected=expected,relative_error=abs(total/expected-1)))
 return ans

def main(out):
 start=time.monotonic();d=model();dr=model(rotate=True);rows=[];checks={}
 for name in ('S8_0','S3_0'):
  p=parent(d,name);terms=coefficients(d,p);cases=[]
  for xi in (.5,1.,2.):
   A=amplitude(d,p,terms,xi);total=sum(A.values());cases.append(dict(xi=xi,parts={k:[v.real,v.imag] for k,v in A.items()},amplitude=[total.real,total.imag],width=p['mass']/(8*math.pi)*abs(total)**2))
  a=amplitude(d,p,terms,1.,uv=1.);a0=amplitude(d,p,terms,1.);uvdiff=sum(a.values())-sum(a0.values())
  soft=amplitude(d,p,terms,1.,s=0.);total=sum(a0.values());width=p['mass']/(8*math.pi)*abs(total)**2
  pp=parent(dr,name);rotamp=sum(amplitude(dr,pp,coefficients(dr,pp)).values())
  refined=sum(amplitude(d,p,terms,xi=2.,n=36,ntheta=16).values())
  referr=abs(refined-complex(*cases[-1]['amplitude']))/max(abs(refined),1e-300)
  rows.append(dict(id=name,mass=p['mass'],terms=len(terms),cases=cases,soft_parts={k:[v.real,v.imag] for k,v in soft.items()},
   amplitude=[total.real,total.imag],width=width,UV_residual=[uvdiff.real,uvdiff.imag],
   internal_rotation_relative_error=abs(rotamp-total)/max(abs(total),1e-300),quadrature_relative_error=referr,
   xi_relative_spread=max(abs(complex(*c['amplitude'])-total) for c in cases)/max(abs(total),1e-300)))
  checks[name+'_gauge']=rows[-1]['xi_relative_spread']<1e-8;checks[name+'_UV']=abs(uvdiff)/max(abs(total),1e-300)<1e-8
  checks[name+'_basis']=rows[-1]['internal_rotation_relative_error']<1e-8;checks[name+'_quadrature']=referr<1e-8
  print(name,'terms',len(terms),'amp',total,'width',width,'xi',rows[-1]['xi_relative_spread'],flush=True)
 scaling=[]
 for ee in (.001,.01):
  dd=model(e=ee,x=25.4000254000381*math.sqrt(.003/ee))
  for r in rows:
   pp=parent(dd,r['id']);yy=sum(amplitude(dd,pp,coefficients(dd,pp)).values());ref=complex(*r['amplitude']);ratio=yy/ref/(ee/.003)**3
   scaling.append(dict(e=ee,id=r['id'],ratio_to_e3=[ratio.real,ratio.imag],relative_error=abs(ratio-1)))
 bench=messenger_benchmark();checks['supersymmetric_messenger_benchmark']=max(t['relative_error'] for t in bench)<1e-10
 checks['weak_scaling']=max(t['relative_error'] for t in scaling)<1e-8
 checks={k:bool(v) for k,v in checks.items()}
 result=dict(claim_id='CC11_ORDINARY_ONSHELL_TRIANGLE_MATCHING_AUDIT',states=rows,checks=checks,weak_scaling=scaling,messenger_benchmark=bench,runtime_seconds=time.monotonic()-start,
  peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
  scope='Experimental full six-triangle ordinary fixed-vacuum Rxi matching, massless external gauginos; gauge/normalization tests determine interpretation, not process exit alone.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
