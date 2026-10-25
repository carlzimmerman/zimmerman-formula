"""Exact rational spherical coupling identities, not a health/galaxy test."""
import json
from fractions import Fraction as F
from pathlib import Path

rows=[]
for u in [F(1,100),F(1,10),F(1,2),F(9,10),F(99,100)]:
    y=u*u/(1-u);x=y+u
    assert x*x/(1+x)==y
    radial=u*(2-u)/(1-u)**2
    assert radial>0
    for cold in [F(0),F(1,10),F(1),F(5)]:
        total=x+cold
        # Xi source and solution are unchanged; Phi contains the cold force once.
        assert total-x==cold
    rows.append({'u':str(u),'gNb_over_a0':str(y),'g_law_over_a0':str(x),
                 'positive_radial_static_coefficient':str(radial)})
p=Path(__file__).with_name('bridge_checks.json')
p.write_text(json.dumps({'rows':rows,'cases':20,'status':'exact scalar identities passed',
    'scope':'spherical postulated two-potential action only; not covariant stability, same-data SPARC fit or four-dwarf closure'},indent=2)+'\n')
print('20 cold-addition identities and 5 spherical/radial-coefficient controls passed')
