# Handoff to astra, 2026-11-04: where the a0 law, clusters and the action stand, and the open lanes

Written at the owner's request ("push up this work and lanes for astra to pick up and continue"). This is a brief, not a result. Every claim points to a lane README, which is the record. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.

## State on 2026-11-04 (read these first)
- **Flagship:** PAPER67 v1.1, DOI 10.5281/zenodo.23966443 (new version of 23883741), audit 685/685. A **v1.2 draft is being written by a Claude helper right now** and will state the scoped action. Don't edit `qwen_claude_field_theory/papers_2026/PAPER67_*` until its commit lands.
- **Owner decision, later on 11-04:** v3s is adopted as the a0 law's action, **scoped** to isolated galaxies, the Solar System, galaxy lensing and GWs. Clusters, growth and the CMB, the radiation era, hosted dwarfs and the MW joint fit stay open. a0 is put in by hand. Decision file: `finish_2026_11_04/FN1_action_call/OWNER_DECISION_2026-11-04_ADOPT_V3S_SCOPED.md` (7ac515f958), plus the last STANDING.md addendum. It supersedes the same day's FN1 "no action" file.
- **Failure record for 11-02 to 11-04:** `FAILURES_EXECUTIVE_SUMMARY_2026-09-28.md` section F (c0412629ce). Every row is a failure or a block, with its commit.
- **Owner rules that apply to your lanes:**
  - Test lanes may reopen frozen or retired items. A test adopts nothing.
  - Hits must pass all gates, with tolerances from real errors set before the search.
  - Ask before downloads, deposits or sending anything.
  - No dark-matter particle. Say "cold dark energy", never "cold dark matter". No ΛCDM inputs.
  - Footings: canonical 9.3603e-11 and alt 1.1312e-10, never pooled.

## What 11-02 to 11-04 settled
| Question | Answer | Lanes |
|---|---|---|
| Is there a cluster term in gas, size, acceleration or temperature? | No. Every hit sits at or below scrambled controls, up to 7.5e11 expressions | BF1-BF3, BK2 L1/L2, SR3, RS1, TX1 |
| Do shared calibration errors explain it? | No: χ² 518-1219 against a mock of about 50 | WA1 |
| What must the missing cluster mass be? | Collisionless, cluster-wide, about 4-5x the hot gas, nearly absent in isolated galaxies | UX6, MG1, MB1, DB1 |
| Is there an ordinary carrier? | No. Cold baryons have no window; per-member halos are too little; the fluid fails; light fermions fail the CMB | DB1, MB1, DF3, HF1, VW1 |
| Which action gives the law and passes the Solar System? | Only v3s's screening length L★. Every unscreened class fails Q2 by 1.69-5.18x | AX1, C6P, V3W, V3X |
| Is there a selector that hides a dust part in galaxies? | None found. 10 fresh ideas: 4 already dead; tidal isotropy, vorticity and the cubic galileon are killed | FA1 (+ I2, I6) |
| Does a0 track ρ_DE at high z? | Untestable on disk: all 22 samples are BLOCKED by a common mode of 0.30-0.60 dex | AT2 |
| A power-law screening length L ∝ M^p? | WINDOW at p 0.30-0.45 (canonical 3/48 points, alt 9/48). The v3s-like p = -0.5 fails the 24 dwarfs. DR4 seal 7ab147288d | FN6 (9fd0447628) |

## Open lanes for astra, best first

### A1. v3s: the two UNDECIDED items (small, closes the adoption's weak spots)
`rebuild_2026_10_22/V3X_v3s_close_undecided/README.md`.
- **W2:** the in-window ladder passes on the physics (Richardson −0.7 % against the 2 % line), but check K1 was frozen at 1e-6 at all three radii, including r_Saturn, which is beyond float64. Write a *new* lane with frozen criteria that grades K1 only at the graded radius, set before running. Don't amend V3X.
- **W4c(b):** the l = 1-4 spectral ladder needs ≥ 24 cells per decade (it missed at 14.6 % against 5 %). Decide, with a stated source, whether 1e-10 is the right tensor line, and do it before rerunning.

### A2. v3s: what is still asserted
From V3W/V3X:
- nonlinear well-posedness;
- the PN-order sign of corrections;
- the Sun at rest in the khronon frame (a moving-source check, like AS3's α1 moving branch);
- a realistic solar interior instead of uniform density;
- constraint causality: constraints act instantaneously, and C5's cone criterion fails.
Each item is its own lane.

### A3. a0 from the v3s action (owner's G5; P3 of your 11-03 goal)
In every class, including v3s, a0 is put in by hand. KF1: κ = 1/(2ξ), with ½ standing for a forcing length c/√(Gρ_DE). KC1 lists the reopen conditions. Is there a v3s term whose natural scale is c/√(Gρ_DE) with coefficient 1?

### A4. FN6's window vs v3s
`finish_2026_11_04/FN6_powerlaw_screening/`. Windows sit at p 0.30-0.45. v3s's own scaling (stood in by p = -0.5, Gaussian smoothing) fails the dwarfs. Does any covariant completion give L ∝ M^0.3-0.45? Would v3s with such a length keep C6P's Q2 margin? Use v3s's own equations, not the Gaussian stand-in.

### A5. Clusters (P1 of your goal): still the hardest
The requirement sheet is in FAILURES section F and FA1's README. Closed selectors, don't repeat:
- baryon mass, potential, gas fraction or density, temperature, g/a0, hosting, epoch, orbit count, σ;
- memory, member halos, a barotropic fluid, light fermions, cold baryons, Σ ∝ σ^q;
- tidal isotropy, vorticity (both readings), the cubic galileon's Hessian determinant.
Standing walls: X22 (galaxies capture forest-passing dust) and X57 (the μ-pincer, Theorem G). A new route needs a principle outside baryon geometry and kinematics.

### A6. FA1 leftovers (small)
- I2: SLACS needs a rotation class per lens.
- The 15 shear keys at selector level for I1 and I2: the gas profiles sit inside X30's drivers.
- I6's Bullet needs a 3D nonlinear solve.
All three are already killed elsewhere, so these only make the record complete.

### A7. a0(z) (needs data; ask the owner)
AT2 names what would decide it:
- 25-50 CO discs at z 1-1.6 with v/σ ≥ 6, three gas tracers and JWST M/L, about 500-1,500 ALMA hours;
- a z < 0.1 CO reference with measured gas, e.g. PHANGS-ALMA or EDGE-CALIFA (names from memory, unchecked).
Any download needs the owner's yes. It is proposal work, not computation.

### A8. BK2's G3 ERR (bookkeeping)
BK2 flagged its Z_shape as too strict, because no cluster-to-cluster scatter is on disk. A new lane could measure that scatter first, freeze it, then regrade. Never widen BK2 itself.

## Housekeeping
- Untracked caches and home-path copies sit in DB1, MB1 and BF1 (`cache_keys/`, `x74_*`, `*.err`, `*.done`). Never commit them, since several carry home paths.
- Other sessions push often and share the git index. Commit with explicit paths (`git commit -- <paths>`), and report your own commit's hash, not HEAD after a merge. On 11-04 a race put the wrong BK2 hash into the PAPER67 draft; the audit caught it.
- Leak check before any push: `git diff origin/main..HEAD | grep -cE '^\+.*(/Users/|ZENODO_ACCESS_TOKEN=|gmail\.com)'` must print 0.
