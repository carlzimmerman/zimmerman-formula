"""Bounded new audit: cold + stellar two-Plummer transport bound, no simulation.

Usage: python3 sol61_push/cold_advance_2026_10_18/transport/check_transport_two_plummer.py RESULT
All old evidence is read only. The report states the conditional reduction.
"""
import json
import math
import sys
from pathlib import Path

BASE = Path('sol61_push/cold_advance_2026_10_18/transport')
DWARF = Path('sol61_push/cold_final_mile_2026_10_13/run_077/results.json')
FORMATION = Path('argon_push/ARGON10_four_gaps_2026-10-16/argon10_formation_results.json')
QUANTUM = Path('argon_push/ARGON10_four_gaps_2026-10-16/argon10_quantum_results.json')
G = 6.67430e-8  # cm^3 / g / s^2, chosen numerical constant
MSUN = 1.98847e33  # g
PC = 3.0856775814913673e18  # cm
YEAR = 31557600.0  # s, Julian year
T = 10e9 * YEAR  # chosen comparison age, not measured halo age
HBARC = 197.3269804e-13  # MeV cm, same value as ARGON10
MEV_G = 1.78266192e-27  # g, same value as ARGON10
checks = []


def ck(name, ok):
    checks.append({'name': name, 'pass': bool(ok)})
    if not ok:
        raise AssertionError(name)


def close(a, b, rtol=2e-12):
    return abs(a-b) <= rtol * max(abs(a), abs(b), 1e-300)


dwarfs = json.loads(DWARF.read_text())['dwarfs']
formation = json.loads(FORMATION.read_text())
quantum = json.loads(QUANTUM.read_text())
q100 = next(x for x in quantum['Q2'] if x['M'] == 100 and x['eps'] == 1)
eps_cap = min(1/q100['Delta_net'], 1/q100['Delta_m'])
source_f3 = next(x for x in formation['F2']['F3_posthoc'] if x['M'] == 100)
ck('derive source leading-log sensitivity cap', close(eps_cap, source_f3['eps_max']))
lumps1 = {x['s']: x for x in formation['F2']['lump'] if x['eps'] == 1}
kappa_cap = lumps1[.1]['cm2g_1MeV'] * eps_cap
ck('natural conversion agrees with independent source value', close(lumps1[.1]['S']*HBARC**2/MEV_G, lumps1[.1]['cm2g_1MeV']))
ck('one cm2/g equals 0.1 m2/kg', close((.01**2)/.001, .1))

micro = []
for s in [.1, .5]:
    src = lumps1[s]
    for eps in [1., .001, 1e-6, eps_cap]:
        Q = src['Q']/eps
        Rcm = src['R']*HBARC
        mass_g = Q*MEV_G
        kappa = 4*math.pi*Rcm**2/mass_g
        ck('fragment geometry conversion '+str((s,eps)), close(kappa, src['cm2g_1MeV']*eps))
        micro.append({'s':s,'epsilon':eps,'mh_MeV':1.,'Q_free_charge_mass_convention':Q,
            'radius_cm':Rcm,'mass_g_using_mhQ':mass_g,'geometric_kappa_cm2g':kappa,
            'kR_at_10kms_equal_mass_cm_momentum':.5*Q*src['R']*(10/299792.458)})

