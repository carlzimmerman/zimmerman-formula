#!/usr/bin/env python3
"""EUC16 image-only evidence for choosing the arc finder (run before the criteria were frozen; reads no spectrum).

For every system with a VIS box (sample S, grade X, the truth lens) it runs EUC15's finder (arc_v1) and the candidate
(arc_v2) and reports:
  T  the truth lens's arc (EUC14 / EUC15: (-1.10, -1.11) arcsec);
  A  agreement with catalogued arc candidates (EUC14's definition: MER objects other than the lens object within
     min(theta_E + 0.7, 3.0) arcsec of the catalogue position) on S systems that have one;
  J  synthetic lensed arcs (singular isothermal sphere, Gaussian source, VIS-like PSF) injected into grade-X boxes and
     recovered;
  R  the distribution of arc radius / theta_E on S and on X.
Run:  python3 -I -B euc16_finder_dev.py --data-dir <dir>
"""
import argparse, csv, json, math, os, sys, time
import numpy as np
from scipy.ndimage import gaussian_filter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "closure_2026_11_12", "EUC14_predicted_split_source_redshifts"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "closure_2026_11_12", "EUC9_grism_spectra_source_redshifts"))
import euc9_common as K
import euc14_geom as GM
import euc16_arc as A

SEED = 20261113
OUT = []
def P(s=""):
    print(s); OUT.append(s)

def systems(data_dir):
    B = K.build(data_dir); SYS, obj = B["SYS"], B["obj"]
    tdir = os.path.join(data_dir, "nisp_tables")
    sysrow = {int(r["sid"]): r for r in csv.DictReader(open(os.path.join(tdir, "systems.csv"), newline=""))}
    mer = {}
    for r in K.read_tab(tdir, "mer"): mer.setdefault(sysrow[int(r["sid"])]["unique_identifier"], []).append(r)
    bdir = os.path.join(data_dir, "euc15", "vis_boxes")
    out = {}
    for lid, d in SYS.items():
        if not d.get("target"): continue
        rows = mer.get(lid, []); lo = [r for r in rows if int(r["object_id"]) == d["oid"]]
        bx = os.path.join(bdir, "%d.fits" % d["oid"])
        if not lo or not os.path.exists(bx): continue
        ra0, de0 = float(lo[0]["ra"]), float(lo[0]["dec"])
        ra_s, de_s = float(obj[lid]["RA_obj"]), float(obj[lid]["DEC_obj"])
        r_a = min(d["thE"] + 0.7, 3.0); cat = []
        for r in rows:
            if int(r["object_id"]) == d["oid"]: continue
            o = GM.tan_offset(float(r["ra"]), float(r["dec"]), ra_s, de_s)
            if float(np.hypot(*o)) > r_a: continue
            cat.append(GM.tan_offset(float(r["ra"]), float(r["dec"]), ra0, de0))
        out[lid] = dict(d, ra0=ra0, de0=de0, box=bx, cat=cat)
    return out

def sis_arc(E_, N_, thE, beta, src_sig, psf_sig_pix, flux):
    """surface brightness of a Gaussian source at beta (arcsec, 2-vector) lensed by an SIS of radius thE, on the
    box's offset grid (supersampled 3 x 3), convolved with a Gaussian PSF; total lensed flux = flux"""
    ny, nx = E_.shape; ss = 3
    dE = (E_[0, 1] - E_[0, 0]); dN = (N_[1, 0] - N_[0, 0])
    o = (np.arange(ss) + 0.5) / ss - 0.5
    img = np.zeros((ny, nx))
    for a in o:
        for b in o:
            x = E_ + a * dE; y = N_ + b * dN; r = np.maximum(np.hypot(x, y), 1e-6)
            bx = x - thE * x / r; by = y - thE * y / r
            img += np.exp(-0.5 * ((bx - beta[0]) ** 2 + (by - beta[1]) ** 2) / src_sig ** 2)
    img = gaussian_filter(img, psf_sig_pix)
    if img.sum() <= 0: return img, None
    img *= flux / img.sum()
    # the bright (outer) image: pixels on the source's side of the lens
    bh = beta / max(np.linalg.norm(beta), 1e-9)
    side = (E_ * bh[0] + N_ * bh[1]) > 0
    w = np.where(side, img, 0.0)
    true = np.array([np.sum(E_ * w) / w.sum(), np.sum(N_ * w) / w.sum()])
    return img, true

