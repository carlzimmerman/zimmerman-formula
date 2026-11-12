# PIK1 forward correction: the bounded quadratic check (2026-11-12)

`check_quadratic.py` is a byte-identical copy of the check another session wrote for `../CORRECTION_2026_11_12.md`:
the second-order action of the gated dust term about FRW, by direct variation and from the quadratic action, plus the
two scope counterexamples for FRM1's ceiling. It is placed here so that the lane's `pik1.py` and `pik1_var.py` stay
exactly as first committed (one is a stub, the other does not compile; that is the record).

Run here by the lead session: `python3 check_quadratic.py --output check_quadratic.json` (STATUS=PASS, byte-identical
JSON to the other session's own run) and with `--mutation drop-mixed` and `--mutation drop-divergence-square`
(both exit 1 with STATUS=FAIL, as a mutation should). The `.out` files are the captured standard output.

It is a quadratic check on a fixed metric. It does not compute any of PIK1's rows, and it is not a coupled-gravity
spectrum. Independent check: `reviews/codex_corrections_audit_2026_11_12/C2_pik1_and_frm1.md`.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
