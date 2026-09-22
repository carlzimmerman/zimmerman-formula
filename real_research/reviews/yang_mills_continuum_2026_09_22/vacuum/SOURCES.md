# Source checks, 2026-09-22

The repository literature-cache lookup for `Bakry` returned no cache.
Only primary-source PDF text was inspected; no PDF was retained because
the route write permission is confined to this directory and the standard
project cache is outside it. The proofs in PROOF.md are derived locally;
the sources below cross-check the exact geometric and radial formulas.
No novelty claim or broad literature coverage is asserted.

1. Dominique Bakry and Michel Emery, *Diffusions hypercontractives*,
   Seminaire de probabilites 19 (1985), 177-206, publisher scan at
   <https://numdam.org/item/SPS_1985__19__177_0.pdf>.
   Page 187, Proposition 3, formulas (4a)-(4b), gives the iterated
   carré-du-champ for L=Delta+grad(h). The dictionary is h=2 log psi,
   hence the curvature tensor is Ric-2 Hess(log psi). The source's
   Gamma normalization is one half of the product-rule defect and
   equals |grad f|^2. The compact spectral-gap implication is proved
   directly in our section 3 rather than imported from a later theorem.
   Authentication and exact formula extraction passed; application is
   valid. The positive-curvature hypothesis fails by our Lemma 2.

2. Irian D'Andrea, Christian W. Bauer, Dorota M. Grabowska, and
   Marat Freytsis, *New basis for Hamiltonian SU(2) simulations*,
   Physical Review D 109, 074501 (2024), DOI 10.1103/PhysRevD.109.074501,
   published PDF at
   <https://scoap3-prod-backend.s3.cern.ch/media/files/84451/10.1103/PhysRevD.109.074501.pdf>.
   Appendix B, pp. 25-26, equations (B1), (B3)-(B5), gives the
   single-plaquette radial equation, sine multiplication, and Dirichlet
   endpoints. Their angle omega=2 theta, x=g^2, a=1 and b=2 reproduce
   our equation (8). Their physical restriction l=0 is our class-function
   sector. Exact radial formula/application checked; the general-b
   small-x convergence in our Lemma 3 is proved locally by min-max and
   compactness, not asserted from their numerical results. Appendix B
   also supplies an optional Mathieu-function cross-check; it is not
   needed for any conclusion here.

Search boundary: exact-primary searches for Bakry–Emery diffusion
curvature and SU(2) single-plaquette Hamiltonian radial/Mathieu reduction.
No source found in this bounded check supplies the missing many-volume
weak-coupling vacuum coercivity estimate.
