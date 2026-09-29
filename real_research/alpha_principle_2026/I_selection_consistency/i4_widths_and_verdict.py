#!/usr/bin/env python3
"""I4 -- widths of the consistency/selection bands relative to 1e-3, the intersection, the chance-probability of a random draw
landing within 1e-3 of alpha_0, and the handle/trial bookkeeping (pre-registered Part 3). Reads i1_bands.json and i2_bands.json (run i1, i2 first).
No physical derivation here: pure bookkeeping.
Run:    python3 i4_widths_and_verdict.py           -> exit 0 if all checks pass
MUTATE: python3 i4_widths_and_verdict.py MUTATE    -> moves the test value alpha_0 by a factor 1.7 (outside the intersection); the check
        'alpha_0 inside every band' must FAIL, exit 1.
"""
import sys, json, math

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
checks = []
def chk(name, ok, info=""):
    checks.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")

b1 = json.load(open("i1_bands.json")); b2 = json.load(open("i2_bands.json"))
a0 = b1["alpha0"]
test_a = a0*1.7 if MUT else a0
print(f"alpha_0 = {a0:.6e} (test value {test_a:.6e})")

def rel(x): return x/a0
# ---- scored hard bands (lo, hi) in alpha
by = {b["name"]: b for b in b1["bands"]}
hard = {
 "Landau toy (SM-fermion QED), hi": (None, by["Landau pole above M_Pl, SM-fermion QED toy (conv A)"]["hi"]),
 "hydrogen stable vs e p -> n nu (recalled), hi": (None, by["hydrogen stable vs e p -> n nu (recalled D_QCD, D_EM)"]["hi"]),
 "Dirac Z_req = 26, hi": (None, by["Dirac Coulomb, Z_req = 26"]["hi"]),
 "stellar window, all c_i = 1": (b2["alpha_lo_c1"], b2["alpha_hi_c1"]),
}
c3 = b2["corners"]["3"]     # (lo_min, lo_max, hi_min, hi_max) over corners c_i in [1/3, 3]
wide_stellar = (c3[0], c3[3])                 # most generous lower/upper edge over the 32 corners
hard_wide = dict(hard); hard_wide["stellar window, most generous edges, c_i in [1/3,3]"] = wide_stellar; del hard_wide["stellar window, all c_i = 1"]
print("\n{:60s} {:>12s} {:>12s} {:>10s} {:>12s}".format("band", "lo/alpha_0", "hi/alpha_0", "width/a0", "width/1e-3"))
def show(nm, lo, hi):
    lo_s = "-" if lo is None else f"{rel(lo):.4g}"; hi_s = "-" if hi is None else f"{rel(hi):.4g}"
    if lo is not None and hi is not None: w = (hi-lo)/a0; ws = f"{w:.4g}"; wk = f"{w/1e-3:.4g}"
    else: ws = "open"; wk = "open"
    print(f"{nm:60s} {lo_s:>12s} {hi_s:>12s} {ws:>10s} {wk:>12s}")
for nm, (lo, hi) in hard.items(): show(nm, lo, hi)
show("stellar window, generous (c_i in [1/3,3])", *wide_stellar)
for nm in ("gravity positivity scaling, lower edge (m_e/M_Pl)^2", "Landau pole above M_Pl, electron only (toy)", "Dirac Coulomb, Z = 1"):
    b = by[nm]; show(nm + " [not in intersection]", b["lo"], b["hi"])

def intersect(bd):
    lo = max([l for l, h in bd.values() if l is not None] + [0.0]); hi = min(h for l, h in bd.values() if h is not None)
    return lo, hi
for label, bd in (("TIGHT (stellar c_i = 1)", hard), ("GENEROUS (stellar edges over c_i in [1/3,3])", hard_wide)):
    lo, hi = intersect(bd)
    print(f"\nIntersection, {label}: [{rel(lo):.4g}, {rel(hi):.4g}] alpha_0; width = {(hi-lo)/a0:.4g} alpha_0 = {(hi-lo)/a0/1e-3:.0f} x 1e-3")
    inside = lo < test_a < hi
    chk(f"alpha_0 inside every band, {label}", inside)
    p_flat = 2e-3*a0/(hi-lo); p_log = 2e-3/math.log(hi/lo)
    print(f"   random draw within 1e-3 of alpha_0: flat prior {p_flat:.3g}, log-flat prior {p_log:.3g}  (i.e. ~ {-math.log2(p_log):.1f} bits at most if the band were a prediction)")
    chk(f"{label}: band is at least 100 x wider than the 1e-3 hit window (a band is not a point)", (hi-lo)/a0/1e-3 > 100)

# ---- handles (declared count 7) and expected chance hits
handles = {
 "H1 Landau edge, electron only": by["Landau pole above M_Pl, electron only (toy)"]["hi"],
 "H2 Landau edge, toy SM fermions": by["Landau pole above M_Pl, SM-fermion QED toy (conv A)"]["hi"],
 "H3 Dirac edge 1/26": by["Dirac Coulomb, Z_req = 26"]["hi"],
 "H4 hydrogen-stability edge": by["hydrogen stable vs e p -> n nu (recalled D_QCD, D_EM)"]["hi"],
 "H5 stellar lower edge (c=1)": b2["alpha_lo_c1"],
 "H6 stellar upper edge (c=1)": b2["alpha_hi_c1"],
 "H7 Carter equality C=1": b2["alpha_C"],
}
print("\nHandles compared to alpha_0 as equalities (hit = within 1e-3):")
hits = 0
for k, v in handles.items():
    h = abs(v/a0 - 1) < 1e-3; hits += h
    print(f"   {k:34s} alpha = {v:.5e}  ratio to alpha_0 = {v/a0:.4f}  {'HIT' if h else 'miss'}")
chk("no handle is a 1e-3 hit (declared expectation)", hits == 0)
p1 = 2e-3/math.log(1e4)
print(f"   trial count = {len(handles)} (H6 and H7 are the same equality, N_crit = N_max: effective distinct = {len(handles)-1});  P(hit) per handle = {p1:.3g} (log-uniform over [1e-4,1]);  E[chance hits] = {len(handles)*p1:.3g}")
print(f"   calibrated-constants Carter reading (recalled stellar numbers): alpha_C = {b2['alpha_C_calibrated']:.4e} = {b2['alpha_C_calibrated']/a0:.3g} alpha_0 (not a handle; reported)")
ok = all(v for _, v in checks)
print(f"\n{sum(v for _,v in checks)}/{len(checks)} checks pass")
sys.exit(0 if ok else 1)
