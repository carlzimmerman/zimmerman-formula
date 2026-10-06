import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',choices=['none','canonical_density','omit_geometry','dust_pressure'],default='none');args=ap.parse_args();rows=[]
def eq(name,x): x=s.factor(s.simplify(x));rows.append(dict(name=name,passed=x==0,residual=str(x)))
K,a,k,N,H=s.symbols('K a k N H',positive=True);h,eps,c,ss=s.symbols('h eps c ss',real=True)
Z,Zd,E,Ed,nu,bet=s.symbols('Z Zd E Ed nu bet',real=True);P=k*k/a**2;U=Z+E;T=3*Z+E;X=T-nu;Ax=Zd+Ed+P*bet
raw=0
for sign in [-1,1]:
 lx=h+sign*eps*Ax*c/2-eps**2*P*bet*U*ss**2/4
 ly=h+sign*eps*Zd*c/2-eps**2*P*bet*Z*ss**2/4
 kin=-K*a**3/N*s.exp(sign*eps*X*c/2)*(4*lx*ly+2*ly**2)
 space=K*N*a*s.exp(sign*eps*(nu+Z-E)*c/2)*(2*sign*eps*k*k*Z*c+eps**2*k*k*(U*Z-s.Rational(3,2)*Z**2)*ss**2)
 raw+=kin+space
# Exact geometric-mean vacuum independent of symmetric exponential relative variables.
raw+=K*N*a*eps**2*k*k*nu**2*ss**2
L2=s.expand(s.diff(raw,eps,2).subs(eps,0)/2).subs({c**2:s.Rational(1,2),ss**2:s.Rational(1,2)})
C=Ax*Zd+Zd**2/2+h*X*(Ax+2*Zd)+s.Rational(3,4)*h*h*X*X-h*P*bet*T
Q=(Z+nu)**2/2
formula=-K*a**3*C/N+K*N*a*k*k*Q
eq('raw_unreduced_plane_ADM_expansion',L2-formula)
eq('raw_shift_is_parent_f',s.diff(C,bet)-P*(Zd-h*nu))
# common lapse varied before relative elimination; move L2 to background Einstein RHS.
rho=-s.diff(formula,N).subs(N,1)/a**3
Ch=s.diff(C,h);Zd2,Ed2,nud,bd=s.symbols('Zdd Edd nud bd',real=True)
Chdot=s.diff(Ch,a)*H*a+s.diff(Ch,Z)*Zd+s.diff(Ch,E)*Ed+s.diff(Ch,nu)*nud+s.diff(Ch,Zd)*Zd2+s.diff(Ch,Ed)*Ed2+s.diff(Ch,bet)*bd
press=(a*s.diff(formula,a)+(K*a**3/N)*(3*H*Ch+Chdot)).subs(N,1)/(3*a**3)
Z0=s.symbols('Z0',real=True)
on={h:H,Z:Z0-nu,Zd:H*nu,Zd2:-H*H*nu,E:-3*Z0+2*nu,Ed:-2*H*nu,Ed2:2*H*H*nu,nud:-H*nu,bet:2*H*nu/P-Z0/H,bd:2*H*H*nu/P}
rhof=s.simplify(rho.subs(on));pf=s.simplify(press.subs(on))
expected=-K*(H*H*nu*nu+P*Z0*Z0)/2
candidate=rhof
if args.control=='canonical_density':candidate=K*P*nu*nu/2
if args.control=='omit_geometry':candidate=-K*P*nu*nu/2
eq('common_lapse_source_not_reduced_H',candidate-expected)
eq('common_scale_pressure_raw_variation',pf+expected/3)
pressure_candidate=0 if args.control=='dust_pressure' else pf
eq('actual_mean_pressure_retained',pressure_candidate+expected/3)
eq('actual_mean_energy_conservation',H*a*s.diff(rhof,a)-H*nu*s.diff(rhof,nu)+3*H*(rhof+pressure_candidate))
# Interacting stress alone, with each lapse and spatial operator varied, not canonical energy.
ax,ay,az=s.symbols('ax ay az',positive=True)
LI=K*N*ay*az*k*k*nu*nu/(2*ax)
rI=-s.diff(LI,N)/(ax*ay*az)
pI=[u*s.diff(LI,u)/(N*ax*ay*az) for u in [ax,ay,az]]
eq('summed_interaction_density',rI.subs(ax,a)+K*P*nu*nu/2)
eq('summed_parallel_pressure',pI[0]-rI)
eq('summed_transverse_pressure_y',pI[1]+rI)
eq('summed_transverse_pressure_z',pI[2]+rI)
eq('interaction_trace_pressure',sum(pI)/3+rI/3)
rIi=rI.subs(ax,a);pIi=(sum(pI)/3).subs(ax,a)
resI=H*a*s.diff(rIi,a)-H*nu*s.diff(rIi,nu)+3*H*(rIi+pIi)
eq('interaction_not_separately_conserved',resI+2*H*rIi)
# Actual firstorder mode and powers; toruscos normalization explicit.
t,Z1=s.symbols('t Z1',real=True);at=s.exp(H*t);mode={a:at,nu:-Z1/at}
eq('full_mean_source_a_minus2',s.diff(at**2*rhof.subs(mode),t))
eq('interaction_source_a_minus4',s.diff(at**4*rIi.subs(mode),t))
eq('full_pressure_curvature_like',pf+rhof/3)
eq('physical_decay_mode_W',s.diff(-Z1/(2*at),t)+H*(-Z1/(2*at)))
eq('frozen_mode_effective_split_nonzero',rhof.subs(nu,0)+K*P*Z0**2/2)
# Relative-order2 EH kinetic becomes time boundary, agrees inherited firstorder reduction.
boundary=-K*H*a**3*(3*H*nu**2+2*nu*nud)/2
fDon={h:H,Zd:H*nu,E:-3*Z-nu,Ed:-3*H*nu-nud,bet:(3*H*nu+nud)/P-(Z+nu)/H}
eq('kinetic_boundary_after_parent_constraints',(-K*a**3*C).subs(fDon)-boundary)
# Physical proper volumes differ from coordinate background even with D0.
eq('each_proper_volume_correction',s.diff(s.exp(-eps*nu*c/2),eps,2).subs(eps,0).subs(c**2,s.Rational(1,2))/2-nu**2/16)
x=s.symbols('x',real=True);eq('periodic_firstorder_source_mean_zero',s.integrate(s.cos(x),(x,0,2*s.pi)))
result=dict(passed=sum(r['passed'] for r in rows),total=len(rows),checks=rows,control=args.control,scope='n3 common-clock exponential mean plane chart; relativeorder2 toruscos; raw common lapse/scale variations before elimination')
p=Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(result,indent=2));print(json.dumps({'passed':result['passed'],'total':result['total'],'failed':[r for r in rows if not r['passed']]}));sys.exit(result['passed']!=result['total'])
