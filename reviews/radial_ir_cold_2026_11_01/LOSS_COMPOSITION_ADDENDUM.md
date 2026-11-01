# Preferred leading-loss composition: interference and final collisions

The preferred coordinator record is run_loss_v2. The original run_loss,
script, contract and LEADING_LOSS_SCOPE.md remain byte-for-byte unchanged.
They composed the earlier narrower set of individual class bounds. Fresh
independent review required explicit amplitude interference when classes
share final states; the new record supplies it and includes the final
leading four-fermion/light-exchange collision bounds.

For decay amplitudes use the triangle inequality in the direct-sum Hilbert
space of final states and phase space:

    Gamma3_upper=(sqrt(Gamma_hard_upper)
                  +sqrt(Gamma_phase_soft_upper)
                  +sqrt(Gamma_virtualG_upper))^2.

The two-body Ward channel has a different final particle multiplicity and
is added separately. Interfering even orthogonal three-body classes in
this inequality is conservative. In particular, mixed hard gauge channels
and light Goldstino-exchange channels need not be treated as disjoint.

For nonrelativistic annihilation at the specified local density use the
same Cauchy/triangle inequality on per-particle rate bounds. The final
run_four_fermion_v2 lists the heavy four-fermion contact, phase/light-
gaugino pairs, separate radial Goldstino pair, two-Ward exchanges and hard
two-vector classes. Replace overlapping estimates by their maximum rather
than counting the same class twice. The coordinator's deliberately looser
hard crossed bound is retained. Then

    Gamma_ann_upper=(sum_classes sqrt(n sigma_v_class_upper))^2.

The resulting leading-loss upper rate is Gamma_Ward+Gamma3_upper+
Gamma_ann_upper. A 1e-8 arithmetic padding covers rounding of recorded
constants; it is not a bound on missing physical perturbative orders.

The cold-state correction separately pins the actual e=.003 radial mass
slopes for all three residual groups and corrects its earlier graph-class
rate sum. The preferred active proof is FOUR_FERMION_COLLISIONS.md read
with FOUR_FERMION_CORRECTION.md. All earlier numerical arithmetic and
known diagnostic limitations remain visible. These corrections leave the
reported leading survival and coldness conclusion unchanged.

The output remains a bound on a named retained vacuum/NR loss set, not an
all-orders total width, early thermal transport history, or a completed
dark-matter/gravity model. A constant local halo density used in n sigma v
is not an integration through an unspecified early cosmological population.
