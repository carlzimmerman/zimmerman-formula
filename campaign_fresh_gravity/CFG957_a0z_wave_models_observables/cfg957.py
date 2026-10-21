"""CFG957: the owner's idea (2026-10-21) -- a0(z) oscillates like a wave (larger early, on the way down now).
Physical models (Part 1) and every observable other than the expansion bound (Part 2).  Criteria: FROZEN_CRITERIA.md
(8e884c9a2b), committed alone before this script.  CFG956 owns the expansion-data bound; nothing here recomputes it.

Modes (env CFG957_MODE): K (controls K1-K5) -> cfg957_K.{out,json}; MAIN -> cfg957.{out,json};
MUTATE (M-a..M-d) -> cfg957_MUTATE.{out,json}.

Inputs (read only): CFG689's cfg689.json (primary best fit + band quantiles; its script is never imported),
FIGURE_SUMMARY_2026-10-21/plotted_numbers.json (the panel-(d) points), the points' source files (K1), CFG223's
cfg223_results.json (rival curve, K5).  kappa = 1/2 is FITTED; footings 9.3603e-11 / 1.1312e-10 m s^-2 never pooled;
cold energy is not a particle species; not a closed theory; nothing here says the data favour the framework.

Run: OMP_NUM_THREADS=1 nice -n 10 env CFG957_MODE=K python3 cfg957.py   (then MAIN, then MUTATE; each < 1 GB, minutes)
"""
import csv
import glob
import json
import math
import os
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.integrate import solve_ivp, quad

TRAPZ = getattr(np, "trapezoid", None) or np.trapz

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
ROOT = os.path.dirname(CFG)
MODE = os.environ.get("CFG957_MODE", "MAIN").upper()
T0 = time.time()
OUT, CHECKS = [], []


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


def check(name, ok, info=""):
    CHECKS.append((name, bool(ok)))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}  {info}")


# ============================================================================== inputs
D689 = glob.glob(os.path.join(CFG, "CFG689_*"))[0]
J689 = json.load(open(os.path.join(D689, "cfg689.json")))
PB = J689["BAO+SN"]["P2"]["pbest"]
OM = PB[7] + PB[8]
WK = PB[6]
W0 = PB[0]
OMR = 2.4728e-5 * (1 + 0.2271 * 3.044)
H2_0 = OM + OMR + WK + W0
h = math.sqrt(H2_0)
OL = W0 / H2_0
GYR_PER_H100 = 9.777922216807891          # 1/(100 km/s/Mpc) in Gyr
H0_PER_YR = h * 1.0227121650537077e-10   # H0 in yr^-1
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
C_LIGHT = 2.99792458e8
H0_SI = h * 1e5 / 3.0856775814913673e22
BANDZ = {1.0: J689["BAO+SN"]["P1"]["1.0"]["sqrtX_q"], 1.2: J689["BAO+SN"]["P1"]["1.2"]["sqrtX_q"],
         1.5: J689["BAO+SN"]["P1"]["1.5"]["sqrtX_q"], 2.0: J689["BAO+SN"]["P6"]["2.0"]["sqrtX_q"],
         2.33: J689["BAO+SN"]["P1"]["2.33"]["sqrtX_q"]}
PN = json.load(open(os.path.join(CFG, "FIGURE_SUMMARY_2026-10-21", "plotted_numbers.json")))["items"]
J223 = json.load(open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_results.json")))
ZC223, HZ223 = np.array(J223["curves"]["z"]), np.array(J223["curves"]["H(z)"])

AI = 1e-3
NI = math.log(AI)
XMASS = (3.0, 5.0, 10.0, 20.0, 40.0)                 # m/H0, declared (illustrative, outside the record)
RATES = {"H_Lambda": math.sqrt(OL)}
for f_, a0_ in A0.items():
    RATES[f"a0/c ({f_})"] = a0_ / C_LIGHT / H0_SI
    RATES[f"sqrt(G rho) ({f_})"] = 2 * a0_ / C_LIGHT / H0_SI
READ = ("eps", "-p", "V")
ZPRED = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)
WLOW, WHIGH = (0.5, 1.0, 1.5, 2.0), (2.5, 3.0, 3.5, 4.0, 4.5, 5.0)
SIG_SYS = 0.375
ZSTAR = 1089.9


# ============================================================================== the KG solver
def rhs(N, y, mu, V0, om, omr, wk, s):
    phi, phiN, D, DN = y
    a = math.exp(N)
    B = om * a**-3 + omr * a**-4 + wk * a**-2 + V0
    H2 = (B + 0.5 * mu * mu * phi * phi) / (1.0 - 0.5 * phiN * phiN)
    dB = -3 * om * a**-3 - 4 * omr * a**-4 - 2 * wk * a**-2
    dH2 = dB - 3 * s * H2 * phiN * phiN
    HNH = dH2 / (2 * H2)
    return [phiN, -(3 * s + HNH) * phiN - mu * mu * phi / H2, DN, -(2 + HNH) * DN + 1.5 * om * a**-3 / H2 * D]


def solve(mu, V0, phi_i, phiN_i=0.0, a_i=AI, a_end=1.0, om=OM, omr=OMR, wk=WK, s=1.0, ngrid=20001):
    Ni, Ne = math.log(a_i), math.log(a_end)
    sol = solve_ivp(rhs, [Ni, Ne], [phi_i, phiN_i, a_i, a_i], args=(mu, V0, om, omr, wk, s), method="DOP853",
                    rtol=1e-10, atol=1e-13, dense_output=True)
    if sol.status != 0:
        raise RuntimeError(sol.message)
    N = np.linspace(Ni, Ne, ngrid)
    phi, phiN, D, DN = sol.sol(N)
    a = np.exp(N)
    B = om * a**-3 + omr * a**-4 + wk * a**-2 + V0
    H2 = (B + 0.5 * mu * mu * phi**2) / (1 - 0.5 * phiN**2)
    kin = 0.5 * H2 * phiN**2
    pot = 0.5 * mu * mu * phi**2
    rho = kin + pot
    eps = V0 + rho
    mp = V0 + pot - kin
    Vr = V0 + pot
    dB = -3 * om * a**-3 - 4 * omr * a**-4 - 2 * wk * a**-2
    dH2 = dB - 3 * s * H2 * phiN**2
    return dict(N=N, a=a, z=1 / a - 1, phi=phi, phiN=phiN, D=D, DN=DN, H2=H2, HNH=dH2 / (2 * H2), rho=rho, eps=eps, mp=mp, V=Vr,
                trace=(eps - 3 * (kin - pot - V0)) / 4, active=-(eps + 3 * (kin - pot - V0)) / 2,
                d_eps=-3 * s * H2 * phiN**2, d_mp=2 * mu * mu * phi * phiN + 3 * s * H2 * phiN**2, d_V=mu * mu * phi * phiN,
                mu=mu, V0=V0, sol=sol)


