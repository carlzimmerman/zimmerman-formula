#!/usr/bin/env python3
"""
The CORRECT a0(z) evolution law for the modified-INERTIA framework, + the figure.
Footing (locked): modified INERTIA, horizon a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11,
Lambda(z) ~ rho_DE(z) (the DARK-ENERGY-ONLY canonical branch), so a0 ~ sqrt(rho_DE).

Closed-form (CPL dark energy, w(z)=w0+wa z/(1+z)):
    a0(z)/a0(0) = (1+z)^{ (3/2)(1+w0+wa) } * exp( -(3/2) wa z/(1+z) )

Low-z expansion (honest -- shows why Gemini's linear 'mic-drop' inverts the physics):
    a0(z)/a0(0) = 1 + (3/2)(1+w0) z + (3/4)( wa - (1+w0) + (3/2)(1+w0)^2 ) z^2 + O(z^3)
    The linear coeff is +, but the z^2 coeff is wa-driven and NEGATIVE for DESI values,
    so the initial rise REVERSES near z ~ z_turn -> a small BUMP then a DECLINE.

Contrast branches plotted:
  * canonical framework  a0 ~ sqrt(rho_DE)         (bump-then-decline)  <-- the prediction
  * rival footing        a0 ~ sqrt(rho_total)~E(z) (monotonic rise)     <-- REJECTED footing
  * Gemini 'manufactured win' = linear term only, wa dropped            <-- the error
  * data: MUSE-DARK III reported rise; MSA-3D (this work) inferred trend (M/L-degenerate abs)
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

Om, OL = 0.315, 0.685
Ez   = lambda z: np.sqrt(Om*(1+z)**3 + OL)                         # rival sqrt(rho_total) ratio
def a0_canon(z, w0, wa):                                          # canonical sqrt(rho_DE) ratio
    return np.sqrt((1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*z/(1+z)))
def a0_gemini(z, w0):                                             # dropped-wa linear
    return 1 + 1.5*(1+w0)*z

# ---------- print the correct law + the bump-reversal redshift ----------
print("="*80); print("CORRECT a0(z) LAW  (canonical modified-inertia, sqrt(rho_DE) footing)"); print("="*80)
print("  a0(z)/a0(0) = (1+z)^[1.5(1+w0+wa)] * exp[-1.5 wa z/(1+z)]")
for name,w0,wa in [("DESI-DR2-ish",-0.83,-0.75),("DESI-DR1-ish",-0.45,-1.79)]:
    lin = 1.5*(1+w0); quad = 0.75*(wa-(1+w0)) + (9/8)*(1+w0)**2
    zt = -lin/(2*quad) if quad<0 else np.inf
    zpk = np.linspace(0,1,2001); pk = a0_canon(zpk,w0,wa); zbump=zpk[np.argmax(pk)]
    print(f"  {name} (w0={w0},wa={wa}): low-z ~ 1 + {lin:+.2f} z {quad:+.2f} z^2 ; "
          f"bump peak z~{zbump:.2f} (+{100*(pk.max()-1):.0f}%), then declines; "
          f"a0(z=3)/a0(0)={a0_canon(3,w0,wa):.2f}")

# ---------- MSA-3D inferred trend (this work) -- normalized to its own low-z bin ----------
KPC=3.0856775814913673e19; KMS=1e3; a0c=9.36e-11
G=[(0.58,5.37,51.5,152.1,0.59),(1.17,3.38,43.4,73.6,0.67),(1.25,2.92,44.9,114.9,0.70),
(0.98,3.04,39.4,165.6,0.63),(1.34,4.13,54.3,120.6,0.47),(1.08,1.59,49.5,168.9,0.58),
(1.59,5.86,45.5,79.3,0.53),(1.17,7.63,58.0,149.7,0.79),(1.28,2.53,61.5,121.8,0.73),
(1.03,1.95,49.8,106.0,0.51),(1.68,3.94,37.9,141.1,0.83),(1.10,5.28,43.1,261.6,0.70),
(1.57,3.89,47.1,208.1,0.77),(1.18,3.67,55.6,259.5,0.77),(0.98,5.83,44.2,137.9,0.75),
(0.74,4.97,32.6,110.3,0.68),(0.74,4.98,43.1,180.6,0.57),(1.51,2.91,45.4,327.9,0.52),
(0.74,4.52,36.6,132.8,0.36),(1.05,5.31,64.5,105.5,0.21),(1.24,4.36,59.7,189.8,0.26),
(0.76,2.58,43.6,83.5,0.50),(1.04,4.61,40.3,187.3,0.88)]
def a0inf(g):
    z,Re,s0,V,f=g; Vc2=(V*KMS)**2+3.356*(s0*KMS)**2
    go=Vc2/(Re*KPC); gb=(1-f)*go; return z,(go**2-gb**2)/gb
zz=np.array([a0inf(g)[0] for g in G]); aa=np.array([a0inf(g)[1] for g in G])/a0c
bins=[(0.5,0.9),(0.9,1.2),(1.2,1.8)]; bz=[]; bm=[]; be=[]
rng=np.random.default_rng(3)
for lo,hi in bins:
    m=(zz>=lo)&(zz<hi); v=aa[m]; bz.append(zz[m].mean()); bm.append(np.median(v))
    boot=[np.median(rng.choice(v,len(v))) for _ in range(3000)]; be.append(np.std(boot))
bz=np.array(bz); bm=np.array(bm); be=np.array(be)
norm=bm[0]; bm_n=bm/norm; be_n=be/norm                            # normalize to low-z bin

# ---------- FIGURE ----------
z=np.linspace(0,3,400)
fig,(ax,axin)=plt.subplots(1,2,figsize=(13.5,5.6),gridspec_kw={'width_ratios':[1.55,1]})

# left: the full landscape
ax.axhline(1.0,color='0.6',ls=(0,(6,4)),lw=1.4,label=r'$\Lambda$CDM ($w{=}{-}1$): flat')
ax.plot(z,a0_canon(z,-0.83,-0.75),color='#1a5fb4',lw=2.8,
        label=r'framework canonical $\propto\!\sqrt{\rho_{\rm DE}}$  (DESI-DR2)')
ax.plot(z,a0_canon(z,-0.45,-1.79),color='#3584e4',lw=2.0,ls='-.',
        label=r'framework canonical  (DESI-DR1)')
ax.plot(z,Ez(z),color='#2ec27e',lw=2.0,ls=':',
        label=r'RIVAL footing $\propto\!\sqrt{\rho_{\rm total}}\!\sim\!H(z)$ (rejected)')
ax.plot(z,a0_gemini(z,-0.8),color='#e01b24',lw=2.4,ls=(0,(5,2)),
        label=r"Gemini 'mic-drop' (dropped $w_a$)")
# MUSE-DARK reported rise (0.5<z<1.44), ~doubling by z~1 as characterized
zm=np.linspace(0.5,1.44,50)
ax.plot(zm,1+zm,color='#c064c7',lw=2.0,label='MUSE-DARK III reported rise')
# MSA-3D inferred trend (this work), normalized to low-z bin
ax.errorbar(bz,bm_n,yerr=be_n,fmt='s',ms=8,color='#f5c211',mec='k',mew=1.1,capsize=4,zorder=6,
            label='MSA-3D inferred trend (this work)')
ax.axhspan(0,0,color='none')
ax.set_xlim(0,3); ax.set_ylim(0.55,4.2)
ax.set_xlabel('redshift  $z$',fontsize=12)
ax.set_ylabel(r'$a_0(z)\,/\,a_0(0)$',fontsize=12)
ax.set_title(r'$a_0(z)$: framework prediction vs the manufactured win',fontsize=12.5,weight='bold')
ax.legend(fontsize=8.4,loc='upper left',framealpha=0.95)
ax.annotate('manufactured "win":\nlinear rise, $w_a$ dropped',xy=(2.0,a0_gemini(2.0,-0.8)),
            xytext=(1.35,3.4),fontsize=8.6,color='#e01b24',
            arrowprops=dict(arrowstyle='->',color='#e01b24',lw=1.3))
ax.annotate('data (MUSE + MSA-3D)\nrise = TENSION\nvs canonical',xy=(1.1,2.1),xytext=(2.05,2.55),
            fontsize=8.6,color='#8f4700',ha='left',
            arrowprops=dict(arrowstyle='->',color='#8f4700',lw=1.2))
ax.text(0.02,0.02,r'$a_0=c^2\sqrt{\Lambda/32\pi}=9.36\times10^{-11}$ m s$^{-2}$;  modified inertia, $g_{\rm obs}=\sqrt{g_{\rm bar}^2+g_{\rm bar}a_0}$',
        transform=ax.transAxes,fontsize=7.6,color='0.35')

# right: zoom on the BUMP-then-decline (the actual prediction)
zz2=np.linspace(0,2,300)
axin.axhline(1.0,color='0.6',ls=(0,(6,4)),lw=1.2)
axin.plot(zz2,a0_canon(zz2,-0.83,-0.75),color='#1a5fb4',lw=2.8)
axin.plot(zz2,a0_canon(zz2,-0.45,-1.79),color='#3584e4',lw=2.0,ls='-.')
zp=np.linspace(0,1,1000); pk=a0_canon(zp,-0.83,-0.75); zbmp=zp[np.argmax(pk)]
axin.plot(zbmp,pk.max(),'o',color='#1a5fb4',ms=8,zorder=5)
axin.annotate(f'bump  +{100*(pk.max()-1):.0f}%\nat z≈{zbmp:.2f}',xy=(zbmp,pk.max()),
              xytext=(0.55,1.14),fontsize=9,color='#1a5fb4',
              arrowprops=dict(arrowstyle='->',color='#1a5fb4',lw=1.2))
axin.annotate('then DECLINES\n(0.70–0.74 at z=3)',xy=(1.7,a0_canon(1.7,-0.83,-0.75)),
              xytext=(1.02,0.90),fontsize=9,color='#1a5fb4',
              arrowprops=dict(arrowstyle='->',color='#1a5fb4',lw=1.2))
axin.set_xlim(0,2); axin.set_ylim(0.78,1.20)
axin.set_xlabel('redshift  $z$',fontsize=12)
axin.set_ylabel(r'$a_0(z)\,/\,a_0(0)$',fontsize=12)
axin.set_title('the ACTUAL prediction: bump → decline',fontsize=11.5,weight='bold')

fig.tight_layout()
out="real_research/figures/a0z_evolution_gemini_vs_correct.jpg"
fig.savefig(out,dpi=170,format='jpg',bbox_inches='tight',facecolor='white')
print("\nSaved figure ->",out)
print(f"MSA-3D bins (norm to low-z): z={bz.round(2)}  ratio={bm_n.round(2)}  (abs a0/a0c={bm.round(1)})")
