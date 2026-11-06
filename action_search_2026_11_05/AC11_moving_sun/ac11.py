#!/usr/bin/env python3
"""AC11: the moving Sun in AC2q's clock frame (analogue of astra's AZ37; AZ37 is read, never edited).

Criteria: FROZEN_CRITERIA.md (8649eb6d06). Geometric units G = c = 1 inside the linear system (K = 4 pi);
SI for reporting. s^2 <= 2 rho_DE = 8 a0^2 (framework-native). Both footings, never pooled.
Run from the repo root:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 python3 action_search_2026_11_05/AC11_moving_sun/ac11.py
AC11_MUTATE=1: gamma -> -gamma in B2 (Omega'^2 must turn negative on every cell). kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, math, hashlib, time, resource
sys.dont_write_bytecode = True
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[key] = "1"
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.integrate import solve_ivp

MUT = os.environ.get("AC11_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
OUT, CHK = [], {}
RES = {"lane": "AC11_moving_sun", "criteria": "8649eb6d06", "mutate": MUT}
T0 = time.monotonic()


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, detail):
    CHK[name] = bool(ok); RES.setdefault("checks", {})[name] = dict(ok=bool(ok), detail=str(detail))
    P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")


P("AC11  moving Sun in AC2q's clock frame" + ("  [MUTATE: gamma -> -gamma in B2]" if MUT else ""))

# ======================================================= B1: the exact P = 0 branch
P("B1: exact P = 0 GR branch")
# B1a(i): on-region stiffness at P = 0, first variation in P. D.P = div P - P.A for spatial P (n.P = 0), so
#   -(gamma/2)[(D.P)^2 + 4 X D.P] -> -2 gamma X (div dP - dP.A) -> +2 gamma dP.(grad X + X A) after integration by parts;
#   P.A -> dP.A ; W -> 0 (quadratic at P = 0).  P equation (spatial): A (1 + 2 gamma X) + 2 gamma D X = 0.
gam, Xs = sp.symbols("gamma X", positive=True)
DX = sp.Symbol("DX", real=True)
A_scalar = -DX / (2 * Xs)                                  # acceleration of the phi-leaf normal (checked in B1a(ii))
Peq = sp.factor(A_scalar * (1 + 2 * gam * Xs) + 2 * gam * DX)
P(f"  P equation at P = 0 with A = -DX/(2X): {Peq} = 0")
sol_DX = sp.solve(sp.Eq(Peq, 0), DX)
check("B1a_Peq", sol_DX == [0], f"solutions DX = {sol_DX} (unless 2 gamma X = 1): the clock must be geodesic, D X = 0")
# B1a(ii): acceleration identity a_mu = n^nu nabla_nu n_mu = -h_mu^nu d_nu X/(2X) for n = -d phi/sqrt(2X), flat 1+2
t, x, y = sp.symbols("t x y", real=True)
ph = sp.Function("phi")(t, x, y)
eta = sp.diag(-1, 1, 1); co = (t, x, y)
dph = sp.Matrix([sp.diff(ph, c) for c in co])
Xf = -(dph.T * eta.inv() * dph)[0] / 2
n_lo = -dph / sp.sqrt(2 * Xf)
n_up = eta.inv() * n_lo
acc = sp.Matrix([sum(n_up[nu] * sp.diff(n_lo[mu], co[nu]) for nu in range(3)) for mu in range(3)])
hproj = eta + n_lo * n_lo.T                                 # h_{mu nu} (lower); h_mu^nu = h_{mu a} eta^{a nu}
dX = sp.Matrix([sp.diff(Xf, c) for c in co])
rhs = -(hproj * eta.inv() * dX) / (2 * Xf)
res_acc = [sp.simplify(acc[i] - rhs[i]) for i in range(3)]
check("B1a_accel", all(r == 0 for r in res_acc), f"a_mu + h_mu^nu d_nu X/(2X) = {res_acc} (flat 1+2, general phi)")
# B1b: Klein-Gordon for phi = f(tau), |d tau| = 1:  box phi = -f'' + f' box tau ... with theta = nabla.u, u = -d tau:
#   box phi = f'' g^{ab} tau_a tau_b + f' box tau = -f'' - f' theta = V'(f): theta must be a function of tau alone.
r, E, M = sp.symbols("r E M", positive=True)
f = 1 - 2 * M / r
ur = -sp.sqrt(E ** 2 - f)                                   # u^r for tau = E t + T(r), infalling branch
theta = sp.simplify(sp.diff(r ** 2 * ur, r) / r ** 2)        # stationary: d/dt terms vanish
dth = sp.simplify(sp.diff(theta, r))
P(f"  theta(r) = {theta};  d theta/dr = {dth}")
vals = {str(Ev): str(sp.nsimplify(dth.subs({E: Ev, M: 1, r: 10}))) for Ev in (1, sp.Rational(13, 12), sp.Rational(5, 3))}
nonuni = all(sp.simplify(dth.subs({E: Ev, M: 1, r: 10})) != 0 for Ev in (1, sp.Rational(13, 12), sp.Rational(5, 3)))
# known answer (corrected after the first run, see README): flat space with static observers (M = 0, E = 1) has theta = 0,
# uniform; a flat radial congruence with E > 1 is itself non-uniform, so M = 0 alone is not a known answer.
ka_flat = sp.simplify(theta.subs({M: 0, E: 1}))
check("B1b", nonuni and ka_flat == 0,
      f"theta varies along each leaf (d theta/dr at M=1, r=10: {vals}); known answer M = 0, E = 1: theta = {ka_flat}")
branch_label = "BRANCH ABSENT (s != 0, tested family)" if (CHK["B1a_Peq"] and CHK["B1a_accel"] and CHK["B1b"]) else "UNSETTLED"
P(f"  B1 label: {branch_label}; at s = 0 the Klein-Gordon obstruction is absent (AZ37's v3s branch).")
RES["B1"] = dict(label=branch_label, P_equation=str(Peq), theta=str(theta), dtheta_dr=str(dth))

# ======================================================= B2: AC2q's own forced linear system
P("B2: forced oscillator on AC7's hand-built on-region system with a baryon source")
K, s, Mt, k, om = sp.symbols("K s M_theta k omega", positive=True)
gL = sp.Symbol("gamma_L", positive=True)
d0 = sp.Symbol("rho0", positive=True)
W2 = sp.Symbol("W2", positive=True)
dphi, dsig, dXi, drb = sp.symbols("dphi dsigma dXi drho_b")
dP = sp.symbols("dP0:3"); dPv = sp.Matrix(dP)
kh = sp.Matrix([0, 0, 1])


def system(gam_):
    # longitudinal block only: the transverse P rows read -K M_theta dP_perp = 0 exactly (stiffness acts along k only)
    dPz = dP[2]
    dC2 = s ** 2 * (-2 * sp.I * om * dsig - 2 * dphi)
    dD = sp.I * k * dPz
    Peq_ = sp.I * k * dXi - K * Mt * dPz - gam_ * k ** 2 * dPz + sp.I * gam_ * k * dC2
    drt = (1 - 2 * gam_ * s ** 2) * dD + s ** 2 * (1 - 2 * gam_ * d0) * (-sp.I * om * dsig - 2 * dphi)
    rx0 = d0 + s ** 2 * (1 - 2 * gam_ * d0)
    ce = -sp.I * om * drt + rx0 * k ** 2 * dsig
    pois = -k ** 2 * dphi - K * ((1 - 2 * gam_ * s ** 2) * dD + s ** 2 * (1 - 2 * gam_ * d0) * (-2 * sp.I * om * dsig - 3 * dphi)) - K * drb
    be = dXi - (dphi + sp.I * om * dsig)
    unk = [dphi, dsig, dXi, dPz]
    Am, bm = sp.linear_eq_to_matrix([pois, ce, be, Peq_], unk)
    det = sp.expand(Am.det(method="berkowitz"))
    xa = [sp.expand(v) for v in (Am.adjugate() * bm)]       # = det * solution (Cramer)
    sub = dict(zip(unk, xa))
    tr = sp.cancel(sp.expand(drt.subs(sub)) / (det * drb))
    sg = sp.cancel(xa[1] / (det * drb)); fi = sp.cancel(xa[0] / (det * drb))
    c2 = sp.cancel(sp.expand(dC2.subs(sub)) / (det * drb))
    return tr, sg, fi, c2


gam_use = -gL if MUT else gL
Tr, Sg, Fi, C2t = system(gam_use)
Tr_w = sp.cancel(Tr.subs(om, sp.sqrt(W2)))
num, den = sp.fraction(Tr_w)
num = sp.expand(num); den = sp.expand(den)
assert not num.has(sp.sqrt(W2)) and not den.has(sp.sqrt(W2)), "odd powers of omega in the transfer"
P(f"  degree in omega^2: numerator {sp.degree(num, W2)}, denominator {sp.degree(den, W2)}")
den_roots = sp.solve(sp.Eq(den, 0), W2)
Om2 = sp.factor(den_roots[0]) if len(den_roots) == 1 else None
c_inst = sp.factor(sp.cancel(sp.Poly(num, W2).coeff_monomial(W2 ** sp.degree(den, W2)) / sp.Poly(den, W2).LC())) \
    if sp.degree(num, W2) == sp.degree(den, W2) else sp.Integer(0)
Fp = sp.factor(sp.cancel((Tr_w - c_inst) * (Om2 - W2))) if Om2 is not None else None
assert Fp is None or not Fp.has(W2), "transfer is not single-pole"
P(f"  Omega'^2 = {Om2}")
P(f"  instantaneous part c0 = {c_inst};  forcing F' = {Fp}")
# B2a known answer at s = 0
Om2_az = d0 * (K * (Mt - 1) + gam_use * k ** 2)
ka_T = sp.simplify(Tr.subs(s, 0) - K * d0 / (Om2_az - om ** 2))
check("B2a", ka_T == 0 and Fp is not None and not sp.simplify(Fp - K * d0).subs(s, 0) != 0,
      f"s = 0: T - K rho0/(Omega^2 - omega^2) = {ka_T}  (gamma = K Lstar^2/2 gives AZ37's oscillator)")
RES["B2_symbolic"] = dict(transfer=str(Tr), Omega2=str(Om2), c_inst=str(c_inst), F=str(Fp),
                          dsigma_per_drho=str(Sg), dphi_per_drho=str(Fi), dC2_per_drho=str(C2t))

# numbers
cl = 2.99792458e8; PC = 3.0856775814913673e16; AU = 1.495978707e11; G = 6.67430e-11; MSUN = 1.98847e30
GMs = 1.32712440018e20
inputs = {"canonical": dict(a0=9.3603e-11, rho=0.0447, xe=1.15, lengths=(21.68, 24., 27.), az_v=(753.5, 938.4), az_T=5.383373929284541e-15),
          "alt": dict(a0=1.1312e-10, rho=0.0514, xe=2.6, lengths=(22.85, 24., 24.60), az_v=(851.6, 916.9), az_T=6.190110012324432e-15)}
fOm2 = sp.lambdify((K, d0, Mt, gL, s, k), Om2, "mpmath")
fF = sp.lambdify((K, d0, Mt, gL, s, k), Fp, "mpmath")
fc0 = sp.lambdify((K, d0, Mt, gL, s, k), c_inst, "mpmath")
fSg = sp.lambdify((K, d0, Mt, gL, s, k, om), Sg, "mpmath")
fFi = sp.lambdify((K, d0, Mt, gL, s, k, om), Fi, "mpmath")
fC2 = sp.lambdify((K, d0, Mt, gL, s, k, om), C2t, "mpmath")


def analytic(u, xx, resonance):
    with mp.workdps(50):
        U = mp.mpf(str(u)); X = U if resonance else mp.mpf(str(xx))
        if resonance:
            ans = (mp.sin(U) / U - mp.exp(-mp.j * U)) / (2 * mp.j * U)
        else:
            ans = (mp.exp(-mp.j * X) - mp.cos(U) + mp.j * X * mp.sin(U) / U) / (U * U - X * X)
        conv = mp.quad(lambda z: mp.sin(U * (1 - z)) / U * mp.exp(-mp.j * X * z), [0, 1])
        return complex(ans), float(abs(ans - conv) / max(1, abs(ans)))


def numerical(u, xx, tight):
    rhs_ = lambda T, yv: (yv[1], np.exp(-1j * xx * T) - u * u * yv[0])
    sol = solve_ivp(rhs_, (0, 1), (0j, 0j), method="DOP853", rtol=1e-11 if tight else 1e-9, atol=1e-13 if tight else 1e-11)
    return complex(sol.y[0, -1]), bool(sol.success)


mp.mp.dps = 40
B2 = {}
all_res, all_neg, conv_ok, conv_err = True, True, True, 0.0
for foot, p in inputs.items():
    ag = p["a0"] / cl ** 2; s2v = 8 * ag ** 2
    rho_geo = G * p["rho"] * MSUN / PC ** 3 / cl ** 2
    mt = (1 + p["xe"]) ** 2; Kn = 4 * math.pi
    rows = []
    for sval in (0.0, math.sqrt(s2v)):
        for L in p["lengths"]:
            gl = Kn * (L * PC) ** 2 / 2
            for v in (220000., 369000.):
                for rAU in (1., 9.58):
                    kk = 1 / (rAU * AU)
                    O2g = float(fOm2(Kn, rho_geo, mt, gl, sval, kk))
                    if O2g <= 0:
                        rows.append(dict(s=sval, Lstar_pc=L, v=v, r_AU=rAU, Omega2_geo=O2g, real_phase_speed=False))
                        all_res = False
                        continue
                    all_neg = False
                    Og = math.sqrt(O2g); Osi = Og * cl
                    vph = Osi / kk
                    pole = vph / v
                    Fsi = float(fF(Kn, rho_geo, mt, gl, sval, kk)) * cl ** 2
                    c0 = complex(fc0(Kn, rho_geo, mt, gl, sval, kk))
                    if not (0 < pole <= 1):
                        all_res = False
                    cells = []
                    for direction, cosine in (("transverse", 0.), ("resonant", pole), ("parallel", 1.)):
                        for cross in (1., 10.):
                            tend = cross * rAU * AU / v; u = Osi * tend
                            xx = u if direction == "resonant" else kk * v * cosine * tend
                            ex, err = analytic(u, xx, direction == "resonant")
                            co_, ok0 = numerical(u, xx, False); fi_, ok1 = numerical(u, xx, True)
                            sc = max(1, abs(ex))
                            e = max(abs(co_ - ex), abs(fi_ - ex), abs(fi_ - co_)) / sc
                            conv_err = max(conv_err, e); conv_ok &= (e <= 1e-7 and err <= 1e-30 and ok0 and ok1)
                            transfer = Fsi * tend ** 2 * ex
                            cells.append(dict(direction=direction, cosine=cosine, crossings=cross,
                                              transfer_magnitude=abs(transfer), conv_err=e, convolution_err=err))
                    # B2d: stationary clock-velocity and X transfers (transverse omega = 0, parallel omega = k v), per unit drho_geo
                    amp = GMs / cl ** 2 * kk ** 3 / (2 * math.pi ** 2)     # Sun's Fourier density scale (geometric) at k
                    xd = {}
                    for nm, w_ in (("static", 0.0), ("parallel", kk * v / cl)):
                        if abs(O2g - w_ ** 2) < 1e-30 * O2g:
                            continue
                        sgv = complex(fSg(Kn, rho_geo, mt, gl, sval, kk, w_ if w_ > 0 else 1e-300))
                        c2v = complex(fC2(Kn, rho_geo, mt, gl, sval, kk, w_ if w_ > 0 else 1e-300)) if sval > 0 else None
                        fiv = complex(fFi(Kn, rho_geo, mt, gl, sval, kk, w_ if w_ > 0 else 1e-300))
                        xd[nm] = dict(khronon_velocity_over_c=abs(kk * sgv) * amp, dphi=abs(fiv) * amp,
                                      dX_over_X=(abs(c2v) * amp / sval ** 2) if c2v is not None else None)
                    rows.append(dict(s=sval, Lstar_pc=L, v=v, r_AU=rAU, Omega2_geo=O2g, real_phase_speed=True,
                                     phase_speed_m_s=vph, pole_cosine=pole, F_SI=Fsi, c0=[c0.real, c0.imag],
                                     max_transfer=max(c["transfer_magnitude"] for c in cells), cells=cells, B2d=xd))
    B2[foot] = rows
    if not MUT:
        r0 = [q for q in rows if q["s"] == 0.0]; r1 = [q for q in rows if q["s"] > 0]
        v0 = (min(q["phase_speed_m_s"] for q in r0), max(q["phase_speed_m_s"] for q in r0))
        v1 = (min(q["phase_speed_m_s"] for q in r1), max(q["phase_speed_m_s"] for q in r1))
        T0_ = max(q["max_transfer"] for q in r0); T1_ = max(q["max_transfer"] for q in r1)
        check(f"B2b_known_{foot}", abs(v0[0] - p["az_v"][0]) < 0.05 and abs(v0[1] - p["az_v"][1]) < 0.05,
              f"s = 0 phase speeds {v0[0]:.1f}-{v0[1]:.1f} m/s vs AZ37 {p['az_v'][0]}-{p['az_v'][1]}")
        # post-run addition (README): the frozen B2b reference was transcribed from AZ37's README (rounded); compare to its stored JSON too
        azj = json.load(open(os.path.join(ROOT, "astra_goal_2026_11_05/AZ37_moving_sun/main/response.json")))["footings"][foot]["cases"]
        azv = (min(c["phase_speed_m_s"] for c in azj), max(c["phase_speed_m_s"] for c in azj))
        check(f"B2b_json_{foot}_postrun", abs(v0[0] / azv[0] - 1) < 1e-12 and abs(v0[1] / azv[1] - 1) < 1e-12,
              f"s = 0 phase speeds vs AZ37 stored JSON {azv[0]:.10f}-{azv[1]:.10f}: rel diff {abs(v0[1]/azv[1]-1):.1e}")
        check(f"B2c_known_{foot}", abs(T0_ / p["az_T"] - 1) < 1e-6,
              f"s = 0 max |rho_tau/rho_source| {T0_:.6e} vs AZ37 {p['az_T']:.6e}")
        dvr = max(abs(a["phase_speed_m_s"] / b["phase_speed_m_s"] - 1) for a, b in zip(r1, r0))
        dTr = max(abs(a["max_transfer"] / b["max_transfer"] - 1) for a, b in zip(r1, r0))
        c0max = max(math.hypot(*q["c0"]) for q in r1)
        poles = (min(q["pole_cosine"] for q in r1), max(q["pole_cosine"] for q in r1))
        xvel = max(max(d["khronon_velocity_over_c"] for d in q["B2d"].values()) for q in r1)
        dXX = max(max(d["dX_over_X"] for d in q["B2d"].values()) for q in r1)
        B2[foot + "_summary"] = dict(phase_speeds_s0=v0, phase_speeds_AC2q=v1, max_rel_phase_change=dvr,
                                     max_transfer_s0=T0_, max_transfer_AC2q=T1_, max_rel_transfer_change=dTr,
                                     max_instantaneous_c0=c0max, pole_cosines=poles,
                                     max_khronon_velocity_over_c=xvel, max_dX_over_X=dXX, s2_geo=s2v)
        P(f"  [{foot}] AC2q phase speeds {v1[0]:.2f}-{v1[1]:.2f} m/s (max rel change vs s=0 {dvr:.2e}); pole cosines "
          f"{poles[0]:.5f}-{poles[1]:.5f}; max |rho_tau/rho_source| {T1_:.6e} (rel change {dTr:.2e}); |c0| <= {c0max:.2e}")
        P(f"  [{foot}] B2d at the Sun's Fourier amplitude: khronon velocity/c <= {xvel:.2e}, |dX/X| <= {dXX:.2e}")
check("B2_resonance", all_res if not MUT else True, "every physical cell has a real Omega' and 0 < pole <= 1 (resonance survives)")
check("B2_convergence", conv_ok, f"DOP853 pairs vs exact <= 1e-7 (max {conv_err:.2e}); 50-digit convolution <= 1e-30")
if MUT:
    check("MUTATE_bites", all_neg, "gamma -> -gamma: Omega'^2 < 0 on every cell (no real phase speed)")
else:
    dxmax = max(B2[f + "_summary"]["max_dX_over_X"] for f in inputs)
    check("B2d_Xpositive", dxmax < 1, f"|dX/X| <= {dxmax:.2e} < 1 at the Sun's Fourier amplitude: X stays > 0 in the linear moving response")
RES["B2"] = B2

# B2e: linearity diagnostic. Static T(omega=0) * point-mass source -> q_sun(r) = Phi_N/gamma (geometric)
if not MUT:
    B2e = {}
    for foot, p in inputs.items():
        rho_geo = G * p["rho"] * MSUN / PC ** 3 / cl ** 2
        rows = []
        for L in p["lengths"]:
            gl = 4 * math.pi * (L * PC) ** 2 / 2
            q = lambda rr: GMs / cl ** 2 / rr / gl
            req = GMs / cl ** 2 / gl / rho_geo
            rows.append(dict(Lstar_pc=L, q_over_rho0_1AU=q(AU) / rho_geo, q_over_rho0_958AU=q(9.58 * AU) / rho_geo, r_equal_AU=req / AU))
            P(f"  B2e [{foot}] Lstar {L} pc: q_sun/rho0 = {q(AU)/rho_geo:.3e} at 1 AU, {q(9.58*AU)/rho_geo:.3e} at 9.58 AU; "
              f"q_sun = rho0 at {req/AU:.0f} AU")
        B2e[foot] = rows
    RES["B2e"] = B2e
    # off-region oscillator (stiffness off): report only
    Troff, _, _, _ = system(0)
    num_o, den_o = sp.fraction(sp.together(sp.simplify(Troff.subs(om, sp.sqrt(W2)))))
    Om2_off = sp.simplify(sp.solve(sp.Eq(sp.expand(den_o), 0), W2)[0])
    P(f"  off-region Omega^2 = {Om2_off} (k-independent: phase speed -> 0 as k grows; resonance present there too)")
    RES["off_region_Omega2"] = str(Om2_off)

# labels
fail = (not MUT) and ((not CHK.get("B2_resonance", True) and any(not q["real_phase_speed"] for f in inputs for q in B2[f])) or not CHK.get("B2d_Xpositive", True))
label = "FAIL" if fail else "NO VERDICT"
RES["label"] = label
RES["scope"] = ("Frozen Galactic on-region coefficients, isotropic Hessian, zero initial response; B1 on one congruence family. "
                "No nonlinear moving solve, no metric PPN coefficient, no observational exclusion.")
srcs = [os.path.join(HERE, "ac11.py"), os.path.join(HERE, "FROZEN_CRITERIA.md"),
        os.path.join(ROOT, "astra_goal_2026_11_05/AZ37_moving_sun/response.py"),
        os.path.join(ROOT, "action_search_2026_11_05/AC7_charge_switch/ac7.py")]
RES["sources"] = {os.path.relpath(q, ROOT): hashlib.sha256(open(q, "rb").read()).hexdigest() for q in srcs}
RES["seconds"] = time.monotonic() - T0
RES["peak_rss_bytes"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
P(f"LABEL: {label} (complete moving-Sun prediction); B1 {branch_label}" + ("  [MUTATE]" if MUT else ""))
with open(os.path.join(HERE, f"ac11{TAG}.json"), "w") as fh:
    json.dump(RES, fh, indent=1, default=str)
with open(os.path.join(HERE, f"ac11{TAG}.out"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
sys.exit(0 if all(CHK.values()) else 1)
