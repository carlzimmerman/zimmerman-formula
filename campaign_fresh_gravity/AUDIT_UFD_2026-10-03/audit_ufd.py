#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUDIT_UFD_2026-10-03 -- independent re-derivation of the Milky Way ultra-faint (UFD) offset that CFG313 reports for the
bare law on native inputs (+0.325 dex, 3.77 sigma canonical | +0.304 dex, 3.55 sigma alt).

Written from scratch: reads the Local Volume Database MW table on disk directly, re-implements the estimator, the
Kaplan-Meier median with the 9 upper limits, the bootstrap and the floor, and then varies one declared input at a
time (no fitting, no knob scan; kappa = 1/2 fixed, both footings).  The only record function imported is nu_mono
(to show the kernel used by the record equals the adopted nu_mono in the UFD regime).

Run: python3 campaign_fresh_gravity/AUDIT_UFD_2026-10-03/audit_ufd.py
Outputs: audit_ufd.out, audit_ufd_results.json (next to this file).
"""
import os, sys, csv, math, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
DATA = os.path.join(REPO, "real_research", "data", "dsph")
OUT = []


def P(s=""):
    print(s); OUT.append(s)


# ------------------------------------------------------------------ constants (SI); both footings, kappa = 1/2 fixed
G, MSUN, PC, KPC = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
UPS_V0 = 2.0
MW_MB = 6.0e10          # the record's MW baryonic mass for the EFE rival (h43 / FG001)
LMC_MB = 1.5e10         # LMC baryons, used only in one EFE variant for the 7 LMC-hosted systems (stars ~2.7e9 + HI ~0.5e9 is lower; declared upper-ish value)


def fnum(v):
    try:
        x = float(v); return x if np.isfinite(x) else None
    except (TypeError, ValueError):
        return None


def nu_exp(y):
    y = max(float(y), 1e-12); return 1.0 / (1.0 - math.exp(-math.sqrt(y)))


# ------------------------------------------------------------------ 1. raw table
rows = list(csv.DictReader(open(os.path.join(DATA, "lvd_dwarf_mw.csv"))))
RES, UL = [], []
for r in rows:
    MV = fnum(r["M_V"]); sig = fnum(r["vlos_sigma"]); ul = fnum(r["vlos_sigma_ul"])
    rh_sph = fnum(r["rhalf_sph_physical"]); rh_maj = fnum(r["rhalf_physical"])
    rh = rh_sph or rh_maj
    Dh = fnum(r["distance_host"]) or fnum(r["distance_gc"])
    if MV is None or MV <= -7.7 or rh is None or Dh is None:
        continue
    d = dict(name=r["name"], host=r["host"], MV=MV, LV=10 ** (0.4 * (4.83 - MV)), rh=rh, rh_maj=rh_maj or rh,
             ell=fnum(r["ellipticity"]), Dgc=fnum(r["distance_gc"]), Dhost=Dh, ms_lvd=fnum(r["mass_stellar"]),
             MHI=(10 ** fnum(r["mass_HI"]) if fnum(r["mass_HI"]) is not None else 0.0), ref=r["ref_vlos"],
             feh=fnum(r["metallicity_spectroscopic"]))
    if sig is not None and ul is None and sig > 0:
        d["sig"] = sig; d["esig"] = 0.5 * ((fnum(r["vlos_sigma_em"]) or 0.2 * sig) + (fnum(r["vlos_sigma_ep"]) or 0.2 * sig)); RES.append(d)
    elif ul is not None:
        d["sig_ul"] = ul; UL.append(d)
P("AUDIT_UFD 2026-10-03 -- independent re-derivation of the MW ultra-faint offset (bare law, native inputs)")
P("=" * 110)
P(f"1. RAW TABLE: lvd_dwarf_mw.csv ({len(rows)} rows). Cut M_V > -7.7, r_half and distance present: {len(RES)} resolved + {len(UL)} upper limits")
P(f"   upper limits: {', '.join(d['name'] for d in UL)}")
P(f"   HI present in any UFD: {sum(d['MHI'] > 0 for d in RES + UL)}")

# spot checks: L_V and M* against the LVD's own mass_stellar column (log10 M*, Upsilon_V = 2 per PROVENANCE), r_sph = r_maj sqrt(1 - e)
P("\n   Spot check (5 systems): raw LVD columns vs what the estimator uses")
P(f"   {'name':16s} {'M_V':>6s} {'L_V':>9s} {'2L_V':>9s} {'LVD M*':>9s} {'r_maj':>7s} {'e':>5s} {'r_maj*sqrt(1-e)':>15s} {'r_sph':>7s} {'sigma':>6s} ref")
spot = {}
for nm in ("Bootes I", "Ursa Major I", "Segue 1", "Tucana II", "Coma Berenices"):
    d = next(x for x in RES if x["name"] == nm)
    rs = d["rh_maj"] * math.sqrt(1 - d["ell"]) if d["ell"] is not None else float("nan")
    P(f"   {nm:16s} {d['MV']:6.2f} {d['LV']:9.3e} {2 * d['LV']:9.3e} {10 ** d['ms_lvd']:9.3e} {d['rh_maj']:7.1f} {d['ell']:5.2f} {rs:15.1f} {d['rh']:7.1f} {d['sig']:6.2f} {d['ref']}")
    spot[nm] = dict(MV=d["MV"], M_star_used=2 * d["LV"], M_star_LVD=10 ** d["ms_lvd"], r_sph=d["rh"], r_sph_check=rs, sigma=d["sig"], ref=d["ref"])
ms_dev = max(abs(math.log10(2 * d["LV"]) - d["ms_lvd"]) for d in RES + UL if d["ms_lvd"] is not None)
P(f"   max |log10(2 L_V) - LVD mass_stellar| over all 40: {ms_dev:.3f} dex (the LVD's own Upsilon_V = 2 stellar mass)")

# McConnachie 2012 cross-check (older compilation, independent transcription)
mc = {}
for r in csv.DictReader(open(os.path.join(DATA, "mcconnachie2012_dsph.csv"))):
    mc[r["Name"].replace("(I)", "").replace("(", "").replace(")", "").strip().lower()] = r
alias = {"bootes i": "bootes", "segue 1": "segue", "segue 2": "segue ii", "ursa major i": "ursa major i", "coma berenices": "coma berenices",
         "ursa major ii": "ursa major ii", "willman 1": "willman 1", "bootes ii": "bootes ii", "canes venatici ii": "canes venatici ii",
         "leo iv": "leo iv", "leo v": "leo v", "hercules": "hercules", "pisces ii": "pisces ii"}
P("\n   Cross-check against McConnachie 2012 (on disk; older values): sigma [km/s], M_V, R_half [pc]")
xc = []
for d in RES + UL:
    k = alias.get(d["name"].lower())
    if k and k in mc:
        m = mc[k]; s_new = d.get("sig", d.get("sig_ul"))
        P(f"   {d['name']:18s} LVD sigma {s_new:5.2f}{' (UL)' if 'sig_ul' in d else ''}  M12 sigma {m['sigma*']:>5s}+-{m['e_sigma*']:<4s} | M_V {d['MV']:6.2f} vs {m['VMag']:>5s} | r_maj {d['rh_maj']:6.1f} vs {m['R2']:>5s}")
        xc.append((d["name"], s_new, fnum(m["sigma*"])))


# ------------------------------------------------------------------ 2. estimators
def g_iso(Mb, r_m, a0, kern=nu_exp):
    gN = G * 0.5 * Mb * MSUN / r_m ** 2
    return gN * kern(gN / a0)


def g_efe(Mb, r_m, a0, gNe):
    """the record's algebraic EFE (h43 / FG001 a_int): g = gNi nu(|gNi+gNe|/a0) + gNe (nu_tot - nu_e)."""
    gNi = G * 0.5 * Mb * MSUN / r_m ** 2
    nt = nu_exp((gNi + gNe) / a0); ne = nu_exp(gNe / a0)
    return gNi * nt + gNe * (nt - ne)


