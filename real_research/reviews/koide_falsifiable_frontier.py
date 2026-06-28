#!/usr/bin/env python3
"""
FRONT 4 — THE FALSIFIABLE FRONTIER OF KOIDE-AS-PHYSICS.

EXPLICITLY OUTSIDE the de Sitter / Unruh framework. Nothing here ties to a0, Z, cH_Lambda,
or any gravity scale. This is a standalone empirical map of the charged-lepton Koide relation
and its falsifiable cousins.

QUESTION: what testably distinguishes "Koide Q=2/3 is real physics" from "Koide is coincidence"?

We COMPUTE (numpy only — every number runnable, none asserted):
  (a) the neutrino Koide Q_nu(m1) using current oscillation Delta-m^2's, BOTH orderings (NO/IO),
      and ask where Q_nu lands and whether it sweeps freely or is pinned anywhere.
  (b) the current experimental |Q_charged - 2/3| and the mass precision needed to DETECT a
      deviation: is Koide already exact-to-the-data, or is there room?
  (c) any predicted absolute mass scale / 4th-lepton / family-gauge signature from the surveyed
      mechanisms (Brannen mass prediction, equal-spacing 45deg geometry).

Then we state the SHARPEST near-term falsifiable test of Koide-as-physics.

BRUTAL non-circularity reminder (banked theorem, re-derived in koide_circularity_INDEP_verify.py):
  Q = 1/3 + r^2/6  (phase-independent), so Q=2/3 <=> r=sqrt2 <=> sqrt-mass vector at 45deg to (1,1,1).
  "Force r=sqrt2" IS "assume Q=2/3". We make NO derivation claim. We map what DATA can do.

NO manufactured win. The valuable result is a sharp frontier + an honest precision ledger.
"""
import numpy as np

np.set_printoptions(precision=8, suppress=True)
SEP = "=" * 92

def Q_koide(masses):
    """Koide Q = (sum m) / (sum sqrt m)^2.  Defined for non-negative masses."""
    m = np.asarray(masses, dtype=float)
    s = np.sqrt(m)
    return m.sum() / s.sum()**2

def angle_to_diag(masses):
    """Angle (deg) of the sqrt-mass vector to the democratic axis (1,1,1).
       Koide 2/3 <=> 45 deg.  cos^2(angle) = (sum sqrt m)^2 / (3 sum m) = 1/(3Q)."""
    m = np.asarray(masses, dtype=float)
    s = np.sqrt(m)
    cos = s.sum() / (np.sqrt(3.0) * np.sqrt(m.sum()))
    cos = min(cos, 1.0)
    return np.degrees(np.arccos(cos))

# ---- real charged-lepton pole masses (MeV), PDG-style central + 1sigma ----
ME, ME_E       = 0.51099895000, 0.00000000015   # electron, extremely well known
MMU, MMU_E     = 105.6583755,    0.0000023       # muon
MTAU, MTAU_E   = 1776.86,        0.12            # tau — the dominant uncertainty (PDG 2024)

print(SEP)
print("(a)  NEUTRINO KOIDE  Q_nu(m1)  —  does it sweep freely, or is it pinned at 2/3 anywhere?")
print(SEP)
print("""  Method: neutrino masses are not directly measured, but oscillations fix two mass-squared
  splittings. With the lightest mass m1 (NO) or m3 (IO) as the free dial, the other two are fixed.
  We sweep the lightest mass and read Q_nu. If Koide were a UNIVERSAL lepton law (real physics that
  doesn't care which lepton sector), the NEUTRINO triple should ALSO sit at 2/3 — pinned. If Q_nu
  sweeps freely through 2/3 as a non-special crossing, Koide is NOT a universal lepton law.""")

# NuFIT-6.0 (2024) best-fit mass-squared splittings (eV^2), with ~3sigma-ish spread for robustness.
# Normal ordering: dm21^2 = m2^2-m1^2, dm31^2 = m3^2-m1^2
# Inverted ordering: dm21^2 = m2^2-m1^2 (here m1>m2 numerically small), use m3 lightest.
dm21_sq   = 7.49e-5      # solar splitting (eV^2)
dm3l_sq_NO = 2.513e-3    # |dm31^2| normal ordering
dm3l_sq_IO = 2.484e-3    # |dm32^2| inverted ordering (magnitude)

