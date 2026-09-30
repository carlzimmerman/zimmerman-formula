"""CFG235_02_main.py -- L1, L2, F1 on the 62-row sample, three look-elsewhere tiers, labels, outcome class (frozen sections 4-9).
Refuses to run unless CFG235_01_controls_results.json exists with every control passing (frozen section 14).  The controls
failed four frozen expectations (see CFG235_01_controls.out); the gate can be passed only with CFG235_GATE_OVERRIDE=1, in
which case every output carries a banner naming the failed controls.  Exit 0 = computed."""
import os, sys, json, math, time
sys.dont_write_bytecode = True
import numpy as np
from scipy.stats import norm
import CFG235_common as C

t0 = time.time()
gate = os.path.join(C.HERE, "CFG235_01_controls_results.json")
if not os.path.exists(gate):
    print("REFUSED: CFG235_01_controls_results.json missing (run CFG235_01_controls.py first)")
    sys.exit(1)
ctl = json.load(open(gate))
samp = json.load(open(os.path.join(C.HERE, "CFG235_00_sample_results.json")))
failed_ctl = ctl["failed"]
override = os.environ.get("CFG235_GATE_OVERRIDE") == "1"
if failed_ctl and not override:
    print("REFUSED: controls failed:", failed_ctl, "(set CFG235_GATE_OVERRIDE=1 to pass the gate with a banner)")
    sys.exit(1)


def P(*a):
    print(C.clean(" ".join(str(x) for x in a)), flush=True)


P("CFG235_02_main: repo = <repo>; kappa = 1/2 is FITTED; nothing here says the data favour any theory")
if failed_ctl:
    P("*" * 100)
    P("GATE OVERRIDDEN: the planted-galaxy controls did NOT all pass. Failed (kept, not repaired):")
    for f in failed_ctl:
        P("   -", f)
    P("All four are properties of the FROZEN design found in the controls before any real statistic was read:")
    P("  (a) the Westfall-Young permutation of residuals with sigma held cannot fire unless the row's sigma is among the smallest")
    P("      (C5b, P1.L1_T2); (b) L2 reaches z_rob > 3 inside its frozen range only with ZERO noise and M200,need >= 3e14 (C6: max 3.06); with the frozen sigmas it cannot (P3, label).")
    P("The main result below is computed exactly as frozen; alternatives are labelled POST-HOC.")
    P("*" * 100)

rows = C.load_sample()
P("frozen sha256", C.FROZEN_SHA, "| n draws", C.N_MC, "| m =", C.M_TRIALS, "| z_B =", round(C.Z_B, 4))
res, meta = C.score_sample(rows, n=C.N_MC, n_perm=100000, n_sim=100000, m_trials=C.M_TRIALS)
R = {q["id"]: q for q in res}
rowd = {r["id"]: r for r in rows}
dups = C.dup_pairs(rows)
dupids = {i for p in dups for i in p[:2]}


def fz(v):
    return "   n/a" if v is None or (isinstance(v, float) and not math.isfinite(v)) else f"{v:6.2f}"


# ------------------------------------------------------------------------------------ table A: every row
P("\nTABLE A: every row. z_prim = primary cell (GS, primary sigma, canonical a0, P2); z_rob = min over the frozen cells.")
P(f"{'id':16} {'z':>5} {'L1 zprim':>8} {'L1 zrob':>8} {'F1 zprim':>8} {'F1 zrob':>8} {'L2':>22} {'T0':>4} {'label T0/T1/T2':>34}  notes")
for q in res:
    r = rowd[q["id"]]
    l2 = q["L2"]
    if not l2.get("defined"):
        l2s = "UNDEFINED(" + ("z>5" if "z > 5" in l2.get("reason", "") else "no floor" if "floor" in l2.get("reason", "") else "range") + ")"
    elif l2.get("not_needed"):
        l2s = "not needed (M_dyn<=M_b)"
    else:
        l2s = f"zrob {l2['z_rob']:.2f}"
    f = []
    if r["known"]:
        f.append(r["known"])
    if q["id"] in dupids:
        f.append("possible-dup")
    if r["vsig"] < 1:
        f.append("V/s<1")
    if r.get("flag_agn"):
        f.append("AGN?")
    if r["tier"] == "G":
        f.append("tier-G")
    if r.get("mapped"):
        f.append("map-assumption")
    t0f = "".join(c for c, k in (("L", "L1"), ("2", "L2"), ("F", "F1")) if q[k]["T0"]) or "-"
    P(f"{q['id']:16} {q['z']:5.2f} {fz(q['L1'].get('z_primary')):>8} {fz(q['L1'].get('z_rob')):>8} {fz(q['F1'].get('z_primary')):>8} {fz(q['F1'].get('z_rob')):>8} {l2s:>22} {t0f:>4} "
      f"{q['label_T0'] + '/' + q['label_T1'] + '/' + q['label_T2']:>34}  {' '.join(f)}")

