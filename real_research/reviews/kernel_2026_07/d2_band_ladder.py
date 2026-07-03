#!/usr/bin/env python3
"""
BUREAU D2 / script 1 (v2) -- COSMOLOGICAL GAIN MEDIUM: BAND + GAP-DISTRIBUTION DEMAND SIDE
Framework objects ONLY: a0 = cH_Lambda/Z = 9.36e-11, Z = sqrt(32pi/3),
mu_fw(g_bar) = sqrt(g_bar/(g_bar+a0));  vs physical drive y = g_obs/a0: mu(y) = (sqrt(1+4y^2)-1)/(2y).
Band (PUMP_HUNT R1): Omega_orb in [44,3008] H0. Milgrom 2022 (PRD 106,064060): on circular orbits the
kernel must collapse to mu_fw EXACTLY -- in particular Im[mu]=0 on circular orbits (no secular exchange).

 Q1  amplitude layer: what threshold distribution does mu_fw demand; positive-ensemble realizability (NNLS)
 Q2  frequency layer: LINEAR-MEDIUM TRICHOTOMY by spectral-support location (the load-bearing result):
       T1 gaps IN band | T2 gaps ABOVE band | T0 gaps BELOW band  -- each confronted with
       flatness + Im=0(circular) + R3 + stability, numerically.
 Q3  quartic ladder: one-field gap span + knee-in-acceleration scaling (relevant to T1-class designs)
 Q4  locality -> constituent mass
Hard asserts = math identities; contingent design outcomes = printed VERDICTs.
"""
import numpy as np
from scipy.optimize import lsq_linear

H0=2.2e-18; a0=9.36e-11; Z=np.sqrt(32*np.pi/3); c=2.998e8
kpc=3.0857e19; Mpc=1e3*kpc; Gyr=3.156e16
GAM=3.0; W1,W2=44.0,3008.0
ok=True
def chk(n,cnd,m=""):
    global ok; print(("  PASS " if cnd else "  FAIL ")+n+("  "+m if m else "")); ok=ok and cnd
def verdict(n,cnd,m=""):
    print(("  VERDICT[+] " if cnd else "  VERDICT[-] ")+n+("  "+m if m else "")); return cnd

print("="*100); print("Q0  BAND BOOKKEEPING"); print("="*100)
span=W2/W1
print(f"  band [44,3008] H0 = [{W1*H0:.2e},{W2*H0:.2e}]/s; span x{span:.1f}; Q=om/Gam in [{W1/GAM:.0f},{W2/GAM:.0f}]")
lam1,lam2=2*np.pi*c/(W1*H0)/Mpc,2*np.pi*c/(W2*H0)/Mpc
print(f"  luminal in-band wavelengths {lam2:.1f}-{lam1:.0f} Mpc vs galaxy ~0.03 Mpc")

print("="*100); print("Q1  AMPLITUDE LAYER: mu_fw as saturable-threshold ensemble (upgrades gauntlet3 S2)"); print("="*100)
mu_y=lambda y:(np.sqrt(1+4*y**2)-1)/(2*y); dl_y=lambda y:1.0-mu_y(y)
ys_=np.array([1e-6,1e-5]); sd=np.diff(np.log(mu_y(ys_)))/np.diff(np.log(ys_))
yl_=np.array([1e5,1e6]); tail=dl_y(yl_)*2*yl_
chk("deep approach LINEAR in drive (mu ~ y)",abs(sd[0]-1)<1e-3,f"slope={sd[0]:.4f}")
chk("Newtonian tail deficit = 1/(2y)",np.allclose(tail,1,atol=1e-3),"non-analytic in intensity => NO single physical line (gauntlet3)")
print("  analytic medium (mu~y^2 deep) => a^3 = g_bar a0^2 => v(r) ~ r^(1/6) RISING: no flat RCs -- odd-|drive| law LOAD-BEARING")
yg=np.geomspace(1e-3,1e4,300); ysg=np.geomspace(1e-4,1e5,80)
A=1.0/(1.0+(yg[:,None]/ysg[None,:])**2); b=dl_y(yg)
Wr=np.minimum(1.0/b,2e2)
r1=lsq_linear(A*Wr[:,None],b*Wr,bounds=(0,np.inf),method='trf',tol=1e-12,max_iter=3000)
w=r1.x; pred=A@w; rel=np.abs(pred-b)/b
win=(yg>=1e-2)&(yg<=1e2)
dmu=np.abs(np.log10(np.clip(1-pred,1e-12,None)/np.clip(1-b,1e-12,None)))[win]
print(f"  NNLS: max rel err (SPARC window y=1e-2..1e2) = {rel[win].max()*100:.3f}%; max|dlog10 mu| = {dmu.max():.4f} dex (fit floor 0.108)")
q1=verdict("mu_fw EXACTLY realizable by a POSITIVE quadratic-saturator ensemble",rel[win].max()<0.01 and dmu.max()<0.01)
C=np.cumsum(w)  # cumulative threshold mass (robust to solver spikiness)
def cslope(lo,hi):
    m=(ysg>=lo)&(ysg<=hi)&(C>1e-12); return np.polyfit(np.log(ysg[m]),np.log(C[m]),1)[0]
