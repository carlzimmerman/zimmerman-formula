#!/usr/bin/env python3
"""AC1: keep a spatial box of a FITS cube read as a byte stream, all channels, so a cube larger than the free disk can be scored. Bounded memory, one
row at a time; later HDUs (a BEAMS table) pass through unchanged. Prints the sha256 of the bytes read, which is the archive file's. Scores nothing.
    curl -L URL | python3 -I ac1_stream_cutout.py - OUT.fits RA_deg DEC_deg HALF_arcsec
kappa = 1/2 FITTED; one disc excludes no model; not theory closed."""
import hashlib, json, math, os, sys
from astropy.io import fits
from astropy.wcs import WCS
src, out, ra, dec, half = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
f = sys.stdin.buffer if src == "-" else open(src, "rb"); sha = hashlib.sha256(); nread = 0
def rd(n):
    global nread
    b = bytearray()
    while len(b) < n:
        c = f.read(min(n - len(b), 1 << 24))
        if not c: raise SystemExit(f"stream ended early at byte {nread + len(b)}: no complete cube, output is not valid")
        b += c
    sha.update(b); nread += n; return bytes(b)
hb = b""
while True:
    blk = rd(2880); hb += blk
    if any(blk[i:i + 80].startswith(b"END     ") or blk[i:i + 80].rstrip() == b"END" for i in range(0, 2880, 80)): break
H = fits.Header.fromstring(hb.decode("ascii")); assert H["NAXIS"] >= 3 and abs(H["BITPIX"]) in (32, 64) and H.get("SIMPLE")
nx, ny = H["NAXIS1"], H["NAXIS2"]; npl = math.prod(H[f"NAXIS{i}"] for i in range(3, H["NAXIS"] + 1)); bp = abs(H["BITPIX"]) // 8
xc, yc = [float(t) for t in WCS(H).celestial.world_to_pixel_values(ra, dec)]; hp = half / (abs(H["CDELT2"]) * 3600)
x0, x1 = max(0, int(math.floor(xc - hp))), min(nx, int(math.ceil(xc + hp)) + 1); y0, y1 = max(0, int(math.floor(yc - hp))), min(ny, int(math.ceil(yc + hp)) + 1)
assert x1 > x0 and y1 > y0, "target outside the image"
O = H.copy(); O["NAXIS1"], O["NAXIS2"] = x1 - x0, y1 - y0; O["CRPIX1"] = H["CRPIX1"] - x0; O["CRPIX2"] = H["CRPIX2"] - y0
tmp = out + ".partial"
with open(tmp, "wb") as g:
    g.write(O.tostring().encode("ascii")); row = nx * bp; a, b = x0 * bp, x1 * bp; nout = 0
    for _ in range(npl):
        for j in range(ny):
            r = rd(row)
            if y0 <= j < y1: g.write(r[a:b]); nout += b - a
    g.write(b"\0" * (-nout % 2880))
    pad = -(nx * ny * npl * bp) % 2880
    if pad: rd(pad)
    while True:
        c = f.read(1 << 24)
        if not c: break
        sha.update(c); nread += len(c); g.write(c)
os.replace(tmp, out)
R = dict(source_sha256=sha.hexdigest(), source_bytes=nread, source_shape=[nx, ny, npl], box=[x0, x1, y0, y1], half_arcsec=half, cutout_bytes=os.path.getsize(out))
json.dump(R, open(out + ".provenance.json", "w"), indent=1); print(json.dumps(R), flush=True)
