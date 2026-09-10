import unittest
from pathlib import Path
import importlib.util
import sympy as s

class RadialActionTests(unittest.TestCase):
    def model(self):
        path=Path(__file__).with_name('radial_action.py')
        self.assertTrue(path.exists(),'DHOST radial action is absent')
        spec=importlib.util.spec_from_file_location('tested_dhost_radial',path)
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        return m

    def test_radial_EH_boundary_identity(self):
        m=self.model();a=m.build()
        self.assertEqual(s.factor(a['EH_boundary_residual']),0)

    def test_auxiliary_constraint_is_varied(self):
        m=self.model();a=m.build();v=a['symbols']
        want=v['X']-v['q']**2/(2*v['N']**2)+v['p']**2/(2*v['B'])
        self.assertEqual(s.factor(a['EL']['lam']/a['measure']-want),0)

    def test_constant_F_KGB_current_recovered(self):
        m=self.model();a=m.build();v=a['symbols']
        off={v[k]:0 for k in ('f','j','D','Dx')}
        equation=a['EL']['X'].subs(off)
        slope=s.diff(equation,v['lam'])
        self.assertNotEqual(slope,0)
        lam=-equation.subs(v['lam'],0)/slope
        actual=(a['current']/a['measure']).subs(off).subs(v['lam'],lam)
        want=(-v['Px']*v['p']+v['Gx']*(a['box']*v['p']+v['X1']))/v['B']
        self.assertEqual(s.factor(actual-want),0)

    def test_new_operator_changes_actual_equations(self):
        m=self.model();a=m.build();v=a['symbols']
        self.assertNotEqual(s.factor(s.diff(a['current'],v['D'])),0)

    def test_raw_radial_covariant_contractions(self):
        m=self.model();a=m.build();v=a['symbols']
        N,B,p,q,r=[v[k] for k in ('N','B','p','q','r')]
        g=v['N1']/N;b=v['B1']/(2*B);p1=v['p1']
        eta=s.diag(-1,1,1,1);cov=s.Matrix([q/N,p/s.sqrt(B),0,0]);con=eta*cov
        H=s.diag(-g*p/B,(p1-b*p)/B,p/(B*r),p/(B*r))
        H[0,1]=H[1,0]=-q*g/(N*s.sqrt(B))
        pair=(con.T*H*con)[0]
        raw=[s.trace(eta*H)*pair,(con.T*H*eta*H*con)[0],pair**2]
        z=-q*q*g/(N*N)-p*p1/B+p*p*v['B1']/(2*B*B)
        for value,key in zip(raw,('L3','L4','L5')):
            self.assertEqual(s.factor(value-a[key].subs(v['X1'],z)),0)

if __name__=='__main__':unittest.main(verbosity=2)
