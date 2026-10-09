#!/usr/bin/env python3
"""CFG508: dark energy vs cold energy -- difference and unity. Criteria: FROZEN_CRITERIA.md (committed alone first, 7e07bbe99).
On-disk data only (DESI DR2 w0wa chains; DESI DR1 ShapeFit f sigma8 table as transcribed in L181); CAMB for the LCDM P_lin;
stock CLASS for validation (K2).
Run:  nice -n 15 python3 cfg508_unity.py                    -> cfg508.out, cfg508_results.json
      CFG508_MUTATE=1 nice -n 15 python3 cfg508_unity.py    -> cfg508_MUTATE.out, cfg508_results_MUTATE.json
      (MUTATE: unified fluid with constant rest-frame c_s^2 = 0.01 on an LCDM background; T1a must EXCLUDE it.)"""
import os, sys, json, math, time
os.environ.setdefault("OMP_NUM_THREADS", "4")
import numpy as np
from scipy.integrate import solve_ivp, simpson
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
CHAINS = os.path.abspath(os.path.join(REPO, "..", "_external_data", "desi_dr2_chains"))
sys.path.insert(0, CFG)
import CFG2_common as C2  # noqa: E402  (read-only: footings)

MUT = os.environ.get("CFG508_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

# ---------------- cosmology (Planck 2018, flat; radiation neglected after z = 200) ----------------
h, OBH2, OCH2 = 0.6736, 0.02237, 0.1200
OB, OC = OBH2 / h**2, OCH2 / h**2
OM = OB + OC
OU = 1.0 - OB                      # unified fluid today (GCG) = 1 - Omega_b
CH0 = 2997.92458                   # c/H0 in Mpc/h
AI = 1.0 / 201.0
NI = math.log(AI)
KGRID = np.logspace(-3, math.log10(2.0), 40)   # h/Mpc
ZOUT = [0.0, 0.295, 0.510, 0.706, 0.919, 1.317, 1.491, 0.5, 1.0, 1.5]
ZOUT = sorted(set(ZOUT))
A0 = dict(C2.A0)
R_AMT = OC / OB

def gcg(alpha):
    """GCG background with the early dust amount = Omega_c (Planck) and flatness. Returns funcs of a."""
    q = 1.0 + alpha
    As = 1.0 - (OC / OU) ** q
    def x(a): return (1.0 - As) * a ** (-3.0 * q)
    def rho(a): return OU * (As + x(a)) ** (1.0 / q)
    def w(a): return -As / (As + x(a))
    return As, rho, w

# ---------------- linear sub-horizon solver (CLASS-form fluid equations, Newtonian gauge) ----------------
def solve_model(OD, rho_f, w_f, ca2_f, cs2_f, OL, kgrid, zout, rtol=1e-7):
    """Vectorised over k. Returns dict z -> arrays (delta_b, theta_b, delta_u, theta_u, psi_proxy) of shape (nk,)."""
    nk = len(kgrid)
    w_i = w_f(AI)
    y0 = np.concatenate([np.full(nk, AI), np.full(nk, -AI), np.full(nk, (1.0 + w_i) * AI), np.full(nk, -AI)])
    K = (np.asarray(kgrid) * CH0) ** 2
    def rhs(N, yy):
        a = math.exp(N)
        rf, w, ca2, cs2 = rho_f(a), w_f(a), ca2_f(a), cs2_f(a)
        rd = OD * a ** -3
        E2 = rd + rf + OL
        dE2 = -3.0 * rd - 3.0 * (1.0 + w) * rf
        dlnH = 0.5 * dE2 / E2
        K2 = K / (a * a * E2)
        db, tb, du, tu = yy[:nk], yy[nk:2*nk], yy[2*nk:3*nk], yy[3*nk:]
        K2psi = -1.5 * (rd * db + rf * du) / E2
        out = np.empty_like(yy)
        out[:nk] = -tb
        out[nk:2*nk] = -(2.0 + dlnH) * tb + K2psi
        out[2*nk:3*nk] = -(1.0 + w) * tu - 3.0 * (cs2 - w) * du - 9.0 * (1.0 + w) * (cs2 - ca2) * tu / K2
        out[3*nk:] = -(1.0 - 3.0 * cs2) * tu - (1.0 + dlnH) * tu + cs2 * K2 * du / (1.0 + w) + K2psi
        return out
    Nout = sorted([math.log(1.0 / (1.0 + z)) for z in zout])
    # add a neighbour point for each output to get dlnpsi/dN
    Neval = sorted(set(Nout + [n - 1e-3 for n in Nout]))
    def blow(N, yy): return 1e12 - np.max(np.abs(yy)) / AI
    blow.terminal = True
    with np.errstate(all="ignore"):
        s = solve_ivp(rhs, [NI, 0.0], y0, t_eval=Neval, method="DOP853", rtol=rtol, atol=1e-14, events=blow)
    if s.status == 1 or (not s.success) or len(s.t) < len(Neval):
        return None, s.nfev            # linear instability (imaginary sound speed): growth > 1e12 x before z = 0
    res = {}
    for z in zout:
        n = math.log(1.0 / (1.0 + z))
        j = int(np.argmin(np.abs(np.array(s.t) - n))); jm = int(np.argmin(np.abs(np.array(s.t) - (n - 1e-3))))
        def unpack(col):
            yy = s.y[:, col]; a = math.exp(s.t[col])
            db, tb, du, tu = yy[:nk], yy[nk:2*nk], yy[2*nk:3*nk], yy[3*nk:]
            psi = a * a * (OD * a ** -3 * db + rho_f(a) * du)       # psi up to a k-dependent constant
            return db, tb, du, tu, psi, a
        db, tb, du, tu, psi, a = unpack(j)
        _, _, _, _, psim, _ = unpack(jm)
        res[z] = dict(db=db, tb=tb, du=du, tu=tu, a=a, dlnpsi=(np.log(np.abs(psi)) - np.log(np.abs(psim))) / (s.t[j] - s.t[jm]))
    return res, s.nfev

def model_funcs(alpha=None, cs2_const=None):
    """U-A at alpha (adiabatic), or the MUTATE fluid (alpha = 0 background, constant rest-frame cs2)."""
    a_ = 0.0 if alpha is None else alpha
    As, rho, w = gcg(a_)
    ca2 = lambda a: -a_ * w(a)
    cs2 = (lambda a: cs2_const) if cs2_const is not None else ca2
    return As, rho, w, ca2, cs2

def observer_fields(res_z, alpha, rho_f, w_f):
    a = res_z["a"]
    rb, rce = OB * a ** -3, OC * a ** -3
    ru, w = rho_f(a), w_f(a)
    dobs = (rb * res_z["db"] + ru * res_z["du"]) / (rb + rce)
    vb = -res_z["tb"]
    vtot = -(rb * res_z["tb"] + (1.0 + w) * ru * res_z["tu"]) / (rb + (1.0 + w) * ru)
    return dobs, res_z["db"], vb, vtot

# ---------------- CAMB LCDM P_lin(k, z) ----------------
def camb_plin():
    import camb
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=100 * h, ombh2=OBH2, omch2=OCH2, mnu=0.0, num_massive_neutrinos=0, omk=0.0)
    pars.InitPower.set_params(As=2.1e-9, ns=0.9649)
    pars.set_matter_power(redshifts=ZOUT[::-1], kmax=20.0)
    r = camb.get_results(pars)
    kh, zs, pk = r.get_matter_power_spectrum(minkh=1e-4, maxkh=10.0, npoints=600)
    return kh, {round(float(z), 3): pk[i] for i, z in enumerate(zs)}

