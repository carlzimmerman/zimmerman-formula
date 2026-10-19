"""CFG799 -- HIFI band-1a total-power search for a fixed spacecraft-frame mirror line at 541.664 / 541.700 GHz.
Criteria: FROZEN_CRITERIA.md (+ addendum A).  Inputs: red_<obsid>.npz written by cfg799_fetch.py (data dir, not in repo).
Run:  python3 -I cfg799.py <data_dir>        (CFG799_MUTATE=1: inject a line of 10 sigma_a at nu_t, separate outputs)
kappa = 1/2 FITTED; not theory closed.  External numbers (sideband gain, load coupling, WBS response, S) provisional.
The framework predicts NO line.
"""
import glob, json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(sys.argv[1])
MUT = os.environ.get("CFG799_MUTATE") == "1"
SFX = "_MUTATE" if MUT else ""
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


NU_T, NU_2 = 541.664, 541.700          # GHz
H2O = 556.936
FWHM = np.hypot(0.3, 1.1)              # MHz
SIG_G = FWHM / 2.3548
HALF = 50.0                            # MHz fit half-window
EDGE = 100.0                           # MHz common window (M2)
OFFS = [-20, -10, -5, 5, 10, 20]
kB, c, MSUN, PC = 1.380649e-23, 2.99792458e8, 1.989e30, 3.0857e16
RHO, AREA = 0.01 * MSUN / PC ** 3, 9.6
S_LIST = (10.0, 50.0, 1000.0)


def legendre_design(x, ncoef=4):
    return np.polynomial.legendre.legvander(x, ncoef - 1)


def gauss(d):
    return np.exp(-0.5 * (d / SIG_G) ** 2)


# ---------------------------------------------------------------- load reduced data
def load():
    man = json.load(open(os.path.join(DATA, "cfg799_manifest.json")))
    obs = {}
    for f in sorted(glob.glob(os.path.join(DATA, "red_*.npz"))):
        oid = os.path.basename(f)[4:-4]
        z = np.load(f)
        meta = json.loads(str(z["meta"]))
        ds = []
        for pol in ("h", "v"):
            for i in range(meta["pol"][pol]["n"]):
                g = lambda k: z[f"{pol}{i}_{k}"]
                sc = g("scal")
                ds.append(dict(pol=pol, ds=int(sc[0]), lo=float(sc[1]), nsky=sc[2], non=sc[3], nref=sc[4], JH=sc[5],
                               JC=sc[6], tS=sc[7], corr=sc[8], Nall=g("Nall").astype(float), Nref=g("Nref").astype(float),
                               H=g("H").astype(float), C=g("C").astype(float), L1=g("L1").astype(float),
                               IF=g("IF").astype(float), flag=g("L1flag")))
        obs[oid] = dict(ds=ds, man=man.get(oid, {}))
    return man, obs


def _mad(x):
    return 1.4826 * np.median(np.abs(x - np.median(x)))


def anchor_ds(d):
    """Robust L1 anchor (deviation D1, README): the frozen std-based RMA ratio is wrecked by isolated Level-1 spike
    channels (e.g. Mars, std ~1e3 K in two sub-bands).  Per sub-band: drop L1-flagged channels and channels > 10 MAD
    from the median in either spectrum, 16-channel boxcar, ratio MAD(D)/MAD(L1) signed by the correlation; median over
    the four sub-bands."""
    Non = (d["nsky"] * d["Nall"] - d["nref"] * d["Nref"]) / d["non"]
    D = (Non - d["Nref"]) * (d["JH"] - d["JC"]) / (d["H"] - d["C"])
    k = np.ones(16) / 16
    ts, cs = [], []
    for sb in range(4):
        l, x = d["L1"][sb], D[sb]
        ok = (d["flag"][sb] == 0) & np.isfinite(l) & np.isfinite(x)
        if ok.sum() < 200:
            continue
        ok &= np.abs(l - np.median(l[ok])) < 10 * _mad(l[ok])
        ok &= np.abs(x - np.median(x[ok])) < 10 * _mad(x[ok])
        ls, xs = np.convolve(l[ok], k, "valid"), np.convolve(x[ok], k, "valid")
        cc = np.corrcoef(xs, ls)[0, 1]
        if not np.isfinite(cc) or _mad(ls) == 0:
            continue
        ts.append(np.sign(cc) * _mad(xs) / _mad(ls)); cs.append(cc)
    return (float(np.median(ts)), float(np.median(cs))) if ts else (np.nan, np.nan)


