#!/usr/bin/env python3
"""
Does the Cassini Q2 QUADRUPOLE bound require an omega_c INSIDE the paper's [1.78, 2.21]e-14 rad/s band?
=======================================================================================================
ONE consistency number.  The written passive-frame MI action (MI_FIELD_THEORY_RESULTS_2026.md, Sec. 5)
survives the solar system ONLY through a gated crossover with a FREE fifth constant omega_c, quoted as

      omega_c in [1.78, 2.21]e-14 rad/s   (canonical footing a0 = 9.355e-11)
      omega_c in [1.78, 1.83]e-14 rad/s   (alt footing      a0 = 1.13e-10, knife-edge +2.7%)

Separately, reviews/cassini_quadrupole_framework.py establishes that the Desmond-Hees-Famaey 2024
(MNRAS 530,1781) -> Park+ 2026 (arXiv:2602.17884) RAR-vs-solar-quadrupole tension is 3-15 sigma and that
the framework's AeST / modified-GRAVITY realization INHERITS it (QUMOND-like quasi-static limit).

QUESTION: is the omega_c that the Q2 bound requires INSIDE that already-quoted band (one free gate buys
off BOTH solar-system constraints => consistent), or does Q2 demand a DIFFERENT omega_c (=> a REAL new
internal tension: two solar-system constraints fighting over one free parameter)?

CALIBRATION HELD THROUGHOUT (manufacture neither a win nor a deficit):
  * The passive frame (0 frame dof) is NOT claimed to kill Q2 by itself.  The paper's own ungated
    10^3-10^4x planetary exclusion proves the passive-frame structure does NOT freely evade the solar
    system.  The GATE does the work, and the gate COSTS omega_c -- which Cassini then bounds.
  * Both a0 footings are carried on every load-bearing number.
  * The LENSING sector is kept strictly separate: the disformal photon metric is GW170817-excluded by
    ~6-7 orders (paper erratum v2).  That is S_photon.  Q2 dynamics live in S_matter.  Not conflated.
  * Every adopted modelling choice is printed and labelled [ADOPTED] or [ASSUMPTION].
No TOE language.  No "theory closed".  numpy + sympy.  Exits 0.
"""
import numpy as np
import sympy as sp

# ----------------------------------------------------------------------------------------------------
# 0. CONSTANTS AND CITED ANCHORS
# ----------------------------------------------------------------------------------------------------
A0_CANON_FRAME = 9.355e-11     # framework canonical: a0 = c H_Lambda / Z = (c/2) sqrt(G rho_Lambda)
A0_ALT_FRAME   = 1.13e-10      # framework alt footing (rho_total / cH0)
A0_MCGAUGH     = 1.20e-10      # McGaugh RAR z=0 anchor -- ONLY for regression vs the existing script

V_SUN, R_SUN_KPC = 233e3, 8.2          # existing script's fiducial (Milky Way at the Sun)
KPC = 3.0857e19
G_EXT_FID = V_SUN**2 / (R_SUN_KPC * KPC)   # ~2.15e-10 m/s^2
G_EXT_LOW = 1.8e-10                        # low end of the MW-mass-model spread (sensitivity only)

# Cassini quadrupole (Park+ 2026, arXiv:2602.17884), as already used in aest_quasistatic_cassini.py
Q2_CENTRAL, Q2_SIGMA = 1.6e-27, 1.8e-27           # s^-2, 1 sigma
Q2_95 = Q2_CENTRAL + 1.645 * Q2_SIGMA             # ~4.6e-27, one-sided 95%
BOOST_BOUND_95 = 0.02                             # Q2_95 <-> <= 2% MOND boost at the solar position

YR = 365.25 * 86400.0
GM_SUN, GM_EARTH = 1.32712440018e20, 3.986004418e14
R_MOON, A_SAT = 3.844e8, 1.43353e12
T_SAT_DAYS = 10759.22                             # Saturn sidereal period (29.4571 yr)
OMEGA_SAT = 2 * np.pi / (T_SAT_DAYS * 86400.0)    # ~6.76e-9 rad/s  -- the Cassini-relevant frequency
OMEGA_GAL_SUN = V_SUN / (R_SUN_KPC * KPC)         # ~9.2e-16 rad/s  -- the Sun's own galactic orbit

