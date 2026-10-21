#!/usr/bin/env python3
"""Bounded exact checks for the Hodge/clock S2 candidate; not a theory validator.

Command: python3 checks.py --output run_001/results.json
Run from this directory, or pass an absolute --output path. No repo imports/data.
"""
import argparse
import json
import math
import platform
from pathlib import Path
import sympy as s

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
args = parser.parse_args()
checks = {}
def check(name, condition, detail):
    checks[name] = {'passed': bool(condition), 'detail': str(detail)}
    if not condition:
        raise AssertionError(name + ': ' + str(detail))
def zero(name, expr):
    val = s.simplify(expr)
    check(name, val == 0, val)

K, a0, u, g, gam, eta, beta, k = s.symbols(
    'K a0 u g gamma eta beta k', positive=True)
W = a0**2*(-u/a0-s.log(1-u/a0))/K
Wr = W-u**2/(2*K)
zero('full_remainder_split', K*s.diff(Wr,u)-u**2/(a0-u))
zero('full_force', K*s.diff(W,u)-u/(1-u/a0))
zero('critical_quadratic', s.limit(s.diff(W,u,2),u,0)-1/K)
zero('remainder_zero_quadratic', s.limit(s.diff(Wr,u,2),u,0))
usol = a0*g/(a0+g)
zero('canonical_law', g-usol-g**2/(g+a0))
zero('longitudinal_full_hessian', K**2*s.diff(W,u,2)-K/(1-u/a0)**2)
zero('transverse_full_hessian', K**2*s.diff(W,u)/u-K/(1-u/a0))
x = s.symbols('x', positive=True)
check('static_hessian_positive_interior',
      s.simplify((K/(1-u/a0)-K).subs(u,a0*x/(1+x))).is_positive,
      'Transverse lower bound K*x>0; longitudinal >= transverse, for x>0.')
V = a0*(g-a0*s.log(1+g/a0))/K
zero('legendre_derivative', s.diff(V,g)-usol/K)
zero('BM_susceptibility', s.diff(-2*K*V,g)/(2*g)+a0/(g+a0))

# Weak-static two-potential variational coefficients (each spatial component).
ph, ps, p = s.symbols('dPhi dPsi P', real=True)
Lstat=(ps**2-2*ph*ps)/(2*K)+p*ph-K*p*p/2
zero('Psi_equation_coefficient', s.diff(Lstat,ps)-(ps-ph)/K)
zero('expanded_S2_quadratic', Lstat.subs(ps,ph)+(ph-K*p)**2/(2*K))

# Flat Hodge identity in Fourier space, with arbitrary covector and wavevector.
kv=s.Matrix(s.symbols('kx ky kz', real=True))
pv=s.Matrix(s.symbols('px py pz', real=True))
F=kv*pv.T-pv*kv.T
zero('flat_Hodge_symbol', (kv.dot(pv))**2+sum(v*v for v in F)/2-kv.dot(kv)*pv.dot(pv))

# Derivative TT variation, k along z with arbitrary P and both polarizations.
# Rotation of k to z loses no generality; P remains arbitrary.
hp,hc=s.symbols('hplus hcross', real=True)
htt=s.Matrix([[hp,hc,0],[hc,-hp,0],[0,0,0]])
wave=s.Matrix([0,0,k])
conn=[[[ (wave[i]*htt[j,l]+wave[j]*htt[i,l]-wave[l]*htt[i,j])/2
          for l in range(3)] for j in range(3)] for i in range(3)]
DP=s.Matrix(3,3,lambda i,j:-sum(conn[i][j][l]*pv[l] for l in range(3)))
divdelta=-sum(wave[i]*htt[i,j]*pv[j] for i in range(3) for j in range(3))
zero('TT_divergence_derivative',divdelta)
zero('TT_curl_derivative',sum((DP[i,j]-DP[j,i])**2 for i in range(3) for j in range(3)))
naive=s.simplify(sum(v*v for v in DP))
zero('naive_gradient_counterexample_formula',naive-k*k*pv.dot(pv)*(hp*hp+hc*hc)/2)
check('mutation_naive_gradient_changes_tensor_symbol',
      naive.subs({pv[0]:1,pv[1]:0,pv[2]:0,hp:1,hc:0,k:1})==s.Rational(1,2),
      'A naive |DP|^2 completion has nonzero TT spatial symbol at P != 0.')

# Exact P=0 Minkowski scalar action, spatial gauge hij=exp(2zeta)deltaij.
# pL=-i*k*zeta/K from lapse. Y=div shift, real mode phase chosen consistently.
zd,z,Y=s.symbols('zetadot zeta Y', real=True)
LEH=(-(6+9*beta)*zd**2+(4+6*beta)*zd*Y-beta*Y**2+2*k*k*z*z)/(4*K)
L0=LEH+eta*k*k*zd**2/(2*K*K)-(K+gam*k*k)*k*k*z*z/(2*K*K)
Ysol=s.solve(s.diff(L0,Y),Y)[0]
zero('zero_field_shift',Ysol-(2+3*beta)*zd/beta)
Lred=s.factor(L0.subs(Y,Ysol))
Q0=(2+3*beta)/(K*beta)+eta*k*k/(K*K)
zero('zero_field_reduced_action',Lred-(Q0*zd**2-gam*k**4*z*z/(K*K))/2)
w0=s.factor(gam*k**4/(K*(2+3*beta)/beta+eta*k*k))
zero('zero_field_low_k_limit',s.limit(w0/k**4,k,0)-gam*beta/(K*(2+3*beta)))
zero('zero_field_front_speed',s.limit(w0/k**2,k,s.oo)-gam/eta)
check('zero_field_positive_finite_k',w0.is_positive and Q0.is_positive,
      'All symbols positive; excludes k=0 and beta=0 rank-changing strata.')
