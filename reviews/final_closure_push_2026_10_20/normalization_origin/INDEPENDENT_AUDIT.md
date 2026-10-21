# Independent audit of the compression-normalization obstruction

**Normalized claim.** At x=10, for a fixed supported spherical core, fixed conditioning radius R, fixed temperature, fixed source length L at least the reference rms cloud radius, and a smooth spherical scalar mass density equal to the conditioned Maxwell-Boltzmann profile, imposing C=4πGχ/V=1 forces order-one or larger scalar self-gravity. The independent-particle tracer distribution therefore cannot also approximate a weakly self-gravitating macroscopic cloud under these conventions.

**Primary verdict: proved as written** for the revised, explicitly macroscopic-continuum claim in DERIVATION.md, SHA-256 `d26b0d4d4c34f79cae582b31b4dfd1a64f0a48420a48df06118cadb569f73962`. Equations (1)–(4), their units, and their quoted x=10 numbers are correct under that file's smooth spherical-density/continuum interpretation. Its added finite-N correction is also correct as an independent-product expectation, not a per-configuration theorem. The first draft lacked this restriction and admitted an N=1 counterexample; the author incorporated the restriction and self-pair distinction during this review. The earlier draft's scope gap was not a factor error in its continuum-density formulas.

The scoped result does **not** establish an obstruction for every source-length convention, host, thermal protocol, interacting phase, or acceleration-dipole construction. Most of the author's wording already observes those limits. “Unit gravitational susceptibility” should be read as unit **curvature-compression** coefficient under the declared normalization, because the missing operator bridge is not supplied here.

## Independent reconstruction

The audited source Hamiltonian is

\[
H_E=\sum_{i=1}^N\left[\frac{p_i^2}{2m}
+\frac{m}{2}(\kappa+E/L)r_i^2\right],\quad
Q=\frac{m}{2L}\sum_i r_i^2,
\quad |\mathbf r_i|<R.
\]

Here T,m,N,R,L and the reference κ are held fixed in the E derivative. The domain must stay fixed; choosing L as a reference rms radius does not license L(E). Momentum integrals and 1/N! cancel from the response. With x=mκR²/(2T), the one-particle radial law is proportional to r² exp(−xr²/R²). The change of variable t=xr²/R² gives

\[
f_t(t)=\frac{t^{1/2}e^{-t}}{\gamma(3/2,x)},\quad
\langle r^2\rangle=\frac{R^2\mu}{x},\quad
\operatorname{Var}(r^2)=\frac{R^4v}{x^2}.
\]

The ordinary canonical derivative, with this fixed bounded domain, is

\[
-\partial_E\langle Q\rangle=\frac{\operatorname{Var}(Q)}T
=\frac{Nm^2R^4v}{4L^2Tx^2}.
\]

Using Nm/V=qρ_b, 4πGρ_b=3κ and T/m=κR²/(2x) independently yields

\[
C=\frac{3qv}{2x}\frac{R^2}{L^2},\qquad
q(C=1)=\frac{2x}{3v}\frac{L^2}{R^2}.
\]

These reproduce equations (1) and (2), including the factor 3/2.

For a normalized smooth spherical density ρ_d(r)=ρ_0 exp(−xr²/R²),

\[
M_d=4\pi\rho_0\int_0^R r^2e^{-xr^2/R^2}dr
=\frac{2\pi\rho_0R^3}{x^{3/2}}\gamma(3/2,x).
\]

Therefore

\[
\frac{\rho_0}{\rho_b}
=\frac{2q x^{3/2}}{3\gamma(3/2,x)}
=\frac{4q x^{3/2}}{3\sqrt\pi P},
\]

which is equation (3). For an actual smooth spherical density, g_d(r)=4πGρ_0 r/3+O(r³), while g_b(r)=κr; their central curvature ratio is indeed ρ_0/ρ_b. This uses a mass density in Poisson's equation, not just a position probability density without a continuum approximation.

Finally the Newtonian binding energy of a smooth spherical density is W=−G∫₀ᴹ M/r(M) dM. Since r(M)≤R,

\[
|W|\geq\frac{GM_d^2}{2R},\qquad
U_{\rm trap}=\frac\kappa2M_d\langle r^2\rangle.
\]

The baryonic core mass obeys κ=GM_b/R³ and q=M_d/M_b, so

\[
\frac{|W|}{U_{\rm trap}}
\geq\frac{qR^2}{\langle r^2\rangle}=\frac{qx}{\mu}.
\]

This is equation (4), without a missing 1/2 or double-counting of the continuum potential energy. The positive trap term is the curvature-dependent part of the host energy; a constant potential offset is irrelevant to the response.

## Units, source convention, and numerical checks

