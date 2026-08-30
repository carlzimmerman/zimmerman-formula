"""Adversarial check of the minisuperspace-miss worry for the extended-BIMOND BD signal.
I test the ONE robust link: is the LAPSE-VELOCITY-SQUARED (Hessian) term a genuine, background-INDEPENDENT
signal, or an artifact of a particular FRW slice? And what is the true CONSTANT-COEFFICIENT healthy locus?"""
import sympy as sp

t = sp.Symbol('t')
Ng, Nf, ag, af = (sp.Function('N_g')(t), sp.Function('N_f')(t), sp.Function('a_g')(t), sp.Function('a_f')(t))
X = [t, sp.Symbol('x'), sp.Symbol('y'), sp.Symbol('z')]
def metric(N,a): return sp.diag(-N**2, a**2, a**2, a**2)
g  = metric(Ng,ag);  gi  = g.inv()
gh = metric(Nf,af);  ghi = gh.inv()
def christoffel(gm, gmi):
    G=[[[sp.Integer(0)]*4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                s=sp.Integer(0)
                for si in range(4):
                    s+= gmi[l,si]*(sp.diff(gm[si,m],X[n])+sp.diff(gm[si,n],X[m])-sp.diff(gm[m,n],X[si]))
                G[l][m][n]=s/2
    return G
Gg  = christoffel(g,gi); Gf  = christoffel(gh,ghi)
C   = [[[sp.simplify(Gg[l][m][n]-Gf[l][m][n]) for n in range(4)] for m in range(4)] for l in range(4)]

def T_full():
    s=sp.Integer(0)
    for a in range(4):
     for b in range(4):
      for m in range(4):
       for n in range(4):
        for r in range(4):
         for sig in range(4):
          s+= C[a][m][n]*C[b][r][sig]*g[a,b]*gi[m,r]*gi[n,sig]
    return s
def P(a): return sum(gi[m,n]*C[a][m][n] for m in range(4) for n in range(4))
def T_Ptrace(): return sum(g[a,b]*P(a)*P(b) for a in range(4) for b in range(4))
def V(mu): return sum(C[a][a][mu] for a in range(4))
def T_Vtrace(): return sum(gi[m,n]*V(m)*V(n) for m in range(4) for n in range(4))
def T_ricci():
    s=sp.Integer(0)
    for m in range(4):
     for n in range(4):
      for a in range(4):
       for b in range(4):
        s+= gi[m,n]*C[a][m][b]*C[b][n][a]
    return s
T1,T2,T3,T4 = sp.expand(T_full()), sp.expand(T_Ptrace()), sp.expand(T_Vtrace()), sp.expand(T_ricci())

dNg,dNf = sp.symbols('dNg dNf', real=True)
subsV = {sp.Derivative(Ng,t):dNg, sp.Derivative(Nf,t):dNf}
c1,c2,c3,c4 = sp.symbols('c1 c2 c3 c4', real=True)
Mlin = (c1*T1+c2*T2+c3*T3+c4*T4).subs(subsV)
Mlin = sp.expand(Mlin)

print("=== (A) Coefficient of the LAPSE KINETIC term dNg^2 (the Hessian-decisive piece) ===")
cff2 = sp.simplify(Mlin.coeff(dNg,2))
print("   coeff(dNg^2) =", cff2)
print("   -> vanishes IFF:", sp.simplify(cff2*Ng**4))
# is it background (a_g,a_f,N_f)-independent?
print("   depends on a_g,a_f,N_f? ->", cff2.has(ag) or cff2.has(af) or cff2.has(Nf))

print("\n=== (B) cross term dNg*dNf and dNf^2 ===")
print("   coeff(dNg*dNf) =", sp.simplify(Mlin.coeff(dNg,1).coeff(dNf,1)))
print("   coeff(dNf^2)   =", sp.simplify(Mlin.coeff(dNf,2)))

print("\n=== (C) TRUE constant-coefficient lapse-velocity-FREE locus ===")
# Require: no dNg^2, no dNf^2, no dNg*dNf, AND no linear dNg, dNf terms -- with CONSTANT c_i.
# Collect the full polynomial in (dNg,dNf); every coefficient (a field expression) must vanish as identity.
poly = sp.Poly(Mlin, dNg, dNf)
conds = set()
for monom, coef in poly.terms():
    if monom == (0,0):   # the dNg^0 dNf^0 piece is the velocity-free part; keep it
        continue
    # coef is a field expression linear in c1..c4; split into independent field-structures
    ce = sp.expand(coef)
    # gather coefficients of c1..c4 and of the field monomials
    for ci in (c1,c2,c3,c4):
        part = ce.coeff(ci)
        # part is a pure field expression; its vanishing patterns give conditions.
    conds.add(sp.simplify(ce))
# Instead of the messy split, directly require Mlin - (velocity-free part) == 0 as identity in dNg,dNf and fields.
vfree = poly.coeff_monomial((0,0))
remainder = sp.expand(Mlin - vfree)  # all velocity-carrying terms
# treat field functions and their derivatives as independent atoms and require remainder==0 => conditions on c_i
atoms = remainder.atoms(sp.Function, sp.Derivative)
# Build a linear system: remainder must be identically zero as a function of dNg,dNf and all field atoms.
# Extract coefficients by pattern: collect w.r.t. dNg,dNf and w.r.t. distinct field-monomials.
remainder = sp.expand(remainder)
# get all monomials in the "variables" = dNg,dNf,Ng,Nf,ag,af, dag=Derivative(ag), daf=Derivative(af)
dag, daf = sp.Derivative(ag,t), sp.Derivative(af,t)
syms = [dNg,dNf,Ng,Nf,ag,af,dag,daf]
p2 = sp.Poly(remainder, *syms)
lin_conds = [sp.Eq(coef,0) for coef in p2.coeffs()]  # each field-monomial coefficient (in c_i) must be 0
sol = sp.solve(lin_conds, [c1,c2,c3,c4], dict=True)
print("   constant-coefficient healthy locus (all velocity terms killed):", sol)
