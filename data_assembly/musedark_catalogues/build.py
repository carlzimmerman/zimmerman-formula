#!/usr/bin/env python3
"""Join the public MUSE-DARK catalogues (the collaboration's UDF data release, 126 galaxies; https://dark-matter.osu-lyon.fr/ , /data/catalogues/*.txt).

Downloaded 2026-09-29 with the owner's go: nine text files, 252,000 bytes in all (sizes from HEAD requests), kept outside the repo in ~/new_physics/_external_data/muse_dark/ with sha256 in manifest.json.
The release supports MUSE-DARK-I (arXiv:2506.19721) and III (arXiv:2604.22613; "Ciocan et al. 2026a, 2026b" on the site).
Files: photometry_catalogue (z, r_kpc, incl, PA, Mstar, SFR), one best-fit file per halo family (DC14, NFW, cNFW, Einasto, Dekel-Zhao, Burkert), baryons_only_bestfit (log_Mdisk, log_Mgas),
Fit_statistics_all_models (chi2, BIC, AIC, log Z per family).  The column meanings below are those of the file headers; no README ships with the files, so units are NOT stated by the source:
every unit or definition not in a header is left as unknown.  No acceleration, a0 or verdict is computed here.
Outputs: musedark_joined.csv (one row per muse_id), checks.txt, manifest.json.
"""
import csv, glob, hashlib, json, math, os, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.expanduser("~/new_physics/_external_data/muse_dark/")
LOG = []
def check(c, m):
    LOG.append(("PASS  " if c else "FAIL  ") + m); print(LOG[-1])
    if not c:
        open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n"); raise SystemExit(m)
def fl(x):
    return float(x) if x not in ("", None) else None
def table(name):
    return list(csv.DictReader(open(EXT + name), delimiter=" "))
manifest = {os.path.basename(f): dict(bytes=os.path.getsize(f), sha256=hashlib.sha256(open(f, "rb").read()).hexdigest()) for f in sorted(glob.glob(EXT + "*.txt"))}
phot = table("photometry_catalogue.txt")
check(len(phot) == 251, f"photometry_catalogue: {len(phot)} rows (the release page says 126 galaxies in the UDF sample; this file is larger)")
ids_phot = [r["muse_id"] for r in phot]
LOG.append(f"photometry_catalogue: {len(set(ids_phot))} distinct muse_id; duplicates {[i for i in set(ids_phot) if ids_phot.count(i) > 1][:5]}"); print(LOG[-1])
fam = {"DC14": "DC14_bestfit.txt", "NFW": "NFW_bestfit.txt", "cNFW": "cNFW_bestfit.txt", "Einasto": "Einastot_bestfit.txt", "DZ": "DZF_bestfit.txt", "Burkert": "Burkert_bestfit.txt"}
halo = {}; dups = {}
for k, f in fam.items():
    rows = table(f)
    ids = [r["muse_id"] for r in rows]
    dup = sorted(set(i for i in ids if ids.count(i) > 1))
    LOG.append(f"{f}: {len(rows)} rows, {len(set(ids))} distinct muse_id, duplicated ids {dup}"); print(LOG[-1])
    halo[k] = {}
    dups[k] = {i: [r for r in rows if r["muse_id"] == i] for i in dup}
    for r in rows:
        if r["muse_id"] not in dup:              # a duplicated id is NOT assigned to either row (the source does not say which is right)
            halo[k][r["muse_id"]] = r
