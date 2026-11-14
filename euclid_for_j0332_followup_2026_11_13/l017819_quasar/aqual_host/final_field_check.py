"""Direct/refined fields at final SS6 masses; fixed-mass SS12 image checks."""
import sys,json,time,argparse
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P))
import run_host as rh
import operator_controls as oc
import numpy as np

def snapshot(dest,name,ff,m,light):
    gg=ff['grid'];np.savez_compressed(dest/(name+'.npz'),phi=ff['phi'],gr=ff['gr'],gt=ff['gt'],
        xf=gg.xf,xc=gg.xc,tf=gg.tf,tc=gg.tc,rf=gg.rf,rc=gg.rc,
        logmass=m,light=light,zl=rh.ZL,zs=rh.ZS,a0=rh.A0)
    rh.save(dest/(name+'_config.json'),dict(**rh.field_metadata(ff),logmass=m,light=light.tolist(),
        nr=gg.nr,nt=gg.nt,rmin_Re=1e-5,rmax_Re=500.,inclination=90.,zl=rh.ZL,zs=rh.ZS,
        kpc_per_arcsec=rh.SCALE,Dls_over_Ds=rh.BETA,mass_definition='infinite-total Sersic normalization',
        axisymmetric_coordinates='R,z kpc, northern hemisphere; symmetry on axis/equator',
        potential_units='(km/s)^2; additive zero at outer sphere',gradient_units='(km/s)^2/kpc'))

def main(base,control,out):
    base=Path(base);control=Path(control);out=Path(out);out.mkdir(parents=True,exist_ok=True);start=time.time();results=[]
    data=json.loads((control/'result.json').read_text())
    for result in data['fixtures']:
        tag=result['fixture'];dest=out/tag;dest.mkdir();light=np.array(result['light']);m=result['ss6_logmass_total']
        f=rh.field_for(light,m);snapshot(dest,'best_field',f,m,light)
        high=rh.field_for(light,m,nr=448,nt=80);snapshot(dest,'best_field_refined',high,m,light)
        print(json.dumps(dict(stage='fields saved',fixture=tag,logmass=m,seconds=time.time()-start)),flush=True)
        lib=np.load(base/tag/'library.npz');lmap=rh.mapped(light,lib['alpha'],lib['rad'],lib['angle'],lib['logmass'],m)
        amap=rh.project_map(f);bmap=rh.mapped(light,amap)
        rad=np.geomspace(.002,8.,192);ang=np.linspace(0,np.pi/2,97)
        ahigh=rh.project_map(high,rad,ang,nlos=256);hmap=rh.mapped(light,ahigh,rad,ang)
        np.savez_compressed(dest/'refined_map.npz',rad=rad,angle=ang,alpha=ahigh,light=light,logmass=m,zl=rh.ZL,zs=rh.ZS,a0=rh.A0)
        obj=rh.FieldAdapter(light,ns=21,step=.06,supersample=12)
        lr,lo=oc.precision_profile(obj,lmap)
        br,bo=oc.precision_profile(obj,bmap)
        hr,ho=oc.precision_profile(obj,hmap,True)
        probes=np.vstack([obj.A,obj.C,light[:2]+np.array([.4,.3]),light[:2]+np.array([-1.3,.7]),light[:2]+np.array([2.,-1.5])])
        co=np.cos(light[5]);si=np.sin(light[5]);d=probes-light[:2]
        u=co*d[:,0]+si*d[:,1];v=-si*d[:,0]+co*d[:,1]
        au,av=rh.al.projected_deflection(high,u,v,zl=rh.ZL,zs=rh.ZS,nlos=512)
        direct=np.array([co*au-si*av,si*au+co*av]);library=np.array(lmap(*probes.T));refmap=np.array(hmap(*probes.T))
        r=dict(fixture=tag,logmass_total=m,mass_msun=10**m,light=light.tolist(),
            library_ss12=rh.compact(lr),direct_mass_standard_grid_ss12=rh.compact(br),refined_ss12=rh.compact(hr),
            loglambda_library=lo['loglambda'],loglambda_direct=bo['loglambda'],loglambda_refined=ho['loglambda'],
            delta_chi2_direct_minus_library=br['chi2']-lr['chi2'],delta_score_direct_minus_library=br['score']-lr['score'],
            delta_chi2_refined_minus_library=hr['chi2']-lr['chi2'],delta_score_refined_minus_library=hr['score']-lr['score'],
            max_library_direct_ray_delta_arcsec=float(np.max(np.linalg.norm(library-direct,axis=0))),
            max_refined_map_direct_ray_delta_arcsec=float(np.max(np.linalg.norm(refmap-direct,axis=0))),
            probes=probes.tolist(),direct_LOS512=direct.tolist(),library=library.tolist(),refined_map=refmap.tolist(),
            standard_field=rh.field_metadata(f),refined_field=rh.field_metadata(high))
        rh.save(dest/'result.json',r)
        np.savez_compressed(dest/'refined_reconstruction.npz',source=hr['source'],model_valid=hr['model'],coefficient=hr['coef'],mask=obj.mask,data=obj.data,noise=obj.noise)
        results.append(r)
    rh.save(out/'result.json',dict(assertion_tested='Direct/refined AQUAL fields at the SS6 optimized masses, checked against stored library with SS12 fixed-mass precision profiles.',
        seconds=time.time()-start,fixtures=results,
        non_claims=['Fixed mass validation, not a new global fit','No proof of continuum field or source-basis convergence','No stellar-mass prior or full screened action test']))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--base',required=True);p.add_argument('--control',required=True);p.add_argument('--output',required=True);a=p.parse_args();main(a.base,a.control,a.output)
