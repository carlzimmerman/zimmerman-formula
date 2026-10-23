#!/usr/bin/env python3
"""H3_jeans_control: hostile test of H1's T1 reading (C5's negative-energy omega = 0 mode of AeST + gamma_L + capped F
is the dust's Jeans growth mode, not a ghost).  Criteria: FROZEN_CRITERIA.md (committed first, 04355110c4).

Read-only reuse: C5's quad_matrix / jordan_energy / sz_lagrangian (source slices exec'd, as H1 does), H1's dust term.
External input on disk: SZ21 newRMONDLett.tex eq. Minkowski_action.  No data.  kappa = 1/2 FITTED; not theory closed.

Run: OMP_NUM_THREADS=1 nice -n 15 python3 h3_jeans_control.py          (H3_MUTATE=1 for the mutation run)
"""
import json
import os
import resource
import sys
import time

import mpmath as mp
import sympy as sp

T0 = time.time()
MUT = os.environ.get("H3_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUTF = open(os.path.join(HERE, f"h3_jeans_control{TAG}.out"), "w")
RES = {"lane": "H3_jeans_control", "mutate": MUT, "criteria": "FROZEN_CRITERIA.md"}
CHECKS = []
SG = -1 if MUT else 1          # mutation: repulsive Newtonian gravity (T1b) and I -> -I (T1a, T4)


def P(*a):
    s = " ".join(str(v) for v in a)
    print(s, flush=True)
    OUTF.write(s + "\n")
    OUTF.flush()


def check(kid, ok, value, thr):
    CHECKS.append({"id": kid, "pass": bool(ok), "value": str(value), "threshold": thr})
    P(f"{kid} {'PASS' if ok else 'FAIL'} {value} {thr}")


P(f"H3_jeans_control  mutate={MUT}")
P("kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed.")

# ================================================================ C5 machinery (read-only exec of source slices)
C5 = os.path.join(REPO, "covariant_push_2026_10_22", "C5_health")
src = open(os.path.join(C5, "c5_health.py")).read()


def sl(a, b):
    i = src.index(a)
    return src[i:src.index(b, i)]


ns = {}
exec(compile("import sympy as sp\nimport math\nimport mpmath as mp\nSZSGN = 1\n"
             + sl("t, x, y, z = sp.symbols", "NAMES = [")
             + sl("def quad_matrix(", "log(f\"C5_health  mutate")
             + sl("KB, KK2, lam, Q0, Ls = sp.symbols", "Msz = sz_scalar()")
             + sl("def jordan_energy(", "EJ_aest = jordan_energy"), "c5_slices", "exec"), ns)
t, x, y, z, w, k = (ns[s] for s in ("t", "x", "y", "z", "w", "k"))
KB, KK2, lam, Q0, Ls = (ns[s] for s in ("KB", "KK2", "lam", "Q0", "Ls"))
quad_matrix, sz_lagrangian, jordan_energy = ns["quad_matrix"], ns["sz_lagrangian"], ns["jordan_energy"]
ETA4, X4 = ns["ETA4"], ns["X4"]
c5json = json.load(open(os.path.join(C5, "c5_health_results.json")))
h1json = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "H1_aest_F", "h1_aest_f_results.json")))
loc = {"k": k, "K_B": KB, "K_2": KK2, "lambda_s": lam, "Q_0": Q0, "L_s": Ls}
I, eps, rho = sp.symbols("I epsilon rho_bar", real=True)
G = sp.Rational(1, 16) / sp.pi                      # 16 pi G = 1


def jordan_solution(M):
    """v0 (linear-in-t part), v1 (static part) of the omega = 0 Jordan chain, as C5's jordan_energy builds them."""
    Mz = M.subs(w, 0)
    M1 = sp.diff(M, w).subs(w, 0)
    out = []
    for v0 in Mz.nullspace():
        sol, params = Mz.gauss_jordan_solve(-sp.I * M1 * v0)
        out.append((v0, sol.subs({p_: 0 for p_ in params})))
    return out


def growth_OI(M, small):
    """leading root Gamma^2 = -omega^2 of det M under (omega^2, small) -> s (omega^2, small)."""
    W2, s_ = sp.symbols("W2 s")
    dp = sp.expand(M.det().subs(w, sp.sqrt(W2)))
    cs = sp.Poly(sp.expand(dp.subs({W2: s_ * W2, small: s_ * small})), s_).all_coeffs()[::-1]
    lead = next(c for c in cs if sp.simplify(c) != 0)
    sols = sp.solve(lead, W2)
    return [sp.factor(-s0) for s0 in sols]


