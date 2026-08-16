# INTERP 0048 — the weak mixing angle as the shared bridge number

SEED 0048 collided three fragments:
  * M_lens/M_dyn = 29 at the f = 1/3 fixed point "measured by" m_W/m_Z = 0.8814
  * an entropy partition of sin^2 theta_W = 0.2312 sets the 0.108-dex RAR at Ups = 0.70
  * wildcard: what single dimensionless number do BOTH bullets share if true?

## Charitable decipherment
The two SM numbers quoted are NOT independent. m_W/m_Z = cos(theta_W) = 0.8814 and
sin^2(theta_W) = 1 - (m_W/m_Z)^2 = 0.2231 (on-shell 0.2312). Both are two faces of ONE
number: the Weinberg weak-mixing angle theta_W. So the wildcard answer is: **theta_W**
(the weak mixing angle) is the single dimensionless number both bullets share if the
collision is real. The bridge claim: one electroweak parameter simultaneously (a) projects
the lensing/dynamical mass ratio M_lens/M_dyn = 29 at f = 1/3, and (b) via an entropy
partition sets the RAR offset 0.108 dex at Ups = 0.70.

## Hypothesis (H)
theta_W is the sole free input. There exist monotone maps
  F( theta_W ) -> M_lens/M_dyn    and    G( theta_W ) -> RAR offset(dex)
such that at the measured theta_W (sin^2 = 0.2312, m_W/m_Z = 0.8814),
  F( theta_W ) = 29        and        G( theta_W ) = 0.108.
Both maps share the same argument; they are NOT fit independently.

## Exact test (T)
1. Build F and G so that F(0.2312)=29 and G(0.2312)=0.108 with theta_W the ONLY input
   (no separate constants, no a0 footing — see note).
2. COINCIDENCE GATE: the same theta_W must land BOTH targets. Sweep theta_W and require a
   single theta_W* in the window [0.229,0.234] to hit M_lens/M_dyn in [28,30] AND RAR in
   [0.103,0.113] dex. If the two targets require two different theta_W*, H fails.
3. JOINT p-VALUE: treat the two observables as having independent experimental errors
   (M_lens/M_dyn ~ +/3; RAR offset ~ +/0.01 dex). The probability that ONE free parameter
   pinned by coincidence reproduces BOTH is ~ P1*P2. Report it; a "hit" must clear a
   pre-stated joint threshold (use mm_search.py so FDR is self-registered).
4. Both footings (a0 = 9.3619e-11 / 1.1279e-10): all three targets are DIMENSIONLESS
   ratios, so they are footing-AGNOSTIC; state that explicitly. If any acceleration scale
   enters F/G, report both footings and show the targets are footing-independent.

## Kill condition (K)
H is REFUTED if ANY of:
  - F(0.2312) or G(0.2312) misses its target band (29+/-3, 0.108+/-0.01);
  - the two targets need two different theta_W* (no single coincident value);
  - the joint coincidence p-value exceeds the pre-stated threshold.
A single theta_W that cannot pin both numbers simultaneously is a coincidence, not a bridge.

## Falsifiability / status
Pure prediction: theta_W is the shared number. No a0, no kappa=1/2 (kappa is FITTED,
0.551+/-0.043, not derived). If blind referee finds F/G need extra free constants, that is
the falsifier working. Grade: REFUTED/NULL/DISCARD all acceptable outcomes.
