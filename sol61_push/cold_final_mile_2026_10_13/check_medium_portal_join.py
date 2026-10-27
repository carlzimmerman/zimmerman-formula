import json,sys
from fractions import Fraction as F
mchi=F('.93956542194')-F('.0005');mS=F('.001');mn=F('.93956542194');checks=0
q={'chi':1,'S':1,'antiS':-1,'n':0,'gamma':0}
for ins,outs in [(['chi','antiS'],['n','gamma']),(['chi','gamma'],['n','S'])]:
 assert sum(q[x] for x in ins)==sum(q[x] for x in outs);checks+=1
ratio=mchi/mS
assert ratio>900 and F(1)/mS!=F(1)/mchi;checks+=1
for Nchi,NS in [(F(1),F(1)),(F(10),F(1)),(F(1),F(1,1000))]:
 Mq=mchi*(Nchi+NS);Mc=mchi*Nchi+mS*NS
 assert Mq-Mc==(mchi-mS)*NS and Mq>Mc;checks+=1
# A chi -> neutron + same-charge remnant conversion leaves Gauss charge unchanged.
assert mchi*((10-1)+1)==mchi*10;checks+=1
assert mchi*(10-1)+mS<mchi*10;checks+=1
# Opposite charge pair carries rest energy, but zero net Gauss charge.
assert q['chi']+q['antiS']==0 and mchi+mS>0;checks+=1
assert mchi+mS-mn==F('.0005');checks+=1
json.dump(dict(checks=checks,remnant_charge_to_mass_ratio_relative_to_chi=str(ratio),scope='Conditional identification of portal and medium gauge sectors; actual two-current dynamics and material matching not derived'),open(sys.argv[1],'w'),indent=2)
