#!/usr/bin/env python3
"""EUC2 under AMENDMENT A1 (post hoc, disclosed; AMENDMENT_A1.md, commit a24ffd2dc2).

The frozen SECURE-D thresholds plus a pixel-level doublet-preference fit: a cluster is kept only if a doublet beats the
best single line (free centre, free width from a sub-resolution spike to a broad bump) by chi^2 >= 4.  SECURE-M is an
annotation only.  H2 (fake-separation null) is the gate.  Everything this script prints is POST HOC READING (A1).

Run:  python3 -I euc2_a1.py --data-dir <dir with the two ECLIPSE csv files and desi_spectra/>
"""
import argparse, csv, json, math, os, sys, time
import numpy as np
from scipy.special import erf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import euc2 as H
E = H.E
OII_A, OII_SEP, C_KMS, WMIN, WMAX, DZ, ZTOP = H.OII_A, H.OII_SEP, H.C_KMS, H.WMIN, H.WMAX, H.DZ, H.ZTOP
DCHI_MIN = 4.0
OUT = []
def P(s=""):
    print(s); OUT.append(s)

def pixgauss(x, c, sg, dwl):
    """unit-area Gaussian integrated over each pixel, per Angstrom."""
    q = sg * math.sqrt(2.0)
    return 0.5 * (erf((x + 0.5 * dwl - c) / q) - erf((x - 0.5 * dwl - c) / q)) / dwl