# window inputs, from prep_2026/mi_planetary_falsification/window_joint.py + paper Sec. 5.2
OMEGA_GAL_MAX_DEEPMOND = 5.94e-15   # UGC05721 innermost deep-MOND orbit, binding lower edge
GATE_KEEP = 0.90                    # RAR preservation: require Re G >= 0.90 at every deep-MOND orbit
GDOT_LLR_2SIG = (5.0 + 2 * 9.6) * 1e-15   # /yr, Biskupek & Mueller 2021 (|cen| + 2 sigma) = 2.42e-14
DG_SATURN = 7.0e-15                 # Fienga & Minazzoli 2024 per-planet reactive delta_g bound
PAPER_WINDOW = {"canon": (1.78e-14, 2.21e-14), "alt": (1.78e-14, 1.83e-14)}

RULE = "=" * 102
def head(s): print("\n" + RULE + "\n" + s + "\n" + RULE)

# ----------------------------------------------------------------------------------------------------
# 1. THE GATE -- the paper's form, verbatim, with the causal identity machine-checked
# ----------------------------------------------------------------------------------------------------
def ReG(omega, wc): return 1.0 / (1.0 + (omega / wc) ** 2)
def ImG(omega, wc): return -(omega / wc) / (1.0 + (omega / wc) ** 2)
def AbsG(omega, wc): return 1.0 / np.sqrt(1.0 + (omega / wc) ** 2)

def invert_ReG(S):
    """omega/omega_c at which Re G = S  ->  omega_c = omega / x."""
    return np.sqrt(1.0 / S - 1.0)

def invert_AbsG(S):
    return np.sqrt(1.0 / S ** 2 - 1.0)

head("1.  THE GATE FORM  [taken from the paper, NOT adopted by me]")
w, wc = sp.symbols("omega omega_c", positive=True)
Gs = 1 / (1 + sp.I * w / wc)
ident = sp.simplify(sp.Abs(Gs) ** 2 - sp.re(sp.expand(sp.simplify(Gs))))
print(f"""
  Source: MI_FIELD_THEORY_RESULTS_2026.md Sec. 5.2 + prep_2026/mi_planetary_falsification/window_joint.py

      single-pole causal Debye memory relaxator   G(omega) = 1 / (1 + i omega / omega_c)
      time domain   g(t) = omega_c exp(-omega_c t) theta(t)      (retention time tau = 1/omega_c)
      Re G(omega) = 1/(1 + (omega/omega_c)^2)        <- RETAINED reactive (conservative) MI amplitude
      Im G(omega) = -(omega/omega_c)/(1+(omega/omega_c)^2)  <- dissipative lag, FORCED by causality
      MI response  K_eff = 1 - S(|a|/a0) G(omega),  S -> a0/(2 g_N) deep-Newton
      reactive anomalous accel = (a0/2) Re G(omega)   ;   secular drift d ln r/dt = a0 omega_c / g_N

  MI is ACTIVE for omega << omega_c and SUPPRESSED for omega >> omega_c (Re G -> (omega_c/omega)^2).
  sympy check of the defining 1-pole identity |G|^2 = Re G : residual = {sp.simplify(ident)}  (must be 0)

  [ADOPTED #1 -- the frequency argument]  The paper's gate is evaluated at the ORBITAL ANGULAR FREQUENCY
  of the body whose dynamics is measured.  This is not my invention: the window's LOWER edge uses
  omega_gal = V/r of the orbiting gas in SPARC galaxies (5.94e-15 = 16.5 km/s / 0.09 kpc, UGC05721) and
  the UPPER edge uses per-planet omega_p = 2pi/T_p.  I apply the SAME rule to Q2 => omega = omega_Saturn.
  This is the single load-bearing assumption of the whole calculation; Section 6 forks it both ways.
""")
assert sp.simplify(ident) == 0, "1-pole identity |G|^2 = Re G failed"

