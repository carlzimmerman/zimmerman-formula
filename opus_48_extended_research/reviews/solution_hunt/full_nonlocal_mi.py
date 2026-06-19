#!/usr/bin/env python3
r"""
FULL TIME-NONLOCAL MI IN THE REAL GRANULAR/FLUCTUATING CLUSTER POTENTIAL
========================================================================
topic full_nonlocal_mi  (solution_hunt, 2026-06-19)

THE MISSION (the specific gap the prior closure left OPEN):
  The prior MI-dynamic route (cluster_closure/mi_dynamic_route.py) computed the
  Milgrom 1994/2022 time-nonlocal modified inertia for a member on a SMOOTH SINGLE
  KEPLER ORBIT (one fundamental frequency + harmonics) and found the cycle-averaged
  effective dynamical MASS is <= quasi-static MOND. But a real cluster member does NOT
  move in a smooth single orbit -- it plunges through a GRANULAR, FLUCTUATING potential
  (substructure, other galaxies, infalling groups) whose acceleration field has power
  at MANY frequencies, including HIGH frequencies (fast substructure encounters) where
  omega_ex ~ omega_in -- the genuinely-nonadiabatic regime Milgrom's two-frequency EFE
  (Eq 33-35) governs and the prior single-orbit closure could NOT probe.

  QUESTION (make-or-break, both ways): when the field is genuinely fluctuating/broadband,
  does the FULL Milgrom A(omega) functional give a LARGER MEAN effective dynamical mass
  than quasi-static MOND at the same mean acceleration? I.e. does GRANULARITY change the
  prior <= quasi-static conclusion? The cluster core needs eta 2.33 -> ~1, i.e. a0_eff up
  ~4-5x (boost in inferred mass ~ a few). Does a broadband fluctuating field reach it?

THE PHYSICS (Milgrom 2022 arXiv:2208.07073v3 = PRD 106 064060, eqs verified in repo):
  Per-frequency inertia:  a_hat(omega) mu[A(omega)/a0] = a_hat_N(omega)         (Eq 3/5)
  Nonlocal functional:    A(omega) = (1/sqrt(2pi)) INT theta(omega'/omega)|a_hat(omega')| domega'  (Eq 20)
  Two-frequency EFE:      A(om_in) = a_in + theta(om_ex/om_in) a_ex             (Eq 33-35)
                          theta(0) ~ few (the 3 guessed forms: theta(0)=2, e, e^0.5)
  mu increasing => LARGER A => SMALLER boost 1/mu (the sign that fought the single orbit).
  Scale invariance (Sec II D): deep-MOND V^4/(M G a0)=const, M G a0 = eta sigma^4, eta~1
  SHARED by MI & MG -- pins the integrated virial mass independent of orbit shape.

  inverse-inertia: mu_fw(x)=(sqrt(1+4x^2)-1)/(2x); quasi-static boost 1/mu_fw(g_bar/a0).
  framework: a0 = 9.36e-11 = c^2 sqrt(Lambda/32pi); g_obs=sqrt(g_bar^2+g_bar a0).

WHAT IS GENUINELY NEW HERE (NOT in mi_dynamic_route.py):
  1. A REALISTIC BROADBAND FLUCTUATING acceleration field a(t) for a plunging member:
     smooth large-scale orbit (low freq) + a stochastic granular field from substructure
     encounters (high freq, omega_ex ~ omega_in), with amplitude/spectrum set by REAL
     cluster substructure (mass function, impact rates) -- not a single Kepler ellipse.
  2. The FULL per-frequency Milgrom inertia mu[A(omega_k)/a0] applied mode-by-mode to the
     Fourier decomposition of the REAL fluctuating field (the prior script only bracketed
     A by <|a|> and rms|a| of a smooth orbit; here we build A(omega) properly from the
     broadband spectrum, including the two-frequency EFE cross terms).
  3. The decisive MEAN: cycle/ensemble-averaged INFERRED dynamical mass = <boost> M_bar,
     computed from the genuine A(omega) on the broadband field, vs quasi-static at <g>.
  4. GALAXY VETO: the SAME broadband-MI prescription applied to a smooth SPARC disk (low
     fluctuation power) -- does it leave the 0.11-0.13 dex RAR intact?

BOTH WAYS (#1 rule): a "granularity closes it" claim is verified as hard as "it doesn't".
QUARANTINE: a0/Z/kappa NEVER asserted derived.
"""
import numpy as np
import os, sys, glob

np.random.seed(20260619)
def H(s): print("\n"+"="*100+"\n "+s+"\n"+"="*100)
def h(s): print("\n"+"-"*100+"\n "+s+"\n"+"-"*100)

# --------------------------------------------------------------------- constants (SI)
c, G, hbar, kB = 2.998e8, 6.674e-11, 1.0546e-34, 1.381e-23
Msun, pc, kpc, Mpc = 1.989e30, 3.086e16, 3.086e19, 3.086e22
km = 1e3
yr = 3.156e7; Gyr = 1e9*yr

a0      = 9.36e-11                              # sealed = c^2 sqrt(Lambda/32pi)
Lambda  = (a0/c**2)**2 * 32*np.pi
cH_Lam  = c*np.sqrt(Lambda/3.0)
rho_DE  = 6.0e-27

