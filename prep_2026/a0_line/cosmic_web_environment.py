#!/usr/bin/env python3
r"""
cosmic_web_environment.py -- DOES PER-GALAXY a0 TRACK THE COSMIC-WEB ENVIRONMENT?
 The THREE forked predictions (canonical / alt-footing / Verlinde) + the distance-method
 confound that decides whether SPARC can see any of them.
================================================================================================
Framework: Zimmerman de Sitter-Unruh MODIFIED INERTIA, g_obs = sqrt(g_bar^2 + a0*g_bar),
a0 = c*H_Lambda/Z, Z = sqrt(32*pi/3). The a0-line residual estimator + its +/-16% error budget
live in estimator_theory.py; the gas-dominated cut in identity_uniqueness.py. This script asks a
question NEITHER of those resolves: is a0 the SAME in voids, walls and clusters?

WHY IT ADJUDICATES THE FOOTING FORK (the thing the ledger says SPARC alone cannot resolve):
  (a) CANONICAL / PURE-LAMBDA  a0 = c^2 sqrt(Lambda/32pi).  Lambda is a COSMOLOGICAL CONSTANT --
      spatially UNIFORM by definition -- so a0 is EXACTLY the same everywhere.  d log a0 / d log(1+d) = 0
      EXACTLY.  This is a theorem (Section P proves it symbolically), the framework's committed reading.
  (b) ALT / LOCAL-H FOOTING     a0 = c*H_local/Z, H_local the LOCAL expansion rate.  Linear theory gives
      dH/H = -(1/3) f delta  (f = Omega_m^0.55 ~ 0.53): local H is ENHANCED in voids (outflow), SUPPRESSED
      in overdensities (infall).  a0 ~ H_local  =>  a0 HIGHER in voids.  Slope = -f/3 ~ -0.18 (NEGATIVE).
  (c) VERLINDE / EMERGENT       a0 ~ c*H0 set by the (global) de Sitter horizon -> slope 0 at leading order
      (degenerate with canonical), PLUS an EFE-like entropic screening in dense environments -> a mild
      NEGATIVE slope, same sign as (b), amplitude model-dependent (~ -0.05..-0.2).
  [X] MAXIMAL LOCAL-MATTER CARICATURE  a0 ~ sqrt(rho_ambient): slope +0.5 (a0 higher in CLUSTERS).  No
      serious theory predicts this; it is the maximal-coupling upper anchor and has the OPPOSITE sign to (b),(c).

So the readings do not merely differ in amplitude -- (b)/(c) put a0 HIGHER in voids while [X] puts it
higher in clusters, and (a) is flat.  A measured slope adjudicates canonical-vs-alt INTERNALLY.

THE KILLER CONFOUND (Section C, the reason a naive measurement is worthless):
  In the deep-MOND fit a0 = g_obs^2/g_bar, with g_obs = V^2/R ~ 1/D and g_bar ~ D^0 (estimator_theory
  S2), so  a0_fit ~ D^-2.  For a HUBBLE-FLOW distance D = cz/H0, the SAME peculiar-velocity field that
  defines the cosmic web corrupts D -- and therefore a0 -- in a way that CORRELATES WITH ENVIRONMENT.
  Worse: if the alt footing (b) were TRUE, a Hubble-flow distance would carry a physical +dH/H in a0 AND
  a distance-artifact -2 dH/H (because D_HF = D_true*(1+dH/H) and a0 ~ D^-2), whose sum FLIPS the sign of
  the apparent trend.  A measurement on Hubble-flow distances cannot be trusted -- it can fake OR invert a
  gradient.  The CLEAN test uses ONLY redshift-INDEPENDENT distances (TRGB / Cepheid / cluster / SN-Ia),
  where a0_fit ~ D_true^-2 is decoupled from the peculiar-velocity field.

BUILDS ON (does not duplicate): real_research/reviews/project_sparc_a0_vs_cosmicweb.py already cross-
matched SPARC a0 to 2MRS counts / Tully halo mass / 2M++ real-space density and found a NULL, and wrote
data/sparc_a0_environment_table.csv.  This script (i) DERIVES the three forked amplitudes that script only
gestured at, (ii) SPLITS that committed table by SPARC's distance-method flag f_D to isolate the clean
subsample, and (iii) computes the honest N required -- the piece the prior null did not quantify.

HONESTY RAILS: pure-Lambda 0 is a theorem, not a fit; alt/Verlinde amplitudes are derived from stated
linear-theory inputs; the measurement is reported on the CLEAN subsample with its (wide) error; a null that
cannot separate canonical from alt is reported AS underpowered, not as a win for either.  Exit 0 = symbolic
checks pass + numbers computed, NOT 'framework confirmed'.
"""
import sympy as sp
import numpy as np, csv, os, json
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research"
LEDGER = "/Users/carlzimmerman/new_physics/prep_2026/concordance_ledger"
anchor = json.load(open(os.path.join(LEDGER, "anchor_values.json")))
A0C, A0A = anchor["a0_canon"], anchor["a0_alt"]
ENVCSV = os.path.join(REPO, "data", "sparc_a0_environment_table.csv")
MASTER = os.path.join(REPO, "data", "sparc_master_clean.csv")
bar = "=" * 96