# ----------------------------------------------------------------------------------------------------
# 2. REGRESSION: RECONSTRUCT THE PAPER'S [1.78, 2.21]e-14 BAND FROM ITS TWO OBSERVABLES
#    (this both validates my gate implementation and answers "WHICH observables set the band")
# ----------------------------------------------------------------------------------------------------
head("2.  REGRESSION ANCHOR A -- rebuild the quoted omega_c band from scratch")
print(f"""
  LOWER edge  = galactic RAR preservation.  Require Re G(omega_gal) >= {GATE_KEEP} at every confirmed
                deep-MOND SPARC orbit  ->  omega_c >= k * omega_gal,max ,  k = 1/sqrt(1/{GATE_KEEP} - 1) = 3
  UPPER edge  = LUNAR LASER RANGING secular drift.  d ln r/dt = a0 omega_c / g_N(Moon) <= LLR Gdot/G
                2-sigma face value {GDOT_LLR_2SIG:.2e}/yr  (Biskupek & Mueller 2021)
  (the per-planet REACTIVE delta_g bounds are looser -- computed below for rank ordering)
""")
k_lo = 1.0 / invert_ReG(GATE_KEEP)
gN_moon = GM_EARTH / R_MOON ** 2
gN_sat = GM_SUN / A_SAT ** 2
rebuilt = {}
print(f"  {'footing':<10}{'a0':>12}{'lower edge':>14}{'upper edge (LLR)':>19}{'paper band':>26}{'match':>9}")
print("  " + "-" * 92)
for lab, a0 in [("canon", A0_CANON_FRAME), ("alt", A0_ALT_FRAME)]:
    lo = OMEGA_GAL_MAX_DEEPMOND * k_lo
    hi = (GDOT_LLR_2SIG / YR) * gN_moon / a0
    rebuilt[lab] = (lo, hi)
    plo, phi = PAPER_WINDOW[lab]
    ok = abs(lo / plo - 1) < 0.02 and abs(hi / phi - 1) < 0.02
    print(f"  {lab:<10}{a0:>12.3e}{lo:>14.3e}{hi:>19.3e}"
          f"{f'[{plo:.2e}, {phi:.2e}]':>26}{'YES' if ok else 'NO':>9}")
    assert ok, f"failed to reproduce the paper's {lab} window"
# rank the per-planet reactive ceiling for context (Re G ~ (wc/w)^2 => wc <= w sqrt(2 dg/a0))
wc_reactive_sat = OMEGA_SAT * np.sqrt(2 * DG_SATURN / A0_CANON_FRAME)
print(f"""
  Both edges reproduced to <2%.  So the [1.78, 2.21]e-14 band is set by exactly TWO observables:
  SPARC deep-MOND rotation curves (from below) and LLR Gdot/G (from above).  Neither is Q2.
  For rank ordering, the per-planet REACTIVE ceiling (Saturn, delta_g <= {DG_SATURN:.1e} m/s^2) is
  omega_c <= {wc_reactive_sat:.3e} rad/s -- already {wc_reactive_sat/rebuilt['canon'][1]:.0f}x looser than the LLR edge, as the paper says.
""")

# ----------------------------------------------------------------------------------------------------
# 3. THE UNGATED Q2 -- regression against reviews/cassini_quadrupole_framework.py
# ----------------------------------------------------------------------------------------------------
head("3.  UNGATED Q2 AT THE SOLAR POSITION -- inherited at full strength, regression anchored")
def nu_frame(y):  return np.sqrt(1.0 + 1.0 / y)                    # THE FRAMEWORK'S OWN kernel
def nu_rar(y):    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))         # McGaugh RAR (comparison only)
def nu_simple(y): return (1.0 + np.sqrt(1.0 + 4.0 / y)) / 2.0      # 'simple' nu (comparison only)

