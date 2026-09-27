#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR8 (0/4) -- THE INVERSE SPECIFICATION: WHAT THE DARK COMPONENT MUST DO, CHECKED AGAINST THE RECORD, AND WHAT IT MEANS IN
PHYSICAL UNITS FOR THE ONE CONTINUUM THAT PASSES.

PART A.  Every row of XR8_README.md's spec table cites a file and a verbatim snippet.  This script checks that each
  snippet is present at the cited path and records whether the path is committed (git) or only in the working tree
  (several of the day's inputs -- CV3, CV4, FL1 -- were uncommitted when XR8 ran).  It reads nothing but text.
PART C NUMBERS (arithmetic only; no simulation).  For the continuum XR8 2/4 finds passing (the order parameter with a
  light radial mode, i.e. a nearly free complex field), with L383's boson-mass floor m >= 1.9-5.2e-19 eV (with the
  framework's clearing; 4.9e-19 - 1.25e-18 without):
  N1  the de Broglie length h / (m v) in a dwarf, a Milky-Way halo and a cluster, as a fraction of the system's size,
      against L374's tested lambda / L = 1e-2 (the test is conservative where the physical ratio is smaller: a smaller
      lambda / L tracks better, L374 MUTATE and XR8 2/4);
  N2  the occupation number per de Broglie cell, N = (rho / m) lambda^3 (classical field if N >> 1);
  N3  what the pass condition W <= W_c (XR8 2/4's scan; 1e-3 if that file is absent) requires of the field's
      self-interaction in a halo: c_s = sqrt(W_c) v, i.e. a radial (amplitude) mass m_r = 2 m c_s / c and a quartic
      coupling lambda4 <= 2 W_c (v/c)^2 m^4 / rho (natural units; V = m^2 R^2/2 + lambda4 R^4/4, covariant_clock RESULT).
CHECKS
  A*  one check per spec row: every cited snippet is present at its path.
  N1-N3 as above (N >> 1 at the floor; lambda / R below 1e-2 in Milky-Way halos and clusters; the dwarf is reported).
MUTATE=1 tampers one cited number (the Bullet lag ratio 11 -> 12): its row must FAIL (rc = 1).

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR8_spec_table.py   (seconds)
"""
import os, sys, json, math, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR8_spec_table" + ("_MUTATE" if MUTATE else "")
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR8-0", "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def committed(path):
    r = subprocess.run(["git", "-C", REPO, "log", "-1", "--format=%h", "--", path], capture_output=True, text=True)
    h = r.stdout.strip()
    st = subprocess.run(["git", "-C", REPO, "status", "--porcelain", "--", path], capture_output=True, text=True).stdout.strip()
    if not h:
        return "UNCOMMITTED (untracked)"
    return h + (" (+ uncommitted working-tree edits)" if st else "")


CC = "qwen_claude_field_theory/closure_2026/condensate_pincer_2026/"
SPEC = [
    ("A1 background and CMB: w = 0 and cold; linear cosmology sees only the GDM triple (w, c_s^2, c_vis^2) plus an amount",
     [("real_research/reviews/mi_particle_vs_mode_2026.py", "generalized-dark-matter (GDM) triple (w, c_s^2, c_vis^2) plus its amount"),
      ("real_research/reviews/mi_particle_vs_mode_2026.py", "w0 <= ~2.0e-14"),
      ("real_research/reviews/mi_particle_vs_mode_2026.py", "a gap of ~5.85 orders of magnitude")]),
    ("A2 the Lyman-alpha forest at z = 2-3: cold (c_s(z = 3) below ~5 km/s as a check threshold; <= 9.5 km/s via L185)",
     [(CC + "condensate_mu_pincer_2026.out", "c_s(z=3) < 5 km/s"),
      (CC + "dark_solid_first_gates_2026.out", "forest-cold at z = 3 (c_L < 5 km/s)"),
      ("real_research/clock_2026/L289_carrier_requirements.out", "the forest (L185) needs c_s(z = 3) <= 9.5 km/s"),
      ("real_research/condensate_dust_2026/README.md", "m ≳ 2 × 10⁻²¹ eV (Iršič et al. 2017)")]),
    ("A3 kernel-invisible, hence Newtonian gravity only (reciprocity)",
     [("real_research/g03_audit_2026/L353_kernel_invisible_dark_component.out",
       "a static Lagrangian's species-response matrix is symmetric, so a kernel-invisible component feels no phantom"),
      ("real_research/chk_v0_2026/CV1_nr_assembly.out", "the dark component feels u (Newtonian only)")]),
    ("A4 collisionless in cluster mergers, no pressure support (Bullet lag >= 11x the offset; Harvey beta)",
     [(CC + "merger_gate_supported_media_2026.out", "min lag / max offset = " + ("12" if MUTATE else "11")),
      ("real_research/merger_infall_2026/README.md", "β = δSI/δSG = −0.04 ± 0.07"),
      ("real_research/merger_infall_2026/README.md", "limit +0.10, i.e. 2.2σ from Harvey's −0.04 ± 0.07")]),
    ("A5 multistreams through shell crossing (the minimal condensate breaks; a wave field passes above a boson-mass floor)",
     [("real_research/condensate_dust_2026/README.md", "cold, it breaks down at the first stream crossing;"),
      ("real_research/condensate_dust_2026/README.md", "| 5 km/s | 1.25 × 10⁻¹⁸ eV | 4.9–5.2 × 10⁻¹⁹ eV |"),
      ("real_research/condensate_dust_2026/README.md", "| 10 km/s | 4.9 × 10⁻¹⁹ eV | 1.9–2.0 × 10⁻¹⁹ eV |")]),
    ("A6 cleared from galaxy halos by z ~ 2-2.5, about half retained in clusters (X-COP two-sided gate)",
     [("real_research/dark_sector_2026/README.md", "absent from galaxy halos at z ≲ 2.5, about half-present in clusters at z = 0"),
      ("real_research/dark_sector_2026/README.md", "It requires 0.286 ≤ ε ≤ 0.835 on the canonical footing and 0.220 ≤ ε ≤ 0.768 on the alternative."),
      ("real_research/dark_sector_2026/L388_linear_gate_pooled.out", "X-COP two-sided 0.286-0.768; clearing <= 0.30; forest <= 0.10; S8 >= 0.922")]),
    ("A7 small-scale power suppressed by z ~ 0.5 (cosmic shear: MOND regions capped near 1.75 Mpc with L388's retention)",
     [("real_research/mond_sector_gate_2026/README.md", "MOND regions must stop growing near 1.75 Mpc (z = 0.5)"),
      ("real_research/mond_sector_gate_2026/README.md", "With the cap and L388's density-trigger retention it passes: 1.05 / 1.12."),
      ("real_research/mond_sector_gate_2026/README.md", "uncapped, worst R is 2.47–4.32 against 1.2")]),
    ("A8 S8 / KiDS",
     [("real_research/dark_sector_2026/L365_virialization_triggered_carrier.out", "sigma_8(model)/sigma_8(LCDM) >= 0.922")]),
    ("A9 criterion B: not the khronon's own dust (the foliation would fold); the khronon's leaves are CMC in bound regions",
     [("real_research/cross_thread_review_2026_09_26/XR3_obligations.md", "Shell crossing is then a caustic of the foliation"),
      ("real_research/chk_v0_2026/CV4_khronon_K_profile.out", "its leaves are constant-mean-curvature (CMC) at this order"),
      ("real_research/chk_v0_2026/CV4_khronon_K_profile.out", "max |K/3H - 1| = 4.79e-03")]),
    ("A10 V0's multiplier rule: a varied quantity reads only constrained fields, so the fluid is not a multiplier",
     [("real_research/chk_v0_2026/README.md", "constraint Hessian's determinant is then a²b² for every gate shape")]),
    ("A11 the MOND-sector switch is carrier-blind (the fluid must not enter what the switch reads)",
     [("real_research/mond_sector_gate_2026/README.md", "The switch is carrier-blind, so there is no bistability and no self-limiting clearing.")]),
    ("A12 no new particle species, and the dark MASS is still required",
     [("real_research/cross_thread_review_2026_09_26/XR3_obligations.md", "**No new dark-matter particle species**"),
      ("real_research/cross_thread_review_2026_09_26/XR3_obligations.md", "The dark **mass** is still required (CMB, clusters)")]),
]

P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: one cited number tampered (Bullet lag ratio 11 -> 12) ***")
P("\n" + "=" * 116 + "\nPART A  THE SPEC TABLE, row by row: is every cited snippet at its path?\n" + "=" * 116)
ROWS = {}
for row, cites in SPEC:
    found = []
    for path, snip in cites:
        full = os.path.join(REPO, path)
        txt = open(full, encoding="utf-8").read() if os.path.exists(full) else ""
        line = next((i + 1 for i, ln in enumerate(txt.splitlines()) if snip in ln), None)
        found.append(dict(path=path, line=line, present=line is not None, status=committed(path), snippet=snip))
    ROWS[row] = found
    check(row, "; ".join(f"{f['path']}:{f['line']} [{f['status']}]" if f["present"] else f"MISSING in {f['path']}" for f in found),
          all(f["present"] for f in found))
OUT["numbers"]["rows"] = ROWS

# ------------------------------------------------------------------------------------------------ Part C numbers
P("\n" + "=" * 116 + "\nPART C NUMBERS  the passing continuum (a nearly free complex field) in physical units\n" + "=" * 116)
HBARC_EVM = 1.973269804e-7                                        # eV m
C_KMS = 299792.458
MSUN, PC = 1.98892e30, 3.0857e16
EV_KG = 1.78266192e-36                                            # kg per eV/c^2
KGM3_TO_EV4 = (1.0 / EV_KG) * (HBARC_EVM ** 3)                    # (kg/m^3) -> eV^4 in natural units
wc_file = os.path.join(HERE, "XR8_order_parameter_scan_results.json")
W_C = 1e-3
if os.path.exists(wc_file):
    try:
        wcs = [v["W_c"] for v in json.load(open(wc_file))["numbers"]["W_c"].values() if v]
        W_C = min(wcs) if wcs else W_C
    except Exception:
        pass
P(f"  W_c used: {W_C:g} (the smallest passing-edge W over XR8 2/4's scans; 1e-3 if absent)")
SYSTEMS = {"Segue-1-like dwarf": (5.7, 7.0, 29.0), "Milky-Way halo (solar radius)": (0.01, 200.0, 8000.0),
           "cluster core (1e14.5 Msun)": (1e-3, 1000.0, 1e5)}        # (rho in Msun/pc^3, v in km/s, size R in pc)
TABN = {}
for m in (1.9e-19, 5.2e-19):
    for name, (rho_ms, v, Rsz) in SYSTEMS.items():
        rho = rho_ms * MSUN / PC ** 3                              # kg/m^3
        lam_db = 2 * math.pi * HBARC_EVM / (m * v / C_KMS)         # m  (h / (m v))
        n = rho / (m * EV_KG)                                      # per m^3
        N = n * lam_db ** 3
        rho4 = rho * KGM3_TO_EV4                                   # eV^4
        lam4 = 2 * W_C * (v / C_KMS) ** 2 * m ** 4 / rho4
        m_r = 2 * m * math.sqrt(W_C) * (v / C_KMS)
        TABN[f"m={m:g}|{name}"] = dict(lambda_dB_pc=lam_db / PC, lambda_over_R=lam_db / PC / Rsz, occupation=N,
                                       lambda4_max=lam4, m_r_max_eV=m_r)
        P(f"    m = {m:.1e} eV, {name:30s}: h/(m v) = {lam_db / PC:9.3g} pc = {lam_db / PC / Rsz:.1e} of R = {Rsz:g} pc; "
          f"occupation per de Broglie cell {N:9.2e}; light-radial condition: m_r <= {m_r:.2e} eV, quartic lambda4 <= {lam4:.1e}")
OUT["numbers"]["physical"] = TABN
OUT["numbers"]["W_c_used"] = W_C
Nmin = min(v["occupation"] for v in TABN.values())
big = [v["lambda_over_R"] for k_, v in TABN.items() if "dwarf" not in k_]
dw = [v["lambda_over_R"] for k_, v in TABN.items() if "dwarf" in k_]
check("N1/N2 at L383's floor the field is classical (occupation >> 1) in every system; in Milky-Way halos and clusters its de Broglie "
      "length is far below L374's tested lambda / L = 1e-2 (the 1-D test is conservative there); in an ultra-faint dwarf it is not",
      f"min occupation {Nmin:.1e}; lambda / R: Milky Way and cluster {min(big):.1e}-{max(big):.1e}; Segue-1-like dwarf "
      f"{min(dw):.2f}-{max(dw):.2f}", Nmin > 1e20 and max(big) < 1e-2,
      reading="'not particles' = a classical coherent field at occupation ~1e78-1e88; its quanta, if quantised, are bosons of mass m.  "
              "In ultra-faint dwarfs lambda / r_h ~ 0.1-0.3: wave effects are order unity there -- L383's heating floor, not this test, "
              "is the binding constraint")
check("N3 the pass condition W <= W_c translates into a nearly FREE field: a radial (amplitude) mass far below the boson mass and a "
      "quartic self-coupling below ~1e-70 in every system", {k: f"m_r <= {v['m_r_max_eV']:.1e} eV, lambda4 <= {v['lambda4_max']:.1e}"
                                                             for k, v in TABN.items() if k.startswith('m=1.9e-19')},
      max(v["lambda4_max"] for v in TABN.values()) < 1e-70,
      reading="the order parameter's Thomas-Fermi (condensate) regime is excluded where streams cross; its self-interaction "
              "must be negligible there -- a nearly free complex field")

n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {SLUG}_results.json   "
  f"[{time.time() - T0:.1f}s]")
P(f"rc={0 if n_fail == 0 else 1}")
sys.exit(0 if n_fail == 0 else 1)