# ================================================================ T0 / K2: machinery sanity
q, p = [sp.Function(nm)(t, z) for nm in ("q", "p")]
E_free = jordan_energy(quad_matrix(sp.diff(q, t) ** 2 / 2, [q], (t, z), {}), w)
E_ghost = jordan_energy(quad_matrix(-sp.diff(q, t) ** 2 / 2, [q], (t, z), {}), w)
E_first = jordan_energy(quad_matrix(p * sp.diff(q, t) - p ** 2 / 2, [q, p], (t, z), {}), w)
signs = [sp.sign(E_free[0]), sp.sign(E_ghost[0]), sp.sign(E_first[0])]
check("K2", signs == [1, -1, 1], f"E_J signs free/ghost/first-order = {signs} ({E_free}, {E_ghost}, {E_first})",
      "+, -, + (T0: jordan_energy reads kinetic sign correctly)")
RES["T0"] = {"free": str(E_free), "ghost": str(E_ghost), "first_order": str(E_first)}

# ================================================================ shared metric pieces (Newtonian gauge, 2nd order)
Psi, Phi, al, vp, chi = [sp.Function(nm)(t, z) for nm in ("Psi", "Phi", "alpha", "varphi", "chi")]
hup = sp.diag(-2 * Psi, -2 * Phi, -2 * Phi, -2 * Phi)
gu00 = -1 + 2 * eps * Psi
guij = 1 + 2 * eps * Phi
sqg = (1 - 2 * eps * Psi) ** sp.Rational(-1, 2) * (1 + 2 * eps * Phi) ** sp.Rational(-3, 2)


def gr_part(hup_):
    """the first four (Fierz-Pauli) terms of C5's sz_lagrangian, written out here; K3 checks the split."""
    hlo = ETA4 * hup_ * ETA4
    htr = sum(ETA4[m, m] * hup_[m, m] for m in range(4))
    d = lambda f, m: sp.diff(f, X4[m])
    up = lambda m: ETA4[m, m]
    L = -sp.Rational(1, 2) * sum(d(htr, m) * d(hup_[m, n], n) for m in range(4) for n in range(4))
    L += sp.Rational(1, 4) * sum(up(r) * d(htr, r) ** 2 for r in range(4))
    L += sp.Rational(1, 2) * sum(d(hup_[m, r], m) * d(hup_[n, s], n) * ETA4[s, r]
                                 for m in range(4) for n in range(4) for r in range(4) for s in range(4))
    L += -sp.Rational(1, 4) * sum(up(r) * d(hup_[m, n], r) * d(hlo[m, n], r)
                                  for r in range(4) for m in range(4) for n in range(4))
    return L


def aest_extras(hup_, A, vphi):
    d = lambda f, m: sp.diff(f, X4[m])
    E = [d(A[i], 0) - sp.Rational(1, 2) * d(hup_[0, 0], i + 1) for i in range(3)]
    V = [d(vphi, i + 1) + Q0 * A[i] for i in range(3)]
    L = KB * sum(e ** 2 for e in E) - 2 * KB * sum(((d(A[j], i + 1) - d(A[i], j + 1)) / 2) ** 2
                                                    for i in range(3) for j in range(3))
    L += (2 - KB) * (2 * sum(E[i] * V[i] for i in range(3)) - (1 + lam) * sum(v ** 2 for v in V))
    L += 2 * KK2 * (d(vphi, 0) + Q0 * hup_[0, 0] / 2) ** 2
    return L


A_al = [sp.diff(al, v) for v in (x, y, z)]
k3 = sp.simplify(sp.expand(sz_lagrangian(hup, A_al, vp, False) - gr_part(hup) - aest_extras(hup, A_al, vp)))
check("K3", k3 == 0, f"sz_lagrangian - GR - AeST extras = {k3}", "0 (T1a's GR operator is exactly C5's)")

# ================================================================ AeST (H1's construction), K1
Ai = [eps * a for a in A_al]
A0low = -sp.sqrt((1 + guij * sum(a ** 2 for a in Ai)) / (-gu00))
dphi = [Q0 + eps * sp.diff(vp, t)] + [eps * sp.diff(vp, v) for v in (x, y, z)]
Aup = [gu00 * A0low] + [guij * a for a in Ai]
Qex = sum(Aup[m] * dphi[m] for m in range(4))
dL_aest = sp.expand(2 * SG * I * sp.series(sqg * (Qex - Q0), eps, 0, 3).removeO().coeff(eps, 2))
FA = [Psi, Phi, al, vp]
AE = {}
for stiff in (False, True):
    L0 = sz_lagrangian(hup, A_al, vp, stiff)
    M0 = quad_matrix(L0, FA, (t, z), {})
    M = quad_matrix(L0 + dL_aest, FA, (t, z), {})
    AE[stiff] = dict(M0=M0, M=M, EJ=jordan_energy(M0, w)[0], G2=growth_OI(M, I)[0], JS=jordan_solution(M0))