print(f"""
  [ADOPTED #2]  Ungated Q2 = the FULL inherited QUMOND-like boost.  I take the paper's own conservative
  posture (its covariant/CMB-safe realization AeST has a QUMOND-like quasi-static limit, so the Desmond
  tension transplants) rather than any "modified inertia evades it" shortcut.  Q2 is linear in the boost
  B = nu(g_ext/a0) - 1 for small B (mapping already established in reviews/aest_quasistatic_cassini.py),
  with B <= {BOOST_BOUND_95:.0%} <-> Q2_95 = {Q2_95:.2e} s^-2.  Section 7 shows what a strictly-LOCAL MI reading
  would instead give, clearly separated, and does NOT let it drive the verdict.

  g_ext = V^2/R = {G_EXT_FID:.3e} m/s^2   (V = {V_SUN/1e3:.0f} km/s, R = {R_SUN_KPC} kpc)
""")
print(f"  {'a0 [m/s^2]':<28}{'g_ext/a0':>9}{'B frame nu':>12}{'B RAR nu':>10}{'B simple':>10}"
      f"{'B/bound (frame)':>17}")
print("  " + "-" * 92)
B_ungated = {}
for lab, a0 in [("McGaugh 1.20e-10 (regr.)", A0_MCGAUGH), ("framework canon 9.355e-11", A0_CANON_FRAME),
                ("framework alt 1.13e-10", A0_ALT_FRAME)]:
    y = G_EXT_FID / a0
    bF, bR, bS = nu_frame(y) - 1, nu_rar(y) - 1, nu_simple(y) - 1
    B_ungated[lab] = dict(y=y, frame=bF, rar=bR, simple=bS)
    print(f"  {lab:<28}{y:>9.2f}{bF:>11.1%}{bR:>10.1%}{bS:>10.1%}{bF/BOOST_BOUND_95:>16.1f}x")
regr = B_ungated["McGaugh 1.20e-10 (regr.)"]
ok_rar = abs(regr["rar"] - 0.356) < 0.01 and abs(regr["simple"] - 0.400) < 0.01
frm = B_ungated["framework canon 9.355e-11"]
ok_frm = abs(frm["rar"] - 0.282) < 0.01
print(f"""
  REGRESSION vs reviews/cassini_quadrupole_framework.py:  it prints y = 1.79 / boost 35.6% (RAR),
  40.0% (simple) for McGaugh a0, and y = 2.29 / 28.2% for the framework a0.  Reproduced here:
  {regr['y']:.2f} / {regr['rar']:.1%} / {regr['simple']:.1%} and {frm['y']:.2f} / {frm['rar']:.1%}.   MATCH = {ok_rar and ok_frm}

  On the framework's OWN kernel nu = sqrt(1 + a0/g) the ungated boost is {frm['frame']:.1%} (canon) /
  {B_ungated['framework alt 1.13e-10']['frame']:.1%} (alt) -- i.e. {frm['frame']/BOOST_BOUND_95:.0f}x over the {BOOST_BOUND_95:.0%} Cassini allowance.  That ~10x
  overshoot is the order-of-magnitude stand-in for the literature's 3-15 sigma; it is MILDER than the
  28-40% obtained with McGaugh/simple nu, but it does NOT clear the bound.  Ungated Q2 FAILS. Anchor set.
""")
assert ok_rar and ok_frm, "regression against cassini_quadrupole_framework.py failed"

# ----------------------------------------------------------------------------------------------------
# 4. APPLY THE GATE AT SATURN'S ORBITAL FREQUENCY
# ----------------------------------------------------------------------------------------------------
head("4.  THE GATE AT omega_Saturn -- suppression factor and the gated Q2")
print(f"\n  omega_Saturn = 2pi / {T_SAT_DAYS:.2f} d = {OMEGA_SAT:.4e} rad/s   (T = 29.457 yr)\n")
print(f"  {'footing':<8}{'omega_c':>12}{'omega_Sat/omega_c':>19}{'Re G (retained)':>18}"
      f"{'gated B':>13}{'gated B / bound':>17}")