def sigma_pred(d, foot, ups=UPS_V0, mode="iso", r_key="rh", kern=nu_exp, host_mass=None, mass_factor=1.0):
    a0 = A0[foot]
    Mb = (ups * d["LV"] + 1.33 * d["MHI"]) * mass_factor
    r_m = (4.0 / 3.0) * d[r_key] * PC
    if mode == "iso":
        g = g_iso(Mb, r_m, a0, kern)
    elif mode == "deep481":                         # isolated deep-MOND: sigma^4 = (4/81) G M a0
        return (4.0 / 81.0 * G * Mb * MSUN * a0) ** 0.25 / 1e3
    elif mode in ("efe", "efe_lmc"):
        Mh = MW_MB; D = d["Dgc"] or d["Dhost"]
        if mode == "efe_lmc" and d["host"] == "lmc":
            Mh = LMC_MB; D = d["Dhost"]
        gNe = G * Mh * MSUN / (D * KPC) ** 2
        g = g_efe(Mb, r_m, a0, gNe)
    else:
        raise ValueError(mode)
    return math.sqrt(g * r_m / 3.0) / 1e3


def km_median(x, xu):
    """Kaplan-Meier median of offsets x (detections) with upper limits xu (offset <= xu): flip sign -> right-censored."""
    y = np.concatenate([-np.asarray(x), -np.asarray(xu)]); ev = np.concatenate([np.ones(len(x), bool), np.zeros(len(xu), bool)])
    o = np.lexsort((~ev, y)); y, ev = y[o], ev[o]
    S, n, i = 1.0, len(y), 0
    while i < len(y):
        t = y[i]; j = i; dd = 0; cc = 0
        while j < len(y) and y[j] == t:
            dd += int(ev[j]); cc += int(not ev[j]); j += 1
        if dd:
            S *= 1.0 - dd / n
            if S <= 0.5:
                return -t
        n -= dd + cc; i = j
    return -y[-1]


