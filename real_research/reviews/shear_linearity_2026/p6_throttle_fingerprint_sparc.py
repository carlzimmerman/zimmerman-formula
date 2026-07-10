#!/usr/bin/env python3
"""
LANE 2 -- THE THROTTLE FINGERPRINT (P6 follow-up).

Two branches to discriminate on SPARC point-level data (protocol verbatim from the
banked decider real_research/reviews/branchB_q2_gate_2026/decider_sparc_pointlevel.py;
benchmark 0.1083 dex @ Ups=0.70 canonical asserted before judging):

  Branch A (modified inertia, framework-nu exact):
      F_A(y) = nu_fw(y) - 1 = sqrt(1 + 1/y) - 1            at ALL y
  Branch B (throttled elastic medium, entropy-budget tail):
      F_B(y) = F_A(y) * T(y),   T(y) = min(1, (y_c/y)^n),  n = 1,
      y_c = Z/2, Z = sqrt(32 pi / 3) = 5.7888  ->  y_c = 2.894 (canonical footing)
                                                   y_c = 2.898 (alt footing)

Fingerprint profile: Delta(y) = log10[(1+F_A)/(1+F_B)]  (dex), zero below y_c.

Sections:
  S1  fingerprint profile, both footings + y_c sensitivity band (Z/2 x {0.5,1,2})
  S2  pipeline benchmark assert (framework-nu canonical: 0.1083 @ 0.70)
  S3  per-branch SPARC fits (Ups, rms, window medians y=2,4,6,10 w/ galaxy bootstrap)
  S4  anchor reproduction: observed median log10(gobs/gbar) at y~6, Ups=0.70
  S5  Upsilon-absorption of the fingerprint (the delta-family lesson, quantified)
  S6  discrimination sigma TODAY (per-galaxy bootstrap; windows share gal+Ups so the
      combined statistic is bootstrapped as a whole, never treated as independent)
  S7  sensitivity for 3 sigma: N scaling, Q=1 subsample, fixed-Ups (M/L prior) case
  S8  BTFR zero-point (outermost/flat points: is the throttle invisible there?)
  S9  y~2-3 RAR curvature statement (kink at y_c)

Honest outcomes allowed: INDISTINGUISHABLE-today / throttle disfavored / MI disfavored.
No commits, no Zenodo. exit 0.
"""
import numpy as np, glob, os, sys, time

rng = np.random.default_rng(20260710)
kpc = 3.086e19
A0C, A0A = 9.36e-11, 1.13e-10                    # canonical / alt footings
Z = np.sqrt(32*np.pi/3)                          # 5.78881
YC_CAN = Z/2                                     # 2.89440 (canonical budget solve)
YC_ALT = 2.898                                   # alt-footing budget solve (banked)
DATADIR = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"
MRT     = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/SPARC_Lelli2016c.mrt"

# ---------------------------------------------------------------- load (verbatim + gal id)
def load_sparc():
    Rl,Vol,eVl,Vg2l,Vd2l,Vb2l,Gl,names = [],[],[],[],[],[],[],[]
    gid = 0
    for f in sorted(glob.glob(os.path.join(DATADIR,"*_rotmod.dat"))):
        try: d = np.genfromtxt(f, comments="#")
        except Exception: continue
        if d.ndim != 2 or d.shape[1] < 6: continue
        R,Vobs,eV,Vgas,Vdisk,Vbul = (d[:,i] for i in range(6))
        Rl.append(R*kpc); Vol.append(Vobs); eVl.append(eV)
        Vg2l.append(np.sign(Vgas)*Vgas**2); Vd2l.append(Vdisk**2); Vb2l.append(Vbul**2)
        Gl.append(np.full(len(R), gid, dtype=int))
        names.append(os.path.basename(f).replace("_rotmod.dat",""))
        gid += 1
    return (np.concatenate(Rl), np.concatenate(Vol), np.concatenate(eVl),
            np.concatenate(Vg2l), np.concatenate(Vd2l), np.concatenate(Vb2l),
            np.concatenate(Gl), names)