print("  " + "-" * 92)
gated = {}
for lab, a0 in [("canon", A0_CANON_FRAME), ("alt", A0_ALT_FRAME)]:
    B = nu_frame(G_EXT_FID / a0) - 1
    for edge, wcv in zip(("lo", "hi"), PAPER_WINDOW[lab]):
        S = ReG(OMEGA_SAT, wcv)
        gated[(lab, edge)] = (wcv, S, B * S)
        print(f"  {lab+'/'+edge:<8}{wcv:>12.3e}{OMEGA_SAT/wcv:>19.3e}{S:>18.3e}"
              f"{B*S:>13.3e}{B*S/BOOST_BOUND_95:>17.2e}")
S_hi = gated[("canon", "hi")][1]
print(f"""
  GATE SUPPRESSION FACTOR at Saturn's frequency, at the window's MOST PERMISSIVE corner
  (omega_c = 2.21e-14, canon):  Re G = {S_hi:.2e}  -- eleven orders of magnitude.
  Gated Q2 boost = {gated[('canon','hi')][2]:.2e}, i.e. {gated[('canon','hi')][2]/BOOST_BOUND_95:.1e} of the Cassini allowance.
  Equivalent Q2 = {gated[('canon','hi')][2]*Q2_95/BOOST_BOUND_95:.2e} s^-2 vs Q2_95 = {Q2_95:.2e} s^-2.
  This is NOT a free win: it is bought entirely with the free constant omega_c, whose value is postulated.
""")

# ----------------------------------------------------------------------------------------------------
# 5. INVERT -- the omega_c that Q2 REQUIRES, and the INSIDE/OUTSIDE verdict
# ----------------------------------------------------------------------------------------------------
head("5.  INVERSION -- the omega_c REQUIRED by the Cassini Q2 bound, vs [1.78, 2.21]e-14 rad/s")
print(f"""
  Solve  B_ungated * Re G(omega_Saturn, omega_c) = {BOOST_BOUND_95:.0%}  for omega_c.
  Re G = S  =>  omega_Sat/omega_c = sqrt(1/S - 1)  =>  omega_c <= omega_Sat / sqrt(1/S - 1).
  Q2 gives an UPPER ceiling on omega_c only (a bigger corner = a more open gate = more boost); it says
  nothing about the lower edge, which stays owned by SPARC RAR preservation.
""")
print(f"  {'footing':<8}{'kernel':<10}{'B_ungated':>11}{'S required':>12}"
      f"{'omega_c REQUIRED (ceiling)':>28}{'vs band top':>14}{'verdict':>10}")
print("  " + "-" * 96)
results = []
for lab, a0 in [("canon", A0_CANON_FRAME), ("alt", A0_ALT_FRAME)]:
    for kname, kf in [("frame nu", nu_frame), ("RAR nu", nu_rar), ("simple nu", nu_simple)]:
        B = kf(G_EXT_FID / a0) - 1
        S_req = BOOST_BOUND_95 / B
        wc_req = OMEGA_SAT / invert_ReG(S_req)
        top = PAPER_WINDOW[lab][1]
        factor = wc_req / top
        verdict = "INSIDE" if wc_req >= top else "OUTSIDE"
        results.append((lab, kname, B, S_req, wc_req, factor, verdict))
        print(f"  {lab:<8}{kname:<10}{B:>10.1%}{S_req:>12.3e}{wc_req:>28.3e}{factor:>13.2e}x{verdict:>10}")

