#!/usr/bin/env python3
"""CFG894 -- the kappa campaign register: counts, chance-hit (look-elsewhere) statistics, ledger tables.

Reads  kappa_attempts_register.csv   (this directory; one row per attempt, append-only)
       ledger_intro.md               (hand-written prose; placeholders {{...}} are filled here)
Writes KAPPA_ATTEMPTS_LEDGER.md      (intro + per-family tables rendered from the CSV)
       kappa_campaign_lee.json       (all numbers printed below)
stdout -> kappa_campaign_lee.out (redirect when running).

Light: Python standard library only, well under a second, single core.
Run from the repo root:
    nice -n 10 python3 campaign_fresh_gravity/CFG894_kappa_campaign_ledger/kappa_campaign_lee.py \
        > campaign_fresh_gravity/CFG894_kappa_campaign_ledger/kappa_campaign_lee.out
MUTATE=1 moves the hit window's centre from 0.417 to 0.300 (a control: the in-window counts and the
look-elsewhere numbers must change) and writes *_MUTATE outputs; it never touches the ledger .md.

Definitions (frozen in KAPPA_CAMPAIGN_RULES.md, section 7-8):
  law          a0 = kappa c sqrt(G rho_DE); kappa = 1/2 FITTED.
  W_data       [k_meas - 2 s, k_meas + 2 s] with the current primary measurement (CFG493 kappa_Lambda
               0.417 +- 0.095, file campaign_fresh_gravity/CFG493_kappa_combined/cfg493_kappa_combined.out).
  generator    the 'record-natural' option space: kappa^2 = (p/q) pi^k, 1 <= p,q <= 16, gcd(p,q) = 1,
               k in {-2..2}, kept if 0.05 <= kappa <= 5 (two decades around O(1)).
               class 'odd' = odd k only (the set an a-and-H-only route can reach: the L3b / CFG263
               pi-parity obstruction), class 'any' = all k (density routes), class 'cont' = log-uniform
               on [0.05, 5] (a transcendental root with no declared structure).
               Weightings: 'flat' (each distinct value equal) and 'simple' (weight 1/(p q (1+|k|)),
               which favours simple numbers such as 1/4 and is the conservative choice for chance hits).
  p_data(i)    generator mass inside W_data for attempt i's class.
  p_exact(i)   generator mass at kappa^2 = 1/4 exactly (zero for 'odd' and 'cont').
  P_LEE        1 - prod_i (1 - p(i)) over every counted trial: the chance that the campaign so far
               produces at least one hit if no route knows the true value.
"""
import csv
import json
import math
import os
import sys
from fractions import Fraction
from math import gcd, log, pi

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SUFFIX = "_MUTATE" if MUTATE else ""

# ---------------------------------------------------------------- inputs (all from committed files)
K_MEAS, K_SIG = 0.417, 0.095          # CFG493 kappa_Lambda (rho_DE footing)
K_MEAS_CRIT, K_SIG_CRIT = 0.345, 0.078  # CFG493 kappa_crit (rho_crit footing), reported only
if MUTATE:
    K_MEAS = 0.300
LO, HI = K_MEAS - 2 * K_SIG, K_MEAS + 2 * K_SIG
KAPPA_MIN, KAPPA_MAX = 0.05, 5.0
P_MAX, Q_MAX, K_POW = 16, 16, 2

