"""
COLOR-CHANNEL LEPTON-SELECTOR  (Task C, the cross-fermion wall)
================================================================
THE GAP the prior 6 hammers did NOT close:
  All prior color tests used color as a *cancelling overall multiplicity*
  (w_i = N_c, uniform across generations -> cancels in the Q-ratio, the
   closed door) OR as a *per-state degeneracy that is generation-uniform*.

  This script tests the genuinely-NEW object from the wave-1 per-irrep vs
  per-state distinction, applied to COLOR:
    - a per-STATE measure counts each color a separate microstate
      (g_c = N_c states per quark generation) -> the thermal/Plancherel DEFAULT
    - a per-CHANNEL/per-IRREP measure counts color as a CHANNEL multiplicity
      g_c that enters the family-gauge / dS-Unruh PARTITION differently.

  THE CLAIM TO TEST (both-ways, ruthlessly):
    Could a color-channel weight make leptons land at channel-equipartition
    (|singlet|^2 = |doublet|^2, i.e. r=sqrt2, Koide) while pushing quarks OFF,
    WITHOUT the weight being hand-tuned to do exactly that?

KEY ALGEBRA we must respect (sympy-exact, reproduced below):
    Q = 1/3 + r^2/6, where r = |doublet-projection|/|singlet-projection| of
    the sqrt-mass vector under the S3 1+2 decomposition. Q=2/3 <=> r=sqrt2.
    A measure that multiplies the WHOLE sqrt-mass vector by an overall
    color factor leaves r (a RATIO of projections of the SAME vector)
    UNCHANGED -> cancels. To move r, the weight must act DIFFERENTLY on the
    singlet channel vs the doublet channel (asymmetric per-channel weight).

  So the ONLY way color can be a selector is if it reweights the
  SINGLET channel relative to the DOUBLET channel. We test whether any
  NATURAL color-channel assignment does this, and whether the lepton
  outcome (r=sqrt2) is FORCED or TUNED.

DISCIPLINE: any weight whose definition references 2/3 / r=sqrt2 / 45deg
is circular -> DEAD. The weight must be defined from color reps ALONE.

mpmath dps>=40 ; real S3 character theory.
"""
import mpmath as mp
from mpmath import mpf, sqrt, matrix
mp.mp.dps = 50

# =====================================================================
# 0. PDG masses, the exact Q(r) relation, and the S3 1+2 projection.
# =====================================================================
m_e   = mpf('0.51099895000'); m_mu = mpf('105.6583755'); m_tau = mpf('1776.86')
mu_u = mpf('2.16'); mu_c = mpf('1270.0'); mu_t = mpf('172570.0')
md_d = mpf('4.67'); md_s = mpf('93.4');  md_b = mpf('4180.0')

def koide_Q(ms):
    return sum(ms)/sum(sqrt(m) for m in ms)**2

# S3 1+2 decomposition of a 3-vector v=(v1,v2,v3):
#   singlet (democratic) axis  s_hat = (1,1,1)/sqrt3
#   doublet (standard) plane    = orthogonal complement
# projection amplitudes (geometric):
#   a_sing = v . s_hat
#   a_doub = |v - (v.s_hat) s_hat|
# RELATION to the circulant Koide amplitude r_circ (sqrt(m_i)=M(1+r_circ cos(...))):
#   g := a_doub/a_sing = r_circ / sqrt2   (verified sympy/mpmath-exact).
# Koide Q = 1/3 + r_circ^2/6 = 1/3 + g^2/3.
#   Koide point Q=2/3  <=>  r_circ=sqrt2  <=>  g=1 (EQUAL singlet & doublet
#   geometric amplitude = per-irrep equipartition). This is the natural
#   per-CHANNEL coordinate: g=1 means |singlet channel| = |doublet channel|.
def projections(v):
    s_hat = matrix([mpf(1),mpf(1),mpf(1)]) / sqrt(3)
    a_sing = sum(v[i]*s_hat[i] for i in range(3))
    proj = [v[i] - a_sing*s_hat[i] for i in range(3)]
    a_doub = sqrt(sum(p**2 for p in proj))
    return a_sing, a_doub

def g_and_Q_from_sqrtmass(ms):
    v = [sqrt(m) for m in ms]
    a_s, a_d = projections(v)
    g = a_d/a_s                    # = r_circ/sqrt2 ; Koide <=> g=1
    Q = mpf(1)/3 + g**2/3
    return g, Q

