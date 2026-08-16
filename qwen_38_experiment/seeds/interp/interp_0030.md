# INTERP 0030 -- one shared RG slope (charitable read of SEED 0030)

SEED: (1) a projection of R_dm=0.387 sets m_W/m_Z=0.8814.
      (2) the "torsion" of n_s=0.9649 bounds the fixed-point argument (drain vs pin).
      (3) wildcard: the single dimensionless number BOTH bullets share.

## Hypothesis (single sentence)
There is ONE dimensionless RG eigenvalue gamma at the framework fixed point that
appears in both bullets: bullet 1 is the linearized projection of the dark-matter
scale R_dm toward that fixed point, and bullet 2 is the same gamma read off as the
spectral-index "torsion" (running); the drain-vs-pin verdict is the SIGN/magnitude
of gamma.

## Bullet 1 -- exact test
- Quantity: m_W/m_Z (cos theta_W) = 0.8814; input R_dm = 0.387.
- Project by the 1-parameter map P(R) = R + gamma*(R - R*)  iterated to fixed point
  R* = 0.387, then read cos theta_W = P-infinity(R_dm); OR the simpler claim
  m_W/m_Z = P(R_dm) with P a monotone map using gamma as its only knob.
- KILL: if reaching 0.8814 from 0.387 needs >1 free parameter beyond gamma, or
  lands off 0.8814 by > 3 sigma, bullet 1 is REFUTED.
- Both footings on any dimensional projection (9.3619e-11 / 1.1279e-10):
  if P mixes in a dimensionful a0, report under both and require agreement.

## Bullet 2 -- exact test
- Quantity: n_s = 0.9649; its "torsion" = the running alpha_s = dn_s/dln k
  (Planck ~ -0.005) OR the slow-roll curvature eta entering 1 - n_s = 2 eps - eta.
- Drain = attractive fixed point (gamma<0, generic); pin = pinned (gamma->0+,
  fine-tuned). Bound: |torsion| must lie on the drain side for the fixed point to
  be generic; on the pin side it requires fine-tuning.
- KILL: if |alpha_s| puts the flow on the pin side, the "drain" reading dies and
  the hypothesis must be restated as a pinned (non-generic) claim -- DISCARD unless
  the pin is itself predicted.

## Wildcard -- the shared number
Charitable candidate: gamma itself is the shared dimensionless number, and numerically
the seed hints gamma ~ (1 - R_dm) = 0.613 ~ 1/phi = 0.618 (golden-ratio conjugate)
OR gamma ~ the running alpha_s. STATE this as a flagged guess, NOT a hit:
a golden-ratio coincidence is a CONVENTION-grade / p-hacking risk per PROTOCOL and
must NOT be counted as confirmation. The falsifiable content is: ONE gamma serves
both bullets; two independent gammas => REFUTED.

## Overall
If gamma can be extracted from bullet 1 and independently from bullet 2 and they agree
to within their errors -> PURSUE. If they disagree -> REFUTED.
If bullet 1 needs >1 knob -> REFUTED. If bullet 2 is on the pin side -> DISCARD.
HONESTY: kappa=1/2 is FITTED (0.551 +/- 0.043), not derived; do not claim otherwise.
