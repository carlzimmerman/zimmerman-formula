"""D7d_screened_q2 -- Cassini Q2 of the STIFFENED DSF-21 action in the Galaxy's field.

Criteria: FROZEN_CRITERIA.md (a13e418498) + AMENDMENT 1 (e1ba64cf92, pre-result).
Run:  OMP_NUM_THREADS=1 nice -n 10 python3 d7d_screened_q2.py [--mutate]
      --mutate: Route N uses the scalar Laplacian on the spherical components of q (must break K5 or K6).
Deterministic, no network, single thread. kappa = 1/2 FITTED; not theory closed.

Equations (A33 (L), (P); static, O(eps), f = 1; p = K P, Phi = ln N):
    lap Phi = K rho + div p ;   grad Phi + (L*^2/2) lap p = a0 p/(a0 - |p|).
At L* = 0 this is AQUAL with mu = x/(1+x) (A33 K4). Route F = linear Fourier response about the Galactic
background (exact for L* >> r_M); Route N = nonlinear axisymmetric grid (any L*).
"""
import os, sys, json, math, time, resource, warnings
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import d7d_solver as S

MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
ROOT = os.path.dirname(os.path.dirname(HERE))
def rel(*p): return os.path.join(ROOT, *p)

# ---------------------------------------------------------------- inputs (labelled)
GM = 1.32712440018e20; AU = 1.495978707e11; PC = 3.0857e16; MSUN_GM = GM
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
HEES = (3e-27, 3e-27); PARK = (1.6e-27, 1.8e-27)
BAND_H = (HEES[0] - 2 * HEES[1], HEES[0] + 2 * HEES[1]); BAND_P = (PARK[0] - 2 * PARK[1], PARK[0] + 2 * PARK[1])
R_SAT = 9.58 * AU
LSTARS_PC = [24.0, 50.0, 90.0]
BN11 = (3.8e-26, 1.2e-10, 1.9e-10)
PLANET_BOUNDS = {"Earth": (1.0 * AU, 8.7e-15), "Mars": (1.524 * AU, 1.4e-15), "Saturn": (9.58 * AU, 7.0e-15)}
d7b = json.load(open(rel("doors_push_2026_10_22", "D7b_cassini_Q2", "d7b_cassini_q2_results.json")))
EV = {f: {E: dict(gNe=v["gNe"], ge=v["ge_total"], Q2_D7b=v["Q2_M"]) for E, v in d7b["grid"][f]["none"].items()} for f in A0}
YT = d7b["closure"]["yt_32pi"]
cfg691 = json.load(open(rel("campaign_fresh_gravity", "CFG691_stiffness_window", "cfg691_results.json")))["numbers"]["profile"]["S_table"]
cfg820 = json.load(open(rel("campaign_fresh_gravity", "CFG820_stiffness_from_globulars", "cfg820_results.json")))
GLOB = {"canonical": cfg820["primary (no Pal 3)|canonical"]["L95"], "alt": cfg820["primary (no Pal 3)|alt"]["L95"]}
cfg770 = json.load(open(rel("campaign_fresh_gravity", "CFG770_cassini_stiff_action", "cfg770_results.json")))["numbers"]["T1_Q2"]
A0_770 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
d2 = json.load(open(rel("doors_push_2026_10_22", "D2_wide_binary_fork", "d2_wide_binary_fork_results.json")))["gamma_table"]
D2_20 = {f: d2[f"{f}|PREREG_primary|20"]["avg"] for f in A0}

RES = {"inputs": dict(GM=GM, a0=A0, E=EV, Hees2014=HEES, Park2026=PARK, band_Hees_2sigma=BAND_H, band_Park_2sigma=BAND_P,
                      R_Saturn_AU=9.58, Lstar_pc=LSTARS_PC, BN11_mu1=BN11, planet_bounds=PLANET_BOUNDS, yt_32pi=YT,
                      CFG691_S_table=cfg691, CFG820_L95=GLOB, CFG770_T1=cfg770, D2_gamma20_PREREG_primary=D2_20, mutate=MUT),
       "checks": {}}