print("="*72)
print("0. BASELINE: g=a_doub/a_sing (=r_circ/sqrt2), Q per sector. Koide <=> g=1")
print("="*72)
for name, ms in [('charged_leptons',[m_e,m_mu,m_tau]),
                 ('up_quarks',[mu_u,mu_c,mu_t]),
                 ('down_quarks',[md_d,md_s,md_b])]:
    g,Q = g_and_Q_from_sqrtmass(ms)
    print(f"  {name:16s}  g={mp.nstr(g,8):11s} (Koide g=1) "
          f" Q={mp.nstr(Q,8):11s}  Q_direct={mp.nstr(koide_Q(ms),8)}")
print(f"  Koide target: g=1 (|singlet|=|doublet| channel amplitude), Q=2/3={mp.nstr(mpf(2)/3,8)}")
print("  (leptons hit g=1 = per-channel equipartition; quarks do not. Goal: a")
print("   color weight that moves quark g OFF 1 while LEAVING lepton g AT 1.)\n")

# =====================================================================
# 1. THE OVERALL-FACTOR CANCELLATION (the closed door, re-proven exact).
#    An overall color weight w (same for all 3 generations AND both channels)
#    multiplies v -> w*v. Both a_sing and a_doub scale by w. g unchanged.
# =====================================================================
print("="*72)
print("1. OVERALL color factor cancels (closed door), re-proven exact:")
print("="*72)
w = mpf('7.3')  # arbitrary overall color weight
v = [sqrt(m) for m in (mu_u,mu_c,mu_t)]
a_s0,a_d0 = projections(v);   g0 = a_d0/a_s0
vw = [w*x for x in v]
a_sw,a_dw = projections(vw);  gw = a_dw/a_sw
print(f"  up g (no weight)     = {mp.nstr(g0,12)}")
print(f"  up g (overall w={mp.nstr(w,3)}) = {mp.nstr(gw,12)}   IDENTICAL -> overall color cancels.\n")

# =====================================================================
# 2. THE ONLY NON-TRIVIAL HOOK: a PER-CHANNEL color weight.
#    Reweight singlet channel by w_S, doublet channel by w_D.
#    Then the reweighted vector has  a_sing -> w_S * a_sing,
#                                    a_doub -> w_D * a_doub,
#    so  g_eff = (w_D/w_S) * g_bare.
#    => Q_eff = 1/3 + (w_D/w_S)^2 * g_bare^2 / 3.
#    The selector works IFF (w_D/w_S) is a color-derived ratio that is
#    1 for leptons and != 1 for quarks (to move them), AND lands leptons
#    at g=1 (which it does automatically IFF lepton bare g is already 1
#    -- which it IS. So leptons need w_D/w_S = 1 EXACTLY).
# =====================================================================
print("="*72)
print("2. PER-CHANNEL color weight: g_eff = (w_D/w_S) * g_bare")
print("   For leptons to STAY Koide, need w_D/w_S = 1 (lepton bare g already 1).")
print("   For quarks to be PUSHED OFF, need w_D/w_S != 1 for quarks.")
print("="*72)

# Bare g per sector
gb = {}
for name, ms in [('lepton',[m_e,m_mu,m_tau]),
                 ('up',[mu_u,mu_c,mu_t]),
                 ('down',[md_d,md_s,md_b])]:
    a_s,a_d = projections([sqrt(m) for m in ms]); gb[name]=a_d/a_s

print(f"  bare g: lepton={mp.nstr(gb['lepton'],7)}  up={mp.nstr(gb['up'],7)}  down={mp.nstr(gb['down'],7)}")
print(f"  Koide g = 1")
print()

# THE CRUCIAL POINT: leptons are ALREADY at g=1 with NO weight.
# So a color-channel selector that "lands leptons at Koide" must do NOTHING
# to leptons (w_D/w_S=1). It can ONLY add value if it moves the QUARKS.
# But the quarks are ALREADY off Koide with no weight. So the selector is
# not NEEDED to push quarks off -- they are off already. The honest question
# flips: is there a color weight that (a) keeps leptons AT g=1 and (b) is
# defined by color reps alone (not tuned)? And does requiring w_D/w_S=1 for
# the COLORLESS lepton emerge naturally?

print("  *** THE LOGICAL PIVOT (both-ways honesty): ***")
print("  Leptons are ALREADY at g=1 with NO weight (bare). Quarks are")
print("  ALREADY off with no weight. So a color SELECTOR is not needed to")
print("  separate them -- the bare masses already do. The selector idea only")
print("  has CONTENT if the framework's dS-Unruh measure OVERSHOOTS leptons")
print("  to g=sqrt2 (per-STATE equipartition r_circ=2, the wave-1 result), and")
print("  a color per-CHANNEL correction pulls leptons BACK to g=1. Test THAT:\n")

