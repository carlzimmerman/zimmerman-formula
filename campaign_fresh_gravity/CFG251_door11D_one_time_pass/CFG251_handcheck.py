#!/usr/bin/env python3
"""CFG251 -- door 11D (a one-time passage of the dark-energy flow): phase-1 hand-check.

Frozen criteria: campaign_fresh_gravity/CFG251_FROZEN_CRITERIA.md (sha256 in
CFG251_FROZEN_CRITERIA_SHA256.txt, recorded before this script existed).

Every input number is read from a COMMITTED file of the repository (JSON, .out or README/markdown); each is
printed with its path. The only computations are: unit translations of the committed sky-dipole bound, the
comoving horizon / distance integrals and the linear growth equation at the committed cosmological parameters,
and ratios of committed numbers. No data are fetched, no knob is scanned, nothing in the repository is edited.

Modes (outputs named by mode, never overwritten across modes):
  MUTATE=0 (default) -> CFG251_handcheck.out / CFG251_handcheck_results.json
  MUTATE=1           -> the declared front passes at z_pass = 1: reading (i)'s headline T1 must FAIL (exit 1)
  MUTATE=2           -> (iii-b) "a pass at any collapse" scored as reading (iii)'s primary: H2 and G5 must FAIL (exit 1)
kappa = 1/2 is FITTED. Nothing here says the theory is closed or that any data favour it.
"""
import json
import math
import os
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
MUTATE = os.environ.get("MUTATE", "0").strip() or "0"
if MUTATE not in ("0", "1", "2"):
    raise SystemExit("MUTATE must be 0, 1 or 2")
TAG = "" if MUTATE == "0" else "_MUTATE%s" % MUTATE
OUT = HERE / ("CFG251_handcheck%s.out" % TAG)
RES = HERE / ("CFG251_handcheck%s_results.json" % TAG)

LINES, CHECKS, NUM, SOURCES = [], [], {}, []


def P(s=""):
    LINES.append(s)


def H(title):
    P("")
    P("=" * 110)
    P(title)
    P("=" * 110)


def cite(path, what):
    SOURCES.append({"path": path, "what": what})
    return "<repo>/" + path


def J(path):
    with open(REPO / path) as fh:
        return json.load(fh)


def T(path):
    return (REPO / path).read_text()


def rx(pattern, text, what, cast=float, group=None):
    m = re.search(pattern, text)
    if not m:
        raise SystemExit("pattern for %s not found: %r" % (what, pattern))
    if group is None:
        return tuple(cast(g) for g in m.groups()) if len(m.groups()) > 1 else cast(m.group(1))
    return cast(m.group(group))


def check(name, ok, detail, load_bearing=True):
    CHECKS.append({"name": name, "ok": bool(ok), "detail": detail, "load_bearing": load_bearing})
    P("  [%s]%s %s" % ("PASS" if ok else "FAIL", "" if load_bearing else " (reported)", name))
    P("         " + detail)


def simpson(f, a, b, n):
    if n % 2:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3.0


P("CFG251 -- door 11D, a one-time passage of the dark-energy flow: phase-1 hand-check (MUTATE=%s)" % MUTATE)
P("The owner's idea, from a dream; a hypothesis to test, not evidence. Readings (i) cosmic front, (ii) per-system")
P("passage at formation, (iii) set once at first decoupling from the Hubble flow, then frozen -- scored separately.")
P("Numbers are read from committed files only; kappa = 1/2 FITTED; P2 primary.")

# ------------------------------------------------------------------------------------------------------------
H("S1  T2 -- the committed a0 sky-dipole bound, translated into a maximum anisotropy of an imprint")
f182 = "campaign_fresh_gravity/CFG182_a0_sky_dipole/cfg182_b_dipole_results.json"
d182 = J(f182)
A95 = d182["numbers"]["upper_limit"]["A95"]
Ahat = d182["numbers"]["primary"]["A"]
sigA = d182["numbers"]["bootstrap"]["sigA"]
pA = d182["numbers"]["permutation"]["pA"]
cmb_hi = d182["numbers"]["fixed_directions"]["CMB dipole (264.0, 48.3)"]["hi95"]
P("  %s" % cite(f182, "A-hat, bootstrap sigma_A, permutation p, A95 (random direction), 95% upper end along the CMB dipole"))
P("    A-hat = %.3f +- %.3f (p = %.3f); A95 = %.3f; along the CMB dipole direction the 95%% upper end is %.3f"
  % (Ahat, sigA, pA, A95, cmb_hi))
f192m = "campaign_fresh_gravity/CFG192_sky_dipole_referee/CFG192_main.json"
A95_ref = J(f192m)["numbers"]["summary"]["A95"]
f192cd = "campaign_fresh_gravity/CFG192_sky_dipole_referee/CFG192_attacks_CD.json"
nested = J(f192cd)["numbers"]["results"]["C2_nested"]
power = {k: v[0] for k, v in nested.items()}
P("  %s -> referee A95 = %.3f" % (cite(f192m, "referee Neyman A95"), A95_ref))
P("  %s -> detection power (p < 0.05, look-elsewhere included) at A = %s: %s"
  % (cite(f192cd, "nested detection power"), ", ".join(power), ", ".join("%.2f" % power[k] for k in power)))
rows = []
for label, eps in (("A95 (CFG182, random direction)", A95), ("A95 (CFG192 referee)", A95_ref),
                   ("upper end along the CMB dipole (CFG182)", cmb_hi)):
    ratio = (1 + eps) / (1 - eps)
    g_up, g_dn = math.sqrt(1 + eps) - 1, 1 - math.sqrt(1 - eps)
    dg = (math.sqrt(1 + eps) - math.sqrt(1 - eps)) / (math.sqrt(1 + eps) + math.sqrt(1 - eps))
    rows.append({"label": label, "eps": eps, "a0_up_over_down": ratio, "deep_force_up": g_up,
                 "deep_force_down": g_dn, "deep_force_dipole_exact": dg, "deep_force_dipole_linear": eps / 2,
                 "imprint_amount_dipole": eps})
    P("    %-42s eps < %.3f: a0 upwind/downwind < %.2f; deep-MOND force +%.3f / -%.3f (dipole %.3f exact, %.3f linear);"
      % (label, eps, ratio, g_up, g_dn, dg, eps / 2))
    P("    %-42s the imprint amount C(r) = (a0/4pi) M_b(<r) is linear in a0, so its sky dipole is < %.3f" % ("", eps))
NUM["T2_translation"] = rows
NUM["T2_power"] = power
check("C1 CONTROL: CFG182's committed headline is the door-11 record's 'A = 0.24 +- 0.20, A95 = 0.43'",
      abs(Ahat - 0.24) < 0.005 and abs(sigA - 0.20) < 0.005 and abs(A95 - 0.425) < 1e-9,
      "A-hat %.4f, sigma %.4f, A95 %.3f" % (Ahat, sigA, A95))
