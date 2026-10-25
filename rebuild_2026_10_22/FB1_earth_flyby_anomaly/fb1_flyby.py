"""FB1_earth_flyby_anomaly (criteria FROZEN_CRITERIA.md, commit b7871a1296).

The framework's prediction for the Earth flyby anomaly vs Anderson et al. 2008 (PRL 100, 091102) Table I.
Readings: R-S screened theory (hedgehog GM/L*^2 inside L*), R-M nu_mono (unscreened, verdict kernel),
R-1 unscreened AQUAL nu1 (reported only; Cassini-dead per E2).
MUTATE (FB1_MUTATE=1 or --mutate): prediction = Anderson's empirical formula; the grader must return FB EXPLAINS.
kappa = 1/2 FITTED; footings never pooled; cold dark energy, not matter; not theory closed.
"""
import json
import math
import os
import sys

MUTATE = os.environ.get("FB1_MUTATE") == "1" or "--mutate" in sys.argv
TAG = "_MUTATE" if MUTATE else ""
HERE = os.path.dirname(os.path.abspath(__file__))

G = 6.67430e-11
GM_E = 3.986004418e14
GM_S = 1.32712440018e20
AU = 1.495978707e11
PC = 3.0856775814913673e16
R_E = 6.3781e6
OMEGA_E = 7.2921159e-5
C = 299792458.0
A0_SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LSTAR_PC = (24.0, 28.9, 90.0)
T_ARC = 2.0e6            # s, bound window (frozen)
R_REGION = 1.0e9         # m, flyby region for the Sun's tidal hedgehog term (frozen)
K_AND = 2 * OMEGA_E * R_E / C

# Anderson et al. 2008 Table I: name, v_inf (km/s), perigee altitude (km), delta_in, delta_out (deg), dv (mm/s), sigma (mm/s)
TABLE = [
    ("Galileo I 1990", 8.949, 960, -12.52, -34.15, 3.92, 0.3),
    ("Galileo II 1992", 8.877, 303, -34.26, -4.87, -4.6, 1.0),
    ("NEAR 1998", 6.851, 539, -20.76, -71.96, 13.46, 0.01),
    ("Cassini 1999", 16.010, 1175, -12.92, -4.99, -2.0, 1.0),
    ("Rosetta 2005", 3.863, 1956, -2.81, -34.29, 1.80, 0.03),
    ("MESSENGER 2005", 4.056, 2347, 31.44, -31.92, 0.02, 0.01),
]
POST_NULLS = ["Rosetta II 2007", "Rosetta III 2009", "Juno 2013"]

out_lines = []


def P(s=""):
    print(s)
    out_lines.append(s)


def anderson_mm(row):
    _, v, _, din, dout, _, _ = row
    return K_AND * v * 1e3 * (math.cos(math.radians(din)) - math.cos(math.radians(dout))) * 1e3


def log10_nu_mono_minus1(y):
    # nu - 1 = 1/(e^sqrt(y) - 1); for large y, log10 = -sqrt(y)/ln10 - log10(1 - e^-sqrt(y))
    s = math.sqrt(y)
    return -s / math.log(10) - math.log10(-math.expm1(-s))


def grade(pred_mm, bound_mm):
    """pred_mm: list of predicted dv per flyby (mm/s); bound_mm: max |dv| bound (mm/s)."""
    within = [abs(p - r[5]) <= 2 * r[6] for p, r in zip(pred_mm, TABLE)]
    if all(within):
        return "FB EXPLAINS", within
    if bound_mm < 1e-3 * 0.01:
        return "FB SILENT (= GR)", within
    return "FB CONFLICTS", within


P("FB1_earth_flyby_anomaly" + (" [MUTATE: Anderson formula injected]" if MUTATE else ""))
P(f"Anderson K = 2 omega R/c = {K_AND:.4e}")

# K0 transcription check
k0 = []
for r in TABLE:
    a = anderson_mm(r)
    ok = abs(a - r[5]) <= max(3 * r[6], 0.6)
    k0.append(ok)
    P(f"  K0 {r[0]:16s} obs {r[5]:+7.2f} +- {r[6]:.2f}  Anderson {a:+7.2f}  {'ok' if ok else 'off'}")
K0 = sum(k0) >= 5
P(f"K0 transcription: {sum(k0)}/6 within tolerance -> {'PASS' if K0 else 'FAIL (stop)'}")
if not K0:
    sys.exit(2)

results = {"mutate": MUTATE, "K_anderson": K_AND, "K0_pass_count": sum(k0), "footings": {}}
r_min = min(R_E + r[2] * 1e3 for r in TABLE)
g_sun_1au = GM_S / AU ** 2

