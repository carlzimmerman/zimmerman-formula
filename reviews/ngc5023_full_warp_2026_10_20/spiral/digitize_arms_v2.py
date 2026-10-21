#!/usr/bin/env python3
"""Pixel trace extraction from the versioned Figure11 raster; no data fitting."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
out=Path(args.output);out.mkdir(exist_ok=True)
here=Path(__file__).resolve().parent
im=np.asarray(Image.open(here/'figure11.png'))
red=(im[:,:,0]>180)&(im[:,:,1]<100)&(im[:,:,2]<100)
black=(im[:,:,:3]<100).all(2)
# Pixel centers of axis ticks in the actual 2983x3455 rendered raster.
x0,x6=381.,2523.
radius=np.linspace(0,360,20)
xp=x0+(x6-x0)*radius/360
cal={
 'width':{'ticks_value':[0,20,30,40],'ticks_y':[1141.5,747.5,551.5,355.5],
          'panel':[190,1170],'units':'arcsec'},
 'phase':{'ticks_value':[0,100,200,300,400],'ticks_y':[2149.5,1964.5,1780.5,1596.5,1412.5],
          'panel':[1200,2180],'units':'degrees'},
 'amplitude':{'ticks_value':[0,.0001,.0002,.0003,.0004,.0005,.0006],
          'ticks_y':[3157,3004.5,2851.5,2699.5,2546.5,2393.5,2241.5],
          'panel':[2210,3180],'units':'Jy km/s/arcsec^2'}}
# Black-curve guards prevent right-axis ticks from contaminating trace nodes.
black_guess={
 'width':[13,17.5,21,26,28.5,32,35,36.4,37.3,37.3,37.3,36.7,36.8,36.9,37.7,39.1,41.5,44.5,46,46.3],
 'phase':[390.8,365,329,284,252,216,185,158,125,111,95,76,70,59,54,45,38,33,26,21],
 'amplitude':[0,0,0,.000001,.000008,.000018,.000075,.00020,.00022,.00024,.00024,.00025,.00026,.000235,.00020,.00015,.00009,.00004,.00001,0]}
traces={}
for key,c in cal.items():
    slope,intercept=np.polyfit(c['ticks_value'],c['ticks_y'],1)
    c['pixel_y_per_unit']=float(slope);c['pixel_y_at_zero']=float(intercept)
    vals={};pixels={}
    for color,mask in [('arm1_black',black),('arm2_red',red)]:
        ys=[]
        for i,x in enumerate(xp):
            xx=int(round(np.clip(x,x0+8,x6-8)))
            lo,hi=c['panel']
            if color=='arm1_black':
                expected=intercept+slope*black_guess[key][i]
                margin={'width':35,'phase':35,'amplitude':110}[key]
                if key=='amplitude' and i==19: margin=8
                lo=max(lo,int(expected-margin));hi=min(hi,int(expected+margin))
            y=np.flatnonzero(mask[lo:hi,xx-2:xx+3].any(1))+lo
            if len(y)==0:
                raise ValueError('Trace missing '+key+' '+color+' '+str(i))
            ys.append(float(np.median(y)))
        pixels[color]=ys
        vals[color]=[(y-intercept)/slope for y in ys]
    traces[key]={'values':vals,'pixel_y':pixels}
# At the degenerate first/last boundary traces partly merge with axes. Keep
# unadjusted readings and expose the stated central anchors separately.
raw={k:v['values'] for k,v in traces.items()}
arm1={k:np.array(v['values']['arm1_black'],dtype=float) for k,v in traces.items()}
arm2={k:np.array(v['values']['arm2_red'],dtype=float) for k,v in traces.items()}
arm1['width'][0]=13.;arm1['phase'][0]=390.8
arm2['width'][0]=10.;arm2['phase'][0]=497.9
for a in [arm1,arm2]:
    a['amplitude']=np.maximum(a['amplitude'],0)
    a['amplitude'][0]=0
profiles={'checkpoint':'ngc5023-full-warp-2026-10-20',
 'source':'Kamphuis2013 arXiv1306.5312v1 Figure11/Table4',
 'source_raster_sha256':hashlib.sha256((here/'figure11.png').read_bytes()).hexdigest(),
 'radii_arcsec':radius.tolist(),
 'radial_sampling':'20 visible, nearly equally spaced markers from0 to6arcmin; approximated exact uniform positions. Not recovered RADI card.',
 'arm1':{'color':'black dashed','width_arcsec':arm1['width'].tolist(),
         'phase_deg_approaching_CCW':arm1['phase'].tolist(),
         'amplitude_Jy_km_s_arcsec2':arm1['amplitude'].tolist(),
         'height_arcsec':14.,'height_visual_range_halfwidth_arcsec':9.,
         'mass_Msun':4.9e7,'mass_visual_range_halfwidth_Msun':.7e7},
 'arm2':{'color':'red solid','width_arcsec':arm2['width'].tolist(),
         'phase_deg_approaching_CCW':arm2['phase'].tolist(),
         'amplitude_Jy_km_s_arcsec2':arm2['amplitude'].tolist(),
         'height_arcsec':9.,'height_visual_range_halfwidth_arcsec':6.,
         'mass_Msun':4.3e7,'mass_visual_range_halfwidth_Msun':.3e7},
 'digitization_not_physical_uncertainty':{
     'radii_arcsec_halfwidth':1.,'width_arcsec_halfwidth':.4,
     'phase_deg_halfwidth':2.,'amplitude_Jy_km_s_arcsec2_halfwidth':1.e-5,
     'meaning':'Declared conservative raster/axis/line-reading envelope, not statistical standard deviation or covariance; image endpoint/axis overlap and low amplitudes dominate.'},
 'published_visual_one_parameter_halfwidths':{
     'arm1_width_arcsec':23.,'arm2_width_arcsec':25.,'both_phase_deg':7.5,
     'meaning':'Table4 average maximum permitted parameter deviations with other parameters held fixed, not independent ring errors or Gaussian priors.'},
 'central_anchor_policy':'Use exact Table4 central widths13,10arcsec andphases390.8,497.9deg. Setcentralamplitudes0wherecurveaxisdegenerate; retainallrawreadings. Clipnegativeoverdensityreadingsbelow0 inmodelprofile,within1e-5readinguncertainty.',
 'raw_trace_readings':raw,'raw_trace_pixel_y':{k:v['pixel_y'] for k,v in traces.items()},
 'axis_calibration':cal}
(out/'profiles.json').write_text(json.dumps(profiles,indent=2,allow_nan=False)+'\n')
print(json.dumps({'nodes':len(radius),'arm1_peak':float(arm1['amplitude'].max()),
                 'arm2_peak':float(arm2['amplitude'].max()),'source_image_shape':list(im.shape)},indent=2))