# =====================================================================
# 3. THE REAL TEST: per-STATE overshoot (g=sqrt2, r_circ=2) and whether a
#    COLOR channel weight pulls leptons to g=1 but NOT quarks.
#    Wave-1: per-state mode-count equipartition gives doublet:singlet
#    amplitude ratio with the doublet's dim-2 multiplicity -> overshoot
#    r_circ=2 (Q=1), i.e. g_state = r_circ/sqrt2 = sqrt2.
#    Per-irrep (class-function) equipartition gives g=1 (r_circ=sqrt2, Q=2/3).
#    The ratio g_state/g_channel = sqrt2/1 = sqrt2 = sqrt(doublet dim).
#    QUESTION: is the per-irrep (channel) measure FORCED for leptons and
#    the per-state measure forced for quarks -- by COLOR?
# =====================================================================
print("="*72)
print("3. THE per-STATE vs per-CHANNEL ratio and a COLOR hook")
print("="*72)
print(f"  per-state (overshoot)  g_state   = sqrt2  -> r_circ=2,    Q=1   (doublet dim-2 multiplicity)")
print(f"  per-channel (Koide)    g_channel = 1      -> r_circ=sqrt2, Q=2/3 (equal per-irrep amplitude)")
print(f"  ratio g_state/g_channel = sqrt2 = sqrt(doublet-dim=2). COLOR-INDEPENDENT.")
print()
print("  The doublet dimension is 2 for EVERY charge sector (S3 rep is the")
print("  generation index, color-blind). So the per-state/per-channel gap is")
print("  the SAME sqrt2 for leptons AND quarks. Color does not enter it.\n")

# To make color enter, POSIT a measure interpolating state<->channel by a
# color-dependent exponent:  g_eff = g_channel * (sqrt2)^(f(color))
# with f=0 -> channel (Koide g=1), f=1 -> state (overshoot g=sqrt2).
# A "natural" color hook would be e.g. f = (N_c - 1)/something, or
# f tied to the color rep being a singlet (lepton) vs triplet (quark).
# Test the cleanest color-defined f's and ask: does ANY land leptons at
# Koide (needs f_lepton=0) AND output the ACTUAL quark g (not just 'off')?

print("  Test: g_eff(sector) = 1 * (sqrt2)^f(color),  f from color reps ONLY.")
print("  (f=0 -> Koide g=1 ; f=1 -> overshoot g=sqrt2). Need f_lepton=0 for Koide,")
print("   and f_quark chosen by color must REPRODUCE the actual quark g, not just !=1.\n")

# Actual quark g targets (bare, pole/MSbar)
g_up_target   = gb['up']
g_down_target = gb['down']
# Solve for the f that each sector WOULD need:  g = (sqrt2)^f -> f = log(g)/log(sqrt2)
def f_needed(g_target):
    return mp.log(g_target)/mp.log(sqrt(2))

print(f"  f needed for lepton (g=1):     {mp.nstr(f_needed(gb['lepton']),6)}  (=0, good: colorless)")
print(f"  f needed for up    (g={mp.nstr(g_up_target,5)}): {mp.nstr(f_needed(g_up_target),6)}")
print(f"  f needed for down  (g={mp.nstr(g_down_target,5)}): {mp.nstr(f_needed(g_down_target),6)}")
print()
print("  COLOR-DEFINED candidates for f (defined WITHOUT Koide):")
color_f = {
  'f = N_c - 1':         {'lepton':0, 'up':2,   'down':2},     # 0 for color-singlet, 2 for triplet
  'f = (N_c-1)/2':       {'lepton':0, 'up':1,   'down':1},
  'f = 1 - 1/N_c':       {'lepton':0, 'up':mpf(2)/3, 'down':mpf(2)/3},
  'f = log2(N_c)':       {'lepton':0, 'up':mp.log(3)/mp.log(2), 'down':mp.log(3)/mp.log(2)},
  'f = C2(color)':       {'lepton':0, 'up':mpf(4)/3, 'down':mpf(4)/3},  # Casimir of fundamental
}
print(f"  {'rule':22s} {'f_up':>10s} {'g_up_pred':>12s} {'g_up_act':>12s} {'f_down':>10s} {'g_dn_pred':>12s} {'g_dn_act':>12s}")
for rule, fv in color_f.items():
    g_up_pred = (sqrt(2))**fv['up']
    g_dn_pred = (sqrt(2))**fv['down']
    print(f"  {rule:22s} {mp.nstr(fv['up'],4):>10s} {mp.nstr(g_up_pred,7):>12s} {mp.nstr(g_up_target,7):>12s} "
          f"{mp.nstr(fv['down'],4):>10s} {mp.nstr(g_dn_pred,7):>12s} {mp.nstr(g_down_target,7):>12s}")

