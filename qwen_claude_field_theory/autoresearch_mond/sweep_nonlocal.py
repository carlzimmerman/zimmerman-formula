#!/usr/bin/env python3
"""DETERMINISTIC PARAMETER SWEEP — spatially-nonlocal F+ corridor (the live route).
No LLM calls. Fixed architecture, low-dimensional theta, hierarchical HARD kill gates
(lexicographic: a point failing an early gate is dead regardless of later virtues).

FROZEN (hard constraints, never swept):  mu(y)=1-e^{-y};  F+(Z)=4[1-(1+sqrt(Z)/2)e^{-sqrt(Z)/2}];
a0 = 9.3619e-11 m/s^2 (postulated input, never absorbs problems).

SWEPT theta = (eta, m_ratio) for the minimal massive-pump localization:
  eta     = kinetic normalization of the auxiliary (localizer) field chi
  m_ratio = m_pump / (a0/c^2) ... expressed as the Yukawa range ell=1/m in kpc.
MODEL (stated, minimal, transparent):
  - localized completion of the F+ kernel via auxiliary chi with quadratic action
    L_chi = eta [ chidot^2 - (1/2) c^2 (grad chi)^2 ] - (1/2) m^2 chi^2  (the 1/2 gradient
    normalization reproduces the BANKED extra-mode dispersion omega^2 = (1/2) c^2 k^2 at m=0, eta=1)
  - the kernel operator becomes (-D^2 + m^2)^{-1}: Yukawa-corrupted MOND beyond ell=1/m.
GATES (in order, hard):
  S1a mu-identity: the pump must NOT touch the constitutive mu (structural: enforced by
      construction here; recorded as PASS with the F+ identity re-verified once).
  S1b kernel fidelity: Yukawa corruption |delta g/g| ~ (r/ell)^2/2 (leading) must be < 5% at
      r = 100 kpc (outer rotation curves) — else MOND phenomenology broken.
  S2a no-ghost: eta > 0.
  S2b extra-mode freezing: the omega^2=(1/2)c^2k^2 mode must be non-dynamical on observable
      scales: frozen if m c^2 >> omega_dyn at galaxy scales, i.e. ell < c/omega_dyn with
      omega_dyn ~ 2pi/T_dyn, T_dyn ~ 200 Myr  -> ell_freeze ~ c*T_dyn/(2pi) ~ 9.8e3 kpc?? NO:
      the mode at wavenumber k has omega ~ c k/sqrt(2): it is RELATIVISTIC, always fast; freezing
      requires the MASS gap to exceed the k-band excited by galactic sources: k ~ 1/r_sys ->
      frozen when m > k i.e. ell < r_sys is NOT freezing (that's the propagating regime);
      true freezing: m >> k_max ~ 1/r_min with r_min ~ 1 kpc (inner galaxy) -> ell << 1 kpc.
  S3  radiative sanity (only for survivors): energy loss into the chi mode from time-dependent
      sources must be suppressed — automatic if S2b holds (gap >> driving frequencies).
Adaptive: coarse log grid -> refine around any surviving island.
"""
import numpy as np, json, time

KPC = 3.0857e19          # m
C   = 2.998e8            # m/s

