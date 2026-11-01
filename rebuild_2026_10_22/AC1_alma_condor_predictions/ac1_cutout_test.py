#!/usr/bin/env python3
"""AC1: does the scorer read the same inputs from a cutout as from the whole cube? MOCK only, NOT ALMA DATA; 2-pixel-scale check, BEAMS table variant, truncated stream, and a broken-offset twin.
    python3 -B ac1_cutout_test.py DIR    exit 1 on any failure
kappa = 1/2 FITTED; not theory closed."""
import hashlib, json, os, subprocess, sys
D = sys.argv[1]; sys.argv = [sys.argv[0]]
import numpy as np
from astropy.io import fits
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "..", "campaign_fresh_gravity", "CFG942_alma_scoring_readiness"))
import cfg942_common as C
RA, DEC, NU, BOX, HALF, VWIN, VCONT = 34.0, -5.2, 98.2, 4.0, 3.4, 500.0, 600.0   # mock geometry; BOX and HALF as ac1_score.py
n, nch, pix = 400, 160, 0.03
def cube(path, beams, ax4):
    rng = np.random.default_rng(5); v = np.arange(nch) * 20.0 - 1590; nu = NU * (1 - v / C.CKMS)
    h = fits.Header(); h["CTYPE1"], h["CTYPE2"], h["CUNIT1"], h["CUNIT2"] = "RA---SIN", "DEC--SIN", "deg", "deg"; h["CRVAL1"], h["CRVAL2"] = RA, DEC; h["CRPIX1"], h["CRPIX2"] = 210.5, 190.5; h["CDELT1"], h["CDELT2"] = -pix / 3600, pix / 3600
    h["CTYPE3"], h["CUNIT3"], h["CRVAL3"], h["CRPIX3"], h["CDELT3"] = "FREQ", "Hz", nu[0] * 1e9, 1.0, (nu[1] - nu[0]) * 1e9; h["RESTFRQ"] = 345.796e9; h["OBJECT"] = "MOCK"; h["BUNIT"] = "Jy/beam"
    d = rng.standard_normal((nch, n, n)).astype(np.float32) * 1e-3; d[70:90, 180:200, 200:220] += 5e-3; d[:, 5, 5] = np.nan
    if not beams: h["BMAJ"], h["BMIN"], h["BPA"] = 0.2 / 3600, 0.15 / 3600, 30.0
    if ax4: d = d[None]; h["CTYPE4"], h["CRVAL4"], h["CRPIX4"], h["CDELT4"] = "STOKES", 1.0, 1.0, 1.0
    hl = [fits.PrimaryHDU(d, h)]
    if beams: hl.append(fits.BinTableHDU.from_columns([fits.Column("BMAJ", "E", array=np.full(nch, .2), unit="arcsec"), fits.Column("BMIN", "E", array=np.full(nch, .15), unit="arcsec"), fits.Column("BPA", "E", array=np.full(nch, 30.), unit="deg"), fits.Column("CHAN", "J", array=np.arange(nch)), fits.Column("POL", "J", array=np.zeros(nch, int))], name="BEAMS"))
    fits.HDUList(hl).writeto(path, overwrite=True)
def inputs(p): return C.stream_mom0(p, RA, DEC, NU, BOX, VWIN, VCONT), C.load_box(p, RA, DEC, NU, HALF, 650.0, VCONT)
def same(p, q):
    a, ab = inputs(p); b, bb = inputs(q); t = 0.0
    t = max(float(np.nanmax(np.abs(a["m0"] - b["m0"]))), float(np.nanmax(np.abs(ab["data"] - bb["data"]))), abs(a["sig_ch"] - b["sig_ch"]))
    return bool(t == 0 and a["m0"].shape == b["m0"].shape and (a["xc"], a["yc"], ab["xc"], ab["yc"]) == (b["xc"], b["yc"], bb["xc"], bb["yc"]) and a["beam"] == b["beam"] and a["nu_cover"] == b["nu_cover"]), t
TOOL = os.path.join(H, "ac1_stream_cutout.py"); ok = []
def cut(p, q, half=4.5): return subprocess.run([sys.executable, "-I", TOOL, "-", q, str(RA), str(DEC), str(half)], stdin=open(p, "rb"), capture_output=True, text=True)
for nm, b, a in (("keywords, 3 axes", False, False), ("BEAMS table, 3 axes", True, False), ("keywords, 4 axes", False, True)):
    p, q = os.path.join(D, "full.fits"), os.path.join(D, "cut.fits"); cube(p, b, a); r = cut(p, q); s, t = same(p, q); sh = json.loads(r.stdout)["source_sha256"] == hashlib.sha256(open(p, "rb").read()).hexdigest()
    ok.append((nm + ": scorer inputs identical, source sha right", s and sh, f"max |d| {t}")); 
p, q = os.path.join(D, "full.fits"), os.path.join(D, "cut.fits"); cube(p, False, True); r = cut(p, q); a = fits.getdata(p); b = fits.getdata(q); hh = fits.getheader(q); x0, x1, y0, y1 = json.loads(r.stdout)["box"]
ok.append(("4 axes: pixels match by slice", bool(np.array_equal(a[..., y0:y1, x0:x1], b, equal_nan=True) and hh["NAXIS4"] == 1), ""))
cube(p, False, False); tr = os.path.join(D, "trunc.fits"); open(tr, "wb").write(open(p, "rb").read()[:5000000]); q2 = os.path.join(D, "cut2.fits"); r = cut(tr, q2)
ok.append(("truncated stream refused, no output", r.returncode != 0 and not os.path.exists(q2), r.stderr.strip()[:60]))
r = cut(p, q); x = fits.open(q, mode="update"); x[0].header["CRPIX1"] += 1; x.close(); s, t = same(p, q); ok.append(("control: off-by-one CRPIX is caught", not s, f"max |d| {t}"))
for k, g, x in ok: print(f"[{'PASS' if g else 'FAIL'}] {k} {x}")
print("MOCK, NOT ALMA DATA. Scores nothing."); sys.exit(0 if all(g for _, g, _ in ok) else 1)