In physical units, [κ]=time⁻², [T]=mass·length²/time², [E]=length/time², [Q]=mass·length, and [χ]=mass·time². Thus 4πGχ/V is dimensionless. The variable E is an acceleration-dimension coordinate for an isotropic curvature increment δκ=E/L. It is not a uniform-acceleration source. The proof correctly uses a scalar second moment, rather than a center-of-mass dipole.

For L equal to the fixed reference rms radius, L²/R²=μ/x. Hence q=2μ/(3v), the lowest required mass ratio in the explicitly stated L≥rms class. Increasing L raises q and the central density quadratically. No physical theorem in the packet establishes that every possible operator bridge must choose L≥rms; outside this class the conclusion is not proved. In particular, L≪rms can reduce the normalization inventory. The author discloses this escape and does not claim it solves the missing source map.

A separate standard-library Simpson integration, performed during this audit on y=r/R in [0,1] with 8000 intervals and weight y²exp(−xy²), gives

| quantity at x=10 | independent value |
|---|---:|
| μ | 1.4983797427823766 |
| v | 1.4846049311991067 |
| P | 0.9998302575644504 |
| q for L=R | 4.4905324821210435 |
| q for L=reference rms | 0.6728522905516436 |
| central ratio, L=R | 106.84036595352552 |
| central ratio, L=reference rms | 16.008744005621857 |
| energy ratio lower bound, L=R | 29.96925514878136 |
| energy ratio lower bound, L=reference rms | 4.4905324821210435 |

The integral checks are spot checks of the displayed constants, not the proof of the exact implication. The asymptotic coefficients quoted by the author also follow: μ,v→3/2, q_rms→2/3, central ratio ∼8x^(3/2)/(9√π); for L=R the central ratio ∼16x^(5/2)/(27√π).

## The finite-particle qualification

For literal point particles the interaction Hamiltonian contains

\[
W_{\rm pair}=-Gm^2\sum_{i<j}|\mathbf r_i-\mathbf r_j|^{-1},
\]

not the diagonal i=j terms. If f is the one-particle probability density and ρ_smooth=Nm f, independence gives

\[
\mathbb E W_{\rm pair}=(1-1/N)W[\rho_{\rm smooth}].
\]

Likewise, conditional on one tagged particle's location, the mean density of *other* particles is (N−1)m f, so its mean self-gravitating curvature has the same (1−1/N) factor. N=1 has W_pair=0 identically and no self-force, although equations (1)–(3) still assign a large coefficient to its ensemble-averaged density. A fixed supported host and conditioned thermal particle remain a valid mathematical counterexample to an unqualified arbitrary-N incompatibility claim.

This does not rescue the intended macroscopic cloud. The factors approach one as N grows. Even at N=2 the corresponding *expected* energy-ratio lower bound in the L≥rms class is at least 4.49053/2=2.24527, while the tagged-particle mean central ratio is at least 16.00874/2=8.00437. The revised author file now identifies the continuum/spherical mean-field reading explicitly and includes these finite-particle distinctions in its equation (4a) and accompanying text. No statement that an individual finite-N microstate is spherically symmetric follows from an isotropic ensemble.

## Obligation matrix and scope of the stationary controls

| obligation | result |
|---|---|
| fixed-domain canonical derivative and independent-particle variance | passed |
| truncated radial moments and equations (1)–(2) | passed |
| density normalization in equation (3) | passed |
| central Poisson curvature for a smooth spherical density | passed |
| equation (4) for a smooth spherical density | passed |
| distinguish smooth continuum gravity from exact discrete self-gravity | passed in the revised claim; absent in the first draft |
| L fixed during E derivative; L≥reference rms in the claimed obstruction | passed as an explicit hypothesis |
| establish a physical uniform-acceleration/dipole operator bridge | not addressed; explicitly outside the claimed result |
| select abundance, thermal receiver, EOS, host, or κ=1/2 | not addressed |
| globally exclude all interacting stationary states | out of scope and not established |

The exact continuum obstruction needs none of the new stationary controls. I inspected equations (5)–(6) and the source for consistency, but did **not** independently reproduce the stationary shooting run or certify its branches. The dimensionless factors agree: with r₀=c_s/√κ₀, 4πGρ_b r₀²/c_s²=3 produces w′=3δr²eʰ, and fixed-mass differentiation gives the displayed −3q/(2R²) width derivative for L=R. The code's finite shooting and refinement checks do not establish uniqueness, stability, a physical EOS, thermalization, or formation selection; the author correctly disclaims all of those.

One small comparison caveat: the *conditioned* x=10 ideal tracer's exact compression fraction at s=2 is 0.4994593996605737, not exactly 0.5. The number 0.5 is the unconditioned rational formula, which the text calls the “tracer rational formula.” The distinction should be retained when discussing an exact finite-core baseline. It cannot explain the stationary controls' much smaller responses and does not affect equations (1)–(4).

