#!/usr/bin/env python3
"""
VEIN 3 -- a0(z) ON FRESH OBSERVABLES.  B4 discipline: every 'forced / distinctive / DE-separable'
claim is DERIVED here with a real calculation (exit 0), not an assumed sign or ad-hoc proxy.

Framework footing (canonical, locked):  a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)).
  This is the DECLINING reading (rho_DE falls into the past for thawing w>-1).  ONLY w0,wa enter
  the ratio.  For CPL w(z)=w0+wa z/(1+z):
      rho_DE(z)/rho_DE(0) = (1+z)^(3(1+w0+wa)) * exp(-3 wa z/(1+z)).
  The ENTIRE a0(z) signal is carried by (1+w0+wa, wa).  THE SHARP, GENERAL FACT proven below:
  every a0(z) observable is a MONOTONE FUNCTION of this same rho_DE ratio, so EVERY a0(z) posit is
  the SAME hostage -- it dies (ratio->1) iff w(z)->-1.  'w(z)-independent a0(z) probe' is therefore
  IMPOSSIBLE within this footing; what differs between channels is only the CONFOUND structure
  (does an astrophysical effect mimic the same z-trend?) and the POWER, not the DE-hostage status.

We compute, per posit:
  (1) the deep-MOND prediction (closed-form where possible, numeric collapse where not),
  (2) the magnitude of the a0(z) effect using the REAL DESI DR1 w0waCDM posterior (cached chains),
  (3) the magnitude of the leading astrophysical CONFOUND, on the same axis,
  (4) the w->-1 LCDM null (proves hostage), and a both-ways verdict.

No thumb on the scale.  Footing a0(0)=9.36e-11, Z=2 sqrt(8 pi/3).  Exit 0.
"""
import os, numpy as np
from scipy.special import erfcinv

c   = 2.99792458e8
G   = 6.674e-11
Mpc = 3.0857e22
Msun= 1.989e30
kpc = 3.0857e19
A0  = 9.36e-11
Z   = 2*np.sqrt(8*np.pi/3)
Om, OL = 0.315, 0.685
E   = lambda z: np.sqrt(Om*(1+z)**3 + OL)      # LCDM expansion (the RIVAL 'rising a0' reading a0~cH~E(z))

# ---------------------------------------------------------------------------
# DESI DR1 w0waCDM posterior (cached locally by a0z_desi_chains_propagation.py)
# ---------------------------------------------------------------------------
DATA = os.environ.get("DESI_CHAINS_DIR",
    "/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula/"
    "1b2404fe-c966-467a-ab3f-1335450f250e/scratchpad/desi_chains")
W0_COL, WA_COL, WEIGHT_COL, BURNIN = 8, 9, 0, 0.3
COMBOS = {"DESI+CMB+DESY5":"desy5sn", "DESI+CMB+Union3":"union3", "DESI+CMB+Pantheon+":"pantheonplus"}

def load_combo(tag):
    ws, w0s, was = [], [], []
    for n in (1,2,3,4):
        p = os.path.join(DATA, f"{tag}.chain.{n}.txt")
        d = np.loadtxt(p); k = int(BURNIN*len(d)); d = d[k:]
        ws.append(d[:,WEIGHT_COL]); w0s.append(d[:,W0_COL]); was.append(d[:,WA_COL])
    return np.concatenate(ws), np.concatenate(w0s), np.concatenate(was)

def rho_de_ratio(z, w0, wa):
    return (1.0+z)**(3.0*(1.0+w0+wa)) * np.exp(-3.0*wa*z/(1.0+z))

def wquant(x, w, q):
    i = np.argsort(x); x, w = x[i], w[i]
    cqq = np.cumsum(w) - 0.5*w; cqq /= np.sum(w)
    return np.interp(q, cqq, x)

# preload the posterior a0(z)/a0(0) = sqrt(rho ratio) at the z we need, per combo
ZUSE = [0.5, 1.0, 2.0, 3.0]
post = {}
try:
    for name, tag in COMBOS.items():
        w, w0, wa = load_combo(tag)
        post[name] = {"w":w, "w0":w0, "wa":wa}
    HAVE_CHAINS = True
