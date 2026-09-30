#!/usr/bin/env python3
"""CFG229 -- the PRE-FLIGHT (Q1): can the class-M sample separate FLAT from a0 ~ H(z) (or from the PROXY) at the class-M gas band plus a stated stellar band?
BLIND TO THE VELOCITIES BY CONSTRUCTION: reads only cfg229_inputs_static.csv (z, radii, stellar and gas masses, velocity ERRORS, inclinations); never opens the kinematics file (control C8 proves it).
Compilation; calibration-limited; not a detection.  LambdaCDM has no a0: the proxy is an effective-a0 PROXY.  kappa = 1/2 FITTED.  No sentence says the data favour a law.
Frozen criteria: FROZEN_CRITERIA.md here (5c131c037).  Run: python3 campaign_fresh_gravity/CFG229_class_m_gold/cfg229_preflight.py        (MUTATE=1: the truth labels FLAT and H(z) are swapped in the mocks)"""
import os, sys, math, json, time, subprocess, tempfile, shutil
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from scipy.integrate import quad
from scipy.special import i0e, i1e, k0e, k1e, j1

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
MUT = os.environ.pop("MUTATE", "").strip() == "1"
CHILD = os.environ.pop("CFG229_PF_CHILD", "") == "1"                    # the blindness control re-runs this script without the kinematics file
JSON_OUT = os.environ.pop("CFG229_PF_JSON", os.path.join(LANE, "cfg229_preflight_results" + ("_MUTATE" if MUT else "") + ".json"))
sys.path.insert(0, CFG)
import CFG4_common as K
sys.path.insert(0, os.path.join(REPO, "sonnet55_push", "puzzle_32pi", "agents", "Z1_causal_horizon_a0z"))
import zcommon as Z1                                                   # READ-ONLY: lcdm_native

OUT, CHK = [], []
T0 = time.time()
G2SI = 1e6 / 3.0856775814913673e19                                      # (km/s)^2 per kpc -> m/s^2
G_KPC = 4.30091e-6                                                      # kpc (km/s)^2 / Msun
XN = 1.678
OM = 0.315
SEED = 229
NU, A0 = K.nu_mono, K.A0["canonical"]
B_GAS, B_STAR = 0.093, 0.30                                             # outer bands (class M gas; declared stellar)
IN_GAS = 0.03                                                           # inner gas band; inner stellar band = each source's 1 sigma
SIG_INT = 0.15


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + 1 - OM)


LAWS = {"FLAT": lambda z: 1.0, "PROXY": lambda z: Z1.lcdm_native(z), "H(z)": E}
TRUTHS = ("FLAT", "H(z)", "PROXY")


def disc_v2(M, Re, Rr):                                                 # thin exponential disc (Freeman), (km/s)^2; Re, Rr in kpc
    Rd = Re / XN
    y = Rr / (2 * Rd)
    return 2 * G_KPC * M / Rd * y ** 2 * (i0e(y) * k0e(y) - i1e(y) * k1e(y))


def gbar_fn(Ms, Mg, Re, R):                                             # m/s^2, one disc for stars + gas
    return disc_v2(Ms + Mg, Re, R) / R * G2SI


P(__doc__.split("Run:")[0].strip())
P(f"MUTATE = {'1 (truth labels FLAT and H(z) swapped in the mock generation)' if MUT else 'none'}")
ST = pd.read_csv(os.path.join(LANE, "cfg229_inputs_static.csv"))
n = len(ST)
gid = ST["gid"].tolist()
z = ST["z"].values
Ms0 = ST["Mstar"].values
Mg0 = 10 ** ST["logMgas_He"].values
Re, R = ST["Re_kpc"].values, ST["R_kpc"].values
e_st, e_gas = ST["e_logMstar_inner"].values, ST["e_logMH2"].values
sigV = ST["sigV_dex"].values
i_used, e_i = ST["i_used"].values, ST["e_i_used"].values
FL = {L: np.array([LAWS[L](float(x)) for x in z]) for L in LAWS}
P(f"\nstatic inputs: {n} galaxies {gid}; columns read: {len(ST.columns)}; the kinematics file is never opened")
gb0 = gbar_fn(Ms0, Mg0, Re, R)


def gtrue(gb, T):
    return gb * NU(gb / (A0 * FL[T]))


def delta(gobs, gb, L):
    return np.log10(gobs / (gb * NU(gb / (A0 * FL[L]))))


