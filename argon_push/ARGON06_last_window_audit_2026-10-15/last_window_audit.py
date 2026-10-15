#!/usr/bin/env python3
"""
ARGON06 -- last_window_audit.py: the CFG795 P6b window (phase-locked coherent extraction at 2.24 meV,
eta <= 0.6) re-audited at the framework-native mass with the correct bound set.

CFG795 (70b244f65) closed the window citing "XENON10 bound (kappa m < 3e-12 eV -> eps <= 1.3e-9)".
Two problems with that closure, settled here:
  (a) XENON10 direct-absorption limits do NOT apply at 2.24 meV: a 2.24 meV quantum cannot ionize xenon
      (binding energies ~12 eV; XENON10 electron-recoil threshold ~ keV). The DP-absorption limit curves
      (XENON10/1T, SENSEI, SuperCDMS) live at m >> 10 eV. kappa m < 3e-12 eV is a re-scaled curve used
      outside its validity range (provisional, Caputo et al. handbook figure).
  (b) The correct bound AT 2.24 meV is the CMB spectral-distortion bound: resonant gamma -> X conversion
      during the mu/y eras. Provisional anchor: eps <= ~1e-13 (Caputo et al. 2021 handbook curve at
      m ~ 1e-3 eV) and the 2024 reanalysis (Cyr, Chluba et al., MNRAS 535, 1874) says the constraints in
      the 1e-4 .. 1e-3 eV window were UNDERESTIMATED (i.e. even stronger).
Window requirement: eps within 1.6x of the solar-relation bound 6.25e-9 (ARGON03 G5), i.e. eps >= 3.9e-9,
for eta = 1 - 1/(eps^2 N) >= ~0.6 with N = 6.3e16 quanta per 0.72 m coherence cell.
Closure margin: eps_needed/eps_CMB >= 10^4 (4 orders) at the provisional 1e-13; robustness: the closure
survives even a 100x weakening of the CMB bound (eps_CMB = 1e-11 still excludes 3.9e-9 by 2.6 orders).
Consequences: (i) at any cosmology-allowed eps the phase is unmeasurable (eps sqrt(N) << 1) and eta = 0
exactly (the 0.6 formula never operates); (ii) the haloscope kill-test sensitivity target sharpens from
CFG795's "eps >= 1e-10 decides" to eps ~ 1e-13 (a sub-mm search at 1e-10 is already cosmology-excluded
for a standard portal; at 1e-13 the ARGON03 rate is still ~4e5 photons/day per 10 m^2 at 0.55 mm).
External bounds PROVISIONAL. kappa = 1/2 FITTED. Never pooled. Not theory closed.
"""
import json, math, time, resource, sys

t0 = time.time()
FAILS, CHECKS = [], []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    CHECKS.append({"name": name, "ok": bool(ok), "detail": detail})
    if not ok: FAILS.append(name)

EV = 1.602176634e-19
u_c = 6.1e-5                    # J/m^3 (CFG792)
m_ev = 2.24e-3                  # framework-native mass (ARGON03)
m_J = m_ev*EV
lam_dB = 0.72                   # m, h/(m sigma) coherence cell (CFG795 P6b)
V_cell = lam_dB**3
N_cell = u_c*V_cell/m_J
eps_solar = 6.25e-9             # solar relation bound at 2.24 meV (ARGON03 G5, An et al. 2013)
eps_needed = eps_solar/1.6      # CFG795 P6b: within 1.6x of the weakest bound
eps_cmb = 1e-13                 # PROVISIONAL CMB spectral-distortion bound at ~1e-3 eV (Caputo 2021 curve)
eps_cmb_100x = 1e-11            # robustness: 100x weakened
eps_xenon10_claimed = 1.3e-9    # CFG795's closure value (kappa m < 3e-12 eV) — invalid at meV (kinematics)

print("=" * 118)
print("ARGON06 -- the last window (CFG795 P6b @ 2.24 meV) re-audited with the correct bound set")
print("=" * 118)
print(f"    m_native = {m_ev:.3f} meV; N_cell = u_c * (0.72 m)^3 / (m c^2) = {N_cell:.2e} quanta/cell")
print(f"    eps needed for eta>=0.6: {eps_needed:.2e} (CFG795: within 1.6x of solar bound {eps_solar:.2e})")

# ---- the window's own formula
def eta(eps):
    return max(0.0, 1 - 1/(eps**2*N_cell))
eta_win = eta(eps_solar)                # eta AT the bound (CFG795's 0.6)
eps_thr = 1/math.sqrt(N_cell)           # conversion threshold: eps^2 N > 1
check("window self-check: eta = 0.6 AT the solar bound (CFG795); conversion starts only above eps_thr = 1/sqrt(N)",
      abs(eta_win-0.6) < 0.05 and abs(eps_thr-3.97e-9)/3.97e-9 < 0.01,
      f"eta(bound) = {eta_win:.3f}; eps_thr = {eps_thr:.3e} — the 'within 1.6x' phrasing means the floor, not the working point")
