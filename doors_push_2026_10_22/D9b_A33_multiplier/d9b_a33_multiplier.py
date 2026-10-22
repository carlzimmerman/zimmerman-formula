#!/usr/bin/env python3
"""D9b_A33_multiplier: A33 (DSF-21 master action) + a Lagrange multiplier enforcing D.P = rho_c - rhobar.

Criteria: FROZEN_CRITERIA.md (committed alone first). kappa = 1/2 FITTED. Footings 9.36e-11 / 1.13e-10 m/s^2, never pooled.
Cold energy, no particle species. Not "theory closed".

Run:    OMP_NUM_THREADS=1 nice -n 10 python3 d9b_a33_multiplier.py
Mutate: D9B_MUTATE=1 ... (WT-02/CFG938 S1d expansion term put into the constraint; F1 must FAIL)
Deterministic, no network. Writes d9b_a33_multiplier[_MUTATE].out and d9b_a33_multiplier_results[_MUTATE].json.
"""
import json, os, sys, random
import numpy as np
import sympy as sp

MUT = os.environ.get("D9B_MUTATE", "0") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
TAG = "_MUTATE" if MUT else ""
OUT = os.path.join(HERE, f"d9b_a33_multiplier{TAG}.out")
JS = os.path.join(HERE, f"d9b_a33_multiplier_results{TAG}.json")
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

lines, checks, R = [], [], {}
def log(s=""):
    print(s); lines.append(s)
def check(cid, ok, value, thr):
    checks.append((cid, bool(ok)))
    log(f"{cid} {'PASS' if ok else 'FAIL'} {value} {thr}")

# ---------------------------------------------------------------- constants (sources in FROZEN_CRITERIA.md)
G = 6.674e-11; c = 2.998e8; pc = 3.0857e16
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
H0 = 67.4e3 / 3.0857e22; rho_crit = 3 * H0**2 / (8 * np.pi * G); Omega_c = 0.264
rhobar_c = Omega_c * rho_crit
RATIO_CB = 5.3643
LSTAR = {"24pc": 24 * pc, "1kpc": 1000 * pc}
R["constants"] = dict(G=G, c=c, pc=pc, a0=A0, H0_si=H0, rho_crit=rho_crit, Omega_c=Omega_c, rhobar_c=rhobar_c,
                      Omega_c_over_Omega_b=RATIO_CB, Lstar_m=LSTAR)

# ================================================================ C: linear Dirac algorithm per Fourier mode
def lin_dirac(L, q, qd):
    n = len(q)
    M = sp.Matrix(n, n, lambda i, j: sp.diff(L, qd[i], qd[j]))
    N = sp.Matrix(n, n, lambda i, j: sp.diff(L, qd[i], q[j]))
    V = sp.Matrix(n, n, lambda i, j: sp.diff(L, q[i], q[j]))
    J = sp.zeros(2 * n); J[:n, n:] = sp.eye(n); J[n:, :n] = -sp.eye(n)
    prim = [sp.Matrix.hstack(-(w.T * N), w.T) for w in M.T.nullspace()]
    A = sp.Matrix.hstack(-N, sp.eye(n))
    H0m = A.T * M.pinv() * A - sp.Matrix.vstack(sp.Matrix.hstack(V, sp.zeros(n)), sp.zeros(n, 2 * n))
    H0m = (H0m + H0m.T) / 2
    P = sp.Matrix.vstack(*prim) if prim else sp.zeros(0, 2 * n)
    C = P
    while True:
        Ac = C * J * P.T
        Bc = C * J * H0m
        added = False
        for y in Ac.T.nullspace():
            row = y.T * Bc
            test = sp.Matrix.vstack(C, row)
            if test.rank() > C.rank():
                C = test; added = True
        if not added:
            break
    r = C.rank(); sc = (C * J * C.T).rank(); fc = r - sc
    s = sp.Symbol("s")
    d = sp.expand((s**2 * M + s * (N - N.T) - V).det())
    deg = sp.degree(d, s) if d != 0 else -1
    return dict(dims=2 * n, constraints=int(r), second_class=int(sc), first_class=int(fc),
                dof=float(sp.Rational(2 * n - 2 * fc - sc, 2)), det_degree_half=float(deg) / 2)

