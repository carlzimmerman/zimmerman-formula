#!/usr/bin/env python3
"""Render measured finite-interval contrasts, without fitting or changing data."""
import argparse
import json
from pathlib import Path

import numpy as np


def plot_payload(data):
    primary = data['scenarios']['primary']
    if not primary['rows']:
        raise ValueError('cannot plot an empty empirical sample')
    obs = np.array([r['observed_D_J_dex'] for r in primary['rows']])
    pred = np.array([r['predicted_D_J_dex']['mu_exp'] for r in primary['rows']])
    cov = np.array([r['covariance_D_J_dex2'] for r in primary['rows']])
    return pred, obs, np.sqrt(cov[:, [0, 1], [0, 1]]), primary['summary']


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=here/'results.json')
    parser.add_argument('--output', type=Path, default=here/'finite_interval_results.png')
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    pred, obs, error, summary = plot_payload(data)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False})
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5))
    titles = ['Two-point response', 'Three-point curvature']
    for j, ax in enumerate(axes):
        ax.errorbar(pred[:, j], obs[:, j], yerr=error[:, j], fmt='o', ms=4,
                    color='#245979', alpha=.65, ecolor='#b1c6d4', elinewidth=.8)
        extent = [min(pred[:, j].min(), obs[:, j].min()-error[:, j].max()),
                  max(pred[:, j].max(), obs[:, j].max()+error[:, j].max())]
        ax.plot(extent, extent, '--', color='#ba6b31', lw=1.5, label='Exact agreement')
        ax.set_xlabel('Exponential prediction (dex)')
        ax.set_ylabel('Observed contrast (dex)')
        ax.set_title(titles[j], loc='left', fontweight='bold')
        ax.grid(alpha=.15)
    axes[1].axhline(0, color='gray', linewidth=.8)
    axes[0].legend(frameon=False)
    fig.suptitle(f"Finite-interval MOND tests | {summary['galaxies']} SPARC galaxies | no fitted parameters",
                 x=.07, ha='left', fontsize=14)
    fig.text(.07, .025, 'One baryon-selected triple per galaxy. Bars: catalog velocity errors only; baryonic and inter-ring systematics excluded.\n'
             'Algebraic rotation-law approximation, not a full disk-field solution. Familiar data; no independent discovery claim.',
             fontsize=9, color='#555555')
    fig.tight_layout(rect=[.025, .12, 1., .93])
    fig.savefig(args.output, dpi=160)
    plt.close(fig)
    print(args.output)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