Rm,Vobs,eV,Vg2,Vd2,Vb2,GAL,NAMES = load_sparc()
NGAL = len(NAMES)
gobs = (Vobs*1e3)**2/Rm
w = 1.0/np.clip(eV,1,None)**2*np.clip(Vobs,1,None)**2
UGRID = np.arange(0.30,1.2001,0.025)

# quality flags from the Lelli+2016 master table (bytes 1-11 name right-justified, 97-99 Q)
QFLAG = {}
NAMESET = set(NAMES)
try:
    with open(MRT) as fh:
        for line in fh:
            tok = line.split()
            if tok and tok[0] in NAMESET and len(tok) >= 18 and tok[17] in ("1","2","3"):
                QFLAG[tok[0]] = int(tok[17])
except Exception:
    pass
GALQ = np.array([QFLAG.get(n, 0) for n in NAMES])   # 0 = unknown

# ---------------------------------------------------------------- branch definitions
def F_A(y):
    y = np.maximum(y,1e-12)
    return np.sqrt(1.0+1.0/y)-1.0
def make_F_B(yc, n=1.0):
    def FB(y):
        y = np.maximum(y,1e-12)
        return F_A(y)*np.minimum(1.0,(yc/y)**n)
    return FB

# ---------------------------------------------------------------- fit machinery
GALPTS = [np.where(GAL==g)[0] for g in range(NGAL)]

def fit(boost, a0, idx=None):
    """Upsilon-refit protocol verbatim; idx = point subset (bootstrap resample)."""
    if idx is None: idx = slice(None)
    _Vg2,_Vd2,_Vb2,_Rm = Vg2[idx],Vd2[idx],Vb2[idx],Rm[idx]
    _gobs,_Vobs,_w = gobs[idx],Vobs[idx],w[idx]
    best = (None,1e9,None,None)
    for Ud in UGRID:
        gb = (_Vg2+Ud*_Vd2+1.4*Ud*_Vb2)*1e6/_Rm
        ok = (gb>0)&(_gobs>0)&np.isfinite(gb)&(_Vobs>0)
        gp = gb[ok]*(1.0+boost(gb[ok]/a0))
        r  = np.log10(_gobs[ok])-np.log10(gp)
        rms= np.sqrt(np.sum(_w[ok]*r**2)/np.sum(_w[ok]))
        if rms < best[1]: best = (Ud,rms,r,gb[ok]/a0)
    return best   # Ud, rms, residuals, y

WINS = (2.0,4.0,6.0,10.0)
def win_medians(r, y):
    out = {}
    for ys in WINS:
        m = np.abs(np.log10(y/ys)) < 0.15
        out[ys] = (np.median(r[m]) if m.sum()>=8 else np.nan, int(m.sum()))
    return out
def highy_stat(r, y, lo=4.0, hi=30.0):
    m = (y>=lo)&(y<=hi)
    return (np.median(r[m]) if m.sum()>=8 else np.nan, int(m.sum()))

def boot_indices(galpool):
    pick = rng.choice(galpool, size=len(galpool), replace=True)
    return np.concatenate([GALPTS[g] for g in pick])

def bootstrap(boost, a0, nboot=300, galpool=None, fixU=None):
    """per-GALAXY bootstrap of {window medians, high-y median, Ups, rms}."""
    if galpool is None: galpool = np.arange(NGAL)
    meds = {ys: [] for ys in WINS}; C=[]; UPS=[]; RMS=[]
    for _ in range(nboot):
        idx = boot_indices(galpool)
        if fixU is None:
            Ud,rms,r,y = fit(boost,a0,idx)
        else:
            Ud = fixU
            gb=(Vg2[idx]+Ud*Vd2[idx]+1.4*Ud*Vb2[idx])*1e6/Rm[idx]
            ok=(gb>0)&(gobs[idx]>0)&np.isfinite(gb)&(Vobs[idx]>0)
            gp=gb[ok]*(1.0+boost(gb[ok]/a0))
            r=np.log10(gobs[idx][ok])-np.log10(gp); y=gb[ok]/a0
            rms=np.sqrt(np.sum(w[idx][ok]*r**2)/np.sum(w[idx][ok]))
        for ys in WINS: meds[ys].append(win_medians(r,y)[ys][0])
        C.append(highy_stat(r,y)[0]); UPS.append(Ud); RMS.append(rms)
    sig = {ys: np.nanstd(meds[ys]) for ys in WINS}
    return sig, np.nanstd(C), np.array(C), np.array(UPS), np.array(RMS), meds

