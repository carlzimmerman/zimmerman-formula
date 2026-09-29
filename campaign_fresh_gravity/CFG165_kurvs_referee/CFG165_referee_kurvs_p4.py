#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG165 -- independent referee re-derivation of CFG160 (KURVS a0(z) under the Kretschmer+2021 pressure-support
calibration, P4).  Written from CFG165_FROZEN_CRITERIA.md alone; no CFG140/141/160 script/out/json was open.

Main:      ZF_REPO=<repo> python3 CFG165_referee_kurvs_p4.py           -> CFG165_main.out / CFG165_main_results.json, rc 0
MUTATE:    MUTATE={1,1b,2,3,4,5,6} ...                               -> CFG165_MUTATE_<k>.out/.json, rc 1 iff the control bites
Independence stops at: CFG4_common (nu_mono, a0 constants; imported read-only), the Kretschmer alpha(x) as quoted, the data files.
"""
import os
import sys
import json
import math
import time

sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "2")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo():
    r = os.environ.get("ZF_REPO")
    if r and os.path.isdir(os.path.join(r, "data_assembly")):
        return r
    d = HERE
    for _ in range(8):
        if os.path.isdir(os.path.join(d, "data_assembly")) and os.path.isdir(os.path.join(d, "campaign_fresh_gravity")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("set ZF_REPO")


REPO = find_repo()
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
_mut_env = os.environ.get("MUTATE")
os.environ["MUTATE"] = "0"          # CFG4_common reads MUTATE at import for its own harness; not ours
import CFG4_common as CC              # noqa: E402  (read-only: nu_mono, A0)
if _mut_env is None:
    os.environ.pop("MUTATE")
else:
    os.environ["MUTATE"] = _mut_env
MODE = os.environ.get("MUTATE", "0")

G = CC.G_SI
MSUN = CC.MSUN
KPC = CC.KPC
A0 = CC.A0
FOOTS = ("canonical", "alt")
nu_mono = CC.nu_mono
LN10 = math.log(10.0)
OM, OL = 0.315, 0.685
MUS = (0.25, 0.67, 1.5, 4.0)
DELS = (-0.2, 0.0, 0.2)
KURVS_IDS = (3, 7, 8, 9, 11, 13, 15, 16, 17, 21)
DEC = dict(mu=0.67, delta=0.0, foot="canonical")


def rel(p):
    return os.path.relpath(p, REPO).replace(os.sep, "/")


def E_of_z(z):
    return np.sqrt(OM * (1 + np.asarray(z, float)) ** 3 + OL)


# ----------------------------------------------------------------------------------------------- alpha (Kretschmer Table 1 gas/disc, as quoted)
def alpha_K(x, scale=1.0):
    x = np.clip(np.asarray(x, float), 0.0, 4.0)
    return scale * (-0.146 * x ** 2 + 1.204 * x + 1.475)


# ----------------------------------------------------------------------------------------------- data
def read_csv(path):
    import csv
    with open(os.path.join(REPO, path), newline="") as f:
        return list(csv.DictReader(f))


def fnum(s):
    try:
        return float(s)
    except Exception:
        return float("nan")


class Sample:
    """arrays for one sample; fields: R kpc, V, eV km/s, Rd, Reff kpc, logM, z, inc rad, einc rad, sig(out), esig, sig0, esig0,
    grad2 (d sigma^2/dR km^2 s^-2 kpc^-1), mgas_abs (Msun or None), name"""
    pass


def load_sigma_profiles():
    rows = read_csv("data_assembly/arxiv_tables/kurvs_sigma_profiles/kurvs_sigma_profiles.csv")
    prof = {}
    for r in rows:
        k = int(r["kurvs_id"])
        if int(fnum(r["clipped_white_marker"])) == 1:          # the authors' clipped markers excluded (CFG141 frozen + disclosed)
            continue
        R = fnum(r["R_kpc"])
        s = fnum(r["sigma_obs_kms"])
        if int(fnum(r["has_errbar"])) == 1:
            e = 0.5 * (fnum(r["err_up_kms"]) + fnum(r["err_lo_kms"]))
        else:
            e = 0.20 * s                                       # declared 20% where no bar
        if not (np.isfinite(R) and np.isfinite(s) and np.isfinite(e) and e > 0):
            e = 0.20 * s if np.isfinite(s) else e
        prof.setdefault(k, []).append((R, s, e))
    return prof


def sigma_out(points, Rmax):
    """CFG141 frozen rules, with my declared reading (see criteria section 1): per side interpolate at Rmax where that
    side reaches it (average the sides that do, error in quadrature/n); if neither side reaches, error-weighted mean of the
    outermost three unclipped points of the merged |R| ordering.  Returns (sigma_out, e, route, grad2, n_out)."""
    P = [(abs(R), s, e, 1 if R >= 0 else -1) for R, s, e in points]
    P.sort()
    sides = {}
    for sgn in (1, -1):
        q = [(a, s, e) for a, s, e, sg in P if sg == sgn]
        if q:
            sides[sgn] = np.array(q)
    vals = []
    for sgn, q in sides.items():
        if q[-1, 0] >= Rmax and q[0, 0] <= Rmax:
            vals.append((np.interp(Rmax, q[:, 0], q[:, 1]), np.interp(Rmax, q[:, 0], q[:, 2])))
    merged = np.array(P)[:, :3]
    top3 = merged[-3:]
    w = 1.0 / top3[:, 2] ** 2
    # gradient of sigma^2 from a linear fit to the outermost three merged points (declared, unweighted)
    if len(top3) >= 3 and np.ptp(top3[:, 0]) > 0:
        grad2 = float(np.polyfit(top3[:, 0], top3[:, 1] ** 2, 1)[0])
    else:
        grad2 = 0.0
    if vals:
        s = float(np.mean([v[0] for v in vals]))
        e = float(math.sqrt(sum(v[1] ** 2 for v in vals)) / len(vals))
        return s, e, f"interp({len(vals)} side)", grad2, len(P)
    s = float(np.sum(w * top3[:, 1]) / np.sum(w))
    e = float(1.0 / math.sqrt(np.sum(w)))
    return s, e, "outer3", grad2, len(P)


def load_kurvs(ids=KURVS_IDS, inc_col="inc_sfr_deg"):
    I = {int(r["kurvs_id"]): r for r in read_csv("data_assembly/arxiv_tables/kurvs2023_integrated.csv")}
    K = {int(r["kurvs_id"]): r for r in read_csv("data_assembly/arxiv_tables/kurvs2023_kinematics.csv")}
    Vr = {int(r["kurvs_id"]): r for r in read_csv("data_assembly/arxiv_tables/kurvs2023_velocities_at_radii.csv")}
    F = {int(r["kurvs_id"]): r for r in read_csv("data_assembly/arxiv_tables/kurvs2023_fdm.csv")}
    prof = load_sigma_profiles()
    S = Sample()
    S.ids = list(ids)
    S.R = np.array([fnum(Vr[i]["R_halpha_max_kpc"]) for i in ids])
    S.V = np.array([fnum(Vr[i]["v_at_last_point_kms"]) for i in ids])
    S.eV = np.array([fnum(Vr[i]["e_v_last"]) for i in ids])
    S.Reff = np.array([fnum(I[i]["reff_kpc"]) for i in ids])
    S.Rd = S.Reff / 1.68
    S.logM = np.array([fnum(I[i]["logMstar"]) for i in ids])
    S.z = np.array([fnum(I[i]["z_halpha"]) for i in ids])
    S.inc = np.radians([fnum(I[i][inc_col]) for i in ids])
    S.einc = np.full(len(ids), math.radians(5.0))
    S.sig0 = np.array([fnum(K[i]["sigma0_kms"]) for i in ids])
    S.esig0 = np.array([fnum(K[i]["e_sigma0"]) for i in ids])
    so = [sigma_out(prof[i], S.R[j]) for j, i in enumerate(ids)]
    S.sig = np.array([a[0] for a in so])
    S.esig = np.array([a[1] for a in so])
    S.route = [a[2] for a in so]
    S.grad2 = np.array([a[3] for a in so])
    S.mgas_abs = None
    S.mass_err = 0.15
    S.name = [f"KURVS-{i}" for i in ids]
    S.fdm_ids = sorted(int(k) for k in F)
    return S


def load_sparc_anchor():
    d = os.path.join(REPO, "real_research", "data", "sparc_data")
    tab = {}
    with open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")) as f:
        for line in f:
            tok = line.split()
            if len(tok) != 19:
                continue
            try:
                v = [float(t) for t in tok[1:18]]
            except ValueError:
                continue
            tab[tok[0]] = dict(zip(("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q"), v))
    rows = []
    for fn in sorted(os.listdir(d)):
        if not fn.endswith("_rotmod.dat"):
            continue
        nm = fn[:-len("_rotmod.dat")]
        m = tab.get(nm)
        if m is None:
            continue
        try:
            a = np.genfromtxt(os.path.join(d, fn), comments="#")
        except Exception:
            continue
        if a.ndim != 2 or a.shape[1] < 6:
            continue
        Mst = 0.5 * m["L36"] * 1e9
        if not (m["Q"] <= 2 and m["Inc"] >= 30.0 and np.log10(Mst) >= 9.5):
            continue
        rows.append((nm, a[-1], m, a))
    S = Sample()
    S.ids = [r[0] for r in rows]
    S.name = S.ids
    S.R = np.array([r[1][0] for r in rows])
    S.V = np.array([r[1][1] for r in rows])
    S.eV = np.array([r[1][2] for r in rows])
    S.Rd = np.array([r[2]["Rdisk"] for r in rows])
    S.Reff = 1.68 * S.Rd
    S.logM = np.array([np.log10(0.5 * r[2]["L36"] * 1e9) for r in rows])
    S.z = np.zeros(len(rows))
    S.inc = np.radians([r[2]["Inc"] for r in rows])
    S.einc = np.radians([r[2]["eInc"] for r in rows])
    S.sig0 = np.full(len(rows), 10.0)
    S.esig0 = np.zeros(len(rows))
    S.sig = S.sig0.copy()
    S.esig = S.esig0.copy()
    S.grad2 = np.zeros(len(rows))
    S.mgas_abs = np.array([1.33 * r[2]["MHI"] * 1e9 for r in rows])
    S.mass_err = 0.10
    S.rot = [r[3] for r in rows]
    return S


def load_kross():
    rows = read_csv("data_assembly/high_z_tf_tables/kross_v2.csv")
    keep = []
    for r in rows:
        if r["kin_type"] not in ("RT", "RT+"):
            continue
        v, s = fnum(r["vc_kms_intrinsic_at_2Rhalf"]), fnum(r["sigma0_kms"])
        M, ri = fnum(r["mstar_msun"]), fnum(r["rim_kpc"])
        if not all(np.isfinite([v, s, M, ri, fnum(r["z_halpha"]), fnum(r["b_over_a"])])) or M <= 0 or ri <= 0 or s <= 0:
            continue
        if v / s < 1.0:
            continue
        keep.append(r)
    S = Sample()
    S.name = [r["name"] for r in keep]
    S.ids = S.name
    S.R = np.array([2 * fnum(r["rim_kpc"]) for r in keep])
    S.V = np.array([fnum(r["vc_kms_intrinsic_at_2Rhalf"]) for r in keep])
    eV = []
    for r in keep:
        lo, up = fnum(r["e_vc_lower"]), fnum(r["e_vc_upper"])
        eV.append(np.nanmean([lo, up]))
    S.eV = np.array(eV)
    S.Reff = np.array([fnum(r["rim_kpc"]) for r in keep])
    S.Rd = S.Reff / 1.68
    S.logM = np.log10(np.array([fnum(r["mstar_msun"]) for r in keep]))
    S.z = np.array([fnum(r["z_halpha"]) for r in keep])
    ba = np.clip(np.array([fnum(r["b_over_a"]) for r in keep]), 0.05, 0.999)
    S.inc = np.arccos(ba)
    S.einc = np.full(len(keep), math.radians(5.0))
    S.sig0 = np.array([fnum(r["sigma0_kms"]) for r in keep])
    e = np.array([fnum(r["e_sigma0"]) for r in keep])
    S.esig0 = np.where(np.isfinite(e), e, 0.2 * S.sig0)
    S.sig, S.esig = S.sig0.copy(), S.esig0.copy()
    S.grad2 = np.zeros(len(keep))
    S.mgas_abs = None
    S.mass_err = 0.15
    good = np.isfinite(S.eV) & (S.eV > 0)
    S.eV = np.where(good, S.eV, 0.2 * S.V)
    return S


# ----------------------------------------------------------------------------------------------- physics
def enclosed(y):
    return 1.0 - np.exp(-y) * (1.0 + y)


def gbar(S, mu, delta, gas_scale=2.0):
    """thin-exponential-disc enclosed baryons, spherical shortcut; stars y=R/Rd, gas y=R/(gas_scale Rd)."""
    Ms = 10.0 ** (S.logM + delta)
    Mg = S.mgas_abs if S.mgas_abs is not None else mu * Ms
    Mb = Ms * enclosed(S.R / S.Rd) + Mg * enclosed(S.R / (gas_scale * S.Rd))
    return G * Mb * MSUN / (S.R * KPC) ** 2


def gpred(gb, a):
    return nu_mono(gb / a) * gb


def slope(gb, a):
    f = 1.01
    return (np.log10(gpred(gb * f, a)) - np.log10(gpred(gb / f, a))) / (2 * math.log10(f))


# correction specs -----------------------------------------------------------------------------
def spec(kind, **kw):
    d = dict(kind=kind)
    d.update(kw)
    return d


def corr(S, sp, anchor=False):
    """returns (C, dC/dsigma) in km^2/s^2 and km/s: V_c^2 = V^2 + C.  Anchor/KROSS use sig0, no gradient."""
    k = sp["kind"]
    sig = S.sig
    if k == "P0":
        return np.zeros_like(S.V), np.zeros_like(S.V)
    if k == "P1":
        s = S.sig0
        return 2 * s ** 2 * S.R / S.Rd, 4 * s * S.R / S.Rd
    if k == "P2":
        return 2 * sig ** 2 * S.R / S.Rd, 4 * sig * S.R / S.Rd
    if k == "P3":
        C = sig ** 2 * S.R / S.Rd - S.R * S.grad2
        C = np.maximum(C, 0.0)
        return C, np.where(C > 0, 2 * sig * S.R / S.Rd, 0.0)
    if k in ("alpha", "P4"):
        if k == "P4":
            fac = sp.get("Refac", 1.0) if not anchor else sp.get("Refac_anchor", 1.0)
            x = S.R / (fac * S.Reff) - 1.0
            al = alpha_K(x, sp.get("scale", 1.0))
        else:
            al = sp["fn"](S, anchor)
        al = np.asarray(al, float) * np.ones_like(S.V)
        return al * sig ** 2, 2 * al * sig
    raise ValueError(k)


def vc2(S, sp, anchor=False):
    C, dC = corr(S, sp, anchor)
    if sp.get("invert"):
        f = 1.0 + C / S.V ** 2
        return S.V ** 2 / f, dC, f
    return S.V ** 2 + C, dC, None


def per_object(S, sp, mu, delta, foot, anchor=False, gas_scale=2.0):
    """returns dict of per-object arrays: delta_flat, delta_H, err_flat, err_H"""
    Vc2, dC, f = vc2(S, sp, anchor)
    R_m = S.R * KPC
    gobs = Vc2 * 1e6 / R_m
    gb = gbar(S, mu, delta, gas_scale)
    out = {}
    if f is None:
        dlog_dV = 2 * S.V / Vc2
        dlog_dsig = dC / Vc2
        v_inc = (S.V ** 2 / Vc2)
    else:
        # invert control: errors approximated by the bare velocity term
        dlog_dV = 2.0 / S.V
        dlog_dsig = 0.0 * dC
        v_inc = np.ones_like(S.V)
    ev = (dlog_dV * S.eV) / LN10
    es = (np.abs(dlog_dsig) * S.esig) / LN10 if not anchor else np.zeros_like(S.V)
    if sp["kind"] == "P1":
        es = (np.abs(dC) * S.esig0) / Vc2 / LN10
    ei = (2.0 * v_inc / LN10) * (1.0 / np.tan(S.inc)) * S.einc
    for law in ("flat", "H"):
        a = A0[foot] * (1.0 if law == "flat" else E_of_z(S.z))
        gp = gpred(gb, a)
        d = np.log10(gobs) - np.log10(gp)
        em = S.mass_err * np.abs(slope(gb, a))
        err = np.sqrt(ev ** 2 + es ** 2 + ei ** 2 + em ** 2)
        out["d_" + law] = d
        out["e_" + law] = err
    out["gobs"] = gobs
    out["gbar"] = gb
    out["Vc2_over_V2"] = Vc2 / S.V ** 2
    return out


def pool(d, e):
    w = 1.0 / e ** 2
    m = float(np.sum(w * d) / np.sum(w))
    err = float(1.0 / math.sqrt(np.sum(w)))
    n = len(d)
    chi2 = float(np.sum(w * (d - m) ** 2))
    dof = max(n - 1, 1)
    infl = math.sqrt(chi2 / dof) if chi2 / dof > 1 else 1.0
    return m, err * infl, chi2 / dof


_anchor_cache = {}


def anchor_pool(sp, delta, foot, AS=None):
    key = (json.dumps({k: (v if not callable(v) else id(v)) for k, v in sp.items()}, sort_keys=True, default=str), delta, foot, id(AS))
    if key in _anchor_cache:
        return _anchor_cache[key]
    po = per_object(AS, sp, None, delta, foot, anchor=True)
    r = {law: pool(po["d_" + law], po["e_" + law]) for law in ("flat", "H")}
    r["median_flat"] = float(np.median(po["d_flat"]))
    _anchor_cache[key] = r
    return r


def cell(S, AS, sp, mu, delta, foot, sp_anchor=None, gas_scale=2.0):
    po = per_object(S, sp, mu, delta, foot, gas_scale=gas_scale)
    ap = anchor_pool(sp_anchor if sp_anchor is not None else sp, delta, foot, AS)
    res = {}
    for law in ("flat", "H"):
        m, e, c = pool(po["d_" + law], po["e_" + law])
        am, ae, ac = ap["flat"] if law == "flat" else ap["H"]
        # anchor is z=0, E=1: both laws coincide there; use its flat pooled offset for both (frozen: anchor = Delta_flat)
        am, ae, ac = ap["flat"]
        dp = m - am
        sg = math.sqrt(e ** 2 + ae ** 2)
        res[law] = dict(raw=m, raw_err=e, chi2dof=c, anchor=am, anchor_err=ae, dprime=dp, sigma=sg, z=dp / sg)
    res["po"] = po
    return res


def classify(zf, zh):
    fw, rw = abs(zf) <= 2.0, abs(zh) <= 2.0
    if fw and zh < -2.0:
        return "lean flat"
    if rw and zf > 2.0:
        return "lean rival"
    if fw and rw:
        return "non-diagnostic (both within)"
    return "non-diagnostic (both outside)"


def sep_power(S, sp, mu, delta, foot):
    """R0: pooled expected separation of the laws (baryons only) / pooled per-object error with V replaced by the flat
    prediction's V (no observed velocity enters)."""
    gb = gbar(S, mu, delta)
    a0 = A0[foot]
    gf = gpred(gb, a0)
    gh = gpred(gb, a0 * E_of_z(S.z))
    dsep = np.log10(gh) - np.log10(gf)
    Vc2_f = gf * S.R * KPC / 1e6
    Vf = np.sqrt(np.maximum(Vc2_f, 1e-9))
    C, dC = corr(S, sp)
    Vp = np.sqrt(np.maximum(Vc2_f - C, 0.05 * Vc2_f))
    Vc2 = Vp ** 2 + C
    ev = (2 * Vp * S.eV / Vc2) / LN10
    es = (np.abs(dC) * S.esig / Vc2) / LN10
    ei = (2 * Vp ** 2 / Vc2 / LN10) * (1 / np.tan(S.inc)) * S.einc
    em = S.mass_err * np.abs(slope(gb, a0))
    err = np.sqrt(ev ** 2 + es ** 2 + ei ** 2 + em ** 2)
    w = 1 / err ** 2
    sep = float(np.sum(w * dsep) / np.sum(w))
    return sep, float(1 / math.sqrt(np.sum(w))), float(sep / (1 / math.sqrt(np.sum(w))))


