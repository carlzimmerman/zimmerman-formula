"""Ideal Bose capacity gate, not an interacting finite-temperature phase solution."""
import json,math,sys
from pathlib import Path
import mpmath as mp
from scipy.integrate import quad
from scipy.optimize import brentq
prior=json.loads(Path('sol61_push/explicit_neutral_medium_2026_10_14/run/results.json').read_text())
nSI=prior['rows'][-1]['total_conserved_number_density_per_m3'];hc=1.973269804e-7;c=299792458.;m=1.;M=2.;delta=2e-9;kB=8.617333262e-5;n=nSI*hc**3
mp.mp.dps=40;zeta15=float(mp.zeta(1.5));zeta25=float(mp.zeta(2.5));checks=[]
def ck(name,e,t):
    assert e<=t,(name,e,t)
    checks.append(dict(name=name,error=float(e),tolerance=t))
def poly(order,x):return float(mp.polylog(order,mp.exp(-x)))
def capacities(T):
    atomic=(m*T/(2*math.pi))**1.5*zeta15
    mediator=(M*T/(2*math.pi))**1.5*poly(1.5,delta/T)
    kinetic=1.5*T*(2*(m*T/(2*math.pi))**1.5*zeta25+(M*T/(2*math.pi))**1.5*poly(2.5,delta/T))
    return 2*atomic+2*mediator,kinetic,mediator
Tc=math.exp(brentq(lambda logT:capacities(math.exp(logT))[0]/n-1,math.log(1e-8),math.log(.1),xtol=1e-13))
cap,energy,nR=capacities(Tc)
ck('critical_capacity_equation',abs(cap/n-1),1e-11)
# Independent momentum integral, variable y=p/sqrt(2mT).
for x in [0.,delta/Tc,.01,1.]:
    def integrand(y):
        a=y*y+x
        if a>700:return 0.
        if a==0:return 1.
        return y*y/math.expm1(a)
    integral=quad(integrand,0,math.inf,epsabs=1e-12,epsrel=1e-12)[0]
    ck('polylog_vs_momentum_integral',abs(integral/(math.sqrt(math.pi)/4*poly(1.5,x))-1),1e-10)
atomicTc=2*math.pi/m*(n/(2*zeta15))**(2/3)
zero_gapTc=2*math.pi/m*(n/((2+2*(M/m)**1.5)*zeta15))**(2/3)
assert zero_gapTc<Tc<atomicTc
rows=[]
energy_rows=[]
for speed in [30e3,100e3,200e3,1000e3]:
    labelT=m*(speed/c)**2;capacity,_,_=capacities(labelT)
    # Label T uses a classical energy/dispersion conversion only as a comparison.
    rows.append(dict(assigned_1D_speed_m_s=speed,kinetic_temperature_label_eV=labelT,maximum_ideal_noncondensed_constituent_fraction=min(1.,capacity/n),ideal_excess_density_fraction=max(0.,1-capacity/n),classical_comparison_energy_per_constituent_eV=1.5*labelT))
    target=1.5*labelT
    # Match kinetic energy directly on the saturated ideal branch. A condensate
    # in the zero-energy atomic modes supplies the remaining constituents.
    assert target<energy/n
    Te=math.exp(brentq(lambda logT:capacities(math.exp(logT))[1]/n/target-1,math.log(1e-10),math.log(Tc),xtol=1e-13))
    ne,ue,nre=capacities(Te)
    ck('matched_kinetic_energy_'+str(int(speed)),abs(ue/n/target-1),1e-11)
    assert ne<n
    energy_rows.append(dict(assigned_1D_speed_m_s=speed,matched_kinetic_energy_per_constituent_eV=target,ideal_equilibrium_temperature_eV=Te,ideal_noncondensed_constituent_fraction=ne/n,ideal_atomic_condensate_constituent_fraction=1-ne/n,detuning_energy_per_constituent_eV=delta*nre/n))
result=dict(energy_matched_ideal_equilibrium=energy_rows,scope='Noninteracting chemical-equilibrium capacity with conserved N and neutral Q; no claim about actual interacting condensate fraction or halo thermal equilibrium',total_constituent_density_per_m3=nSI,critical_temperature_eV=Tc,critical_temperature_K=Tc/kB,atomic_only_critical_temperature_eV=atomicTc,zero_detuning_three_species_critical_temperature_eV=zero_gapTc,kinetic_energy_per_constituent_at_threshold_eV=energy/n,detuning_energy_per_constituent_at_threshold_eV=delta*nR/n,equivalent_1D_speed_from_threshold_kinetic_energy_m_s=c*math.sqrt(2*energy/(3*m*n)),benchmark_interaction_scale_over_critical_T=prior['rows'][-1]['NR_scale_over_mass']*m/Tc,velocity_comparisons=rows,checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
