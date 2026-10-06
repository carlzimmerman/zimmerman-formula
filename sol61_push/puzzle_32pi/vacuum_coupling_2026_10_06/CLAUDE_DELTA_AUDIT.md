# Concurrent Claude checkpoint: conditional premise and auxiliary coupling

Inspected commits after the common entry checkpoint:

- `3fd60f9fb`: `fable_independent_2026/lean_2026/PUZZLE_32pi_premise_A_2026_10_05.lean` and its recorded output.
- `424268bec`: `sonnet55_push/puzzle_32pi/p53_bimond_general_alpha.py` and its recorded output.

This is a mathematical reading of the exact files, not a fresh independent Lean compilation or authenticated rerun of their scripts. The source files remain untouched.

## Premise A is the missing obligation

With c=1, positive a₀, r=1/(2a₀), and Λ=8πGρ, the premise Gρ(4πr²)=4π reduces by cancellation to Gρr²=1. Hence Λ=32πa₀². The converse also holds under these same ingredients: Λ=32πa₀² gives Gρ=4a₀² and then Gρr²=1. Thus the premise and the target are mathematically equivalent once the standard ingredients are fixed. Giving the premise a new coupling interpretation can suggest physics, but the conditional theorem alone does not independently select it.

Replacing G by kG in that premise yields Λ/a₀²=32π/k, as Claude's theorem shows. This correctly demonstrates sensitivity to a changed premise. It does not fix k=1. The current phase's conservation classification addresses one possible realization of that missing premise; its exclusions are restricted to algebraic all-conserved-jet sources, not all separately coupled sectors.

## General auxiliary coupling retains a boundary obligation

The displayed NR flux equations give

    m=(ν−1)/[ν+(ν−1)/α],
    x_*=y[ν+(ν−1)/α].

Direct differentiation yields

    m d(x_*²)−(ν−1)d(y²)
       =d{[(1+α)/α] y²(ν−1)²}.

Here I_ν=∫(ν−1)d(y²)=2∫y(ν−1)dy, twice the C moment used in the earlier kernel-tail investigation. Thus the finite moment identity J=I_ν is conditional on this boundary term vanishing at both endpoints and on the change of variables/integration branch being legitimate. The script checks the derivative identity; its prose statement that the boundary vanishes is not separately checked there for arbitrary kernels. For a regular MOND deep endpoint, y²(ν−1)²→0. At the strong endpoint it is a further tail condition. Our earlier nonnegative elliptic finite-moment tail theorem supplies one sufficient condition: f=y(ν−1), D=1+2f′>0, and finite ∫f imply f→0, because the remaining tail exceeds f(Y)². That argument is additional to the symbolic identity; D>0 is this earlier restricted ellipticity hypothesis, not an automatically established condition for every general-α BIMOND branch.

Coincident-vacuum consistency with nonzero vacuum primitive M(0) gives q=1/(1+α) for nonsingular α, so Λ/a₀²=I_ν/(1+α) after the boundary condition and vacuum normalization are imposed. α=0 is singular in the NR map; α=−1 is singular in this vacuum relation, even though its NR map formally reduces to the main-class expression. These special branches must not be treated as regular members of the same nonzero coincident-vacuum formula. If M(0)=0, the coincident vacuum is Ricci-flat and the metric consistency no longer fixes q or the prefactor derivative; α=−1 can retain that trivial branch. No healthy sign or full perturbation classification is supplied by these three algebraic checks.

Accordingly the new result enlarges the identifiability problem: a measured coefficient constrains I_ν/(1+α), not α and the kernel moment separately. This agrees with the current phase's source-normalization requirement and adds no independent selector. The strongest next test is the common-source action and its observable second prediction, not another substitution of the target into either free quantity.

A concrete branch warning follows for the printed RAR fit α≈−0.742. If −1<α<0 and a continuous MOND ν spans ν→∞ at the deep endpoint and ν→1 at the strong endpoint, the denominator ν+(ν−1)/α must cross zero at ν=1/(1+α)>1. At that finite positive y, x_*=0 while m diverges with nonzero numerator. A regular C¹ interaction M(z) cannot realize this map. Thus lowering the kernel moment below 32π and solving algebraically for such an α does not provide a regular branch; a singular/cusp or other explicitly changed completion would need its own analysis. This is a source-map obstruction, separate from any kinetic-sign assessment.