CHK = []
def check(name, ok, detail):
    CHK.append(ok); RES["checks"][name] = dict(ok=bool(ok), detail=detail)
    P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")

G1, G2 = (30, 48), (60, 96)
def rich(q1, q2): return (4 * q2 - q1) / 3
def rM_of(a0, gm=GM): return math.sqrt(gm / a0)
def xe_of(f, E): return EV[f][E]["ge"] / A0[f]
def toQ(raw, a0): return -raw * a0 / rM_of(a0)       # Phi-convention dimensionless -> BN11/Hees convention, s^-2
def QF(f_a0, xe, L): return -S.routeF_Q2_raw(GM, L, xe)   # BN11/Hees convention
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
def grid(Lam, gres, rin=1e-5): return S.Grid(rin, 1e4 * max(1.0, Lam), gres[0], gres[1])
def run_v(Lam, xe, gres, U0g=None, rin=1e-5):
    g = grid(Lam, gres, rin)
    U0 = None if U0g is None else S.regrid(U0g[0], U0g[1], g)
    U, fin, it = S.solve_v(g, Lam, xe, scalar_lap=MUT, U0=U0)
    return g, U, fin, it
t0 = time.time()
P("=" * 100)
P("D7d_screened_q2 -- Cassini Q2 of the stiffened DSF-21 action in the Galactic field" + ("  [MUTATE: scalar Laplacian]" if MUT else ""))
P("=" * 100)

# ---------------------------------------------------------------- K1 derivation (sympy)
import sympy as sy
g_, gN, u, a0s = sy.symbols("g g_N u a0", positive=True)
sol_u = sy.solve(sy.Eq(g_, a0s * u / (a0s - u)), u)[0]                 # (P) at L* = 0
k1a = sy.simplify((g_ - sol_u) - g_ ** 2 / (g_ + a0s)) == 0             # (L): g_N = g - u
s_, Lst, rMs, GMs = sy.symbols("s L r_M GM", positive=True)
qf = sy.Function("q")
ell = Lst ** 2 / (2 * rMs); Aamp = a0s * rMs / ell; rr = ell * s_
uu = Aamp * qf(s_)
lapvec = (sy.diff(uu, s_, 2) + 2 * sy.diff(uu, s_) / s_ - 2 * uu / s_ ** 2) / ell ** 2
lhs = -(Lst ** 2 / 2) * lapvec + uu ** 2 / a0s - GMs / rr ** 2              # u << a0 limit of u^2/(a0-u)
target = -(sy.diff(qf(s_), s_, 2) + 2 * sy.diff(qf(s_), s_) / s_ - 2 * qf(s_) / s_ ** 2) + qf(s_) ** 2 - 1 / s_ ** 2
k1b = sy.simplify((lhs / (GMs / ell ** 2) - target).subs(GMs, a0s * rMs ** 2)) == 0
gan = sy.simplify(Aamp * qf(s_) / (sy.sqrt(GMs * a0s) / rr * s_ * qf(s_))).subs(GMs, a0s * rMs ** 2)
k1c = sy.simplify(gan) == 1
check("K1", k1a and k1b and k1c, f"L*=0 -> g_N=g^2/(g+a0): {k1a}; isolated reduction = CFG691 ODE with l=L*^2/(2r_M): {k1b}; g_an=sqrt(GMa0)/r*s*q: {k1c}")

# ---------------------------------------------------------------- K2 Route F at L*=0 = linear AQUAL EFE
cc = np.linspace(-0.999, 0.999, 41); worst = 0.0
for xe in (0.3, 1.0, 1.9, 2.6, 5.0):
    mu = xe / (1 + xe); L0 = 1 / (1 + xe)
    worst = max(worst, float(np.max(np.abs(1 + S.chi(0.0, cc, xe) - 1 / (mu * (1 + L0 * cc ** 2))))))
