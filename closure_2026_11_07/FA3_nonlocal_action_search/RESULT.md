# FA3: nonlocal, history and global actions. No candidate survives; the three graded all FAIL the web row, and none closes the residue

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No particle. Footings never pooled.

- Criteria: FROZEN_CRITERIA.md + IDEAS.md (local 6955fb5190, origin 1488cb5b05), committed and pushed alone before any
  script or number. The I4 formula correction and the KiDS-bound wording came from the adversarial review and were made
  before the freeze (disclosed in both files).
- Script: fa3.py. GB1 is exec'd read-only up to its main block, and SV5's sv5_web is imported read-only.
- Outputs: fa3.json / fa3.out (main) and fa3_MUTATE.json / fa3_MUTATE.out. Logs: run_main.txt, run_mutate.txt.
- One thread, nice 15, about 3 min per run.

## Labels

| Candidate | Label | Rows |
|---|---|---|
| **I1** causal memory of the phantom (retarded kernel along the khronon flow, tau set by G1) | **FAIL** | W1 web (r 75.4 / 78.8 at tau_gal); G2-G7 as the plain law |
| **I3** formation-epoch a0 memory, z_f built from top-hat collapse density | **FAIL** | G2-G7, W1 |
| **I4** conserved phantom charge (ratchet mu x merger N_eff) | **FAIL** (W1); **NO VERDICT** (G1-G7; history not carried) | brackets: G2, G3, G6 FAIL at every bracket value; G5 FAIL canonical at every value, PASS alt only at the most gas-rich SPARC progenitor |

No candidate SURVIVES. The five not graded (I2, I5-I8) and the two reviewer additions (I9, I10) carry their kill in
IDEAS.md.

## Known answers (all PASS, both footings)

| KA | canonical | alt | line |
|---|---|---|---|
| KA1 GB1 L0 class means | max \|d\| 4.3e-7 | 4.5e-7 | 1e-6 |
| KA1 L0 G1-G8 numbers vs gb1.json | 0 | 0 | 1e-9 |
| KA2 SV5 iter_1 law-on web r | 74.742402 (rel 0) | 89.362969 (rel 0) | 1e-6 rel |
| K1 I1 at tau -> 0 | 74.742402 (rel 0) | 89.362969 (rel 0) | 1e-6 rel |

Line used: W1 |r - 1| <= 3 sigma_A = 0.0722 (sigma_A 0.0241). Background t0 = 14.07 Gyr (QX3 iter3 solver, from z 3400).

## I1: causal memory cannot switch the law off on the web

**Inputs to the kernel-free theorem, both measured.**
- (a) Web: at every adjacent ZG pair the earlier snapshot's |W| is not smaller in 100.00 % of the mass. The mean cosine
  between snapshots is 1.00000, and the median past/present ratio per step is 1.12-1.38.
- (b) KiDS K1 lenses: |W|/a0 is 0.037-0.185 canonical and 0.033-0.170 alt.

**Theorem reading.** For any positive causal kernel, S_web >= (|W_host|/a0) S_host >= 0.17 S_host. The web needs
S <= 0.005 (F_web). A host needs S ~ 1 (G1 forces S_host >= 0.88 / 0.82). So no kernel and no tau works: the gap is
about 30x.

**Graded run (exponential kernel).**

| | canonical | alt |
|---|---|---|
| tau_gal (largest tau with G1 PASS) | 0.466 t0 = 6.55 Gyr | 0.590 t0 = 8.30 Gyr |
| S_host | 0.883 | 0.816 |
| G1 at tau_gal | Z +0.0561 (line 0.057), rms 0.14574 (line 0.14575) | Z +0.0476, rms 0.14242 (line 0.14247) |
| **W1 r at tau_gal** | **75.39** (line 1.072) | **78.77** |
| F_web max | 1.006 (line 0.005) | 0.933 |

Memory slightly RAISES the web phantom at small tau, because the past web phantom was larger (r 78.8 / 94.3 at
tau = 0.1 t0).

