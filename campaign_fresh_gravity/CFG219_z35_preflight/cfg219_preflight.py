#!/usr/bin/env python3
"""CFG219 -- a pre-flight power forecast for the z > 3.5 decisive test, on the data chat's class-A independent-baryon discs.
Frozen criteria: FROZEN_CRITERIA.md here (e62ce4cff), committed before any number.  kappa = 1/2 FITTED, NOT DERIVED.  A forecast, not a measurement: no sentence says the data favour a framework.
Inputs per disc: z, radius, baryon masses and errors ONLY (no velocities, no f_DM).  Laws (Z1, 1138d817f, imported read-only): FLAT, H(z), particle HORIZON, LCDM-NATIVE.
Statistic: the lanes' -- median delta over discs, galaxy bootstrap (B = 300) inside each of 500 mocks; a gas-calibration systematic c_k ~ N(0, tau) shared by every disc of a tracer class.
Run:  python3 campaign_fresh_gravity/CFG219_z35_preflight/cfg219_preflight.py        (MUTATE=1: a +0.20 dex offset on every baryon mass; response controls only)
"""
import os, sys, csv, math, json, time
sys.dont_write_bytecode = True
import numpy as np
from scipy.special import i0e, i1e, k0e, k1e

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
_mut = os.environ.pop("MUTATE", None)
try:
    import CFG4_common as K
finally:
    if _mut is not None:
        os.environ["MUTATE"] = _mut
MODE = (_mut or "").strip()
assert MODE in ("", "0", "1")
MUT = MODE == "1"
SFX = "_MUTATE" if MUT else ""
Z1DIR = os.path.join(REPO, "sonnet55_push", "puzzle_32pi", "agents", "Z1_causal_horizon_a0z")
sys.path.insert(0, Z1DIR)
import zcommon as Z1                                              # READ-ONLY: Cosmo, laws, lcdm_native, PLANCK

T0 = time.time()
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(s)


CHK = []


def check(name, val, ok):
    CHK.append(bool(ok))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


G2SI = 1e6 / 3.0856775814913673e19
G_KPC = 4.30091e-6
XN = 1.678
OM = 0.315
NMC, NB, SEED = 500, 300, 219
TAUS = (0.0, 0.10, 0.25, 0.40)
SHIFT = 0.20 if MUT else 0.0
A0S = {"canonical": K.A0["canonical"], "alt": K.A0["alt"]}
KERN = {"nu_mono": K.nu_mono, "P2": K.nu_p2}


def disc_v2(M, Re, Rr):                                            # CFG216's thin exponential disc (Freeman), (km/s)^2
    Rd = Re / XN
    y = Rr / (2 * Rd)
    return 2 * G_KPC * M / Rd * y ** 2 * (i0e(y) * k0e(y) - i1e(y) * k1e(y))


def Ez(z):
    return math.sqrt(OM * (1 + z) ** 3 + 1 - OM)


cos = Z1.Cosmo(**Z1.PLANCK)
LZ = Z1.laws(cos)
LAWF = {"FLAT": lambda z: 1.0, "H(z)": Ez, "HORIZON": LZ["particle horizon d_p (radius OR diameter)"], "LCDM-NATIVE": Z1.lcdm_native}
LAWS = tuple(LAWF)
PAIRS = [(a, b) for i, a in enumerate(LAWS) for b in LAWS[i + 1:]]
P(__doc__.split("Run:")[0].strip())

# ------------------------------------------------------------------------------------------------ inputs
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")


def rd(p):
    return list(csv.DictReader(open(p, newline="")))


smp = {r["id"]: r for r in rd(os.path.join(AT, "cristal2025_sample.csv"))}
kin = {r["id"]: r for r in rd(os.path.join(AT, "cristal2025_kinematics.csv"))}
dyn = {r["id"]: r for r in rd(os.path.join(AT, "cristal2025_dynamics.csv"))}
DET = ("02", "03", "07a", "11", "19", "20")
SIG_STAR = 0.15


