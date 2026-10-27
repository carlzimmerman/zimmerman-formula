# Round 2: full vector stiffness from specified material models

**The scale is still not derived.** This round supplies three stronger results: a scoped obstruction to an ordinary elastic-displacement origin; an explicit alignment lattice that generates the complete longitudinal and transverse operator; and a local mediator whose full dynamical response can be integrated and tested. The latter two retain an unfixed coefficient even after stability, tensor matching, interaction range and propagation speed are specified. An internal optical coordinate also fails the single-medium total-mass displacement dictionary at linear order.

Published base: `8aa3f7046a7ae14a99f3515fd42df5bf061fb1db`. Only immutable round-1 sources in `/private/tmp/core-open-publish.GPoQNP` were used; their exact hashes are in [source_map.json](source_map.json). No other round-2 lane was consulted. The complete candidate arguments appear in [raw_derivation.md](raw_derivation.md), sent for coordinator review before the final narrative. The computations below passed **29/29 checks**, plus four optional frozen-source hash comparisons. This is a bounded research checkpoint, not a microscopic completion of S2 or a claim of exhausted possibilities.

## 1. The target and what changed since round 1

Keep the exact canonical normalization

\[
 K=4\pi G,\qquad F_{\rm grad}=\frac\gamma2\int|\nabla P|^2\,d^3x,
 \qquad \gamma=\frac{K L_*^2}{2}.
\]

The full target Fourier Hessian is \(\gamma k^2 I_3\). Matching pressure alone gives only the longitudinal projector. The inherited gravitational-plus-local Hessian about a homogeneous background is

\[
 H_0(\hat k)=K\{\Pi_T(\hat k)+B I+(A-B)ee^T\},\quad
 B=\frac{s}{1-s},\quad A=\frac{s(2-s)}{(1-s)^2},
 \quad s=K|P_0|/a_0.
\]

It is positive for \(0<s<1\), while its longitudinal vacuum mode is gapless. This round retains \(H_0\), \(W_{\rm rem}\), and the gravitational coupling as supplied inputs. It does not derive them from the material constructions.

The benchmark interval is inherited unchanged: 24 pc is the primary canonical globular lower edge; 1 kpc was a scan boundary; the soft SPARC upper edge is 2.042 kpc canonical / 2.138 kpc alternate under the stated screening approximation. None of these numbers was used to choose a model parameter. Requirements calculated at those lengths are explicitly conditional comparisons.

## 2. Ordinary elastic displacement: a precise limitation

Assume a homogeneous, isotropic, stress-free solid with no prestress, ordinary displacement \(\xi\), positive density \(\rho_0\), and the S3 dictionary \(P=-\rho_0\xi\). Its quadratic frame-indifferent strain energy is

\[
 F_{\rm el}=\int\left[\frac\lambda2(\operatorname{tr}\varepsilon)^2+
 \mu\varepsilon_{ij}\varepsilon_{ij}\right]d^3x,
 \qquad\varepsilon_{ij}=\frac{\partial_i\xi_j+\partial_j\xi_i}{2}.
\]

Direct differentiation gives

\[
 D_{\rm el}(k)=\rho_0^{-2}\{\mu k^2 I+(\lambda+\mu)kk^T\}.
\]

Matching **both** canonical sectors forces

\[
 \mu=\gamma\rho_0^2,\qquad\lambda=-\mu,
 \qquad B_{\rm bulk}=\lambda+\frac{2\mu}{3}=-\frac\mu3<0.
\]

Uniform affine compression \(\xi=\alpha x\) then has energy density \(-3\mu\alpha^2/2\). Thus a stress-free solid with positive bulk and shear moduli cannot provide this full operator in this dictionary.

**The boundary qualification is essential.** For periodic or decaying fields, integration by parts instead gives

\[
 F_{\rm el}=\frac\mu2\int|\nabla\xi|^2+
 \frac{\lambda+\mu}{2}\int(\nabla\cdot\xi)^2.
\]

At \(\lambda=-\mu\), every nonzero plane-wave mode is positive. The negative affine modulus therefore does **not** prove canonical S2 unstable or exclude a pinned model with restricted boundaries. It excludes the proposed stress-free ordinary-solid origin. Prestress, anchors, micropolar degrees of freedom and internal-vector order parameters change its hypotheses. Also, an infinitesimal rigid rotation has zero ordinary strain energy but nonzero local \(|\nabla\xi|^2\); exact local-energy matching requires more than matching periodic Fourier operators.

This is new information beyond round 1's observation that a fluid lacks shear: simply adding a healthy ordinary shear modulus does not complete the required tensor structure in a free solid.

## 3. Alignment lattice: full operator obtained, amplitude free

Specify a cubic lattice of spacing \(b\) with an internal vector \(p_R\) at each cell. Each positive-axis bond is counted once and has energy

\[
 F_b=\frac J2\sum_{R,\alpha}|p_{R+b e_\alpha}-p_R|^2,
 \qquad T=\frac M2\sum_R|\dot p_R|^2,\qquad J,M>0.
\]

