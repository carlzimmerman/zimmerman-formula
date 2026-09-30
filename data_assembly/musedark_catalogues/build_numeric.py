#!/usr/bin/env python3
"""Parse the per-galaxy numeric files of the MUSE-DARK UDF release (galpak_run_DC14/: true_Vrot.dat, galaxy_parameters, derived_parameters, run_parameters, model).

Fetched 2026-09-29 with the owner's go (882 small files, 7 per galaxy, 126 galaxies; all HTTP 200; ~1.3 MB) into ~/new_physics/_external_data/muse_dark/numeric/ID<nnnn>/DC14_<n>_<file> (outside the repo; fetch_log.txt there).
Joined with `musedark_joined.csv` (photometric M*).  No README ships with the files: column meanings are the file headers'; every definition not printed in a file is marked unverified.
No acceleration, a0 or verdict is computed.  Outputs: musedark_numeric.csv (one row per galaxy), checks_numeric.txt.
"""
import csv, glob, math, os, re, statistics as st
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.expanduser("~/new_physics/_external_data/muse_dark/numeric/")
LOG = []
def check(c, m):
    LOG.append(("PASS  " if c else "FAIL  ") + m); print(LOG[-1])
    if not c:
        open(os.path.join(HERE, "checks_numeric.txt"), "w").write("\n".join(LOG) + "\n"); raise SystemExit(m)
ids = sorted(os.path.basename(d)[2:] for d in glob.glob(EXT + "ID*"))
check(len(ids) == 126, f"126 galaxy folders (got {len(ids)})")
FILES = ["true_Vrot.dat", "galaxy_parameters.txt", "galaxy_parameters.dat", "derived_parameters.txt", "derived_parameters.dat", "run_parameters.txt", "model.txt"]
miss = [(i, f) for i in ids for f in FILES if not os.path.exists(f"{EXT}ID{i}/DC14_{int(i)}_{f}") or os.path.getsize(f"{EXT}ID{i}/DC14_{int(i)}_{f}") == 0]
check(not miss, f"all 7 files present and non-empty for every galaxy ({len(miss)} missing)")
tot = sum(os.path.getsize(p) for p in glob.glob(EXT + "ID*/DC14_*"))
LOG.append(f"total bytes of the 882 files: {tot}"); print(LOG[-1])
def fnum(x):
    try: return float(x)
    except (TypeError, ValueError): return float("nan")
def kv_txt(path):
    out = {}
    for l in open(path):
        m = re.match(r"\s*([A-Za-z0-9_]+): *([^\s±(]+)(?: *± *([^\s(]+))?", l)
        if m:
            out[m.group(1)] = (fnum(m.group(2)), fnum(m.group(3)))
            ci = re.search(r"CI 95%: \[\s*([^\s,]+),\s*([^\s\]]+)\]", l)
            if ci: out[m.group(1) + "_ci"] = (fnum(ci.group(1)), fnum(ci.group(2)))
    return out
def model_kv(path):
    d = {}
    for l in open(path):
        m = re.match(r"\s*([A-Za-z_]+) = (.*?)\s*$", l)
        if m: d[m.group(1)] = m.group(2)
    return d
phot = {r["muse_id"]: r for r in csv.DictReader(open(os.path.join(HERE, "musedark_joined.csv")))}
rows = []; issues = []
for i in ids:
    n = int(i); p = lambda f: f"{EXT}ID{i}/DC14_{n}_{f}"
    g = kv_txt(p("galaxy_parameters.txt")); d = kv_txt(p("derived_parameters.txt")); m = model_kv(p("model.txt"))
    rows_v = [[c.strip() for c in l.strip().strip("|").split("|")] for l in open(p("true_Vrot.dat")) if l.strip()]
    hdr = rows_v[0]; A = np.array([[float(c) for c in r] for r in rows_v[1:]])
    if hdr != ["dx_arcsec", "rad_Re", "flux_slit", "v_kms", "sig_kms"]: issues.append((i, "true_Vrot header", hdr))
    ph = phot.get(str(n), {})
    kpc = float(m["kpc"]); Re_kpc = d.get("rad_kpc", (None, None))[0]
    # check: dx_arcsec / rad_Re = R_e in arcsec; R_e * kpc_per_arcsec should be rad_kpc
    ratio = np.abs(A[:, 0][np.abs(A[:, 1]) > 0.2]) / np.abs(A[:, 1][np.abs(A[:, 1]) > 0.2])
    Re_arcsec = float(np.median(ratio))
    pos = A[A[:, 1] > 0]; neg = A[A[:, 1] < 0]
    row = dict(muse_id=n, z=float(m["redshift"]), kpc_per_arcsec=kpc, pixscale_arcsec=float(m["pixscale"].split()[0]),
               adrift=m.get("adrift"), rotation_curve=m.get("rotation_curve"), dispersion_profile=m.get("dispersion_profile"), thickness_profile=m.get("thickness_profile"), aspect=float(m.get("aspect", "nan")),
               logMstar_phot=ph.get("logMstar_phot"), DC14_logMdisk=d["log_Mdisk"][0], DC14_logMdisk_err=d["log_Mdisk"][1],
               DC14_log_X=g["log_X"][0], DC14_logMvir=d["log_Mvir"][0], logMdyn=d["log_Mdyn"][0], logMbulge=d["log_Mbulge"][0] if "log_Mbulge" in d else None, fDM_at_Re=d["fDM_at_Re"][0], v22=d["v22"][0], Re_kpc=Re_kpc,
               gas_density_Msun_pc2=g["gas_density"][0], gas_density_lo95=g["gas_density_ci"][0], gas_density_hi95=g["gas_density_ci"][1],
               incl_deg=g["inclination"][0], sersic_n=g["sersic_n"][0], sigma_fit_kms=g["velocity_dispersion"][0], Vvir=g["virial_velocity"][0], has_bulge=int("BT_ratio" in g), BT_ratio=g["BT_ratio"][0] if "BT_ratio" in g else None,
               n_slit_rows=len(A), Re_arcsec_from_table=round(Re_arcsec, 4), maxR_over_Re_pos=float(pos[:, 1].max()) if len(pos) else None, maxR_over_Re_neg=float(-neg[:, 1].min()) if len(neg) else None,
               v_at_maxR_pos=float(pos[np.argmax(pos[:, 1]), 3]) if len(pos) else None, v_at_maxR_neg=float(neg[np.argmin(neg[:, 1]), 3]) if len(neg) else None,
               sig_min=float(A[:, 4].min()), sig_max=float(A[:, 4].max()), sig_at_centre=float(A[np.argmin(np.abs(A[:, 1])), 4]), sig_at_maxR_pos=float(pos[np.argmax(pos[:, 1]), 4]) if len(pos) else None)
    row["Re_kpc_from_table"] = round(Re_arcsec * kpc, 3)
    row["log_X_plus_logMvir"] = round(g["log_X"][0] + d["log_Mvir"][0], 3)
    rows.append(row)