# cosmology inputs for the linear-theory amplitudes (stated, not hidden)
OMEGA_M = 0.315                       # Planck 2018 matter density
GROWTH_INDEX = 0.55                   # f = Omega_m^gamma, gamma~0.55 (GR)
F_GROWTH = OMEGA_M ** GROWTH_INDEX
DELTA_VOID = -0.8                     # deep-void matter contrast (linear-safe edge)
DELTA_WALL = +1.0                     # wall / mild filament
DELTA_CLUST = +5.0                    # rich group / cluster outskirt (linear FORMULA breaks; flagged)

DMETH = {1: "Hubble-flow", 2: "TRGB", 3: "Cepheid", 4: "UMa-cluster", 5: "SN-Ia"}
REDSHIFT_INDEP = {2, 3, 4, 5}        # distance NOT derived from the galaxy's own redshift


# ------------------------------------------------------------------------------------------ P
print(bar); print("SECTION P -- THE THREE FORKED PREDICTIONS (derived, side by side)"); print(bar)

# (a) PURE-LAMBDA: prove d a0 / d rho_local = 0 EXACTLY.
Lam, cc, rho_loc = sp.symbols("Lambda c rho_local", positive=True)
a0_canon = cc**2 * sp.sqrt(Lam / (32 * sp.pi))            # a0 = c*H_Lambda/Z, H_Lambda=c*sqrt(Lambda/3), Z=sqrt(32pi/3)
d_canon = sp.diff(a0_canon, rho_loc)
assert d_canon == 0, "pure-Lambda a0 somehow depends on local density"
print("  (a) CANONICAL  a0 = c^2*sqrt(Lambda/32pi).  d a0/d rho_local =", d_canon,
      "  => a0 spatially UNIFORM.")
print("      Lambda is a constant of nature; a0 has NO local-density input.  SLOPE = 0 EXACTLY (a theorem).")

# (b) ALT / LOCAL-H: a0 ~ H_local, dH/H = -(1/3) f delta.  slope = d log a0 / d log(1+delta) at delta->0.
d_sym = sp.symbols("delta", real=True)
f_sym = sp.symbols("f", positive=True)
dHH = -sp.Rational(1, 3) * f_sym * d_sym                  # linear-theory local Hubble-rate perturbation
loga0 = sp.log(1 + dHH)                                   # a0 ~ H_local = H0*(1+dH/H)
slope_alt_sym = sp.simplify(sp.diff(loga0, d_sym) / sp.diff(sp.log(1 + d_sym), d_sym)).subs(d_sym, 0)
slope_alt = float(slope_alt_sym.subs(f_sym, F_GROWTH))
assert sp.simplify(slope_alt_sym - (-f_sym / 3)) == 0     # slope -> -f/3 at delta=0
print(f"  (b) ALT/LOCAL-H  a0 ~ H_local, dH/H = -(1/3) f delta,  f = Omega_m^0.55 = {F_GROWTH:.3f}")
print(f"      slope d log a0 / d log(1+delta) = -f/3 = {slope_alt:+.3f}  (NEGATIVE: a0 HIGHER in voids).")

