#!/usr/bin/env python3
"""N3 -- scale and scheme systematics of the tower emergence closures (pre-registration: N2_PREREGISTRATION.md, criterion N4/N6 bands).
Run:    PYTHONDONTWRITEBYTECODE=1 python3 n3_scale_scheme.py          (exit 0 iff the integrity checks pass)
MUTATE: PYTHONDONTWRITEBYTECODE=1 python3 n3_scale_scheme.py MUTATE   (positional argv; the number of tower states counted below Lambda_sp uses ceil(x) instead of floor(x);
                                                                       the independent recount of levels with m_j <= Lambda_sp must then fail -> exit 1)
Systematics (each closure re-solved with the modulus M_c re-fitted to the same measured coupling):
  (a) Lambda_sp -> c Lambda_sp, c in {1/2, 2}: Lambda^2 N = (c M_red)^2 (the O(1) coefficient of the species bound is not derived);
  (b) hard-cutoff scheme constant of lane J: c_hard = -0.2804 per ln(Lambda^2/m^2) of a unit-charge Dirac fermion (b = 4/3), i.e. kappa = 0.2804/(3 pi)/(4/3) = 0.02231 per unit b, applied with both signs to
      every state (SM zero modes + tower) as an ORDER-OF-MAGNITUDE estimate (the constant for scalars and vectors is not computed);
  (c) decomposition of F_i into SM log part, tower linear (5D divergence) part and the -(1/2) ln(2 pi x) boundary part.
Not included (each would only enlarge the band): two-loop coefficients, SM threshold structure between M_Z and M_c (top, Higgs), tower Yukawa/mass corrections, brane-localised terms.
"""
import sys, json, math
sys.dont_write_bytecode = True
import tower_lib as T

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
fails = []
def chk(n, ok, m=""):
    print(("[PASS] " if ok else "[FAIL] ") + n + (" " + m if m else ""))
    if not ok: fails.append(n)

