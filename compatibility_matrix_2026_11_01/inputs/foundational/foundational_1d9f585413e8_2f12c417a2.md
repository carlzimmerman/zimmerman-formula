# Density and collar closure: live state

Checkpoint **X48-DEN-2026-11-01-A**, from [TARGET.md](TARGET.md).
**Original goal remains open.** No actual common interval for central-quarter
`C>=4` has been proved, and the all-time entropy-floor theorem remains
conditional on uniform seeding.

New proved conditional result: under the actual tight prefix envelope
`|x-x_d|<=1/32` through `ceil(N/2)` and its specified cutoff halos,
the complete nonlinear first energy satisfies

\[
 Y'\le\{1/(16s)+C(s^{-1/2}+1)\}Y
              +C_Ls^2E_{v,\mathrm{outer}}+C_Ls^4
\]

with positive mechanical and heat dissipation retained on the left and
all constants independent of N. A density-only midpoint gradient potential
cancels the principal mechanical cross term. Relative entropy and a
one-sided K-gradient energy close its memory-gradient cost, including
closed heat faces. Every local and collar term is accounted for.

The fixed-N activation trace launches this uniform inequality with singular
exponent `1/16`. Nested cutoffs yield `Y_inner<=Cs^5` and
`sum V phi_inner (x-x_d)^2<=Cs^6`, conditionally on the same actual prefix
envelope. The cutoffs cover all `i<=ceil(N/4)`, including the first cell.
Independent reconstruction passed these conditional implications; see
[INDEPENDENT_AUDIT.md](INDEPENDENT_AUDIT.md).

The original theorem still needs two implications:

1. Actual nonlinear pointwise control from the compatible cold evolution,
   uniform in N and valid at the origin. A small weighted L2 energy alone
   does not imply a maximum bound.
2. Propagation of the prefix/collar hypotheses on one common interval.
   An estimate on a smaller inner cutoff does not close a bootstrap at the
   outer edge of the assumed prefix.

The bounded actual pointwise continuation proves a sufficient constitutive
reduction: a uniform bound `||(S-S_d)/s^2||_infinity<=Cs^theta`, theta>0,
would imply `||x-x_d||_infinity<=C(s^theta+s^3)` on the covered prefix.
The exact all-p stress identity retains its heat-dependent weight and mixed
heat flux. Their level-dependent coefficient remainder is the first
unclosed implication in this attempt. See
[pointwise_continuation.md](pointwise_continuation.md) and
[HANDOFF.md](HANDOFF.md). A static one-cell example shows only that the
energy estimate alone cannot imply a maximum bound; it is not an IVP
counterexample.

The alternative boundary route now has a uniform bound on the spatially
summed actual volume variation and a fixed good cut, from energy plus a
one-sided prefix cap. Its separated moving-graph Poisson-kernel estimate
is still open. That alternative is not required as an extra premise of the
new localized energy theorem.

Full derivation and route map: [README.md](README.md). Sources and checks:
[PROVENANCE.md](PROVENANCE.md). Earlier partial results and failed local
metric methods remain in their original notes. The new gradient-dependent
energy is outside the restricted class of those method obstructions.

No constitutive law, material scale, cold datum, test source, or previous
finite-run artifact changed. Energy conservation and exact quiet-gate
inactivity retain their previous proofs; no new simulation was run.
The original research route stays open and is not marked exhausted.
