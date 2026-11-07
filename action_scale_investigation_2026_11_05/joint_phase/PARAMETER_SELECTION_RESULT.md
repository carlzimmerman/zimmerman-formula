# Physical parameter selection: three tests and a conditional Lean certificate

2026-11-07. **No uncalibrated 1/2 has been derived.** The new result is an
explicit continuous freedom that survives phase coexistence and particle mass
matching, plus necessary normalization conditions for two possible additional
closures. This strengthens the diagnosis beyond isolated numerical examples.
The previously sampled stable, roughly flat halos remain conditional examples.

## 1. Coexistence does not fix wall tension

Use the existing canonical scalar with

    V(phi) = V0 + lambda*phi^2*(phi-v)^2/4
             + DeltaV*(3*(phi/v)^2-2*(phi/v)^3),
    m_chi(phi)^2 = m^2 + y^2*phi^2.

For positive s, transform v -> s*v, lambda -> lambda/s^4, y -> y/s,
keeping V0, DeltaV and m fixed. At fixed z=phi/v the entire potential and
particle mass function are unchanged. Bulk vacuum energies, coexistence and
mass gap therefore cannot distinguish these theories. The canonical kinetic
term is kept fixed: these are physically different theories, not a field
relabeling. Scalar curvature masses change by 1/s.

For the degenerate thin-wall profile,

    Sigma = sqrt(lambda/2)*v^3/6,
    Sigma -> s*Sigma; wall thickness -> s*wall thickness.

The squared tension identity and the endpoint invariants are Lean-certified.
The positive square root, wall integral and thin-wall approximation are not
formalized. With small fixed bias, the usual leading thin-wall expression
retains this freedom. Validity restrictions may bound s but do not by themselves
pick a single value. The force balance P+DeltaV=2*Sigma/R therefore still has
a physical scale not fixed by coexistence. Finite-temperature gas corrections
and quantum corrections would require specified couplings and state; they
have not been shown to select a unique value.

The local Newtonian model also uses vacuum contrast, not the common vacuum
offset. A common shift leaves its force unchanged; this is NOT a statement
about full general relativity, where the offset gravitates. It identifies why
this model alone cannot determine an acceleration from absolute rho_DE.

Could marginal stability choose a state? If P scales as R^(-alpha), then

    F = P+DeltaV-2*Sigma/R,
    F' at equilibrium = [DeltaV-(alpha-1)*P]/R.

At marginality, P=DeltaV/(alpha-1) and
R=2*Sigma*(alpha-1)/(alpha*DeltaV), when denominators are nonzero.
Fixed-N adiabatic monatomic gas has alpha=5, giving P=DeltaV/4.
A square root then contains 1/2, but this is a pressure relation, not a MOND
coefficient. Sigma remains free, marginality is not an attracting rule, and
the replenished, radiatively cooled halo is not that adiabatic system. For
DeltaV<0 and alpha>1, positive P cannot satisfy this marginality condition.
The general denominator-cleared marginal pressure implication is certified.

## 2. Conserved charge can constrain inventory, not select its normalization

The current real Z2 scalar has no continuous particle-number Noether charge.
Introducing a charged field would change the model. Conservation gives

    N_chi = Q_total - q_b*N_b

in units of the pool particle's charge. Initial total charge remains an input.
If an additional neutrality mechanism sets Q_total=0, the mass ratio is
eta=M_pool/M_b=-(m_chi/m_b)*q_b. Neither the mass ratio nor the charge ratio
has been selected. With particle/antiparticle pairs, neutrality fixes net
charge rather than total particle mass; asymmetry or annihilation is another
physical requirement. This extends the earlier BARYON_PHASE_RESULT inventory
observation; it is not presented as a new charge-neutrality mechanism.

A useful necessary matching condition follows in a singular-isothermal tail
with negligible core and baryonic gravitational contribution to that tail:

    rho(r)=v^2/(4*pi*G*r^2),  velocity dispersion squared=v^2/2,
    M_pool=v^2*R/G,  P_edge=v^4/(8*pi*G*R^2),
    v^4=sqrt(8*pi)*G^(3/2)*M_pool*sqrt(P_edge).

