"""AGB2 collector: applies the known-answer checks and the frozen words of FROZEN_CRITERIA.md to the outputs of
agb2_run.py (KG, K1, K2, K3, K4, H) and agb2_joint.py (J). Writes agb2_results.json; prints the tables
(redirect to agb2_collect.out). It fits nothing."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = sys.argv[1] if len(sys.argv) > 1 else HERE
load = lambda name: json.load(open(os.path.join(OUTDIR, f"agb2_{name}.json")))


def word6(d0, d1):
    if d1 >= 9 and d0 < 4: return "AGE BIAS EXCLUDED AT 3 SIGMA"
    if 4 <= d1 < 9 and d0 < 4: return "AGE BIAS DISFAVOURED"
    if d0 >= 9 and d1 < 4: return "AGE BIAS REQUIRED AT 3 SIGMA"
    if 4 <= d0 < 9 and d1 < 4: return "AGE BIAS FAVOURED"
    if d0 < 4 and d1 < 4: return "UNDECIDED"
    return "NEITHER"


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
    return "ROBUST" if not bad else "FRAGILE (" + ", ".join(f"{k}: {others[k]}" for k in bad) + ")"


def row(label, r, w=None):
    s = f"  {label:34s} A {r['A']:+.3f} +- {r['sd_A']:.3f}   dchi2(A=0) {r['D_A0']:6.2f}   dchi2(A=1) {r['D_A1']:6.2f}"
    if "g" in r: s += f"   g {r['g']:+.4f} +- {r['sd_g']:.4f}"
    return s + (f"   {w}" if w else "")


def main():
    KG, K1, K2, K3, K4, H = (load(k) for k in ("KG", "K1", "K2", "K3", "K4", "H"))
    F = H["fits"]; res = dict(lane="AGB2")
    checks = dict(KG=KG["passed"], K1=K1["passed"], K2=K2["passed"], K3=K3["passed"], K4=K4["passed"])
    print("AGB2 known-answer checks")
    print(f"  KG galaxy model: anchor {KG['anchor']:.3f}; rise share {KG['frac_rise']:.3f}; half formed by {KG['half_formed_lookback']:.2f} Gyr,"
          f" middle half {KG['middle_half_span']:.2f} Gyr; step convergence {KG['step_convergence']:.4f} Gyr -> {'PASS' if KG['passed'] else 'FAIL'}")
    print(f"  K1 supernovae-only flat LCDM: Om {K1['Om']:.4f} (target 0.334, tolerance 0.009) -> {'PASS' if K1['passed'] else 'FAIL'}")
    print(f"  K2 raw constant step: g {K2['R']['g']:+.4f} +- {K2['R']['sd_g']:.4f} mag (window 0.02-0.09) -> {'PASS' if K2['passed'] else 'FAIL'}"
          f"   [published magnitudes: {K2['P']['g']:+.4f} +- {K2['P']['sd_g']:.4f}]")
    print(f"  K3 twins: {sum(t['passed'] for t in K3['twins'])} of {len(K3['twins'])} pass -> {'PASS' if K3['passed'] else 'FAIL'}")
    for tn in ("run", "host"):
        k = K4[tn]; print(f"  K4 {tn:4s}: mean {k['mean_over_sigma']:+.3f} sigma, scatter ratio {k['sd_over_sigma']:.3f} -> {'PASS' if k['passed'] else 'FAIL'}")
    h_ok = all(checks[k] for k in ("KG", "K1", "K3", "K4")); r_ok = checks["K2"]
    res.update(checks=checks, partH_evaluable=bool(h_ok), readingR_evaluable=bool(r_ok))
    prim = "primary" if r_ok else "fork_P"
    forks = dict(reading_P="fork_P", median="fork_median", bins40="fork_bins40", measured="fork_measured")
    print(f"\nPart H ({'evaluable' if h_ok else 'NOT EVALUABLE: numbers below are a reading only'}; judged on {'reading R' if r_ok else 'reading P (K2 failed)'})")
    res["H"] = {}
    for hn, title in (("H1", "step run"), ("H2", "per host")):
        p = F[prim][hn]; first = word6(p["D_A0"], p["D_A1"])
        others = {k: word6(F[v][hn]["D_A0"], F[v][hn]["D_A1"]) for k, v in forks.items() if v != prim}
        sec = second(first, others) if r_ok else "FRAGILE (no R)"
        print(f" {hn}, {title}:")
        print(row("primary (all, R, mean, 20 bins)" if r_ok else "primary (all, P, mean, 20 bins)", p, first))
        for k, v in forks.items():
            if v != prim: print(row("fork " + k, F[v][hn], others[k]))
        word = f"{first} / {sec}" if h_ok else "NOT EVALUABLE"
        print(f"  -> {hn}: {word}")
        res["H"][hn] = dict(primary=p, first=first, forks={k: dict(fit=F[v][hn], word=others[k]) for k, v in forks.items() if v != prim},
                            second=sec, word=word)
    print("\nReported only")
    print("  model age gap high - low (Gyr) at z " + " ".join(f"{z:g}" for z in H["dtau"]["z"]) + ": " + " ".join(f"{v:.2f}" for v in H["dtau"]["gyr"]))
    for rd in ("R", "P"):
        b = F["bands_" + rd]; print(f"  constant step by redshift band, reading {rd} (low-mass minus high-mass, mag):")
        for (a, c), zb, n, g, s, p in zip(b["bands"], b["z_mean"], b["n"], b["step"], b["sd"], b["predicted_A1"]):
            print(f"     z {a:.2f}-{c:.2f} (mean {zb:.3f}, n {n:4d})  {g:+.4f} +- {s:.4f}    slope predicts at A = 1: {p:+.4f}")
        print(f"     straight line: {b['line_slope']:+.4f} +- {b['line_slope_sd']:.4f} mag per unit z; predicted at A = 1: {b['line_slope_predicted_A1']:+.4f}")
    print(row("reading R, constant step fixed at 0", F["R_g0"]))
    for k in [x for x in F if x.startswith(("model_", "sample_"))]:
        print(row(k + " H1", F[k]["H1"])); print(row(k + " H2", F[k]["H2"]))
    res["reported"] = {k: F[k] for k in F if k not in ("primary",) + tuple(forks.values())}
    res["population_z0_median_gyr"] = KG["population_z0_median"]
    print(f"  the C14 galaxies' own z = 0 population: median progenitor age {KG['population_z0_median']:.2f} Gyr (AGB1's template: 6.70 Gyr)")

    try:
        J = load("J")
    except FileNotFoundError:
        J = None
    if J is not None:
        j_ok = bool(h_ok and J["KJ_passed"]); hk = "H1_R" if r_ok else "H1_P"; S = J["samples"]
        print(f"\nPart J ({'evaluable' if j_ok else 'NOT EVALUABLE: numbers below are a reading only'}); host prior {hk}: A {J['hosts'][hk][0]:+.3f} +- {J['hosts'][hk][1]:.3f}")
        for s in ("full", "des_only"):
            k = S[s]["KJ"]; print(f"  KJ {s}: no-prior dchi2 {k['D_A0'][0]:.3f} / {k['D_A1'][0]:.3f} against AGB1 {k['D_A0'][1]:.3f} / {k['D_A1'][1]:.3f}"
                                  f" -> {'PASS' if k['passed'] else 'FAIL'}")
        combos = [("full", hk)] + [(s, h) for s in ("full", "des_only") for h in ("H1_R", "H1_P") if (s, h) != ("full", hk)]
        res["J"] = dict(evaluable=j_ok, combos={})
        for s, h in combos:
            r = S[s]["joint"][h]; w1 = word6(r["D_A0"], r["D_A1"]); w2 = today(r["q0"], r["D_today"]); w3 = ever(r["D_never"])
            res["J"]["combos"][f"{s}+{h}"] = dict(joint=r, J1=w1, J2=w2, J3=w3)
            print(f"  AGB1 {s:8s} + {h}: A {r['A']:+.3f} (68% {r['ci68'][0]} to {r['ci68'][1]})  dchi2(A=0) {r['D_A0']:.2f}  dchi2(A=1) {r['D_A1']:.2f}  {w1}")
            print(f"       q0 {r['q0']:+.3f}; q0 = 0: dchi2 {r['D_today']:.2f}  {w2};  never accelerated: dchi2 {r['D_never']:.2f}  {w3}   grid edges {r['edge']}")
        c = res["J"]["combos"]; first = c[f"full+{hk}"]["J1"]
        sec = second(first, {k: v["J1"] for k, v in c.items() if k != f"full+{hk}"})
        res["J"].update(J1=f"{first} / {sec}" if j_ok else "NOT EVALUABLE", J2=c[f"full+{hk}"]["J2"] if j_ok else "NOT EVALUABLE",
                        J3=c[f"full+{hk}"]["J3"] if j_ok else "NOT EVALUABLE")
        print(f"  -> J1: {res['J']['J1']}\n  -> J2: {res['J']['J2']}\n  -> J3: {res['J']['J3']}")
        for s in ("full", "des_only"):
            r = S[s]["joint"]["H2_R"]; n = S[s]["no_prior"]
            print(f"  reported, AGB1 {s} alone: A {n['A']:+.3f}  dchi2 {n['D_A0']:.2f} / {n['D_A1']:.2f}; with H2 (per host): A {r['A']:+.3f}"
                  f"  dchi2 {r['D_A0']:.2f} / {r['D_A1']:.2f}  [{word6(r['D_A0'], r['D_A1'])}]  q0 {r['q0']:+.3f}  today {r['D_today']:.2f}  never {r['D_never']:.2f}")
            print(f"  reported, host minus distances in combined errors ({s}): " + ", ".join(f"{k} {v:+.2f}" for k, v in S[s]["tension"].items()))
        res["J"]["reported"] = {s: dict(no_prior=S[s]["no_prior"], with_H2=S[s]["joint"]["H2_R"], tension=S[s]["tension"]) for s in S}
    with open(os.path.join(OUTDIR, "agb2_results.json"), "w") as fh: json.dump(res, fh, indent=1, default=float)
    print("\nwrote agb2_results.json")


if __name__ == "__main__":
    main()
