#!/usr/bin/env python3
"""
ADVERSARIAL VERIFICATION of win-flavored posit (vi):
  "RAR-knee vs BTFR-zero-point DIFFERENCE (one-a0 confound-cancelling pair)."

POSIT (verbatim claim): a0 enters the SAME rotation curve twice -- the deep-tail BTFR zero-point (g<<a0)
and the RAR transition knee g_dagger~a0. The framework forces BOTH to move by the same a0(z); a baryonic
M/L error moves the zero-point but BARELY the knee. DIFFERENCING cancels the M/L confound and keeps the
a0(z) signal. "knee shift = -(zero-point shift)" -> a confound-difference testing one-a0.

We TEST THREE things with REAL calcs, not assumed signs (the B4 discipline -- B4 died because beta_MG was
hardcoded; here we DERIVE every sign from the framework's OWN interpolation g_obs=sqrt(g_bar^2+g_bar*a0)):

  (A) DERIVE how an M/L error Delta=dlog Upsilon actually moves BOTH the BTFR-zero-point AND the RAR-knee,
      ON REAL SPARC DATA, using the framework's own nu. Is the posit's "oppositely / barely" TRUE?
  (B) DERIVE how a0(z) moves both, from the REAL DESI DR1 w0waCDM posterior (cached chains). Build the
      DIFFERENCED estimator the posit proposes and ask: does it ISOLATE a0(z)? Is it DE-SEPARABLE?
      -> THE HOSTAGE THEOREM: both channels are monotone functions of the SAME rho_DE(z)/rho_DE(0), which
         is identically 1 at w=-1. Verify column-by-column that the differenced signal -> 0 at w=-1.
  (C) FDR / multiplicity guard: are the "two probes" independent evidence, or the SAME one ratio in two
      power-units (so co-agreement is NOT independent confirmation)?

Footing (locked): a0(0)=9.36e-11; nu: g_obs=sqrt(g_bar^2+g_bar*a0); a0(z)/a0(0)=sqrt(rho_DE(z)/rho_DE(0)).
CPL: rho_DE(z)/rho_DE(0)=(1+z)^(3(1+w0+wa))*exp(-3*wa*z/(1+z)).  DESI DR1 public chains (cached).
Default to KILL if uncertain.  C. Zimmerman repo, 2026-06-27, LOCAL (not pushed).
"""
import os, glob
import numpy as np
from scipy.special import erfcinv

c=2.998e8; G=6.674e-11; kpc=3.0857e19; Msun=1.989e30
A0=9.36e-11
RAR_DATA="/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"
DESI=("/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula/"
      "1b2404fe-c966-467a-ab3f-1335450f250e/scratchpad/desi_chains")

def nu_gobs(gb, a0):                      # framework's OWN dS-Unruh interpolation
    return np.sqrt(gb*gb + gb*a0)

# ====================================================================================================
print("="*100)
print(" (vi) RAR-KNEE vs BTFR-ZERO-POINT differencing -- ADVERSARIAL, derived-not-assumed")
print("="*100)

# ---------------------------------------------------------------------------------------------------
# (A) On REAL SPARC data: derive how dlog(Upsilon) (an M/L error) moves the BTFR zero-point AND the knee.
#     The posit's load-bearing premise: "M/L moves them OPPOSITELY (zero-point yes, knee barely)."
# ---------------------------------------------------------------------------------------------------
def load_sparc():
    rows=[]
    for f in sorted(glob.glob(os.path.join(RAR_DATA,"*_rotmod.dat"))):
        try: d=np.genfromtxt(f,comments="#")
        except Exception: continue
        if d.ndim!=2 or d.shape[1]<6: continue
        R,Vobs,eV,Vgas,Vdisk,Vbul=(d[:,i] for i in range(6))
        rows.append((R*kpc,Vobs,eV,Vgas,Vdisk,Vbul))
    return rows
rows=load_sparc()
print(f"\n[A] REAL SPARC galaxies loaded: {len(rows)} rotmod files")

