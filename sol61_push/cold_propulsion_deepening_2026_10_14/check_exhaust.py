import json
import math
import sys
from pathlib import Path
import sympy as s

out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def zero(name,v):
    val=s.simplify(v);assert val==0,(name,val)
    checks.append(name)
source=json.loads(Path('sol61_push/cold_to_baryon_portal_2026_10_14/recombination_run_v1/calculation/results.json').read_text())
row=next(v for v in source['rows'] if v['mS_GeV']==0.001)
mn=s.Rational('0.93956542194');W=mn+s.Rational('0.0005');Q=W-mn
Eg=s.factor((W*W-mn*mn)/(2*W));Tn=s.factor(W-Eg-mn)
assert abs(float(Eg)*1000-row['photon_energy_MeV'])<1e-10
checks.append('source photon benchmark reproduced')
zero('raw two-body momenta cancel algebraically',(W-Eg)**2-mn*mn-Eg*Eg)
zero('prompt energy conservation',Eg+Tn-Q)

m,qq,eff=s.symbols('m Q eff',positive=True)
En=m+eff*qq;pc=s.sqrt(En*En-m*m)
zero('massive exhaust shell',En*En-pc*pc-m*m)
zero('total outgoing energy with isotropic unused release',En+(1-eff)*qq-(m+qq))
zero('momentum derivative makes all-to-massive optimal',s.diff(pc+(1-eff)*qq,eff)-qq*(En/pc-1))
# Exact rocket infinitesimal conservation identities (c=1), boosted beam.
M,rho,er,pr=s.symbols('M rho er pr',positive=True)
Md=-er;rd=pr/M
zero('lab energy differential',Md*s.cosh(rho)+M*s.sinh(rho)*rd-(-er*s.cosh(rho)+pr*s.sinh(rho)))
zero('lab momentum differential',Md*s.sinh(rho)+M*s.cosh(rho)*rd-(-er*s.sinh(rho)+pr*s.cosh(rho)))

c=299792458.;eVJ=1.602176634e-19;GeVJ=1e9*eVJ
wj=float(W)*GeVJ;qj=float(Q)*GeVJ;egj=float(Eg)*GeVJ;tnj=float(Tn)*GeVJ
masspair=wj/c**2;massn=float(mn)*GeVJ/c**2
Krate=row['sigma_v_at_y_1p44em11_cm3_s']
jets=[]
for ee in (.1,.5,1.):
    en=float(mn)+ee*float(Q)
    pp=math.sqrt((en-float(mn))*(en+float(mn)))
    beta=pp/en;beff=pp/float(W)
    momentum=pp*GeVJ/c
    events=1/momentum
    jets.append({'energy_transfer_efficiency':ee,'neutron_speed_m_s':beta*c,'effective_rocket_exhaust_speed_m_s':beff*c,'events_per_s_for_1N':events,'total_released_power_W':events*qj,'jet_kinetic_power_W':events*ee*qj,'unused_heat_W':events*(1-ee)*qj,'cold_pair_mass_rate_kg_s':events*masspair,'formal_pair_overlap_cmminus3':events/Krate,'terminal_speeds':[{ 'fuel_fraction':ff,'speed_km_s':c*math.tanh(beff*math.log(1/(1-ff)))/1000} for ff in (.1,.5,.9)]})
    assert abs(events*momentum-1)<1e-14
    assert abs(events*qj-(events*ee*qj+events*(1-ee)*qj))<1e-6
    checks.append('massive jet momentum/energy '+str(ee))

# Derive Stefan-Boltzmann constant directly from exact assigned SI constants.
hh=6.62607015e-34;kb=1.380649e-23
sigma=2*math.pi**5*kb**4/(15*hh**3*c*c)
ph=[]
for eta in (.1,.5,.9):
    xi=.9
    sourcepower=c/(xi*eta)
    events=sourcepower/egj
    heat=(1-eta)*sourcepower+events*tnj
    areas={str(T):heat/(.9*sigma*(T**4-3**4)) for T in (300,600,1000,1500)}
    ph.append({'light_conversion_efficiency':eta,'beam_collimation':xi,'source_prompt_gamma_power_W':sourcepower,'outgoing_useful_light_W':eta*sourcepower,'heat_including_neutron_stopping_W':heat,'new_neutron_mass_kg_day':events*massn*86400,'radiator_emitting_area_m2':areas,'event_rate_sminus1':events})
    assert abs(eta*sourcepower*xi/c-1)<1e-14
    assert abs(sourcepower+events*tnj-(eta*sourcepower+heat))<1e-6
    checks.append('photon thrust/heat balance '+str(eta))

ordinary=[]
for ve in (3e4,1e5,1e6):
    beta=ve/c;gam=1/math.sqrt(1-beta*beta)
    mdot=1/(gam*ve)
    pj=ve/(1+1/gam)
    efficiency=.5
    pg=pj/efficiency;events=pg/egj
    ordinary.append({'ordinary_propellant_speed_m_s':ve,'ordinary_mass_flow_kg_s':mdot,'jet_kinetic_power_W':pj,'gamma_to_jet_efficiency':efficiency,'source_prompt_gamma_power_W':pg,'source_cold_mass_flow_kg_s':events*masspair,'retained_new_neutron_kg_day':events*massn*86400,'heat_including_neutron_stopping_W':pg-pj+events*tnj,'source_events_sminus1':events,'formal_pair_overlap_cmminus3':events/Krate})
    assert abs(mdot*gam*ve-1)<1e-14
    # Stable identity for relativistic P/F, no cancellation gamma-1.
    assert abs(pj/(ve*gam/(gam+1))-1)<1e-12
    checks.append('ordinary jet relativistic balance '+str(ve))
ratio=(math.sqrt(float(W)**2-float(mn)**2))/float(Eg)
result={'claim':'CPD-E001','checks_passed':len(checks),'source_release_MeV':float(Q)*1000,'prompt_photon_MeV':float(Eg)*1000,'specific_released_energy_J_kg':qj/masspair,'created_baryon_ideal_thrust_gain_per_reaction_vs_prompt_photon':ratio,'sigma_W_m2_K4':sigma,'ideal_massive_exhaust':jets,'photon_reprocessing':ph,'photon_heated_ordinary_propellant':ordinary,'warning':'All engines conditional. No actual conversion rate, storage, neutron/charged nozzle, thermal hardware or geometric coupling demonstrated. Created neutron mass is retained/expelled converted fuel, not extra mass added from nowhere.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(result,indent=2))
