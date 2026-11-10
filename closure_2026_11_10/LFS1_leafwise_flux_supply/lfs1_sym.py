"""LFS1 symbolic part (criteria 8ddf81950c): S1 (a)-(e), KA1, KA2, KA3.

Notation as QX17 (closure_2026_11_06/QX17_covariant_field_equations/RESULT.md), unitary gauge: lapse N, shift N^i,
s = sqrt(gamma), P^i (P^0 = 0), Pi = Pi_+ on the positive branch (on Pi < 0 every gamma_L term is zero: set gL = 0),
X = N (1 + gL Pi), Y^i = s P^i, d = mu^2 (1/N - 1)/K.

MUTATE MU1 (env LFS1_MUTATE=MU1): flip the sign of lambda in the khronon equation (QX17's own mutation).
Writes lfs1_sym.json / lfs1_sym.out (or *_MUTATE_MU1.*). Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys
import sympy as sp

MUT = os.environ.get("LFS1_MUTATE", "")
SGN = -1 if MUT == "MU1" else 1
tag = "_MUTATE_MU1" if MUT == "MU1" else ""
here = os.path.dirname(os.path.abspath(__file__))
out_lines = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); out_lines.append(s)

res = {}
t, x1, x2, x3 = sp.symbols("t x1 x2 x3", real=True)
xs = (x1, x2, x3)
gL, K, mu = sp.symbols("gamma_L K mu", positive=True)
args = (t, x1, x2, x3)
N = sp.Function("N")(*args)
s = sp.Function("s")(*args)
Pi = sp.Function("Pi")(*args)
P = [sp.Function(f"P{i}")(*args) for i in range(3)]
Sh = [sp.Function(f"S{i}")(*args) for i in range(3)]   # shift N^i
X = N * (1 + gL * Pi)
Y = [s * P[i] for i in range(3)]
d = mu**2 * (1 / N - 1) / K

def Ddiv(V):   # leaf divergence D_i V^i = (1/s) d_i (s V^i)
    return sum(sp.diff(s * V[i], xs[i]) for i in range(3)) / s

V = [(1 + gL * Pi) * P[i] for i in range(3)]
A = [sp.diff(sp.log(N), xs[i]) for i in range(3)]
rhoQ = N * (Ddiv(V) + sum(V[i] * A[i] for i in range(3))) + d          # QX17 E3, unitary gauge

def ndot(f):   # n^m d_m f = (1/N)(d_t - N^i d_i) f
    return (sp.diff(f, t) - sum(Sh[i] * sp.diff(f, xs[i]) for i in range(3))) / N

lam = (1 + gL * Pi) * ndot(sp.log(N)) + gL * ndot(Pi)                 # QX17 E2 normal part

# S1(a)
r_a = sp.simplify(s * rhoQ - (sum(sp.diff(X * Y[i], xs[i]) for i in range(3)) + s * d))
# S1(b)
r_b = sp.simplify(lam * N**2 - (sp.diff(X, t) - sum(Sh[j] * sp.diff(X, xs[j]) for j in range(3))))
# S1(c): khronon equation vs the divergence form (mu kept: its terms carried separately)
E3 = sp.diff(s * rhoQ, t) - sum(sp.diff(s * (Sh[i] * rhoQ + SGN * lam * N**2 * P[i]), xs[i]) for i in range(3))
divY = sum(sp.diff(X * Y[j], xs[j]) for j in range(3))
form = sum(sp.diff(X * sp.diff(Y[i], t) + sum(Sh[j] * sp.diff(X, xs[j]) for j in range(3)) * Y[i] - Sh[i] * divY, xs[i])
           for i in range(3))
form += sp.diff(s * d, t) - sum(sp.diff(s * Sh[i] * d, xs[i]) for i in range(3))
r_c = sp.simplify(sp.expand(E3 - form))
say("S1(a) s rho_Q - [d_i(X Y^i) + s d]          residual:", r_a)
say("S1(b) lambda N^2 - (d_t - N^j d_j) X          residual:", r_b)
say("S1(c) khronon eq. - divergence form (3D, shift, mu) residual:", "0" if r_c == 0 else "NON-ZERO (%d ops)" % sp.count_ops(r_c))
res["S1a"] = str(r_a); res["S1b"] = str(r_b); res["S1c_zero"] = bool(r_c == 0)

# S1(d), (e): spherical. Radial coordinate r; s = r^2 h(r,t) (sin theta dropped: an overall constant per ray).
r = sp.symbols("r", positive=True)
Nr = sp.Function("N")(t, r); h = sp.Function("h")(t, r); Pir = sp.Function("Pi")(t, r)
Pr = sp.Function("P")(t, r); Ur = sp.Function("U")(t, r)       # U = shift N^r
sr = r**2 * h
Xr = Nr * (1 + gL * Pir); Yr = sr * Pr
dr = mu**2 * (1 / Nr - 1) / K
Dcum = sp.Function("Dc")(t, r)   # Dc' = s d  (enclosed dust part)
rho_s = sp.diff(Xr * Yr, r) + sr * dr                          # = s rho_Q  (S1(a) radial)
lam_r = ((1 + gL * Pir) * (sp.diff(sp.log(Nr), t) - Ur * sp.diff(sp.log(Nr), r))
         + gL * (sp.diff(Pir, t) - Ur * sp.diff(Pir, r))) / Nr
E3r = sp.diff(rho_s, t) - sp.diff(Ur * rho_s + SGN * sr * lam_r * Nr**2 * Pr, r)
# integrated from 0 to r (regular centre: every flux vanishes at r = 0), with Dc' = s d:
E3int = sp.diff(Xr * Yr + Dcum, t) - (Ur * (sp.diff(Xr * Yr, r) + sr * dr) + SGN * sr * lam_r * Nr**2 * Pr)
chk_int = sp.simplify(sp.diff(E3int, r) - E3r.subs(sp.diff(Dcum, r), sr * dr)
                      - (sp.diff(sp.diff(Dcum, t), r) - sp.diff(sr * dr, t)))
# zero shift, mu = 0: integrated equation is X d_t Y = 0
z0 = sp.simplify(E3int.subs({Ur: 0, mu: 0, Dcum: 0}))
z0_ratio = sp.simplify(z0 - Xr * sp.diff(Yr, t))
# with shift, mu = 0: X (d_t Y - U d_r Y) = 0
zs = sp.simplify(E3int.subs({mu: 0, Dcum: 0}))
zs_ratio = sp.simplify(zs - Xr * (sp.diff(Yr, t) - Ur * sp.diff(Yr, r)))
# (e) with mu: along the clock flow dR/dt = -U, enclosed total charge Qt = X Y + Dc changes by Y dX/dt|flow
Qt = Xr * Yr + Dcum
dQ_flow = sp.diff(Qt, t) - Ur * sp.diff(Qt, r)
e_res = sp.simplify((dQ_flow - E3int).subs(sp.diff(Dcum, r), sr * dr)
                    - Yr * (sp.diff(Xr, t) - Ur * sp.diff(Xr, r)))
say("S1(d) integrated radial form consistent with E3 (d/dr) residual:", chk_int)
say("S1(d) zero shift, mu 0: [integrated E3] - X d_t Y   residual:", z0_ratio)
say("S1(d) shift,      mu 0: [integrated E3] - X (d_t Y - N^r d_r Y) residual:", zs_ratio)
say("S1(e) with mu: dQ_tot/dt|flow - [integrated E3] - Y dX/dt|flow residual:", e_res)
res["S1d_consistency"] = str(chk_int); res["S1d_zero_shift"] = str(z0_ratio)
res["S1d_shift"] = str(zs_ratio); res["S1e"] = str(e_res)

# ---------------- known answers ----------------
G, M, a0, rr = sp.symbols("G M a0 r", positive=True)
# KA1: deep law. g = sqrt(G M a0)/r; phantom M_ph = r sqrt(G M a0)/G - M; rho_ph = dM_ph/dr /(4 pi r^2)
g = sp.sqrt(G * M * a0) / rr
Kk = 4 * sp.pi * G
rho_ph = sp.diff(rr * sp.sqrt(G * M * a0) / G - M, rr) / (4 * sp.pi * rr**2)
p_iso = g**2 / (2 * Kk)
sig2 = sp.simplify(p_iso / rho_ph)
ka1 = sp.simplify(sig2 - sp.sqrt(G * M * a0) / 2)
# hydrostatic check: dp/dr = -rho g
hyd = sp.simplify(sp.diff(p_iso, rr) + rho_ph * g)
say("KA1 sigma^2 - (1/2) sqrt(G M a0) residual:", ka1, "; hydrostatic dp/dr + rho g residual:", hyd)
res["KA1"] = bool(ka1 == 0 and hyd == 0)
# KA2: law S, K P = (1 - mu) g, mu = x/(1+x), x = g/a0
gg, gN = sp.symbols("g g_N", positive=True)
gN_lawS = gg**2 / (gg + a0)                 # from g^2 = g_N (g + a0)
P_r = (1 - (gg / a0) / (1 + gg / a0)) * gg / Kk
ka2 = sp.simplify(4 * sp.pi * rr**2 * P_r - rr**2 * (gg - gN_lawS) / G)
ka2b = sp.simplify(rr**2 * (gg - gN_lawS) / G - rr**2 * gg * a0 / (G * (gg + a0)))
say("KA2 4 pi R^2 P_r - M_b (nu - 1) residual:", ka2, "; closed form residual:", ka2b)
res["KA2"] = bool(ka2 == 0 and ka2b == 0)

# KA3 (a): covariant current -> unitary gauge (1+1 is enough for the identity; shift kept)
Nf = sp.Function("N")(t, r); sf = sp.Function("s")(t, r); rhof = sp.Function("rho")(t, r)
lamf = sp.Function("lam")(t, r); Pf = sp.Function("P")(t, r); Uf = sp.Function("U")(t, r)
sqrtg = Nf * sf
J0 = rhof / Nf                         # n^0 rho, n^0 = 1/N
Jr = -Uf * rhof / Nf - SGN * lamf * Nf * Pf   # n^r rho - lambda P^r / Q, Q = 1/N
cov = sp.diff(sqrtg * J0, t) + sp.diff(sqrtg * Jr, r)
uni = sp.diff(sf * rhof, t) - sp.diff(sf * (Uf * rhof + lamf * Nf**2 * Pf), r)
ka3a = sp.simplify(cov - uni)
say("KA3(a) covariant current vs QX17 unitary-gauge E3 residual:", ka3a)
# KA3 (b): project E2 on n with an explicit ADM metric in (t, r): n_m = (-N, 0), n^m = (1/N, -U/N)
Phat_r = sp.Function("Phr")(t, r)       # Phat^m = (0, Phat^r) (n.Phat = 0 since n_r = 0... with P^0 = 0)
gam = sp.Function("gam")(t, r)          # gamma_rr
ginv = sp.Matrix([[-1 / Nf**2, Uf / Nf**2], [Uf / Nf**2, 1 / gam - Uf**2 / Nf**2]])
coords = (t, r)
lN = -sp.log(Nf)                        # l = ln Q
Pif = sp.Function("Pi")(t, r); KW = sp.Function("KW")(t, r)
grad = lambda f: [sp.diff(f, c) for c in coords]
up = lambda v: [sum(ginv[a, b] * v[b] for b in range(2)) for a in range(2)]
n_low = [-Nf, 0]; n_up = [1 / Nf, -Uf / Nf]
dl_up = up(grad(lN)); dPi_up = up(grad(Pif))
Phat_up = [0, Phat_r]
E2 = [-dl_up[a] - KW * Phat_up[a] + gL * (dPi_up[a] - Pif * dl_up[a]) + lamf * n_up[a] for a in range(2)]
proj = sp.simplify(sum(n_low[a] * E2[a] for a in range(2)))
lam_E2 = sp.solve(sp.Eq(proj, 0), lamf)[0]
lam_QX = (1 + gL * Pif) * (sp.diff(sp.log(Nf), t) - Uf * sp.diff(sp.log(Nf), r)) / Nf \
         + gL * (sp.diff(Pif, t) - Uf * sp.diff(Pif, r)) / Nf
ka3b = sp.simplify(lam_E2 - lam_QX)
say("KA3(b) lambda from n.E2 - QX17 normal formula residual:", ka3b)
# KA3 (c): T^P_{0i} at gamma_L = 0, zero shift: g_0i = 0, n_i = 0, P_0 = 0
# T^P_0i = g_0i (P.A) + [P_0 d_i l + P_i d_0 l] + (div P) n_0 n_i - lambda (n_0 P_i + n_i P_0)
Pi_low = sp.Function("Pl")(t, r)
lam0 = sp.diff(sp.log(Nf), t) / Nf                      # zero shift, gamma_L = 0
T0i = 0 + (0 + Pi_low * sp.diff(-sp.log(Nf), t)) + 0 - SGN * lam0 * (-Nf * Pi_low + 0)
ka3c = sp.simplify(T0i)
say("KA3(c) T^P_{0i} (zero shift, gamma_L 0, lambda from E2) residual:", ka3c)
res["KA3"] = bool(ka3a == 0 and ka3b == 0 and ka3c == 0)
res["KA3_parts"] = [str(ka3a), str(ka3b), str(ka3c)]

res["S1_pass"] = bool(r_a == 0 and r_b == 0 and r_c == 0 and chk_int == 0 and z0_ratio == 0
                      and zs_ratio == 0 and e_res == 0)
res["mutate"] = MUT
say("S1 all residuals zero:", res["S1_pass"], "| KA1", res["KA1"], "KA2", res["KA2"], "KA3", res["KA3"])
say("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
json.dump(res, open(os.path.join(here, f"lfs1_sym{tag}.json"), "w"), indent=1)
open(os.path.join(here, f"lfs1_sym{tag}.out"), "w").write("\n".join(out_lines) + "\n")

# Adopts nothing. kappa = 1/2 FITTED; not theory closed.