KAPPA = 0.2804 / (4 * math.pi)
print("kappa (lane J hard-cutoff constant per unit b) = %.5f" % KAPPA)
base = json.load(open("n2_results.json"))
res = {}
for tw, tag in ((T.TA, "TA"), (T.TB, "TB")):
    for i in range(3):
        b0 = base["%s|%s|G" % (tag, T.NAMES[i])]
        if not b0:
            print("[%s closure %s] no root in the base solve: nothing to band" % (tag, T.NAMES[i])); continue
        s0 = T.summarize(b0[0]["Mc"], tw)
        chk("[%s,%s] base root reproduced from n2_results.json" % (tag, T.NAMES[i]), abs(T.find_roots(i, tw)[0][0] / b0[0]["Mc"] - 1) < 1e-9)
        k_used = math.ceil(s0["x"]) if MUT else s0["k"]
        chk("[%s,%s] independent recount: tower levels with m_j <= Lambda_sp equals k" % (tag, T.NAMES[i]), s0["pinned"] or k_used == sum(1 for j in range(1, 10000) if j * s0["Mc"] <= s0["Lambda"] * (1 + 1e-12)), "k used %d, recount %d" % (k_used, sum(1 for j in range(1, 10000) if j * s0["Mc"] <= s0["Lambda"] * (1 + 1e-12))))
        row = dict(em0=s0["em_0"], x=s0["x"], Mc=s0["Mc"])
        # (a) scale factor
        ac = []
        for c in (0.5, 2.0):
            r, _ = T.find_roots(i, tw, M=c * T.M_RED)
            if not r: ac.append(None); continue
            sc = T.summarize(r[0], tw, M=c * T.M_RED)
            ac.append(dict(c=c, em0=sc["em_0"], x=sc["x"], Mc=sc["Mc"], Lam=sc["Lambda"]))
        band_c = max(abs(a["em0"] - s0["em_0"]) for a in ac if a) if any(ac) else float("nan")
        # (b) scheme constant
        sb = []
        for sg in (+1.0, -1.0):
            r, _ = T.find_roots(i, tw, shift_sign=sg, kappa=KAPPA)
            if not r: sb.append(None); continue
            ss = T.summarize(r[0], tw, shift_sign=sg, kappa=KAPPA)
            sb.append(dict(sign=sg, em0=ss["em_0"], x=ss["x"], Mc=ss["Mc"]))
        band_s = max(abs(a["em0"] - s0["em_0"]) for a in sb if a) if any(sb) else float("nan")
        band = math.hypot(band_c, band_s)
        tot_b = [T.BSM[j] + s0["bsum"][j] for j in range(3)]
        shift_size = [KAPPA * t for t in tot_b]
        # (c) decomposition of F_Y, F_2, F_3
        lev = T._lev(tw, 1, True)[2]
        dec = []
        for j in range(3):
            sm = T.BSM[j] * s0["lnL"] / T.TWO_PI
            lin = lev[j] * s0["x"] / T.TWO_PI * (1 if tw is not T.TC else 0)
            bnd = -lev[j] * 0.5 * math.log(2 * math.pi * s0["x"]) / T.TWO_PI
            dec.append((sm, lin, bnd, s0["F"][j]))
        print("\n[%s, closure %s] x = %.2f, M_c = %.3e; base 1/alpha_em(0) = %.3f" % (tw.name, T.NAMES[i], s0["x"], s0["Mc"], s0["em_0"]))
        for a in ac:
            if a: print("   (a) c = %.1f: x = %.2f, Lambda_sp = %.3e, 1/alpha_em(0) = %.3f (shift %+.3f)" % (a["c"], a["x"], a["Lam"], a["em0"], a["em0"] - s0["em_0"]))
        for a in sb:
            if a: print("   (b) scheme shift sign %+d: x = %.2f, 1/alpha_em(0) = %.3f (shift %+.3f)" % (a["sign"], a["x"], a["em0"], a["em0"] - s0["em_0"]))
        print("   (b') size of the scheme shift kappa*(b_SM + sum b_tower) in 1/alpha_(Y,2,3): (%.2f, %.2f, %.2f)" % tuple(shift_size))
        for j in range(3):
            sm, lin, bnd, F = dec[j]
            print("   (c) F_%s = %.3f = SM log %.3f + tower linear %.3f + boundary %.3f (+ O(1/x) %.3f); linear share of |F| = %.0f %%" % (T.NAMES[j], F, sm, lin, bnd, F - sm - lin - bnd, 100 * abs(lin) / max(abs(F), 1e-9)))
        print("   band on 1/alpha_em(0): scale %.3f, scheme %.3f, quadrature %.3f = %.2f %% of 137.036" % (band_c, band_s, band, 100 * band / T.ALPHA_INV0))
        row.update(band_c=band_c, band_s=band_s, band=band, a=ac, b=sb, shift_size=shift_size, resid=list(s0['resid']))
        res["%s|%s" % (tag, T.NAMES[i])] = row
        # residuals of the non-fitted couplings against their bands (N4 test) at this closure root
        rr = s0["resid"]
        print("   implied 1/alpha at Lambda_sp: Y %.2f  2 %.2f  3 %.2f (emergence needs 0); scale-only spread of these under c=1/2,2: " % tuple(rr) +
              ", ".join("c=%.1f: (%s)" % (a["c"], ", ".join("%.1f" % (T.MEAS[j] - T.summarize(a["Mc"], tw, M=a["c"] * T.M_RED)["F"][j]) for j in range(3))) for a in ac if a))
chk("all bands finite for the solved closures", all(math.isfinite(v["band"]) for v in res.values()))
json.dump(res, open("n3_results_MUTATE.json" if MUT else "n3_results.json", "w"), indent=1, default=float)
print("SUMMARY: fails =", fails)
sys.exit(1 if fails else 0)
