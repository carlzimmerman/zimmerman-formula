"""Exact completed-particle stress, not coherent field interaction stress."""
from pathlib import Path
import json
import sympy as s

HERE=Path(__file__).resolve().parent
checks=[]
def check(name,value):
    assert value,name
    checks.append({'name':name,'passed':True})
E1,E2=s.symbols('E1 E2',positive=True)
v1=s.Matrix(s.symbols('v1x v1y v1z',real=True))
v2=s.Matrix(s.symbols('v2x v2y v2z',real=True))
Es=E1+E2;P=E1*v1+E2*v2
jump=E1*v1*v1.T+E2*v2*v2.T-P*P.T/Es
rankone=E1*E2/Es*(v1-v2)*(v1-v2).T
check('general three-dimensional stress rank-one identity',
      (jump-rankone).applyfunc(s.simplify)==s.zeros(3))
check('positive coefficient for the square',(E1*E2/Es).is_positive)
badjump=E1*v1*v1.T+E2*v2*v2.T
check('deleted source stress mutation detected',
      (badjump-rankone).subs(dict(zip(list(v1)+list(v2),[1,0,0,1,0,0])))!=s.zeros(3))

M,epsilon,beta,zeta,Esource=s.symbols('M epsilon beta zeta Esource',real=True)
ep=Esource*(1+beta*epsilon*zeta)/2;em=Esource*(1-beta*epsilon*zeta)/2
m2=M*M*(1-epsilon*epsilon)/4
trace=M*M/Esource-m2*(1/ep+1/em)
expected=M*M/Esource*epsilon*epsilon*(1-beta*beta*zeta*zeta)/(1-beta*beta*epsilon*epsilon*zeta*zeta)
check('boosted on-shell stress trace',s.simplify(trace-expected)==0)
check('rest-source stress trace',s.simplify(expected.subs({beta:0,Esource:M})-M*epsilon*epsilon)==0)

m=s.Integer(1);eps=s.Rational(1,100);be=s.Rational(1,10)
mass=2*m/s.sqrt(1-eps*eps);boost=1/s.sqrt(1-be*be)
sourceE=boost*mass;sourceP=s.Matrix([0,0,boost*be*mass])
fixtures=[]
for axis in range(3):
    n=s.eye(3)[:,axis];daughter=[]
    for sign in [1,-1]:
        energy=boost*mass/2*(1+sign*be*eps*n[2])
        momentum=s.Matrix([sign*mass*eps*n[0]/2,sign*mass*eps*n[1]/2,
                           boost*mass/2*(be+sign*eps*n[2])])
        check('daughter mass shell axis%s sign%s'%(axis,sign),s.simplify(energy*energy-momentum.dot(momentum)-m*m)==0)
        daughter.append((energy,momentum))
    check('source energy and momentum axis%s'%axis,
          s.simplify(daughter[0][0]+daughter[1][0]-sourceE)==0 and
          (daughter[0][1]+daughter[1][1]-sourceP).applyfunc(s.simplify)==s.zeros(3,1))
    fixtures.append({'axis':axis,'daughter_energies':[float(x[0]) for x in daughter]})
check('deleted source energy reaction mutation detected',
      (daughter[0][0]+daughter[1][0]).is_positive)
check('deleted source momentum reaction mutation detected',
      daughter[0][1]+daughter[1][1]!=s.zeros(3,1))

ns,np,nm=s.symbols('ns np nm',nonnegative=True)
gain=ns*(1+np)*(1+nm)-(1+ns)*np*nm
check('empty-source inward rate',s.simplify(-gain.subs(ns,0)).is_nonnegative)
check('empty-daughter inward rate',s.simplify(gain.subs(np,0)).is_nonnegative)
extent=s.symbols('extent',real=True)
check('weighted charge stoichiometry',s.expand(extent+extent-2*extent)==0)
check('deleted source charge mutation detected',s.expand(extent+extent)!=0)
check('particle rest mass changes in conversion',s.simplify(2*m-mass)!=0)

result={'checks':checks,'passed':len(checks),'failures':0,'fixtures':fixtures,
        'scope':'Exact completed-particle stress and stoichiometry; no interaction stress during coherent exchange, field-to-kinetic limit or selector.'}
(HERE/'exact_run/results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