The physical normalization is \(p=P\). For a literal internal displacement \(d\), inertial mass \(m_{\rm cell}\), spring constant \(j\), and polarization normalization \(P=\zeta d\), this means \(M=m_{\rm cell}/\zeta^2\) and \(J=j/\zeta^2\). The generalized \(M\) is not automatically a particle mass.

The **exact** bond Hessian per volume is

\[
 D_b(k)=\frac{4J}{b^3}\sum_{\alpha=1}^3
 \sin^2(k_\alpha b/2)\,I_3.
\]

Consequently,

\[
 \boxed{\gamma=J/b=j/(\zeta^2b)},\qquad
 I_{\rm eff}=M/b^3,\qquad c_{\rm ac}^2=Jb^2/M,
 \qquad L_*^2=2J/(Kb).
\]

This specified positive microscopic bond energy supplies both vector sectors. The finite lattice has cubic anisotropy, but the leading continuum term is isotropic. The 1% relative-gradient-error boundary is \(kb=0.345377\) along an axis and 0.598210 along the body diagonal. A real-space 125-site lattice and its complete 375-coordinate vector Hessian reproduce the independently calculated Fourier eigenvalues. A bond-tensor mutation with different stiffness along and across a bond remains stable but breaks the canonical equality, demonstrating that equality is a constitutive restriction.

For fixed \(b\), the continuous family

\[
 (J,M)\longmapsto a(J,M),\qquad a>0,
\]

preserves every frequency of the pure bond system, its acoustic speed and all relative derivative errors, but multiplies \(\gamma\) and \(L_*^2\) by \(a\). Its local potential and gravitational coupling can stay unchanged. Background restoring frequencies from those retained terms are **not** invariant. Thus the construction does not select \(J/b\) from stability, speed or the full tensor match. Independently measured mass, polarization normalization, spacing and spring constants could determine it; none is supplied by canonical S2.

The isolated bond system has an independent internal-rotation symmetry, but \(P\cdot\nabla\Phi\) removes that independence. The remaining simultaneous rotation symmetry permits distinct divergence and curl coefficients. No radiative protection of their equality is claimed.

### The mass-displacement transfer test

For two positive masses \(m_1,m_2\) in a cell, an optical separation \(d\) at fixed center of mass moves them by \(m_2d/(m_1+m_2)\) and \(-m_1d/(m_1+m_2)\). Therefore

\[
 m_1\delta x_1+m_2\delta x_2=0,
\]

and the internal change in the total density Fourier amplitude starts at

\[
 \delta\rho(k)=-\frac{\mu_{\rm red}}2(k\cdot d)^2+O((k\cdot d)^3),
 \qquad \mu_{\rm red}=\frac{m_1m_2}{m_1+m_2}.
\]

There is no linear total-mass dipole to identify with \(\delta\rho=\nabla\cdot P\) and \(P\propto d\). A single-species polarization, a separate center-of-mass mode or an external anchor changes that conclusion's scope. The alignment model thus matches the spatial operator while its mapping to S3 remains open; calling an optical coordinate a mass displacement would skip a substantive obstruction.

## 4. Local mediator: exact response and a second freedom test

To advance beyond an instantaneous bond kernel, introduce a second internal vector \(q\). For each eigenvalue \(h\ge0\) of the inherited \(H_0\), specify

\[
 \mathcal L_2=\frac I2\dot p^2+\frac{J_q}2\dot q^2
 -\frac h2p^2-\frac C2(q-p)^2-\frac D2|\nabla q|^2,
 \qquad I,J_q,C,D>0.
\]

The continuum \(D\) can be supplied by the alignment coefficient \(J/b\); the mediator action alone does not predict it. Eliminating \(q\) gives the exact frequency-dependent inverse response

\[
 H_{\rm eff}(\omega,k)=h+C-I\omega^2-
 \frac{C^2}{C+Dk^2-J_q\omega^2}.
\]

In the static limit,

\[
 \boxed{H_{\rm eff}(0,k)=h+\frac{Dk^2}{1+\ell^2k^2}},
 \quad\ell^2=D/C,\quad\gamma=D.
\]

The same scalar correction applies to all three inherited eigenmodes. The relative error of its local-gradient approximation is **exactly \((k\ell)^2\)**. At high \(k\) it saturates at \(C\), so it cannot be substituted for canonical stiffness outside its derivative expansion. A lattice-generated \(D\) adds the independent requirement \(kb\ll1\).

The exact two-branch dispersion obeys

\[
 IJ_q\omega^4-[J_q(h+C)+I(C+Dk^2)]\omega^2
 +(h+C)(C+Dk^2)-C^2=0.
\]

The kinetic form is positive, and the potential determinant is
\(Ch+Dh k^2+CDk^2\). Hence both branches have nonnegative \(\omega^2\), with a zero mode only at \(h=k=0\). At that vacuum point,

\[
 c_{\rm ac}^2=\frac D{I+J_q},\qquad
 \Omega_{\rm opt}^2=\frac{C(I+J_q)}{IJ_q}.
\]

