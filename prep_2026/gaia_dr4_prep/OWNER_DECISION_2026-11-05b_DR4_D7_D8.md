# OWNER DECISION, 2026-11-05 (second note, pre-data): Gaia DR4 decisions D7 and D8

**Status: filed.** The owner accepted, in chat on 2026-11-05, before any DR4 byte exists (DR4 due 2026-12-02): "File as
recommended". This closes D7 and D8, left OPEN by `OWNER_DECISION_2026-11-05_DR4_FORKS.md` (413c1c8e24). Committed alone;
never edited after commit; any change goes in a new dated file. It edits no frozen file: not PREREGISTRATION_DR4.md or its
22 amendments, not the D2 note or A1-A3, not CFG740, CFG800/825, CFG943, or the 10-21 kill-line note
(`campaign_fresh_gravity/OWNER_DECISION_2026-10-21_DR4_KILL_LINE.md`, which already settled CFG943 N1, N2, N3, N6, N10).
No prediction, estimator, cut, threshold or verdict row changes. κ = ½ FITTED; footings never pooled; not theory closed.

## D7. CFG943 §7 items still open after 10-21 (N4, N5, N7, N9)

**N4, stability on boost-side verdicts (adopts CFG943's proposed text, first option).**
1. The NSS-off rung is run as `build(drop_nss=True, smax_kau=30)` (the code path that exists in
   `build_variant_catalogue.py`). It is wired into the sweep tooling as new code before release and must reproduce the D2
   lane's DR3 NSS-off probe on the DR3 extract before it is used on DR4. If that DR3 check fails, the rung is declared
   NOT IMPLEMENTED in the DR4 report and does not block a verdict; σ_sys(b) is then computed without it and that is stated.
2. A shift smaller than 1 σ_fit counts as passing the NSS-off condition ("moves γ̂ toward the verdict value" is read only
   for shifts ≥ 1 σ_fit).
3. The ladder rule is applied as written. Beside any "systematic-limited" outcome the report states the expected
   false-failure rate of the 3-20 kAU rung under a correct model (~40 %, CFG943 MOCK).

**N5, the R input catalogue.** The DR4 R input is **the registered catalogue** (stage G, NSS-screened, 30 kAU cap), with
`make_pair_table.py` run with `--declare-neutral non_single_star`. The CFG825 variant catalogue (`build_variant_catalogue.py`,
declared 2026-10-18, never filed) is run and reported as **information only**, with no verdict weight.

**N7, CFG740 falsifiers with no registered statistic.** Falsifier 1 beyond ~37 kAU and falsifier 2 (log-slope 2) are
**not scored** in the DR4 confrontation. Any test of them needs its own criteria committed alone before use.

**N9, tooling defaults.** The primary build is run with `--cut13 cones-literal` (Amendment 16(b)'s primary), passed
explicitly and recorded in the manifest. Amendment 18's seed sweep uses the existing **extract-builder** cut-13 mode,
recorded in the manifest as such. If a bulk-crossmatch transport for cut 13 is later filed (separate dated pre-data
amendment with a DR3 equivalence test), this choice may be revisited only in that filing, before the data.

## D8. σ_sys(b) and the NSS-off probe

**Option (a) adopted: σ_sys(b) stays as frozen** (D2 A3: max(0.020, ½ × full spread of γ̂ across the frozen robustness ladder
and the NSS-off probe), measured on DR4). No pre-data amendment separates "contamination removed" from "systematic".

Added as **information only, no verdict weight:** a mock-triple injection test (known triple fractions injected into the
frozen population generator, run through the frozen pipeline with and without the NSS-off rung) may be run before or after
release and reported beside the verdict, to show how much of the NSS-off shift is contamination removal. It can never change
σ_sys, a band, or a verdict.

Stated now so it is not decided on release day: this choice raises the chance that DR4 reads UNDECIDED (the 2c table of
413c1c8e24 shows the band widening with σ_sys). It was chosen over an amendment because changing the binding error term weeks
before the data, after DR3 showed it binding, would read as tuning, and because it could add power only against the bare
law; v3s can never be confirmed over Newton by DR4 (CQ2).

## Sources
CFG943 README §7 (N4, N5, N7, N9 proposed texts); 10-21 kill-line note §3 (open list); D2 note A2-A3; CQ2 SEALED_PREDICTION.md;
`OWNER_DECISION_2026-11-05_DR4_FORKS.md` (413c1c8e24); `reviews/GAIA_DR4_DEEP_REVIEW_2026-11-05.md` (2c69526e6b).