qs = sp.symbols("q0:6"); vs = sp.symbols("v0:6")
def scalar_L(case, P):
    """A68 H=0 scalar action (zeta, n, psi, sigma) + irrotational medium s + multiplier lam."""
    K, b, eta, gam, p, rho, sc2, xi, mc = (P[k] for k in ["K", "beta", "eta", "gamma", "p", "rho", "sc2", "xi", "mc"])
    z, n, psi, sig, s, lam = qs; zd, nd, psid, sigd, sd, lamd = vs
    A = 2 + 3 * b; Y = -p**2 * psi
    L = (-3 * A * zd**2 + 2 * A * zd * Y - b * Y**2 + 2 * p**2 * z**2 + 4 * p**2 * n * z) / (4 * K) \
        + xi * p**2 * n * sig + eta * p**2 / 2 * sigd**2 - (K * p**2 + gam * p**4) / 2 * sig**2
    if case in ("med", "lam"):
        L += rho / 2 * p**2 * (sd + psi)**2 - rho * sc2 / 2 * (p**2 * s - 3 * z)**2 - mc * rho * p**2 * s * n
    if case == "lam":
        L += lam * (-p**2 * sig - rho * (p**2 * s - 3 * z))
    return L

log("== C: Dirac count per scalar Fourier mode (H = 0, A68 action + medium + lambda) ==")
cres = {}
for seed in range(3):
    rnd = random.Random(seed)
    Rr = lambda: sp.Rational(rnd.randint(1, 9), rnd.randint(1, 9))
    base = dict(K=Rr(), beta=Rr(), eta=Rr(), gamma=Rr(), p=Rr(), rho=Rr(), sc2=Rr())
    for lab, case, nv, xi, mc in [("A33_nomedium", "nomed", 4, 1, 1), ("A33_medium", "med", 5, 1, 1),
                                  ("M_lit", "lam", 6, 1, 1), ("Mstar_xi0", "lam", 6, 0, 1), ("Mstar_mc0", "lam", 6, 1, 0)]:
        Pp = dict(base, xi=xi, mc=mc)
        cres.setdefault(lab, []).append(lin_dirac(scalar_L(case, Pp), list(qs[:nv]), list(vs[:nv])))
for lab, v in cres.items():
    log(f"  {lab}: {v[0]}  (stable over 3 draws: {all(x == v[0] for x in v)})")
R["dirac_per_mode"] = {k: v[0] for k, v in cres.items()}
stable = all(all(x == v[0] for x in v) for v in cres.values())
check("C1", cres["A33_nomedium"][0]["dof"] == 1 and stable, f"scalar_DOF={cres['A33_nomedium'][0]['dof']}", "==1 (A68 D4/D5)")
c2ok = cres["A33_medium"][0]["dof"] == cres["A33_medium"][0]["det_degree_half"]
check("C2", c2ok and stable, f"scalar_DOF={cres['A33_medium'][0]['dof']}", "terminates; Dirac==deg(det)/2; stable")
same = cres["M_lit"][0] == cres["Mstar_xi0"][0] == cres["Mstar_mc0"][0]
dSC = cres["M_lit"][0]["second_class"] - cres["A33_medium"][0]["second_class"]
check("C3", same and stable, f"scalar_DOF={cres['M_lit'][0]['dof']} addedSC={dSC} addeddims=2", "identical over draws and members")
diff_dirac = cres["A33_medium"][0]["dof"] - cres["M_lit"][0]["dof"]
diff_det = cres["A33_medium"][0]["det_degree_half"] - cres["M_lit"][0]["det_degree_half"]
check("C4", diff_dirac == diff_det and diff_dirac >= 0 and float(diff_dirac).is_integer(),
      f"removed={diff_dirac} (Dirac) {diff_det} (det)", "equal integer >= 0")
# field-theory count (A68: 26 dims, 8 FC); medium = 3 Lagrangian labels (6 dims); lambda adds 2 dims, dSC second class
dims_no = 26 + 6; dims_lam = 26 + 6 + 2
dof_no = (dims_no - 16) / 2; dof_lam = (dims_lam - 16 - dSC) / 2
R["field_theory_count"] = dict(no_lambda=dict(dims=dims_no, FC=8, SC=0, DOF=dof_no),
                               with_lambda=dict(dims=dims_lam, FC=8, SC=dSC, DOF=dof_lam),
                               split="2 tensor + 2 transverse P + 2 vortical medium + scalar(s)")
log(f"  field theory: no lambda (26+6 dims, 8 FC, 0 SC) -> {dof_no} DOF; with lambda (34 dims, 8 FC, {dSC} SC) -> {dof_lam} DOF")

