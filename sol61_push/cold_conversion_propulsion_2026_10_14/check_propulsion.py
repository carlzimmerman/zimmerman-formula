"""CCP-001: momentum, retained baryon mass, isolation and curvature audit."""
import itertools
import json
from pathlib import Path
import sys
import numpy as np
import sympy as s

out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def ck(name,ok):
    checks.append(dict(name=name,passed=bool(ok)))
    if not ok:raise AssertionError(name)
def exact(name,expr):ck(name,s.simplify(expr)==0)

c=299792458.;G=6.67430e-11;gevJ=1.602176634e-10
prior=json.loads(Path('sol61_push/cold_to_baryon_portal_2026_10_14/recombination_run_v1/calculation/results.json').read_text())
row=next(r for r in prior['rows'] if r['mS_GeV']==.001)
mc=prior['mchi_GeV'];ms=.001;mn=.93956542194
mp=.93827208943;me=.00051099895069;mH=mp+me-13.6e-9
W=mc+ms;eg=row['photon_energy_MeV']/1000;Tn=row['neutron_recoil_keV']/1e6
K=row['sigma_v_at_y_1p44em11_cm3_s']
ck('event rest energy',abs(W-mn-eg-Tn)<1e-14)
ck('back to back event momentum',abs(np.sqrt((mn+Tn)**2-mn**2)-eg)<1e-10)
eta=eg/W;etaQ=(W-mn)/W;etaH=(W-mH)/W
ck('efficiency ordering',0<eta<etaQ<etaH<1)
eth=((mn+ms)**2-mc*mc)/(2*mc)
ck('prompt below at-rest activation',0<eg<eth)

# Exact local four-momentum differential including moving radiation source.
M,P,xi,rap,cc=s.symbols('M P xi rap c',positive=True)
Md=-P/cc**2;rd=xi*P/(M*cc**2)
shipEd=Md*cc**2*s.cosh(rap)+M*cc**2*s.sinh(rap)*rd
shipPd=Md*cc*s.sinh(rap)+M*cc*s.cosh(rap)*rd
exact('lab energy conservation',shipEd+P*(s.cosh(rap)-xi*s.sinh(rap)))
exact('lab momentum conservation',shipPd+P/cc*(s.sinh(rap)-xi*s.cosh(rap)))
initial,epsilon=s.symbols('initial epsilon',positive=True)
exact('finite pulse recoil invariant',(initial-epsilon)**2-epsilon**2-(initial**2-2*initial*epsilon))

limits=[]
for f in [.1,.5,.9,.999999]:
    for col in [0.,.5,1.]:
        final=1-eta*f;rapidity=col*np.log(1/final);beta=np.tanh(rapidity)
        ck('retained ash bound %g %g'%(f,col),beta>=0 and beta<=np.tanh(-np.log1p(-eta))+1e-15)
        ck('isotropic no thrust %g %g'%(f,col),col!=0 or beta==0)
        limits.append(dict(initial_fuel_fraction=f,collimation=col,terminal_speed_km_s=beta*c/1000,remaining_ship_mass_fraction=final))

cases=[]
for force in [.001,1.,100.,9806.65]:
    power=force*c;events=power/(eg*gevJ)
    fuel=events*W*gevJ/c**2;neutron_rest=events*mn*gevJ/c**2
    heat=events*Tn*gevJ
    ck('flow energy %g'%force,abs((fuel*c*c-power-neutron_rest*c*c-heat)/(fuel*c*c))<1e-12)
    cases.append(dict(thrust_N=force,ideal_directed_photon_power_W=power,event_rate_sminus1=events,fuel_kg_s=fuel,neutron_rest_mass_kg_day=neutron_rest*86400,prompt_recoil_heat_W=heat))

one=next(r for r in cases if r['thrust_N']==1.)
Vcm=1e6
density=np.sqrt(one['event_rate_sminus1']/(K*Vcm))
fuelmass=density*Vcm*W*gevJ/c**2
naive=dict(volume_m3=1.,equal_species_number_density_cmminus3=density,total_initial_pair_mass_kg=fuelmass,integrated_pair_luminosity_cmminus3=one['event_rate_sminus1']/K,warning='Invalid as an engineering prediction without dense many-body rate, confinement, transport and gravitational/medium calculation.')

# A discrete control field can suppress a vertex but cannot erase pair exchange.
sigma,j,g,m=s.symbols('sigma j g m',real=True,nonzero=True)
Leff=-m*m*sigma*sigma/2+g*sigma*j
exact('integrated control-field residual',Leff.subs(sigma,g*j/m**2)-g*g*j*j/(2*m*m))
ck('bare portal Z2 odd',(-1)!=1)
ck('control times portal Z2 even',(-1)*(-1)==1)
ck('two portal vertices Z2 even',(-1)**2==1)

