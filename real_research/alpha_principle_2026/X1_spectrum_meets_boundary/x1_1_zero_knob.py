#!/usr/bin/env python3
"""x1_1_zero_knob -- Track Z of lane X1: the 52 zero-knob (spectrum, boundary rule) pairs (pre-registered in X1_PREREGISTRATION.md).
Every exotic mass is one of two discrete, parameter-free prescriptions (P_dec: decoupled at the boundary, P_EW: at m_Z); every scale is a programme scale or is solved by the rule itself.
Run (real):    PYTHONDONTWRITEBYTECODE=1 python3 x1_1_zero_knob.py           -> writes x1_1_results.json; exit 0 iff the controls pass (2 otherwise); the pair verdicts are DATA, not pass/fail of the script
Run (control): PYTHONDONTWRITEBYTECODE=1 python3 x1_1_zero_knob.py MUTATE    -> the positive control (a synthetic rule equal to the central run) is perturbed by 8%: K1 must FAIL; exit 1 if the control bites, 3 if it does not; writes x1_1_results_MUTATE.json
Controls inside: K1 positive control passes T-JOINT; K2 negative control (+8%) fails; K3 lane D's bar interface (clears at a 1e-11 match with precision 1e-11, does not clear at 1%).
"""
import sys
sys.dont_write_bytecode = True
import json
import math
import numpy as np
import x1_lib as L

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
chk = L.Checks(MUT)
XP, XR = L.XP, L.XR
XS = L.species_scale


def jsonable(o):
    if isinstance(o, dict):
        return {k: jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, (np.floating, np.integer, np.bool_)):
        return o.item()
    if isinstance(o, np.ndarray):
        return jsonable(o.tolist())
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return None
    return o


def build_variants():
    V = []

    def add(spec, prescr, n27, rule):
        V.append(dict(spectrum=spec, prescription=prescr, n27=n27, rule=rule))
    # S1
    for tag, X in (("X_P", XP), ("X_R", XR), ("X_S", XS(118))):
        add("S1", "none", 0, L.make_rule("RC", X=X, xtag=tag, param_scale=(tag == "X_S")))
    for tag, X in (("X_P", XP), ("X_S", XS(118))):
        add("S1", "none", 0, L.make_rule("RD", X=X, xtag=tag, s1=True, param_scale=(tag == "X_S")))
    for N in (118, 126):
        add("S1", "none", 0, L.make_rule("RF", X=XS(N), xtag="X_S", N=N, param_scale=True))
    for N in (118, 126):
        add("S1", "none", 0, L.make_rule("RG", X=XS(N), xtag="X_S", N=N, param_scale=True))
    # S2
    for tag, X in (("X_P", XP), ("X_R", XR), ("X_S", XS(118))):
        add("S2", "none", 0, L.make_rule("RA", X=X, xtag=tag, param_scale=(tag == "X_S")))
    add("S2", "none", 0, L.make_rule("RB", xtag="cross"))
    for tag, X in (("X_P", XP), ("X_S", XS(118)), ("cross", None)):
        add("S2", "none", 0, L.make_rule("RD", X=X, xtag=tag, h=8, param_scale=(tag == "X_S")))
    add("S2", "none", 0, L.make_rule("RE", xtag="het"))
    # S3, P_dec
    n = 3
    for tag, X in (("X_P", XP), ("X_S", XS(118 + 22 * n)), ("cross", None)):
        add("S3", "P_dec", n, L.make_rule("RD", X=X, xtag=tag, h=12, param_scale=(tag == "X_S")))
    for n27 in (1, 3):
        for base in (118, 126):
            N = base + 22 * n27
            add("S3", "P_dec", n27, L.make_rule("RF", X=XS(N), xtag="X_S", N=N, param_scale=True))
    for n27 in (1, 3):
        for base in (118, 126):
            N = base + 22 * n27
            add("S3", "P_dec", n27, L.make_rule("RG", X=XS(N), xtag="X_S", N=N, param_scale=True))
    # S3, P_EW
    for n27 in (1, 3):
        Ns = 118 + 22 * n27
        for tag, X in (("X_P", XP), ("X_R", XR), ("X_S", XS(Ns))):
            add("S3", "P_EW", n27, L.make_rule("RA", X=X, xtag=tag, param_scale=(tag == "X_S")))
        add("S3", "P_EW", n27, L.make_rule("RB", xtag="cross"))
        for tag, X in (("X_P", XP), ("X_S", XS(Ns)), ("cross", None)):
            add("S3", "P_EW", n27, L.make_rule("RD", X=X, xtag=tag, h=12, param_scale=(tag == "X_S")))
        add("S3", "P_EW", n27, L.make_rule("RE", xtag="het"))
        for base in (118, 126):
            N = base + 22 * n27
            add("S3", "P_EW", n27, L.make_rule("RF", X=XS(N), xtag="X_S", N=N, param_scale=True))
        for base in (118, 126):
            N = base + 22 * n27
            add("S3", "P_EW", n27, L.make_rule("RG", X=XS(N), xtag="X_S", N=N, param_scale=True))
    for i, v in enumerate(V):
        v["id"] = f"Z{i + 1:02d}"
    return V