t0=time.time()
print("="*96)
print("S1  FINGERPRINT PROFILE  Delta(y) = log10[(1+F_A)/(1+F_B)]  (dex)")
print("="*96)
print(f"Z = sqrt(32pi/3) = {Z:.5f};  y_c = Z/2 = {YC_CAN:.4f} (canonical), {YC_ALT:.4f} (alt)")
ygrid = np.array([0.01,0.1,0.5,1.0,2.0,2.894,3.0,4.0,6.0,10.0,20.0,30.0])
print(f"\n{'y':>7} | " + " ".join(f"yc={v:6.3f}" for v in (YC_CAN*0.5,YC_CAN,YC_CAN*2.0,YC_ALT)))
for yy in ygrid:
    row=[]
    for yc in (YC_CAN*0.5,YC_CAN,YC_CAN*2.0,YC_ALT):
        FB = make_F_B(yc)
        row.append(np.log10((1+F_A(np.array([yy]))[0])/(1+FB(np.array([yy]))[0])))
    print(f"{yy:>7.3f} | " + " ".join(f"{v:8.4f}" for v in row))
d6  = np.log10((1+F_A(np.array([6.0]))[0]) /(1+make_F_B(YC_CAN)(np.array([6.0]))[0]))
d10 = np.log10((1+F_A(np.array([10.0]))[0])/(1+make_F_B(YC_CAN)(np.array([10.0]))[0]))
print(f"\nverify: Delta=0 for y<=y_c (exact, T=1 there); Delta(6)={d6:.4f}, Delta(10)={d10:.4f} dex "
      f"[expected ~0.015-0.017]")
assert d6>0.014 and d6<0.019 and abs(np.log10((1+F_A(np.array([2.0]))[0])/(1+make_F_B(YC_CAN)(np.array([2.0]))[0])))<1e-12

print("\n"+"="*96)
print("S2  PIPELINE BENCHMARK (framework-nu, canonical a0)")
print("="*96)
Uf,rf,r_A,y_A = fit(F_A, A0C)
print(f"framework-nu: rms = {rf:.4f} dex @ Ups = {Uf:.2f}   (banked 0.1083 @ 0.70)")
assert abs(rf-0.1083)<0.005 and abs(Uf-0.70)<0.05, "pipeline broken -- do not judge"
print("[BENCH OK]")

print("\n"+"="*96)
print("S3  PER-BRANCH SPARC FITS (Ups refit; window medians +/- per-galaxy bootstrap err)")
print("="*96)
NBOOT=300
models = [("A  framework-nu  (can)", F_A, A0C),
          ("B  throttle yc=Z/2 (can)", make_F_B(YC_CAN), A0C),
          ("B  yc=Z/4  x0.5   (can)", make_F_B(YC_CAN*0.5), A0C),
          ("B  yc=Z    x2.0   (can)", make_F_B(YC_CAN*2.0), A0C),
          ("A  framework-nu  (alt)", F_A, A0A),
          ("B  throttle yc     (alt)", make_F_B(YC_ALT), A0A)]
RES={}
for tag,Fb,a0 in models:
    Ud,rms,r,y = fit(Fb,a0)
    meds = win_medians(r,y); Chat,nC = highy_stat(r,y)
    sig, sigC, Cboot, UPSb, RMSb, medboot = bootstrap(Fb,a0,NBOOT)
    RES[tag]=dict(Ud=Ud,rms=rms,meds=meds,sig=sig,C=Chat,sigC=sigC,nC=nC,
                  Cboot=Cboot,UPSb=UPSb,RMSb=RMSb,r=r,y=y)
    ms=" ".join(f"y={ys:g}:{meds[ys][0]:+.4f}+/-{sig[ys]:.4f}(n={meds[ys][1]})" for ys in WINS)
    print(f"{tag:>26}: Ups={Ud:.3f} rms={rms:.4f} | {ms}")
    print(f"{'':>26}  high-y stat (median resid, 4<=y<=30, n={nC}): C={Chat:+.4f} +/- {sigC:.4f}")

