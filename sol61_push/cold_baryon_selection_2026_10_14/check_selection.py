"""Four bounded discriminators for baryon-phase selection; not a solved model."""
import json
import math
import sys
import ast
from types import SimpleNamespace
from pathlib import Path
import sympy as s
import numpy as np

checks=[]
def check(name,condition):
    passed=bool(condition)
    checks.append(dict(name=name,passed=passed))
    if not passed:
        raise AssertionError(name)
def identity(name,expr):
    check(name,s.simplify(expr)==0)

# G: the corrected action sees all source densities in the same vertex.
K,a,u,g,phi,rc,rh,rf=s.symbols('K a u g phi rc rh rf',positive=True)
W=(-a*u-a*a*s.log(1-u/a))/K
L=-g*g/(2*K)+u*g/K-W-(rc+rh+rf)*phi
identity('all phase densities have the same gravitational vertex',s.diff(L,rc)-s.diff(L,rh))
identity('free source has the same ordinary gravitational vertex',s.diff(L,rc)-s.diff(L,rf))
identity('density-preserving baryon phase swap leaves the action unchanged',
         L.xreplace({rc:rh,rh:rc})-L)
identity('full polarization force in corrected action',K*s.diff(L,u)-(g-a*u/(a-u)))
b,h,f=s.symbols('b h f',positive=True)
R=u*u/(a-u)
identity('static cold law must read all external gravity',
         (a*u/(a-u)-(u+b+h+f))-(R-b-h-f))
identity('condensed-only template leaves omitted gravity on carrier',
         (R-b-h-f).subs(b,R)+h+f)
# A frequency filter reads the static mean field of hot gas as well.
kappa,Jc,Jh=s.symbols('kappa Jc Jh',positive=True)
response=(Jc+Jh)/kappa
identity('static hot source is retained by nonzero static susceptibility',response-Jc/kappa-Jh/kappa)
check('hot static response is positive',s.ask(s.Q.positive(Jh/kappa)) is True)

# K: a zero-drift Maxwell collision term has heat sign Tb-Tchi.
mb,mc,Tb,Tc,A=s.symbols('mb mc Tb Tc A',positive=True)
mu=mb*mc/(mb+mc)
s2=Tc/mc+Tb/mb
Q=mu/(mb+mc)*(Tb-Tc)*A/s2
identity('elastic heat exchange vanishes at equal temperatures',Q.subs(Tb,Tc))
check('elastic prefactor multiplying Tb-Tchi is positive',
      s.ask(s.Q.positive(mu*A/((mb+mc)*s2))) is True)
# Cold pressureless corotation with ordinary matter is incompatible with R>=0.
bt,ut,at=s.symbols('bt ut at',positive=True)
gordinary=bt+ut
anet=-gordinary+ut+at
identity('corotation force residual is outward full tether',anet+gordinary-(ut+at))
check('corotation residual positive for nonzero tether',s.ask(s.Q.positive(ut+at)) is True)

# S: a proposed coefficient switching the full tether has an exact critical point.
x,alpha,bb=s.symbols('x alpha bb',positive=True)
wn=-x-s.log(1-x)
effective=alpha*wn-x*x/2
F=s.diff(effective,x)
identity('state-dependent full tether net residual',F-((alpha-1)*x+alpha*x*x/(1-x)))
identity('state-dependent coefficient curvature at zero',s.diff(effective,x,2).subs(x,0)-(alpha-1))
identity('static coefficient equation',s.expand((F-bb)*(1-x))-
         (x*x+(bb+alpha-1)*x-bb))
identity('critical coefficient recovers intended residual',F.subs(alpha,1)-x*x/(1-x))
identity('subcritical coefficient admits unsourced polarized root',
         (x*x+(alpha-1)*x).subs(x,1-alpha))
identity('subcritical root has positive radial curvature',
         s.diff(effective,x,2).subs(x,1-alpha)-(1/alpha-1))
chi=s.symbols('chi',real=True)
alpha_chi=s.Function('alpha')(chi)
identity('phase evolution has nonzero polarization work term',
         s.diff(alpha_chi*wn,chi)-s.diff(alpha_chi,chi)*wn)

