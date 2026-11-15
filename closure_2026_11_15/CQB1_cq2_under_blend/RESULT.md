# CQB1_cq2_under_blend: CQ2's sealed DR4 wide-binary prediction under the adopted Pi^6 blend

**LABEL [canonical]: MARGIN HOLDS, UNCHANGED** (min Sigma/b over the frozen region 6.38e4; 3.00e4 after the
independent-estimate factor)

**LABEL [alt]: MARGIN HOLDS, UNCHANGED** (min Sigma/b 4.90e4; 2.34e4 after the factor)

kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

Criteria: `FROZEN_CRITERIA.md`, commit 37f878538f, committed alone before any script or number. Commissioned by item Q6
of `prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-15b_DR4_OPEN_GAPS.md`. Pre-data. The seal
(`cq_lanes_2026_11_04/CQ2_v3s_dr4_seal/`) is not edited; `git status --short` on its folder prints nothing.

## Answer

Yes, on both footings, and with nothing to recompute. The blend F = gamma_L b^2 f(Sigma/b) is identical to the raw
stiffness (F, F', F'' and QX17D's stress term Sigma F') wherever Sigma >= b. Everywhere CQ2's solution lives, Sigma is
at least 4.9e4 times b. So the static equations CQ2 solved are the same equations under the blend on an open set
covering that whole region, and CQ2's solution is a solution of the blended action with the same numbers.
The sealed prediction stands as printed: screened and Newtonian, gamma_r - 1 = 4.450e-05 (canonical) and
4.013e-05 (alt) at 30 kAU. Both of CQ2's readings carry: V3S-REST (static hedgehog) and V3S-MOVE (gamma_r = 1).

## What Sigma and b are (step 2)

| quantity | how it is fixed | canonical | alt |
|---|---|---|---|
| rho_DE = a0^2 / (kappa^2 c^2 G), kappa = 1/2 (U1, this lane's SI constants) | a0 law | 5.842e-27 kg/m^3 = 8.633e-08 Msun/pc^3 | 8.533e-27 kg/m^3 = 1.261e-07 Msun/pc^3 |
| b as the blend's own lanes use it (QX19: G = c = 1, b = s^2/2 = 4 (a0/c^2)^2) | U2 | 4.3387e-54 m^-2 | 6.3366e-54 m^-2 |
| G rho_DE / c^2 from U1 | U2 | same, rel 0 | same, rel 1.8e-16 |
| Galactic phantom, box minimum (X3 D2, R 7.2-9.2 kpc, \|z\| <= 1 kpc) | R1 | 0.005506 Msun/pc^3 | 0.006178 Msun/pc^3 |
| minus 2.5 x the deepest 1 Msun lobe (worst row) | R1 | 0.005505 | 0.006177 |
| Galactic phantom at the Sun (near zone, smaller of X3's two values) | R2 | 0.0447 | 0.0449 |
| **min Sigma/b over R1 and R2** | S2 | **6.377e4** | **4.900e4** |
| Sigma/b at the Sun | S2 | 5.18e5 | 3.56e5 |
| independent SI estimate, worst factor from X3 (U4) | U4 | 2.12 | 2.09 |
| **min Sigma/b after that factor** | label gate | **3.00e4** | **2.34e4** |

Why Sigma/b = rho_ph / rho_DE (U3). In CQ2's static weak-field limit, (L) reads lap Phi = K rho + div p with p = K P and
K = 4 pi (G = c = 1). So Sigma = D.P = div P = div p / K = G rho_ph / c^2, with rho_ph = div p_SI / (4 pi G). U2 shows
b = rho_DE in the same geometric normalisation, G rho_DE / c^2. The D.P that X3 and CQ2 report in Msun/pc^3 is
div p_SI / (4 pi G) / (Msun/pc^3); that line is pinned verbatim in X3's script. X3's Msun/pc^3 constant agrees with
this lane's to 3.0e-5. So Sigma/b is the phantom density over rho_DE, in the same units. TC1 N2 states the same
relation for AC2q: Sigma/X = 2 + rho_ph/rho_DE.

Independent check (U4). This lane's own code computes a spherical Hernquist Milky Way (Mb 4-8e10 Msun, aH 2-4 kpc) with
simple-nu QUMOND, in SI. The phantom's box minimum comes out at 0.0038-0.0054 (canonical; X3 0.0055) and 0.0042-0.0061
(alt; X3 0.0062) Msun/pc^3. The in-plane value at the Sun comes out at 0.050-0.095 (X3 0.0447) and 0.057-0.107
(X3 0.0514), with an assumed local baryon density of 0.08 Msun/pc^3. The worst disagreement is a factor of 2.1. A
unit or solver slip would have to exceed the margin, about 2e4, to move the label.

## Why the equations are the same (S1, exact)

The lane builds f from AC21 iter_6's exact rational f'' pieces (form.json, sha256 77a58d28fb...), integrating in sympy:

- f(1) = 1/2, f'(1) = 1, f''(1-) = 1, f'''(1-) = f''''(1-) = 0, and f'' = 1 above 1. So f = q^2/2 exactly for
  q >= 1.
- For Sigma >= b, the blend gives F = Sigma^2/2, F' = Sigma, F'' = 1 and dF/db = 0. Sigma F' = 2F, so QX17D's R2 stress
  term equals the raw one there.
- On (0, 1/2], f = (122363904/44610575) q^6, as QX19 C6 states. The interior knots are C4 joins.

In CQ2's static limit the stiffness enters only as gamma_L grad F'(Sigma), with the constitutive factor 1 + gamma_L F'.
Both are identical on the open set {Sigma > b}, which contains the whole frozen region.

## The frozen region, checked piece by piece

- **R1, the Galactic environment over the DR4 volume.** CQ2's six K4 rows per footing (x_e 1.15 / 2.6; L* floor, 24,
  90 pc), each the box minimum of the Galactic phantom minus 2.5 Msun's deepest negative lobe. The lobes are 3.1e-7
  Msun/pc^3 or less per Msun, which changes Sigma by less than 1.5e-4 relative.
- **R2, the near zone.** The Galactic phantom at the Sun. Within the binary itself, the response is the hedgehog's
  divergence M/(2 pi L*^2 r), which is positive: +2.3e-4 Msun/pc^3 for 0.1 Msun at 30 kAU. A point mass's negative D.P
  starts at 24.9 pc, 171 times the widest DR4 separation (S3). So the binary only raises Sigma.
- **R3, the model's domain.** CQ2's linear response sits on an infinite uniform background, so R1's minimum bounds it
  everywhere.
- **S4, Galactic inputs.** x_e = g_obs/a0 is observed (1.778, 1.9 and 2.32 e-10 m/s^2), so the action cannot move it.
  rho_gal enters CQ2 only through the switch margin. Its stiffness dependence is X3's far-region estimate, 2.84e-7,
  times max f'' = 6.24, giving 1.8e-6 relative. The line is 1e-3.

## Checks and their mutations

| check | result | mutation (separate outputs) | mutation result |
|---|---|---|---|
| K0 inputs pinned (CQ2 cq2.py / cq2.json, form.json, X3 json) | PASS | none | none |
| KA1 CQ2 reproduced by its byte-identical copy (sha256 6fbf2abfe5...) | PASS: 980 numeric leaves of cq2.json, max rel 0.0; switch margin 7064, near zone +0.0449, gamma_r - 1 at 30 kAU 4.4497e-05 / 4.0133e-05; its K1-K7 all PASS; 26.8 s | M2 breaks the known answer | see KA2 |
| KA2 this lane's Route F copy vs CQ2 (s 1, 10, 30 kAU) | PASS, max rel 0.0 | **M2** L* floors swapped between footings | KA2 FAIL (rel 1.0e-1), both labels NOT EVALUABLE: **BITES** |
| U1 rho_DE in SI | PASS | none | none |
| U2 QX19's b = G rho_DE / c^2 | PASS, rel <= 1.8e-16 | **M3** 1/kappa^2 dropped | U2 FAIL (rel 0.75), both labels NOT EVALUABLE: **BITES** |
| U3 unit chain pinned; Msun/pc^3 constants agree | PASS (3.0e-5) | none | none |
| U4 independent phantom estimate within x10 | PASS (worst x2.12) | none | none |
| S1 blend = raw for q >= 1, exact | PASS | none | none |
| S3 near-zone sign | PASS | none | none |
| S4 Galactic inputs | PASS (1.8e-6) | none | none |
| KC CHANGED-branch method reduces to raw for q >= 1; f' inverse exact | PASS (1.8e-15, 4.4e-16) | none | none |
| label | UNCHANGED / UNCHANGED | **M1** b raised so the region's minimum sits at q = 1/4 | MARGIN FAILS / MARGIN FAILS: **BITES** |
| label | UNCHANGED / UNCHANGED | **M1b** the same with the minimum at q = 3/4 | MARGIN FAILS / MARGIN FAILS: **BITES** |

All four MUTATE runs exit 1, as frozen. The main run exits 0.

What the margin mutations show (mutations only, not a result). If CQ2's region had sat inside the blend layer, the
sealed numbers would not have stood. Under M1 the worst-case gamma_r - 1 at 30 kAU rises to 8.1e-5 / 7.9e-5, and under
M1b to 1.30e-4 / 1.38e-4: a factor of 1.8 to 3.4 above the seal. That is still under CQ2's NEWTONIAN line of 1e-3, and
at most 6.9e-3 of the DR4 error scale 0.02. The layer is soft in places: f'' dips to 0.0057 on [1/2, 1], against a
maximum of 6.24. So the blend is not harmless inside the layer. It simply never reaches CQ2's region, which sits
4.9e4 to 6.4e4 times above it.

## The lead's hand estimate: RIGHT

The estimate read: D.P about 0.0055-0.045 Msun/pc^3, rho_DE of order 1e-7 Msun/pc^3, Sigma/b of order 1e4-1e5, and
the blend equal to the raw form exactly. Each part checks out:

- D.P is 0.0055 / 0.0062 at the box minimum and 0.0447 / 0.0449 at the Sun.
- rho_DE is 8.6e-8 / 1.26e-7.
- min Sigma/b is 6.4e4 / 4.9e4. At the Sun it is 5.2e5 / 3.6e5, a little above the stated range.
- The estimate's premise, that Sigma and b are the same quantity in the same units, holds (U2, U3).
- The blend equals the raw form exactly on the region.

The grading rule (rho_DE within x3 of 1e-7, min Sigma/b within 10^3.5-10^5.5, both labels UNCHANGED, U2 and U3
passing) was written into the script after the criteria and before the run.

## Limits

- This lane checks only where CQ2's solution sits relative to the blend layer. It does not re-test CQ2's own model:
  the linear response about a uniform background, the Route F monopole, CW1's machinery, or X15's motion statement. Those
  carry over unchanged because the equations are unchanged on the region.
- The Galactic phantom values are X3's isolated MW-like disc model (H4 S5a). The independent check is a spherical
  estimate with assumed round inputs (Mb, aH, a local baryon density of 0.08 Msun/pc^3) and is good to a factor of
  about 2. The margin is 2.3e4 after that factor.
- The CHANGED-branch method (screened local inversion: spherical, monopole, with the MOND term only through the sealed
  F) was frozen in advance but is exercised only by the mutations. It is an approximation, not a solve of the blended
  3D equations.
- The blend's own limits stay as adopted: local-in-time well-posedness, spherical-3D tests only, power 6 not forced.
  None of them bears on this static check.

## Disclosures

- KA1 ran a byte-identical copy of CQ2's `cq2.py` from this folder, because the script writes its outputs next to
  itself. Running it in CQ2's folder would have overwritten the seal's files. The copy cannot carry this lane's header
  line, being byte-identical; neither can its outputs `cq2.out` / `cq2.json` / `cq2.time`.
- The reproduced `cq2.json` hashes differently from CQ2's (2b424eb6... vs a73f754c...). The only differing fields are
  the excluded `wall_s` and `peak_rss_gb`; every other leaf is identical. KA1 used 26.8 s, 1.68 GB `ru_maxrss` and
  0.42 GB peak physical footprint; no other python job above 2 GB was running.
- R2 uses the smaller of X3's H4 C3 minimum (0.0449, one value for both footings) and X3's at-Sun value for the footing.
  For alt that is 0.0449, not 0.0514.
- Written after the criteria, before the first run: the hand-estimate grading rule; U4's 41 x 41 box grid; the M1 / M1b
  b factors computed from the post-U4 margin; the local-inversion quadrature (400,001 log points from u = 1e-12, with
  the saturated tail added analytically).
- The record's float evaluation of f (QX19) carries about 1e-4 cancellation near q = 1 (TC1's note). This lane builds
  f exactly in sympy and evaluates it with shifted Horner polynomials: |f(1-) - 1/2| and |f'(1-) - 1| are 1e-12.

## Files

- `FROZEN_CRITERIA.md` (37f878538f)
- `cqb1.py` and its main outputs `cqb1.out` / `cqb1.json`
- `cqb1_MUTATE_{M1,M1b,M2,M3}.out` / `.json`
- `cq2.py` (byte-identical copy of CQ2's, sha256 6fbf2abfe5...) and its outputs here, `cq2.out` / `cq2.json` /
  `cq2.time`
- `RESULT.md`

Reproduce from this folder:

- `OMP_NUM_THREADS=1 nice -n 10 /usr/bin/time -l python3 -I -B cq2.py` (KA1, about 30 s)
- `OMP_NUM_THREADS=1 nice -n 10 python3 -I -B cqb1.py` (exit 0)
- `... cqb1.py --mutate M1`, `M1b`, `M2`, `M3` (each exits 1 when it bites)

kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.
