#!/usr/bin/env python3
"""Post-selection diagnostic controls, retaining the frozen candidate and input runs."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.ndimage import gaussian_filter1d
from cube_analysis import Cube, bins, pair, metrics, candidate_value, support, HALF, XX, ZZ, YY, X, Z, U, KNOWN, BLANK_CENTERS

HERE=Path(__file__).resolve().parent


def strict_support(radius):
    m=support('candidate_search').copy()
    for x,z,u,width in KNOWN:
        for s in [-1,1]:
            # A bin is discarded if its footprint intersects this enlarged box.
            m &= ~((abs(XX-s*x)<=radius+20)&(abs(ZZ-s*z)<=radius+20)&(abs(YY-s*u)<=width/2+12.36))
    return m


def spectrum(a,index):
    k,j,i=index
    return a[:,j*10:(j+1)*10,i*10:(i+1)*10].sum((1,2))*16


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    out=Path(args.output);out.mkdir(exist_ok=True)
    frozen=json.loads((HERE/'discovery_run001/candidate.json').read_text());idx=frozen['index']
    src=np.load(HERE/'discovery_run001/arrays.npz')
    other=np.load(HERE/'replication_run001/arrays.npz')
    arrays={**{k:src[k] for k in src},**{k:other[k] for k in other}}
    result={'status':'post-selection sensitivity and shape comparison; exploratory, no new candidate selection',
      'frozen_candidate':frozen,'spectral_control_note':'Additional20/40km/s Gaussian smoothing on already resampled observed cubes is an LSF-sensitivity check, not exact native LSF deconvolution/matching.',
      'datasets':{},'template_comparison':{}}
    saved={}
    derivatives=[]
    for name in ['HR','LR','WHISP']:
        c=Cube(name,40.)
        a=arrays[name+'_aligned40'];b=arrays[name+'_binned40'];blanks=arrays[name+'_blanks40']
        centers=[(x,z) for x,z in BLANK_CENTERS if np.isfinite(c.sample(dx=x,dz=z)).all()]
        rec={'strict_known_feature_masks':{},'matched_operator_controls':{},'fine_center_slices':[]}
        for r in [40.,60.,80.]:
            mask=strict_support(r)
            rec['strict_known_feature_masks'][str(r)]={'candidate_included':bool(mask[tuple(idx)]),
              'interpretation':'Known feature box expanded by spatial radius plus half bin width; paired exclusion',
              'metrics':metrics(b,blanks,mask)}
        # Reprocess source and blank cubes through identical interpolation/warp/LSF operators.
        for kind in ['cubic','dewarp','spectral20','spectral40','no_spatial_baseline']:
            if kind=='cubic':aa=c.sample(order=3)
            elif kind=='dewarp':aa=c.sample(warp=frozen['warp_control'])
            elif kind.startswith('spectral'):
                fwhm=float(kind.replace('spectral',''));aa=gaussian_filter1d(a,fwhm/(2.354820045*4.12),axis=0,mode='nearest')
            else:
                c.a+=c.baseline[:,None,None];aa=c.sample()
            bb=[]
            for dx,dz in centers:
                if kind=='cubic':ba=c.sample(dx=dx,dz=dz,order=3)
                elif kind=='dewarp':ba=c.sample(dx=dx,dz=dz,warp=frozen['warp_control'])
                else:
                    ba=c.sample(dx=dx,dz=dz)
                    if kind.startswith('spectral'):ba=gaussian_filter1d(ba,fwhm/(2.354820045*4.12),axis=0,mode='nearest')
                if np.isfinite(ba).all():bb.append(bins(ba))
            bb=np.array(bb)
            assert len(bb)>=8
            ab=bins(aa)
            rec['matched_operator_controls'][kind]={'blank_count':len(bb),
               'candidate':candidate_value(ab,bb,idx),'global':metrics(ab,bb,support('all')),
               'strict40':metrics(ab,bb,strict_support(40.))}
            if kind=='no_spatial_baseline':c.a-=c.baseline[:,None,None]
        # Fine one-axis controls expose joint behavior; no Gaussian center prior inferred.
        for axis in ['dx','dz','dv']:
            for offset in [-2.,-1.,0.,1.,2.]:
                kw={axis:offset};bb=bins(c.sample(**kw))
                rec['fine_center_slices'].append({'axis':axis,'offset':offset,
                  'candidate':candidate_value(bb,blanks,idx),'global':metrics(bb,blanks,support('all'))})
        if name=='HR':
            for axis in ['dx','dz','dv']:
                plus,_=pair(bins(c.sample(**{axis:4.})))
                minus,_=pair(bins(c.sample(**{axis:-4.})))
                derivatives.append((plus-minus)/8.)
            dd,_=pair(b);dw,_=pair(bins(arrays['HR_dewarped40']))
            derivatives.append(dd-dw)
        saved[name+'_candidate_spectrum_sideA_Jy']=spectrum(a,idx)
        saved[name+'_candidate_spectrum_sideB_Jy']=spectrum(a[::-1,::-1,::-1],idx)
        result['datasets'][name]=rec
        print(name,'additional controls done',flush=True)
        del c
    # Fixed HALOGAS templates, subsequently compared with old data. This extension
    # follows the first frozen-bin comparison; it is not a preregistered test.
    hd,_=pair(arrays['HR_binned40'])
    J=np.stack(derivatives,axis=-1)
    for label,mask in [('original_search',support('candidate_search')),
                       ('strict40',strict_support(40.)),('strict60',strict_support(60.))]:
        m=mask&HALF
        template=hd[m].astype(float)
        design=J[m].astype(float)
        q,_=np.linalg.qr(design,mode='reduced')
        residual=template-q@(q.T@template)
        rec={'paired_bins':int(m.sum()),'template_norm_squared':float(template@template),
          'after_linear_center_and_empiricalwarp_projection_norm_squared':float(residual@residual),
          'design_singular_values':np.linalg.svd(design,compute_uv=False).tolist(),
          'limitation':'Linear center derivatives and one data-derived warp shape are diagnostics, not the complete asymmetric warp/spiral/emissivity model.',
          'data':{}}
        for name in ['HR','LR','WHISP']:
            d,_=pair(arrays[name+'_binned40']);v=d[m]
            bb=arrays[name+'_blanks40'];db=bb-bb[:,::-1,::-1,::-1];bv=db[:,m]
            plain=v@template/(template@template)
            projected=v@residual/(residual@residual)
            bp=bv@template/(template@template);br=bv@residual/(residual@residual)
            rec['data'][name]={'fixed_HR_template_amplitude':float(plain),
              'template_blank_mean':float(bp.mean()),'template_blank_scatter':float(bp.std(ddof=1)),
              'linear_nuisance_projected_amplitude':float(projected),
              'projected_blank_mean':float(br.mean()),'projected_blank_scatter':float(br.std(ddof=1)),
              'note':'Amplitude1 is the discovery HR template by construction; blanks overlap and weights come from discovery data. No formal new discovery significance.'}
        result['template_comparison'][label]=rec
        saved[label+'_HR_residual_template']=residual
    np.savez_compressed(out/'arrays.npz',**saved)
    (out/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':main()