r1 = [sp.simplify(AE[False]["EJ"] - sp.sympify(c5json["H10"]["jordan_energy_AeST"][0], locals=loc)),
      sp.simplify(AE[True]["EJ"] - sp.sympify(c5json["H10"]["jordan_energy_AeST_plus_stiffness"][0], locals=loc))]
h1lin = h1json["linear"]
locI = dict(loc, I=I)
r1 += [sp.simplify(AE[False]["G2"] - sp.sympify(h1lin["no_gamma_L"]["Gamma2"], locals=locI)),
       sp.simplify(AE[True]["G2"] - sp.sympify(h1lin["with_gamma_L"]["Gamma2"], locals=locI))]
check("K1", MUT or all(r == 0 for r in r1), f"E_J - C5 (no gL, gL), Gamma^2 - H1 (no gL, gL) = {r1}",
      "all 0 (MUTATE: I sign flipped, Gamma^2 differs by design)")

# ================================================================ T1a: GR + k-essence dust
Q2ex = -gu00 * (Q0 + eps * sp.diff(chi, t)) ** 2 - guij * eps ** 2 * sum(sp.diff(chi, v) ** 2 for v in (x, y, z))
Qk = sp.sqrt(Q2ex)
dQ1_k = sp.series(Qk, eps, 0, 2).removeO().coeff(eps, 1)
dL_k = sp.expand(2 * SG * I * sp.series(sqg * (Qk - Q0), eps, 0, 3).removeO().coeff(eps, 2))
# AMENDMENT A1-1 (post-result): Q0 > 0 (SZ); RUN1 left Abs(Q0) from sqrt(Q0^2) in the norm
dQ1_k, dL_k = (sp.expand(e_.subs(sp.Abs(Q0), Q0)) for e_ in (dQ1_k, dL_k))
L0k = gr_part(hup) + 2 * KK2 * dQ1_k ** 2
FK = [Psi, Phi, chi]
M0k = quad_matrix(L0k, FK, (t, z), {})
Mk = quad_matrix(L0k + dL_k, FK, (t, z), {})
EJk = jordan_energy(M0k, w)
G2k = growth_OI(Mk, I)
P(f"  T1a GR+k-essence: dQ^(1) = {dQ1_k}; E_J(I=0) = {EJk}; Gamma^2 (O(I)) = {G2k}")

# ================================================================ T1b: Newtonian Clebsch dust
drho, th, PhN = [sp.Function(nm)(t, z) for nm in ("drho", "theta", "PhiN")]
LN0 = -drho * (sp.diff(th, t) + PhN) - SG * sp.diff(PhN, z) ** 2 / (8 * sp.pi * G)
LN = LN0 - rho / 2 * sp.diff(th, z) ** 2
FN = [drho, th, PhN]
M0N = quad_matrix(LN0, FN, (t, z), {})
MN = quad_matrix(LN, FN, (t, z), {})
EJN = jordan_energy(M0N, w)
G2N = growth_OI(MN, rho)
P(f"  T1b Newton Clebsch: E_J(rho=0) = {EJN}; Gamma^2 (O(rho)) = {G2N}")
# K4: hand Noether energy on the Jordan solution, and Gamma^2 = 4 pi G rho at every k
(v0N, v1N), = jordan_solution(M0N)
drho_s, Phi_s = v1N[0], v1N[2]
H_hand = sp.simplify(sp.re(sp.expand(drho_s * sp.conjugate(Phi_s) + k ** 2 * Phi_s * sp.conjugate(Phi_s) / (8 * sp.pi * G))))
ratioN = sp.simplify(EJN[0] / H_hand) if H_hand != 0 else None
k4 = (len(G2N) == 1 and sp.simplify(G2N[0] - 4 * sp.pi * G * rho) == 0 and ratioN is not None and ratioN.is_number
      and float(ratioN) > 0)
check("K4", k4, f"jordan_energy / hand Noether H = {ratioN} (constant normalisation); Gamma^2 - 4 pi G rho = "
      f"{[sp.simplify(g_ - 4 * sp.pi * G * rho) for g_ in G2N]}", "positive constant AND 0 at every k")
normN = ratioN if ratioN is not None and ratioN.is_number else sp.Integer(1)


