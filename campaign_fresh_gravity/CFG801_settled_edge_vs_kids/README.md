# CFG801: ARGON02 kill test (b) on public KiDS lensing. The settled-halo edge is EXCLUDED

**Question.** ARGON02 predicts that each galaxy's settled cold halo stops at the supply edge r_e = 5.84 r_M (44–90 kpc here),
so the lensing signal should break there. Brouwer et al. 2021 (KiDS-1000) measured lensing around isolated galaxies, in
4 stellar-mass bins, with full covariance.

| footing | range | Δχ² (edge − no edge), M_b profiled | zero-knob M* | class |
|---|---|---|---|---|
| canonical | R ≤ 0.31 Mpc (primary) | **+197** | +303 | **EDGE EXCLUDED** |
| canonical | all radii | +753 | +867 | EXCLUDED |
| alt | R ≤ 0.31 Mpc | +234 | +341 | EXCLUDED |
| alt | all radii | +813 | +938 | EXCLUDED |

- The lensing keeps going well past 44–90 kpc, as in Mistele et al. (2024). The settled-only halo, ending at the
  supply edge, **cannot be the whole lensing mass**. ARGON02's own kill test (b) fires on public data.
- **Consequences.**
  - The outer mass must come from somewhere else: S4 "free debris", or a supply rule without a sharp edge.
  - Neither is specified in the record, so this is an open problem for the S3/S4 cold-energy bookkeeping.
  - The galaxy law itself is NOT what fails here: the no-edge continuation is the law's own profile.
- **Disclosed.**
  - The no-edge model also fits poorly in absolute terms (χ² 84 on 28 dof).
  - Its profiled masses sit 0.1–0.2 dex above the provisional M* means.
  - Two-halo contamination in the outer bins biases against the edge, but the primary range is the inner 0.31 Mpc.
  - Implementation fix after the freeze: non-finite χ² at extreme grid masses now returns ∞. Numbers are unchanged.

Controls: K1 (r_e = 5.843 r_M), K2 (ARGON02 deep amplitude 0.969) and K3 pass. MUTATE (data := edge model + noise)
gives EDGE FAVOURED, so the test bites.

κ fitted; not theory closed. Bin M* means are provisional.
