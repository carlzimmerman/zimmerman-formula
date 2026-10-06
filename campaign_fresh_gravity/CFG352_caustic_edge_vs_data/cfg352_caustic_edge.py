#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG346 -- CFG337's stable (smeared) switch edge against the data.  Criteria frozen first: FROZEN_CRITERIA.md (188df575b).

  object     inverted triggered symmetron (CFG337); f = f_in phi^2, phi = screened-Poisson smoothing (range lam = ell/sqrt(2 f_in))
             of B's sharp edge Theta(r_ta - r); f_in = 1 + 2/R (AS-DECLARED, the verdict level) or 1 (UNIT, reported).
             The phantom DENSITY is multiplied by f: M(r) = M_b + Int_0^r f dM_ph.
  configs    each CFG337 reader / E_c mode / R at ell_min (max over 1e5/1e6 K) and 1.5 ell_min.
  scores     K: KiDS isolated lenses (FP1 slice + FP20 projector, CFG4_switch K3 logic), d chi^2 <= +9 vs law, both footings.
             S: SPARC A3 at R_HI (CFG45 P3 rows) >= 90% with |d log v| < 0.03, spirals and dwarfs; rotmod RAR d rms < 0.005; both footings.
             G: f = 0 on linear FRW (delta << 1) for every ell; tail f(20 h^-1 Mpc comoving) <= 1.2e-3 for every system.
