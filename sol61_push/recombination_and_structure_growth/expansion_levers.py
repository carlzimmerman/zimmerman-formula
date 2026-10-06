"""Fixed-physical-density flat-FRW sensitivities, not a recombination solver.
Writes only the requested --output path. No project scripts imported.
"""
import argparse
import json
from pathlib import Path
import mpmath as mp
import numpy as np
from scipy.integrate import quad

mp.mp.dps = 50
ap = argparse.ArgumentParser()
ap.add_argument('--output', required=True)
args = ap.parse_args()
checks = {}
def check(name, truth):
    checks[name] = bool(truth)
    print(('PASS ' if truth else 'FAIL ') + name)

c = 299792458.0
G = 6.67430e-11
kb = 1.380649e-23
hbar = 1.054571817e-34
Mpc = 3.085677581491367e22
H100 = 100000.0 / Mpc
T0 = 2.7255
wb, wc, h = 0.02237, 0.1200, 0.6736
wg = np.pi**2 * (kb*T0)**4/(15*hbar**3*c**5)/(3*H100**2/(8*np.pi*G))
wr = wg*(1+(7/8)*(4/11)**(4/3)*3.046)
wm = wb+wc
wv = h*h-wm-wr
astar = 1/1091.0
Rcoef = 3*wb/(4*wg)
def denom(a, vacuum=wv):
    return wr+wm*a+vacuum*a**4
def weight(a, acoustic=False, vacuum=wv):
    out = 1/np.sqrt(denom(a,vacuum))
    return out/np.sqrt(3*(1+Rcoef*a)) if acoustic else out
def integral(acoustic=False, vacuum=wv):
    bounds = (0,astar) if acoustic else (astar,1)
    return quad(lambda a:weight(a,acoustic,vacuum),*bounds,epsabs=1e-10,epsrel=3e-12)[0]
rs = c/H100/Mpc*integral(True)
dm = c/H100/Mpc*integral(False)
derivs = {}
for name,acoustic in [('rs',True),('DM',False)]:
    bounds = (0,astar) if acoustic else (astar,1)
    num = quad(lambda a:weight(a,acoustic)*wv*a**4/denom(a),*bounds,epsabs=1e-15,epsrel=3e-12)[0]
    derivs[name] = -num/(2*integral(acoustic))
fstar = wv*astar**4/denom(astar)
check('local_vacuum_fraction_below_two_billionths',0<fstar<2e-9)
check('sound_horizon_derivative_bound',0 < -derivs['rs'] < fstar/2)
check('late_distance_vacuum_sensitivity',0.03 < -derivs['DM'] < .2)

# Orthogonal arbitrary-precision differentiation of the complete integrals.
wrm,wmm,wvm,rm,asm = map(lambda x:mp.mpf(str(x)),(wr,wm,wv,Rcoef,astar))
def imp(vacuum,acoustic):
    def fn(a):
        out=1/mp.sqrt(wrm+wmm*a+vacuum*a**4)
        return out/mp.sqrt(3*(1+rm*a)) if acoustic else out
    return mp.quad(fn,[0,asm]) if acoustic else mp.quad(fn,[asm,mp.mpf('.01'),mp.mpf('.1'),1])
high_precision = {}
for name,acoustic in [('rs',True),('DM',False)]:
    value=imp(wvm,acoustic)
    slope=wvm*mp.diff(lambda v:imp(v,acoustic),wvm)/value
    high_precision[name]={'dimensionless_integral':str(value),'log_vacuum_derivative':str(slope)}
    check(name+'_independent_50_digit_derivative',abs(float(slope)-derivs[name])<max(abs(derivs[name])*2e-9,1e-20))
    check(name+'_independent_quadrature',abs(float(value)/integral(acoustic)-1)<1e-10)

variants=[]
for fac in (0,0.5,1,2):
    rsratio=imp(wvm*fac,True)/imp(wvm,True)
    dmratio=imp(wvm*fac,False)/imp(wvm,False)
    variants.append({'vacuum_multiplier':fac,'Hstar_ratio':float(mp.sqrt((wrm+wmm*asm+wvm*fac*asm**4)/(wrm+wmm*asm+wvm*asm**4))),
                     'rs_ratio':str(rsratio),'DM_ratio':str(dmratio),'theta_ratio':str(rsratio/dmratio),
                     'implied_H0_km_s_Mpc':100*np.sqrt(wr+wm+wv*fac)})
check('zero_vacuum_leaves_early_ruler_nearly_unchanged',abs(float(variants[0]['rs_ratio'])-1)<1e-9)
check('zero_vacuum_changes_late_distance',float(variants[0]['DM_ratio'])>1.05)
check('acoustic_ratio_log_derivative',derivs['rs']-derivs['DM']>0)
# Added smooth early energy is different from present constant vacuum.
early=[{'early_total_fraction':f,'H_over_baseline':1/np.sqrt(1-f)} for f in (.01,.05,.1)]
check('ten_percent_early_energy_is_not_negligible',early[-1]['H_over_baseline']-1>.05)
result={'checks':checks,'model':'flat GR background, baryons+CDM, massless neutrino radiation, constant vacuum; fixed zstar=1090 and physical matter/radiation densities; H0 changes when vacuum changes',
        'inputs':{'wb':wb,'wc':wc,'h':h,'T0_K':T0,'Neff':3.046,'zstar_fixed':1090},
        'derived':{'wg':wg,'wr':wr,'wm':wm,'wv':wv,'equality_z':wm/wr-1,'local_vacuum_fraction':fstar,'dlnHstar_dlnwv':fstar/2,
                   'rs_Mpc':rs,'DM_Mpc':dm,'theta':rs/dm,'log_derivatives':derivs,'dln_theta_dlnwv':derivs['rs']-derivs['DM']},
        'independent_high_precision':high_precision,'vacuum_variants':variants,'early_energy_control':early,
        'non_claims':['No solved ionization history or changed zstar','No Planck likelihood or exact neutrino-mass treatment','No dark-sector microphysical identity','No proof a modified action shares this Friedmann law','Early control only local H, not recombination solution']}
out=Path(args.output)
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result['derived'],indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
