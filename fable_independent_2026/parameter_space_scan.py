#!/usr/bin/env python3
"""
parameter_space_scan.py -- brute-force the reduced relativistic-MOND parameter space against the full
gate battery, in parallel (built for a 64 GB M4 Max: uses all cores via multiprocessing).

WHAT IT DOES. Enumerates the 6 architecture axes of single-metric relativistic MOND (L122 reduction) PLUS the
continuous dark-sector mass and the a0 coefficient, and evaluates EVERY candidate against the gate battery
(L118 gates, encoded from the committed findings L88-L123). It reports (a) how much of the space is
eliminated, and (b) the SURVIVING region -- the candidates that pass all gates.

HONESTY. The gate functions encode the *distilled* results proven in the lanes (transition health L119/Phase A,
conformal ghost L116/L117, BBN stiff genericity L87/L123, CMB third peak / z_eq L121/L123, galaxy overshoot
L61, neutrino pincer g04i, PPN gamma L112). They are NOT a from-scratch Boltzmann/PPN solve -- a full CMB
Boltzmann run and the O(w) alpha_1 solve would refine the CMB and alpha_1 gates (flagged inline). So this is a
fast *screening* brute-force that reproduces the reduction and maps the surviving dark-sector window; treat a
survivor as "passes every constraint we have distilled", to be confirmed by the full calcs.

USAGE:
    python3 parameter_space_bruteforce.py                 # full scan, all cores
    python3 parameter_space_scan.py --mass-steps 400 --kappa-steps 50   # finer continuum
Outputs a summary + writes survivors to parameter_space_survivors.json.
"""
from __future__ import annotations
import argparse, json, math, os, itertools, time
from multiprocessing import Pool, cpu_count

# ---------------------------------------------------------------- physical constants / bounds
c = 2.998e8; Mpc = 3.0857e22; H0 = 67.4e3 / Mpc; cH0 = c * H0
A0_CANON = 9.3619e-11
Z_REC = 1090.0
OM, OR, OB = 0.315, 9.2e-5, 0.049           # ΛCDM matter, radiation, baryon density params
OMEGA_DM_TARGET = 0.265                       # dark density needed for the CMB (Ω_dm h^2 ~ 0.12)
ALPHA1_BOUND = 1e-4                            # |alpha_1| PPN bound (LLR)
# neutrino/hot-dark pincer windows (eV), from g04i:
NU_CMB_MIN_EV = 27.0                          # CMB (Neff/Omega) needs a COLD relic >= ~27 eV
NU_GAL_MAX_EV = 11.0                          # RAR/clusters free-streaming need <= ~11 eV

# ---------------------------------------------------------------- the axes (L122)
AXES = {
    "propagation":  ["propagating", "cuscuton"],
    "source":       ["lapse", "field"],
    "constraint":   ["khronometric_by_MOND", "Hperp_firstclass"],
    "a0_scaling":   ["local", "const_cosmo", "H_of_z"],
    "kernel":       ["exp", "simple", "standard", "nu_RAR"],
    "dark_sector":  ["none", "cosmological_const", "hot_nu", "kessence_dust",
                     "sterile_nu_cold", "particle_CDM"],
}

def z_eq(omega_clustering: float) -> float:
    """matter-radiation equality redshift for a clustering density Omega (baryons + clustering dark)."""
    return (OB + omega_clustering) / OR - 1.0

