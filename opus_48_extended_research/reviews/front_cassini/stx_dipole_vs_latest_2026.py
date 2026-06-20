#!/usr/bin/env python3
r"""
FRONT A (Cassini / planetary-ephemeris) — the framework-DISTINCTIVE near-term SME test.

JOB (COMPUTE phase of workflow front-cassini-stx):
  (1) Pin the EXACT s^TX boost-dipole prediction (magnitude + SIGN + which projection).
  (2) Margin vs the LATEST tightest 2024-2026 bound — is it still "~9.6x" or has data moved it?
  (3) Re-derive the CPT-even-ONLY theorem bite (k_AF=0 at ~150x the photon bound).
  (4) Quantify the 0.12% CMB-dipole inertia anisotropy at a~a0 as a DISTINCT (cleaner?) test.

FOOTING (banked, quarantined):
  - a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2  -- the framework's OWN value, INPUT. NOT derived here.
  - Modified inertia (dS-Unruh): m_inertial -> m*mu_fw(|a|/a0), mu_fw(x)=1 - 1/(2x) + 1/(8x^2) - ...
      so the fractional deviation from the Lorentz-invariant mass is  -a0/(2|a|)  along u^mu (cosmic rest frame).
  - PROVEN preferred-frame (covariant Cassini-safe-lensing NO-GO) => an SME background.
  - Induced gravity-sector spurion (banked S_TENSOR ledger w5k0n9hd0):
        s_bar^{mu nu} = (a0 / 2|a|) * ( u^mu u^nu )_traceless         (CPT-even, two-u, universal/WEP-exact)
    In the Sun-centered celestial frame the cosmic rest frame moves at the CMB boost beta_cmb along the
    CMB-apex direction n_hat; the SME components are then organized by powers of beta_cmb:
        s^TT  = (3/4) A           O(1)   isotropic   ABSORBABLE (Bailey-Kostelecky gr-qc/0603030)
        s^TJ  = A * beta * n_J    O(beta)  DIPOLE     <-- leading observable; s^TX dominates (|n_X|~0.97)
        s^<JK>= A * beta^2 ...    O(beta^2) quadrupole  doubly suppressed
        trace = 0 exactly
    with  A = a0/(2|a|).  There is NO O(1) un-beta-suppressed anisotropic observable (SO(3)-irrep +
    trajectory-independence => all direction inherited from u^mu).

BOTH-WAYS DISCIPLINE (Carl #1): we report the margin against the GENUINELY TIGHTEST published bound
(combined global fit, 1.3e-9) AND the looser planetary-ephemeris-only bound (8.3e-9, the source of the
banked "9.6x"), at EVERY body's acceleration (the conservative worst-case Saturn AND the realistic
inner-planet weighting). We surface the full spread, never a single cherry-picked corner.

LATEST BOUNDS (PULL #1, verified from primary PDFs this session):
  Kostelecky-Russell, "Data Tables for Lorentz and CPT Violation," arXiv:0801.0287 v19 (2026-02-09):
    sbar^TX = (-0.1 +/- 1.3)e-9   COMBINED global fit  [ref 364 = Hees et al 2016, arXiv:1610.04682 Tab.9]  <- TIGHTEST
    sbar^TY = ( 0.4 +/- 2.3)e-9   combined
    sbar^TZ = (-0.6 +/- 5.5)e-9   combined
    sbar^TX < 2.9e-9  pulsar-ONLY  [ref 358 = Dong, Wang & Shao 2024, arXiv:2311.11038, PRD 109 084024]  <- NEW post-banked
    sbar^TX in (-5.2,5.3)e-9 binary pulsars [369]; (-0.9 +/- 1.0)e-8 LLR [365]
    INPOP planetary-ephemeris-ONLY: (-2.9 +/- 8.3)e-9  [Hees 2016 Tab.4]  <- the OLD banked "conservative" baseline
    spatial s^JK (tighter, NOT this channel): |s^XZ|<5.6e-12 pulsars; s^XY~6.5e-12; s^XX-s^YY~1.9e-11
  alpha-PPN (INPOP/EPM): alpha1 <~ 2e-6, alpha2 <~ 4e-6 (weak-field, directly applicable)
    Nordtvedt solar-spin alpha2 <~ 2.4e-7.
  No INPOP21a/EPM2021/BepiColombo SME s^TX fit beating 1.3e-9 has been published (BepiColombo Mercury
    orbit insertion delayed to Nov-2026, thruster issue -> s^TX tightening lands post-2026, consistent
    with the framework's own ~2028-32 analysis-limited timeline).
"""
import mpmath as mp
import sympy as sp
mp.mp.dps = 30

