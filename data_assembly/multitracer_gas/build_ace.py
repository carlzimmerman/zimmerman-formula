#!/usr/bin/env python3
"""Parse the per-galaxy tables of the ACE (ALMA Chemical Evolution) papers from their arXiv HTML (fetched 2026-09-30, sha256 in manifest_ace.json):
  arXiv:2609.21604 (overview: fluxes S_CO(3-2), Band 7 and Band 6 fluxes; sample properties), arXiv:2609.21072 (molecular gas: S_CO, M_mol from CO, M_mol/M*, t_dep),
  arXiv:2609.20926 (dust-to-gas: L_nu873, L'_CO(3-2), M_dust, M_mol, 12+log(O/H)), arXiv:2609.21040 (dust content: nu_obs, S_nu, M_dust).
Conversions stated: CO(3-2) -> CO(1-0) with r31 = 0.77 +- 0.14 (Boogaard+2020) and a metallicity-dependent alpha_CO (the ACE calibration of Shivaei+2026 as adopted in 2609.21072); dust: single-band Band 7,
optically thin, beta = 2.08, kappa = 0.4 m2/kg at 250 micron (2609.20926 Eq. 1).  Nothing is recomputed; limits are kept as flags."""
import sys, os, re, csv, json, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "highz_literature_tables"))
from tabutil import *
RAW = os.path.join(HERE, "raw_small"); LOG = []
def log(m): LOG.append(m); print(m)
def page(i): return open(os.path.join(RAW, f"arxiv_{i}_html_fetched_2026-09-30.html"), errors="ignore").read()
def numid(x):
    m = re.search(r"(\d{3,6})", x); return m.group(1) if m else x.strip()
def table(s, tid, names, start=2):
    out = []
    for r in rows(s, tid)[start:]:
        if len(r) < len(names) or not re.search(r"\d", r[0]): continue
        d = {"id": numid(r[0]), "id_raw": r[0]}
        for k, nm in enumerate(names, start=1):
            if k >= len(r): break
            v, lo, hi, fl = val(r[k]); d[nm] = v; d[nm + "_errlo"] = lo; d[nm + "_errhi"] = hi
            if fl: d[nm + "_flag"] = fl
        out.append(d)
    return out
gas = table(page("2609.21072"), "A1.T2.5", ["z", "Mstar_1e10", "SFR", "OH", "SCO32dv_Jykms", "Mmol_CO_1e10", "Mmol_over_Mstar", "tdep_Gyr"])
dgr = table(page("2609.20926"), "A1.T3.2", ["V2ID", "z", "logLnu873", "logLpCO32", "logMdust", "logMmol", "OH"])
dust = table(page("2609.21040"), "A1.T2.5", ["ra", "dec", "z", "Mstar_1e9", "SFR", "OH", "nu_obs_GHz", "S_nu", "Mdust_1e7"])
fl = table(page("2609.21604"), "S1.T1.5.1", ["v4id", "prog", "SCO32_mJykms", "eSCO32", "B7_mJy", "eB7", "B6_mJy", "eB6"])
log(f"ACE tables: gas {len(gas)}, dgr {len(dgr)}, dust {len(dust)}, fluxes {len(fl)}")
for nm, t in (("ace_gas_2609.21072", gas), ("ace_dgr_2609.20926", dgr), ("ace_dust_2609.21040", dust), ("ace_fluxes_2609.21604", fl)): write(os.path.join(HERE, nm + ".csv"), t)
G = {d["id"]: d for d in gas}; D = {d["id"]: d for d in dgr}; U = {d["id"]: d for d in dust}
ids = sorted(set(G) | set(D) | set(U)); M = []
for i in ids:
    g, d, u = G.get(i, {}), D.get(i, {}), U.get(i, {}); z = g.get("z") or d.get("z") or u.get("z")
    M.append(dict(id=i, z=z, OH=g.get("OH") or d.get("OH") or u.get("OH"), Mstar_1e10=g.get("Mstar_1e10"), Mmol_CO_1e10=g.get("Mmol_CO_1e10"), Mmol_CO_flag=g.get("Mmol_CO_1e10_flag"), logMmol_2609_20926=d.get("logMmol"), logMdust_2609_20926=d.get("logMdust"), logMdust_flag=d.get("logMdust_flag"),
                  Mdust_1e7_2609_21040=u.get("Mdust_1e7"), Mdust_flag_2609_21040=u.get("Mdust_1e7_flag"), logLpCO32=d.get("logLpCO32"), logLnu873=d.get("logLnu873"), SCO32dv_Jykms=g.get("SCO32dv_Jykms")))
write(os.path.join(HERE, "ace_merged_per_galaxy.csv"), M)
co_det = [m for m in M if m["Mmol_CO_1e10"] is not None and not m["Mmol_CO_flag"]]; du_det = [m for m in M if (m["Mdust_1e7_2609_21040"] is not None and not m["Mdust_flag_2609_21040"]) or (m["logMdust_2609_20926"] is not None and not m["logMdust_flag"])]
both = [m for m in co_det if m in du_det]
log(f"ACE merged {len(M)} galaxies; CO detections {len(co_det)}; dust detections {len(du_det)}; both {len(both)}; z range {min(m['z'] for m in M if m['z']):.3f}-{max(m['z'] for m in M if m['z']):.3f}")
open(os.path.join(HERE, "checks_ace.txt"), "w").write("\n".join(LOG) + "\n")
json.dump({f: hashlib.sha256(open(os.path.join(RAW, f), "rb").read()).hexdigest() for f in sorted(os.listdir(RAW)) if "26" in f and f.split("_")[1].startswith("2609")}, open(os.path.join(HERE, "manifest_ace.json"), "w"), indent=1)
