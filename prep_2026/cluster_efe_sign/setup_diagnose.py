#!/usr/bin/env python3
r"""
setup_diagnose.py -- CLUSTER-MEMBER EFE sigma-SPREAD SIGN: DIVERGENCE DIAGNOSIS + TIMESCALE PIN
================================================================================================
prep_2026/cluster_efe_sign/ , 2026-07-17.  Exit 0.  numpy/sympy.  BOTH footings.
Frozen repo READ-ONLY; this file re-implements the small kernel functions.

THE JOB (setup/diagnosis lane).  Two banked calcs CONTRADICT on the sign of the cluster-member
infall-phase relational sigma-spread:
  * GAP_STATEMENT.md E4/E7 (prep_2026/sigma_spread/): sign NEGATIVE -- "plungers less boosted",
    first-infall DEFICIT (cooler). E7 kill-condition: a significantly POSITIVE sign falsifies.
  * predict.py (prep_2026/cluster_efe_channel/): baseline POSITIVE -- "plungers HOTTER"; PLUS a
    dated pericentre SIGN-FLIP (pre-peri DEFICIT / post-peri EXCESS), tau_M ~ 0.45 Gyr.
  * D3 (reviews/residual_doors_2026_07/D3_amplitude_vs_settledness.py) pre-registers the SAME
    pericentre flip (post-peri EXCESS(+), first-infall/pre-peri DEFICIT(-)), tau_mem~0.45 Gyr.
The D3 sign-flip pre-registration (DOI 10.5281/zenodo.21179352) is HOSTAGE to this sign.

FRAMEWORK (de Sitter-Unruh MODIFIED INERTIA; NEVER McGaugh nu):
  g_obs = nu(y) g_bar,  nu(y)=sqrt(1+1/y),  y=g_bar/a0,  a0 = c H_Lambda / Z,  Z=sqrt(32pi/3).
  mu_fw(x)=(sqrt(1+4x^2)-1)/(2x) is the exact inverse.  MI = the inertial response is a time-
  NONLOCAL functional of the worldline 4-acceleration through the covariant kernel K(Box_u/a0^2)
  with memory time tau_mem = 2c/a0 = 2Z/H_Lambda (equation-book E10, EXACT, footing-free).
  a0 VALUE and sign s=-1 are POSTULATES; MG=0 (at fixed true field) is the sole theorem.
  Milgrom 1983/1999 (PLA 253:273) wellhead credit for the nu-kernel; Milgrom 2022 (PRD 106
  064060) for the two-frequency EFE subsystem-boost theta(y), y=omega_ex/omega_in.

WHAT THIS SCRIPT DELIVERS:
  (1) Reproduce BOTH signs and locate EXACTLY where they diverge.
  (2) SEPARATE the shared instantaneous theta(y_cur) EFE boost from the MG-impossible HISTORY
      spread at fixed y_cur.
  (3) PIN which memory timescale governs the history-spread SIGN: the 203 Gyr horizon tau_mem
      (=> deep-adiabatic frozen) or the internal response/crossing time (~Gyr, => transient).
  All both footings.  No 'proves'.  Honest both ways: the point is to RECONCILE, not to
  manufacture a clean win.
"""
import math
import numpy as np
import sympy as sp

np.seterr(all="ignore")

# ================================================================ constants / footings
c   = 2.99792458e8
Mpc = 3.0856775814913673e22
kpc = Mpc/1e3
yr  = 3.1557e7
Gyr = 1e9*yr
G   = 6.674e-11
MSUN= 1.989e30
H0  = 67.4e3/Mpc
OmL = 0.685
HL  = H0*math.sqrt(OmL)
Z   = math.sqrt(32*math.pi/3.0)                    # 5.789...
A0_CAN = c*HL/Z                                    # canonical cH_Lambda/Z
A0_ALT = c*H0/Z                                    # alt cH0/Z
assert abs(A0_CAN-9.36e-11) < 1e-13 and abs(A0_ALT-1.13e-10) < 1e-12
FOOTINGS = [("CANONICAL a0=9.36e-11 (cH_Lambda/Z)", A0_CAN),
            ("ALTERNATE a0=1.13e-10 (cH0/Z)",       A0_ALT)]