print("#"*96)
print("# FRONT A — s^TX boost dipole, EXACT prediction + margin vs LATEST 2024-2026 bounds")
print("#"*96)

# ============================================================================
# 0. SYMBOLIC — confirm the dipole formula, its leading order, and the trace=0 / no-O(1)-anisotropy
# ============================================================================
print("\n[0] SYMBOLIC structure of the induced s_bar^{mu nu}")
a0_s, a_s, beta_s = sp.symbols('a0 a beta', positive=True)
nT, nX, nY, nZ = sp.symbols('n_T n_X n_Y n_Z', real=True)   # boosted u^mu components (n_T~gamma, n_J~gamma*beta*n_J)
A = a0_s/(2*a_s)
gamma = 1/sp.sqrt(1-beta_s**2)
# u^mu in the SCF: u^T = gamma, u^J = gamma*beta*nhat_J  (cosmic rest frame boosted by the CMB velocity)
uT = gamma
uX = gamma*beta_s*nX; uY = gamma*beta_s*nY; uZ = gamma*beta_s*nZ
# s_bar^{mu nu} = A*(u^mu u^nu - (1/4) eta^{mu nu} (u.u)); with mostly-minus eta, u.u = +1 for timelike unit u
# Use traceless symmetric part: s^{mu nu} = A*(u^mu u^nu - 1/4 eta^{mu nu})
eta = sp.diag(1,-1,-1,-1)
u = sp.Matrix([uT,uX,uY,uZ])
S = sp.zeros(4,4)
for i in range(4):
    for j in range(4):
        S[i,j] = A*(u[i]*u[j] - sp.Rational(1,4)*eta[i,j])
# trace with eta (s^mu_mu = eta_{mu nu} s^{mu nu})
tr = sp.simplify(sum(eta[i,i]*S[i,i] for i in range(4)))
print("    u.u (should be +1):", sp.simplify(uT**2 - (uX**2+uY**2+uZ**2)).subs(nX**2+nY**2+nZ**2,1))
print("    trace eta_{mu nu} s^{mu nu} =", sp.simplify(tr.subs(nX**2+nY**2+nZ**2,1)), "  (=> traceless, as required)")
sTT = sp.series(S[0,0], beta_s, 0, 3).removeO()
sTX = sp.series(S[0,1], beta_s, 0, 3).removeO()
sXXmYY = sp.series(S[1,1]-S[2,2], beta_s, 0, 3).removeO()
print("    s^TT   (series in beta) =", sp.simplify(sTT), "   -> O(1) isotropic 3A/4, ABSORBABLE")
print("    s^TX   (series in beta) =", sp.simplify(sTX), "   -> O(beta) DIPOLE  = A*beta*n_X  (leading observable)")
print("    s^XX-YY(series in beta) =", sp.simplify(sXXmYY), "   -> O(beta^2) quadrupole (doubly suppressed)")
print("    => leading-order s^TX = A * beta * n_X  with A=a0/(2|a|); CONFIRMS the banked dipole formula.")