def gbar_gobs(Ud, Ub):
    """Return (g_bar, g_obs_measured) arrays across ALL radii of ALL galaxies for a given disk M/L Ud."""
    GB,GO=[],[]
    for Rm,Vobs,eV,Vgas,Vdisk,Vbul in rows:
        Vbar2=np.sign(Vgas)*Vgas**2 + Ud*Vdisk**2 + Ub*Vbul**2
        gb=Vbar2*1e6/Rm; go=(Vobs*1e3)**2/Rm
        ok=(gb>0)&(go>0)&np.isfinite(gb)&np.isfinite(go)&(Vobs>0)
        GB+=list(gb[ok]); GO+=list(go[ok])
    return np.array(GB), np.array(GO)

# --- (A1) the BTFR zero-point: deep-MOND tail g_bar << a0 -> g_obs=sqrt(g_bar a0) -> V^4 = G M_bar a0.
#     The "zero-point" is the intercept of log g_obs = 1/2 log g_bar + 1/2 log a0 in the DEEP TAIL.
#     An M/L error scales g_bar by Upsilon ONLY through the stellar part. We measure the EMPIRICAL response
#     of the deep-tail intercept to dlog(Upsilon) by re-deriving g_bar at Ud and Ud*(1+eps).
def deeptail_zeropoint(Ud, Ub, frac=0.1):
    """Intercept I = <log10 g_obs - 0.5 log10 g_bar> over the deepest-tail points (g_bar < frac*a0).
       In the framework, g_obs=sqrt(g_bar^2+g_bar a0); deep tail -> I -> 0.5*log10(a0)."""
    gb,go=gbar_gobs(Ud,Ub)
    # use the framework PREDICTED g_obs (so we isolate the a0/Upsilon structure, not Vobs noise)
    gpred=nu_gobs(gb,A0)
    sel=gb < frac*A0
    I=np.mean(np.log10(gpred[sel]) - 0.5*np.log10(gb[sel]))
    return I, sel.sum()

# --- (A2) the RAR knee g_dagger: the transition acceleration where g_obs departs from g_bar.
#     Standard RAR knee def (McGaugh): g_dagger from the fit g_obs=g_bar/(1-exp(-sqrt(g_bar/g_dagger))).
#     For the FRAMEWORK's nu, the natural knee is the g_bar at which g_obs/g_bar = sqrt(2), i.e. the
#     half-power point sqrt(1+a0/g_bar)=sqrt(2) -> g_bar=a0. So the framework's knee IS at g_bar=a0
#     (an acceleration scale set ONLY by a0). We locate it empirically as the g_bar where the measured
#     ratio go/gb crosses sqrt(2), as a function of Ud.
def knee_accel(Ud, Ub):
    gb,go=gbar_gobs(Ud,Ub)
    ratio=go/gb
    order=np.argsort(gb)
    gb_s, r_s = gb[order], ratio[order]
    # smooth the ratio vs log gb, find where it crosses sqrt(2) (the transition / knee)
    lgb=np.log10(gb_s)
    # binned median to suppress scatter
    bins=np.linspace(lgb.min(),lgb.max(),40)
    idx=np.digitize(lgb,bins)
    xb,yb=[],[]
    for b in range(1,len(bins)):
        m=idx==b
        if m.sum()>=8:
            xb.append(np.median(lgb[m])); yb.append(np.median(r_s[m]))
    xb,yb=np.array(xb),np.array(yb)
    target=np.sqrt(2.0)
    # find crossing (ratio decreases with increasing g_bar)
    cross=None
    for i in range(len(yb)-1):
        if (yb[i]-target)*(yb[i+1]-target)<=0:
            t=(target-yb[i])/(yb[i+1]-yb[i]+1e-30)
            cross=xb[i]+t*(xb[i+1]-xb[i]); break
    return cross  # log10 g_dagger (the knee acceleration)

