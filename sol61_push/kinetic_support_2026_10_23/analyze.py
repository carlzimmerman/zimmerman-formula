import json,sys,numpy as np
from pathlib import Path
from scipy.stats import ks_2samp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
b=Path(__file__).parent;out=Path(sys.argv[1]);names=['dynamic32','dynamic48','dynamic64','particles48','timestep32','dilation32','dilation48','box72','long_equilibrium','long_dilation'];data={};summary={}
for name in names:
 r=json.loads((b/name/'result.json').read_text());data[name]=r;a=r['rows'];late=[d for d in a if d['t']>.75*a[-1]['t']];rad=np.linalg.norm(np.array(r['final_x']),axis=1)
 summary[name]=dict(reason=r['reason'],time=a[-1]['t'],r50_final=a[-1]['r50'],r50_late_min=min(d['r50'] for d in late),r50_late_max=max(d['r50'] for d in late),r10_final=a[-1]['r10'],shape_final=a[-1]['shape_ratio'],max_energy_error=r['max_energy_error'],field_cell=r['field_cell'],particles=r['particles'],central_aperture_counts={str(q):int(sum(rad<q)) for q in [.25,.5,1,2]})
comparisons={}
for one,two in [('dynamic32','timestep32'),('dynamic48','particles48'),('particles48','dynamic64'),('particles48','box72')]:
 r1=np.linalg.norm(np.array(data[one]['final_x']),axis=1);r2=np.linalg.norm(np.array(data[two]['final_x']),axis=1);comparisons[one+' vs '+two]=dict(relative_r50=float(np.median(r2)/np.median(r1)-1),radial_CDF_distance=float(ks_2samp(r1,r2).statistic))
fam=json.loads((b/'family/result.json').read_text());ref=json.loads((b/'refinement/result.json').read_text());sp=json.loads((b/'spectrum_v2/result.json').read_text());gr=json.loads((b/'growth_v2/result.json').read_text());vv=json.loads((b/'virial/result.json').read_text())
fig,ax=plt.subplots(2,2,figsize=(10,7),constrained_layout=True)
for K in [.01,.025,.05,.1]:
 rows=[d for d in fam if d['K']==K];ax[0,0].plot([d['M']*130.25798545 for d in rows],[d['r50']*.44042213 for d in rows],'o-',label='K='+str(K))
ax[0,0].set(xlabel='Supplied mass [million Msun]',ylabel='Equilibrium half-mass radius [kpc]',title='Supported families, not a selected mass');ax[0,0].legend(fontsize=8)
for name in ['particles48','dynamic64','box72','long_equilibrium','long_dilation']:
 rows=data[name]['rows'];ax[0,1].plot([r['t']*.01207427 for r in rows],[r['r50']*.44042213 for r in rows],label=name)
ax[0,1].set(xlabel='Elapsed time [Gyr]',ylabel='Half-mass radius [kpc]',title='Free 3D motion; no gas or cosmological expansion');ax[0,1].legend(fontsize=7)
for n in [300,600,900]:
 row=next(d for d in sp if d['n']==n);ax[1,0].plot([d['l'] for d in row['modes']],[d['eigenvalues'][0] for d in row['modes']],'o-',label='radial cells '+str(n))
ax[1,0].axhline(0,color='k',lw=.7);ax[1,0].set(xlabel='Spherical harmonic l',ylabel='Minimum density-energy curvature',title='Dipole approaches translation zero mode');ax[1,0].legend(fontsize=7)
for d in [fam[0],fam[4],fam[8],fam[12]]:
 ax[1,1].plot(np.array(d['r'])*.44042213,np.array(d['rho']),label='K='+str(d['K']))
ax[1,1].set(xlim=(0,2),xlabel='Radius [kpc]',ylabel='Dimensionless cold density',title='Finite continuum centres at M=5.48 million Msun');ax[1,1].legend(fontsize=8)
fig.savefig(out.parent/'summary.png',dpi=160)
res=dict(dynamics=summary,comparisons=comparisons,equilibrium_refinement=[{k:v for k,v in d.items() if k not in ['r','rho','fields']} for d in ref],max_family_mass_error=max(d['mass_error'] for d in fam),max_family_p=max(d['Pmax'] for d in fam),spectrum_finest=sp[-1],virial_max=max(d['virial_relative'] for d in vv),mass_identity_max=max(d['identity_relative_error'] for d in vv))
json.dump(res,open(out,'w'),indent=2);print(json.dumps(comparisons,indent=2));print(json.dumps(summary,indent=2))
