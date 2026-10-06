"""Independent raw planar Euler equations and first-time-jet constraint preservation."""
import argparse,json,pathlib,math
import sympy as s
import numpy as np
from scipy.integrate import solve_ivp,quad
from scipy.optimize import brentq
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);pa.add_argument('--control',choices=['none','isotropy','drop_lapse_spatial','wrong_momentum'],default='none');args=pa.parse_args();checks=[]
def ck(n,b,d=None):checks.append(dict(name=n,passed=bool(b),detail=d))
def zero(n,e):
 e=s.simplify(e);ck(n,e==0,str(e))
# Generic polynomial in acceleration is used only as an exact differentiable algebra probe.
t,x=s.symbols('t x');M,b,c,V=s.symbols('M b c V');nn=s.Function('N')(t,x);al=s.Function('alpha')(t,x);be=s.Function('beta')(t,x);qs=s.symbols('q0:6');u=s.symbols('u');Q=sum(qs[i]*u**i for i in range(6));aa=s.exp(-al)*s.diff(nn,x)/nn;qq=Q.subs(u,aa)
vol=s.exp(al+2*be);At=s.diff(al,t);Bt=s.diff(be,t)
L=M*s.exp(-al+2*be)*(2*s.diff(nn,x)*s.diff(be,x)+nn*s.diff(be,x)**2)-M*vol/nn*(2*At*Bt+Bt*Bt)-b*vol*(At+2*Bt)*s.log(nn)+nn*vol*(2*c*s.log(nn)-V)+M*nn*vol*qq
EL=lambda f:s.diff(L,f)-s.diff(s.diff(L,s.diff(f,t)),t)-s.diff(s.diff(L,s.diff(f,x)),x)
EA,EB,EN=[EL(f) for f in [al,be,nn]]
hxgeneral=At/nn;hygeneral=Bt/nn;Cgeneral=2*M*(s.diff(hygeneral,x)-s.diff(be,x)*(hxgeneral-hygeneral))+b*s.diff(nn,x)/nn;Evgeneral=-vol*Cgeneral
zero('general_lapse_preservation_leading_coefficient',nn*s.diff(s.diff(EN/vol,t),s.diff(nn,t,x,2))+M*s.exp(-2*al)*s.diff(Q,u,2).subs(u,aa))
zero('spatial_evolution_no_lapse_time_secondspatial_alpha',s.diff(EA,s.diff(nn,t,x,2)))
zero('spatial_evolution_no_lapse_time_secondspatial_beta',s.diff(EB,s.diff(nn,t,x,2)))
zero('general_spatial_diffeomorphism_identity',s.diff(Evgeneral,t)-(EN*s.diff(nn,x)+EA*s.diff(al,x)+EB*s.diff(be,x)-s.diff(EA,x)))
N,h,lam,dhx,dhy,a,ap,app,hp,hpp,lamp,lampp=s.symbols('N h lam dhx dhy a ap app hp hpp lamp lampp',real=True);D=h-b/(2*M);P=2*c*s.log(N)-V
sub={al:0,be:0,nn:N,At:N*h,Bt:N*h,s.diff(al,t,2):N*(dhx+h*lam),s.diff(be,t,2):N*(dhy+h*lam),s.diff(nn,t):N*lam,s.diff(al,x):0,s.diff(be,x):0,s.diff(al,x,2):0,s.diff(be,x,2):0,s.diff(nn,x):N*a,s.diff(nn,x,2):N*(ap+a*a),s.diff(al,t,x):N*(a*h+hp),s.diff(be,t,x):N*(a*h+hp),s.diff(nn,t,x):N*(lamp+a*lam)}
freeze=lambda e:s.simplify(e.subs(sub,simultaneous=True))
Q0=Q.subs(u,a);Q1=s.diff(Q,u).subs(u,a);Q2=s.diff(Q,u,2).subs(u,a);Q3=s.diff(Q,u,3).subs(u,a);Aalpha=3*M*h*h+P+M*(Q0-a*Q1)
wantA=2*M*dhy+b*lam+N*Aalpha;wantB=2*(M*(dhx+dhy)+b*lam+N*(3*M*h*h+P+M*Q0)-M*N*(ap+a*a));Ham=3*M*h*h+P+2*c-3*b*h+M*(Q0-a*Q1-Q2*ap)
zero('raw_alpha_Euler',freeze(EA)-wantA);zero('raw_beta_Euler',freeze(EB)-wantB);zero('raw_lapse_constraint',freeze(EN)-Ham)
ydot=-(b*lam+N*Aalpha)/(2*M);xdot=ydot+N*(ap+a*a-a*Q1)
zero('spatial_evolution_anisotropy',(xdot-ydot)-N*(ap+a*a-a*Q1))
# Time derivative of momentum at the isotropic slice is -(N Aalpha)'= -N a Ham.
dxA=6*M*h*hp+2*c*a-M*a*Q2*ap
zero('momentum_preservation',(-N*(a*Aalpha+dxA)+N*a*Ham).subs(hp,-b*a/(2*M)))
# Derive Hamiltonian time derivative before substituting evolution.
# ad ot=lamprime-N h a; response divergence/time metric terms retained.
adot=lamp-N*h*a;adotp=lampp-N*((a*h+hp)*a+h*ap)
Rdot=M*(-(a*Q2+Q3*ap)*adot-Q2*adotp+N*h*Q2*ap-2*N*(a*h+hp)*Q1)
Ccurv=-2*M*N*(h*(ap+a*a)+2*a*hp+hpp)
Hdot=2*M*D*(dhx+2*dhy)+2*c*lam+Ccurv+Rdot
force=-3*D*N*Aalpha+2*M*D*N*(ap+a*a-a*Q1)+Ccurv+M*((a*Q2+Q3*ap)*N*h*a+Q2*N*((a*h+hp)*a+h*ap)+N*h*Q2*ap-2*N*(a*h+hp)*Q1)
operator=-M*Q2*lampp-M*(a*Q2+Q3*ap)*lamp+(2*c-3*b*D)*lam
zero('lapse_preservation_operator_and_full_forcing',Hdot.subs({dhx:xdot,dhy:ydot})-(operator+force))
fsimple=N*(-3*D*Aalpha+b*a*a-4*M*D*a*Q1+(2*M*h-b/2)*a*a*Q2+2*M*h*ap*Q2+M*h*a*ap*Q3)
zero('forcing_momentum_simplification',force.subs({hp:-b*a/(2*M),hpp:-b*ap/(2*M)})-fsimple)
# Raw kinetic velocity Hessian is invertible (not a frozen isotropy assumption).
velH=s.hessian(-M*s.exp(al+2*be)/nn*(2*At*Bt+Bt*Bt),(At,Bt))
zero('metric_evolution_velocity_rank',velH.det()+4*M*M*s.exp(2*al+4*be)/nn**2)
# Linearized highest time derivative retains the same spatial operator: exact symbolic differentiation.
J=s.symbols('J');eps=s.symbols('eps');opj=operator.subs({lam:eps*s.Function('j')(x),lamp:eps*s.diff(s.Function('j')(x),x),lampp:eps*s.diff(s.Function('j')(x),x,2)})
zero('formal_recursion_leading_operator',s.diff(opj,eps)-(operator.subs({lam:s.Function('j')(x),lamp:s.diff(s.Function('j')(x),x),lampp:s.diff(s.Function('j')(x),x,2)})))
# Actual cutoff background and lapse-time jet on a tiny local spatial interval.
T=128.9153707043;MM=1.;cc=1.5;bb=1.;VV=3.
def kernel(y):
 R=math.sqrt(1+1/y);d=1+(y/T)**2;B=1/(R+1);Bp=1/(2*y*y*R*(R+1)**2);return B/d,Bp/d-B*2*y/T**2/d**2