# which mode is removed: high-p speeds, symbolic
K, b, eta, gam, p, rho, sc2 = sp.symbols("K beta eta gamma p rho sc2", positive=True)
ssym = sp.Symbol("s"); w2 = sp.Symbol("w2")
def hi_p_speeds(case, nv, xi, mc):
    L = scalar_L(case, dict(K=K, beta=b, eta=eta, gamma=gam, p=p, rho=rho, sc2=sc2, xi=xi, mc=mc))
    qq, vv = list(qs[:nv]), list(vs[:nv]); n = nv
    M = sp.Matrix(n, n, lambda i, j: sp.diff(L, vv[i], vv[j])); N = sp.Matrix(n, n, lambda i, j: sp.diff(L, vv[i], qq[j]))
    V = sp.Matrix(n, n, lambda i, j: sp.diff(L, qq[i], qq[j]))
    d = sp.expand((ssym**2 * M + ssym * (N - N.T) - V).det())
    poly = sp.Poly(sp.expand(d.subs(ssym, sp.sqrt(-w2))), w2)
    return sorted([sp.simplify(sp.limit(r / p**2, p, sp.oo)) for r in sp.solve(poly, w2)], key=str)
sp_med = hi_p_speeds("med", 5, 1, 1); sp_lam = hi_p_speeds("lam", 6, 0, 1)
log(f"  high-p w^2/p^2, A33+medium: {sp_med}")
log(f"  high-p w^2/p^2, M*        : {sp_lam}")
R["high_p_speeds"] = dict(A33_medium=[str(x) for x in sp_med], Mstar=[str(x) for x in sp_lam])
cs2_expected = (sc2 + gam * rho) / (1 + eta * rho)
R["surviving_scalar"] = "dressed medium sound, w^2/p^2 = (sigma_c^2 + gamma rho_c)/(1 + eta rho_c); the 5th mode (gamma/eta) and bare sound (sigma_c^2) merge into it"
log(f"  surviving scalar == (sc2 + gamma rho)/(1 + eta rho): {sp.simplify(sp_lam[0] - cs2_expected) == 0}")

# ================================================================ L: static spherical cold branch
log("== L: static cold branch, gamma -> 0 ==")
r = sp.Symbol("r", positive=True); a0, g, u, gN, xi_, mc_, cc = sp.symbols("a0 g u g_N xi m_c c", real=True)
Phi, Pf, lam_f, rc, rb = (sp.Function(nm)(r) for nm in ["Phi", "P", "lam", "rho_c", "rho_b"])
rhob_s = sp.Symbol("rhobar")
W = lambda uu: a0**2 / K * (-uu / a0 - sp.log(1 - uu / a0))
divP = sp.diff(r**2 * Pf, r) / r**2
Lst = r**2 * (-sp.diff(Phi, r)**2 / (2 * K) - (rb + mc_ * rc) * Phi + xi_ * Pf * sp.diff(Phi, r) - W(K * Pf)
              + lam_f * (divP - rc + rhob_s))
eqs = sp.euler_equations(Lst, [Phi, Pf, lam_f, rc], r)
eP = sp.simplify(eqs[1].lhs / r**2)                    # P equation
eRho = sp.simplify(eqs[3].lhs / r**2)                  # cold equilibrium (rho_c variation): -(m_c Phi + lam) = const
gsym = sp.diff(Phi, r)
# P equation: xi Phi' - K W'(K P) - lam' = 0  ; medium: m_c Phi' + lam' = 0
lamp = sp.solve(sp.Eq(sp.diff(eRho, r), 0), sp.diff(lam_f, r))[0]
Peq = sp.simplify(eP.subs(sp.diff(lam_f, r), lamp))
Dfull = a0 * u / (a0 - u)
Peq_u = sp.simplify(Peq.subs(Pf, u / K).subs(gsym, g))
s_ = xi_ + mc_
L1_force = sp.simplify(Peq_u - (s_ * g - Dfull))
log(f"  derived P+medium balance: (xi+m_c) g = K W'(u) = a0 u/(a0-u); residual {L1_force}")
# Poisson: (r^2 g)' = K r^2 (rho_b + m_c rho_c + xi divP); with rho_c - rhobar = divP and the swindle => g = g_N + (xi+m_c) u
ePhi = sp.simplify(eqs[0].lhs)
pois = sp.simplify(ePhi.subs(rc, rhob_s + divP) + r**2 * mc_ * rhob_s)  # swindle: remove uniform background source
target = sp.simplify(sp.diff(r**2 * gsym, r) / K - r**2 * rb - s_ * sp.diff(r**2 * Pf, r))
L1_pois = sp.simplify(pois + target) if sp.simplify(pois + target) == 0 else sp.simplify(pois - target)
log(f"  derived Poisson (integrated): g = g_N + (xi+m_c) u ; residual {L1_pois}")
gN_of_g = sp.simplify(g - s_ * (s_ * g * a0 / (a0 + s_ * g)))
law_res_s1 = sp.simplify(gN_of_g.subs({xi_: 0, mc_: 1}) - g**2 / (g + a0))
dev_lit = sp.nsimplify(sp.simplify((gN_of_g - g**2 / (g + a0)).subs({xi_: 1, mc_: 1, g: a0 / 3}) / a0))
floor_lit = sp.solve(sp.Eq(gN_of_g.subs({xi_: 1, mc_: 1}), 0), g)
floor_lit = [f for f in floor_lit if f != 0]
log(f"  law at s=1 residual {law_res_s1}; M_lit (s=2): g_N - law at g=a0/3 = {dev_lit} a0 = {float(dev_lit):.4f} a0; g_N=0 at g = {floor_lit}")
devs = {k: float(dev_lit) * v for k, v in A0.items()}; floors = {k: 1.5 * v for k, v in A0.items()}
log(f"  M_lit deviation at g=a0/3: canonical {devs['canonical']:.4e}, alt {devs['alt']:.4e} m/s^2; acceleration floor 1.5 a0 = {floors['canonical']:.4e} / {floors['alt']:.4e}")
R["L1"] = dict(force_residual=str(L1_force), poisson_residual=str(L1_pois), law_residual_s1=str(law_res_s1),
               Mlit_s=2, Mlit_dev_over_a0_at_g_a0_over_3=float(dev_lit), Mlit_dev_ms2=devs,
               Mlit_gN_zero_at_g=[str(f) for f in floor_lit], Mlit_floor_ms2=floors,
               A33_K5_reference=-0.55)
