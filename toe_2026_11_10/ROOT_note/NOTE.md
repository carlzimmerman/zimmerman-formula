# ROOT note: why the TOE swing failed, in one line (2026-11-10)

A note, not a graded lane: no criteria were committed before the script. Adopts nothing. kappa = 1/2 FITTED; not theory
closed. Script `root.py`, output `root.out` (sympy, exact).

## The result

TOE0 failed T2 (QG1: no weakly coupled flat vacuum) and T3 (HZ1: the law's function cannot sit in a renormalizable UV
action). Both failures are the same fact, and the fact is MOND itself, not action (A)'s choice of mu.

In the khronometric form (GR + (a0^2/K) J(u), u = |A|/a0) the law is mu(x) = 1 - J'(x)/x. Any interpolating function
with a deep-MOND regime, mu(x) = x + m2 x^2 + m3 x^3 + ..., forces

    J = u^2/2 - u^3/3 - (m2/4) u^4 - (m3/5) u^5 + ...

whatever m2, m3 are. Two consequences:

1. **alpha(0) = 2 exactly.** At zero acceleration the law's quadratic term cancels GR's lapse-gradient term, which is
   Blas-Pujolas-Sibiryakov's G_N = G/(1 - alpha/2) -> infinity point. The khronon scalar's speed^2,
   (beta + lambda)(2 - alpha)/[...], is then 0 for every beta and lambda. No choice of the other khronometric couplings
   gives the vacuum a restoring force. That is T2's Minkowski FAIL.
2. **The leading surviving term is -|A|^3/3 = -(A.A)^(3/2)/3.** It is odd in |A|, so it is not a polynomial in A_i, and
   no power-counting-renormalizable action contains it. That is T3(i)'s FAIL.

Control: a non-MOND mu with mu(0) = 1/2 gives alpha(0) = 1 and escapes (1). The MUTATE bites.

**In words:** deep MOND is gravity tuned to the point where the Newtonian response diverges, with a scale-invariant
cubic as what is left. Deep MOND's space-time scale invariance is Milgrom's (arXiv:0810.4065; PROVISIONAL). A
fundamental field theory cannot sit there: its vacuum is strongly coupled, and its leading term is non-analytic. So
**MOND cannot be a fundamental term in a TOE. It has to be emergent: the infrared fixed point of some sector**, with
gravity's Gaussian (Newtonian) regime crossing over to it at a0. Non-analytic, scale-invariant response and strong
fluctuations at the critical point are what fixed points do. At a fixed point they are expected, not defects.

## What that makes the path to a TOE

One missing object, stated as precisely as the record allows:

- **A sector whose infrared fixed point, coupled to the clock's acceleration, has free energy -(M_Pl^2/a0)|A|^3/3**
  (in the units above) and crosses over to the Gaussian A^2 term at |A| ~ a0. In 3-d space, deep MOND's
  (grad phi)^3 is conformally invariant, so the natural candidate is a 3-d conformal sector on the clock's slices.
- Its crossover scale must be set by the only infrared scale available, the horizon (a0 ~ cH). That is the form the
  record already forces by four routes.
- If such a sector exists, kappa would be a universal amplitude ratio of its fixed point (computable, not fitted). The
  record's walls (sqrt(pi) wall, "kappa irreducibly free") were proved for the June geometric and thermal routes, not for
  a fixed point's amplitude ratio. They bind only if the sector's normalization runs through 8 pi G.
- T2 would then read differently: strong coupling at A = 0 is the fixed point's own regime. But T2 is frozen and stays
  FAIL; a new gate would have to grade the sector.

What is not known: whether any such sector exists. HZ1 tried five perturbative ones (one had the right shape and missed
the size by 10^55.4). Lane NPJ1 (`toe_2026_11_10/NPJ1_nonperturbative_J/`, running) is computing the non-perturbative
candidates. Nothing here is a derivation of the sector.

## Scope

- Proved for the khronometric form (the record's (A), Blanchet-Marsat type). For a separate-scalar MOND (AQUAL; AeST's
  phi) the deep regime is the same (grad phi)^3 with no quadratic gradient term at grad phi = 0. That is the same
  structure, stated in words here, not computed.
- Time-nonlocal modified inertia evades the theorem (it has no local J). The June record walled that route for other
  reasons (Milgrom 1994 no-go; the T_eff -> m_eff mechanism a GAP).
