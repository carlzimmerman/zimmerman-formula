import sympy as sp

t, x, y, z, eps = sp.symbols('t x y z epsilon', real=True)
cs = [x, y, z]

# static background: N = N(x^i) arbitrary, h_ij static, zero shift
N = sp.Function('N')(x, y, z)

# background spatial metric (arbitrary static), perturbed by a TRACE-FREE s_ij
A = sp.Function('A')(x, y, z)
B = sp.Function('B')(x, y, z)
C = sp.Function('C')(x, y, z)
h0 = sp.Matrix([[A, 0, 0], [0, B, 0], [0, 0, C]])
s = sp.Matrix([[sp.Function('s11')(t, x, y, z), sp.Function('s12')(t, x, y, z), sp.Function('s13')(t, x, y, z)],
               [sp.Function('s12')(t, x, y, z), sp.Function('s22')(t, x, y, z), sp.Function('s23')(t, x, y, z)],
               [sp.Function('s13')(t, x, y, z), sp.Function('s23')(t, x, y, z), sp.Function('s33')(t, x, y, z)]])
# impose trace-free: s33 = -(A s11 + B s22)/C  (s^i_i = A^-1 s11 + B^-1 s22 + C^-1 s33 = 0)
s33 = -(A*sp.Function('s11')(t, x, y, z) + B*sp.Function('s22')(t, x, y, z))/C
s = s.subs(sp.Function('s33')(t, x, y, z), s33)

h = h0 + eps*s

def christoffel(g, inv, cs):
    n = len(cs)
    G = [[[sp.S.Zero]*n for _ in range(n)] for _ in range(n)]
    for u in range(n):
        for i in range(n):
            for j in range(n):
                sm = sp.S.Zero
                for l in range(n):
                    sm += inv[u, l]*(sp.diff(g[i, l], cs[j]) + sp.diff(g[j, l], cs[i]) - sp.diff(g[i, j], cs[l]))
                G[u][i][j] = sm/2
    return G

def Kij_of(h):
    inv = h.inv()
    G = christoffel(h, inv, cs)
    K = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            K[i, j] = sp.diff(h[i, j], t)  # shift = 0
            for l in range(3):
                K[i, j] -= 2*0  # zero shift
            K[i, j] = K[i, j]/(2*N)
    return K, inv

K, hinv = Kij_of(h)
theta = sp.simplify(sum(hinv[i, j]*K[i, j] for i in range(3) for j in range(3)))
th0 = sp.simplify(theta.subs(eps, 0))
th1 = sp.simplify(sp.diff(theta, eps).subs(eps, 0))
print("theta^(0) (static background) =", th0)
print("theta^(1) (trace-free perturbation) =", th1)

# contrast: give the perturbation a trace
h2 = h0 + eps*(s + sp.Function('tr')(t, x, y, z)*h0)
K2, hinv2 = Kij_of(h2)
th2 = sp.simplify(sum(hinv2[i, j]*K2[i, j] for i in range(3) for j in range(3)))
print("\nwith a trace part: theta^(1) =", sp.simplify(sp.diff(th2, eps).subs(eps, 0)), "  (nonzero -> contrast)")
