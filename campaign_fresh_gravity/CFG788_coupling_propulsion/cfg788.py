"""CFG788 -- cold-energy coupling window and propulsion ceiling (criteria FROZEN_CRITERIA.md, a47848e67).  Analytic; seconds.
Run after T1x: python3 cfg788.py   (CFG788_MUTATE=1: stiffness off).  Experimental limits PROVISIONAL (from memory).
kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG788_MUTATE") == "1"
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
GM, PC, YR, C = 1.32712440018e20, 3.0857e16, 3.156e7, 2.998e8
A1 = 3e-15 * 9.8 * 0.8          # MICROSCOPE differential acceleration ceiling
A2 = 1e-15                      # Eot-Wash galactic-source differential ceiling
A3 = 3.66e-14                   # ephemeris sunward ceiling (composition-independent)
amax_diff, amax_univ = min(A1, A2), A3
P("CFG788  cold-energy coupling window and propulsion ceiling" + ("  [MUTATE stiffness off]" if MUT else ""))
P(f"  A: MICROSCOPE {A1:.1e}, Eot-Wash galactic {A2:.1e}, ephemeris (universal) {A3:.1e} m/s^2")
P(f"     ceiling for a composition-dependent (engineerable) coupling: {amax_diff:.1e}; universal coupling: {amax_univ:.1e}")
res = {}
for lab, a in (("composition-dependent", amax_diff), ("universal", amax_univ)):
    t = {dv: dv / a / YR for dv in (1.0, 1e3, 0.01 * C)}
    res[lab] = dict(a=a, years=t, thrust_N_1t=a * 1000)
    P(f"  B {lab:22s}: a {a:.1e} m/s^2 -> 1 m/s in {t[1.0]:.2e} yr, 1 km/s in {t[1e3]:.2e} yr, 0.01c in {t[0.01*C]:.2e} yr; thrust on 1 t {a*1000:.1e} N")
P(f"     (sunlight on 1 m^2 per tonne at 1 AU: {4.56e-6/1000:.1e} m/s^2)")
K1 = GM / (5.75 * PC) ** 2
P(f"  K1 zero coupling: framework residual G M_sun / L*^2 = {K1:.2e} m/s^2 (CFG770/774: 4.2e-15)")
# C: P exhaust. Stiffness screening length in the Solar background (CFG770): lambda_e ~ 2.1-2.4 pc
lam = 0.0 if MUT else 2.2 * PC
for r in (1.0, 10.0):
    supp = (r / lam) ** 2 if lam > 0 else 1.0
    P(f"  C device r = {r:g} m: coupling to P suppressed by (r/lambda_e)^2 = {supp:.1e}" + (" (stiffness off: unscreened)" if MUT else ""))
# a 1 kg mass oscillating at 1 kHz with 1 mm amplitude: max gravitational-type momentum transfer to P ~ m * a_source * supp
m, f, A = 1.0, 1e3, 1e-3
asrc = A * (2 * math.pi * f) ** 2
pdot = m * asrc * ((1.0 / lam) ** 2 if lam > 0 else 1.0)
P(f"     1 kg at 1 kHz, 1 mm (source acceleration {asrc:.1e} m/s^2): screened momentum coupling ~ {pdot:.1e} N (upper bound, order of magnitude)")
P("  Symmetry theorem: a source invariant under SO(3) in a uniform background has zero net self-force (all dipole moments vanish); propulsion requires a dipole asymmetry.")
cls = "NO PRACTICAL PROPULSION" if max(amax_diff, amax_univ) <= 1e-12 else "WINDOW"
exhaust = "P EXHAUST CLOSED" if (not MUT and pdot < 1e-20) else "P EXHAUST OPEN/UNSCREENED (mutate)" if MUT else "P EXHAUST OPEN"
P(f"\n  CLASS: {cls}; {exhaust}")
json.dump(dict(cls=cls, exhaust=exhaust, res=res, K1=K1, pdot=pdot, mutate=MUT), open(os.path.join(HERE, f"cfg788_results{'_MUTATE' if MUT else ''}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg788{'_MUTATE' if MUT else ''}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else 0)
