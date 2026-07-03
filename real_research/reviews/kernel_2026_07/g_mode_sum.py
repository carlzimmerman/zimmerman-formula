#!/usr/bin/env python3
"""GATE-G MODE SUM: collective lasing/ASE threshold for the inverted Gaussian line.
Construction: m_eff=m[1-S(|a|/a0)R(w)], one inverted line nu2 in [1.1e6,9.9e7] H0,
Gamma_hom=3H0, Gaussian inhomog. sigma_inh, weight -m-tuned (T4, <=1%).
KK lock: in-band Delta=-mS  <=>  |Im K(w)| = (pi/2) m S nu2^3 G_sigma(w-nu2).
Gain on any oscillator DOF at w inside the line: gamma_gain = |Im K|/(2 m w) = (pi/4) S w^2 G_sigma(dw).
Framework objects only: a0=9.36e-11, mu_fw. exit 0."""
import numpy as np
H0=2.2e-18; a0=9.36e-11; G=6.674e-11; Msun=1.989e30; AU=1.496e11; yr=3.156e7; pc=3.086e16
kB=1.381e-23; mH=1.67e-27; Gam=3.0  # H0 units
W=3008.0; TOL=4.8e-5                # band top, in-band Im/Re orbit-count tolerance (av #5)
mu=lambda x:(np.sqrt(1+4*x**2)-1)/(2*x); S_of=lambda u:1-mu(u)
ok=True
def chk(n,c,msg=""):
    global ok; print(("  PASS " if c else "  FAIL ")+n+(("  "+msg) if msg else "")); ok&=c
Gs=lambda d,s:np.exp(-d**2/(2*s**2))/(np.sqrt(2*np.pi)*s)

print("="*100);print("S1  KK-LOCKED GAIN + sigma_max from band tail (WITH the (pi/2)nu2^3/W^2 prefactor)");print("="*100)
def sigma_max(nu2):                 # largest sigma passing Im/Re(bandtop)<=TOL
    f=lambda s:(np.pi/2)*nu2**3*Gs(nu2-W,s)/W**2 - TOL
    lo,hi=nu2/40,nu2/2
    for _ in range(200):
        mid=np.sqrt(lo*hi)
        if f(mid)>0: hi=mid
        else: lo=mid
    return lo
for nu2 in (1.1e6,1e7,9.9e7):
    sm=sigma_max(nu2); tail_av=np.exp(-((nu2-W)/(nu2/6))**2/2)
    imre6=(np.pi/2)*nu2**3*Gs(nu2-W,nu2/6)/W**2
    print(f"  nu2={nu2:.1e}: sigma_max=nu2/{nu2/sm:.1f}; av's sigma=nu2/6 -> bare tail {tail_av:.1e} BUT Im/Re={imre6:.2f} (prefactor {imre6/tail_av:.1e})")
chk("av_verify Gaussian-tail check omitted prefactor ~4e7; sigma=nu2/6 FAILS TOL x1e4; corrected sigma_max~nu2/7.4",
    (np.pi/2)*1e21*Gs(1e7-W,1e7/6)/W**2>1e3*TOL and 7.0<1e7/sigma_max(1e7)<8.0)
peak_perrad=lambda nu2:(np.pi/4)*nu2*Gs(0,sigma_max(nu2))     # gain per radian / S
g0=peak_perrad(1e7)
print(f"  KK-locked MINIMUM peak gain (sigma at max): gamma_gain/w = {g0:.2f}*S per radian (=0.313*nu2/sigma*S)")
print(f"  verifier scaling check: sigma/Gam_hom = {(1e7/6)/3:.1e} (5.6e5 reproduced) -- correct RATIO vs homogeneous line,")
print(f"  but ABSOLUTE gain after full dilution is still {g0:.1f}*S*nu2 ~ 1e6-1e8 H0*S, vs mode losses, NOT vs 3H0.")
chk("dilution cannot reduce peak per-radian gain below ~2.3S (band tail caps sigma)",g0>2.0)

