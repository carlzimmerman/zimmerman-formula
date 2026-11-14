"""AGB1R Part C: BAO + DESI compressed CMB prior + supernovae, CAMB 1.6.6 background (PPF), Sum m_nu 0.06 eV in one
massive state, N_eff 3.044, flat. Fitted (h, omega_b, omega_bc, w0, wa); M and A profiled analytically.
Modes: k5 (BAO + prior only: w0wa vs LCDM), full, des_only. Writes agb1r_C_<mode>.json / .out."""
import os, sys, time
import numpy as np
import camb
from scipy.optimize import minimize
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agb1r_common import (load_des, sample_keep, SN, BAO, build_template, CMB_MU, CMB_ICOV, C_KMS, qz, q0, QZ,
                          w1_word, w2_word, w3_word, intervals, dump, HERE, STARTS_A)

MODE = sys.argv[1]
OMNU = 0.06/93.14
GRID = [round(-1.0 + 0.25*i, 2) for i in range(17)]
SCALES = np.array([0.01, 3e-4, 2.5e-3, 0.1, 0.3])
t0 = time.time()
logf = open(os.path.join(HERE, f"agb1r_C_{MODE}.out"), "w")
def log(s=""):
    print(s, flush=True); logf.write(s + "\n"); logf.flush()

bao = BAO("all")
ZB = bao.zall
if MODE in ("full", "des_only"):
    D = load_des(); keep = sample_keep(D, MODE)
    TT = build_template("S"); sn = SN(D, keep, TT["spline"](D["zhd"][keep]))
else:
    sn = None

_cache = {}
def camb_bg(h, ob, obc, w0, wa):
    key = tuple(np.round([h, ob, obc, w0, wa], 12))
    if key in _cache: return _cache[key]
    P = camb.CAMBparams()
    P.set_dark_energy(w=w0, wa=wa, dark_energy_model="ppf")
    P.set_cosmology(H0=100*h, ombh2=ob, omch2=obc - ob, mnu=0.06, num_massive_neutrinos=1, nnu=3.044, omk=0)
    P.WantTransfer = False; P.WantCls = False
    R = camb.get_background(P); d = R.get_derived_params()
    zs = np.r_[ZB] if sn is None else np.r_[ZB, sn.z]
    DM = R.comoving_radial_distance(zs)
    DH = C_KMS/R.hubble_parameter(ZB)
    out = dict(th=d["thetastar"]/100, rd=d["rdrag"], DMb=DM[:len(ZB)], DH=DH, DMsn=DM[len(ZB):])
    if len(_cache) > 5000: _cache.clear()
    _cache[key] = out
    return out

def h_from_theta(ob, obc, w0, wa, th=CMB_MU[0]):
    P = camb.CAMBparams(); P.set_dark_energy(w=w0, wa=wa, dark_energy_model="ppf")
    P.set_cosmology(thetastar=th, ombh2=ob, omch2=obc - ob, mnu=0.06, num_massive_neutrinos=1, nnu=3.044, omk=0)
    return P.H0/100

def Om_of(h, obc): return (obc + OMNU)/h**2

def in_box(h, ob, obc, w0, wa):
    if not (0.4 < h < 1.0 and ob > 0.005 and obc - ob > 0.01): return False
    if not (-3 <= w0 <= 1 and -3 <= wa <= 2 and w0 + wa < 0): return False
    return 0.05 < Om_of(h, obc) < 0.7

def at_edge(h, ob, obc, w0, wa):
    e = []; Om = Om_of(h, obc)
    if Om - 0.05 < 0.003 or 0.7 - Om < 0.003: e.append("Om")
    if w0 + 3 < 0.01 or 1 - w0 < 0.01: e.append("w0")
    if wa + 3 < 0.01 or 2 - wa < 0.01: e.append("wa")
    if -(w0 + wa) < 0.01: e.append("w0+wa")
    if h - 0.4 < 0.003 or 1.0 - h < 0.003: e.append("h")
    return e

