#!/usr/bin/env python3
"""AUDIT 4: WHY does the graviton enter as cos(qx) (mass) not q sin(qx) (gradient)?
The real all-n mechanism (NOT the hardcoded ansatz). Inspect which Christoffels carry
d_x h vs d_t h, and which contract into u^a D_a on the frame legs.
u^a = (u0, 0, u^y, 0): only TIME (a=0) and Y (a=2) directions are nonzero.
u.grad = u0 d_t + u^y d_y. There is NO u^x, so u.grad NEVER differentiates along x directly.
The graviton d_x h can only enter via a Gamma^l_{a m} with a in {0,y} (contracted by u^a).
Print all Gamma that carry d_x h (i.e. sin(qx)) and see if any is picked by u^a (a=0 or a=2)."""
import sympy as sp, functools
print=functools.partial(print,flush=True)
t,x,y,z=sp.symbols('t x y z',real=True)
H=sp.symbols('H',positive=True)
q1,p=sp.symbols('q1 p',real=True)
e1,ep=sp.symbols('e1 ep',real=True)
crd=[t,x,y,z]
A1=sp.Function('A1')(t);V=sp.Function('V')(t)
# single graviton for clarity
def trunc(expr):
    for s in (e1,ep):
        expr=sp.series(expr,s,0,3).removeO()
    return sp.expand(expr)
a=sp.exp(H*t)
h=e1*A1*sp.cos(q1*x)
g=sp.diag(-1,a**2,a**2*(1+h),a**2*(1-h))
gi=g.inv()
n=4
G=[[[sp.Integer(0)]*n for _ in range(n)] for _ in range(n)]
for l in range(n):
    for m in range(n):
        for nu in range(n):
            G[l][m][nu]=trunc(sum(gi[l,s]*(sp.diff(g[s,m],crd[nu])+sp.diff(g[s,nu],crd[m])-sp.diff(g[m,nu],crd[s])) for s in range(n))/2)
nm=['t','x','y','z']
print("=== Christoffels carrying the graviton SPATIAL gradient d_x h ~ sin(q1 x) ===")
for l in range(n):
    for m in range(n):
        for nu in range(n):
            gg=G[l][m][nu]
            if gg!=0 and gg.has(sp.sin(q1*x)):
                print(f"  Gamma^{nm[l]}_{{{nm[m]}{nm[nu]}}} carries sin(qx): {sp.expand(gg)}")
print("\n=== Now: u.grad = u^a d_a with u^a nonzero ONLY for a=t (a=0) and a=y (a=2) ===")
print("A graviton d_x gradient reaches the frame leg ONLY through Gamma^l_{a m} with a in {t,y}")
print("(the LOWER index a contracted by u^a). List Gamma^l_{a m} with a in {t,y} that carry sin(qx):")
found=[]
for l in range(n):
    for m in range(n):
        for a in (0,2):  # only u^t and u^y are nonzero
            gg=G[l][a][m]
            if gg!=0 and gg.has(sp.sin(q1*x)):
                found.append((nm[l],nm[a],nm[m],gg))
                print(f"  a={nm[a]}: Gamma^{nm[l]}_{{{nm[a]}{nm[m]}}} = {sp.expand(gg)}")
if not found:
    print("  >>> NONE. No Gamma^l_{a m} with a in {t,y} carries the graviton's d_x gradient.")
    print("  >>> Therefore u^a Gamma cannot inject q sin(qx) onto the frame via the a-slot.")
print("\n=== But the graviton d_x can ALSO enter via the OTHER Gamma index (m or nu = x) ===")
print("i.e. when the frame vector index m being differentiated is x, OR via d_a of h in the")
print("connection where a=x. But a=x slot is contracted by u^x=0. Check: does any surviving")
print("term in Dop on the frame vector produce sin(qx)?  Build Dop once and inspect.")
def Dop(w,u_up):
    out=[]
    for m in range(n):
        e=0
        for al in range(n):
            e+=u_up[al]*(sp.diff(w[m],crd[al])-sum(G[l][al][m]*w[l] for l in range(n)))
        out.append(trunc(e))
    return sp.Matrix(out)
uy=ep*V*sp.cos(p*x)
u0=sp.symbols('u0d')
sol=sp.solve(sp.Eq(g[0,0]*u0**2+g[2,2]*uy**2,-1),u0)
pick=[s for s in sol if sp.simplify(s.subs({e1:0,ep:0})-1)==0]
u0v=trunc(pick[0])
u_up=sp.Matrix([u0v,0,uy,0])
u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
D1=Dop(u_low,u_up)
D2=Dop(D1,u_up)
print("  (D u)_mu has sin(qx)? ", [D1[m].has(sp.sin(q1*x)) for m in range(4)])
print("  (D^2 u)_mu has sin(qx)? ", [D2[m].has(sp.sin(q1*x)) for m in range(4)])
B1=trunc(sum(u_up[m]*D2[m] for m in range(4)))
print("  B_1 = u.D^2 u has sin(qx)?", B1.has(sp.sin(q1*x)), " has explicit q1 poly?", strip:=None)
