"""Unit-consistent isolated gravitational dimer example, not formation evidence."""
import json,pathlib,sys
import mpmath as m
m.mp.dps=50
G=m.mpf('6.67430e-11')
h=m.mpf('6.62607015e-34')
hbar=h/(2*m.pi)
clight=m.mpf('299792458')
eV=m.mpf('1.602176634e-19')
mass=m.mpf('1e6')*eV/clight**2
alpha=G*mass**2/(hbar*clight)
aB=2*hbar**2/(G*mass**3)
EB=G**2*mass**5/(4*hbar**2)
omega=8*EB/(9*hbar)
assert abs(aB*EB-G*mass**2/2)<m.mpf('1e-120')
assert abs(EB/(mass*clight**2)-alpha**2/4)<m.mpf('1e-100')
out={'mass_input_MeV':1,'constants_SI':{'G':str(G),'h':str(h),'c':str(clight),'electron_volt_J':str(eV)},'mass_kg':str(mass),'alpha_G':str(alpha),'Bohr_radius_m':str(aB),'binding_energy_J':str(EB),'binding_energy_eV':str(EB/eV),'omega_1s_3d_s_inverse':str(omega),'inverse_omega_seconds':str(1/omega),'period_seconds':str(2*m.pi/omega),'fractional_contact_shift_per_lambda_rep':str(alpha/(4*m.pi)),'non_claims':['No preparation rate or abundance','No cosmological isolated-state applicability','No numerical gravitational-radiation lifetime','Mass is an explicit prior benchmark, not a derived prediction']}
pathlib.Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['Bohr_radius_m','binding_energy_eV','omega_1s_3d_s_inverse','inverse_omega_seconds']}))
