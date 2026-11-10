# DT1: what the clock's dust term has to do, and one candidate (2026-11-10)

Adopts nothing. kappa = 1/2 FITTED; not theory closed. Not registered. **A design note, not a graded lane: no criteria, no
label, and every number in it is hand-level arithmetic** (`dt1_design.py` -> `dt1_design.out`). Written at the owner's
instruction ("do the new design work") while lane MK1 was still running; MK1's interim rows already showed that the
quadratic dust term has no single constant. The candidate below has passed no gate. It is to be graded by a lane (MK2).

## Graded since (added 2026-11-10 evening): the candidate fails

MK2 (`../MK2_exponential_dust_term/RESULT.md`, origin 6bbfd8697b) graded the exponential term: **NO VALUE / NO VALUE.**
Clusters and groups pass at no sound speed. It also found this note wrong in three places and incomplete in one:

- Section 3's "wells much deeper than x_T fill without limit; conservation caps them at their share" does not survive
  self-gravity with the cap: each cluster's static state stops existing first (between 1000 and 750 km/s), with dust at
  24 to 79 % of the baryons.
- The "570 km/s" match to QX2's cluster amount and the group number beside it are moot: there is no static state there.
- The "ordering" QX2 named was the onset radius of an oscillation, not the pooled amount.
- Section 2's "Jeans length of at least 17 Mpc for z < 2" holds only at some epoch of that stretch (a mean-value
  statement). The trade-off itself holds under conditions this note did not write: n monotone, the threshold measured
  from today's offset, weak field.

What MK2 confirmed: galaxies stay clean above about 300 km/s, and above about 500 km/s the clock around a galaxy is
static out to form B's cap. The text below is left as written.

## Answer first

1. **One requirement cannot be met by any dust term, and it is the one the quadratic was being pushed towards.** A dust
   term cannot both keep the dust clumping on small scales at late times and keep it out of galaxy wells. So under
   form B the dust must be warm at late times, and everything small and late has to be built by baryons and the law's
   halos. That is a consequence, not a choice, and it is untested.
2. **A one-constant candidate exists for the rest:** an exponential dust term, which makes the clock's dust isothermal
   with a fixed sound speed of a few hundred km/s. It is dust at every epoch, it stays out of galaxies, and it fills the
   deepest wells first. Whether it passes the record's gates is not known.

## 1. The dust term as one function

The term L_K(Q) enters through n(x) = K L_K'(1 + x), x = Q - 1 (n is 4 pi G times the dust density over c^2). For any n:

- **Background.** n(xbar(a)) = n0 / a^3 (the conserved charge).
- **Coldness.** c_s^2 = n / n', and the Jeans wavenumber is k_J^2 = n'(xbar), physical. For the quadratic this is
  k_J = mu_K, MK1's row 2.
- **Wells.** A static clock sits at x = xbar_inf + phi, phi = |Phi| / c^2 (QX17's static row; TPA1 section 4.5). So a
  well of depth phi holds dust n(xbar_inf + phi). **The same function sets how cold the dust is and how much of it
  pools.**

## 2. The trade-off (holds for every n)

If n' >= k^2 while the background density runs from n_a to n_b, that stretch spans a clock offset of at most
(n_b - n_a) / k^2. Every well deeper than that stretch's start plus its width then holds at least n_b.

In numbers: clumping at 20 per Mpc (physical) from z = 2 to 5 confines that stretch to an offset of 1e-8, while galaxy
wells are 1e-7 to 4e-6 deep. To keep the deepest spirals below 216 times the mean, n must be flat below the z = 2
density: slope at most 0.14 per Mpc^2, a Jeans length of at least 17 Mpc for z < 2. The quadratic at the record's CMB
line (198 per Mpc) has slope 3.9e4 and puts 1.9e5 times the mean density into a dwarf's well.

So the three things asked of the dust split as follows:

| Asked | Possible together with empty galaxies? |
|---|---|
| Dust at the CMB and before (w small, cold on CMB scales) | yes: steep n at high density |
| Deep wells (clusters) hold their share; galaxies hold almost none | yes: n flat at low offset, rising beyond galaxy depths |
| Dust still clumping on galaxy and forest scales at late times | **no** |

## 3. The candidate: an exponential term

    L_K(Q) = (n_* x_T / K) exp((Q - 1) / x_T),      n(x) = n_* exp(x / x_T),      one constant x_T = c_s^2 / c^2 .

n_* only shifts the clock's zero. The clock's dust is then isothermal: w = c_s^2 = x_T at every epoch, and a well holds
n = n_mean exp(phi / x_T).

| | c_s 350 km/s | c_s 500 km/s | c_s 1000 km/s | quadratic at 198 / Mpc |
|---|---|---|---|---|
| w, all epochs | 1.4e-6 | 2.8e-6 | 1.1e-5 | 0.011 at z 3400, then falling |
| Jeans k, comoving, z 1100 (want 0.3 or more) | 4.1 | 2.9 | 1.5 | 0.18 |
| Jeans length, comoving, z 3 | 25 Mpc | 36 Mpc | 72 Mpc | 0.13 Mpc |
| Dust in a dwarf's well (x mean) | 1.1 | 1.0 | 1.0 | 1.9e5 |
| Dust in the deepest spiral's well | 19 | 4.2 | 1.4 | 7.4e6 |
| Dust in a group's well (depth 8e-6) | 354 | 18 | 2.1 | 1.5e7 |
| Dust in a cluster core (depth 3e-5) | 3.6e9 (capped by the share) | 4.8e4 | 15 | 5.6e7 |

For scale: the quadratic at QX2's cluster value (1.78 per Mpc) puts 4.5e3 times the mean in a cluster core. The
exponential gives that at c_s near 570 km/s.

What it does by construction:

- Dust at the CMB, at BBN and today, with no stiff early phase.
- Galaxy wells hold a few times the mean: less than 1e8 Msun inside 30 kpc of the deepest spiral.
- Deep wells fill first, clusters before groups before galaxies. That is the ordering QX2 found the quadratic gets
  wrong.
- Wells much deeper than x_T would fill without limit; conservation caps them at their share. That is form B's cluster.

## 4. Where it may fail (not graded)

1. **Late small-scale structure.** The dust does not clump below 25 to 70 Mpc (comoving) at z = 3, nor below 50 to 140
   today. The forest, growth and CMB-lensing rows that form B carries "from the cold reference" would no longer be
   carried. They would rest on baryons and the law's halos, which nobody has computed. This is the largest risk.
2. **The record's clustering line** (MK1 row 2, at least 2.5e4 per Mpc) fails by construction. Whether that line still
   applies when galaxies need no dust of their own is for the grading lane to say, not this note.
3. **Groups and clusters with one constant.** At 570 km/s a group's well holds about ten times the mean, far less than
   the groups row asked of the quadratic. Self-gravity and the cap change this; it must be solved, not estimated.
4. **The cluster's radial shape.** Isothermal dust colder than the cluster gas is more concentrated than the gas.
   X-COP's shape gate may fail.
5. **A sound speed of hundreds of km/s** sits near the edge of what the CMB allows for a cold component's sound speed
   in the literature as I remember it. Not checked here.
6. **Health.** L_K'' > 0, so the sound speed is real. The term has no minimum at Q = 1. Nothing else was checked.

## 5. What grading it means

Lane MK2, once MK1 has landed: MK1's rows with this term in place of the quadratic, one constant c_s; the static cluster
and group solved with self-gravity and the cap; SCS1's stability condition with this term; and the trade-off of section 2
certified in Lean. The forest and growth rows need the structure computation that COL1 is the first step of.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