VALID_CLS = {
    "odd": "determinate, a-and-H-only (kappa^2 in Q*pi^odd; cannot give 1/2 exactly)",
    "any": "determinate, density route (kappa^2 in Q*pi^k; can give 1/2)",
    "cont": "determinate, transcendental root (log-uniform reference)",
    "menu": "several values from admissible variants (non-determinate: never a hit)",
    "free": "condition only / free ratio / trade / bound / not selected (no number)",
    "pend": "registered, not yet run",
    "obs": "observational determination of kappa (not a derivation; not a trial)",
    "audit": "audit / meta / control (not a trial)",
    "lean": "logic or Lean formalisation (not a trial)",
    "nk": "kappa-blind lane listed for completeness (not counted)",
}
TRIAL_CLS = {"odd", "any", "cont", "menu"}
FAMILY_ORDER = [
    ("HT", "Horizon / thermodynamic (Unruh, Gibbons-Hawking, KMS, surface gravity)"),
    ("HE", "Holographic / entropic (BH entropy, CKN seesaw, Verlinde, entanglement, Jacobson)"),
    ("VM", "Vacuum-energy matching (the a0 sector's vacuum = rho_DE; kernel tails, BIMOND/QUMOND)"),
    ("FN", "Field-theory normalisation of W(u) / action coefficients (four-form, spectral, heat kernel, a0-as-field)"),
    ("PS", "16pi / 32pi / pi-counting and geometric structures (Gauss-Bonnet, SdS/Nariai, membranes, Tolman/Komar)"),
    ("GB", "Graviton bath / mode counting"),
    ("TA", "Topological / index / anomaly"),
    ("QG", "Quantum-gravity programmes (asymptotic safety, DSSYK, RG improvement)"),
    ("KS", "Kinetic / settling / collective / cold-energy dynamics"),
    ("CC", "Cosmological consistency (horizons, epochs, H0, unimodular, sequestering)"),
    ("NU", "Numerology and grammar searches (flagged)"),
    ("OB", "Observational determinations of kappa (NOT derivations)"),
    ("AU", "Audits, controls, meta-analyses"),
    ("LN", "Logic / Lean formalisations"),
    ("EX", "External pasted derivations"),
]
FAMILIES = dict(FAMILY_ORDER)

checks = []


def check(name, measured, ok, reading):
    checks.append({"name": name, "measured": measured, "ok": bool(ok), "reading": reading})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {measured} -- {reading}")


# ---------------------------------------------------------------- generator
def generator():
    vals = {}
    for k in range(-K_POW, K_POW + 1):
        for p in range(1, P_MAX + 1):
            for q in range(1, Q_MAX + 1):
                if gcd(p, q) != 1:
                    continue
                k2 = (p / q) * pi ** k
                kap = math.sqrt(k2)
                if KAPPA_MIN <= kap <= KAPPA_MAX:
                    vals[(Fraction(p, q), k)] = (kap, 1.0 / (p * q * (1 + abs(k))))
    return vals


def masses(vals, cls, weighting):
    tot = inw = ex = 0.0
    for (r, k), (kap, w) in vals.items():
        if cls == "odd" and k % 2 == 0:
            continue
        wt = 1.0 if weighting == "flat" else w
        tot += wt
        if LO <= kap <= HI:
            inw += wt
        if k == 0 and r == Fraction(1, 4):
            ex += wt
    return inw / tot, ex / tot, tot


def cont_masses():
    span = log(KAPPA_MAX / KAPPA_MIN)
    lo, hi = max(LO, KAPPA_MIN), min(HI, KAPPA_MAX)
    p_data = log(hi / lo) / span if hi > lo else 0.0
    p_near = log(1.01 / 0.99) / span
    return p_data, p_near


def p_lee(ps):
    prod = 1.0
    for p in ps:
        prod *= (1.0 - p)
    return 1.0 - prod


# ---------------------------------------------------------------- register
def read_register():
    path = os.path.join(HERE, "kappa_attempts_register.csv")
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    return rows


