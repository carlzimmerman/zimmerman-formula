"""Post-scan source-location sensitivity; never a blind discovery mask."""
import argparse,json
from pathlib import Path
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from compare_model import regions,XX,ZZ,UU,outside_features
HERE=Path(__file__).resolve().parent

def boxes(a,ku):return sliding_window_view(a,(ku,2,2),axis=(-3,-2,-1)).sum(axis=(-3,-2,-1))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output);out.mkdir(exist_ok=True)
    z=np.load(HERE/'analysis_run002/arrays.npz');d=z['data'];p=z['predictions'];b=z['blanks'];n=z['numerical_discrepancy'];ratios=z['training_ratio']
    tr,va,gu=regions();extension=np.zeros(XX.shape,bool)
    # Rectangle hulls of described source features; not recovered source segmentation.
    # Include finite bin halfwidth and20arcsec beamguard; velocity guard8.24km/s.
    source_boxes=[([-260,-94],[-78,-24],[-75,-25]),([94,190],[24,78],[0,60])]
    for xr,zr,ur in source_boxes:
        for sign in [-1,1]:
            xr0,xr1=sorted(np.array(xr)*sign);zr0,zr1=sorted(np.array(zr)*sign);ur0,ur1=sorted(np.array(ur)*sign)
            extension|=((XX>=xr0-30)&(XX<=xr1+30)&(ZZ>=zr0-30)&(ZZ<=zr1+30)&(UU>=ur0-14.42)&(UU<=ur1+14.42))
    records=[];arr={'extension_exclusion':extension}
    for radius in [40,60,80]:
        safe=outside_features(radius,20)&~extension
        for region,reg in [('validation',va),('guarded',gu)]:
            mask=reg&safe
            for ku in [2,3]:
                use=boxes(mask.astype(int),ku)==ku*4;db=boxes(d,ku);pb=boxes(p,ku);bb=boxes(b,ku);num=boxes(n,ku)
                sd=bb.std(0,ddof=1);sd=np.maximum(sd,np.median(sd)*.5)
                for gate in [1.1,1.25,1.5]:
                    keep=ratios<=gate;lo=pb[keep].min(0)-num;hi=pb[keep].max(0)+num
                    dist=np.where(db>hi,db-hi,np.where(db<lo,db-lo,0))/sd
                    idx=np.argmax(np.where(use,abs(dist),-1));k,j,i=np.unravel_index(idx,dist.shape)
                    records.append({'known_localized_radius_arcsec':radius,'region':region,'velocity_bins':ku,'training_ratio_gate':gate,
                      'correlated_box_positions':int(use.sum()),'max_abs_family_distance_blank_scatter':float(abs(dist[use]).max()),
                      'top_center_major_minor_u':[float((z['X'][i]+z['X'][i+1])/2),float((z['Z'][j]+z['Z'][j+1])/2),float((z['U'][k]+z['U'][k+ku-1])/2)]})
                arr['mask_%s_r%d_ku%d'%(region,radius,ku)]=use
    (out/'results.json').write_text(json.dumps({'scope':'Post-scan source-driven broad-envelope sensitivity. Rectangular hulls, interpolation between plottedcuts and beamguard are analyst choices; no exact source mask recovered, no blindvalidation, and exclusion cannot prove physical origin or absence.', 'source_angular_velocity_hulls_majorNE_minorSE_u':source_boxes,'rows':records},indent=2)+'\n');np.savez_compressed(out/'arrays.npz',**arr)
    for r in records:
        if r['known_localized_radius_arcsec']==40 and r['training_ratio_gate']==1.1:print(r,flush=True)
if __name__=='__main__':main()