def w8(x):
    return 3.0 * (np.sin(x) - x * np.cos(x)) / x ** 3

def sig8(kh, pk, ratio2):
    integ = pk * ratio2 * w8(8.0 * kh) ** 2 * kh ** 2 / (2 * np.pi ** 2)
    return math.sqrt(simpson(integ, x=kh))

def interp_ratio(kh, kgrid, r):
    lr = np.interp(np.log(kh), np.log(kgrid), r, left=r[0], right=r[-1])
    return lr

# DESI DR1 Table 9 (as transcribed in fable_independent_2026/L181_desi_dr1_fsigma8_check.py)
DESI = [("BGS", 0.295, 0.80, 0.20, 0.20, 0.84, 0.19, 0.19), ("LRG1", 0.510, 1.09, 0.12, 0.14, 1.16, 0.13, 0.13),
        ("LRG2", 0.706, 1.05, 0.12, 0.12, 1.04, 0.11, 0.092), ("LRG3", 0.919, 0.96, 0.11, 0.10, 0.997, 0.10, 0.084),
        ("ELG2", 1.317, 0.95, 0.11, 0.08, 0.945, 0.097, 0.077), ("QSO", 1.491, 1.16, 0.12, 0.12, 1.16, 0.12, 0.12)]

def score_model(args):
    """Run one model; return T1 quantities. args = (label, alpha, cs2_const)."""
    label, alpha, cs2c = args
    As, rho, w, ca2, cs2 = model_funcs(alpha, cs2c)
    t0 = time.time()
    res, nfev = solve_model(0.0 + OB, rho, w, ca2, cs2, 0.0, KGRID, ZOUT)
    return label, alpha, cs2c, res, nfev, time.time() - t0

# ---------------- chains ----------------
def load_chain(nm):
    fn1 = os.path.join(CHAINS, nm, "chain.1.txt")
    hdr = open(fn1).readline().lstrip("#").split()
    cols = [hdr.index(c) for c in ("weight", "w", "wa", "omegam")]
    xs = []
    for kk in range(1, 5):
        d = np.loadtxt(os.path.join(CHAINS, nm, f"chain.{kk}.txt"), usecols=cols)
        xs.append(d[int(0.3 * len(d)):])
    x = np.vstack(xs)
    return x[:, 0], x[:, 1], x[:, 2], x[:, 3]

def wpct(v, wt, qs):
    o = np.argsort(v); c = np.cumsum(wt[o]) / wt.sum()
    return [float(v[o][min(np.searchsorted(c, q), len(v) - 1)]) for q in qs]

def cpl_f(z, w0, wa):
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))

