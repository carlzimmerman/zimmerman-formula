#!/usr/bin/env python3
"""
ROUTE 5 -- DESI DR3 / future forecast: can the evolving-DE measurement PIN the framework's
distinctive a0(z), and is it DECISIVE?  (Opus 4.8, 2026-06-14)

The framework: a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0)  (the IF cancels in the ratio).
  - If DE is a TRUE cosmological constant (w=-1): rho_DE const -> a0(z)=a0(0) CONSTANT at all z
    => NO distinctive content (identical to z=0 MOND). DISTINCTIVE TEST VANISHES.
  - If DE EVOLVES (DESI DR2 w0>-1, wa<0, thawing): rho_DE lower in past -> a0(z) DECLINES.
    => the distinctive declining branch is LIVE and falsifiable.

So DESI is a CONDITIONAL GATE on whether there is a distinctive test at all. This script forecasts:
  (A) the gate: how DESI DR3 firming-up / reverting changes the framework's distinctive exposure;
  (B) the tracking test -- a0(z) measured from high-z kinematics MUST track DESI's rho_DE(z);
      the SNR on that, marginalized over the DR3 (w0,wa) prior (the binding term, NOT galaxy N);
  (C) the timeline + decisiveness: when can a0(z)-tracks-rho_DE(z) be tested at >3 sigma?

Both ways: DESI measures the INPUT rho_DE, NOT a0 -- "DESI confirms a0(z)" is FORBIDDEN. The
distinctive prediction currently LEANS UNFAVOURABLE (MUSE rising, de-syst ~1.5 sigma against).
Reported straight. No manufactured win from the DESI alignment, no dismissal of the distinctive bet.

Numbers reproduce the banked combined_fisher_ultra.py machinery; DR3 prior = DR2 / 1.5 (DESI forecast,
arXiv 2503.14738: w0,wa uncertainties improve ~1.5-1.8x DR2->final-survey). numpy-only.
"""
import numpy as np

LN10 = np.log(10.0)

# ---- DESI DR2 CPL central values + the (w0,wa) covariance (DESI+CMB+DESY5) ----
W0, WA = -0.752, -0.86
W0_ERR_DR2, WA_ERR_DR2 = 0.057, 0.220
RHO = -0.45                      # w0-wa anti-correlation in the DESI contour

# ---- the survey baseline (labeled assumptions, matched to the banked forecast) ----
SIG_DEX = 0.06                   # per-galaxy log V_flat precision (intrinsic ~0.026 + meas ~0.05)
P_BTFR  = 0.25                   # V_flat = (G M_b a0)^(1/4) -> O=logV ~ (1/4) log a0


def rho_DE_ratio(z, w0=W0, wa=WA):
    a = 1.0/(1.0+z)
    return a**(-3.0*(1.0+w0+wa)) * np.exp(-3.0*wa*(1.0-a))


def ln_ratio(z, w0=W0, wa=WA):
    a = 1.0/(1.0+z)
    return -3.0*(1.0+w0+wa)*np.log(a) - 3.0*wa*(1.0-a)


def a0_ratio(z, w0=W0, wa=WA):                 # framework: a0(z)/a0(0) = sqrt(rho_DE ratio)
    return np.sqrt(rho_DE_ratio(z, w0, wa))


def _ders(z, p=P_BTFR, beta=1.0):
    """d O / d(beta, w0, wa) at fiducial beta=1, O = log10 V_flat ; a0(z)=a0(0)[rho_DE]^(beta/2)."""
    a = 1.0/(1.0+z)
    dlnr_dw0 = -3.0*np.log(a)
    dlnr_dwa = -3.0*np.log(a) - 3.0*(1.0-a)
    dO_dbeta = 0.5*p*ln_ratio(z)/LN10
    dO_dw0   = 0.5*p*beta*dlnr_dw0/LN10
    dO_dwa   = 0.5*p*beta*dlnr_dwa/LN10
    return np.array([dO_dbeta, dO_dw0, dO_dwa])


def sigma_beta_marg(bins, w0e, wae, rho=RHO, sig=SIG_DEX, p=P_BTFR):
    """Marginalized sigma(beta) over a (w0,wa) prior of width (w0e,wae). bins=[(N,z),...]."""
    F = np.zeros((3,3))
    for N,z in bins:
        g = _ders(z,p); F += N*np.outer(g,g)/sig**2
    cov_p = np.array([[w0e**2, rho*w0e*wae],[rho*w0e*wae, wae**2]])
    F[1:,1:] += np.linalg.inv(cov_p)
    return np.sqrt(np.linalg.inv(F)[0,0])


def nsig(bins, w0e, wae):
    return 1.0/sigma_beta_marg(bins, w0e, wae)


print("="*100)
print("ROUTE 5 -- DESI DR3 forecast: can evolving-DE PIN a0(z), and is it decisive?")
print("="*100)

