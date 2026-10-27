"""Deterministic controls; invoke through the audit runner, not on import."""
import argparse
import json
import math
from pathlib import Path
import time

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy import special

from disk_kernel import (G_KPC_KMS2_MSUN as G, build_annular_kernel,
    uniform_disk_v2_per_surface_density as disk, thin_uniform_disk_v2_per_surface_density as thindisk,
    ring_v2_direct_angle, ring_v2_elliptic, vertical_tail_mass)


def direct_volume(R,lo,hi,h,vertical,order):
    """Original ring-force integral; Duffy triangles around (a=R,z=0)."""
    nodes,weights=leggauss(order)
    u=(nodes+1.0)/2.0; w=weights/2.0
    uu=u[:,None]; vv=u[None,:]; ww=w[:,None]*w[None,:]
    Z=24*h
    norm=1.0-vertical_tail_mass(vertical,24)
    def integrand(a,z):
        t=z/h
        if vertical=="exponential":
            profile=np.exp(-t)/h/norm
        else:
            e=np.exp(-2*t);profile=4*e/(1+e)**2/h/norm
        return 2*a/(hi*hi-lo*lo)*profile*ring_v2_elliptic(R,a,z)
    result=0.0
    segments=[]
    if lo<R<hi:
        segments=[(-1.0,R-lo),(1.0,hi-R)]
    elif R==lo:
        segments=[(1.0,hi-R)]
    elif R==hi:
        segments=[(-1.0,R-lo)]
    if segments:
        for sign,L in segments:
            x1=L*uu; z1=Z*uu*vv
            x2=L*uu*vv; z2=Z*uu
            result+=float(np.sum(ww*L*Z*uu*(integrand(R+sign*x1,z1)+integrand(R+sign*x2,z2))))
    else:
        a=lo+(hi-lo)*uu; z=Z*vv
        result=float(np.sum(ww*(hi-lo)*Z*integrand(a,z)))
    return result