def anchor(o):
    """Deviation D2 (README): FastDBS nod-B datasets anchor badly (ON/REF labelling from Level-1 kept rows does not
    reproduce Level-1 there, corr ~0.55, sign-flipped continuum), so t_S is the median over WELL-ANCHORED datasets
    (corr >= 0.9).  Pass: >= 30% of datasets well anchored and their relative MAD scatter <= 10%.  t_S is a timing
    constant of the observation, applied to all datasets; REF-only spectra use well-anchored datasets only."""
    tc = [anchor_ds(d) for d in o["ds"]]
    for d, (t, cc) in zip(o["ds"], tc):
        d["anc_good"] = bool(np.isfinite(cc) and cc >= 0.9 and t > 0)
    good = np.array([t for (t, cc), d in zip(tc, o["ds"]) if d["anc_good"]])
    cr = np.array([cc for _, cc in tc if np.isfinite(cc)])
    if len(good) == 0:
        return dict(tS=np.nan, rmad=np.inf, corr=float(np.median(cr)) if len(cr) else np.nan, ok=False, n=len(tc), n_good=0)
    med = float(np.median(good))
    rmad = float(np.median(np.abs(good - med)) / med)
    frac = len(good) / len(tc)
    ok = rmad <= 0.10 and frac >= 0.3
    return dict(tS=med, rmad=rmad, corr=float(np.median(cr)), ok=bool(ok), n=len(tc), n_good=len(good), frac_good=frac)


def build_spectra(oid, o, tS):
    groups = {}
    for d in o["ds"]:
        G = (d["JH"] - d["JC"]) / (d["H"] - d["C"])
        Tall = (d["Nall"] / tS - d["C"]) * G + d["JC"]
        Tref = (d["Nref"] / tS - d["C"]) * G + d["JC"]
        key = (d["pol"], int(round(d["lo"] * 1000)))
        g = groups.setdefault(key, dict(w=0., wr=0., wo=0., Tall=0., Tref=0., L1=0., flag=0, IF=d["IF"], lo=d["lo"], pol=d["pol"]))
        g["Tall"] = g["Tall"] + d["nsky"] * Tall; g["w"] += d["nsky"]
        if d.get("anc_good"):
            g["Tref"] = g["Tref"] + d["nref"] * Tref; g["wr"] += d["nref"]
        g["L1"] = g["L1"] + d["non"] * d["L1"]; g["wo"] += d["non"]
        g["flag"] = g["flag"] | d["flag"]
    spec = []
    for key, g in groups.items():
        spec.append(dict(obs=oid, pol=g["pol"], lo=g["lo"], IF=g["IF"], flag=g["flag"], Tall=g["Tall"] / g["w"],
                         Tref=(g["Tref"] / g["wr"]) if g["wr"] > 0 else np.full_like(g["Tall"], np.nan),
                         L1=g["L1"] / g["wo"], nsky=g["w"]))
    return spec


def choose_sb(IF, ifc, half):
    best, bm = None, -1
    for sb in range(4):
        ax = IF[sb][10:-10]
        lo_, hi_ = min(ax[0], ax[-1]), max(ax[0], ax[-1])
        m = min(ifc - half - lo_, hi_ - (ifc + half))
        if m >= 0 and m > bm:
            best, bm = sb, m
    return best


