# The halo half and the vacuum coefficient

The cosmological coefficient remains **underived**. The strongest exact positive result is still the point-mass equivalence between the quadrature law and local isotropic pressure support with \(P=\rho v_c^2/2\). Today's proposed GF2 shortcut does not derive the vacuum coefficient from that halo half. The two ratios can differ in an explicit countermodel. For the full G002 one-function kernel, this review also obtains a closed pressure expression that distinguishes an exact identity from a deep-limit identity.

This is a research checkpoint dated October 8, 2026, based on commit `22a527e4445ed0299ebfe3966fd95da80be8ab3f`. Existing uncommitted work was left alone. The original objective is to derive the physical coefficient in \(a_0=(c/2)\sqrt{G\rho_\Lambda}\), or obtain exact useful consequences and identify the remaining implication. A coefficient derivation must fix the *measured* acceleration relative to vacuum mass density without imposing their ratio. A halo identity alone does not meet that criterion.

## What the last week changes

The October 1–8 Git history contains 852 commits at the starting checkpoint. This review searched that history and read the relevant coefficient summaries and selected raw arguments; it is not an independent audit of every commit or empirical result.

| Work reviewed | Useful conclusion | Remaining issue |
|---|---|---|
| `sonnet55_push/puzzle_32pi/README.md`, especially corrections and sections 53–70 | The vacuum-integral route connects the coefficient to a complete interpolation kernel, including its high-field end. The simple geometric and hyperbola rewritings leave a free physical normalization. | Neither the required kernel cutoff nor a compatible complete theory is selected. Empirical exclusions in those sections were not re-fit here. |
| `sol61_push/CUTOFF_SOURCE_AND_TRACE_CHECKPOINT_2026-10-06.md` | Source calibration and stable scalar constructions narrow specific candidate mechanisms. | Stability alone does not select the vacuum/response ratio; the documented bounds are conditional on those actions. |
| GF1, October 8 | \(a_0=s/n\), with \(s=c\sqrt{G\rho_\Lambda}\), is a convenient parameterization. | Algebra does not force \(n\) to be an integer or select \(n=2\). The input register's near-perfect numerical closure is not a new independent measurement. |
| GF2, October 8 | A log-potential isothermal halo has \(\sigma^2/v_c^2=1/2\). | Identifying this ratio with \(a_0/s\) is the missing implication. General barotropy is also weaker than the pressure law used in the calculation. |
| CFG9 and CFG44 | The exact P2 pressure identity and its converse were already derived. | Their acceleration normalization and dynamical formation are additional requirements. They should not be rediscovered as new coefficient derivations. |
| October 8 CFG484, CFG488 and CFG489 commit records | A GR plus cold-fluid construction remains an active alternative; shell composition alone does not supply a new settling law. | CFG489 was criteria-only at this checkpoint. This review does not claim to have run its fluid dynamics. |

## The two halves are different quantities

Use separate symbols:

\[
k_{\rm halo}=\frac{P}{\rho v_c^2},\qquad
k_{\rm vac}=\frac{a_0}{c\sqrt{G\rho_\Lambda}}.
\]

For \(C>0\), \(r>0\), the Newtonian log branch gives

\[
g=\frac C r,\quad v_c^2=C,\quad
\rho=\frac{C}{4\pi G r^2},\quad
P'= -\rho g.
\]

Integration yields \(P=C\rho/2+P_0\). The isothermal choice \(P_0=0\) gives \(k_{\rm halo}=1/2\), for **every** \(C\). Writing \(C=\sqrt{GM_ba_0}\) still permits every positive \(a_0\). Vacuum density does not appear in these equations.

These are formal Newtonian point-source and halo equations. Their physical use is restricted to the weak-field domain; neither a singular origin nor an infinite halo is being asserted as a complete relativistic configuration.

An explicit countermodel to the claimed implication sets \(c=G=\rho_\Lambda=s=1\), \(a_0=1/3\), \(M_b=3\), and \(C=1\). Poisson, hydrostatic equilibrium, the log branch, and \(C^2=GM_ba_0\) all hold. Yet

\[
k_{\rm halo}=\frac12,\qquad k_{\rm vac}=\frac13,
\qquad A\Lambda=72\pi^2\ne32\pi^2.
\]

Here \(A=\pi c^4/a_0^2\) is the Schwarzschild comparison area used in the puzzle and \(\Lambda=8\pi G\rho_\Lambda/c^2\). It is not a claim that this comparison black hole is embedded in the same de Sitter solution. Likewise, the countermodel refutes an implication between the stated local equations, not the existence of a complete theory enforcing a further vacuum relation.

GF2's decisive unsupported step is `GF2_closure_half.py`, L1c: it **defines** the computed halo ratio as the framework's kappa and then applies GF1's separate vacuum identity. The cited temperature ladder (`G132`, `G151`, `G163`) takes \(a_0\) and the halo dispersion as inputs; it does not supply that equality.

