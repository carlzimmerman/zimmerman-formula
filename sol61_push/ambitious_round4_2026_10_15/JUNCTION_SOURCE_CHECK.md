# Junction convention check

Checked 15 October 2026. Source question: the sign, normal orientation and
surface-energy normalization of the two timelike wall junctions used in
`einstein/PROOF.md`. No novelty claim is made.

[W. Israel, Singular hypersurfaces and thin shells in general relativity,
Nuovo Cimento B 44, 1–14 (1966)](https://doi.org/10.1007/BF02710419) is
identified by the publisher. Its primary scanned text was read at
[the public paper copy](https://images.shoutwiki.com/gamebm/0/02/Israel1966_Article_SingularHypersurfacesAndThinSh.pdf),
section 2 equations (7)–(8), section 3's minus-to-plus normal, and section 5
equations (19)–(20). They give the stated extrinsic-curvature jump sign after
translating its coupling to 8piG/c^4. This checks the convention, not the new
body's existence or stability. Publisher access provided metadata only.
The erratum's metadata was located, but its text was not authenticated here.
No full paper was retained or redistributed.

The application to bounded nonvacuum bulk matter also has a direct local
derivation. In Gaussian normal coordinates at a timelike wall, write
`ds²=dell²+gamma_ij dx^i dx^j` and `K_ij=(1/2)partial_ell gamma_ij`, with
ell increasing from inside to outside. The singular Einstein tensor is

    G_ij,sing = -([K_ij]-gamma_ij[K]) delta(ell).

Bounded bulk stresses add no delta term. Equating this coefficient to
`(8piG/c^4) S_ij delta(ell)` gives

    [K_ij] = -(8piG/c^4)(S_ij-gamma_ij S/2).

For the actual area wall, `S^i_j=-sigma delta^i_j`, this is
`[K^i_j]=-4piG sigma/c^4 delta^i_j`. With one common outward normal,
`K^theta_theta=sqrt(F)/R` and `K^tau_tau=sqrt(F)nu'`. These yield both
equations (15) of the Einstein proof, without assuming vacuum bulk on the
interior side or importing the vacuum normal-pressure constraint.

The root independently eliminated these two jumps and recovered both the
redshifted wall/Maxwell-tail ADM mass and the quadratic traction equation.
The source comparison and this derivation support those conventions only;
the branch's actual source and contraction are separate proof obligations.
