# Nonlinear transport gate → stationary clock construction

Base: `5b5b7af83c3dfd8c42f328a2fcfcc4fefd1ccf1c`. Full gravity remains **OPEN**. Previous goal turn: progress (published action calculation and conditional Lean proofs).

This checkpoint changes the action on mathematical evidence, not by relabeling the previous quadratic certificate. Carl Zimmerman supplied the primordial-clock direction and the global a₀ requirement. No particle-CDM species is added, but the clock/χ fields supply an effective dark dust stress. No claim of literature priority or empirical discovery is made.

## 1. Why the previous action needed a nonlinear repair

For the previous covariant density K(Q,τ)−C(Q,τ)Y+U(τ)√Xτ−V(τ), choose the timelike clock gauge τ=t. Write F=K−CY, pχ=√h F_Q and E=(pχ/√h)Q−F. Direct Legendre differentiation gives E_p=Q and E_Y=−F_Y. The functional Hamiltonian bracket, modulo the total spatial momentum constraint, contains

\[
j^i=\sqrt h\,[-2QF_Y-F_Q]D^i\chi
=\sqrt h\,[2QC-K_Q+C_QY]D^i\chi.
\]

Preserving the Hamiltonian constraint therefore contains the first-order lapse operator 2jⁱ∂ᵢN+N∂ᵢjⁱ. Its real sine/cosine principal matrix has computed rank two when j·k≠0 and rank zero when j·k=0. The latter includes transverse directions; a zero principal symbol is not a full operator/kernel count. On exactly homogeneous χ, j vanishes identically. The FLRW constraint count cannot simply be transferred to an inhomogeneous field.

For the old r=0 coefficient C=K_Q²/[2(QK_Q+U)], the leading defect is −AU/(qA+U)≠0 for A,U,q>0. Independently expanding the same action at a local inertial event with τ=t, χ=Qt+gx gives a cubic characteristic polynomial. Its cubic coefficient is 2g(B−C_QQ g²)(2QC−A+C_Qg²). Two independent derivative expansions agree. After rescaling w=gv,

\[
\lim_{g\to0}g^2\det\mathcal P(w/g,g)
=-\frac{BUw^2(2Aw+U)}{AQ+U},\qquad
w_{\rm fast}=-\frac{U}{2A}.
\]

The nonzero limiting root is simple. The resulting fast characteristic scales as v≈−U/(2Ag). This is a singular inhomogeneous limit, not a new ordinary sound-speed parameter.

At the exact previously used profile event Q=10/11, A=1/10, B=726/725, U=1/110 and g/Q=1/100, the characteristic polynomial, after clearing nonzero factors, is

\[
1618128500398262v^3+9256916134592200v^2+5857568581738v-131701478915325.
\]

Its values at −6 and −5 have opposite signs. `Characteristic.lean` proves that an actual real root lies below −1 using continuity and the intermediate value theorem. The source bridge compares the *actual Lean definition* against the coefficients computed from the action; no speed or rank is hard-coded into a certification result. The numerical root is approximately −5.71763. This refutes an unrestricted metric-cone claim for that local principal symbol. A full global solution, boundary-value interpretation and nonlinear DOF classification are separate obligations; a characteristic determinant alone is not a complete physical initial-data count.

## 2. Exact bracket repair, not another parameter scan

Instead use the single covariant sector

\[
\boxed{S=\int d^4x\sqrt{-g}\left[\frac{M^2}{2}(R-2\Lambda)
+P(X,\tau)+\sqrt{X_\tau}\,W(Y,\tau)-V(\tau)\right]+S_m[g,\psi],}
\]

where X=−∇χ·∇χ, Xτ=−∇τ·∇τ>0, nμ=−∇μτ/√Xτ, Q=n·∇χ and Y=(g^{μν}+n^μn^ν)∇μχ∇νχ, so X=Q²−Y. Ordinary matter is a separately minimally coupled sector, not part of the tests below.

In unitary gauge the W term is independent of lapse. The lapse constraint contains the Lorentz-invariant P(X,τ) Hamiltonian; its self-bracket closes on the ordinary spatial momentum constraint **for arbitrary Q and Y**, not just the background value q. The lapse-independent Hamiltonian is H₀=−∫√h W. This repairs the specific transport defect identically.

