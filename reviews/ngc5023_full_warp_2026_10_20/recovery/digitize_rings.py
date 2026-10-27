#!/usr/bin/env python3
"""Calibrated Figure12 marker digitization; no inference from HI cube residuals.

Source marker pixel centers below were transcribed after image inspection and
black/red threshold checks. This is a transparent graphical reconstruction,
not a recovery of the unrounded TiRiFiC parameter file.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    out=Path(args.output);out.mkdir(exist_ok=True)
    source=HERE/'figure12_source.png'
    im=np.array(Image.open(source).convert('RGB'))
    # Native PNG coordinates, before the UI's display resize.
    x=np.linspace(285.,1892.,20)
    # Black SW approaching markers, red NE receding markers. Small overlaps
    # obscure some red markers; equal traces use black centroids where needed.
    inc_sw=np.array([333.,333.5,333.5,333.5,332.5,332.5,333.,333.5,333.5,333.5,335.5,344.5,354.5,377.5,399.5,424.,441.5,463.5,480.5,501.5])
    inc_ne=np.array([333.,333.5,333.5,333.5,332.5,332.5,333.,333.5,333.5,333.5,345.5,359.5,376.5,393.,409.,416.,432.,450.,463.5,473.])
    pa_sw=np.array([1124.5]*12+[1096.5,1080.5,1063.,1041.5,1025.5,1011.5,1004.5,1006.])
    pa_ne=np.array([1124.5]*12+[1096.5,1056.5,1028.5,983.,924.,884.5,853.5,843.])
    v=np.array([1767.,1667.5,1550.,1472.,1445.5,1423.5,1413.5,1392.,1354.5,1341.5,1340.5,1334.5,1343.5,1353.5,1354.5,1355.5,1357.5,1356.5,1357.5,1357.])
    sb=np.array([2352.,2315.5,1957.,1860.5,2041.5,2100.,2190.5,2145.5,2114.5,2148.5,2178.5,2209.5,2263.5,2294.,2337.5,2359.5,2375.5,2375.5,2374.5,2374.5])
    calibration={
      'radius_arcmin':{'pixels':[285,1892],'values':[0,6]},
      'inclination_deg':{'pixels':[180,297,415,532,649],'values':[95,90,85,80,75]},
      'PA_deg':{'pixels':[757,849,941,1033,1217],'values':[36,34,32,30,26]},
      'VROT_km_s':{'pixels':[1332,1431,1530,1628,1727,1826],'values':[90,80,70,60,50,40]},
      'NHI_1e20_cm2':{'pixels':[1926,2151,2377],'values':[6,3,0]},
      'SBR_Jy_km_s_arcsec2':{'pixels':[1907,2001,2095,2189,2283,2377],'values':[.0005,.0004,.0003,.0002,.0001,0]}}
    affine={k:np.polyfit(d['pixels'],d['values'],1) for k,d in calibration.items()}
    def val(k,arr):return np.polyval(affine[k],arr)
    R=val('radius_arcmin',x)*60
    arrays={'radius_arcsec':R,'radius_arcmin':R/60,
      'inclination_approaching_SW_deg':val('inclination_deg',inc_sw),
      'inclination_receding_NE_deg':val('inclination_deg',inc_ne),
      'PA_approaching_SW_deg':val('PA_deg',pa_sw),'PA_receding_NE_deg':val('PA_deg',pa_ne),
      'VROT_both_sides_km_s':val('VROT_km_s',v),
      'NHI_faceon_1e20_cm2':val('NHI_1e20_cm2',sb),
      'SBR_both_sides_Jy_km_s_arcsec2':val('SBR_Jy_km_s_arcsec2',sb)}
    pixel_intervals={'radius_arcsec':2*abs(affine['radius_arcmin'][0])*60,
      'inclination_deg':5*abs(affine['inclination_deg'][0]),
      'PA_deg':5*abs(affine['PA_deg'][0]),
      'VROT_km_s':5*abs(affine['VROT_km_s'][0]),
      'NHI_1e20_cm2':5*abs(affine['NHI_1e20_cm2'][0]),
      'SBR_Jy_km_s_arcsec2':5*abs(affine['SBR_Jy_km_s_arcsec2'][0])}
    # Cross-check the digitized face-on column profile, with paper D=6.6Mpc
    # only for this source check, not for any acceleration/halo inference.
    D=6.6e6*3.0856775814913673e18
    theta=R/206264.80624709636
    mass=np.trapz(2*np.pi*theta*arrays['NHI_faceon_1e20_cm2']*1e20,theta)*D*D*1.6735575e-24/1.98847e33
    flux=np.trapz(2*np.pi*R*arrays['SBR_both_sides_Jy_km_s_arcsec2'],R)
    checks={
      'source_image_shape':im.shape==(2591,2237,3),
      'twenty_ordered_markers':len(R)==20 and bool(np.all(np.diff(R)>0)),
      'central_inclination_within_digitization_of_table88_5':abs(arrays['inclination_receding_NE_deg'][0]-88.5)<pixel_intervals['inclination_deg'],
      'central_PA_within_digitization_of_table28':abs(arrays['PA_receding_NE_deg'][0]-28)<pixel_intervals['PA_deg'],
      'outer_rotation_within_published5km_s_of87_6':abs(arrays['VROT_both_sides_km_s'][-1]-87.6)<5,
      'integrated_disk_mass_within_published0_26e8_error':abs(mass-4.8e8)<.26e8,
      'all_surface_brightness_nonnegative':bool(np.all(arrays['SBR_both_sides_Jy_km_s_arcsec2']>=0))}
    checks={k:bool(v) for k,v in checks.items()}
    result={'source':'Kamphuis2013 arXiv1306.5312v1 Figure12; exact archived source image',
      'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
      'exact_TiRiFiC_parameters_recovered':False,'status':'Graphical digitization with explicit intervals',
      'side_conventions':'Black dashed=approachingSW; red solid=recedingNE; VROT andSBR common bothsides per caption.',
      'radius_convention':'20plotted nodes spanning0..6arcmin. Exact TiRiFiC ring-center/edge convention not recovered; use center/interpolation/support alternatives when rendering.',
      'axis_calibration':calibration,'axis_affine_coefficients':{k:v.tolist() for k,v in affine.items()},
      'marker_pixel_x':x.tolist(),'marker_pixel_y':{'incl_SW':inc_sw.tolist(),'incl_NE':inc_ne.tolist(),'PA_SW':pa_sw.tolist(),'PA_NE':pa_ne.tolist(),'VROT':v.tolist(),'SBR':sb.tolist()},
      'profiles':{k:v.tolist() for k,v in arrays.items()},
      'digitization_interval_halfwidths':pixel_intervals,
      'interval_definition':'Conservative2pxhorizontal,5pxvertical trace/marker/axis reading envelope, not Gaussian standard errors. Endpoint markers partly obscure axes. Rings are correlated; do not draw independent Gaussian perring errors.',
      'published_model_error_ranges':{'inclination_deg':1.3,'PA_deg':1.,'VROT_km_s':5.,'disk_scaleheight_arcsec':3.,'disk_mass_Msun':.26e8},
      'published_error_definition':'Table4 average maximum allowed oneparameter deviations with othersfixed and neighboringring degeneracies; not joint posterior/covariance.',
      'disk_mass_check_Msun':float(mass),'disk_flux_from_digitized_SBR_Jy_km_s':float(flux),
      'table4_disk_mass_Msun':4.8e8,'table4_disk_mass_visual_error_Msun':.26e8,
      'checks':checks,'all_checks_pass':all(checks.values())}
    (out/'ring_profiles.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'all_checks_pass':all(checks.values()),'disk_mass_Msun':float(mass),'disk_flux_Jy_km_s':float(flux),'digitization_intervals':pixel_intervals},indent=2))
    return 0 if all(checks.values()) else 1

if __name__=='__main__':raise SystemExit(main())