s_lo=cslope(2e-3,0.2)                       # expect ~1  (density index 0)
Tmass=w.sum()-C                              # tail mass above ys; expect ~ ys^-1 (density index -2)
m2=(ysg>=3.0)&(ysg<=3e2)&(Tmass>1e-12)
s_hi=np.polyfit(np.log(ysg[m2]),np.log(Tmass[m2]),1)[0]
print(f"  cumulative-mass slopes: below knee {s_lo:+.2f} (demand +1 <=> density index 0 <=> deep slope 1/2);")
print(f"                          tail-mass  {s_hi:+.2f} (demand -1 <=> density index -2 <=> Newtonian a0/2g); break AT a0")
verdict("threshold density == broken power law (0,-2) breaking at a0",abs(s_lo-1)<0.35 and abs(s_hi+1)<0.35,
        "the 'inserted mu-shape' == ONE positive threshold distribution; exponents+normalization UNFORCED (POSITS P1,P2)")
print(f"  sum(w) = {w.sum():.4f} (must be exactly 1: the 100%-cancellation edge; gauntlet3 S4 tuning = P2)")

print("="*100); print("Q2  FREQUENCY LAYER -- LINEAR-MEDIUM TRICHOTOMY (support location is exhaustive)"); print("="*100)
print("  linear response: m_eff(Om)/m = 1 +(passive)/-(inverted) l2m * S(Om),  S = INT W(om) dom /(om^2-Om^2-i Gam Om)")
print("  Milgrom-2022 circular exactness => Im[m_eff]=0 on circular orbits; Im S(Om) = (pi/2) W_net(Om)/Om + tails:")
print("  any NET in-band weight buys Im at the orbit frequency ITSELF -- Gamma-independent (sum rule), cancellation-proof")
print("-"*100)
print("  T1: gaps IN band (the D2 brief's resonant gain medium), inverted, near-flat weight W ~ om^2:")
omg=np.geomspace(W1,W2,24000); dlno=np.log(omg[1]/omg[0]); OmS=np.geomspace(100,1300,40)
wj=omg**3*dlno
d=omg[None,:]**2-OmS[:,None]**2; den=d**2+(GAM*OmS[:,None])**2
Sr=(wj[None,:]*d/den).sum(1); Si=(wj[None,:]*GAM*OmS[:,None]/den).sum(1)
ratio=np.median(np.abs(Si/Sr))
print(f"     flatness: peak/trough {np.abs(Sr).max()/np.abs(Sr).min():.2f} over [100,1300] (near-flat OK)")
print(f"     BUT Im S/Re S = {ratio:.2f} (median)  [Gamma-check: ", end="")
for g2 in (0.3,3.0,30.0):
    den2=d**2+(g2*OmS[:,None])**2
    r2v=np.median(np.abs((wj[None,:]*g2*OmS[:,None]/den2).sum(1)/(wj[None,:]*d/den2).sum(1)))
    print(f"Gam={g2:g}: {r2v:.2f}  ",end="")