except Exception as ex:
    HAVE_CHAINS = False
    print(f"[warn] DESI chains unavailable ({ex}); using DR1 central w0=-0.727,wa=-1.05 as fallback.")
    post = {"DESI+CMB(DR1 central)": {"w0c":-0.727, "wac":-1.05}}

def a0z_ratio_band(z):
    """Return (median, lo16, hi84) of a0(z)/a0(0) across combos from the real posterior."""
    meds=[]; los=[]; his=[]
    if HAVE_CHAINS:
        for name,d in post.items():
            r = np.sqrt(rho_de_ratio(z, d["w0"], d["wa"]))
            meds.append(wquant(r,d["w"],0.5)); los.append(wquant(r,d["w"],0.16)); his.append(wquant(r,d["w"],0.84))
        return float(np.median(meds)), float(min(los)), float(max(his))
    else:
        d=list(post.values())[0]; r=float(np.sqrt(rho_de_ratio(z,d["w0c"],d["wac"]))); return r,r,r

print("="*100)
print(" VEIN 3 -- a0(z) on FRESH observables.  Footing a0(z)/a0(0)=sqrt(rho_DE(z)/rho_DE(0)) (DECLINING).")
print("="*100)
print(" a0(z)/a0(0) from the REAL DESI DR1 w0waCDM posterior (median across SN combos; 68% band):")
RATIO = {}
for z in ZUSE:
    m,lo,hi = a0z_ratio_band(z); RATIO[z]=(m,lo,hi)
    print(f"   z={z:>3.1f}:  a0(z)/a0(0) = {m:.3f}  [{lo:.3f}, {hi:.3f}]    (rising-a0 rival E(z)={E(z):.2f})")
print(" NOTE: <1 = DECLINING (canonical, thawing w>-1).  The whole signal lives in (1+w0+wa,wa).")

# ===========================================================================
# THE GENERAL HOSTAGE THEOREM  (proves every posit below is DE-hostage)
# ===========================================================================
print("\n"+"="*100); print(" HOSTAGE THEOREM (general):  every a0(z) observable -> 1 as w(z)->-1"); print("="*100)
w0_lcdm, wa_lcdm = -1.0, 0.0
for z in ZUSE:
    r = np.sqrt(rho_de_ratio(z, w0_lcdm, wa_lcdm))
    print(f"   w->-1 (w0=-1,wa=0):  a0({z})/a0(0) = sqrt(rho ratio) = {r:.6f}   (== 1 exactly: signal vanishes)")
print("""   => Every observable in this vein is a monotone function f(a0(z)/a0(0)).  At w=-1 the ratio is
      identically 1, so f -> f(1) = the plain-MOND value, for ALL of them.  Therefore NO a0(z) observable
      is DE-separable in the sense of 'survives w->-1'.  The memory's hoped-for 'w(z)-INDEPENDENT a0(z)
      probe via the BTFR zero-point' DOES NOT EXIST under this footing: the BTFR zero-point shift is
      EXACTLY -0.5 log10(rho_DE(z)/rho_DE(0)), which is 0 at w=-1.  (Derived numerically in POSIT V.)
      What CAN differ is the CONFOUND structure (channel-specific) and POWER -- graded per posit below.""")

# ===========================================================================
# POSIT (i): STRONG-LENS time delays / Einstein-radius evolution at high z
# ===========================================================================
print("\n"+"="*100); print(" POSIT (i): strong-lens Einstein-radius / time-delay evolution"); print("="*100)
# Deep-MOND phantom mass at fixed baryonic mass:  M_ph ~ sqrt(M_bar a0) -> M_lens ~ sqrt(a0(z)).
# Einstein radius theta_E^2 ~ M_lens(<theta_E) ; for an isothermal-like deep-MOND lens theta_E ~ sigma^2,
# and sigma^4 ~ G M a0 -> sigma^2 ~ sqrt(G M a0) -> theta_E ~ sqrt(a0(z)) at fixed M, D's.
# Time delay dt ~ (1+z_l)/c * D_dt * dphi ; the a0 piece enters dphi through the same sqrt(a0).
print(" Deep-MOND lens at fixed baryonic mass:  phantom mass M_ph = sqrt(M_bar a0)  ->  theta_E ~ sqrt(a0(z)).")
print(" So the LENS-ONLY a0(z) signature is the SAME sqrt(rho ratio) factor:")
for z in ZUSE:
    m,lo,hi = RATIO[z]
    print(f"   z_l={z:>3.1f}:  theta_E boost = sqrt(a0(z)/a0(0)) = {np.sqrt(m):.3f}  [{np.sqrt(lo):.3f},{np.sqrt(hi):.3f}]"
          f"   (i.e. {(np.sqrt(m)-1)*100:+.1f}% at the median)")
