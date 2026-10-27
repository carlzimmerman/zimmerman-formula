import json, sys
from fractions import Fraction as F
n=0
for x in [F(1,100),F(1,10),F(1,2),F(9,10),F(99,100)]:
    for f in [F(0),F(1,10),F(1,2),F(9,10),F(1)]:
        u=x; gn=u*u/(1-u)
        actual=(f*u)**2/(1-f*u)/gn
        formula=f*f*(1-x)/(1-f*x)
        assert actual==formula
        assert 0<=actual<=f*f
        assert actual==1 if f==1 else actual<1
        n+=3
# A time dependent density proportional to the canonical profile requires a source.
# Continuity with zero velocity is rho_dot=S_rho, not zero.
f=F(1,2); x=F(1,2)
json.dump(dict(checks=n,half_formed_example=dict(u_over_a0=str(x),outward_over_gN=str(f*f*(1-x)/(1-f*x)),net_inward_over_gN=str(1-f*f*(1-x)/(1-f*x))),scope='Exact rational controls; universal inequality proved separately in FORMATION_FORCE_RESULT.txt'),open(sys.argv[1],'w'),indent=2)
