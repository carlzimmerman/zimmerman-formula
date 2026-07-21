#!/usr/bin/env python3
"""
a0(z): the framework's REAL prediction, the tension so far, and what JWST can still decide.
Footing (locked): modified inertia, a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11, a0 ~ sqrt(rho_DE).
  CANONICAL law: a0(z)/a0(0) = (1+z)^{1.5(1+w0+wa)} exp[-1.5 wa z/(1+z)]  (bump-then-decline).
Shows: the framework curve vs the latest competing models, the data already reported
(MUSE-DARK III + MSA-3D this work), and the OPEN JWST redshift windows with the model
spread (discriminating power) in each.  No 'manufactured win' line.
"""
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Patch

Om, OL = 0.315, 0.685
Ez  = lambda z: np.sqrt(Om*(1+z)**3 + OL)                       # rival sqrt(rho_total)~H(z)
canon = lambda z,w0,wa: np.sqrt((1+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z)))

# ---- MSA-3D inferred trend (this work), normalized to its own low-z bin (abs is M/L-degenerate)
KPC=3.0856775814913673e19; KMS=1e3; a0c=9.36e-11
G=[(0.58,5.37,51.5,152.1,0.59),(1.17,3.38,43.4,73.6,0.67),(1.25,2.92,44.9,114.9,0.70),
(0.98,3.04,39.4,165.6,0.63),(1.34,4.13,54.3,120.6,0.47),(1.08,1.59,49.5,168.9,0.58),
(1.59,5.86,45.5,79.3,0.53),(1.17,7.63,58.0,149.7,0.79),(1.28,2.53,61.5,121.8,0.73),
(1.03,1.95,49.8,106.0,0.51),(1.68,3.94,37.9,141.1,0.83),(1.10,5.28,43.1,261.6,0.70),
(1.57,3.89,47.1,208.1,0.77),(1.18,3.67,55.6,259.5,0.77),(0.98,5.83,44.2,137.9,0.75),
(0.74,4.97,32.6,110.3,0.68),(0.74,4.98,43.1,180.6,0.57),(1.51,2.91,45.4,327.9,0.52),
(0.74,4.52,36.6,132.8,0.36),(1.05,5.31,64.5,105.5,0.21),(1.24,4.36,59.7,189.8,0.26),
(0.76,2.58,43.6,83.5,0.50),(1.04,4.61,40.3,187.3,0.88)]
def inv(g):
    z,Re,s0,V,f=g; Vc2=(V*KMS)**2+3.356*(s0*KMS)**2; go=Vc2/(Re*KPC); gb=(1-f)*go
    return z,(go**2-gb**2)/gb/a0c
zz=np.array([inv(g)[0] for g in G]); aa=np.array([inv(g)[1] for g in G])
rng=np.random.default_rng(3); bz=[]; bm=[]; be=[]
for lo,hi in [(0.5,0.9),(0.9,1.2),(1.2,1.8)]:
    m=(zz>=lo)&(zz<hi); v=aa[m]; bz.append(zz[m].mean()); bm.append(np.median(v))
    be.append(np.std([np.median(rng.choice(v,len(v))) for _ in range(3000)]))
bz=np.array(bz); bmN=np.array(bm)/bm[0]; beN=np.array(be)/bm[0]

z=np.linspace(0,4.5,500)
fig,(ax,axr)=plt.subplots(1,2,figsize=(14.5,6.2),gridspec_kw={'width_ratios':[1.9,1]})

# ---- open JWST windows (shaded) ----
ax.axvspan(0.4,1.7,color='#f6d5d5',alpha=0.55,zorder=0)
ax.axvspan(1.7,3.0,color='#d8ead8',alpha=0.6,zorder=0)
ax.axvspan(3.0,4.5,color='#d3e0f2',alpha=0.7,zorder=0)
ax.text(1.05,10.5,'REPORTED\nMUSE tension · MSA-3D watch',ha='center',fontsize=8.2,color='#a11',weight='bold')
ax.text(2.35,10.5,'OPEN — JWST/NIRSpec + ALMA\n$a_0$ at cosmic noon',ha='center',fontsize=8.2,color='#276027',weight='bold')
ax.text(3.75,10.5,'OPEN — JWST + ALMA\nz≳3 BTFR-sign (decisive)',ha='center',fontsize=8.2,color='#1a4a86',weight='bold')

# ---- model curves ----
ax.axhline(1.0,color='0.55',ls=(0,(6,4)),lw=1.5,label=r'$\Lambda$CDM ($w{=}{-}1$): $a_0$ constant')
ax.plot(z,canon(z,-0.83,-0.75),color='#1a5fb4',lw=3.2,zorder=5,
        label=r'YOUR framework $\propto\!\sqrt{\rho_{\rm DE}}$ (DESI-DR2)')
ax.plot(z,canon(z,-0.45,-1.79),color='#3584e4',lw=2.0,ls='-.',zorder=5,
        label=r'YOUR framework (DESI-DR1 params)')
ax.plot(z,Ez(z),color='#2ec27e',lw=2.2,ls=':',zorder=5,
        label=r'rival $\propto\!\sqrt{\rho_{\rm total}}\!\sim\!H(z)$ (rejected footing)')

