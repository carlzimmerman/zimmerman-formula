#!/usr/bin/env python3
"""WD1 (FROZEN_CRITERIA.md 0cd6ef1dcb): outside proposal, a merger-decohered condensate supplement with a 1.6 Mpc Thomas-Fermi
core, graded AS WRITTEN under the record's gates. TEST lane, quarantined; adopts nothing (the owner adopts). No dark-matter
particle is adopted: a declared supplementary component is graded exactly as PJ1 and BG1 were. kappa = 1/2 FITTED; not theory
closed. Both footings (canonical a0 9.3603e-11 / alt 1.1312e-10 m/s^2, the record's kappa = 1/2 values as QX5 / GB1 / PJ1
define them) graded separately, never pooled.

    python3 wd1.py ka       -> parts/ka.json          KA1, KA2, KA3 (own quasistatic form and own rebuilt dynamic integrator)
    python3 wd1.py local    -> parts/local.json       G1 (+G1b, G1c), G2, G3 (+shape), G4, G5 (+G5b), G10; as-written, derived bracket,
                                                      the proposal's own nu beside the adopted law; KA4 (f -> 0 replay)
      WD1_MUTATE=M1|M2|M3 python3 wd1.py local -> parts/local_M1.json ...  (M1 R_c0 -> 50 kpc; M2 W_crit -> inf; M3 f -> 0)
    python3 wd1.py bullet   -> parts/bullet.json      G6 (a) asserted centering on the galaxies, (b) gas-traced (DB1 / UX6 child)
    python3 wd1_cmb.py      -> parts/cmb_<footing>.json  G7 (F1A machinery, constant weight), KA5
    python3 wd1_web.py      -> parts/web.json         G8 (growth + PR4 lensing with the 1.6 Mpc halo-core suppression), G9 (forest)
    python3 wd1_grade.py    -> wd1.json / wd1.out, wd1_MUTATE.json / wd1_MUTATE.out

Mechanism in the record's words (FROZEN_CRITERIA.md): a pressureless component of cosmic amount f M_b, f = 4.40, that clusters as
cold dust before first shell-crossing and afterwards sits in a Thomas-Fermi core of radius R_c0 = 1.60 Mpc around every
collisionless baryonic centroid, enclosed mass M(<r) = f M_b r^3 / (r^2 + R_c^2)^(3/2). Mergers lower the core radius through a
decoherence scalar s driven by the tidal tensor's lag: quasistatic W_lag(r) = 16 mu^2 (d^2/(r^2 + d^2))^2, s(r) = gamma N W_lag^2 /
(W_lag + W_crit), R_c(r) = R_c0 e^(-s/2); dynamic form: s integrated along tracers through a two-body inspiral (rebuilt here from
its equations). Satellites keep min[1, (v_esc/sigma_host)^3] of their share. The adopted law runs on the summed Newtonian source.
The enclosed-mass formula is evaluated LITERALLY with R_c(r) at the radius asked (primary, as written); where that makes the
enclosed mass fall outward (negative shell density) the fraction of such shells is reported and a monotone (floored-density)
reading is reported beside it, never graded.

Read-only use of PJ1 (imported as a module for the record's constants, the law, the depth convention and the loaders it carries),
QX8 (SPARC exact-field parts), GB1 / QX5 (battery loaders and gate formulae), UD1 / UD2, S1, X1 / LW1, DB1 / UX6 (Bullet child).
One thread, RSS < 1 GB (the DB1 child's 1.39 GB is the record's machinery and is recorded), SIGTERM checkpoint."""
import os, sys, json, math, io, contextlib, time, signal, resource, csv
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import warnings; warnings.filterwarnings("ignore")
import numpy as np
np.seterr(all="ignore")

T0 = time.time()
CRIT = "0cd6ef1dcb"
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
# PJ1's lane directory (origin/main). WD1_PJ1_DIR points at a read-only copy when the shared checkout is behind origin.
PJ1DIR = os.environ.get("WD1_PJ1_DIR", os.path.join(REPO, "closure_2026_11_08", "PJ1_potential_gated_jeans"))
sys.path.insert(0, PJ1DIR)
_argv = sys.argv; sys.argv = [os.path.join(PJ1DIR, "pj1.py")]
with contextlib.redirect_stdout(io.StringIO()):
    import pj1 as J                     # read-only: constants, law, depth, loaders; nothing of PJ1's is run or written
sys.argv = _argv
CL6, CL7, RB, DATA = J.CL6, J.CL7, J.RB, J.DATA
PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
FOOTS = J.FOOTS; A0H = J.A0H; RF = J.RF; glaw = J.glaw
G_SI, MS, KPC, MPC, CL, PC = J.G_SI, J.MS, J.KPC, J.MPC, J.CL, J.PC
G_KPC = 4.3009172706e-6                  # kpc (km/s)^2 / Msun
KMS_TO_KPC_MYR = 1.022712165e-3
MUTATE = os.environ.get("WD1_MUTATE", "")
WHICH = sys.argv[1] if len(sys.argv) > 1 else ""
SUFFIX = ("_" + MUTATE if MUTATE else "")
NOTE = "kappa = 1/2 FITTED; not theory closed"

# ---------------- declared constants and per-class inputs (the proposal's own; graded as written)
F_COSMIC = 0.0 if MUTATE == "M3" else 4.40
RC0_KPC = 50.0 if MUTATE == "M1" else 1600.0
W_CRIT = float("inf") if MUTATE == "M2" else 0.020
GAMMA = 2.0; MU_DEFAULT = 0.25; LAMBDA_IR = 1.0e-12          # Myr^-2, the integrator's vacuum regulator
CLASS = dict(spiral=(0.0, 0.0), elliptical=(1.0, 35.0), group=(4.0, 400.0), group_code=(4.5, 420.0), cluster=(6.0, 600.0),
             bullet_main=(6.0, 600.0), bullet_sub=(5.0, 500.0))
SIGMA_COMA = 1000.0                                           # km/s, declared
SIGMA_HOST_DSPH = 180.0                                       # km/s, the proposal's own host value for the MW (its Crater II self-test); M31 taken alike, reported only
BRACKET = dict(one_event=True, q=(0.6, 0.4), d_sep0_ell_kpc=40.0, n_steps=600, n_angles=12)   # the derived bracket (frozen)

RES = {}
def P(s=""): print(s, flush=True)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, float) and not math.isfinite(o): return str(o)
    return o
def dump(name, obj): json.dump(clean(obj), open(os.path.join(PARTS, name), "w"), indent=1)
def on_term(sig, frm):
    dump(f"{WHICH}{SUFFIX}_partial.json", RES); P("SIGTERM: partial checkpoint written"); sys.exit(143)
signal.signal(signal.SIGTERM, on_term)
def nu_prop(y):
    """the proposal's own interpolation (reported bracket, never graded): nu(y) = 1/(1 - e^(-sqrt y))."""
    y = np.maximum(np.asarray(y, float), 1e-30); return 1.0 / (1.0 - np.exp(-np.sqrt(y)))
def g_prop(gN, a0): return gN * nu_prop(gN / a0)