# ============================================================================
# 1. CONSTANTS + the CMB-apex projection
# ============================================================================
print("\n[1] Constants + CMB-apex projection n_X")
a0      = mp.mpf('9.36e-11')                 # framework a0 (INPUT, quarantined)
c_ms    = mp.mpf('299792458')
v_cmb   = mp.mpf('369820')                   # m/s  (Planck 2018 solar-system CMB dipole 369.82 km/s)
beta    = v_cmb/c_ms                          # 1.2336e-3
# CMB dipole apex (Galactic l=264.021, b=48.253; equatorial RA=167.942 Dec=-6.944 J2000)
RA      = mp.radians(mp.mpf('167.942'))
Dec     = mp.radians(mp.mpf('-6.944'))
nX_v    = mp.cos(Dec)*mp.cos(RA)
nY_v    = mp.cos(Dec)*mp.sin(RA)
nZ_v    = mp.sin(Dec)
gam2    = 1/(1-beta**2)
print(f"    a0 (INPUT)   = {mp.nstr(a0,4)} m/s^2")
print(f"    beta_cmb     = v_cmb/c = {mp.nstr(beta,6)}   (0.1234%)")
print(f"    CMB apex n_X = {mp.nstr(nX_v,4)},  n_Y = {mp.nstr(nY_v,4)},  n_Z = {mp.nstr(nZ_v,4)}")
print(f"    gamma^2-1    = {mp.nstr(gam2-1,4)}  (+{mp.nstr(100*(gam2-1),3)}% — utterly negligible)")
print(f"    => |n_X|~0.96 dominant; s^TX is the LARGEST of the three s^TJ. SIGN: n_X<0 => s^TX<0.")

# ============================================================================
# 2. PER-BODY accelerations and the s^TX prediction
# ============================================================================
print("\n[2] Per-body |a| = GM_sun/r^2 and the predicted s^TX = (a0/2|a|)*beta*n_X")
GM_sun = mp.mpf('1.32712440018e20')
AU     = mp.mpf('1.495978707e11')
bodies = [('Mercury', mp.mpf('0.387098')),
          ('Venus',   mp.mpf('0.723332')),
          ('Earth',   mp.mpf('1.000000')),
          ('Mars',    mp.mpf('1.523679')),
          ('Jupiter', mp.mpf('5.2044')),
          ('Saturn',  mp.mpf('9.5826'))]   # Saturn = Cassini tracking point (lowest-a well-tracked)
def accel(a_AU):  return GM_sun/(a_AU*AU)**2
def sTX_pred(a):  return (a0/(2*a))*gam2*beta*nX_v   # SIGNED (n_X<0 => negative)

# ============================================================================
# 3. MARGINS vs every latest bound
# ============================================================================
bounds = {
    'combined_1.3e-9  (Hees16 Tab9, TIGHTEST published)': mp.mpf('1.3e-9'),
    'pulsar_2.9e-9    (Dong24, NEW post-banked)'        : mp.mpf('2.9e-9'),
    'binarypulsar_5.25e-9 (Hees16 Tab6)'                : mp.mpf('5.25e-9'),
    'INPOP_8.3e-9     (Hees16 Tab4, OLD banked base)'   : mp.mpf('8.3e-9'),
    'LLR_1.0e-8       (Hees16 Tab3)'                    : mp.mpf('1.0e-8'),
}
print("\n    Predicted |s^TX| per body (signed s^TX<0):")
print("    " + "-"*88)
print(f"    {'body':8s}{'a [m/s2]':>12s}{'A=a0/2a':>12s}{'|s^TX|':>12s}"
      f"{'margin/comb':>13s}{'margin/INPOP':>14s}")
print("    " + "-"*88)
rows = {}
for name,a_AU in bodies:
    a = accel(a_AU); A_v = a0/(2*a); s = sTX_pred(a); sa = abs(s)
    rows[name] = (a, sa)
    mc = mp.mpf('1.3e-9')/sa; mi = mp.mpf('8.3e-9')/sa
    print(f"    {name:8s}{mp.nstr(a,3):>12s}{mp.nstr(A_v,3):>12s}{mp.nstr(sa,3):>12s}"
          f"{mp.nstr(mc,3):>13s}{mp.nstr(mi,4):>14s}")
print("    " + "-"*88)

