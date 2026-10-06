#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG350 -- an EMERGENT switch from the coarse-grained phase-space state (criteria: FROZEN_CRITERIA.md, e3e17f0fc).

State variable: sigma_ij = P_ij/rho, the second moment of the DF (10-moment / Gaussian closure, Q = 0).
Scored (MS-allowed, baryons): R-b0 f = H(sigma_b^2); R-b1 f = S(sigma_b^2/sigma_ref^2 - 1); R-s f = H(s_b - s_IGM).
Reported only: R-c (cold sigma, MS-forbidden), R-q (shock label), R-* (stellar sigma).
Tests (a) FRW/linear, (b) bound + fidelity + no flicker, (c) hyperbolicity + stress + edge, (d) conservation.
Controls K1 (FRW closure), K2 (isothermal sphere), MUTATE (CFG350_MUTATE=1: instantaneous theta_b reader).
DE12's transition() and L341's growth harness are exec'd read-only.
"""
import os, sys, json, math, io, contextlib, time
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("CFG350_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
T0 = time.time()
P = lambda *a: print(*a, flush=True)
OUT = {"lane": "CFG350", "mutate": MUTATE, "checks": {}, "numbers": {}}
CH = []


def check(name, measured, ok, reading=""):
    ok = bool(ok)
    CH.append((name, ok))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}" + (f"\n         reading:  {reading}" if reading else ""))
    return ok


def banner(t):
    P("\n" + "=" * 110 + "\n" + t + "\n" + "=" * 110)


P(__doc__.strip())
if MUTATE:
    P("\n  *** CFG350_MUTATE=1: the sigma reader is REPLACED by the instantaneous theta_b reader f = H(-theta_b) (CFG347 R1) ***")

# ------------------------------------------------------------------ record machinery, read-only (as CFG349)
P_DE12 = os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness.py")
NS = {"__name__": "de12_readonly", "__file__": P_DE12}
_src = open(P_DE12).read().split('banner("G1 G2')[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src, NS)
G, KPC, MS, FB, CS, transition, host = [NS[k] for k in ("G", "KPC", "MS", "FB", "CS", "transition", "host")]
H0, Om, rho_crit0, A0, Hz = NS["H0"], NS["Om"], NS["rho_crit0"], NS["A0"], NS["Hz"]
KB, MP = 1.380649e-23, 1.67262192e-27
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


def r_ta(z, Mb):
    """CFG347/349's turnaround radius: mean enclosed density (NFW + mean) = 5.55 rho_m-bar(z)."""
    hs = host(Mb, z); rb = rhom(z)
    fn = lambda lr: (menc_nfw(Mb, z, math.exp(lr)) / (4 / 3 * math.pi * math.exp(lr) ** 3) + rb) - 5.55 * rb
    return math.exp(brentq(fn, math.log(hs["r200"]), math.log(1e3 * hs["r200"])))


def Sstep(u):
    """C-infinity step: 0 for u <= 0, 1 for u >= 1 (no shape constant)."""
    if u <= 0: return 0.0
    if u >= 1: return 1.0
    a, b = math.exp(-1 / u), math.exp(-1 / (1 - u))
    return a / (a + b)


def dSstep(u, h=1e-6):
    return (Sstep(u + h) - Sstep(u - h)) / (2 * h)


SmaxP = max(dSstep(u) for u in np.linspace(0.01, 0.99, 981))
sig_th = lambda T, mu=0.59: math.sqrt(KB * T / (mu * MP))
Z_RE, TPOST, TPOST_LEN, GAM_TD = 7.7, 1e4, 5e3, 1.6


def T_igm(z, Tpost=TPOST):
    if z >= 150: return 2.725 * (1 + z)
    if z >= Z_RE: return 2.725 * 151 * ((1 + z) / 151) ** 2
    return Tpost


def sig_igm(z, Tpost=TPOST):
    return sig_th(T_igm(z, Tpost), 0.59 if z < Z_RE else 1.22)


SIG_HI, DSPH = 10.0 * KMS, {"Carina": 6.6, "Leo II": 6.6, "Sextans": 7.9, "Draco": 9.1, "Sculptor": 9.2, "Fornax": 11.7}
P(f"\n  DE12 loaded read-only (24 hosts); f_b = {FB:.4f}; host gas sigma(1e6 K, DE12 mu 0.6) = {CS['1e6K']/KMS:.1f} km/s; max S' = {SmaxP:.3f}")