# ------------------------------------------------------------------ controls on the disc function (C3, C4)
P("\nCONTROLS ON THE DISC FORCE")
yy = np.linspace(0.2, 6, 4000)
# Freeman: V^2 = 4 pi G Sigma0 R_d y^2 [I0K0 - I1K1], Sigma0 = M/(2 pi R_d^2) => V^2 = 2 G M / R_d y^2 [...]; peak of y^2[...] is 0.1936 at y = 1.08 => V^2_peak = 0.3872 G M / R_d
pk = float(np.max(yy ** 2 * (i0e(yy) * k0e(yy) - i1e(yy) * k1e(yy)))) * 2
check("C3 Freeman's peak V^2 = 0.3872 G M/R_d to 0.003", f"{pk:.5f}", abs(pk - 0.3872) < 0.003)
far = gbar_fn(1e11, 0.0, 2.0, 1000.0) / (G_KPC * 1e11 / 1000.0 ** 2 * G2SI)
check("C3 far field g -> GM/r^2 at r = 500 R_d to 1e-4", f"ratio {far:.6f}", abs(far - 1) < 1e-4)


def g_hankel(M, Re_, R_):                                               # independent path: g_R = 2 pi G Sigma0 R_d^2 int_0^inf k J1(kR) (1 + k^2 R_d^2)^(-3/2) dk
    Rd = Re_ / XN
    S0 = M / (2 * math.pi * Rd ** 2)
    f = lambda k: k * j1(k * R_) * (1 + (k * Rd) ** 2) ** (-1.5)
    kmax = 400.0 / Rd
    val = 0.0
    edges = np.linspace(0, kmax, 4001)
    for a, b in zip(edges[:-1], edges[1:]):
        val += quad(f, a, b, limit=200)[0]
    return 2 * math.pi * G_KPC * S0 * Rd ** 2 * val                                                        # (km/s)^2 per kpc


dev = []
for i in range(n):
    Mi = Ms0[i] + Mg0[i]
    gh = g_hankel(Mi, Re[i], R[i]) * G2SI                                # m/s^2
    gc = gbar_fn(Ms0[i], Mg0[i], Re[i], R[i])
    dev.append(abs(gh / gc - 1))
check("C4 independent Hankel-transform disc force agrees with the Bessel closed form at the seven (R, R_d) (H12)", f"max relative difference {max(dev):.2e}", max(dev) < 1e-3)

# ------------------------------------------------------------------ mocks
rng = np.random.default_rng(SEED)
B = 1000
SETS = {"ALL7": list(range(n))}
SETS.update({gid[i]: [i] for i in range(n)})
SETS["ALPAKA5"] = [i for i in range(n) if gid[i].startswith("ALPAKA")]
SETS["BX610+ALESS"] = [i for i in range(n) if not gid[i].startswith("ALPAKA")]
TT = {"FLAT": "H(z)", "H(z)": "FLAT"} if MUT else {}                   # MUTATE: swap the generating truth of FLAT and H(z)


def draw_inc(size):
    out = np.zeros(size)
    for i in range(n):
        if not math.isfinite(e_i[i]):
            continue
        ii = rng.normal(i_used[i], e_i[i], size=size[0])
        for _ in range(60):
            bad = (ii < 5) | (ii > 85)
            if not bad.any():
                break
            ii[bad] = rng.normal(i_used[i], e_i[i], size=int(bad.sum()))
        out[:, i] = 2 * np.log10(np.sin(np.radians(ii)) / np.sin(np.radians(i_used[i])))
    return out


def noise(Bm):
    return dict(eV=rng.normal(0, 1, (Bm, n)) * sigV, einc=draw_inc((Bm, n)), eint=rng.normal(0, SIG_INT, (Bm, n)),
                est=rng.normal(0, 1, (Bm, n)) * e_st, eg=rng.normal(0, 1, (Bm, n)) * e_gas)


NZ = noise(B)
gb_obs_mock = gbar_fn(Ms0 * 10 ** NZ["est"], Mg0 * 10 ** NZ["eg"], Re, R)        # the analyst's baryons carry the random errors (same draws for every truth)


def mock_delta(T, NZ_, gb_obs, tau_g=0.0, tau_s=0.0):
    """delta_L (L in TRUTHS) of mocks generated from truth T; the TRUE baryons are the nominal ones shifted by (tau_g, tau_s) dex"""
    Tg = TT.get(T, T)
    gbt = gbar_fn(Ms0 * 10 ** tau_s, Mg0 * 10 ** tau_g, Re, R)
    lg = np.log10(gtrue(gbt, Tg)) + NZ_["eV"] + NZ_["einc"] + NZ_["eint"]
    go = 10 ** lg
    return {L: delta(go, gb_obs, L) for L in TRUTHS}, np.log10(gb_obs / A0)