# ================================================================== the mechanism, quasistatic form (own implementation)
def w_lag(r_kpc, d_kpc, mu=MU_DEFAULT):
    r = np.asarray(r_kpc, float); return 16.0 * mu * mu * (d_kpc * d_kpc / (r * r + d_kpc * d_kpc)) ** 2
def s_quasi(r_kpc, N, d_kpc, mu=MU_DEFAULT):
    r = np.asarray(r_kpc, float)
    if N <= 0 or d_kpc <= 0 or mu <= 0 or not math.isfinite(W_CRIT): return np.zeros_like(r)
    W = w_lag(r, d_kpc, mu); return GAMMA * N * W * W / (W + W_CRIT)
def rc_of(r_kpc, N, d_kpc, mu=MU_DEFAULT, s=None):
    s = s_quasi(r_kpc, N, d_kpc, mu) if s is None else np.asarray(s, float); return RC0_KPC * np.exp(-0.5 * s)
def shape(r_kpc, Rc_kpc):
    r = np.asarray(r_kpc, float); return r ** 3 / (r * r + np.asarray(Rc_kpc, float) ** 2) ** 1.5
def capture(v_esc, sigma_host):
    if sigma_host <= 0 or v_esc >= sigma_host: return 1.0
    return float(max(0.0, (v_esc / sigma_host) ** 3))
def M_comp(r_kpc, Mb_tot, N=0.0, d_kpc=0.0, cap=1.0, s_of_r=None, mu=MU_DEFAULT):
    """enclosed component mass (same unit as Mb_tot) at r (kpc), literal form: R_c evaluated at the radius asked.
    s_of_r: a callable s(r_kpc) from the dynamic integrator (the derived bracket) replaces the quasistatic s."""
    r = np.asarray(r_kpc, float); s = s_of_r(r) if s_of_r is not None else None
    return F_COSMIC * Mb_tot * cap * shape(r, rc_of(r, N, d_kpc, mu, s))
def M_comp_monotone(r_kpc, Mb_tot, N=0.0, d_kpc=0.0, cap=1.0, s_of_r=None, n=2000):
    """reported reading: the literal profile with its negative-density shells floored (cumulative maximum of the literal M(<r) on a
    fine log grid); identical to the literal form wherever dM/dr >= 0 (every N = 0 system)."""
    r = np.atleast_1d(np.asarray(r_kpc, float)); rg = np.geomspace(1e-3, max(1e4, 2 * r.max()), n)
    Ml = M_comp(rg, Mb_tot, N, d_kpc, cap, s_of_r); Mm = np.maximum.accumulate(Ml)
    neg = float(np.mean(np.diff(Ml) < 0)); return np.interp(r, rg, Mm), neg
def rho_comp(r_kpc, Mb_tot, N=0.0, d_kpc=0.0, cap=1.0):
    """component density (Mb_tot unit per kpc^3) from the literal enclosed mass, centred difference."""
    r = float(r_kpc); h = 1e-3 * r
    return float((M_comp(r + h, Mb_tot, N, d_kpc, cap) - M_comp(r - h, Mb_tot, N, d_kpc, cap)) / (2 * h) / (4 * math.pi * r * r))

# ================================================================== the dynamic form (own rebuild from the equations)
def tidal_tensor(pts, centre, M_msun, a_kpc):
    """E_ij = (d_i d_j - delta_ij lap/3) Phi for a Plummer-softened point mass (kpc, Myr): Phi = -GM/sqrt(r^2 + a^2) gives
    E_ij = -GM (3 x_i x_j - r^2 delta_ij) / (r^2 + a^2)^(5/2)."""
    dx = pts - centre[None, :]; r2 = np.einsum("ij,ij->i", dx, dx); GM = G_KPC * M_msun * KMS_TO_KPC_MYR ** 2
    pref = -GM / (r2 + a_kpc * a_kpc) ** 2.5
    return pref[:, None, None] * (3.0 * dx[:, :, None] * dx[:, None, :] - r2[:, None, None] * np.eye(3)[None, :, :])
def inspiral(t, d0, v_orb, t_decay, m1, m2):
    """two progenitors on a decaying circular orbit about their centre of mass: separation d0 e^(-(t/t_decay)^2 / 2), angular speed
    v_orb / sqrt(d^2 + (0.15 d0)^2) (softened at the end of the inspiral)."""
    d = d0 * math.exp(-0.5 * (t / max(t_decay, 1.0)) ** 2); om = (v_orb / math.sqrt(d * d + (0.15 * d0) ** 2)) * KMS_TO_KPC_MYR
    u = np.array([math.cos(om * t), math.sin(om * t), 0.0]); M = m1 + m2
    return (m2 / M) * d * u, -(m1 / M) * d * u
def rhs(pts, Sig, t, tau, par):
    """Israel-Stewart relaxation of the tracked tidal tensor and the decoherence source:
    tau dSig/dt = E - Sig;  ds/dt = gamma |E| W^2/(W + W_crit),  W = |E - Sig|^2 / (|E|^2 + Lambda_IR)."""
    r1, r2 = inspiral(t, par["d0"], par["v"], par["t_decay"], par["m1"], par["m2"])
    E = tidal_tensor(pts, r1, par["m1"], par["a"]) + tidal_tensor(pts, r2, par["m2"], par["a"]); D = E - Sig
    E2 = np.einsum("ijk,ijk->i", E, E); D2 = np.einsum("ijk,ijk->i", D, D); W = D2 / (E2 + LAMBDA_IR)
    ds = (GAMMA * np.sqrt(E2) * W * W / (W + W_CRIT)) if math.isfinite(W_CRIT) else np.zeros_like(W)
    return D / tau[:, None, None], ds, W
def integrate_merger(radii_kpc, m1, m2, d0, v_orb, t_total, dt, n_angles=12):
    """s(r) after one two-body merger: tracers on rings of radius r (tilted 0.4 rad), RK4 in time; tau_rel = the local dynamical
    time sqrt(r^2 + d0^2)/v_circ(sqrt(r^2 + d0^2)) of the total Newtonian mass; the tracked tensor starts relaxed to the merged
    (centre-of-mass) Plummer field. Returns shell means of s, the peak W per shell and R_c(r)."""
    radii = np.asarray(radii_kpc, float); th = np.linspace(0, 2 * math.pi, n_angles, endpoint=False); c4, s4 = math.cos(0.4), math.sin(0.4)
    pts = np.array([[r * math.cos(t), r * math.sin(t) * c4, r * math.sin(t) * s4] for r in radii for t in th]); idx = np.repeat(np.arange(len(radii)), n_angles)
    rm = np.linalg.norm(pts, axis=1); M = m1 + m2; a = 0.15 * d0
    Rl = np.sqrt(rm * rm + d0 * d0); vc = np.sqrt(G_KPC * M / Rl); tau = (Rl / vc) / KMS_TO_KPC_MYR
    par = dict(d0=d0, v=v_orb, t_decay=0.45 * t_total, m1=m1, m2=m2, a=a)
    Sig = tidal_tensor(pts, np.zeros(3), M, a); s = np.zeros(len(pts)); Wmax = np.zeros(len(pts)); t = 0.0
    for _ in range(int(math.ceil(t_total / dt))):
        k1, l1, W1 = rhs(pts, Sig, t, tau, par); k2, l2, _ = rhs(pts, Sig + 0.5 * dt * k1, t + 0.5 * dt, tau, par)
        k3, l3, _ = rhs(pts, Sig + 0.5 * dt * k2, t + 0.5 * dt, tau, par); k4, l4, _ = rhs(pts, Sig + dt * k3, t + dt, tau, par)
        Sig = Sig + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4); s = s + dt / 6 * (l1 + 2 * l2 + 2 * l3 + l4); Wmax = np.maximum(Wmax, W1); t += dt
    s_sh = np.array([s[idx == i].mean() for i in range(len(radii))]); W_sh = np.array([Wmax[idx == i].mean() for i in range(len(radii))])
    return dict(r=radii, s=s_sh, W_peak=W_sh, Rc=RC0_KPC * np.exp(-0.5 * s_sh))
