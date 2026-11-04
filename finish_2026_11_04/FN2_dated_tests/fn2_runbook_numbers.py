#!/usr/bin/env python3
"""FN2 A4: every derived number in RELEASE_DAY_RUNBOOK.md, from the committed archive listing (fn2_archive_meta.json) and the record's
measured transfer rate (CFG569 FETCH_LOG: 12-17 MB/s bulk). Image shapes are inferred from file sizes (a FITS file = header blocks +
NAXIS1*NAXIS2*NCHAN*4 bytes padded to 2880); the stream's header gives the truth on the day. Reads only; writes this lane's outputs.
    python3 -B fn2_runbook_numbers.py
kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); M = json.load(open(os.path.join(HERE, "fn2_archive_meta.json")))
OUT = []; R = {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
def size(files, suffix): return [f for f in files if f["name"].endswith(suffix)][0]["content_length"]
A, B = M["A3"]["nested_files"], M["B2"]["units"][0]["nested_files"]
def shape(cube, mfs, hdr_blocks_max=40):
    """Square plane n x n from the single-plane mfs size, then NCHAN from the cube size; both must be exact for some header size."""
    for hb in range(1, hdr_blocks_max):
        d = mfs - hb * 2880; n = int(round(math.sqrt(d / 4)))
        if n * n * 4 == d or (math.ceil(n * n * 4 / 2880) * 2880 == d):
            for hc in range(1, hdr_blocks_max):
                c = cube - hc * 2880; nch = c / (n * n * 4)
                if abs(nch - round(nch)) < 1e-9: return dict(n=n, nchan=int(round(nch)), mfs_header_blocks=hb, cube_header_blocks=hc)
    return None
RATE = (12e6, 17e6)
for tag, files, pre, half, plane in (("U4_28473 rows B, spw25", A, "UDS28473_sci.spw25", 4.5, None), ("U4_27928 row A, spw23", A, "UDS28473_sci.spw23", 13.0, None),
                                     ("GS4_24110 [CI](2-1), spw31", B, "Pointing-F_sci.spw31", None, None)):
    cb, mb = size(files, f"{pre}.cube.I.pbcor.fits"), size(files, f"{pre}.mfs.I.pbcor.fits"); sh = shape(cb, mb)
    r = dict(cube_bytes=cb, mfs_bytes=mb, inferred=sh, transfer_minutes=[round(cb / RATE[1] / 60), round(cb / RATE[0] / 60)])
    if half and sh:
        cut = {}
        for pix in (0.013, 0.0225):
            hp = half / pix; w = int(math.ceil(hp)) + 1 + int(math.ceil(hp))   # ac1_stream_cutout: floor(xc-hp) .. ceil(xc+hp)+1
            cut[str(pix)] = dict(width_px=w, bytes=w * w * sh["nchan"] * 4, GB=round(w * w * sh["nchan"] * 4 / 1e9, 2))
        r["cutout_half_arcsec"] = half; r["cutout"] = cut
    R[tag] = r; P(f"{tag}: cube {cb:,} B, mfs {mb:,} B -> inferred {sh}; transfer at 17-12 MB/s {r['transfer_minutes'][0]}-{r['transfer_minutes'][1]} min"
                  + (f"; cutout +-{half}\": " + ", ".join(f"pix {k}\" -> {v['width_px']} px, {v['GB']} GB" for k, v in r["cutout"].items()) if half and sh else ""))
P("coverage (from fn2_archive_meta.json, information): " + json.dumps(M["A3"]["window_coverage_information"]))
P("GS4 coverage (information): " + json.dumps(M["B2"]["units"][0]["window_coverage_information"]))
json.dump(R, open(os.path.join(HERE, "fn2_runbook_numbers.json"), "w"), indent=1)
open(os.path.join(HERE, "fn2_runbook_numbers.out"), "w").write("\n".join(OUT) + "\n")