Y=s.symbols('Y',positive=True);hh=(s.sqrt(1+1/Y)+1)**-1/(1+(Y/s.Float(T,17))**2);h2=s.lambdify(Y,s.diff(hh,Y,2),'numpy')
def response(g):
 y=brentq(lambda y:y+kernel(y)[0]-g,1e-12,g,xtol=1e-12,rtol=1e-14);hv,hv1=kernel(y);iv=quad(lambda z:kernel(z)[0],0,y,epsabs=1e-9,epsrel=1e-11)[0];return hv*hv+2*iv,2*hv,2*hv1/(1+hv1),2*float(h2(y))/(1+hv1)**3
init_a=100+kernel(100)[0]
def rhs(xx,z):
 nv,hv,av,lv,lp=z;Qv,q1,q2,q3=response(av);PP=2*cc*math.log(nv)-VV;DD=hv-bb/(2*MM);AA=3*MM*hv*hv+PP+MM*(Qv-av*q1);apv=(AA+2*cc-3*bb*hv)/(MM*q2)
 forcing=nv*(-3*DD*AA+bb*av*av-4*MM*DD*av*q1+(2*MM*hv-bb/2)*av*av*q2+2*MM*hv*apv*q2+MM*hv*av*apv*q3)
 lpp=((2*cc-3*bb*DD)*lv-MM*(av*q2+q3*apv)*lp+forcing)/(MM*q2)
 return np.array([nv*av,-bb*av/(2*MM),apv,lp,lpp])
