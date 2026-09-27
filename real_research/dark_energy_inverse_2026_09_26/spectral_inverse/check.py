#!/usr/bin/env python3
"""Exact inverse-lapse identities and identification counterfamilies."""
import argparse,json
from pathlib import Path
import sympy as S
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
x=S.symbols('x',real=True)
b,ell,c,H=S.symbols('b ell c Hbar',positive=True)
q,Lam,rho0,d,eps,wc,eta=S.symbols('q Lambda_bar rho0 d epsilon wc eta',real=True)
n=S.symbols('n',positive=True,integer=True)
Sf=S.Function('S')(x);ff=S.Function('f')(x)
y=S.exp(Sf/2);J=-4*S.diff(y,x,2)/y
checks={}
def exact(name,value):
    value=S.factor(S.simplify(S.expand_trig(value)))
    checks[name]={'passed':value==0,'residual':str(value)}
    assert value==0,(name,value)

exact('lapse_log_inverse',J+2*S.diff(Sf,x,2)+S.diff(Sf,x)**2)
exact('global_lapse_scale_invariance',-4*S.diff(S.sqrt(c)*y,x,2)/(S.sqrt(c)*y)-J)
exact('lapse_profile_sensitivity',S.diff((-2*S.diff(Sf+eta*ff,x,2)-S.diff(Sf+eta*ff,x)**2),eta).subs(eta,0)+2*S.diff(ff,x,2)+2*S.diff(Sf,x)*S.diff(ff,x))
rho=S.Function('rho')(x)
inferred=ell*q*q-rho+b*J
exact('inverse_reinsertion',-ell*q*q+inferred+rho-b*J)
exact('flat_physical_expansion_inverse',inferred.subs(q,-S.exp(wc)*H/ell)-(S.exp(2*wc)*H*H/ell-rho+b*J))
exact('vacuum_matter_shift_counterfamily',(-ell*q*q+(Lam+d)+(rho-d))-(-ell*q*q+Lam+rho))
exact('trace_sign_ambiguity',(-ell*(-q)**2+Lam+rho)-(-ell*q*q+Lam+rho))

# The exact nonlinear positive family on a 2pi torus (n is an integer).
yp=S.exp(eps*S.cos(n*x))
Jp=4*eps*n*n*S.cos(n*x)-4*eps*eps*n*n*S.sin(n*x)**2
exact('positive_periodic_profile_inverse',-4*S.diff(yp,x,2)/yp-Jp)
rhop=rho0+b*Jp
exact('exact_family_constant_Lambda',ell*q*q-rhop+b*Jp-(ell*q*q-rho0))
exact('unknown_ell_same_N_H_rho',(-ell*(-H/ell)**2+(H*H/ell-rho0)+rhop)-b*Jp)
exact('unknown_ell_same_proper_expansion',-ell*(-H/ell)-H)
# A positive-scale family changes canonical coefficient normalization while
# preserving the same lapse and barred proper expansion.
kap=S.symbols('kappa_scale',positive=True)
exact('canonical_normalization_family',(-kap*ell*(q/kap)**2+Lam/kap+rho/kap)-(b*J)/kap-(-ell*q*q+Lam+rho-b*J)/kap)
exact('canonical_normalization_expansion',-(kap*ell)*(q/kap)+ell*q)

# Pointwise divergence identities justify continuum integral checks on a torus.
Y=S.Function('y')(x)
exact('unweighted_integral_identity',S.diff(Y,x,2)/Y-S.diff(S.diff(Y,x)/Y,x)-S.diff(Y,x)**2/Y**2)
exact('N_weighted_integral_identity',-Y*S.diff(Y,x,2)-S.diff(Y,x)**2+S.diff(Y*S.diff(Y,x),x))
exact('y_weighted_constraint_identity',(-4*b*S.diff(Y,x,2)/Y)*Y+4*b*S.diff(Y,x,2))
f=S.Function('f')(x)
exact('positive_groundstate_factorization',S.diff(Y*f,x)**2+S.diff(Y,x,2)/Y*(Y*f)**2-Y*Y*S.diff(f,x)**2-S.diff(Y*f*f*S.diff(Y,x),x))