# ================================================================ T2b/T3: lump normalisation G_eff(k)
def lump(EJ, JS, dQ_fn, rho_per_dQ):
    (v0, v1), = JS
    dQ_static, dQ_secular = dQ_fn(v0, v1)
    drho_ = rho_per_dQ * dQ_static
    Geff = sp.simplify(-EJ * k ** 2 / (2 * sp.pi * drho_ * sp.conjugate(drho_)) / normN) if drho_ != 0 else None
    return dict(dQ_static=sp.simplify(dQ_static), dQ_secular=sp.simplify(dQ_secular), Geff_over_G=sp.simplify(Geff / G)
                if Geff is not None else None)


dQ_aest = lambda v0, v1: (v0[3] - Q0 * v1[0], -Q0 * v0[0])           # phi-dot - Q0 Psi
dQ_kess = lambda v0, v1: (v0[2] - Q0 * v1[0], -Q0 * v0[0])           # chi-dot - Q0 Psi
LUMP = {"Newton": dict(dQ_static=drho_s, dQ_secular=v0N[0],
                       Geff_over_G=sp.simplify(-EJN[0] * k ** 2 / (2 * sp.pi * drho_s * sp.conjugate(drho_s)) / normN / G)),
        "GR+kess": lump(EJk[0], jordan_solution(M0k), dQ_kess, 4 * KK2 * Q0),
        "AeST": lump(AE[False]["EJ"], AE[False]["JS"], dQ_aest, 4 * KK2 * Q0),
        "AeST+gL": lump(AE[True]["EJ"], AE[True]["JS"], dQ_aest, 4 * KK2 * Q0)}
for kk_, v in LUMP.items():
    P(f"  lump [{kk_}]: dQ_static = {v['dQ_static']}, dQ_secular = {v['dQ_secular']}, G_eff/G = {v['Geff_over_G']}")

# AMENDMENT A1-4 (reported only): G_pot(k) = -k^2 Psi_static / (4 pi G drho) on the Jordan mode; E_J vs -1/2 drho Psi
def gpot(JS, ipsi, dQ_fn, rho_per_dQ):
    (v0, v1), = JS
    drho_ = rho_per_dQ * dQ_fn(v0, v1)[0]
    return sp.simplify(-k ** 2 * v1[ipsi] / (4 * sp.pi * G * drho_) / G * G)


GPOT = {"Newton": sp.simplify(-k ** 2 * Phi_s / (4 * sp.pi * G * drho_s)),
        "GR+kess": gpot(jordan_solution(M0k), 0, dQ_kess, 4 * KK2 * Q0),
        "AeST": gpot(AE[False]["JS"], 0, dQ_aest, 4 * KK2 * Q0),
        "AeST+gL": gpot(AE[True]["JS"], 0, dQ_aest, 4 * KK2 * Q0)}
for kk_, v in GPOT.items():
    P(f"  G_pot/G [{kk_}] (lump's own static potential) = {sp.simplify(v)}; G_eff(energy)/G - G_pot/G = "
      f"{sp.simplify(LUMP[kk_]['Geff_over_G'] - v)}")
RES["G_pot_over_G"] = {kk_: str(sp.simplify(v)) for kk_, v in GPOT.items()}

# ================================================================ T1 grading
pos = {k: 1, KK2: sp.Rational(1, 2), Q0: 1, KB: sp.Rational(1, 20), lam: 0}


def neg_everywhere(expr, subs_extra=None, kgrid=None):
    f = sp.lambdify(k, sp.re(expr.subs({lam: 0, KB: sp.Rational(1, 20), Q0: 1, KK2: sp.Rational(39, 40)}
                                     | (subs_extra or {}))), "mpmath")
    kg = kgrid or [mp.mpf(10) ** (e / 10) for e in range(-40, 81)]
    vals = [f(kv) for kv in kg]
    return all(v_ < 0 for v_ in vals), vals


t1 = {}
for lab, EJ_, G2_, rho_expr in (("GR+kess", EJk[0], G2k[0], 2 * I * Q0), ("Newton", EJN[0], G2N[0], rho)):
    neg, _ = neg_everywhere(EJ_)
    ir = sp.simplify(sp.limit(G2_, k, 0) - 4 * sp.pi * G * rho_expr)
    rat = sp.simplify(EJ_ / G2_)
    small = I if lab == "GR+kess" else rho
    neg_ratio, _ = neg_everywhere(rat * small)
    t1[lab] = dict(EJ_negative_all_k=neg, Gamma2_IR_residual=str(ir), EJ_over_Gamma2_times_source_negative_on_grid=neg_ratio,
                   EJ=str(EJ_), Gamma2=str(G2_), ratio=str(rat))
    P(f"  T1 [{lab}]: E_J<0 all k: {neg}; Gamma^2(0) - 4 pi G rho = {ir}; E_J*src/Gamma^2 < 0 on grid: {neg_ratio}")
