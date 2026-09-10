import unittest
import mpmath as mp
import pressure_inverse as p


class GeneralInverseTests(unittest.TestCase):
    def test_symbolic_derivation(self):
        result=p.symbolic_checks()
        for key in ('pressure_derivative','determinant_residual','angular_residual','j_shift_residual','metric_identity'):
            self.assertTrue(all(value==0 for value in result[key]),key)

    def test_general_geometry_derivatives_and_bianchi(self):
        with mp.workdps(55):
            for eta in ('-2','0','3'):
                a=p.geometry('1e-6','.1',eta)
                direct=mp.diff(lambda yy:p.geometry('1e-6',yy,eta)['pr'],a['y'])/a['ry']
                self.assertLess(abs(direct-a['prr']),mp.mpf('1e-35'))
                identity=a['prr']+a['g']*(a['rho']+a['pr'])-2*(a['pt']-a['pr'])/a['r']
                self.assertLess(abs(identity)/max(abs(a['prr']),1),mp.mpf('1e-35'))
                self.assertLess(abs(a['pr']+mp.mpf(eta)*a['y']**2/a['B']),mp.mpf('1e-35'))

    def test_old_limit_original_closed_inverse(self):
        with mp.workdps(60):
            for j in ('0','-3000'):
                a=p.control('1e-6','.1','0',j)
                old=p.closed.coefficients(a['eps'],a['y'],a['X'],a['U'],a['f']*a['z'],a['F'],a['f'],a['j'],backend=mp)
                for key in ('P','PX','GX','zr'):
                    self.assertLess(abs(a[key]-old[key])/max(abs(old[key]),1),mp.mpf('1e-40'))

    def test_original_EF_and_physical_equations_nonzero_pressure(self):
        with mp.workdps(60):
            for eta in ('-2','3'):
                result=p.inspect_control('1e-6','.1',eta,'-3000')
                self.assertNotEqual(result['state']['pr'],0)
                for key in ('EF_Einstein_error','EF_current_error','physical_Einstein_error','physical_current_error','constitutive_P_error'):
                    self.assertLess(result[key],mp.mpf('1e-35'),key)
                self.assertLess(result['determinant_error'],mp.mpf('1e-40'))

    def test_pressure_omission_is_detected(self):
        with mp.workdps(50):
            a=p.control('1e-6','.1','3','0')
            wrong=dict(a);wrong['Echi']+=a['f']*a['pr']
            residual=p.physical_residuals(wrong)
            self.assertGreater(residual['physical_current_error'],mp.mpf('1e-12'))

    def test_no_inserted_healthy_verdict_and_common_eta_scaling(self):
        with mp.workdps(45):
            first=p.geometry('1e-6','.1','3');second=p.geometry('2e-6','.1','3')
            self.assertLess(abs(second['fractional_B_correction']/first['fractional_B_correction']-4),mp.mpf('1e-35'))
            for a in (first,second):
                self.assertLess(abs((a['B']-(1+2*a['r']*a['g']))-a['eta']*(a['r']*a['y'])**2),mp.mpf('1e-35'))

    def test_normalized_matches_physical_with_nonzero_pressure(self):
        with mp.workdps(55):
            for eta,j in (('-2','-3000'),('3','2500')):
                a=p.control('1e-6','.1',eta,j)
                n=p.normalized(a,a['X'],a['U'],a['f']*a['z'],a['F'])
                for left,right in ((n['P'],a['P']),(n['W'],a['f']*a['zr']+a['j']*a['z']**2),
                    (n['kappa'],a['PX']/a['f']),(n['gamma'],a['GX']/a['f']),
                    (n['inverse_determinant'],a['inverse_determinant'])):
                    self.assertLess(abs(left-right)/max(abs(left),abs(right),1),mp.mpf('1e-40'))


if __name__=='__main__':unittest.main()