def model(mH0, r_i, a_end=1.0, s=1.0, ngrid=20001):
    """V0 solved so that V0 + rho_phi(a=1) = W0 (secant); r_i = (1/2) m^2 phi_i^2 / V0."""
    mu = mH0 * h

    def run(V0, ae=1.0, ng=2001):
        return solve(mu, V0, math.sqrt(2 * r_i * V0) / mu, a_end=ae, s=s, ngrid=ng)

    def g(V0):
        o = run(V0)
        return V0 + o["rho"][-1] - W0

    if r_i == 0:
        V0 = W0
    else:
        x0, x1 = W0, W0 / (1 + r_i)
        g0, g1 = g(x0), g(x1)
        for _ in range(60):
            if g1 == g0:
                break
            x2 = x1 - g1 * (x1 - x0) / (g1 - g0)
            if x2 <= 0:
                x2 = 0.5 * x1
            x0, g0, x1 = x1, g1, x2
            g1 = g(x1)
            if abs(g1) < 1e-13 * W0:
                break
        V0 = x1
    o = solve(mu, V0, math.sqrt(2 * r_i * V0) / mu if r_i > 0 else 0.0, a_end=a_end, s=s, ngrid=ngrid)
    o["mH0"], o["r_i"] = mH0, r_i
    return o


def at_a1(o, key):
    i = int(np.argmin(np.abs(o["N"])))
    return o[key][i], i


def ratio(o, rd):
    k = {"eps": "eps", "-p": "mp", "V": "V", "trace": "trace", "active": "active"}[rd]
    F = o[k]
    F0, _ = at_a1(o, k)
    with np.errstate(invalid="ignore"):
        return np.where(F >= 0, np.sqrt(np.clip(F, 0, None) / F0), np.nan)


def dF(o, rd):
    return {"eps": o["d_eps"], "-p": o["d_mp"], "V": o["d_V"]}[rd]


def count_ext(o, rd, Nlo, Nhi):
    d = dF(o, rd)
    F = o[{"eps": "eps", "-p": "mp", "V": "V"}[rd]]
    m = (o["N"] >= Nlo) & (o["N"] <= Nhi)
    dd = d[m]
    tol = 1e-12 * np.abs(F[m]).max()
    sg = np.sign(np.where(np.abs(dd) < tol, 0, dd))
    sg = sg[sg != 0]
    return int(np.sum(sg[1:] != sg[:-1])) if sg.size > 1 else 0


def lnz_N(z):
    return -math.log(1 + z)


def interp_z(o, arr, z):
    """value of arr at redshift z (N = -ln(1+z)); o['N'] is increasing."""
    return float(np.interp(-math.log(1 + z), o["N"], arr))


def band_pass(o):
    r = ratio(o, "eps")
    ok, info = True, {}
    for z, q in BANDZ.items():
        v = interp_z(o, r, z)
        info[z] = v
        if not (q[0] <= v <= q[4]):
            ok = False
    return ok, info


def pos_pass(o):
    m = o["N"] <= 1e-12
    return bool(np.all(o["mp"][m] >= 0))


def z_osc(o):
    H = np.sqrt(o["H2"])
    mu = o["mu"]
    if H[-1] >= mu:
        return None
    i = np.where(H >= mu)[0]
    if i.size == 0:
        return float(o["z"][0])
    j = i[-1]
    # linear interpolation in N
    Nj = np.interp(mu, [H[j + 1], H[j]], [o["N"][j + 1], o["N"][j]])
    return float(math.exp(-Nj) - 1)


def beta_fit(o, zlo, zhi):
    m = (o["z"] >= zlo) & (o["z"] <= zhi)
    x, y = np.log1p(o["z"][m]), np.log(o["rho"][m])
    return float(np.polyfit(x, y, 1)[0])


# ============================================================================== cosmic time (comparison background)
def H_base(a):
    return math.sqrt(OM * a**-3 + OMR * a**-4 + WK * a**-2 + W0)


def t_of_z(z):
    a = 1 / (1 + z)
    return quad(lambda x: 1 / (x * H_base(x)), 0, a, epsabs=0, epsrel=1e-12, limit=400)[0]   # units 1/H100


# ============================================================================== points (panel d, read only)
PT_KEYS = ["meerkat", "rc100_q1", "rc100_q2", "rc100_q3", "aless", "alpine6", "cristal_rout"]
LABELS = {"meerkat": "MeerKAT HI", "rc100_q1": "RC100 B Q1", "rc100_q2": "RC100 B Q2", "rc100_q3": "RC100 B Q3",
          "aless": "ALESS 122.1", "alpine6": "ALPINE 6 pooled", "cristal_rout": "CRISTAL R_out", "cristal_re": "CRISTAL R_e",
          "rc100_q4": "RC100 B Q4 (95% upper bound)"}


def load_points(keys):
    z = np.array([PN[f"d.pt.{k}.z"]["value"] for k in keys])
    s = np.array([PN[f"d.pt.{k}.s"]["value"] for k in keys])
    lo = np.array([PN[f"d.pt.{k}.lo68"]["value"] for k in keys])
    hi = np.array([PN[f"d.pt.{k}.hi68"]["value"] for k in keys])
    return z, np.log10(s), 0.5 * (np.log10(hi) - np.log10(lo))


# ============================================================================== detection statistic
def bank(zs, tz):
    T, lab = [], []
    for mH0 in XMASS:
        for beta in (0.0, 3.0):
            for j in range(8):
                ph = j * math.pi / 8
                T.append((1 + zs) ** beta * np.cos(2 * mH0 * h * tz + ph))
                lab.append((mH0, beta, ph))
    return np.array(T), lab


