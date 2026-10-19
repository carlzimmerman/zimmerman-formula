#!/usr/bin/env python3
"""Independent bounded algebra/angle/regulator review; no QCD data imported."""
import json, sys
from pathlib import Path
import sympy as s
import mpmath as mp

out=Path(sys.argv[1]); R=s.Rational
checks=[]
def exact(name, expr):
    assert s.simplify(expr)==0, (name,expr)
    checks.append(name)

# Direct differentiation of an abstract two-configuration source quotient.
# This construction uses exponentials, rather than the author's jet algebra.
x,y=s.symbols('x y',real=True)
p=[R(2,5),R(3,5)]
Bs=[2+3*x-y+2*x*y+x*x, -1+x+4*y-x*y+3*y*y]
Ls=[x+2*y+3*x*y+x*x,-2*x+y-2*x*y+y*y]
E=lambda values:sum(a*b for a,b in zip(p,values))
cov=lambda a,b:E([aa*bb for aa,bb in zip(a,b)])-E(a)*E(b)
at0=lambda f:f.subs({x:0,y:0})
N=E([b*s.exp(l) for b,l in zip(Bs,Ls)])
Z=E([s.exp(l) for l in Ls])
C=N/Z
B=[at0(b) for b in Bs]
U=[[at0(s.diff(l,t)) for l in Ls] for t in (x,y)]
Ba=[[at0(s.diff(b,t)) for b in Bs] for t in (x,y)]
mu_nonzero=E(U[0])
assert mu_nonzero!=0
quotient=[]
for a,t in enumerate((x,y)):
    for b,v in enumerate((x,y)):
        Hab=[at0(s.diff(l,t,v)) for l in Ls]
        Bab=[at0(s.diff(bb,t,v)) for bb in Bs]
        third=E([(bb-E(B))*(ua-E(U[a]))*(ub-E(U[b]))
                 for bb,ua,ub in zip(B,U[a],U[b])])
        rhs=E(Bab)+cov(Ba[a],U[b])+cov(Ba[b],U[a])+cov(B,Hab)+third
        exact('quotient_%d%d'%(a,b),at0(s.diff(C,t,v))-rhs)
        # The Gaussian-integrated ratio has uncentered determinant Hessian.
        num=E(Bab)+E([aa*bb for aa,bb in zip(Ba[a],U[b])])+E([aa*bb for aa,bb in zip(Ba[b],U[a])])+cov(B,[hh+ua*ub for hh,ua,ub in zip(Hab,U[a],U[b])])
        Ca=[at0(s.diff(C,t)),at0(s.diff(C,v))]
        extra=Ca[0]*E(U[b])+Ca[1]*E(U[a])
        exact('integrate_then_normalize_%d%d'%(a,b),num-rhs-extra)
        quotient.append({'ab':[a,b],'C_ab':str(rhs),'Gaussian_integrated_second_coefficient_before_half_G':str(num),'nonzero_mean_extra':str(extra)})

# Noncommuting exact matrices distinct from author's finite benchmark.
D0=s.Matrix([[4,1,0],[0,3,1],[1,0,5]])
Va=s.Matrix([[0,1,2],[2,1,0],[1,-1,1]])
Vb=s.Matrix([[1,-2,0],[0,2,1],[3,0,-1]])
W=s.Matrix([[1,0,1],[-1,2,0],[0,1,-2]])
Sl=(D0+R(2,3)*s.eye(3)).inv()
mass_rows=[]
for delta in [R(-1,4),R(0),R(3,5),R(2)]:
    Ss=(D0+(R(2,3)+delta)*s.eye(3)).inv()
    exact('resolvent_'+str(delta),sum((Sl-Ss-delta*Sl*Ss).applyfunc(abs)))
    ell=(R(2,3)-R(1,3))*s.trace(Sl*Va)-R(1,3)*s.trace(Ss*Va)
    exact('charge_sum_'+str(delta),ell-delta*s.trace(Sl*Ss*Va)/3)
    h=lambda z:s.trace(z*W-z*Va*z*Vb)
    P=Sl*Ss
    exact('same_loop_difference_'+str(delta),h(Ss)-h(Sl)-delta*s.trace(-P*W+P*Va*Ss*Vb+Sl*Va*P*Vb))
    exact('flavor_square_'+str(delta),R(5,9)*h(Sl)+R(1,9)*h(Ss)-R(2,3)*h(Sl)-(h(Ss)-h(Sl))/9)
    mass_rows.append({'delta':str(delta),'single_loop':str(ell),'same_loop':str(R(5,9)*h(Sl)+R(1,9)*h(Ss))})
assert mass_rows[1]['single_loop']=='0' and mass_rows[1]['same_loop']!='0'

# An exact complex-valued Cauchy-Schwarz bound, using centered product variance.
BC=[1+s.I,2-s.I,-2+3*s.I]
TC=[2-s.I,-1+2*s.I,3+s.I]
TD=[1+2*s.I,4-s.I,-3]
pr=[R(1,4),R(1,2),R(1,4)]
EC=lambda a:sum(w*v for w,v in zip(pr,a))
cen=lambda a:[v-EC(a) for v in a]
var=lambda a:EC([s.expand_complex(v*s.conjugate(v)) for v in cen(a)])
YP=[a*b for a,b in zip(cen(TC),cen(TD))]
kk=EC([a*b for a,b in zip(cen(BC),YP)])
gap=s.simplify(var(BC)*var(YP)-kk*s.conjugate(kk))
assert gap>=0
checks.append('complex_centered_product_covariance_bound')