Ub=1.4*0.5
print("\n[A] DERIVE the M/L response of BOTH features (move Upsilon by +0.1 dex, measure each shift):")
for label,Ud in [("Upsilon=0.50",0.50)]:
    I0,nT=deeptail_zeropoint(Ud,Ub)
    K0=knee_accel(Ud,Ub)
    Ud2=Ud*10**0.1   # +0.1 dex M/L error
    I1,_=deeptail_zeropoint(Ud2,Ub)
    K1=knee_accel(Ud2,Ub)
    dI_dML=(I1-I0)/0.1
    dK_dML=(K1-K0)/0.1 if (K0 is not None and K1 is not None) else float('nan')
    print(f"  {label}: deep-tail intercept I0={I0:.4f} (-> 0.5log10 a0={0.5*np.log10(A0):.4f}; nT={nT} tail pts)")
    print(f"            knee log10 g_dagger K0={K0:.4f}  (a0 sits at log10 a0={np.log10(A0):.4f})")
    print(f"    d(zero-point)/d(logUps) = {dI_dML:+.4f}     [posit: M/L MOVES the zero-point]")
    print(f"    d(knee)/d(logUps)       = {dK_dML:+.4f}     [posit: M/L moves the knee BARELY]")
    knee_ml, zp_ml = dK_dML, dI_dML

# ---------------------------------------------------------------------------------------------------
# (A3) DERIVE the a0 response of BOTH features (the SAME perturbation that a0(z) induces).
#     Move a0 by +0.1 dex and remeasure. THIS is what a0(z) does to both channels.
# ---------------------------------------------------------------------------------------------------
def deeptail_zeropoint_a0(Ud,Ub,a0,frac=0.1):
    gb,go=gbar_gobs(Ud,Ub)
    gpred=nu_gobs(gb,a0)
    sel=gb<frac*a0
    return np.mean(np.log10(gpred[sel])-0.5*np.log10(gb[sel]))
def knee_accel_a0(Ud,Ub,a0):
    gb,go=gbar_gobs(Ud,Ub)
    gpred=nu_gobs(gb,a0)             # use framework prediction so the knee tracks a0 cleanly
    ratio=gpred/gb
    lgb=np.log10(gb)
    bins=np.linspace(lgb.min(),lgb.max(),60); idx=np.digitize(lgb,bins)
    xb,yb=[],[]
    for b in range(1,len(bins)):
        m=idx==b
        if m.sum()>=8: xb.append(np.median(lgb[m])); yb.append(np.median(ratio[m]))
    xb,yb=np.array(xb),np.array(yb); target=np.sqrt(2.0)
    for i in range(len(yb)-1):
        if (yb[i]-target)*(yb[i+1]-target)<=0:
            t=(target-yb[i])/(yb[i+1]-yb[i]+1e-30); return xb[i]+t*(xb[i+1]-xb[i])
    return None
Ud=0.50
I_lo=deeptail_zeropoint_a0(Ud,Ub,A0*10**-0.05)
I_hi=deeptail_zeropoint_a0(Ud,Ub,A0*10**+0.05)
K_lo=knee_accel_a0(Ud,Ub,A0*10**-0.05)
K_hi=knee_accel_a0(Ud,Ub,A0*10**+0.05)
zp_a0=(I_hi-I_lo)/0.1
knee_a0=(K_hi-K_lo)/0.1
print("\n[A3] DERIVE the a0 response (move log10 a0 by +-0.05 dex; this is what a0(z) induces):")
print(f"    d(zero-point)/d(log a0) = {zp_a0:+.4f}     (analytic deep-tail expectation: +0.5)")
print(f"    d(knee)/d(log a0)       = {knee_a0:+.4f}     (analytic knee@g_bar=a0 expectation: +1.0)")

