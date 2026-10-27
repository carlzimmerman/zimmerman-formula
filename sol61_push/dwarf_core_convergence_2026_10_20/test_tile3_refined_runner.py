"""Versioned tile3 runner must preserve the frozen fixed-state evolution."""
import contextlib
import hashlib
import importlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from evolution import initial_conditions,h4_step
from fast_gravity import gravity

try:
    runner=importlib.import_module('run_tile3_refined')
    launcher=importlib.import_module('launch_tile3_refined')
except ModuleNotFoundError:
    runner=launcher=None

HERE=Path(__file__).resolve().parent


def fixed_state(folder):
    x,v,m,cold,ic=initial_conditions(512,64,87319,10.,gravity)
    ic['relative_state_sha256']=hashlib.sha256(x.tobytes()+v.tobytes()+m.tobytes()).hexdigest()
    path=folder/'initial.npz'
    np.savez(path,x=x,v=v,m=m,cold=cold)
    (folder/'initial_metadata.json').write_text(json.dumps(dict(initial_conditions=ic)))
    return path,x,v,m,cold


class Tile3RunnerTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(runner,'new tile3 wrapper is missing')

    def test_tile3_selects_separate_budget_and_freezes_new_sources(self):
        # Accidentally routing to tile2 or freezing the old wrapper defeats isolation.
        with tempfile.TemporaryDirectory(dir=HERE) as directory:
            path,*_=fixed_state(Path(directory))
            spec=launcher.prepare_launch('tile3_tiny_review',
                ['--initial',str(path),'--ncold','512','--backend','tile3'],timeout=60)
            for filename in ['run_tile3_refined.py','launch_tile3_refined.py',
                             'tile3_gravity.py','tile3_gravity.mm','TILE3_NUMERICAL_BUDGET.md']:
                self.assertIn(str((HERE/filename).relative_to(launcher.ROOT)),spec['inputs'])
            self.assertIn('TILE3_GRAVITY_LIBRARY',spec['selected_libraries'])
            self.assertEqual(spec['command'][spec['command'].index('--initial')+1],str(path.resolve()))
            self.assertIn(str(launcher.REL/'run_tile3_refined.py'),spec['command'])
            reference=(np.ones((2,3)),-1.,-np.ones(2))
            answer=(reference[0]+1e-7,reference[1],reference[2])
            metrics=runner.precision_metrics(answer,reference)
            self.assertTrue(runner.precision_pass(metrics,'tile3'))
            self.assertFalse(runner.precision_pass(metrics,'metal'))
            self.assertFalse(runner.precision_pass({'force_relative_L2':0.},'tile3'))

    def test_cpu_common_state_map_matches_frozen_h4_without_source_changes(self):
        # A copy error or new IC normalization changes the actual saved phase space.
        frozen={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                for name in ('run_refined.py','launch_refined.py','refined_core.py')}
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);path,x,v,m,cold=fixed_state(root);output=root/'result'
            args=runner.parser().parse_args(['--initial',str(path),'--output',str(output),
                '--ncold','512','--backend','cpu','--threads','1','--eps','20.',
                '--dt','.25','--duration','.25','--record-interval','.25','--collisionless'])
            with contextlib.redirect_stdout(io.StringIO()):runner.main(args)
            with np.load(output/'initial.npz') as actual:
                for key,value in [('x',x),('v',v),('m',m),('cold',cold)]:
                    np.testing.assert_array_equal(actual[key],value)
            xx,vv=x.copy(),v.copy()
            def force(xx):
                a,U,phi=gravity(xx,m,20.,threads=1)
                return a,U,phi,np.zeros_like(xx),np.zeros(len(m))
            h4_step(xx,vv,.25,force)
            with np.load(output/'final.npz') as actual:
                np.testing.assert_array_equal(actual['x'],xx)
                np.testing.assert_array_equal(actual['v'],vv)
        for name,digest in frozen.items():
            self.assertEqual(hashlib.sha256((HERE/name).read_bytes()).hexdigest(),digest)


if __name__=='__main__':unittest.main()
