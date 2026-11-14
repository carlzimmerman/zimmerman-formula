# PAPER72 v1.5 DRAFT insert (2026-11-14, written 13:58 EST by the clock; NOT DEPOSITED)

The owner asked for a draft of version 1.5 that folds in lane XJ1's junction finding. Nothing here is deposited, and
no deposit is made without a new go from the owner.

**Why an insert and not an edit of the paper.** When this draft was started, another tool was editing the paper's
source, its audit and CJ1's two files in the shared checkout (uncommitted; a dated local correction of the
crossing-speed argument, with its own folder `codex_mass_budget_2026_11_14/`). Two writers on one file lose work, so
this draft does not write under `qwen_claude_field_theory/papers_2026/`. It is a script of anchored edits:

- `apply_v1_5.py` reads the paper's current TeX and audit, applies the version 1.5 edits (every anchor must occur
  exactly once or it stops) and writes `out/PAPER72_v1_5_DRAFT.tex` and `out/PAPER72_audit_v1_5.py`.
- `out/` is generated and not committed: it contains whatever the shared source holds at the time, the other tool's
  uncommitted correction included. Regenerate it with `python3 -I -B apply_v1_5.py`; build with
  `tectonic out/PAPER72_v1_5_DRAFT.tex`; audit with `python3 -I -B out/PAPER72_audit_v1_5.py`.

**What the edits are.** The version line; one abstract paragraph; a paragraph "What changed since version 1.4"; one
item in Section 6; one sentence each at the end of "f, edge by edge" (Section 9.1) and of Section 10.4; a new Section
11 (the junction of versions 1.3 and 1.4; the law itself inside; the post hoc caustic cases; FWN2 and the blind RRL1R;
the lanes table; where this leaves the form); estimate (xxiii); a Method paragraph; and 60 audit checks, each quoting
a committed file of XJ1, FWN2 or RRL1R.

**State at first build (13:58).** The merged copy builds (37 pages). All 60 new checks pass. 108 older checks read
"uncommitted": every one of them cites CJ1's `COMPLETED_FORM.md` or `SCORECARD.md`, or the other tool's snapshot
folder, whose working copies differ from any committed copy. They clear when those edits are committed.

**Still to do before this could be deposited.**
1. XJ1's bracket stage: the fragility flag of each label, then one sentence in Section 11.3 and the labels in its two
   tables (`LAB` and `BRACKET_SENTENCE` at the top of the script).
2. XJ1's second build and the blind lane XJ1R for the caustics: Section 11.3 says they were running; if they land
   first, they go in.
3. The merge into the shared source once the other tool's correction is committed, CJ1's scorecard update for XJ1,
   the supplement rebuild and the Zenodo metadata for version 1.5 (a new version of record 24221457).

The lead checked the other tool's correction of the crossing-speed argument independently in SI: at the virial radius
of the full share, with the same baryon mass, the law's enclosed mass is above the share for every system slower than
1.185 v* and below it for faster ones (5.1 times at log M_b 9, 1.67 at 12, 0.82 at 14, canonical), which is the reverse
of the sentence in versions 1.3 and 1.4. So the crossing speed is an intersection of two scalings, not a derived switch.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
