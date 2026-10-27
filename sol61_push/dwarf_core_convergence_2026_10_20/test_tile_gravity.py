"""Explicit empirical gates for a new FP32-tile/DS-merge GPU candidate."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
from fast_gravity import gravity as reference


HERE=Path(__file__).resolve().parent
path=HERE/'tile_gravity.py'
if path.exists():
    spec=importlib.util.spec_from_file_location('tile_candidate',path)
    candidate=importlib.util.module_from_spec(spec);spec.loader.exec_module(candidate)
else:candidate=None


class TileTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(candidate,'new tile candidate not implemented')

    def compare(self,x,m,eps):
        a,U,phi=candidate.gravity(x,m,eps);b,V,psi=reference(x,m,eps)
        self.assertLess(np.linalg.norm(a-b)/np.linalg.norm(b),5.e-7)
        self.assertLess(np.max(np.linalg.norm(a-b,axis=1)/np.maximum(np.linalg.norm(b,axis=1),1.e-100)),2.e-6)
        self.assertLess(np.max(abs((phi-psi)/psi)),5.e-7)
        self.assertLess(abs(U/V-1.),5.e-7)
        self.assertEqual(U,.5*float(m@phi))
        f=m[:,None]*a
        self.assertLess(np.linalg.norm(f.sum(0))/np.linalg.norm(f,axis=1).sum(),1.e-8)
        self.assertLess(np.linalg.norm(np.cross(x,f).sum(0))/np.sum(np.linalg.norm(x,axis=1)*np.linalg.norm(f,axis=1)),1.e-8)
        return a,U,phi

    def test_unequal_mass_non_tilemultiple_coincident_distinct_sources(self):
        rng=np.random.default_rng(19873);x=rng.normal(size=(513,3))*[500,100,30]
        x[1]=x[0];m=rng.uniform(.1,5,len(x))*1000.
        self.compare(x,m,5.)

    def test_close_remnant_far_first_tail_nonzero_offset_and_translation(self):
        rng=np.random.default_rng(19874)
        x=np.r_[[[-4.e5,5.e5,-2.e5]],rng.normal(size=(256,3))*[2,3,1]+[80000.12345,-30000.9876,2000.42]]
        m=rng.uniform(.1,5,len(x))*1000.
        a,U,phi=self.compare(x,m,2.)
        b,V,psi=candidate.gravity(x+[200000.,-300000.,100000.],m,2.)
        np.testing.assert_allclose(a,b,rtol=2.e-6,atol=1.e-9)
        self.assertLess(abs(V/U-1.),5.e-7)

    def test_many_source_tiles_accumulate_and_keep_vector_invariants(self):
        rng=np.random.default_rng(19875);x=rng.normal(size=(4097,3))*100.
        m=rng.uniform(.1,5,len(x))*1000.
        self.compare(x,m,5.)

    def test_actual_evolved_snapshot_and_per_particle_phi_against_CPU(self):
        state=np.load(HERE/'run_pilot_gpu8k_iso'/'final.npz')
        self.compare(state['x'],state['m'],10.)

    def test_raw3f_encoding_and_declared_separate_precision_budget(self):
        metadata=candidate.backend_metadata()
        self.assertEqual(metadata['abi_version'],4)
        self.assertIn('FP32',metadata['precision'])
        self.assertEqual(metadata['tile_threads'],128)
        self.assertEqual(metadata['DS_merge_frequency'],'once per source tile')
        x=np.array([[80000.123456789,-30000.987654321,2000.123456789]])
        packed=candidate._pack_particles(x,np.array([3000.123456789]))
        np.testing.assert_array_equal(packed[:,[0,2,4]].astype(float)+packed[:,[1,3,5]].astype(float)+packed[:,8:11].astype(float),x)


if __name__=='__main__':unittest.main()