check("C2 CONTROL: the referee's A95 (CFG192) is 0.40 and its power at A = 0.5 is below 0.5 (a weak bound)",
      abs(A95_ref - 0.40) < 1e-9 and power["0.5"] < 0.5, "A95 %.3f; power(0.5) %.2f" % (A95_ref, power["0.5"]))
P("  CMB large-scale isotropy: NOT in the repo. From memory, unverified: after the kinematic dipole the temperature")
f186 = "campaign_fresh_gravity/CFG186_a0_vs_cmb_speed/FROZEN_QUESTION.md"
vsun = rx(r"v_sun = ([0-9.]+) km/s", T(f186), "v_sun")
P("  anisotropy is ~1e-5 at l = 2. Committed only: the kinematic dipole v_sun = %.1f km/s (%s, quoting Planck 2018)."
  % (vsun, cite(f186, "kinematic CMB dipole, a literature value quoted in a frozen question")))

# ------------------------------------------------------------------------------------------------------------
H("S2  T1 -- epochs where the record observes extra gravity, and the passage epoch reading (i) needs")
f121 = "fable_independent_2026/L121_a0_scaling_cmb_recheck.out"
t121 = T(f121)
zeq_b, zrec, zeq_m = rx(r"baryon-only (\d+) < z_rec (\d+) < with-a\S*-matter (\d+)", t121, "z_eq / z_rec", int)
P("  %s -> baryon-only z_eq = %d < z_rec = %d < z_eq with a clustering a^-3 component = %d; PEAK-2: an acceleration"
  % (cite(f121, "z_rec, z_eq and the density-not-acceleration statement (PEAK-1, PEAK-2)"), zeq_b, zrec, zeq_m))
P("    scale cannot supply the clustering density the third peak needs")
peak2_ok = "does NOT add a gravitating DENSITY" in t121
f129 = "fable_independent_2026/L129_smooth_dust_third_peak_boltzmann.out"
p32c, p32s = rx(r"peak3/peak2: clustering=([0-9.]+), smooth=([0-9.]+)", T(f129), "third/second peak")
P("  %s -> peak3/peak2 clustering %.4f vs smooth %.4f" % (cite(f129, "third-to-second peak ratio"), p32c, p32s))
fg = "campaign_fresh_gravity/closure_map/GATES.md"
och2, och2e = rx(r"Omega_c h\^2 = ([0-9.]+) ± ([0-9.]+)", T(fg), "Omega_c h^2")
P("  %s gate 3.01 -> Omega_c h^2 = %.4f +- %.4f" % (cite(fg, "gate 3.01, 4.01"), och2, och2e))
f4c = "campaign_fresh_gravity/CFG4_cosmology.out"
t4c = T(f4c)
h = rx(r"h = ([0-9.]+), omega_b", t4c, "h")
ob, ocdm = rx(r"omega_b ([0-9.]+), omega_cdm ([0-9.]+)", t4c, "omega_b, omega_cdm")
Om = rx(r"\(Omega_m ([0-9.]+)\)", t4c, "Omega_m")
fs8_chi, fs8_n = rx(r"f sigma_8 chi\^2 = ([0-9.]+) over (\d+) points", t4c, "f sigma_8 chi^2")
P("  %s -> h = %.6f, omega_b %.6f, omega_cdm %.5f, Omega_m %.4f; LCDM f sigma_8 chi^2 = %.2f over %d points"
  % (cite(f4c, "Planck 2018 best-fit inputs, Omega_m, f sigma_8 chi^2"), h, ob, ocdm, Om, fs8_chi, fs8_n))
check("C3 CONTROL: parsed z_rec = 1090, z_eq = 532 / 3423 (L121), peak ratios 0.9906 / 0.5545 (L129), PEAK-2 present",
      (zrec, zeq_b, zeq_m) == (1090, 532, 3423) and abs(p32c - 0.9906) < 1e-9 and abs(p32s - 0.5545) < 1e-9 and peak2_ok,
      "z_rec %d, z_eq %d / %d; %.4f / %.4f; PEAK-2 text %s" % (zrec, zeq_b, zeq_m, p32c, p32s, peak2_ok))
check("C4 CONTROL: Omega_m 0.3157 exceeds (omega_b + omega_cdm)/h^2 by less than 0.005 (massive neutrinos)",
      0 <= Om - (ob + ocdm) / h ** 2 < 0.005, "(omega_b + omega_cdm)/h^2 = %.4f vs Omega_m %.4f" % ((ob + ocdm) / h ** 2, Om))

# epochs from CFG197
f197 = "campaign_fresh_gravity/CFG197_gas_floor_highz/CFG197_phase2_results.json"
f197p = "campaign_fresh_gravity/CFG197_gas_floor_highz/CFG197_preflight_results.json"
f197r = "campaign_fresh_gravity/CFG197_gas_floor_highz/README.md"
r197 = J(f197)["numbers"]["results"]
t197 = T(f197r)
bins = {
    "E_4 (z > 3.5 pooled)": ("z>3.5 pooled (Danhaive + CRISTAL)|primary (paper M_dyn + CRISTAL 3.36)|sph/mlf|Newton|P2|canonical",
                             r"\*\*z > 3\.5 pooled\*\* \| 53 \| ([0-9.]+)"),
    "E_1.5 (KURVS)": ("comparison: KURVS (10)|primary (paper f_DM)|sph/mlf|Newton|P2|canonical",
                      r"KURVS \(r = R_eff\) \| 10 \| ([0-9.]+)"),
    "E_1.5 (MSA-3D)": ("comparison: MSA-3D (all 30)|primary (3.36)|sph/mlf|Newton|P2|canonical",
                       r"MSA-3D \(z 0\.6–1\.7\) \| 30 \| ([0-9.]+)"),
}
epochs = [{"name": "E_CMB (recombination, all-sky)", "z": float(zrec), "R_obs": None, "conditional": False}]
newton_all_consistent = True
for name, (key, pat) in bins.items():
    med = r197[key]["median"]
    zmed = rx(pat, t197, name)
    verdict = r197[key]["verdict"]
    newton_all_consistent &= (verdict == "CONSISTENT")
    epochs.append({"name": name, "z": zmed, "R_obs": 10 ** med, "log_R_obs": med, "conditional": True,
                   "newton_verdict": verdict})
    P("  %s [%s] -> median z %.2f; Newton median log M_dyn/M* = %.3f (R_obs = %.1f); Newton verdict %s; a baryons-only"
      % (cite(f197, "Newton median R_obs per bin"), name, zmed, med, 10 ** med, verdict))
    P("      reading needs M_gas/M* = R_obs - 1 = %.1f inside r_e (CFG197 cannot say whether the gas supplies it)" % (10 ** med - 1))