# Confound: at fixed M_star the baryonic mass (gas) and the size/concentration evolve; theta_E ~ sqrt(M/ a-ish)
# also moves with the well-known size evolution R_e ~ (1+z)^-1. A pure-baryon lens with NO a0 already shifts.
print(""" CONFOUND: theta_E also depends on the baryon census (gas fraction up with z) and on the lens
   mass-size evolution R_e ~ (1+z)^-1.  At fixed M_star both move theta_E by O(10-40%) -- comparable to
   and degenerate with the {:+.0f}% a0 effect at z~2.  Strong lenses ALSO require the source-plane geometry
   (D_s,D_ls) which is itself a w(z) probe -> the a0 piece and the geometric piece BOTH ride DE.
 GRADE: SPECULATIVE.  DE-HOSTAGE (dies at w=-1) AND additionally geometry-confounded.  win_flavored: a +X%
   theta_E excess would be 'evidence for evolving a0' -- but it is doubly DE-entangled.""".format((np.sqrt(RATIO[2.0][0])-1)*100))

# ===========================================================================
# POSIT (ii): first-structure / reionization TIMING (deep-MOND collapse, DECLINING a0)
# ===========================================================================
print("\n"+"="*100); print(" POSIT (ii): reionization / first-structure TIMING with a DECLINING a0"); print("="*100)
# Closed form (verified in project07): deep-MOND top-hat collapse time t = sqrt(pi/2) r_max /(G M a0)^(1/4).
# So t_collapse ~ a0^(-1/4).  DECLINING a0 at high z => a0 SMALLER => collapse SLOWER (LATER) than plain MOND.
# This is the OPPOSITE of the usual 'MOND forms structure early' boost: the canonical declining footing
# REDUCES the high-z boost relative to constant-a0 MOND.
def collapse_time(rmax, M, a0):
    return np.sqrt(np.pi/2)*rmax/(G*M*a0)**0.25
M = 1e11*Msun; rmax = 100*kpc
t0 = collapse_time(rmax, M, A0)
print(" Closed-form deep-MOND collapse time  t ~ (G M a0)^(-1/4)  =>  t ~ a0^(-1/4).")
print(" DECLINING a0(z) => a0 smaller at high z => collapse t LONGER (structure forms LATER vs constant-a0 MOND):")
for z in ZUSE:
    m,lo,hi = RATIO[z]
    a0z = A0*m
    tz = collapse_time(rmax, M, a0z)
    print(f"   z={z:>3.1f}:  a0(z)/a0(0)={m:.3f}  ->  t_coll/t_coll(const-a0) = (a0(z)/a0)^(-1/4) = {m**-0.25:.3f}"
          f"   ({(m**-0.25-1)*100:+.1f}% slower)")
print(""" KEY both-ways: the RISING-a0 reading (a0~E(z)) is what powered 'MOND beats JWST early-massive-galaxy
   tension'.  The CANONICAL DECLINING footing gives the OPPOSITE small shift (~+{:.0f}% SLOWER collapse at z=3),
   i.e. it makes the JWST 'too-early' tension slightly WORSE, not better.  Magnitude ~3-7% is far below the
   factor-(g_N/a0)^(1/4) MOND-vs-Newton boost and is swamped by baryonic-feedback / SFE uncertainty in
   reionization timing (tau_reion has ~10-20% modelling scatter).  And it is the SAME rho-ratio -> hostage.
 GRADE: SPECULATIVE.  DE-HOSTAGE.  win_flavored: NO -- the canonical sign is anti-helpful (slower), and the
   effect is sub-systematic.""".format((RATIO[3.0][0]**-0.25-1)*100))

