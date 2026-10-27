import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import engine
import executor
import lean_cert
import orchestrator


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def research(key='normalization'):
    return {'id': key, 'kind': 'research', 'question': 'Does an independent selector fix lambda?',
            'model_version': 'action-v1', 'assumptions': ['s independently fixed'],
            'depends_on': [], 'context': []}


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.store = engine.Store(self.root)

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def test_reused_slot_cannot_overwrite_historical_evidence(self):
        a = self.store.record(research(), 'constructive', {'text': 'first'}, {'validity': 'proposal'})
        b = self.store.record(research(), 'constructive', {'text': 'second'}, {'validity': 'proposal'})
        self.assertNotEqual(a['id'], b['id'])
        self.assertEqual(self.store.load(a['id'])['response']['text'], 'first')

    def test_changed_artifact_is_not_accepted_as_original_evidence(self):
        a = self.store.record(research(), 'constructive', {}, {'validity': 'proposal'})
        Path(a['path']).write_text('{}')
        with self.assertRaises(ValueError): self.store.load(a['id'])

    def test_generated_symlink_cannot_exfiltrate_a_host_file_into_archive(self):
        secret = self.root/'outside.txt'; secret.write_text('must not be copied')
        scratch = self.root/'scratch'; scratch.mkdir()
        (scratch/'link').symlink_to(secret)
        with self.assertRaises(ValueError):
            self.store.record(research(), 'constructive', {}, {'validity':'proposal'}, work=scratch)

    def test_proposal_cannot_be_promoted_by_a_review_label(self):
        a = self.store.record(research(), 'referee', {}, {'validity': 'proposal'})
        with self.assertRaises(ValueError):
            self.store.review(a['id'], 'accept', 'independent reviewer', 'Looks convincing')

    def test_role_rotation_survives_restart_and_does_not_rank_legacy_scores(self):
        c, role = self.store.next_job([research()])
        self.assertEqual(role, 'constructive')
        self.store.record(c, role, {}, {'validity': 'proposal'})
        self.store.close()
        self.store = engine.Store(self.root)
        self.assertEqual(self.store.next_job([research()])[1], 'counterexample')

    def test_dependency_is_not_satisfied_by_a_proposal(self):
        dep = research('dependent'); dep['depends_on'] = ['normalization']
        self.store.record(research(), 'constructive', {}, {'validity': 'proposal'})
        with self.assertRaises(ValueError): self.store.next_job([dep])


class EvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.evaluator = self.root/'evaluator.py'
        self.evaluator.write_text('''import json, os, sys
mode = os.environ['ORCH_MODE']
checks = {'target': mode != 'negative', 'diagnostic': True}
print(json.dumps({'protocol': 2, 'complete': True, 'checks': checks}))
''')
        self.contract = {**research(), 'kind': 'evaluator', 'reviewed_by': 'fixture reviewer',
            'review_note': 'Reviewed exact target and controls', 'required_checks': ['target'],
            'evaluator': {'path': str(self.evaluator), 'sha256': digest(self.evaluator)},
            'inputs': [], 'negative_checks': ['target'], 'timeout_s': 3}

    def tearDown(self): self.tmp.cleanup()

    def run_contract(self):
        self.contract['evaluator']['sha256'] = digest(self.evaluator)
        return executor.evaluate(self.contract, self.root/'runs')

    def test_complete_positive_and_negative_controls_validate_main(self):
        r = self.run_contract()
        self.assertEqual((r['validity'], r['outcome']), ('checked', 'supported'))

    def test_control_crash_is_inconclusive_even_after_pass_output(self):
        with self.evaluator.open('a') as f:
            f.write("\nif mode == 'negative': sys.exit(7)\n")
        r = self.run_contract()
        self.assertEqual((r['validity'], r['outcome']), ('invalid', 'inconclusive'))

    def test_diagnostic_cannot_mask_failed_target(self):
        self.evaluator.write_text(self.evaluator.read_text().replace("mode != 'negative'", "mode == 'positive'"))
        r = self.run_contract()
        self.assertEqual((r['validity'], r['outcome']), ('checked', 'rejected'))

    def test_missing_target_cannot_pass(self):
        self.evaluator.write_text(self.evaluator.read_text().replace("'target':", "'other':"))
        self.assertEqual(self.run_contract()['validity'], 'invalid')

    def test_non_boolean_check_cannot_pass(self):
        self.evaluator.write_text(self.evaluator.read_text().replace("mode != 'negative'", "'True'"))
        self.assertEqual(self.run_contract()['validity'], 'invalid')

    def test_changed_evaluator_is_rejected_before_execution(self):
        self.evaluator.write_text('raise RuntimeError("changed")')
        with self.assertRaises(ValueError): executor.evaluate(self.contract, self.root/'runs')

    def test_inputs_are_pinned_and_copied(self):
        data = self.root/'data.csv'; data.write_text('x\n1\n')
        self.contract['inputs'] = [{'name': 'sample', 'path': str(data), 'sha256': digest(data)}]
        self.assertEqual(self.run_contract()['validity'], 'checked')
        data.write_text('x\n2\n')
        with self.assertRaises(ValueError): executor.evaluate(self.contract, self.root/'runs')

    def test_archived_replay_works_after_original_script_is_deleted(self):
        with engine.Store(self.root/'ledger') as store:
            a=orchestrator.process_response(store,self.contract,'verification',{}, {})
            self.evaluator.unlink()
            b=orchestrator.replay_attempt(store,a['id'])
            self.assertEqual(b['result']['validity'],'checked')
            self.assertEqual(store.load(a['id'])['contract_hash'],store.load(b['id'])['contract_hash'])
            self.assertEqual(orchestrator.replay_attempt(store,b['id'])['result']['validity'],'checked')


class LeanTests(unittest.TestCase):
    def test_modified_compiled_definition_invalidates_environment_digest(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); compiler=root/'bin/lean'; compiler.parent.mkdir(); compiler.write_text('compiler')
            cache=root/'project/.lake/build/lib'; cache.mkdir(parents=True)
            module=cache/'A.olean'; module.write_text('first definition')
            a=lean_cert.compiled_environment(root/'project',compiler)['digest']
            module.write_text('other definition')
            b=lean_cert.compiled_environment(root/'project',compiler)['digest']
            self.assertNotEqual(a,b)
    def test_missing_target_is_rejected(self):
        with self.assertRaises(ValueError): lean_cert.render({}, 'rfl')

    def test_added_axiom_and_arbitrary_declarations_are_rejected(self):
        c = {'statement': '(1 : Nat) = 1', 'preamble': 'import Mathlib'}
        for proof in ['axiom cheated : False', 'def unrelated : Nat := 7', 'sorry',
                      'run_tac IO.println "hi"', 'exact (by admit)', '#eval 7']:
            with self.subTest(proof=proof):
                with self.assertRaises(ValueError): lean_cert.render(c, proof)

    def test_axiom_audit_rejects_new_axiom_and_missing_audit(self):
        self.assertFalse(lean_cert.allowed_axioms("'OrchTarget' depends on axioms: [cheated]"))
        self.assertFalse(lean_cert.allowed_axioms(''))
        self.assertTrue(lean_cert.allowed_axioms("'OrchTarget' depends on axioms: [propext, Classical.choice, Quot.sound]"))