def exotics_for(v):
    if v["prescription"] == "P_EW":
        return L.exotics_e6(L.MZ, L.MZ, v["n27"])
    return []


# ------------------------------------------------------------------------------------------------ controls
print("=" * 118)
print("X1-1 Track Z (zero knobs) -- mode:", "MUTATE (control)" if MUT else "REAL RUN")
print("=" * 118)
V = build_variants()
chk("K0 registered Track-Z variants: 52 (S1 9, S2 8, S3 P_dec 11, S3 P_EW 24); ids unique", len(V) == 52 and len({v["id"] for v in V}) == 52, f"({len(V)})")
cen = L.desert("2L-T")
Apos = cen.A(XP)
scale_pos = 1.08 if MUT else 1.0
syn = L.make_rule("SYN", X=XP, xtag="X_P")
syn["pred"] = (Apos * scale_pos).tolist()
syn["absolute"] = False
evp = L.evaluate_bands(syn, [])
chk("K1 positive control: a synthetic rule equal to the central run's own values passes T-JOINT" + (" [MUTATE: perturbed by 8%]" if MUT else ""), evp["pass"], f"(r = {np.round(evp['cen_r'], 4)}, tol = {np.round(evp['tol'], 4)})")
synn = dict(syn)
synn["pred"] = (Apos * 1.08).tolist()
evn = L.evaluate_bands(synn, [])
chk("K2 negative control: the same values x 1.08 fail T-JOINT", not evn["pass"], f"(r = {np.round(evn['cen_r'], 4)})")
ok_pos, _ = L.bar_verdict(1e-11, 1e-11)
ok_neg, _ = L.bar_verdict(1e-2, 1e-2)
chk("K3 lane D's bar interface: clears at a 1e-11 match with precision 1e-11 (81 trials, 0 fitted reals), does not clear at 1%", ok_pos and not ok_neg)

