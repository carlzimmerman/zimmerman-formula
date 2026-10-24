"""Structural coefficient-selection checks; no fitted acceleration inputs."""
import argparse
import json
from pathlib import Path
import sympy as s

p=argparse.ArgumentParser()
p.add_argument('--output',required=True)
p.add_argument('--mutate',action='store_true')
args=p.parse_args()
lam,xi,lam0,xi0,t=s.symbols('lambda xi lambda0 xi0 t',positive=True)
pi=s.pi
bl=18*lam**2/(16*pi**2)
offset=-s.Rational(1,6) if args.mutate else s.Rational(1,6)
bx=6*lam*(xi+offset)/(16*pi**2)
checks=[]
def check(name,expr):
    residual=s.simplify(expr)
    checks.append({'name':name,'residual':str(residual),'passed':residual==0})
invariant=(xi+s.Rational(1,6))/lam**s.Rational(1,3)
check('RG_invariant',s.diff(invariant,lam)*bl+s.diff(invariant,xi)*bx)
ratio=lam/(4*xi)
check('ratio_beta',s.diff(ratio,lam)*bl+s.diff(ratio,xi)*bx-lam**2*(12*xi-1)/(64*pi**2*xi**2))
running_lam=lam0/(1-18*lam0*t/(16*pi**2))
check('lambda_flow',s.diff(running_lam,t)-bl.subs(lam,running_lam))
# Verify the curvature flow using the algebraic variable u=(lambda/lambda0)^(1/3).
u=s.symbols('u',positive=True)
running_xi=(xi0+s.Rational(1,6))*u-s.Rational(1,6)
du=6*lam0*u**4/(16*pi**2)
check('xi_flow',s.diff(running_xi,u)*du-bx.subs({lam:lam0*u**3,xi:running_xi}))
crossing=1/(1+6*xi0)
check('positive_branch_boundary',running_xi.subs(u,crossing))
# Convention reversal: paper xi_E is minus the tracker xi.
xe=s.symbols('xi_E')
paper_beta=6*lam*(xe-s.Rational(1,6))/(16*pi**2)
check('curvature_sign_dictionary',-paper_beta.subs(xe,-xi)-bx)

x,zeta,g,h,scale=s.symbols('x zeta g h scale',positive=True)
U=(lam+2*g*x+h*x*x)/(4*(xi+zeta*x)**2)
xstar=(zeta*lam-g*xi)/(h*xi-zeta*g)
check('angular_stationarity',s.diff(U,x).subs(x,xstar))
vac=(lam*h-g*g)/(4*(h*xi*xi-2*g*xi*zeta+lam*zeta*zeta))
check('vacuum_invariant',U.subs(x,xstar)-vac)
check('angular_curvature',s.diff(U,x,2).subs(x,xstar)-(h*xi-zeta*g)/(2*(xi+zeta*xstar)**3))
rescale={lam:scale*lam,g:(g if args.mutate else scale*g),h:(h if args.mutate else scale*h)}
check('angle_under_common_quartic_rescaling',xstar.subs(rescale,simultaneous=True)-xstar)
check('vacuum_under_common_quartic_rescaling',vac.subs(rescale,simultaneous=True)-scale*vac)

G,c,rm,rv,redshift=s.symbols('G c rho_m rho_v z',positive=True)
R=8*pi*G*(rm+4*rv)/c**2
check('curvature_matter_contamination',R/(32*pi*G*rv/c**2)-(1+rm/(4*rv)))
check('curvature_redshift',R.subs(rm,rm*(1+redshift)**3)/R-(rm*(1+redshift)**3+4*rv)/(rm+4*rv))
d=s.symbols('d',positive=True)
conformal=-(d-2)/(4*(d-1))
check('four_dimensional_conformal_sign',conformal.subs(d,4)+s.Rational(1,6))

result={'mutated':args.mutate,'checks':checks,'passed':sum(v['passed'] for v in checks),
        'total':len(checks),'outcome':'symbolic structural audit, not a mechanism selecting a0',
        'scope':'massless one-loop matter RG truncation; classical scale-invariant two-scalar angular vacuum; homogeneous dust-plus-vacuum trace'}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(0 if all(v['passed'] for v in checks) else 1)
