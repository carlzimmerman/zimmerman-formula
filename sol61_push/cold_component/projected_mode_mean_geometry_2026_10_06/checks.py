import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',choices=['none','coordinate_as_normal','omit_mean_response','dust_mean'],default='none');args=ap.parse_args();rows=[]
def eq(n,x):x=s.factor(s.simplify(x));rows.append(dict(name=n,passed=x==0,residual=str(x)))
K,a,k,N,H=s.symbols('K a k N H',positive=True);hx,hy,eps,c,ss=s.symbols('hx hy eps c ss',real=True);Z,Zd,E,Ed,nu,bet=s.symbols('Z Zd E Ed nu bet',real=True);P=k*k/a**2;U=Z+E;T=3*Z+E;X=T-nu;Ax=Zd+Ed+P*bet
raw=0
for sign in [-1,1]:
 lx=hx+sign*eps*Ax*c/2-eps**2*P*bet*U*ss**2/4
 ly=hy+sign*eps*Zd*c/2-eps**2*P*bet*Z*ss**2/4
 raw+=-K*a**3/N*s.exp(sign*eps*X*c/2)*(4*lx*ly+2*ly**2)
 raw+=K*N*a*s.exp(sign*eps*(nu+Z-E)*c/2)*(2*sign*eps*k*k*Z*c+eps**2*k*k*(U*Z-s.Rational(3,2)*Z*Z)*ss**2)