print("\n[3] FULL margin ledger — Saturn (conservative worst-case body) vs every bound:")
sat_a, sat_s = rows['Saturn']
for label, b in bounds.items():
    print(f"    Saturn |s^TX|={mp.nstr(sat_s,3)}  vs {label:48s}  margin = {mp.nstr(b/sat_s,3)}x"
          f"  ({mp.nstr(sat_s/b,3)} sigma inside)")

print("\n    Realistic inner-planet weighting (ephemeris s^TX is set by the best-ranged inner planets):")
for nm in ['Mercury','Venus','Earth','Mars']:
    a_, s_ = rows[nm]
    print(f"    {nm:8s} |s^TX|={mp.nstr(s_,3)}  vs combined 1.3e-9 -> {mp.nstr(mp.mpf('1.3e-9')/s_,4)}x"
          f"   vs INPOP 8.3e-9 -> {mp.nstr(mp.mpf('8.3e-9')/s_,4)}x")

# ============================================================================
# 4. BOTH-WAYS verdict on the headline number
# ============================================================================
print("\n[4] BOTH-WAYS on the '~9.6x' headline (Carl #1 rule):")
m_sat_comb = mp.mpf('1.3e-9')/sat_s
m_sat_inpop = mp.mpf('8.3e-9')/sat_s
m_merc_comb = mp.mpf('1.3e-9')/rows['Mercury'][1]
print(f"    WAY 1 (tighter/righter bound shrinks it): the TIGHTEST published s^TX is the COMBINED")
print(f"      global fit at 1.3e-9, NOT the INPOP-only 8.3e-9 the banked '9.6x' used. At Saturn's")
print(f"      acceleration the margin is {mp.nstr(m_sat_comb,3)}x — the banked 9.6x is NOT robust to the")
print(f"      correct (tightest) bound; the Saturn corner sits only ~{mp.nstr(m_sat_comb,2)}x = {mp.nstr(sat_s/mp.mpf('1.3e-9'),2)} sigma inside.")
print(f"    WAY 2 (right body weighting loosens it): Saturn (a={mp.nstr(sat_a,2)}) is the LOWEST-a body =>")
print(f"      largest A=a0/2a => worst case. A real ephemeris s^TX is dominated by the best-ranged inner")
print(f"      planets (Mercury via MESSENGER, Mars via MRO); at Mercury's a the margin is {mp.nstr(m_merc_comb,4)}x")
print(f"      even vs the tightest bound.")
print(f"    HONEST NET: predicted |s^TX| spans {mp.nstr(rows['Mercury'][1],3)} (Mercury-a) to {mp.nstr(sat_s,3)} (Saturn-a).")
print(f"      Binding worst corner (Saturn-a x combined-bound) ~{mp.nstr(m_sat_comb,2)}x; typical margin tens-to-hundreds.")
print(f"      => LIVE/falsifiable (binds within ~1 order in the worst corner), NOT excluded, NOT comfortably safe.")
print(f"      No 2024-2026 result moved the binding combined bound (still 1.3e-9 from Hees 2016).")

# ============================================================================
# 5. CPT-EVEN-ONLY THEOREM BITE — re-derive k_AF=0 at ~150x the photon bound
# ============================================================================
# ----------------------------------------------------------------------------
# 4b. ADVERSARIAL both-ways: the SPATIAL quadrupole channel at Saturn-a (a correction to the banked ledger)
# ----------------------------------------------------------------------------
print("\n[4b] Spatial s^JK quadrupole channel vs the TIGHTER spatial bounds (both-ways correction):")
print("     The banked S_TENSOR ledger said the O(beta^2) quadrupole clears the spatial bound by '>10^3x'")
print("     — but that used LAB g. At SATURN's acceleration (the binding body) A=a0/2a is ~10^5 larger:")
for nm in ['Earth','Mars','Jupiter','Saturn']:
    a_, _ = rows[nm]; A_ = a0/(2*a_)
    sXXmYY = A_*beta**2*(nX_v**2-nY_v**2)
    sXZ    = A_*beta**2*nX_v*nZ_v
    print(f"     {nm:8s} s^XX-YY={mp.nstr(abs(sXXmYY),3)} (vs 1.9e-11 -> {mp.nstr(mp.mpf('1.9e-11')/abs(sXXmYY),3)}x)"
          f"   s^XZ={mp.nstr(abs(sXZ),3)} (vs pulsar 5.6e-12 -> {mp.nstr(mp.mpf('5.6e-12')/abs(sXZ),4)}x)")
