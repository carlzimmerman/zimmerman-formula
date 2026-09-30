"""CFG230 script F: incidence matrix analysis (hard-core set H, exhaustive minimum cover, support, fragile requirements), the 4.5 pincers
(documentary), and MUTATE M1 (drop D02 and D04), M2 (placebo: drop D06), M7 (AQUAL-relabelled row and the target-as-input detector)."""
import itertools, math, re
import CFG230_common as C
import CFG230_data as D

R = C.Run("CFG230_F_incidence_pincers")
M = C.mode()
R.p(f"CFG230 F. repo=<repo> mode={M or 'main'}")

def theorem_core(req, amend=False):
    sub = (D.SUB_AMEND1 if amend else D.SUB)[req]
    return any(cl == "THEOREM" and lb for (_, cl, gr, lb) in sub)

def analyse(matrix, label):
    reqs = D.REQS
    H = [r for i, r in enumerate(reqs) if not any(v[i] == "P" for v in matrix.values())]
    failed = [k for k, v in matrix.items() if "F" in v]
    covers = []
    for k in range(1, len(reqs) + 1):
        for S in itertools.combinations(range(len(reqs)), k):
            if all(any(matrix[row][i] == "F" for i in S) for row in failed):
                covers.append(S)
        if covers:
            break
    support = {r: [k for k, v in matrix.items() if v[i] == "F"] for i, r in enumerate(reqs)}
    sole = {r: [k for k, v in matrix.items() if v[i] == "F" and sum(1 for c in v if c == "F") == 1] for i, r in enumerate(reqs)}
    fragile = [r for r in reqs if len(support[r]) <= 2 and not theorem_core(r)]
    listed = [r for r in reqs if support[r] or theorem_core(r)]
    return dict(H=H, failed=failed, mincover_size=len(covers[0]) if covers else None,
                mincovers=[[reqs[i] for i in S] for S in covers], support=support, sole=sole, fragile=fragile, listed=listed)

base = analyse(D.MATRIX, "base")
R.p("\n== baseline (frozen matrix)")
R.p(f"  hard-core set H = {base['H']} (|H| = {len(base['H'])}); HAND expectation H = R03..R12 (10)")
R.check("EXPECT", "|H| = 10 and H = R03..R12", base["H"] == D.REQS[2:], str(base["H"]))
R.p(f"  failed rows (>= 1 F): {len(base['failed'])} of {len(D.MATRIX)}: {base['failed']}")
R.p(f"  exhaustive minimum cover of the failed rows by requirements they violate (2^12 subsets): size {base['mincover_size']}, {len(base['mincovers'])} minimum cover(s)")
for c in base["mincovers"][:20]:
    R.p("    " + ", ".join(c))
R.check("EXPECT", "minimum cover size 3-4 (HAND)", base["mincover_size"] in (3, 4), f"size {base['mincover_size']}")
def mincover_restricted(allowed):
    idx = [D.REQS.index(r) for r in allowed]
    for k in range(1, len(idx) + 1):
        cs = [S for S in itertools.combinations(idx, k) if all(any(D.MATRIX[row][i] == "F" for i in S) for row in base["failed"])]
        if cs:
            return k, [[D.REQS[i] for i in S] for S in cs]
    return None, []
thm = [r for r in D.REQS if theorem_core(r)]
k1, c1 = mincover_restricted(thm)
k2, c2 = mincover_restricted([r for r in D.REQS if r != "R03"])
R.p(f"  minimum cover using only requirements with a THEOREM core {thm}: size {k1}: {c1[:8]}")
R.p(f"  minimum cover excluding the DECLARED-CHOICE requirement R03: size {k2}: {c2[:8]}")
R.res["mincover_theorem_core_only"] = [k1, c1]; R.res["mincover_without_R03"] = [k2, c2]
R.p("  reading: the cover is a statement about which requirement labels explain the scored failures, not about which are necessary or sufficient for a mechanism; a small cover shows heavy overlap between requirements.")
R.p("  support (rows with F) per requirement:")
for r in D.REQS:
    R.p(f"    {r}: {len(base['support'][r])} rows {base['support'][r]}  theorem-core={theorem_core(r)}")
R.p(f"  rows where a requirement is the ONLY F of the row: { {r: v for r, v in base['sole'].items() if v} or 'none' }")
R.p(f"  FRAGILE (support <= 2 rows and no THEOREM core): {base['fragile']}")
R.p(f"  zero-support requirements (no scored row shows an F): {[r for r in D.REQS if not base['support'][r]]}: they rest on their theorem core, not on door failures")
R.res["baseline"] = base
R.check("EXPECT", "stop condition of the frozen plan: not more than three requirements UNSUPPORTED or FRAGILE", len(base["fragile"]) <= 3, f"fragile: {base['fragile']}")