def offsets(foot, sample=None, ulsample=None, **kw):
    s = RES if sample is None else sample; u = UL if ulsample is None else ulsample
    x = np.array([math.log10(d["sig"] / sigma_pred(d, foot, **kw)) for d in s])
    xu = np.array([math.log10(d["sig_ul"] / sigma_pred(d, foot, **kw)) for d in u])
    return x, xu


def boot(x, xu, nb=1000, seed=42):
    rng = np.random.default_rng(seed); v = []
    for _ in range(nb):
        v.append(km_median(x[rng.integers(0, len(x), len(x))], xu[rng.integers(0, len(xu), len(xu))]))
    return float(np.std(v))


def stat(foot, ups_floor=(1.0, 4.0), sample=None, ulsample=None, **kw):
    x, xu = offsets(foot, sample, ulsample, **kw)
    m = km_median(x, xu); e = boot(x, xu)
    kw2 = {k: v for k, v in kw.items() if k != "ups"}
    lo = km_median(*offsets(foot, sample, ulsample, ups=ups_floor[0], **kw2)); hi = km_median(*offsets(foot, sample, ulsample, ups=ups_floor[1], **kw2))
    f = 0.5 * abs(hi - lo); tot = math.sqrt(e ** 2 + f ** 2)
    return dict(km=m, res_median=float(np.median(x)), res_mean=float(np.mean(x)), boot=e, f_ups=f, tot=tot, z=m / tot, n=len(x), nul=len(xu))


RESULTS = {"spot": spot, "max_dlogMstar_vs_LVD": ms_dev}
P("\n2. REPRODUCTION (record estimator: sigma^2 = g r / 3 at r = 4/3 r_half(circularised), M = 2 L_V, half mass inside r, isolated)")
for foot in A0:
    s = stat(foot)
    RESULTS[f"base|{foot}"] = s
    P(f"   {foot:9s}: KM median {s['km']:+.4f}  boot {s['boot']:.4f}  Upsilon floor {s['f_ups']:.4f}  total {s['tot']:.4f}  z {s['z']:+.2f}   "
      f"(resolved median {s['res_median']:+.4f}, resolved mean {s['res_mean']:+.4f}; n {s['n']} + {s['nul']} UL)")
P("   record (CFG45/CFG313 law row): canonical +0.3245 +- 0.0860 z +3.77 | alt +0.3045 +- 0.0858 z +3.55")

# kernel check: the record's exponential kernel vs the adopted nu_mono over the UFD y range
sys.path.insert(0, LANES)
try:
    import CFG7_common as C
    ys = []
    for d in RES + UL:
        r_m = (4.0 / 3.0) * d["rh"] * PC; gN = G * 0.5 * UPS_V0 * d["LV"] * MSUN / r_m ** 2
        ys.append(gN / A0["canonical"])
    ys = np.array(ys)
    dk = max(abs(float(C.nu_mono(np.array([y]))[0]) / nu_exp(y) - 1) for y in ys)
    P(f"\n   kernel: UFD y = g_N/a0 spans {ys.min():.1e} .. {ys.max():.1e} (median {np.median(ys):.1e}); max |nu_mono/nu_exp - 1| there = {dk:.1e}")
    for foot in A0:
        x1, xu1 = offsets(foot, kern=lambda y: float(C.nu_mono(np.array([y]))[0]))
        P(f"   {foot:9s}: KM median with nu_mono {km_median(x1, xu1):+.4f}")
    RESULTS["kernel"] = dict(y_min=float(ys.min()), y_max=float(ys.max()), y_med=float(np.median(ys)), max_rel_diff=dk)
