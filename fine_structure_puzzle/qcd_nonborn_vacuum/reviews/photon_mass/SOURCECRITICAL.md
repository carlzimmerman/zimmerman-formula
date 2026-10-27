# Massive-photon primary-source and canonical-matching note

Created before reading the new author photon_mass/ packet. PRETARGET.md is
pinned as e5f054b17352783219246814d99dfafa172f9ea3ec038e045a8867082109a0d5.
Its persistence-failure/contact-hint chronology is explicit; the footnote
question is not claimed blind. The projector and new exact-check code were
independently derived before seeing any new author target.

## Primary source authentication and scope

Direct primary PDF opened through the search-service connector:
https://arxiv.org/pdf/1507.08916v3 . The visible banner authenticates Endres,
Shindler, Tiburzi, Walker-Loud, arXiv:1507.08916v3, 11 Aug 2016. Page 2 Eq. (3)
gives the universal -alpha Q^2 m_gamma/2 term and an analytic m_gamma^2/M
term with an unfixed local coefficient. The stated analysis is leading order
in alpha, with canonically normalized A and expansion in m_gamma/M. It does
not display explicit cubic magnetic/radius coefficients.

Page 6, footnote [42], admits m_gamma^2 A_mu A_mu psi-dagger psi and says it
contributes at N3LO. No coefficient or explicit e power is supplied. This is
not a source derivation of its tadpole or a matching identity for a fixed
pure-QCD two-current tensor. The source also treats the temporal zero mode
nonperturbatively, giving a finite-four-volume Gaussian time dependence.

A separately delegated source-only reviewer independently checked this primary
PDF and the author-institution mirror, and supplied the precise convention
comparison with Clark et al. 2201.03251v1 and the 1512.08983 zero-mode paper.
Their notes are in qedm_sources/. No source bytes were retained, so a primary
PDF content hash is unavailable; the exact URL/version/locators and source-note
hashes are recorded instead. No source-cache write occurred.

## Electromagnetic order and the actual obstruction

The source footnote alone cannot determine the e-power of its unspecified
Wilson coefficient. To demonstrate the possible order, define an EFT term
explicitly as

 Delta L_E = u*c_s*s*A_mu A_mu*N-dagger N/M^3,  u=e^2.

One free-photon contraction carries no further u, so its tadpole contributes
at first order u. In a gauge with propagator trace rho/(Q^2+s), its mass
response f=M_u/M includes

 (rho*c_s/M^4)*s*integral d^4Q/(2*pi)^4 1/(Q^2+s).

A soft cutoff gives integral=[Lambda^2-s log((Lambda^2+s)/s)]/(16*pi^2),
so this term has an s^2 log(s) coefficient rho*c_s/(16*pi^2*M^4). The same
projector keeps this coefficient. Analyticity of c_s in s does not remove the
nonanalytic photon tadpole. The rho value and coefficient convention depend
on the EFT/gauge definition; no source value is assigned here.

This demonstration does NOT establish that such an independent c_s is present
in the canonical observable. It establishes that a generic admitted contact
cannot be discarded as a higher order in u without a counting/matching check.

## Canonical deformation versus a general massive-photon mass curve

Define the canonical observable microscopically: the u=0 pure-QCD matter action
and all its external-current derivatives are independent of s; only the free
photon covariance is changed to D_s. Expanding the minimally coupled matter
functional to first order u then gives the complete fixed QCD two-current
kernel contracted with D_s, with its predetermined action/current seagulls,
normalization, endpoint and renormalization contacts. In this definition there
is no additional freely chosen u*s*A^2*N-dagger N vertex. A full matching
identity, rather than a guessed individual EFT coefficient, fixes any faithful
hadronic representation of this canonical deformation.

An EFT field redefinition or use of a massive-photon equation of motion can
redistribute a gauge-invariant F^2 interaction into terms involving s*A^2 and
other current/contact operators. Hence absence of an independent vertex does
not mean its coefficient is zero in every EFT basis. Conversely, generic
massive-photon EFT permits extra operators and prescriptions; the primary
footnote does not prove their coefficients correlated with the canonical
current tensor. Calling an arbitrary fitted massive-photon curve canonical
without specifying and matching those terms would be a missing implication.

The safe statement is conditional: the canonical fixed-tensor filter is valid
under its specified deformation; transfer to a generic QED_M mass curve needs
microscopic/current-to-EFT matching, including the full operator combination at
order u and s^2 log(s), plus the fixed-parameter calibration path. Analytic local
mass counterterms are annihilated; analytic coefficients multiplying photon
vertices cannot automatically be called annihilated mass counterterms.

## Propagator dictionary and positivity

Let x=Q^2. The current-tensor representation uses D_s=1/(x+s). The parent's
massless radial density instead uses P_s=x/(x+s)=x*D_s. Since x is independent
of s, every differential/stencil operation gives

 Pi[P_s]=x*Pi[D_s].

For Pi_full=(2/(3s^2)) E(E-1)(E-2)(E-1/2)(E-3/2),

 Pi_full[D_s]=-5s(3x-s)(x-3s)/(x+s)^6,
 Pi_full[P_s]=-5s*x(3x-s)(x-3s)/(x+s)^6.

The extra x belongs to the regulator-multiplier convention, not a changed
projector normalization. Both full weights change sign. Individual alternating
ordinary derivatives of D_s are positive; the negative NB third-derivative
kernel is positive after multiplication by minus one. This does not make the
full fifth-order filter or the NB hadronic tensor positive.

## Classification and limits

QED_M infrared extrapolation and its leading terms are established methods.
This projector is a method translation/formal corollary of asymptotic
coefficient extraction, not a global novelty claim. The new bounded check
will verify algebra and convention translation, not physical QCD data,
remainder bounds or matching of the additional EFT operators.
