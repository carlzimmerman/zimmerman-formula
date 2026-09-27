#!/usr/bin/env python3
"""Off-shell ADM trace velocity Hessian and primary momentum relations."""
import argparse,json
from pathlib import Path
import sympy as S
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
B,r,s,K,VU,VN,hfac,N,dh,dU,dnu=S.symbols('B r s K VU VN sqrt_h N htrace_dot Udot nudot',real=True)
Q=B+S.Rational(2,3);T=2+3*B
checks={}
def exact(n,v):
    v=S.factor(v);checks[n]={'residual':str(v),'passed':v==0};assert v==0,(n,v)
# Standard ADM sign K=(h^ij hdot_ij - shift terms)/(2N), so K=-K_display.
trace=-Q*(K-3*r*VU-3*s*VN)**2
expanded=-Q*K*K+2*T*r*K*VU+2*T*s*K*VN-3*T*r*r*VU*VU-6*T*r*s*VU*VN-3*T*s*s*VN*VN
exact('full_trace_factorization',trace-expanded)
H=S.hessian(trace,(K,VU,VN));a=S.Matrix([1,-3*r,-3*s])
for i in range(3):
    for j in range(3):exact('hessian_entry_'+str(i)+str(j),H[i,j]+2*Q*a[i]*a[j])
for idx,nvec in enumerate([S.Matrix([3*r,1,0]),S.Matrix([3*s,0,1])]):
    for j,val in enumerate(H*nvec):exact('null_vector_'+str(idx)+'_'+str(j),val)
assert H.rank()==1
checks['trace_rank_one']={'rank':1,'condition':'B+2/3 != 0','passed':True}
full=S.diag(2,2,2,2,2,H)
assert full.rank()==6
checks['full_velocity_rank_six']={'rank':6,'dimension':8,'condition':'B+2/3 != 0; N != 0; positive invertible spatial metric','passed':True}
# htrace_dot is h^ij hdot_ij; pi_trace=3*dL/dhtrace_dot.
density=N*hfac*trace.subs({K:dh/(2*N),VU:dU/N,VN:dnu/N})
pi_trace=3*S.diff(density,dh)
pU=S.diff(density,dU);pnu=S.diff(density,dnu)
exact('primary_U_constraint',pU+2*r*pi_trace)
exact('primary_lapse_constraint',pnu+2*s*pi_trace)
# Einstein kinetic trace includes -2/3 K^2; the extra -B K^2 is explicit.
exact('Einstein_trace_included',Q-(B+S.Rational(2,3)))
wrong=S.factor((pU-2*r*pi_trace).subs({B:1,r:1,s:0,hfac:1,N:1,dh:1,dU:0,dnu:0}))
assert wrong!=0
checks['ADM_sign_negative_control']={'wrong_sign_residual':str(wrong),'passed':True}
result={'result':'Exact nonlinear trace kinetic Hessian has rank one and yields two primary momentum constraints; not a complete Dirac count.',
 'checks':checks,'standard_ADM_factor':'-Q(K_ADM-3r V_U-3s V_N)^2',
 'primary_constraints':['p_U+2r*pi_trace=0','p_lnn+2s*pi_trace=0'],
 'conformal_coordinate':'hbar_ij=exp[-2(r U+s lnN)] h_ij; its trace scalar is v=psi+rU+sphi',
 'scope':'Fixed real coefficients r,s,B, positive lapse and spatial metric; spatial-gradient-only penalty does not add velocities.',
 'non_claims':['No secondary constraint or Poisson-bracket closure calculation','No physical scalar classification','No full nonlinear well-posedness theorem']}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