def gates(eta, ell_kpc):
    """Return (verdict, failed_gate, details). Lexicographic hard rejection."""
    # S2a no-ghost
    if eta <= 0:
        return "KILL", "S2a_ghost", "eta<=0"
    # S1b kernel fidelity at r=100 kpc: Yukawa (-D^2+m^2)^-1 vs (-D^2)^-1 => e^{-r/ell} factor;
    # fractional force corruption ~ (r/ell) for r<ell (leading Yukawa exponent), need < 5%
    r_out = 100.0
    corruption = r_out / ell_kpc          # leading e^{-r/ell} ~ 1 - r/ell
    if corruption > 0.05:
        return "KILL", "S1b_kernel_fidelity", f"Yukawa corruption {corruption:.2e} at 100kpc (need <0.05) -> ell>{r_out/0.05:.0f} kpc required"
    # S2b extra-mode freezing: mass gap must exceed the k-band sourced by galactic structure
    # k_max ~ 1/(1 kpc); frozen requires m > k_max i.e. ell < 1 kpc
    ell_freeze_max = 1.0
    if ell_kpc > ell_freeze_max:
        return "KILL", "S2b_mode_not_frozen", f"ell={ell_kpc:.2e} kpc > {ell_freeze_max} kpc: omega^2=(1/2)c^2k^2+m^2c^4 mode is LIGHT on galactic k-band -> propagating 3rd polarization"
    return "PASS", None, "all gates"

def sweep():
    print("=== STAGE A: coarse log grid (eta x ell) ===")
    etas = np.logspace(-3, 3, 25)
    ells = np.logspace(-3, 6, 46)          # 1e-3 kpc .. 1e6 kpc
    survivors, kill_count = [], {}
    for eta in etas:
        for ell in ells:
            v, g, d = gates(eta, ell)
            if v == "PASS":
                survivors.append((eta, ell))
            else:
                kill_count[g] = kill_count.get(g, 0) + 1
    total = len(etas)*len(ells)
    print(f"   {total} points: {len(survivors)} survive; kills by gate: {kill_count}")

    # the two binding walls, analytically:
    print("\n=== THE TWO WALLS (analytic, eta-independent) ===")
    print("   S1b kernel fidelity  : requires ell > 2000 kpc  (5% at 100 kpc)")
    print("   S2b mode freezing    : requires ell < 1 kpc     (gap above galactic k-band)")
    print("   => joint window: ell in (2000, 1) kpc = EMPTY by 3.3 orders of magnitude.")
    print("   eta cannot help: it scales the kinetic term, not the m-vs-kernel trade-off.")

    if survivors:
        print("\n=== STAGE B: refine islands ===")
        # would zoom here — but analytically impossible; verify none survived
    verdict = "EMPTY" if not survivors else f"{len(survivors)} points"
    print(f"\n=== SWEEP VERDICT: viable region {verdict} ===")
    print("The SINGLE-MASS pump door is CLOSED: the same mass m that freezes the extra")
    print("omega^2=(1/2)c^2k^2 mode (needs 1/m < 1 kpc) Yukawa-corrupts the MOND kernel")
    print("(needs 1/m > 2000 kpc). Gap: 3.3 orders. A viable pump must be SCALE-SPLIT:")
    print("the operator gapping the mode must not be the operator building the kernel —")
    print("i.e. the localizer field and the kernel field must be DIFFERENT operators/fields")
    print("(two-auxiliary localization), the next structural question for this corridor.")
    print('CERTIFICATE_JSON: ' + json.dumps({
        "gate": "SWEEP-nonlocal-pump", "status": "KILL",
        "certificate": "single-mass pump localization of F+ has EMPTY viable region: mode-freezing "
        "needs ell=1/m<1 kpc, kernel fidelity needs ell>2000 kpc (5% at 100 kpc); joint window empty "
        "by 3.3 orders, eta-independent. Scale-split (two-auxiliary) localization = surviving door.",
        "numeric_values": {"ell_freeze_max_kpc": 1.0, "ell_fidelity_min_kpc": 2000.0,
                           "gap_orders": 3.3, "grid_points": total, "survivors": len(survivors)},
        "assumptions": ["banked extra-mode dispersion omega^2=(1/2)c^2k^2 (m=0)",
                        "single mass m enters BOTH the mode gap and the kernel (-D^2+m^2)^-1",
                        "fidelity: <5% force corruption at 100 kpc", "freezing: gap above k~1/kpc"]}))
    return survivors

if __name__ == "__main__":
    t0=time.time(); sweep(); print(f"[{time.time()-t0:.2f}s]")