def set_stats(D, ly, idx):
    m = np.median(D[:, idx], axis=1)
    if len(idx) >= 3:
        x = ly[:, idx]
        xc = x - x.mean(axis=1, keepdims=True)
        sl = (xc * (D[:, idx] - D[:, idx].mean(axis=1, keepdims=True))).sum(axis=1) / (xc ** 2).sum(axis=1)
    else:
        sl = np.full(D.shape[0], np.nan)
    return m, sl


# noise-free helpers
def nf_delta(Ttruth, tau_g, tau_s_vec, gbt_nominal=True, Tlaw="FLAT"):
    gbt = gbar_fn(Ms0, Mg0, Re, R)
    go = gtrue(gbt, TT.get(Ttruth, Ttruth))
    gba = gbar_fn(Ms0 * 10 ** tau_s_vec, Mg0 * 10 ** tau_g, Re, R)
    return delta(go, gba, Tlaw)


def corner_shifts(idx, kind):
    """noise-free set-median shift of delta_FLAT (truth FLAT) at the band corners; kind in outer, gas, star, inner"""
    out = []
    for sgn in (+1, -1):
        if kind == "outer":
            tg, ts = sgn * B_GAS, np.full(n, sgn * B_STAR)
        elif kind == "gas":
            tg, ts = sgn * B_GAS, np.zeros(n)
        elif kind == "star":
            tg, ts = 0.0, np.full(n, sgn * B_STAR)
        else:
            tg, ts = sgn * IN_GAS, sgn * e_st
        d = nf_delta("FLAT", tg, ts)
        out.append(float(np.median(d[idx])))
        if len(idx) >= 3:
            ly = np.log10(gbar_fn(Ms0 * 10 ** ts, Mg0 * 10 ** tg, Re, R) / A0)
            xc = ly[idx] - ly[idx].mean()
            out.append(float(((xc * (d[idx] - d[idx].mean())).sum()) / (xc ** 2).sum()))
    # out = [med+, slope+, med-, slope-] (or [med+, med-] for n < 3)
    if len(idx) >= 3:
        return dict(med=(out[0], out[2]), slope=(out[1], out[3]))
    return dict(med=(out[0], out[1]), slope=(float("nan"), float("nan")))


P("\nPRE-FLIGHT (mocks on the ACTUAL galaxies; sigma_int = 0.15 dex declared; 1,000 mocks per (set, truth), seed 229; descriptive of THIS sample, never a statement about a real galaxy)")
MD = {}
for T in TRUTHS:
    MD[T], LY = mock_delta(T, NZ, gb_obs_mock)
NF = {T: {L: nf_delta(T, 0.0, np.zeros(n), Tlaw=L) for L in TRUTHS} for T in TRUTHS}
RES = {}
rows = []
for sname, idx in SETS.items():
    stats = {T: {L: set_stats(MD[T][L], LY, idx) for L in TRUTHS} for T in TRUTHS}
    sd = float(np.std(stats["FLAT"]["FLAT"][0], ddof=1))
    sig_mock = {T: abs(float(np.median(stats[T]["FLAT"][0]))) for T in ("H(z)", "PROXY")}
    sig_nf = {T: abs(float(np.median(NF[T]["FLAT"][idx]))) for T in ("H(z)", "PROXY")}
    cs = {k: corner_shifts(idx, k) for k in ("outer", "gas", "star", "inner")}
    S = {k: max(abs(cs[k]["med"][0]), abs(cs[k]["med"][1])) for k in cs}
    S_half = 0.5 * abs(cs["outer"]["med"][0] - cs["outer"]["med"][1])
    rule = {}
    for T in ("H(z)", "PROXY"):
        rule[T] = dict(outer=bool(sig_mock[T] > S["outer"] + 2 * sd), gas_only=bool(sig_mock[T] > S["gas"] + 2 * sd), inner=bool(sig_mock[T] > S["inner"] + 2 * sd))
    # slope statistic
    if len(idx) >= 3:
        sl_sd = float(np.std(stats["FLAT"]["FLAT"][1], ddof=1))
        sl_sig = {T: abs(float(np.median(stats[T]["FLAT"][1]))) for T in ("H(z)", "PROXY")}
        sl_S = max(abs(cs["outer"]["slope"][0]), abs(cs["outer"]["slope"][1]))
        sl_rule = {T: bool(sl_sig[T] > sl_S + 2 * sl_sd) for T in ("H(z)", "PROXY")}
    else:
        sl_sd, sl_sig, sl_S, sl_rule = float("nan"), {"H(z)": float("nan"), "PROXY": float("nan")}, float("nan"), {"H(z)": False, "PROXY": False}
    # C6 planted-law recovery: the set-median delta under the TRUE law is within 2 SD of 0 in >= 90% of mocks; under the other laws it is offset by the noise-free amount to within 3 SD
    rec = {T: float(np.mean(np.abs(stats[T][T][0]) < 2 * sd)) for T in TRUTHS}
    off = {T: float(np.median(stats[T]["FLAT"][0]) - np.median(NF[T]["FLAT"][idx])) for T in ("H(z)", "PROXY")}
    RES[sname] = dict(n=len(idx), sd=sd, signal_mock=sig_mock, signal_noisefree=sig_nf, S=S, S_half=S_half, corner=cs, rule=rule, slope=dict(sd=sl_sd, signal=sl_sig, S=sl_S, rule=sl_rule), recovery=rec, offset_vs_noisefree=off)
    rows.append((sname, len(idx), sd, sig_mock["H(z)"], sig_nf["H(z)"], sig_mock["PROXY"], sig_nf["PROXY"], S["outer"], S["gas"], S["star"], S["inner"], S_half, rule))
