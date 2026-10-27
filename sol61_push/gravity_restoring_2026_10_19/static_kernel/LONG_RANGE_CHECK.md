# A bounded check of apparent long-range loopholes

Checked 19 October 2026. Question: can known condensate-mediated forces or
phonon loops supply the **positive material inverse-density kernel**
`+4piG/k²` missing in this particle model? This is a source/application
check, not a literature-wide exclusion or novelty search.

The two exact identifiers below had no hit in the project literature cache.
The PDFs/HTML were read online; no full text was retained and no source-byte
hash is asserted. Initial search/HTML discovery preceded the exact cache
lookups. The cache itself was not modified.

## 1. An actual condensate can mediate a long-range force

Berezhiani and Khoury, *Emergent long-range interactions in Bose-Einstein
Condensates*, [arXiv:1812.09332v1](https://arxiv.org/abs/1812.09332v1),
21 December 2018. The official unversioned PDF returned a printed v1 header;
the abstract's version history independently identifies v1. The attempted
v3 URL was unavailable and was not used. Checked printed pp. 2–4,
equations (1), (7)–(11), (14)–(25), including the force sign discussion.
The source introduces an extra modulus–source contact, finds a Yukawa force
whose range diverges as self-interaction vanishes, and treats nonlinear
source screening. This verifies the counterexample to “a massive elementary
scalar cannot mediate a long-range force in a condensate.” It does not
identify that induced attraction with a positive material density stiffness.
Its source contact must also be matched to the present theory rather than
borrowed as a new coupling. General effect: known after notation translation.

## 2. A phonon-loop Coulomb term also exists, with qualifications

Fujii, Hongo and Enss, *Universal van der Waals Force Between Heavy Polarons
in Superfluids*, [arXiv:2206.01048v3](https://arxiv.org/html/2206.01048v3),
30 November 2022, PRL129,233401. Checked official version history and full
equations (1)–(16), not only the abstract. For weak contact impurities in a
Galilean superfluid their zero-temperature tail is attractive `r^-7`.
Equation (12) has a negative `T^6/k²` thermal correction only for
`T<<cs|k|`, below the hydrodynamic cutoff; equation (15) gives a different
`-T|k|³` regime at smaller momentum. Thus this is neither a positive
restoring Coulomb kernel nor its infrared continuation. Applying coefficients
to the present particles would require the medium, impurity and source
matching. The scoped force result is verified; the target application is
inapplicable under that sign/operator identification. No all-loop claim.

## 3. Internal source-to-kernel dictionary

The following argument is a direct Gaussian/variational calculation in our
declared convention, not an imported force coefficient. Let an external
number source `J` couple through `eta J delta n` to a stable NR condensate.
Its quadratic static density energy is

\[
 E=\frac12\int_k\left(g_2+\frac{k^2}{4mn_0}\right)
       |\delta n_k|^2+\eta\int_k J_{-k}\delta n_k.
\]

Minimization gives

\[
 \delta n_k=-\eta\chi_n(k)J_k,\quad
 \chi_n=\left(g_2+\frac{k^2}{4mn_0}\right)^{-1},\quad
 E_{\rm ind}[J]=-\frac{\eta^2}{2}\int_k\chi_n(k)|J_k|^2.
 \tag{A}
\]

If `g2` tends to zero on a controlled condensate state, `chi_n` approaches
`4mn0/k²`. A long-range *induced attraction* then appears for like sources.
The material inverse kernel is instead `h_n=1/chi_n`, which approaches
`k²/(4mn0)`. These are different functionals of different variables; their
opposite signs/inverse powers must not be interchanged. With `g2>0` the
range is set by `kappa²=4mn0 g2`, not by the heavy dynamical amplitude gap.
This is consistent with the full phase–density response in the sibling
lane and with the literature check.

Likewise, integrating any stable static real Gaussian mediator coupled
linearly to a real source gives a negative semidefinite induced quadratic
form `-J K^-1 J/2`. That fact does not preclude repulsive *bare* contact
energy, interactions between oppositely signed sources, position-space
oscillations, or a Gauss-law vector field. It does prevent replacing the
same-source induced term by the required positive long-range material
energy without supplying another physical mechanism.

These checks leave quantum/thermal nonlocal kernels open in general, while
removing two specific apparent shortcuts. Neither cited work proves the
original microscopic rational law, critical normalization or vacuum scale.
