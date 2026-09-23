# Qwen path/control audit — 2026-09-22 10:54 UTC follow-up

Target66b8164cf7434139b5e7cf630bff7baa. Original candidate preserved byte for
byte. Codex's separate AST instrumentation inserts only a capture of path
arrays before filtering: transport, random calls, seed42/43 and photon counts
are unchanged. The independent harness recomputes ensemble residuals, exact
means, geometry, complete finite counts, and substitutes T for D on the SAME
paths. It does not hardcode negative check outcomes. This is an independent
harness replay, NOT an independently implemented transport simulator.

All20 audit checks pass. For uniform/quadratic respectively:
main Rz1.7313,.5764; Gz.1433,-.2181; meanz.4514,.6065;
positive Rz-.9694,-1.9373; Gz-1.4083,1.3942; meanz.3813,-1.9630.
Actual T-substituted R z29.5779,16.2356(main),41.8295,22.9372(positive).
Thus useful finite path evidence survives, and a genuine negative fails without
fabricated booleans. It does not prove a universal identity or novelty.

Original candidate certificate remains rejected: forced False negative,
noncontract seeds, missing mean/completeness predicates, fake atom proxy,
invalid geometry marked escaped, and dropped degenerate scatterings. No path
in this finite audit was filtered, but that does not validate those edge cases.
Later2835eabd/2c1a7b1b use exp(-d) instead of exp(-integral kappa dr), and
reseed each photon over overlapping adjacent ranges. This duplicates nearly
all samples, understates SE and overlaps main/positive. Keep their failure,
not an alleged counterexample. v11 gives the precise repairs, targets intact.

Absorption b675534e,4a7877ba,7757e28a mis-unpack the conservative dictionary;
4a and775 then replace failed data with zeros. Actual API is cons['delay'],
cons['time']; killed_transport returns(escaped_D,n_escape). 775 has real killed
numbers but no valid conservative comparison. Margin SE is incorrectly reused
for mean/variance in these wrappers. v5 supplies exact APIs and uncertainties.
No claim about absorption selection has passed both estimators this visit.

certified/ preserves first execution:20 checks passed but the wrapper forgot
to write the declared result file, so manifest status result-missing. No physics
failure. replay_v2.py writes that file; certified_v2/ is the successful bounded
run and validated manifest. Earlier source/contract/logs are untouched.

No runner/model changes, remote calls, observational or novelty promotion.
The existing conservative opacity-cap proof remains Codex self-reviewed;
independent peer review and empirical applicability remain open.
