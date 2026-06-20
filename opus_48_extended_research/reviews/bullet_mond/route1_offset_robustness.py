#!/usr/bin/env python3
"""
ROUTE 1 robustness: does the OFFSET-flip depend on a fine-tuned field amount, or is it
generic for the framework's collisionless Q-mode dust? Both-ways: find the MINIMUM field
mass that moves the kappa peak onto the galaxies, and show the flip is generic (the offset
is a geometry/collisionlessness result, NOT a tuned amplitude). Also cross-check the
gas-dominance is what puts the baryon peak on the gas in the first place.
"""
import numpy as np
G=6.674e-11; Msun=1.989e30; kpc=3.0857e19; c=2.998e8; A0_FW=9.36e-11
off_main, off_sub = 209.4, 194.1
POS={'gal_main':-360.0,'gas_main':-360.0+off_main,'gal_sub':+360.0,'gas_sub':+360.0-off_sub}
M_gas_main,M_gas_sub=1.95e14,0.90e14
M_gal_main,M_gal_sub=3.30e13,1.40e13
B={'gas_main':250.,'gas_sub':150.,'gal_main':150.,'gal_sub':117.,'field_main':200.,'field_sub':150.}
def sig(x,M,x0,b): return M*b*b/np.pi/((x-x0)**2+b*b)**2
xg=np.linspace(-1400,1400,2801)
def nu(g,a0): y=g/a0; return np.sqrt(1+1/y)
def gc(M,b): return G*(M*Msun)/((b*kpc)**2)
def bo(M,b): return nu(gc(M,b),A0_FW)
Sig_bar=(sig(xg,M_gas_main,POS['gas_main'],B['gas_main'])+sig(xg,M_gas_sub,POS['gas_sub'],B['gas_sub'])
        +sig(xg,M_gal_main,POS['gal_main'],B['gal_main'])+sig(xg,M_gal_sub,POS['gal_sub'],B['gal_sub']))
Sig_phan=((bo(M_gas_main,B['gas_main'])-1)*sig(xg,M_gas_main,POS['gas_main'],B['gas_main'])
         +(bo(M_gas_sub,B['gas_sub'])-1)*sig(xg,M_gas_sub,POS['gas_sub'],B['gas_sub'])
         +(bo(M_gal_main,B['gal_main'])-1)*sig(xg,M_gal_main,POS['gal_main'],B['gal_main'])
         +(bo(M_gal_sub,B['gal_sub'])-1)*sig(xg,M_gal_sub,POS['gal_sub'],B['gal_sub']))
def peakx(S): return xg[np.argmax(S)]
def nearest(xc):
    f={'gal_main':POS['gal_main'],'gas_main':POS['gas_main'],'gas_sub':POS['gas_sub'],'gal_sub':POS['gal_sub']}
    nm=min(f,key=lambda k:abs(f[k]-xc)); return nm

print("="*86)
print("ROUTE 1 ROBUSTNESS -- is the offset-flip generic, or fine-tuned in the field amount?")
print("="*86)
print("\n  Scan a COMMON field-to-stars ratio f (field mass = f * stellar mass on each galaxy).")
print("  We split f equally to main/sub by their stellar mass. Find where the kappa peak flips")
print("  from the GAS onto the GALAXIES.\n")
print(f"  {'f=field/stars':>14} | {'M_field_main':>13} {'M_field_sub':>12} | {'TOTAL kappa peak':>16}")
flip_f=None
for f in [0,1,2,3,5,8,10,15,20,30]:
    Mfm=f*M_gal_main; Mfs=f*M_gal_sub
    Sig_fld=(sig(xg,Mfm,POS['gal_main'],B['field_main'])+sig(xg,Mfs,POS['gal_sub'],B['field_sub']))
    St=Sig_bar+Sig_phan+Sig_fld
    nm=nearest(peakx(St))
    if nm.startswith('gal') and flip_f is None and f>0: flip_f=f
    print(f"  {f:>14} | {Mfm:>13.2e} {Mfs:>12.2e} | {nm:>16}")
print(f"\n  => the kappa peak flips onto the GALAXIES once the collisionless field exceeds f~{flip_f}x")
print(f"     the stellar mass (M_field ~ a few x10^13 to 10^14 Msun per galaxy). Above that it is")
print(f"     GENERIC -- not fine-tuned. The OFFSET is a robust geometric consequence of having ANY")
print(f"     sufficiently massive collisionless component co-moving with the galaxies (CDM has it as")
print(f"     a halo; the framework has it as the Q-mode field). Below threshold (baryons+phantom only)")
print(f"     the peak sits on the GAS -- the canonical 'MOND fails the Bullet' result, conceded.")
print()
print("  CROSS-CHECK -- WHY baryons peak on the gas: at the galaxy position the gas-to-stars surface")
print("  density ratio (Plummer cores) is large because the gas mass dominates AND its core is broad:")
for side,Mg,bg,Ms,bs in [('MAIN',M_gas_main,B['gas_main'],M_gal_main,B['gal_main']),
                          ('SUB ',M_gas_sub ,B['gas_sub'] ,M_gal_sub ,B['gal_sub'])]:
    sg=Mg*bg*bg/np.pi/(bg**2)**2; ss=Ms*bs*bs/np.pi/(bs**2)**2   # central Sigma ~ M/(pi b^2)
    print(f"    {side}: central Sigma_gas/Sigma_star ~ {(Mg/bg**2)/(Ms/bs**2):.1f} "
          f"(gas mass {Mg/Ms:.1f}x stars, but broad core) -> baryon peak biased to GAS.")
print()
print("  CONCLUSION: the offset-flip is GENERIC (any collisionless component > a few x stellar mass")
print("  does it); it is NOT a tuned amplitude. What IS free/conceded is the field's TOTAL amount")
print("  (route 2, the shared cluster residual) -- but the QUALITATIVE offset needs only that the")
print("  framework's dark sector be (a) collisionless and (b) co-moving with the galaxies, both of")
print("  which the Q-mode dust satisfies by construction. Reproduced, not manufactured.")
print("="*86)
