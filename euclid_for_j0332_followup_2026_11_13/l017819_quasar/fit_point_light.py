"""L017819 photometric deblending: one Sersic lens and two independent PSFs.

This estimates light and quasar astrometry, not a gravitational mass model.
No quasar flux ratio or released four-position gate is imposed.
"""
import argparse
import json
import sys
from pathlib import Path
sys.dont_write_bytecode = True
import numpy as np
from astropy.io import fits
from scipy.ndimage import map_coordinates
from scipy.optimize import least_squares, lsq_linear
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sys.path.insert(0, str(BASE / 'light_shapes'))
from fit_light_shapes import Renderer, physical
DATA = HERE / 'inputs/dataset/Tile102140883RA2311901412524DEC0441637579847.fits'
PIX = .1
YY, XX = np.indices((100, 100))
X, Y = (XX-49.5)*PIX, (YY-49.5)*PIX
# x_lens,y_lens,ln(Re_major),ln(n),q,phi; x_A,y_A,x_B,y_B
LOW = np.array([-.45,-.25,np.log(.15),np.log(.7),.25,-np.pi, .15,-.4,-1.4,.35])
HIGH = np.array([.15,.35,np.log(3.),np.log(9.),.99,np.pi, .75,.15,-.75,.95])

def point(psf, x, y, order=3):
    p = np.asarray(psf,float) / np.sum(psf)
    coordinates = [(Y-y)/PIX+(p.shape[0]-1)/2, (X-x)/PIX+(p.shape[1]-1)/2]
    v = map_coordinates(p, coordinates, order=order, mode='constant', cval=0.)
    return v / np.sum(v)

def model_and_linear(p, data, noise, mask, renderer, psf, order=3):
    components = np.stack([renderer.render(p[:6]), point(psf,*p[6:8],order),
                           point(psf,*p[8:10],order), np.ones_like(data)])
    A = (components[:,mask]/noise[mask]).T
    y = data[mask]/noise[mask]
    coef = np.linalg.lstsq(A,y,rcond=None)[0]
    if np.any(coef[:3] < 0):
        coef = lsq_linear(A,y,bounds=([0,0,0,-np.inf],[np.inf]*4),tol=1e-11).x
    model = np.einsum('k,kij->ij',coef,components)
    return (model[mask]-data[mask])/noise[mask],coef,model,components

def fit(data,noise,mask,psf,start,fixed_n=None,order=3,max_nfev=130):
    p0 = np.clip(np.array(start,float),LOW+1e-7,HIGH-1e-7)
    free = np.array([i for i in range(10) if i!=3 or fixed_n is None])
    if fixed_n is not None: p0[3] = np.log(fixed_n)
    renderer = Renderer(psf)
    def unpack(z):
        p = p0.copy(); p[free] = z; return p
    def residual(z):
        return model_and_linear(unpack(z),data,noise,mask,renderer,psf,order)[0]
    opt = least_squares(residual,p0[free],bounds=(LOW[free],HIGH[free]),
                        x_scale='jac',diff_step=2e-4,ftol=3e-7,xtol=3e-7,
                        gtol=2e-6,max_nfev=max_nfev)
    p = unpack(opt.x)
    residuals,coef,model,components = model_and_linear(p,data,noise,mask,renderer,psf,order)
    fine = model_and_linear(p,data,noise,mask,Renderer(psf,fine=True),psf,order)
    dg = (fine[2]-model)[mask]/noise[mask]
    cov = np.zeros((10,10)); cov[np.ix_(free,free)] = np.linalg.pinv(opt.jac.T@opt.jac,rcond=1e-11)
    return dict(parameters=p.tolist(),physical=physical(p[:6]),linear_coefficients=coef.tolist(),
                coefficient_order=['infinite_lens_flux','quasar_A_flux','quasar_B_flux','sky'],
                quasar_A_west_north_arcsec=p[6:8].tolist(),quasar_B_west_north_arcsec=p[8:10].tolist(),
                separation_arcsec=float(np.linalg.norm(p[6:8]-p[8:10])),
                chi2=float(residuals@residuals),n_pixels=int(mask.sum()),
                success=bool(opt.success),message=str(opt.message),nfev=int(opt.nfev),
                fixed_n=fixed_n,point_interpolation_order=order,
                local_covariance=cov.tolist(),
                fine_integration_check=dict(max_RMS=float(np.max(abs(dg))),rms_RMS=float(np.sqrt(np.mean(dg*dg))),
                                            delta_chi2=float(fine[0]@fine[0]-residuals@residuals)),
                model=model,components=components,mask=mask)

def compact(r): return {k:v for k,v in r.items() if k not in ['model','components','mask']}

