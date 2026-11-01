# Entropy memory stress candidate for X48

The strongest construction found here is a density-gated entropy polytrope
with energy-conserving collapse heating. It has an exact stress-free material
domain, positive active acoustic stiffness, and finite spherical core branches
with a positive radial stability gap. Its cores resist a defined smooth
baryonic loading more strongly than a circular-shell dust reference.

**The finite cold-collapse experiment now settles with conserving entropy
transport.** The [2026-11-01 transport phase](entropy_transport/README.md)
adds an outward hot-to-cold flux gated by adverse entropy ordering and
work-conserving bulk damping. One fixed coefficient set forms quiet spherical
cores at 32--256 shells through t32, with positive post-warming central
entropy approaching an independent mass/energy-selected regular endpoint.
Radial size and entropy perturbations relax through t64 at N64.

A mesh-uniform dynamical floor, global transport stability, cosmological halo
formation and observed forest viability remain open. Exact quiet-domain tests
are conditional on the material activation gate. The new transport is an
experimental alternative under X48, not a replacement for frozen production
dynamics. The original heating/bounce pilot and constructed parcel endpoints
below remain distinct historical evidence.

## Proposed stress and memory

Let rho be the positive inertial density of the clustered cold component.
The new material parameters are a fixed physical density `rho_q` and a
compression time `tau`. With `d=rho/rho_q` and history variable `chi>=0`,

\[
 \boxed{P=P_0\chi d^2h(d),\qquad P_0=\frac{a_0^2}{8\pi G}},
\]
\[
 h(d)=\begin{cases}
 0&d\le1,\\
 3(d-1)^2-2(d-1)^3&1<d<2,\\
 1&d\ge2.
 \end{cases}
\]

Set `K=chi P0/rho_q^2`. The energy is `e=K W(rho)`, where `W'=h`, `W=rho`
above `2rho_q`, and `W=3rho_q/2` below `rho_q`; the joining polynomial is in
[DERIVATION.md](DERIVATION.md). Retaining this dormant energy is what makes
stress-free expansion compatible with memory and conservation.

For `C=max(-div v,0)`,

\[
 D_t\chi=h(d)C(\tau C-1)_+,\qquad
 q=P_0\frac{\rho W}{\rho_q^2}h(d)(\tau C-1)_+ .
\]

Use the same total isotropic stress `(P+q)I` in momentum. The identity
`rho W D_tK=qC` supplies all heating from mechanical work. When compression
subsides, chi is advected. Equal rho with different chi gives different
pressure, so this is nonbarotropic.

For every history, `rho<=rho_q` gives exactly `P=q=D_tchi=0`. Initially
unheated material also stays stress-free while `tau C<=1`, including the
expanding background and sufficiently small perturbations. These are exact
conditions. Placing the observed Lyman-alpha forest inside those conditions
requires a density/history test; it has not been inferred from a name or a
linearization. Neither rho_q nor tau is fitted here.

## Stable finite core branches

For fixed K the sound speed is nonnegative:

\[
 c_s^2=K(2\rho h+\rho^2h'_\rho)\ge0.
\]

The active entropy-volume energy is convex. Smooth spherical baryons of finite
central density admit finite regular cold centers and a finite pressure-free
surface at rho_q. For admissible adiabatic radial modes, with fixed baryons
and the physical free-traction boundary condition,

\[
 \omega^2\ge\frac{8\pi G\rho_q}{3}>0.
\]

This is a radial stability theorem for the stated isolated-core model.
Convective stability additionally requires nondecreasing K outward; constant
K is neutrally buoyant. It is not a global nonlinear or nonradial interface
theorem. Exact inactivity leaves a cold dust phase whose multistream/kinetic
completion is separate.

The dense core has `P=K rho^2` and characteristic scale

\[
 R_1=\frac{a_0}{4G\rho_q}\sqrt{\chi}.
\]

Thus a0 normalizes the material stress; rho_q and generated history determine
core size. No fixed pressure ceiling or universal surface density is imposed.

## Quantified baryon resistance

The current [static evidence](static_verification_inner_shells/results.json)
contains eight smooth Plummer-loading cases: initial central densities
`5rho_q` and `20rho_q`, baryon mass fractions 0.1 and 0.3, and baryon scales
0.1 and 0.3 times the initial radius. Cold mass and K remain fixed.

| Enclosed cold mass | Retained radius with stress | Retained radius in dust reference |
|---|---:|---:|
| 1% | 0.643--0.910 | 0.289--0.717 |
| 5% | 0.686--0.916 | 0.332--0.751 |
| 10% | 0.711--0.919 | 0.381--0.779 |
| 50% | 0.775--0.934 | 0.642--0.880 |

These are ranges across the declared grid; all 32 paired comparisons favor
weaker contraction with stress. Central densities still rise and cores still
shrink. The comparator preserves `r[m_shell+Mb(r)]` for circular shells, not
every collisionless orbit. Only one case received the tighter ODE solve; its
reported profile scales changed by at most `1.35e-7` relatively.

An arbitrarily compact point baryon instead forces a `1/r` cold cusp. A
rotating baryonic disc, responsive baryons, a diffuse halo envelope and the
cosmological Lambda background are not covered by these static tests.

## Earlier formation pilot and constructed endpoint

The preserved [Radau formation snapshots](formation_radau_snapshot/n64_tau05/result.json)
start with K=0 and rho=0.25rho_q. The 64-shell pilot reaches t=8; the
128-shell pilot is resource-limited at t=3.8634. Their peak sampled 5%-mass
mean densities are approximately 2.398rho_q, and accepted energy errors are
below 1.8e-9. A tighter time solve agrees closely on its observed interval.

The remnant remains moving and has adverse entropy ordering. These results
support finite-time radial heating and bounce, not stable halo formation or
a continuum density cap.

The subsequent [exact-parcel endpoint](ENTROPY_ENDPOINT.md) sorts the measured
equal-mass parcel entropies and increases every coefficient by the same
energy-selected factor, approximately 1.41932. It preserves the sorted
histogram before heating and requires no parcel to lose entropy. The
constructed sphere has finite central density, positive radial stiffness,
and restoring density jumps at all 63 entropy contacts. Its energy matches
the recorded N64 initial energy within the declared numerical acceptance;
that initial energy itself differs from its continuum value by about 0.023%.

Keeping that same entropy profile under Plummer loading `Mb=0.3Mc`,
`b=0.1R` retains 0.667 of the inner 5%-mass radius and 0.817 of the half-mass
radius, versus 0.440 and 0.644 in the circular reference. Central density rises
from approximately 48.3rho_q to 199.8rho_q. These are finite constructed
states, not evolved disc or relaxation results. Their positive minimum K is
measured at N64; no resolution-independent lower entropy bound or converged
central core radius has been established.

[ROUTES.md](ROUTES.md) preserves the failed and deferred
routes; [PROVENANCE.md](PROVENANCE.md) identifies current evidence and old
source snapshots.

Run the scoped tests from the repository root:

```bash
python3 -m unittest discover -s rebuild_2026_10_22/X48_native_cf_zoom/stable_stress_search -p 'test_*.py' -v
```

The current implementation is in [material.py](material.py), static solver in
[equilibria.py](equilibria.py), and formation pilot in [collapse.py](collapse.py).
The endpoint constructor is [entropy_endpoint.py](entropy_endpoint.py), whose
CLI defaults to exact parcels; the historical Python API defaults to its
explicitly labeled linear proxy.
The exact equations, proofs, primary-source comparisons and limitations are in
[DERIVATION.md](DERIVATION.md). No novelty or observational validation is
claimed. Kappa=1/2 remains fitted; this is not theory closed.

[STATUS.md](STATUS.md) is the live handoff. The current phase synthesis is
[entropy_transport/CHECKPOINT_2026_11_01.md](entropy_transport/CHECKPOINT_2026_11_01.md);
[CHECKPOINT_2026_10_31.md](CHECKPOINT_2026_10_31.md) records the earlier phase.