def stat_T(Y, sig, TB):
    """Y: (n_mock, n_pts). Returns T = chi2_flat+c - min_k chi2_(c + A T_k)."""
    w = 1 / sig**2
    Sw = w.sum()
    Swy = Y @ w
    Swyy = (Y**2) @ w
    chi0 = Swyy - Swy**2 / Sw
    best = np.full(Y.shape[0], np.inf)
    for Tk in TB:
        S1, S2 = (w * Tk).sum(), (w * Tk**2).sum()
        Sty = Y @ (w * Tk)
        det = Sw * S2 - S1**2
        # chi2_min = Swyy - [b^T M^-1 b], b = (Swy, Sty), M = [[Sw, S1],[S1, S2]]
        q = (S2 * Swy**2 - 2 * S1 * Swy * Sty + Sw * Sty**2) / det
        best = np.minimum(best, Swyy - q)
    return chi0 - best


def chi2_curve(y, sig, f):
    w = 1 / sig**2
    r = y - f
    c = (w * r).sum() / w.sum()
    return float((w * (r - c) ** 2).sum())


# ============================================================================== MODE K
def run_K():
    P(f"CFG957 mode K  (criteria 8e884c9a2b). The owner's idea (2026-10-21).")
    P(f"background (CFG689 primary best fit): omega_m {OM:.6f} omega_k {WK:+.6f} omega_r {OMR:.4e} W0 {W0:.6f}; h {h:.5f}")
    res = {}
    # K1 points from their source files
    P("K1: the panel-(d) points re-read from their sources")
    c303 = json.load(open(os.path.join(CFG, "CFG303_lcdm_free_inputs", "cfg303_rc100_cristal_LCDMFREE_results.json")))
    c303 = c303.get("numbers", c303)["points"]
    c309 = json.load(open(os.path.join(CFG, "CFG309_mightee_width_frame", "cfg309_cfg301chain_FRAME_summary.json")))["frame"]
    c301 = json.load(open(os.path.join(CFG, "CFG301_mightee_hi_catalogue_width_chain", "cfg301_stageB_results.json")))["numbers"]["results"]
    cp = {r["object"]: r for r in csv.DictReader(open(os.path.join(CFG, "CHART_a0z_combined_2026-09-30", "chart_a0z_points.csv")))}
    src = {}
    q = c309["q_a0"]
    src["meerkat"] = dict(z=float(np.median([c301[w]["z_med"] for w in ("W1", "W2", "W3")])), s=c309["s"], lo68=q[1] / 9.3603e-11,
                          hi68=q[2] / 9.3603e-11, lo95=q[0] / 9.3603e-11, hi95=q[3] / 9.3603e-11)
    for i, qq in enumerate(("B Q1", "B Q2", "B Q3")):
        r = c303["RC100"][qq]
        src[f"rc100_q{i + 1}"] = dict(z=r["z_med"], s=r["s"], lo68=r["lo68"], hi68=r["hi68"], lo95=r["lo95"], hi95=r["hi95"])
    r = c303["RC100"]["B Q4"]
    src["rc100_q4"] = dict(z=r["z_med"], s=r["hi95"], lo68=r["hi95"], hi68=r["hi95"], lo95=r["hi95"], hi95=r["hi95"])
    for k, row in (("aless", "ALESS_122.1"), ("alpine6", "ALPINE6 pooled")):
        r = cp[row]
        src[k] = dict(z=float(r["z"]), s=float(r["s_star"]), lo68=float(r["stat68_lo"]), hi68=float(r["stat68_hi"]),
                      lo95=float(r["stat95_lo"]), hi95=float(r["stat95_hi"]))
    for k, key in (("cristal_re", "R_e native, six"), ("cristal_rout", "R_out native, six, outermost data marker (primary)")):
        r = c303["CRISTAL"][key]
        src[k] = dict(z=r["z_med"], s=r["s"], lo68=r["lo68"], hi68=r["hi68"], lo95=r["lo95"], hi95=r["hi95"])
    worst = 0.0
    for k, d in src.items():
        for fld, v in d.items():
            pv = PN[f"d.pt.{k}.{fld}"]["value"]
            worst = max(worst, abs(v - pv) / max(abs(pv), 1e-300))
    check("K1 points equal plotted_numbers.json (relative)", worst <= 1e-9, f"worst {worst:.2e} over {len(src)} points")
    res["K1"] = dict(worst=worst)
    # K2 CFG689 quantiles and h
    worst = 0.0
    for z, key in ((1.0, "1.0"), (1.2, "1.2"), (1.5, "1.5"), (2.0, "2.0"), (2.33, "2.33")):
        qq = BANDZ[z]
        for j, nm in ((1, "q16"), (2, "q50"), (3, "q84")):
            pv = PN[f"d.band.{key}.{nm}"]["value"]
            worst = max(worst, abs(qq[j] - pv) / abs(pv))
    hP3 = J689["BAO+SN"]["P3"]["H0_q"][2] / 100
    check("K2 CFG689 band quantiles equal plotted_numbers.json", worst <= 1e-9, f"worst {worst:.2e}")
    check("K2 h from pbest within 0.005 of P3 median", abs(h - hP3) <= 0.005, f"h {h:.5f} vs {hP3:.5f}")
    res["K2"] = dict(worst=worst, h=h, h_P3=hP3)
    # K3 solver
    P("K3: the Klein-Gordon solver")
    o = model(10.0, 0.0)
    dev = max(np.nanmax(np.abs(ratio(o, rd) - 1)) for rd in ("eps", "-p", "V"))
    check("K3a r_i = 0: every reading ratio == 1", dev <= 1e-10, f"max |ratio - 1| {dev:.2e}")
    mu = 10.0
    oe = solve(mu, 0.0, 1e-3, a_i=1e-6, a_end=3.0, om=1.0, omr=0.0, wk=0.0, ngrid=200001)
    tt = (2.0 / 3.0) * oe["a"] ** 1.5
    x = mu * tt
    m = (x >= 0.1) & (x <= 30)
    err = float(np.max(np.abs(oe["phi"][m] / 1e-3 - np.sin(x[m]) / x[m])))
    check("K3b EdS: phi/phi_i = sin(mt)/(mt) over mt in [0.1, 30]", err <= 1e-6, f"max abs err {err:.2e}")
    oc = model(10.0, 0.5, ngrid=200001)
    deps = np.gradient(oc["eps"], oc["N"], edge_order=2)
    m = oc["N"] > NI + 0.05
    rel = float(np.max(np.abs(deps[m] + 3 * (oc["eps"][m] - oc["mp"][m])) / oc["eps"][m]))
    check("K3c |d eps/dN + 3(eps + p)| / eps <= 1e-6 (m = 10 H0, r_i = 0.5)", rel <= 1e-6, f"max {rel:.2e}")
    cross = {}
    for mm in (1.2, 2.0):
        od = solve(mm, 1.0, 1e-3, a_i=1.0, a_end=math.exp(20.0), om=0.0, omr=0.0, wk=0.0, ngrid=40001)
        sg = np.sign(od["phi"])
        cross[mm] = int(np.sum(sg[1:] != sg[:-1]))
    check("K3d de Sitter: m = 1.2 H never crosses zero; m = 2 H does", cross[1.2] == 0 and cross[2.0] >= 1, f"crossings {cross}")
    res["K3"] = dict(dev_r0=dev, eds_err=err, energy_rel=rel, ds_crossings={str(k): v for k, v in cross.items()})
    # K4 WKB damping
    o4 = model(40.0, 0.01)
    b4 = beta_fit(o4, 0.3, 3.0)
    check("K4 beta_rho at m = 40 H0 over z in [0.3, 3] within 3 +- 0.1", abs(b4 - 3) <= 0.1, f"beta_rho {b4:.4f}")
    res["K4"] = dict(beta_rho=b4)
    # K5 rival
    worst = 0.0
    for zz in (1.0, 2.0, 3.0, 4.0, 5.0):
        v = float(np.interp(zz, ZC223, HZ223))
        worst = max(worst, abs(v - PN[f"d.rival.{zz:.1f}"]["value"]) / v)
    check("K5 rival a0 ∝ H(z) equals plotted_numbers.json", worst <= 1e-9, f"worst {worst:.2e}")
    res["K5"] = dict(worst=worst)
    ok = all(o_ for _, o_ in CHECKS)
    P(f"K overall: {'PASS' if ok else 'FAIL'}  ({sum(o_ for _, o_ in CHECKS)}/{len(CHECKS)})")
    return dict(K_pass=ok, results=res)


