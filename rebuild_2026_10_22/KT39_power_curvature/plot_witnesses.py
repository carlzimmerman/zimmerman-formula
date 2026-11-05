#!/usr/bin/env python3
"""Export the two refined KT39 power-action MW witnesses against unchanged data."""
import json
import os
from pathlib import Path
import sys
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/kt34_matplotlib')
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'mw'))
import search as U
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
M=U.M
d=json.loads((HERE/'mw/refine_001/results.json').read_text())
fig,axs=plt.subplots(1,2,figsize=(11.4,4.5))
ax=axs[0]
ax.errorbar(M.C.OR,M.C.OV,yerr=M.C.OE,fmt='.',color='#657387',alpha=.7,
            markersize=4,capsize=2,label='Ou data + frozen errors')
ax.set(xlabel='Radius [kpc]',ylabel='Circular speed [km/s]',title='Milky Way radial check')
ax=axs[1]
ax.errorbar(M.C.BR_R,M.C.BR_K,yerr=M.C.BR_E5,fmt='.',color='#657387',alpha=.65,
            markersize=4,capsize=2,label='Bovy–Rix data + frozen errors')
ax.errorbar([M.C.R0],[M.C.KZ],yerr=[2*M.C.KZE],fmt='s',color='#222222',capsize=5,
            markersize=4,label='Local vertical cut (2σ)')
ax.set(xlabel='Radius [kpc]',ylabel='Vertical force equivalent [M☉ / pc²]',title='At height z = 1.1 kpc')
for foot,color,label in [('canonical','#087e8b','Canonical a₀'),('alt','#b25128','Alternate a₀')]:
    q=next(x['score'] for x in d['rows'] if x['footing']==foot and x['power']==1.125 and x['refine']==5)
    axs[0].plot(M.C.OR,q['vc_Ou'],color=color,lw=2,label=f'{label}: χ² = {q["cO"]:.2f}')
    order=U.np.argsort(M.C.BR_R)
    axs[1].plot(U.np.asarray(M.C.BR_R)[order],U.np.asarray(q['K'])[order],color=color,lw=2,
                label=f'{label}: χ² = {q["cK"]:.2f}')
for ax in axs:
    ax.grid(alpha=.18);ax.spines[['top','right']].set_visible(False)
    ax.legend(frameon=False,fontsize=8)
fig.suptitle('Curvature action: p = 9/8 and ℓ = 3 kpc, full variation',fontsize=13)
fig.text(.5,.025,'Both witnesses pass the four original MW cuts. Neither passes the separate strict vertical scale-length cut.',
         ha='center',fontsize=9,color='#5a3a31')
fig.tight_layout(rect=(0,.065,1,.94))
fig.savefig(HERE/'mw_witnesses.png',dpi=180)
fig.savefig(HERE/'mw_witnesses.pdf')
