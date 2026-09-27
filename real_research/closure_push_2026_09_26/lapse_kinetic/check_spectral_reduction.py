#!/usr/bin/env python3
"""Exact two-mode analogue of normalized lapse spectral reduction."""
import argparse,json
from pathlib import Path
import sympy as S
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
q,p,c,g,eta=S.symbols('q p c gap eta',real=True)
theta=q+S.pi/4
lam=p+q*q
M=S.diag(S.exp(q),S.exp(-q))
root=S.diag(S.exp(q/2),S.exp(-q/2))
invroot=S.diag(S.exp(-q/2),S.exp(q/2))
u=S.Matrix([S.cos(theta),S.sin(theta)])
v=S.Matrix([-S.sin(theta),S.cos(theta)])
K=root*(lam*S.eye(2)+g*v*v.T)*root
y=invroot*u
checks={}
def exact(name,expr):
    # Expand both angle sums and their products before trig reduction; the
    # default simplifier leaves a rotated quadratic-form identity unreduced.
    value=S.simplify(S.trigsimp(S.expand(S.expand_trig(expr))))
    checks[name]={'residual':str(value),'passed':value==0}
    assert value==0,(name,value)

exact('mass_normalization',(y.T*M*y)[0]-1)
for idx,val in enumerate(K*y-lam*M*y):exact('generalized_eigenvector_'+str(idx),val)
exact('positive_branch_offdiagonal',K[0,1]+g*S.cos(theta)*S.sin(theta))
H=-(y.T*K*y)[0]
exact('normalized_H_equals_minus_eigenvalue',H+lam)
eta_q=S.simplify((y.T*S.diff(M,q)*y)[0])
exact('metric_volume_variation',eta_q-S.cos(2*theta))
hf_q=(y.T*S.diff(K,q)*y)[0]
exact('generalized_Hellmann_Feynman_q',hf_q-S.diff(lam,q)-lam*eta_q)
exact('generalized_Hellmann_Feynman_p',(y.T*S.diff(K,p)*y)[0]-S.diff(lam,p))
exact('fixed_lapse_H_variation_correction',-hf_q+S.diff(lam,q)+lam*eta_q)
exact('normalized_total_derivative',S.diff(H,q)+S.diff(lam,q))
exact('normalization_derivative',2*(y.T*M*S.diff(y,q))[0]+eta_q)
exact('chain_rule_correction',(-2*lam*y.T*M*S.diff(y,q))[0]-lam*eta_q)

# A normalized shape coordinate, positive branch near eta=0.
shape=invroot*S.Matrix([S.cos(theta+eta),S.sin(theta+eta)])
Hfull=-c*(shape.T*K*shape)[0]
exact('shape_Hamiltonian',Hfull+c*(lam+g*S.sin(eta)**2))
exact('shape_stationarity',S.diff(Hfull,eta).subs(eta,0))
exact('shape_secondary_primary_bracket',-S.diff(Hfull,eta,2).subs(eta,0)-2*c*g)
Hred=-c*lam
qdot=S.diff(Hred,p);pdot=-S.diff(Hred,q)
exact('reduced_qdot',qdot+c)
exact('reduced_pdot',pdot-2*c*q)
exact('global_constraint_preserved',S.diff(lam,q)*qdot+S.diff(lam,p)*pdot)
exact('global_constraint_regularity',S.diff(lam,p)-1)

# General second-class graph reduction block: p_shape=0, shape-Y(z)=0.
J=S.Matrix([[0,1],[-1,0]])
zero=S.zeros(2);eye=S.eye(2)
constraint_matrix=S.BlockMatrix([[zero,-eye],[eye,J]]).as_explicit()
inverse=S.BlockMatrix([[J,eye],[-eye,zero]]).as_explicit()
for idx,val in enumerate(constraint_matrix*inverse-S.eye(4)):
    exact('second_class_block_inverse_'+str(idx),val)
assert inverse[2:4,2:4]==zero
checks['canonical_z_Dirac_bracket']={'passed':True,'reason':'For z-only observables the p_shape brackets vanish and the shape-shape block of the inverse constraint matrix is zero.'}
control=S.simplify((lam*eta_q).subs({q:S.pi/8,p:0}))
assert control!=0
checks['missing_volume_term_negative_control']={'passed':True,'q':'pi/8','p':0,'omitted_term':str(control)}
out={'result':'Exact finite-dimensional spectral normalization and conditional symplectic reduction identities pass.',
 'checks':checks,'model':{'mass_matrix':str(M),'groundvalue':str(lam),'gap':str(g),'positive_groundvector_range':'-pi/4<q<pi/4','shape_regularity':'c>0,gap>0'},
 'reduced_dynamics':{'Hamiltonian':'-c(t)(p+q^2)','qdot':str(qdot),'pdot':str(pdot),'lambda_dot':'0'},
 'continuum_correction':'d lambda = d quadratic_form|y - lambda*d norm|y; fixed-y dH=-d lambda-lambda*d norm|y; the normalized total pullback is H=-lambda.',
 'non_claims':['Not a continuum PDE existence theorem','Not a proof that all omitted full-theory constraints are compatible','Not a spectral-gap proof on noncompact leaves','Not a particle/clock field classification or completed MOND splice']}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
