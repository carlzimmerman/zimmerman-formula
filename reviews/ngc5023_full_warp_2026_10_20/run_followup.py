"""Recheck frozen boxes in actualnative/common40arcsec imaging and olderdata."""
import argparse,json,sys
from pathlib import Path
import numpy as np
from followup_model import render
from compare_model import bin20,XC,ZC,UC
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent/'ngc5023_cube_2026_10_20'))
from cube_analysis import Cube,BLANK_CENTERS

def aperture(a,c):
    x,z,u=c['center_major_minor_u'];ku=c['velocity_bins']
    i=np.argmin(abs((XC[:-1]+XC[1:])/2-x));j=np.argmin(abs((ZC[:-1]+ZC[1:])/2-z));k=np.argmin(abs((UC[:-ku+1]+UC[ku-1:])/2-u))
    assert abs((XC[i]+XC[i+1])/2-x)<1e-6 and abs((ZC[j]+ZC[j+1])/2-z)<1e-6 and abs((UC[k]+UC[k+ku-1])/2-u)<1e-6
    return a[...,k:k+ku,j:j+2,i:i+2].sum(axis=(-3,-2,-1))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output);out.mkdir(exist_ok=True)
    cs=json.loads((HERE/'followup_candidates.json').read_text())['cases'];params=json.loads((HERE/'uncertainty_scenarios.json').read_text())['cases']+json.loads((HERE/'trace_scenarios.json').read_text())['cases']
    ar=np.load(HERE/'analysis_run002/arrays.npz');ratios=ar['training_ratio'];fitrecords=[]
    for n in ['family_run001','trace_run001']:fitrecords+=json.loads((HERE/n/'results.json').read_text())['cases']
    archive={};report={'scope':'Exploratory frozen-box checks; HR/LR sameobservations, olderWHISP1996 differentcampaign butfullvisibilitydisjointnessunverified, sameWSRT. No matcheddiscovery p-values, no acceleration/cosmology. Common40 model sampled on each actualnativegrid. OriginalHRfitcoefficients retained; no fitting olderdata.','datasets':{}}
    for which in ['HR','LR','WHISP']:
        info={'data':{},'native_operator_model_checks':{}}
        for beam in [0.,40.]:
            cube=Cube(which,beam);d=bin20(cube.sample());blanks=np.array([bin20(cube.sample(dx=x,dz=z)) for x,z in BLANK_CENTERS]);label='native' if beam==0 else '40arcsec'
            info['data'][label]={'metadata':cube.metadata,'boxes':[]};archive[which+'_'+label+'_data']=d;archive[which+'_'+label+'_blanks']=blanks
            for c in cs:
                flux=float(aperture(d,c));bv=aperture(blanks,c);sd=float(bv.std(ddof=1));mean=float(bv.mean())
                info['data'][label]['boxes'].append({'id':c['id'],'flux_Jy_km_s':flux,'blank_mean_Jy_km_s':mean,'blank_scatter_Jy_km_s':sd,'flux_minus_blank_mean_scatter_units':(flux-mean)/sd})
            if which=='HR' and beam==0:
                controls=[]
                for dx,dz,dv in [(-4,0,0),(4,0,0),(0,-4,0),(0,4,0),(0,0,-4),(0,0,4)]:
                    q=bin20(cube.sample(dx=dx,dz=dz,dv=dv));controls.append({'dx':dx,'dz':dz,'dv':dv,'box_fluxes':[float(aperture(q,c)) for c in cs]})
                q=bin20(cube.sample(order=3));controls.append({'kind':'cubic_interpolation','box_fluxes':[float(aperture(q,c)) for c in cs]})
                info['data'][label]['aperture_perturbations']=controls
            del cube
        # Fullfinitefamily common40 forwardreconstruction. Use sourcefitHR amplitudes,
        # never refit older/lowerresolution intensity. All failedtraining cases remain.
        model_flux=[]
        for index,(case,fit) in enumerate(zip(params,fitrecords)):
            m,meta=render(case['parameters'],beam=which+'40');b=np.array([bin20(x) for x in m]);pred=np.tensordot(fit['bounded_fit']['coefficients'],b,axes=(0,0))
            model_flux.append([float(aperture(pred,c)) for c in cs])
            if index==0:archive[which+'_40arcsec_nominal_model']=pred
        model_flux=np.array(model_flux);archive[which+'_40arcsec_model_box_fluxes']=model_flux
        for gate in [1.1,1.25,1.5]:
            keep=ratios<=gate;info['native_operator_model_checks'][str(gate)]={'retained':int(keep.sum()),'box_prediction_min':model_flux[keep].min(0).tolist(),'box_prediction_max':model_flux[keep].max(0).tolist()}
        # Nominal effective-dispersion sensitivity for the olderobservations only.
        if which=='WHISP':
            values=[]
            for sigma in [8.,12.]:
                p=params[0]['parameters'].copy();p['dispersion_total_km_s']=sigma;m,meta=render(p,beam=which+'40');b=np.array([bin20(x) for x in m]);pred=np.tensordot(fitrecords[0]['bounded_fit']['coefficients'],b,axes=(0,0));values.append({'effective_sigma_km_s':sigma,'box_model_flux':[float(aperture(pred,c)) for c in cs]})
            info['source_effective_dispersion_sensitivity']=values
        report['datasets'][which]=info;print(which,info['data']['40arcsec']['boxes'],flush=True)
    (out/'results.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n');np.savez_compressed(out/'arrays.npz',**archive)
if __name__=='__main__':main()