# ============================================================================== MODE MAIN
def rmax_search(mH0):
    grid = 10 ** np.arange(-4, 3.0001, 0.25)
    pb_, pp_ = [], []
    for r in grid:
        o = model(mH0, float(r), ngrid=8001)
        pb_.append(band_pass(o)[0])
        pp_.append(pos_pass(o))

    def edge(flags, test):
        flags = np.array(flags)
        if flags.all():
            return float(grid[-1]), "grid edge (>= 1e3)", int(np.sum(~flags))
        i = int(np.argmax(~flags))
        if i == 0:
            return 0.0, "< 1e-4", int(np.sum(~flags))
        lo, hi = math.log10(grid[i - 1]), math.log10(grid[i])
        for _ in range(30):
            mid = 0.5 * (lo + hi)
            if test(model(mH0, 10**mid, ngrid=8001)):
                lo = mid
            else:
                hi = mid
        nonmono = int(np.sum(flags[i:]))
        return float(10**lo), "bisected", nonmono

    rb = edge(pb_, lambda o: band_pass(o)[0])
    rp = edge(pp_, pos_pass)
    return dict(r_band=rb[0], r_band_how=rb[1], band_passes_after_first_fail=rb[2], r_pos=rp[0], r_pos_how=rp[1],
                pos_passes_after_first_fail=rp[2], r_max={"eps": rb[0], "V": rb[0], "-p": min(rb[0], rp[0])})