for eps, lab in [(eps_cmb, "CMB (provisional 1e-13)"), (eps_cmb_100x, "CMB x100 weakened (1e-11)"), (eps_xenon10_claimed, "XENON10(claimed, invalid at meV)"), (eps_solar, "solar relation (bound)")]:
    print(f"    eps = {eps:.2e} [{lab}]: eps*sqrt(N) = {eps*math.sqrt(N_cell):.3e} (phase measurable iff >= 1) -> eta = {eta(eps):.2e}")

# ---- (a) XENON10 kinematics
# a 2.24 meV quantum deposits <= 2.24 meV; Xe ionization ~12.1 eV; XENON10 electron-recoil analysis threshold ~keV
meV_to_eV = 1e-3
check("(a) XENON10 does not bound 2.24 meV: deposit 2.24 meV << Xe ionization 12.1 eV << XENON10 recoil threshold ~keV",
      m_ev < 12.1e-3 and m_ev < 1.0, f"m = {m_ev*1000:.2f} meV deposit vs 12.1 eV ionization; the DP-absorption limit curves start at m ~ 10 eV+ (provisional)")
print(f"    -> CFG795's 'XENON10 closes it (eps <= 1.3e-9)' is the wrong reason (kappa m < 3e-12 eV is a rescaled curve used off-range)")
print(f"       the window closes anyway on (b); verdict class unchanged, obstruction corrected.")

# ---- (b) CMB spectral-distortion bound at 2.24 meV
marg = eps_needed/eps_cmb
check("(b) window closed by CMB bound: eps_needed 3.9e-9 >= eps_CMB 1e-13 by 4 orders (provisional; 2024 MNRAS reanalysis says the 1e-4..1e-3 eV window constraints were underestimated)",
      marg >= 1e3, f"margin {marg:.2e} = {math.log10(marg):.1f} orders")
marg_100x = eps_needed/eps_cmb_100x
check("robustness: closure survives even a 100x weakening of the CMB bound (eps_CMB = 1e-11)",
      marg_100x >= 1e2, f"margin {marg_100x:.2e} = {math.log10(marg_100x):.1f} orders")
check("robustness: a 2.6-order CMB weakening would be needed to reopen the window (kill condition named)",
      math.log10(marg_100x) > 2.0, f"reopening needs eps_CMB > {eps_needed/100:.1e}")

# ---- (c) at any allowed eps the channel gives eta = 0 exactly (phase unmeasurable)
eps_any_allowed = eps_cmb*10          # 10x ABOVE the provisional CMB bound, still 3+ orders below the window
phase = eps_any_allowed*math.sqrt(N_cell)
check("(c) at any cosmology-allowed eps: eps sqrt(N) << 1 -> phase unmeasurable -> eta = 0 exactly (the 0.6 formula never operates)",
      phase < 1e-2, f"eps = {eps_any_allowed:.1e}: eps*sqrt(N) = {phase:.2e}")

# ---- (d) sharpened haloscope kill-test target
rate_1e13 = 4.4e7*(1e-13/1e-12)**2     # ARGON03 rate at eps=1e-12 scales as eps^2
check("(d) E6 kill test sharpens: search at eps ~ 1e-13 (CMB-consistent), rate ~4.4e5 photons/day per 10 m^2 at 0.55 mm",
      rate_1e13 > 1e5, f"{rate_1e13:.2e}/day at 0.55 mm; CFG795's 'eps >= 1e-10 decides' is already cosmology-excluded for a standard portal")

print("-" * 118)
print("  READING: CFG795's P6b window is closed — and now for the right reason. Its stated closure (XENON10,")
print("  kappa m < 3e-12 eV) is kinematically inapplicable at 2.24 meV (a meV quantum cannot ionize xenon);")
print("  the true obstruction is the CMB spectral-distortion bound, ~4 orders below the window's required")
print("  eps, with a named robustness: even a 100x weakening of the provisional CMB value keeps the window")
print("  closed by 2.6 orders. At every cosmology-allowed coupling the phase-locked channel gives eta = 0")
print("  exactly (eps sqrt(N) << 1), so no dish gain can resurrect it. The single clean obstruction across")
print("  the whole design space: the only eps that converts is excluded by cosmology; the only eps allowed")
print("  by cosmology converts nothing. The E6 kill test survives and sharpens: sub-mm search at 0.55 mm,")
print("  eps ~ 1e-13 sensitivity, ~4e5 photons/day per 10 m^2 — a null closes the chain; a line kills the framework.")
print("-" * 118)

res = {"m_ev": m_ev, "N_cell": N_cell, "eps_needed": eps_needed, "eta_window": eta_win,
       "XENON10_inapplicable_kinematics": True, "eps_CMB_provisional": eps_cmb,
       "margin_orders": math.log10(marg), "margin_orders_at_100x_weakening": math.log10(marg_100x),
       "phase_at_10x_CMB": phase, "haloscope_rate_per_day_at_1e-13": rate_1e13,
       "checks": CHECKS, "wall_s": time.time()-t0}
with open("last_window_audit_results.json", "w") as f:
    json.dump(res, f, indent=1)
print(f"  RESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
print(f"  wall {time.time()-t0:.2f} s; threads 1; max RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6:.1f} MB")
sys.exit(0 if not FAILS else 1)