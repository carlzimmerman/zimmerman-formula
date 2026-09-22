# Verification and route outcome

Date: 2026-09-22. Repository HEAD during run:
`b73311096299e2f1816be00036ccdb2922bc44d4`. Existing unrelated dirty files
were present; no files outside this route were changed by this agent.

## Analytic status

`PROOF.md` contains four analytic lemmas, not inferred from the finite run:

1. Exact gauge-invariant ground-state-transform identity and its physical
   scaling target.
2. An actual one-plaquette SU(2) counterexample to global positive
   Bakry–Emery curvature at weak coupling.
3. Single-plaquette physical gap converges to 2 sqrt(b) as x->0, with a
   min–max/compactness proof.
4. Exact oscillator chains with uniform conditional Poincare gaps but a
   singlet gap tending to zero; the necessary approximate-tensorization
   constant diverges at least as 1/(2 omega_1).

The Gaussian chain is explicitly a surrogate counterexample to a general
inference, not a counterexample to Yang–Mills. The actual interacting
weak-coupling many-volume Poincare estimate remains unproved.

## Finite computation contract and interpretation

`verify.py` uses deterministic IEEE float64 arithmetic with NumPy 1.26.2,
SciPy 1.11.4, Python 3.9.6. It compares the first three eigenvalues of
the SU(2) character matrix at dimensions 200/400 with an independent
8192-point radial finite-difference operator, for b=2 and
x in {1, .25, .1, .04, .01, .002}. It checks the b=0 electric benchmark,
curvature trace bounds, and the weak-coupling limiting gap normalization.
For oscillator chains it checks lengths 1,2,4,8,16,32,64,128, x=.1,
adjoint dimension 3, the sine transform, matrix square root, conditional
gap floor, and the exact conditional-variance formula for the singlet
quadratic witness.

Result: **implementation and finite assertions verified in the stated
range, conditional on floating arithmetic and the standard eigensolver.**
The numerical Ritz gaps are not certified lower bounds for the infinite
character operator; no interval enclosure was attempted.

All 8 check groups passed. At x=.002 the gap divided by 2 sqrt(2) is
0.9995578979654488. At L=128 the chain's exact-formula singlet gap is
0.04870565920799013 while its minimum one-site conditional Poincare
eigenvalue is 25.465420333202555. The explicit quadratic witness requires
an approximate-tensorization constant at least 26.14601892275804 for
that length; the simpler proved lower bound is 20.531495030785884.

Run provenance is `run/manifest.json`; declared raw results are
`run/results.json`. The manifest records the input hashes before/after,
command, elapsed time, exit status, Git state, and resource caps. Limits
were wall time 40 s, CPU time 30 s, total log bytes 1 MiB, and cooperative
numerical-library thread cap 1. No process address-space cap was imposed.

The following command passed after the completed run:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.1/skills/computation-audit/scripts/validate_manifest.py real_research/reviews/yang_mills_continuum_2026_09_22/vacuum/run/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Reproduction: the manifest's `command` records the executed argv, and
`computation_contract.json` declares the scientific range. The bounded
runner requires a fresh output directory; `verify.py` currently writes
the declared `run/results.json`, so choose a fresh copied route directory
or adjust both output declarations together before a new recorded run.

## Conservative proofreading self-review

Scope: all newly written mathematical prose in this route. Routine edit:
corrected source author Irian D'Andrea after inspecting the primary
paper's title page. No mathematical-token proofreading changes. No
unresolved local notation or reference issue found. The unresolved
scientific implication is listed explicitly in `PROOF.md`.

## Independent review of root's blocking result

Read-only review of `../blocking/SCHUR_GAP.md` independently reconstructed
the completion-of-squares gap inequality with the G metric. The stated
operator-domain hypotheses suffice. One map wording correction was sent
to the root: ker K=G^(1/2)ker S, so its isometric embedding is
J G^(-1/2); J itself embeds ker S. A suggested domain clarification is to
define the unbounded K by its closed form k[z]=s[G^(-1/2)z], with domain
G^(1/2)dom(s). The main proof already projects onto ker S and is valid.

The independent two-level product obstruction was also checked: for a
bare projector |phi><phi| and exact product vacuum psi, the vector
Q psi=psi-alpha phi has squared norm 1-|alpha|^2 and shifted energy
|alpha|^2 L e_bare. This gives the proposed vanishing Rayleigh upper
bound for D=Q(H-E0)Q without implying that the full product gap vanishes.
