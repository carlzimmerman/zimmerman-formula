"""Finite-family residual and correlated real-blank calibration diagnostics.

The tested family is not a confidence set. Boxwise envelopes do not imply
that one member fits all boxes. All intensity searches are exploratory.
"""
import argparse,json
from pathlib import Path
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from scipy.optimize import lsq_linear
from compare_model import regions,XC,ZC,UC
HERE=Path(__file__).resolve().parent

def boxes(a,ku):
    # Works on either cube or a stack of cubes; no circular/zero padding.
    return sliding_window_view(a,(ku,2,2),axis=(-3,-2,-1)).sum(axis=(-3,-2,-1))

def metrics(residual,sd,mask):
    return {'bins':int(mask.sum()),'RMS_Jy_km_s':float(np.sqrt(np.mean(residual[mask]**2))),
      'RMS_blank_scatter_units':float(np.sqrt(np.mean((residual[mask]/sd[mask])**2))),
      'median_absolute_blank_scatter_units':float(np.median(abs(residual[mask])/sd[mask]))}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output);out.mkdir(exist_ok=True)
    runs=['family_run001','trace_run001'];records=[];pred=[];comp=[];raw=[]
    for run in runs:
        records+=json.loads((HERE/run/'results.json').read_text())['cases'];z=np.load(HERE/run/'arrays.npz')
        pred.append(z['predictions']);comp.append(z['components']);raw.append(z['peak_fixed_unfitted'])
    pred=np.concatenate(pred);comp=np.concatenate(comp);raw=np.concatenate(raw)
    z=np.load(HERE/'nominal_run001/arrays.npz');data=z['data_binned'];blanks=z['blanks_binned'];tr,va,gu=regions()
    sd0=blanks.std(0,ddof=1);floor=np.median(sd0[tr])*.5;sd=np.maximum(sd0,floor);scale=sd[tr]
    c=np.load(HERE/'controls_run001/arrays.npz');cpred=c['predictions'];numerical=np.max(abs(cpred-cpred[0]),axis=0)
    weighted=np.array([r['bounded_fit']['weighted_training_RMS'] for r in records]);ratios=weighted/weighted[0]
    # Propagate measured blank perturbations through training-only bounded amplitude fit.
    # All20 translated blanks are retained, with no independent-draw interpretation.
    co=np.array([r['bounded_fit']['coefficients'] for r in records]);dco=np.empty((len(records),len(blanks),3))
    for i,(m,r) in enumerate(zip(comp,records)):
        A=m[:,tr].T.astype(np.float64)/scale[:,None];lo,hi=np.array(r['bounded_fit']['coefficient_bounds'])
        for j,b in enumerate(blanks):
            fit=lsq_linear(A,(data[tr]+b[tr]).astype(np.float64)/scale,bounds=(lo,hi),tol=1e-10)
            assert fit.success;dco[i,j]=fit.x-co[i]
    report={'scope':'Finite scenario and finite numerical-control envelopes only; no posterior, confidence coverage, independent holdout, blind discovery, formal p-value, or absence theorem.',
      'number_labeled_scenarios':len(records),'number_distinct_parameter_sets':117,
      'training_footprint':'|z|<=20arcsec; centers|z|<=10; prior full-cube source fit already unblinded.',
      'relative_training_gates':'1.10/1.25/1.50 times nominal weighted RMS; these are sensitivity strata, not adequacy criteria.',
      'nominal':{name:metrics(data-pred[0],sd,mask) for name,mask in [('train',tr),('validation',va),('guarded',gu)]},
      'finite_family':{},'numerical':{},'search':[],
      'noise':'20 real translated apertures, spatially overlapping and not independent; refit training data+blank_train and propagate amplitude change. Local empirical noise sensitivity, not calibrated null sampling.'}
    for name,mask in [('train',tr),('validation',va),('guarded',gu)]:
        q=np.array([np.sqrt(np.mean(((data-p)[mask]/sd[mask])**2)) for p in pred])
        report['finite_family'][name]={'RMS_scatter_min':float(q.min()),'RMS_scatter_max':float(q.max()),'best_case':records[int(q.argmin())]['id'],
          'nominal_numerical_control_max_RMS_scatter':float(np.max(np.sqrt(np.mean(((cpred-cpred[0])[:,mask]/sd[mask])**2,axis=1))))}
    report['numerical']['method']='Maximum absolute per-bin change across same-operator cloud/native refinement and no-CIC-compensation controls is added to envelope. Finite discrepancy, not a rigorous error bound on every scenario.'
    report['numerical']['controls']={name:{'relative_L1_all':float(np.sum(abs(p-cpred[0]))/np.sum(abs(cpred[0]))),'max_abs_Jy_km_s':float(abs(p-cpred[0]).max())} for name,p in zip(['nominal','cloud_refined','native_refined','no_CIC_compensation'],cpred)}
    report['amplitude_noise']={'maximum_coefficient_change':np.max(abs(dco),axis=(0,1)).tolist(),
      'nominal_coefficient_blank_std':dco[0].std(0,ddof=1).tolist(),
      'nominal_mass_bound_hits':records[0]['bounded_fit']['bound_hits']}
    # Report emission-bearing validation separately so empty cube volume cannot hide its residual.
    emission=pred[0]>sd
    report['nominal_emission_selected']={name:metrics(data-pred[0],sd,mask&emission) for name,mask in [('validation',va),('guarded',gu)] if np.any(mask&emission)}
    report['emission_selection_scope']='Supplementary descriptive subset fixed by nominal model prediction>one measured blank scatter per bin, not observed data threshold; selection still comes from already fitted source.'
    arrays={'data':data,'blanks':blanks,'predictions':pred,'components':comp,'unfitted_predictions':raw,'training_mask':tr,'validation_mask':va,'guarded_mask':gu,'sd':sd,'numerical_discrepancy':numerical,'amplitude_blank_deltas':dco,'training_ratio':ratios,'X':XC,'Z':ZC,'U':UC}
    for gate in [1.1,1.25,1.5]:
        keep=ratios<=gate;key=str(gate);report['finite_family'][key]={'retained':int(keep.sum()),'ids':[r['id'] for r,k in zip(records,keep) if k]}
        arrays['envelope_min_'+key]=pred[keep].min(0);arrays['envelope_max_'+key]=pred[keep].max(0)
    for ku in [2,3]:
        db=boxes(data,ku);pb=boxes(pred,ku);bb=boxes(blanks,ku);nb=boxes(numerical,ku)
        bsd=bb.std(0,ddof=1);bfloor=np.median(bsd)*.5;bsd=np.maximum(bsd,bfloor)
        # Noise residual for every scenario and every retained actual sky aperture.
        # Use maximum over scenarios for each blank when comparing scan maxima.
        null_stats=[]
        for i in range(len(records)):
            fit_response=np.tensordot(dco[i],comp[i],axes=(1,0))
            null_stats.append((bb-boxes(fit_response,ku))/bsd)
        null_stats=np.array(null_stats)
        for region,mask in [('validation',va),('guarded',gu)]:
            safe=boxes(mask.astype(int),ku)==ku*4
            for gate in [1.1,1.25,1.5]:
                keep=ratios<=gate;lo=pb[keep].min(0)-nb;hi=pb[keep].max(0)+nb
                dist=np.where(db>hi,db-hi,np.where(db<lo,db-lo,0));stat=dist/bsd
                nominal_stat=(db-pb[0])/bsd
                null_max=np.max(abs(null_stats[keep][:,:,safe]),axis=(0,2))
                ranked=np.argsort(np.where(safe,abs(stat),-1).ravel())[-5:][::-1];top=[]
                for flat in ranked:
                    k,j,i=np.unravel_index(flat,stat.shape)
                    top.append({'center_major_arcsec':float((XC[i]+XC[i+1])/2),'center_minor_arcsec':float((ZC[j]+ZC[j+1])/2),
                       'center_relative_velocity_km_s':float((UC[k]+UC[k+ku-1])/2),'observed_flux_Jy_km_s':float(db[k,j,i]),
                       'prediction_envelope_including_finite_numerical':[float(lo[k,j,i]),float(hi[k,j,i])],
                       'signed_distance_blank_scatter_units':float(stat[k,j,i]),'nominal_signed_residual_scatter_units':float(nominal_stat[k,j,i]),
                       'measured_blank_scatter_Jy_km_s':float(bsd[k,j,i]),'positive_and_negative_sum_can_cancel':True})
                report['search'].append({'velocity_bins':ku,'box_size_arcsec_km_s':[40,40,ku*12.36],'region':region,'training_ratio_gate':gate,'retained_cases':int(keep.sum()),
                  'number_correlated_box_positions':int(safe.sum()),'max_abs_persistent_distance_blank_scatter':float(abs(stat[safe]).max()),
                  'max_nominal_abs_residual_blank_scatter':float(abs(nominal_stat[safe]).max()),
                  'blank_search_maxima_after_training_refit_worst_retained_case':null_max.tolist(),
                  'blank_maximum_range':[float(null_max.min()),float(null_max.max())],
                  'top5_exploratory_boxes':top,
                  'interpretation':'Every listed box is robust only against this finite retained family. Envelopes can use different members per box; no common globally adequate model is asserted. Multiple scales/regions/gates are correlated and exploratory.'})
                arrays['distance_ku%d_%s_g%s'%(ku,region,gate)]=np.where(safe,stat,np.nan)
    (out/'results.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n');np.savez_compressed(out/'arrays.npz',**arrays)
    print(json.dumps({'nominal':report['nominal'],'family':{k:v for k,v in report['finite_family'].items() if 'RMS_scatter_min' in v},'search':[{k:r[k] for k in ['velocity_bins','region','training_ratio_gate','retained_cases','max_abs_persistent_distance_blank_scatter','blank_maximum_range']} for r in report['search']]},indent=2),flush=True)
if __name__=='__main__':main()