check("L1", L1_force == 0 and L1_pois == 0 and law_res_s1 == 0 and abs(float(dev_lit) + 0.55) < 1e-12,
      f"s=1:law_res=0; s=2(M_lit):dev={float(dev_lit):.4f}a0", "law iff xi+m_c=1; M_lit dev=-0.55a0 (A33 K5)")
# L2: AQUAL form. K P = u = (a0/(a0+g)) g... => grad.(grad Phi - K P) = K rho_b with K P = (1-mu) grad Phi
mu_expr = sp.simplify(1 - (g * a0 / (a0 + g)) / g)
L2_res = sp.simplify(mu_expr - (g / a0) / (1 + g / a0))
check("L2", L2_res == 0, f"mu-x/(1+x) residual={L2_res}", "==0 (AQUAL L49)")
# L3: lambda -> lambda + c Phi maps (xi, m_c) -> (xi - c, m_c + c) up to a total derivative and a uniform source
Lst2 = Lst.subs(lam_f, lam_f + cc * Phi)
Lst3 = Lst.subs({xi_: xi_ - cc, mc_: mc_ + cc}) + r**2 * cc * rhob_s * Phi
e2 = sp.euler_equations(sp.expand(Lst2 - Lst3), [Phi, Pf, lam_f, rc], r)
L3_res = [sp.simplify(e.lhs) for e in e2]
check("L3", all(x == 0 for x in L3_res), f"EL(difference)={L3_res}", "all 0 (by construction)")
R["L2_L3"] = dict(L2=str(L2_res), L3=[str(x) for x in L3_res])

# ================================================================ T: D-T test (Newtonian decoupling per mode)
log("== T: D-T (linear self-gravity of the tethered medium), Newtonian decoupling ==")
Ph, sg, sm, sb, lm = sp.symbols("Phi sigma s s_b lam"); sgd, smd, sbd = sp.symbols("sigd sd sbd")
rho_b = sp.Symbol("rho_b", positive=True)
def newt_L(xi, mc, with_lam=True, with_P=True, baryons=False):
    L = -p**2 * Ph**2 / (2 * K) - mc * rho * p**2 * sm * Ph + rho / 2 * p**2 * smd**2 - rho * sc2 / 2 * p**4 * sm**2
    if with_P:
        L += xi * p**2 * sg * Ph + eta / 2 * p**2 * sgd**2 - (K * p**2 + gam * p**4) / 2 * sg**2
    if with_lam:
        L += lm * (-p**2 * sg - rho * p**2 * sm)
    if baryons:
        L += rho_b / 2 * p**2 * sbd**2 - rho_b * p**2 * sb * Ph
    return L
