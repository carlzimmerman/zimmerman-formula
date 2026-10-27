"""Fixed-state, precision-admission and bounded-launcher regressions."""
import contextlib
import hashlib
import importlib
import io
import json
from pathlib import Path
import tempfile
import unittest
import os
import subprocess
import sys

import numpy as np

from evolution import initial_conditions, h4_step
from fast_gravity import gravity

try:
    runner = importlib.import_module('run_refined')
    launcher = importlib.import_module('launch_refined')
except ModuleNotFoundError:
    runner = launcher = None

HERE = Path(__file__).resolve().parent
FROZEN_DRIVER_SHA256 = 'e13233e8b73db3c401cbf000ab8f7bb708edc4ba38120a38ada8594b685bec30'


def common_state(folder):
    x, v, m, cold, ic = initial_conditions(512, 64, 87319, 10., gravity)
    ic['relative_state_sha256'] = hashlib.sha256(x.tobytes()+v.tobytes()+m.tobytes()).hexdigest()
    path = folder / 'initial.npz'
    np.savez(path, x=x, v=v, m=m, cold=cold)
    (folder / 'initial_metadata.json').write_text(json.dumps(dict(initial_conditions=ic)))
    return path, x, v, m, cold


class RefinedRunnerTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(runner, 'versioned refined runner is missing')

    def test_common512_softening_control_preserves_velocities_and_h4_map(self):
        # Regenerating/renormalizing the IC at eps20 changes saved v and this map.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path, x, v, m, cold = common_state(root)
            for eps in (10., 20.):
                output = root / ('eps' + str(int(eps)))
                # The audit runner reserves the fresh output and writes manifest first.
                output.mkdir()
                (output/'manifest.json').write_text('{"run":{"status":"running"}}')
                args = runner.parser().parse_args(['--initial', str(path), '--output', str(output),
                    '--ncold', '512', '--backend', 'cpu', '--threads', '1', '--eps', str(eps),
                    '--dt', '.25', '--duration', '.25', '--record-interval', '.25', '--collisionless'])
                with contextlib.redirect_stdout(io.StringIO()):
                    runner.main(args)
                with np.load(output / 'initial.npz') as actual:
                    for key, expected in [('x', x), ('v', v), ('m', m), ('cold', cold)]:
                        np.testing.assert_array_equal(actual[key], expected)
                xx, vv = x.copy(), v.copy()
                def force(xx):
                    aa, U, phi = gravity(xx, m, eps, threads=1)
                    return aa, U, phi, np.zeros_like(xx), np.zeros(len(m))
                h4_step(xx, vv, .25, force)
                with np.load(output / 'final.npz') as final:
                    np.testing.assert_array_equal(final['x'], xx)
                    np.testing.assert_array_equal(final['v'], vv)
                result = json.loads((output / 'results.json').read_text())
                self.assertTrue(result['initial_conditions']['common_initial_state'])
                self.assertEqual(result['collision_method'], 'ctmc')
                self.assertEqual(result['collisions'], 0)
                self.assertEqual(set(result['fixed_membership_groups']), {'final_core', 'other_cold', 'stars'})
                self.assertIn('internal_work', result['maxima'])
            self.assertEqual(hashlib.sha256((HERE/'run_resolution.py').read_bytes()).hexdigest(), FROZEN_DRIVER_SHA256)

    def test_candidate_admission_uses_separate_budget_and_records_absolute_scale(self):
        # Reusing the DS1e-11 gate would reject the intentionally small FP32 error.
        ref = (np.array([[1., 0., 0.], [0., 2., 0.]]), -3., np.array([-1., -2.]))
        answer = (ref[0] + 1.e-7, -3.0000003, ref[2] * 1.0000001)
        metrics = runner.precision_metrics(answer, ref)
        self.assertGreater(metrics['force_relative_L2'], 1.e-11)
        self.assertTrue(runner.precision_pass(metrics, 'mixed'))
        self.assertFalse(runner.precision_pass(metrics, 'metal'))
        self.assertGreater(metrics['force_max_absolute_normalized'], 0.)
        bad = (ref[0] + .0001, ref[1], ref[2])
        self.assertFalse(runner.precision_pass(runner.precision_metrics(bad, ref), 'tile'))

    def test_force_cancellation_is_visible_without_hiding_global_error(self):
        # Replacing per-particle max by only L2 would hide the force-zero error.
        ref = (np.array([[0., 0., 0.], [1., 0., 0.]]), -1., -np.ones(2))
        answer = (np.array([[1.e-9, 0., 0.], [1., 0., 0.]]), -1., -np.ones(2))
        metrics = runner.precision_metrics(answer, ref)
        self.assertAlmostEqual(metrics['force_max_absolute_normalized'], 1.e-9)
        self.assertGreater(metrics['force_relative_max'], 2.e-6)
        self.assertFalse(runner.precision_pass(metrics, 'mixed'))

    def test_missing_precision_observations_cannot_pass_candidate_gate(self):
        # Checking only metrics that happen to exist would silently omit phi/U.
        self.assertFalse(runner.precision_pass({'force_relative_L2': 0.}, 'mixed'))

    def test_tile2_has_its_own_backend_and_frozen_library_closure(self):
        # Routing tile2 to v1, or omitting its sources, invalidates candidate evidence.
        with tempfile.TemporaryDirectory(dir=HERE) as directory:
            path, *_ = common_state(Path(directory))
            args = ['--initial', str(path), '--ncold', '512', '--backend', 'tile2']
            spec = launcher.prepare_launch('tiny_tile2_test', args, timeout=60)
            self.assertIn(str((HERE/'tile2_gravity.mm').relative_to(launcher.ROOT)), spec['inputs'])
            self.assertIn(str((HERE/'tile2_gravity.py').relative_to(launcher.ROOT)), spec['inputs'])
            self.assertIn('TILE2_GRAVITY_LIBRARY', spec['selected_libraries'])
            ref = (np.ones((2,3)), -1., -np.ones(2))
            candidate = (ref[0]+1.e-7, ref[1], ref[2])
            self.assertTrue(runner.precision_pass(runner.precision_metrics(candidate,ref),'tile2'))

    def test_relative_initial_is_absolute_in_worker_argv(self):
        # Worker cwd is ROOT, unlike this launcher invocation from HERE.
        with tempfile.TemporaryDirectory(dir=HERE) as directory:
            path, *_ = common_state(Path(directory))
            relative = str(path.relative_to(Path.cwd()))
            spec = launcher.prepare_launch('relative_initial_test',
                ['--initial', relative, '--ncold', '512', '--backend', 'cpu'], timeout=60)
            argv = spec['command']
            self.assertEqual(argv[argv.index('--initial')+1], str(path.resolve()))

    def test_blas_limits_are_set_before_the_first_numpy_import(self):
        # Setting the env in refined_core after NumPy loads can initialize excess threads.
        code = '''import sys,os,importlib.abc
class ObserveNumpy(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='numpy':
            assert all(os.environ.get(k)=='1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS')), 'BLAS limits were late'
        return None
sys.meta_path.insert(0,ObserveNumpy())
import run_refined
'''
        environment = dict(os.environ,OMP_NUM_THREADS='7',OPENBLAS_NUM_THREADS='7',VECLIB_MAXIMUM_THREADS='7')
        process = subprocess.run([sys.executable,'-c',code],cwd=HERE,env=environment,capture_output=True,text=True)
        self.assertEqual(process.returncode,0,process.stderr)

    def test_launcher_input_closure_and_fresh_case_validation(self):
        # Omitting common bytes/metadata or the selected backend breaks provenance.
        with tempfile.TemporaryDirectory(dir=HERE) as directory:
            path, *_ = common_state(Path(directory))
            args = ['--initial', str(path), '--ncold', '512', '--backend', 'tile']
            spec = launcher.prepare_launch('tiny_refined_test', args, timeout=60)
            inputs = spec['inputs']
            for target in [path, path.with_name('initial_metadata.json'), HERE/'tile_gravity.mm',
                           HERE/'tile_gravity.py', HERE/'metal_gravity.mm', HERE/'refined_core.py']:
                self.assertIn(str(target.relative_to(launcher.ROOT)), inputs)
            self.assertIn('candidate', spec['contract']['mathematics']['coefficient_domain'].lower())
            self.assertIn('5e-7', spec['contract']['mathematics']['coefficient_domain'])
            self.assertEqual(spec['contract']['mathematics']['bounds']['ncold'], 512)
            self.assertEqual(spec['contract']['mathematics']['bounds']['loaded_total_particles'], 576)
            with self.assertRaises(ValueError):
                launcher.prepare_launch('../bad', args, timeout=60)


if __name__ == '__main__':
    unittest.main()
