# Exact research inputs

The associated PN28/VR28 and one-shot-review records were produced in a
shared checkout with active, untracked Claude research. INDEX.json preserves
the exact current input bytes missing from the committed base, with their
original paths and hashes. Active source directories are not included in
this commit. Original run manifests retain their own version claims; a
current snapshot does not repair a historical stale hash.

On a clean checkout, materialize missing inputs before validating manifests:

    python3 research_inputs_2026_10_28/materialize.py --root .

The helper creates missing files only, verifies existing matching files and
refuses to overwrite differing files. Alternatively use a disposable clone
as the root. The snapshots are repository research inputs, not fetched full
external papers.