print("\n"+"="*96)
print("S4  ANCHOR REPRODUCTION: observed median log10(gobs/gbar) at y~6, Ups=0.70 canonical")
print("="*96)
Ud=0.70
gb=(Vg2+Ud*Vd2+1.4*Ud*Vb2)*1e6/Rm
ok=(gb>0)&(gobs>0)&np.isfinite(gb)&(Vobs>0)
robs=np.log10(gobs[ok])-np.log10(gb[ok]); yobs=gb[ok]/A0C
m6=np.abs(np.log10(yobs/6.0))<0.15
anchor=np.median(robs[m6])
ab=[]
okidx=np.where(ok)[0]
for _ in range(600):
    idx=boot_indices(np.arange(NGAL))
    sub=idx[np.isin(idx,okidx)]
    rr=np.log10(gobs[sub])-np.log10((Vg2[sub]+Ud*Vd2[sub]+1.4*Ud*Vb2[sub])*1e6/Rm[sub])
    yy=(Vg2[sub]+Ud*Vd2[sub]+1.4*Ud*Vb2[sub])*1e6/Rm[sub]/A0C
    mm=np.abs(np.log10(yy/6.0))<0.15
    if mm.sum()>=8: ab.append(np.median(rr[mm]))
anchor_sig=np.std(ab)
print(f"observed boost at y~6 window: {anchor:+.4f} +/- {anchor_sig:.4f} dex  (n={m6.sum()} pts)")
print(f"claimed banked anchor:        +0.034 +/- 0.014 dex")
print(f"branch A predicts log10(1+F_A(6)) = {np.log10(1+F_A(np.array([6.]))[0]):+.4f}")
print(f"branch B predicts log10(1+F_B(6)) = {np.log10(1+make_F_B(YC_CAN)(np.array([6.]))[0]):+.4f}")
if abs(anchor-0.034) > 2*anchor_sig:
    print("!! ANCHOR DOES NOT REPRODUCE under the banked protocol (Ups=0.70, Ub=1.4*Ud):")
    print("   the observed y~6 median is NEGATIVE -- data sit BELOW gbar there, i.e. below BOTH")
    print("   branch predictions.  (The decider's own table shows +0.034 only as med(y=2) of the")
    print("   pow p=8 yt=1.5 member -- the claimed y~6 anchor appears to be a mis-transcription.)")
    print("   NOTE the y>4 points are bulge-dominated and the protocol LOCKS Ub=1.4*Ud=0.98;")
    print("   see S10 for the two-M/L robustness check before reading this as physics.")

print("\n"+"="*96)
print("S5  UPSILON ABSORPTION OF THE FINGERPRINT (the delta-family lesson)")
print("="*96)
A=RES["A  framework-nu  (can)"]; B=RES["B  throttle yc=Z/2 (can)"]
print(f"Ups shift under throttle: {A['Ud']:.3f} -> {B['Ud']:.3f}  "
      f"(refit moves M/L {'UP' if B['Ud']>A['Ud'] else 'DOWN/none'} to soak the high-y deficit)")
print(f"rms cost of throttle: {B['rms']-A['rms']:+.4f} dex (A {A['rms']:.4f} -> B {B['rms']:.4f})")
print(f"\n{'window':>8} {'raw Delta':>10} {'eff sep = medB-medA':>20} {'absorbed frac':>14}")
for ys in WINS:
    raw=np.log10((1+F_A(np.array([ys]))[0])/(1+make_F_B(YC_CAN)(np.array([ys]))[0]))
    sep=B['meds'][ys][0]-A['meds'][ys][0]
    absf=(1-sep/raw) if raw>1e-6 else np.nan
    print(f"{ys:>8g} {raw:>10.4f} {sep:>20.4f} {absf if np.isfinite(absf) else float('nan'):>14.2f}")
