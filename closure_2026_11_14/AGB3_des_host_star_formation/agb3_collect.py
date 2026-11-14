"""AGB3 collector: applies the known-answer checks and the frozen words of FROZEN_CRITERIA.md to the outputs of
agb3_run.py (KM, K1, K2, K3, K4, D) and agb3_cosmo.py (S, E, J). Writes agb3_results.json; prints the tables
(redirect to agb3_collect.out). It fits nothing."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = sys.argv[1] if len(sys.argv) > 1 else HERE
REPO = os.environ.get("AGB3_REPO") or os.path.normpath(os.path.join(HERE, "..", ".."))
AGB2 = os.path.join(REPO, "closure_2026_11_14", "AGB2_host_mass_step_redshift")


def load(name):
    p = os.path.join(OUTDIR, f"agb3_{name}.json")
    return json.load(open(p)) if os.path.exists(p) else None


def word6(d0, d1):
    if d1 >= 9 and d0 < 4: return "AGE BIAS EXCLUDED AT 3 SIGMA"
    if 4 <= d1 < 9 and d0 < 4: return "AGE BIAS DISFAVOURED"
    if d0 >= 9 and d1 < 4: return "AGE BIAS REQUIRED AT 3 SIGMA"
    if 4 <= d0 < 9 and d1 < 4: return "AGE BIAS FAVOURED"
    if d0 < 4 and d1 < 4: return "UNDECIDED"
    return "NEITHER"


def uword(a, d1):
    if d1 < 4: return "HOSTS AS LARGE AS THE SLOPE NEEDS"
    if a < 1: return "SLOPE OVERPREDICTS THE HOSTS AT 3 SIGMA" if d1 >= 9 else "SLOPE OVERPREDICTS THE HOSTS (2 SIGMA)"
    return "HOSTS LARGER THAN THE SLOPE NEEDS"


def today(q0, d):
    if d >= 4 and q0 < 0: return "ACCELERATING TODAY"
    if d >= 4 and q0 > 0: return "DECELERATING TODAY"
    return "SIGN NOT SETTLED"


def ever(d):
    if d >= 9: return "NEVER-ACCELERATED EXCLUDED AT 3 SIGMA"
    if d >= 4: return "NEVER-ACCELERATED DISFAVOURED"
    return "NEVER-ACCELERATED ALLOWED"


def second(first, others):
    bad = [k for k, w in others.items() if w != first]
    return "ROBUST" if not bad else "FRAGILE (" + "; ".join(f"{k}: {others[k]}" for k in bad) + ")"


def row(label, r, w=""):
    s = f"  {label:38s} A {r['A']:+.3f} +- {r['sd_A']:.3f} (sandwich {r['sandwich_sd_A']:.3f})  dchi2(A=0) {r['D_A0']:7.2f}  dchi2(A=1) {r['D_A1']:7.2f}"
    if "g" in r: s += f"  g {r['g']:+.4f} +- {r['sd_g']:.4f}"
    return s + (f"   {w}" if w else "")


def main():
    KM, K1, K2, K3, K4, D, S, E, J = (load(k) for k in ("KM", "K1", "K2", "K3", "K4", "D", "S", "E", "J"))
    res = dict(lane="AGB3"); pf = lambda b: "PASS" if b else "FAIL"
    print("AGB3 known-answer checks")
    print(f"  KM two-component model: passive age {KM['passive_age']:.2f} against burst age {KM['burst_age']:.2f}; constant case {KM['const_grid']:.4f} / {KM['const_quad']:.4f};"
          f" largest gap to the mass-only model on its own galaxies {KM['worst_track_gap']:.2f} Gyr -> {pf(KM['passed'])}")
    print(f"  K1 table: {K1['n_common']} in common; identity step {K1['identity_step']:+.4f}, scatter {K1['identity_scatter']:.4f} -> {pf(K1['passed'])}")
    print(f"  K2 mass step from the published standardisation: {K2['B']['g']:+.4f} +- {K2['B']['sd_g']:.4f} (published 0.033, tolerance 0.016) -> {pf(K2['passed'])}"
          f"   [raw {K2['R']['g']:+.4f} +- {K2['R']['sd_g']:.4f}; as published {K2['P']['g']:+.4f} +- {K2['P']['sd_g']:.4f}]")
    print(f"  K3 twins: {sum(t['passed'] for t in K3['twins'])} of {len(K3['twins'])} -> {pf(K3['passed'])}")
    for k in ("D1", "D2", "U"):
        print(f"  K4 {k:2s}: mean {K4[k]['mean_over_sigma']:+.3f} sigma; shuffle scatter / sigma {K4[k]['sd_over_sigma']:.3f}; sandwich / sigma {K4[k]['sandwich_over_sigma']:.3f} -> {pf(K4[k]['passed'])}")
    d_base = all((KM["passed"], K1["passed"], K2["passed"], K3["passed"]))
    res["checks"] = dict(KM=KM["passed"], K1=K1["passed"], K2=K2["passed"], K3=K3["passed"], K4={k: K4[k]["passed"] for k in ("D1", "D2", "U")})
    F = D["fits"]; P = F["primary"]

    print(f"\nPart D, the slope from the hosts ({'evaluable' if d_base else 'NOT EVALUABLE'}; primary: des_only, reading R, 20 bins, z_f 3)")
    forks_d2 = dict(reading_P="fork_P", full="fork_full", bins40="fork_bins40", pure="fork_pure", zf2="fork_zf2", zf5="fork_zf5")
    first = word6(P["D2"]["D_A0"], P["D2"]["D_A1"]); oth = {k: word6(F[v]["D2"]["D_A0"], F[v]["D2"]["D_A1"]) for k, v in forks_d2.items()}
    oth["half_template"] = word6(P["D2"]["D_A0"], P["D2"]["D_A1_half"])
    print(" D2, per host, measured star formation, constant mass step free:")
    print(row("primary", P["D2"], first))
    for k, v in forks_d2.items(): print(row("fork " + k, F[v]["D2"], oth[k]))
    print(f"  fork half_template: dchi2(A=1) {P['D2']['D_A1_half']:.2f}   {oth['half_template']}")
    ok = d_base and K4["D2"]["passed"]; res["D2"] = dict(fit=P["D2"], first=first, forks=oth, word=f"{first} / {second(first, oth)}" if ok else "NOT EVALUABLE")
    print(f"  -> D2: {res['D2']['word']}")
    forks_u = dict(reading_B="fork_B", full="fork_full", bins40="fork_bins40", pure="fork_pure", zf2="fork_zf2", zf5="fork_zf5")
    first = uword(P["U"]["A"], P["U"]["D_A1"]); oth = {k: uword(F[v]["U"]["A"], F[v]["U"]["D_A1"]) for k, v in forks_u.items()}
    oth["half_template"] = uword(2*P["U"]["A"], P["U"]["D_A1_half"]); oth["mass_only_ages"] = uword(F["U_mass"]["A"], F["U_mass"]["D_A1"])
    print(" U, the upper limit (no constant step):")
    print(row("primary", P["U"], first))
    for k, v in forks_u.items(): print(row("fork " + k, F[v]["U"], oth[k]))
    print(f"  fork half_template: A {2*P['U']['A']:+.3f} +- {2*P['U']['sd_A']:.3f}  dchi2(A=1) {P['U']['D_A1_half']:.2f}   {oth['half_template']}")
    print(row("fork mass_only_ages", F["U_mass"], oth["mass_only_ages"]))
    ok = d_base and K4["U"]["passed"]; res["U"] = dict(fit=P["U"], first=first, forks=oth, word=f"{first} / {second(first, oth)}" if ok else "NOT EVALUABLE")
    print(f"  -> U: {res['U']['word']}")
    print(" reported only:")
    print(row("D1 step run, des_only", P["D1"])); print(row("D1 step run, full", F["fork_full"]["D1"]))
    try:
        h = json.load(open(os.path.join(AGB2, "agb2_H_diag.json")))["fits"]["sample_drop_DES"]["H1"]
        w1, w2 = 1/P["D1"]["sd_A"]**2, 1/h["sd_A"]**2; a = (P["D1"]["A"]*w1 + h["A"]*w2)/(w1 + w2); s = (w1 + w2)**-0.5
        print(f"  D1 des_only combined with AGB2's Pantheon+ fit without DES ({h['A']:+.3f} +- {h['sd_A']:.3f}): A {a:+.3f} +- {s:.3f}  dchi2(A=0) {(a/s)**2:.2f}  dchi2(A=1) {((a - 1)/s)**2:.2f}")
        res["D1_combined"] = dict(A=a, sd=s, pantheon=[h["A"], h["sd_A"]], des=[P["D1"]["A"], P["D1"]["sd_A"]])
    except (OSError, KeyError):
        print("  AGB2 output not found; D1 combination skipped")
    print(row("per host, mass-only ages, step free", F["mass_perhost"]))
    for k in ("D1", "D2", "U"): print(row(f"short-delay DTD {k}", F["dtdW"][k]))
    for k in ("D2", "U"): print(row(f"full, as published {k}", F["full_P"][k]))
    c = D["contrast"]; print(f"  age gap between the mass groups (des_only): {c['two_component']:.2f} Gyr from measured star formation, {c['mass_only']:.2f} Gyr in the mass-only model")
    for rd in ("R", "P"):
        for tr in ("mass", "ssfr", "colour"):
            b = F[f"steps_des_only_{rd}_{tr}"]; print(f"  {tr} step by band, des_only, reading {rd} (young side minus old side, mag):")
            for (lo, hi), n, ny, g, sd, p, ag in zip(b["bands"], b["n"], b["n_young"], b["step"], b["sd"], b["predicted_A1"], b["age_gap"]):
                if n: print(f"     z {lo:.1f}-{hi:.1f} (n {n:4d}, young side {ny:4d})  {g:+.4f} +- {sd:.4f}   slope predicts {p:+.4f}   (age gap {ag:.2f} Gyr)")
    res["D_reported"] = {k: F[k] for k in F if k not in ("primary",)}

    if S is not None:
        s_ok = bool(KM["passed"] and K1["passed"] and S["KS_passed"]); f = S["fits"]
        print(f"\nPart S, the sample's own age drift ({'evaluable' if s_ok else 'NOT EVALUABLE'})")
        for smp in ("full", "des_only"):
            k = S["KS"][smp]; print(f"  KS {smp}: today {k['today_A0'][0]:.3f} / {k['today_A1'][0]:.3f} against AGB1 {k['today_A0'][1]:.3f} / {k['today_A1'][1]:.3f};"
                                    f" never {k['never_A0'][0]:.3f} / {k['never_A1'][0]:.3f} against {k['never_A0'][1]:.3f} / {k['never_A1'][1]:.3f} -> {pf(k['passed'])}")
        def line(label, x):
            b = x["base"]; w2, w3 = today(b["q0"], x["D_today"]), ever(x["D_never"])
            print(f"  {label:44s} Om {b['Om']:.3f} w0 {b['w0']:+.3f} wa {b['wa']:+.3f} q0 {b['q0']:+.3f}  dchi2 today {x['D_today']:6.2f}  {w2};  never {x['D_never']:7.2f}  {w3}")
            return w2, w3
        line("full, A_H = 0 (published moduli)", f["full"]["A0"])
        w2, w3 = line("full, A_H = 1 (PRIMARY)", f["full"]["A1"])
        oth = {}
        for key, lab in (("des_only", "des_only, its own T_H"), ("full_mass", "full, T_H from mass-only ages"), ("full_zf2", "full, z_f 2"), ("full_zf5", "full, z_f 5")):
            oth[key] = line(lab + ", A_H = 1", f[key]["A1"])[0]
        line("full, correction host by host (reported)", f["full_perhost"]["A1"]); line("full, A_H free (reported)", f["full"]["Afree"])
        for smp in ("full", "des_only"):
            print(f"  reported, {smp}: A_H free {f[smp]['A_free']:+.3f}; dchi2(A_H = 0) {f[smp]['D_A0']:.2f}; dchi2(A_H = 1) {f[smp]['D_A1']:.2f}")
        res["S"] = dict(S2=f"{w2} / {second(w2, oth)}" if s_ok else "NOT EVALUABLE", S3=w3 if s_ok else "NOT EVALUABLE", forks=oth,
                        q0=f["full"]["A1"]["base"]["q0"], D_today=f["full"]["A1"]["D_today"], D_never=f["full"]["A1"]["D_never"])
        print(f"  -> S2: {res['S']['S2']}\n  -> S3: {res['S']['S3']}")
        if J is not None:
            j_ok = bool(s_ok and d_base and K4["D2"]["passed"]); c = J["combos"]
            print(f"\nPart J, slope from the hosts times drift from the hosts ({'evaluable' if j_ok else 'NOT EVALUABLE'})")
            jw = {}
            for name, r in c.items():
                jw[name] = (today(r["q0"], r["D_today"]), ever(r["D_never"]))
                print(f"  {name:16s} joint A_H {r['A']:+.3f} (68% {r['ci68'][0]} to {r['ci68'][1]})  dchi2(0) {r['D_A0']:.2f} dchi2(1) {r['D_A1']:.2f}  q0 {r['q0']:+.3f}"
                      f"  dchi2 today {r['D_today']:.2f}  {jw[name][0]};  never {r['D_never']:.2f}  {jw[name][1]}   edges {r['edge']}")
            first = jw["primary"][0]; oth = {k: v[0] for k, v in jw.items() if k != "primary"}
            res["J"] = dict(J2=f"{first} / {second(first, oth)}" if j_ok else "NOT EVALUABLE", J3=jw["primary"][1] if j_ok else "NOT EVALUABLE", combos=c)
            print(f"  -> J2: {res['J']['J2']}\n  -> J3: {res['J']['J3']}")
    if E is not None:
        e_ok = bool(K1["passed"] and KM["passed"] and (S is not None and S["KS_passed"])); f = E["fits"]
        print(f"\nPart E, young hosts only ({'evaluable' if e_ok else 'NOT EVALUABLE'})")
        ew = {}
        for name in ("young", "blue", "young10", "old", "young_des"):
            x = f[name]; b = x["base"]; ew[name] = (today(b["q0"], x["D_today"]), ever(x["D_never"]))
            print(f"  {name:10s} n {x['n']:4d} ({x['n_des']} DES)  Om {b['Om']:.3f} w0 {b['w0']:+.3f} wa {b['wa']:+.3f} q0 {b['q0']:+.3f}  dchi2 today {x['D_today']:6.2f}  {ew[name][0]};"
                  f"  never {x['D_never']:7.2f}  {ew[name][1]}   [AGB1's template free: A {x['A_S_free']:+.2f}, dchi2 {x['D_AS0']:.2f} / {x['D_AS1']:.2f}]")
        first = ew["young"][0]; oth = {k: ew[k][0] for k in ("blue", "young10")}
        res["E"] = dict(E2=f"{first} / {second(first, oth)}" if e_ok else "NOT EVALUABLE", E3=ew["young"][1] if e_ok else "NOT EVALUABLE", words={k: list(v) for k, v in ew.items()})
        print(f"  -> E2: {res['E']['E2']}\n  -> E3: {res['E']['E3']}")
    with open(os.path.join(OUTDIR, "agb3_results.json"), "w") as fh: json.dump(res, fh, indent=1, default=float)
    print("\nwrote agb3_results.json")


if __name__ == "__main__":
    main()
