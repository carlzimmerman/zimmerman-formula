# Open items, consolidated into the orchestrator chat (2026-10-02)

The owner said (2026-10-02): **"consolidate everything into this chat please"**.
- The single working thread is now the orchestrator ("Complete gravity theory"). This supersedes the 09-26 single-thread rule.
- Peer chats finish only what is already running under an owner's yes. They send one ANSWER-ROW per result and start nothing new.
- New owner yes-items reaching a peer are relayed here.

## Running (launched from here)
| item | what | where |
|---|---|---|
| CFG290 | hostile MNRAS referee of the v3 manuscript (32f9a609c) | campaign_fresh_gravity/CFG290_mnras_v3_referee/ |
| CFG291 | khronon dipole radiation in binary pulsars over the chassis window (recipe G7/G11; never run before) | campaign_fresh_gravity/CFG291_khronon_binary_pulsar/ |
| CFG292 | strong hyperbolicity of GR + the BPS khronon; criterion-B cone compatibility (XC2's OPEN item) | campaign_fresh_gravity/CFG292_khronon_strong_hyperbolicity/ |
| CFG293 | CFG288's wave field → solitonic cores → the satellites (inside-r_half rule CFG286 requires) | campaign_fresh_gravity/CFG293_wavefield_cores_satellites/ |

## Finishing in peer chats under the owner's earlier yes (an ANSWER-ROW will arrive here)
- **MIGHTEE-HI r1p0 download** (High-z chat): 4 cubes, 24.4 GB, cap 30 GB, to `_external_data/mightee_hi_dr1/`, outside the repo. It runs in the owner's Terminal tab "MIGHTEE download" and resumes on restart (fetch_mightee_r1p0.sh, fetch.log, FETCH_MANIFEST.jsonl).
- **CFG300** (calc chat): MIGHTEE cube cutout probe, cap 10 GB (≈198 kB used so far). Three targets are fixed by rule from the paper's Table 3. The question it answers: resolved rotation curves, or widths only?
- **CFG301** (calc chat): criteria DRAFT on the catalogue columns only. Freeze and launch it from here once the table exists.

## Needs the owner
1. **Zenodo deposits:** the owner runs them, because the classifier blocks Claude's publish.
   - PAPER39 v1.1: `python3 zenodo_publish_paper39.py`.
   - PAPER35: `python3 zenodo_publish_paper35.py`. It must be public before Gaia DR4 (2 Dec 2026).
   - Then record the DOIs. The README / STANDING row for PAPER38 v1.3 (10.5281/zenodo.23108862) is not yet added.
2. **MIGHTEE-HI catalogue table** (arXiv:2605.28731, MNRAS supplementary): it sits behind an OUP Cloudflare bot check, so the owner downloads it in a browser, or asks the first author ("data on request"). The record and column schema are in data_assembly/mightee_hi_catalogue_2026-10-02/ (d4229dba2).
3. **CFG287's open item:** the journal (published) versions of RC100 (ApJ 944, 78), FS+18 and Umehata+25. None is on disk; fetching them needs a yes.
4. **Home paths in committed code:** 585 committed .py files hard-code the owner's home path, which contains the name. A forward fix to relative paths is possible; history is never rewritten.
5. **Before DR4:** a registered Gaia archive account.
6. **MNRAS v3:** submit after CFG290's fixes. The checklist notes the APC £2,356 and that the waiver form goes to OUP at the same time as submission.
7. **Older items still awaiting a go:**
   - PAPER34 v3 (not deposited);
   - Amendment 15 and the author-ask (09-28; check STANDING before acting);
   - the JWST Cycle 6 proposal stays PRIVATE (never publish it before review).
   - Not to be deposited: PAPER37, which PAPER39 supersedes.

## Carried artefacts
- **The shared a₀(z) artifact:** https://claude.ai/artifact/4CmdAxm5XqZ9QWRXWQ2zjA (v21). It mirrors chart_a0z_one.py at 374d54a77. Its data are inline, so update it with Artifact read + republish using `url`. Its build sources were in the High-z chat's scratchpad and are not in the repo.
- **The chart README** (CHART_a0z_rar_z0_5_2026-10-01/README.md) documents every lane's drawing choice.
- **The fetch helper** data_assembly/fetch_range_logged.py (host allow-list + cumulative cap). The ADF22 arXiv PDFs are in `_external_data/arxiv_pdf/`.

## Update 2026-10-02 (evening)
- **DONE:** the MIGHTEE-HI catalogue table is in the repo (the owner's browser download; 19adffd49). The r1p0 cubes are complete (24.31 GB, checksummed, 4 files). Disk free is ~33 GiB.
- **DONE:** MNRAS v3.1 is committed and tagged `mnras-v3.1` (51413cc1b) with both owner decisions: PAPER6 dropped; AI disclosure names Claude, OpenAI, DeepSeek, GLM, Qwen and Gemini.
- **Running:** CFG301 (catalogue a₀ + direct BTFR) and CFG302 (raw cube widths).
- **Still needs the owner:** a second referee pass on v3.1 before submission (recommended); optionally run `bash reproduce_all.sh` personally so the "author ran the scripts" wording can be restored.

## Update 2026-10-03
- **Owner approved (in this chat):** the DESI DR1 lensing repo, the rest of the KiDS shear catalogue (~10.6 GB), the DESI BGS catalogue (~5.2 GB) and the CIGALE masses (~7.3 GB). CFG315 and CFG316 are running.
- **Needs the owner:** an HSC account for the HSC Y3 shapes; a decision on the DES Y3 shapes once CFG316 reports their size.
- **Needs the owner:** MNRAS v3.3 submission steps; PAPER40, PAPER39 and PAPER35 deposits.
