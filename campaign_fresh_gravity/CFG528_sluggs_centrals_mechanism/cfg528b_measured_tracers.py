#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG528b -- the four SLUGGS centrals with MEASURED GC density profiles and MEASURED anisotropy.
Frozen criteria: FROZEN_CRITERIA_v2.md (d7a546f9c).  Machinery: CFG528's helpers (exec'd read-only up to its header print, which
itself execs CFG331 read-only).  New: variable-beta, multi-population Jeans for tabulated rho(r).
kappa = 1/2 FITTED; footings 9.36e-11 | 1.13e-10; nu_mono.  CFG528B_MUTATE=1: MA (gamma 3, beta 0 reproduce), MB (gamma 4, beta -0.5).
"""
import os, sys, math, json, hashlib, itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("CFG528B_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""

# ------------------------------------------------------------------ 0. CFG528 helpers (read-only; no CFG528 output is written)
for k in ("CFG528_MUTATE", "CFG528_POSTFREEZE"):
    os.environ.pop(k, None)
_p = os.path.join(HERE, "cfg528_mechanism.py")
_src = open(_p).read()
NS = {"__file__": _p, "__name__": "cfg528_ro"}
exec(compile(_src[:_src.index('\nP("=" * 120)')], "cfg528_mechanism", "exec"), NS)
B, GAL, A0, CEN, RG, LR, G, KPC = NS["B"], NS["GAL"], NS["A0"], NS["CEN"], NS["RG"], NS["LR"], NS["G"], NS["KPC"]
build, score, SIG, ORIG = NS["build"], NS["score"], NS["SIG"], NS["ORIG"]
set_distance, restore, EPSF, Mpop = NS["set_distance"], NS["restore"], NS["eps_row"], NS["Mpop"]
sig_los = NS["sig_los"]
C331 = NS["C331"]; K0J = NS["K0J"]
NS["OUT"].clear()
OUT = []
def P(s=""):
    print(s); OUT.append(s)

EXT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg528_work", "src"))

# ------------------------------------------------------------------ 1. deprojection and tracer profiles
UU = np.linspace(0.0, 12.0, 6001); CHU = np.cosh(UU)
MR = (RG >= 0.3) & (RG <= 1.0e6)


def abel(dS):
    r = RG[MR]; out = np.empty_like(r)
    for i in range(0, len(r), 500):
        rr = r[i:i + 500, None] * CHU[None, :]
        out[i:i + 500] = -np.trapz(dS(rr), UU, axis=1) / math.pi
    rho = np.zeros_like(RG); rho[MR] = np.maximum(out, 0.0); rho[RG < 0.3] = rho[MR][0]
    return rho


def bn_cb(n):
    return 2 * n - 1 / 3 + 4 / (405 * n) + 46 / (25515 * n ** 2)


def sersic_rho(Re, n, b, S0=1.0):
    def dS(R):
        x = np.maximum(R / Re, 1e-300); e = np.exp(-b * x ** (1.0 / n))
        return -S0 * e * b / (n * Re) * x ** (1.0 / n - 1.0)
    return abel(dS)


def as2kpc(a, n):
    return a * math.pi / 180 / 3600 * GAL[n]["D"] * 1e3


def pl_rho(gamma):
    return RG ** (-gamma)


TR = {}
for l in open(os.path.join(os.path.dirname(HERE), "CFG323_sluggs_measured_tracers", "cfg323_transcribed_values.tsv")):
    p = l.rstrip("\n").split("\t")
    if len(p) == 3 and not l.startswith("#"):
        try:
            TR[p[0]] = json.loads(p[2])
        except Exception:
            pass


def m87_agnello():
    S0 = [1.0, TR["A14_Sib"][0], TR["A14_Srb"][0]]; rho = np.zeros_like(RG)
    for j in range(3):
        n_ = TR["A14_n"][j][0]; rho = rho + sersic_rho(as2kpc(TR["A14_Re_as"][j][0], 4486), n_, bn_cb(n_), S0[j])
    return rho


def m87_peng():
    z = TR["Z14"]
    return sersic_rho(as2kpc(z["R0_as"][0], 4486), z["n"][0], z["bn_log10"] * math.log(10))


def n4365_blom(dn=0.0, dRe=0.0):
    n_ = 2.68 + dn; Re = (6.1 + dRe) * 60.0
    return sersic_rho(as2kpc(Re, 4365), n_, 1.9992 * n_ - 0.3271)


def n5846_pops(f=1.0, g=1.0):
    """red and blue rho (Napolitano+14 L133/L148); f scales n, g scales R_e (both pops jointly)."""
    def one(n_, Re_as, Ne):
        n_ = n_ * f; Re = as2kpc(Re_as * g, 5846); b = bn_cb(n_)
        # N_e is the surface density AT R_e: Sigma = N_e exp(-b[(R/Re)^(1/n) - 1]) -> S0 = N_e e^b
        return sersic_rho(Re, n_, b, Ne * math.exp(b))
    return one(2.9, 160.0, 3.3), one(2.9, 780.0, 0.24)


# ------------------------------------------------------------------ 2. anisotropy profiles
def beta_const(b):
    return np.full_like(RG, b)


def beta_zhu(shift=0.0):
    nodes_r = np.log([5.0, 15.0, 40.0, 120.0]); nodes_b = np.array([-0.2, 0.0, 0.2, 0.0])
    return np.interp(LR, nodes_r, nodes_b) + shift


def beta_nap(b2, ra_as, shift=0.0, c=6.0):
    ra = as2kpc(ra_as, 5846)
    return (b2 + shift) * RG ** c / (RG ** c + ra ** c)


# ------------------------------------------------------------------ 3. variable-beta multi-population Jeans
UP = np.linspace(0, 14, 4000); CHP = np.cosh(UP)


def sig_multi(Rb, g, pops):
    """pops: list of (rho, beta_array).  sigma_los^2 = sum_j num_j / sum_j den_j."""
    num = np.zeros(len(Rb)); den = np.zeros(len(Rb))
    for rho, beta in pops:
        lnF = np.concatenate([[0.0], np.cumsum(0.5 * (2 * beta[1:] + 2 * beta[:-1]) * np.diff(LR))])
        w = rho * np.exp(lnF) * g * RG * KPC
        cum = np.concatenate([np.cumsum((0.5 * (w[1:] + w[:-1]) * np.diff(LR))[::-1])[::-1], [0.0]])
        lP = np.log(np.maximum(cum / np.exp(lnF), 1e-300)); lrho = np.log(np.maximum(rho, 1e-300))
        for i, R in enumerate(Rb):
            r = R * CHP; lr = np.log(r); bt = np.interp(lr, LR, beta)
            num[i] += np.trapz((1 - bt / CHP ** 2) * np.exp(np.interp(lr, LR, lP)) * r, UP)
            den[i] += np.trapz(np.exp(np.interp(lr, LR, lrho)) * r, UP)
    return np.sqrt(num / den) / 1e3


def off_pops(n, g, pops):
    b = B[n]; s = sig_multi(b["Rb"], g, pops); o = b["outer"]
    return float(np.mean(np.log10(b["Sb"][o] / s[o])))


READ = {"K0": {}, "bar": dict(gas="extrap"), "own": dict(gas="extrap", own=True)}


def field(n, a0, reading, **kw):
    r = build(n, a0, **{**READ[reading], **kw})
    return None if r is None else r[0]


# measured tracer specs (computed once; distance rows rebuild them)
def measured_pops(n, var=None):
    var = var or {}
    if n == 4486:
        rho = m87_peng() if var.get("dens") == "peng" else m87_agnello()
        return [(rho, beta_zhu(var.get("bshift", 0.0)) if "bconst" not in var else beta_const(var["bconst"]))]
    if n == 4365:
        rho = pl_rho(var["gamma"]) if "gamma" in var else n4365_blom(var.get("dn", 0.0), var.get("dRe", 0.0))
        return [(rho, beta_const(var.get("bconst", 0.0)))]
    if n == 4374:
        return [(pl_rho(var.get("gamma", 2.09)), beta_const(var.get("bconst", 0.0)))]
    if n == 5846:
        red, blue = n5846_pops(var.get("f", 1.0), var.get("g", 1.0))
        if "bconst" in var:
            return [(red, beta_const(var["bconst"])), (blue, beta_const(var["bconst"]))]
        s = var.get("bshift", 0.0)
        if var.get("red_only"):
            return [(red, beta_nap(0.43, 200.0, s))]
        return [(red, beta_nap(0.43, 200.0, s)), (blue, beta_nap(0.15, 100.0, s))]


ROWS = {}
def row(name, fn, note=""):
    res = {}
    for foot, a0 in A0.items():
        per = {}
        for n in CEN:
            try:
                per[n] = fn(n, a0, foot)
            except Exception as e:
                per[n] = None; P(f"    [{name}] NGC{n} {foot}: not computable ({e})")
        res[foot] = score(per, foot)
    closes = all(res[ft]["closes"] for ft in A0)
    ROWS[name] = dict(note=note, closes_both=closes, **res)
    for ft in A0:
        r = res[ft]
        P(f"  {name:36s} {ft:9s} " + " ".join(f"{(r['per'][f'NGC{n}'] if r['per'][f'NGC{n}'] is not None else float('nan')):+.3f}({r['Z'][f'NGC{n}']:+5.1f})" for n in CEN)
          + f" | mean {r['mean']:+.3f} Zc {r['Z_class']:+5.1f} | cleared {r['n_cleared']}/4" + (f" rev {r['n_reversed']}" if r['n_reversed'] else ""))
    P(f"  {'':36s} -> CLOSES both footings: {closes}" + (f"  ({note})" if note else ""))
    return ROWS[name]


ok = []
def check(lbl, cond, det):
    ok.append(bool(cond)); P(f"  [{'PASS' if cond else 'FAIL'}] {lbl}\n         {det}")


P("=" * 124)
P("CFG528b -- SLUGGS centrals with MEASURED GC density profiles and anisotropy" + ("   *** MUTATE ***" if MUTATE else ""))
P("=" * 124)
P("columns: offset dex (Z) for NGC 4486 | 4365 | 4374 | 5846; sigma_i = CFG466 bootstrap")

if not MUTATE:
    # ---------------------------------------------------------------- controls
    P("\nCONTROLS")
    k1 = 0.0
    for ft, a0 in A0.items():
        for n in CEN:
            g = field(n, a0, "K0")
            for bt in (0.0, 0.5):
                s_new = sig_multi(B[n]["Rb"], g, [(pl_rho(3.0), beta_const(bt))]); s_old = sig_los(B[n]["Rb"], g, 3.0, bt)
                k1 = max(k1, float(np.max(np.abs(np.log10(s_new / s_old)))))
    check("K1 new solver vs CFG331 sig_los (rho r^-3, beta 0 / +0.5) <= 1e-3 dex", k1 <= 1e-3, f"max |dlog sigma| {k1:.2e}")
    a = 2.0
    pl = abel(lambda R: -2 * R / a ** 2 * 2 * (1 + R ** 2 / a ** 2) ** -3 / (math.pi * a ** 2) * 1.0)    # d/dR of Sigma = (1/pi a^2)(1+R^2/a^2)^-2
    ana = 3 / (4 * math.pi * a ** 3) * (1 + RG ** 2 / a ** 2) ** -2.5
    k = (RG > 1) & (RG < 120)
    k2 = float(np.max(np.abs(pl[k] / ana[k] - 1)))
    check("K2 Abel deprojection of a Plummer profile <= 1e-3 relative (1-120 kpc)", k2 <= 1e-3, f"max rel {k2:.2e}")
    c4 = {ft: off_pops(4486, field(4486, a0, "K0"), [(m87_agnello(), beta_const(0.0))]) for ft, a0 in A0.items()}
    k3 = max(abs(c4["canonical"] - 0.21780), abs(c4["alt"] - 0.20620))
    check("K3 M87 Agnello central, beta 0, K0 reproduces CFG466 C4 (+0.2178 / +0.2062) <= 2e-3", k3 <= 2e-3, f"{c4['canonical']:+.5f} / {c4['alt']:+.5f}")
    log = open(os.path.join(HERE, "FETCH_LOG.md")).read(); bad = []
    for l in log.splitlines():
        p = [x.strip() for x in l.split("|")]
        if len(p) > 4 and len(p[-2]) == 64:
            fn = os.path.join(EXT, p[1].replace("/", "_") + ".tar")
            h = hashlib.sha256(open(fn, "rb").read()).hexdigest() if os.path.exists(fn) else "missing"
            if h != p[-2]:
                bad.append(p[1])
    check("K4 SHA-256 of every source tar matches FETCH_LOG.md", not bad, f"mismatches: {bad}")

    # ---------------------------------------------------------------- measured rows
    P("\nTRACERS (local 3D slope -dln rho/dln r at the outer GC bins; beta at those radii)")
    for n in CEN:
        pops = measured_pops(n); rho = sum(p[0] for p in pops)
        sl = -np.gradient(np.log(np.maximum(rho, 1e-300)), LR); ro = B[n]["Rb"][B[n]["outer"]]
        P(f"    NGC{n}: gamma_loc {np.round(np.interp(np.log(ro), LR, sl), 2).tolist()} at R {np.round(ro, 1).tolist()} kpc; "
          + "beta " + "; ".join(str(np.round(np.interp(np.log(ro), LR, p[1]), 2).tolist()) for p in pops))
    P("\nROW M (measured density + measured beta; NGC 4365 / 4374 beta = 0)")
    for rd in ("K0", "bar", "own"):
        row(f"M {rd}", lambda n, a0, ft, rd=rd: off_pops(n, field(n, a0, rd), measured_pops(n)))
    P("\nREPORTED")
    row("M own, beta 0 for all", lambda n, a0, ft: off_pops(n, field(n, a0, "own"), measured_pops(n, dict(bconst=0.0))))
    alt = {4486: dict(dens="peng"), 4365: dict(gamma=2.21), 4374: dict(gamma=2.22), 5846: dict(red_only=True)}
    row("M own, alt tracer (Peng / PL 2.21 / red 2.22 / red-only)", lambda n, a0, ft: off_pops(n, field(n, a0, "own"), measured_pops(n, alt[n])))
    row("M own, NGC 4374 blue 2.00 (others M)", lambda n, a0, ft: off_pops(n, field(n, a0, "own"), measured_pops(n, dict(gamma=2.00) if n == 4374 else None)))

    # ---------------------------------------------------------------- joint best case
    P("\nJOINT BEST CASE (R-own, heaviest admissible IMF, D x1.1, most favourable density/beta within quoted +-2 sigma)")
    EPS = EPSF("salp"), EPSF("chab2x"), EPSF("chab")
    EPSD = {"salp": EPS[0], "chab2x": EPS[1], "chab": EPS[2]}
    def heaviest(n, ft):
        best, bm = "jam", None
        for r in ("salp", "chab2x", "chab"):
            if EPSD[r][ft][f"NGC{n}"] <= 0.06:
                m = Mpop(n, r)
                if m > build(n, A0[ft])[2] and (bm is None or m > bm):
                    best, bm = r, m
        return best
    GRID = {4486: [dict(dens=d, bshift=s) for d in ("agn", "peng") for s in (-0.1, 0.0, 0.1)],
            4365: [dict(dn=a_, dRe=b_, bconst=c_) for (a_, b_) in [(0, 0), (-0.82, -2.4), (-0.82, 2.4), (0.82, -2.4), (0.82, 2.4)] for c_ in (-0.5, 0.0, 0.5)],
            4374: [dict(gamma=gm, bconst=c_) for gm in (1.85, 2.09, 2.33) for c_ in (-0.5, 0.0, 0.5)],
            5846: [dict(f=f_, g=g_, bshift=s) for f_ in (0.8, 1.0, 1.2) for g_ in (0.8, 1.0, 1.2) for s in (-0.1, 0.0, 0.1)]}
    JBEST = {}
    def joint(n, a0, ft):
        set_distance(n, 1.1 * ORIG[n]["D"])
        try:
            g = field(n, a0, "own", mstar=heaviest(n, ft))
            vals = [(off_pops(n, g, measured_pops(n, v)), v) for v in GRID[n]]
        finally:
            restore(n)
        o, v = min(vals, key=lambda t: t[0])
        JBEST[(n, ft)] = dict(offset=o, var=v, imf=heaviest(n, ft), range=[min(t[0] for t in vals), max(t[0] for t in vals)])
        return o
    J = row("J joint best case", joint)
    for ft in A0:
        P(f"    {ft}: " + "; ".join(f"{n}: {JBEST[(n, ft)]['var']} IMF {JBEST[(n, ft)]['imf']} (grid range {JBEST[(n, ft)]['range'][0]:+.3f}..{JBEST[(n, ft)]['range'][1]:+.3f})" for n in CEN))

    # ---------------------------------------------------------------- verdict
    P("\nVERDICT (frozen order)")
    if ROWS["M K0"]["closes_both"]:
        V = "DATA-ISSUE"
    elif ROWS["M bar"]["closes_both"] or ROWS["M own"]["closes_both"]:
        V = "MECHANISM FOUND"
    elif J["closes_both"]:
        V = "NOT DIAGNOSTIC"
    else:
        V = f"GENUINE TENSION ({min(J[ft]['Z_class'] for ft in A0):.1f} sigma, joint best case, less favourable footing)"
    P(f"  headline: {V}")
    P("  row M Z_class: " + "; ".join(f"{rd} " + ", ".join(f"{ft} {ROWS['M ' + rd][ft]['Z_class']:+.2f} ({ROWS['M ' + rd][ft]['n_cleared']}/4)" for ft in A0) for rd in ("K0", "bar", "own")))
    P("  J Z_class: " + ", ".join(f"{ft} {J[ft]['Z_class']:+.2f} ({J[ft]['n_cleared']}/4)" for ft in A0))
    res = dict(lane="CFG528b", frozen_commit="d7a546f9c", mutate=False, kappa="1/2 FITTED", a0=A0, rows=ROWS,
               joint_choice={f"NGC{n}|{ft}": v for (n, ft), v in JBEST.items()}, headline=V, checks_pass=sum(ok), checks_total=len(ok))
else:
    P("\nMUTATE")
    ma = 0.0
    for ft, a0 in A0.items():
        for n in CEN:
            ma = max(ma, abs(off_pops(n, field(n, a0, "K0"), [(pl_rho(3.0), beta_const(0.0))]) - K0J[ft]["per_galaxy"][f"NGC{n}"]),
                     abs(off_pops(n, field(n, a0, "own"), [(pl_rho(3.0), beta_const(0.0))]) - C331[f"{ft}|own"]["per"][f"NGC{n}"]))
    check("MA gamma 3, beta 0 reproduces CFG528 K0 and R-own per central <= 1e-3 dex", ma <= 1e-3, f"max |diff| {ma:.2e}")
    MK0 = {ft: {n: off_pops(n, field(n, a0, "K0"), measured_pops(n)) for n in CEN} for ft, a0 in A0.items()}
    mb = row("MB gamma 4, beta -0.5, K0", lambda n, a0, ft: off_pops(n, field(n, a0, "K0"), [(pl_rho(4.0), beta_const(-0.5))]))
    cb = (not mb["closes_both"]) and all(mb[ft]["per"][f"NGC{n}"] >= MK0[ft][n] for ft in A0 for n in CEN)
    check("MB must NOT close; every offset >= row-M K0", cb, "; ".join(f"{ft}: " + ", ".join(f"{n} {mb[ft]['per'][f'NGC{n}'] - MK0[ft][n]:+.3f}" for n in CEN) for ft in A0))
    res = dict(lane="CFG528b", mutate=True, rows=ROWS, checks_pass=sum(ok), checks_total=len(ok))

P(f"\n  {sum(ok)}/{len(ok)} checks pass")
json.dump(res, open(os.path.join(HERE, f"cfg528b_measured_tracers{TAG}_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg528b_measured_tracers{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(ok) else 1)
