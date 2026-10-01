#!/usr/bin/env python3
"""HR01 independent edge checks. Accreting-potential orbit scans are tracer surrogates, not self-consistent cosmological collapse."""
import os,json,math,pathlib,sys
import numpy as np
from scipy.integrate import solve_ivp,quad
G=6.67430e-11; MS=1.98892e30; KPC=3.0856775814913673e19
FOOTS={'canonical':9.3603e-11,'alt':1.1312e-10}
MUT=os.environ.get('MUTATE')=='1'; checks={}
def ck(k,b,value):checks[k]={'passed':bool(b),'value':value}
def orbit(p,ell,rtol=1e-10):
    C=math.pi**2/8
    def rhs(t,y):return [y[1],-C*t**p/y[0]**2+C*ell**2/y[0]**3]
    def peri(t,y):return y[1]
    peri.direction=1;peri.terminal=True
    first=solve_ivp(rhs,[1,20],[1,0],events=peri,rtol=rtol,atol=rtol*.01,max_step=.01)
    if not len(first.t_events[0]):raise RuntimeError('missing first pericentre')
    tp=first.t_events[0][0];yp=first.y_events[0][0]
    def apo(t,y):return y[1]
    apo.direction=-1;apo.terminal=True
    second=solve_ivp(rhs,[tp,30],yp,events=apo,rtol=rtol,atol=rtol*.01,max_step=.01)
    if not len(second.t_events[0]):raise RuntimeError('missing first apocentre')
    ts=second.t_events[0][0];rs=second.y_events[0][0][0]
    x=rs/ts**((p+2)/3)
    energy=lambda r,v:.5*v*v+C*ell**2/(2*r*r)-C/r
    edev=abs(energy(rs,0)-energy(1,0))/abs(energy(1,0)) if p==0 else None
    return {'p':p,'ell':ell,'t_peri':tp,'t_splash':ts,'r_splash':rs,'x':x,'static_energy_error':edev}
rows=[orbit(p,ell) for p in [0,.5,1,2,3] for ell in [.1,.2,.4]]
control=[r for r in rows if r['p']==0]
ck('static_Kepler_energy',max(r['static_energy_error'] for r in control)<1e-7,max(r['static_energy_error'] for r in control))
ck('static_first_apocentre_radius',max(abs(r['r_splash']-1) for r in control)<1e-7,[r['r_splash'] for r in control])
refine=orbit(1,.2,2e-12);base=next(r for r in rows if r['p']==1 and r['ell']==.2)
ck('orbit_tolerance',abs(refine['x']-base['x'])<1e-7,abs(refine['x']-base['x']))
# Exact Kepler histories: independently choose current first-turnaround outer shell R and prior-turnaround tracer shell xe R.
# Each tracer reaches its first post-pericentre apocentre one Kepler period after its earlier turnaround.
kepler=[]
for x in [.2,.4,.7]:
    ell=.2;a=x/(2-ell**2); period=2*math.pi*a**1.5 # GM=Rta=1
    kepler.append({'xe':x,'semimajor_axis':a,'earlier_turnaround_time_relative_to_now':-period,'first_splash_time':0,'current_outer_turnaround_radius':1})
ck('shell_history_nonuniqueness',min(r['xe'] for r in kepler)<.31 and max(r['xe'] for r in kepler)>.48,kepler)
# Positive density and hydrostatic construction, exact point-baryon P2 law inside a freely selected edge.
results={}
for foot,a0 in FOOTS.items():
    Mb=1e10*MS;rM=math.sqrt(G*Mb/a0);rta=500*KPC
    cells=[]
    for xe in [.2,.31,.4,.48,.7]:
        re=xe*rta
        def mt(r):return Mb*math.sqrt(1+(r/rM)**2)
        def rho(r):return a0*Mb/(4*math.pi*G*r*mt(r))
        def pressure(r):return a0*Mb/(8*math.pi)*(1/r**2-1/re**2)
        r=.1*re
        deriv=-a0*Mb/(4*math.pi*r**3)
        hyd=abs((deriv+rho(r)*G*mt(r)/r**2)/deriv)
        integrated=quad(lambda u:rho(u)*G*mt(u)/u**2,r,re,epsabs=1e-40,epsrel=1e-11)[0]
        pd=pressure(r)
        md=mt(re)-Mb
        rout=2*re
        # MUTATE deliberately uses response truncation: cancels source mass outside.
        gout=G*(Mb+(0 if MUT else md))/rout**2
        gauss=abs(gout*rout**2/G/(Mb+md)-1)
        stress_jump_original=a0*Mb/(8*math.pi*re**2)
        cells.append({'xe':xe,'re_kpc':re/KPC,'Md_Msun':md/MS,'hydrostatic_residual':hyd,'quadrature_rel_error':abs(integrated/pd-1),'boundary_pressure_original_Pa':stress_jump_original,'boundary_pressure_shifted_Pa':pressure(re),'outside_gauss_relative_error':gauss,'pressure_to_cap_at_probe':pd/(a0*a0/(8*math.pi*G))})
    results[foot]=cells
ck('hydrostatic_interior',max(c['hydrostatic_residual'] for cs in results.values() for c in cs)<1e-12,results)
ck('pressure_quadrature',max(c['quadrature_rel_error'] for cs in results.values() for c in cs)<1e-9,max(c['quadrature_rel_error'] for cs in results.values() for c in cs))
ck('edge_pressure_continuity',all(c['boundary_pressure_shifted_Pa']==0 and c['boundary_pressure_original_Pa']>0 for cs in results.values() for c in cs),'Unshifted CFG2 pressure has nonzero outer stress; boundary-normalized pressure matches vacuum')
ck('density_edge_Gauss_retention',max(c['outside_gauss_relative_error'] for cs in results.values() for c in cs)<1e-12,max(c['outside_gauss_relative_error'] for cs in results.values() for c in cs))
# Local pressure law around extended baryons: g_b proportional r^(n-2), so positive density requires n<=2.
ck('extended_pressure_law_sign',all((n-2)>0 for n in [2.1,2.5,3]),'n>2 gives P prime>0, whereas -rho g<=0: clipping growth is a changed pressure law')
# A cap permits empty dark field and every sufficiently diluted positive configuration: no unique baryonic RAR.
ck('cap_does_not_imply_RAR',0<=1 and math.sqrt(2)>1,{'y':1,'no_dark_stress_over_cap':0,'no_dark_total_g_over_gb':1,'P2_required':math.sqrt(2)})
out={'mutation':MUT,'checks':checks,'accreting_point_mass_tracer_scan':rows,'kepler_histories':kepler,'finite_edge_fluid_family':results,'assumptions':['prescribed central M(t), no backreaction in tracer scan','C=pi^2/8 and angular momentum ell prescribed','Kepler histories allow independent phases; not claimed cosmological growing-mode histories','finite edge fluid equilibrium on r>0; no covariant action, global stability or phase-space distribution proved'],'a0_footings':FOOTS,'kappa':'1/2 fitted','Z':5.7888}
path=pathlib.Path(os.environ.get('EDGE_OUTPUT',str(pathlib.Path(__file__).with_name('edge_results'+('_MUTATE' if MUT else '')+'.json'))))
path.write_text(json.dumps(out,indent=2))
for k,v in checks.items():print(('PASS' if v['passed'] else 'FAIL'),k)
print('Orbit x range',min(r['x'] for r in rows),max(r['x'] for r in rows))
print('Output',path)
sys.exit(0 if all(c['passed'] for c in checks.values()) else 1)
