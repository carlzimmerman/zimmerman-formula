"""Assess numerical resolution and whether output supplies cold kinetic data."""
import json,sys
from pathlib import Path
import numpy as np

p=Path(__file__).parent
coarse=json.loads((p/'coupled_fragmentation_run/results.json').read_text())
fine=json.loads((p/'coupled_fragmentation_96_run/results.json').read_text())
r64=coarse['rows'][2];r96=fine['rows'][0]
comparisons={key:abs(r96[key]-r64[key]) for key in
 ['late_variance_fraction','late_gradient_fraction','late_pressure_over_energy']}
data=np.genfromtxt(p/'coupled_fragmentation_96_run/fine96.csv',delimiter=',',names=True)
late=data['z']>=150
rho=data['phi_kinetic_physical']+data['phi_gradient']+data['phi_potential']
interaction_fraction=float(np.sum(data['phi_potential'][late])/np.sum(rho[late]))
source=fine['source'];H=source['H_GeV'];m=.001;M=2*m*np.sqrt(1+.02**2)
aend=float(data['a'][-1]);a_X=np.sqrt(H/M)
omega=H*source['omega_over_H']
mass_ratio_end=float(m/np.sqrt(H/(aend*aend)*M))
checks=dict(fine_energy=r96['energy_work_residual']<.002,
 fine_charge=r96['charge_absolute_drift']<1e-9,
 fine_UV=r96['final_uv_gradient_fraction']<.05,
 refinement=max(comparisons.values())<.02)
out=dict(checks=checks,all_pass=all(checks.values()),
 absolute_64_to_96_changes=comparisons,
 measured=dict(late_inhomogeneous_Phi_variance_fraction=r96['late_variance_fraction'],
  late_coherent_variance_fraction=1-r96['late_variance_fraction'],
  late_Phi_pressure_over_energy=r96['late_pressure_over_energy'],
  late_Phi_interaction_energy_fraction=interaction_fraction,
  X_mean_square_relative_change=r96['final_X_mean_physical_squared_ratio']-1,
  final_H_GeV=H/aend**2,minimum_resolved_nonzero_p_over_m=r96['minimum_nonzero_p_over_m']),
 kinetic_handoff=dict(ready=False,cold_relic_yield=None,cold_mass_for_collapse=None,
  reasons=['Order-one coherent Phi component remains; a dilute particle distribution is not established.',
   'Phi interaction energy is not negligible and its average pressure is radiation-like.',
   'X remains overdamped: H/M is much greater than one; its homogeneous amplitude is not a late particle number.',
   'All nonzero box momenta are much greater than m; no late cold spectrum has been resolved.',
   'Classical-statistical vertices do not supply the complete quantum gain/loss collision terms in a dilute regime.']),
 hierarchy=dict(a_at_final=aend,a_at_H_equals_M=float(a_X),
  additional_scale_factor_to_X_oscillation=float(a_X/aend),
  conformal_z_at_H_equals_M=float((a_X-1)*source['omega_over_H'])),
 scope='Numerical assessment of one conditional finite-band realization. The absence of a cold kinetic handoff here is not proof that no later cold matter forms.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
sys.exit(0 if out['all_pass'] else 1)