P("\n  set            n     SD   signal H(z) [mock | noise-free]   signal PROXY [mock | noise-free]    S_outer  S_gas   S_star  S_inner  S_half   flat vs H(z): outer / gas-only / inner      flat vs PROXY: outer / gas-only / inner")
for sname, nn, sd, sh, shn, sp, spn, so, sg, ss, si, sh2, rule in rows:
    f = lambda d: " / ".join("POSSIBLE" if d[k] else "no" for k in ("outer", "gas_only", "inner"))
    P(f"  {sname:12s} {nn:2d}  {sd:.3f}   {sh:.3f} | {shn:.3f}                   {sp:.3f} | {spn:.3f}               {so:.3f}   {sg:.3f}   {ss:.3f}   {si:.3f}    {sh2:.3f}    {f(rule['H(z)']):36s}  {f(rule['PROXY'])}")
P("\n  second statistic, robust to a common baryon offset: within-set OLS slope of delta_FLAT against log10(y), y = g_bar/a0 (sets with n >= 3)")
for sname in ("ALL7", "ALPAKA5"):
    r = RES[sname]["slope"]
    P(f"    {sname}: SD {r['sd']:.3f}; signal H(z) {r['signal']['H(z)']:.3f}, PROXY {r['signal']['PROXY']:.3f}; systematic (outer corners) {r['S']:.3f}; rule: flat vs H(z) {'POSSIBLE' if r['rule']['H(z)'] else 'no'}, vs PROXY {'POSSIBLE' if r['rule']['PROXY'] else 'no'}")

# ------------------------------------------------------------------ marginalised run (systematics drawn, not applied at the corners)
P("\nMARGINALISED RUN (20,000 mocks per truth; one common tau_g ~ U(-0.093, +0.093) and one common tau_* ~ U(-0.30, +0.30) per mock move the TRUE baryons; flat vs H(z) separable if the 5th percentile of the H(z)-true set-medians of delta_FLAT exceeds the 95th percentile of the FLAT-true ones)")
Bm = 20000
NZm = noise(Bm)
gbm = gbar_fn(Ms0 * 10 ** NZm["est"], Mg0 * 10 ** NZm["eg"], Re, R)
tg = rng.uniform(-B_GAS, B_GAS, size=(Bm, 1)); ts = rng.uniform(-B_STAR, B_STAR, size=(Bm, 1))
tg_only = np.broadcast_to(tg, (Bm, n))


def mock_delta_marg(T, tgv, tsv):
    Tg = TT.get(T, T)
    gbt = gbar_fn(Ms0 * 10 ** tsv, Mg0 * 10 ** tgv, Re, R)
    go = gtrue(gbt, Tg) * 10 ** (NZm["eV"] + NZm["einc"] + NZm["eint"])
    return delta(go, gbm, "FLAT")