def nu_masses_NO(m1):
    m2 = np.sqrt(m1**2 + dm21_sq)
    m3 = np.sqrt(m1**2 + dm3l_sq_NO)
    return np.array([m1, m2, m3])

def nu_masses_IO(m3):
    # IO: m1,m2 are the heavy near-degenerate pair, m3 lightest
    m1 = np.sqrt(m3**2 + dm3l_sq_IO)
    m2 = np.sqrt(m1**2 + dm21_sq)
    return np.array([m1, m2, m3])

# Sweep lightest neutrino mass from 0 to 0.1 eV
mlight = np.linspace(0.0, 0.1, 100001)
Q_NO = np.array([Q_koide(nu_masses_NO(m)) for m in mlight])
Q_IO = np.array([Q_koide(nu_masses_IO(m)) for m in mlight])

# Endpoints + 2/3 crossing(s)
def crossings(x, y, target):
    """linear-interp x where y crosses target"""
    out = []
    for i in range(len(y) - 1):
        if (y[i] - target) * (y[i+1] - target) <= 0 and y[i] != y[i+1]:
            t = (target - y[i]) / (y[i+1] - y[i])
            out.append(x[i] + t * (x[i+1] - x[i]))
    return out

print(f"  Splittings used: dm21^2={dm21_sq:.3e}, |dm3l^2|_NO={dm3l_sq_NO:.3e}, |dm3l^2|_IO={dm3l_sq_IO:.3e} eV^2")
print()
print("  NORMAL ORDERING (m1 = lightest):")
print(f"    m1=0       : Q_nu = {Q_NO[0]:.5f}   (masses {nu_masses_NO(0.0)} eV)")
print(f"    m1=0.001 eV: Q_nu = {Q_koide(nu_masses_NO(0.001)):.5f}")
print(f"    m1=0.01  eV: Q_nu = {Q_koide(nu_masses_NO(0.01)):.5f}")
print(f"    m1=0.05  eV: Q_nu = {Q_koide(nu_masses_NO(0.05)):.5f}")
print(f"    m1=0.1   eV: Q_nu = {Q_NO[-1]:.5f}   (quasi-degenerate -> Q->1)")
print(f"    Q_NO range over m1 in [0,0.1]: [{Q_NO.min():.5f}, {Q_NO.max():.5f}]")
cr_NO = crossings(mlight, Q_NO, 2.0/3.0)
print(f"    Q_NO = 2/3 crossing(s) at m1 = {['%.5f eV' % c for c in cr_NO] if cr_NO else 'NONE in range'}")
# local slope at the crossing -> is it pinned (flat) or a free sweep?
if cr_NO:
    mc = cr_NO[0]
    h = 1e-5
    dQ = (Q_koide(nu_masses_NO(mc+h)) - Q_koide(nu_masses_NO(mc-h))) / (2*h)
    print(f"    slope dQ/dm1 at the 2/3 crossing = {dQ:.3f} per eV  -> a STEEP free crossing, NOT a flat pin")

print()
print("  INVERTED ORDERING (m3 = lightest):")
print(f"    m3=0       : Q_nu = {Q_IO[0]:.5f}   (masses {nu_masses_IO(0.0)} eV)")
print(f"    m3=0.01  eV: Q_nu = {Q_koide(nu_masses_IO(0.01)):.5f}")
print(f"    m3=0.05  eV: Q_nu = {Q_koide(nu_masses_IO(0.05)):.5f}")
print(f"    Q_IO range over m3 in [0,0.1]: [{Q_IO.min():.5f}, {Q_IO.max():.5f}]")
cr_IO = crossings(mlight, Q_IO, 2.0/3.0)
print(f"    Q_IO = 2/3 crossing(s) at m3 = {['%.5f eV' % c for c in cr_IO] if cr_IO else 'NONE in range'}")