# ---------------------------------------------------------------- the gate battery
def gates(cand: dict) -> tuple[bool, list[str]]:
    """Return (passes_all, list_of_failures). Each gate encodes a committed finding."""
    fails = []
    prop = cand["propagation"]; src = cand["source"]; con = cand["constraint"]
    a0s = cand["a0_scaling"]; ker = cand["kernel"]; dark = cand["dark_sector"]
    m_eV = cand["dark_mass_eV"]; kappa = cand["kappa"]

    # G1 ghost / G3 transition health -- from L116/L117/L119/Phase A:
    #   a propagating MOND scalar is superluminal/ghostly in the transition; lapse-sourcing liberates the
    #   conformal ghost; only (cuscuton + field-sourced + H_perp first-class) is healthy.
    if prop != "cuscuton":
        fails.append("G1/G3 propagating scalar: RAQUAL superluminal / KGB wrong-sign in transition (L120/L118)")
    if src != "field":
        fails.append("G1 lapse-sourced: conformal ghost H0=-p^2/12M^2<0 (L116/L117)")
    if con != "Hperp_firstclass":
        fails.append("G2/G1 khronometric-by-MOND: H_perp second-class + ghost (L117)")

    # G3 transition health is kernel-blind under field-sourcing (L122): all four kernels pass; no fail here.

    # G5 gamma=1 (no-slip) holds structurally for the field-sourced branch (L112) -- pass.
    # G7 BTFR: the elliptic AQUAL field gives mass-dependent BTFR (Phase C); a fixed-power propagating
    #   kinetic term does not -- already excluded by prop!=cuscuton above.

    # G-a0 (Axis 5): local a0 is observationally excluded (rho_local null 13-34 sigma, L121); a0 must be
    #   cosmological. a0∝H(z) is the distinctive survivor; const_cosmo is allowed but non-distinctive.
    if a0s == "local":
        fails.append("Axis5 local a0: rho_local null 13-34 sigma (L121)")

    # G8 CMB third peak (L121/L123): needs a CLUSTERING a^-3 density giving z_eq > z_rec.
    clustering_omega = 0.0
    if dark in ("kessence_dust", "sterile_nu_cold", "particle_CDM"):
        clustering_omega = OMEGA_DM_TARGET      # these can supply a clustering a^-3 density
    elif dark == "hot_nu":
        # hot neutrinos free-stream: they cluster only if massive/cold enough; encode via the pincer below.
        clustering_omega = OMEGA_DM_TARGET if m_eV >= NU_CMB_MIN_EV else 0.0
    if z_eq(clustering_omega) <= Z_REC:
        fails.append(f"G8 CMB 3rd peak: z_eq={z_eq(clustering_omega):.0f} <= z_rec={Z_REC:.0f} (no clustering a^-3 density) (L123)")

    # G9 BBN (L87/L123): a shift-symmetric SCALAR dust carries a generic a^-6 stiff tail => >20-order tuning.
    if dark == "kessence_dust":
        fails.append("G9 BBN: shift-symmetric scalar dust has a generic a^-6 stiff tail (~24-order tuning, L87/L123)")

    # G-nu pincer (g04i): a hot/relic component must be COLD enough for the CMB (>=27 eV) yet free-stream out
    #   of galaxies/clusters (<=11 eV). No overlap => any single hot component that fixes the CMB over-clusters.
    if dark in ("hot_nu",):
        if not (m_eV >= NU_CMB_MIN_EV):
            fails.append(f"G-nu: m={m_eV:.1f} eV < {NU_CMB_MIN_EV} eV, too hot to supply CMB density")
        if not (m_eV <= NU_GAL_MAX_EV):
            fails.append(f"G-nu: m={m_eV:.1f} eV > {NU_GAL_MAX_EV} eV, over-clusters galaxies/RAR (L61)")

    # G-gal (L61 excess-spent-once ~1.69x overshoot): the dark component must be SMOOTH on galaxy scales.
    #   particle_CDM and sterile_nu_cold cluster in galaxies -> add mass there -> MOND already gives the RAR,
    #   so they double-count unless free-streaming smooths them below galaxy scales. Cold CDM does NOT
    #   free-stream -> over-clusters in galaxies (L61). A sterile nu at keV-scale free-streams to smooth
    #   galaxies while clustering on large scales.
    # VELOCITY-ORDERING LEMMA (down-select agent, L125): a decoupled collisionless species has v_rms ∝ 1/a
    # (monotonically DECREASING), so "cold enough to cluster for the CMB (G8a)" ⟹ "even colder today" ⟹
    # "clusters in galaxies" ⟹ L61 overshoot. Hence G8a ∧ G-gal is EMPTY for ANY decoupled dark component.
    if clustering_omega > 0.0:
        fails.append("G-gal: velocity-ordering lemma -- clustering for the CMB (G8a) forces clustering in "
                     "galaxies (colder today, v_rms∝1/a) -> L61 ~1.69x overshoot; G8a ⟹ ¬G-gal (L125)")

    # G6a PPN alpha_1: the health branch is VECTOR-FREE (cuscuton clock is a scalar) -- provisional PASS,
    #   pending the O(w) moving-frame solve (agent running). AeST failed via its VECTOR; a scalar clock has
    #   no vector alpha_1 source. (Flagged: this gate is provisional.)
    # (no fail added; provisional)

    # G10 a0 coefficient: fitted; any kappa in the observational band is allowed (not a discriminator).
    if not (0.30 <= kappa <= 0.70):
        fails.append(f"G10 a0 coeff kappa={kappa:.3f} outside the observational band [0.30,0.70]")

    return (len(fails) == 0, fails)

