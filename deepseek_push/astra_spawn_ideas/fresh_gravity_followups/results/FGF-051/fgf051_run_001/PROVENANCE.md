# Source and execution provenance

Worker: `/root/fgf051_author`; execution `/root/fgf051_author:fgf051_run_001`.
The exact model identifier is not exposed to this child and is not inferred.
Task SHA256: ee8c6a996506cd502deaa255a9859b2f2ce7bdf0aa011aea7b51dda0f6f6a4cc.
An exclusive claim was reserved by the coordinator before dispatch. All writes
are confined to this run directory; no other agent was spawned.

All ten task ancestry pins were SHA256-checked and matched before source text
was read. Task text was read to extract the expected pins; then all pins and
the task's supplied hash were checked. Exact inputs and contract hashes are
in input_sha256.json. The inherited Git base is
 eccd1c0e59459b5ec1acf2e916fb7a05a7f67971;
the shared working tree is dirty, so actual bytes, not Git alone, identify
inputs. No new stage38 root or reviewer proof/preview was read. A parent
message that the reviewer had frozen supplied no mathematical content.

Text consulted: FGF048 DERIVATION sections 1-9, especially exact equations,
chart (2.1), first-gradient block (3.1), Lipschitz/restart section 5 and
compatibility/energy sections 7-8; FGF050 DERIVATION sections 1-7;
FGF050 reconciliation, corrected ancillary display, previous root transport
check and its review, NEXT_ROUTE and FGF047 reconciliation. Pinned old result
JSON files were used as hash ancestry only, not mathematical premises.
The common framework and result contract were read. Ownership claim was
inspected only for scope; its mutable running status is not a proof input.
No new mathematical theorem is imported from that bookkeeping.

Using mathbox proof-audit for the author self-review and proofread-math for
final mathematical proofreading. research-program was read for provenance and
scope but its sustained portfolio is not applied: the delegated task requires
one bounded derivation, not a new broad research program. No literature
mechanism, external theorem, historical novelty check or network query is used.

Administrative operations were filesystem reads (`cat`, `sed`, `wc`, `rg`),
Python SHA256 checks, writing these Markdown/JSON/Python metadata artifacts,
and the read-only verification command below. No mathematical executable
experiment, numerical parameter sweep, symbolic computation or simulation was
run. Thus numerical wall/CPU/thread/log bounds are not applicable, and no
memory cap is claimed. The recorded run start 2026-10-06T07:43:36Z is the
observed UTC output-directory initialization time after initial source reading;
it is not represented as an exact dispatch timestamp.

Replay administrative verification from the repository root:

    python3 deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-051/fgf051_run_001/verify_metadata.py

This prints only JSON on stdout and performs no writes, clock reads or
scientific tests. It checks required result keys, source/artifact/freeze hashes,
all ten pinned ancestry entries and equality of source maps. Freeze excludes
itself to avoid self-reference and includes result.json. result.json's artifact
map excludes itself and FREEZE.json; input_sha256.json is also a pinned output.
No timestamped mutable validation file is created. Replaying the verifier
therefore preserves all frozen bytes.

Scientific content is proof-only over all sufficiently large integers N with
fixed positive compatible backgrounds/coefficient choices. No finite tested
range, random seed, numerical tolerance or observed empirical data is claimed.
Independent review must cite the final result/derivation hashes before any
promotion beyond this author candidate.
