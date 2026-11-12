# EFC1 FROZEN CRITERIA: which number is the Milky Way's external field, and what each reading does

Committed alone, 2026-11-12, before any script. A post hoc consolidation prompted by LIT1's flag. TEST
lane. Adopts nothing. Relabels no other lane. Does not decide which reading is right: that is the
owner's and the theory's. kappa = 1/2 FITTED; not theory closed.

## The flag

The record's external field at the Milky Way, e_N = 0.01273 (hunt item 81), is used inside the kernel
as a NEWTONIAN source field (DW1, G239, PLT1, MWJ1, MWG1 and their successors). Item 81 built its
dominant term from the 2M++ density field with LambdaCDM linear theory, g = 3 H0 Omega_m v / (2 b):
that is the acceleration from ALL matter in the standard model, 1.161e-12 m/s^2, the same size as the
Local Group's actual acceleration. The MOND literature quotes the Milky Way's external field as an
ACTUAL acceleration of 0.01 to 0.03 a0 (LIT1, PROVISIONAL). Inside the kernel, a Newtonian field e
produces an actual field nu(e) e. So the same 1.19e-12 m/s^2 gives very different results depending
on whether it is read as the Newtonian source or as the actual field.

## Disclosed

Hand arithmetic done before freezing: read as an actual field, 0.0127 a0 corresponds to a
Newtonian-equivalent e_N near 1.6e-4, which is inside every field window found today (0 to 0.0075
and wider), and puts the takeover radius near 800 kpc instead of about 100 kpc. Read as the record
reads it, 0.01273 implies an actual external acceleration of about 0.12 a0, nine times the
acceleration it was derived from. Nothing below has been computed with the gates.

## Readings (per footing; kernel nu(y) = 1/(1 - exp(-sqrt(y))))

- **R, the record's:** e_N = g_tot / a0 with g_tot = 1.191e-12 m/s^2 (0.01273 canonical, 0.01054 alt;
  the lanes used 0.01273 on both footings, which is also evaluated).
- **A, actual-field:** the same g_tot read as the actual external acceleration; e_N solves
  nu(e) e = g_tot / a0.
- **L, literature:** actual field 0.01, 0.02 and 0.03 a0; e_N solves nu(e) e = that.
- **B, baryons-only source:** item 81's large-scale term multiplied by Omega_b / Omega_m (0.049 / the
  script's Omega_m), plus its Newtonian M31 and LMC terms, summed as vectors; e_N = |sum| / a0.

For each: e_N; the actual field it implies (in a0 and m/s^2); the takeover radius where the Galaxy's
Newtonian field equals e_N a0 (census point mass); the saturation mass [nu(e) + e nu'(e)/3] M_b; the
line at 80, 200 and 273 kpc; and MWJ1's three gates (curves, outer masses, plateau rows) with census
baryons and with MWG1's Miller and Bregman hot gas.

## Labels

Per reading, footing and baryon set: **PASSES** all three gates, or **FAILS** naming the gates.
Headline: **CONVENTION-DEPENDENT** if reading R and reading A differ in any gate outcome at census
baryons; **CONVENTION-INDEPENDENT** otherwise. Also stated: under which readings the takeover radius
is inside 300 kpc.

## Known-answer checks (before any label)

| id | check | pass condition |
|---|---|---|
| KA1 | the vector sum of item 81's three terms (large-scale 1.161e-12 toward (267.5, +40.3); M31 1.3e11 Msun at 770 kpc toward (121.17, -21.57); LMC 3.0e9 Msun at 49.9 kpc toward (280.47, -32.89)) | 1.191e-12 m/s^2 within 1 per cent, direction within 1 degree of (268.5, +33.0) |
| KA2 | at e_N = 0.01273, census, canonical | Q 4.89 within 0.03 and satellite-class plateau median -2.72 within 0.02 (MWJ1) |
| KA3 | the inversion nu(e) e = x | round trip to 1e-10 at x = 0.01, 0.0127, 0.03 |

## Mutation

M1: in reading A with the kernel replaced by 1, e_N must equal reading R's (the two readings differ by
exactly the kernel factor).
