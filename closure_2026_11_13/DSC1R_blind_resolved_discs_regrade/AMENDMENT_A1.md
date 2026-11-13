# DSC1R AMENDMENT A1 (2026-11-13): A = 1 is the record's reference halo, not 5.41 x M_b

Committed alone, before any A1 run. Still blind: every blindness rule of the brief stays in force for this step.
TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

## What changes

The brief defined the reference halo as "a halo holding 5.41 x M_b". The lead states this was the lead's error: the
record's reference layout for a disc is the halo SRJ2's `srj2_rc.py` builds and SRJ3 reuses. Under A1, **A = 1 means
that halo**:

- M_ta = X M_b h / (1 - FB) (Msun/h), X from the record's XTAB (PD1 share medians): z < 1 the z = 0 value, else the
  z = 1 value; canonical 59.4861 / 55.7159, alt 59.5029 / 55.7313. So the halo now differs slightly between footings.
- Cold mass inside r: C(r) = X M_b m(r / r_s) / m(c x_ta), r capped at r_ta; Duffy-form concentration
  c = 10.14 (M / 2e12)^-0.081 (1+z)^-1.01; Delta_ta(z) and Omega_m(z) as FRZ1.
- The halo's own cosmology is the record's (CFG556: h 0.6736, Om = 0.14237 / 0.6736^2 = 0.31377, FB = 0.02237 / 0.14237),
  as in FRZ1's halo_basics_z. The membership rule, v*(z) and E(z) keep the brief's cosmology (Omega_Lambda 0.6847),
  unchanged.
- A free multiple A multiplies this fixed profile, as before.

## What does not change

Sample, membership (it does not depend on the halo), baryon models, data construction, the chi^2 statistic, the
correlated-point correction, the misfit scale s^2, the power rule, the 3.84 s^2 interval, the 9 s^2 and p < 0.0027 lines,
labels, the twelve brackets, KA1-KA3 (KA1's halo checks are run on the A1 halo) and the twins TW-V / TW-M with their
bite rules. The A grid stays -2 to 40.

## This is post hoc

RESULT_BLIND.md (99f7bc86e6) already reports where the record's X falls on the as-frozen A axis (A ~ 10.3-11.0, outside
the as-frozen interval on both footings). A1 is therefore not blind to the direction of its own answer for the above
group. The as-frozen labels stay first in every report; A1 labels are a second reading.

Run: `python3 -I -B dsc1r.py --A1` writes `dsc1r_A1.json / .out` and `dsc1r_A1_MUTATE_TWV / TWM`; without the flag the
script must reproduce its committed outputs byte for byte (timing-free).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
