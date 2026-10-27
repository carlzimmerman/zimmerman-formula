"""Scientific figures from retained actual cube/model diagnostics."""
import argparse,json,os
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output);out.mkdir(exist_ok=True)
    os.environ['MPLCONFIGDIR']=str(out/'mpl_cache')
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import AsinhNorm
    from matplotlib.patches import Rectangle
    z=np.load(HERE/'analysis_run002/arrays.npz');data=z['data'];pred=z['predictions'][0];b=z['blanks'];u=z['U']
    fig,axes=plt.subplots(2,3,figsize=(12.8,7.8),constrained_layout=True)
    for row,(center,marked,title) in enumerate([(-49.44,(-220,-60),'Published southwest extension'),(61.8,(-60,100),'Unclassified guarded positive peak')]):
        k=np.argmin(abs((u[:-1]+u[1:])/2-center));d=data[k:k+2].sum(0);p=pred[k:k+2].sum(0);sd=b[:,k:k+2].sum(1).std(0,ddof=1)
        for col,(im,label) in enumerate([(d,'Actual HALOGAS HR'),(p,'Reconstructed disk + warp + arms'),((d-p)/sd,'Residual / measured blank scatter')]):
            ax=axes[row,col]
            if col<2:
                art=ax.imshow(im,origin='lower',extent=[-300,300,-120,120],cmap='magma',norm=AsinhNorm(linear_width=.002,vmin=0,vmax=.14),aspect='auto')
                cb=fig.colorbar(art,ax=ax,shrink=.84,pad=.02);cb.set_label('Jy km/s per 20×20 arcsec bin',fontsize=8)
            else:
                art=ax.imshow(im,origin='lower',extent=[-300,300,-120,120],cmap='RdBu_r',vmin=-6,vmax=6,aspect='auto')
                cb=fig.colorbar(art,ax=ax,shrink=.84,pad=.02);cb.set_label('Empirical scatter units',fontsize=8)
            ax.add_patch(Rectangle((marked[0]-20,marked[1]-20),40,40,facecolor='none',edgecolor='#36e2db',linewidth=1.5))
            ax.axhline(20,color='white',alpha=.35,lw=.5);ax.axhline(-20,color='white',alpha=.35,lw=.5)
            ax.set_title(label,fontsize=10);ax.set_xlabel('Major offset [arcsec; NE positive]',fontsize=9);ax.set_ylabel('Minor offset [arcsec; SE positive]',fontsize=9)
            ax.text(.02,.98,title+'\nu = %.2f to %.2f km/s'%(u[k]-6.18,u[k+1]+6.18),va='top',transform=ax.transAxes,fontsize=8,color='white' if col<2 else 'black',bbox=dict(facecolor='black' if col<2 else 'white',alpha=.45,edgecolor='none'))
    fig.suptitle('NGC5023: actual brightness, reconstructed full model, and local mismatches',fontsize=13)
    fig.savefig(out/'summary.png',dpi=175);fig.savefig(out/'summary.pdf');plt.close(fig)
    follow=json.loads((HERE/'followup_run001/results.json').read_text());cs=json.loads((HERE/'followup_candidates.json').read_text())['cases']
    fig,ax=plt.subplots(figsize=(13.2,5.5),constrained_layout=True)
    xx=np.arange(len(cs));colors={'HR':'#2b67c1','LR':'#d27215','WHISP':'#2f9359'}
    for offset,name in [(-.22,'HR'),(0.,'LR'),(.22,'WHISP')]:
        r=follow['datasets'][name];rows=r['data']['40arcsec']['boxes'];y=np.array([t['flux_Jy_km_s']-t['blank_mean_Jy_km_s'] for t in rows]);err=np.array([t['blank_scatter_Jy_km_s'] for t in rows]);lo=r['native_operator_model_checks']['1.1']['box_prediction_min'];hi=r['native_operator_model_checks']['1.1']['box_prediction_max']
        ax.vlines(xx+offset,lo,hi,color=colors[name],lw=8,alpha=.25,label=name+' finite model range (76 labels)')
        ax.errorbar(xx+offset,y,yerr=err,fmt='o',ms=4,color=colors[name],capsize=3,lw=1,label=name+' brightness ± blank scatter')
    labels=[]
    for i,c in enumerate(cs):
        x,z0,v=c['center_major_minor_u'];labels.append(('Known SW' if i==0 else 'Box '+str(i+1))+'\n(%g, %g, %g)'%(x,z0,round(v,1)))
    ax.set_xticks(xx,labels,fontsize=8);ax.set_ylabel('40×40 arcsec aperture flux [Jy km/s]');ax.axhline(0,color='0.4',lw=.7);ax.grid(axis='y',alpha=.2)
    ax.set_title('Frozen selected boxes at a common 40 arcsec beam; no fit to older WHISP data',fontsize=12)
    ax.legend(ncol=3,fontsize=8,loc='upper right');fig.suptitle('Empirical scatter bars are not confidence intervals; overlapping blanks and same-instrument systematics remain',fontsize=9)
    fig.savefig(out/'followup.png',dpi=175);fig.savefig(out/'followup.pdf');plt.close(fig)
    (out/'results.json').write_text(json.dumps({'figures':['summary.png','summary.pdf','followup.png','followup.pdf'],'scope':'Descriptive scientific figures; common40 family ranges are finite source/reconstruction sensitivities, not confidence intervals. EarlierWHISP is a reused oldercampaign check, not blinddiscovery.'},indent=2)+'\n')
if __name__=='__main__':main()
