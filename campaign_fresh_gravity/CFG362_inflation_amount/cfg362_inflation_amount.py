"""CFG362: can inflation fix the cold fluid amount (stochastic misalignment)? Criteria: FROZEN_CRITERIA.md (ece4d2f82).

Run: python3 cfg362_inflation_amount.py ; MUTATE=1 multiplies the de Sitter noise by 10 (T0a must fail, rc 1).
Natural units, GeV.
"""
import json, math, os, sys

MUTATE = os.environ.get("MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
TAG = "_MUTATE" if MUTATE else ""
checks, lines = [], []


def say(s=""):
    print(s)
    lines.append(s)


def check(name, ok, val):
    checks.append({"name": name, "pass": bool(ok), "value": val})
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


M_Pl = 1.220890e19
Mbar = M_Pl / math.sqrt(8 * math.pi)
eV = 1e-9
hbarc_cm = 1.973269804e-14
om_c = 0.1200
rho_c0 = om_c * 1.05375e-5 * hbarc_cm**3          # GeV^4
s0 = 2891.2 * hbarc_cm**3                          # GeV^3
T0 = 2.7255 * 8.617333e-14                         # GeV
P_zeta = 2.1e-9
NOISE = 10.0 if MUTATE else 1.0


def gstar(T):                                      # declared approximate step table (rho and s taken equal above 1 MeV)
    if T > 170: return 106.75, 106.75
    if T > 1.0: return 86.25, 86.25
    if T > 0.15: return 61.75, 61.75
    if T > 1e-3: return 10.75, 10.75
    return 3.36, 3.91


say("CFG362 inflation fixes the amount?" + ("  (MUTATE: noise x10)" if MUTATE else ""))
say("=" * 78)

# ---------------------------------------------------------------- T0
say("T0 controls")
H, m = 1.0, 0.05                                   # units of H; m/H = 0.05
phi2, dN, N = 0.0, 1e-2, 0.0
target_eq = 3 * H**4 / (8 * math.pi**2 * m**2)
N_rel_an = 3 * H**2 / (2 * m**2)
N_hit = None
while N < 12 * N_rel_an:
    phi2 += dN * ((NOISE * H / (2 * math.pi)) ** 2 - (2 * m**2 / (3 * H**2)) * phi2)
    N += dN
    if N_hit is None and phi2 >= (1 - math.exp(-1)) * target_eq:
        N_hit = N
eq_err = phi2 / target_eq - 1
rel_err = (N_hit / N_rel_an - 1) if N_hit else float("inf")
check("T0a moment equation integrated: <phi^2>_eq = 3H^4/(8 pi^2 m^2) and N_rel = 3H^2/(2m^2) reproduced to 1%",
      abs(eq_err) < 0.01 and abs(rel_err) < 0.01, f"eq {eq_err:+.2e}, N_rel (1-1/e point) {rel_err:+.2e}")
check("T0b rho_c0/s0 from the inputs", 3e-10 < rho_c0 / s0 < 6e-10, f"{rho_c0/s0:.3e} GeV per unit entropy")
j360 = json.load(open(os.path.join(HERE, "..", "CFG360_baryon_tie", "cfg360_baryon_tie_results.json")))
m_lo, m_hi = j360["window_eV"]
check("T0c mass window read from CFG360's committed JSON", 1e-21 < m_lo < 1e-19 and 1 < m_hi < 10,
      f"[{m_lo:.1e}, {m_hi:.2f}] eV")


# ---------------------------------------------------------------- T1 relation
def solve(m_GeV, gscale=1.0):
    T = 1.0
    for _ in range(60):                            # fixed point for g*(T_osc)
        g, gs = gstar(T)
        g, gs = g * gscale, gs * gscale
        T = math.sqrt(m_GeV * M_Pl / (1.66 * math.sqrt(g)))
    s_osc = 2 * math.pi**2 / 45 * gs * T**3
    rho_osc = (rho_c0 / s0) * s_osc                # n/s conserved and rho = m n both before and after
    H_I = (rho_osc * 8 * math.pi**2 / 3) ** 0.25    # complex field mean: rho_osc = 3 H^4/(8 pi^2)
    return H_I, T


say("\nT1 relation H_I(m) over the window")
grid = [m_lo * (m_hi / m_lo) ** (i / 40) for i in range(41)]
rows = []
for mm in grid:
    H_I, T = solve(mm * eV)
    rows.append((mm, H_I, T))
for mm, H_I, T in rows[::10]:
    say(f"    m = {mm:.2e} eV: H_I = {H_I:.3e} GeV, T_osc = {T:.3e} GeV")
slope = math.log(rows[-1][1] / rows[0][1]) / math.log(rows[-1][0] / rows[0][0])
Hg2 = solve(m_hi * eV, 2.0)[0] / rows[-1][1]
check("T1 relation solved over the whole window", all(r[1] > 0 for r in rows),
      f"H_I from {rows[0][1]:.2e} to {rows[-1][1]:.2e} GeV; slope d ln H_I/d ln m = {slope:.3f}; g* x2 moves H_I by x{Hg2:.3f}")

# ---------------------------------------------------------------- T2 equilibration
say("\nT2 equilibration e-folds")
t2 = []
for mm, H_I, T in rows:
    m_ = mm * eV
    N_rel = 3 * H_I**2 / (2 * m_**2)
    S_dS = math.pi * M_Pl**2 / H_I**2
    tcc = math.log(M_Pl / H_I)
    t2.append((mm, N_rel, S_dS, tcc))
ok2 = [r for r in t2 if r[1] <= r[2]]
margin = [r[2] / r[1] for r in t2]
check("T2 PRIMARY: N_rel <= S_dS (de Sitter entropy) somewhere in the window",
      len(ok2) > 0, f"{len(ok2)}/{len(t2)} grid masses pass; S_dS/N_rel from {min(margin):.2e} to {max(margin):.2e} "
      f"(N_rel {t2[0][1]:.1e} .. {t2[-1][1]:.1e} e-folds)")
say(f"    REPORTED ONLY (TCC conjecture): N_rel <= ln(M_Pl/H_I) ~ {t2[0][3]:.0f}: violated by x{t2[0][1]/t2[0][3]:.1e} .. x{t2[-1][1]/t2[-1][3]:.1e}")

# ---------------------------------------------------------------- T3 consistency
say("\nT3 consistency")
t3 = []
for mm, H_I, T in rows:
    light = mm * eV < H_I / 10
    V14 = (3 * H_I**2 * Mbar**2) ** 0.25
    reheat = V14 > 5e-3
    onset = T > 1e5 * T0
    t3.append((light, reheat, onset, V14))
check("T3a field light during inflation (m < H_I/10), whole window", all(r[0] for r in t3),
      f"max m/H_I = {max(mm*eV/H for mm, H, T in rows):.1e}")
check("T3b inflation can reheat above 5 MeV, whole window", all(r[1] for r in t3),
      f"V^(1/4) from {t3[0][3]:.2e} to {t3[-1][3]:.2e} GeV")
check("T3c fluid in place before z = 1e5 (T_osc > 1e5 T0 = {:.1e} GeV), whole window".format(1e5 * T0), all(r[2] for r in t3),
      f"min T_osc = {min(T for _, _, T in rows):.2e} GeV")
say("    T3d minimal coupling during inflation: DECLARED, not tested")

# ---------------------------------------------------------------- T4 isocurvature
say("\nT4 isocurvature")
S_amp = [2 * math.sqrt(2 / 3) * mm * eV / H_I for mm, H_I, T in rows]
P_S = max(S_amp) ** 2
check("T4 uncorrelated isocurvature P_S < 0.04 P_zeta, whole window", P_S < 0.04 * P_zeta,
      f"max S = {max(S_amp):.1e}, P_S = {P_S:.1e} vs limit {0.04*P_zeta:.1e}")

# ---------------------------------------------------------------- T5 prediction / falsifier
say("\nT5 prediction and falsifier")
r_vals = [2 * H_I**2 / (math.pi**2 * Mbar**2 * P_zeta) for _, H_I, _ in rows]
H_r3 = math.pi * Mbar * math.sqrt(1e-3 * P_zeta / 2)
falsify = H_r3 > max(H for _, H, _ in rows)
check("T5 a B-mode detection at r = 1e-3 lies above every H_I in the window (a detection excludes the route for every mass)",
      falsify, f"r predicted {min(r_vals):.1e} .. {max(r_vals):.1e}; r = 1e-3 needs H_I = {H_r3:.2e} GeV vs window max {max(H for _, H, _ in rows):.2e}")

# ---------------------------------------------------------------- T6 draw scatter
q05, q95 = -math.log(0.95), -math.log(0.05)       # exponential quantiles over the mean
say(f"\nT6 draw scatter: local amount / mean in [{q05:.3f}, {q95:.2f}] (5-95%) -> the amount is fixed only to a factor ~{q95/q05:.0f} (5-95% span); "
    "H_I inherits a 1/4-power: x[{:.2f}, {:.2f}]".format(q05 ** -0.25, q95 ** -0.25))

# ---------------------------------------------------------------- verdict
gates = len(ok2) > 0 and all(r[0] and r[1] and r[2] for r in t3) and P_S < 0.04 * P_zeta
verdict = "CONDITIONAL-TESTABLE" if gates else "NO-GO"
say(f"\nVERDICT: {verdict}. The amount is fixed by H_I (one new constant, from outside the framework) up to the T6 draw; "
    "relocated, not reduced. Falsifier: any primordial B-mode detection. The cold MASS is still required.")
n = sum(c_["pass"] for c_ in checks)
say(f"\n{n}/{len(checks)} pass" + ("  (MUTATE)" if MUTATE else ""))
json.dump({"lane": "CFG362", "mutate": MUTATE, "verdict": verdict, "window_eV": [m_lo, m_hi],
           "relation": [{"m_eV": mm, "H_I_GeV": H, "T_osc_GeV": T} for mm, H, T in rows], "slope": slope,
           "gstar_x2_factor": Hg2, "S_dS_over_Nrel": [min(margin), max(margin)], "r_range": [min(r_vals), max(r_vals)],
           "H_I_for_r_1e-3": H_r3, "draw_5_95": [q05, q95], "checks": checks},
          open(os.path.join(HERE, f"cfg362_inflation_amount_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg362_inflation_amount{TAG}.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if n == len(checks) else 1)