# ============================================================================== FRW thermal history; route definitions
banner("ROUTES and the FRW thermal history of the baryons")
zgrid = np.concatenate([np.linspace(0, 10, 201), np.geomspace(10.01, 1100, 400)])
sIGM = np.array([sig_igm(z) for z in zgrid])
sig_post_max = max(sig_igm(z) for z in zgrid if z < Z_RE)
lin_fac = 1.1 ** ((GAM_TD - 1) / 2)          # sigma factor of a delta = 0.1 parcel on T ∝ Delta^(gamma-1)
SIG_REF = sig_post_max * lin_fac               # R-b1: the minimum sigma_ref that keeps (a)
P(f"  sigma_IGM: z=1100 {sig_igm(1100)/KMS:.2f}, z=150 {sig_igm(150)/KMS:.3f}, z=20 {sig_igm(20)/KMS:.3f}, z=8 {sig_igm(8)/KMS:.3f}, post-reion {sig_post_max/KMS:.2f} km/s "
  f"(lenient T0 5e3 K: {sig_th(TPOST_LEN)/KMS:.2f}); min over z <= 1100: {sIGM.min()/KMS:.3f} km/s > 0")
P(f"  R-b1 sigma_ref (minimum passing (a), incl. delta = 0.1 parcels on gamma = {GAM_TD}): {SIG_REF/KMS:.2f} km/s  [1 constant]")


def f_route(route, sig, s_minus_sIGM=None):
    if MUTATE: raise RuntimeError
    if route == "R-b0": return 1.0 if sig > 0 else 0.0
    if route == "R-b1": return Sstep(sig ** 2 / SIG_REF ** 2 - 1)
    if route == "R-s": return 1.0 if s_minus_sIGM > 0 else 0.0


ROUTES = ("R-b0", "R-b1", "R-s")
RES = {r: {} for r in ROUTES}

# ============================================================================== (a)
banner("(a) FRW + LINEAR")
a1 = {}
a1["R-b0"] = (sIGM.min() > 0, f"sigma_IGM >= {sIGM.min()/KMS:.3f} km/s > 0 at every z <= 1100: f = 1 on FRW (gas is never cold)")
a1["R-b1"] = (all(sig_igm(z) * (lin_fac if z < Z_RE else 1) <= SIG_REF * (1 + 1e-12) for z in zgrid),
              f"max sigma (mean + delta 0.1) = {sig_post_max*lin_fac/KMS:.2f} <= sigma_ref {SIG_REF/KMS:.2f} km/s (OFF by construction)")
# R-s: voids after reionisation sit ABOVE the mean adiabat when gamma < 5/3: s - s_IGM = (1.5(gamma - 1) - 1) ln Delta
coef = 1.5 * (GAM_TD - 1) - 1
s_void = coef * math.log(0.9)
a1["R-s"] = (s_void > 0, f"post-reion s - s_IGM = {coef:+.2f} ln Delta: a delta = -0.1 parcel has {s_void:+.4f} > 0 (ON) for every gamma < 5/3")
OFF = {"R-b0": sIGM.min() <= 0, "R-b1": a1["R-b1"][0], "R-s": s_void <= 0}
for r in ROUTES:
    RES[r]["A1"] = bool(OFF[r])
    P(f"  A1 {r}: {'OFF' if RES[r]['A1'] else 'ON'} on FRW/linear -- {a1[r][1]}")

# A2: 1D Zel'dovich multi-stream sigma (units: k = 1, Ddot = 1)
qg = np.linspace(-math.pi, math.pi, 400001)


def zel_sigma(DA, xs):
    X = qg + DA * np.sin(qg); V = np.sin(qg); J = 1 + DA * np.cos(qg)
    out = []
    for x0 in xs:
        d = X - x0; idx = np.where(np.sign(d[:-1]) * np.sign(d[1:]) < 0)[0]
        w = 1 / np.abs(J[idx]); v = V[idx]
        if len(idx) == 0:
            continue
        if len(idx) == 1:
            out.append((1, 0.0)); continue
        vb = np.sum(w * v) / np.sum(w)
        out.append((len(idx), math.sqrt(max(np.sum(w * (v - vb) ** 2) / np.sum(w), 0.0))))
    return out