P("  (median redshifts from %s)" % cite(f197r, "median z per bin; 'gas or other unseen mass'; CRISTAL gas fractions ~50% (mu ~ 1)"))
floor_flat = J(f197p)["numbers"]["z>3.5 pooled (Danhaive + CRISTAL)|P2|canonical"]["median_floor_flat"]
P("  %s -> the flat law's gas-free floor at z > 3.5 is %.2f against the observed %.1f"
  % (cite(f197p, "flat-law floor"), floor_flat, epochs[1]["R_obs"]))
fgl = "campaign_fresh_gravity/CFG4_galaxy_law_results.json"
gl = J(fgl)["numbers"]["H2"]
rms = {k: gl[k]["rms"] for k in ("canonical|P2", "canonical|nu_mono", "alt|P2", "alt|nu_mono", "canonical|Newton")}
epochs.append({"name": "E_0 (SPARC RAR, z = 0)", "z": 0.0, "R_obs": None, "conditional": False})
P("  %s -> E_0: RAR rms law %.4f-%.4f dex vs Newton %.4f"
  % (cite(fgl, "SPARC RAR rms"), min(v for k, v in rms.items() if "Newton" not in k),
     max(v for k, v in rms.items() if "Newton" not in k), rms["canonical|Newton"]))
check("C5 CONTROL: CFG197's Newton medians reproduce its README (5.1 at z > 3.5, 4.0 KURVS, 11.4 MSA-3D; all CONSISTENT)",
      abs(epochs[1]["R_obs"] - 5.1) < 0.05 and abs(epochs[2]["R_obs"] - 4.0) < 0.05 and abs(epochs[3]["R_obs"] - 11.4) < 0.1
      and newton_all_consistent,
      "R_obs %.2f / %.2f / %.2f; Newton CONSISTENT in all three: %s"
      % (epochs[1]["R_obs"], epochs[2]["R_obs"], epochs[3]["R_obs"], newton_all_consistent))
NUM["T1_epochs"] = epochs

# comoving horizon and distance at the committed parameters
Or = Om / (1 + zeq_m)
OL = 1 - Om - Or
cH0 = 299792.458 / (100 * h)          # Mpc
tH0 = 977.7922216807891 / (100 * h)   # Gyr


def eta(a, n=4000):   # comoving particle horizon, Mpc; a = s^2 substitution
    return cH0 * simpson(lambda s: 2 * s / math.sqrt(Or + Om * s * s + OL * s ** 8), 0.0, math.sqrt(a), n)


def tcos(a, n=4000):  # cosmic time, Gyr
    return tH0 * simpson(lambda s: 2 * s ** 3 / math.sqrt(Or + Om * s * s + OL * s ** 8), 0.0, math.sqrt(a), n)


def chi(z):
    return eta(1.0) - eta(1.0 / (1 + z))


a_rec, a_eq = 1.0 / (1 + zrec), 1.0 / (1 + zeq_m)
eta0 = eta(1.0)
conv = abs(eta(1.0, 8000) - eta0) / eta0
eta_rec, eta_eq = eta(a_rec), eta(a_eq)
chi_rec, chi_eq = eta0 - eta_rec, eta0 - eta_eq
need_rec, need_eq = 2 * chi_rec / eta_rec, 2 * chi_eq / eta_eq
t_rec, t_eq, t_z1 = tcos(a_rec), tcos(a_eq), tcos(0.5)
P("")
P("  Flat FRW at the committed parameters: Omega_r = Omega_m/(1 + z_eq) = %.3e, Omega_L = %.4f, c/H0 = %.1f Mpc" % (Or, OL, cH0))
P("    comoving particle horizon eta(z_rec) = %.1f Mpc; comoving distance to last scattering chi(z_rec) = %.0f Mpc" % (eta_rec, chi_rec))
P("    eta(z_eq = %d) = %.1f Mpc; chi(z_eq) = %.0f Mpc; t(z_rec) = %.3f Myr; t(z_eq) = %.1f kyr; t(z = 1) = %.2f Gyr"
  % (zeq_m, eta_eq, chi_eq, t_rec * 1e3, t_eq * 1e6, t_z1))
P("    [sanity, from memory, unverified: chi(z_rec) ~ 13.9 Gpc, eta(z_rec) ~ 280 Mpc, t(z_rec) ~ 0.37 Myr]")
P("  A planar front starting at t = 0 must travel 2 chi comoving to cross the whole last-scattering sphere; comoving")
P("  distance covered = (v_f/c) eta. Hence:")
P("    luminal front: fraction of the sphere's diameter crossed by z_rec = %.4f (%.2f%%); by z_eq = %.4f" % (1 / need_rec, 100 / need_rec, 1 / need_eq))
P("    full coverage by z_rec needs v_f/c >= %.0f; by z_eq needs v_f/c >= %.0f" % (need_rec, need_eq))
P("    the horizon at z_rec subtends %.2f deg of radius on today's sky" % math.degrees(eta_rec / chi_rec))
check("C6 CONTROL: the horizon integral converges (N = 4000 vs 8000 differ by < 1e-6 relative)", conv < 1e-6, "rel. diff %.2e" % conv)
check("C7 (reported sanity) chi(z_rec) within 13-15 Gpc and eta(z_rec) within 250-320 Mpc (from-memory ranges)",
      13000 < chi_rec < 15000 and 250 < eta_rec < 320, "chi %.0f Mpc, eta %.1f Mpc" % (chi_rec, eta_rec), load_bearing=False)
NUM["T1_cosmology"] = {"Omega_r": Or, "Omega_L": OL, "cH0_Mpc": cH0, "eta_rec_Mpc": eta_rec, "chi_rec_Mpc": chi_rec,
                       "eta_eq_Mpc": eta_eq, "chi_eq_Mpc": chi_eq, "vf_over_c_needed_rec": need_rec,
                       "vf_over_c_needed_eq": need_eq, "luminal_fraction_rec": 1 / need_rec, "t_rec_Myr": t_rec * 1e3,
                       "t_eq_kyr": t_eq * 1e6, "t_z1_Gyr": t_z1}


def score_T1_i_own(z_pass, vf_over_c):
    """Reading (i-own): the front's compaction is the only extra gravity. z_pass None = starts at t = 0."""
    missed = [e["name"] for e in epochs if z_pass is not None and e["z"] > z_pass]
    if z_pass is None:
        covered = vf_over_c >= need_rec
        if not covered:
            return "FAIL", "coverage: a front at v_f/c = %.3g crosses %.2f%% of the last-scattering sphere by z_rec" % (
                vf_over_c, 100 * vf_over_c / need_rec), missed
        return ("MET ONLY AS T4", "covers the last-scattering sphere by z_rec (v_f/c = %.3g >= %.0f); by PEAK-2 the imprint"
                " must then BE a clustering a^-3 density -> REDUCES TO T4 (candidate B's cold component)" % (vf_over_c, need_rec), missed)
    if any(n.startswith("E_CMB") for n in missed):
        return "FAIL", "the passage (z = %g) follows recombination: no clustering density at z_rec (massless medium," \
                       " PEAK-2); also missed: %s" % (z_pass, "; ".join(n for n in missed if not n.startswith("E_CMB"))), missed
    return "MET ONLY AS T4", "passage before every observed epoch", missed