T1_PASS = all(v["EJ_negative_all_k"] and v["Gamma2_IR_residual"] == "0" for v in t1.values())
T1_signs = all(v["EJ_over_Gamma2_times_source_negative_on_grid"] for v in t1.values())
P(f"T1 control (criterion (i) flags normal gravity): {'PASS' if T1_PASS and T1_signs else 'FAIL'}")
RES["T1"] = t1
RES["T1_pass"] = bool(T1_PASS and T1_signs)

# ================================================================ T2a: roots and Krein at I = 0 (AeST, lambda = 0)
mu_v, KBv, Q0v = mp.mpf(1), mp.mpf("0.05"), mp.mpf(1)
K2v = mu_v ** 2 * (2 - KBv) / (2 * Q0v ** 2)
Lsv = mp.mpf("2.4e-5")
mp.mp.dps = 60
W2 = sp.Symbol("W2")


def detpoly(M):
    d = sp.expand(M.det())
    assert sp.expand(d.subs(w, -w) - d) == 0
    return sp.Poly(sp.expand(d.subs(w, sp.sqrt(W2))), W2)


def num_subs(stiff, Iv):
    return {KB: sp.nsimplify("0.05"), Q0: 1, KK2: sp.nsimplify("0.975"), lam: 0, Ls: sp.nsimplify("2.4e-5") if stiff else 0,
            I: sp.nsimplify(Iv)}


def roots_W2(polyW2, sub, kv):
    cs = [mp.mpmathify(sp.N(c.subs(sub).subs(k, sp.nsimplify(kv)), 70)) for c in polyW2.all_coeffs()]
    while cs and cs[0] == 0:
        cs = cs[1:]
    zeros_at_0 = 0
    while cs and abs(cs[-1]) == 0:
        cs = cs[:-1]
        zeros_at_0 += 1
    r = mp.polyroots(cs, maxsteps=400, extraprec=400) if len(cs) > 1 else []
    return list(r), zeros_at_0


def krein(M, sub, kv, W2v):
    wv = mp.sqrt(W2v)
    Mn = M.subs(sub).subs(k, sp.nsimplify(kv))
    Am = mp.matrix([[mp.mpmathify(sp.N(Mn[i, j].subs(w, sp.Float(str(wv), 60)), 60)) for j in range(Mn.cols)]
                    for i in range(Mn.rows)])
    U, S, V = mp.svd_c(Am)
    v = V.transpose_conj()[:, Mn.cols - 1]
    dM = sp.diff(Mn, w)
    dMn = mp.matrix([[mp.mpmathify(sp.N(dM[i, j].subs(w, sp.Float(str(wv), 60)), 60)) for j in range(Mn.cols)]
                     for i in range(Mn.rows)])
    return float(mp.re(wv * (v.transpose_conj() * dMn * v)[0])), float(S[Mn.cols - 1] / S[0])


POLY = {s_: detpoly(AE[s_]["M"]) for s_ in (False, True)}
t2a, T2a_ok = {}, True
for stiff in (False, True):
    for kv in ("1e-3", "1", "1e3", "1e6"):
        sub = num_subs(stiff, 0)
        P0 = sp.Poly(sp.expand(AE[stiff]["M0"].det().subs(w, sp.sqrt(W2))), W2)
        rts, z0 = roots_W2(P0, sub, kv)
        # multiplicity of omega = 0 in omega: 2 * (multiplicity of W2 = 0)
        kr = []
        for r in rts:
            ok_r = abs(mp.im(r)) < 1e-30 * max(1, abs(r)) and mp.re(r) > 0
            kre = krein(AE[stiff]["M0"], sub, kv, mp.re(r)) if ok_r else (None, None)
            kr.append((float(mp.re(r)), kre[0], kre[1]))
            T2a_ok &= bool(ok_r) and kre[0] is not None and kre[0] > 0
        T2a_ok &= z0 == 1
        t2a[f"{'gL' if stiff else 'no gL'}|k={kv}"] = {"omega0_mult_in_omega": 2 * z0, "nonzero_roots(W2,krein,svd_rel)": kr}
        P(f"  T2a [{'gL' if stiff else 'no gL'}] k={kv}: omega=0 multiplicity {2 * z0}; roots {kr}")