# collapse occurs where J -> 0, i.e. q = pi; re-centre on q = pi
qg = np.linspace(0, 2 * math.pi, 400001)
xs = math.pi + np.linspace(-0.8, 0.8, 81)
pre = zel_sigma(0.9, xs); post = zel_sigma(1.5, xs)
pre_max = max(s for _, s in pre); pre_streams = max(n for n, _ in pre)
post_max = max(s for _, s in post); ms = [x - math.pi for x, (n, s) in zip(xs, post) if n >= 3]
P(f"  D*A = 0.9 (before crossing): max streams {pre_streams}, max sigma {pre_max:.3e} (exactly 0)")
P(f"  D*A = 1.5 (after):  multi-stream zone |x - x_c| <= {max(abs(v) for v in ms):.3f}, max sigma {post_max:.3f} (in units of the velocity amplitude)")
a2_ok = pre_streams == 1 and pre_max == 0.0 and post_max > 0
OUT["numbers"]["zeldovich"] = dict(pre_max=pre_max, post_max=post_max, ms_halfwidth=max(abs(v) for v in ms))

# A3 growth: L341 harness
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


GR = {fv: {ft: growth(ft, fv) for ft in FOOTS} for fv in (0.0, 1.0)}
P("  L341 growth: f = 0 -> " + "; ".join(f"{ft} D {v[0]:.8f} s8 {v[1]:.4f}" for ft, v in GR[0.0].items())
  + " | f = 1 -> " + "; ".join(f"{ft} D {v[0]:.2f} s8 {v[1]:.2f}" for ft, v in GR[1.0].items()))
fFRW = {"R-b0": 1.0, "R-b1": 0.0, "R-s": 0.0}   # the mean-FRW value of f for each route
for r in ROUTES:
    RES[r]["A2"] = a2_ok
    RES[r]["A3"] = all(abs(v[0] - 1) < 1e-6 for v in GR[fFRW[r]].values())
    RES[r]["a"] = RES[r]["A1"] and RES[r]["A2"] and RES[r]["A3"]
    check(f"A-{r} (a) FRW/linear: f OFF on the mean IGM and linear parcels; single-stream sigma = 0; growth = LCDM",
          f"A1 {RES[r]['A1']}, A2 {RES[r]['A2']}, A3 {RES[r]['A3']} (D ratio {GR[fFRW[r]]['canonical'][0]:.6g})", RES[r]["a"])

# ============================================================================== (b)
banner("(b) BOUND: ON at 30 kpc + local gas disc, fidelity, no flicker (closure ODE under compression cycles)")
rows = []
for hk in HOSTS:
    z, Mb, ft = hk; tr = TRS[KEY(*hk)]
    i = int(np.searchsorted(tr["r"], r30))
    gN = G * Mb * MS / r30 ** 2; g = float(np.interp(r30, tr["r"], tr["g"])); gph = g - gN
    yv = tr["y"][i]
    rph = max(Mb * MS * (NS["h_of"](yv) - yv * NS["dh_of"](yv)) / (2 * math.pi * r30 ** 3 * yv), 0.0)
    rb = tr["rho_b"][i]; sg = CS["1e6K"]
    ds = 1.5 * math.log(sg ** 2 / sig_igm(z) ** 2) - math.log(rb / (FB * rhom(z)))
    rows.append(dict(host=KEY(*hk), z=z, rb=rb, rph=rph, gph=gph, g=g, sig=sg, s_minus=ds))
hi_rho = 1.0e6 * 1.4 * MP                        # n_H = 1 cm^-3 local gas disc
ds_hi = 1.5 * math.log(SIG_HI ** 2 / sig_igm(0) ** 2) - math.log(hi_rho / (FB * rhom(0)))


def fid_dev(r, df):
    out = []
    for kk in (1 / KPC, 1 / (10 * KPC)):
        A = CS["1e6K"] ** 2 * kk ** 2 - 4 * math.pi * G * (r["rb"] / FB + r["rph"])
        out.append(df * (4 * math.pi * G * r["rph"] + abs(r["gph"]) * kk) / abs(A))
    return max(out)


