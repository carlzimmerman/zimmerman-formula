# WV1 AMENDMENT A2 (post hoc): the law bracket at nu_max is graded on the outputs it reaches

Committed alone. **Post hoc**: written after the two log M_b 9.4 law-bracket runs at nu_max (both footings) had produced
outputs at z = 2, 1 and 0.5 and their R_s values there (all 0) were seen. The two log M_b 10.7 bracket runs at nu_max had
not yet reached z = 2 when this was written. No threshold changes.

## Why

S3(b) as frozen grades max(R_s law off, R_s bracket), each the minimum over the last-Gyr set. The bracket (the law on
the baryons' field everywhere, as if the frame were static everywhere) deepens the well at every radius, so Psi
collapses much harder than in the primary run. At nu_max its soliton reaches 5e9 to 8e10 times the mean density by
z = 0.5 at log M_b 9.4. Its half-mass radius is then about 0.07 kpc, one to two grid cells. The run's own fold-free
check flags it (19 and 35 density maxima narrower than 4 cells at z = 0.5, canonical and alt), and the time step falls
to about 6e-6 time units. Reaching z = 0 would take many hours, and the inner profile would be set by the grid rather
than by the physics. Higher-nu bracket runs (nu_max x 4 to x 1024) finish normally.

## Replacement (A2)

For the four bracket runs at nu_max only: the lead stops each run after it has reached at least the z = 2 output.
R_s(bracket) is the minimum of R_s over the outputs the run reached, taken from its checkpoint
(`runs/<tag>_partial.json`, written by `wv1_partial.py`). This value replaces the bracket's last-Gyr minimum in S3(b)'s
graded value at nu_max. The primary law-off runs and every other bracket run keep the last-Gyr set as frozen.

Labels are reported three ways: as frozen (KA4(ii) failed, so V1 reads NO VERDICT), under A1 (the bracket runs at
nu_max do not finish, so V1's S3(b) reads NO VERDICT: a deciding run did not finish), and under A1 + A2. V2's label
rests on neither amendment.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
