"""DBL1: list extensions, headers and columns of the DESI DR1 P1D QMLE files, and look at column relations.

Usage (from anywhere): python3 -I -B dbl1_file.py
Reads the archive at <repo root>/_external_data/desi_dr1_p1d_qmle/raw/data_points.tar and the copy under
<repo root>/_external_data/desi_dr1_p1d_qmle/ext/. Writes nothing; print to stdout (redirect to dbl1_file.out).
Light compute only.
"""
import io
import os
import tarfile

import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "_external_data", "desi_dr1_p1d_qmle")
TAR = os.path.join(BASE, "raw", "data_points.tar")
EXT = os.path.join(BASE, "ext")
MAIN = "desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits"


def show_hdul(label, hd):
    print("=" * 100)
    print("FILE", label)
    for i, h in enumerate(hd):
        print("-" * 100)
        print("HDU", i, "name", h.name, "type", type(h).__name__, "shape",
              getattr(h.data, "shape", None) if h.data is not None else None)
        for card in h.header.cards:
            print("   ", repr(card.keyword), "=", repr(card.value), "/", card.comment)
        if isinstance(h, fits.BinTableHDU):
            d = h.data
            for c in h.columns:
                v = np.asarray(d[c.name])
                if v.dtype.kind in "fiu":
                    print("    COL %-10s fmt %-6s unit %-10s min % .6e max % .6e mean % .6e" %
                          (c.name, c.format, c.unit, np.nanmin(v), np.nanmax(v), np.nanmean(v)))
                else:
                    print("    COL %-10s fmt %-6s unit %-10s (non-numeric) first %r" % (c.name, c.format, c.unit, v[:3]))


def relations(label, hd):
    print("=" * 100)
    print("COLUMN RELATIONS in", label)
    if "P1D_BLIND" not in [h.name for h in hd]:
        print("  no P1D_BLIND extension")
        return
    d = hd["P1D_BLIND"].data
    names = d.columns.names
    col = {n: np.asarray(d[n], float) for n in names if np.asarray(d[n]).dtype.kind in "fiu"}

    def rel(name, a, b):
        diff = a - b
        scale = np.nanmax(np.abs(a)) if np.nanmax(np.abs(a)) > 0 else 1.0
        print("  %-38s max|diff| %.3e  (max|lhs| %.3e)  rel %.3e" % (name, np.nanmax(np.abs(diff)), scale,
                                                                       np.nanmax(np.abs(diff)) / scale))
    P = col
    if all(k in P for k in ("PLYA", "PFID", "ThetaP")):
        rel("PLYA vs PFID + ThetaP", P["PLYA"], P["PFID"] + P["ThetaP"])
        rel("PLYA vs PINPUT + ThetaP", P["PLYA"], P["PINPUT"] + P["ThetaP"])
        print("  rows with PFID == 0:", int(np.sum(P["PFID"] == 0)))
        if all(k in P for k in ("PRAW", "PNOISE")):
            rel("PFID + ThetaP vs PRAW - PNOISE", P["PFID"] + P["ThetaP"], P["PRAW"] - P["PNOISE"])
            a = P["PFID"] + P["ThetaP"]
            b = P["PRAW"] - P["PNOISE"]
            ok = np.isclose(a, b, rtol=1e-6, atol=1e-6)
            print("  rows where PFID + ThetaP == PRAW - PNOISE (rtol 1e-6): %d of %d" % (ok.sum(), len(a)))
            m = P["PFID"] > 0
            with np.errstate(divide="ignore", invalid="ignore"):
                r = P["PLYA"][m] / a[m]
            print("  PLYA/(PFID + ThetaP) on PFID > 0 rows: median %.5f  1-99%% %.5f %.5f" %
                  (np.median(r), *np.percentile(r, [1, 99])))
    if all(k in P for k in ("PLYA", "PRAW", "PNOISE")):
        rel("PLYA vs PRAW - PNOISE", P["PLYA"], P["PRAW"] - P["PNOISE"])
    if all(k in P for k in ("PLYA", "PSMOOTH")):
        r = P["PLYA"] / P["PSMOOTH"]
        print("  PLYA/PSMOOTH: median %.4f  16-84%% %.4f %.4f" % (np.nanmedian(r), *np.nanpercentile(r, [16, 84])))
    if all(k in P for k in ("PLYA", "PINPUT")):
        r = P["PLYA"] / P["PINPUT"]
        print("  PLYA/PINPUT : median %.4f  16-84%% %.4f %.4f" % (np.nanmedian(r), *np.nanpercentile(r, [16, 84])))
    if all(k in P for k in ("PFID", "PINPUT")):
        rel("PFID vs PINPUT", P["PFID"], P["PINPUT"])
    if all(k in P for k in ("PLYA", "PFID")):
        with np.errstate(divide="ignore", invalid="ignore"):
            r = P["PLYA"] / P["PFID"]
        print("  PLYA/PFID   : median %.4f  16-84%% %.4f %.4f" % (np.nanmedian(r), *np.nanpercentile(r, [16, 84])))
    # per-redshift view of a few rows
    if "Z" in P and "K" in P:
        zs = np.unique(np.round(P["Z"], 3))
        print("  redshift bins:", zs)
        print("  K range per z (first z):", np.nanmin(P["K"][np.isclose(P["Z"], zs[0], atol=1e-3)]),
              np.nanmax(P["K"][np.isclose(P["Z"], zs[0], atol=1e-3)]))
        print("  sample rows (Z, K, PLYA, E_PK if present) at K nearest 0.01, 0.02 s/km:")
        ek = "E_PK" if "E_PK" in P else None
        for z in zs:
            m = np.isclose(P["Z"], z, atol=1e-3)
            for kt in (0.01, 0.02):
                j = np.where(m)[0][np.argmin(np.abs(P["K"][m] - kt))]
                print("    z %.2f k %.5f PLYA %.6e %s  k*PLYA/pi %.6e" %
                      (z, P["K"][j], P["PLYA"][j], ("E %.3e" % P[ek][j]) if ek else "",
                       P["K"][j] * P["PLYA"][j] / np.pi))


