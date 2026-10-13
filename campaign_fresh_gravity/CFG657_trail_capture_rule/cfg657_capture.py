#!/usr/bin/env python3
"""CFG657: a derived cold-energy capture rule for the NGC 1052 trail (DF2, DF4, DF9) and LEDA 4014647.

Criteria: FROZEN_CRITERIA.md (committed alone, 20d95b0d1). One process, seconds, no downloads.
MUTATE=1: M1 (V_coll -> 0 must give full supply) and M2 (cold energy -> 0 must give none); separate outputs.
kappa = 1/2 fitted; cold energy mass required; not theory closed.
"""
import itertools, json, math, os, sys
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import erf

MUTATE = os.environ.get("MUTATE", "0") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
TAG = "_MUTATE" if MUTATE else ""

GK = 4.30091e-6            # kpc (km/s)^2 / Msun
KPC_M = 3.0857e19
GYR = 0.97779              # 1 kpc/(km/s) in Gyr
RATIO = 5.364              # Omega_c/Omega_b (A3)
FOOTS = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0K = {k: v * KPC_M / 1e6 for k, v in FOOTS.items()}   # (km/s)^2 / kpc
LN_EDGE = math.log(1.0 + 1.0 / RATIO)                   # CFG541 T2a point-mass edge, f_ret = 1


# ---- the record's XC4 repaired kernel (copied from CFG655 / CFG5_common.nu_mono)
def _h_rar(y):
    z = np.sqrt(y); return y / np.expm1(z)


_dh = lambda t: (2 * np.expm1(math.sqrt(t)) - math.sqrt(t) * (1 + np.expm1(math.sqrt(t)))) / (2 * np.expm1(math.sqrt(t)) ** 2)
_YP = brentq(_dh, 1.0, 5.0); _HP = _h_rar(_YP); _DELTA = 0.05
_YS = brentq(lambda t: _dh(t) - _DELTA * _HP / (t + _YP), 1.0, _YP)


def nu_mono(y):
    y = float(y)
    h = _h_rar(max(y, 1e-300)) if y <= _YS else _h_rar(_YS) + _DELTA * _HP * math.log((y + _YP) / (_YS + _YP))
    return 1.0 + h / y


# ---- inputs (FROZEN_CRITERIA.md)
GAL = {  # CFG655 frozen table + vD+22 Table 1 positions
    "DF2":  dict(Ms=2.0e8, eMs=0.20, Re=2.0, Dref=20.0, D=20.0, obs=(8.5, 2.3, 3.1), pos=(40.4451, -8.4028), age=(8.28, 2.07, 1.41)),
    "DF4":  dict(Ms=1.5e8, eMs=0.27, Re=1.6, Dref=20.0, D=20.0, obs=(6.3, 2.5, 1.6), pos=(39.8128, -8.1160), age=(10.68, 1.38, 1.51)),
    "DF9":  dict(Ms=1.4e8, eMs=0.23, Re=1.1, Dref=20.6, D=20.6, obs=(6.5, 3.9, 4.3), pos=(40.0292, -8.2290), age=(10.36, 1.61, 1.95)),
    "LEDA": dict(Ms=10 ** 7.98, eMs=10 ** 0.06 - 1, Re=0.601, Dref=17.7, D=17.7, obs=(15.8, 2.0, 2.0), pos=(39.7021, -8.0494), age=(11.54, 1.12, 1.69)),
}
LABEL655 = {"DF2": "E", "DF4": "E", "DF9": "E", "LEDA": "T"}
BOUND655 = {"DF2": {"canonical": 0.36, "alt": 0.33}, "DF4": {"canonical": 0.29, "alt": 0.26}, "DF9": {"canonical": 0.52, "alt": 0.46}}
HOSTS = {"NGC1052": (40.2700, -8.2558), "NGC1035": (39.8713, -8.1328)}

PRIMARY = dict(Rfac=1.0, Vcoll=358.0, t=8.0, Mp=1e9, Mg=1e11, M35=5e9, k=1.0, X=1.0, alpha=1.0)
BRACKET = dict(Rfac=(0.5, 1.0), Vcoll=(250.0, 450.0), t=(6.0, 9.0), Mp=(3e8, 1e10), Mg=(5e10, 3e11), M35=(3e9, 1e10),
               k=(1.0, 3.0), X=(1.0, 2.0), alpha=(0.5, 2.0))


