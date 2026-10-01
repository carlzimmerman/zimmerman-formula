"""Render the scale-width ambiguity and the estimator noise comparison."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
base=json.loads((HERE/'run_001/results.json').read_text())
opt=json.loads((HERE/'run_optimization_001/results.json').read_text())
rar=json.loads((HERE/'run_rar_001/results.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(12,5),layout='constrained')
ax=axes[0]; example=base['unknown_width_degeneracy']
B=np.array(example['B_over_a_reference']); w=np.array(example['weights'])
unit=np.sqrt(9.3619e-11*5*3.085677581491367e19)/1000
v=np.linspace(-300,300,1500); x=v/unit
for model,color in zip(example['models'],['#007d83','#c34b32']):
    a=model['scale']; s=np.sqrt(model['width_variance']); u=(B*B+a*B)**.25
    density=np.sum(w[:,None]*(np.exp(-.5*((x[None,:]-u[:,None])/s)**2)
        +np.exp(-.5*((x[None,:]+u[:,None])/s)**2)),axis=0)/(2*s*np.sqrt(2*np.pi)*unit)
    ax.plot(v,density,color=color,lw=2,label=f"a/a₀ = {a:.3f}; width = {s*unit:.1f} km/s")
ax.set(xlabel='Line velocity [km/s]',ylabel='Normalized spectral density [1/(km/s)]',
       title='Same second and fourth moments; different spectra')
ax.legend(fontsize=8,loc='upper right',framealpha=1);ax.grid(alpha=.15)
ax.text(.035,.055,'Constructed source mixture, canonical scale.\nSixth moments separate the two hypotheses.',transform=ax.transAxes,fontsize=8,
        bbox=dict(facecolor='white',edgecolor='none',alpha=.9))
ax=axes[1]
direct=[r for r in base['disk_runs'] if r['scale']==1 and r['broadening']=='gaussian']
ax.plot([r['psf_sigma_over_r_reference'] for r in direct],[r['sigma_scale_at_10000_photons'] for r in direct],
        marker='o',color='#b45839',label='Q: original correction')
ax.plot([r['psf_sigma'] for r in opt['full_resolution']],
        [r['scale_tests'][0]['sigma_at_10000_photons'] for r in opt['full_resolution']],
        marker='s',color='#007d83',label='Q: optimized weights')
rr=[r for r in rar['rows'] if r['scale']==1]
ax.plot([r['psf_sigma'] for r in rr],[r['local_sigma_RAR_scale_at_10000_photons'] for r in rr],
        marker='^',color='#7b6aab',label='RAR: positive source weights')
ax.set(yscale='log',xlabel='Spatial mixing width / reference radius',ylabel='Scale standard error at 10,000 expected photons',
       title='Choosing the observable avoids an unstable inverse')
ax.grid(alpha=.15);ax.legend(fontsize=8,loc='upper left')
ax.text(.035,.45,'Synthetic disk; source and instrument maps known.\nPoisson noise only; not an empirical forecast.',transform=ax.transAxes,fontsize=8)
fig.savefig(HERE/'stage_results.png',dpi=170)
print(HERE/'stage_results.png')
