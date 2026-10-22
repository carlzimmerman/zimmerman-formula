# Doors push 2026-10-22: shared brief for lanes D1–D9

The owner asked for a rigorous pass on every open door left after the DSF-21 push
(`deepseek_push/DS_FINAL_2026_10_21/`) and the Argon AG6/AG7 lanes (`argon_push/`), looking for
**new, crisp findings or matchings**. A crisp finding is a number or a sign that a committed script
computes and that a reader can check: a decisive power estimate, an error in the record, a test that
can run now on data on disk, or a no-go with the obstruction named. Restating the record is not a
finding.

## Lanes

| lane | door |
|---|---|
| D1_skew_preflight | n = 1 vs n = 2 occupancy-noise skew test: power pre-flight on data on disk |
| D2_wide_binary_fork | law-first vs medium-first fork (γ_v 1.18 vs 1.0 at 20 kAU), κ leverage, what can run before Gaia DR4 |
| D3_cfg960_status | CFG960 1024³ native shear run: what happened, what it says, what is needed |
| D4_alma_status | ALMA CFG806/CFG809 governing plans: readiness and honest power |
| D5_kappa_four | the "4" in ρ_DE c²/(a₀²/G), i.e. why κ |
| D6_u_mechanism | the u(r) retained-fraction mechanism (u ≈ 0.47 inside splashback) |
| D7_turnoff_yt | origin of the strong-field turn-off y_t |
| D8_Lstar_value | microscopic value of L★ (window 24–90 pc) |
| D9_uv_parent | covariant parent / UV completion of the cold sector |

## Standing rules (all lanes, no exceptions)

1. **Test the framework on its own terms; verify a fail as hard as a win; never manufacture either.**
2. **κ = ½ is FITTED.** The thermal value κ = Z/4π = 0.460659 (a₀ = cH_Λ/2π) is a **postulate**
   (DSF-21 A75), and it is Milgrom's relation 2πa₀ ≈ c²(Λ/3)^½ (arXiv:1605.07458 eq. 5), not new.
   Z = 2√(8π/3) = 5.78881 (never ≈ 21). Never say "derived" for either value.
3. **Two footings, never pooled:** canonical a₀ = 9.36e-11 m/s², alt 1.13e-10 m/s². Report both.
4. **No dark-matter particle.** The extra mass is the cold-energy sector ("cold energy").
5. **Never write "theory closed"** and never say the data favour the framework over ΛCDM.
6. **Check the record first.** Before proposing anything, grep the repo (`campaign_fresh_gravity/LEDGER*`,
   `deepseek_push/CANDIDATE_LAWS_REGISTER.md`, `deepseek_push/DS_FINAL_2026_10_21/`, `argon_push/`,
   `why_4_puzzle/`, `what_is_time/`, `core_open_problems_*`) for prior attempts. `deepseek_push/DS_FINAL_2026_10_21/BRIEF.md`
   §2 lists closed doors: do not re-run them. Say in your report what you checked.
7. **No knob scans.** Zero declared free parameters added silently; every constant is listed with its
   source. No fitting to the target number.
8. **Frozen criteria first.** Write `FROZEN_CRITERIA.md` (what is tested, pass/fail lines, what each
   outcome means) **before** any script or number, and commit it alone:
   `git add <lane>/FROZEN_CRITERIA.md && git commit -m "<LANE> FROZEN CRITERIA ..." -- <lane>/FROZEN_CRITERIA.md`.
   Any later change is an append-only `AMENDMENT` section, marked pre- or post-result.
9. **Scripts:** `<lane>.py` prints one line per check (`K1 PASS <value> <threshold>`), ends
   `<LANE> COMPLETE: N/M checks PASS.`, exit 0 iff all pass; deterministic, no network; writes
   `<lane>.out` and `<lane>_results.json`. A `--mutate` mode (or env var) must break at least one
   check, with output in separate files named by mode (`*_MUTATE.out`, `*_results_MUTATE.json`).
10. **Compute budget:** a live heavy job may start at any time. Every run: `OMP_NUM_THREADS=1 nice -n 10`,
    < 2 GB RSS, single thread, minutes not hours. No downloads: data on disk only.
    No new outside data without the owner's OK (say what you would need instead).
11. **Repo hygiene:** write only inside `doors_push_2026_10_22/<your lane>/`. Never edit another
    lane's or campaign's files, never `_external_data` contents, never the frozen Gaia DR4
    pre-registration. No user names or home paths in committed files (use repo-relative paths).
    Commit **only your own lane's paths** with `git commit -- <paths>` (another session is committing in
    the same checkout; if `index.lock` exists, wait a few seconds and retry). **Never push, never
    rebase, never amend, never delete.**
12. `README.md` in the lane: **Verdict first** (one of `CRISP FINDING`, `RUNNABLE NOW`, `DATA-GATED`,
    `SCOPED NO-GO`, `NOTHING NEW`), then the numbers, then what it does not show. Plain English,
    short sentences. Every number appears in `<lane>_results.json` or is a labelled external input.

## Return to the coordinator (your final message, ≤ 25 lines)

Verdict; the 1–3 crispest results with numbers; the commit hashes; what you checked in the record;
anything you found wrong in the existing record (file:line); the single most valuable next step.