def angsep(p, q):
    ra1, d1, ra2, d2 = map(math.radians, (p[0], p[1], q[0], q[1]))
    c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(ra1 - ra2)
    return math.acos(min(1.0, c))


def host_halo(Mb, a0):
    Vf = (GK * Mb * a0) ** 0.25
    rM = math.sqrt(GK * Mb / a0)
    return Vf, rM / LN_EDGE


def vesc_host(Mb, a0, r):
    Vf, rs = host_halo(Mb, a0)
    if r >= rs:
        return math.sqrt(2 * GK * (1 + RATIO) * Mb / r)
    return math.sqrt(2 * (Vf ** 2 * math.log(rs / r) + GK * (1 + RATIO) * Mb / rs))


def maxwell_cdf(v, s):           # P(|u| < v), isotropic 3-D Maxwellian with 1-D sigma s
    if s <= 0: return 1.0
    x = v / s
    return float(erf(x / math.sqrt(2)) - math.sqrt(2 / math.pi) * x * math.exp(-x * x / 2))


def shifted_cdf(v, V, s):        # P(|V + u| < v), u isotropic Maxwellian (1-D sigma s), |V| = V
    if V < 1e-6 * max(s, 1e-30):
        return maxwell_cdf(v, s)
    f = lambda w: w / (V * s * math.sqrt(2 * math.pi)) * (math.exp(-(w - V) ** 2 / (2 * s * s)) - math.exp(-(w + V) ** 2 / (2 * s * s)))
    return min(1.0, quad(f, 0.0, v, limit=200)[0])


def dwarf(g, a0):
    f = g["D"] / g["Dref"]; M = g["Ms"] * f * f; rh = (4.0 / 3.0) * g["Re"] * f
    a = rh / 1.305
    gNh = GK * 0.5 * M / rh ** 2                # CFG655 estimator
    nuh = nu_mono(gNh / a0)
    Mtgt = (nuh - 1.0) * 0.5 * M
    ve0 = math.sqrt(2 * GK * M / a)
    rMd = math.sqrt(GK * M / a0)
    return dict(M=M, rh=rh, a=a, nuh=nuh, Mtgt=Mtgt, ve0=ve0, rstar=rMd / LN_EDGE, Sigma=0.5 * M / (math.pi * (g["Re"] * f) ** 2))