def as_float(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def options_of(row):
    opts = []
    for tok in (row.get("options") or "").split(";"):
        v = as_float(tok.strip())
        if v is not None:
            opts.append(v)
    return opts


def main():
    print("CFG894 kappa campaign register" + (" [MUTATE: window centre 0.300]" if MUTATE else ""))
    print(f"W_data (rho_DE footing) = [{LO:.3f}, {HI:.3f}]  from kappa = {K_MEAS} +- {K_SIG} (2 sigma)")
    print(f"rho_crit footing window = [{K_MEAS_CRIT - 2*K_SIG_CRIT:.3f}, {K_MEAS_CRIT + 2*K_SIG_CRIT:.3f}] (reported only)")
    print(f"1/2 inside W_data: {LO <= 0.5 <= HI};  0.4607 (KMS / 2pi) inside: {LO <= math.sqrt(2/(3*pi)) <= HI}")
    print()

    vals = generator()
    out = {"window": [LO, HI], "kappa_meas": K_MEAS, "kappa_sig": K_SIG, "mutate": MUTATE}
    gen = {}
    for cls in ("any", "odd"):
        for wtg in ("flat", "simple"):
            pd, pe, tot = masses(vals, cls, wtg)
            gen[f"{cls}_{wtg}"] = {"p_data": pd, "p_exact": pe}
    pdc, pnc = cont_masses()
    gen["cont"] = {"p_data": pdc, "p_exact": 0.0, "p_near_1pct": pnc}
    n_any = len(vals)
    n_odd = sum(1 for (r, k) in vals if k % 2)
    print(f"Generator: {n_any} distinct values (odd-pi subset {n_odd}) in kappa [{KAPPA_MIN}, {KAPPA_MAX}]")
    for key, d in gen.items():
        extra = f", p_near(+-1%) {d['p_near_1pct']:.4f}" if "p_near_1pct" in d else ""
        print(f"  {key:12s} p_data {d['p_data']:.4f}  p_exact(1/2) {d['p_exact']:.5f}{extra}")
    out["generator"] = gen
    quarter_in = sum(1 for (r, k) in vals if k == 0 and r == Fraction(1, 4))
    check("K1 generator holds kappa^2 = 1/4 exactly once", quarter_in, quarter_in == 1,
          "the exact target is in the reference option space once")
    check("K2 odd-pi class cannot reach 1/2", gen["odd_flat"]["p_exact"], gen["odd_flat"]["p_exact"] == 0.0,
          "pi-parity: an a-and-H-only route never lands on 1/2 exactly")
    print()

    rows = read_register()
    ids = [r["kid"] for r in rows]
    bad_cls = [r["kid"] for r in rows if r["cls"] not in VALID_CLS]
    bad_fam = [r["kid"] for r in rows if r["family"] not in FAMILIES]
    bad_num = [r["kid"] for r in rows if r["cls"] in {"odd", "any", "cont"} and as_float(r["kappa"]) is None]
    check("K3 register integrity", f"{len(rows)} rows; dup ids {len(ids) - len(set(ids))}; bad cls {bad_cls}; "
          f"bad family {bad_fam}; determinate rows without a number {bad_num}",
          len(ids) == len(set(ids)) and not bad_cls and not bad_fam and not bad_num,
          "every row has a unique id, a valid class and family; determinate rows carry a number")

    counted = [r for r in rows if r["cls"] != "nk"]
    deriv = [r for r in counted if r["family"] not in {"OB", "AU", "LN"}
             and r["cls"] not in {"obs", "audit", "lean"}]
    trials = [r for r in counted if r["cls"] in TRIAL_CLS]
    det = [r for r in trials if r["cls"] in {"odd", "any", "cont"}]
    menus = [r for r in trials if r["cls"] == "menu"]
    obs = [r for r in counted if r["cls"] == "obs"]
    pend = [r for r in counted if r["cls"] == "pend"]

    fam_counts = {}
    for f, _ in FAMILY_ORDER:
        sub = [r for r in counted if r["family"] == f]
        fam_counts[f] = {
            "rows": len(sub),
            "determinate": sum(1 for r in sub if r["cls"] in {"odd", "any", "cont"}),
            "menu": sum(1 for r in sub if r["cls"] == "menu"),
            "free": sum(1 for r in sub if r["cls"] == "free"),
            "pending": sum(1 for r in sub if r["cls"] == "pend"),
            "obs": sum(1 for r in sub if r["cls"] == "obs"),
        }
    print("Counts by family (rows / determinate / menu / no-number / pending / observational):")
    for f, d in fam_counts.items():
        print(f"  {f}  {d['rows']:4d} {d['determinate']:4d} {d['menu']:4d} {d['free']:4d} {d['pending']:4d} {d['obs']:4d}")
    print(f"Counted rows {len(counted)}; derivation/selection attempts {len(deriv)}; trials with a number "
          f"{len(trials)} (determinate {len(det)}, menus {len(menus)}); observational {len(obs)}; pending {len(pend)}; "
          f"kappa-blind listed {len(rows) - len(counted)}")
    out["counts"] = {"rows": len(rows), "counted": len(counted), "derivation_attempts": len(deriv),
                     "trials": len(trials), "determinate": len(det), "menus": len(menus),
                     "observational": len(obs), "pending": len(pend), "by_family": fam_counts}
    print()

    # empirical landing rates
    det_in = [r for r in det if LO <= as_float(r["kappa"]) <= HI]
    det_half = [r for r in deriv if r.get("half", "0") == "1"]
    menu_in = [r for r in menus if any(LO <= v <= HI for v in options_of(r))]
    emp_data = len(det_in) / len(det) if det else float("nan")
    emp_half = len(det_half) / len(deriv) if deriv else float("nan")
    print(f"Empirical: determinate predictions inside W_data {len(det_in)}/{len(det)} = {emp_data:.3f}")
    print("   ", "; ".join(f"{r['kid']} {r['src']} {r['kappa']}" for r in det_in))
    print(f"Empirical: derivation attempts that output exactly 1/2 (by insertion, posit, tuning, naming, circularity "
          f"or error; every one voided or conditional) {len(det_half)}/{len(deriv)} = {emp_half:.3f}")
    print("   ", "; ".join(f"{r['kid']} {r['src']}" for r in det_half))
    print(f"Empirical: menus with at least one option inside W_data {len(menu_in)}/{len(menus)}")
    out["empirical"] = {"det_in_window": len(det_in), "det": len(det), "rate_data": emp_data,
                        "half_outputs": len(det_half), "deriv": len(deriv), "rate_half": emp_half,
                        "menus_in_window": len(menu_in), "menus": len(menus),
                        "det_in_window_ids": [r["kid"] for r in det_in],
                        "half_ids": [r["kid"] for r in det_half]}
    print()

    # look-elsewhere
    def p_for(r, kind, wtg):
        cls = r["cls"]
        if cls == "cont":
            return gen["cont"]["p_data"] if kind == "data" else 0.0
        if cls in {"odd", "any"}:
            return gen[f"{cls}_{wtg}"]["p_data" if kind == "data" else "p_exact"]
        if cls == "menu":  # naive reading only: chance that at least one of n options lands
            n = max(1, len(options_of(r)))
            p1 = gen[f"any_{wtg}"]["p_data" if kind == "data" else "p_exact"]
            return 1.0 - (1.0 - p1) ** n
        return 0.0

    lee = {}
    for wtg in ("flat", "simple"):
        for kind in ("data", "exact"):
            ps_rules = [p_for(r, kind, wtg) for r in det]
            ps_naive = [p_for(r, kind, wtg) for r in trials]
            lee[f"{kind}_{wtg}"] = {
                "P_LEE_rules": p_lee(ps_rules), "expected_hits_rules": sum(ps_rules),
                "P_LEE_naive_with_menus": p_lee(ps_naive), "expected_hits_naive": sum(ps_naive)}
    print("Look-elsewhere over all counted trials (rules: determinate only; naive: menus included):")
    for key, d in lee.items():
        print(f"  {key:13s} P_LEE(rules) {d['P_LEE_rules']:.4f}  E[hits] {d['expected_hits_rules']:.2f}   "
              f"P_LEE(naive) {d['P_LEE_naive_with_menus']:.4f}  E[hits] {d['expected_hits_naive']:.2f}")
    out["lee"] = lee
    print(f"Observed data-level landings among determinate trials: {len(det_in)} "
          f"(expected under the null, flat weighting: {lee['data_flat']['expected_hits_rules']:.1f}; "
          f"simple weighting: {lee['data_simple']['expected_hits_rules']:.1f})")

    # what a future hit needs
    thr = 0.0027
    prev = lee["exact_simple"]["P_LEE_rules"]
    need = None if prev >= thr else 1.0 - (1.0 - thr) / (1.0 - prev)
    print(f"A new EXACT hit reaches campaign-level 3 sigma (P_LEE <= {thr}) only if prior budget < {thr}: "
          f"prior P_LEE(exact, simple) = {prev:.4f} -> "
          + ("IMPOSSIBLE on the hit alone; it must earn significance from an independent second prediction"
             if need is None else f"needs p_new <= {need:.5f}"))
    out["future_exact_hit_needs"] = need
    check("K4 empirical data-level rate is within the generator range",
          f"{emp_data:.3f} vs p_data any_flat {gen['any_flat']['p_data']:.3f} / any_simple {gen['any_simple']['p_data']:.3f}",
          True, "reported, not graded: a rate far above the generator would hint that routes home in on kappa")
    print()

    # render ledger
    if not MUTATE:
        intro_path = os.path.join(HERE, "ledger_intro.md")
        intro = open(intro_path).read()
        repl = {
            "{{N_ROWS}}": str(len(rows)), "{{N_COUNTED}}": str(len(counted)),
            "{{N_DERIV}}": str(len(deriv)), "{{N_TRIALS}}": str(len(trials)), "{{N_DET}}": str(len(det)),
            "{{N_MENU}}": str(len(menus)), "{{N_OBS}}": str(len(obs)), "{{N_PEND}}": str(len(pend)),
            "{{N_DET_IN}}": str(len(det_in)), "{{N_HALF}}": str(len(det_half)),
            "{{WINDOW}}": f"[{LO:.3f}, {HI:.3f}]",
        }
        for k, v in repl.items():
            intro = intro.replace(k, v)
        lines = [intro.rstrip(), "", "## Counts by family", "",
                 "| family | rows | determinate | menu | no number | pending | observational |",
                 "|---|---|---|---|---|---|---|"]
        for f, d in fam_counts.items():
            lines.append(f"| {f} {FAMILIES[f]} | {d['rows']} | {d['determinate']} | {d['menu']} | {d['free']} | "
                         f"{d['pending']} | {d['obs']} |")
        lines += ["", "Class key: " + "; ".join(f"`{k}` {v}" for k, v in VALID_CLS.items()) + ".", ""]
        for f, title in FAMILY_ORDER:
            sub = [r for r in rows if r["family"] == f]
            if not sub:
                continue
            lines += [f"## {f}: {title}", "",
                      "| id | source | path | mechanism | kappa (or options) | class | verdict | commit |",
                      "|---|---|---|---|---|---|---|---|"]
            for r in sub:
                kap = r["kappa"] or (("{" + r["options"].replace(";", ", ") + "}") if r["options"] else "-")
                cell = lambda s: (s or "").replace("|", "/")
                lines.append(f"| {r['kid']} | {cell(r['src'])} | `{cell(r['path'])}` | {cell(r['mechanism'])} | "
                             f"{cell(kap)} | {r['cls']} | {cell(r['verdict'])} | {cell(r['commit'])} |")
            lines.append("")
        with open(os.path.join(HERE, "KAPPA_ATTEMPTS_LEDGER.md"), "w") as fh:
            fh.write("\n".join(lines) + "\n")
        print("Wrote KAPPA_ATTEMPTS_LEDGER.md")

    if MUTATE:
        base_path = os.path.join(HERE, "kappa_campaign_lee.json")
        try:
            base = json.load(open(base_path))
            b_in = base["empirical"]["det_in_window"]
            b_lee = base["lee"]["data_flat"]["expected_hits_rules"]
            moved = (b_in != len(det_in)) and abs(b_lee - lee["data_flat"]["expected_hits_rules"]) > 1e-9
            check("M1 window-centre mutation moves the in-window count and the expected chance hits",
                  f"in-window {b_in} -> {len(det_in)}; E[hits] {b_lee:.2f} -> {lee['data_flat']['expected_hits_rules']:.2f}",
                  moved, "the control bites: the statistics depend on the declared window, not on a hard-coded result")
        except FileNotFoundError:
            check("M1 needs the normal-run JSON", base_path, False, "run without MUTATE first")

    out["checks"] = checks
    with open(os.path.join(HERE, f"kappa_campaign_lee{SUFFIX}.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    n_fail = sum(1 for c in checks if not c["ok"])
    print(f"checks: {len(checks) - n_fail}/{len(checks)} pass")
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
