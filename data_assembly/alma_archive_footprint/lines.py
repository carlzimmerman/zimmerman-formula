#!/usr/bin/env python3
"""Which archival ALMA observations at each KURVS position have a spectral window covering a redshifted CO/[CI] line at the galaxy's H-alpha redshift?

Input: alma_footprint_rows.csv (ALMA archive ivoa.obscore rows whose s_region contains the KURVS position; see query.py).
frequency_support is the archive's own string '[f1..f2GHz, channel width, S mJy/beam@10km/s, S uJy/beam@native, pols] U [...]'.
Line rest frequencies (GHz): CO(2-1) 230.538, CO(3-2) 345.796, CO(4-3) 461.041, [CI](1-0) 492.161, [CI](2-1) 809.342.  Observed = rest/(1+z_Halpha).
The sensitivity is the archive's ESTIMATE for that spectral window at the pointing (not a measured map rms, not corrected for the primary beam at the position).
No line flux, no gas mass, no verdict.
"""
import csv, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
LINES = {"CO(2-1)": 230.538, "CO(3-2)": 345.796, "CO(4-3)": 461.041, "[CI](1-0)": 492.161, "[CI](2-1)": 809.342}
z = {r["kurvs_id"]: float(r["z_halpha"]) for r in csv.DictReader(open(os.path.join(HERE, "..", "arxiv_tables", "kurvs_positions", "kurvs_positions.csv")))}
rows = list(csv.DictReader(open(os.path.join(HERE, "alma_footprint_rows.csv"))))
pat = re.compile(r"\[([\d.]+)\.\.([\d.]+)GHz,([\d.]+)kHz,([\d.]+)(mJy|uJy|Jy)/beam@10km/s")
scale = {"Jy": 1e3, "mJy": 1.0, "uJy": 1e-3}
LOGL = []
# control: parser check on the first row
first = pat.findall(rows[0]["frequency_support"])
assert first and float(first[0][0]) < float(first[0][1]), "frequency_support parser failed"
out = {}
for r in rows:
    zz = z[r["kurvs_id"]]
    wins = [(float(a), float(b), float(c), float(d) * scale[u]) for a, b, c, d, u in pat.findall(r["frequency_support"])]
    for name, nu0 in LINES.items():
        nu = nu0 / (1 + zz)
        hit = [w for w in wins if w[0] <= nu <= w[1]]
        if hit:
            key = (r["kurvs_id"], r["proposal_id"], name)
            a = out.setdefault(key, dict(kurvs_id=r["kurvs_id"], proposal_id=r["proposal_id"], line=name, z_halpha=zz, nu_obs_GHz=round(nu, 3), n_rows=0,
                                          best_sens_mJy_per_beam_at_10kms=None, best_res_arcsec=None, band=set(), pi=r["pi_name"], title=r["obs_title"]))
            a["n_rows"] += 1; a["band"].add(r["band_list"])
            s = min(w[3] for w in hit)
            a["best_sens_mJy_per_beam_at_10kms"] = s if a["best_sens_mJy_per_beam_at_10kms"] is None else min(a["best_sens_mJy_per_beam_at_10kms"], s)
            try:
                res = float(r["s_resolution"]); a["best_res_arcsec"] = res if a["best_res_arcsec"] is None else min(a["best_res_arcsec"], res)
            except ValueError: pass
res = sorted(out.values(), key=lambda a: (int(a["kurvs_id"]), a["line"], a["proposal_id"]))
for a in res: a["band"] = ";".join(sorted(a["band"])); a["best_sens_mJy_per_beam_at_10kms"] = round(a["best_sens_mJy_per_beam_at_10kms"], 3)
with open(os.path.join(HERE, "alma_line_coverage.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(res[0].keys())); w.writeheader(); w.writerows(res)
print(len(res), "(kurvs, proposal, line) combinations with a spectral window on the line")
for kid in sorted({a["kurvs_id"] for a in res}, key=int):
    print("KURVS-" + kid, "; ".join(sorted({f"{a['line']} {a['proposal_id']}" for a in res if a['kurvs_id'] == kid})))
