"""TPA1 items 2-5 and D2: reductions of the two-phase action, each by a hand closed form (route 1) and a direct sympy
variation of the reduced action (route 2).  Criteria: FROZEN_CRITERIA.md (b81c28d00c).  c = 1, K = 4 pi G (geometric units
in the numbers: lengths in m, densities in kg/m^3, K = 4 pi G / c^2, a0 -> a0 / c^2).
TPA1_MUTATE=M1 flips the S' term of the clock charge (the wall pressure must flip direction) and writes
tpa1_reduce_MUTATE_M1.json / .out.
"""
import os, sys, json, math, time, resource
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq

ARM = os.environ.get("TPA1_MUTATE", "")
assert ARM in ("", "M1")
SGN = -1 if ARM == "M1" else 1
HERE = os.path.dirname(os.path.abspath(__file__))
OUTL = []
def P_(s=""):
    print(s, flush=True); OUTL.append(str(s))
t0 = time.time()
RES = {"lane": "TPA1", "items": "2-5, D2", "criteria": "b81c28d00c", "mutate_arm": ARM or None, "checks": {}}
def record(key, ok, **kw):
    RES["checks"][key] = dict(pass_=bool(ok), **kw)
    P_(f"{key}: {'PASS' if ok else 'FAIL'}  " + ", ".join(f"{k}={v}" for k, v in kw.items() if not isinstance(v, (list, dict))))

K, a0, mu, gam = sp.symbols("K a0 mu_K gamma_L", positive=True)
def Wphys(p): return (a0**2 / K) * (-p / a0 - sp.log(1 - p / a0))
def Jphys(A): return (a0**2 / K) * (A / a0 - sp.log(1 + A / a0))

# ======================================================================================== K0: Legendre map with S
A_, p_, S_ = sp.symbols("A p S", positive=True)
stat = sp.diff(S_ * (p_ * A_ - Wphys(K * p_)), p_)
pstar = sp.solve(sp.Eq(sp.simplify(stat / S_), 0), p_)
pstar = [s for s in pstar if s.is_positive is not False]
ps = sp.simplify(pstar[0])
legendre_map_ok = sp.simplify(K * ps - a0 * A_ / (a0 + A_)) == 0
val = sp.simplify(sp.expand_log(S_ * (ps * A_ - Wphys(K * ps)) - S_ * Jphys(A_), force=True))
# mutation: S on P.A only
stat_m = sp.diff(S_ * p_ * A_ - Wphys(K * p_), p_)
pm = [s for s in sp.solve(sp.Eq(stat_m, 0), p_)][0]
mut_map = sp.simplify(K * pm)
mut_differs = sp.simplify(mut_map - a0 * A_ / (a0 + A_)) != 0
record("K0_legendre_with_S", legendre_map_ok and val == 0 and mut_differs,
       stationary_KP=str(sp.simplify(K * ps)), value_residual=str(val), S_on_PA_only_gives=str(mut_map))

# ======================================================================================== item 2: FRW
t = sp.Symbol("t"); a = sp.Function("a")(t); Nl = sp.Function("N")(t); tau = sp.Function("tau")(t)
Sfun = sp.Function("S"); n_ = sp.Symbol("n")
Qf = sp.diff(tau, t) / Nl
nd_of = lambda Q: mu**2 * (Q - 1) / K
LK = lambda Q: mu**2 * (Q - 1)**2 / (2 * K)
# isotropy: A = 0 on the background; the P equation's leaf part S K W'(K|P|) Phat = 0 forces |P| = 0 where S > 0
pp = sp.Symbol("p", nonnegative=True)
Wp_roots = sp.solve(sp.Eq(sp.diff(Wphys(pp), pp), 0), pp)
iso_ok = Wp_roots == [0]
# minisuperspace: N a^3 [L_K(Q) + S(n_d) Lam_law(P=0)], Lam_law(P=0) = -W(0) - gamma F(0); F the blend has F(0) = 0
Lam0 = sp.simplify(-Wphys(sp.Integer(0)) - gam * 0)
Lmini = Nl * a**3 * (LK(Qf) + Sfun(nd_of(Qf)) * Lam0)
rho_mini = sp.simplify(-sp.diff(Lmini, Nl) / a**3).subs(Nl, 1)                  # energy density
clock_mom = sp.simplify(sp.diff(Lmini, sp.diff(tau, t))).subs(Nl, 1)              # conserved: a^3 n_d
I, I0 = sp.symbols("I I0", positive=True)
Qbar = 1 + K * I / (mu**2 * a**3)                                                  # a^3 mu^2 (Q-1)/K = I
rho_bar = sp.simplify(rho_mini.subs(sp.diff(tau, t), Qbar))
w0 = I0 / (4 * mu**2)
rho_rec = (I0 * (1 + w0 / a**3) / (2 * K * a**3)).subs(I0, 2 * K * I)
frw_ok = (sp.simplify(clock_mom.subs(sp.diff(tau, t), Qbar) - I) == 0 and sp.simplify(rho_bar - rho_rec) == 0
          and Lam0 == 0 and not rho_mini.has(Sfun))
