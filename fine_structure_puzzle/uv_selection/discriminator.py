"""Exact coupled-U(1) discriminator. See CONTRACT.md; this is not a full FRG run."""
import argparse
import json
from pathlib import Path
import sympy as s

p = argparse.ArgumentParser()
p.add_argument('--output', required=True)
p.add_argument('--mutate', action='store_true')
args = p.parse_args()
data = json.loads(Path('fine_structure_puzzle/uv_selection/source_equations.json').read_text())
F, gy, gx, gt, z = s.symbols('F gy gx gt z', positive=True)
lam = s.Symbol('lambda')
cs = (gy, gx, gt)
R = s.Rational
G = s.Matrix([[gy, gt], [0, gx]])
H = G * G.T
checks = []

def check(label, expr):
    ok = all(s.simplify(x) == 0 for x in list(expr)) if isinstance(expr, s.MatrixBase) else s.simplify(expr) == 0
    checks.append({'label': label, 'passed': bool(ok)})
    if not ok:
        raise AssertionError(label + ': ' + str(expr))

result = {'models': {}, 'arithmetic': 'exact SymPy rationals and symbolic polynomial identities', 'nonclaims': 'No full FRG fixed point, no alpha(0), no flavor/threshold fit'}
ys = list(map(R, data['Y']))
mults = data['fermion_multiplicities_per_generation']

for name, model in data['models'].items():
    xs = list(map(R, model['X']))
    qs = [s.Matrix([y, x]) for y, x in zip(ys, xs)]
    B = s.zeros(2)
    for q, multiplicity in zip(qs, mults):
        B += 3 * R(2, 3) * multiplicity * q * q.T
    for key, multiplicity in [('H_charge', 2), ('phi_charge', 1)]:
        q = s.Matrix(list(map(R, model[key])))
        B += R(1, 3) * multiplicity * q * q.T
    b1,b2,b3,b4,b5 = list(map(R, model['B_coefficients']))
    check(name + ': independently summed charge matrix', B-s.Matrix([[R(41,6), b2/2],[b2/2,b1]]))
    assert B.det() > 0 and B[0,0] > 0
    if args.mutate:
        b3 = -b3
    # Published beta_g1 converted to gY using g1^2=(5/3)gY^2.
    beta = s.Matrix([
        R(41,6)*gy**3 - F*gy,
        b1*gx**3 + R(41,6)*gx*gt**2 + b2*gx**2*gt - F*gx,
        R(5,3)*b3*gx*gy**2 + b4*gx*gt**2 + R(41,3)*gy**2*gt + b5*gx**2*gt + R(41,6)*gt**3 - F*gt
    ])
    from_triangular = s.zeros(2)
    for coord, component in zip(cs, beta):
        from_triangular += H.diff(coord)*component
    check(name + ': triangular beta equals invariant matrix beta', from_triangular-2*(H*B*H-F*H))
    hstar = F*B.inv()
    # Algebraic inverse of triangular matrix: gY^2=H11-H12^2/H22.
    gxstar = s.sqrt(hstar[1,1])
    gtstar = s.simplify(hstar[0,1]/gxstar)
    gystar = s.sqrt(s.simplify(hstar[0,0]-hstar[0,1]**2/hstar[1,1]))
    subsstar = dict(zip(cs, [gystar, gxstar, gtstar]))
    check(name + ': nonzero source fixed point', beta.subs(subsstar))
    J = beta.jacobian(cs)
    check(name + ': full rank characteristic polynomial', J.subs(subsstar).charpoly(lam).as_expr()-(lam-2*F)**3)
    # Rank-one ellipse at gy=0, arbitrary slope z=gt/gx.
    Q = B[1,1] + 2*B[0,1]*z + B[0,0]*z*z
    rankone = {gy:0, gx:s.sqrt(F/Q), gt:z*s.sqrt(F/Q)}
    check(name + ': rank-one fixed ellipse for arbitrary slope', beta.subs(rankone))
    # z=1 is an independent exact hand-computable point on each ellipse.
    check(name + ': rank-one characteristic polynomial', J.subs(rankone).subs(z,1).charpoly(lam).as_expr()-lam*(lam+F)*(lam-2*F))
    # Physical matching for phi=(0,1), unbroken n=(1,0), rather than arbitrary charge norm.
    K = s.simplify(H.inv())
    check(name + ': physical surviving hypercharge', K[0,0]-1/gy**2)
    check(name + ': matched full rank hypercharge', (hstar.inv())[0,0]-R(41,6)/F)
    # Subtract beta_yt/yt-beta_yb/yb; left-doublet and universal f_y cancel.
    qu, qd = qs[1], qs[2]
    delta_norm = s.expand((qu.T*H*qu)[0]-(qd.T*H*qd)[0])
    c1,c2,c3 = list(map(R, model['C_coefficients']))
    delta_source = gy**2/3 + (c2+R(2,3))*gx**2/3 - (c1-c3)*gx*gt/3 + gt**2/3
    check(name + ': Yukawa difference from independent charge norm', delta_norm-delta_source)
    delta_star = s.simplify(delta_norm.subs(subsstar))
    ratio = s.simplify(delta_star/(gystar*gystar))
    # Fixed lattice basis covariance (unimodular shear, followed by integral units).
    S = s.Matrix([[1,1],[0,1]])
    Bprime = S*B*S.T
    hprime = S.inv().T*hstar*S.inv()
    check(name + ': fixed-lattice basis covariance', hprime-F*Bprime.inv())
    check(name + ': charge norm basis invariance', ((S*qu).T*hprime*(S*qu))[0]-(qu.T*hstar*qu)[0])
    result['models'][name] = {
      'B': [[str(v) for v in row] for row in B.tolist()], 'det_B':str(B.det()),
      'Hstar_over_F': [[str(v) for v in row] for row in B.inv().tolist()],
      'gYstar_squared_over_F':str(s.simplify(gystar**2/F)),
      'gxstar_squared_over_F':str(s.simplify(gxstar**2/F)),
      'gtstar_over_gxstar':str(s.simplify(gtstar/gxstar)),
      'full_rank_rescaled_eigenvalues':['2*F']*3,
      'rank_one_rescaled_eigenvalues':['-F','0','2*F'],
      'Yukawa_delta_over_F':str(s.simplify(delta_star/F)),
      'Yukawa_delta_over_gY_squared':str(ratio),
      'Yukawa_delta_over_gY_squared_decimal':float(ratio),
      'conditional_F_from_nonzero_Yukawa_delta':str(s.simplify(F/delta_star)),
      'at_F_1_5473_illustration_only':{'gYstar':float(gystar.subs(F,R(15473,10000))), 'gxstar':float(gxstar.subs(F,R(15473,10000))), 'gtstar':float(gtstar.subs(F,R(15473,10000)))}
    }

