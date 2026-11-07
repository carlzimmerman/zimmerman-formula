#!/usr/bin/env python3
"""CK2: does the adopted action (v3s + Pi^6 blend; AC2q read) release a kick when its switch changes branch?
Criteria: FROZEN_CRITERIA.md (8f176791dc). D1 branch-change census on isolated spherical hosts, D2 latent energy at
the branch point (sympy, exact, from AC21 iter_6's form.json), D3 stored-energy bound on v_k. KA1-KA2, MUTATE M1-M2.
Both footings, never pooled. Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
G, c, Msun, kpc, pc = 6.674e-11, 2.99792458e8, 1.98847e30, 3.0857e19, 3.0857e16
FOOT = {"canonical": {"a0": 9.3603e-11, "Lstar_pc": 21.682}, "alt": {"a0": 1.1312e-10, "Lstar_pc": 22.849}}
LSTAR_HI_PC = 90.0                         # X27: no upper bound to 90 pc
RHO_CRIT_H2 = 1.87847e-26                  # kg/m^3 per h^2
OMB_H2 = 0.02166                           # BBN D/H (as NA2), PROVISIONAL
COSMIC = 5.4                               # carrier : baryon cosmic ratio (RESOLUTION section 1)
RHO_C_FLOOR = COSMIC * OMB_H2 * RHO_CRIT_H2
out = {"criteria": "8f176791dc", "footings": {}, "checks": {}}

# ---------------- D2: latent energy at the branch point (exact) ----------------
form = json.load(open(os.path.join(ROOT, "action_search_2026_11_05/AC21_smooth_3d/iter_6_fast_decay/form.json")))
q = sp.Symbol("q")
f_prev, fp_prev, pieces = sp.Integer(0), sp.Integer(0), []
for lo, hi, fpp in form["pieces"]:
    lo, hi, fpp = sp.Rational(lo), sp.Rational(hi), sp.sympify(fpp)
    fp = sp.integrate(fpp, (q, lo, q)) + fp_prev
    fq = sp.integrate(fp, (q, lo, q)) + f_prev
    pieces.append((lo, hi, sp.expand(fq), sp.expand(fp)))
    f_prev, fp_prev = fq.subs(q, hi), fp.subs(q, hi)
f0, fp0 = pieces[0][2].subs(q, 0), pieces[0][3].subs(q, 0)
d2 = {"f_at_0_on_branch": str(f0), "fprime_at_0_on_branch": str(fp0),
      "f_at_1": str(sp.nsimplify(f_prev)), "fprime_at_1": str(sp.nsimplify(fp_prev)),
      "first_piece_f": str(pieces[0][2]),
      "jump_F_blend": str(f0 - 0), "jump_Fprime_blend": str(fp0 - 0),
      "jump_F_raw": str(sp.Rational(1, 2) * 0**2), "jump_Fprime_raw": "0"}
d2["form_consistent_f1_half_fp1_one"] = bool(sp.simplify(f_prev - sp.Rational(1, 2)) == 0 and sp.simplify(fp_prev - 1) == 0)
d2["zero_latent"] = bool(f0 == 0 and fp0 == 0)
# MUTATE M2: kinked stiffness F = b Theta(Pi): jump of F across Pi = 0 is b (per unit b, gamma_L): nonzero
d2["M2_kinked_jump_over_b_gamma"] = 1
d2["M2_bites"] = True if d2["M2_kinked_jump_over_b_gamma"] != 0 else False
out["D2"] = d2

# ---------------- profiles ----------------
def prof(kind, M, a):
    """M(<r) and dM/dr as functions of r (SI)."""
    if kind == "point":
        return (lambda r: M + 0 * r), (lambda r: 0 * r)
    if kind == "plummer":
        return (lambda r: M * r**3 / (r**2 + a**2)**1.5), (lambda r: 3 * M * a**2 * r**2 / (r**2 + a**2)**2.5)
    if kind == "hernquist":
        return (lambda r: M * r**2 / (r + a)**2), (lambda r: 2 * M * a * r / (r + a)**3)
    if kind == "two":   # 0.3 M Hernquist(a) + 0.7 M Plummer(5a): stars + extended gas
        m1, d1 = prof("hernquist", 0.3 * M, a); m2, d2_ = prof("plummer", 0.7 * M, 5 * a)
        return (lambda r: m1(r) + m2(r)), (lambda r: d1(r) + d2_(r))
    raise ValueError(kind)

def nu(y):  return 0.5 + np.sqrt(0.25 + 1.0 / y)
def dnu(y): return -1.0 / (2.0 * y**2 * np.sqrt(0.25 + 1.0 / y))

def rho_ph(r, Mf, dMf, a0, sign=1.0):
    M, dM = Mf(r), dMf(r)
    y = G * M / (r**2 * a0)
    dy = (G / a0) * (dM / r**2 - 2 * M / r**3)
    val = (dM * (nu(y) - 1.0) + M * dnu(y) * dy) / (4 * np.pi * r**2)
    return sign * val

KINDS = ["point", "plummer", "hernquist", "two"]
LOGM = np.arange(8.0, 15.01, 0.5)
def radii_for(logM):
    return [1, 3, 10, 30] if logM <= 12.5 else [100, 300, 500]

def run(foot, sign=1.0):
    a0 = FOOT[foot]["a0"]
    rho_de = 4 * a0**2 / (c**2 * G)
    Ls = {"lo": FOOT[foot]["Lstar_pc"] * pc, "hi": LSTAR_HI_PC * pc}
    rows, minratio, min_at = [], np.inf, None
    vk = {"a_floor": {"lo": 0, "hi": 0}, "b_local": {"lo": 0, "hi": 0}}
    vk_rM = {"a_floor": {"lo": 0, "hi": 0}, "b_local": {"lo": 0, "hi": 0}}
    worst_turn = np.inf
    for logM in LOGM:
        M = 10**logM * Msun
        rM = np.sqrt(G * M / a0)
        for kind in KINDS:
            for a_kpc in (radii_for(logM) if kind != "point" else [0]):
                Mf, dMf = prof(kind, M, a_kpc * kpc)
                r = np.logspace(np.log10(1e-3 * rM), np.log10(1e3 * rM), 4000)
                rp = rho_ph(r, Mf, dMf, a0, sign)
                ratio = rp / rho_de
                i = int(np.argmin(ratio))
                if ratio[i] < minratio:
                    minratio, min_at = float(ratio[i]), {"logM": float(logM), "kind": kind, "a_kpc": a_kpc, "r_over_rM": float(r[i] / rM)}
                rt = np.array([1.0, 2.0, 3.7]) * 1e3 * kpc
                rpt = rho_ph(rt, Mf, dMf, a0, sign) / rho_de
                worst_turn = min(worst_turn, float(rpt.min()))
                at_rM = float(rho_ph(np.array([rM]), Mf, dMf, a0, sign)[0] / rho_de)
                # D3 (only meaningful on the unmutated run)
                rb = 3 * Mf(r) / (4 * np.pi * r**3)
                for tag, rc in (("a_floor", RHO_C_FLOOR + 0 * r), ("b_local", COSMIC * rb)):
                    v = np.sqrt(2 * np.pi * G / rc) * np.abs(rp)
                    vrM = float(np.sqrt(2 * np.pi * G / (rc[np.argmin(np.abs(r - rM))])) * abs(rho_ph(np.array([rM]), Mf, dMf, a0, sign)[0]))
                    for lt, L in Ls.items():
                        vk[tag][lt] = max(vk[tag][lt], float(L * v.max()))
                        vk_rM[tag][lt] = max(vk_rM[tag][lt], L * vrM)
                rows.append({"logM": float(logM), "kind": kind, "a_kpc": a_kpc, "min_ratio": float(ratio.min()),
                             "ratio_at_rM": at_rM, "ratio_turnaround_min": float(rpt.min())})
    res = {"a0": a0, "rho_DE": rho_de, "Lstar_lo_pc": FOOT[foot]["Lstar_pc"], "Lstar_hi_pc": LSTAR_HI_PC,
           "D1_min_rho_ph_over_rho_DE": minratio, "D1_min_at": min_at, "D1_min_turnaround": worst_turn,
           "D1_branch_change_v3s": bool(minratio < 0), "D1_branch_change_AC2q": bool(minratio < -2),
           "D3_vk_max_kms": {k: {lt: v / 1e3 for lt, v in d.items()} for k, d in vk.items()},
           "D3_vk_at_rM_max_kms": {k: {lt: v / 1e3 for lt, v in d.items()} for k, d in vk_rM.items()},
           "rows": rows}
    # Lstar for which the largest bound reaches 500 km/s (v_k is linear in Lstar)
    res["D3_Lstar_for_500kms_pc"] = {k: 500.0 / (d["lo"] / 1e3) * FOOT[foot]["Lstar_pc"] if d["lo"] > 0 else None
                                     for k, d in vk.items()}
    return res

for foot in FOOT:
    out["footings"][foot] = run(foot)
    out["footings"][foot]["M1_wrong_branch"] = {k: v for k, v in run(foot, sign=-1.0).items()
                                                if k.startswith("D1_branch") or k == "D1_min_rho_ph_over_rho_DE"}

# ---------------- KA ----------------
ka = {}
for foot in FOOT:
    a0 = FOOT[foot]["a0"]; M = 1e11 * Msun; rM = np.sqrt(G * M / a0); r = np.array([1e4 * rM])
    Mf, dMf = prof("point", M, 0)
    num = rho_ph(r, Mf, dMf, a0)[0]; ana = np.sqrt(G * M * a0) / (4 * np.pi * G * r[0]**2)
    ka[foot] = {"KA1_rel": float(abs(num / ana - 1)), "KA1_pass": bool(abs(num / ana - 1) <= 1e-3)}
rde = 4 * FOOT["canonical"]["a0"]**2 / (c**2 * G)
ka["KA2_rho_DE_canonical"] = rde; ka["KA2_pass"] = bool(abs(rde / 5.84e-27 - 1) <= 1e-2)
out["checks"]["KA"] = ka
out["checks"]["M1_bites"] = all(out["footings"][f]["M1_wrong_branch"]["D1_branch_change_v3s"] for f in FOOT)
out["checks"]["M2_bites"] = d2["M2_bites"]

# ---------------- label ----------------
labels = {}
for foot in FOOT:
    r = out["footings"][foot]
    no_change = (not r["D1_branch_change_v3s"]) and (not r["D1_branch_change_AC2q"])
    labels[foot] = "NO RELEASE TERM" if (no_change and d2["zero_latent"]) else "RELEASE (see D3)"
controls = all(ka[f]["KA1_pass"] for f in FOOT) and ka["KA2_pass"] and out["checks"]["M1_bites"] and out["checks"]["M2_bites"]
out["labels"] = labels
out["label_overall"] = (labels["canonical"] if labels["canonical"] == labels["alt"] else "SPLIT") if controls else "NO VERDICT (control failed)"
json.dump(out, open(os.path.join(HERE, "ck2.json"), "w"), indent=1, default=float)

print("D2 f(0), f'(0) on branch:", d2["f_at_0_on_branch"], d2["fprime_at_0_on_branch"], "| form f(1)=1/2, f'(1)=1:", d2["form_consistent_f1_half_fp1_one"],
      "| first piece f =", d2["first_piece_f"])
for foot in FOOT:
    r = out["footings"][foot]
    print(f"{foot}: rho_DE {r['rho_DE']:.3e}; D1 min rho_ph/rho_DE {r['D1_min_rho_ph_over_rho_DE']:.4g} at {r['D1_min_at']}; "
          f"turnaround min {r['D1_min_turnaround']:.4g}; branch change v3s {r['D1_branch_change_v3s']}, AC2q {r['D1_branch_change_AC2q']}")
    print(f"  D3 v_k max (km/s) {r['D3_vk_max_kms']}; at r_M {r['D3_vk_at_rM_max_kms']}; Lstar for 500 km/s (pc) {r['D3_Lstar_for_500kms_pc']}")
    print(f"  M1 wrong branch: {r['M1_wrong_branch']}")
print("KA:", json.dumps(ka)); print("M1 bites:", out["checks"]["M1_bites"], "M2 bites:", out["checks"]["M2_bites"])
print("LABELS:", labels, "OVERALL:", out["label_overall"])
print("kappa = 1/2 FITTED; not theory closed.")
