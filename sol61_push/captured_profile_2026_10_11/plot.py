"""Render existing recorded results; no new scientific calculation."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

folder = Path(__file__).resolve().parent
data = json.loads((folder/'refinement_run/results.json').read_text())
edges = np.array(data['edges'])
rows = [c for c in data['cells'] if c['n']==10]
mask = (edges>=.05)&(edges<=.4)
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), constrained_layout=True)
colors = ['#175e91', '#c66a24']
for row, color in zip(rows, colors):
    label = 'Contraction T='+str(int(row['duration']))
    axes[0].plot(edges[mask], row['shape_scores']['repaired']['normalized_observed'],
                 'o-', color=color, label=label, markersize=4)
    axes[1].plot(edges, np.array(row['mass_below'])/.001,
                 'o-', color=color, label=label, markersize=3)
for key, label, color, linestyle in [('repaired','Repaired target','#26744c','--'),
                                     ('exponential','Exponential target','#595959',':')]:
    axes[0].plot(edges[mask], rows[0]['shape_scores'][key]['normalized_target'],
                 color=color, linestyle=linestyle, label=label, linewidth=2)
axes[0].set(xscale='log', xlabel='Radius (G=M=a0=1 for target overlay)',
            ylabel='Conditional mass fraction in 0.05 < r < 0.4',
            title='Inner annular shape', ylim=(-.02, 1.02))
axes[1].set(xscale='log', yscale='log', xlabel='Radius (G=M=1)',
            ylabel='Orbit-averaged mass / initial reservoir mass',
            title='Same input mass, strong assembly memory')
for ax in axes:
    ax.grid(alpha=.18)
    ax.legend(frameon=False, fontsize=9)
fig.suptitle('Capture profile diagnostic: prescribed source, no cold self-gravity',fontsize=13)
fig.savefig(folder/'profile_comparison.png', dpi=170)
plt.close(fig)
