import argparse,json,math,pathlib
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--control',choices=['none','zero_flow','wrong_transition_flow','clock_equals_metric'],default='none');args=p.parse_args();rows=[]
def ck(n,ok,d=None):rows.append({'name':n,'passed':bool(ok),'detail':d})
def zero(n,e):ck(n,s.simplify(e)==0,str(s.simplify(e)))
r=s.symbols('r',positive=True);M,H,c,A,m,eta,q=s.symbols('M H c A m eta q',positive=True)
N=s.Function('N')(r);B=s.Function('B')(r);V=s.Function('V')(r);Np=s.diff(N,r);Bp=s.diff(B,r);Vp=s.diff(V,r);a=Np/(N*B);Q=s.Function('Q');U=-3*M*H**2+2*c*s.log(N)
L=M*(N*(B+1/B)+2*r*Np/B)-M*r*V**2*(Bp/N+B*Np/N**2)+N*B*r*r*U-2*c/(3*H)*B*r*r*V*Np/N+M*N*B*r*r*Q(a)
def EL(x):return s.diff(L,x)-s.diff(s.diff(L,s.diff(x,r)),r)
zero('exact_momentum',EL(V)+2*M*B*r/N*(V*(Bp/B+Np/N)+c*r*Np/(3*M*H)))
qprime=s.diff(Q(a),a) if False else s.Subs(s.Derivative(Q(s.Symbol('aa')),s.Symbol('aa')),s.Symbol('aa'),a)
Eb=M*(N*(1-B**-2)-2*r*Np/B**2+(V**2+2*r*V*Vp)/N-2*r*V**2*Np/N**2)-2*c/(3*H)*r*r*V*Np/N+N*r*r*U+M*N*r*r*(Q(a)-a*qprime)
En=M*(B-1/B+2*r*Bp/B**2+((B+2*r*Bp)*V**2+2*r*B*V*Vp)/N**2)+2*c/(3*H)*s.diff(B*r*r*V,r)/N+B*r*r*(U+2*c)+M*B*r*r*(Q(a)-a*qprime)-M*s.diff(r*r*qprime,r)
zero('exact_B_Euler',EL(B)-Eb);zero('exact_N_Euler',EL(N)-En)
jr=(2*c/(3*H*q))*(Np/B**2-3*H*V-V/N*(Vp+(Bp/B+2/r)*V))+M*V/(q*B*r*r)*s.diff(r*r*qprime,r)
zero('exact_zero_charge_dependency',q*B*r*r*jr+V*EL(N)-V*B/N*EL(B)+(V**2/N+N/B**2)*EL(V))
ss=m/r**2;aa=s.sqrt(ss*(ss+A));vv=-eta*H*r*(1+ss/A);Wa=s.sqrt(s.factor(aa*aa+A*A/4))-A/2
zero('P2_source_inversion',Wa-ss);zero('P2_log_derivative',r*s.diff(aa,r)+2*aa-A*ss/aa)
zero('forced_nonzero_flow',vv*(s.diff(aa,r)+2*aa/r)+eta*H*aa)
zero('deep_MOND_mass_exponent',m*s.diff(s.sqrt(m*A)/r,m)/(s.sqrt(m*A)/r)-s.Rational(1,2))
zero('deep_MOND_radius_exponent',r*s.diff(s.sqrt(m*A)/r,r)/(s.sqrt(m*A)/r)+1)
# Response variation yields current after integrating psi'' term.
P=s.Function('P')(r);Qp=s.Function('Qp')(r)
variation=M*r*r*Qp*s.diff(N*V*s.diff(P,r),r)/q
canonical=s.diff(variation,s.diff(P,r))-s.diff(s.diff(variation,s.diff(P,r,2)),r)
zero('exact_response_current_variation',canonical+M*N*V*s.diff(r*r*Qp,r)/q)
# Weak momentum/radial identities force the physical-force identity.
g=s.Function('g')(r);acc=s.Function('acc')(r);S=s.Function('S')(r)
b=r*g-S/2
zero('physical_force_identity',s.diff(b,r).subs(s.diff(S,r),2*(acc-g))-(r*s.diff(g,r)+2*g-acc))
# Leading total current cancellation; remainder explicitly nonzero, not claimed solved.
rem=-eta*H*(3*H*vv+vv*(s.diff(vv,r)+2*vv/r))
ck('subleading_scalar_current_not_zero',s.simplify(rem)!=0,str(s.simplify(rem)))
profiles=[]
for mm in [1e-24,1e-21,1e-18]:
 for factor in [10.,30.,100.]:
  AA=.2;hh=1.;ee=.5;rm=math.sqrt(mm/AA);rr=factor*rm;ssv=mm/rr**2;av=math.sqrt(ssv*(ssv+AA));Vpval=-ee*hh*rr*(1+ssv/AA);vp_der=-ee*hh*(1-ssv/AA)
  gflow=av-Vpval*vp_der+hh**2*rr
  flux=math.sqrt(av*av+AA*AA/4)-AA/2
  flow_ratio=abs(Vpval*vp_der-hh*hh*rr)/ssv
  braid_ratio=abs(ee*hh*(Vpval+hh*rr))/ssv
  pn_ratio=AA*rr
  profiles.append({'m':mm,'r_over_rM':factor,'a':av,'V':Vpval,'flow_omission_vs_massflux':flow_ratio,'braid_omission_vs_massflux':braid_ratio,'postNewton_estimate_Ar':pn_ratio,'physical_clock_difference':gflow-av})
  ck('bounded_P2_flux_'+str((mm,factor)),math.isclose(flux,ssv,rel_tol=2e-12))
  ck('bounded_weak_deep_window_'+str((mm,factor)),av/AA<.11 and abs(Vpval)<1e-5 and flow_ratio<.02 and braid_ratio<.02 and pn_ratio<1e-5)
if args.control=='zero_flow':zero('CONTROL_wrong_zero_flow',eta*H*aa)
if args.control=='wrong_transition_flow':zero('CONTROL_wrong_transition_flow',(-eta*H*r)*(s.diff(aa,r)+2*aa/r)+eta*H*aa)
if args.control=='clock_equals_metric':ck('CONTROL_wrong_exact_clock_metric_identity',all(x['physical_clock_difference']==0 for x in profiles))
result={'passed':all(x['passed'] for x in rows),'checks':rows,'profiles':profiles,'control':args.control,'non_claims':['Leading profiles are not exact solutions','Exterior m not yet proved equal baryonic mass','No angular/regular-center/global-matching proof','No finite-gradient stability','No32pi selector']};out=pathlib.Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'checks':len(rows),'failed':[x['name'] for x in rows if not x['passed']]}));raise SystemExit(0 if result['passed'] else 1)
