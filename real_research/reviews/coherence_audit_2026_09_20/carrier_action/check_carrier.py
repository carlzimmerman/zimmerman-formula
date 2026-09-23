"""Action-specific exact identities and bounded reproducible counterexamples.

No source imports or writes. SymPy proves the displayed algebra only; the report
supplies variational derivations and distinguishes these from the coupled model.
"""
from pathlib import Path
import json
import math
import sys
import sympy as sp

out = Path(sys.argv[1])
checks = {}
def equal(name, lhs, rhs=0):
    residual = sp.factor(sp.simplify(lhs-rhs))
    checks[name] = str(residual)
    assert residual == 0, (name, residual)

X, X0, p1, g = sp.symbols('X X0 p1 g', positive=True)
D = X-X0
p = p1*D+g*D**2/2
rho = 2*X*sp.diff(p,X)-p
equal('quadratic_density', rho, 2*X0*p1+(p1+2*X0*g)*D+sp.Rational(3,2)*g*D**2)
equal('quadratic_pressure_background', p.subs(X,X0))
equal('quadratic_density_background', rho.subs(X,X0), 2*X0*p1)
equal('quadratic_cs_background', (sp.diff(p,X)/sp.diff(rho,X)).subs(X,X0),p1/(p1+2*X0*g))
equal('quadratic_affine_eos_residual',p-p1/(p1+2*X0*g)*(rho-2*X0*p1),g*(X-X0)**2*(X0*g-p1)/(2*X0*g+p1))

# G1/G2 are symbols in the actual builder, so inserting time dependence after
# Euler-Lagrange variation necessarily omits these coefficient derivatives.
t=sp.symbols('t', real=True)
a=sp.Function('a')(t)
chi=sp.Function('chi')(t)
psi=sp.Function('psi')(t)
Phi=sp.Function('Phi')(t)
Cp, A, p10=sp.symbols('C A p10',positive=True)
pp=sp.Function('p1')(t)
gg=sp.Function('g')(t)
K=pp+2*Cp**2*gg
L2=a**3*(K*(sp.diff(chi,t)-Cp*psi)**2-6*Cp*pp*Phi*(sp.diff(chi,t)-Cp*psi))
EL=-sp.diff(sp.diff(L2,sp.diff(chi,t)),t)
EL_frozen=EL.subs({sp.diff(pp,t):0,sp.diff(gg,t):0})
moving={pp:p10/a**3,gg:(A-1)*p10/(2*Cp**2*a**3)}
equal('EL_time_coefficient_omission', (EL-EL_frozen).subs(moving).doit(),
      6*p10*sp.diff(a,t)/a*(A*(sp.diff(chi,t)-Cp*psi)-3*Cp*Phi))
equal('fixed_X_charge_violation',sp.diff(a**3*p1*Cp,t),3*a**2*sp.diff(a,t)*p1*Cp)

# Exact constitutive completion: a positive-X interval, m>1/2 and rho0>0.
m, R, z, Y, Yd=sp.symbols('m rho0 z Y Yd',positive=True)
pc=R/(2*m)*((X/X0)**m-1)
rc=sp.simplify(2*X*sp.diff(pc,X)-pc)
equal('completion_affine_EOS',pc,(rc-R)/(2*m-1))
equal('completion_sound_speed',sp.diff(pc,X)/sp.diff(rc,X),1/(2*m-1))
equal('completion_zero_pressure',pc.subs(X,X0))
equal('completion_fixed_density',rc.subs(X,X0),R)
equal('completion_fixed_first_jet',sp.diff(pc,X).subs(X,X0),R/(2*X0))
equal('completion_second_jet',sp.diff(pc,X,2).subs(X,X0),R*(m-1)/(2*X0**2))
equal('completion_m_derivative',sp.diff(R*(sp.exp(m*z)-1)/(2*m),m),R*((m*z-1)*sp.exp(m*z)+1)/(2*m**2))

