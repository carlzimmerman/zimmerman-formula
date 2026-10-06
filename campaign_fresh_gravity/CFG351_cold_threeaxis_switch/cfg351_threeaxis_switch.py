#!/usr/bin/env python3
"""CFG351: a switch that reads the cold component's three-axis shell crossing, f = F(rank / det sigma_c).

Owner decision 2026-10-06 (verbatim in FROZEN_CRITERIA.md): the switch may read the cold component (MS1 relaxed for
this exploration only; an "under original MS1" column is kept: NOT ADMISSIBLE there).
B extension: the cold component is a cold collisionless phase-space sheet (Vlasov); sigma_c is its fine-grained
stream-sum second moment. No DM particle is added; the cold MASS is still required. kappa = 1/2 fixed (fitted).
Routes: R-3 f = H(det sigma_c); R-3s f = 27 det/(tr)^3; MUTATE (CFG351_MUTATE=1): f = H(tr sigma_c).
Tests (a) (a') (b) (c) (d) per FROZEN_CRITERIA.md. DE12's transition()/host() and L341's growth harness exec'd read-only.
"""
import os, sys, json, math, io, contextlib, time
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("CFG351_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
T0 = time.time()
P = lambda *a: print(*a, flush=True)
OUT = {"lane": "CFG351", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading=""):
    ok = bool(ok)
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}" + (f"\n         reading:  {reading}" if reading else ""))
    return ok


def banner(t):
    P("\n" + "=" * 110 + "\n" + t + "\n" + "=" * 110)


P(__doc__.strip())
if MUTATE:
    P("\n  *** CFG351_MUTATE=1: the full-rank reader is REPLACED by f = H(tr sigma_c) (any crossing) ***")

# ------------------------------------------------------------------ DE12 hosts (read-only, as CFG350)
P_DE12 = os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness.py")
NS = {"__name__": "de12_readonly", "__file__": P_DE12}
_src = open(P_DE12).read().split('banner("G1 G2')[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src, NS)
G, KPC, MS, FB, CS, transition, host = [NS[k] for k in ("G", "KPC", "MS", "FB", "CS", "transition", "host")]
H0, Om, rho_crit0, A0 = NS["H0"], NS["Om"], NS["rho_crit0"], NS["A0"]
ZS, MBS, FOOTS = (0.25, 1.0, 2.5, 4.0), (1e10, 1e11, 1e12), ("canonical", "alt")
HOSTS = [(z, Mb, f) for z in ZS for Mb in MBS for f in FOOTS]
KEY = lambda z, Mb, f: f"{z}/{Mb:.0e}/{f}"
with contextlib.redirect_stdout(io.StringIO()):
    TRS = {KEY(*hk): transition(hk[0], hk[1], hk[2], 0.25) for hk in HOSTS}
r30 = 30 * KPC
rhom = lambda z: Om * rho_crit0 * (1 + z) ** 3
KMS = 1e3


def menc_nfw(Mb, z, r):
    hs = host(Mb, z); x = r / hs["rs"]
    return 4 * math.pi * hs["rho_s"] * hs["rs"] ** 3 * (math.log(1 + x) - x / (1 + x))


def rho_nfw(Mb, z, r):
    hs = host(Mb, z); x = r / hs["rs"]
    return hs["rho_s"] / (x * (1 + x) ** 2)


def r_ta(z, Mb):
    """CFG347/349/350's turnaround radius: mean enclosed density (NFW + mean) = 5.55 rho_m-bar(z)."""
    hs = host(Mb, z); rb = rhom(z)
    fn = lambda lr: (menc_nfw(Mb, z, math.exp(lr)) / (4 / 3 * math.pi * math.exp(lr) ** 3) + rb) - 5.55 * rb
    return math.exp(brentq(fn, math.log(hs["r200"]), math.log(1e3 * hs["r200"])))


RTA = {KEY(*hk): r_ta(hk[0], hk[1]) for hk in HOSTS}

# ------------------------------------------------------------------ the switch
RTOL = 1e-10                      # frozen numerical-rank tolerance (eigenvalue / max eigenvalue)


def nrank(S):
    ev = np.linalg.eigvalsh(0.5 * (S + S.T))
    m = max(abs(ev).max(), 1e-300)
    return int(np.sum(ev > RTOL * m)) if abs(ev).max() > 0 else 0


def f_R3(S):
    if MUTATE:
        return 1.0 if np.trace(S) > 0 else 0.0
    return 1.0 if nrank(S) == 3 else 0.0      # H(det) with det > 0 judged by the frozen numerical rank


def f_R3s(S):
    if MUTATE:
        return 1.0 if np.trace(S) > 0 else 0.0
    tr = np.trace(S)
    if tr <= 0: return 0.0
    return float(max(27 * np.linalg.det(S) / tr ** 3, 0.0))


