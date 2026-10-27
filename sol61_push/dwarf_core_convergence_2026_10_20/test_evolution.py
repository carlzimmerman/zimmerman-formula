"""Independent integrator and matched quiet-initial-state checks."""
import unittest
import numpy as np

try:
    import evolution
except ImportError:
    evolution=None


class EvolutionTests(unittest.TestCase):
    def test_hamiltonian_fourth_order_against_analytic_oscillator(self):
        # A missing kick, wrong composition coefficient, or second-order
        # replacement loses fourth-order convergence to the analytic solution.
        self.assertIsNotNone(evolution,'fourth-order step not implemented')
        def force(x):
            return (-x,None,None,np.zeros_like(x),None)
        errors=[]
        for dt in (.2,.1):
            x=np.array([[1.,0.,0.]]);v=np.zeros((1,3));state=force(x)
            for _ in range(round(2./dt)):
                state=evolution.h4_step(x,v,dt,force,state)
            errors.append(np.linalg.norm(np.r_[x[0,0]-np.cos(2.),v[0,0]+np.sin(2.)]))
        self.assertGreater(errors[0]/errors[1],14.)
        self.assertLess(errors[0]/errors[1],18.)

    def test_hamiltonian_kick_receipts_close_work(self):
        # Incorrect midpoint velocity or signed kick duration breaks exact
        # discrete kinetic work, including the negative composition kicks.
        self.assertIsNotNone(evolution,'kick receipts not implemented')
        x=np.array([[1.,2.,-.5]]);v=np.array([[.3,-.2,.4]])
        kinetic0=.5*np.sum(v*v);work=[];durations=[]
        def force(xx):return (-xx,None,None,-xx,None)
        def receipt(xx,before,after,state,delta):
            work.append(float(np.sum(.5*(before+after)*state[3]*delta)))
            durations.append(delta)
        evolution.h4_step(x,v,.1,force,force(x),receipt)
        self.assertAlmostEqual(sum(work),.5*np.sum(v*v)-kinetic0,places=14)
        self.assertAlmostEqual(sum(durations),.1,places=14)
        self.assertTrue(any(d<0 for d in durations))

    def test_quiet_raw_phases_nested(self):
        # Changing dimension/seed between resolution levels or losing the
        # opposite partner makes refinement confound gross phase changes.
        self.assertIsNotNone(evolution,'nested quiet phases not implemented')
        a,b=evolution.quiet_phases(32,19),evolution.quiet_phases(64,19)
        np.testing.assert_array_equal(a,b[:32])

    def test_initial_distribution_moments_and_antithetic_bulk(self):
        self.assertIsNotNone(evolution,'quiet initial conditions not implemented')
        # This is an independent analytic moment of a uniform unit ball.
        raw=evolution.quiet_phases(4096,19)
        q=evolution.unit_ball(raw)
        self.assertLess(abs(np.mean(np.sum(q*q,axis=1))-.6),.003)
        paired=np.r_[q,-q]
        np.testing.assert_allclose(paired.mean(axis=0),0.,atol=2e-16)


if __name__=='__main__':unittest.main()
