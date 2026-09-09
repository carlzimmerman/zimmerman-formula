# Localized V4 checkpoint

## Result first

The localized action is a constructive prototype, not a complete gravity
theory.  At fixed flat background and nonzero Fourier mode, the explicit
elliptic fields eliminate exactly to the V3 scalar, Hodge, and TT quadratic
forms.  The actual finite-mode Dirac calculation finds one scalar clock mode,
zero transverse-vector modes, and one tensor polarization in the single TT
block; the homogeneous scalar block is analyzed separately.  This is evidence
that localization need not automatically add a propagating auxiliary, but it
does not yet prove the full covariant ten-gate target.

## Explicit action

The prototype uses

\[
S_{\rm loc}=S_{\rm EH}+{1\over16\pi G_b}\int\sqrt{-g}\,{cal L}_{\rm loc}
+S_m[g,\psi_m],
\]

with

\[
\begin{aligned}
{cal L}_{\rm loc}={}&R-2\Lambda-\ell\theta^2+a_0^2f(a/a_0)
 +\eta_UU^2+\eta_XU\chi\\
&+\eta_V(2A^iJ_i-A^i{\cal H}_1A_i)
 +\eta_{TT}(K_{TT}^{ij}K^{TT}_{ij}-2Q^{ij}R^{TT}_{ij}
 +Q^{ij}{\cal H}_{TT}Q_{ij})\\
&+\lambda_\chi(\Delta_h\chi-D_iD_jK^{ij})
 +\lambda_A D_iA^i+\lambda_Q^{ij}(D^kQ_{ki},Q^i{}_i),
\end{aligned}
\]

where (f'(y)/(2y)=2-C(1-e^{-y})), (U=K-\langle K\rangle-\chi),
and the kernels are removed explicitly.  The witness is

\[
C=5/3,\quad \ell=1/100,\quad
(\eta_U,\eta_X,\eta_V,\eta_{TT})=(1/12,1/3,-1/3,-1/6).
\]

The matter action is minimally coupled to (g_{\mu\nu}), so its own Ward
identity remains the ordinary metric one; consistency of the localized
gravitational constraints with that identity is not yet a theorem.

## Derived finite checks

The localizer equations are varied and solved.  For (k^2\ne0),

\[
\chi=S/k^2,\quad A_T=J_T/k^2,\quad Q_{TT}=R_{TT}/k^2,
\]

and substitution gives exactly (-S^2/k^2), (J_T^2/k^2), and
(-R_{TT}^2/k^2), respectively.  The static metric potentials are varied
independently: the Ψ equation is Δ(Ψ−Φ)=0, and matching the harmonic
boundary mode gives

\[
\nabla\cdot[(1-e^{-|\nabla\Phi|/a_0})\nabla\Phi]
 =4\pi G_N\rho,\qquad G_N=2G_b/C.
\]

The six conserved source-polarization response remains the V3 response: 19
uncancelled spatial poles for the unrepaired tensor normalization, zero for
the V3 normalization, and zero failures of the two-wave-factor divisibility
test at the witness.  The weighted cochain metric-variation surrogate agrees
with finite differences to below (6.4\times10^{-8}) on grids 3 and 4; omitting
the inverse or projector variations changes the derivative by (1.5\times10^{-2})
or more.

The new `york_variation_gate.py` extends this to a metric-dependent TT
principal symbol.  For a positive non-Euclidean (h_{ij}) and nonzero covector
(k_i=(1,2,3)), the computed divergence-plus-trace constraint matrix has
derived rank 4 and a two-dimensional TT kernel.  The analytic derivative of
the weighted York projector and of (R_{TT}{\cal H}_{TT}^{\dagger}R_{TT})
agrees with centered finite differences at (3.6\times10^{-10}); projector
idempotence, TT constraint, and weighted self-adjointness residuals are below
(5\times10^{-16}).  This is a principal-symbol check only: connection terms,
spatially varying background derivatives, and full multiplier preservation are
still not computed.

The follow-up `curved_york_variation_gate.py` retains the first spatial jet
of h_{ij}, its Christoffel symbols, the complex WKB divergence-plus-trace
operator, and the complete metric variation of those connection terms.  At
the same nonzero covector its actual constraint matrix has derived rank 4 and
a two-dimensional TT kernel.  The analytic projector derivative agrees with
centered finite differences at (2.0\times10^{-10}), while the TT action
derivative agrees at (2.6\times10^{-11}); idempotence, weighted
self-adjointness, and the constraint residual remain below (5\times10^{-16}).
This closes the previously omitted local connection-variation term at the
tested curved metric jet.  It still does not prove global elliptic boundary
compatibility, lower-order transport, or nonlinear multiplier preservation.

## Requirement audit

| Requirement | Current status |
|---|---|
| exact exponential MOND law | Derived on fixed-​a0 static branch |
| Φ=Ψ and γPPN=1 | Leading static slip equation derived; full PPN open |
| two gravitational tensor modes | Curved WKB TT block verified; full nonlinear count open |
| no hidden auxiliary scalar | Flat localizer block has no extra scalar beyond clock; curved count open |
| matter conservation | Minimal-matter Ward identity; coupled constraint consistency open |
| α₁,α₂,α₃ | Only a restricted α₁ matching exists; full values open |
| cT=c and stability | Flat/curved principal tensor checks; full nonlinear stability open |
| FLRW with H≠0 | Prior V3 background exists; localized perturbations open |
| k=0 and y→0 | Separate k=0 block exists; y→0 strong-coupling/regularity open |
| empirical galaxy/cluster/cosmology fit | Not performed by this checkpoint |
| Lean proof | Lean unavailable; exact identities exported as JSON |

The reproducibility record is `run_008/manifest.json`; it pins the local
modules and the two prior V3 dependency files used by the causal gate.

The follow-up `flrw_ward_gate.py` independently varies the lapse before the
cosmic-time gauge.  It derives

\[
3(2+3\ell)H^2=16\pi G_b\rho+2\Lambda,
\]

shows that all localized fields vanish on an exactly homogeneous isotropic
leaf, and verifies symbolically that the minimally coupled continuity equation
(\dot\rho=-3H(\rho+p)) differentiates the Friedmann residual into the
acceleration residual.  This is a background Ward/FLRW result, not a
perturbation or nonlinear constraint proof.  The latest run is
`run_008/manifest.json`.

## Verdict

**OPEN.** This is a new action-derived constructive branch with a finite
auxiliary-elimination and Dirac checkpoint.  It is not a certified complete
theory.  The next decisive calculation is the full curved York-TT variation
and preservation of all multiplier constraints; if that introduces an
unpaired instantaneous channel or an extra mode, the localized branch fails.
