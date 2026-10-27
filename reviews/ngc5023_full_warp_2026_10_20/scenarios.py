"""Predeclared finite source-anchored sensitivity family; no probability weights."""
import copy,json
from pathlib import Path
import numpy as np
from scipy.stats import qmc
from forward_model import load_preferred,KPC_PER_ARCSEC

HERE=Path(__file__).resolve().parent

def shifted(p,mode,value):
    p=copy.deepcopy(p);t=np.asarray(p['radius'])/360
    def add(keys,delta):
        for key in keys:p[key]=(np.asarray(p[key])+delta).tolist()
    if mode=='inc':add(['inc_sw','inc_ne'],value)
    elif mode=='pa':add(['pa_sw','pa_ne'],value)
    elif mode=='vrot':
        for key in ['v_sw','v_ne']:p[key]=np.maximum(0,np.asarray(p[key])+value).tolist()
    elif mode=='lag':p['lag_km_s_arcsec']+=value*KPC_PER_ARCSEC
    elif mode.startswith('h'):p['h'][int(mode[-1])]+=value
    elif mode in ['phase1','phase2']:p['arm'+mode[-1]]['phase']=(np.asarray(p['arm'+mode[-1]]['phase'])+value).tolist()
    elif mode in ['width1','width2']:p['arm'+mode[-1]]['width']=np.maximum(0,np.asarray(p['arm'+mode[-1]]['width'])+value).tolist()
    elif mode=='vsys':p['vsys_sw']+=value;p['vsys_ne']+=value
    elif mode=='east':p['center_east_arcsec']+=value
    elif mode=='north':p['center_north_arcsec']+=value
    elif mode in ['counterwarp_inc','counterwarp_pa']:
        key=mode.split('_')[-1];ramp=np.clip((t-t[9])/(1-t[9]),0,1)
        p[key+'_sw']=(np.asarray(p[key+'_sw'])+value*ramp).tolist()
        p[key+'_ne']=(np.asarray(p[key+'_ne'])-value*ramp).tolist()
    elif mode.startswith('phase_slope') or mode.startswith('phase_curve'):
        key='arm'+mode[-1];shape=2*t-1 if 'slope' in mode else np.sin(np.pi*t)
        p[key]['phase']=(np.asarray(p[key]['phase'])+value*shape).tolist()
    elif mode.startswith('width_slope'):
        key='arm'+mode[-1];p[key]['width']=np.maximum(0,np.asarray(p[key]['width'])+value*(2*t-1)).tolist()
    elif mode.startswith('brightness_arm'):
        key='arm'+mode[-1];p[key]['sbr']=(np.asarray(p[key]['sbr'])*(1+value*(2*t-1))).tolist()
    elif mode=='brightness_disk':
        for key in ['sbr_sw','sbr_ne']:p[key]=(np.asarray(p[key])*(1+value*(2*t-1))).tolist()
    else:raise ValueError(mode)
    return p


