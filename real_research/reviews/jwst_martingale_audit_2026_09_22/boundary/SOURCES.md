# Bounded overlap check — 2026-09-22

Question: is the central-source, uniform-sphere Thomson identity
Var(T-Z)=1/3+k^2/10+(2k/5)E[Z]-(1/3)E[Z^2], or its extremum bounds, already
stated in primary radiation-transport or random-flight literature?
Classification: **partial/adjacent results only; novelty remains unverified**.
No assertion of “apparently new” follows from this search.

Read the existing repo source ledger first. Web discovery queries were:
“photon escape time variance sphere Thomson scattering central source second
moment exact”; “radiative transfer sphere path length second moment exit angle
central point source”; “residence time moments sphere scattering”; “mean square
escape time photons sphere”; “random flights exit time moments spherical domain
anisotropic scattering”. Two strategies used astrophysical and random-flight
terminology, but the same reviewer performed both. Coverage was a general web
index plus direct arXiv/publisher primary sources, English, through this date.
No exhaustive ADS/MathSciNet or forward/backward citation graph was completed.

1. Achterberg and Norman, *Relativistic theory of particles in a scattering
flow III: photon transport*, MNRAS 479 (2018), 1783–1799, published 8 June 2018,
[DOI 10.1093/mnras/sty1496](https://academic.oup.com/mnras/article/479/2/1783/5034957).
Publisher full text, Appendix A equations A1–A6 checked. It gives the Thomson
collision operator and angular tensor relaxation. Its sigma_T*n_e is our
scattering rate with c=1; directions are unit vectors. This authenticates
overlap of the angular prerequisite, not our finite-sphere exit-time identity.
The paper's principal application is radiation stress in scattering flows.

2. Zoia, Dumonteil and Mazzolo, *Collision statistics for random flights with
anisotropic scattering and absorption*,
[arXiv:1110.0789v1](https://arxiv.org/pdf/1110.0789v1), 4 October 2011.
Primary PDF version verified from its header; introduction and equations
33–37 inspected. It treats collision-count moments using transport operators
and discusses the established Feynman–Kac approach to residence times.
Their phase-space z is not our scalar exit projection Z. Collision-count
factorial moments are not directly Var(T-Z); no exact translation to our
boundary-observer correction was established. This is strong adjacent prior
art and a reason not to label the general moment method novel.

3. Haichao Xu, *Photon Escape from Slab Thomson Media: A Scattering-order-resolved
Recursive Formalism for Comptonization Applications*,
[arXiv:2606.01087v2](https://arxiv.org/abs/2606.01087v2), 23 July 2026.
Abstract and version metadata checked only. Slab escape and angular recursion
are relevant discovery leads, not verification of the spherical formula.

No source binaries were retained; URLs and inspected locations are recorded.
The proof in README is internally derived and does not rely on importing an
unverified theorem from these papers. Next literature work should examine the
older random-flight residence-time references and sphere moment equations,
explicitly distinguishing T from T-Z and Thomson from isotropic scattering.
