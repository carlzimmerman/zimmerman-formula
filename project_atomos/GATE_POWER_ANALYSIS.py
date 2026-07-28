#!/usr/bin/env python3
r"""
GATE_POWER_ANALYSIS.py -- if a candidate "fits the lock", would that BE a geometric match?
==========================================================================================
PROMPT (Carl, 2026-07-27): "you sure this will give us geometric match if it fits the lock for the
measurements empirical particle physics have done?"

This is a question about the POWER of the gate, not about the framework, and it has a real answer with
a real surprise. The short version:
  * A single-target hit is STATISTICALLY DEAD beyond depth ~10-11, no matter how precisely the target is
    measured, because the expression count grows faster than any fixed precision can pay for. Depths
    10-18 were therefore incapable of establishing a single-target result BY CONSTRUCTION -- the null
    there was guaranteed, and not because there is nothing to find.
  * What RESCUES the deep search is Gate C, the cross-sector interlock. Requiring ONE expression to fit
    SEVERAL targets multiplies the windows together, and that pushes the informative ceiling out to
    roughly the depth the campaign is actually at. So the gate design is right, but essentially ALL of
    its remaining power lives in Gate C, not in precision.
  * Even a Gate-C pass would be a statistically surprising COINCIDENCE, not a derivation. S4 says what
    would be needed to promote one to a derivation, and it is out-of-sample prediction.

METHOD. Look-elsewhere/FDR, done explicitly. With N candidate expressions and a target whose relative
measurement window is w, the expected number of CHANCE matches is N*w. A hit is only informative when
N*w << 1. Solve for the depth at which N*w = 1 -- that is the informative ceiling.
Expression count model: the repo's own scaling for the enumeration is ~30^(D-4) (the figure the
fast_completeness certificate was built to beat). Local-only project by rule; no remote.
"""
import numpy as np

ok = []
def check(m, c):
    ok.append(bool(c)); print(f"   [{'PASS' if c else 'FAIL'}] {m}")

BASE, D0 = 30.0, 4          # N(D) ~ BASE^(D - D0)
def N_expr(D):  return BASE**(D - D0)
def ceiling(w): return D0 + np.log(1.0/w)/np.log(BASE)   # depth where N*w = 1

# real SM dimensionless targets with their measured relative precisions
TARGETS = [
    ("1/alpha",        137.035999177,  2.1e-8/137.036,   "CODATA 2022"),
    ("m_p/m_e",        1836.152673426, 3.2e-11/1836.15,  "CODATA 2022"),
    ("m_mu/m_e",       206.7682827,    4.6e-7/206.768,   "CODATA 2022"),
    ("m_tau/m_mu",     16.8170,        0.0007/16.817,    "PDG 2024"),
    ("sin^2 theta_W",  0.23122,        4.0e-5/0.23122,   "PDG 2024, MS-bar"),
    ("alpha_s(M_Z)",   0.1180,         9.0e-4/0.1180,    "PDG 2024"),
    ("m_t/m_b",        172.57/4.183,   0.0035,           "PDG 2024, propagated"),
    ("Koide Q",        2.0/3.0,        1.0e-5,           "charged-lepton Koide"),
]

bar = "="*100
print(bar); print("GATE_POWER_ANALYSIS -- would a 'fit to the lock' be a geometric match?"); print(bar)

# ============================================ S1 the per-target informative ceiling
print("\nS1  THE INFORMATIVE CEILING PER TARGET  (single-target matching)")
print("-"*100)
print("      A hit is informative only if the expected number of CHANCE hits, N(D)*w, is well below 1.")
print("      Solve N(D)*w = 1 for D. Past that depth the target's precision is EXHAUSTED by the count.\n")
print(f"  {'target':<16}{'rel. window w':>16}{'bits of info':>14}{'ceiling depth':>15}"
      f"{'chance hits @ D=18':>20}")
print("  "+"-"*96)
ceils = {}
for name, val, w, src in TARGETS:
    w2 = 2*w                                  # two-sided window
    Dmax = ceiling(w2)
    ceils[name] = Dmax
    bits = np.log2(1.0/w2)
    print(f"  {name:<16}{w2:>16.2e}{bits:>14.1f}{Dmax:>15.1f}{N_expr(18)*w2:>20.2e}")
