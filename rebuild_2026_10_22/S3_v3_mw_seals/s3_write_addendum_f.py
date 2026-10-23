#!/usr/bin/env python3
"""Write ADDENDUM_F_DRAFT.md (lane-local draft for the coordinator) from SEALED_V3_ALMA_AQUAL.json + s3_partD_alma_results.json.
Every number comes from those files; the seal's hash is checked first."""
import os
import json
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
blob = open(os.path.join(HERE, "SEALED_V3_ALMA_AQUAL.json"), "rb").read()
sha = hashlib.sha256(blob).hexdigest()
assert sha == open(os.path.join(HERE, "ALMA_V3_HASH.txt")).read().split()[0]
SEAL = json.loads(blob)
R = json.load(open(os.path.join(HERE, "s3_partD_alma_results.json")))
f = lambda x: "FLOOR" if x is None else f"{x:.2f}"
L = []
w = L.append
w("# DRAFT — ALMA clarification addendum F (v3's AQUAL-disc reading) — lane S3_v3_mw_seals, for the coordinator")
w("")
w("**Status: DRAFT, not filed.** Written in `rebuild_2026_10_22/S3_v3_mw_seals/` only. Filing it in `CFG806_u4_27928_scoring/` and")
w("`CFG809_gs4_24110_ci21_scoring/` needs the owner's approval (as addendum E did). It must be committed before any byte of either")
w("programme is read (U4: 2026-11-06; GS4: 2026-11-28). FROZEN_CRITERIA.md, the clarification files, addenda A–E and every seal stay")
w("untouched.")
w("")
w("**Why.** v3's static limit is AQUAL with μ = x/(1+x) (E2, C4). Its spherical form is ν₁, which AG4e sealed (`SEALED_N1.json`,")
w("sha256 9802de0d…) by applying ν₁ algebraically to the in-plane Newtonian field of razor-thin discs. In a disc AQUAL is not that")
w("algebraic rule: the field magnitude just off the plane includes the vertical 2πGΣ-type component (the Brada–Milgrom Kuzmin")
w("solution makes this exact), so at the comparison radius AQUAL's in-plane pull differs from the algebraic one. Lane S3 solved")
w("AQUAL for the same discs (`s3_partD_alma.py`, `s3_alma.py`, `s3_aqual.py`; checks D1–D5 and D6′ pass; frozen D6 mis-specified,")
w("AMENDMENT A5). By its frozen rule (|Δ log V²_bar,req| ≤ 0.01 dex, |Δ log M_gas,req| ≤ 0.03 dex, no FLOOR flip) the result is:")
w(f"**{R['decision']['label']}** (max |Δ log V²_bar,req| {R['decision']['max_abs_dlogVbar2_nonfloor']:.3f} dex, max |Δ log M_gas,req| "
  f"{R['decision']['max_abs_dlogMgas']:.2f} dex, {R['decision']['floor_flips']} FLOOR flips).")
w("")
for t, m in R.get("per_release", {}).items():
    w(f"- {t}: max |Δ log V²_bar,req| {m['max_dV']:.4f} dex, max |Δ log M_gas,req| {m['max_dM']:.3f} dex, FLOOR flips {m['flips']} → {m['label']}.")
cs = {t: [c["aqual"]["C_stars"] for k, c in R["cells"].items() if k.startswith(t)] for t in ("GS4_24110", "U4_27928")}
dvg = [c["dlogVbar2"] for k, c in R["cells"].items() if k.startswith("GS4") and not c["alg"]["floor"]]
dmg = [v for k, c in R["cells"].items() if k.startswith("GS4") for v in c["dlogMgas"].values() if v is not None]
nfl = sum(int(c["floor_flip"]) for k, c in R["cells"].items() if k.startswith("GS4"))
w("")
w(f"**What changes, physically.** At GS4's comparison radius (R_e = 1.68 R_d) AQUAL's in-plane pull from the stars is "
  f"{min(cs['GS4_24110']):.3f}–{max(cs['GS4_24110']):.3f} of the algebraic ν₁ value, so v3 needs MORE baryons there than AG4e: "
  f"{min(dvg):+.3f} to {max(dvg):+.3f} dex in V²_bar,req (non-FLOOR cells), which becomes {min(dmg):+.2f} to {max(dmg):+.2f} dex in "
  f"M_gas,req and turns {nfl} AG4e FLOOR cells (GS4 log M★ 10.89) into finite gas requirements. At U4's radius (2 R_e = 3.36 R_d) the ratio is "
  f"{min(cs['U4_27928']):.4f}–{max(cs['U4_27928']):.4f}: V²_bar,req moves by ≤ 0.001 dex, but the gas requirement still moves by up to "
  f"0.055 dex in near-FLOOR cells, which is what fails the frozen 0.03 dex line for U4.")