MARG = {}
for sname in ("ALL7", "ALPAKA5", "BX610+ALESS", "ALESS_122.1"):
    idx = SETS[sname]
    for lab, tsv in (("gas+stars", np.broadcast_to(ts, (Bm, n))), ("gas only", np.zeros((Bm, n)))):
        mm = {T: np.median(mock_delta_marg(T, tg_only, tsv)[:, idx], axis=1) for T in TRUTHS}
        p5h, p95f, p95h, p5f = np.percentile(mm["H(z)"], 5), np.percentile(mm["FLAT"], 95), np.percentile(mm["H(z)"], 95), np.percentile(mm["FLAT"], 5)
        p5p = np.percentile(mm["PROXY"], 5)
        MARG[f"{sname}|{lab}"] = dict(Hz_p5=float(p5h), flat_p95=float(p95f), flat_p5=float(p5f), Hz_p95=float(p95h), proxy_p5=float(p5p), sep_Hz=bool(p5h > p95f or p95h < p5f), sep_proxy=bool(p5p > p95f or np.percentile(mm["PROXY"], 95) < p5f))
        r = MARG[f"{sname}|{lab}"]
        P(f"  {sname:12s} [{lab:9s}] H(z)-true 5th pct {r['Hz_p5']:+.3f} (95th {r['Hz_p95']:+.3f}), FLAT-true 95th pct {r['flat_p95']:+.3f} (5th {r['flat_p5']:+.3f}): flat vs H(z) {'SEPARABLE' if r['sep_Hz'] else 'not separable'}; PROXY-true 5th pct {r['proxy_p5']:+.3f}: flat vs proxy {'SEPARABLE' if r['sep_proxy'] else 'not separable'}")

# ------------------------------------------------------------------ per-galaxy table
P("\nPER GALAXY (noise-free at the nominal baryons; total error budget from the mocks)")
P("  galaxy        y = g_bar/a0   d(flat vs H(z))   d(flat vs proxy)   SD of delta_FLAT (truth FLAT)   S_outer (alone)   |d_Hz| / sqrt(SD^2 + S^2)")
PG = {}
for i in range(n):
    sdi = float(np.std(set_stats(MD["FLAT"]["FLAT"], LY, [i])[0], ddof=1))
    Si = RES[gid[i]]["S"]["outer"]
    dh, dp = float(NF["H(z)"]["FLAT"][i]), float(NF["PROXY"]["FLAT"][i])
    PG[gid[i]] = dict(y=float(gb0[i] / A0), d_Hz=dh, d_proxy=dp, sd=sdi, S_outer=Si)
    P(f"  {gid[i]:12s} {gb0[i] / A0:9.2f}       {dh:+.3f}           {dp:+.3f}             {sdi:.3f}                      {Si:.3f}             {abs(dh) / math.sqrt(sdi ** 2 + Si ** 2):.3f}")

# ------------------------------------------------------------------ IMPLIED a0 (Addendum 1 A5): the estimator of CFG223, blind, on the mocks
sys.path.insert(0, LANE)
from a0implied import implied, lever, kernel_slope


def R_dec(zz, w0=-0.838, wa=-0.62):
    return math.sqrt((1.0 + zz) ** (3.0 * (1.0 + w0 + wa)) * math.exp(-3.0 * wa * zz / (1.0 + zz)))


FL4 = dict(FL)
FL4["M-DEC"] = np.array([R_dec(float(x)) for x in z])
T4 = ("FLAT", "PROXY", "H(z)", "M-DEC")


def gtrue_F(gb, Farr):
    return gb * NU(gb / (A0 * Farr))


GO = {T: gtrue_F(gb0, FL4[TT.get(T, T)]) for T in T4}
P("\nIMPLIED a0 PRE-FLIGHT (Addendum 1 A5; the estimator of CFG223, s* = the a0 scale that zeroes the set-median delta; descriptive, not a verdict; log10 s* = 0 is the canonical footing 9.3603e-11 m/s^2)")
P("  expected s* if each law were true (noise-free, nominal baryons; F_L(z) of the law beside it for a single galaxy), the kernel lever lambda = d log10 s*/d(baryon dex) at the nominal g_bar, the kernel slope, and the shift of log10 s* at the OUTER band corners (gas +-0.093 and stars +-0.30, same sign)")
P("  set            y=g_bar/a0  slope    lambda   s*_FLAT  s*_PROXY  s*_H(z)  s*_M-DEC   shift at outer corners (-,+) [log10 s*]     A3 verdict")
IMP = {}
for sname, idx in SETS.items():
    Dn = {T: GO[T] / gb0 for T in T4}
    sx = {T: float(implied(Dn[T][idx], gb0[idx], NU, A0)[0][0]) for T in T4}
    lam, lflag = lever(Dn["FLAT"][idx], gb0[idx], NU, A0)
    lam = float(lam[0])
    sl = float(np.median(kernel_slope(NU, gb0[idx] / A0)))
    sh, anyroot_lost = [], False
    for sgn in (-1, +1):
        gbp = gbar_fn(Ms0 * 10 ** (sgn * B_STAR), Mg0 * 10 ** (sgn * B_GAS), Re, R)
        ls, unb = implied((GO["FLAT"] / gbp)[idx], gbp[idx], NU, A0)
        sh.append(float(ls[0]) - sx["FLAT"]); anyroot_lost = anyroot_lost or bool(unb[0])
    ok = (abs(lam) <= 10) and (not anyroot_lost) and (max(abs(v) for v in sh) <= 1.0)
    IMP[sname] = dict(y=float(np.median(gb0[idx] / A0)), slope=sl, lever=lam, s_exp={T: 10 ** sx[T] for T in T4}, corner_shift=sh, corner_root_lost=anyroot_lost, informative=bool(ok))
    why = []
    if abs(lam) > 10: why.append("|lambda| > 10")
    if anyroot_lost: why.append("the outer band removes the root")
    if max(abs(v) for v in sh) > 1.0: why.append("the outer band moves log s* by > 1 dex")
    P(f"  {sname:12s} {np.median(gb0[idx] / A0):9.2f}  {sl:6.3f}  {lam:+8.1f}   {10 ** sx['FLAT']:6.2f}   {10 ** sx['PROXY']:6.2f}   {10 ** sx['H(z)']:6.2f}   {10 ** sx['M-DEC']:6.2f}     {sh[0]:+7.2f} / {sh[1]:+7.2f}{'  (root lost)' if anyroot_lost else ''}                  {'INFORMATIVE' if ok else 'UNINFORMATIVE: ' + '; '.join(why)}")