RES["T2a"] = t2a

# ================================================================ T2b grading
geA = {s_: LUMP["AeST+gL" if s_ else "AeST"]["Geff_over_G"] for s_ in (False, True)}
dqA = {s_: LUMP["AeST+gL" if s_ else "AeST"]["dQ_static"] for s_ in (False, True)}
kgrid = [mp.mpf(10) ** (e / 20) for e in range(-60, 141)]
fA = {s_: sp.lambdify(k, geA[s_].subs({lam: 0, KB: sp.nsimplify("0.05"), Q0: 1, KK2: sp.nsimplify("0.975"),
                                        Ls: sp.nsimplify("2.4e-5")}), "mpmath") for s_ in (False, True)}
gA0 = {s_: sp.limit(geA[s_].subs(lam, 0), k, 0) for s_ in (False, True)}
valsA = {s_: [mp.re(fA[s_](kv)) for kv in kgrid] for s_ in (False, True)}
g0n = {s_: float(gA0[s_].subs({KB: 0.05, Q0: 1, KK2: 0.975})) for s_ in (False, True)}
grav_noL = dqA[False] != 0 and g0n[False] > 0 and all(0 < v_ <= g0n[False] * (1 + 1e-12) for v_ in valsA[False])
neg_idx = [i for i, v_ in enumerate(valsA[True]) if v_ < 0]
first_neg = kgrid[neg_idx[0]] if neg_idx else None
grav_L = (dqA[True] != 0 and g0n[True] > 0 and all(v_ <= g0n[True] * (1 + 1e-12) for v_ in valsA[True])
          and (not neg_idx or all(v_ < 0 for v_ in valsA[True][neg_idx[0]:])))
T2_PASS = bool(T2a_ok and grav_noL and grav_L)
geK0 = sp.limit(LUMP["GR+kess"]["Geff_over_G"], k, 0) if LUMP["GR+kess"]["Geff_over_G"] is not None else None
P(f"  T2b: G_eff/G(k->0) AeST = {gA0[False]} (no gL), {gA0[True]} (gL); GR+kess = {geK0}; Newton = {LUMP['Newton']['Geff_over_G']}")
P(f"  T2b: AeST no gL: G_eff in (0, G_eff(0)] on grid: {grav_noL}; gL: <= G_eff(0), negative only above "
  f"k = {mp.nstr(first_neg, 5) if first_neg is not None else 'none'} mu: {grav_L}")
P(f"T2 (instability, not ghost): {'PASS' if T2_PASS else 'FAIL'}  (T2a {T2a_ok})")
RES["T2"] = {"T2a_ok": bool(T2a_ok), "Geff_over_G_AeST": str(geA[False]), "Geff_over_G_AeST_gL": str(geA[True]),
             "Geff0_AeST": str(gA0[False]), "Geff0_AeST_gL": str(gA0[True]), "Geff0_GRkess": str(geK0),
             "Geff_Newton": str(LUMP["Newton"]["Geff_over_G"]), "grav_form_noL": bool(grav_noL), "grav_form_gL": bool(grav_L),
             "Geff_first_negative_k_over_mu_gL": None if first_neg is None else float(first_neg),
             "Geff_min_max_noL": [float(min(valsA[False])), float(max(valsA[False]))], "pass": T2_PASS}

# ================================================================ T3: vacuum
EJk_neg = t1["GR+kess"]["EJ_negative_all_k"]
dqK = LUMP["GR+kess"]["dQ_static"]
# AMENDMENT A1-3 (post-result): RUN1 also required the control's E_J < 0 at every k, which the frozen T3 line does not
T3_jeans = bool(dqA[False] != 0 and dqA[True] != 0 and dqK != 0 and geK0 is not None and float(geK0) > 0)
P(f"T3 vacuum: AeST dQ_static = {dqA[False]} / {dqA[True]}; GR+kess dQ_static = {dqK}, G_eff^GR(0)/G = {geK0}; "
  f"verdict: {'zero-background Jeans mode' if T3_jeans else 'genuine vacuum negative-energy mode (or control differs)'}")
RES["T3"] = {"dQ_static_AeST": str(dqA[False]), "dQ_static_AeST_gL": str(dqA[True]), "dQ_static_GRkess": str(dqK),
             "dQ_secular": {kk_: str(v["dQ_secular"]) for kk_, v in LUMP.items()}, "zero_background_jeans": T3_jeans}