# ---- data ----
zm=np.linspace(0.5,1.44,40)
ax.plot(zm,1+zm,color='#c064c7',lw=2.4,zorder=6,label='MUSE-DARK III (reported rise)')
ax.errorbar(bz,bmN,yerr=beN,fmt='s',ms=9,mfc='white',color='#b08c0a',mec='#b08c0a',mew=1.6,
            capsize=4,zorder=7,label='MSA-3D raw inversion (selection-confounded → WATCH)')

ax.annotate('YOUR prediction:\nbump +3% (z≈0.3)\nthen DECLINE → 0.66 at z=3.5',
            xy=(3.0,canon(3.0,-0.83,-0.75)),xytext=(2.15,0.55),fontsize=8.6,color='#1a5fb4',
            arrowprops=dict(arrowstyle='->',color='#1a5fb4',lw=1.3))
ax.annotate('MUSE rise = the TENSION\n(real, contested)',xy=(1.2,2.2),xytext=(0.28,4.9),
            fontsize=8.8,color='#8f4700',arrowprops=dict(arrowstyle='->',color='#8f4700',lw=1.2))
ax.annotate('MSA-3D audit: rise is >half\nacceleration-selection;\ng_obs-controlled slope\n+0.91±0.8 (~1.1σ from flat)\n→ WATCH, not tension',
            xy=(1.43,3.19),xytext=(1.62,5.4),fontsize=7.8,color='#7a6207',
            arrowprops=dict(arrowstyle='->',color='#b08c0a',lw=1.1))
ax.set_yscale('log'); ax.set_ylim(0.5,13); ax.set_xlim(0,4.5)
ax.set_yticks([0.5,0.7,1,1.5,2,3,5,8]); ax.set_yticklabels(['0.5','0.7','1','1.5','2','3','5','8'])
ax.set_xlabel('redshift  $z$',fontsize=12.5); ax.set_ylabel(r'$a_0(z)\,/\,a_0(0)$',fontsize=12.5)
ax.set_title(r'$a_0(z)$: your prediction, the tension, and the open JWST windows',fontsize=13,weight='bold')
ax.legend(fontsize=8.6,loc='lower left',framealpha=0.96,ncol=1)
ax.text(0.015,0.015,r'$a_0=c^2\sqrt{\Lambda/32\pi}=9.36\times10^{-11}$ m s$^{-2}$;  '
        r'$a_0(z)/a_0(0)=(1{+}z)^{\frac{3}{2}(1+w_0+w_a)}e^{-\frac{3}{2} w_a z/(1+z)}$',
        transform=ax.transAxes,fontsize=8,color='0.3')

# ---- right: discriminating power (model spread) vs z ----
spread = Ez(z)/canon(z,-0.83,-0.75)              # rival / your framework
axr.axvspan(1.7,3.0,color='#d8ead8',alpha=0.6); axr.axvspan(3.0,4.5,color='#d3e0f2',alpha=0.7)
axr.axvspan(0.4,1.7,color='#f6d5d5',alpha=0.55)
axr.plot(z,spread,color='#613583',lw=2.8)
for zt in [1,2,3,4]:
    s=Ez(zt)/canon(zt,-0.83,-0.75); axr.plot(zt,s,'o',color='#613583',ms=6)
    axr.annotate(f'{s:.1f}×',(zt,s),textcoords='offset points',xytext=(6,-2),fontsize=9,color='#613583')
axr.axhline(1,color='0.6',ls=':',lw=1)
axr.set_xlim(0,4.5); axr.set_ylim(0.8,12); axr.set_yscale('log')
axr.set_yticks([1,2,3,5,8]); axr.set_yticklabels(['1','2','3','5','8'])
axr.set_xlabel('redshift  $z$',fontsize=12.5)
axr.set_ylabel('model spread  (rival / your framework)',fontsize=11)
axr.set_title('where a measurement decides:\nspread grows 1.9× → ~10× by z=4',fontsize=11,weight='bold')
axr.text(2.35,1.05,'z≈2–3\nJWST reach',ha='center',fontsize=8,color='#276027',weight='bold')
axr.text(3.75,1.05,'z≳3\nkill zone',ha='center',fontsize=8,color='#1a4a86',weight='bold')

fig.tight_layout()
out="real_research/figures/a0z_jwst_roadmap.jpg"
fig.savefig(out,dpi=175,format='jpg',bbox_inches='tight',facecolor='white')
print("saved ->",out)
print("\nMODEL PREDICTIONS vs z (a0(z)/a0(0)):")
print(f"{'z':>4}{'LCDM':>8}{'YOU(DR2)':>10}{'YOU(DR1)':>10}{'rival':>8}{'spread':>8}")
for zt in [0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0]:
    print(f"{zt:>4.1f}{1.0:>8.2f}{canon(zt,-0.83,-0.75):>10.2f}{canon(zt,-0.45,-1.79):>10.2f}"
          f"{Ez(zt):>8.2f}{Ez(zt)/canon(zt,-0.83,-0.75):>8.1f}")
