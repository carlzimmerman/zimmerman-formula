# FSP-005 boundary route result

For the actual relative gauge wall on B_R^3 x S_L^1, the fixed charged
Matsubara-pair determinant has the verified local term

    Gamma_n|inverse = +16/(315 |2 pi n/L+v| R).

The corresponding mixed heat coefficient is A_4=-128 pi/(315R), in the
normalization K(t)~(4pi t)^(-3/2) sum A_k t^(k/2). Tangential Dirichlet
rank is three, normal Robin rank is one, S=-2P_normal/R for the inward
source normal. The moving-projector terms are essential. Exact TE/TM
spectral decomposition provides an independent specialization check.

This is a boundary-domain calculation for constant gapped holonomy. The
full frequency sum needs a common four-dimensional regulator and a cubic
extrinsic-curvature surface counterterm; its absolute finite coefficient
is scheme dependent until surface matching is fixed. It is not a complete
monopole determinant or a physical vacuum-stress result.

The profile h=v-1/r changes the same inverse-radius order. The hand
scalar-potential response finds both the expansion of the lower wall
logarithm and a K*partial_in m/m wall term. Furthermore, keeping common
PV fields through the frequency sum gives a finite contribution
+4L/(3pi R) from the lower wall term -8R mu/3. At center holonomy the
odd mass-jet sum vanishes. These additional profile statements are exposed
for fresh review in `ADDENDUM_COMMON_PV_PROFILE.md`; they are not evidence
that the bulk and core contributions have been matched.

Evidence:

* `INDEPENDENT_DERIVATION.md`: exact hand mixed-projector and TE/TM derivation;
* `SOURCE_RECORDS.json`: primary source versions, exact locators, hypotheses,
  normal/sign translation, and temporary-source SHA-256 hashes;
* `EXACT_CONTRACT.json`, `check_exact.py`, `runs/exact-001/manifest.json`:
  precontracted bounded exact arithmetic, completed and validated v2 evidence;
* `ADDENDUM_COMMON_PV_PROFILE.md`: explicitly later comparison and regulator
  correction, with prior source/input hashes;
* `REPRODUCE.md`: provenance and reproduction limits.

Strongest safe outcome: the actual moving relative wall has a nonzero
constant-mass inverse-radius benchmark, correcting the missing-domain
ambiguity. Smallest remaining obligation: independently audit the profile
mass-jet and common-PV terms, then match the spectral wall sector with the
bulk derivative representative, finite surface scheme, and monopole core.
No alpha selector or electromagnetic bridge has been produced.
