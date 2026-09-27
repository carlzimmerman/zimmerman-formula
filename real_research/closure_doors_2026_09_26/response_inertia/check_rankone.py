#!/usr/bin/env python3
"""General rank-one mixing: full conserved scalar tidal transfer decomposition."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
checks={}
def exact(name,value):
    v=s.factor(s.simplify(value));checks[name]={'residual':str(v),'passed':v==0};assert v==0,(name,v)
p,f,u,be,dp,du,E,z,B,R,w,r=s.symbols('p f u be dp du E z B R omega r',real=True)
T=2+3*B;kap=2*T/B
L=(-6*dp**2+4*be*dp+2*p**2-4*f*p+E*f**2-z*(u+f)**2
   -B*(3*dp-be)**2-2*r*T*(3*dp-be)*du-3*r*r*T*du**2)
v,dv=s.symbols('v vdot',real=True);Lv=s.expand(L.subs({p:v-r*u,dp:dv-r*du}))
Dr=E*(z-2*r*r)+2*r*r*z+4*r*r-4*r*z
aux=s.solve([s.diff(Lv,zz)for zz in[f,be,u]],[f,be,u],dict=True)[0]
exact('general_rankone_reduction',Lv.subs(aux)-(kap*dv**2-2*z*(2-E)/Dr*v**2))
D=-s.I*w
eq=[s.diff(L,p)-D*s.diff(L,dp)-w*w*R,s.diff(L,f)-R,s.diff(L,be)+D*R,s.diff(L,u)-D*s.diff(L,du)]
eq=[s.expand(ee.subs({dp:D*p,du:D*u}))for ee in eq]
M=s.Matrix([[s.diff(ee,q)for q in[p,f,be,u]]for ee in eq]);src=s.Matrix([-ee.subs({p:0,f:0,be:0,u:0})for ee in eq])
sol=M.inv()*src
tidal=s.factor((-sol[1]-D*sol[2]-w*w*sol[0])/R)
q=s.symbols('q',real=True)
n3=T*r*r*(E-z)
n2=3*T*r*r*(E-z)-2*T*r*r+2*T*r*z-(2*B+1)*E*z
n1=2*T*r*(r-z)+z*(B+E)
n0=-B*z
d1=2*T*Dr;d0=2*B*z*(E-2)
pred=(n3*q**3+n2*q**2+n1*q+n0)/(d1*q+d0)
exact('full_tidal_transfer',tidal-pred.subs(q,w*w))
c2=s.cancel(n3/d1)
c1=s.cancel((n2-d0*c2)/d1)
c0=s.cancel((n1-d0*c1)/d1)
res=s.cancel(n0-d0*c0)
exact('contact_and_pole_division',pred-(c2*q*q+c1*q+c0+res/(d1*q+d0)))
exact('nonlocal_contact_coefficient',c2-r*r*(E-z)/(2*Dr))
exact('retarded_pole_speed',-d0/d1-2*z*(2-E)/(kap*Dr))
exact('zero_mixing_negative_energy_branch',(2*z*(2-E)/Dr).subs(r,0)-2*(2-E)/E)
exact('equal_E_zeta_D_square',Dr.subs(z,E)-(E-2*r)**2)
exact('r_one_limit',Dr.subs(r,1)-(2-z)*(2-E))
exact('static_gain_preserved',sol[1].subs(w,0)/(-R/4)-2/(2-E))
physical_control=s.factor(c2.subs({E:-1,z:s.Rational(1,4),r:1}))
assert physical_control != 0
checks['nonlocal_contact_negative_control']={'E':-1,'zeta':'1/4','r':1,'coefficient':str(physical_control),'passed':True}
result={'result':'general-r same-action wave/contact split; high-x healthy/contact-free compatibility has no regular solution',
        'checks':checks,'Dr':str(Dr),'kinetic':'kappa=2(2+3B)/B','wave_speed_squared':'2 zeta (2-E)/(kappa Dr)',
        'full_transfer_coefficients':{nm:str(vv)for nm,vv in [('n3',n3),('n2',n2),('n1',n1),('n0',n0),('d1',d1),('d0',d0)]},
        'contact_definition':'c2=n3/d1; c1=(n2-d0*c2)/d1; c0=(n1-d0*c1)/d1; residue=n0-d0*c0',
        'dangerous_contact':'c2=r^2(E-zeta)/(2Dr); with compact generator R=-k^2 F gives -c2 omega^4/k^2 F',
        'compatibility':'c2=0 iff r=0 or E=zeta. If E<0: r=0 has negative Veff; E=zeta gives Dr=(E-2r)^2 and negative Veff.',
        'scope':'k nonzero, regular Dr, zeta nonzero, positive physical kappa; only this trace-mixing completion and conserved scalar source',
        'non_claims':['No universal no-go for arbitrary actions/constraint families',
                      'No field-dependent coefficient completion beyond a static frozen background',
                      'No global positive-matter or nonlinear Cauchy-data theorem']}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
