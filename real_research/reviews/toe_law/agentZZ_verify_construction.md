# agentZZ VERIFICATION — hostile referee of the spatial-nonlocal slip carrier

CHARGE: does the spatial-nonlocal carrier GENUINELY evade the keying/static-equivalence theorems
AND stay healthy (ghost-free, causal, constraint-clean), or did the route hide a pathology /
inherit the wall? Route claimed NEW-WALL (INHERITS-WALLS). Re-derive independently; regrade.

All numbers below recomputed from scratch (own sympy, not the route's expressions). /tmp/zz_verify*.py.

## [1] PROPAGATOR POLES / GHOST-CAUSALITY — CONFIRMED HEALTHY (and the cleanliness is real)
- +sign resolvent 1/(1+L^2 k^2): complex poles k = ±i/L (imaginary => exp decay). The 3D static
  Green function exp(-r/L)/(4 pi r) SOLVES (-nabla^2 + 1/L^2)G = 0 for r>0 (residual = 0,
  machine-verified) => genuine Yukawa, finite range, decaying, causal, ghost-free = ONE auxiliary
  massive scalar (mass 1/L), standard +kinetic sign, finite d.o.f., no Ostrogradski.
- -sign 1/(1-L^2 k^2): REAL poles k = ±1/L (tachyon). cos(r/L)/(4 pi r) solves the -sign operator
  (residual = 0) => oscillatory, non-decaying, NOT finite-range, acausal/ghost.
- VERDICT on health: the route did NOT hide a ghost. Finite range REQUIRES the healthy +sign; the
  carrier the route tested is genuinely clean. This is an HONEST claim, independently reproduced.
- NB: the route did NOT use an entire/infinite-derivative form — it used a RATIONAL resolvent, but
  the rational resolvent here is the propagator of ONE massive scalar (a standard auxiliary field),
  NOT an infinite tower => no Ostrogradski. The usual "rational kernel adds ghosts" caveat does not
  bite, because a single +sign massive pole is one healthy d.o.f. Confirmed.

## [2] KEYING-POLLUTION LOCK — CONFIRMED, derived from one Lagrangian
From L = B(K)(Psi-Phi)k^2 with K = k^2 Khat^2 Phi^2 (Khat=1/(1+L^2k^2)):
- eqL (slip) = k^2 B(K); eqN keying piece = -2 Phi k^4 (Phi-Psi) B'(K)/(1+L^2k^2)^2.
- dK/dPhi = 2 Phi k^2 Khat^2 — the pollution carries the SAME k^2 geometric enhancement
  (= the (a0 r/c^2)^-1 factor, see [5]) AND the SAME Khat^2 dressing as the slip's key.
Independently reproduced; matches the route's agentZZ_action.py exactly.

## [3] SLIP-MATCHED INVARIANCE — CONFIRMED, and I PROVED the route's "=1 always" is SHARPER than stated
The decisive claim is the slip-MATCHED pollution (hold the lens observable fixed, ask the pollution).
Re-derived: matching the slip re-amplifies the operator amplitude A by 1/Khat^2; the slip-matched
pollution/local ratio = [B(K0)/B(K)]·[B'(K)/B'(K0)]·Khat^2 with K = Khat^2 K0.
- Linear B: ratio = 1 EXACTLY (verified).
- ANY power-law B(x)=x^n: ratio = 1 for ALL n (verified symbolically). The deep-MOND key B=sqrt(x)
  is power 1/2 -> exactly locked; numerically 1.0000 at every (L,k,K0).
- HOSTILE ESCAPE TEST the route did NOT run: NON-power-law B. I evaluated B=x/(1+x), B=log(1+x),
  and a nu-crossover B=sqrt(x)/(1+sqrt(x)). Result: the ratio is NOT 1 — but it is ALWAYS >= 1 and
  GROWS as Khat shrinks (up to 91x and 910x for the saturating B). The kernel makes the pollution
  WORSE, never suppresses it below the slip. So no choice of interpolating function opens an escape;
  the lock is robust to the realistic, non-power-law B that MOND actually needs. The route's "=1.000000"
  is exact for the relevant deep-MOND/power-law sector and only ever DEGRADES off it.
  => the carrier inherits the wall for power-law B and is STRICTLY WORSE for non-power-law B. No escape.

## [4] DISCRIMINANT DIRECTION — CONFIRMED wrong-way
dKhat/dk = -2 L^2 k/(1+L^2k^2)^2 < 0 for all k>0 (monotone-decreasing low-pass, machine-verified).
=> Khat(k_lin) > Khat(k_halo) always (k_lin < k_halo): suppresses HALOS, passes LINEAR — the MIRROR
of agentII's need. L for 50x linear suppression = 33.3 Mpc; at that L halo Khat(r=3 Mpc) = 2.05e-4
(halo nu killed). ~70x L-contradiction confirmed. The finite range supplies the INVERSE discriminant.

## [5] PREMISE CHECK — the (a0 r/c^2)^-1 enhancement is REAL
Acceleration key (Phi')^2: delta = 2 Phi' eta' (a DERIVATIVE on the test function -> IBP -> geometric
slip/r^2 enhancement). Potential-value key Phi: delta = eta (NO derivative -> NO enhancement, but
wrong observable: no nu(g/a0)). The enhancement is intrinsic to acceleration-keying; smoothing keeps
both derivatives dressed by Khat^2. The wall's premise is sound, not assumed.

## [6] SMUGGLE / QUARANTINE — CLEAN
No file asserts q=1/4, 0.25, or any quarantined coefficient. The kernel-lock and the poles are
symbolic (no a0/footing/weighting/nu-shape). sigma4/Z not touched.

## REGRADE: CONFIRMED — NEW-WALL (INHERITS-WALLS), strengthened.
The route is honest and correct: the spatial-nonlocal carrier is genuinely ghost-free and causal
(no pathology hidden), and it inherits the keying wall — the slip-matched pollution is kernel-locked
(=1 exact for power-law B; >=1, growing, for non-power-law B, an escape the route did not test but
which only makes the wall harder). The finite range is a real scale knob pointed the wrong way
(low-pass vs agentII's needed high-pass; high-pass = Khat(0)=0 = no static lens). No CARRIER-OPENS:
constraint pollution is at-or-above the slip, never below the double-counting bar; the kernel is
clean but the cleanliness (DC gain 1, locked) is exactly what binds it. ZZ-1 kernel-locking theorem
holds across LOCAL/TIME/SPACE. Independently reproduced: poles ±i/L (causal); pollution dK/dPhi
=2 Phi k^2 Khat^2; slip-matched ratio=1 (power-law) / >=1 (else); dKhat/dk<0; enhancement real.