Reported only (not a scan used for anything):

| tau / t0 | G1 canonical | r canonical | G1 alt | r alt |
|---|---|---|---|---|
| 1 | FAIL (Z +0.127) | 41.7 | FAIL (Z +0.104) | 49.7 |
| 10 | FAIL (Z +0.361) | 3.19 | FAIL (Z +0.353) | 3.51 |
| 100 | FAIL (Z +0.423) | 1.167 | FAIL (Z +0.422) | 1.187 |

Even at tau = 100 t0, where galaxies are essentially Newtonian, the web sits above the line.

I1's other rows equal the plain law's: X-COP, groups, ellipticals, UDGs, dSphs and KiDS FAIL. The memory touches
static hosts only through S_host.

## I3: a0 memory is too small and has the wrong sign

**Built z_f (graded, Delta_c 18 pi^2; Omega_m 0.334, H0 65 from the solver's background).** Medians are the same on
both footings:

| Class | z_f |
|---|---|
| SPARC | 12.1 |
| ellipticals | 16.0 |
| X-COP | 3.70 |
| groups | 1.87 |
| Coma UDGs | 10.7 |
| dSphs | 20-42 |
| KiDS early / late | 1.98 / 1.48 |

Almost every system formed where a0(z_f)/a0(0) = 0.91-0.94, which lowers the boost.

| Row | canonical | alt | L0 (GB1) canonical / alt |
|---|---|---|---|
| G1 SPARC | PASS Z +0.041 | PASS Z +0.013 | +0.027 / -0.001 |
| G2 X-COP | FAIL +0.483 | FAIL +0.450 | +0.468 / +0.435 |
| G3 groups | FAIL 0, 0 of 20 | FAIL 0, 0 | 0, 0 |
| G4 ellipticals | FAIL +0.220 | FAIL +0.199 | +0.210 / +0.189 |
| G5 Coma UDGs | FAIL +1.140 (4.35 sigma_U) | FAIL +1.097 (4.19) | |
| G6 dSph | FAIL (bright M31 +0.205 [+0.084, +0.398]) | FAIL | |
| G7 KiDS | FAIL R +0.159 (2.47 sigma) | FAIL | |
| G8 | PASS 0.192 | PASS 0.173 | |
| W1 | FAIL 74.7 | FAIL 89.4 | |

Reported brackets:
- Turnaround Delta_c 5.55: same labels.
- Envelope top r_z 1.21 everywhere, the most favourable: X-COP +0.434 / +0.401, groups <= 1 of 20, UDGs +1.08 / +1.04.
  It still fails G2-G7.
- The deep-MOND ceiling 0.5 log10 1.21 = 0.041 dex stands.

## I4: a history charge cannot fit the hot classes, even with its history free

- **Web.** The linear web is unbound and carries no charge, so r = 74.7 / 89.4: W1 FAIL.
- **Residue arm, brackets.** m = mu N_eff is not carried by any class.
  - **X-COP:**

    | N_eff | canonical (mean, rms) | alt (mean, rms) |
    |---|---|---|
    | 8 | +0.075, 0.123 | +0.037, 0.105 |
    | 16 | -0.066, 0.119 | -0.105, 0.144 |

    No N_eff reaches the rms line 0.10: the profile SHAPE fails before the amplitude. The m that zeroes the mean is
    11.6 / 9.6.
  - **Groups:** at most 5 of 20 pass at any N_eff in 1-16, on either footing (16 needed). m needed 3.7 / 3.0.
  - **Coma UDGs:** m needed 189 / 154. The SPARC progenitors with M* in the UDG range (log 7.70-8.39, N 15) give
    mu = 1/(1 - f_gas) of median 4.86, 84th percentile 5.92, max 16.5.
    - Canonical: FAIL at every value, best +0.526 = 2.006 sigma_U against 2.
    - Alt: PASS only at the single most gas-rich progenitor (+0.481, 1.84 sigma_U).
  - **Brackets of the cold anchors:**
    - G1 SPARC passes only at N_eff = 1 (N_eff 2 gives Z -0.079 / -0.110). Any merger history in discs breaks SPARC.
    - G6 dSph fails at N_eff 1 and 2.
    - G4 ellipticals pass at N_eff 2 (+0.127 / +0.101).
    - G7 KiDS passes only for (early 2, late 1).
- **Reading.** The needed charge ratios (X-COP ~10, groups ~3, UDGs ~150-190, SPARC exactly 1) are DX1's ~100x spread
  again, now as an assembly history. The history would have to be chosen class by class, and X-COP's and groups'
  scatter fails even then.

## MUTATE (fa3_MUTATE.*)

| Twin | Result | Bites? |
|---|---|---|
| I1 M1 planted growing web source W ~ t^4, tau 10 t0 | r 1.239 / 1.266, W1 FAIL | **NO, as frozen** (needed W1 PASS) |
| I1 M2 Newton | G1 FAIL (Z +0.431) | yes |
| I3 M1 planted r_z = (1 + z_f)^2 | X-COP mean moves -0.583 / -0.589 | yes |
| I4 M1 planted N_eff 8 everywhere | G1 FAIL (Z -0.321 / -0.357) | yes |

Overall MUTATE exits 1, because I1 M1 did not bite as frozen.
- Post-freeze reading, not a regrade: the main run at the same tau = 10 t0 gives r 3.19 / 3.51. The planted growing
  history lowers r 2.6-2.8x, so the memory machinery responds to the sign of the source's history. The planted
  exponent and tau were too weak to cross 1.072. That was a design slip in the twin.
- I1's FAIL does not rest on this twin. It rests on KA2/K1 (exact replay), the measured theorem inputs, and r >= 1.17
  at every tau in the reported table.

## Disclosed

1. **RSS line missed.** The frozen compute line was "under 1 GB RSS". ru_maxrss read 1.87 GB (main) / 1.75 GB
   (MUTATE), while macOS's peak memory footprint was 0.65 / 0.64 GB. The script keeps one footing's ten web snapshots
   at a time (float32). The first two runs crashed on loader bugs (GB1's row printer lies past its main cut; KiDS
   features are raw dicts) before any label and are overwritten. No number depends on this.
2. **The I1 host model is generous to the candidate.** Each host is taken to have held its present phantom since
   t = 0, and KiDS lenses are taken at t0. The web holds each snapshot back piecewise-constant. This UNDER-states the
   web's memory phantom, so r is a lower bound.
3. **I1 graded one kernel family (exponential).** The kernel-free statement rests on the two measured inputs, not on a
   proof over all kernels in Lean.
   - Non-stationary kernels: an expansion-keyed rate Gamma(theta) is WL1's door. A signed derivative kernel cannot
     track H(2 - f) and breaks rotating discs.
4. **I3 z_f uses the solver's Omega_m 0.334 (baryons + the target cold component).** A baryon-only background raises
   every z_f, which pushes r_z further onto the 0.91 plateau: the same sign.
5. **I4 G8** takes mu = N_eff = 1 for the Sun (stated in the criteria). The UDG progenitor pool needed no widening.
6. Everything is static plus the linear web. None of the three has field equations, a well-posedness check or a causal
   analysis beyond IDEAS.md's statement (I1: hyperbolic along n, with the leaf-elliptic mode inherited).

## What this lane closes

- Memory classes acting on the law's phantom (I1) cannot make the web differ from hosts. The web's own past phantom is
  larger, and hosts can never borrow more than a0/|W| of theirs.
- a0 history (I3) moves offsets by <= 0.04 dex, mostly downward.
- A conserved history charge (I4) needs DX1's 100x spread as an assembly history. It fails the X-COP and group scatter
  even when that history is free, and it leaves the web untouched.

Both walls stand: the residue and the CMB-lensing shape. Kappa = 1/2 FITTED; not theory closed.