def if_of(s, nu):
    return (nu - s["lo"]) * 1000.0 if nu > s["lo"] else (s["lo"] - nu) * 1000.0


def prep(spectra):
    keep, drop = [], {"M1": 0, "M2": 0, "IF": 0}
    for s in spectra:
        ifc = if_of(s, NU_T)
        if not 3900 <= ifc <= 8100:
            drop["IF"] += 1; continue
        if abs(2 * s["lo"] - NU_T - H2O) < 0.6:
            drop["M1"] += 1; continue
        sb = choose_sb(s["IF"], ifc, EDGE)
        if sb is None:
            drop["M2"] += 1; continue
        s["sb"] = sb; s["ifc"] = ifc; s["usb"] = NU_T > s["lo"]
        keep.append(s)
    return keep, drop


def fit_one(IFax, y, flag, centre, inject=0.0, with_line=True):
    sel = np.abs(IFax - centre) <= HALF
    if sel.sum() < 100:
        return None
    x, yy, fl = IFax[sel], y[sel].copy(), flag[sel]
    if np.any(fl[np.abs(x - centre) <= 3.0] != 0) or np.mean(fl != 0) > 0.2:
        return None
    g = gauss(x - centre)
    yy = yy + inject * g
    w = (fl == 0) & np.isfinite(yy)
    if w.sum() < 100:
        return None
    A = legendre_design((x - centre) / HALF)
    if with_line:
        A = np.column_stack([A, g])
    Aw, yw = A[w], yy[w]
    coef, *_ = np.linalg.lstsq(Aw, yw, rcond=None)
    res = yw - Aw @ coef
    dof = max(len(yw) - A.shape[1], 1)
    s2 = float(res @ res / dof)
    cov = np.linalg.inv(Aw.T @ Aw) * s2
    if with_line:
        return float(coef[-1]), float(np.sqrt(cov[-1, -1])), x, yy - A[:, :-1] @ coef[:-1]
    return x, yy - A @ coef


def l1_masked(s, centre):
    IFax = s["IF"][s["sb"]]; y = s["L1"][s["sb"]]
    sel = np.abs(IFax - centre) <= HALF
    x, yy = IFax[sel], y[sel]
    if len(x) < 100:
        return True
    A = legendre_design((x - centre) / HALF)
    coef, *_ = np.linalg.lstsq(A, yy, rcond=None)
    r = np.convolve(yy - A @ coef, np.ones(3) / 3, "same")
    rms = 1.4826 * np.median(np.abs(r - np.median(r)))
    near = np.abs(x - centre) <= 10.0
    return bool(np.max(np.abs(r[near])) > 5 * rms) if rms > 0 else True


def amps(sp, nu, key="Tall", inject=0.0, use_mask=True):
    out = []
    for s in sp:
        centre = if_of(s, nu)
        if not ((nu > s["lo"]) == s["usb"]):
            continue
        if use_mask and l1_masked(s, centre):
            continue
        r = fit_one(s["IF"][s["sb"]], s[key][s["sb"]], s["flag"][s["sb"]], centre, inject=inject)
        if r is None or not np.isfinite(r[1]) or r[1] <= 0:
            continue
        out.append((r[0], r[1], s))
    return out


def stack(a, inflate=True):
    if len(a) == 0:
        return dict(a=np.nan, sig=np.nan, z=np.nan, chi2nu=np.nan, n=0)
    v = np.array([x[0] for x in a]); e = np.array([x[1] for x in a])
    w = 1 / e ** 2
    m = float(np.sum(w * v) / np.sum(w)); sg = float(np.sum(w) ** -0.5)
    chi2nu = float(np.sum(w * (v - m) ** 2) / max(len(v) - 1, 1))
    if inflate:
        sg *= max(1.0, np.sqrt(chi2nu))
    return dict(a=m, sig=sg, z=m / sg, chi2nu=chi2nu, n=len(v))


