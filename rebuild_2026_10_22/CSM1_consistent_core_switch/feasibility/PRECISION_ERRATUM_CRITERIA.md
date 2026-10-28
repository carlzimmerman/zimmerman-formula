# Post-result precision erratum, before corrective arithmetic

Independent calibration column review identified that EM1/X43 imports full-precision a0 from
`real_research/derivation_chain_2026/FP0_core_postulates_results.json` via CFG4_common, whereas this lane's first
scalar audit used the displayed rounded footing values (as old CL3's diagnostic root solver did). The first
packet correctly noticed the rounded-PC conversion but missed the additional a0 digits. Its reproduction of
old CL3 remains valid; labeling its newly computed X43 roots as exact to the actual scorer was too strong.
Keep the original artifacts and frozen inputs unchanged. The lens-support cap uses the explicitly rounded
X53/F2 values and is unaffected; heldout/LG/UFD reviews use actual logged floors and are unaffected.

Use the already validated background-A collapse column and S9 data from run001. Its critical level at logM12.3
rescales by `(a0_FP0/a0_displayed)^(4/5)`. Record both the running predeclared challenge and the value that would
exactly satisfy the original algebraic target with actual a0. At the already running L challenge, direct
column/floor ratio at12.3 is `a0_displayed/a0_FP0`; report the discrepancy. Do not introduce or run a second
observational challenge. The coordinator decides whether to preserve the running point and disclose the tiny
target mismatch; no permission to add another model cell follows from this erratum.

Checks: actual X43 floor reconstructed from FP0 must equal logged calibrated CORE_RECORD floor within1e-12;
critical-level rescaling must substitute to ratio1 within1e-12; inputs stable. No CLASS run or fitting is needed.