print("     => at Saturn-a the spatial quadrupole is ~19-43x (NOT >1000x). It is a REAL constraint, but the")
print("        DIPOLE channel (~1.5x) remains the BINDING one. CORRECTION (constraining direction): the banked")
print("        '>10^3x clears the spatial channel' is a lab-g artifact; at the binding body it is tens-x.")

print("\n[5] CPT-even-ONLY theorem: where does k_AF=0 BITE?")
hbar = mp.mpf('1.054571817e-34')   # J s
H0_kms_Mpc = mp.mpf('67.4')        # Planck 2018
Mpc = mp.mpf('3.0856775814913673e22')
eV = mp.mpf('1.602176634e-19'); GeV = eV*mp.mpf('1e9')
H0 = H0_kms_Mpc*1000/Mpc
hbarH0_GeV = (hbar*H0)/GeV
kAF_bound = mp.mpf('1e-44')        # photon CFJ k_AF bound (GeV), the tightest CPT-odd bound in physics
print(f"    The dS-Unruh kernel T_eff = sqrt(a_mu a^mu + (cH)^2) is a SCALAR, EVEN in u (two u's).")
print(f"    CPT-parity = index count (Kostelecky hep-th/0312310): even-index => CPT-EVEN c_munu/s_munu;")
print(f"    the CPT-ODD one-u coefficients a_mu, b_mu, k_AF are FORCED to zero (any bare a_mu ~ d_mu(scalar)")
print(f"    is a gradient, removable by a spinor phase; Kostelecky eq.21 a_mu - d_mu phi = 0 identically).")
print(f"    The natural cosmic-frame LV scale is hbar*H0 = {mp.nstr(hbarH0_GeV,4)} GeV.")
print(f"    Tightest CPT-odd bound (photon CFJ k_AF) = {mp.nstr(kAF_bound,2)} GeV.")
print(f"    RATIO hbar*H0 / k_AF_bound = {mp.nstr(hbarH0_GeV/kAF_bound,4)}x")
print(f"    => a CPT-ODD realization at the framework's OWN scale would ALREADY BE FALSIFIED by ~{mp.nstr(hbarH0_GeV/kAF_bound,3)}x.")
print(f"    The framework survives ONLY because its coupling is CPT-EVEN by structure (not by tuning).")
print(f"    This is a genuine falsifiable theorem: the framework predicts k_AF = b_mu = a_mu = 0 EXACTLY,")
print(f"    against the tightest CPT bounds (photon 1e-44, neutron b~1e-33, electron b~1e-31 GeV).")