# ---------------------------------------------------------------- framework kernel (exact)
def mu_fw(x):
    x = np.asarray(x, float);  return (np.sqrt(1.0 + 4.0*x*x) - 1.0)/(2.0*x)
def boost(A, a0):
    """internal MOND boost B=(sigma/sigma_baryon)^2 = 1/mu_fw(A/a0). EFE SUPPRESSES it:
       larger loaded field A -> mu->1 -> boost->1 (Newtonian) -> cooler."""
    return 1.0/mu_fw(A/a0)
def sigma_ratio(A, a0):
    return math.sqrt(boost(A, a0))

# Milgrom-2022 two-frequency loading theta(y), y=omega_ex/omega_in (DECREASING; kernel-hostage)
theta_rat = lambda y: 2.0/(1.0 + y*y)                          # theta(0)=2   (fiducial)
theta_e1  = lambda y: math.exp(1.0 - abs(y))                   # theta(0)=e   (ceiling)
theta_s2  = lambda y: math.sqrt(2.0)/(1.0 + (math.sqrt(2.0)-1.0)*y*y)   # theta(0)=v2 (floor)
KERNELS = [("theta0=2 rational", theta_rat), ("theta0=e exp", theta_e1), ("theta0=v2 pilot", theta_s2)]

print("="*100)
print(" setup_diagnose.py -- CLUSTER-MEMBER EFE sigma-SPREAD: SIGN DIVERGENCE + TIMESCALE PIN")
print("="*100)
print(f"  Z={Z:.4f}  H_Lambda={HL:.3e} 1/s   a0_can={A0_CAN:.3e}  a0_alt={A0_ALT:.3e}")

# =====================================================================================
print("\n" + "="*100)
print(" (1) REPRODUCE BOTH SIGNS -- and locate EXACTLY where they diverge")
print("="*100)

# ---- 1a: the GAP / rederive_spread_and_power path (the source GAP E4/E7 cites) ----
print("\n [1a] GAP path -- boost across the infall-phase window y (fixed a_ex, fixed a_in):")
print("      A(y) = a_in + a_ex*theta(y);  boost=1/mu_fw(A/a0);  sigma_ratio=sqrt(boost).")
for flabel, a0 in FOOTINGS[:1]:
    a_in, a_ex = 0.3*a0, 2.0*a0
    print(f"      [{flabel}]  a_in=0.3a0, a_ex=2.0a0, theta0=2:")
    ys = [0.05, 0.5, 1.0, 1.5]
    srs = []
    for y in ys:
        A = a_in + a_ex*theta_rat(y);  sr = sigma_ratio(A, a0);  srs.append(sr)
        print(f"        y={y:4.2f} (settled->plunger)  theta={theta_rat(y):.3f}  A/a0={A/a0:.2f}  "
              f"sigma_ratio={sr:.4f}")
    assert srs[-1] > srs[0], "code must give plunger (high y) HOTTER"
    print(f"      => sigma_ratio RISES {srs[0]:.4f} (y=0.05 settled) -> {srs[-1]:.4f} (y=1.5 plunger):")
    print(f"         the CODE says PLUNGERS ARE HOTTER (POSITIVE).  GAP E4/E7's text 'plungers less")
    print(f"         boosted' + 'prediction NEGATIVE' CONTRADICTS the very script it cites")
    print(f"         (rederive_spread_and_power.py). ==> GAP negative sign = a TEXT-LABEL BUG.")