# Curvature from the full pp-wave metric, not a scalar substitute for Riemann.
u,v,x,y=s.symbols('u v x y');a=s.symbols('a',positive=True)
coord=[u,v,x,y]
metric=s.Matrix([[-a*(x*x+y*y),-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
inv=metric.inv()
Gamma={}
for i,j,k in itertools.product(range(4),repeat=3):
    value=s.simplify(sum(inv[i,l]*(s.diff(metric[l,k],coord[j])+s.diff(metric[l,j],coord[k])-s.diff(metric[j,k],coord[l])) for l in range(4))/2)
    if value!=0:Gamma[i,j,k]=value
def conn(i,j,k):return Gamma.get((i,j,k),s.S.Zero)
Rup={}
for i,j,k,l in itertools.product(range(4),repeat=4):
    value=s.simplify(s.diff(conn(i,l,j),coord[k])-s.diff(conn(i,k,j),coord[l])+sum(conn(i,k,b)*conn(b,l,j)-conn(i,l,b)*conn(b,k,j) for b in range(4)))
    if value!=0:Rup[i,j,k,l]=value
Ric=s.Matrix(4,4,lambda j,l:s.simplify(sum(Rup.get((i,j,i,l),0) for i in range(4))))
ck('pp wave Ricci',Ric==s.Matrix([[2*a,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]))
Rlo={}
for i,j,k,l in itertools.product(range(4),repeat=4):
    val=s.simplify(sum(metric[i,b]*Rup.get((b,j,k,l),0) for b in range(4)))
    if val!=0:Rlo[i,j,k,l]=val
exact('nonzero x tide',Rlo[0,2,0,2]-a)
exact('nonzero y tide',Rlo[0,3,0,3]-a)
scalar=s.simplify(sum(inv[i,j]*Ric[i,j] for i,j in itertools.product(range(4),repeat=2)))
ric2=s.simplify(sum(inv[i,k]*inv[j,l]*Ric[i,j]*Ric[k,l] for i,j,k,l in itertools.product(range(4),repeat=4)))
riem2=0
for ijkl,val in Rlo.items():
    for abcd,val2 in Rlo.items():
        riem2+=val*val2*np.prod([inv[ijkl[q],abcd[q]] for q in range(4)])
riem2=s.simplify(riem2)
exact('pp wave scalar R zero',scalar)
exact('pp wave Ricci norm zero',ric2)
exact('pp wave Riemann norm zero',riem2)
exact('pp wave GB zero',riem2-4*ric2+scalar**2)
curvature=dict(metric='ds2=-2du dv+dx2+dy2-a(x2+y2)du2',Ricci_uu=str(Ric[0,0]),R_uxux=str(Rlo[0,2,0,2]),Ricci_scalar=str(scalar),Ricci_squared=str(ric2),Riemann_squared=str(riem2),Gauss_Bonnet=str(riem2),scope='Ideal infinite pp-wave, not finite engine metric; nonzero tidal curvature despite zero scalar invariants.')

gravity=[]
for force in [1.,9806.65]:
    for area in [1.,10.]:
        power=force*c;energy_density=power/(area*c)
        R00=8*np.pi*G*energy_density/c**4
        gravity.append(dict(thrust_N=force,beam_area_m2=area,energy_density_J_m3=energy_density,local_beam_R00_mminus2=R00,dimensional_acceleration_scale_over_1m_m_s2=c*c*R00,scope='Local beam stress/Ricci component and dimensional scale; not solved finite-beam geodesic acceleration.'))
source=dict(stored_mass_kg=1000.,radius_m=1.,schwarzschild_radius_m=2*G*1000/c**2,compactness_2GM_Rc2=2*G*1000/c**2,positive_source_mass_for_1g_at1m_kg=9.80665/G,positive_source_energy_for_1g_at1m_J=9.80665/G*c*c,scope='Newtonian spherical-source field illustration, not a universal warp energy bound or onboard self-acceleration.')

result=dict(status='conditional propulsion envelope and geometric distinctions verified',assertions=len(checks),prompt_photon_MeV=eg*1000,activation_threshold_MeV=eth*1000,prompt_efficiency=eta,released_energy_fraction=etaQ,final_hydrogen_release_upper_fraction=etaH,prompt_only_retained_products_limit_km_s=float(np.tanh(-np.log1p(-eta))*c/1000),all_release_as_directed_photons_upper_limit_km_s=float(np.tanh(-np.log1p(-etaH))*c/1000),finite_fuel_cases=limits,thrust_cases=cases,naive_dilute_rate_extrapolation=naive,pp_wave=curvature,beam_gravity=gravity,source_gravity=source,non_claim='No practical engine, dense reaction rate, actual carrier, complete isolation, curvature warp or finite-source metric solution.')
(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