The first reconstruction, P=aX+bX²/4+k₀ and W=U+dY−bY²/4, matches the old background and quadratic action exactly. `repair.py` derives the matching coefficients and removes the cubic characteristic. It also finds genuine gradient failures: only 48/111 and 54/111 sampled longitudinal events pass for the two tested clock profiles. These results are recomputed at 70 digits, not dismissed as numerical noise. This polynomial version is not the surviving candidate.

## 3. A necessary coefficient from nonlinear stability

At Y=0 the local scalar restoring numerator for the new architecture is

\[
\mathscr R(X)=P_X(U-2dX)-dU,\qquad d=W_Y(0),
\]

with a positive kinetic denominator on the regular branch. Exact pressurelessness requires ℛ(q²)=0. Nonnegative restoring response on *both sides* of that interior point requires ℛ′(q²)=0, rather than a simple sign-changing zero. Using A=2qP_X and B=2P_X+4q²P_XX gives the necessary relation

\[
\boxed{B=\frac A q+\frac{2A^2}{U}=\frac A q\left(1+\frac2m\right),\qquad U=mqA.}
\]

This is a within-architecture necessary condition, not a universal gravity coefficient. `stationary.py` derives it, and `Stationarity.lean` proves its algebraic implication. In particular, the old prescribed m=m₀a² profile cannot simply retain its old B after this gate.

## 4. Explicit surviving logarithmic/square-root construction

Let m>0, q=Q_c/(1+m), A=I/a³, U=V=mqA, and retain the dust+Λ background H²=Λ/3+Q_cI/(3M²a³). Define

\[
d=\frac{AU}{2q(qA+U)},\qquad \ell=\frac{q^2m}{2},
\]

\[
\boxed{P(X,\tau)=-\frac U2\log\frac{U-2dX}{U-2dq^2},\qquad
W(Y,\tau)=U+2d\ell\left(\sqrt{1+Y/\ell}-1\right).}
\]

All coefficients are functions of τ through the reconstructed background. Required domain: Xτ>0 and U−2dX>0; Y≥0 for the timelike clock foliation. This is a specified action, not a stress tensor assigned afterward. It has P(q²)=0, K_Q=A, K_QQ=B as required, and effective spatial coefficient C=P_X−W_Y=A²/[2(qA+U)] at the background. Thus the *entire FLRW quadratic action* has the same coefficient form used in the finite-pressure inverse derivation, now with a different clock history. Higher interactions have changed and require their own tests.

The logarithmic choice makes ℛ(X)=0 exactly for all regular homogeneous X, not merely to first order about q². The square-root W supplies independent nonlinear spatial response. These functions are reconstructed to satisfy the stated gates; neither microphysics nor the MOND interpolation law nor κ=1/2 has been derived from them.

The finite-k pressure-cancellation inverse equation and the new B condition jointly determine the history. For Ω=1/(1+RΛa³), RΛ=ΛM²/(Q_cI), N=ln a and v=−Be/(3A),

\[
\frac{m'}m=\frac32\Omega+\frac{3v(m+1)}{m+2},
\]

\[
v'=(v-1)\left[\frac{3\Omega(3m^2+8m+6)}{2(m+1)(m+2)}
+\frac{3v(m^2+2m+2)}{(m+2)^2}-2\right].
\]

`stationary.py` derives these equations from the earlier inverse, rather than inserting a dust growth equation. It integrates log m and logit v to avoid spurious rank loss from subtracting v from one at early times. Initial data m(1)=0.1, v(1)=0.5, I=0.1, Q_c=M²=1 and Λ=0.7 are illustrative, not a fit. DOP853 and tighter Radau integrations agree within approximately 2.13×10⁻¹¹ in the integrated log coordinates over 10⁻⁶≤a≤10³. Numerical profile evidence is not a rigorous interval enclosure or all-time existence proof.

## 5. Independent directions and off-background tests

For a local wave with spatial projection g∥ of ∇χ, put w_R=W_Y+2g∥²W_YY and S=W−2g∥²W_Y−2Q²w_R. Direct expansion of the *new action* gives

Here v is the characteristic phase velocity, not the profile coordinate v in the preceding section.

