# A nonlinear extension of field–orbit reciprocity

2026-09-21; base revision `44f1694720574d9f5a2d46ce6b5e1d215d142627`.

**Result:** a source-dipole-subtracted, opposite-side force statistic has a
universal far-field limit fixed by the isolated orbital slope. For the same
isolated rotation curve it distinguishes AQUAL from QUMOND:

\[
\boxed{\mathcal N_{\rm AQUAL}=\frac{1+2\beta}{1-2\beta}},
\qquad
\boxed{\mathcal N_{\rm QUMOND}=\frac{1+2\beta}{2}}.
\]

Here \(\beta=d\ln v_c/d\ln r\) belongs to an **isolated spherical exterior**
at the same physical acceleration as the uniform background in the separate
external-field experiment. In the deep limit, \(\beta=0\), the two coefficients
are **1 and 1/2**, respectively. This is a factor of two in the normalized
nonlinear coefficient, not in total gravity, velocities, or detection significance.

The new content relative to the reviewed repository material is the explicit
quadratic exterior solution, its axial cancellation of the second response
derivative, and the radial subtraction that removes the unknown source dipole.
The existing package `../field_orbit_reciprocity_2026_09_20/` treats the leading
linear anisotropy. Older directional-EFE scripts already study lopsidedness;
lopsidedness itself is **not** a discovery here.

**Evidence status:** a conditional asymptotic theorem, exact second-order
calculation, and bounded numerical verification. The general-source theorem
assumes a twice-differentiable multipole expansion with a controlled asymptotic
remainder; its existence for every nonlinear AQUAL solution is not proved here.
This is a substantive research advance within the searched repo, not an
established new law of nature or a global priority claim.

## Define a force statistic that actually removes the nuisance

Write \(\Phi=g_e z+\phi\), with \(g_e>0\). The positive z-axis follows the
**external potential gradient**, opposite the external gravitational acceleration.
Subtract this uniform background before defining inward axial forces:

\[
F_+(r)=\partial_z\phi(0,0,r),\qquad
F_-(r)=-\partial_z\phi(0,0,-r),
\]
\[
S(r)=\frac{F_+(r)+F_-(r)}2,\qquad
D(r)=\frac{F_-(r)-F_+(r)}2,\qquad
\mathcal K=\lim_{r\to\infty}r^2 S(r)>0.
\]

The nonlinear statistic is

\[
\boxed{\mathcal N=\lim_{r\to\infty}
 \frac{2g_e r^4}{3\mathcal K^2}\,[D(r)-8D(2r)].}
\]

Equivalently replace \(r^4/\mathcal K^2\) by \(1/S(r)^2\) inside the limit.
Thus neither source mass nor a separately fitted acceleration normalization is
needed to define the ideal field statistic. This replacement does not remove
measurement uncertainty in \(S\), the background, or the radial coordinates.

Why the subtraction is essential: the axial odd potential has the expansion

\[
\frac{\phi(r\hat z)-\phi(-r\hat z)}2
 =\frac{d}{r^2}+\frac{B}{r^3}+o_1(r^{-3}),
\qquad B=\frac{\mathcal K^2}{g_e}\mathcal N.
\]

Consequently \(D=2d/r^3+3B/r^4+o(r^{-4})\). The dipole \(d\) depends on
source matching and can dominate the raw asymmetry. The combination at r and 2r
annihilates it. Even potential multipoles, including the quadrupole at
\(r^{-3}\), cancel in the opposite-side difference itself.

If the next odd potential term is \(o/r^4\), a three-radius version cancels
that term too:

\[
\mathcal N_3(r)=-\frac{2g_e r^4}{3\mathcal K^2}
 [D(r)-40D(2r)+256D(4r)].
\]

The large weights amplify measurement noise. This is a mathematical extraction
rule, not a demonstrated observing strategy or a claim that the asymptotic
limit can be reached in a real tidal environment.

## The mechanism

For AQUAL, let

