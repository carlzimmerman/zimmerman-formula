"""CFG235_00_sample.py -- the SAMPLE table only (criteria section 2, 14, 15).  No test statistic, no label.
Prints: frozen-file hash check, the 62-row sample table, counts per source, the CRISTAL ID-mapping conflict, the duplicate
check, the limit-flag reading and the separability index S_i (an input-only quantity).  Exit 0 ok; exit 2 on a sample or
frozen-hash mismatch."""
import os, sys, json, math
sys.dont_write_bytecode = True
import numpy as np
import CFG235_common as C

out = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(C.clean(s), flush=True)
    out.append(C.clean(s))


P("CFG235_00_sample: repo = <repo>; kappa = 1/2 is FITTED; nothing here is a test statistic")
fp = C.frozen_path()
sha = C.sha256_file(fp) if fp else None
P("frozen criteria file:", C.clean(fp) if fp else None, "sha256", sha)
if sha != C.FROZEN_SHA:
    P("EXIT 2: frozen-file hash mismatch (expected", C.FROZEN_SHA + ")")
    sys.exit(2)
P("frozen-file hash matches the committed criteria (commit bfc86d36d)")

rows = C.load_sample()
cnt = {}
for r in rows:
    cnt[r["src"]] = cnt.get(r["src"], 0) + 1
P("\nN per source:", cnt, " total rows", len(rows))
EXPECT = {"D": 41, "C": 14, "R": 4, "A": 2, "P": 1}
if cnt != EXPECT or len(rows) != 62:
    P("EXIT 2: N differs from the frozen section 2.2", EXPECT)
    sys.exit(2)
P("sample counts equal the frozen N (41, 14, 4, 2, 1; 62)")

# ---- CRISTAL ID mapping conflict
P("\nCRISTAL ID mapping (frozen: dynamics id X joined to sample/kinematics row X, else X+'a'):")
sam = {r["id"]: r for r in C.rd("cristal2025_sample.csv")}
kin = {r["id"]: r for r in C.rd("cristal2025_kinematics.csv")}
for r in rows:
    if r["src"] == "C":
        i = r["id"][2:]
        P(f"  {i:>6}  mapped-by-'a'={str(r['mapped']):5}  finite M*={math.isfinite(r['lMstar'])}  z={r['z']}  field={r['field']}"
          f"  dust-detection set={'yes' if r.get('lgas') is not None else 'no'}")
r09 = next(r for r in rows if r["id"] == "C_09")
P("  CONFLICT: the data note says CRISTAL-09 has no SED M* in the sample table; under the frozen mapping 09 -> 09a the"
  f" sample table carries a finite M* (finite: {math.isfinite(r09['lMstar'])}). Not resolved by hand: the frozen mapping is used,"
  " and the 09 row is flagged 'mapping-assumption' in every table.")
P("  rows with NO finite M* (L1/F1 UNDEFINED, counted in m):", [r["id"] for r in rows if r["tier"] == "S" and not math.isfinite(r["lMstar"])])

# ---- limit flags
P("\nLimit-flag reading (table flag columns):")
P("  Danhaive sigma0 '<' (upper limit) rows:", sum(1 for r in rows if r["src"] == "D" and r["sigma_lim"].strip() == "<"),
  "of 41 ; logMstar_lim / logMdyn_lim non-empty:", sum(1 for r in rows if r["src"] == "D" and (r["Mstar_lim"].strip() or r["Mdyn_lim"].strip())))
P("  frozen rule 3.5: M_dyn upper limit -> face value; sigma0 limits already inside the table's M_dyn (no variant changes a label);")
P("  M* upper limit -> not testable; M_dyn lower limit -> not testable for a break. Rows affected by the last two:",
  sum(1 for r in rows if C.limit_untestable(r) and math.isfinite(r["lMstar"])))
P("  ALPAKA ID 28 sigma_ext flag:", next(r for r in rows if r["id"] == "P_28")["sigma_lim"], "(upper limit; face value in V_c^2 = V_ext^2 + 3.36 sigma^2, conservative)")
P("  Roman-Oliveira SGP38326-1/-2: gas error missing in the table -> 0.3 dex stand-in (phase-2 reading, as CFG197)")

# ---- duplicates
P("\nDuplicate check (frozen 2.4: same field AND |dz| <= 0.02 where one lacks coordinates => POSSIBLE duplicate):")


dps = C.dup_pairs(rows)
for p in dps:
    P("  POSSIBLE DUPLICATE (z and field only; Danhaive has no coordinates on disk):", p)