def cycles(r, route):
    """10 cycles of a 10% compression at Omega(30 kpc); closure: d ln sigma^2/dt = -(2/3) theta (isotropic), s conserved."""
    Om30 = math.sqrt(r["g"] / r30); T = 10 * 2 * math.pi / Om30
    lnr = lambda t: 0.5 * math.log(1.1) * (1 - math.cos(Om30 * t))
    th = lambda t: -0.5 * math.log(1.1) * Om30 * math.sin(Om30 * t)
    sol = solve_ivp(lambda t, y: [-(2 / 3) * th(t)], (0, T), [math.log(r["sig"] ** 2)], max_step=T / 4000, rtol=1e-11, atol=1e-13, dense_output=True)
    tt = np.linspace(0, T, 8001); s2 = np.exp(sol.sol(tt)[0])
    resp = float(np.max(s2) / s2[0] - 1)
    adi = float(np.max(np.abs(s2 / s2[0] - np.exp((2 / 3) * np.array([lnr(t) for t in tt])))))
    if MUTATE:
        fv = np.array([1.0 if th(t) <= 0 else 0.0 for t in tt])
    elif route == "R-s":
        smin = [r["s_minus"] + 1.5 * math.log(v / s2[0]) - lnr(t) for v, t in zip(s2, tt)]
        fv = np.array([f_route(route, 0, x) for x in smin])
    else:
        fv = np.array([f_route(route, math.sqrt(v)) for v in s2])
    drop = float(np.max(np.maximum.accumulate(fv) - fv))
    return drop, resp, adi, int(np.sum(np.abs(np.diff(fv)) > 0.5))


for rt in ROUTES:
    fs = [f_route(rt, r["sig"], r["s_minus"]) if not MUTATE else 1.0 for r in rows]
    f_hi = f_route(rt, SIG_HI, ds_hi) if not MUTATE else float("nan")
    devs = []
    for r in rows:
        x = r["sig"] ** 2 / SIG_REF ** 2
        df = 0.0 if rt != "R-b1" else abs(Sstep(x * 1.1 ** (2 / 3) - 1) - Sstep(x - 1))
        devs.append(fid_dev(r, df))
    cy = [cycles(r, rt) for r in rows]
    RES[rt].update(B1a=min(fs) >= 0.9, B1b=f_hi >= 0.9, B2=max(devs) <= 0.1, B3=max(c[0] for c in cy) <= 1e-12)
    RES[rt]["b"] = RES[rt]["B1a"] and RES[rt]["B1b"] and RES[rt]["B2"] and RES[rt]["B3"]
    resp = max(c[1] for c in cy); adi = max(c[2] for c in cy); flips = max(c[3] for c in cy)
    OUT["numbers"][f"b_{rt}"] = dict(f_hosts=[min(fs), max(fs)], f_disc=f_hi, dev_max=max(devs), drop=max(c[0] for c in cy),
                                     sig2_response=resp, adiabat_err=adi, flips=flips)
    check(f"B-{rt} (b) ON 24/24 hosts at 30 kpc and in a local gas disc; fidelity dev <= 0.1; no flicker",
          f"hosts f {min(fs):.3f}-{max(fs):.3f} ({sum(v >= 0.9 for v in fs)}/24); disc f {f_hi:.3f}; dev max {max(devs):.2e}; "
          f"max drop {max(c[0] for c in cy):.2e}, flips {flips}; sigma^2 response {resp:.4f} (= 1.1^(2/3) - 1 = {1.1**(2/3)-1:.4f}), adiabat err {adi:.1e}",
          RES[rt]["b"])
P(f"  R-s numbers: host s - s_IGM at 30 kpc {min(r['s_minus'] for r in rows):+.2f}..{max(r['s_minus'] for r in rows):+.2f}; local disc {ds_hi:+.2f}")
P(f"  dSph reference (reported): sigma {sorted(DSPH.values())} km/s vs R-b1 sigma_ref {SIG_REF/KMS:.2f}: "
  f"{sum(v * KMS > SIG_REF for v in DSPH.values())}/6 above")
win = sig_post_max * lin_fac >= SIG_HI
P(f"  R-b1 window: max OFF (IGM post-reion, delta 0.1) {sig_post_max*lin_fac/KMS:.2f} km/s vs min ON (local HI disc) {SIG_HI/KMS:.1f} km/s -> "
  f"{'EMPTY: no constant sigma_ref passes (a) and (b)' if win else 'non-empty'}")
