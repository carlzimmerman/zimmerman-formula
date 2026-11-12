#!/usr/bin/env python3
"""Bounded exact identity/counterexample check; no observed galaxy or a0 fit."""
from fractions import Fraction as F
from pathlib import Path
import json
import math
import hashlib
import sys

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'route_spectral_run_001' / 'results.json'
k = F(1, 1000)  # Toy calibrated arcsec per (km/s); not an instrument assertion.


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def image(x, v, direction, translation):
    return tuple(xi + k*v*ei + ai for xi, ei, ai in zip(x, direction, translation))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


velocities = [F(v) for v in [-250, -100, 0, 100, 250]]
cases = 0
for v1 in velocities:
    for v2 in velocities:
        for morphology in [F(-7, 10), F(0), F(13, 10)]:
            for offset in [F(-1, 10), F(0), F(2, 10)]:
                x1, x2 = (morphology, F(3, 10)), (F(9, 10), F(-2, 10))
                plus, minus = (F(1), F(0)), (F(-1), F(0))
                tp, tm = (offset, F(7, 100)), (-offset, F(-2, 100))
                dp = sub(image(x1, v1, plus, tp), image(x2, v2, plus, tp))
                dm = sub(image(x1, v1, minus, tm), image(x2, v2, minus, tm))
                recovered = dot(plus, sub(dp, dm)) / (2*k)
                assert recovered == v1-v2
                # Orthogonal invariant: sky morphology from the pair average.
                assert tuple((a+b)/2 for a, b in zip(dp, dm)) == sub(x1, x2)
                # Non-opposite unit-vector pair, with the same centroid weights.
                other = (F(3, 5), F(4, 5))
                dj = sub(image(x1, v1, other, tm), image(x2, v2, other, tm))
                de = sub(plus, other)
                assert dot(de, sub(dp, dj))/(k*dot(de, de)) == v1-v2
                cases += 1
assert cases == 225

# Zero true velocity, but a spatially varying unresolved [NII]/Halpha ratio.
# Approximate vacuum wavelengths in nm; fixed 6549:6584 flux ratio 1:3.
c = F(299792458, 1000)  # km/s, exact SI speed of light converted.
ha, nii_blue, nii_red = F(656461, 1000), F(654986, 1000), F(658527, 1000)
def blend_velocity(r):
    return c/ha * r*((nii_red-ha)+(nii_blue-ha)/3)/(1+4*r/3)
blend_delta = blend_velocity(F(1, 2))-blend_velocity(F(1, 10))
assert blend_delta > 150

# Opposite-pair second moments are nonidentifying with one direction.
# C_x,xx + k^2 Var(v) is identical in two positive-covariance models,
# and Cov(x,v)=200 in both, so the odd covariance is also identical.
moments = []
for spatial_variance, velocity_variance in [(F(1), F(40000)), (F(99,100), F(50000))]:
    b = F(200)
    assert spatial_variance*velocity_variance-b*b >= 0
    moments.append((spatial_variance+k*k*velocity_variance, 4*k*b))
assert moments[0] == moments[1]

z = 0.6959
lam = float(ha)*(1+z)
dispersion_blue = 0.3/1.239  # arcsec/nm: nominal native scale/dispersion.
kk = dispersion_blue*lam/float(c)
i = math.radians(54)
e055 = 0.055
centroid_sigma_snr10 = 0.530/2.355/10
result = {
    'assertion_tested': '225 exact rational centroid and morphology-cancellation cases; exact two-model second-moment degeneracy; stationary blended-line counterexample.',
    'exact_cases': cases,
    'centroid_identity_passed': True,
    'second_moment_degeneracy_passed': True,
    'zero_true_velocity_blend_false_difference_kms': float(blend_delta),
    'blend_inputs': {'r_NII6584_to_Halpha': [0.1, 0.5], 'vacuum_wavelengths_nm': [float(ha), float(nii_blue), float(nii_red)]},
    'illustrative_blue_scale_only': {
        'z': z, 'lambda_observed_nm': lam, 'k_arcsec_per_kms': kk,
        'four_degree_vs_opposite_noise_penalty': 1/math.sin(math.radians(2)),
        'single_centroid_sigma_arcsec_at_SNR10_PSF_only': centroid_sigma_snr10,
        'delta_v_sigma_kms_four_centroids_SNR10': centroid_sigma_snr10/kk,
        'W_half_delta_v_sigma_kms_SNR10': centroid_sigma_snr10/(2*kk),
        'relative_clump_double_difference_bias_kms_for_0p02arcsec': 0.02/(2*kk),
        'BTFR_velocity_only_sigma_dex_W204': 4*(centroid_sigma_snr10/(2*kk))/204/math.log(10),
    },
    'BTFR_sensitivity_not_a_data_fit': {
        'inclination54deg_error5deg_log10a_error':4/math.log(10)*math.cos(i)/math.sin(i)*math.radians(5),
        'gas_missing_fraction_bias_dex': {str(f):-math.log10(1-f) for f in [0.3,0.5]},
        'thin_disk_overestimate_dex_if_true_thickness_q0': {str(q):-2*math.log10(1-q*q) for q in [0.2,0.3,0.4]},
        'separate_component_ceiling_for_0p055dex': {
            'fractional_velocity':e055*math.log(10)/4,
            'inclination_error_degrees_at54':math.degrees(e055*math.log(10)/4*math.tan(i)),
            'fractional_mass_linearized':e055*math.log(10),
        },
    },
    'non_claims': ['No real velocity measurement validated.', 'No rotation curve or Vflat inferred.', 'No inclination recovered without a shape model.', 'No gas mass measured.', 'No a0 or normalization fitted.', 'No guarantee opposite grism exposures exist for a given target.'],
    'original_repository_input_hashes_unchanged': {},
}
inputs = json.loads((ROOT/'route_spectral_inputs.json').read_text())
for row in inputs['repository_inputs']:
    same = hashlib.sha256(Path(row['path']).read_bytes()).hexdigest() == row['sha256']
    result['original_repository_input_hashes_unchanged'][row['path']] = same
    assert same
OUT.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
