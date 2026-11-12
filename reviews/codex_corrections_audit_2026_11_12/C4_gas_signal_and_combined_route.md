# C4: FINAL5 gas-signal correction and the two research folders (audit, 2026-11-12)

Independent auditor C4. Read-only on every lane, research and PAPER72 file. Checks were run from copies in a
scratch folder outside the repository. "Independent" below means my own derivation or my own short script; "reproduced"
means I re-ran the notice's own script.

## Verdict table

| Item | Grade | One line |
|---|---|---|
| FINAL5 notice (RESULT.md and PROPOSAL.md, line 1, identical text) | CORRECT | Projection, beam and flux-unit errors are real; the ~100 sigma forecast and "no outcome in between" are rightly withdrawn |
| gas_corrections/RESULT.md + corrected_signal.py (the physics) | CORRECT WITH LIMITS | Every number I recomputed in SI agrees to 4 digits on both footings. The shell profile is still one example, as the file itself says |
| final5_signal.py edited in place (17 lines added, 535 removed) | RECORD REWRITTEN (process breach) | The committed script was replaced by a wrapper. Committed outputs no longer follow from the live file; the tracked file now depends on an untracked one |
| combined_route/RESULT.md headline | CORRECT WITH LIMITS | "The theory is not closed". The arithmetic and the EFE matching numbers check out. It derives no kappa and no 5.41, finds no joint, identifies no medium and rescues no data row |
| closure_push_02/RESULT.md headline | CORRECT WITH LIMITS (partly NOT CHECKED) | A negative result: the QX17/PIK1 gated construction is "not a closed, healthy theory". The early-history bound is verified; the galaxy pressure ceiling is not. Canonical footing only |
| "Frozen before numbers" in the two folders | NOT SHOWABLE | They are untracked, so only file mtimes exist. closure_push_02's CONTRACT.md was last modified after its own early results |
| Rule breaches in new text | MINOR | Home paths in run records. "cold dark self-gravity factor" in two closure_push_02 files. No "cold dark matter" used for the component. No statement that the data favour the framework |
| PAPER72 Section 8.5 FINAL5 sentence | KEEP; one optional clause; fix the table cell | The sentence stays true. Table row 340, "the deciding observation", repeats the framing that has now been withdrawn |

## Part 1: FINAL5

**What the notice asserts** (RESULT.md:1 and PROPOSAL.md:1): "The projection, beam, flux units and universal
detectability/shape conclusions below are superseded ... No guaranteed 100-sigma detection or universal
mass-conservation exclusion is established." The notice adds a banner and deletes nothing. FROZEN_CRITERIA.md,
final5_signal.json, final5_signal.out and final5_signal_MUTATE.out are unchanged (git diff is empty). Their SHA-256
values match `gas_corrections/originals/sha256.json`, and so does the HEAD version of the script.

**Independent SI check (my script, both footings, kT = 0.2 keV, <M_b> = 8.42e10 Msun, R_out = 2.6 Mpc).**
1. The requirement is a constant g_bar = a0/x_b^2, with x_b^2 = 5.41 x 6.41. That gives M(<r) = a0 r^2/(G x_b^2). The gas is
   rho = Sigma/(2r) above R_in = sqrt(G M_b x_b^2/a0), with R_in = 65.95 kpc (canonical) and 59.99 kpc (alt).
2. The Compton parameter is y = (sigma_T/m_e c^2) * Integral n_e kT dl, with n_e = rho/(mu_e m_p) and mu_e = 1.14. I integrated it numerically
   along the line of sight.

| b (Mpc) | my N_e canonical (cm^-2) | my y canonical | committed y (flat sheet) | corrected y | my y alt | corrected y alt |
|---|---|---|---|---|---|---|
| 0.3 | 1.924e21 | 5.009e-7 | 1.76e-7 | 5.009e-7 | 6.053e-7 | 6.053e-7 |
| 1.0 | 1.087e21 | 2.829e-7 | 1.76e-7 | 2.829e-7 | 3.419e-7 | 3.419e-7 |
| 2.0 | 5.107e20 | 1.330e-7 | 1.76e-7 | 1.330e-7 | 1.607e-7 | 1.607e-7 |

My y is acosh(R_out/b) = 2.849 / 1.609 / 0.756 times the committed flat-sheet value. So the committed run's default
(`geom = 1.0`, described in its own docstring as "this is the MINIMUM") was not a minimum: at 2 Mpc the spherical
column is 0.756 of it. The corrected file's "old_default_column_relative_error -0.379" is 1/1.609 - 1 at b = 1 Mpc.
The physical signal is therefore not flat in b. It falls by about 3.8 times between 0.3 and 2 Mpc, and its amplitude scales
linearly with T. The corrected numbers are right.

3. **X-ray flux units.** With L_X = 3e44 erg/s at z = 0.308, I get D_L = 1657 Mpc and F_X = 9.13e-13 erg/s/cm^2. The committed
   value was 9.1e-9: it divided erg/s by D_L^2 in m^2 and labelled the result per cm^2, which is 1e4 too large. CONFIRMED.