# ----------------------------------------------------------------------------------------------- main
SP = dict(P0=spec("P0"), P1=spec("P1"), P2=spec("P2"), P3=spec("P3"), P4=spec("P4"))


def apply_mutation(S, AS, sp_p4, mode):
    """returns (S, AS, sp, decision-cell overrides, note)"""
    dec = dict(DEC)
    note = ""
    if mode == "1":
        sp_p4 = spec("alpha", fn=lambda S_, a: 0.0 * S_.V); note = "alpha = 0 (no pressure correction)"
    elif mode == "1b":
        sp_p4 = spec("alpha", fn=lambda S_, a: 1.0 + 0.0 * S_.V); note = "alpha = 1"
    elif mode == "2":
        sp_p4 = dict(spec("P4"), invert=True); note = "sign flipped: Vc2 = V2/(1+alpha sig2/V2)"
    elif mode == "4":
        dec["mu"] = 1.5; note = "decision cell moved to mu = 1.5"
    elif mode == "5":
        S.V = S.V * 10 ** 0.3; S.eV = S.eV * 10 ** 0.3; note = "KURVS v_last x 10^0.3"
    elif mode == "6":
        rng = np.random.default_rng(165)
        p = rng.permutation(len(S.sig))
        S.sig = S.sig[p]; S.esig = S.esig[p]; S.grad2 = S.grad2[p]; note = "sigma_out permuted (seed 165)"
    elif mode == "3":
        note = "flat/rival labels swapped in the verdict"
    return S, AS, sp_p4, dec, note


