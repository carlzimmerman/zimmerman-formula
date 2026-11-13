"""Bounded, descriptive L002777/SILO790 spectral and source-association audit.

No redshift confirmation or gravity likelihood is claimed.  Local line fits use
the archived SILO foreground-subtracted spectrum, not a new foreground refit.
"""
import argparse
import csv
import json
from pathlib import Path

import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from scipy.optimize import least_squares
from scipy.special import ndtr
from scipy.integrate import quad
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

HERE = Path(__file__).resolve().parent
Z = 0.9713690280914307
OII = np.array([3727.092, 3729.875]) * (1 + Z)  # vacuum Angstrom
C = 299792.458
BITS = {19: 'PARTIALREJECT', 23: 'BRIGHTSKY', 25: 'COMBINEREJ',
        27: 'BADSKYCHI', 28: 'REDMONSTER'}


def serial(x):
    if isinstance(x, (str, int, float, bool)) or x is None:
        return x
    if isinstance(x, (bytes, np.bytes_)):
        return x.decode().strip()
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, np.generic):
        return x.item()
    raise TypeError(type(x))


def line_kernel(wave, sig_inst, centres, velocity, integrated=True):
    """Unit integrated-flux Gaussian, native log pixels, local Gaussian LSF.

    Per-line LSF sigma is interpolated from the actual WDISP array.  The
    integrated-versus-sampled control measures possible pixel-response overlap
    because released WDISP describes the effective coadded resolution.
    """
    widths = np.sqrt(np.interp(centres, wave, sig_inst) ** 2 +
                     (centres * velocity / C) ** 2)
    if integrated:
        lo, hi = wave * 10 ** (-0.00005), wave * 10 ** 0.00005
        return ((ndtr((hi[:, None] - centres) / widths) -
                 ndtr((lo[:, None] - centres) / widths)) / (hi - lo)[:, None])
    return np.exp(-0.5 * ((wave[:, None] - centres) / widths) ** 2) / (np.sqrt(2 * np.pi) * widths)


