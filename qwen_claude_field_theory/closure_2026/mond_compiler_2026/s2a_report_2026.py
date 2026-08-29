"""
s2a_report_2026.py -- STAGE 2A consolidated certificate table.

Merges s2a_certificates_part1.json (exact static gates) and
s2a_certificates_part2.json (exact G4 / G5) into one per-candidate, per-gate ledger.
"""
import json
import textwrap

ORDER = ["C1_MAXWELL_AETHER_BEKENSTEIN",
         "C2_ALGEBRAIC_AETHER_NO_KINETIC_TERM",
         "C3_ALGEBRAIC_TRACELESS_TENSOR",
         "(general aether)", "(all vector-carrier candidates)",
         "(all tensor-carrier candidates)", "(all three)", "(basis)", "(pipeline)"]

VERDICT = {
    "C1_MAXWELL_AETHER_BEKENSTEIN":
        ("Gate-PPN / G4 + G5",
         "PASSES G1 (mu(y) closed form, k^2 = 3 sqrt 2), G2 (Bekenstein M5 = 4 M1) and "
         "G3 (once G_N is the measured constant).  DIES on G5 and G4 together: its only "
         "vector-kinetic operator F_mn F^mn is blind to the longitudinal aether mode "
         "(c123 = 0 exactly), so that mode has a finite time-kinetic term and ZERO "
         "gradient term -- infinite strong coupling, not a second-class constraint -- "
         "and the Bekenstein disformal coupling that supplies G2 sources exactly that "
         "mode as soon as matter moves.  alpha_2 is a pole, not a large number; "
         "alpha_1 = -2."),
    "C2_ALGEBRAIC_AETHER_NO_KINETIC_TERM":
        ("Gate-PPN / G4 + G5",
         "PASSES G1, G2, G3.  DIES on G5 and G4 together: the aether has NO derivative "
         "operator at all, so the three boost moduli of A_mu have no field equation; the "
         "transverse projection of the A-equation annihilates the whole carrier side and "
         "leaves an over-determining constraint on MATTER, v = w_aether."),
    "C3_ALGEBRAIC_TRACELESS_TENSOR":
        ("Gate-PPN / G4 + G5",
         "PASSES G1, G2 (M6 = 6 M1/S_00 = 4 sqrt 3 M1 at the exact vacuum "
         "S_00 = sqrt(3)/2), G3.  DIES on G5 and G4 together: the tensor is purely "
         "algebraic, so its six Lorentz-orbit moduli are undetermined functions in "
         "vacuum, and where matter is present the equation forces [S, T~] = 0."),
}


