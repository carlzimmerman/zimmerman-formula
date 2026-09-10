import unittest
import mpmath as mp
import sympy as s
import logslip_reference as r


class ReferenceTests(unittest.TestCase):
    def test_fast_general_metric_formulas_against_actual_matrix(self):
        rr,B,Br,g,gr,X,U,w,F=s.symbols('r B Br g gr X U w F',nonzero=True)
        a=r.general.metric_invariants(rr,B,Br,g,gr)
        d=r.general.linear_system(a,X,U,w,F,s.Integer(1),s.Integer(0),sqrt=s.sqrt)
        p=s.sqrt(B*U);Q=2*X+U;b=Br/(2*B)
        S=4*F*(a['rho']+a['pt'])/rr+4*w*(rr*g-1)/(B*rr**2)
        Gamma=p*rr*S/(2*Q*w)
        L=2*F*(a['rho']+a['pr'])+2*w*(g+b)/B+3*w*w/(F*B)
        W=B*(L-2*X*w*Gamma/p)/2
        H=((2/rr+w/F)*U-(2*g+w/F)*X)/p
        kappa=2*d['P']/F+H*Gamma
        residual=s.Matrix(d['matrix'])*s.Matrix([W,kappa,Gamma])-s.Matrix(d['rhs'])
        self.assertTrue(all(s.factor(value)==0 for value in residual))

    def test_geometry_and_not_zero_pressure(self):
        with mp.workdps(60):
            a=r.geometry('1e-6','.1')
            self.assertLess(abs(mp.sqrt(a['B'])-1-a['r']*a['g']),mp.mpf('1e-55'))
            self.assertLess(abs(a['pr']+a['g']**2/a['B']),mp.mpf('1e-40'))
            self.assertNotEqual(a['pr'],0)
            old=r.general.geometry('1e-6','.1',0)
            self.assertNotEqual(a['B'],old['B'])
            direct=mp.diff(lambda y:r.geometry('1e-6',y)['B'],a['y'])/a['ry']
            self.assertLess(abs(direct-a['Br']),mp.mpf('1e-45'))

    def test_explicit_zero_pressure_generic_control(self):
        with mp.workdps(55):
            a=r.general.geometry('1e-6','.1',0)
            args=list(map(mp.mpf,('.5','1e-7','-.01','.525')))
            new=r.general.normalized(a,*args)
            old=r.general.closed.normalized(mp.mpf('1e-6'),mp.mpf('.1'),*args,backend=mp)
            for key in ('P','W','kappa','gamma'):
                self.assertLess(abs(new[key]-old[key])/max(abs(old[key]),1),mp.mpf('1e-35'))

    def test_first_jets_and_actual_P_derivative(self):
        with mp.workdps(55):
            a=r.control();f=mp.mpf('.05');j=mp.mpf('-3000')
            phys=r.physical_state(a,f,j);jet=r.jets(a,f,j)
            for index,key in enumerate(('P','PX','GX')):
                self.assertLess(abs(jet[index]-phys[key])/max(abs(phys[key]),1),mp.mpf('1e-35'))
            point=[a[k] for k in r.STATE_KEYS];v=r.flow(a,f,j)[:5]
            derivative=mp.diff(lambda t:r.normalized(a['eps'],*[x+t*d for x,d in zip(point,v)])['P'],0)
            self.assertLess(abs(derivative-jet[1])/max(abs(jet[1]),1),mp.mpf('1e-30'))

    def test_original_EF_health_and_on_shell(self):
        with mp.workdps(55):
            out=r.evaluate(r.control(),mp.mpf('.05'),mp.mpf('-3000'))
            for key in ('EF_Einstein_error','EF_current_error','physical_Einstein_error','physical_current_error'):
                self.assertLess(out[key],mp.mpf('1e-35'),key)
            self.assertTrue(out['strict_EF_scalar_cone'])

    def test_next_includes_changing_f_and_third_jets(self):
        with mp.workdps(50):
            a=r.control();f=mp.mpf('.05');j=mp.mpf('-3000');ell=mp.mpf('7')
            p0=[a[k] for k in r.STATE_KEYS]+[f];v=r.flow(a,f,j)
            def moved(t):
                pt=[x+t*d for x,d in zip(p0,v)]
                return r.jets(r.normalized(a['eps'],*pt[:5]),pt[5],j+t*ell)
            direct=mp.matrix([mp.diff(lambda t:moved(t)[i],0) for i in (3,4)])
            predicted=r.third_jets(a,f,j,ell)
            for x,y in zip(direct,predicted):
                self.assertLess(abs(x-y)/max(abs(x),1),mp.mpf('1e-30'))
            wrong=r.next_derivatives(a,f,0)
            right=r.next_derivatives(a,f,j)
            self.assertGreater(mp.norm(right-wrong),1)

    def test_shared_action_gap_and_same_state_control(self):
        with mp.workdps(45):
            a=r.control();b=r.control('2e-6');f=mp.mpf('.05');j=mp.mpf('-3000')
            self.assertEqual(list(r.matching_gap(a,a,f,j)),[0]*5)
            self.assertGreater(mp.norm(r.matching_gap(a,b,f,j)),1)
            self.assertEqual(a['F'],b['F']);self.assertEqual(a['X'],b['X'])


if __name__=='__main__':unittest.main()
