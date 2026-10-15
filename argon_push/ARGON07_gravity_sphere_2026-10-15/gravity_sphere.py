#!/usr/bin/env python3
"""
ARGON07 -- gravity_sphere.py: the 'activated sphere' idea (artificial gravity by pulling in the cold
medium) scored against the framework's own constants.

Idea (Carl): a sphere that is 'activated' and pulls in dark energy from around it, creating a
gravitational field that can push/pull in any direction.

Framework facts used (all on the record):
- the settled phantom halo: M_c(r)/M_b = (sqrt(1+4r^2/r_M^2)-1)/2, r_M = sqrt(G M_b/a0) (ARGON02);
- supply rule: M_c,tot = 5.364 M_b within r_e = 5.84 r_M;
- deep-regime field: g_ph = sqrt(G M_b a0)/r (amplitude LOCKED, no free parameter);
- stiffness screening: device-scale response suppressed by (d/L*)^2, L* >= 5.75 pc (CFG770 T2/CFG772 L2/CFG795 P9);
- no non-gravitational coupling: E6 (CFG723), built-in portal suppressed (CFG793/ARGON05), rest-mass
  conversion forbidden by continuity, any converting eps excluded by cosmology (ARGON06);
- medium dynamics: W_rem gap 7.4e-9 rad/s -> response time 1/omega_gap ~ 4.3 yr (CFG793 run).
kappa = 1/2 FITTED. Canonical a0 = 9.3603e-11 only. Not theory closed.
"""
import json, math, time, resource, sys

t0 = time.time()
FAILS, CHECKS = [], []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    CHECKS.append({"name": name, "ok": bool(ok), "detail": detail})
    if not ok: FAILS.append(name)

G = 6.67430e-11; c = 2.99792458e8
A0 = 9.3603e-11
PC = 3.085677581491367e16
LSTAR = 5.75*PC
SUPPLY = 5.364
GAP = 7.4e-9

print("=" * 118)
print("ARGON07 -- the artificial-gravity sphere, scored on the framework's own constants")
print("=" * 118)

# 1) what a mass already does: the settled halo is the medium pulled in around it
for M_b, tag in [(1e3, "1 ton"), (1e6, "1000 tons"), (1.5e22, "planetoid (1 g at 1 m)")]:
    rM = math.sqrt(G*M_b/A0)
    Mc_tot = SUPPLY*M_b
    g_ph_1m = math.sqrt(G*M_b*A0)/1.0          # deep-regime phantom field at 1 m (unscreened)
    g_ph_screened = g_ph_1m*(1.0/LSTAR)**2     # (d/L*)^2 screening at d = 1 m
    rho_halo_rM = M_b/(2*math.pi*rM**2*rM*math.sqrt(1+4))   # settled density at r = r_M
    print(f"    {tag:14s}: r_M = {rM:9.1f} m, M_c,tot = {Mc_tot:.2e} kg, g_ph(1 m) = {g_ph_1m:.2e} m/s^2")
    print(f"      screened at d = 1 m: x(d/L*)^2 = {(1.0/LSTAR)**2:.1e} -> g_ph = {g_ph_screened:.2e} m/s^2; halo density at r_M = {rho_halo_rM:.2e} kg/m^3 (cosmic 2.4e-27)")

# 2) the amplitude is locked: what mass gives 1 g at 1 m?
M_1g = 9.8**2/(G*A0)      # sqrt(G M a0)/r = 9.8 at r = 1 -> M = (9.8)^2/(G a0)
check("amplitude lock: 1 g at 1 m needs M_b = 1.5e22 kg (planetoid) — no activation multiplies this",
      abs(M_1g-1.54e22)/1.54e22 < 0.05, f"M = {M_1g:.2e} kg = {M_1g/5.972e24:.2e} Earth masses")

# 3) screening kills the lab sphere
d = 1.0
scr = (d/LSTAR)**2
check("stiffness screening: a 1 m device couples to the medium at (d/L*)^2 = 3e-35 — the medium does not respond to lab-scale devices",
      scr < 1e-30, f"(1 m / 5.75 pc)^2 = {scr:.1e}")
d_need = math.sqrt(0.01)*LSTAR
print(f"    (d/L*)^2 = 0.01 would need d = {d_need/PC:.2f} pc — the 'sphere' must be pc-scale to couple at 1%")

# 4) dynamics: the medium's response time
tau_med = 1/GAP
check("medium response time 1/omega_gap = 4.3 yr — no dynamic manipulation on device timescales",
      abs(tau_med-1.35e8)/1.35e8 < 0.05, f"tau = {tau_med:.2e} s = {tau_med/3.156e7:.1f} yr")

# 5) the energy reservoir is real but unreleasable
E_res = SUPPLY*1e3*c**2
print(f"    1-ton sphere's settled reservoir: M_c c^2 = {E_res:.2e} J (5.4 tons x c^2) — unreleasable: continuity forbids rest-mass conversion (CFG793/ARGON05), any converting eps excluded by cosmology (ARGON06)")

# 6) directional push/pull: the halo follows the baryons (symmetric around symmetric mass)
print("    directional control: the settled halo is radial around a symmetric mass; steering the field = steering mass")
print("    (the phantom ADDS to Newton; it cannot cancel or redirect it without asymmetric mass).")

print("-" * 118)
print("  VERDICT: the sphere idea is real physics — every mass already IS an activated sphere: it pulls in the")
print("  medium (M_c = 5.364 M_b within 5.84 r_M) and carries a locked-amplitude field g_ph = sqrt(G M_b a0)/r.")
print("  But the framework's own constants close the device version: (1) stiffness screens lab scales by")
print("  (d/L*)^2 ~ 1e-34 (the medium only responds at L* >= 5.75 pc scales); (2) the amplitude is locked —")
print("  1 g at 1 m needs a 1.5e22 kg planetoid, no activation multiplies it; (3) no coupling exists to")
print("  'activate' the medium (E6; every portal closed); (4) the medium's dynamics are glacial (4.3 yr).")
print("  The sphere works — at galactic scales, where it is called a galaxy: the settled halo IS the medium")
print("  pulled in, and ARGON02's ESD is its measurable signature.")
print("-" * 118)

res = {"M_1g_at_1m_kg": M_1g, "screening_1m": scr, "d_for_1pct_coupling_pc": d_need/PC,
       "medium_response_yr": tau_med/3.156e7, "reservoir_1ton_J": E_res,
       "checks": CHECKS, "wall_s": time.time()-t0}
with open("gravity_sphere_results.json", "w") as f:
    json.dump(res, f, indent=1)
print(f"  RESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
print(f"  wall {time.time()-t0:.2f} s; threads 1; max RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6:.1f} MB")
sys.exit(0 if not FAILS else 1)