except Exception as ex:                                            # pragma: no cover
    P(f"   kernel check skipped: {ex}")

# ------------------------------------------------------------------ 3. one-at-a-time input variants (declared list; nothing tuned)
P("\n3. VARIANTS (one input changed at a time; offset = KM median of 31 + 9; z uses the same error recipe)")
VAR = [
    ("deep-MOND isolated sigma^4 = (4/81) G M a0", dict(mode="deep481")),
    ("major-axis r_half instead of circularised", dict(r_key="rh_maj")),
    ("Upsilon_V = 1.0", dict(ups=1.0)),
    ("Upsilon_V = 1.5 (old metal-poor, Chabrier/Kroupa-like)", dict(ups=1.5)),
    ("Upsilon_V = 3.0 (Salpeter-like, old)", dict(ups=3.0)),
    ("EFE rival: MW 6e10 point mass at D_gc (record's a_int)", dict(mode="efe")),
    ("EFE rival, LMC-hosted 7 feel the LMC (1.5e10) instead", dict(mode="efe_lmc")),
]
for lab, kw in VAR:
    row = {}
    for foot in A0:
        s = stat(foot, **kw); row[foot] = s
    RESULTS["var|" + lab] = row
    c, a = row["canonical"], row["alt"]
    P(f"   {lab:58s} can {c['km']:+.3f} (z {c['z']:+.2f}, d {c['km'] - RESULTS['base|canonical']['km']:+.3f}) | alt {a['km']:+.3f} (z {a['z']:+.2f})")

# Upsilon_V needed (isolated estimator): z < 2 and zero offset
P("\n   Upsilon_V the isolated law would need (mass_factor on 2 L_V; reported, not a fit):")
for foot in A0:
    base = RESULTS[f"base|{foot}"]
    need = {}
    for target, lab in ((2.0 * base["tot"], "z = 2"), (0.0, "offset 0")):
        lo, hi = 1.0, 1e4
        for _ in range(80):
            mid = math.sqrt(lo * hi)
            m = km_median(*offsets(foot, mass_factor=mid))
            lo, hi = (mid, hi) if m > target else (lo, mid)
        need[lab] = 2.0 * math.sqrt(lo * hi)
    RESULTS[f"ups_need|{foot}"] = need
    P(f"   {foot:9s}: Upsilon_V for z = 2 (error held) {need['z = 2']:.1f}; for zero offset {need['offset 0']:.1f}")

# ------------------------------------------------------------------ 4. sample / equilibrium cuts
P("\n4. SAMPLE CUTS (reported; sample choice is the test of selection-neutrality)")
TIDAL = {"Tucana III", "Bootes III", "Hercules", "Willman 1", "Segue 2", "Tucana V"}   # recalled literature list of disturbed / disrupting systems; not from the file
cuts = [
    ("resolved only (no limits), median", None),
    ("drop recalled tidally disturbed (Tuc III, Boo III, Her, Wil 1, Seg 2, Tuc V)", lambda d: d["name"] not in TIDAL),
    ("D_gc > 80 kpc only", lambda d: (d["Dgc"] or 0) > 80),
    ("D_gc <= 80 kpc only", lambda d: (d["Dgc"] or 0) <= 80),
    ("drop the 7 LMC-hosted", lambda d: d["host"] != "lmc"),
    ("sigma error <= 25%", lambda d: ("sig" in d and d["esig"] / d["sig"] <= 0.25)),
]
for lab, fn in cuts:
    row = {}
    for foot in A0:
        if fn is None:
            x, xu = offsets(foot)
            row[foot] = dict(km=float(np.median(x)), n=len(x), nul=0, z=float("nan"))
            continue
        s_ = [d for d in RES if fn(d)]; u_ = [d for d in UL if fn(d)]
        if len(u_) == 0:
            x, _ = offsets(foot, s_, [])
            m = float(np.median(x)); rng = np.random.default_rng(42)
            e = float(np.std([np.median(x[rng.integers(0, len(x), len(x))]) for _ in range(1000)]))
            f = 0.5 * abs(float(np.median(offsets(foot, s_, [], ups=4.0)[0])) - float(np.median(offsets(foot, s_, [], ups=1.0)[0])))
            tot = math.sqrt(e ** 2 + f ** 2); row[foot] = dict(km=m, tot=tot, z=m / tot, n=len(x), nul=0)
        else:
            row[foot] = stat(foot, sample=s_, ulsample=u_)
    RESULTS["cut|" + lab] = row
    c, a = row["canonical"], row["alt"]
    P(f"   {lab:72s} n {c['n']:2d}+{c['nul']}: can {c['km']:+.3f} (z {c['z']:+.2f}) | alt {a['km']:+.3f} (z {a['z']:+.2f})")