# Independent explicit gamma trace for the point theory.
I=s.I; eye=s.eye(2); zero=s.zeros(2)
pauli=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-I],[I,0]]),s.diag(1,-1)]
g0=s.diag(1,1,-1,-1)
g=[g0]+[zero.row_join(a).col_join((-a).row_join(zero)) for a in pauli]
m,Q,xx=s.symbols('m Q xx',positive=True,real=True)
pslash=m*g0
qslash=I*Q*xx*g0-Q*s.sqrt(1-xx*xx)*g[3]
contract=sum((g[mu]*(pslash-qslash+m*s.eye(4))*g[mu]*(1 if mu==0 else -1) for mu in range(4)),s.zeros(4))
trace=s.trace((pslash+m*s.eye(4))*contract)
exact('explicit_Minkowski_gamma_trace',trace-(8*m*m+8*I*m*Q*xx))
even=s.simplify(((m+I*Q*xx)/(Q*Q+2*I*m*Q*xx)+(m-I*Q*xx)/(Q*Q-2*I*m*Q*xx))/2)
exact('paired_Euclidean_selfenergy',even-m*(Q*Q+2*Q*Q*xx*xx)/(Q**4+4*m*m*Q*Q*xx*xx))

# Soft series for arbitrary charge and moment; does not use authors' code.
t,zcharge,pa=s.symbols('t zcharge pa',real=True)
f1=zcharge+s.Symbol('slope')*t*t
f2=pa+s.Symbol('slope2')*t*t
A=f1*f1+t*t*f2*f2
Cc=A*(1+t*t)-3*t*t*(f1+f2)**2
BB=Cc*(s.sqrt(1+t*t)-t)+t*(3*f1*f1-A)/2
soft=s.series(BB,t,0,4).removeO().expand()
exact('soft_charge_constant',soft.coeff(t,0)-zcharge*zcharge)
exact('soft_arbitrary_Pauli_linear_cancellation',soft.coeff(t,1))
X=s.symbols('X',positive=True)
evan=s.integrate(2*X-2,(X,0,1))
logterm=s.integrate(-2*(4-2*X)*s.log(1-X),(X,0,1))
exact('MSbar_evanescent_plus_log_finite',evan+logterm-4)

mp.mp.dps=65
fmt=lambda v:mp.nstr(v,55)
def bdir(z):
    rr=mp.sqrt(1+z*z)
    return (rr+2*z)/(rr+z)**2
def born(z,f,g):
    a=f*f+z*z*g*g
    return ((1+z*z)*a-3*z*z*(f+g)**2)/(mp.sqrt(1+z*z)+z)+z*(3*f*f-a)/2
angles=[]
for raw in ['.003','.07','.3','3','31']:
    z=mp.mpf(raw)
    for f,gp in [(mp.mpf(1),mp.mpf(0)),(mp.mpf(1),mp.mpf('2.3')),(mp.mpf('-.4'),mp.mpf('.8'))]:
        # theta on S3, rather than direct x quadrature.
        def ff(th):
            x0=mp.cos(th)
            T1=2*(z*z*(f+gp)**2/(z*z+x0*x0)-f*f)
            T2=2*(f*f+z*z*gp*gp)/(z*z+x0*x0)
            return mp.sin(th)**2*(-3*T1+(1-x0*x0)*T2)
        val=2*mp.quad(ff,[0,mp.pi/2-mp.atan(z),mp.pi/2])*z/(2*mp.pi)
        err=abs(val-born(z,f,gp));assert err<mp.mpf('1e-52')
        angles.append({'z':raw,'F1':str(f),'F2':str(gp),'absolute_error':fmt(err)})

P=lambda Q,L:1/((1+(Q/L)**2)*(1+2*(Q/L)**2))
pvrows=[]
for raw in ['.03','.1','1','16','1024']:
    L=mp.mpf(raw)
    # Q=L*tan(theta) maps the full integral onto a finite interval.
    def it(th):
        if th==mp.pi/2:return mp.mpf(0)
        q=L*mp.tan(th)
        return bdir(q/2)*P(q,L)*L/(mp.cos(th)**2)/(4*mp.pi**2)
    pivot=mp.atan(1/L)
    value=mp.quad(it,sorted(set([mp.mpf(0),pivot,mp.pi/4,mp.pi/2])))
    ct=(-3*mp.log(L*L)+mp.mpf('2.5')+6*mp.log(2))/(16*mp.pi**2)
    pvrows.append({'Lambda_over_m':raw,'PV_value':fmt(value),'MSbar_matched_mu_m':fmt(value+ct),'difference_from_MSbar_limit':fmt(value+ct-1/(4*mp.pi**2))})

data={'schema':'fsp008.independent_kernel_flavor_review.v1','exact_checks':checks,'exact_check_count':len(checks),'quotient_cases':quotient,'mass_cases':mass_rows,'complex_CS_squared_gap':str(gap),'soft_series_arbitrary_charge_moment':str(soft),'angular_cases':angles,'PV_cases':pvrows,'IR_per_e2':fmt(1/(4*mp.pi**2)),'nonclaims':['No QCD ensemble or all-momentum physical proton tensor.','No alpha or cosmological datum.','65-digit quadrature comparisons are not interval error certification.','Abstract nonzero-mean source example is a normalization diagnostic; physical C-invariant QCD has zero one-current means.']}
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'exact_checks':len(checks),'angular_cases':len(angles),'PV_cases':len(pvrows),'max_angle_error':max(float(a['absolute_error']) for a in angles),'IR_per_e2':data['IR_per_e2']},indent=2))