The same point survives inside GF1's own interpolation family:

\[
\mu_n(u)=1-(1+u)^{-n},\quad u=g/s,\quad
\mu_n(g/s)g=g_N.
\]

For every real \(n>0\), \(\mu_n(u)=nu+O(u^2)\), so \(a_0=s/n\). Every member has \(g\sim\sqrt{GM_bs/n}/r\) at large radius and hence the isotropic, zero-boundary-pressure asymptote \(k_{\rm halo}\to1/2\). Taking the permitted integer \(n=3\) already separates that half from \(k_{\rm vac}=1/3\). Flatness cannot count these channels.

**Audit verdict:** GF2's claim to derive the vacuum coefficient is **incomplete, with the smallest missing implication \(k_{\rm halo}=k_{\rm vac}\)**. The local-equations implication without this bridge is refuted by the countermodel. Its isothermal halo calculation survives.

| Dependency or obligation | Review status |
|---|---|
| Log field to inverse-square density by Poisson | Passed, exact differentiation |
| Constant isothermal dispersion to the halo half | Passed under the stated restriction |
| General barotropy implies the same pressure ratio | Failed, boundary offset retained below |
| Halo half equals vacuum coefficient | Not established; local-equation countermodel supplied |
| Temperature ladder supplies the equality | Not established; its acceleration scale is an input |
| Poisson and hydrostatics prove formation or stability | Out of scope |

## Barotropy and the boundary matter

Barotropy means \(P=P(\rho)\); it does not mean \(P=\rho\sigma^2\) with constant \(\sigma^2\) and zero pressure offset. For a log halo ending at \(R\) with pressure \(P_R\), the exact equilibrium is

\[
P(r)=\frac{C^2}{8\pi G}
\left(\frac1{r^2}-\frac1{R^2}\right)+P_R.
\]

At a free boundary \(P_R=0\),

\[
\boxed{\frac{P}{\rho v_c^2}=\frac12\left(1-\frac{r^2}{R^2}\right).}
\]

The ratio is \(3/8\) at \(r=R/2\), \(0.095\) at \(r=0.9R\), and tends to zero at the edge. The derivative \(dP/d\rho=C/2\) remains fixed: sound-speed squared and \(P/\rho\) must not be conflated. To preserve the exact isothermal half up to the edge requires exterior pressure \(P_R=C^2/(8\pi G R^2)\), or a separately specified boundary stress. This is an equilibrium boundary condition, not a claim of dynamical stability.

GF2's broad uniqueness wording also needs the isothermal restriction. A different self-gravitating barotropic power law on \(0<r<R\) is

\[
\rho=\frac A r,\quad g=2\pi GA,\quad
P=2\pi GA^2\log(R/r).
\]

It satisfies Poisson and hydrostatics, has nonnegative pressure, and has \(dP/d\rho=2\pi GA^2/\rho>0\). Thus \(\gamma=2\) is not the unique *barotropic* self-gravitating power law. It is the nontrivial scale-free one for a constant isothermal dispersion under the stated self-source assumptions.

## The exact result for the quadrature law

For a point baryonic mass, let \(g_N=GM_b/r^2\), \(r_M=\sqrt{GM_b/a_0}\), and \(x=r/r_M\). Under

\[
g^2=g_N^2+a_0g_N,
\]

the additional density and its isotropic equilibrium pressure with \(P(\infty)=0\) are

\[
\rho_c=\frac{M_b}{4\pi r_M^3 x\sqrt{1+x^2}},\quad
P=\frac{a_0M_b}{8\pi r^2},\quad
\boxed{P=\frac12\rho_c v_c^2.}
\]

Conversely, outside a point source, Poisson plus hydrostatics plus this exact half imply \(\rho_c r^3g=Q\), a constant. For \(w=r^2g\),

\[
(w^2)'=8\pi GQr,\qquad
w^2=(GM_b)^2+4\pi GQr^2.
\]

The quadrature law follows with \(a_0=4\pi Q/M_b\). This is the existing CFG9 theorem, independently checked here. It fixes a **shape conditional on the pressure closure**, not the charge \(Q\) relative to vacuum density. A finite free boundary replaces the half by exactly the same factor \(\tfrac12(1-r^2/R^2)\) above, while leaving the interior density and field unchanged. Maintaining the original half needs \(P_R=a_0M_b/(8\pi R^2)\).

## A closed pressure formula for the full one-function kernel

The G002 member \(\mu_2(u)=1-(1+u)^{-2}\) is distinct from the quadrature kernel. For a general increasing \(\mu(u)>0\) in the point-mass relation \(g\mu(g/s)=GM_b/r^2\), define