def capture(name, foot, P, coldfac=1.0):
    """Upper-bound captured fraction f_cap of the law target inside r_1/2 (FROZEN_CRITERIA, channels S, F, D)."""
    g = GAL[name]; a0 = A0K[foot]; d = dwarf(g, a0)
    D = g["D"]
    # ambient field: settled halos of NGC 1052 and NGC 1035 superposed, continued isothermally (k for unsettled)
    rho_amb = 0.0; sig = []; Rg = None
    for h, Mh in (("NGC1052", P["Mg"]), ("NGC1035", P["M35"])):
        R = max(P["Rfac"] * D * 1000 * angsep(g["pos"], HOSTS[h]), 1.0)
        Vf, _ = host_halo(Mh, a0)
        rho_amb += P["k"] * Vf ** 2 / (4 * math.pi * GK * R ** 2)
        sig.append(Vf / math.sqrt(2))
        if h == "NGC1052": Rg, Vg = R, Vf
    rho_amb *= coldfac
    s_amb = min(sig)
    Mg_in = Vg ** 2 * Rg / GK
    RJ = Rg * (d["nuh"] * d["M"] / (2 * Mg_in)) ** (1 / 3)
    Rc = min(RJ, d["rstar"])
    # --- S: separation retention with the progenitor fallback test
    Vsh = 0.5 * P["Vcoll"]
    vep = vesc_host(P["Mp"], a0, d["rh"])
    Vfp, _ = host_halo(P["Mp"], a0); sp = Vfp / math.sqrt(2)
    fallback = Vsh < vep
    Pcos = coldfac * P["X"] * RATIO * d["M"]
    if fallback:
        MS = Pcos; PS = 1.0
    else:
        PS = shifted_cdf(d["ve0"], Vsh, sp); MS = Pcos * PS
    # --- F: sudden capture at formation
    PF = maxwell_cdf(d["ve0"], s_amb)
    MF = rho_amb * (4 * math.pi / 3) * Rc ** 3 * PF
    # --- D: Gould-type capture with the CFG541 drift as the dissipation
    M, a = d["M"], d["a"]
    def integrand(r):
        gN = GK * M * r / (r * r + a * a) ** 1.5
        rho_b = 3 * M / (4 * math.pi * a ** 3) * (1 + r * r / (a * a)) ** -2.5
        tau = (4 * math.pi * GK * (rho_b + rho_amb + 1e-300)) ** -0.5
        nu = nu_mono(max(gN, 1e-300) / a0)
        return gN * P["alpha"] * tau * (nu - 1.0) * gN
    I = quad(integrand, 0.0, Rc, limit=400, points=[a])[0]        # (km/s)^3
    ve = d["ve0"]
    if I > 0:
        umax = brentq(lambda u: u * u * math.sqrt(u * u + ve * ve) - 4 * I, 0.0, max(1e3, 10 * (4 * I) ** (1 / 3)))
    else:
        umax = 0.0
    if rho_amb > 0 and umax > 0:
        fM = lambda u: (2 * math.pi * s_amb ** 2) ** -1.5 * math.exp(-u * u / (2 * s_amb ** 2))
        flux = quad(lambda u: 4 * math.pi * u * u * fM(u) * u * (1 + ve * ve / (u * u)) if u > 0 else 0.0, 0.0, umax, limit=200)[0]
        Mdot = rho_amb * math.pi * Rc ** 2 * flux               # Msun per kpc/(km/s)
        MD = Mdot * P["t"] / GYR
    else:
        MD = 0.0
    fcap = min(1.0, (MS + MF + MD) / d["Mtgt"])
    fcap_strict = min(1.0, MS / d["Mtgt"])
    return dict(fcap=fcap, fcap_A6strict=fcap_strict, fS=MS / d["Mtgt"], fF=MF / d["Mtgt"], fD=MD / d["Mtgt"],
                fallback=bool(fallback), Vshift=Vsh, vesc_p=vep, sigma_p=sp, P_S=PS, P_F=PF, umax_D=umax, I_D=I,
                rho_amb=rho_amb, sigma_amb=s_amb, R_NGC1052=Rg, R_J=RJ, rstar_d=d["rstar"], R_c=Rc,
                vesc_d0=d["ve0"], nu_half=d["nuh"], M_tgt=d["Mtgt"], M_b=d["M"], r_half=d["rh"], Sigma_e=d["Sigma"])


# ---- CFG655 estimator for f thresholds (sigma used only for scoring)
def sig_pred(name, foot, fs):
    g = GAL[name]; a0 = FOOTS[foot]; G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19
    out = []
    for Mfac in (1.0, 1.0 + g["eMs"]):
        f = g["D"] / g["Dref"]; Mb = g["Ms"] * f * f * Mfac; r = (4 / 3) * g["Re"] * f * KPC
        gN = G * 0.5 * Mb * MSUN / r ** 2
        nu = 1.0 + fs * (nu_mono(gN / a0) - 1.0)
        out.append(math.sqrt(nu * gN * r / 3.0) / 1e3)
    return out[0], abs(out[1] - out[0])


def zf(name, foot, fs):
    s, up, lo = GAL[name]["obs"]; sp, ep = sig_pred(name, foot, fs)
    e = up if sp > s else lo
    return (s - sp) / math.sqrt(e * e + ep * ep)


def f_at_Z(name, foot, Z):
    h = lambda f: zf(name, foot, f) - Z
    if h(0.0) * h(1.0) > 0:
        return float("nan") if h(0.0) < 0 else float("inf")
    return brentq(h, 0.0, 1.0)


lines = []
def Pr(s=""):
    print(s); lines.append(s)


