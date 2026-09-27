#!/usr/bin/env python3
"""Reproduce a deliberately conditional screen of SPT-3G x DES Y3 Pol results.

The published cross-spectrum amplitude is not a likelihood for an arbitrary
gravity model. In particular, the square of a single-redshift sigma8 ratio is
only a uniform-power *proxy*, not this theory's C_ell^(kappa gamma).
"""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
XR32_EXTRACT = HERE / "spt_pol_growth_input.json"
OUTPUT = HERE / "spt_pol_screen_result.json"

# Ouellette et al. (2026), arXiv:2606.26223v2, Tables 4 and 5.
POL_AMP = 1.02
POL_AMP_SIGMA = 0.073
POL_S8 = 0.833
POL_S8_LOWER_ERROR = 0.061
POL_S8_UPPER_ERROR = 0.047
RAW_GMV_AMP = 0.86  # Foreground-biased estimator: included as a warning, not a fit.


def calculate() -> dict:
    source = json.loads(XR32_EXTRACT.read_text())
    base_s8 = float(source["planck_baseline_S8"])
    model_s8 = float(source["nominal_conversion_S8_z0"])
    ratios = {z: float(source["nominal_linear_sigma8_ratio_by_z"][z]) for z in ("0.0", "0.5", "1.0", "2.0")}
    assert abs(model_s8 / base_s8 - ratios["0.0"]) < 1e-4

    # A fixed-template, split-normal one-dimensional check. This is a posterior
    # coordinate comparison, not a fit of the conversion model to the bandpowers.
    s8_offset = POL_S8 - model_s8
    s8_sigma = POL_S8_LOWER_ERROR if model_s8 < POL_S8 else POL_S8_UPPER_ERROR

    # If growth suppression were independent of scale and constant over the
    # entire cross-lensing kernel, power would scale like (sigma8 ratio)^2.
    # Evaluating at separate redshifts exposes why z=0 cannot stand in for a
    # broad line-of-sight C_ell projection.
    proxy = {}
    for z, ratio in ratios.items():
        amp = ratio * ratio
        proxy[z] = {
            "sigma8_ratio": ratio,
            "uniform_power_amplitude_proxy": amp,
            "pol_amplitude_residual_in_reported_sigma": (POL_AMP - amp) / POL_AMP_SIGMA,
        }

    return {
        "source": {
            "cross_paper": "https://arxiv.org/html/2606.26223v2",
            "cross_tables": [4, 5],
            "xr32_input_extract": XR32_EXTRACT.name,
            "xr32_original_sha256": source["source_sha256"],
        },
        "published": {
            "full_pol_A_planck": POL_AMP,
            "full_pol_A_planck_sigma": POL_AMP_SIGMA,
            "full_pol_S8": POL_S8,
            "full_pol_S8_lower_error": POL_S8_LOWER_ERROR,
            "full_pol_S8_upper_error": POL_S8_UPPER_ERROR,
            "raw_gmv_A_planck_foreground_biased": RAW_GMV_AMP,
        },
        "xr32_nominal": {
            "planck_baseline_S8": base_s8,
            "conversion_linear_S8_at_z0": model_s8,
        },
        "s8_coordinate_screen": {
            "difference_pol_minus_xr32": s8_offset,
            "residual_in_published_lower_1sigma_error": s8_offset / s8_sigma,
            "conditional_only": True,
        },
        "uniform_power_proxy_by_redshift": proxy,
        "limitations": [
            "No action-derived metric-potential transfer or nonlinear cross-spectrum is supplied.",
            "Published S8 is marginalized in a Lambda-CDM plus IA model; it is not an action-level likelihood.",
            "No numerical 96-point Full x Pol bandpowers and covariance were verified public.",
            "The proxy has neither the DES source-redshift kernels nor the paper's inverse-covariance weights.",
            "SPT auto-lensing and this cross-spectrum reuse maps and cannot be multiplied as independent.",
        ],
    }


def main() -> None:
    result = calculate()
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
