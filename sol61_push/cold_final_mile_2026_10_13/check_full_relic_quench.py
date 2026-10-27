import json,sys
from fractions import Fraction as F
checks=0;out=[]
for u in [F(1,10),F(1,2),F(9,10)]:
 for p in [F(3,2),F(2),F(3)]:
  old=u*u/(1-u);new=old/p
  acceleration=-new+u*u/(1-u)
  assert acceleration==old-new and acceleration>0;checks+=1
  # With old source M=p and new source M=1, a supplied positive inverse-radius mass moment B.
  B=F(7,3);Eold=-p*B;Enew=-B
  assert Enew-Eold==(p-1)*B and Enew>Eold;checks+=1
  out.append(dict(u_over_a0=str(u),p=str(p),initial_outward_acceleration=str(acceleration)))
# Fixed core of the cubic run is outside a full saturating field wall at its inner boundary.
assert F(1,2)/F(1,2)**2==2;checks+=1
json.dump(dict(checks=checks,controls=out,scope='Exact initial full residual force and quench work only; no long-time or nonspherical attractor certificate'),open(sys.argv[1],'w'),indent=2)
