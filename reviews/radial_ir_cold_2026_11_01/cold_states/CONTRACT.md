# TP04 cold microscopic states: frozen bounded contract

1 November 2026. Authorized subroute of the parent TP04 contract. Write only
this directory; TP01--TP03 and sibling inputs remain immutable. Starting
revision 27a0d27db1c343e1752698da36aa300398214689 is historical; hash actual
inputs before and after every load-bearing run. No Git mutation.

Action: canonical-K rigid SU(5), W=fX+h X Tr(A²)/2+lambda Tr(A²B)/2,
the specified commuting valley, h=lambda=e and g=sqrt(29/200)e. Use f=1;
restore mu=sqrt(f) in masses and widths. Fixed weak trial couplings .01,.03
for full tree vertices and .003 for the conditional neutral photino state.
The matched radial metric/curvature is the sibling radial result, not a
tree-mass surrogate. Photino pole thresholds are the sibling finite-F
one-loop calculation. No scale, vacuum offset, population or production is
selected by this computation.

Bounded assertions to test:

* Project the exact Goldstino and unbroken-gaugino null space in the full
  Takagi basis; sum fermion-to-lighter-scalar widths from actual rotated
  vertices. Separate physical flat scalars from gauge Goldstones.
* Test the light SU3 scalar's tree channels into physical zero modes. A
  tree zero does not establish radiative stability or a gauge-invariant
  asymptotic particle in a nonabelian confining sector.
* Test the unitary transpose C involution on action tensors, scalar and
  fermion Hessians. This establishes a perturbative selection rule around
  its invariant vacuum, not an independently authenticated discrete-anomaly
  classification of a completed gravitational theory.
* Evaluate the U1 photino mass slope by repeated symmetric stencils and
  its radial source feedback for the stated nonrelativistic benchmark.
* Use the primary-source Goldstino low-energy theorem to compute the
  photino-photon-Goldstino partial width and radial-Goldstino partial width.
  Do not silently identify partial and total lifetimes. Record all lower
  dimension allowed channels, thresholds and the remaining dimension-seven
  transition coefficient as an explicit matching dependency if no actual
  bound is proved. No guessed Wilson coefficient is a total-width proof.

Numerical tolerances: action symmetries and projection identities relative
1e-9; mass/width e scaling 1e-7; slope convergence 1e-5. No negative masses
clipped beyond frozen builder's recorded relative zero convention. One
numerical thread, wall 180s, CPU 175s, measured RSS below 1GB. macOS memory
and affinity enforcement are not claimed. No installs/downloads, production
simulation, finite-temperature rate or nonperturbative prefactor inference.
Failures remain archived. Source equations and finite-momentum limitations
are documented in DERIVATION.md; reproducibility uses a v2 runner manifest.
