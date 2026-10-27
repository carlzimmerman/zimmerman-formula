"""Units for the conditional bare-subluminal two-field response bound."""
import json
import math
import sys
from pathlib import Path

out=Path(sys.argv[1]);assert out.is_dir()
c=299792458.;year=365.25*86400.;kpc=3.085677581491367e19
age=10e9*year;fraction=.5;rows=[];checks=[]
for L in (1.,10.,100.):
    light=L*kpc/c
    maximum=(age/light)**2/(2*fraction)
    minimum=math.sqrt(2*fraction*1e47)*light
    passed=abs(math.sqrt(2*fraction*maximum)*light/age-1)<1e-14
    checks.append(dict(name='bound inverse identity L='+str(L),passed=passed));assert passed
    rows.append(dict(inverse_wavenumber_kpc=L,light_time_years=light/year,
        static_enhancement_ceiling_to_reach_half_in_10Gyr=maximum,
        minimum_time_years_to_half_of_enhancement_1e47=minimum/year))
result=dict(hypotheses='Same reciprocal channel and normalization; zero initial perturbations; stable full quadratic system; canonical source kinetic coefficient Z; bare C/Z<=c^2; bound is necessary, not sufficient',
    rows=rows,checks=checks,non_claims=['Contact shift is not automatically this susceptibility enhancement','No universal limit for nonlinear, preloaded or different source-matched states'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
