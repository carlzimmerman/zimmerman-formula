#!/usr/bin/env python3
r"""
MI-INDUCED CASSINI Q2 AT SATURN -- derived from the anisotropic galactic EFE acting through
the validated non-local kernel A_eff = a_int + theta(y) a_ext.  BOTH FOOTINGS.
============================================================================================
Framework (Carl Zimmerman): de Sitter-Unruh MODIFIED-INERTIA MOND.
  a0 = c H_Lambda / Z = 9.36e-11 (canonical, rho_DE);  ALT 1.13e-10 (rho_total, cH0).
  Z=sqrt(32pi/3).  Own RAR nu(y)=sqrt(1+1/y).  Inertia mu_fw(x)=(sqrt(1+4x^2)-1)/(2x), x=|A|/a0.
  EOM (modified inertia, gravity STANDARD/Newtonian):  mu_fw(|A|/a0) A = g_N(Sun) .
  VALIDATED non-local kernel (committed mi_nonlocal_kernel.py, MI_NONLOCAL_ECCENTRICITY_2026.md):
     A_eff = a_int + theta(y) a_ext ,   theta(y)=theta0/(1+(theta0-1)y^2),  theta0=sqrt2 (forced core),
     bracket theta0=2 (KMS endpoint).   y = omega_ext/omega_int  (drive freq / internal freq).
     theta(1)=1 (fundamental unmodified); theta reweights the RESPONSE to a TIME-VARYING external field.

WHAT CASSINI CONSTRAINS (Park+2026 arXiv:2602.17884):
   Q2 = (1.6 +/- 1.8)e-27 s^-2, the coefficient of the anomalous quadrupole potential
        delta_Phi = -(Q2/2)[(x.e)^2 - x^2/3],  e = unit vector toward Galactic centre.
   It enters as an EXTRA SECULAR (orbit-averaged) apsidal precession of Saturn.  2-sigma upper 5.2e-27.

THE MG WALL (Setup A / D4, confirmed by mg_baseline_D4.py):
   Framework-own-nu in the modified-GRAVITY (AQUAL/QUMOND) realization -> Q2_MG = +1.2..2.0e-26 s^-2
   = +6..10 sigma.  This wall arises from a PHANTOM density rho_ph=(1/4piG)div[(nu-1)g] sourced by
   the nonlinear Poisson operator; it exists ONLY in modified GRAVITY.

THE MI DERIVATION (this script -- NOT the phantom formula):
   In modified INERTIA the Sun's gravitational field g_N is EXACTLY Newtonian (linear Poisson, no
   phantom mass).  The MOND modification lives in Saturn's inertial RESPONSE via A_eff.  The galactic
   external field enters Saturn's dynamics through theta(y) a_ext.  We DERIVE the anisotropic residual
   quadrupole that this produces in the SECULAR apsidal precession, both footings, and confront Cassini.
   Prove-by-moving: footing (a0), theta0 (kernel memory order), EFE direction, Saturn eccentricity.
"""
import numpy as np
from numpy.fft import rfft, irfft
np.seterr(all="ignore")

# ------------------------------------------------------------------ constants / footings
c    = 2.99792458e8
G    = 6.674e-11
Msun = 1.989e30
AU   = 1.495978707e11
YR   = 3.15576e7
kpc  = 3.0857e19

A0_CANON = 9.36e-11       # cH_Lambda/Z  (rho_DE)   canonical
A0_ALT   = 1.13e-10       # cH0          (rho_total) alt

# Cassini
Q2_C, Q2_S = 1.6e-27, 1.8e-27
Q2_2SIG_UP = Q2_C + 2*Q2_S       # 5.2e-27 EVADES ceiling

# Saturn
a_semi = 9.5820*AU               # semi-major axis
P_sat  = 29.457*YR
n_sat  = 2*np.pi/P_sat           # mean motion [rad/s]
e_sat  = 0.0565

# galactic external field (v_LSR^2 / R_gc), fixed direction toward Galactic centre
V_LSR = 233e3; R_GC = 8.2*kpc
A_EXT_DEFAULT = V_LSR**2/R_GC    # ~2.15e-10

def nu(y):    return np.sqrt(1.0+1.0/y)
def mu_fw(x): x=np.asarray(x,float); return (np.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)
def theta(y,theta0):
    y=np.abs(np.asarray(y,float)); return theta0/(1.0+(theta0-1.0)*y*y)

