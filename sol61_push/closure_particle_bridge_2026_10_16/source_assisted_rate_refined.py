"""Resolved pole-free source-assisted rate after diagnosing angular error.

The original coarse script and its failed 2-percent gate remain unchanged.
This driver extracts its declared definitions and uses angular refinement
where the separate resolution experiment found the error.
"""
import json
import math
import sys
from pathlib import Path
from scipy.special import kve

out=Path(sys.argv[1]);assert out.is_dir()
path=Path(__file__).with_name('source_assisted_thermal.py')
source=path.read_text();marker='\ncoarse=Thermal('
assert source.count(marker)==1
ns={'__file__':str(path),'__name__':'cpb_source_assisted_definitions'}
exec(compile(source.split(marker,1)[0],str(path),'exec'),ns)
Thermal=ns['Thermal'];m,M,g,lam=ns['m'],ns['M'],ns['g'],ns['lam']
checks=[]
def check(name,value):
    checks.append({'name':name,'passed':bool(value)});assert value,name

# Uniform physical-region amplitude bound from the proved internal gaps.
amplitude_bound=8*abs(g)*((lam+g*g/(4*m*(M+m)))/(M*(M+2*m))+2*lam/(m*m))
def gamma_bound(T):
    ip=m*T*kve(1,m/T)/(4*math.pi**2)
    ix=M*T*kve(1,M/T)/(4*math.pi**2)
    return amplitude_bound**2/(16*math.pi)*ix*ip*ip*math.exp(-(M-2*m)/T)

rows=[]
for ratio in (.003,.01,.03,.1,.3,1.,3.):
    if ratio<=.3:
        dc,df=(24,12,6,12),(40,20,10,20)
    elif ratio==1.:
        dc,df=(40,20,18,36),(40,20,26,52)
    else:
        dc,df=(40,20,26,52),(40,20,34,68)
    coarse,fine=Thermal(*dc),Thermal(*df)
    T=m*ratio
    low,high=coarse.gamma_scaled(T),fine.gamma_scaled(T)
    A,B=ns['scaled_densities'](T)
    nr=ns['K3zero']*B*A*A
    pair=B*B*ns['pair_reverse'](T)
    bound=gamma_bound(T)
    row=dict(Tdark_over_m=ratio,T_dark_GeV=T,gamma3_scaled_GeV4=high,
             coarse_dimensions=dc,fine_dimensions=df,coarse_relative_difference=low/high-1,
             gamma3_over_NR=high/nr,two_conjugate_channels_over_pair_coefficient=2*high/pair,
             analytic_scaled_upper_bound_GeV4=bound,numerical_over_upper_bound=high/bound,
             min_internal_denominator_over_m2=fine.min_safe_denominator)
    rows.append(row);print(json.dumps(row),flush=True)
    check('positive rate '+str(ratio),high>0)
    check('original 2-percent refinement gate '+str(ratio),abs(low/high-1)<.02)
    check('analytic global rate bound '+str(ratio),high<=bound)
    check('physical internal propagator gaps '+str(ratio),fine.min_safe_denominator>=1-1e-8)
check('NR reaction-density normalization',abs(rows[0]['gamma3_over_NR']-1)<.04)

result=dict(verdict='Pole-free source-assisted thermal rate resolved at the stated gate; omitted warm coefficient is comparable to the earlier pair coefficient',
    parameters=ns['p'],threshold_amplitude_GeVminus1=ns['amp0'],
    NR_event_coefficient_GeVminus5=ns['K3zero'],amplitude_global_bound_GeVminus1=amplitude_bound,
    rows=rows,checks=checks,
    non_claims=['Quadrature differences are finite evidence, not rigorous error bars',
               'Narrow external source, vacuum tree, common ideal MB distributions',
               'The other source-assisted crossing has a real source pole and is not subtracted here',
               'No new abundance evolution, full production, galaxy law or global novelty established'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print('All %d refined thermal controls passed.'%len(checks))