# convention robustness: use |G| (amplitude) instead of Re G = |G|^2
wc_req_absG = OMEGA_SAT / invert_AbsG(BOOST_BOUND_95 / (nu_frame(G_EXT_FID / A0_CANON_FRAME) - 1))
# g_ext sensitivity
B_low = nu_frame(G_EXT_LOW / A0_CANON_FRAME) - 1
wc_req_glow = OMEGA_SAT / invert_ReG(BOOST_BOUND_95 / B_low)
canon_frame = [r for r in results if r[0] == "canon" and r[1] == "frame nu"][0]
print(f"""
  HEADLINE (canonical footing, framework's own kernel):
      omega_c REQUIRED by Cassini Q2   <=  {canon_frame[4]:.3e} rad/s
      paper's quoted band                  [1.78e-14, 2.21e-14] rad/s
      the band sits a factor {canon_frame[5]:.2e} BELOW the Q2 ceiling   ->   VERDICT = {canon_frame[6]}

  ROBUSTNESS of that verdict:
    * kernel choice (frame / RAR / simple nu):  ceiling {min(r[4] for r in results):.2e} - {max(r[4] for r in results):.2e} rad/s -- all INSIDE
    * footing (canon 9.355e-11 / alt 1.13e-10): both INSIDE (alt band top 1.83e-14, factor
      {[r for r in results if r[0]=='alt' and r[1]=='frame nu'][0][5]:.2e}x)
    * suppression convention |G| instead of Re G:  ceiling {wc_req_absG:.2e} rad/s -> still INSIDE by {wc_req_absG/2.21e-14:.1e}x
    * g_ext = 1.8e-10 instead of 2.15e-10 (MW mass-model spread): B = {B_low:.1%}, ceiling {wc_req_glow:.2e} -> INSIDE
    * a 100x TIGHTER future Cassini/ephemeris Q2 bound (0.02% not 2%): ceiling
      {OMEGA_SAT/invert_ReG(0.0002/(nu_frame(G_EXT_FID/A0_CANON_FRAME)-1)):.2e} rad/s -> STILL INSIDE by ~{OMEGA_SAT/invert_ReG(0.0002/(nu_frame(G_EXT_FID/A0_CANON_FRAME)-1))/2.21e-14:.0e}x
  The INSIDE verdict is robust to every one of these; it is NOT robust to [ADOPTED #1] -- see Section 6.

  RANKING of the solar-system ceilings on omega_c (all canon):
      LLR Gdot/G secular drift   omega_c <= {rebuilt['canon'][1]:.2e} rad/s   <-- BINDING (sets the band top)
      Saturn reactive delta_g    omega_c <= {wc_reactive_sat:.2e} rad/s   ({wc_reactive_sat/rebuilt['canon'][1]:.0f}x looser)
      Cassini Q2 quadrupole      omega_c <= {canon_frame[4]:.2e} rad/s   ({canon_frame[4]/rebuilt['canon'][1]:.0e}x looser)  <-- LOOSEST
  Q2 is the WEAKEST of the three constraints on omega_c.  It adds no new information about the corner.
  Concretely, the Q2 ceiling is NON-OPERATIVE: at omega_c = {canon_frame[4]:.2e} (tau = {1/canon_frame[4]/YR:.1f} yr) the reactive
  a0/2 tail retained at Saturn would be (a0/2) Re G = {A0_CANON_FRAME/2*ReG(OMEGA_SAT, canon_frame[4]):.2e} m/s^2, which overshoots the
  Fienga-Minazzoli Saturn bound {DG_SATURN:.1e} m/s^2 by {A0_CANON_FRAME/2*ReG(OMEGA_SAT, canon_frame[4])/DG_SATURN:.0f}x -- so that corner is already dead on ephemerides
  long before Q2 has anything to say.  Q2 never becomes the binding solar-system constraint on omega_c.
""")

