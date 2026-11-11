"""PAR1 spec checks S1-S8, S12 (REL1 root), Lemma 0. Exact (sympy). Criteria 51522963e0.

Run: python3 par1_spec.py            -> par1_spec.out / par1_spec.json
     PAR1_MUTATE=MU1|MU2|MU3 python3 par1_spec.py -> par1_spec_MUTATE_<MU>.out/.json
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys, time
import sympy as sp

MUT = os.environ.get("PAR1_MUTATE", "")
TAG = f"_MUTATE_{MUT}" if MUT else ""
OUT = {}
LINES = []
t0 = time.time()


def rep(key, val, note=""):
    OUT[key] = val
    LINES.append(f"{key}: {val}" + (f"   [{note}]" if note else ""))
    print(LINES[-1][:300], f"  t={time.time()-t0:.1f}s", flush=True)


t0 = time.time()

# ---------------------------------------------------------------- S1 (LFS1 known answer)
x, y, z, t = sp.symbols("x y z t", real=True)
X = sp.Function("X")(x, y, z, t)
Y = [sp.Function(f"Y{i}")(x, y, z, t) for i in range(3)]
Nsh = [sp.Function(f"N{i}")(x, y, z, t) for i in range(3)]
crd = [x, y, z]
divXY = sum(sp.diff(X * Y[i], crd[i]) for i in range(3))
lamN2 = sp.diff(X, t) - sum(Nsh[j] * sp.diff(X, crd[j]) for j in range(3))  # normal equation (QX17 E2 normal part)
# QX17 E3, unitary gauge, gamma_L Pi_+ kept inside X, mu_K terms dropped (LFS1 S1(c) checks them separately)
E3 = sp.diff(divXY, t) - sum(sp.diff(Nsh[i] * divXY + lamN2 * Y[i], crd[i]) for i in range(3))
LFS1_form = sum(sp.diff(X * sp.diff(Y[i], t) + sum(Nsh[j] * sp.diff(X, crd[j]) for j in range(3)) * Y[i]
                        - Nsh[i] * divXY, crd[i]) for i in range(3))
res_S1c = sp.expand(sp.expand(E3) - sp.expand(LFS1_form))
rep("S1c_residual_E3_vs_LFS1_form", str(res_S1c), "LFS1 S1(c), 3D generic functions, with shift")
# spherical, zero shift: sqrt(gamma) rho_Q = d_r(X Y); E3 -> d_r(X d_t Y) = 0 -> X d_t Y = 0 (regular centre)
r = sp.symbols("r", positive=True)
Xs = sp.Function("X")(r, t); Ys = sp.Function("Y")(r, t)
E3s = sp.diff(sp.diff(Xs * Ys, r), t) - sp.diff((sp.diff(Xs, t)) * Ys, r)  # zero shift: lambda N^2 = d_t X
res_S1d = sp.simplify(E3s - sp.diff(Xs * sp.diff(Ys, t), r))
rep("S1d_residual_spherical_zero_shift", str(res_S1d), "E3 = d_r(X d_t Y); regular centre => X d_t Y = 0: Y frozen")
# net zero: charge in [0,R] = X Y|_R - X Y|_0 ; Y(0)=0 (regular), Y(R)=0 (P = 0 at the edge)
R = sp.symbols("R", positive=True)
Q_net = (Xs * Ys).subs(r, R) - (Xs * Ys).subs(r, 0)
rep("S1a_net_charge_with_Y0_YR_zero", str(sp.simplify(Q_net.subs({Ys.subs(r, R): 0, Ys.subs(r, 0): 0}))),
    "LFS1 S1(a)/A2: region bounded where P = 0 is neutral")

# ---------------------------------------------------------------- S2 (EW2 known answer)
eps, mu, Rr, G, M = sp.symbols("epsilon mu R G M", positive=True)
delta = 2 * eps + eps ** 2
s_ = (1 - eps) * G * M / Rr ** 2
lhs = (mu ** 2 / G) * (Rr ** 2 / 4) * s_ * (Rr / 4) ** 2 / 2
sol = sp.simplify(sp.solve(sp.Eq(lhs, 4 * delta * M), mu ** 2)[0] * Rr ** 2)
rep("S2_bound_muR2", str(sp.simplify(sol)), "EW2: (mu R)^2 <= 512 delta/(1 - eps)")
rep("S2_bound_check_residual", str(sp.simplify(sol - 512 * delta / (1 - eps))))
epsv = 10 ** 0.05 - 1
muR = float(sp.sqrt(512 * (2 * epsv + epsv ** 2) / (1 - epsv)))
rep("S2_muR_at_eps", round(muR, 3), "EW2 prints 12.3")
rep("S2_window_gap_mu_w_over_mu_h", round(10 / 0.063, 1), "EW2: mu_w 10, mu_h 0.063 per Mpc, 'x160'")

# ---------------------------------------------------------------- S3 (X14 F2 known answer)
tau, w, K, Sb = sp.symbols("tau w K Sigma_b", positive=True)
Jf = sp.Function("J")
# crossing a sheet: J'' = -K Sigma_b delta(x(t)) J ; integral of delta(x(t)) dt = 1/|xdot| = 1/w
Jdot_jump = -K * Sb * 1 / w  # J = 1 before crossing
Jsol = sp.dsolve(sp.Eq(Jf(tau).diff(tau, 2), 0), Jf(tau), ics={Jf(0): 1, Jf(tau).diff(tau).subs(tau, 0): Jdot_jump}).rhs
rep("S3_J_after", str(Jsol))
rep("S3_residual_vs_X14", str(sp.simplify(Jsol - (1 - K * Sb * tau / w))))
tf = sp.solve(sp.Eq(Jsol, 0), tau)[0]
rep("S3_tau_fold", str(tf))
rep("S3_tau_fold_residual", str(sp.simplify(tf - w / (K * Sb))))

# ---------------------------------------------------------------- S5 / S4 (T-SCR), derived from the reduced Lagrangian
# 1D planar reduced Newtonian Lagrangian of action (A) + a general dust term P(h) (COL1 Part 1 form):
#   L = P(h) + Jf(h_x) - Phi_x^2/(2K) - rho_b Phi,   h = -(phi_t + phi_x^2/2 + Phi)
a0 = sp.symbols("a0", positive=True)
phi = sp.Function("phi")(x, t); Ph = sp.Function("Phi")(x, t); rb = sp.Function("rho_b")(x)
Pf = sp.Function("P")
hexpr = -(sp.diff(phi, t) + sp.diff(phi, x) ** 2 / 2 + Ph)
uu = sp.symbols("u", real=True)
Jfun = (a0 ** 2 / K) * (sp.sqrt(uu ** 2) / a0 - sp.log(1 + sp.sqrt(uu ** 2) / a0))  # J(|h_x|)
Jg = sp.Function("Jg")  # generic J (any law function); the physical J enters only through J' below
L = Pf(hexpr) + Jg(sp.diff(hexpr, x)) - sp.diff(Ph, x) ** 2 / (2 * K) - rb * Ph
EL_phi = sp.euler_equations(L, [phi], [x, t])[0].lhs
# charge N = L_h - d_x L_{h_x}; check EL_phi == -(d_t N + d_x (N phi_x))
hs, hxs = sp.symbols("h h_x", real=True)
Lh = Pf(hs) + Jg(hxs)
Nexpr = sp.diff(Lh, hs).subs({hs: hexpr, hxs: sp.diff(hexpr, x)}) \
    - sp.diff(sp.diff(Lh, hxs).subs({hs: hexpr, hxs: sp.diff(hexpr, x)}), x)
cons = sp.diff(Nexpr, t) + sp.diff(Nexpr * sp.diff(phi, x), x)
res_cons = sp.expand(sp.expand(EL_phi.doit()) - sp.expand(cons.doit()))
if res_cons != 0:
    res_cons = sp.simplify(res_cons)
rep("S5_charge_conservation_residual", str(res_cons), "EL(phi) = +(d_t N + d_x(N v)), N = P'(h) - d_x J'(h_x) = P'(h) + d_x P_pol")
# polarization form: -d_x J'(|h_x|) sgn = d_x (a0 A/(K(a0+|A|))), A = -h_x
Apos = sp.symbols("A", positive=True)
Jp = sp.diff(Jfun, uu).subs(uu, Apos)
rep("S5_J_prime_is_Legendre_P", str(sp.simplify(Jp - a0 * Apos / (K * (a0 + Apos)))), "K P = a0 A/(a0+|A|)")
rep("S5_J_second_at_0", str(sp.limit(sp.diff(Jfun, uu, 2), uu, 0, "+")), "deep MOND: J''(0) = 1/K")

# linear response: dN = chi dh + eps_r k^2 dh/K (eps_r = d(KP)/dA, 1 at A=0), dPhi = -K dN/k^2,
# d_t^2 dN = -nbar k^2 (dPhi + dh)   (from d_t dN = -nbar d_x dv,  d_t dv = -d_x(dPhi + dh))
k, nb, chi, epsr, om2 = sp.symbols("k nbar chi epsilon_r omega2", real=True)
if MUT == "MU1":
    dN_over_dh = chi  # polarization charge dropped
else:
    dN_over_dh = chi + epsr * k ** 2 / K
dh = 1 / dN_over_dh  # per unit dN
dPhi = -K / k ** 2
minus_om2 = sp.simplify(-nb * k ** 2 * (dPhi + dh))  # = d_t^2 dN / dN = -omega^2
om2_expr = sp.simplify(-minus_om2)
rep("S5_omega2_general", str(sp.factor(om2_expr)))
om2_A0 = sp.simplify(om2_expr.subs(epsr, 1))
target = -K * nb * K * chi / (K * chi + k ** 2)
rep("S5_omega2_at_A0", str(sp.factor(om2_A0)))
rep("S5_residual_vs_TSCR", str(sp.simplify(om2_A0 - target)), "T-SCR: omega^2 = -K nbar K chi/(K chi + k^2)")
# sign: for chi >= 0, k real: omega^2 <= 0 (no restoring force)
chip, kp, nbp, Kp = sp.symbols("chi_p k_p n_p K_p", positive=True)
sgn = sp.simplify(om2_A0.subs({chi: chip, k: kp, nb: nbp, K: Kp}))
rep("S5_minus_omega2_at_A0_is_positive", bool(sp.simplify(-sgn).is_positive), "chi, k, nbar, K > 0")
# MU1 check: Jeans support returns
om2_MU1 = sp.simplify(-(-nb * k ** 2 * (dPhi + 1 / chi)))
rep("S5_MU1_reference_Jeans", str(sp.factor(om2_MU1)), "c_s^2 k^2 - K nbar with c_s^2 = nbar/chi")
# high-k limit with a background field
rep("S5_high_k_limit", str(sp.simplify(sp.limit(om2_expr, k, sp.oo))), "K nbar (1/eps_r - 1)")
# S4: quadratic dust P = mu^2 h^2/(2K) -> chi = mu^2/K ; growth rate^2 = -omega^2
muK = sp.symbols("mu_K", positive=True)
growth = sp.simplify(-om2_A0.subs(chi, muK ** 2 / K))
rep("S4_growth_quadratic", str(growth))
rep("S4_residual_vs_TPA1", str(sp.simplify(growth - K * nb / (1 + k ** 2 / muK ** 2))))
# Jeans scale identity: k_J^2 = K nbar / c_s^2 with c_s^2 = nbar/chi  ->  K chi
cs2 = nb / chi
rep("S5_kJ2_equals_Kchi_residual", str(sp.simplify(K * nb / cs2 - K * chi)))

# ---------------------------------------------------------------- S6 (T-DEP)
# static clock: v = 0 => d_t v = -d_x(Phi + h) = 0 => h = C - Phi ; dust part n_d = P'(h) = P'(hbar + DeltaPhi)
C, hbar, Phi_inf = sp.symbols("C hbar Phi_inf", real=True)
phi_static = -C * t  # phi_t = -C, phi_x = 0
h_static = hexpr.subs(phi, phi_static).doit()
rep("S6_h_static", str(sp.simplify(h_static)), "h = C - Phi")
# match: far away h -> hbar where Phi -> Phi_inf => C = hbar + Phi_inf ; h = hbar + (Phi_inf - Phi) = hbar + depth
h_matched = sp.simplify(h_static.subs(C, hbar + Phi_inf))
rep("S6_h_matched", str(h_matched))
rep("S6_dust_part", "n_d = P'(hbar + (Phi_inf - Phi)): one function of the depth in every system")

# ---------------------------------------------------------------- S7 (T-SPAN)
n, n0, c0, A_, B_ = sp.symbols("n n0 c0 A B", positive=True)
# dh = c^2 dn / n ; non-increasing n^2 c^2 <= n0^2 c0^2  =>  h - h0 <= int n0^2 c0^2 / n^3 dn
span_bound = sp.integrate(n0 ** 2 * c0 ** 2 / n ** 3, (n, n0, n))
rep("S7_span_bound", str(sp.simplify(span_bound)), "(c0^2/2)(1 - n0^2/n^2) < c0^2/2")
if MUT == "MU3":
    Pmod = A_ * n ** 2  # convex EOS
else:
    Pmod = -A_ / n + B_  # Chaplygin: n^2 c^2 constant (attains the bound)
c2 = sp.diff(Pmod, n)
span = sp.integrate((c2 / n).subs(n, sp.Symbol("q", positive=True)), (sp.Symbol("q", positive=True), n0, n))
c0sq = c2.subs(n, n0)
rep("S7_model_EOS", str(Pmod))
rep("S7_model_span", str(sp.simplify(span)))
rep("S7_model_span_minus_bound", str(sp.simplify(span - (c0sq / 2) * (1 - n0 ** 2 / n ** 2))))
big = sp.simplify((span / (c0sq / 2)).subs(n, 10 * n0))
rep("S7_model_span_over_half_c0sq_at_10n0", str(big), "<= 1 unless convex (MU3 must exceed 1)")
# P''(tau) = n^2 d(n^2 c^2)/dn
tau_ = sp.symbols("tau", positive=True)
Pg = sp.Function("Pg")
Ptau = Pg(1 / tau_)
P2tau = sp.diff(Ptau, tau_, 2)
nn = sp.symbols("nn", positive=True)
expr_n = (nn ** 2 * sp.diff(nn ** 2 * sp.diff(Pg(nn), nn), nn))
res_P2 = sp.simplify(P2tau.subs(tau_, 1 / nn).doit() - expr_n)
rep("S7_P2tau_identity_residual", str(res_P2), "P''(tau) = n^2 d(n^2 c_s^2)/dn")

# ---------------------------------------------------------------- S8 (T-SHK): energy defect of a barotropic jump
D, t1, p1, a_, b_, c_ = sp.symbols("Delta tau1 P1 a b c", real=True)
if MUT == "MU2":
    # Chaplygin in tau: P = -A n = -A/tau -> P(tau) linear? no: P = -A/n = -A tau (linear in tau) => P''(tau) = 0
    Pt = lambda tt: p1 + a_ * (tt - t1)
else:
    Pt = lambda tt: p1 + a_ * (tt - t1) + b_ * (tt - t1) ** 2 / 2 + c_ * (tt - t1) ** 3 / 6
tt = sp.symbols("tt", real=True)
t2 = t1 + D
m2 = -(Pt(t2) - Pt(t1)) / D  # momentum RH with mass flux m: m^2 = -[P]/[tau]
dh_ = sp.integrate(tt * sp.diff(Pt(tt), tt), (tt, t1, t2))  # dh = tau dP
E_over_m = m2 * (t2 ** 2 - t1 ** 2) / 2 + dh_  # energy flux jump / m (u = m tau)
ser = sp.series(sp.expand(E_over_m), D, 0, 5).removeO()
c3 = sp.simplify(ser.coeff(D, 3))
rep("S8_energy_jump_over_m_series", str(sp.expand(ser)))
rep("S8_coeff_D3", str(c3), "frozen text: -P''(tau)/12; A1 (post hoc): +P''(tau)/12")
rep("S8_coeff_D3_residual_frozen_sign", str(sp.simplify(c3 - (-b_ / 12 if MUT != 'MU2' else 0))))
rep("S8_coeff_D3_residual_A1_sign", str(sp.simplify(c3 - (b_ / 12 if MUT != 'MU2' else 0))),
    "A1: energy-flux jump = +(m/12) P''(tau) (Delta tau)^3, < 0 for a compressive jump (dissipation; LL weak shock)")
rep("S8_coeff_D1_D2", [str(sp.simplify(ser.coeff(D, 1))), str(sp.simplify(ser.coeff(D, 2)))])

# ---------------------------------------------------------------- S12: REL1 runaway root
s, rho, kk = sp.symbols("s rho k_spring", positive=True)
roots = sp.solve(sp.Eq(s ** 4 / K - rho * s ** 2 - kk, 0), s ** 2)
target_root = (K * rho + sp.sqrt(K ** 2 * rho ** 2 + 4 * K * kk)) / 2
rep("S12_REL1_root_residual", str(min([sp.simplify(rt - target_root) for rt in roots], key=lambda e: len(str(e)))),
    "REL1: s^2 = [K rho + sqrt(K^2 rho^2 + 4 K k)]/2")

# ---------------------------------------------------------------- Lemma 0 (FRW)
hFRW = sp.Function("hF")(t)
NF = sp.diff(Lh, hs).subs({hs: hFRW, hxs: 0}) - sp.diff(sp.diff(Lh, hxs).subs({hs: hFRW, hxs: 0}), x)
rep("L0_FRW_charge", str(sp.simplify(NF)), "only P'(h): the phantom (d_x P_pol) is zero on FRW")

OUT["runtime_s"] = round(time.time() - t0, 1)
OUT["mutate"] = MUT
with open(f"par1_spec{TAG}.json", "w") as f:
    json.dump(OUT, f, indent=1, default=str)
with open(f"par1_spec{TAG}.out", "w") as f:
    f.write(f"PAR1 spec checks (criteria 51522963e0); mutate={MUT or 'none'}\n")
    f.write("\n".join(LINES) + "\n")
    f.write("Adopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
print("\n".join(LINES))

# Adopts nothing. kappa = 1/2 FITTED; not theory closed.
