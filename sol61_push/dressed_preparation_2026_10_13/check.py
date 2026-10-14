import json,math,sys
from pathlib import Path
from scipy.integrate import solve_ivp
p=Path(__file__).parent
b=json.loads((p/'INPUT_WIDTHS.json').read_text())['benchmark'];gamma=b['radiative_width_s_inv'];base=b['nonradiative_width_s_inv']
rows=[]
for f in [.01,1.,100.]:
 for ratio in [1e-6,.01,1.,100.,base/gamma]:
  matter=ratio*gamma;D=matter*(1+2*f)+gamma;ss=matter*f*f/D
  # tau=D*t. Includes gross inverse collisions and final-state Bose stimulation.
  def ode(t,y):
   N,C=y
   return [(matter/D)*(f*f*(1+N)-(1+f)**2*N)-(gamma/D)*N,(gamma/D)*N]
  end=3.;sol=solve_ivp(ode,[0,end],[0,0],rtol=1e-10,atol=1e-12)
  exact=ss*(-math.expm1(-end));count=gamma/D*ss*(end+math.expm1(-end))
  assert sol.success and abs(sol.y[0,-1]-exact)<1e-8*(1+exact)
  assert abs(sol.y[1,-1]-count)<1e-8*(1+count)
  assert gamma*ss<=gamma*f*f/(1+2*f)*(1+1e-12)
  rows.append(dict(f=f,matter_over_photon=ratio,occupation_stationary=ss,occupation_bath_equilibrium=f*f/(1+2*f),
   photon_flux_per_mode_s_inv=gamma*ss,relaxation_seconds=1/D,ode_error=abs(sol.y[0,-1]-exact),photon_count_error=abs(sol.y[1,-1]-count)))
# A stipulated maintained excited population, distinct from a thermal mode bath.
c=299792458.;omega=5*.7143737072979501;M=2000005.
energy_per_source_equivalent_kg=omega/M*c*c
result=dict(rows=rows,gamma_s_inv=gamma,base_matter_s_inv=base,
 maintained_population=dict(initial_power_W_per_source_equivalent_kg=gamma*energy_per_source_equivalent_kg,
 gross_replacement_power_W_per_source_equivalent_kg=(gamma+base)*energy_per_source_equivalent_kg,
 photon_energy_fraction=gamma/(gamma+base),
 qualification='Gross excitation replacement if each decay removes an excitation; not net work or heat loss if matter energy is recovered.'),
 scope='Fixed incoherent isotropic bath, equal occupation f at the two on-shell momenta, Markov and golden-rule closure; one normalized gapped mode. No condensate depletion or preparation of the bath derived.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result['maintained_population'],indent=2))