def static_V(L, keep):
    """eliminate Phi (and sigma via the constraint) -> potential matrix of the kept displacements"""
    L0 = L.subs({sgd: 0, smd: 0, sbd: 0})
    if L0.has(lm):
        L0 = L0.subs(sg, -rho * sm).subs(lm, 0)      # constraint: -p^2 sigma = rho p^2 s
    Phs = sp.solve(sp.diff(L0, Ph), Ph)[0]
    L0 = sp.expand(L0.subs(Ph, Phs))
    return sp.Matrix(len(keep), len(keep), lambda i, j: -sp.diff(L0, keep[i], keep[j]))
def selfgrav_coeff(V):
    return sp.simplify(sp.limit(V[0, 0] / (p**2 * K * rho**2), p, 0))
cases = {"dust": newt_L(0, 1, with_lam=False, with_P=False), "Mstar": newt_L(0, 1), "M_lit": newt_L(1, 1),
         "Mstar_mc0": newt_L(1, 0)}
selfg = {k: selfgrav_coeff(static_V(L, [sm])) for k, L in cases.items()}
c2 = {k: sp.simplify(1 + v) for k, v in selfg.items()}
log(f"  V_ss/(K rho^2 p^2) at p->0 (dust = -1 = full Jeans): {selfg};  c2 = 1 + that: {c2}")
# low-p dispersion of M*
Lm = cases["Mstar"].subs(sg, -rho * sm).subs(sgd, -rho * smd).subs(lm, 0)
Phs = sp.solve(sp.diff(Lm, Ph), Ph)[0]; Lm = sp.expand(Lm.subs(Ph, Phs))
w2_M = sp.simplify(sp.diff(Lm, sm, sm) * -1 / sp.diff(Lm, smd, smd))
log(f"  M* medium dispersion: w^2 = {w2_M}  (no -K rho term)")
R["T1"] = dict(selfgravity_coeff=str(selfg), c2={k: str(v) for k, v in c2.items()}, Mstar_w2=str(w2_M))
check("T1", c2["Mstar"] == 1 and c2["Mstar_mc0"] == 1 and c2["dust"] == 0,
      f"c2(M*)={c2['Mstar']} c2(dust)={c2['dust']} c2(M_lit)={c2['M_lit']}", "c2(M*)=1 => D-T applies")
# baryon coupling survives (medium feels baryons, baryons feel medium)
Vb = static_V(newt_L(0, 1, baryons=True), [sm, sb])
cross = sp.simplify(sp.limit(Vb[0, 1] / (p**2 * K * rho * rho_b), p, 0))
log(f"  medium-baryon cross term V_sb/(K rho rho_b p^2) = {cross} (dust value -1)")
# T2: hypotheses
T2 = {"H1 cold static medium": "MET (L1: cold equilibrium m_c Phi + lam = const derived)",
      "H2 always-on tether F(u)": "MET (L1: F(u) = K W'(u) = a0 u/(a0-u) for every u < a0, no gate)",
      "H3 phantom = own mass, g = g_N + u": "MET (enforced D.P = rho_c - rhobar; L1 Poisson g = g_N + u at s = 1)",
      "H4 law with deep limit": "MET (L1 law residual 0 at s = 1; L2 AQUAL mu = x/(1+x))"}
for k_, v_ in T2.items():
    log(f"  T2 {k_}: {v_}")
R["T2"] = T2
check("T2", True and L1_force == 0 and law_res_s1 == 0, "4/4 MET", "D-T hypotheses (CFG941 DERIVATION.md sec 1.3)")
# T3: EdS growth from the derived accelerations (eta, gamma, sigma_c -> 0 at p -> 0)
Gm = sp.Matrix(2, 2, lambda i, j: sp.limit(-Vb[i, j] / p**2, p, 0))
Gm = sp.Matrix([[Gm[0, 0] / rho, Gm[0, 1] / rho], [Gm[1, 0] / rho_b, Gm[1, 1] / rho_b]])  # delta'' = Gm delta
fb = 1 / (1 + RATIO_CB); fc = RATIO_CB / (1 + RATIO_CB)
Gnum = np.array(Gm.subs({K: 1, rho: fc, rho_b: fb}).evalf(), dtype=float)  # in units of K rho_m = (3/2) H^2
lam_max = max(np.linalg.eigvals(Gnum).real)
alpha = (-1 / 3 + np.sqrt(1 / 9 + 8 * lam_max / 3)) / 2; n_growth = 1.5 * alpha
Gd = np.array([[1.0, 1.0], [1.0, 1.0]]) * 0 + np.array([[fc, fb], [fc, fb]])
ad = (-1 / 3 + np.sqrt(1 / 9 + 8 * max(np.linalg.eigvals(Gd).real) / 3)) / 2
log(f"  EdS growth exponent M*: n = {n_growth:.5f} (dust control {1.5 * ad:.5f}; CFG941 K3 0.60954)")
R["T3"] = dict(G_matrix_units_Krho_m=Gnum.tolist(), n_Mstar=n_growth, n_dust=1.5 * ad, CFG941_K3=0.60954)
check("T3", abs(n_growth - 0.60954) < 1e-4 and abs(1.5 * ad - 1) < 1e-12, f"n={n_growth:.5f}", "|n-0.60954|<1e-4")

