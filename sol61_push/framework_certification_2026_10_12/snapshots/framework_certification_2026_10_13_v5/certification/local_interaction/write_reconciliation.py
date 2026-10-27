from pathlib import Path
import json,hashlib
h=Path(__file__).resolve().parent;ctx=json.loads((h/'CONTEXT_RECONCILIATION.json').read_text());old=json.loads((h/'run/results.json').read_text());new=json.loads((h/'run_reconciled/results.json').read_text());mf=json.loads((h/'run_reconciled/manifest.json').read_text())
assert (h/'run/results.json').read_bytes()==(h/'run_reconciled/results.json').read_bytes()
assert hashlib.sha256((h/'run/manifest.json').read_bytes()).hexdigest()==ctx['original_run_manifest_sha256']
assert hashlib.sha256((h/'context_historical_hash_matched.txt').read_bytes()).hexdigest()==ctx['historical_sha256']
oldverification=h/'verification_original.json'
if not oldverification.exists():oldverification.write_bytes((h/'verification.json').read_bytes())
report=f'''CONTEXT FRESHNESS RECONCILIATION — FRAMEWORK-CERT-TRANSPORT-2026-10-12
This supplements RESULT.txt; it does not overwrite the original evidence or
retroactively change its execution status, inputs, claim count or hashes.

Only stale contextual input
---------------------------
{ctx['context_path']}
Historical: {ctx['historical_bytes']} bytes, sha256 {ctx['historical_sha256']}.
Current: {ctx['current_bytes']} bytes, sha256 {ctx['current_sha256']}.
Current producer publication208e62e10e contains the latter exact bytes.
The historical bytes were recovered by reversing the three explicit additions
observed against the earlier complete tool read, then validated AGAINST THE
EXACT ORIGINAL SHA256. They are preserved as context_historical_hash_matched.txt.
This is an exact verified reconstruction, not an approximate quotation or claim
that the producer supplied a cached copy. context_current_snapshot.txt preserves
the current read; context_delta.patch provides all differences.

Exact substantive delta
-----------------------
1. Intro now identifies a DISTINCT two-local-field spatial continuation that
   provides actual streaming and flat-space prototype stress, while physical
   coupling, microscopic origin, action and selector remain open.
2. Provenance now records a third pre-run criteria commit
   d7e7b0dbc6afd3a73232ed70ab03ef773cb51cc9 for local_run, and its changed
   field assumption/supplemental exact omission control.
3. New LOCAL CONTINUATION paragraph distinguishes that prototype from the old
   global two-mode receiver; it explicitly retains gravity, coupled action,
   microscopic rate and selector as open, with zero/aligned-state inactivity.
The existing phi/chi charged carrier action, all symbolic checks and original
RESULT open-interaction statements used by this agent are otherwise unchanged.
The prototype is not a newly supplied phi/chi-to-receiver microscopic vertex.
Our physical interaction/DE/selector boundary therefore does not change.

Scientific versus contextual dependence
---------------------------------------
checks.py reads no producer RESULT.txt or other repository input at runtime; its
identities are directly coded from the pinned existing charged-carrier action.
The producer result was declared as contextual interpretation provenance in the
original contract; input freshness validation correctly treats its changed bytes
as a mismatch. This does not falsify the31 computed identities, but means the
old manifest cannot be called CURRENT-SOURCE valid at this moment.
No recorded hash has been silently refreshed. The old run/manifest and INPUTS
remain byte-identical historical-context evidence, with matching recovered old
source snapshot. We classify that run as HISTORICAL CONTEXT / NOT CURRENT-SOURCE
FRESH, not as a new physical failure or a still-valid current input record.

New actual execution
--------------------
INPUTS_reconciled.json pins the CURRENT contextual source/locators and preserves
the original inventory as history. contract_reconciled.json declares this exact
change and otherwise unchanged31-check assertion. The old checks.py was executed
again into NEW run_reconciled/, with original action/source files unchanged.
Schema-v2 manifest: completed, Git {mf['repository']['commit']},
dirty={mf['repository']['dirty']}, runtime {mf['run']['runtime_seconds']:.6f}s.
The computation-audit validator returned 'valid evidence record; mathematical
interpretation requires review' against the current repository root.
Result bytes are EXACTLY IDENTICAL to the original31-check results.json;
sha256 {hashlib.sha256((h/'run_reconciled/results.json').read_bytes()).hexdigest()}.
This rerun improves current-source provenance; it does not add31 new independent
physical claims or alter the54 DISTINCT checks originally reported.

Counts and preserved freshness
-------------------------------
Original execution:31 carrier identities+15 classical work checks+8 cold-rate
checks=54. Current-source valid local interaction runs now are
run_reconciled31 + classical_run15 + cold_rate_run8 = the same54 distinct checks.
The replay adds31 executed check events, for85 total events across historical
and current local-interaction executions; that is not85 independent results.
verification_original.json preserves the prior54-check verification verbatim.
verification_reconciled.json now explicitly lists historical versus current dispositions.
The separately executed carrier_cosmology25 checks are unaffected.

RESULT.txt is deliberately unchanged because carrier_cosmology/run declares its
bytes as an execution input. Rewriting it to update the context sentence would
make that otherwise fresh run stale. This supplemental report is the current
freshness interpretation, and should be read alongside the preserved RESULT.
No files outside local_interaction/ were changed for this reconciliation.
No survey fit, physical coefficient or new interaction was introduced.
'''
(h/'RECONCILIATION_REPORT.txt').write_text(report)
verification={'checkpoint':'FRAMEWORK-CERT-TRANSPORT-2026-10-12','distinct_checks':54,'historical_original_check_count':54,'current_source_valid_runs':{'run_reconciled':31,'classical_run':15,'cold_rate_run':8},'historical_context_runs':{'run':{'checks':31,'current_source_fresh':False,'reason':'declared contextual producer RESULT changed','original_manifest_unchanged':True,'historical_source_recovered_exact_hash':True}},'total_executed_check_events_including_replay':85,'reconciled_result_bytes_identical':True,'all_current_source_runs_validated':True,'carrier_cosmology_25_check_run_unmodified':True,'original_RESULT_txt_unchanged_for_downstream_freshness':True,'framework_only_subset':'Exact classical local charge/stress and instantaneous component-work identities','conditional_quantum_subset':'Bose kinetics, projected positive-frequency Hamiltonian, vacuum width/coldness-rate relation','physical_interaction_leaf_still_missing':True,'original_verification_preserved':'verification_original.json','report_sha256':hashlib.sha256((h/'RESULT.txt').read_bytes()).hexdigest(),'reconciliation_report_sha256':hashlib.sha256(report.encode()).hexdigest()}
(h/'verification_reconciled.json').write_text(json.dumps(verification,indent=2)+'\n');print(json.dumps(verification))