def d_clusters(SN, A, z_ref, sep):
    """clusters of the FROZEN SECURE-D condition (same thresholds as euc2.classify), peak = largest S_OII."""
    z = np.arange(z_ref + 0.05, ZTOP, DZ)
    if len(z) < 20: return []
    def at(lam0):
        lam = lam0 * (1.0 + z); ok = (lam >= WMIN) & (lam <= WMAX)
        for d in H.DEFL: ok &= np.abs(lam - d * (1.0 + z_ref)) > 6.0
        i = np.clip(np.rint((lam - WMIN) / 0.2).astype(int), 0, len(SN) - 1)
        return np.where(ok, SN[i], np.nan), np.where(ok, A[i], np.nan)
    s1, a1 = at(OII_A); s2, a2 = at(OII_A + sep)
    both = (s1 > 0) & (s2 > 0)
    S2 = np.where(both, np.sqrt(np.where(both, s1, 0.0) ** 2 + np.where(both, s2, 0.0) ** 2), 0.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(both, a2 / a1, np.nan)
    sec = (S2 >= 7.0) & (s1 >= 3.0) & (s2 >= 3.0) & (ratio >= 0.35) & (ratio <= 2.0)
    if not sec.any(): return []
    idx = np.where(sec)[0]; out = []
    for grp in np.split(idx, np.where(np.diff(z[idx]) > 0.002)[0] + 1):
        j = grp[int(np.argmax(S2[grp]))]
        ann = {}
        for nm, lam0 in (("NeIII", H.NEIII), ("Hb", H.HB), ("OIIIb", H.O3B), ("Ha", H.HA)):
            s, _ = at(lam0); w = s[max(j - H.NSL, 0): j + H.NSL + 1]
            ann[nm] = float(np.nanmax(w)) if np.isfinite(w).any() else float("nan")
        out.append(dict(z0=float(z[j]), S_OII=float(S2[j]), sn_a=float(s1[j]), sn_b=float(s2[j]), **ann))
    return out

def dfit(p, z0, sep, r):
    """doublet against the best single line.  Returns dict(dchi, z, sv, ratio) or None."""
    wl, iv = p["wl"], p["iv"]; dwl = float(np.median(np.diff(wl)))
    s = sep * (1.0 + z0); la0 = OII_A * (1.0 + z0); lb0 = la0 + s
    q = (wl >= la0 - 2.5 * s) & (wl <= lb0 + 2.5 * s) & (iv > 0)
    if q.sum() < 12: return None
    x, y, w = wl[q], r[q], iv[q]
    chi0 = float(np.sum(w * y * y)); wsa = float(np.interp(la0, wl, p["ws"]))
    best2 = None
    for dz in np.arange(-6, 7) * DZ:
        z = z0 + dz; la = OII_A * (1.0 + z); lb = (OII_A + sep) * (1.0 + z)
        for sv in (40.0, 70.0, 110.0, 160.0):
            sg = math.sqrt(wsa ** 2 + (sv / C_KMS * la) ** 2)
            ga, gb = pixgauss(x, la, sg, dwl), pixgauss(x, lb, sg, dwl)
            Saa, Sbb, Sab = np.sum(w * ga * ga), np.sum(w * gb * gb), np.sum(w * ga * gb)
            Sya, Syb = np.sum(w * y * ga), np.sum(w * y * gb)
            det = Saa * Sbb - Sab * Sab
            if det <= 0: continue
            Aa, Ab = (Sya * Sbb - Syb * Sab) / det, (Syb * Saa - Sya * Sab) / det
            if Aa <= 0 or Ab <= 0: continue
            chi = chi0 - (Aa * Sya + Ab * Syb)
            if best2 is None or chi < best2[0]: best2 = (float(chi), float(z), sv, float(Aa), float(Ab))
    if best2 is None: return None
    cs = np.arange(la0 - s, lb0 + s + 1e-9, 0.2)[:, None, None]
    sgs = np.geomspace(0.4, 4.0 * s, 16)[None, :, None]
    g = pixgauss(x[None, None, :], cs, sgs, dwl)
    Syg = np.sum(w * y * g, axis=2); Sgg = np.sum(w * g * g, axis=2)
    with np.errstate(divide="ignore", invalid="ignore"):
        gain = np.where((Syg > 0) & (Sgg > 0), Syg ** 2 / Sgg, 0.0)
    chi1 = chi0 - float(gain.max())
    return dict(dchi=chi1 - best2[0], z=best2[1], sv=best2[2], ratio=best2[4] / best2[3], Aa=best2[3], Ab=best2[4])

def a1_hunt(p, z_ref, sep=OII_SEP, inject=None):
    r = p["r"] if inject is None else p["r"] + inject
    SN, A, D, sig = H.mfilter(p, r)
    out = []
    for c in d_clusters(SN, A, z_ref, sep):
        f = dfit(p, c["z0"], sep, r)
        if f is None or f["dchi"] < DCHI_MIN or not (0.35 <= f["ratio"] <= 2.0): continue
        out.append(dict(c, z=f["z"], dchi=f["dchi"], ratio=f["ratio"], sv=f["sv"], Aa=f["Aa"], Ab=f["Ab"]))
    return out, (SN, A, D, sig)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args()
    t0 = time.time(); sdir = os.path.join(a.data_dir, "desi_spectra")
    P("EUC2 under AMENDMENT A1  (POST HOC READING; the frozen search keeps its own word)")
    rows, _ = E.load(a.data_dir); E.OUT.clear()
    byid = {r["id"]: r for r in rows}
    Sm, _ = E.select(rows, ("A", "B")); Pm, _ = E.select(rows, ("A",))
    inS = {r["id"] for r in Sm}; inP = {r["id"] for r in Pm}
    M = list(csv.DictReader(open(os.path.join(HERE, "euc2_matches.csv"))))
    for m in M:
        m["flagged"] = m["flagged"] == "True"; m["z_desi"] = float(m["z_desi"]); m["zwarn"] = int(float(m["zwarn"]))
        m["primary"] = m["specprimary"] in ("True", "true", "1")
        m["zcat"] = float(m["desi_deflector_specz"]) if m["desi_deflector_specz"] else float("nan")
        k = byid.get(m["unique_identifier"])
        if m["flagged"]: m["role"], m["z_ref"] = "deflector", m["zcat"]
        elif k is None or not (k["z"] > 0): m["role"], m["z_ref"] = "unused", float("nan")
        elif m["zwarn"] == 0 and (k["zlo"] - 0.1) <= m["z_desi"] <= (k["zhi"] + 0.1): m["role"], m["z_ref"] = "deflector", m["z_desi"]
        elif m["zwarn"] == 0 and m["spectype"] == "GALAXY" and m["z_desi"] >= k["zhi"] + 0.15: m["role"], m["z_ref"] = "source_candidate", k["z"]
        else: m["role"], m["z_ref"] = "unused", float("nan")
    P("\n[spectra] %d spectra on %d lenses; roles: deflector %d (flagged %d, extension %d), source candidates %d, unused %d"
      % (len(M), len({m["unique_identifier"] for m in M}), sum(m["role"] == "deflector" for m in M),
         sum(m["role"] == "deflector" and m["flagged"] for m in M), sum(m["role"] == "deflector" and not m["flagged"] for m in M),
         sum(m["role"] == "source_candidate" for m in M), sum(m["role"] == "unused" for m in M)))

    FAKES = (1.80, 4.00, 4.50, 5.20)
    prepared, det = {}, []; nreal = 0; nfake = {s: 0 for s in FAKES}; nmiss = 0; nfrozenD = 0
    for m in M:
        if m["role"] == "unused" or not np.isfinite(m["z_ref"]): continue
        fp = os.path.join(sdir, m["sparcl_id"] + ".npz")
        if not os.path.exists(fp): nmiss += 1; continue
        p = H.prepare(np.load(fp), use_model=(m["role"] == "deflector"))
        if p is None: continue
        dets, (SN, A, D, sig) = a1_hunt(p, m["z_ref"])
        if m["role"] == "deflector":
            prepared[m["sparcl_id"]] = (p, m["z_ref"]); nreal += len(dets)
            nfrozenD += len(d_clusters(SN, A, m["z_ref"], OII_SEP))
            for s in FAKES: nfake[s] += len(a1_hunt(p, m["z_ref"], sep=s)[0])
            for d in dets: det.append(dict(m, cls="SECURE-A1", z_s=d["z"], **{k: d[k] for k in ("S_OII", "sn_a", "sn_b", "dchi", "ratio", "sv", "NeIII", "Hb", "OIIIb", "Ha", "Aa", "Ab")}))
        else:
            hit = [d for d in dets if abs(d["z"] - m["z_desi"]) < 0.002]
            if hit:
                d = max(hit, key=lambda d: d["S_OII"])
                det.append(dict(m, cls="SECURE-Z-A1", z_s=m["z_desi"], **{k: d[k] for k in ("S_OII", "sn_a", "sn_b", "dchi", "ratio", "sv", "NeIII", "Hb", "OIIIb", "Ha", "Aa", "Ab")}))
    P("  spectra missing on disk: %d" % nmiss)
    P("\n[search] frozen SECURE-D clusters on deflector spectra: %d; kept by the doublet-preference fit (SECURE-A1): %d" % (nfrozenD, nreal))
    src, excl = {}, []
    for lid in sorted({d["unique_identifier"] for d in det}):
        dd = [d for d in det if d["unique_identifier"] == lid]
        if max(d["z_s"] for d in dd) - min(d["z_s"] for d in dd) > 0.01: excl.append(lid); continue
        src[lid] = max(dd, key=lambda d: d["S_OII"])
    P("  lenses with one A1-secure source redshift: %d; excluded for conflicting redshifts: %d %s" % (len(src), len(excl), excl))

    # ---------------------------------------------------------------- checks
    P("\n[checks under A1]")
    CK = {}
    lim = max(1, 0.2 * nreal); okH2 = nfake[4.50] <= lim
    P("  %s H2  fake-separation null at 4.50 A: %d  (limit max(1, 20%% of %d) = %.1f);  other fake separations 1.80 / 4.00 / 5.20 A: %d / %d / %d"
      % ("PASS" if okH2 else "FAIL", nfake[4.50], nreal, lim, nfake[1.80], nfake[4.00], nfake[5.20]))
    CK["H2"] = dict(fake=nfake, real=nreal, ok=bool(okH2))
    keys = sorted(prepared)
    for S in (10.0, 14.0):
        rng = np.random.default_rng(H.SEED); rec = tried = 0
        while tried < 200 and keys:
            p, zr = prepared[keys[int(rng.integers(0, len(keys)))]]
            if zr + 0.1 >= 1.6: continue
            zi = float(rng.uniform(zr + 0.1, 1.6))
            SN, A, D, sig = H.mfilter(p)
            la, lb = OII_A * (1 + zi), (OII_A + OII_SEP) * (1 + zi)
            ia, ib = int(round((la - WMIN) / 0.2)), int(round((lb - WMIN) / 0.2))
            if ib >= len(H.CG) or not (np.isfinite(D[ia]) and np.isfinite(D[ib])): continue
            if any(abs(la - d * (1 + zr)) <= 8.0 or abs(lb - d * (1 + zr)) <= 8.0 for d in H.DEFL): continue
            Aa = S / math.sqrt(D[ia] + 1.69 * D[ib]); dwl = float(np.median(np.diff(p["wl"])))
            g = lambda lam, s: np.exp(-0.5 * ((p["wl"] - lam) / s) ** 2) / (s * math.sqrt(2 * math.pi)) * dwl
            dets, _ = a1_hunt(p, zr, inject=Aa * g(la, sig[ia]) + 1.3 * Aa * g(lb, sig[ib])); tried += 1
            rec += any(abs(d["z"] - zi) < 3e-4 for d in dets)
        CK["H1_S%d" % S] = dict(rec=rec, tried=tried)
        P("       H1  injected doublets at S = %2.0f recovered: %d / %d = %.3f   (reported, not a gate under A1)" % (S, rec, tried, rec / max(tried, 1)))
    fl = [m for m in M if m["flagged"] and m["primary"]]; okj = sum(abs(m["z_desi"] - m["zcat"]) < 0.002 for m in fl)
    P("  %s H3  flagged, primary spectrum: |z_DESI - catalogue| < 0.002: %d / %d = %.3f" % ("PASS" if okj / max(len(fl), 1) >= 0.95 else "FAIL", okj, len(fl), okj / max(len(fl), 1)))
    CK["H3"] = dict(ok=bool(okj / max(len(fl), 1) >= 0.95), n=okj, N=len(fl))
    kid = "EUCL-DR1-L015763"; zk = src.get(kid, {}).get("z_s", float("nan"))
    P("  %s H4  known pair %s (z_s = 1.366 +- 0.008): %s" % ("PASS" if np.isfinite(zk) and abs(zk - 1.366) <= 0.01 else "MISS", kid,
      "z_s = %.4f" % zk if np.isfinite(zk) else "no A1-secure redshift"))
    CK["H4"] = dict(z=zk, ok=bool(np.isfinite(zk) and abs(zk - 1.366) <= 0.01))
    gr = {g: sum(1 for l, d in src.items() if d["flagged"] and d["grade"] == g) for g in "ABC"}
    P("       H5  A1-secure systems among flagged lenses by grade A / B / C: %d / %d / %d   (paper, by eye: 12 / 5 / 3)" % (gr["A"], gr["B"], gr["C"]))

    # ---------------------------------------------------------------- table
    P("\n[A1-secure sources, one row per lens]")
    P("  %-17s %s %-3s %-3s %-5s %-5s %7s %7s %6s %6s %5s %4s  %s" % ("lens", "g", "set", "fl", "model", "final", "z_ref", "z_s", "S_OII", "dchi2", "ratio", "sv", "other lines (SN >= 3)"))
    for lid, d in sorted(src.items(), key=lambda kv: kv[1]["z_s"]):
        k = byid.get(lid); oth = ", ".join("%s %.1f" % (nm, d[nm]) for nm in ("NeIII", "Hb", "OIIIb", "Ha") if np.isfinite(d[nm]) and d[nm] >= 3.0)
        P("  %-17s %s %-3s %-3s %-5s %-5s %7.4f %7.4f %6.1f %6.1f %5.2f %4.0f  %s" % (lid, d["grade"], "P" if lid in inP else ("S" if lid in inS else "-"),
          "yes" if d["flagged"] else "no", ("yes" if k["success"] else "no") if k else "n/a", ("yes" if k["final"] else "no") if k else "n/a",
          d["z_ref"], d["z_s"], d["S_OII"], d["dchi"], d["ratio"], d["sv"], oth))
    with open(os.path.join(HERE, "euc2_a1_sources.csv"), "w", newline="") as f:
        cols = ["unique_identifier", "grade", "flagged", "cls", "role", "z_ref", "z_s", "S_OII", "sn_a", "sn_b", "dchi", "ratio", "sv",
                "NeIII", "Hb", "OIIIb", "Ha", "sparcl_id", "targetid", "sep_arcsec", "z_desi", "zwarn", "survey", "program"]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader()
        for lid, d in sorted(src.items()): w.writerow(d)

    # ---------------------------------------------------------------- reading
    P("\n[POST HOC READING (A1): EUC1's boost b at the true source redshift]")
    READ = {}
    def reading(name, sample, note=""):
        sel = [r for r in sample if r["id"] in src]
        if not sel:
            P("  %s: no lens with an A1-secure source redshift" % name); READ[name] = dict(N=0); return
        zs = np.array([src[r["id"]]["z_s"] for r in sel]); zph = E.arr(sel, "z")
        zl = np.array([src[r["id"]]["z_ref"] if src[r["id"]]["role"] == "deflector" else r["z"] for r in sel])
        lm = E.arr(sel, "lm") + 2.0 * np.log10(E.EUCLID.DL(zl) / E.EUCLID.DL(zph))
        eng, z, RE, Re, n, lm = E.build(sel, z=zl, lm=lm)
        out = dict(N=len(sel), per_lens=[]); bt, bi = {}, {}
        for law in ("S", "B"):
            for nm, a0 in E.FOOT.items():
                bt[(law, nm)] = eng.solve_b(math.pi * RE ** 2 * E.EUCLID.sigcr(z, zs), a0, law)
                bi[(law, nm)] = eng.solve_b(math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF), a0, law)
                st = E.stats(bt[(law, nm)]); si = E.stats(bi[(law, nm)]); out["%s_%s" % (law, nm)] = dict(true=st, inf=si)
                P("  %-9s law %s %-9s N=%2d  b_med(true z_s) = %+.3f [%+.3f, %+.3f]   source-free b_med = %+.3f   n(b > 0.25) = %d%s"
                  % (name, law, nm, len(sel), st["b_med"], st["b_med_lo"], st["b_med_hi"], si["b_med"], int(np.sum(bt[(law, nm)] > 0.25)), note))
        P("  %s per lens (law S): id, grade, model, final, z_l, z_s, theta_E, theta_E/theta_e, n, log M*, b canonical / alt, (source-free b alt)" % name)
        for i in np.argsort(zs):
            r = sel[i]
            P("    %-17s %s %-3s %-3s %.3f %.3f %5.2f\" %5.2f %5.2f %6.2f   %+.3f / %+.3f   (%+.3f)%s" % (r["id"], r["grade"], "yes" if r["success"] else "no",
              "yes" if r["final"] else "no", zl[i], zs[i], r["tE"], r["tE"] / r["te"], r["n"], lm[i], bt[("S", "canonical")][i], bt[("S", "alt")][i],
              bi[("S", "alt")][i], "  [theta_E > 2 arcsec]" if r["tE"] > 2.0 else ""))
            out["per_lens"].append(dict(id=r["id"], grade=r["grade"], model_success=r["success"], final=r["final"], z_l=float(zl[i]), z_s=float(zs[i]),
                                        theta_E=r["tE"], logM=float(lm[i]), n=r["n"], b_S_canonical=float(bt[("S", "canonical")][i]),
                                        b_S_alt=float(bt[("S", "alt")][i]), b_inf_S_alt=float(bi[("S", "alt")][i])))
        READ[name] = out
    usable = [r for r in rows if r["tE"] > 0 and r["te"] > 0 and 0.6 <= r["n"] <= 10.0 and r["z"] > 0 and r["lm"] > 0]
    reading("P", Pm); reading("S", Sm)
    reading("U", usable, "   [not quality-cut]")
    reading("U-model", [r for r in usable if r["success"]], "   [not quality-cut; lens model inspected and successful]")
    reading("U-nomodel", [r for r in usable if not r["success"]], "   [not quality-cut; lens model not successful or not inspected]")
    nP = READ["P"]["N"]
    word = ("EUC1-F under A1 applies (N(P) = %d)" % nP) if nP >= 10 else ("POST HOC READING (A1), NOT A GATE: N(P) = %d < 10; EUC1-F stays open" % nP)
    P("\n[summary]")
    P("  purity gate H2 under A1: %s" % ("PASS" if okH2 else "FAIL -> the amended search is NOT EVALUABLE either"))
    P("  %s" % word)
    P("  kappa = 1/2 FITTED. No outcome favours the framework.  (%.0f s)" % (time.time() - t0))

    # ---------------------------------------------------------------- figures
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        os.makedirs(os.path.join(HERE, "figs_a1"), exist_ok=True)
        items = sorted(src.items(), key=lambda kv: kv[1]["z_s"])
        for pg in range(0, len(items), 8):
            chunk = items[pg:pg + 8]
            fig, ax = plt.subplots(len(chunk), 2, figsize=(11, 2.1 * len(chunk)), squeeze=False)
            for i, (lid, d) in enumerate(chunk):
                p = H.prepare(np.load(os.path.join(sdir, d["sparcl_id"] + ".npz")), use_model=(d["role"] == "deflector"))
                err = np.where(p["iv"] > 0, 1.0 / np.sqrt(np.where(p["iv"] > 0, p["iv"], 1.0)), np.nan)
                zz = d["z_s"]; la, lb = OII_A * (1 + zz), H.OII_B * (1 + zz); s = lb - la; dwl = float(np.median(np.diff(p["wl"])))
                sg = math.sqrt(float(np.interp(la, p["wl"], p["ws"])) ** 2 + (d["sv"] / C_KMS * la) ** 2)
                for j, hw in enumerate((4.0 * s, 70.0)):
                    q = (p["wl"] > la - hw) & (p["wl"] < lb + hw); axx = ax[i, j]
                    axx.step(p["wl"][q], p["r"][q], where="mid", lw=0.8, color="k")
                    axx.fill_between(p["wl"][q], -err[q], err[q], color="0.85", step="mid")
                    for l in (la, lb): axx.axvline(l, color="r", lw=0.6, ls="--")
                    if j == 0 and "Aa" in d:
                        xm = np.linspace(la - hw, lb + hw, 400)
                        axx.plot(xm, d["Aa"] * pixgauss(xm, la, sg, dwl) + d["Ab"] * pixgauss(xm, lb, sg, dwl), color="b", lw=0.8)
                    axx.tick_params(labelsize=6)
                    axx.set_title("%s (%s) z_l=%.3f z_s=%.4f S_OII=%.1f dchi2=%.1f ratio=%.2f" % (lid[-7:], d["grade"], d["z_ref"], zz, d["S_OII"], d["dchi"], d["ratio"]) if j == 0 else "context", fontsize=7)
            fig.tight_layout(); fig.savefig(os.path.join(HERE, "figs_a1", "a1_%02d.png" % (pg // 8)), dpi=70); plt.close(fig)
    except Exception as ex:
        P("  (figures skipped: %s)" % type(ex).__name__)
    json.dump(dict(lane="EUC2", amendment="A1 a24ffd2dc2", n_frozen_D=nfrozenD, n_A1=nreal, n_lenses=len(src), excluded=excl, checks=CK,
                   reading=READ, word=word, H2_pass=bool(okH2)), open(os.path.join(HERE, "euc2_a1_results.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, "euc2_a1.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if okH2 else 3)

if __name__ == "__main__":
    main()
