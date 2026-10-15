"""CFG795 -- converter design space for the hypothetical cold-energy photon ramjet.  Criteria: FROZEN_CRITERIA.md (2be9ffbb1).
Run: nice python3 cfg795.py   (CFG795_MUTATE=1: rho_c -> 0, separate outputs, exit 1 by design).  Seconds, numpy only.
External bounds quoted from memory / web summaries: PROVISIONAL.  kappa = 1/2 FITTED; not theory closed.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG795_MUTATE") == "1"
OUT = []


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


c, G, MSUN, PC, YR, EV = 2.99792458e8, 6.674e-11, 1.989e30, 3.0857e16, 3.156e7, 1.602e-19
RHO = 0.0 if MUT else 0.01 * MSUN / PC ** 3
U0 = RHO * c ** 2
V0 = 2.3e5
F0 = U0 * V0                                  # W/m^2 intercepted at rest
SIG = 1e-6                                    # kg/m^2 reference intake (graphene, CFG791 D1)
ETA_T = 0.01
LSTAR = 5.75 * PC
R_E, R_CORE, R_MOON = 6.371e6, 3.48e6, 1.737e6
HEAT_E = 47e12
NIGHT = 1e-3                                  # lux, moonless night sky
LM = 93.0                                     # lm/W (CFG792)
R = {"lane": "CFG795", "mutate": MUT, "rho": RHO, "flux_W_m2": F0}
P("CFG795  converter design space (hypothetical cold-energy ramjet)" + ("  [MUTATE rho_c=0]" if MUT else ""))
P(f"  rho c^2 {U0:.3e} J/m^3; flux rho c^2 v0 {F0:.2f} W/m^2; intake 1 mg/m^2; target eta >= {ETA_T}")


def tau0_days(eta):
    return SIG / (eta * RHO * c) / 86400 if (eta > 0 and RHO > 0) else float("inf")


def frac_max(excess):                         # allowed natural conversion fraction given full-conversion excess
    return min(1.0, 1.0 / excess) if excess > 0 else 1.0


# ---- controls (CFG792) ----
lux_full = F0 / 4 / 2 * LM
x_sky = lux_full / NIGHT
x_heat = F0 * np.pi * R_E ** 2 / HEAT_E
k1 = MUT or abs(lux_full / 160 - 1) < 0.05
k2 = MUT or abs(x_heat / 38 - 1) < 0.05
P(f"  K1 ground light (full conversion) {lux_full:.1f} lux vs CFG792 160: {'PASS' if k1 else 'FAIL'}")
P(f"  K2 Earth interception {x_heat:.1f} x 47 TW vs CFG792 38: {'PASS' if k2 else 'FAIL'}")
R.update(K1=dict(lux=lux_full, ok=bool(k1)), K2=dict(x_heat=x_heat, ok=bool(k2)))

rows = []
k_dev = -np.log(1 - ETA_T) / SIG              # per-mass rate a 1 mg/m^2 sheet needs for eta 0.01


def add(cls, eta, note, off=None, on=None):
    rows.append(dict(cls=cls, eta_max=float(eta), tau0_d=tau0_days(eta), note=note, off_needed=off, on_needed=on))


# ---- P1 per-mass ----
col_atm = 1.03e4
col_earth = 4 / 3 * R_E * 5514.0
col_moon = 4 / 3 * R_MOON * 3344.0
x_moon = (F0 / 4) / 0.020
kP1 = {"night sky (whole atmosphere)": frac_max(x_sky) / col_atm,
       "Earth heat flow": frac_max(x_heat) / col_earth,
       "Moon heat flow": frac_max(x_moon) / col_moon}
kmax1 = min(kP1.values()) if RHO else float("inf")
eta1 = -np.expm1(-kmax1 * SIG) if np.isfinite(kmax1) else 1.0
P("\nP1 per-mass portal (nucleons / bound electrons)")
for kk, v in kP1.items():
    P(f"   {kk:30s}: k <= {v:.2e} m^2/kg")
P(f"   eta(1 mg/m^2) <= {eta1:.1e}; needs natural-matter 'off' factor {k_dev / kmax1:.1e}; ramjet figure of merit"
  f" tau0 >= 1/(k rho c) = {1 / (kmax1 * RHO * c) / YR if RHO else float('inf'):.1e} yr for ANY areal mass")
add("P1 per-mass", eta1, "Earth heat flow", off=k_dev / kmax1)
R["P1"] = dict(k=kP1, eta=eta1)

# ---- P2 free electrons ----
n_core = 1.1e4 / (56 * 1.6605e-27) * 1.5
col_core = 4 / 3 * R_CORE * n_core
x_core = F0 * np.pi * R_CORE ** 2 / HEAT_E
k_core = frac_max(x_core) / col_core
k_iono = frac_max(x_sky) / 1e17
k2max = min(k_core, k_iono) if RHO else float("inf")
col_foil = SIG / (26.98 * 1.6605e-27) * 3
eta2 = -np.expm1(-k2max * col_foil) if np.isfinite(k2max) else 1.0
P("\nP2 free-electron portal")
P(f"   core column {col_core:.1e} e/m^2 (excess x{x_core:.1f}) -> k <= {k_core:.1e} m^2; ionosphere k <= {k_iono:.1e} m^2")
P(f"   1 mg/m^2 Al foil ({col_foil:.1e} e/m^2): eta <= {eta2:.1e}; 'off' factor needed {0.01 / eta2:.1e}")
add("P2 free electrons", eta2, "Earth core heat", off=0.01 / eta2)
R["P2"] = dict(k_core=k_core, k_iono=k_iono, eta=eta2)

# ---- P3 axion-like, P4 kinetic mixing (dish formula x engineered gain) ----
TESLA, GAIN, CV = 1.9535e-16, 1e6, c / V0
P(f"\nP3/P4 coherent-field portals, dish formula x engineered gain G <= {GAIN:.0e} (c/v0 = {CV:.0f})")
for m_eV, lab in ((2.4, "CFG790 line 2.4 eV"), (2.24e-3, "native 2.24 meV")):
    m = m_eV * 1e-9
    e3 = GAIN * (6.6e-11 * 1e3 * TESLA / m) ** 2 * CV
    P(f"   P3 {lab}: g 6.6e-11/GeV, B 1e3 T -> eta <= {e3:.1e}")
    add(f"P3 axion-like, {lab}", e3, "CAST/HB g, B 1e3 T, G 1e6", on=ETA_T / e3)
    eps = 1e-14 if m_eV > 1 else 6.25e-9
    e4 = GAIN * eps ** 2 * CV
    P(f"   P4 {lab}: eps <= {eps:.2e} -> eta <= {e4:.1e} (bare dish {eps ** 2 * CV:.1e})")
    add(f"P4 kinetic mixing, {lab}", e4, f"eps {eps:.0e}, G 1e6", on=ETA_T / e4)

# ---- P5 superconductor-gated ----
A_sn, dcr, fabs = 1e-8, 1e-5, 0.1
eta5 = min(1.0, dcr * 1.0 * EV / (F0 * A_sn * fabs)) if RHO else 1.0
M_ns, R_ns = 1.4 * MSUN, 1.2e4
P_ns = np.pi * R_ns ** 2 * (1 + 2 * G * M_ns / (R_ns * V0 ** 2)) * RHO * V0 * c ** 2
T_ns = (P_ns / (4 * np.pi * R_ns ** 2 * 5.670e-8)) ** 0.25
P("\nP5 superconductor / condensate-gated")
P(f"   neutron star full conversion: {P_ns:.1e} W -> T {T_ns:.0f} K vs coldest limits ~4e4 K: NOT constraining")
P(f"   SNSPD film (1e-8 m^2, 1e-5 Hz dark, 10% absorbed, 1 eV): eta <= {eta5:.1e}")
add("P5 superconductor-gated", eta5, "SNSPD dark counts", on=ETA_T / eta5)
R["P5"] = dict(P_ns=P_ns, T_ns=T_ns, eta=eta5)

# ---- P6 laser stimulation / phase-locked coherent extraction ----
P("\nP6a laser (Bose) stimulation without phase knowledge: net transfer ∝ (N_cold - N_mode); N_mode > N_cold REVERSES it")
add("P6a laser-stimulated (no phase)", 0.0, "detailed balance", on=float("inf"))
P("P6b phase-locked extraction (displacement nulling): needs the cold phase per coherence cell; frozen test eps*sqrt(N) >= 1")
P("    eta_lock = max(0, 1 - 1/s), s = eps^2 N (quantum-limited residual; formula set after the freeze, disclosed)")
EPS0 = 8.854e-12
R["P6"] = {}
for m_eV, eps, lab in ((2.4, 1e-14, "2.4 eV, stellar eps"), (2.24e-3, 6.25e-9, "2.24 meV, solar-relation eps"),
                       (2.24e-3, 1.34e-9, "2.24 meV, XENON10 eps (sensitivity)")):
    lam = 1239.84e-9 / m_eV * CV
    N = U0 * lam ** 3 / (m_eV * EV)
    need = 1 / np.sqrt(N) if N > 0 else float("inf")
    sF = eps ** 2 * N                                  # frozen
    sD = eps ** 2 * CV * N                             # dish geometry, bare (post-hoc refinement, looser)
    etaL = max(0.0, 1 - 1 / sF) if sF > 0 else 0.0
    E_lo = np.sqrt(2 * U0 / (EPS0 * eps ** 2)) if RHO else 0.0
    E_loG = np.sqrt(2 * U0 / (EPS0 * GAIN * eps ** 2 * CV)) if RHO else 0.0
    tc = lam / V0
    P(f"   {lab}: cell {lam:.2e} m, t_c {tc:.1e} s, N_cold {N:.1e}; eps_need {need:.1e} (allowed/need {eps / need:.2f});"
      f" s {sF:.2e} (dish-geometry s {sD:.1e}); eta_lock {etaL:.2f}; LO field {E_lo:.1e} V/m ({E_loG:.1e} with G 1e6, c/v)")
    R["P6"][lab] = dict(cell=lam, tc=tc, N=N, eps_need=need, eps=eps, s_frozen=sF, s_dish=sD, eta_lock=etaL,
                        E_LO=E_lo, E_LO_gain=E_loG)
    if m_eV > 1 or eps > 5e-9:
        add(f"P6b phase-locked, {lab}", etaL, "quantum phase noise; framework E6 kill" if etaL > 0 else "phase unmeasurable")
P(f"   a 100 km^2 intake at 2.24 meV holds {1e8 / (0.721 ** 2):.1e} cells, each re-measured every ~3 us")

# ---- P7 2-3 eV resonance ----
P(f"\nP7 2-3 eV material resonance: cold line width (v/c)^2 = {(V0 / c) ** 2:.1e}; natural bands (~0.1 eV) cover 2-3 eV -> P1 bound")
add("P7 2-3 eV resonance", eta1, "nature has the resonance (P1)", off=k_dev / kmax1)

# ---- P8 gravity only ----
ceil8 = 0.5 * (V0 / c) ** 2
Mdev, Adev = SIG * 1e8, 1e8                   # 100 km^2 at 1 mg/m^2
Pdf = 4 * np.pi * G ** 2 * Mdev ** 2 * RHO * 10 / V0
eta8 = Pdf / (F0 * Adev) if RHO else 0.0
P(f"\nP8 gravity only: kinetic ceiling (v0/c)^2/2 = {ceil8:.1e}; dynamical friction on 100 km^2 sheet: {Pdf:.1e} W -> eta {eta8:.1e}")
add("P8 gravity only", min(ceil8, eta8), f"ceiling {ceil8:.1e}; actual dyn. friction")

# ---- P9 framework screening (reading R1) ----
P(f"\nP9 framework screening (R1, cold energy = bound charge of stiff P), L* = 5.75 pc")
R["P9"] = {}
for d in (1.0, 1e4):
    s = (d / LSTAR) ** 2
    P(f"   d = {d:g} m: eta <= (d/L*)^2 = {s:.1e}")
    R["P9"][str(d)] = s
dneed = np.sqrt(ETA_T) * LSTAR
P(f"   eta 0.01 needs d >= {dneed:.2e} m = {dneed / PC:.2f} pc")
R["P9"]["d_need_pc"] = dneed / PC
s9 = (1e4 / LSTAR) ** 2

# ---- table + verdict ----
P(f"\n{'class':48s} {'eta_max':>9s} {'tau0 (1 mg/m^2)':>16s}  bound")
for r in rows:
    t = r["tau0_d"]
    ts = f"{t / 365.25:.1e} yr" if np.isfinite(t) else "inf"
    P(f"{r['cls']:48s} {r['eta_max']:9.1e} {ts:>16s}  {r['note']}")
best = max(rows, key=lambda r: r["eta_max"])
open_ = (best["eta_max"] >= ETA_T)
verdict = "WINDOW OPEN" if open_ else "CLOSED"
P(f"\nleast-constrained window (R2, portal added by hand): {best['cls']} eta_max {best['eta_max']:.1e} (eta_max/0.01 = {best['eta_max'] / ETA_T:.1e})")
nl = [r for r in rows if not r["cls"].startswith("P6b")]
b2 = max(nl, key=lambda r: r["eta_max"])
P(f"best WITHOUT phase-locked extraction: {b2['cls']} eta_max {b2['eta_max']:.1e} (short of 0.01 by x{ETA_T / b2['eta_max']:.1e})")
P("framework-native (no portal; only gravity): P8, eta ~1e-50; a visible line at 2.24 meV would be ARGON03/CFG723-E6's kill")
P(f"under R1 the framework's own screening caps a 10 km device at {s9:.1e}")
P(f"VERDICT (eta >= 0.01 anywhere): {verdict}" + (" -- ONLY outside the framework (hand-added 2.24 meV mixing near its bound);"
  " CLOSED within it (R1 screening, R2 gravity-only)" if open_ else ""))
R.update(best_without_lock=b2["cls"], best_without_lock_eta=b2["eta_max"], rows=rows, best=best["cls"], best_eta=best["eta_max"], verdict=verdict, screen_10km=s9)
if MUT:
    bite = (lux_full == 0 and x_heat == 0 and s9 == (1e4 / LSTAR) ** 2)
    P(f"MUTATE: natural excesses {lux_full:.1e}/{x_heat:.1e}, screening {s9:.1e} unchanged -> {'bites' if bite else 'DID NOT BITE'}")
    R["mutate_bites"] = bool(bite)
sfx = "_MUTATE" if MUT else ""
json.dump(R, open(os.path.join(HERE, f"cfg795_results{sfx}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg795{sfx}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else 0)