out = []
for x in dwarfs:
    name = x['name']
    M = 53.64*x['Mb_Msun']*MSUN
    Mb = x['Mb_Msun']*MSUN
    R = x['r12_pc']*PC
    a_star = .75*R  # exact source Plummer convention yields Mstar(<r12)=.512Mb
    b = 10*R
    rho0 = 3*M/(4*math.pi*b**3)
    vbound = math.sqrt(8*G*(M/b+Mb/a_star))
    coeff = rho0*vbound*T  # Lambda_max per cm2/g
    # Independent unit implementation in Msun, pc, km/s, Gyr.
    G_pc = G*MSUN/PC/1e10
    vbound_kms = math.sqrt(8*G_pc*((M/MSUN)/(b/PC)+(Mb/MSUN)/(a_star/PC)))
    rho_msunpc3 = 3*(M/MSUN)/(4*math.pi*(b/PC)**3)
    coeff_units = rho_msunpc3*(MSUN/PC**3)*vbound_kms*1e5*T
    ck(name+' independent unit path', close(coeff, coeff_units))
    ck(name+' source stellar enclosed fraction',close((R/a_star)**3/(1+(R/a_star)**2)**1.5,.512))
    ck(name+' stellar central potential ratio',close((Mb/a_star)/(M/b),(10/.75)/53.64))
    ck(name+' Plummer density at b is rho0/2^2.5', close((3*M*b*b/(4*math.pi*(b*b+b*b)**2.5))/rho0, 2**(-2.5)))
    # Analytic derivatives: dM/dr = 4pi r2 rho and dPhi/dr=GM(r)/r2.
    for y in [.1,1.,10.]:
        r = y*b
        menc = M*r**3/(r*r+b*b)**1.5
        dMdr = 3*M*b*b*r*r/(r*r+b*b)**2.5
        rho = 3*M*b*b/(4*math.pi*(r*r+b*b)**2.5)
        ck(name+' Poisson/mass derivative y='+str(y), close(dMdr,4*math.pi*r*r*rho))
        ck(name+' force/mass identity y='+str(y), close(G*M*r/(r*r+b*b)**1.5,G*menc/(r*r)))
    uniform_vrel = 4/math.sqrt(math.pi)*math.sqrt(G*M/(5*b))
    def exposure(scale,kap):
        return kap*3*M/(4*math.pi*scale**3)*math.sqrt(8*G*(M/scale+Mb/a_star))*T
    def b_for_exposure(kap,needed):
        lo,hi=b*1e-8,b*1e8
        for _ in range(180):
            mid=math.sqrt(lo*hi)
            if exposure(mid,kap)>needed:lo=mid
            else:hi=mid
        return math.sqrt(lo*hi)
    kappa_cases = []
    for label,kappa in [('source_sensitivity_cap_1MeV_s0.1',kappa_cap),('chosen_reference_0.708',.708),('chosen_reference_10',10.)]:
        lam = kappa*coeff
        bmax = b_for_exposure(kappa,1.)
        b10 = b_for_exposure(kappa,10.)
        b100 = b_for_exposure(kappa,100.)
        for needed,scale in [(1,bmax),(10,b10),(100,b100)]:
            ck(name+' radius inversion '+label+str(needed),close(exposure(scale,kappa),needed))
            ck(name+' radius monotonicity '+label+str(needed),exposure(scale*.99,kappa)>needed>exposure(scale*1.01,kappa))
        kappa_cases.append({'label':label,'kappa_cm2g':kappa,'Lambda_max_10Gyr':lam,
            'ever_collided_probability_upper_bound_if_fixed_background':-math.expm1(-lam),
            'radial_tau_upper':kappa*rho0*b,'minimum_mean_free_path_pc':1/(kappa*rho0)/PC,
            'bmax_pc_for_Lambda_max_at_least_one':bmax/PC,
            'bmax_pc_for_Lambda_max_at_least_ten':b10/PC,
            'bmax_pc_for_Lambda_max_at_least_one_hundred':b100/PC})
    # Current target-state aperture mean density, with stellar sigma only a proxy.
    targetM = x['cold_required_in_r12_over_Mb']*x['Mb_Msun']*MSUN
    targetrho = 3*targetM/(4*math.pi*R**3)
    targetv = 4/math.sqrt(math.pi)*x['sigma_obs_kms']*1e5
    targetN = targetrho*targetv*T*kappa_cap
    out.append({'name':name,'fixed_stock_Msun':M/MSUN,'r12_pc':R/PC,
        'target_cold_fraction_eta':x['fraction_all_cold_needed_inside_r12'],
        'Plummer_start_b_pc':b/PC,'stellar_Plummer_scale_pc':a_star/PC,
        'stellar_central_potential_over_cold_central_potential':(Mb/a_star)/(M/b),
        'Plummer_start_aperture_fraction':1/101**1.5,
        'Plummer_central_density_Msun_pc3':rho_msunpc3,'Plummer_pair_speed_upper_kms':vbound/1e5,
        'kappa_min_cm2g_for_Lambda_max_at_least_one':1/coeff,
        'kappa_cases':kappa_cases,
        'uniform_global_virial_estimate':{'vrel_kms':uniform_vrel/1e5,
            'kappa_one_collision_cm2g':1/(rho0*uniform_vrel*T),
            'N_at_protected_kappa':rho0*uniform_vrel*T*kappa_cap},
        'target_state_Maxwell_proxy':{'mean_cold_density_Msun_pc3':targetrho/(MSUN/PC**3),
            'assumed_carrier_1D_sigma_equals_stellar_sigma_kms':x['sigma_obs_kms'],
            'kappa_one_collision_cm2g':1/(targetrho*targetv*T),
            'N_10Gyr_at_protected_kappa':targetN}})

by = {x['name']:x for x in out}
for name in ['Draco','Ursa Minor','Canes Venatici I','Sextans']:
    x=by[name]
    ck(name+' chosen kappa10 has Lambda max below one at10r12',x['kappa_cases'][-1]['Lambda_max_10Gyr']<1)
    ck(name+' processed fraction below required transfer under direct collision premise',
        x['kappa_cases'][-1]['ever_collided_probability_upper_bound_if_fixed_background']<x['target_cold_fraction_eta']-x['Plummer_start_aperture_fraction'])
ck('radius scaling coefficient exponent',close((2**1.5)**(2/7),2**(3/7)))
ck('source target population covers exactly eleven',len(out)==11 and len(by)==11)

res={'claim_id':'CE-ADV-TRANSPORT-TWO-PLUMMER-2026-10-18','outcome':'implementation and finite assertion verified in stated conditional benchmark',
 'comparison_age_Gyr':10.,'constants_cgs':{'G':G,'Msun':MSUN,'pc':PC,'Julian_year_s':YEAR,'hbarc_MeV_cm':HBARC,'MeV_g':MEV_G},
 'source_leading_log_sensitivity_epsilon_cap_M100':eps_cap,'geometric_kappa_at_cap_s0.1_mh1MeV':kappa_cap,
 'free_same_charge_kappa_at_cap_mh1MeV':formation['F2']['gas'][0]['cm2g_1MeV']*eps_cap**2,
 'fragment_geometry':micro,'dwarfs':out,'checks':checks,'n_checks':len(checks),'all_pass':all(x['pass'] for x in checks),
 'scope':'Newtonian fixed bound TWO-Plummer cold + stellar potential; stellar scale .75r12 and cold stock53.64Mb. Monodisperse classical elastic transport with kappa=geometric sigma/m; 10Gyr comparison age. Source fragment sizes/sensitivity cap are estimates, not rerun. Lambda upper is a conditional collision exposure bound, not collapse time or a no-go for evolving self-consistent halos. Actual transport, inelasticity, fragment spectrum, halo history and modified gravity remain uncomputed. The uniform global-virial estimate remains the separately labeled cold-only auxiliary.'}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'n_checks':len(checks),'all_pass':res['all_pass'],'epsilon_cap':eps_cap,'kappa_cap':kappa_cap,
    'dense_dwarf_kappa_min':{k:by[k]['kappa_min_cm2g_for_Lambda_max_at_least_one'] for k in ['Draco','Ursa Minor','Canes Venatici I','Sextans']}},indent=2))