sepC = B['C']-A['C']
# raw Delta averaged over the actual high-y points of branch A
mA=(A['y']>=4)&(A['y']<=30)
rawC=np.median(np.log10((1+F_A(A['y'][mA]))/(1+make_F_B(YC_CAN)(A['y'][mA]))))
print(f"\nhigh-y combined stat: raw Delta(median y|4-30) = {rawC:.4f}, eff sep = {sepC:+.4f}, "
      f"absorbed = {1-sepC/rawC:.2f}")

print("\n"+"="*96)
print("S6  DISCRIMINATION TODAY (per-galaxy bootstrap; windows NOT treated as independent)")
print("="*96)
print("If a branch is the true model its post-fit residual medians are ~0; the wrong branch")
print("shows the unabsorbed fingerprint. z = med/sigma_boot per branch:")
print(f"\n{'window':>10} {'z_A':>8} {'z_B':>8}   (positive z_B = data sit ABOVE throttle prediction)")
for ys in WINS:
    zA=A['meds'][ys][0]/A['sig'][ys]; zB=B['meds'][ys][0]/B['sig'][ys]
    print(f"{ys:>10g} {zA:>8.2f} {zB:>8.2f}")
zA_C=A['C']/A['sigC']; zB_C=B['C']/B['sigC']
print(f"{'C(4-30)':>10} {zA_C:>8.2f} {zB_C:>8.2f}   <-- the single combined statistic")
drms = RES['B  throttle yc=Z/2 (can)']['RMSb']-RES['A  framework-nu  (can)']['RMSb']
# NOTE: RMSb arrays come from independent bootstrap draws, so their difference OVERSTATES
# the noise on (rms_B - rms_A); do a paired bootstrap for the honest version:
pair=[]
for _ in range(NBOOT):
    idx=boot_indices(np.arange(NGAL))
    _,rmsA,_,_=fit(F_A,A0C,idx); _,rmsB,_,_=fit(make_F_B(YC_CAN),A0C,idx)
    pair.append(rmsB-rmsA)
pair=np.array(pair)
print(f"\npaired bootstrap Delta-rms (B - A): {B['rms']-A['rms']:+.4f} +/- {pair.std():.4f} dex "
      f"-> z = {(B['rms']-A['rms'])/pair.std():.2f}")
fav = "A (framework-nu)" if abs(zA_C)<abs(zB_C) else "B (throttle)"
print(f"\nFAVORED TODAY on the combined high-y statistic: branch {fav}")
print(f"  data reject the OTHER branch at {max(abs(zA_C),abs(zB_C)):.2f} sigma "
      f"(and the favored at {min(abs(zA_C),abs(zB_C)):.2f} sigma)")

print("\n"+"="*96)
print("S7  SENSITIVITY FOR A 3-SIGMA CALL")
print("="*96)
sep_eff=abs(sepC); sig_now=B['sigC']
print(f"effective (post-absorption) separation on C: {sep_eff:.4f} dex; current sigma(C): {sig_now:.4f} dex")
if sep_eff>0:
    need=sep_eff/3.0; factor=(sig_now/need)**2
    print(f"3-sigma needs sigma(C) <= {need:.4f} dex -> {factor:.1f}x more high-y statistics "
          f"(~{int(np.ceil(factor*B['nC']))} high-y points vs {B['nC']} now, error ~1/sqrt(N))")
# Q=1 subsample
q1=np.where(GALQ==1)[0]
print(f"\nQ=1 subsample: {len(q1)} galaxies")
if len(q1)>20:
    ptsq1=np.concatenate([GALPTS[g] for g in q1])
    UdA1,rmsA1,rA1,yA1=fit(F_A,A0C,ptsq1); UdB1,rmsB1,rB1,yB1=fit(make_F_B(YC_CAN),A0C,ptsq1)
    CA1,nA1=highy_stat(rA1,yA1); CB1,nB1=highy_stat(rB1,yB1)
    bootq=[]
    for _ in range(NBOOT):
        idx=boot_indices(q1)
        _,_,rr,yy=fit(make_F_B(YC_CAN),A0C,idx)
        bootq.append(highy_stat(rr,yy)[0])
    sq=np.nanstd(bootq)
    print(f"  A: Ups={UdA1:.3f} rms={rmsA1:.4f} C={CA1:+.4f} | B: Ups={UdB1:.3f} rms={rmsB1:.4f} "
          f"C={CB1:+.4f} +/- {sq:.4f} (n={nB1}) -> z_B(Q=1) = {CB1/sq:.2f}")