print("""
  READING: every color-defined f gives f_up = f_down (up and down are BOTH
  color triplets, identical color rep), so EVERY such rule predicts
  g_up = g_down EXACTLY. But the actual g_up=%s != g_down=%s. So no
  color-channel exponent can split up from down -- they have the SAME color.
  The up/down splitting is an ELECTROWEAK / Yukawa effect, NOT color.""" %
      (mp.nstr(g_up_target,5), mp.nstr(g_down_target,5)))

# =====================================================================
# 4. THE DECISIVE no-go: up and down share color => any color weight is
#    blind to the up/down difference. And the lepton 'success' (f=0) is
#    just 'colorless does nothing' -- which is the SAME statement as the
#    neutrino (also colorless) which is NOT at Koide. So colorless does
#    not imply Koide.
# =====================================================================
print("\n" + "="*72)
print("4. DECISIVE no-go + the neutrino check")
print("="*72)
# neutrino is colorless (N_c=1) like the charged lepton -> f_nu = f_lepton = 0
# so any color-channel selector predicts neutrinos ALSO at r=sqrt2 (Koide).
# Reality: neutrino Q is a FREE function of m1, NOT 2/3.
dm21sq = mpf('7.42e-5'); dm31sq = mpf('2.515e-3')
print("  Neutrino (colorless, N_c=1 -> f=0 -> predicted g=1, Q=2/3):")
for m1 in [mpf('0'), mpf('0.001'), mpf('0.01'), mpf('0.05')]:
    m1e = m1 if m1>0 else mpf('1e-12')
    m2 = sqrt(m1e**2+dm21sq); m3 = sqrt(m1e**2+dm31sq)
    a_s,a_d = projections([sqrt(mm) for mm in (m1e, m2, m3)])
    g_nu = a_d/a_s
    Qn = koide_Q([m1e, m2, m3])
    print(f"    m1={mp.nstr(m1,3):8s} eV -> actual g={mp.nstr(g_nu,6):9s} Q={mp.nstr(Qn,6)}  "
          f"(color rule PREDICTS g=1, Q=2/3 -> FALSIFIED)")
print("""
  => A color-channel selector that sets f=0 for color-singlets predicts the
  NEUTRINO (also a color singlet) at Koide r=sqrt2 too. But neutrino r is a
  free function of m1, generically NOT sqrt2. So 'color-singlet -> Koide'
  is FALSIFIED by the neutrino. The selector is not lepton-selective; it is
  color-singlet-selective, and the two colorless sectors (charged lepton,
  neutrino) do NOT both obey Koide.""")

print("\n" + "="*72)
print("VERDICT")
print("="*72)
print("""
- An overall color factor CANCELS in r (closed door, re-proven exact).
- The ONLY non-trivial color hook is a PER-CHANNEL (singlet-vs-doublet)
  weight giving r_eff=(w_D/w_S)*r_bare. But the S3 doublet/singlet split is
  the GENERATION index, color-blind: the per-state<->per-channel gap is
  sqrt(2)=sqrt(doublet-dim) for EVERY charge sector. Color does not enter it.
- To force color in, a color-exponent f(N_c) must (a) be 0 for the colorless
  lepton (so it stays at Koide -- but this is 'colorless does nothing', and
  the colorless NEUTRINO is then ALSO predicted Koide, FALSE), and (b) split
  up from down -- IMPOSSIBLE, both are identical color triplets.
- Therefore: NO natural color-channel weight is lepton-selective. The two
  things color would have to do (keep leptons-only at Koide; split up/down)
  are both blocked: colorless includes the non-Koide neutrino, and up/down
  share color. Any weight that does it must be HAND-TUNED per sector
  (3 free numbers w_D/w_S, exactly the generic-fit trap), reproducing the
  measured r by construction, predicting nothing.
- The lepton-selectivity is ELECTROWEAK/charge (Sumino's QED-charge +
  conjugate U(3) reps), NOT color. The wall STANDS.
""")
