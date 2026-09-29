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

**Live check, 2026-09-29.** `SPARC_Lelli2016c.mrt` is byte-identical to the copy on the SPARC site, `https://astroweb.case.edu/SPARC/SPARC_Lelli2016c.mrt`. Both files are 28,259 bytes with sha256 `5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243`, and `cmp` finds no differences. The server gives `Last-Modified: Mon, 28 Mar 2016 21:07:01 GMT`, so Table 1 has not been revised since publication. The old host `astroweb.cwru.edu` (the address in the March 2026 appendix) no longer accepts connections. The live SPARC index lists no file named `SPARC_table.txt`.

**Rotation-curve check, 2026-09-29.** All 175 files in `sparc_data/*_rotmod.dat` are byte-identical to the files in the SPARC site's `https://astroweb.case.edu/SPARC/Rotmod_LTG.zip`. The zip is 110,737 bytes, sha256 `0a80cc90714828cc28b7dd57923576714d209f2490328c087c4a4ad607faf588`, `Last-Modified: Fri, 25 Mar 2016 21:38:04 GMT`. It contains exactly 175 `*_rotmod.dat` files with the same names as the repo set, and nothing else. A file-by-file `cmp` finds 0 differences. The repo's 175 files are tracked and unmodified in the working tree. For a quick re-check without the zip, the combined sha256 of the repo set is `11d8822ec2254170cfd050f851f9f6231e2d2188820bb6b18f573fba5cdb8d4c`. It is computed over the files sorted by name, hashing each file's name, a NUL byte, then its bytes.
