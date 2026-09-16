# H038 and H043 — two structural results

## H038 — R10 CLOSED: phidot = 0 is an IMPOSED CONSTRAINT, not an attractor
18 Lean theorems, exit 0, ZERO sorry. 27/27 python.

Three measured facts:
1. **Kinematics.** In homogeneous FLRW, K = -phidot^2/(2 Lambda^4) <= 0 for every
   real phidot. The domain K >= 0 is the SINGLE POINT phidot = 0 — no
   neighbourhood, so "attractor" cannot even be posed.
2. **Reality.** Off the locus, f'(K) = mu_2(iw) = [w^2(w^2+3) + 2iw]/(1+w^2)^2
   has Im = 2w/(1+w^2)^2 != 0 for all w != 0. The Noether current a^3 f' phidot
   is COMPLEX, so no real rolling FLRW solution exists.
3. **No protection.** f'(K) <= 2 sqrt(K) -> 0 as K -> 0+: the principal
   coefficient VANISHES at the frozen point. No barrier, no restoring force,
   and the linearised EOM is 0 = 0. K = 0 is a flat minimum.

phidot decays as a^-3/2 in modulus ONLY OUTSIDE the domain (K < 0 at all 4000
samples on every trajectory).

**Consequence:** any future lane wanting a rolling cosmological scalar must
postulate a real extension of f to K < 0. It cannot be read off this Lagrangian.

## H043 — D = 4 IS THE UNIQUE CONSISTENT DIMENSION
32 Lean theorems, exit 0, ZERO sorry. 13/13 python.

Three INDEPENDENT selectors, none of them H030's mode count:

1. **Dimensional.** r_M = sqrt(GM/a_0) has dimensions L^((D-2)/2) — a length
   ONLY at D = 4. At D = 5 the ratio r/r_M carries L^(-1/2) and cannot equal a
   mass ratio.
2. **Flatness.** Deep law with g_N = GM/R^(D-2) gives
   d ln v / d ln R = (4-D)/4. D = 5 => v ~ R^(-1/4): a 44% decline per decade,
   against SPARC flatness of a few percent.
3. **BTFR.** M ~ V^(2(D-2)). Observed exponent 3.85 +/- 0.09 implies
   D = 3.925 +/- 0.045.

**Honest negatives — these do NOT select D:**
- Sigma_ph universality survives in EVERY D (mass-independent to 1e-16 over 6
  decades; only the geometric prefactor A_k = pi^(k/2)/Gamma(k/2+1) changes).
- c_s^2 = (u^2+3u+2)/(u^2+3u+4) is provably D-free, with 1/2 <= c_s^2 < 1.
  Stability gives NO constraint.

**Caveat:** a_0 = (1/2) c sqrt(G rho_Lambda) was deliberately NOT used (H029
circularity). This is a consistency derivation from the framework's own laws
plus SPARC-class facts, not pure first principles.

**Note:** H038_results.json holds Agent B's attractor run; Agent H also wrote
H038_dark_matter_density_profile.py to the same number — a collision.
