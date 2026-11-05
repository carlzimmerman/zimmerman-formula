"""Regression for radial angular-source cancellation and Hessian convergence."""
import argparse,importlib,json,time
from pathlib import Path
from scipy.sparse import diags
from refine import grid,geometric_tests


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);ap.add_argument('--operator',choices=['v1','v2'],required=True)
    args=ap.parse_args();J=importlib.import_module('generalized' if args.operator=='v1' else 'generalized_v2');M,np=J.M,J.np
    out=dict(operator=args.operator,checks=[],all_checks_pass=False);start=time.monotonic()
    for refinement in (1,2,3,4):
        g,mu=grid('canonical',refinement);sol=M.Solver(g,mu,M.C.A0['canonical']);model=J.Generalized(sol)
        angular=(model.hess[2]+model.hess[3]-2*diags(1/g.r2d)@g.Crr).tocsr()
        w=g.vol
        weighted=diags(w)@angular;skew=weighted-weighted.T
        skewrel=float(np.max(np.abs(skew.data))/np.max(np.abs(weighted.data))) if skew.nnz else 0.
        rb=np.exp(-g.r2d*g.r2d/100)
        residual=angular.T@(w*rb);scale=abs(angular).T@(w*rb)
        use=scale>1e-100
        cancellation=float(np.max(abs(residual[use])/scale[use]))
        controls=geometric_tests(model)
        row=dict(refine=refinement,weighted_angular_symmetry_relative=skewrel,
            radial_angular_source_cancellation_relative=cancellation,controls=controls)
        out['checks'].append(row);args.output.write_text(json.dumps(out,indent=2)+'\n');print(row,flush=True)
        assert skewrel<1e-12 and cancellation<1e-12
        assert max(c['spurious_polar_relative_max'] for c in controls['spherical_force'])<1e-6
    first,last=out['checks'][0]['controls'],out['checks'][-1]['controls']
    assert last['axial_quadratic_boundary_max']<first['axial_quadratic_boundary_max']
    assert last['axial_quadratic_interior_max']<first['axial_quadratic_interior_max']
    assert last['plummer_hessian_relative_max']<.001
    assert max(c['radial_relative_max'] for c in last['spherical_force'])<.003
    out['all_checks_pass']=True;out['runtime_seconds']=time.monotonic()-start
    args.output.write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__':main()