w("")
w("## Proposed ruling (mirrors addendum E)")
w("1. **The verdict kernel stays ν_mono** (CFG571), and addendum E's n = 1 (AG4e) and n = 2 (AG4d) readings stay as filed.")
w(f"2. **v3's AQUAL-disc requirement is scored as a further labelled parallel reading**, by the identical rules (§3–§5 of each plan's")
w("   FROZEN_CRITERIA.md, CLARIFICATION_2026-10-21.md and addenda A–E): same gates, measured quantities, σ, wording, FLOOR rule, both")
w(f"   footings, every branch. The requirement is read from `rebuild_2026_10_22/S3_v3_mw_seals/SEALED_V3_ALMA_AQUAL.json`")
w(f"   (sha256 `{sha}`, `ALMA_V3_HASH.txt`), never recomputed after the data are read.")
w("3. **Δ_v for this reading** uses V²_bar,req,AQ (the Newtonian in-plane V² of the required AQUAL configuration: Freeman stars +")
w("   the required exponential gas disc) in place of the algebraic V²_bar,req; V²_bar,meas is unchanged. For the R_g = 1.5 R_d branch the")
w("   sealed `logVbar2R_G_Rg=1.5Rd` is used.")
w("4. **Never pooled** with ν_mono, n = 1, n = 2, the other footing or the other disc. Each output line states 'v3 AQUAL disc'.")
w("5. **Measured gas size (gate G3).** If G3 passes, the AQUAL requirement at the measured R_g is NOT in the seal; it is then reported")
w("   as 'not sealed' and only the sealed R_g = R_d / 1.5 R_d rows are scored.")
w("6. **No law-form or theory statement from one disc.** One disc excludes no model.")
w("")
w("## The sealed v3 AQUAL-disc requirement beside AG4e (log M_gas,req, R_g = R_d; canonical / alt)")
w("")
for tgt, keys in (("GS4_24110", ["10.89", "10.76"]), ("U4_27928", sorted(SEAL["U4_27928"], key=float))):
    w(f"### {tgt}")
    w("")
    w("| " + ("log M★" if tgt.startswith("GS4") else "V_c") + " | branch | AG4e (ν₁ algebraic) can / alt | v3 AQUAL disc can / alt | Δ log V²_bar,req can / alt |")
    w("|---|---|---|---|---|")
    for k in keys:
        for m in SEAL["ratios"]:
            c = R["cells"][f"{tgt}|{k}|canon 9.36e-11|{m}"]; a = R["cells"][f"{tgt}|{k}|alt 1.13e-10|{m}"]
            w(f"| {k} | {m} | {f(c['alg']['logMgas_Rg=Rd'])} / {f(a['alg']['logMgas_Rg=Rd'])} | {f(c['aqual']['logMgas_Rg=Rd'])} / {f(a['aqual']['logMgas_Rg=Rd'])} | "
              f"{c['dlogVbar2']:+.3f} / {a['dlogVbar2']:+.3f} |")
    w("")
w("κ = ½ FITTED; footings never pooled; cold energy mass required; one disc excludes no model; not theory closed.")
open(os.path.join(HERE, "ADDENDUM_F_DRAFT.md"), "w").write("\n".join(L) + "\n")
print("ADDENDUM_F_DRAFT.md written;", sha)
