#!/usr/bin/env python3
"""Independent small synthetic/noise controls for central cube inversion."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.ndimage import map_coordinates
from scipy.signal import fftconvolve


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    out = Path(ap.parse_args().output)
    u, z, x = np.meshgrid(np.linspace(-8, 8, 41), np.linspace(-4, 4, 33),
                          np.linspace(-7, 7, 49), indexing='ij')
    bend = 0.15*x + 0.004*x**3
    amplitude = np.exp(-0.5*(x/3.2)**2-0.5*((z-bend)/0.8)**2)
    velocity = 4.0*np.tanh(x/2.0)/(1+0.07*np.abs(z-bend))
    cube = amplitude*np.exp(-0.5*((u-velocity)/0.9)**2)
    reverse = lambda v: v[::-1, ::-1, ::-1]
    records = []

    def record(name, passed, **details):
        records.append(dict(name=name, passed=bool(passed), **details))

    zero = float(np.max(np.abs(cube-reverse(cube))))
    record('odd_warp_symmetric_lag_exact_cube_null', zero < 2e-14,
           max_absolute=zero, shape=list(cube.shape))
    # A tilted elliptical PSF is centrally symmetric without separate x/z symmetry.
    ky, kx = np.meshgrid(np.arange(-7, 8), np.arange(-9, 10), indexing='ij')
    angle = 0.43
    ka = np.cos(angle)*kx+np.sin(angle)*ky
    kb = -np.sin(angle)*kx+np.cos(angle)*ky
    sky = np.exp(-0.5*(ka/2.7)**2-0.5*(kb/1.1)**2)
    kernel = np.exp(-0.5*(np.arange(-3, 4)/0.8)**2)[:, None, None]*sky[None]
    kernel /= kernel.sum()
    smooth = fftconvolve(cube, kernel, mode='same')
    smooth_residual = float(np.max(np.abs(smooth-reverse(smooth))))
    record('rotated_elliptical_beam_preserves_central_null', smooth_residual < 2e-14,
           max_absolute=smooth_residual)
    patch = 0.05*np.exp(-0.5*((x-2.4)/0.7)**2-0.5*((z-1.1)/0.4)**2
                        -0.5*((u-3.0)/0.8)**2)
    asymmetric = cube+patch
    raw_residual = asymmetric-reverse(asymmetric)
    record('unpaired_emissivity_patch_breaks_null', float(np.max(np.abs(raw_residual))) > .04,
           max_absolute=float(np.max(np.abs(raw_residual))))
    signed_sum = float(raw_residual.sum())
    record('global_signed_sum_is_tautologically_zero_even_for_asymmetry',
           abs(signed_sum) < 1e-12, signed_sum=signed_sum,
           absolute_residual_sum=float(np.abs(raw_residual).sum()))
    mask = ~((x > 1.5) & (z > 0.4) & (u > 0))
    bad = cube*mask
    common = mask & reverse(mask)
    corrected = cube*common
    badmax = float(np.max(np.abs(bad-reverse(bad))))
    goodmax = float(np.max(np.abs(corrected-reverse(corrected))))
    record('asymmetric_coverage_fails_until_common_paired_mask', badmax > .1 and goodmax < 2e-14,
           zero_fill_max_residual=badmax, common_support_max_residual=goodmax,
           retained_fraction=float(common.mean()))
    # Four-point moment projector. Constant systemic errors cancel exactly.
    qmm = lambda a: (a-a[:, ::-1]-a[::-1, :]+a[::-1, ::-1])/4
    xx, zz = x[0], z[0]
    straight = 5*np.tanh(xx/2)/(1+0.2*np.abs(zz))
    qmax = float(np.max(np.abs(qmm(straight+3.7))))
    vertical_miscenter = 5*np.tanh(xx/2)/(1+0.2*np.abs(zz+0.17))
    qshift = float(np.max(np.abs(qmm(vertical_miscenter))))
    record('four_point_moment_cancels_systemic_but_leaks_vertical_center',
           qmax < 2e-14 and qshift > .05,
           systemic_offset_qmax=qmax, vertical_center_error_qmax=qshift)
    # Native samples of an analytically symmetric off-grid source need not remain
    # exactly symmetric after a one-sided linear interpolated reflection.
    native = np.arange(41, dtype=float)
    center = 20.23
    f = lambda a: np.exp(-0.5*((a-center)/1.4)**2)
    data = f(native)
    reflected = map_coordinates(data, [2*center-native], order=1, mode='constant', cval=np.nan,
                                prefilter=False)
    finite = np.isfinite(reflected)
    interr = float(np.max(np.abs((data-reflected)[finite])))
    analytic_err = float(np.max(np.abs(f(native)-f(2*center-native))))
    record('subpixel_linear_reflection_has_deterministic_interpolation_residual',
           interr > .02 and analytic_err < 2e-14,
           interpolated_max_residual=interr, analytic_max_residual=analytic_err,
           message='This requires a resolution/interpolator control, not a physical interpretation.')
    rng = np.random.default_rng(502320261020)
    fractions = [0.3, 0.2, 0.7]
    weights = np.array([np.prod([p if bit else 1-p for p, bit in zip(fractions, bits)])
                        for bits in np.ndindex(2, 2, 2)])
    nmc = 100000
    noise = rng.normal(size=(nmc, 16))
    diff = noise[:, :8] @ weights-noise[:, 8:] @ weights
    expected = float(2*np.dot(weights, weights))
    observed = float(np.var(diff, ddof=1))
    record('trilinear_white_noise_variance_uses_squared_weights',
           abs(observed/expected-1) < .025, expected_variance=expected,
           observed_variance=observed, incorrect_uninterpolated_variance=2.0,
           Monte_Carlo_draws=nmc)
    # Adjacent samples share a [1/4,1/2,1/4] filter. The nine-sample sum is
    # a fixed linear form with an exactly computable covariance-aware variance.
    raw = rng.normal(size=(nmc, 11))
    correlated = .25*raw[:, :9]+.5*raw[:, 1:10]+.25*raw[:, 2:11]
    sum_variance = float(np.var(correlated.sum(axis=1), ddof=1))
    exact_sum_variance = 9*.375+2*8*.25+2*7*.0625
    wrong_sum_variance = 9*.375
    record('correlated_bins_cannot_use_independent_pixel_variance',
           abs(sum_variance/exact_sum_variance-1) < .025,
           expected_covariance_aware_sum_variance=exact_sum_variance,
           observed_sum_variance=sum_variance,
           incorrect_independent_pixel_variance=wrong_sum_variance,
           variance_underestimate_factor=exact_sum_variance/wrong_sum_variance)
    result = dict(outcome='finite synthetic controls only; not an actual-cube measurement',
                  seed=502320261020, checks=records,
                  all_passed=all(v['passed'] for v in records),
                  non_claims=['No real residual significance', 'No covariance authenticated for HALOGAS',
                              'No independent replication', 'No new gravity or memory signature'])
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'all_passed':result['all_passed'], 'checks':len(records)}))
    return 0 if result['all_passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
