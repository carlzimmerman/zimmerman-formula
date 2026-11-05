#!/usr/bin/env python3
"""Exact checks of the stated ADM and static-energy reductions, not full health."""
import argparse, hashlib, json, platform
from pathlib import Path
import sympy as S

ap=argparse.ArgumentParser()
ap.add_argument('--mode',choices=['main','clock_sign','drop_gradient'],default='main')
ap.add_argument('--out',required=True)
args=ap.parse_args()
checks=[]
def check(name, value):
    checks.append({'name':name,'passed':bool(value)})
def z(x):
    return S.simplify(S.expand(x))==0

M,H,k,mu,R=S.symbols('M H k mu R',positive=True)
v,V1,V2=S.symbols('v V1 V2',real=True)
alpha,shift,q,qd,sd,P,e=S.symbols('alpha shift q qdot sigmadot P e',real=True)
# Flat spatial gauge. The scalar shift shear-square minus trace-square
# integrates to zero for a Fourier mode; k is physical wave number here.
N=1+e*alpha
ADM=M**2/(2*N)*(-6*H**2-4*e*H*k**2*shift)
ADM+=(v+e*qd-e**2*k**2*shift*q)**2/(2*N)
ADM-=N*(S.Symbol('V0')+e*V1*q+e**2*(V2+k**2)*q**2/2)
L2=S.expand(S.series(ADM,e,0,3).removeO()).coeff(e,2)
expected=(qd**2/2-v*alpha*qd+(v**2/2-3*M**2*H**2)*alpha**2
          -V1*alpha*q-(V2+k**2)*q**2/2
          +k**2*shift*(2*M**2*H*alpha-v*q))
check('ADM_quadratic_from_expansion',z(L2-expected))
# K=4piG=1/(2M^2). At P=0 the potential is P^2/(4M^2).
LP=k*P*(alpha-sd)-P**2/(4*M**2)
Psol=S.solve(S.diff(LP,P),P)[0]
induced=S.factor(LP.subs(P,Psol))
check('polarization_elimination',z(induced-M**2*k**2*(alpha-sd)**2))
sign=-1 if args.mode=='clock_sign' else 1
extra=sign*induced+M**2*mu**2*(alpha-sd)**2
full=L2+extra
b=v/(2*M**2*H)
asol=S.solve(S.diff(full,shift),alpha)[0]
check('shift_constraint_unchanged',z(asol-b*q))
ssol=S.solve(S.diff(full,alpha),shift)[0]
check('lapse_solves_shift_not_clock_charge',z(S.diff(full,alpha).subs(shift,ssol)))
check('constraint_jacobian_nonsingular',z(S.det(S.hessian(full,[alpha,shift]))+4*M**4*H**2*k**4))
reduced=S.expand(full.subs(alpha,asol))
g=v*b
vd=-3*H*v-V1
Hd=-v**2/(2*M**2)
gdot=S.diff(g,v)*vd+S.diff(g,H)*Hd
# Remove -g q qdot by integration by parts with measure R^3.
mass=S.factor(V2-2*((v**2/2-3*M**2*H**2)*b**2-V1*b)-gdot-3*H*g)
f=v**2/(M**2*H)
fdot=S.diff(f,v)*vd+S.diff(f,H)*Hd
mQ=V2-fdot-3*H*f
check('canonical_scalar_mass_identity',z(mass-mQ))
C=2*M**2*(sign*k**2+mu**2)
Lclean=qd**2/2-(k**2+mQ)*q**2/2+C*(sd-b*q)**2/2
check('reduced_action_after_time_boundary',z(reduced+g*q*qd+(gdot+3*H*g)*q**2/2-Lclean))
K=S.hessian(Lclean,[qd,sd])
check('positive_clock_kinetic_coefficient',z(K[1,1]-2*M**2*(k**2+mu**2)))
check('nonzero_k_clock_rank',z(K.det().subs(mu,0)-2*M**2*k**2))
check('zero_coupling_canonical_limit',z((Lclean-C*(sd-b*q)**2/2)-(qd**2/2-(k**2+mQ)*q**2/2)))
j,pq=S.symbols('j p_q',real=True)
speed=b*q+j/(R**3*C)
routh=S.factor((R**3*Lclean-j*sd).subs(sd,speed))
routh_target=R**3*(qd**2/2-(k**2+mQ)*q**2/2)-b*j*q-j**2/(2*R**3*C)
check('fixed_charge_Routhian',z(routh-routh_target))
check('clock_charge_not_a_constraint',z(S.diff(R**3*Lclean,sd).subs(sd,speed)-j))
Ham=S.factor((pq*qd+j*sd-R**3*Lclean).subs({qd:pq/R**3,sd:speed}))
Hamtarget=pq**2/(2*R**3)+R**3*(k**2+mQ)*q**2/2+b*j*q+j**2/(2*R**3*C)
check('Legendre_transform',z(Ham-Hamtarget))
check('charge_source_scalar_equation',z(S.diff(routh,q)+R**3*(k**2+mQ)*q+b*j))
check('arbitrary_charge_known_answer',z((R**3*C*(sd-b*q)).subs({M:1,H:1,k:1,mu:0,v:0,R:1,q:0,sd:S.Rational(1,2)})-1))

# Exact scalar-only exponential potential: lambda^2=2 epsilon.
lam=S.symbols('lambda',positive=True)
exp_sub={v:lam*M*H,V1:-lam*M*(3-lam**2/2)*H**2,
         V2:lam**2*(3-lam**2/2)*H**2}