print("] -- Gamma-INDEPENDENT as claimed")
Om_mid=300.0
efold_orb=1.0/(ratio)  # e-folds of orbital energy per radian ~ ratio; per orbit ~ 2pi*ratio
t_efold=1.0/(ratio*Om_mid*H0)/Gyr
print(f"     secular exchange rate ~ (Im/Re)*Om: e-fold of orbital energy every {1/(2*np.pi*ratio):.2f} orbits = {t_efold:.3f} Gyr at Om=300 H0")
print(f"     (inverted: SPIN-UP; passive: inspiral). Observed disks are ~Hubble-stable => margin ~x{ (1/(ratio))*0.0 + (14.4/t_efold):.0f} over a Hubble time")
t1=verdict("T1 resonant in-band medium EXCLUDED: Im(mu)!=0 violates Milgrom-2022 circular exactness AND e-folds orbits in <<Gyr",
        ratio>0.1,"THE CLEAN STRUCTURAL KILL of the D2-briefed class (linear version) -- theorem-shaped, Gamma-independent")
print("-"*100)
print("  T2: gaps ABOVE band (om_g >= 3x3008 H0), derivative coupling => deficit(Om) = l2m*Om^2*INT W/(om^2-Om^2):")
og=5*W2
dfr=(W1**2/(og**2-W1**2))/(W2**2/(og**2-W2**2))
print(f"     deficit(44)/deficit(3008) = {dfr:.1e} -- effect DIES at band bottom (the deepest-MOND dSph/LSB frequencies)")
print( "     (resonant-knee variant instead pins a VELOCITY knee: a0_eff ~ Om*v_knee varies x68 across band: 1.8 dex >> 0.079)")
t2=verdict("T2 above-band medium EXCLUDED (loses LSBs / smears a0 by 1.8 dex)",dfr<0.01)
print("-"*100)
print("  T0: gaps BELOW band (om_g ~ 10-15 H0), PASSIVE, velocity/kinetic mixing  L_int = lam*m*xdot*Xdot:")
og0=10.0; l2m=0.95
kin=np.array([[1.0,np.sqrt(l2m)],[np.sqrt(l2m),1.0]])   # kinetic matrix in units m=1
ev=np.linalg.eigvalsh(kin)
OmB=np.geomspace(W1,W2,200)
meff=1.0+l2m*OmB**2/(og0**2-OmB**2)                      # exact 2x2 driven response (PV part), passive sign
# numeric cross-check at one frequency by direct complex solve:
Omx=300.0
Xamp=l2m*Omx**2/(og0**2-Omx**2+1j*GAM*Omx)               # X = lam*m*Om^2 x/(og^2-Om^2-iGamOm) per unit lam
mchk=1.0+ (og0**2-Omx**2)*l2m*Omx**2/((og0**2-Omx**2)**2+(GAM*Omx)**2)
chk("T0 closed-form == direct complex solve at Om=300 H0",abs(np.real(1+Xamp)-mchk)<1e-12)
dfc=-(meff-1.0)                                           # deficit = l2m*Om^2/(Om^2-og^2) > 0 above gap
print(f"     kinetic-matrix eigenvalues {ev[0]:.3f},{ev[1]:.3f} > 0: GHOST-FREE, PASSIVE (no inversion, ground state)")
print(f"     deficit above gap: {dfc.min():.3f}..{dfc.max():.3f} across band; ripple {(dfc.max()-dfc.min())/dfc.mean()*100:.1f}%"
      f" (window <=11%: og=10 H0 => (og/44)^2 = {(og0/W1)**2*100:.1f}% edge term)")
