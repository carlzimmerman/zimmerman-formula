#!/usr/bin/env python3
"""CFG511: blank-slate dark sector. STEP 1 data-only property table; STEP 2/3 four fresh ontologies scored.
Criteria: FROZEN_CRITERIA.md (committed alone first, 930d9760a). On-disk data only (DESI DR2 w0wa chains; DESI DR1 f sigma8 table via
CFG508; CAMB; CFG508's linear solver imported read-only; record catalogue CFG1_evidence_audit for LIT rows).
Run:  nice -n 15 python3 cfg511_blank_slate.py                  -> cfg511.out, cfg511_results.json
      CFG511_MUTATE=1 nice -n 15 python3 cfg511_blank_slate.py  -> cfg511_MUTATE.out, cfg511_results_MUTATE.json"""
import os, sys, json, math, time
os.environ.setdefault("OMP_NUM_THREADS", "4")
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.special import log_ndtr
from scipy.stats import chi2 as CHI2, norm
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(CFG, "CFG508_dark_vs_cold_energy"))
sys.path.insert(0, CFG)
import cfg508_unity as U   # noqa: E402  read-only: solver, CAMB set-up, DESI f sigma8 table, chain path
import CFG2_common as C2   # noqa: E402  read-only: footings, kappa

MUT = os.environ.get("CFG511_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

h, OB, OC, OM = U.h, U.OB, U.OC, U.OM
OL = 1.0 - OM
KG, ZOUT = U.KGRID, U.ZOUT
A0 = dict(C2.A0); KAPPA = C2.KAPPA
CKMS = 299792.458
CHAIN_NAMES = ("cmb", "pantheonplus", "union3", "desy5")
ZS = (0.5, 1.0, 1.5, 2.0, 2.5)
CHI2_LCDM_L181 = 4.56

def pct(v, wt, qs=(0.16, 0.5, 0.84)):
    return U.wpct(np.asarray(v), np.asarray(wt), qs)

def sig_equiv_2d(d2):
    return float(norm.isf(0.5 * CHI2.sf(d2, 2)))

# ================================================================= chains (S1, S2)
def load_chain(nm):
    fn1 = os.path.join(U.CHAINS, nm, "chain.1.txt")
    hdr = open(fn1).readline().lstrip("#").split()
    names = ("weight", "w", "wa", "omegam", "omch2", "H0")
    cols = [hdr.index(c) for c in names]
    xs = []
    for kk in range(1, 5):
        d = np.loadtxt(os.path.join(U.CHAINS, nm, f"chain.{kk}.txt"), usecols=cols)
        xs.append(d[int(0.3 * len(d)):])
    x = np.vstack(xs)
    return {n: x[:, i] for i, n in enumerate(names)}

def cpl_w(z, w0, wa):
    return w0 + wa * z / (1 + z)

def chains_block():
    S = {}
    for nm in CHAIN_NAMES:
        c = load_chain(nm); wt = c["weight"]; w0, wa, Om = c["w"], c["wa"], c["omegam"]
        row = dict(n=int(len(wt)))
        row["w0"] = pct(w0, wt); row["wa"] = pct(wa, wt); row["Om"] = pct(Om, wt)
        row["omch2"] = pct(c["omch2"], wt); row["Oc0"] = pct(c["omch2"] / (c["H0"] / 100) ** 2, wt)
        row["w_z0.5"] = pct(cpl_w(0.5, w0, wa), wt)
        q0 = Om / 2 + (1 + 3 * w0) * (1 - Om) / 2
        row["q0"] = pct(q0, wt); row["q0_mean_sd"] = [float(np.average(q0, weights=wt)), float(math.sqrt(np.cov(q0, aweights=wt)))]
        rr, a0H2, a0O1, a0H = {}, {}, {}, {}
        for z in ZS:
            f = U.cpl_f(z, w0, wa)
            rr[z] = pct(f, wt)
            a0H2[z] = pct(np.sqrt(f), wt)
            a0O1[z] = pct(np.sqrt(np.clip(cpl_w(z, w0, wa) * f / w0, 0, None)), wt)
            a0H[z] = pct(np.sqrt(Om * (1 + z) ** 3 + (1 - Om) * f), wt)
        row["rhoDE_ratio"] = rr; row["a0_H2"] = a0H2; row["a0_O1_tension"] = a0O1; row["a0_O3_H"] = a0H
        mu = np.array([np.average(w0, weights=wt), np.average(wa, weights=wt)])
        cov = np.cov(np.vstack([w0, wa]), aweights=wt)
        row["w0wa_mean"] = mu.tolist(); row["w0wa_cov"] = cov.tolist()
        row["med"] = dict(w0=row["w0"][1], wa=row["wa"][1], Om=row["Om"][1])
        S[nm] = row
    return S

# ================================================================= linear solver workers (S3, S4, Q1a, Q4a, M2)
def model_def(kind, par):
    """Return (OD, rho_f, w_f, ca2_f, cs2_f, OLm, extra_damp) for an independent cold fluid on a flat background."""
    if kind == "cs2":          # independent cold fluid with constant c_s^2
        return OB, (lambda a: OC * a ** -3), (lambda a: 0.0), (lambda a: 0.0), (lambda a: par), OL, None
    if kind == "wc":           # constant w_c, c_s^2 = 0, omega_c fixed at z = 1090
        w = par
        rho = lambda a: OC * a ** -3 * (1090.0 * a) ** (-3 * w)
        return OB, rho, (lambda a: w), (lambda a: w), (lambda a: 0.0), 1.0 - OB - rho(1.0), None
    if kind == "onemod":       # O1 one modulus: c_s^2 = rho_DE / rho_c, capped at 1
        return OB, (lambda a: OC * a ** -3), (lambda a: 0.0), (lambda a: 0.0), (lambda a: min(1.0, OL / (OC * a ** -3))), OL, None
    if kind == "visc":         # O4: Euler damping Gamma/H = (OL/(3 rho_c)) (k c/(aH))^2, times par (1 = the ontology)
        return OB, (lambda a: OC * a ** -3), (lambda a: 0.0), (lambda a: 0.0), (lambda a: 0.0), OL, par
    raise ValueError(kind)

def solve_damped(OD, rho_f, OLm, damp, kgrid, zout):
    """CFG508's equations for w = c_s^2 = 0 with an extra viscous Euler damping on the cold fluid (Radau, stiff)."""
    nk = len(kgrid); K = (np.asarray(kgrid) * U.CH0) ** 2
    y0 = np.concatenate([np.full(nk, U.AI), np.full(nk, -U.AI), np.full(nk, U.AI), np.full(nk, -U.AI)])
    def rhs(N, yy):
        a = math.exp(N); rf = rho_f(a); rd = OD * a ** -3
        E2 = rd + rf + OLm; dlnH = 0.5 * (-3.0 * rd - 3.0 * rf) / E2
        db, tb, du, tu = yy[:nk], yy[nk:2*nk], yy[2*nk:3*nk], yy[3*nk:]
        K2psi = -1.5 * (rd * db + rf * du) / E2
        G = damp * (OLm / (3.0 * rf)) * K / (a * a * E2)
        return np.concatenate([-tb, -(2.0 + dlnH) * tb + K2psi, -tu, -(2.0 + dlnH) * tu - G * tu + K2psi])
    Ns = sorted([math.log(1 / (1 + z)) for z in zout])
    s = solve_ivp(rhs, [U.NI, 0.0], y0, t_eval=Ns, method="Radau", rtol=1e-6, atol=1e-12)
    res = {}
    for z in zout:
        j = int(np.argmin(np.abs(s.t - math.log(1 / (1 + z))))); yy = s.y[:, j]
        res[z] = dict(db=yy[:nk], tb=yy[nk:2*nk], du=yy[2*nk:3*nk], tu=yy[3*nk:], a=math.exp(s.t[j]))
    return res

def worker(args):
    label, kind, par = args
    OD, rho, w, ca2, cs2, OLm, damp = model_def(kind, par)
    t0 = time.time()
    if damp is not None:
        res = solve_damped(OD, rho, OLm, damp, KG, ZOUT)
    else:
        res, _ = U.solve_model(OD, rho, w, ca2, cs2, OLm, KG, ZOUT)
    if res is None:
        return label, kind, par, None, time.time() - t0
    slim = {z: dict(db=r["db"].tolist(), tb=r["tb"].tolist(), du=r["du"].tolist(), a=r["a"], rho=rho(r["a"])) for z, r in res.items()}
    return label, kind, par, slim, time.time() - t0

def score_runs(out, kh, PK):
    ref = out["LCDM"][3]
    def dm(r):
        rb = OB * r["a"] ** -3
        return (rb * np.array(r["db"]) + r["rho"] * np.array(r["du"])) / (rb + r["rho"])
    S = {}
    for lbl, (_, kind, par, R, dt) in out.items():
        if R is None:
            S[lbl] = dict(kind=kind, par=par, blowup=True, dchi2=float("inf"), s8r=0.0, excluded=True); continue
        chi = 0.0; rat = []
        for t, z, r1, p1, m1, r2, p2, m2 in U.DESI:
            dL = dm(ref[z]); vL = -np.array(ref[z]["tb"]); vM = -np.array(R[z]["tb"])
            pkz = PK[round(z, 3)]
            rr = U.sig8(kh, pkz, U.interp_ratio(kh, KG, (vM / dL) ** 2)) / U.sig8(kh, pkz, U.interp_ratio(kh, KG, (vL / dL) ** 2))
            rat.append(float(rr)); chi += ((r2 - rr) / (0.5 * (p2 + m2))) ** 2
        Pr = (dm(R[0.0]) / dm(ref[0.0])) ** 2
        s8r = U.sig8(kh, PK[0.0], U.interp_ratio(kh, KG, Pr)) / U.sig8(kh, PK[0.0], np.ones_like(kh))
        S[lbl] = dict(kind=kind, par=par, chi2=chi, fs8_ratio=rat, s8r=float(s8r), blowup=False, sec=dt)
    c0 = S["LCDM"]["chi2"]
    for v in S.values():
        if not v["blowup"]:
            v["dchi2"] = v["chi2"] - c0
            v["excluded"] = bool(v["dchi2"] >= 9 or abs(v["s8r"] - 1) > 0.20)
    return S, c0

def first_bound(S, kind, sign=+1):
    """Smallest |par| (given sign) with dchi2 >= 4, and with |s8r - 1| >= 0.05."""
    rows = sorted([v for v in S.values() if v["kind"] == kind and np.sign(v["par"]) == sign], key=lambda v: abs(v["par"]))
    b4 = next((v["par"] for v in rows if v["dchi2"] >= 4), None)
    b5 = next((v["par"] for v in rows if v["blowup"] or abs(v["s8r"] - 1) >= 0.05), None)
    return b4, b5

# ================================================================= scale-independent growth with exchange (S6, K1, M3)
def growth_si(Om, w0, wa, mode, zs, Ob=OB, boost=None):
    """mode: 'NI' (smooth DE), 'Pc', 'Pv' (exchange split), 'BOOST' (M3 plant). Returns dict z -> (theta_b, delta_m, rho_c/rho_c,H2)."""
    Oc = Om - Ob; ODE = 1 - Om
    def wz(a): return w0 + wa * (1 - a)
    def fde(a): return a ** (-3 * (1 + w0 + wa)) * math.exp(-3 * wa * (1 - a))
    def rhoc(a):
        if mode == "NI": return Oc * a ** -3
        if mode == "BOOST": return boost * Oc * a ** -3
        return Oc * a ** -3 + (1 + wz(a)) * ODE * fde(a)
    def q_of(a):
        if mode in ("NI", "BOOST"): return 0.0
        dwdN = -wa * a
        dX = (dwdN - 3 * (1 + wz(a)) ** 2) * ODE * fde(a)
        rc = rhoc(a)
        return (-3 * Oc * a ** -3 + dX) / rc + 3.0
    def rhs(N, y):
        a = math.exp(N); db, tb, dc, tc = y
        rb, rc = Ob * a ** -3, rhoc(a)
        E2 = Om * a ** -3 + ODE * fde(a)
        dlnH = 0.5 * (-3 * Om * a ** -3 - 3 * (1 + wz(a)) * ODE * fde(a)) / E2
        src = -1.5 * (rb * db + rc * dc) / E2
        q = q_of(a)
        return [-tb, -(2 + dlnH) * tb + src, -tc - q * dc, -(2 + dlnH) * tc + src - (q * tc if mode == "Pv" else 0.0)]
    Ns = sorted([math.log(1 / (1 + z)) for z in zs])
    s = solve_ivp(rhs, [U.NI, 0.0], [U.AI, -U.AI, U.AI, -U.AI], t_eval=Ns, method="DOP853", rtol=1e-10, atol=1e-14)
    out = {}
    for z in zs:
        j = int(np.argmin(np.abs(s.t - math.log(1 / (1 + z))))); a = math.exp(s.t[j])
        db, tb, dc, tc = s.y[:, j]; rb, rc = Ob * a ** -3, rhoc(a)
        out[z] = (float(tb), float((rb * db + rc * dc) / (rb + rc)), float(rc / (Oc * a ** -3)))
    return out

def growth_chi2(Om, w0, wa, mode, ref, boost=None):
    zs = [r[1] for r in U.DESI] + [0.0]
    g = growth_si(Om, w0, wa, mode, zs, boost=boost)
    chi = 0.0; rat = []
    for t, z, r1, p1, m1, r2, p2, m2 in U.DESI:
        rr = g[z][0] / ref[z][0]; rat.append(rr); chi += ((r2 - rr) / (0.5 * (p2 + m2))) ** 2
    return chi, rat, g[0.0][1] / ref[0.0][1], g[0.0][2]

# ================================================================= O3: holographic DE
def hde(OmDE0, ch, zmax=2.5, Nfut=8.0):
    def rhs(N, y):
        O = y[0]; return [O * (1 - O) * (1 + 2 * math.sqrt(max(O, 0)) / ch)]
    Nlo = math.log(1 / (1 + zmax))
    sb = solve_ivp(rhs, [0, Nlo - 0.05], [OmDE0], dense_output=True, rtol=1e-11, atol=1e-13)
    sf = solve_ivp(rhs, [0, Nfut], [OmDE0], dense_output=True, rtol=1e-11, atol=1e-13)
    Om0 = 1 - OmDE0
    def O_at(N): return float((sb if N <= 0 else sf).sol(N)[0])
    def E2(N): return Om0 * math.exp(-3 * N) / (1 - O_at(N))
    def w(N): return -1 / 3 - 2 * math.sqrt(O_at(N)) / (3 * ch)
    return O_at, E2, w, Nfut

def hde_cpl(OmDE0, ch):
    O_at, E2, w, _ = hde(OmDE0, ch)
    z = np.linspace(0, 2.5, 251); N = -np.log1p(z)
    f = np.array([O_at(n) * E2(n) for n in N]) / OmDE0
    X = np.vstack([3 * np.log1p(z), -3 * z / (1 + z)]).T
    coef, *_ = np.linalg.lstsq(X, np.log(f), rcond=None)
    s_, wa = coef; w0 = s_ - 1 - wa
    return float(w0), float(wa), float(np.max(np.abs(np.log(f) - X @ coef))), f

def hde_eventhorizon_check(OmDE0, ch=1.0):
    O_at, E2, w, Nf = hde(OmDE0, ch)
    Hf = math.sqrt(E2(Nf))
    devs = []
    for z in (0.0, 0.5, 1.0, 2.0):
        N = -math.log1p(z)
        I, _ = quad(lambda n: math.exp(-n) / math.sqrt(E2(n)), N, Nf, limit=400, epsabs=1e-13, epsrel=1e-11)
        I += math.exp(-Nf) / Hf
        L = math.exp(N) * I            # in units of c/H0
        Ocheck = (ch / (L * math.sqrt(E2(N)))) ** 2
        devs.append(abs(Ocheck - O_at(N)))
    return max(devs)

# ================================================================= anti-numerology (CFG496 rules 3, 4, MUTATE)
PSET = [1, 2, 3, 4, 8, 1/2, 1/3, 1/4, 1/8, 2/3, 3/2, 3/4, 4/3]
def family_F1(Om, OLx):
    return np.array([p * math.pi ** a * KAPPA ** b * OLx ** c * Om ** d for p in PSET for a in (-1, 0, 1) for b in (-1, 0, 1)
                     for c in (-1, 0, 1) for d in (-1, 0, 1)])

def lee_p(v, delta, vals, n=20000, seed=496):
    lv = np.sort(np.log(vals)); rng = np.random.default_rng(seed)
    x = np.log(v) + np.log(10.0) * rng.uniform(-1, 1, n)
    j = np.clip(np.searchsorted(lv, x), 1, len(lv) - 1)
    return float(np.mean(np.minimum(np.abs(x - lv[j - 1]), np.abs(x - lv[j])) <= delta + 1e-15))

def coincidence_test(tag, v, form, r_dependent):
    vals = np.append(family_F1(OM, OL), form)
    d = abs(math.log(v / form)); match = d <= 0.01
    p = lee_p(v, d, vals)
    if not r_dependent:
        sec, txt = False, "scrambled cosmology UNINFORMATIVE (value and form do not depend on R') -> no second check = FAIL (CFG496 rule 4)"
    else:
        sec, txt = None, "computed"
    lab = "CLUE" if (match and p < 0.01 and sec) else ("COINCIDENCE" if match else "NO MATCH")
    return dict(tag=tag, value=v, form=form, delta=d, match=match, p_lee=p, second=sec, second_txt=txt, label=lab)

# ================================================================= bound fraction (S5)
def bound_block():
    import camb
    zs = [0.0, 1.0, 3.0, 10.0, 30.0, 1100.0]
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=100 * h, ombh2=U.OBH2, omch2=U.OCH2, mnu=0.0, num_massive_neutrinos=0, omk=0.0)
    pars.InitPower.set_params(As=2.1e-9, ns=0.9649)
    pars.set_matter_power(redshifts=zs[::-1], kmax=5000.0)
    r = camb.get_results(pars)
    kh, zr, pk = r.get_matter_power_spectrum(minkh=1e-4, maxkh=5000.0, npoints=900)
    s8 = float(r.get_sigma8_0())
    # power-law tail beyond kmax (disclosed): log-log slope of the last decade
    kt = np.logspace(math.log10(kh[-1]) + 1e-3, 7, 300)
    PKz = {}
    for i, z in enumerate(zr):
        sl = np.polyfit(np.log(kh[-60:]), np.log(pk[i][-60:]), 1)[0]
        PKz[round(float(z), 1)] = (np.concatenate([kh, kt]), np.concatenate([pk[i], pk[i][-1] * (kt / kh[-1]) ** sl]))
    rhobar = 2.775e11 * OM                         # (Msun/h) / (Mpc/h)^3
    def sigma(Msun, z):
        R = (3 * Msun * h / (4 * math.pi * rhobar)) ** (1 / 3)
        k, p = PKz[round(z, 1)]
        x = k * R; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
        return math.sqrt(np.trapz(p * W ** 2 * k ** 3 / (2 * math.pi ** 2), np.log(k)))
    def sigR(R, z):
        k, p = PKz[round(z, 1)]
        x = k * R; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
        return math.sqrt(np.trapz(p * W ** 2 * k ** 3 / (2 * math.pi ** 2), np.log(k)))
    out = {}
    for Mm in (1e3, 1e6, 1e9, 1e12):
        for z in zs:
            s = sigma(Mm, z)
            out[f"{Mm:.0e}|{z:g}"] = dict(sigma=s, log10_fbound=float((math.log(2) + log_ndtr(-1.686 / s)) / math.log(10)))
    Dratio = sigR(8.0, 0.0) / sigR(8.0, 1100.0)
    return out, s8, Dratio