def evaluate(p, A, use_sn=True):
    h, ob, obc, w0, wa = p
    o = camb_bg(h, ob, obc, w0, wa)
    m = bao.model_vec(o["DMb"][:-1]/o["rd"], o["DH"][:-1]/o["rd"], o["DMb"][-1]/o["rd"], o["DH"][-1]/o["rd"])
    cb = bao.chi2_fixed(m)
    dv = np.array([o["th"], ob, obc]) - CMB_MU; cp = float(dv @ CMB_ICOV @ dv)
    if use_sn and sn is not None:
        muth = 5*np.log10((1 + sn.zhel)*o["DMsn"]) + 25
        cs, Au, M = sn.chi2(muth, A)
    else:
        cs, Au, M = 0.0, A, None
    return dict(chi2=cb + cp + cs, chi2_bao=cb, chi2_prior=cp, chi2_sn=cs, A=Au, M=M, theta=o["th"], rd=o["rd"])

def minq_p(p):
    h, ob, obc, w0, wa = p; q = qz(QZ, Om_of(h, obc), w0, wa); i = int(np.argmin(q)); return float(q[i]), float(QZ[i])

# ---------------- preconditioned Nelder-Mead ----------------
def _nm(f, x0, L, step=1.0, maxiter=6000):
    n = len(x0)
    g = lambda u: f(x0 + L @ u)
    sim = np.vstack([np.zeros(n)] + [np.eye(n)[i]*step for i in range(n)])
    r = minimize(g, np.zeros(n), method="Nelder-Mead",
                 options=dict(initial_simplex=sim, xatol=1e-6, fatol=1e-7, maxiter=maxiter, maxfev=2*maxiter))
    return x0 + L @ r.x, float(r.fun)

def hessian_L(f, x, scales):
    n = len(x); e = scales*0.3; f0 = f(x); H = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            if i == j:
                fp = f(x + e*np.eye(n)[i]); fm = f(x - e*np.eye(n)[i])
                if max(fp, fm) >= 1e9: return np.diag(scales)
                H[i, i] = (fp - 2*f0 + fm)/e[i]**2
            else:
                ei = e*np.eye(n)[i]; ej = e*np.eye(n)[j]
                vals = [f(x + ei + ej), f(x + ei - ej), f(x - ei + ej), f(x - ei - ej)]
                if max(vals) >= 1e9: return np.diag(scales)
                H[i, j] = H[j, i] = (vals[0] - vals[1] - vals[2] + vals[3])/(4*e[i]*e[j])
    lam, V = np.linalg.eigh(H)
    lam = np.maximum(np.abs(lam), 1e-6*np.abs(lam).max())
    return V @ np.diag(1/np.sqrt(lam))    # unit step along each column ~ dchi2 of 1

def nm_pre(f, x0, scales):
    """Raw-scaled NM, then two rounds of NM in Hessian-whitened coordinates (the restart polish)."""
    x, v = _nm(f, np.asarray(x0, float), np.diag(scales))
    for _ in range(2):
        L = hessian_L(f, x, scales)
        x2, v2 = _nm(f, x, L)
        if v2 <= v: x, v = x2, v2
    return x, v

# ---------------- fits ----------------
_starts_cache = {}
def fixed_starts():
    if "s" not in _starts_cache:
        _starts_cache["s"] = [(h_from_theta(CMB_MU[1], CMB_MU[2], w0, wa), CMB_MU[1], CMB_MU[2], w0, wa)
                              for (_, w0, wa) in STARTS_A]
    return _starts_cache["s"]

