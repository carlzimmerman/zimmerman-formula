# Protected gauge route: authenticated primary sources

2026-10-20. Read-only web authentication; no PDFs downloaded, scripts,
numerical scans or compilations. Versioned primary text or an unversioned
primary PDF with its explicit arXiv version header was inspected. Formulas
in `PROTECTED_GAUGE.md` not attributed below are direct analytic diagnostics,
not results claimed by these sources.

## G1. Seiberg: the protected scalar polynomial and its components

N. Seiberg, *Five Dimensional SUSY Field Theories, Non-trivial Fixed Points
and String Dynamics*, hep-th/9608111v2, 3 Sep 1996.

- Metadata: https://arxiv.org/abs/hep-th/9608111
- Exact primary PDF: https://arxiv.org/pdf/hep-th/9608111v2
- Exact primary HTML: https://arxiv.org/html/hep-th/9608111v2
- PDF header explicitly identifies v2 and 3 Sep 1996. The PDF equation
  numbers are authoritative here; the HTML rendering repeats incorrect
  equation labels in places.
- Eqs(2.1)--(2.3): at most cubic prepotential; one-field
  A^2/(2g^2)+cA^3/6; component scalar/gauge kinetic and CS interactions.
- Eqs(2.4)--(2.6): dual coordinate and BPS electric/string quantities.
  Their normalization is not imported into a universal gravitational
  source coupling in our report.
- Section3, Eqs(3.2)--(3.5): piecewise-Coulomb response and charged
  thresholds. This is a low-energy Coulomb description, not the full
  finite-field interacting theory at a massless wall.

## G2. Intriligator--Morrison--Seiberg: exactness and charge hypotheses

K. Intriligator, D.R. Morrison and N. Seiberg, *Five-Dimensional
Supersymmetric Gauge Theories and Degenerations of Calabi-Yau Spaces*,
hep-th/9702198v2, 5 Mar 1997.

- Metadata: https://arxiv.org/abs/hep-th/9702198
- Primary PDF opened: https://arxiv.org/pdf/hep-th/9702198
- The inspected PDF header explicitly says hep-th/9702198v2, 5 Mar 1997.
  A versioned HTML request was unavailable; no claim is based on it.
- Section2.1, Eqs(2.1)--(2.5): prepotential, its Hessian as the Coulomb
  metric/gauge-coupling matrix, and c_ijk A^i wedge F^j wedge F^k/(24pi^2).
- The paper explicitly notes that its cubic coefficient differs by a
  factor of two from the convention used in cited earlier work, including
  Seiberg. No numerical c is silently shared between G1, G2 and G3.
- For a single U(1), Eq(2.6) and adjoining text distinguish c in 6Z for
  a generic five-manifold from c in Z for the restricted geometries at
  issue in the M-theory construction. Eq(2.8)'s integral basis and
  Eqs(2.9)--(2.10)'s charged-matter half-level shifts retain their stated
  hypotheses. We do not assert a universal bare integer on every manifold.
- Section2.3, Eq(2.22): exact locally piecewise-cubic Coulomb prepotential,
  with classical quadratic/cubic data and vector/hypermultiplet terms.
- Section3: positivity/convexity of the Coulomb metric is a necessary
  discriminator for candidate fixed points, not by itself a complete
  microscopic health theorem.

## G3. Dudas--Gherghetta--Groot Nibbelink: off-shell component action

E. Dudas, T. Gherghetta and S. Groot Nibbelink, *Vector/tensor duality in
the five dimensional supersymmetric Green-Schwarz mechanism*,
hep-th/0404094v2, 22 Jul 2004.

- Metadata: https://arxiv.org/abs/hep-th/0404094
- Exact primary HTML: https://arxiv.org/html/hep-th/0404094v2
- Section3.1, Eqs(37)--(42): real scalar, vector and auxiliary component
  definitions; free bosonic action with Y=D+partial5 sigma.
- Eq(43): real quadratic/cubic prepotential. Eq(44): superspace action.
  **Eq(45)**: general bosonic component action, including P_ab times
  -F^2/4-(partial sigma)^2/2+Y^2/2+Fauxbar Faux, and the CS component
  term P_abc epsilon AFF/24. This is the coefficient authority for the
  explicit convention in our report. Calling the component formula
  Eq(44) would be an off-by-one citation error.
- Section5, Eqs(113)--(116): brane-localized FI sources, auxiliary
  equations and compensating scalar/brane expectation values. These
  equations do not select the FI magnitude or assert the UV completion
  of an arbitrary bulk FI deformation of a non-Abelian fixed point.
- Our algebraic addition of kappa sigma^3, four-dimensional N=1 W=yZ^3/3,
  and the combined cubic+FI crossover are explicit diagnostics. They are
  not potentials claimed to follow from G3's protected prepotential.

## G4. Gauntlett et al.: gravitational normalization without electric cubic

J.P. Gauntlett, J.B. Gutowski, C.M. Hull, S. Pakis and H.S. Reall,
*All supersymmetric solutions of minimal supergravity in five dimensions*,
hep-th/0209114v3, 2 Sep 2003.

- Primary PDF opened: https://arxiv.org/pdf/hep-th/0209114
- The inspected PDF header explicitly identifies v3 and 2 Sep 2003;
  a separate document-generation date on its title page is not treated
  as the arXiv version date.
- Section2, Eq(2.1), in the paper's signature/curvature conventions:

      S=(1/(4pi G5)) integral[-R star1/4-F wedge star F/2
                              -2 F wedge F wedge A/(3sqrt(3))].

- Eq(2.2): Einstein equation and d star F+2 F wedge F/sqrt(3)=0.
  Our report uses this exact Maxwell equation, rather than silently
  translating the source's R convention into a new action normalization.
- This is the minimal **ungauged** theory. It supplies a fixed relative
  gravitational/gauge/CS coefficient, a Maxwell pure-electric sector,
  and a Ricci-flat zero-field vacuum. It does not establish a statement
  about all gauged theories or a positive-vacuum normalization theorem.
- The source's supersymmetric source qualification is not a universal
  matter-sector postulate. We do not use BPS charge/mass relations to
  identify all inertial masses with a same-sign gauge charge.

## Internal overlap and formal scope

- `../current_interactions/RESULT.md`: distinguish the previously tested
  2+1-dimensional CS-Higgs magnetic-current response from five-dimensional
  pure electric CS, and from the independent neutral Jacobian-current toy.
- `../protected_auxiliaries/RESULT.md`: ordinary healthy vector auxiliary
  Hessians and FI/BI analytic response are prior results; no new universal
  auxiliary-ghost theorem is asserted here.
- `../current_interactions/CurrentEnergy.lean`: charged_energy,
  charged_gap_factorization, charged_global_lower_bound and
  charged_equality_iff already contain the fixed-D rational-polynomial
  minimization used here after the substitutions recorded in the report.
  This source was read without compiling or changing it. These lemmas do
  not certify supersymmetry, UV completeness, force signs, gradient
  elimination or the operational ratio.
