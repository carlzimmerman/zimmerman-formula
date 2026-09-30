"""CFG236 compare: POST-RUN, labelled.  Written and run only after CFG236_main, CFG236_MUTATE (M1-M7) and attacks (b)-(f) were saved.
Opens CFG198's and CFG199's committed *_results.json (their targets) and compares row by row with my saved outputs.  Exit 0."""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG236_common as c

o = c.Out("compare")
c.header(o, "CFG236 compare (POST-RUN)")
L = os.path.join(c.REPO, "campaign_fresh_gravity")
j198 = json.load(open(os.path.join(L, "CFG198_musedark_pergalaxy_a0z", "cfg198_musedark_a0z_results.json")))["numbers"]
j199 = json.load(open(os.path.join(L, "CFG199_musedark_level_pressure", "cfg199_musedark_level_results.json")))["numbers"]
mine = json.load(open(os.path.join(HERE := c.HERE, "CFG236_main_results.json")))
m237 = None
try:
    m237 = json.load(open(os.path.join(HERE, "CFG236_main_seed237_results.json")))
except Exception:
    pass
rows = []


def row(i, what, theirs, m, tol=0.05, note=""):
    d = m - theirs
    ok = abs(d) <= tol
    rows.append((i, what, theirs, m, d, ok))
    o.P(f"{'REPRO ' if ok else 'DIFF  '} {i:10s} {what:48s} theirs {theirs:+.4f}  mine {m:+.4f}  diff {d:+.4f} {note}")


P = j198["primary"]
mp = mine["R198_primary"]["st"]
for r, k in (("i", "i"), ("ii", "ii"), ("iii", "iii")):
    row("198-b", f"b_{r}", P[r]["b"], mp[k]["b"])
    row("198-lo", f"CI lo route ({r})", P[r]["ci"][0], mp[k]["lo"], 0.05, "(bootstrap edge)")
    row("198-hi", f"CI hi route ({r})", P[r]["ci"][1], mp[k]["hi"], 0.05, "(bootstrap edge)")
row("198-db", "Delta b", P["db"]["db"], mp["d_ii_i"]["b"])
row("198-dblo", "Delta b CI lo", P["db"]["ci"][0], mp["d_ii_i"]["lo"], 0.05)
row("198-dbhi", "Delta b CI hi", P["db"]["ci"][1], mp["d_ii_i"]["hi"], 0.05)
row("198-dbiii", "b_iii - b_i", P["db_iii"], mp["d_iii_i"]["b"])
p1 = mine["P1"]
for k, kk in (("delta_star = log M_fit - log M*_SED", "dstar"), ("delta_star - log(1 + mu_mol) (fitted disc vs SED + H2)", "dstar_h2")):
    row("198-P1", k[:40] + " b", j198["P1"][k]["b"], p1[kk]["b"], 0.03)
    row("198-P1lo", k[:40] + " lo", j198["P1"][k]["ci"][0], p1[kk]["lo"], 0.05)
    row("198-P1hi", k[:40] + " hi", j198["P1"][k]["ci"][1], p1[kk]["hi"], 0.05)
lev = mine["levels198"]
for r in ("i", "ii", "iii"):
    for t in range(3):
        row("198-lev", f"median log a0 z-third {t+1} route ({r})", P[r]["median_log_a0_by_z_third"][t], lev[r][t], 0.05)
mapn = {"Sigma_HI = 0": "Sig0", "Sigma_HI = 15": "Sig15", "mu_mol x 0.5": "mu0.5", "mu_mol x 2": "mu2"}
for kk, nm in mapn.items():
    J = j198["robustness"][kk]
    M = mine["robust198"][nm]["st"]
    row("198-rob", f"{kk}: b_ii", J["b"]["ii"], M["ii"]["b"])
    row("198-rob", f"{kk}: Delta b", J["db"]["db"] if isinstance(J["db"], dict) else J["db"], M["d_ii_i"]["b"])
    o.P(f"      R1 excluded theirs {J['verdicts']} | mine {mine['robust198'][nm]['excluded']}")
o.P("CFG198 route (i) CI [%s]: R0 in theirs = %s" % (P["i"]["ci"], j198["primary_verdicts"]))

# CFG199
R = mine["R199"]
for rd, key in (("a", "a: v_perp = v_file"), ("b", "b: v_perp = v_file / sin i")):
    J = j199["readings"][key]
    M = R[rd]["st"]
    for r in ("i", "ii", "iii"):
        row("199-b", f"({rd}) b_{r}", J["L2"][r]["b"], M[r]["b"])
        row("199-lo", f"({rd}) CI lo route ({r})", J["L2"][r]["ci"][0], M[r]["lo"], 0.05)
        row("199-hi", f"({rd}) CI hi route ({r})", J["L2"][r]["ci"][1], M[r]["hi"], 0.05)
    row("199-db", f"({rd}) Delta b", J["db"]["db"], M["d_ii_i"]["b"])
    row("199-lev", f"({rd}) L1 level lowest third", J["L1"]["median"], R[rd]["level"][0])
    row("199-levlo", f"({rd}) L1 CI lo", J["L1"]["ci"][0], R[rd]["level"][1], 0.05)
    row("199-levhi", f"({rd}) L1 CI hi", J["L1"]["ci"][1], R[rd]["level"][2], 0.05)
    row("199-rho", f"({rd}) rho(v/v_c198, sin i)", J["L3"]["rho_sin_i"], R[rd]["rho"], 0.05)
# quantities computed here from the common code (post-run): lowest-third medians of routes ii/iii in R199, and the median log ratio of README
T = c.load_numeric()
idx, cnt = c.sample(T)
C = c.get_cols(T, idx)
z = C["z"]
dat = c.load_dat(T, idx)
R198 = c.routes(C)
for rd, key in (("a", "a: v_perp = v_file"), ("b", "b: v_perp = v_file / sin i")):
    J = j199["readings"][key]
    gp = c.gperp_reading(dat["v1"], C["Re"], C["incl"], rd)
    Rr = c.routes(C, dict(mode="R199", gperp=gp))
    vi = np.isfinite(Rr["a0_i"])
    th = c.thirds(z[vi])
    ids_i = np.where(vi)[0]
    for r in ("ii", "iii"):
        Lv = c.level_log(Rr["a0_" + r])
        row("199-lev23", f"({rd}) lowest-third median route ({r})", J["levels_ii_iii"][r], float(np.nanmedian(Lv[ids_i[th[0]]])))
    lr = np.log10(gp / R198["gobs"])
    o.P(f"   ({rd}) median log10(g_perp/g_obs,198): over S {np.median(lr):+.3f}; over the lowest z-third of route (i) {np.median(lr[ids_i[th[0]]]):+.3f}; CFG199 README states {J['L1']['shift_vs_CFG198']:+.3f} (its L1 'shift')")
    row("199-shift", f"({rd}) shift vs CFG198, lowest third", J["L1"]["shift_vs_CFG198"], float(np.median(lr[ids_i[th[0]]])), 0.02)
nrep = sum(1 for r in rows if r[5])
o.P(f"\nrows compared: {len(rows)}; within tolerance: {nrep}; outside: {[ (r[0], r[1], round(r[4], 3)) for r in rows if not r[5]]}")
if m237:
    o.P("seed 237 main: pass lines fail (non-info): %s" % [p["id"] for p in m237["pass_lines"] if not p["ok"] and not p.get("info")])
o.res = dict(rows=[dict(id=r[0], what=r[1], theirs=r[2], mine=r[3], diff=r[4], ok=r[5]) for r in rows])
o.finish()
sys.exit(0)