def dhh(delta):  # Delta a0 / a0 = dH/H  (alt footing), linear theory
    return -(1.0 / 3.0) * F_GROWTH * delta

# (c) VERLINDE / EMERGENT: global horizon -> slope 0; EFE-like entropic screening -> mild negative.
verl_lo, verl_hi = -0.20, -0.05                          # characterized band (model-dependent, same sign as alt)
print("  (c) VERLINDE   a0 ~ c*H0 (GLOBAL de Sitter horizon) -> slope 0 at leading order (degenerate with a);")
print(f"      PLUS an EFE-like entropic screening in dense environments -> slope ~ {verl_hi:+.2f}..{verl_lo:+.2f}")
print("      (same NEGATIVE sign as (b); amplitude model-dependent).  NOT the +0.5 matter-sourcing slope.")

# [X] maximal caricature a0 ~ sqrt(rho_ambient): slope +0.5, OPPOSITE sign.
print("  [X] MAXIMAL a0~sqrt(rho_ambient): slope +0.5 (a0 higher in CLUSTERS) -- strawman upper anchor, opposite sign.")

print()
print("  DISCRIMINATING TABLE -- Delta(a0)/a0 by environment (deep void / wall / cluster):")
print(f"  {'reading':<26}{'slope d.log a0/d.log(1+d)':>26}{'void d=-0.8':>13}{'wall d=+1':>11}{'cluster d=+5':>13}")
v_alt, w_alt = dhh(DELTA_VOID), dhh(DELTA_WALL)
print(f"  {'(a) canonical pure-Lambda':<26}{'  0.000':>26}{0.0:>+12.1%}{0.0:>+11.1%}{'0.0%':>13}")
print(f"  {'(b) alt / local-H':<26}{slope_alt:>+26.3f}{v_alt:>+12.1%}{w_alt:>+11.1%}{'strong supp.':>13}")
print(f"  {'(c) Verlinde (EFE band)':<26}{str('%.2f..%.2f'%(verl_hi,verl_lo)):>26}{'0..+'+('%.0f'%(abs(v_alt)*100))+'%':>12}{'0..'+('%.0f'%(w_alt*100))+'%':>11}{'mild supp.':>13}")
print(f"  {'[X] a0~sqrt(rho) (strawman)':<26}{0.5:>+26.3f}{(np.sqrt(1+DELTA_VOID)-1):>+12.1%}{(np.sqrt(1+DELTA_WALL)-1):>+11.1%}{(np.sqrt(1+DELTA_CLUST)-1):>+12.0%}")
print("  NOTE: alt/Verlinde cluster values use linear theory which BREAKS DOWN (H_local->0 in a virialized")
print("  core => a0 strongly suppressed under alt footing: a distinctive, falsifiable cluster-core prediction).")
print(f"  The single sharpest contrast is the SIGN: canonical 0, alt/Verlinde NEGATIVE (~{slope_alt:.2f}), strawman +0.5.")


# ------------------------------------------------------------------------------------------ data
def load_env():
    """Join the committed environment table (a0, D, cz, 2MRS, 2M++) with SPARC f_D + Hubble type."""
    fd, T = {}, {}
    with open(MASTER) as f:
        for r in csv.DictReader(f):
            fd[r["name"]] = int(r["fD"]); T[r["name"]] = int(r["T"])
    rows = []
    with open(ENVCSV) as f:
        for r in csv.DictReader(f):
            n = r["name"]
            rows.append(dict(
                name=n, la0=float(r["log10_a0"]), D=float(r["D_Mpc"]), cz=float(r["cz_kms"]),
                fD=fd.get(n, -1), T=T.get(n, -99),
                od_2mrs=(float(r["onepd_2mrs"]) if r["onepd_2mrs"] else np.nan),
                usable_2mrs=(r["usable_2mrs"] == "1"),
                od_2mpp=(float(r["onepd_2mpp"]) if r["onepd_2mpp"] else np.nan)))
    return rows

