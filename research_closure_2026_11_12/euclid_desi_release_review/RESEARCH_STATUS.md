# Research contract and live routes

Checkpoint ancestry: document-only publication branch codex/euclid-desi-review-2026-11-12, first checkpoint 09b8dd7c6aad534bde13ade93b764607aae45b58. Source checkout initially 2ffc012fa56dcdcbb4b3d5f169ba757fe482bcb8 with unrelated existing changes. Inputs are pinned by per-route hashes; a newer message does not supersede incompatible evidence.

User objective: use the Euclid/DESI clues to find a substantive new route or result for the Zimmerman relation, while retaining all existing predictions and failures, and push the work for collaboration.

Success standard: an independently checked mathematical consequence or observational discriminator with explicit assumptions, identifiable parameters and a feasible measurement path. A theory breakthrough additionally requires one specified healthy model to meet all relevant gates. Neither a candidate observable nor a numerical identity is an empirical confirmation or a healthy completion.

## Portfolio

| Route | Central move | First uncertain implication | Discriminating check | Current state |
|---|---|---|---|---|
| R1 lensing–dynamics | Cancel mass normalization using deflection and global dispersion | Does cancellation survive finite aperture, transition regime and source/tracer differences? | Derive virial relation; change tracer mass profile as counterexample | Conditional deep-limit relation; generic universal claim fails |
| R2 redshift/dynamics | Infer D_A a₀ from resolved radial shape rather than stellar normalization | Is the transition observable identifiable with unknown radial baryons/inclination? | Rank calculation and exact radial-M/L counterexample | Conditional cancellation derived; nuisance/identifiability audit in progress |
| R3 slitless spectroscopy | Use opposite dispersions to separate spatial and spectral displacement | Can same-line features and matched weighting be recovered from released exposures? | Double-difference identity; zero-velocity line-blend counterexample | Algebraic route; exposure and line-deblending gates unresolved |
| R4 double-source-plane lenses | Use external geometry to convert two source scales into a deflection-shape constraint | Do multiple planes/line-of-sight sheets remove the purported cancellation? | Power-law identity and sheet/multiplane counterexample | Known-method connection; no unique a₀ normalization |
| R5 joint dimensionless closure | Combine D_A a₀ and BAO ratios in the Friedmann equation | Is κ identifiable without a ruler/early-density prior, and is FRW closure justified? | Independent algebra, rank and nuisance audit | Candidate under independent review |

The first three route owners are separate agents. Root owns R4 and R5 synthesis. Route files are disjoint; only the coordinator edits this live index. Numerical toy examples use synthetic inputs, not the released galaxy residuals. No candidate is selected by agreement with the theory.

## Current strongest candidate, pending audit

Let T(z)=D_A(z)a₀(z) be inferred from resolved dynamical shape under a specified kernel and baryonic geometry, d_M=D_M/r_d and d_H=D_H/r_d be BAO observables. Define

\[
q=\frac{(1+z)T}{c^2d_M}=\frac{a_0r_d}{c^2},\qquad h=\frac1{d_H}=\frac{Hr_d}{c}.
\]

With the standard Friedmann equation, conserved matter and radiation, specified curvature and a₀²=κ²c²Gρ_DE,

\[
h^2=A(1+z)^3+B(1+z)^4+K(1+z)^2+\frac{8\pi}{3\kappa^2}q^2.
\]

The hypothesized κ=1/2 corresponds to coefficient 32π/3. The absolute sound horizon and Hubble constant do not appear. This uses an independent dynamical observable; constructing T from the same assumed cosmology/formula would make the test circular. It is conditional on Friedmann closure and the dynamical extraction, not a derivation of that closure from the bare scale relation.

Rank, radial stellar-population gradients, gas, inclination, correlated BAO errors and selection can still block this measurement. The research task is to establish exactly what survives these tests, not to declare all nuisances cancelled.

## Preservation

Historical SP1/SP2 seals and contradictory criterion directions are unchanged. No old result is regraded here. The 39-object lens metadata pool remains distinct from the rotation-curve population needed by R2/R5. Publication of the literature audit does not imply those observational experiments were run.