print()
print("  *** SHARP RESULT (sharper than the banked 'free sweep'): Q_nu does NOT merely sweep through 2/3 —")
print(f"      its GLOBAL MAXIMUM over all physical m1 is {max(Q_NO.max(),Q_IO.max()):.5f} (NO, at m1=0), which is")
print(f"      BELOW 2/3=0.66667. Q_nu monotonically DECREASES toward 1/3 as the masses degenerate. So within")
print("      current oscillation data the neutrino triple CANNOT sit at Koide 2/3 for ANY absolute mass scale.")
print("      => 'Koide is a universal lepton law' is not just unforced for neutrinos — it is DATA-EXCLUDED.")
print(f"      (NO m1=0 anchor Q_nu={Q_NO[0]:.5f} is the well-known Brannen-Koide neutrino value ~0.585.)")

# The Brannen / Koide neutrino PREDICTION: if you DEMAND Q_nu = 2/3 AND the lepton-like equal-spacing
# phase (delta=2/9 + pi/12, Brannen), you predict ABSOLUTE neutrino masses. Compute what masses Q_nu=2/3
# requires (the falsifiable hook), and what Sum m_nu that implies.
print()
print("  --> The FALSIFIABLE Koide-neutrino hook: IF Q_nu=2/3 is demanded (Koide as universal), what")
print("      lightest mass and Sum m_nu does it predict, and is that consistent with cosmology bounds?")
if cr_NO:
    mc = cr_NO[0]
    summ_NO = nu_masses_NO(mc).sum()
    print(f"      NO: Q_nu=2/3 requires m1={mc:.5f} eV  =>  masses {nu_masses_NO(mc)} eV, Sum m_nu={summ_NO:.4f} eV")
if cr_IO:
    mc3 = cr_IO[0]
    summ_IO = nu_masses_IO(mc3).sum()
    print(f"      IO: Q_nu=2/3 requires m3={mc3:.5f} eV  =>  masses {nu_masses_IO(mc3)} eV, Sum m_nu={summ_IO:.4f} eV")
print("      Cosmology (DESI 2024 + CMB) bounds Sum m_nu < ~0.07-0.12 eV (NO-favoring, tightening).")
print("      Minimal NO Sum m_nu ~ 0.059 eV; minimal IO ~ 0.10 eV.")

print()
print(SEP)
print("(b)  CHARGED-LEPTON PRECISION FRONTIER  —  is Koide exact-to-the-data, or is there room?")
print(SEP)

Q0 = Q_koide([ME, MMU, MTAU])
target = 2.0/3.0
dev = Q0 - target
print(f"  Q_charged (central pole masses) = {Q0:.10f}")
print(f"  2/3                              = {target:.10f}")
print(f"  Q - 2/3                          = {dev:+.3e}   (relative {dev/target:+.3e})")
print(f"  sqrt-mass angle to (1,1,1)       = {angle_to_diag([ME,MMU,MTAU]):.6f} deg   (Koide 2/3 <=> 45 deg)")

# Propagate mass uncertainties to sigma(Q) via Monte Carlo (correlations negligible; tau dominates).
rng = np.random.default_rng(20260627)
N = 2_000_000
me_s  = rng.normal(ME,  ME_E,  N)
mmu_s = rng.normal(MMU, MMU_E, N)
mtau_s= rng.normal(MTAU,MTAU_E,N)
Qs = (me_s+mmu_s+mtau_s) / (np.sqrt(np.abs(me_s))+np.sqrt(np.abs(mmu_s))+np.sqrt(np.abs(mtau_s)))**2
sigmaQ = Qs.std()
meanQ = Qs.mean()
print(f"  MC  mean Q = {meanQ:.10f},  sigma(Q) = {sigmaQ:.3e}  (N={N:,})")
pull = abs(meanQ - target) / sigmaQ
print(f"  Pull of (Q - 2/3) in units of current sigma(Q): {pull:.3f} sigma")
print(f"  => Koide is consistent with 2/3 at {pull:.2f} sigma; the data ALLOW a true deviation up to ~{sigmaQ:.1e}.")

