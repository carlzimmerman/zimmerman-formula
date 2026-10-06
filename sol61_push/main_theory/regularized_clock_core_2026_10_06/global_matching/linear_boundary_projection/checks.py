"""Exact real modified-Bessel boundary projection and independent finite linear ODE."""
import argparse,json,pathlib,hashlib,math
import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);pa.add_argument('--control',choices=['none','wronskian','drop_r2','C0_is_growing0'],default='none');args=pa.parse_args();mp.mp.dps=50
P=pathlib.Path(__file__).resolve().parents[1];eta=mp.mpf('.5');kap=mp.mpf('.99');mu=eta*(1-eta)/kap;nu=3*eta*eta/kap;alpha=mp.sqrt(nu);omega=mp.sqrt(mu-mp.mpf('.25'));sigma=1j*omega;checks=[]
def ck(n,b,d=None):checks.append(dict(name=n,passed=bool(b),detail=d))
def basis(r):
 z=alpha*r;I=mp.besseli(sigma,z);K=mp.besselk(sigma,z);Ip=(mp.besseli(sigma-1,z)+mp.besseli(sigma+1,z))/2;Kp=-(mp.besselk(sigma-1,z)+mp.besselk(sigma+1,z))/2
 return mp.re(I)/mp.sqrt(r),mp.re(K)/mp.sqrt(r),mp.re(-I/2+z*Ip)/mp.sqrt(r),mp.re(-K/2+z*Kp)/mp.sqrt(r)
def particular(r):
 term=1/(1-eta);value=term;k=mp.mpf(0);terms=1
 for j in range(1,121):
  term*=nu*r*r/((2*j)**2+2*j+mu);value+=term;k+=2*j*term;terms+=1
  if abs(term)<mp.mpf('1e-48'):break
 return value,k,terms
for rr in ['.003','.03','.3']:
 r=mp.mpf(rr);I,K,ki,kk=basis(r);det=I*kk-K*ki;ck('real_basis_Wronskian_'+rr,abs(det+1/r)<mp.mpf('1e-45'),str(det))
 ci=mp.besseli(sigma,alpha*r);ck('imaginaryI_is_K_'+rr,abs(mp.im(ci)+mp.sinh(mp.pi*omega)*K*mp.sqrt(r)/mp.pi)<mp.mpf('1e-45'))
 for ind,name in [(0,'I'),(1,'K')]:
  f=lambda x:basis(x)[ind];df=mp.diff(f,r);d2=mp.diff(f,r,2);err=r*r*d2+2*r*df+(mu-nu*r*r)*f(r);ck('Bessel_ODE_'+name+'_'+rr,abs(err)<mp.mpf('1e-44'),str(err))
 q,kq,nterms=particular(r);qp=lambda x:particular(x)[0];err=r*r*mp.diff(qp,r,2)+2*r*mp.diff(qp,r)+(mu-nu*r*r)*q-eta/kap;ck('regular_particular_ODE_'+rr,abs(err)<mp.mpf('1e-42'),str(err))