# M: carrier condensation does not identify baryon phase at fixed density.
z,beta,aa,coup=s.symbols('z beta aa coup',positive=True)
landau=aa*z+beta*z*z/2-coup*(rc+rh)*z
identity('carrier Landau order parameter reads total baryon source',
         s.diff(landau,rc)-s.diff(landau,rh))
identity('Landau positive branch stationary equation',
         s.diff(landau,z).subs(z,(coup*(rc+rh)-aa)/beta))
identity('baryon phase swap leaves carrier Landau energy unchanged',
         landau.xreplace({rc:rh,rh:rc})-landau)

# S: inspect the actual small tagging function without loading a PM engine.
# All model globals, particle grids and FFT construction are intentionally absent.
memory_rows=[]
for code_path in ['campaign_fresh_gravity/CFG640_phase_source_pm/cfg640_pm.py',
                  'campaign_fresh_gravity/CFG650_theory_v2_combined_pm/cfg650_pm.py']:
    module=ast.parse(Path(code_path).read_text())
    nodes=[node for node in module.body if isinstance(node,ast.FunctionDef) and node.name=='update_tags']
    check('unique actual tagging function '+code_path,len(nodes)==1)
    extracted=ast.Module(body=nodes,type_ignores=[])
    def serial_map(fn,chunks):
        return [fn(chunk) for chunk in chunks]
    env={'np':np,'pmap':serial_map}
    exec(compile(extracted,code_path,'exec'),env)
    mesh=SimpleNamespace(M=2,dx=1.)
    positions=np.zeros((2,3),dtype=np.float64)
    particle=SimpleNamespace(fd=np.array([0.,.8],dtype=np.float16),ichunks=[(0,2)],
                             positions=lambda start,stop:positions[start:stop])
    codes=np.ones((2,2,2),dtype=np.int64)
    env['update_tags'](mesh,particle,codes,[0.,.1])
    first=particle.fd.astype(np.float64).tolist()
    check('same current catchment retains different histories '+code_path,
          first[0]<.11 and first[1]>.79)
    env['update_tags'](mesh,particle,np.zeros_like(codes),[0.,.1])
    check('outside catchment does not erase tags '+code_path,
          np.array_equal(particle.fd.astype(np.float64),np.array(first)))
    env['update_tags'](mesh,particle,codes,[0.,.6])
    last=particle.fd.astype(np.float64).tolist()
    check('new catchment can raise but not lower tags '+code_path,
          .59<last[0]<.61 and last[1]>.79)
    memory_rows.append(dict(code=code_path,after_same_current_catchment=first,
                            after_higher_condensed_catchment=last))

tcoord,xcoord=s.symbols('tcoord xcoord',real=True)
rho=s.Function('rho')(tcoord,xcoord)
velocity=s.Function('velocity')(tcoord,xcoord)
eta=s.Function('eta')(tcoord,xcoord)
identity('weighted baryon current has a conversion source',
         s.diff(eta*rho,tcoord)+s.diff(eta*rho*velocity,xcoord)
         -eta*(s.diff(rho,tcoord)+s.diff(rho*velocity,xcoord))
         -rho*(s.diff(eta,tcoord)+velocity*s.diff(eta,xcoord)))

# Numerical rows are diagnostics with assigned inputs, not observations.
C=299792458.0
EV=1.602176634e-19
KB=1.380649e-23
HBAR=1.054571817e-34
MP=1.67262192369e-27
G=6.67430e-11
MSUN=1.98847e30
PC=3.085677581491367e16
RSUN=6.957e8
heat_rows=[]
for m_eV in [.62,16.,143.]:
    for T_K in [10.,100.,1e4]:
        sigma=1e5
        Tchi=m_eV*EV*(sigma/C)**2/KB
        m_min=KB*T_K/EV*(C/sigma)**2
        check('assigned cold-gas example heats light carrier m=%g T=%g'%(m_eV,T_K),T_K>Tchi)
        heat_rows.append(dict(mass_eV=m_eV,baryon_temperature_K=T_K,
                              sigma_km_s=sigma/1e3,carrier_kinetic_temperature_K=Tchi,
                              cooling_requires_mass_eV_above=m_min,
                              contact_heat_sign='heats carrier'))