The revised phrase “The scoped macroscopic target is resolved” is safe for the explicitly restricted tracer construction. It would be too strong if read as a global no-go for normalization or interacting cold states. The author's following statement, “The theory's normalization target remains open,” correctly limits that inference. The three sampled stationary branches cannot extend the exact tracer result to every interacting branch or contact strength.

## Dependency graph, remaining gap, and provenance

Dependency graph: conditioned fixed-domain independent-particle Hamiltonian → canonical variance identity → elementary truncated-Gamma moments → equations (1)–(2); smooth spherical density identification → mass normalization and Poisson central limit → equation (3); smooth nonnegative spherical gravity → shell-energy formula → equation (4). The first arrow is an exact statistical identity; the smooth-density identification is the extra modeling leaf. No external theorem verification is load-bearing here.

**Strongest safe statement:** with the declared continuum spherical density, fixed core volume, x=10, and L≥reference rms, unit curvature-compression normalization forces large self-gravity, so its response cannot consistently remain the independent-tracer response. The numerical stationary controls illustrate some alternatives; they do not close the global problem. The exact remaining physical obligations are the choice of a supported live host and EOS, an actual thermal protocol and population selection, and an operator map to the acceleration-conjugate source. No additional physical experiment was required for this audit.

This was an independent reconstruction by a subagent that did not author DERIVATION.md or check_backreaction.py. It is not independent experimental or model evidence. No author file, output, criterion, or packet inventory was altered. The authorized write is this audit only.

Requested base: `f659e6d8e1ee4cf2b756f091aff56b018da1fb1e`. Initial read/check time: 2026-10-20 15:25:56 UTC. Observed shared-workspace HEAD: `5c9edd07b9bc1b9610f8080de8b7700d3ccdb7bb`. The initial DERIVATION.md had SHA-256 `66bde09a8bcc4d418797390008941ecb39aa7decd8a9a859fab4b41f7ad7ee03`; after reporting the finite-N scope gap, the independently re-read author revision has the current hash below. No code or numerical-result change was needed. Exact audited SHA-256 values:

| artifact | SHA-256 |
|---|---|
| DERIVATION.md, revised continuum claim | `d26b0d4d4c34f79cae582b31b4dfd1a64f0a48420a48df06118cadb569f73962` |
| CONTRACT.md | `6352ab3046591d6dab5c6ff0c4c77833ac8a67fe99d32d258f3a640fd2f11354` |
| check_backreaction.py | `1843fb2bbddb57f984505e38620bf35f68a823a61bea8064aedb8edc419c89d7` |
| canonical_response/CANONICAL_RESPONSE.md | `e97cb72d71a31a31226414184ff8bf1f5a5280596a7d01f8028ed3690727c622` |
| run_004/manifest.json | `9675a78cb080252b5dec8bf5f20bc80ebf58d3e760b106a2fce1d8516e6ba22d` |
| run_004/results.json | `8f46a157fc53dd67c1dfed17b627fbcd1fc9d2fe532c80daab729552bcf3eae4` |

These match the author's provenance inventory for the corresponding versions. `run_004` records completed/41 checks passed; that is a read-only status observation, not a fresh reproduction or endorsement of every finite-control inference. The independent moment spot check used Python 3.9.6, no imported scientific package, and no files or new physical run.

Mathematical proofreading covered this audit only: display delimiters, fixed-reference notation, signs, factors and scope wording checked; no author source was edited. The only changes during that pass reconcile the audit with the author's explicitly restricted revision. No unresolved mathematical-token typo remains in this audit.

## Editorial recheck of the current author version

The author subsequently clarified the non-load-bearing s=2 comparison, exactly as requested above. Current DERIVATION.md SHA-256 is `49fb137a581d4933692640fbdc726f7105cb21cebb1cb536efc5bcc0a3da1cca`; the previously audited `d26b0d4d4c34f79cae582b31b4dfd1a64f0a48420a48df06118cadb569f73962` remains the substantive-proof history. PROVENANCE.json's second documentation-correction record identifies those same before/after hashes.

I read the changed paragraph and verified the exact textual delta: it now calls 0.5 the **unconditioned** rational comparator and explicitly gives the conditioned x=10 finite-wall value approximately 0.4994594. Reversing only that paragraph replacement in memory restores the previously audited SHA-256 `d26b0d4d4c34f79cae582b31b4dfd1a64f0a48420a48df06118cadb569f73962`, so no other author-text change is hidden in the current file. There was no file modification, scientific rerun or new numerical calculation for this check. The **proved as written** verdict for the explicitly restricted macroscopic-continuum obstruction therefore also applies to current hash `49fb137a581d4933692640fbdc726f7105cb21cebb1cb536efc5bcc0a3da1cca`; all physical scope limitations remain unchanged.
