"""FN3 Stage 1 fetcher: byte-range cutouts from the public MUSE HUDF DR2 cubes (criteria s3, s9).

  python3 fn3_fetch.py --dry-run     HEAD requests only: file sizes and the transfer plan. No data.
  python3 fn3_fetch.py --approved    only after the owner's yes: fetches the DR2 catalogue tarball (9.1 MB), reads
                                     each cube's FITS headers with range requests, then for each primary/secondary
                                     galaxy reads 81 planes x (DATA, STAT) x 25 full rows and keeps a 25 x 25 x 81 box.

Never downloads a full cube. Cutouts and the catalogue go to ../_external_data/fn3_musedark_cutouts/ beside the repo,
with a sha256 manifest committed in this folder. kappa = 1/2 FITTED; not theory closed.
"""
import hashlib
import io
import json
import math
import os
import sys
import tarfile
import time
import urllib.request

import numpy as np

import fn3_common as C

BASE = "https://amused.univ-lyon1.fr/data/UDF/HUDF/download/"
CUBES = {"UDF10": "DATACUBE_UDF-10.fits", "MXDF": "DATACUBE_MXDF.fits", "MOSAIC": "DATACUBE_UDF-MOSAIC.fits"}
CATALOG = "UDF_HUDF_Catalogs_FULL.tar.gz"
OUTDIR = os.path.abspath(os.path.join(C.REPO, "..", "_external_data", "fn3_musedark_cutouts"))
NCH = 3681          # MUSE DR2 spectral axis, 4750-9350 A at 1.25 A
BOX, NPL = 25, 81
F_L1, F_L2 = 3726.2, 3728.9          # the survey's [OII] lines, as fn3_cube


def head(url):
    req = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(req, timeout=60) as r:
        return int(r.headers["Content-Length"]), r.headers.get("Accept-Ranges", "")


def get_range(url, a, b, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"Range": f"bytes={a}-{b}"})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            if len(data) == b - a + 1:
                return data
        except Exception:
            time.sleep(2 * (k + 1))
    raise RuntimeError(f"range {a}-{b} failed for {url}")


def field_of(gid):
    run = open(os.path.join(C.NUMERIC, f"ID{gid:04d}", f"DC14_{gid}_run_parameters.txt")).read()
    for f in CUBES:
        if f"/{f}_" in run:
            return f
    raise ValueError(gid)


def plan(sample):
    rows = []
    for gid in sample:
        rows.append((gid, field_of(gid)))
    sizes = {}
    for f, fn in CUBES.items():
        n, ar = head(BASE + fn)
        nxy = n / (2 * 4 * NCH)
        side = math.sqrt(nxy)
        sizes[f] = dict(bytes=n, accept_ranges=ar, approx_pixels_per_plane=nxy, approx_naxis1=side)
    nc, _ = head(BASE + CATALOG)
    per_full_rows = {f: NPL * 2 * BOX * sizes[f]["approx_naxis1"] * 4 for f in CUBES}
    per_kept = NPL * 2 * BOX * BOX * 4
    tot_transfer = sum(per_full_rows[f] for _, f in rows) + nc
    return rows, sizes, nc, per_full_rows, per_kept, tot_transfer


