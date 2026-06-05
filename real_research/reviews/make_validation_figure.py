#!/usr/bin/env python3
"""
Publication figure: the framework's a0 on the REAL SPARC radial-acceleration relation + the BTFR z~3 bridge prediction.
======================================================================================================================
Two panels, from genuine SPARC data (data/sparc_data/*_rotmod.dat):
  (A) the radial-acceleration relation g_obs vs g_bar (3389 points), with the framework MOND curve
      g_obs = g_bar nu(g_bar/a0), a0 = c^2 sqrt(Lambda/32pi). The visual z=0 validation.
  (B) the baryonic Tully-Fisher relation V_flat vs M_b (per galaxy), with the framework BTFR line at z=0 and the
      DISTINCTIVE predicted z=3 line (a0 -> 0.74 a0 under DESI dark energy -> V_flat lower by a0^1/4).
Needs numpy, matplotlib.
"""
import glob, os, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

KPC=3.0856775814913673e19; KMS=1.0e3; ML_D,ML_B=0.5,0.7; G=6.674e-11; Msun=1.989e30
C=2.99792458e8; MPC=3.0857e22; H0=67.4e3/MPC; OmL=0.685
A0=C**2*np.sqrt(3*OmL*H0**2/C**2/(32*np.pi))      # framework a0 = 9.36e-11
DATA=os.path.join(os.path.dirname(__file__),"..","data","sparc_data")
nu=lambda y:0.5+np.sqrt(0.25+1.0/y)


def load():
    gb,go,vflat,Mb=[],[],[],[]
    for path in sorted(glob.glob(os.path.join(DATA,"*_rotmod.dat"))):
        R,VO,VB=[],[],[]
        for line in open(path):
            s=line.strip()
            if not s or s.startswith("#"): continue
            p=s.split()
            if len(p)<6: continue
            try: r,vo,ev,vg,vd,vb=(float(p[i]) for i in range(6))
            except ValueError: continue
            if r<=0 or vo<=0: continue
            vbar2=ML_D*vd*vd+ML_B*vb*vb+vg*abs(vg)
            if vbar2<=0: continue
            gb.append(vbar2*KMS**2/(r*KPC)); go.append((vo*KMS)**2/(r*KPC))
            R.append(r); VO.append(vo); VB.append(np.sqrt(vbar2))
        if len(R)>=4:
            R,VO,VB=map(np.array,(R,VO,VB))
            vflat.append(np.median(VO[-3:]))                     # outer (flat) rotation speed
            Mb.append(VB[-1]**2*KMS**2*(R[-1]*KPC)/G/Msun)        # enclosed baryonic mass ~ total
    return map(np.array,(gb,go,vflat,Mb))


def main():
    gb,go,vflat,Mb=load()
    fig,(axA,axB)=plt.subplots(1,2,figsize=(13,5.4))

    # Panel A: RAR
    axA.hexbin(np.log10(gb),np.log10(go),gridsize=45,cmap='Blues',mincnt=1,bins='log')
    x=np.logspace(-12.5,-8.5,200)
    axA.plot(np.log10(x),np.log10(x*nu(x/A0)),'r-',lw=2.2,label=r'framework $a_0=c^2\sqrt{\Lambda/32\pi}$')
    axA.plot(np.log10(x),np.log10(x),'k:',lw=1,label='1:1 (Newtonian)')
    scat=np.std(np.log10(go)-np.log10(gb*nu(gb/A0)))
    axA.set_xlabel(r'$\log_{10}\,g_{\rm bar}\;[{\rm m\,s^{-2}}]$'); axA.set_ylabel(r'$\log_{10}\,g_{\rm obs}$')
    axA.set_title(f'(A) SPARC radial-acceleration relation\n175 galaxies, 3389 pts; framework $a_0$ scatter = {scat:.3f} dex')
    axA.legend(loc='upper left',fontsize=9); axA.set_xlim(-12.3,-8.6); axA.set_ylim(-12.3,-8.6)

    # Panel B: BTFR + z=3 prediction
    axB.scatter(np.log10(Mb),np.log10(vflat),s=14,c='0.5',alpha=0.6,label='SPARC galaxies (z~0)')
    M=np.logspace(8,11.5,100)
    V0=(G*M*Msun*A0)**0.25/KMS
    V3=(G*M*Msun*A0*0.737)**0.25/KMS                # z=3: a0 -> 0.737 a0 (DESI sqrt(rho_DE))
    axB.plot(np.log10(M),np.log10(V0),'b-',lw=2,label=r'BTFR $z=0$: $V=(GM_ba_0)^{1/4}$')
    axB.plot(np.log10(M),np.log10(V3),'r--',lw=2,label=r'framework prediction $z=3$ ($a_0\!\to\!0.74a_0$)')
    axB.set_xlabel(r'$\log_{10}\,M_{\rm bar}\;[M_\odot]$'); axB.set_ylabel(r'$\log_{10}\,V_{\rm flat}\;[{\rm km/s}]$')
    axB.set_title('(B) Baryonic Tully-Fisher + the $z\\sim3$ bridge prediction\n(same baryons rotate ~7% slower at $z=3$ if dark energy evolves)')
    axB.legend(loc='upper left',fontsize=9); axB.set_xlim(8.2,11.4); axB.set_ylim(1.4,2.5)

    fig.tight_layout()
    out="real_research/figures/sparc_validation_bridge.png"
    fig.savefig(out,dpi=120,bbox_inches='tight')
    print(f"  validation figure written: {out}")
    print(f"  Panel A: framework a0 reproduces the real SPARC RAR at {scat:.3f} dex scatter.")
    print(f"  Panel B: z=0 BTFR anchor + the distinctive z=3 prediction (the coefficient-free bridge, visualized).")


if __name__=="__main__":
    main()
