#!/usr/bin/env python3
"""List which HEALPix (nside 64, nested) pixels have DESI DR1 MWS per-pixel RV files (rv_output/240520/healpix/<survey>/<program>/<hpx//100>/<hpx>/) by reading the public DIRECTORY INDEXES only (no data files).
Writes desi_mws_pixels_by_survey_program.json (small). Apache index pages are read with 12 threads."""
import re, json, urllib.request, concurrent.futures as cf, time
B = "https://data.desi.lbl.gov/public/dr1/vac/dr1/mws/iron/v1.0/rv_output/240520/healpix/"
def ls(u, tries=4):
    for k in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("utf8", "ignore")
        except Exception as e: time.sleep(1 + k)
    return ""
def subdirs(u): return re.findall(r'href="([0-9A-Za-z_\-]+)/"', ls(u))
out = {}; n_req = 0
for sv in subdirs(B):
    for pg in subdirs(B + sv + "/"):
        tops = subdirs(f"{B}{sv}/{pg}/")
        with cf.ThreadPoolExecutor(12) as ex:
            res = list(ex.map(lambda t: (t, subdirs(f"{B}{sv}/{pg}/{t}/")), tops))
        pix = sorted(int(p) for t, ps in res for p in ps if p.isdigit()); out[f"{sv}/{pg}"] = pix; n_req += 1 + len(tops)
        print(sv, pg, "top dirs", len(tops), "pixels", len(pix), flush=True)
json.dump(out, open("desi_mws_pixels_by_survey_program.json", "w"))
print("index requests about", n_req)