def cristal_rows(sig_star=SIG_STAR):
    rows = []
    for i in DET:
        f = float(kin[i]["f_molgas"]); sf = 0.5 * (float(kin[i]["errhi"]) + float(kin[i]["errlo"]))
        Ms = 10 ** float(smp[i]["logMstar"])
        Re = float(dyn[i]["Re_disk_kpc"]); Ro = float(dyn[i]["Rout_over_Re"]) * Re
        rows.append(dict(name=f"CRISTAL-{i}", z=float(smp[i]["z_cii"]), Re=Re, Rout=Ro, Ms=Ms, Mg=Ms * f / (1 - f), sig_star=sig_star,
                         sig_gas=sf / (math.log(10) * f * (1 - f)), cls=0, f=f, prov=False))
    return rows


def provisional_rows(reb_re=1.5):
    return [dict(name="GN20 (provisional)", z=4.055, Re=3.6, Rout=3.6, Ms=1.6e11, Mg=1.0e11, sig_star=0.15, sig_gas=0.30, cls=1, f=1.0 / 2.6, prov=True),
            dict(name="REBELS-25 (provisional; R_e placeholder)", z=7.3065, Re=reb_re, Rout=reb_re, Ms=8e9, Mg=1.0e11, sig_star=0.20, sig_gas=0.17, cls=1, f=1.0e11 / 1.08e11, prov=True)]


def make_base(rows, radius="Re"):
    b = {k: np.array([r[k] for r in rows]) for k in ("z", "Re", "Rout", "Ms", "Mg", "sig_star", "sig_gas", "cls")}
    b["name"] = [r["name"] for r in rows]
    Rr = b["Re"] if radius == "Re" else b["Rout"]
    b["Rr"] = Rr
    b["cg"] = np.array([disc_v2(1.0, re, rr) / rr * G2SI for re, rr in zip(b["Re"], Rr)])       # g_bar per unit baryon mass [m/s^2 / Msun]
    b["Mb"] = b["Ms"] + b["Mg"]
    b["F"] = {l: np.array([LAWF[l](z) for z in b["z"]]) for l in LAWS}
    assert all(np.all(np.isfinite(v)) for v in b["F"].values()), "a law is not finite at a disc redshift"
    return b


# ------------------------------------------------------------------------------------------------ noiseless machinery
def delta_noiseless(b, T, L, nu, a0, shift=0.0):
    gt = b["Mb"] * b["cg"]
    gobs = gt * nu(gt / (a0 * b["F"][T]))
    gm = gt * 10 ** shift
    return np.log10((gobs / gm) / nu(gm / (a0 * b["F"][L])))


