"""AKD1 grade: known answers, MUTATE bites, and the frozen label rule (criteria d88d310eb1, section 4).
Reads the lane's outputs only. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda n: json.load(open(os.path.join(HERE, n)))
a1, k4, dec, ev = J("akd1_a1.json"), J("akd1_k4.json"), J("akd1_dec.json"), J("akd1_eval.json")
k4m, decm = J("akd1_k4_MUTATE_MU3.json"), J("akd1_dec_MUTATE_MU3.json")
mu1, mu2 = J("akd1_eval_MUTATE_MU1.json"), J("akd1_eval_MUTATE_MU2.json")
out = {}
def say(*a):
    print(*a, flush=True)

ka = {
    "KA1 K1 covariant current vs EL (<= 1e-30)": a1["K1_pass"] and max(a1["K1_residuals"]) <= 1e-30,
    "KA2 FY = 0 gives TK1's A_z = FQQ a^5/(4 N0 adot^2)": k4["KA2_residual"] == "0",
    "KA3 M_2 constant: mu_B1a 198.25 / 198.24 to 1e-4": ev["KA3_pass"],
    "KA4 K4's A_z(k)/A_z(0) = decoupling inertia ratio": dec["KA4_pass"] and k4["KA4_residual"] == "0",
    "KA5 flat law-on dispersion = SCS1 closed form (and TPA1 4.4)": dec["KA5_pass"] and dec["KA5_TPA1_4.4_residual_at_Km_1"] == "0",
    "KA6 law g closed form vs root solve (1e-12)": ev["KA6_pass"],
}
struct = {"K2 no velocity in L_K (unitary gauge)": a1["K2_pass"],
          "K3 symbol ratio 1 at the jets where defined": all(abs(r - 1) < 1e-12 for r in a1["K3_symbol_ratio"] if r is not None)}
say("== known answers"); [say("  %-62s %s" % (k, "PASS" if v else "FAIL")) for k, v in ka.items()]
say("== structural checks"); [say("  %-62s %s" % (k, "PASS" if v else "FAIL")) for k, v in struct.items()]
out["known_answers"] = ka; out["structural"] = struct

# MUTATE
def kth3400(evj, label, f):
    r = evj["A1"][label][f]["rows"]["3400"]
    M20 = 3e4**2 + 1e-6
    return (M20 * (1 + r["q0"])**2 / (r["R"] - 1))**0.5
bites = {}
bites["MU1 p -> -2 flips A1 to WELL-POSED (both footings)"] = all(
    mu1["A1"]["MU1_p_minus2"][f]["label"] == "WELL-POSED AROUND FRW" for f in ("canonical", "alt"))
r_k = {f: kth3400(mu2, "MU2_gc_x100", f) / kth3400(ev, "primary", f) for f in ("canonical", "alt")}
zx = {f: (ev["A1"]["primary"][f]["z_x_R_equals_1"], mu2["A1"]["MU2_gc_x100"][f]["z_x_R_equals_1"]) for f in ("canonical", "alt")}
bites["MU2 g_c x 100 moves the z 3400 threshold k by >= 10 and moves z_x"] = all(r_k[f] >= 10 and zx[f][0] != zx[f][1] for f in r_k)
bites["MU3 FY dropped: KA4 fails (K4 side and decoupling side)"] = (k4m["KA4_residual"] != "0") and (not decm["KA4_pass"])
lean_ok = open(os.path.join(HERE, "compile.txt")).read().strip().endswith("exit 0")
mut_txt = open(os.path.join(HERE, "compile_MUTATE.txt")).read()
fail_lines = sorted({int(m.group(1)) for m in re.finditer(r"AKD1_MUTATE\.lean:(\d+):", mut_txt)})
lean_src = open(os.path.join(HERE, "AKD1_MUTATE.lean")).read().splitlines()
thm_starts = [i + 1 for i, l in enumerate(lean_src) if l.startswith("theorem ")]
failed_thms = {max(s for s in thm_starts if s <= ln) for ln in fail_lines}
bites["Lean: AKD1.lean compiles; every false twin fails"] = lean_ok and len(failed_thms) == len(thm_starts) == 9
say("== MUTATE"); [say("  %-66s %s" % (k, "BITES" if v else "DOES NOT BITE")) for k, v in bites.items()]
say("  MU2: threshold k at z 3400 moves x%.1f / x%.1f; z_x %s" % (r_k["canonical"], r_k["alt"], zx))
say("  Lean: %d of %d false theorems fail" % (len(failed_thms), len(thm_starts)))
out["mutate"] = bites; out["MU2_kth_ratio"] = r_k; out["MU2_zx"] = zx

# labels
labels = {}
for f in ("canonical", "alt"):
    if not all(ka.values()):
        lab = "NO VERDICT"
    elif ev["A1"]["primary"][f]["label"] != "WELL-POSED AROUND FRW" or not all(struct.values()) or not ka["KA1 K1 covariant current vs EL (<= 1e-30)"]:
        lab = "BREAKS AT A1"
    else:
        lab = "(A1 passes: continue to A3)"
    labels[f] = lab
out["labels"] = labels
say("== LABEL (Part A): canonical %s / alt %s;  Part B: NOT GRADED (Part A structurally dead)" % (labels["canonical"], labels["alt"]))
against = []
for f in ("canonical", "alt"):
    p = ev["A1"]["primary"][f]
    against.append("%s: ghost on R1 at z %s (z_x %.2f); R0 ghost at z 3400, 1100, 10 within [H, 1/pc]" % (f, p["ghost_on_R1_at"], p["z_x_R_equals_1"]))
    for nm, b in ev["brackets"].items():
        against.append("%s bracket %s: %s, ghost on R1 at z %s" % (f, nm, b[f]["label"] if f in b else b, b[f]["ghost_on_R1_at"] if f in b else ""))
    wins = [lm for lm, w in ev["A4_W"][f].items() if w["W_max_inside_window"] > 1]
    against.append("%s: W > 1 inside the middle KiDS window at log M_b %s (frozen label 4 would also fire)" % (f, wins))
out["counts_against"] = against
say("== counts against the candidate"); [say("  " + a) for a in against]
json.dump(out, open(os.path.join(HERE, "akd1_grade.json"), "w"), indent=1, default=str)