# ------------------------------------------------------------------------------------ counts
P("\nSAMPLE-LEVEL COUNTS")
for crit in ("L1", "L2", "F1"):
    dfn = [q for q in res if q[crit].get("defined")]
    P(f"  {crit}: defined for {len(dfn)} of 62 rows; T0 flags {sum(q[crit]['T0'] for q in res)}; T1 {sum(q[crit]['T1'] for q in res)}; "
      f"T2 {sum(q[crit]['T2'] for q in res)}; chance expectation at 3 sigma, m = 62: {62 * norm.sf(3.0):.3f}")
l2r = {}
for q in res:
    if not q["L2"].get("defined"):
        k = q["L2"].get("reason", "")
        l2r[k] = l2r.get(k, 0) + 1
P("  L2 UNDEFINED reasons:", l2r)
P("  L2 literal (owner wording: needed M200 exceeds the mass where < 1 halo is expected, central values, V_ref):",
  [q["id"] for q in res if q["L2"].get("literal_break")] or "none")
P("  structural check: every L1 T0 flag is also an F1 T0 flag:", all((not q["L1"]["T0"]) or q["F1"]["T0"] for q in res))

# ------------------------------------------------------------------------------------ L2 detail
P("\nTABLE L2: halo needed to supply the DM inside r (DM14 c-M, central values, V_ref = 2 deg^2 x dz 1). 'literal' = N_exp(central) < 1 (owner wording; REPORTED, not a 3-sigma statement)")
P(f"{'id':16} {'z':>5} {'r_kpc':>6} {'log M200 need':>13} {'N_exp(central)':>15} {'literal':>8} {'z_prim':>7} {'z_rob':>7} {'p2 at z_rob cell':>17}")
for q in res:
    l2 = q["L2"]
    r = rowd[q["id"]]
    if l2.get("defined") and not l2.get("not_needed"):
        P(f"{q['id']:16} {q['z']:5.2f} {r['r_kpc']:6.2f} {l2['M200_central_log']:13.2f} {l2['n_exp_central']:15.3g} {str(l2['literal_break']):>8} {l2['z_primary']:7.2f} {l2['z_rob']:7.2f} {l2['p2_min']:17.3g}")
    elif (not l2.get("defined")) and "range" in l2.get("reason", "") and "z > 5" not in l2.get("reason", ""):
        P(f"{q['id']:16} {q['z']:5.2f} {r['r_kpc']:6.2f} {l2.get('M200_central_log', float('nan')):13.2f}   UNDEFINED: solved M200 outside 1e10-1e15 (central log M200 shown; > 15 = more massive than any halo in range)")