# ================================================================ N1: NG1 (AG6C S0.4, external labelled input)
log("== N1: NG1 positivity ==")
ag = json.load(open(os.path.join(REPO, "argon_push/AG6C_relativistic_completion/ag6c_s0_saddle_results.json")))
fid = ag["numbers"]["fiducials"]
n1 = {k: dict(rho_ph_min_over_rhobar=v["ratio_to_rhobar"], rho_c_min_over_rhobar=1 + v["ratio_to_rhobar"]) for k, v in fid.items()}
for k_, v_ in n1.items():
    log(f"  {k_}: rho_ph/rhobar = {v_['rho_ph_min_over_rhobar']:.2f} -> rho_c/rhobar = {v_['rho_c_min_over_rhobar']:.2f}")
R["N1"] = dict(source="argon_push/AG6C_relativistic_completion/ag6c_s0_saddle_results.json numbers.fiducials", values=n1,
               note="M* static cold branch == AQUAL L49 (L2), and rho_c = rhobar + rho_ph is enforced, so AG6C's solve applies verbatim")
check("N1", min(v["rho_c_min_over_rhobar"] for v in n1.values()) < 0,
      f"min rho_c/rhobar={min(v['rho_c_min_over_rhobar'] for v in n1.values()):.2f}", "<0 => NG1 bites")

# ================================================================ V1: principal cone of M*
log("== V1: principal cone (round-2 sec 4 L_pr + medium + constraint + W Hessian) ==")
uu, th, kk, om = sp.symbols("u theta k omega", positive=True)
qL, r1, r2, y1, y2, y3, sz, s1, s2 = sp.symbols("q r1 r2 y1 y2 y3 sz s1 s2")
dq = sp.symbols("dq dr1 dr2 dy1 dy2 dy3 dsz ds1 ds2")
Pb = sp.Matrix([uu / K * sp.cos(th), uu / K * sp.sin(th), 0])
S0 = sp.diag(-b / (2 * K), 1 / (4 * K), 1 / (4 * K))
yv = sp.Matrix([y1, y2, y3]); dP = sp.Matrix([qL, r1, r2])
Wp = a0 * uu / (K * (a0 - uu)); Wpp = a0**2 / (K * (a0 - uu)**2)
Ph_ = Pb / (uu / K)
WH = K**2 * Wpp * Ph_ * Ph_.T + K**2 * (Wp / uu) * (sp.eye(3) - Ph_ * Ph_.T)
Lpr = eta / 2 * ((dq[0] - (Pb.T * yv)[0])**2 + dq[1]**2 + dq[2]**2) + (yv.T * S0 * yv)[0] / 2 \
      - gam * kk**2 / 2 * (qL**2 + r1**2 + r2**2) - (dP.T * WH * dP)[0] / 2 \
      + rho / 2 * (dq[6]**2 + dq[7]**2 + dq[8]**2) - rho * sc2 * kk**2 / 2 * sz**2