def eps_of(a_peak, S):
    if not np.isfinite(a_peak) or a_peak <= 0:
        return 0.0
    W_ssb = 2 * 1.0645 * a_peak * FWHM * 1e6
    return float(np.sqrt(2 * S * kB * W_ssb / ((2 / 3) * RHO * c ** 3 * AREA)))


def a_of_eps(eps, S):
    W_ssb = eps ** 2 * (2 / 3) * RHO * c ** 3 * AREA / (2 * S * kB)
    return W_ssb / (2 * 1.0645 * FWHM * 1e6)


def chi2_sf(x, k):
    from scipy.stats import chi2
    return float(chi2.sf(x, k))


def main():
    man, obs = load()
    P(f"CFG799  HIFI band-1a total-power mirror-line search" + ("  [MUTATE: injected line at nu_t]" if MUT else ""))
    P(f"  nu_t = {NU_T} GHz (primary), nu_2 = {NU_2} GHz; profile FWHM {FWHM:.2f} MHz; fit +-{HALF:.0f} MHz deg-3 Legendre")
    R = {"lane": "CFG799", "mutate": MUT, "nu_t": NU_T, "nu_2": NU_2}
    # anchor
    spectra, anc, hours = [], {}, 0.0
    for oid, o in obs.items():
        a = anchor(o); anc[oid] = a
        if a["ok"]:
            spectra += build_spectra(oid, o, a["tS"])
    n_ok = sum(a["ok"] for a in anc.values())
    P(f"  observations reduced: {len(obs)}; L1-anchor pass: {n_ok}; fail: {[k for k, a in anc.items() if not a['ok']]}")
    R["anchor"] = anc
    sp, drops = prep(spectra)
    used_obs = sorted({s["obs"] for s in sp})
    hours = sum(obs[o]["man"].get("t_int_h", 0) for o in used_obs)
    P(f"  spectra (obs x pol x LO): {len(spectra)}; after M1/M2: {len(sp)} (dropped {drops}); obs used {len(used_obs)}; "
      f"CFG798 t_int of used obs {hours:.2f} h")
    R.update(n_spectra=len(sp), drops=drops, used_obs=used_obs, t_int_h_used=hours)

    if MUT:
        main_res = json.load(open(os.path.join(HERE, "cfg799_results.json")))
        A_mut = 10 * main_res["main"]["nu_t"]["sig"]
        for s in sp:
            for key in ("Tall", "Tref"):
                for sb in range(4):
                    s[key][sb] = s[key][sb] + A_mut * gauss(s["IF"][sb] - if_of(s, NU_T))
        P(f"  MUTATE: injected peak {A_mut * 1e3:.3f} mK at nu_t into total power (not Level-1)")
        R["A_mut"] = A_mut

    res = {}
    for name, nu in (("nu_t", NU_T), ("nu_2", NU_2)):
        a = amps(sp, nu); st = stack(a)
        ref = stack(amps(sp, nu, key="Tref")); l1 = stack(amps(sp, nu, key="L1"))
        ifs = np.array([x[2]["ifc"] for x in a]); medif = np.median(ifs) if len(ifs) else 0
        lo_h = stack([x for x in a if x[2]["ifc"] <= medif]); hi_h = stack([x for x in a if x[2]["ifc"] > medif])
        d = (lo_h["a"] - hi_h["a"]); dz = d / np.hypot(lo_h["sig"], hi_h["sig"])
        from scipy.stats import norm
        p_split = float(2 * norm.sf(abs(dz))) if np.isfinite(dz) else np.nan
        a95 = max(st["a"], 0) + 1.645 * st["sig"]
        res[name] = dict(st, ref=ref, L1=l1, low_if=lo_h, high_if=hi_h, p_split=p_split, a95=a95,
                         eps95={f"S{S:.0f}": eps_of(a95, S) for S in S_LIST})
        P(f"\n  [{name} = {nu} GHz]  a = {st['a'] * 1e3:+.3f} +- {st['sig'] * 1e3:.3f} mK (DSB peak)  z = {st['z']:+.2f}  "
          f"chi2nu {st['chi2nu']:.2f}  n = {st['n']}")
        P(f"     REF-only z {ref['z']:+.2f} (a {ref['a'] * 1e3:+.3f} mK);  Level-1 z {l1['z']:+.2f};  low-IF z {lo_h['z']:+.2f}, "
          f"high-IF z {hi_h['z']:+.2f}, split p {p_split:.3f}")
        P(f"     a95 = {a95 * 1e3:.3f} mK -> eps95 = " + ", ".join(f"S={S:.0f}: {eps_of(a95, S):.2e}" for S in S_LIST))
    R["main"] = res
    sig_t = res["nu_t"]["sig"]

    # C1 injection
    A_inj = 10 * sig_t
    inj = stack(amps(sp, NU_T, inject=A_inj))
    rec = (inj["a"] - res["nu_t"]["a"]) / A_inj
    C1 = bool(0.8 <= rec <= 1.2)
    P(f"\n  C1 injection: A_inj {A_inj * 1e3:.3f} mK -> recovered {inj['a'] * 1e3:.3f} mK, r = {rec:.3f}, z {inj['z']:.1f}  "
      f"{'PASS' if C1 else 'FAIL'}")
    # informational: injected profile differs from the fit profile (FWHM 1.10 MHz, centre +0.2 MHz) -> tests mismatch
    inj2 = []
    for s in sp:
        s2 = dict(s); s2["Tall"] = s["Tall"].copy()
        for sb in range(4):
            dd = s["IF"][sb] - if_of(s, NU_T + (0.0002 if s["usb"] else -0.0002))
            s2["Tall"][sb] = s["Tall"][sb] + A_inj * np.exp(-0.5 * (dd / (1.10 / 2.3548)) ** 2)
        inj2.append(s2)
    inj2s = stack(amps(inj2, NU_T)); rec2 = (inj2s["a"] - res["nu_t"]["a"]) / A_inj
    P(f"  (info) mismatched-profile injection (FWHM 1.10 MHz, +0.2 MHz): r = {rec2:.3f}  [C1 itself is exact by linearity]")
    R["inj_mismatch_r"] = rec2
    # C2 offsets
    zs = []
    for dlt in OFFS:
        st = stack(amps(sp, NU_T + dlt / 1000.0)); zs.append(st["z"])
    zs = np.array(zs); chi = float(np.nansum(zs ** 2)); pchi = chi2_sf(chi, len(OFFS))
    C2 = bool(np.all(np.abs(zs) < 3) and pchi > 0.001)
    P(f"  C2 null offsets {OFFS} MHz: z = {np.round(zs, 2).tolist()}  sum z^2 {chi:.2f}, p {pchi:.3f}  {'PASS' if C2 else 'FAIL'}")
    # C3 IF shuffle
    rng = np.random.default_rng(799)
    ifc_all = np.array([s["ifc"] for s in sp])
    sh = []
    for i, s in enumerate(sp):
        cand = rng.permutation(np.delete(ifc_all, i))
        chosen = []
        for f in cand:
            if len(chosen) >= 20:
                break
            if any(abs(f - q) < 5 for q in chosen):
                continue
            rfs = (s["lo"] + f / 1000, s["lo"] - f / 1000)
            if min(abs(r - n) for r in rfs for n in (NU_T, NU_2)) * 1000 <= 60:
                continue
            sb = choose_sb(s["IF"], f, HALF + 10)
            if sb is None:
                continue
            ss = dict(s, sb=sb)
            if l1_masked(ss, f):
                continue
            r = fit_one(s["IF"][sb], s["Tall"][sb], s["flag"][sb], f)
            if r is None or not r[1] > 0:
                continue
            chosen.append(f); sh.append((r[0], r[1], s))
    shs = stack(sh)
    C3 = bool(abs(shs["z"]) < 3)
    P(f"  C3 IF-shuffle: n {shs['n']}, a {shs['a'] * 1e3:+.3f} +- {shs['sig'] * 1e3:.3f} mK, z {shs['z']:+.2f}, chi2nu {shs['chi2nu']:.2f}  "
      f"{'PASS' if C3 else 'FAIL'}")
    # C4 anchor
    n_red = len(obs)
    C4 = bool(n_red > 0 and n_ok > n_red / 2)
    P(f"  C4 L1 anchor: {n_ok}/{n_red} observations pass  {'PASS' if C4 else 'FAIL'}")
    R["controls"] = dict(C1=dict(pass_=C1, r=rec, A_inj=A_inj, inj=inj), C2=dict(pass_=C2, z=zs.tolist(), p=pchi),
                         C3=dict(pass_=C3, **shs), C4=dict(pass_=C4, n_ok=n_ok, n=n_red))
    ctrl_ok = C1 and C2 and C3 and C4

    # informational scan
    deltas = np.arange(-40, 40.01, 0.5)
    zscan = np.array([stack(amps(sp, NU_T + d / 1000))["z"] for d in deltas])
    P(f"\n  scan d = -40..+40 MHz (0.5 MHz): max |z| {np.nanmax(np.abs(zscan)):.2f} at d = {deltas[np.nanargmax(np.abs(zscan))]:+.1f} MHz; "
      f"#|z|>4: {int(np.sum(np.abs(zscan) > 4))}, #|z|>5: {int(np.sum(np.abs(zscan) > 5))} of {len(deltas)}")
    R["scan"] = dict(delta_MHz=deltas.tolist(), z=zscan.tolist())

    # converter-window tier (addendum A)
    per_obs = {}
    for oid in used_obs:
        st = stack([x for x in amps(sp, NU_T) if x[2]["obs"] == oid], inflate=False)
        if st["n"]:
            per_obs[oid] = st
    conv = {}
    for S in S_LIST:
        A_conv = a_of_eps(4e-9, S)
        excl = [o for o, st in per_obs.items() if st["a"] + 5 * st["sig"] < A_conv]
        frac = len(excl) / max(len(per_obs), 1)
        med_a = float(np.median([st["a"] for st in per_obs.values()])) if per_obs else np.nan
        conv[f"S{S:.0f}"] = dict(A_conv_K=A_conv, frac_obs_excluding=frac, median_a_obs=med_a,
                                 verdict="EXCLUDED" if frac >= 0.8 else ("ALLOWED?" if med_a >= A_conv / 2 else "UNDECIDED"))
        P(f"  converter-window tier S={S:.0f}: A_conv {A_conv:.3g} K DSB peak; {len(excl)}/{len(per_obs)} obs exclude it at 5 sigma "
          f"-> {conv[f'S{S:.0f}']['verdict']}")
    R["converter_tier"] = conv
    R["per_obs"] = per_obs

    # classification
    def candidate(r):
        return (r["z"] >= 5 and ctrl_ok and r["low_if"]["z"] >= 2 and r["high_if"]["z"] >= 2 and r["p_split"] > 0.01
                and r["ref"]["z"] >= 3 and abs(r["ref"]["a"] - r["a"]) <= 2 * np.hypot(r["ref"]["sig"], r["sig"])
                and abs(r["L1"]["z"]) < 3)
    cls, why = None, ""
    if len(sp) < 10:
        cls, why = "INCONCLUSIVE", "fewer than 10 usable spectra"
    elif not ctrl_ok:
        cls, why = "INCONCLUSIVE", "a control failed"
    elif any(candidate(res[k]) for k in res):
        cls, why = "LINE CANDIDATE", "z>=5 with RF-not-IF, REF-only and Level-1 absence"
    elif any(res[k]["z"] >= 5 or res[k]["z"] <= -5 for k in res):
        cls, why = "INCONCLUSIVE", "|z|>=5 failing the discriminators (artefact at target)"
    else:
        cls, why = "NULL", "z<5 at both frequencies, controls pass"
        hints = [k for k in res if 3 <= res[k]["z"] < 5]
        if hints:
            why += f"; hint (3<=z<5) at {hints}"
    R["class"] = cls; R["why"] = why
    P(f"\n  CLASS: {cls}  ({why})")
    if cls == "NULL":
        e = res["nu_t"]["eps95"]
        P(f"  eps95 at nu_t: S=10 {e['S10']:.2e} | S=50 {e['S50']:.2e} | S=1000 {e['S1000']:.2e}  vs converter window 4e-9, kill line 1e-12")
    if MUT:
        P(f"  MUTATE check: {'bites (LINE CANDIDATE)' if cls == 'LINE CANDIDATE' else 'DID NOT BITE -> pipeline blind'}")
    P("  kappa = 1/2 fitted; not theory closed; sideband gain 0.5, load coupling 1, WBS profile, S provisional.")

    # small plot (main run only)
    if not MUT:
        try:
            import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
            grid = np.arange(-45, 45.01, 0.5); num = np.zeros_like(grid); den = np.zeros_like(grid)
            for a_, e_, s in amps(sp, NU_T):
                x, r = fit_one(s["IF"][s["sb"]], s["Tall"][s["sb"]], s["flag"][s["sb"]], s["ifc"], with_line=False)
                dx = (x - s["ifc"]) * (1 if s["usb"] else -1)
                o = np.argsort(dx); ri = np.interp(grid, dx[o], r[o]); num += ri / e_ ** 2; den += 1 / e_ ** 2
            fig, ax = plt.subplots(2, 1, figsize=(7, 5), sharex=True)
            ax[0].plot(grid, num / den * 1e3, lw=0.8, color="#333")
            ax[0].axvline(0, color="#c33", lw=0.6); ax[0].axvline(36, color="#36c", lw=0.6, ls="--")
            ax[0].set_ylabel("stacked residual [mK]")
            ax[1].plot(deltas, zscan, lw=0.8, color="#333"); ax[1].axhline(5, color="#c33", lw=0.5, ls=":")
            ax[1].axhline(-5, color="#c33", lw=0.5, ls=":"); ax[1].set_ylabel("line z"); ax[1].set_xlabel("RF - 541.664 GHz [MHz]")
            fig.suptitle("CFG799 HIFI total power at 541.664 GHz (spacecraft frame)", fontsize=9)
            fig.tight_layout(); fig.savefig(os.path.join(HERE, "cfg799_stack.png"), dpi=110)
        except Exception as ex:  # noqa
            P(f"  (plot skipped: {ex})")
        rows = ["obsid,mode,target,status,t_int_h,n_datasets_h,n_datasets_v,tS,anchor_rmad,anchor_corr,anchor_ok"]
        for oid, m in man.items():
            if oid.startswith("_"):
                continue
            a = anc.get(oid, {})
            nd = m.get("n_dsets", {})
            rows.append(f"{oid},{m.get('mode','')},\"{m.get('target','')}\",{m.get('status','')},{m.get('t_int_h','')},"
                        f"{nd.get('h','')},{nd.get('v','')},{a.get('tS', float('nan')):.3f},{a.get('rmad', float('nan')):.3f},"
                        f"{a.get('corr', float('nan')):.2f},{a.get('ok','')}")
        open(os.path.join(HERE, "cfg799_manifest.csv"), "w").write("\n".join(rows) + "\n")

    json.dump(R, open(os.path.join(HERE, f"cfg799_results{SFX}.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, f"cfg799{SFX}.out"), "w").write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
