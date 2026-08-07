# D01 — Actually load SPARC. Nothing in this folder ever has.
COST: M | script: `mi_sparc_loader_2026.py`

> ENGINEERING / DATA task. Import `TOOLS/mi_constants.py` — never retype a constant.
> `../02_HOUSE_RULES.md` and `../03_NUMERIC_HAZARDS.md` apply.

## The gap this closes
The 2026-08-07 review grepped for `loadtxt|read_csv|genfromtxt|Rotmod|MassModels` across the whole of
`qwen_36_experiment/` and found **nothing** — zero data loads. Every "SPARC confirms" and "236 galaxies" in
tn26 is unbacked *in that folder*. Fix it once, properly, and every later task reuses it.

## Do
1. Locate the SPARC data in the repo (search `real_research/` for Rotmod / SPARC tables — the committed
   `rar_framework_a0_mlfit.py` loads it; read that and reuse its parsing rather than reinventing).
2. Write a loader returning, per galaxy: name, R, V_obs, e_V, V_gas, V_disk, V_bul, distance, quality flag.
3. Reproduce two committed numbers as correctness checks: the RAR residual **0.108 dex at Υ = 0.70**, and the
   sample size after the standard quality cuts. If you cannot reproduce them, your loader is wrong.
4. Save it as an importable module and say so in the ledger, so D02–D04 build on it.

## Settles if
The loader reproduces both committed anchors. That is the whole test.