P("\n  Monte Carlo of the estimator under truth FLAT (s* = 1): median and 16-84% range of log10 s* over the mocks that have a root, and the fraction with NO root or a root at the edge; 'stat' = velocity, inclination and random baryon errors only (the error the DATA estimate will carry); '+ sigma_int' adds the declared 0.15 dex intrinsic scatter")
P("  set            stat: median [16%, 84%]   no-root     + sigma_int: median [16%, 84%]   no-root")
gobs_stat = GO["FLAT"] * 10 ** (NZ["eV"] + NZ["einc"])
gobs_int = gobs_stat * 10 ** NZ["eint"]
for sname, idx in SETS.items():
    row = []
    for go_ in (gobs_stat, gobs_int):
        ls, unb = implied((go_ / gb_obs_mock)[:, idx], gb_obs_mock[:, idx], NU, A0)
        ok = ~unb
        if ok.sum() > 10:
            q = np.percentile(ls[ok], [16, 50, 84]); row.append((float(q[1]), float(q[0]), float(q[2]), float(unb.mean())))
        else:
            row.append((float("nan"), float("nan"), float("nan"), float(unb.mean())))
    IMP[sname]["mc_stat"], IMP[sname]["mc_int"] = row
    P(f"  {sname:12s}   {row[0][0]:+6.2f} [{row[0][1]:+6.2f}, {row[0][2]:+6.2f}]     {row[0][3]:.2f}        {row[1][0]:+6.2f} [{row[1][1]:+6.2f}, {row[1][2]:+6.2f}]       {row[1][3]:.2f}")
P("  (log10 s* values; 0 = the canonical footing.  A range wider than 1 dex means the implied a0 of that set is undetermined at the stated errors.)")

# ------------------------------------------------------------------ control C5 (directions), C6 (recovery), analytic-vs-MC SD (C9)
P("\nCONTROLS")
gbs = gbar_fn(Ms0, Mg0 * 10 ** 0.1, Re, R); gbt_ = gbar_fn(Ms0 * 10 ** 0.1, Mg0, Re, R)
dgas, dst = nf_delta("FLAT", 0.1, np.zeros(n)), nf_delta("FLAT", 0.0, np.full(n, 0.1))
check("C5 raising the gas (+0.1 dex) or the stellar mass (+0.1 dex) lowers delta_FLAT at every galaxy", f"gas max {dgas.max():+.3f}, stars max {dst.max():+.3f}", bool((dgas < 0).all() and (dst < 0).all()))
nfid = {T: float(np.max(np.abs(nf_delta(T, 0.0, np.zeros(n), Tlaw=T)))) for T in TRUTHS}
nfoth = {T: float(min(np.min(np.abs(nf_delta(T, 0.0, np.zeros(n), Tlaw=L))) for L in TRUTHS if L != T)) for T in TRUTHS}
check("C6n noise-free planted-law identity (added after the first MUTATE run, see the README): under truth T the noise-free delta_T is 0 to 1e-9 at every galaxy and delta under each other law is non-zero at every galaxy", f"max |delta_T(T)| {max(nfid.values()):.1e}; min |delta_other| {min(nfoth.values()):.4f}", max(nfid.values()) < 1e-9 and min(nfoth.values()) > 0)
for sname in ("ALL7", "ALPAKA5", "BX610+ALESS"):
    r = RES[sname]
    ok = all(r["recovery"][T] >= 0.90 for T in TRUTHS) and all(abs(r["offset_vs_noisefree"][T]) < 3 * r["sd"] for T in ("H(z)", "PROXY"))
    check(f"C6 planted-law recovery, {sname}: the set-median delta under the TRUE law is within 2 SD of 0 in >= 90% of mocks; the other laws' offsets agree with the noise-free ones to 3 SD", f"recovery FLAT {r['recovery']['FLAT']:.2f}, H(z) {r['recovery']['H(z)']:.2f}, PROXY {r['recovery']['PROXY']:.2f}; offsets vs noise-free {r['offset_vs_noisefree']['H(z)']:+.3f}, {r['offset_vs_noisefree']['PROXY']:+.3f} (SD {r['sd']:.3f})", ok)