def build():
    base=load_preferred();cases=[]
    def save(name,p,group,notes):cases.append({'id':name,'group':group,'notes':notes,'parameters':p})
    save('nominal',base,'nominal','Digitized preferred reconstruction, source Table4 constants.')
    anchors={'inc':1.3,'pa':1.,'vrot':5.,'lag':3.8,'h0':3.,'h1':9.,'h2':6.,'phase1':7.5,'phase2':7.5,'width1':23.,'width2':25.,'vsys':4.}
    for mode,amount in anchors.items():
        for sign in [-1,1]:
            save(mode+('_minus' if sign<0 else '_plus'),shifted(base,mode,sign*amount),'source_anchor',
             'Coherent chosen radial direction anchored to source quoted range; no joint coverage. Width nodes clamp at zero with finite peak; record raw peak-fixed and conditional component-mass-calibrated predictions separately.')
    for mode,amount in [('east',2.),('north',2.),('east',46.37),('north',6.)]:
        for sign in [-1,1]:
            save('center_'+mode+'_'+str(amount)+('_minus' if sign<0 else '_plus'),shifted(base,mode,sign*amount),
                 'literal_center_stress' if amount>2 else 'local_center',
                 '46.37arcsecE/6arcsecN literal Table4 RA-time/Dec source stress; 2arcsec local direction analyst selected. Observed feature masks stay fixed.')
    for mode,amount in [('counterwarp_inc',1.3),('counterwarp_pa',1.),('phase_slope1',7.5),('phase_slope2',7.5),('phase_curve1',7.5),('phase_curve2',7.5),('width_slope1',23.),('width_slope2',25.),('brightness_arm1',.2),('brightness_arm2',.2),('brightness_disk',.1)]:
        for sign in [-1,1]:save(mode+('_minus' if sign<0 else '_plus'),shifted(base,mode,sign*amount),'profile_shape',
            'Analyst smooth profile direction, not source pointwise uncertainty; inner-ten-ring geometry ties and disk/arm geometry ties retained. Brightness taper fractions chosen as sensitivity only.')
    for key,amount in [('inc',.213),('pa',.109),('vrot',.506)]:
        for sign in [-1,1]:save('trace_'+key+('_minus' if sign<0 else '_plus'),shifted(base,key,sign*amount),'digitization','Coherent trace readout halfwidth; not independent ring standard errors.')
    for sign in [-1,1]:
        p=copy.deepcopy(base)
        for key in ['sbr_sw','sbr_ne']:p[key]=np.maximum(0,np.asarray(p[key])+sign*5.32e-6).tolist()
        save('trace_disk_sbr'+('_minus' if sign<0 else '_plus'),p,'digitization','Coherent disk raster halfwidth; raw and mass-calibrated maps retained.')
    p=copy.deepcopy(base);p['radius']=(np.asarray(p['radius'])*361/360).tolist();p['support_arcsec']=361
    save('radial_grid_361',p,'structural','Author baseline grid is0..361; preferred graphic0..360 remains nominal.')
    p=copy.deepcopy(base);p['interpolation']='nearest';save('nearest_profiles',p,'structural','Unrecovered preferred interpolation-card sensitivity.')
    p=copy.deepcopy(base);p['support_arcsec']=360+360/38;save('outer_half_cell',p,'structural','Analyst extension holds last node over a half-cell; source says disk edge not observed.')
    p=copy.deepcopy(base);p['arm_wedge_deg']=90;save('arms_90deg',p,'structural','Early90degree support convention alternative; preferred exact AZ card unavailable.')
    for kind,factor in [('gaussian',np.sqrt(2)),('sech2',np.sqrt(24)/np.pi),('uniform',np.sqrt(6))]:
        p=copy.deepcopy(base);p['vertical']=kind;p['h']=(np.asarray(p['h'])*factor).tolist()
        save('vertical_'+kind+'_same_variance',p,'structural','Analyst alternative shape matched to exponential variance2h²; baseline LTYPE3 supports exponential.')
    p=copy.deepcopy(base);p['inc_sw']=[88.5]*20;p['inc_ne']=[88.5]*20
    save('remove_LOS_warp',p,'structural','Source-described model-class control; no refitted source lag imported.')
    p=copy.deepcopy(base);p['h'][1:]=[9.1,9.1];save('fixed_arm_heights',p,'structural','Source-described model-class control, shared disk height.')
    modes=list(anchors)+['east','north'];amplitudes=list(anchors.values())+[2.,2.]
    for i,row in enumerate(qmc.Sobol(d=len(modes),scramble=False).random_base2(5)):
        p=copy.deepcopy(base)
        for mode,amount,x in zip(modes,amplitudes,2*row-1):p=shifted(p,mode,amount*x)
        save('joint_sobol_%02d'%i,p,'joint_box_sensitivity','32 deterministic unscrambled Sobol box points; equal/no weights, not independent source errors or a posterior. Joint corners can fail training.')
    return {'schema':1,'scope':'Finite family only; no probability/coverage claim; no LambdaCDM or project acceleration law.',
        'selection_predeclared':'Report all; relative training-loss gates1.10,1.25,1.50 times nominal weighted RMS are sensitivity labels, not confidence. Absolute model adequacy separately assessed against real blank scatter.',
        'amplitude_rule':'Every case retains peak-fixed unfitted prediction and a three-component fit on |z|<=20arcsec full footprint only, conditional on separate Table4 component flux ranges. These ranges come from same cube, not external priors. Global amplitude rescaling never compensates individual zero-width nodes with singular peaks.',
        'search_predeclared':'Known-feature masks unchanged. Full40x40arcsec spatial boxes with24.72 or37.08km/s widths, all included bins in validation or guarded region. Search maxima compared with20 real blank-aperture maxima after central-strip refit; correlated empirical controls, no Gaussian p-value. Finite numerical-control discrepancy carried additively.',
        'cases':cases}

if __name__=='__main__':
    out=HERE/'uncertainty_scenarios.json';out.write_text(json.dumps(build(),indent=2,allow_nan=False)+'\n');print(out,len(build()['cases']))
