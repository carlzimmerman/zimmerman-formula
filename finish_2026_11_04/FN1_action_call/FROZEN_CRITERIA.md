# FN1_action_call: frozen criteria

Committed alone, before the brief, any script or any number. Item 1 of the finish push (`../README.md`). κ = ½ FITTED.
Footings canonical a0 = 9.3603e-11 and alt 1.1312e-10 m/s², never pooled. Not theory closed. Nothing here says the data
favour the framework. The cold sector stays retired. No dark-matter particle. Not blind: AX1, C6P, V3W, the v3s verdict,
KT14–KT34, CZ1–CZ5, CW1, CW3, CFG691, CFG820, CFG821 and AS3 were read first.

## What this lane makes

`DECISION_BRIEF.md`, for the owner, on PAPER67's requirement 12, "have an action". It lays out three options:

- (a) v3s as it stands (frozen 10-24; regraded under the owner's 11-04 lift; adopts nothing);
- (b) a covariant smoothed-QUMOND action with a fixed universal length;
- (c) no action selected, so requirement 12 stays open and is stated as open.

For each option the brief gives:
1. what passes and what fails, with numbers and the commit or file each comes from;
2. what is ungraded;
3. what finishing it would take;
4. what PAPER67 and STANDING.md would then say, as proposed text. Neither file is edited here.

It leads with a one-paragraph bottom line. It recommends adopting nothing; the choice is the owner's. It may say which
option leaves the fewest ungraded doors. An ungraded door is a gate with no verdict on record for that option. The
gates counted are AX1's G1–G5 plus the 10-24 verdict's scope: clusters, growth and CMB, the radiation era, hosted dwarfs,
the Milky Way disc and caustics.

## Step 2, decided from the record before any script

Option (b)'s static limit at one universal length is **not** fully graded on the current gates (the Newtonian host
field in ν; the 3D field where a saddle matters):

| gate | what the record has at a fixed universal length | graded? |
|---|---|---|
| Milky Way cells | KT14, source-only rule, 0.25 / 0.5 / 1 / 2 kpc; no host field, so no CZ1 defect. Nothing at 24–100 pc. The action-derived (reciprocal) form of KT33 was graded only at ξ = r_M/2, never at a fixed length | partly |
| 24 Local Group dwarfs | KT15's 2 kpc arm only, alt only, with the CZ1 defect. CZ1/CZ2 fixed the scaled and local arms, not this one | defect only |
| Cassini Q2 | KT16's 2 kpc arm only, with the CZ1 defect, through KT16's flux integral. KT33 shows that integral omits an origin surface term once the Sun is smoothed | defect only |
| planets | CZ3/CZ4 graded r_M-scaled and local widths only | no |
| SPARC | KT19 graded ε = 0.55 r_M only | no |

So `FN1b_fixed_length_static/` runs under its own `FROZEN_CRITERIA.md`, committed alone before its scripts. The brief
reports its frozen label, whatever it is.

## check_brief.py (PAPER67_audit.py's pattern)

- A list of (fragment in the brief, source file, literal in that file). A row passes when the fragment is in the brief
  and the literal is in the source.
- **Coverage.** Every number in the brief must sit inside at least one checked fragment. A number is a digit run not
  joined to letters or underscores, so lane names such as KT14 are not numbers. Dates, commit hashes and file names are
  stripped before the scan. An uncovered number is a failed check.
- **Forbidden in the brief:** "theory closed", "kappa derived", "κ derived", "favour the framework" unless preceded by
  "Nothing here says the data", "measured flat", "/Users/", and personal names.
- **Required in the brief:** "κ = ½ FITTED", "not closed", "adopts nothing".
- **MUTATE (`--mutate`).** Bump the last digit of each source literal. The twin passes when at least 80 % of the bumped
  literals are no longer found, with every survivor listed (PAPER67_audit's line).
- Exit 0 only if every check passes. `check_brief.out` and `check_brief_MUTATE.out` are committed.

## Rules

No downloads, deposits or sending. PAPER67, STANDING.md, the v3s verdict and every other lane are left unedited.
No home paths or personal names in committed files, logs included. Commits add these files by explicit path only.
