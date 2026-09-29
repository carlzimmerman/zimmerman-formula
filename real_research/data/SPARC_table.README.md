# `SPARC_table.txt` is not data

`SPARC_table.txt` in this folder is a 196-byte HTML "404 Not Found" page (sha256 `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880`). The download failed when the file was first committed (e1603604aa, 2026-03-17). The later repo reorganisation (999f94dfee) only moved it here from `data/`.

**Use these instead:**

| what | file |
|---|---|
| SPARC Table 1 (175 galaxies: T, D, e_D, f_D, Inc, e_Inc, L[3.6], Reff, Rdisk, MHI, RHI, Vflat, Q, refs) | `SPARC_Lelli2016c.mrt` (the SPARC site's own filename for Table 1) |
| 10-column extract of Table 1 | `sparc_master_clean.csv` |
| rotation curves and baryonic components (the Table 2 content) | `sparc_data/*_rotmod.dat` (175 files) |

Checked 2026-09-29: the `.mrt` has 175 rows whose names match the 175 rotmod files exactly, and `sparc_master_clean.csv` agrees with the `.mrt` on all 10 of its columns (0 mismatches).

**Audit, 2026-09-29.** No script on any branch has ever read `SPARC_table.txt`. `git log --all -S SPARC_table` over `*.py`, `*.ipynb` and `*.sh` finds only `deepseek_push/L06_rar_moment.py`, which names the file only to say it was not used. So nothing parsed the 404 page, and no committed number was computed from it. It is the only HTML page among the 88,283 tracked data files. Some docs listed it as a data source (the qwen_claude_field_theory protocol and idea prompts, swarm-week packet F2, and the SPARC row of `data_assembly/timeline/sample_ledger.csv`). None of those tasks was run, and each doc now has a correction appended.

**Why the file is kept unchanged.** Its sha256 is pinned in `real_research/swarm_week_2026_09_20/INPUTS.json` and in the handoff mirror manifest. Replacing its content or deleting it would break those pins, and a replacement would add a second copy of Table 1 under a misleading name.