def run_MAIN():
    P(f"CFG957 mode MAIN  (criteria 8e884c9a2b). The owner's idea (2026-10-21): a0(z) oscillates like a wave.")
    P(f"background (CFG689 primary best fit): omega_m {OM:.6f} omega_k {WK:+.6f} W0 {W0:.6f}; h {h:.5f}; Omega_L {OL:.5f}")
    P("kappa = 1/2 FITTED; footings never pooled; not theory closed; CFG956 owns the expansion bound.")
    R = {}
    # ---------------------------------------------------------------- Part 1, M1 (R) record rates
    P("")
    P("=== Part 1, M1 (R): the record's own rates (CFG245) ===")
    P(f"  threshold for asymptotic oscillation (3/2) H_Lambda = {1.5 * math.sqrt(OL):.4f} H0")
    RR = {}
    for nm, rate in RATES.items():
        row = {}
        for r_i in (0.01, 1.0):
            o = model(rate, r_i, a_end=100.0, ngrid=40001)
            row[str(r_i)] = {rd: dict(ext_z5=count_ext(o, rd, lnz_N(5), 0), ext_z10=count_ext(o, rd, lnz_N(10), 0),
                                      ext_future=count_ext(o, rd, 1e-9, math.log(100.0))) for rd in READ}
            row[str(r_i)]["phi_zero_crossings_all"] = int(np.sum(np.sign(o["phi"][1:]) != np.sign(o["phi"][:-1])))
        RR[nm] = dict(m_over_H0=rate, runs=row)
        e = row["1.0"]
        P(f"  {nm:22s} m = {rate:.4f} H0 | r_i 1: extrema z<=5 eps/-p/V {e['eps']['ext_z5']}/{e['-p']['ext_z5']}/{e['V']['ext_z5']}, "
          f"z<=10 {e['eps']['ext_z10']}/{e['-p']['ext_z10']}/{e['V']['ext_z10']}, future(a<=100) {e['eps']['ext_future']}/"
          f"{e['-p']['ext_future']}/{e['V']['ext_future']}; phi zero crossings {e['phi_zero_crossings_all']}; "
          f"r_i 0.01 same counts: {row['0.01']['-p']['ext_z5']}/{row['0.01']['-p']['ext_future']} (-p)")
    wave_R = any(RR[n]["runs"][ri][rd]["ext_z5"] >= 2 for n in RR for ri in RR[n]["runs"] for rd in READ)
    P(f"  => WAVE from a record rate: {wave_R}")
    R["M1_R"] = dict(rates=RR, wave_from_record_rate=wave_R)

    # ---------------------------------------------------------------- Part 1, M1 (X) masses
    P("")
    P("=== Part 1, M1 (X): declared outside masses m/H0 in {3, 5, 10, 20, 40}; two new constants (m, r_i) ===")
    MX = {}
    curves = {}
    for mH0 in XMASS:
        t1 = time.time()
        rm = rmax_search(mH0)
        info = dict(rmax=rm)
        P(f"  m = {mH0:4.0f} H0: r_band {rm['r_band']:.4g} ({rm['r_band_how']}), r_pos {rm['r_pos']:.4g} ({rm['r_pos_how']}); "
          f"r_max eps/V {rm['r_max']['eps']:.4g}, -p {rm['r_max']['-p']:.4g}  "
          f"[non-monotone flags: band {rm['band_passes_after_first_fail']}, pos {rm['pos_passes_after_first_fail']}]  ({time.time() - t1:.0f} s)")
        per = {}
        for rd in READ:
            r_i = rm["r_max"][rd]
            o = model(mH0, r_i, a_end=100.0, ngrid=60001)
            ob = model(mH0, r_i, ngrid=50001)            # a <= 1, fine grid for observables
            curves[(mH0, rd)] = ob
            zo = z_osc(ob)
            rr = ratio(ob, rd)
            pred = {str(z): float(np.log10(interp_z(ob, rr, z))) for z in ZPRED}
            ext5 = count_ext(o, rd, lnz_N(5), 0)
            ext10 = count_ext(o, rd, lnz_N(10), 0)
            extf = count_ext(o, rd, 1e-9, math.log(100.0))
            Fk = {"eps": "eps", "-p": "mp", "V": "V"}[rd]
            F0, i0 = at_a1(ob, Fk)
            rate_today = 0.5 * dF(ob, rd)[i0] / F0          # (1/a0) da0/dt in H0 units (H(a=1) = H0)
            # damping
            beta = None
            if zo is not None and zo >= 2:
                beta = beta_fit(ob, 0.0, zo / 2)
            # beta_eps = beta + <dlnH/dln(1+z)>
            beta_eps = None
            if beta is not None:
                msk = (ob["z"] >= 0) & (ob["z"] <= zo / 2)
                beta_eps = beta + float(np.mean(-ob["HNH"][msk]))
            Hz = lambda z: math.sqrt(interp_z(ob, ob["H2"], z))
            Pln = {str(z): math.pi * Hz(z) / ob["mu"] for z in (0.0, 1.0, 2.33)}
            Ta0 = math.pi / ob["mu"] * GYR_PER_H100
            # testability
            nlow = sum(abs(pred[str(z)]) >= 0.15 for z in WLOW)
            nhigh = sum(abs(pred[str(z)]) >= 0.15 for z in WHIGH)
            # ratchet (one-sided running max) and two-sided average
            lnF = 0.5 * np.log(np.clip({"eps": ob["eps"], "-p": ob["mp"], "V": ob["V"]}[rd], 1e-300, None) / F0)
            m3 = ob["z"] <= 3.0
            m10 = ob["z"] <= 10.0
            dt = np.gradient(ob["N"]) / np.sqrt(ob["H2"])
            ratchet3 = float(np.max(lnF[m3]))
            ratchet10 = float(np.max(lnF[m10]))
            avg3 = float(np.sum(lnF[m3] * dt[m3]) / np.sum(dt[m3]))
            lev = R.get("lever", None)
            # mismatch with the expansion-side eps ratio over z in [2.5, 5]
            re = ratio(ob, "eps")
            mz = (ob["z"] >= 2.5) & (ob["z"] <= 5.0)
            with np.errstate(invalid="ignore", divide="ignore"):
                mism = float(np.nanmax(np.abs(np.log10(rr[mz]) - np.log10(re[mz]))))
            fossil = 0.25 * float(np.max(lnF[m10]))
            # galaxy-response: bin averaging factor (Delta ln(1+z) = 0.2)
            sinc = {}
            for z in (1.0, 2.5, 4.0):
                x_ = math.pi * 0.2 / Pln_at(ob, z)
                sinc[str(z)] = abs(math.sin(x_) / x_)
            per[rd] = dict(r_i=r_i, V0=ob["V0"], z_osc=zo, extrema_z5=ext5, extrema_z10=ext10, extrema_future=extf,
                           wave=ext5 >= 2, pred_log10=pred, rate_today_H0=rate_today, rate_today_per_yr=rate_today * H0_PER_YR,
                           down_today=bool(rate_today < 0), beta=beta, beta_eps=beta_eps, P_ln=Pln, T_a0_Gyr=Ta0,
                           n_low_ge015=nlow, n_high_ge015=nhigh, testable_low=nlow >= 2, testable_high=nhigh >= 2,
                           ratchet_z3=ratchet3, ratchet_z10=ratchet10, twosided_avg_z3=avg3, mismatch_z25_5=mism,
                           fossil_E_sigma=fossil, sinc_bin02=sinc)
            P(f"    {rd:3s} r_i {r_i:.4g}: z_osc {zo if zo is None else round(zo, 2)}, extrema z<=5 {ext5} (z<=10 {ext10}, future {extf}), "
              f"T_a0 {Ta0:.2f} Gyr, P_ln(0/1/2.33) {Pln['0.0']:.2f}/{Pln['1.0']:.2f}/{Pln['2.33']:.2f}, beta "
              f"{'-' if beta is None else f'{beta:.3f}'}{'' if beta_eps is None else f' (eps ripple {beta_eps:.2f})'}, "
              f"today {'DOWN' if rate_today < 0 else 'up'} {rate_today:+.3e} H0")
            P(f"        log10 a0(z)/a0(0) at z 0.5..5: " + " ".join(f"{pred[str(z)]:+.3f}" for z in ZPRED) +
              f" | >=0.15 dex: low {nlow}, high {nhigh} | ratchet z<=3 {ratchet3:+.3f} (z<=10 {ratchet10:+.3f}), avg {avg3:+.4f}; "
              f"mismatch {mism:.3f} dex")
        info["readings"] = per
        MX[str(mH0)] = info
    R["M1_X"] = MX

    # ---------------------------------------------------------------- phase map
    P("")
    P("=== phase today on 400 log-spaced masses in [3, 40] H0 at r_i = 0.01 ===")
    ms = np.geomspace(3, 40, 400)
    down = {rd: [] for rd in READ}
    ext5 = {rd: [] for rd in READ}
    for mH0 in ms:
        o = model(float(mH0), 0.01, ngrid=6001)
        for rd in READ:
            F0, i0 = at_a1(o, {"eps": "eps", "-p": "mp", "V": "V"}[rd])
            down[rd].append(bool(dF(o, rd)[i0] < 0))
            ext5[rd].append(count_ext(o, rd, lnz_N(5), 0))
    PH = {}
    for rd in READ:
        fr = float(np.mean(down[rd]))
        cls = "THEOREM (always non-increasing)" if rd == "eps" else ("NATURAL" if fr >= 0.9 else "CHOSEN")
        if rd == "eps" and fr < 1.0:
            cls = "check: eps non-increasing but sign 0/rounding"
        PH[rd] = dict(frac_down=fr, cls=cls, ext5_min=int(min(ext5[rd])), ext5_max=int(max(ext5[rd])),
                      m_down=[float(x) for x, d in zip(ms, down[rd]) if d][:400])
        P(f"  {rd:3s}: fraction 'on the way down' today {fr:.3f} -> {cls}; extrema z<=5 range {min(ext5[rd])}-{max(ext5[rd])}")
    R["phase_map"] = PH

    # ---------------------------------------------------------------- (a) galaxy points: curves vs flat; detection statistic
    P("")
    P("=== (a) galaxy dynamics: the committed points (panel d), statistic T ===")
    zs, y, sig = load_points(PT_KEYS)
    for k, zz, yy, ss in zip(PT_KEYS, zs, y, sig):
        P(f"  {LABELS[k]:16s} z {zz:6.3f}  log10 s* {yy:+.3f}  sigma {ss:.3f} dex")
    zq4 = PN["d.pt.rc100_q4.z"]["value"]
    P(f"  {LABELS['rc100_q4']}: z {zq4:.2f}, s* < {PN['d.pt.rc100_q4.s']['value']:.3f} (listed only)")
    sig_sys = np.sqrt(sig**2 + SIG_SYS**2)
    CV = {}
    for mH0 in XMASS:
        for rd in READ:
            ob = curves[(mH0, rd)]
            f = np.array([math.log10(interp_z(ob, ratio(ob, rd), z)) for z in zs])
            d_stat = chi2_curve(y, sig, f) - chi2_curve(y, sig, 0 * f)
            d_sys = chi2_curve(y, sig_sys, f) - chi2_curve(y, sig_sys, 0 * f)
            pulls = (f - 0) / sig
            CV[f"{mH0:g}|{rd}"] = dict(dchi2_stat=d_stat, dchi2_sys=d_sys, shift_dex=[float(v) for v in f],
                                       max_shift_over_sigma=float(np.max(np.abs(f) / sig)))
    P("  Delta chi2 (curve + c) - (flat + c), stat / sys, per (m, reading) at r_max:")
    for mH0 in XMASS:
        P("   m " + f"{mH0:4.0f}" + "  " + "  ".join(f"{rd}: {CV[f'{mH0:g}|{rd}']['dchi2_stat']:+.2f}/{CV[f'{mH0:g}|{rd}']['dchi2_sys']:+.3f} "
                                                   f"(max |shift|/sigma {CV[f'{mH0:g}|{rd}']['max_shift_over_sigma']:.2f})" for rd in READ))
    R["curves_vs_points"] = CV
    tz = np.array([t_of_z(z) for z in zs])
    TB, lab = bank(zs, tz)
    rng = np.random.default_rng(9571)
    Tnull = stat_T(rng.normal(0, 1, (4000, len(zs))) * sig, sig, TB)
    T3 = float(np.quantile(Tnull, 0.9973))
    Tobs = float(stat_T(y[None, :], sig, TB)[0])
    p_stat = (1 + int(np.sum(Tnull >= Tobs))) / 4001
    rng2 = np.random.default_rng(9573)
    Tnull_s = stat_T(rng2.normal(0, 1, (4000, len(zs))) * sig_sys, sig_sys, TB)
    Tobs_s = float(stat_T(y[None, :], sig_sys, TB)[0])
    p_sys = (1 + int(np.sum(Tnull_s >= Tobs_s))) / 4001
    # best template (reported; never adopted)
    w = 1 / sig**2
    bestk, bestchi = None, np.inf
    for k, Tk in enumerate(TB):
        X = np.vstack([np.ones_like(Tk), Tk]).T
        Wm = np.diag(w)
        coef = np.linalg.solve(X.T @ Wm @ X, X.T @ Wm @ y)
        chi = float(((y - X @ coef) ** 2 * w).sum())
        if chi < bestchi:
            bestchi, bestk, bestcoef = chi, k, coef
    if p_stat >= 0.05:
        lbl = "NO WAVE SIGNAL"
    elif p_sys >= 0.05:
        lbl = "PATTERN IN STATISTICAL ERRORS ONLY"
    elif p_stat < 0.003:
        lbl = "WAVE-LIKE PATTERN, NOT A DETECTION"
    else:
        lbl = "PATTERN IN STATISTICAL ERRORS ONLY (p_sys < 0.05 but p_stat >= 0.003)"
    P(f"  statistic T (80 templates): T_obs {Tobs:.2f}, p_stat {p_stat:.4f} (T_3sigma {T3:.2f}); systematic variant T {Tobs_s:.2f}, "
      f"p_sys {p_sys:.4f} -> {lbl}")
    P(f"  best template (reported, never adopted): m {lab[bestk][0]:g} H0, beta {lab[bestk][1]:g}, phi {lab[bestk][2]:.3f}; "
      f"A {bestcoef[1]:+.3e}, c {bestcoef[0]:+.3f}; chi2 flat+c {chi2_curve(y, sig, 0 * y):.2f} -> {bestchi:.2f}")
    # variant: CRISTAL R_e instead of R_out
    keys_v = [k if k != "cristal_rout" else "cristal_re" for k in PT_KEYS]
    zv, yv, sv = load_points(keys_v)
    TBv, _ = bank(zv, np.array([t_of_z(z) for z in zv]))
    rngv = np.random.default_rng(9575)
    Tn_v = stat_T(rngv.normal(0, 1, (4000, len(zv))) * sv, sv, TBv)
    To_v = float(stat_T(yv[None, :], sv, TBv)[0])
    p_v = (1 + int(np.sum(Tn_v >= To_v))) / 4001
    P(f"  variant (CRISTAL R_e for R_out): T_obs {To_v:.2f}, p_stat {p_v:.4f}")
    R["statistic"] = dict(T_obs=Tobs, p_stat=p_stat, T3sigma=T3, T_obs_sys=Tobs_s, p_sys=p_sys, label=lbl,
                          best_template=dict(m_over_H0=lab[bestk][0], beta=lab[bestk][1], phi=lab[bestk][2], A=float(bestcoef[1]),
                                             c=float(bestcoef[0]), chi2_flat=chi2_curve(y, sig, 0 * y), chi2_best=bestchi),
                          variant_cristal_re=dict(T_obs=To_v, p_stat=p_v), points=dict(keys=PT_KEYS, z=zs.tolist(), y=y.tolist(), sigma=sig.tolist()),
                          caveat="53 no-root galaxies at z~2-5 are excluded from the points (selection biases them high); baryon masses move s* by factors 2-10 (CFG223)")

    # ---------------------------------------------------------------- (c) shear lever
    P("")
    P("=== (c) structure growth: the shear engine's footing lever and the ratchet ===")
    lnr = math.log(1.1312e-10 / 9.3603e-11)
    lev = dict(native=(-9.39 + 10.08) / lnr, inherited=(-7.18 + 7.70) / lnr)
    P(f"  lever dDelta chi2/d ln a0: native {lev['native']:.3f}, inherited {lev['inherited']:.3f} (NC2x robust span -12.85 .. -5.69; TENSION at +4)")
    SH = {}
    for mH0 in XMASS:
        for rd in READ:
            pr = MX[str(mH0)]["readings"][rd]
            SH[f"{mH0:g}|{rd}"] = dict(dd_native_ratchet3=lev["native"] * pr["ratchet_z3"], dd_native_ratchet10=lev["native"] * pr["ratchet_z10"],
                                       dd_native_avg3=lev["native"] * pr["twosided_avg_z3"], dd_inh_ratchet3=lev["inherited"] * pr["ratchet_z3"])
    mx = max(abs(v["dd_native_ratchet10"]) for v in SH.values())
    P(f"  largest |Delta Delta chi2| (native lever x one-sided ratchet over z<=10) over every curve: {mx:.2f}; class line needs >= {4 + 9.39:.2f}")
    R["shear"] = dict(lever=lev, per_curve=SH, max_abs=mx, class_change=bool(mx >= 13.39))
    fmax = max(MX[str(m_)]["readings"][rd]["fossil_E_sigma"] for m_ in XMASS for rd in READ)
    P(f"  largest deep-MOND fossil E_sigma = (1/4) ln(a0_max/a0_0) over z<=10: {fmax:+.3f} (dwarfs +0.38, CFG827)")
    R["fossil_max"] = fmax

    # ---------------------------------------------------------------- (d) CMB distance and ISW
    P("")
    P("=== (d) CMB: distance to last scattering (reported only; CFG689 theta* blocked by K9) and an ISW proxy ===")
    ob0 = model(10.0, 0.0, ngrid=50001)

    def DM_star(o):
        N = o["N"]
        f = np.exp(-N) / np.sqrt(o["H2"])
        chi = TRAPZ(f, N)
        V0, r_i = o["V0"], o["r_i"]
        tail = quad(lambda x: 1 / (x * x * math.sqrt(OM * x**-3 + OMR * x**-4 + WK * x**-2 + V0 * (1 + r_i))),
                    1 / (1 + ZSTAR), AI, epsabs=0, epsrel=1e-12)[0]
        chi += tail
        return math.sinh(math.sqrt(WK) * chi) / math.sqrt(WK) if WK > 0 else chi

    def ISW(o):
        m = o["z"] <= 3.0
        g = (o["DN"] - o["D"]) / o["a"]
        return float(TRAPZ(np.abs(g[m]), o["N"][m]))

    dm0, isw0 = DM_star(ob0), ISW(ob0)
    CM = {}
    for mH0 in XMASS:
        ob = curves[(mH0, "eps")]
        dd = DM_star(ob) / dm0 - 1
        di = ISW(ob) / isw0 - 1
        CM[str(mH0)] = dict(r_i=ob["r_i"], dDM_over_DM=dd, theta_pull=-dd / (0.00030 / 1.04109), dISW=di)
        P(f"  m {mH0:4.0f} H0 (r_i {ob['r_i']:.4g}): dD_M(z*)/D_M {dd:+.3e} (= {-dd / (0.00030 / 1.04109):+.1f} sigma of 100theta* 1.04109 +- 0.00030, "
          f"no refit), ISW proxy change {di:+.3e} (vs 20%)")
    R["cmb"] = dict(DM0=dm0, ISW0=isw0, per_mass=CM, blocked="CFG689 theta* rows held back: K9 failed as frozen; no class rests here")

    # ---------------------------------------------------------------- (b) summary of today's rate
    P("")
    P("=== (b) today's (1/a0) da0/dt at r_max (H0 units; per yr) ===")
    for mH0 in XMASS:
        P("   m " + f"{mH0:4.0f}" + "  " + "  ".join(f"{rd}: {MX[str(mH0)]['readings'][rd]['rate_today_H0']:+.2e} H0 "
                                                   f"({MX[str(mH0)]['readings'][rd]['rate_today_per_yr']:+.1e}/yr)" for rd in READ))
    P("  record local constraints on da0/dt: none (Solar System screened, CFG770; WB envelope a0-free, CFG740; globulars screened, CFG820)")

    # ---------------------------------------------------------------- report-only readings (trace, active) for m = 10
    ob = model(10.0, MX["10.0"]["rmax"]["r_max"]["V"], ngrid=20001)
    tr = {rd: {str(z): float(np.log10(interp_z(ob, ratio(ob, rd), z))) for z in (1.0, 2.5, 4.0)} for rd in ("trace", "active")}
    P("")
    P(f"  report only, m 10 H0 at r_max(V): trace {tr['trace']}, active {tr['active']}")
    R["report_only_trace_active_m10"] = tr

    # ---------------------------------------------------------------- export curves for the figure
    zgrid = np.linspace(0, 5.75, 600)
    EXP = {}
    for mH0 in XMASS:
        for rd in READ:
            ob = curves[(mH0, rd)]
            rr = ratio(ob, rd)
            EXP[f"{mH0:g}|{rd}"] = [float(interp_z(ob, rr, z)) for z in zgrid]
    R["figure_curves"] = dict(z=zgrid.tolist(), curves=EXP)
    return R