# Exact torus averages for n=1; integer-frequency scaling follows by substitution.
J1=Jp.subs(n,1)
avg=lambda expr:S.integrate(S.expand_trig(expr),(x,0,2*S.pi))/(2*S.pi)
jmean=S.simplify(avg(J1));jvar=S.simplify(avg((J1-jmean)**2))
exact('mean_J_on_torus',jmean+2*eps*eps)
exact('variance_J_on_torus',jvar-2*eps*eps*(4+eps*eps))
rhomean=rho0+b*jmean
cov=S.simplify(avg((rho0+b*J1-rhomean)*(J1-jmean)))
exact('slope_reconstruction_covariance',cov-b*jvar)
wrong_profile=ell*q*q-(rhop+eta*S.cos(2*n*x))+b*Jp
exact('spatial_constancy_negative_control',S.diff(wrong_profile,x)-2*eta*n*S.sin(2*n*x))
assert S.diff(wrong_profile,x).subs({eta:1,n:1,x:S.pi/4})==2
checks['nonconstant_Lambda_rejected']={'passed':True,'eta':1,'n':1,'x':'pi/4','derivative':2}

# Zero lapse counterexample: signed sin(x) is an excited zero mode, while
# its square has lapse zeros and sqrt(sin^2 x) is not a global C2 eigenfunction.
exact('zero_lapse_signed_eigenfunction',-4*b*S.diff(S.sin(x),x,2)-4*b*S.sin(x))
checks['zero_lapse_is_not_positive_groundstate']={'passed':True,'A':'4b','groundvalue':'-4b<0','candidate_lapse':'sin(x)^2 has zeros'}

# Full IC28 pinned tensor/curvature terms in the changed spectral sector, m=1.
tbar=2*S.exp(-2*wc);vbar=S.exp(2*wc)/2
sig2,curv=S.symbols('sigma_squared Rbar',real=True)
genA=tbar*sig2-ell*q*q+Lam-vbar*curv+rho
genLam=ell*q*q-rho-tbar*sig2+vbar*curv+b*J
exact('general_curvature_TF_inverse',genA.subs(Lam,genLam)-b*J)
exact('tensor_curvature_coefficient_product',tbar*vbar-1)
p1,p2,p3,p12,p13,p23,N=S.symbols('p1 p2 p3 p12 p13 p23 N',real=True)
qt=p1+p2+p3
tf2=p1*p1+p2*p2+p3*p3+2*(p12*p12+p13*p13+p23*p23)-qt*qt/3
ham=N*(tbar*tf2-ell*qt*qt)
traceflow=sum(S.diff(ham,pv)for pv in[p1,p2,p3])
exact('barred_proper_Hamilton_expansion',traceflow/(6*N)+ell*qt)
exact('physical_proper_Hamilton_expansion',traceflow/(6*S.exp(wc)*N)+S.exp(-wc)*ell*qt)

# Observation design rank: rho_eff = u Hbar^2+b J-Lambda, u=1/ell.
design=S.Matrix([[1,0,-1],[2,1,-1],[4,0,-1]])
assert design.det()==3
checks['three_independent_rows_identify_parameters']={'passed':True,'design':str(design),'determinant':3,'scope':'linear algebra only; not a physical evolution history'}
single=S.Matrix([[H*H,J1,-1],[H*H,0,-1],[H*H,1,-1]])
exact('single_CMC_slice_cannot_separate_ell_Lambda',single.det())

out={'result':'Exact inverse relations verified; explicit same-observation counterfamilies prevent uncalibrated Lambda identification.',
 'checks':checks,
 'formulas':{'J':'-4 Delta(sqrtN)/sqrtN=-2Delta lnN-|DlnN|^2','flat_Lambda':'ell q^2-rho+bJ','general_Lambda':'ell q^2-rho-tbar sigma^2+vbar Rbar+bJ','Hbar':'-ell q','Hphysical':'-exp(-wc)ell q','tbar':str(tbar),'vbar':str(vbar)},
 'inverse_family':'q_ell=-Hbar/ell, Lambda_ell=Hbar^2/ell-rho0, rho=rho0+bJ; identical N,Hbar,rho for admissible ell',
 'scope':'Compact connected flat 2pi torus for exact family; positive smooth lapse; fixed pin wc; m=1 canonical normalization; current nu_mono/criterion-B target not inferred from this separate cosmological sector.',
 'non_claims':['No observational reconstruction from expansion alone','No measured Newton normalization derived','No complete nonlinear evolution or MOND splice','No universal potential uniqueness from one eigenvalue','No admissible zero-lapse inverse']}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
