"""Render declared passing witnesses and separated upper transition scales."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

BASE=Path(__file__).resolve().parent
d=json.loads((BASE/'mw/summary.json').read_text())
fig,axs=plt.subplots(2,1,figsize=(9.5,4.8),sharex=True)
green='#147d64';blue='#1766b1';red='#bd423b'
for ax,foot,name in zip(axs,['canonical','alt'],['Canonical','Alternate']):
    r=d['footings'][foot];upper=r['MW_production_upper_supremum'];fine=r['MW_selected_higher_resolution_upper_edge'];ca=r['Cassini_onset']
    ax.axvspan(ca,.76,color=blue,alpha=.14)
    for lo,hi in r['transition_pass_interval_closed_cover']:
        ax.plot([lo,hi],[.42,.42],color=green,lw=8,solid_capstyle='butt')
    ax.scatter(r['refined_small_epsilon_passing_witnesses'],[.42]*len(r['refined_small_epsilon_passing_witnesses']),c=green,s=40,zorder=5)
    ax.axvspan(fine,upper,color='#888888',alpha=.35)
    ax.axvline(upper,color=green,lw=1.5,ls='--')
    ax.axvline(ca,color=blue,lw=1.5)
    ax.annotate('',xy=(ca,.66),xytext=(upper,.66),arrowprops=dict(arrowstyle='<->',lw=1.3,color=red))
    ax.text((upper+ca)/2,.73,'No overlap',ha='center',color=red,fontsize=10)
    ax.text(upper-.008,.12,f'MW upper ≈ {fine:.3f}',ha='right',color=green,fontsize=10)
    ax.text(ca+.01,.12,f'Cassini ≥ {ca:.4f}',ha='left',color=blue,fontsize=10)
    ax.text(.105,.87,name,fontsize=12,fontweight='bold',va='top')
    ax.set_ylim(0,1);ax.set_yticks([]);ax.grid(axis='x',alpha=.18)
    for edge in ['top','left','right']:ax.spines[edge].set_visible(False)
axs[-1].set_xlim(.1,.76);axs[-1].set_xlabel(r'Common Gaussian width fraction $\epsilon$')
fig.suptitle('Corrected Gaussian: Milky Way and Cassini require separated widths',fontsize=13,y=.98)
handles=[Line2D([],[],color=green,marker='o',ls='',label='Refined MW passing examples'),Line2D([],[],color=green,lw=6,label='Mapped MW upper transition'),Patch(facecolor=blue,alpha=.14,label='Numerical Cassini passing branch')]
fig.legend(handles=handles,loc='lower center',ncol=3,frameon=False,fontsize=8.5,bbox_to_anchor=(.5,.045))
fig.text(.5,.018,'Lower MW windows are not fully mapped. Endpoint spread is numerical; no common window was found.',ha='center',fontsize=8.5,color='#555555')
fig.subplots_adjust(top=.90,bottom=.22,hspace=.18,left=.07,right=.98)
fig.savefig(BASE/'epsilon_windows.png',dpi=180)
fig.savefig(BASE/'epsilon_windows.pdf')
plt.close(fig)