# mean-of-offsets statistic, weighted by measurement error (resolved only), as a statistic cross-check
P("\n5. STATISTIC CROSS-CHECKS (resolved 31)")
for foot in A0:
    x, _ = offsets(foot)
    ex = np.array([d["esig"] / d["sig"] / math.log(10) for d in RES])
    w = 1 / ex ** 2; wm = float(np.sum(w * x) / np.sum(w)); we = float(1 / math.sqrt(np.sum(w)))
    f = RESULTS[f"base|{foot}"]["f_ups"]
    P(f"   {foot:9s}: inverse-variance mean {wm:+.3f} +- {we:.3f} (stat) ; with the Upsilon floor z {wm / math.sqrt(we ** 2 + f ** 2):+.2f};"
      f" chi2/dof about zero offset {float(np.sum(w * x ** 2)) / len(x):.1f}; about the mean {float(np.sum(w * (x - wm) ** 2)) / (len(x) - 1):.1f}")
    RESULTS[f"wmean|{foot}"] = dict(mean=wm, err=we, z_with_floor=wm / math.sqrt(we ** 2 + f ** 2))
    # narrower, SPS-motivated floor (Upsilon 1.5..3.0) instead of the record's 1..4
    s2 = stat(foot, ups_floor=(1.5, 3.0))
    RESULTS[f"sps_floor|{foot}"] = s2
    P(f"   {foot:9s}: with an SPS-range floor (Upsilon_V 1.5..3.0) instead of 1..4: total {s2['tot']:.3f}, z {s2['z']:+.2f}")

# per-object table
P("\n6. PER-OBJECT (canonical, isolated, Upsilon_V 2): name | host | D_gc | M* | r_sph | sigma_obs | sigma_pred | offset | EFE sigma_pred")
per = []
for d in sorted(RES + UL, key=lambda q: q["name"]):
    sp = sigma_pred(d, "canonical"); se = sigma_pred(d, "canonical", mode="efe")
    so = d.get("sig", d.get("sig_ul")); tag = "UL" if "sig_ul" in d else "  "
    P(f"   {d['name']:18s} {d['host']:3s} {d['Dgc'] or 0:6.1f} {2 * d['LV']:9.2e} {d['rh']:6.1f} {so:5.2f}{tag} {sp:5.2f} {math.log10(so / sp):+.3f} {se:5.2f}")
    per.append(dict(name=d["name"], host=d["host"], Dgc=d["Dgc"], Mstar=2 * d["LV"], r_sph=d["rh"], sigma=so, upper_limit=("sig_ul" in d),
                    sigma_pred_iso=sp, offset=math.log10(so / sp), sigma_pred_efe=se))
RESULTS["per_object"] = per