OUT["numbers"]["window"] = dict(max_off=sig_post_max * lin_fac / KMS, min_on=SIG_HI / KMS, empty=bool(win))
if MUTATE:
    flick = OUT["numbers"]["b_R-b0"]["flips"] > 0
    P(f"\n  MUTATE: theta_b reader flips {OUT['numbers']['b_R-b0']['flips']} times in 10 cycles -> flicker {'reproduced' if flick else 'NOT reproduced'}")
    json.dump(OUT, open(os.path.join(HERE, f"cfg350_emergent_switch_results{SUF}.json"), "w"), indent=1, default=str)
    sys.exit(1 if flick else 0)

# ============================================================================== (c)
banner("(c) TRANSITION: 10-moment hyperbolicity, the switch stress, the edge")


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


rng = np.random.default_rng(350)
bad = 0; maxim = 0.0; minrank = 10; speed_err = 0.0
for _ in range(1000):
    Mx = rng.normal(size=(3, 3)); Pm = Mx @ Mx.T + 0.05 * np.eye(3); rho = rng.uniform(0.1, 10); u = rng.normal()
    A = jac(rho, u, *rng.normal(size=2), Pm[0, 0], Pm[0, 1], Pm[0, 2], Pm[1, 1], Pm[1, 2], Pm[2, 2])
    ev, vec = np.linalg.eig(A)
    maxim = max(maxim, float(np.max(np.abs(ev.imag))))
    rk = np.linalg.matrix_rank(vec, tol=1e-9); minrank = min(minrank, rk)
    c = math.sqrt(Pm[0, 0] / rho)
    exp = np.sort([u] * 4 + [u - c, u - c, u + c, u + c, u - math.sqrt(3) * c, u + math.sqrt(3) * c])
    speed_err = max(speed_err, float(np.max(np.abs(np.sort(ev.real) - exp))))
    bad += rk < 10
A0d = jac(1.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0); rk0 = np.linalg.matrix_rank(np.linalg.eig(A0d)[1], tol=1e-9)
c1_ok = bad == 0 and maxim < 1e-8 and speed_err < 1e-6
check("C1 (c) 10-moment system strongly hyperbolic for sigma > 0 (1000 random states): real speeds u, u+-sqrt(s_xx) (x2), u+-sqrt(3 s_xx); 10 eigenvectors",
      f"non-diagonalisable {bad}/1000; max |Im| {maxim:.1e}; speed error {speed_err:.1e}; min rank {minrank}; dust limit sigma = 0: rank {rk0}/10 (dust's own Jordan block)", c1_ok)

# C2 switch stress: chi = 2 |L_M| S'/(rho sigma_ref^2); at 30 kpc and at the first caustic / shock ~0.35 r_ta
RTA = {KEY(*hk): r_ta(hk[0], hk[1]) for hk in HOSTS}
chi30, chiE = [], []
for hk, r in zip(HOSTS, rows):
    z, Mb, ft = hk; LM = r["gph"] ** 2 / (8 * math.pi * G)
    x = r["sig"] ** 2 / SIG_REF ** 2
    chi30.append(2 * LM * dSstep(x - 1) / (r["rb"] * SIG_REF ** 2))
    re = 0.35 * RTA[KEY(*hk)]; gNe = G * Mb * MS / re ** 2
    gphe = math.sqrt(gNe * A0[ft]) - gNe
    rbe = 4 * FB * 5.55 * rhom(z)                 # post-shock gas at the edge (lenient-high density)
    chiE.append(2 * (gphe ** 2 / (8 * math.pi * G)) * SmaxP / (rbe * SIG_REF ** 2))
C2 = {"R-b0": (True, "x delta(x) = 0: the sharp zero threshold adds no stress"),
      "R-b1": (max(chi30) < 1 and max(chiE) < 1, f"chi(30 kpc) max {max(chi30):.2e}; chi(edge, S' max) {min(chiE):.2e}-{max(chiE):.2e}"),
      "R-s": (True, "sharp threshold on s: s delta(s - s_IGM) stress lives on the edge surface only; bulk 0")}