P("")
P("  T1 scoring for reading (i-own) (the compaction is the only extra gravity):")
t1_rows = {}
decl = [("luminal front from t = 0", None, 1.0), ("front from t = 0 at the minimum covering speed", None, need_rec)]
if MUTATE == "1":
    decl = [("luminal front from t = 0", None, 1.0), ("DECLARED FRONT at z_pass = 1 (MUTATE=1)", 1.0, 1.0)]
for label, zp, v in decl:
    lab, why, missed = score_T1_i_own(zp, v)
    t1_rows[label] = {"label": lab, "why": why, "missed_epochs": missed}
    P("    %-50s T1 %s -- %s" % (label, lab, why))
primary_label = decl[1][0]
primary_T1 = t1_rows[primary_label]["label"]
P("  T1 for (i+T4) (cold component kept): E_CMB met by T4, not by the front; E_4 and E_1.5 NON-DIAGNOSTIC for the")
P("    front's timing (Newton + unseen mass CONSISTENT in every CFG197 bin); z_pass is then a new constant (G4) unless it")
P("    precedes every bound system (initial data -> REDUCES TO candidate B).")
P("  T1 for (ii) and (iii): no bound systems exist at z_rec -> PASS WITH T4 KEPT; 11D adds nothing at E_CMB.")
NUM["T1_i_own"] = t1_rows
check("HEADLINE-T1: reading (i-own)'s declared primary front meets T1 at all (as T4); a late front must FAIL",
      primary_T1 == "MET ONLY AS T4", "%s: %s" % (primary_label, primary_T1))

# ------------------------------------------------------------------------------------------------------------
H("S3  T3 -- what stores the compaction after the passage")
xs = (0.1, 1.0, 3.0, 30.0)
tgt = {x: math.sqrt(1 + x * x) for x in xs}
P("  Target (CFG44 README, P2 point mass): M_dyn/M_b = sqrt(1 + x^2): " + ", ".join("x = %g: %.3f" % (x, tgt[x]) for x in xs))
P("  (M0) baryons made denser: mass is conserved, so by the shell theorem M_dyn/M_b = 1 beyond them; short by x %.2f at x = 30" % tgt[30.0])
f48g1 = "campaign_fresh_gravity/CFG48_gap1_switch/G1_gauss_noether_results.json"
g1why = J(f48g1)["verdicts"]["GE / flux-gated (action-derived)"]["why"]
P("       the record's field version: %s -> '%s'" % (cite(f48g1, "Gauss lemma verdict"), g1why))
f173 = "campaign_fresh_gravity/CFG173_door11B_directional_flow/cfg173_directional_flow_results.json"
c173 = J(f173)["checks"]
maxR = max(float(re.search(r"max R = g_ach/a_ph = ([0-9.e+-]+)", c["detail"]).group(1))
           for c in c173 if "max R = g_ach/a_ph" in c.get("detail", ""))
P("  (M2) the massless medium itself: its own gravity is at most %.2e of the phantom (%s) -> the stored object must be"
  % (maxR, cite(f173, "max g_ach/a_ph over V1'-V3")))
P("       something with mass-energy: the cold component T4 (REDUCES TO T4), or a field: the law's phantom (REDUCES TO B)")
check("C8 CONTROL: CFG173's committed maximum own-gravity ratio is 1.2e-6 (door-11 result table)", abs(maxR - 1.2e-6) < 0.05e-6,
      "max R %.3e" % maxR)
check("T3-M0: literal compaction of the baryons fails G1 (M_dyn/M_b = 1 against sqrt(1 + x^2) > 1.1 for x >= 0.5)",
      tgt[30.0] > 1.1 and tgt[1.0] > 1.1, "target %.3f at x = 1, %.2f at x = 30; compacted baryons give 1.000" % (tgt[1.0], tgt[30.0]))
NUM["T3"] = {"target_Mdyn_over_Mb": tgt, "cfg173_max_own_gravity_ratio": maxR}

# ------------------------------------------------------------------------------------------------------------
H("S4  Reading (iii): H1 hierarchy, H2 tidal dwarfs, G5 Solar System, DR4 Arm C")
f7r = "campaign_fresh_gravity/CFG7_README.md"
t7r = T(f7r)
emb = re.search(r"\*\*Formed embedded\*\* \(([^)]*)\)", t7r).group(1)
emb_ok = all(s in emb for s in ("tidal dwarfs", "wide binaries", "the Solar System"))
P("  %s -> FG001's formed-embedded class: (%s)" % (cite(f7r, "FG001 classes: top-level, accreted, formed embedded"), emb))
P("  (iii-a)'s assignment, class by class:")
h1 = [
    ("top-level (turned around from the Hubble flow on its own)", "owns (set at its turnaround)", "the law", True),
    ("accreted (satellites, cluster members, UDGs)", "owns: set at its own earlier turnaround, frozen, kept", "keeps its infall cold component", True),
    ("formed embedded (TDGs, GCs, DF2/DF4, wide binaries, Solar System)", "none: never decoupled from the Hubble flow on its own", "Newtonian", True),
    ("nested: a group turning around after its galaxies", "a second compaction at the group's turnaround, members keep theirs", "one phantom; members are lumps inside it (T5 max rule)", False),
]
for cls, iii, fg001_state, same in h1:
    P("    %-66s (iii-a): %-52s FG001: %s -> %s" % (cls, iii, fg001_state, "same" if same else "needs an extra postulate"))
f48g3 = "campaign_fresh_gravity/CFG48_gap1_switch/G3_history_action_causality_results.json"
g3 = J(f48g3)
latch_c = g3["numbers"]["results"]["LATCH"]["c"]
latch_v = g3["verdicts"]["GA / ownership latch ('has ever turned around')"]["status"]
label_v = g3["verdicts"]["GA / prescribed advected label (ownership as initial data)"]["status"]
P("  %s -> 'ownership latch (has ever turned around)' inside an action: %s (advanced dependence c = %.3f);"
  % (cite(f48g3, "latch and label verdicts"), latch_v, latch_c))
P("       'prescribed advected label': %s (causal, but the assignment rule is a postulate)" % label_v)
f63 = "campaign_fresh_gravity/CFG63_discrimination_forecast/forecast_results.json"
r63 = {r["pair"]: r for r in J(f63)["rows"]}
dB = r63["B vs LCDM/Newton [canonical, frozen sigma_fit]"]["delta"]
fd11 = "campaign_fresh_gravity/closure_map/DOOR11_RESULT_2026-09-29.md"
p2lo, p2hi = rx(r"canonical: \*\*([0-9.]+) / ([0-9.]+)\*\*", T(fd11), "P2 merge")
P("  %s -> DR4: B (ownership, Arm C) minus LCDM/Newton = %.3f in gamma-hat, i.e. Arm C = 1.000, the same as Newton/LCDM"
  % (cite(f63, "Arm C vs Newton"), dB))