def Pln_at(o, z):
    return math.pi * math.sqrt(interp_z(o, o["H2"], z)) / o["mu"]


# ============================================================================== MODE MUTATE
def run_MUTATE():
    P(f"CFG957 mode MUTATE  (criteria 8e884c9a2b). The owner's idea (2026-10-21).")
    R = {}
    zs, y, sig = load_points(PT_KEYS)
    tz = np.array([t_of_z(z) for z in zs])
    TB, _ = bank(zs, tz)
    rng = np.random.default_rng(9571)
    Tnull = stat_T(rng.normal(0, 1, (4000, len(zs))) * sig, sig, TB)
    T3 = float(np.quantile(Tnull, 0.9973))
    # M-a planted wave
    Tp = (1 + zs) ** 3 * np.cos(2 * 7.0 * h * tz + 1.0)
    Ap = 3.0 / math.sqrt(np.mean((Tp / sig) ** 2))
    rng4 = np.random.default_rng(9574)
    Ymock = Ap * Tp[None, :] + rng4.normal(0, 1, (500, len(zs))) * sig
    Tm = stat_T(Ymock, sig, TB)
    rate = float(np.mean(Tm >= T3))
    check("M-a planted wave (m 7 H0, beta 3, phi 1.0, RMS 3x the real errors) detected in >= 90%", rate >= 0.9,
          f"rate {rate:.3f} at T_3sigma {T3:.2f}; planted shifts (dex) {np.round(Ap * Tp, 3).tolist()}")
    R["M_a"] = dict(rate=rate, T3=T3, A_p=Ap, planted_dex=(Ap * Tp).tolist())
    # M-b null
    rng2 = np.random.default_rng(9572)
    Tn2 = stat_T(rng2.normal(0, 1, (4000, len(zs))) * sig, sig, TB)
    fp = float(np.mean(Tn2 >= T3))
    check("M-b fresh null mocks: false-positive rate at T_3sigma <= 0.01", fp <= 0.01, f"rate {fp:.4f}")
    R["M_b"] = dict(fp=fp)
    # M-c friction teeth
    o = model(40.0, 0.01)
    b = beta_fit(o, 0.3, 3.0)
    orv = solve(40.0 * h, o["V0"], o["phi"][0], s=-1.0, ngrid=20001)
    m = (orv["z"] >= 0.3) & (orv["z"] <= 3.0)
    brv = float(np.polyfit(np.log1p(orv["z"][m]), np.log(orv["rho"][m]), 1)[0])
    check("M-c reversed Hubble friction gives beta_rho < 0 while normal beta_rho in 3 +- 0.1", brv < 0 and abs(b - 3) <= 0.1,
          f"normal {b:.3f}, reversed {brv:.3f}")
    R["M_c"] = dict(beta=b, beta_reversed=brv)
    # M-d partner teeth
    mu = 10.0 * h
    phi_i = math.sqrt(2 * 0.1 * W0) / mu

    def rhs_p(N, yv, q):
        phi, phiN = yv
        a = math.exp(N)
        H2 = OM * a**-3 + OMR * a**-4 + WK * a**-2 + W0
        HNH = (-3 * OM * a**-3 - 4 * OMR * a**-4 - 2 * WK * a**-2) / (2 * H2)
        Hh = math.sqrt(H2)
        Q = q * 3 * Hh * W0
        return [phiN, -(3 + HNH) * phiN - mu * mu * phi / H2 + (Q / (Hh**3 * phiN) if q > 0 else 0.0)]

    ev = lambda N, yv, q: yv[1]
    ev.terminal = False
    s0 = solve_ivp(rhs_p, [NI, 0], [phi_i, 1e-3 * phi_i], args=(0.0,), method="DOP853", rtol=1e-10, atol=1e-14, events=ev, dense_output=True)
    n0 = len(s0.t_events[0])
    evt = lambda N, yv, q: yv[1]
    evt.terminal = True
    s1 = solve_ivp(rhs_p, [NI, 0], [phi_i, 1e-3 * phi_i], args=(1e-6,), method="Radau", rtol=1e-9, atol=1e-16, events=evt, dense_output=True)
    n1 = len(s1.t_events[0])
    NN = np.linspace(NI, s1.t[-1], 20001)
    minphiN = float(np.min(s1.sol(NN)[1]))
    ok = n0 >= 2 and n1 == 0 and s1.status == 0 and minphiN > 0
    check("M-d partner: Q = 0 gives >= 2 sign changes of phi'; Q > 0 gives none and min phi' > 0", ok,
          f"Q=0: {n0} sign changes; Q>0: {n1} events, status {s1.status}, reached N {s1.t[-1]:.3f}, min phi_N {minphiN:.3e}")
    R["M_d"] = dict(sign_changes_Q0=n0, events_Qpos=n1, status=int(s1.status), N_end=float(s1.t[-1]), min_phiN=minphiN)
    ok = all(o_ for _, o_ in CHECKS)
    P(f"MUTATE overall: {'PASS' if ok else 'FAIL'}  ({sum(o_ for _, o_ in CHECKS)}/{len(CHECKS)})")
    R["pass"] = ok
    return R


