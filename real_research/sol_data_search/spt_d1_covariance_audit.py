#!/usr/bin/env python3
"""Audit information localization in the public SPT-3G D1 kk data release.

Requires numpy and the official spt_candl_data repository at the pinned commit
given in SPT_D1_RELEASE_AUDIT.md. This is data linear algebra, not a theory fit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np


PINNED_COMMIT = "efe35b7bfd815a115d5123e210a6849a4175bc81"
HERE = Path(__file__).resolve().parent


def read_variant(release: Path, variant: str) -> dict:
    base = release / "spt_candl_data/SPT3G_D1_KK_v0" / variant
    paths = {
        "bandpowers": base / f"SPT3G_D1_KK_{variant}_bdp.txt",
        "covariance": base / f"SPT3G_D1_KK_{variant}_cov_CMBmarg.txt",
        "windows": base / "windows/kk_window_functions.txt",
    }
    d = np.loadtxt(paths["bandpowers"])
    C = np.loadtxt(paths["covariance"])
    W = np.loadtxt(paths["windows"])
    assert d.shape == (17,) and C.shape == (17, 17) and W.shape[1] == 18
    assert np.allclose(C, C.T, rtol=1e-12, atol=0)
    assert np.linalg.eigvalsh(C).min() > 0
    assert np.all(W[:, 1:] >= 0)
    ell = W[:, 0]
    weights = W[:, 1:]
    effective_ell = np.sum(ell[:, None] * weights, axis=0) / np.sum(weights, axis=0)

    # A data-vector self-template is chosen only to diagnose how the released
    # covariance localizes amplitude sensitivity among nested multipole bins.
    # Q is not a goodness-of-fit statistic or a significance for a gravity model.
    q_all = float(d @ np.linalg.solve(C, d))
    q_cholesky = float(np.linalg.norm(np.linalg.solve(np.linalg.cholesky(C), d)) ** 2)
    assert np.isclose(q_all, q_cholesky, rtol=1e-10)
    prefixes = {}
    for n in (4, 8, 12, 17):
        q = float(d[:n] @ np.linalg.solve(C[:n, :n], d[:n]))
        prefixes[str(n)] = {
            "max_effective_ell": float(effective_ell[n - 1]),
            "quadratic_norm": q,
            "fraction_of_full_quadratic_norm": q / q_all,
        }
    assert all(prefixes[str(a)]["quadratic_norm"] <= prefixes[str(b)]["quadratic_norm"] + 1e-8
               for a, b in ((4, 8), (8, 12), (12, 17)))
    return {
        "file_sha256": {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in paths.items()},
        "n_bins": len(d),
        "window_ell_range": [int(ell[0]), int(ell[-1])],
        "effective_ell": [float(x) for x in effective_ell],
        "covariance_min_eigenvalue": float(np.linalg.eigvalsh(C).min()),
        "quadratic_norm": q_all,
        "prefixes": prefixes,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("release", type=Path, help="Checkout of SouthPoleTelescope/spt_candl_data")
    p.add_argument("--output", type=Path, default=HERE / "spt_d1_covariance_result.json")
    args = p.parse_args()
    rev = subprocess.check_output(["git", "-C", str(args.release), "rev-parse", "HEAD"], text=True).strip()
    if rev != PINNED_COMMIT:
        raise SystemExit(f"Expected pinned release {PINNED_COMMIT}; found {rev}")
    out = {
        "source": "https://github.com/SouthPoleTelescope/spt_candl_data",
        "commit": rev,
        "observable": "SPT-3G D1 C_L^(kappa kappa)",
        "covariance_choice": "CMB-marginalized lensing-only",
        "metric": "d_prefix^T C_prefix^-1 d_prefix, self-template diagnostic only",
        "variants": {name: read_variant(args.release, name) for name in ("PP", "GMV", "GMVprof")},
    }
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
