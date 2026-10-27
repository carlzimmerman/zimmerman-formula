"""Continuous exponential disk: boundary superposition vs published formula."""
import argparse
import json
import math
from pathlib import Path
from scipy import integrate,special
from disk_kernel import G_KPC_KMS2_MSUN as G, uniform_disk_v2_per_surface_density


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--output",required=True)
    args=parser.parse_args()
    rows=[]
    for R in (0.173,0.573,1.133,2.173,4.133,7.733):
        def integrand(a):
            return math.exp(-a)*float(uniform_disk_v2_per_surface_density(R,a))
        left,left_err=integrate.quad(integrand,0,R,epsabs=1e-13,epsrel=2e-11,limit=200)
        right,right_err=integrate.quad(integrand,R,40,epsabs=1e-13,epsrel=2e-11,limit=200)
        computed=left+right
        y=R/2
        reference=math.pi*G*R*R*(special.iv(0,y)*special.kv(0,y)-special.iv(1,y)*special.kv(1,y))
        # For a>=40>R, a disk's midplane boundary force is monotonic in R/a;
        # use its convergent positive elliptic series, or simply the bound
        # |R*dPhi/dR| <= G*R*a*2pi/(a-R) <= 2pi*G*R*40/(40-R).
        # Integrate exp(-a) over a>=40 to bound the omitted superposition.
        tail=math.exp(-40)*2*math.pi*G*R*40/(40-R)
        rows.append(dict(R_kpc=R,computed=computed,published=reference,
                         relative_error=abs(computed/reference-1),quad_abs_error_estimate=left_err+right_err,
                         continuous_outer_superposition_abs_bound=tail))
    maximum=max(r["relative_error"] for r in rows)
    result={"all_passed":bool(maximum<1e-7),"max_relative_error":float(maximum),"rows":rows,
        "formula":"pi G Sigma0 R^2/Rd [I0(R/2Rd)K0(R/2Rd)-I1(R/2Rd)K1(R/2Rd)]",
        "continuous_superposition":"Sigma0 exp(-R/Rd)=integral_R^infinity da Sigma0/Rd exp(-a/Rd); each term is a uniform disk of radius a.",
        "interpretation":"Continuous forward-kernel implementation control; no claim for any observed galaxy."}
    Path(args.output).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"all_passed":result["all_passed"],"max_relative_error":maximum}))
    if not result["all_passed"]:raise SystemExit(1)


if __name__=="__main__":main()