# ---- 1b: the predict.py path -- baseline AND the felt_excess sign-flip ----
print("\n [1b] predict.py path -- felt y_eff = y_cur + (y_hist - y_cur)*w, w=exp(-t/tau_M):")
TAU_M = 0.45*Gyr
def felt_excess_predict(y_cur, y_hist, t_since, a0, a_in=0.3, a_ex=1.0, theta=theta_rat):
    w   = math.exp(-t_since/TAU_M)
    yef = y_cur + (y_hist - y_cur)*w
    A_now = (a_in + a_ex*theta(yef ))*a0
    A_set = (a_in + a_ex*theta(y_cur))*a0
    return sigma_ratio(A_now, a0)/sigma_ratio(A_set, a0) - 1.0, yef, w
a0 = A0_CAN
exc_post, yef_post, w_post = felt_excess_predict(0.60, 1.50, 0.50*Gyr, a0)   # post-peri
exc_pre,  yef_pre,  w_pre  = felt_excess_predict(0.90, 0.10, 0.30*Gyr, a0)   # first-infall
print(f"      POST-peri (y_cur=0.60,y_hist=1.50): y_eff={yef_post:.2f} -> {exc_post*100:+.1f}% EXCESS")
print(f"      PRE-peri  (y_cur=0.90,y_hist=0.10): y_eff={yef_pre:.2f} -> {exc_pre*100:+.1f}% DEFICIT")
assert exc_post > 0 and exc_pre < 0, "predict.py sign-flip must reproduce"
print("      => predict.py's flip REPRODUCES: post-peri EXCESS, first-infall DEFICIT.")

print("""
 [DIVERGENCE LOCATED -- it is NOT a numeric disagreement; it is two labelling errors and a
  timescale import, on top of one internally-correct baseline]:
   (A) GAP E4/E7 'NEGATIVE (plungers less boosted)' contradicts its OWN cited script's output
       (1a: plungers HOTTER). It conflates 'plunger has LOW theta' with 'plunger has LOW boost'
       -- but in EFE physics LOW theta = LESS external loading = LESS suppression = MORE boost.
       So GAP's sign is inverted at the text level. E7's kill-condition ('positive sign
       falsifies') is therefore BACKWARDS: it would flag the framework's OWN correct baseline
       (plunger/first-infall hotter) as a falsification -- a self-trip.
   (B) predict.py's BASELINE ('plungers HOTTER') is CORRECT and matches 1a.
   (C) predict.py's & D3's pericentre SIGN-FLIP (first-infall DEFICIT) rests on encoding the
       'cold isolated past' as y_hist~0.1 (LOW y).  But theta(y~0)~2 is MAXIMAL loading, so
       'low-y past' = memory of the cluster field applied ADIABATICALLY (theta=2), NOT memory
       of isolation (a_ex=0).  Isolation is a_ex->0 => loading a_ex*theta -> 0 for ANY theta.
       Feeding a FIXED nonzero a_ex while sending y_hist->0 injects MAX past loading and flips
       the sign to a spurious deficit.  See (3) for the field-space correction.""")

# =====================================================================================
print("="*100)
print(" (2) SEPARATE: shared instantaneous theta(y_cur) boost  vs  MG-impossible HISTORY spread")
print("="*100)
print("""  DECOMPOSITION of a member's felt loaded field:
     A_felt(t) = a_in  +  [ memory-weighted external loading L(t) ]
   INSTANTANEOUS piece: if the member equilibrates to the CURRENT field, L = a_ex*theta(y_cur).
     -> spread ACROSS y_cur = the banked 6-13%.  SIGN: higher y_cur (less loading) = HOTTER.
     This piece is 'partly shared': it is the current-configuration EFE; an MG modeler who is
     handed y_cur (a position/velocity label) can attempt to fit its correlation with the field.
   HISTORY piece (the CLEAN MG-impossible one): at FIXED current field AND FIXED y_cur, two
     members with DIFFERENT past L-history carry DIFFERENT A_felt ONLY in MI (memory kernel).
     MG's L is a function of the CURRENT position only -> identical for the two members -> 0.""")

