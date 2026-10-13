"""Exact rational spot checks of the one-field potential expansion."""
from fractions import Fraction as F
import json
from pathlib import Path

count = 0
for f in map(F, (1, 10, 100)):
    lam = F(1000001, 500000)/f**2
    m = F(1)
    assert 2*lam*f*f > 4*m*m
    for h in (-2*f, -f, F(0), f/1000, f):
        for y in (F(0), f/100, f):
            direct = lam/4*((f+h)**2+y*y-f*f)**2+m*m*y*y/2
            expanded = lam*f*f*h*h+m*m*y*y/2+lam*f*h*(h*h+y*y)+lam/4*(h*h+y*y)**2
            assert direct == expanded and direct >= 0
            count += 1
out = dict(exact_points=count, all_equal=True, all_nonnegative=True,
           arithmetic="fractions.Fraction over Q",
           non_claim="Finite arithmetic checks supplement the displayed algebraic identity; no dynamics tested",
           preliminary_float_check="A 1e-11 absolute-scaled threshold failed at 1.4552e-11 from cancellation; exact arithmetic used instead")
(Path(__file__).parent/'one_field_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