class WorkflowTests(unittest.TestCase):
    def test_oversized_door_evidence_is_inconclusive_not_a_loop_crash(self):
        with tempfile.TemporaryDirectory() as td,engine.Store(td) as store:
            parent=store.record(research(),'constructive',{'argument':'x'*46000},
                                {'validity':'candidate_checked','outcome':'supported'})
            report=orchestrator.chase_doors(store,research(),parent,max_depth=1)
            self.assertEqual(report['status'],'inconclusive')

    def test_repair_sees_previous_program_and_actual_stderr(self):
        answer={'hypothesis':'fixed hypothesis','assumptions':['fixture'],'argument':'fixture',
                'next_test':'none','code':'raise RuntimeError("repair-fixture")',
                'required_checks':['target'],'negative_checks':['target'],'inputs':[]}
        seen=[]
        def reply(role,prompt,store):
            seen.append(prompt)
            return json.dumps(answer),{}
        with tempfile.TemporaryDirectory() as td,engine.Store(td) as store:
            with patch.object(orchestrator.llm,'generate',side_effect=reply):
                a=orchestrator.one_iteration(store,[research()])
            self.assertEqual(a['result']['validity'],'invalid')
            self.assertIn('repair-fixture',seen[1])
            self.assertIn('Traceback',seen[1])
            self.assertIn('fixed hypothesis',seen[1])

    def test_generated_code_cannot_read_or_write_outside_scratch(self):
        with tempfile.TemporaryDirectory() as td, engine.Store(Path(td)/'runtime') as store:
            secret=Path(td)/'private.txt'; secret.write_text('private fixture')
            code='''import json,os
blocked=[]
for op in ['read','write']:
 try:
  if op=='read': open(PATH).read()
  else: open(PATH,'w').write('overwritten')
  blocked.append(False)
 except PermissionError: blocked.append(True)
print(json.dumps({'protocol':2,'complete':True,'checks':{'target':all(blocked) and os.environ['ORCH_MODE']!='negative'}}))
'''.replace('PATH',repr(str(secret)))
            response={'hypothesis':'sandbox fixture','assumptions':['fixture only'],'argument':'Check isolation',
                      'next_test':'none','code':code,'required_checks':['target'],'negative_checks':['target'],'inputs':[]}
            a=orchestrator.process_response(store,research(),'constructive',response,{})
            self.assertEqual(a['result']['outcome'],'supported')
            self.assertEqual(secret.read_text(),'private fixture')

    def test_changed_door_hypothesis_cannot_advance_to_lean(self):
        answer={'hypothesis':'Different claim','assumptions':['test only'],'argument':'fixture',
                'next_test':'none','code':'print(0)','required_checks':['target'],'negative_checks':['target'],'inputs':[]}
        frozen={k:answer[k] for k in ('hypothesis','assumptions','required_checks','negative_checks')}
        frozen['hypothesis']='Exact required consequence'
        replies=[json.dumps({'decision':'advance','reason':'fixture','next_test':'frozen test','door_contract':frozen})]
        replies += [json.dumps(answer)]*3
        with tempfile.TemporaryDirectory() as td,engine.Store(td) as store:
            parent=store.record(research(),'constructive',{}, {'validity':'candidate_checked','outcome':'supported'})
            with patch.object(orchestrator.llm,'generate',side_effect=[(x,{}) for x in replies]):
                r=orchestrator.chase_doors(store,research(),parent,max_depth=1)
            self.assertEqual(r['survived_doors'],0)
            self.assertNotIn('lean',r)

    def test_malformed_input_is_recorded_without_killing_loop(self):
        response={'hypothesis':'A','assumptions':[],'argument':'B','next_test':'C',
                  'inputs':[{'name':'missing path'}]}
        with tempfile.TemporaryDirectory() as td, engine.Store(td) as store:
            with patch.object(orchestrator.llm,'generate',return_value=(json.dumps(response),{})):
                a=orchestrator.one_iteration(store,[research()])
            self.assertEqual(a['result']['validity'],'invalid')
            self.assertEqual(store.summary()['attempts'],3)
    def test_autonomous_door_runs_generated_code_and_attempts_fixed_lean_target(self):
        answer = {'hypothesis': 'Fixture arithmetic', 'assumptions': ['test only'],
                  'argument': 'Baseline and control', 'next_test': 'Independent replication',
                  'code': 'import json,os\nprint(json.dumps({"protocol":2,"complete":True,"checks":{"target":os.environ["ORCH_MODE"]!="negative"}}))',
                  'required_checks': ['target'], 'negative_checks': ['target'], 'inputs': []}
        frozen = {k:answer[k] for k in ('hypothesis','assumptions','required_checks','negative_checks')}
        replies = [json.dumps({'decision':'advance','reason':'Fixture review', 'door_contract':frozen,
                               'next_test':'Independently recompute the arithmetic'}),
                   json.dumps(answer),
                   json.dumps({'decision':'advance','reason':'Executed fixture implements frozen requirement'}),
                   json.dumps({'statement':'(1 : Nat) = 1','rationale':'Wiring fixture only'}),
                   json.dumps({'proof':'rfl'})]
        with tempfile.TemporaryDirectory() as td, engine.Store(td) as store:
            parent = orchestrator.process_response(store, research(), 'constructive', answer, {})
            with patch.object(orchestrator.llm, 'generate', side_effect=[(x, {'model':'test-fixture'}) for x in replies]):
                report = orchestrator.chase_doors(store, research(), parent, max_depth=1)
            self.assertEqual(report['survived_doors'], 1)
            self.assertEqual(report['lean']['result']['validity'], 'formal_checked')
            self.assertFalse(store.accepted(research()))

    def test_proposal_without_execution_spec_cannot_run_arbitrary_python(self):
        with tempfile.TemporaryDirectory() as td:
            marker = Path(td)/'must-not-exist'
            answer = {'hypothesis': 'Candidate selector', 'assumptions': ['s fixed'],
                      'argument': 'Needs proof', 'next_test': 'Try a counterexample',
                      'code': f"open({str(marker)!r}, 'w').write('bad')"}
            with engine.Store(td) as store:
                a = orchestrator.process_response(store, research(), 'constructive', answer, {})
                self.assertEqual(store.load(a['id'])['result']['validity'], 'proposal')
                self.assertFalse(marker.exists())

    def test_generated_experiment_runs_and_remains_a_candidate(self):
        with tempfile.TemporaryDirectory() as td:
            answer = {'hypothesis': 'Fixture arithmetic', 'assumptions': ['test only'],
                      'argument': 'Baseline and control', 'next_test': 'Independent replication',
                      'code': 'import json,os\nprint(json.dumps({"protocol":2,"complete":True,"checks":{"target":os.environ["ORCH_MODE"]!="negative"}}))',
                      'required_checks': ['target'], 'negative_checks': ['target'], 'inputs': []}
            with engine.Store(td) as store:
                a = orchestrator.process_response(store, research(), 'constructive', answer, {})
                self.assertEqual(a['result']['validity'], 'candidate_checked')
                self.assertEqual(a['result']['outcome'], 'supported')
                self.assertIn('runs', a['result'])

    def test_budget_reservations_survive_restart(self):
        with tempfile.TemporaryDirectory() as td:
            with engine.Store(td) as store:
                self.assertIsNotNone(store.reserve(0.75, 1.0))
            with engine.Store(td) as store:
                self.assertIsNone(store.reserve(0.75, 1.0))

    def test_duplicate_model_json_keys_are_rejected(self):
        with self.assertRaises(ValueError):
            orchestrator.parse_response('{"hypothesis":"A","hypothesis":"B"}')

    def test_changed_contract_invalidates_prior_acceptance(self):
        with tempfile.TemporaryDirectory() as td:
            with engine.Store(td) as store:
                c = research()
                a = store.record(c, 'constructive', {}, {'validity':'checked', 'outcome':'supported'})
                store.review(a['id'], 'accept', 'reviewer', 'Fixture result')
                self.assertTrue(store.accepted(c))
                c['assumptions'].append('new premise')
                self.assertFalse(store.accepted(c))


if __name__ == '__main__': unittest.main()