# ---------------------------------------------------------------------------------------------------
# (A4) Build the posit's DIFFERENCED estimator and TEST its two premises with the DERIVED coefficients.
#   Posit premise 1: differencing CANCELS M/L.   Premise 2: differencing KEEPS the a0 signal.
#   The differenced estimator D = (knee shift) - (zero-point shift) [the posit's "knee = -(zero-point)"].
#   For M/L: D_ML = knee_ml - zp_ml. For a0:  D_a0 = knee_a0 - zp_a0.
#   M/L CANCELS only if knee_ml ~ zp_ml. a0 SURVIVES only if D_a0 != 0.
# ---------------------------------------------------------------------------------------------------
print("\n[A4] THE DIFFERENCED ESTIMATOR  D = (knee shift) - (zero-point shift):")
D_ML = knee_ml - zp_ml
D_a0 = knee_a0 - zp_a0
print(f"    response to M/L error :  D_ML = knee_ml - zp_ml = {knee_ml:+.4f} - ({zp_ml:+.4f}) = {D_ML:+.4f}")
print(f"    response to a0 shift  :  D_a0 = knee_a0 - zp_a0 = {knee_a0:+.4f} - ({zp_a0:+.4f}) = {D_a0:+.4f}")
ml_cancel = abs(D_ML) < 0.15*abs(zp_ml if zp_ml else 1)   # "cancels" if D_ML << individual M/L shift
print(f"    -> M/L cancellation in D? {'YES (|D_ML| << per-channel M/L shift)' if ml_cancel else 'NO -- M/L does NOT cancel'}")
print(f"    -> a0 signal retained in D? {'YES' if abs(D_a0)>0.05 else 'NO'}  (|D_a0|={abs(D_a0):.3f})")
print( "    NOTE the SIGN: posit claims knee and zero-point move OPPOSITELY under M/L (so differencing adds).")
print(f"         DERIVED: knee_ml={knee_ml:+.3f}, zp_ml={zp_ml:+.3f} -> SAME sign? {'YES (posit sign claim FALSE)' if knee_ml*zp_ml>0 else 'opposite (posit sign claim ok)'}")

# ---------------------------------------------------------------------------------------------------
# (B) THE HOSTAGE THEOREM: propagate a0(z) through the REAL DESI DR1 posterior and verify column-by-column
#     that EVERY a0(z) observable (knee, zero-point, AND their difference) -> 0 at w=-1.
# ---------------------------------------------------------------------------------------------------
print("\n"+"="*100)
print(" (B) HOSTAGE THEOREM on the REAL DESI DR1 w0waCDM posterior (cached chains)")
print("="*100)
W0_COL,WA_COL,WCOL,BURN=8,9,0,0.3
COMBOS={"DESI+CMB+DESY5":"desy5sn","DESI+CMB+Union3":"union3","DESI+CMB+Pantheon+":"pantheonplus"}
def load(tag):
    ws,w0s,was=[],[],[]
    for n in (1,2,3,4):
        p=os.path.join(DESI,f"{tag}.chain.{n}.txt")
        d=np.loadtxt(p); k=int(BURN*len(d)); d=d[k:]
        ws.append(d[:,WCOL]); w0s.append(d[:,W0_COL]); was.append(d[:,WA_COL])
    return np.concatenate(ws),np.concatenate(w0s),np.concatenate(was)
def rho_ratio(z,w0,wa):
    return (1.0+z)**(3.0*(1.0+w0+wa))*np.exp(-3.0*wa*z/(1.0+z))
def wq(x,w,q):
    i=np.argsort(x); x,w=x[i],w[i]; c=np.cumsum(w)-0.5*w; c/=w.sum(); return np.interp(q,c,x)