# ------------------------------------------------------------------ 7. reported: the law on INITIAL baryons (FG001 class A / CFG35 conservation read literally)
# M_b,init = R_ind x M_b,now with CFG317's leaky-box R_ind (nominal yield; per object, matched by stellar mass). NOT candidate B as frozen; a candidate escape only.
P("\n7. REPORTED ESCAPE CHECK: isolated law on the INITIAL baryons, M_init = R_ind M_now, R_ind from CFG317's leaky box (nominal yield -0.2, and -0.5 / +0.1)")
try:
    j317 = json.load(open(os.path.join(LANES, "CFG317_baryon_loss_cold_mass", "cfg317_baryon_loss_results.json")))["numbers"]
    allok = True; esc = {}
    for yv in ("-0.2", "-0.5", "0.1"):
        EU, EL, EC = j317["EST"][yv + "|ufd"], j317["EST"][yv + "|ul"], j317["EST"][yv + "|cls"]
        names = j317["NAMES"]["ufd"]
        R_res = {}
        for nm, e in zip(names, EU):
            d = next(x for x in RES if x["name"] == nm)
            if e is None:
                R_res[nm] = 1.0; continue
            allok &= abs(e["Ms"] / (2 * d["LV"]) - 1) < 1e-6
            R_res[nm] = 10 ** e["lR"] if e.get("lR") is not None else 1.0
        R_ul = []
        for d, e in zip(UL, EL):
            if e is None:
                R_ul.append(1.0); continue
            allok &= abs(e["Ms"] / (2 * d["LV"]) - 1) < 1e-6
            R_ul.append(10 ** e["lR"] if e.get("lR") is not None else 1.0)
        for foot in A0:
            x = np.array([math.log10(d["sig"] / sigma_pred(d, foot, mass_factor=R_res[d["name"]])) for d in RES])
            xu = np.array([math.log10(d["sig_ul"] / sigma_pred(d, foot, mass_factor=R)) for d, R in zip(UL, R_ul)])
            esc[f"ufd|{yv}|{foot}"] = km_median(x, xu)
        # MW classicals (stars only x R; my own isolated estimator, no infall gas): what the same reading does to them
        cl = []
        for r in rows:
            MV = fnum(r["M_V"]); sig = fnum(r["vlos_sigma"]); rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
            if MV is None or MV > -7.7 or sig is None or rh is None:
                continue
            cl.append(dict(name=r["name"], LV=10 ** (0.4 * (4.83 - MV)), rh=rh, rh_maj=rh, MHI=(10 ** fnum(r["mass_HI"]) if fnum(r["mass_HI"]) else 0.0), sig=sig))
        nmc = j317["NAMES"]["cls"]
        for foot in A0:
            x0, x1 = [], []
            for nm, e in zip(nmc, EC):
                d = next((q for q in cl if q["name"] == nm), None)
                if d is None or e is None or e.get("lR") is None:
                    continue
                x0.append(math.log10(d["sig"] / sigma_pred(d, foot)))
                x1.append(math.log10(d["sig"] / sigma_pred(d, foot, mass_factor=10 ** e["lR"])))
            esc[f"cls|{yv}|{foot}"] = (float(np.median(x0)), float(np.median(x1)), len(x1))
    RESULTS["escape_initial_baryons"] = {k: v for k, v in esc.items()}
    P(f"   stellar-mass match to CFG317's per-object table: {'exact' if allok else 'MISMATCH'}")
    for yv in ("-0.2", "-0.5", "0.1"):
        c0, c1, nc = esc[f"cls|{yv}|canonical"]
        P(f"   yield {yv:>4s}: UFD KM median can {esc[f'ufd|{yv}|canonical']:+.3f} | alt {esc[f'ufd|{yv}|alt']:+.3f}   ;   MW classical (n {nc}, stars only) median can {c0:+.3f} -> {c1:+.3f}")
except Exception as ex:
    P(f"   skipped: {ex}")

# self-checks
ok1 = abs(RESULTS["base|canonical"]["km"] - 0.3245) < 5e-4 and abs(RESULTS["base|alt"]["km"] - 0.3045) < 5e-4
ok2 = abs(RESULTS["base|canonical"]["z"] - 3.77) < 0.02 and abs(RESULTS["base|alt"]["z"] - 3.55) < 0.02
ok3 = len(RES) == 31 and len(UL) == 9
P("\nCHECKS")
P(f"   [{'PASS' if ok3 else 'FAIL'}] sample is 31 resolved + 9 limits")
P(f"   [{'PASS' if ok1 else 'FAIL'}] independent KM median reproduces the record to 5e-4 dex on both footings")
P(f"   [{'PASS' if ok2 else 'FAIL'}] independent z reproduces the record to 0.02 on both footings")
RESULTS["checks"] = dict(sample=ok3, km=ok1, z=ok2)
open(os.path.join(HERE, "audit_ufd.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RESULTS, open(os.path.join(HERE, "audit_ufd_results.json"), "w"), indent=1, default=float)
sys.exit(0 if (ok1 and ok2 and ok3) else 1)
