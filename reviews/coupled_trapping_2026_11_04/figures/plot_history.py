"""Render recorded conditional trajectories; no scientific rerun."""
import sys,os
sys.dont_write_bytecode=True
os.environ['MPLCONFIGDIR']='/private/tmp/ct09-matplotlib-cache'
import json,csv,math,time,resource
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def main(first,late,png,pdf,table,metadata):
 start=time.monotonic();records=[]
 for name,path in [('Narrow-width reference (32 bins)',first),('Late finite-width continuation (24 bins)',late)]:
  q=Path(path);r=json.loads(q.read_text());m=json.loads((q.parent/'manifest.json').read_text())
  assert m['run']['status']=='completed' and all(r['checks'].values())
  records.append((name,r['case']))
 mu=records[0][1]['mu_GeV'];mC=math.sqrt(.006)/2*mu;gate=.1*.44e-9/mC;pole=math.sqrt(60/(31*.003))
 fig,axes=plt.subplots(2,1,figsize=(10,7.4),sharex=True,gridspec_kw={'height_ratios':[1,1.2]})
 palette=['#406b8c','#b65f31']
 for (label,run),color in zip(records,palette):
  h=run['history'];t=np.array([p['Tc_over_mu'] for p in h]);lo=np.array([p['x_inner'] for p in h]);hi=np.array([p['x_outer'] for p in h]);x=np.array([p['x_minimum'] for p in h]);Y=np.array([p['Y_charged'] for p in h])
  axes[0].plot(t,x,color=color,lw=1.8,label=label);axes[0].fill_between(t,lo,hi,color=color,alpha=.15)
  axes[1].plot(t,Y/gate,color=color,lw=1.9,label=label)
 axes[0].axhline(pole,color='#67645e',ls='--',lw=1,label='Tree scalar resonance')
 axes[1].axhline(1,color='#5c7545',ls='--',lw=1.5,label='10% dark-matter allowance')
 axes[0].set_ylabel('Field X / μ');axes[1].set_ylabel('Charged yield / allowed yield')
 axes[1].set_yscale('log');axes[1].set_ylim(.5,2e9)
 for ax in axes:
  ax.set_xscale('log');ax.grid(alpha=.2,which='major');ax.spines[['top','right']].set_visible(False)
 axes[1].set_xlim(.005,min(p['Tc_over_mu'] for _,r in records for p in r['history'])*.85)
 axes[1].set_xlabel('Momentum temperature $T_c / \\mu$  (cooling →)')
 axes[0].legend(loc='lower left',fontsize=8,frameon=False)
 axes[1].legend(loc='upper right',fontsize=8,frameon=False)
 fig.suptitle('Vacuum capture succeeds in these closures; heavy relic removal falls short',fontsize=13,y=.98)
 fig.text(.5,.935,'Pole-aligned leading candidate: e = 0.003, μ = 2 × 10⁶ GeV',ha='center',fontsize=10)
 fig.text(.5,.012,'Conditional histories: empty gaugino bath, absorbing parent exits; full statistical and delayed-parent dynamics uncomputed.',ha='center',fontsize=8,color='#555555')
 fig.tight_layout(rect=(0,.035,1,.91));fig.savefig(png,dpi=180);fig.savefig(pdf)
 with open(table,'w',newline='') as stream:
  writer=csv.writer(stream);writer.writerow(['history','Tc_over_mu','x_inner','x_outer','x_minimum','Y_charged','Y_over_gate'])
  for label,run in records:
   for p in run['history']:writer.writerow([label,p['Tc_over_mu'],p['x_inner'],p['x_outer'],p['x_minimum'],p['Y_charged'],p['Y_charged']/gate])
 result=dict(claim_id='CT09_RECORDED_HISTORY_FIGURE',checks=dict(completed_inputs=True,positive_gate=gate>0),charged_gate=gate,mu_GeV=mu,inputs=[first,late],scope='Figure of conditional recorded histories only; different radial resolutions are explicitly labelled.',runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 Path(metadata).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main(*sys.argv[1:])
