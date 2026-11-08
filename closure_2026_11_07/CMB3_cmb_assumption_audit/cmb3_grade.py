#!/usr/bin/env python3
"""CMB3 grader (FROZEN_CRITERIA.md, origin e46081b7a9): assembles parts/*.json into cmb3.json / cmb3.out and
cmb3_MUTATE.json / cmb3_MUTATE.out. kappa = 1/2 FITTED; not theory closed."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, "parts"); F1A = os.path.join(HERE, "../F1A_primary_cmb_audit/parts")
NOTE = "kappa = 1/2 FITTED; not theory closed"
J = lambda n, d=P: json.load(open(os.path.join(d, n)))
FEET = ("canonical", "alt")

def label(dmb, S, dR):
    if dmb <= 25 or (dR is not None and abs(dR) > 0.25): return "BREAKS"
    if S < 0.5 or (dR is not None and abs(dR) > 0.10): return "BENDS"
    return "HOLDS"

out = dict(criteria="e46081b7a9", note=NOTE, F1A={}, assumptions={})
for f in FEET:
    c, m = J(f"fit_B2_{f}_cold.json", F1A), J(f"fit_B2_{f}_MB.json", F1A)
    out["F1A"][f] = dict(chi2_cold=c["chi2"]["PA"], chi2_MB=m["chi2"]["PA"], DeltaMB=m["chi2"]["PA"] - c["chi2"]["PA"], R=c["pars"]["oc"] / c["pars"]["ob"])

# KA
ka = J("ka.json"); kas = {}
for f in FEET:
    k2 = J(f"fit_KA2_{f}_cold.json")["KA2"]
    kas[f] = dict(KA1=ka["KA1"][f"{f}_DeltaMB"]["pass_"] and ka["KA1"][f"{f}_cold"]["pass_"] and ka["KA1"][f"{f}_MB"]["pass_"],
                  KA1_d=[ka["KA1"][f"{f}_{m}"]["d"] for m in ("cold", "MB")], KA2=k2["pass_"], KA2_dchi2=k2["dchi2"], KA2_dR=k2["dR"],
                  KA3=ka["KA3"][f]["pass_"], KA3_d=ka["KA3"][f]["d"], KA4=ka["KA4"][f]["pass_"], KA4_d=ka["KA4"][f]["d"])
out["KA"] = kas; ka_ok = all(all(v for k, v in kas[f].items() if k in ("KA1", "KA2", "KA3", "KA4")) for f in FEET)

mu = J("mutate.json"); m_ok = all(mu["M1"][f]["pass_"] and mu["M2"][f]["pass_"] for f in FEET)

# A1
a1 = J("a1.json"); out["assumptions"]["A1"] = {f: dict(label=a1[f]["label"], cH_over_a0=a1[f]["cold"]["cH_over_a0"],
    y_cold=a1[f]["cold"]["y"], y_MB=a1[f]["MB"]["y"], k=a1[f]["cold"]["k"], max_nu_minus_1_MB=a1[f]["max_nu_minus_1_MB"],
    nu_needed=a1[f]["needed"]["nu_needed"], y_needed=a1[f]["needed"]["y_needed"],
    brief_estimate_y_range=[min(e["y"] for e in a1[f]["cold"]["brief_estimate"]), max(e["y"] for e in a1[f]["cold"]["brief_estimate"])]) for f in FEET}

# A2U, A2T, A3N, A4P
for X in ("A2U", "A2T", "A3N", "A4P"):
    row = {}
    for f in FEET:
        try: c, m = J(f"fit_{X}_{f}_cold.json"), J(f"fit_{X}_{f}_MB.json")
        except FileNotFoundError: row[f] = dict(label="NOT RUN"); continue
        d = m["chi2"]["PA"] - c["chi2"]["PA"]; S = d / out["F1A"][f]["DeltaMB"]; dR = c["R"] / out["F1A"][f]["R"] - 1
        row[f] = dict(label=label(d, S, dR), DeltaMB=d, S=S, R=c["R"], dR=dR, chi2_cold=c["chi2"]["PA"], chi2_MB=m["chi2"]["PA"],
                      dchi2_cold_vs_F1A=c["chi2"]["PA"] - out["F1A"][f]["chi2_cold"], theta_cold=c["theta"], theta_MB=m["theta"],
                      edge_cold=c["at_edge"], edge_MB=m["at_edge"], nfev=[c["nfev"], m["nfev"]])
    out["assumptions"][X] = row

# A6
a6 = J("a6point.json"); row = {}
for f in FEET:
    try: m = J(f"fit_A6F_{f}_MB.json")
    except FileNotFoundError: row[f] = dict(label="NOT RUN"); continue
    cw = a6[f"{f}_cold"]["chi2_wide"]; d = m["chi2"]["PA"] - cw; S = d / out["F1A"][f]["DeltaMB"]
    row[f] = dict(label=label(d, S, None), DeltaMB=d, S=S, nuisance_sensitivity=S - 1, point_step1=dict(cold=a6[f"{f}_cold"]["d"], MB=a6[f"{f}_MB"]["d"]),
                  chi2_MB=m["chi2"]["PA"], chi2_cold_wide_point=cw, theta_MB=m["theta"], nuis_MB=m["chi2"]["nuis"], edge_MB=m["at_edge"],
                  R_note="cold not refit (frozen): R is F1A's; the cold refit gain bound is the step-1 cold change")
out["assumptions"]["A6"] = row

# A4 degeneracy
hs = {}
for f in FEET:
    try: h = J(f"a4hess_{f}.json"); hs[f] = {k: h[k] for k in ("sigma", "corr_od_ns", "corr_od_nrun", "dod_dns", "dR_dns", "dR_dnrun", "dns_for_10pct_R", "sigma_R", "R", "chi2_0")}
    except FileNotFoundError: hs[f] = "NOT RUN"
out["assumptions"]["A4_degeneracy"] = hs
out["assumptions"]["A5"] = {f: dict(label="BREAKS (by the record's own data; READING)") for f in FEET}
out["KA_pass"] = ka_ok; out["MUTATE_pass"] = m_ok; out["lane_valid"] = bool(ka_ok and m_ok)
json.dump(out, open(os.path.join(HERE, "cmb3.json"), "w"), indent=1, default=float)
json.dump(dict(M1=mu["M1"], M2=mu["M2"], pass_=m_ok, note=NOTE), open(os.path.join(HERE, "cmb3_MUTATE.json"), "w"), indent=1, default=float)

L = [f"CMB3 (criteria e46081b7a9). KA {'PASS' if ka_ok else 'FAIL'}; MUTATE {'PASS' if m_ok else 'FAIL'}."]
for f in FEET: L.append(f"F1A {f}: DeltaMB {out['F1A'][f]['DeltaMB']:+.1f}, R {out['F1A'][f]['R']:.3f}")
for f in FEET: L.append(f"A1 {f}: {out['assumptions']['A1'][f]['label']}  cH/a0 {out['assumptions']['A1'][f]['cH_over_a0']:.3g}  "
                        f"y_MB {[round(v, 3) for v in out['assumptions']['A1'][f]['y_MB']]}  y_cold {[round(v, 3) for v in out['assumptions']['A1'][f]['y_cold']]}  "
                        f"max nu-1 MB {out['assumptions']['A1'][f]['max_nu_minus_1_MB']:.3f} (needed nu {out['assumptions']['A1'][f]['nu_needed']:.2f})")
for X in ("A2U", "A2T", "A3N", "A4P", "A6"):
    for f in FEET:
        r = out["assumptions"][X][f]
        if "DeltaMB" not in r: L.append(f"{X} {f}: {r['label']}"); continue
        L.append(f"{X} {f}: {r['label']}  DeltaMB {r['DeltaMB']:+.1f}  S {r['S']:.4f}" + (f"  R {r['R']:.3f} dR {r['dR']:+.4f}" if "R" in r else f"  sens {r['nuisance_sensitivity']:+.4f}"))
for f in FEET: L.append(f"A4 degeneracy {f}: {json.dumps(hs[f], default=lambda v: round(v, 4))}")
L.append("A5: BREAKS by the record's own data (reading). " + NOTE)
open(os.path.join(HERE, "cmb3.out"), "w").write("\n".join(L) + "\n"); print("\n".join(L))
M = [f"M1 {f}: d(H1/H2) {mu['M1'][f]['d_oe']:+.4f}, |H3/H2 vs cold - 1| {mu['M1'][f]['third_peak_offset']:.4f}, dchi2 vs cold {mu['M1'][f]['dchi2_vs_cold']:+.1f}, pass {mu['M1'][f]['pass_']}" for f in FEET]
M += [f"M2 {f}: {json.dumps(mu['M2'][f]['dchi2'], default=lambda v: round(v, 2))}, pass {mu['M2'][f]['pass_']}" for f in FEET]
open(os.path.join(HERE, "cmb3_MUTATE.out"), "w").write("\n".join(M) + "\n"); print("\n".join(M))