def main():
    s = json.load(open(os.path.join(C.HERE, "fn3_sample.json")))
    sample = sorted(set(s["primary"]) | set(s["secondary"]))
    if "--dry-run" in sys.argv:
        rows, sizes, nc, pfr, pk, tot = plan(sample)
        from collections import Counter
        cnt = Counter(f for _, f in rows)
        lines = ["FN3 fetch plan (dry run: HEAD requests only, no data)"]
        for f, d in sizes.items():
            lines.append(f"  {CUBES[f]}: {d['bytes']:,} bytes, Accept-Ranges {d['accept_ranges']!r}, "
                         f"~{d['approx_naxis1']:.0f} px per row (from size / (2 x 4 B x {NCH} channels)); "
                         f"{cnt.get(f, 0)} galaxies; ~{pfr[f] / 1e6:.1f} MB read per galaxy (full rows)")
        lines.append(f"  {CATALOG}: {nc:,} bytes")
        lines.append(f"  galaxies: {len(rows)} (primary + secondary); kept per galaxy {pk / 1e6:.3f} MB; kept in all {len(rows) * pk / 1e6:.1f} MB")
        lines.append(f"  total transferred (full-row reads + catalogue): ~{tot / 1e9:.2f} GB; full cubes never stored")
        lines.append("kappa = 1/2 FITTED; not theory closed.")
        print("\n".join(lines))
        open(os.path.join(C.HERE, "fn3_fetch_plan.out"), "w").write("\n".join(lines) + "\n")
        return
    if "--approved" not in sys.argv:
        print("refusing: pass --dry-run, or --approved after the owner's yes")
        sys.exit(2)
    from astropy.io import fits
    from astropy.wcs import WCS
    from fn3_cutout import read_box, read_layout
    os.makedirs(OUTDIR, exist_ok=True)
    catp = os.path.join(OUTDIR, CATALOG)
    if not os.path.exists(catp):
        n, _ = head(BASE + CATALOG)
        open(catp, "wb").write(get_range(BASE + CATALOG, 0, n - 1))
    tf = tarfile.open(catp)
    members = [m for m in tf.getmembers() if m.name.lower().endswith(".fits")]
    cats = []
    for m in members:
        try:
            t = fits.open(io.BytesIO(tf.extractfile(m).read()))[1].data
            cols = {c.upper(): c for c in t.columns.names}
            if all(k in cols for k in ("ID", "RA", "DEC")) and any(k in cols for k in ("Z", "Z_MUSE", "REDSHIFT")):
                cats.append((m.name, t, cols))
        except Exception:
            continue
    if not cats:
        print("no catalogue with ID, RA, DEC and Z among", [m.name for m in members][:20])
        sys.exit(3)
    name, cat, cols = cats[0]
    zc = next(cols[k] for k in ("Z", "Z_MUSE", "REDSHIFT") if k in cols)
    phot, _ = C.load_catalogue()
    layouts = {}
    readers = {}
    for f, fn in CUBES.items():
        url = BASE + fn
        readers[f] = (lambda u: (lambda off, n: get_range(u, off, off + n - 1)))(url)
        layouts[f] = read_layout(readers[f])
    man = {}
    for gid in sample:
        f = field_of(gid)
        sel = np.where(np.asarray(cat[cols["ID"]]) == gid)[0]
        zs = [float(cat[zc][i]) for i in sel]
        good = [i for i, zz in zip(sel, zs) if abs(zz - phot[gid]["z"]) <= 0.002]
        if len(good) != 1:
            man[gid] = dict(status="NO MATCH", field=f, candidates=len(sel))
            continue
        i = good[0]
        ra, dec = float(cat[cols["RA"]][i]), float(cat[cols["DEC"]][i])
        h = layouts[f]["ext"]["DATA"]["header"]
        w = WCS(h).celestial
        x, y = w.world_to_pixel_values(ra, dec)
        cd3 = float(h.get("CD3_3", h.get("CDELT3")))
        jc = ((F_L1 + F_L2) / 2 * (1 + phot[gid]["z"]) - float(h["CRVAL3"])) / cd3 + float(h["CRPIX3"]) - 1
        x0, y0, j0 = int(round(float(x))) - BOX // 2, int(round(float(y))) - BOX // 2, int(round(jc)) - NPL // 2
        try:
            box = read_box(readers[f], layouts[f], x0, y0, j0, BOX, NPL)
        except Exception as e:
            man[gid] = dict(status=f"READ FAILED: {e}", field=f)
            continue
        lam0 = float(h["CRVAL3"]) + (j0 + 1 - float(h["CRPIX3"])) * cd3
        g = C.load_galaxy(gid)
        out = os.path.join(OUTDIR, f"ID{gid:04d}.npz")
        np.savez(out, DATA=box["DATA"], STAT=box["STAT"], lam0=lam0, dlam=cd3,
                 psf_fwhm=g["psf"]["fwhm"], psf_beta=g["psf"]["beta"], x0=x0, y0=y0, j0=j0, field=f, ra=ra, dec=dec)
        man[gid] = dict(status="OK", field=f, ra=ra, dec=dec, x0=x0, y0=y0, j0=j0, sha256=hashlib.sha256(open(out, "rb").read()).hexdigest())
        print(f"ID{gid} {f} OK", flush=True)
    json.dump(dict(catalogue=name, cutouts=man), open(os.path.join(C.HERE, "fn3_cutouts_manifest.json"), "w"), indent=1)
    print("cutouts:", sum(1 for v in man.values() if v["status"] == "OK"), "of", len(man))

if __name__ == "__main__":
    main()