# fixed-Ups (external M/L prior kills the absorption channel)
print("\nfixed Ups=0.70 for BOTH branches (perfect external M/L prior; no absorption):")
for tag,Fb in (("A",F_A),("B",make_F_B(YC_CAN))):
    gb=(Vg2+0.70*Vd2+1.4*0.70*Vb2)*1e6/Rm
    ok=(gb>0)&(gobs>0)&np.isfinite(gb)&(Vobs>0)
    rr=np.log10(gobs[ok])-np.log10(gb[ok]*(1+Fb(gb[ok]/A0C))); yy=gb[ok]/A0C
    Cfx,nfx=highy_stat(rr,yy)
    _,sCfx,_,_,_,_=bootstrap(Fb,A0C,NBOOT,fixU=0.70)
    print(f"  {tag}: C = {Cfx:+.4f} +/- {sCfx:.4f} (n={nfx}) -> z = {Cfx/sCfx:.2f}")

print("\n"+"="*96)
print("S8  BTFR ZERO-POINT (v^4 at the flat outskirts)")
print("="*96)
UdA=A['Ud']
last=np.array([p[-1] for p in GALPTS])
gb_last=(Vg2[last]+UdA*Vd2[last]+1.4*UdA*Vb2[last])*1e6/Rm[last]
y_last=gb_last/A0C
okl=np.isfinite(y_last)&(gb_last>0)
frac_below=np.mean(y_last[okl]<YC_CAN)
dv=[0.5*np.log10((1+F_A(np.array([yl]))[0])/(1+make_F_B(YC_CAN)(np.array([yl]))[0]))
    for yl in y_last[okl]]
dv=np.array(dv)
print(f"outermost point per galaxy: {100*frac_below:.1f}% have y < y_c (throttle EXACTLY off);")
print(f"velocity shift Delta log v_flat = 0.5*Delta(y_out): median {np.median(dv):.5f} dex, "
      f"max {dv.max():.5f} dex, mean {dv.mean():.5f} dex")
print(f"-> BTFR zero-point shift <= {dv.mean():.4f} dex on average (0.01 dex in v^4 terms = "
      f"{4*dv.mean():.4f} dex in mass) -- {'UNTOUCHED' if dv.mean()<0.005 else 'affected'}")

print("\n"+"="*96)
print("S9  y~2-3 RAR CURVATURE")
print("="*96)
yk=np.array([2.0,2.5,2.894,3.0,3.5,4.0])
dk=np.log10((1+F_A(yk))/(1+make_F_B(YC_CAN)(yk)))
print("Delta(y) around the kink:", ", ".join(f"y={a:g}:{b:.4f}" for a,b in zip(yk,dk)))
slope=(dk[4]-dk[2])/ (np.log10(3.5)-np.log10(2.894))
print(f"the throttle is exactly zero through y=2.894 then rises with initial slope "
      f"~{slope:.3f} dex/dex: a KINK (2nd-derivative discontinuity) at y_c, curvature in the")
print("y=2-3 RAR is IDENTICAL between branches below y_c -- no curvature discriminator there.")

print("\n"+"="*96)
print("S10 ROBUSTNESS: FREE BULGE M/L (the high-y windows are bulge-dominated; the banked")
print("    protocol locks Ub = 1.4*Ud = 0.98 -- is the high-y offset an M/L artifact?)")
print("="*96)
# how bulge-dominated is the discriminating region?
UdA=A['Ud']
gbA=(Vg2+UdA*Vd2+1.4*UdA*Vb2)*1e6/Rm
okA=(gbA>0)&(gobs>0)&np.isfinite(gbA)&(Vobs>0)
yA=gbA[okA]/A0C
fb=(1.4*UdA*Vb2[okA])/(Vg2[okA]+UdA*Vd2[okA]+1.4*UdA*Vb2[okA])
mh=(yA>=4)&(yA<=30)
print(f"bulge fraction of gbar at 4<=y<=30 points: median {np.median(fb[mh]):.2f}, "
      f"mean {np.mean(fb[mh]):.2f}; fraction of points >50% bulge: {np.mean(fb[mh]>0.5):.2f}")