# MG=0 for BOTH sub-channels (symbolic, arbitrary interpolation)
a_in_s, a_ex_s, a0_s, y_s, th0_s = sp.symbols("a_in a_ex a0 y theta0", positive=True)
mu_s = sp.Function("mu")
# (i) y-channel: MG boost at matched momentary a_ex depends on (a_in+a_ex)/a0 only, no y:
sig_MG_y = sp.sqrt(1/mu_s((a_in_s + a_ex_s)/a0_s))
assert sp.diff(sig_MG_y, y_s) == 0
# (ii) history-channel: MG felt field = current field (no memory variable); d/d(history)=0:
hist = sp.symbols("history", positive=True)
sig_MG_h = sp.sqrt(1/mu_s((a_in_s + a_ex_s)/a0_s))   # no 'hist' appears
assert sp.diff(sig_MG_h, hist) == 0
print("  [OK] MG = EXACTLY 0 for BOTH sub-channels (d/dy = 0 AND d/d(history) = 0), symbolic,")
print("       any interpolation, any a0.  MG=0 at fixed true field is the SOLE theorem-grade claim")
print("       and is UNTOUCHED by the sign confusion.  (Milgrom 2022 Eq.35: constant theta0 is an")
print("       MG-absorbable EFE; only the y-DEPENDENCE / the history-memory is MG-impossible.)")

# instantaneous spread magnitude, both footings (reproduce the banked band)
print("\n  Instantaneous theta(y_cur) spread (the 'shared/current' piece), BOTH footings:")
def inst_spread(a_in, a_ex, theta, a0, ymax=1.5, n=40):
    ys = np.linspace(0.0, ymax, n)
    R = np.array([sigma_ratio(a_in + a_ex*theta(y), a0) for y in ys])
    return (R.max()-R.min())/R.mean()
for flabel, a0 in FOOTINGS:
    band = [inst_spread(0.3*a0, 2.0*a0, th, a0) for _, th in KERNELS]
    print(f"    [{flabel[:24]:24s}]  theta-band = {min(band)*100:.1f}% .. {max(band)*100:.1f}%  "
          f"(fiducial theta0=2: {inst_spread(0.3*a0,2.0*a0,theta_rat,a0)*100:.1f}%)")
print("  => banked 6-13% REPRODUCES as the INSTANTANEOUS piece.  SIGN of this piece: at fixed a_ex,")
print("     the higher-y_cur / less-loaded member is HOTTER (POSITIVE) -- matches 1a, predict baseline.")

# =====================================================================================
print("="*100)
print(" (3) THE HISTORY SPREAD DONE IN FIELD-SPACE (a_ex), not in y -- fixes the flip sign")
print("="*100)
print("""  Encode history by the felt EXTERNAL FIELD (the physical quantity), not by y.  The EFE
  suppresses the boost, so a member that has felt LESS net external loading is HOTTER.
     first-infall (field RISING toward peri; memory of the LOWER/isolated outside): felt < now
     backsplash / post-peri (field FALLING from peak; memory of the HIGHER pericentre):  felt > now""")
for flabel, a0 in FOOTINGS:
    a_in, a_ex = 0.3*a0, 1.0*a0
    A_set = a_in + 1.0*a_ex           # settled twin: felt = current
    A_fi  = a_in + 0.4*a_ex           # first-infall: felt < current (rising, lag)
    A_bs  = a_in + 1.6*a_ex           # backsplash:   felt > current (falling, lag)
    r_set, r_fi, r_bs = sigma_ratio(A_set,a0), sigma_ratio(A_fi,a0), sigma_ratio(A_bs,a0)
    print(f"  [{flabel[:24]:24s}]  settled={r_set:.4f}  first-infall={r_fi:.4f} ({(r_fi/r_set-1)*100:+.1f}%)"
          f"  backsplash={r_bs:.4f} ({(r_bs/r_set-1)*100:+.1f}%)")
    assert r_fi > r_set > r_bs, "field-lag: first-infall HOTTER, backsplash COOLER"