# ============================================================================== main
if __name__ == "__main__":
    if MODE == "K":
        res = run_K()
        base = "cfg957_K"
    elif MODE == "MUTATE":
        res = run_MUTATE()
        base = "cfg957_MUTATE"
    else:
        res = run_MAIN()
        base = "cfg957"
    P("")
    P(f"done in {time.time() - T0:.0f} s. kappa = 1/2 FITTED; footings never pooled; not theory closed; the owner's idea (2026-10-21).")
    open(os.path.join(HERE, base + ".out"), "w").write("\n".join(OUT) + "\n")

    def conv(x):
        if isinstance(x, dict):
            return {str(k): conv(v) for k, v in x.items()}
        if isinstance(x, (list, tuple)):
            return [conv(v) for v in x]
        if isinstance(x, (np.floating,)):
            return float(x)
        if isinstance(x, (np.integer,)):
            return int(x)
        if isinstance(x, np.bool_):
            return bool(x)
        return x

    json.dump(conv(dict(mode=MODE, criteria="8e884c9a2b", checks=[dict(name=n, ok=o) for n, o in CHECKS], results=res,
                        note="the owner's idea (2026-10-21); kappa = 1/2 FITTED; footings never pooled")),
              open(os.path.join(HERE, base + ".json"), "w"), indent=1)
    sys.exit(0 if all(o for _, o in CHECKS) else 1)
