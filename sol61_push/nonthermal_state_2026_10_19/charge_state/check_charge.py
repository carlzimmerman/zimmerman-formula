"""Finite controls for the positive-charge and failed square-dark constructions."""
import json, pathlib, sys
import sympy as s
import numpy as np
import mpmath as mp

checks=[]
def check(name,condition,detail=None):
    assert bool(condition),(name,detail)
    checks.append({'name':name,'passed':True,'detail':detail})

delta=s.Rational(3);c=s.Rational(1,5);kap=s.Rational(1,7);k=kap+c*c/delta
for Q in range(17):
    size=Q//2+1
    A=s.diag(*[(Q-2*j)*(Q-2*j-1) for j in range(size)])
    H=s.zeros(size)
    F=s.zeros((Q-2)//2+1 if Q>=2 else 0,size)
    for j in range(size):
        n=Q-2*j
        H[j,j]=delta*j+k*n*(n-1)
        if j+1<size:
            H[j,j+1]=H[j+1,j]=c*s.sqrt((j+1)*n*(n-1))
        if j>0:
            F[j-1,j]=s.sqrt(delta*j)
        if n>=2:
            F[j,j]=c/s.sqrt(delta)*s.sqrt(n*(n-1))
    v=s.Matrix([(-c/delta)**j*s.sqrt(s.factorial(Q)/(s.factorial(Q-2*j)*s.factorial(j))) for j in range(size)])
    check('square decomposition Q='+str(Q),s.simplify(H-F.T*F-kap*A)==s.zeros(size))
    check('exact F-dark vector Q='+str(Q),s.simplify(F*v)==s.zeros(F.rows,1))
    if Q>=2:
        check('F rank/nullity Q='+str(Q),F.rank()==size-1)
        norm=(v.T*v)[0]
        var=s.simplify((v.T*A*A*v)[0]/norm-((v.T*A*v)[0]/norm)**2)
        check('dark state not stationary Q='+str(Q),var>0,{'contact_variance':str(var)})
        evals,evecs=np.linalg.eigh(np.array(H.evalf(),dtype=float))
        check('positive finite-Q ground and gap Q='+str(Q),evals[0]>0 and evals[1]-evals[0]>1e-12,
              {'excitation_ground':float(evals[0]),'gap':float(evals[1]-evals[0])})

n,beta,cc,kk,dd,mu=s.symbols('n beta c k delta mu',positive=True)
A=s.Matrix([[2*kk,-cc/beta],[-cc/beta,cc*n/(2*beta**3)]])
v=s.Matrix([2,-1]);J=2*cc*n*beta
L=(v.T*A*v)[0]
gap=s.expand(J*L)
check('symbolic conversion gap',s.simplify(gap-(16*kk*cc*n*beta+cc**2*n**2/beta**2+8*cc**2*n))==0)
r,De=s.symbols('r Delta',positive=True)
identity=gap.subs(kk,(mu+2*cc*beta)/(2*n)).subs(cc,beta*De/n).subs(beta**2,r*n)
check('gap composition identity',s.simplify(identity-(De**2*(1+4*r)**2+8*r*mu*De))==0)

# Independent numerical checks of the stationary fixed-charge minimum.
mp.mp.dps=40
dm=mp.mpf('.02');cm=mp.mpf('.003');km=mp.mpf('.002');m=mp.mpf(1);M=2+dm
for mum in map(mp.mpf,['.00001','.0001','.001']):
    De=dm-2*mum;nm=mum/(2*(km-cm*cm/De));bm=cm*nm/De;qm=nm+2*bm*bm
    energy=lambda ss:dm*ss-2*cm*(qm-2*ss)*mp.sqrt(ss)+km*(qm-2*ss)**2
    check('stationary composition mu='+str(mum),abs(mp.diff(energy,bm*bm))<mp.mpf('1e-30'))
    check('composition curvature mu='+str(mum),mp.diff(energy,bm*bm,2)>0)
    Am=mp.matrix([[2*km,-cm/bm],[-cm/bm,cm*nm/(2*bm**3)]])
    check('positive matter Hessian mu='+str(mum),Am[0,0]>0 and mp.det(Am)>0)
    for z in map(mp.mpf,['.0001','.001','.01']):
        Bm=mp.matrix([[z*nm/m,0],[0,z*bm*bm/M]])+2*cm*nm*bm*mp.matrix([[4,-2],[-2,1]])
        tr=(Am*Bm)[0,0]+(Am*Bm)[1,1];det=mp.det(Am)*mp.det(Bm)
        disc=mp.sqrt(tr*tr-4*det)
        lo=(tr-disc)/2;hi=(tr+disc)/2
        check('positive matter modes '+str((mum,z)),lo>0 and hi>lo)

# Vacuum X decay agrees with the same NR pair-production vertex at threshold.
for detuning in map(mp.mpf,['.01','.001','.0001']):
    mass=2+detuning;g=mp.mpf('.003')
    cnr=g/(2*mp.sqrt(2*mass))
    nr=cnr*cnr*mp.sqrt(detuning)/mp.pi
    rel=g*g/(8*mp.pi*mass)*mp.sqrt(1-4/(mass*mass))
    expected=mp.sqrt(4+detuning)/(2+detuning)
    check('NR decay matching delta='+str(detuning),abs(rel/nr-expected)<mp.mpf('1e-30'))

out={'all_passed':True,'count':len(checks),'checks':checks,'finite_scope':'Q=0..16 exact finite matrices; three stable homogeneous NR backgrounds and nine nonzero momenta; three vacuum near-threshold decay comparisons. No full relativistic quantum state, preparation, nonlinear evolution or lifetime was simulated.'}
pathlib.Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'count':len(checks),'all_passed':True}))
