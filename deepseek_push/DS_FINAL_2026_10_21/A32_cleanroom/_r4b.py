import sympy as sp

t, x, y, z, eps = sp.symbols('t x y z epsilon', real=True)
cs = [x, y, z]
N = sp.Function('N')(x, y, z)          # static lapse, arbitrary

# flat static background h0 = I ; general trace-free perturbation s_ij(t,x^i)
s11, s22, s12, s13, s23 = [sp.Function(n)(t, x, y, z) for n in ('s11', 's22', 's12', 's13', 's23')]
s = sp.Matrix([[s11, s12, s13], [s12, s22, s23], [s13, s23, -(s11 + s22)]])

h = sp.eye(3) + eps*s

def christoffel(g, inv, cs):
    n = len(cs)
    G = [[[sp.S.Zero]*n for _ in range(n)] for _ in range(n)]
    for u in range(n):
        for i in range(n):
            for j in range(n):
                sm = sp.S.Zero
                for l in range(n):
                    sm += inv[u, l]*(sp.diff(g[i, l], cs[j]) + sp.diff(g[j, l], cs[i]) - sp.diff(g[i, j], cs[l]))
                G[u][i][j] = sp.expand(sm/2)
    return G

inv = h.inv()
G = christoffel(h, inv, cs)
K = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        K[i, j] = sp.diff(h[i, j], t)/(2*N)          # zero shift
theta = sp.expand(sum(inv[i, j]*K[i, j] for i in range(3) for j in range(3)))
th1 = sp.simplify(sp.diff(theta, eps).subs(eps, 0))
print("theta^(0) =", sp.simplify(theta.subs(eps, 0)))
print("theta^(1) =", th1)
print("PASS theta^(1)==0 :", th1 == 0)

# cross-check via Jacobi identity theta = d_t ln det(h) / (2N)
theta_J = sp.simplify(sp.diff(sp.log(sp.det(h)), t)/(2*N))
print("Jacobi check theta == d_t ln det h/(2N):", sp.simplify(theta - theta_J) == 0)

# a perturbation WITH a trace must give nonzero theta^(1) (contrast)
tr = sp.Function('tr')(t, x, y, z)
h2 = (1 + eps*tr)*sp.eye(3) + eps*s
inv2 = h2.inv()
K2 = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        K2[i, j] = sp.diff(h2[i, j], t)/(2*N)
th2 = sp.expand(sum(inv2[i, j]*K2[i, j] for i in range(3) for j in range(3)))
print("\ntheta^(1) with trace:", sp.simplify(sp.diff(th2, eps).subs(eps, 0)))