zero('transverse_P_dispersion', (K+gam*k*k)/eta-K/eta-gam*k*k/eta)
check('mutation_negative_stiffness_unstable',
      w0.subs({K:1,beta:1,eta:1,gam:-1,k:1})<0,
      'Changing only the stiffness sign gives negative scalar omega^2.')

# Nonzero P: aligned high-frequency principal block AFTER leading lapse constraint.
# q is the longitudinal one-form fluctuation, Y=div shift. This is not a
# finite-k/off-shell dispersion or an arbitrary-angle/full-background reduction.
P,qd,q=s.symbols('P qdot q', real=True)
Lhi=eta*(qd-P*Y)**2/2-beta*Y**2/(4*K)-gam*k*k*q*q/2
D=beta-2*K*eta*P*P
Yhi=s.solve(s.diff(Lhi,Y),Y)[0]
zero('aligned_shift_solution',Yhi+2*K*eta*P*qd/D)
Lhireduced=s.factor(Lhi.subs(Y,Yhi))
Qhi=eta*beta/D
zero('aligned_reduced_action',Lhireduced-(Qhi*qd**2-gam*k*k*q*q)/2)
uhi=s.sqrt(beta*K/(2*eta))
zero('rank_loss_location',D.subs(P,uhi/K))
rankeq=s.simplify(s.diff(Lhi,Y).subs(beta,2*K*eta*P*P))
zero('rank_loss_constraint',rankeq+eta*P*qd)
zero('aligned_speed',gam/Qhi-(gam/eta)*(1-2*K*eta*P*P/beta))
check('forbidden_parameter_counterexample',
      Qhi.subs({K:1,eta:1,beta:1,P:1})<0,
      'Take a0=2, u=1, K=eta=beta=gamma=1: within cap, D=-1, Q=-1, c_parallel^2=-1.')
zero('finite_acceleration_at_threshold', (u/(1-u/a0)).subs(u,uhi)-a0*uhi/(a0-uhi))

# Orthogonal check of full shift quadratic matrix, arbitrary wave orientation.
PL,PT1,PT2=s.symbols('PL PT1 PT2', real=True)
vv=s.Matrix([PL,PT1,PT2])
shift=s.diag(-beta/(2*K),1/(4*K),1/(4*K))+eta*vv*vv.T
zero('oblique_shift_determinant',s.det(shift)/(-beta/(32*K**3))-
     (1-2*K*eta*PL*PL/beta+4*K*eta*(PT1*PT1+PT2*PT2)))

# Screened spherical inner particular solution; boundary matching is NOT checked.
r,GM,Lstar=s.symbols('r GM Lstar',positive=True)
Pr=GM/(2*gam)
lap=s.diff(Pr,r,2)+2*s.diff(Pr,r)/r-2*Pr/r**2
zero('screened_inner_radial_equation',gam*lap+GM/r**2)
zero('screened_inner_acceleration', (K*Pr).subs(gam,K*Lstar**2/2)-GM/Lstar**2)
pc=3.085677581491367e16
AU=149597870700.0
mu_sun=1.32712440018e20
solar=[{'Lstar_pc':lp,'u_inner_m_s2':mu_sun/(lp*pc)**2,
        'fraction_of_newtonian_at_1_AU':(AU/(lp*pc))**2}
       for lp in [24.0,1000.0]]

out={'claim':'Scoped S2 covariant candidate identities and counterexample; original four-gate goal OPEN',
     'software':{'python':platform.python_version(),'sympy':s.__version__},
     'checks':checks,'checks_passed':len(checks),
     'formulas':{'W_full':str(W),'W_rem':str(Wr),'Q_zero':str(Q0),
                 'omega_zero_squared':str(w0),'Q_aligned_high_frequency':str(Qhi),
                 'u_rank_loss':str(uhi),'shift_determinant_factor':str(s.factor(s.det(shift)/(-beta/(32*K**3))))},
     'illustrative_solar_screening':solar,
     'not_checked':['PPN/preferred-frame bounds','global/nonlinear well-posedness','strong coupling',
                    'general on-shell polarized halo spectrum','S3 current/mass embedding',
                    'finite-stiffness boundary-value solutions','cosmological perturbations'],
     'review_provenance':'self-review; exact algebra and separately derived ADM/connection controls'}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'checks_passed':len(checks),'status':'scoped identities verified; full goal open',
                  'solar':solar},indent=2))