# ------------------------------------------------------------------------------------ flagged galaxies
P("\nEVERY GALAXY THAT BREAKS EITHER THEORY AT ANY TIER (T0 = z_rob > 3 in every cell)")
flagged = [q for q in res if any(q[c]["T0"] for c in ("L1", "L2", "F1"))]
P(f"  {len(flagged)} galaxies; z_B = {meta['zB']:.3f} (Bonferroni, m = 62); WY = Westfall-Young step-down adjusted p (permutation, sigma held); PAR = parametric-null adjusted p (reported only)")
for q in flagged:
    r = rowd[q["id"]]
    P(f"  {q['id']:16} z={q['z']:.3f} src={q['src']} tier={r['tier']} {r['known'] or ''} {'possible-dup' if q['id'] in dupids else ''} {'V/sigma<1' if r['vsig']<1 else ''}")
    for c in ("L1", "L2", "F1"):
        d = q[c]
        if d.get("defined") and not d.get("not_needed") and d.get("T0"):
            pw, pp = d.get("p_wy", float("nan")), d.get("p_param", float("nan"))
            P(f"      {c}: z_prim {fz(d.get('z_primary'))}  z_rob {fz(d['z_rob'])} (cell {d['cell_min']})  | after Bonferroni: {'PASS' if d['T1'] else 'fail'} (z_rob - z_B = {d['z_rob'] - meta['zB']:+.2f})"
              f"  | after WY: p = {pw:.3f} (z-equiv {norm.isf(min(max(pw, 1e-12), 0.5)):.2f}) {'PASS' if d['T2'] else 'fail'}  | PAR p = {pp:.3f}")
    P(f"      labels T0/T1/T2: {q['label_T0']} / {q['label_T1']} / {q['label_T2']}")
if not flagged:
    P("  none")

P("\nNEAR-MISSES (not flagged; top 10 by F1 z_rob and top 10 by L1 z_rob among defined rows), for transparency:")
for crit in ("F1", "L1"):
    top = sorted([q for q in res if q[crit].get("defined")], key=lambda q: -q[crit]["z_rob"])[:10]
    P(f"  {crit}: " + "; ".join(f"{q['id']} {q[crit]['z_rob']:.2f}" for q in top))

# ------------------------------------------------------------------------------------ reported-only columns
P("\nREPORTED-ONLY COLUMNS (never label-bearing)")
P("  S+G cell (measured dust gas at x1/3 added; primary cell) for the six CRISTAL detections:")
for q in res:
    if q["rep"]:
        P(f"    {q['id']:8} L1 z {fz(q['rep'].get('SG_L1_z'))}   F1 z {fz(q['rep'].get('SG_F1_z'))}   (tier S primary: L1 {fz(q['L1'].get('z_primary'))}, F1 {fz(q['F1'].get('z_primary'))})")
P("  rival a0 x E(z) floor (F1 primary cell, P2, canonical) for the rows with F1 z_prim > 1 (reported; the rival has no label):")
for q in res:
    r = rowd[q["id"]]
    if q["F1"].get("defined") and q["F1"]["z_primary"] > 1.0:
        C.A0K["rival"] = C.A0K["canonical"] * float(C.E(r["z"]))
        nd = C.base_draws(r, C.N_MC, C.rng_for(r["id"]))
        dr = C.gen(r, nd)
        m, s = C.cell_stats(r, nd, dr, "GS", "primary", "P2", "rival")
        P(f"    {q['id']:16} F1 z_prim flat {q['F1']['z_primary']:6.2f}   rival {m / s:6.2f}")
P("  no-pressure-term variant (V-lim style: sigma_0 term dropped from V_c^2), primary cell, rows with L1 z_prim > 1 or F1 z_prim > 1:")
for q in res:
    r = dict(rowd[q["id"]])
    if not (q["F1"].get("defined") and max(q["L1"]["z_primary"], q["F1"]["z_primary"]) > 1.0):
        continue
    if r["kind"] == "D":
        vc2 = 10 ** r["lMdyn"] * C.G_KPC / (C.KTOT_D * r["r_kpc"])
        fac = max(1 - C.K_PRESS * r["sigma0"] ** 2 / vc2, 0.01) if math.isfinite(r["sigma0"]) else 1.0
        r["lMdyn"] = r["lMdyn"] + math.log10(fac)
    elif r["kind"] in ("C", "R", "P"):
        r["sigma0"] = 1e-3
    o = C.score_row_LF(r, n=C.N_MC)
    P(f"    {q['id']:16} L1 z_prim {q['L1']['z_primary']:6.2f} -> {o['L1']['z_primary']:6.2f} ; F1 z_prim {q['F1']['z_primary']:6.2f} -> {o['F1']['z_primary']:6.2f}")