P("  %s addendum 2 -> the P2 merged (unscreened) value 1.089 / 1.102 canonical" % cite(fd11, "P2 merge value"))
H1_label = "PARTIAL"
P("  H1 = %s: (iii-a) reproduces FG001's three classes and gives Arm C (1.000) with no separate wide-binary postulate," % H1_label)
P("       but needs T5's max rule for nested systems; it was written knowing FG001, so Arm C is not an independent prediction;")
P("       as a latch inside an action it is CFG48 G3's FAIL, as a label CFG48 G3's PARTIAL.")
check("C9 CONTROL: FG001's formed-embedded list contains tidal dwarfs, wide binaries and the Solar System; CFG48 G3 latch FAIL, label PARTIAL",
      emb_ok and latch_v == "FAIL" and label_v == "PARTIAL" and dB == 0.0,
      "list ok %s; latch %s (c %.4f); label %s; Arm C - Newton = %.3f" % (emb_ok, latch_v, latch_c, label_v, dB))

# H2 tidal dwarfs
f041 = "campaign_fresh_gravity/CFG7_tdg_fg041_results.json"
d041 = J(f041)["numbers"]
chiN = d041["H1"]["chi2_newton"]
pN = d041["H1"]["p"]
ratio, ratio_e = d041["H1"]["mean_ratio"], d041["H1"]["err_mean_ratio"]
cells = {k: (v["chi_efe"] - chiN, v["chi_iso"]) for k, v in d041["H2"].items()}
P("  %s -> six TDGs (Lelli et al. 2015): Newton chi^2 = %.2f (p = %.3f); <M_dyn/M_bar> = %.3f +- %.3f"
  % (cite(f041, "TDG chi^2: Newton, law + host field, isolated law"), chiN, pN, ratio, ratio_e))
for k, (dchi, chiso) in cells.items():
    P("    law in the TDG itself, %-16s: with the host's field (most favourable host mass) d chi^2 = %+.2f vs Newton; isolated chi^2 = %.1f" % (k, dchi, chiso))
iiia_H2 = chiN <= 12.6
iiib_H2 = not (all(dchi >= 4 for dchi, _ in cells.values()) or all(chiso > 12.6 for _, chiso in cells.values()))
P("  (iii-a): TDGs formed inside an owned host -> Newtonian -> H2 %s (line chi^2 <= 12.6)" % ("PASS" if iiia_H2 else "FAIL"))
P("  (iii-b): a pass at the TDG's own collapse -> the law applies -> H2 %s (line d chi^2 >= 4 on both footings, or isolated > 12.6)"
  % ("PASS" if iiib_H2 else "FAIL"))
P("  (A2) advected compaction: the debris of an owned disc carries it -> TDGs would not be Newtonian -> H2 FAIL (same numbers)")
check("C10 CONTROL: FG041's committed numbers reproduce CFG7's README (chi^2 1.09; d chi^2 +5.2 to +12.0; isolated 118-152)",
      abs(chiN - 1.09) < 0.01 and abs(min(c[0] for c in cells.values()) - 5.2) < 0.05
      and abs(max(c[0] for c in cells.values()) - 12.0) < 0.05 and 117 < min(c[1] for c in cells.values()) < 118.5
      and 151 < max(c[1] for c in cells.values()) < 152.5,
      "chi^2 %.3f; d chi^2 %.2f-%.2f; isolated %.1f-%.1f" % (chiN, min(c[0] for c in cells.values()),
                                                            max(c[0] for c in cells.values()),
                                                            min(c[1] for c in cells.values()), max(c[1] for c in cells.values())))

# G5
f185 = "campaign_fresh_gravity/CFG185_kernel_tail/cfg185_kernel_tail_results.json"
q2 = J(f185)["numbers"]["Q2"]
tails = [v for k, v in q2.items() if k.startswith("h_p2|")]
m401lo, m401hi = rx(r"margin ([0-9.]+e[0-9]+)-([0-9.]+e[0-9]+)", T(fg), "gate 4.01 margin")
P("  %s -> P2's anomalous monopole at Earth/Mars = %.0f-%.0fx the planetary bound (a Sun that owns a phantom)"
  % (cite(f185, "P2 tail over the planetary bound"), min(tails), max(tails)))
P("  %s gate 4.01 -> candidate B passes by ownership, margin %s-%s" % (cite(fg, "gate 4.01"), m401lo, m401hi))
iiia_G5, iiib_G5 = True, not (min(tails) > 1.0)
P("  (iii-a): the Sun formed inside the owned Milky Way -> no own compaction -> G5 PASS (inherits 4.01)")
P("  (iii-b): the Sun formed by collapse -> owns a phantom -> G5 %s" % ("PASS" if iiib_G5 else "FAIL"))
check("C11 CONTROL: CFG185's committed P2 tail is 1258-1545x (STANDING, GATES 4.01 note)",
      abs(min(tails) - 1258.1) < 0.5 and abs(max(tails) - 1545.4) < 0.5, "%.1f-%.1f" % (min(tails), max(tails)))
primary_iii = "(iii-b) any collapse" if MUTATE == "2" else "(iii-a) first decoupling"
pH2 = iiib_H2 if MUTATE == "2" else iiia_H2
pG5 = iiib_G5 if MUTATE == "2" else iiia_G5
P("  (iii-b) and DR4: wide binaries form by collapse inside the Milky Way -> they own a compaction -> Arm C (1.000) is lost;")
P("       the value the variant predicts (an owned, frozen, isolated law) is not in the record: UNDEFINED numerically, != 1.000")
check("HEADLINE-iii: reading (iii)'s primary [%s] passes H2 (tidal dwarfs) and G5 (Solar System)" % primary_iii,
      pH2 and pG5, "H2 %s, G5 %s" % ("PASS" if pH2 else "FAIL", "PASS" if pG5 else "FAIL"))
NUM["iii"] = {"H1": H1_label, "latch_c": latch_c, "TDG_chi2_newton": chiN, "TDG_cells": cells,
              "iiia": {"H2": iiia_H2, "G5": iiia_G5}, "iiib": {"H2": iiib_H2, "G5": iiib_G5},
              "P2_tail_over_bound": [min(tails), max(tails)], "armC_minus_newton": dB, "P2_merge": [p2lo, p2hi],
              "primary": primary_iii}