check("K2", worst < 1e-12, f"max|1+chi - 1/(mu(1+L0 c^2))| = {worst:.1e} <1e-12")

# ---------------------------------------------------------------- K3 QUMOND machinery vs D7b
if MUT: P("  [MUTATE mode: only K1, K2, K5, K6 (L*=30 r_M) are run -- memory/time budget; the mutation touches only Route N's stiffness operator]")
if not MUT:
    k3 = {}; worst = 0.0; signok = True
    for f in A0:
        a0 = A0[f]; rq = R_SAT / rM_of(a0)
        for E in EV[f]:
            xe = xe_of(f, E); qq = []
            for gres in (G1, G2):
                g = grid(0, gres); U = S.solve_qumond(g, xe); qq.append(toQ(S.q2_raw(g, U[0], rq), a0))
            R = rich(*qq); ref = EV[f][E]["Q2_D7b"]
            k3[f"{f}_{E}"] = dict(Q30=qq[0], Q60=qq[1], R=R, D7b=ref, ratio=R / ref)
            worst = max(worst, abs(R / ref - 1)); signok &= (R > 0) == (ref > 0)
    RES["K3_qumond"] = k3
    check("K3", worst < 0.02 and signok, f"max|R/D7b-1| = {worst:.2e} (8 points, sign agree {signok}) <2e-2")

    # ---------------------------------------------------------------- K4 L*=0 is AQUAL: BN11 mu1
    a0b, geb = BN11[1], BN11[2]; xb = geb / a0b; rqb = R_SAT / rM_of(a0b); qq = []
    for gres in (G1, G2):
        g, U, fin, it = run_v(0.0, xb, gres); qq.append(toQ(S.q2_raw(g, U[0], rqb), a0b))
    Rb = rich(*qq); gq = grid(0, G2); Uq = S.solve_qumond(gq, xb); Rq_b = toQ(S.q2_raw(gq, Uq[0], rqb), a0b)
    RES["K4_AQUAL_BN11"] = dict(Q30=qq[0], Q60=qq[1], R=Rb, ratio=Rb / BN11[0])
    check("K4", abs(Rb / BN11[0] - 1) < 0.10, f"AQUAL(L*=0) Q2 = {Rb:.4e} vs BN11 3.8e-26: ratio {Rb / BN11[0]:.4f} (within 10%)")

# ---------------------------------------------------------------- K5 isolated profile vs CFG691
Lam5 = 100.0; ell5 = Lam5 ** 2 / 2
g5 = S.Grid(1e-5, 1e4 * Lam5, 60, 8); U5 = S.solve_isolated(g5, Lam5, scalar_lap=MUT)
Sprof = U5[1].mean(1) * g5.r
k5 = {}; worst = 0.0
for sv in ("0.01", "0.1", "0.3", "1", "3", "10"):
    Sv = float(np.interp(np.log(float(sv) * ell5), g5.x, Sprof)); k5[sv] = dict(S=Sv, CFG691=cfg691[sv], rel=Sv / cfg691[sv] - 1)
    worst = max(worst, abs(Sv / cfg691[sv] - 1))
RES["K5_S_profile"] = k5
check("K5", worst < 0.01, f"isolated L*=100 r_M: max|S/S_CFG691-1| = {worst:.2e} over s=0.01..10 <1e-2")

# ---------------------------------------------------------------- K6 Route N vs Route F (canonical, E0 and E3)
k6 = {}; worst = 0.0; signok = True
a0 = A0["canonical"]; rq = R_SAT / rM_of(a0)
for Lam in ((30.0,) if MUT else (30.0, 100.0)):
    for E in ("E0", "E3"):
        xe = xe_of("canonical", E); qq = []
        for gres in (G1, G2):
            g, U, fin, it = run_v(Lam, xe, gres); qq.append(toQ(S.q2_raw(g, U[0], rq), a0))
        R = rich(*qq); F = QF(a0, xe, Lam * rM_of(a0))
        k6[f"{Lam:g}_{E}"] = dict(Q30=qq[0], Q60=qq[1], R=R, F=F, ratio=R / F)
        worst = max(worst, abs(R / F - 1)); signok &= (R > 0) == (F > 0)