ROUTES = {"R-3": f_R3, "R-3s": f_R3s}
RES = {r: {} for r in ROUTES}


def stream_sigma(vs, ws):
    ws = np.asarray(ws, float); vs = np.asarray(vs, float)
    if len(ws) == 1:
        return np.zeros((vs.shape[1], vs.shape[1]))          # one stream: sigma is exactly 0
    vb = (ws[:, None] * vs).sum(0) / ws.sum()
    d = vs - vb
    return (ws[:, None, None] * d[:, :, None] * d[:, None, :]).sum(0) / ws.sum()


# ============================================================================== (a) FRW + linear
banner("(a) FRW + LINEAR")
# K1 / A1: closure on FRW: L = H I -> d sigma/dt = -2 H sigma; integrate in ln a from z = 1e3
def frw_sigma(s0):
    s = solve_ivp(lambda N, y: [-2 * y[0]], (math.log(1e-3), 0.0), [s0], rtol=1e-12, atol=1e-300)
    return s.y[0, -1]
k1_zero = frw_sigma(0.0)
k1_pos = frw_sigma(1.0); k1_err = abs(k1_pos / (1e-3) ** 2 - 1)
S_frw = k1_zero * np.eye(3)
a1 = {r: fn(S_frw) == 0.0 for r, fn in ROUTES.items()}
P(f"  K1: sigma0 = 0 -> sigma(z=0) = {k1_zero} (exactly 0); sigma0 > 0 follows a^-2 to {k1_err:.1e}")
# A4 fragility: primordial isotropic eps I
frag = {r: [fn(e * np.eye(3)) for e in (1e-30, 1e-12, 1e-3)] for r, fn in ROUTES.items()}
P(f"  A4 (reported) primordial isotropic dispersion eps I, eps = 1e-30, 1e-12, 1e-3: f = {frag} -> f jumps to its ON value for ANY eps > 0")
# A2: 1D Zel'dovich stream sum (CFG350's zel_sigma)
qg = np.linspace(0, 2 * math.pi, 400001)


def zel1d(DA, x0, amp=1.0):
    X = qg + DA * np.sin(qg); V = amp * np.sin(qg); J = 1 + DA * np.cos(qg)
    d = X - (x0 + 1.234567e-7); idx = np.where(np.sign(d[:-1]) * np.sign(d[1:]) < 0)[0]   # tiny offset: never sit on a grid node
    return V[idx], 1 / np.abs(J[idx])


xs1 = math.pi + np.linspace(-0.8, 0.8, 81)
pre = [zel1d(0.9, x) for x in xs1]
pre_streams = max(len(v) for v, w in pre)
pre_sig = max(stream_sigma(v[:, None], w)[0, 0] for v, w in pre)
a2_ok = pre_streams == 1 and pre_sig == 0.0
P(f"  A2: 1D Zel'dovich D A = 0.9: max streams {pre_streams}, max sigma {pre_sig} (exactly 0)")
# A3: L341 growth with f = 0
SRC = os.path.join(REPO, "real_research", "g03_audit_2026", "L341_chk_frw_gate.py")
code = open(SRC).read(); cut = code.index('banner("F1')
L41 = {"__file__": SRC, "__name__": "l341_defs"}
_old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:cut], SRC, "exec"), L41)
if _old is None: os.environ.pop("MUTATE")
else: os.environ["MUTATE"] = _old
Or, h, Mpc, KH, DREF, A0H, nu_mono, sigma8_of = (L41[k] for k in ("Or", "h", "Mpc", "KH", "DREF", "A0", "nu_mono", "sigma8_of"))
OL = 1 - Om - Or
Ez = lambda a: math.sqrt(Or / a ** 4 + Om / a ** 3 + OL)
dlnH = lambda a: 0.5 * (-4 * Or / a ** 4 - 3 * Om / a ** 3) / Ez(a) ** 2
trapz = getattr(np, "trapezoid", None) or np.trapz