# ------------------------------------------------------------------------------------------------------------
H("S5  H3 -- does a pass frozen at turnaround give the amount C(r) = (a0/4pi) M_b(<r)?")
f70 = "campaign_fresh_gravity/CFG70_memory_kernel_exchange/cfg70_memory_kernel_exchange_results.json"
d70 = J(f70)["numbers"]
xe = 0.4
P("  %s -> B's committed r_ta (P2), r_e = 0.4 r_ta and r_e/r_M (key 'x_e' in that file):" % cite(f70, "r_ta, r_e, r_e/r_M; reaction; energy ratio"))
A1 = {}
for M in ("1e+09", "1e+10", "1e+12"):
    c = d70["E1"][M]["committed_P2"]
    re_rM = c["x_e"]
    rM_rta = xe / re_rM
    A1[M] = {"r_ta_kpc": c["r_ta"], "r_e_kpc": c["r_e"], "r_e_over_r_M": re_rM, "frozen_frac_at_r_e": xe ** 3,
             "frozen_frac_at_r_M": rM_rta ** 3, "energy_ratio_B_rta": c["ratio_num"]}
    P("    M_b = %s: r_ta %.0f kpc, r_e %.0f kpc, r_e/r_M %.1f -> frozen M_b,ta(<r)/M_b(<r) = %.3f at r_e, %.2e at r_M"
      % (M, c["r_ta"], c["r_e"], re_rM, xe ** 3, rM_rta ** 3))
sl_rta = math.log(A1["1e+12"]["r_ta_kpc"] / A1["1e+09"]["r_ta_kpc"]) / math.log(1e3)
sl_ratio = math.log(A1["1e+12"]["r_e_over_r_M"] / A1["1e+09"]["r_e_over_r_M"]) / math.log(1e3)
P("  (reported; added after the first full run, no gate changed) the turnaround scale in B's committed convention goes as")
P("       r_ta ~ M_b^%.3f, while the law's r_M = sqrt(G M_b/a0) ~ M_b^0.5: r_e/r_M ~ M_b^%.3f runs %.0f -> %.0f over 1e9 -> 1e12."
  % (sl_rta, sl_ratio, A1["1e+09"]["r_e_over_r_M"], A1["1e+12"]["r_e_over_r_M"]))
P("       An imprint set at turnaround carries the turnaround scale, not r_M, unless a0 is written into it (the restatement).")
NUM["H3_scales"] = {"slope_r_ta": sl_rta, "slope_r_e_over_r_M": sl_ratio}
P("  (A1) literal freeze (B's GR top-hat: at turnaround the baryons fill r_ta uniformly; today a point mass inside r_M):")
P("       short by x%.1f at r_e and by x%.1e-%.1e at r_M -> H3 FAIL (line: within 10%% at r <= r_e)"
  % (1 / xe ** 3, 1 / max(v["frozen_frac_at_r_M"] for v in A1.values()), 1 / min(v["frozen_frac_at_r_M"] for v in A1.values())))
mc30 = math.sqrt(1 + 30 ** 2) - 1
P("  (A2) advected with the baryons: zero beyond the baryons, against the target's M_c(<30 r_M) = %.2f M_b -> H3 FAIL" % mc30)
reac = d70["late_reaction_over_glaw"]["P"]
P("  (A3) label only: the amount is B's law -> REDUCES TO candidate B (a restatement). Maintained dynamically, it costs CFG70's")
P("       reaction %.3f-%.1f g_law (x = 0.3-30; line 0.10) and %.0f / %.0f / %.0f x the orbital energy (M_b = 1e9 / 1e10 / 1e12, B's r_ta)"
  % (reac["0.3"], reac["30"], A1["1e+09"]["energy_ratio_B_rta"], A1["1e+10"]["energy_ratio_B_rta"], A1["1e+12"]["energy_ratio_B_rta"]))
check("C12 CONTROL: CFG70's committed energy ratios (B's r_ta, P2) are 318 / 179 / 57 and the reaction 0.065-22.5 g_law",
      abs(A1["1e+09"]["energy_ratio_B_rta"] - 318.2) < 0.5 and abs(A1["1e+10"]["energy_ratio_B_rta"] - 178.9) < 0.5
      and abs(A1["1e+12"]["energy_ratio_B_rta"] - 56.6) < 0.5 and abs(reac["0.3"] - 0.065) < 0.001 and abs(reac["30"] - 22.5) < 0.05,
      "%.1f / %.1f / %.1f; %.4f-%.2f" % (A1["1e+09"]["energy_ratio_B_rta"], A1["1e+10"]["energy_ratio_B_rta"],
                                         A1["1e+12"]["energy_ratio_B_rta"], reac["0.3"], reac["30"]))
NUM["H3"] = {"A1": A1, "A2_target_Mc_over_Mb_x30": mc30, "A3_reaction": reac}

# ------------------------------------------------------------------------------------------------------------
H("S6  H4 -- the ultra-faint tension and 'formation-epoch compaction'")
f28 = "campaign_fresh_gravity/CFG28_ufd_referee_results.json"
d28 = J(f28)["numbers"]
off_c, eoff_c = d28["RES"]["canonical"]["km"]
off_a, eoff_a = d28["RES"]["alt"]["km"]
z_c, z_a = d28["RES"]["canonical"]["z_km"], d28["RES"]["alt"]["z_km"]
fdisp_c, fdisp_a = d28["T3"]["canonical"]["factor"]["par"], d28["T3"]["alt"]["factor"]["par"]
ffg = "campaign_fresh_gravity/CFG7_hierarchy_fg001_results.json"
cls = J(ffg)["numbers"]["GATES"]["G4 MW classical dSphs"]
P("  %s -> offset +%.3f / +%.3f dex (canonical / alt), %.1f / %.1f sigma with the 0.077-dex floor; dispersion factor %.2f / %.2f"
  % (cite(f28, "UFD offset, significance, dispersion factor"), off_c, off_a, z_c, z_a, fdisp_c, fdisp_a))
P("  %s -> MW classical dSphs under FG001: %.2f / %.2f sigma (pass)" % (cite(ffg, "classical dSph gate"), cls["canonical"]["fg001"], cls["alt"]["fg001"]))
P("  (iii-a) with the flat tie: UFDs are accreted; B already applies the isolated law of their infall baryons, and a0 is the")
P("       same at every epoch -> freezing at turnaround changes nothing -> the tension stands.")
fac_c, fac_a = 10 ** (4 * off_c), 10 ** (4 * off_a)


def z_of_E(E):
    lo, hi = 0.0, 1e4
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if math.sqrt(Or * (1 + mid) ** 4 + Om * (1 + mid) ** 3 + OL) < E:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


zc_r, za_r = z_of_E(fac_c), z_of_E(fac_a)
P("  REPORTED ONLY, POST HOC, NOT SCORED: deep limit sigma ~ a0^(1/4) (CFG44: sigma_inf^2 = 1/2 sqrt(G a0 M_b)), so an imprint")
P("       carrying the whole offset would need a0 x%.1f / x%.1f at the UFDs' imprint. Under the RIVAL a0 ~ H(z) (not the framework's" % (fac_c, fac_a))
P("       flat tie) that is E(z) = %.1f / %.1f, i.e. z = %.1f / %.1f. The flat law excludes this by construction; it was never frozen;" % (fac_c, fac_a, zc_r, za_r))
P("       the classical dSphs, which pass under the flat law, would have to escape it; no formation epochs are committed.")
P("  H4 = NON-DIAGNOSTIC.")
check("C13 CONTROL: CFG28's committed UFD offset is +0.325 / +0.304 dex at 3.8 / 3.5 sigma",
      abs(off_c - 0.3245) < 0.001 and abs(off_a - 0.3045) < 0.001 and abs(z_c - 3.77) < 0.01 and abs(z_a - 3.55) < 0.01,
      "+%.4f / +%.4f; %.2f / %.2f sigma" % (off_c, off_a, z_c, z_a))
