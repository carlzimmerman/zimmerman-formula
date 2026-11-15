#!/usr/bin/env python3
"""DP8 grader (criteria FROZEN_CRITERIA.md, 4caa8bc91f): reads the check runner's outputs (checks/, dry_run_dr3/) and writes
dp8_checks.json (machine-readable states the release-day wrapper reads: q1_launcher_check, q8_code_path_check) and dp8_checks.out.
Each check is graded with its mutation twin; a check passes only if the check passes AND its mutation bites. Offline; reads files.
  python3 -B dp8_grade.py [--stage1]     --stage1: before C6 (which needs the q1 state); C6 and the labels read 'pending'
kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.
"""
import sys
sys.dont_write_bytecode = True
import hashlib, json, os, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
O, DRY = HERE / "checks", HERE / "dry_run_dr3"
DP3, DP7 = REPO / "dr4_push_2026_11_05" / "DP3_release_day", REPO / "dr4_push_2026_11_05" / "DP7_seed_mean_check"
CORRECTED = {"/nss_off_seed_mean/note", "/canonical/nss_off_entry_in_b_and_e", "/alt/nss_off_entry_in_b_and_e"}
STAGE1 = "--stage1" in sys.argv


def txt(p):
    try:
        return Path(p).read_text()
    except FileNotFoundError:
        return ""