# candidates compared on image evidence only (FROZEN_CRITERIA.md section 2b): v1 = EUC15; c = recentred; ce = recentred +
# elliptical; ceN / ceM = ce divided by the local scatter of its own annulus (negative residuals / all residuals);
# eN = ceN without recentring; ceF<eps> = ce divided by sqrt(sky^2 + (eps * lens model)^2)
VAR_ALL = {"v1": A.arc_v1,
           "c": lambda i, e, n, t: A.arc_find(i, e, n, t, True, False, None),
           "ce": lambda i, e, n, t: A.arc_find(i, e, n, t, True, True, None),
           "ceN": lambda i, e, n, t: A.arc_find(i, e, n, t, True, True, "neg"),
           "ceM": lambda i, e, n, t: A.arc_find(i, e, n, t, True, True, "mad"),
           "eN": lambda i, e, n, t: A.arc_find(i, e, n, t, False, True, "neg"),
           "ceF02": lambda i, e, n, t: A.arc_find(i, e, n, t, True, True, "model", eps=0.02),
           "ceF03": lambda i, e, n, t: A.arc_find(i, e, n, t, True, True, "model", eps=0.03),
           "ceF05": lambda i, e, n, t: A.arc_find(i, e, n, t, True, True, "model", eps=0.05),
           "ceF10": lambda i, e, n, t: A.arc_find(i, e, n, t, True, True, "model", eps=0.10)}