BR_RADII = np.geomspace(3.0, 6000.0, 28)
_BRC = {}
def bracket_s(Mb_tot_msun, d0_kpc, a0, tag=None):
    """the derived bracket: ONE merger event, progenitors 3:2 of the system's baryons, d_sep0 given (R500 for groups and clusters,
    40 kpc for ellipticals), orbital speed = the adopted law's circular speed on the baryons at d_sep0, duration one orbit, 600 steps.
    Returns s(r_kpc) (interpolated in log r, held constant beyond the tracer rings) and the run's table."""
    key = (round(float(Mb_tot_msun), 3), round(float(d0_kpc), 3), a0)
    if key in _BRC: return _BRC[key]
    q1, q2 = BRACKET["q"]; d0 = float(d0_kpc); gN = G_SI * Mb_tot_msun * MS / (d0 * KPC) ** 2; v = math.sqrt(glaw(gN, a0) * d0 * KPC) / 1e3
    t_tot = 2 * math.pi * d0 / v / KMS_TO_KPC_MYR; dt = t_tot / BRACKET["n_steps"]
    out = integrate_merger(BR_RADII, q1 * Mb_tot_msun, q2 * Mb_tot_msun, d0, v, t_tot, dt, BRACKET["n_angles"])
    lr, ls = np.log(out["r"]), out["s"]
    s_of_r = lambda r: np.interp(np.log(np.asarray(r, float)), lr, ls)
    tab = dict(Mb_tot=Mb_tot_msun, d_sep0_kpc=d0, v_orb_kms=v, t_total_Myr=t_tot, dt_Myr=dt, r_kpc=out["r"].tolist(), s=out["s"].tolist(), Rc_kpc=out["Rc"].tolist(), W_peak=out["W_peak"].tolist())
    _BRC[key] = (s_of_r, tab); return _BRC[key]

# ================================================================== known answers KA1-KA3
def run_ka():
    ka = {}
    # KA1: r 500 kpc, M_b 1.2e11, N 0 -> component 0.117 M_b; the proposal's nu gives +0.025 dex; the adopted law's shift reported
    r, Mb = 500.0, 1.2e11; mc = float(M_comp(r, Mb, 0.0, 0.0)); frac = mc / Mb
    gN = G_SI * Mb * MS / (r * KPC) ** 2; gT = gN * (1 + frac)
    for f in FOOTS:
        a0 = A0H[f]; sh_nu = math.log10(g_prop(gT, a0) / g_prop(gN, a0)); sh_law = math.log10(glaw(gT, a0) / glaw(gN, a0))
        ka[f"KA1_{f}"] = dict(r_kpc=r, Mb=Mb, comp_over_Mb=frac, Rc_kpc=float(rc_of(r, 0, 0)), shift_dex_proposal_nu=sh_nu, shift_dex_adopted_law=sh_law,
                              pass_=bool(abs(frac - 0.117) <= 0.002 and abs(sh_nu - 0.025) <= 0.003))
    sh12 = math.log10(g_prop(gT, 1.2e-10) / g_prop(gN, 1.2e-10))
    ka["KA1_at_proposal_a0_1p2e-10"] = dict(comp_over_Mb=frac, shift_dex_proposal_nu=sh12, pass_=bool(abs(frac - 0.117) <= 0.002 and abs(sh12 - 0.025) <= 0.003))
    # KA2: group proxy r 200 kpc, M_b 1.5e12, N 4.5, d 420: R_c <= 150 kpc, component/M_b >= 3.0 (the proposal prints ~3.8)
    N, d = CLASS["group_code"]; rc2 = float(rc_of(200.0, N, d)); fr2 = float(M_comp(200.0, 1.5e12, N, d)) / 1.5e12
    ka["KA2_group_proxy"] = dict(r_kpc=200.0, Mb=1.5e12, N=N, d_kpc=d, s=float(s_quasi(200.0, N, d)), Rc_kpc=rc2, comp_over_Mb=fr2, pass_=bool(rc2 <= 150.0 and fr2 >= 3.0))
    # KA3: the rebuilt integrator: Case A (6e10 + 6e10, d 40, v 220, 1200 Myr, dt 2): s(300) in [0.005, 0.02]; Case B (1.2e13 + 8e12, d 450, v 650, 2500 Myr, dt 4): s(200) in [4.5, 6.5]
    radii = np.array([50.0, 100.0, 200.0, 300.0, 500.0, 1000.0])
    A = integrate_merger(radii, 6e10, 6e10, 40.0, 220.0, 1200.0, 2.0); B = integrate_merger(radii, 1.2e13, 8e12, 450.0, 650.0, 2500.0, 4.0)
    sA = float(A["s"][3]); sB = float(B["s"][2])
    ka["KA3_dynamic_integrator"] = dict(caseA=dict(r=radii.tolist(), s=A["s"].tolist(), Rc_kpc=A["Rc"].tolist(), W_peak=A["W_peak"].tolist(), s_300=sA, band=[0.005, 0.02], ok=bool(0.005 <= sA <= 0.02)),
                                        caseB=dict(r=radii.tolist(), s=B["s"].tolist(), Rc_kpc=B["Rc"].tolist(), W_peak=B["W_peak"].tolist(), s_200=sB, band=[4.5, 6.5], ok=bool(4.5 <= sB <= 6.5)))
    ka["KA3_dynamic_integrator"]["pass_"] = bool(ka["KA3_dynamic_integrator"]["caseA"]["ok"] and ka["KA3_dynamic_integrator"]["caseB"]["ok"])
    ka["KA3_dynamic_integrator"]["mismatch"] = None if ka["KA3_dynamic_integrator"]["pass_"] else f"case A s(300) {sA:.4f} vs [0.005, 0.02]; case B s(200) {sB:.3f} vs [4.5, 6.5]: the quasistatic form is graded alone"
    # the tidal tensor against a finite-difference Hessian of the Plummer potential (own check of the rebuild)
    rng = np.random.default_rng(3); pts = rng.normal(size=(5, 3)) * 100.0; M_, a_ = 1e12, 30.0; GM = G_KPC * M_ * KMS_TO_KPC_MYR ** 2
    phi = lambda x: -GM / math.sqrt(float(np.dot(x, x)) + a_ * a_); h = 1e-2; worst = 0.0
    for x in pts:
        H = np.zeros((3, 3))
        for i in range(3):
            for j in range(3):
                e_i = np.eye(3)[i] * h; e_j = np.eye(3)[j] * h; H[i, j] = (phi(x + e_i + e_j) - phi(x + e_i - e_j) - phi(x - e_i + e_j) + phi(x - e_i - e_j)) / (4 * h * h)
        Efd = H - np.eye(3) * np.trace(H) / 3; Ean = tidal_tensor(x[None, :], np.zeros(3), M_, a_)[0]; worst = max(worst, float(np.max(np.abs(Efd - Ean)) / np.max(np.abs(Ean))))
    ka["KA3_tensor_finite_difference_check"] = dict(max_rel_dev=worst, pass_=bool(worst <= 1e-4))
    # a light check of the bracket construction on the KA3 masses (reported): one event, 3:2, d_sep0 450 kpc, law speed, one orbit
    s_of_r, tab = bracket_s(2.0e13, 450.0, A0H["canonical"]); ka["bracket_example_2e13_450kpc"] = dict(tab, s_200=float(s_of_r(200.0)), Rc_200=float(RC0_KPC * math.exp(-0.5 * s_of_r(200.0))))
    for k, v in ka.items(): P(f"{k}: {'PASS' if v.get('pass_', True) else 'FAIL'}  " + json.dumps(clean({a: b for a, b in v.items() if a not in ('pass_',)}))[:420])
    ka["all_pass"] = bool(all(v.get("pass_", True) for v in ka.values())); ka["criteria"] = CRIT; ka["note"] = NOTE; ka["mutate"] = MUTATE
    dump(f"ka{SUFFIX}.json", ka); return ka