record("ITEM2_FRW", iso_ok and frw_ok, Wprime_zero_only_at=str(Wp_roots), Lam_law_at_P0=str(Lam0),
       rho_bar=str(rho_bar), S_in_background=str(rho_mini.has(Sfun)),
       note="background independent of S at every order; change at S = epsilon is exactly zero")

# ======================================================================================== item 3: linear theory
eps = sp.Symbol("epsilon", positive=True)
abar, Qb, f2 = sp.symbols("abar Qbar f2", positive=True)
al = sp.Symbol("alpha"); ze = sp.Symbol("zeta")
dal = sp.symbols("alpha_1:4"); pv = sp.symbols("p_1:4"); dpp = sp.symbols("dp_1:4")    # dp_i = d_i p_i (no sum)
Nn = 1 + eps * al
gam_up = 1 / (abar**2 * (1 + 2 * eps * ze))
sqrtgam = abar**3 * (1 + 2 * eps * ze)**sp.Rational(3, 2)
Qn = Qb / Nn
Ai = [eps * dal[i] / Nn for i in range(3)]
Pi_ = [eps * pv[i] for i in range(3)]
PA = gam_up * sum(Pi_[i] * Ai[i] for i in range(3))
Pmod2 = gam_up * sum(Pi_[i]**2 for i in range(3))
PiDiv = eps * gam_up * sum(dpp)                      # leading Pi = D_i P^i
Fgen = f2 * PiDiv**2 / 2                             # generic F with F(0) = F'(0) = 0; the adopted blend has f2 = 0
Wser = sp.series(Wphys(pp), pp, 0, 4).removeO()
Wlaw = Wser.subs(pp, K * sp.sqrt(Pmod2))
Llaw = Nn * sqrtgam * Sfun(nd_of(Qn)) * (PA - Wlaw - gam * Fgen)
L2law = sp.simplify(sp.diff(Llaw, eps, 2).subs(eps, 0) / 2)
has_Sprime = L2law.has(sp.Derivative) or any(isinstance(x, sp.Subs) for x in sp.preorder_traversal(L2law))
Sb = Sfun(mu**2 * (Qb - 1) / K)
target = Sb * abar * (sum(pv[i] * dal[i] for i in range(3)) - K * sum(pv[i]**2 for i in range(3)) / 2) \
    - Sb * gam * f2 * sum(dpp)**2 / (2 * abar)
lin_a = sp.simplify(L2law - target) == 0
# eliminate p (blend: f2 = 0): p_i = alpha_i / K
L2el = sp.simplify(target.subs(f2, 0).subs({pv[i]: dal[i] / K for i in range(3)}))
lin_c1 = sp.simplify(L2el - Sb * abar * sum(d**2 for d in dal) / (2 * K)) == 0
# dust sector: alpha^2 coefficient of N sqrt(gamma) L_K(Qbar/N)
Ldust = Nn * sqrtgam * LK(Qn)
L2dust = sp.expand(sp.diff(Ldust, eps, 2).subs(eps, 0) / 2)
c_alpha2 = sp.simplify(L2dust.coeff(al, 2))
lin_c2 = sp.simplify(c_alpha2 - abar**3 * mu**2 * Qb**2 / (2 * K)) == 0
kk = sp.Symbol("k", positive=True)
shifted = sp.simplify((c_alpha2 + Sb * abar * kk**2 / (2 * K)) * 2 * K / abar**3)
record("ITEM3_quadratic_action", lin_a and lin_c1 and lin_c2 and not has_Sprime,
       S_prime_terms_at_second_order=str(has_Sprime), law_L2=str(L2law), dust_alpha2_coeff=str(c_alpha2),
       alpha2_total_times_2K_over_a3=str(shifted),
       note="Sbar = 0: the law drops out at second order; Sbar = eps: mu^2 Qbar^2 -> mu^2 Qbar^2 + eps k^2/a^2")

# ---- (d) dispersion relation, route 2: expand the covariant non-GR Lagrangian in Newtonian gauge with a Stuckelberg clock,
# at exact rational parameter values (K, mu_K, eps, nbar, k), so every Hessian entry is an exact rational.
Ph, Ps, pt, px, ptt, ptx, pxx, pP = sp.symbols("Phi Psi pi_t pi_x pi_tt pi_tx pi_xx pP")
Phx, Psx, Pht, Pst = sp.symbols("Phi_x Psi_x Phi_t Psi_t")
JL = [Ph, Ps, pt, px, ptt, ptx, pxx, pP, Phx, Psx, Pht, Pst]
def Lnon_at(Kv, muv, epv, nbv):
    gtt = -(1 + 2 * Ph); gxx = 1 - 2 * Ps
    QB = 1 + Kv * nbv / muv**2
    dtau = [QB + pt, px]
    Q2 = -(dtau[0]**2 / gtt + dtau[1]**2 / gxx)
    Qx = sp.sqrt(Q2)
    def Dt(expr):
        return sp.diff(expr, pt) * ptt + sp.diff(expr, px) * ptx + sp.diff(expr, Ph) * Pht + sp.diff(expr, Ps) * Pst
    def Dx(expr):
        return sp.diff(expr, pt) * ptx + sp.diff(expr, px) * pxx + sp.diff(expr, Ph) * Phx + sp.diff(expr, Ps) * Psx
    dl = [Dt(Q2) / (2 * Q2), Dx(Q2) / (2 * Q2)]
    n_low = [-dtau[0] / Qx, -dtau[1] / Qx]
    ginv = [1 / gtt, 1 / gxx]
    n_up = [ginv[0] * n_low[0], ginv[1] * n_low[1]]
    Px_ = pP
    Pt_ = -n_up[1] * Px_ / n_up[0]                       # n.P = 0
    Pup = [ginv[0] * Pt_, ginv[1] * Px_]
    PA2 = -(Pup[0] * dl[0] + Pup[1] * dl[1])
    Pm2 = Pup[0] * Pt_ + Pup[1] * Px_
    sqrtg = sp.sqrt(-gtt * gxx**3)
    return sqrtg * (muv**2 * (Qx - 1)**2 / (2 * Kv) + epv * (PA2 - Kv * Pm2 / 2))   # W to quadratic order: K|P|^2/2
