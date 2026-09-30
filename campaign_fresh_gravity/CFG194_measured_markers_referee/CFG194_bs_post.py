#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG194 variant BS -- POST-COMPARISON (written after CFG189's .out/.json and CFG184's layout were opened; NOT part of the frozen main).
Departure from the frozen plan, disclosed: the frozen text said BS would use CFG184's functions imported read-only; CFG184 could only be opened
after my main/MUTATE runs were saved, and CFG184's forward model (galaxy-sky convolution) is not re-derived here. I therefore take the per-disc
beam-smearing fractions f_bs at R_out as PRINTED in CFG189's committed .out (3 decimals) -- a shared, quoted input -- and apply the frozen rule
sigma_int = sigma * sqrt(1 - f_bs) inside MY pipeline. BS is thus NOT independent of CFG184/CFG189; what is independent is everything downstream."""
import re
import json
from CFG194_lib import *   # noqa

AS = M.load_sparc_anchor()
txt = open(os.path.join(REPO, "campaign_fresh_gravity", "CFG189_kurvs_measured_markers", "cfg189_measured_markers.out")).read()
line = [l for l in txt.splitlines() if "f_bs at R_out" in l][0]
fbs = {int(k): float(v) for k, v in re.findall(r"K(\d+) ([0-9.]+)", line)}
P("f_bs at R_out (quoted from CFG189's .out):", fbs)
S, info = build(rule_primary)
Sb = copy.copy(S)
Sb.sig = np.array([S.sig[j] * math.sqrt(1 - fbs[k]) for j, k in enumerate(IDS)])
Sb.esig = np.array([S.esig[j] * math.sqrt(1 - fbs[k]) for j, k in enumerate(IDS)])   # error scaled with sigma (my choice; CFG189's rule leaves esig unscaled -- see diag)
Sb2 = copy.copy(S)
Sb2.sig = Sb.sig.copy()   # esig unscaled
out = {}
for nm, SS in (("BS (esig scaled with sigma)", Sb), ("BS (esig unscaled)", Sb2)):
    c = cells_three(SS, AS, spec_s(1.0))
    P(f"  {nm:30s}", fmt_cells(c))
    c0 = cells_three(SS, AS, spec_s(0.0))
    P(f"  {nm:30s} P0:", fmt_cells(c0))
    be = {}
    for s in S_AXIS[1:]:
        be[s] = {l: break_even(SS, AS, spec_s(s), l) for l in LAWS}
        P(f"     s={s:4.2f} mu_be " + "  ".join(f"{l}: {be[s][l]['mu']:.3f} ({status(be[s][l])})" for l in LAWS))
    fp = {l: fit_point_s(SS, AS, l) for l in LAWS}
    P("     fit points:", fp)
    out[nm] = dict(cell={l: dict(c[l]) for l in LAWS}, cls=classes(c), be={str(s): {l: dict(v) for l, v in d.items()} for s, d in be.items()}, fit=fp)
json.dump(out, open(os.path.join(HERE, "CFG194_bs_post_results.json"), "w"), indent=1, default=jdefault)
