#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG331 -- does the framework's own treatment of the host environment remove the four SLUGGS centrals' excess?
Frozen criteria: FROZEN_CRITERIA.md (b0be6dc0c).  Base: a COPY of CFG330's K0 code (raw Forbes+17 GC velocities, ATLAS3D JAM
calibration, gamma 3, isotropic, outer bins, nu_mono, both footings; kappa = 1/2 FITTED).  Readings, never pooled:
  R-own  PAPER35 sec. 2 / FG001: the outermost bound system carries the phantom (centre: host baryons; member: own baryons)
  R-bar  law(stars + measured gas)        (R-barN reported: law(stars) + Newtonian gas)
  R-efe  1D external-field form, g_e from the host at the galaxy's position (0 at an exact centre)
CFG331_MUTATE=1: host mass x10 (gas + members); separate outputs.
"""
import os, sys, math, json
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
DATA = os.path.join(REPO, "real_research", "data")
sys.path.insert(0, LANES)
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4                                   # frozen nu_mono, read-only
MUTATE = os.environ.get("CFG331_MUTATE", "0") == "1"
HOSTX = 10.0 if MUTATE else 1.0
TAG = "_MUTATE" if MUTATE else ""
CENTRALS = (4486, 4365, 4374, 5846)
OUT = []
def P(s=""):
    print(s); OUT.append(s)


G = 6.674e-11; KPC = 3.0857e19; MSUN = 1.989e30
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
ARCSEC = math.pi / 180 / 3600
KERN = {"nu_mono": lambda y: np.asarray(C4.nu_mono(np.maximum(np.asarray(y, float), 1e-14)), float),
        "nu_RAR": lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(np.asarray(y, float), 1e-14))))}


# ------------------------------------------------------------------ raw readers (written for this audit)
def vizier(fn):
    rows = [l.rstrip("\n") for l in open(os.path.join(DATA, fn), encoding="latin-1") if l.strip() and not l.startswith("#")]
    k = next(i for i, l in enumerate(rows) if set(l.replace("\t", "").strip()) <= set("-"))
    hdr = [h.strip() for h in rows[k - 2].split("\t")]
    return [dict(zip(hdr, [x.strip() for x in l.split("\t")])) for l in rows[k + 1:]]


def f(x):
    try:
        return float(x)
    except Exception:
        return float("nan")


GAL = {}
for r in vizier("sluggs_forbes2017_galaxies.tsv"):
    if r["NGC"].isdigit():
        GAL[int(r["NGC"])] = dict(D=f(r["Dist"]), lMs=f(r["logM*"]), Re_as=f(r["Reff"]), vsys=f(r["Vsys"]), env=r["Env"])
GCS = {n: [] for n in GAL}
for r in vizier("sluggs_forbes2017_gcvel.tsv"):
    key = r["Star"].split("_")[0]
    if not key.startswith("NGC") or not key[3:].isdigit():
        continue
    n = int(key[3:])                                           # integer key: immune to the NGC0720 / NGC720 mismatch
    v, e, rg = f(r["HRV"]), f(r["e_HRV"]), f(r["Rgal"])
    if n in GCS and np.isfinite(v) and np.isfinite(rg):
        GCS[n].append((rg, v, e if np.isfinite(e) else 15.0))

A3 = {}
for l in open(os.path.join(DATA, "atlas3d_fj_table.tsv")):
    if l.startswith("#") or not l.strip():
        continue
    p = l.rstrip("\n").split("\t")
    if p[0] == "name":
        H = p; continue
    A3[p[0]] = dict(zip(H, p))


# ------------------------------------------------------------------ dispersion estimator (own: deconvolved Gaussian ML, 3-sigma clip)
def ml_sigma(v, e):
    s2 = max(np.var(v) - np.mean(e ** 2), 1.0)
    for _ in range(500):
        w = 1 / (s2 + e ** 2); mu = np.sum(w * v) / np.sum(w)
        # exact ML stationarity for s2: sum w (1 - w (v-mu)^2) = 0  -> fixed-point
        s2n = max(np.sum(w ** 2 * ((v - mu) ** 2 - e ** 2)) / np.sum(w ** 2), 1.0)
        if abs(s2n - s2) < 1e-9 * s2:
            s2 = s2n; break
        s2 = s2n
    return mu, math.sqrt(s2)


def clipped(a, vsys):
    a = a[np.abs(a[:, 1] - vsys) < 1200.0]
    for _ in range(20):
        mu, s = ml_sigma(a[:, 1], a[:, 2])
        k = np.abs(a[:, 1] - mu) < 3.0 * math.hypot(s, a[:, 2].mean())
        if k.all():
            break
        a = a[k]
    return a


def bins_for(n):
    g = GAL[n]
    a = np.array(GCS[n], float)
    if len(a) < 8:
        return None
    a = clipped(a, g["vsys"])
    if len(a) < 30:
        return None
    kpc_am = math.pi / 180 / 60 * g["D"] * 1e3
    R = a[:, 0] * kpc_am
    o = np.argsort(R); a, R = a[o], R[o]
    nb = max(2, min(6, len(a) // 25))
    idx = np.array_split(np.arange(len(a)), nb)                # equal-number bins
    out = []
    for ii in idx:
        if len(ii) < 12:
            continue
        mu, s = ml_sigma(a[ii, 1], a[ii, 2])
        out.append((float(np.median(R[ii])), s, len(ii)))
    if len(out) < 2:
        return None
    Re = g["Re_as"] * ARCSEC * g["D"] * 1e3
    Rb = np.array([b[0] for b in out]); Sb = np.array([b[1] for b in out])
    outer = Rb > max(Re, 2.0)
    if not outer.any():
        outer = np.ones(len(Rb), bool)
    return dict(n=n, N=len(a), Re=Re, Rb=Rb, Sb=Sb, outer=outer)


# ------------------------------------------------------------------ Jeans (own)
RG = np.geomspace(1e-3, 1e8, 6000); LR = np.log(RG)


def g_law(M, a_h, a0, kern):
    gN = G * M * MSUN * RG ** 2 / (RG + a_h) ** 2 / (RG * KPC) ** 2
    return gN * KERN[kern](gN / a0), gN


def sig_los(Rb, g, gamma, beta=0.0):
    # sigma_r^2(r) = r^(gamma - 2 beta) int_r^inf r'^(2 beta - gamma) g(r') dr'   (SI, dr in m)
    w = RG ** (2 * beta - gamma) * g * RG * KPC                # integrand per d ln r
    cum = np.concatenate([np.cumsum((0.5 * (w[1:] + w[:-1]) * np.diff(LR))[::-1])[::-1], [0.0]])
    s2 = cum / RG ** (2 * beta - gamma)
    u = np.linspace(0, 14, 4000); ch = np.cosh(u)
    out = []
    for R in Rb:
        r = R * ch
        s2r = np.exp(np.interp(np.log(r), LR, np.log(np.maximum(s2, 1e-30))))
        rho = r ** -gamma
        num = np.trapz((1 - beta / ch ** 2) * rho * s2r * r, u)
        den = np.trapz(rho * r, u)
        out.append(math.sqrt(num / den) / 1e3)
    return np.array(out)


def jam_mass(Mjam, r12, a0, kern, frac=0.5):
    fn = lambda lm: math.log10(frac * 10 ** lm * float(KERN[kern](G * frac * 10 ** lm * MSUN / (r12 * KPC) ** 2 / a0))) - math.log10(frac * Mjam)
    return 10 ** brentq(fn, math.log10(Mjam) - 4, math.log10(Mjam) + 1, xtol=1e-12)


def stat(x):
    x = np.asarray(x, float); e = x.std(ddof=1) / math.sqrt(len(x))
    return float(x.mean()), float(e), float(x.mean() / e)


# ------------------------------------------------------------------ sample (copied from CFG330 K0)
B = {n: bins_for(n) for n in sorted(GAL) if np.isfinite(GAL[n]["D"]) and np.isfinite(GAL[n]["lMs"])}
B = {n: b for n, b in B.items() if b is not None}
CFG55_16 = [1023, 2768, 3377, 3607, 4278, 4365, 4374, 4459, 4473, 4486, 4494, 4526, 4649, 4697, 5846, 7457]
OTHERS = [n for n in CFG55_16 if n not in CENTRALS]
for n in CFG55_16:
    a = A3[f"NGC{n:04d}"]; DS, DA = GAL[n]["D"], f(a["Dist_Mpc"])
    B[n]["Mjam"] = 10 ** (f(a["logML_JAM"]) + f(a["logL"])) * DS / DA
    B[n]["r12"] = 10 ** f(a["logr12"]) * ARCSEC * DS * 1e3
    B[n]["ah"] = B[n]["Re"] / 1.8153

# ------------------------------------------------------------------ host gas (CFG57 D1 / CFG323 urban_trunc conventions, re-implemented here)
GD = os.path.join(DATA, "cfg57_gas_sources")
MU_E, MP_G, KPC_CM, MSUN_G = 1.155, 1.67262192e-24, 3.0856775814913673e21, 1.98892e33
RHO_PER_NE = MU_E * MP_G * KPC_CM ** 3 / MSUN_G
RGAS = np.geomspace(1e-3, 3e4, 4000)


def rd_tsv(fn):
    L = [l.rstrip("\n").split("\t") for l in open(os.path.join(GD, fn)) if l.strip() and not l.startswith("#")]
    return [dict(zip([h.strip() for h in L[0]], [x.strip() for x in r])) for r in L[1:]]


LAK = {}
for r_ in rd_tsv("lakhchaura2018_ne_profiles.tsv"):
    LAK.setdefault(r_["name"], []).append(r_)
FUK = {r_["name"]: r_ for r_ in rd_tsv("fukazawa2006_table4.tsv")}
TR = {}
for l in open(os.path.join(LANES, "CFG323_sluggs_measured_tracers", "cfg323_transcribed_values.tsv")):
    p = l.rstrip("\n").split("\t")
    if len(p) == 3 and p[0] in ("C08", "U11"):
        TR[p[0]] = json.loads(p[2])
SRC1, SRC2 = (4486, 4374, 5846, 4649), (4365, 3607, 4697)


def am2kpc(a, D):
    return a * math.pi / 180 / 60 * D * 1e3


def gas_on_RG(n):
    """measured gas M(<r) on RG (Msun) and info, or (None, None)."""
    DS = GAL[n]["D"]; key = f"NGC{n}"; lg = np.log(RGAS)
    if n in SRC1:
        rows = sorted(LAK[key], key=lambda x: float(x["r_kpc"]))[:-1]                       # D1: drop the upturned outermost shell
        fD = DS / float(rows[0]["D_Mpc_paper"])
        r = np.array([float(x["r_kpc"]) for x in rows]) * fD; ne = np.array([float(x["ne_cm3"]) for x in rows]) * fD ** -0.5
        lr_, ln_ = np.log(r), np.log(ne)
        s = np.polyfit(lr_[-3:], ln_[-3:], 1)[0]
        lne = np.where(lg <= lr_[0], ln_[0], np.where(lg >= lr_[-1], ln_[-1] + s * (lg - lr_[-1]), np.interp(lg, lr_, ln_)))
        info = dict(src="Lakhchaura+18 D1", r_meas=float(r[-1]), slope=float(s))
        if n == 4486:                                                                           # urban_trunc
            c, u = TR["C08"], TR["U11"]; fc, fu = DS / c["D"], DS / u["D"]
            ne_c = lambda x: c["ne0"] * fc ** -0.5 * (1 + (x / (c["rc_kpc"] * fc)) ** 2) ** (-1.5 * c["beta"])
            rcmax = am2kpc(c["rmax_am"], c["D"]) * fc
            l2 = np.where(lg <= math.log(rcmax), np.log(ne_c(RGAS)), math.log(ne_c(rcmax)) + u["slope"] * (lg - math.log(rcmax)))
            l2 = np.where(lg > math.log(u["rmax_kpc"] * fu), -700.0, l2)
            lne = np.where(lg > lr_[-1], l2, lne)
            info.update(src="Lakhchaura D1 + Churazov+08 + Urban+11 (to 1.2 Mpc)", r_meas=float(u["rmax_kpc"] * fu), r_meas_C08=rcmax)
    elif n in SRC2:
        row = FUK[key]; fD = DS / float(row["D_Mpc"])
        ne10 = float(row["ne10_1e-3cm3"]) * 1e-3 * fD ** -0.5; r10 = 10.0 * fD
        shape = lambda x: (1 + (x / 1.0) ** 2) ** (-0.75)
        lne = np.log(ne10 * shape(RGAS) / shape(r10)); info = dict(src="Fukazawa+06 beta-model", r_meas=float(row["Rmax_kpc"]) * fD)
    else:
        return None, None
    dm = 4 * math.pi * RGAS ** 2 * RHO_PER_NE * np.exp(lne)
    M = np.concatenate([[dm[0] * RGAS[0] / 3], dm[0] * RGAS[0] / 3 + np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(RGAS))])
    return np.interp(LR, np.log(RGAS), M), info


# ------------------------------------------------------------------ members (2MRS table 3) and host sigma_V (KT17)
def read_2mrs():
    out, on = [], False
    for l in open(os.path.join(DATA, "2mrs_huchra2012.tsv")):
        if l.startswith("#Table"):
            on = "table3" in l; continue
        p = l.rstrip("\n").split("\t")
        if on and len(p) >= 4:
            v = [f(x) for x in p[:4]]
            if all(np.isfinite(v)):
                out.append(v)
    return np.array(out)


M2 = read_2mrs()
KT = {}
for l in open(os.path.join(DATA, "kt2017_groups_full.tsv")):
    p = l.split("\t")
    if len(p) > 8 and p[0].strip().isdigit():
        KT[int(p[0])] = dict(sig=f(p[4]), logMd=f(p[8]))
SIGV = {4486: KT[41220]["sig"], 4374: KT[41220]["sig"], 4365: KT[41220]["sig"], 5846: KT[53932]["sig"]}
RADEC = {}
for r in vizier("sluggs_forbes2017_galaxies.tsv"):
    if r["NGC"].isdigit():
        RADEC[int(r["NGC"])] = (f(r["RAJ2000"]), f(r["DEJ2000"]))


def sep_deg(ra1, de1, ra2, de2):
    d1, d2 = np.radians(de1), np.radians(de2)
    c = np.sin(d1) * np.sin(d2) + np.cos(d1) * np.cos(d2) * np.cos(np.radians(ra1 - ra2))
    return np.degrees(np.arccos(np.clip(c, -1, 1)))


def members(n):
    ra, de = RADEC[n]; s = sep_deg(ra, de, M2[:, 0], M2[:, 1]); i0 = int(np.argmin(s))
    Kc, czc = M2[i0, 3], M2[i0, 2]
    Rp = np.radians(s) * GAL[n]["D"] * 1e3
    k = (Rp < B[n]["Rb"][-1]) & (np.abs(M2[:, 2] - czc) < 3 * SIGV[n]) & (np.arange(len(M2)) != i0)
    return dict(match_deg=float(s[i0]), Kc=float(Kc), Rp=Rp[k], dK=M2[k, 3] - Kc)


# ------------------------------------------------------------------ fields
def gN_of(n, M, Mx):
    b = B[n]
    return G * (M * RG ** 2 / (RG + b["ah"]) ** 2 + Mx) * MSUN / (RG * KPC) ** 2


def nu(y):
    return KERN["nu_mono"](y)


def calib(n, a0, Mg):
    b = B[n]; Mjam, r12 = b["Mjam"], b["r12"]
    Mg12 = 0.0 if Mg is None else float(np.interp(math.log(r12), LR, Mg))
    fn = lambda lm: math.log10((0.5 * 10 ** lm + Mg12) * float(nu(G * (0.5 * 10 ** lm + Mg12) * MSUN / (r12 * KPC) ** 2 / a0))) - math.log10(0.5 * Mjam)
    lo = math.log10(Mjam) - 4
    if fn(lo) > 0:
        return float("nan")
    return 10 ** brentq(fn, lo, math.log10(Mjam) + 1, xtol=1e-12)   # total Hernquist mass (M/2 inside r12)


def off_g(n, g):
    b = B[n]; s = sig_los(b["Rb"], g, 3.0, 0.0)
    return float(np.mean(np.log10(b["Sb"][b["outer"]] / s[b["outer"]])))


def g_efe(gN, ge, a0):
    return nu(np.abs(gN + ge) / a0) * (gN + ge) - nu(ge / a0) * ge


def run(n, a0, x, reading, own_class=True, host_gas=True):
    """x = host-mass multiplier (0 = host removed); host_gas=False: a top-level system, no host baryons (C2)."""
    Mg = GAS[n][0] if host_gas else None
    Mg = None if (Mg is None or x == 0) else Mg * x
    if reading == "efe":
        M = jam_mass(B[n]["Mjam"], B[n]["r12"], a0, "nu_mono"); gN = gN_of(n, M, 0.0)
        return off_g(n, g_efe(gN, GE[(n, a0)] * (x > 0), a0))
    M = calib(n, a0, Mg) if Mg is not None else jam_mass(B[n]["Mjam"], B[n]["r12"], a0, "nu_mono")
    Mx = np.zeros_like(RG) if Mg is None else Mg.copy()
    if reading == "own" and own_class and n in (4486, 5846) and x > 0:
        mb = MEM[n]
        for rp, dk in zip(mb["Rp"], mb["dK"]):
            Mx = Mx + x * M * 10 ** (-0.4 * dk) * (RG >= rp)
    if reading == "barN":
        gN0 = gN_of(n, M, 0.0); return off_g(n, nu(gN0 / a0) * gN0 + G * Mx * MSUN / (RG * KPC) ** 2)
    gN = gN_of(n, M, Mx)
    return off_g(n, nu(gN / a0) * gN)


GAS = {n: gas_on_RG(n) if n in CENTRALS + (4649, 3607, 4697) else (None, None) for n in CFG55_16}
MEM = {n: members(n) for n in CENTRALS}
# external field at the galaxy (R-efe)
GE = {}
for a0 in A0.values():
    for n in CFG55_16:
        GE[(n, a0)] = 0.0
    m87 = jam_mass(B[4486]["Mjam"], B[4486]["r12"], a0, "nu_mono")
    D87 = GAL[4486]["D"]
    th = sep_deg(*RADEC[4374], *RADEC[4486]); Rp = math.radians(th) * D87 * 1e3
    Mv = m87 * Rp ** 2 / (Rp + B[4486]["ah"]) ** 2 + float(np.interp(math.log(Rp), LR, GAS[4486][0]))
    gNe = G * Mv * MSUN / (Rp * KPC) ** 2; GE[(4374, a0)] = float(nu(gNe / a0) * gNe)
    th = math.radians(sep_deg(*RADEC[4365], *RADEC[4486])); D1, D2 = GAL[4365]["D"], D87
    r3 = math.sqrt(D1 ** 2 + D2 ** 2 - 2 * D1 * D2 * math.cos(th)) * 1e3
    gNe = G * 10 ** KT[41220]["logMd"] * MSUN / (r3 * KPC) ** 2; GE[(4365, a0)] = float(nu(gNe / a0) * gNe)
    GE[("r", 4374)], GE[("r", 4365)] = Rp, r3

# ------------------------------------------------------------------ run
K0 = json.load(open(os.path.join(LANES, "CFG330_sluggs_icgc_clip", "cfg330_summary_K0.json")))["CFG330"]
P("=" * 110); P("CFG331 -- SLUGGS centrals: the host environment, three framework readings" + ("   *** MUTATE: host mass x10 ***" if MUTATE else "")); P("=" * 110)
P("Inputs per central (gas profile; measured edge vs GC bins; members inside the outermost bin):")
for n in CENTRALS:
    i = GAS[n][1]; b = B[n]; mb = MEM[n]
    P(f"  NGC{n}: {i['src']}; measured to {i['r_meas']:.1f} kpc; GC bins {b['Rb'][0]:.1f}-{b['Rb'][-1]:.1f} kpc (outer median "
      f"{np.median(b['Rb'][b['outer']]):.1f}); 2MRS match {mb['match_deg'] * 3600:.1f}\"; members {len(mb['Rp'])} "
      + ", ".join(f"R_p {r:.0f} kpc dK {d:+.2f}" for r, d in zip(mb["Rp"], mb["dK"])))
P(f"  R-efe: g_e(NGC4374) at R_p {GE[('r', 4374)]:.0f} kpc from M87 = {GE[(4374, A0['canonical'])] / A0['canonical']:.3f} a0; "
  f"g_e(NGC4365) at r_3D {GE[('r', 4365)]:.0f} kpc from Virgo (KT17 M_d) = {GE[(4365, A0['canonical'])] / A0['canonical']:.4f} a0 (canonical)")

READ = ("own", "bar", "barN", "efe")
RES = {}
for foot, a0 in A0.items():
    for rd in READ:
        RES[(foot, rd)] = {n: run(n, a0, HOSTX, rd) for n in CENTRALS}
    RES[(foot, "base")] = {n: run(n, a0, 0.0, "bar") for n in CFG55_16}
    RES[(foot, "others_owngas")] = {n: run(n, a0, 1.0, "bar") for n in OTHERS}

P("\nPer-galaxy offsets (dex) and means:")
SUM = {}
for foot in A0:
    oth = K0[foot]["others"][0]; cen0 = K0[foot]["centrals"][0]; ex0 = cen0 - oth
    P(f"  [{foot}] K0 centrals {cen0:+.4f}, others {oth:+.4f}, excess {ex0:.4f}")
    for rd in READ:
        r = RES[(foot, rd)]; m = stat([r[n] for n in CENTRALS]); ex = m[0] - oth
        if rd == "barN":
            v = "reported"
        else:
            v = None
        SUM[(foot, rd)] = dict(per={f"NGC{n}": r[n] for n in CENTRALS}, mean=m, excess=ex, drop=1 - ex / ex0, within=abs(m[0] - oth) <= 0.05)
        P(f"    R-{rd:5}: " + "  ".join(f"NGC{n} {r[n]:+.3f}" for n in CENTRALS) + f" | mean {m[0]:+.4f} +- {m[1]:.4f} | excess {ex:.4f} (drop {100 * (1 - ex / ex0):.0f}%)")
    so = stat(list(RES[(foot, "others_owngas")].values()))
    P(f"    reported: the 12 others with their own measured gas (4649, 3607, 4697) -> mean {so[0]:+.4f} (K0 {oth:+.4f})")

P("\nVerdicts (both footings):")
VERD = {}
for rd in ("own", "bar", "efe"):
    s = [SUM[(ft, rd)] for ft in A0]
    VERD[rd] = "ENVIRONMENT EXPLAINS" if all(x["within"] for x in s) else ("PARTIAL" if all(x["drop"] >= 0.5 for x in s) else "NOT SUPPORTED")
    P(f"  R-{rd}: {VERD[rd]}  (drop canonical {100 * s[0]['drop']:.0f}%, alt {100 * s[1]['drop']:.0f}%)")

# ------------------------------------------------------------------ checks
P("\nCHECKS"); ok = []
def check(lbl, cond, det):
    ok.append(bool(cond)); P(f"  [{'PASS' if cond else 'FAIL'}] {lbl}\n         {det}")
if not MUTATE:
    d1 = max(abs(run(n, a0, 0.0, rd) - K0[ft]["per_galaxy"][f"NGC{n}"]) for ft, a0 in A0.items() for rd in READ for n in CENTRALS)
    d1b = max(abs(RES[(ft, "base")][n] - K0[ft]["per_galaxy"][f"NGC{n}"]) for ft in A0 for n in CFG55_16)
    check("C1 host mass zero: every reading reproduces CFG330 K0 per galaxy to 1e-9 dex", max(d1, d1b) < 1e-9, f"max |diff| {max(d1, d1b):.2e}")
    d2 = max(abs(run(n, a0, 1.0, "own", own_class=False, host_gas=False) - K0[ft]["per_galaxy"][f"NGC{n}"]) for ft, a0 in A0.items() for n in OTHERS)
    check("C2 R-own on the 12 non-centrals as top-level systems (no host baryons) leaves each unchanged to 1e-9", d2 < 1e-9, f"max |diff| {d2:.2e}")
    c3 = all(RES[(ft, "efe")][n] >= K0[ft]["per_galaxy"][f"NGC{n}"] - 1e-12 for ft in A0 for n in CENTRALS)
    c3b = all(abs(RES[(ft, "efe")][n] - K0[ft]["per_galaxy"][f"NGC{n}"]) < 1e-9 for ft in A0 for n in (4486, 5846))
    check("C3 R-efe: exact centres unchanged; no offset lowered", c3 and c3b, f"centres unchanged {c3b}; none lowered {c3}")
else:
    m = SUM[("canonical", "own")]["mean"][0]
    check("M1 MUTATE host x10: the centrals' R-own mean goes negative (over-correction flagged)", m < 0, f"R-own canonical mean {m:+.4f}")

json.dump(dict(mutate=MUTATE, host_x=HOSTX, verdicts=VERD,
               summary={f"{ft}|{rd}": v for (ft, rd), v in SUM.items()},
               g_ext_over_a0={f"NGC{n}|{ft}": GE[(n, a0)] / a0 for ft, a0 in A0.items() for n in CENTRALS},
               members={f"NGC{n}": dict(Rp=MEM[n]["Rp"].tolist(), dK=MEM[n]["dK"].tolist()) for n in CENTRALS},
               gas={f"NGC{n}": GAS[n][1] for n in CENTRALS}),
          open(os.path.join(HERE, f"cfg331_environment{TAG}_results.json"), "w"), indent=1, default=float)
P(f"\n  {sum(ok)}/{len(ok)} checks pass")
open(os.path.join(HERE, f"cfg331_environment{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(ok) else 1)
