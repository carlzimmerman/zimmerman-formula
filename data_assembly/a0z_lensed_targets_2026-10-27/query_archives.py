"""a0(z) lensed-disc target search, step 2: merge duplicate parents by position, then query archive METADATA only (no data products):
MAST (JWST observations whose footprint contains each object: NIRSpec IFU / MSA, NIRCam imaging) and the ALMA archive TAP (observations
whose footprint contains each object; spatial resolution; whether a spectral window covers CO(2-1..5-4) or [CI](1-0)/(2-1) at the object's z).
Every query is logged in query_log.jsonl (endpoint, position, UTC time, rows). Run: python3 -I query_archives.py"""
import csv, json, math, os, time, datetime, warnings, re
warnings.filterwarnings("ignore")
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
HERE = os.path.dirname(os.path.abspath(__file__)); LOG = os.path.join(HERE, "query_log.jsonl")
def log(**k):
    k["utc"] = datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"; open(LOG, "a").write(json.dumps(k) + "\n")

P = list(csv.DictReader(open(os.path.join(HERE, "parents.csv"))))
for p in P:
    for k in ("ra", "dec", "z", "logMstar", "V", "sigma", "vsig"):
        p[k] = float(p[k]) if p[k] not in ("", "None") else None
# merge by position (<= 1.5 arcsec) into unique objects; keep every survey's values
groups = []
for p in P:
    c = SkyCoord(p["ra"] * u.deg, p["dec"] * u.deg)
    for g in groups:
        if c.separation(g["c"]).arcsec <= 1.5: g["rows"].append(p); break
    else:
        groups.append(dict(c=c, rows=[p]))
def gsel(g): return any(r["selected"] == "True" for r in g["rows"])
SEL = [g for g in groups if gsel(g)]
print(f"unique objects {len(groups)}; selected unique {len(SEL)}")

from astroquery.mast import Observations
from pyvo.dal import TAPService
ALMA = TAPService("https://almascience.eso.org/tap")
LINES = {"CO(2-1)": 230.538, "CO(3-2)": 345.796, "CO(4-3)": 461.041, "CO(5-4)": 576.268, "[CI](1-0)": 492.161, "[CI](2-1)": 809.342}
out = []
for g in SEL:
    r0 = sorted(g["rows"], key=lambda r: r["survey"])[0]; z = np.nanmedian([r["z"] for r in g["rows"] if r["z"]])
    names = " / ".join(f"{r['name']} [{r['survey'].split(' ')[0]}]" for r in g["rows"])
    rec = dict(names=names, ra=g["c"].ra.deg, dec=g["c"].dec.deg, z=z,
               surveys=[{k: r[k] for k in ("survey", "logMstar", "V", "sigma", "vsig", "vsig_def", "kin_class", "note")} for r in g["rows"]])
    # MAST
    try:
        t = Observations.query_region(g["c"], radius=2 * u.arcsec); j = t[t["obs_collection"] == "JWST"]
        log(endpoint="MAST Observations.query_region", ra=rec["ra"], dec=rec["dec"], radius_arcsec=2, rows=len(t), jwst=len(j))
        jw = {}
        for row in j:
            inst = str(row["instrument_name"]); key = (inst, str(row["proposal_id"]))
            sep = g["c"].separation(SkyCoord(float(row["s_ra"]) * u.deg, float(row["s_dec"]) * u.deg)).arcsec
            e = jw.setdefault(key, dict(instrument=inst, proposal=str(row["proposal_id"]), filters=set(), texp=0.0, min_sep=1e9, calib=set()))
            e["filters"].add(str(row["filters"])); e["texp"] += float(row["t_exptime"] or 0); e["min_sep"] = min(e["min_sep"], sep); e["calib"].add(str(row["calib_level"]))
        rec["jwst"] = [dict(v, filters=sorted(v["filters"]), calib=sorted(v["calib"])) for v in jw.values()]
    except Exception as ex:
        rec["jwst_error"] = f"{type(ex).__name__}: {str(ex)[:200]}"; log(endpoint="MAST", ra=rec["ra"], dec=rec["dec"], error=rec["jwst_error"])
    # ALMA
    try:
        q = (f"SELECT obs_id, proposal_id, band_list, spatial_resolution, frequency_support, em_min, em_max, t_exptime, obs_release_date, target_name "
             f"FROM ivoa.obscore WHERE INTERSECTS(CIRCLE('ICRS', {rec['ra']}, {rec['dec']}, {2 / 3600}), s_region) = 1")
        res = ALMA.search(q).to_table(); log(endpoint="ALMA TAP ivoa.obscore", ra=rec["ra"], dec=rec["dec"], radius_arcsec=2, rows=len(res))
        al = []
        for row in res:
            fs = str(row["frequency_support"]); spw = [(float(a), float(b)) for a, b in re.findall(r"\[(\d+\.\d+)\.\.(\d+\.\d+)GHz", fs)]
            hits = [n for n, f0 in LINES.items() if any(a <= f0 / (1 + z) <= b for a, b in spw)]
            al.append(dict(obs_id=str(row["obs_id"]), proposal=str(row["proposal_id"]), band=str(row["band_list"]), res_arcsec=float(row["spatial_resolution"]),
                           lines=hits, texp=float(row["t_exptime"]), release=str(row["obs_release_date"])[:10], target=str(row["target_name"])))
        rec["alma"] = al
    except Exception as ex:
        rec["alma_error"] = f"{type(ex).__name__}: {str(ex)[:200]}"; log(endpoint="ALMA TAP", ra=rec["ra"], dec=rec["dec"], error=rec["alma_error"])
    out.append(rec)
    ifu = [e for e in rec.get("jwst", []) if "IFU" in e["instrument"]]; nc = [e for e in rec.get("jwst", []) if "NIRCAM" in e["instrument"].upper()]
    alines = [a for a in rec.get("alma", []) if a["lines"]]
    print(f"{names[:70]:70s} z {z:.2f} | JWST IFU {len(ifu)} NIRCam {len(nc)} other {len(rec.get('jwst', [])) - len(ifu) - len(nc)} | ALMA obs {len(rec.get('alma', []))}, with CO/[CI] line {len(alines)}"
          + (f" (best res {min(a['res_arcsec'] for a in alines):.2f}\")" if alines else "") + (f" ERR {rec.get('jwst_error', '')}{rec.get('alma_error', '')}" if ('jwst_error' in rec or 'alma_error' in rec) else ""))
    time.sleep(0.5)
json.dump(out, open(os.path.join(HERE, "archive_coverage.json"), "w"), indent=1, default=str)