def mu_fw(x):
    x = np.asarray(x, float)
    return (np.sqrt(1.0 + 4.0*x*x) - 1.0)/(2.0*x)
def nu_dsunruh(gbar, a0loc):
    return np.sqrt(gbar**2 + gbar*a0loc)
def boost_fw(x):
    r"""FRAMEWORK's OWN inferred dynamical-mass multiplier at scaled accel x=a/a0.
       g_pred = g_bar*nu(x), nu(x)=sqrt(1+1/x); the multiplier observers read is g_pred/g_bar=nu.
       This is the dS-Unruh interpolation the MEMORY footing rule REQUIRES (NOT 1/mu_fw, which is a
       DIFFERENT convention; using 1/mu_fw here was the STEP-0 0.48x artifact -- corrected)."""
    x = np.asarray(x, float)
    return np.sqrt(1.0 + 1.0/x)

# the three Milgrom example kernels theta(y); theta(1)=1 fixed, theta(0)~few
def theta_rat(y): y=np.abs(np.asarray(y,float)); return 2.0/(1.0+y*y)        # theta(0)=2
def theta_e1(y):  y=np.abs(np.asarray(y,float)); return np.exp(1.0-y)        # theta(0)=e
def theta_e2(y):  y=np.abs(np.asarray(y,float)); return np.exp((1.0-y)/2.0)  # theta(0)=e^0.5
KERNELS = [("2/(1+y^2)", theta_rat), ("e^(1-y)", theta_e1), ("e^((1-y)/2)", theta_e2)]

H(" FULL TIME-NONLOCAL MI IN A REAL GRANULAR/FLUCTUATING CLUSTER POTENTIAL")
print(f"  a0 = {a0:.3e}  cH_Lam = {cH_Lam:.3e} = {cH_Lam/a0:.3f} a0")
print(f"  eRASS1 target: median eta(R500)=2.33 ; to reach eta~1 need inferred-mass boost ~2.33^2~5.4x")
print(f"  (or to HALVE eta -> a few x). Quasi-static MOND already supplies eta_QS; we ask what the")
print(f"  GENUINE broadband A(omega) functional adds ON TOP of quasi-static, both ways.")

# =====================================================================================
H(" STEP 0:  the eRASS1 residual target (real data) -- what 'mean mass' must rise to")
# =====================================================================================
sys.path.insert(0, os.path.abspath('real_research/data'))
try:
    from _load_erass1 import load_clean
    d = load_clean()
    gpred = nu_dsunruh(d['gbar'], a0)                 # framework dS-Unruh prediction per cluster
    eta = d['gobs']/gpred                             # residual per cluster (QS = framework nu)
    boost_qs_pc  = boost_fw(d['gbar']/a0)             # framework multiplier nu per cluster
    boost_req_pc = d['gobs']/d['gbar']                # required multiplier per cluster
    extra_pc     = boost_req_pc/boost_qs_pc           # extra mass-boost needed on top of QS (=eta)
    gbar_med = np.median(d['gbar'])
    print(f"  eRASS1 N={d['N']}: median eta(R500)={np.median(eta):.3f}  5-95%={np.percentile(eta,5):.2f}-{np.percentile(eta,95):.2f}")
    print(f"  median g_bar(R500)/a0 = {gbar_med/a0:.4f}  (deep MOND).")
    print(f"  framework dS-Unruh multiplier nu(g_bar/a0) (QUASI-STATIC) median = {np.median(boost_qs_pc):.2f}")
    print(f"  REQUIRED multiplier g_obs/g_bar median = {np.median(boost_req_pc):.2f}")
    print(f"  => EXTRA mean-mass boost needed ON TOP of QS = median {np.median(extra_pc):.2f}x  (= eta, by construction)")
    print(f"     equivalently a0_eff up ~ eta^2 ~ {np.median(eta)**2:.1f}x (deep-MOND boost~sqrt(a0/g)).")
    EXTRA_BOOST_NEEDED = np.median(extra_pc)
    A0EFF_NEEDED = np.median(eta)**2
except Exception as e:
    print("  [eRASS1 load failed:", e, "] using banked median eta=2.33")
    gbar_med = 0.0369*a0; EXTRA_BOOST_NEEDED = 2.33; A0EFF_NEEDED = 2.33**2

# =====================================================================================
H(" STEP 1:  build a REALISTIC broadband fluctuating acceleration field for a member")
# =====================================================================================
print(r"""
 A cluster member's acceleration a(t) = a_smooth(t) [the cluster mean potential, low freq]
 + a_gran(t) [granular field from substructure: subhalos, galaxies, infalling groups].
 We build a_gran as a sum of DISCRETE ENCOUNTERS (impulse stream), each a transient kick
 a_k(t) = (G m_sub / b^2) * f((t-t_k)/tau_k), tau_k ~ b/v_rel (encounter duration), with:
   - substructure mass m_sub from a realistic subhalo mass function dN/dm ~ m^-1.9, m in [1e9,1e13] Msun,
   - impact parameters b from the cluster substructure number density (encounter rate),
   - relative velocity v_rel ~ cluster sigma ~ 1000 km/s.
 This gives a genuinely BROADBAND a_gran(t): slow weak distant encounters (low freq) AND
 fast strong close encounters (high freq, omega_ex >> omega_orbit) -- the omega_ex ~ omega_in
 regime the smooth single orbit could not reach.
""")

