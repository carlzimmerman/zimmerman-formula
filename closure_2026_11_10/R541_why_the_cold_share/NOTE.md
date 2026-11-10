# R541 NOTE: why is the cold share 5.41? NOT DERIVED. In the adopted action it is FREE (an integration constant)

2026-11-10. Owner's question: "why 5.41?". Five parallel parts (record, action, the law's own halo, literature,
relation hunt), collected and checked by one lead session.

**This is a note, not a graded lane.** No criteria were committed before the numbers. Parts C and E wrote their
candidate list and search space to a file before computing, but no commit proves that order. The note adopts nothing,
relabels nothing and registers nothing. Footings are never pooled. kappa = 1/2 is FITTED; the theory is not closed;
nothing here says the data favour this framework.

## The answer

1. 5.41 is what the acoustic peaks of the CMB need. It is fitted (lane F1A), and it is the standard cosmic ratio of
   cold density to baryon density refitted on this framework's background (the standard fit gives 5.364 +- 0.065).
2. In the adopted action the cosmic amount of cold dark energy is an integration constant. No equation of the action
   sets it. a0 and kappa do not appear in the background equations, so no relation ties 5.41 to the law.
3. The law's own halo does not produce 5.41 under any boundary rule the framework owns. In bound systems 5.41 enters
   only as a cap put in by hand.
4. No simple expression in the framework's own quantities matches 5.41 more often than chance.
5. No published theory of a particle-free dust field fixes this amount either (provisional: abstract look-ups).

So the framework has two fitted numbers, 1/2 and 5.41, and 5.41 is an initial condition of the field. That is where
the standard cosmological model stands with the same ratio. A value for it needs a new ingredient (section 7), and
none has been tested.

## 1. Where the number comes from (part A, quotes re-read by the lead)

- Source: `closure_2026_11_07/F1A_primary_cmb_audit/RESULT.md:22`: "R = omega_d / omega_b at the B2 best fit |
  5.410 | 5.412" (canonical | alt). Line 23 gives the fit: omega_b 0.02236 / 0.02234, omega_d 0.1209, h 0.674,
  n_s 0.967, tau 0.070 / 0.073. The data are Planck PR4 and ACT DR6 high-multipole spectra.
- No uncertainty on R is stated anywhere in the record: the fit is a best fit with no posterior. Part E falls back on
  the Planck 2018 errors, 1.2 %, 0.065.
- Pinning the optical depth does not move it: `closure_2026_11_09/CO2_form_b_amplitude_pinned/RESULT.md:16`, "The cold
  amount does not move (5.411 / 5.412 times the baryons)". CO1 carries it as "fitted, not derived"
  (`closure_2026_11_09/CO1_form_b_cosmology_computed/RESULT.md:37`).
- The standard value the record uses: 0.1200 / 0.02237 = 5.364 +- 0.065
  (`campaign_fresh_gravity/CFG360_baryon_tie/FROZEN_CRITERIA.md:11`). 5.41 is 0.9 % above it, about 0.7 of that width.
- Every later use (RB1's cap in hot systems, PD1, CO1's cluster share, MK1, MK2) reuses this one number. It was never
  fitted a second time.
- Earlier attempts in the record, all negative:
  - "Shift-charge road (A2, proved): the cold amount is a free integration constant"
    (`campaign_fresh_gravity/STANDING_2026-09-29.md:551`).
  - CFG360 baryon tie: "Verdict: NO-GO. The cold amount stays a free number"
    (`campaign_fresh_gravity/CFG360_baryon_tie/README.md:7`).
  - CFG360-DE, five mechanism classes: "PARTIAL, no mechanism: amount never fixed with 0 constants"
    (`campaign_fresh_gravity/LEDGER.md:334`).
  - CFG642, a formula search over the framework's constants at named epochs: CHANCE-LEVEL
    (`campaign_fresh_gravity/LEDGER.md:427`).
  - C2: "I0 is the conserved shift charge, an initial datum. Nothing in the action fixes it"
    (`covariant_push_2026_10_22/C2_aest_cosmology/README.md:12`).
  - TK1: the static-well charge is "short of 5.41 M_b at 8 of 8 points"
    (`closure_2026_11_10/TK1_expansion_keyed_dust/RESULT.md:36`).
  - Listed by the sweep and not re-read by the lead: CFG723 route C, the opus_48 Door E abundance pin, CMB2,
    CFG338 / CFG339.

## 2. The action: FREE (part B, `part_B_action/`, re-run by the lead)

Action (A) of PAPER70 (`qwen_claude_field_theory/papers_2026/PAPER70_field_equations_closure_2026.tex:54-57`) in a
homogeneous expanding background with P = 0:

- The stiffness term drops out (F(0) = F'(0) = 0) and W(0) = 0. The action then depends on the clock tau only through
  Q = tau-dot / N, so tau is cyclic.
- The shift symmetry tau -> tau + const gives the first integral a^3 mu_K^2 (Q - 1) / K = C. This is the record's
  own reduction: "(E3): a^3 mu_K^2 (Q-1)/K = const ... J, a0 and gamma_L absent (Y = 0, Pi = 0)"
  (`closure_2026_11_06/QX17_covariant_field_equations/RESULT.md:107`).
- On shell the density is rho_K = C / a^3 + K C^2 / (2 mu_K^2 a^6). At late times R = C / rho_b0.
- The Friedmann constraint only trades C for H. b = rho_DE sits in F, which vanishes here. a0 sits in W, which
  vanishes at P = 0. rho_DE enters only as Lambda. The relation holds exactly, so there is no attractor.
- The record fits the constant: "I0 = 4.037e-8 Mpc^-2 per footing"
  (`fable52_push/MK1_one_dust_constant/RESULT.md:112`), and "the 5.41 (fitted)"
  (`closure_2026_11_10/THEORY_ASSEMBLED_2026-11-10.md:27`).

No late process can change it. For P tangent to the clock's slices, Pi = D_i P^i exactly, a pure divergence on each
slice, and the polarization part of the charge is likewise a slice divergence (both checked symbolically with a
general lapse). The halo the law builds around baryons therefore carries no net charge: it moves charge, and what it
gains inside is balanced outside or through the boundary. Collapse, the switch and screening can only move charge
around. With baryon number also conserved, R is fixed once both are set: it is a primordial initial condition of this
action.

Relation to kappa or a0: none. a0 enters only through W, kappa only through a0, and W is identically zero in the
background.

`frw_charge.py` prints each of these checks; `frw_charge.out` is its output.

## 3. The law's own halo: NO (part C, `part_C_halo/`, re-run by the lead, output identical)

The law as the record writes it, mu(x) = x / (1 + x) (`closure_2026_11_10/THEORY_ASSEMBLED_2026-11-10.md:16`), so
g = g_N / 2 + sqrt(g_N^2 / 4 + a0 g_N).

- **Where the cap sits.** Halo / baryons = g / g_N - 1. With this mu that equals R exactly where g = a0 / R, that is
  g = 0.1848 a0 = 1.730e-11 m/s^2 (canonical; 2.091e-11 alt), g_N = a0 / (R (R + 1)). This is an identity of the
  interpolation function and holds for any spherical profile, so it carries no information. The cap radius is
  5.889 sqrt(G M / a0): 0.7 kpc at 1e7 solar masses, 7,187 kpc at 1e15; 0.085 to 1.83 of R200.
- **Is a0 / 5.41 a scale the framework owns?** Twelve fixed candidates and four mass-dependent ones were listed in
  `candidates_written_first.txt` before any ratio was computed. None lands within a few percent. Nearest, as ratios
  to the cap acceleration: a0 / 2 pi 0.861, a0 / 4 1.353, c H0 Omega_m / 2 5.97, c H0 / 2 pi 6.02; a typical external
  field (0.01 to 0.03 a0) 0.05 to 0.16. The mass-dependent ones match at one mass each.
- **Truncating the halo by a native rule instead.** The ratio runs with mass under every rule and is far above 5.41:

  | rule | halo / baryons at 1e10 | at 1e14 | census mean, bound baryons |
  |---|---|---|---|
  | zero-gravity radius (law against dark-energy repulsion) | 490 | 49 | 272 |
  | half the Lagrangian separation | 151 | 32 | 98 |
  | half the separation, census fractions | 307 | 95 | 208 |
  | turnaround radius (FLD1) | 48.7 | 10.1 | 31 |

  The census weights (12 % galaxies with their surrounding gas, 4 % hot gas in groups and clusters, 84 % diffuse)
  were quoted from memory by the part and not re-checked. They do not change the conclusion.
- **Cosmic version.** The law around the mean baryon density gives a ratio of 5.41 at r = 745 Mpc (900 Mpc alt):
  0.168 of c / H0, 5.1 sound horizons, 6.65 horizons at equality. It matches no native length.

## 4. Relation hunt: chance level (part E, `part_E_hunt/`, re-run by the lead, output identical)

The search space is in `FROZEN_SEARCH_SPACE.md`. Target 5.410 (canonical), width 0.065 (Planck fallback). Expected
counts are the mean over control targets from 4.4 to 6.4.

| family | unique values | within 1 width: found / expected | within 2 widths: found / expected |
|---|---|---|---|
| pure numbers (2, 3, 4, pi, and the factors of the framework's law) | 1,084 | 5 / 5.35 (p 0.62) | 11 / 10.81 (p 0.52) |
| with fitted cosmological inputs | 2,856 | 3 / 5.35 (p 0.90) | 10 / 10.97 (p 0.66) |
| expressions that restate the fit, counted apart | 615 | 0 / 0.4 | 0 / 0.81 |

No excess. The simplest matches are 4 + sqrt(2) = 5.414, 8 pi / 3 - 3 = 5.378 and pi sqrt(3) = 5.441. Nothing in the
framework produces any of them; at this width each is a coincidence. The search was not blind (its author knew some
near values), which is why it is graded on control counts. This agrees with CFG642's CHANCE-LEVEL.

The law and the share have no parameter in common except through flatness, so the two fitted relations imply nothing
further that could have failed. Restated numbers: cold over dark energy density 0.389; the two are equal at
z = 0.370; a0 / (c H0) = 0.143. `hunt.json` also holds a cross-check from galaxy-fitted kappa values plus flatness; it
has no power.

## 5. Literature (part D): nothing fixes it. PROVISIONAL

Web look-ups of abstracts and paper text, not downloads. The lead re-read three abstracts (marked *); the rest stand
as the part reported them.

- Skordis and Zlosnik 2021 (arXiv:2007.00082), Blanchet and Skordis 2024 (arXiv:2404.06584 *, the nearest theory in
  kind: title and authors confirmed; the statement that the dust constant is set by initial conditions is in the
  paper body and was not re-read), mimetic dust (arXiv:1308.5410), Mukohyama 2009 (arXiv:0905.3563): in each the
  dust amount is a free integration constant or initial condition, set to match observation.
- Nearest thing to a mechanism: Chamseddine and Mukhanov, "Mimetic Dark Matter from Inflation", 9 January 2026
  (arXiv:2601.05931 *). A Gauss-Bonnet coupling makes the dust during inflation, with a density set by the Hubble
  rate at the end of inflation. The amount still rests on a chosen coupling and nothing ties it to baryons.
- Verlinde 2016 (arXiv:1611.02269): Omega_D^2 = (4/3) Omega_B, a ratio near 5.2; the part reports that the author
  himself warns against reading much into it.
- Banerjee, Brzeminski and Hook 2024 (arXiv:2410.22412 *): the ratio 5.36 is reproduced for N = 8 in a composite
  axion model. It needs an axion particle, which this framework's rules exclude.
- Asymmetric and mirror dark matter need particles; out.
- The part found nothing from 2024 to 2026 that derives a ratio of 5.3 to 5.5 from dark energy, MOND or a clock field.

## 6. The one independent measurement

X-COP clusters, Newtonian: M_dark / M_bar = 5.73 +- 0.68, "1.07 x the cosmic" ratio
(`campaign_fresh_gravity/CFG4_README.md:215,227`). It is reported only and was never pooled with the CMB value. It
shows the same number in a second place; it does not explain it.

## 7. What would fix it (part B's list; all UNTESTED, none claimed to work)

- Coupling the charge's current to baryon number, eps J_B . d tau: does nothing. With baryon number conserved it is a
  total derivative (checked).
- A direct coupling of the clock to the matter fluid (alpha n_B f(Q), or beta Q T): one clock field, no particle, and
  R would follow from the coupling. It breaks the rule that matter couples to the metric only, predicts
  equivalence-principle and fifth-force signals, and replaces one fitted number with another.
- Breaking the shift symmetry early with a potential V(tau): the amount left over is set by V's scale and the time it
  switches off. One clock field. It predicts an early phase with a changing equation of state and possibly
  isocurvature. The match to the baryons stays unexplained unless V is tied to how the baryons were made.
- Making the dust during inflation (the 2026 mimetic route): one new coupling; no link to baryons.

Each is a new mechanism and would be a lane of its own, on the owner's go.

## Checks by the lead

- Part B's script re-run: every printed check as reported. Its record quotes re-read at the lines given.
- Parts C and E re-run from copies and again in this folder: outputs identical to the committed `.out` and `.json`.
  `hunt.py` had its output path made relative to its own folder; nothing else was changed.
- The cap identity (g = a0 / R for mu = x / (1 + x)) re-derived by hand.
- Part A's quotes re-read at the lines given in section 1, except the four listed there as not re-read.
- Part D: three abstracts re-read; the rest provisional.

## Files

- `part_B_action/frw_charge.py`, `frw_charge.out`
- `part_C_halo/candidates_written_first.txt`, `halo541.py`, `halo541.out`
- `part_E_hunt/FROZEN_SEARCH_SPACE.md`, `hunt.py`, `hunt.out`, `hunt.json`
