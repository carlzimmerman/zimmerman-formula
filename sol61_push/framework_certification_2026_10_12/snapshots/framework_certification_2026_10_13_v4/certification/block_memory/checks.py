from pathlib import Path
import json,sys
import sympy as s

dest=Path(sys.argv[1]); checks=[]
def z(name,expr):
    r=s.simplify(expr)
    ok=(r==s.zeros(*r.shape)) if isinstance(r,s.MatrixBase) else (r==0)
    checks.append({'name':name,'passed':bool(ok),'residual':str(r)})
def yes(name,condition):checks.append({'name':name,'passed':bool(condition),'condition':str(condition)})

E=s.symbols('E',real=True)
# Exact block fixture; general causal derivation is recorded separately.
A=s.Matrix([[s.Rational(1,2),s.Rational(1,7)],[s.Rational(1,7),s.Rational(3,4)]])
B=s.Matrix([[s.Rational(1,5)],[s.Rational(2,9)]])
C=s.Matrix([[s.Rational(5,6)]])
H=A.row_join(B).col_join(B.T.row_join(C))
z('fixture Hermitian block matrix',H-H.T)
S=E*s.eye(2)-A-B*(E*s.eye(1)-C).inv()*B.T
G=(E*s.eye(3)-H).inv()
z('full retained resolvent equals Schur inverse',G[:2,:2]-S.inv())
z('eliminated-retained resolvent block',G[2:3,:2]-(E*s.eye(1)-C).inv()*B.T*S.inv())
z('determinant Schur factorization',(E*s.eye(3)-H).det()-(E*s.eye(1)-C).det()*S.det())
yes('mutation deleting mixed self-energy detected',s.simplify((S-(E*s.eye(2)-A))[0,1])!=0)
# A finite closed avoided crossing, not a physical source-only decay model.
t,E0=s.symbols('t E0',real=True);h=s.symbols('h',positive=True,real=True)
Hr=s.Matrix([[E0,h],[h,E0]])
Gr=(E*s.eye(2)-Hr).inv()
z('resonant projected full resolvent',Gr[0,0]-(E-E0)/((E-E0)**2-h*h))
z('full determinant nonzero at bare eliminated pole',(E*s.eye(2)-Hr).det().subs(E,E0)+h*h)
z('full projected inverse zero at bare eliminated pole',Gr[0,0].subs(E,E0))
z('full off-diagonal inverse finite at bare pole',Gr[0,1].subs(E,E0)+1/h)
z('actual spectral polynomial',(E*s.eye(2)-Hr).det()-(E-E0-h)*(E-E0+h))
u=s.exp(-s.I*E0*t)*s.cos(h*t);v=-s.I*s.exp(-s.I*E0*t)*s.sin(h*t)
state=s.Matrix([u,v])
z('actual closed source/daughter ODE',s.I*state.diff(t)-Hr*state)
z('closed initial retained state',state.subs(t,0)-s.Matrix([1,0]))
z('norm exactly conserved',s.trigsimp((state.conjugate().T*state)[0])-1)
z('full interaction-inclusive energy conserved',s.trigsimp((state.conjugate().T*Hr*state)[0])-E0)
z('complete transfer probability at half cycle',s.simplify((v*s.conjugate(v)).subs(t,s.pi/(2*h)))-1)
z('complete source probability return',s.simplify((u*s.conjugate(u)).subs(t,s.pi/h))-1)
yes('mutation bare eliminated energy is not full spectral pole',((E*s.eye(2)-Hr).det().subs(E,E0)).is_negative)
gamma=s.symbols('gamma',positive=True,real=True)
yes('mutation inserted closed damping violates norm derivative',s.simplify(s.diff(s.exp(-gamma*t),t).subs(t,0)).is_negative)
out={'all_passed':all(x['passed'] for x in checks),'check_count':len(checks),'checks':checks,'scope':'Exact Hermitian block/resolvent and fully backreacted closed two-level diagnostic. Actual Q3 action blocks constructed independently; no physical local rate, UV or Markov completion.'}
(dest/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_passed':out['all_passed'],'check_count':len(checks)}));assert out['all_passed']
