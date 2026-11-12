# FINAL-7 FROZEN CRITERIA: what the medium IS — the M5 hypothesis triage (2026-11-11)

TEST lane, quarantined. Relabels nothing, adopts nothing, not registered. kappa = 1/2 FITTED; not
theory closed. Footings graded separately, never pooled: canonical a0 = 9.3603e-11 m/s^2
(2888.4 (km/s)^2/kpc), alt a0 = 1.1312e-10 m/s^2 (3489.9 (km/s)^2/kpc). Cold dark energy is a
gravitating field component, never a particle. Nothing here says the data favour the framework. No
LCDM-calibrated machinery enters any verdict.

**Committed alone, before any FINAL-7 script exists and before any FINAL-7 number is computed.**

---

## 0. The question, and the two things it splits into

The crux check establishes that form B's *static* spherical halo must be carried by a stress whose
radial principal value is negative:

    Pi_ij = J(g) delta_ij - g_i g_j /(K(1+u)),   K = 4 pi G,  u = g/a0
    J(g)  = (a0^2/K)[u - ln(1+u)]
    Pi_rr + Pi_tt -> 0 as u -> 0        =>   sigma_r^2 = Pi_rr/rho_c -> -v_inf^2/2
                                              sigma_t^2 = Pi_tt/rho_c -> +v_inf^2/2
    v_inf^4 = G M_b a0

`sigma_r^2 < 0` is a **radial tension**, not a dispersion: for any f >= 0,
`P_r = int f v_r^2 d^3v >= 0` pointwise, so no kinetic medium (cold, warm, hot, collisional,
collisionless, anisotropic) can carry it. A medium with a shear modulus can.

M5's NO-GO has three hypotheses about the medium: **(i) LOCAL**, **(ii) MOMENTUM-CONSERVING
(medium alone)**, **(iii) NORMALLY SELF-GRAVITATING**. Since M5's class is empty, whatever does
the job must break at least one. FINAL-7 asks **which one it must break**, and whether that break is
compatible with MEDIUM_DESIGN's four properties:

1. conserved, and cold in the expanding universe at 5.41 x the baryons;
2. passes through itself and through gas (the Bullet's offset);
3. hot and at full share in clusters;
4. locked to the baryons in galaxies, with no second halo beside the law.

The sharpening is (2). A solid's configuration map is a **homeomorphism** (injective); two solid
halos that have passed through each other require a 2-to-1 map. So either there is a carrier of `Pi`
that interpenetrates, or the class of media is closed — and then `sigma_r^2 < 0` has to be read some
other way.

---

## 1. Pre-registered kills (written before any number; each is the expected outcome)

| # | Kill | Expectation |
|---|---|---|
| K1 | **The solid is not elastic.** Its own solution strains it by `|u| >> 1` | FIRES |
| K2 | **The Bullet.** No material continuum interpenetrates; and at 4700 km/s it yields | FIRES |
| K3 | **Property 1.** A carrier with no material identity (a field) has no conserved cold rest mass | FIRES |
| K4 | **Property 3.** A field is not hot; the cluster dispersion needs matter to carry it | FIRES |
| K5 | **Locality is forced.** Replacing `Pi(g)` by `Pi(g_L)` (field smoothed on scale L) destroys the equilibrium | FIRES |
| K6 | **No ghost / no superluminal.** Both sound speeds stay real and below `c` on the window | **HOLDS** |
| K7 | **The multi-stream escape.** N cosmologically mixed, mutually transparent elastic constituents does not rescue interpenetration | FIRES |

K6 is the gate the brief asks to grade; K1–K5, K7 are the triage. I expect the medium to die with
K6 holding: **the elastic solid is dynamically healthy and physically impossible.**

---

## 2. Fixed inputs

- Units: kpc, km/s, M☉. `G = 4.30091e-6 kpc (km/s)^2 / Msun`, `K = 4 pi G`, `c = 2.99792458e5 km/s`.
- Masses `log10 M_b = 9.40, 10.45, 10.70, 10.90` (the record's four). `r_M = sqrt(G M_b/a0)`.
- Profiles: point mass; Plummer `b = R50/1.3048`; Hernquist `a = R50/(1+sqrt2)`;
  `R50 = 0.10 kpc (M/Msun)^0.14 (1 + M/3.98e10)^0.25` (SCS2's transcription; as-read, not re-sourced).
- Law (spherical, exact): `g^2/(g+a0) = g_N`, `g = (g_N + sqrt(g_N^2 + 4 a0 g_N))/2`;
  `rho_c = [2(g-g_N)/r + g' - g_N']/K` with `g' = (dg/dg_N) g_N'`,
  `dg/dg_N = (1 + (g_N + 2 a0)/sqrt(g_N^2 + 4 a0 g_N))/2`.
- Reference density `rho_ref` (for the mass-conserving map): primary `33.92 Msun/kpc^3`
  (5.41 x Omega_b x rho_crit, Omega_b = 0.049, h = 0.679); brackets at z = 2, 5, 10
  (x27, x216, x1331); extreme bracket z = 1100 used only inside the M5 arm.
- Graded window: `r/r_M in [0.2, 60]`, 80 log-spaced points; the mass-conserving map
  `R(r) = [3 M_c(<r)/(4 pi rho_ref)]^{1/3}`, `u_rr = 1 - dR/dr`, `u_tt = 1 - R/r`.
- Lines: SPARC rms in g = 0.0660 canonical / 0.0658 alt; sound-speed line `c`.
- Bullet (transcribed from DB1 / RB1, used as-is): `v = 4700 km/s`; RB1 gate 4 puts the lensing
  peak with the galaxies (model 14 / 10 kpc); the gas sits hundreds of kpc away;
  DB1 tests (i) `Sigma_c >= 3 x` swept ICM column, (ii) `G Sigma_c^2 >= rho_ICM v^2`.
- Cluster regime (S3 analogue): `log10 M_b = 13.40, 14.00, 14.60`, `sigma_v = 1000 km/s`.

## 3. Conventions frozen here (they decide signs, so they are binding)

- Cauchy stress is **tensile-positive**; static balance in spherical symmetry reads
  `(div sigma)_r = d sigma_rr/dr + (2/r)(sigma_rr - sigma_tt) = + rho_c g`, with `g > 0` the
  inward field magnitude. `KA9` below fixes which sign of `Pi` is the material stress.
- `sigma_r^2 := Pi_rr/rho_c` and `sigma_t^2 := Pi_tt/rho_c` are the *principal values per unit
  medium density*, called "dispersions" only by abuse of language.

---

## 4. Items, in order; every gate that does not depend on a fired structural gate is still run

### Q0. Known answers (all must pass before any row is graded)

- **KA1.** `(Pi_rr + Pi_tt)/J -> +(2/3) u` as `u -> 0`; check at u = 1e-1…1e-4 (rel. err → 0 as O(u)).
- **KA2.** `sigma_r^2/(v_inf^2/2) -> -1`, `sigma_t^2/(v_inf^2/2) -> +1` at x = 1e3…1e6 (residual → 0 as 1/x).
- **KA3.** Point-mass `M_c = M_b (sqrt(1+4x^2)-1)/2` vs numerical integral of `rho_c` (1e-6).
- **KA4.** Modulus-inversion identities on 200 random draws (1e-12).
- **KA5.** Navier–Cauchy: `s^2 = -c_L^2 k^2` (longitudinal), `s^2 = -c_T^2 k^2` (transverse), symbolically.
- **KA6.** Map mass conservation: Eulerian mass = `rho_ref` x Lagrangian volume (1e-8).
- **KA7.** Newtonian limit (`a0 x 1e-6`, `x 1e-9`): residual falls as `a0`, `< 1e-4`.
- **KA8.** `2W = sigma:u` for a quadratic isotropic energy (symbolic).
- **KA9.** Which sign is the material stress: `div(+/-Pi)/(rho_c g)` on all 24 rows (needs +1).
- **KA10 (NEW — the Maxwell signature).** In the deep field the law's stress must reduce to the
  Maxwell/canonical stress of a field carrying energy density `J`:

      sigma = -Pi  ->  diag(+J, -J, -J)   (radial tension = energy density)

  Test the two invariants: (a) the Maxwell tension ratio
  `eps/(2J) -> 1` with `eps := g^2/(K(1+u))`; (b) the anisotropy ratio
  `Pi_rr/(-Pi_tt) -> 1`. Report the leading correction (expected O(u)).

### Q1. The sound speeds — THE GRADE THE BRIEF ASKS FOR

With `sigma = -Pi` and the mass-conserving strain (`mu_s`, `lambda` by exact inversion):

    c_T^2 = mu_s/rho_c ,  c_L^2 = (lambda + 2 mu_s)/rho_c

24 rows, both footings, window `[0.2, 60] r_M`:

- **Q1a** FIRES if any row has `c_T^2 < 0` or `c_L^2 < 0` anywhere.
- **Q1b** FIRES if any row has `|c_T| > c` or `|c_L| > c` anywhere.
- **Q1c (new, structural).** Report the exact pole of `lambda + 2 mu_s` and the branch structure of the
  family: `3 lambda + 2 mu_s = J/(7y/3 - 3)` in the deep field, so the family is mechanically
  stable only for `y > 9/7`; report the shell `6/5 < y < 9/7` (where `c_L^2 < 0`) and the radii
  at which it falls, against the physical halo edge (`rho_bar = 200 rho_ref`).
- **Q1d (new, closure).** Closed forms: `c_T^2 = (3/(2n)) v_inf^2 / y` and
  `c_L^2 = ((12 - 10n)/(3(3-7n/3)))... ` — report the deep-field pair and the ratio
  `c_L^2/c_T^2 -> 10/7`, checked numerically at `x = 60`.
- **Q1e (new, the physical reading).** Report `c_T^2 / sigma_t^2 = 3/(2y)` — the elastic sound speed
  is *below* the dispersion the halo must carry, which is the melt condition used in Q4.

### Q2. WHICH HYPOTHESIS MUST BREAK — three arms, each a complete candidate family

For each arm: does the resulting carrier satisfy all four properties? (A medium that satisfies all four
is the answer to the brief; a medium that fails any one is not.)

- **Arm N — drop (i) LOCAL.** Representative nonlocal family: `sigma = -Pi(g_L)` where `g_L` is the
  Newtonian field of the baryons smoothed on a scale `L`. Grade: rms dex of the implied halo density
  against the law, on the window, at the four masses, for `L = 0, 10, 50, 200 kpc`; line 0.066 dex.
  Structural grade: does nonlocality touch (2) at all?
- **Arm P — drop (ii) MOMENTUM-CONSERVING (medium alone).** Two sub-cases.
  - *P1, contact.* The medium exchanges momentum with the baryons through a direct coupling. Recompute
    MEDIUM_DESIGN section 3's two kills from scratch: (a) the opacity `kappa = pi G/a0` needed for the
    contact to switch on where the mean enclosed acceleration is a0, the mean free path at z = 1100 and
    the drag/H ratio at z = 1100 and z = 3400; (b) the Bullet's gas column in optical depths.
  - *P2, no material identity.* The carrier is a sourced field, not a substance: `-Pi = T[phi]`, `grad phi = g`.
    Grade (2) by superposition; grade (1) by whether the carrier's charge is conserved: compute
    `M_c(<r)/M_b` against the 5.41 budget and its asymptotic growth.
- **Arm S — drop (iii) NORMALLY SELF-GRAVITATING** (tethered / cancelled self-gravity). Grade (1)+(3):
  a component that does not gravitate cannot be "at full share" in clusters; compute the implied lensing
  deficit at the KiDS radii used by AMT1 (272 kpc, 637 kpc). Grade (2) structurally.

**Q2 rule.** The answer to the brief's question is the **unique hypothesis whose being broken is
compatible with property (2)**, because (2) is the sharpest test and it is the only property that
constrains the ontology of the carrier. If more than one arm survives (1)–(4), NO VERDICT.

### Q3. The Bullet (pre-registered to kill)

- **Q3a, structural.** Homeomorphism vs the interpenetrated mass the data require (>= `M_c,sub`).
- **Q3b, dynamical.** Elastic Mach number `v/|c_T|` and yield parameter `Y = rho_c v^2/|mu_s|` at
  `v = 4700 km/s` in the cluster regime.
- **Q3c, the blind spot (reported, must be flagged).** DB1's two tests: does the solid pass them?
- **Q3 rule.** FIRES unless the medium passes through gas *and* the other cluster's medium and stays
  with the galaxies.

### Q4. What `sigma_r^2 < 0` then means (reported)

- The Maxwell identification (KA10) and what it makes the "cold component": polarization charge, not
  rest mass. Total "mass" of the settled halo: `M_c(<r) = (g-g_N) r^2/G ~ r` — divergent, so no
  conserved 5.41 x baryon substance is being carried.
- Kinetic reading: the required `P_r = rho_c sigma_r^2 < 0` needs `f < 0` on a set of measure
  `|sigma_r^2|`; quantify the deficit in (km/s)^2 and as a fraction of `v_inf^2`.
- Cluster melt (Q1e) and the amount cap (AMT1: 41.5 / 97.8 M_b demanded vs 5.41 available).

---

## 5. MUTATE arms (each must bite; outputs `fin7_MUTATE_<arm>.out/.json`)

- **M1 (sign).** Use `sigma = +Pi` (the pre-A1 reading): equilibrium must fail and `c_T^2 < 0` everywhere.
- **M2 (no shear).** Replace `Pi` by an isotropic pressure `P = J` (the kinetic/isothermal reading):
  the halo must be consistent in the deep field *by construction* — so the bite must come from
  elsewhere: show that, there, `mu_s == 0` identically (no transverse mode, M5's S4 disease returns)
  and that the anisotropy `Pi_rr - Pi_tt = -eps` is left uncarried, i.e. it is not the law's stress.
- **M3 (no law).** Newtonian limit: halo and moduli vanish; the gate must fail.
- **M4 (no mass conservation).** Drop C3, integrate the energy ODE from the energy condition alone:
  the branch must fold or be rigid.
- **M5 (the multi-stream escape).** N mutually transparent, cosmologically mixed identical elastic
  constituents: show the passage still forces each constituent's map through a fold (Jacobian zero),
  i.e. the escape does not rescue (2).

Rule: an arm BITES only if the planted defect is detected by the gate it targets.

## 6. Labels (vocabulary frozen)

Per footing: **NO MEDIUM — CLOSED AT <item>** / **MEDIUM FOUND — <which>** / **NO VERDICT**.
Both footings always reported; never "passes".

## 7. Process

`fin7.py` writes `fin7.out` and `fin7.json`; arms write `fin7_MUTATE_*.out/.json`. One thread,
`nice -n 10`, no downloads. Later changes go in `AMENDMENT_An.md`, each committed alone, marked post
hoc if any number has been seen.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
