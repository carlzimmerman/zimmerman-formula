#!/usr/bin/env python3
"""Validated finite-core radial cutoff, preserving the original calculation."""
import argparse,json,math,time
from pathlib import Path
import calculate as C


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();start=time.monotonic()
    out=dict(law='full P=xQ(z)/z, z=x+ell²H:H; Q(0)=0, simple nu',
        core_prescription='rmin=max(1e-10,.001 sigma); analytic origin contacts retained; independent half/quarter-radius check recorded',footings={},checks={})
    for foot,a0 in C.old.A0.items():
        eta=C.old.GEXT/a0;rm=math.sqrt(C.old.GM/a0)
        rows=out['footings'][foot]=dict(a0=a0,eta=eta,physical_lengths={},controls={})
        point=C.quadrupole(eta,0.,nr=12000,nm=240)
        reference=C.old.quadrupole(eta,0.,0.,nr=12000,nm=240,rmin=1e-8,rmax=1e6)
        rows['controls']['plain']=C.physical(point,a0)
        out['checks'][foot+'|plain_reproduction']=abs(point['q_signed']-reference['q_hessian_signed'])<1e-9
        smooth=C.quadrupole(eta,0.,sigma=.5,nr=12000,nm=240)
        smooth_ref=C.old.quadrupole(eta,.5,0.,nr=12000,nm=240,rmin=1e-8,rmax=1e6)
        corrected_ref=smooth_ref['q_flux_signed']+smooth_ref['analytic_inner_surface']
        rows['controls']['plain_gaussian_core']=C.physical(smooth,a0)
        out['checks'][foot+'|smooth_origin_contact']=abs(smooth['q_signed']-corrected_ref)<1e-9
        rows['controls']['newtonian']=C.quadrupole(eta,1000.,sigma=.1,nr=1000,nm=40,newtonian=True)
        out['checks'][foot+'|newtonian']=rows['controls']['newtonian']['q_signed']==0.
        for length in [.03,.1,.3,1.,3.,10.]:
            ell=length*C.KPC/rm
            base=C.physical(C.quadrupole(eta,ell),a0)
            fine=C.physical(C.quadrupole(eta,ell,nr=16000,nm=320,rmin=1e-10,rmax=1e7),a0)
            rows['physical_lengths'][str(length)]=dict(base=base,fine=fine)
            scale=max(abs(fine['q_signed']),1e-12)
            out['checks'][foot+f'|{length}|refinement']=abs(base['q_signed']-fine['q_signed'])/scale<2e-4
            out['checks'][foot+f'|{length}|density']=abs(fine['flux_density_difference'])/scale<2e-4
            print(foot,length,'q_A',fine['q_A_flux'],'q_B',fine['q_B_flux'],'q',fine['q_signed'],'ratio',fine['x_ceiling'],'densitydiff',fine['flux_density_difference'],flush=True)
        ell=.03*C.KPC/rm;reg=[];point=rows['physical_lengths']['0.03']['fine']['q_signed']
        for sigma in [.5,.1,.01,.001,5e-7]:
            rr=C.physical(C.quadrupole(eta,ell,sigma,nr=12000,nm=240,rmin=max(1e-10,.001*sigma),rmax=1e7),a0)
            rr['point_relative_difference']=abs(rr['q_signed']/point-1)
            reg.append(rr)
        rows['controls']['shrinking_gaussian']=reg
        out['checks'][foot+'|point_regularization']=max(x['point_relative_difference'] for x in reg[-3:])<2e-4
        out['checks'][foot+'|regularized_density']=max(abs(x['flux_density_difference'])/max(abs(x['q_signed']),1e-12) for x in reg)<2e-4
    spherical=C.quadrupole(0.,1000.,sigma=.1,nr=1000,nm=40)
    out['controls_zero_external']=spherical
    out['checks']['zero_external']=spherical['q_signed']==0.
    core=json.loads((C.HERE/'core_debug_001/results.json').read_text())
    out['checks']['independent_core_radius_check']=core['passed']
    out['all_checks_pass']=all(out['checks'].values())
    out['runtime_seconds']=time.monotonic()-start
    out['outcome']='finite constant-external-field quadrupole, full variation and Gaussian point limit; empirical quadrature errors'
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print('all checks',out['all_checks_pass'],'runtime',out['runtime_seconds'],flush=True)
    if not out['all_checks_pass']:raise SystemExit(1)


if __name__=='__main__':main()
