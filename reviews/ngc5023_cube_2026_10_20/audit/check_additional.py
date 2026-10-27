#!/usr/bin/env python3
"""Orthogonal checks of masks/template linear algebra and operator blank loops.

The measured source/blank resampling uses the already audited production Cube;
mask intersections and SVD/lstsq algebra are reconstructed independently.
"""
import argparse
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
import numpy as np
from scipy.ndimage import gaussian_filter1d

PACKET=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(PACKET))
from cube_analysis import Cube


def integrate(a):
    return a.reshape(10,6,6,10,15,10).sum(axis=(1,3,5))*65.92


def difference(b):return b-np.flip(b)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    source=np.load(PACKET/'discovery_run001/arrays.npz')
    independent=np.load(PACKET/'replication_run001/arrays.npz')
    a={**{k:source[k] for k in source},**{k:independent[k] for k in independent}}
    result=json.loads((PACKET/'additional_run001/results.json').read_text())
    nominal=json.loads((PACKET/'discovery_run001/results.json').read_text())
    frozen=result['frozen_candidate'];index=tuple(frozen['index'])
    U,Z,X=np.meshgrid((np.arange(10)-4.5)*24.72,(np.arange(6)-2.5)*40,
                      (np.arange(15)-7)*40,indexing='ij')
    known=[(-72.,80.,-24.8,56.),(112.,92.,39.2,40.),(120.,-76.,39.2,52.)]
    masks={}
    for radius in [None,40.,60.,80.]:
        m=(abs(X)<=175)&(abs(Z)>=60)
        for x,z,u,width in known:
            for sign in [-1,1]:
                radial=40 if radius is None else radius+20
                overlap=(abs(X-sign*x)<=radial)&(abs(Z-sign*z)<=radial)&(abs(U-sign*u)<=width/2+12.36)
                m &= ~overlap
        masks[radius]=m
    checks=[]
    def add(name,passed,**kw):checks.append(dict(name=name,passed=bool(passed),**kw))
    for radius in [40.,60.,80.]:
        actual=masks[radius]
        expected=result['datasets']['HR']['strict_known_feature_masks'][str(radius)]
        add('known_feature_footprint_mask_'+str(radius),
            bool(actual[index])==expected['candidate_included'] and int((actual&(X>0)).sum())==expected['metrics']['paired_bins'],
            candidate_included=bool(actual[index]),paired_bins=int((actual&(X>0)).sum()))
    # Recompute each four-column nuisance response from the production sampler,
    # then use an independent least-squares/SVD route instead of reduced QR.
    cube=Cube('HR',40.)
    derivatives=[]
    for axis in ['dx','dz','dv']:
        derivatives.append((difference(integrate(cube.sample(**{axis:4.})))
                            -difference(integrate(cube.sample(**{axis:-4.}))))/8.)
    h=difference(a['HR_binned40'])
    derivatives.append(h-difference(integrate(a['HR_dewarped40'])))
    J=np.stack(derivatives,axis=-1)
    archive=np.load(PACKET/'additional_run001/arrays.npz')
    for key,radius in [('original_search',None),('strict40',40.),('strict60',60.)]:
        mask=masks[radius]&(X>0)
        template=h[mask].astype(float);design=J[mask].astype(float)
        beta,_,rank,sv=np.linalg.lstsq(design,template,rcond=None)
        residual=template-design@beta
        stored=archive[key+'_HR_residual_template']
        error=float(np.max(abs(residual-stored)))
        add(key+'_independent_lstsq_projection',error<2e-9 and rank==4,
            max_saved_residual_difference=error,rank=int(rank),singular_values=sv.tolist(),
            retained_power_fraction=float(residual@residual/(template@template)),
            maximum_design_orthogonality_error=float(np.max(abs(design.T@residual))))
        for name in ['HR','LR','WHISP']:
            d=difference(a[name+'_binned40'])[mask]
            blanks=a[name+'_blanks40'].astype(float)
            db=blanks-np.flip(blanks,axis=(1,2,3));bv=db[:,mask]
            plain=float(d@template/(template@template))
            projected=float(d@residual/(residual@residual))
            bp=bv@template/(template@template);br=bv@residual/(residual@residual)
            found=result['template_comparison'][key]['data'][name]
            values={'fixed_HR_template_amplitude':plain,'linear_nuisance_projected_amplitude':projected,
                    'template_blank_mean':float(bp.mean()),'template_blank_scatter':float(bp.std(ddof=1)),
                    'projected_blank_mean':float(br.mean()),'projected_blank_scatter':float(br.std(ddof=1))}
            err=max(abs(v-found[k]) for k,v in values.items())
            add(key+'_'+name+'_amplitudes',err<2e-6,max_error=err,**values)
    del cube
    # Source/blank operator comparison. These are reproductions through shared
    # resampling, not an independent raw implementation of all transformed cubes.
    for name in ['HR','WHISP']:
        cube=Cube(name,40.)
        centers=nominal['datasets']['HR']['blank_centers_major_minor_arcsec']
        for kind in ['dewarp','spectral20','spectral40','no_spatial_baseline']:
            if kind=='no_spatial_baseline':cube.a+=cube.baseline[:,None,None]
            outputs=[]
            for center in [[0.,0.]]+centers:
                if kind=='dewarp':aa=cube.sample(dx=center[0],dz=center[1],warp=frozen['warp_control'])
                else:
                    aa=cube.sample(dx=center[0],dz=center[1])
                    if kind.startswith('spectral'):
                        width=float(kind.replace('spectral',''))
                        # Independent explicit symmetric filter matrix instead of
                        # gaussian_filter1d, including its nearest endpoint rule.
                        sigma=width/(2.354820045*4.12);r=int(4*sigma+.5)
                        q=np.arange(-r,r+1);w=np.exp(-q*q/(2*sigma*sigma));w/=w.sum()
                        matrix=np.zeros((60,60))
                        for row in range(60):
                            for offset,weight in zip(q,w):matrix[row,np.clip(row+offset,0,59)]+=weight
                        aa=(matrix@aa.reshape(60,-1)).reshape(aa.shape)
                bb=integrate(aa);outputs.append(float(difference(bb)[index]))
            sourcevalue=outputs[0];bg=np.array(outputs[1:])
            expected=result['datasets'][name]['matched_operator_controls'][kind]['candidate']
            error=max(abs(sourcevalue-expected['signed_difference_Jy_km_s']),
                      abs(bg.mean()-expected['blank_mean']),abs(bg.std(ddof=1)-expected['blank_scatter']))
            add(name+'_'+kind+'_operator_matched_candidate',error<2e-6,
                maximum_scalar_error=error,source_difference=sourcevalue,
                blank_mean=float(bg.mean()),blank_scatter=float(bg.std(ddof=1)),blank_count=len(bg))
            if kind=='no_spatial_baseline':cube.a-=cube.baseline[:,None,None]
        del cube
    output={'outcome':'additional masks, fixed-template least-squares projection and selected matched-operator controls verified in stated range',
            'all_passed':all(x['passed'] for x in checks),'checks':checks,
            'scope':'Independent mask/linear-algebra/filter implementation; operator source sampling shares the already audited production Cube. HR and WHISP checked for selected matched operators; not every ancillary scalar independently recomputed.',
            'non_claims':['No joint center likelihood or physical nuisance prior','No complete asymmetric warp/spiral model','No formal significance or strong independent residual detection','No proof that no signal exists']}
    Path(args.output).write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'all_passed':output['all_passed'],'checks':len(checks)}))
    return 0 if output['all_passed'] else 1


if __name__=='__main__':raise SystemExit(main())