def main():
    t0 = time.time()
    outj = {"mode": MODE, "checks": {}, "numbers": {}}
    log = []

    def P(*a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)

    checks = []

    def check(name, ok, meas):
        checks.append((name, bool(ok)))
        outj["checks"][name] = dict(ok=bool(ok), measured=str(meas))
        P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {meas}")

    P("=" * 100)
    P(f"CFG165 referee re-derivation of CFG160 (P4).  MODE={MODE}.  repo=<repo>")
    P("=" * 100)
    S = load_kurvs()
    AS = load_sparc_anchor()
    S0 = load_kurvs()   # untouched copy for ladder under mutation
    sp_p4 = SP["P4"]
    S, AS, sp_p4, dec, note = apply_mutation(S, AS, sp_p4, MODE)
    if note:
        P("MUTATION:", note)

    # ---------------- controls
    P("\n-- controls")
    check("C2 alpha(0)=1.475, alpha(1)=2.533, alpha(4)=3.955 to 1e-9",
          abs(alpha_K(0) - 1.475) < 1e-9 and abs(alpha_K(1) - 2.533) < 1e-9 and abs(alpha_K(4) - 3.955) < 1e-9,
          (float(alpha_K(0)), float(alpha_K(1)), float(alpha_K(4))))
    xs = np.linspace(0, 4, 401)
    check("C2b alpha monotone increasing on [0,4]", bool(np.all(np.diff(alpha_K(xs)) > 0)), "")
    y = np.array([1e-12, 1e12])
    a_ = 1.0
    r1 = float(nu_mono(1e-12) * 1e-12 / math.sqrt(1e-12) - 1)
    r2 = float(nu_mono(1e12) - 1)
    check("C3 kernel limits (y=1e-12: g/sqrt(gbar a)-1 <1e-5; y=1e12: g/gbar-1 <1e-5)", abs(r1) < 1e-5 and abs(r2) < 1e-5, (r1, r2))
    check("C4a ten IDs are exactly the f_DM rows", sorted(S.ids) == S.fdm_ids and len(S.ids) == 10, S.ids)
    fin = all(np.all(np.isfinite(getattr(S, k))) for k in ("R", "V", "eV", "Rd", "logM", "z", "inc", "sig", "esig", "sig0"))
    check("C4b all KURVS inputs finite", fin, "")
    xK = S.R / S.Reff - 1
    check("C4c no galaxy has x outside [0,4]", bool(np.all((xK >= 0) & (xK <= 4))), (float(xK.min()), float(xK.max())))

    # P4 == P2 with alpha = 2 R/Rd (my own C1)
    sp_c1 = spec("alpha", fn=lambda S_, a: 2 * S_.R / S_.Rd)
    dmax = 0.0
    for mu in MUS:
        for dl in DELS:
            for ft in FOOTS:
                a = cell(S0, AS, SP["P2"], mu, dl, ft)
                b = cell(S0, AS, sp_c1, mu, dl, ft)
                for law in ("flat", "H"):
                    for k in ("dprime", "sigma"):
                        dmax = max(dmax, abs(a[law][k] - b[law][k]))
    check("C1 alpha := 2R/Rd reproduces my own P2 grid to 1e-12 (24 cells x 4)", dmax < 1e-12, dmax)

    # ---------------- sample table
    P("\n-- KURVS inputs (R_max kpc, V, sigma_out +- err [route], R/Rd, x)")
    for j in range(len(S.ids)):
        P(f"  {S.name[j]:9s} R={S.R[j]:5.1f} V={S.V[j]:6.1f}+-{S.eV[j]:4.1f} sig0={S.sig0[j]:4.0f} sig_out={S.sig[j]:5.1f}+-{S.esig[j]:4.1f} [{S.route[j]}] R/Rd={S.R[j]/S.Rd[j]:4.2f} x={xK[j]:5.2f} alpha={float(alpha_K(xK[j])):5.3f}")
    P(f"  SPARC anchor: n={len(AS.ids)}")
    outj["numbers"]["sigma_out"] = {S.name[j]: [float(S.sig[j]), float(S.esig[j]), S.route[j]] for j in range(len(S.ids))}
    outj["numbers"]["n_anchor"] = len(AS.ids)

    # ---------------- R0 power (before any g_obs)
    P("\n-- R0 power (expected separation / pooled error, before any g_obs; V replaced by the flat prediction's V)")
    pw = {}
    for mu in MUS:
        row = []
        for dl in DELS:
            for ft in FOOTS:
                sep, er, zz = sep_power(S, sp_p4, mu, dl, ft)
                row.append(zz)
        pw[mu] = (min(row), max(row))
        P(f"  mu={mu:5.2f}: separation/error over delta,footing in [{min(row):.2f}, {max(row):.2f}] sigma")
    outj["numbers"]["R0_power_range_over_cells"] = pw

    # ---------------- ladder
    P("\n-- ladder, decision cell (mu=0.67, delta=0, canonical), anchor-corrected; README targets in []")
    tgt = dict(P0=("-0.130 +-0.057", "-0.279"), P1=("+0.398 +-0.070", "+0.244"), P2=("+0.390 +-0.065", "+0.237 +-0.063"),
               P3=("+0.24 +-0.07", "+0.09 +-0.07"), P4=("+0.144 +-0.044", "-0.006 +-0.044"))
    ladder = {}
    for name in ("P0", "P1", "P2", "P3", "P4"):
        sp = sp_p4 if name == "P4" else SP[name]
        c = cell(S, AS, sp, DEC["mu"], DEC["delta"], DEC["foot"])
        ladder[name] = {law: {k: c[law][k] for k in ("dprime", "sigma", "z", "raw", "anchor", "anchor_err")} for law in ("flat", "H")}
        P(f"  {name}: flat {c['flat']['dprime']:+.3f} +-{c['flat']['sigma']:.3f} ({c['flat']['z']:+.1f}s)  rival {c['H']['dprime']:+.3f} +-{c['H']['sigma']:.3f} ({c['H']['z']:+.1f}s)   anchor {c['flat']['anchor']:+.3f}+-{c['flat']['anchor_err']:.3f}   [flat {tgt[name][0]}; rival {tgt[name][1]}]")
    outj["numbers"]["ladder_decision_cell"] = ladder
    a0c = per_object(AS, SP["P0"], None, 0.0, "canonical", anchor=True)
    P(f"  C1(README) anchor P0 median Delta_flat = {np.median(a0c['d_flat']):+.3f} [README +0.064], pooled {pool(a0c['d_flat'], a0c['e_flat'])[0]:+.3f} +-{pool(a0c['d_flat'], a0c['e_flat'])[1]:.3f} [README +0.092 +-0.013]")
    outj["numbers"]["anchor_P0_median_pooled"] = [float(np.median(a0c["d_flat"])), pool(a0c["d_flat"], a0c["e_flat"])[0], pool(a0c["d_flat"], a0c["e_flat"])[1]]

    # ---------------- decision cell and verdict
    cd = cell(S, AS, sp_p4, dec["mu"], dec["delta"], dec["foot"])
    zf, zh = cd["flat"]["z"], cd["H"]["z"]
    if MODE == "3":
        zf, zh = zh, zf     # labels swapped in the verdict (pure control of the verdict code)
    cls = classify(zf, zh)
    P("\n-- DECISION CELL (P4)" + ("  [MUTATED]" if MODE != "0" else ""))
    P(f"  Delta'_flat = {cd['flat']['dprime']:+.4f} +- {cd['flat']['sigma']:.4f} ({cd['flat']['z']:+.2f}s)   Delta'_H = {cd['H']['dprime']:+.4f} +- {cd['H']['sigma']:.4f} ({cd['H']['z']:+.2f}s)")
    P(f"  class (frozen map) = {cls}")
    outj["numbers"]["decision"] = {law: {k: cd[law][k] for k in ("dprime", "sigma", "z", "raw", "raw_err", "anchor", "anchor_err", "chi2dof")} for law in ("flat", "H")}
    outj["numbers"]["decision_class"] = cls

    if MODE in ("0",):
        # ---------------- sensitivity table
        P("\n-- sensitivity rows (canonical, delta=0) [README targets]")
        rows = {}
        for mu in MUS:
            c = cell(S, AS, sp_p4, mu, 0.0, "canonical")
            rows[f"mu={mu}"] = {law: (c[law]["dprime"], c[law]["sigma"], c[law]["z"]) for law in ("flat", "H")}
        for nm, sp in (("alpha x0.6", spec("P4", scale=0.6)), ("alpha x1.4", spec("P4", scale=1.4)), ("Re=2Reff", spec("P4", Refac=2.0))):
            c = cell(S, AS, sp, 0.67, 0.0, "canonical")
            rows[nm] = {law: (c[law]["dprime"], c[law]["sigma"], c[law]["z"]) for law in ("flat", "H")}
        c = cell(S, AS, spec("P4", Refac=2.0, Refac_anchor=2.0), 0.67, 0.0, "canonical")
        rows["Re=2Reff (anchor also 2x; my variant)"] = {law: (c[law]["dprime"], c[law]["sigma"], c[law]["z"]) for law in ("flat", "H")}
        for k, v in rows.items():
            P(f"  {k:38s} flat {v['flat'][0]:+.3f} +-{v['flat'][1]:.3f} ({v['flat'][2]:+.2f}s)   rival {v['H'][0]:+.3f} +-{v['H'][1]:.3f} ({v['H'][2]:+.2f}s)")
        outj["numbers"]["sensitivity"] = rows

        # ---------------- full 24-cell grid
        P("\n-- P4 24-cell grid (Delta' / sigma) : classes counted (>+2s, within, <-2s)")
        grid = {}
        cnt = {"flat": [0, 0, 0], "H": [0, 0, 0]}
        for mu in MUS:
            for dl in DELS:
                for ft in FOOTS:
                    c = cell(S, AS, sp_p4, mu, dl, ft)
                    grid[f"{mu}|{dl}|{ft}"] = {law: (c[law]["dprime"], c[law]["sigma"], c[law]["z"]) for law in ("flat", "H")}
                    for law in ("flat", "H"):
                        z = c[law]["z"]
                        cnt[law][0 if z > 2 else (2 if z < -2 else 1)] += 1
                    P(f"  mu={mu:4.2f} d={dl:+.1f} {ft:9s} flat {c['flat']['dprime']:+.3f} ({c['flat']['z']:+.1f}s)  rival {c['H']['dprime']:+.3f} ({c['H']['z']:+.1f}s)  {classify(c['flat']['z'], c['H']['z'])}")
        P(f"  counts [>+2s, within 2s, <-2s]: flat {cnt['flat']}  rival {cnt['H']}   [README: flat disfavoured 14; rival disfavoured (<-2s) 10, within 14]")
        outj["numbers"]["grid"] = grid
        outj["numbers"]["grid_counts"] = cnt
        # alt: P0-P3 grids counts
        for name in ("P2", "P3"):
            cn = {"flat": [0, 0, 0], "H": [0, 0, 0]}
            for mu in MUS:
                for dl in DELS:
                    for ft in FOOTS:
                        c = cell(S, AS, SP[name], mu, dl, ft)
                        for law in ("flat", "H"):
                            z = c[law]["z"]
                            cn[law][0 if z > 2 else (2 if z < -2 else 1)] += 1
            P(f"  {name} counts [>+2s, within, <-2s]: flat {cn['flat']}  rival {cn['H']}   [README {name}: flat survives 3 of 24 (P2) / disfav 16 (P3)]")
            outj["numbers"][f"grid_counts_{name}"] = cn

        # ---------------- per galaxy
        P("\n-- R3 per galaxy (central cell, unanchored): x, alpha, Vc2/V2 under P4 and P2, Delta_flat, Delta_H")
        p4 = per_object(S, sp_p4, 0.67, 0.0, "canonical")
        p2 = per_object(S, SP["P2"], 0.67, 0.0, "canonical")
        pg = {}
        for j in range(len(S.ids)):
            P(f"  {S.name[j]:9s} x={xK[j]:5.2f} alpha={float(alpha_K(xK[j])):5.3f} Vc2/V2 P4={p4['Vc2_over_V2'][j]:5.2f} P2={p2['Vc2_over_V2'][j]:5.2f}  Dflat P4={p4['d_flat'][j]:+.3f} (P2 {p2['d_flat'][j]:+.3f})  DH P4={p4['d_H'][j]:+.3f} gbar/a0={p4['gbar'][j]/A0['canonical']:.2f}")
            pg[S.name[j]] = dict(x=float(xK[j]), alpha=float(alpha_K(xK[j])), f4=float(p4["Vc2_over_V2"][j]), f2=float(p2["Vc2_over_V2"][j]),
                                 dflat=float(p4["d_flat"][j]), dH=float(p4["d_H"][j]))
        P(f"  ranges: x {xK.min():.2f}-{xK.max():.2f}; alpha {alpha_K(xK).min():.2f}-{alpha_K(xK).max():.2f}; Vc2/V2 P4 {p4['Vc2_over_V2'].min():.2f}-{p4['Vc2_over_V2'].max():.2f} (P2 {p2['Vc2_over_V2'].min():.2f}-{p2['Vc2_over_V2'].max():.2f}); Dflat {p4['d_flat'].min():+.2f}..{p4['d_flat'].max():+.2f}; DH {p4['d_H'].min():+.2f}..{p4['d_H'].max():+.2f}")
        P("  largest x: " + ", ".join(f"{S.name[j]} ({xK[j]:.2f})" for j in np.argsort(-xK)))
        P("  largest |Delta_flat - median|: " + ", ".join(f"{S.name[j]}" for j in np.argsort(-np.abs(p4['d_flat'] - np.median(p4['d_flat'])))[:4]))
        outj["numbers"]["per_galaxy"] = pg

    # ---------------- verdict and exit
    outj["elapsed_s"] = round(time.time() - t0, 1)
    if MODE == "0":
        okc = all(ok for _, ok in checks)
        P(f"\n{sum(ok for _, ok in checks)}/{len(checks)} controls pass; decision class = {cls}")
        with open(os.path.join(HERE, "CFG165_main_results.json"), "w") as f:
            json.dump(outj, f, indent=1, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
        return 0 if okc else 1
    bites = (cls != "lean rival")
    outj["bites"] = bites
    P(f"\nMUTATE={MODE}: class = {cls}  ->  {'CONTROL BITES (exit 1)' if bites else 'CONTROL FAILED TO BITE (exit 0)'}")
    with open(os.path.join(HERE, f"CFG165_MUTATE_{MODE}_results.json"), "w") as f:
        json.dump(outj, f, indent=1, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
    return 1 if bites else 0


if __name__ == "__main__":
    sys.exit(main())
