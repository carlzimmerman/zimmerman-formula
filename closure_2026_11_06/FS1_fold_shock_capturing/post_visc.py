#!/usr/bin/env python3
"""FS1 POST-RESULT reading (information only; NOT a label, NOT in CRITERIA f716e2f98f). Written after grade.py
returned NO VERDICT on K-visc. Two questions:
 (1) On the frozen K-visc sample (20 phantom pairs), does the PAIR ratio t_AC2q/t_v3s move with (c_Q, c_L) = (2, 1)?
 (2) The frozen sample (every 8th stiffness-on AC2q row) holds phantom rows only, so the clock-only DIFF-TIME pairs
     were never viscosity-tested. Here every 4th clock-only AC2q row (20 rows) is rerun at its deciding rung with
     (2, 1), and with (0.5, 0.25); the v3s twin is dust (no viscosity), so its time is unchanged.
Separate outputs: parts_post/, POST_VISC.json. Run from the repo root:
  nice -n 15 python3 closure_2026_11_06/FS1_fold_shock_capturing/post_visc.py
kappa = 1/2 FITTED; not theory closed; adopts nothing.
"""
import os, sys, json, importlib.util
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fs1
spec = importlib.util.spec_from_file_location("fs1_grade", os.path.join(HERE, "grade.py"))
grade = importlib.util.module_from_spec(spec); spec.loader.exec_module(grade)
ac10 = fs1.ac10
os.makedirs(os.path.join(HERE, "parts_post"), exist_ok=True)


def main():
    out = {"note": "POST-RESULT, information only; not a label; criteria f716e2f98f unchanged"}
    # (1) pair ratios on the frozen sample, base vs doubled viscosity
    s = fs1.stiff_ac2q()[::8]; q1 = []
    for a in s:
        b = fs1.twin(a); La, Lb = grade.ladder_of(a), grade.ladder_of(b)
        va = grade.load_one("parts_checks", dict(a, cq=2.0, cl=1.0, _chk="visc"), La["deciding"])
        vb = grade.load_one("parts_checks", dict(b, cq=2.0, cl=1.0, _chk="visc"), Lb["deciding"])
        ent = dict(foot=a["foot"], r_kpc=a["r_kpc"], w=a["w_kms"], M1=a["M1"], L=a["Lstar_pc"],
                   base=grade.pair_outcome(La, Lb)["outcome"], class_base=(La["label"], Lb["label"]),
                   class_visc=(fs1.klass(va), fs1.klass(vb)))
        if La["label"] == Lb["label"] == "FOLD":
            ent.update(r_base=La["dec"]["t_fold"] / Lb["dec"]["t_fold"], r_visc=va["t_fold"] / vb["t_fold"],
                       t_shift_AC2q=va["t_fold"] / La["dec"]["t_fold"] - 1)
        else:
            ent.update(Jmin_base=(La["dec"]["J_min"], Lb["dec"]["J_min"]), Jmin_visc=(va["J_min"], vb["J_min"]))
        q1.append(ent)
    out["sample_pairs_visc"] = q1
    fr = [abs(e["r_visc"] / e["r_base"] - 1) for e in q1 if "r_visc" in e]
    out["sample_max_pair_ratio_shift"] = max(fr) if fr else None
    out["sample_max_abs_time_shift"] = max(abs(e["t_shift_AC2q"]) for e in q1 if "t_shift_AC2q" in e)
    out["sample_class_changes"] = sum(e["class_base"] != e["class_visc"] for e in q1)
    print(f"(1) sample: max |r_visc/r_base - 1| = {out['sample_max_pair_ratio_shift']:.3e}; max |t shift| AC2q = "
          f"{out['sample_max_abs_time_shift']:.3e}; class changes {out['sample_class_changes']}", flush=True)

    # (2) clock-only AC2q rows, viscosity x2 and x0.5
    clk = [r for r in fs1.stiff_ac2q() if r["kind"] == "clock_only"][::4]
    jobs = []
    for r in clk:
        L = grade.ladder_of(r)
        for cq, cl in ((2.0, 1.0), (0.5, 0.25)):
            jobs.append((dict(r, cq=cq, cl=cl, _chk="post"), L["deciding"], "parts_post"))
    fs1.pool_run(jobs, 4)
    q2 = []
    for r in clk:
        L = grade.ladder_of(r); Lb = grade.ladder_of(fs1.twin(r)); tb = Lb["dec"]["t_fold"]
        ent = dict(foot=r["foot"], r_kpc=r["r_kpc"], w=r["w_kms"], M1=r["M1"], L=r["Lstar_pc"], N=L["deciding"],
                   r_base=L["dec"]["t_fold"] / tb)
        for cq, cl in ((2.0, 1.0), (0.5, 0.25)):
            v = grade.load_one("parts_post", dict(r, cq=cq, cl=cl, _chk="post"), L["deciding"])
            ent[f"r_cq{cq}"] = v["t_fold"] / tb if v and v["t_fold"] else None
        q2.append(ent)
    out["clock_only_visc"] = q2
    rb = [e["r_base"] for e in q2]; r2 = [e["r_cq2.0"] for e in q2]; r05 = [e["r_cq0.5"] for e in q2]
    out["clock_only_summary"] = dict(n=len(q2), r_base=[min(rb), max(rb)], r_cq2=[min(r2), max(r2)], r_cq05=[min(r05), max(r05)],
                                     max_shift_cq2=max(abs(a / b - 1) for a, b in zip(r2, rb)),
                                     max_shift_cq05=max(abs(a / b - 1) for a, b in zip(r05, rb)))
    print(f"(2) clock-only: {out['clock_only_summary']}", flush=True)
    json.dump(out, open(os.path.join(HERE, "POST_VISC.json"), "w"), indent=1, default=float)


if __name__ == "__main__":
    main()