def analytic_sd(i):                                                     # finite-difference error propagation: an independent path to the mock SD (no inclination term)
    h = 1e-3
    Ft = FL[TT.get("FLAT", "FLAT")][i]
    Fa = FL["FLAT"][i]
    gnom = float(gbar_fn(Ms0[i], Mg0[i], Re[i], R[i]))
    gt = gnom * float(NU(np.array([gnom / (A0 * Ft)]))[0])

    def dl(dm_s, dm_g):
        gb = float(gbar_fn(Ms0[i] * 10 ** dm_s, Mg0[i] * 10 ** dm_g, Re[i], R[i]))
        return math.log10(gt / (gb * float(NU(np.array([gb / (A0 * Fa)]))[0])))
    ds, dg = (dl(h, 0) - dl(-h, 0)) / (2 * h), (dl(0, h) - dl(0, -h)) / (2 * h)
    return math.sqrt(sigV[i] ** 2 + SIG_INT ** 2 + (ds * e_st[i]) ** 2 + (dg * e_gas[i]) ** 2)


an = {gid[i]: analytic_sd(i) for i in range(n) if not math.isfinite(e_i[i])}
mcsd = {gid[i]: PG[gid[i]]["sd"] for i in range(n) if not math.isfinite(e_i[i])}
worst = max(abs(mcsd[k] / an[k] - 1) for k in an)
check("C9 the mock SD of delta_FLAT (truth FLAT) for the galaxies without an inclination term equals the finite-difference error propagation (an independent path) to 8%", "; ".join(f"{k} MC {mcsd[k]:.3f} vs analytic {an[k]:.3f}" for k in an), worst < 0.08)
import re as _re
src223 = open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_a0_over_time.py")).read()
seg = src223[src223.index("LO_LS, HI_LS, NIT"):src223.index("_IDX = {}")]
ns223 = {"np": np}
exec(compile(seg, "cfg223_a0_over_time.py", "exec"), ns223)
rr = np.random.default_rng(1234)
same = True
for _ in range(200):
    Dq = 10 ** rr.uniform(-0.3, 0.9, size=(5, 7)); gq = 10 ** rr.uniform(-11, -8, size=(5, 7))
    a1, u1 = ns223["implied"](Dq, gq, NU, A0)
    a2, u2 = implied(Dq, gq, NU, A0)
    same = same and np.array_equal(a1, a2) and np.array_equal(u1, u2)
check("C10 the implied-a0 estimator of a0implied.py equals CFG223's original bit for bit on 200 random sets (verbatim copy)", f"identical {same}", bool(same))

# ------------------------------------------------------------------ Q3 (post hoc, labelled): what baryon precision would make the pooled separation possible?
P("\nQ3 (POST HOC, not frozen): the common precision d (dex) on stars and gas (random errors AND outer band both set to d) at which flat vs H(z) in ALL7 satisfies signal > S_max + 2 SD; the inherent noise floor is sigma_int, the velocity errors and the ALPAKA inclinations")


def pf_at(d, Bq=400):
    r2 = np.random.default_rng(SEED + 7)
    est, eg = r2.normal(0, d, (Bq, n)), r2.normal(0, d, (Bq, n))
    eV = r2.normal(0, 1, (Bq, n)) * sigV
    ein = r2.normal(0, SIG_INT, (Bq, n))
    gbo = gbar_fn(Ms0 * 10 ** est, Mg0 * 10 ** eg, Re, R)
    out = {}
    for T in ("FLAT", "H(z)"):
        go = gtrue(gb0, TT.get(T, T)) * 10 ** (eV + ein)
        out[T] = np.median(delta(go, gbo, "FLAT"), axis=1)
    sdq = float(np.std(out["FLAT"], ddof=1)); sg = abs(float(np.median(out["H(z)"])))
    Sq = max(abs(float(np.median(nf_delta("FLAT", s * d, np.full(n, s * d)))) ) for s in (+1, -1))
    return sg, sdq, Sq, bool(sg > Sq + 2 * sdq)


