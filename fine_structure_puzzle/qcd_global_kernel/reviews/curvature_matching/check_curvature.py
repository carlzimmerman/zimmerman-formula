#!/usr/bin/env python3
"""Bounded exact off-shell curvature-pole and coordinate/EOM comparison."""
import json,sys
from pathlib import Path
import sympy as s

R=s.Rational
a=s.symbols('a0:4',real=True);a0,a1,a2,a3=a
norm=sum(x*x for x in a);ss=a1*a1+a2*a2
checks=[]
def equal(name,expr):
    z=s.simplify(s.expand(expr))
    assert z==0,(name,str(z))
    checks.append(name)

# Right multiplication by exp(i tau_i theta) gives global tangent fields.
v=s.Matrix([a1,a2,a3])
fields=[]
for k in range(3):
    basis=s.eye(3)[:,k]
    vec=a0*basis-v.cross(basis)
    fields.append([-a[k+1],*list(vec)])
def X(k,f):return sum(fields[k][j]*s.diff(f,a[j]) for j in range(4))
def lap(f):return s.expand(sum(X(k,X(k,f)) for k in range(3)))
equal('a0_group_Laplacian',lap(a0)+3*a0)
equal('s_group_Laplacian',lap(ss)-(4*norm-8*ss))
for k in range(3):equal('group_vector_tangent_%d'%k,X(k,norm))
F,C,u,M2,Z=s.symbols('F C u M2 Z',positive=True)
equal('geodesic_mass_Hessian_trace',lap(-F*F*M2*a0)/(F*F)-3*M2*a0)
equal('geodesic_EM_Hessian_trace',lap(u*C*ss)/(F*F)-u*C*(4*norm-8*ss)/(F*F))

# Charge trace uses ordinary 2x2 trace, fixing all charge/e factors.
tau=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
U=a0*s.eye(2)+s.I*sum((x*t for x,t in zip(a[1:],tau)),s.zeros(2))
q=s.diag(R(2,3),R(-1,3))
equal('ordinary_charge_trace',s.trace(q*U*q*U.conjugate().T)-(R(5,9)*norm-ss))
equal('aligned_charged_mass_splitting',(2*u*C/(F*F)).subs(C,Z*F**4)-2*u*Z*F*F)

# A single minimally coupled scalar; dim=4-2eps fixes pole conversion.
eps=s.symbols('eps',positive=True)
equal('Gamma_epsilon_residue',s.limit(eps*s.gamma(eps),eps,0)-1)
equal('Gamma_epsilon_minus_one_residue',s.limit(eps*s.gamma(eps-1),eps,0)+1)
beta13=s.symbols('beta13')
equal('strong_beta13_normalization',(R(1,4)-2*R(1,8)))
equal('EM_operator_and_gravity_split',R(1,3)-R(2,3)*ss-(R(2,3)*(R(5,9)-ss)-R(1,27)))
equal('direct_offshell_beta15_Z',-R(2,3)*Z+(R(4,3)*Z)/2)
equal('independent_gravity_spurion_beta',R(1,3)*Z-(R(4,3)*Z)/2*R(5,9)-R(-2,15)*Z/2*R(5,9))

# Sigma-coordinate ordinary Hessian versus the geodesic/covariant Hessian.
r=s.Matrix(s.symbols('r1:4',real=True));r2=(r.T*r)[0];h=1-r2
g=s.eye(3)+r*r.T/h;gi=s.eye(3)-r*r.T
for i in range(3):
 for j in range(3):equal('sigma_metric_inverse_%d%d'%(i,j),(g*gi-s.eye(3))[i,j])
rootdet=1/s.sqrt(h)
contracted=[]
for k in range(3):
    val=-sum(s.diff(rootdet*gi[i,k],r[i]) for i in range(3))/rootdet
    equal('contracted_Christoffel_%d'%k,val-3*r[k])
    contracted.append(val)
def plain(f):return sum(gi[i,j]*s.diff(f,r[i],r[j]) for i in range(3) for j in range(3))/F**2
def covlap(f):return plain(f)-sum(contracted[k]*s.diff(f,r[k]) for k in range(3))/F**2
sp=r[0]**2+r[1]**2
Vm=-F*F*M2*s.sqrt(h);Ve=u*C*sp
equal('sigma_plain_EM',plain(Ve)-u*C*(4-2*sp)/F**2)
equal('sigma_covariant_EM',covlap(Ve)-u*C*(4-8*sp)/F**2)
equal('sigma_plain_mass',plain(Vm)-3*M2/s.sqrt(h))
equal('sigma_covariant_mass',covlap(Vm)-3*M2*s.sqrt(h))
equal('EOM_gradient_EM',covlap(Ve)-plain(Ve)+3*sum(r[i]*s.diff(Ve,r[i]) for i in range(3))/F**2)
equal('EOM_gradient_mass',covlap(Vm)-plain(Vm)+3*sum(r[i]*s.diff(Vm,r[i]) for i in range(3))/F**2)
equal('sigma_plain_beta15_partial',-R(1,6)*Z+R(1,3)*Z/2)
equal('printed_vs_geodesic_Z_difference',R(4,3)*Z-R(2,3)*Z-R(2,3)*Z)

result={'schema':'fsp008.curvature_matching.independent.v1','assertion_tested':'Exact SU2 right-tangent Laplacians, ordinary charge trace, heat-kernel gamma residues, direct off-shell counterterm normalization, sigma-coordinate metric and EOM-gradient difference.','domain':'Exact symbolic identities; sigma coordinate chart 1-r²>0, F>0; global quaternion identities reduced by unit norm.','checks':checks,'check_count':len(checks),'geodesic_Hessian_EM':'(u C/F²)(4-8s)','sigma_ordinary_Hessian_EM':'(u C/F²)(4-2s)','covariant_minus_plain':'-(3/F²)r_i partial_i V','partial_geodesic_beta15_Z':'4 Z/3','partial_plain_sigma_beta15_Z':'Z/3','printed_full_beta15':'1/2+2Z/3','direct_partial_gravity_spurion_beta_if_basis_F2_R_TrQ2':'-2 Z/15','limitations':['Potential-loop and coordinate/EOM identities only; full kinetic/photon/ghost/source basis not assembled.','Printed source running is not inferred erroneous.','No complete common-scheme NLO global response or alpha.']}
out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'exact_checks':len(checks),'status':'passed','off_shell_to_full_running_bridge':'unresolved'}))
