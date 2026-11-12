#!/usr/bin/env python3
"""EUC2 (DESI SOURCE HUNT): automatic search for lensed-source redshifts in the public DESI DR1 spectra of
Euclid's strong lenses, and EUC1's boost b at the true source redshift.

Frozen criteria: FROZEN_CRITERIA.md (commit 364e9d08c9).  Spectra come from euc2_fetch.py.

Run:
  python3 -I euc2.py --data-dir <dir with the two ECLIPSE csv files and desi_spectra/>
  EUC2_MUTATE=fakesep python3 -I euc2.py --data-dir <dir>        (must exit 1)

kappa = 1/2 FITTED.  Footings never pooled.  No outcome favours the framework.
"""
import argparse, csv, json, math, os, sys, time
import numpy as np
from scipy.ndimage import maximum_filter1d, median_filter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC1_eclipse_saturation_ceiling"))
import euc1 as E

MUT = (os.environ.get("EUC2_MUTATE", "") or "").strip()
C_KMS = 299792.458
OII_A, OII_B = 3727.092, 3729.875
OII_SEP, FAKE_SEP = OII_B - OII_A, 4.50
SIG_SEP = FAKE_SEP if MUT == "fakesep" else OII_SEP        # what the search treats as the signal
NEIII, HB, O3A, O3B, HA = 3869.86, 4862.683, 4960.295, 5008.240, 6564.61
DEFL = [OII_A, OII_B, HB, O3A, O3B, HA, 6585.27, 6718.29, 6732.67]
SKY = [5578.9, 6302.0, 6365.5]
WMIN, WMAX = 3600.0, 9824.0
CG = np.arange(WMIN, WMAX + 1e-9, 0.2)
DZ, ZTOP, NSL = 5.0e-5, WMAX / OII_B - 1.0, 6
SEED = 20261112
OUT = []
def P(s=""):
    print(s); OUT.append(s)

# ------------------------------------------------------------------ spectrum preparation (criteria section 2)
def prepare(sp, use_model=True):
    wl = sp["wavelength"].astype(float); flux = sp["flux"].astype(float); ivar = sp["ivar"].astype(float)
    model = sp["model"].astype(float); ws = sp["wave_sigma"].astype(float)
    good = (ivar > 0) & (sp["mask"] == 0) & np.isfinite(flux) & np.isfinite(model)
    for s in SKY: good &= np.abs(wl - s) >= 3.0
    if good.sum() < 1000: return None
    r = flux - (model if use_model else 0.0)
    rf = np.interp(wl, wl[good], r[good])
    r1 = rf - median_filter(rf, size=151, mode="nearest")
    chi = np.abs(r1) * np.sqrt(np.where(good, ivar, 0.0))
    s = np.maximum(1.4826 * median_filter(np.interp(wl, wl[good], chi[good]), size=501, mode="nearest"), 1.0)
    okw = np.isfinite(ws) & (ws > 0)
    ws = np.where(okw, ws, np.median(ws[okw]) if okw.any() else 0.8)
    return dict(wl=wl, r=r1, iv=np.where(good, ivar / s ** 2, 0.0), good=good.astype(float), ws=ws)

def mfilter(p, r=None):
    """matched filter on the 0.2 A centre grid: SN and amplitude of a unit-area Gaussian line."""
    wl, iv, good = p["wl"], p["iv"], p["good"]; r = p["r"] if r is None else r
    dwl = float(np.median(np.diff(wl)))
    sig = np.sqrt(np.interp(CG, wl, p["ws"]) ** 2 + (70.0 / C_KMS * CG) ** 2)
    k0 = np.rint((CG - wl[0]) / dwl).astype(int)
    M = int(math.ceil(5.0 * float(sig.max()) / dwl))
    N = np.zeros(len(CG)); D = np.zeros(len(CG)); Wg = np.zeros(len(CG)); Wt = np.zeros(len(CG))
    for m in range(-M, M + 1):
        k = k0 + m; inb = (k >= 0) & (k < len(wl)); kk = np.clip(k, 0, len(wl) - 1)
        lam = wl[0] + dwl * k
        t = np.exp(-0.5 * ((lam - CG) / sig) ** 2) / (sig * math.sqrt(2.0 * math.pi)) * dwl
        Wt += t; t = np.where(inb, t, 0.0)
        N += r[kk] * t * iv[kk]; D += t * t * iv[kk]; Wg += t * good[kk]
    ok = (Wg / Wt >= 0.8) & (D > 0)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(ok, N / np.sqrt(D), np.nan), np.where(ok, N / D, np.nan), np.where(ok, D, np.nan), sig