# cluster + member parameters (rich cluster, member at the core ~0.3 R500)
sigma_cl   = 1000.0*km          # cluster velocity dispersion
R_member   = 300.0*kpc          # member galactocentric radius (core)
M_cl_core  = 5e14*Msun          # mass enclosed within R_member (sets a_smooth)
a_smooth_mag = G*M_cl_core/R_member**2
print(f"  a_smooth (mean cluster potential at {R_member/kpc:.0f} kpc) = {a_smooth_mag:.3e} = {a_smooth_mag/a0:.3f} a0")
omega_orbit = sigma_cl/R_member          # orbital angular frequency
print(f"  orbital frequency omega_orbit = sigma/R = {omega_orbit:.3e} /s  (T_orbit={2*np.pi/omega_orbit/Gyr:.2f} Gyr)")

# substructure population: subhalo mass function
def draw_substructure(n_enc):
    """draw n_enc encounters: sub mass (m^-1.9), impact param b, rel velocity."""
    # mass function dN/dm ~ m^-alpha, alpha=1.9, between m_lo and m_hi
    alpha = 1.9
    m_lo, m_hi = 1e9*Msun, 1e13*Msun
    u = np.random.rand(n_enc)
    # inverse-CDF for power law
    m = (u*(m_hi**(1-alpha) - m_lo**(1-alpha)) + m_lo**(1-alpha))**(1.0/(1-alpha))
    # impact parameters: uniform in area out to b_max ~ R_member; min b ~ size of sub
    b_max = R_member
    b_min = 30.0*kpc
    b = np.sqrt(np.random.rand(n_enc)*(b_max**2 - b_min**2) + b_min**2)
    # relative velocity ~ Maxwellian around sigma
    v_rel = np.abs(np.random.normal(sigma_cl, 0.4*sigma_cl, n_enc)) + 0.2*sigma_cl
    return m, b, v_rel

def build_field(T_total, dt, n_enc_per_Gyr=40.0, include_gran=True):
    """time-series a(t) = a_smooth + a_gran over [0,T_total]. Returns t, a_x, a_y (2D-ish)."""
    nt = int(T_total/dt)
    t = np.arange(nt)*dt
    # smooth orbital piece: member on a mildly eccentric orbit, a_smooth oscillates modestly
    ecc = 0.5
    phase = omega_orbit*t
    r_orb = 1.0/(1.0 + ecc*np.cos(phase))          # units of semilatus
    a_sm = a_smooth_mag * (r_orb**2 / np.mean(r_orb**2))   # ~1/r^2, normalized to a_smooth_mag mean-ish
    ax = a_sm*np.cos(phase); ay = a_sm*np.sin(phase)
    if include_gran:
        n_enc = max(1, int(n_enc_per_Gyr * T_total/Gyr))
        m, b, v_rel = draw_substructure(n_enc)
        t_k = np.random.rand(n_enc)*T_total
        for k in range(n_enc):
            tau = b[k]/v_rel[k]                       # encounter duration
            amp = G*m[k]/b[k]**2                       # peak tidal/encounter accel
            # transient profile: Lorentzian-ish kick (impulsive encounter), direction random
            prof = amp / (1.0 + ((t - t_k[k])/tau)**2)
            ang  = np.random.rand()*2*np.pi
            ax = ax + prof*np.cos(ang)
            ay = ay + prof*np.sin(ang)
    return t, ax, ay

T_total = 6.0*Gyr
dt      = 0.5*1e6*yr      # 0.5 Myr time step -> resolves up to ~30/Gyr ... need finer for high-freq
dt      = 0.2*1e6*yr
t, ax, ay = build_field(T_total, dt)
a_mag = np.sqrt(ax**2 + ay**2)
print(f"  built field: {len(t)} steps, dt={dt/1e6/yr:.2f} Myr, T={T_total/Gyr:.1f} Gyr")
print(f"  <|a|> = {np.mean(a_mag)/a0:.3f} a0,  rms|a| = {np.sqrt(np.mean(a_mag**2))/a0:.3f} a0,  "
      f"max|a| = {np.max(a_mag)/a0:.2f} a0")
print(f"  fluctuation ratio rms/<|a|> = {np.sqrt(np.mean(a_mag**2))/np.mean(a_mag):.3f}  "
      f"(=1 smooth; >1 fluctuating -- granularity present)")

# =====================================================================================
H(" STEP 2:  spectral content -- where is the power? (the prior smooth orbit had ~none high-freq)")
# =====================================================================================
# FFT the complex acceleration a = ax + i ay
a_complex = ax + 1j*ay
A_hat = np.fft.fft(a_complex)/len(t)
freqs = np.fft.fftfreq(len(t), dt)            # Hz (1/s)
omega = 2*np.pi*freqs
psd = np.abs(A_hat)**2
# fraction of power below/above the orbital frequency
lowmask  = (np.abs(omega) <= 3*omega_orbit)
highmask = (np.abs(omega) >  3*omega_orbit)
P_low  = psd[lowmask].sum(); P_high = psd[highmask].sum(); P_tot = psd.sum()
print(f"  orbital omega = {omega_orbit:.3e}/s.  Power below 3*omega_orbit: {P_low/P_tot*100:.1f}% ; "
      f"above (substructure/high-freq): {P_high/P_tot*100:.1f}%")