def fit(A, mode="free", extra=(), use_sn=True, lcdm=False):
    """mode free / q0 / never; A number or None (profiled). lcdm: w0 = -1, wa = 0 fixed (K5)."""
    if lcdm:
        unpack = lambda x: (x[0], x[1], x[2], -1.0, 0.0); sc = SCALES[:3]
        starts = [s[:3] for s in fixed_starts()[:1]] + [tuple(e[:3]) for e in extra]
    elif mode == "q0":
        def unpack(x):
            h, ob, obc, wa = x; return (h, ob, obc, -1/(3*(1 - Om_of(h, obc))), wa)
        sc = SCALES[[0, 1, 2, 4]]
        starts = [(s[0], s[1], s[2], s[4]) for s in list(fixed_starts()) + list(extra)]
    else:
        unpack = lambda x: tuple(x); sc = SCALES
        starts = [tuple(s) for s in list(fixed_starts()) + list(extra)]
    def base(x):
        p = unpack(x)
        if not in_box(*p): return 1e10
        try: return evaluate(p, A, use_sn)["chi2"]
        except Exception: return 1e10
    best = None
    for s0 in starts:
        if mode == "never":
            x = np.array(s0, float)
            for Lm in (1e2, 1e4, 1e6, 1e8):
                def f(xx, Lm=Lm):
                    v = base(xx)
                    if v >= 1e10: return v
                    return v + Lm*max(0.0, -minq_p(unpack(xx))[0])**2
                x, _ = nm_pre(f, x, sc)
            v = base(x); vr = v if minq_p(unpack(x))[0] >= -1e-3 else v + 1e6
        else:
            x, v = nm_pre(base, s0, sc); vr = v
        if best is None or vr < best[2]: best = (x, v, vr)
    x, v, _ = best
    p = unpack(x); r = evaluate(p, A, use_sn); mq, zq = minq_p(p)
    h, ob, obc, w0, wa = p; Om = Om_of(h, obc)
    rec = dict(h=float(h), omega_b=float(ob), omega_bc=float(obc), w0=float(w0), wa=float(wa), Om=float(Om),
               q0=float(q0(Om, w0)), chi2=r["chi2"], chi2_bao=r["chi2_bao"], chi2_prior=r["chi2_prior"],
               chi2_sn=r["chi2_sn"], A=r["A"], theta=r["theta"], rd=r["rd"], minq=mq, z_minq=zq, edge=at_edge(*p))
    if mode == "never": rec["constraint_met"] = bool(mq >= -1e-3)
    return rec

def pt(r): return (r["h"], r["omega_b"], r["omega_bc"], r["w0"], r["wa"])

def fmt(r):
    s = (f"h {r['h']:.4f} ob {r['omega_b']:.5f} obc {r['omega_bc']:.5f} Om {r['Om']:.4f} w0 {r['w0']:+.4f} "
         f"wa {r['wa']:+.4f} q0 {r['q0']:+.4f} A {r['A'] if r['A'] is None else round(r['A'], 4)}  chi2 {r['chi2']:.4f} "
         f"(BAO {r['chi2_bao']:.3f}, prior {r['chi2_prior']:.3f}, SN {r['chi2_sn']:.3f})  min q {r['minq']:+.4f} at z {r['z_minq']:.3f}")
    if r["edge"]: s += "  AT PRIOR EDGE " + ",".join(r["edge"])
    if "constraint_met" in r and not r["constraint_met"]: s += "  CONSTRAINT NOT MET"
    return s

out = dict(mode=MODE)
if MODE == "k5":
    lc = fit(0.0, lcdm=True, use_sn=False)
    ww = fit(0.0, use_sn=False)
    d = ww["chi2"] - lc["chi2"]
    out.update(lcdm=lc, w0wa=ww, dchi2=d, K5_pass=bool(abs(d + 8.0) <= 1.0))
    log(f"K5 BAO + compressed CMB prior, no SN:\n  LCDM {fmt(lc)}\n  w0wa {fmt(ww)}\n  chi2(w0wa) - chi2(LCDM) = {d:.3f}"
        f" (target -8.0 +- 1.0) -> {'PASS' if out['K5_pass'] else 'FAIL'}")