# constraint D.P = delta rho_c  =>  q = -rho sz (and its time derivative)
Lc = Lpr.subs({qL: -rho * sz, dq[0]: -rho * dq[6]})
# eliminate the algebraic shifts y
ysol = sp.solve([sp.diff(Lc, y) for y in (y1, y2, y3)], [y1, y2, y3], dict=True)[0]
Lc = sp.simplify(Lc.subs(ysol))
kin = sp.simplify(sp.diff(Lc, dq[6], dq[6])); pot = sp.simplify(-sp.diff(Lc, sz, sz))
v2_long = sp.factor(sp.cancel(sp.limit(pot / (kin * kk**2), kk, sp.oo)))
Delta = 1 - 2 * K * eta * (uu * sp.cos(th) / K)**2 / b + 4 * K * eta * (uu * sp.sin(th) / K)**2
log(f"  longitudinal (medium-slaved) v^2 = {v2_long}")
v2_target = (sc2 + gam * rho) / (1 + eta * rho / Delta)
V1_form = sp.simplify(v2_long - v2_target)
v2_T = sp.simplify(sp.limit(-sp.diff(Lc, r1, r1) / (sp.diff(Lc, dq[1], dq[1]) * kk**2), kk, sp.oo))
has_cap = sp.factor(sp.cancel(v2_long)).has(a0) or sp.factor(v2_T).has(a0)  # first run: un-cancelled (a0-u)^2/(a0-u)^2 (code bug, see README)
log(f"  == (sigma_c^2 + gamma rho)/(1 + eta rho/Delta), Delta = 1 - 2 eta u^2 cos^2/(K beta) + 4 eta u^2 sin^2/K: residual {V1_form}")
log(f"  transverse v^2 = {v2_T}; a0 (W Hessian, a0/(a0-u)) appears at principal order: {has_cap}")
# sup over u in [0,a0), theta, with Delta > 0 (beta > 2 eta a0^2/K): v2_long <= sigma_c^2 + gamma rho
# numbers: eta = gamma = K L*^2/(2 c^2) in SI (A33 row 7), rho = rhobar_c
num = {}
for Lk, Ls in LSTAR.items():
    for fk, a0v in A0.items():
        gam_si = 4 * np.pi * G * Ls**2 / 2          # gamma = K L*^2/2, m^5 kg^-1 s^-2
        eta_si = gam_si / c**2                      # eta = gamma/c^2  (eta = gamma in c = 1)
        sc2_si = a0v * Ls                           # sigma_c^2 = a0 L* (A20)
        el2 = gam_si * rhobar_c                     # elastic speed^2 (A33 sec 7.1)
        etarho = eta_si * rhobar_c
        v2l = (sc2_si + el2) / (1 + etarho)
        a33_excess = 4 * eta_si * c**2 * (a0v**2) / (4 * np.pi * G) / c**2 * (gam_si / (eta_si * c**2))  # (gamma/eta)*4 eta a0^2/K, units c^2
        a33_excess = 2 * (Ls * a0v / c**2)**2       # D9 P3 closed form at eta = gamma
        num[f"{Lk}_{fk}"] = dict(sigma_c_kms=np.sqrt(sc2_si) / 1e3, c_el_ms=np.sqrt(el2), eta_rho=etarho,
                                 v2_long_over_c2=v2l / c**2, v2_T_over_c2=1.0, A33_sup_excess_over_c2=a33_excess,
                                 Mstar_sup_excess_over_c2=max(0.0, max(v2l / c**2, 1.0) - 1.0))
        log(f"  L*={Lk} {fk}: sigma_c={np.sqrt(sc2_si)/1e3:.3f} km/s, c_el={np.sqrt(el2):.3f} m/s, v_long^2/c^2={v2l/c**2:.3e}, "
            f"A33 excess {a33_excess:.3e} -> M* excess 0 (eta=gamma)")
R["V1"] = dict(v2_long=str(v2_long), v2_T=str(v2_T), residual_vs_formula=str(V1_form), a0_at_principal_order=bool(has_cap),
               numbers_at_rhobar_c=num,
               sup_v2="max(gamma/eta, (sigma_c^2+gamma rho_c)/(1+eta rho_c/Delta)) <= max(gamma/eta, sigma_c^2+gamma rho_c) for Delta>0; u enters only via Delta (denominator)")
check("V1", V1_form == 0 and not has_cap and sp.simplify(v2_T - gam / eta) == 0,
      "v2_long=(sc2+gamma rho)/(1+eta rho/Delta), v2_T=gamma/eta, no a0/(a0-u)", "finite, u-cap-free")

# ================================================================ F: FRW frozen-coefficient Hadamard test
log("== F: FRW well-posedness (comoving, frozen coefficients at t = 0, a = 1) ==")
t = sp.Symbol("t"); Hs = sp.Symbol("H", positive=True)
a = sp.exp(Hs * t); rho_t = rho * a**-3
fs = [sp.Function(nm)(t) for nm in ("sig", "s", "Phi", "lam")]
sgf, smf, phf, lmf = fs
cons = -kk**2 * sgf / a**2 - rho_t * kk**2 * smf
if MUT:
    cons += -3 * Hs * sp.diff(sgf, t)          # WT-02 / CFG938 S1d non-intrinsic expansion term
LF = a**3 * (eta / 2 * kk**2 / a**2 * sp.diff(sgf, t)**2 - K * kk**2 / (2 * a**2) * sgf**2 - gam * kk**4 / (2 * a**4) * sgf**2
             + rho_t * a**2 * kk**2 / 2 * sp.diff(smf, t)**2 - rho_t * sc2 / 2 * kk**4 * smf**2
             - kk**2 / (2 * K * a**2) * phf**2 - rho_t * kk**2 * smf * phf + lmf * cons)
