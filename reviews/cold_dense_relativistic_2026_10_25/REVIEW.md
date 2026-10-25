# Self-review

Primary verdict: computationally verified only in the stated range, for the
formal averaged-fluid diagnostic. No physical real-scalar star or stability
certificate is claimed.

Passed: exact full potential, dense turning point, cycle-averaged pressure,
virial control, quadrature refinement, independent direct derivative check,
vacuum-active-force sign, center expansion, uniform-density analytic TOV check,
and all 61 terminal classifications at two resolutions/tolerances.

Failed as a physical closure: the pressure-zero surface region has dP/dE>1 under
the naive perfect-fluid interpretation. This is a failure of that interpretation,
not a demonstrated violation of causality by the canonical scalar. The initial
failed run is preserved; continuation is explicitly diagnostic.

Conditional: applying isotropic time-averaged stress to the real scalar neglects
gradients, phase structure, interface stresses and metric oscillations. The
coordinate cutoff F=1e-5 is not a black-hole formation result. A finite central
density scan cannot rule out every full-field solution or nonmonotonic branch.

Not addressed: real-field surface matching, radial perturbation eigenvalues,
nonlinear stability, formation, radiative lifetime, cosmological occupation,
cluster population profile and the model's galaxy force/lensing calculation.

Source translation: TOV Lambda signs and separation of mass/vacuum were checked
against primary-source equations (13)–(14); details in SOURCE_CHECK.md. Stability
claims from that source were not transferred to this EOS.

Proofreading: complete REPORT.md reviewed. Distinguishes excitation density E,
pressure P, vacuum 1.6, dimensionless radius x, mass mu and metric factor F.
Formal zero-vacuum solutions are not presented as physical candidates.
Review provenance: self-review of this checkpoint continuing e8b0beff16.