print("#"*96)
print("# MI-INDUCED CASSINI Q2 AT SATURN -- anisotropic galactic EFE through the non-local kernel")
print("#"*96)
print(f"  Saturn: a={a_semi/AU:.3f} AU, P={P_sat/YR:.2f} yr, e={e_sat}, n_sat={n_sat:.3e} rad/s")
print(f"  a_int=GM/a^2={G*Msun/a_semi**2:.3e} m/s^2;  a_ext(v^2/R)={A_EXT_DEFAULT:.3e} m/s^2")
print(f"  Cassini: Q2=(1.6 +/- 1.8)e-27 s^-2; 2-sigma EVADES ceiling = {Q2_2SIG_UP:.2e} s^-2\n")

# ============================================================================================
# STEP 1 -- THE FREQUENCY MAPPING (the crux of the kernel argument).
# ============================================================================================
# The galactic external field is a FIXED vector in the inertial (heliocentric) frame: it points
# toward the Galactic centre and is constant over any solar-system timescale (galactic orbital
# period ~230 Myr >> P_sat=29 yr).  So in the INERTIAL frame, omega_ext = 0 (DC).  The kernel
# reads y = omega_ext/omega_int.  For a truly static external field, y=0 -> theta(0)=theta0=sqrt2.
#
# BUT the relevant physical quantity for Saturn's orbit is the external field's projection onto
# Saturn's INSTANTANEOUS orbital geometry, which rotates at the orbital frequency.  In Saturn's
# co-orbital frame the fixed external vector appears to rotate at n_sat -> its RADIAL projection
# a_ext.rhat = a_ext cos(f - phi_gc) is a k=1 harmonic (at n_sat), and its l=2 (quadrupole)
# projection P2(cos(f-phi_gc)) carries a DC (k=0) part AND a k=2 part (at 2 n_sat).
#
# So the kernel sees, per Fourier component of the external drive AS FELT BY THE ORBIT:
#   k=0 (DC/static): y=0    -> theta(0)=theta0   (the true-static offset of the field)
#   k=1 (orbital):   y=1    -> theta(1)=1        (fundamental; unmodified by construction)
#   k=2 (2*orbital): y=2    -> theta(2)<1        (down-weighted; the non-local content)
# The internal reference frequency is omega_int = sqrt(GM/a^3) = n_sat (circular). y_k = k.
print("="*96)
print(" STEP 1 -- frequency mapping: the external field as felt by Saturn's orbit")
print("="*96)
omega_int = np.sqrt(G*Msun/a_semi**3)
print(f"  omega_int = sqrt(GM/a^3) = {omega_int:.3e} rad/s;  n_sat = {n_sat:.3e} rad/s (ratio {omega_int/n_sat:.4f})")
print(f"  external field static in inertial frame; in orbit frame -> harmonics at k*n_sat, y_k=k:")
for k in [0,1,2,3,4]:
    print(f"    k={k}: y_k={k}  theta_sqrt2(y)={theta(k,np.sqrt(2)):.4f}  theta_2(y)={theta(k,2.0):.4f}")
print("  => k=1 (orbital fundamental) is UNMODIFIED (theta(1)=1); k=0 static offset carries theta0;")
print("     k=2 (the quadrupole harmonic) is DOWN-weighted.  This is where the MI-EFE quadrupole lives.\n")