# C3 edge: OFF in mean IGM/voids; OFF in unbound WHIM filaments; ON out to >= 0.3 r_ta
whim = [(T, D) for T in (1e5, 1e6, 1e7) for D in (10, 100)]
C3 = {}
C3["R-b0"] = (False, "ON on the mean IGM (sigma_th > 0 everywhere): no edge")
whim_on_b1 = [sig_th(T) > SIG_REF for T, D in whim]
C3["R-b1"] = (not any(whim_on_b1), f"WHIM sigma {sig_th(1e5)/KMS:.0f}-{sig_th(1e7)/KMS:.0f} km/s > sigma_ref: ON in {sum(whim_on_b1)}/6 unbound filament states")
whim_s = [1.5 * math.log(T / TPOST) - math.log(D) for T, D in whim]
C3["R-s"] = (False, f"ON in voids (a) and in {sum(v > 0 for v in whim_s)}/6 WHIM states; s - s_IGM range {min(whim_s):+.1f}..{max(whim_s):+.1f}")
for rt in ROUTES:
    RES[rt]["C1"] = c1_ok; RES[rt]["C2"] = C2[rt][0]; RES[rt]["C3"] = C3[rt][0]
    RES[rt]["c"] = c1_ok and C2[rt][0] and C3[rt][0]
    check(f"C-{rt} (c) hyperbolic + switch stress keeps P > 0 + edge confined to bound region",
          f"C1 {c1_ok}; C2 {C2[rt][1]}; C3 {C3[rt][1]}", RES[rt]["c"])
P(f"  host r_ta {min(RTA.values())/KPC:.0f}-{max(RTA.values())/KPC:.0f} kpc; first caustic 0.364 r_ta = {0.364*min(RTA.values())/KPC:.0f}-{0.364*max(RTA.values())/KPC:.0f} kpc "
  f"(Bertschinger 1985, quoted); gas shock 0.347 r_ta: both outside 30 kpc")

# ============================================================================== (d)
banner("(d) CONSERVATION and monotonicity")
t_, x_ = sp.symbols("t x", real=True)
rho_, u_, p_ = (sp.Function(n)(t_, x_) for n in ("rho", "u", "p"))      # 1D: p = P_xx
# primitive 10-moment (1D, xx component): rho_t = -(rho u)_x ; u_t = -u u_x - p_x/rho ; p_t = -u p_x - 3 p u_x
subs = {sp.diff(rho_, t_): -sp.diff(rho_ * u_, x_), sp.diff(u_, t_): -u_ * sp.diff(u_, x_) - sp.diff(p_, x_) / rho_,
        sp.diff(p_, t_): -u_ * sp.diff(p_, x_) - 3 * p_ * sp.diff(u_, x_)}
mom = sp.simplify((sp.diff(rho_ * u_, t_) + sp.diff(rho_ * u_ ** 2 + p_, x_)).subs(subs))
E_ = rho_ * u_ ** 2 / 2 + p_ / 2
en = sp.simplify((sp.diff(E_, t_) + sp.diff(u_ * E_ + p_ * u_, x_)).subs(subs))
adi = sp.simplify((sp.diff(p_ / rho_ ** 3, t_) + u_ * sp.diff(p_ / rho_ ** 3, x_)).subs(subs))
P(f"  sympy: momentum residual {mom}; energy residual {en}; 1D adiabat D(p/rho^3)/Dt = {adi}")
d1 = mom == 0 and en == 0 and adi == 0
# D2 parcel: L = M Vdot^2/2 - U(V) + f(sigma(V)) L_M(V) with sigma^2 = s0^2 (V0/V)^(2/3) on the adiabat; energy has no multiplier
tt_ = sp.symbols("t"); Vf = sp.Function("V")(tt_); Mi, s0, V0 = sp.symbols("M s0 V0", positive=True)
U, fF, LMf = sp.Function("U"), sp.Function("f"), sp.Function("L_M")
sig2 = s0 ** 2 * (V0 / Vf) ** sp.Rational(2, 3)
Lp = Mi * sp.diff(Vf, tt_) ** 2 / 2 - U(Vf) + fF(sig2) * LMf(Vf)
Ep = sp.simplify(sp.diff(Vf, tt_) * sp.diff(Lp, sp.diff(Vf, tt_)) - Lp)
eom = sp.diff(sp.diff(Lp, sp.diff(Vf, tt_)), tt_) - sp.diff(Lp, Vf)
dE = sp.simplify(sp.diff(Ep, tt_) - sp.diff(Vf, tt_) * eom)
P(f"  parcel energy E = {Ep};  dE/dt - Vdot*EOM = {sp.simplify(dE)}  (no multiplier anywhere; contrast CFG349 L-ord: E linear in lambda)")
d2 = sp.simplify(dE) == 0
# D3: RH entropy jump gamma = 5/3, s = 1.5 (ln p - gamma ln rho)
gm = 5 / 3
dsRH = []
for M in np.geomspace(1.0001, 100, 200):
    pr = (2 * gm * M ** 2 - (gm - 1)) / (gm + 1); dr = (gm + 1) * M ** 2 / ((gm - 1) * M ** 2 + 2)
    dsRH.append(1.5 * (math.log(pr) - gm * math.log(dr)))
