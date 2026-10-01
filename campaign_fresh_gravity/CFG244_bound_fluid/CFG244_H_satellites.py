#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG244 Gate H -- HIERARCHY (satellites): (a) "satellites own nothing" (best of three variants) against (b) "satellites keep their bound
core" (the record's LambdaCDM comparator), scored by ONE rule on N = 88 systems (MW ultra-faints 40 = 31 resolved + 9 limits by
Kaplan-Meier, MW classical dSphs 14, M31 LVD 34), in two views (V1 = the record's error model, V2 = equal floors), on both footings.
Frozen criteria: ../CFG244_FROZEN_CRITERIA.md (committed 84e100c47, sha256 944adc80...), written before this script.
Outcome classes (frozen wording):
  H1 binding FAIL: Delta_V1 <= -9 on both footings (satellites own nothing is preferred).
  H3 binding FAIL ("neither"): Delta_V2 >= 9 on both footings but (b) not acceptable on its own (some |z_b| >= 2 in V1 canonical, or chi2_b(V1) > 11.34).
  H2 PASS, the route is a DIFFERENT LAW from B at satellites: Delta_V2 >= 9 on both footings and (b) acceptable.
  H4 PASS, AMBIGUOUS: anything else (incl. mixed footings or kernel disagreement).
Run: python3 CFG244_H_satellites.py ; MUTATE=MH1..MH5 python3 CFG244_H_satellites.py   (ZF_REPO=<repo> if not run inside the repository)
Exit: main 0; MUTATE exits 1 when the control bites (its target cell flips), 0 otherwise.
The repository is read, never written.  kappa = 1/2 FITTED; no dark-matter particle; the mass is required; nothing here is closure.
"""
import os, sys, math, json, time
sys.dont_write_bytecode = True
import numpy as np
import CFG244_common as K

K.use_lane_code()
MUT = os.environ.get("MUTATE", "")
SLUG = "CFG244_H_satellites" + (f"_MUTATE_{MUT}" if MUT else "")
R = K.Report(SLUG)
P = R.P
P(__doc__.split("Run: python3")[0].strip())
P(f"\n  repo: <repo>   mode: {'MUTATE=' + MUT if MUT else 'main'}")

g42 = K.exec_prefix("CFG42_satellites_rule.py", K.BAR + "C1 / C2")
SAMPLES, UL, A0H, UPS_V, G, Msun = g42["SAMPLES"], g42["UL"], g42["A0H"], g42["UPS_V"], g42["G"], g42["Msun"]
FB, halo_mass, CAL_L, CAL_R, CAL_LO = g42["FB"], g42["halo_mass"], g42["LCAL"], g42["RAT"], g42["LO"]
RHO_C = g42["g36"]["RHO_C"]
HL = g42["HL"]
SEED, NB = 244001, 2000
FOOTS = ("canonical", "alt")
FLOORS = (1e8, 3e8, 1e9, 3e9, 1e10)
HH = 0.674
kpc = HL.kpc
POPS = (("P1", "ufd", False), ("P2", "cls", True), ("P3", "m31", True))
LABEL = {"P1": "MW ultra-faints (40)", "P2": "MW classical dSphs (14)", "P3": "M31 LVD (34)", "COL": "M31 Collins+13 (14)"}


# ------------------------------------------------------------------------------------------------ the estimator and the two readings
def nu_P2(y):
    return math.sqrt(1.0 + 1.0 / max(y, 1e-30))


def nu_RAR(y):
    return HL.nu_s(y)


def c_duffy_full(Mh):
    return 5.71 * (np.asarray(Mh, float) / (2e12 / HH)) ** (-0.084)


def c_duffy_relaxed(Mh):
    return 6.71 * (np.asarray(Mh, float) / (2e12 / HH)) ** (-0.091)


def c_dm(Mh):
    return 10 ** (0.905 - 0.101 * (np.log10(np.asarray(Mh, float) * 0.674) - 12.0))


CONC = {"duffy_full": c_duffy_full, "duffy_relaxed": c_duffy_relaxed, "dutton_maccio": c_dm}


def m_nfw(t):
    return np.log1p(t) - t / (1 + t)


def nfw_enc(Mh, r_kpc, cfn):
    c = cfn(Mh); R200 = (3 * Mh / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.) * 1000.0
    x = min(max(r_kpc / R200, 1e-4), 5.0)
    return Mh * float(m_nfw(c * x) / m_nfw(c))


def infall_gas_u(d, ups):
    lm = math.log10(ups * d["LV"])
    if lm < CAL_LO:
        return 0.0
    nn = np.argsort(np.abs(CAL_L - lm))[:5]
    return float(CAL_R[nn].mean()) * ups * d["LV"]


def sigma_pred(d, reading, foot, kernel="P2", ups=None, gas=False, hmf=1.0, floor_mh=None, conc="duffy_full",
               halo_ups=False, host_off=False, record_efe=False):
    """predicted sigma (km/s) with the record's single-radius estimator: sigma^2 = g r / 3 at r = (4/3) r_half, half the baryons enclosed."""
    ups = UPS_V if ups is None else ups
    Ms = ups * d["LV"]
    Mb = Ms + (max(1.33 * d["MHI"], infall_gas_u(d, ups) if halo_ups else g42["infall_gas"](d)) if gas else 1.33 * d["MHI"])
    rh_pc = (4.0 / 3.0) * d["rh"]; rh = rh_pc * 3.0857e16
    gN = G * 0.5 * Mb * Msun / rh ** 2
    a0 = A0H[foot]
    nu = nu_P2 if kernel == "P2" else nu_RAR
    if reading == "a0":
        g = gN
    elif reading == "a1":
        g = gN * nu(gN / a0)
    elif reading == "a2":
        gNe = 0.0
        if (not host_off) and d.get("D") and d.get("host_mb"):
            gNe = G * d["host_mb"] * Msun / (d["D"] * kpc) ** 2
        g = gN * nu(math.sqrt(gN ** 2 + gNe ** 2) / a0)
    elif reading == "a2rec":       # the record's own EFE rule (h43's a_int), labelled, not a frozen variant
        gNe = G * d["host_mb"] * Msun / (d["D"] * kpc) ** 2 if (d.get("D") and d.get("host_mb")) else 0.0
        g = HL_aint(gN, gNe, a0)
    elif reading == "b":
        Mh = float(halo_mass((ups if halo_ups else UPS_V) * d["LV"])) * hmf
        if floor_mh is not None and UPS_V * d["LV"] < 1e5:
            Mh = floor_mh * hmf
        g = G * (0.5 * Mb + (1 - FB) * nfw_enc(Mh, rh_pc / 1000.0, CONC[conc])) * Msun / rh ** 2
    else:
        raise ValueError(reading)
    return math.sqrt(g * rh / 3.0) / 1e3


def HL_aint(gNi, gNe, a0):
    nt = HL.nu_s((gNi + gNe) / a0); ne = HL.nu_s(gNe / a0) if gNe > 0 else 0.0
    return gNi * nt + gNe * (nt - ne)


def km_median(x, xu):
    y = np.concatenate([-x, -xu]); ev = np.concatenate([np.ones(len(x), bool), np.zeros(len(xu), bool)])
    o = np.lexsort((~ev, y)); y, ev = y[o], ev[o]
    S, n, i = 1.0, len(y), 0
    while i < len(y):
        t = y[i]; j = i; d_ = 0; c_ = 0
        while j < len(y) and y[j] == t:
            d_ += int(ev[j]); c_ += int(not ev[j]); j += 1
        if d_:
            S *= 1.0 - d_ / n
            if S <= 0.5:
                return -t
        n -= d_ + c_; i = j
    return -y[-1]


def boot_km(x, xu, nb, seed):
    rng = np.random.default_rng(seed); v = []
    for _ in range(nb):
        v.append(km_median(x[rng.integers(0, len(x), len(x))], xu[rng.integers(0, len(xu), len(xu))]))
    return float(np.std(v))


def boot_med(x, nb, seed):
    rng = np.random.default_rng(seed)
    return float(np.std([np.median(x[rng.integers(0, len(x), len(x))]) for _ in range(nb)]))


OBS_SCALE = 0.5 if MUT == "MH2" else 1.0
HMF_MUT = 0.01 if MUT == "MH5" else 1.0


def data(pk, obs_scale=1.0):
    smp = SAMPLES[pk]
    return smp, UL if pk == "ufd" else []


def offsets(pk, gas, sigfn, obs_scale):
    smp, ul = data(pk)
    x = np.array([math.log10(obs_scale * d["sig"] / sigfn(d, gas)) for d in smp])
    xu = np.array([math.log10(obs_scale * d["sig_ul"] / sigfn(d, gas)) for d in ul]) if ul else np.array([])
    return x, xu


def stat_central(pk, gas, sigfn, obs_scale):
    x, xu = offsets(pk, gas, sigfn, obs_scale)
    return (km_median(x, xu) if pk == "ufd" else float(np.median(x))), x, xu


def pop_stat(pk, gas, reading, foot, *, kernel="P2", view="V2", recipe="C42", hmf=1.0, conc="duffy_full", nb=NB, seed=SEED,
             obs_scale=1.0, host_off=False, only_p1_floor=False):
    """offset (dex), total error and z of one population under one reading; the record's error recipe (CFG42/CFG69):
    e^2 = e_stat^2 + f_ups^2 + f_mh^2.  V1: the collapse-mass floor for (b); V2: Upsilon floor only.  recipe C91: bootstrap SE for every
    population and Upsilon propagated into the halo mass and infall gas (CFG91's frozen recipe)."""
    hu = (recipe == "C91")
    mk = lambda ups=None, fm=None: (lambda d, g_: sigma_pred(d, reading, foot, kernel, ups=ups, gas=g_, hmf=hmf, floor_mh=fm, conc=conc,
                                                              halo_ups=hu, host_off=host_off))
    m, x, xu = stat_central(pk, gas, mk(), obs_scale)
    if pk == "ufd":
        err = boot_km(x, xu, nb, seed)
    elif recipe == "C91":
        err = boot_med(x, nb, seed)
    else:
        err = 1.2533 * float(np.std(x)) / math.sqrt(len(x))
    uv = [stat_central(pk, gas, mk(ups=u), obs_scale)[0] for u in (1.0, 4.0)]
    f_ups = 0.5 * abs(uv[1] - uv[0])
    f_mh = 0.0; flo = [m]
    if reading == "b" and view == "V1" and (not only_p1_floor or pk == "ufd"):
        flo = [stat_central(pk, gas, mk(fm=fm), obs_scale)[0] for fm in FLOORS]
        f_mh = 0.5 * (max(flo) - min(flo))
    tot = math.sqrt(err ** 2 + f_ups ** 2 + f_mh ** 2)
    return dict(off=float(m), err=float(err), f_ups=float(f_ups), f_mh=float(f_mh), tot=float(tot), z=float(m / tot), chi2=float((m / tot) ** 2),
                n=len(x) + len(xu))


# ------------------------------------------------------------------------------------------------ the full scoring
def score(kernel="P2", recipe="C42", hmf=1.0, conc="duffy_full", obs_scale=1.0, nb=NB, host_off=False, seed=SEED, only_p1_floor=False,
          swap=False, a_variants=("a0", "a1", "a2")):
    out = {"a": {}, "b": {}}
    for foot in FOOTS:
        out["a"][foot] = {}
        for var in a_variants:
            out["a"][foot][var] = {pn: pop_stat(pk, gas, var, foot, kernel=kernel, view="V2", recipe=recipe, obs_scale=obs_scale, nb=nb, seed=seed,
                                                host_off=host_off) for pn, pk, gas in POPS}
        out["b"][foot] = {}
        for view in ("V1", "V2"):
            out["b"][foot][view] = {pn: pop_stat(pk, gas, "b", foot, kernel=kernel, view=view, recipe=recipe, hmf=hmf, conc=conc, obs_scale=obs_scale,
                                                 nb=nb, seed=seed, only_p1_floor=only_p1_floor) for pn, pk, gas in POPS}
    res = {}
    for foot in FOOTS:
        chi_a = {v: sum(out["a"][foot][v][pn]["chi2"] for pn, _, _ in POPS) for v in a_variants}
        best = min(chi_a, key=chi_a.get)
        for view in ("V1", "V2"):
            cb = sum(out["b"][foot][view][pn]["chi2"] for pn, _, _ in POPS)
            ca = chi_a[best]
            d = ca - cb
            res[(foot, view)] = dict(chi2_a=ca, a_best=best, chi2_a_by_variant=chi_a, chi2_b=cb, delta=(-d if swap else d))
    return out, res


def classify(res, out):
    d = lambda f, v: res[(f, v)]["delta"]
    cb1 = res[("canonical", "V1")]["chi2_b"]
    zb = {pn: out["b"]["canonical"]["V1"][pn]["z"] for pn, _, _ in POPS}
    b_ok = all(abs(z) < 2 for z in zb.values()) and cb1 <= 11.34
    if all(d(f, "V1") <= -9 for f in FOOTS):
        return "H1", b_ok, zb
    if all(d(f, "V2") >= 9 for f in FOOTS):
        return ("H2" if b_ok else "H3"), b_ok, zb
    return "H4", b_ok, zb


def run_all(**kw):
    out, res = score(**kw)
    cls, b_ok, zb = classify(res, out)
    return out, res, cls, b_ok, zb


def print_table(out, res, cls, b_ok, zb, tag=""):
    P(f"\n  GATE H TABLE {tag}: per population offset (dex) / error / z / chi2  (a) variants (V-independent) and (b) in V1 and V2")
    for foot in FOOTS:
        P(f"\n  --- footing {foot} (a0 = {A0H[foot]:.4g} m/s^2) ---")
        P(f"  {'population':26s} {'reading':12s} {'offset':>8s} {'error':>7s} {'z':>7s} {'chi2':>7s}   (error parts: stat / Upsilon / collapse-mass floor)")
        for pn, pk, gas in POPS:
            for v in ("a0", "a1", "a2"):
                s = out["a"][foot][v][pn]
                P(f"  {LABEL[pn]:26s} {'(a) ' + v:12s} {s['off']:+8.3f} {s['tot']:7.3f} {s['z']:+7.2f} {s['chi2']:7.2f}   {s['err']:.3f} / {s['f_ups']:.3f} / 0")
            for view in ("V1", "V2"):
                s = out["b"][foot][view][pn]
                P(f"  {LABEL[pn]:26s} {'(b) ' + view:12s} {s['off']:+8.3f} {s['tot']:7.3f} {s['z']:+7.2f} {s['chi2']:7.2f}   {s['err']:.3f} / {s['f_ups']:.3f} / {s['f_mh']:.3f}")
        P(f"  chi2 totals over the three populations: (a0) {res[(foot, 'V1')]['chi2_a_by_variant']['a0']:.2f}, (a1) {res[(foot, 'V1')]['chi2_a_by_variant']['a1']:.2f}, "
          f"(a2) {res[(foot, 'V1')]['chi2_a_by_variant']['a2']:.2f}  -> (a) = best = {res[(foot, 'V1')]['a_best']}  chi2_a = {res[(foot, 'V1')]['chi2_a']:.2f}")
        for view in ("V1", "V2"):
            r = res[(foot, view)]
            P(f"  {view}: chi2_b = {r['chi2_b']:.2f}   Delta chi2 = chi2_a - chi2_b = {r['delta']:+.2f}")
    P(f"\n  (b) acceptable (all |z_b| < 2 in V1 canonical and chi2_b(V1) <= 11.34): {b_ok}; z_b: " + ", ".join(f"{k} {v:+.2f}" for k, v in zb.items()))
    P(f"  OUTCOME CLASS: {cls}")


# ================================================================================================ the planted-sample machinery (MH4)
def planted(truth, n_mock=200, seed=244002, nb=200):
    """mock data sets from the real systems' L_V, r_half, host distances, with sigma_obs drawn around the TRUTH reading's prediction; the full
    pipeline (V1/V2, both footings, best-of-three) is run on each.  Per-system scatter = the real offsets' scatter about their median under
    the truth reading; the 9 limits keep their real distance above the resolved median.  Bootstrap reduced to nb resamples (disclosed)."""
    rng = np.random.default_rng(seed)
    lab = {"b": "b", "a1": "a1"}[truth]
    cache = {}
    for foot in FOOTS:
        for pn, pk, gas in POPS:
            sm, ul = data(pk)
            for var in ("a0", "a1", "a2", "b"):
                for tag, kw in (("c", {}), ("u1", {"ups": 1.0}), ("u4", {"ups": 4.0})):
                    cache[(foot, pn, var, tag)] = (np.array([math.log10(sigma_pred(d, var, foot, "P2", gas=gas, **kw)) for d in sm]),
                                                   np.array([math.log10(sigma_pred(d, var, foot, "P2", gas=gas, **kw)) for d in ul]) if ul else np.array([]))
            for fm in FLOORS:
                cache[(foot, pn, "b", fm)] = (np.array([math.log10(sigma_pred(d, "b", foot, "P2", gas=gas, floor_mh=fm)) for d in sm]),
                                              np.array([math.log10(sigma_pred(d, "b", foot, "P2", gas=gas, floor_mh=fm)) for d in ul]) if ul else np.array([]))
    real = {}
    for pn, pk, gas in POPS:
        sm, ul = data(pk)
        real[pn] = (np.array([math.log10(d["sig"]) for d in sm]), np.array([math.log10(d["sig_ul"]) for d in ul]) if ul else np.array([]))
    cnt = {"H1": 0, "H2": 0, "H3": 0, "H4": 0}; deltas = []
    for im in range(n_mock):
        # the truth is evaluated on the canonical footing for (a1) (the footing only moves a0)
        mock = {}
        for pn, pk, gas in POPS:
            lp, lpu = cache[("canonical", pn, lab, "c")]
            xr = real[pn][0] - lp; s_p = float(np.std(xr, ddof=1)); mr = float(np.median(xr))
            lo = lp + rng.normal(0.0, s_p, len(lp))
            if len(lpu):
                xu_real = real[pn][1] - lpu
                lou = lpu + xu_real - mr
            else:
                lou = np.array([])
            mock[pn] = (lo, lou)
        pe = {}
        for foot in FOOTS:
            for pn, pk, gas in POPS:
                lo, lou = mock[pn]
                def st(var, tag):
                    lp, lpu = cache[(foot, pn, var, tag)]
                    x = lo - lp; xu = (lou - lpu) if len(lou) else np.array([])
                    return (km_median(x, xu) if pk == "ufd" else float(np.median(x))), x, xu
                for var in ("a0", "a1", "a2", "b"):
                    m, x, xu = st(var, "c")
                    err = boot_km(x, xu, nb, im + 1) if pk == "ufd" else 1.2533 * float(np.std(x)) / math.sqrt(len(x))
                    fu = 0.5 * abs(st(var, "u4")[0] - st(var, "u1")[0])
                    fm1 = 0.0
                    if var == "b":
                        fl = [st("b", fm)[0] for fm in FLOORS]; fm1 = 0.5 * (max(fl) - min(fl))
                    pe[(foot, pn, var)] = dict(m=m, e2=err ** 2 + fu ** 2, f1=fm1)
        res = {}
        for foot in FOOTS:
            ca = {v: sum((pe[(foot, pn, v)]["m"]) ** 2 / pe[(foot, pn, v)]["e2"] for pn, _, _ in POPS) for v in ("a0", "a1", "a2")}
            ca = min(ca.values())
            for view in ("V1", "V2"):
                cb = sum(pe[(foot, pn, "b")]["m"] ** 2 / (pe[(foot, pn, "b")]["e2"] + (pe[(foot, pn, "b")]["f1"] ** 2 if view == "V1" else 0.0)) for pn, _, _ in POPS)
                res[(foot, view)] = ca - cb
        zb = [pe[("canonical", pn, "b")]["m"] / math.sqrt(pe[("canonical", pn, "b")]["e2"] + pe[("canonical", pn, "b")]["f1"] ** 2) for pn, _, _ in POPS]
        cb1 = sum(z * z for z in zb); b_ok = all(abs(z) < 2 for z in zb) and cb1 <= 11.34
        if all(res[(f, "V1")] <= -9 for f in FOOTS):
            c = "H1"
        elif all(res[(f, "V2")] >= 9 for f in FOOTS):
            c = "H2" if b_ok else "H3"
        else:
            c = "H4"
        cnt[c] += 1; deltas.append([res[("canonical", "V1")], res[("canonical", "V2")], res[("alt", "V1")], res[("alt", "V2")]])
    dl = np.array(deltas)
    return dict(counts=cnt, n=n_mock, median_delta=dict(zip(("can_V1", "can_V2", "alt_V1", "alt_V2"), np.median(dl, axis=0).tolist())),
                p16=dict(zip(("can_V1", "can_V2", "alt_V1", "alt_V2"), np.percentile(dl, 16, axis=0).tolist())),
                p84=dict(zip(("can_V1", "can_V2", "alt_V1", "alt_V2"), np.percentile(dl, 84, axis=0).tolist())))


# ================================================================================================ main
t0 = time.time()
if MUT in ("", "MH1", "MH2", "MH3", "MH5"):
    # ---------------- controls first
    R.banner("CONTROLS (C-H1..C-H5): the record's committed numbers reproduced with the record's own kernel and recipe")
    ctrl = {}
    for foot in FOOTS:
        for pn, pk, gas in POPS:
            ctrl[("a1", foot, pn)] = pop_stat(pk, gas, "a1", foot, kernel="RAR", view="V2", recipe="C42", nb=1000, seed=42)
            ctrl[("b", foot, pn)] = pop_stat(pk, gas, "b", foot, kernel="RAR", view="V1", recipe="C42", nb=1000, seed=42)
    committed = {("a1", "canonical", "P1"): 0.325, ("a1", "alt", "P1"): 0.304, ("a1", "canonical", "P2"): 0.027, ("a1", "alt", "P2"): 0.008,
                 ("a1", "canonical", "P3"): 0.044, ("a1", "alt", "P3"): 0.031,
                 ("b", "canonical", "P1"): 0.080, ("b", "canonical", "P2"): -0.029, ("b", "canonical", "P3"): -0.062}
    dev = max(abs(ctrl[k]["off"] - v) for k, v in committed.items())
    P("  record (CFG42 / CFG69 READMEs)  vs  reproduced (RAR kernel, nb = 1000, seed 42):")
    for k, v in committed.items():
        P(f"    {k[0]} {k[1]:9s} {k[2]}: committed {v:+.3f}   here {ctrl[k]['off']:+.4f}   z here {ctrl[k]['z']:+.2f}")
    R.check("C-H1 the record's isolated-law and LambdaCDM-comparator offsets reproduced to 0.005 dex", f"max |d| = {dev:.4f} dex", dev <= 0.005)
    zc = {"a1c-P1": ctrl[("a1", "canonical", "P1")]["z"], "a1a-P1": ctrl[("a1", "alt", "P1")]["z"]}
    R.check("C-H1b the record's UFD significance (3.77 / 3.55 sigma) reproduced to 0.1", f"here {zc['a1c-P1']:.2f} / {zc['a1a-P1']:.2f}",
            abs(zc["a1c-P1"] - 3.77) <= 0.1 and abs(zc["a1a-P1"] - 3.55) <= 0.1)
    # C-H2 Newtonian limit: M_coll -> 0 and nu = 1 in closed form
    d0 = SAMPLES["cls"][3]
    sb0 = sigma_pred(d0, "b", "canonical", "P2", gas=True, hmf=1e-30)
    Mb0 = UPS_V * d0["LV"] + max(1.33 * d0["MHI"], g42["infall_gas"](d0)); rh0 = (4 / 3) * d0["rh"] * 3.0857e16
    sn0 = math.sqrt(G * 0.5 * Mb0 * Msun / rh0 ** 2 * rh0 / 3) / 1e3
    R.check("C-H2 Newtonian limit: (b) with M_coll -> 0 and (a0) equal the closed form", f"(b)/(closed) - 1 = {sb0 / sn0 - 1:.1e}; (a0)/(closed) - 1 = "
            f"{sigma_pred(d0, 'a0', 'canonical', 'P2', gas=True) / sn0 - 1:.1e}", abs(sb0 / sn0 - 1) < 1e-9 and abs(sigma_pred(d0, 'a0', 'canonical', 'P2', gas=True) / sn0 - 1) < 1e-9)
    # C-H3 deep-MOND limit: (a1) with a vanishing baryon mass -> sigma^2 = (a0 g_N)^(1/2) r / 3
    dd = dict(d0, LV=1.0, MHI=0.0)
    s_dm = sigma_pred(dd, "a1", "canonical", "P2", ups=1.0, gas=False)
    Mbd = 1.0; rhd = (4 / 3) * dd["rh"] * 3.0857e16; gNd = G * 0.5 * Mbd * Msun / rhd ** 2
    s_dm_c = math.sqrt(math.sqrt(A0H["canonical"] * gNd) * rhd / 3) / 1e3
    R.check("C-H3 deep-MOND limit of (a1) (P2): sigma^2 = sqrt(a0 g_N) r / 3", f"ratio - 1 = {s_dm / s_dm_c - 1:.1e}", abs(s_dm / s_dm_c - 1) < 1e-6)
    # C-H4 EFE limits
    de = SAMPLES["ufd"][5]
    s1 = sigma_pred(de, "a1", "canonical", "P2"); s2off = sigma_pred(de, "a2", "canonical", "P2", host_off=True)
    big = dict(de, host_mb=1e30)
    s2big = sigma_pred(big, "a2", "canonical", "P2")
    gNe_big = G * 1e30 * Msun / (de["D"] * kpc) ** 2
    Mb_ = UPS_V * de["LV"] + 1.33 * de["MHI"]; rh_ = (4 / 3) * de["rh"] * 3.0857e16; gN_ = G * 0.5 * Mb_ * Msun / rh_ ** 2
    s_newt = math.sqrt(gN_ * rh_ / 3) / 1e3
    R.check("C-H4 EFE limits: host -> 0 returns (a1) to 1e-12; host -> infinity returns the Newtonian value (nu -> 1)",
            f"host off: {s2off / s1 - 1:.1e}; huge host: sigma_a2/sigma_Newton - 1 = {s2big / s_newt - 1:.1e}", abs(s2off / s1 - 1) < 1e-12 and abs(s2big / s_newt - 1) < 1e-6)
    # C-H5 the labelled swap changes the sign of Delta (checked below on the primary scoring)
    # ---------------- primary scoring
    R.banner("PRIMARY SCORING  (kernel P2; recipe: the record's committed (CFG42); bootstrap 2000 resamples, seed 244001)")
    kw = dict(kernel="P2", recipe="C42", obs_scale=OBS_SCALE, hmf=HMF_MUT, host_off=(MUT == "MH3"), swap=(MUT == "MH1"))
    out, res, cls, b_ok, zb = run_all(**kw)
    print_table(out, res, cls, b_ok, zb, tag=("(MUTATE " + MUT + ")" if MUT else "(P2 kernel)"))
    R.num("primary", dict(out=out, res={f"{k[0]}|{k[1]}": v for k, v in res.items()}, outcome=cls, b_acceptable=b_ok, z_b=zb))
    if not MUT:
        # kernel cross-check with the record's RAR kernel
        R.banner("KERNEL CROSS-CHECK (the record's exponential RAR kernel) -- if the category differs the lane reports AMBIGUOUS (H4)")
        outr, resr, clsr, b_okr, zbr = run_all(kernel="RAR", recipe="C42")
        print_table(outr, resr, clsr, b_okr, zbr, tag="(RAR kernel)")
        R.num("rar_kernel", dict(out=outr, res={f"{k[0]}|{k[1]}": v for k, v in resr.items()}, outcome=clsr))
        final = cls if clsr == cls else "H4"
        P(f"\n  P2 outcome {cls}; RAR-kernel outcome {clsr}; FINAL OUTCOME CLASS (more cautious on disagreement): {final}")
        # C-H5
        _, res_sw = score(kernel="P2", recipe="C42", swap=True, nb=300)
        _, res_nsw = score(kernel="P2", recipe="C42", swap=False, nb=300)
        R.check("C-H5 swapping the readings' labels changes the sign of every Delta", "; ".join(f"{k[0]}/{k[1]}: {res_nsw[k]['delta']:+.2f} -> {res_sw[k]['delta']:+.2f}" for k in res_nsw),
                all(abs(res_nsw[k]["delta"] + res_sw[k]["delta"]) < 1e-9 for k in res_nsw))
    else:
        final = cls

    # ---------------- cells read by the MUTATE controls
    out0, res0, cls0, b_ok0, zb0 = (out, res, cls, b_ok, zb) if not MUT else run_all(kernel="P2", recipe="C42")
    cell_a2 = {}
    for nm, ho in (("host_on", False), ("host_off", True)):
        pa1 = pop_stat("ufd", False, "a1", "canonical", kernel="P2", host_off=ho, nb=300)["off"]
        pa2 = pop_stat("ufd", False, "a2", "canonical", kernel="P2", host_off=ho, nb=300)["off"]
        cell_a2[nm] = pa2 - pa1
    P(f"\n  (a2) minus (a1) UFD median offset, canonical: host on {cell_a2['host_on']:+.4f} dex, host off {cell_a2['host_off']:+.4f} dex")
    R.num("a2_minus_a1_ufd", cell_a2)

    # ---------------- reported robustness rows (main only)
    if not MUT:
        R.banner("ROBUSTNESS ROWS (reported; none changes the verdict).  Delta chi2 = chi2_a - chi2_b; entries V1/V2 canonical | V1/V2 alt")
        rows = {}

        def row(name, **kw2):
            o, r_, c_, bo, zb_ = run_all(nb=500, **kw2)
            rows[name] = dict(delta={f"{k[0]}|{k[1]}": r_[k]["delta"] for k in r_}, chi2_a=r_[("canonical", "V1")]["chi2_a"], chi2_b_V1=r_[("canonical", "V1")]["chi2_b"],
                              chi2_b_V2=r_[("canonical", "V2")]["chi2_b"], outcome=c_, b_ok=bo, z_b={k: v for k, v in zb_.items()}, a_best=r_[("canonical", "V1")]["a_best"])
            P(f"  {name:58s} Delta {r_[('canonical','V1')]['delta']:+7.2f}/{r_[('canonical','V2')]['delta']:+7.2f} | {r_[('alt','V1')]['delta']:+7.2f}/{r_[('alt','V2')]['delta']:+7.2f}"
              f"   chi2_b(V1) {r_[('canonical','V1')]['chi2_b']:5.2f}  -> {c_}  (b ok {bo})")
        row("baseline (nb = 500)")
        for f_ in (0.1, 0.3, 3.0, 10.0):
            row(f"(b) collapse mass x{f_}", hmf=f_)
        row("(b) Dutton-Maccio concentration", conc="dutton_maccio")
        row("(b) Duffy relaxed concentration", conc="duffy_relaxed")
        row("CFG91 recipe (bootstrap SE + Upsilon propagated into halo and gas)", recipe="C91")
        row("(b) floors on P1 only (frozen letter)", only_p1_floor=True)
        row("record kernel (RAR)", kernel="RAR")
        # clamp scan for (b): every satellite with M_* < 1e5 set to the value
        P("\n  clamp scan of (b) (every satellite with M_* < 1e5 set to the collapse mass), canonical, P1 KM median / V2 z:")
        clamp = {}
        for fm in FLOORS + (None,):
            s_ = pop_stat("ufd", False, "b", "canonical", kernel="P2", view="V2", nb=300)
            m_, _, _ = stat_central("ufd", False, lambda d, g_, fm=fm: sigma_pred(d, "b", "canonical", "P2", gas=g_, floor_mh=fm), 1.0)
            clamp[str(fm)] = float(m_)
            P(f"    M_coll = {fm if fm else 'Moster (clamped 1e9)'}: KM median {m_:+.3f}")
        R.num("clamp_scan", clamp)
        # Upsilon = 1 and 4 central
        for u_ in (1.0, 4.0):
            tot = {}
            for foot in FOOTS:
                for nm, var in (("a1", "a1"), ("b", "b")):
                    for pn, pk, gas in POPS:
                        m_, _, _ = stat_central(pk, gas, lambda d, g_, var=var, u_=u_, foot=foot: sigma_pred(d, var, foot, "P2", ups=u_, gas=g_), 1.0)
                        tot[(foot, nm, pn)] = float(m_)
            P(f"  Upsilon_V = {u_:.0f} central offsets canonical: a1 " + ", ".join(f"{pn} {tot[('canonical','a1',pn)]:+.3f}" for pn, _, _ in POPS) +
              " | b " + ", ".join(f"{pn} {tot[('canonical','b',pn)]:+.3f}" for pn, _, _ in POPS))
            rows[f"Upsilon_V = {u_:.0f}"] = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in tot.items()}
        # leave-one-population-out (from the primary scoring)
        P("\n  leave-one-population-out Delta chi2 (primary, V1 | V2, canonical and alt):")
        for drop in ("P1", "P2", "P3"):
            seg = []
            for foot in FOOTS:
                ca = min(sum(out["a"][foot][v][pn]["chi2"] for pn, _, _ in POPS if pn != drop) for v in ("a0", "a1", "a2"))
                for view in ("V1", "V2"):
                    seg.append(ca - sum(out["b"][foot][view][pn]["chi2"] for pn, _, _ in POPS if pn != drop))
            P(f"    without {drop}: can V1 {seg[0]:+.2f} V2 {seg[1]:+.2f} | alt V1 {seg[2]:+.2f} V2 {seg[3]:+.2f}")
            rows[f"without {drop}"] = seg
        # Collins in place of P3
        P("\n  M31 Collins+13 (14; 13 shared with P3) in place of P3 (primary scoring, canonical V1 | V2):")
        colz = {}
        for foot in ("canonical",):
            a_ = {v: pop_stat("col", True, v, foot, kernel="P2")["chi2"] for v in ("a0", "a1", "a2")}
            b1 = pop_stat("col", True, "b", foot, kernel="P2", view="V1")["chi2"]; b2 = pop_stat("col", True, "b", foot, kernel="P2", view="V2")["chi2"]
            sc = {pn: out["a"][foot][v][pn]["chi2"] for pn in ("P1", "P2") for v in ("a1",)}
            ca = min(sum(out["a"][foot][v][pn]["chi2"] for pn in ("P1", "P2")) + a_[v] for v in ("a0", "a1", "a2"))
            cb1 = sum(out["b"][foot]["V1"][pn]["chi2"] for pn in ("P1", "P2")) + b1; cb2 = sum(out["b"][foot]["V2"][pn]["chi2"] for pn in ("P1", "P2")) + b2
            P(f"    Collins alone: offsets a1 {pop_stat('col', True, 'a1', foot, kernel='P2')['off']:+.3f}, b {pop_stat('col', True, 'b', foot, kernel='P2', view='V1')['off']:+.3f};"
              f" Delta (P1+P2+Collins) V1 {ca - cb1:+.2f}, V2 {ca - cb2:+.2f}")
            colz = dict(V1=ca - cb1, V2=ca - cb2)
        rows["collins_in_place_of_P3"] = colz
        # luminosity trend of the UFD offsets (resolved-only Spearman vs M_V)
        from scipy.stats import spearmanr
        P("\n  UFD offset against M_V (resolved only, Spearman rho, p) under each reading (CFG83 flagged only; model-independent ordering):")
        for var in ("a1", "a2", "b"):
            x_, _ = offsets("ufd", False, lambda d, g_, var=var: sigma_pred(d, var, "canonical", "P2", gas=g_), 1.0)
            rho, p_ = spearmanr([d["MV"] for d in SAMPLES["ufd"]], x_)
            P(f"    {var}: rho = {rho:+.2f}  p = {p_:.3f}  (n = {len(x_)})")
            rows[f"MV_trend_{var}"] = (float(rho), float(p_))
        # the record's own EFE rule (h43 a_int), labelled
        P("\n  the record's own EFE rule (h43's a_int; RAR kernel; labelled, not a frozen variant), canonical medians:")
        for pn, pk, gas in POPS:
            m_, _, _ = stat_central(pk, gas, lambda d, g_: sigma_pred(d, "a2rec", "canonical", "RAR", gas=g_), 1.0)
            m1_, _, _ = stat_central(pk, gas, lambda d, g_: sigma_pred(d, "a1", "canonical", "RAR", gas=g_), 1.0)
            P(f"    {LABEL[pn]:26s} a2rec {m_:+.3f}   a1 (RAR) {m1_:+.3f}")
            rows[f"a2rec_{pn}"] = (float(m_), float(m1_))
        # the sum rule S (hybrid), reported medians only
        P("\n  the record's sum rule S (law + collapse debris; hybrid, not a reading of this class; CFG42's sigma_rule with its collapse-mass convention), canonical medians:")
        for pn, pk, gas in POPS:
            xs = np.array([math.log10(d["sig"] / g42["sigma_rule"](d, "canonical", rule=True, gas=gas)[0]) for d in SAMPLES[pk]])
            xu = np.array([math.log10(d["sig_ul"] / g42["sigma_rule"](d, "canonical", rule=True, gas=gas)[0]) for d in UL]) if pk == "ufd" else np.array([])
            m_ = km_median(xs, xu) if pk == "ufd" else float(np.median(xs))
            P(f"    {LABEL[pn]:26s} S median {m_:+.3f}")
            rows[f"S_{pn}"] = float(m_)
        R.num("robustness", rows)

    # ---------------- the MUTATE verdict
    if MUT:
        main_cls = run_all(kernel="P2", recipe="C42", nb=500)[2]
        if MUT == "MH1":
            bite = (cls != main_cls) and all(res[k]["delta"] * 1.0 for k in res)
            tgt = f"verdict {main_cls} -> {cls}"
        elif MUT == "MH2":
            d_main = run_all(kernel="P2", recipe="C42", nb=500)[1]
            bite = (cls != main_cls) or any(np.sign(res[k]["delta"]) != np.sign(d_main[k]["delta"]) for k in res)
            tgt = f"verdict {main_cls} -> {cls}; Delta (can V1) {d_main[('canonical','V1')]['delta']:+.2f} -> {res[('canonical','V1')]['delta']:+.2f}"
        elif MUT == "MH3":
            bite = cell_a2["host_on"] >= 0.01 and cell_a2["host_off"] < 0.01
            tgt = f"cell (a2 - a1) UFD >= 0.01 dex: host on {cell_a2['host_on']:+.4f} / host off {cell_a2['host_off']:+.4f}; verdict {main_cls} -> {cls} (expected unchanged)"
        elif MUT == "MH5":
            zb_main = run_all(kernel="P2", recipe="C42", nb=500)[4]
            bite = abs(zb_main["P1"]) < 2 and abs(zb["P1"]) >= 2
            tgt = f"(b) P1 |z|: {abs(zb_main['P1']):.2f} -> {abs(zb['P1']):.2f} (line 2); verdict {main_cls} -> {cls}"
        P(f"\n  MUTATE {MUT}: target cell: {tgt}\n  BITES: {bite}")
        R.num("mutate", dict(id=MUT, bites=bool(bite), target=tgt))
        R.write()
        sys.exit(1 if bite else 0)
    # ---------------- main: write and exit 0
    R.num("final_outcome", final)
    P(f"\n  GATE H RESULT: outcome class {final}   ({time.time() - t0:.0f} s)")
    R.write()
    sys.exit(0)

