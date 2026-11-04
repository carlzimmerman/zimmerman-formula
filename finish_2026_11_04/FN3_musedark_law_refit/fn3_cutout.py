"""FN3 Stage 1 cutout extraction through any byte-range reader (criteria s3, s9). No network here.

read_layout(reader): parse the primary, DATA and STAT headers of a MUSE DR2 cube from byte ranges only.
read_box(reader, layout, x0, y0, j0, nb, nl): a (nl, nb, nb) box of DATA and STAT, one range per plane (full rows).
continuum_subtract(data, var, centre, half): per-spaxel linear continuum from channels outside +-half of the line.
SELFTEST: writes a synthetic cube with the same layout to the scratch path given, reads a box through a file reader,
and compares with astropy's own slicing. kappa = 1/2 FITTED; not theory closed.
"""
import os
import sys

import numpy as np

BLOCK = 2880


def _header_at(reader, off, chunk=2880 * 16):
    from astropy.io import fits
    buf = b""
    while True:
        buf += reader(off + len(buf), chunk)
        for k in range(0, len(buf) - 79, 80):
            if buf[k:k + 8] == b"END     ":
                end = k + 80
                hlen = (end + BLOCK - 1) // BLOCK * BLOCK
                return fits.Header.fromstring(buf[:end].decode("ascii", "replace")), hlen
        if len(buf) > 2880 * 400:
            raise RuntimeError("no END card")


def _datalen(h):
    if h.get("NAXIS", 0) == 0:
        return 0
    n = abs(int(h["BITPIX"])) // 8
    for i in range(1, int(h["NAXIS"]) + 1):
        n *= int(h[f"NAXIS{i}"])
    return (n + BLOCK - 1) // BLOCK * BLOCK


def read_layout(reader):
    h0, l0 = _header_at(reader, 0)
    off = l0 + _datalen(h0)
    ext = {}
    for _ in range(4):
        try:
            h, l = _header_at(reader, off)
        except Exception:
            break
        name = str(h.get("EXTNAME", "")).strip().upper()
        ext[name] = dict(header=h, data_off=off + l)
        off = off + l + _datalen(h)
        if "DATA" in ext and "STAT" in ext:
            break
    return dict(primary=h0, ext=ext)


def read_box(reader, layout, x0, y0, j0, nb, nl):
    out = {}
    for name in ("DATA", "STAT"):
        e = layout["ext"][name]
        h = e["header"]
        nx, ny, nz = int(h["NAXIS1"]), int(h["NAXIS2"]), int(h["NAXIS3"])
        if not (0 <= x0 and x0 + nb <= nx and 0 <= y0 and y0 + nb <= ny and 0 <= j0 and j0 + nl <= nz):
            raise ValueError("box outside the cube")
        bpp = abs(int(h["BITPIX"])) // 8
        dt = np.dtype(">f4") if int(h["BITPIX"]) == -32 else np.dtype(">f8")
        box = np.empty((nl, nb, nb), np.float32)
        for k in range(nl):
            j = j0 + k
            a = e["data_off"] + ((j * ny + y0) * nx) * bpp
            raw = reader(a, nb * nx * bpp)
            rows = np.frombuffer(raw, dtype=dt).reshape(nb, nx)
            box[k] = rows[:, x0:x0 + nb]
        out[name] = box
    return out


def continuum_subtract(data, var, centre, half):
    nl = data.shape[0]
    j = np.arange(nl)
    m = np.abs(j - centre) > half
    out = np.empty_like(data, dtype=np.float64)
    for iy in range(data.shape[1]):
        for ix in range(data.shape[2]):
            y = data[:, iy, ix].astype(float)
            w = m & np.isfinite(y) & np.isfinite(var[:, iy, ix]) & (var[:, iy, ix] > 0)
            if w.sum() < 10:
                out[:, iy, ix] = np.nan
                continue
            for _ in range(3):
                p = np.polyfit(j[w], y[w], 1)
                r = y - np.polyval(p, j)
                s = np.nanstd(r[w])
                w = w & (np.abs(r) < 3 * s)
            out[:, iy, ix] = y - np.polyval(p, j)
    return out


def file_reader(path):
    def rd(off, n):
        with open(path, "rb") as f:
            f.seek(off)
            return f.read(n)
    return rd


def selftest(scratch):
    from astropy.io import fits
    rng = np.random.default_rng(7)
    nx, ny, nz = 97, 83, 211
    d = rng.normal(size=(nz, ny, nx)).astype(np.float32)
    v = rng.uniform(0.5, 2.0, size=(nz, ny, nx)).astype(np.float32)
    ph = fits.PrimaryHDU()
    ph.header["OBJECT"] = "FN3 selftest"
    hd = fits.ImageHDU(d, name="DATA")
    hs = fits.ImageHDU(v, name="STAT")
    for k in range(300):
        hd.header[f"HIERARCH FN3 PAD{k}"] = k          # long headers, like the DR2 cubes
    p = os.path.join(scratch, "fn3_selftest_cube.fits")
    fits.HDUList([ph, hd, hs]).writeto(p, overwrite=True)
    rd = file_reader(p)
    lay = read_layout(rd)
    ok = True
    for (x0, y0, j0) in ((0, 0, 0), (40, 30, 100), (72, 58, 130)):
        box = read_box(rd, lay, x0, y0, j0, 25, 81)
        ok &= np.array_equal(box["DATA"], d[j0:j0 + 81, y0:y0 + 25, x0:x0 + 25])
        ok &= np.array_equal(box["STAT"], v[j0:j0 + 81, y0:y0 + 25, x0:x0 + 25])
    # continuum: a known slope plus a line is recovered
    j = np.arange(81)
    cube = (5 + 0.1 * j)[:, None, None] * np.ones((81, 3, 3)) + (10 * np.exp(-0.5 * ((j - 40) / 1.5) ** 2))[:, None, None]
    cs = continuum_subtract(cube, np.ones_like(cube), 40, 12)
    ok2 = float(np.max(np.abs(cs[:, 1, 1] - 10 * np.exp(-0.5 * ((j - 40) / 1.5) ** 2)))) < 1e-6
    os.remove(p)
    lines = [f"cutout selftest: boxes byte-identical to astropy slicing -> {'PASS' if ok else 'FAIL'}",
             f"continuum selftest: line recovered to 1e-6 -> {'PASS' if ok2 else 'FAIL'}",
             "kappa = 1/2 FITTED; not theory closed."]
    print("\n".join(lines))
    return ok and ok2, lines


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "SELFTEST":
        good, lines = selftest(sys.argv[2])
        open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fn3_cutout_selftest.out"), "w").write("\n".join(lines) + "\n")
        sys.exit(0 if good else 1)
