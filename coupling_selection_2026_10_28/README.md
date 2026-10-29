# CS28: deriving the remaining couplings

Three selection routes have been tested in DERIVATION.md.
The original one-loop flow has no physical interior fixed ray, and its
radiative vacuum runs away from the Gaussian UV regime. Under the stated
operator hypotheses a unitary SCFT with both Yukawa interactions nonzero
is also excluded. A conditional SU(6) normalization fixes h/lambda but
leaves lambda^4 in B/V. No numerical ratio has been predicted.

The continuation in HIERARCHY.md derives the conditional relation

    B_curv/V_model = C(alpha)/L^2,
    C(alpha)=100alpha(16alpha+13)/[87(1+30alpha)],
    alpha=h_*^2/lambda_*^2, L=ln(mu_*/Lambda_5).

If the SU(6) normalization holds at the vacuum scale, alpha=1/30 and
C=7/27 exactly. This exchanges the remaining coupling for a hierarchy;
it does not select the hierarchy or establish the embedding's threshold
matching. The normalization is not invariant under the broken SU(5) flow.
Minimizing the existing tree energy over positive couplings also has no
finite stationary point; a physical modulus completion needs extra terms.

`run_verified/result.json`: 15 named checks pass, including nine finite
one-loop trajectories. The version-2 manifest validates with current input
and output hashes. The cutoff max(h^2,lambda^2,g^2)=4 is an arbitrary
diagnostic exit surface, not a physical perturbativity boundary.

`run_hierarchy/result.json`: 10 further named checks pass, including 12
direct numerical comparisons. Both successful manifests validate against
current inputs and outputs. SELF_REVIEW.md states proof and source scope;
HANDOFF.md records the remaining research target.

The first run (`run/`) failed because SymPy structural expression equality
was used instead of checking an expanded polynomial difference. A minimal
reproduction gave structural equality false and expanded difference zero.
The fix changes only the identity checker, not any equation or parameter.
That initial manifest pins the pre-fix script and is retained as historical
failed evidence; it is not current-input validation and supports no claim.

Reproduce the verified result with the documented contract:

```bash
python3 coupling_selection_2026_10_28/check_selection.py /tmp/cs28-result.json
```

For full bounded-run provenance use computation-audit's run_experiment.py,
the inputs listed in contract.json, a fresh output directory and a result
path inside that directory. All mathematical and external-source scopes
are explicit in DERIVATION.md and SOURCES.md.