UBGRID=np.arange(0.30,1.2001,0.05)
def fit2(boost,a0,idx=None,ubgrid=UBGRID):
    if idx is None: idx=slice(None)
    _Vg2,_Vd2,_Vb2,_Rm=Vg2[idx],Vd2[idx],Vb2[idx],Rm[idx]
    _gobs,_Vobs,_w=gobs[idx],Vobs[idx],w[idx]
    best=(None,None,1e9,None,None)
    for Ud in UGRID:
        base=(_Vg2+Ud*_Vd2)
        for Ub in ubgrid:
            gb=(base+Ub*_Vb2)*1e6/_Rm
            ok=(gb>0)&(_gobs>0)&np.isfinite(gb)&(_Vobs>0)
            gp=gb[ok]*(1.0+boost(gb[ok]/a0))
            r=np.log10(_gobs[ok])-np.log10(gp)
            rms=np.sqrt(np.sum(_w[ok]*r**2)/np.sum(_w[ok]))
            if rms<best[2]: best=(Ud,Ub,rms,r,gb[ok]/a0)
    return best
R2={}
for tag,Fb in (("A",F_A),("B",make_F_B(YC_CAN))):
    Ud2_,Ub2_,rms2,r2,y2=fit2(Fb,A0C)
    meds2=win_medians(r2,y2); C2,n2=highy_stat(r2,y2)
    R2[tag]=dict(Ud=Ud2_,Ub=Ub2_,rms=rms2,meds=meds2,C=C2,n=n2)
    ms=" ".join(f"y={ys:g}:{meds2[ys][0]:+.4f}" for ys in WINS)
    print(f"  {tag}: Ud={Ud2_:.3f} Ub={Ub2_:.3f} rms={rms2:.4f} | {ms} | C={C2:+.4f} (n={n2})")
# paired bootstrap on the 2-M/L discrimination (coarser Ub grid for speed)
UBG_B=np.arange(0.30,1.2001,0.10)
NB2=150
pair2=[];CA2boot=[];CB2boot=[]
for _ in range(NB2):
    idx=boot_indices(np.arange(NGAL))
    _,_,rmsA2,rA2,yA2=fit2(F_A,A0C,idx,UBG_B)
    _,_,rmsB2,rB2,yB2=fit2(make_F_B(YC_CAN),A0C,idx,UBG_B)
    pair2.append(rmsB2-rmsA2)
    CA2boot.append(highy_stat(rA2,yA2)[0]); CB2boot.append(highy_stat(rB2,yB2)[0])
pair2=np.array(pair2); sCA2=np.nanstd(CA2boot); sCB2=np.nanstd(CB2boot)
d2rms=R2['B']['rms']-R2['A']['rms']
print(f"\n  2-M/L paired Delta-rms (B-A): {d2rms:+.4f} +/- {pair2.std():.4f} -> z = {d2rms/pair2.std():+.2f}")
print(f"  2-M/L high-y stat: A C={R2['A']['C']:+.4f} +/- {sCA2:.4f} (z={R2['A']['C']/sCA2:+.2f}); "
      f"B C={R2['B']['C']:+.4f} +/- {sCB2:.4f} (z={R2['B']['C']/sCB2:+.2f})")
mov=abs(R2['A']['C']-A['C'])
print(f"  bulge-M/L moves the branch-A high-y stat by {mov:.4f} dex "
      f"(fingerprint separation is {abs(sepC):.4f} dex)")
if mov > abs(sepC):
    print("  -> the bulge-M/L systematic is LARGER than the A-vs-B separation: any preference")
    print("     between the branches at high y is NOT robust to the M/L treatment.")

print(f"\n[runtime {time.time()-t0:.1f}s]")
print("exit 0")
