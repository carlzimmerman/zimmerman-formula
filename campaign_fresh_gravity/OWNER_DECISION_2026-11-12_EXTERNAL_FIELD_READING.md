# Owner decision, 2026-11-12 (dated note; no frozen file edited)

**Decision:** the framework's lanes use the ACTUAL-FIELD reading of the Milky Way's external field
from here.

The owner was asked, after lane EFC1 (`closure_2026_11_12/EFC1_external_field_convention/`, origin
36288d8ebd), "Which reading of the Milky Way's external field should the framework's lanes use from
here?" and answered: "Actual-field reading".

**What it means.** The acceleration computed in hunt item 81 (1.191 x 10^-12 m/s^2 toward Galactic
(268.5, +33.0), dominated by the LambdaCDM linear-theory acceleration from all matter) is read as the
actual external acceleration at the Milky Way, not as a Newtonian source. Inside the kernel the
Newtonian-equivalent field e_N is the solution of nu(e_N) e_N = g / a0. With
nu(y) = 1 / (1 - exp(-sqrt(y))) that is **0.000160 (canonical) and 0.000110 (alt)**, in place of
0.01273. With another kernel, solve the same equation with that kernel.

**Scope.** Forward only. Earlier lanes stand as frozen; their field cases are read through this note.

**Consequences, from committed outputs (nothing recomputed here):**

- The field takes over near 790 kpc (canonical) / 870 kpc (alt). Inside 300 kpc the Milky Way line
  is the no-field line: 5.69 / 6.22 at 80 kpc, 13.7 / 15.0 at 200 kpc, 18.6 / 20.4 at 273 kpc
  (10^11 Msun, canonical / alt). There is no plateau near 100 kpc. (EFC1.)
- With census baryons the line passes the DESI curves (NMB1: Q 2.40 / 0.05; NIM2 at three radii:
  7.59, fragile, / 2.01), the published masses at 100 kpc and beyond, and the rows beyond 150 kpc.
  (EFC1 reading A; PLT1's no-field case.)
- With Miller and Bregman hot gas added: canonical passes; alt sits at the gate against the rows
  beyond 150 kpc (+2.00 with the profile extrapolated, inside the gate with it stopped at 250 kpc).
  A corona as massive as Faerman 2017's fails high: it needed a field of 0.004 or more. (EFC1, HG2.)
- The rotation curve at zero field needs a stellar mass of 7.08 [6.92, 7.24] (Ou 2024) or
  6.81 [6.68, 6.94] (Eilers 2019) x 10^10 on canonical, and 6.42 [6.27, 6.57] or 6.20 [6.07, 6.32] on
  alt. RCF1's free fit preferred a larger field by a chi-square gain of 1.6 to 5.6; under this
  decision the field is not free. (RCF1, post hoc rows.)
- FALSIFIER_MATRIX row 32: the kill as first registered (a measured M(<200 kpc) >= 1.0 x 10^12)
  would now fire on the framework's own line (1.37 / 1.50 x 10^12 at 200 kpc), so it cannot stand as
  a kill under this reading. The re-scoped kill (gamma(100-200) <= -2.25) is consistent with it.
  The row's status is not changed by this note.
- Numbers that belong to the earlier reading and should not be quoted as the framework's: G239's
  plateau (5.26 x 10^11) and its 80 kpc pulls with the field; hunt item 38's "stops at 5.07 x 10^11
  beyond 71 kpc"; DW1's external-field rows; the 2026-11-12 correction lane's matched-field values;
  the field cases of PLT1, MWJ1, MWG1, SAT1 and NIM2.

**Not decided by this note:** the reading for other galaxies' environments; whether a baryons-only
source (e_N 0.0027) is ever the right one; the field's direction; and what the framework's
large-scale dynamics is. The lead's argument for this reading (the cold component is counted once,
so the kernel must not be applied to an all-matter acceleration) is an argument, not a derivation.

kappa = 1/2 FITTED; not theory closed.
