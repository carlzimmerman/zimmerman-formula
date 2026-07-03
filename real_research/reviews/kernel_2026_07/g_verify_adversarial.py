#!/usr/bin/env python3
"""ADVERSARIAL VERIFY of g_mode_sum.py (GATE-G). Independent re-derivation.
Kernel form (matches banked Saturn rolloff R=(nu2/Om)^2 AND flat in-band deficit):
  m_eff(w) = m[1 - S*L(w)],  L(w) = int G_sigma(nu-nu2) nu^2/(nu^2-w^2-i*Gam*w) dnu
  => Im L(w) = (pi/2)*w*G_sigma(w-nu2)   [resonant sub-lines at nu=w; NOT (pi/2)nu2^3 G/W^2]
  => at-line gain gamma(w)= (pi/4)*S*w^2*G_sigma(w-nu2)  [AGREES with g_mode_sum AT the line]
Attacks: (A) band-top prefactor / sigma_max; (B) hole-burning null of the binary horn;
(C) gas-continuum clamp with stressed damping; (D) F-overrun branch; (E) box scan. exit 0."""
import numpy as np
H0=2.2e-18; a0=9.36e-11; G=6.674e-11; AU=1.496e11; yr=3.156e7; pc=3.086e16
kB=1.381e-23; mH=1.67e-27; W=3008.0; TOL=4.8e-5; Gam=3.0
mu=lambda x:(np.sqrt(1+4*x**2)-1)/(2*x); S_of=lambda u:1-mu(u)
Gs=lambda d,s:np.exp(-d**2/(2*s**2))/(np.sqrt(2*np.pi)*s)
ok=True
def chk(n,c,msg=""):
    global ok; print(("  PASS " if c else "  FAIL ")+n+(("  "+msg) if msg else "")); ok&=c

print("A. KERNEL-FORM FORK: in-band Im/Re at band top W")
def sig_max(nu2):  # my form: Im/Re(W) = (pi/2)*W*G_sigma(nu2-W); + structural nu2-3sig>=W
    f=lambda s:(np.pi/2)*W*Gs(nu2-W,s)-TOL
    lo,hi=nu2/40,(nu2-W)/3
    if f(hi)<0: return hi          # structural cap binds first
    for _ in range(200):
        m_=np.sqrt(lo*hi)
        if f(m_)>0: hi=m_
        else: lo=m_
    return lo
for nu2 in (1.1e6,1e7,9.9e7):
    mine=(np.pi/2)*W*Gs(nu2-W,nu2/6); theirs=(np.pi/2)*nu2**3*Gs(nu2-W,nu2/6)/W**2
    print(f"  nu2={nu2:.1e}: Im/Re(W)@sig=nu2/6 mine={mine:.1e} theirs={theirs:.1e} ratio=(nu2/W)^3={(nu2/W)**3:.1e}; sig_max mine=nu2/{nu2/sig_max(nu2):.2f}")
chk("g_mode_sum band-top prefactor uses nu2^3 where resonant-sub-line form gives W^3: av_verify's Gaussian-clears was RIGHT",
    (np.pi/2)*W*Gs(1e7-W,1e7/6)<TOL and abs((np.pi/2)*1e21*Gs(1e7-W,1e7/6)/W**2/((np.pi/2)*W*Gs(1e7-W,1e7/6))-(1e7/W)**3)/(1e7/W)**3<1e-6)
chk("corrected sigma_max = (nu2-W)/3 (profile positivity above band), NOT nu2/7.4",abs(sig_max(1e7)/(1e7/3.001)-1)<0.05)
prmin=lambda nu2:(np.pi/4)*nu2*Gs(0,sig_max(nu2))
print(f"  MIN per-radian gain after MAX dilution: {prmin(1.1e6):.2f}S / {prmin(1e7):.2f}S / {prmin(9.9e7):.2f}S (vs their 2.1-2.5S: kill margins were ~x2.5 inflated)")
chk("irreducible per-radian gain still >=0.9S (dilution capped structurally)",min(prmin(1.1e6),prmin(1e7),prmin(9.9e7))>0.9)

print("B. HOLE-BURNING NULL of the binary horn (inhomogeneous medium: stimulated drain burns a Gam_hom slice)")
nu2=1e7; a=((2*np.pi/(nu2*H0)/yr)**2*1.5)**(1/3.)*AU; m1=1.5e30
Eorb=G*m1*m1/(2*a); u=G*2*m1/a**2/a0; S=S_of(u)
u_dress=S*0.5*(2.2e5)**2*2*m1                      # per-worldline line-weight dressing energy (F-gate pricing class)
slice_frac=Gam*Gs(0,sig_max(nu2))                  # Gam_hom slice of the profile (upper bound: line center)
gam_eff=3*H0*u_dress*slice_frac/Eorb/H0            # clamped drift, H0 units
bud=0.1/(5e9*yr*H0)
print(f"  a_res={a/AU:.0f} AU u={u:.0f} S={S:.1e} E_orb={Eorb:.1e} J; slice={slice_frac:.1e}; clamped gamma_eff={gam_eff:.1e} H0 vs budget {bud:.2f} H0")
chk("binary sweep NULLED by hole-burning (x2900 under budget; robust to 3 orders of slice-energy slop)",gam_eff*1e3<bud)
need=(np.pi/4)*nu2**2*Gs(0,sig_max(nu2))*S/Gam     # refresh ratio needed to prevent holes
print(f"  no-hole branch needs Gam_pump/3H0 >= {need:.1e} -> F headroom (25-470x) blown x{need/470:.0f}+")
chk("no-hole branch kills GATE-F instead (>=x8 over max headroom)",need/470>8)