cool = 1.5 * math.log(1e4 / 1e6) - math.log(100.0)    # isobaric cooling 1e6 -> 1e4 K (rho x100)
P(f"  D3: RH entropy jump min {min(dsRH):.2e} (M -> 1+) .. {max(dsRH):.2f} (M = 100), all >= 0; Zel'dovich crossing raises sigma from 0 to {post_max:.3f};")
P(f"      isobaric radiative cooling 1e6 -> 1e4 K changes s by {cool:+.2f}: collisional baryons are NOT monotone (cooling erases the record)")
for rt in ROUTES:
    RES[rt]["d"] = d1 and d2
check("D (d) conservation: conservative 10-moment momentum + energy identities; state-function switch has an ordinary parcel action (energy conserved, no multiplier)",
      f"D1 {d1}; D2 {d2}; D3 RH min ds {min(dsRH):.1e} >= 0, cooling {cool:+.2f}", d1 and d2)
OUT["numbers"]["d"] = dict(RH_min=min(dsRH), cooling_ds=cool)

# ============================================================================== reported routes + ownership
banner("REPORTED (not scored): R-c, R-q, R-*; OWNERSHIP")
rep = {
 "R-c": "sigma_c: exactly 0 on FRW single stream (a PASS), >0 inside the first caustic 0.364 r_ta (b PASS at 30 kpc, saturated, no flicker: "
        "x delta(x) = 0), strongly hyperbolic for sigma > 0, but ON in every shell-crossed sheet/filament (Zel'dovich sheet delta_lin = 1, unbound) "
        "-> C3 FAIL; MS1 matter/carrier door; B's S_cold is dust (no sigma) -> would add a collisionless-DF assumption. Equivalent tier: PARTIAL, not admissible.",
 "R-q": "shock/caustic label q (0 -> 1 at an entropy jump, advected): OFF on FRW and linear, ON in DE12's 1e6 K (shocked) gas, no flicker; legal as a Brown-type "
        "advected scalar; but after radiative cooling the local state carries no record (D3), so q is a MEMORY FIELD, not a coarse-grained state "
        "(CFG349's class); ON in shocked WHIM filaments; cold-mode (unshocked) streams at z >= 2 leave CGM gas OFF.",
 "R-*": "stellar sigma: 0 where no stars (FRW, web, star-free outer HI discs and CGM); stars are born with sigma ~ gas sigma, so 'sigma_* > 0' = 'stars "
        "present'; needs a coarse-graining scale L (1 constant); edge = stellar extent, far inside 0.3 r_ta; GC stars ON.",
}
for k, v in rep.items():
    P(f"  {k}: {v}")
own = dict(
    GC=dict(rho_own=1e3, sig_own=7.0, rho_host=1e-3, sig_host=150.0),
    binary_10kau=dict(rho_own_at_L_gt_a=0.0, sig_own=0.3, rho_host=0.1, sig_host=30.0))
sGC = math.sqrt((1e3 * 7.0 ** 2 + 1e-3 * (150 ** 2 + 150 ** 2)) / (1e3 + 1e-3))
P(f"  GC (class E): mass-weighted local sigma_b = {sGC:.2f} km/s (own dominates, rho_own/rho_host ~ 1e6): R-b0 ON, R-b1 {'OFF' if sGC*KMS < SIG_REF else 'ON'}, R-c ON (host halo)")
P(f"  dSph (class A): sigma 6.6-11.7 km/s, same range as GCs -> no sigma threshold separates E (GC) from A (dSph)")
P(f"  wide binary (class E): internal 0.3 km/s, but at any L > a the local DF is the field's (~30 km/s, 0.1 Msun/pc^3) -> R-b0/R-b1/R-c ON (inherit)")
P("  verdict on ownership: a local sigma reads 'own' only where the subsystem dominates the local density (GC cores), and then by amplitude it")
P("  cannot separate GCs (E, Newtonian) from dSphs (A, ON); binaries inherit the host. FG001's E/A classes are NOT reproduced.")
OUT["numbers"]["ownership"] = dict(GC_sigma=sGC, reproduced=False)

