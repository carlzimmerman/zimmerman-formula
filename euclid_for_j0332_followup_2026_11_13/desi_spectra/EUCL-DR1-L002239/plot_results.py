from pathlib import Path
import json,numpy as np,os
os.environ['MPLCONFIGDIR']='/private/tmp/forj0332-mpl'
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent;r=np.load(P/'run_01/residuals.npz');result=json.loads((P/'run_01/result.json').read_text());fig,ax=plt.subplots(2,1,figsize=(14,7),sharex=True)
for band,color in [('b','tab:blue'),('r','tab:orange'),('z','tab:red')]:
 w=r[band+'_w'];f=r[band+'_f'];n=r[band+'_n'];mod=r[band+'_mod'];res=r[band+'_res'];v=r[band+'_valid'];ax[0].plot(w,f,color=color,lw=.4,alpha=.55,label=band+' data');ax[0].plot(w,mod,color='black',lw=.6);ax[1].plot(w,np.where(v,res/n,np.nan),color=color,lw=.4)
ax[0].legend(ncol=3);ax[0].set_ylabel('Viewer flux units');ax[0].set_title('EUCL-DR1-L002239: actual DESI data and embedded Redrock foreground model');ax[1].set_ylim(-6,6);ax[1].set_ylabel('Residual / viewer noise');ax[1].set_xlabel('Observed vacuum wavelength (Å)');ax[1].axhline(0,color='black',lw=.5);fig.tight_layout();fig.savefig(P/'spectrum_diagnostic.png',dpi=150);plt.close(fig)
peak=result['strongest_diagnostic_peaks'][0];z=peak['z'];C=json.loads((P/'contract.json').read_text());fig,axes=plt.subplots(1,4,figsize=(14,3));checks={}
for a,(group,lines) in zip(axes,C['groups_vacuum_A'].items()):
 lam=lines[-1]*(1+z);seen=[]
 for band,color in [('b','tab:blue'),('r','tab:orange'),('z','tab:red')]:
  w=r[band+'_w'];valid=r[band+'_valid'];q=(abs(w-lam)<25);q&=valid
  if q.sum():
   a.plot(w[q]-lam,r[band+'_res'][q],color=color,label=band);a.fill_between(w[q]-lam,-r[band+'_n'][q],r[band+'_n'][q],color=color,alpha=.15);seen.append(band)
 a.axvline(0,color='black',lw=.5);a.set_title(group);a.set_xlabel('Δλ (Å)');checks[group]={'observed_line_A':lam,'cameras_covering_unmasked_window':seen}
fig.suptitle(f'Highest subthreshold peak z={z:.4f}: NOT a source-redshift candidate');fig.tight_layout();fig.savefig(P/'subthreshold_peak.png',dpi=150);plt.close(fig)
overlap={}
for a,b in [('b','r'),('r','z')]:
 wa=r[a+'_w'];wb=r[b+'_w'];valid=r[a+'_valid']&(wa>=wb.min())&(wa<=wb.max());nb=np.interp(wa,wb,r[b+'_n']);fb=np.interp(wa,wb,r[b+'_f']);valid&=np.interp(wa,wb,r[b+'_valid'].astype(float))>.99;diff=(r[a+'_f']-fb)/np.sqrt(r[a+'_n']**2+nb**2);overlap[a+b]={'n':int(valid.sum()),'median_normalized_difference':float(np.median(diff[valid])),'robust_scatter':float(1.4826*np.median(abs(diff[valid]-np.median(diff[valid]))))}
(P/'camera_checks.json').write_text(json.dumps(dict(subthreshold_peak=checks,overlaps=overlap),indent=2));print(overlap)