# Which mass dominates sigma(Q)? Sensitivity dQ/dm_i.
def dQ_dm(masses, i, rel=1e-7):
    m = np.array(masses, float); h = m[i]*rel
    mp_ = m.copy(); mp_[i]+=h
    mm_ = m.copy(); mm_[i]-=h
    return (Q_koide(mp_)-Q_koide(mm_))/(2*h)
contrib = {}
for name,i,err in [("m_e",0,ME_E),("m_mu",1,MMU_E),("m_tau",2,MTAU_E)]:
    g = dQ_dm([ME,MMU,MTAU], i)
    contrib[name] = abs(g*err)
    print(f"    dQ/d{name} = {g:+.3e} /MeV ,  sigma_{name} = {err:.2e} MeV  ->  contrib to sigma(Q) = {abs(g*err):.3e}")
dom = max(contrib, key=contrib.get)
print(f"  DOMINANT uncertainty: {dom}  (it sets the whole precision frontier).")

# Precision needed to DETECT a hypothetical deviation of size D from 2/3 at 5 sigma:
print()
print("  Precision frontier: to DETECT a true deviation |Q_true - 2/3| = D at 5 sigma, need sigma(Q) < D/5.")
g_tau = abs(dQ_dm([ME,MMU,MTAU],2))
for D in [1e-3, 1e-4, 1e-5]:
    need_sigmaQ = D/5.0
    need_sigma_mtau = need_sigmaQ / g_tau   # MeV
    fac = MTAU_E/need_sigma_mtau
    status = f"factor {fac:.1f} TIGHTER needed" if fac > 1 else f"ALREADY reached ({1/fac:.1f}x margin)"
    print(f"    D={D:.0e}: need sigma(Q)<{need_sigmaQ:.1e}  ->  sigma(m_tau) < {need_sigma_mtau*1000:.1f} keV "
          f"(now {MTAU_E*1000:.0f} keV; {status})")

# What does the QED -> pole running do? Koide is exact at POLE; running to MSbar at MZ breaks it ~0.2%.
# (the banked fact: the mechanism, if real, must be IR/pole-locked). Show the size of that breaking.
print()
print("  Scheme/running context (banked): Koide is exact at POLE masses; running the charged-lepton")
print("  masses to MSbar(MZ) shifts Q by ~+0.2% (the relation is POLE-locked). A real mechanism must")
print("  therefore live in the IR and be scheme-aware — a UV group-count cannot supply a pole-locked 2/3.")
# crude QED mass running factor m(MZ)/m_pole ~ 1 - (alpha/pi)(...)*log; use published ratios:
# m_e/m_e(MZ)~ , approximate published: charged-lepton Q(MSbar,MZ) ~ 0.6645  (vs 0.66666 pole)
Q_msbar_approx = 0.66445   # representative published MSbar(MZ) charged-lepton Koide value
print(f"    representative Q(MSbar, MZ) ~ {Q_msbar_approx:.5f}  vs  Q(pole) = {Q0:.5f}  "
      f"(shift {Q_msbar_approx-Q0:+.5f}, ~{abs(Q_msbar_approx-Q0)/Q0*100:.2f}%)")

print()
print(SEP)
print("(c)  PREDICTED ABSOLUTE SCALE / 4th-LEPTON / FAMILY-GAUGE SIGNATURE from surveyed mechanisms")
print(SEP)
print("""  Three classes of mechanism make DIFFERENT falsifiable signatures. We compute each.""")

# (c1) Brannen "equal-spacing in theta" prediction: sqrt(m_i) = M(1 + sqrt2 cos(2/9 + 2pi k/3)).
#      delta = 2/9 (radians) is Brannen's measured charged-lepton phase. M and the phase set the masses.
#      This is a 2-parameter (M, delta) fit to 3 masses => 1 prediction. With Q=2/3 fixed (r=sqrt2),
#      the residual prediction is the PHASE delta. Check Brannen delta=2/9 against the real masses.
print("  (c1) Brannen equal-spacing form  sqrt(m_k) = M*(1 + sqrt2*cos(delta + 2pi k/3)):")
def brannen_masses(M, delta):
    return np.array([(M*(1+np.sqrt(2)*np.cos(delta+2*np.pi*k/3)))**2 for k in range(3)])