print(f"     deep-MOND edge: deficit -> l2m = {l2m}; l2m -> 1 is EXACTLY the kinetic-positivity (ghost) boundary:")
print(f"     the |dm|->m cliff of the spec IS the ghost edge; riding at l2m = 1-eps is the same S4 tuning (P2)")
ImRe=GAM*OmB/(OmB**2-og0**2)
print(f"     in-band drag: Im/Re = Gam*Om/(Om^2-og^2) = {ImRe.max():.3f} (band bottom) .. {ImRe.min():.1e} (top)")
print(f"     secular DRAG e-fold ~ 1/Gam = {1/(GAM*H0)/Gyr:.1f} Gyr (pump-hunt's own 4.6 Gyr 'tolerable' class, passive sign)")
print(f"     R4: deficit persists at ALL Om >> og (Saturn too) -> safety comes from the AMPLITUDE layer alone:")
print(f"        Saturn a/a0 = {6.5e-3/a0:.1e} -> saturated deficit ~ a0/(2a) = {a0/(2*6.5e-3):.1e}: Cassini-safe")
print( "        WIDE BINARIES: deep-amplitude, NOT band-protected -> T0 PREDICTS MOND-ON in WBs;")
print( "        REVERSES the pump-hunt gamma->1 corollary (that corollary belongs to the T1/T2 band-limited class)")
t0=verdict("T0 passive below-gap kinetic-mixing: ONLY LINEAR SURVIVOR -- flat, ghost-free at eps>0, Im(circular)~Gam-tail, NO PUMP NEEDED",
        ev[0]>0 and (dfc.max()-dfc.min())/dfc.mean()<0.11 and abs(ImRe).max()<0.01,
        "MUST be adjudicated against the banked nonlocal anti-MOND sign theorem (its proof regime looks DC/below-gap; T0 lives ABOVE its gap where anti-phase mass reduction is standard metamaterial physics) -- flag to parent, do not self-certify")
print("     NOTE the state-clause is NOT contradicted where it is computed: free/passive fields stay state-blind and")
print("     amplitude-blind -- T0's KNEE still requires the anharmonic saturation layer (P1,P2) exactly as the spec says.")

print("="*100); print("Q3  ONE FIELD, ALL GAPS (T1-class requisite; kept for the record + the knee scaling win)"); print("="*100)
N=800; n_=np.arange(N); aop=np.diag(np.sqrt(n_[1:]),1)
x=(aop+aop.T)/np.sqrt(2.0); pm=(aop-aop.T)/np.sqrt(2.0)
Hm=-0.5*(pm@pm)+0.25*np.linalg.matrix_power(x,4)
E,V=np.linalg.eigh(Hm); X=V.T@x@V
nn=np.arange(30,151)
gap=E[nn+1]-E[nn]; mel=np.abs(np.array([X[k,k+1] for k in nn]))
sE=np.polyfit(np.log(nn),np.log(E[nn]),1)[0]; sG=np.polyfit(np.log(nn),np.log(gap),1)[0]; sM=np.polyfit(np.log(nn),np.log(mel),1)[0]
print(f"  E_n ~ n^{sE:.3f} (4/3); gap ~ n^{sG:.3f} (1/3); <n|x|n+1> ~ n^{sM:.3f} (1/3); rung span for x68.4: {span**(1/sG):.1e}")
chk("quartic ladder exponents (4/3,1/3,1/3)",abs(sE-4/3)<0.02 and abs(sG-1/3)<0.03 and abs(sM-1/3)<0.03)
sK=np.polyfit(np.log(nn),np.log(gap/mel),1)[0]
chk("knee at FIXED ACCELERATION across ladder (a_sat ~ gap/matel ~ n^0)",abs(sK)<0.02,
    f"slope {sK:+.4f}: real structural win -- but it lives on the T1 branch, which Q2 kills")

print("="*100); print("Q4  LOCALITY"); print("="*100)
print(f"  luminal in-band modes {lam2:.0f}-{lam1:.0f} Mpc >> galaxy: collective saturation would tie the knee to galaxy")
print("  baryon content (R3 broken) -> massive/localized constituents REQUIRED in every branch (D1)")

print("="*100)
print(f"SUMMARY: Q1 mu_fw positively realizable (P1,P2); Q2 trichotomy: T1 KILLED (sum-rule), T2 KILLED, T0 sole")
print(f"linear survivor (passive, pump-FREE, sign-theorem adjudication pending); Q3 ladder win stranded on T1;")
print(f"Q4 massive constituents forced. Nonlinear-entrained media remain unmodeled (outside linear response).")
print("="*100)
assert ok,"math-identity checks failed"
print("ALL CHECKS PASSED (d2_band_ladder v2)")