MUTATE    CFG346_MUTATE=1: ell = 10 ell_min (over-smeared) must fail K or S for the best configuration; outputs *_MUTATE.
CFG352 copy of CFG346 (sharp-edge path, turnaround radii x EDGE_FRAC). Run: python3 campaign_fresh_gravity/CFG352_caustic_edge_vs_data/cfg352_caustic_edge.py
"""
import os, sys, io, math, json, contextlib, time
EDGE_FRAC = 1.0  # CFG352: set per row below
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG7_common as C7                                                     # noqa: E402
import CFG4_common as C4                                                     # noqa: E402
sys.path.insert(0, os.path.join(C7.REPO, "hunt_2026"))
MUTATE = os.environ.get("CFG346_MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT, CHECKS = [], []


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, ok, detail=""):
    CHECKS.append(dict(name=name, ok=bool(ok), detail=detail)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}  {detail}")


P(__doc__.split("Run: python3")[0].strip())
FOOTS = ("canonical", "alt")
KPC_M = 3.0856775814913673e19
J337 = json.load(open(os.path.join(LANES, "CFG337_stable_switch_action", "cfg337_switch_results.json")))["numbers"]["transition"]
J4S = json.load(open(os.path.join(LANES, "CFG4_switch_results.json")))["numbers"]
DTA_025 = J4S["D1"]["0.25"]["one_plus_delta_ta"]
DTA_000 = J4S["D1"]["0.0"]["one_plus_delta_ta"]
H2B = {f: J4S["H2b"]["d_chi2"][f"{f}|nu_mono|turnaround|A0"] for f in FOOTS}

# ------------------------------------------------------------------------------------------------ configurations
CONSTS = {"C1": "mu0 (ell), E_c (R), + DE12 gate width w and Umax (inherited)", "C2": "mu0 (ell), E_c (R), Delta_e"}
CONFIGS = []
for door in ("C1", "C2"):
    for R in (4, 40):
        for mode in ("local", "universal"):
            res = J337[door]["results"][f"R{R}/{mode}"]
            lm = max(res["1e5K/100kpc"]["ell_min_kpc"], res["1e6K/100kpc"]["ell_min_kpc"])
            n = (4 if door == "C1" else 3) - (1 if mode == "local" else 0)
            CONFIGS.append(dict(door=door, R=R, mode=mode, ell_min=lm, ratio100=max(res["1e5K/100kpc"]["ratio"], res["1e6K/100kpc"]["ratio"]),
                                n_const=n, consts=CONSTS[door] + ("; E_c LOCAL = a per-system function, not a constant" if mode == "local" else "")))
REP_ONLY = J337["C2"]["results"]["R4/local"]["1e6K/100kpc"]["ell_min_kpc"]
MULTS = (10.0,) if MUTATE else (1.0, 1.5)


# ------------------------------------------------------------------------------------------------ the smeared profile
def phi(r, a, lam):
    """screened-Poisson smoothing of Theta(a - r), range lam (same units); exact uniform-ball solution."""
    r = np.asarray(r, float)
    if lam <= 0:
        return (r <= a).astype(float)
    if not np.isfinite(a):
        return np.ones_like(r)
    A = a / lam
    x = np.maximum(r / lam, 1e-12)
    with np.errstate(over="ignore", invalid="ignore"):
        if A > 600:                                                 # overflow-safe forms
            ins = 1.0 - (1 + A) * np.exp(np.minimum(x - A, 0.0)) * (1 - np.exp(-2 * x)) / (2 * x)
            out = 0.5 * ((A - 1) + (A + 1) * np.exp(-2 * A)) * np.exp(np.minimum(A - x, 0.0)) / x
        else:
            ins = 1.0 - (1 + A) * np.exp(-A) * np.where(x < 1e-6, 1.0 + x * x / 6, np.sinh(np.minimum(x, 700)) / x)
            out = (A * math.cosh(A) - math.sinh(A)) * np.exp(-x) / x
    return np.clip(np.where(r <= a, ins, out), 0.0, 1.0)


def fprof(r, a, ell, fin):
    lam = ell / math.sqrt(2.0 * fin) if ell > 0 else 0.0
    return fin * phi(r, a, lam) ** 2


def smear_mass(r, Mb, Mlaw, a, ell, fin):
    """M(r) = M_b + Int_0^r f dM_ph on a radial grid r (M_ph = Mlaw - Mb, M_ph(0) = 0)."""
    if ell <= 0:                                                    # sharp: the CFG4_switch code path (density edge)
        if not np.isfinite(a):
            return Mb + fin * (Mlaw - Mb)
        Mt = np.interp(a, r, Mlaw)
        return Mb + fin * (np.where(r <= a, Mlaw, Mt) - Mb)
    Mph = np.concatenate([[0.0], np.asarray(Mlaw - Mb, float)])
    rr = np.concatenate([[0.0], r])
    f = fprof(rr, a, ell, fin)
    inc = 0.5 * (f[1:] + f[:-1]) * np.diff(Mph)
    return Mb + np.cumsum(inc)


# ================================================================================================ K: KiDS (CFG4_switch K3 logic, CFG340 copy)
t = time.time()
GK = {"np": np, "math": math, "os": os, "REPO": C4.REPO, "G_SI": 6.67430e-11, "_trap": C4._trap}
GK = C4.exec_slices(os.path.join(C4.CHAIN, "FP1_static_sector.py"),
                    [("# ---- KiDS: L355's machinery", "w0 = np.zeros(len(ES)); w0[0] = 1.0")], ns=GK, name="fp1_kids")[0]
FIX = C4.ESDFix(GK["rrK"], GK["Rp"], GK["PCm2"], GK["MS"])
RRK, RPK, MPCK, MSK = GK["rrK"], GK["Rp"], GK["MPCm"], GK["MS"]
LM, NPB = GK["LM"], GK["npb"]
W0 = np.zeros(len(GK["ES"])); W0[0] = 1.0
GN = 6.67430e-11
A0K = C4.A0
RHOM_ZL = GK["rho_m_z"] * MSK / C4.MPC ** 3                                   # as CFG4_switch (C.MPC)


def M_law(Mb, a0):
    return Mb * C4.nu_mono(GN * Mb / RRK ** 2 / a0)


def r_bound(M, Delta):
    """CFG4_switch r_bound (copied): first radius where the enclosed mean density falls to Delta rho_m(z_l)."""
    D = M / (4.0 / 3.0 * math.pi * RRK ** 3 * RHOM_ZL)
    k = np.where(D < Delta)[0]
    if not len(k) or k[0] == 0:
        return RRK[-1] if not len(k) else RRK[0]
    i = k[0]
    return EDGE_FRAC * float(math.exp(np.interp(math.log(Delta), [math.log(D[i]), math.log(D[i - 1])], [math.log(RRK[i]), math.log(RRK[i - 1])])))


def kids_chi2(Mfun, foot):
    T = np.zeros((len(GK["ES"]), len(LM), 4, NPB))
    for im, lm in enumerate(LM):
        Mb = 10 ** lm * MSK
        dS = FIX(Mfun(Mb, A0K[foot]), Mb)
        T[0, im] = [np.interp(GK["Rd"][b], RPK / MPCK, dS) for b in range(4)]
    return GK["kfit"]({foot: T}, foot, W0, 0.0)[0]


def M_sw(ell_m, fin, edge=True):
    def f_(Mb, a0):
        Ml = M_law(Mb, a0)
        a = r_bound(Ml, DTA_025) if edge else np.inf
        return smear_mass(RRK, Mb, Ml, a, ell_m, fin)
    return f_


KBASE = {f: kids_chi2(M_law, f) for f in FOOTS}
P(f"\n  KiDS machinery exec'd ({time.time() - t:.0f} s): law chi^2 {KBASE['canonical']:.4f} / {KBASE['alt']:.4f}")
RTA_K = {f: [r_bound(M_law(10 ** lm * MSK, A0K[f]), DTA_025) / MPCK for lm in (10.0, 10.5, 11.0, 11.5)] for f in FOOTS}
P(f"  KiDS-like lenses r_ta (Mpc, log M_b 10/10.5/11/11.5): can {[round(x, 3) for x in RTA_K['canonical']]}, alt {[round(x, 3) for x in RTA_K['alt']]}")


def score_K(ell_kpc, fin):
    d = {f: kids_chi2(M_sw(ell_kpc * KPC_M, fin), f) - KBASE[f] for f in FOOTS}
    return all(v <= 9.0 for v in d.values()), d


# ================================================================================================ S: SPARC (CFG45 prefix + CFG4_galaxy_law prefix, CFG340 copy)
def quiet_exec(code, ns, name):
    _e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(code, name, "exec"), ns)
    os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
    return ns


t = time.time()
SRC45 = open(os.path.join(LANES, "CFG45_rule_readings.py")).read()
SRC45 = SRC45[:SRC45.index('R.banner("C1  CONTROLS: (S) and (L) against the lanes\' committed results")')]
assert SRC45.count('READ = ("L", "S", "M", "E")') == 1
SRC45 = SRC45.replace('READ = ("L", "S", "M", "E")', 'READ = ("L",)')
NS = quiet_exec(SRC45, {"__file__": os.path.join(LANES, "CFG45_rule_readings.py"), "__name__": "cfg45_ro"}, "CFG45_ro")
G_, KPC, MSUN, A0SI, NU = NS["G_"], NS["KPC"], NS["MSUN"], NS["A0SI"], NS["NU"]
MASTER = NS["g10"]["read_master"]()
NUV = lambda y: np.asarray(C7.nu_mono(np.asarray(y, float)), float)            # vectorised; checked equal to CFG45's NU below
_yy = np.geomspace(1e-6, 1e3, 40)
assert max(abs(NUV(v) - NU(float(v))) / NU(float(v)) for v in _yy) < 1e-9, "CFG45 NU != nu_mono"

OMH2 = 0.02237 + 0.1200
RHO_M0 = 3 * (100e3 / (1e3 * KPC)) ** 2 * OMH2 / (8 * math.pi * G_)           # kg/m^3 at z = 0
RG = np.geomspace(0.05, 2.0e5, 3000) * KPC                                    # radial grid [m] for the SPARC point-mass profiles


def r_ta_point(Mb_kg, a0):
    Ml = Mb_kg * NUV(G_ * Mb_kg / RG ** 2 / a0)
    D = Ml / (4.0 / 3.0 * math.pi * RG ** 3 * RHO_M0)
    i = int(np.where(D < DTA_000)[0][0])
    return EDGE_FRAC * float(math.exp(np.interp(math.log(DTA_000), [math.log(D[i]), math.log(D[i - 1])], [math.log(RG[i]), math.log(RG[i - 1])]))), Ml


SPROWS = []
for name, m in MASTER.items():
    Ms = 0.61 * m["L36"] * 1e9; Mb = Ms + 1.33 * m["MHI"] * 1e9
    if Ms <= 0 or m["RHI"] <= 0:
        continue
    SPROWS.append(dict(name=name, Ms=Ms, Mb=Mb, r=m["RHI"], kind="dwarf" if math.log10(Ms) < 10.0 else "spiral"))
RTA_S = {f: {s["name"]: r_ta_point(s["Mb"] * MSUN, A0SI[f]) for s in SPROWS} for f in FOOTS}


def sparc_a3(kind, foot, ell_kpc, fin):
    dv = []
    for s in SPROWS:
        if s["kind"] != kind:
            continue
        a, Ml = RTA_S[foot][s["name"]]
        Mb = s["Mb"] * MSUN
        Msm = smear_mass(RG, Mb, Ml, a, ell_kpc * KPC, fin)
        r = s["r"] * KPC
        dv.append(0.5 * math.log10(float(np.interp(r, RG, Msm)) / float(np.interp(r, RG, Ml))))
    dv = np.abs(np.array(dv))
    return float(np.mean(dv < 0.03)), float(dv.max()), len(dv)


t = time.time()
g4, _ = C4.exec_slices(os.path.join(LANES, "CFG4_galaxy_law.py"), [(None, 'banner("K  CONTROLS')], name="cfg4_galaxy_ro")
GAL4, UPS, Rm, GB, GO, OK, WW, GI = (g4[k] for k in ("GAL", "UPS", "Rm", "GB", "GO", "OK", "WW", "GI"))
iu = int(np.argmin(np.abs(UPS - 0.61)))
gb4, go4, ok4, ww4 = GB[:, iu], GO[:, iu], OK[:, iu], WW[:, iu]
GPRED = {f: np.where(ok4, np.asarray(C7.nu_mono(np.where(ok4, gb4, 1.0) / C7.A0_SI[f]), float) * np.where(ok4, gb4, 1.0), 1.0) for f in FOOTS}
GSI, MSI = 6.67430e-11, 1.98847e30
GMB = {}
for i, g in enumerate(GAL4):
    m = g.get("meta") or {}
    if m and m.get("L36", 0) > 0:
        GMB[i] = (0.61 * m["L36"] * 1e9 + 1.33 * m.get("MHI", 0.0) * 1e9) * MSI


def rms(gp):
    r1 = np.log10(np.where(ok4, go4, 1.0)) - np.log10(gp)
    return float(np.sqrt(np.sum(ww4 * r1 ** 2) / np.sum(ww4)))


RMS0 = {f: rms(GPRED[f]) for f in FOOTS}
RTA_G = {f: {i: r_ta_point(Mb, C7.A0_SI[f])[0] for i, Mb in GMB.items()} for f in FOOTS}
P(f"  SPARC harnesses exec'd ({time.time() - t:.0f} s): {len(SPROWS)} P3 rows, {len(GAL4)} rotmod galaxies; rms0 {RMS0['canonical']:.6f} / {RMS0['alt']:.6f}")
rt_med = {f: float(np.median([v[0] for v in RTA_S[f].values()]) / KPC) for f in FOOTS}
P(f"  SPARC r_ta (z = 0, point-mass law mass): median {rt_med['canonical']:.0f} / {rt_med['alt']:.0f} kpc")


def sparc_rms_sw(foot, ell_kpc, fin):
    gp = GPRED[foot].copy()
    for i, Mb in GMB.items():
        sel = np.where((GI == i) & ok4)[0]
        if not len(sel):
            continue
        o = np.argsort(Rm[sel]); sel = sel[o]
        rr = Rm[sel]                                                     # m
        Mph = np.maximum(gp[sel] - gb4[sel], 0.0) * rr ** 2 / GSI
        a = RTA_G[foot][i]
        f = fprof(np.concatenate([[0.0], rr]), a, ell_kpc * KPC, fin)          # ell = 0 -> fin Theta (sharp)
        Msm = np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(np.concatenate([[0.0], Mph])))
        gp[sel] = gb4[sel] + GSI * Msm / rr ** 2
    return rms(gp)


def score_S(ell_kpc, fin):
    a3 = {(k, f): sparc_a3(k, f, ell_kpc, fin) for k in ("spiral", "dwarf") for f in FOOTS}
    dr = {f: sparc_rms_sw(f, ell_kpc, fin) - RMS0[f] for f in FOOTS}
    ok_a3 = all(v[0] >= 0.90 for v in a3.values())
    ok_rms = all(abs(v) < 0.005 for v in dr.values())
    return ok_a3 and ok_rms, dict(a3={f"{k[0]}|{k[1]}": v[0] for k, v in a3.items()}, a3_ok=ok_a3, drms=dr, rms_ok=ok_rms)


# ================================================================================================ G: growth leak
R20 = 20.0 / 0.6736 * 1e3 * KPC                                              # 20 h^-1 Mpc comoving at z = 0 [m]
R20_K = R20 / 1.25                                                           # physical at the KiDS z_l = 0.25


def score_G(ell_kpc, fin):
    # G1: delta << 1 random field: U = (1 + delta)/Delta_e < 1 -> T < 0 -> no source -> sigma = 0 (any ell)
    rng = np.random.default_rng(346)
    delta = 1e-2 * rng.standard_normal(200000)
    Uc2 = (1 + delta) / DTA_000                                            # C2 leaf threshold at the turnaround contrast
    T = 1 - 1 / Uc2
    src = np.where(T > -2.0 / 4.0, 1.0, 0.0)                               # broken phase needs T > -2/R (R >= 4 most lenient)
    g1 = bool(src.max() == 0.0 and np.all(T < 0))
    # G2: tail at 20 h^-1 Mpc from every KiDS / SPARC system
    tails = []
    for f in FOOTS:
        for lm in (10.0, 10.5, 11.0, 11.5):
            a = r_bound(M_law(10 ** lm * MSK, A0K[f]), DTA_025)
            tails.append(float(fprof(np.array([R20_K]), a, ell_kpc * KPC_M, fin)[0]))
        for nm, (a, _) in RTA_S[f].items():
            tails.append(float(fprof(np.array([R20]), a, ell_kpc * KPC, fin)[0]))
    tmax = max(tails)
    return g1 and tmax <= 1.2e-3, dict(G1_off_on_linear_FRW=g1, max_U_linear=float(Uc2.max()), tail_max_20hMpc=tmax)



# ================================================================================================ CFG352 rows
import json as _json
MUT = os.environ.get("CFG352_MUTATE", "0") == "1"
ROWS = (0.05,) if MUT else (1.0, 0.359, 0.232)
OUT352 = {"lane": "CFG352", "mutate": MUT, "rows": {}}
for ef in ROWS:
    EDGE_FRAC = ef
    RTA_S.clear(); RTA_S.update({f: {s_["name"]: r_ta_point(s_["Mb"] * MSUN, A0SI[f]) for s_ in SPROWS} for f in FOOTS})
    RTA_G.clear(); RTA_G.update({f: {i_: r_ta_point(Mb_, C7.A0_SI[f])[0] for i_, Mb_ in GMB.items()} for f in FOOTS})
    okK, dK = score_K(0.0, 1.0); okS, dS = score_S(0.0, 1.0); okG, dG = score_G(0.0, 1.0)
    OUT352["rows"][str(ef)] = {"kids": dK, "kids_ok": okK, "sparc": dS, "sparc_ok": okS, "growth": dG, "growth_ok": okG}
    P(f"\nCFG352 EDGE_FRAC {ef}: KiDS dchi2 {dK['canonical']:+.2f} / {dK['alt']:+.2f} ({'pass' if okK else 'FAIL'}); SPARC A3 {dS['a3']} drms {dS['drms']} ({'pass' if okS else 'FAIL'}); growth {'pass' if okG else 'FAIL'}")
if not MUT:
    r = OUT352["rows"]["0.232"]; n = sum([r["kids_ok"], r["sparc_ok"], r["growth_ok"]])
    OUT352["verdict"] = "PASS" if n == 3 else ("PARTIAL" if n == 2 else "FAIL")
    P(f"\nCFG352 VERDICT (edge 0.232 r_ta): {OUT352['verdict']}")
H = os.path.dirname(os.path.abspath(__file__))
_json.dump(OUT352, open(os.path.join(H, "cfg352_caustic_edge" + ("_MUTATE" if MUT else "") + "_results.json"), "w"), indent=1, default=str)