# ============================================================================
# 6. THE 0.12% CMB-DIPOLE INERTIA ANISOTROPY at a~a0 — a DISTINCT (cleaner?) test
# ============================================================================
print("\n[6] DISTINCTIVE door: the 0.12% CMB-dipole inertia anisotropy at a~a0")
print("    Mechanism: at a ~ a0, mu_fw deviates from 1 by O(1) (deep-MOND), and the boost of the local")
print("    inertia tensor relative to the cosmic rest frame is O(beta_cmb)=0.12% — UN-beta-suppressed")
print("    relative to the deep-MOND O(1) signal (the suppression that protects the SOLAR-system s^TX is")
print("    GONE here because the leading effect itself is O(1), not O(a0/|a|)).")
print(f"    Fractional anisotropy amplitude  = beta_cmb = {mp.nstr(beta,4)} = {mp.nstr(100*beta,3)}%")
print( "    WHERE it shows: galaxy outskirts / dwarf-galaxy / tidal-stream dynamics at a<=a0, MODULATED")
print( "    by the angle between the local acceleration and the CMB apex (RA=167.9, Dec=-6.9). The rotation")
print( "    curve / velocity dispersion at fixed a~a0 should differ by ~0.12% between systems whose")
print( "    acceleration points TOWARD vs AWAY from the CMB apex (a dipole on the sky locked to the CMB).")
print( "    WHY cleaner in principle: it is the framework-DISTINCTIVE content (modified INERTIA's preferred")
print( "    frame), it is NOT a0/|a|-suppressed (it is the O(1) deep-MOND regime times beta_cmb), and it has")
print( "    a FIXED sky direction (the CMB apex) — a template the solar-system s^TX cannot mimic.")
print( "    WHY hard: 0.12% is far below current rotation-curve/dispersion systematics (distance, M/L,")
print( "    inclination, non-circular motions all >>0.12%); needs a large statistical sample binned by")
print( "    apex-angle to beat down systematics. NO current instrument resolves it on a single system.")
# crude statistical-reach estimate: to detect a 0.12% dipole at 3-sigma against per-system scatter sigma_sys,
# need N ~ (3 * sigma_sys / 0.12%)^2 systems (dipole fit, half the sky each lobe)
for sig in [mp.mpf('0.05'), mp.mpf('0.10'), mp.mpf('0.20')]:
    N = (3*sig/(beta))**2
    print(f"    reach: per-system frac scatter {mp.nstr(100*sig,2)}% -> N ~ {mp.nstr(N,2)} systems for a 3-sigma dipole")
print("    => SHARPER in DISTINCTIVENESS (un-beta-suppressed, framework-unique, fixed CMB direction),")
print("       but FARTHER from current sensitivity than the planetary s^TX (which is ~1.5x at the corner).")
print("       The planetary s^TX is the nearer-term LIVE test; the CMB-dipole anisotropy is the cleaner")
print("       in-principle DISCRIMINATOR (no LCDM/MOND-of-the-other-sign mimic) but data-farther.")

# ============================================================================
# 7. DECISIVE test + timeline
# ============================================================================
print("\n[7] DECISIVE test + timeline")
print("    NEAR-TERM LIVE: the planetary-ephemeris/Cassini s^TX boost dipole. Binding corner ~1.5x")
print("      (Saturn-a x combined 1.3e-9). DECIDED by a next-generation s^TX fit reaching ~1e-9 -> ~1e-10")
print("      with: (i) full Cassini Grand-Finale + extended INPOP/EPM ranging, (ii) BepiColombo Mercury")
print("      ranging AFTER orbit insertion (delayed to Nov-2026; SME s^TX fit lands ~2028-32 analysis-")
print("      limited), (iii) Mars-orbiter + MSP-timing-array growth (Dong24 pulsar-only already 2.9e-9).")
print("      A factor ~10 improvement to ~1.3e-10 would CONFRONT the Saturn-a prediction 8.7e-10 head-on.")
print("    DISTINCTIVE (cleaner, farther): the 0.12% CMB-apex dipole in deep-MOND (a<=a0) galaxy/stream")
print("      kinematics — needs ~1e3-1e4 well-measured low-a systems binned by apex angle (e.g. a future")
print("      wide deep IFU/astrometry survey). This is the ONLY test of the framework-DISTINCTIVE content;")
print("      the planetary s^TX tests only a beta-suppressed PROJECTION shared with any preferred-frame EFT.")
print("\n    STATUS: LIVE / FALSIFIABLE. Not falsified by any current bound; not comfortably safe (the")
print("    Saturn-a x tightest-bound corner is ~1.5x). Data-gated: the decisive planetary improvement is")
print("    ~2028-32 analysis-limited; the distinctive CMB-dipole test awaits a large low-a kinematic sample.")
print("\n    QUARANTINE: every number above takes a0=9.36e-11 as INPUT. a0/Z/kappa are NOT derived here.")