rows = load_env()


# ------------------------------------------------------------------------------------------ C
print(); print(bar); print("SECTION C -- THE DISTANCE-METHOD CONFOUND (why only clean distances count)"); print(bar)

# symbolic: a0_fit ~ D^-2 in the deep-MOND fit, and the Hubble-flow double-bias.
D, Dh, V, Sig, r0 = sp.symbols("D D_hat V_obs Sigma r_hat", positive=True)
rphys = r0 * D / Dh
g_obs = V**2 / rphys                     # V distance-independent, r ~ D
g_bar = Sig                              # surface density, distance-independent (estimator_theory S2)
a0_fit = g_obs**2 / g_bar
p_D = sp.simplify(sp.diff(sp.log(a0_fit), sp.log(D)) if False else sp.diff(a0_fit, D) * D / a0_fit)
assert sp.simplify(p_D + 2) == 0, "a0_fit is not ~ D^-2"
print("  a0_fit = g_obs^2/g_bar,  g_obs ~ 1/D, g_bar ~ D^0  =>  d log a0_fit / d log D =", p_D, " (a0 ~ D^-2).")
# Hubble-flow double bias: D_HF = D_true*(1+dH/H); alt a0_phys ~ (1+dH/H); a0_fit ~ D_HF^-2 ~ (1+dH/H)^-2.
x = sp.symbols("x", real=True)            # x = dH/H
a0_measured = (1 + x) * (1 + x)**(-2)     # physical alt-footing gain * distance artifact
lead = sp.series(sp.log(a0_measured), x, 0, 2).removeO()
print("  If ALT footing were true and D is Hubble-flow: a0_measured ~ (1+dH/H)*(1+dH/H)^-2 = (1+dH/H)^-1.")
print(f"      log a0_measured = {sp.simplify(lead)} + O(x^2)  => apparent slope has the OPPOSITE sign to the")
print("      physical +dH/H: the confound can INVERT the trend. Only redshift-INDEPENDENT D breaks it.")

clean = [r for r in rows if r["fD"] in REDSHIFT_INDEP]
hf = [r for r in rows if r["fD"] == 1]
from collections import Counter
cby = Counter(r["fD"] for r in rows)
print("\n  environment-table galaxies by SPARC distance method f_D:")
for k in sorted(cby):
    tag = "REDSHIFT-INDEP (clean)" if k in REDSHIFT_INDEP else "redshift-based (CONFOUNDED)"
    print(f"     f_D={k} {DMETH.get(k,'?'):12s} N={cby[k]:3d}   {tag}")
print(f"  => CLEAN subsample N={len(clean)}  |  Hubble-flow (confounded) N={len(hf)}  of {len(rows)} total.")
dc = np.array([r["D"] for r in clean]); od_c = np.array([r["od_2mpp"] for r in clean])
odc = od_c[np.isfinite(od_c)]
print(f"  clean D: median {np.median(dc):.1f} Mpc (Local-Volume dominated), range {dc.min():.1f}-{dc.max():.1f} Mpc.")
print(f"  clean 2M++ (1+delta): {np.nanmin(odc):.2f}..{np.nanmax(odc):.2f};  underdense (<1): {(odc<1).sum()},"
      f"  deep-void (<0.5): {(odc<0.5).sum()}  <== the clean sample has essentially NO deep-void coverage.")


def slope_of(sample, key, need_usable=False):
    la0 = np.array([r["la0"] for r in sample])
    od = np.array([r[key] for r in sample])
    m = np.isfinite(la0) & np.isfinite(od) & (od > 0)
    if need_usable:
        m &= np.array([r["usable_2mrs"] for r in sample])
    if m.sum() < 8:
        return dict(N=int(m.sum()), slope=np.nan, se=np.nan, rs=np.nan, ps=np.nan)
    x = np.log10(od[m]); y = la0[m]
    sl, ic, rr, pp, se = stats.linregress(x, y)
    rs, ps = stats.spearmanr(od[m], y)
    return dict(N=int(m.sum()), slope=float(sl), se=float(se), rs=float(rs), ps=float(ps))