# Flat at Y=0, asymptotically proportional to sqrt(Y), with the same Yd.
B=(1+(Y/Yd)**2)**sp.Rational(1,4)
mY=1+(A-1)/(2*B)
equal('smooth_m_Y_at_zero',sp.diff(mY,Y).subs(Y,0))
equal('smooth_m_at_zero',mY.subs(Y,0),(A+1)/2)
equal('smooth_m_YY_at_zero',sp.diff(mY,Y,2).subs(Y,0),-(A-1)/(4*Yd**2))
equal('smooth_B_asymptotic',sp.limit(B/sp.sqrt(Y/Yd),Y,sp.oo),1)
psmooth=pc.subs(m,mY)
equal('all_X_pY_zero',sp.diff(psmooth,Y).subs(Y,0))
equal('all_X_pXY_zero',sp.diff(psmooth,X,Y).subs(Y,0))
equal('all_X_pXXY_zero',sp.diff(psmooth,X,X,Y).subs(Y,0))
equal('completion_kinetic_coefficient',sp.diff(pc,X)+2*X*sp.diff(pc,X,2),
      (2*m-1)*R/(2*X)*(X/X0)**m)

# Conserved FRW trajectory at fixed homogeneous Y=0; a=1 sets X=X0.
av=sp.symbols('a',positive=True)
U=av**(-3*(1+1/A))
rhob=R*(A*U+1)/(A+1)
pb=R*(U-1)/(A+1)
equal('FRW_continuity',av*sp.diff(rhob,av)+3*(rhob+pb))
equal('FRW_charge',av**3*(av**(-6/A))**(A/2),1)
equal('FRW_sound_speed',sp.diff(pb,av)/sp.diff(rhob,av),1/A)

# Original sqrt(Y) switch is not differentiable in scalar spatial gradient
# at a rolling background. Exact counterexample using integer m(0)=2.
q=sp.symbols('q',real=True)
m_orig=1+1/(1+sp.Abs(q)) # A=3, delta=a0tilde=1
pcusp=((sp.Rational(2))**m_orig-1)/(2*m_orig)
right=sp.limit((pcusp-pcusp.subs(q,0))/q,q,0,dir='+')
left=sp.limit((pcusp-pcusp.subs(q,0))/q,q,0,dir='-')
assert sp.simplify(right-left)!=0

table=[]
A_num=10**10
delta=4e-5
for av_num in (1,0.3,0.01,0.001):
    logu=-3*(1+1/A_num)*math.log(av_num)
    u=math.exp(logu)
    rho_num=(A_num*u+1)/(A_num+1)
    pressure=math.expm1(logu)/(A_num+1)
    table.append(dict(a=av_num,relative_rho_to_dust=rho_num*av_num**3,
                      p_over_rho=pressure/rho_num,
                      log_X_over_X0=-6*math.log(av_num)/A_num,
                      rho_over_rho0=rho_num))

switch=[]
for s in (0,0.05,0.28,0.315,0.39,0.8):
    orig=1/(1+(A_num-1)/(1+s/delta))
    smooth=1/(1+(A_num-1)/(1+(s/delta)**4)**0.25)
    switch.append(dict(s=s,original_cs2=orig,smooth_cs2=smooth,relative_difference=smooth/orig-1))

result=dict(exact_identity_count=len(checks),residuals=checks,
    smallest_pressure_counterexample={'X':1,'X0':1,'p1':1,'g':1,'p':0,'rho':2,'cs2':'1/3','rho_cs2':'2/3'},
    cusp_counterexample={'A':3,'X_over_X0':2,'rho0':1,'q_left_derivative':str(left),'q_right_derivative':str(right)},
    cosmology_table=table,switch_comparison=switch,
    nonclaims=['No coupled field stability or strong-coupling cutoff is certified.',
               'No halo profile, CMB spectrum, or novelty claim is established.',
               'The completion is a new candidate action, not a validation of L291.'])
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
