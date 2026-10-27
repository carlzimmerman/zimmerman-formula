import argparse,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    root=Path(__file__).parent
    r=json.loads((root/'run_refine/results.json').read_text())['runs']
    q=json.loads((root/'run_quantum/results.json').read_text())['runs']
    fig,axes=plt.subplots(1,2,figsize=(11,4.2),layout='constrained')
    for x,c,label in [(r[3],'#176e9e','No initial circulation'),(r[4],'#d36a31','Initial circulation Ω=0.15')]:
        axes[0].plot([s['time'] for s in x['rows']],[s['field_projection'] for s in x['rows']],color=c,label=label)
    axes[0].axhline(1,color='.5',ls=':',label='Bare source')
    axes[0].set(xlabel='Dimensionless time',ylabel='Self-consistent source-mode amplitude',title='3D coupled mean-field test (4³ cells)')
    axes[0].legend(fontsize=8);axes[0].grid(alpha=.2)
    for i,c in zip([3,4,5],['#7c67ad','#176e9e','#d36a31']):
        x=q[i];axes[1].plot(x['times'],x['excited'],color=c,label=f"Quantum: Δ/Ω = {x['detuning_ratio']:g}")
    axes[1].axhline(1,color='.3',ls=':',label='Factorized mean field')
    axes[1].set(xlabel='Dimensionless time',ylabel='Orbital excited-state population',title='Same electric origin: quantum countercharge mode',ylim=(-.04,1.06))
    axes[1].legend(fontsize=8);axes[1].grid(alpha=.2)
    fig.suptitle('Conservation and energy exchange demonstrated; galaxy separation remains untested',fontsize=12)
    out=Path(a.output);fig.savefig(out.parent/'findings.png',dpi=170)
    out.write_text(json.dumps({'figure':'findings.png','source':'run_refine and run_quantum results; no fitted curves'})+'\n')
if __name__=='__main__':main()