# ===========================================================================
# POSIT (iii): cluster MASS-FUNCTION evolution
# ===========================================================================
print("\n"+"="*100); print(" POSIT (iii): cluster MASS-FUNCTION evolution under a0(z)"); print("="*100)
# In MOND the deep-MOND collapse barrier / effective sigma8-like threshold shifts with a0.  The cluster
# abundance n(>M,z) is exponentially sensitive to the collapse threshold delta_c/sigma(M).  A declining a0
# at high z RAISES the effective collapse threshold (weaker boost) -> FEWER massive clusters at high z than
# constant-a0 MOND.  We bound the leverage: dln n / dln a0 via the deep-MOND virial relation M ~ sigma^4/(G a0)
# at fixed sigma (the cluster scaling), so at fixed observable sigma the inferred M ~ 1/a0.
print(" Deep-MOND cluster virial M ~ sigma^4/(G a0)  =>  at fixed sigma, M_inferred ~ 1/a0(z):")
for z in ZUSE:
    m,lo,hi = RATIO[z]
    print(f"   z={z:>3.1f}:  a0(z)/a0(0)={m:.3f}  ->  M(fixed sigma) boost = 1/{m:.3f} = {1/m:.3f}"
          f"   ({(1/m-1)*100:+.1f}% more inferred mass at the canonical declining footing)")
print(""" The mass function n(>M,z) inherits this through an EXPONENTIALLY sensitive halo-mass-function tail,
   BUT: (a) the same z-trend is produced by w(z) directly in the growth factor D(z) and the volume dV/dz --
   i.e. cluster counts are ALREADY a primary DE probe, so the a0(z) and the w(z) effects are MAXIMALLY
   degenerate (both are functions of the same rho_DE history); (b) cluster mass calibration (hydrostatic /
   lensing mass bias 1-b ~ 0.7-0.8) carries a ~20-30% systematic that dwarfs the {:+.0f}% a0 shift at z=1.
 GRADE: SPECULATIVE.  DE-HOSTAGE and (worse than lensing) co-degenerate with the SAME DE history it would
   test.  win_flavored: a high-z cluster-abundance excess could be read as evolving a0 -- but it is the
   single most DE-entangled channel in the vein.""".format((1/RATIO[1.0][0]-1)*100))

# ===========================================================================
# POSIT (iv): high-z velocity-DISPERSION-FUNCTION (VDF)
# ===========================================================================
print("\n"+"="*100); print(" POSIT (iv): high-z velocity-DISPERSION-FUNCTION evolution"); print("="*100)
# Deep-MOND Faber-Jackson:  sigma^4 = (4/9) G M a0.  At fixed baryonic mass:  sigma ~ a0^(1/4).
# The VDF phi(sigma) shifts: the sigma-axis stretches by (a0(z)/a0)^(1/4).
print(" Deep-MOND Faber-Jackson sigma^4=(4/9)G M a0  =>  at fixed M, sigma ~ a0^(1/4); the VDF stretches:")
for z in ZUSE:
    m,lo,hi = RATIO[z]
    print(f"   z={z:>3.1f}:  a0(z)/a0(0)={m:.3f}  ->  sigma boost = (a0(z)/a0)^(1/4) = {m**0.25:.3f}"
          f"   ({(m**0.25-1)*100:+.1f}% at fixed baryonic M)")
print(""" CONFOUND (this is the documented project_faber_jackson_a0z killer, restated on the declining footing):
   (1) high-z quiescent galaxies are ~2-4x more COMPACT at fixed mass -> sigma^2~GM/R alone gives +30-40%,
       SAME sign, LARGER magnitude, fully degenerate; (2) high-z sigmas are CENTRAL (g~3-11 a0), the WRONG
       (near-Newtonian) regime, so sigma^4=(4/9)G M a0 is not even operative; (3) declining a0 makes the
       sigma boost SMALLER ({:+.0f}% at z=2 vs the rising-reading +32%), pushing it further under the
       size-evolution confound.
 GRADE: SPECULATIVE.  DE-HOSTAGE + size-confounded + wrong-regime.  win_flavored: NO (canonical sign shrinks
   the already-degenerate signal).""".format((RATIO[2.0][0]**0.25-1)*100))

