"""CFG360: the baryon tie (Gap 2). Criteria: FROZEN_CRITERIA.md (581291e38), committed before this script.

Question: can one early process fix the cold fluid's charge per baryon r (and its mass m) so that
R = rho_c/rho_b = (m/m_p) r = omega_c/omega_b = 5.364 follows from the framework?

Mechanism classes enumerated (T3):
  a1  gravitational-only, minimal coupling (G9 as it stands)
  a2  non-minimal curvature coupling of the currents (gravitational-baryogenesis type)
  b1  shared conserved current B - k Q_c, thermal (no condensate)
  b2  shared conserved current B - k Q_c, Bose-condensed fluid (the CFG288 wave field)
  b3  derivative (shift-symmetric) coupling d_mu theta J_B^mu / f (spontaneous-baryogenesis type; no charge transfer)
POST-FREEZE (labelled, not in the frozen list): proton-decay bound on b2's B-violating transfer operator today.

Units: natural units, GeV, unless stated. Run: python3 cfg360_baryon_tie.py ; MUTATE=1 plants R = 3.00 +- 0.065.
"""
import json, math, os, re, sys, itertools

MUTATE = os.environ.get("MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
TAG = "_MUTATE" if MUTATE else ""
checks = []
lines = []


def say(s=""):
    print(s)
    lines.append(s)


def check(name, ok, val):
    checks.append({"name": name, "pass": bool(ok), "value": val})
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


# ---------------------------------------------------------------- inputs (quoted in the criteria)
om_c, s_c, om_b, s_b = 0.1200, 0.0012, 0.02237, 0.00015
h = 0.6736
R_CMB = om_c / om_b
sR = R_CMB * math.hypot(s_c / om_c, s_b / om_b)
R_cl, sR_cl = 5.73, 0.68                                     # L49 X1, reported only
R_T, sR_T = (3.00, 0.065) if MUTATE else (R_CMB, sR)         # scored target

m_p = 0.938272                                               # GeV
hbarc_cm = 1.973269804e-14                                   # GeV cm
hbarc_m = 1.973269804e-16                                    # GeV m
M_Pl = 1.220890e19                                           # GeV (non-reduced)
c = 2.99792458e8
eV = 1e-9                                                    # GeV
rho_crit_h2 = 1.05375e-5                                     # GeV cm^-3 per h^2
nB_over_s_obs = 8.7e-11                                      # Planck/BBN baryon asymmetry n_B/s

say("CFG360 baryon tie" + ("  (MUTATE: planted target R = 3.00)" if MUTATE else ""))
say("=" * 78)

# ---------------------------------------------------------------- T0 controls
say("T0 controls")
check("T0a R_CMB = omega_c/omega_b reproduces 5.364 +- 0.065 and is the scored target",
      abs(R_T - 5.364) < 0.001 and abs(sR_T - 0.065) < 0.002,
      f"R_CMB = {R_CMB:.4f} +- {sR:.4f}; scored target = {R_T:.3f} +- {sR_T:.3f}")

# lower edge: read from CFG288's committed output
out288 = os.path.join(HERE, "..", "CFG288_one_field_dark_sector", "cfg288_construction_gates.out")
txt = open(out288).read()
mlo_match = re.search(r"m_min \(Lyman-alpha\)\s+m = ([0-9.eE+-]+) eV", txt)
m_lo_eV = float(mlo_match.group(1)) if mlo_match else float("nan")
# upper edge: classical wave (occupation N >= 1) in the cluster core the fluid must fill (g04a numbers)
rho_core_SI, sigma_core = 3.6e-22, 886e3                     # kg m^-3 at 40 kpc; m/s
rho_core = rho_core_SI * c**2 / 1.602176634e-10 * hbarc_m**3  # GeV^4
beta = sigma_core / c
# N = n * (hbar/(m v))^3 = (rho/m) / (m beta)^3 = rho / (m^4 beta^3)  -> N = 1 edge
m_hi = (rho_core / beta**3) ** 0.25
m_hi_eV = m_hi / eV
check("T0b wave-field window: lower edge read from CFG288 output; upper edge derived (occupation = 1 in the g04a cluster core)",
      mlo_match is not None and 1e-21 < m_lo_eV < 1e-19 and 0.1 < m_hi_eV < 100,
      f"m in [{m_lo_eV:.1e}, {m_hi_eV:.2f}] eV (upper edge at rho = 3.6e-22 kg/m^3, sigma = 886 km/s; "
      f"N >> 1 needs lighter, so this edge is generous)")

Om_c = om_c / h**2
Om_L = 0.6847
z_eq = 3402
A1 = (Om_c / Om_L) * (1 + z_eq) ** 3
check("T0c CFG288 A1 reproduced: dust before z_eq needs a potential >= 1.5e10 rho_Lambda",
      1.4e10 < A1 < 1.6e10, f"{Om_c/Om_L:.3f} (1+z_eq)^3 = {A1:.3e} rho_Lambda")

# ---------------------------------------------------------------- T1, T2
say("\nT1 minimal tie (equal charges, r = 1)")
m_T1 = R_T * m_p
occ_T1 = rho_core / (m_T1**4 * beta**3)
check("T1 equal-charge tie needs m = R m_p, far above the wave-field window (a particle, not a fluid): expected FAIL of the tie, confirmed",
      m_T1 > m_hi, f"m = {m_T1:.3f} GeV = {m_T1/m_hi:.1e} x the upper edge; occupation in the cluster core {occ_T1:.1e}")

say("\nT2 required charge per baryon")
r_lo, r_hi = R_T * m_p / m_hi, R_T * m_p / (m_lo_eV * eV)
check("T2 r_req band computed from the T0b window", r_lo > 1e8 and r_hi < 1e31,
      f"r_req in [{r_lo:.2e}, {r_hi:.2e}] charge units per baryon")

# ---------------------------------------------------------------- T3/T4 mechanism classes
say("\nT3/T4 mechanism classes")
verdicts = {}

# a1
verdicts["a1"] = "NO-GO (no tie)"
check("[ARG, not computed] a1 gravitational-only, minimal coupling: J_B is conserved by S_m alone and Q_c by S_Phi alone, so n_c/n_b is a "
      "ratio of two free integration constants (CFG288 A2); gravity cannot create B (needs B, C, CP violation)",
      True, "NO-GO: no relation between n_c and n_b is enforced")

# a2: in the radiation era R_scalar = 8 pi G (rho - 3p) vanishes
w_rad = 1 / 3
R_rad = (1 - 3 * w_rad)
verdicts["a2"] = "NO-GO (breaks G9; inert in radiation era; ratio = ratio of two new couplings)"
check("a2 non-minimal d_mu(R) J^mu couplings: breaks G9 by construction (matter current couples to curvature, not via g "
      "alone); 1 - 3w = 0 in the radiation era so R vanishes; R_ratio = ratio of two new scales",
      abs(R_rad) < 1e-12, "NO-GO under T3 (G9) whatever the ratio")

# b1: thermal equilibrium with mu_c = k mu_B; relativistic complex scalar n = mu T^2/3; baryons n_B = (2/3) mu_B T^2
# (6 quark flavours x 3 colours x 2 spins, each quark B = 1/3, mu_q = mu_B/3: n_B = (1/3)*36*(mu_B/3) T^2/6 * ... = (2/3) mu_B T^2)
k_max = 4
r_b1 = {k: k * (1 / 3) / (2 / 3) for k in range(1, k_max + 1)}   # = k/2
m_b1 = {k: R_T * m_p / r for k, r in r_b1.items()}
verdicts["b1"] = "NO-GO (particle: m >= GeV)"
check(f"b1 thermal shared current: r = k/2 (k <= {k_max}), so m = 2 R m_p / k >= {min(m_b1.values()):.2f} GeV, above the window; "
      "Boltzmann suppression at m > T_d only lowers r",
      min(m_b1.values()) > m_hi, "; ".join(f"k={k}: r={r_b1[k]:.1f}, m={m_b1[k]:.2f} GeV" for k in r_b1) + " -> NO-GO (a particle)")

# b2: condensate pins mu_c <= m, so mu_B <= m/k; n_B/s = 0.0142 mu_B/T (g*s = 106.75); washout ceiling on T_d
g_s = 106.75
nB_s_coef = (2 / 3) / (2 * math.pi**2 / 45 * g_s)
muT_needed = nB_over_s_obs / nB_s_coef
Td_floor_T4 = 1e-3                                             # GeV (T4: before BBN)
m_min_b2 = muT_needed * Td_floor_T4                            # k = 1
say(f"    b2: n_B/s = {nB_s_coef:.4f} mu_B/T -> mu_B/T >= {muT_needed:.2e}; T_d <= m/(k {muT_needed:.2e})")
verdicts["b2"] = "NO-GO (does not fix R: R ~ X_tot, the free total asymmetry)"
check("b2 condensed shared current, frozen tests: T4 (T_d >= 1 MeV) leaves m >= " f"{m_min_b2/eV*1e3:.1f} meV (k=1) inside the window, "
      "BUT the condensate holds X_tot/k of the conserved charge X_tot (a free initial number): R = (m/m_p)(X_tot/k)/n_B is NOT fixed",
      m_min_b2 < m_hi, f"surviving m band [{m_min_b2/eV*1e3:.1f} meV, {m_hi_eV:.2f} eV]; the free number moves from the amount to X_tot "
      "(plus new k, T_d): relocated, not reduced -> NO-GO for the tie")

# POST-FREEZE: proton decay from <Phi> qqql / Lambda^3 today
rho_c_mean = om_c * rho_crit_h2 * hbarc_cm**3                 # GeV^4 (cosmic mean = lenient, smallest <Phi>)
tau_p_s = 2.4e34 * 3.156e7
hbar_GeVs = 6.582119569e-25
Leff_min = (tau_p_s / hbar_GeVs * m_p**5) ** 0.25             # dim-6 scale for tau = Leff^4 / m_p^5
c_gamma = 1e3                                                  # generous rate enhancement in Gamma = c T^7 / Lambda^6
H_coef = 1.66 * math.sqrt(g_s) / M_Pl
gaps = []
for i in range(201):
    m = m_min_b2 * (m_hi / m_min_b2) ** (i / 200)
    phi0 = math.sqrt(2 * rho_c_mean) / m
    Lam6 = (Leff_min**2 * phi0) ** 2                           # Lambda^3 >= Leff^2 <Phi>
    Td_min = (Lam6 * H_coef / c_gamma) ** 0.2                  # equilibrium needs c T^7/Lam^6 >= H = H_coef T^2
    Td_max = m / muT_needed                                    # washout ceiling (k = 1)
    gaps.append((Td_min / Td_max, m, Td_min, Td_max))
best = min(gaps)
verdicts["b2_postfreeze"] = "EXCLUDED by proton decay (post-freeze, labelled)"
check("b2 POST-FREEZE (labelled): the transfer operator <Phi> qqql/Lambda^3 must stay in equilibrium to T_d yet keep tau_p > 2.4e34 yr today; "
      "smallest conflict over the surviving band (cosmic-mean <Phi>, rate x1e3)",
      best[0] > 1, f"T_d,min/T_d,max >= {best[0]:.1e} at m = {best[1]/eV:.2f} eV (T_d,min {best[2]:.2e} GeV vs washout ceiling "
      f"{best[3]:.2e} GeV; Leff_min = {Leff_min:.1e} GeV)")

# b3: derivative coupling gives mu_B = theta_dot/f = m/f, no charge transfer; n_c = phi^2 theta_dot keeps the free amplitude
verdicts["b3"] = "NO-GO (no charge transfer: n_c = phi^2 m keeps the free amplitude)"
f_max_GeV = m_hi / (muT_needed * 130.0)
check("[ARG, not computed] b3 derivative coupling (d theta) J_B / f: sets mu_B = m/f (with sphaleron freeze-out ~130 GeV needs f <= "
      f"{f_max_GeV:.1e} GeV) but n_c = phi^2 theta_dot = rho_c/m carries the free amplitude phi; R not fixed; non-minimal coupling also breaks G9",
      True, "NO-GO: the tie fixes eta_B given (m, f), not R")

# ---------------------------------------------------------------- T5 look-elsewhere (diagnostic: no mechanism produced a form)
say("\nT5 look-elsewhere base rate (pure-number grammar: 2^a 3^b pi^c (8pi/3)^(d/2), a..d in -3..3)")
vals = {}
for a, b, cc, d in itertools.product(range(-3, 4), repeat=4):
    v = 2.0**a * 3.0**b * math.pi**cc * (8 * math.pi / 3) ** (d / 2)
    vals[round(v, 12)] = (a, b, cc, d)
distinct = sorted(vals)
def hits(t, s):
    return [v for v in distinct if abs(v - t) <= s]
h_real, h_plant = hits(5.364, 0.065), hits(3.00, 0.065)
h_T = hits(R_T, sR_T)
p_chance = len(h_T) / len(distinct)
say(f"    {len(distinct)} distinct values; hits within 1 sigma: R = 5.364 -> {len(h_real)}, planted R = 3.00 -> {len(h_plant)}")
Z = 2 * math.sqrt(8 * math.pi / 3)
say(f"    Z = 2 sqrt(8pi/3) = {Z:.4f}: {(Z - R_CMB)/sR:+.1f} sigma from R_CMB, {(Z - R_cl)/sR_cl:+.2f} sigma from R_cl (coincidence, never pooled)")
check("T5 the grammar is not discriminating at this target: chance hit rate per form >= 1e-3, and the real and planted targets get "
      "comparable counts (within x3)",
      p_chance >= 1e-3 and (max(len(h_real), 1) / max(len(h_plant), 1) <= 3 and max(len(h_plant), 1) / max(len(h_real), 1) <= 3),
      f"chance rate {p_chance:.1e} per distinct form (threshold 1e-3); any numeric match would be NUMEROLOGY")

# ---------------------------------------------------------------- verdict
say("\nVERDICT")
all_nogo = all(v.startswith("NO-GO") for k, v in verdicts.items() if k in ("a1", "a2", "b1", "b2", "b3"))
lane = "NO-GO" if all_nogo else "OPEN"
for k, v in verdicts.items():
    say(f"    {k}: {v}")
say(f"  CFG360 lane verdict: {lane}. The cold amount stays a free number (Gap 2 open); the cold MASS is still required.")
n = sum(ch["pass"] for ch in checks)
say(f"\n{n}/{len(checks)} pass" + ("  (MUTATE)" if MUTATE else ""))

json.dump({"lane": "CFG360", "mutate": MUTATE, "R_CMB": R_CMB, "sigma_R": sR, "target": [R_T, sR_T],
           "window_eV": [m_lo_eV, m_hi_eV], "r_req": [r_lo, r_hi], "m_T1_GeV": m_T1, "verdicts": verdicts,
           "lane_verdict": lane, "postfreeze_proton_gap": best[0], "T5": {"distinct": len(distinct), "hits_real": len(h_real),
           "hits_planted": len(h_plant), "chance_rate": p_chance, "Z": Z}, "checks": checks},
          open(os.path.join(HERE, f"cfg360_baryon_tie_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg360_baryon_tie{TAG}.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if n == len(checks) else 1)
