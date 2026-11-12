#!/usr/bin/env python3
"""BI1 (FROZEN_CRITERIA.md 91e81dcd76): gate B0, covariant consistency of variant R's switched coupling f_clus(Xi), both carriers.
(i) f in the matter action: sympy Euler-Lagrange of L = -f(x) m c^2 sqrt(1 + 2 Phi/c^2 - v^2/c^2), weak field, to O(1/c^0) in the force;
    the extra force -c^2 grad ln f vs g_N (L* M_b 8e10) at 0.1-3 Mpc; what Xi's stress tensor must carry. MUTATE M1: f constant.
(ii) f in the active mass only: sympy pair forces and centre-of-mass self-acceleration; nabla(f T) with T = diag(rho c^2, rho sigma^2 x3):
    the static-dust escape and the non-vanishing terms, in numbers. MUTATE M2: f = 1.
    python3 bi1.py   -> bi1.json / bi1.out
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, json, math
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); CRIT = "91e81dcd76"; L = []
def P(s): print(s, flush=True); L.append(str(s))
RES = dict(criteria=CRIT, note="TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed")
# ---------------- (i) symbolic
t, m, c = sp.symbols("t m c", positive=True); x = sp.Function("x")(t); f = sp.Function("f"); Phi = sp.Function("Phi")
v = sp.diff(x, t); Lag = -f(x) * m * c ** 2 * sp.sqrt(1 + 2 * Phi(x) / c ** 2 - v ** 2 / c ** 2)
EL = sp.diff(sp.diff(Lag, v), t) - sp.diff(Lag, x)                          # = 0
a = sp.symbols("a"); EL_a = EL.subs(sp.diff(x, t, 2), a)
asol = sp.solve(sp.Eq(EL_a, 0), a)[0]
eps = sp.symbols("epsilon", positive=True)                                   # 1/c^2 bookkeeping
lead = sp.limit(sp.simplify(asol), c, sp.oo) if False else None
asol_series = sp.series(asol.subs(c, 1 / sp.sqrt(eps)), eps, 0, 1).removeO()
coef_minus1 = sp.simplify(sp.expand(asol_series * eps).subs(eps, 0))         # coefficient of 1/eps = c^2
coef_0 = sp.simplify(sp.expand(asol_series - coef_minus1 / eps).subs(eps, 0))
RES["i_symbolic"] = dict(acceleration_exact=str(sp.simplify(asol)), c2_coefficient=str(coef_minus1), order_c0_terms=str(coef_0))
P(f"(i) EOM: a = c^2 x [{coef_minus1}] + [{coef_0}] + O(1/c^2)  (extra force -c^2 grad ln f; toward low f)")
const_check = sp.simplify(asol.subs(f(x), sp.Integer(3)).doit())
RES["i_M1_f_const"] = str(sp.simplify(sp.series(const_check.subs(c, 1 / sp.sqrt(eps)), eps, 0, 1).removeO()))
P(f"(i) MUTATE M1 f constant: a = {RES['i_M1_f_const']} (the extra force vanishes)")
# stress-tensor bookkeeping (dust, f in the action): T_c^{mu nu} = f rho u^mu u^nu; nabla_mu T_c^{mu nu} = -rho c^2 d^nu f (static), so Xi must supply +rho c^2 d^nu f
RES["i_conservation"] = "nabla_mu T_chi^{mu nu} = -rho c^2 d^nu f (rest frame); total conservation needs nabla_mu T_Xi^{mu nu} = +rho c^2 d^nu f: Xi must be a dynamical field coupled with strength of order the component's rest energy. A Yukawa-smoothed dispersion functional has no local stress tensor."
# ---------------- numbers (both footings: g_N and the law)
G, MS, MPC, C = 6.6743e-11, 1.98892e30, 3.0857e22, 2.99792458e8; A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}; Mb = 8e10 * MS; R = 5.41; GYR = 3.15576e16
def glaw(g, a0): return 0.5 * g + math.sqrt(0.25 * g * g + a0 * g)
for foot, a0 in A0.items():
    rows = []
    for RW in (1.5, 2.0):
        for r in (0.1, 0.3, 1.0, 3.0):
            gN = G * Mb / (r * MPC) ** 2; ex = C ** 2 / (RW * MPC); rows.append(dict(R_W_Mpc=RW, r_Mpc=r, extra_c2_gradlnf=ex, g_N=gN, g_law=glaw(gN, a0), ratio_to_gN=ex / gN, ratio_to_law=ex / glaw(gN, a0)))
    worst = min(x["ratio_to_law"] for x in rows); RES.setdefault(foot, {})["i"] = dict(rows=rows, min_ratio_to_law=worst, status="FAIL" if worst >= 1e-3 else "PASS")
    P(f"[{foot}] (i) extra force c^2 |grad ln f| = {C**2/(1.5*MPC):.2e} m/s^2 (R_W 1.5 Mpc); vs the law's g at 0.1 / 0.3 / 1 / 3 Mpc: " + " / ".join(f"{x['ratio_to_law']:.1e}" for x in rows if x['R_W_Mpc'] == 1.5) + f" x -> B0(i) {RES[foot]['i']['status']}")
# ---------------- (ii) symbolic: pair
Mg, mc, d, fs, Gs = sp.symbols("M_g m_c d f G", positive=True)
F_on_g = Gs * Mg * (fs * mc) / d ** 2                                         # toward the component (+ direction from g to c)
F_on_c = -Gs * mc * Mg / d ** 2                                               # toward the galaxy (passive m_c, active M_g)
Fnet = sp.simplify(F_on_g + F_on_c); acm = sp.simplify(Fnet / (Mg + mc))
RES["ii_symbolic"] = dict(net_force=str(Fnet), a_cm=str(acm), M2_f1=str(sp.simplify(Fnet.subs(fs, 1))))
P(f"(ii) pair: net force {Fnet} (zero only for f = 1: {sp.simplify(Fnet.subs(fs, 1))}); a_cm = {acm}")
# field form: nabla_mu (f T^{mu nu}) = T^{mu nu} d_mu f (with nabla T = 0); T = diag(rho c^2, rho s^2 x3), Minkowski, coordinates (ct, x, y, z)
rho, s2, cc = sp.symbols("rho sigma2 c", positive=True); X = sp.symbols("x0:4"); ff = sp.Function("f")(*X)
T = sp.diag(rho * cc ** 2, rho * s2, rho * s2, rho * s2)
viol = [sp.simplify(sum(T[mu, nu] * sp.diff(ff, X[mu]) for mu in range(4))) for nu in range(4)]
RES["ii_field"] = dict(violation=[str(vv) for vv in viol], static_dust=str([sp.simplify(vv.subs(s2, 0).subs(sp.diff(ff, X[0]), 0)) for vv in viol]))
P(f"(ii) field: T^(mu nu) d_mu f = {viol}; static pressureless dust (sigma2 = 0, d_t f = 0): {RES['ii_field']['static_dust']}")
for foot, a0 in A0.items():
    rows = []
    for eps_ in (1.0, 0.1):
        for r in (0.1, 0.3, 1.0):
            mcv = eps_ * R * Mb; acm_v = G * Mb * mcv / ((Mb + mcv) * (r * MPC) ** 2); disp = 0.5 * acm_v * (10 * GYR) ** 2 / MPC
            rows.append(dict(epsilon=eps_, r_Mpc=r, a_cm=acm_v, displacement_10Gyr_Mpc=disp))
    sig = 150e3; disp_term = [dict(r_Mpc=r, sigma2_gradf=sig ** 2 / (1.5 * MPC), g_law=glaw(G * Mb / (r * MPC) ** 2, a0), ratio=(sig ** 2 / (1.5 * MPC)) / glaw(G * Mb / (r * MPC) ** 2, a0)) for r in (0.1, 0.3, 1.0)]
    dtf = 1 / (2 * GYR); H0 = 100 * 0.674 * 1e3 / MPC
    worst_disp = max(x["displacement_10Gyr_Mpc"] for x in rows if x["epsilon"] == 0.1); worst_ratio = min(x["ratio"] for x in disp_term)
    st = "FAIL" if (worst_ratio >= 1e-3 or worst_disp > 0.1) else "PASS"
    RES[foot]["ii"] = dict(pair=rows, dispersion_term=disp_term, time_term=dict(d_t_f=dtf, over_H0=dtf / H0, active_mass_change_rate_Msun_per_Gyr=R * 8e10 / 2.0), status=st)
    P(f"[{foot}] (ii) a_cm (f 0) full share / eps 0.1 at 0.1 / 0.3 / 1 Mpc: " + " / ".join(f"{x['a_cm']:.1e}" for x in rows if x['epsilon'] == 1.0) + " ; " + " / ".join(f"{x['a_cm']:.1e}" for x in rows if x['epsilon'] == 0.1)
      + f" m/s^2; 10 Gyr displacement (eps 0.1) " + " / ".join(f"{x['displacement_10Gyr_Mpc']:.2f}" for x in rows if x['epsilon'] == 0.1) + " Mpc")
    P(f"[{foot}] (ii) dispersion term sigma^2 |grad f| = {sig**2/(1.5*MPC):.1e} m/s^2 vs law g at 0.1 / 0.3 / 1 Mpc: " + " / ".join(f"{x['ratio']:.2f}" for x in disp_term) + f"; time term d_t f / H0 = {dtf/H0:.1f} (active mass changes by order itself per collapse time) -> B0(ii) {st}")
for foot in A0:
    lab = "FAIL at B0" if (RES[foot]["i"]["status"] == "FAIL" and RES[foot]["ii"]["status"] == "FAIL") else "B0 PASSED by a carrier (usual gates next)"
    RES[foot]["label"] = lab; P(f"[{foot}] BI1 LABEL: {lab}")
json.dump(RES, open(os.path.join(HERE, "bi1.json"), "w"), indent=1, default=str); open(os.path.join(HERE, "bi1.out"), "w").write("\n".join(L) + "\n")
