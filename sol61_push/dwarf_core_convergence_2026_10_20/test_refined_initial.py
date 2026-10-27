"""Fixed-array controls must not be silently renormalized or mismatched."""
import hashlib,json,importlib.util,tempfile,unittest
from pathlib import Path
import numpy as np
from evolution import initial_conditions
from fast_gravity import gravity

p=Path(__file__).with_name('refined_initial.py')
if p.exists():
    spec=importlib.util.spec_from_file_location('refined_initial_test',p)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
else:module=None

class FixedInitialTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(module,'fixed-array loader missing')

    def fixture(self,d):
        x,v,m,cold,ic=initial_conditions(512,64,87319,10.,gravity)
        ic['relative_state_sha256']=hashlib.sha256(x.tobytes()+v.tobytes()+m.tobytes()).hexdigest()
        np.savez(Path(d)/'initial.npz',x=x,v=v,m=m,cold=cold)
        (Path(d)/'initial_metadata.json').write_text(json.dumps(dict(initial_conditions=ic)))
        return x,v,m,cold,ic

    def test_loaded_state_unchanged_and_independent_copies(self):
        with tempfile.TemporaryDirectory() as d:
            expected=self.fixture(d);actual=module.load_initial(Path(d)/'initial.npz',512,87319)
            for a,b in zip(expected[:4],actual[:4]):np.testing.assert_array_equal(a,b)
            actual[0][:]=0
            again=module.load_initial(Path(d)/'initial.npz',512,87319)
            np.testing.assert_array_equal(again[0],expected[0])

    def test_mismatched_seed_count_and_changed_bytes_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            x,v,m,cold,_=self.fixture(d);p=Path(d)/'initial.npz'
            with self.assertRaises(ValueError):module.load_initial(p,1024,87319)
            with self.assertRaises(ValueError):module.load_initial(p,512,87320)
            v[0,0]+=1e-9;np.savez(p,x=x,v=v,m=m,cold=cold)
            with self.assertRaises(ValueError):module.load_initial(p,512,87319)

if __name__=='__main__':unittest.main()
