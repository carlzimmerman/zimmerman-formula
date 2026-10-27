"""Exact static-kernel and finite-band discriminator; not a phase search."""
import json
import sys
from pathlib import Path
import sympy as s

checks = []
def ck(name, value):
    if not bool(value):
        raise AssertionError(name)
    checks.append({"name": name, "passed": True})
def zero(name, expr):
    if isinstance(expr, s.MatrixBase):
        ck(name, all(s.simplify(v) == 0 for v in expr))
    else:
        ck(name, s.simplify(expr) == 0)

z = s.symbols('z', positive=True)
rho = s.symbols('rho', real=True)
R = s.Rational
cases = [
    ('diagonal', s.diag(1,4), s.diag(1,R(1,2)), s.Matrix([1,2]), s.S.Zero),
    ('noncommuting_with_local_response', s.Matrix([[3,1],[1,2]]),
     s.Matrix([[2,1],[1,1]]), s.Matrix([1,-2]), R(1,3)),
    ('critical_zero_curvature', s.ones(2), s.diag(1,2), s.Matrix([1,-1]), s.S.Zero),
    ('pure_local_auxiliary', s.Matrix([[2,-1],[-1,3]]), s.zeros(2),
     s.Matrix([1,1]), s.S.Zero),
]

# An exact physical NR retained-source background, before the separately
# documented negative-frequency matching correction. Both mass source entries
# are retained; their interference may have either sign.
m=R(1); M=R(2001,1000); delta=M-2*m; c=R(1,10000)
g2=8*m*m*M*c*c; lam_rep=R(1,10000)
lam_tot=lam_rep+g2/(M*M-4*m*m); kc=lam_tot/(4*m*m)
mu=delta/1000; detuning=delta-2*mu
n=mu/(2*(kc-c*c/detuning)); b=-c*n/detuning
A=s.Matrix([[4*kc*n,2*c*s.sqrt(n)],[2*c*s.sqrt(n),detuning]])
B=s.diag(1/(2*m),1/(2*M))
q=s.sqrt(2)*m*s.Matrix([s.sqrt(n),2*b])
zero('source background phase equation',mu-2*kc*n-2*c*b)
zero('source background source equation',detuning*b+c*n)
ck('source background positive density and detuning',n>0 and detuning>0)
ck('source amplitude stability',A[0,0]>0 and A.det()>0)
ck('source fraction is small at declared point',s.simplify(b*b/n)<R(1,1000))
cases.append(('actual_retained_source_NR',A,B,q,s.S.Zero))

rows=[]
for name,A,B,q,local in cases:
    K=A+z*B
    inv=K.inv()
    v=inv*q
    chi=s.factor(local+(q.T*v)[0])
    h=s.factor(1/chi)
    diss=s.factor((v.T*B*v)[0])
    zero(name+' inverse derivative',s.diff(chi,z)+diss)
    zero(name+' positive inverse-response derivative',s.diff(h,z)-diss/chi**2)
    # Independent constrained-energy/KKT check, with a local auxiliary
    # population if the constant response local is present.
    if local:
        L=s.diag(K,s.Matrix([[1/local]]))
        Q=s.Matrix(list(q)+[1])
    else:
        L=K; Q=q
    x=L.inv()*Q*rho/(Q.T*L.inv()*Q)[0]
    zero(name+' constrained density', (Q.T*x)[0]-rho)
    zero(name+' constrained Euler equation', L*x-h*rho*Q)
    zero(name+' minimized energy', (x.T*L*x)[0]-h*rho**2)
    grid=([R(1,10**8),R(1,10**6),R(1,10**4)] if name.startswith('actual')
          else [R(1,100),R(1),R(100)])
    sample=[]
    for zz in grid:
        kval=K.subs(z,zz)
        ck(name+' positive kernel at '+str(zz),kval[0,0]>0 and kval.det()>0)
        ck(name+' nonnegative derivative at '+str(zz),s.simplify(diss.subs(z,zz))>=0)
        sample.append({'k_squared':str(zz),'chi':float(chi.subs(z,zz)),
                       'inverse_density_kernel':float(h.subs(z,zz)),
                       'inverse_kernel_derivative':float(s.diff(h,z).subs(z,zz))})
    ck(name+' finite ordering',all(sample[i]['inverse_density_kernel']<=sample[i+1]['inverse_density_kernel'] for i in range(2)))
    rows.append({'case':name,'chi_exact':str(chi),'h_exact':str(h),'samples':sample})

za,zb,kg=s.symbols('z_a z_b K_g',positive=True)
opt=2*kg/(za+zb)
err=(zb-za)/(zb+za)
zero('optimal endpoint lower error',1-opt/(kg/za)-err)
zero('optimal endpoint upper error',opt/(kg/zb)-1-err)
zero('endpoint feasibility bound',
     (1-err)*kg/za-(1+err)*kg/zb)
band=[]
for ratio in [R(11,10),R(2),R(10),R(100)]:
    bound=(ratio**2-1)/(ratio**2+1)
    ck('band bound is strict subunit '+str(ratio),0<bound<1)
    band.append({'k_ratio':str(ratio),'minimum_relative_uniform_error':str(bound),
                 'minimum_relative_uniform_error_float':float(bound)})

# A polynomial/contact plus healthy scalar exchange has the opposite slope
# from positive Coulomb restoring energy, even at its allowed critical tuning.
v0,coupling,ms2=s.symbols('v0 c M_squared',positive=True)
screened=v0-coupling**2/(z+ms2)
zero('healthy scalar exchange positive derivative',s.diff(screened,z)-coupling**2/(z+ms2)**2)
zero('critical contact cancellation leaves gradient kernel',
     screened.subs(v0,coupling**2/ms2)-coupling**2*z/(ms2*(z+ms2)))
zero('positive Coulomb has opposite derivative',s.diff(kg/z,z)+kg/z**2)

result={'claim_id':'CE-GRAV-STATIC-KERNEL-2026-10-19','checks_count':len(checks),
        'checks':checks,'cases':rows,'finite_band_bounds':band,
        'physical_point':{'m':str(m),'M':str(M),'delta':str(delta),'c3':str(c),
                          'lambda_rep':str(lam_rep),'density':str(n),
                          'source_fraction':float(b*b/n)},
        'scope':'Exact finite matrix/KKT identities and endpoint minimax algebra. General monotonicity/band conclusions use the explicit proof, not the finite sample count.',
        'non_claims':['No all-loop, all-phase or flowing/inhomogeneous medium theorem.',
                      'No original-model rational force, physical a0, or empirical prediction.',
                      'Retained source example is NR RWA before the documented small threshold correction; matrix sign argument is coefficient independent.']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks_count':len(checks),'finite_band_bounds':band}))