# K1
L24 = 24.0 * PC
hedge_E24 = GM_E / L24 ** 2
K1 = abs(hedge_E24 * L24 ** 2 / GM_E - 1) < 1e-12
P(f"K1 Earth hedgehog at 24 pc = {hedge_E24:.3e} m/s^2 -> {'PASS' if K1 else 'FAIL'}")

for foot, a0 in A0_SI.items():
    P(f"\n=== footing {foot}: a0 = {a0:.4e} m/s^2 ===")
    fr = {}
    # R-S screened
    rs = {}
    for Lpc in LSTAR_PC:
        L = Lpc * PC
        hedge_E = GM_E / L ** 2
        hedge_S = GM_S / L ** 2
        tidal_S = 2 * hedge_S * R_REGION / AU      # gradient of a constant-magnitude radial field ~ 2 g/r (upper)
        dg = hedge_E + tidal_S
        bound_mm = dg * T_ARC * 1e3
        rs[str(Lpc)] = {"hedge_E": hedge_E, "hedge_S_at_1AU": hedge_S, "tidal_S": tidal_S, "max_dg": dg,
                        "bound_mm_s": bound_mm}
        P(f"  R-S L*={Lpc:5.1f} pc: Earth hedgehog {hedge_E:.2e}, Sun hedgehog {hedge_S:.2e} (tidal {tidal_S:.2e}) "
          f"-> |dv| <= {bound_mm:.2e} mm/s (exact static-central value 0)")
    worst_bound = max(v["bound_mm_s"] for v in rs.values())
    pred = [anderson_mm(r) for r in TABLE] if MUTATE else [0.0] * len(TABLE)
    cls, within = grade(pred, worst_bound if not MUTATE else 1.0)
    fr["R-S"] = {"per_Lstar": rs, "worst_bound_mm_s": worst_bound, "pred_mm_s": pred, "within_2sigma": within,
                 "class": cls}
    P(f"  R-S class: {cls}")
    # R-M nu_mono: smallest y anywhere on the flyby = total field >= g_sun(1AU) - tiny; use g_sun(1AU) (most permissive)
    y_min = g_sun_1au / a0
    l10 = log10_nu_mono_minus1(y_min)
    l10_bound = l10 + math.log10(g_sun_1au * T_ARC * 1e3)
    fr["R-M"] = {"y_min": y_min, "log10_nu_minus1": l10, "log10_bound_mm_s": l10_bound,
                 "class": "FB SILENT (= GR)" if l10_bound < math.log10(1e-5) else "FB CONFLICTS"}
    P(f"  R-M nu_mono: y_min = {y_min:.3e}, log10(nu-1) = {l10:.1f}, log10 |dv| bound = {l10_bound:.1f} mm/s "
      f"-> {fr['R-M']['class']}")
    # R-1 unscreened AQUAL nu1: delta g ~ a0 (y >> 1), reported only
    b1 = a0 * T_ARC * 1e3
    fr["R-1"] = {"bound_mm_s": b1, "note": "reported only; Cassini-dead (E2)"}
    P(f"  R-1 nu1 (reported only, Cassini-dead): |dg| ~ a0 -> |dv| <= {b1:.2f} mm/s; a near-uniform field, no omega_E term")
    results["footings"][foot] = fr

classes = {f: results["footings"][f]["R-S"]["class"] for f in A0_SI}
verdict = classes["canonical"] if classes["canonical"] == classes["alt"] else "UNDECIDED"
results["verdict"] = verdict
results["needed_vs_supplied"] = {
    "NEAR_needed_mm_s": 13.46,
    "R-S_worst_bound_mm_s": max(results["footings"][f]["R-S"]["worst_bound_mm_s"] for f in A0_SI),
}
results["post_2008_nulls_reported"] = POST_NULLS
P(f"\nVERDICT (primary R-S, both footings): {verdict}")
P(f"NEAR needs 13.46 mm/s; screened framework supplies <= {results['needed_vs_supplied']['R-S_worst_bound_mm_s']:.1e} mm/s.")
P("Anderson's K = 2 omega_E R_E / c needs a coupling to Earth's spin; no framework reading has one (all are static, "
  "spherically symmetric about each body).")
P(f"Post-2008 flybys with no anomaly (reported): {', '.join(POST_NULLS)}")

with open(os.path.join(HERE, f"fb1_flyby_results{TAG}.json"), "w") as f:
    json.dump(results, f, indent=1)
with open(os.path.join(HERE, f"fb1_flyby{TAG}.out"), "w") as f:
    f.write("\n".join(out_lines) + "\n")

if MUTATE:
    ok = all(results["footings"][ft]["R-S"]["class"] == "FB EXPLAINS" for ft in A0_SI)
    P(f"MUTATE: grader returned FB EXPLAINS for the injected formula: {ok}")
    sys.exit(1 if ok else 0)