VAR = VAR_ALL

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); ap.add_argument("--n-inj", type=int, default=400)
    ap.add_argument("--variants", default=",".join(VAR_ALL))
    a = ap.parse_args(); t0 = time.time()
    global VAR; VAR = {v: VAR_ALL[v] for v in a.variants.split(",")}
    tag = "" if a.variants == ",".join(VAR_ALL) else "_" + a.variants.replace(",", "_")
    SY = systems(a.data_dir)
    S = sorted(i for i, d in SY.items() if d["inS"]); X = sorted(i for i, d in SY.items() if d["isX"])
    P("EUC16 finder evidence (image only).  systems with a box: S %d, X %d, truth %s" % (len(S), len(X), K.TRUTH[0] in SY))
    ARC = {}
    for lid in S + X + [K.TRUTH[0]]:
        d = SY[lid]; img, E_, N_ = A.offsets(d["box"], d["ra0"], d["de0"])
        if np.mean(np.isfinite(img) & (img != 0)) < 0.90: continue
        ARC[lid] = {v: f(img, E_, N_, d["thE"]) for v, f in VAR.items()}
    V = list(VAR)
    t = ARC[K.TRUTH[0]]
    P("\n[T] truth lens (theta_E %.2f; EUC15's arc (-1.10, -1.11)): %s" % (SY[K.TRUTH[0]]["thE"], "; ".join("%s (%+.2f, %+.2f)" % (v, *t[v]) for v in V)))
    P("\n[A] S systems with a catalogued arc candidate (EUC14 definition)")
    for tol in (0.3, 0.5):
        n = 0; h = {v: 0 for v in V}
        for lid in S:
            if lid not in ARC or not SY[lid]["cat"]: continue
            n += 1
            for v in V: h[v] += min(float(np.hypot(*(ARC[lid][v] - c))) for c in SY[lid]["cat"]) <= tol
        P("  within %.1f arcsec of a candidate (of %d): %s" % (tol, n, "; ".join("%s %d (%.3f)" % (v, h[v], h[v] / n) for v in V)))
    n = 0; h = {v: 0 for v in V}
    for lid in S:
        if lid not in ARC: continue
        th = SY[lid]["thE"]; cs = [c for c in SY[lid]["cat"] if 0.4 * th <= np.hypot(*c) <= 1.6 * th]
        if not cs: continue
        n += 1
        for v in V:
            az = math.atan2(ARC[lid][v][1], ARC[lid][v][0])
            h[v] += min(abs((math.atan2(c[1], c[0]) - az + math.pi) % (2 * math.pi) - math.pi) for c in cs) <= math.radians(20)
    P("  azimuth within 20 deg of a candidate at 0.4 to 1.6 theta_E (of %d): %s" % (n, "; ".join("%s %d (%.3f)" % (v, h[v], h[v] / max(n, 1)) for v in V)))
    P("\n[R] arc radius / theta_E (percentiles 10, 25, 50, 75, 90)")
    for nm, grp in (("S", S), ("X", X)):
        for v in V:
            rr = [np.hypot(*ARC[i][v]) / SY[i]["thE"] for i in grp if i in ARC]
            P("  %s %-5s N %d: %s;  radius >= 0.67 arcsec %.3f" % (nm, v, len(rr), " ".join("%.2f" % x for x in np.percentile(rr, [10, 25, 50, 75, 90])),
              np.mean([np.hypot(*ARC[i][v]) >= 0.67 for i in grp if i in ARC])))
    rrS = [np.hypot(*c) / SY[i]["thE"] for i in S for c in SY[i]["cat"]]
    P("  catalogued candidates (S): N %d: %s" % (len(rrS), " ".join("%.2f" % x for x in np.percentile(rrS, [10, 25, 50, 75, 90]))))
    rng = np.random.default_rng(SEED)
    Xb = [i for i in X if i in ARC]
    P("\n[J] SIS arcs injected into grade-X boxes (seed %d, %d per S/N): beta / theta_E in [0.1, 0.6], source sigma 0.03 to 0.10 arcsec, PSF sigma 0.7 pix;"
      " k-agree = |found . u / true . u - 1| <= 0.3 for a random direction u with |true . u| >= 0.67 arcsec" % (SEED, a.n_inj))
    for snr in (15.0, 30.0, 60.0):
        res = {v: [] for v in V}; rad = {v: [] for v in V}; kag = {v: [] for v in V}
        for k in range(a.n_inj):
            lid = Xb[int(rng.integers(len(Xb)))]; d = SY[lid]
            img, E_, N_ = A.offsets(d["box"], d["ra0"], d["de0"])
            thE = d["thE"]; bm = float(rng.uniform(0.1, 0.6)) * thE; ph = float(rng.uniform(0, 2 * math.pi))
            beta = np.array([bm * math.cos(ph), bm * math.sin(ph)])
            good = np.isfinite(img) & (img != 0)
            sky = 1.4826 * np.median(np.abs(img[good] - np.median(img[good])))
            ss = float(rng.uniform(0.03, 0.10))
            arc, true = sis_arc(E_, N_, thE, beta, ss, 0.7, 1.0)
            ud = rng.normal(size=2); ud /= np.linalg.norm(ud)
            if true is None: continue
            m = arc > 0.1 * arc.max(); fl = snr * sky * math.sqrt(m.sum()) / arc[m].sum()
            img2 = np.where(good, img + fl * arc, img)
            for v in V:
                g = VAR[v](img2, E_, N_, thE)
                res[v].append(float(np.hypot(*(g - true)))); rad[v].append(float(np.hypot(*g) / np.hypot(*true)))
                if abs(true @ ud) >= 0.67: kag[v].append(abs((g @ ud) / (true @ ud) - 1.0) <= 0.3)
        for v in V:
            r_ = np.array(res[v]); q_ = np.array(rad[v])
            P("  S/N %3.0f %-4s: within 0.3 arcsec %.3f, within 0.5 %.3f; k-agree %.3f (of %d); found / true radius median %.2f [25-75 %% %.2f, %.2f]"
              % (snr, v, np.mean(r_ <= 0.3), np.mean(r_ <= 0.5), np.mean(kag[v]), len(kag[v]), np.median(q_), *np.percentile(q_, [25, 75])))
    json.dump({i: dict({v: list(map(float, ARC[i][v])) for v in V}, ra0=SY[i]["ra0"], de0=SY[i]["de0"], thE=SY[i]["thE"], oid=SY[i]["oid"],
                       S=SY[i]["inS"], X=SY[i]["isX"], Pin=SY[i]["inP"], cat=[list(map(float, c)) for c in SY[i]["cat"]]) for i in ARC},
              open(os.path.join(a.data_dir, "euc16", "finder_dev_arcs%s.json" % tag), "w"))
    P("\n(%.0f s)" % (time.time() - t0))
    open(os.path.join(HERE, "euc16_finder_dev%s.out" % tag), "w").write("\n".join(OUT) + "\n")

if __name__ == "__main__":
    main()
