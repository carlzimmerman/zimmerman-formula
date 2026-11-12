# A5: audit of Codex merge 2207a1df48 and the other recent Codex branches (2026-11-12)

Read-only. Refs: A = `codex/backup-main-before-merge-2026-11-12` (2ffc012fa5, = merge parent 1), B = `codex/backup-origin-main-before-merge-2026-11-12` (729090afac, = merge parent 2),
M = `origin/main` = 2207a1df48 (merge, 2026-11-12 11:38:20 -0500). Merge base of A and B: 95435f152c (11-07).

## 1. Nothing lost

- `git merge-base --is-ancestor A origin/main` -> yes; same for B -> yes.
- Paths in A absent from M (`git diff --no-renames --diff-filter=D A M`): 2.
  - `qwen_claude_field_theory/papers_2026/PAPER70_supplement_lean_and_record_2026.zip` (blob 508e0df6fd):
    MOVED, byte-identical, to `PAPER70_supplement_archive/500b55e31a/` (same blob). Deliberate archive.
  - `prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-05c_DR4_SEED_MEAN_NSS_OFF_DRAFT.md`: RENAMED on the B side
    before the merge (a35171230f, owner "Yes, check and file", file renamed from _DRAFT; rename similarity 76%,
    status block added). Not lost; the merge took B's rename.
- Paths in B absent from M: 0.
- Paths in M in neither parent: 3, all in `PAPER70_supplement_archive/500b55e31a/` (zip, A's old manifest, README).
- Files changed on both sides since the base: 2,689. Of these 2,682 are identical on both sides (patch-equivalent
  replays of the same commits). Result equals NEITHER parent: **0 files**. Side taken where they differ:
  - B (remote): `closure_2026_11_06/CLOSURE_FINAL.md`, `closure_2026_11_07/CLOSURE_REGISTER.json`,
    `closure_2026_11_07/build_paper70_supplement.py`, `PAPER70_field_equations_closure_2026.zenodo.json`,
    `PAPER70_supplement_manifest.json`, `PAPER70_zenodo_publish.py`. The A-side commits behind A's versions
    (54ba271771, b45650d209, bf8b7c9c58, a9063fbd08) all have patch-equivalent twins in B (`git log --cherry-pick`),
    and B's versions are later (e.g. CLOSURE_FINAL records the Pi^6 adoption; publish.py keeps the committed-manifest
    gate as d47d5589aa). Nothing of A's content is missing from these six.
  - A (local): `closure_2026_11_10/NH2_ngc1052_host_mass/RESULT.md` (A carries the real local/origin commit ids;
    B had "see the ids commit"). Matches the merge message.
- Modes: three scripts are 100755 in A, 100644 in B, 100755 in M (`CMB1.../run_c.sh`, `F1A.../run_fits.sh`,
  `GL3.../gl3_sandbox.sh`): A's executable bit kept, as the message says.

## 2. No rewrite

- `git rev-list --count`: A 13,772; B 13,949; M 14,520. Unique to A (B..A) 570, unique to B (A..B) 747.
  13,772 + 747 + 1 (merge) = 14,520: every commit of both parents is reachable; none dropped.
- B (previous origin/main tip) is an ancestor of M: yes. The push was a fast-forward of origin/main.

## 3. Lane folders (all under `closure_2026_11_10/`)

`git log -1 origin/main -- <dir>` then `git diff --quiet <that> origin/main -- <dir>`; also checked equal to BOTH parents.

| folder | last commit | = last commit | = A | = B | files |
|---|---|---|---|---|---|
| DSB1_dwarf_systematics_blind | a6cb044a13 | yes | yes | yes | 12 |
| EDG1_held_edge_layer | d1881ba1bd | yes | yes | yes | 24 |
| HLF1_own_halo_list_forest | bf412d9a8d | yes | yes | yes | 53 |
| FRZ1_forest_redistribution_at_z | 42f4d537ab | yes | yes | yes | 16 |
| FRZ1R_blind_forest_regrade | fc60c7b801 | yes | yes | yes | 13 |
| FRZ2_forest_a0_of_z | fe938ded32 | yes | yes | yes | 40 |
| EFN1_external_field_nonlinear | 1b4d90250f | yes | yes | yes | 39 |
| R541_why_the_cold_share | 87789ab5bc | yes | yes | yes | 10 |
| R541A_clock_matter_coupling | ae86f8c505 | yes | yes | yes | 10 |
| R541B_early_symmetry_breaking | 35cfd71c0a | yes | yes | yes | 18 |
| R541C_made_in_inflation | 12970cf520 | yes | yes | yes | 9 |
| R541D_baryon_current_cogenesis | fab7dad5c9 | yes | yes | yes | 6 |
| R541E_b_minus_l_variant | e9ad45e8e3 | yes | yes | yes | 6 |

None was touched by the merge. Only working-tree note: FRZ2 has one untracked `run_all.done` marker.

## 4. PAPER72 v1.1 (DOI 10.5281/zenodo.24125791)

`git diff --stat 31393f05ee origin/main -- 'qwen_claude_field_theory/papers_2026/PAPER72_*'` -> empty. **Identical.**
31393f05ee is on the B side; its local twin 8f2471cf7e (same message, 3 s earlier) is on the A side, and
`git diff 31393f05ee 8f2471cf7e -- PAPER72_*` is also empty. The deposited files did not change.

