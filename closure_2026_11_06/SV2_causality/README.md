# SV2: AC18's light-cone failure is PHYSICAL (forced, paradox-free); NO REPAIR IN the standard khronometric CLASS; MUTATE BITES

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md and iter_k/FROZEN_CRITERIA.md
(7d31bb0ac2, pushed as dade339cae), frozen alone before any script or number. Input: AC18 (505affaed6).
Scripts: sv2_common.py (AC18's kernel H and g_hat coefficients, rebuilt verbatim), iter_1_physical/sv2_iter1.py,
iter_2_repair/sv2_iter2.py, iter_3_mutate/sv2_iter3.py (single thread, nice 15, seconds each).
Lean: fable_independent_2026/lean_2026/SV2_causality.lean, SV2_repair.lean (exit 0, 0 sorry, axioms propext,
Classical.choice, Quot.sound); twins SV2_causality_MUTATE.lean, SV2_repair_MUTATE.lean (every planted claim fails,
exit 1). Both footings throughout, never pooled.

## Labels

| step | label | why |
|---|---|---|
| iter_1 | **PHYSICAL**, FORCED, PARADOX-FREE | The signal reaches test matter and carries the sender's choice. Its size is set by G, c, and the law-forced Pi and x only. Tau-ordering closes no loop for any observer. |
| iter_2 | **NO REPAIR IN CLASS** | Neither alpha a^2 nor beta K_ij K^ij nor lambda K^2, at any healthy value, removes the instantaneous mode (Lean). lambda makes it 1e13 larger at the bound edge. |
| iter_3 | **BITES** | Flipping alpha gives a ghost and flipping beta + lambda gives a gradient instability. The instantaneous mode stays. All Lean planted claims fail. |

## iter_1: is the failure physical?

- **D1 (reaches matter).** The detector is the tidal tensor E_ij = c^2 R_0i0j of a free test pair at rest in the
  khronon frame. It is sourced through retarded linear GR by the khronon's dq and Pi dv in the observer's own past
  ball: E_ij = 4 pi G (4 Q_ij - delta_ij dq). Values at (1 s, 1e10 m):
  - canonical: |E| = 2.1e-111 to 6.2e-111 s^-2
  - alt: |E| = 6.0e-111 to 6.7e-110 s^-2

  These sit 2.5e15 to 3.3e15 above the floor on all 36 rows. The strain of a 1 m pair is 1e-111 to 5e-110 after 1 s.
  The local khronon energy density changes by c^2 dq ~ 1e-86 J/m^3. Energy delivered to a free pair is second order
  in the source.
- **D2 (information).** Flipping the source direction at t = 0 changes E outside the cone, at 2.3e15 to 3.3e15 times
  the floor on every row.
- **FORCED.** dv = C(x, n) K Pi G m c^2 v_s t^6 / r^5:
  - The coefficient C agrees across the three (t, r) cells to 5e-51, and dv is exactly linear in Pi.
  - The gamma (Lstar) part of the symbol is a polynomial, so it acts only on the source.
  - C_max is 0.067 (canonical) and 0.49 (alt).
  - Because r > c t, the outside-cone signal obeys |dv| <= C_max (t/t_dyn)^2 G m v_s/(c^3 t), with
    t_dyn = (4 pi G Pi)^-1/2 = 19.9 / 18.6 Myr. At t = 1 s this is <= 4.2e-64 / 3.6e-63 m/s for a ton at 1 m/s.
  - The suppression (t/t_dyn)^2 is the only small number, and it is not a chosen one. The leading-order expansion
    holds for t << t_dyn only.
- **PARADOX-FREE.**
  - Lean proves four things: tau advances along every future causal displacement when grad tau is timelike; a chain
    with one positive leg cannot close; a luminal return arrives at t >= L/(c + |w|); a boosted observer can see an
    instantaneous leg run backward.
  - The sweep covered 3380 loops, with emitter speeds up to 0.999999 c. 1416 of them run backward in the emitter's
    frame. None closes: the minimum t* c / L is 0.50000025 = 1/(1 + |w|/c).
  - The leaves are spacelike on the background (1 - v^2/c^2 = 0.99999946).
- **KA and MUTATE.** KA1 (x = 0) and KA2 (Pi = 0) both give zero. MUTATE uses AC18's hyperbolic leaf, with earliest
  arrival 54 s against a 1 or 10 s sample. It returns HARMLESS-BY-STRUCTURE on both footings, so the control bites.

What this means: the gate failure is a real, information-carrying, tau-ordered signal. It is the Blas-Pujolas-
Sibiryakov instantaneous mode of preferred-foliation theories, and it cannot be used to build a causal paradox. It
is not light-cone causal. No data constrain it.

## iter_2: the standard khronometric terms

- **Derivation.** Sympy derived the leaf-mode dispersion exactly from the Euler-Lagrange equations of the weak-field
  L2 with alpha, beta and lambda added: omega^2 = (Pi + l2 k^2)/(1/Z + alpha/(2K)), with Z = K f(k_hat) + gamma k^2
  and l2 = (beta + lambda) c^2/(2K). The P equations carry no omega: the leaf constraint survives every term in the
  class.
- **R1: KEPT.** The k -> 0 limit is omega0^2 = Pi K f/(1 + alpha f/2), with f = 1/(k_hat.Mt^-1.k_hat) between 1 + x
  and (1 + x)^2.
  - Its anisotropy is exactly omega0^2(e)/omega0^2(perp) - 1 = 2x/(alpha(1+x)^2 + 2). It does not depend on beta or
    lambda, and it is positive for every alpha >= 0 and x > 0. Lean proves this as `no_repair_in_class`,
    `anisotropy_exact` and `omega0_strict_mono`.
  - The solution kernel is therefore discontinuous at k = 0 and is not supported in any ball (Paley-Wiener-Schwartz).
  - Control: at x = 0 the anisotropy is 0 and R1 returns REMOVED-CANDIDATE, so the test can pass.
- **R1b (sizes, t = 1 s, r = 1e10 m).**
  - The lambda (beta + lambda) term makes matter source the leaf mode at first order in G, through the nonlocal symbol
    l2 K k^2 f(k_hat). Per unit (beta + lambda) this gives |dv_lambda| = 1.0e-44 to 8.5e-43 m/s, which is 2.8e27 to
    9.9e27 times AC18's dv. At the window edge beta + lambda = 2.8e-15 (where c_k = c) it is 8e12 to 2.8e13 times
    AC18. The term amplifies the mode instead of removing it.
  - The alpha channel changes the kernel f -> f/(1 + alpha f/2). At the symbol level the relative change is <= 6e-15
    (canonical) and 1.8e-14 (alt) on the alpha = 2 beta line, and <= 5.8e-5 / 1.6e-4 at alpha = 2.5e-5.
- **R2.** c_k^2 = (beta + lambda) c^2/alpha, isotropic. This reproduces the standard result (known answer, PASS). At
  alpha = 0 the large-k speed is infinite. A finite c_k is available, but only for the principal part: the order-0
  anisotropic term stays.
- **R3 (health).** alpha >= 0 is ghost-free at all k, and beta + lambda >= 0 is gradient-stable (Lean).
- **R4 (window; literature formulas, provisional, not re-derived on v3s).**
  - beta lies in (-6e-15, 1.4e-15), from c_T^2 = 1/(1-beta) and GW170817.
  - |alpha - 2 beta| <= 2.5e-5, from alpha1 = 4(alpha - 2beta)/(beta - 1) and LLR.
  - alpha2 is proportional to (alpha - 2 beta).
  - Health requires alpha >= 0 and beta + lambda >= 0. c_k <= c in addition needs beta + lambda <= alpha.
  - On the alpha = 2 beta line, alpha <= 2.8e-15. The R1 verdict does not use the window.
- **R5 (static law).** The beta and lambda terms vanish on static leaves. At alpha = 2.5e-5 the change in g is
  <= 8.6e-5 dex (with G_N absorbed) over g_N/a0 from 1e-3 to 1e3, and min(mu - alpha/2) = 0.031. This passes on both
  footings: the result is identical in g/a0.
- **Structural reason.** Both the k -> 0 anisotropy and AC18's signal come from the law's own anisotropic Hessian
  (x > 0) together with a nonzero charge Pi. Both are forced wherever the theory does MOND. Inside this class only
  x = 0 or Pi = 0 removes them. A term outside the class (for example a kinetic term for P) is not tested here.

## iter_3: MUTATE (window-edge member alpha = 2 beta = 2.8e-15, beta + lambda = alpha)

- **M1 (alpha -> -alpha).** A ghost appears above k = 5.65e-11 / 5.36e-11 m^-1 (scale 1.8e10 m). The unflipped
  member is ghost-free at 10x that k.
- **M2 (beta + lambda flipped).** Modes go gradient-unstable above k = 1.42e-16 / 1.52e-16 m^-1 (0.23 / 0.21 pc). The
  growth rate is 1.1e-11 / 1.3e-11 s^-1 at 10 k_grad.
- **M3.** The anisotropy stays at x (1.15 / 2.6) under both flips, so the instantaneous mode is kept.
- **Lean twins.** All seven planted claims fail:
  - a spacelike leg advances tau;
  - a chain with legs of any sign advances;
  - a return leg arrives at t = 0;
  - the leaf frequency is isotropic at x > 0;
  - omega0^2 decreases with f;
  - alpha < 0 is ghost-free;
  - beta + lambda < 0 is stable.

## Slips, disclosed

- **iter_1 row selection.** The first main run selected the "ct/r = 0.03" rows by matching 0.03 to 1e-9. The actual
  value is 0.02998, so no row matched and the label printed HARMLESS-BY-STRUCTURE even though D1 and D2 were true on
  every row. The selector was fixed to the frozen cell (t 1 s, r 1e10 m) and the script rerun; numbers are unchanged.
- **iter_3 criteria formula.** The criteria wrote k_ghost = (2/Lstar) sqrt(2/|alpha| - f). The correct closed form is
  sqrt(2)/Lstar times the same root. The script finds the root numerically, and the root agrees with the corrected
  closed form to 8 digits.
- **Lean build.** At run time this checkout's lean_2026/.lake had no Mathlib build: something else re-created the
  .lake folder at 21:08 with sources only. The .lean files were compiled with `lake env lean` from a sibling checkout
  that has the identical toolchain (v4.34.0-rc2) and the same Mathlib rev (85e3a25e). Nothing was downloaded or
  rebuilt.

## Not done

- 1PN stresses of the P / Xi sector in E_ij. They are a different order in Pi, so they cannot cancel the computed
  term.
- Strong-field leaves, and orders beyond leading in G and t.
- Exact PPN alpha2 and the BBN bounds (literature, provisional).
- Recomputing AC2q separately. AC18's regulator bound of <= 6e-32 carries the leaf result to AC2q.
- Testing out-of-class terms, such as a kinetic term for P.

Kappa = 1/2 FITTED; not theory closed.
