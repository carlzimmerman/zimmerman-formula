# Independent critical audit of the full-remainder warm transfer

**Normalized claim.** In the specified spherical, zero-stiffness reciprocal two-species effective model with fixed positive central point baryon mass, the full saturating remainder admits bounded smooth nonnegative invariant distribution functions with strictly negative physical energy slope, positive radial dispersion on the selected closed law annulus, exact prescribed species densities, and finite total stock. Their summed enclosed cold mass equals the full-law target there. This is stationary existence, not warm stability.

**Primary verdict: proved as written**, for the corrected WARM_TRANSFER.md with SHA-256 `0d2bd9654b1c1fdfe17d75399e48bb0dd93f503c3f688d7eb43ba3e93bd751ad`, under its explicit fixed-model, positive-point-baryon, fraction, taper and sufficiently-small-fixed-width hypotheses. The inherited inverse's displayed estimates are applicable to these potentials; I found no hidden use of the cubic force law or M=A r after its initial target specification. This is an analytic proof-transfer audit, not a formal certificate, an independently established microscopic model, or a numerical validation.

## 1. The field being warmed

The relevant model is the separately specified reciprocal energy in SOURCE_RESPONSE.md and FULL_REMAINDER_SHELL.md. Writing B=M_b>0, T=fM and F=(1−f)M, its fixed-field inward accelerations are

\[
h_t=\Phi_t'=\frac{G(B+F)}{r^2}-\mathcal R(u),\quad
h_f=\Phi_f'=\frac{G(B+M)}{r^2},\quad
u=\frac{GfM}{r^2},\quad
\mathcal R(u)=\frac{u^2}{a_0-u}.
\]

The symbol \(\mathcal R\) here avoids confusing the force remainder with the outer support radius. The original inverse uses L for **squared specific angular momentum**. Consequently

\[
U(r,L)=\Phi(r)+\frac{L}{2r^2},\quad
L_c=r^3\Phi',\quad U_{rr}(s,L_c(s))=\frac{L_c'(s)}{s^3}.
\]

It is this actual fixed-background orbit frequency that the inverse needs. A positive coherent-shell quadratic alone would not supply it.

The selected target

\[
C_b(r)=\frac B2\left[\sqrt{1+\frac{4a_0r^2}{GB}}-1\right]
\]

is positive and strictly increasing for r>0. Its full-law identity is \(\mathcal R(GC_b/r^2)=GB/r^2\). The explicit cutoff construction gives 0≤M≤C_b globally, M′>0 throughout the open hollow shell, and M=C_b on the law annulus. The target is **M=T+F**, not T alone. This is necessary for the claimed ordinary-tracer law and avoids adding the free mass twice.

## 2. Actual circular geometry and escape cap

Direct differentiation of the two fixed forces gives