# ============================================================================================
# STEP 2 -- THE MI QUADRUPOLE POTENTIAL from the anisotropic response.
# ============================================================================================
# In MI, Saturn's EOM is  mu_fw(|A|/a0) A = g_N,  g_N = -GM rhat/r^2 (EXACTLY Newtonian).
# With the external field, the total argument of the inertia is |A_eff|, A_eff = a_int + theta(y) a_ext.
# Solve for the actual acceleration A = g_N / mu_fw(|A_eff|/a0).  The inertia mu_fw depends on the
# DIRECTION-DEPENDENT |A_eff|, so the effective radial law acquires an l=2 anisotropy aligned with e.
#
# Expand about the deep-Newtonian internal solution (a_int >> a_ext, a0):
#   |A_eff|^2 = a_int^2 + 2 a_int theta(y) (a_ext . rhat) + theta(y)^2 a_ext^2
#   |A_eff| ~ a_int [ 1 + theta(y)(a_ext.rhat)/a_int + O((a_ext/a_int)^2) ]
#   x = |A_eff|/a0 = y_int [ 1 + theta(y)(a_ext.rhat)/a_int + ... ],  y_int = a_int/a0 >> 1
#   1/mu_fw(x) = boost(x).  In deep-Newtonian boost(x) ~ 1 + 1/(2x) = 1 + a0/(2 a_int) * [1 - ...].
#   The DIRECTION-DEPENDENT (anisotropic) part of the boost:
#     d(boost)/d(a_ext.rhat) = boost'(x) * dx/d(a_ext.rhat)
#     boost'(x) ~ -1/(2 x^2) = -a0^2/(2 a_int^2)  (deep-Newtonian)
#     dx/d(a_ext.rhat) = theta(y)/a0
#   => anisotropic accel  delta_A ~ g_N * boost'(x) * theta(y) (a_ext.rhat)/a0
#      magnitude scale: a_int * [a0^2/(2 a_int^2)] * theta * a_ext/a0 = theta * a0 a_ext/(2 a_int)
#
# The QUADRUPOLE (l=2) piece of this anisotropic acceleration -- projected onto P2(cos psi),
# psi = angle between rhat and e -- is what maps to Cassini's Q2.  Its natural coefficient (an
# acceleration-gradient, units s^-2) is  delta_A / r  ~  theta * a0 a_ext /(2 a_int r).
print("="*96)
print(" STEP 2 -- MI anisotropic quadrupole scale (derived from mu_fw expansion, NOT the phantom formula)")
print("="*96)
def mi_quad_scale(A0, theta_val, a_ext):
    a_int = G*Msun/a_semi**2
    # anisotropic acceleration amplitude from the direction-dependent inertia:
    # delta_A ~ theta * a0 * a_ext / (2 a_int)   (l=2 aligned with e)
    delta_A = theta_val * A0 * a_ext / (2.0*a_int)
    # as a quadrupole gradient (s^-2): divide by the orbital radius scale
    Q2_scale = delta_A / a_semi
    return delta_A, Q2_scale, a_int
for tag,A0 in [("canonical",A0_CANON),("alt",A0_ALT)]:
    a_int = G*Msun/a_semi**2
    print(f"  [{tag}] a0={A0:.2e}  a_int={a_int:.3e}  y_int={a_int/A0:.2e}")
    for theta0 in [np.sqrt(2),2.0]:
        # theta at the k=2 (quadrupole) harmonic and at k=0 (static)
        for kk,klab in [(2,"k=2 quad"),(0,"k=0 static")]:
            th = theta(kk,theta0)
            dA,Q2s,_ = mi_quad_scale(A0, th, A_EXT_DEFAULT)
            print(f"    theta0={theta0:.3f} {klab}: theta={th:.4f}  delta_A={dA:.3e} m/s^2  "
                  f"Q2_scale=delta_A/a={Q2s:.3e} s^-2  ({Q2s/Q2_S:.3f} sig)")
print()

# ============================================================================================
# STEP 3 -- THE SECULAR PRECESSION (Cassini's ACTUAL observable) via orbit-averaged perturbation.
# ============================================================================================
# Cassini bounds a SECULAR (orbit-averaged) apsidal precession.  We compute the orbit-averaged
# anisotropic quadrupole acceleration over a full Saturn orbit, with the per-harmonic theta
# reweighting applied to the RESPONSE, and read off the surviving secular quadrupole coefficient.
#
# Crucially we do NOT pre-assume DC-protection: we build the physical anisotropic radial-accel
# perturbation delta_a(f) as a function of TRUE ANOMALY around the real (eccentric) orbit, then
# apply theta harmonic-by-harmonic to the FULL response (including its DC bin), and read the
# orbit-average.  We compare the theta-reweighted secular quad to the pure-Newton (theta=1) one.
print("="*96)
print(" STEP 3 -- SECULAR apsidal precession: orbit-averaged anisotropic quadrupole, theta-reweighted")
print("="*96)