NUM["H4"] = {"offset_dex": [off_c, off_a], "sigma": [z_c, z_a], "a0_factor_needed_post_hoc": [fac_c, fac_a],
             "z_under_rival_post_hoc": [zc_r, za_r], "classical_dsph_sigma": [cls["canonical"]["fg001"], cls["alt"]["fg001"]]}

# ------------------------------------------------------------------------------------------------------------
H("S7  T5 -- clustering and flows ('the dark energy sweeps galaxies together')")
P("  (a) A uniform one-direction front v = v_f n-hat has div v = 0 identically: it displaces everything together and makes no")
P("      overdensity grow. Sweeping galaxies together needs div v < 0 on overdensities, i.e. a sink (door 11A).")
f171 = "campaign_fresh_gravity/CFG171_door11A_inflow/cfg171_s3_gates_results.json"
g171 = J(f171)["numbers"]["G3_literal_medium"]
e171 = [v[k] for v in g171.values() for k in ("E_over_Eb_A", "E_over_Eb_B") if k in v]
P("      %s -> 11A's literal medium carries %.1f-%.0f x the baryons' orbital energy" % (cite(f171, "11A literal-medium energy"), min(e171), max(e171)))
f176 = "campaign_fresh_gravity/CFG176_dark_energy_flow/CFG176_de_flow_results.json"
c176 = J(f176)["checks"]
cap_s = next(c["measured"] for c in c176 if "largest carried fraction" in str(c.get("measured", "")))
cap, Rc, Ra = rx(r"largest carried fraction ([0-9.]+) vs R ([0-9.]+) / ([0-9.]+)", cap_s, "CFG176 cap")
P("  (b) %s -> a NEC-respecting flowing dark energy carries <= %.4f of the vacuum column vs %.3f / %.3f needed"
  % (cite(f176, "NEC-limited carried column"), cap, Rc, Ra))
P("  (c) %s -> LCDM's density-sourced growth fits f sigma_8 with chi^2 %.2f / %d; gate 3.03 allows d chi^2 <= 4 for anything added"
  % (cite(f4c, "f sigma_8 chi^2"), fs8_chi, fs8_n))


def growth(Om_, n=20000, a0=1e-3):
    """Linear growth in flat LCDM (no radiation), D'' + (2 + dlnH/dlna) D' - 1.5 Om(a) D = 0 in ln a, D = a initially."""
    OL_ = 1 - Om_

    def rhs(lna, y):
        a = math.exp(lna)
        E2 = Om_ * a ** -3 + OL_
        Oma = Om_ * a ** -3 / E2
        return (y[1], -(2 - 1.5 * Oma) * y[1] + 1.5 * Oma * y[0])
    x0, x1 = math.log(a0), 0.0
    hstep = (x1 - x0) / n
    y = (a0, a0)
    x = x0
    for _ in range(n):
        k1 = rhs(x, y)
        k2 = rhs(x + hstep / 2, (y[0] + hstep / 2 * k1[0], y[1] + hstep / 2 * k1[1]))
        k3 = rhs(x + hstep / 2, (y[0] + hstep / 2 * k2[0], y[1] + hstep / 2 * k2[1]))
        k4 = rhs(x + hstep, (y[0] + hstep * k3[0], y[1] + hstep * k3[1]))
        y = (y[0] + hstep / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]), y[1] + hstep / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]))
        x += hstep
    return y[0], y[1] / y[0]


g0, f0 = growth(Om)
gE, fE = growth(1.0)
f055 = Om ** 0.55
P("  (d) growth at the committed Omega_m = %.4f: D(z=0)/a = %.3f relative to Einstein-de Sitter (Lambda SUPPRESSES late growth by %.0f%%);"
  % (Om, g0, 100 * (1 - g0)))
P("      f(z=0) = dlnD/dlna = %.3f vs Omega_m^0.55 = %.3f (exponent from memory, unverified); CFG176: a w = -1 or compacted"
  % (f0, f055))
P("      DE-like medium has rho + 3p < 0 and repels. In standard cosmology dark energy opposes clustering; it does not drive it.")
check("C14 CONTROL: the growth solver returns Einstein-de Sitter exactly at Omega_m = 1 (D = a, f = 1)",
      abs(gE - 1) < 1e-6 and abs(fE - 1) < 1e-6, "D/a %.8f, f %.8f" % (gE, fE))
check("C15 CONTROL: CFG171 / CFG176 committed numbers reproduce the door-11 record (16-205x; 0.078 vs 0.293)",
      15.5 < min(e171) < 16.5 and 204 < max(e171) < 206 and abs(cap - 0.0781) < 1e-4 and abs(Rc - 0.293) < 1e-3,
      "%.1f-%.1f; %.4f vs %.3f" % (min(e171), max(e171), cap, Rc))
P("  T5 scoring: (i) -- (a) a sweep needs a sink -> REDUCES TO 11A (G3 FAIL, %.0f-%.0fx); (b) cap %.3f vs %.3f; (c) UNDEFINED (no"
  % (min(e171), max(e171), cap, Rc))
P("      velocity model; phase 2 must price it against gate 3.03). (iii) -- NOT IMPLEMENTED (no sweeping; clustering is B's).")
NUM["T5"] = {"E_over_Eorb_11A": [min(e171), max(e171)], "NEC_cap": cap, "R_needed": [Rc, Ra], "fs8_chi2": fs8_chi,
             "fs8_n": fs8_n, "D0_over_a": g0, "f0": f0, "Om055": f055}