# ------------------------------------------------------------------------------------------------ the 52 pairs
results = []
print()
print(f"{'id':4s} {'spec':3s} {'presc':6s} {'n27':3s} {'rule':26s} {'X (GeV)':>10s}  residuals (tol) [factor |r|/tol]                                    verdict")
for v in V:
    rule = v["rule"]
    exo = exotics_for(v)
    ev = L.evaluate_bands(rule, exo)
    rec = dict(id=v["id"], spectrum=v["spectrum"], prescription=v["prescription"], n27=v["n27"], rule=rule["id"], kind=rule["kind"], absolute=rule["absolute"], K_eq=rule["K_eq"], u=rule["u"], ev=ev)
    if not ev["exists"]:
        rec["verdict"] = "Z-DEAD (scale does not exist below the integrated range: crossing absent below 3 X_P or the run left the perturbative range)"
        rec["margin_max"] = None
        line = f"{v['id']} {v['spectrum']:3s} {v['prescription']:6s} {v['n27']:<3d} {rule['id']:26s} {'--':>10s}  scale absent  -> Z-DEAD"
    else:
        dom = L.domain_kill(ev)
        mono, mono_hits = L.mono_kill(rule, ev)
        rec["domain_kill"], rec["mono_kill"], rec["mono_hits"] = dom, mono, mono_hits
        rec["margin_max"] = float(max(ev["margin"]))
        if dom:
            verdict = "Z-DEAD (domain: X > M_P)"
        elif mono:
            verdict = "Z-DEAD (matter-monotone: " + ",".join(mono_hits) + ")"
        elif ev["pass"]:
            verdict = "Z-PASS" + (" (relational: alpha(0) stays an INPUT)" if not rule["absolute"] else "")
        else:
            verdict = f"Z-FAIL (x{rec['margin_max']:.1f} the running's uncertainty)"
        rec["verdict"] = verdict
        rs = " ".join(f"{n}:{r:+.3f}({t:.3f})[{m:.1f}]" for n, r, t, m in zip(ev["names"], ev["cen_r"], ev["tol"], ev["margin"]))
        line = f"{v['id']} {v['spectrum']:3s} {v['prescription']:6s} {v['n27']:<3d} {rule['id']:26s} {ev['X']:10.3e}  {rs:70s} -> {verdict}"
        # T-ABS and bar
        if ev["implied"]:
            imp = ev["implied"]
            clears, br = L.bar_verdict(imp["delta"], imp["tol_em"])
            rec["alpha0"] = dict(implied_inv=imp["central"], delta=imp["delta"], tol_em=imp["tol_em"], clears_bar=clears, within_tol=imp["delta"] <= imp["tol_em"],
                                 valid_translation=bool(all(L.Run("2L-T", []).a0[k] + (ev["pred"][k] - ev["A"][k]) > 0 for k in range(3) if ev["pred"][k] is not None)))
            line += f"\n        alpha(0): implied 1/alpha = {imp['central']:.2f} (miss {imp['delta']:.3f}, tol_em {imp['tol_em']:.3f}); bar: {'CLEARS' if clears else 'does not clear'}"
        # inequality checks for unified rules
        unified = rule["kind"] in ("RA", "RB", "RE") or (rule["kind"] == "RD" and not rule["s1"])
        if unified and ev["A"] is not None:
            pc, tau = L.proton_check(ev["X"], ev["A"][1])
            rec["ineq"] = dict(proton=pc, tau_yr=tau)
            line += f"\n        proton lifetime check (recalled scaling): {pc} (tau ~ {tau:.2e} yr)"
    print(line)
    results.append(rec)

# --- predicted Landau-pole scales (reported numbers, no data to compare)
print()
land = {}
for name, exo in (("desert (S1, S2, S3 P_dec)", []), ("S3 P_EW n27=1", L.exotics_e6(L.MZ, L.MZ, 1)), ("S3 P_EW n27=3", L.exotics_e6(L.MZ, L.MZ, 3))):
    a, z = L.landau_scale_log10(exo)
    land[name] = dict(log10_aY_eq_1=a, log10_aY_extrap_zero=z)
    print(f"  U(1)_Y non-perturbative onset (a_Y = 1), {name}: log10(GeV) = {a}; linear extrapolation to a_Y = 0: {z}")
# --- tallies
def tally(pred):
    return sum(1 for r in results if pred(r))
n_pass = tally(lambda r: r["verdict"].startswith("Z-PASS"))
n_fail = tally(lambda r: r["verdict"].startswith("Z-FAIL"))
n_dead = tally(lambda r: r["verdict"].startswith("Z-DEAD"))
print(f"\nTrack Z tally: {n_pass} Z-PASS, {n_fail} Z-FAIL, {n_dead} Z-DEAD (total {len(results)})")
for r in results:
    if r["verdict"].startswith("Z-PASS"):
        print("  Z-PASS:", r["id"], r["spectrum"], r["prescription"], r["rule"], "margin", r["margin_max"])
out = dict(variants=results, landau=land, tally=dict(pass_=n_pass, fail=n_fail, dead=n_dead), mutate=MUT)
with open("x1_1_results_MUTATE.json" if MUT else "x1_1_results.json", "w") as f:
    json.dump(jsonable(out), f, indent=1)
chk.finish("X1-1")
