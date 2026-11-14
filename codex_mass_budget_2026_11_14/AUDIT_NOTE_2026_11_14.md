# Audit note for this folder (2026-11-14, written 14:38 EST by the clock)

Written by the lead session, not by the tool that produced this folder. The folder is a Codex session's work of
2026-11-14, done on the owner's authorisation and handed to the lead. It is committed on main after an independent
audit by a separate agent, whose own re-runs are in `reviews/codex_mass_budget_audit_2026_11_14/` (README first).
Nothing here is adopted; no lane label changes.

**Grades of the audit (each claim's deciding step was redone):**
- Enclosed-mass audit of the implemented layouts (10,272 cases, total mass conserved to 6.7e-16; at z = 0 and f = 2 the
  uncapped raw law asks for more than the patch's cold charge in 172 / 240 canonical and 186 / 250 alt grid haloes for
  the retained source, 240 / 240 and 250 / 250 for all explicit baryons): CORRECT. Grid counts, not population
  fractions.
- The denominators (5.41; grid ratio 5.364327224; FRZ1's share 59.4861 / 59.5029 at z 0, 55.7159 / 55.7313 at z >= 1):
  CORRECT.
- `calculation/BUDGET_BOUND.md` (criterion, radius, monotonicity proof): CORRECT. Its example table: CORRECT WITH
  LIMITS. Six of eight rows were checked and match to the last digit with the halo code's G; with CODATA G and the
  record's solar mass every radius is 1.3e-4 larger, and the folder's "independent physical-unit check" reuses the
  halo code's G, so it does not test that convention. No count changes.
- `latest_review/JUNCTION_THEOREM.md` (the static junction; [J^r] - Rdot [J^t] = 0; the reading of QX17's E2 and E3;
  lambda = 0 in an exactly stationary interior; the advective reduction and its consequences) and
  `latest_review/TRANSPORT_PATH.md` (the kinematic interpolation and its velocity bound): CORRECT, the stationary-
  interior step WITH LIMITS that the theorem itself states.
- "7,110 snapshots; 3,706 require outer outflow if the front grows while the inside stands still": CORRECT (recounted:
  27 with zero outer density, 3,706 with the law's density below the outer one, 3,373 above, 4 equal).
- **WRONG in the weak field:** the sentence "Full polarization transport can change that conclusion" (README and the
  handoff). The non-advective term lambda P / Q of QX17's current is (g r / c^2) / (dln M / dln r) of the advective
  flux, 3e-7 to 5e-7 for a Milky-Way-mass system at 100 kpc. A thin transition layer does not change the scaling unless
  its width is 1e-14 of the radius or less, which is the surface reservoir the theorem excludes. So in the weak field
  the advective condition stands to about one part in a million.
- The WLJ1 grader regression (`closure_2026_11_13/WLJ1_power_and_lensing_amplitude_with_split/test_wlj1_grade.py` and
  `codex_fix_2026_11_14/`): CORRECT. 7 of 7 tests pass; the pooled-flag mutant fails; the six outputs reproduce byte
  for byte.
- `INDEPENDENT_REVIEW.md` and `verification/VERIFICATION.md`: CORRECT WITH LIMITS. The "independent" reviewer is a
  subagent of the same session, so it is not independent of that session, and it re-ran no numerical experiment. The
  "nine validated manifests" rest on a validator outside the repository that checks hashes and provenance, not
  correctness.

**Not checked by the audit:** the two z = 4.4 budget rows; the 76 interior crossings; the scope tables of run_003 and
the figure; COL1's reduction itself; the manifest validator; `latest_sn_review/`.

**What is committed and what is not.** Committed: 82 files (3.3 MB). Home-directory paths were replaced by `<repo>`,
`<codex-skill>` or `<home>` in ten of them (listed in the audit's README under hygiene); `calculation/reproduce.py`
therefore needs its validator path set before it runs. Left untracked on main: `calculation/SHA256SUMS` (stale after
the redaction), `calculation/run_005/` (a failed run), two files of `calculation/run_001/` over 5 MB (regenerable),
`latest_review/run_001` to `run_006` and `run_007/junction_checks.json` (5.8 MB, regenerable), four duplicate copies in
`before_correction/`, `latex_compile.json`, `latest_sn_review/` (another lane's subject) and the handoff text at the
repository root. The unredacted originals are on the branch `codex/mass-budget-2026-11-14`.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
