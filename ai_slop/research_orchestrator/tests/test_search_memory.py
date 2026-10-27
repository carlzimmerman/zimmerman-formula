"""Regression coverage for repetition and loss of referee feedback in long runs."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import engine, orchestrator, prompts, frontier
from test_repairs import answer, contract

class SearchMemoryTests(unittest.TestCase):
    def test_cluster_catalogue_exposes_actual_fits_columns_and_units(self):
        from astropy.io import fits
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); app=root/'ai_slop/research_orchestrator'; app.mkdir(parents=True)
            data=root/'real_research/data/xcop/A1'; data.mkdir(parents=True)
            fits.BinTableHDU.from_columns([
                fits.Column(name='RADIUS',format='D',unit='kpc',array=[1.0]),
                fits.Column(name='MASS',format='D',unit='solMass',array=[2.0])
            ]).writeto(data/'profile.fits')
            with patch.dict(frontier.CONFIG,{'root':app.resolve()}): catalog=frontier.digest('cluster-source-closure')
            self.assertEqual(catalog['available_inputs'][0].get('columns'),[
                {'name':'RADIUS','unit':'kpc'}, {'name':'MASS','unit':'solMass'}])

    def test_referee_feedback_survives_restart_and_six_record_window(self):
        with tempfile.TemporaryDirectory() as td:
            with engine.Store(td) as store:
                parent=store.record(contract(),'constructive',answer(),{'validity':'proposal'})
                review=store.record(contract(),'door-referee',
                    {'decision':'reject','reason':'predicate changed in negative mode','next_test':'derive a new predicate'},
                    {'validity':'proposal'},request={'parent':parent['id']})
                for _ in range(9): store.record(contract(),'repair',answer(),{'validity':'invalid','reason':'fixture'})
                other={**contract(),'id':'unrelated'}
                store.record(other,'door-referee',{'decision':'reject','reason':'UNRELATED'}, {'validity':'proposal'})
            with engine.Store(td) as store:
                memory=store.search_memory(contract())
                self.assertIn(review['id'],[r['id'] for r in memory['rejected_routes']])
                self.assertNotIn('UNRELATED',json.dumps(memory))
                self.assertEqual(memory['primary_attempts'],1)

    def test_exact_script_repeat_is_redirected_but_explicit_replay_still_runs(self):
        with tempfile.TemporaryDirectory() as td,engine.Store(td) as store:
            first=orchestrator.process_response(store,contract(),'constructive',answer(),{})
            changed=answer(); changed['code']='# A cosmetic change\n'+changed['code']
            second=orchestrator.process_response(store,contract(),'constructive',changed,{})
            self.assertEqual(second['result'].get('duplicate_of'),first['id'])
            self.assertFalse(second['result'].get('runs'))
            replay=orchestrator.replay_attempt(store,first['id'])
            self.assertEqual(replay['result']['validity'],'candidate_checked')

    def test_materially_changed_code_runs_under_same_hypothesis(self):
        with tempfile.TemporaryDirectory() as td,engine.Store(td) as store:
            first=orchestrator.process_response(store,contract(),'constructive',answer(),{})
            changed=answer(); changed['code']=changed['code'].replace("'main':3","'main':4")
            second=orchestrator.process_response(store,contract(),'constructive',changed,{})
            self.assertEqual(second['result']['validity'],'candidate_checked')
            self.assertTrue(second['result']['runs'])

    def test_narrower_hypothesis_can_reuse_same_calculation(self):
        with tempfile.TemporaryDirectory() as td,engine.Store(td) as store:
            first=orchestrator.process_response(store,contract(),'constructive',answer(),{})
            narrow=answer(); narrow['hypothesis']='The specified fixture fails the square-equals-four test'
            second=orchestrator.process_response(store,contract(),'constructive',narrow,{})
            self.assertEqual(second['result']['validity'],'candidate_checked')
            self.assertTrue(second['result']['runs'])

    def test_changed_input_bytes_are_not_a_duplicate(self):
        with tempfile.TemporaryDirectory() as td,engine.Store(Path(td)/'ledger') as store:
            p=Path(td)/'input.csv'; p.write_text('x\n1\n')
            c=contract(); a=answer()
            first={'inputs':[{'name':'sample','sha256':engine.sha(p.read_bytes())}],
                   'required_checks':['target'],'negative_checks':['target']}
            old=store.record(c,'constructive',a,{'validity':'candidate_checked','outcome':'rejected',
                                              'execution_contract':first,'runs':{'main':{}}})
            self.assertEqual(store.duplicate_experiment(c,a,first),old['id'])
            p.write_text('x\n2\n')
            fresh={**first,'inputs':[{'name':'sample','sha256':engine.sha(p.read_bytes())}]}
            self.assertIsNone(store.duplicate_experiment(c,a,fresh))

    def test_duplicate_lookup_detects_modified_manifest(self):
        with tempfile.TemporaryDirectory() as td,engine.Store(td) as store:
            first=orchestrator.process_response(store,contract(),'constructive',answer(),{})
            p=Path(first['path']); content=json.loads(p.read_text()); content['response']['code']='print(0)'
            p.write_text(json.dumps(content))
            with self.assertRaises(ValueError):
                store.duplicate_experiment(contract(),answer(),{'inputs':[],
                    'required_checks':['target'],'negative_checks':['target']})

    def test_route_rotation_is_persistent_and_not_advanced_by_repairs(self):
        c=contract(); routes={c['id']:[{'id':'ward','question':'Vary the action'},
                                      {'id':'spectral','question':'Derive the measure'}]}
        with tempfile.TemporaryDirectory() as td:
            with engine.Store(td) as store:
                with patch.dict(orchestrator.CONFIG,{'research_routes':routes}),patch.object(orchestrator.llm,'generate',return_value=(json.dumps(answer()),{})):
                    first=orchestrator.one_iteration(store,[c])
                self.assertEqual(store.load(first['id'])['request']['search']['route']['id'],'ward')
                store.record(c,'repair',{}, {'validity':'invalid'})
            with engine.Store(td) as store:
                changed=answer(); changed['code']=changed['code'].replace("'main':3","'main':4")
                with patch.dict(orchestrator.CONFIG,{'research_routes':routes}),patch.object(orchestrator.llm,'generate',return_value=(json.dumps(changed),{})):
                    second=orchestrator.one_iteration(store,[c])
                self.assertEqual(store.load(second['id'])['request']['search']['route']['id'],'spectral')

if __name__=='__main__': unittest.main()
