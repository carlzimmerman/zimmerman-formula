#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L323 -- AUDIT OF THE BH* "REGIME COINCIDENCE" (CFJC RFC-0001, waves K/P/T/U): what it is, what it is not.

THE CLAIM AUDITED.  The Balmer layer of the little-red-dot "black hole stars" (M = 1e4 Msun, r_B = 100 au, n_H = 1e10 cm^-3)
sits at g_B / a0(rho_B) = 1.00, with a0(rho) = (c/2) sqrt(G rho) evaluated at the GAS's own density; KP1
r_B^4 n_H c^2 mu m_p = 4 G M^2 and KP2 v_inf ~ M^{1/4} were derived from it; wave U called Gamma = 56.6 "13% above the cap".

WHAT THIS LANE CHECKS (both directions -- a demotion is verified as hard as a win):
  R1  control: the fiducial ratio is reproduced (1.00).
  R2  the ratio is a pure kinematic number: g / a0(rho) = 2 (v_c/c) (t_ff/t_dyn), t_ff = 1/sqrt(G rho), t_dyn = r/v_c
      (Lean I17 ratio_is_freefall_kinematics) -- a0(rho_gas) is c times the gas free-fall rate, not the framework's scale.
  R3  a crossing is GUARANTEED: for any envelope rho ~ r^-p with p < 4 the ratio ~ r^(p/2 - 2) is strictly decreasing and
      crosses 1 exactly once (Lean I17 unique_crossing); across the paper's whole (n_H, M) band it lands inside the envelope.
  R4  the chance probability that the guaranteed crossing lands within x2 of the Balmer layer (null: crossing log-uniform
      over the envelope) and the propagated uncertainty of the "1.001 +/- 0.02" ratio from the paper's own input ranges.
  R5  the same classifier labels the air at the Earth's surface "strong-a0" (g/a0(rho_air) << 1) where gravity is
      Newtonian to high precision: the label carries no dynamics (the paper concedes "classifier, not mechanism").
  R6  the framework's ACTUAL scale (flat a0, both footings): every BH* layer is deep-Newtonian => the framework's own
      prediction for BH* envelopes is a NULL (no a0 signature), not a coincidence.
  R7  KP2's exponent 1/4 follows from the published family scaling alone (r_B = f R_phot ~ sqrt M at fixed T_eff, Gamma):
      it does not test the density form (Lean I17 kp2_from_family).
  R8  wave U's Gamma: composition (kappa_es 0.40 vs 0.34 cm^2/g) and the published log g = -2.2 +/- 0.2.
  R9  I10's "tau_ion >= 1e3 tau_es for f_n > 1e-4": 9.47e6 x 1e-4 = 947 < 1e3 (Lean I17 void_threshold).
REFERENCE (not re-run here): the density form as an ENVIRONMENTAL law (a0 ~ sqrt(rho_local), slope +0.5) is excluded on the
175 SPARC galaxies at 13.0 sigma (internal) / ~34 sigma (kNN) / 6.8 sigma (2M++ real-space field):
real_research/A0_DENSITY_EMPIRICAL_EVIDENCE.md, real_research/reviews/A0_COSMICWEB_ENVIRONMENT_2026-06.md and
real_research/reviews/project_sparc_a0_vs_cosmicweb.py.
MUTATE=1 sets the envelope slope to p = 5 (steeper than the p < 4 theorem allows): R3's guaranteed-crossing check must FAIL.

