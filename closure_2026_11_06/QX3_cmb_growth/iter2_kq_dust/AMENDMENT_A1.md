# QX3 iter2 Amendment A1 (post-bug, after G1's first printed number; disclosed)

The first G1 stage printed a worst-corner chi^2 of 44.27 (iter2_bug_lCl_only.out). Debugging found the cause: CLASS run with
`output: lCl` alone returns a truncated C_L^phiphi. Against FFP10, X/FFP10 was 0.68 at L = 10 and 0.11 at L = 400. With
`output: tCl,lCl` it is 1.00 and 0.95. Every G1 number in that output is void.

Changes, nothing else:
- run_class uses `output: tCl,lCl` (plus mPk where needed).
- New code check K1b: a CLASS reference run (h 0.67, omega_b 0.0224, omega_c 0.12, n_s 0.965, A_s 2.1e-9; a code test only,
  never a model or verdict input, as in CFG917's K tests) must give X/FFP10 within 10 % at L = 10, 40, 100 and 400.
  If it does not, G1 is NO VERDICT.
Lines, gates and labels are unchanged.

## A1b (numerics only, before any G2 number)

The growth ODE is integrated vectorised over k with implicit midpoint on a fixed 6001-step ln a grid (plus the output epochs).
This replaces per-k LSODA, which was too slow on deep sub-Jeans modes. K2 test run: R at mu = 1e6 deviates by at most 2.2e-4
(line 1e-3). Deep sub-Jeans modes (k/(a mu) > ~180) have unresolved phases. Their amplitude stays bounded at its generous
initial value, so this does not tighten mu_min.
