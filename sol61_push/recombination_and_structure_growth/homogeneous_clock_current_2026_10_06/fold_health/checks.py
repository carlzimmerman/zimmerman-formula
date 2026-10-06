"""Exact constrained kinetic checks, including canonical dust; no mode evolution claim."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--omit-matter-mixing',action='store_true');ap.add_argument('--vacuum-transplant',action='store_true');ap.add_argument('--response-sign',action='store_true');args=ap.parse_args()
checks=[]
def ck(name,expr): checks.append({'name':name,'passed':bool(expr)})
def zero(expr):return s.simplify(expr)==0
M,c,H,Hs,q,X=s.symbols('M c H Hs q X',positive=True);eta,h,kappa,p=s.symbols('eta h kappa p',positive=True)
K=-c*s.log(X);G=-s.sqrt(2)*c/(3*Hs*s.sqrt(X));GX=s.diff(G,X)
Theta=M*H-q*X*GX
Sigma=X*s.diff(K,X)+2*X**2*s.diff(K,X,2)+12*H*q*X*GX+6*H*q*X**2*s.diff(G,X,2)-3*M*H**2
subs={X:q*q/2,H:h*Hs,c:3*M*Hs**2*eta}
Th=s.simplify(Theta.subs(subs,simultaneous=True));Sig=s.simplify(Sigma.subs(subs,simultaneous=True))
ck('Theta_actual_H',zero(Th-M*Hs*(h-eta)))
ck('Sigma_actual_H',zero(Sig-3*M*Hs**2*(eta*(1+h)-h*h)))
GS=s.simplify(3*M+Sig*M*M/Th**2)
ck('GS_actual_H',zero(GS-3*M*eta*(1+eta-h)/(h-eta)**2))
D=s.diff(K,X)+2*X*s.diff(K,X,2)+6*H*q*(GX+X*s.diff(GX,X))+6*X**2*GX**2/M
ck('debraided_D',zero(D.subs(subs,simultaneous=True)-3*M*Hs**2*eta*(1-h+eta)/(q*q/2)))
# Raw matter-free ADM derivative block and matter P(Y) derivative block.
zd,vd,nu,t,v=s.symbols('zd vd nu t v',real=True);R,C=s.symbols('R C',positive=True);theta,sigma=s.symbols('theta sigma',nonzero=True,real=True)
raw=-3*M*zd**2+sigma*nu**2+6*theta*nu*zd-2*theta*nu*t+2*M*zd*t+C*(vd-nu)**2+R*v*t+kappa*M*p*p*nu**2
nu_sol=(M*zd+R*v/2)/theta
ck('shift_with_matter',zero(s.diff(raw,t).subs(nu,nu_sol)))
red=s.expand(raw.subs(nu,nu_sol));vel=s.Matrix([zd,vd]);KM=s.hessian(red,vel)/2
A=3*M+sigma*M*M/theta**2+kappa*M**3*p*p/theta**2;d=M/theta
expected=s.Matrix([[A+C*d*d,-C*d],[-C*d,C]])
ck('reduced_full_velocity_matrix',s.simplify(KM-expected)==s.zeros(2))
used=KM.copy()
if args.omit_matter_mixing:used[0,1]=used[1,0]=0
ck('matter_Schur_is_clock_coefficient',zero(used.det()-C*A))
ck('positive_matter_square_null_direction',zero((s.Matrix([1,d]).T*KM*s.Matrix([1,d]))[0]-A))
# Direct coordinate-density Sorkin expansion (one longitudinal spatial component).
# J0=Jb(1+delta), ell=-m(t+v); auxiliary j=Ji/J0, shift beta.
j,beta,grad,N=s.symbols('j beta grad N',real=True);Jb,m=s.symbols('Jb m',positive=True)
aux=m*Jb*((j+beta)**2/(2*N)+j*grad)
j_sol=-beta-N*grad
ck('Sorkin_spatial_current_EL',zero(s.diff(aux,j).subs(j,j_sol)))
ck('Sorkin_spatial_reduction',zero(aux.subs(j,j_sol)+m*Jb*(N*grad**2/2+beta*grad)))
pi,wd,ddot,w,ps,lam=s.symbols('pi wd ddot w ps lam',real=True)
dust_raw=-3*M*zd**2+sigma*nu**2+6*theta*nu*zd-2*theta*nu*t+2*M*zd*t+kappa*M*p*p*nu**2+pi*(vd-nu)-R*p*p*v*v/2+R*v*t
ck('dust_exact_shift',zero(s.diff(dust_raw,t).subs(nu,nu_sol)))
dust_red=s.expand(dust_raw.subs(nu,nu_sol).subs({v:w+d*s.symbols('zeta'),vd:wd+d*zd+ddot*s.symbols('zeta')}))
ck('dust_canonical_pi_wdot',zero(s.diff(dust_red,pi,wd)-1))
ck('dust_no_pi_zdot',zero(s.diff(dust_red,pi,zd)))
ck('dust_clock_velocity_hessian',zero(s.diff(dust_red,zd,2)/2-A))
Pz=s.diff(dust_red,zd);zd_sol=s.solve(Pz-ps,zd)[0]
Ham=s.expand((ps*zd+pi*wd-dust_red).subs(zd,zd_sol))
ck('dust_physical_momentum_curvature',zero(s.diff(Ham,ps,2)-1/(2*A)))
# Recover dust-dependent tadpoles from the exact time-dependent unitary action.
eps,zeta,Hdot,Vpot,b,qdlog=s.symbols('eps zeta Hdot Vpot b qdlog',real=True)
Nloc=1+eps*nu
hom=s.exp(3*eps*zeta)*(-3*M*(H+eps*zd)**2/Nloc+Nloc*(2*c*s.log(Nloc)-Vpot)-3*b*(H+eps*zd)*s.log(Nloc)-b*qdlog)
quad=s.expand(s.series(hom,eps,0,3).removeO()).coeff(eps,2)
ck('full_ADM_zeta_nu_tadpole',zero(s.diff(quad,zeta,nu)-3*(3*M*H**2+2*c-Vpot-3*b*H)))
ck('full_ADM_zeta_mass_on_shell',zero((quad.coeff(zeta,2)+9*M*(Hdot+3*H**2)).subs(Vpot,3*M*H**2+2*M*Hdot-b*qdlog)))
ck('full_ADM_Sigma_before_substitution',zero(quad.coeff(nu,2)-(c+3*b*H/2-3*M*H**2)))
# Physical density convention: pi=rho(delta+3*zeta); one temporal IBP
# converts 3rho*zeta*vdot to -3rho*zd*v because a^3rho is constant.
delta,deltadot=s.symbols('delta deltadot',real=True)
coordinate=3*R*zeta*nu+R*(delta+3*zeta)*(vd-nu)
physical=-R*v*deltadot-3*R*zd*v-R*delta*nu
ck('coordinate_vs_physical_dust_IBP',zero(coordinate-physical-R*(delta*vd+v*deltadot)-3*R*(zeta*vd+zd*v)))
# Eliminating the canonical dust coordinate changes the apparent kinetic matrix.
B,Lz=s.symbols('B Lz',nonzero=True,real=True);pid=s.symbols('pid',real=True)
eliminated=A*zd**2-(Lz*zd-pid)**2/(4*B)
Kd=s.hessian(eliminated,[zd,pid])/2
ck('density_coordinate_kinetic_determinant',zero(Kd.det()+A/(4*B)))

# Complete finite-time dust mode variational derivatives, before choosing a history.
full=-3*M*zd**2+(sigma+kappa*M*p*p)*nu**2+6*theta*nu*zd+M*p*p*zeta**2+2*M*p*p*nu*zeta+3*R*zeta*nu+pi*(vd-nu)-R*p*p*v*v/2
fullred=full.subs(nu,nu_sol);Rnu=(2*(sigma+kappa*M*p*p)*nu+6*theta*zd+(2*M*p*p+3*R)*zeta-pi).subs(nu,nu_sol)
ck('full_mode_zeta_canonical_momentum',zero(s.diff(fullred,zd)-(-6*M*zd+6*theta*nu_sol+d*Rnu)))
ck('full_mode_pi_equation',zero(s.diff(fullred,pi)-(vd-nu_sol)))
ck('full_mode_velocity_coordinate_equation',zero(s.diff(fullred,v)-(R*Rnu/(2*theta)-R*p*p*v)))
ck('full_mode_zeta_force',zero(s.diff(fullred,zeta)-(2*M*p*p*zeta+(2*M*p*p+3*R)*nu_sol)))

Scoef=sigma+kappa*M*p*p; e=R/(2*theta)
Bexpr=Scoef*e**2-R*p*p/2; Lzexpr=2*e*(Scoef*d+3*theta)
ck('density_velocity_mixing_proportional_clock',zero(Lzexpr-R*A/M))
ck('density_elimination_regular_at_clock_zero',zero(Bexpr.subs(sigma,-3*theta**2/M-kappa*M*p*p)-(-3*R**2/(4*M)-R*p*p/2)))

# Actual branch and finite-wave-number comparisons.
response=-kappa if args.response_sign else kappa
usedGS=3*M*eta**2/(1-eta)**2 if args.vacuum_transplant else GS
Ac=s.simplify(usedGS+response*M*p*p/(Hs*Hs*(h-eta)**2))
correct= M*(3*eta*(1+eta-h)+kappa*p*p/(Hs*Hs))/(h-eta)**2
ck('clock_actual_background_coefficient',zero(Ac-correct))
ck('fold_finite_k_repair',zero(correct.subs(h,1+eta)-kappa*M*p*p/Hs**2))
crit=3*eta*Hs**2*(h-1-eta)/kappa
ck('kinetic_zero_boundary',zero(correct.subs(p*p,crit)))
ratio=3*eta*(h-1-eta)/(kappa*h*h)
ck('max_negative_band_ratio_stationary',zero(s.diff(ratio,h).subs(h,2*(1+eta))))
ck('max_negative_band_ratio',zero(ratio.subs(h,2*(1+eta))-3*eta/(4*kappa*(1+eta))))
rows=[]
for hh,pp in [(10,s.Rational(3,10)),(10,10),(s.Rational(3,2),s.Rational(3,10)),(s.Rational(11,10),s.Rational(3,10))]:
 val=s.simplify(correct.subs({M:1,Hs:1,eta:s.Rational(1,2),kappa:1,h:hh,p:pp}))
 rows.append({'h':str(hh),'p_over_Hstar':str(pp),'clock_kinetic_over_M_exact':str(val),'sign':s.sign(val).__str__()})
ck('early_long_mode_negative',s.Rational(rows[0]['clock_kinetic_over_M_exact'])<0)
ck('early_short_mode_positive',s.Rational(rows[1]['clock_kinetic_over_M_exact'])>0)
ck('fold_nonzero_k_positive',s.Rational(rows[2]['clock_kinetic_over_M_exact'])>0)
ck('late_clock_positive',s.Rational(rows[3]['clock_kinetic_over_M_exact'])>0)
out={'checks':checks,'summary':{'passed':sum(x['passed'] for x in checks),'total':len(checks)},'bounded_points':rows,'scope':'Exact quadratic velocity Hessian and dust canonical momentum curvature; no growth rates, quantum decay, gradient stability, nonlinear strong-coupling scale or radiation history.'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['summary']));raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
