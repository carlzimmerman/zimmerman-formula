"""Bounded launcher regressions; slow nonlinear solver is mocked at its boundary."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

PATH = Path(__file__).with_name('parallel_sweep.py')
spec = importlib.util.spec_from_file_location('parallel_sweep', PATH)
sweep = importlib.util.module_from_spec(spec) if PATH.exists() else None
if sweep is not None:
    spec.loader.exec_module(sweep)


class SweepTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(sweep, 'parallel launcher has not been implemented')

    def test_determinism_interleaving_and_control(self):
        jobs = [sweep.make_job(i, 11) for i in range(4)]
        self.assertEqual([j['mode'] for j in jobs], ['geometry', 'clock'] * 2)
        self.assertEqual(jobs[0]['start'], [306704.1420152562, .1800733844324149, 3057.7826875767923, .1])
        self.assertEqual(jobs[2], sweep.make_job(2, 11))
        self.assertNotEqual(jobs[2]['start'], sweep.make_job(2, 12)['start'])
        self.assertEqual(jobs[2], [sweep.make_job(i, 11) for i in (3, 2)][1])

    def test_checkpoint_resume_rejects_mismatch_and_duplicate(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'run.jsonl'
            header = {'type': 'header', 'config': {'starts': 4}, 'sources': {'x': 'abc'}}
            with sweep.Checkpoint(path, header, False) as ck:
                ck.append({'type': 'result', 'index': 0})
                with self.assertRaises(ValueError):
                    ck.append({'type': 'result', 'index': 0})
                with self.assertRaises(RuntimeError):
                    with sweep.Checkpoint(path, header, True):
                        pass
            with sweep.Checkpoint(path, header, True) as ck:
                self.assertEqual(set(ck.results), {0})
            with self.assertRaises(ValueError):
                with sweep.Checkpoint(path, dict(header, sources={'x': 'changed'}), True):
                    pass
            with self.assertRaises(ValueError):
                with sweep.Checkpoint(path, dict(header, config={'starts': 5}), True):
                    pass
            with self.assertRaises(FileExistsError):
                with sweep.Checkpoint(path, header, False):
                    pass

    def test_rejects_partial_checkpoint_instead_of_silently_skipping(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'run.jsonl'
            path.write_text('{"type":"header"}\n{"type":', encoding='utf-8')
            with self.assertRaises(ValueError):
                with sweep.Checkpoint(path, {'type': 'header'}, True):
                    pass

    def test_optimizer_flag_does_not_queue_nonmatch(self):
        row = {'accepted_numerical_joint': False, 'optimizer_status': 1}
        with patch.object(sweep, 'call_solver', return_value=row), patch.object(sweep, 'screen_candidate') as screen:
            result = sweep.run_job(sweep.make_job(1, 2), 1, sweep.source_hashes())
        self.assertTrue(result['optimizer_success'])
        self.assertFalse(result['accepted_numerical_joint'])
        self.assertFalse(result['verification_queued'])
        screen.assert_not_called()

    def test_health_reject_and_queue_are_distinct(self):
        row = dict(sweep.CONTROL, accepted_numerical_joint=True, optimizer_status=0)
        for flag in (False, True):
            with patch.object(sweep, 'call_solver', return_value=row), patch.object(sweep, 'screen_candidate', return_value={'needs_high_precision': flag}):
                result = sweep.run_job(sweep.make_job(0, 2), 1, sweep.source_hashes())
            self.assertTrue(result['accepted_numerical_joint'])
            self.assertFalse(result['optimizer_success'])
            self.assertEqual(result['verification_queued'], flag)
            self.assertEqual(result['health_rejected'], not flag)
            self.assertEqual(result['candidate']['parameters'], sweep.CONTROL['parameters'])

    def test_chart_and_health_screen_failures_recorded(self):
        with patch.object(sweep, 'call_solver', side_effect=ValueError('invalid coordinate chart')):
            result = sweep.run_job(sweep.make_job(2, 2), 1, sweep.source_hashes())
        self.assertEqual(result['failure_stage'], 'solve')
        self.assertIn('invalid coordinate chart', result['error'])
        row = dict(sweep.CONTROL, accepted_numerical_joint=True, optimizer_status=1)
        with patch.object(sweep, 'call_solver', return_value=row), patch.object(sweep, 'screen_candidate', side_effect=ArithmeticError('bad screen')):
            result = sweep.run_job(sweep.make_job(0, 2), 1, sweep.source_hashes())
        self.assertTrue(result['accepted_numerical_joint'])
        self.assertFalse(result['verification_queued'])
        self.assertEqual(result['failure_stage'], 'health_screen')

    def test_source_change_is_not_a_solver_success(self):
        with patch.object(sweep, 'call_solver') as solve:
            result = sweep.run_job(sweep.make_job(0, 2), 1, {'changed': 'hash'})
        self.assertEqual(result['failure_stage'], 'source_check')
        solve.assert_not_called()

    def test_transitive_action_dependencies_are_pinned(self):
        sources = sweep.source_hashes()
        for path in ('kgb_shared_pressure_2026/shared_pressure.py',
                     'ticking_kgb_inverse_2026/kgb_inverse.py'):
            self.assertIn(path, sources)


if __name__ == '__main__':
    unittest.main()
