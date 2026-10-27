"""Do not confuse direct parent radiation with a successful upward cascade."""
import argparse,json
from pathlib import Path
import numpy as np
from vertex import vertex,equal_resonance
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();d=json.loads(Path('nonlinear_cascade_2026_10_25/run_triad/results.json').read_text());rho=d['rhoT'];u=d['uT'];kappa=.0006995338357181399;c=1814.398688540639;g=1716.802731965808;tdyn=55.93636549117685;rows=[]
for row in d['rows']:
 q=row['q'];R=4*np.pi/q;vol=R**3/3;v=vertex(*equal_resonance(q,rho,u,kappa),rho,u,kappa,vol);A=v['A'];w=v['omega'];N=.1**2*rho**2*vol/(64*A[0]**2);tau=row['coherent_transfer_time_Myr']/tdyn;x=2*w[2]*R/c;F=3*(np.sin(x)-x*np.cos(x))/x**3;gamma3=32*g*g*w[2]**3/c**3*F*F*N*tau;f=row['max_daughter_energy_fraction'];bound=min(row['escaped_fraction'],10*gamma3*A[2]**4*f*f);x0=2*w[0]*R/c;F0=3*(np.sin(x0)-x0*np.cos(x0))/x0**3;gamma0=32*g*g*w[0]**3/c**3*F0*F0;half=tdyn/(4*gamma0*A[0]**4*N)
 rows.append({'q':q,'total_escaped_fraction':row['escaped_fraction'],'upper_bound_daughter_escaped_fraction':float(bound),'direct_parent_only_half_loss_time_Myr':float(half),'interpretation':'A high total escaped fraction at this elapsed time does not establish an upward cascade; parents were populated initially in this local test.'})
out={'rows':rows,'scope':'Bounds inside the weak resonant envelope model only. The daughter bound uses recorded maximum daughter occupation over5 normalized coupling times; no actual infall population is inferred.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