w, k = sp.symbols("omega k", positive=True)
jets = {"Phi": [(Ph, 1), (Phx, sp.I * k), (Pht, -sp.I * w)], "Psi": [(Ps, 1), (Psx, sp.I * k), (Pst, -sp.I * w)],
        "pi": [(pt, -sp.I * w), (px, sp.I * k), (ptt, -w**2), (ptx, w * k), (pxx, -k**2)], "p": [(pP, 1)]}
fields = list(jets)
def omega2_route2(Kv, muv, epv, nbv, kv):
    L1 = Lnon_at(Kv, muv, epv, nbv)
    zero = {j: 0 for j in JL}
    first = {ja: sp.diff(L1, ja) for ja in JL}
    HESS = {}
    for i_, ja in enumerate(JL):
        for jb in JL[i_:]:
            HESS[(ja, jb)] = HESS[(jb, ja)] = sp.nsimplify(sp.diff(first[ja], jb).subs(zero))
    L2g = (Psx**2 - 2 * Phx * Psx) / (2 * Kv)                          # GR, Newtonian quasi-static (standard)
    for ja in JL:
        for jb in JL:
            HESS[(ja, jb)] += sp.diff(L2g, ja, jb)
    flds = fields if epv != 0 else [f for f in fields if f != "p"]   # at eps = 0 the P row vanishes identically
    if epv == 0:
        assert all(HESS[(pP, jb)] == 0 for jb in JL), "P must drop out at S = 0"
    Mx = sp.zeros(len(flds), len(flds))
    for i, fi in enumerate(flds):
        for j, fj in enumerate(flds):
            Mx[i, j] = sp.expand(sum(sp.conjugate(ci) * HESS[(si, sj)] * cj for (si, ci) in jets[fi] for (sj, cj) in jets[fj]))
    det = sp.expand(Mx.det().subs(k, kv))
    roots = sp.Poly(det, w).nroots(n=40, maxsteps=200)
    w2s = sorted({sp.re(r**2) for r in roots if abs(r) > 1e-30}, key=lambda z: abs(z))
    return w2s, sp.Poly(det, w).degree()
Kv0, mu0, nb0 = sp.Rational(1, 2), sp.Rational(7, 10), sp.Rational(1, 10**8)
disp_rows = []
ok_disp = True
for epv in (sp.Integer(0), sp.Rational(3, 10), sp.Integer(1)):
    for kv in (sp.Rational(1, 10), sp.Integer(1), sp.Integer(10)):
        rels = []
        for nbv in (nb0, nb0 / 2):
            w2s, deg = omega2_route2(Kv0, mu0, epv, nbv, kv)
            r1 = -Kv0 * nbv * (1 - kv**2 / (mu0**2 + epv * kv**2))
            best = min(w2s, key=lambda z: abs(z - r1)) if w2s else sp.nan
            rels.append(float(abs(best - r1) / abs(r1)))
            if nbv == nb0:
                row = dict(eps=str(epv), k=str(kv), omega2_route2=float(best), omega2_route1=float(r1), rel=rels[0],
                           omega_degree=deg, all_nonzero_omega2=[float(z) for z in w2s])
        row["rel_at_half_nbar"] = rels[1]; row["ratio"] = rels[0] / rels[1] if rels[1] > 0 else float("inf")
        disp_rows.append(row)
        ok_disp &= rels[0] <= 1e-5 and 1.8 <= row["ratio"] <= 2.2   # agreement at first order in nbar: residual is O(nbar)
eps_s, k_s, nb_s, mu_s, K_s = sp.symbols("varepsilon k nbar mu_K K", positive=True)
r1sym = -K_s * nb_s * (1 - k_s**2 / (mu_s**2 + eps_s * k_s**2))
ka_e1 = sp.simplify(r1sym.subs(eps_s, 1) - (-K_s * nb_s / (1 + k_s**2 / mu_s**2))) == 0
ka_e0 = sp.simplify(r1sym.subs(eps_s, 0) - (-K_s * nb_s * (1 - k_s**2 / mu_s**2))) == 0
RES["dispersion_rows"] = disp_rows
for r_ in disp_rows:
    P_(f"  eps {r_['eps']:>5s} k {r_['k']:>5s}: omega^2 route 2 {r_['omega2_route2']:+.12e}  route 1 {r_['omega2_route1']:+.12e}  rel {r_['rel']:.2e} (ratio at nbar/2: {r_['ratio']:.3f})")