# ---------------------------------------------------------------- worker
def eval_combo(args):
    keys, combo, masses, kappas = args
    base = dict(zip(keys, combo))
    survivors = []
    # only scan mass/kappa when they matter (dark sectors with a mass; kappa always)
    mass_grid = masses if base["dark_sector"] in ("hot_nu", "sterile_nu_cold", "particle_CDM") else [0.0]
    for m in mass_grid:
        for kap in kappas:
            cand = dict(base, dark_mass_eV=m, kappa=kap)
            ok, _ = gates(cand)
            if ok:
                survivors.append(cand)
    tested = len(mass_grid) * len(kappas)
    return tested, survivors

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mass-steps", type=int, default=200)
    ap.add_argument("--kappa-steps", type=int, default=41)
    ap.add_argument("--procs", type=int, default=0, help="0 = all cores")
    args = ap.parse_args()

    # continuum grids
    masses = [10 ** x for x in _linspace(-1.0, 6.0, args.mass_steps)]   # 0.1 eV .. 1 MeV (log)
    kappas = _linspace(0.25, 0.75, args.kappa_steps)

    keys = list(AXES.keys())
    combos = list(itertools.product(*[AXES[k] for k in keys]))
    tasks = [(keys, combo, masses, kappas) for combo in combos]

    nproc = args.procs or cpu_count()
    print(f"[brute-force] axes={ {k: len(v) for k, v in AXES.items()} }")
    print(f"[brute-force] discrete architecture combos = {len(combos)}; "
          f"x mass({args.mass_steps}) x kappa({args.kappa_steps}) continuum; cores = {nproc}")
    t0 = time.time()
    total_tested = 0; all_survivors = []
    with Pool(nproc) as pool:
        for tested, survs in pool.imap_unordered(eval_combo, tasks, chunksize=4):
            total_tested += tested; all_survivors.extend(survs)
    dt = time.time() - t0

    # collapse survivors to distinct architectures (ignore the kappa/mass continuum for the count)
    arch_keys = ("propagation", "source", "constraint", "a0_scaling", "kernel", "dark_sector")
    surv_arch = sorted({tuple(s[k] for k in arch_keys) for s in all_survivors})

    print(f"\n[brute-force] tested {total_tested:,} candidates in {dt:.1f}s")
    print(f"[brute-force] survivors: {len(all_survivors):,} candidate points "
          f"({100*len(all_survivors)/max(total_tested,1):.4f}% of the scanned space)")
    print(f"[brute-force] distinct SURVIVING ARCHITECTURES: {len(surv_arch)} "
          f"(out of {len(combos)} discrete = {100*(1-len(surv_arch)/len(combos)):.1f}% architecture-space reduction)")
    for a in surv_arch:
        print("    SURVIVOR:", dict(zip(arch_keys, a)))
    if not surv_arch:
        print("    NO SURVIVOR -- the hybrid is also pincered (report which gate has no pass).")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parameter_space_survivors.json")
    with open(out, "w") as f:
        json.dump({"surviving_architectures": [dict(zip(arch_keys, a)) for a in surv_arch],
                   "n_survivor_points": len(all_survivors), "n_tested": total_tested,
                   "architecture_reduction_pct": 100*(1-len(surv_arch)/len(combos))}, f, indent=2)
    print(f"[brute-force] wrote {out}")

def _linspace(a, b, n):
    if n <= 1: return [a]
    return [a + (b - a) * i / (n - 1) for i in range(n)]

if __name__ == "__main__":
    main()
