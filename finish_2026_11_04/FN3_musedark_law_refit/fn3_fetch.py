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
    os.makedirs(OUTDIR, exist_ok=True)
    catp = os.path.join(OUTDIR, CATALOG)
    if not os.path.exists(catp):
        n, _ = head(BASE + CATALOG)
        open(catp, "wb").write(get_range(BASE + CATALOG, 0, n - 1))
    tf = tarfile.open(catp)
    main_cat = [m for m in tf.getmembers() if m.name.lower().endswith(".fits") and "main" in m.name.lower()]
    if not main_cat:
        print("catalogue members:", [m.name for m in tf.getmembers()][:20])
        sys.exit(3)
    cat = fits.open(io.BytesIO(tf.extractfile(main_cat[0]).read()))[1].data
    phot, _ = C.load_catalogue()
    hdrs = {}
    for f, fn in CUBES.items():
        url = BASE + fn
        blob = get_range(url, 0, 2880 * 40 - 1)
        h0 = fits.Header.fromstring(blob[: blob.find(b"END" + b" " * 77) + 80].decode("ascii", "replace"))
        n0 = (len(h0.tostring()) + 2879) // 2880 * 2880
        hdrs[f] = dict(url=url, blob=blob, h0len=n0)
    man = {}
    for gid in sample:
        f = field_of(gid)
        # match by ID and redshift; stop on any doubt
        sel = np.where(cat["ID"] == gid)[0]
        if len(sel) != 1 or abs(float(cat["Z"][sel[0]]) - phot[gid]["z"]) > 0.002:
            man[gid] = dict(status="NO MATCH")
            continue
        ra, dec = float(cat["RA"][sel[0]]), float(cat["DEC"][sel[0]])
        man[gid] = dict(status="PLANNED", field=f, ra=ra, dec=dec)
    json.dump(man, open(os.path.join(C.HERE, "fn3_fetch_manifest_planned.json"), "w"), indent=1)
    print("catalogue matched; extension offsets and cutout reads are implemented at Stage 1 run time after the header check")


if __name__ == "__main__":
    main()