Run from the repository root:  python3 real_research/bhstar_audit_2026/L323_bhstar_regime_coincidence_audit.py
"""
import os, sys, json, math, random

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L323_bhstar_regime_coincidence_audit"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L323", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__)
G, C, MSUN, AU, MP = 6.6743e-11, 2.99792458e8, 1.98892e30, 1.495978707e11, 1.67262192e-27
SIGMA_SB = 5.670374419e-8
A0_FLAT = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
MU = 1.4                                  # mass per H atom (the campaign's convention, CFJC eq. 4)
M_FID, RB_FID, N_FID = 1e4, 100.0, 1e10   # Msun, au, cm^-3
R_PHOT = 941.0                            # au, median stack (CFJC Table 2)
P_SLOPE = 5.0 if MUTATE else 2.0          # envelope rho ~ r^-p


def rho_of_n(n_cm3): return MU * MP * n_cm3 * 1e6                      # kg/m^3
def a0_rho(rho): return 0.5 * C * math.sqrt(G * rho)
def g_at(M, r_au): return G * M * MSUN / (r_au * AU) ** 2


# ================================================================= R1
banner("R1 -- CONTROL: the fiducial regime ratio")
ratio_fid = g_at(M_FID, RB_FID) / a0_rho(rho_of_n(N_FID))
OUT["numbers"]["ratio_fiducial"] = ratio_fid
check("R1 g_B/a0(rho_B) at (1e4 Msun, 100 au, 1e10 cm^-3, mu = 1.4) within 1% of 1.00", f"{ratio_fid:.4f}",
      abs(ratio_fid - 1) < 0.01, "reproduced; the question is what it means")

# ================================================================= R2
banner("R2 -- THE RATIO IS A KINEMATIC NUMBER: g/a0(rho) = 2 (v_c/c)(t_ff/t_dyn)")
r = RB_FID * AU; rho = rho_of_n(N_FID); v = math.sqrt(G * M_FID * MSUN / r)
t_ff, t_dyn = 1 / math.sqrt(G * rho), r / v
rhs = 2 * (v / C) * (t_ff / t_dyn)
OUT["numbers"]["R2"] = {"v_c_over_c": v / C, "t_ff_yr": t_ff / 3.156e7, "t_dyn_yr": t_dyn / 3.156e7, "t_ff_over_t_dyn": t_ff / t_dyn}
P(f"   v_c/c = {v/C:.3e}   t_ff(gas) = {t_ff/3.156e7:.0f} yr   t_dyn = {t_dyn/3.156e7:.2f} yr   t_ff/t_dyn = {t_ff/t_dyn:.0f}")
check("R2 |g/a0(rho) - 2(v_c/c)(t_ff/t_dyn)| / ratio < 1e-12", f"{abs(ratio_fid - rhs)/ratio_fid:.1e}",
      abs(ratio_fid - rhs) / ratio_fid < 1e-12,
      "'1.00' = (v_c/c ~ 1e-3) x (t_ff/t_dyn ~ 500) x 2: two unrelated ratios of THIS envelope; no cosmic density enters")

# ================================================================= R3
banner(f"R3 -- THE CROSSING IS GUARANTEED (envelope rho ~ r^-{P_SLOPE:g})")
ok3, rows = True, []
for logM in (3.4, 3.7, 4.0, 4.3):
    M = 10 ** logM
    rB = RB_FID * math.sqrt(M / M_FID)                  # published family: r_B = f R_phot ~ sqrt(M)
    Rph = R_PHOT * math.sqrt(M / M_FID)
    for logn in (9.0, 10.0, 11.0):
        def ratio_r(r_au):
            n = 10 ** logn * (rB / r_au) ** P_SLOPE
            return g_at(M, r_au) / a0_rho(rho_of_n(n))
        grid = [rB * 10 ** (k / 50) for k in range(-100, 101)]      # 1e-2 .. 1e2 x r_B
        vals = [ratio_r(x) for x in grid]
        mono = all(vals[i] > vals[i + 1] for i in range(len(vals) - 1))
        r_in = rB * (10 ** logn / 1e12) ** (1 / P_SLOPE)           # where n reaches 1e12 cm^-3 (envelope inner edge)
        inside = ratio_r(r_in) > 1 > ratio_r(Rph)
        rows.append({"logM": logM, "logn_at_rB": logn, "monotone_decreasing": mono, "crossing_inside_envelope": inside,
                     "ratio_at_rB": ratio_r(rB)})
        ok3 &= mono and inside
OUT["numbers"]["R3"] = rows
check("R3 ratio strictly decreasing outward AND crossing 1 between n = 1e12 and the photosphere, for all 12 (M, n) cases",
      f"{sum(1 for x in rows if x['monotone_decreasing'] and x['crossing_inside_envelope'])}/12", ok3,
      "a g = a0(rho) surface exists inside EVERY such envelope for every allowed parameter -- its existence is not a finding")

# ================================================================= R4
banner("R4 -- CHANCE PROBABILITY AND THE HONEST ERROR BAR")
r_in_fid, r_out_fid = RB_FID * math.sqrt(N_FID / 1e12), R_PHOT
p_chance = math.log10(4.0) / math.log10(r_out_fid / r_in_fid)   # crossing within x2 either side of r_B, log-uniform null
random.seed(20260922)
logs = []
for _ in range(200000):
    ln_ = random.uniform(9.0, 11.0)                    # CLOUDY band quoted by the campaign
    lf = random.uniform(-0.3, 0.3)                     # r_B/R_phot unmeasured (P1 audit): x2 either side of f = 0.106
    lr0 = random.uniform(-0.1, 0.1)                    # family-constant scatter x1.6 (CFJC Table 2)
    logs.append(math.log10(ratio_fid) - 0.5 * (ln_ - 10.0) - 2 * lf - 2 * lr0)
mean = sum(logs) / len(logs); sd = math.sqrt(sum((x - mean) ** 2 for x in logs) / len(logs))
OUT["numbers"]["R4"] = {"p_chance_within_x2_of_rB": p_chance, "log_ratio_sd_dex": sd,
                        "envelope_au": [r_in_fid, r_out_fid]}
P(f"   envelope {r_in_fid:.0f}-{r_out_fid:.0f} au; P(crossing within x2 of r_B | log-uniform) = {p_chance:.2f}")
P(f"   propagated from the campaign's own input ranges: log10(g_B/a0) = 0.00 +/- {sd:.2f} dex (ratio x/÷ {10**sd:.1f})")
check("R4 the coincidence is NOT significant: P(chance) > 0.05 and the ratio's honest error bar exceeds 0.2 dex",
      f"P = {p_chance:.2f}; sd = {sd:.2f} dex (the paper quotes +/- 0.02, i.e. 0.009 dex)", p_chance > 0.05 and sd > 0.2,
      "'1.001 +/- 0.02' is the precision of round inputs, not of a measurement; one named layer in a 2-dex envelope "
      "catches a guaranteed crossing ~1/3 of the time")

# ================================================================= R5
banner("R5 -- THE CLASSIFIER ON LABORATORY MATTER")
lab = {"Earth surface air (1.2 kg/m^3, g = 9.81)": (9.81, 1.2), "Earth crust (2700 kg/m^3, g = 9.81)": (9.81, 2700.0),
       "solar photosphere (2e-4 kg/m^3, g = 274)": (274.0, 2e-4)}
labrows = {}
for k, (g, rh) in lab.items():
    labrows[k] = g / a0_rho(rh)
    P(f"   {k:44s}: g/a0(rho) = {labrows[k]:.2e}")
OUT["numbers"]["R5"] = labrows
check("R5 the Earth's surface air is 'strong-a0' by the same classifier (ratio < 0.1, deeper than the BH* photosphere's 0.10)",
      f"{labrows['Earth surface air (1.2 kg/m^3, g = 9.81)']:.4f}", labrows["Earth surface air (1.2 kg/m^3, g = 9.81)"] < 0.1,
      "every laboratory torsion balance sits on the 'strong' side; the label has no dynamical content, so the layer "
      "coinciding with it predicts nothing the framework can be held to")

# ================================================================= R6
banner("R6 -- THE FRAMEWORK'S OWN SCALE (flat a0): every BH* layer is deep-Newtonian")
g_phot = 10 ** (-2.2 - 2)                                    # log g = -2.2 cgs -> m/s^2
mins = {}
for fk, a0 in A0_FLAT.items():
    mins[fk] = {"g_B/a0": g_at(M_FID, RB_FID) / a0, "g_phot/a0": g_phot / a0,
                "r_M_pc(1e4 Msun)": math.sqrt(G * M_FID * MSUN / a0) / 3.0857e16}
    P(f"   {fk:9s}: g_B/a0 = {mins[fk]['g_B/a0']:.2e}   g_phot/a0 = {mins[fk]['g_phot/a0']:.2e}   "
      f"r_M = {mins[fk]['r_M_pc(1e4 Msun)']:.2f} pc (photosphere ~ {R_PHOT/206265:.4f} pc)")
OUT["numbers"]["R6"] = mins
check("R6 g/a0_flat >= 1e5 at the Balmer layer and the photosphere, both footings",
      f"min = {min(min(v['g_B/a0'], v['g_phot/a0']) for v in mins.values()):.2e}",
      all(min(v["g_B/a0"], v["g_phot/a0"]) >= 1e5 for v in mins.values()),
      "on its own terms the framework predicts NO a0 signature in any BH* envelope (a null, consistent with CFJC Thm 3's "
      "1e-6 a0-blindness of the mass chain); the only BH* object with an a0 lever is the naked-BH host (L324)")

# ================================================================= R7
banner("R7 -- KP2's EXPONENT COMES FROM THE PUBLISHED FAMILY SCALING, NOT THE DENSITY FORM")
xs, ys = [], []
for i in range(10):
    logM = 3.4 + 0.1 * i
    M = 10 ** logM
    rB = RB_FID * math.sqrt(M / M_FID) * AU                   # family only; no a0(rho) anywhere
    xs.append(logM); ys.append(math.log10(math.sqrt(2 * G * M * MSUN / rB)))
xb, yb = sum(xs) / len(xs), sum(ys) / len(ys)
slope = sum((x - xb) * (y - yb) for x, y in zip(xs, ys)) / sum((x - xb) ** 2 for x in xs)
OUT["numbers"]["R7_slope"] = slope
check("R7 d log v_esc(r_B) / d log M = 0.250 under the family scaling alone", f"{slope:.6f}", abs(slope - 0.25) < 1e-9,
      "KP2 (v ~ M^1/4) tests the published recombination-pinned family, not the framework; KP1 at a common n likewise "
      "reduces to r_B ~ sqrt(M) plus one normalisation, and that normalisation is the fiducial chosen at r_B = 100 au")

# ================================================================= R8
banner("R8 -- WAVE U's GAMMA: composition and the published log g error")
T, LOGG, DLOGG = 4662.0, -2.2, 0.2
gam = {}
for kap_cgs in (0.40, 0.34):
    for dl in (-DLOGG, 0.0, DLOGG):
        gam[f"kappa={kap_cgs}, logg={LOGG+dl:+.1f}"] = (kap_cgs / 10) * SIGMA_SB * T ** 4 / (C * 10 ** (LOGG + dl - 2))
for k, v in gam.items():
    P(f"   {k:26s}: Gamma = {v:6.1f}")
OUT["numbers"]["R8"] = gam
g40, g34 = gam["kappa=0.4, logg=-2.2"], gam["kappa=0.34, logg=-2.2"]
check("R8 the cap 50 lies inside the +/-0.2 dex band for both compositions, and X = 0.7 puts the central value below it",
      f"Gamma = {g40:.1f} (pure H) / {g34:.1f} (X = 0.7); band [{min(gam.values()):.0f}, {max(gam.values()):.0f}]",
      g34 < 50 < g40 and all(gam[f"kappa={k}, logg={LOGG+DLOGG:+.1f}"] < 50 < gam[f"kappa={k}, logg={LOGG-DLOGG:+.1f}"]
                             for k in (0.4, 0.34)),
      "'13% above the cap' is inside the error and flips sign with solar composition; the identity itself is L/L_Edd "
      "with M from log g (standard), not a new observable")

# ================================================================= R9
banner("R9 -- I10's '>= 1e3 at 0.01% neutral'")
prod = 9.47e6 * 1e-4
OUT["numbers"]["R9"] = {"R_sigma_x_1e-4": prod, "fn_threshold_for_1e3": 1e3 / 9.47e6}
check("R9 9.47e6 x 1e-4 < 1e3 (the docstring's claim is off; threshold f_n = 1.056e-4; theorem proves 1e2)",
      f"{prod:.0f}; threshold {1e3/9.47e6:.4e}", prod < 1e3, "a 5% prose error; the void verdict (>= 2 dex) survives")

lb = [c for c in CH if c[2]]
npass = sum(1 for c in lb if c[1])
banner(f"VERDICT  ({npass}/{len(lb)} load-bearing PASS{'  -- MUTATE RUN' if MUTATE else ''})")
P("""  * The BH* 'regime coincidence' is NOT a framework result: it uses a0 at the gas's own density (a branch the framework does
    not use and the SPARC environment test excludes as a law), its ratio is 2(v_c/c)(t_ff/t_dyn), a crossing is
    guaranteed inside every envelope, and the chance that it lands within x2 of the one named layer is ~1/3.
  * The framework's own (flat-a0) prediction for BH* envelopes is a NULL: every layer is >= 1e5 a0.
  * KP2's exponent is the published family's; wave U's 'Gamma 13% above cap' is inside errors and composition-dependent.
  * Nothing here refutes the framework and nothing here supports it: the BH* campaign's framework-facing claims carry no
    evidential weight either way.  The one live framework test in the BH* sample is A2744-QSO1 (L324).""")
OUT["verdict"] = {"load_bearing_pass": npass, "load_bearing_total": len(lb)}
suffix = "_MUTATE" if MUTATE else ""
with open(os.path.join(HERE, f"{SLUG}_results{suffix}.json"), "w") as f:
    json.dump(OUT, f, indent=1, default=str)
sys.exit(0 if npass == len(lb) else 1)