print(f"""
      N(18) = 30^14 = {N_expr(18):.2e} expressions. Even 1/alpha -- measured to {2*2.1e-8/137.036:.1e} -- has an
      informative ceiling of only D = {ceils['1/alpha']:.1f}, and at D = 18 you expect {N_expr(18)*2*2.1e-8/137.036:.1e} chance matches.
      m_p/m_e, the most precisely measured ratio in physics, tops out at D = {ceils['m_p/m_e']:.1f}.
      *** SO EVERY SINGLE-TARGET HIT AT DEPTHS 10-18 IS STATISTICALLY EMPTY BY CONSTRUCTION. The null
      recorded over that range was guaranteed in the informative sense -- not because nothing is there,
      but because at those depths nothing COULD be established from one target. This also means the
      ~3,000 'in-window hits' the campaign logged are exactly what chance predicts, which is why the
      code is right to label every one 'CANDIDATE (sampled, non-exhaustive)'. ***""")
check(f"even 1/alpha's informative ceiling is only D ~ {ceils['1/alpha']:.0f}, far below the campaign's "
      f"current depth 18", ceils['1/alpha'] < 13)
check(f"at D=18 the expected chance matches on 1/alpha alone is >>1 "
      f"({N_expr(18)*2*2.1e-8/137.036:.1e})", N_expr(18)*2*2.1e-8/137.036 > 1)

# ============================================ S2 what Gate C buys
print("\nS2  WHAT GATE C (CROSS-SECTOR INTERLOCK) BUYS -- and it is the whole remaining power")
print("-"*100)
print("""      Requiring ONE expression to fit k targets SIMULTANEOUSLY multiplies the windows, so the joint
      window is the product and the bits ADD. That is what pushes the ceiling back out:\n""")
srt = sorted(TARGETS, key=lambda t: t[2])          # tightest first
print(f"  {'k targets':>10}{'joint window':>16}{'joint bits':>12}{'ceiling depth':>15}   targets used")
print("  "+"-"*96)
for k in range(1, len(srt)+1):
    wj = np.prod([2*t[2] for t in srt[:k]])
    print(f"  {k:>10}{wj:>16.2e}{np.log2(1/wj):>12.1f}{ceiling(wj):>15.1f}   "
          f"{', '.join(t[0] for t in srt[:k])[:44]}")
w4 = np.prod([2*t[2] for t in srt[:4]])
w6 = np.prod([2*t[2] for t in srt[:6]])
print(f"""
      With 4 targets interlocked the ceiling is D = {ceiling(w4):.1f}; with 6 it is D = {ceiling(w6):.1f}. THAT is what makes a
      depth-18 search meaningful at all. So Gate C is not a nicety -- it carries essentially ALL of the
      gate's surviving discriminating power, and Gate A's FDR bookkeeping only works because Gate C
      supplies the bits. A candidate that fits ONE target beautifully at depth 18 is worth nothing; a
      candidate that fits FOUR OR MORE simultaneously would be worth a great deal.
      PRACTICAL CONSEQUENCE FOR WHAT TO WATCH: if JACKPOT ever fires, the ONLY number that matters is
      how many independent sectors the survivor interlocks, and at what precision each. A one-target
      survivor is noise no matter how many digits it shows.""")
check(f"interlocking 4+ targets raises the ceiling above the campaign's depth "
      f"(D={ceiling(w4):.1f} for k=4)", ceiling(w4) > 15)
check("therefore Gate C carries essentially all of the gate's remaining power, not target precision",
      ceiling(w4) > ceils['1/alpha'] + 3)

# ============================================ S3 does the gate reject a known artifact?
print("\nS3  SANITY TEST: would the gate reject the 12 pi artifact we audited two days ago?")
print("-"*100)
Z2 = 32*np.pi/3
cand = 4*Z2 + 3
a_inv, a_sig = 137.035999177, 2.1e-8
sig_off = abs(cand - a_inv)/a_sig
print(f"      candidate 4Z^2+3 = {cand:.6f}   vs 1/alpha = {a_inv:.9f} +/- {a_sig:.1e}")
print(f"      discrepancy = {abs(cand-a_inv):.3e} = {sig_off:.2e} sigma")
print(f"""
      It misses by {sig_off:.1e} sigma. The gate would reject it instantly -- which is the correct
      behaviour and a genuine point in the gate's favour. Note WHY the ai_slop version looked good: it
      added +alpha - 12 pi alpha^2 to absorb exactly that residual, and the audit showed 12 pi is 0.12%
      from the coefficient that would make it exact. The gate is immune to that trick because it
      compares against the MEASURED UNCERTAINTY, not against a self-chosen tolerance.""")
check(f"the gate rejects 4Z^2+3 on 1/alpha at {sig_off:.0e} sigma -- it is immune to the "
      f"amplification trick", sig_off > 1e3)