\[
D(u)=\frac{u\mu'(u)}{\mu(u)},\qquad
r^2=\frac{GM_b}{su\mu(u)}.
\]

Poisson and the zero-pressure condition at infinity give

\[
\rho_c=\frac{M_b}{2\pi r^3}\frac{D}{\mu(1+D)},\quad
P(u)=\frac{s^2}{4\pi G}\int_0^u v^2\frac{\mu'(v)}{\mu(v)}\,dv,
\]

\[
\frac{P}{\rho_c v_c^2}
=\frac{1+D}{2u^2D}\int_0^u v^2\frac{\mu'(v)}{\mu(v)}\,dv.
\]

For \(\mu_2\), this becomes the explicit expression

\[
\boxed{
\frac{P}{\rho_c v_c^2}
=\frac{u^2+3u+4}{4u^2}
\left[4\log(1+u/2)-2\log(1+u)\right].}
\]

It tends to \(1/2\) as \(u\to0\), equals approximately \(0.471132\) at \(u=1\), and behaves as \(\tfrac12\log u-\log2+o(1)\) at large \(u\). Therefore the full one-function halo does not have an exact universal half even with the zero-pressure condition. Its asymptotic half remains compatible with the other integer members. This explicit expression was derived in this review; no literature-wide novelty claim is made.

## What the \(32\pi^2\) puzzle now requires

With physical SI acceleration and vacuum **mass** density,

\[
A\Lambda=\left(\frac{\pi c^4}{a_0^2}\right)
\left(\frac{8\pi G\rho_\Lambda}{c^2}\right)
=\frac{8\pi^2}{k_{\rm vac}^2}.
\]

Thus \(32\pi^2\) is equivalent to \(k_{\rm vac}=1/2\). GF1's displayed \(A\Lambda=8\pi^2n^2/c^4\) uses the geometric-area formula with a physical acceleration; in SI the area carries \(c^4\), and the dimensionless product is \(8\pi^2n^2\). This units correction does not select \(n\).

Three routes were tested here: the GF2 halo-to-vacuum identification, a selection of GF1's \(n\) by the halo half, and the all-radius pressure criterion for the actual kernels. The first lacks a bridge, the second admits the explicit \(n=3\) counterexample, and the third recovers the known P2 shape while leaving its amplitude free and distinguishing it from \(\mu_2\).

The next meaningful coefficient calculation needs an independently specified action or boundary law that fixes \(a_0/(c\sqrt{G\rho_\Lambda})\). It must continue to do so when the halo amplitude, boundary pressure and interpolation-family parameter are left free at the start. Repeating the local halo-half algebra cannot supply that information. The action-based vacuum selector remains open; its October 6 coupling-selection gap was not removed here. Fluid formation and stability likewise remain open and are separate from these exact equilibrium results.

## Verification and provenance

`checks_v2.py` contains exact symbolic residuals, the countermodel, finite-boundary controls, and independent radial pressure integrations for \(n=1,2,3\) and \(u=0.01,0.1,1,10,100\). The field-based integral is checked against a direct radial integral whose implicit field is solved separately. The radial integral extends 25 logarithmic radius units; its omitted asymptotic tail is negligible for the declared tolerance, but it is a bounded numerical check, not the proof.

The original `checks.py`, `contract.json` and `run_main/` preserve a 60-second symbolic-limit timeout. SymPy's general simplifier had combined the logarithms into an expensive expression for its limit engine. Version 2 simplifies only the rational prefactor and leaves the logarithms expanded; the mathematical expression and assertion are unchanged. The interrupted unbuffered diagnostic reproduced the problematic limit before that change.

`contract_v2.json`, `run_main_v2/` and `run_mutation/` preserve the final inputs, outputs, versions and commands. **Main: 40/40 passed, exit 0. Mutation: 39/40, exit 1**, with exactly the intended log-halo hydrostatic failure when its pressure coefficient is changed to 0.51. All three manifests, including the timeout, validate against their retained input and output hashes. The displayed analytic derivations are the universal arguments. Review is a separate adversarial self-review, not an independent-agent certificate. Mathematical proofreading covered this report and its equations; earlier research files and their verdicts were not rewritten.

## Continuation

The [variational response continuation](variational_response/REPORT.md) derives a sharp minimum-gradient bound, a nearby explicitly selected interpolation law, the exact 28/27 gradient-energy comparison for the quadrature state, and a direct-energy obstruction. The vacuum normalization remains open.

The [critical spinor continuation](critical_spinor_response/REPORT.md) supplies a proposed analytic source-coupled parent for deep MOND, derives its exact spherical mass correction and finite-shell threshold, checks a local dynamical sector, and proves a trial-state obstruction for a specified relaxed fluctuation model. Critical tuning, full interpolation, and the vacuum coefficient remain unresolved.

The [flux-gradient continuation](flux_gradient_response/REPORT.md) replaces the spatial term, preserves an exact P2 exterior branch, proves conditional suppression for regular monotone sources, computes matched-source examples, and derives a coercive second variation covering angular perturbations of aligned spherical backgrounds away from zero-field points. The [fifty-step research map](flux_gradient_response/NEXT_50.md) separates the remaining mathematical, physical, observational and vacuum-normalization obligations.
