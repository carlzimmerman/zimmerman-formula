"""Summary of pinned conditional late-stage results; no new kinetic solution."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,time,resource,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[3]
def main(output):
 start=time.monotonic();base=ROOT/'reviews/collision_completion_2026_11_04';paths=[base/'post_memory/run_future001/result.json',base/'memory/run_stage001/result.json',base/'production/run001/result.json'];env,stage,prod=[json.loads(p.read_text()) for p in paths];gate=env['charged_10percent_gate'];charge=[stage['stationary_control_final_Y']/gate,env['endpoint_over_gate']]+[r['charged_future_floor_over_gate'] for r in env['comparisons']];dist=[b['mean_free_streaming_kpc']/1000 for b in prod['baseline']]
 plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'white'})
 fig,(a,b)=plt.subplots(1,2,figsize=(11.2,4.9),gridspec_kw={'width_ratios':[1.25,1]});fig.suptitle('Computed corrections in the specified late-stage model',fontsize=14,y=.97)
 labels=['Stationary control','Resonance memory','Maximum future cleanup\n(vacuum widths)','Maximum future cleanup\n(fermionic exits blocked)'];colors=['#94a3b8','#3b82a6','#d69540','#b85b42'];a.barh(range(4),[v-.4 for v in charge],left=.4,color=colors,height=.62);a.set_yticks(range(4),labels);a.invert_yaxis();a.set_xscale('log');a.set_xlim(.4,2400);a.axvline(1,color='#a32222',lw=1.4,ls='--');a.set_xlabel('Charged abundance / allowed abundance');a.set_title('Charged particles still exceed the gate',fontsize=11,pad=12)
 for i,v in enumerate(charge):a.text(v*1.12,i,f'{v:,.1f}×',va='center',fontsize=9)
 b.barh(range(2),[v-.0003 for v in dist],left=.0003,color=['#527f83','#836c9d'],height=.47);b.set_yticks(range(2),['Octet decay','Triplet decay']);b.invert_yaxis();b.set_xscale('log');b.set_xlim(.0003,1000);b.axvline(.001,color='#a32222',lw=1.4,ls='--');b.set_xlabel('Mean free-streaming distance [Mpc]');b.set_title('Conditional late photinos are hot',fontsize=11,pad=12)
 for i,v in enumerate(dist):b.text(v*.78,i,f'{v:.1f} Mpc',color='white',ha='right',va='center',fontsize=9)
 fig.subplots_adjust(left=.22,right=.98,top=.80,bottom=.24,wspace=.46)
 fig.text(.02,.08,'Dashed lines: allowed charged abundance (left), 1 kpc coldness target (right).\nConditional fixed-width late model; the photino vertex remains unmatched on shell.\nThese panels do not constitute a common end-to-end cosmological history.',fontsize=8,color='#475569')
 dest=Path(output);fig.savefig(dest.with_name('summary.png'),dpi=180);fig.savefig(dest.with_name('summary.pdf'));plt.close(fig)
 out=dict(claim_id='CC10_PINNED_RESULTS_FIGURE',checks=dict(charge_above_gate=min(charge)>1,conditional_hot=min(dist)>.001),charged_ratios=charge,conditional_mean_free_stream_Mpc=dist,sources=[dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths],runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Visualization of pinned conditional calculations, not a new evolution or total radiation ledger.')
 dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));assert all(out['checks'].values())
if __name__=='__main__':main(sys.argv[1])