print("="*100);print("S2  MODE CENSUS: what resonates inside the line?");print("="*100)
wJ_gal=np.sqrt(4*np.pi*G*0.25e6*mH)/H0; wJ_cos=np.sqrt(4*np.pi*G*0.049*(3*H0**2/(8*np.pi*G)))/H0
print(f"  gravity-mediated collective coupling: (wJ/nu2)^2 = {(wJ_gal/1.1e6)**2:.1e} (galactic n=0.25/cc) .. {(wJ_cos/9.9e7)**2:.1e} (cosmic)")
print(f"  cooperative (Dicke) rate ~ wJ^2/nu2 = {wJ_gal**2/1e7:.1f} H0 << sigma_inh ~ {1e7/7.4:.1e} H0: superradiance DEPHASED (verifier right, that channel only)")
chk("gravitational collective/Dicke channel negligible",(wJ_gal/1.1e6)**2<1e-6 and wJ_gal**2/1e7<1e7/7.4/1e3)
print("  BUT gain is PER-WORLDLINE (local kernel): no phase-matching needed; ANY oscillator DOF with eigenfrequency")
print("  inside the line is anti-damped: (i) diffuse-gas sound/MHD (continuum, all w); (ii) BOUND KEPLERIAN ORBITS.")
for nu2 in (1.1e6,1e7,9.9e7):
    P=2*np.pi/(nu2*H0); a=( (P/yr)**2*1.5 )**(1/3.)
    print(f"  nu2={nu2:.1e} H0: P={P/yr/1e3:.2f} kyr -> resonant binaries a={a:.0f} AU (M=1.5Msun); Sedna P=11.4 kyr = {2*np.pi/(11400*yr)/H0:.1e} H0")
print("  binary separation distribution 100-2200 AU: CONTINUOUS, no gap (El-Badry+Rix 2021 MNRAS 506,2269; Raghavan 2010): input")

print("="*100);print("S3  THRESHOLD MAP -- gas channels (gamma_gain vs gamma_damp), box floor/center/ceiling");print("="*100)
envs=[("cold HI/CNM",30,80,1e-19,0.3),("WNM",0.3,8000,1e-19,0.5),("mol.cloud",1e3,15,3e-19,3.0),
      ("hot halo/WIM",3e-3,1e6,None,0.7),("IGM/WHIM",2.7e-7,1e5,None,1.0)]  # n/cc, T, sigma_coll, u=|a|/a0 typical
worst_gas={}
for nu2 in (1.1e6,1e7,9.9e7):
    sm=sigma_max(nu2); pr=(np.pi/4)*nu2*Gs(0,sm)   # per-radian /S
    print(f"  nu2={nu2:.1e} (per-radian gain {pr:.2f}*S):")
    rows=[]
    for nm,n,T,sig,u in envs:
        cs=np.sqrt(5/3.*kB*T/mH); k=nu2*H0/cs
        if sig: eps=min(0.7*k/(n*1e6*sig),1.0)      # viscous/free-molec damping per radian
        else:   eps=0.3                              # Landau/transit-time, kinetic plasma
        Sv=S_of(u); ratio=pr*Sv/eps
        rows.append((nm,ratio)); print(f"    {nm:14s} lambda={2*np.pi/k/pc:.1e} pc  eps={eps:.1e}  S={Sv:.2f}  gain/loss = x{ratio:.1f}")
    worst_gas[nu2]=max(r for _,r in rows)
    chk(f"    cold-HI channel ABOVE lasing threshold at nu2={nu2:.0e}",rows[0][1]>3,f"x{rows[0][1]:.0f}")
print("  -> the HI that SPARC's deep-MOND points are MEASURED IN is a super-threshold gain medium at every nu2 in the box")

print("="*100);print("S4  RESERVOIR DICHOTOMY (energy conservation; medium internal energy is a free posit)");print("="*100)
bud=0.1/(5e9*yr)/H0   # orbit-energy budget: 10% over 5 Gyr, in H0 units
print(f"  HORN (i) small reservoir (u_lock-class, F-gate pricing): stimulated drain clamps at pump -> weight collapses")
print(f"    steady-state delivered weight ~ loss/gain: cold-HI suppression factors:")
for nu2 in (1.1e6,1e7,9.9e7):
    sup=worst_gas[nu2]; print(f"    nu2={nu2:.1e}: a0_eff collapse in HI ~ x{sup:.0f} = {np.log10(sup):.1f} dex vs universality budget 0.079 dex")
    chk(f"    HORN-i kill at nu2={nu2:.0e}: HI/RAR + R3 universality broken",np.log10(sup)>0.3)
