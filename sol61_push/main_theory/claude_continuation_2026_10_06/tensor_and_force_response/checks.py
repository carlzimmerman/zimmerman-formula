import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--mutation',choices=['freeze_F','omit_scalar_trace','import_UV_lowp']);ar=ap.parse_args();rows=[]
def ck(n,b,e=''):rows.append({'name':n,'passed':bool(b),'detail':str(e)})
def z(n,e):e=s.simplify(s.expand(e));ck(n,e==0,e)
t,M,xi,A,al=s.symbols('t M xi A al',positive=True);F=M-2*xi*A/t;H=2/(3*t)
z('F_definition',F-M*(1-2*xi*A/(M*t)))
# ADM TT sector: KijKij-K²=-6H²+tr(dotgamma²)/4, R3=-tr(gradgamma²)/(4a²).
vel,grad=s.symbols('vel grad');Ltt=F*s.Rational(1,2)*(vel/4-grad/4)
z('TT_action_coefficient',Ltt-F*(vel-grad)/8)
gd=s.symbols('gamma_dot');K=s.diag(H+gd/2,H-gd/2,H)
z('raw_extrinsic_TT_kinetic',s.trace(K*K)-s.trace(K)**2+6*H**2-gd**2/2)
r=s.symbols('r');gam=s.Function('gamma')(r);wx=s.exp(gam/2);wy=s.exp(-gam/2)
R3=-2*(s.diff(wx,r,2)/wx+s.diff(wy,r,2)/wy+s.diff(wx,r)*s.diff(wy,r)/(wx*wy))
z('raw_spatial_TT_gradient',R3+s.diff(gam,r)**2/2)

fr=2/t+s.diff(F,t)/F
if ar.mutation=='freeze_F':fr=2/t
z('TT_actual_friction',fr-(2/t+2*xi*A/(t*(M*t-2*xi*A))))
# Normalize a³=t² for homogeneous tensor equation.
y=s.log(1-al/t)/al
z('zero_k_TT_integral',s.diff(y,t)-1/(t*(t-al)))
z('zero_k_TT_Euler',s.diff(t*(t-al)*s.diff(y,t),t))
az=s.Function('a')(t);FF=s.Function('F')(t);zz=az*s.sqrt(FF)
z('tensor_WKB_amplitude_log_rate',s.diff(s.log(1/zz),t)+s.diff(az,t)/az+s.diff(FF,t)/(2*FF))
# Two-real field local static scalar-tensor constraints.
a1,a2=s.symbols('a1 a2');ff=M-xi*(a1*a1+a2*a2);SS=s.diff(ff,a1)**2+s.diff(ff,a2)**2
z('coupling_gradient_norm',SS-4*xi*(M-ff))
z('circular_gradient_norm',SS.subs(a2*a2,2*A/t-a1*a1)-8*xi**2*A/t)
S,rho,FP=s.symbols('S rho FP',positive=True);R,dF,Phi,Psi=s.symbols('R dF Phi Psi',real=True)
# R and dF stand for deltaR and laplacian(deltaF); signs T=-rho.
sol=s.solve([FP*R-rho-3*dF,dF+(0 if ar.mutation=='omit_scalar_trace' else S)*R/2],[R,dF])
z('full_scalar_trace_denominator',sol[R]-2*rho/(2*FP+3*S))
ph=(rho+sol[dF])/(2*FP);ps=ph-sol[dF]/FP
z('Poisson_Phi',ph-rho*(FP+S)/(FP*(2*FP+3*S)))
z('Poisson_Psi',ps-rho*(FP+2*S)/(FP*(2*FP+3*S)))
z('lensing_Poisson',ph+ps-rho/FP)
boost=(2*FP+4*S)/(2*FP+3*S)
z('force_boost_above_one',boost-1-S/(2*FP+3*S))
z('force_boost_below_four_thirds',s.Rational(4,3)-boost-2*FP/(3*(2*FP+3*S)))
d=s.symbols('d',positive=True)
z('relative_bare_force_exact',boost.subs({FP:M*(1-d),S:4*xi*M*d})/(1-d)-(2*(1-d)+16*xi*d)/((1-d)*(2*(1-d)+12*xi*d)))
z('slip_limits',s.limit((FP+S)/(FP+2*S),S,s.oo)-s.Rational(1,2))
# Exact fixed-EdS relative radial/phase scalar rows; metric equations not eliminated.
w=s.symbols('omega',positive=True);u=s.Function('u')(t);v=s.Function('v')(t);qrel=(u+s.I*v)
rel=s.diff(qrel,t,2)+(1+2*s.I*w)/t*s.diff(qrel,t)
real=s.diff(u,t,2)+s.diff(u,t)/t-2*w*s.diff(v,t)/t
imag=s.diff(v,t,2)+s.diff(v,t)/t+2*w*s.diff(u,t)/t
z('relative_radial_phase_rows',rel-real-s.I*imag)
nu,phi=s.Function('Psi')(t),s.Function('Phi')(t);dr=s.symbols('deltaR');mass2=4*xi/(3*t*t)
forcing=(-s.Rational(1,2)+s.I*w)/t*(s.diff(nu,t)+3*s.diff(phi,t))-2*mass2*nu-xi*dr
forcingR=-1/(2*t)*(s.diff(nu,t)+3*s.diff(phi,t))-2*mass2*nu-xi*dr
forcingI=w/t*(s.diff(nu,t)+3*s.diff(phi,t))
z('metric_driven_scalar_rows',forcing-forcingR-s.I*forcingI)
p,Om,ws=s.symbols('p Om ws',positive=True)
mat=s.Matrix([[p*p-ws*ws,2*s.I*Om*ws],[-2*s.I*Om*ws,p*p-ws*ws]])
z('frozen_radial_phase_determinant',mat.det()-((p*p-ws*ws)**2-4*Om**2*ws**2))
slow=p*p if ar.mutation=='import_UV_lowp' else (s.sqrt(p*p+Om*Om)-Om)**2
z('slow_lowp_frequency_squared',s.limit(slow/p**4,p,0)-1/(4*Om*Om))
# Exact finite-interval inequality supplied by alpha<ti.
ti,tf,ratio=s.symbols('ti tf ratio',positive=True)
z('late_fraction_from_early_margin',al/tf-(al/ti)*(ti/tf))
z('time_ratio_from_EdS_scale_factor', (s.Symbol('af',positive=True)/s.Symbol('ai',positive=True))**(-s.Rational(3,2))-(s.Symbol('ai',positive=True)/s.Symbol('af',positive=True))**s.Rational(3,2))
ck('illustrative_late_lensing_limit',1/(1-s.Rational(1,100))<s.Rational(1011,1000))
ck('illustrative_late_force_limit',s.Rational(4,3)/(1-s.Rational(1,100))<s.Rational(1347,1000))
res={'passed':all(r['passed'] for r in rows),'checks':rows,'scope':'Exact tensor/UV/static hierarchy and scalar rows; no coupled lowp force or full health','mutation':ar.mutation,'software':s.__version__};ar.out.mkdir(parents=True,exist_ok=True);(ar.out/'results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'passed':res['passed'],'total':len(rows),'failed':[r['name'] for r in rows if not r['passed']]}));sys.exit(0 if res['passed'] else 1)