check(not issues, f"every true_Vrot.dat has the header dx_arcsec|rad_Re|flux_slit|v_kms|sig_kms ({issues[:2]})")
bad = [(r["muse_id"], r["Re_kpc"], r["Re_kpc_from_table"]) for r in rows if r["Re_kpc"] and abs(r["Re_kpc"] / r["Re_kpc_from_table"] - 1) > 0.02]
check(not bad, f"rad_kpc (derived_parameters) = dx_arcsec/rad_Re x kpc-per-arcsec within 2% for every galaxy, i.e. rad_kpc is R_e in kpc and rad_Re is R/R_e (exceptions {bad[:4]})")
def mtot(r):
    return r["DC14_logMdisk"] if r["logMbulge"] is None else math.log10(10 ** r["DC14_logMdisk"] + 10 ** r["logMbulge"])
diffs = [mtot(r) - r["log_X_plus_logMvir"] for r in rows]
LOG.append(f"log(M_disk + M_bulge) minus (log_X + log_Mvir), all from the files' posterior medians: median {st.median(diffs):+.3f} dex, 90th percentile of |diff| {sorted(abs(x) for x in diffs)[int(.9*len(diffs))]:.2f}, max |diff| {max(abs(x) for x in diffs):.2f}; so the total stellar mass is close to, not exactly, X times the halo virial mass (medians of separate posteriors; my reading, unverified)"); print(LOG[-1])
fields = list(rows[0].keys())
with open(os.path.join(HERE, "musedark_numeric.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(rows)
# ---- descriptive statistics
dm = [r["DC14_logMdisk"] - float(r["logMstar_phot"]) for r in rows if r["logMstar_phot"] not in (None, "")]
srt = sorted(dm)
LOG.append(f"DC14-fit log_Mdisk minus photometric log M*: n={len(dm)}, median {st.median(dm):+.2f} dex, 16-84% {srt[int(.16*len(srt))]:+.2f} to {srt[int(.84*len(srt))]:+.2f}, |diff|>0.3 dex for {sum(abs(x)>0.3 for x in dm)}, |diff|>0.5 for {sum(abs(x)>0.5 for x in dm)}, min {min(dm):+.2f}, max {max(dm):+.2f}"); print(LOG[-1])
e = [r["DC14_logMdisk_err"] for r in rows]; LOG.append(f"quoted log_Mdisk 1-sigma error: median {st.median(e):.2f} dex, max {max(e):.2f}"); print(LOG[-1])
gd = [r["gas_density_Msun_pc2"] for r in rows]; hi = [r["gas_density_hi95"] for r in rows]
LOG.append(f"gas_density (fit parameter; prior box 0 to 15 Msun/pc^2 from run_parameters, the max_boundaries line of ID3, assumed the same for all): median {st.median(gd):.1f}; upper 95% limit >= 14 for {sum(h >= 14 for h in hi)} of 126; lower 95% limit < 1 for {sum(r['gas_density_lo95'] < 1 for r in rows)}"); print(LOG[-1])
mp = [r["maxR_over_Re_pos"] for r in rows if r["maxR_over_Re_pos"]]; mn = [r["maxR_over_Re_neg"] for r in rows if r["maxR_over_Re_neg"]]
LOG.append(f"true_Vrot coverage max R/R_e: positive side median {st.median(mp):.2f} (min {min(mp):.2f}, max {max(mp):.2f}); negative side median {st.median(mn):.2f}; rows per file median {st.median([r['n_slit_rows'] for r in rows])}"); print(LOG[-1])
LOG.append("model strings: " + str(sorted(set((r['adrift'], r['rotation_curve'], r['dispersion_profile'], r['thickness_profile'], r['aspect']) for r in rows)))); print(LOG[-1])
sc = [r["sig_at_maxR_pos"] / r["sig_at_centre"] for r in rows if r["sig_at_maxR_pos"]]
LOG.append(f"model sigma at the outermost positive-side row over sigma at the centre: median {st.median(sc):.2f} (min {min(sc):.2f}, max {max(sc):.2f})"); print(LOG[-1])
open(os.path.join(HERE, "checks_numeric.txt"), "w").write("\n".join(LOG) + "\n")