print("    (gas-poor dSphs keep full a0, HI disks lose it: O(1) environment split; SPARC HI curves go Newtonian)")
print(f"  HORN (ii) large reservoir (no clamp): resonant binaries anti-damped at full KK-locked gain:")
for nu2 in (1.1e6,1e7,9.9e7):
    P=2*np.pi/(nu2*H0); a=((P/yr)**2*1.5)**(1/3.)
    g=G*3e30/(a*AU)**2; u=g/a0; Sv=S_of(u)
    gam=(np.pi/4)*nu2*Gs(0,sigma_max(nu2))*Sv*nu2/nu2  # per-radian*S -> rate = per-radian*nu2
    gam=(np.pi/4)*nu2**2*Gs(0,sigma_max(nu2))*Sv
    ef=1/(gam*H0)/(1e6*yr)
    print(f"    nu2={nu2:.1e}: a_res={a:.0f} AU u={u:.0f} S={Sv:.1e} -> gamma={gam:.1e} H0, e-fold {ef:.2f} Myr, over budget x{gam/bud:.1e}")
    chk(f"    HORN-ii kill at nu2={nu2:.0e}: binaries over existence budget >1e4",gam/bud>1e4)
print("    growth self-limits by chirping OUT of the line after da/a~2/3*(3sigma/nu2)~0.4-0.7: sweeps a factor ~1.8")
print("    separation gap + wide-edge pileup in <<Gyr -- observed distributions are smooth: population kill stands")
print("    AND stimulated drain >> 3H0 spontaneous: F-gate headroom 25-470x blown by gain/3H0:")
print(f"      gain/pump = {(np.pi/4)*1e14*Gs(0,sigma_max(1e7))*1.3e-3/Gam:.1e} (center, binary-slice alone)")

print("="*100);print("S5  FDT / NOISE COROLLARY (honest both-ways: heating does NOT kill)");print("="*100)
sm=sigma_max(1e7); tail=np.exp(-(1e7/sm)**2/2)
gam_disk=(np.pi/4)*1e14*Gs(0,sm)*0.5*tail   # in-band noise anti-damping on stars at ~100 H0: Gaussian tail
print(f"  in-band (disk-star, 44-3008 H0) noise from Gaussian tail: rate ~{gam_disk:.1e} H0 -> dv2/v2 over 10 Gyr ~{gam_disk*10e9*yr*H0:.1e}")
chk("old-thin-disk direct noise heating NEGLIGIBLE (no kill manufactured here)",gam_disk*10e9*yr*H0<1e-3)
Pkg=Gam*H0*0.5*0.4*(2.2e5)**2
print(f"  clamped-state dump into gas = pump throughput {Pkg:.1e} W/kg ~ {Pkg/6e-7*100:.0f}% of ISM radiative budget: ABSORBABLE")
chk("gas heating at clamp absorbable (<50% ISM budget)",Pkg/6e-7<0.5)

print("="*100);print("S6  PASS-REGION SCAN over the full box (25-pt log grid, both horns)");print("="*100)
alive=[]
for nu2 in np.logspace(np.log10(1.1e6),np.log10(9.9e7),25):
    sm=sigma_max(nu2); pr=(np.pi/4)*nu2*Gs(0,sm)
    cs=np.sqrt(5/3.*kB*80/mH); eps=min(0.7*(nu2*H0/cs)/(30e6*1e-19),1.0)
    horn1=pr*S_of(0.3)/eps>2.0                       # cold-HI super-threshold (S at outer-disk u~0.3)
    P=2*np.pi/(nu2*H0); a=((P/yr)**2*1.5)**(1/3.); u=G*3e30/(a*AU)**2/a0
    horn2=(np.pi/4)*nu2**2*Gs(0,sm)*S_of(u)/bud>1e4  # binary overshoot
    if not (horn1 and horn2): alive.append(nu2)
print(f"  subregions where EITHER horn fails to kill: {len(alive)} of 25  {alive if alive else '(NONE -- box empty)'}")
chk("NO pass region anywhere in [1.1e6, 9.9e7] H0: GATE-G closes NEGATIVE on both horns",len(alive)==0)
assert ok,"a check failed"
print("ALL CHECKS PASS. GATE-G VERDICT: FIFTH THEOREM (at-line resonant catastrophe). exit 0")
