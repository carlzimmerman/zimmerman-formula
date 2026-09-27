#!/usr/bin/env python3
"""Spatial smoothing at a MOND zero, and a separate source-sensitivity control.

Fixed periodic flat geometry, dimensionless a0=1, one Fourier-coordinate
dependence embedded in T^3. All accelerations stay below the phantom peak,
where the operative nu_mono is exactly nu_RAR. No interpolated kernel table.
"""
import argparse,json
from pathlib import Path
import numpy as np
import sympy as s


def phantom(a):
    y=np.abs(a)
    h=np.zeros_like(y)
    nz=y>0
    h[nz]=y[nz]/np.expm1(np.sqrt(y[nz]))
    return np.sign(a)*h


def sample(n,xi,eps):
    x=2*np.pi*np.arange(n)/n
    k=np.fft.fftfreq(n,d=1/n)
    inner=np.exp(-xi*xi/2)*eps*np.sin(x)
    ff=phantom(inner)
    fh=np.fft.fft(ff)/n
    heat=np.exp(-xi*xi*k*k/2)
    # 1D longitudinal projector is identity except at the zero mode.
    heat[k==0]=0
    force=np.fft.ifft(n*heat*fh).real
    deriv=np.fft.ifft(n*1j*k*heat*fh).real
    rawderiv=np.fft.ifft(n*1j*k*fh).real
    # Untruncated bound: discrete sum plus rigorous Gaussian integral tail.
    # f(t)=t²e^(-xi²t²) is decreasing for t>=1/xi.
    cut=max(64,int(np.ceil(12/xi)))
    kk=np.arange(1,cut+1,dtype=float)
    # For t>=cut, t² <= exp(xi² t²/2)/xi² for cut*xi>=12.
    # Gaussian tail <= exp(-xi² cut²/2)/(xi² cut).
    tail=2*np.exp(-xi*xi*cut*cut/2)/(xi**4*cut)
    bound2=2*np.sum(kk*kk*np.exp(-xi*xi*kk*kk))+tail
    f_norm=float(np.sqrt(np.mean(ff*ff)))
    bound=float(np.sqrt(bound2)*f_norm)
    maximum=float(np.max(np.abs(deriv)))
    assert maximum<=bound*(1+1e-12)
    assert np.max(np.abs(inner))<2.5396
    assert np.isfinite(force).all() and np.isfinite(deriv).all()
    return {'n':n,'xi':xi,'source_amplitude':eps,'phantom_L2':f_norm,
            'force_L2':float(np.sqrt(np.mean(force*force))),
            'filtered_max_spatial_derivative':maximum,
            'unfiltered_max_spectral_derivative':float(np.max(np.abs(rawderiv))),
            'spectral_Lipschitz_bound':bound,'bound_sum_tail_upper':float(tail)}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    rows=[sample(n,xi,.2)for xi in [.05,.1,.2] for n in [512,1024,2048,4096,8192]]
    convergence=[]
    for xi in [.05,.1,.2]:
        rr=[r for r in rows if r['xi']==xi]
        rel=abs(rr[-1]['filtered_max_spatial_derivative']/rr[-2]['filtered_max_spatial_derivative']-1)
        assert rel<.001
        assert rr[-1]['unfiltered_max_spectral_derivative']>2*rr[0]['unfiltered_max_spectral_derivative']
        convergence.append({'xi':xi,'last_refinement_relative_change':rel})
    # Source changes remain only Holder at a zero. The outer heat operator
    # smooths space; it does not linearize sqrt(epsilon) dependence on data.
    sens=[sample(8192,.1,eps)for eps in [1e-4,1e-6,1e-8,1e-10]]
    for row in sens:
        row['force_over_source_amplitude']=row['force_L2']/row['source_amplitude']
        row['force_over_sqrt_source']=row['force_L2']/np.sqrt(row['source_amplitude'])
    assert sens[-1]['force_over_source_amplitude']>900*sens[0]['force_over_source_amplitude']
    assert abs(sens[-1]['force_over_sqrt_source']/sens[-2]['force_over_sqrt_source']-1)<.001
    k,xi=s.symbols('k xi',positive=True)
    gaussian=s.integrate(k**4*s.exp(-xi*xi*k*k),(k,0,s.oo))*4*s.pi
    exact=s.simplify(gaussian-3*s.pi**s.Rational(3,2)/(2*xi**5))
    assert exact==0
    out={'scope':'Fixed-geometry spatial Lipschitz force, not full coupled Cauchy closure',
         'refinement':rows,'convergence':convergence,'source_sensitivity':sens,
         'continuum_R3_gradient_heat_bound_constant':'sqrt(3)/(4*pi^(3/4)*xi^(5/2))',
         'gaussian_integral_identity_residual':str(exact),
         'non_claims':['No spatially uniform derivative bound as xi tends to zero',
                       'No source-to-force Lipschitz estimate at vanishing acceleration',
                       'No metric/lapse/filter variation or nonlinear gravitational wellposedness',
                       'R3 L2 estimate is conditional on phantom L2 integrability; an isolated MOND 1/r tail is not L2']}
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'refinement_cases':len(rows),'source_cases':len(sens),'passed':True,'max_last_relative_change':max(r['last_refinement_relative_change']for r in convergence)}))


if __name__=='__main__':main()
