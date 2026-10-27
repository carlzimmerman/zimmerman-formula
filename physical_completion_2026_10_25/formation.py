import argparse,json
from pathlib import Path
import numpy as np,torch
from vacuum_checked import Vacuum
from fast_complete import finish
from joint import T
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);m=Vacuum();allF=json.loads(Path('physical_completion_2026_10_25/run_vacuum/all_F.json').read_text());xx=T(np.zeros(m.n)).requires_grad_(True);zz=T(np.log(allF['mass']));H=torch.autograd.functional.hessian(lambda x:m.energy(zz,x),xx).detach().numpy();sv=np.sqrt(m.vol.numpy());ev,vec=np.linalg.eigh(H/(sv[:,None]*sv[None,:]));seed=np.abs(vec[:,0]/sv);seed*=.02/max(seed);v=np.r_[allF['mass'],seed];assert m.direct(v)[0]<allF['energy'];formed=finish(m,v,dest.with_name('formed.json'),initial_iterations=320,newton_iterations=120);out={'source':'run_vacuum/all_F.json','minimum_phase_eigenvalue':float(ev[0]),'seed_max_x':.02,'formed':formed,'released_energy_Eunit':allF['energy']-formed['energy']};dest.write_text(json.dumps(out,indent=2)+'\n');print({k:formed.get(k) for k in ['scaled_law_error_bound_percent','scaled_density_rebound','scaled_boundary_kpc','density_KKT_max','gradient_max','free_exterior_mass','free_exterior_T_fraction','optimizer']},flush=True)