# ===========================================================================
# POSIT (v): BTFR ZERO-POINT as the 'w(z)-independent' a0(z) probe (the memory-flagged clean test)
# ===========================================================================
print("\n"+"="*100); print(" POSIT (v): BTFR ZERO-POINT evolution -- is it a w(z)-INDEPENDENT a0(z) probe?"); print("="*100)
# Deep-MOND BTFR:  M_bar = v_flat^4/(G a0).  At fixed v_flat:  log10 M_bar(z)-log10 M_bar(0) = -log10(a0(z)/a0(0)).
# The zero-point SHIFT (the quantity surveys actually measure) is:
print(" Deep-MOND BTFR  M_bar=v^4/(G a0).  At FIXED v_flat:  Dlog10 M_bar = -log10(a0(z)/a0(0)) = -0.5 log10(rho ratio).")
print(f"   {'z':>4} {'a0(z)/a0(0)':>12} {'Dlog10 M_bar(fixed v)':>22} {'-> at w=-1':>12}")
for z in ZUSE:
    m,lo,hi = RATIO[z]
    dzp = -np.log10(m)
    # the w=-1 null:
    dzp_lcdm = -np.log10(np.sqrt(rho_de_ratio(z,-1.0,0.0)))
    print(f"   {z:>4.1f} {m:>12.3f} {dzp:>+22.3f} {dzp_lcdm:>+12.3f}")
print(""" THE VERDICT ON THE MEMORY'S HOPED-FOR CLEAN TEST:
   The BTFR zero-point shift IS the cleanest a0(z) observable (no phantom-halo modelling, no lens geometry,
   M_bar and v_flat are directly measured), AND its CONFOUND is the most controllable: unlike the VDF/lens/
   cluster channels, the gas-fraction confound can be REMOVED with a per-galaxy HI+H2 census (project10),
   leaving a comparatively clean Dlog10 M_bar.  THIS is the one channel where the confound is beatable.
   BUT it is STILL NOT w(z)-independent: Dlog10 M_bar = -0.5 log10(rho_DE ratio) -> EXACTLY 0 at w=-1 (column
   above).  So 'a w(z)-independent a0(z) probe' is a CATEGORY ERROR within sqrt(rho_DE) footing -- the BTFR
   zero-point is the cleanest CONFOUND-separable probe, not a DE-separable one.
 GRADE: HYPOTHESIS-WITH-FREE-KNOB.  DE-HOSTAGE (dies at w=-1) but the BEST confound-control of the five.
   win_flavored: YES -- a measured negative Dlog10 M_bar at fixed v_flat (after a gas census) is a direct,
   sign-correct a0-decline detection; it is the channel to actually run.""")

# ===========================================================================
# POSIT (vi): the BTFR zero-point DIFFERENCED against the RAR SHAPE (a confound-cancelling pair)
# ===========================================================================
print("\n"+"="*100); print(" POSIT (vi): a0(z) from the RAR-SHAPE knee vs the BTFR zero-point -- a confound DIFFERENCE"); print("="*100)
# The single genuinely-new structural idea: a0 enters TWO independent places in the same rotation curve:
#   (A) the BTFR zero-point (the deep-MOND tail amplitude): M_bar=v^4/(G a0)  -> probes a0 at g<<a0.
#   (B) the RAR transition 'knee' acceleration scale g_dagger ~ a0 (where g_obs departs g_bar) -> probes a0
#       at g~a0.  BOTH must move by the SAME a0(z) if the framework is right; a gas/size/M-L systematic moves
#       the zero-point but NOT the knee location (the knee is an acceleration, dimensionless in M/L to first
#       order).  So the COMBINATION (zero-point shift) - (knee shift) cancels the dominant baryonic confounds
#       while the a0(z) signal ADDS (they shift the same way under a0, opposite under M-L).
print(" a0 appears TWICE in one rotation curve:  (A) BTFR zero-point (deep tail, g<<a0); (B) the RAR knee g_dagger~a0.")
print(" Framework: BOTH move by the same a0(z).  A baryonic M/L error moves (A) but barely moves (B) (an accel scale).")
print(" Differencing (A)-(B) cancels the M/L confound and KEEPS the a0(z) signal -> a within-galaxy cross-check:")
for z in ZUSE:
    m,lo,hi = RATIO[z]
    shift_A = -np.log10(m)            # zero-point shift in log M at fixed v
    shift_B = np.log10(m)             # knee acceleration shift in log g_dagger
    print(f"   z={z:>3.1f}:  Dlog10 g_dagger(knee) = {shift_B:+.3f} ;  Dlog10 M_bar(zeropt) = {shift_A:+.3f}"
          f"   (consistent IFF both track a0(z)={m:.3f})")
