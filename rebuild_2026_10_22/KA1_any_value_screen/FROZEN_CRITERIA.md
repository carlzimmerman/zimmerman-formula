# KA1_any_value_screen: FROZEN CRITERIA, committed alone before any script or number

Owner's choice, 2026-11-02: stop requiring exactly 1/2; any forced value is acceptable. κ = 1/2 FITTED. Footings never pooled. Not theory closed. No cold component, no particle. **Not blind:** I have read the campaign rules, CFG891's README and register rows for Z = 6, including K038, K240 and K354. Rules: CFG894 `KAPPA_CAMPAIGN_RULES.md`.

## Question
Does any route already on the register force a single κ, at any value, with a live mechanism and a second prediction? The exact-1/2 test is dropped. Nothing else in the entry screen is relaxed.

## Input
`campaign_fresh_gravity/CFG894_kappa_campaign_ledger/kappa_attempts_register.csv`, read only, all rows K001 to K813.

## Stage A, mechanical
1. **Determinate:** `kappa` holds a number and `cls` is `odd`, `any` or `cont`. Menus are not determinate (§4).
2. **In window:** inside W_data on either footing, reported per footing: ρ_DE [0.227, 0.607], ρ_crit [0.189, 0.501].
3. **Not already dead:** the verdict text contains none of, case-insensitive: VOID, EXCLUDED, TAUTOLOG, CIRCULAR, CLOSURE, TRADE, WITHDRAWN, ALGEBRA ERROR, FAILS, not forced, unforced, not integrable.

Rows removed by step 3 are listed with the matching word, so a wrong removal can be seen. Every distinct κ value that left at step 3 is also listed, because a value can return by another route.

## Stage B, by hand, on Stage A survivors
Read the row's source file. Grade S1 to S8 of §3, each pass, fail or not shown, citing the file. Not shown counts as not passed. S4 is the deciding screen for this lane: name the second quantity and the data, or the row fails.

## Controls
- **MUTATE:** W_data set to [100, 101]. Stage A must return 0 rows; exit 1 by design. Outputs named `_MUTATE`.
- **Null count:** in-window count at step 2 is stated against the reference generator's chance mass from `kappa_campaign_lee.json`. If that file does not carry it, the count is stated without a null, and the README says so.
- **Planted:** a synthetic live row in the script's self-test must pass Stage A, and a synthetic row with verdict `VOID` must not.

## Labels
- **FORCED ROUTE, CONSISTENT:** at least one row passes S1 to S8. Never a detection (§7). Becomes a candidate for its own frozen lane on its second prediction.
- **SCREEN INCOMPLETE:** a row passes all but S4, with a second prediction that could be derived. That derivation is the next lane.
- **NO ROUTE:** no row reaches either label. This applies to the register as it stands and is not a no-go theorem.

## Limits declared now
Verdict strings were written by earlier lanes and step 3 trusts them. Stage B is one reader's grading, not an independent audit. No κ is produced, so P_LEE is unchanged. The lane adds one audit row (`cls` audit) to the register and reruns `kappa_campaign_lee.py`. No download. Single thread, seconds.