def relative(actual,expected):
    return float(np.max(np.abs(np.asarray(actual)/np.asarray(expected)-1.0)))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    start=time.monotonic()
    checks=[]
    def record(name, passed, **details):
        checks.append(dict(name=name,passed=bool(passed),**details))

    # Direct Green-function angular derivative, includes interior negative sign.
    ringrows=[]
    for R,a,z in [(0.3,1.0,0.0),(2.0,1.0,0.0),(1.0,1.0,0.05),
                  (0.99,1.0,0.02),(1.01,1.0,0.02),(1.7,0.6,0.4)]:
        exact=float(ring_v2_elliptic(R,a,z));raw=ring_v2_direct_angle(R,a,z)
        err=abs(exact/raw-1)
        ringrows.append(dict(R=R,a=a,z=z,elliptic=exact,direct_angular=raw,relative_error=err))
    record("ring_elliptic_vs_original_angular",max(r["relative_error"] for r in ringrows)<2e-10,rows=ringrows)
    record("interior_ring_pulls_outward",ringrows[0]["elliptic"]<0 and ringrows[1]["elliptic"]>0)

    # Boundary-integral identity compared to independent inside/outside formula.
    radii=np.array([0.01,0.2,0.7,0.99,1.01,1.5,4.0,50.0])
    error=relative(disk(radii,1.0,0.0),thindisk(radii,1.0))
    record("uniform_thin_disk_boundary_vs_landen",error<2e-10,max_relative_error=error,radii=radii.tolist())

    # Nonnegative mass basis retains signed exterior gravity. No shell theorem.
    K=build_annular_kernel([0.2,3.0],[0.8,1.2],0.15,order=96)
    record("finite_annulus_force_sign",K[0,0]<0 and K[1,0]>0,values=K[:,0].tolist())

    # Conservative normalization and correct finite far-field point mass limit.
    far=build_annular_kernel([1000.0],[0.0,0.4,1.2,3.0],0.2,order=96)[0]
    expected=G/1000.0
    farerror=relative(far,expected)
    record("unit_mass_far_field",farerror<1e-5,max_relative_error=farerror,values=far.tolist(),point_mass=expected)
    nearzero=build_annular_kernel([0.0],[0.0,0.8,2.0],0.2)
    record("central_symmetry",np.all(nearzero==0),values=nearzero.tolist())
    # Uniform subdivision telescopes exactly at each common height.
    R=np.array([0.1,0.8,1.7,2.4,3.2])
    edges=np.array([0,0.3,0.7,1.1,1.8,2.5])
    mass=math.pi*np.diff(edges**2)
    piece=build_annular_kernel(R,edges,0.2,order=96)@mass
    whole=build_annular_kernel(R,[0,2.5],0.2,order=96)[:,0]*math.pi*2.5**2
    telescope=relative(piece,whole)
    record("mass_normalization_uniform_subdivision",telescope<1e-12,max_relative_error=telescope)

    # Challenging edge/near-edge grid, no fitted displacement of target radii.
    R=np.array([0.2,0.799999,0.8,0.800001,1.0,1.199999,1.2,1.200001,2.0])
    refinement=[]
    for vertical in ("exponential","sech2"):
        for h in (0.02,0.2,0.5):
            matrices={n:build_annular_kernel(R,[0,0.8,1.2,2.5],h,vertical,order=n) for n in (48,96,192)}
            adaptive=build_annular_kernel(R,[0,0.8,1.2,2.5],h,vertical,method="adaptive")
            # Scale against G/kpc; relative-to-zero entries have no meaning.
            scale=G
            delta96=float(np.max(np.abs(matrices[96]-matrices[48]))/scale)
            delta192=float(np.max(np.abs(matrices[192]-matrices[96]))/scale)
            cross=float(np.max(np.abs(matrices[192]-adaptive))/scale)
            refinement.append(dict(vertical=vertical,h_kpc=h,delta_48_to_96_in_G_per_kpc=delta96,
                                   delta_96_to_192_in_G_per_kpc=delta192,adaptive_192_difference_in_G_per_kpc=cross))
    record("vertical_order_refinement_vs_adaptive",max(r["adaptive_192_difference_in_G_per_kpc"] for r in refinement)<1e-5,rows=refinement,scale_G_per_kpc=G,radii=R.tolist())

    # Original radial+vertical volume integration with independent ring derivative.
    volumes=[]
    for R,lo,hi,h,vertical in [(1.0,0.8,1.2,0.2,"exponential"),(0.8,0.8,1.2,0.2,"exponential"),
                              (1.0,0.8,1.2,0.02,"exponential"),(1.0,0.8,1.2,0.2,"sech2"),
                              (0.2,0.8,1.2,0.2,"exponential"),(3.0,0.8,1.2,0.2,"sech2")]:
        boundary=float(build_annular_kernel([R],[lo,hi],h,vertical,method="adaptive")[0,0])
        low=direct_volume(R,lo,hi,h,vertical,96)
        high=direct_volume(R,lo,hi,h,vertical,192)
        err=abs(high-boundary)/G
        volumes.append(dict(R=R,lo=lo,hi=hi,h=h,vertical=vertical,boundary=boundary,
                            volume96=low,volume192=high,error_in_G_per_kpc=err,
                            refinement_in_G_per_kpc=abs(high-low)/G))
    record("boundary_vs_original_ring_volume_duffy",max(r["error_in_G_per_kpc"] for r in volumes)<2e-5,rows=volumes)

    # The published Freeman disk formula, with exact exponential mass in every
    # step-function surface-density bin. Targets avoid bin-edge singularities.
    R=np.array([0.173,0.573,1.133,2.173,4.133,7.733])
    y=R/2.0
    published=math.pi*G*R**2*(special.iv(0,y)*special.kv(0,y)-special.iv(1,y)*special.kv(1,y))
    exponential=[]
    for nbin in (256,1024,4096):
        edges=np.linspace(0,24,nbin+1)
        f=lambda x: 1.0-(1.0+x)*np.exp(-x)
        masses=2*math.pi*np.diff(f(edges))
        computed=build_annular_kernel(R,edges,0.0)@masses
        exponential.append(dict(bins=nbin,computed=computed.tolist(),published=published.tolist(),max_relative_error=relative(computed,published)))
    record("published_exponential_disk_bessel_benchmark",exponential[-1]["max_relative_error"]<0.01,rows=exponential,radii=R.tolist(),vertical="razor thin",Rd_kpc=1.0,Sigma0_msun_kpc2=1.0,support_kpc=24.0,
           omitted_mass_fraction=25*math.exp(-24))

    result={"assertion_tested":"Finite enumerated benchmark controls in contract.json", "all_passed":all(r["passed"] for r in checks),
            "checks":checks,"seconds":time.monotonic()-start,
            "interpretation":"Conditional binary64 numerical implementation validation; no universal error certification or observational inference.",
            "tail_mass":{v:vertical_tail_mass(v,24) for v in ("exponential","sech2")}}
    Path(args.output).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"all_passed":result["all_passed"],"checks":len(checks),"seconds":result["seconds"]}))
    if not result["all_passed"]:
        raise SystemExit(1)


if __name__=="__main__":
    main()