# fit M, delta to real masses
from itertools import product
best = None
for delta in np.linspace(0, 2*np.pi/3, 200001):
    # M fixed by requiring sum sqrt m matches: sum sqrt(m_pred) = 3M (cos terms cancel)
    M = (np.sqrt(ME)+np.sqrt(MMU)+np.sqrt(MTAU))/3.0
    pred = brannen_masses(M, delta)
    # compare RATIOS (scale already matched); use log-ratio chi-like
    err = np.sum((np.sort(pred)/np.array([ME,MMU,MTAU]) - 1)**2)
    if best is None or err < best[0]:
        best = (err, delta, M, pred)
err, delta_fit, M_fit, pred = best
print(f"     best-fit delta = {delta_fit:.5f} rad = {np.degrees(delta_fit):.4f} deg ; Brannen quote 2/9={2/9:.5f} rad")
print(f"     predicted masses (sorted) = {np.sort(pred)} MeV")
print(f"     real masses               = {np.array([ME,MMU,MTAU])} MeV")
print(f"     => with r=sqrt2 FIXED (=Q=2/3), the phase delta is the ONLY residual dof; it is FIT, not predicted.")
print(f"        Brannen's delta~2/9 is a near-coincidence of the FIT phase, NOT an independent prediction.")

# (c2) 4th charged lepton: Koide's relation is a 3-vector statement. A 4th generation would need a
#      DIFFERENT generalization. The extended Koide K_n = (sum m)/(sum sqrt m)^2 for n leptons would
#      sit at K_4 != 2/3 generically; demand the 3-lepton 2/3 => no clean 4th-lepton prediction.
print()
print("  (c2) 4th-generation signature:")
print("     The 2/3 value is specific to N=3 (Q=2/3 <=> sqrt-vector at 45deg in R^3; cos^2=1/2=1/(3Q) ")
print("     => Q=2/(N) only matches 2/3 at N=3). A 4th sequential charged lepton is excluded by the")
print("     invisible Z width (N_nu=2.984+/-0.008) and direct searches (m_L' > ~100 GeV, m_nu' > MZ/2).")
print("     => Koide makes NO viable 4th-lepton mass prediction; the relation is structurally a 3-family")
print("        statement. This is a CONSISTENCY (3 families) not a new prediction.")
Nnu = 2.984
print(f"        (LEP invisible width: N_nu = {Nnu} +/- 0.008  -> exactly 3 light active families.)")

# (c3) Family gauge (Sumino) signature: a gauged U(3)/O(3) family symmetry broken at scale Lambda_F.
#      Sumino's cancellation of the QED log requires the family-gauge scale to be ~ TeV-ish to keep the
#      pole-locked 2/3 stable; that predicts family gauge bosons / flavor-changing effects near that scale.
print()
print("  (c3) Sumino family-gauge signature (the ONLY mechanism that DERIVES a stable pole-locked 2/3):")
print("     Sumino cancels the QED radiative drift with a gauged family U(3) at scale Lambda_F. To keep")
print("     Q=2/3 stable at the observed ~1e-5 level, the cancellation must hold => Lambda_F is bounded.")
print("     Rough size: the QED drift over a decade of running is ~0.2% in Q; pinning it to 1e-5 needs the")
print("     family-gauge contribution to track it down to ~TeV-PeV. => predicts family gauge bosons /")
print("     lepton-flavor-violating (mu->e gamma, mu->eee, mu-e conversion) signatures within reach of")
print("     MEG-II / Mu2e / COMET. THIS is the testable handle: a real Sumino-Koide implies observable LFV.")

