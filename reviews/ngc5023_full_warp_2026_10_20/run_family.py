"""Run one fixed deterministic scenario slice or numerical control suite."""
import argparse,json,time
from pathlib import Path
import numpy as np
from forward_model_v2 import load_preferred,render
from compare_model import bin20,fit_components,regions
HERE=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--controls',action='store_true');ap.add_argument('--start',type=int,default=0);ap.add_argument('--stop',type=int,default=10000);a=ap.parse_args()
    out=Path(a.output);out.mkdir(exist_ok=True)
    old=np.load(HERE/'nominal_run001/arrays.npz');data=old['data_binned'];blanks=old['blanks_binned'];cases=json.loads((HERE/'uncertainty_scenarios.json').read_text())['cases']
    if a.controls:
        cases=[dict(id=name,group='numerical',parameters=load_preferred(),render_settings=settings) for name,settings in [
          ('nominal_v2',{}),('cloud_refined',dict(dr=3,nphi=512,narm=128,nz=16)),
          ('native_refined',dict(refinement=2,dr=3,nphi=512,narm=128,nz=16)),
          ('no_CIC_compensation',dict(compensate=False))]]
    else:cases=cases[a.start:a.stop]
    output=[];predictions=[];components=[];unfitted=[];archive={}
    tr,va,gu=regions();sd=blanks.std(0,ddof=1);scale=np.maximum(sd[tr],np.median(sd[tr])*.5)
    for case in cases:
        tick=time.monotonic();m,meta=render(case['parameters'],**case.get('render_settings',{}));mb=np.array([bin20(x) for x in m]);fit,pred=fit_components(mb,data,blanks,meta,True)
        free,freepred=fit_components(mb,data,blanks,meta,False)
        sv=np.linalg.svd(mb[:,tr].T/scale[:,None],compute_uv=False)
        fit['weighted_training_RMS']=float(np.sqrt(np.mean(((data[tr]-pred[tr])/scale)**2)))
        co=np.array(fit['coefficients']);lo,hi=np.array(fit['coefficient_bounds']);fit['bound_hits']=np.where((abs(co-lo)<1e-5)|(abs(co-hi)<1e-5))[0].tolist()
        fit['weighted_design_singular_values']=sv.tolist();fit['weighted_design_condition_number']=float(sv[0]/sv[-1])
        raw=mb.sum(0);rawmeta={}
        for label,mask in [('train',tr),('validation',va),('guarded_validation',gu)]:rawmeta[label]=float(np.sqrt(np.mean((data[mask]-raw[mask])**2)))
        output.append({'id':case['id'],'group':case['group'],'render_metadata':meta,'bounded_fit':fit,'broad_0_to_3_amplitude_diagnostic':free,'peak_fixed_unfitted_RMS_Jy_km_s':rawmeta,'seconds':time.monotonic()-tick})
        predictions.append(pred);components.append(mb);unfitted.append(raw)
        if a.controls:archive[case['id']+'_native_components']=m
        print(case['id'],fit['metrics']['train']['RMS_in_empirical_blank_scatter'],fit['metrics']['guarded_validation']['RMS_in_empirical_blank_scatter'],flush=True)
    np.savez_compressed(out/'arrays.npz',predictions=np.array(predictions),components=np.array(components),peak_fixed_unfitted=np.array(unfitted),**archive)
    (out/'results.json').write_text(json.dumps({'scope':'Finite source-anchored sensitivity and numerical checks; not a posterior or exact preferredTiRiFiC model.','cases':output},indent=2,allow_nan=False)+'\n')
if __name__=='__main__':main()