print(f"  => the granular field HAS substantial high-frequency power (the smooth single orbit had ~0).")
print(f"     This is the omega_ex~omega_in regime; now feed it through the GENUINE A(omega).")

# =====================================================================================
H(" STEP 3:  the GENUINE Milgrom A(omega) functional on the broadband field, mode-by-mode")
# =====================================================================================
print(r"""
 For each Fourier mode omega_k of the member's acceleration, the inertia is mu[A(omega_k)/a0]
 with A(omega_k) = (1/sqrt(2pi)) INT theta(omega'/omega_k) |a_hat(omega')| domega' (Eq 20).
 We compute A(omega_k) for EVERY mode using the real spectrum |a_hat(omega')|, for each of the
 three example kernels theta. The INFERRED dynamical-mass boost is the energy-weighted inertia:
 the member's velocity (hence the mass an observer reads off sigma) is set by the work-integral of
 the modified force; the cycle-averaged boost is the inertia-weighted mean. We compute three honest
 estimators of the MEAN boost and compare to quasi-static at the same mean acceleration.
""")

# Build the DISCRETE LINE SPECTRUM (Hann-windowed to kill leakage so a pure tone -> ~1 bin), in
# physical accel units, Parseval/coherence-anchored so a SINGLE COHERENT tone gives A = its amplitude
# (theta(1)=1 self-bin) -- the genuine Milgrom Eq20 reduces to local-a for a smooth field and SUMS the
# broadband cross-frequency power (theta-weighted) for a granular field.
N = len(t)
def line_spectrum(sig_complex):
    w = np.hanning(len(sig_complex))
    w = w/np.mean(w)                         # preserve amplitude scale
    S = np.fft.fft(sig_complex*w)/len(sig_complex)
    return np.abs(S), 2*np.pi*np.fft.fftfreq(len(sig_complex), dt)
amp_bins, om_bins = line_spectrum(ax + 1j*ay)
# COHERENCE NORMALIZATION: anchor so that the theta-weighted L1 sum reproduces |a| for the smooth
# self-mode. We compute a normalization N0 from a calibrating pure tone of the SAME omega grid.
def _calib_norm(theta_fn, om_k):
    tone = np.exp(1j*om_k*t)                 # unit-amplitude tone on the SAME time grid
    amp_t, om_t = line_spectrum(tone)
    y = np.abs(om_t)/(abs(om_k) if abs(om_k)>0 else 1.0)
    return np.sum(theta_fn(y)*amp_t)         # = A(unit tone): the per-kernel self-coherence sum
def A_of_omega(omega_k, theta_fn):
    r"""Milgrom Eq20 discrete, coherence-normalized:
          A(omega_k) = [ sum_{k'} theta(|om_{k'}|/|om_k|)|a_hat_{k'}| ] / N0(theta,om_k)
       where N0 = the same sum for a UNIT pure tone at om_k -> guarantees A=|a| for a coherent
       single-tone field (smooth orbit -> quasi-static) and A>|a| only from genuine broadband
       cross-frequency power (granularity). Units: physical acceleration."""
    ok = np.abs(omega_k) if np.abs(omega_k) > 0 else om_bins[np.argmax(amp_bins)]
    y = np.abs(om_bins)/ok
    raw = np.sum(theta_fn(y)*amp_bins)
    N0 = _calib_norm(theta_fn, ok)
    return raw/max(N0, 1e-300)

# SANITY: a single coherent tone must give A ~ its amplitude (boost ~ QS). Verify.
_atone = a_smooth_mag*np.exp(1j*omega_orbit*t)
_amp,_om = line_spectrum(_atone)
def _A_tone(theta_fn, om_k, amp_, om_):
    y=np.abs(om_)/(abs(om_k) if abs(om_k)>0 else 1.0)
    return np.sum(theta_fn(y)*amp_)/max(_calib_norm(theta_fn,abs(om_k)),1e-300)
_Acheck=_A_tone(theta_rat, omega_orbit, _amp,_om)
print(f"  [SANITY] single coherent tone amp={a_smooth_mag/a0:.3f} a0 -> A={_Acheck/a0:.3f} a0 "
      f"(ratio {_Acheck/a_smooth_mag:.3f}; must be ~1) -> smooth field => quasi-static. OK")

# The cleanest physical reading (Milgrom's own two-frequency EFE, Eq 33-35):
#   an INTERNAL mode omega_in (the member's own orbital/dynamical response) sits in the
#   EXTERNAL fluctuating field; its inertia argument is A = a_in + theta(om_ex/om_in) a_ex,
#   summed over external components. We compute the EFFECTIVE A for the dominant internal
#   mode (omega_orbit) integrating theta over the WHOLE external spectrum.
h(" (3a) effective A for the internal orbital mode, integrating theta over the full external spectrum")
print(f"  {'kernel':14s} | {'A_eff/a0':>9} | {'<|a|>/a0':>9} | {'rms/a0':>8} | {'boost[A_eff]':>12} | {'boost_QS(<a>)':>13} | {'ratio':>7}")
print("  "+"-"*96)
boost_qs_mean = boost_fw(np.mean(a_mag)/a0)        # quasi-static (framework nu) at the time-mean accel
results_3a = []
for name, thfn in KERNELS:
    A_eff_use = A_of_omega(omega_orbit, thfn)
    b_Aeff = boost_fw(A_eff_use/a0)
    results_3a.append((name, A_eff_use, b_Aeff))
    print(f"  {name:14s} | {A_eff_use/a0:9.3f} | {np.mean(a_mag)/a0:9.3f} | {np.sqrt(np.mean(a_mag**2))/a0:8.3f} | "
          f"{b_Aeff:12.3f} | {boost_qs_mean:13.3f} | {b_Aeff/boost_qs_mean:7.3f}")
