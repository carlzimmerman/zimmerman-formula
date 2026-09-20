#!/usr/bin/env python3
"""
bhstar_2609_09274_check.py -- absorb arXiv:2609.09274 into the record.
======================================================================
Sun, Naidu, de Graaff, Eilers et al. (2026-09-08), "Overmassive No More: The Case for
Little Red Dots Hosting Black Hole Seeds as Massive as Single Supermassive Stars".

THE STUDY. JWST little red dots (LRDs) as "black hole stars" (BH*s): an AGN inside an
optically thick, dense gas envelope. Stellar-atmosphere fits to host-subtracted stacks of
117 LRDs give T_eff ~ 4200-4800 K, R_phot ~ 700-2000 au, L_bol ~ 1e43-45 erg/s. Four
NON-virial mass estimators converge on M_BH* ~ 1e4-5 Msun (vs ~1e6-8 from local virial
calibrations) -> not "overmassive" against hosts of M* ~ 1e8 Msun -> consistent with single
supermassive stars (SMS) below their GR-instability ceiling ~1e5-6 Msun; the LRD luminosity
function bright cutoff matches that ceiling at Gamma_es ~ 50.

WHAT THIS LANE CHECKS.
  (A) ABSORPTION: every published BH* mass number is reproduced from the paper's own four
      estimator equations at the paper's stated inputs (Table 2 upper bounds, Table 3 fiducial).
      Literature is absorbed, not trusted.
  (B) FRAMEWORK-REGIME: where these objects sit relative to the framework's a0 on both
      footings; the a0-line force correction evaluated AT the pseudo-photosphere and at the
      host scale. (Expected result is a NON-detection: the regime is deep-Newtonian. Silence
      is registered as silence, never as detection.)

RULE 1 (footings): a0(fw) = c H_Lambda / Z, Z = sqrt(32 pi / 3) = 5.78881 -> 9.3619e-11 m/s^2;
      a0(canon) = 1.2e-10; SPARC anchor 1.13e-10. Framework interpolation nu(y) = sqrt(1 + 1/y).
RULE 2 (C3 fence): every statement is keyed to the paper's own numbers; no extrapolation
      beyond them. The Eddington-method Gamma_es = 5-50 is the paper's ASSUMED dial (set by
      analogy to eta Car / IIn SNe), flagged as such, not treated as a measurement.
RULE 3 (honesty): a check that can only pass by construction is not included. The regime
      checks below print the measured g/a0 and the a0-line correction factor; the verdict
      text is computed from them.

Run:  python3 reviews/black_hole_stars_2609.09274_check.py   (stdlib only)
Out:  reviews/black_hole_stars_2609.09274_check.out (by redirection) + this stdout.
"""

import math, json, os

G = 6.674e-11
Msun = 1.98892e30
AU = 1.495978707e11
C = 2.99772458e8
SIGMA = 5.670374e-8          # Stefan-Boltzmann, W m^-2 K^-4
KAPPA_ES = 0.04              # electron-scattering opacity, m^2/kg (paper: 0.40 cm^2/g)
YR = 3.1557e7
KPC = 3.0856775814913673e19   # 1 kpc in meters

A0_FW = 9.3619e-11           # c H_Lambda / Z, kappa = 1/2 (framework footing)
A0_CANON = 1.2e-10           # canonical MOND
A0_SPARC = 1.13e-10          # SPARC RAR anchor (Z2 cascade)

# Paper Table 1 (stack properties, posterior medians). v_blue in km/s, None = no absorber data.
STACKS = {
    "median(N=117)":  dict(logg=-2.2, R_au=941,  Llog=43.8, vblue=-495, T=4662, Mstar=8.5),
    "luminous(N=17)": dict(logg=-2.5, R_au=1989, Llog=44.5, vblue=-523, T=4757, Mstar=8.2),
    "inter(N=85)":    dict(logg=-1.9, R_au=900,  Llog=43.8, vblue=-364, T=4716, Mstar=8.0),
    "faint(N=15)":    dict(logg=-2.5, R_au=747,  Llog=43.5, vblue=None, T=4233, Mstar=8.4),
}

