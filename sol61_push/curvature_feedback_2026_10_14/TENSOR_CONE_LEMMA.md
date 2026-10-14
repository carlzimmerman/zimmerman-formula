# Tensor cone obstruction to activation from rest

Consider Einstein gravity with constant positive reduced Planck mass M_P,
a scalar coupling +F(φ)𝒢, and matter minimally coupled to the metric. On a
flat homogeneous background, define the tensor coefficients without the
irrelevant overall polarization normalization:

\[
Q_T=M_P^2+8H\dot F,\qquad
\mathcal F_T=M_P^2+8\ddot F,\qquad
c_T^2=\mathcal F_T/Q_T.
\]

These follow from the known quadratic action: [Kobayashi, Yamaguchi and
Yokoyama, 1105.5723v3, Appendix A, Eq. 92](https://arxiv.org/html/1105.5723v3).
Here their ξ is our F. This lemma is a formal corollary of that result; no
novelty is claimed.

**Claim.** Suppose a(t) > 0 is continuously differentiable, F(t) is twice
continuously differentiable, Q_T > 0, and c_T² ≤ 1 throughout an interval
starting at t₀. If Ḟ(t₀) = 0, then Ḟ(t) ≤ 0 throughout that interval.
Consequently, a path with Ḟ(t) > 0 at some later time cannot satisfy all these
conditions. A healthy tensor gradient additionally requires c_T² > 0.

**Proof.** Positivity of Q_T permits multiplication of the speed inequality:

\[
c_T^2\le1\quad\Longrightarrow\quad\ddot F-H\dot F\le0.
\]

Since H = ȧ/a,

\[
\frac{d}{dt}\left(\frac{\dot F}{a}\right)
=\frac{\ddot F-H\dot F}{a}\le0.
\]

The left-hand quantity starts at zero, so it cannot become positive. Multiplying
by a > 0 proves Ḟ ≤ 0. This argument does not require a particular potential,
scalar kinetic function, reheating rate, or sign of Ḣ.

For the quadratic coupling, growing |φ| gives Ḟ = ηφφ̇ > 0 when η > 0.
The saturating coupling also increases with |φ| at every finite |φ|. Activation
of these fields from φ̇ = 0 therefore violates the strict tensor upper-cone
condition somewhere, unless another hypothesis fails. A tiny excess above one
still violates that exact mathematical condition, although it need not produce
a detectable observational effect.

This is not a proof of closed timelike curves, an observed exclusion, or a
universal objection to gravitational production. An EFT characteristic speed
and the ultraviolet front velocity are different questions. Additional
derivative operators can change the tensor coefficients; alternative initial
data, a decreasing coupling, or a different gravity/matter sector change the
problem. Requiring all propagation cones to lie inside the matter cone is
stronger than merely avoiding ghosts and gradient instabilities.

Self-audit: no division by φ̇, no scalar unitary gauge, no inflaton perfect-fluid
approximation, and no omitted endpoint assumption enters this proof. It applies
to the original tensor sector even where the separate scalar diagnostic needs
a fuller matter perturbation action.
