"""LAM3 stage 0 SDSS fetch (criteria d5c434a268, owner approved all stages): SpecObj + galSpecLine + galSpecIndx, and NSA
(nsatlas), inside 1-deg RA strips around SAMI DR3 galaxies with stellar kinematics. Matching is local. Resumable.
Run: python3 -I lam3_fetch.py"""
import os, csv, time, urllib.parse, urllib.request, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "_external_data")
SD = os.path.join(EXT, "lam3_sami_dr3_2026_11_03"); OUTD = os.path.join(EXT, "lam3_sdss_2026_11_03"); os.makedirs(OUTD, exist_ok=True)
URL = "https://skyserver.sdss.org/dr17/SkyServerWS/SearchTools/SqlSearch"
k = {r["CATID"] for r in csv.DictReader(open(os.path.join(SD, "stelkin.csv")))}
P = [(float(r["RA_OBJ"]), float(r["DEC_OBJ"])) for f in ("pos_gama", "pos_clusters", "pos_filler")
     for r in csv.DictReader(open(os.path.join(SD, f + ".csv"))) if r["CATID"] in k]
strips = {}
for ra, de in P: strips.setdefault(int(np.floor(ra)), []).append(de)
SPEC = ("SELECT s.specobjid,s.ra,s.dec,s.z,s.plate,s.mjd,s.fiberID,s.run2d,s.velDisp,s.velDispErr,s.snMedian,l.h_alpha_eqw,"
        "l.sigma_balmer,i.d4000_n,i.lick_mgb,i.lick_fe5270,i.lick_hd_a FROM SpecObj s LEFT JOIN galSpecLine l ON l.specobjid=s.specobjid "
        "LEFT JOIN galSpecIndx i ON i.specobjid=s.specobjid WHERE s.class='GALAXY' AND s.zWarning=0 AND s.z<0.15 AND "
        "s.ra>={a} AND s.ra<{b} AND s.dec>={c} AND s.dec<{d}")
NSA = ("SELECT nsaid,ra,dec,z,sersic_mass,sersic_n,sersic_th50,sersic_absmag_u,sersic_absmag_r FROM nsatlas WHERE "
       "ra>={a} AND ra<{b} AND dec>={c} AND dec<{d}")
def get(q, fn):
    if os.path.exists(fn): return os.path.getsize(fn)
    for t in range(6):
        try:
            b = urllib.request.urlopen(URL + "?" + urllib.parse.urlencode({"cmd": q, "format": "csv"}), timeout=120).read()
            if b.startswith(b"{\"ErrorCode"): raise RuntimeError(b[:200])
            open(fn, "wb").write(b); return len(b)
        except Exception as e: print("retry", os.path.basename(fn), t, e, flush=True); time.sleep(10 * (t + 1))
    raise SystemExit("fetch failed " + fn)
tot = 0
for ra, decs in sorted(strips.items()):
    c, d = np.floor(min(decs) - 0.01), np.ceil(max(decs) + 0.01); arg = dict(a=ra, b=ra + 1, c=c, d=d)
    tot += get(SPEC.format(**arg), os.path.join(OUTD, f"spec_ra{ra:03d}.csv")) + get(NSA.format(**arg), os.path.join(OUTD, f"nsa_ra{ra:03d}.csv"))
print(f"{len(P)} SAMI positions, {len(strips)} strips, {tot} bytes", flush=True)
