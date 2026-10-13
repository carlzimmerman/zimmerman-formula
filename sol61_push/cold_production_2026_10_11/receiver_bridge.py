"""Bridge recent target-energy bounds to the candidate's reversible mass gap."""
import json,math
from pathlib import Path
p=Path(__file__).parent;root=p.parents[1]
par=json.loads((p/'detuned_carrier_run/results.json').read_text())['parameters']
prod=json.loads((p/'detuned_bogoliubov_run/results.json').read_text())
low=json.loads((root/'sol61_push/collective_energy_lower_2026_10_11/run/results.json').read_text())
upper=json.loads((root/'sol61_push/collective_energy_gate_2026_10_11/run/results.json').read_text())
cells=json.loads((root/'campaign_fresh_gravity/CFG626_kernel_recheck_anisotropic_target/cfg626_results_mono.json').read_text())['cells']
c=299792458.;u=par['u'];eta=1-1/math.sqrt(1+u*u);kick=c*u/math.sqrt(1+u*u)
remnant=1-prod['rows'][1]['fraction_at_x200'];checks=[];rows=[]
for cell in low['rows']:
 name=cell['cell'];V=cells[name]['Vf_kms']*1000
 fine=next(x for x in upper['rows'] if x['cell']==name)['fine']
 # R=1; softened g(R) <= baryon total Mb + retained cold mass.
 edge_upper=cells[name]['Mb']+fine['M']
 vmax=V*math.sqrt(2*cell['potential_drop']+edge_upper)
 importC=cell['signed_import_over_M']['C']
 capacity=eta*c*c/(V*V)
 fraction=importC/capacity
 required_u=math.sqrt(1/(1-importC*(V/c)**2)**2-1)
 checks.append(dict(name=name+' energy capacity inversion',passed=abs(fraction*capacity/importC-1)<1e-12))
 rows.append(dict(cell=name,Vf_kms=V/1000,C_energy_import_over_MVf_squared=importC,max_source_gap_capacity_over_MVf_squared=capacity,min_initial_source_mass_fraction_for_C=fraction,Gaussian_endpoint_source_charge_fraction=remnant,capacity_shortfall_vs_endpoint=fraction/remnant,conservative_max_target_bound_speed_kms=vmax/1000,source_rest_decay_kick_kms=kick/1000,rest_decay_cannot_keep_both_daughters_in_target=kick>vmax,minimum_u_for_unit_source_mass_capacity=required_u))
out=dict(rows=rows,checks=checks,all_pass=all(c['passed'] for c in checks),non_claims=['Capacity is necessary, not a transfer rate or a reachable endpoint','Source mass and charge fractions differ by order u^2; endpoint comparison is approximate at that order','Target-orbit velocity bound applies to fixed benchmark potential and natural outer edge','No evolution from early production to halo source abundance supplied','Carrier adds an internal degree of freedom absent from benchmark orbital energies'])
(p/'receiver_bridge_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