record("ITEM3_dispersion", ok_disp and ka_e1 and ka_e0, route1="omega^2 = -K nbar [1 - k^2/(mu_K^2 + eps k^2)] (first order in nbar)",
       nbar=float(nb0), max_rel=max(r_["rel"] for r_ in disp_rows), KA_eps1_RK04=ka_e1, KA_eps0_isolated_fluid=ka_e0)

# ---- GAL1 bound on epsilon
MPC = 3.0856775814913673e22
f_allow = 0.01968
q_max = 1.5 * f_allow / (1 - f_allow)
gal1 = {}
for foot, muK in (("canonical", 8.890e6), ("alt", 8.889e6)):
    kmax = 1.0
    corr_at_eps1 = (kmax / muK)**4 / (1 - (kmax / muK)**2)
    eps_bound = q_max / corr_at_eps1
    mu_bite = kmax / q_max**0.25                       # eps = 1 excluded only if mu_K below about this (Mpc^-1)
    gal1[foot] = dict(mu_K_Mpc=muK, q_max=q_max, first_correction_at_eps1_kmax1=corr_at_eps1,
                      eps_bound=eps_bound, vacuous=bool(eps_bound > 1), mu_K_below_which_eps1_bites_Mpc=mu_bite)
RES["gal1_bound"] = gal1
P_(f"GAL1 bound: q_max {q_max:.5f}; first correction at eps 1, k 1/Mpc: {gal1['canonical']['first_correction_at_eps1_kmax1']:.3e} "
   f"(canonical); eps bound {gal1['canonical']['eps_bound']:.3e} -> vacuous; bites only for mu_K < {gal1['canonical']['mu_K_below_which_eps1_bites_Mpc']:.3f} /Mpc")

# ======================================================================================== item 4: static weak field
x = sp.Symbol("x")
N = sp.Function("N")(x); Sx = sp.Function("S")
Qinf = sp.Symbol("Q_inf", positive=True)
rhob = sp.Function("rho_b")(x)
Qs = Qinf / N
Astat = sp.diff(N, x) / N                                                  # A_x = d ln N (static clock)
pon = a0 * Astat / (K * (a0 + Astat))                                       # Legendre map (field along +x)
# ---- 4b route A, exact: covariant divergence of the switched law stress in the static planar metric
tt, yy, zz = sp.symbols("tt yy zz")
coords = [tt, x, yy, zz]
gmat = sp.diag(-N**2, 1, 1, 1); ginvm = gmat.inv()
def christ(gm, gi):
    G_ = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for b in range(4):
        for a_ in range(4):
            for c in range(4):
                G_[b][a_][c] = sp.simplify(sum(gi[b, d] * (sp.diff(gm[d, c], coords[a_]) + sp.diff(gm[d, a_], coords[c])
                                                        - sp.diff(gm[a_, c], coords[d])) for d in range(4)) / 2)
    return G_
Gam = christ(gmat, ginvm)
pfx = sp.Function("p")(x)
def law_stress(Sval, SQval, pfun, include_SQ):
    l = sp.log(Qs); dlv = [sp.diff(l, c) for c in coords]
    nlow = [-N, 0, 0, 0]
    Plow = [0, pfun, 0, 0]; Pup = [ginvm[i, i] * Plow[i] for i in range(4)]
    sg = N
    LA = -sum(Pup[i] * dlv[i] for i in range(4)) - Wphys(K * pfun)
    divSP = sp.diff(sg * Sval * pfun, x) / sg
    Tm = sp.zeros(4, 4)
    for m in range(4):
        for nn in range(4):
            Tm[m, nn] = (gmat[m, nn] * Sval * LA + Sval * (Plow[m] * dlv[nn] + Plow[nn] * dlv[m])
                         + divSP * nlow[m] * nlow[nn]
                         + (Sval * K * sp.diff(Wphys(pp), pp).subs(pp, K * pfun) * Plow[m] * Plow[nn] / pfun if pfun != 0 else 0))
            if include_SQ:
                Tm[m, nn] += Qs * SQval * LA * nlow[m] * nlow[nn]
    return Tm, LA
def cov_div_x(Tm):
    # nabla^m T_{m x} = g^{ma} (d_a T_{mx} - Gam^b_{am} T_{bx} - Gam^b_{ax} T_{mb})
    tot = 0
    for m in range(4):
        for a_ in range(4):
            if ginvm[m, a_] == 0: continue
            cov = sp.diff(Tm[m, 1], coords[a_]) - sum(Gam[b][a_][m] * Tm[b, 1] for b in range(4)) \
                - sum(Gam[b][a_][1] * Tm[m, b] for b in range(4))
            tot += ginvm[m, a_] * cov
    return tot