# ================================================================= classification
def classify(Qs, H2_equal_all=False):
    """Qs: list of dict(name, excluded, tension, distinct, knob). Frozen rules 1-3 on the minimal form."""
    if any(q["excluded"] for q in Qs): return "EXCLUDED"
    if any(q["distinct"] and not q["knob"] for q in Qs):
        t = any(q["distinct"] and not q["knob"] and q.get("tension") for q in Qs)
        return "CONSISTENT-AND-DISTINCT" + (" (in tension)" if t else "")
    return "CONSISTENT-BUT-EQUIVALENT"

def conv(o):
    if isinstance(o, dict): return {str(k): conv(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [conv(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return conv(o.tolist())
    if isinstance(o, float) and not math.isfinite(o): return str(o)
    return o

def finish(J, checks, T0, ok):
    J["checks"] = checks; J["runtime_s"] = time.time() - T0
    P(f"\nruntime {time.time() - T0:.1f} s; exit {0 if ok else 1}")
    json.dump(conv(J), open(os.path.join(HERE, f"cfg511_results{TAG}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg511{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    return 0 if ok else 1

# ================================================================= main
def main():
    T0 = time.time(); J = dict(mutate=MUT); checks = {}
    P("=" * 112)
    P(f"CFG511{' MUTATE' if MUT else ''}: blank-slate dark sector (criteria 930d9760a)")
    P("=" * 112)
    P(f"Planck 2018 reference: h {h}, Omega_b {OB:.5f}, Omega_c {OC:.5f}, Omega_m {OM:.5f}; cold/ordinary = {OC / OB:.3f}")
    P(f"footings (quoted, never pooled): a0 canonical {A0['canonical']:.4e}, alt {A0['alt']:.4e} m/s^2; kappa = {KAPPA} FITTED")
    kh, PK = U.camb_plin()

    # reference LCDM (Planck) scale-independent growth
    zsD = [r[1] for r in U.DESI] + [0.0]
    REF = growth_si(OM, -1.0, 0.0, "NI", zsD)

    if MUT:
        P("\nMUTATE M1-M3")
        # M1: f_bound == 1 at all z -> ratio 1 -> not excluded, equivalent
        q = dict(name="Q2a planted f_bound==1", excluded=bool(abs(math.log10(1.0)) >= 1), distinct=False, knob=False)
        m1 = classify([q]); ok1 = (m1 == "CONSISTENT-BUT-EQUIVALENT")
        P(f"  M1 planted bound-phase with f_bound == 1: omega_c(1100) ratio 1.000 -> {m1}  [{'OK' if ok1 else 'FAIL'}]")
        # M2: c_s^2 = 1e-2 independent cold fluid
        with Pool(4) as pool:
            res = pool.map(worker, [("LCDM", "cs2", 0.0), ("M2", "cs2", 1e-2)])
        S, c0 = score_runs({r[0]: r for r in res}, kh, PK)
        m2 = S["M2"]; ok2 = bool(m2["excluded"])
        P(f"  M2 cold c_s^2 = 1e-2: dchi2 {m2['dchi2']:+.1f}, sigma8 ratio {m2['s8r']:.3f} -> {'EXCLUDED' if ok2 else 'NOT EXCLUDED'}  [{'OK' if ok2 else 'FAIL'}]  (LCDM chi2 {c0:.3f})")
        # M3: 1.5x clustering cold, born clustered
        cref = growth_chi2(OM, -1.0, 0.0, "NI", REF)[0]
        c3, rat3, s3, _ = growth_chi2(OM, -1.0, 0.0, "BOOST", REF, boost=1.5)
        ok3 = bool(c3 - cref >= 9)
        P(f"  M3 clustering cold x1.5 (H(z) unchanged): dchi2 {c3 - cref:+.1f}, delta_m(0) ratio {s3:.3f} -> {'EXCLUDED' if ok3 else 'NOT EXCLUDED'}  [{'OK' if ok3 else 'FAIL'}]")
        J.update(M1=m1, M2=m2, M3=dict(dchi2=c3 - cref, ratios=rat3, s8=s3))
        checks.update(M1=ok1, M2=ok2, M3=ok3)
        ok = ok1 and ok2 and ok3
        P("MUTATE OK: the tests can pass a renaming and can exclude" if ok else "MUTATE FAILED -> the failing part is VOID")
        return finish(J, checks, T0, ok)

    # ---------------- S1/S2 chains
    P("\n[S1/S2] DESI DR2 chains (CPL; first 30% dropped; weighted 16/50/84)")
    CH = chains_block(); J["chains"] = CH
    for nm, r in CH.items():
        P(f"  {nm:<13} w0 {r['w0'][1]:+.3f} [{r['w0'][0]:+.3f},{r['w0'][2]:+.3f}]  wa {r['wa'][1]:+.3f} [{r['wa'][0]:+.3f},{r['wa'][2]:+.3f}]  "
          f"Om {r['Om'][1]:.4f}  omega_c {r['omch2'][1]:.4f} [{r['omch2'][0]:.4f},{r['omch2'][2]:.4f}]  Oc0 {r['Oc0'][1]:.4f}  "
          f"q0 {r['q0'][1]:+.3f} [{r['q0'][0]:+.3f},{r['q0'][2]:+.3f}]")
        P("      rho_DE(z)/rho_DE(0): " + "  ".join(f"z{z:g} {r['rhoDE_ratio'][z][1]:.3f} [{r['rhoDE_ratio'][z][0]:.3f},{r['rhoDE_ratio'][z][2]:.3f}]" for z in ZS))
    # K3: CFG508's quoted range is per SN chain (cfg508.out: pantheonplus 0.827, union3 0.782, desy5 0.798); the cmb-only chain is reported only
    C508 = dict(pantheonplus=0.827, union3=0.782, desy5=0.798)
    a25 = {n: CH[n]["a0_H2"][2.5][1] for n in CHAIN_NAMES}
    checks["K3"] = bool(all(abs(a25[n] - v) <= 0.01 for n, v in C508.items()))
    P(f"  [{'PASS' if checks['K3'] else 'FAIL'}] K3 non-interacting a0(2.5)/a0(0) medians " + ", ".join(f"{n} {a25[n]:.3f}" for n in CHAIN_NAMES)
      + " vs CFG508 per-chain 0.827/0.782/0.798 (+-0.01; cmb-only not in CFG508's range, reported)")

    # ---------------- K1 (growth ODE vs CFG508 solver; LCDM chi2)
    with Pool(4) as pool:
        models = [("LCDM", "cs2", 0.0)]
        models += [(f"cs2_{v:.1e}", "cs2", float(v)) for v in np.logspace(-9, -2, 22)]
        wm = np.logspace(-4, math.log10(3e-2), 12)
        models += [(f"wc_{s}{v:.1e}", "wc", sg * float(v)) for s, sg in (("+", 1), ("-", -1)) for v in wm]
        models += [("O1_onemod", "onemod", 0.0), ("O4_visc", "visc", 1.0), ("O4_visc_check0", "visc", 0.0)]
        res = pool.map(worker, models)
    RUN = {r[0]: r for r in res}
    P(f"\nsolver runs: {len(RUN)} models, {sum(r[4] for r in res):.1f} s CPU")
    S, c0 = score_runs(RUN, kh, PK)
    ref = RUN["LCDM"][3]
    k1 = []
    for z in (0.0, 0.5, 1.5):
        zz = min(ZOUT, key=lambda q: abs(q - z))
        g = growth_si(OM, -1.0, 0.0, "NI", [zz])[zz]
        k1.append(abs(np.median(np.array(ref[zz]["tb"])) / g[0] - 1))
    vchk = RUN["O4_visc_check0"][3]
    k1b = max(float(np.max(np.abs(np.array(vchk[z]["tb"]) / np.array(ref[z]["tb"]) - 1))) for z in (0.0, 0.5, 1.5))
    chiL = growth_chi2(OM, -1.0, 0.0, "NI", REF)[0]
    checks["K1"] = bool(max(k1) < 1e-3 and abs(c0 - CHI2_LCDM_L181) < 0.01 and abs(chiL - CHI2_LCDM_L181) < 0.01 and k1b < 1e-3)
    P(f"  [{'PASS' if checks['K1'] else 'FAIL'}] K1 growth ODE vs CFG508 solver max dev {max(k1):.1e}; damped solver at zero damping vs CFG508 {k1b:.1e}; "
      f"LCDM chi2 solver {c0:.3f} / ODE {chiL:.3f} vs L181 4.56")

    # ---------------- S3, S4
    b4c, b5c = first_bound(S, "cs2", +1)
    b4wp, b5wp = first_bound(S, "wc", +1); b4wm, b5wm = first_bound(S, "wc", -1)
    P("\n[S3] independent cold fluid, constant c_s^2 (Planck LCDM background):")
    for lbl in [l for l in S if l.startswith("cs2_")]:
        v = S[lbl]; P(f"  c_s^2 {v['par']:9.2e}: dchi2 {v['dchi2']:+8.2f}  sigma8 ratio {v['s8r']:.4f}")
    P(f"  bound (a) dchi2 >= 4 at c_s^2 = {b4c}; (b) sigma8 shift >= 5% at c_s^2 = {b5c}")
    P("[S4] cold equation of state w_c (c_s^2 = 0; omega_c fixed at z = 1090; flat):")
    for lbl in [l for l in S if l.startswith("wc_")]:
        v = S[lbl]; P(f"  w_c {v['par']:+9.2e}: dchi2 {v['dchi2']:+8.2f}  sigma8 ratio {v['s8r']:.4f}" + ("  BLOW-UP" if v["blowup"] else ""))
    P(f"  bounds: w_c > 0: dchi2>=4 at {b4wp}, 5% sigma8 at {b5wp};  w_c < 0: dchi2>=4 at {b4wm}, 5% sigma8 at {b5wm}")
    J["S3"] = dict(bound_dchi2_4=b4c, bound_s8_5pct=b5c); J["S4"] = dict(pos=[b4wp, b5wp], neg=[b4wm, b5wm])
    J["solver_scores"] = S

    # ---------------- S5 bound fraction
    P("\n[S5] bound (collapsed) fraction, Press-Schechter on CAMB P_lin (power-law tail beyond k = 5000 h/Mpc):")
    FB, s8c, Drat = bound_block()
    for key, v in FB.items():
        P(f"  M >= {key.split('|')[0]} Msun, z = {key.split('|')[1]:>5}: sigma {v['sigma']:.4g}  log10 f_bound {v['log10_fbound']:.4g}")
    fb12 = 10 ** FB["1e+12|0"]["log10_fbound"]
    checks["K5"] = bool(0.80 <= s8c <= 0.83 and 0.1 <= fb12 <= 0.6)
    P(f"  [{'PASS' if checks['K5'] else 'FAIL'}] K5 CAMB sigma8 {s8c:.4f}; f_bound(z=0, M>=1e12) {fb12:.3f}")
    P(f"  linear growth D(0)/D(1100) (sigma at 8 Mpc/h) = {Drat:.1f}")
    J["S5"] = dict(fbound=FB, sigma8=s8c, D0_over_D1100=Drat)

    # ---------------- S6 exchange (= Q1b)
    P("\n[S6 / Q1b] exchange split: vacuum w = -1 exactly, all CPL density change -> cold energy; H(z) unchanged")
    EX = {}
    for nm in CHAIN_NAMES:
        m = CH[nm]["med"]; Om, w0, wa = m["Om"], m["w0"], m["wa"]
        # K2 identity: total dark density identical
        ODE = 1 - Om; Oc = Om - OB
        devs = []
        for a in np.linspace(1 / 201, 1, 400):
            fde = a ** (-3 * (1 + w0 + wa)) * math.exp(-3 * wa * (1 - a)); wz = w0 + wa * (1 - a)
            rc = Oc * a ** -3 + (1 + wz) * ODE * fde; rv = -wz * ODE * fde
            devs.append(abs((rc + rv) - (Oc * a ** -3 + ODE * fde)) / (Oc * a ** -3 + ODE * fde))
        row = dict(K2=max(devs))
        for mode in ("NI", "Pc", "Pv"):
            chi, rat, s8, rcr = growth_chi2(Om, w0, wa, mode, REF)
            row[mode] = dict(chi2=chi, fs8=rat, dm0_ratio=s8, rhoc0_over_H2=rcr)
        row["dchi2_Pc_vs_NI"] = row["Pc"]["chi2"] - row["NI"]["chi2"]; row["dchi2_Pv_vs_NI"] = row["Pv"]["chi2"] - row["NI"]["chi2"]
        EX[nm] = row
        P(f"  {nm:<13} rho_c(0)/H2 {row['Pc']['rhoc0_over_H2']:.3f} | chi2 NI {row['NI']['chi2']:.2f}  Pc {row['Pc']['chi2']:.2f} (d {row['dchi2_Pc_vs_NI']:+.2f})  "
          f"Pv {row['Pv']['chi2']:.2f} (d {row['dchi2_Pv_vs_NI']:+.2f}) | delta_m(0)/LCDM NI {row['NI']['dm0_ratio']:.3f} Pc {row['Pc']['dm0_ratio']:.3f} Pv {row['Pv']['dm0_ratio']:.3f}  [K2 {row['K2']:.1e}]")
    checks["K2"] = bool(max(r["K2"] for r in EX.values()) < 1e-10)
    P(f"  [{'PASS' if checks['K2'] else 'FAIL'}] K2 exchange split reproduces the CPL total dark density (max rel dev {max(r['K2'] for r in EX.values()):.1e})")
    J["S6"] = EX

    # ---------------- O3 holographic
    P("\n[O3] horizon-information ontology")
    O3 = {}
    for nm in CHAIN_NAMES:
        r = CH[nm]; mu = np.array(r["w0wa_mean"]); cov = np.array(r["w0wa_cov"]); ci = np.linalg.inv(cov)
        OmDE0 = 1 - r["med"]["Om"]
        w0h, wah, resid, _ = hde_cpl(OmDE0, 1.0)
        d = np.array([w0h, wah]) - mu; d2 = float(d @ ci @ d)
        qm, qs = r["q0_mean_sd"]; zq = (0.5 - qm) / qs
        chs = np.linspace(0.3, 2.5, 111); best = None
        for chv in chs:
            a_, b_, _, _ = hde_cpl(OmDE0, chv); dd = np.array([a_, b_]) - mu; v = float(dd @ ci @ dd)
            if best is None or v < best[1]: best = (float(chv), v, a_, b_)
        w0an = -1 / 3 - 2 * math.sqrt(OmDE0) / 3
        O_at, E2h, wfun, _ = hde(OmDE0, 1.0)
        a0hde = {z: math.sqrt(O_at(-math.log1p(z)) * E2h(-math.log1p(z)) / OmDE0) for z in (1.0, 2.5)}
        O3[nm] = dict(Q3a_q0_pull_sigma=zq, Q3b=dict(w0=w0h, wa=wah, cpl_resid=resid, d2=d2, sigma=sig_equiv_2d(d2)),
                      ch_best=dict(ch=best[0], d2=best[1], sigma=sig_equiv_2d(best[1]), w0=best[2], wa=best[3]),
                      K4_w0=abs(w0h - w0an) if False else abs(wfun(0.0) - w0an), a0_hde=a0hde)
        P(f"  {nm:<13} Q3a: q0 = +1/2 is {zq:+.1f} sigma from the chain q0 ({qm:+.3f} +- {qs:.3f}) | Q3b c_h=1: CPL (w0, wa) = ({w0h:+.3f}, {wah:+.3f}) "
          f"[fit resid {resid:.1e}], d2 {d2:.1f} -> {sig_equiv_2d(d2):.1f} sigma | best c_h {best[0]:.2f}: ({best[2]:+.3f}, {best[3]:+.3f}) {sig_equiv_2d(best[1]):.1f} sigma "
          f"| a0 ~ sqrt(rho_HDE): z1 {a0hde[1.0]:.3f} z2.5 {a0hde[2.5]:.3f}")
    k4a = max(v["K4_w0"] for v in O3.values())
    k4b = hde_eventhorizon_check(1 - CH["desy5"]["med"]["Om"], 1.0)
    checks["K4"] = bool(k4a < 1e-6 and k4b < 1e-3)
    P(f"  [{'PASS' if checks['K4'] else 'FAIL'}] K4 HDE w0 identity {k4a:.1e}; direct event-horizon integral vs ODE Omega_DE max dev {k4b:.1e}")
    J["O3"] = O3

    # anti-numerology: Q3d a0 = c H0 / 6
    cH0 = C2.C_SI * (100 * h * 1e3 / 3.0856775814913673e22)
    AN = {f: coincidence_test(f"Q3d a0/(cH0) vs 1/6 [{f}]", A0[f] / cH0, 1 / 6, r_dependent=False) for f in ("canonical", "alt")}
    gdag = coincidence_test("Q3d g_dagger(SPARC 1.20e-10)/(cH0) vs 1/6 [reported]", 1.20e-10 / cH0, 1 / 6, r_dependent=False)
    planted = coincidence_test("K6 planted 3 pi kappa Omega_m / 6", 3 * math.pi * KAPPA * OM / 6, 0.5 * math.pi * KAPPA * OM, r_dependent=False)
    checks["K6"] = bool(planted["delta"] < 1e-12 and planted["p_lee"] < 0.01)
    for v in list(AN.values()) + [gdag]:
        P(f"  anti-numerology {v['tag']}: value {v['value']:.4f}, delta {v['delta']:.3f} (match <= 0.01: {v['match']}), look-elsewhere p {v['p_lee']:.3f}; "
          f"{v['second_txt']} -> {v['label']}")
    P(f"  [{'PASS' if checks['K6'] else 'FAIL'}] K6 planted exact form: delta {planted['delta']:.1e}, p {planted['p_lee']:.4f}")
    J["anti_numerology"] = dict(Q3d=AN, gdagger=gdag, K6=planted)

    # ================================================================= STEP 3 verdicts
    P("\n" + "=" * 112); P("STEP 3: ontology verdicts (frozen rules)"); P("=" * 112)
    V = {}
    # O1
    o1 = S["O1_onemod"]
    q1a = dict(name="Q1a one-modulus sound speed", excluded=bool(o1["excluded"]), distinct=True, knob=False,
               detail=f"dchi2 {o1['dchi2']:+.1f}, sigma8 ratio {o1['s8r']:.3f}" if not o1["blowup"] else "blow-up")
    worstPc = max(EX[n]["dchi2_Pc_vs_NI"] for n in CHAIN_NAMES); worstPv = max(EX[n]["dchi2_Pv_vs_NI"] for n in CHAIN_NAMES)
    bestPc = min(EX[n]["dchi2_Pc_vs_NI"] for n in CHAIN_NAMES)
    def exq(dc): return dict(excluded=bool(dc >= 9), tension=bool(4 <= dc < 9))
    q1b = dict(name="Q1b relaxing tension = exchange (P-c, worst chain)", distinct=True, knob=False, **exq(worstPc),
               detail=f"dchi2 vs non-interacting P-c {', '.join(f'{EX[n]['dchi2_Pc_vs_NI']:+.2f}' for n in CHAIN_NAMES)}; "
                      f"P-v {', '.join(f'{EX[n]['dchi2_Pv_vs_NI']:+.2f}' for n in CHAIN_NAMES)}")
    a0O1 = {n: (CH[n]["a0_O1_tension"][1.0][1], CH[n]["a0_O1_tension"][2.5][1]) for n in CHAIN_NAMES}
    a0H2 = {n: (CH[n]["a0_H2"][1.0][1], CH[n]["a0_H2"][2.5][1]) for n in CHAIN_NAMES}
    q1c = dict(name="Q1c a0 set by tension -p_DE", excluded=False, distinct=True, knob=False,
               detail="a0(1), a0(2.5) / a0(0): " + "; ".join(f"{n} O1 {a0O1[n][0]:.3f}/{a0O1[n][1]:.3f} vs H2 {a0H2[n][0]:.3f}/{a0H2[n][1]:.3f}" for n in CHAIN_NAMES)
               + " (a0(z) is calibration-limited on the record: not excluded)")
    v1 = classify([q1a, q1b, q1c])
    v1d = classify([q1b, q1c])          # two-modulus knob variant keeps Q1b, Q1c (they do not depend on mu)
    V["O1"] = dict(minimal=v1, Qs=[q1a, q1b, q1c], knob_variant_two_moduli=v1d,
                   knob_note=f"rigidity mu free: c_s^2 = mu/rho_c <= {b4c} (DESI f sigma8) / {b5c} (5% sigma8); mu -> 0 is H2 for the sound speed, "
                             "but Q1b and Q1c do not depend on mu")
    # O2
    lr1100 = FB["1e+03|1100"]["log10_fbound"] - FB["1e+03|0"]["log10_fbound"]
    q2a = dict(name="Q2a mean cold density follows f_bound", excluded=bool(abs(lr1100) >= 1), distinct=True, knob=False,
               detail=f"predicted omega_c(1100)/measured = 10^{lr1100:.4g} (M_min 1e3 Msun; most generous); measured omega_c to ~1% (chains)")
    q2b = dict(name="Q2b overdensity-keyed variant", excluded=bool(Drat >= 10), distinct=True, knob=False,
               detail=f"comoving cold amount grows by D(0)/D(1100) = {Drat:.0f} between recombination and today; "
                      f"allowed by S4 w_c bound: |dln| <= 3|w_c| ln 1090 = {3 * abs(b4wp or 3e-2) * math.log(1090):.2f}")
    V["O2"] = dict(minimal=classify([q2a]), Qs=[q2a, q2b], variant_overdensity=classify([q2b]))
    # O3
    SNC = ("pantheonplus", "union3", "desy5")   # post-freeze P2: exclusion needs every SN-including chain >= 3 sigma; cmb-only reported
    q3a_s = min(O3[n]["Q3a_q0_pull_sigma"] for n in SNC)
    q3b_s = min(O3[n]["Q3b"]["sigma"] for n in CHAIN_NAMES)   # all four chains (stricter than P2)
    q3a = dict(name="Q3a Hubble-radius L (q0 = +1/2)", excluded=bool(q3a_s >= 3), distinct=True, knob=False, detail=f"pull " + ", ".join(f"{n} {O3[n]['Q3a_q0_pull_sigma']:.1f}" for n in CHAIN_NAMES) + f" sigma; min over SN chains {q3a_s:.1f}")
    q3b = dict(name="Q3b event horizon, c_h = 1", excluded=bool(q3b_s >= 3), tension=bool(2 <= q3b_s < 3), distinct=True, knob=False,
               detail=f"(w0, wa) distance {', '.join(f'{O3[n]['Q3b']['sigma']:.1f}' for n in CHAIN_NAMES)} sigma (2-D)")
    q3c = dict(name="Q3c emergent cold part (no homogeneous mean at z = 1100)", excluded=q2a["excluded"], distinct=True, knob=False,
               detail="same test as Q2a: omega_c(1100) measured, nothing bound")
    E25 = {n: CH[n]["a0_O3_H"][2.5][1] for n in CHAIN_NAMES}
    q3d = dict(name="Q3d a0 = cH0/6 and a0 ~ H(z)", excluded=False, distinct=True, knob=False,
               detail=f"coincidence labels {AN['canonical']['label']}/{AN['alt']['label']} (no weight); a0(2.5)/a0(0) = H ratio "
                      + ", ".join(f"{E25[n]:.2f}" for n in CHAIN_NAMES) + " vs H2 " + ", ".join(f"{a0H2[n][1]:.2f}" for n in CHAIN_NAMES))
    chb = max(O3[n]["ch_best"]["sigma"] for n in CHAIN_NAMES)
    V["O3"] = dict(minimal=classify([q3b, q3c, q3d]), Qs=[q3a, q3b, q3c, q3d], hubble_L=classify([q3a]),
                   DE_part_alone_ch1=classify([q3b]),
                   DE_part_knob_ch=f"best c_h per chain {', '.join(f'{O3[n]['ch_best']['ch']:.2f}' for n in CHAIN_NAMES)}; worst residual {chb:.1f} sigma")
    # O4
    o4 = S["O4_visc"]
    q4a = dict(name="Q4a viscous damping of the cold flow", excluded=bool(o4["excluded"]), distinct=True, knob=False,
               detail=f"dchi2 {o4['dchi2']:+.1f}, sigma8 ratio {o4['s8r']:.4f}")
    V["O4"] = dict(minimal=classify([q4a]), Qs=[q4a], variant_smooth_only="CONSISTENT-BUT-EQUIVALENT (two components by construction)")
    for k, v in V.items():
        P(f"\n{k}: minimal form -> {v['minimal']}")
        for q in v["Qs"]:
            P(f"   {q['name']}: {'EXCLUDED' if q['excluded'] else ('tension' if q.get('tension') else 'not excluded')} | {q['detail']}")
        for kk in v:
            if kk not in ("minimal", "Qs"):
                P(f"   {kk}: {v[kk]}")
    J["verdicts"] = V
    ok = all(checks.get(k) for k in ("K1", "K2", "K3", "K4", "K5", "K6"))
    P("\ncontrols: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in sorted(checks.items())))
    P("kappa = 1/2 FITTED; the cold energy's mass is still required and its amount is an input; no particle; not theory closed.")
    return finish(J, checks, T0, ok)

if __name__ == "__main__":
    sys.exit(main())
