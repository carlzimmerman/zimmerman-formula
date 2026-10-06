"""Exact unfixed-radius spherical ADM variation plus high-precision residual controls.
No bounded residual control is an existence proof or a nonlinear force fit.
"""
import argparse,json
from pathlib import Path
import sympy as s
import mpmath as mp
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True,type=Path);ap.add_argument('--mutation',choices=['none','drop_braid_momentum','use_lapse_potential'],default='none');args=ap.parse_args();base=Path(__file__).resolve().parent;out=args.output_dir.resolve();out.relative_to(base);out.mkdir(parents=True,exist_ok=True)
r=s.symbols('r',positive=True);K,c,b,H,A,Veff=s.symbols('K c b H A Veff',positive=True)
N=s.Function('N')(r);B=s.Function('B')(r);V=s.Function('V')(r);R=s.Function('R')(r)
D=s.diff(V,r)+s.diff(B,r)*V/B;E=V*s.diff(R,r)/R
# Signed N'>0 local branch. The exact response is C2 at zero; use |N'| for other signs.
g=s.diff(N,r)/(N*B);U=s.Function('U');S=2*c*s.log(N)-Veff+U(g)
L=K*(N*B+N*s.diff(R,r)**2/B+2*s.diff(N,r)*R*s.diff(R,r)/B-B*(2*R*s.diff(R,r)*V*D+s.diff(R,r)**2*V**2)/N)+N*B*R**2*S-b*B*R**2*V*s.diff(N,r)/N
checks={}
def ck(n,v):checks[n]=bool(v);print(('PASS ' if v else 'FAIL ')+n)
def el(q):return s.diff(L,q)-s.diff(s.diff(L,s.diff(q,r)),r)
EN,EB,EV,ER=[s.simplify(el(q)) for q in [N,B,V,R]]
EVexpected=2*K*B*R*s.diff(R,r)*V/N*(s.diff(R,r,2)/s.diff(R,r)-s.diff(B,r)/B-s.diff(N,r)/N)-b*B*R**2*s.diff(N,r)/N
if args.mutation=='drop_braid_momentum':EVexpected+=b*B*R**2*s.diff(N,r)/N
ck('unfixed_momentum_equation',s.simplify(EV-EVexpected)==0)
identity=EN*s.diff(N,r)+ER*s.diff(R,r)+2*s.diff(V,r)*EV+V*s.diff(EV,r)-B*s.diff(EB,r)
ck('lost_angular_radial_Noether_identity',s.simplify(identity)==0)
subR={R:r,s.diff(R,r):1,s.diff(R,r,2):0,s.diff(R,r,3):0}
ENa=s.simplify(EN.subs(subR));EBa=s.simplify(EB.subs(subR));EVa=s.simplify(EV.subs(subR));ERa=s.simplify(ER.subs(subR))
F=N*N-B*B*V*V
Ug=s.diff(U(g),g) if False else s.Subs(s.Derivative(U(s.Symbol('x')),s.Symbol('x')),s.Symbol('x'),g)
# Combine B equation with exact momentum to remove all braid terms.
combo=s.expand(N*B*B*EBa-N*B*V*EVa)
expected=K*((N*B)**2-s.diff(r*F,r))+(N*B)**2*r*r*(S-g*Ug)
ck('exact_physical_Killing_constraint',s.simplify(combo-expected)==0)
# Independently derived stationary shift-current and stress/energy-flux identity.
jrq=b*(s.diff(N,r)/B**2-3*H*V-V/N*(s.diff(V,r)+(s.diff(B,r)/B+2/r)*V))+V/(B*r*r)*s.diff(r*r*Ug,r)
fluxcombo=-N*V*ENa+B*V*EBa-(N*N/(B*B)+V*V)*EVa
ck('stationary_current_full_metric_identity',s.simplify((fluxcombo-N*B*r*r*jrq).subs(c,3*b*H/2))==0)
# Direct areal action after an additional V' IBP agrees up to total derivative.
La=s.simplify(L.subs(subR));Lcompact=K*(N*(B+1/B)+2*r*s.diff(N,r)/B-r*V*V*(s.diff(B,r)/N+B*s.diff(N,r)/(N*N)))+N*B*r*r*S-b*B*r*r*V*s.diff(N,r)/N
ck('areal_shift_integration_by_parts',s.simplify(La-Lcompact+s.diff(K*B*r*V*V/N,r))==0)
# DeSitter exact benchmark, response vanishes along N'=0. replace U through a polynomial surrogate with same jets.
L0=Lcompact.replace(lambda e:e.func==U,lambda e:K*e.args[0]**2)
def el0(q):return s.simplify(s.diff(L0,q)-s.diff(s.diff(L0,s.diff(q,r)),r))
E0=[el0(q) for q in [N,B,V]]
subs={N:1,B:1,V:-H*r,Veff:3*K*H*H,b:2*c/(3*H)}
ck('exact_flat_slicing_deSitter_benchmark',all(s.simplify(e.subs(subs).doit())==0 for e in E0))
# Formal deep-MOND flow candidate satisfies momentum exactly, not the full equations.
eta,Lam,r0=s.symbols('eta Lam r0',positive=True)
Nc=(r/r0)**Lam;Bc=1+Lam;Vc=-eta*H*r*Nc
cand={N:Nc,B:Bc,V:Vc,b:2*K*eta*H,c:3*K*eta*H*H,Veff:3*K*H*H}
ck('formal_MOND_flow_exact_momentum',s.simplify(EVa.subs(cand).doit())==0)
Fc=Nc*Nc-Bc*Bc*Vc*Vc
circular=s.simplify(r*s.diff(Fc,r)/(2*Fc))
expectedcirc=Lam-Bc*Bc*eta*eta*H*H*r*r/(1-Bc*Bc*eta*eta*H*H*r*r)
if args.mutation=='use_lapse_potential':expectedcirc=Lam
ck('physical_circularspeed_not_lapse_only',s.simplify(circular-expectedcirc)==0)
# Exact W response and its pressure inequality: 0<Wgg<1 => 0<gWg-W<g²/2.
x=s.symbols('x',positive=True);W=(x*s.sqrt(x*x+A*A/4)+A*A*s.asinh(2*x/A)/4)/2-A*x/2
Wg=s.diff(W,x);Uexact=K*x*x-2*K*W
ck('response_pressure_legendre_identity',s.simplify(Uexact-x*s.diff(Uexact,x)-2*K*(x*Wg-W-x*x/2))==0)
# Substitute g before differentiating to retain all N/B dependence.
Lfull=Lcompact.replace(lambda e:e.func==U,lambda e:Uexact.subs(x,e.args[0]))
Efull=[s.diff(Lfull,q)-s.diff(s.diff(Lfull,s.diff(q,r)),r) for q in [N,B,V]]
exprs=[s.simplify(e.subs(cand).doit()) for e in Efull]
mp.mp.dps=70
funcs=[s.lambdify((r,K,H,A,eta,Lam,r0),e,'mpmath') for e in exprs]
controls=[]
# m, H, A set independently; L²=m A is a proposed source normalization, not proved matching.
for mm in ['1e-12','1e-18']:
 m=mp.mpf(mm);hh=mp.mpf(1);aa=mp.mpf(1);ee=mp.mpf('.5');ll=mp.sqrt(m*aa);lo=10*ll/aa;hi=lo*2;rr0=mp.sqrt(lo*hi)
 fN=lambda rr:funcs[0](rr,1,hh,aa,ee,ll,rr0)
 integ=mp.quad(fN,[lo,hi])/(2*m)
 vals=[]
 for j in range(9):
  rr=lo*(hi/lo)**(mp.mpf(j)/8);nc=(rr/rr0)**ll;bn=1+ll
  en,eb,ev=[ff(rr,1,hh,aa,ee,ll,rr0) for ff in funcs]
  gc=ll/(bn*rr);wg=mp.sqrt(gc*gc+aa*aa/4)-aa/2
  vals.append({'r':str(rr),'clock_g_over_A':str(gc/aa),'cosmic_flux_ratio_H2r3_over_m':str(hh*hh*rr**3/m),'radial_spatial_residual_over_KNL':str(eb/(nc*ll)),'momentum_residual':str(ev),'proposed_flux_relative_defect':str(wg*rr*rr/m-1),'circularspeed_squared':str(ll-bn*bn*ee*ee*hh*hh*rr*rr/(1-bn*bn*ee*ee*hh*hh*rr*rr))})
 controls.append({'m':str(m),'L':str(ll),'H':str(hh),'A':str(aa),'eta':str(ee),'r_min':str(lo),'r_max':str(hi),'integrated_lapse_residual_over_source_flux':str(integ),'samples':vals})
ck('bounded_formal_flow_residual_controls',all(abs(mp.mpf(z['integrated_lapse_residual_over_source_flux']))<mp.mpf('.1') and all(abs(mp.mpf(v['proposed_flux_relative_defect']))<mp.mpf('.02') for v in z['samples']) for z in controls))
(out/'equations.txt').write_text('L_unfixed='+str(L)+'\nE_N_areal='+str(ENa)+'\nE_B_areal='+str(EBa)+'\nE_V_areal='+str(EVa)+'\nE_R_areal='+str(ERa)+'\n')
res={'checks':checks,'formal_candidate_residual_controls':controls,'mutation':args.mutation,'arithmetic':'SymPy exact, mpmath70digits','limitations':['Formal ansatz residuals are not an exact solution','No source-interior matching or global boundary continuation','L²=mA proposed charge not independently measured GN determination','No finite-gradient health or 32pi selector']};(out/'results.json').write_text(json.dumps(res,indent=2)+'\n');raise SystemExit(0 if all(checks.values()) else 1)