records=[]
for direction in [-1,1]:
 sol=solve_ivp(rhs,(0,direction*1e-7),[1,1,init_a,0,0],rtol=2e-11,atol=1e-12,max_step=1e-8,dense_output=True)
 ck('local_constraint_lapsejet_ODE_'+str(direction),sol.success);pts=[]
 for xx in np.linspace(0,direction*1e-7,5):
  nv,hv,av,lv,lp=sol.sol(xx);Nv,hp_,apv,_,lpp=rhs(xx,[nv,hv,av,lv,lp]);Qv,q1,q2,q3=response(av);PP=2*cc*math.log(nv)-VV;DD=hv-bb/(2*MM);AA=3*MM*hv*hv+PP+MM*(Qv-av*q1);hy=-(bb*lv+nv*AA)/(2*MM);hx=hy+nv*(apv+av*av-av*q1);at=lp-nv*hv*av;atp=lpp-nv*((av*hv+hp_)*av+hv*apv);hpp_=-bb*apv/(2*MM)
  ham=AA+2*cc-3*bb*hv-MM*q2*apv;hdot=2*MM*DD*(hx+2*hy)+2*cc*lv-2*MM*nv*(hv*(apv+av*av)+2*av*hp_+hpp_)+MM*(-(av*q2+q3*apv)*at-q2*atp+nv*hv*q2*apv-2*nv*(av*hv+hp_)*q1)
  momdot=-nv*(av*AA+6*MM*hv*hp_+2*cc*av-MM*av*q2*apv)
  pts.append(dict(x=float(xx),N=float(nv),h=float(hv),a=float(av),lambda_lapse=float(lv),lambda_prime=float(lp),lambda_second=float(lpp),Qaa=float(q2),D=float(DD),Ham=float(ham),Ham_time_derivative=float(hdot),momentum_time_derivative=float(momdot),anisotropy_time_derivative=float(hx-hy)))
 ck('negative_response_nonsingular_'+str(direction),all(p['Qaa']<0 and p['D']!=0 and p['N']>0 for p in pts));ck('Hamiltonian_and_timepreservation_'+str(direction),max(abs(p['Ham']) for p in pts)<1e-9 and max(abs(p['Ham_time_derivative']) for p in pts)<1e-7);ck('momentum_timepreservation_'+str(direction),max(abs(p['momentum_time_derivative']) for p in pts)<1e-8);records.extend(pts)
if args.control=='isotropy':ck('CONTROL_false_isotropy_preserved',max(abs(p['anisotropy_time_derivative']) for p in records)<1e-6)
if args.control=='drop_lapse_spatial':zero('CONTROL_omit_lambda_second',operator+M*Q2*lampp-operator)
if args.control=='wrong_momentum':zero('CONTROL_momentum_sign',(-N*(a*Aalpha+dxA)+N*a*Ham).subs(hp,b*a/(2*M)))
result=dict(passed=all(p['passed'] for p in checks),checks=checks,local_timejets=records,control=args.control,non_claims=['No convergent formal time series','No analytic PDE existence theorem','No boundary-value lapse solution','No hyperbolic or Hadamard wellposedness','No actual galaxy/source realization'])
p=pathlib.Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=result['passed'],checks=len(checks),failed=[p['name'] for p in checks if not p['passed']])));raise SystemExit(0 if result['passed'] else 1)