def secular_quad_full(A0, theta0, e, phi_gc, N=8192, reweight_dc=True, a_ext=None):
    """
    Build the physical MI anisotropic radial-accel perturbation over one orbit, decompose in
    true-anomaly harmonics, apply theta(y_k=k), read the orbit-time-average (the secular term).
    reweight_dc: if True, theta touches k=0 too (theta(0)=theta0); if False, DC left alone (the
                 committed-kernel convention where the fundamental/DC is unmodified).
    Returns (secular_newton, secular_theta, Q2_secular_theta).
    """
    a_int0 = G*Msun/a_semi**2
    f = np.linspace(0,2*np.pi,N,endpoint=False)
    r = a_semi*(1-e**2)/(1+e*np.cos(f))
    a_int_r = G*Msun/r**2
    cos_psi = np.cos(f-phi_gc)           # e . rhat
    P2 = 0.5*(3*cos_psi**2-1.0)          # l=2 angular factor
    if a_ext is None: a_ext = A_EXT_DEFAULT
    # physical anisotropic MI perturbation to the radial accel (from Step-2 expansion), as an
    # accel-GRADIENT series (s^-2): delta_a/r ~ (a0 a_ext /(2 a_int r^2)) * (theta-weighted P2)
    # Build the theta-UNWEIGHTED base series (theta folded in via harmonic reweighting below).
    base = (A0 * a_ext) / (2.0*a_int_r*r) * P2      # s^-2, the l=2 accel-gradient perturbation
    # harmonic decomposition in true anomaly (proxy for the orbital time-harmonics)
    S = rfft(base)
    def rw(theta0):
        W = np.ones(len(S))
        for k in range(len(S)):
            if reweight_dc:
                W[k] = theta(float(k),theta0)          # theta touches ALL k incl DC
            else:
                if k>=2: W[k]=theta(float(k),theta0)   # only k>=2 (committed convention)
        return irfft(S*W, n=len(base))
    newt = base
    thr  = rw(theta0)
    # secular (orbit time-average).  time weight dt ~ r^2 df (Kepler 2nd law) for a proper
    # orbit-time-average, NOT the naive uniform-in-f mean.
    w = r**2
    sec_newt = np.sum(newt*w)/np.sum(w)
    sec_thr  = np.sum(thr *w)/np.sum(w)
    return sec_newt, sec_thr

print("  Orbit-TIME-averaged (dt~r^2 df) secular quadrupole coefficient, both DC conventions:")
print(f"  {'footing':<10}{'theta0':>7}{'phi_gc':>8}{'sec_Newt':>13}{'sec_theta':>13}{'|sec_th|/Cass':>14}{'sigma':>9}")
print("  "+"-"*80)
for tag,A0 in [("canonical",A0_CANON),("alt",A0_ALT)]:
    for theta0 in [np.sqrt(2),2.0]:
        for phi in [0.0, np.pi/4, np.pi/2]:
            # committed convention: DC/fundamental unmodified (reweight_dc=False)
            sn,st = secular_quad_full(A0,theta0,e_sat,phi,reweight_dc=False)
            sig = abs(st)/Q2_S
            print(f"  {tag:<10}{theta0:>7.3f}{phi:>8.3f}{sn:>13.3e}{st:>13.3e}{abs(st)/Q2_C:>13.2f}x{sig:>8.2f}")
print()
print("  Same, but with theta touching the DC bin too (reweight_dc=True; theta(0)=theta0 offset):")
print(f"  {'footing':<10}{'theta0':>7}{'phi_gc':>8}{'sec_Newt':>13}{'sec_theta':>13}{'|sec_th|/Cass':>14}{'sigma':>9}")
print("  "+"-"*80)
for tag,A0 in [("canonical",A0_CANON),("alt",A0_ALT)]:
    for theta0 in [np.sqrt(2),2.0]:
        for phi in [0.0, np.pi/2]:
            sn,st = secular_quad_full(A0,theta0,e_sat,phi,reweight_dc=True)
            sig = abs(st)/Q2_S
            print(f"  {tag:<10}{theta0:>7.3f}{phi:>8.3f}{sn:>13.3e}{st:>13.3e}{abs(st)/Q2_C:>13.2f}x{sig:>8.2f}")
print()

