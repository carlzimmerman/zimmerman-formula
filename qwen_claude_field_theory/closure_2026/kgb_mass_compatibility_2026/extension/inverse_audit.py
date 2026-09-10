#!/usr/bin/env python3
"""Bounded independent audit of conformal_inverse.py at representative jets.

Reconstruct a 3x3 current/lapse/pressure-preservation system using direct
mpmath derivatives; audit the author's reduced 2x2 solve and complex step.
Then check original EF KGB stress against independently differentiated EF
geometry. This is a vacuum local diagnostic, not a continuation certificate.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import sys
import unittest
import mpmath as mp
import ef_principal as ef

ROOT_PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT_PACKAGE))
import conformal_inverse as root

CASES = [('.1','.1','.25','1.5'),('.1','.1','.25','.5'),('1','.001','.75','1'),
         ('2','1','1.25','1.5'),('20','.000001','.25','2')]


def geometry(eps,y):
    radius = lambda v:eps/mp.sqrt(v*(-mp.expm1(-v)))
    gg = lambda v:v/(1-2*radius(v)*v)
    BB = lambda v:1+2*radius(v)*gg(v)
    r,ry = radius(y),mp.diff(radius,y)
    g,B = gg(y),BB(y)
    gr,Br = mp.diff(gg,y)/ry,mp.diff(BB,y)/ry
    rho = (1-1/B)/r**2+Br/(B**2*r)
    pr = (1/B-1)/r**2+2*g/(B*r)
    pt = (gr+g*g-g*Br/(2*B)+(g-Br/(2*B))/r)/B
    return dict(r=r,ry=ry,g=g,gr=gr,B=B,Br=Br,rho=rho,pr=pr,pt=pt)


def pressure(eps,y,X,z,sigma):
    a = geometry(eps,y)
    F,Fx = (1+sigma*X)/2,sigma/2
    return (2*Fx*z*(a['g']+2/a['r'])+3*Fx**2*z*z/(2*F))/a['B']


def independent_coefficients(eps,y,X,U,P,sigma):
    a = geometry(eps,y)
    r,g,B,Br = [a[k] for k in ('r','g','B','Br')]
    F,Fx = (1+sigma*X)/2,sigma/2
    K,Kx = 3*Fx**2/(2*F),-3*Fx**3/(2*F**2)
    aa = g+2/r
    z = B*P/(Fx*(aa+mp.sqrt(aa*aa+3*B*P/(2*F))))
    py = mp.diff(lambda v:pressure(eps,v,X,z,sigma),y)
    pX = mp.diff(lambda v:pressure(eps,y,v,z,sigma),X)
    pz = mp.diff(lambda v:pressure(eps,y,X,v,sigma),z)
    p = mp.sqrt(B*U)
    Q = 2*X*(U/X-r*g)/(p*r)
    Ricci = a['rho']-a['pr']-2*a['pt']
    # Unknown vector is (X'',P_X,G_X), without pre-eliminating X''.
    matrix = mp.matrix([[pz,-z,0],[-2*K/B,1,-Q],[2*Fx/B,0,2*X*z/p]])
    rhs = mp.matrix([-(pX*z+py/a['ry']),
        -Fx*Ricci+Kx*z*z/B+2*K*(g-Br/(2*B)+2/r)*z/B,
        2*F*a['rho']+P+K*z*z/B-2*Fx*(2/r-Br/(2*B))*z/B])
    zr,PX,GX = mp.lu_solve(matrix,rhs)
    return dict(**a,X=X,U=U,P=P,sigma=sigma,z=z,zr=zr,PX=PX,GX=GX,
                pressure_gradient_coefficient=pz,three_by_three_determinant=mp.det(matrix),
                three_by_three_residual=max(abs(v) for v in matrix*mp.matrix([zr,PX,GX])-rhs))


def independent_curvatures(eps,y,X,U,P,sigma):
    a = independent_coefficients(eps,y,X,U,P,sigma)
    point = (y,X,U,P)
    tangent = (1/a['ry'],a['z'],-2*a['g']*(2*X+U)-2*a['z'],a['PX']*a['z'])
    def differentiated(key):
        return mp.diff(lambda t:independent_coefficients(eps,*[v+t*d for v,d in zip(point,tangent)],sigma)[key],mp.mpf(0))/a['z']
    return a,differentiated('PX'),differentiated('GX')


def background(a,sigma):
    X,U,r,B,Br,g,z = [a[k] for k in ('X','U','r','B','Br','g','z')]
    p = mp.sqrt(B*U)
    Ur = -2*g*(2*X+U)-2*z
    return dict(r=r,A=1/(2*X+U),B=B,g=g,BrB=Br/B,p=p,
                pr=p*(Br/B+Ur/U)/2,X=X,Xr=z,sigma=sigma,q=mp.mpf(-1))


def ef_on_shell(a,sigma,PXX,GXX):
    out = ef.evaluate(mp.mpf(1),background(a,sigma),
        dict(P=a['P'],PX=a['PX'],PXX=PXX,GX=a['GX'],GXX=GXX))
    C,h,D,R,Bt,gt,pt = [out['background'][k] for k in ('C','h','D','R','B','g','p')]
    hp = sigma*a['zr']/C-h*h
    Dp = h/2+a['r']*hp/2
    BrBt = (a['Br']/a['B']-2*Dp/D)/(mp.sqrt(C)*D)
    gRt = (a['gr']+hp/2-(a['g']+h/2)*(h/2+Dp/D))/(C*D*D)
    geometric = [(1-1/Bt)/R**2+BrBt/(Bt*R),
        (1/Bt-1)/R**2+2*gt/(Bt*R),
        (gRt+gt*gt-gt*BrBt/2+(gt-BrBt/2)/R)/Bt]
    stress = out['stress']
    scale = max(abs(v) for v in geometric)
    error = max(abs(stress[0,0]-geometric[0]),abs(stress[1,1]-geometric[1]),
        abs(stress[2,2]-geometric[2]),abs(stress[0,1]))/scale
    box = -out['background']['H'][0][0]+sum(out['background']['H'][i][i] for i in (1,2,3))
    chiR = a['z']/(C**mp.mpf('2.5')*D)
    current_terms = [out['action']['P1']*pt/Bt,-out['action']['G1']*box*pt/Bt,
                     -out['action']['G1']*chiR/Bt]
    current_error = abs(sum(current_terms))/sum(abs(v) for v in current_terms)
    return dict(relative_EF_Einstein_stress_error=error,relative_EF_current_error=current_error,
        EF_rho=geometric[0],EF_pr=geometric[1],EF_pt=geometric[2],
        kinetic=out['kinetic'],cross=out['cross'],radial=out['radial'],angular=out['angular'],
        light_margin=out['light_margin'],clock_norm_error=out['relative_clock_norm_error'],
        clock_derivative_error=out['relative_clock_derivative_error'],
        bounded_EF=out['bounded_EF_static_quadratic_energy'],strict_cone_EF=out['strict_EF_scalar_cone'])


@lru_cache(None)
def audit_case(case,dps=80):
    with mp.workdps(dps):
        y,sigma,b,d = map(mp.mpf,case)
        eps,X = mp.mpf('1e-6'),mp.mpf('.5')
        metric = geometry(eps,y)
        U = b*X*metric['r']*metric['g']
        P = pressure(eps,y,X,-d*metric['g'],sigma)
        a,PXX,GXX = independent_curvatures(eps,y,X,U,P,sigma)
        check = ef_on_shell(a,sigma,PXX,GXX)
        fy,fs,fb,fd = map(float,case)
        fX,fU,fP = root.initial(1e-6,fy,fs,fb,fd)
        author = root.inspect(1e-6,fy,fX,fU,fP,fs)
        reference = dict(PX=a['PX'],PXX=PXX,GX=a['GX'],GXX=GXX,z=a['z'],zr=a['zr'],
            **{k:check[k] for k in ('kinetic','cross','radial','angular','light_margin')})
        errors = {k:abs(mp.mpf(author[k])-v)/max(abs(v),mp.mpf('1e-100')) for k,v in reference.items()}
        # Also check the helper at precisely the author's returned input jets.
        fa,fp2,fg2 = root.action_curvatures(1e-6,fy,fX,fU,fP,fs)
        fmp = {k:mp.mpf(v) for k,v in fa.items() if k in ('X','U','P','r','ry','g','gr','B','Br','z','zr','PX','GX')}
        helper_same_float_jet = ef_on_shell(fmp,mp.mpf(fs),mp.mpf(fp2),mp.mpf(fg2))
        same_errors = {k:abs(mp.mpf(author[k])-helper_same_float_jet[k])/max(abs(helper_same_float_jet[k]),mp.mpf('1e-100'))
                       for k in ('kinetic','cross','radial','angular','light_margin')}
        return dict(case=list(case),dps=dps,reference=reference,independent_EF=check,
            author=author,author_relative_errors=errors,
            author_helper_same_jet_relative_errors=same_errors,
            author_jet_EF_stress_error=helper_same_float_jet['relative_EF_Einstein_stress_error'],
            regular_chart=dict(C=1+sigma*X,X=X,U=U,B=a['B'],
                D=1+a['r']*sigma*a['z']/(2*(1+sigma*X)),sigma=sigma,
                z=a['z'],Pz=a['pressure_gradient_coefficient'],
                three_by_three_determinant=a['three_by_three_determinant']),
            source_3by3_residual=a['three_by_three_residual'])


class InverseAuditTests(unittest.TestCase):
    def test_representative_points_on_shell_in_EF(self):
        for case in CASES:
            row = audit_case(tuple(case))
            self.assertLess(row['independent_EF']['relative_EF_Einstein_stress_error'],mp.mpf('1e-55'))
            self.assertLess(row['independent_EF']['relative_EF_current_error'],mp.mpf('1e-55'))

    def test_root_dictionary_at_identical_jets(self):
        for case in CASES:
            row = audit_case(tuple(case))
            self.assertLess(max(row['author_helper_same_jet_relative_errors'].values()),mp.mpf('1e-12'))

    def test_root_solve_and_total_derivatives(self):
        for case in CASES:
            row = audit_case(tuple(case))
            for key in ('PX','PXX','GX','GXX','z','zr'):
                self.assertLess(row['author_relative_errors'][key],mp.mpf('1e-11'))

    def test_healthy_seed_and_regular_charts(self):
        healthy = audit_case(tuple(CASES[0]))
        self.assertTrue(healthy['independent_EF']['bounded_EF'])
        self.assertTrue(healthy['independent_EF']['strict_cone_EF'])
        for case in CASES:
            chart = audit_case(tuple(case))['regular_chart']
            for key in ('C','X','U','B','D'):
                self.assertGreater(chart[key],0)
            for key in ('sigma','z','Pz','three_by_three_determinant'):
                self.assertNotEqual(chart[key],0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--result-file',type=Path)
    args = parser.parse_args()
    tests = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(InverseAuditTests))
    result = ef.serial(dict(cases=[audit_case(tuple(case)) for case in CASES],
        tests=dict(run=tests.testsRun,failures=len(tests.failures),errors=len(tests.errors),passed=tests.wasSuccessful())))
    output = json.dumps(result,indent=2)+'\n'
    if args.result_file:args.result_file.write_text(output)
    else:print(output)
    return 0 if tests.wasSuccessful() else 1


if __name__=='__main__':raise SystemExit(main())