# held argument: S = S(x)
Sh = Sx(x)
Th, LAh = law_stress(Sh, 0, pfx, False)
divh = cov_div_x(Th)
resid_held = sp.simplify((divh - LAh * sp.diff(Sh, x)).subs(pfx, pon).doit())
# slaved argument: S = S(Q(x)), with the Q dS/dQ Lam n n term
Qsym = sp.Symbol("Qs", positive=True)
SofQ = sp.Function("Sq")
Ss = SofQ(Qs); SQs = sp.diff(SofQ(Qsym), Qsym).subs(Qsym, Qs)
Tsl, LAs = law_stress(Ss, SQs, pfx, True)
divs = cov_div_x(Tsl)
resid_slaved = sp.simplify(divs.subs(pfx, pon).doit())
record("ITEM4b_routeA_noether_force", resid_held == 0 and resid_slaved == 0,
       held_residual=str(resid_held), slaved_residual=str(resid_slaved),
       note="held: nabla^m T^L_mx = Lam_law dS/dx exactly on the P shell; slaved (S = S(Q)): = 0 exactly")
# on-shell leaf stress T^L_xx = -S W(K p)
Txx_on = sp.simplify((Th[1, 1] + Sh * Wphys(K * pfx)).subs(pfx, pon))
record("ITEM4b_leaf_stress", sp.simplify(Txx_on) == 0, Txx_plus_SW_on_shell=str(Txx_on))

# ---- the wall identity from the covariant leaf stress: Pi_xx = E^2/(2K) - S W(K|P|); jump at fixed displacement
u, y = sp.symbols("u y", positive=True)
Wu = u - sp.log(1 + u) - u**2 / (2 * (1 + u)**2)
E_in = a0 * u; Kp_in = a0 * u / (1 + u)
Pi_in = E_in**2 / (2 * K) - Wphys(Kp_in)
yv = u**2 / (1 + u)
Pi_out = (a0 * yv)**2 / (2 * K)
jump = sp.simplify(sp.expand_log((Pi_in - Pi_out) * K / a0**2 - Wu, force=True))
# d Pi/dS at fixed displacement: Pi(S, E) with D = E (1 - S/(1+E/a0)) fixed; dPi/dE|_S * dE/dS + dPi/dS = J
Ssym, Esym = sp.symbols("S_ E_", positive=True)
Dfix = Esym * (1 - Ssym / (1 + Esym / a0))
Kp_S = a0 * Esym / (a0 + Esym)
PiS = Esym**2 / (2 * K) - Ssym * Wphys(Kp_S)
dEdS = -sp.diff(Dfix, Ssym) / sp.diff(Dfix, Esym)
dPi = sp.simplify(sp.diff(PiS, Esym) * dEdS + sp.diff(PiS, Ssym))
# momentum balance: the carrier receives -dPi/dx... d Pi_xx / dS along fixed D equals + J? sign recorded
dPi_minus_J = sp.simplify(sp.expand_log(dPi - Jphys(Esym), force=True))
record("ITEM4b_wall_identity_symbolic", jump == 0 and dPi_minus_J == 0, jump_minus_W=str(jump),
       dPi_dS_fixed_D_minus_J=str(dPi_minus_J))

# ---- numbers: route A (integral of Lam_law dS across the wall) and route B (clock charge's S' term), vs swt1.json
SW = json.load(open(os.path.join(HERE, "..", "SWT1_switch_theorems", "swt1.json")))
G, MS, PC, CL = 6.6743e-11, 1.98847e30, 3.0856775814913673e16, 2.99792458e8
KPC = 1e3 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
def u_of(S, yv_):
    """field (units a0) at switch value S for displacement y: (1 - S/(1+u)) u = y."""
    return brentq(lambda uu: (1 - S / (1 + uu)) * uu - yv_, 0.0, yv_ + 2.0, xtol=1e-300, rtol=1e-15)
def Jhat(uu): return uu - math.log1p(uu)
def wall_routeA(yv_):
    """force per area / (a0^2/K): integral over the wall of the law sector's force density -Lam_law dS, S: 1 -> 0."""
    return quad(lambda S: Jhat(u_of(S, yv_)), 0.0, 1.0, epsabs=0, epsrel=1e-13, limit=200)[0]
def wall_routeB(yv_, sgn=1):
    """the clock charge's S' term N_S = S_Q Lam_law gives the force density on the dust f = -N_S dQ/dx. Integrate it over
    an explicit logistic profile S(Q) = 1/(1 + exp((Q - 1)/w)) in Q (any width; the dust density rises outward), at fixed
    displacement y: force per area = -integral S_Q(Q) J(u(S(Q), y)) dQ.  sgn = -1 is the M1 arm (term flipped)."""
    wq = 1.0
    def SQ(Q):
        z = (Q - 1.0) / wq
        return -math.exp(-abs(z)) / (wq * (1.0 + math.exp(-abs(z))) ** 2)
    def Sof(Q):
        z = (Q - 1.0) / wq
        return 1.0 / (1.0 + math.exp(z)) if z < 0 else math.exp(-z) / (1.0 + math.exp(-z))
    f = lambda Q: -sgn * SQ(Q) * Jhat(u_of(Sof(Q), yv_))
    val = 0.0
    for lo, hi in ((-60.0, -10.0), (-10.0, 0.0), (0.0, 10.0), (10.0, 60.0)):
        val += quad(f, 1.0 + lo * wq, 1.0 + hi * wq, epsabs=0, epsrel=1e-13, limit=400)[0]
    return val