# ----------------------------------------------------------------------------------------------------
# 6. THE FORK THAT FLIPS THE VERDICT -- stated at full strength, not softened
# ----------------------------------------------------------------------------------------------------
head("6.  THE FORK -- which frequency does the Q2 anomaly actually ride?  (verdict-flipping)")
S_req_c = BOOST_BOUND_95 / (nu_frame(G_EXT_FID / A0_CANON_FRAME) - 1)
wc_forkB = OMEGA_GAL_SUN / invert_ReG(S_req_c)
rar_at_forkB = ReG(OMEGA_GAL_MAX_DEEPMOND, wc_forkB)
print(f"""
  [ADOPTED #1] said: gate the Q2 anomaly at omega_Saturn, because the paper gates every other anomaly at
  the orbital frequency of the measured body.  But Q2 is not the test body's own a0/2 tail -- it is the
  EXTERNAL-FIELD-EFFECT quadrupole, sourced by g_ext, and in a modified-GRAVITY reading g_ext is a
  quasi-STATIC field in the Sun's frame.  Three readings, three different answers:

  FORK A  [the paper's own prescription, used above]  omega = omega_Saturn = {OMEGA_SAT:.2e} rad/s
          -> omega_c ceiling {canon_frame[4]:.2e} rad/s.  Band INSIDE by {canon_frame[5]:.1e}x.  CONSISTENT.

  FORK B  [g_ext rotates only with the SUN's galactic orbit]  omega = V/R = {OMEGA_GAL_SUN:.2e} rad/s
          -> omega_c ceiling {wc_forkB:.2e} rad/s, which is {PAPER_WINDOW['canon'][0]/wc_forkB:.0f}x BELOW the band's LOWER
          edge (1.78e-14) => OUTSIDE => CONFLICT.  And it is worse than merely outside: at
          omega_c = {wc_forkB:.2e} the retained galactic boost at the binding deep-MOND orbit is
          Re G = {rar_at_forkB:.2e} -- i.e. that corner is RAR-DEAD, exactly the disease the paper's own
          forced corner a0/2c has.  Under Fork B, no omega_c reconciles Q2 with the rotation curves.

  FORK C  [the quadrupole is a genuinely STATIC / secular field]  omega -> 0
          -> Re G(0) = 1 for EVERY omega_c.  A low-pass gate cannot suppress a DC anomaly at any corner.
          Under Fork C the inherited ~{nu_frame(G_EXT_FID/A0_CANON_FRAME)-1:.0%} boost stands undiminished, {(nu_frame(G_EXT_FID/A0_CANON_FRAME)-1)/BOOST_BOUND_95:.0f}x over the bound,
          and Q2 is a constraint the free gate does NOT buy off -- omega_c-UNFIXABLE, not re-tunable.

  This fork is NOT resolvable from the written action as it stands.  It is the same missing computation
  both source documents already flag: AeST's / the MI action's quasi-static weak-field limit worked out
  in detail.  Fork A is the internally consistent one (same rule as every other gated bound in Sec. 5);
  Forks B and C are the honest exposures.  Reporting only Fork A would be a manufactured save.
""")

# ----------------------------------------------------------------------------------------------------
# 7. SECONDARY (NOT the verdict): what a strictly-LOCAL MI response would give ungated
# ----------------------------------------------------------------------------------------------------
head("7.  SECONDARY, EXPLICITLY NOT THE VERDICT -- the strictly-local MI residue, ungated")
# deep-Newton: delta_a = (a0/2) a_hat, a = g_N n + g_ext e.  Orbit-averaging the anisotropic piece:
#   <delta_a> = (a0/2)(g_ext/g_N)(1 - 1/2) e = a0 g_ext r^2 / (4 GM) e   -> gradient a0 g_ext r/(2 GM)
print(f"""
  If the MI anomaly is strictly LOCAL in the test body's own acceleration (no propagating field), then
  with a = g_N n + g_ext e and nu - 1 -> a0/(2|a|), the orbit-averaged DC anisotropic residue is
      <delta_a> = (a0 g_ext / 4 g_N) e = a0 g_ext r^2 / (4 GM) e ,  gradient  Q2_loc ~ a0 g_ext r / (2 GM)
  which is suppressed relative to the a0/2 tail by g_ext/g_N = {G_EXT_FID/gN_sat:.2e} at Saturn:
""")
for lab, a0 in [("canon", A0_CANON_FRAME), ("alt", A0_ALT_FRAME)]:
    q2loc = a0 * G_EXT_FID * A_SAT / (2 * GM_SUN)
    print(f"    {lab:<7} Q2_local ~ {q2loc:.2e} s^-2   vs Cassini Q2_95 = {Q2_95:.2e} s^-2"
          f"   -> {Q2_95/q2loc:.0f}x BELOW the bound, UNGATED")
