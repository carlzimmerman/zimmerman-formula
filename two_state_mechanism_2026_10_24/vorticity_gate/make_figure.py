"""Plot accepted evidence only; no simulation or parameter selection."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

p = Path(__file__).resolve().parent
rows = json.loads((p/'run_angular256/results.json').read_text())['runs']
diag = json.loads((p/'run_diagnostics/results.json').read_text())
fig, axes = plt.subplots(1, 2, figsize=(12, 5.2), constrained_layout=True)
arr = np.full((4, 3), np.nan)
for r in rows:
    col = 0 if r['f'] == .3 else (2 if r['seed'] < .5 else 1)
    if col == 1 and r['f'] != .95:
        continue
    if 'tethered_mass_fraction' in r:
        arr[r['profile_index'], col] = r['tethered_mass_fraction']
ax = axes[0]
ax.imshow(np.ma.masked_invalid(arr), vmin=0, vmax=1, cmap='Blues', aspect='auto')
for i in range(4):
    for j in range(3):
        val = arr[i, j]
        txt = 'Unstable T\n(not evolved)' if np.isnan(val) else f'{100*val:.4f}%'
        ax.text(j, i, txt, ha='center', va='center', color='white' if val > .5 else '#172b4d', fontsize=10)
ax.set_xticks(range(3), ['Weak rotation\ninitially T', 'Strong rotation\ninitially T', 'Strong rotation\ninitially F'])
ax.set_yticks(range(4), ['3e5 / 0.3', '1e8 / 1', '6e10 / 3', '1e14 / 300'])
ax.set_ylabel('Baryon mass (solar masses) / scale (kpc)')
ax.set_title('Final tethered mass fraction', loc='left', fontweight='bold')
ax = axes[1]
for r, label in zip(diag['profiles'], ['3e5', '1e8', '6e10', '1e14']):
    ax.plot(r['x_path'], r['energy_over_T_energy'], label=label + ' solar masses', linestyle='--' if label=='1e14' else '-')
ax.set(xlabel='Uniform mixing coordinate x: free (0) to tethered (1)', ylabel='Internal energy / pure-T energy', xlim=(0,1))
ax.set_title('Rotation supplies a barrier, not formation', loc='left', fontweight='bold')
ax.legend(fontsize=9, frameon=False)
ax.grid(alpha=.2)
fig.suptitle('Constructed effective model • fixed density • common parameters\nTime = 100 internal units, not Gyr; uniform paths do not prove spatial stability', fontsize=12)
fig.savefig(p/'results.png', dpi=180)