def Wclosed(uu): return uu - math.log1p(uu) - uu * uu / (2 * (1 + uu) ** 2)
def u_in(yv_): return 0.5 * yv_ + math.sqrt(0.25 * yv_ * yv_ + yv_)
rows = []
for r in SW["KA"]["KA_W1"]["rows"]:
    yv_ = r["y"]
    A_ = wall_routeA(yv_); B_ = wall_routeB(yv_, SGN)
    rows.append(dict(y=yv_, swt1_closed=r["closed"], routeA=A_, routeB=B_, relA=abs(A_ / r["closed"] - 1),
                     relB=abs(B_ / r["closed"] - 1), outward_B=bool(B_ > 0)))
okA = all(rw["relA"] <= 1e-9 for rw in rows)
okB = all(rw["relB"] <= 1e-9 and rw["outward_B"] for rw in rows)
RES["wall_KA_W1"] = rows
if ARM == "M1":
    flips = all(rw["routeB"] < 0 for rw in rows)
    record("M1_wall_pressure_flips", flips, routeB_signs=str([("in" if rw["routeB"] < 0 else "out") for rw in rows]))
else:
    record("ITEM4b_vs_swt1_KA_W1", okA and okB, max_relA=max(rw["relA"] for rw in rows),
           max_relB=max(rw["relB"] for rw in rows), all_outward=all(rw["outward_B"] for rw in rows))
# KA_W3: Plummer sphere forces 4 pi R^2 p_wall (canonical in swt1.json; alt against the transcribed closed form)
def plummer_force(Rk, a0v, route):
    Mp, b = 1e11 * MS, 3.0 * KPC
    R = Rk * KPC
    Mb = Mp * R**3 / (R * R + b * b) ** 1.5
    yv_ = G * Mb / R**2 / a0v
    Wv = wall_routeA(yv_) if route == "A" else wall_routeB(yv_, SGN)
    return 4 * math.pi * R * R * a0v * a0v / (4 * math.pi * G) * Wv, 4 * math.pi * R * R * a0v * a0v / (4 * math.pi * G) * Wclosed(u_in(yv_))
w3rows = []
for r in SW["KA"]["KA_W3"]["rows"]:
    fA, _ = plummer_force(r["R_kpc"], A0["canonical"], "A"); fB, _ = plummer_force(r["R_kpc"], A0["canonical"], "B")
    fAalt, cfalt = plummer_force(r["R_kpc"], A0["alt"], "A"); fBalt, _ = plummer_force(r["R_kpc"], A0["alt"], "B")
    w3rows.append(dict(R_kpc=r["R_kpc"], swt1_closed_canonical=r["closed"], routeA_canonical=fA, routeB_canonical=fB,
                       relA=abs(fA / r["closed"] - 1), relB=abs(fB / r["closed"] - 1),
                       alt_closed=cfalt, routeA_alt=fAalt, routeB_alt=fBalt,
                       relA_alt=abs(fAalt / cfalt - 1), relB_alt=abs(fBalt / cfalt - 1)))
RES["wall_KA_W3"] = w3rows
if not ARM:
    okw3 = all(max(r_["relA"], r_["relB"], r_["relA_alt"], r_["relB_alt"]) <= 1e-9 for r_ in w3rows)
    record("ITEM4b_vs_swt1_KA_W3_both_footings", okw3,
           max_rel=max(max(r_["relA"], r_["relB"], r_["relA_alt"], r_["relB_alt"]) for r_ in w3rows))
    for r_ in w3rows:
        P_(f"  Plummer R {r_['R_kpc']:6.1f} kpc: force canonical {r_['routeA_canonical']:.10e} (swt1 {r_['swt1_closed_canonical']:.10e}); "
           f"alt {r_['routeA_alt']:.10e}")

# ---- 4c compensation from the covariant energy density (held switch, mu_K = 0): M_eff = M_b + 4 pi r^2 S P_r
def ka_cp3(a0v):
    Mb, R = 1e10 * MS, 300 * KPC; wdt = 0.02 * R; worst = 0.0
    def Meff(r):
        S = 0.5 * (1 - math.tanh((r - R) / wdt)); yv_ = G * Mb / r ** 2 / a0v
        # Gauss with the covariant energy density div(S P): g = G M_b / r^2 + 4 pi G S P_r, K P_r = g/(1 + g/a0)
        uu = brentq(lambda uu: uu - S * uu / (1 + uu) - yv_, 0.0, 10 * (yv_ + math.sqrt(yv_)) + 2.0, xtol=1e-300, rtol=1e-15)
        g = a0v * uu
        Pr = g / (1 + g / a0v) / (4 * math.pi * G)
        return Mb + 4 * math.pi * r * r * S * Pr, g * r * r / G
    for r in np.linspace(1.2 * R, 3 * R, 40):
        m_dens, m_g = Meff(r)
        worst = max(worst, abs(m_dens / Mb - 1), abs(m_g / Mb - 1))
    m_in, m_in_g = Meff(0.5 * R)
    return worst, m_in / Mb, m_in_g / Mb