else:
    log(f"AGB1R Part C, sample {MODE}: {len(sn.z)} supernovae + all BAO + compressed CMB prior; template T_S")
    log("A profile (two sweeps):")
    up = {}; prev = None
    for A in GRID:
        up[A] = fit(A, extra=[] if prev is None else [pt(prev)]); prev = up[A]
    dn = {}; prev = None
    for A in GRID[::-1]:
        dn[A] = fit(A, extra=[] if prev is None else [pt(prev)]); prev = dn[A]
    prof = {}
    for A in GRID:
        prof[A] = up[A] if up[A]["chi2"] <= dn[A]["chi2"] else dn[A]
        prof[A]["sweep_diff"] = abs(up[A]["chi2"] - dn[A]["chi2"])
        log(f"  A {A:+.2f}  {fmt(prof[A])}  (sweeps differ {prof[A]['sweep_diff']:.2e})")
    gmin = min(GRID, key=lambda a: prof[a]["chi2"])
    fr = fit(None, extra=[pt(prof[gmin])])
    log(f"A free: {fmt(fr)}")
    forks = {"Afree": fr}
    for lab, Af in (("A0", 0.0), ("A1", 1.0)):
        r = fit(Af, extra=[pt(prof[Af])])
        if r["chi2"] > prof[Af]["chi2"]: r = prof[Af]
        prof[Af] = r; forks[lab] = r
    chis = np.array([prof[a]["chi2"] for a in GRID])
    from scipy.interpolate import CubicSpline
    sp = CubicSpline(GRID, chis); fine = np.linspace(GRID[0], GRID[-1], 400001); cf = sp(fine)
    ivg = {}
    for L in (1.0, 4.0):
        idx = np.where(cf - fr["chi2"] <= L)[0]
        if len(idx) == 0: ivg[L] = None; continue
        ivg[L] = [float(fine[idx[0]]) if idx[0] > 0 else None, float(fine[idx[-1]]) if idx[-1] < len(fine) - 1 else None]
    i = int(np.argmin(cf))
    d0 = prof[0.0]["chi2"] - fr["chi2"]; d1 = prof[1.0]["chi2"] - fr["chi2"]
    log(f"best A {fr['A']:+.4f}; dchi2 = 1 interval {ivg[1.0]}; dchi2 = 4 interval {ivg[4.0]}; spline min "
        f"{fine[i]:+.4f} ({cf[i]:.4f})")
    log(f"dchi2(A = 0) = {d0:.4f};  dchi2(A = 1) = {d1:.4f};  first word {w1_word(d0, d1)}")
    out.update(profile=prof, A_free=fr, interval_1=ivg[1.0], interval_4=ivg[4.0], dchi2_A0=d0, dchi2_A1=d1,
               spline_Amin=float(fine[i]), spline_chi2min=float(cf[i]), W1_first=w1_word(d0, d1))
    if MODE == "full":
        a0 = forks["A0"]
        out["K6"] = dict(w0=a0["w0"], wa=a0["wa"], pass_=bool(abs(a0["w0"] + 0.803) <= 0.040 and abs(a0["wa"] + 0.72) <= 0.16))
        log(f"K6 A = 0 fork: w0 {a0['w0']:+.4f} (target -0.803 +- 0.040), wa {a0['wa']:+.4f} (target -0.72 +- 0.16)"
            f" -> {'PASS' if out['K6']['pass_'] else 'FAIL'}")
    out["forks"] = {}
    for lab, Af in (("A0", 0.0), ("A1", 1.0), ("Afree", None)):
        b = forks[lab]
        rq = fit(Af, "q0", extra=[pt(b)]); rn = fit(Af, "never", extra=[pt(b)])
        dt = rq["chi2"] - b["chi2"]; dnv = rn["chi2"] - b["chi2"]
        out["forks"][lab] = dict(best=b, q0zero=rq, never=rn, dchi2_today=dt, dchi2_never=dnv,
                                 W2=w2_word(b["q0"], dt), W3=w3_word(dnv))
        log(f"fork {lab}:\n  best      {fmt(b)}\n  q0 = 0    {fmt(rq)}   dchi2_today {dt:.4f}\n"
            f"  never     {fmt(rn)}   dchi2_never {dnv:.4f}\n  W2 {w2_word(b['q0'], dt)};  W3 {w3_word(dnv)}")
out["runtime_s"] = time.time() - t0
dump(out, os.path.join(HERE, f"agb1r_C_{MODE}.json"))
log(f"done in {out['runtime_s']:.0f} s")