P("  pairs found:", len(dps), "| CRISTAL-08 and -12 are the GOODS-S/ECDFS CRISTAL rows; ALESS (ECDFS by name, from memory, unverified)")
P("  treatment (frozen): both rows kept and scored; counted once in 'unique'; m stays 62")
P("  same-system pairs kept as separate rows: CRISTAL 23b/23c; SGP38326-1/-2")

# ---- table
P("\nSAMPLE TABLE (inputs only):")
P(f"{'id':16} {'src':3} {'tier':4} {'z':>6} {'field':8} {'r_kpc':>7} {'r/re':>4} {'logM*':>6} {'logMdyn,enc':>11} {'logM_b':>7} {'V/sig':>6} {'flags'}")
rng = np.random.default_rng(1)
keep = []
for r in rows:
    nd = C.base_draws(r, 20000, rng)
    lMd, lMb, lr = C.gen(r, nd)
    lMdc = float(np.mean(lMd))
    lMbc = float(np.mean(lMb))
    fl = []
    if r["known"]:
        fl.append(r["known"])
    if r.get("mapped"):
        fl.append("mapping-assumption")
    if r["id"] == "C_09":
        fl.append("table-vs-figure-mismatch")
    if r["id"] == "C_15":
        fl.append("table-vs-figure-mismatch")
    if r["id"] in ("C_23b", "C_23c"):
        fl.append("same-system-pair")
    if r["id"].startswith("R_SGP"):
        fl.append("same-system-pair")
    if r.get("flag_agn"):
        fl.append("SED-AGN-suspect")
    if r["vsig"] < 1:
        fl.append("dispersion-dominated(V/sigma<1)")
    if r["tier"] == "G":
        fl.append("tier-G(gas-only)")
    if r.get("lgas") is not None:
        fl.append("dust-detection(S+G reported)")
    P(f"{r['id']:16} {r['src']:3} {r['tier']:4} {r['z']:6.3f} {r['field']:8} {r['r_kpc']:7.3f} {r['rr']:4.1f} "
      f"{(r['lMstar'] if math.isfinite(r['lMstar']) else float('nan')):6.2f} {lMdc:11.2f} {lMbc:7.2f} {r['vsig']:6.2f} {' '.join(fl)}")
    keep.append(dict(id=r["id"], src=r["src"], tier=r["tier"], z=r["z"], field=r["field"], r_kpc=r["r_kpc"], rr=r["rr"],
                     lMstar=None if not math.isfinite(r["lMstar"]) else r["lMstar"], lMdyn_enc_central=lMdc, lMb_central=lMbc,
                     vsig=r["vsig"], flags=fl))

# ---- separability index (inputs only)
P("\nSEPARABILITY INDEX S_i = log10 nu(x_*) / sigma_tot,primary  (x_* from central inputs, GS geometry, canonical a0, P2 kernel;")
P("sigma_tot,primary = sd of the primary-cell Delta_L1 from 20,000 draws; NO test statistic is printed)")
sep = {}
for r in rows:
    if C.limit_untestable(r):
        P(f"  {r['id']:16} undefined (no finite stellar/baryon floor)")
        continue
    nd = C.base_draws(r, 20000, np.random.default_rng(2))
    dr = C.gen(r, nd)
    m, s = C.cell_stats(r, nd, dr, "GS", "primary")
    lMd, lMb, lr = dr
    cg = C.c_geo("GS", r["rr"], r["tier"])
    xs = cg * C.G_KPC * 10 ** np.mean(lMb) / 10 ** (2 * np.mean(lr)) / C.A0K["canonical"]
    lnu = float(np.log10(C.nu_p2(xs)))
    S = lnu / s
    sep[r["id"]] = dict(x=float(xs), log_nu=lnu, sigma=s, S=S)
    P(f"  {r['id']:16} x_*={xs:9.3g}  log10 nu={lnu:6.3f}  sigma={s:5.3f}  S_i={S:6.2f}  {'(framework-only label reachable: S_i >= 3)' if S >= 3 else '(framework-only NOT reachable)'}")
P("  rows with S_i >= 3:", [k for k, v in sep.items() if v["S"] >= 3])
json.dump(dict(counts=cnt, n=len(rows), frozen_sha=sha, sample=keep, separability=sep, duplicates=[list(p) for p in dps]),
          open(os.path.join(C.HERE, "CFG235_00_sample_results.json"), "w"), indent=1, default=float)
P("\nCFG235_00_sample: exit 0")
sys.exit(0)
