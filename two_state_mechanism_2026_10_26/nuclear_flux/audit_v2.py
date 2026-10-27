import argparse,json,sys
from pathlib import Path
import numpy as np
from electronic import states
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();b=Path(__file__).resolve().parent
sys.path.insert(0,str(b.parent/'continuum'));from kmat import read_k
pre=json.loads((b/'run_preflight_env/results.json').read_text());kernels=[]
for R,label,src in [(2,'run_kernel',b.parent/'continuum/run_physical_radial25'),(3,'run_kernel_R3',b/'run_capture_R3'),(4,'run_kernel_R4',b/'run_capture_R4')]:
 d=json.loads((b/label/'results.json').read_text());npz=np.load(b/label/'kernel.npz');err=float(np.max(abs(np.linalg.eigvalsh(npz['H_QQ'])-states(R)[3])));assert err<1e-8
 row=d['rows'][0];uk=read_k(src/'Kmat.txt')[0];S=lambda z:np.array(z['S_real'])+1j*np.array(z['S_imag']);diff=float(np.max(abs(S(row)-S(uk))))
 kernels.append(dict(R=R,Q_CI_eigenvalue_max_error=err,coulomb_only_vs_UKRmol_max_S_difference_at_001=diff,optical_identity_max_relative_error=max(r['optical_identity_relative_error'] for r in d['rows']),open_ranks=[int(np.sum(np.array(r['width_eigenvalues'])>1e-10)) for r in d['rows']]))
nuclear=[]
for label in ['run_lead_ry2_h10','run_lead_ry2_h05','run_lead_ry2_h025','run_lead_ry2_R40','run_lead_ry3_h05','run_stream_ry3_h025','run_stream_ry4_h05']:
 d=json.loads((b/label/'results.json').read_text());r=next(x for x in d['rows'] if x['energy']==-.6)
 assert r['mode_weights'][0][0]>.99
 nuclear.append(dict(run=label,basis=d['settings']['basis'],h=d['settings']['h'],end=d['settings']['end'],ground_dominated_mode_to_other_modes_probability=float(sum(r['probabilities'][i][0] for i in range(1,len(r['probabilities'])))),max_unitarity_error=max(x['unitarity_error'] for x in d['rows']),max_reciprocity_error=max(x['reciprocity_error'] for x in d['rows'])))
checks=json.loads((b/'run_checks/results.json').read_text())
result=dict(kernels=kernels,nuclear=nuclear,atomic=[dict(basis=r['basis'],first_dipole_allowed_energy=r['atomic_energies'][r['first_E1_states'][0]],line_frequency=r['line_frequencies'][0],E1_coefficient=r['E1_rate_divided_by_alpha_cubed'][0],retained_ground_derivative_fraction=r['nuclear_derivatives'][-1]['retained_fractions'][str(r['electronic_singlet_Ag_states'])]) for r in pre['rows']],independent_checks=checks,physical_DR_rates_derived=False,physical_DR_product_branching_derived=False,physical_photon_galaxy_runs=0,classification='Partial microscopic operators and neutral radial flux; rates unavailable, nuclear convergence unresolved, ideal-lead transition results rejected for physical interpretation')
Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