4. **Beam.** The committed `smear` is a weighted average using exp(-(b-R)^2/2s^2) b, normalised at each radius. The 2D
   circular-Gaussian radial kernel is (b/s^2) exp(-(R^2+b^2)/2s^2) I0(Rb/s^2), which equals the corrected
   `b/s^2 exp(-(R-b)^2/2s^2) i0e(Rb/s^2)` (my own reduction of the azimuthal integral). The old kernel omits the I0
   factor. CONFIRMED.
5. **Epoch of the overdensity.** (1+0.308)^3 = 2.238. The committed delta/rho_b = 2483 used z = 0 denominators. CONFIRMED.
   KA3: 3.234e13/3.186e13 = 1.015, so the old "reproduces" hides a 1.5 % mismatch. CONFIRMED.
6. Reproduced: a copy of corrected_signal.py gives JSON identical to `run_001/results.json`.

**Limits.** The gas shell is one realisation of a lower bound on the enclosed mass. The file says this itself. The X-ray cooling
coefficient is illustrative. No significance is assigned, which is correct because y needs T and the map filtering.
A2's grade (OVERSTATED, not decisive for the joint) stands and is reinforced.

**The in-place script edit.** The commit holds a 552-line script. It had a flat-sheet default, a 1D-normalised beam, a
cgs/SI flux mix-up, the KA1-KA5 known answers, the M1-M4 mutation arms and the printed tables that produced
final5_signal.out, .json and _MUTATE.out. In the working tree it is now an 18-line wrapper that `runpy`s
`research_closure_2026_11_12/combined_route/gas_corrections/corrected_signal.py`. Consequences:
- The committed outputs no longer correspond to the live script. Running it writes a different JSON and no .out tables.
  The old code still exists in git history and in the untracked `originals/` (hash verified). Even so, the working-tree file
  was rewritten rather than added to, which breaks the forward-only convention.
- A tracked file now depends on an untracked path. If the lane folder is committed without the research folder, the
  script raises FileNotFoundError.
- `python final5_signal.py final5_signal.json` would overwrite a frozen output. The wrapper only guards the default.
- Recommendation for whoever commits: restore the HEAD script and add the corrected code as a new file, or commit
  the research folder alongside. PAPER72's supplement builder already refuses on this folder (tex line 2).

## Part 2: the research folders

**(a) Conclusions in their own words.**
- combined_route: "The errors have forward corrections; the theory is not closed. The combined mass-retention/
  external-field idea survives as a conditional research route." It establishes Mc/Mb = 5.41 Fc/Fb as "an accounting
  identity, not a formation law", where 5.41 is "the supplied initial composition". It also gives the AQUAL matching values
  g_ext/a0 = 0.01318417, g_N,ext/a0 = 1.715603e-4 and R_E = 75.84856 r_M, "inferred from the target amount, not independent
  environmental predictions". Under a supplied environment model it needs a 6.54-fold conditional cold-mass growth.
- closure_push_02: "The current QX17/PIK1 density-gated implementation is not a closed, healthy theory." The joint
  obstruction: the galaxy pressure bound needs mu <= ~450/Mpc, while the unchanged early history needs mu >= 8.89e6/Mpc
  (2.30e6 even if the stiff energy may equal all radiation). "No universal all-theory impossibility or derivation of kappa is claimed."

Neither folder claims a completed theory, a derivation of kappa or of 5.41, a found joint, an identified medium or a
rescued data row. Claims that come close: the combined_route "useful partial progress" (a positive finite-mass Newtonian
equilibrium, which the file says "exists for every positive mass ratio", so it selects nothing) and closure_push_02's
"inner galaxy solution exists" (a finite annulus reproducing a reference force to 3.55e-7). Neither is a hit on the
framework's open questions. The "independent reviews" they cite are other agents in the same session. They are not an
independent re-grade in the record's sense. A real re-grade would have to re-derive: the closure_push_02 constrained
principal symbol A_inf = Q^2 H_QQ - c^2/D from the action; the static pressure ceiling of 435-446/Mpc; and, for
combined_route, the 1.44212 radius-window baryon growth.

**(b) Checks of the load-bearing results.**
1. *Retention and EFE matching (combined_route), independent.* 5.41/59.5 = 0.0909244. With the simple-kernel nu
   at y = 1.715603e-4, x = 0.01318416. Linearising AQUAL about the external field (mu_e, L = dln mu/dln x = 1/(1+x)), I
   integrated the Gauss flux of the anisotropic point-mass solution over a sphere myself. It gives an asymptotic
   excess of 59.500 (F_A = 60.5), matching the contract's atan(sqrt L)/(mu sqrt L). R_E/r_M = 1/x = 75.8486. The growth arithmetic
   (59.5 x 1.44212)/13.1172 = 6.5415 holds, and 1/6.54147 = 0.152871. CORRECT. 1.44212 itself is model-dependent and NOT CHECKED.