if not ARM:
    cp = {}
    for foot in ("canonical", "alt"):
        wv, rin, rin_g = ka_cp3(A0[foot]); cp[foot] = dict(exterior_excess=wv, interior_ratio=rin, interior_ratio_from_g=rin_g)
    rel_in = abs(cp["canonical"]["interior_ratio"] / SW["KA"]["KA_CP3"]["interior_Meff_over_Mb"] - 1)
    okcp = cp["canonical"]["exterior_excess"] <= 1e-6 and cp["alt"]["exterior_excess"] <= 1e-6 and rel_in <= 1e-9
    RES["compensation"] = cp
    record("ITEM4c_compensation", okcp, exterior_excess_canonical=cp["canonical"]["exterior_excess"],
           exterior_excess_alt=cp["alt"]["exterior_excess"], interior_canonical=cp["canonical"]["interior_ratio"],
           swt1_interior=SW["KA"]["KA_CP3"]["interior_Meff_over_Mb"], rel_interior=rel_in)

# ---- 4a static reduction, route 1 (covariant energy density + Poisson) vs route 2 (static Lagrangian), Newtonian order
ev = sp.Symbol("ev", positive=True)        # bookkeeping: Phi, rho_b, a0 ~ ev; a slaved switch varies over dn_d ~ ev
phi = sp.Function("phi")(x); rh = sp.Function("rh")(x)
sc0, sc1, sc2, sc3 = sp.symbols("s0:4")
Shat = lambda n: sc0 + sc1 * n + sc2 * n**2 + sc3 * n**3   # general for a local identity: only S, S', S'' enter
al0 = sp.Symbol("alpha0", positive=True)
Nv = 1 + ev * phi
Qv = 1 / Nv                                 # static clock, Q_inf = 1 (no dust where Phi = 0)
nd_v = mu**2 * (Qv - 1) / K
a0e = ev * al0
Av = sp.diff(Nv, x) / Nv
Jv = (a0e**2 / K) * (Av / a0e - sp.log(1 + Av / a0e))
def EL1d(Lx, f):
    return sp.diff(Lx, f) - sp.diff(sp.diff(Lx, sp.diff(f, x)), x)
def route2_static(Sexpr):
    Lst = -(sp.diff(ev * phi, x))**2 / (2 * K) - ev * rh * ev * phi + Nv * LK(Qv) + Nv * Sexpr * Jv
    return sp.series(EL1d(Lst, phi) / ev**2, ev, 0, 1).removeO()
def route1_static(Sexpr, dSdQ):
    pv_ = a0e * Av / (K * (a0e + Av))                       # Legendre map on the P shell
    Wl = lambda pq: (a0e**2 / K) * (-pq / a0e - sp.log(1 - pq / a0e))      # W with the scaled a0 (run-1 bug fixed)
    rho_law = Sexpr * Wl(K * pv_) + sp.diff(Sexpr * pv_, x) + Qv * dSdQ * (pv_ * Av - Wl(K * pv_))
    rho_dust = (mu**2 / (2 * K)) * (Qv**2 - 1)
    resid = sp.diff(ev * phi, x, 2) / K - (ev * rh + rho_dust + rho_law)
    return sp.series(resid / ev, ev, 0, 1).removeO()
uu_t = sp.diff(phi, x) / al0
Sheld = sp.Function("Sh")(x)
r2h = sp.simplify(route2_static(Sheld)); r1h = sp.simplify(route1_static(Sheld, 0))
def z(e_): return sp.simplify(sp.expand_log(sp.expand(e_), force=True)) == 0
held_agree = z(r2h - r1h)
target_held = sp.diff((1 - Sheld / (1 + uu_t)) * sp.diff(phi, x), x) + mu**2 * phi - K * rh
held_target = z(K * r1h - target_held)
qq = sp.Symbol("qq", positive=True)
Ssl = Shat(nd_v / ev)
dSdQ_sl = sp.diff(Shat(mu**2 * (qq - 1) / (K * ev)), qq).subs(qq, Qv)
r2s = sp.simplify(route2_static(Ssl)); r1s = sp.simplify(route1_static(Ssl, dSdQ_sl))
sl_agree = z(r2s - r1s)
nloc = -mu**2 * phi / K
nsym = sp.Symbol("n_")
Shp = sp.diff(Shat(nsym), nsym).subs(nsym, nloc)
Jn = (al0**2 / K) * (uu_t - sp.log(1 + uu_t))
target_sl = sp.diff((1 - Shat(nloc) / (1 + uu_t)) * sp.diff(phi, x), x) + mu**2 * phi - K * rh - mu**2 * Shp * Jn
sl_target = z(K * r1s - target_sl)
sl_target2 = z(K * r2s - target_sl)
record("ITEM4a_static_reduction", held_agree and held_target and sl_agree and sl_target and sl_target2,
       held_routes_agree=held_agree, held_equals_SWT1_class_plus_muK=held_target, slaved_routes_agree=sl_agree,
       slaved_equals_SWT1_operator_plus_layer=sl_target, slaved_route2_equals_target=sl_target2,
       slaved_extra_term="mu_K^2 S'(n_d) J(|grad Phi|) on the source side, n_d = -mu_K^2 Phi / K (a layer where S varies)")