# =====================================================================================
# (A) THE GATE: DESI decides whether a distinctive test EXISTS at all
# =====================================================================================
print("\n(A) THE CONDITIONAL GATE -- does the framework HAVE a distinctive a0(z) test?")
print("-"*100)
print("  branch                         a0(z)/a0(0): z=1   z=2   z=3   z=5    distinctive content")
flat = lambda z: np.ones_like(np.atleast_1d(z)*1.0)
for label, f, note in [
    ("DE = true Lambda (w=-1)",  flat,    "VANISHES -- identical to z=0 MOND, NO beyond-MOND test"),
    ("DE evolves (DESI w0wa)",   a0_ratio,"LIVE -- declining branch, falsifiable distinctive bet"),
]:
    vals = [f(np.array([z]))[0] for z in (1,2,3,5)]
    print(f"  {label:30s}      {vals[0]:.3f} {vals[1]:.3f} {vals[2]:.3f} {vals[3]:.3f}   {note}")
# how strongly does DESI itself say "evolving" -> sets the gate probability
# current DR2: 2.8-4.2 sigma; DR3 ~1.5x tighter on w0,wa -> if signal real, sigma scales ~x1.5
print("\n  DESI's own evolving-vs-Lambda significance (this is the GATE, not an a0 measurement):")
print("    DR2 (2025): 2.8-4.2 sigma (SN-sample dependent; 3.1 sigma combined). Sign-aligned w/ declining a0.")
print("    DR3 (~2027, full 5yr survey): w0,wa errors ~1.5-1.8x tighter. IF the central w0wa holds,")
for dr2_sig, f_tight in [(3.1, 1.5), (4.2, 1.5), (3.1, 1.8), (4.2, 1.8)]:
    print(f"      DR2={dr2_sig:.1f}sig, x{f_tight} tighter -> DR3 ~{dr2_sig*f_tight:.1f} sigma evolving-DE")
print("    => DR3 can push evolving-DE to ~5-7.5 sigma IF central holds (gate OPENS, declining a0 becomes SHARP)")
print("       OR regress toward w=-1 if it was a fluctuation (gate CLOSES, distinctive content VANISHES).")
print("    HONEST: this is a real fork. DESI DR3 does NOT measure a0; it decides whether a0(z) is even non-trivial.")

# =====================================================================================
# (B) THE TRACKING TEST: a0(z) from kinematics MUST track DESI's rho_DE(z)
#     SNR marginalized over the DESI prior -- the binding term is the DE prior, not galaxy N
# =====================================================================================
print("\n(B) THE DECISIVE TRACKING TEST -- measured a0(z) vs DESI's rho_DE(z): does beta=1, !=0?")
print("-"*100)
print("  beta=1: a0 ~ sqrt(rho_DE) (framework, tracks DESI). beta=0: a0 const (MOND null, does NOT track).")
print("  The DE prior is PARTLY DEGENERATE with beta -> it sets a sigma(beta) FLOOR independent of galaxy N.")
print()
# canonical decisive survey and a two-redshift split, under DR2 vs DR3 vs perfect-DE priors
surveys = [
    ("60 discs @ z=3.5",            [(60,3.5)]),
    ("40@z3 + 25@z5 (two-z)",       [(40,3.0),(25,5.0)]),
    ("100@z3 + 100@z5 (aggressive)",[(100,3.0),(100,5.0)]),
    ("infinite data (z3 & z5)",     [(10**7,3.0),(10**7,5.0)]),
]
print(f"  {'survey':<32}{'DR2 prior':>12}{'DR3 (/1.5)':>12}{'DR3 (/1.8)':>12}{'DE perfect':>12}")
for name, bins in surveys:
    s_dr2 = nsig(bins, W0_ERR_DR2,        WA_ERR_DR2)
    s_d15 = nsig(bins, W0_ERR_DR2/1.5,    WA_ERR_DR2/1.5)
    s_d18 = nsig(bins, W0_ERR_DR2/1.8,    WA_ERR_DR2/1.8)
    s_perf= nsig(bins, 1e-6,              1e-6)
    print(f"  {name:<32}{s_dr2:>11.1f}s{s_d15:>11.1f}s{s_d18:>11.1f}s{s_perf:>11.1f}s")
print("\n  READING: the DESI prior is the BINDING term. With the DR3 (~1.5-1.8x) prior the two-z BTFR survey")
print("  reaches ~2.3-2.6 sigma (was ~1.9 at DR2); a clean >3 sigma TRACKING test needs a TIGHTER-than-DR3 DE")
print("  prior (Euclid+Rubin+CMB-S4 ~2030, or DESI+all combined) AND multi-redshift kinematics. DR3 alone")
print("  TIGHTENS but does NOT deliver the 3-sigma tracking test by itself.")

# what DE-prior tightening is REQUIRED for the canonical survey to hit 3 and 5 sigma?
print("\n  Required DE-prior tightening (vs DR2) for 40@z3+25@z5 to reach a target tracking SNR:")
bins = [(40,3.0),(25,5.0)]
print(f"  {'target':>8}{'prior factor vs DR2':>22}{'~who/when':>34}")
for tgt in (2.0, 3.0, 5.0):
    f = None
    for ff in np.linspace(1.0, 60.0, 6000):
        if nsig(bins, W0_ERR_DR2/ff, WA_ERR_DR2/ff) >= tgt:
            f = ff; break
    who = {2.0:"DR3 (~1.5-1.8x) -- reachable ~2027",
           3.0:"DESI-final + Euclid/Rubin/CMB-S4 stack ~2028-30",
           5.0:"Stage-IV DE FoM x10+ -- ~2030s, OR a beta!=0 detection from the SIGN alone"}[tgt]
    fac = "UNREACHABLE" if f is None else f"x{f:.1f}"
    print(f"  {tgt:>6.0f}s{fac:>22}{who:>34}")

