"""Exact local two-field completion and its explicitly degenerate control."""
import argparse, json
from pathlib import Path
import sympy as s

p=argparse.ArgumentParser(); p.add_argument('--output',required=True); args=p.parse_args()
k2,m2,g2,w2=s.symbols('k2 m2 g2 w2', positive=True)
g,zd,cd,zx,cx,ch,pz,pc=s.symbols('g zd cd zx cx ch pz pc',real=True)
A=m2+g2
checks={}
def exact(name,expr):
    residual=s.simplify(expr)
    assert residual==0,(name,residual)
    checks[name]={'passed':True,'residual':str(residual)}
L=(zd**2+cd**2-zx**2-cx**2-m2*ch**2)/2+g*ch*zd
H=s.expand(pz*zd+pc*cd-L).subs({zd:pz-g*ch,cd:pc})
exact('derived_positive_Hamiltonian',H-((pz-g*ch)**2+pc**2+zx**2+cx**2+m2*ch**2)/2)
exact('nondegenerate_two_velocity_Hessian',s.det(s.hessian(L,(zd,cd)))-1)
P=(w2-k2)*(w2-k2-m2)-g2*w2
wm=k2+A/2-s.sqrt(A**2+4*g2*k2)/2
wp=k2+A/2+s.sqrt(A**2+4*g2*k2)/2
exact('light_root',P.subs(w2,wm))
exact('heavy_root',P.subs(w2,wp))
exact('positive_root_sum',wm+wp-(2*k2+A))
exact('positive_root_product',wm*wp-k2*(k2+m2))
exact('low_k_sound_coefficient',s.diff(wm,k2).subs(k2,0)-m2/A)
exact('low_k_positive_fourth_coefficient',s.diff(wm,k2,2).subs(k2,0)/2-g2**2/A**3)
cs,d4=s.symbols('cs d4',positive=True)
Amatch=(1-cs)**2/d4
exact('match_sound_coefficient',(m2/A).subs({m2:cs*Amatch,g2:(1-cs)*Amatch},simultaneous=True)-cs)
exact('match_fourth_coefficient',(g2**2/A**3).subs({m2:cs*Amatch,g2:(1-cs)*Amatch},simultaneous=True)-d4)
# Principal homogeneous polynomial in omega,k (not in omega^2,k^2).
scale=s.symbols('scale')
exact('actual_degree_four_principal_polynomial',s.expand(P.subs({w2:scale**2*w2,k2:scale**2*k2})).coeff(scale,4)-(w2-k2)**2)

# Removing chi's time derivative makes it an elliptic constraint.
Le=(zd**2-zx**2-(k2+m2)*ch**2)/2+g*ch*zd
chi_solution=s.solve(s.diff(Le,ch),ch)[0]
exact('elliptic_constraint_solution',chi_solution-g*zd/(m2+k2))
reduced=s.simplify(Le.subs(ch,chi_solution))
exact('reduced_positive_inertia',s.diff(reduced,zd,2)-(1+g**2/(m2+k2)))
we=k2*(m2+k2)/(A+k2)
exact('elliptic_dispersion_rearrangement',we-(k2-g2*k2/(A+k2)))
exact('elliptic_low_k_sound',s.diff(we,k2).subs(k2,0)-m2/A)
exact('elliptic_low_k_fourth',s.diff(we,k2,2).subs(k2,0)/2-g2/A**2)
q=s.symbols('q',positive=True)
ve=s.diff(s.sqrt(we.subs(k2,q**2)),q)
exact('elliptic_high_k_group_excess',s.limit(q**2*(ve-1),q,s.oo)-g2/2)
# For compactly supported z0>=0, outside support (A-Delta)^-1 z0>0.
# ztt = Delta z - g2 (A-Delta)^-1 Delta z; outside = -g2*A*(A-Delta)^-1 z0.
ell=s.symbols('ell',nonnegative=True)
exact('elliptic_acceleration_operator_identity',-ell+g2*ell/(A+ell)-(-ell+g2-g2*A/(A+ell)))
M,x=s.symbols('M x',positive=True)
green=s.exp(-M*x)/(2*M)
exact('positive_Yukawa_Green_away_from_source',M**2*green-s.diff(green,x,2))
# Jump of derivative G'(0+)-G'(0-)=-1 supplies unit delta source.
exact('Yukawa_jump_normalization',s.diff(green,x).subs(x,0)-s.Rational(1,2)+1)
result={'checks':checks,'scope':'Constant-coefficient local quadratic two-field system; exact algebra, no full gravitational embedding',
 'conditions':{'healthy_local':'m2>0,g2>0; real g with g^2=g2','matching':'0<cs<1,d4>0'},
 'non_claims':['No one-clock DOF closure','No nonlinear or curved-background proof','No embedding with exact AQUAL/lensing/PPN','No claim that group speed alone proves front causality'],
 'comparison':{'local':'two canonical scalar pairs, positive Hamiltonian, principal metric wave cones','elliptic':'one pair, positive kinetic coefficient, but nonlocal instantaneous acceleration for compact supported data'}}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'all_passed':True}))
