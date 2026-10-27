# CI-5: field-responsive charge with inherited constant phase elasticity

CI-4 corrects charge response but still develops multiple interfaces. The
response-weighted phase stiffness becomes weak where the T field is small.
Restore the ORIGINAL constant ell30 stiffness from LIO, now coupled to the
new field-responsive charge. This changes the hypothesis of its earlier
no-charge exclusion. No new dimensional elasticity parameter is added.

Use Local's exact constant exterior capacitance, not the response tail.
All charge field-mass derivatives remain, while the constant gradient energy
has no direct cold-mass derivative. Positive metric D+L+Ltail. Large disk,
n128, beta100,1000, k100,1000,10000, starts.4,.7:12 minima. Same joint gates.
Refinement, complete species forces and stability required before any pass.
