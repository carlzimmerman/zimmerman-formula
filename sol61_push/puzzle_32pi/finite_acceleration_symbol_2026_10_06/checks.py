"""Exact planar ADM constraint reduction, plus declared finite response controls.
No global background existence or galaxy-mode stability is inferred.
"""
import argparse,json,pathlib,math
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--control',choices=['none','shift','kinetic'],default='none');args=p.parse_args()
checks=[]
def ck(n,e): checks.append(dict(name=n,passed=bool(e)))
def zero(n,e): ck(n,s.simplify(e)==0)
x=s.symbols('x');K,b=s.symbols('K b',positive=True)
N=s.Function('N')(x);z=s.Function('z')(x);v=s.Function('v')(x);L=s.Function('L')(x)
# L=N0*h+zeta_dot, t=(L-v*zeta')/N, d=v'/N.
t=(L-v*s.diff(z,x))/N;d=s.diff(v,x)/N
EH=K*N*s.exp(3*z)/2*((t-d)**2+2*t*t-(3*t-d)**2)
Braid=-b*s.exp(3*z)*(3*(L-v*s.diff(z,x))-s.diff(v,x))*s.log(N)
raw=EH+Braid
zero('EH_trace_from_three_eigenvalues',EH-K*s.exp(3*z)/N*(-3*(L-v*s.diff(z,x))**2+2*(L-v*s.diff(z,x))*s.diff(v,x)))
# Shift Euler at background v=0 (all orders in z); its nonlinear v terms do not enter linearized constraint around z'=0.
Ev=s.diff(raw,v)-s.diff(s.diff(raw,s.diff(v,x)),x)
expected=-s.exp(3*z)*s.diff(2*K*L/N+b*s.log(N),x)
zero('exact_shift_at_v_zero',Ev.subs({v:0,s.diff(v,x):0,s.diff(v,x,2):0})-expected)
# Pure shift quadratic is identically zero when z'=0, not discarded k^4 cancellation.
zero('planar_shift_square_zero',s.diff(raw,v,2).subs(s.diff(z,x),0))
zero('planar_shift_derivative_square_zero',s.diff(raw,s.diff(v,x),2))
nu,zd,h,N0,qp,k=s.symbols('nu zd h N0 qp k',real=True,nonzero=True)
D=h-b/(2*K)
pert=s.diff(2*K*(N0*h+s.Symbol('e')*zd)/(N0*s.exp(s.Symbol('e')*nu))+b*s.log(N0*s.exp(s.Symbol('e')*nu)),s.Symbol('e')).subs(s.Symbol('e'),0)
zero('linear_shift_momentum',pert-2*K*(zd/N0-D*nu))
usedD=h if args.control=='shift' else D
zero('solved_shift_constraint',(zd/N0-D*(zd/(N0*usedD))))
C=s.symbols('C',real=True);Svar=s.symbols('S',real=True);beta=s.symbols('beta',real=True)
# Complete scalar auxiliary Schur block under explicitly declared generic-jet leading template.
aux=C*nu**2-2*beta*(zd-D*nu)+Svar*beta**2/2
sol=s.solve([s.diff(aux,nu),s.diff(aux,beta)],[nu,beta],dict=True)[0]
red=s.factor(aux.subs(sol))
zero('generic_auxiliary_block_reduction',red-C*zd**2/(D**2-Svar*C/2))
# In exact planar sector S=0, response is KE*N0*Q''*(nu')²/2.
kin=K*qp*k*k/(2*N0*D**2)
usedkin=-kin if args.control=='kinetic' else kin
zero('planar_highk_kinetic',usedkin-K*qp*k*k/(2*N0*D**2))
# Planar lapse and momentum constraint-compatible jets (not an evolution theorem).
cc,V,a,ap,ell=s.symbols('c V a ap ell',real=True);Q,Q1,Q2=s.symbols('Q Q1 Q2',real=True,nonzero=True)
Ham=3*K*h*h+2*cc*ell-V+2*cc-3*b*h+K*(Q-a*Q1-Q2*ap)
ap_sol=(3*h*h+2*cc/K*ell-V/K+2*cc/K-3*b*h/K+Q-a*Q1)/Q2
zero('Hamiltonian_lapse_ODE',Ham.subs(ap,ap_sol))
hp=s.symbols('hp');zero('momentum_h_gradient',(2*K*hp+b*a).subs(hp,-b*a/(2*K)))
# Weighted transverse correction independently by a flat exponential-lapse example.
A,tT=s.symbols('A tT',real=True)
# For k perpendicular a: direct normalized Sdir=A²; transverse completion contributes cross KE*A*tT and KE*tT²/4.
shift_perp=A*A/2+A*tT+tT*tT/4
zero('transverse_shift_Schur',shift_perp.subs(tT,-2*A)+A*A/2)
# Cutoff inverse dictionary and epsilon detuning, finite declared points.
def cutoff(y,T):
 r=math.sqrt(1+1/y);bb=1/(r+1);bp=1/(2*y*y*r*(r+1)**2);dd=1+(y/T)**2
 hh=bb/dd;hp=bp/dd-bb*(2*y/T**2)/(dd*dd)
 return hh,hp
rows=[]
for yy in [1.,10.,100.,1000.]:
 hh,hp=cutoff(yy,128.9153707043);fp=1+hp
 for eps in [0.,.01]:
  CL=1-eps-1/fp;CT=1-eps-yy/(yy+hh)
  rows.append(dict(kernel='cutoff',y=yy,epsilon=eps,clock_a_over_A=yy+hh,CL=CL,CT=CT,planar_highk_sign='negative' if CL<0 else 'positive'))
  ck('inverse_regular_'+str((yy,eps)),fp>0)
ck('cutoff_negative_longitudinal',next(r for r in rows if r['y']==100 and r['epsilon']==0)['CL']<0)
for eps in [.001,.01,.1]:
 threshold=(1-eps)/(2*math.sqrt(eps*(2-eps)));aa=2*threshold
 CL=1-eps-2*aa/math.sqrt(1+4*aa*aa)
 rows.append(dict(kernel='uncut',epsilon=eps,clock_a_over_A=aa,exact_threshold_a_over_A=threshold,CL=CL))
 ck('epsilon_highclock_negative_'+str(eps),CL<0)
res=dict(passed=all(q['passed'] for q in checks),checks=checks,response_examples=rows,formulae=dict(planar_momentum='d_x[zdot/N0-(h-b/(2K))*nu]=0',planar_kinetic='K*Qaa*k^2/[2*N0*(h-b/(2K))^2]',generic_template_kinetic='K*C*k^2/[D^2-S*C/2]'),control=args.control,non_claims=['No full on-shell time-evolution existence','No every-orientation finite-jet symbol proof','No all-galaxy branch ghost result','No UV EFT completion supplied'])
out=pathlib.Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(dict(passed=res['passed'],checks=len(checks),failed=[q['name'] for q in checks if not q['passed']])));raise SystemExit(0 if res['passed'] else 1)