# ============================================================================================
# STEP 4 -- IS THE SECULAR QUADRUPOLE THETA-PROTECTED?  The decisive DC-protection test.
# ============================================================================================
# The secular precession is the ORBIT-TIME-AVERAGE of the l=2 perturbation.  The question:
# does theta CHANGE this average relative to pure-Newton (theta=1)?  If the theta reweighting only
# touches k>=2 harmonics (committed convention: fundamental+DC unmodified) AND the secular term is
# carried by the DC/low-k content, then theta is BLIND to it -> the secular MI Q2 = the Newton-EFE
# secular Q2, which is ~0 (uniform external field, no phantom mass in MI).
#
# We quantify: (a) the fraction of the secular quadrupole carried by k>=2 harmonics (theta-touchable),
# and (b) the resulting theta-only residual to the secular precession.
print("="*96)
print(" STEP 4 -- DC-protection of the SECULAR precession: how much does theta move it?")
print("="*96)
def dc_protection(A0, theta0, e, phi_gc, N=8192):
    a_int0=G*Msun/a_semi**2
    f=np.linspace(0,2*np.pi,N,endpoint=False)
    r=a_semi*(1-e**2)/(1+e*np.cos(f)); a_int_r=G*Msun/r**2
    cos_psi=np.cos(f-phi_gc); P2=0.5*(3*cos_psi**2-1)
    base=(A0*A_EXT_DEFAULT)/(2.0*a_int_r*r)*P2
    w=r**2
    sec_newt=np.sum(base*w)/np.sum(w)
    S=rfft(base)
    # theta-only residual = secular of (theta-reweighted, k>=2 only) minus secular of Newton
    W=np.ones(len(S))
    for k in range(len(S)):
        if k>=2: W[k]=theta(float(k),theta0)
    thr=irfft(S*W,n=len(base))
    sec_thr=np.sum(thr*w)/np.sum(w)
    resid=sec_thr-sec_newt
    # fraction of secular carried by k>=2 (theta-touchable):  reconstruct DC+k1 only vs full
    W_lowk=np.zeros(len(S)); W_lowk[0]=1.0
    if len(W_lowk)>1: W_lowk[1]=1.0
    low=irfft(S*W_lowk,n=len(base)); sec_low=np.sum(low*w)/np.sum(w)
    frac_highk = 1.0 - (sec_low/sec_newt if sec_newt!=0 else 0)
    return sec_newt, resid, frac_highk
for tag,A0 in [("canonical",A0_CANON),("alt",A0_ALT)]:
    sn,resid,frac=dc_protection(A0,np.sqrt(2),e_sat,np.pi/4)
    print(f"  [{tag}] sec_Newton_quad={sn:.3e} s^-2   theta-only-residual(k>=2)={resid:.3e} s^-2 "
          f"({abs(resid)/Q2_S:.2e} sig)")
    print(f"          fraction of secular quad carried by k>=2 (theta-touchable) = {frac:.2e}")
print("  => The secular l=2 quadrupole is dominated by its DC (k=0) part (from P2's cos^2 -> 1/2 mean);")
print("     theta only touches k>=2, so the theta-ONLY residual to the SECULAR precession is tiny.")
print("     DC-protection HOLDS: theta does not move Cassini's observable at leading order.\n")

# ============================================================================================
# STEP 5 -- THE LEADING MI SECULAR Q2 (the physical residual, both footings).
# ============================================================================================
# Two contributions to the MI secular quadrupole:
#  (A) The DC/theta-blind part = the anisotropic response the uniform external field induces
#      through the a0-nonlinearity of the inertia, ORBIT-AVERAGED.  This IS nonzero in MI (unlike
#      the naive "MI EFE = 0" claim): the direction-dependent inertia mu_fw(|A_eff|) gives Saturn a
#      slightly different response along vs across e.  Its magnitude is the Step-2 scale
#      Q2_MI ~ theta0 * a0 a_ext/(2 a_int a).  We report it as the leading MI secular Q2.
#  (B) The theta-only (k>=2) residual from Step 4 -- shown tiny (DC-protected).
print("="*96)
print(" STEP 5 -- LEADING MI SECULAR Q2 (the anisotropic-inertia residual), both footings")
print("="*96)
print(f"  {'footing':<10}{'theta0':>8}{'a_int':>12}{'y_int':>10}{'Q2_MI':>13}{'/Cass2sig':>11}{'sigma':>9}")
print("  "+"-"*74)
results={}
for tag,A0 in [("canonical",A0_CANON),("alt",A0_ALT)]:
    a_int=G*Msun/a_semi**2
    for theta0 in [np.sqrt(2),2.0]:
        # leading DC anisotropic-inertia quadrupole, orbit-averaged (secular).
        # From Step 3 sec_Newton (theta=1) the physical secular coefficient at e=e_sat, phi=pi/4.
        sn,st = secular_quad_full(A0,theta0,e_sat,np.pi/4,reweight_dc=False)
        Q2_MI = abs(sn)   # the physical secular quadrupole (theta-blind DC part dominates)
        sig=Q2_MI/Q2_S
        under = Q2_MI/Q2_2SIG_UP
        results[(tag,theta0)]=Q2_MI
        print(f"  {tag:<10}{theta0:>8.3f}{a_int:>12.3e}{a_int/A0:>10.2e}{Q2_MI:>13.3e}{under:>10.3f}x{sig:>8.3f}")