NAMES = list(GAL)
RES = {"primary": {}, "corners": {}, "scan": {}, "thresholds": {}, "alpha": {}, "verdict": {}}
Pr("CFG657  derived cold-energy capture rule: NGC 1052 trail + LEDA 4014647" + ("   [MUTATE]" if MUTATE else ""))
Pr("upper-bound channels S (separation, fallback test), F (sudden capture), D (Gould + CFG541 drift); f_cap of the law target in r_1/2")

if MUTATE:
    out = {}
    ok = True
    for foot in FOOTS:
        for n in NAMES:
            P1 = dict(PRIMARY, Vcoll=1e-6); c1 = capture(n, foot, P1)
            c2 = capture(n, foot, dict(PRIMARY, k=0.0), coldfac=0.0)
            m1 = bool(abs(c1["fcap"] - 1.0) < 1e-12); m2 = bool(c2["fcap"] == 0.0)
            ok &= m1 and m2
            out[f"{foot}:{n}"] = dict(M1_fcap=c1["fcap"], M1_fallback=c1["fallback"], M2_fcap=c2["fcap"], M1_ok=m1, M2_ok=m2)
            Pr(f"{foot:9s} {n:5s}  M1 (V_coll->0): f_cap = {c1['fcap']:.6f} fallback={c1['fallback']}  [{'ok' if m1 else 'FAIL'}]   "
               f"M2 (cold energy->0): f_cap = {c2['fcap']:.3g}  [{'ok' if m2 else 'FAIL'}]")
    Pr("MUTATE: " + ("both teeth behave (M1 full supply, M2 none) on both footings" if ok else "a tooth FAILED -> construction failure"))
    json.dump(out, open(os.path.join(HERE, f"cfg657_capture{TAG}_results.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg657_capture{TAG}.out"), "w").write("\n".join(lines) + "\n")
    sys.exit(0 if ok else 2)

# ---- thresholds from CFG655's estimator
for foot in FOOTS:
    # Correction 1 (README): Z = (obs - pred)/e, so the E upper bound on f is at Z = -2 (pred = obs + 2 e_up) and LEDA's
    # lower bound on f is at Z = +2 (pred = obs - 2 e_lo); the frozen text wrote the two signs the other way round.
    RES["thresholds"][foot] = {n: dict(f_max_E=f_at_Z(n, foot, -2.0), f_min_T=f_at_Z(n, foot, +2.0)) for n in NAMES}
Pr(""); Pr("thresholds from the CFG655 estimator (E: largest f with Z >= -2; LEDA: smallest f with Z <= +2)")
for foot in FOOTS:
    t = RES["thresholds"][foot]
    Pr(f"  {foot:9s} f_max: DF2 {t['DF2']['f_max_E']:.3f}  DF4 {t['DF4']['f_max_E']:.3f}  DF9 {t['DF9']['f_max_E']:.3f}   "
       f"LEDA f_min = {t['LEDA']['f_min_T']:.3f}")

# ---- primary
for foot in FOOTS:
    Pr(""); Pr(f"=== {foot}  a0 = {FOOTS[foot]:.4e} m/s^2  (primary inputs)")
    Pr(f"{'gal':5s} {'M_b':>8s} {'r1/2':>5s} {'Sig_e':>7s} {'vesc_d0':>7s} {'nu':>5s} | {'Vsh':>5s} {'vesc_p':>6s} fb | "
       f"{'R_1052':>6s} {'R_c':>6s} {'rho_amb':>8s} {'sig_a':>5s} | {'f_S':>9s} {'f_F':>9s} {'f_D':>9s} | {'f_cap':>9s}")
    RES["primary"][foot] = {}
    for n in NAMES:
        c = capture(n, foot, PRIMARY); RES["primary"][foot][n] = c
        Pr(f"{n:5s} {c['M_b']:8.2e} {c['r_half']:5.2f} {c['Sigma_e']:7.2e} {c['vesc_d0']:7.2f} {c['nu_half']:5.2f} | {c['Vshift']:5.0f} "
           f"{c['vesc_p']:6.1f} {'Y' if c['fallback'] else 'n'}  | {c['R_NGC1052']:6.1f} {c['R_c']:6.2f} {c['rho_amb']:8.2e} {c['sigma_amb']:5.1f} | "
           f"{c['fS']:9.2e} {c['fF']:9.2e} {c['fD']:9.2e} | {c['fcap']:9.2e}")

# ---- bracket: every combination of bracket endpoints (2^9), max and min f_cap per galaxy
keys = list(BRACKET)
for foot in FOOTS:
    best = {n: (-1, None) for n in NAMES}; worst = {n: (9, None) for n in NAMES}
    for combo in itertools.product(*[BRACKET[k] for k in keys]):
        Pc = dict(zip(keys, combo))
        for n in NAMES:
            f = capture(n, foot, Pc)["fcap"]
            if f > best[n][0]: best[n] = (f, Pc)
            if f < worst[n][0]: worst[n] = (f, Pc)
    RES["corners"][foot] = {n: dict(fmax=best[n][0], at_max=best[n][1], fmin=worst[n][0], at_min=worst[n][1],
                                    detail_max=capture(n, foot, best[n][1])) for n in NAMES}
    Pr(""); Pr(f"=== {foot}: bracket corners (all 512 endpoint combinations)")
    for n in NAMES:
        b = RES["corners"][foot][n]; dm = b["detail_max"]
        Pr(f"  {n:5s} f_cap range [{b['fmin']:.2e}, {b['fmax']:.2e}]   at max: f_S {dm['fS']:.2e} f_F {dm['fF']:.2e} f_D {dm['fD']:.2e} "
           f"fallback={dm['fallback']}  ({', '.join(f'{k}={v:g}' for k, v in b['at_max'].items())})")

# ---- one-at-a-time scan (from primary)
for foot in FOOTS:
    RES["scan"][foot] = {}
    for k in keys:
        RES["scan"][foot][k] = {n: [capture(n, foot, dict(PRIMARY, **{k: v}))["fcap"] for v in BRACKET[k]] for n in NAMES}

# ---- alpha needed to reach the E bounds / LEDA f_min at primary (other inputs primary)
def alpha_needed(n, foot, target):
    f = lambda la: capture(n, foot, dict(PRIMARY, alpha=10 ** la))["fcap"] - target
    if f(-3) > 0: return 0.0
    if f(12) < 0: return float("inf")
    return 10 ** brentq(f, -3, 12, xtol=1e-3)
for foot in FOOTS:
    th = RES["thresholds"][foot]
    RES["alpha"][foot] = {n: alpha_needed(n, foot, BOUND655[n]["alt"] if n != "LEDA" else th["LEDA"]["f_min_T"]) for n in NAMES}
Pr(""); Pr("alpha at which f_cap reaches the E alt bound (DF2/DF4/DF9) or LEDA's f_min (others primary):")
for foot in FOOTS:
    Pr(f"  {foot:9s} " + "  ".join(f"{n} {RES['alpha'][foot][n]:.3g}" for n in NAMES))

# ---- verdict
Pr(""); Pr("=== VERDICT")
for foot in FOOTS:
    th = RES["thresholds"][foot]; fminL = th["LEDA"]["f_min_T"]
    prim = RES["primary"][foot]; cor = RES["corners"][foot]
    E_prim = all(prim[n]["fcap"] <= BOUND655[n]["alt"] for n in ("DF2", "DF4", "DF9"))
    E_up = all(cor[n]["fmax"] <= BOUND655[n]["alt"] for n in ("DF2", "DF4", "DF9"))
    L_prim = prim["LEDA"]["fcap"] >= fminL; L_up = cor["LEDA"]["fmax"] >= fminL
    if not E_prim: v = "FAIL (E side)"
    elif not E_up: v = "BRACKET-DEPENDENT (E side)"
    elif L_prim and L_up: v = "PASS"
    elif not L_up: v = "FAIL (LEDA not derived): E side DERIVED; LEDA NOT DERIVED"
    else: v = "FAIL (LEDA only at the all-upper corner)"
    RES["verdict"][foot] = dict(verdict=v, E_primary=E_prim, E_upper=E_up, LEDA_primary=L_prim, LEDA_upper=L_up, f_min_LEDA=fminL,
                                fcap_LEDA_upper=cor["LEDA"]["fmax"], fcap_E_upper={n: cor[n]["fmax"] for n in ("DF2", "DF4", "DF9")})
    Pr(f"{foot:9s}: {v}   (E within alt bounds: primary {E_prim}, all-upper {E_up}; LEDA f_cap max {cor['LEDA']['fmax']:.2e} vs f_min {fminL:.3f})")

# ---- KNOB label (frozen rule: alpha flipping the verdict inside [0.5, 2]) and the alpha window that reproduces all four
Pr("")
for foot in FOOTS:
    sc = RES["scan"][foot]; th = RES["thresholds"][foot]
    def ok(fs): return all(fs[n] <= BOUND655[n]["alt"] for n in ("DF2", "DF4", "DF9")) and fs["LEDA"] >= th["LEDA"]["f_min_T"]
    flips = [k for k in keys if any(not ok({n: sc[k][n][i] for n in NAMES}) for i in (0, 1))]
    al = RES["alpha"][foot]
    lo, hi = al["LEDA"], min(al["DF2"], al["DF4"], al["DF9"])
    knob = "alpha" in flips
    RES["verdict"][foot].update(flipping_inputs=flips, KNOB_alpha=knob, alpha_window=[lo, hi])
    Pr(f"{foot:9s}: inputs whose bracket end flips the four-label outcome: {flips}; alpha window reproducing all four "
       f"(others primary): [{lo:.3g}, {hi:.3g}]" + ("  -> KNOB (alpha)" if knob else ""))

HEAD = {f: RES["verdict"][f]["verdict"] + ("; KNOB (alpha)" if RES["verdict"][f]["KNOB_alpha"] else "") for f in FOOTS}
RES["headline"] = HEAD
Pr("HEADLINE: " + "; ".join(f"{f}: {v}" for f, v in HEAD.items()))

# ---- fallback thresholds: progenitor mass above which the gas stays bound to its own cold energy (V_coll = 358),
#      and collision speed below which it does (M_b,p = 1e9)
Pr(""); Pr("separation (channel S) fallback thresholds: gas re-bound to its own cold energy if V_coll/2 < v_esc,p(r_1/2)")
RES["fallback_threshold"] = {}
for foot in FOOTS:
    a0 = A0K[foot]; row = {}
    for n in NAMES:
        rh = dwarf(GAL[n], a0)["rh"]
        Mcrit = 10 ** brentq(lambda lm: vesc_host(10 ** lm, a0, rh) - 0.5 * PRIMARY["Vcoll"], 6, 13)
        Vcrit = 2 * vesc_host(PRIMARY["Mp"], a0, rh)
        row[n] = dict(Mp_crit=Mcrit, Vcoll_crit=Vcrit)
    RES["fallback_threshold"][foot] = row
    Pr(f"  {foot:9s} " + "  ".join(f"{n}: M_b,p < {row[n]['Mp_crit']:.2e} | V_coll > {row[n]['Vcoll_crit']:.0f}" for n in NAMES))

# ---- reported: what distinguishes LEDA physically; A6-strict; channel assignment by age (CFG655 Rule A, context)
Pr(""); Pr("LEDA 4014647 vs the trail dwarfs (canonical, primary): v_esc,d(0) and surface density Sigma_e (Msun/kpc^2)")
for n in NAMES:
    c = RES["primary"]["canonical"][n]
    Pr(f"  {n:5s} v_esc,d(0) {c['vesc_d0']:5.1f} km/s   Sigma_e {c['Sigma_e']:.2e}   f_cap {c['fcap']:.2e}   A6-strict {c['fcap_A6strict']:.2e}")
RES["A6strict_primary"] = {foot: {n: RES["primary"][foot][n]["fcap_A6strict"] for n in NAMES} for foot in FOOTS}

json.dump(RES, open(os.path.join(HERE, f"cfg657_capture{TAG}_results.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg657_capture{TAG}.out"), "w").write("\n".join(lines) + "\n")
Pr(""); Pr("kappa = 1/2 fitted; cold energy mass required; not theory closed.")
open(os.path.join(HERE, f"cfg657_capture{TAG}.out"), "w").write("\n".join(lines) + "\n")
