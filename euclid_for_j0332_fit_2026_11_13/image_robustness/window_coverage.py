"""Ray coverage of released source segmentation, independent of source fitting."""
import argparse,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import AsinhNorm
from astropy.io import fits
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE))
from lens_models import AqualLens,sie_parameters,sie_deflection


def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    src=fits.getdata(BASE/'inputs/dataset/segmentation/source_binary.fits')>0
    artifact=fits.getdata(BASE/'inputs/dataset/segmentation/artefact_binary.fits')
    with fits.open(BASE/'inputs/dataset/Tile102034383RA0532498193624DECNEG0359643115588.fits') as hd:
        noise=np.asarray(hd['VIS_RMS'].data)
    jj,ii=np.meshgrid(np.arange(noise.shape[1]),np.arange(noise.shape[0]));X=(jj-49.5)*.1;N=(ii-49.5)*.1
    info=json.loads((BASE/'inputs/dataset/info.json').read_text())
    mask=((-N-info['mask_centre'][0])**2+(X-info['mask_centre'][1])**2<info['mask_radius']**2)&(artifact==0)&(noise>0)
    arc=mask&src
    assert arc.sum()>0
    result=json.loads((BASE/'image_robustness/run_02/result.json').read_text())
    models=[r for r in result['optimizations'] if r['name']==result['best_free_name']]
    med=[r for r in result['optimizations'] if r['fixed_logmass']==11.8310873126]
    models.append(max(med,key=lambda x:x['score_image_and_shear_prior']))
    models.extend(r for r in result['optimizations'] if r['name'] in ['fixed_SED_upper_1sigma','fixed_SED_upper_2sigma'])
    # Same reference-shear low-mass case isolates footprint from nuisance optimization.
    models.append({'name':'SED_mass_with_reference_shear','parameters':[11.8310873126,-.020224029220632385,-.15843063089888157,0.]})
    lens=AqualLens();records=[]
    for model in models:
        m,g1,g2,_=model['parameters'];bu=[];bv=[]
        for di in [-.025,.025]:
            for dj in [-.025,.025]:
                ax,an=lens.deflection(X+dj,N+di,m,g1,g2)
                bu.append((X+dj-ax)[arc]);bv.append((N+di-an)[arc])
        bu,bv=np.concatenate(bu),np.concatenate(bv)
        rec={'name':model['name'],'logmass':m,'shear':[g1,g2],
             'beta_u_quantiles':dict(zip(['min','p01','p05','median','p95','p99','max'],map(float,np.quantile(bu,[0,.01,.05,.5,.95,.99,1])))),
             'beta_v_quantiles':dict(zip(['min','p01','p05','median','p95','p99','max'],map(float,np.quantile(bv,[0,.01,.05,.5,.95,.99,1])))),
             'source_support_coverage':{}}
        for label,ns,h in [('original_25_h004',25,.04),('expanded_33_h004',33,.04),('wide_33_h006',33,.06)]:
            dist=np.maximum(abs(bu+.03),abs(bv+.05))
            rec['source_support_coverage'][label]={'fraction_within_outer_nodes':float(np.mean(dist<=(ns-1)*h/2)),
                  'fraction_with_any_bilinear_support':float(np.mean(dist<(ns+1)*h/2)),
                  'outside_bilinear_support_rays':int(np.sum(dist>=(ns+1)*h/2))}
        records.append(rec)
    pos=np.asarray(json.loads((BASE/'inputs/dataset/positions.json').read_text())['arguments']['values']['array'])
    px,pn=pos[:,1],-pos[:,0]
    def position_stat(name,params=None):
        ax,an=sie_deflection(px,pn,**sie_parameters()) if params is None else lens.deflection(px,pn,*params[:3])
        beta=np.column_stack([px-ax,pn-an]);d=np.linalg.norm(beta[:,None,:]-beta[None,:,:],axis=-1)
        return {'name':name,'parameters':params,'beta_west_north_arcsec':beta.tolist(),'max_pair_separation_arcsec':float(d.max()),'passes_03':bool(d.max()<=.3),'passes_05':bool(d.max()<=.5)}
    pos_stats=[position_stat('fixed_catalogue_SIE')]
    pos_stats.extend(position_stat('wide_'+x['name'],x['parameters']) for x in result['optimizations'])
    r1=json.loads((BASE/'image_robustness/run_01/result.json').read_text())
    for c in r1['cases']:
        for x in c['optimizations']:
            if x['a0_ratio']==1.:pos_stats.append(position_stat(c['case']+'_'+x['name'],x['parameters']))
    # Preserve distinct unconstrained branches visually, without suppressing the low-mass result.
    images=np.load(BASE/'image_robustness/run_02/images_sources.npz')
    template=np.asarray(fits.getdata(BASE/'inputs/results/model.fits','VIS_GALAXY_0'))
    chosen=[next(x for x in result['optimizations'] if x['name']=='free_start_high'),
            next(x for x in result['optimizations'] if x['name']=='free_start_low'),
            max(med,key=lambda x:x['score_image_and_shear_prior'])]
    fig,axes=plt.subplots(3,4,figsize=(15,10),constrained_layout=True)
    ext=[-5,5,-5,5]
    for row,fit in enumerate(chosen):
        name=fit['name'];model=np.full(noise.shape,np.nan);model[mask]=images[name+'_model_valid']
        nuisance=fit['fit']['lens_amplitude']*template+fit['fit']['sky']
        observed=np.asarray(images['data'])-nuisance;source_model=model-nuisance
        vmax=max(float(np.nanpercentile(np.maximum(observed[mask],0),99.3)),1e-6)
        norm=AsinhNorm(linear_width=vmax/10,vmin=-vmax*.15,vmax=vmax)
        axes[row,0].imshow(observed,origin='lower',extent=ext,cmap='magma',norm=norm)
        axes[row,1].imshow(source_model,origin='lower',extent=ext,cmap='magma',norm=norm)
        im=axes[row,2].imshow((images['data']-model)/noise,origin='lower',extent=ext,cmap='RdBu_r',vmin=-5,vmax=5)
        coef=images[name+'_source'];peak=max(float(abs(coef).max()),1e-10)
        sm=axes[row,3].imshow(coef,origin='lower',extent=[-1.02,.96,-1.04,.94],cmap='RdBu_r',vmin=-peak,vmax=peak)
        for col in range(3):axes[row,col].set_xlim(-2.6,2.2);axes[row,col].set_ylim(-2.7,2.1)
        for col in range(4):axes[row,col].set_xlabel('West (arcsec)');axes[row,col].set_ylabel('North (arcsec)')
        axes[row,0].text(.02,.97,f"{name}\nlog M={fit['parameters'][0]:.6f}\nchi2={fit['fit']['chi2']:.1f}",transform=axes[row,0].transAxes,va='top',color='white',fontsize=9)
        fig.colorbar(im,ax=axes[row,2],shrink=.75,label='residual / RMS')
        fig.colorbar(sm,ax=axes[row,3],shrink=.75,label='source coefficient')
    for col,title in enumerate(['Data minus fitted lens/sky','Modeled source image','Pixel residual','Reconstructed source (separate scales)']):axes[0,col].set_title(title,fontsize=10)
    fig.suptitle('Wide source window: unconstrained high-mass, low-bound, and fixed-SED branches\nGaussian source coefficients can be negative; no image-position association gate applied',fontsize=12)
    fig.savefig(out/'wide_branch_comparison.png',dpi=180);plt.close(fig)
    r={'assertion_tested':'For 2x2 subpixel rays through released source-segmentation pixels inside the fitted image mask, measure geometric source-basis coverage at the wide-window optimized parameters and a reference low-mass case.',
       'source_segmentation_pixels_within_fit_mask':int(arc.sum()),'rays_per_model':int(4*arc.sum()),'models':records,'released_positions_pipeline_south_west':pos.tolist(),'source_position_statistics':pos_stats,
       'non_claims':['Released source segmentation is a diagnostic selection, not independent data or all relevant PSF-contributing pixels.','Geometric support says only that source coefficients can contribute; it does not remove Gaussian source-prior regularization or prove fit adequacy.','Not a theorem excluding source truncation at arbitrarily faint image pixels.']}
    (out/'result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