P("  L2 z-clamped (c-M at min(z, 5)) for the rows with z > 5 (POST-FREEZE-labelled reported column; never enters a label):")
for r in rows:
    if r["z"] > 5.0 and not C.limit_untestable(r):
        o = C.score_row_L2(r, n=C.N_MC, clamp=True)
        if o.get("defined") and not o.get("not_needed"):
            P(f"    {r['id']:16} z={r['z']:.2f} z_prim {o['z_primary']:6.2f} z_rob {o['z_rob']:6.2f}  N_exp(central, V_ref) = {o['n_exp_central']:.3g}  M200_central = 1e{o['M200_central_log']:.2f}")
        else:
            P(f"    {r['id']:16} z={r['z']:.2f} {'not needed (M_dyn <= M_b)' if o.get('not_needed') else o.get('reason')}")
P("  fit-route model output (never used as data): CRISTAL f_DM and D = 1/(1 - f_DM):")
for r in rows:
    if r["src"] == "C":
        P(f"    {r['id']:8} f_DM {r['fdm']:.2f}  D {1 / (1 - r['fdm']):.2f}")

# ------------------------------------------------------------------------------------ outcome class (frozen wording, literal)
P("\nOUTCOME CLASS (frozen section 9, applied literally)")
lab_T2 = [q for q in res if q["label_T2"] in ("LCDM-only", "framework-only")]
sysprone = lambda q: (rowd[q["id"]]["vsig"] < 1 or q["id"] in dupids or rowd[q["id"]]["tier"] == "G" or rowd[q["id"]].get("flag_agn"))
anyT0 = any(q[c]["T0"] for q in res for c in ("L1", "L2", "F1"))
anyT1 = any(q[c]["T1"] for q in res for c in ("L1", "L2", "F1"))
anyT2 = any(q[c]["T2"] for q in res for c in ("L1", "L2", "F1"))
n_l2 = sum(1 for q in res if q["L2"].get("defined"))
sepok = [k for k, v in samp["separability"].items() if v["S"] >= 3]
P("  T0/T1/T2 flags exist:", anyT0, anyT1, anyT2, "| rows with L2 defined:", n_l2, "(< 20 triggers 'inconclusive' for L2) | rows with separability index S_i >= 3:", len(sepok))
cond_a = (anyT0 or anyT1) and not anyT2
cond_b = n_l2 < 20
cond_c = len(sepok) == 0
P(f"  inconclusive conditions: (a) T0/T1 flags but no T2: {cond_a} ; (b) fewer than 20 rows with L2 defined: {cond_b} ; (c) separability makes the theories indistinguishable (no row with S_i >= 3): {cond_c}")
if lab_T2:
    cls = "one theory broken (in scope)" + (" but every such row is systematic-prone" if all(sysprone(q) for q in lab_T2) else "")
elif cond_a or cond_b or cond_c:
    cls = "INCONCLUSIVE (literal frozen rule)"
else:
    cls = "both survive, only at gross-outlier sensitivity"
P("  CLASS (literal frozen wording):", cls)
fw_only = [q["id"] for q in res if q["label_T2"] == "framework-only"]
lc_only = [q["id"] for q in res if q["label_T2"] == "LCDM-only"]
both_T0 = [q["id"] for q in res if q["label_T0"] == "both"]
P("  sub-statements: framework survives (this test) =", not fw_only, "; LambdaCDM survives (this test) =", not lc_only,
  "; 'both' (mass-estimate outlier) rows at T0 (excluded from both tallies):", both_T0)
P("  Note: 'framework survives' is trivially guaranteed when no row has S_i >= 3 (the label 'framework only' is unreachable), and")
P("  'LambdaCDM survives' is nearly guaranteed: with the frozen sigmas L2 cannot exceed z_rob 3 inside its range (controls P3, C6).")

json.dump(dict(gate_override=bool(failed_ctl), failed_controls=failed_ctl, zB=meta["zB"], m=meta["m"], class_literal=cls,
               conditions=dict(a=cond_a, b=cond_b, c=cond_c), rows=res, dup_pairs=[list(p) for p in dups],
               seconds=time.time() - t0), open(os.path.join(C.HERE, "CFG235_02_main_results.json"), "w"), indent=1, default=float)
P(f"\nCFG235_02_main: done in {time.time() - t0:.0f} s; exit 0")
sys.exit(0)