def fit_line(wave, sig_inst, resid, ivar, use, doublet, integrated=True):
    w, si, y, wt = wave[use], sig_inst[use], resid[use], np.sqrt(ivar[use])
    ref = float(OII.mean())
    bases = OII if doublet else np.array([ref])
    n = len(bases)
    def prediction(p):
        return line_kernel(w, si, bases + p[0], p[1], integrated) @ p[2:2+n] + p[-2] + p[-1] * (w-ref)/30
    def residual(p):
        return (prediction(p) - y) * wt
    lower = [-8., 0.] + [0.] * n + [-np.inf, -np.inf]
    upper = [8., 400.] + [np.inf] * n + [np.inf, np.inf]
    results = []
    for shift in [-3., 0., 3.]:
        for velocity in [10., 80., 180.]:
            start = [shift, velocity] + [3.] * n + [0., 0.]
            r = least_squares(residual, start, bounds=(lower, upper),
                              ftol=1e-11, xtol=1e-11, gtol=1e-10, max_nfev=500)
            results.append(r)
    best = min(results, key=lambda r: float(r.fun @ r.fun))
    p = best.x
    return dict(chi2=float(best.fun @ best.fun), n_pixels=int(use.sum()),
                n_parameters=len(p), nominal_dof=int(use.sum()-len(p)),
                shift_angstrom=float(p[0]), intrinsic_sigma_kms=float(p[1]),
                integrated_fluxes=p[2:2+n].tolist(), baseline=float(p[-2]),
                baseline_change_per_30A=float(p[-1]), parameters=p.tolist(),
                successful_starts=sum(r.success for r in results), starts=len(results),
                best_success=bool(best.success),
                best_worst_start_chi2=[float(min(r.fun@r.fun for r in results)), float(max(r.fun@r.fun for r in results))],
                centres_angstrom=(bases+p[0]).tolist(),
                native_model=prediction(p).tolist(), native_wave=w.tolist())


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    names=['WAVE','FLUX','IVAR','AND_MASK','OR_MASK','MODEL_SILO','IVAR_RESCALED','RESIDUAL_FLUX']
    a={x:np.fromfile(HERE/f'silo790_{x}.bin',dtype='>i4' if 'MASK' in x else '>f4') for x in names}
    for value in a.values():
        assert value.shape == (4622,)
    sdss=fits.open(HERE/'spec-5718-56693-0056.fits')
    coadd=sdss[1].data
    consistency={x:float(np.max(abs(a[x].astype(float)-coadd[x].astype(float)))) for x in ['FLUX','IVAR','AND_MASK','OR_MASK']}
    assert all(v==0 for v in consistency.values())
    consistency['wavelength_max_difference_angstrom']=float(max(abs(a['WAVE']-10.**coadd['LOGLAM'])))
    consistency['residual_identity_max_abs']=float(max(abs(a['RESIDUAL_FLUX']-(a['FLUX']-a['MODEL_SILO']))))
    assert consistency['wavelength_max_difference_angstrom']<.0011
    assert consistency['residual_identity_max_abs']<1e-6
    wave=a['WAVE'].astype(float);sig_inst=coadd['WDISP'].astype(float)*np.log(10)*1e-4*wave
    resid=a['RESIDUAL_FLUX'].astype(float)
    raw=(HERE/'silo_emlines_all_fixed_rows.bin').read_bytes()
    hdr=fits.Header.fromstring(raw[:5760].decode('ascii'),sep='')
    dt=fits.ColDefs([fits.Column(name=hdr[f'TTYPE{i}'],format=hdr[f'TFORM{i}']) for i in range(1,hdr['TFIELDS']+1)]).dtype.newbyteorder('>')
    rows=np.frombuffer(raw,dtype=dt,offset=5760,count=7637)
    selected=rows[rows['DETECTION_CATALOG_ID']==790]
    assert len(selected)==7
    lines=[]
    for r in selected:
        d={x:serial(r[x]) for x in ['NAME','EM_WAVE','SN','GAUSS_BASE_HEIGHT','GAUSS_AMPLITUDE','GAUSS_SIGMA','RCHI2_SAMPLE','NDOF_SAMPLE','RCHI2_3SIG','NDOF_3SIG','SAMPLE_SIZE']}
        d['GAUSS_FIT_REPORTED']=bool(r['GAUSS_FIT_REPORTED']==84)
        lines.append(d)

    # Orthogonal kernel validation: adaptive scalar integral, normalization,
    # and exact noiseless recovery with planted nonzero intrinsic width.
    wc=np.linspace(7330,7370,80);sc=np.full_like(wc,1.7)
    kernel=line_kernel(wc,sc,OII,70)
    errs=[]
    for j in [20,30,40,50]:
        for k,centre in enumerate(OII):
            s=np.sqrt(1.7**2+(centre*70/C)**2);lo=wc[j]*10**(-.00005);hi=wc[j]*10**.00005
            val=quad(lambda x:np.exp(-.5*((x-centre)/s)**2)/np.sqrt(2*np.pi)/s,lo,hi,epsabs=1e-13)[0]/(hi-lo)
            errs.append(abs(val-kernel[j,k]))
    syn_use=(abs(wave-OII.mean())<30)
    synp=[.75,65.,3.5,2.2,.02,.03]
    synth=line_kernel(wave,sig_inst,OII+synp[0],synp[1])@np.array(synp[2:4])+synp[4]+synp[5]*(wave-OII.mean())/30
    synfit=fit_line(wave,sig_inst,synth,np.ones_like(wave)*100,syn_use,True)
    synthetic_max_parameter_error=float(max(abs(np.array(synfit['parameters'])-synp)))
    assert max(errs)<1e-10 and synthetic_max_parameter_error<1e-5
    checks=dict(kernel_quadrature_max_absolute_error=float(max(errs)),
                noiseless_doublet_parameter_max_absolute_error=synthetic_max_parameter_error,
                noiseless_chi2=synfit['chi2'])
    fits_out=[]
    for halfwindow in [20,30,40]:
        for mask_mode in ['positive_ivar','and_zero']:
            for noise in ['IVAR_RESCALED','IVAR']:
                use=(abs(wave-OII.mean())<halfwindow)&(a[noise]>0)&np.isfinite(resid)
                if mask_mode=='and_zero':use&=(a['AND_MASK']==0)
                sf=fit_line(wave,sig_inst,resid,a[noise],use,False)
                df=fit_line(wave,sig_inst,resid,a[noise],use,True)
                fits_out.append(dict(halfwindow_angstrom=halfwindow,mask=mask_mode,noise=noise,pixel_integrated=True,
                                     single=sf,doublet=df,delta_chi2_single_minus_doublet=sf['chi2']-df['chi2']))
    use=(abs(wave-OII.mean())<30)&(a['IVAR_RESCALED']>0)
    sf=fit_line(wave,sig_inst,resid,a['IVAR_RESCALED'],use,False,False)
    df=fit_line(wave,sig_inst,resid,a['IVAR_RESCALED'],use,True,False)
    fits_out.append(dict(halfwindow_angstrom=30,mask='positive_ivar',noise='IVAR_RESCALED',pixel_integrated=False,
                         single=sf,doublet=df,delta_chi2_single_minus_doublet=sf['chi2']-df['chi2']))
    windows=[]
    for name,centres in [('OII',OII),('Hbeta',np.array([9586.142578125])),('OIII4959',np.array([9778.572265625])),('OIII5007',np.array([9873.0869140625]))]:
        use=abs(wave-centres.mean())<30
        core=abs(wave-centres.mean())<10
        windows.append(dict(name=name,centres_angstrom=centres.tolist(),window_pixels=int(use.sum()),
            positive_original_ivar_pixels=int((use&(a['IVAR']>0)).sum()),positive_rescaled_ivar_pixels=int((use&(a['IVAR_RESCALED']>0)).sum()),
            median_wdisp_pixels=float(np.median(coadd['WDISP'][use])),median_sigma_instrument_angstrom=float(np.median(sig_inst[use])),
            median_fwhm_instrument_angstrom=float(2*np.sqrt(2*np.log(2))*np.median(sig_inst[use])),
            core_pixels=int(core.sum()),core_sky_minmax=[float(min(coadd['SKY'][core])),float(max(coadd['SKY'][core]))],
            core_flags={kind:{label:int((core&((a[kind]&(1<<bit))!=0)).sum()) for bit,label in BITS.items()} for kind in ['AND_MASK','OR_MASK']},
            window_flags={kind:{label:int((use&((a[kind]&(1<<bit))!=0)).sum()) for bit,label in BITS.items()} for kind in ['AND_MASK','OR_MASK']}))
        with (out/f'{name}_pixels.csv').open('w') as f:
            writer=csv.writer(f);writer.writerow(['wave_A','flux','model_silo','residual','ivar','ivar_rescaled','wdisp_pixels','sigma_inst_A','sky','and_mask','or_mask'])
            for i in np.flatnonzero(use):writer.writerow([wave[i],a['FLUX'][i],a['MODEL_SILO'][i],resid[i],a['IVAR'][i],a['IVAR_RESCALED'][i],coadd['WDISP'][i],sig_inst[i],coadd['SKY'][i],a['AND_MASK'][i],a['OR_MASK'][i]])
    primary=next(x for x in fits_out if x['halfwindow_angstrom']==30 and x['mask']=='positive_ivar' and x['noise']=='IVAR_RESCALED' and x['pixel_integrated'])
    fig,axes=plt.subplots(2,4,figsize=(16,6),gridspec_kw={'height_ratios':[3,1]},sharex='col',constrained_layout=True)
    for j,win in enumerate(windows):
        centre=np.mean(win['centres_angstrom']);use=abs(wave-centre)<30;iv=a['IVAR_RESCALED'][use]
        err=np.divide(1,np.sqrt(iv),out=np.full_like(iv,np.nan),where=iv>0)
        ax=axes[0,j];ax.errorbar(wave[use],resid[use],yerr=err,fmt='.',color='black',capsize=1,lw=.6,label='SILO residual ± rescaled noise')
        for c in win['centres_angstrom']:ax.axvline(c,color='steelblue',ls=':',lw=1)
        flagged=use&(a['AND_MASK']!=0);ax.scatter(wave[flagged],resid[flagged],s=65,facecolors='none',edgecolors='darkorange',label='nonzero AND mask')
        ax.axhline(0,color='grey',lw=.7);ax.set_title(win['name']);ax.set_ylabel('Flux density (native units)' if j==0 else '')
        if j==0:
            for key,color in [('single','crimson'),('doublet','royalblue')]:ax.plot(primary[key]['native_wave'],primary[key]['native_model'],color=color,label=key)
            ax.legend(fontsize=7)
        lower=axes[1,j];lower.step(wave[use],coadd['SKY'][use],where='mid',color='grey');lower.set_ylabel('Sky' if j==0 else '');lower.set_xlabel('Vacuum wavelength (Å)')
        for c in win['centres_angstrom']:lower.axvline(c,color='steelblue',ls=':',lw=1)
    fig.suptitle('L002777 / SILO790: local line-shape diagnostic; no source-redshift confirmation')
    fig.savefig(out/'spectrum_windows.png',dpi=170);plt.close(fig)

    specobj=sdss[2].data[0]
    specdata={x:serial(specobj[x]) for x in ['SPECOBJID','PLATE','MJD','FIBERID','CLASS','SUBCLASS','Z','Z_ERR','ZWARNING','VDISP','VDISP_ERR','VDISPCHI2','VDISPNPIX','VDISPDOF','SN_MEDIAN_ALL','RA','DEC']}
    portal=json.loads((HERE/'portal_lens_record.json').read_text());master=portal['master']
    status={k:master[k] for k in ['unique_identifier','tile_id','grade','vis_lp_completed','vis_pix_completed','sersic_vis_completed','expected_band_count','completed_band_count','metadata_error_count','inspection_status','inspection_votes','success_votes','failure_votes','inspection_consensus_75']}
    posmeta=json.loads((HERE/'dataset/positions_meta.json').read_text())
    used=np.array(posmeta['positions_used']);used=np.c_[used[:,1],-used[:,0]]
    drop=np.array([[p['x'],-p['y']] for p in posmeta['dropped']])
    dataset=fits.open(HERE/f'dataset/{portal["id"]}.fits')
    imagechecks=[]
    for band in ['VIS','NIR_Y','NIR_J','NIR_H','HSC_G','MEGACAM_R','PANSTARRS_I','HSC_Z']:
        im=dataset[band+'_BGSUB'].data;noise=dataset[band+'_RMS'].data;psf=dataset[band+'_PSF'].data
        imagechecks.append(dict(band=band,shape=list(im.shape),finite_data=int(np.isfinite(im).sum()),finite_positive_noise=int((np.isfinite(noise)&(noise>0)).sum()),psf_sum=float(psf.sum()),psf_shape=list(psf.shape)))
    wcs=WCS(dataset['VIS_BGSUB'].header);ix,iy=wcs.world_to_pixel_values(float(specobj['RA']),float(specobj['DEC']))
    fiber=np.array([(ix-49.5)*.1,(iy-49.5)*.1])
    fig,axes=plt.subplots(1,3,figsize=(12,4.5),constrained_layout=True)
    for ax,band in zip(axes,['VIS','HSC_G','NIR_H']):
        im=dataset[band+'_BGSUB'].data.astype(float);scale=np.percentile(abs(im),80)
        ax.imshow(np.arcsinh(im/max(scale,1e-12)),origin='lower',extent=[-5,5,-5,5],cmap='gray_r',vmin=0,vmax=np.arcsinh(np.percentile(im,99.7)/scale))
        ax.scatter(used[:,0],used[:,1],s=90,facecolors='none',edgecolors='dodgerblue',label='Kept gate positions')
        ax.scatter(drop[:,0],drop[:,1],s=110,facecolors='none',edgecolors='red',marker='s',label='Dropped position, preserved')
        ax.add_patch(Circle(fiber,1.,edgecolor='green',fill=False,ls='--',lw=1,label='2″ BOSS fiber'))
        ax.set(xlim=(-2.5,2.5),ylim=(-2.5,2.5),xlabel='West offset (arcsec)',title=band)
    axes[0].set_ylabel('North offset (arcsec)');axes[0].legend(fontsize=7,loc='upper left')
    fig.suptitle('L002777: competing source associations remain unresolved')
    fig.savefig(out/'positions_and_fiber.png',dpi=170);plt.close(fig)
    points={}
    for fname in ['coolest.json','coolest_sersic.json']:
        model=json.loads((HERE/'results'/fname).read_text());entities=[]
        for entity in model['lensing_entities']:
            e={key:entity.get(key) for key in ['name','type','redshift']}
            for kind in ['light_model','mass_model']:
                e[kind]=[dict(type=p['type'],parameters={k:v['point_estimate']['value'] for k,v in p['parameters'].items()}) for p in entity.get(kind,[]) if 'parameters' in p]
            entities.append(e)
        points[fname]=entities
    result=dict(assertion_tested='Local spectral line shapes and released source-association metadata for one spatially matched candidate; no confirmation or gravity fit',
                target='EUCL-DR1-L002777',silo_catalog_id=790,source_redshift_candidate=Z,
                array_consistency=consistency,checks=checks,sdss=specdata,
                oii_vacuum_wavelengths=OII.tolist(),oii_separation_angstrom=float(np.diff(OII)[0]),
                published_lines=lines,published_same_window_delta_chi2=float((lines[-1]['RCHI2_SAMPLE']-lines[0]['RCHI2_SAMPLE'])*17),
                local_fits=fits_out,windows=windows,portal_status=status,released_point_models=points,
                positions_pipeline_meta=posmeta,positions_sky_west_north=used.tolist(),dropped_sky_west_north=drop.tolist(),
                fiber_west_north_arcsec=fiber.tolist(),image_checks=imagechecks,
                sed_input_redshift='Unverified; catalogue photo-z does not establish redshift used for SED fitting',
                non_claims=['Not a source-redshift confirmation; line-fit chi2 differences are descriptive, not calibrated significance or Bayes factors',
                            'No stellar-template refit or sky-residual likelihood; published SILO residual and Gaussian effective LSF remain conditional',
                            'No official failure cause inferred; rejected model thetaE is not a valid gravity constraint',
                            'No spherical velocity-dispersion reinterpretation of a visibly flattened disk or rotation treatment'])
    (out/'result.json').write_text(json.dumps(result,indent=2,default=serial)+'\n')
    print(json.dumps(dict(primary_delta_chi2=primary['delta_chi2_single_minus_doublet'],
               delta_chi2_all=[x['delta_chi2_single_minus_doublet'] for x in fits_out],checks=checks,
               oii_window=windows[0],sdss=specdata),default=serial))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
