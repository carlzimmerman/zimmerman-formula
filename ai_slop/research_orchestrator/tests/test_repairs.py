"""Regressions for the first live Qwen run: invalid frozen metadata and repeated JSON."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import engine
import executor
import llm
import orchestrator


def contract():
    return {'id':'repair-fixture','kind':'research','question':'Test this fixed claim',
            'model_version':'fixture','assumptions':['fixture only'],'context':[],'depends_on':[]}


def answer():
    return {'hypothesis':'The measured square equals four','assumptions':['fixture only'],
            'argument':'Evaluate a fixed numerical predicate','next_test':'none',
            'required_checks':['target'],'negative_checks':['target'],'inputs':[],
            'code':'''import json,os
x = {'main':3,'positive':2,'negative':5}[os.environ['ORCH_MODE']]
print(json.dumps({'protocol':2,'complete':True,'checks':{'target':x*x==4}}))
'''}


class RepairRegressionTests(unittest.TestCase):
    def test_invalid_negative_names_can_be_corrected_without_changing_claim(self):
        bad=answer(); bad['negative_checks']=['perturbed_not_equal']
        with tempfile.TemporaryDirectory() as td,engine.Store(td) as store:
            replies=[bad,answer(),answer()]
            with patch.object(llm,'generate',side_effect=[(json.dumps(x),{}) for x in replies]):
                final=orchestrator.one_iteration(store,[contract()])
            self.assertEqual(final['result']['validity'],'candidate_checked')
            self.assertEqual(final['result']['outcome'],'rejected')
            self.assertEqual(store.summary()['attempts'],2)

    def test_protocol_repair_cannot_replace_the_scientific_claim(self):
        bad=answer(); bad['negative_checks']=['perturbed_not_equal']
        changed=answer(); changed['hypothesis']='A different claim'
        with tempfile.TemporaryDirectory() as td,engine.Store(td) as store:
            with patch.object(llm,'generate',side_effect=[(json.dumps(x),{}) for x in [bad,changed,changed]]):
                final=orchestrator.one_iteration(store,[contract()])
            self.assertEqual(final['result']['validity'],'invalid')
            self.assertIn('changed',final['result']['reason'].lower())

    def test_valid_check_spec_stays_frozen_after_runtime_failure(self):
        bad=answer(); bad['code']='raise RuntimeError("fixture")'
        changed=answer(); changed['required_checks']=['easier']; changed['negative_checks']=['easier']
        changed['code']=changed['code'].replace("'target'","'easier'")
        with tempfile.TemporaryDirectory() as td,engine.Store(td) as store:
            with patch.object(llm,'generate',side_effect=[(json.dumps(x),{}) for x in [bad,changed,changed]]):
                final=orchestrator.one_iteration(store,[contract()])
            self.assertEqual(final['result']['validity'],'invalid')
            self.assertIn('changed',final['result']['reason'].lower())

    def test_repairs_do_not_accumulate_old_answers(self):
        prompts=[]; replies=[]
        for marker in ['FIRST_FAILURE_MARKER','LATEST_FAILURE_MARKER','FINAL_FAILURE_MARKER']:
            a=answer(); a['code']='raise RuntimeError('+repr(marker)+')'; replies.append(json.dumps(a))
        def model(role,prompt,store):
            prompts.append(prompt)
            return replies[len(prompts)-1],{}
        with tempfile.TemporaryDirectory() as td,engine.Store(td) as store:
            with patch.object(llm,'generate',side_effect=model):
                orchestrator.one_iteration(store,[contract()])
        self.assertIn('LATEST_FAILURE_MARKER',prompts[2])
        self.assertNotIn('FIRST_FAILURE_MARKER',prompts[2])

    def test_local_request_enables_json_mode_and_records_truncation(self):
        class Reply:
            def raise_for_status(self): pass
            def json(self): return {'response':'{"proof":"rfl"}', 'done':True,
                                    'done_reason':'length','eval_count':4096}
        sent=[]
        def post(url,**kwargs):
            sent.append(kwargs['json']); return Reply()
        with tempfile.TemporaryDirectory() as td,engine.Store(td) as store:
            with patch.object(llm.requests,'post',side_effect=post):
                raw,metadata=llm.generate('constructive','Return JSON',store)
        self.assertEqual(sent[0].get('format'),'json')
        self.assertEqual(metadata.get('done_reason'),'length')

    def test_control_failure_names_exact_mismatched_checks(self):
        with tempfile.TemporaryDirectory() as td,engine.Store(Path(td)/'ledger') as store:
            a=answer(); a['code']=a['code'].replace("'positive':2","'positive':3")
            result=orchestrator.process_response(store,contract(),'constructive',a,{})['result']
        self.assertEqual(result['validity'],'invalid')
        self.assertEqual(result.get('control_failures'),{'positive_expected_true':['target'],
                                                       'negative_expected_false':[]})

if __name__=='__main__': unittest.main()
