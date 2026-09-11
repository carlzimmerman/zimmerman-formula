#!/usr/bin/env python3
"""Finite-volume radial spectrum of the action-derived lapse operator.

Fixed constrained Gaussian initial slices, gamma=0. The domain is 0<r<10R
with center regularity and stated outer boundary. Not a static halo solution.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
from scipy.linalg import eigh
from scipy.special import gammainc
import sympy as s

HERE=Path(__file__).resolve().parent


@lru_cache(maxsize=1)
def gap_function():
    data=json.loads((HERE/'run_002/density.json').read_text())
    assert all(data['checks'].values())
    rho=s.Symbol('rho');H,M,m,v=s.symbols('H M2 m v')
    expression=s.sympify(data['stationary_full_gap'],locals={'rho':rho,'H':H,'M2':M,'m':m,'v':v})
    fixed=expression.subs({H:s.sqrt(s.Rational(4,15)),M:1,m:s.Rational(1,10),v:s.Rational(1,2)})
    assert fixed.free_symbols <= {rho}
    return s.lambdify(rho,fixed,'numpy')


def spectrum(eta,width,n,outer='dirichlet'):
    if eta<0 or width<=0 or n<8 or outer not in ('dirichlet','neumann'):
        raise ValueError('invalid density, radius, mesh or boundary')
    faces=np.linspace(0.,10.,n+1);x=(faces[1:]+faces[:-1])/2;dx=faces[1]
    def metric(xx):
        integral=eta*np.sqrt(np.pi)/4*gammainc(1.5,xx*xx)
        ff=1-np.divide(integral,xx,out=np.zeros_like(xx),where=xx!=0)
        if np.min(ff)<=0:raise ValueError('metric patch not regular')
        return 1/np.sqrt(ff)
    ac=metric(x);af=metric(faces)
    weights=ac*np.diff(faces**3)/3
    conductance=faces**2/af/dx
    stiffness=np.zeros((n,n))
    for j in range(1,n):
        c=conductance[j]
        stiffness[j-1,j-1]+=c;stiffness[j,j]+=c
        stiffness[j-1,j]-=c;stiffness[j,j-1]-=c
    # Dirichlet face is half a cell from the last unknown. Center flux is zero.
    if outer=='dirichlet':stiffness[-1,-1]+=2*conductance[-1]
    background=float(gap_function()(0.))
    local_gap=gap_function()(eta*np.exp(-x*x)/width**2)*width**2
    operator=stiffness+np.diag(weights*local_gap)
    eigen,vectors=eigh(operator,np.diag(weights),subset_by_index=(0,2))
    residual=np.linalg.norm(operator@vectors-weights[:,None]*vectors*eigen,axis=0)
    denominator=np.linalg.norm(operator@vectors,axis=0)+np.linalg.norm(weights[:,None]*vectors*eigen,axis=0)
    # For the small Neumann homogeneous eigenvalue, use absolute residual too;
    # a cancellation-dominated relative residual is not treated as an instability.
    assert np.max(residual)<1e-8
    assert eigen[0]>=background*width**2-1e-10
    return dict(eta=eta,width=width,n=n,outer=outer,scaled_eigenvalues=eigen.tolist(),
        shifted_scaled_eigenvalues=(eigen-background*width**2).tolist(),
        maximum_eigen_residual=float(max(residual)),maximum_relative_eigen_residual=float(max(residual/denominator)),
        minimum_scaled_local_gap=float(min(local_gap)),background_scaled_gap=background*width**2)


def run():
    rows=[spectrum(eta,width,n,outer) for eta in (0.,1e-6,.01,1.)
          for width in (.03,.003,.0003) for n in (64,128,256)
          for outer in ('dirichlet','neumann')]
    similarities=[]
    for eta in (0.,1e-6,.01,1.):
        for n in (64,128,256):
            for outer in ('dirichlet','neumann'):
                selected=[row for row in rows if row['eta']==eta and row['n']==n and row['outer']==outer]
                vals=np.array([row['shifted_scaled_eigenvalues'] for row in selected])
                error=float(np.max(np.ptp(vals,axis=0)))
                assert error<1e-9
                similarities.append(error)
    return dict(cases=rows,maximum_similarity_error=max(similarities),
        scaling='R²(lambda_j(R)-mu_background²) depends on eta=rho_center R², not R separately, with domain r<10R',
        boundaries='regular center; outer Dirichlet and Neumann separately',
        non_claims=['not infinite-domain or continuum spectral certification',
                    'not k=0 count for unrestricted spacetime',
                    'not static halo or dust depletion','not a physical response pole'],full_theory_status='OPEN')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path)
    parser.add_argument('--verify',action='store_true')
    args=parser.parse_args()
    if args.verify:
        subprocess.run([sys.executable,'-m','unittest','discover','-s',str(HERE),'-p','test_spectrum.py'],check=True)
        lean=HERE.parents[1]/'clock_constitutive_construction_2026/lean_formalization_2026'
        subprocess.run(['/opt/homebrew/bin/lake','env','lean',str(HERE/'SpectrumBound.lean')],cwd=lean,check=True)
    result=run()
    if args.result_file:args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(cases=len(result['cases']),maximum_similarity_error=result['maximum_similarity_error'],
                         maximum_eigen_residual=max(row['maximum_eigen_residual'] for row in result['cases']),
                         full_theory_status='OPEN'),indent=2))
