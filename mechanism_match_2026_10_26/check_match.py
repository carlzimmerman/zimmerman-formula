import argparse,json
from pathlib import Path
import numpy as np
import sympy as sp
from matched import Matched

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
model=Matched();m=model.m;rng=np.random.default_rng(26026)
a=model.reference['a'].copy()*np.exp(1j*.02*rng.normal(size=(2,m.n)))
x=model.reference['alpha'].copy();rho=abs(a[0])**2/m.vol
s=model.relaxed_s(a)*(1+.001*np.cos(m.r));ps=m.vol*(1e-4*model.M*model.lam*rho)
chi=.01*m.sigma/(m.g+m.g2*max(rho))*np.exp(-(m.wr/5)**2)
vel=1e-5*np.sin(m.wr)*np.exp(-(m.wr/5)**2)
P=model.deposit((m.g+model.h*s)*abs(a[0])**2)+m.wvol*vel
p=m.Z(a)*1e-3*np.exp(-(m.r/5)**2)
z=(a,x,p,chi,P,s,ps);gr=model.gradient(z);f=model.field(z)
dirs=[.02*a*(rng.normal(size=a.shape)+1j*rng.normal(size=a.shape)),
      .01*np.exp(-(m.r/8)**2),m.Z(a)*1e-3*np.sin(m.r)*np.exp(-(m.r/8)**2),
      .01*m.sigma/(m.g+m.g2*max(rho))*np.sin(m.wr)*np.exp(-(m.wr/5)**2),
      m.wvol*1e-5*np.cos(m.wr)*np.exp(-(m.wr/5)**2),
      model.lam*rho*.01*np.sin(m.r),m.vol*model.M*model.lam*rho*1e-4*np.cos(m.r)]
rows=[]
for i,name in enumerate(['complex_amplitudes','carrier','carrier_momentum','chi','canonical_Pchi','mediator','canonical_Ps']):
 analytic=float(2*np.real(np.vdot(gr[i],dirs[i])) if i==0 else gr[i]@dirs[i]);errors=[]
 for eps in [1e-3,3e-4,1e-4]:
  vals=[]
  for coeff in [-2,-1,1,2]:
   zz=list(z);zz[i]=z[i]+coeff*eps*dirs[i];vals.append(model.energy(tuple(zz)))
  fd=(vals[0]-8*vals[1]+8*vals[2]-vals[3])/(12*eps)
  errors.append({'eps':eps,'finite_difference':fd,'relative_error':abs(fd-analytic)/max(1e-8,abs(analytic))})
 assert min(e['relative_error'] for e in errors)<2e-5,(name,analytic,errors)
 rows.append({'variable':name,'analytic':analytic,'checks':errors})
geo=model.geometry(z);D=geo[-1];jT=D/m.sigma;psi=geo[-2]
jF=m.k*m.w*np.imag(np.conj(psi[1,:-1])*psi[1,1:])/m.sigma
Gamma=2*m.J/m.sigma*np.imag(np.conj(a[0])*model.align(a,x)[0])
md=2*np.real(np.conj(a)*f[0]);expected=np.array([Gamma,-Gamma])
expected[0,:-1]-=jT;expected[0,1:]+=jT;expected[1,:-1]-=jF;expected[1,1:]+=jF
continuity=float(np.max(abs(md-expected)));assert continuity<1e-11
massdot=float(np.sum(md));chargedot=float(np.sum(f[4]));assert abs(massdot)<1e-11 and abs(chargedot)<1e-10

# Exact embedded old Hamiltonian, including the nontrivial canonical chart.
ss=model.lam*rho;PP=model.deposit((m.g+m.g2*rho)*abs(a[0])**2)+m.wvol*vel
zz=(a,x,p,chi,PP,ss,np.zeros(m.n));beta=(m.g+2*m.g2*rho)*m.chi_m(chi)/m.sigma
phi=a.copy();phi[0]*=np.exp(-1j*beta)
old=m.full_energy(phi,x,p,chi,vel);sgrad=.5*m.c*m.c*np.sum(m.w*np.diff(ss)**2)
match_error=model.energy(zz)-sgrad-old;assert abs(match_error)<1e-10
# On the constrained s=lambda*rho surface the chain force restores the old
# density companion; check by finite differences of the pulled-back energy.
gg=model.gradient(zz);s_only_grad=m.c*m.c*model.lapgrad(m.w,ss)
chain=gg[0].copy();chain[0]+=model.lam*(gg[5]-s_only_grad)/m.vol*a[0]
dd=dirs[0];expected_chain=2*np.real(np.vdot(chain,dd));es=[]
for e in [1e-3,3e-4,1e-4]:
 def pulled(t):
  aa=a+t*dd;rr=abs(aa[0])**2/m.vol;sz=model.lam*rr
  zt=(aa,x,p,chi,PP,sz,np.zeros(m.n))
  return model.energy(zt)-.5*m.c*m.c*np.sum(m.w*np.diff(sz)**2)
 fd=(pulled(-2*e)-8*pulled(-e)+8*pulled(e)-pulled(2*e))/(12*e)
 es.append(abs(fd-expected_chain)/max(1e-8,abs(expected_chain)))
assert min(es)<2e-5
# all-F endpoint regularity, no divisions by component amplitude.
af=np.array([np.zeros(m.n,complex),np.sqrt(np.sum(abs(a)**2,axis=0)).astype(complex)])
zf=(af,x,p,chi,m.wvol*vel,np.zeros(m.n),np.zeros(m.n));assert all(np.all(np.isfinite(t)) for t in model.field(zf))

# Exact local algebraic elimination, retaining the spatial square.
d,B,M,h,k,r,sig,v2=sp.symbols('d B M h k r sig v2',positive=True)
L=-M**2*d**2/2+h*d*B-k*h*h*r*v2*d*d/(2*sig*sig)
ds=sp.solve(sp.diff(L,d),d)[0]
assert sp.simplify(L.subs(d,ds)-h*h*B*B/(2*(M*M+k*h*h*r*v2/(sig*sig))))==0
out={'force_checks':rows,'mass_derivative':massdot,'shift_charge_derivative':chargedot,'continuity_max_error':continuity,
     'old_Hamiltonian_matching_error':match_error,'old_chain_force_relative_errors':es,'all_F_endpoint_finite':True,
     'nonlinear_elimination_identity':'exact symbolic pass','parameters':{'length_kpc':model.length_kpc,'M':model.M,'h':model.h,'lambda':model.lam,'alpha':model.alpha,'g2':m.g2,'n':m.n},
     'non_claim':'No time-evolved formation, global hyperbolicity, or prediction of added parameters.'}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