def read_fig(t, name):
    b = t.extractfile(name).read()
    if name.startswith("fig_9"):
        cols = ["z", "k", "smooth_ratio", "e_smooth_ratio", "best_fit", "small_dla", "sub_dla"]
        return np.genfromtxt(io.BytesIO(b), skip_header=1, names=cols)
    return np.genfromtxt(io.BytesIO(b), names=True)


def figure_checks(t):
    print("=" * 100)
    print("FIGURE DATA vs TABLE (baseline P1D_BLIND)")
    with fits.open(io.BytesIO(t.extractfile(MAIN).read())) as hd:
        d = hd["P1D_BLIND"].data
        Z, K = np.asarray(d["Z"], float), np.asarray(d["K"], float)
        PL, EP, ES = (np.asarray(d[c], float) for c in ("PLYA", "E_PK", "E_STAT"))
    for name in ("fig_8a_qmle.txt", "fig_8a_fft.txt", "fig_8b_edr.txt", "fig_9_eboss_dr1_dla.txt"):
        f = read_fig(t, name)
        zs = np.unique(np.round(f["z"], 2))
        nmatch = 0
        dev = []
        for i in range(len(f)):
            j = np.where(np.isclose(Z, round(f["z"][i], 2)) & np.isclose(K, f["k"][i], rtol=1e-4))[0]
            if len(j) == 0:
                continue
            nmatch += 1
            if "ratio" in f.dtype.names:
                # fractional error of the figure ratio vs fractional error of the table
                dev.append(f["err"][i] / (1 + f["ratio"][i]) - EP[j[0]] / PL[j[0]])
        dev = np.array(dev)
        print("  %-26s rows %4d  z %s  rows on the table's (z,k) grid %4d" % (name, len(f), zs, nmatch))
        if len(dev):
            print("      max |err/(1+ratio) - E_PK/PLYA| = %.3e" % np.max(np.abs(dev)))
    f = read_fig(t, "fig_9_eboss_dr1_dla.txt")
    print("  fig_9 smooth_ratio range per z:")
    for z in np.unique(np.round(f["z"], 2)):
        m = np.isclose(f["z"], z)
        print("      z %.1f k %.6f..%.6f smooth_ratio %.4f..%.4f" % (z, f["k"][m].min(), f["k"][m].max(),
                                                                   f["smooth_ratio"][m].min(), f["smooth_ratio"][m].max()))
    f = read_fig(t, "fig_6b_e_jackknife.txt")
    m = np.isclose(Z, 2.4)
    r = []
    for i in range(len(f)):
        j = np.where(m & np.isclose(K, f["k"][i], rtol=1e-4))[0]
        if len(j):
            r.append(f["e_qmle"][i] / ES[j[0]])
    r = np.array(r)
    print("  fig_6b e_qmle / E_STAT at z 2.4: median %.4f min %.4f max %.4f (n %d)" % (np.median(r), r.min(), r.max(), len(r)))
    m = t.getmember("fig_10a_bF.txt")
    head = t.extractfile(m).read(600)
    print("  fig_10a_bF.txt: %d bytes; first bytes look like a tar header: %r" % (m.size, head[:40]))


def main():
    t = tarfile.open(TAR)
    members = t.getmembers()
    print("ARCHIVE", os.path.relpath(TAR, ROOT), "members", len(members))
    for m in members:
        print("  %-70s %12d bytes" % (m.name, m.size))
    fits_members = [m for m in members if m.name.endswith(".fits")]
    for m in fits_members:
        raw = t.extractfile(m).read()
        with fits.open(io.BytesIO(raw)) as hd:
            show_hdul("tar:" + m.name, hd)
            relations("tar:" + m.name, hd)
    # copies under ext/
    for fn in sorted(os.listdir(EXT)):
        p = os.path.join(EXT, fn)
        with fits.open(p) as hd:
            show_hdul("ext:" + fn, hd)
        # byte identity with the tar member of the same name
        try:
            raw = t.extractfile(fn).read()
            with open(p, "rb") as f:
                same = f.read() == raw
            print("BYTE-IDENTICAL to tar member", fn, ":", same)
        except KeyError:
            print("no tar member named", fn)
    figure_checks(t)
    # figure text files: heads
    print("=" * 100)
    print("FIGURE TEXT FILES (first 12 lines of each named in the brief, first 4 of the rest)")
    named = {"fig_8a_qmle.txt", "fig_8a_fft.txt", "fig_8b_edr.txt", "fig_9_eboss_dr1_dla.txt"}
    for m in members:
        if not m.name.endswith(".txt"):
            continue
        f = t.extractfile(m)
        n = 12 if m.name in named else 4
        print("-" * 100)
        print(m.name)
        for _ in range(n):
            line = f.readline()
            if not line:
                break
            print("   ", line.decode("utf-8", "replace").rstrip()[:200])


if __name__ == "__main__":
    main()