def js(p):
    try:
        return json.loads(Path(p).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def exit_of(t):
    m = re.findall(r"^exit (\d+)$", t, re.M)
    return int(m[-1]) if m else None


def leaves(x, p=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from leaves(v, p + "/" + str(k))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from leaves(v, p + "/" + str(i))
    else:
        yield p, x


def cmp_json(mine, ref, allowed_strings=frozenset()):
    a, b = js(mine), js(ref)
    if a is None or b is None:
        return dict(ok=False, why=f"missing {'mine' if a is None else 'ref'}")
    o, r = dict(leaves(a)), dict(leaves(b))
    num = [k for k, v in r.items() if isinstance(v, (int, float)) and not isinstance(v, bool)]
    bad = [k for k in num if o.get(k) != r[k]]
    sd = sorted(k for k, v in r.items() if not isinstance(v, (int, float)) or isinstance(v, bool) if o.get(k) != v)
    ok = (not bad) and set(o) == set(r) and set(sd) <= set(allowed_strings)
    return dict(ok=ok, n_numeric=len(num), n_numeric_differ=len(bad), keys_equal=(set(o) == set(r)), other_leaves_differ=sd,
                b=[o.get("/canonical/b"), o.get("/alt/b")], ref_b=[r.get("/canonical/b"), r.get("/alt/b")], examples=bad[:5])


def sha(p):
    try:
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()
    except FileNotFoundError:
        return None


def passlines(t):
    out = {}
    for line in t.splitlines():
        m = re.match(r"^\S+Z (PASS|FAIL) (.*)$", line)
        if m:
            key = re.sub(r"\s*\(peak RSS [0-9.]* GB\)", "", m.group(2)).strip()
            key = re.sub(r"\s*\(exit \d+\)$", "", key)
            out[key] = m.group(1)
    return out


def dry_compare(mine_text, ref_text):
    ref, mine = passlines(ref_text), passlines(mine_text)
    missing = [k for k, v in ref.items() if v == "PASS" and mine.get(k) != "PASS"]
    new = {k: v for k, v in mine.items() if k not in ref}
    fails = [k for k, v in mine.items() if v != "PASS"]
    return dict(ok=(not missing and not fails), n_ref_pass=sum(v == "PASS" for v in ref.values()), n_mine_pass=sum(v == "PASS" for v in mine.values()),
                ref_steps_not_pass=missing, failing=fails, new_steps=new)


R = {}
# ---------------------------------------------------------------- C1
c1 = txt(O / "c1_check.out"); ctl = txt(O / "c1_mirror_control.out"); m15b = txt(O / "c1_MUTATE_15b.out"); m15 = txt(O / "c1_MUTATE_15.out")
pb, pa = txt(O / "pins_before.txt"), txt(O / "pins_after.txt")
R["C1"] = dict(check=("hashes: all 30 pinned files OK" in c1 and "SUMMARY hashes OK" in c1), mirror_control=("SUMMARY hashes OK" in ctl),
               mutate_15b=("HASH MISMATCH prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-15b_DR4_OPEN_GAPS.md" in m15b and "NOT clean" in m15b and "SUMMARY hashes FAIL" in m15b),
               mutate_15=("HASH MISMATCH prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-15_DR4_FORM_B_READING.md" in m15 and "NOT clean" in m15 and "SUMMARY hashes FAIL" in m15),
               pins_before_after_equal=(bool(pb) and pb == pa) if pa else "pending (post)",
               pins_count=re.findall(r"pinned files: (\d+); off their pinned value: (\d+)", pb))
R["C1"]["passed"] = bool(R["C1"]["check"] and R["C1"]["mirror_control"] and R["C1"]["mutate_15b"] and R["C1"]["mutate_15"] and R["C1"]["pins_before_after_equal"] is not False)
# ---------------------------------------------------------------- C2
ast_ok = "IDENTICAL" in txt(O / "c2_text_only.out"); ast_mut = "DIFFERENT" in txt(O / "c2_text_only_MUTATE.out")
optoff = cmp_json(O / "c2_d6_replay_optoff.json", DP7 / "dp3_d6_replay.json")
d6in = cmp_json(O / "c2_d6inputs_seedmean.json", DP7 / "dp3_seedmean_d6inputs.json", CORRECTED)
rp = cmp_json(O / "c2_seedmean_releasepath.json", DP7 / "dp3_seedmean_releasepath.json", CORRECTED)
rp_dry = cmp_json(DRY / "sigma_sys_dr3_releasepath_seedmean.json", DP7 / "dp3_seedmean_releasepath.json", CORRECTED)
mut = cmp_json(O / "c2_MUTATE_no_option.json", DP7 / "dp3_seedmean_releasepath.json", CORRECTED)
ref = js(DP7 / "dp3_seedmean_releasepath.json") or {}
mj = js(O / "c2_MUTATE_no_option.json") or {}
mut_single = all(mj.get(f, {}).get("b") == ref.get(f, {}).get("b_single_seed") for f in ("canonical", "alt"))
R["C2"] = dict(text_only_ast=ast_ok, text_only_mutate_bites=ast_mut, option_off_d6_replay=optoff, option_on_d6_inputs=d6in, release_path_standalone=rp,
               release_path_dry_run_D6c=rp_dry, mutate_no_option=dict(comparison_fails=not mut["ok"], b=mut["b"], equals_reference_b_single_seed=mut_single))
R["C2"]["passed"] = bool(ast_ok and ast_mut and optoff["ok"] and d6in["ok"] and rp["ok"] and rp_dry["ok"] and not mut["ok"] and mut_single)
# ---------------------------------------------------------------- C3
dry = txt(O / "c3_dry_run.out"); dref = txt(DP3 / "dry_run_dr3" / "release_day_dryrun.out")
dc = dry_compare(dry, dref)
doctored = dref.replace("PASS D7 R reproduces the official DR3 C4 (R, N_R)", "FAIL D7 R reproduces the official DR3 C4 (R, N_R)", 1)
dmut = dry_compare(doctored, dref)
Path(O / "c3_MUTATE_comparator.out").write_text("MUTATE C3: DP3's committed dry-run log with 'PASS D7 R reproduces the official DR3 C4 (R, N_R)' turned into FAIL, "
                                                 f"compared with the reference: comparator ok = {dmut['ok']}; steps not PASS: {dmut['ref_steps_not_pass']}; failing: {dmut['failing']}\n")
st = txt(DRY / "D1_selftest_dr4_outcome_map.out"); st_ref = txt(DP3 / "dr4_outcome_map_selftest.out")
m1, m2 = txt(O / "c3_outcome_map_MUTATE1.out"), txt(O / "c3_outcome_map_MUTATE2.out")
nums = dict(d2_extract_builder=("6,210 pairs, sha256 6fff64d964ebaa72" in dry), d2_cones_literal=("6180 pairs, sha256 c5cb89e8f95bfe3d" in dry),
            d3_gamma=("gamma-hat 1.0750 = 1.0750" in dry), d6_reproduces=("PASS D6 ladder shifts and sigma_sys(b) reproduce the D2 lane" in dry and "max diff 0.0000; (b) 0.0375 vs 0.0375" in dry and "(b) 0.0412 vs 0.0412" in dry),
            d7_R=("R 0.972839 (official C4 0.972839), N_R 348 (348)" in dry))
ld = {}
for f in ("outcome_map_dr3_dryrun.out", "outcome_map_dr3_dryrun_releasepath.out"):
    a, b = txt(DRY / f), txt(DP3 / "dry_run_dr3" / f)
    ld[f] = dict(identical=(a == b and bool(a)), labels_mine=re.findall(r"(UNDECIDED\w*|LAW_FIRST_EXCLUDED|SCREENED_EXCLUDED|BOTH_EXCLUDED|GUARD_ZONE|SUB_NEWTON_NO_VERDICT)", a)[:8],
                 labels_ref=re.findall(r"(UNDECIDED\w*|LAW_FIRST_EXCLUDED|SCREENED_EXCLUDED|BOTH_EXCLUDED|GUARD_ZONE|SUB_NEWTON_NO_VERDICT)", b)[:8])
labels_same = all(v["labels_mine"] == v["labels_ref"] and v["labels_mine"] for v in ld.values())
R["C3"] = dict(dry_run_exit=exit_of(dry), complete=("DRY RUN COMPLETE: every D step PASS" in dry), compare=dc, numbers=nums, outcome_map_files=ld, d8_labels_same=labels_same,
               outcome_map_selftest=dict(twenty_of_twenty=("20/20" in st), identical_to_committed=(st == st_ref)),
               outcome_map_mutate1=dict(exit=exit_of(m1), thirteen=("13/20" in m1)), outcome_map_mutate2=dict(exit=exit_of(m2), nineteen=("19/20" in m2)),
               mutate_comparator_bites=(not dmut["ok"]))
R["C3"]["passed"] = bool(dc["ok"] and R["C3"]["complete"] and R["C3"]["dry_run_exit"] == 0 and all(nums.values()) and labels_same and ("20/20" in st)
                         and exit_of(m1) == 1 and "13/20" in m1 and exit_of(m2) == 1 and "19/20" in m2 and not dmut["ok"])
# ---------------------------------------------------------------- C4
c4 = txt(O / "c4_ruwe.out"); hs = re.findall(r"([0-9a-f]{64})", c4); c4m = txt(O / "c4_MUTATE_merged.out"); hm = re.findall(r"([0-9a-f]{64})", c4m)
dry_c4 = ("PASS D6d the main sigma_sys json is byte-identical after the information call" in dry)
R["C4"] = dict(main_sha_before_after_fresh=hs, all_equal=(len(hs) == 3 and len(set(hs)) == 1), dry_run_D6d=dry_c4,
               mutate_merged_differs=(len(hm) == 2 and hm[0] != hm[1]),
               b_e=dict(main={f: [(js(O / "c4_main.json") or {}).get(f, {}).get(x) for x in ("b", "e")] for f in ("canonical", "alt")},
                        ruwe_info={f: [(js(O / "c4_ruwe_info.json") or {}).get(f, {}).get(x) for x in ("b", "e")] for f in ("canonical", "alt")},
                        merged_mutate={f: [(js(O / "c4_MUTATE_merged.json") or {}).get(f, {}).get(x) for x in ("b", "e")] for f in ("canonical", "alt")}))
R["C4"]["passed"] = bool(R["C4"]["all_equal"] and dry_c4 and R["C4"]["mutate_merged_differs"])
# ---------------------------------------------------------------- C5 (the Q8 code-path check)
s1, s1m = js(O / "c5_selftest.json") or {}, js(O / "c5_selftest_MUTATE.json") or {}
a1 = js(O / "c5_standalone_1.json") or {}
h = {k: sha(p) for k, p in (("standalone_1", O / "c5_standalone_1.json"), ("standalone_2", HERE / "work" / "c5_standalone_2.json"),
                            ("dry_run_D9", DRY / "sepbins_dr3.json"), ("mutate_droprow", O / "c5_MUTATE_droprow.json"))}
R["C5"] = dict(i_selftest=bool(s1.get("passed")), i_mutate_edges_fails=(s1m.get("passed") is False),
               ii_finite_7_bins=bool(a1.get("all_finite") and len(a1.get("rows", [])) == 7), ii_deterministic=bool(h["standalone_1"] and h["standalone_1"] == h["standalone_2"]),
               iii_dry_run_equals_standalone=bool(h["standalone_1"] and h["standalone_1"] == h["dry_run_D9"]), iii_mutate_droprow_differs=bool(h["mutate_droprow"] and h["mutate_droprow"] != h["standalone_1"]),
               sha256=h, rows=[dict(bin=f"{r['lo']:g}-{r['hi']:g}", n=r["n"], r_b=round(r["ratio"], 4), sigma_b=round(r["sig_med"], 4)) for r in a1.get("rows", [])])
R["C5"]["passed"] = all(R["C5"][k] for k in ("i_selftest", "i_mutate_edges_fails", "ii_finite_7_bins", "ii_deterministic", "iii_dry_run_equals_standalone", "iii_mutate_droprow_differs"))
# ---------------------------------------------------------------- C7
FO = ("canonical", "alt")


def k_rows(d1, d2, ks=(0, 1, 2), pref="dp7"):
    rows, ok = [], True
    for k in ks:
        a, b = js(d1 / f"{pref}_k{k:02d}.json"), js(d2 / f"dp7_k{k:02d}.json")
        if a is None or b is None:
            return False, [dict(k=k, missing=True)]
        q = [("base n_pairs", a["base"]["n_pairs"], b["base"]["n_pairs"]), ("base sha256", a["base"]["sha256"], b["base"]["sha256"]),
             ("rung n_pairs", a["rung"]["n_pairs"], b["rung"]["n_pairs"]), ("rung sha256", a["rung"]["sha256"], b["rung"]["sha256"])]
        for f in FO:
            for x in ("base", "rung", "delta", "sigma_fit_base", "sigma_fit_rung"):
                q.append((f"{f} {x}", a[f][x], b[f][x]))
        for nm, u, v in q:
            ok &= (u == v)
            rows.append(dict(k=k, quantity=nm, launcher=u, dp7=v, identical=(u == v)))
    return ok, rows


eq_ok, eq_rows = k_rows(O / "c7_eq", DP7 / "parts")
mu_ok, mu_rows = k_rows(O / "c7_MUTATE", DP7 / "parts")
mut_parts = [js(O / "c7_MUTATE" / f"dp7_k{k:02d}.json") for k in (0, 1, 2)]
mut_shape = all(p and p["rung"]["sha256"] == p["base"]["sha256"] and all(p[f]["delta"] == 0 for f in FO) for p in mut_parts)
cnt = js(DRY / "nss_off_fallback_counts_dr3.json") or {}
g11, swp = cnt.get("g11_rung") or {}, cnt.get("sweep_rung_k0") or {}
rerr, cmut = txt(O / "c7b_MUTATE_rung_error.out") + txt(HERE / "logs" / "c7b_rung_error.time"), txt(O / "c7b_MUTATE_count.out")
R["C7"] = dict(a_launcher_equals_dp7_parts=eq_ok, a_n_values=len(eq_rows), a_n_identical=sum(r.get("identical", False) for r in eq_rows),
               a_launcher_exit=exit_of(txt(O / "c7_launcher_eq.out")), a_mutate_keepnss_comparison_fails=(not mu_ok), a_mutate_rung_equals_base_deltas_zero=mut_shape,
               b_counts=dict(g11_form=g11.get("n_without_cone"), g11_flagged=g11.get("n_flagged_by_fallback"), g11_policy=g11.get("policy"),
                             sweep_k0=swp.get("n_without_cone"), sweep_flagged=swp.get("n_flagged_by_fallback"), sweep_policy=swp.get("policy")),
               b_mutate_rung_error=dict(exit=exit_of(rerr), cone_coverage_error=("ConeCoverageError" in rerr)), b_mutate_count_exit=exit_of(cmut),
               rows=eq_rows)
R["C7"]["a_passed"] = bool(eq_ok and R["C7"]["a_launcher_exit"] == 0 and not mu_ok and mut_shape)
R["C7"]["b_passed"] = bool(g11.get("n_without_cone") == 139 and swp.get("n_without_cone") == 139 and g11.get("n_flagged_by_fallback") == 0 and swp.get("n_flagged_by_fallback") == 0
                           and g11.get("policy") == "extract-fallback" and (exit_of(rerr) or 0) != 0 and "ConeCoverageError" in rerr and exit_of(cmut) == 1
                           and "PASS D5b fallback count = DP7's 139 pairs, 0 flagged" in dry)
R["C7"]["passed"] = R["C7"]["a_passed"] and R["C7"]["b_passed"]
# ---------------------------------------------------------------- C6
if not STAGE1:
    real, g1, g11s, mg = txt(O / "c6_run_real.out"), txt(O / "c6_run_noGO_G1.out"), txt(O / "c6_run_noGO_G11S.out"), txt(O / "c6_MUTATE_GO_G11S.out")
    pre = txt(O / "c6_G11S_no_checkfile.out"); sbc = txt(O / "c6_sandbox_control.out")
    R["C6"] = dict(a_real_run_refused_exit3=(exit_of(real) == 3 and "STOP: DR4 not yet available" in real),
                   b_stop_at_G1_exit10=(exit_of(g1) == 10 and "STOP at G1" in g1),
                   c_stop_at_G11S_exit10=(exit_of(g11s) == 10 and "STOP at G11S" in g11s),
                   c_before_checkfile_needs_owner_exit7=(exit_of(pre) == 7 and "NEEDS OWNER" in pre),
                   mutate_GO_G11S=dict(exit=exit_of(mg), go_on_record=("G11S: GO on record" in mg), step_failed=("STEP FAILED: G11S" in mg)),
                   d_launcher_refusals_in_dry_run=sum(1 for k, v in passlines(dry).items() if k.startswith("D5c") and v == "PASS"),
                   e_sandbox_control_denied=("denied" in sbc and "CONNECTED" not in sbc))
    f1, f2, fm = txt(O / "c6f_no_output.out"), txt(O / "c6f_form_ok.out"), txt(O / "c6f_MUTATE_K8.out")
    R["C6"]["f_amendment_A1"] = dict(f1_no_output_needs_owner=(exit_of(f1) == 7 and "O12: NEEDS OWNER" in f1),
                                     f2_form_ok_reaches_sigma_sys=(exit_of(f2) == 7 and "STEP FAILED: O12 sigma_sys" in f2 and "NEEDS OWNER" not in f2),
                                     mutate_K8_needs_owner=(exit_of(fm) == 7 and "O12: NEEDS OWNER" in fm))
    R["C6"]["passed"] = bool(R["C6"]["a_real_run_refused_exit3"] and R["C6"]["b_stop_at_G1_exit10"] and R["C6"]["c_stop_at_G11S_exit10"] and R["C6"]["c_before_checkfile_needs_owner_exit7"]
                             and exit_of(mg) == 7 and R["C6"]["mutate_GO_G11S"]["go_on_record"] and R["C6"]["mutate_GO_G11S"]["step_failed"]
                             and R["C6"]["d_launcher_refusals_in_dry_run"] == 3 and R["C6"]["e_sandbox_control_denied"] and all(R["C6"]["f_amendment_A1"].values()))
else:
    R["C6"] = dict(passed="pending")
q1 = "PASS" if R["C7"]["a_passed"] else "FAIL"
q8 = "PASS" if R["C5"]["passed"] else "FAIL"
P = lambda k: R[k]["passed"] is True
labels = {}
if not STAGE1:
    labels = {"Q1": "WIRED" if all(P(k) for k in ("C1", "C2", "C3", "C6")) and R["C7"]["a_passed"] else "NOT WIRED",
              "Q2": "WIRED" if R["C7"]["b_passed"] and P("C3") else "NOT WIRED",
              "Q5": "WIRED" if P("C4") else "NOT WIRED",
              "Q8": "WIRED" if P("C5") else "NOT WIRED (the wrapper prints NOT RUN)",
              "pins": "WIRED" if P("C1") else "NOT WIRED"}
out = dict(lane="DP8", criteria="FROZEN_CRITERIA.md (4caa8bc91f)", stage=("1 (before C6)" if STAGE1 else "final"),
           q1_launcher_check=q1, q8_code_path_check=q8, checks={k: R[k]["passed"] for k in ("C1", "C2", "C3", "C4", "C5", "C6", "C7")}, labels=labels,
           note="DR3 numbers are code-path tests, never results. kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.")
(HERE / "dp8_checks.json").write_text(json.dumps(out, indent=1) + "\n")
(HERE / "dp8_grade_detail.json").write_text(json.dumps(R, indent=1, default=str) + "\n")
lines = [f"DP8 grade ({out['stage']}): q1_launcher_check {q1}; q8_code_path_check {q8}"]
for k in ("C1", "C2", "C3", "C4", "C5", "C6", "C7"):
    lines.append(f"  {k}: {R[k]['passed']}")
for k, v in labels.items():
    lines.append(f"  label {k}: {v}")
lines.append(out["note"])
(HERE / "dp8_checks.out").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