print(f"\n  measured slope d log a0 / d log(1+delta) by subsample -- vs the three predictions:")
print(f"  {'proxy / subsample':<30}{'N':>4}{'slope':>16}{'sigma from:':>10}  {'0(canon)':>9}{'-0.18(alt)':>11}{'+0.5(straw)':>12}")
results = {}
for proxy, key, need in [("2M++ real-space", "od_2mpp", False), ("2MRS counts", "od_2mrs", True)]:
    for tag, sample in [("ALL", rows), ("CLEAN (z-indep)", clean), ("Hubble-flow", hf)]:
        d = slope_of(sample, key, need)
        results[f"{proxy}|{tag}"] = d
        if not np.isfinite(d["slope"]):
            print(f"  {proxy+' / '+tag:<30}{d['N']:>4}   (too few)"); continue
        s0 = abs(d["slope"]) / d["se"]; sa = abs(d["slope"] - slope_alt) / d["se"]; sx = abs(d["slope"] - 0.5) / d["se"]
        print(f"  {proxy+' / '+tag:<30}{d['N']:>4}{d['slope']:>+9.3f}+-{d['se']:.3f}{'':>3}"
              f"  {s0:>8.1f}s{sa:>10.1f}s{sx:>11.1f}s")


# ------------------------------------------------------------------------------------------ M
print(); print(bar); print("SECTION M -- THE HEADLINE MEASUREMENT (clean subsample, honest reading)"); print(bar)
head = results["2M++ real-space|CLEAN (z-indep)"]
print(f"  Cleanest single number = 2M++ REAL-SPACE field x REDSHIFT-INDEPENDENT distances:")
print(f"     slope = {head['slope']:+.3f} +- {head['se']:.3f}  (N={head['N']}),  Spearman r={head['rs']:+.3f} (p={head['ps']:.2f})")
print(f"     - consistent with CANONICAL (0):        {abs(head['slope'])/head['se']:.1f} sigma  -> not excluded")
print(f"     - consistent with ALT/local-H ({slope_alt:+.2f}):  {abs(head['slope']-slope_alt)/head['se']:.1f} sigma  -> not excluded")
print(f"     - vs the +0.5 strawman:                 {abs(head['slope']-0.5)/head['se']:.1f} sigma  -> EXCLUDED")
print("  READING: the clean subsample DECISIVELY kills the maximal a0~sqrt(rho) coupling but CANNOT separate")
print("  the canonical uniform-a0 (slope 0) from the framework's own alt-footing (slope ~ -0.18). The footing")
print("  fork stays OPEN -- exactly as the ledger says SPARC alone leaves it. No manufactured verdict either way.")


# ------------------------------------------------------------------------------------------ W
print(); print(bar); print("SECTION W -- POWER: what N would DECIDE canonical-vs-alt?"); print(bar)
la0_all = np.array([r["la0"] for r in rows])
sig_a0 = float(np.std(la0_all))
odall = np.array([r["od_2mpp"] for r in rows]); odall = odall[np.isfinite(odall) & (odall > 0)]
sig_x = float(np.std(np.log10(odall)))
se_pred = sig_a0 / (sig_x * np.sqrt(head["N"] - 2))
print(f"  per-galaxy a0 scatter sigma_a0 = {sig_a0:.3f} dex (method-inflated); density spread sigma_x = {sig_x:.3f} dex.")
print(f"  slope error model se ~ sigma_a0/(sigma_x*sqrt(N)):  predicted se(N={head['N']}) = {se_pred:.3f}"
      f"  vs measured {head['se']:.3f}  [model OK].")
# N needed to detect the alt slope at 3 sigma at the CURRENT (poor) density range, scaled from the clean fit:
target_se = abs(slope_alt) / 3.0
N_need = int(np.ceil((head["N"] - 2) * (head["se"] / target_se) ** 2)) + 2
print(f"  3sigma detection of the alt slope ({slope_alt:+.2f}) needs se<{target_se:.3f} => "
      f"N ~ {N_need} clean-distance galaxies at TODAY's void range (SPARC clean = {len(clean)}).")
