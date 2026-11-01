# Mathematical proofreading: changed hunks only

1 November 2026, author self-review after the proof audit and substantive
authorized corrections. Coverage: the TP01 additions in `RESULT.md`, the
current-summary correction hunks and the appended frozen-verdict erratum.

- Routine edits: removed a joining artifact in the evidence-scope paragraph;
  checked notation definitions, positive-domain restrictions, local Markdown
  table delimiters and relative links.
- Intentional mathematical changes under the proof audit: S/B identity,
  S excess bound, S slope/curvature/anchor, scalar S EFE and its b=0 boundary,
  exact certificate hypotheses, geometric a_geo=a₀/c² convention and the
  version-specific source locator. These were substantive authorized
  corrections, not mathematical typos silently repaired as proofreading.
- No mathematical-token changes were made by proofreading beyond those
  already justified in `RESULT.md`. Original Lean statements, numerical fit
  values, source data and sealed predictions were not rewritten.
- Unresolved scientific issues: full nonspherical EFE, physical kernel
  selection, high-field/covariant admissibility, microscopic normalization
  and complete dynamics remain outside these algebraic corrections.
- Validation: `run_002` completed; `adapter_004` compiles all five statements
  with standard axioms but records failure of its 1 GB RSS target. See the
  separately pinned manifest and verification record.
