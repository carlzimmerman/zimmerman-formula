#!/usr/bin/env python3
"""AC21 iter_1: 3D well-posedness of the smoothed switch, and a 3D-admissible AC2q-exact smoothing
(criteria ../FROZEN_CRITERIA.md, 3891804624).
Run from the repo root, one thread:
  OMP_NUM_THREADS=1 nice -n 15 python3 action_search_2026_11_05/AC21_smooth_3d/iter_1_3d_symbol/ac21_i1.py
MUTATE (AC21_MUTATE=1): gamma -> -gamma in T1 (must give c^2 < 0) and the pure max form through T3 (m = 2 must fail).
Outputs ac21_i1[_MUTATE].json/.out. kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys, time, itertools
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MUT = os.environ.get("AC21_MUTATE") == "1"
tag = "ac21_i1_MUTATE" if MUT else "ac21_i1"
ok, res = {}, {}
T0 = time.time()

# ---------------- T1: Makino-variable symmetrizer, d = 3 ----------------
Pi, u = sp.symbols("Pi u", positive=True)
gs = sp.Symbol("gamma", positive=True)
g = -gs if MUT else gs
F = sp.Function("F")
Fpp = sp.Function("Fpp")(Pi)              # F''(Pi), stiff side
wprime = sp.sqrt(Fpp / Pi)                 # w'(Pi)
c_expr = Pi * wprime                       # coefficient of div v in the w equation
ok["T1_c_equals_sqrt_PiFpp"] = sp.simplify(c_expr - sp.sqrt(Pi * Fpp)) == 0
ok["T1_force_equals_c_gradw"] = sp.simplify(Fpp / wprime - sp.sqrt(Pi * Fpp)) == 0   # F'' grad Pi = (F''/w') grad w
k1, k2, k3, v1, v2, v3 = sp.symbols("k1 k2 k3 v1 v2 v3", real=True)
cc = sp.Symbol("c", nonnegative=True)
kv = sp.Matrix([k1, k2, k3]); vk = v1 * k1 + v2 * k2 + v3 * k3
Asym = sp.zeros(4, 4)
Asym[0, 0] = vk
for i in range(3):
    Asym[0, i + 1] = cc * kv[i]; Asym[i + 1, 0] = cc * kv[i]; Asym[i + 1, i + 1] = vk
ok["T1_symmetric"] = Asym == Asym.T
ev = Asym.subs({k1: 0, k2: 0, k3: 1}).eigenvals()
res["T1"] = dict(eigenvalues_k_z=[str(e) for e in ev], speeds="v.k (x2), v.k +- c|k|")
ok["T1_speeds"] = set(sp.simplify(e) for e in ev) == {v3, v3 + cc, v3 - cc}
# c^2 = Pi F'' with F = gamma Pi^2/2 (v3s) must be >= 0; MUTATE flips gamma
c2_v3s = Pi * sp.diff(g * Pi ** 2 / 2, Pi, 2)
ok["T1_c2_nonneg_v3s"] = bool(sp.ask(sp.Q.nonnegative(c2_v3s), sp.Q.positive(Pi) & sp.Q.positive(gs)))
res["T1"]["c2_v3s"] = str(c2_v3s)

# ---------------- T2: c(w) smoothness across w = 0 ----------------
def c_over_w_series(Fexpr, var, nterm=4):
    """For F ~ Pi^m near 0: return m and the series of c/w in Pi (c = sqrt(Pi F''), w = int_0^Pi sqrt(F''/u) du)."""
    fpp = sp.diff(Fexpr, var, 2)
    lead = sp.Poly(sp.series(fpp, var, 0, 12).removeO(), var).monoms()
    m = min(mm[0] for mm in lead) + 2
    tt = sp.Symbol("t", positive=True)                    # Pi = t^2 makes every power integral
    integrand = sp.series(sp.sqrt(sp.expand(fpp.subs(var, tt ** 2))) * 2 , tt, 0, (m - 2) + 2 * nterm + 2).removeO()
    wser = sp.integrate(sp.expand(integrand), (tt, 0, tt))  # w(t) (du = 2 t dt, sqrt(F''/t^2) * 2t = 2 sqrt(F''))
    cser = sp.series(tt * sp.sqrt(sp.expand(fpp.subs(var, tt ** 2))), tt, 0, (m - 1) + 2 * nterm + 2).removeO()
    ratio = sp.series(sp.expand(cser) / sp.expand(wser), tt, 0, 2 * nterm + 1).removeO()
    return m, sp.expand(ratio.subs(tt, sp.sqrt(var)))

mm = sp.Symbol("m", positive=True)
Fpow = Pi ** mm
w_pow = sp.integrate(sp.sqrt(sp.diff(Fpow, Pi, 2) / u).subs(Pi, u), (u, 0, Pi), conds="none")
c_pow = sp.sqrt(Pi * sp.diff(Fpow, Pi, 2))
ratio_pow = sp.simplify(sp.powsimp(c_pow / w_pow, force=True).subs(mm, 6))
# code fix (first run): integrating with symbolic m and substituting afterwards gave a wrong ratio (sympy piecewise
# branch); integrate per integer m instead. No graded number depends on the symbolic form.
def _ratio_M(M_):
    Fm = Pi ** M_
    wM = sp.integrate(sp.sqrt(sp.diff(Fm, Pi, 2).subs(Pi, u) / u), (u, 0, Pi))
    return sp.simplify(sp.sqrt(Pi * sp.diff(Fm, Pi, 2)) / wM)
ok["T2_pure_power_linear"] = all(sp.simplify(_ratio_M(M_) - sp.Rational(M_ - 1, 2)) == 0 for M_ in (3, 4, 5, 6, 7))
res["T2_pure_power_ratio"] = {M_: str(_ratio_M(M_)) for M_ in (3, 4, 5, 6, 7)}
a = sp.Symbol("a", positive=True)
T2 = {}
forms = {"AC20_contact_a": Pi ** 4 / (Pi + 1) ** 2,
         "AC20_spline_m4": 5 * Pi ** 4 - 10 * Pi ** 5 + sp.Rational(15, 2) * Pi ** 6 - 2 * Pi ** 7,
         "pure_power_6": Pi ** 6 / 30}
for name, Fx in forms.items():
    m_, rser = c_over_w_series(Fx, Pi)
    p = sp.Poly(rser, Pi)
    terms = sorted(p.terms(), key=lambda tm: tm[0][0])
    const = [cf for (e,), cf in terms if e == 0]
    nonconst = [(e, cf) for (e,), cf in terms if e > 0 and cf != 0]
    first = nonconst[0] if nonconst else None
    # c = w * (c0 + c_j Pi^j + ...), Pi ~ w^(2/(m-1))  =>  first non-linear power of w: 1 + 2 j/(m-1)
    pw = (1 + sp.Rational(2 * first[0], m_ - 1)) if first else None
    T2[name] = dict(m=m_, c_over_w_series=str(rser), linear_coeff=str(const[0]) if const else None,
                    first_correction=(str(first[1]) + f" Pi^{first[0]}") if first else "none",
                    first_nonlinear_w_power=str(pw) if pw is not None else "none (c linear in w near 0)",
                    smooth_in_w=(first is None) or (pw is not None and pw.is_integer))
res["T2"] = T2
ok["T2_contact_not_smooth"] = not T2["AC20_contact_a"]["smooth_in_w"]
ok["T2_spline_m4_not_smooth"] = not T2["AC20_spline_m4"]["smooth_in_w"]
ok["T2_pure_power_smooth"] = T2["pure_power_6"]["smooth_in_w"]

# ---------------- T3: H^s count, m > d + 2 ----------------
T3 = {}
for m_ in ((2,) if MUT else (2, 3, 4, 5, 6)):
    T3[m_] = {d: (sp.Rational(m_, 2) > sp.Rational(d, 2) + 1) for d in (1, 2, 3)}
res["T3"] = {str(k): {str(d): bool(v) for d, v in r.items()} for k, r in T3.items()}
i4 = json.load(open(os.path.join(ROOT, "action_search_2026_11_05/AC20_smooth_switch/iter_4_richardson/ac20_i4.json")))
i1 = json.load(open(os.path.join(ROOT, "action_search_2026_11_05/AC20_smooth_switch/iter_1_power/ac20_i1.json")))
res["T3_cross_check_AC20_1D"] = dict(n3_kink_r=i4["grades"]["control_n3"]["r"], n3_Dinf=i4["grades"]["control_n3"]["Dinf"],
                                     iter1_label=i1.get("label"))
if MUT:
    ok["T3_m2_fails_all_d"] = not any(T3[2].values())
else:
    ok["T3_count"] = (not any(T3[2].values()) and not any(T3[3].values()) and T3[4] == {1: True, 2: False, 3: False}
                      and T3[5] == {1: True, 2: True, 3: False} and all(T3[6].values()))
    ok["T3_matches_AC20_1D"] = 0.9 <= i4["grades"]["control_n3"]["r"] <= 1.1   # m = 3 is a finite kink in 1D, as counted

# ---------------- T4: construction, pure power 6 on (0, tau], C^k blend on [tau, 1], q^2/2 above 1 ----------------
q = sp.Symbol("q", positive=True)
def build(tau, kk):
    D = 2 * kk + 2
    A = sp.Symbol("A"); cs = sp.symbols(f"p0:{D + 1}")
    p = sum(ci * q ** i for i, ci in enumerate(cs))       # f'' on [tau, 1]
    left = A * q ** 4                                      # f'' on (0, tau]
    eqs = [sp.Eq(sp.diff(p, q, j).subs(q, tau), sp.diff(left, q, j).subs(q, tau)) for j in range(kk + 1)]
    eqs += [sp.Eq(p.subs(q, 1), 1)] + [sp.Eq(sp.diff(p, q, j).subs(q, 1), 0) for j in range(1, kk + 1)]
    eqs += [sp.Eq(sp.integrate(left, (q, 0, tau)) + sp.integrate(p, (q, tau, 1)), 1),                    # f'(1) = 1
            sp.Eq(sp.integrate((1 - q) * left, (q, 0, tau)) + sp.integrate((1 - q) * p, (q, tau, 1)), sp.Rational(1, 2))]  # f(1) = 1/2
    sol = sp.solve(eqs, [A] + list(cs), dict=True)
    if len(sol) != 1:
        return None
    s = sol[0]; Av = s[A]; pv = sp.expand(p.subs(s))
    roots = [r for r in sp.Poly(pv, q).real_roots() if tau <= r <= 1]
    pos = (Av > 0) and not roots and pv.subs(q, (tau + 1) / 2) > 0
    # Bernstein coefficients on [tau, 1] (for the Lean positivity certificate)
    sv = sp.Symbol("s"); ps = sp.Poly(sp.expand(pv.subs(q, tau + (1 - tau) * sv)), sv)
    a_c = [ps.coeff_monomial(sv ** i) for i in range(D + 1)]
    bern = [sum(sp.binomial(j, i) / sp.binomial(D, i) * a_c[i] for i in range(j + 1)) for j in range(D + 1)]
    return dict(tau=tau, k=kk, D=D, A=Av, p=pv, roots_in_layer=roots, positive=bool(pos), bern=bern,
                bern_all_pos=all(b_ > 0 for b_ in bern))

T4 = None; tried = []
for kk, tau in [(4, sp.Rational(1, 2)), (4, sp.Rational(1, 3)), (4, sp.Rational(2, 3)),
                (3, sp.Rational(1, 2)), (3, sp.Rational(1, 3)), (3, sp.Rational(2, 3))]:
    r_ = build(tau, kk)
    tried.append(dict(tau=str(tau), k=kk, solved=r_ is not None, positive=(r_ or {}).get("positive"),
                      A=str((r_ or {}).get("A")), bern_all_pos=(r_ or {}).get("bern_all_pos")))
    if r_ is not None and r_["positive"]:
        T4 = r_; break
res["T4_tried"] = tried
ok["T4_convex_member"] = T4 is not None
if T4 is not None:
    tau, Av, pv = T4["tau"], T4["A"], T4["p"]
    fpp = sp.Piecewise((Av * q ** 4, q <= tau), (pv, q <= 1), (1, True))
    f1_left = Av * q ** 5 / 5; f_left = Av * q ** 6 / 30
    f1_mid = f1_left.subs(q, tau) + sp.integrate(pv, (q, tau, q))
    f_mid = f_left.subs(q, tau) + f1_left.subs(q, tau) * (q - tau) + sp.integrate(sp.integrate(pv, (q, tau, q)), (q, tau, q))
    ok["T4_f1_at_1"] = sp.simplify(f1_mid.subs(q, 1) - 1) == 0
    ok["T4_f_at_1"] = sp.simplify(f_mid.subs(q, 1) - sp.Rational(1, 2)) == 0
    qq = np.linspace(0, 1, 40001)
    f1n = np.where(qq <= float(tau), float(Av) * qq ** 5 / 5, sp.lambdify(q, f1_mid, "numpy")(qq))
    dev = float(np.max(np.abs(f1n - qq)))
    ok["T5_Sb_dev"] = dev <= 1.0
    res["T4"] = dict(tau=str(tau), k=T4["k"], degree=T4["D"], A=str(Av), A_float=float(Av), fpp_layer=str(pv),
                     f_layer=str(sp.expand(f_mid)), fprime_layer=str(sp.expand(f1_mid)),
                     bernstein=[str(b_) for b_ in T4["bern"]], bern_all_pos=T4["bern_all_pos"],
                     min_fpp_layer=float(min(sp.lambdify(q, pv, "numpy")(np.linspace(float(tau), 1, 20001)))),
                     max_abs_fprime_minus_q=dev)

# ---------------- T5: statics bounds (AC20 S-d, depend on b only) ----------------
G_, c_, Msun, pc = 6.67430e-11, 2.99792458e8, 1.98892e30, 3.0856775814913673e16
du = Msun / pc ** 3; Sd = {}
for fn, f_ in {"canonical": dict(a0=9.3603e-11, cass=0.0055, Lstar=21.7), "alt": dict(a0=1.1312e-10, cass=0.0062, Lstar=22.9)}.items():
    rho_de = 4 * f_["a0"] ** 2 / (c_ ** 2 * G_); bphys = rho_de / du
    rho_ph = np.sqrt(G_ * 1e9 * Msun * f_["a0"]) / (4 * np.pi * G_ * (30e3 * pc) ** 2) / du
    row = dict(b_Msun_pc3=bphys, cassini=bphys / f_["cass"], globular=bphys / 0.084,
               floor_shift_pct=bphys / 1.5e-4 * 0.042, sparc=(f_["Lstar"] / 1e3) ** 2 * bphys / rho_ph)
    row["pass"] = row["cassini"] <= 1e-3 and row["globular"] <= 1e-3 and row["floor_shift_pct"] <= 0.01 and row["sparc"] <= 1e-4
    Sd[fn] = row
res["T5_Sd"] = Sd
ok["T5_statics"] = all(r["pass"] for r in Sd.values())

# ---------------- T6: AC2q FRW (b = X), exact region (AC20 S-e recheck) ----------------
Xs, Dd, s_ = sp.symbols("X D s", positive=True)
Floc = lambda Q: gs / 2 * Q ** 2
g1 = sp.simplify(sp.diff(Floc(Dd + 2 * Xs), Dd, 2).subs(Dd, 0))
g2 = sp.simplify(sp.diff(sp.diff(Floc(Dd + 2 * Xs) - Floc(2 * Xs), Dd).subs(Dd, 0), Xs))
kq_, K_, al, P_ = sp.symbols("k K alpha P", positive=True)
PA = kq_ * P_ * al / 2; W_ = K_ * P_ ** 2 / 4; DD = kq_ ** 2 * P_ ** 2 / 2; XD = (-s_ ** 2 * al) * (-kq_ * P_) / 2
integ = lambda L: sp.simplify(L.subs(P_, sp.solve(sp.diff(L, P_), P_)[0]))
factor = sp.factor(sp.simplify(integ(PA - W_ - g1 / 2 * DD - g2 * XD) / integ(PA - W_ - gs / 2 * DD)))
ok["T6_g1_g2"] = sp.simplify(g1 - gs) == 0 and sp.simplify(g2 - 2 * gs) == 0
ok["T6_factor"] = sp.simplify(factor - (1 - 2 * gs * s_ ** 2) ** 2) == 0
res["T6"] = dict(g1=str(g1), g2=str(g2), factor=str(factor),
                 exact_neighbourhood="F = gamma Pi^2/2 for Pi >= b = X; FRW Pi = 2X, so |D.P| < X keeps the background exact")

# ---------------- T7: PN symbol with a general local stiffness (AC17 Lagrangian, v3s) ----------------
t7 = {}
if not MUT:
    src = open(os.path.join(ROOT, "action_search_2026_11_05/AC17_pn_sign_all_directions/ac17.py")).read()
    head = src.split("res = {}")[0]
    target_line = "L += sg * (-gam / 2 * s**2)"
    assert target_line in head
    head = head.replace(target_line, "L += sg * (-gam / 2 * (beta_ * s + Cst_ * s**2 / 2))")
    ns = {"__file__": os.path.join(ROOT, "action_search_2026_11_05/AC17_pn_sign_all_directions/ac17.py"),
          "__name__": "ac17_spliced"}
    exec("import sympy as sp\nbeta_, Cst_ = sp.symbols('beta C', real=True)\n" + head, ns)
    spn = ns
    L2 = spn["lagrangian"]("v3s"); eqs = spn["symbol_eqs"](L2)
    Fs, k_, w_, lam = spn["Fs"], spn["k"], spn["w"], spn["lam"]
    M = sp.zeros(4, 4)
    for a_ in range(4):
        c2e = sp.expand(eqs[a_].subs(Fs[4], 0)).coeff(lam, 2)
        for b_ in range(4): M[a_, b_] = spn["freeze"](c2e.coeff(Fs[b_]))
    Aw = sp.simplify(M[0, 0].coeff(w_, 2)); m0 = sp.expand(M[0, 0].subs(w_, 0))
    cpl = sp.factor(M[0, 1] / (k_[0] * w_)); pL = sp.factor(M[1, 1] / k_[0] ** 2)
    kk2 = sum(x_ ** 2 for x_ in k_)
    w1s = sp.Symbol("w1")
    iso = sp.simplify((-(m0 - m0.coeff(w1s) * w1s)) / kk2)
    Aeff = sp.factor(sp.simplify(Aw - cpl ** 2 / pL))
    s0 = spn["freeze"](spn["s0f"])
    N0, Psi0, gam0, muS, KS = spn["N0"], spn["Psi0"], spn["gam0"], spn["mu"], spn["K"]
    # v3s check: beta = 0, C = 2 must reproduce AC17's A_eff
    Aeff_v3s = sp.simplify(Aeff.subs({spn["beta_"]: 0, spn["Cst_"]: 2}))
    ok["T7_reduces_to_AC17"] = sp.simplify(Aeff_v3s - Psi0 ** 6 * (N0 * (1 + gam0 * s0) ** 2 / gam0 + muS ** 2 / (KS * N0))) == 0
    bet, Cs = spn["beta_"], spn["Cst_"]
    PdlnN = spn["freeze"](spn["PdlnN"]); PdNs = spn["freeze"](spn["PdNs"])
    cand = N0 ** 3 * Psi0 ** 2 * ((1 + bet * gam0 / 2) * (s0 + PdlnN) + (Cs * gam0 / 2) * (s0 ** 2 + PdNs)
                                  + muS ** 2 * (1 - N0) / (KS * N0 ** 2))
    ok["T7_iso_closed_form"] = sp.simplify(sp.expand(iso - cand)) == 0
    Aeff_c = Psi0 ** 6 * (N0 * (2 + gam0 * (bet + Cs * s0)) ** 2 / (2 * Cs * gam0) + muS ** 2 / (KS * N0))
    ok["T7_Aeff_closed_form"] = sp.simplify(Aeff - Aeff_c) == 0
    # on shell: background P equation with F gives K Psi^2 W1 qhat = a + (gamma/2) grad(N F'(s))/N; with the local
    # quadratic F' = beta + C s its contraction is (1 + gamma beta/2) P.a + (C gamma/2) P.grad(N s)/N = K Psi^2 W1 |q|,
    # i.e. exactly the iso terms. So B_gen = (1 + gamma beta/2) s + (C gamma/2) s^2 + mu^2 (1-N)/(K N^2).
    Nn = sp.Function("N")(*spn["X"]); s0fx = spn["s0f"]
    Fp = sp.Function("Fp")
    lhs = (gam0 / 2) * sum(spn["P0"][i] * sp.diff(Nn * (bet + Cs * s0fx), spn["X"][i]) for i in range(3)) / Nn
    rhs = (gam0 * bet / 2) * sum(spn["P0"][i] * sp.diff(Nn, spn["X"][i]) for i in range(3)) / Nn + (Cs * gam0 / 2) * spn["PdNs"]
    ok["T7_contraction_identity"] = sp.simplify(sp.expand(lhs - rhs)) == 0
    sS, F1, F2 = sp.symbols("s Fprime Fpp", real=True)
    Bgen = (1 + gam0 * (F1 - sS * F2) / 2) * sS + (F2 * gam0 / 2) * sS ** 2
    ok["T7_B_equals_s_plus_half_gamma_s_Fprime"] = sp.simplify(Bgen - (sS + gam0 * sS * F1 / 2)) == 0
    t7 = dict(A_eff=str(Aeff), iso_weight=str(sp.factor(iso)), coupling=str(cpl), p_long=str(pL),
              A_eff_at_v3s=str(sp.factor(Aeff_v3s)),
              closed_form_iso="N^3 Psi^2 [(1 + gamma beta/2)(s + P.a) + (C gamma/2)(s^2 + P.grad(N s)/N) + mu^2(1-N)/(K N^2)]",
              closed_form_Aeff="Psi^6 [N (2 + gamma(beta + C s))^2/(2 C gamma) + mu^2/(K N)]",
              B_on_shell="s + (gamma/2) s F'(s) + mu^2 (1-N)/(K N^2) + x0 W' sin^2 theta  (beta = F' - s F'', C = F'')",
              positivity="B >= s > 0 iff F'(s) >= 0 (and N <= 1, W' >= 0); A_eff > 0 iff F''(s) > 0 (gamma > 0)")
    res["T7"] = t7
    spn_ = dict(Aeff=Aeff, iso=iso, beta=spn["beta_"], C=spn["Cst_"], s0=s0, gam0=gam0, N0=N0, Psi0=Psi0, mu=muS, K=KS)
res["elapsed_s"] = round(time.time() - T0, 1)

if not MUT:
    out_partial = dict(checks=ok, results=res)
    open(os.path.join(HERE, tag + "_stage1.json"), "w").write(json.dumps(out_partial, indent=1, default=str) + "\n")
    print(json.dumps(dict(T7=t7), indent=1), flush=True)

# T7 sign analysis is done in stage 2 below (needs the printed closed forms), see ac21_i1_t7.py
label = None
if not MUT:
    contact3d = "NOT A 3D REPAIR" if (not T2["AC20_contact_a"]["smooth_in_w"] or not T3[4][3]) else "PASS"
    t7_general = all(ok.get(k_, False) for k_ in ("T7_reduces_to_AC17", "T7_iso_closed_form", "T7_Aeff_closed_form",
                                                   "T7_contraction_identity", "T7_B_equals_s_plus_half_gamma_s_Fprime"))
    if ok["T4_convex_member"]:
        t4lab = "candidate (needs iter_2 numerics)"
        ac2q = "EXISTS" if (ok["T5_statics"] and ok["T6_g1_g2"] and ok["T6_factor"] and ok.get("T5_Sb_dev")) else "NO-GO for the declared family"
    else:
        t4lab = "FAIL as frozen: no convex member in the declared family (minimal-degree blends, tau in {1/2,1/3,2/3}, C^4/C^3 knots)"
        ac2q = "NO-GO for the declared family (as frozen)"
    label = dict(contact_form_3d=contact3d,
                 T4_form_3d=t4lab,
                 AC2q_smoothing=ac2q,
                 T1_T3_theorem="PASS: classical H^s theory across a transverse switch needs F a pure power Pi^m near 0 with m > d + 2"
                 if (ok["T1_symmetric"] and ok["T1_speeds"] and ok["T2_pure_power_linear"] and ok["T2_pure_power_smooth"] and ok["T3_count"]) else "FAIL",
                 PN_sign_layer=("PASS (general): B = s + (gamma/2) s F'(s) + ... >= s for any convex F with F(0) = F'(0) = 0; A_eff > 0 iff F'' > 0"
                                if t7_general else "UNDECIDED"))
if MUT:
    label = "MUTATE: " + ("bites (T1 c^2 sign broken, m = 2 fails T3)" if (not ok["T1_c2_nonneg_v3s"] and ok["T3_m2_fails_all_d"]) else "DOES NOT BITE")
out = dict(mode="MUTATE" if MUT else "main", label=label, checks=ok, results=res, note="kappa = 1/2 FITTED; not theory closed")
open(os.path.join(HERE, tag + ".json"), "w").write(json.dumps(out, indent=1, default=str) + "\n")
txt = "\n".join(f"{k}: {'ok' if v else 'FAIL'}" for k, v in ok.items()) + f"\nLABEL(stage1): {label}\n"
open(os.path.join(HERE, tag + ".out"), "w").write(txt)
print(txt)
if MUT:
    sys.exit(1 if label.endswith("T3)") else 0)   # bites -> exit 1 (record convention)