q3 = {}
for d in (0.30, 0.20, 0.10, 0.05, 0.02, 0.01, 0.005):
    sg, sdq, Sq, ok = pf_at(d)
    q3[d] = dict(signal=sg, sd=sdq, S=Sq, possible=ok)
    P(f"    d = {d:5.3f}: signal {sg:.3f}, SD {sdq:.3f} (sigma_int-only floor ~ {SIG_INT / math.sqrt(n) * 1.25:.3f}), S {Sq:.3f} -> {'POSSIBLE' if ok else 'not possible'}  (ALPAKA inclination terms omitted here: a lower bound on the noise)")
P("    (the noise floor alone, sigma_int = 0.15 over seven galaxies, sets SD ~ 0.07, so a signal below ~0.14 cannot be separated even with perfect baryons)")
P("\n  radius at which the galaxy would be in the informative regime (y = 3), nominal baryons: R*(y = 3) and the noise-free d(flat vs H(z)) there")
RS = {}
for i in range(n):
    f = lambda RR: gbar_fn(Ms0[i], Mg0[i], Re[i], RR) / A0 - 3.0
    grid = np.linspace(R[i], 60.0, 2000)
    vals = np.array([f(x) for x in grid])
    j = np.where(vals < 0)[0]
    if len(j) == 0 or f(R[i]) < 0:
        RS[gid[i]] = dict(Rstar=float("nan"), d=float("nan")); P(f"    {gid[i]:12s} y(R) < 3 already at the stated radius" if f(R[i]) < 0 else f"    {gid[i]:12s} y > 3 out to 60 kpc"); continue
    Rs = float(grid[j[0]])
    gbs_ = float(gbar_fn(Ms0[i], Mg0[i], Re[i], Rs))
    nu_h = float(NU(np.array([gbs_ / (A0 * FL["H(z)"][i])]))[0])                # this galaxy's own H(z) factor (scalar)
    nu_f = float(NU(np.array([gbs_ / (A0 * FL["FLAT"][i])]))[0])
    dd = math.log10(nu_h / nu_f)
    RS[gid[i]] = dict(Rstar=Rs, d=dd)
    P(f"    {gid[i]:12s} R*(y=3) = {Rs:6.2f} kpc ({Rs / R[i]:.1f} x the stated radius): d(flat vs H(z)) = {dd:+.3f}")

# ------------------------------------------------------------------ C8 blindness
if not CHILD:
    kin = os.path.join(LANE, "cfg229_inputs_kin.csv")
    hid = kin + ".hidden_for_blindness_test"
    tmpj = os.path.join(tempfile.mkdtemp(), "pf.json")
    res_main = dict(RES=RES, PG=PG, MARG=MARG, q3={str(k): v for k, v in q3.items()}, RS=RS, IMP=IMP)
    try:
        os.rename(kin, hid)
        env = dict(os.environ, CFG229_PF_CHILD="1", CFG229_PF_JSON=tmpj)
        if MUT:
            env["MUTATE"] = "1"
        pr = subprocess.run([sys.executable, os.path.abspath(__file__)], env=env, capture_output=True, text=True)
    finally:
        if os.path.exists(hid):
            os.rename(hid, kin)
    same = pr.returncode in (0, 1) and os.path.exists(tmpj)
    if same:
        child = json.load(open(tmpj))
        same = json.dumps(child["RES"], sort_keys=True, default=float) == json.dumps(json.loads(json.dumps(res_main["RES"], default=float)), sort_keys=True)
    check("C8 blindness: with the kinematics file REMOVED the pre-flight runs to completion and gives the same set statistics bit for bit", f"child exit {pr.returncode}, identical {same}", bool(same))
    shutil.rmtree(os.path.dirname(tmpj), ignore_errors=True)
else:
    res_main = dict(RES=RES, PG=PG, MARG=MARG, q3={str(k): v for k, v in q3.items()}, RS=RS, IMP=IMP)

P(f"\n{sum(CHK)}/{len(CHK)} controls pass; {time.time() - T0:.0f} s")
res_main["controls"] = CHK
res_main["params"] = dict(seed=SEED, B=B, sig_int=SIG_INT, B_gas=B_GAS, B_star=B_STAR, in_gas=IN_GAS, mutate=MUT)
json.dump(res_main, open(JSON_OUT, "w"), indent=1, default=float)
if not CHILD:
    open(os.path.join(LANE, "cfg229_preflight" + ("_MUTATE" if MUT else "") + ".out"), "w").write("\n".join(OUT).replace(REPO, "<repo>") + "\n")
sys.exit(0 if all(CHK) else 1)