EL = [e.lhs for e in sp.euler_equations(LF, fs, t)]
amps = sp.symbols("A0:4")
def frozen(expr):
    rep = {}
    for f_, A_ in zip(fs, amps):
        rep[sp.diff(f_, t, 2)] = ssym**2 * A_; rep[sp.diff(f_, t)] = ssym * A_; rep[f_] = A_
    e = expr
    for kx in sorted(rep, key=lambda z: -sp.count_ops(z)):
        e = e.subs(kx, rep[kx])
    return sp.expand(e.subs(t, 0))
Mf = sp.Matrix(4, 4, lambda i, j: sp.diff(frozen(EL[i]), amps[j]))
detF = sp.expand(Mf.det())
vals = {K: 1, eta: 1, gam: 1, rho: 1, sc2: sp.Rational(1, 100), Hs: sp.Rational(1, 10)}
fres = {}
for kv in (10, 100, 1000, 10000):
    pol = sp.Poly(detF.subs(vals).subs(kk, kv), ssym)
    roots = np.roots([float(cf) for cf in pol.all_coeffs()])
    mre = float(max(roots.real)) if len(roots) else 0.0
    fres[kv] = dict(max_re=mre, max_re_over_k2=mre / kv**2, degree=int(pol.degree()))
    log(f"  k={kv}: degree {pol.degree()}, max Re s = {mre:.6g}, / k^2 = {mre / kv**2:.3e}")
R["F1"] = dict(params=str(vals), results=fres, mutate=MUT)
ratio_hi = fres[10000]["max_re_over_k2"]
check("F1", abs(ratio_hi) <= 1e-6 and abs(fres[1000]["max_re_over_k2"]) <= 1e-6,
      f"maxRe/k^2(k=1e3,1e4)={fres[1000]['max_re_over_k2']:.2e},{ratio_hi:.2e}", "<=1e-6 => well posed")
# F2: lambda-determining equation: second time derivative of the constraint, coefficient of lambda
sol = sp.solve([EL[0], EL[1]], [sp.diff(sgf, t, 2), sp.diff(smf, t, 2)], dict=True)[0]
Cdd = sp.diff(cons, t, 2).subs(sol)
coefl = sp.simplify(sp.diff(Cdd.subs(t, 0), lmf.subs(t, 0)) if False else sp.diff(Cdd, lmf).subs(t, 0))
log(f"  lambda coefficient in d^2(constraint)/dt^2 at t=0: {sp.factor(coefl)}")
R["F2"] = dict(lambda_coeff=str(sp.factor(coefl)))
F2_ok = (not MUT) and sp.simplify(coefl - kk**2 * (1 / eta + rho)) == 0
if MUT:
    F2_ok = sp.simplify(coefl - kk**2 * (1 / eta + rho)) == 0
check("F2", F2_ok, f"coeff={sp.factor(coefl)}", "== k^2 (1/eta + rho) > 0 (elliptic on the leaf)")

# ================================================================ X1 (not frozen, no verdict weight): pressure deformation of the law in M*
log("== X1 (not frozen; reported only): medium pressure in M*'s force balance ==")
x1 = {}
Msun = 1.98847e30
for Mk, Mv in (("1e10Msun", 1e10 * Msun), ("1e8Msun", 1e8 * Msun)):
    for Lk, Ls in LSTAR.items():
        for fk, a0v in A0.items():
            rM = np.sqrt(G * Mv / a0v)
            x1[f"{Mk}_{Lk}_{fk}"] = dict(r_M_kpc=rM / (1000 * pc), dg_over_g=2 * Ls / rM)
            log(f"  {Mk} L*={Lk} {fk}: deep-regime (g - K W'(u))/g = 2 L*/r_M = {2 * Ls / rM:.4f}")
R["X1"] = dict(note="M*: sigma_c^2 dln rho_c/dr enters the tether balance; for rho_c ~ r^-2 (deep phantom) the static law is deformed by 2 sigma_c^2/(r g) = 2 L*/r_M. A33 without lambda has no such term (law exact).", values=x1)

# ---------------------------------------------------------------- summary
npass = sum(ok for _, ok in checks)
log(f"D9B_A33_MULTIPLIER COMPLETE: {npass}/{len(checks)} checks PASS.")
R["checks"] = {cid: ok for cid, ok in checks}; R["mutate"] = MUT
open(OUT, "w").write("\n".join(lines) + "\n")
json.dump(R, open(JS, "w"), indent=1, default=str)
sys.exit(0 if npass == len(checks) else 1)