# ================================================================ T4: exact roots at finite I
kc = (2 * mu_v ** 2 / Lsv ** 2) ** mp.mpf("0.25")
kg4 = sorted([mp.mpf(10) ** (-3 + 9 * i / 399) for i in range(400)] + [kc * mp.mpf("0.99"), kc * mp.mpf("1.01")])
t4, T4_ok, K5val = {}, True, None
T4_fail_lines = []
# AMENDMENT A1-2 (post-result): RUN1 substituted I = 0 into the O(I) closed form (K5 = inf); keep I symbolic
G2cl = {s_: sp.lambdify((k, I), AE[s_]["G2"].subs({kk_: v_ for kk_, v_ in num_subs(s_, 0).items() if kk_ != I}), "mpmath")
        for s_ in (False, True)}
for Iv in ("2e-7", "2e-3"):
    for stiff in (False, True):
        sub = num_subs(stiff, Iv)
        g4 = mp.mpf(Iv) * Q0v / 2
        maxr, nunst_max, band_end_ok, last_pos_k, nk_bad_krein = mp.mpf(-1e9), 0, True, None, 0
        gams = []
        for kv in kg4:
            rts, z0 = roots_W2(POLY[stiff], sub, str(kv))
            unst = [r for r in rts if mp.re(r) < 0 and abs(mp.im(r)) < 1e-20 * max(1, abs(r))]
            cplx = [r for r in rts if abs(mp.im(r)) >= 1e-20 * max(1, abs(r))]
            nun = len(unst) + len(cplx)
            nunst_max = max(nunst_max, nun)
            gam = max([-mp.re(r) for r in unst], default=mp.mpf(0))
            gams.append(gam)
            if gam > 0:
                last_pos_k = kv
            maxr = max(maxr, gam / g4)
            if stiff and kv >= kc * mp.mpf("1.01") and gam > 0:
                band_end_ok = False
            if kv == kg4[0] and Iv == "2e-7" and not stiff:
                exact = gam
                ocl = mp.re(G2cl[False](kv, mp.mpf(Iv)))
                K5val = float(abs(exact / ocl - 1)) if ocl != 0 else float("inf")
        gam_hi_increasing = bool(gams[-1] > gams[-2] > gams[-3] > 0)
        ok = nunst_max <= 1 and maxr <= 1 + mp.mpf("1e-6") and (band_end_ok if stiff else True)
        T4_ok &= ok
        # A1-5: the frozen FAIL ('pathological') line, separate from PASS
        T4_fail_lines.append(bool(nunst_max > 1 or maxr > 1 + mp.mpf("1e-6") or gam_hi_increasing))
        lab = f"I={Iv}|{'gL' if stiff else 'no gL'}"
        t4[lab] = {"max_Gamma2_over_4piGrho": float(maxr), "max_unstable_roots_per_k": nunst_max,
                   "band_ends_by_1.01kc": band_end_ok if stiff else None,
                   "largest_k_with_growth_over_mu": None if last_pos_k is None else float(last_pos_k)}
        P(f"  T4 [{lab}]: max Gamma^2/(4 pi G rho) = {mp.nstr(maxr, 10)}; max #unstable W2 roots/k = {nunst_max}; "
          f"band ends (gL) {band_end_ok if stiff else '-'}; largest k with growth = "
          f"{mp.nstr(last_pos_k, 5) if last_pos_k is not None else 'none'} mu (k_c = {mp.nstr(kc, 5)})")
# A1-4 (reported): the same exact-root scan for the GR + k-essence control, and Krein of every omega^2 > 0 root
POLYK = detpoly(Mk)
t4c = {}
for Iv in ("2e-7", "2e-3"):
    subk = {KK2: sp.nsimplify("0.975"), Q0: 1, I: sp.nsimplify(Iv)}
    nmax, kr_neg = 0, []
    for kv in kg4[::20] + [mp.mpf(1e5)]:
        rts, z0 = roots_W2(POLYK, subk, str(kv))
        nmax = max(nmax, sum(1 for r in rts if mp.re(r) < 0 or abs(mp.im(r)) > 1e-20 * max(1, abs(r))))
        for r in rts:
            if mp.re(r) > 0 and abs(mp.im(r)) < 1e-30 * abs(r):
                kre = krein(Mk, subk, str(kv), mp.re(r))[0]
                if kre < 0:
                    kr_neg.append((float(kv), float(mp.re(r)), kre))
    t4c[f"I={Iv}"] = {"max_unstable_roots_per_k": nmax, "negative_krein_roots(k,W2,krein)": kr_neg[:6],
                      "n_negative_krein": len(kr_neg)}
    P(f"  T4-control GR+kess I={Iv}: max #unstable/k = {nmax}; negative-Krein omega^2>0 roots: {len(kr_neg)} "
      f"(first {kr_neg[:3]})")