# ================================================================== local gates
def run_local():
    from astropy.io import fits
    sys.path.insert(0, os.path.join(CL6, "QX8_sparc_exact_field")); a_ = sys.argv; sys.argv = [a_[0]]
    with contextlib.redirect_stdout(io.StringIO()):
        import qx8 as Q8
    sys.argv = a_
    GALS = Q8.load_sparc(); Q8J = json.load(open(os.path.join(CL6, "QX8_sparc_exact_field", "qx8.json")))
    GB = J.load_prefix(os.path.join(CL6, "GB1_all_gates_battery", "gb1.py"), "# ------------------------------------------------------------------ main", "gb1_lib")
    GBJ = json.load(open(os.path.join(CL6, "GB1_all_gates_battery", "gb1.json")))
    XC, GR = GB["XC"], GB["GR"]; LE = GB["NS"]["lensing"]()
    R500 = {}; XPROF = {}
    for name in sorted({z["name"] for z in XC}):
        p_ = os.path.join(GB["DATA"], "xcop", name)
        with fits.open(os.path.join(p_, f"{name}_fgas_profile.fits")) as h:
            R500[name] = float(h[1].header["R500"]); gas = h[1].data.copy(); gr = np.array(gas["RADIUS"], float) * R500[name]; gM = np.array(gas["MGAS"], float)
        with fits.open(os.path.join(p_, f"{name}_mstar.fits")) as h:
            st = h[2].data.copy(); sr = np.array(st["RADIUS"], float); sM = np.array(st["MSTAR"], float)
        Mbl = [z for z in XC if z["name"] == name][0]["Mb_last"]
        rr = np.geomspace(max(gr[gr > 0][0], sr[sr > 0][0], 1.0), Mbl[1], 60)
        li = lambda r, m, t: 10 ** np.interp(np.log10(t), np.log10(r[m > 0]), np.log10(m[m > 0]))
        XPROF[name] = dict(r=rr, Mb=li(gr, gM, rr) + li(sr, sM, rr), Mgas=li(gr, gM, rr), Mb_last=Mbl, Mof=J.loglog_M(rr, li(gr, gM, rr) + li(sr, sM, rr)), Mgof=J.loglog_M(rr, li(gr, gM, rr)))
    lU, lN = np.log(Q8.UPS), np.log(Q8.NODES)
    PRE = {f: [np.array([np.interp(lU, lN, T[:, j]) for j in range(T.shape[1])]) for T in
               (np.load(os.path.join(Q8.PARTS, f, f"{i:03d}.npz"), allow_pickle=False)["T"] for i in range(len(GALS)))] for f in FOOTS}
    def fit_stats(q, lgp):
        OK, W = q["OK"], q["W"]; r = np.where(OK, np.log10(q["GO"])[:, None] - lgp, 0.0); Wm = np.where(OK, W[:, None], 0.0)
        wr2 = (Wm * r * r).sum(0); wr = (Wm * r).sum(0); ws = Wm.sum(0); i = int(np.argmin(wr2 / np.maximum(ws, 1e-300)))
        return wr2[i], wr[i], ws[i], i
    def pooled(rows, sel=None):
        idx = list(range(len(rows))) if sel is None else list(sel)
        wr2 = sum(rows[i][0] for i in idx); wr = sum(rows[i][1] for i in idx); ws = sum(rows[i][2] for i in idx)
        return dict(rms=float(math.sqrt(wr2 / ws)), mean=float(wr / ws), U_median=float(np.median([Q8.UPS[rows[i][3]] for i in idx])), n=len(idx))
    def sparc_eval(f, bf_list, law="adopted"):
        a0 = A0H[f]; rows = []
        for i, (q, Tf) in enumerate(zip(GALS, PRE[f])):
            g = q["GB"] * bf_list[i][:, None]; gl = glaw(g, a0) if law == "adopted" else g_prop(g, a0)
            rows.append(fit_stats(q, np.log10(np.maximum(gl, 1e-300)) + Tf))
        return rows
    SPROF = []
    for q in GALS:
        R = q["R"]; VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2
        Mb = np.maximum.accumulate(np.clip(VB2 * R / G_KPC, 0, None)); Mb = np.maximum(Mb, 1e3)
        SPROF.append(dict(R=R, Mb=Mb, Mtot=float(Mb[-1]), Vflat=q["meta"]["Vflat"]))
    massive = [i for i, s in enumerate(SPROF) if s["Vflat"] >= 250.0]
    UD1 = json.load(open(os.path.join(RB, "UD1_agc114905_udg_rotation", "ud1.json"))); UD2 = json.load(open(os.path.join(RB, "UD2_malin1_giant_lsb", "ud2.json")))
    CONV = 1e6 / 3.0857e19
    agc = dict(R=np.array(UD1["data2024"]["R"]), V=np.array(UD1["data2024"]["V"]), E=np.array(UD1["data2024"]["E"]), vb2=np.array(UD1["baryons"]["Vgas"]) ** 2 + np.array(UD1["baryons"]["Vstar"]) ** 2)
    mal = dict(R=np.array([12.5, 37.5, 62.5, 87.5]), V=np.array([236.9, 216.2, 197.4, 214.1]), E=np.array([9.4, 2.6, 4.7, 11.8]),
               vb2=np.array(UD2["decoHL"]["gas"]) ** 2 + np.array(UD2["decoHL"]["lsb"]) ** 2 + np.array(UD2["decoHL"]["hsb"]) ** 2)
    for d in (agc, mal): d["Mb"] = np.maximum.accumulate(d["vb2"] * d["R"] / G_KPC)
    def rc_chi2(d, a0, fK=None, law="adopted"):
        gN = d["vb2"] / d["R"] * CONV * (1.0 if fK is None else 1 + fK); g = glaw(gN, a0) if law == "adopted" else g_prop(gN, a0)
        V = np.sqrt(np.maximum(g / CONV * d["R"], 0.0)); return float(np.sum(((d["V"] - V) / d["E"]) ** 2))
    S1D = os.path.join(RB, "S1_v3_hosted_small"); UROWS = list(csv.DictReader(open(os.path.join(S1D, "s1_coma_per_galaxy.csv"))))
    UD = {f: [r for r in UROWS if r["footing"] == f] for f in FOOTS}
    # Coma's host field as the record carries it (S1): the hydrostatic field of the L23 beta model, g_beta(d) = CB d/(d^2 + rc^2)
    KEV, MP = 1.602176634e-16, 1.67262e-27; BETA = dict(kT=8.6, rc=276.0, beta=0.71, mu=0.6); CB = 3 * BETA["beta"] * BETA["kT"] * KEV / (BETA["mu"] * MP); KPC_C = 3.0857e19
    def g_beta(d_kpc): r = d_kpc * KPC_C; rc = BETA["rc"] * KPC_C; return CB * r / (r * r + rc * rc)
    def law_inverse(g, a0): return g * g / (g + a0)                      # the law's Newtonian source for a given field
    def coma_host(f):
        """Coma's baryons as the law implies them from the record's hydrostatic field (framework-native), R500 from that field."""
        a0 = A0H[f]; h = float(json.load(open(os.path.join(CL7, "F1A_primary_cmb_audit", "parts", f"fit_B2_{f}_cold.json")))["pars"]["h"])
        rho_c = 3 * (h * 1e5 / MPC) ** 2 / (8 * math.pi * G_SI)
        Mb_of = lambda d: law_inverse(g_beta(d), a0) * (d * KPC_C) ** 2 / G_SI / MS          # Msun inside d (kpc)
        r5 = 300.0
        for _ in range(200): r5 = (3 * Mb_of(r5) * MS / (4 * math.pi * 500 * rho_c)) ** (1 / 3) / KPC * 0.5 + 0.5 * r5   # fixed point on the law-implied total (HSE) mass
        Mtot5 = law_inverse(g_beta(r5), a0) * (r5 * KPC_C) ** 2 / G_SI / MS
        return dict(R500_kpc=r5, Mb_tot=Mtot5, Mb_of=Mb_of, h=h)
    X1R = {(r["footing"], r["name"]): r for r in csv.DictReader(open(os.path.join(RB, "X1_hosted_recount", "x1_per_system.csv")))}
    LW = json.load(open(os.path.join(RB, "LW1_law_scorecard", "lw1_dwarfs.json")))
    def delta_b(b, ft, a0, law="adopted"):
        gN = GB["need"](ft, "x") * a0; gf = glaw if law == "adopted" else (lambda g, a: g_prop(g, a)); return math.log10(gf(b * gN, a0) / gf(gN, a0))

    def eval_set(f, variant, B, base, verbose=False):
        """variant: dict(mode='as_written'|'bracket'|'monotone', law='adopted'|'proposal', group=(N,d)). Returns the gate dicts."""
        a0 = A0H[f]; law = variant.get("law", "adopted"); mode = variant.get("mode", "as_written"); out = dict(variant=variant); gf = glaw if law == "adopted" else g_prop
        def Mc(r_kpc, Mb_tot, cls, d0_bracket=None, cap=1.0):
            N, d = CLASS[cls] if isinstance(cls, str) else cls
            if mode == "bracket" and N > 0:
                s_of_r, _ = bracket_s(Mb_tot, d0_bracket, a0); return M_comp(r_kpc, Mb_tot, N, d, cap, s_of_r), 0.0
            if mode == "monotone" and N > 0: return M_comp_monotone(r_kpc, Mb_tot, N, d, cap)
            return M_comp(r_kpc, Mb_tot, N, d, cap), 0.0
        # ---- G1 SPARC (N 0, component inside each galaxy's last measured radius), G1b massive tail, G1c
        FK = [np.asarray(Mc(s["R"], s["Mtot"], "spiral")[0]) / s["Mb"] for s in SPROF]
        rows = sparc_eval(f, [1 + fk for fk in FK], law); pa = pooled(rows); pb = pooled(rows, massive)
        out["G1"] = dict(status="PASS" if (pa["rms"] <= base["rms"] + 0.010 and abs(pa["mean"]) <= 0.05) else "FAIL", **pa, rms_line=base["rms"] + 0.010, fK_median_last=float(np.median([fk[-1] for fk in FK])), fK_max_last=float(np.max([fk[-1] for fk in FK])))
        out["G1b"] = dict(status="PASS" if (pb["rms"] <= base["rms_massive"] + 0.010 and abs(pb["mean"]) <= 0.05) else "FAIL", **pb, rms_line=base["rms_massive"] + 0.010)
        g1c = {}
        for nm, d in (("AGC114905", agc), ("Malin1", mal)):
            fk = np.asarray(Mc(d["R"], float(d["Mb"][-1]), "spiral")[0]) / d["Mb"]
            g1c[nm] = dict(law_only=rc_chi2(d, a0, None, law), with_component=rc_chi2(d, a0, fk, law), fK_last=float(fk[-1]))
        out["G1c"] = g1c
        # ---- G2 KiDS: 59 points, each lens bin's stellar mass as the record carries it (QX5 lensing loader), r = sqrt(G M_b / g_bar)
        def kids(cls, d0b=None):
            per = []
            for p in LE:
                Mb = p["Mb"] / MS; r = math.sqrt(G_SI * p["Mb"] / p["gbar"]); mk, neg = Mc(r / KPC, Mb, cls, d0b)
                sh = math.log10(gf(p["gbar"] + G_SI * float(mk) * MS / r ** 2, a0) / gf(p["gbar"], a0))
                per.append(dict(lm=round(math.log10(Mb), 3), r_Mpc=r / MPC, gbar=p["gbar"], shift=sh, comp_over_Mb=float(mk) / Mb, Rc_kpc=float(rc_of(r / KPC, *(CLASS[cls] if isinstance(cls, str) else cls))) if mode != "bracket" else None))
            sh = np.array([x["shift"] for x in per]); outer = np.array([x["r_Mpc"] >= 0.3 for x in per])
            return dict(status="PASS" if np.all(np.abs(sh) <= 0.05) else "FAIL", max_abs_shift=float(np.max(np.abs(sh))), mean_shift=float(sh.mean()), outer_max_abs_shift=float(np.max(np.abs(sh[outer]))), outer_mean_shift=float(sh[outer].mean()),
                        n_points=len(per), n_fail=int(np.sum(np.abs(sh) > 0.05)), n_outer=int(outer.sum()), points=per if verbose else None,
                        shift_by_r={"0.0-0.1": float(np.mean(sh[np.array([x["r_Mpc"] < 0.1 for x in per])])), "0.1-0.3": float(np.mean(sh[np.array([0.1 <= x["r_Mpc"] < 0.3 for x in per])])),
                                    "0.3-1.0": float(np.mean(sh[np.array([0.3 <= x["r_Mpc"] < 1.0 for x in per])])), ">=1.0": float(np.mean(sh[np.array([x["r_Mpc"] >= 1.0 for x in per])])) if any(x["r_Mpc"] >= 1.0 for x in per) else None})
        out["G2"] = kids("spiral")                                                                   # primary: the isolated selection, N 0
        out["G2_ETG_bracket"] = kids("elliptical", BRACKET["d_sep0_ell_kpc"])                       # bracket: the proposal's ETG inputs (N 1, d 35; dynamic: 40 kpc, 3:2)
        # ---- G3 X-COP: the amount as given (f x the cluster's baryons inside the outermost measured radius), declared cluster inputs, no fitted amplitude; NA2 per-bin shape
        d = []; xr = []; conc = []; negs = []
        for name, pr in XPROF.items():
            Mbt = pr["Mb_last"][0]
            for z in XC:
                if z["name"] != name: continue
                mk, neg = Mc(z["r_kpc"], Mbt, "cluster", R500[name]); mk = float(mk); rm = z["r_kpc"] * KPC
                Mp = gf(G_SI * (z["M_b"] + mk) * MS / rm ** 2, a0) * rm ** 2 / G_SI / MS; d.append(math.log10(z["M_obs"] / Mp)); xr.append(z["r_kpc"] / R500[name]); negs.append(neg)
            r25, r70 = 0.25 * R500[name], 0.7 * R500[name]; m25 = float(Mc(r25, Mbt, "cluster", R500[name])[0]); m70 = float(Mc(r70, Mbt, "cluster", R500[name])[0])
            zz = [z for z in XC if z["name"] == name][0]; hM = lambda rk: 10 ** np.interp(math.log10(rk), np.log10(zz["hr"]), np.log10(np.maximum(zz["hM"], 1.0)))
            conc.append(dict(name=name, R500=R500[name], Mb_last=Mbt, c_comp=m25 / max(m70, 1e-30), c_gas=float(pr["Mgof"](r25 * KPC) / pr["Mgof"](r70 * KPC)), c_b=float(pr["Mof"](r25 * KPC) / pr["Mof"](r70 * KPC)), c_need_hse=float(hM(r25) / hM(r70)),
                             comp_over_Mb_at_100kpc=float(Mc(100.0, Mbt, "cluster", R500[name])[0]) / Mbt, comp_over_Mb_at_500kpc=float(Mc(500.0, Mbt, "cluster", R500[name])[0]) / Mbt, comp_over_Mb_at_R500=float(Mc(R500[name], Mbt, "cluster", R500[name])[0]) / Mbt,
                             Rc_kpc_at_0p1_0p5_R500=[float(rc_of(0.1 * R500[name], *CLASS["cluster"])), float(rc_of(0.5 * R500[name], *CLASS["cluster"]))] if mode != "bracket" else None))
        d = np.array(d); xr = np.array(xr); EDG = [0.0, 0.25, 0.5, 0.75, 1.0, 2.0]; bins = []
        for lo, hi in zip(EDG[:-1], EDG[1:]):
            m = (xr >= lo) & (xr < hi); bins.append(dict(lo=lo, hi=hi, n=int(m.sum()), mean=float(d[m].mean()) if m.sum() else None, graded=bool(m.sum() >= 3), within=bool(abs(d[m].mean()) <= 0.10) if m.sum() >= 3 else None))
        amp_ok = abs(d.mean()) <= 0.05 and math.sqrt((d ** 2).mean()) <= 0.10; shape_ok = all(b["within"] for b in bins if b["graded"])
        out["G3"] = dict(status="PASS" if (amp_ok and shape_ok) else "FAIL", amount_status="PASS" if amp_ok else "FAIL", shape_status="PASS" if shape_ok else "FAIL", mean=float(d.mean()), rms=float(math.sqrt((d ** 2).mean())), n=len(d),
                         bins=bins, shape=conc, c_comp_median=float(np.median([c["c_comp"] for c in conc])), c_gas_median=float(np.median([c["c_gas"] for c in conc])), c_b_median=float(np.median([c["c_b"] for c in conc])), c_need_median=float(np.median([c["c_need_hse"] for c in conc])),
                         negative_shell_fraction_literal=float(np.mean(negs)) if mode == "monotone" else None)
        # ---- G4 groups (Lovisari 20): declared group inputs (one N, one d); M_b,tot = gas inside R500 x (1 + f*)
        def groups(cls):
            o = {}
            for fst in (0, 1):
                npass = 0; med = []; per = []
                for gp in GR:
                    Mbt = gp["g5"] * (1 + fst); ok = True
                    for p in gp["pts"]:
                        rm = p["r_kpc"] * KPC; Mb = p["M_gas"] * (1 + fst); mk = float(Mc(p["r_kpc"], Mbt, cls, gp["R5"])[0])
                        Mp = gf(G_SI * (Mb + mk) * MS / rm ** 2, a0) * rm ** 2 / G_SI / MS; dl = math.log10(p["M_obs"] / Mp); med.append(dl)
                        ok &= abs(dl) <= 2 * p["eM"] / (p["M_obs"] * math.log(10)); per.append(dict(name=gp["name"], r_kpc=p["r_kpc"], comp_over_Mb=mk / Mb, dlog=dl))
                    npass += ok
                o[f"fst{fst}"] = dict(n_pass=int(npass), median_res=float(np.median(med)), per=per if verbose else None)
            return dict(status="PASS" if all(v["n_pass"] >= 16 for v in o.values()) else "FAIL", **o)
        out["G4"] = groups("group"); out["G4_code_inputs_reported"] = groups("group_code")
        # ---- G5 Coma UDGs: each UDG's component at the satellite capture factor, Coma's own component in the external field (1D EFE map, declared)
        CH = coma_host(f); res = []; res_nohost = []; bs = []; caps = []; xe_ratio = []
        for p, row in zip(B["U"], UD[f]):
            Ms = float(row["Mstar"]); Re = float(row["Re_kpc"]); dk = float(row["d_mean_kpc"]); a_pl = Re * KPC
            v_esc = math.sqrt(2 * G_SI * Ms * MS / a_pl) / 1e3; cap = capture(v_esc, SIGMA_COMA); caps.append(cap)
            rh = 4 / 3 * Re; mk = float(Mc(rh, Ms, "spiral", None, cap)[0]); b = 1.0 + mk / (0.5 * Ms); bs.append(b)
            gNi = GB["need"](p["feat"], "x") * a0
            gext_rec = g_beta(dk); gN_ext_rec = law_inverse(gext_rec, a0)                                  # the record's host field and its law-implied Newtonian source
            mcoma = float(Mc(dk, CH["Mb_tot"], "cluster", CH["R500_kpc"])[0]); gN_ext_new = gN_ext_rec + G_SI * mcoma * MS / (dk * KPC_C) ** 2
            nu = lambda gN_tot: gf(gN_tot, a0) / gN_tot
            d_efe = math.log10(nu(math.hypot(gNi, gN_ext_new)) / nu(math.hypot(gNi, gN_ext_rec)))        # 1D external-field map on the law's nu (declared approximation)
            xe_ratio.append(gf(gN_ext_new, a0) / gext_rec)
            res.append(p["D"] - delta_b(b, p["feat"], a0, law) - d_efe); res_nohost.append(p["D"] - delta_b(b, p["feat"], a0, law))
        mu_ = float(np.mean(res)); mu0 = float(np.mean(res_nohost))
        out["G5"] = dict(status="PASS" if abs(mu_) <= 2 * B["sigU"] else "FAIL", mean=mu_, sigma_U=B["sigU"], z=mu_ / B["sigU"], b_median=float(np.median(bs)), capture_median=float(np.median(caps)), capture_max=float(np.max(caps)),
                         mean_without_host_component=mu0, z_without_host_component=mu0 / B["sigU"], host_field_ratio_median=float(np.median(xe_ratio)),
                         coma_host=dict(R500_kpc=CH["R500_kpc"], Mb_tot_law_implied=CH["Mb_tot"], comp_over_Mb_at_1Mpc=float(Mc(1000.0, CH["Mb_tot"], "cluster", CH["R500_kpc"])[0]) / CH["Mb_tot"]), law_only_mean=float(np.mean([p["D"] for p in B["U"]])))
        # G5b: MW classical and bright M31 dSphs (X1 rows; LW1's law-only residual), reported the same way (sigma_host 180 km/s for both hosts, the proposal's own MW value)
        g5b = {}
        for cls in ("MW classical", "bright M31"):
            rows = []
            for n_, s in LW["footings"][f]["per_system"].items():
                if s["cls"] != cls: continue
                xr_ = X1R.get((f, n_))
                if xr_ is None: continue
                Ms = 10 ** float(xr_["logMstar"]); rh = float(xr_["rh_pc"]) / 1e3; v_esc = math.sqrt(2 * G_SI * Ms * MS / (rh * KPC)) / 1e3; cap = capture(v_esc, SIGMA_HOST_DSPH)
                mk = float(Mc(rh, Ms, "spiral", None, cap)[0]); b = 1 + mk / (0.5 * Ms); x = GB["x_from_nu"](10 ** (float(xr_["Delta[Newton]"]) - s["plain"]))
                dlt = math.log10(gf(b * x * a0, a0) / gf(x * a0, a0)) if (np.isfinite(x) and x > 0) else 0.0
                rows.append(dict(name=n_, D_law=s["plain"], capture=cap, comp_over_Mb=mk / Ms, shift=dlt))
            g5b[cls] = dict(n=len(rows), median_D_law=float(np.median([r["D_law"] for r in rows])), median_shift=float(np.median([r["shift"] for r in rows])), max_shift=float(np.max([r["shift"] for r in rows])), capture_max=float(np.max([r["capture"] for r in rows])))
        out["G5b_dsph_reported"] = g5b
        # ---- G10 Cassini (KT16 gate) with the MW's component (N 0 primary; N 1 d 35 bracket) at the Sun's radius, c_T = 1 stated
        g10 = {}
        for tag, cls in (("MW_N0", "spiral"), ("MW_N1_d35_bracket", "elliptical")):
            Mb_mw = 6e10; m82 = float(Mc(8.2, Mb_mw, cls, 40.0)[0]); rhoK = rho_comp(8.2, Mb_mw, *(CLASS[cls])) * MS / KPC ** 3 if mode != "bracket" else (lambda h: (float(Mc(8.2 + h, Mb_mw, cls, 40.0)[0]) - float(Mc(8.2 - h, Mb_mw, cls, 40.0)[0])) / (2 * h) / (4 * math.pi * 8.2 ** 2))(1e-3) * MS / KPC ** 3
            def cand(ft, rhoK=rhoK):
                gN = ft["x"] * a0; gK = 4 * math.pi / 3 * G_SI * rhoK * ft["r"]; return dict(delta=math.log10(gf(gN + gK, a0) / gf(gN, a0)))
            ok, num = GB["g_ss"](cand, B, a0)
            g10[tag] = dict(status="PASS" if ok else "FAIL", M_comp_inside_8p2kpc_Msun=m82, formula_check_4p4Mb_r3=4.4 * Mb_mw * (8.2 / 1600.0) ** 3, rhoK_Msun_pc3=rhoK / MS * PC ** 3, cassini_use=num["cassini_use"], worst_planet_use=num["worst_planet_use"])
        out["G10"] = dict(g10["MW_N0"], bracket_N1_d35=g10["MW_N1_d35_bracket"], cT="1 (a dust component; the action's kinetic structure is unchanged)")
        return out
    def summary(o):
        return (f"G1 {o['G1']['status'][0]} rms {o['G1']['rms']:.4f}/{o['G1']['rms_line']:.4f} mean {o['G1']['mean']:+.4f} fK {o['G1']['fK_median_last']:.1e} | G1b {o['G1b']['status'][0]} {o['G1b']['rms']:.4f}/{o['G1b']['rms_line']:.4f} "
                f"| G2 {o['G2']['status'][0]} max {o['G2']['max_abs_shift']:.3f} outer {o['G2']['outer_max_abs_shift']:.3f} ({o['G2']['n_fail']} over) ETG-br {o['G2_ETG_bracket']['max_abs_shift']:.3f} | G3 {o['G3']['status'][0]} {o['G3']['mean']:+.3f}/{o['G3']['rms']:.3f} bins "
                + " ".join(f"{b['mean']:+.2f}" for b in o['G3']['bins'] if b['graded']) + f" cK {o['G3']['c_comp_median']:.2f} | G4 {o['G4']['status'][0]} {o['G4']['fst0']['n_pass']}/{o['G4']['fst1']['n_pass']} | G5 {o['G5']['status'][0]} {o['G5']['mean']:+.3f} ({o['G5']['z']:+.2f}) cap {o['G5']['capture_median']:.1e} | G10 {o['G10']['status'][0]}")
    for f in FOOTS:
        a0 = A0H[f]; R_ = {}; RES[f] = R_
        S, E_, X = GB["build"](f, a0); U = GB["udgs"](f, a0)
        st = GB["R1"][f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / math.log(10)
        B = dict(f=f, S=S, E=E_, X=X, U=U, sigU=sigU)
        # law-only baselines (the record's own numbers) and KA4 (f -> 0 replay)
        rows0 = sparc_eval(f, [np.ones(len(q["R"])) for q in GALS]); p0 = pooled(rows0); pm0 = pooled(rows0, massive)
        rx = Q8J["footings"][f].get("exact", Q8J["footings"][f].get("st_ex", {})); L0 = GBJ["cands"]["L0"][f]
        d0 = np.array([math.log10(z["M_obs"] / (glaw(G_SI * z["M_b"] * MS / (z["r_kpc"] * KPC) ** 2, a0) * (z["r_kpc"] * KPC) ** 2 / G_SI / MS)) for z in XC])
        u0 = float(np.mean([p["D"] for p in U]))
        base = dict(rms=p0["rms"], mean=p0["mean"], rms_massive=pm0["rms"], n_massive=len(massive))
        R_["baselines"] = dict(sparc=base, sparc_qx8=dict(rms=rx["rms"], U=rx["U_median"]), xcop_law_only=dict(mean=float(d0.mean()), rms=float(math.sqrt((d0 ** 2).mean()))), gb1_L0_xcop=[L0["G2 X-COP"]["num"]["mean"], L0["G2 X-COP"]["num"]["rms"]],
                               groups_gb1_L0=[L0["G3 groups"]["num"]["fst0"]["n_pass"], L0["G3 groups"]["num"]["fst1"]["n_pass"]], udg_law_only=u0, gb1_L0_udg=L0["G5 Coma UDGs"]["num"]["mean"], sigma_U=sigU)
        ka4 = {}
        if MUTATE in ("", "M3"):
            saved = globals()["F_COSMIC"]; globals()["F_COSMIC"] = 0.0
            z = eval_set(f, dict(mode="as_written", law="adopted"), B, base)
            globals()["F_COSMIC"] = saved
            ka4 = dict(G1_rms=z["G1"]["rms"], qx8_rms=rx["rms"], G1_ok=bool(abs(z["G1"]["rms"] - rx["rms"]) <= 1e-6 and abs(z["G1"]["U_median"] - rx["U_median"]) <= 1e-6),
                       G2_max_shift=z["G2"]["max_abs_shift"], G2_ok=bool(z["G2"]["max_abs_shift"] <= 1e-6),
                       G3=[z["G3"]["mean"], z["G3"]["rms"]], gb1=[L0["G2 X-COP"]["num"]["mean"], L0["G2 X-COP"]["num"]["rms"]], G3_ok=bool(abs(z["G3"]["mean"] - L0["G2 X-COP"]["num"]["mean"]) <= 1e-6 and abs(z["G3"]["rms"] - L0["G2 X-COP"]["num"]["rms"]) <= 1e-6),
                       G4=[z["G4"]["fst0"]["n_pass"], z["G4"]["fst1"]["n_pass"]], G4_med=[z["G4"]["fst0"]["median_res"], z["G4"]["fst1"]["median_res"]], gb1_G4=[L0["G3 groups"]["num"]["fst0"]["n_pass"], L0["G3 groups"]["num"]["fst1"]["n_pass"]], gb1_G4_med=[L0["G3 groups"]["num"]["fst0"]["median_res"], L0["G3 groups"]["num"]["fst1"]["median_res"]],
                       G4_ok=bool(z["G4"]["fst0"]["n_pass"] == L0["G3 groups"]["num"]["fst0"]["n_pass"] and z["G4"]["fst1"]["n_pass"] == L0["G3 groups"]["num"]["fst1"]["n_pass"] and abs(z["G4"]["fst0"]["median_res"] - L0["G3 groups"]["num"]["fst0"]["median_res"]) <= 1e-6),
                       G5_mean=z["G5"]["mean_without_host_component"], gb1_G5=L0["G5 Coma UDGs"]["num"]["mean"], G5_ok=bool(abs(z["G5"]["mean_without_host_component"] - L0["G5 Coma UDGs"]["num"]["mean"]) <= 1e-6), G5_mean_with_host_efe_map=z["G5"]["mean"],
                       G10=z["G10"]["status"], law_only_set=z)
            ka4["pass_"] = bool(ka4["G1_ok"] and ka4["G2_ok"] and ka4["G3_ok"] and ka4["G4_ok"] and ka4["G5_ok"])
            P(f"[{f}] KA4 (f -> 0 replays the record's law-only numbers): {'PASS' if ka4['pass_'] else 'FAIL'} G1 {ka4['G1_ok']} G2 {ka4['G2_ok']} G3 {ka4['G3_ok']} G4 {ka4['G4_ok']} G5 {ka4['G5_ok']}; "
              f"X-COP {ka4['G3'][0]:+.6f}/{ka4['G3'][1]:.6f} (GB1 {ka4['gb1'][0]:+.6f}/{ka4['gb1'][1]:.6f}); groups {ka4['G4']} (GB1 {ka4['gb1_G4']}); UDGs {ka4['G5_mean']:+.6f} (GB1 {ka4['gb1_G5']:+.6f}); G5 with the host EFE map at f 0: {ka4['G5_mean_with_host_efe_map']:+.6f}  [{time.time()-T0:.0f}s {rss():.2f}GB]")
        R_["KA4"] = ka4
        if ka4 and not ka4["pass_"]: P(f"[{f}] KA4 FAIL: stop"); continue
        R_["sets"] = {}
        for tag, var in (("as_written", dict(mode="as_written", law="adopted")), ("bracket_dynamic", dict(mode="bracket", law="adopted")), ("monotone_reported", dict(mode="monotone", law="adopted")),
                         ("proposal_nu_reported", dict(mode="as_written", law="proposal"))):
            o = eval_set(f, var, B, base, verbose=(tag == "as_written")); R_["sets"][tag] = o
            P(f"[{f}] {tag:22s}: " + summary(o) + f"  [{time.time()-T0:.0f}s {rss():.2f}GB]")
            dump(f"local{SUFFIX}_partial.json", RES)
        R_["bracket_runs"] = {f"{k[0]:.4g}|{k[1]:.4g}": v[1] for k, v in _BRC.items() if k[2] == a0}
    RES["peak_rss_GB"] = rss(); RES["seconds"] = time.time() - T0; RES["criteria"] = CRIT; RES["mutate"] = MUTATE; RES["note"] = NOTE
    RES["declared"] = dict(f=F_COSMIC, Rc0_kpc=RC0_KPC, W_crit=W_CRIT, gamma=GAMMA, mu=MU_DEFAULT, classes=CLASS, sigma_coma=SIGMA_COMA, sigma_host_dsph=SIGMA_HOST_DSPH, bracket=BRACKET, a0=A0H)
    dump(f"local{SUFFIX}.json", RES)
    pp = os.path.join(PARTS, f"local{SUFFIX}_partial.json")
    if os.path.exists(pp): os.remove(pp)
    P(f"local{SUFFIX} done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")

if __name__ == "__main__":
    P(f"WD1 {WHICH}{SUFFIX}. Criteria {CRIT}. f {F_COSMIC}, R_c0 {RC0_KPC} kpc, W_crit {W_CRIT}, gamma {GAMMA}; a0 canonical {A0H['canonical']:.4e} / alt {A0H['alt']:.4e}; R_cmb {RF['canonical']:.4f} / {RF['alt']:.4f}. {NOTE}; footings never pooled; adopts nothing.")
    if WHICH == "ka": run_ka()
    elif WHICH == "local": run_local()
    elif WHICH == "bullet":
        from wd1_bullet import run_bullet; run_bullet(RES)
    P(f"Adopts nothing. {NOTE}.")
