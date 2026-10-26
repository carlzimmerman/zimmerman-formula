"""Scientific figure from sealed numerical analysis, no new model fit."""
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/cct021_mpl');os.environ.setdefault('MPLBACKEND','Agg')
import argparse,json,hashlib,resource
from pathlib import Path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True);src=P/'analysis_001/result.json';d=json.loads(src.read_text());fig,axs=plt.subplots(3,2,figsize=(11,10.5),sharex='col');notes=[]
 def lineage(path):
  folders=[]
  while True:
   folders.append(path);dd=json.loads((path/'result.json').read_text())
   if 'resume_origin' not in dd:break
   path=Path(dd['resume_origin']['parent'])
  return list(reversed(folders))
 for col,gal in enumerate(['Draco','Sextans']):
  candidates=[name for name,r in d['runs'].items() if r['galaxy']==gal and r['ne']==8192 and (ROOT/Path(r['path'])).parent==P];latest=max(candidates,key=lambda name:d['runs'][name]['t']);finepath=ROOT/d['runs'][latest]['path'];coarsepath=P.parent/'cold_pre_stellar_settling_2026_10_25'/(gal+'_base_continued');dd=json.loads((finepath/'result.json').read_text());tu=dd['units']['t_Myr'];ax=axs[0,col];massax=axs[1,col];bottom=axs[2,col]
  tracks=[(coarsepath,'0.6','coarse4096'),(finepath,'#1764ab','fine8192')];higher=P/(gal+'_higher_IC')
  if higher.name in d['runs']:tracks.append((higher,'#138a64','independent16384'))
  for folder,color,label in tracks:
   names=[p.name for p in lineage(folder)];rr={round(r['t'],10):r for r in d['rows'] if r['run'] in names and r['footing']=='canonical' and r['beta']==0 and r['snapshot_numerically_valid']};rr=[rr[t] for t in sorted(rr)]
   if rr:
    for j in range(len(rr[0]['selected_position_population_sigma_kms'])):ax.plot([r['time_Myr'] for r in rr],[r['selected_position_population_sigma_kms'][j] for r in rr],'.-',color=color,label=label+(' tracer'+str(j+1) if len(rr[0]['selected_position_population_sigma_kms'])>1 else ''))
   hist={}
   for pp in lineage(folder):
    for r in json.loads((pp/'result.json').read_text())['history']:
     if r['numerically_valid']:hist[round(r['t'],10)]=r
   hh=[hist[t] for t in sorted(hist)];massax.plot([r['time_Myr'] for r in hh],[r['cold_Mref']*dd['units']['M_Msun']/1e8 for r in hh],color=color,label=label)
   window={}
   for pp in lineage(folder):
    for r in json.loads((pp/'result.json').read_text())['settling']:window[round(r['t'],10)]=r
   ww=[window[t] for t in sorted(window)];
   if ww:bottom.plot([r['t']*tu for r in ww],[max(r['CDF_range'],1e-6) for r in ww],color=color,label=label)
  obs=rr[0]['selected_observed_sigma'];ax.axhline(obs,color='black',ls='--',lw=1,label='selected-data constant sigma');ax.set_title(gal);ax.set_ylabel('LOS support [km/s]');ax.grid(alpha=.2);ax.legend(fontsize=7)
  massax.set_ylabel('Cold mass within reference radius\n[1e8 Msun]');massax.grid(alpha=.2);massax.legend(fontsize=7)
  bottom.axhline(.01,color='black',ls='--',lw=1,label='CDF window limit');bottom.set_yscale('log');bottom.set_ylabel('Trailing CDF range /\ntotal cold mass');bottom.set_xlabel('Elapsed collapse time [Myr]');bottom.grid(alpha=.2);bottom.legend(fontsize=7)
  stop=dd['t']*tu
  for aa in [ax,massax,bottom]:aa.axvline(stop,color='#a33a2b',ls=':',lw=1)
  notes.append(gal+': '+dd['status']+', '+('no qualifying stellar birth' if dd['birth_time'] is None else 'birth T='+str(dd['birth_time'])))
 fig.suptitle('CCT022: continued collapse, inner mass and settling',fontsize=13);fig.text(.06,.02,'\n'.join(notes)+'\nFixed-tracer moments; these are not evolved stellar velocities.\nElapsed time is not a cosmological star-formation date. Mass histories are sampled.\nReference-sphere mass change is redistribution, not escape. CDF is one of three settling tests.\nCoarse curves exclude failed terminal states. Red dotted lines mark the 8192 stops.\nIndependent 16384 runs end before T=2 and have no eligible settling windows.',fontsize=8);fig.tight_layout(rect=[0,.17,1,.95]);fig.savefig(out/'later_collapse.png',dpi=180);plt.close(fig)
 result=dict(scope='plot of sealed analysis only; no model or acceptance change',input_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),matplotlib=matplotlib.__version__,output_sha256=hashlib.sha256((out/'later_collapse.png').read_bytes()).hexdigest(),notes=notes,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);(out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