RES["K6_N_vs_F"] = k6
check("K6", worst < 0.05 and signok, f"max|N/F-1| = {worst:.2e} at L*=30,100 r_M (E0,E3), sign agree {signok} <5e-2")

if not MUT:
    # ---------------------------------------------------------------- K7 limits
    xe2 = xe_of("canonical", "E2")
    g0, U0, fin0, _ = run_v(0.0, xe2, G1); Q0 = toQ(S.q2_raw(g0, U0[0], rq), a0)
    gs_, Us_, fins_, _ = run_v(0.01, xe2, G1, U0g=(U0, g0)); Qs_ = toQ(S.q2_raw(gs_, Us_[0], rq), a0)
    QF_inf = QF(a0, xe2, 1e4 * PC)
    RES["K7"] = dict(Q_L0=Q0, Q_L001=Qs_, conv=[fin0, fins_], QF_1e4pc=QF_inf)
    check("K7", abs(Qs_ / Q0 - 1) < 0.02 and abs(QF_inf / Q0) < 1e-9,
          f"(a) N(L*=0.01 r_M)/N(0) - 1 = {Qs_ / Q0 - 1:+.2e} <2e-2; (b) |F(1e4 pc)/AQUAL(0)| = {abs(QF_inf / Q0):.1e} <1e-9")

    # ---------------------------------------------------------------- K8 convergence
    k8 = {}; ok8 = True
    for Lam in (0.0, 3.0):
        qq = []
        for gres in (G1, G2):
            g, U, fin, it = run_v(Lam, xe2, gres); qq.append(toQ(S.q2_raw(g, U[0], rq), a0))
        R = rich(*qq)
        gh, Uh, finh, _ = run_v(Lam, xe2, G2, rin=5e-6); Qh = toQ(S.q2_raw(gh, Uh[0], rq), a0)
        k8[f"L{Lam:g}"] = dict(Q30=qq[0], Q60=qq[1], R=R, corr=abs(R - qq[1]) / abs(R), rin_half=Qh, rin_change=abs(Qh / qq[1] - 1))
        ok8 &= k8[f"L{Lam:g}"]["corr"] < 0.02 and k8[f"L{Lam:g}"]["rin_change"] < 0.02
    fq1 = S.routeF_I2(xe2); fq2 = S.routeF_I2(xe2, nk=8000, nc=128, kmin=1e-5, kmax=2e4)
    k8["routeF_quad_rel"] = abs(fq2 / fq1 - 1); ok8 &= k8["routeF_quad_rel"] < 1e-6
    RES["K8"] = k8
    check("K8", ok8, "Richardson corr L*=0 {:.2e}, 3 r_M {:.2e}; r_in/2 change {:.2e}, {:.2e} (<2e-2); Route F quadrature {:.1e} (<1e-6)".format(
        k8["L0"]["corr"], k8["L3"]["corr"], k8["L0"]["rin_change"], k8["L3"]["rin_change"], k8["routeF_quad_rel"]))

    # ---------------------------------------------------------------- K9 linear validity at 24 pc
    worst = 0.0
    for f in A0:
        for E in EV[f]:
            ue = A0[f] * xe_of(f, E) / (1 + xe_of(f, E)); worst = max(worst, GM / (24 * PC) ** 2 / ue)
    check("K9", worst < 1e-4, f"max (GM/L*^2)/u_e at 24 pc = {worst:.2e} <1e-4")

    # ---------------------------------------------------------------- K10 CFG770 reproduction
    worst = 0.0; signok = True; k10 = {}
    for key, v in cfg770.items():
        f, ge = key.split("_"); ge = float(ge)
        raw = S.routeF_Q2_raw(GM, 5.75 * PC, ge / A0_770[f]); k10[key] = dict(ours_Phi_conv=raw, cfg770=v, ratio=raw / v)
        worst = max(worst, abs(raw / v - 1)); signok &= (raw > 0) == (v > 0)
    RES["K10_CFG770"] = k10
    check("K10", worst < 0.01 and signok, f"Route F at CFG770 inputs: max|ratio-1| = {worst:.2e}, same sign (Phi convention) {signok} <1e-2")
    P(f"  [time {time.time() - t0:.0f}s, max RSS {rss():.2f} GB]")

    # ================================================================= RESULTS
    P("")
    P("R1  Q2 at the physical L* (Route F; BN11/Hees sign; two-sided 2sigma bands Hees [-3.0e-27, 9.0e-27], Park [-2.0e-27, 5.2e-27])")
    R1 = {}
    for f in A0:
        for Lpc in LSTARS_PC:
            row = []
            for E in EV[f]:
                q = QF(A0[f], xe_of(f, E), Lpc * PC); row.append(q)
                R1[f"{f}|{Lpc:g}|{E}"] = dict(Q2=q, hees=BAND_H[0] <= q <= BAND_H[1], park=BAND_P[0] <= q <= BAND_P[1],
                                              over_Hees_upper=q / BAND_H[1])
            ok = all(BAND_H[0] <= q <= BAND_H[1] for q in row)
            P(f"  {f:9s} L*={Lpc:4.0f} pc  Q2 = " + " ".join(f"{q:.3e}" for q in row) +
              f"   max Q2/9e-27 = {max(row) / BAND_H[1]:.2e}   Hees {'PASS' if ok else 'FAIL'}  Park {'PASS' if all(BAND_P[0] <= q <= BAND_P[1] for q in row) else 'FAIL'}")
    RES["R1_physical"] = R1

    P("")
    P("R2  Route N scan for the Cassini lower bound L*_C (two continuation sweeps at (30,48); converged = scaled residual < 1e-9)")
    LGRID = [0.0] + [float(10 ** e) for e in np.arange(-1.5, 2.001, 0.25)]
    R2 = {}
    for f in A0:
        a0 = A0[f]; rM = rM_of(a0); rq = R_SAT / rM
        for E in EV[f]:
            xe = xe_of(f, E); pts = {}
            prev = None
            for Lam in LGRID:                                   # upward sweep
                g, U, fin, it = run_v(Lam, xe, G1, U0g=prev)
                conv = fin < 1e-9; q = toQ(S.q2_raw(g, U[0], rq), a0) if conv else float("nan")
                pts.setdefault(Lam, {})["up"] = dict(conv=bool(conv), Q2=q, res=fin, it=it)
                if conv: prev = (U, g)
            prev = None
            for Lam in LGRID[::-1]:                             # downward sweep
                if Lam == 0.0: continue
                g, U, fin, it = run_v(Lam, xe, G1, U0g=prev)
                conv = fin < 1e-9; q = toQ(S.q2_raw(g, U[0], rq), a0) if conv else float("nan")
                pts[Lam]["down"] = dict(conv=bool(conv), Q2=q, res=fin, it=it)
                if conv: prev = (U, g)
            # score
            status = {}
            for Lam in LGRID:
                qs = [v["Q2"] for v in pts[Lam].values() if v["conv"]]
                status[Lam] = None if not qs else all(BAND_H[0] <= q <= BAND_H[1] for q in qs)
            conv_L = [L for L in LGRID if status[L] is not None]
            lo, hi = None, None
            for i, L in enumerate(conv_L):
                if all(status[M] for M in conv_L[i:]): hi = L; break
            fails_below = [L for L in conv_L if hi is not None and L < hi and not status[L]]
            lo = max(fails_below) if fails_below else None
            nonconv = [L for L in LGRID if status[L] is None]
            # Richardson re-run of the passing endpoint (continuation from the converged G1 solution)
            Rhi = None
            if hi is not None:
                srcs = [k for k in ("down", "up") if pts[hi].get(k, {}).get("conv")]
                g1h, U1h, fin1, _ = run_v(hi, xe, G1)
                if fin1 >= 1e-9:   # need continuation: redo the downward path to hi
                    prev = None
                    for Lam in [L for L in LGRID[::-1] if L >= hi and L > 0]:
                        g1h, U1h, fin1, _ = run_v(Lam, xe, G1, U0g=prev); prev = (U1h, g1h)
                g2h, U2h, fin2, _ = run_v(hi, xe, G2, U0g=(U1h, g1h))
                Rhi = rich(toQ(S.q2_raw(g1h, U1h[0], rq), a0), toQ(S.q2_raw(g2h, U2h[0], rq), a0)) if fin2 < 1e-9 else float("nan")
            R2[f"{f}|{E}"] = dict(points={f"{L:.6g}": pts[L] for L in LGRID}, status={f"{L:.6g}": status[L] for L in LGRID},
                                 bracket_rM=[lo, hi], bracket_pc=[None if lo is None else lo * rM / PC, None if hi is None else hi * rM / PC],
                                 nonconverged_rM=nonconv, Q2_at_hi_Richardson=Rhi, QF_at_hi=None if hi is None else QF(a0, xe, hi * rM),
                                 x_e=xe, cap_edge_rM=math.sqrt(1 + xe))
            line = " ".join(f"{L:.3g}:{'-' if status[L] is None else ('P' if status[L] else 'F')}" for L in LGRID)
            P(f"  {f:9s} {E}: {line}")
            qfh = R2[f"{f}|{E}"]["QF_at_hi"]
            lo_s = "-" if lo is None else f"{lo * rM / PC:.4f}"; hi_s = "-" if hi is None else f"{hi * rM / PC:.4f}"
            P(f"      L*_C bracket = ({lo}, {hi}] r_M = ({lo_s}, {hi_s}] pc; Q2(hi) Richardson "
              f"{'-' if Rhi is None else f'{Rhi:.3e}'}, Route F {'-' if qfh is None else f'{qfh:.3e}'}; "
              f"non-converged {[round(L, 3) for L in nonconv]}; sqrt(1+x_e) = {math.sqrt(1 + xe):.3f}")
            P(f"      Q2 (up / down): " + "; ".join(f"{L:.3g}:" + "/".join(f"{v['Q2']:.2e}" if v["conv"] else "nc" for v in pts[L].values()) for L in LGRID))
        P(f"  [time {time.time() - t0:.0f}s, max RSS {rss():.2f} GB]")
    RES["R2_scan"] = R2
    LC = {}
    for f in A0:
        his = [R2[f"{f}|{E}"]["bracket_pc"][1] for E in EV[f]]; los = [R2[f"{f}|{E}"]["bracket_pc"][0] for E in EV[f]]
        LC[f] = dict(upper_pc=None if None in his else max(his), lower_pc=None if all(v is None for v in los) else max(v for v in los if v is not None),
                     globular_L95_pc=GLOB[f], CFG691_Lmin_pc=5.754)
        P(f"  {f:9s}: Cassini L*_C in ({LC[f]['lower_pc']}, {LC[f]['upper_pc']}] pc (all E)  vs globulars {GLOB[f]:.2f} pc, CFG691 Saturn 5.75 pc")
    RES["L_C"] = LC

    # ---------------------------------------------------------------- consequences
    P("")
    P("C1  Wide binary 1.5 Msun at 20 kAU, gamma_v - 1 (Route F monopole in the Galactic field) vs CFG740 isolated 1/2 (s/L*)^2")
    s20 = 20e3 * AU; GMb = 1.5 * GM; C1 = {}
    for f in A0:
        for Lpc in LSTARS_PC:
            vals = []
            for E in EV[f]:
                a_an = S.routeF_radial(GMb, Lpc * PC, xe_of(f, E), s20); vals.append(math.sqrt(1 + a_an / (GMb / s20 ** 2)) - 1)
            iso = 0.5 * (s20 / (Lpc * PC)) ** 2
            C1[f"{f}|{Lpc:g}"] = dict(gamma_minus_1=vals, CFG740_isolated=iso)
            P(f"  {f:9s} L*={Lpc:4.0f} pc: gamma_v-1 = " + " ".join(f"{v:.3e}" for v in vals) + f"  (isolated {iso:.3e}); unscreened law-first (D2) {D2_20[f]:.3f}")
    RES["C1_wide_binary"] = C1
    P("C2  Inner planets: anomalous radial acceleration (sunward), screened (Route F, E0..E3) vs bounds and vs the unscreened law")
    C2 = {}
    for f in A0:
        for Lpc in LSTARS_PC:
            for name, (r, bnd) in PLANET_BOUNDS.items():
                vals = [S.routeF_radial(GM, Lpc * PC, xe_of(f, E), r) for E in EV[f]]
                C2[f"{f}|{Lpc:g}|{name}"] = dict(a=vals, GM_over_L2=GM / (Lpc * PC) ** 2, bound=bnd, ratio=max(vals) / bnd)
            P(f"  {f:9s} L*={Lpc:4.0f} pc: GM/L*^2 = {GM / (Lpc * PC) ** 2:.3e};  " + "; ".join(
                f"{n} {max(C2[f'{f}|{Lpc:g}|{n}']['a']):.3e} ({max(C2[f'{f}|{Lpc:g}|{n}']['a']) / b[1]:.2e} of bound)" for n, b in PLANET_BOUNDS.items()))
        a0 = A0[f]
        for name, (r, bnd) in PLANET_BOUNDS.items():
            y = GM / r ** 2 / a0; nu1 = (math.sqrt(1 + 4 / y) - 1) / 2
            C2[f"{f}|unscreened|{name}"] = dict(no_turnoff=nu1 * GM / r ** 2, with_P5=nu1 / (1 + (y / YT) ** 2) * GM / r ** 2, bound=bnd)
        P(f"  {f:9s} unscreened law: " + "; ".join(f"{n} no-P5 {C2[f'{f}|unscreened|{n}']['no_turnoff']:.3e} ({C2[f'{f}|unscreened|{n}']['no_turnoff'] / b[1]:.1e}x), "
                                                     f"P5 {C2[f'{f}|unscreened|{n}']['with_P5']:.2e}" for n, b in PLANET_BOUNDS.items()))
    RES["C2_planets"] = C2

    # ---------------------------------------------------------------- outcome
    allpass = all(v["hees"] for v in R1.values())
    lcmax = [LC[f]["upper_pc"] for f in A0]
    if allpass and None not in lcmax and max(lcmax) <= 24:
        outcome = (f"SCREENED THEORY PASSES CASSINI for L* >= L*_C, L*_C <= {max(lcmax):.3f} pc (both footings, all E); "
                   f"consistent with the globulars ({GLOB['canonical']:.2f}/{GLOB['alt']:.2f} pc). The binding lower gate stays CFG691's Saturn monopole (5.75 pc).")
    else:
        outcome = "SCREENING DOES NOT RESCUE Q2 (see R1/R2)"
    RES["outcome"] = outcome
    P("")
    P("OUTCOME: " + outcome)
n_ok = sum(CHK); P(f"\nD7D_SCREENED_Q2 COMPLETE: {n_ok}/{len(CHK)} checks PASS.  [time {time.time() - t0:.0f}s, max RSS {rss():.2f} GB]")
RES["n_pass"], RES["n_checks"] = n_ok, len(CHK)
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o
json.dump(clean(RES), open(os.path.join(HERE, f"d7d_screened_q2_results{TAG}.json"), "w"), indent=1, sort_keys=True)
open(os.path.join(HERE, f"d7d_screened_q2{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n_ok == len(CHK) else 1)
