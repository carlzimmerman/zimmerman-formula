"""Display the frozen full-EKG witness; no new fit or field solve."""
from pathlib import Path
import hashlib
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

base = Path(__file__).resolve().parent
profile = base / 'equilibria/run_001/mixed_center.npz'
data = np.load(profile)
r, f, h = [data[k] for k in ('r', 'f', 'h')]
G, omega, m = [float(data[k]) for k in ('G', 'omega', 'm')]
mass = data['v'] / G**1.5
local = omega / data['alpha']
cap = np.sqrt(float(data['M'])**2 - float(data['g'])**2 /
              float(data['lambda_total'])) / 2
old_bound = (1 - (1 + .02**2 * 2/3)**-2) / 2
R99 = 79.6940278051  # continuous mass-polynomial root in owner's verifier
keep = r <= 250

plt.rcParams.update({'font.size': 11, 'axes.spines.top': False,
                     'axes.spines.right': False})
fig, axes = plt.subplots(1, 3, figsize=(13, 3.8), constrained_layout=True)
ax = axes[0]
ax.plot(r[keep], f[keep]/f[0], label=r'$f/f_c$')
ax.plot(r[keep], h[keep]/h[0], label=r'$h/h_c$')
ax.set(xlabel=r'Areal radius $r$ (units $m^{-1}$)',
       ylabel='Normalized field amplitude', title='Both fields localized')
ax.legend(frameon=False)
ax = axes[1]
ax.plot(r[keep], (local[keep]/m-1)*1e4, color='#6654a6')
ax.axhline((cap/m-1)*1e4, color='#bd5034', linestyle='--',
           label='Homogeneous TF ceiling')
ax.set(xlabel=r'Areal radius $r$', ylabel=r'$10^4(\Omega/m-1)$',
       title='Gradients remove the local ceiling')
ax.legend(frameon=False, fontsize=9)
ax = axes[2]
ax.plot(r[keep], G*mass[keep]/r[keep], color='#20766c',
        label=r'$G\mathcal{M}(r)/r$')
ax.axvline(R99, color='#777777', linestyle=':', label=r'$R_{99}$')
ax.axhline(old_bound, color='#bd5034', linestyle='--',
           label='Old TF number (different radius)')
ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
ax.set(xlabel=r'Areal radius $r$', ylabel='Enclosed compactness',
       title='Full metric, with scalar tails')
ax.legend(frameon=False, fontsize=8)
fig.suptitle('Original two-field action: numerical spherical equilibrium\n'
             r'$m=\lambda=1,\ G=8.5\times10^{-5},\ u_*=0.02,\ r_\lambda=2$; '
             'stability assessed separately', fontsize=12)
out = base/'FULL_EKG_WITNESS.png'
fig.savefig(out, dpi=180)
(base/'FIGURE_PROVENANCE.json').write_text(json.dumps({
    'input': str(profile.relative_to(base)),
    'sha256': hashlib.sha256(profile.read_bytes()).hexdigest(),
    'purpose': 'Display frozen numerical witness; no new field solve or fit',
    'radius_caveat': 'Old TF theorem uses finite surface; R99 is a separate tail convention',
    'stability_caveat': 'Equilibrium alone does not establish stability',
    'output': out.name
}, indent=2)+'\n')
print(out)
