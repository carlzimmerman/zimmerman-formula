# Ancestry and unresolved curvature-renormalization bridge

This note is separate from the frozen previous reviews and from all science files.

## Nearest-ancestor overlap

The base compact SU(2) Haar/Dashen integral, y=0 and x=0 axes, first charge insertion, metric cancellation, and canonical zero-mode measure cancellation are already established in FSP003:

* `qcd_prediction/controlled_model/qcd_zero_modes/REPORT.md`, sections 4,6,7;
* `qcd_prediction/coordinator/ZERO_MODE_QED_RAW.md`;
* the exact-over-Gaussian replacement proposal is explicitly in the report's section 9.

Here x equals the ancestor's `2mu` at theta=0 and y equals its t. Re-deriving or re-sampling these identities is not a new research result. The genuine continuation to assess is the first nonconstant-pion source contraction and its matching/renormalization, not another grid for the base integral.

## Authenticated source and pole question

Primary source: B. Kubis and U.-G. Meissner, *Virtual photons in the pion form factors and the energy-momentum tensor*, arXiv:hep-ph/9908261v2, banner dated 2001-05-15. Local PDF `/private/tmp/fsp007-curved-sources/kubis9908261v2.pdf`; SHA256 `6c4267db298d51fdf8df0205edeaa5dede792b4b014eb88cd2397e58025bdb72`. Official arXiv PDF text and the local printed p.11 were both inspected, the latter visually.

Equations (4.7),(4.8) literally give

`L_(4,em,R)=k15 F^2 R Tr(QUQUdagger)`, `beta15=1/2+2Z/3`, `Z=C/F^4`.

The source's (2.5) defines `l_i^r(mu)=beta_i[bar l_i+log(Mpi0^2/mu^2)]/(32pi^2)`, and (4.5) gives `beta13=1/8`. Its stated calculation concerns pion form factors, with additional pion-independent terms omitted from the displayed curvature basis.

Independently, the covariant constant-background contraction of the stated nonlinear pion action gives `g_div=R/(96pi^2 epsilon F^2)` for `d=4-2epsilon`. Its mass term has pole

`W_mass,div=V R M^2 a0/(64pi^2 epsilon)`.

Since `Tr chi+=4M^2 a0`, this is canceled by `delta l13=-1/(256pi^2 epsilon)`, agreeing with beta13=1/8 in the usual `1/[16pi^2(d-4)]` bare convention. This cross-check fixes the tadpole's factor-of-two dimensional convention.

For the electromagnetic orientation, `Delta_(S3)s=4-8s` yields

`W_EM,div=V u C R(1-2s)/(48pi^2 epsilon F^2)`.

If the single displayed Euclidean operator is identified literally with `+u F^2 k15 R(5/9-s)`, its s term would require `delta k15=-Z/(24pi^2 epsilon)`. This corresponds to a pion part `4Z/3`, whereas using the printed `2Z/3` in the same standard bare convention gives half that residue.

This is an **unresolved translation/renormalization obligation**, not a certified source error. The bridge from the off-shell collective-background effective action to the form-factor counterterm basis may involve equation-of-motion operators, field/measure conventions, omitted source-only curvature terms, or a different bare definition. Those possibilities have not been checked sufficiently to choose one. Merely replacing a spectral s=1 regulator pole by a dimensional epsilon without a common regulator calculation is also insufficient.

Consequently the first tadpole source contraction can be accepted as a specified partial bare/common-regulator contribution, while identifying its complete subtraction with the quoted k15 beta function cannot yet be certified. A finite common-scheme curvature LEC remains an explicit input. No closed scale-independent NLO QCD+QED sphere response follows from this calculation alone.
