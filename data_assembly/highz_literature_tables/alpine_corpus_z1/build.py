#!/usr/bin/env python3
"""Flatten the High-z Kinematic Corpus Z1 (arXiv:2605.25339, Zenodo 10.5281/zenodo.21834678 'corrected' record; zip downloaded by my user in a browser because Zenodo blocked automated fetches; copy in
~/new_physics/_external_data/alpine_corpus_z1/) into CSVs and CHECK its per-ring values against the Jones+2021 Table A3 that was parsed independently from the arXiv HTML.
The corpus is a SECONDARY compilation of ALPINE [CII] kinematics (Jones+21 tilted-ring fits; stellar masses and SFR from Faisst+20).  The zip also holds `omega_results_z1.csv` and a figure: derived quantities of the corpus author's own
'omega' construction (not data); they are NOT used here."""
import json, csv, os, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); Z = os.path.expanduser("~/new_physics/_external_data/alpine_corpus_z1"); d = json.load(open(os.path.join(Z, "corpus", "high_z_kinematic_corpus_Z1.json")))
gal = []; rings = []
for g in d["galaxies"]:
    gal.append({k: v for k, v in g.items() if not isinstance(v, (dict, list))} | {k: v for k, v in g["w15_criteria"].items()} | {"n_known_issues": len(g.get("known_issues", []))})
    for r in g.get("data", []): rings.append({"galaxy": g["galaxy"], "z": g["redshift"], **r})
def w(fn, rows):
    keys = []
    for r in rows:
        for k in r:
            if k not in keys: keys.append(k)
    csv.DictWriter(open(os.path.join(HERE, fn), "w", newline=""), fieldnames=keys).writeheader() if False else None
    with open(os.path.join(HERE, fn), "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=keys); wr.writeheader(); wr.writerows(rows)
w("corpus_z1_galaxies.csv", gal); w("corpus_z1_rings.csv", rings)
LOG = [f"corpus: {len(gal)} galaxies, {len(rings)} ring rows, tier 1: {sum(1 for g in gal if g['quality_tier']==1)}, classes {d['metadata']['class_counts']}"]
J = list(csv.DictReader(open(os.path.join(HERE, "..", "jones2021_alpine", "jones2021_tableA3_rings.csv"))))
jm = {(r["name"], round(float(r["R_kpc"]), 2)): r for r in J}; ok = 0; bad = []
for r in rings:
    key = (r["galaxy"], round(r["R_kpc"], 2)); j = jm.get(key)
    if j is None: bad.append(("no Jones ring", key)); continue
    if abs(float(j["vrot_kms"]) - r["Vrot_kms"]) < 0.02 and abs(float(j["sigma_kms"]) - r["sigma_kms"]) < 0.02: ok += 1
    else: bad.append(("value", key, j["vrot_kms"], r["Vrot_kms"]))
LOG.append(f"corpus rings matched to Jones+21 Table A3 (R, v_rot, sigma equal to 0.02): {ok} of {len(rings)}; mismatches/extra: {bad}")
LOG.append(f"Jones A3 ring rows not in the corpus: {[k for k in jm if k not in {(r['galaxy'], round(r['R_kpc'], 2)) for r in rings}]}")
print("\n".join(LOG)); open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
json.dump({"zip_sha256": hashlib.sha256(open(os.path.join(Z, "21834678.zip"), "rb").read()).hexdigest(), "zip_bytes": os.path.getsize(os.path.join(Z, "21834678.zip")), "source": "Zenodo record 21834678 (downloaded by the user in a browser, 2026-09-30)"}, open(os.path.join(HERE, "manifest.json"), "w"), indent=1)