def classify(SN, A, z_ref, sep=None):
    """secure clusters of trial redshift.  Returns list of dicts (z, cls, score, per-line SN)."""
    sep = SIG_SEP if sep is None else sep
    z = np.arange(z_ref + 0.05, ZTOP, DZ)
    if len(z) < 20: return []
    def at(lam0):
        lam = lam0 * (1.0 + z); ok = (lam >= WMIN) & (lam <= WMAX)
        for d in DEFL: ok &= np.abs(lam - d * (1.0 + z_ref)) > 6.0
        i = np.clip(np.rint((lam - WMIN) / 0.2).astype(int), 0, len(SN) - 1)
        return np.where(ok, SN[i], np.nan), np.where(ok, A[i], np.nan)
    def sl(x): return maximum_filter1d(np.where(np.isfinite(x), x, -1e9), 2 * NSL + 1, mode="nearest")
    s1, a1 = at(OII_A); s2, a2 = at(OII_A + sep)
    both = (s1 > 0) & (s2 > 0)
    S2 = np.where(both, np.sqrt(np.where(both, s1, 0.0) ** 2 + np.where(both, s2, 0.0) ** 2), 0.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(both, a2 / a1, np.nan)
    secD = (S2 >= 7.0) & (s1 >= 3.0) & (s2 >= 3.0) & (ratio >= 0.35) & (ratio <= 2.0)
    sNe, _ = at(NEIII); sHb, _ = at(HB); sOa, aOa = at(O3A); sOb, aOb = at(O3B); sHa, _ = at(HA)
    with np.errstate(divide="ignore", invalid="ignore"):
        r3 = aOb / aOa
    pair = (sOa >= 4.0) & (~np.isfinite(sOb) | ((r3 >= 1.5) & (r3 <= 6.0)))
    pair_sl = maximum_filter1d(pair.astype(np.uint8), 2 * NSL + 1, mode="nearest") > 0
    lNe, lHb, lOb, lHa, lS2 = sl(sNe), sl(sHb), sl(sOb), sl(sHa), sl(S2)
    o_oii = (lNe >= 4) | (lHb >= 4) | pair_sl | (lOb >= 4) | (lHa >= 4)
    o_o3 = (lS2 >= 4) | (lNe >= 4) | (lHb >= 4) | pair_sl | (lHa >= 4)
    o_ha = (lS2 >= 4) | (lNe >= 4) | (lHb >= 4) | pair_sl | (lOb >= 4)
    secM = ((S2 >= 6.0) & o_oii) | ((sOb >= 6.0) & o_o3) | ((sHa >= 6.0) & o_ha)
    sec = secD | secM
    if not sec.any(): return []
    def q(x): return np.where(x >= 2.5, x, 0.0) ** 2
    score = np.sqrt(q(np.nan_to_num(s1, nan=0.0)) + q(np.nan_to_num(s2, nan=0.0)) + q(lNe) + q(lHb) + q(sl(sOa)) + q(lOb) + q(lHa))
    idx = np.where(sec)[0]; cuts = np.where(np.diff(z[idx]) > 0.002)[0]
    out = []
    for grp in np.split(idx, cuts + 1):
        j = grp[int(np.argmax(score[grp]))]
        f = lambda x: (float(x[j]) if np.isfinite(x[j]) and x[j] > -1e8 else float("nan"))
        out.append(dict(z=float(z[j]), cls="D" if secD[grp].any() else "M", score=float(score[j]), S_OII=float(S2[j]),
                        sn_a=f(s1), sn_b=f(s2), ratio=f(ratio), NeIII=f(lNe), Hb=f(lHb), OIIIa=f(sl(sOa)), OIIIb=f(lOb), Ha=f(lHa)))
    return out

def hunt(p, z_ref, flip=False, sep=None, inject=None):
    r = p["r"] if inject is None else p["r"] + inject
    SN, A, D, sig = mfilter(p, r)
    if flip: SN, A = -SN, -A
    return classify(SN, A, z_ref, sep), (SN, A, D, sig)

def best(cl):
    if not cl: return None, False
    b = max(cl, key=lambda c: c["score"])
    return b, any(abs(c["z"] - b["z"]) > 0.01 for c in cl)

# ================================================================== main
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args()
    t0 = time.time(); tag = "euc2" + ("_MUTATE_" + MUT if MUT else "")
    sdir = os.path.join(a.data_dir, "desi_spectra")
    P("EUC2 (DESI SOURCE HUNT)%s" % ("   *** MUTATE = %s ***" % MUT if MUT else ""))
    rows, _ = E.load(a.data_dir)
    byid = {r["id"]: r for r in rows}
    Sm, _ = E.select(rows, ("A", "B")); Pm, _ = E.select(rows, ("A",))
    inS = {r["id"] for r in Sm}; inP = {r["id"] for r in Pm}
    M = list(csv.DictReader(open(os.path.join(HERE, "euc2_matches.csv"))))
    for m in M:
        m["flagged"] = m["flagged"] == "True"; m["z_desi"] = float(m["z_desi"]); m["zwarn"] = int(float(m["zwarn"]))
        m["primary"] = m["specprimary"] in ("True", "true", "1")
        m["zcat"] = float(m["desi_deflector_specz"]) if m["desi_deflector_specz"] else float("nan")
    lenses = sorted({m["unique_identifier"] for m in M})
    P("\n[spectra] %d spectra on %d lenses (flagged lenses %d, extension lenses %d)"
      % (len(M), len(lenses), len({m["unique_identifier"] for m in M if m["flagged"]}),
         len({m["unique_identifier"] for m in M if not m["flagged"]})))

    # ---------------------------------------------------------------- roles (criteria section 3)
    for m in M:
        lid = m["unique_identifier"]; k = byid.get(lid)
        if m["flagged"]:
            m["role"], m["z_ref"] = "deflector", m["zcat"]
        elif k is None or not (k["z"] > 0):
            m["role"], m["z_ref"] = "unused", float("nan")
        elif m["zwarn"] == 0 and (k["zlo"] - 0.1) <= m["z_desi"] <= (k["zhi"] + 0.1):
            m["role"], m["z_ref"] = "deflector", m["z_desi"]
        elif m["zwarn"] == 0 and m["spectype"] == "GALAXY" and m["z_desi"] >= k["zhi"] + 0.15:
            m["role"], m["z_ref"] = "source_candidate", k["z"]
        else:
            m["role"], m["z_ref"] = "unused", float("nan")
    P("  roles: deflector %d (flagged %d, extension %d), source candidates %d, unused %d"
      % (sum(m["role"] == "deflector" for m in M), sum(m["role"] == "deflector" and m["flagged"] for m in M),
         sum(m["role"] == "deflector" and not m["flagged"] for m in M), sum(m["role"] == "source_candidate" for m in M),
         sum(m["role"] == "unused" for m in M)))

    # ---------------------------------------------------------------- the search
    prepared, det, nmiss = {}, [], 0
    nD_real = nfake = nflip = ncand = 0
    for m in M:
        if m["role"] == "unused": continue
        fp = os.path.join(sdir, m["sparcl_id"] + ".npz")
        if not os.path.exists(fp): nmiss += 1; continue
        sp = np.load(fp); p = prepare(sp, use_model=(m["role"] == "deflector"))
        if p is None or not np.isfinite(m["z_ref"]): continue
        cl, (SN, A, D, sig) = hunt(p, m["z_ref"])
        if m["role"] == "deflector":
            prepared[m["sparcl_id"]] = (p, m["z_ref"])
            nD_real += sum(c["cls"] == "D" for c in cl)
            nfake += sum(c["cls"] == "D" for c in classify(SN, A, m["z_ref"], sep=(OII_SEP if MUT == "fakesep" else FAKE_SEP))
                         if c["S_OII"] >= 7 and c["sn_a"] >= 3 and c["sn_b"] >= 3)
            nflip += len(classify(-SN, -A, m["z_ref"]))
            b, multi = best(cl)
            if b is None and np.nanmax(np.where(np.isfinite(SN), SN, -1)) >= 8.0: ncand += 1
            if b is not None:
                det.append(dict(m, z_s=b["z"], cls="SECURE-" + b["cls"], multi=multi, **{k: b[k] for k in
                           ("score", "S_OII", "sn_a", "sn_b", "ratio", "NeIII", "Hb", "OIIIa", "OIIIb", "Ha")}))
        else:
            hit = [c for c in cl if abs(c["z"] - m["z_desi"]) < 0.002]
            if hit:
                b = max(hit, key=lambda c: c["score"])
                det.append(dict(m, z_s=m["z_desi"], cls="SECURE-Z", multi=False, **{k: b[k] for k in
                           ("score", "S_OII", "sn_a", "sn_b", "ratio", "NeIII", "Hb", "OIIIa", "OIIIb", "Ha")}))
    P("  spectra missing on disk: %d" % nmiss)
    P("\n[search] secure detections: %d spectra  (SECURE-D %d, SECURE-M %d, SECURE-Z %d); single-line candidates (unused) %d"
      % (len(det), sum(d["cls"] == "SECURE-D" for d in det), sum(d["cls"] == "SECURE-M" for d in det),
         sum(d["cls"] == "SECURE-Z" for d in det), ncand))

    # per lens
    src, excl = {}, []
    for lid in sorted({d["unique_identifier"] for d in det}):
        dd = [d for d in det if d["unique_identifier"] == lid]
        if any(d["multi"] for d in dd) or max(d["z_s"] for d in dd) - min(d["z_s"] for d in dd) > 0.01:
            excl.append(lid); continue
        src[lid] = max(dd, key=lambda d: d["score"])
    P("  lenses with one secure source redshift: %d; excluded for conflicting secure redshifts: %d %s" % (len(src), len(excl), excl))

    # ---------------------------------------------------------------- instrument checks
    P("\n[instrument checks]")
    CK = {}
    def ck(k, what, val, ok):
        CK[k] = dict(what=what, value=val, ok=bool(ok)); P("  %s %-3s %s : %s" % ("PASS" if ok else "FAIL", k, what, val))
    # H1 injection
    rng = np.random.default_rng(SEED); keys = sorted(prepared)
    rec = tried = 0
    while tried < 200 and keys:
        p, zr = prepared[keys[int(rng.integers(0, len(keys)))]]
        if zr + 0.1 >= 1.6: continue
        zi = float(rng.uniform(zr + 0.1, 1.6))
        SN, A, D, sig = mfilter(p)
        la, lb = OII_A * (1 + zi), (OII_A + SIG_SEP) * (1 + zi)
        ia, ib = int(round((la - WMIN) / 0.2)), int(round((lb - WMIN) / 0.2))
        if ib >= len(CG) or not (np.isfinite(D[ia]) and np.isfinite(D[ib])): continue
        if any(abs(la - d * (1 + zr)) <= 8.0 or abs(lb - d * (1 + zr)) <= 8.0 for d in DEFL): continue
        Aa = 10.0 / math.sqrt(D[ia] + 1.69 * D[ib]); dwl = float(np.median(np.diff(p["wl"])))
        g = lambda lam, s: np.exp(-0.5 * ((p["wl"] - lam) / s) ** 2) / (s * math.sqrt(2 * math.pi)) * dwl
        inj = Aa * g(la, sig[ia]) + 1.3 * Aa * g(lb, sig[ib])
        cl, _ = hunt(p, zr, inject=inj); tried += 1
        rec += any(abs(c["z"] - zi) < 3e-4 for c in cl)
    ck("H1", "injected [O II] doublets at S = 10 recovered as secure, |dz| < 3e-4, >= 90%", "%d / %d = %.3f" % (rec, tried, rec / max(tried, 1)),
       tried > 0 and rec / tried >= 0.90)
    lim = max(1, 0.2 * nD_real)
    ck("H2", "fake-separation null: SECURE-D-like clusters at 4.50 A <= max(1, 20%% of the real %d)" % nD_real,
       "%d  (sign-flipped null, all classes: %d clusters)" % (nfake, nflip), nfake <= lim)
    fl = [m for m in M if m["flagged"] and m["primary"]]
    okj = sum(abs(m["z_desi"] - m["zcat"]) < 0.002 for m in fl)
    ck("H3", "flagged lenses, primary spectrum: |z_DESI - catalogue| < 0.002 in >= 95%", "%d / %d = %.3f" % (okj, len(fl), okj / max(len(fl), 1)),
       len(fl) > 0 and okj / len(fl) >= 0.95)
    kid = "EUCL-DR1-L015763"; km = [m for m in M if m["unique_identifier"] == kid]
    if km:
        zk = src.get(kid, {}).get("z_s", float("nan"))
        okk = np.isfinite(zk) and abs(zk - 1.366) <= 0.01
        CK["H4"] = dict(what="known pair EUCL-DR1-L015763, z_s = 1.366", value=zk, ok=bool(okk))
        P("  %s H4  known pair %s (z_s = 1.366 +- 0.008): %d spectra, search returns %s" % ("PASS" if okk else "MISS", kid, len(km),
          "z_s = %.4f" % zk if np.isfinite(zk) else "no secure redshift"))
    else:
        CK["H4"] = dict(what="known pair EUCL-DR1-L015763", value="no DESI spectrum within 1.5 arcsec", ok=True)
        P("  note H4  %s: no DESI spectrum within 1.5 arcsec" % kid)
    gr = {g: sum(1 for l, d in src.items() if d["flagged"] and d["grade"] == g) for g in "ABC"}
    P("       H5  secure systems among flagged lenses by grade A / B / C: %d / %d / %d   (paper, by eye: 12 / 5 / 3)" % (gr["A"], gr["B"], gr["C"]))
    CK["H5"] = dict(what="yield reference", value=gr, ok=True)

    RES = dict(lane="EUC2", criteria_commit="364e9d08c9", mutate=MUT, n_spectra=len(M), n_lenses=len(lenses),
               n_secure_spectra=len(det), n_secure_lenses=len(src), excluded=excl, nD_real=nD_real, n_fake=nfake, n_flip=nflip,
               n_candidates=ncand, checks=CK)
    if MUT:
        ref = json.load(open(os.path.join(HERE, "euc2_results.json")))
        ok = nD_real < 0.2 * ref["nD_real"]
        P("\n[MUTATE %s] SECURE-D clusters with the 4.50 A separation as signal: %d (reference %d) -> %s"
          % (MUT, nD_real, ref["nD_real"], "below 20%, as required; exit 1" if ok else "NOT below 20%"))
        json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1, default=str)
        open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if ok else 2)

    # ---------------------------------------------------------------- detections table
    P("\n[secure sources, one row per lens]")
    P("  %-17s %s %-4s %-3s %-9s %7s %7s %6s %6s %5s  %s" % ("lens", "g", "P/S", "fl", "class", "z_ref", "z_s", "S_OII", "score", "sep", "other lines (SN)"))
    for lid, d in sorted(src.items(), key=lambda kv: kv[1]["z_s"]):
        oth = ", ".join("%s %.1f" % (k, d[k]) for k in ("NeIII", "Hb", "OIIIa", "OIIIb", "Ha") if np.isfinite(d[k]) and d[k] >= 3.0)
        P("  %-17s %s %-4s %-3s %-9s %7.4f %7.4f %6.1f %6.1f %5.2f  %s" % (lid, d["grade"], "P" if lid in inP else ("S" if lid in inS else "-"),
          "yes" if d["flagged"] else "no", d["cls"], d["z_ref"], d["z_s"], d["S_OII"], d["score"], float(d["sep_arcsec"]), oth))
    with open(os.path.join(HERE, "euc2_sources.csv"), "w", newline="") as f:
        cols = ["unique_identifier", "grade", "flagged", "in_P", "in_S", "cls", "z_ref", "z_s", "role", "sparcl_id", "targetid", "sep_arcsec",
                "z_desi", "zwarn", "score", "S_OII", "sn_a", "sn_b", "ratio", "NeIII", "Hb", "OIIIa", "OIIIb", "Ha"]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader()
        for lid, d in sorted(src.items()): w.writerow(d)

    # ---------------------------------------------------------------- the reading (criteria section 5)
    P("\n[reading: EUC1's boost b at the true source redshift]")
    READ = {}
    def reading(name, sample):
        sel = [r for r in sample if r["id"] in src]
        if not sel:
            P("  %s: no lens with a secure source redshift" % name); READ[name] = dict(N=0); return
        zs = np.array([src[r["id"]]["z_s"] for r in sel]); zph = E.arr(sel, "z")
        zl = np.array([src[r["id"]]["z_ref"] if src[r["id"]]["role"] == "deflector" else r["z"] for r in sel])
        lm = E.arr(sel, "lm") + 2.0 * np.log10(E.EUCLID.DL(zl) / E.EUCLID.DL(zph))
        eng, z, RE, Re, n, lm = E.build(sel, z=zl, lm=lm)
        out = dict(N=len(sel), per_lens=[])
        bt, bi = {}, {}
        for law in ("S", "B"):
            for nm, a0 in E.FOOT.items():
                bt[(law, nm)] = eng.solve_b(math.pi * RE ** 2 * E.EUCLID.sigcr(z, zs), a0, law)
                bi[(law, nm)] = eng.solve_b(math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF), a0, law)
                st = E.stats(bt[(law, nm)]); si = E.stats(bi[(law, nm)])
                out["%s_%s" % (law, nm)] = dict(true=st, inf=si)
                P("  %s law %s %-9s N=%2d  b_med(true z_s) = %+.3f [%+.3f, %+.3f]   b_med(source-free) = %+.3f   f25(true) = %.2f"
                  % (name, law, nm, len(sel), st["b_med"], st["b_med_lo"], st["b_med_hi"], si["b_med"], st["f25"]))
        P("  %s per lens (law S): id, z_l, z_s, theta_E, log M*, b canonical / alt, source-free b alt" % name)
        for i in np.argsort(zs):
            r = sel[i]
            P("    %-17s %.3f %.3f %5.2f\" %6.2f   %+.3f / %+.3f   (%+.3f)%s" % (r["id"], zl[i], zs[i], r["tE"], lm[i], bt[("S", "canonical")][i],
              bt[("S", "alt")][i], bi[("S", "alt")][i], "  [theta_E > 2 arcsec]" if r["tE"] > 2.0 else ""))
            out["per_lens"].append(dict(id=r["id"], z_l=float(zl[i]), z_s=float(zs[i]), theta_E=r["tE"], logM=float(lm[i]),
                                        b_S_canonical=float(bt[("S", "canonical")][i]), b_S_alt=float(bt[("S", "alt")][i]),
                                        b_inf_S_alt=float(bi[("S", "alt")][i])))
        READ[name] = out
    reading("P", Pm); reading("S", Sm)
    nP = READ["P"]["N"]
    if nP >= 10:
        w = {}
        for nm in E.FOOT:
            st = READ["P"]["S_" + nm]["true"]
            w[nm] = "LENS GATE HOLDS" if st["b_med_hi"] <= 0.15 else ("LENS GATE FAILS" if st["b_med_lo"] >= 0.25 else "NO VERDICT")
        word = "EUC1-F: %s / %s" % (w["canonical"], w["alt"])
    else:
        word = "EARLY READING, NOT A GATE (N(P) = %d < 10; EUC1-F stays open)" % nP
    RES["reading"] = READ; RES["word"] = word
    allok = all(CK[k]["ok"] for k in ("H1", "H2", "H3"))
    P("\n[summary]")
    P("  instrument checks H1-H3: %s" % ("all pass" if allok else "FAILED -> NOT EVALUABLE"))
    P("  %s" % (word if allok else "NOT EVALUABLE"))
    P("  kappa = 1/2 FITTED. No outcome favours the framework.  (%.0f s)" % (time.time() - t0))
    RES["checks_all_pass"] = allok

    # ---------------------------------------------------------------- figures (every secure lens)
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        os.makedirs(os.path.join(HERE, "figs"), exist_ok=True)
        items = sorted(src.items(), key=lambda kv: kv[1]["z_s"])
        for pg in range(0, len(items), 6):
            chunk = items[pg:pg + 6]
            fig, ax = plt.subplots(len(chunk), 4, figsize=(15, 2.3 * len(chunk)), squeeze=False)
            for i, (lid, d) in enumerate(chunk):
                sp = np.load(os.path.join(sdir, d["sparcl_id"] + ".npz")); p = prepare(sp, use_model=(d["role"] == "deflector"))
                err = np.where(p["iv"] > 0, 1.0 / np.sqrt(np.where(p["iv"] > 0, p["iv"], 1.0)), np.nan)
                for j, (nm, lines, hw) in enumerate((("[O II]", (OII_A, OII_B), 14.0), ("H-beta", (HB,), 20.0),
                                                     ("[O III]", (O3A, O3B), 45.0), ("H-alpha", (HA,), 20.0))):
                    c = np.mean(lines) * (1 + d["z_s"]); q = (p["wl"] > c - hw * (1 + d["z_s"]) / 1.5) & (p["wl"] < c + hw * (1 + d["z_s"]) / 1.5)
                    axx = ax[i, j]
                    if c < WMIN or c > WMAX or q.sum() < 5:
                        axx.text(0.5, 0.5, nm + " out of range", ha="center", transform=axx.transAxes, fontsize=8); axx.set_xticks([]); axx.set_yticks([]); continue
                    axx.step(p["wl"][q], p["r"][q], where="mid", lw=0.8, color="k")
                    axx.fill_between(p["wl"][q], -err[q], err[q], color="0.85", step="mid")
                    for l in lines: axx.axvline(l * (1 + d["z_s"]), color="r", lw=0.6, ls="--")
                    axx.tick_params(labelsize=6)
                    axx.set_title("%s  %s  %s z_l=%.3f z_s=%.4f  S_OII=%.1f" % (lid[-7:], d["cls"], nm, d["z_ref"], d["z_s"], d["S_OII"]) if j == 0 else nm, fontsize=7)
            fig.tight_layout(); fig.savefig(os.path.join(HERE, "figs", "secure_%02d.png" % (pg // 6)), dpi=70); plt.close(fig)
    except Exception as ex:
        P("  (figures skipped: %s)" % type(ex).__name__)

    json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if allok else 3)

if __name__ == "__main__":
    main()