def cpl_fit(alpha):
    As, rho, w = gcg(alpha)
    z = np.linspace(0, 2.5, 251); a = 1 / (1 + z)
    rde = OB * a ** -3 + rho(a) - OM * a ** -3          # rho_total - rho_m,obs  (crit0 units)
    f = rde / rde[0]
    X = np.vstack([3 * np.log(1 + z), -3 * z / (1 + z)]).T
    coef, *_ = np.linalg.lstsq(X, np.log(f), rcond=None)
    s, wa = coef; w0 = s - 1 - wa
    resid = float(np.max(np.abs(np.log(f) - X @ coef)))
    return float(w0), float(wa), resid, float(rde.min())

# ======================================================================================================
def main():
    T0 = time.time()
    P("=" * 110)
    P(f"CFG508{' MUTATE' if MUT else ''}: dark energy vs cold energy -- difference and unity (criteria 7e07bbe99)")
    P("=" * 110)
    P(f"Planck 2018: h {h}, Omega_b {OB:.5f}, Omega_c {OC:.5f}, Omega_m {OM:.5f}, R = Omega_c/Omega_b = {R_AMT:.3f}")
    P(f"footings (reported only; ratios are footing-independent): a0 canonical {A0['canonical']:.4e}, alt {A0['alt']:.4e}")
    J = dict(mutate=MUT, cosmology=dict(h=h, Ob=OB, Oc=OC, Om=OM, R=R_AMT))
    checks = {}

    # ---- CAMB ----
    kh, PK = camb_plin()
    P(f"CAMB LCDM P_lin at z = {sorted(PK)} (kmax 10 h/Mpc)")

    # ---- models ----
    if MUT:
        models = [("LCDM", 0.0, None), ("MUT_cs2_0.01", 0.0, 0.01)]
    else:
        mags = np.logspace(-8, -1, 29)
        models = [("LCDM", 0.0, None)] + [(f"a{s}{m:.2e}", s_ * m, None) for s, s_ in (("+", 1), ("-", -1)) for m in mags]
    with Pool(4) as pool:
        out = pool.map(score_model, models)
    out = {o[0]: o for o in out}
    P(f"solver runs: {len(out)} models, total {sum(o[5] for o in out.values()):.1f} s CPU")

    lab0, _, _, RL, _, _ = out["LCDM"]
    _, rhoL, wL = gcg(0.0)

    # ---- K1: alpha = 0 vs standard growth ODE ----
    def std_growth():
        def rhs(N, y):
            a = math.exp(N); E2 = OM * a ** -3 + (1 - OM)
            Om_a = OM * a ** -3 / E2; dlnH = 0.5 * (-3 * OM * a ** -3) / E2
            return [y[1], 1.5 * Om_a * y[0] - (2 + dlnH) * y[1]]
        Ns = sorted(set([math.log(1 / (1 + z)) for z in ZOUT]))
        s = solve_ivp(rhs, [NI, 0], [AI, AI], t_eval=Ns, method="DOP853", rtol=1e-11, atol=1e-15)
        return {round(1 / math.exp(n) - 1, 3): (s.y[0][i], s.y[1][i] / s.y[0][i]) for i, n in enumerate(s.t)}
    SG = std_growth()
    k1 = []
    for z in (0.0, 0.5, 1.5):
        dobs, db, vb, vt = observer_fields(RL[z], 0.0, rhoL, wL)
        D, f = SG[round(z, 3)]
        k1.append(max(np.max(np.abs(dobs / D - 1)), np.max(np.abs(vb / dobs / f - 1)), np.max(np.abs(vt / dobs / f - 1))))
    checks["K1"] = bool(max(k1) < 1e-4)
    P(f"  [{'PASS' if checks['K1'] else 'FAIL'}] K1 alpha = 0 reproduces the LCDM growth ODE (D, f, both tracers) at z = 0, 0.5, 1.5: max dev {max(k1):.2e} (< 1e-4)")

    # ---- K2: vs stock CLASS for a constant-cs2 fluid ----
    try:
        from classy import Class
        Ofld = 0.119 / h ** 2; Ocdm = 0.001 / h ** 2
        def run_class(cs2v):
            cl = Class()
            cl.set(dict(h=h, omega_b=OBH2, omega_cdm=0.001, Omega_fld=Ofld, w0_fld=-1e-5, wa_fld=0.0, cs2_fld=cs2v, use_ppf="no",
                        output="mTk", **{"P_k_max_h/Mpc": 3.0, "z_pk": 0.0}))
            cl.compute(); tr = cl.get_transfer(0.0); bg = cl.get_background()
            k = tr["k (h/Mpc)"]; d = tr["d_fld"]
            OLc = bg["(.)rho_lambda"][-1] / bg["(.)rho_crit"][-1]
            cl.struct_cleanup(); cl.empty()
            return k, d, OLc
        kc, d1, OLc = run_class(1e-6); _, d0, _ = run_class(0.0)
        kt = np.array([0.1, 0.3, 1.0])
        rc = np.interp(kt, kc, d1 / d0)
        OD = OB + Ocdm; wf = -1e-5
        rho_f = lambda a: Ofld * a ** (-3 * (1 + wf)); w_f = lambda a: wf; ca2_f = lambda a: wf
        OLm = 1 - OD - Ofld
        r1, _ = solve_model(OD, rho_f, w_f, ca2_f, lambda a: 1e-6, OLm, kt, [0.0])
        r0, _ = solve_model(OD, rho_f, w_f, ca2_f, lambda a: 0.0, OLm, kt, [0.0])
        rm = r1[0.0]["du"] / r0[0.0]["du"]
        dev = np.abs(rm - rc); mask = rc > 0.1
        checks["K2"] = bool(np.all(dev[mask] <= 0.02))
        P(f"  [{'PASS' if checks['K2'] else 'FAIL'}] K2 solver vs stock CLASS, fluid cs2 = 1e-6, delta_fld ratio at z = 0, k = 0.1/0.3/1: "
          f"mine {rm[0]:.4f}/{rm[1]:.4f}/{rm[2]:.4f}, CLASS {rc[0]:.4f}/{rc[1]:.4f}/{rc[2]:.4f}; max |dev| {dev[mask].max():.4f} (<= 0.02); CLASS Omega_L {OLc:.4f} vs mine {OLm:.4f}")
        J["K2"] = dict(mine=rm.tolist(), CLASS=rc.tolist(), k=kt.tolist())
    except Exception as e:
        checks["K2"] = False
        P(f"  [FAIL] K2 CLASS validation could not run: {e!r}")

    # ---- T1: fsigma8 and growth cut per model ----
    def t1(lbl):
        _, alpha, cs2c, R, nfev, dt = out[lbl]
        As, rho, w, ca2, cs2 = model_funcs(alpha, cs2c)
        rows = {}
        for trc in ("baryon", "total"):
            chi_sfb = chi_sf = 0.0; ratios = []
            for t, z, r1, p1, m1, r2, p2, m2 in DESI:
                dL, _, vL, _ = observer_fields(RL[z], 0.0, rhoL, wL)
                dM, dbM, vbM, vtM = observer_fields(R[z], alpha, rho, w)
                vM = vbM if trc == "baryon" else vtM
                pkz = PK[round(z, 3)]
                num = sig8(kh, pkz, interp_ratio(kh, KGRID, (vM / dL) ** 2))
                den = sig8(kh, pkz, interp_ratio(kh, KGRID, (vL / dL) ** 2))
                rr = num / den; ratios.append(rr)
                chi_sfb += ((r2 - rr) / (0.5 * (p2 + m2))) ** 2; chi_sf += ((r1 - rr) / (0.5 * (p1 + m1))) ** 2
            dL0, _, _, _ = observer_fields(RL[0.0], 0.0, rhoL, wL)
            dM0, dbM0, _, _ = observer_fields(R[0.0], alpha, rho, w)
            dd = dM0 if trc == "total" else dbM0
            Pr = (dd / dL0) ** 2
            s8r = sig8(kh, PK[0.0], interp_ratio(kh, KGRID, Pr)) / sig8(kh, PK[0.0], np.ones_like(kh))
            mP = float(np.max(np.abs(Pr[KGRID <= 1.0] - 1)))
            rows[trc] = dict(fs8_ratio=ratios, chi2_SFB=chi_sfb, chi2_SF=chi_sf, s8_ratio=s8r, maxP=mP,
                             cut_ok=bool(abs(s8r - 1) <= 0.05 and mP <= 0.10))
        return rows, nfev, dt
    BLOW = [l for l in out if out[l][3] is None]
    T1 = {lbl: t1(lbl) for lbl in out if lbl not in BLOW}
    c0 = T1["LCDM"][0]["baryon"]["chi2_SFB"]
    checks["K4"] = bool(abs(c0 - 4.56) < 0.01)
    P(f"  [{'PASS' if checks['K4'] else 'FAIL'}] K4 LCDM chi2 (ShapeFit+BAO) = {c0:.3f} vs L181's 4.56 (|d| < 0.01)")

    P("\nT1 per model (Delta chi2 vs LCDM on DESI DR1 ShapeFit+BAO; growth cut = CFG361 on z = 0 linear P):")
    P(f"  {'model':<14} {'cs2_today':>10} | {'baryon: dchi2  s8r   maxP':>28} | {'total: dchi2  s8r   maxP':>27} | T1a  T1b  [nfev, s]")
    T1sum = {}
    for lbl in BLOW:
        _, alpha, cs2c, _, nfev, dt = out[lbl]
        T1sum[lbl] = dict(alpha=alpha, cs2_const=cs2c, cs2_today=model_funcs(alpha, cs2c)[4](1.0), dchi2=dict(baryon=float("inf"), total=float("inf")),
                          T1a_excluded=True, T1b_fails=True, rows=None, nfev=nfev, blowup=True)
        P(f"  {lbl:<14} {T1sum[lbl]['cs2_today']:10.2e} | LINEAR BLOW-UP (imaginary sound speed; delta > 1e12 x initial before z = 0) -> EXCL FAIL [{nfev}]")
    for lbl in [l for l in out if l not in BLOW]:
        rows, nfev, dt = T1[lbl]
        _, alpha, cs2c, *_ = out[lbl]
        As, rho, w, ca2, cs2 = model_funcs(alpha, cs2c)
        cs2now = cs2(1.0)
        d = {trc: rows[trc]["chi2_SFB"] - c0 for trc in rows}
        excl_a = bool(d["baryon"] >= 9 and d["total"] >= 9)
        fail_b = bool((not rows["baryon"]["cut_ok"]) and (not rows["total"]["cut_ok"]))
        T1sum[lbl] = dict(alpha=alpha, cs2_const=cs2c, cs2_today=cs2now, dchi2=d, T1a_excluded=excl_a, T1b_fails=fail_b,
                          rows=rows, nfev=nfev)
        if True:
            P(f"  {lbl:<14} {cs2now:10.2e} | {d['baryon']:+9.2f} {rows['baryon']['s8_ratio']:6.4f} {rows['baryon']['maxP']:6.3f} |"
              f" {d['total']:+9.2f} {rows['total']['s8_ratio']:6.4f} {rows['total']['maxP']:6.3f} | {'EXCL' if excl_a else 'ok  '} {'FAIL' if fail_b else 'ok  '} [{nfev}, {dt:.1f}]")
    J["T1"] = T1sum

    if MUT:
        m = T1sum["MUT_cs2_0.01"]
        J["mutate_excluded"] = m["T1a_excluded"]
        P(f"\nMUTATE: unified fluid with constant c_s^2 = 0.01: T1a {'EXCLUDED' if m['T1a_excluded'] else 'NOT EXCLUDED'} "
          f"(dchi2 baryon {m['dchi2']['baryon']:+.1f}, total {m['dchi2']['total']:+.1f}); T1b {'FAILS CUT' if m['T1b_fails'] else 'passes cut'}")
        # ISW proxy for MUTATE
        R = out["MUT_cs2_0.01"][3]
        for z in (0.0, 0.5, 1.0):
            ik = [int(np.argmin(np.abs(KGRID - kk))) for kk in (0.01, 0.1)]
            P(f"  ISW proxy dlnPhi/dlna z={z}: k=0.01 {R[z]['dlnpsi'][ik[0]]:+.3f}, k=0.1 {R[z]['dlnpsi'][ik[1]]:+.3f}; LCDM {RL[z]['dlnpsi'][ik[0]]:+.3f}")
        verdict = "MUTATE OK: the power-spectrum test excludes c_s^2 = 0.01" if m["T1a_excluded"] else "MUTATE FAILED: test cannot fail -> lane VOID"
        P(verdict); J["verdict"] = verdict
        ok = m["T1a_excluded"] and checks.get("K1") and checks.get("K4")
        finish(J, checks, T0)
        return 0 if ok else 1

    # ---- allowed interval in alpha ----
    def interval(key):
        lims = {}
        for sgn in (+1, -1):
            labs = sorted([l for l in T1sum if l != "LCDM" and np.sign(T1sum[l]["alpha"]) == sgn], key=lambda l: abs(T1sum[l]["alpha"]))
            allowed = 0.0; first_bad = None
            for l in labs:
                bad = T1sum[l][key]
                if bad:
                    first_bad = abs(T1sum[l]["alpha"]); break
                allowed = abs(T1sum[l]["alpha"])
            notex = [abs(T1sum[l]["alpha"]) for l in labs if not T1sum[l][key]]
            islands = [x for x in notex if first_bad is not None and x > first_bad]
            lims["+" if sgn > 0 else "-"] = dict(last_allowed=allowed, first_excluded=first_bad,
                                                 max_not_excluded=max(notex) if notex else 0.0, islands_beyond_first_exclusion=islands)
        return lims
    IA, IB = interval("T1a_excluded"), interval("T1b_fails")
    P(f"\nT1a (DESI DR1 f sigma8, both tracers) allowed alpha: +side up to {IA['+']['last_allowed']:.2e} (first excluded {IA['+']['first_excluded']}),"
      f" -side down to -{IA['-']['last_allowed']:.2e} (first excluded {IA['-']['first_excluded']})")
    P(f"T1b (CFG361 growth cut) allowed alpha: +side up to {IB['+']['last_allowed']:.2e} (first failing {IB['+']['first_excluded']}),"
      f" -side down to -{IB['-']['last_allowed']:.2e} (first failing {IB['-']['first_excluded']})")
    for nmI, I in (("T1a", IA), ("T1b", IB)):
        for sd in "+-":
            if I[sd]["islands_beyond_first_exclusion"]:
                P(f"  DISCLOSED: {nmI} {sd}side has NOT-excluded grid points beyond the first exclusion (non-contiguous allowed set): "
                  + ", ".join(f"{x:.2e}" for x in I[sd]["islands_beyond_first_exclusion"]) + f"; max not excluded {I[sd]['max_not_excluded']:.2e}")
    both = [T1sum[l]["alpha"] for l in T1sum if not T1sum[l]["T1a_excluded"] and not T1sum[l]["T1b_fails"]]
    P(f"T1a AND T1b together: allowed alpha in [{min(both):.2e}, {max(both):.2e}] (grid), all contiguous: "
      f"{all((not T1sum[l]['T1a_excluded'] and not T1sum[l]['T1b_fails']) for l in T1sum if min(both) <= T1sum[l]['alpha'] <= max(both))}")
    J["T1a_interval"], J["T1b_interval"], J["T1ab_allowed"] = IA, IB, [min(both), max(both)]

    # ---- T2: DESI DR2 background projection ----
    P("\nT2 background (DESI DR2 w0wa chains, 2-D Gaussian; observer assumes non-interacting dust omega_c):")
    w0L, waL, resL, _ = cpl_fit(0.0)
    checks["K3"] = bool(abs(w0L + 1) < 1e-6 and abs(waL) < 1e-6)
    P(f"  [{'PASS' if checks['K3'] else 'FAIL'}] K3 alpha = 0 -> (w0, wa) = ({w0L:+.2e}+(-1), {waL:+.2e})")
    G = {}
    CH = {}
    for nm in ("cmb", "pantheonplus", "union3", "desy5"):
        wt, w0, wa, om = load_chain(nm); CH[nm] = (wt, w0, wa, om)
        mu = np.array([np.average(w0, weights=wt), np.average(wa, weights=wt)])
        C = np.cov(np.vstack([w0, wa]), aweights=wt)
        G[nm] = (mu, np.linalg.inv(C))
        P(f"  chain {nm:12s}: <w0> {mu[0]:+.3f} +- {math.sqrt(C[0,0]):.3f}, <wa> {mu[1]:+.3f} +- {math.sqrt(C[1,1]):.3f}, rho {C[0,1]/math.sqrt(C[0,0]*C[1,1]):+.2f}")
    agrid = np.concatenate([-np.logspace(-1, -5, 41), [0.0], np.logspace(-5, -1, 41), np.linspace(0.11, 0.6, 50), -np.linspace(0.11, 0.6, 50)])
    agrid = np.unique(agrid)
    rows2 = []
    for a_ in agrid:
        w0, wa, res, rmin = cpl_fit(a_)
        chi = {nm: float((np.array([w0, wa]) - G[nm][0]) @ G[nm][1] @ (np.array([w0, wa]) - G[nm][0])) for nm in G}
        rows2.append((a_, w0, wa, res, rmin, chi))
    chi0 = [r for r in rows2 if r[0] == 0.0][0][5]
    best = {}
    for nm in G:
        r = min(rows2, key=lambda r: r[5][nm])
        best[nm] = dict(alpha=float(r[0]), w0=r[1], wa=r[2], dchi2=r[5][nm] - chi0[nm], cpl_resid=r[3], min_rhoDE=r[4])
        P(f"  best alpha for {nm:12s}: {r[0]:+.4f} -> (w0, wa)_eff = ({r[1]:+.3f}, {r[2]:+.3f}), dchi2 vs alpha=0 {r[5][nm]-chi0[nm]:+.2f} (CPL resid {r[3]:.1e}, min rho_DE,eff {r[4]:+.3f})")
    sn = ("pantheonplus", "union3", "desy5")
    # a joint best alpha on SN chains: per-alpha require all three
    prefers = all(best[nm]["dchi2"] <= -4 for nm in sn)
    P(f"  DESI-PREFERS-U-A (dchi2 <= -4 on all three SN chains at each chain's best alpha): {prefers}")
    # what does alpha in the T1a interval do?
    amaxp, amaxm = IA["+"]["last_allowed"], IA["-"]["last_allowed"]
    for a_ in (amaxp, -amaxm):
        w0, wa, res, _ = cpl_fit(a_)
        chi = {nm: float((np.array([w0, wa]) - G[nm][0]) @ G[nm][1] @ (np.array([w0, wa]) - G[nm][0])) - chi0[nm] for nm in G}
        P(f"  at T1a bound alpha = {a_:+.2e}: (w0, wa)_eff = ({w0:+.6f}, {wa:+.6f}); dchi2 vs alpha=0: " + ", ".join(f"{k} {v:+.4f}" for k, v in chi.items()))
    clash = None
    if prefers:
        ab = [best[nm]["alpha"] for nm in sn]
        clash = all((x > amaxp) or (x < -amaxm) for x in ab)
        P(f"  CLASH: preferred alphas {ab} outside T1a interval [-{amaxm:.1e}, {amaxp:.1e}]: {clash}"
          + (" -> the unified-fluid reading of DESI's w(z) is EXCLUDED by growth" if clash else ""))
    J["T2"] = dict(best=best, prefers=prefers, clash=clash, chi0=chi0)

    # a0(z) consequences (U-X decomposition: rho_v = -P = -w rho_u)
    def a0ratio(a_, z):
        _, rho, w = gcg(a_); a = 1 / (1 + z)
        return math.sqrt((-w(a) * rho(a)) / (-w(1.0) * rho(1.0)))
    P("\n  a0(z)/a0(0) = sqrt(rho_v(z)/rho_v(0)) in the U-X decomposition (H2 / w=-1: 1 exactly):")
    a0c = {}
    for tag, a_ in (("T1a bound +", amaxp), ("T1a bound -", -amaxm)) + tuple((f"DESI best {nm}", best[nm]["alpha"]) for nm in sn):
        vals = [a0ratio(a_, z) for z in (1.0, 2.0, 2.5)]
        a0c[tag] = dict(alpha=a_, z1=vals[0], z2=vals[1], z25=vals[2],
                        a0_z25_canonical=vals[2] * A0["canonical"], a0_z25_alt=vals[2] * A0["alt"])
        P(f"    {tag:22s} alpha {a_:+.2e}: z=1 {vals[0]:.6f}, z=2 {vals[1]:.6f}, z=2.5 {vals[2]:.6f}")
    # compare: DESI w0wa (non-interacting) sqrt(rho_DE) at z = 2.5 per chain
    for nm in sn:
        wt, w0, wa, om = CH[nm]
        r = np.sqrt(cpl_f(2.5, w0, wa)); q = wpct(r, wt, (0.16, 0.5, 0.84))
        P(f"    DESI {nm:12s} non-interacting a0(2.5)/a0(0) = sqrt(rho_DE ratio): {q[1]:.3f} [{q[0]:.3f}, {q[2]:.3f}]")
        a0c[f"DESI_noninteracting_{nm}"] = q
    J["a0z"] = a0c

    # ---- ISW proxy ----
    P("\n  ISW proxy: dlnPhi/dlna (LCDM vs U-A at the T1a bound; 0 = no ISW):")
    lb = [l for l in T1sum if abs(T1sum[l]["alpha"] - amaxp) < 1e-15 * max(1, amaxp) or (T1sum[l]["alpha"] == amaxp)]
    isw = {}
    for lbl in ["LCDM"] + lb:
        R = out[lbl][3]; ik = [int(np.argmin(np.abs(KGRID - kk))) for kk in (0.01, 0.1)]
        isw[lbl] = {str(z): [float(R[z]["dlnpsi"][ik[0]]), float(R[z]["dlnpsi"][ik[1]])] for z in (0.0, 0.5, 1.0)}
        P(f"    {lbl:14s}: " + "; ".join(f"z={z}: k0.01 {v[0]:+.4f}, k0.1 {v[1]:+.4f}" for z, v in isw[lbl].items()))
    J["ISW"] = isw

    # ---- T3: fixed ratio ----
    P("\nT3 fixed ratio rho_c/rho_DE across epochs (cold energy non-interacting, CPL rho_DE; DESI DR2 chains):")
    upass = {}
    T3 = {}
    for nm in ("cmb", "pantheonplus", "union3", "desy5"):
        wt, w0, wa, om = CH[nm]
        qq = {}
        for z in (0.5, 1.0, 2.0):
            rr = (1 + z) ** 3 / cpl_f(z, w0, wa)
            qq[z] = wpct(rr, wt, (0.025, 0.5, 0.975))
        ok = all(qq[z][0] <= 1.0 <= qq[z][2] for z in (1.0, 2.0))
        upass[nm] = ok; T3[nm] = {str(z): v for z, v in qq.items()}
        P(f"  {nm:12s}: r(z)/r(0) median [95%]: z=0.5 {qq[0.5][1]:.2f} [{qq[0.5][0]:.2f},{qq[0.5][2]:.2f}], z=1 {qq[1.0][1]:.2f} [{qq[1.0][0]:.2f},{qq[1.0][2]:.2f}],"
          f" z=2 {qq[2.0][1]:.2f} [{qq[2.0][0]:.2f},{qq[2.0][2]:.2f}] -> U-R {'PASSES' if ok else 'fails'}")
    UR = "PASSES" if any(upass.values()) else "EXCLUDED"
    P(f"  U-R (fixed ratio): {UR}")
    # scrambled cosmology (K5)
    rng = np.random.default_rng(508)
    maxdiff = 0.0; fp = 0
    wt, w0, wa, om = CH["desy5"]
    sub = rng.choice(len(w0), size=5000, p=wt / wt.sum())
    w0s, was = w0[sub], wa[sub]
    for _ in range(200):
        Rp = rng.uniform(3, 8); Ocp = Rp * OB; ODp = 1 - Ocp - OB
        passes = True
        for z in (1.0, 2.0):
            r_lit = (Ocp * (1 + z) ** 3 / (ODp * cpl_f(z, w0s, was))) / (Ocp / ODp)
            r_ref = (1 + z) ** 3 / cpl_f(z, w0s, was)
            maxdiff = max(maxdiff, float(np.max(np.abs(r_lit / r_ref - 1))))
            q = np.percentile(r_lit, [2.5, 97.5])
            passes &= bool(q[0] <= 1 <= q[1])
        fp += int(passes)
    checks["K5"] = bool(maxdiff < 1e-12)
    P(f"  [{'PASS' if checks['K5'] else 'FAIL'}] K5 scrambled cosmology (200 draws R' in [3,8]): ratio drift independent of R' (max rel change {maxdiff:.1e}); false U-R passes {fp}/200")
    J["T3"] = dict(per_chain=T3, UR=UR, scrambled_false_pass=fp, scrambled_maxdiff=maxdiff)

    # ---- post-freeze checks (no verdict weight) ----
    P("\nPOST-FREEZE checks (labelled, no verdict weight):")
    PF = {}
    # P1: are the total-tracer 'islands' numerical? re-solve at rtol 1e-9
    for a_ in (10 ** -2.75, 10 ** -1.5):
        As, rho, w, ca2, cs2 = model_funcs(a_)
        r7, _ = solve_model(OB, rho, w, ca2, cs2, 0.0, KGRID, [0.51], rtol=1e-7)
        r9, _ = solve_model(OB, rho, w, ca2, cs2, 0.0, KGRID, [0.51], rtol=1e-9)
        d = float(np.max(np.abs(r7[0.51]["tu"] - r9[0.51]["tu"]) / np.max(np.abs(r9[0.51]["tu"]))))
        PF[f"P1_rtol_{a_:.2e}"] = d
        P(f"  P1 alpha {a_:.2e}: fluid velocity at z=0.51, rtol 1e-7 vs 1e-9: max rel diff {d:.1e} (islands are not a solver artefact if small)")
    # P1b: what the total tracer velocity is made of at an island
    a_ = 10 ** -2.75
    As, rho, w, ca2, cs2 = model_funcs(a_)
    hit = [l for l in out if out[l][3] is not None and np.isclose(out[l][1], a_, rtol=1e-6)]
    R = out[hit[0]][3] if hit else None
    if R is not None:
        z = 0.51; a = R[z]["a"]; ru = rho(a); rb = OB * a ** -3
        ik = int(np.argmin(np.abs(KGRID - 0.1)))
        vb = -R[z]["tb"][ik]; vu = -R[z]["tu"][ik]; vL = -RL[z]["tb"][ik]
        P(f"  P1b alpha {a_:.2e}, k=0.1, z=0.51: baryon velocity / LCDM {vb/vL:+.3f}, fluid velocity / LCDM {vu/vL:+.3f}, "
          f"fluid delta / LCDM {R[z]['du'][ik]/((1+w(a))*RL[z]['du'][ik]/(1+wL(a))):+.3f} -> the total tracer is carried by acoustic flow of the fluid")
        PF["P1b"] = dict(vb=vb / vL, vu=vu / vL)
    # P2: negative-alpha blow-ups restricted to data scales (k <= 0.2 h/Mpc)
    kd = np.logspace(-3, math.log10(0.2), 20)
    for a_ in (-(10 ** -4.5), -1e-4, -1e-3):
        As, rho, w, ca2, cs2 = model_funcs(a_)
        r, _ = solve_model(OB, rho, w, ca2, cs2, 0.0, kd, [0.0, 0.51])
        rL, _ = solve_model(OB, rhoL, wL, lambda a: 0.0, lambda a: 0.0, 0.0, kd, [0.0, 0.51])
        if r is None:
            P(f"  P2 alpha {a_:.2e}: blows up even with k <= 0.2 h/Mpc"); PF[f"P2_{a_:.0e}"] = "blowup_k<=0.2"
        else:
            g = r[0.51]["db"] / rL[0.51]["db"]
            P(f"  P2 alpha {a_:.2e}: k <= 0.2 only: baryon delta / LCDM at z=0.51: k=0.05 {np.interp(0.05, kd, g):.3g}, k=0.1 {np.interp(0.1, kd, g):.3g}, k=0.2 {g[-1]:.3g}")
            PF[f"P2_{a_:.0e}"] = [float(np.interp(0.05, kd, g)), float(np.interp(0.1, kd, g)), float(g[-1])]
    J["postfreeze"] = PF

    # ---- verdict (frozen rule) ----
    P("\nT4 (record read; see README): U-F -- no committed lane fixes Omega_c from the field's constants (CFG428 one Bose field DEAD;"
      " CFG288/CFG360 amount free; CFG496 0/15 clues). U-0 -- identical to H2 by construction, 2 dark constants (= H2).")
    # strict frozen reading: the whole T1a-allowed SET (islands included) must sit below 1e-3
    bound_tight = bool(IA["+"]["max_not_excluded"] < 1e-3 and IA["-"]["max_not_excluded"] < 1e-3)
    P(f"  frozen-rule input: T1a max |alpha| not excluded = {max(IA['+']['max_not_excluded'], IA['-']['max_not_excluded']):.2e} -> bound below 1e-3: {bound_tight}"
      f" (contiguous-from-zero bound {max(amaxp, amaxm):.2e})")
    unified_pref = bool(prefers and not clash)
    if unified_pref:
        verdict = "UNIFIED VIABLE (U-A preferred by DESI and allowed by growth; constant count 3)"
    elif bound_tight and UR == "EXCLUDED":
        verdict = "NOT DECIDABLE (U-0 survives with the same dark-constant count as H2 and is observationally identical to it)"
    else:
        verdict = "NOT DECIDABLE (U-A bound looser than 1e-3 or U-R not excluded; see output)"
    P(f"\nLANE VERDICT (frozen rule): {verdict}")
    J["verdict"] = verdict
    finish(J, checks, T0)
    return 0 if all(checks.get(k) for k in ("K1", "K2", "K3", "K4", "K5")) else 1

def finish(J, checks, T0):
    J["checks"] = checks
    P(f"\ncontrols: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in sorted(checks.items())) + f"   [{time.time()-T0:.0f} s]")
    P("kappa = 1/2 FITTED; the cold energy's mass is still required; no dark-matter particle claimed; not theory closed.")
    open(os.path.join(HERE, f"cfg508{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    def conv(o):
        if isinstance(o, dict): return {str(k): conv(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [conv(v) for v in o]
        if isinstance(o, (np.floating,)): return float(o)
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, np.bool_): return bool(o)
        if isinstance(o, np.ndarray): return conv(o.tolist())
        return o
    json.dump(conv(J), open(os.path.join(HERE, f"cfg508_results{TAG}.json"), "w"), indent=1)

if __name__ == "__main__":
    sys.exit(main())
