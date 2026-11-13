"""Correct the FOR posterior's aperture mass prior; preserve the image likelihood.

Importance transport is exact at fixed profile shape, up to the old Monte Carlo
error. This is not a new joint SED/light-profile fit or a theory p-value.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.special import logsumexp
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[2]
OLD = ROOT / 'euclid_for_j0332_fit_2026_11_13'
sys.path.insert(0, str(OLD))
sys.path.insert(0, str(OLD / 'image_inversion'))
from fit_images_v2 import mass_logprior as original_prior
from inversion_continuous import setup
from lens_models import AqualLens

MED, LO, HI = 11.8310873126, .1041923878, .0863788677
LEVELS = [.025, .16, .5, .84, .975]


def logprior(m, shift=0.):
    d = np.asarray(m) - MED - shift
    sigma = np.where(d < 0, LO, HI)
    return -.5 * (d / sigma)**2 - np.log(sigma)


def wquantile(x, w):
    order = np.argsort(x)
    x, w = np.asarray(x)[order], np.asarray(w)[order]
    return np.interp(LEVELS, np.cumsum(w)-.5*w, x)


def main(out, fraction):
    out = Path(out)
    out.mkdir(exist_ok=True, parents=True)
    assert 0 < fraction < 1
    logf = np.log10(fraction)
    old = np.load(OLD/'gated_posterior_02/chains.npz')
    chain = old['chain'][500:]
    flat = chain.reshape(-1, 4)
    oldlp = old['logprob'][500:].reshape(-1)
    mass = flat[:, 0]
    # Two half-normal branches, each with probability 1/2; the side-dependent
    # density normalization matters. This preserves the original surrogate.
    assert np.max(np.abs(logprior(mass) - np.array([original_prior(m) for m in mass]))) < 1e-12
    areas = [quad(lambda m: np.exp(logprior(m))/np.sqrt(2*np.pi), a, b)[0]
             for a, b in [(MED-2, MED), (MED, MED+2)]]
    assert np.max(np.abs(np.array(areas)-.5)) < 1e-10
    assert np.max(np.abs(logprior(mass+np.log10(1.))-logprior(mass))) == 0
    results = {}
    for name, shift in [('catalogue_redshift', 0.), ('luminosity_distance_only', .00653358)]:
        logw = logprior(mass+logf, shift) - logprior(mass)
        weights = np.exp(logw-logsumexp(logw))
        ess = 1/np.sum(weights**2)
        assert ess > .9*len(weights), 'Insufficient overlap: new sampling required'
        qtotal = wquantile(mass, weights)
        qaper = qtotal+logf
        prior_delta = qaper[2]-MED-shift
        prior_side_sigma = LO if prior_delta < 0 else HI
        qparam = np.stack([wquantile(flat[:, j], weights) for j in range(4)], axis=1)
        chain_medians = []
        for j in range(chain.shape[1]):
            mj = chain[:, j, 0]
            lj = logprior(mj+logf, shift)-logprior(mj)
            wj = np.exp(lj-logsumexp(lj))
            chain_medians.append(float(wquantile(mj, wj)[2]))
        assert np.ptp(chain_medians) < .001
        rec = dict(aperture_fraction=fraction, log10_aperture_fraction=logf,
                   SED_logmass_shift=shift, importance_ESS=ess, n_samples=len(weights),
                   weights_min=float(weights.min()), weights_max=float(weights.max()),
                   log10_total_mass_quantiles=qtotal.tolist(),
                   total_mass_quantiles_Msun=(10**qtotal).tolist(),
                   log10_aperture_mass_quantiles=qaper.tolist(),
                   aperture_mass_quantiles_Msun=(10**qaper).tolist(),
                   parameter_quantiles=qparam.tolist(),
                   shear_quantiles=wquantile(np.hypot(flat[:, 1],flat[:, 2]),weights).tolist(),
                   required_aperture_mass_over_SED_median=float(10**(qaper[2]-MED-shift)),
                   median_difference_in_upper_SED_error_units=float((qaper[2]-MED-shift)/HI),
                   SED_survival_at_median_required_mass=float(norm.sf(prior_delta/prior_side_sigma)),
                   chain_logmass_medians=chain_medians,
                   median_logmass_change_from_original=float(qtotal[2]-np.median(mass)))
        results[name] = rec
        np.savez_compressed(out/(name+'_weights.npz'), weights=weights,
                            posterior_parameters=flat, log_mass_aperture=mass+logf)
    # Recompute five original target values from pixels and the field library.
    # This checks that the importance correction modifies the same likelihood.
    inv, lens = setup(nsource=25, source_pixel=.04, supersample=2), AqualLens()
    checks = []
    for k in [0, 2499, 5000, 7499, 9999]:
        m, g1, g2, z = flat[k]
        fit = inv.evaluate(deflection=lambda X,N: lens.deflection(X,N,m,g1,g2),
                           log_regularization=z, return_arrays=False)
        value = fit['score']+logprior(m)-.5*((g1/.1)**2+(g2/.1)**2)
        checks.append(float(value-oldlp[k]))
    assert max(map(abs, checks)) < 1e-7
    lognew = oldlp+logprior(mass+logf)-logprior(mass)
    best = int(np.argmax(lognew))
    m,g1,g2,z = flat[best]
    fit = inv.evaluate(deflection=lambda X,N: lens.deflection(X,N,m,g1,g2),
                       log_regularization=z, return_arrays=True)
    xy = np.array(json.loads((OLD/'inputs/dataset/positions.json').read_text())['arguments']['values']['array'])
    X,N = xy[:,1],-xy[:,0]
    ax,an = lens.deflection(X,N,m,g1,g2)
    src = np.array([X-ax,N-an]).T
    diameter = float(np.sqrt(np.max(np.sum((src[:,None]-src[None,:])**2,axis=-1))))
    assert diameter <= .3
    np.savez_compressed(out/'representative_fit.npz',source=fit['source'],
                        model_valid=fit['model_valid'],mask=inv.mask,data=inv.data,noise=inv.noise)
    result = dict(assertion_tested='Fixed-shape FOR image posterior with finite-mask stellar-mass normalization corrected by exact importance weights',
                  quantile_levels=LEVELS,parameter_order=['log10_Mtotal','g1','g2','ln_source_precision'],
                  prior_MED_LO_HI_dex=[MED,LO,HI],prior_half_integrals=areas,
                  target_recompute_differences=checks,scenarios=results,
                  representative_sample=dict(scenario='catalogue_redshift',parameters=flat[best].tolist(),
                       log10_aperture_mass=float(m+logf),association_diameter_arcsec=diameter,
                       chi2=fit['chi2'],n_pixels=fit['n_pixels'],
                       source_negative_fraction=fit['negative_source_fraction']),
                  non_claims=['Fixed light profile and constant stellar M/L extrapolated beyond aperture',
                       'No new joint stellar-population, shape, IMF, environment, or covariance posterior',
                       'Importance ESS is not the autocorrelation-corrected MCMC ESS',
                       'SED survival is not a goodness-of-fit p-value or theory probability',
                       'Unscreened smooth galaxy branch only; not full screened covariant model'])
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',required=True)
    parser.add_argument('--aperture-fraction',required=True,type=float)
    args=parser.parse_args()
    main(args.output,args.aperture_fraction)