raw+=K*N*a*eps**2*k*k*nu*nu*ss**2
L2=s.expand(s.diff(raw,eps,2).subs(eps,0)/2).subs({c*c:s.Rational(1,2),ss*ss:s.Rational(1,2)})
C=Ax*Zd+Zd*Zd/2+X*(hy*Ax+(hx+hy)*Zd)+X*X*(hx*hy/2+hy*hy/4)-P*bet*(hy*U+(hx+hy)*Z)
Q=(Z+nu)**2/2
eq('raw_anisotropic_ADM_expansion',L2+K*a**3*C/N-K*N*a*k*k*Q)
ax,ay=s.symbols('ax ay',positive=True);Ca=C.subs(a,ax);L=-K*ax*ay**2*Ca/N+K*N*ay**2/ax*k*k*Q;vol=ax*ay**2
Zd2,Ed2,nud,bd=s.symbols('Zdd Edd nud bd')
def dt(f):return s.diff(f,ax)*H*ax+s.diff(f,ay)*H*ay+s.diff(f,Z)*Zd+s.diff(f,E)*Ed+s.diff(f,nu)*nud+s.diff(f,Zd)*Zd2+s.diff(f,Ed)*Ed2+s.diff(f,bet)*bd
rho=-s.diff(L,N)/vol
px=(ax*s.diff(L,ax)-dt(s.diff(L,hx)))/vol
py=(ay*s.diff(L,ay)-dt(s.diff(L,hy)))/(2*vol)
on={ax:a,ay:a,N:1,hx:H,hy:H,Z:-nu,Zd:H*nu,E:2*nu,Ed:-2*H*nu,Zd2:-H*H*nu,Ed2:2*H*H*nu,nud:-H*nu,bet:2*H*nu/P,bd:2*H*H*nu/P}
r=s.simplify(rho.subs(on));xx=s.simplify(px.subs(on));yy=s.simplify(py.subs(on))
eq('raw_lapse_density',r+K*H*H*nu*nu/2)
eq('raw_parallel_pressure',xx-s.Rational(3,2)*K*H*H*nu*nu)
eq('raw_transverse_pressure',yy+K*H*H*nu*nu/2)
eq('mean_trace_conservation',-H*nu*s.diff(r,nu)+H*(3*r+xx+2*yy))
# Full commonEH coefficient4K; solve zero-mode Friedmann/shear rows.
t,amp,Ai,Si,J=s.symbols('t amp Ai Si J',real=True);at=s.exp(H*t);nmode=-amp/at
A=Ai+amp*amp*(at**-2-1)/96
S=Si+amp*amp*(s.Rational(1,12)-at**-2/4+at**-3/6)+J*(1-at**-3)/(3*H)
Ad=s.diff(A,t);Sd=s.diff(S,t)
eq('mean_Friedmann_constraint',24*K*H*Ad-r.subs(nu,nmode))
eq('mean_anisotropic_spatial_row',4*K*(s.diff(S,t,2)+3*H*Sd)-(xx-yy).subs(nu,nmode))
eq('mean_trace_spatial_row',-8*K*s.diff(A,t,2)-24*K*H*Ad-((xx+2*yy)/3).subs(nu,nmode))
eq('specified_initial_chart_scale',A.subs(t,0)-Ai)
eq('specified_initial_chart_shear',S.subs(t,0)-Si)
eq('specified_initial_chart_shear_rate',Sd.subs(t,0)-J)
# Geometric normal expansion before coordinate/proper time conflation.
num=s.exp(eps*X*c/2)*(3*H+eps*(Ax+2*Zd)*c/2-eps**2*P*bet*T*ss**2/4)
den=s.exp(eps*T*c/2)
num2=s.expand(s.diff(num,eps,2).subs(eps,0)/2).subs({c*c:s.Rational(1,2),ss*ss:s.Rational(1,2)}).subs(on)
den2=s.expand(s.diff(den,eps,2).subs(eps,0)/2).subs(c*c,s.Rational(1,2)).subs(on)
normalH2=s.simplify((num2-3*H*den2)/3)
eq('normal_volume_weighted_expansion_correction',normalH2-H*nu*nu/48)
eq('proper_spatial_volume_correction',den2-nu*nu/16)
normal_answer=Ad+normalH2.subs(nu,nmode)
coordinate_answer=Ad+s.diff(nmode*nmode/48,t)
candidate=coordinate_answer if args.control=='coordinate_as_normal' else normal_answer
if args.control=='omit_mean_response':candidate=normalH2.subs(nu,nmode)
eq('actual_normal_mean_expansion_unchanged',candidate)
eq('coordinate_propervolume_rate_distinct',coordinate_answer+H*nmode*nmode/16)
# Normal shear: raw kx-ky, volume weighted. Linear differencezero fordecayingmode.
shnum=s.exp(eps*X*c/2)*(eps*(Ax-Zd)*c/2-eps**2*P*bet*(U-Z)*ss**2/4)
sh2=s.expand(s.diff(shnum,eps,2).subs(eps,0)/2).subs({c*c:s.Rational(1,2),ss*ss:s.Rational(1,2)}).subs(on)
eq('normal_mean_shear_correction',sh2+H*nu*nu/2)
normalS=Sd+sh2.subs(nu,nmode)
eq('normal_shear_decays_a_minus3',s.diff(at**3*normalS,t))
eq('zero_initial_normal_shear_remains_zero',normalS.subs(J,H*amp*amp/2))
# A dust claim has a nonzero normalexpansion excess absenthere.
if args.control=='dust_mean':eq('false_positive_dust_from_mode',normal_answer-H*amp*amp/(48*at**3))
# Half-period parity of relativefirst fields and integrated local nonlineargradient forcing.
x=s.symbols('x',real=True);eq('relative_first_halfperiod_swap',s.cos(x+s.pi)+s.cos(x))
eq('quadratic_common_momentum_average_zero',s.integrate(s.sin(x)*s.cos(x),(x,0,2*s.pi)))
# Lowest nonanalytic relative EL is divergence of |sin|sin; torusintegralboundary0.
eq('cubic_gradient_relative_zero_mode',s.Abs(s.sin(2*s.pi))*s.sin(2*s.pi)-s.Abs(s.sin(0))*s.sin(0))
out={'passed':sum(x['passed'] for x in rows),'total':len(rows),'checks':rows,'control':args.control,'scope':'formal commonhomogeneousorder2 plane BianchiI response and geometricnormalaverages, notfull localclockcompletion'}
p=Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2));print(json.dumps({'passed':out['passed'],'total':out['total'],'failed':[x for x in rows if not x['passed']]}));sys.exit(out['passed']!=out['total'])