2. *Early-history bound (closure_push_02), independent.* From rho = n0 a^-3 + K n0^2/(2 mu^2) a^-6 with K n0 = 1.5 H0^2 Omega_d,
   I re-derived rho_stiff/rho_r = Omega_d I0/(4 mu^2 Omega_r a^2) with I0 = 3 H0^2 Omega_d. With my own guesses (Omega_d 0.264,
   Omega_r 9.15e-5, H0 67.4, a = T0/0.1 MeV) the 0.067 budget gives mu >= 8.84e6/Mpc, against their 8.89e6. Their
   ratios 19,756, 5,114 and 26.1 million follow exactly. The 0.067 budget comes from committed KD1, so it was frozen earlier.
   CORRECT.
3. *Instability sign (closure_push_02), conditional.* I took their stated A_inf, c and D as given. With S = exp(-u^3), sympy
   finds A_inf < 0 with D > 0 at, for example, Q = 1.5, u = 0.9 and Q = 100, u = 0.9. So the sign claim is consistent with their symbol.
   I did NOT derive the symbol from the action, so the instability itself is NOT CHECKED.
4. *Galaxy pressure ceiling (450/Mpc):* NOT CHECKED. It needs their static construction. Because the gap is a factor of
   about 2e4, the conclusion survives any plausible error of order one, but it is canonical-only (10^11 Msun canonical target).

**(c) Rules.** Criteria frozen first: the folders are untracked, so git cannot show this. The only evidence is mtimes:
- combined_route CONTRACT.md was written at 11:15 and its first run at 11:23. The per-run contract.json files are written
  about 2 s before each run, so they are run manifests, not preregistrations.
- cosmology_diagnostic CONTRACT.md was written at 11:33:40, before its runs at 11:34.
- closure_push_02 CONTRACT.md was last modified at 12:42, after current_transport (12:01) and hamiltonian (12:20) had results.
  It contains a "Continuation after the repair checkpoint" section, so it was amended after numbers were seen.
- mtimes can be changed after the fact, so none of this is proof.

Both footings: gas_corrections runs both. combined_route works in dimensionless units and does not state the footing of
59.5. closure_push_02 is canonical only. Known answers: present (LOS, projected mass, 2D Gaussian beam, Einstein-de
Sitter, homogeneous expansion). Mutations: present (temperature doubling, three failing controls). None of it is a
pass/fail lane, so frozen gates matter less here. The folders grade constructions, not data.

**(d) Breaches.**
- Home-directory paths appear in new run records: combined_route/cosmology_diagnostic/run_commands.txt and central_130/stderr.txt,
  plus dt2_corrections *.out files and final17_run_001/manifest.json, pik1_corrections/run_legacy/stderr.txt, and h062_run_001/stderr.txt.
  They also appear in the archived originals, which are copies of committed text. These must be scrubbed before commit.
- "cold dark matter" appears only in archived copies: FINAL4 describing LambdaCDM, and frozen-criteria copies that forbid the term.
- New text has "The full cold dark self-gravity factor" (closure_push_02 RESULT.md and CORRECTIONS.md). It should read "cold dark
  energy". closure_push_02 also says "the Zimmerman relation". That is the formula's name, not a personal reference, but PAPER72 should not copy it.
- No statement that the data favour the framework.

**(e) What PAPER72 v1.2 may cite once committed.**
- gas_corrections: may be cited for the three errors and the withdrawal of the FINAL5 forecast.
- combined_route: may be cited for the accounting identity Mc/Mb = 5.41 Fc/Fb, as the reason the "5.41 cap" argument is withdrawn
  (A2 already notes this). It may also be cited for the AQUAL matching values as conditions inferred from the target.
- closure_push_02: may be cited as a scoped negative result on the QX17/PIK1 gated dust (no common mu, canonical footing).
  It may also be cited for withdrawing the 25120/Mpc (2.51e4) growth threshold, which bears on the pending MK1 sentence at tex
  line 162 (another auditor's slice).
- Do NOT cite them for: any derivation of kappa or 5.41 (5.41 is an input); retention fractions as predictions; the 6.54-fold
  growth as a bound (it is conditional on a supplied environment model); the inner annulus or positive equilibria as a medium
  or a completion; an independent re-grade; frozen-before-numbers status; any observational likelihood; or the alt footing.

## Part 3: PAPER72

Section 8.5 (tex line 265): "FINAL5 proposes a stacked thermal SZ measurement and grades nothing; A2 finds it not decisive
for the joint." This stays true with or without the notice, so no \pend marker is needed. Once the notice is committed,
optionally add: "A forward correction withdraws its detectability forecast (about 100 sigma): the forecast took the column
as a flat sheet (the projected column of the required shell falls as acosh(R_out/b), 2.85 to 0.76 times the sheet value
between 0.3 and 2 Mpc), used a beam that is not a 2D convolution, and overstated the X-ray flux by 10^4. No significance
is assigned without a temperature model." Table row (tex line 340): change "the deciding observation" to "a proposed
observation". The current cell repeats the framing that has been withdrawn.

## Not checked

The constrained principal symbol and its derivation, the static pressure ceiling, the compression run, the gate-family
lemma, cosmology_diagnostic's focusing time, the 1.44212 window growth, and the DT2, PIK1, G238-G242, FINAL17 and H062
sub-corrections (other slices). Whether the ACT strip covers the KiDS lenses. No heavy runs; no downloads.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