records=[];inputs=[]
for case in ['minus6_a','zero_b','plus_b']:
 path=P/'runs'/case/'results.json';inputs.append(path);d=json.loads(path.read_text());run=min(d['runs'],key=lambda z:z['tol']);r=mp.mpf(str(run['end_r']));L0=mp.mpf(str(d['lnN0']));y=run['end_state'];ell=mp.mpf(str(y[0]))+L0;b=mp.mpf(str(y[1]));k=mp.mpf(str(y[3]));C=b+(1-eta)*ell;I,K,ki,kk=basis(r);q,kq,nterms=particular(r);u=ell-C*q;v=k-C*kq;Wr=I*kk-K*ki;usedWr=-Wr if args.control=='wronskian' else Wr;AI=(u*kk-K*v)/usedWr;AK=(I*v-u*ki)/usedWr
 ck('endpoint_basis_reconstruction_'+case,max(abs(C*q+AI*I+AK*K-ell),abs(C*kq+AI*ki+AK*kk-k))<mp.mpf('1e-45'))
 # Integrate only the exact declared linear equation, not the nonlinear galaxy equations.
 errors=[];sols=[];evals=[]
 for rtol,atol in [(1e-10,1e-18),(1e-12,1e-20)]:
  def rhs(t,z):
   rr=math.exp(t);rrterm=0 if args.control=='drop_r2' else float(nu)*rr*rr
   return [z[1],-z[1]-(float(mu)-rrterm)*z[0]+float(eta*C/kap)]
  sol=solve_ivp(rhs,(math.log(float(r)),math.log(.3)),[float(ell),float(k)],method='DOP853',rtol=rtol,atol=atol,max_step=.1,dense_output=True);ck('finite_linear_IVP_'+case+'_'+str(rtol),sol.success);maxerr=0.;pts=[]
  for rr in np.geomspace(float(r),.3,31):
   mpr=mp.mpf(str(rr));qv,kqv,_=particular(mpr);iv,kv,kiv,kkv=basis(mpr);exact=np.array([float(C*qv+AI*iv+AK*kv),float(C*kqv+AI*kiv+AK*kkv)]);numeric=sol.sol(math.log(rr));err=float(np.max(np.abs(exact-numeric)));maxerr=max(maxerr,err)
   pts.append(dict(r=float(rr),exact=exact.tolist(),numerical=numeric.tolist(),absolute_error=err))
  ck('finite_exactbasis_vs_linearODE_'+case+'_'+str(rtol),maxerr<2e-16,maxerr);errors.append(maxerr);sols.append(sol.y[:,-1]);evals.append(sol.nfev)
 ck('linear_IVP_tolerance_refinement_'+case,float(np.max(np.abs(sols[0]-sols[1])))<2e-16)
 records.append(dict(case=case,L0=str(L0),r=str(r),ell=str(ell),b=str(b),k=str(k),C=str(C),AI_declared_regular_particular=str(AI),AK=str(AK),particular_normalization='p0=1/(1-eta), onlyevenpowers; nonzeroC AI not total growingamplitude',linear_IVP_errors=errors,linear_IVP_nfev=evals,linear_endpoint=sols[-1].tolist()))
# Source-central-lapse interpolation: C0 is separate from finiteell0; no nonlinear root executed.
a,b=records[:2]
def interp(key):
 q0=mp.mpf(a[key]);q1=mp.mpf(b[key]);f=-q0/(q1-q0)
 return {n:mp.mpf(a[n])+f*(mp.mpf(b[n])-mp.mpf(a[n])) for n in ['L0','ell','b','k','C']}
cz=interp('C');lz=interp('ell');r=mp.mpf(a['r']);I,K,ki,kk=basis(r);Wr=I*kk-K*ki;AI0=(cz['ell']*kk-K*cz['k'])/Wr;AK0=(I*cz['k']-cz['ell']*ki)/Wr;pureKratio=kk/K;boundary_residual=cz['k']-pureKratio*cz['ell'];targetell=cz['k']/pureKratio
ck('C0_interpolation',abs(cz['C'])<mp.mpf('1e-45'));ck('C0_still_has_I_mode',abs(AI0)>mp.mpf('1e-9'),str(AI0));ck('lapse0_differs_C0_target',abs(lz['L0']-cz['L0'])>mp.mpf('1e-7'));ck('independent_C0_pureK_condition',abs(boundary_residual)>mp.mpf('1e-8'),str(boundary_residual))
if args.control=='C0_is_growing0':ck('CONTROL_C0_does_not_imply_growing0',abs(AI0)<mp.mpf('1e-20'))
# Replacing p by p+dI changes extractedAI whenCneq0: no asymptoticclaim silentlyborrowed.
C=mp.mpf(records[1]['C']);AI=mp.mpf(records[1]['AI_declared_regular_particular']);ck('particular_convention_ambiguity',C!=0 and abs((AI-C)-AI)>mp.mpf('1e-6'))
result=dict(passed=all(z['passed'] for z in checks),checks=checks,precision_decimal_digits=50,parameters={n:str(v) for n,v in dict(eta=eta,kappa=kap,mu=mu,nu=nu,alpha=alpha,omega=omega).items()},endpoint_projections=records,C0_interpolation={n:str(v) for n,v in cz.items()},finite_lapse0_interpolation={n:str(v) for n,v in lz.items()},C0_mode_projection=dict(AI=str(AI0),AK=str(AK0),pureK_k_over_ell=str(pureKratio),actual_k_over_ell=str(cz['k']/cz['ell']),pureK_boundary_residual=str(boundary_residual),ell_required_at_fixedk=str(targetell)),control=args.control,input_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},non_claims=['No nonlinear sourcecentralshoot atinterpolatedroot','FiniteODE test is linear, not actualnonlinearcontinuation','No rtoinfinity/horizoncosmicmatching theorem','NonzeroC growingamplitude requiresparticularconvention','No universalA/body no-go or32piselection'])
p=pathlib.Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=result['passed'],checks=len(checks),failed=[z['name'] for z in checks if not z['passed']],C0_AI=str(AI0))));raise SystemExit(0 if result['passed'] else 1)