# ------------------------------------------------------------------------------------------------ the mock forecast
def forecast(b, N, tau, T, L, nu, a0, rng, shift=0.0):
    n = len(b["z"])
    s_base = delta_noiseless(b, T, L, nu, a0)
    sgn = 1.0 if np.median(s_base) > 0 else -1.0
    IDXB = rng.integers(0, N, size=(NB, N))
    med = np.empty(NMC); zs = np.empty(NMC); ok = np.empty(NMC, bool)
    CH = max(1, 4_000_000 // (NB * N))
    for c0 in range(0, NMC, CH):
        m = min(CH, NMC - c0)
        idx = np.tile(np.arange(n), (m, 1)) if N == n else rng.integers(0, n, size=(m, N))
        es = rng.normal(0, 1, (m, N)) * b["sig_star"][idx]
        eg = rng.normal(0, 1, (m, N)) * b["sig_gas"][idx]
        ck = rng.normal(0, tau, (m, 2)) if tau > 0 else np.zeros((m, 2))
        cc = np.take_along_axis(ck, b["cls"][idx].astype(int), axis=1)
        Ms, Mg = b["Ms"][idx], b["Mg"][idx]
        Mb_t = Ms + Mg
        Mb_m = (Ms * 10 ** es + Mg * 10 ** (eg + cc)) * 10 ** shift
        cg = b["cg"][idx]
        gt = Mb_t * cg
        gobs = gt * nu(gt / (a0 * b["F"][T][idx]))
        gm = Mb_m * cg
        d = np.log10((gobs / gm) / nu(gm / (a0 * b["F"][L][idx])))
        bs = np.median(d[:, IDXB], axis=2)                                # (m, NB)
        mm = np.median(d, axis=1)
        sd = bs.std(axis=1)
        lo, hi = np.percentile(bs, [2.5, 97.5], axis=1)
        med[c0:c0 + m] = mm
        zs[c0:c0 + m] = sgn * mm / np.maximum(sd, 1e-12)
        ok[c0:c0 + m] = (sgn * lo > 0) if sgn > 0 else (hi < 0)
    return dict(mu=float(np.mean(med)), zmed=float(np.median(zs)), power=float(np.mean(ok)), sd_mock=float(np.std(med)), sgn=sgn)


# ------------------------------------------------------------------------------------------------ controls
P("\nCONTROLS")
Dz = LZ["particle horizon d_p (radius OR diameter)"]
c1 = (abs(Ez(2.5) - 3.77) < 0.01 and abs(Dz(2.5) - 6.05) < 0.02 and abs(Z1.lcdm_native(2.5) - 2.16) < 0.02 and abs(Dz(5.0) - 13.7) < 0.05)
check("C1 Z1 reproduction: at z = 2.5 the ratios 1 / 3.77 / 6.05 / 2.16 and the horizon law at z = 5 (13.7)",
      f"H(z) {Ez(2.5):.3f}, horizon {Dz(2.5):.3f}, LCDM-native {Z1.lcdm_native(2.5):.3f}, horizon(5) {Dz(5.0):.3f}", c1)
Vfree = max(disc_v2(1.0, XN, r) for r in np.linspace(0.5, 12, 4000)) / G_KPC          # R_e = 1.678 kpc gives R_d = 1 kpc: peak V^2 in units of G M / R_d
check("C0 the disc formula reproduces Freeman's peak V^2 = 0.3872 G M / R_d (V_max = 0.622 sqrt(G M / R_d); the first run compared with 0.6238, the square root, an error of the check)", f"{Vfree:.4f}", abs(Vfree - 0.3872) < 0.003)
S6 = make_base(cristal_rows())
S8 = make_base(cristal_rows() + provisional_rows())
z_ok = True
d0 = []
for kname, nu in KERN.items():
    for foot, a0 in A0S.items():
        for L_ in LAWS:
            d0.append(np.max(np.abs(delta_noiseless(S8, L_, L_, nu, a0))))
c2a = max(d0)
oth = np.array([np.abs(delta_noiseless(S8, T_, L_, nu, A0S["canonical"])) for T_ in LAWS for L_ in LAWS if T_ != L_ for nu in KERN.values()]).ravel()
check("C2 (through D = g_obs/g_bar and nu) with no noise the true law's own delta is 0 for every disc, law, kernel and footing", f"max |delta| {c2a:.1e}", c2a < 1e-9)
check("C2b the OTHER laws' deltas are non-zero (>= 1e-3 for >= 90% of disc-law pairs)", f"{100 * np.mean(oth >= 1e-3):.0f}%", np.mean(oth >= 1e-3) >= 0.90)
c3 = 0.0
for T_, L_ in ((a, b_) for a in LAWS for b_ in LAWS if a != b_):
    gt = S8["Mb"] * S8["cg"]
    yT, yL = gt / (A0S["canonical"] * S8["F"][T_]), gt / (A0S["canonical"] * S8["F"][L_])
    an = np.median(np.log10(K.nu_mono(yT)) - np.log10(K.nu_mono(yL)))
    c3 = max(c3, abs(an - np.median(delta_noiseless(S8, T_, L_, K.nu_mono, A0S["canonical"]))))
check("C3 the noiseless median shift equals the analytic per-disc separation log10 nu(y_T)/nu(y_L)", f"max |difference| {c3:.1e}", c3 < 1e-9)
# C4: the response to an injected uniform calibration offset (independent per-disc finite-difference bound)
h = 0.20
dd = delta_noiseless(S8, "FLAT", "H(z)", K.nu_mono, A0S["canonical"], shift=h) - delta_noiseless(S8, "FLAT", "H(z)", K.nu_mono, A0S["canonical"], shift=0.0)
kk = -dd / h
check("C4 an injected +0.20 dex offset on every baryon mass lowers EVERY disc's delta, with |d delta / d log g_bar| between 0.5 and 1 (deep MOND to Newtonian)",
      f"per-disc slopes {np.min(kk):.3f} to {np.max(kk):.3f}", np.all(dd < 0) and 0.5 - 1e-6 <= np.min(kk) and np.max(kk) <= 1.0 + 1e-6)
if MUT:
    P(f"\nMUTATE=1: every mock carries a +{SHIFT:.2f} dex offset on the measured baryon masses; the noiseless separation and the primary pair at N = 6, tau = 0 follow.")
    rng = np.random.default_rng(SEED)
    for T_, L_ in ((a, b_) for a in ("FLAT", "H(z)") for b_ in ("FLAT", "H(z)") if a != b_):
        f0 = forecast(S6, 6, 0.0, T_, L_, K.nu_mono, A0S["canonical"], rng, shift=0.0)
        f1 = forecast(S6, 6, 0.0, T_, L_, K.nu_mono, A0S["canonical"], rng, shift=SHIFT)
        P(f"  {T_} true, {L_} tested: mean median-delta {f0['mu']:+.3f} -> {f1['mu']:+.3f} (shift {f1['mu'] - f0['mu']:+.3f}; the independent per-disc bound: between {-1.0 * SHIFT:+.3f} and {-0.5 * SHIFT:+.3f})")
        check("MUTATE the offset moves the mock's mean median delta down by 0.5-1 x 0.20 dex (within MC error 0.02)", f"{f1['mu'] - f0['mu']:+.3f}", -1.0 * SHIFT - 0.02 <= f1["mu"] - f0["mu"] <= -0.5 * SHIFT + 0.02)
    open(os.path.join(LANE, "cfg219_preflight" + SFX + ".out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if all(CHK) else 1)

# ------------------------------------------------------------------------------------------------ the per-disc table (transparency)
P("\nPER-DISC INPUTS AND THE EXPECTED SEPARATIONS (nu_mono, canonical, R_e; noiseless; s = log10 nu(y_T)/nu(y_L), the median of these is the expected shift)")
P(f"  {'disc':42s} {'z':>6s} {'R_e':>5s} {'log M_b':>8s} {'sig_logMb':>9s} {'g_bar/A0':>9s} | a0(z)/a0(0): " + " ".join(f"{l:>11s}" for l in LAWS))
rng0 = np.random.default_rng(SEED + 1)
for i, nm in enumerate(S8["name"]):
    es = rng0.normal(0, 1, 4000) * S8["sig_star"][i]; eg = rng0.normal(0, 1, 4000) * S8["sig_gas"][i]
    slm = float(np.std(np.log10(S8["Ms"][i] * 10 ** es + S8["Mg"][i] * 10 ** eg)))
    gb = S8["Mb"][i] * S8["cg"][i] / A0S["canonical"]
    P(f"  {nm:42s} {S8['z'][i]:6.3f} {S8['Re'][i]:5.1f} {math.log10(S8['Mb'][i]):8.2f} {slm:9.2f} {gb:9.2f} |               " + " ".join(f"{S8['F'][l][i]:11.2f}" for l in LAWS))
P("  separations s_i (dex) by pair (first-named law true, second tested), S8 discs in the order above:")
for a, b_ in PAIRS:
    s = delta_noiseless(S8, a, b_, K.nu_mono, A0S["canonical"])
    P(f"    {a:11s} -> {b_:11s}: " + " ".join(f"{v:+.3f}" for v in s) + f"   median S6 {np.median(s[:6]):+.3f}, S8 {np.median(s):+.3f}")

# ------------------------------------------------------------------------------------------------ the forecast tables
RES = {}
rng = np.random.default_rng(SEED)


def cell(setname, base, kname, foot, radius, Ns, taus, pairs_ordered):
    nu, a0 = KERN[kname], A0S[foot]
    key = (setname, kname, foot, radius)
    RES[key] = {}
    for (T_, L_) in pairs_ordered:
        for N in Ns:
            for tau in taus:
                RES[key][(T_, L_, N, tau)] = forecast(base, N, tau, T_, L_, nu, a0, rng)
    return RES[key]


ORD = [(a, b_) for a in LAWS for b_ in LAWS if a != b_]
NS6 = (6, 13, 16, 20, 30, 50, 100)
NS8 = (8, 13, 16, 20, 30, 50, 100)
t = time.time()
cell("S6", S6, "nu_mono", "canonical", "Re", NS6, TAUS, ORD)
P(f"\n[S6 primary cell done in {time.time() - t:.0f} s]")
t = time.time()
cell("S8", S8, "nu_mono", "canonical", "Re", NS8, TAUS, ORD)
P(f"[S8 scenario cell done in {time.time() - t:.0f} s]")
SENS_N6, SENS_N8 = (6, 13, 20), (8, 13, 20)
for kname, foot in (("nu_mono", "alt"), ("P2", "canonical"), ("P2", "alt")):
    cell("S6", S6, kname, foot, "Re", SENS_N6, (0.0, 0.25), ORD)
S6o = make_base(cristal_rows(), radius="Rout")
cell("S6", S6o, "nu_mono", "canonical", "Rout", NS6, TAUS, ORD)
P(f"[sensitivity cells done, {time.time() - T0:.0f} s in total]")


def nsig(key, a, b_, N, tau):
    r = RES[key]
    return min(r[(a, b_, N, tau)]["zmed"], r[(b_, a, N, tau)]["zmed"])


def mu_pair(key, a, b_, N, tau):
    r = RES[key]
    return r[(a, b_, N, tau)]["mu"], r[(b_, a, N, tau)]["mu"]


def n3(key, a, b_, Ns, tau, f=None):
    f = f or nsig
    vals = [(N, f(key, a, b_, N, tau)) for N in Ns]
    for k, (N, v) in enumerate(vals):
        if v >= 3.0:
            if k == 0:
                return float(N)
            (N0, v0) = vals[k - 1]
            return float(math.exp(math.log(N0) + (3.0 - v0) * (math.log(N) - math.log(N0)) / (v - v0)))
    return None


def taumax(key, a, b_, N, f=None):
    f = f or nsig
    vs = [f(key, a, b_, N, tau) for tau in TAUS]
    if vs[0] < 3.0:
        return None
    for k in range(1, len(TAUS)):
        if vs[k] < 3.0:
            return TAUS[k - 1] + (vs[k - 1] - 3.0) * (TAUS[k] - TAUS[k - 1]) / (vs[k - 1] - vs[k])
    return float("inf")


def fmt_n(x, cap=100):
    return "not reached by N = 100" if x is None else f"{x:.1f}"


P("\nRESULT 1 -- the expected separation (dex; the mean over mocks of the median delta of the tested law, tau = 0), FIRST-named law true; then z_med = the typical realised significance n_sigma, min over the two directions")
for setname, Ns, nbase in (("S6", NS6, 6), ("S8", NS8, 8)):
    key = (setname, "nu_mono", "canonical", "Re")
    P(f"\n  set {setname}{' (PROVISIONAL inputs for GN20 and REBELS-25)' if setname == 'S8' else ''}; nu_mono, canonical, R_e")
    P(f"    {'pair':24s} {'mu A->B':>8s} {'mu B->A':>8s} | n_sigma at N = " + "  ".join(f"{N:>5d}" for N in Ns[:5]) + "   (tau = 0)")
    for a, b_ in PAIRS:
        m1, m2 = mu_pair(key, a, b_, nbase, 0.0)
        P(f"    {a + ' vs ' + b_:24s} {m1:+8.3f} {m2:+8.3f} |                " + "  ".join(f"{nsig(key, a, b_, N, 0.0):5.2f}" for N in Ns[:5]))
P("\nRESULT 2 -- the same at the BASELINE gas calibration tau = 0.25 dex (shared per tracer class) and the grid")
for setname, Ns, nbase in (("S6", NS6, 6), ("S8", NS8, 8)):
    key = (setname, "nu_mono", "canonical", "Re")
    P(f"\n  set {setname}: n_sigma at tau = " + " ".join(f"{t_:.2f}" for t_ in TAUS) + f" (dex), for N = {nbase} | 13 | 20 | 100")
    for a, b_ in PAIRS:
        P(f"    {a + ' vs ' + b_:24s} " + " | ".join(" ".join(f"{nsig(key, a, b_, N_, t_):5.1f}" for t_ in TAUS) for N_ in (nbase, 13, 20, 100)))
P("\nRESULT 3 -- N needed for 3 sigma and the calibration that a sample can tolerate")
for setname, Ns, nbase in (("S6", NS6, 6), ("S8", NS8, 8)):
    key = (setname, "nu_mono", "canonical", "Re")
    P(f"\n  set {setname}: N for n_sigma >= 3 at tau = 0 / 0.10 / 0.25 / 0.40;  tau_max (dex on the gas mass) at N = {nbase} / 13 / 20 / 100")
    for a, b_ in PAIRS:
        ns_ = [n3(key, a, b_, Ns, t_) for t_ in TAUS]
        tm = [taumax(key, a, b_, N_) for N_ in (nbase, 13, 20, 100)]
        P(f"    {a + ' vs ' + b_:24s} N_3sigma: " + " / ".join("none" if x is None else f"{x:.0f}" for x in ns_) + "     tau_max: " + " / ".join("none" if x is None else (">0.40" if x == float('inf') else f"{x:.2f}") for x in tm))
P("\nRESULT 4 -- decision classes (frozen)")
CLS = {}
for a, b_ in PAIRS:
    key = ("S6", "nu_mono", "canonical", "Re")
    st0 = nsig(key, a, b_, 6, 0.0); st25 = nsig(key, a, b_, 6, 0.25)
    stat = "STAT-POWERED" if st0 >= 3 else "STAT-UNDERPOWERED"
    cal = "CALIBRATION-ROBUST" if st25 >= 3 else "CALIBRATION-LIMITED"
    CLS[(a, b_)] = (stat, cal, st0, st25)
    P(f"  {a + ' vs ' + b_:24s} S6: n_sigma(tau = 0, N = 6) {st0:5.2f} -> {stat}; n_sigma(tau = 0.25, N = 6) {st25:5.2f} -> {cal};  N_3sigma(tau = 0) {fmt_n(n3(key, a, b_, NS6, 0.0))}, "
      f"N_3sigma(tau = 0.25) {fmt_n(n3(key, a, b_, NS6, 0.25))}")
P("\n  the 13-20 disc summary (S6 inputs resampled; n_sigma >= 3?)  tau = 0 | tau = 0.25:")
for a, b_ in PAIRS:
    key = ("S6", "nu_mono", "canonical", "Re")
    P(f"    {a + ' vs ' + b_:24s} N = 13: {nsig(key, a, b_, 13, 0.0):5.2f} ({'yes' if nsig(key, a, b_, 13, 0.0) >= 3 else 'no'}) | {nsig(key, a, b_, 13, 0.25):5.2f} ({'yes' if nsig(key, a, b_, 13, 0.25) >= 3 else 'no'});   "
      f"N = 20: {nsig(key, a, b_, 20, 0.0):5.2f} ({'yes' if nsig(key, a, b_, 20, 0.0) >= 3 else 'no'}) | {nsig(key, a, b_, 20, 0.25):5.2f} ({'yes' if nsig(key, a, b_, 20, 0.25) >= 3 else 'no'})")
P("\nRESULT 5 -- sensitivities (n_sigma; primary cell shown first)  N = 6 | 13 | 20  at tau = 0 and tau = 0.25")
for setname, kname, foot, radius in (("S6", "nu_mono", "canonical", "Re"), ("S6", "nu_mono", "alt", "Re"), ("S6", "P2", "canonical", "Re"), ("S6", "P2", "alt", "Re"), ("S6", "nu_mono", "canonical", "Rout")):
    key = (setname, kname, foot, radius)
    P(f"\n  {setname} {kname} {foot} R = {radius}")
    for a, b_ in PAIRS:
        P(f"    {a + ' vs ' + b_:24s} tau = 0: " + " | ".join(f"{nsig(key, a, b_, N, 0.0):5.2f}" for N in SENS_N6) + "     tau = 0.25: " + " | ".join(f"{nsig(key, a, b_, N, 0.25):5.2f}" for N in SENS_N6))
labels = {}
for a, b_ in PAIRS:
    cl = []
    for kname, foot, radius in (("nu_mono", "canonical", "Re"), ("nu_mono", "alt", "Re"), ("P2", "canonical", "Re"), ("P2", "alt", "Re"), ("nu_mono", "canonical", "Rout")):
        key = ("S6", kname, foot, radius)
        cl.append(("SP" if nsig(key, a, b_, 6, 0.0) >= 3 else "SU") + ("CR" if nsig(key, a, b_, 6, 0.25) >= 3 else "CL"))
    labels[(a, b_)] = "consistent across cells" if len(set(cl)) == 1 else "KERNEL/FOOTING/RADIUS-DEPENDENT (" + ", ".join(cl) + ")"
P("\n  class stability across the sensitivity cells (SP/SU = stat powered/underpowered, CR/CL = calibration robust/limited; cells: mono-can-Re, mono-alt-Re, P2-can-Re, P2-alt-Re, mono-can-Rout):")
for a, b_ in PAIRS:
    P(f"    {a + ' vs ' + b_:24s} {labels[(a, b_)]}")
# S6 input sensitivities and the S8 placeholder radius (primary pair only)
P("\n  input sensitivities, primary pair FLAT vs H(z) (n_sigma = min over the two directions), nu_mono, canonical, R_e:")
for lab, base, N in (("sigma_star 0.10", make_base(cristal_rows(0.10)), 6), ("sigma_star 0.25", make_base(cristal_rows(0.25)), 6), ("S6 baseline sigma_star 0.15", S6, 6),
                     ("S8, REBELS-25 R_e x 0.5", make_base(cristal_rows() + provisional_rows(0.75)), 8), ("S8, REBELS-25 R_e x 2", make_base(cristal_rows() + provisional_rows(3.0)), 8), ("S8 baseline R_e 1.5", S8, 8)):
    vals = []
    for tau in (0.0, 0.25):
        f1 = forecast(base, N, tau, "FLAT", "H(z)", K.nu_mono, A0S["canonical"], rng)
        f2 = forecast(base, N, tau, "H(z)", "FLAT", K.nu_mono, A0S["canonical"], rng)
        vals.append(min(f1["zmed"], f2["zmed"]))
    P(f"    {lab:32s} N = {N}: tau = 0: {vals[0]:5.2f};  tau = 0.25: {vals[1]:5.2f}")

def ntot(key, a, b_, N, tau):
    r = RES[key]
    return min(abs(r[(a, b_, N, tau)]["mu"]) / r[(a, b_, N, tau)]["sd_mock"], abs(r[(b_, a, N, tau)]["mu"]) / r[(b_, a, N, tau)]["sd_mock"])


P("\nRESULT 6 -- POST HOC (written after the frozen numbers were seen; reported only): the frozen z_med is BLIND to the shared calibration systematic")
P("  The frozen n_sigma is the MEDIAN over mocks of |median delta| / (the bootstrap sd inside the mock). A calibration offset shared by every disc shifts the mock's median delta by the same amount in all discs but is not in the")
P("  bootstrap sd, and its sign is symmetric across mocks, so the median over mocks does not move (Result 2 is flat in tau by construction; the frozen class 'CALIBRATION-ROBUST' is therefore NOT evidence of robustness).")
P("  The systematic-inclusive measure used here: n_tot = |mu| / sd_mock, mu the mean and sd_mock the standard deviation over mocks of the pooled median delta (baryon noise + the shared tau + the composition scatter), min over the two directions.")
for setname, radius, Ns, nbase in (("S6", "Re", NS6, 6), ("S6", "Rout", NS6, 6), ("S8", "Re", NS8, 8)):
    key = (setname, "nu_mono", "canonical", radius)
    P(f"\n  set {setname}, R = {radius}: n_tot at tau = " + " ".join(f"{t_:.2f}" for t_ in TAUS) + f" (dex), for N = {nbase} | 13 | 20 | 100")
    for a, b_ in PAIRS:
        P(f"    {a + ' vs ' + b_:24s} " + " | ".join(" ".join(f"{ntot(key, a, b_, N_, t_):5.1f}" for t_ in TAUS) for N_ in (nbase, 13, 20, 100)))
    P(f"  set {setname}, R = {radius}: N for n_tot >= 3 at tau = 0 / 0.10 / 0.25 / 0.40 ('systematic-limited' = not reached by N = 100);  tau_max at N = {nbase} / 13 / 20 / 100")
    for a, b_ in PAIRS:
        ns_ = [n3(key, a, b_, Ns, t_, ntot) for t_ in TAUS]
        tm = [taumax(key, a, b_, N_, ntot) for N_ in (nbase, 13, 20, 100)]
        P(f"    {a + ' vs ' + b_:24s} N_3sigma: " + " / ".join("systematic-limited" if x is None else f"{x:.0f}" for x in ns_) + "     tau_max: " + " / ".join("none" if x is None else (">0.40" if x == float('inf') else f"{x:.2f}") for x in tm))
P("\n  the 13-20 disc summary, systematic-inclusive (S6 inputs resampled, R_e; n_tot >= 3?)  tau = 0 | tau = 0.25:")
for a, b_ in PAIRS:
    key = ("S6", "nu_mono", "canonical", "Re")
    P(f"    {a + ' vs ' + b_:24s} N = 13: {ntot(key, a, b_, 13, 0.0):5.2f} ({'yes' if ntot(key, a, b_, 13, 0.0) >= 3 else 'no'}) | {ntot(key, a, b_, 13, 0.25):5.2f} ({'yes' if ntot(key, a, b_, 13, 0.25) >= 3 else 'no'});   "
      f"N = 20: {ntot(key, a, b_, 20, 0.0):5.2f} ({'yes' if ntot(key, a, b_, 20, 0.0) >= 3 else 'no'}) | {ntot(key, a, b_, 20, 0.25):5.2f} ({'yes' if ntot(key, a, b_, 20, 0.25) >= 3 else 'no'})")
sat2 = all(ntot(("S6", "nu_mono", "canonical", "Re"), a, b_, 13, 0.25) <= ntot(("S6", "nu_mono", "canonical", "Re"), a, b_, 13, 0.0) + 0.3 for a, b_ in PAIRS) and \
    sum(ntot(("S6", "nu_mono", "canonical", "Re"), a, b_, 100, 0.25) < 0.8 * ntot(("S6", "nu_mono", "canonical", "Re"), a, b_, 100, 0.0) for a, b_ in PAIRS) >= 5
P("")
check("C5b (post hoc; discriminating) the systematic-inclusive n_tot saturates: at N = 100 it falls by >= 20% between tau = 0 and 0.25 for at least five of the six pairs, and never rises at N = 13", "the six pairs, S6, R_e", sat2)
# C5 saturation
sat = all(nsig(("S6", "nu_mono", "canonical", "Re"), a, b_, 6, 0.25) <= nsig(("S6", "nu_mono", "canonical", "Re"), a, b_, 6, 0.0) + 0.3 for a, b_ in PAIRS)
P("")
check("C5 saturation: n_sigma at tau = 0.25 never exceeds n_sigma at tau = 0 (N = 6, S6, primary cell) by more than 0.3 (MC error)", "all six pairs", sat)
P(f"\n{sum(CHK)}/{len(CHK)} controls pass; {time.time() - T0:.0f} s")
# JSON
js = {"controls": dict(passed=sum(CHK), n=len(CHK)), "classes": {f"{a}|{b_}": dict(stat=c[0], cal=c[1], n_sigma_tau0=c[2], n_sigma_tau25=c[3], stability=labels[(a, b_)]) for (a, b_), c in CLS.items()},
      "results": {"|".join(map(str, k)): {"|".join(map(str, kk)): v for kk, v in r.items()} for k, r in RES.items()}}
json.dump(js, open(os.path.join(LANE, "cfg219_preflight_results.json"), "w"), indent=1)
open(os.path.join(LANE, "cfg219_preflight.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(CHK) else 1)
