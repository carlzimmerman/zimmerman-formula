"""Independent ticket coverage, generator, and conservation checks for cell CTMC."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import importlib.util
from pathlib import Path
import unittest
import numpy as np

HERE=Path(__file__).resolve().parent
path=HERE/'cell_scatter.py'
if path.exists():
    spec=importlib.util.spec_from_file_location('cell_tested',path)
    cell=importlib.util.module_from_spec(spec);spec.loader.exec_module(cell)
else:cell=None


def hazard(x,v,i,j,h,mass,sigma=.3):
    q=x[i]-x[j];r=float(np.linalg.norm(q))
    if not 0.<r<h:return 0.
    w=v[i]-v[j];z=float(w@w)/(2*.02*306601.39378555055)**2
    ratio=((2-z/(1-z))/2)**2/(1+.02**2*z)
    return 3*mass*sigma*.0002088420524663771/(np.pi*h**3)*ratio*max(-float(w@(q/r)),0.)


class CellScatterTests(unittest.TestCase):
    def setUp(self):self.assertIsNotNone(cell,'cell CTMC is not implemented')

    def test_exhaustive_tickets_cover_every_oriented_candidate_exactly_once(self):
        x=np.array([[-4.1,0,0],[-.1,0,0],[0.,0,0],[.2,0,0],[1.99,0,0],[2.01,0,0],[5.,1.,0]])
        graph=cell.CellProposal(x,1.)
        bins=np.floor(x/2).astype(np.int64)
        expected={(i,j) for i in range(len(x)) for j in range(len(x)) if np.max(abs(bins[i]-bins[j]))<=1}
        actual=[graph.pair_for_ticket(k) for k in range(graph.oriented_count)]
        self.assertEqual(len(actual),len(expected));self.assertEqual(len(set(actual)),len(actual))
        self.assertEqual(set(actual),expected)
        self.assertTrue(all(actual.count((i,i))==1 for i in range(len(x))))
        for bad in (-1,graph.oriented_count):
            with self.assertRaises(ValueError):graph.pair_for_ticket(bad)

    def test_exhaustive_generator_matches_scalar_allpairs_boundaries_and_offsets(self):
        h=1.;near=np.nextafter(1.,0.);outside=np.nextafter(1.,np.inf)
        base=np.array([[-4.,0,0],[-2.,0,0],[-1.,0,0],[0.,0,0],[near,0,0],[1.,0,0],[outside,0,0],[2.,0,0],[2.01,.2,0],[2.01,.2,0]])
        v=np.random.default_rng(78301).normal(size=base.shape)*.2
        for shift in ([0.,0,0],[80000.123,-30000.987,2000.42],[-2.e8,3.e8,-1.e8]):
            x=base+shift;graph=cell.CellProposal(x,h);q=graph.oriented_count
            ticket_hazards={}
            for ticket in range(q):
                i,j=graph.pair_for_ticket(ticket)
                if i==j:continue
                edge=tuple(sorted((i,j)))
                ticket_hazards[edge]=ticket_hazards.get(edge,0.)+.5*hazard(x,v,i,j,h,1000.)
            for i in range(len(x)):
                for j in range(i+1,len(x)):
                    self.assertAlmostEqual(ticket_hazards.get((i,j),0.),hazard(x,v,i,j,h,1000.),delta=1.e-16)
            # The comparison is exact for each represented snapshot; translation
            # can round a boundary pair across h, so its independent rate is used.
            self.assertEqual(q,sum(graph.counts*graph.adjacent_particle_counts))

    def test_large_exact_integer_tickets_are_not_float_weighted(self):
        class Fixed:
            def __init__(self,t):self.t=t
            def integers(self,high):return self.t
        graph=cell.CellProposal(np.zeros((8,3)),1.)
        for ticket in range(graph.oriented_count):
            self.assertEqual(graph.draw(Fixed(ticket)),graph.pair_for_ticket(ticket))
        self.assertEqual(graph.oriented_count,64)
        # Synthetic count-only fixture exercises tickets beyond binary64's
        # exact integer range without allocating a100million-particle array.
        n=100000003
        large=cell.CellProposal.__new__(cell.CellProposal)
        large.oriented_count=n*n;large.cumulative=np.array([n*n],np.int64)
        large.adjacent_particle_counts=np.array([n],np.int64)
        large.counts=np.array([n],np.int64);large.starts=np.array([0],np.int64)
        large.neighbors=np.array([[0]+[-1]*26],np.int32)
        class Identity:
            def __getitem__(self,k):return int(k)
        large.particles=Identity()
        self.assertGreater(large.oriented_count,2**53)
        self.assertEqual(large.draw(Fixed(n*n-1)),(n-1,n-1))
        self.assertEqual(large.draw(Fixed(n*n-2)),(n-1,n-2))

    def test_two_particle_event_probability_and_waiting_time_law(self):
        x=np.array([[-.25,0.,0.],[.25,0.,0.]])
        initial=np.array([[1.,0.,0.],[-1.,0.,0.]])
        mass=np.full(2,1000.);mask=np.ones(2,bool);rng=np.random.default_rng(78302)
        lam=hazard(x,initial,0,1,1.,mass[0]);trials=2500
        for target_exposure in (.15,.65):
            dt=target_exposure/lam;hits=0
            for _ in range(trials):
                report=cell.scatter(x,initial.copy(),mass,mask,dt,1.,rng)
                self.assertIn(report['n'],(0,1));hits+=report['n']
            p=-np.expm1(-target_exposure)
            self.assertAlmostEqual(hits/trials,p,delta=5*np.sqrt(p*(1-p)/trials)+1/trials)

    def test_first_event_rate_in_sparse_nonduniform_cells_matches_scalar_hazard(self):
        rng=np.random.default_rng(78303)
        x=np.array([[-2.1,0,0],[-1.8,0,0],[-.2,.1,0],[.2,0,0],[.7,.1,0],[2.1,0,0]])
        initial=rng.normal(size=x.shape)*.2;m=np.full(len(x),20000.);mask=np.ones(len(x),bool)
        lam=sum(hazard(x,initial,i,j,1.,m[0]) for i in range(len(x)) for j in range(i+1,len(x)))
        dt=.15/lam;hits=0;trials=2000
        for _ in range(trials):hits+=cell.scatter(x,initial.copy(),m,mask,dt,1.,rng)['n']>0
        p=-np.expm1(-.15)
        self.assertAlmostEqual(hits/trials,p,delta=5*np.sqrt(p*(1-p)/trials)+1/trials)

    def test_central_elastic_E_P_vectorJ_stars_and_exact_grid_translation(self):
        rng=np.random.default_rng(78304)
        x=rng.normal(size=(15,3))*.2;initial=rng.normal(size=(15,3))*.2
        mask=np.arange(15)<12;m=np.where(mask,1.e5,2.e4)
        v=initial.copy();w=initial+[100.,-30.,20.]
        report=cell.scatter(x,v,m,mask,.1,1.,np.random.default_rng(51))
        moved=cell.scatter(x+[80000.,0.,-30000.],w,m,mask,.1,1.,np.random.default_rng(51))
        self.assertGreater(report['n'],2)
        self.assertEqual(report['n'],moved['n']);self.assertEqual(report['proposals'],moved['proposals'])
        np.testing.assert_allclose(v,w-[100.,-30.,20.],atol=1.e-9,rtol=0.)
        self.assertAlmostEqual(np.sum(m[:,None]*v*v)/np.sum(m[:,None]*initial*initial),1.,delta=2.e-14)
        np.testing.assert_allclose(np.sum(m[:,None]*(v-initial),axis=0),0.,atol=1.e-9,rtol=0.)
        np.testing.assert_allclose(np.sum(np.cross(x,m[:,None]*(v-initial)),axis=0),0.,atol=1.e-9,rtol=0.)
        np.testing.assert_array_equal(v[~mask],initial[~mask])
        self.assertLess(np.linalg.norm(report['delta_J']),1.e-8)
        self.assertIn('cell',report['proposal_graph']);self.assertTrue(report['exact_integer_tickets'])
        self.assertEqual(report['elapsed_Myr'],.1)

    def test_null_outgoing_self_coincident_and_strict_h_boundary(self):
        m=np.full(2,1000.);mask=np.ones(2,bool)
        for x,v in (([[-.25,0,0],[.25,0,0]],[[-1.,0,0],[1.,0,0]]),
                    ([[0.,0,0],[1.,0,0]],[[1.,0,0],[-1.,0,0]]),
                    ([[0.,0,0],[0.,0,0]],[[1.,0,0],[-1.,0,0]])):
            x=np.array(x);v=np.array(v);old=v.copy()
            report=cell.scatter(x,v,m,mask,4.,1.,np.random.default_rng(78305))
            self.assertEqual(report['n'],0);np.testing.assert_array_equal(v,old)

    def test_fail_closed_domain_resolution_caps_and_inactive_cases(self):
        x=np.array([[-.25,0.,0.],[.25,0.,0.]])
        v=np.array([[-1.,0.,0.],[1.,0.,0.]])
        m=np.full(2,1000.);mask=np.ones(2,bool)
        self.assertEqual(cell.scatter(x,v.copy(),m,mask,0.,1.,np.random.default_rng(52))['n'],0)
        with self.assertRaises(RuntimeError):cell.scatter(x,v.copy(),m,mask,1000.,1.,np.random.default_rng(52),max_proposals=1)
        with self.assertRaises(RuntimeError):cell.scatter(x,v*1.e5,m,mask,1.,1.,np.random.default_rng(52))
        with self.assertRaises(ValueError):cell.CellProposal(x+1.e15,1.)
        with self.assertRaises(ValueError):cell.scatter(x,v.copy(),[1000.,2000.],mask,1.,1.,np.random.default_rng(52))
        rng=np.random.default_rng(78306);xx=rng.normal(size=(8,3))*.1;vv=rng.normal(size=(8,3))
        with self.assertRaises(RuntimeError):cell.scatter(xx,vv,np.full(8,1.e6),np.ones(8,bool),1.,1.,rng,max_events=1)
        for bad in (np.nan,np.inf,-1.):
            with self.assertRaises(ValueError):cell.scatter(x,v.copy(),m,mask,bad,1.,np.random.default_rng(52))

if __name__=='__main__':unittest.main()