# ---------------------------------------------------------------- pincers
R.p("\n== 4.5 pincers (documentary; gap sizes as printed by the lanes)")
n_ok = 0
for pair, stmt, gap, anc in D.PINCERS:
    ok = True
    if anc:
        t = C.read_norm(anc[0]); ok = t is not None and C.norm(anc[1]) in t
    n_ok += ok
    gs = ""
    if gap:
        g = [v for v in gap if v]
        gs = " gap(s) " + ", ".join(f"{v:g} ({math.log10(v):+.2f} dex)" for v in g if v > 0)
    R.p(f"  [{pair}] {stmt};{gs} anchor {'present' if ok else 'ABSENT'}")
R.check("CITATION-AUDIT", "every pincer anchor present in its source", n_ok == len(D.PINCERS), f"{n_ok}/{len(D.PINCERS)}")
R.check("EXPECT", "E10 pincer arithmetic: 4e6/1.2e-6 = 3.3e12; 3.72e6/1.24e-6 = 3.0e12; 140/0.16 = 875; 140/1.2 = 117", abs(4e6 / 1.2e-6 - 3.33e12) < 1e11 and abs(3.72e6 / 1.24e-6 - 3.0e12) < 1e11 and abs(140 / 0.16 - 875) < 1 and abs(140 / 1.2 - 116.7) < 1, f"{4e6/1.2e-6:.3g}, {3.72e6/1.24e-6:.3g}, {140/0.16:.0f}, {140/1.2:.0f}")
R.p("  pincer (R12(b) x R04): P_target/P_cap = 1/x^2, computed in script D (E13); the P43 window (11x up to 1e4-1e5 against ~1e4) is cited.")

# ---------------------------------------------------------------- MUTATE
def drop(rows):
    return {k: v for k, v in D.MATRIX.items() if k not in rows}
if M == "M1":
    a = analyse(drop(["D02"]), "drop D02"); b = analyse(drop(["D04"]), "drop D04"); ab = analyse(drop(["D02", "D04"]), "drop both")
    R.p(f"  M1a drop D02: H = {a['H']} (R01 in H: {'R01' in a['H']})")
    R.p(f"  M1b drop D04: H = {b['H']} (R02 in H: {'R02' in b['H']}; D02 still has P on R02)")
    R.p(f"  M1c drop both: H = {ab['H']}")
    R.res["M1"] = {"D02": a["H"], "D04": b["H"], "both": ab["H"]}
    C.bite(R, ab["H"] != base["H"] or a["H"] != base["H"], f"|H| {len(base['H'])} -> {len(a['H'])} (drop D02), {len(b['H'])} (drop D04), {len(ab['H'])} (both)")
if M == "M2":
    a = analyse(drop(["D06"]), "drop D06")
    R.p(f"  M2 (placebo) drop D06: H = {a['H']}; requirements still listed = {len(a['listed'])} (baseline {len(base['listed'])}); support R01 {len(base['support']['R01'])} -> {len(a['support']['R01'])}; R02 theorem core intact = {theorem_core('R02')}")
    same = a["H"] == base["H"] and a["listed"] == base["listed"]
    R.res["M2"] = {"H_same": a["H"] == base["H"], "listed_same": a["listed"] == base["listed"]}
    C.bite(R, not same, "expected NOT to bite: the requirement list and H do not depend on D06 (R02a is a theorem independent of it)" if same else "the requirement list or H changed: something depends on D06")
if M == "M7":
    naive = {k: list(v) for k, v in D.MATRIX.items()}
    naive["AQUAL_relabelled"] = ["P", "P", "P", "P", "N", "N", "N", "N", "N", "N", "N", "N"]
    with_det = {k: list(v) for k, v in naive.items()}
    with_det["AQUAL_relabelled"][:4] = ["p*", "p*", "p*", "p*"]      # target-as-input flag forces p*
    hn = analyse(naive, "naive")["H"]; hd = analyse(with_det, "detector")["H"]
    R.p(f"  M7: fictitious row 'AQUAL relabelled' (target is its input). H naive = {hn}; H with the target-as-input detector = {hd}; baseline {base['H']}")
    R.res["M7"] = {"naive": hn, "detector": hd}
    C.bite(R, hn != base["H"] and hd == base["H"], "the naive rule would shrink H; the target-as-input detector restores it (the detector is load-bearing)")
R.write()
