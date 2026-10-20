#!/usr/bin/env python3
"""CFG895 check -- (A) tally of the alpha attempts ledger; (B) by-construction pre-flight numbers quoted in
ALPHA_CAMPAIGN_RULES.md and ALPHA_DOORS.md.  Light arithmetic only (no fits, no searches, no downloads).

Run:     nice -n 10 python3 cfg895_check.py          -> exit 0 if every check passes; writes cfg895_check.json
MUTATE:  nice -n 10 python3 cfg895_check.py MUTATE   -> uses (1 + 8 lambda) instead of (1 - 8 lambda) in AS3's f_g formula;
         check K2 (and the checks built on it) must FAIL and the script exits 1 (exit 3 if the control is broken).

alpha(0) enters ONLY as a diagnostic (to size e^2 in the FSP leverage and the SM running offset); nothing here produces alpha,
and nothing here is a derivation.  Every input is quoted with the committed record file it comes from.
"""
import json
import math
import re
import sys
from pathlib import Path

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
HERE = Path(__file__).resolve().parent
CHECKS = []


def chk(tag, ok, info=""):
    CHECKS.append((tag, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {tag} {info}")


# ---------------------------------------------------------------------------------------------- (A) ledger tally
FAMILIES = ["FP", "GEO", "QED", "GRAV", "WGC", "HOR", "STR", "EMG", "DIL", "QCD", "SEL", "NUM", "EXT", "META"]
ledger = (HERE / "ALPHA_ATTEMPTS_LEDGER.md").read_text()
rows = []
for line in ledger.splitlines():
    if not line.startswith("| "):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 8 or cells[1] not in FAMILIES:
        continue
    trials = cells[6]
    kind = "rule" if trials.endswith("R") else "mech"
    n = int(trials[:-1]) if trials.endswith("R") else (int(trials) if trials.isdigit() else 0)
    rows.append({"id": cells[0], "family": cells[1], "verdict": cells[5], "trials": n, "kind": kind,
                 "value": cells[4], "commit": cells[7]})
per_family = {f: sum(1 for r in rows if r["family"] == f) for f in FAMILIES}
n_mech = sum(r["trials"] for r in rows if r["kind"] == "mech" and r["family"] not in ("EXT", "META"))
n_rule = sum(r["trials"] for r in rows if r["kind"] == "rule")
n_ext = sum(r["trials"] for r in rows if r["family"] == "EXT")
ids = [r["id"] for r in rows]
print("== (A) ledger ==")
print(f"   rows {len(rows)}; per family {per_family}")
print(f"   graded mechanism-level value trials (record, lower bound) N_mech = {n_mech}; rule-search trials N_rule = {n_rule}; "
      f"external claims audited = {n_ext}")
chk("A1 ledger parses, every row has a known family code", len(rows) >= 60, f"({len(rows)} rows)")
chk("A2 ledger ids are unique", len(ids) == len(set(ids)), "" if len(ids) == len(set(ids)) else
    str(sorted({i for i in ids if ids.count(i) > 1})))
chk("A3 no ledger row claims a derivation", not any(re.search(r"\bDERIVED\b|\bDERIVATION\b", r["verdict"]) and
                                                    not re.search(r"NOT|no |never", r["verdict"], re.I) for r in rows))

# ---------------------------------------------------------------------------------------------- (B) pre-flight
print("== (B1) asymptotic-safety map (one loop, by construction) ==")
# AS3_fg_cpr_reanchored/AS3_REPORT.md and ALPHA_CHAIN_STATUS.md section 'Asymptotic-safety f_g lanes AS1-AS4':
#   CPR gauge, at a fixed point: f_g = 5 g (1 - 8 lambda) / (36 pi (1 - 2 lambda)^2); EH + SM root (g, lambda) = (0.967159, -1.22293),
#   f_g = 0.03883, P_EH = 95.578; AS4 EH + SM reference f_g = 0.03675, P_EH = 96.373; required f_g = 0.009805 (lane B, 4.89x smaller than 0.04795).
# Lane B: g_Y* = 4 pi sqrt(6 f_g/41)  =>  1/alpha_Y*(M_P) = 41 / (24 pi f_g).
# Y1_running_precision (ALPHA_CHAIN_STATUS.md Y1 bullet): 1/alpha_2(M_P) = 49.203, 1/alpha_em(M_P) = 104.437, 1/alpha_Y(M_P) = 55.234.
SGN = +1 if MUT else -1
def f_g(g, lam):
    return 5 * g * (1 + SGN * 8 * lam) / (36 * math.pi * (1 - 2 * lam) ** 2)

INV_A0_DIAG = 137.035999177          # CODATA 2022, diagnostic only (V1_exactness_harness)
INV_A2_MP, INV_AEM_MP, INV_AY_MP = 49.203, 104.437, 55.234
OFFSET = INV_A0_DIAG - INV_AEM_MP     # SM running M_P -> Thomson limit (diagnostic; the record's '~32.6 units')
def inv_alpha0(fg):
    return 41 / (24 * math.pi * fg) + INV_A2_MP + OFFSET

g3, l3 = 0.967159, -1.22293
fg3 = f_g(g3, l3)
chk("K2 AS3 f_g reproduced from its root (0.03883)", abs(fg3 / 0.03883 - 1) < 3e-3, f"(f_g = {fg3:.5f})")
p3, p4 = inv_alpha0(fg3), inv_alpha0(0.03675)
chk("K3 one-loop map reproduces P_EH (AS3 95.578, AS4 96.373) within 0.5%",
    abs(p3 / 95.578 - 1) < 5e-3 and abs(p4 / 96.373 - 1) < 5e-3, f"({p3:.3f}, {p4:.3f})")
fg_req = 41 / (24 * math.pi * (INV_A0_DIAG - OFFSET - INV_A2_MP))
chk("K4 required f_g reproduced (record 0.009805) within 1%", abs(fg_req / 0.009805 - 1) < 1e-2, f"({fg_req:.6f})")
chk("K4b the alpha_em(M_P) split is consistent (1/a_Y + 1/a_2 = 1/a_em within 0.01)",
    abs(INV_AY_MP + INV_A2_MP - INV_AEM_MP) < 1e-2, f"({INV_AY_MP + INV_A2_MP:.3f})")
# lambda that would give the required f_g at AS3's g (diagnostic only: g also moves when the matter content moves)
c = 0.009805 * 36 * math.pi / (5 * g3)            # (1 - 8 x) = c (1 - 2 x)^2  ->  4c x^2 + (8 - 4c) x + (c - 1) = 0
A_, B_, C_ = 4 * c, 8 - 4 * c, c - 1
disc = B_ * B_ - 4 * A_ * C_
roots = sorted([(-B_ + math.sqrt(disc)) / (2 * A_), (-B_ - math.sqrt(disc)) / (2 * A_)])
res = max(abs(f_g(g3, x) - 0.009805) for x in roots)
chk("K5 lambda roots for f_g = 0.009805 at g = 0.967159 satisfy the formula", res < 1e-10,
    f"(lambda = {roots[0]:.3f}, {roots[1]:.4f}; AS3 has {l3})")
slope_req = -41 / (24 * math.pi * fg_req)
spread = [inv_alpha0(x) for x in (0.037, 0.048)]
print(f"   d(1/alpha(0))/d ln f_g = {slope_req:.1f} at the required f_g; computed f_g 0.037-0.048 -> 1/alpha(0) "
      f"{spread[1]:.1f}-{spread[0]:.1f} (one loop; record 91-96)")
print(f"   to fix 1/alpha(0) to 1% the route needs f_g to {1.37036 / abs(slope_req) * 100:.1f}%; to 5e-10 it needs "
      f"{137.036 * 5e-10 / abs(slope_req):.1e} in ln f_g")

print("== (B2) leverage of the FSP QCD-vacuum selection equation (order of magnitude) ==")
# fine_structure_puzzle/checkpoints/FSP-011.md: partial sum Born^(0) + (1/2) M_u^(p-n) = 5.03-5.89 MeV per e^2 ('It is not M_u^p';
# N0 is missing).  Used here ONLY to size the first-order EM fraction of the proton mass.  M_p = 938.272 MeV (PDG, recalled).
# fine_structure_puzzle/atomic_bridge/qcd_mass/CONSTRAINED_SENSITIVITY.md: R = c_H / C_p^3 = Hbar_dS / (K G m_p^3), K = 8 pi/3,
#   S = dlnR/dln alpha |_(m_q, m_p) = h_alpha - (3 - Q) p_alpha / (1 - P).
# FSP-002 writes the bridge with a_M and kappa; with the framework's a_M = kappa c sqrt(G rho_DE) kappa cancels (identity check below).
E2_DIAG = 4 * math.pi / INV_A0_DIAG
MP = 938.272
S_p = [E2_DIAG * m / MP for m in (5.03, 5.89)]
S_MAX = 10 * S_p[1]                  # generous: |h_alpha| and the (3 - Q)/(1 - P) factor each allowed up to O(several)
chk("K6 first-order EM fraction of m_p is O(5e-4)", 3e-4 < S_p[0] < S_p[1] < 8e-4, f"(p_alpha {S_p[0]:.2e}-{S_p[1]:.2e})")
# kappa cancellation (identity by construction): a_M hbar^2/(G c^2 m_p^3) / (kappa sqrt(8 pi/3)) with a_M = kappa c sqrt(G rho)
kap_a, kap_b = 0.5, 0.417
lhs = [(k * 1.0) / (k * math.sqrt(8 * math.pi / 3)) for k in (kap_a, kap_b)]
chk("K7 kappa cancels from the FSP-002 bridge once a_M = kappa c sqrt(G rho_DE) (R independent of kappa)",
    abs(lhs[0] - lhs[1]) < 1e-15)
sig_lnR_bracket = math.log(73.04 / 68.56)   # H0: SH0ES vs DESI-BAO+BBN (CFG886 commit message) -> H_Lambda = H0 sqrt(Omega_L)
sig_lnR_opt = 0.01                           # optimistic: H0 settled AND c_H, C_p computed to 1%
sl_b, sl_o = sig_lnR_bracket / S_MAX, sig_lnR_opt / S_MAX
chk("K8 FSP selection equation is NON-DIAGNOSTIC for alpha even with |S| = 10 p_alpha (sigma ln alpha > 1)",
    sl_b > 1 and sl_o > 1, f"(sigma ln alpha >= {sl_b:.1f} with the H0 bracket, {sl_o:.2f} at 1%)")
need_1pc, need_bar = 1e-2 * S_MAX, 5e-10 * S_MAX
print(f"   to infer alpha to 1% the cosmological side and c_H/C_p^3 must be known to {need_1pc:.1e}; to 5e-10, to {need_bar:.1e}")

print("== (B3) precision a hit must reach (P < 1e-3) ==")
RHO_D = 0.0250                    # lane D: distinct formula values per unit relative deviation near 137 (D_calibration_bar)
DENS_MECH = 1 / math.log(100)     # mechanism outputs: log-uniform 1/alpha in [10, 1000] (declared here; narrower -> stricter)
table = []
for K in (1, 10, 100, 1e3, 1e6, 3.6e7):
    dD = 1e-3 / (2 * RHO_D * K)
    dM = 1e-3 / (2 * DENS_MECH * K)
    dMc = dM / max(n_mech, 1)
    table.append({"K": K, "delta_formula": dD, "delta_mechanism": dM, "delta_mechanism_campaign": dMc})
    print(f"   option space K = {K:>10.3g}: formula bar delta <= {dD:.2e}; mechanism delta <= {dM:.2e}; "
          f"campaign-wide (x N_mech = {n_mech}) delta <= {dMc:.2e}")
Y1_AEM = 8.8e-4                   # Y1: sigma(1/alpha_em)/137.036 from the running (direct M_W)
p_uv = 2 * Y1_AEM * DENS_MECH
p_joint = (2 * 2.3e-3 * DENS_MECH) * (2 * 2.1e-4 * DENS_MECH)   # alpha_Y and alpha_2 at M_P (Y1 0.23%, 0.021%)
chk("K9 a single-coupling UV route cannot reach campaign-wide P < 1e-3 at Y1's running error",
    p_uv * n_mech > 1e-3, f"(P_single >= {p_uv:.1e}; x N_mech = {p_uv * n_mech:.2f})")
print(f"   a joint two-coupling hit at Y1 precision: P_single ~ {p_joint:.1e} (x N_mech = {p_joint * n_mech:.1e})")

print("== (B4) by-construction arithmetic used in ALPHA_DOORS.md (pre-statements and pre-kills) ==")
# (a) spectral dimension d_s -> 2 in the UV: beta_g = ((d_s - 4)/2) g + b g^3/(16 pi^2) has the AS form with f = (4 - d_s)/2
f_ds2 = (4 - 2) / 2
print(f"   spectral-dimension fixed point: f = {f_ds2:.1f} vs required {0.009805}: ratio {f_ds2 / 0.009805:.0f}")
# (b) unimodular door pre-statement: if AS3's TT-only f_g carries over with lambda absent, f_g = 5 g*/(36 pi)
g_uni = 0.009805 * 36 * math.pi / 5
print(f"   unimodular pre-statement: f_g = 5 g*/(36 pi) = 0.009805 needs g* = {g_uni:.4f} (AS3 EH+SM has g* = {g3})")
# (c) NCG spectral action (RECALLED, to be verified by the door): g^2 f_0/(2 pi^2) = 1/4 -> 1/alpha_unif = 8 f_0/pi
inv_ncg = {"entropy h(0)=ln2": 8 * math.log(2) / math.pi, "characteristic f(0)=1": 8 / math.pi}
inv_a2_cross = INV_A2_MP - (19 / 6) / (2 * math.pi) * math.log(1.22089e19 / 2.8e16)   # one loop from Y1's M_P value to g2=g3
print(f"   NCG: 1/alpha_unif = {inv_ncg} vs 1/alpha_2 ~ {inv_a2_cross:.1f} at the g2 = g3 crossing (one loop from Y1): "
      f"miss x{inv_a2_cross / inv_ncg['entropy h(0)=ln2']:.0f} / x{inv_a2_cross / inv_ncg['characteristic f(0)=1']:.0f}")
# (d) Festina Lente m^2 >= sqrt(6) e q M_P H for the electron (Planck units; H0 = 70 km/s/Mpc; e from alpha_diag)
me = 0.51099895 / 1.22089e22
H0 = 70 / 3.0857e19 * 5.391247e-44
fl_ratio = me ** 2 / (math.sqrt(6) * math.sqrt(4 * math.pi / INV_A0_DIAG) * H0)
print(f"   Festina Lente for the electron: m_e^2 / (sqrt6 e M_P H) = {fl_ratio:.1e} (satisfied by ~{math.log10(fl_ratio):.0f} orders)")
chk("K10 pre-kill arithmetic is as quoted (f ratio ~102, g* 0.222, NCG miss > 15x, FL > 1e15)",
    100 < f_ds2 / 0.009805 < 104 and abs(g_uni - 0.2218) < 1e-3 and inv_a2_cross / inv_ncg["characteristic f(0)=1"] > 15
    and fl_ratio > 1e15)

# ---------------------------------------------------------------------------------------------- verdict
failed = [t for t, ok in CHECKS if not ok]
out = {"rows": len(rows), "per_family": per_family, "N_mech_record_lower_bound": n_mech, "N_rule": n_rule,
       "N_external_claims": n_ext, "AS": {"f_g_AS3": fg3, "P_EH_AS3_one_loop": p3, "P_EH_AS4_one_loop": p4,
       "f_g_required": fg_req, "lambda_roots_at_AS3_g": roots, "slope_inv_alpha0_per_lnfg": slope_req},
       "FSP": {"p_alpha": S_p, "S_max": S_MAX, "sigma_ln_alpha_bracket": sl_b, "sigma_ln_alpha_opt": sl_o,
               "needed_sigma_lnR_1pc": need_1pc, "needed_sigma_lnR_bar": need_bar},
       "precision_table": table, "P_single_uv": p_uv, "P_joint_uv": p_joint,
       "prekill": {"f_spectral_dim_2": f_ds2, "g_star_unimodular_needed": g_uni, "inv_alpha_ncg": inv_ncg,
                   "inv_alpha2_at_g2_eq_g3_one_loop": inv_a2_cross, "festina_lente_ratio_electron": fl_ratio},
       "failed": failed, "mutate": MUT}
if not MUT:
    (HERE / "cfg895_check.json").write_text(json.dumps(out, indent=1))
print(f"failed: {failed}")
if MUT:
    if "K2 AS3 f_g reproduced from its root (0.03883)" in failed:
        print("MUTATE: control works (K2 fails as required)")
        sys.exit(1)
    print("MUTATE: CONTROL BROKEN (K2 did not fail)")
    sys.exit(3)
sys.exit(0 if not failed else 1)