bar = {r["muse_id"]: r for r in table("baryons_only_bestfit.txt")}
stat = {r["muse_id"]: r for r in table("Fit_statistics_all_models.txt")}
sample = sorted(set(halo["NFW"]) | set(halo["DC14"]) | set(dups["DC14"]) | set(bar), key=int)
LOG.append(f"union of the model files: {len(sample)} muse_ids (the release page says 126; the files hold 127 in five halo files; DC14 lacks id 36 and has id 26 twice; baryons-only lacks id 69; Fit_statistics lacks id 36)"); print(LOG[-1])
check(len(sample) == 127, f"127 distinct muse_ids across the model files (got {len(sample)})")
missing = [i for i in sample if i not in set(ids_phot)]
check(not missing, f"every one of the 127 has a photometry row (missing {missing[:5]})")
phot_by = {r["muse_id"]: r for r in phot}
rows = []
for i in sample:
    p = phot_by[i]; b = bar.get(i); s = stat.get(i, {})
    issues = []
    for k in fam:
        if i in dups.get(k, {}): issues.append(f"{k} file has id {i} twice (two different rows), not assigned")
        elif i not in halo[k]: issues.append(f"{k} file lacks id {i}")
    if b is None: issues.append("baryons-only file lacks this id")
    if not s: issues.append("Fit_statistics lacks this id")
    d = dict(muse_id=int(i), z=fl(p["z"]), r_kpc=fl(p["r_kpc"]), incl=fl(p["incl"]), PA=fl(p["PA"]), logMstar_phot=fl(p["Mstar"]), logMstar_phot_err=fl(p["eMstar"]), SFR=fl(p["SFR"]), SFR_err=fl(p["eSFR"]),
             baryons_only_logMdisk=float(b["log_Mdisk"]) if b else None, baryons_only_logMdisk_err=float(b["log_Mdisk_err"]) if b else None,
             baryons_only_logMgas=float(b["log_Mgas"]) if b else None, baryons_only_logMgas_err=float(b["log_Mgas_err"]) if b else None,
             baryons_only_virial_velocity=float(b["virial_velocity"]) if b else None)
    for k in fam:
        h = halo[k].get(i)
        d[f"{k}_logMvir"] = float(h["log_Mvir"]) if h else None
        d[f"{k}_virial_velocity"] = float(h["virial_velocity"]) if h else None
        d[f"{k}_rs_kpc"] = float(h["rs_kpc"]) if h else None
        d[f"{k}_BIC"] = float(s[f"BIC_{ {'DZ': 'Dekel-Zhao'}.get(k, k) if k != 'cNFW' else 'cNFW_fix'}"]) if s and f"BIC_{ {'DZ': 'Dekel-Zhao'}.get(k, k) if k != 'cNFW' else 'cNFW_fix'}" in s else None
    d["baryons_only_BIC"] = float(s["BIC_baryons-only"]) if s and "BIC_baryons-only" in s else None
    d["DC14_logX"] = float(halo["DC14"][i]["log_X"]) if i in halo["DC14"] else None
    d["issues"] = "; ".join(issues)
    rows.append(d)
with open(os.path.join(HERE, "musedark_joined.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
# ---- descriptive checks (no a0)
zs = [r["z"] for r in rows if r["z"] is not None]; LOG.append(f"z range {min(zs):.3f}-{max(zs):.3f}, median {st.median(zs):.3f}"); print(LOG[-1])
lm = [r["logMstar_phot"] for r in rows if r["logMstar_phot"] is not None]; LOG.append(f"photometric log M* {min(lm):.2f}-{max(lm):.2f}, median {st.median(lm):.2f}"); print(LOG[-1])
json.dump({k: {i: v for i, v in dd.items()} for k, dd in dups.items() if dd}, open(os.path.join(HERE, "duplicated_rows.json"), "w"), indent=1)
dm = [r["baryons_only_logMdisk"] - r["logMstar_phot"] for r in rows if r["baryons_only_logMdisk"] is not None and r["logMstar_phot"] is not None]
LOG.append(f"baryons-only fitted log M_disk minus photometric log M*: median {st.median(dm):+.2f} dex, 16-84% {sorted(dm)[int(.16*len(dm))]:+.2f} to {sorted(dm)[int(.84*len(dm))]:+.2f}; |diff| > 0.5 dex for {sum(abs(x) > 0.5 for x in dm)} of {len(dm)}; diff > +1 dex for {sum(x > 1 for x in dm)}"); print(LOG[-1])
gf = [r["baryons_only_logMgas"] - r["logMstar_phot"] for r in rows if r["baryons_only_logMgas"] is not None and r["logMstar_phot"] is not None]
LOG.append(f"baryons-only log M_gas minus photometric log M*: median {st.median(gf):+.2f} (min {min(gf):+.2f}, max {max(gf):+.2f}); constant-HI-surface-density model per the paper, values are the baryons-only fit's"); print(LOG[-1])
open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
json.dump(manifest, open(os.path.join(HERE, "manifest.json"), "w"), indent=1)