print(f"""
  [ASSUMPTION, and DELIBERATELY NOT USED FOR THE VERDICT]  This is an order-of-magnitude
  gradient-of-DC-residue estimate, not the ephemeris Q2 integral, and it IS the "modified inertia evades
  it" escape that BOTH source documents explicitly decline to grant (the framework's covariant realization
  is QUMOND-like; its quasi-static limit is UNCOMPUTED).  It also cannot be squared with the paper's own
  ungated 10^3-10^4x planetary exclusion, which proves locality/passive-frame structure does NOT by itself
  clear the solar system.  Recorded as a third door, given no weight in the verdict until the quasi-static limit
  is actually computed.  Weight given to it in Section 8: ZERO.
""")

# ----------------------------------------------------------------------------------------------------
# 8. VERDICT
# ----------------------------------------------------------------------------------------------------
head("8.  VERDICT")
print(f"""
  omega_c REQUIRED by the Cassini Q2 quadrupole (Fork A, canon footing, framework's own kernel):
        omega_c <= {canon_frame[4]:.2e} rad/s      (alt footing: <= {[r for r in results if r[0]=='alt' and r[1]=='frame nu'][0][4]:.2e} rad/s)

  Paper's already-quoted band:  [1.78, 2.21]e-14 rad/s (canon) / [1.78, 1.83]e-14 (alt)

  ==> INSIDE.  The band sits ~{canon_frame[5]:.0e}x below the Q2 ceiling (canon); ~{[r for r in results if r[0]=='alt' and r[1]=='frame nu'][0][5]:.0e}x (alt).
      Gate suppression at omega_Saturn at the band's most permissive corner: Re G = {S_hi:.1e}.
      Gated Q2 boost = {gated[('canon','hi')][2]:.1e} vs the {BOOST_BOUND_95:.0%} allowance.

  HONEST VERDICT:  SURVIVES-via-free-gate, CONSISTENTLY.
      * The single free fifth constant omega_c accommodates the Q2 quadrupole AND the per-planet /
        LLR bounds simultaneously.  NO new internal tension between the two solar-system constraints.
      * NOT "evaded", NOT "threat dead", NOT a win.  Q2 does not shrink the window because Q2 is the
        LOOSEST of the three solar-system ceilings on omega_c ({canon_frame[4]/rebuilt['canon'][1]:.0e}x looser than the binding LLR drift).
        The band's edges remain owned by SPARC deep-MOND RAR preservation and LLR Gdot/G.
      * The survival is PAID FOR with a postulated constant.  The paper's own Sec. 5.3 shows omega_c is
        forced by no scale in the theory (its own corner a0/2c = 1.56e-19 rad/s is 5 orders low and
        RAR-dead).  Consistency here does not upgrade omega_c from postulate to prediction.
      * The alt footing's +2.7% knife-edge is untouched by Q2 -- neither relieved nor worsened.

  WHAT WOULD FLIP IT (Section 6, at full strength):  if the EFE quadrupole rides the Sun's galactic
  frequency (Fork B) the required corner is {PAPER_WINDOW['canon'][0]/wc_forkB:.0f}x below the band's lower edge and RAR-dead;
  if it is genuinely static (Fork C) no omega_c suppresses it at all and the inherited ~{nu_frame(G_EXT_FID/A0_CANON_FRAME)-1:.0%} boost stands.
  Both are live until the MI action's quasi-static weak-field limit is computed.  That computation, not
  this one, decides whether Q2 is bought off.

  SCOPE:  dynamics sector (S_matter) only.  The lensing sector's disformal photon metric is separately
  GW170817-excluded by ~6-7 orders (paper erratum v2) and is NOT part of this result.  No claim that any
  door is closed; no claim about the framework beyond this one consistency number.
""")
print(RULE)
print("mi_cassini_q2_omegac_2026.py: all regressions passed (window rebuild <2%, existing-script match).")
print(RULE)
