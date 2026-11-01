# Finite two-loop vertices and graph verification

Actual finite vacuum diagrams are now implemented jointly with the
coordinator's gauge route. The common builder supplies all 98-real-scalar,
73-Weyl and 24-vector masses and every scalar cubic, needed quartic and
scalar-Weyl vertex. The coordinator adds six gauge classes to the four
scalar/fermion classes; no RG-only approximation is substituted.

At the reference e=.03 inherited minimum and fixed Qm, the complete
loop-stripped diagram sum is7.5911255946e-7, or3.0441547128e-11 after
dividing by(16pi²)^2. Individual classes reach1.33e-2, so their physical
sum has substantial cancellations. The pressure driver must retain its
own derivative/step controls and the heavy-relaxation term once.

Verification earned here:

- Ten builder/vertex controls pass, including Takagi phases, original
  polynomial cubic/quartic derivatives and Wess-Zumino graph weights.
- Every grouped scalar/fermion graph weight is invariant under degenerate
  basis changes to better than4.1e-16 relative.
- All ten actual finite graphs are invariant after scalar, fermion and
  vector basis changes to1.9e-16 of the absolute graph scale.
- Every graph obeys the predicted e^4 scaling between e=.03 and .01 to
  2.8e-16, and an actual ungauged full-SU5 SUSY sum cancels to1.03e-16.
- Independent source/code review of the coordinator's gauge contractions,
  finite constants, full sum and reduced CS calculation passes with the
  stated restrictions. See GAUGE_FULL_REVIEW.md.

Three successful v2 runs support these controls; an initial NumPy-bool JSON
serialization failure is preserved with its original source snapshot.
Peak observed RSS is248MB. No quartic98^4 array is allocated. Model code
is frozen and reused by the gauge and kinetic researchers.

The separate actual-gap check covers both fully matched phase endpoints
and X/Xmin=1.3 at e=.01,.03. The largest omega²/smallest-positive-mass²
ratios are1.22e-9 for scalars,7.64e-10 for Weyls and2.10e-13 for vectors.
All exact zero/Goldstone/retained modes are counted explicitly. This is a
tree massive-sector hierarchy, not a statement that the entire theory is
gapped. PRESSURE_REVIEW.md independently checks the coordinator's native
phase thermodynamics, matching order, count and lack of double counting.

This fills the finite vacuum-diagram gap within the specified rigid
model at two loops. It does not derive a coupling, vacuum normalization,
occupied cosmological state or gravitational completion. Kinetic/current
matching and the complete occupied-state pressure are separately owned.
All numerical statements retain their finite ranges and float tolerances;
no global novelty or all-order claim is made.