# Exact continuum of UV-complete trajectories in either model, whitened H=c Hstar.
c, tau = s.symbols('c tau', positive=True)
a = c/(c+(1-c)*s.exp(2*F*tau))
check('continuum trajectory solves dc/dtau=2F c(c-1)', s.diff(a,tau)-2*F*a*(a-1))
check('continuum initial value', a.subs(tau,0)-c)
result['continuum'] = {'domain':'0<c<1, tau=t/(16*pi**2)>=0', 'c_of_tau':str(a), 'UV_limit':'0', 'implication':'UV completeness alone admits continuum; full-rank endpoint is an extra branch selection'}
# This second continuum has a non-Gaussian rank-one UV endpoint. No matrix
# square root is needed to check its universal whitened projector equation.
X = s.diag(1,a)
check('interacting-endpoint continuum satisfies whitened matrix flow', X.diff(tau)-2*F*(X*X-X))
result['interacting_endpoint_continuum'] = {'X_of_tau':'P+c(tau)*(I-P), P^2=P, rank(P)=1', 'UV_limit':'P, not zero', 'parameter':'0<c(0)<1', 'implication':'Even at least one interacting matter coupling does not select unique finite-scale H'}
result['checks'] = checks
result['check_count'] = len(checks)
Path(args.output).parent.mkdir(parents=True, exist_ok=True)
Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
print(json.dumps(result, indent=2, sort_keys=True))