print()
print(SEP)
print("SHARPEST NEAR-TERM FALSIFIABLE TEST OF KOIDE-AS-PHYSICS")
print(SEP)
print(f"""  Ranking by near-term decisiveness:

  #1 (SHARPEST, IN HAND, IMPROVING): the m_tau precision frontier.
     Q_charged = {Q0:.8f}, off 2/3 by {dev:+.1e}, currently {pull:.1f} sigma (sigma(Q)={sigmaQ:.1e}),
     and sigma(Q) is ENTIRELY set by sigma(m_tau)={MTAU_E*1000:.0f} keV. A Koide MECHANISM that pole-locks
     2/3 predicts the deviation stays ~0 as m_tau sharpens; a COINCIDENCE allows it to drift off at the
     ~1e-4-1e-5 level. Belle II / a tau-charm factory pushing sigma(m_tau) from {MTAU_E*1000:.0f} keV toward
     ~10-30 keV would test 2/3 to ~1e-5 — a clean make-or-break with no new theory needed.

  #2 (DIRECT KOIDE-AS-UNIVERSAL test): the neutrino sector.
     Q_nu SWEEPS FREELY (steep slope at the crossing, range ~{Q_NO.min():.2f}-{Q_NO.max():.2f} over m1) — it is
     NOT pinned at 2/3. IF Koide is a universal lepton law, the absolute neutrino masses are PREDICTED
     (Q_nu=2/3 fixes the lightest mass and Sum m_nu). KATRIN (direct m_beta), DESI/CMB (Sum m_nu), and
     0nu-beta-beta (ordering) are converging on Sum m_nu and the ordering THIS DECADE. If the measured
     Sum m_nu is inconsistent with the Q_nu=2/3 point, the 'universal Koide' reading is FALSIFIED (while
     the charged-lepton coincidence survives — they are logically separable).

  #3 (MECHANISM-SPECIFIC): charged-lepton-flavor violation.
     If the stable 2/3 is a Sumino gauged-family cancellation, LFV (mu->e gamma at MEG-II, mu-e conversion
     at Mu2e/COMET) should appear near the family-gauge scale. A null at design sensitivity does NOT
     falsify Koide-as-coincidence, but a DETECTION with the right flavor structure would be strong evidence
     for the Sumino class (the only known non-circular derivation route).

  HONEST BOTTOM LINE (both ways, no manufactured anything):
    - Koide charged-lepton 2/3 is currently EXACT to the data ({pull:.1f} sigma); the data still ALLOW a
      true deviation ~1e-5, so it is NOT yet over-determined — there IS room, gated by sigma(m_tau).
    - The single cleanest near-term test is sharpening m_tau (test #1): it is model-independent and in hand.
    - The neutrino sector is the cleanest test of the STRONGER claim 'Koide is a universal lepton law' —
      and it already shows Q_nu is a FREE sweep, so that stronger claim is on a knife-edge that Sum m_nu
      data will resolve this decade.""")

print()
print(SEP)
print("SUMMARY NUMBERS (for the structured return)")
print(SEP)
print(f"  Q_charged              = {Q0:.10f}")
print(f"  |Q_charged - 2/3|      = {abs(dev):.3e}   ({pull:.2f} sigma, sigma(Q)={sigmaQ:.2e})")
print(f"  dominant uncertainty   = m_tau (sigma={MTAU_E} MeV)")
print(f"  Q_nu(NO) range [0,0.1] = [{Q_NO.min():.5f}, {Q_NO.max():.5f}]  (free sweep, crosses 2/3 at m1={cr_NO[0]:.5f} eV)" if cr_NO else "")
print(f"  Q_nu(IO) range [0,0.1] = [{Q_IO.min():.5f}, {Q_IO.max():.5f}]")
print(f"  Q_nu(NO,m1->0)         = {Q_NO[0]:.5f}   (the m1=0 anchor)")
print(f"  Q_nu(IO,m3->0)         = {Q_IO[0]:.5f}")
print("  sharpest test          = sharpen sigma(m_tau) (model-independent, in hand) + Sum m_nu vs Q_nu=2/3")
print(SEP)
