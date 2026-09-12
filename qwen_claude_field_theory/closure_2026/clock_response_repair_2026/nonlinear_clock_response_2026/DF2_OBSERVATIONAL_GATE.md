# Carl's dark-matter-deficient galaxy question

Prompt attribution: Carl Zimmerman asked whether the galaxy reported to
contain no dark matter supplies a clue for this framework (12 September 2026).
The observations themselves and MOND's external-field interpretation are
prior literature, not discoveries or novelty claims of this repository.

The likely objects are NGC 1052-DF2 and DF4. Stellar kinematics in DF2 imply
a low dynamical mass, comparable to the stellar mass within the measured
half-light radius under the adopted Newtonian equilibrium analysis. This
is a statement about the inferred mass discrepancy within a measured region,
not a direct particle census or proof of a zero-mass halo everywhere.
Source: Danieli et al. (2019),
[Still Missing Dark Matter](https://arxiv.org/abs/1901.03711).

The theoretical distinction is important: little required unseen mass does
not automatically validate a no-particle modified-gravity law. An isolated,
equilibrated low-acceleration system is precisely where MOND ordinarily
predicts enhanced gravity. A host's external field can suppress the internal
MOND enhancement, but that must be computed using the actual environment,
not asserted from projected proximity. See Famaey, McGaugh and Milgrom (2018),
[MOND and the dynamics of NGC1052-DF2](https://arxiv.org/abs/1804.04167).
That paper's numerical estimate uses its contemporary observational inputs;
it is not a current likelihood analysis of this action.

Deep imaging confirms tidal tails in DF4 but not DF2 at the reported depth.
Thus halo stripping is a supported possibility for DF4, not an established
universal explanation of both galaxies. See Golini et al. (2024),
[Ultra-deep imaging of NGC1052-DF2 and NGC1052-DF4](https://arxiv.org/abs/2402.04304).

There is a relevant recent update: Tang et al. (June 2026) report a DF2
surface-brightness-fluctuation distance of 17.7 +/- 1.4 Mpc and discuss a
JWST red-giant-tip distance of 17.6 +/- 0.6 Mpc, shorter than the published
HST estimate they quote. They continue to describe the galaxies as
dark-matter deficient and call for uniform JWST observations. A revised
distance affects stellar masses, dynamical masses and host separations;
it is not by itself a proof that the discrepancy is resolved. Source:
[New Measurements of Distances ... Testing the Bullet-Dwarf Origin](https://arxiv.org/abs/2606.05144v2).
Scope: primary-paper abstracts checked on 12 September 2026, not an exhaustive
review or reanalysis of spectra and images.

## Consequence for this project

Inference, not a result already computed: the same action and global a0 must
predict both highly discrepant diffuse galaxies and these nearly baryon-only
systems from independently constrained environments and histories. This is
a sharper test than merely saying no dark matter particles are used.

A future test should propagate distance, stellar mass-to-light ratio,
anisotropy/rotation, equilibrium and three-dimensional host-location
uncertainties through the action-derived internal field and Jeans or
time-dependent dynamics. No local a0, chosen dust-depletion fraction, or
borrowed MOND external-field fit should be installed to manufacture agreement.
No such fit, empirical pass, or universal no-go was performed in this checkpoint.

## Concurrent L198: limited read-only review

While this note was being prepared, commit `d28d97ba1` added
`fable_independent_2026/L198_df2_external_field.py` and its outputs. Reading
the actual source and archived numbers establishes the following limits:

- It uses an assigned RAR nu kernel, a half-mass velocity estimator, a
  retained fraction 0.135, NFW concentration 10, an assumed halo-mass relation,
  and projected host separation. It does not vary or solve the P/W/gamma
  action studied in this checkpoint.
- The external acceleration is first boosted and then supplied as the
  argument of nu again. This prescription is not derived there from a
  consistent external-field boundary-value problem of the action.
- The two distances tested are 20 and 13 Mpc. The quoted low-tension
  near-distance case does not test the June 2026 JWST value of 17.6 Mpc.
- V4's message says the retained-sector prediction exceeds **both** stellar
  measurements by more than two standard deviations, but its predicate
  checks only the Danieli entry. Using the stored predictions with its own
  Emsellem mean/error gives 1.64057 and 1.73765, not greater than two.
- The reported sigma offsets divide by a selected observational error only;
  they do not marginalize stellar, host, distance, profile or model uncertainty.
  They are nominal residuals of that approximation, not robust exclusions.

This does not establish that L198's entire qualitative concern is wrong:
adding a universal retained component can raise a low-dispersion galaxy's
predicted dispersion. It means the new numerical values are not same-action
closure evidence. We did not modify or rerun L198, which writes its output
on execution. Its source remains intact for the collaborating researcher.