print("""  => FIELD-LAG PHYSICS: first-infall EXCESS (hotter), backsplash/post-peri DEFICIT (cooler).
     This is the EXACT INVERSE of predict.py / D3 (which claim first-infall DEFICIT, post-peri
     EXCESS).  The predict/D3 flip is backwards because 'isolated past' was encoded as y_hist~0
     (= theta~2 = MAX loading) instead of a_ex~0 (= ZERO loading).  With the physical encoding
     the leading contrast is UNAMBIGUOUS: the less-net-loaded (more recently-disturbed / first-
     infall / higher-y_cur) member is HOTTER.  Same sign as the instantaneous piece (2).""")

# =====================================================================================
print("="*100)
print(" (4) PIN THE MEMORY TIMESCALE that governs the history-spread SIGN")
print("="*100)
print("  Two candidate memories are in the corpus -- they DISAGREE by ~450x:")
for flabel, a0 in FOOTINGS:
    tau_horizon = 2.0*c/a0
    print(f"    [{flabel[:24]:24s}]  E10 kernel memory tau_mem = 2c/a0 = 2Z/H_Lambda = "
          f"{tau_horizon/Gyr:6.1f} Gyr  (tau*H_Lambda=2Z={2*Z:.2f}, footing-free)")
print(f"    dwarf-v3 phenomenological Lorentzian (D3/predict.py):   tau_M ~ 0.45 Gyr "
      f"(NOT anchored to E10)")
# cluster infall/crossing times
print("\n  Cluster infall / crossing times (the competing dynamical clock):")
for Mcl in (1e14, 5e14, 1e15):
    R = math.sqrt(G*Mcl*MSUN/A0_CAN)          # radius where a_ex=a0
    sig_cl = math.sqrt(0.5*G*Mcl*MSUN/R)
    Tcross = 2*R/sig_cl
    print(f"    M_cl={Mcl:.0e}: shell R(a_ex=a0)={R/Mpc:.2f} Mpc, sigma_cl~{sig_cl/1e3:.0f} km/s, "
          f"T_cross~{Tcross/Gyr:.1f} Gyr  ->  tau_mem(E10)/T_cross ~ {2*c/A0_CAN/Tcross:.0f}x")
print("""
  REASONING FROM THE FRAMEWORK'S OWN KERNEL (Carl's rule: framework-first):
   * The framework's COMMITTED memory is tau_mem = 2c/a0 = 203 Gyr (can) / 168 Gyr (alt),
     equation-book E10, footing-free, and the object the 19/19-verified MI orbit integrator
     (prep_2026/mi_integrator/) and mi_spread.py (prep_2026/sigma_spread/) actually integrate.
   * 203 Gyr >> every cluster infall/crossing time (~1-2 Gyr) by ~100-200x => the cluster-member
     inertia is DEEP in the ADIABATIC regime: its felt external loading is the ~203-Gyr-average
     of a_ex, which for ANY cluster member (in-cluster <~10 Gyr, most 1-5 Gyr) is DOMINATED by
     the pre-infall isolated history where a_ex~0.  So the felt loading is small for EVERYONE and
     the residual spread is set by RESIDENCE-TIME differences, NOT by a sub-orbit pericentre
     transient.  There is NO sharp pericentre sign-FLIP in this regime.
   * predict.py / D3's tau_M ~ 0.45 Gyr is a DIFFERENT (dwarf-v3 Lorentzian) number, NOT the
     E10 covariant-kernel memory.  It is the ONLY thing that makes the pericentre flip a sub-
     orbit resolvable transient; drop it in favour of the committed E10 memory and the flip
     freezes out.  mi_spread.py already made exactly this correction for the star-orbit observable
     (banked 6-13% -> sub-percent), for the same reason (tau_mem >> tau_orbit).""")