\[
\omega_t^2=\frac{G(B+F)}{r^3}
+\frac{2u\mathcal R'(u)-3\mathcal R(u)}r
+\frac{GM'}{r^2}\big[(1-f)-f\mathcal R'(u)\big],
\]

\[
\omega_f^2=\frac{G(B+M)}{r^3}+\frac{GM'}{r^2}.
\]

Here B′=0 because this warm claim fixes a central point mass. The first line includes the negative tethered own-density term that would be canceled only in a coherent material displacement, so it checks the right orbit problem.

Since M≤C_b, u≤f a_0<a_0, and

\[
\mathcal R'(u)=\frac{u(2a_0-u)}{(a_0-u)^2},\qquad
2u\mathcal R'(u)-3\mathcal R(u)
=\frac{u^2(a_0+u)}{(a_0-u)^2}\geq0,
\]

the remaining density bracket obeys

\[
(1-f)-f\mathcal R'(u)
\geq\frac{1-3f+f^2}{(1-f)^2}\geq0
\]

for the declared 0<f≤(3−√5)/2. The positive baryon term then gives L_c′=r³ω²≥GB>0 on the closed target range. In the hollow interior below r_0 the field is Keplerian; beyond R_out the cold masses are constant and the same positive expressions apply with M′=0. Thus L_c is globally strictly increasing from zero to infinity, giving one global circular minimum for every L>0. The saturation gap and r_0>0 give all required bounded smooth physical derivatives on the closed target range. No cubic approximation is involved.

The escape condition is separate from frequency positivity. For v=GM/r², the exact identity

\[
\mathcal R(fv)\leq f^2\mathcal R(v)\leq f^2\frac{GB}{r^2}
\]

gives \((1-f^2)GB/r^2+GF/r^2\leq h_t\leq G(B+F)/r^2\). Integrating the lower bound toward infinity and using nondecreasing F, then using the upper bound for the circular kinetic term, yields

\[
E_{c,t}=\Phi_t+\frac r2h_t
\leq-\frac G r\big[(1/2-f^2)B+F(r)/2\big],\qquad
E_{c,f}\leq-\frac{G[B+M(r)]}{2r}.
\]

The stated fraction bound is below 1/√2. Hence both circular energies have a fixed negative reserve on [r_0,R_out], independent of the later width. Both exterior force integrals converge. This verifies the required escape cap with the potential constants normalized at infinity; merely claiming attractive force would not suffice.

## 3. Tapers and the hypotheses of the inherited inverse

Let d be the distance to the appropriate edge. Differentiating M=C_b S at the inner edge gives

\[
M'=d^{-2}e^{-D_{\rm in}/d}\,a_{\rm in}(d),
\quad D_{\rm in}=r_1-r_0,
\]

with a positive smooth factor at d=0 because C_b(r_0)>0. At the outer edge, the prescribed derivative gives

\[
M'=e^{-D_{\rm out}/d}\,a_{\rm out}(d),
\quad D_{\rm out}=R_{\rm out}-r_2,
\]

with another positive smooth factor because C_b′(R_out)>0. These are exactly the quantitative edge types used by the pinned inverse. They are stronger than unspecified C∞ flatness, which the inherited proof expressly does not handle arbitrarily.

With h=(r−r_0)²(R_out−r)²/(R_out−r_0)³ and dr/dx=h, h is comparable to d² at either edge. Repeated h∂_r differentiation of −D/d plus logarithmic and smooth terms gives bounded intrinsic logarithmic derivatives of μ_i=M_i′. Flatness dominates every finite inverse power of h and d needed when converting derivatives back to E,L. Multiplying by f or 1−f does not change these properties.

The dependency check on EXACT_SMOOTH_INVERSE.md is as follows:

| inherited proof step | actual input used | full-R transfer |
|---|---|---|
| phase-volume Jacobian | L=L_c(s), dy=ds/h, v=ωh w, C=4π² | passed; independent of force formula |
| local orbital expansion | U_r=0, U_rr=ω², bounded smooth derivatives, ω>0 | passed |
| exclude remote orbit pieces | monotone global L_c, closed-interval lower bound on L_c′, bounded h′ | passed |
| fixed energy/angular-momentum tube | circular escape reserve and edge-distance/h bounds | passed |
| local Fourier mode estimate | W=(x−y)²/2+O((x−y)³) uniformly with intrinsic derivatives | passed |
| weighted Schur bounds and smoothing | mode error O(√b_n), √b_n⟨n⟩ bounded, finite chart overlap, comparable local μ weights | passed |
| fixed-space inverse and bootstrap | small error in X_5 and a one-derivative gain | passed |
| positive, decreasing corrected DF | X_3 height and X_5 first-t-derivative bounds, broad positive baseline | passed |
| C∞ zero extension at the physical edges | exponential μ flatness and finite inverse-power derivative losses | passed |

In particular the exact density Jacobian gives

\[
\mu_{f_i}(r(x))=\frac1Z\int
H_i\big(w^2/2+W_i(x,y),y\big)\,dw\,dy.
\]

The target is μ_i(r(x)), not hμ_i. The factor h from dL and the factor ωh from dv cancel the denominator in the inherited DF. This normalization does not use M=A r or the cubic interaction.

For the key mode estimate, substitute y=x−√b_n z and w=√b_n a. The exact W expansion differs from (a²+z²)/2 by O(√b_n), with all intrinsic x derivatives at that order. Its phase has bounded frequency because |k_n|√b_n≤ζ. Smooth flat cutoffs and bounded chart derivatives therefore produce the same O(√b_n) mode error. No derivative of a cubic force coefficient enters. The Fourier coefficient estimates then yield both the O(δ) X_s error and X_s→X_(s+1) gain claimed by the source.

Inversion is done at one fixed order X_5. The equation q=e−E_δq and the one-derivative gain bootstrap smoothness; the argument does not require δ to be simultaneously small for all Sobolev orders. The inherited X_3 and X_5 estimates make the signed correction small relative to the positive baseline and its negative t derivative. The correction is confined to t<δ²/4, leaving an occupied eccentric-velocity region with positive radial dispersion. Those positivity and endpoint steps need only the already checked geometry and taper bounds.

The original proof's opening deep-cubic choice fixes its example potentials; the later inverse treats Φ and μ as fixed inputs. Its separate stability argument in AUDIT_AND_ROUTES.md is not part of this transfer. I found no later use of the deep-cubic source identity, the sign of the coupled field Hessian, or M=A r in the existence argument.

## 4. Exact self-consistency and the limits of the conclusion

Construct each DF in the fixed potential generated by the chosen target pair. The inverse returns exactly μ_t=fM′ and μ_f=(1−f)M′ at every radius, with zero mass outside the shell. Reinstalling those exact densities into the same density-dependent reciprocal field equations leaves both potentials unchanged. This is an exact stationary self-consistency argument in the specified model, rather than a tracer construction with a neglected source change. On the annulus M=C_b,

\[
g=\frac{G(B+M)}{r^2},\qquad
\frac{GB}{r^2}=\frac{g^2}{g+a_0}.
\]

The law amplitude, total stock, split, dimensions, profile and small width remain chosen state data. The theorem does not select them or match a fixed total-energy preparation budget.

For each fixed sufficiently small δ>0, the physical radial dispersion is comparable to δ²ω_i²h². It is strictly positive on the compact interior law annulus, tends to zero at the two spatial edges, and is not claimed to have a bound uniform in the singular cold limit. The fixed negative energy cap follows by taking δ small relative to the circular reserve. Angular momentum stays in the fixed finite positive interval bounded by L_c(r_0) and L_c(R_out).

The original phrase “compact phase-space support inside r_0<r<R_out” required a topological clarification: μ>0 arbitrarily close to both edges, so the support closure cannot be a compact subset strictly inside that open radial interval. The corrected proof now states compact support in the **closed** shell, with positive-density points in the open shell and closure touching its flat edges. That is the convention under which the current verdict is given; no wall or positive-density edge layer is introduced.

No stability conclusion follows merely from f_E<0 or the existence inverse. The full-R coherent-shell quadratic concerns another perturbation class and a singular baseline. Warm radial stability would require its own coupled quadratic/dynamical theorem; nonspherical and nonlinear stability, actual-path confinement, finite stiffness, dynamical baryons, metric/lensing, capture, population formation and cosmological supply remain separate. No frozen empirical pass is transferred to these constructed states.

## 5. Remaining obligations and review provenance

There is no missing cubic-to-full-R implication in the normalized stationary existence transfer after the verified geometric and taper hypotheses are supplied. The unsupported extension would be to warm stability or physical state selection, neither of which is asserted here. The cheapest next mathematical task is to state a warm perturbation class and derive its coupled field/kinetic quadratic; that is a new task, not an inference from this existence result. A physical completion still needs the microscopic source, selected loading and finite conversion/receiver dynamics.

This reviewer did not author WARM_TRANSFER.md, FULL_REMAINDER_SHELL.md or the pinned inverse. I read the actual formulas and reconstructed the relevant implications; prior reviewer agreement was not used as proof. Only this audit was written for this transfer. No scientific computation, source execution, numerical integration, fit or simulation was run. Hashing and reading exact source bytes are the only machine checks.

Requested base: `f659e6d8e1ee4cf2b756f091aff56b018da1fb1e`. Final corrected proof read at 2026-10-20 15:37:42 UTC; observed HEAD `92ab2566731115bd869a639fbe49e4e260d6a0ae`. The two inherited inverse/audit documents match that base byte for byte. The new model/transfer documents are later additions, not frozen-base results.

| exact source | bytes | SHA-256 |
|---|---:|---|
| full_remainder_shell/WARM_TRANSFER.md, corrected support wording | 8509 | `0d2bd9654b1c1fdfe17d75399e48bb0dd93f503c3f688d7eb43ba3e93bd751ad` |
| full_remainder_shell/FULL_REMAINDER_SHELL.md | 16461 | `9d92fbdeb4dcf0d8c9d29335c174445d9f2396b19afc15dbc279f2680eb625b9` |
| full_remainder_shell/SOURCE_PINS.json | 1592 | `0d53577229b8bced25b18da3e8b8783b0c5d4b425a4ca37d25b8887bc17552de` |
| reciprocity/SOURCE_RESPONSE.md | 9991 | `6deb1b415ac7f5a1713754ea5526a05b878445fa8d6c7e98888114815401e173` |
| smooth_exact_2026_10_18/EXACT_SMOOTH_INVERSE.md | 13781 | `490b137269ea5c918dae517085974752a3e1bc3d9df4f3e88b99eeccde41a55b` |
| smooth_exact_2026_10_18/AUDIT_AND_ROUTES.md | 7341 | `c8cf72749343a2493d6bb9b93eb98fcd5454836e223704ed5685e6aa6d5778c2` |

Initial transfer read: 8396 bytes, SHA-256 `ff79787356e28516b188a6a33694aa558162673a413be29fbb7c97e00970e85c`. The only change during this audit was the author's closed-shell/occupied-point/support-closure wording correction, read and accepted above. No new orbital, inverse, positivity or self-consistency argument was inserted by the auditor. Mathematical proofreading of this audit checked signs, coefficient factors, the squared-angular-momentum convention and display delimiters; it did not modify author source.
