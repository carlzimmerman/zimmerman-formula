# Actual provenance

- Worker: current child agent `/root/fgf048_author`. No explicit model override
  was supplied to this child; exact model identifier is not exposed here.
- Repository HEAD observed: `36b9957612c8b422e900874fb053c6baa22456e4`.
  The working tree is shared; actual input bytes, not HEAD alone, are pinned.
- The parent supplied the exclusive run reservation and ownership/deduplication
  assessment. This worker did not repeat, edit, or promote shared queue/claims.
- Task SHA256 matched `028ae73e50048d0412fde4d5ddd88e1b94e8bd127d75b80fc952382fdeb4b377`.
  All eight ancestry pins matched before proof development. Chronology:
  old FGF047 derivation/reconciliation/result and old audit JSON content were
  read immediately before the ancestry hash-check call; the match is actual,
  but this is not described as a hash-before-first-read sequence. Other pinned
  mathematical texts were read after that check.
- No new stage35 author-comparison/root/reviewer proof or frozen route was
  read. Parent progress notices reported reviewers were ready; no reviewer
  mathematical conclusions or derivations were supplied.
- Applied skills: research-program, proof-audit (author self-review), and
  proofread-math (self-review of newly written files), from the installed
  mathbox 3.2.0 skill files. Their route protocol and proof obligation
  checklists were read. No local `.mathbox` ledger exists at repository root.
- First explicitly recorded author UTC timestamp: 2026-10-06T04:41:14Z,
  obtained after initial source reads. The result `started_utc` uses this
  first recorded checkpoint rather than inventing an earlier start time.
- Administrative inspection used `pwd`, `rg --files`, `cat`, `sed`, `shasum`,
  `git rev-parse HEAD`, `ls`, `find`, `date`, and a short Python SHA256 loop.
  The `ls .mathbox` check reported no such directory; no mathematical check
  failed. No network, installation, service, commit or outside-scope write.
- Proof-only result commands are empty as allowed by RESULT_CONTRACT.json.
  The reproducible administrative verification command is:

      python3 deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-048/fgf048_run_001/verify_metadata.py

  It checks task/ancestry/current inputs, required result fields, frozen
  artifact hashes and result hash. It is not a PDE simulation or mathematical
  computation. Its actual output is retained in VALIDATION.txt.