# residence-time (deep-adiabatic frozen) picture -- explicit, both footings
print("  DEEP-ADIABATIC (E10, 203 Gyr) residence-time model of the history spread:")
def frozen_excess(t_res, a0, a_ex_over_a0=1.0, a_in_over_a0=0.3, tau=None):
    """felt loading ~ a_ex * (t_res/tau) for a member resident t_res in the cluster field
       (203-Gyr memory barely loads it). sigma vs a hypothetical fully-loaded settled twin."""
    tau = tau or 2.0*c/a0
    frac = min(t_res*Gyr/tau, 1.0)
    A_res = (a_in_over_a0 + a_ex_over_a0*frac)*a0
    A_full= (a_in_over_a0 + a_ex_over_a0*1.0 )*a0
    return sigma_ratio(A_res, a0)/sigma_ratio(A_full, a0) - 1.0
for flabel, a0 in FOOTINGS:
    e1 = frozen_excess(1.0, a0);  e5 = frozen_excess(5.0, a0)
    print(f"    [{flabel[:24]:24s}]  t_res=1Gyr: {e1*100:+.1f}%   t_res=5Gyr: {e5*100:+.1f}%  "
          f"(recent-infall HOTTER; spread across residence ~{abs(e1-e5)*100:.1f}%, no sharp flip)")
print("""  => FROZEN picture: leading sign = recent-infall / first-infall HOTTER (POSITIVE), SAME as
     (2) and (3); magnitude is FEW-percent (residence-time-limited), an order below the 6-13%
     instantaneous band; and the pericentre sign-FLIP is ABSENT.
  HONEST CAVEAT (do not overclaim the freeze): E13 places real orbital frequencies on the |K|=1
     pure-phase branch (unit gain, phase lag), so fast one-time ramps are felt with gain ~1 and a
     phase DELAY -- a genuine felt!=current transient of order the group delay, not a hard freeze.
     Pinning that delay needs the explicit K(Box_u) group-delay (a follow-on compute).  Either way
     the SIGN is the same (less-net-loaded = hotter); only the MAGNITUDE and whether a resolvable
     transient survives are timescale-hostage.""")

# =====================================================================================
print("="*100)
print(" VERDICT (honest, both ways)")
print("="*100)
print("""  * DIVERGENCE = two labelling errors + one imported timescale, not a numeric clash:
      - GAP E4/E7 'NEGATIVE / plungers less boosted' contradicts its OWN cited script (plungers
        HOTTER); a text-label bug. E7's kill-condition is inverted -> would self-trip on the
        framework's own correct prediction. THE BANKED CALC THAT WAS RIGHT ON SIGN = predict.py's
        BASELINE and rederive_mi_spread.py's synthesis (plungers/first-infall HOTTER, POSITIVE).
      - predict.py / D3 pericentre SIGN-FLIP (first-infall DEFICIT) is backwards (isolated-past
        mis-encoded as low-y=max-loading) AND rests on tau_M~0.45 Gyr, not the E10 memory.
  * SEPARATION: instantaneous theta(y_cur) piece = the 6-13% band, sign 'higher-y_cur hotter',
    partly shared/current-configuration.  MG-impossible piece = history at fixed y_cur; MG=0 for
    it symbolically (the sole theorem).
  * TIMESCALE PIN: the framework's COMMITTED memory is tau_mem = 2c/a0 = 203/168 Gyr (E10),
    >> cluster crossing time -> DEEP ADIABATIC.  The history spread is FROZEN/residence-limited
    (few %, no sharp pericentre flip), not the 0.45-Gyr sub-orbit transient predict/D3 assumed.
  * OUTCOME (C)-leaning-(B): the PERICENTRE SIGN-FLIP is NOT pre-registerable (backwards +
    timescale-hostage).  PRE-REGISTERABLE: (i) EXISTENCE of a fixed-radius history spread (MG=0,
    theorem-grade); (ii) the LEADING sign that a LESS-net-loaded / first-infall / higher-y_cur
    member is HOTTER than a matched long-resident member at the same radius -- which INVERTS
    GAP E4's negative label and the D3 pre-peri-deficit.  Magnitude is timescale-hostage
    (few % frozen .. ~10% instantaneous). a0 value + s=-1 are POSTULATES; the sign tracks s=-1.
    No 'proves'.""")
print("\nEXIT 0: both signs reproduced, divergence located, separation done, timescale pinned. Both footings.")