elif MUT == "MH4":
    R.banner("MH4  planted fake satellite samples with known cores (200 mocks per truth; the full Gate H pipeline on each)")
    pb = planted("b"); pa = planted("a1")
    for nm, p_ in (("truth (b)", pb), ("truth (a1)", pa)):
        P(f"  {nm}: outcome counts {p_['counts']} of {p_['n']}; median Delta (can V1, can V2, alt V1, alt V2) = " + ", ".join(f"{v:+.1f}" for v in p_["median_delta"].values()))
    pw_b = pb["counts"]["H2"] / pb["n"]; pw_a = pa["counts"]["H1"] / pa["n"]
    P(f"\n  power: P(H2 | truth b) = {pw_b:.2f}; P(H1 | truth a1) = {pw_a:.3f}; P(H4 | truth a1) = {pa['counts']['H4'] / pa['n']:.2f}; P(H4 | truth b) = {pb['counts']['H4'] / pb['n']:.2f}")
    top_b = max(pb["counts"], key=pb["counts"].get); top_a = max(pa["counts"], key=pa["counts"].get)
    bite = top_b != top_a
    P(f"  modal outcome: truth b -> {top_b}; truth a1 -> {top_a}.  BITES (the verdict category differs between the plants): {bite}")
    R.num("mh4", dict(truth_b=pb, truth_a1=pa, power_H2_given_b=pw_b, power_H1_given_a1=pw_a, bites=bool(bite)))
    R.write()
    sys.exit(1 if bite else 0)
else:
    raise SystemExit(f"unknown MUTATE id {MUT}")
