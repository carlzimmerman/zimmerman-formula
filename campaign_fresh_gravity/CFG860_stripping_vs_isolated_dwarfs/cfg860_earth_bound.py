"""CFG860 Part E -- the Earth bound: can removing gas here (lab vessel, plant, Earth's atmosphere) set cold energy free, or make it?
Criteria: FROZEN_CRITERIA.md (219d4d5dc), Part E (E1-E7, K2).  Arithmetic only; a bound, not a test against data.
Run: python3 cfg860_earth_bound.py -> cfg860_earth_bound.out, cfg860_earth_bound.json.
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}                 # CFG828 / CFG852 values
g_E, PC, YR = 9.81, 3.0857e16, 3.15576e7                           # Earth's surface field (m/s^2); pc (m); Julian year (s)
LSTAR = 24.0 * PC                                                  # frozen: CFG820's lower edge, the largest (s/L*)^2
S = {"1 m (lab vessel)": 1.0, "1 km (plant)": 1.0e3, "6.371e6 m (Earth radius: the atmosphere)": 6.371e6}
MDOT, REF = 3.0, 1e-9                                              # E4 H escape ~3 kg/s (order of magnitude, provisional, not graded); E5 reference

def f_simple(y):
    """nu - 1 for the simple kernel nu = 1/2 + sqrt(1/4 + 1/y), in the cancellation-free form (1/y) / (sqrt(1/4 + 1/y) + 1/2)."""
    return (1.0 / y) / (math.sqrt(0.25 + 1.0 / y) + 0.5)
def log10_f_e(y):
    """log10(nu_e - 1) for nu_e = 1/(1 - e^-sqrt(y)): nu_e - 1 = 1/(e^t - 1), t = sqrt(y); log10 = -t log10(e) - log10(1 - e^-t)."""
    t = math.sqrt(y); return -t / math.log(10.0) - math.log10(-math.expm1(-t))

P("CFG860 Part E  the Earth bound (arithmetic)")
RES = dict(lane="CFG860", part="E", criteria_commit="219d4d5dc", g_earth=g_E, Lstar_pc=24.0)
P("  E1 conversion: none. The committed action conserves cold mass exactly (CFG793, eta = 0): removing gas cannot make cold energy.")
L820 = json.load(open(os.path.join(LANES, "CFG820_stiffness_from_globulars", "cfg820_results.json")))
fac = {k: (s / LSTAR) ** 2 for k, s in S.items()}
P(f"  stiffness factor (s/L*)^2 at L* = 24 pc (frozen; CFG820 L95 {L820['primary (no Pal 3)|canonical']['L95']:.2f} pc canonical / "
  f"{L820['primary (no Pal 3)|alt']['L95']:.2f} pc alt): " + ", ".join(f"{k.split(' (')[0]} {v:.3e}" for k, v in fac.items()))
E = {}
for ft, a0 in A0.items():
    y = g_E / a0; fs = f_simple(y); lfe = log10_f_e(y)
    e3 = {k: dict(simple=fs * v, log10_nu_e=lfe + math.log10(v)) for k, v in fac.items()}
    mpy = MDOT * YR; s_earth = fac["6.371e6 m (Earth radius: the atmosphere)"]
    e4 = dict(mass_lost_kg_per_yr=mpy, E2_simple_kg_per_yr=fs * mpy, E2_log10_nu_e_kg_per_yr=lfe + math.log10(mpy),
              E3_earth_simple_kg_per_yr=fs * s_earth * mpy, E3_earth_log10_nu_e_kg_per_yr=lfe + math.log10(s_earth * mpy))
    E[ft] = dict(a0=a0, y=y, E2_simple=fs, E2_simple_over_a0g=fs / (a0 / g_E), E2_log10_nu_e=lfe, E3=e3, E4=e4)
    P(f"\n  [{ft}] a0 {a0:.4e}  y = g/a0 = {y:.4e}")
    P(f"    E2 release bound (no stiffness), kg of cold energy per kg of gas: simple kernel {fs:.3e} (= {fs / (a0 / g_E):.6f} a0/g);"
      f"  nu_e: 10^{lfe:.1f}")
    for k, v in e3.items():
        P(f"    E3 with stiffness, s = {k:42s}: simple {v['simple']:.3e}   nu_e 10^{v['log10_nu_e']:.1f}")
    P(f"    E4 natural H escape ~{MDOT:.0f} kg/s = {mpy:.3e} kg/yr: freed cold mass per year  E2 simple {e4['E2_simple_kg_per_yr']:.3e} kg"
      f"  (nu_e 10^{e4['E2_log10_nu_e_kg_per_yr']:.1f});  E3 at Earth radius simple {e4['E3_earth_simple_kg_per_yr']:.3e} kg"
      f"  (nu_e 10^{e4['E3_earth_log10_nu_e_kg_per_yr']:.1f})")
RES["E"] = E
P(f"\n  E5 reference: {REF:.0e} kg per kg removed (about the relative resolution of the best mass comparators; reference only).")
P(f"     largest E2 (simple, alt) / reference = {max(E[f]['E2_simple'] for f in E) / REF:.2e}")
P("  E6 the 541.664 / 595.463 GHz line (CFG797-799) stays the only lab-scale test of the cold sector: 541.664 GHz archive NULL "
  "(eps95 1.9e-11, converter window closed x200, kill line 1e-12 not reached); 595.463 GHz frozen run INCONCLUSIVE (C2 null offsets fail; "
  "converter tier excluded 31/31; kill line not tested).")
K745 = json.load(open(os.path.join(LANES, "CFG745_hot_gas_selector", "cfg745_results.json")))
ks = [K745[ft][fr]["k"] for ft in ("canonical", "alt") for fr in ("0.85", "0.95")]; f1 = fac["1 m (lab vessel)"]
E7 = dict(k_min=min(ks), k_max=max(ks), per_kg_hot_gas_at_1m=[min(ks) * f1, max(ks) * f1])
P(f"  E7 (reported) CFG745 hot-gas term C = k M_hot, k {min(ks):.2f}-{max(ks):.2f} (fitted at galaxy scale, no mechanism): a TETHERED amount, not a conversion;"
  f" x (1 m / L*)^2 -> {E7['per_kg_hot_gas_at_1m'][0]:.2e}-{E7['per_kg_hot_gas_at_1m'][1]:.2e} kg per kg of hot gas at s = 1 m.")
RES["E7"] = E7
# K2
y = 1e4; k2 = abs(f_simple(y) - 1.0 / y) / (1.0 / y); direct = 0.5 + math.sqrt(0.25 + 1.0 / y) - 1.0
aux = abs(log10_f_e(4.0) - math.log10(1.0 / math.expm1(2.0)))
P(f"\n  K2 y = 1e4: simple f {f_simple(y):.9e} vs 1/y {1.0 / y:.9e}, relative {k2:.2e} -> {'PASS' if k2 <= 1e-3 else 'FAIL'}"
  f"  (direct-form f {direct:.9e}; aux nu_e log form at y = 4 vs direct: diff {aux:.1e})")
RES["K2"] = {"f_simple": f_simple(y), "inv_y": 1.0 / y, "rel": k2, "pass": bool(k2 <= 1e-3), "aux_nu_e_log_diff": aux}
cls = "NO LAB CHANNEL" if all(E[f]["E2_simple"] < REF for f in E) else "LAB CHANNEL OPEN"
RES["cls"] = cls; P(f"\n  CLASS: {cls}  (E2 simple-kernel bound < {REF:.0e} kg/kg on both footings: {all(E[f]['E2_simple'] < REF for f in E)})")
json.dump(RES, open(os.path.join(HERE, "cfg860_earth_bound.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg860_earth_bound.out"), "w").write("\n".join(OUT) + "\n")