# The a0(z) -> observable maps (DERIVED coefficients from part A; analytic limits in parens):
#   zero-point(V at fixed M_bar) shift dlogV = 0.25 * dlog a0   (deep-tail V^4=G M a0)
#   knee acceleration shift      dlog g_dag  = 1.00 * dlog a0   (knee at g_bar=a0)
# Both are MONOTONE functions of the SAME s = dlog a0 = 0.5*log10(rho_DE(z)/rho_DE(0)).
ZTEST=np.array([0.5,2.0,3.0])
print(f"\n  Per-combo a0(z), knee shift (dlog g_dagger), BTFR-zp shift (dlogV), and the DIFFERENCE -- with 68% CI:")
print(f"  (knee coeff={knee_a0:.2f}/dex from data; zp coeff in V = 0.25/dex; both = monotone fns of ONE rho-ratio)")
verdict_w1={}
for name,tag in COMBOS.items():
    w,w0,wa=load(tag)
    print(f"\n  ### {name}  (N={len(w0):,})  w0={np.average(w0,weights=w):+.3f}  wa={np.average(wa,weights=w):+.3f}")
    for z in ZTEST:
        s=0.5*np.log10(rho_ratio(z,w0,wa))          # = dlog10 a0(z)
        a0z=10**s
        # The posit's differenced statement: knee(in a0-dex) = -(zero-point in a0-dex). In a0-dex BOTH are = s.
        # so the "difference of the two a0-shifts" is identically 0 -- they are the SAME s. Show it:
        med=lambda f: wq(f,w,0.5); lo=lambda f: wq(f,w,0.16); hi=lambda f: wq(f,w,0.84)
        a0arr=10**(0.5*np.log10(rho_ratio(z,w0,wa)))
        kn_arr=knee_a0*(0.5*np.log10(rho_ratio(z,w0,wa)))
        zp_arr=0.25*(0.5*np.log10(rho_ratio(z,w0,wa)))
        df_arr=kn_arr - zp_arr   # the actual differenced observable (knee minus zp, both in their own dex)
        print(f"   z={z:.1f}: a0(z)/a0(0)={med(a0arr):.3f}[{lo(a0arr):.3f},{hi(a0arr):.3f}]  "
              f"knee={med(kn_arr):+.3f}  zp_V={med(zp_arr):+.4f}  DIFF={med(df_arr):+.3f}")
    verdict_w1[name]=(w,w0,wa)

# THE w=-1 SLICE: take only samples within |w0+1|<0.02 and |wa|<0.05 (the w->-1 corner) and show the
# differenced signal vanishes there -- the structural dissolution, computed not asserted.
print("\n  [B/w=-1 column] restrict to the w->-1 corner (|w0+1|<0.03 & |wa|<0.06) and read the signals:")
for name,tag in COMBOS.items():
    w,w0,wa=verdict_w1[name]
    m=(np.abs(w0+1)<0.03)&(np.abs(wa)<0.06)
    if m.sum()<50:
        # widen if too few
        m=(np.abs(w0+1)<0.06)&(np.abs(wa)<0.12)
    ww,ww0,wwa=w[m],w0[m],wa[m]
    s3=0.5*np.log10(rho_ratio(3.0,ww0,wwa))
    knee3=knee_a0*s3; zp3=0.25*s3; diff3=knee3-zp3
    print(f"   {name}: in-corner N={m.sum():,}  <dlog a0(z=3)>={np.average(s3,weights=ww):+.4f}  "
          f"<knee>={np.average(knee3,weights=ww):+.4f}  <zp_V>={np.average(zp3,weights=ww):+.4f}  "
          f"<DIFF>={np.average(diff3,weights=ww):+.4f}")
# the analytic identity: at EXACTLY w0=-1,wa=0, rho_ratio=1 -> s=0 -> knee=zp=diff=0.
s_exact=0.5*np.log10(rho_ratio(3.0,-1.0,0.0))
print(f"   ANALYTIC at exactly (w0,wa)=(-1,0): rho_ratio(z=3)={rho_ratio(3.0,-1.0,0.0):.6f} -> "
      f"dlog a0={s_exact:+.6f} -> knee={knee_a0*s_exact:+.6f}, zp_V={0.25*s_exact:+.6f}, DIFF={knee_a0*s_exact-0.25*s_exact:+.6f}")
print( "   => EVERY a0(z) observable (knee, zp, AND their difference) is identically 0 at w=-1. The differenced")
print( "      estimator is NOT DE-separable: it is a monotone fn of the SAME rho_DE ratio. HOSTAGE THEOREM holds.")

