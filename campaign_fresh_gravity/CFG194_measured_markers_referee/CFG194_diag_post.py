#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG194 post-comparison diagnostics -- written AFTER CFG189's .py/.out/.json were opened; labelled, not part of any frozen result.
Compares my numbers to CFG189's committed results JSON row by row (per-disc inputs, decision cells at s = 0 and 1, break-evens at all s, fit points)."""
import json
from CFG194_lib import *   # noqa

AS = M.load_sparc_anchor()
J = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG189_kurvs_measured_markers", "cfg189_measured_markers_results.json")))
R = J["numbers"]["results"]
PD = J["numbers"]["perdisc"]
Sm = M.load_kurvs(inc_col="inc_star_deg")
P("-- per-disc inputs (primary): max |mine - CFG189|")
S, info = build(rule_primary)
mx = dict(R=0, V=0, eV=0, sig=0, esig=0)
for j, k in enumerate(IDS):
    p = PD[str(k)]
    mx["R"] = max(mx["R"], abs(info[j]["R"] - p["R"])); mx["V"] = max(mx["V"], abs(info[j]["V"] - p["V"]))
    mx["eV"] = max(mx["eV"], abs(info[j]["eV"] - p["eV"])); mx["sig"] = max(mx["sig"], abs(info[j]["sig"] - p["sig"])); mx["esig"] = max(mx["esig"], abs(info[j]["esig"] - p["esig"]))
P("  ", {k: f"{v:.2e}" for k, v in mx.items()})
variants = {"primary": (rule_primary, {}), "V-a": (rule_outerk, dict(k=3)), "V-b": (rule_bothsides, {}), "V-c": (rule_primary, dict(allow_clipped=True)),
            "V-d": (rule_primary, dict(inc_col="inc_star_deg"))}
LM = {"flat": "flat", "rival": "rival", "T": "T"}
worst = {}
for nm, (rule, kw) in variants.items():
    S_, _ = build(rule, **kw)
    r = R[nm]
    dd = []
    for sk, key in (("0.00", 0.0), ("1.00", 1.0)):
        c = cells_three(S_, AS, spec_s(key))
        for l in LAWS:
            dd.append(abs(c[l]["dprime"] - r["cell"][sk][l][0])); dd.append(abs(c[l]["sigma"] - r["cell"][sk][l][1]))
    dbe = []
    ncls = 0
    for s in S_AXIS[1:]:
        for l in LAWS:
            be = break_even(S_, AS, spec_s(s), l)
            th = r["be"][f"{s:.2f}"][l]
            if th is None or (isinstance(th, float) and th != th):
                dbe.append(0.0 if be["mu"] is None else float("nan"))
            else:
                dbe.append(abs(be["mu"] / th - 1) if be["mu"] else float("nan"))
            stt = {"allowed": "gas-allowed", "excluded": "gas-excluded"}.get(status(be))
            key = f"{s:.2f}|{l}"
            if key in r["st"] and stt is not None and r["st"][key] != stt:
                ncls += 1
    fp = {l: fit_point_s(S_, AS, l) for l in LAWS}
    dfp = [abs(fp[l] - r["s0"][l]) for l in ("flat", "rival") if isinstance(fp[l], float) and r["s0"][l] is not None]
    P(f"  {nm:8s} max |dDelta'|,|dsigma| (s=0,1) {max(dd):.2e}; max relative break-even diff {np.nanmax(dbe):.2e} ({int(np.sum(np.isnan(dbe)))} nan/none mismatches); gas-status label differences {ncls}; fit-point diffs {max(dfp) if dfp else float('nan'):.2e}; class mine/theirs {classes(cells_three(S_, AS, SP1 if False else spec_s(1.0)))} / {r['cls']}")
c = cells_three(Sm, AS, spec_s(1.0))
r = R["model"]
P("  model    decision cell diff", max(abs(c[l]["dprime"] - r["cell"]["1.00"][l][0]) for l in LAWS))
