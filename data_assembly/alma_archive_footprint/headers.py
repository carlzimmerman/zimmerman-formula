#!/usr/bin/env python3
"""Header facts only for the KURVS-15 ALMA Band 6 continuum files (2018.1.00164.S, MOUS uid://A001/X133d/X7ac).  No pixel value is read (fits.getheader only).
Files (downloaded 2026-09-29 with the owner's go, outside the repo): ~/new_physics/_external_data/alma_kurvs15/A001_X133d_X7ac/
"""
import csv, hashlib, math, os
from astropy.io import fits
D = os.path.expanduser("~/new_physics/_external_data/alma_kurvs15/A001_X133d_X7ac/")
HERE = os.path.dirname(os.path.abspath(__file__))
files = ["member.uid___A001_X133d_X7ac.cdfs_31127_sci.spw25_27_29_31.cont.I.pbcor.fits", "member.uid___A001_X133d_X7ac.cdfs_31127_sci.spw25_27_29_31.cont.I.pb.fits.gz"]
listed = {r["file"]: int(r["size_bytes"]) for r in csv.DictReader(open(os.path.join(HERE, "kurvs15_product_file_list.csv")))}
rows = []
for f in files:
    p = D + f
    h = fits.getheader(p)
    open(os.path.join(HERE, "kurvs15_headers", f.replace(".fits.gz", "").replace(".fits", "") + ".header.txt"), "w").write(h.tostring(sep="\n", padding=False) + "\n")
    sha = hashlib.sha256(open(p, "rb").read()).hexdigest()
    ax = {}
    for i in range(1, h["NAXIS"] + 1):
        ax[i] = (h.get(f"CTYPE{i}"), h.get(f"CRVAL{i}"), h.get(f"CDELT{i}"), h.get(f"CRPIX{i}"), h.get(f"NAXIS{i}"), h.get(f"CUNIT{i}"))
    d = dict(file=f, bytes=os.path.getsize(p), listed_bytes=listed[f], sha256=sha, bunit=h.get("BUNIT"), object=h.get("OBJECT"), telescop=h.get("TELESCOP"), date_obs=h.get("DATE-OBS"),
             bmaj_arcsec=(h["BMAJ"] * 3600 if "BMAJ" in h else None), bmin_arcsec=(h["BMIN"] * 3600 if "BMIN" in h else None), bpa_deg=h.get("BPA"),
             restfrq_Hz=h.get("RESTFRQ"), specsys=h.get("SPECSYS"), naxis=h["NAXIS"], shape=" x ".join(str(ax[i][4]) for i in ax),
             pixel_arcsec=abs(ax[1][2]) * 3600 if ax[1][2] else None, axes="; ".join(f"{i}:{v}" for i, v in ax.items()),
             rms_keywords=";".join(f"{k}={h[k]}" for k in h if k.upper() in ("RMS", "NOISE", "SIGMA", "MAPRMS", "DATAMIN", "DATAMAX")) or "none")
    rows.append(d)
    print(d)
with open(os.path.join(HERE, "kurvs15_headers", "band6_continuum_header_facts.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
assert all(r["bytes"] == r["listed_bytes"] for r in rows), "size differs from the archive's listed size"
print("sizes equal the archive-listed sizes")