\[
\mathcal P(v)=\begin{pmatrix}
-S & -2Qw_R\\
-2Qw_R & (2P_X+4Q^2P_{XX})v^2+8Qg_\parallel P_{XX}v-2P_X+4g_\parallel^2P_{XX}+2w_R
\end{pmatrix}.
\]

Its degree is two, not the old cubic. The script derives this matrix with a nonzero transverse χ gradient; it does not infer transverse propagation from a longitudinal test.

The bounded test covers 37 epochs, three offsets Q²/q²=1+ηm/(1+m) with η=−1/2,0,1/2, five spatial-gradient ratios |∇χ|/Q=0.001,0.01,0.1,0.5,0.9, and direction cosines 0,1/2,1: **1,665 events**. In every tested event the logarithm domain, clock principal ellipticity, scalar kinetic sign, real characteristics and metric-cone speed bound pass. Characteristic arithmetic uses 70 digits on the float64-integrated background. This is a bounded local principal-symbol result, **not** a universal nonlinear stability, causality or CMB certificate. Positive kinetic energy does not by itself bound interaction strength.

The maximum absolute speed in this sample is approximately 0.9899784 in c=1 units. The early profile approaches v=1 extremely closely, and the logarithm domain narrows as m tends to zero; these limiting behaviors are not ignored or certified healthy by finite sampling. The zero-field and early-time limits remain explicit obligations.

## 6. Actual constraint status and next decisive work

In clock gauge, the primary constraints are p_N=0 and p_i=0; their secondaries are the Hamiltonian constraint C and spatial momentum constraints H_i. Spatial covariance supplies the usual spatial generators. With π=hᵢⱼπⁱʲ, the next constraint, independent of N, is

\[
T=\sqrt h(V_\tau-P_\tau)-\frac{\pi W}{M^2}
-\frac{4W_Y}{M^2}\left(\pi_{ij}D^i\chi D^j\chi-\tfrac12\pi Y\right)
-2Q\partial_i(\sqrt h W_YD^i\chi).
\]

It follows from ∂τC+{C,H₀} after the self-bracket closes on H_i. Preservation next requires E[N]=∂τT+{T,H₀}+{T,C[N]}=0. **The full variable-coefficient operator δE/δN, its global kernel/boundary conditions and final multiplier preservation are not yet certified.** Consequently there is no completed nonlinear first/second-class count. A local principal ellipticity check is not the missing global inverse.

Next calculate that operator and its complete Dirac chain for the logarithmic/square-root action, including homogeneous modes separately; then derive cubic interaction scales and caustic behavior. Radiation and baryons must be varied and evolved before any CMB claim. The exponential MOND source law, galactic Φ and Ψ, PPN parameters and measured Newton constant must still come from a combined action, with all constraints recalculated. The global a₀ relation remains input; no local-a₀ substitution was used.

## Reproduction and external-source scope

`run_checks.py --result-file <fresh-output>/results.json` records the old-action characteristic, both constructive stages, three Lean files and the previous ten-case regression. Exact argv, exits and source/result hashes are in the bounded run manifest and results. The old seven Lean proofs remain true at their stated scope; no old certificate is silently upgraded. New Lean proofs concern a real characteristic root, the transport sign, bracket identities, coefficient matching and stationary restoring response—not the complete field theory.

The distinction between cosmological degeneracy and arbitrary-background Hamiltonian closure is also explicitly made in Iyonaga, Takahashi and Kobayashi, *Extended Cuscuton: Formulation*, arXiv:1809.10935v2 (5 December 2018), Introduction properties [A], [B] and the following discussion; [primary text](https://arxiv.org/html/1809.10935v2). Checked 10 September 2026. This is adjacent context, not a theorem imported to certify our two-field action. No source cache was modified and no novelty search was completed. The 1703.08226 abstract was a discovery pointer only.

Mathbox computation-audit/proof-audit self-review separated the exact action identities, conditional formal proofs, numerical profile and unproved global implications. No external review or global empirical validation is claimed.

Development note: the first Lean cancellation proof did not discharge its nonzero-denominator obligation and exited 1. It was repaired using the explicitly assumed nonzero denominator; only the subsequently successful build is counted. Exploratory matched-response functions motivated the stationary condition but are not promoted to verified candidates. Self-proofreading covered this new report and its displayed equations; no unrelated mathematical files were rewritten.
