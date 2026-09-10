# arXiv:2404.06584 (JCAP 11 (2024) 040) vs the health branch — a structural comparison

Read from the cached full text. All quotes verbatim.

## Their theory

    S = (c^3/16 pi G) INT d^4x sqrt(-g) [ R - 2 J(Y) + 2 K(Q) ]  +  S_m[Psi, g]     (2.6)

with a Khronon scalar `tau` defining the foliation exactly as we do:

    n_mu = -(c/Q) grad_mu tau ,   Q = c sqrt(-g^{mu nu} grad_mu tau grad_nu tau)     (2.1)-(2.2)
    A_mu = c^2 n^nu grad_nu n_mu = -c^2 q_mu^nu grad_nu ln Q                          (2.3)
    Y   = A_mu A^mu / c^4                                                             (2.5)
    K(Q) = mu^2 (Q-1)^2                                                               (2.7)

In adapted coordinates `tau = t`, `Q = c/N`, so `ln Q = ln c - ln N` and **`A_mu` is the LAPSE
ACCELERATION** `+c^2 q grad ln N`. Their MOND function `J(Y)` is therefore a function of the
**squared lapse acceleration**. Their `K(Q)` is a **ghost-condensate** term; they say so:
"A similar term appears in the case of ghost condensation ... K(X) = mu^2(X+1)^2 with
X = c^2 grad_mu phi grad^mu phi ... phi = tau and X = -Q^2 in our case."

## What is THE SAME as ours

1. A **clock/Khronon scalar defining a preferred foliation** — same object, same construction.
2. Preferred-frame structure with GR recovered in the high-acceleration limit.
3. A **non-propagating scalar sector at linear order**: "only two are propagating which are the
   usual massless tensor modes as in GR. The third degree of freedom is non-propagating (it has
   omega = 0 and so there is no associated wave)".
4. Both target MOND + Solar System + cosmology from one foliation-based action.

## What is DIFFERENT — and both differences are exactly the load-bearing ones

### (A) The MOND source. Theirs is the LAPSE ACCELERATION; ours is not.
Theirs: MOND enters through `J(Y)`, `Y = A_mu A^mu` = squared lapse acceleration.
Ours: MOND enters through `|D phi|^2`, the **leaf-projected spatial gradient of a SEPARATE
non-propagating field**, deliberately NOT the lapse — because our internal analysis (L117/L119)
found that sourcing MOND from the lapse acceleration liberates the metric conformal mode as a
ghost (`H_0 = -p^2/(12 M^2) < 0`), and moving the source off the lapse makes the lapse Hessian
vanish identically so `H_perp` stays first-class.

**HONESTY NOTE — do NOT claim their paper confirms our conformal-ghost result.** It does not.
They attribute their instability explicitly to the OTHER term: *"the linear instability found
above ... is due to the 'condensate' term mu^2(Q-1)^2"*. Their `J(Y)` is not identified as the
culprit. Whether MOND-from-lapse independently carries our conformal ghost is UNTESTED against
this paper and remains our own internal claim.

### (B) The dark sector — and this is the pincer, occupied on both horns.
Theirs: `K(Q) = mu^2(Q-1)^2`, a ghost-condensate kinetic term. It generates the effective a^-3
dust that fits the CMB ("reduces to a subset of the generalized dark matter (GDM) model"), i.e.
dust with **small but FINITE sound speed** -> it CLUSTERS -> the third peak works.
The price, in their own words: the deconstrained Hamiltonian is *"bounded from below for
wavenumbers larger than ~10^-31 eV and unbounded for smaller wavenumbers"*, and *"the same type
of Jeans instability persists also at the MOND limit"* (mu^-1 ~ 22.3 Mpc).

Ours: the cuscuton's degree-1 sqrt-kinetic term. L128 showed it gives **exactly** pressureless
a^-3 dust (rho = V, p = 0 exactly, Friedmann reproduced identically) with **zero** extra
propagating DOF — but `c_s^2 = infinity`, so it is smooth at every scale, and L129's controlled
Boltzmann run showed smooth dust **fails the third peak** (peak3/peak2 = 0.5545 vs 0.9906).

**So the two theories occupy the two horns of the SAME pincer, both explicitly:**

| | kinetic term | c_s | clusters? | CMB | health |
|---|---|---|---|---|---|
| arXiv:2404.06584 | `mu^2(Q-1)^2` (condensate, degree 2) | finite | YES | **PASS** | **IR-unbounded Hamiltonian, k < mu** |
| health branch | `mu^2 sqrt(X)` (cuscuton, degree 1) | infinite | NO | **FAIL** (L129) | bounded; 0 extra DOF |

This is the strongest available evidence that the L128 pincer is **structural rather than a
failure of imagination**: clustering requires finite c_s; finite c_s is what carries the
instability. Two independent constructions, opposite choices, each paying the predicted price.

### (C) Degrees of freedom and closure.
Theirs: **three** dynamical DOF on Minkowski (2 tensor + 1 non-propagating-but-dynamical, whose
solution is secular, `A_k + B_k t`). They state the non-propagation is a LINEAR-ORDER artifact:
*"the higher order terms (for instance, the MOND term), will effectively lead to a non-linear
propagation equation for the third degree of freedom, that is, the non-propagating omega = 0 mode
will become propagating."* And the full Hamiltonian analysis is *left to future work*.
Ours: the cuscuton is fully constrained — 0 extra DOF, with the closure/Dirac chain proven.
This is a genuine advantage of ours, and it is the unachieved combination the literature map
identified (G2-published + G6 + G8 has never been done).

### (D) alpha_1.
Theirs: `alpha_1 = -8(alpha - beta)/(1 - beta)` with `alpha -> 0` only in the HIGH-acceleration
regime, and `alpha -> 1` in deep MOND. So their preferred-frame null is **asymptotic**, and a
pointwise read gives `alpha_1 -> -8` in the deep-MOND regime where MOND is actually tested.
Ours is **exact and structural** (shift-independence to all orders). Note the literature map's
"silence" finding: *no preferred-frame analysis in the low-acceleration regime exists for ANY
theory* — so this is an open, publishable calculation and a natural discriminator.

## Bottom line
Same skeleton (foliation clock scalar), different in exactly the two places that decide the
outcome: **where MOND is sourced from**, and **which kinetic term supplies the dark sector**.
They bought the CMB with a condensate and paid with an IR-unbounded Hamiltonian and an
undetermined nonlinear DOF count. We kept health and exact alpha_1 and paid by not clustering.
Neither is a complete theory. The pincer between them is now concrete, not conjectural.