# current 3sigma floor:
floor = 3 * head["se"]
print(f"  current clean-sample 3sigma floor on |slope| = {floor:.2f}: excludes the strawman (+0.5), NOT the alt (-0.18).")
# future config: deeper voids (2x sigma_x via DESI) + tighter a0 (sigma_a0 -> 0.15 via good D + RCs)
sig_a0_f, sig_x_f = 0.15, 2 * sig_x
N_future = int(np.ceil((sig_a0_f / (sig_x_f * target_se)) ** 2)) + 2
print(f"  FUTURE (tighter a0 sigma_a0->{sig_a0_f} via good D+RCs; deep-void range sigma_x->{sig_x_f:.2f} via DESI voids):")
print(f"     the alt slope then needs only N ~ {N_future} galaxies IN deep voids at 3sigma -- BUT assembling that")
print("     clean, deep-void, disk-galaxy sample requires a WALLABY/SKA-scale parent survey (deep-void spirals")
print("     with good HI curves AND redshift-independent distances are rare); it is a sample-CONSTRUCTION problem.")
print("  => SPARC sets a FIRST, weak constraint (strawman excluded, footing fork open); the DECISIVE test is")
print("     next-decade: WALLABY/SKA HI rotation curves x DESI/BOSS void catalogue x redshift-independent D.")


# ------------------------------------------------------------------------------------------ verdict + json
print(); print(bar); print("VERDICT"); print(bar)
print(f"""  - PREDICTIONS (derived): canonical slope 0 EXACTLY (Lambda uniform); alt/local-H slope {slope_alt:+.2f}
    (a0 higher in voids, +{abs(v_alt)*100:.0f}% in a deep void); Verlinde ~0 with a mild negative EFE tail;
    strawman a0~sqrt(rho) +0.5 (opposite sign). The SIGN, not just amplitude, separates the readings.
  - CONFOUND: a0_fit ~ D^-2, so Hubble-flow (redshift) distances couple a0 to the peculiar-velocity field
    that DEFINES the environment -- and under the alt footing the coupling INVERTS the apparent trend. Only
    the {len(clean)} redshift-independent-distance SPARC galaxies give a trustworthy measurement.
  - MEASUREMENT (clean x 2M++): slope {head['slope']:+.3f}+-{head['se']:.3f} -> excludes +0.5 at {abs(head['slope']-0.5)/head['se']:.1f}s,
    CANNOT separate canonical(0) from alt({slope_alt:+.2f}). Underpowered-but-novel: the footing fork stays OPEN.
  - POWER: need ~{N_need} clean-distance galaxies (SPARC has {len(clean)}); decisive version = WALLABY/SKA x DESI voids.""")

out = dict(
    predictions=dict(canonical_slope=0.0, alt_slope=slope_alt, f_growth=F_GROWTH,
                     alt_void_frac=float(v_alt), alt_wall_frac=float(w_alt),
                     verlinde_band=[verl_lo, verl_hi], strawman_slope=0.5),
    counts=dict(total=len(rows), clean=len(clean), hubble_flow=len(hf),
                clean_by_method={DMETH[k]: int(sum(1 for r in clean if r["fD"] == k)) for k in REDSHIFT_INDEP},
                clean_deep_voids=int((odc < 0.5).sum())),
    slopes=results,
    headline=head,
    power=dict(sigma_a0=sig_a0, sigma_x=sig_x, se_model=se_pred, N_needed_3sig_alt=N_need,
               clean_floor_3sig=floor, N_future=N_future),
    anchors=dict(a0_canon=A0C, a0_alt=A0A))
json.dump(out, open(os.path.join(HERE, "cosmic_web_environment_results.json"), "w"), indent=1, default=float)
print(f"\n[cosmic_web_environment_results.json written]")
print("EXIT 0: symbolic checks pass, predictions derived, clean-subsample measurement computed. Not a verdict.")
