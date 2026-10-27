"""argon_clues: what the 'S^2 orientation measure' derivation actually fixes."""
import sympy as s
G,c,rho=s.symbols('G c rho',positive=True)
K=4*s.pi*G
def kappa(projection, solid_angle):
    Kdir=K/solid_angle
    return s.simplify(projection*s.sqrt(Kdir*rho)/s.sqrt(G*rho))
print('Step 4 of the pasted script is a0 = <cos> * c * sqrt(K_dir rho) : a typed formula, not an output of W_rem (the computed W_poly_diff = a0^2/2 is never used).')
th=s.symbols('th')
proj={'<cos>_hemisphere':s.Rational(1,2),'<cos^2>_sphere (Langevin weak field)':s.Rational(1,3),'sqrt<cos^2>_sphere':1/s.sqrt(3),'<|cos|>_sphere':s.Rational(1,2),'<cos>_hemisphere (flux weighted)':s.Rational(2,3)}
for pn,pv in proj.items():
    for an,av in (('4pi (full S^2)',4*s.pi),('2pi (hemisphere)',2*s.pi)):
        print('  projection %-38s solid angle %-18s -> kappa = %s = %.4f'%(pn,an,kappa(pv,av),float(kappa(pv,av))))
print('=> kappa = 1/2 only for (<cos>_hemi, divide by 4pi) [and the equivalent (<|cos|>_sphere, 4pi)]; other equally natural choices give 0.33, 0.47, 0.58, 0.67, 0.71, 0.82, 0.94; the choice is made after the target is known.')
print('Mutation as written (omit S^2 normalisation) just reinstates kappa = sqrt(4pi)/2 = %.3f: it changes an input, it does not test the derivation.'%float(kappa(s.Rational(1,2),1)))
print('Kill-test numbers: pasted prediction a0(2)/a0(0) = 1.00 +- 0.04 or 0.94 +- 0.05 under DESI; the DESI CPL summary (p13c) gives 0.77-0.94 (68%) at z=2 across four fits -> 0.94 is the top of the band, and thresholds >=1.25 / <=0.70 differ from the sealed CFG571/778 criteria, which govern.')