check('exponential_scalar_mass_cancellation',z(mQ.subs(exp_sub,simultaneous=True)))
check('exponential_clock_scalar_coupling_constant',z(b.subs(v,lam*M*H)-lam/(2*M)))
check('exponential_frozen_energy_schur',z((k**2-C*b**2).subs({v:lam*M*H,mu:0})-k**2*(1-lam**2/2)))
# Conformal equation q''+2 R'/R q'+kcom^2 q=-b j/R.
eta=S.symbols('eta',positive=True)
a=S.Function('a')(eta);u=S.Function('u')(eta);kc,bc=S.symbols('kc b_const',real=True)
qq=u/a
conf=a*(S.diff(qq,eta,2)+2*S.diff(a,eta)/a*S.diff(qq,eta)+kc**2*qq+bc*j/a)
check('conformal_forced_mode_equation',z(conf-(S.diff(u,eta,2)+(kc**2-S.diff(a,eta,2)/a)*u+bc*j)))
t,power=S.symbols('t power',positive=True)
# Leading super-Hubble equation: omitted kphys^2 term is asymptotically
# subleading for fixed comoving k and power>1, not an exact finite-k solution.
qforced=-bc*j*t**(2-3*power)/(2-3*power)
check('leading_charge_response',z(S.diff(qforced,t,2)+3*power/t*S.diff(qforced,t)+bc*j*t**(-3*power)))
check('leading_decaying_homogeneous_mode',z(S.diff(t**(1-3*power),t,2)+3*power/t*S.diff(t**(1-3*power),t)))

# Static Newtonian reduction, K=1, V=Cpot*a(phi)^2.
a0,pp,s,Cpot,a1,a2,a3=S.symbols('a p s Cpot a1 a2 a3',positive=True)
W=a0*(-pp-a0*S.log(1-pp/a0))
U=Cpot*a0**2+W-pp**2/2
sub={pp:a0*s/(1+s)}
h=s+s/(1+s)-2*S.log(1+s)
Upp=S.simplify(S.diff(U,pp,2).subs(sub))
Upa=S.simplify(S.diff(U,pp,a0).subs(sub))
Uaa=S.simplify(S.diff(U,a0,2).subs(sub))
Ua=S.simplify(S.diff(U,a0).subs(sub))
J=2*S.log(1+s)-4*s/(s+2)
check('static_polarization_curvature',z(Upp-s*(s+2)))
check('static_mixed_curvature',z(Upa+s**2))
check('static_scalar_force',z(Ua-a0*(2*Cpot-h)))
check('static_Schur_complement',z(Uaa-Upa**2/Upp-(2*Cpot+J)))
check('static_Schur_uniform_sign_derivative',z(S.diff(J,s)-2*s**2/((1+s)*(s+2)**2)))
check('static_Schur_zero_endpoint',J.subs(s,0)==0)
check('stationary_equation_monotone',z(S.diff(h,s)-s**2/(1+s)**2))
check('stationary_equation_unbounded',S.limit(h,s,S.oo)==S.oo)
Mstatic=a1**2*(2*Cpot+J)+a2*a0*(2*Cpot-h)
check('off_shell_force_remainder',z(a1**2*(Uaa-Upa**2/Upp)+a2*Ua-Mstatic))
check('on_shell_constant_background_positive',z(Mstatic.subs(Cpot,h/2)-a1**2*(h+J)))
check('original_large_s_recovered',z(S.limit(Mstatic/s,s,S.oo)+a0*a2))
# Positive-function factorization: f=-a_phi, q=f eta. Work with independent
# jets to check the total derivative in any one spatial direction.
phix,phixx,qx=S.symbols('phi_x phi_xx q_x',real=True)
ratio=a2/a1
left=qx**2+ratio*phixx*q**2
rem=0 if args.mode=='drop_gradient' else a3/a1*phix**2*q**2
right=(qx-ratio*phix*q)**2-rem
boundary=2*q*qx*ratio*phix+q**2*((a3/a1-ratio**2)*phix**2+ratio*phixx)
check('on_shell_gradient_factorization',z(left-right-boundary))
# A hand-evaluable witness catches omission of the gradient remainder.
check('factorization_nonzero_gradient_witness',z((left-right-boundary).subs({a1:1,a2:2,a3:3,phix:1,phixx:0,q:1,qx:0})))
y,n,B=S.symbols('y n B',positive=True)
af=S.sinh(y)**(-n)
ratio3=S.diff(af,y,3)/(B**2*S.diff(af,y))
want3=(n**2*S.coth(y)**2+(3*n+2)/S.sinh(y)**2)/B**2
check('sinh_third_derivative_ratio',S.simplify(S.trigsimp(ratio3-want3))==0)
# Exact composition checks for the canonical field change, without a scan.
x=S.symbols('x',real=True)
aa=S.Function('aa');ph=S.Function('ph')(x)
check('positive_function_chain_rule',z(S.diff(aa(ph),x,2)-S.diff(aa(ph),ph,2)*S.diff(ph,x)**2-S.diff(aa(ph),ph)*S.diff(ph,x,2)))

here=Path(__file__).resolve().parent
sources=[here/'verify.py',here/'CONTRACT.md']
result=dict(mode=args.mode,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
    formulas=dict(C=str(C),b=str(b),mQ2=str(S.factor(mQ)),static_Schur=str(J+2*Cpot),
                  static_mass=str(Mstatic),sinh_gradient_penalty=str(want3)),
    source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
    software={'python':platform.python_version(),'sympy':S.__version__},
    scope='Exact restricted ADM/static identities. No charged full-GR constraint theorem, nonlinear regularity, empirical pass or kappa derivation.')
out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(mode=args.mode,passed=result['passed'],total=result['total'],failed=[c['name'] for c in checks if not c['passed']]),indent=2))
raise SystemExit(int(result['passed']!=result['total']))