hot_rows=[]
for theta_keV in [.1,1.,8.]:
    theta=theta_keV*1e3
    pr=3*theta*EV/(.6*MP*C*C)
    m_min=theta*(C/1e6)**2
    check('pressure correction small in assigned keV gas %g'%theta_keV,0<pr<1e-4)
    hot_rows.append(dict(kT_keV=theta_keV,schematic_3p_over_rho_c2=pr,
                         sigma_km_s=1000.,cooling_requires_mass_eV_above=m_min))

drag_rows=[]
for y in [1e-4,.01,.1,1.]:
    nu=(1+math.sqrt(1+4/y))/2
    vmax_fraction=1/math.sqrt(nu)
    gamma_t=-math.log1p(-vmax_fraction)
    check('carrier maximum binding speed below baryon circular speed y=%g'%y,
          0<vmax_fraction<1)
    drag_rows.append(dict(gb_over_a0=y,nu=nu,
                         max_carrier_speed_over_baryon_speed=vmax_fraction,
                         frozen_radius_drag_gamma_t_to_binding_ceiling=gamma_t))

# Opaque physical stars; ignores any enhanced dark clustering and long-range vertex.
Nstars=1e10
Rdisc=5e3*PC
Vrel=2e5
focus=1+2*G*MSUN/(RSUN*Vrel*Vrel)
optical_depth=Nstars*(RSUN/Rdisc)**2*focus
max_crossings=1000
encounter_probability_bound=max_crossings*optical_depth
check('physical stellar encounter probability tiny in assigned disc',encounter_probability_bound<1e-6)
stellar=dict(stars=Nstars,disc_radius_kpc=5.,star_radius_m=RSUN,
             relative_speed_km_s=200.,focusing_factor=focus,
             one_crossing_optical_depth=optical_depth,
             assigned_crossings=max_crossings,
             encounter_probability_upper_bound=encounter_probability_bound)

# Ideal free Bose gas: n*lambda_T^3=zeta(3/2), kT=m*sigma^2.
zeta=float(s.zeta(s.Rational(3,2)))
phase_rows=[]
for name,rho_unit,sigma_km in [('galaxy_diagnostic',.01,100.),('cluster_diagnostic',.001,1000.)]:
    rho=rho_unit*MSUN/PC**3
    sigma=sigma_km*1e3
    mass_kg=((2*math.pi)**1.5*HBAR**3*rho/(zeta*sigma**3))**.25
    mass_eV=mass_kg*C*C/EV
    phase_rows.append(dict(name=name,assigned_density_Msun_pc3=rho_unit,
                          assigned_sigma_km_s=sigma_km,ideal_Bose_mass_threshold_eV=mass_eV))
    for test_mass in [.62,1.,16.,143.]:
        n=rho/(test_mass*EV/(C*C))
        lam=math.sqrt(2*math.pi)*HBAR/(test_mass*EV/(C*C)*sigma)
        occupancy=n*lam**3/zeta
        identity_value=(mass_eV/test_mass)**4
        check('Bose criterion independent mass-power check %s m=%g'%(name,test_mass),
              math.isclose(occupancy,identity_value,rel_tol=1e-12))
check('assigned galaxy/cluster diagnostic has a possible phase window',
      phase_rows[0]['ideal_Bose_mass_threshold_eV']>phase_rows[1]['ideal_Bose_mass_threshold_eV'])

out=dict(checks=checks,heat_diagnostics=heat_rows,hot_pressure_diagnostics=hot_rows,
         drag_diagnostics=drag_rows,stellar_encounter_diagnostic=stellar,
         ideal_Bose_diagnostics=phase_rows,actual_PM_memory_controls=memory_rows,
         verdict='class-specific selection obstructions and conditional medium-phase alternative',
         non_claims=['No measured phase temperatures/densities inferred from these diagnostic rows',
                    'No real cross-section or heat/drag rate derived',
                    'Ideal Bose degeneracy alone proves neither superfluidity nor thermalization',
                    'Coefficient-switch and Landau models are comparison models, not adopted actions',
                    'No finite halo, source-phase selector or relativistic completion established'])
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(checks=len(checks),all_passed=all(x['passed'] for x in checks),
                      min_cold_gas_cooling_mass_eV=min(x['cooling_requires_mass_eV_above'] for x in heat_rows),
                      phase_diagnostics=phase_rows,stellar_encounter_bound=encounter_probability_bound),indent=2))
