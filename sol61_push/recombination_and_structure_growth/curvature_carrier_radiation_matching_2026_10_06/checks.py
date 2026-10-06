import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--mutation',choices=['omit_improvement','discard_phase_match','call_prescribed_GR_on_shell']);args=ap.parse_args();rows=[]
def ck(n,b,e=''):rows.append({'name':n,'passed':bool(b),'detail':str(e)})
def eq(n,e):e=s.simplify(s.expand(e));ck(n,e==0,e)
t,te,M,xi,fe,ae=s.symbols('t te M xi fe ae',positive=True);w=s.symbols('w',real=True);z=s.symbols('z',positive=True);y=s.symbols('y',nonnegative=True)
# Chi_e phase chosen real by exact U1 symmetry, |Chi_e|²=fe.
ce=s.sqrt(fe);taue=4*te/3
C1=s.Rational(3,4)*ce*s.sqrt(te)*(1-2*s.I*w)
C0=ce*(s.Rational(1,4)+s.Rational(3,2)*s.I*w)
if args.mutation=='discard_phase_match':C0=s.re(C0);C1=s.re(C1)
chi=C0+C1/s.sqrt(t);H=1/(2*t)
eq('field_match',chi.subs(t,te)-ce)
eq('derivative_match',s.diff(chi,t).subs(t,te)-ce*(-s.Rational(1,2)+s.I*w)/taue)
eq('radiation_scalar_EL',s.diff(chi,t,2)+3*H*s.diff(chi,t))
Rrad=6*(s.diff(H,t)+2*H**2)
eq('radiation_R_zero',Rrad)
tau=t+te/3;Heds=2/(3*tau);Reds=6*(s.diff(Heds,t)+2*Heds**2)
eq('continuous_H',Heds.subs(t,te)-H.subs(t,te))
eq('finite_curvature_jump',Reds.subs(t,te)-3/(4*te**2))
# Scalar acceleration jump from real stepR, continuouschi/chidot.
eds_dd=ce*((-s.Rational(1,2)+s.I*w)**2-(-s.Rational(1,2)+s.I*w))/taue**2
jump=s.diff(chi,t,2).subs(t,te)-eds_dd
# radiation minusEdS = +xi Rstepchi.
eq('scalar_second_derivative_step',s.expand(jump-xi*3*ce/(4*te**2)).subs(w**2,4*xi/3-s.Rational(1,4)))
ff=s.expand(chi*s.conjugate(chi));gz=s.expand(ff.subs(t,te/z**2)/fe)
eq('amplitude_profile',gz-((s.Rational(1,4)+3*z/4)**2+(3*w/2)**2*(z-1)**2))
G=s.expand(gz).subs(w**2,4*xi/3-s.Rational(1,4))
eq('reduced_profile',G-(3*xi*(z-1)**2+s.Rational(3,2)*z-s.Rational(1,2)))
eq('positive_past_derivative',s.diff(G,z)-6*xi*(z-1)-s.Rational(3,2))
sigma=s.symbols('sigma',positive=True);de=sigma/(4*xi)
Dy=de*G.subs(z,y+1)
eq('fraction_profile',Dy-(3*sigma*y**2/4+3*sigma*y/(8*xi)+sigma/(4*xi)))
eq('large_xi_profile',s.limit(Dy,xi,s.oo)-3*sigma*y**2/4)
b=3*de/2;a=3*xi*de;root=(-b+s.sqrt(b*b+4*a*(1-de)))/(2*a)
eq('positive_root_exact',a*root**2+b*root+de-1)
eq('root_large_xi',s.limit(root,xi,s.oo)-2/s.sqrt(3*sigma))
eq('finite_start_bound',4*xi/G.subs(z,y+1)-4*xi/(1+3*y/2+3*xi*y*y))
# Direct full covariant stress for complexχ, L=-|dχ|²−xiR|χ|².
kin=s.expand(s.diff(chi,t)*s.conjugate(s.diff(chi,t)))
f=ff;fd=s.diff(f,t);fdd=s.diff(f,t,2)
G00=3*H*H;Gii=-(2*s.diff(H,t)+3*H*H)
imp_rho=2*xi*(G00*f+3*H*fd)
imp_p=2*xi*(Gii*f-fdd-2*H*fd)
rho=kin+(0 if args.mutation=='omit_improvement' else imp_rho)
pressure=kin+(0 if args.mutation=='omit_improvement' else imp_p)
C02=s.expand(C0*s.conjugate(C0));C12=s.expand(C1*s.conjugate(C1))
eq('raw_full_radiation_rho',rho-3*xi*C02/(2*t**2)-(s.Rational(1,4)-3*xi/2)*C12/t**3)
eq('raw_full_radiation_pressure',pressure-xi*C02/(2*t**2)-(s.Rational(1,4)-3*xi/2)*C12/t**3)
eq('stress_conservation',s.diff(rho,t)+3*H*(rho+pressure))
eq('matched_constant_amplitude',C02.subs(w*w,4*xi/3-s.Rational(1,4))-fe*(3*xi-s.Rational(1,2)))
eq('matched_decaying_amplitude',C12.subs(w*w,4*xi/3-s.Rational(1,4))-3*xi*fe*te)
rhorad=3*M/(4*t*t);prad=M/(4*t*t);de_actual=2*xi*fe/M
rr=s.expand(rho/rhorad).subs(w*w,4*xi/3-s.Rational(1,4)).subs(t,te/z**2)
pp=s.expand(pressure/prad).subs(w*w,4*xi/3-s.Rational(1,4)).subs(t,te/z**2)
eq('matched_rho_ratio',rr-de_actual*(3*xi-s.Rational(1,2))*(1-z*z))
eq('matched_pressure_ratio',pp-de_actual*(3*xi-s.Rational(1,2))*(1-3*z*z))
eq('join_density_zero',rr.subs(z,1))
eq('nonzero_carrier_trace_formula',-rho+3*pressure-2*(s.Rational(1,4)-3*xi/2)*C12/t**3)
if args.mutation=='call_prescribed_GR_on_shell':eq('full_pressure_must_vanish_for_prescribed_GR',pp.subs(z,1))
# Q without conventionalfactor2: a³ Imχ*χdot.
Q=s.simplify(ae**3*(t/te)**s.Rational(3,2)*s.im(s.conjugate(chi)*s.diff(chi,t)))
eq('charge_conserved',s.diff(Q,t))
eq('charge_matching',Q-ae**3*fe*w/taue)
# Finite numeric examples are illustrative exactradicalevaluation, no realcosmicfit.
examples=[]
for xx in [1,10,100,1000,1000000]:
 ss=s.Rational(2,5);yy=root.subs({sigma:ss,xi:xx});zz=1+yy;fraction=1/zz**2
 back=1/(1+1/((ss/(4*xx))*(3*xx-s.Rational(1,2))))
 vals={'xi':xx,'S_over_M':float(ss),'delta_e':float(ss/(4*xx)),'z_F_zero':float(zz),'t_F_zero_over_te':float(fraction),'t_density_backreaction_over_te':float(back),'join_pressure_over_rad':float(-2*(ss/(4*xx))*(3*xx-s.Rational(1,2))),'Smax_over_M_start_te_over100':float((4*xi/G).subs({xi:xx,z:10}))}
 examples.append(vals);ck('backreaction_precedes_Fzero_'+str(xx),float(back)>float(fraction),vals)
args.out.mkdir(parents=True,exist_ok=True);out={'checks':rows,'passed':sum(z['passed'] for z in rows),'total':len(rows),'mutation':args.mutation,'examples':examples,'scope':'exact scalar on prescribed C1 radiation-toEdS metric, not selfconsistent Einsteinmatter history; finite start positivity only'};(args.out/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'passed':out['passed'],'total':out['total'],'failed':[z['name'] for z in rows if not z['passed']],'examples':examples}));sys.exit(0 if out['passed']==out['total'] else 1)