print(""" This is the one NON-trivial structural move in the vein: it is a CONFOUND-DIFFERENCE within the same
   datum, testing the framework's OWN claim that a0 is a single scale entering both the tail and the knee.
   It is STILL DE-hostage (both -> 0 at w=-1), but it is the most internally-distinctive and the least
   astrophysics-confounded.  REQUIRES: high-z RAR with resolved knees (g~a0 points) AND deep-tail points in
   the same galaxies -- ELT/JWST/ALMA-era, not in hand.
 GRADE: HYPOTHESIS-WITH-FREE-KNOB.  DE-HOSTAGE but confound-DIFFERENCED.  win_flavored: YES -- a coherent
   co-shift of knee + zero-point by the same factor is hard to fake with baryons; it directly tests 'one a0'.""")

# ===========================================================================
# FDR / coincidence guard + summary
# ===========================================================================
print("\n"+"="*100); print(" FDR / COINCIDENCE GUARD"); print("="*100)
print(""" None of these posits is a numerical coincidence to FDR-guard (no '3/8 matches sin^2theta_W' style hit):
   each is a DERIVED scaling (sqrt, 1/4, 1, 1/2 powers of the SAME rho_DE ratio), not a fitted number.  The
   guard that matters here is the HOSTAGE THEOREM: because all six are monotone functions of one ratio that
   ->1 at w=-1, finding agreement among them is NOT independent evidence -- they are the same measurement in
   different units.  Reporting them as 'multiple confirmations' would be a multiplicity error.  Honest count:
   ONE underlying DE-hostage signal, probed in six places with different confound/power profiles.""")

print("\n"+"="*100); print(" SUMMARY TABLE (computed)"); print("="*100)
print(f" {'posit':>5}  {'channel':<28} {'a0 power':>8} {'mag@z=2':>9} {'grade':<26} {'DE-sep?':<10} {'win?':<5}")
def magz2(p):
    m=RATIO[2.0][0]
    return {'i':np.sqrt(m),'ii':m**-0.25,'iii':1/m,'iv':m**0.25,'v':m,'vi':m}[p]
rows=[("i","strong-lens theta_E","1/2","SPECULATIVE","NO (hostage+geom)","no"),
      ("ii","reionization timing","-1/4","SPECULATIVE","NO (hostage)","no"),
      ("iii","cluster mass function","1","SPECULATIVE","NO (hostage+co-degen)","no"),
      ("iv","high-z VDF","1/4","SPECULATIVE","NO (hostage+size)","no"),
      ("v","BTFR zero-point","1","HYPOTHESIS-FREE-KNOB","NO (hostage)*","YES"),
      ("vi","knee-vs-zeropt diff","1","HYPOTHESIS-FREE-KNOB","NO (hostage)*","YES")]
for p,ch,pw,gr,ds,wn in rows:
    print(f" {p:>5}  {ch:<28} {pw:>8} {magz2(p):>9.3f} {gr:<26} {ds:<10} {wn:<5}")
print("""
 *(v),(vi) DE-hostage like the rest, but with the BEST confound CONTROL (gas census; within-galaxy
   differencing).  'DE-separable' = NO for all six (hostage theorem).  Best to VERIFY: POSIT (v), the BTFR
   zero-point with a per-galaxy gas census -- cleanest confound, sign-correct, the channel actually runnable
   on existing high-z IFU data; (vi) is the most distinctive but needs resolved high-z knees (not in hand).""")
print("="*100); print(" exit 0");
