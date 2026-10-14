"""Finite-detuning PV and initial on-shell collision source, prescribed bath."""
import json,sys
from pathlib import Path
import mpmath as mp
mp.mp.dps=45;D=mp.mpf
source=json.loads(Path('sol61_push/ordinary_lepton_source_2026_10_13/run/results.json').read_text())['reduced_muon_case']
old=json.loads(Path('sol61_push/thermal_source_carrier_shift_2026_10_13/run/results.json').read_text())
mu=D(str(source['equal_width_mu_R_phi_eV']));m=D('1e6');delta=D('2.6625713955157683e-16');MR=2*m+delta;hb=D('6.582119569e-16')
checks=[]
def ck(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
def sumk(order,x):return sum(mp.besselk(order,n*x)/n for n in range(1,121))
rows=[]
for prior in old['rows']:
 if prior['T_MeV']<.5:continue
 T=D(str(prior['T_MeV']))*10**6
 # One perturbative mass update; not a solved gap equation.
 shift=D(str(prior['carrier_mass_shift_eV']));mi=m+shift;gap=delta-2*shift
 k0=MR/(2*mi)*mp.sqrt(gap*(MR+2*mi));b=k0/T;x=MR/T
 def h(q):
  e=mp.sqrt(q*q+x*x)
  return 1/(e*mp.expm1(e))
 ha=h(b)
 def regular(q):
  if q==b:return mp.diff(h,b)/(2*b)
  return (h(q)-ha)/(q*q-b*b)
 I0=mp.quad(h,[0,1,10,mp.inf])
 correction=b*b*mp.quad(regular,[0,b/2,b,2*b,D('.01'),D('.1'),1,10,mp.inf])
 J=I0+correction
 Pi=-mu*mu*MR*MR/(8*mp.pi**2*mi*mi)*J
 ck('threshold quadrature reproduced '+str(T),abs(I0/D(str(prior['I0_dimensionless']))-1)<D('1e-9'))
 ck('finite detuning real correction small '+str(T),abs(Pi/D(str(prior['thermal_Pi_phi_eV2']))-1)<D('1e-7'))
 ER=MR*MR/(2*mi);Eq=ER-mi
 ck('decay daughter shell '+str(T),abs((Eq*Eq-mi*mi-k0*k0)/(mi*mi))<D('1e-35'))
 fR=1/mp.expm1(ER/T)
 S0=mu*mu*k0/(8*mp.pi*mi*mi)*fR
 # Same Jacobian obtained directly from the reduced invariant phase space.
 jac=abs(k0/ER-k0/Eq)
 phase=mu*mu/(8*mp.pi*mi)*k0*k0/(ER*Eq)/jac*fR
 ck('rest-mode phase-space Jacobian '+str(T),abs(phase/S0-1)<D('1e-30'))
 # Statistical detailed balance at common T, zero chemical potentials.
 f1=1/mp.expm1(mi/T);f2=1/mp.expm1(Eq/T)
 gain=fR*(1+f1)*(1+f2);loss=(1+fR)*f1*f2
 ck('Bose detailed balance '+str(T),abs(gain/loss-1)<D('1e-35'))
 width=mu*mu/(16*mp.pi*MR)*mp.sqrt(gap*(MR+2*mi))/MR
 nR=MR*MR*T/(2*mp.pi**2)*sumk(2,x)
 nphieq=mi*mi*T/mp.pi**2*sumk(2,mi/T)
 mean_dilation=sumk(1,x)/sumk(2,x)
 ndot=2*width*nR*mean_dilation
 rows.append({'T_MeV':float(T/1e6),'one_step_carrier_mass_shift_eV':float(shift),
 'effective_pair_excess_eV':float(gap),'finite_detuning_PV_over_threshold_minus_one':float(Pi/D(str(prior['thermal_Pi_phi_eV2']))-1),
 'rest_mode_parent_momentum_eV':float(k0),'initial_rest_mode_df_dt_per_s':float(S0/hb),
 'quasiparticle_spontaneous_partial_width_eV':float(width),
 'initial_total_number_source_over_equilibrium_number_per_s':float(ndot/nphieq/hb),
 'assumed_R_number_density_eV3':float(nR),'initial_number_source_eV4':float(ndot)})
result={'all_pass':all(c['passed'] for c in checks),'checks':checks,'rows':rows,
 'non_claims':['One mass update and narrow on-shell collision model, not self-consistent spectral kinetics',
 'Initially empty carrier sector; inverse reactions/backreaction must be restored during evolution',
 'No unbounded Bose growth, final abundance, cosmological exclusion or manufacturing protocol']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