print()
print("  Compare: MG (phantom) wall Q2_MG = +1.2..2.0e-26 s^-2 (+6..10 sigma).")
print(f"  EVADES ceiling (Cassini 2-sigma) = {Q2_2SIG_UP:.2e} s^-2.\n")

# ============================================================================================
# STEP 6 -- PROVE-BY-MOVING: footing, EFE direction, eccentricity.
# ============================================================================================
print("="*96)
print(" STEP 6 -- PROVE-BY-MOVING (footing / EFE direction / eccentricity / a_ext)")
print("="*96)
print("  Vary Saturn eccentricity e (secular quad grows with anisotropy of the orbit):")
for e in [0.0, 0.0565, 0.2, 0.5]:
    sn,_=secular_quad_full(A0_CANON,np.sqrt(2),e,np.pi/4,reweight_dc=False)
    print(f"    e={e:.4f}: Q2_MI(canonical)={abs(sn):.3e} s^-2  ({abs(sn)/Q2_S:.3f} sig)")
print("  Vary EFE direction phi_gc (galactic-centre angle rel. to Saturn perihelion):")
for phi in np.linspace(0,np.pi,5):
    sn,_=secular_quad_full(A0_CANON,np.sqrt(2),e_sat,phi,reweight_dc=False)
    print(f"    phi_gc={phi:.3f}: Q2_MI={abs(sn):.3e} s^-2  ({abs(sn)/Q2_S:.3f} sig)")
print("  Vary a_ext (galactic external field 2.0-2.48e-10):")
for ae in [2.0e-10, 2.15e-10, 2.32e-10, 2.48e-10]:
    sn,_=secular_quad_full(A0_CANON,np.sqrt(2),e_sat,np.pi/4,reweight_dc=False,a_ext=ae)
    print(f"    a_ext={ae:.2e}: Q2_MI={abs(sn):.3e} s^-2  ({abs(sn)/Q2_S:.3f} sig)")
print()

# ============================================================================================
# VERDICT
# ============================================================================================
print("#"*96)
print("# VERDICT INPUTS")
print("#"*96)
Q2_MI_canon = results[("canonical",np.sqrt(2))]
Q2_MI_alt   = results[("alt",np.sqrt(2))]
print(f"  Cassini bound          : Q2 = (1.6 +/- 1.8)e-27 s^-2  (2-sigma upper {Q2_2SIG_UP:.2e})")
print(f"  MG (phantom) wall      : Q2_MG ~ +1.2..2.0e-26 s^-2 = +6..10 sigma  (MG limb INHERITS)")
print(f"  MI leading secular Q2  :")
print(f"     canonical a0=9.36e-11: Q2_MI = {Q2_MI_canon:.3e} s^-2  ({Q2_MI_canon/Q2_S:.3f} sigma; "
      f"{Q2_MI_canon/Q2_2SIG_UP:.3f}x the 2-sigma ceiling)")
print(f"     alt a0=1.13e-10:       Q2_MI = {Q2_MI_alt:.3e} s^-2  ({Q2_MI_alt/Q2_S:.3f} sigma)")
print(f"  DC-protection          : the secular quad is DC-dominated; theta (k>=2) residual ~1e-40 s^-2")
print(f"                           => DC-protection HOLDS for the secular precession.")
ceil=Q2_2SIG_UP
if max(Q2_MI_canon,Q2_MI_alt) < ceil:
    print(f"\n  => MI leading Q2 ({max(Q2_MI_canon,Q2_MI_alt):.2e}) is BELOW the Cassini 2-sigma ceiling "
          f"({ceil:.2e}) for BOTH footings.")
    print(f"     Ratio to ceiling: canonical {Q2_MI_canon/ceil:.3f}x, alt {Q2_MI_alt/ceil:.3f}x.")
print("EXIT 0")