# =====================================================================================
# (C) THE SIGN SHORTCUT -- the real near-term decisiveness is the SIGN, not beta-vs-DESI
# =====================================================================================
print("\n(C) THE SIGN SHORTCUT -- what is actually decidable, and when")
print("-"*100)
print("  The beta-vs-DESI tracking SNR is DE-prior-limited. But the framework's distinctive SIGN is")
print("  decidable WITHOUT a tight DE prior, because the three hypotheses differ in SIGN at z>=2:")
print(f"  {'z':>4}{'framework(decl)':>18}{'constant(MOND)':>16}{'rising(rho_tot/cH)':>20}{'V offset fw':>13}")
for z in (2.0, 3.0, 5.0):
    fw = a0_ratio(z); rise = np.sqrt(rho_DE_ratio(z, w0=-1.0, wa=0.0))  # placeholder const for shape
    Ez = np.sqrt(0.315*(1+z)**3+0.685)
    dV = (fw**0.25 - 1)*100
    print(f"  {z:>4.0f}{fw:>18.3f}{1.000:>16.3f}{Ez:>20.3f}{dV:>+12.1f}%")
print("  - rising (cH/rho_total): +large, ALREADY EXCLUDED (Milgrom (1+z)^1.5; cluster const offset; disk BTFR null)")
print("  - framework declining: V_flat ~7% LOW at z=3, ~13% low at z=5 (SIGN = negative offset)")
print("  - constant MOND: zero offset")
print("  The cleanest near-term result is the SIGN of the z>=2 deep-MOND BTFR offset (negative=framework,")
print("  zero=constant MOND, positive=rising/excluded). That needs ~30-80 CLEAN deep-MOND discs and is")
print("  SYSTEMATICS-limited (high-z baryon/gas floor ~0.1 dex vs the 0.13 dex z=3 signal), NOT DE-prior-limited.")

# =====================================================================================
# (D) TIMELINE + DECISIVENESS SUMMARY
# =====================================================================================
print("\n(D) TIMELINE + DECISIVENESS")
print("-"*100)
rows = [
 ("now (2026)", "MUSE-DARK III rising (de-syst ~1.5s AGAINST declining); DESI DR2 evolving 2.8-4.2s (sign-aligned, NOT an a0 meas)", "leaning unfavourable, non-diagnostic"),
 ("~2027 DR3", "DESI full-survey w0,wa x1.5-1.8 tighter -> evolving-DE ~5-7.5s IF central holds (GATE), OR reverts to w=-1 (VANISHES)", "gate opens/closes; tracking SNR 1.9->2.3-2.6s (still <3)"),
 ("~2028-30",  "ELT/HARMONI + ALMA: ~30-80 clean deep-MOND z=2-3.5 discs -> SIGN of BTFR offset at systematic floor", "decisive on SIGN (decl vs const) if M_b syst <0.04 dex"),
 ("~2030s",    "DESI-final + Euclid/Rubin/CMB-S4 DE stack + multi-z kinematics", "a0(z)-tracks-rho_DE(z) at >3s POSSIBLE; full distinctive test"),
]
for when, what, verdict in rows:
    print(f"  [{when:>10}] {what}")
    print(f"  {'':>13} => {verdict}\n")

print("="*100)
print("VERDICT (both ways)")
print("="*100)
print("""  CONDITIONAL BET, not a guaranteed winnable test. DESI DR3 is a GATE, not the measurement:
   - IF DR3 firms evolving-DE (>5s): the declining a0(z) becomes a SHARP, mandatory prediction
     (a0 MUST track sqrt(rho_DE)) -- the framework's distinctive content is fully LIVE and falsifiable.
   - IF DR3 reverts to w=-1: a0 is constant = z=0 MOND, the distinctive content VANISHES entirely.
   The DECISIVE test is DIRECT a0(z) from high-z kinematics cross-checked against DESI's rho_DE(z):
   the framework predicts they TRACK. A measured a0(z) NOT tracking DESI's rho_DE(z) KILLS the distinctive claim.
   But the beta-vs-DESI tracking SNR is DE-PRIOR-LIMITED: ~1.9s at DR2, ~2.3-2.6s at DR3, >3s only with a
   tighter-than-DR3 DE stack (~2030s). The near-term decidable thing is the SIGN of the z>=2 BTFR offset
   (negative=framework), systematics-limited, ELT/ALMA ~2028-30. FORBIDDEN: 'DESI confirms my a0(z)'
   (DESI measures rho_DE, not a0). HONEST current lean: UNFAVOURABLE (MUSE rising ~1.5s against), but the
   distinctive bet is real and the one cosmological tension (DESI evolving-DE) is sign-aligned.""")