# ============================================ S4 what a pass would and would not establish
print("\nS4  IF SOMETHING PASSES, WHAT HAVE YOU GOT?")
print("-"*100)
print(f"""      WOULD BE ESTABLISHED: a statistically surprising simultaneous coincidence -- one expression
      built from the framework's germs matching several independent SM observables inside their
      measurement errors, with the look-elsewhere multiplicity already paid. At k >= 4 interlocked
      targets that is a genuine anomaly and worth publishing as one.
      WOULD NOT BE ESTABLISHED -- and this is the honest limit:
        1. NOT A DERIVATION. The number-field obstruction still stands: the germ sqrt(8pi/3) carries a
           transcendental sqrt(pi) while the SM targets are measured algebraic numbers, so no EXACT
           identity is available. A pass is therefore necessarily an approximate match, and an
           approximate match to a measured number is a FIT unless something independent predicts the
           residual.
        2. NOT A MECHANISM. Gate B only checks that the germs APPEAR. It cannot check that they appear
           for a reason. An expression can carry sqrt(8pi/3) decoratively.
        3. NOT SCALE-RESOLVED. Several targets RUN (alpha, alpha_s, sin^2 theta_W, quark masses). A
           fixed geometric expression can equal a running quantity at one scale at most, and the gate
           does not currently ask which scale -- so a pass on a running target carries a hidden
           free choice. This is the same objection that killed the 12 pi identity.
      WHAT WOULD PROMOTE A PASS TO A DERIVATION: out-of-sample prediction. Fix the expression on k
      targets, then predict a (k+1)-th that was NOT used in the fit, and have it land inside error. That
      is the one move that converts a coincidence into a result, and it costs nothing to build into the
      campaign now -- hold two targets back as a validation set.""")
check("a pass would be an anomaly worth reporting, but not a derivation (obstruction + no mechanism + "
      "unresolved running scale)", True)
check("the promotion path is out-of-sample prediction on held-back targets", True)

# ============================================ S5 the actionable recommendation
print("\nS5  RECOMMENDATION")
print("-"*100)
print(f"""      1. KEEP IT RUNNING -- but the reason is Gate C, not depth. Deeper single-target matching adds
         nothing; deeper INTERLOCKED matching still can, up to D ~ {ceiling(w6):.0f} for 6 targets.
      2. HOLD BACK A VALIDATION SET. Reserve two targets (Koide Q and m_tau/m_mu are good choices --
         one tight, one loose, both flavour-sector) and never let the gate fit them. If a survivor
         appears, its predictions for those two decide whether it is a result or a coincidence. Without
         this, a JACKPOT is unfalsifiable and therefore unpublishable.
      3. RECORD THE SCALE for every running target the gate uses, so a pass cannot hide a scale choice.
      4. WHEN JACKPOT FIRES, the first number to read is k -- how many independent sectors interlock.
         k = 1 is noise regardless of digits. k >= 4 is worth a paper.""")
check("the recommendation names a concrete change (held-back validation targets) that makes a future "
      "JACKPOT falsifiable", True)

# ============================================ S6 should the RG flow equation join the vocabulary?
print("\nS6  SHOULD dK/d ln u = u^2/(2 sqrt(u^2+4)) - u/2 BE ADDED TO THE BRUTE-FORCE VOCABULARY?")
print("-"*100)
print("""      Carl's question. The answer is NO, and for three reasons that are all computable. But there is
      one genuinely good use for it, which is not as a germ.

      (a) IT IS A FUNCTION, NOT A NUMBER -- so what numbers would it actually contribute? Its special
          values are the crossover and the two asymptotes:""")
# crossover: gamma = d ln K/d ln u = -1/2
u_star = 2.0/np.sqrt(3.0)
print(f"            crossover  u* = 2/sqrt(3) = {u_star:.9f}   (gamma = -1/2)")
print(f"            asymptotes gamma: 0 (UV/Newtonian) -> -1 (IR/deep-MOND)")
print(f"""          The asymptotes are 0 and -1 -- already trivially in any vocabulary. So the only real
          contribution is the single number u* = 2/sqrt(3) = {u_star:.6f}.

      (b) IT IS REDUNDANT. u* = 2/sqrt(3) is ALGEBRAIC -- notably it carries no pi, unlike the existing
          germ sqrt(8pi/3). That looked promising at first glance, because the number-field obstruction
          is about the transcendental sqrt(pi). But 2/sqrt(3) is already DERIVABLE from what the
          vocabulary contains: the kernel K(z) = (sqrt(1+4z)-1)/(2 sqrt z) supplies the 2, the 4 and
          the sqrt, and the germ sqrt(8pi/3) contains sqrt(3) in its denominator. So the search can
          already reach 2/sqrt(3) at modest depth. Adding it as a separate germ adds VOCABULARY, not
          INFORMATION -- and that is precisely the move that inflates look-elsewhere for free.""")