t4k = {}
for Iv in ("2e-7", "2e-3"):
    for stiff in (False, True):
        sub = num_subs(stiff, Iv)
        kr_neg, unst2 = [], []
        for kv in kg4[::20] + [mp.mpf(1e5)]:
            rts, z0 = roots_W2(POLY[stiff], sub, str(kv))
            nun = sum(1 for r in rts if mp.re(r) < 0 or abs(mp.im(r)) > 1e-20 * max(1, abs(r)))
            if nun > 1:
                unst2.append((float(kv), [mp.nstr(r, 6) for r in rts]))
            for r in rts:
                if mp.re(r) > 0 and abs(mp.im(r)) < 1e-30 * abs(r):
                    kre = krein(AE[stiff]["M"], sub, str(kv), mp.re(r))[0]
                    if kre < 0:
                        kr_neg.append((float(kv), float(mp.re(r)), kre))
        lab = f"I={Iv}|{'gL' if stiff else 'no gL'}"
        t4k[lab] = {"negative_krein_roots(k,W2,krein)": kr_neg[:6], "n_negative_krein": len(kr_neg),
                    "k_with_two_unstable": unst2[:6]}
        P(f"  T4-AeST Krein {lab}: negative-Krein omega^2>0 roots {len(kr_neg)} (first {kr_neg[:2]}); "
          f"k with >1 unstable root: {unst2[:3]}")
RES["T4_control_GRkess"] = t4c
RES["T4_krein_AeST"] = t4k

check("K5", MUT or (K5val is not None and K5val <= 1e-4), f"exact vs O(I) Gamma^2 at k = 1e-3 mu, I = 2e-7: rel {K5val}",
      "<= 1e-4")
P(f"T4 (rate bounded, band ends): {'PASS' if T4_ok else 'FAIL'}")
RES["T4"] = t4
RES["T4_pass"] = bool(T4_ok)
RES["k_c_gL_over_mu"] = float(kc)

# ================================================================ verdict
# AMENDMENT A1-5 (post-result): RUN1 mapped any failed K-check to UNDECIDED and any non-PASS to FAILS; the frozen
# rule (section 3) is: UNDECIDED iff T0 (K2) fails or the tests split with no FAIL line triggered; FAILS iff a FAIL line.
fA_noL = sp.lambdify(k, AE[False]["EJ"].subs({lam: 0, KB: sp.nsimplify("0.05"), Q0: 1, KK2: sp.nsimplify("0.975")}), "mpmath")
fK = sp.lambdify(k, EJk[0].subs({Q0: 1, KK2: sp.nsimplify("0.975")}), "mpmath")
T1_fail = any(mp.re(fK(kv)) >= 0 and mp.re(fA_noL(kv)) < 0 for kv in kgrid)
T2_fail = bool((not T2a_ok) or (not grav_noL and max(valsA[False]) > g0n[False] * 1e3) or dqA[False] == 0)
T4_fail = any(T4_fail_lines)
RES["fail_lines"] = {"T1": bool(T1_fail), "T2": T2_fail, "T3_genuine": not T3_jeans, "T4": T4_fail}
k2_ok = next(c["pass"] for c in CHECKS if c["id"] == "K2")
if not k2_ok:
    verdict = "UNDECIDED (T0 failed)"
elif RES["T1_pass"] and T2_PASS and T3_jeans and T4_ok:
    verdict = "CLAIM HOLDS"
elif T1_fail or T2_fail or (not T3_jeans) or T4_fail:
    verdict = "CLAIM FAILS (frozen rule; lines " + ", ".join(kk_ for kk_, v in RES["fail_lines"].items() if v) + ")"
else:
    verdict = "UNDECIDED (split, no FAIL line)"
RES["verdict"] = verdict
P(f"VERDICT: {verdict}")
npass = sum(c["pass"] for c in CHECKS)
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
RES.update(checks=CHECKS, n_pass=npass, n_checks=len(CHECKS), runtime_s=round(time.time() - T0, 1), max_rss_GB=round(rss, 3))
RES["LUMP"] = {kk_: {a: str(b) for a, b in v.items()} for kk_, v in LUMP.items()}
P(f"  runtime {time.time() - T0:.1f} s, max RSS {rss:.3f} GB")
P(f"H3 COMPLETE: {npass}/{len(CHECKS)} checks PASS.")
json.dump(RES, open(os.path.join(HERE, f"h3_jeans_control_results{TAG}.json"), "w"), indent=1, default=str)
sys.exit(0 if npass == len(CHECKS) else 1)