The low-energy response contains inertia \(I+J_q\), not \(I\). The expansion requires \(|Dk^2-J_q\omega^2|\ll C\) away from mediator poles. Dropping the auxiliary inertia fails an executed mutation test.

The material PDE's propagating characteristic speed is \(v_q=\sqrt{D/J_q}\); the other principal component is a local oscillator. Imposing \(v_q\le c\) restricts this material sector. **It does not establish relativistic gravitational causality:** \(\Phi\) remains the Newtonian constraint, and the lattice is a preferred-frame microscopic model.

The family

\[
 (D,C,J_q,I)\longmapsto a(D,C,J_q,I)
\]

preserves \(\ell\), \(v_q\), the vacuum acoustic speed, optical gap and entire \(h=0\) spectrum, while changing \(\gamma\) by \(a\). It again fails to preserve background restoring frequencies for fixed nonzero \(h\). If inertia were fixed independently, a front-speed condition would give an inequality rather than select one \(\gamma\).

### A discriminating resolution requirement

As an explicit EFT check, demanding 1% static accuracy at \(k=1/{\rm AU}\) requires \(\ell\le0.1\) AU. Since \(C/K=L_*^2/(2\ell^2)\), this gives

| Comparison \(L_*\) | Required \(C/K\), at least |
|---|---:|
| 24 pc | \(1.225\times10^{15}\) |
| 1 kpc | \(2.127\times10^{18}\) |
| 2.042 kpc | \(8.870\times10^{18}\) |

These are model-validity requirements, not fitted constants or new observational exclusions. They show that identifying the microscopic interaction range with the macroscopic coefficient length is insufficient.

If one additionally assumes \(I+J_q=1/\rho_c\), let \(f=J_q/(I+J_q)\). Then \(v_q^2=c_{\rm ac}^2/f\), so the material speed condition is \(f\ge(c_{\rm ac}/c)^2\). At the assumed canonical cosmic density this lower bound is \(5.67\times10^{-18}\) for 24 pc and \(9.84\times10^{-15}\) for 1 kpc. It leaves a broad continuum of coefficients/inertia partitions and does not select \(L_*\). This optional density dictionary has not been justified for the internal-vector model. No early-universe abundance, cosmological evolution or observational viability was computed.

## 5. Evidence, scope and next step

The executed checks include exact strain and mediator Hessians; 125-site scalar and 375-coordinate vector lattice spectra; 48 directional lattice comparisons; 2,268 two-mode parameter cases; 468 full six-component response matrices over six backgrounds, thirteen directions and six wave numbers; optical density multipoles; sign/tensor/inertia mutations; and continuous scaling-family checks. The full six-mode matrices agree with the independent scalar-branch calculation to a maximum normalized error \(1.75\times10^{-12}\). Exact positive-form arguments, not finite scans, establish stability in the specified positive-parameter regime.

The coordinator independently reconstructed the elastic matching, affine/boundary distinction, mass-dipole cancellation, mediator Schur complement and determinant from the raw derivation. Its review agreed with those scoped claims and emphasized the same inertia and Newtonian-causality qualifications. This is an algebraic review, not an independent microscopic or cosmological validation. [review_receipt.md](review_receipt.md) records its coverage.

Run without source documents, git, network or skill installations:

```sh
python3 -m pip install -r core_open_problems_round2_2026_10_20/04_stiffness/requirements.txt
python3 core_open_problems_round2_2026_10_20/04_stiffness/run_checks.py --output-dir /tmp/stiffness-round2-replay
```

The optional `--verify-frozen-root PATH` compares documentary hashes against the published checkout. The primary run's [manifest](results/manifest.json) records software, ranges, commands and exact input/output hashes; [checks.json](results/checks.json) contains the full finite record. A detached script-only replay reproduces the numerical record exactly; documentary verification has no role in its mathematics.

The first manifest mislabeled the requested published base as the execution checkout's HEAD. Coordinator review caught this provenance error; the script now observes HEAD and dirty state at run start and records the requested base separately. The current run is regenerated, and the old manifest/script are retained under `results/superseded_provenance/` as superseded records. The numerical assertions and results did not change. Detached replay records Git as unavailable, rather than inventing a revision.

**Smallest unresolved step:** specify a microscopic degree of freedom whose normalization and coupling make it the actual total-mass displacement \(P\), while its interaction supplies the full tensor stiffness with independently determined strength. The stress-free solid and isolated optical-coordinate constructions fail different parts of that mapping. The mediator supplies controlled dynamics after the mapping is assumed, but cannot choose its amplitude.

A next discriminating calculation would use a concrete anchored two-component medium, include the anchor's recoil and gravitational source, and derive the center-of-mass and relative response together. It must show which measured mass current satisfies S3 and whether integrating the other mode preserves the full tensor coefficient without an extra unmeasured spring constant. This continuation is untried and remains open. Thermal-history completion of the round-1 contact model is deferred because it would still lack this tensor/mass mapping. No route is described as universally exhausted.
