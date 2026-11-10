"""DCN1 Part A (FROZEN_CRITERIA.md d603f1703c, section 1): the local analysis at a null of the field, exact (sympy).

A1  On any background of the law div[mu(u) grad Phi] = 4 pi G rho_b, mu = u/(1+u), u = |grad Phi|/a0, route L's rate
    Gamma_loc^2 = -4 pi G D.P u (2+u), 4 pi G D.P = div[grad Phi/(1+u)], equals (2+u)[u Phi_nn/(1+u) - 4 pi G rho_b].
A2  At a null inside baryons with the deep-law scaling, u Phi_nn is homogeneous of degree 0 (finite); slab and sphere limits.
A3  The stiffness term: omega^2 = G (1 + gamma F'' m k^2 - K m)/m; the adopted blend has F'' = 0 where Sigma = D.P < 0.
MUTATE M3: the identity with the 1/(1+u) dropped must fail.
Run: python3 -I dcn1_symbol.py  -> dcn1_symbol.json / .out.  TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, os, random, sys
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = {"lane": "DCN1", "part": "A", "criteria": "d603f1703c"}
lines = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); lines.append(s)

a0, s4 = sp.symbols("a0 s4", positive=True)          # s4 = 4 pi G rho_b
x, y, z = sp.symbols("x y z", real=True)

# ---------------------------------------------------------------- A1, step 1: the chain-rule expansions on random cubics
def check_cubic(seed, mutate=False):
    rnd = random.Random(seed)
    mons = [x**i * y**j * z**k for i in range(4) for j in range(4) for k in range(4) if 1 <= i + j + k <= 3]
    Phi = sum(sp.Rational(rnd.randint(-9, 9), rnd.randint(1, 5)) * m for m in mons)
    gx, gy, gz = [sp.diff(Phi, v) for v in (x, y, z)]
    w = sp.sqrt(gx**2 + gy**2 + gz**2)
    u = w / a0
    mu = u / (1 + u)
    rho4 = sum(sp.diff(mu * g, v) for g, v in ((gx, x), (gy, y), (gz, z)))          # 4 pi G rho_b, by the law
    DP4 = sum(sp.diff(g / (1 + u), v) for g, v in ((gx, x), (gy, y), (gz, z)))      # 4 pi G D.P
    Gam2 = -DP4 * u * (2 + u)
    H = sp.hessian(Phi, (x, y, z))
    gv = sp.Matrix([gx, gy, gz])
    Pnn = (gv.T * H * gv)[0] / w**2
    rhs = (2 + u) * (u * Pnn / (1 + u) - rho4) if not mutate else (2 + u) * (u * Pnn - rho4)
    worst = 0.0
    for _ in range(6):
        pt = {x: sp.Rational(rnd.randint(-20, 20), 7), y: sp.Rational(rnd.randint(-20, 20), 7),
              z: sp.Rational(rnd.randint(-20, 20), 7), a0: sp.Rational(rnd.randint(1, 30), 3)}
        L = sp.N(Gam2.subs(pt), 40); R_ = sp.N(rhs.subs(pt), 40)
        worst = max(worst, float(abs(L - R_) / max(abs(L), abs(R_), sp.Float(1e-30))))
    return worst

# ---------------------------------------------------------------- A1, step 2: the algebra in symbols
L_, q_, w_ = sp.symbols("L q w", positive=True)        # L = lap Phi, q = g.H.g, w = |g|
u_ = w_ / a0
mu_ = u_ / (1 + u_)
dmu = sp.diff(u_ / (1 + u_), w_) * a0                  # mu'(u)
rho4_s = mu_ * L_ + dmu * q_ / (a0 * w_)               # div(mu g) = mu L + mu'(u) grad u . g,  grad u . g = q/(a0 w)
DP4_s = L_ / (1 + u_) - q_ / (a0 * w_ * (1 + u_)**2)   # div(g/(1+u))
Gam2_s = -DP4_s * u_ * (2 + u_)
ident = (2 + u_) * (u_ * (q_ / w_**2) / (1 + u_) - rho4_s)
A1_alg = sp.simplify(Gam2_s - ident)
A1_mut = sp.simplify(Gam2_s - (2 + u_) * (u_ * (q_ / w_**2) - rho4_s))
cub = [check_cubic(sd) for sd in (1, 2, 3)]
cub_m = [check_cubic(sd, mutate=True) for sd in (1, 2, 3)]
OUT["A1"] = dict(algebra_difference=str(A1_alg), random_cubic_max_rel=max(cub), PASS=bool(A1_alg == 0 and max(cub) < 1e-10))
OUT["M3_identity_mutated"] = dict(algebra_difference_is_zero=bool(A1_mut == 0), random_cubic_max_rel=max(cub_m),
                                  bites=bool(A1_mut != 0 and max(cub_m) > 1e-6))
P("A1 identity Gamma_loc^2 = (2+u)[u Phi_nn/(1+u) - 4 pi G rho_b]: algebra difference", A1_alg,
  "; random cubics max rel", f"{max(cub):.2e}", "->", "PASS" if OUT["A1"]["PASS"] else "FAIL")
P("M3 (1/(1+u) dropped): algebra difference zero?", A1_mut == 0, "; cubic max rel", f"{max(cub_m):.2e}",
  "->", "BITES" if OUT["M3_identity_mutated"]["bites"] else "DOES NOT BITE")

# ---------------------------------------------------------------- A2: the null
s = sp.symbols("s", positive=True)
# slab: mu(g/a0) g = s4 z  ->  g = (s4 z + sqrt(s4^2 z^2 + 4 a0 s4 z))/2
gs = (s4 * s + sp.sqrt(s4**2 * s**2 + 4 * a0 * s4 * s)) / 2
assert sp.simplify((gs / a0) / (1 + gs / a0) * gs - s4 * s) == 0
us = gs / a0
DP4_slab = sp.diff(gs / (1 + us), s)
Gam2_slab = sp.simplify(-DP4_slab * us * (2 + us))
lim_slab = sp.limit(Gam2_slab / s4, s, 0, "+")
DP_scal_slab = sp.limit(DP4_slab * sp.sqrt(s), s, 0, "+")
id_slab = sp.simplify(Gam2_slab - (2 + us) * (us * sp.diff(gs, s) / (1 + us) - s4))
# uniform sphere: g_N = s4 r/3
gN = s4 * s / 3
gsp = (gN + sp.sqrt(gN**2 + 4 * a0 * gN)) / 2
usp = gsp / a0
DP4_sph = sp.diff(s**2 * gsp / (1 + usp), s) / s**2
Gam2_sph = sp.simplify(-DP4_sph * usp * (2 + usp))
lim_sph = sp.limit(Gam2_sph / s4, s, 0, "+")
DP_scal_sph = sp.limit(DP4_sph * sp.sqrt(s), s, 0, "+")
id_sph = sp.simplify(Gam2_sph - (2 + usp) * (usp * sp.diff(gsp, s) / (1 + usp) - s4))
# sup over s of the closed forms (both negative everywhere?)
neg_slab = all(float(Gam2_slab.subs({s4: 1, a0: 1, s: v})) < 0 for v in (1e-8, 1e-4, 1e-2, 0.1, 1, 10, 1e3))
neg_sph = all(float(Gam2_sph.subs({s4: 1, a0: 1, s: v})) < 0 for v in (1e-8, 1e-4, 1e-2, 0.1, 1, 10, 1e3))
# general deep-law blow-up: Phi = r^(3/2) f(theta) (axisymmetric); u Phi_nn is homogeneous of degree 0 in r
r, th, lam = sp.symbols("r theta lambda", positive=True)
f = sp.Function("f")
Phi_b = r**sp.Rational(3, 2) * f(th)
gr = sp.diff(Phi_b, r); gt = sp.diff(Phi_b, th) / r
w2 = gr**2 + gt**2
# grad(w2) . g  /(2 a0 w) * ... : u Phi_nn = g.grad(w2)/(2 a0 w)... with u = w/a0: u Phi_nn = (g.grad(w2))/(2 a0 w) * (w/w) -> q/(a0 w)
q_b = (gr * sp.diff(w2, r) + gt * sp.diff(w2, th) / r) / 2
uPnn = q_b / (a0 * sp.sqrt(w2))
deg0 = sp.simplify(uPnn.subs(r, lam * r) / uPnn)
DPdeep = None
OUT["A2"] = dict(slab_limit_over_4piGrho=str(lim_slab), sphere_limit_over_4piGrho=str(lim_sph),
                 slab_DP_times_sqrt_s_limit=str(DP_scal_slab), sphere_DP_times_sqrt_s_limit=str(DP_scal_sph),
                 slab_identity_difference=str(id_slab), sphere_identity_difference=str(id_sph),
                 slab_negative_everywhere=neg_slab, sphere_negative_everywhere=neg_sph,
                 blowup_uPnn_scale_ratio=str(deg0),
                 PASS=bool(lim_slab == -1 and lim_sph == sp.Rational(-5, 3) and id_slab == 0 and id_sph == 0 and deg0 == 1))
P("A2 slab: Gamma^2/(4 pi G rho) -> ", lim_slab, "; D.P sqrt(s) ->", DP_scal_slab, "(D.P ~ s^-1/2); identity diff", id_slab,
  "; negative at every s:", neg_slab)
P("A2 sphere: Gamma^2/(4 pi G rho) ->", lim_sph, "; D.P sqrt(s) ->", DP_scal_sph, "; identity diff", id_sph,
  "; negative at every s:", neg_sph)
P("A2 blow-up Phi = r^(3/2) f(theta): u Phi_nn(lambda r)/u Phi_nn(r) =", deg0, "(degree 0: finite, direction-dependent at the null)")
P("A2 ->", "PASS" if OUT["A2"]["PASS"] else "FAIL")

# ---------------------------------------------------------------- A3: stiffness and blend
Gc, K, m, gam, Fpp, k2 = sp.symbols("G K m gamma Fpp k2", real=True)
om2 = Gc * (1 + gam * Fpp * m * k2 - K * m) / m
lim_off = sp.limit(om2.subs(Fpp, 0), k2, sp.oo)
lim_on = sp.limit(om2.subs({Fpp: 1, Gc: 1, gam: 1, m: sp.Rational(1, 2), K: 1}), k2, sp.oo)
# the blend: f'' = A q^4 on (0, tau] (pure Pi^6 near 0), f = 0 for q <= 0 (equals the raw switch there)
qv, Ab = sp.symbols("q A", real=True)
f_left = sp.Integer(0)
f_right = Ab * qv**6 / 30                       # integrates f'' = A q^4 twice, f(0) = f'(0) = 0
cont = [sp.simplify(sp.diff(f_right, qv, j).subs(qv, 0) - sp.diff(f_left, qv, j)) == 0 for j in range(0, 5)]
OUT["A3"] = dict(limit_k_inf_Fpp0=str(lim_off), limit_k_inf_stiff_Gpos=str(lim_on),
                 blend_zero_with_four_derivatives_at_0=all(cont),
                 note="F'' = 0 on Sigma = D.P < 0 (blend = raw switch there; decision 71e4014cd5); the rate at D.P < 0 is the gamma_L = 0 one",
                 PASS=bool(sp.simplify(lim_off - Gc * (1 - K * m) / m) == 0 and lim_on == sp.oo and all(cont)))
P("A3 k->inf, D.P < 0 (F''=0):", lim_off, "(bounded in k); D.P > 0 with stiffness:", lim_on,
  "; blend C4 onto 0 at Sigma = 0:", all(cont), "->", "PASS" if OUT["A3"]["PASS"] else "FAIL")

OUT["PART_A_PASS"] = bool(OUT["A1"]["PASS"] and OUT["A2"]["PASS"] and OUT["A3"]["PASS"])
P("PART A:", "PASS" if OUT["PART_A_PASS"] else "FAIL")
OUT["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
json.dump(OUT, open(os.path.join(HERE, "dcn1_symbol.json"), "w"), indent=1)
open(os.path.join(HERE, "dcn1_symbol.out"), "w").write("\n".join(lines) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