# ============================================================================== controls
banner("CONTROLS")
aa = np.geomspace(1e-3, 1, 200)
s0 = solve_ivp(lambda N, y: [-2 * y[0]], (math.log(1e-3), 0), [0.0], rtol=1e-12, atol=1e-30).y[0]
s1 = solve_ivp(lambda N, y: [-2 * y[0]], (math.log(1e-3), 0), [1.0], rtol=1e-12, atol=1e-30, dense_output=True)
k1err = max(abs(s1.sol(math.log(a))[0] / (a / 1e-3) ** -2 - 1) for a in aa)
k1 = np.max(np.abs(s0)) == 0.0 and k1err < 1e-8
check("K1 single-stream closure on FRW (L = H I): sigma_0 = 0 stays 0; sigma_0 > 0 gives sigma ∝ a^-2", f"max |sigma| (zero IC) {np.max(np.abs(s0)):.1e}; a^-2 err {k1err:.1e}", k1)
vc = 1.0; Gg = 1.0; A_ = vc ** 2 / (4 * math.pi * Gg)
rho_s = lambda r: A_ / r ** 2; M_s = lambda r: 4 * math.pi * A_ * r
k2v = []
for r in (0.1, 1.0, 10.0):
    I = quad(lambda rr: rho_s(rr) * Gg * M_s(rr) / rr ** 2, r, np.inf, limit=200)[0]
    k2v.append(math.sqrt(I / rho_s(r)))
k2 = max(abs(v - vc / math.sqrt(2)) for v in k2v) < 1e-6
check("K2 singular isothermal sphere: Jeans integral sigma = v_c/sqrt2", f"sigma = {k2v} vs {vc/math.sqrt(2):.8f}", k2)

# ============================================================================== verdict
banner("VERDICT (frozen rule, per scored route; best route wins)")
TIER = {}
for rt in ROUTES:
    npass = sum(RES[rt][k] for k in ("a", "b", "c", "d")); nc = 1 if rt == "R-b1" else 0
    tier = ("EMERGENT SWITCH WORKS" if nc == 0 else "WITH COST") if npass == 4 else ("PARTIAL" if npass == 3 else "NO-GO")
    TIER[rt] = dict(passes={k: RES[rt][k] for k in ("a", "b", "c", "d")}, n=npass, constants=nc, tier=tier)
    P(f"  {rt}: a {RES[rt]['a']}  b {RES[rt]['b']}  c {RES[rt]['c']}  d {RES[rt]['d']}  -> {npass}/4, constants {nc}: {tier}")
order = ["EMERGENT SWITCH WORKS", "WITH COST", "PARTIAL", "NO-GO"]
best = min(TIER.values(), key=lambda v: order.index(v["tier"]))["tier"]
P(f"\n  VERDICT: {best}. Obstruction: collisional baryons are never cold on FRW (sigma_IGM > 0 at every z) and lose their record by cooling;")
P(f"  the post-reionisation IGM ({sig_post_max*lin_fac/KMS:.1f} km/s) is hotter than the local gas discs B must switch ON ({SIG_HI/KMS:.0f} km/s), so no")
P(f"  constant threshold exists; the variable that has the right properties (cold sigma_c) is MS-forbidden and ON in unbound sheets.")
P("  Conservation is NOT the obstruction: a state-function switch has an ordinary action (D2). Scoped result, not a closure.")
OUT["routes"] = TIER; OUT["verdict"] = best; OUT["sigma_ref_kms"] = SIG_REF / KMS
OUT["controls"] = dict(K1=bool(k1), K2=bool(k2))
OUT["runtime_s"] = time.time() - T0
json.dump(OUT, open(os.path.join(HERE, f"cfg350_emergent_switch_results{SUF}.json"), "w"), indent=1, default=str)
P(f"\n  runtime {time.time()-T0:.1f} s")
sys.exit(0 if (k1 and k2) else 1)
