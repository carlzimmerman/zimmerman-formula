# INTERP 0051 -- charitable decipher of seed_0051 (blind referee to follow)

## Charitable reading
Bullet 1: the dust-mass-IS-charge theorem (rho/n = Q0) carries a boundary-term
ratio that equals sin^2(theta_W) = 0.2312.
Bullet 2: the muon/electron mass ratio m_mu/m_e = 206.768, taken as a BEAT
frequency omega_beat = (m_mu - m_e) c^2 / hbar, "selects the drain flow."
Wildcard: a SINGLE dimensionless number D is shared by BOTH bullets.

## Shared number
D = sin^2(theta_W)^OS = 0.2312. Both routes must land on this same value.

## Hypothesis H (one, falsifiable)
A single "drain-flow" parameter D is set IDENTICALLY by
  (i)  the dust-mass-is-charge boundary-term ratio  D_bound = B_1 / B_2,
      evaluated at the a0 transition radius r0, and
  (ii) the muon-electron beat selection   D_beat = omega_beat / omega_ref,
      with omega_ref = a0 / c.
and D_bound = D_beat = 0.2312 on BOTH a0 footings.

## Exact quantities
- sin^2(theta_W)^OS = 0.2312, unc ~2e-4 (PDG)
- m_mu/m_e = 206.768(12);  omega_beat = (m_mu - m_e)c^2/hbar
- B_1, B_2 = the two boundary terms of the rho/n = Q0 action
- footings a0 = 9.3619e-11 and 1.1279e-10 m/s^2 (both required)

## Exact test (reproducible, NOT run here)
1. D_bound = B_1/B_2 at r0, each footing.
2. D_beat  = (omega_beat) / (a0/c), each footing.
3. PASS iff |D_bound - 0.2312| < 4e-4 AND |D_beat - 0.2312| < 4e-4
   on BOTH footings AND D_bound agrees with D_beat to within that tol.
   Use mm_search.py (it self-pre-registers FDR); a CONVENTION-grade match
   does NOT count as a hit.

## Kill criteria
- Either route misses 0.2312 by > 2x its uncertainty, or > mm_search 2-sigma
  band => REFUTED.
- D_bound and D_beat disagree with each other => REFUTED (not a single number).
- 0.2312 is reachable only by a FIT (free parameter), not an a-priori map
  B_1/B_2 or omega_ref => CONVENTION match => DISCARD (protocol).
- No a-priori simple selection map omega_beat -> 0.2312 can be written without
  reference to 0.2312 => unfalsifiable-as-stated => mark NULL, do not pursue.

## Honest caveat
The selection map and B_1/B_2 must be fixed WITHOUT reference to 0.2312; if
they cannot, this is p-hacking and the referee should DISCARD, not PURSUE.
kappa = 1/2 is FITTED (0.551 +/- 0.043), never claimed derived.