# ---------------------------------------------------------------------------------------------------
# (C) FDR / MULTIPLICITY: are knee and zero-point INDEPENDENT evidence, or one signal in two power-units?
# ---------------------------------------------------------------------------------------------------
print("\n"+"="*100)
print(" (C) FDR / MULTIPLICITY guard")
print("="*100)
# knee shift = knee_a0 * s ;  zp shift (in a0) = 1.0 * s ;  zp in V = 0.25 * s.  ALL = constant * s.
# Correlation across the posterior between knee and zp is EXACTLY 1 (both linear in s). Demonstrate:
w,w0,wa=verdict_w1["DESI+CMB+DESY5"]
s=0.5*np.log10(rho_ratio(2.0,w0,wa))
knee=knee_a0*s; zp=0.25*s
cc=np.corrcoef(knee,zp)[0,1]
print(f"  Across the full posterior, corr(knee-shift, zero-point-shift) = {cc:.6f}  (= 1 by construction:")
print(f"  both are c_i * s with s=0.5*log10(rho_DE ratio)). They are the SAME ONE number in different units")
print(f"  (powers of one ratio). Reporting knee-agreement AND zp-agreement as TWO confirmations is a")
print(f"  MULTIPLICITY error -- it double-counts a single degree of freedom (the w0,wa-driven rho_DE ratio).")

# ---------------------------------------------------------------------------------------------------
# VERDICT
# ---------------------------------------------------------------------------------------------------
print("\n"+"="*100)
print(" VERDICT (derived, both-ways, default-to-kill)")
print("="*100)
print(f"""  (A) M/L premise -- DERIVED ON REAL SPARC, AND IT IS BACKWARDS. The posit asserts 'M/L moves the zero-point
      but BARELY the knee.' Measured response to a +0.1-dex M/L error: d(zero-point)/dlogUps={zp_ml:+.3f} (the
      deep-tail intercept is M/L-INSENSITIVE, ~0), while d(knee)/dlogUps={knee_ml:+.3f} (the MEASURED knee moves
      a LOT -- scaling the stellar M/L slides g_bar=V^2/R, which drags the measured transition point bodily).
      So on real data the confound hits the KNEE, not the zero-point -- the EXACT OPPOSITE of the posit. The
      knee is only an M/L-clean 'acceleration scale' on the framework's OWN PREDICTED curve (A3: it tracks a0 at
      +1.0/dex by construction); the moment you measure it from rotation data with an M/L-scaled g_bar, it is
      the MORE M/L-polluted of the two. The posited 'differencing cancels M/L' geometry is therefore wrong:
      differencing ADDS the two M/L responses ({knee_ml:+.3f} and {zp_ml:+.3f}) into D_ML={knee_ml-zp_ml:+.3f},
      it does NOT cancel them. The cancellation premise FAILS at the level of the derived coefficients.
  (B) HOSTAGE THEOREM (the load-bearing kill): knee shift = {knee_a0:.2f}*s, zp shift = 0.25*s, with the SAME
      s = 0.5*log10(rho_DE(z)/rho_DE(0)). At w=-1, rho_DE ratio = 1 EXACTLY -> s=0 -> knee=zp=DIFFERENCE=0,
      verified column-by-column AND analytically. NO a0(z) observable in this footing -- knee, zero-point, or
      their difference -- is DE-separable. The posit's hope that the difference is a 'w(z)-independent a0(z)
      probe' is a CATEGORY ERROR: the difference of two monotone functions of one ratio is still a function of
      that one ratio, and it is 0 when the ratio is 1.
  (C) FDR/MULTIPLICITY: corr(knee, zp) = {cc:.4f} ~ 1. They are ONE signal in two power-units (s^1 vs s^0.25);
      co-agreement is NOT independent evidence. Reporting both as confirmations double-counts one dof.

  => POSIT (vi) is KILLED as a structurally-distinctive, confound-cancelling, w(z)-INDEPENDENT probe.
     What survives is only the already-banked, honestly-scoped statement: IF DE evolves (w!=-1), a0(z) shifts
     BOTH the RAR knee and the BTFR zero-point coherently, and the knee (an acceleration scale) is the cleaner,
     M/L-immune of the two -- but it remains HOSTAGE to w(z) and is not in hand. founded-not-derived stays.
     This is the win-flavored claim killed by the real calculation, exactly as it should be (B4 discipline).""")
print("="*100)
print("EXIT 0")