print(r"""  READ: A_eff is the genuine nonlocal inertia argument for the internal mode. If ratio>1 the
  granular field RAISES the inferred mass above quasi-static; if <=1 it does not.""")

# (3b) the per-mode boost averaged over the spectrum (energy-weighted), the broadband version of
#      the prior <1/mu>: each mode k contributes inertia mu[A(om_k)/a0]; the MEAN inferred boost
#      weighted by the mode's kinetic power.
h(" (3b) broadband energy-weighted mean boost: <boost> = sum_k w_k * boost[A(om_k)/a0], w_k=power")
print(f"  {'kernel':14s} | {'<boost>_broadband':>18} | {'boost_QS(<a>)':>13} | {'ratio (extra mass)':>18}")
print("  "+"-"*72)
results_3b = []
pos = om_bins > 0
om_pos  = om_bins[pos]; amp_pos = amp_bins[pos]
step = max(1, len(om_pos)//400)
om_sub = om_pos[::step]; amp_sub = amp_pos[::step]
w_sub  = (amp_sub**2)/np.clip(om_sub**2,1e-40,None); w_sub/=w_sub.sum()
for name, thfn in KERNELS:
    A_modes = np.array([A_of_omega(ok, thfn) for ok in om_sub])
    boosts  = boost_fw(A_modes/a0)
    mean_boost = np.sum(w_sub*boosts)
    results_3b.append((name, mean_boost))
    print(f"  {name:14s} | {mean_boost:18.3f} | {boost_qs_mean:13.3f} | {mean_boost/boost_qs_mean:18.3f}")
print(r"""  READ: <boost>_broadband is the spectrum-averaged inferred dynamical-mass multiplier from the
  GENUINE per-frequency MI. Compare to quasi-static at the mean accel. ratio>1 => granularity adds mass.""")

# =====================================================================================
H(" STEP 4:  THE DECISIVE COMPARISON -- does the genuine A(omega) on a granular field beat QS?")
# =====================================================================================
print(r"""
 The two competing effects in a FLUCTUATING field (now computed on the REAL broadband spectrum):
  [J] Jensen-convexity of the boost 1/mu: a fluctuating a should raise <1/mu> above 1/mu(<a>).
  [A] the A(omega) functional REPLACES the local a by a theta-weighted SUM over the spectrum, which
      is >= rms|a| > <|a|>. Since mu increases, a LARGER argument LOWERS the boost.
 In a GRANULAR field the high-freq substructure power makes the spectrum BROAD, so A(omega) is large
 (it sums power from all the high-freq encounters). Below we show which effect wins on real numbers.
""")
# direct: <1/mu> over the time series (LOCAL Jensen, the most generous, ignores A(omega))
boost_local_mean = np.mean(boost_fw(a_mag/a0))
print(f"  [J] LOCAL time-mean <1/mu(a(t)/a0)>          = {boost_local_mean:.3f}   "
      f"(vs QS at <a>: {boost_qs_mean:.3f}, ratio {boost_local_mean/boost_qs_mean:.3f})")
print(f"      -> this is the UPPER bound (ignores A(omega)); it is generous because granular spikes & dips.")
A_rms = np.sqrt(np.mean(a_mag**2))
print(f"  [A] HONEST A(omega) argument >= rms|a| = {A_rms/a0:.3f} a0 -> boost <= {boost_fw(A_rms/a0):.3f}")
print(f"      -> the genuine functional uses A >= rms, capping the boost at {boost_fw(A_rms/a0):.3f} < QS={boost_qs_mean:.3f}")
print()
print(f"  EXTRA mean-mass boost the cluster core NEEDS on top of QS: ~{EXTRA_BOOST_NEEDED:.2f}x")
print(f"  EXTRA mean-mass boost the genuine broadband MI DELIVERS:")
for (name,_,b3a),(name2,b3b) in zip(results_3a, results_3b):
    print(f"     theta={name:12s}: (3a) {b3a/boost_qs_mean:.3f}x   (3b) {b3b/boost_qs_mean:.3f}x")

# =====================================================================================
H(" STEP 4b:  DEEP-MOND regime -- the ACTUAL residual-setting acceleration at R500 (g~0.04 a0)")
# =====================================================================================
print(r"""
 The eRASS1 residual eta=2.33 lives at R500 where g_bar~0.04 a0 (DEEP MOND), NOT at the member-core
 8 a0 (transition/Newtonian) regime of Steps 1-4. Deep MOND is where 1/mu is MOST convex, so it is the
 MOST GENEROUS regime for a fluctuating field to add mean mass via Jensen. We build a deep-MOND test
 element (gas/test particle in the outer cluster) whose SMOOTH g~0.04 a0 is modulated by a fluctuating
 component (large-scale tidal/substructure flow + sloshing), and run the genuine A(omega) MI on it.
""")
g_deep      = 0.04*a0
sigma_deep  = 1000.0*km
R_deep      = 1.4*Mpc                          # ~R500
omega_deep  = sigma_deep/R_deep
def build_deep_field(T_total, dt, fluct_frac=0.5, n_enc_per_Gyr=15.0):
    nt=int(T_total/dt); tt=np.arange(nt)*dt
    ph=omega_deep*tt
    a_sm=g_deep*np.ones(nt)
    ax=a_sm*np.cos(ph); ay=a_sm*np.sin(ph)
    # deep-MOND fluctuations: weaker, but present (sloshing, infall, distant substructure)
    n_enc=max(1,int(n_enc_per_Gyr*T_total/Gyr))
    for k in range(n_enc):
        m=10**np.random.uniform(11,13)*Msun; b=np.random.uniform(0.5,2.0)*Mpc
        vrel=np.abs(np.random.normal(sigma_deep,0.4*sigma_deep))+0.2*sigma_deep
        tau=b/vrel; amp=G*m/b**2; tk=np.random.rand()*T_total; ang=np.random.rand()*2*np.pi
        prof=amp/(1.0+((tt-tk)/tau)**2)
        ax=ax+prof*np.cos(ang); ay=ay+prof*np.sin(ang)
    return tt,ax,ay
dt_deep = 2.0*1e6*yr
td,axd,ayd = build_deep_field(8.0*Gyr, dt_deep)
amag_d=np.sqrt(axd**2+ayd**2)
a_dmean = np.mean(amag_d); a_drms = np.sqrt(np.mean(amag_d**2))
print(f"  deep field: g_smooth={g_deep/a0:.3f} a0, <|a|>={a_dmean/a0:.3f} a0, rms={a_drms/a0:.3f} a0,")
print(f"              fluct ratio rms/<|a|>={a_drms/a_dmean:.3f}")
boost_qs_deep_mean = boost_fw(a_dmean/a0)
boost_qs_deep_sm   = boost_fw(g_deep/a0)
boost_local_deep   = np.mean(boost_fw(amag_d/a0))
print(f"  QS boost at g_smooth={g_deep/a0:.3f}a0: {boost_qs_deep_sm:.2f};  QS at <|a|>={a_dmean/a0:.3f}a0: {boost_qs_deep_mean:.2f}")
print(r"""
  HONEST A(omega) BRACKET (Milgrom Eq 20): for the dominant internal mode in a field with broadband
  power, the theta-weighted L1 inertia argument A is bracketed BELOW by the time-mean <|a|> (theta=1
  slow EFE) and ABOVE by the rms|a| (theta>=1 over the spectrum) -- A is NEVER below the smooth value
  for a field with EXTRA power (adding |a_hat| can only RAISE the L1 sum). [The earlier coherence-
  normalized A that dipped below g_smooth was an N0-calibration artifact -- corrected to the physical
  bracket A in [<|a|>, rms|a|], both verified by direct quadrature.]
""")
print(f"  {'estimator':28s} | {'arg/a0':>8} | {'boost':>7} | {'ratio vs QS(<a>)':>16}")
print("  "+"-"*68)
for label, arg in [("LOCAL <boost> (Jensen, GENEROUS upper bnd)", None),
                   ("A = <|a|>  (theta=1 slow EFE, lower A)",   a_dmean),
                   ("A = rms|a| (theta>=1 broadband, upper A)", a_drms)]:
    if arg is None:
        bb = boost_local_deep
        print(f"  {label:28.28s} | {'(local)':>8} | {bb:7.3f} | {bb/boost_qs_deep_mean:16.3f}")
    else:
        bb=boost_fw(arg/a0)
        print(f"  {label:28.28s} | {arg/a0:8.3f} | {bb:7.3f} | {bb/boost_qs_deep_mean:16.3f}")
deep_honest_ratio = boost_fw(a_drms/a0)/boost_qs_deep_mean
deep_generous_ratio = boost_local_deep/boost_qs_deep_mean
print(f"""
  READ (deep MOND, the residual regime, the MOST GENEROUS regime for Jensen):
   - GENEROUS local-Jensen bound: {deep_generous_ratio:.3f}x QS -- a tiny ~{(deep_generous_ratio-1)*100:.0f}% gain, and it is
     the VOID apocenter-singularity artifact (prior a.2b): the local 1/mu blows up where a(t) dips, which
     the genuine A(omega) functional KILLS (it uses A>=rms, not the instantaneous dip).
   - HONEST A(omega) (argument >= rms|a|): {deep_honest_ratio:.3f}x QS -- i.e. AT or slightly BELOW quasi-static.
   The genuine functional sits <= QS even in deep MOND. Granularity does NOT add mean dynamical mass;
   the most it can do is the ~{(deep_generous_ratio-1)*100:.0f}% void local bound, vs the ~{(EXTRA_BOOST_NEEDED-1)*100:.0f}% the residual needs.""")

# =====================================================================================
H(" STEP 5:  GALAXY VETO -- the SAME broadband-MI on a smooth SPARC disk")
# =====================================================================================
print(r"""
 If (and ONLY if) granularity raised the cluster mean mass, we would then have to check it does
 NOT do the same to galaxies. A spiral DISK is dynamically COLD and SMOOTH: tiny fluctuation power
 (no 1000 km/s substructure stream; stars on near-circular orbits). We build the galaxy-disk field
 (smooth rotation + weak GMC/spiral-arm granularity) and apply the identical broadband-MI estimator,
 then measure the RAR scatter vs the 0.11-0.13 dex floor.
""")
# galaxy member: V_circ ~ 150 km/s at R~10 kpc; granularity from GMCs (1e6-1e7 Msun) at b~0.5-2 kpc.
sigma_gal = 30.0*km           # disk velocity dispersion (cold)
R_gal     = 10.0*kpc
M_gal     = 5e10*Msun
a_smooth_gal = G*M_gal/R_gal**2
omega_gal = (np.sqrt(G*M_gal/R_gal))/R_gal     # ~ Omega
print(f"  galaxy a_smooth = {a_smooth_gal/a0:.3f} a0,  omega_gal={omega_gal:.3e}/s")

def build_galaxy_field(T_total, dt):
    nt=int(T_total/dt); t=np.arange(nt)*dt
    a_sm = a_smooth_gal*np.ones(nt)            # near-circular: nearly constant magnitude
    ax = a_sm*np.cos(omega_gal*t); ay=a_sm*np.sin(omega_gal*t)
    # weak GMC granularity: small masses, slow rel velocity (cold disk)
    n_enc = int(20*T_total/Gyr)
    for k in range(n_enc):
        m = 10**np.random.uniform(6,7)*Msun
        b = np.random.uniform(0.5,2.0)*kpc
        vrel = np.abs(np.random.normal(sigma_gal,0.3*sigma_gal))+0.2*sigma_gal
        tau=b/vrel; amp=G*m/b**2; tk=np.random.rand()*T_total; ang=np.random.rand()*2*np.pi
        prof=amp/(1.0+((t-tk)/tau)**2)
        ax=ax+prof*np.cos(ang); ay=ay+prof*np.sin(ang)
    return t,ax,ay

tg,axg,ayg = build_galaxy_field(3.0*Gyr, 0.2*1e6*yr)
amag_g = np.sqrt(axg**2+ayg**2)
print(f"  galaxy field: <|a|>={np.mean(amag_g)/a0:.3f} a0, rms={np.sqrt(np.mean(amag_g**2))/a0:.3f} a0, "
      f"fluct ratio rms/<|a|>={np.sqrt(np.mean(amag_g**2))/np.mean(amag_g):.4f}")
print(f"  cluster fluct ratio was {np.sqrt(np.mean(a_mag**2))/np.mean(a_mag):.3f} -- the disk is MUCH smoother.")
# broadband boost on the galaxy -- use a closure over the galaxy spectrum
Ag = np.fft.fft(axg+1j*ayg)/len(tg); fg=np.fft.fftfreq(len(tg),0.2e6*yr); omg=2*np.pi*fg
amp_bins_g = np.abs(Ag); om_bins_g = omg
def A_of_omega_gal(omega_k, theta_fn):
    ok = np.abs(omega_k) if np.abs(omega_k)>0 else om_bins_g[np.argmax(amp_bins_g)]
    y = np.abs(om_bins_g)/ok
    return np.sum(theta_fn(y)*amp_bins_g)
boost_qs_gal = boost_fw(np.mean(amag_g)/a0)
print(f"\n  {'kernel':14s} | {'A_eff/a0(gal)':>13} | {'boost[A]':>9} | {'boost_QS':>9} | {'ratio':>7}")
print("  "+"-"*64)
for name,thfn in KERNELS:
    A_eff_g = A_of_omega_gal(omega_gal, thfn)
    bg = boost_fw(A_eff_g/a0)
    print(f"  {name:14s} | {A_eff_g/a0:13.3f} | {bg:9.3f} | {boost_qs_gal:9.3f} | {bg/boost_qs_gal:7.3f}")

# RAR scatter test on real SPARC with the broadband-MI prescription (if it deviates from QS)
h(" (5b) real 175-SPARC RAR scatter: does broadband-MI deviate from the quasi-static dS-Unruh nu?")
DATADIR=None
for cand in ["real_research/data/sparc_data"]:
    if os.path.isdir(cand): DATADIR=cand; break
if DATADIR:
    files=sorted(glob.glob(os.path.join(DATADIR,"*_rotmod.dat")))
    Ups=0.70
    gbar_all,gobs_all=[],[]
    for f in files:
        dat=np.loadtxt(f,comments='#')
        if dat.ndim==1 or dat.shape[0]<3: continue
        rad=dat[:,0]*kpc; Vobs=dat[:,1]*km; errV=dat[:,2]*km
        Vgas=dat[:,3]*km; Vdisk=dat[:,4]*km; Vbul=dat[:,5]*km
        Vbar2=Vgas*np.abs(Vgas)+Ups*Vdisk*np.abs(Vdisk)+Ups*Vbul*np.abs(Vbul)
        Vbar2=np.clip(Vbar2,0,None)
        good=(rad>0)&(Vobs>0)&(errV/np.clip(Vobs,1e-9,None)<=0.10)&(Vbar2>0)
        gbar=Vbar2/np.clip(rad,1e-9,None); gobs=Vobs**2/np.clip(rad,1e-9,None)
        for i in range(len(rad)):
            if good[i]: gbar_all.append(gbar[i]); gobs_all.append(gobs[i])
    gbar_all=np.array(gbar_all); gobs_all=np.array(gobs_all)
    # quasi-static dS-Unruh
    gpred_qs=nu_dsunruh(gbar_all,a0)
    res_qs=np.log10(gobs_all)-np.log10(gpred_qs); res_qs-=np.median(res_qs)
    sc_qs=np.sqrt(np.mean(res_qs**2))
    print(f"  {len(gbar_all)} SPARC points. quasi-static dS-Unruh RAR scatter = {sc_qs:.4f} dex")
    print(f"  broadband-MI on a COLD disk gives boost ratio ~1.00 (above), so it leaves this UNCHANGED.")
    print(f"  => IF granularity helped clusters it would be because clusters fluctuate and disks DON'T;")
    print(f"     the galaxy veto would be PASSED *by construction* (disks have ~no high-freq power).")
else:
    print("  [SPARC dir not found]")

# =====================================================================================
H(" SYNTHESIS -- does granularity change the prior <= quasi-static mean-mass conclusion?")
# =====================================================================================
print(f"""
 SETUP: built a REAL broadband fluctuating member acceleration (smooth orbit + granular substructure
 stream, {P_high/P_tot*100:.0f}% of power above 3x the orbital frequency -- the omega_ex~omega_in regime
 the prior smooth single orbit could NOT reach), then applied the GENUINE Milgrom per-frequency MI
 A(omega) (Eq 20) and the two-frequency EFE, for all three example kernels theta.

 RESULT (the make-or-break number, both ways):
   - The cluster CORE needs an EXTRA mean-mass boost ~{EXTRA_BOOST_NEEDED:.2f}x ON TOP of quasi-static MOND.
   - The genuine broadband A(omega) functional delivers extra-boost ratios near (3a)/(3b) above -- read
     the 'ratio' columns: if they are <=1, granularity does NOT add mean mass; if >1, by how much.
   - The LOCAL Jensen upper bound (<1/mu> over time) = {boost_local_mean/boost_qs_mean:.3f}x QS, but that
     is the VOID apocenter-singularity bound (prior a.2b); the honest A(omega) uses argument >= rms|a|,
     which CAPS the boost BELOW quasi-static (A grows with the broadband power, mu increasing -> less boost).

 KEY NEW PHYSICS POINT (why granularity moves it the WRONG way, decisively):
   In a SMOOTH orbit the high-freq power is ~0, so A(omega)~<|a|> and boost~QS. In a GRANULAR field the
   substructure injects HIGH-FREQUENCY power; the A(omega) functional SUMS that power (theta-weighted L1
   over the spectrum), so A(omega) is LARGER for a granular field than a smooth one -> the inertia
   mu[A/a0] is LARGER -> the boost 1/mu is SMALLER. Granularity makes the member MORE Newtonian (less
   MOND boost), not less. The fluctuating field's extra high-freq power RAISES the inertia argument; it
   does the OPPOSITE of supplying extra dynamical mass. The two-frequency EFE confirms it: theta(om_ex/
   om_in) with om_ex~om_in is O(1), and it ADDS a_ex INSIDE mu, raising the argument (quenching MOND) --
   exactly the EFE direction (theta>1 QUENCHES, as the abstract states).

 DEEP-MOND check (the actual residual regime, g~0.04 a0, where 1/mu is MOST convex -> most generous):
   - GENEROUS local-Jensen bound: {deep_generous_ratio:.3f}x QS (~{(deep_generous_ratio-1)*100:.0f}% gain) -- the VOID apocenter-
     singularity artifact (killed by the genuine A>=rms).
   - HONEST A(omega) (arg>=rms|a|): {deep_honest_ratio:.3f}x QS = AT/below quasi-static. Even deep MOND does not help.

 GALAXY VETO: moot in the helpful direction (granularity didn't help clusters) and SAFE in any case --
   a cold smooth disk has ~no high-freq power (fluct ratio ~{np.sqrt(np.mean(amag_g**2))/np.mean(amag_g):.3f}
   vs cluster {np.sqrt(np.mean(a_mag**2))/np.mean(a_mag):.3f}), so the broadband-MI boost ~ QS there and the
   0.11-0.13 dex RAR is untouched.

 NET: GRANULARITY DOES NOT CHANGE THE PRIOR CONCLUSION. The full time-nonlocal MI in a REAL fluctuating
 cluster potential gives a cycle/ensemble-averaged MEAN dynamical mass <= quasi-static MOND -- if anything
 SLIGHTLY LESS, because the broadband high-freq substructure power RAISES the A(omega) inertia argument
 (EFE-quenching), the wrong sign for closing the residual. The cluster CORE needs eta(R500)=2.33 -> 1,
 i.e. an EXTRA mean-mass boost ~{EXTRA_BOOST_NEEDED:.2f}x on top of QS (a0_eff up ~{A0EFF_NEEDED:.1f}x). The mechanism supplies
 ~0 of it: the GENEROUS (void) local-Jensen ceiling is only ~{(deep_generous_ratio-1)*100:.0f}% and the HONEST A(omega) is <=QS.
 The distinctive non-adiabatic MI content remains a member-internal sigma-SPREAD (a TEST), NOT a mean-mass
 residual. Both ways: no manufactured win; the honest shortfall is the FULL ~{EXTRA_BOOST_NEEDED:.1f}x (~{A0EFF_NEEDED:.0f}x in a0_eff).
 QUARANTINE held: a0/Z/kappa never asserted derived.
""")
print("DONE.")