## 5. PAPER70 supplement move

- The ZIP (blob 508e0df6fd) existed only on A, added by f639380e36 (11-11 23:39, "FINAL mile"). It and A's manifest
  (git_head 500b55e31a, 868 files) moved together to `PAPER70_supplement_archive/500b55e31a/` with a README.
  B never had the ZIP. The canonical `PAPER70_supplement_manifest.json` is B's (git_head a74f342f7d, 1,023 files,
  introduced by 047b6de1f9, 2026-11-09 14:50, the PAPER70 v2.1 deposit manifest); its ZIP is not in the tree.
- "Two stale canonical-manifest hashes": all 1,023 entries match their own git_head a74f342f7d. At B and at M,
  2 do not: `closure_2026_11_07/CLOSURE_2026_11_07.md` and `closure_2026_11_07/CLOSURE_REGISTER.json`, edited after
  the deposit on the B side (d81f1ac743 11-09 14:51 deposit record, eb7ae1668a, a620292b45, 1ca52c1ef3 11-10).
  The mismatch predates the merge, as claimed. It is expected drift of a deposit snapshot, not damage.

## 6. Local state

- `git rev-list --left-right --count HEAD...origin/main` -> `1 0`.
- The extra local commit is cace4617bb (11:46:31, after the merge): "Z196 ops note: correction session in-flight
  (G238/G240/G241/G242 + DS_FINAL fix-forward)", one appended line in `deepseek_push/CANDIDATE_LAWS_REGISTER.md`.
  Parent = origin/main, so it would fast-forward. Content is harmless, but it belongs to the conductor cron session
  whose correction work is still uncommitted; leave the push to that session. Not pushed here.
- `git status --short | grep -v '^??'`: 59 modified tracked files, among them the in-flight deepseek_push
  G238/G240/G241/G242 and DS_FINAL files, fable52_push PIK1/FRM1/CLOSURE, closure_2026_11_11 FINAL3/4/6,
  closure_2026_11_12/OUT4, SS2 cosmo outputs, `DOORS.md`, `fable_independent_2026/lean_2026/lakefile.toml`,
  hy4_preview_push CLOSE-1_DT2. These are other sessions' live work, not merge debris.

## 7. Other Codex branches newer than 11-05, not ancestors of origin/main

- `codex/euclid-desi-review-2026-11-12` (local + origin, 8db464d4bc, 4 commits on 729090afac, 69 files, only
  `research_closure_2026_11_12/euclid_desi_release_review/`). Review; claims NO new observational pass.
- `codex/response-kernels-2026-11-08-rk03` (4607e420cc, 1 commit, 58 files, `response_kernel_2026_11_08/`, none on
  main). RK03 vector self-current kernels; "Objective unresolved", fails its cluster/disc lines; adopts nothing.
- `codex/pool-finite-halo-2026-11-06` (93836ea737, 31 commits, 226 new files under
  `action_scale_investigation_2026_11_05/joint_phase/`). Coupled-condensate pressure, Lean conditional theorems;
  claims an obstruction (edge-speed exponent >= 6/5, no universal v^4 scaling) and that nothing selects 1/2. No adoption.
- `codex/merge-yesterday-2026-11-12` = 2207a1df48, already in origin/main. Backups: ancestors (section 1).

Euclid review (the "Nov 12 Euclid review" of the merge message), five lines:
1. Reviewed all 26 Euclid DR1-Foundation manuscripts (targeted, not line-by-line), DESI DR2 public products, and
   22 prior prediction lanes in this repo, to find executable tests of a0 = kappa c sqrt(G rho_DE).
2. Concluded: no new observational pass; best lead is an angular T = D_A a0 observable plus a conditional joint
   BAO closure, which survives derivation but has a material robustness limit (an omitted radial stellar gradient
   biases T by 0.30-0.63 dex); calibrated weak shear is deferred to 2027.
3. It flags that SP1/SP2 sealed criteria have inequality directions that conflict with their text, and that A55's
   fixed-normalization SLACS fail stands next to A85; it repairs and scores nothing.
4. Downloads: 26 PDFs + 2 ECLIPSE catalogue ZIPs (3.7 MB + 27 MB, Zenodo 19654904), about 280 MB in all, in
   `/private/tmp/euclid_dr1_review_20261112/` outside the repo, untracked; not redistributed. 4 small SPARC files
   copied from the repo into the branch with hashes. A 236 MB archive and 4 GB images were left untouched.
5. Tracked by git only on the branch; on main the same 69 files sit untracked (byte-identical to the branch).

## Verdict

**MERGE CLEAN WITH NOTES.** Nothing lost: both parents are ancestors, no commit dropped, 0 files equal neither
parent, the only path removals are a byte-identical ZIP move into an archive and a pre-merge owner-filed rename.
Notes: (a) 6 conflict files took B and 1 took A, each the later or more complete record; (b) the canonical PAPER70
manifest is 2 entries stale since 11-09/11-10, inherited; (c) PAPER72 v1.1 unchanged; (d) local cace4617bb unpushed,
belongs to the live conductor session; (e) three Codex research branches (Euclid review, RK03, pool/finite halo)
remain unmerged, none claims a pass or adopts anything.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