\[
\mu_e=\mu(g_e)>0,\quad L=\frac{g_e\mu'_e}{\mu_e},\quad
M=\frac{g_e^2\mu''_e}{\mu_e},\quad \Gamma=1+L>0,
\]
\[
\zeta=z/\sqrt\Gamma,\quad s=\sqrt{x^2+y^2+\zeta^2},\quad
t=\zeta/s,\quad C=\frac{GM_b}{\mu_e\sqrt\Gamma},\quad
A=\frac{L+M/2}{\Gamma}.
\]

The monopole is \(\phi_1=-C/s\). The universal monopole-induced quadratic
part of the exterior potential is

\[
\boxed{\phi_2=\frac{C^2}{g_e\sqrt\Gamma\,s^3}
 \left[(A-L/2)t+(3L/2-A)t^3\right].}
\]

On the axis, \(t=\pm1\). The two coefficients sum to \(L\), eliminating
\(M\), and the stretched-coordinate factors cancel:

\[
\phi_2(\pm r\hat z)=\pm\frac{L(GM_b/\mu_e)^2}{g_e r^3}.
\]

This fixes \(\mathcal N=L\) regardless of the full interpolation function.
The isolated flux law gives \((1+L)(1-2\beta)=2\), yielding the first result.

For QUMOND, put \(k_\nu=d\ln\nu/d\ln n_e\), with \(n_e\) the Newtonian
external acceleration and \(g_e=\nu_e n_e\). Its quadratic Poisson source
has the opposite inversion sign and is driven by the Newtonian monopole.
The analogous axial coefficient is \(\mathcal N=-k_\nu\). Matching the
isolated spherical laws gives \((1+L)(1+k_\nu)=1\), yielding the second result.
The complete derivation, multipole qualification and induced-dipole calculation
are in [PROOF.md](PROOF.md).

| Isolated exterior slope | AQUAL nonlinear coefficient | QUMOND nonlinear coefficient |
| --- | ---: | ---: |
| -1/2, Newtonian limit | 0 | 0 |
| -1/4 | 1/3 | 1/4 |
| 0, deep-MOND limit | 1 | 1/2 |

## Checks and boundaries

- `verify.py`: 46 exact symbolic identities; full nonlinear-operator residuals
  for 12 AQUAL and 9 QUMOND background/kernel cases. The residual falls as
  approximately \(r^{-7}\) after adding the correction, versus \(r^{-5}\)
  for the leading potential alone.
- An independent second-order radial Green calculation integrates the actual
  source interior for three compact ellipsoidal profiles and four response
  derivative pairs, with three extraction radii: 36 cases. The three-radius
  coefficient agrees to about \(3\times10^{-14}\). The raw estimator can
  have the wrong sign; it is not used as evidence for the filtered law.
- `verify_global_qumond.py`: nonlinear deep-QUMOND source evaluated without
  Taylor expansion, followed by a finite-mode Green solve for four compact
  spherical source models, three angular/radial resolutions and four radii.
  All 48 cases pass; at the largest extraction radius the maximum coefficient
  error is \(1.73\times10^{-7}\). Results and convergence checks are in
  `certified/global_qumond.json`.
- `TailAlgebra.lean`: eight conditional algebraic theorems, including the radial
  filters, orbital elimination and deep-limit separation. The PDE and general
  existence of its asymptotic expansion are **not formalized** by this file.
- Commands, input hashes and outputs are pinned in `certified/manifest.json`.
  See [REVIEW.md](REVIEW.md) for the self-audit and [LITERATURE.md](LITERATURE.md)
  for the bounded overlap search and attribution.

Regenerate the calculations and Lean check from the repository root into a
separate output directory:

```bash
python3 real_research/reviews/nonlinear_external_field_tail_2026_09_21/verify_all.py /tmp/nonlinear-external-field-check
```

The bundled mathbox `computation-audit/scripts/run_experiment.py` generated the
certified provenance record; its complete argv, software versions, base Git
revision and dirty state are stored in that record. The manifest pins the Python
scripts, Lean file, toolchain and Lake dependency manifest. It does not hash
every installed Python library or compiled Mathlib object.

The local equation \(\nabla\cdot[\mu(|\nabla\Phi|)\nabla\Phi]=4\pi G\rho_b\)
is a physical hypothesis. Nonlocal completions, extra fields, external tides,
noncircular motion and finite observation radii require their own calculation.
The isolated orbital reference must be spherical and outside its baryonic
source, with ordinary test-body inertia and the same response at the same
physical acceleration. No projected velocity statistic, lensing prediction,
kappa selection, or cosmological completion is established here.

The strongest next step is a nonlinear AQUAL boundary-value calculation with
controlled outer-boundary, angular and radial errors, extracting this coefficient
for multiple source shapes. The present full nonlinear Green check is QUMOND;
the global AQUAL source checks stop at second order.