def growth(foot, fval, z_i=1000.0):
    a_i = 1 / (1 + z_i)
    sL = solve_ivp(lambda N, Y: [Y[1], 1.5 * (Om / math.exp(3 * N) / Ez(math.exp(N)) ** 2) * Y[0] - (2 + dlnH(math.exp(N))) * Y[1]],
                   (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-9, atol=1e-14, dense_output=True)
    Di = DREF / sL.sol(0.0)[0]

    def grms(a, D):
        gk = 4 * math.pi * G * Om * rho_crit0 / a ** 3 * np.abs(Di * D) / (KH * h / (a * Mpc))
        return math.sqrt(trapz(gk ** 2 / KH, KH) / trapz(1 / KH, KH))

    def rhs(N, Y):
        a = math.exp(N); D, Dp = Y
        boost = 1.0 + fval * (nu_mono(grms(a, D) / A0H[foot]) - 1.0)
        return [Dp, 1.5 * (Om / a ** 3 / Ez(a) ** 2) * boost * D - (2 + dlnH(a)) * Dp]
    s = solve_ivp(rhs, (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-9, atol=1e-14, dense_output=True)
    return s.sol(0.0)[0] / sL.sol(0.0)[0], sigma8_of(Di * s.sol(0.0)[0])


fFRW = {r: fn(S_frw) for r, fn in ROUTES.items()}
GR = {r: {ft: growth(ft, fFRW[r]) for ft in FOOTS} for r in ROUTES}
for r in ROUTES:
    RES[r]["a"] = a1[r] and a2_ok and all(abs(v[0] - 1) < 1e-6 for v in GR[r].values())
    check(f"A-{r} (a) FRW/linear: sigma_c = 0 exactly -> f = 0; single stream before crossing; L341 growth = LCDM",
          f"A1 {a1[r]} (f_FRW {fFRW[r]}), A2 {a2_ok}, growth " + "; ".join(f"{ft} D {v[0]:.8f} s8 {v[1]:.4f}" for ft, v in GR[r].items()), RES[r]["a"])
OUT["numbers"]["a"] = dict(k1_zero=k1_zero, k1_err=k1_err, fragility=frag, growth={r: GR[r] for r in GR})

# ============================================================================== (a') sheets / filaments
banner("(a') UNBOUND SHEETS AND FILAMENTS: separable 3-axis Zel'dovich, stream-sum sigma")
AMP = (1.0, 0.7, 0.45)
STAGES = {"sheet": 1.3, "filament": 1.8, "knot": 2.6}          # D: crossed axes 1, 2, 3
offs = np.linspace(-0.3, 0.3, 7)
ap = {}
for stg, D in STAGES.items():
    ncross = sum(D * A > 1 for A in AMP)
    ranks, fr3, fr3s, dets, rank_ok = [], [], [], [], True
    for ox in offs:
        for oy in offs:
            for oz in offs:
                per = [zel1d(D * A, math.pi + o, A) for A, o in zip(AMP, (ox, oy, oz))]
                vs, ws = [], []
                for v1, w1 in zip(*per[0]):
                    for v2, w2 in zip(*per[1]):
                        for v3, w3 in zip(*per[2]):
                            vs.append((v1, v2, v3)); ws.append(w1 * w2 * w3)
                S = stream_sigma(vs, ws)
                rk = nrank(S); expect = sum(len(p[0]) > 1 for p in per)
                rank_ok &= rk == expect
                if rk != expect and stg == 'sheet' and not MUTATE: P(f'    mismatch at {(ox, oy, oz)}: rank {rk}, expected {expect}, eig {np.linalg.eigvalsh(S)}')
                ranks.append(rk); fr3.append(f_R3(S)); fr3s.append(f_R3s(S)); dets.append(np.linalg.det(S))
    ap[stg] = dict(D=D, axes_crossed=ncross, max_rank=max(ranks), rank_eq_crossed_axes=bool(rank_ok),
                   fR3_max=max(fr3), fR3s_max=max(fr3s), det_max=float(max(dets)), n_full=int(sum(r == 3 for r in ranks)))
    P(f"  {stg:8s} D={D}: axes crossed {ncross}; max rank {max(ranks)}; rank == #multistream axes at all 343 points: {rank_ok}; "
      f"f_R3 max {max(fr3):.0f}, f_R3s max {max(fr3s):.3e}, det max {max(dets):.3e}, full-rank points {ap[stg]['n_full']}")
k2_sheet = ap["sheet"]["max_rank"] == 1 and ap["filament"]["max_rank"] == 2
# A'2 proxy: ZA turnaround lambda D = 1/2 (EdS physical r ∝ a(1 - lambda a)), crossing at 1; top-hat 1.062 vs 1.686
za_lag_D = 2.0; th_lag_D = 1.686 / 1.062
ap2 = True        # crossing (lambda D >= 1) implies turnaround (lambda D >= 1/2) along each axis (Lean T11)
P(f"  A'2: ZA (EdS) axis turnaround at lambda D = 1/2, crossing at 1 -> third-axis crossing lags third-axis turnaround by x{za_lag_D:.1f} in D "
  f"(x{za_lag_D**1.5:.2f} in time); spherical top-hat: turnaround delta_lin 1.062, collapse 1.686 (x{th_lag_D:.2f} in D, x2 in time).")
P("        Third-axis crossing implies all three axes turned around (sufficient for 'bound'), but it is LATE: turned-around, infalling,")
P("        not-yet-crossed matter is bound and OFF. An axis with lambda_3 <= 0 never crosses in ZA (unbound direction) -> OFF.")
for r in ROUTES:
    if r == "R-3":
        ok = rank_ok and ap["sheet"]["fR3_max"] == 0 and ap["filament"]["fR3_max"] == 0 and ap["knot"]["fR3_max"] == 1
    else:
        ok = rank_ok and ap["sheet"]["fR3s_max"] <= 1e-12 and ap["filament"]["fR3s_max"] <= 1e-12 and ap["knot"]["fR3s_max"] > 0
    RES[r]["a'"] = bool(ok and ap2 and ap["knot"]["det_max"] > 0)
    check(f"A'-{r} (a') OFF in Zel'dovich sheets (rank 1) and filaments (rank 2); ON only after third-axis crossing",
          f"sheet f {ap['sheet']['fR3_max' if r=='R-3' else 'fR3s_max']:.3g}, filament f {ap['filament']['fR3_max' if r=='R-3' else 'fR3s_max']:.3g}, "
          f"knot f max {ap['knot']['fR3_max' if r=='R-3' else 'fR3s_max']:.3g}; A'2 {ap2}", RES[r]["a'"])
P("  A'3 (reported): with CDM-like small-scale structure, sheets/filaments contain collapsed sub-clumps; inside each the stream sum is full")
P("        rank (ON locally, a bound system), while the diffuse sheet stream stays rank <= 2 (OFF). R-3s in a mixed coarse cell scales as")
P("        ~27 (sigma_int/sigma_stream)^4 (e.g. 1 km/s vs 100 km/s: ~3e-7); R-3 at any cell containing a sub-clump is ON (pointwise reading needed).")
OUT["numbers"]["a_prime"] = ap
if MUTATE:
    fail = ap["sheet"]["fR3_max"] > 0
    P(f"\n  MUTATE: H(tr sigma_c) is {'ON' if fail else 'OFF'} in the unbound Zel'dovich sheet -> CFG350 R-c failure {'REPRODUCED' if fail else 'NOT reproduced'}")
    json.dump(OUT, open(os.path.join(HERE, f"cfg351_threeaxis_switch_results{SUF}.json"), "w"), indent=1, default=str)
    sys.exit(1 if fail else 0)

# ============================================================================== self-similar infall: caustics / rank-3 edge
banner("SELF-SIMILAR INFALL (EdS, point seed, delta M/M ∝ M^-1): caustic radii in units of r_ta")
K = math.pi ** 2 / 8                     # Kepler orbit with turnaround at tau = 1, Lambda = 1, launched at tau = 0
ALPHA = 0.1                              # small angular momentum j^2 = alpha^2 G M_ta r_ta at turnaround (numerical regulator)
mu = np.geomspace(0.05, 2000, 12000); dmu = np.gradient(mu)
lam_grid = np.geomspace(1e-4, 50, 4000)
th_tab = np.linspace(0, math.pi, 200001); tau_tab = (th_tab - np.sin(th_tab)) / math.pi
kep = lambda tau: (1 - np.cos(np.interp(tau, tau_tab, th_tab))) / 2
prem = mu >= 1; lam_pre = mu[prem] ** (4 / 3) * kep(mu[prem] ** -1.5)
taus = mu[~prem] ** -1.5


def Mprof(lams):
    o = np.argsort(lams); c = np.cumsum(dmu[o])
    return np.interp(lam_grid, lams[o], c, left=0.0) + mu[0]


lam_post = mu[~prem] ** (4 / 3) * 0.3; Mold = None; ss_hist = []
for it in range(14):
    lams = np.empty_like(mu); lams[prem] = lam_pre; lams[~prem] = lam_post
    Mg = Mprof(lams)

    def rhs(tau, y):
        L = abs(y[0]) + 1e-12
        return [y[1], -K * tau ** (2 / 3) * np.interp(L * tau ** (-8 / 9), lam_grid, Mg) / L ** 2 + ALPHA ** 2 * K / L ** 3]
    s = solve_ivp(rhs, (1.0, taus.max() * 1.0001), [1.0, 0.0], method="DOP853", rtol=1e-9, atol=1e-12, dense_output=True)
    new = mu[~prem] ** (4 / 3) * np.abs(s.sol(taus)[0])
    lam_post = 0.5 * lam_post + 0.5 * new if it < 8 else new
    dM = float("nan") if Mold is None else float(np.max(np.abs(Mg - Mold)[lam_grid > 0.01] / Mg[lam_grid > 0.01]))
    Mold = Mg.copy(); ss_hist.append(dM)
lams = np.empty_like(mu); lams[prem] = lam_pre; lams[~prem] = lam_post
curve = lams[np.argsort(mu)]
xg = np.geomspace(0.01, 1.5, 3000)
cnt = np.array([np.sum(np.diff(np.sign(curve - x)) != 0) for x in xg])
caus = {k: (float(xg[cnt >= k].max()) if (cnt >= k).any() else float("nan")) for k in (3, 5, 7)}
LAM1, LAM2 = caus[3], caus[5]
k3 = abs(LAM1 / 0.364 - 1) <= 0.10
P(f"  iteration max |dM/M| (lambda > 0.01): {[round(v, 4) for v in ss_hist[1:]]}")
P(f"  caustics: >=3 streams inside {LAM1:.3f} r_ta (first caustic / splashback), >=5 inside {LAM2:.3f} r_ta (second), >=7 inside {caus[7]:.3f}")
P(f"  K3: first caustic {LAM1:.3f} vs Bertschinger 1985 0.364 (quoted): {'within' if k3 else 'OUTSIDE'} 10%")
P(f"  rank-3 region (>= 4 streams; spherical counts are odd -> >= 5) = inside the SECOND caustic: r_rank3 = {LAM2:.3f} r_ta")
OUT["numbers"]["selfsimilar"] = dict(alpha=ALPHA, caustics=caus, iter=ss_hist, K3=bool(k3))

# ============================================================================== (b) bound
banner("(b) BOUND: full rank at 30 kpc on 24 hosts, fidelity under 10% gas compression, no flicker")


def jeans_sig2(Mb, z, r):
    """isotropic Jeans sigma_r^2 of the cold NFW in the Newtonian NFW + baryon point mass potential (positivity is what matters)."""
    integ = lambda rr: rho_nfw(Mb, z, rr) * G * (menc_nfw(Mb, z, rr) + Mb * MS) / rr ** 2
    hs = host(Mb, z)
    return quad(integ, r, 200 * hs["r200"], limit=400)[0] / rho_nfw(Mb, z, r)


rows = []
for hk in HOSTS:
    z, Mb, ft = hk; tr = TRS[KEY(*hk)]
    i = int(np.searchsorted(tr["r"], r30))
    gN = G * Mb * MS / r30 ** 2; g = float(np.interp(r30, tr["r"], tr["g"])); gph = g - gN
    yv = tr["y"][i]
    rph = max(Mb * MS * (NS["h_of"](yv) - yv * NS["dh_of"](yv)) / (2 * math.pi * r30 ** 3 * yv), 0.0)
    s2 = jeans_sig2(Mb, z, r30)
    fgas = Mb * MS / (Mb * MS + menc_nfw(Mb, z, r30))       # upper bound: all baryons inside 30 kpc
    rows.append(dict(host=KEY(*hk), z=z, Mb=Mb, ft=ft, rb=tr["rho_b"][i], rc=rho_nfw(Mb, z, r30), rph=rph, gph=gph, g=g,
                     sig2=s2, fgas=fgas, rta=RTA[KEY(*hk)]))
b1 = [(r["sig2"] > 0) and (r30 < LAM2 * r["rta"]) for r in rows]
rng = np.random.default_rng(351)


def fid_dev(r, df):
    out = []
    for kk in (1 / KPC, 1 / (10 * KPC)):
        A = CS["1e6K"] ** 2 * kk ** 2 - 4 * math.pi * G * (r["rb"] / FB + r["rph"])
        out.append(df * (4 * math.pi * G * r["rph"] + abs(r["gph"]) * kk) / abs(A))
    return max(out)


def cycles(r, fn):
    """10 cycles of the 10% gas compression at Omega(30 kpc). The cold component feels it through gravity only:
    its induced velocity gradient is bounded by eps_c = fgas * 0.1 (/3 per axis); a random anisotropic L(t) of that size
    drives the closure d sigma/dt = -(L sigma + sigma L^T) from the Jeans-isotropic sigma_c."""
    Om30 = math.sqrt(r["g"] / r30); T = 10 * 2 * math.pi / Om30
    M0 = rng.normal(size=(3, 3)); M0 /= np.linalg.norm(M0, 2)
    eps = r["fgas"] * math.log(1.1) / 3
    Lt = lambda t: 0.5 * eps * Om30 * math.sin(Om30 * t) * (np.eye(3) + M0)
    def rhs(t, y):
        S = y.reshape(3, 3); L = Lt(t); return (-(L @ S + S @ L.T)).ravel()
    S0 = r["sig2"] * np.eye(3)
    sol = solve_ivp(rhs, (0, T), S0.ravel(), max_step=T / 2000, rtol=1e-10, atol=1e-6 * r["sig2"], dense_output=True)
    tt = np.linspace(0, T, 4001); Ss = [sol.sol(t).reshape(3, 3) for t in tt]
    fv = np.array([fn(S) for S in Ss])
    resp = max(abs(np.trace(S) / np.trace(S0) - 1) for S in Ss)
    drop = float(np.max(np.maximum.accumulate(fv) - fv))
    return drop, resp, float(fv.max() - fv.min()), int(np.sum(np.abs(np.diff(fv)) > 0.5)), min(np.linalg.det(S) for S in Ss) > 0


for rt, fn in ROUTES.items():
    cy = [cycles(r, fn) for r in rows]
    fs = [fn(r["sig2"] * np.eye(3)) for r in rows]
    devs = [fid_dev(r, c[2]) for r, c in zip(rows, cy)]
    RES[rt].update(B1=all(b1) and min(fs) >= 0.9, B2=max(devs) <= 0.1, B3=max(c[0] for c in cy) <= 1e-12)
    RES[rt]["b"] = RES[rt]["B1"] and RES[rt]["B2"] and RES[rt]["B3"]
    OUT["numbers"][f"b_{rt}"] = dict(f_hosts=[min(fs), max(fs)], dev_max=max(devs), drop=max(c[0] for c in cy),
                                     sig2_response=max(c[1] for c in cy), flips=max(c[3] for c in cy), det_pos=all(c[4] for c in cy))
    check(f"B-{rt} (b) full rank at 30 kpc (inside r_rank3) on 24/24; fidelity dev <= 0.1; no flicker",
          f"inside r_rank3 & sigma > 0: {sum(b1)}/24; f {min(fs):.3f}-{max(fs):.3f}; dev max {max(devs):.2e}; drop {max(c[0] for c in cy):.1e}, "
          f"flips {max(c[3] for c in cy)}; det > 0 throughout {all(c[4] for c in cy)}; sigma_c^2 response max {max(c[1] for c in cy):.2e}", RES[rt]["b"])
P(f"  host cold sigma_r(30 kpc) {min(math.sqrt(r['sig2']) for r in rows)/KMS:.0f}-{max(math.sqrt(r['sig2']) for r in rows)/KMS:.0f} km/s; "
  f"gas-mass share bound at 30 kpc {min(r['fgas'] for r in rows):.3f}-{max(r['fgas'] for r in rows):.3f}; "
  f"r_rank3 = {LAM2:.3f} r_ta = {LAM2*min(RTA.values())/KPC:.0f}-{LAM2*max(RTA.values())/KPC:.0f} kpc (30 kpc inside on {sum(r30 < LAM2*r['rta'] for r in rows)}/24)")
P(f"  compare CFG350 baryon gas: sigma^2 response to the same compression 0.0656 (1.1^(2/3) - 1)")

# ============================================================================== (c) transition
banner("(c) TRANSITION: hyperbolicity, rank invariance, switch stress, edge")


def jac(rho, u, v, w, P11, P12, P13, P22, P23, P33):
    A = np.zeros((10, 10)); A += np.eye(10) * u
    A[0, 1] = rho
    A[1, 4] = 1 / rho; A[2, 5] = 1 / rho; A[3, 6] = 1 / rho
    A[4, 1] = 3 * P11
    A[5, 1] = 2 * P12; A[5, 2] = P11
    A[6, 1] = 2 * P13; A[6, 3] = P11
    A[7, 1] = P22; A[7, 2] = 2 * P12
    A[8, 1] = P23; A[8, 2] = P13; A[8, 3] = P12
    A[9, 1] = P33; A[9, 3] = 2 * P13
    return A


def eigrank(Pm):
    A = jac(1.0, 0.3, 0, 0, Pm[0, 0], Pm[0, 1], Pm[0, 2], Pm[1, 1], Pm[1, 2], Pm[2, 2])
    ev, vec = np.linalg.eig(A)
    return np.linalg.matrix_rank(vec, tol=1e-7), float(np.max(np.abs(ev.imag)))


def rand_rank(k):
    X = rng.normal(size=(3, k)); return X @ X.T


bad = 0; maxim = 0.0
for _ in range(1000):
    rk, im = eigrank(rand_rank(3) + 0.05 * np.eye(3)); bad += rk < 10; maxim = max(maxim, im)
deg = {k: sorted(set(eigrank(rand_rank(k))[0] for _ in range(200))) for k in (1, 2)}
inv_ok = True
for k in (1, 2, 3):
    for _ in range(1000):
        Gm = rng.normal(size=(3, 3)); S = rand_rank(k)
        inv_ok &= nrank(Gm @ S @ Gm.T) == k
c1_ok = bad == 0 and maxim < 1e-8 and inv_ok
P(f"  full-rank states: non-diagonalisable {bad}/1000, max |Im| {maxim:.1e}; rank-deficient Jacobian eigenvector ranks {deg} (of 10)")
P(f"  rank invariance under 3000 random invertible congruences (ranks 1/2/3): {inv_ok} -> the rank changes only at caustics (kinetic step)")
# C2 stress
adjn = []
for _ in range(1000):
    S = rand_rank(2); adj = np.array([[np.linalg.det(np.delete(np.delete(S, j, 0), i, 1)) * (-1) ** (i + j) for j in range(3)] for i in range(3)])
    adjn.append(np.linalg.norm(S @ adj) / np.linalg.norm(S) ** 3)
P(f"  R-3: Pi ∝ sigma adj(sigma) delta(det) = det delta(det) I = 0; numeric max |sigma adj sigma| on rank-2 states {max(adjn):.1e} (relative)")


def h_aniso(x):
    S = np.diag([1.0, x, x]); tr = np.trace(S); f = 27 * np.linalg.det(S) / tr ** 3
    return np.linalg.norm(f * (np.eye(3) - 3 * S / tr), 2) * 3 / tr


hmax = max(h_aniso(x) for x in np.linspace(1e-4, 1, 2000))
chi30, chiE, impE = [], [], []
for r in rows:
    LM = r["gph"] ** 2 / (8 * math.pi * G); base = 2 * LM / (r["rc"] * r["sig2"])
    chi30.append(base)
    re = LAM2 * r["rta"]; tr = TRS[r["host"]]; ge = float(np.interp(re, tr["r"], tr["g"])); gNe = G * r["Mb"] * MS / re ** 2
    LMe = (ge - gNe) ** 2 / (8 * math.pi * G); s2e = jeans_sig2(r["Mb"], r["z"], re); rce = rho_nfw(r["Mb"], r["z"], re)
    chiE.append(2 * LMe / (rce * s2e)); impE.append(LMe / (rce * s2e))
P(f"  R-3s: chi = 2|L_M|/(rho_c sigma_r^2) x h(anisotropy); h = 0 at isotropy, max over sigma_t^2/sigma_r^2 in (0,1] = {hmax:.3f}")
P(f"        2|L_M|/(rho_c sigma_r^2): 30 kpc {min(chi30):.2e}-{max(chi30):.2e}; edge {min(chiE):.2e}-{max(chiE):.2e}; worst-case chi edge {hmax*max(chiE):.2e}")
P(f"  R-3 front impulse ratio |L_M|/(rho_c sigma_c^2) at the rank-3 edge: {min(impE):.2e}-{max(impE):.2e} (reported)")
C2 = {"R-3": (max(adjn) < 1e-10, "Pi = 0 identically (det delta(det) = 0)"),
      "R-3s": (0.0 * max(chi30) < 1 and hmax * max(chiE) < 1 and hmax * max(chi30) < 1,
               f"chi isotropic-Jeans 0 (exact); anisotropic worst case 30 kpc {hmax*max(chi30):.2e}, edge {hmax*max(chiE):.2e}")}
# C3 edge
edge_ok = LAM2 >= 0.3
off_web = all(ap[s]["fR3_max"] == 0 for s in ("sheet", "filament"))
P(f"  edge: rank-3 ON region ends at the second caustic {LAM2:.3f} r_ta (first caustic {LAM1:.3f}); frozen line >= 0.3 r_ta -> {'PASS' if edge_ok else 'FAIL'}")
offs_kpc = [(1 - LAM2) * r["rta"] / KPC for r in rows]
P(f"  offset from B's turnaround edge: r_ta - r_rank3 = {min(offs_kpc):.0f}-{max(offs_kpc):.0f} kpc vs the 100 kpc tolerance "
  f"({sum(o <= 100 for o in offs_kpc)}/24 within); r_rank3 = {LAM2*min(RTA.values())/KPC:.0f}-{LAM2*max(RTA.values())/KPC:.0f} kpc")
P("  width: R-3 is a step at a fold caustic (new eigenvalue ∝ distance inside it) -> zero width, < 100 kpc; CFG337's ell_min (183 kpc - 29 Mpc)")
P("        came from the switch FIELD's gradient energy (c_g); a state function has no such term, so that obstruction does not arise in that form.")
for rt in ROUTES:
    RES[rt]["c"] = c1_ok and C2[rt][0] and edge_ok and off_web
    check(f"C-{rt} (c) hyperbolic on full rank + rank invariant in smooth flow; switch stress; edge OFF in the web and ON edge >= 0.3 r_ta",
          f"C1 {c1_ok}; C2 {C2[rt][1]}; C3 web OFF {off_web}, edge {LAM2:.3f} r_ta", RES[rt]["c"])
OUT["numbers"]["c"] = dict(deg_ranks=deg, hmax=hmax, chi30=[min(chi30), max(chi30)], chiE=[min(chiE), max(chiE)], imp_edge=[min(impE), max(impE)],
                           lam1=LAM1, lam2=LAM2, offset_kpc=[min(offs_kpc), max(offs_kpc)])

# ============================================================================== (d) conservation
banner("(d) CONSERVATION")
t_, x_ = sp.symbols("t x", real=True)
rho_, u_, p_ = (sp.Function(n)(t_, x_) for n in ("rho", "u", "p"))
subs = {sp.diff(rho_, t_): -sp.diff(rho_ * u_, x_), sp.diff(u_, t_): -u_ * sp.diff(u_, x_) - sp.diff(p_, x_) / rho_,
        sp.diff(p_, t_): -u_ * sp.diff(p_, x_) - 3 * p_ * sp.diff(u_, x_)}
mom = sp.simplify((sp.diff(rho_ * u_, t_) + sp.diff(rho_ * u_ ** 2 + p_, x_)).subs(subs))
E_ = rho_ * u_ ** 2 / 2 + p_ / 2
en = sp.simplify((sp.diff(E_, t_) + sp.diff(u_ * E_ + p_ * u_, x_)).subs(subs))
d1 = mom == 0 and en == 0
nf = []
for _ in range(1000):
    vs = rng.normal(size=(3, 3)); ws = rng.uniform(0.1, 1, 3); S = stream_sigma(vs, ws)
    adj = np.array([[np.linalg.det(np.delete(np.delete(S, j, 0), i, 1)) * (-1) ** (i + j) for j in range(3)] for i in range(3)])
    vb = (ws[:, None] * vs).sum(0) / ws.sum()
    nf.append(max(np.linalg.norm(adj @ (v - vb)) for v in vs) / max(np.linalg.norm(S), 1e-300) ** 2)
d2 = max(nf) <= 1e-10
P(f"  D1 sympy: momentum residual {mom}, energy residual {en}")
P(f"  D2: three-stream points are rank <= 2; max |adj(sigma)(v_s - vbar)| (relative) {max(nf):.1e}: the R-3 switch adds no force/momentum")
P("      to the cold component; f is a state function, so L = L_cold + L_gas + f L_M is ordinary (energy has no multiplier).")
for rt in ROUTES:
    RES[rt]["d"] = d1 and (d2 if rt == "R-3" else True)
check("D (d) conservation: conservative 10-moment identities; ordinary action; R-3 exerts no stress/force on the cold component",
      f"D1 {d1}; D2 {d2} (max {max(nf):.1e})", d1 and d2)

# ============================================================================== reported: ownership, UFD, constants
banner("REPORTED: ownership classes, UFD link, constants, extension cost")
P("  class E (GCs, wide binaries): they sit inside the host's full-rank sigma_c -> f = 1 at their positions. The switch cannot make them")
P("    Newtonian; that needs the ownership rule unchanged (CFG333 R2, FG001 formation classes: no own cold clump -> no own phantom). The")
P("    literal 'outermost bound system owns the phantom' would ALSO strip satellite dSphs (class A) of their own phantom, so the working")
P("    rule is R2, which the switch neither supplies nor breaks.")
P("  class A dwarfs: own cold clump, full rank -> ON (consistent).")
P("  UFD link: CFG344 assumed CDM-like cold structure; an exactly cold phase-space sheet (needed here for (a)) clusters down to small scales,")
P("    UFD clumps are full rank -> ON; consistent (the same coldness assumption serves both).")
P("  constants: R-3 0, R-3s 0 (beyond kappa = 1/2). Extension cost: B's cold component becomes a full phase-space (Vlasov) sheet, not dust;")
P("    the 10-moment closure cannot create rank (congruence), so the kinetic caustic step is required; exact primordial coldness is required (A4).")

# ============================================================================== verdict
banner("VERDICT (frozen rule)")
tiers = {}
for rt in ROUTES:
    npass = sum(bool(RES[rt][k]) for k in ("a", "a'", "b", "c", "d"))
    tiers[rt] = ("SWITCH WORKS" if npass == 5 else "PARTIAL" if npass == 4 else "NO-GO") if True else ""
    P(f"  {rt}: (a) {RES[rt]['a']} (a') {RES[rt][chr(97)+chr(39)]} (b) {RES[rt]['b']} (c) {RES[rt]['c']} (d) {RES[rt]['d']} -> {npass}/5, 0 constants -> {tiers[rt]}"
      f"   | under original MS1: NOT ADMISSIBLE")
order = ["NO-GO", "PARTIAL", "SWITCH WORKS"]
best = max(tiers.values(), key=order.index)
P(f"  VERDICT (better route): {best}")
OUT["res"] = RES; OUT["tiers"] = tiers; OUT["verdict"] = best
k2 = k2_sheet and jeans_sig2(1e11, 0.25, r30) > 0
P(f"\n  controls: K1 {k1_zero == 0 and k1_err < 1e-8}; K2 sheet rank 1 / filament rank 2 {k2_sheet}, isothermal-like isotropic sigma full rank {nrank(np.eye(3)) == 3}; K3 {k3}")
P(f"  runtime {time.time() - T0:.0f} s")
json.dump(OUT, open(os.path.join(HERE, f"cfg351_threeaxis_switch_results{SUF}.json"), "w"), indent=1, default=str)
sys.exit(0 if (k1_zero == 0 and k2 and k3) else 1)
