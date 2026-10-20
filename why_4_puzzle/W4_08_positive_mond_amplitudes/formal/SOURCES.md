# Sources and explicit leaves for the continuation

2026-10-20. No source downloads. The new canonical, cone, radial-source and
scale/gap calculations are direct derivations, with independent raw-proof
review. The primary sources below support only the bounded claims named.

- Z. Sun, D. N. Basov and M. M. Fogler, *Third-order optical conductivity
  of an electron fluid*, Phys. Rev. B 97, 075432 (2018),
  [accepted manuscript](https://link.aps.org/accepted/10.1103/PhysRevB.97.075432),
  Appendix A. Its massless Dirac thermodynamics agrees with the direct
  free-particle pressure integral used in the continuation; g=4 gives
  P(mu)=mu^3/(3pi v^2) at zero temperature. It does not realize our source
  coupling or normalize a gravitational vacuum.
- B. Wunsch, T. Stauber, F. Sols and F. Guinea,
  *Dynamical polarization of graphene at finite doping*,
  [cond-mat/0610630v2](https://arxiv.org/html/cond-mat/0610630v2),
  2007-01-09, Eqs. 3 and 8-13. It gives frequency/momentum dependent
  finite-density polarization; the static pressure is insufficient to
  specify a local microscopic dynamical parent. The HTML rendering's
  generated date is not used as the paper's revision date.
- S. Coleman and E. Weinberg, *Radiative Corrections as the Origin of
  Spontaneous Symmetry Breaking*, Phys. Rev. D 7, 1888 (1973),
  [original paper](https://www2.physik.uni-muenchen.de/lehre/vorlesungen/wise_21_22/Neutrino-Mass-and-Grand-Unification/Material/Coleman_Weinberg.pdf),
  sections IV-V, primary historical background. The precise common-scale,
  coupled-gap Hessian and Schur bound here were differentiated directly;
  they are not quoted as a theorem of that source. The existing local
  single-field dilaton report is acknowledged in MICROSCOPIC_CONTINUATION.

Formal external leaves are the installed Lean/mathlib definitions and
ordered-field/calculus support, pinned by lean-toolchain, lake-manifest
and direct source/object hashes in the bounded run records. The Lean
source imports only the needed public library interface and meta tactics.
Lean 4.34's legacy file mode loads private transitive declarations/IR;
adding the documented `module` header resolved that avoidable memory
failure. The real-pi adapter still exceeds the light-job memory cap.

The physical pressure/stress and source-to-coefficient dictionaries are
specified mathematical inputs. They are not secretly replaced by a
formal axiom asserting the desired amplitude. No formal pi-transcendence
result has been added or assumed. The analytical original W4-08 source
list remains in ../SOURCES.md.

The charged sextic continuation additionally uses these primary sources:

- S. Kvedaraite, T. Steudtner and M. Uetrecht,
  *Revisiting the phi6 Theory in Three Dimensions at Large N*,
  [arXiv:2502.07880v2](https://arxiv.org/html/2502.07880v2), 2025-09-01,
  Eqs. 1, 20-22, 39, 76-81 and 91-95. Supplies coupling normalization,
  the leading-N potential and finite-1/N qualifications. The charged
  O(2) minimization in REGULAR_PRESSURE_PARENT is our conditional
  application; the paper does not establish the full real-time MOND bridge.
- W. A. Bardeen, M. Moshe and M. Bander,
  [Fermilab-Pub-83/53-THY](https://lss.fnal.gov/archive/1983/pub/Pub-83-053-T.pdf),
  June 1983. Its leading-N stress-tensor discussion supports exact
  tracelessness in that limit. Read with the modern source; no old claim
  about a physical finite-N BMB fixed point is adopted here.

The timelike tree scalar, amplitude spectra, Gauss-law envelope obstruction
and charged leading-N application were derived directly and independently
checked. Regularity and vacuum conclusions retain their stated classical,
state-dependent or leading-N qualifications.