# ------------------------------------------------------------------------------------------------------------
H("S8  Hand estimates declared in the frozen file (section 8), against the numbers (wrong ones kept)")
est = [
    ("1 luminal coverage ~1% of the diameter by z_rec; ~100c needed; ~250c by z_eq",
     0.005 < 1 / need_rec < 0.02 and 70 < need_rec < 140 and 180 < need_eq < 350,
     "%.2f%%; %.0fc; %.0fc" % (100 / need_rec, need_rec, need_eq)),
    ("3 A1: 0.064 at r_e and <= 1e-6 at r_M", abs(xe ** 3 - 0.064) < 1e-9 and max(v["frozen_frac_at_r_M"] for v in A1.values()) <= 1e-6,
     "%.3f; %.2e" % (xe ** 3, max(v["frozen_frac_at_r_M"] for v in A1.values()))),
    ("4 growth D(0)/a ~ 0.78, f(0) ~ 0.53, |f - Om^0.55| < 0.01", abs(g0 - 0.78) < 0.02 and abs(f0 - 0.53) < 0.02 and abs(f0 - f055) < 0.01,
     "%.3f, %.3f, %.4f" % (g0, f0, abs(f0 - f055))),
    ("5 TDG (iii-a) PASS, (iii-b) FAIL; Cassini (iii-b) FAIL by > 1000x", iiia_H2 and not iiib_H2 and min(tails) > 1000,
     "%s / %s; %.0fx" % (iiia_H2, iiib_H2, min(tails))),
    ("6 UFD a0 factor ~20 (canonical)", 15 < fac_c < 25, "%.1f" % fac_c),
    ("7 a0 upwind/downwind < 2.5; deep-force dipole < 0.21", rows[0]["a0_up_over_down"] < 2.5 and rows[0]["deep_force_dipole_linear"] < 0.21,
     "%.2f; %.4f" % (rows[0]["a0_up_over_down"], rows[0]["deep_force_dipole_linear"])),
]
for name, ok, det in est:
    check("E%s" % name, ok, det, load_bearing=False)

# ------------------------------------------------------------------------------------------------------------
H("S9  Verdict matrix (labels frozen in CFG251_FROZEN_CRITERIA.md section 7; never pooled)")
iii_H2 = "PASS" if pH2 else "FAIL"
iii_G5 = "PASS" if pG5 else "FAIL"
matrix = [
    ("(i-own) cosmic front, compaction the only extra gravity",
     {"T1": ("FAIL (late passage)" if primary_T1 == "FAIL" else
             "met only by v_f >= %.0fc or initial data, then REDUCES TO T4; luminal FAIL (%.1f%% coverage)" % (need_rec, 100 / need_rec)),
      "T2": "luminal: partial coverage of the last-scattering sphere -> FAIL; otherwise PASS (weak bound, eps < %.3f)" % A95,
      "T3": "REDUCES TO T4 (a clustering density) -- M0 compacted baryons FAIL G1",
      "passage": "REDUCES TO 11B' (a transient massless flux: own gravity <= %.1e, a push is Le Sage)" % maxR,
      "T5": "(a) REDUCES TO 11A (G3 FAIL); (b) cap %.3f vs %.3f; (c) UNDEFINED" % (cap, Rc),
      "G4/G5": "z_pass, v_f counted; v_f > c FAILS causality unless a preferred slice (-> 11C) or initial data (-> T4)"}),
    ("(i+T4) cosmic front, cold component kept",
     {"T1": "E_CMB by T4; E_4, E_1.5 NON-DIAGNOSTIC (Newton + unseen mass CONSISTENT); z_pass a new constant (G4 FAIL) unless initial data",
      "T3": "REDUCES TO candidate B's law (M1) -- needs ownership",
      "verdict": "REDUCES TO candidate B, plus one constant if the passage is late"}),
    ("(ii) per-system passage at formation",
     {"T1": "PASS WITH T4 KEPT", "T4": "(ii-flat) null, identical to B; (ii-epoch) a new function (G4), NON-DIAGNOSTIC",
      "identity": "formation = turnaround -> (iii-a); formation = any collapse -> (iii-b)"}),
    ("(iii) set once at first decoupling from the Hubble flow, frozen [primary: %s]" % primary_iii,
     {"H1": "%s (reproduces FG001's classes and Arm C, needs T5's max rule; a latch = CFG48 G3 FAIL, a label = PARTIAL)" % H1_label,
      "H2": iii_H2 + " (TDGs: Newton chi^2 %.2f; law d chi^2 +%.1f to +%.1f)" % (chiN, min(c[0] for c in cells.values()), max(c[0] for c in cells.values())),
      "G5": iii_G5 + (" (the Sun owns: %.0f-%.0fx)" % (min(tails), max(tails)) if not pG5 else " (inherits gate 4.01 via ownership)"),
      "H3": "A1 FAIL (x%.1f short at r_e); A2 FAIL; A3 REDUCES TO B (restatement)" % (1 / xe ** 3),
      "H4": "NON-DIAGNOSTIC (flat tie: no change; the UFD tension stands)",
      "T1": "PASS WITH T4 KEPT", "T2": "isotropic imprint: trivially PASS (direction dropped); directional: NON-DIAGNOSTIC",
      "T3": "a label (CFG48 G3) plus B's law", "T4": "null under the flat tie", "T5": "NOT IMPLEMENTED"}),
]
for name, gates in matrix:
    P("  %s" % name)
    for g, v in gates.items():
        P("      %-9s %s" % (g, v))
NUM["matrix"] = {n: g for n, g in matrix}

# ------------------------------------------------------------------------------------------------------------
H("VERDICT")
P("  (i)   a single cosmic front meets the CMB epoch only if it is initial data or superluminal (>= %.0fc), and then only if it"
  % need_rec)
P("        leaves a clustering density: it REDUCES TO candidate B's cold component. A luminal front covers %.1f%% of the" % (100 / need_rec))
P("        last-scattering sphere by recombination (T1 and T2 FAIL). The act of compacting is 11B''s class (no-go).")
P("        Declared primary front: T1 %s." % primary_T1)
P("  (ii)  identical to (iii-a) or (iii-b) depending on what 'formation' means; its own content (epoch dependence) is NON-DIAGNOSTIC.")
P("  (iii) primary %s: H2 %s, G5 %s; H1 PARTIAL (bookkeeping, not a mechanism); H3 FAILS or restates B; H4 NON-DIAGNOSTIC." % (primary_iii, iii_H2, iii_G5))
P("        (iii-b) 'a pass at any collapse' fails the tidal dwarfs and Cassini and loses Arm C.")
P("  Nothing here supplies B's missing mechanism. At most (iii-a) names the ownership label's assignment rule (first decoupling")
P("  from the Hubble flow), which CFG48 G3 already scored. kappa = 1/2 FITTED; the mass is still required; nothing is closed.")

lb_fail = [c["name"] for c in CHECKS if c["load_bearing"] and not c["ok"]]
rep_fail = [c["name"] for c in CHECKS if not c["load_bearing"] and not c["ok"]]
P("")
P("  %d checks: %d pass; load-bearing failures %d%s; reported failures %d%s"
  % (len(CHECKS), sum(c["ok"] for c in CHECKS), len(lb_fail), (" " + str(lb_fail)) if lb_fail else "",
     len(rep_fail), (" " + str(rep_fail)) if rep_fail else ""))

with open(OUT, "w") as fh:
    fh.write("\n".join(LINES) + "\n")
with open(RES, "w") as fh:
    json.dump({"slug": "CFG251_handcheck", "mutate": MUTATE, "summary": {"n_checks": len(CHECKS),
               "load_bearing_failures": len(lb_fail), "failed": lb_fail + rep_fail},
               "checks": CHECKS, "numbers": NUM, "sources": SOURCES}, fh, indent=1, default=str)
print("\n".join(LINES))
sys.exit(1 if lb_fail else 0)
