"""Exact mixed-running/matching and inverse-moment checks; no QCD samples."""
import json
import sys
from pathlib import Path
import sympy as s

g,u,t,b0,SQ,mu0=s.symbols('g u t b0 S_Q mu0', positive=True)
pi=s.pi
checks=[]
def check(name,a,b=0):
    d=s.simplify(a-b)
    assert d==0,(name,d)
    checks.append(name)

# Derive the g beta from the source's alpha_s convention.
als=s.symbols('alpha_s',positive=True)
beta01=-2*SQ
beta_als=-2*als*((als/(4*pi))*b0+(als/(4*pi))*(u/(16*pi*pi))*beta01)
beta_g=s.simplify(beta_als.subs(als,g*g/(4*pi))*2*pi/g)
check('alpha_s to canonical g beta',beta_g,
      -b0*g**3/(16*pi*pi)+2*SQ*u*g**3/(16*pi*pi)**2)
beta_y=-2*beta_g/g**3
check('inverse coupling mixed coefficient',s.diff(beta_y,u),-SQ/(64*pi**4))
y0=s.symbols('y0',positive=True)
y=y0+beta_y*t
check('retained inverse coupling solution',s.diff(y,t),beta_y)
g0=s.symbols('g0',positive=True)
ypath=y.subs(y0,1/(g0*g0))
g0dot=-SQ*g0**3*t/(128*pi**4)
check('low-scale coupling boundary tangent',
      s.diff(ypath,u)+s.diff(ypath,g0)*g0dot)
pole=-8*pi*pi/(g0*g0*(b0-SQ*u/(8*pi*pi)))
check('formal pole derivative at zero charge',s.diff(pole,u).subs(u,0),
      -SQ/(b0*b0*g0*g0))
check('mixed term vanishes for no charged quarks',s.diff(beta_y,u).subs(SQ,0))

M,Ml,Al,k=s.symbols('M M_ell A_ell k',nonzero=True)
check('pure scale response removed by proton matching',
      (k*Al-(k*Ml/Ml)*Al)/M**3)
j11,j12,j21,j22=s.symbols('j11 j12 j21 j22')
J=s.Matrix([[j11,j12],[j21,j22]])
a=s.Matrix([[s.symbols('A1'),s.symbols('A2')]])
v=s.Matrix(s.symbols('v1 v2'));p=s.Matrix(s.symbols('p1 p2'))
check('full calibration projector invariant under parameter tangent',
      (a*v-a*J.inv()*(p+J*v)+a*J.inv()*p)[0])

rows=[]
for nf,charges in [(0,[]),(3,[s.Rational(2,3),-s.Rational(1,3),-s.Rational(1,3)]),
                   (4,[s.Rational(2,3),-s.Rational(1,3),-s.Rational(1,3),s.Rational(2,3)]),
                   (5,[s.Rational(2,3),-s.Rational(1,3),-s.Rational(1,3),s.Rational(2,3),-s.Rational(1,3)]),
                   (6,[s.Rational(2,3),-s.Rational(1,3),-s.Rational(1,3),s.Rational(2,3),-s.Rational(1,3),s.Rational(2,3)])]:
    cq=sum(q*q for q in charges)
    rows.append({'active_flavors':nf,'charge_square_sum':str(cq),'beta_s_01':str(-2*cq),
                 'b0':str(11-s.Rational(2,3)*nf)})
check('three-flavor mixed strong coefficient',s.Rational(rows[1]['beta_s_01']),-s.Rational(4,3))

# Independent data-insufficiency counterexample, preserving three moments.
z,B=s.symbols('z B',positive=True)
masses=[s.Integer(k) for k in (1,2,3,4)]
mom=s.Matrix([[1 for _ in masses],[1/x for x in masses],[1/x**2 for x in masses]])
variation=s.Matrix([-1,12,-27,16])
check('moment nullspace',sum((mom*variation)[j]**2 for j in range(3)))
check('independent nullspace reconstruction',
      sum((mom.nullspace()[0]*16-variation)[j]**2 for j in range(4)))
deltaC=sum(variation[j]/(masses[j]+z) for j in range(4))
check('unchanged C zero value',deltaC.subs(z,0))
check('unchanged C zero slope',s.diff(deltaC,z).subs(z,0))
check('unchanged leading UV coefficient',s.limit(z*deltaC,z,s.oo))
delta_integral=sum(variation[j]*(s.log(B+masses[j])-s.log(masses[j])) for j in range(4))
check('finite integral difference',s.limit(delta_integral,B,s.oo),27*s.log(3)-44*s.log(2))
assert 3**27 != 2**44
assert all(40+v>0 and 40-v>0 for v in variation)
checks+=['integral difference nonzero by integer prime powers','both sign variations retain positive baseline']

result={'assertion_tested':'Declared truncated mixed-beta conversion, matching-projector cancellation and three-moment inverse-data counterexample',
        'checks':checks,'check_count':len(checks),'mixed_coefficients':rows,
        'moment_variation':list(variation),'integral_difference':str(27*s.log(3)-44*s.log(2)),
        'physical_R_computed':False,'full_sea_mass_computed':False,'alpha_input_used':False,
        'limits':'No running through strong coupling, no actual QCD spectral interpolation, no sphere/current data'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2,default=str)+'\n')
print(json.dumps({'check_count':len(checks),'status':'all exact assertions pass'}))
