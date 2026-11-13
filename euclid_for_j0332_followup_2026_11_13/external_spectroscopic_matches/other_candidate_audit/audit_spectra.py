"""Three fixed SILO candidates: observed spectra, quality, and local OII controls.
No lens or stellar-population fit, source-redshift confirmation, or p-value.
"""
import argparse,csv,hashlib,json,struct,sys,zlib
from pathlib import Path
import numpy as np
from astropy.io import fits
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
sys.path.insert(0,str(BASE/'l002777_inputs'))
import inspect_target_v2 as local


def scalar(x):
    if isinstance(x,(bytes,np.bytes_)):return x.decode().strip()
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    return x


def main(out):
    out.mkdir(parents=True,exist_ok=True)
    targets=json.loads((HERE/'targets.json').read_text())
    raw=(BASE/'l002777_inputs/silo_emlines_all_fixed_rows.bin').read_bytes()
    hdr=fits.Header.fromstring(raw[:5760].decode('ascii'),sep='')
    dtype=fits.ColDefs([fits.Column(name=hdr[f'TTYPE{i}'],format=hdr[f'TFORM{i}']) for i in range(1,hdr['TFIELDS']+1)]).dtype.newbyteorder('>')
    tab=np.frombuffer(raw,dtype=dtype,offset=5760,count=7637)
    result=[];selected_count=0
    for t in targets:
        sid=t['silo']['CATALOG_ID'];folder=HERE/t['euclid_id'];dest=out/t['euclid_id'];dest.mkdir(exist_ok=True)
        spectra={name:np.fromfile(folder/f'silo{sid}_{name}.bin',dtype='>f4').astype(float) for name in ['WAVE','FLUX','MODEL_SILO','IVAR_RESCALED','RESIDUAL_FLUX']}
        hd=fits.open(next(folder.glob('spec*.fits')));coadd=hd[1].data;obj=hd[2].data[0]
        consistency={'flux_exact':bool(np.array_equal(spectra['FLUX'],coadd['FLUX'])),
                     'wavelength_max_difference_A':float(np.max(abs(spectra['WAVE']-10.**coadd['LOGLAM']))),
                     'residual_identity_max_abs':float(np.max(abs(spectra['RESIDUAL_FLUX']-spectra['FLUX']+spectra['MODEL_SILO'])))}
        assert consistency['flux_exact'] and consistency['wavelength_max_difference_A']<.0021 and consistency['residual_identity_max_abs']<1e-6
        n=len(coadd);assert all(len(x)==n for x in spectra.values())
        wave=spectra['WAVE'];res=spectra['RESIDUAL_FLUX'];iv=spectra['IVAR_RESCALED'];sigma=coadd['WDISP']*np.log(10)*.0001*wave
        zs=t['silo']['DETECTION_Z'];local.OII=np.array([3727.092,3729.875])*(1+zs)
        selected=tab[tab['DETECTION_CATALOG_ID']==sid];selected_count+=len(selected);lines=[]
        for row in selected:
            rec={k:scalar(row[k]) for k in ['NAME','EM_WAVE','SN','RCHI2_SAMPLE','NDOF_SAMPLE','GAUSS_SIGMA','GAUSS_AMPLITUDE']}
            rec['GAUSS_FIT_REPORTED']=bool(row['GAUSS_FIT_REPORTED']==84);lines.append(rec)
        specdata={k:scalar(obj[k]) for k in ['SPECOBJID','PLATE','MJD','FIBERID','Z','Z_ERR','ZWARNING','VDISP','VDISP_ERR','VDISPCHI2','VDISPDOF','VDISPNPIX','SN_MEDIAN_ALL','RA','DEC','CLASS','SUBCLASS']}
        specdata['reported_dispersion_fractional_error']=float(obj['VDISP_ERR']/obj['VDISP'])
        windows=[]
        for line in lines:
            if line['NAME'].startswith('Single'):continue
            c=line['EM_WAVE'];use=abs(wave-c)<30;core=abs(wave-c)<10
            if not use.any():continue
            linesky=coadd['SKY'][core]
            q=dict(name=line['NAME'],centre_A=c,published_SNR=line['SN'],n_pixels=int(use.sum()),core_pixels=int(core.sum()),
                core_positive_rescaled_ivar=int((core&(iv>0)).sum()),core_positive_original_ivar=int((core&(coadd['IVAR']>0)).sum()),
                window_positive_rescaled_ivar=int((use&(iv>0)).sum()),
                instrument_sigma_A=float(np.median(sigma[use])),instrument_fwhm_A=float(2.354820045*np.median(sigma[use])),
                core_sky_minmax=[float(linesky.min()),float(linesky.max())],
                core_flags={kind:{label:int((core&((coadd[kind]&(1<<bit))!=0)).sum()) for bit,label in local.BITS.items()} for kind in ['AND_MASK','OR_MASK']})
            windows.append(q)
            with (dest/(line['NAME'].replace('/','_').replace(' ','_')+'_pixels.csv')).open('w') as f:
                writer=csv.writer(f);writer.writerow(['wave_A','flux','model_silo','residual','ivar_rescaled','ivar_original','wdisp','sky','and_mask','or_mask'])
                for i in np.flatnonzero(use):writer.writerow([wave[i],spectra['FLUX'][i],spectra['MODEL_SILO'][i],res[i],iv[i],coadd['IVAR'][i],coadd['WDISP'][i],coadd['SKY'][i],coadd['AND_MASK'][i],coadd['OR_MASK'][i]])
        model_fits=[]
        for halfwidth in [20,30]:
            for mask in ['positive_ivar','and_zero']:
                use=(abs(wave-local.OII.mean())<halfwidth)&(iv>0)
                if mask=='and_zero':use&=(coadd['AND_MASK']==0)
                one=local.fit_line(wave,sigma,res,iv,use,False)
                two=local.fit_line(wave,sigma,res,iv,use,True)
                model_fits.append(dict(halfwidth_A=halfwidth,mask=mask,single=one,doublet=two,delta_chi2_single_minus_doublet=one['chi2']-two['chi2']))
        selected_windows=windows if sid==310 else windows[:2]
        fig,axes=plt.subplots(2,len(selected_windows),figsize=(4*len(selected_windows),6),sharex='col',gridspec_kw={'height_ratios':[3,1]},constrained_layout=True,squeeze=False)
        for j,win in enumerate(selected_windows):
            c=win['centre_A'];use=abs(wave-c)<30;error=np.divide(1,np.sqrt(iv[use]),out=np.full(use.sum(),np.nan),where=iv[use]>0)
            ax=axes[0,j];ax.errorbar(wave[use],res[use],yerr=error,fmt='.',color='black',capsize=1,lw=.7)
            excluded=use&(iv<=0);ax.scatter(wave[excluded],res[excluded],marker='x',color='red',label='Zero rescaled IVAR')
            flagged=use&(coadd['AND_MASK']!=0);ax.scatter(wave[flagged],res[flagged],facecolors='none',edgecolors='orange',s=60,label='Nonzero AND')
            ax.axhline(0,color='grey',lw=.7)
            centres=local.OII if j==0 else [c]
            for centre in centres:ax.axvline(centre,color='steelblue',ls=':',lw=1)
            ax.set_title(win['name']+'; table S/N='+format(win['published_SNR'],'.2f'))
            if j==0:
                fit=model_fits[2]
                for key,color in [('single','crimson'),('doublet','royalblue')]:ax.plot(fit[key]['native_wave'],fit[key]['native_model'],color=color,label=key)
                ax.set_ylabel('SILO residual flux density');ax.legend(fontsize=7)
            axes[1,j].step(wave[use],coadd['SKY'][use],where='mid',color='grey');axes[1,j].set_xlabel('Vacuum wavelength (Å)')
            if j==0:axes[1,j].set_ylabel('Sky')
        fig.suptitle(t['euclid_id']+f' / SILO{sid}: candidate z={zs:.6f}; quality audit, not source confirmation')
        fig.savefig(dest/'spectrum_windows.png',dpi=150);plt.close(fig)
        portalpath=folder/'portal_record.json';portal=None
        if portalpath.exists():
            m=json.loads(portalpath.read_text())['master'];portal={k:v for k,v in m.items() if 'completed' in k or 'votes' in k or 'inspection' in k or k in ['grade','metadata_error_count']}
        meta_path=folder/'dataset/positions_meta.json';meta=json.loads(meta_path.read_text()) if meta_path.exists() else None
        models={}
        for name in ['coolest.json','coolest_sersic.json']:
            path=folder/'results'/name
            if not path.exists():continue
            full=json.loads(path.read_text());models[name]=[]
            for entity in full['lensing_entities']:
                e={k:entity.get(k) for k in ['name','type','redshift']}
                for kind in ['light_model','mass_model']:
                    e[kind]=[dict(type=x['type'],parameters={k:v['point_estimate']['value'] for k,v in x['parameters'].items()}) for x in entity.get(kind,[]) if 'parameters' in x]
                models[name].append(e)
        rr=dict(target_metadata=t,spectrum=specdata,array_consistency=consistency,source_line_table=lines,line_windows=windows,
                OII_fit_controls=model_fits,OII_separation_A=float(np.diff(local.OII)[0]),portal_status=portal,
                positions_meta=meta,released_models=models)
        result.append(rr);print(t['euclid_id'],json.dumps(dict(spectrum=specdata,windows=windows,delta_chi2=[r['delta_chi2_single_minus_doublet'] for r in model_fits])))
    assert len(result)==3 and selected_count==14
    # Verify local ZIP headers, sizes and CRCs before treating published JPEGs
    # as target images; no whole archive extraction or filename-path writes.
    index=json.loads((HERE/'colour_index_selected.json').read_text());extracted=[]
    assert len(index['selected'])==3 and index['entries']==26667
    for record in index['selected']:
        name=Path(record['name']).name;blob=(HERE/(name+'.zip_member.bin')).read_bytes();h=struct.unpack_from('<4s5H3L2H',blob)
        assert h[0]==b'PK\x03\x04' and h[3]==record['method']==0
        filename=blob[30:30+h[-2]].decode();assert filename==record['name']
        body=blob[30+h[-2]+h[-1]:30+h[-2]+h[-1]+record['compressed_size']]
        assert len(body)==record['uncompressed_size'] and zlib.crc32(body)==record['crc32']
        (out/name).write_bytes(body);extracted.append(dict(**record,sha256=hashlib.sha256(body).hexdigest(),crc_verified=True))
    (out/'result.json').write_text(json.dumps(dict(assertion_tested='Three-target spectral/metadata audit; 14 fixed line rows; no new redshift confirmation or mass fit',
        targets=result,colour_image_extraction=extracted,non_claims=['Candidate grade does not confirm redshift or image association','Local line chi2 differences are descriptive only','Foreground VDISP is reported observed, not independently refitted or aperture-corrected','No accepted lens mass from failed/no-consensus models']),indent=2,default=scalar)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