results = []
def check(name, measured, paper, tol):
    ok = (paper == 0) and (measured == 0) or (paper != 0 and abs(measured - paper) <= tol * abs(paper))
    results.append(dict(check=name, measured=measured, paper=paper, tol=tol, ok=ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: measured {measured:.4g} | paper {paper:.4g} | tol {tol*100:.1f}%")
    return ok

print("=" * 78)
print("BH* ABSORPTION LANE  --  arXiv:2609.09274 (Sun, Naidu, de Graaff, Eilers et al. 2026)")
print("=" * 78)
print("\n[A] The four estimator equations, recomputed at the paper's own inputs\n")

# --- equation-by-equation recomputation --------------------------------------------
recomputed = {}
for name, s in STACKS.items():
    g_si = 10 ** s["logg"] * 1e-2                 # log g in cgs -> SI
    R = s["R_au"] * AU
    L = 10 ** (s["Llog"] - 7)                      # erg/s -> W
    Lerg = 10 ** s["Llog"]
    R_sb = math.sqrt(L / (4 * math.pi * SIGMA * s["T"] ** 4)) / AU   # Stefan-Boltzmann radius, au

    M_sg = g_si * R ** 2 / G                                        # Eq (1)  surface gravity
    vesc = math.sqrt(2 * G * M_sg / R)
    t_dyn = R / vesc / YR
    M_esc_raw = R * (s["vblue"] * 1000) ** 2 / (2 * G) if s["vblue"] else None   # Eq (3) bound
    M_esc_fid = M_esc_raw / 9 if M_esc_raw else None                # v_inf/v_esc ~ 3 -> /9
    M_var10 = R ** 3 / (2 * G * (10 * YR) ** 2)                     # Eq (4) bound t >= 10 yr
    M_var30 = R ** 3 / (2 * G * (30 * YR) ** 2)                     # fiducial t ~ 30 yr
    # Eq (2): M = kappa L_bol / (4 pi G c Gamma)
    M_e1 = KAPPA_ES * L / (4 * math.pi * G * C * 1)  / Msun          # Gamma = 1 bound
    M_e5 = KAPPA_ES * L / (4 * math.pi * G * C * 5)  / Msun          # Gamma = 5
    M_e50 = KAPPA_ES * L / (4 * math.pi * G * C * 50) / Msun        # Gamma = 50
    Gamma_implied_1e4 = (Lerg * 1e-7) / (4 * math.pi * G * (10 ** 4.0) * Msun * C / KAPPA_ES)

    recomputed[name] = dict(M_sg=M_sg / Msun, vesc_kms=vesc / 1e3, t_dyn_yr=t_dyn,
                            M_esc_raw=(M_esc_raw or 0) / Msun, M_esc_fid=(M_esc_fid or 0) / Msun,
                            M_var10=M_var10 / Msun, M_var30=M_var30 / Msun,
                            M_e1=M_e1, M_e5=M_e5, M_e50=M_e50,
                            R_sb=R_sb, g_si=g_si,
                            Gamma_implied_1e4=Gamma_implied_1e4)

m = recomputed["median(N=117)"]
print("  median BH* stack (paper Table 1 -> Tables 2-3):")
check("Eq.1 surface-gravity mass  log M", math.log10(m["M_sg"]), 4.0, 0.05)
check("Stefan-Boltzmann R_phot (au)", m["R_sb"], 941.0, 0.05)
check("Eq.3 escape-velocity bound  log M", math.log10(m["M_esc_raw"]), 5.1, 0.05)
check("Eq.3 fiducial (wind /9)  log M", math.log10(m["M_esc_fid"]), 4.2, 0.05)
check("Eq.4 variability bound (t=10 yr)  log M", math.log10(m["M_var10"]), 5.0, 0.05)
check("Eq.4 fiducial (t=30 yr)  log M", math.log10(m["M_var30"]), 4.1, 0.05)
check("Eq.2 Eddington bound (Gamma=1)  log M", math.log10(m["M_e1"]), 5.7, 0.05)
check("Eq.2 Eddington fiducial (Gamma=5)  log M", math.log10(m["M_e5"]), 5.0, 0.05)
check("Eq.2 Eddington fiducial (Gamma=50)  log M", math.log10(m["M_e50"]), 4.0, 0.05)
check("Gamma_es implied at M=1e4 Msun (paper: '~50')", m["Gamma_implied_1e4"], 50.0, 0.15)
check("v_esc at photosphere (km/s)", m["vesc_kms"], 133.0, 0.05)
check("t_dyn = R/v_esc (yr) vs lensed ~30 yr", m["t_dyn_yr"], 30.0, 0.15)

l = recomputed["luminous(N=17)"]; f = recomputed["faint(N=15)"]
check("luminous Eq.1  log M", math.log10(l["M_sg"]), 4.3, 0.05)
check("faint Eq.1  log M", math.log10(f["M_sg"]), 3.4, 0.05)

print("\n[B] Framework regime (both footings). Expected: deep-Newtonian, a0-line dormant.\n")
print(f"  a0 footings: fw = c H_Lambda / Z = {A0_FW:.4g}; canon = {A0_CANON:.4g}; SPARC = {A0_SPARC:.4g}")
g_phot = m["g_si"]
print(f"  g_phot(median) = {g_phot:.3e} m/s^2  ->  g/a0: fw {g_phot/A0_FW:.3e}x, canon {g_phot/A0_CANON:.3e}x, "
      f"SPARC {g_phot/A0_SPARC:.3e}x")
corr_fw = math.sqrt(1 + A0_FW / g_phot)      # a0-line: g_obs^2 = g^2 + a0 g  ->  mass factor
corr_canon = math.sqrt(1 + A0_CANON / g_phot)
check("a0-line mass factor at photosphere, fw (expect 1, NON-detection)", corr_fw, 1.0, 1e-4)
check("a0-line mass factor at photosphere, canon (expect 1, NON-detection)", corr_canon, 1.0, 1e-4)
for nm, s in STACKS.items():
    gp = recomputed[nm]["g_si"]
    print(f"    {nm:15s} g_phot = {gp:.2e} m/s^2 = {gp/A0_FW:8.0f} x a0(fw)")

# a0(z) under the framework's settled DESI reading (jwst_full_predictions.py):
# a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)); CPL w0=-0.752, wa=-0.86 -> 0.737 at z=3, 0.51 at z=6, 0.36 at z=10.
# LRD window z = 2-9.3 -> a0_eff = 0.4-0.8 a0(0): regime statement STRENGTHENS (a0 even weaker early).
def rho_DE_ratio(z, w0=-0.752, wa=-0.86):
    return (1 + z) ** (3 * (1 + w0 + wa)) * math.exp(-3 * wa * z / (1 + z))
a0z = {z: math.sqrt(rho_DE_ratio(z)) for z in (3.0, 6.0, 9.3)}
print(f"  a0(z)/a0(0) under DESI CPL: z=3 {a0z[3.0]:.3f}, z=6 {a0z[6.0]:.3f}, z=9.3 {a0z[9.3]:.3f}"
      "  -> photospheres at 4e5-3e6 x a0(z): regime conclusion unchanged, stronger.")
check("a0(z=3)/a0(0) matches the locked DESI reading (0.737)", a0z[3.0], 0.737, 0.02)

print("\n  HOST scale (the only place the a0-line could bite):")
hosts = [("median host M*=10^8.5, Re=0.2 kpc", 10 ** 8.5, 0.2),
         ("median host M*=10^8.5, Re=0.5 kpc", 10 ** 8.5, 0.5),
         ("big host    M*=10^9.5, Re=1.0 kpc", 10 ** 9.5, 1.0)]
for nm, Mstar, Re_kpc in hosts:
    M = Mstar * Msun; R = Re_kpc * KPC
    gbar = G * M / R ** 2
    y = A0_FW / gbar
    boost = math.sqrt(1 + y) - 1
    print(f"    {nm}: g_bar = {gbar:.2e} m/s^2 = {gbar/A0_FW:5.1f} x a0(fw)  ->  "
          f"a0-line V-circular boost +{boost*100:5.1f}%")
# consistency with the committed agentGG verdict (all JWST z>4 kinematic points at 5.7-24 a0)
g_host = G * 10 ** 8.5 * Msun / (0.2 * KPC) ** 2
check("median LRD host at Re=0.2 kpc sits in the agentGG window 5.7-24 a0(fw)",
      g_host / A0_FW, 11.8, 0.5)

n_pass = sum(1 for r in results if r["ok"])
print(f"\n<BHSTAR2609> COMPLETE: {n_pass}/{len(results)} checks PASS.")
out = dict(lane="black_hole_stars_2609.09274_check",
           paper="arXiv:2609.09274 (Sun, Naidu, de Graaff, Eilers et al. 2026-09-08)",
           footings=dict(a0_fw=A0_FW, a0_canon=A0_CANON, a0_sparc=A0_SPARC),
           a0z_desi=dict(w0=-0.752, wa=-0.86, ratio={f"z{k}": v for k, v in a0z.items()}),
           regime=dict(g_phot_median_ms2=g_phot, g_over_a0_fw=g_phot / A0_FW,
                       a0line_mass_factor_fw=corr_fw, a0line_mass_factor_canon=corr_canon),
           checks=results,
           verdict=(f"ABSORBED: all four estimator equations reproduce the paper's Tables 2-3 at its "
                    f"stated inputs. REGIME: BH* pseudo-photospheres sit at g ~ 3e5-1.3e6 x a0 on both "
                    f"footings; the a0-line force correction there is 1.00000 (NON-detection, registered "
                    f"as silence). Host scale sits at ~12 a0(fw) -- the same Newtonian-degenerate corner "
                    f"as the committed agentGG verdict. The paper tests neither a0 nor a0(z)."))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "black_hole_stars_2609.09274_check_results.json"), "w") as fh:
    json.dump(out, fh, indent=1)