# explicit GATE OUTCOME table.  Every cell is backed by a certificate printed below.
GATES = ["G1 MOND", "G2 LENSING", "G3 NEWTON", "G4 PPN-DARK", "G5 HEALTH"]
OUTCOME = {
    "C1_MAXWELL_AETHER_BEKENSTEIN": [
        ("PASS", "PROVEN", "mu(y) = [(sqrt(k^2+4y)-k)/2]^2/y, k^2 = 3 sqrt 2 exact; "
                           "mu->1 and mu->y/k^2 proved as limits"),
        ("PASS", "PROVEN", "Phi~' - Psi~' = 0 on shell; requires M5 = 4 M1 (1-M3)"),
        ("PASS*", "PROVEN", "G_eff/G_N -> 1, but the aether renormalises the BARE G by "
                            "4/3 = 1/(1-c14/2); stage 1 missed this (A01 = Phi1, not 0)"),
        ("FAIL", "PROVEN", "c123 = 0 exactly -> the quasi-static longitudinal operator "
                           "D(k) = (c1-c4) k^2 (k.v)^2 vanishes on the whole plane k.v=0 "
                           "where the G2-forced source lives.  The only regulator, the "
                           "multiplier background lam_bar, is O(G rho) and vanishes in "
                           "vacuum where alpha_2 is defined -> alpha_2 is a POLE "
                           "(scope certificate PARTIAL).  alpha_1 = -2 (Foster-Jacobson "
                           "cross-check, ASSUMED)"),
        ("FAIL", "PROVEN", "longitudinal mode: time-kinetic coefficient 1/2, gradient "
                           "coefficient 0 -> c_s^2 = 0.  Infinite strong coupling, NOT a "
                           "second-class constraint"),
    ],
    "C2_ALGEBRAIC_AETHER_NO_KINETIC_TERM": [
        ("PASS", "COMPUTATIONALLY_VERIFIED", "same cubic AQUAL, k^2 = 0.7980"),
        ("PASS", "COMPUTATIONALLY_VERIFIED", "M5 = 4 M1 to the printed precision of the "
                                             "stage-1 floats; exactly 0 slip at M5 = 4 M1"),
        ("PASS", "PROVEN", "kinetic-free aether -> no renormalisation, Phi1 = Psi1 = "
                           "Sigma/8 exactly"),
        ("FAIL", "PROVEN", "transverse A-equation is not an equation for A: it forces "
                           "(v - w_aether)(v w_aether - 1) = 0, i.e. matter must be "
                           "comoving with the aether"),
        ("FAIL", "PROVEN", "the 3 boost moduli of A_mu have identically zero action and "
                           "no secondary constraint: undetermined functions, not "
                           "second-class constraints"),
    ],
    "C3_ALGEBRAIC_TRACELESS_TENSOR": [
        ("PASS", "PROVEN", "chi eliminated from a CUBIC; mu(y) is still an output, no "
                           "free function"),
        ("PASS", "PROVEN", "M6 = 6 M1 / S_00 with the exact vacuum S_00 = sqrt(3)/2, "
                           "i.e. M6 = 4 sqrt(3) M1 -- matches the stage-1 float to 15 "
                           "digits"),
        ("PASS", "PROVEN", "no derivative operator for S -> metric sector is pure GR"),
        ("FAIL", "PROVEN", "the carrier side of the S-equation is a matrix polynomial in "
                           "S, so it commutes with S; the equation therefore forces "
                           "[S, T~] = 0"),
        ("FAIL", "PROVEN", "the 6 Lorentz-orbit moduli of the S-VEV have identically "
                           "zero action: undetermined functions in vacuum"),
    ],
}


def gate_table():
    print("\n" + "=" * 92)
    print("GATE OUTCOME TABLE  (every cell backed by a certificate below)")
    print("=" * 92)
    print(f"  {'candidate':36s} " + " ".join(f"{g:12s}" for g in GATES))
    for cand, rows in OUTCOME.items():
        print(f"  {cand:36s} " + " ".join(f"{r[0]:12s}" for r in rows))
    print("\n  * G3 PASS with a recorded diagnostic (bare-G renormalisation 4/3).")
    print("\n  why each cell:")
    for cand, rows in OUTCOME.items():
        print(f"\n  {cand}")
        for g, (out, st, why) in zip(GATES, rows):
            print(f"     {g:12s} {out:6s} [{st}]")
            for line in textwrap.wrap(why, 78):
                print(f"        {line}")


def main():
    gate_table()
    recs = []
    for f in ["s2a_certificates_part1.json", "s2a_certificates_part2.json"]:
        with open(f) as fh:
            recs += json.load(fh)
    print("=" * 92)
    print("STAGE 2A -- CONSOLIDATED CERTIFICATE LEDGER")
    print("=" * 92)
    print(f"total certificates: {len(recs)}")
    counts = {}
    for r in recs:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print("by status: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))

    for cand in ORDER:
        rs = [r for r in recs if r["candidate"] == cand]
        if not rs:
            continue
        print("\n" + "-" * 92)
        print(cand)
        if cand in VERDICT:
            g, txt = VERDICT[cand]
            print(f"   VERDICT: dies at {g}")
            for line in textwrap.wrap(txt, 86):
                print("     " + line)
        print("-" * 92)
        for r in rs:
            print(f"  [{r['status']:26s}] {r['gate']}")
            for line in textwrap.wrap(r["claim"], 84):
                print(f"        {line}")
            if r["residual"]:
                for line in textwrap.wrap("residual: " + r["residual"], 84)[:6]:
                    print(f"        {line}")
    leftover = [r for r in recs if r["candidate"] not in ORDER]
    for r in leftover:
        print(f"\n  [{r['status']}] {r['candidate']} {r['gate']}")
    print("\n" + "=" * 92)


if __name__ == "__main__":
    main()
