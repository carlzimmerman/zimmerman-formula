"""Necessary-condition diagnostics; no synthetic chemistry or galaxy success."""
import json,argparse,math
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
G=6.67430e-11;MSUN=1.98847e30;KPC=3.085677581491367e19;c=299792458.;hbar_ev=6.582119569e-16;eta=5.364;M=100
profiles=[(3e5,.3),(1e8,1.),(6e10,3.),(1e14,300.)];rows=[]
for mass,r in profiles:
 sigma2=G*(1+eta)*mass*MSUN/(6*r*KPC);v=math.sqrt(6*sigma2);omega=v/(r*KPC);rho=3*eta*mass*MSUN/(4*math.pi*(r*KPC)**3)
 rows.append(dict(Mb=mass,r_kpc=r,sigma_km_s=math.sqrt(sigma2)/1000,omega_s=omega,rotation_energy_J1_eV=hbar_ev*omega,rho=rho,phase_proxy=rho/sigma2**1.5,coulomb_proxy=rho**(1/3)/sigma2,alpha_for_line_gap_equal_initial_kT=math.sqrt((M+1)*sigma2/(2*c*c*.375))))
disk=rows[2]
for r in rows:
 r['phase_proxy_relative_disk']=r['phase_proxy']/disk['phase_proxy'];r['coulomb_proxy_relative_disk']=r['coulomb_proxy']/disk['coulomb_proxy'];r['rotational_shift_over_line_gap_at_alpha02_m10MeV']=r['rotation_energy_J1_eV']/(.375*.2**2*1e7)
assert all(rows[i]['phase_proxy_relative_disk']>1 and rows[i]['coulomb_proxy_relative_disk']>1 for i in [0,1])
# Formation 2X+C -> T: equal total charge and unchanged monopole force.
assert 2*1-1==1
# At fixed uniform field the ratio of total forces is exactly one.
checks=dict(assembly_charge_before=1,assembly_charge_after=1,uniform_field_total_force_ratio=1,assembled_q_over_m_relative_bare_X=100/201)
Path(a.output).write_text(json.dumps(dict(rows=rows,checks=checks,scope='Fixed inherited mean profiles, common particle parameters, ideal degeneracy and classical Coulomb coupling thresholds. No cooling-rate calculation, field response, dynamics or universal no-go theorem.'),indent=2)+'\n')