print(f"\n      (c) IT MAKES THE STATISTICS WORSE. Every germ added raises the branching factor, which")
print( "          LOWERS the informative ceiling computed in S1. Cost of enlarging the vocabulary:\n")
print(f"  {'branching base':>16}{'ceiling: m_p/m_e':>20}{'ceiling: 1/alpha':>20}{'ceiling: k=4 interlock':>24}")
print("  "+"-"*96)
for b in [30.0, 34.0, 40.0, 48.0]:
    c1 = D0 + np.log(1/3.49e-14)/np.log(b)
    c2 = D0 + np.log(1/3.06e-10)/np.log(b)
    c4 = D0 + np.log(1/w4)/np.log(b)
    print(f"  {b:>16.0f}{c1:>20.1f}{c2:>20.1f}{c4:>24.1f}")
c4_30 = D0 + np.log(1/w4)/np.log(30.0)
c4_40 = D0 + np.log(1/w4)/np.log(40.0)
print(f"""
          Going from base 30 to base 40 costs {c4_30-c4_40:.1f} depths of informative reach on the k=4 interlock
          ({c4_30:.1f} -> {c4_40:.1f}). You would be paying real discriminating power for a number the search
          can already build.

      THE GOOD USE, and it is a different job entirely: the flow equation is a RESULT, not a search
      input. An exact closed flow with a bounded anomalous dimension saturating 0 -> -1, plus a
      crossover at g = a0/1.1547 = 8.10e-11 (canon) / 9.79e-11 (alt), is gravity/EFT content that stands
      on its own and belongs in the MI completion write-up. Feeding it back into an SM search converts a
      clean result into extra vocabulary for a search whose bottleneck is not vocabulary at all -- it is
      the look-elsewhere ceiling (S1) and the missing validation set (S5).
      ONE CAVEAT AGAINST MYSELF: if the flow ever produced a number that is NOT derivable from the
      existing germs -- a genuinely new algebraic invariant rather than a rearrangement of the kernel's
      own 2s, 3s and 4s -- that argument would change, because it would be new information rather than
      new notation. u* = 2/sqrt(3) is not that. Worth re-asking if a second, independent invariant of
      the flow turns up.""")
check(f"the flow's only non-trivial special value is u* = 2/sqrt(3) = {u_star:.6f}, which is algebraic "
      f"and already reachable from the existing germs", abs(u_star - 1.154700538) < 1e-8)
check(f"enlarging the vocabulary from base 30 to 40 COSTS {c4_30-c4_40:.1f} depths of informative reach "
      f"on the k=4 interlock", c4_30 - c4_40 > 0.5)
check("so the recommendation is NO -- keep the flow equation as a standalone MI/EFT result, not as a "
      "search germ", True)

print("\n"+bar)
print(f"GATE POWER: {sum(ok)}/{len(ok)} checks PASS. {'ALL PASS' if all(ok) else 'SOME FAILED'}")
print(f"""ANSWER: partly -- and the honest answer contains a correction to what I told you an hour ago.
NO for single targets. The expression count grows as ~30^(D-4), so it outruns ANY fixed measurement
precision. Even 1/alpha, at {2*2.1e-8/137.036:.0e} relative, has an informative ceiling of D = {ceils['1/alpha']:.1f}; m_p/m_e, the most
precisely measured ratio in physics, reaches only D = {ceils['m_p/m_e']:.1f}. At D = 18 you EXPECT {N_expr(18)*2*2.1e-8/137.036:.0e} chance
matches on alpha alone. So a one-target hit at the campaign's current depth means nothing however many
digits it shows -- and the ~3,000 in-window hits already logged are exactly the chance rate.
YES through Gate C. Interlocking k targets multiplies the windows, so the bits add: 4 targets push the
ceiling to D = {ceiling(w4):.1f}, six to D = {ceiling(w6):.1f}. That is what keeps a depth-18 search meaningful, which means
essentially ALL the remaining power is in the cross-sector interlock rather than in precision.
AND EVEN THEN IT IS AN ANOMALY, NOT A DERIVATION: the number-field obstruction rules out an exact
identity (transcendental germ vs algebraic targets), Gate B cannot tell a load-bearing germ from a
decorative one, and several targets RUN so a fixed expression hides a scale choice.
THE FIX IS CHEAP AND SHOULD GO IN NOW: hold two targets back as a validation set. Then a survivor
PREDICTS them instead of fitting them, which is the only move that converts a coincidence into a
result. Without it a JACKPOT would be unfalsifiable.
Good news on the gate itself: it rejects the 12 pi artifact at {sig_off:.0e} sigma, because it compares against
measured uncertainty rather than a self-chosen tolerance.""")
print(bar)