These are tail approximations, not identities for the solved finite profiles.
Set p=P_edge/(rho_DE*c^2) and define
kappa=v^4/[G*M_b*c*sqrt(G*rho_DE)]. Then

    kappa^2 = 8*pi*eta^2*p.

Exact kappa=1/2 requires **32*pi*eta^2*p=1** (Lean-certified conditional
implication). This is a target to explain, not a proposed physical postulate.
For the higher-energy interior, P_edge=abs(DeltaV)+2*Sigma/R, so tension also
introduces radius dependence. Neutrality alone does not fix this product.

## 3. A cosmological temperature gives a scale, not the missing force law

Source checked: S. Deser and O. Levin, *Accelerated Detectors and Temperature
in (Anti) de Sitter Spaces*, arXiv:gr-qc/9706018v1 (6 June 1997), p.3,
equation (8), https://arxiv.org/pdf/gr-qc/9706018 . The constant-acceleration
de Sitter detector relation is 2*pi*T=sqrt(a^2+Lambda/3) in natural units;
the discussion includes a conformally coupled massless scalar. It establishes
a detector temperature, not a galactic force law. Existing repository de Sitter
routes already recognize this missing response law; this audit isolates its
normalization algebra.

For dark-energy mass density rho_DE, let
A=c*H_Lambda=c*sqrt(8*pi*G*rho_DE/3). Suppose, as an ADDITIONAL unproved
response law with beta>0, that

    g_N = beta*(sqrt(g^2+A^2)-A).

Exact inversion gives

    g^2 = g_N^2/beta^2 + 2*A*g_N/beta.

The cross-term identity is Lean-certified, with the square-root relation and
response explicitly supplied as hypotheses. In the low-acceleration regime,
a0=2*A/beta, hence kappa=2*sqrt(8*pi/3)/beta. Exact kappa=1/2 requires
beta=4*sqrt(8*pi/3), not supplied by the detector calculation. Moreover, this
same constant-beta law has g approximately g_N/beta at high acceleration:
with G fixed independently by Newtonian measurements, the Newtonian limit
requires beta=1. Thus a constant response normalization cannot satisfy both
the target coefficient and that Newtonian limit. A variable response could
be engineered, but needs an independently derived interaction.

The 1/2 in sqrt(A^2+g^2)-A approximately g^2/(2*A) becomes a factor TWO in
a0 when the force law is inverted. It is not the requested prediction.

## Certificate, evidence and review

Source: lean/ParameterSelection.lean, eight theorems over an arbitrary
Lean.Grind.Field. Lean 4.34.0-rc2 compiled it with exit 0. All eight list only
propext, Classical.choice and Quot.sound; no sorryAx or added physical axioms.
Field laws and each displayed theorem hypothesis remain assumptions. No
ordered-real instance, positivity, calculus, detector QFT, transport dynamics
or stability proof is supplied by this certificate.

Run: parameter_selection_evidence/manifest.json and lean-output.txt.
Negative control: parameter_selection_mutation/ changes the detector cross
term from 2*A*beta*g_N to A*beta*g_N; its failed compilation is retained and
must not be treated as a second certificate. The wrong relation also has a
simple exact counterexample: t=5, g=4, A=3, beta=1, g_N=2 gives 16 versus 10.

Reproduce the positive certificate from the repository root:

    lean action_scale_investigation_2026_11_05/joint_phase/lean/ParameterSelection.lean

The provenance runner commands are recorded verbatim in each manifest.
Self-review checked force signs, differentiation at fixed pressure scaling,
isothermal mass/pressure elimination, density units, detector inversion and
Newtonian normalization. No new halo solver run is claimed. This is a
conditional algebra certificate plus a physical selection audit, not a proof
that every possible pool theory fails.

The remaining constructive task is specific: derive a baryon-coupled source
and a vacuum/phase state from one microscopic action, showing that the selected
eta and pressure obey the required matching relation over a mass family,
while also selecting wall tension and retaining the observed Newtonian limit.
Assigning that relation or beta by hand would only hide the calibration.