# ======================================================================================== item 5
uS, yS, gS, gN = sp.symbols("u y g g_N", positive=True)
law_ok = sp.simplify(((uS**2 - yS * (1 + uS)).subs({uS: gS / a0, yS: gN / a0}) * a0**2) - (gS**2 - gN * (gS + a0))) == 0
# S = 0 phase: S multiplies every term that carries a0 (W) or the law's fields, so the S = 0 Lagrangian has no a0
sS, PAs, Pms, Fs, nPs, Qs_, lam_s = sp.symbols("s PA Pm F nP Q lam")
Lred = LK(Qs_) + sS * (PAs - Wphys(K * Pms) - gam * Fs) + lam_s * nPs
a0_absent = (a0 not in Lred.subs(sS, 0).free_symbols) and (a0 in Lred.free_symbols)
# static clock monotonicity: d/dN S(n_d(N)) = S'(n) * (-mu^2 Q_inf / (K N^2)), >= 0 for S' <= 0
Nn_ = sp.Symbol("N", positive=True)
mono = sp.diff(Sfun(mu**2 * (Qinf / Nn_ - 1) / K), Nn_)
Sp_at = sp.diff(Sfun(nsym), nsym).subs(nsym, mu**2 * (Qinf / Nn_ - 1) / K)
mono_ok = sp.simplify(mono - Sp_at * (-mu**2 * Qinf / (K * Nn_**2))) == 0
record("ITEM5_phases", law_ok and a0_absent and mono_ok, S1_spherical_law=law_ok, S0_a0_absent=a0_absent,
       static_clock_dS_dN_over_Sprime=str(sp.simplify(-mu**2 * Qinf / (K * Nn_**2))))
# numbers: how far a static clock can stay in the S = 1 phase
MPCm = MPC
Kgeo = 4 * math.pi * G / CL**2
I0geo = 4.037e-8 / MPCm**2
rho_mean = I0geo / (2 * Kgeo)
dphi = {}
for foot, muK in (("canonical", 8.890e6), ("alt", 8.889e6)):
    mug = muK / MPCm
    dphi[foot] = {f"{m:g}x": Kgeo * m * rho_mean / mug**2 for m in (1, 1e3, 1e6)}
RES["static_clock_phase_width"] = dict(rho_mean_kg_m3=rho_mean, dPhi_over_c2_max=dphi,
                                       note="a static clock stays at n_d <= n_1 only across a potential difference K n_1/mu_K^2 (units c^2)")
P_(f"static clock: mean cold density {rho_mean:.3e} kg/m^3; max potential range (c^2 units) in the S = 1 phase at n_1 = 1, 1e3, 1e6 x mean: "
   + ", ".join(f"{v:.2e}" for v in dphi["canonical"].values()) + " (canonical)")

# ======================================================================================== D2: S reads N_2 = n_d + Pi
pD = sp.Function("pD")(x); Af = sp.Function("A")(x); ndf = sp.Function("nd")(x); S2 = sp.Function("S2")
LamD = pD * Af - Wphys(K * pD)
LD2 = S2(ndf + sp.diff(pD, x)) * LamD
EL_p = sp.simplify(EL1d(LD2, pD))
# route 1 (hand): S (A - K W'(K p)) - d/dx [ S'(N_2) Lam ] = 0
Nn2 = ndf + sp.diff(pD, x)
S2p = sp.diff(S2(nsym), nsym).subs(nsym, Nn2)
hand = S2(Nn2) * (Af - K * sp.diff(Wphys(pp), pp).subs(pp, K * pD)) - sp.diff(S2p * LamD, x)
d2_ok = sp.simplify(sp.expand(EL_p - hand)) == 0
record("D2_P_equation", d2_ok, P_equation=("S(N_2) (A - K W'(K|P|)) = d/dx [ S'(N_2) (P A - W) ];"
                                           " the Legendre map is broken where S' != 0 and P obeys a 2nd-order equation in space"))

# ======================================================================================== labels and output
RES["seconds"] = round(time.time() - t0, 1)
RES["peak_rss_GB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 3)
RES["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
suffix = f"_MUTATE_{ARM}" if ARM else ""
with open(os.path.join(HERE, f"tpa1_reduce{suffix}.json"), "w") as fh:
    json.dump(RES, fh, indent=1, default=str)
P_(f"runtime {RES['seconds']} s, peak RSS {RES['peak_rss_GB']} GB")
P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
with open(os.path.join(HERE, f"tpa1_reduce{suffix}.out"), "w") as fh:
    fh.write("\n".join(OUTL) + "\n")

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
