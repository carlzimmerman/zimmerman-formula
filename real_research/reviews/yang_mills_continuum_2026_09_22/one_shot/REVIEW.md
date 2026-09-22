# YM-C2 self-review and verification

Scope: `PROOF.md`, the new finite-block theorem, its explicit constant and
the proposed use in the existing Schur bridge. This is a self-review, not
independent review. The preceding YM-C1 evidence was checked for unchanged
content; its computations were not rerun.

**Primary verdict for Yang–Mills closure: incomplete, with the smallest missing
implication being a volume-uniform whole-layer discarded-sector estimate for
successive exact coarse Hamiltonians.** Terminal coercivity and the actual
continuum quantum-field construction also remain open.

The finite-block theorem (1)–(2) is proved as written in the finite compact
setting. Its dependency chain is:

    finite-volume positive ground state
      -> Feynman–Kac comparison with only touching plaquettes removed
      -> conditional density oscillation
      -> conditional Haar Poincare comparison
      -> form-compressed discarded-sector lower bound.

The explicit exp(-C_B/x) version additionally uses the compact Li–Yau heat
estimate, derived in the proof and checked against its original source.

| Obligation | Result | Check |
|---|---|---|
| True vacuum and energy shift | Passed | The semigroup uses the actual psi and E0; E0 cancels only in a same-time ratio |
| Exterior-volume independence | Passed for fixed B,p_B | V_out is retained inside the same positive exterior expectation for both initial block configurations |
| Independence needed for factorization | Passed | Free link Brownian motions are independent; V_hit is removed before factorization |
| Conditional density | Passed | The normalized psi-squared density has oscillation R_B^2, not R_B |
| Time/coupling normalization | Passed | s=xt/2; 2t W_B=8s b p_B/x^2 |
| Form domain and orthogonal projection | Passed in finite volume | Conditional expectation is smoothness preserving and H1 bounded for fixed smooth positive psi; closure gives the restricted form |
| Gauge invariance | Passed | The conditional integral intertwines the separate link-coordinate gauge actions |
| Haar spectral normalization | Passed | Positive product Casimir eigenvalues are at least C_F in the conventions of YM-C1 |
| Heat bound | Passed | Nonnegative Ricci, no boundary, normalized kernel mass one, correct earlier/later time integrations |
| Exponent optimization | Passed | Exact differentiation gives s_* and minimum 4D_N sqrt(3m b p_B)/x |
| Decoupled case b p_B=0 | Passed | Free-link ground factor is constant; no division by zero in optimization is used |
| All-block or all-N uniformity | Not claimed | The displayed constants explicitly depend on m,N,p_B |
| Repeat on exact coarse operators | Not established | No Wilson-form stability theorem is supplied |
| Original Yang–Mills target | Incomplete | Whole-layer bounds, terminal form/metric and continuum field construction are missing |

Counterchecks against known failed routes: P1=1 prevents the bare-vacuum
overlap defect. The effective Schur metric has not been discarded. The bound
does not infer global mixing from single-block estimates. Divergence of the
certificate in equation (8) is not represented as divergence of the actual
inverse-gap sum or as a mass-gap counterexample.

Fresh verification on 2026-09-22:

- All 36 SHA-256 entries in the original `../CHECKPOINT.json` match.
- The original I15 proof still has SHA-256
  `223d5d0f7ba6bd6fc7cfeffc8cfa18ac32c906e7172af2f4acd2708b5e149b72`.
- The computation-audit `validate_manifest.py` command, with `--root .`,
  accepts each of `../blocking/run_exact/manifest.json`,
  `../rg/run/manifest.json`, and `../vacuum/run/manifest.json`.
- A Python 3 / SymPy exact symbolic check of the derivative and minimum of
  `3*m*D**2/(2*s)+8*s*b*p/x**2` with positive symbols passes, including strict
  convexity in s. This checks the displayed algebra only; the proof is analytic.
- The earlier failed `../blocking/run/` is preserved as a historical failure,
  as documented in YM-C1; it is not one of the successful manifests.

Proofreading covered all newly added prose and equations. No unresolved
notation or local algebra correction remained. No claims of operator-proof
mechanization, empirical Yang–Mills verification, or completed continuum
construction are made.
