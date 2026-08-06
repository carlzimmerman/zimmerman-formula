# DOOR A1 — Publish the strong no-go, correctly scoped
STATUS: OPEN | RANK: 1 | COST: S | KILLS FAST: n/a (banks a result you already own)

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
`linear_response_anti_mond_proof.md` attributes the anti-MOND wall to the KMS condition. **That is not the
wall.** For the exact Bunch-Davies worldline kernel, the commutator spectral function is

    rho(omega) = omega / pi^2      EXACTLY — beta and H cancel identically

because the commutator of a free field is a c-number. Verified two ways in review: by residues (rel dev
<= 5.3e-41) and by scanning random density matrices in a 40-level Fock space (G_> - G_< = 1.000000000000 in
every normalizable state). So delta_m > 0 follows from **microcausality + boson statistics**, not equilibrium.
Leaving equilibrium cannot lift it. The correctly scoped theorem is stronger and more publishable than what
you have: *no state deformation of a linearly coupled free bosonic bath — equilibrium or not — gives
delta_m < 0.*

## Why it works with the framework
It touches nothing in the phenomenology. a0, the a0-line, ν = √(1+1/y) and every MI result are untouched.
It replaces a weaker claim about your own mechanism with a stronger one, and it defines exactly where the
escapes live (A2, A3, A4) — which is what makes the rest of this list a map rather than a guess.

## Concrete first calculation
1. Derive rho(omega) by residues for G_BD(tau) = -H^2/(4 pi^2 sinh^2(H tau/2 - i eps)). Show beta cancels.
2. Confirm numerically with mpmath quadrature at 5 frequencies, dps >= 30.
3. Scan >= 200 random positive-semidefinite density matrices (mixed, thermal, squeezed, displaced,
   deliberately inversion-shaped), keeping support off the truncation edge; report max |G_> - G_< - 1|.
4. State the scope sentence and name the two escapes it leaves open.

## Settles if / refuted if
SETTLED: beta cancels symbolically AND the density-matrix scan gives 1 to < 1e-10 in every state.
REFUTED: any normalizable state gives G_> - G_< != 1, which would be a much bigger result — check the
truncation edge first before believing it.

## Known walls — do not rediscover
The scope boundary is real: the identity rho = 2 pi sum (p_n - p_m) |phi_nm|^2 delta(...) IS negative in an
inverted state. The theorem is about the **unbounded boson ladder**, not about Hilbert-space positivity in
general. Do not over-close it — that is what A2 and A3 exploit.
