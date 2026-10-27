import argparse,json,sys
from pathlib import Path
import numpy as np
from test_flux import main as test_flux
from test_lead import main as test_lead
from test_branch_energy import main as test_energy
from electronic import states
from pyscf import fci,ao2mo,symm
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
test_flux();test_lead();test_energy();bench=[]
for R,basis in [(2.,'aug-cc-pvdz'),(2.,'rydberg3'),(12.,'rydberg2')]:
 m,C,ci,en=states(R,basis);h=C.T@(m.intor('int1e_kin')+m.intor('int1e_nuc'))@C
 solver=fci.direct_spin0_symm.FCI(m);solver.orbsym=symm.label_orb_symm(m,m.irrep_id,m.symm_orb,C);solver.wfnsym='Ag';solver.nroots=3;solver.conv_tol=1e-11;solver.max_cycle=300
 E,_=solver.kernel(h,ao2mo.kernel(m,C),len(C),(1,1));assert all(solver.converged);err=float(np.max(abs(np.array(E)+m.energy_nuc()-en[:3])));assert err<1e-8
 bench.append(dict(R=R,basis=basis,max_energy_error=err));print('independentCI',bench[-1],flush=True)
b=Path(__file__).resolve().parent;s=json.loads((b/'run_stream_check/results.json').read_text());d=json.loads((b/'run_lead_ry2_h10/results.json').read_text());err=max(float(np.max(abs(np.array(x['probabilities'])-y['probabilities']))) for x,y in zip(s['rows'],d['rows']));assert err<1e-10
Path(a.output).write_text(json.dumps(dict(independent_CI=bench,streamed_vs_stored_max_probability_error=err,free_lead_and_coupled_lead_checks=True,event_energy_charge_constituent_conservation=True,thermal_Einstein_balance=True,physical_DR_rates_tested=False),indent=2)+'\n')