def main(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    artifact=fits.getdata(HERE/'inputs/dataset/segmentation/artefact_binary.fits')>0
    radius=np.hypot(X+.15,Y-.05)
    rows=[];arrays={};checks={};best_by_band={}
    start=np.array([-.15,.05,np.log(.7),np.log(4.),.65,.95, .45,-.15,-1.1,.65])
    with fits.open(DATA) as hd:
        for band in ['VIS','NIR_H','HSC_Z']:
            data=np.array(hd[band+'_BGSUB'].data,float);noise=np.array(hd[band+'_RMS'].data,float)
            psf=np.array(hd[band+'_PSF'].data,float)
            valid=np.isfinite(data)&np.isfinite(noise)&(noise>0)&~artifact
            mask=valid&(radius<3.)
            arrays[band+'_data']=data;arrays[band+'_noise']=noise
            checks[band]={'raw_PSF_sum':float(psf.sum()),'PSF_min':float(psf.min()),
                          'BUNIT':hd[band+'_BGSUB'].header.get('BUNIT'),
                          'MAGZERO':float(hd[band+'_BGSUB'].header['MAGZERO'])}
            # Finer galaxy quadrature generates the injected noiseless control.
            if band=='VIS':
                fine=Renderer(psf,fine=True);truth=start.copy();truth[2]=np.log(.8);truth[3]=np.log(3.7)
                synthetic=20*fine.render(truth[:6])+5*point(psf,*truth[6:8])+3*point(psf,*truth[8:10])+.001
                recovery=fit(synthetic,np.full_like(noise,.01),mask,psf,start,max_nfev=180)
                delta=np.array(recovery['parameters'])-truth
                checks['synthetic_finer_quadrature_recovery']={'truth':truth.tolist(),'fit':compact(recovery),'parameter_errors':delta.tolist()}
                assert recovery['success'] and max(abs(delta[:2]))<.002 and max(abs(delta[2:6]))<.015 and max(abs(delta[6:]))<.002
                # Integer shifts preserve each measured empirical PSF exactly.
                integer=point(psf,.05,.05);p=psf/psf.sum()
                direct=np.zeros((100,100));direct[40:61,40:61]=p
                checks['integer_PSF_shift_max_abs']=float(np.max(abs(integer-direct)))
                assert checks['integer_PSF_shift_max_abs']<1e-10
            n4=fit(data,noise,mask,psf,start,fixed_n=4.)
            free_starts=[np.array(n4['parameters']),start.copy()]
            free_starts[1][3]=np.log(2.)
            freefits=[fit(data,noise,mask,psf,s) for s in free_starts]
            best=min(freefits,key=lambda v:v['chi2'])
            best['all_start_solutions']=[compact(v) for v in freefits]
            best_by_band[band]=best
            variants=[('free_n_radius3',best),('n4_radius3',n4)]
            if band=='VIS':
                variants.append(('free_n_radius2',fit(data,noise,valid&(radius<2.),psf,best['parameters'])))
                variants.append(('free_n_linear_PSF',fit(data,noise,mask,psf,best['parameters'],order=1)))
            for name,result in variants:
                result.update(band=band,variant=name)
                rows.append(compact(result));arrays[band+'_'+name+'_model']=result['model'];arrays[band+'_'+name+'_mask']=result['mask']
                arrays[band+'_'+name+'_components']=result['components']
                print(json.dumps({'band':band,'variant':name,'physical':result['physical'],'chi2':result['chi2'],
                                  'separation':result['separation_arcsec'],'success':result['success'],'nfev':result['nfev']}),flush=True)
            (output/'progress.json').write_text(json.dumps({'checks':checks,'fits':rows},indent=2)+'\n')
    fig,axes=plt.subplots(3,3,figsize=(12,11),constrained_layout=True)
    for j,band in enumerate(['VIS','NIR_H','HSC_Z']):
        best=best_by_band[band];data=arrays[band+'_data'];noise=arrays[band+'_noise'];model=best['model'];mask=best['mask']
        stretch=max(np.percentile(data[mask],99)/8,1e-12)
        axes[0,j].imshow(np.arcsinh(data/stretch),origin='lower',extent=[-5,5,-5,5],cmap='magma')
        axes[1,j].imshow(np.arcsinh(model/stretch),origin='lower',extent=[-5,5,-5,5],cmap='magma')
        im=axes[2,j].imshow(np.where(mask,(data-model)/noise,np.nan),origin='lower',extent=[-5,5,-5,5],cmap='RdBu_r',vmin=-4,vmax=4)
        axes[0,j].set_title(band+' raw image')
        axes[1,j].set_title('Two PSFs + Sersic; n={:.2f}, Re={:.2f}″'.format(best['physical']['n'],best['physical']['Re_geometric_mean_arcsec']))
        axes[2,j].set_title('Residual / released RMS');fig.colorbar(im,ax=axes[2,j],shrink=.7)
        for ax in axes[:,j]:ax.set_xlim(-2.4,2.1);ax.set_ylim(-2.2,2.3);ax.set_xlabel('West (arcsec)');ax.set_ylabel('North (arcsec)')
    fig.savefig(output/'point_light_fits.png',dpi=160);plt.close(fig)
    result={'assertion_tested':'Photometric feasibility of Sersic lens + two independent point sources in L017819',
            'fits':rows,'checks':checks,'bounds':{'lower':LOW.tolist(),'upper':HIGH.tolist()},
            'parameter_order':['x_lens','y_lens','ln_Re_major','ln_n','q','phi_west_radians','x_A','y_A','x_B','y_B'],
            'non_claims':['No gravity model, stellar mass, IMF, source association gate or flux-ratio lensing constraint fitted.',
                          'Reported local covariances are conditional on diagonal RMS, single-Sersic light and supplied finite PSFs.',
                          'Different bands are fitted independently; PSF normalization/support and quasar-host contamination remain systematic uncertainties.',
                          'A completed optimizer is not an accepted physical lens model.']}
    (output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    np.savez_compressed(output/'models.npz',**arrays)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);main(parser.parse_args().output)