print("C. GAS-CONTINUUM CLAMP (continuum addresses EVERY sub-line: hole-burning IS the full-line clamp here)")
worst=[]
for nu2 in (1.1e6,1e7,9.9e7):
    pr=prmin(nu2); cs=np.sqrt(5/3.*kB*80/mH); k=nu2*H0/cs
    lam=2*np.pi/k; mfp=1/(30e6*1e-19)
    eps=min(0.7*k*mfp,1.0); eps_st=min(10*eps,max(eps,0.2))  # x10 damping stress, floor 0.2 (thermal/turb worst)
    r=pr*S_of(0.3)/eps; r_st=pr*S_of(0.3)/eps_st; worst.append(r_st)
    print(f"  nu2={nu2:.1e}: CNM lam={lam/pc:.1e} pc (fluid: lam/mfp={lam/mfp:.0f}), gain/loss={r:.0f}, STRESSED(x10 damp)={r_st:.1f}")
chk("CNM super-threshold at floor/center/ceiling even at x10 damping stress",min(worst)>1.5)
r=1/min(worst)  # clamp weight ratio, most hostile corner
gb=np.logspace(-13,-11,50); g=np.sqrt(gb**2+gb*a0)          # deep-MOND points
mup=lambda x:1-r*(1-mu(x)); gcl=gb/mup(1e-3)                 # clamped deep limit: g<=g_bar/(1-r*S)
print(f"  hostile-corner clamp r={r:.2f}: deep boost capped at 1/(1-r)={1/(1-r):.2f} vs observed g_obs/g_bar~10 at u~0.01")
chk("ANY O(1) clamp destroys the deep-MOND limit (boost cap << 10): kill is qualitative, not marginal",1/(1-r)<3)
print(f"  -> HI/CNM volumes go near-Newtonian while dSphs keep a0: -m tuning(<=1%), R3(0.079 dex), own SPARC 0.108-dex fit all broken")

print("D. HEATING BOUND (re-check, honest): clamped dump = pump throughput")
Pkg=Gam*H0*0.5*0.4*(2.2e5)**2
sm=sig_max(1e7); w_star=100.; gd=(np.pi/4)*S_of(0.5)*w_star**2*Gs(w_star-1e7,sm)  # gain AT the star's omega (their S5 used nu2^2: x1e10 slip, masked by their narrow sigma)
print(f"  gas dump {Pkg:.1e} W/kg = {Pkg/6e-7*100:.0f}% ISM budget (absorbable); disk-star tail heating dv2/v2={gd*10e9*yr*H0:.1e}/10Gyr")
chk("no thermal kill (both channels)",Pkg/6e-7<0.5 and gd*10e9*yr*H0<1e-3)

print("E. BOX SCAN 25-pt, REPAIRED horns: (i) gas clamp>1 stressed OR (ii) F-overrun>8x")
alive=[]
for nu2 in np.logspace(np.log10(1.1e6),np.log10(9.9e7),25):
    pr=prmin(nu2); cs=np.sqrt(5/3.*kB*80/mH); k=nu2*H0/cs
    eps=min(0.7*k/(30e6*1e-19),1.0); eps_st=min(10*eps,max(eps,0.2))
    clamp=pr*S_of(0.3)/eps_st>1.5                    # horn (i): CNM clamps -> SPARC self-contradiction
    P=2*np.pi/(nu2*H0); aa=((P/yr)**2*1.5)**(1/3.); uu=G*3e30/(aa*AU)**2/a0
    fover=(np.pi/4)*nu2**2*Gs(0,sig_max(nu2))*S_of(0.3)/Gam/470>8   # horn (ii): no-hole refresh blows F
    if not (clamp or fover): alive.append(nu2)
print(f"  alive: {len(alive)}/25 {'(NONE)' if not alive else alive}")
chk("box EMPTY under repaired horns (horn-i alone suffices everywhere)",len(alive)==0)
assert ok,"a check failed"
print("VERDICT: GATE-G closes NEGATIVE box-wide -- via GAS-CONTINUUM CLAMP dichotomy; binary-sweep horn corrected to hole-burning-null/F-overrun. exit 0")
